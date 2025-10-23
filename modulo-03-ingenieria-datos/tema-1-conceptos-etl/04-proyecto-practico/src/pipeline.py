"""
Módulo del pipeline ETL principal.

Este módulo orquesta todo el flujo ETL:
Extract → Validate → Transform → Load
"""

import logging
import time
from pathlib import Path
from typing import Any

from src.carga import cargar_ventas_idempotente, crear_tabla_ventas
from src.extraccion import extraer_clientes, extraer_productos, extraer_ventas
from src.transformacion import transformar_ventas
from src.utilidades import (
    calcular_metricas_pipeline,
    configurar_logging,
    formatear_fecha,
)
from src.validacion import validar_datos

# Configurar logging
configurar_logging("INFO")
logger = logging.getLogger(__name__)


def pipeline_etl(
    fecha: str,
    directorio_datos: str = "datos",
    db_path: str = "ventas.db",
) -> dict[str, Any]:
    """
    Pipeline ETL completo para procesar ventas de una fecha específica.

    Flujo:
    1. Extract: Lee ventas, productos y clientes desde CSV
    2. Validate: Valida calidad de datos
    3. Transform: Enriquece ventas con info de productos y clientes
    4. Load: Carga en SQLite (idempotente)

    Args:
        fecha: Fecha a procesar (formato: YYYY-MM-DD)
        directorio_datos: Directorio con los archivos CSV
        db_path: Ruta a la base de datos SQLite

    Returns:
        Diccionario con métricas de ejecución:
        - fecha: Fecha procesada
        - filas_extraidas: Número de ventas extraídas
        - filas_validas: Número de ventas válidas
        - filas_cargadas: Número de ventas cargadas
        - tiempo_segundos: Tiempo de ejecución
        - estado: "EXITOSO", "ERROR", "SIN_DATOS"
        - errores: Lista de errores (si aplica)

    Examples:
        >>> metricas = pipeline_etl("2025-10-01")
        >>> metricas["estado"]
        'EXITOSO'
    """
    logger.info(f"🚀 Iniciando pipeline ETL para fecha: {fecha}")

    metricas = {
        "fecha": fecha,
        "filas_extraidas": 0,
        "filas_validas": 0,
        "filas_cargadas": 0,
        "tiempo_segundos": 0,
        "estado": "INICIADO",
        "errores": [],
    }

    inicio = time.time()

    try:
        # Validar formato de fecha
        fecha = formatear_fecha(fecha)

        # Construir rutas a archivos
        directorio = Path(directorio_datos)
        ruta_ventas = directorio / "ventas.csv"
        ruta_productos = directorio / "productos.csv"
        ruta_clientes = directorio / "clientes.csv"

        # PASO 1: EXTRACT
        logger.info("📂 Extrayendo datos...")
        ventas = extraer_ventas(str(ruta_ventas))
        productos = extraer_productos(str(ruta_productos))
        clientes = extraer_clientes(str(ruta_clientes))

        logger.info(
            f"✅ Extraídos: {len(ventas)} ventas, "
            f"{len(productos)} productos, {len(clientes)} clientes"
        )

        # Filtrar ventas de la fecha especificada
        ventas_fecha = [v for v in ventas if v["fecha"] == fecha]
        metricas["filas_extraidas"] = len(ventas_fecha)

        if len(ventas_fecha) == 0:
            logger.warning(f"⚠️ No hay ventas para la fecha {fecha}")
            metricas["estado"] = "SIN_DATOS"
            return metricas

        logger.info(f"📊 Encontradas {len(ventas_fecha)} ventas para {fecha}")

        # PASO 2: VALIDATE
        logger.info("✅ Validando datos...")
        es_valido, errores_validacion = validar_datos(ventas_fecha)

        if not es_valido:
            logger.error(f"❌ Validación falló: {errores_validacion}")
            metricas["estado"] = "ERROR"
            metricas["errores"] = errores_validacion
            return metricas

        metricas["filas_validas"] = len(ventas_fecha)
        logger.info(f"✅ Validación exitosa: {len(ventas_fecha)} ventas válidas")

        # PASO 3: TRANSFORM
        logger.info("🔄 Transformando datos...")
        ventas_transformadas = transformar_ventas(ventas_fecha, productos, clientes)
        logger.info(f"✅ Transformadas {len(ventas_transformadas)} ventas")

        # PASO 4: LOAD
        logger.info(f"💾 Cargando datos en {db_path}...")

        # Crear tabla si no existe
        crear_tabla_ventas(db_path)

        # Cargar datos (idempotente)
        num_cargadas = cargar_ventas_idempotente(ventas_transformadas, fecha, db_path)

        metricas["filas_cargadas"] = num_cargadas
        logger.info(f"✅ Cargadas {num_cargadas} ventas")

        # Métricas finales
        metricas_tiempo = calcular_metricas_pipeline(inicio, num_cargadas)
        metricas["tiempo_segundos"] = metricas_tiempo["tiempo_segundos"]
        metricas["estado"] = "EXITOSO"

        logger.info(
            f"✅ Pipeline completado en {metricas['tiempo_segundos']}s "
            f"({metricas_tiempo['filas_por_segundo']} filas/s)"
        )

        return metricas

    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {e}")
        metricas["estado"] = "ERROR"
        metricas["errores"] = [f"Archivo no encontrado: {e}"]
        raise

    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}", exc_info=True)
        metricas["estado"] = "ERROR"
        metricas["errores"] = [str(e)]
        raise

    finally:
        metricas["tiempo_segundos"] = round(time.time() - inicio, 2)
        logger.info(f"📊 Métricas finales: {metricas}")


def pipeline_etl_con_reintentos(
    fecha: str,
    directorio_datos: str = "datos",
    db_path: str = "ventas.db",
    max_intentos: int = 3,
) -> dict[str, Any]:
    """
    Pipeline ETL con reintentos automáticos en caso de fallo.

    Args:
        fecha: Fecha a procesar (formato: YYYY-MM-DD)
        directorio_datos: Directorio con los archivos CSV
        db_path: Ruta a la base de datos SQLite
        max_intentos: Número máximo de intentos

    Returns:
        Diccionario con métricas de ejecución

    Raises:
        Exception: Si todos los intentos fallan

    Examples:
        >>> metricas = pipeline_etl_con_reintentos("2025-10-01", max_intentos=3)
        >>> metricas["estado"]
        'EXITOSO'
    """
    for intento in range(1, max_intentos + 1):
        try:
            logger.info(f"🔄 Intento {intento}/{max_intentos}")

            metricas = pipeline_etl(fecha, directorio_datos, db_path)

            logger.info(f"✅ Éxito en intento {intento}")
            return metricas

        except Exception as e:
            logger.warning(f"⚠️ Intento {intento} falló: {e}")

            if intento == max_intentos:
                logger.error("❌ Todos los intentos fallaron")
                raise

            # Exponential backoff
            espera = 2**intento
            logger.info(f"⏳ Esperando {espera}s antes de reintentar...")
            time.sleep(espera)

    # Si llegamos aquí, todos los intentos fallaron (no debería pasar por el raise anterior)
    raise RuntimeError(f"Pipeline falló después de {max_intentos} intentos")
