"""
Orquestador del pipeline completo.

Integra todos los módulos para ejecutar el pipeline end-to-end.
"""

import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import Engine

from src.cargador import cargar_a_base_datos, cargar_a_parquet
from src.extractor import (
    extraer_noticias_api_simulada,
    guardar_en_bronze,
)
from src.transformador_bronze import transformar_bronze_a_silver
from src.transformador_silver import transformar_silver_a_gold
from src.validador import generar_reporte_calidad

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def ejecutar_pipeline_completo(
    num_noticias: int,
    engine: Engine,
    directorio_salida: Path,
    guardar_intermedios: bool = True,
) -> dict:
    """
    Ejecuta pipeline completo: extracción → transformación → carga.

    Args:
        num_noticias: Número de noticias a simular
        engine: SQLAlchemy engine para BD
        directorio_salida: Directorio base para guardar datos
        guardar_intermedios: Si guardar datos intermedios (Bronze, Silver)

    Returns:
        Dict con métricas del pipeline

    Examples:
        >>> from sqlalchemy import create_engine
        >>> from pathlib import Path
        >>> engine = create_engine("sqlite:///:memory:")
        >>> resultado = ejecutar_pipeline_completo(10, engine, Path("data"))
        >>> resultado["exito"]  # doctest: +SKIP
        True
    """
    metricas = {
        "inicio": datetime.now().isoformat(),
        "exito": False,
        "registros_extraidos": 0,
        "registros_silver": 0,
        "registros_gold": 0,
    }

    try:
        logger.info("=== Iniciando pipeline completo ===")

        # 1. Extracción (Bronze)
        logger.info(f"Extrayendo {num_noticias} noticias...")
        df_bronze = extraer_noticias_api_simulada(num_noticias)
        metricas["registros_extraidos"] = len(df_bronze)

        if guardar_intermedios:
            ruta_bronze = directorio_salida / "bronze" / "noticias.parquet"
            guardar_en_bronze(df_bronze, ruta_bronze)
            logger.info(f"Bronze guardado en {ruta_bronze}")

        # 2. Transformación Bronze → Silver
        logger.info("Transformando Bronze → Silver...")
        df_silver = transformar_bronze_a_silver(df_bronze)
        metricas["registros_silver"] = len(df_silver)

        if guardar_intermedios:
            ruta_silver = directorio_salida / "silver" / "noticias.parquet"
            cargar_a_parquet(df_silver, ruta_silver)
            logger.info(f"Silver guardado en {ruta_silver}")

        # 3. Validación de calidad
        logger.info("Validando calidad de datos...")
        reporte_calidad = generar_reporte_calidad(df_silver)
        metricas["calidad"] = reporte_calidad
        logger.info(f"Esquema válido: {reporte_calidad['esquema_valido']}")

        # 4. Transformación Silver → Gold
        logger.info("Transformando Silver → Gold...")
        datos_gold = transformar_silver_a_gold(df_silver)
        metricas["registros_gold"] = len(datos_gold["por_fuente"])

        # 5. Carga en Gold (Parquet + BD)
        logger.info("Cargando datos Gold...")

        # Cargar agregación por fuente
        ruta_por_fuente = directorio_salida / "gold" / "noticias_por_fuente.parquet"
        cargar_a_parquet(datos_gold["por_fuente"], ruta_por_fuente)
        cargar_a_base_datos(
            datos_gold["por_fuente"], engine, "noticias_por_fuente", if_exists="replace"
        )

        # Cargar agregación por categoría
        ruta_por_categoria = (
            directorio_salida / "gold" / "noticias_por_categoria.parquet"
        )
        cargar_a_parquet(datos_gold["por_categoria"], ruta_por_categoria)
        cargar_a_base_datos(
            datos_gold["por_categoria"],
            engine,
            "noticias_por_categoria",
            if_exists="replace",
        )

        metricas["exito"] = True
        logger.info("=== Pipeline completado exitosamente ===")

    except Exception as e:
        metricas["exito"] = False
        metricas["error"] = str(e)
        logger.error(f"Error en pipeline: {e}", exc_info=True)

    finally:
        metricas["fin"] = datetime.now().isoformat()

    return metricas
