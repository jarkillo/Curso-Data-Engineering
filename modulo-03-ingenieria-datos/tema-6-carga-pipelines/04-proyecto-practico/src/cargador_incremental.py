"""
Módulo para estrategia de carga incremental.

Implementa funciones para cargar solo registros nuevos desde el último checkpoint.

SECURITY NOTE: SQL Injection y Nombres de Tablas
------------------------------------------------
Este módulo usa f-strings para insertar nombres de tabla en queries SQL.
Esto es SEGURO porque se validan con validar_identificador_sql() antes de usar.
Ver cargador_full.py para más detalles sobre esta práctica.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError, OperationalError

from src.error_ids import ErrorIds
from src.logging_utils import log_error, log_for_debugging
from src.validations import (
    validar_columna_existe,
    validar_identificador_sql,
)


def guardar_checkpoint(valor: str | int, archivo: str) -> None:
    """
    Guarda un checkpoint en archivo.

    Args:
        valor: Valor del checkpoint (ID, timestamp, etc.)
        archivo: Ruta al archivo de checkpoint

    Examples:
        >>> guardar_checkpoint(100, "checkpoint.txt")
        >>> guardar_checkpoint("2024-01-15 10:30:00", "checkpoint.txt")
    """
    Path(archivo).write_text(str(valor))


def leer_checkpoint(archivo: str) -> str | int:
    """
    Lee el último checkpoint desde archivo.

    Args:
        archivo: Ruta al archivo de checkpoint

    Returns:
        Valor del checkpoint, o 0 si el archivo no existe

    Raises:
        ValueError: Si el checkpoint contiene datos inválidos o está vacío

    Examples:
        >>> ultimo_id = leer_checkpoint("checkpoint.txt")
        >>> print(ultimo_id)
        100
    """
    checkpoint_path = Path(archivo)

    if not checkpoint_path.exists():
        return 0

    contenido = checkpoint_path.read_text().strip()

    # Checkpoint vacío es un error
    if not contenido:
        log_error(
            "Checkpoint file is empty",
            {"error_id": ErrorIds.CHECKPOINT_CORRUPTED, "archivo": archivo},
        )
        raise ValueError(f"Archivo de checkpoint '{archivo}' está vacío")

    # Intentar convertir a int
    try:
        return int(contenido)
    except ValueError:
        # Si no es int, debe ser timestamp válido
        log_for_debugging(
            "Checkpoint is not an integer, treating as timestamp string",
            {"archivo": archivo, "contenido": contenido[:50]},
        )
        # Validar que al menos parece un timestamp
        try:
            pd.Timestamp(contenido)  # Validar que es parseable
            return contenido
        except Exception as e:
            log_error(
                "Checkpoint file contains invalid data",
                {
                    "error_id": ErrorIds.CHECKPOINT_CORRUPTED,
                    "archivo": archivo,
                    "contenido": contenido[:100],
                    "error": str(e),
                },
            )
            raise ValueError(
                f"Checkpoint '{archivo}' contiene datos inválidos: {contenido[:50]}"
            ) from e


def incremental_load(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    columna_timestamp: str,
    checkpoint_file: str,
) -> dict:
    """
    Carga incremental: solo registros nuevos desde último checkpoint.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_timestamp: Nombre de la columna temporal para filtrar
        checkpoint_file: Archivo de checkpoint

    Returns:
        Dict con métricas: {"procesados": int, "cargados": int, "omitidos": int}

    Raises:
        ValueError: Si la columna de timestamp no existe

    Examples:
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3],
        ...     "timestamp": pd.date_range("2024-01-15", periods=3, freq="h"),
        ...     "valor": [100, 200, 300]
        ... })
        >>> resultado = incremental_load(df, engine, "tabla", "timestamp", "checkpoint.txt")
        >>> print(resultado["cargados"])
        3
    """
    # Validaciones de seguridad
    validar_identificador_sql(tabla)
    validar_identificador_sql(columna_timestamp)

    # DataFrame vacío es válido en carga incremental (no hay nuevos datos)
    if len(df) > 0:
        validar_columna_existe(df, columna_timestamp)

    # Leer último checkpoint
    checkpoint = leer_checkpoint(checkpoint_file)

    # Crear timestamp default
    default_timestamp = pd.Timestamp("2000-01-01")

    # Si la columna es timezone-aware, localizar el default a la misma timezone
    if pd.api.types.is_datetime64_any_dtype(df[columna_timestamp]):
        if (
            hasattr(df[columna_timestamp].dtype, "tz")
            and df[columna_timestamp].dtype.tz is not None
        ):
            # Columna es timezone-aware, localizar el default
            default_timestamp = default_timestamp.tz_localize(
                df[columna_timestamp].dtype.tz
            )

    # Convertir checkpoint a timestamp
    if isinstance(checkpoint, str) and checkpoint != "0":
        try:
            last_timestamp = pd.Timestamp(checkpoint)
            # Si default es tz-aware, localizar last_timestamp también
            if hasattr(default_timestamp, "tz") and default_timestamp.tz is not None:
                if last_timestamp.tz is None:
                    last_timestamp = last_timestamp.tz_localize(default_timestamp.tz)
        except (ValueError, TypeError) as e:
            # Errores esperados de parsing de timestamp
            log_error(
                "Cannot parse checkpoint timestamp - resetting to default",
                {
                    "error_id": ErrorIds.CHECKPOINT_INVALID_TIMESTAMP,
                    "checkpoint_value": checkpoint,
                    "checkpoint_file": checkpoint_file,
                    "error": str(e),
                    "falling_back_to": str(default_timestamp),
                },
            )
            log_for_debugging(
                f"⚠️ ADVERTENCIA: Checkpoint inválido, se procesarán TODOS los datos desde {default_timestamp}",
                {"checkpoint_file": checkpoint_file},
            )
            last_timestamp = default_timestamp
        except Exception as e:
            # Errores inesperados - logear y re-raise
            log_error(
                "Unexpected error parsing checkpoint timestamp",
                {
                    "error_id": ErrorIds.UNEXPECTED_ERROR,
                    "checkpoint": checkpoint,
                    "checkpoint_file": checkpoint_file,
                    "error": str(e),
                },
            )
            raise
    elif checkpoint == 0:
        last_timestamp = default_timestamp
    else:
        last_timestamp = checkpoint

    # Filtrar solo registros nuevos
    # Si DataFrame está vacío, no hay nada que filtrar
    if len(df) == 0:
        df_nuevos = df.copy()
    elif pd.api.types.is_datetime64_any_dtype(df[columna_timestamp]):
        df_nuevos = df[df[columna_timestamp] > last_timestamp].copy()
    else:
        # Para columnas no-datetime (strings, ints), convertir last_timestamp al tipo de la columna
        if isinstance(last_timestamp, pd.Timestamp):
            # Convertir timestamp a string para comparar con columnas tipo string
            last_timestamp_str = str(last_timestamp)
            df_nuevos = df[df[columna_timestamp] > last_timestamp_str].copy()
        else:
            df_nuevos = df[df[columna_timestamp] > last_timestamp].copy()

    procesados = len(df)
    cargados = len(df_nuevos)
    omitidos = procesados - cargados

    if cargados > 0:
        # Cargar solo registros nuevos
        with engine.begin() as conn:
            df_nuevos.to_sql(
                tabla, conn, if_exists="append", index=False, method="multi"
            )

        # Actualizar checkpoint con el valor máximo
        nuevo_checkpoint = df_nuevos[columna_timestamp].max()
        guardar_checkpoint(str(nuevo_checkpoint), checkpoint_file)

    return {"procesados": procesados, "cargados": cargados, "omitidos": omitidos}


def incremental_load_con_validacion(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    columna_timestamp: str,
    checkpoint_file: str,
    columnas_requeridas: list[str] | None = None,
    columnas_no_nulas: list[str] | None = None,
) -> dict:
    """
    Carga incremental con validación previa.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_timestamp: Columna temporal para filtrar
        checkpoint_file: Archivo de checkpoint
        columnas_requeridas: Columnas que deben existir
        columnas_no_nulas: Columnas que no deben tener nulos

    Returns:
        Dict con resultado: {"valido": bool, "cargados": int, "invalidos": int, "mensaje": str}

    Examples:
        >>> resultado = incremental_load_con_validacion(
        ...     df,
        ...     engine,
        ...     "tabla",
        ...     "timestamp",
        ...     "checkpoint.txt",
        ...     columnas_requeridas=["id", "timestamp"]
        ... )
        >>> print(resultado["valido"])
        True
    """
    resultado = {"valido": True, "cargados": 0, "invalidos": 0, "mensaje": "OK"}

    # Validar columnas requeridas
    if columnas_requeridas:
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if columnas_faltantes:
            resultado["valido"] = False
            resultado["mensaje"] = f"Faltan columnas: {columnas_faltantes}"
            return resultado

    # Filtrar registros inválidos (con nulos en columnas críticas)
    df_valido = df.copy()

    if columnas_no_nulas:
        mask_valido = pd.Series([True] * len(df))
        for col in columnas_no_nulas:
            if col in df.columns:
                mask_valido &= df[col].notna()

        df_valido = df[mask_valido].copy()
        resultado["invalidos"] = len(df) - len(df_valido)

    # Cargar registros válidos
    try:
        metricas = incremental_load(
            df_valido, engine, tabla, columna_timestamp, checkpoint_file
        )
        resultado["cargados"] = metricas["cargados"]
    except (OperationalError, IntegrityError) as e:
        # Errores esperados de base de datos
        log_error(
            "Incremental load failed - database error",
            {
                "error_id": ErrorIds.DATABASE_OPERATION_FAILED,
                "tabla": tabla,
                "num_rows": len(df_valido),
                "error": str(e),
            },
        )
        resultado["valido"] = False
        resultado["mensaje"] = f"Error de base de datos: {str(e)}"
    except Exception as e:
        # Errores inesperados - logear y re-raise
        log_error(
            "Incremental load failed - unexpected error",
            {
                "error_id": ErrorIds.UNEXPECTED_ERROR,
                "tabla": tabla,
                "error": str(e),
            },
        )
        raise

    return resultado
