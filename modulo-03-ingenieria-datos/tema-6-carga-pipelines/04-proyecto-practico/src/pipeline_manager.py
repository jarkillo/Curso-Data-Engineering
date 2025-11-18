"""
Módulo para orquestar pipelines completos.

Integra todos los módulos de carga y proporciona una interfaz unificada.
"""

import logging
from datetime import datetime

import pandas as pd
from sqlalchemy import Engine
from src.cargador_full import full_load
from src.cargador_incremental import incremental_load
from src.cargador_upsert import upsert
from src.metrics_collector import PipelineMetrics

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def seleccionar_estrategia_carga(df: pd.DataFrame) -> str:
    """
    Selecciona automáticamente la estrategia de carga.

    Args:
        df: DataFrame a analizar

    Returns:
        Estrategia recomendada: "full", "incremental", o "upsert"

    Examples:
        >>> df = pd.DataFrame({"id": range(500)})
        >>> estrategia = seleccionar_estrategia_carga(df)
        >>> print(estrategia)
        'full'
    """
    # Dataset pequeño -> full load
    if len(df) < 1000:
        return "full"

    # Tiene timestamp -> incremental
    timestamp_cols = ["timestamp", "created_at", "fecha", "date"]
    for col in timestamp_cols:
        if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
            return "incremental"

    # Tiene ID -> upsert
    if "id" in df.columns or any("id" in col.lower() for col in df.columns):
        return "upsert"

    # Default: full load
    return "full"


def validar_datos_pipeline(
    df: pd.DataFrame,
    columnas_requeridas: list[str] | None = None,
    columnas_no_nulas: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Valida datos y separa válidos de inválidos.

    Args:
        df: DataFrame a validar
        columnas_requeridas: Columnas que deben existir
        columnas_no_nulas: Columnas que no deben tener nulos

    Returns:
        Tupla (df_valido, df_invalido)

    Raises:
        ValueError: Si faltan columnas requeridas

    Examples:
        >>> df_valido, df_invalido = validar_datos_pipeline(
        ...     df,
        ...     columnas_requeridas=["id", "valor"]
        ... )
    """
    # Validar columnas requeridas
    if columnas_requeridas:
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if columnas_faltantes:
            raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")

    # Filtrar registros inválidos (con nulos en columnas críticas)
    df_valido = df.copy()

    if columnas_no_nulas:
        mask_valido = pd.Series([True] * len(df))
        for col in columnas_no_nulas:
            if col in df.columns:
                mask_valido &= df[col].notna()

        df_valido = df[mask_valido].copy()
        df_invalido = df[~mask_valido].copy()
    else:
        df_invalido = pd.DataFrame()

    return df_valido, df_invalido


def ejecutar_pipeline(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    estrategia: str = "auto",
    validar: bool = False,
    columnas_requeridas: list[str] | None = None,
    columnas_no_nulas: list[str] | None = None,
    columna_timestamp: str | None = None,
    columna_clave: str | None = None,
    checkpoint_file: str = "checkpoint.txt",
) -> PipelineMetrics:
    """
    Ejecuta pipeline completo de carga.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        estrategia: "full", "incremental", "upsert", o "auto"
        validar: Si aplicar validación previa
        columnas_requeridas: Columnas que deben existir
        columnas_no_nulas: Columnas que no deben tener nulos
        columna_timestamp: Columna para incremental load
        columna_clave: Columna clave para upsert
        checkpoint_file: Archivo de checkpoint

    Returns:
        PipelineMetrics con resultados

    Examples:
        >>> resultado = ejecutar_pipeline(
        ...     df,
        ...     engine,
        ...     "tabla",
        ...     estrategia="full"
        ... )
        >>> print(f"Éxito: {resultado.success}")
    """
    metricas = PipelineMetrics(start_time=datetime.now())

    try:
        logger.info(f"=== Iniciando pipeline para tabla '{tabla}' ===")
        metricas.rows_extracted = len(df)
        logger.info(f"Filas extraídas: {metricas.rows_extracted}")

        # Seleccionar estrategia
        if estrategia == "auto":
            estrategia = seleccionar_estrategia_carga(df)
            logger.info(f"Estrategia auto-seleccionada: {estrategia}")
        else:
            logger.info(f"Estrategia: {estrategia}")

        # Validar datos si se solicita
        if validar:
            logger.info("Validando datos...")
            df_valido, df_invalido = validar_datos_pipeline(
                df, columnas_requeridas, columnas_no_nulas
            )
            metricas.rows_validated = len(df_valido)
            metricas.rows_failed = len(df_invalido)
            logger.info(
                f"Válidos: {metricas.rows_validated}, Inválidos: {metricas.rows_failed}"
            )

            if metricas.rows_failed > 0:
                logger.warning(
                    f"{metricas.rows_failed} registros inválidos serán omitidos"
                )

            df = df_valido

        # Ejecutar carga según estrategia
        logger.info(f"Ejecutando carga con estrategia '{estrategia}'...")

        if estrategia == "full":
            num_cargados = full_load(df, engine, tabla)
            metricas.rows_loaded = num_cargados

        elif estrategia == "incremental":
            if not columna_timestamp:
                # Intentar detectar columna timestamp
                timestamp_cols = ["timestamp", "created_at", "fecha"]
                for col in timestamp_cols:
                    if col in df.columns:
                        columna_timestamp = col
                        break

            if not columna_timestamp:
                raise ValueError("Estrategia incremental requiere columna_timestamp")

            resultado = incremental_load(
                df, engine, tabla, columna_timestamp, checkpoint_file
            )
            metricas.rows_loaded = resultado["cargados"]

        elif estrategia == "upsert":
            if not columna_clave:
                # Intentar detectar columna clave
                if "id" in df.columns:
                    columna_clave = "id"
                else:
                    for col in df.columns:
                        if "id" in col.lower():
                            columna_clave = col
                            break

            if not columna_clave:
                raise ValueError("Estrategia upsert requiere columna_clave")

            upsert(df, engine, tabla, columna_clave)
            metricas.rows_loaded = len(df)

        else:
            raise ValueError(f"Estrategia '{estrategia}' no soportada")

        metricas.success = True
        logger.info("✅ Pipeline completado exitosamente")
        logger.info(f"Filas cargadas: {metricas.rows_loaded}")

    except Exception as e:
        metricas.success = False
        metricas.error_message = str(e)
        logger.error(f"❌ Error en pipeline: {e}", exc_info=True)

    finally:
        metricas.finalize()
        logger.info(f"Duración: {metricas.duration_seconds:.2f} segundos")

    return metricas
