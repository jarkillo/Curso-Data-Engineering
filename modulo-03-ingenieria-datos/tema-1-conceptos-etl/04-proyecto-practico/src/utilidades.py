"""
Módulo de utilidades para logging, métricas y helpers.

Este módulo contiene funciones auxiliares que son utilizadas
por todo el pipeline ETL.
"""

import logging
import time
from datetime import datetime


def configurar_logging(nivel: str = "INFO") -> None:
    """
    Configura el sistema de logging para todo el pipeline.

    Args:
        nivel: Nivel de logging ("DEBUG", "INFO", "WARNING", "ERROR")

    Examples:
        >>> configurar_logging("INFO")
        >>> logging.info("Mensaje de log")
    """
    nivel_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }

    nivel_logging = nivel_mapping.get(nivel, logging.INFO)

    logging.basicConfig(
        level=nivel_logging,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("pipeline.log"),
            logging.StreamHandler(),
        ],
        force=True,  # Reconfigurar si ya está configurado
    )


def calcular_metricas_pipeline(
    tiempo_inicio: float, num_filas: int
) -> dict[str, float]:
    """
    Calcula métricas de ejecución del pipeline.

    Args:
        tiempo_inicio: Timestamp de inicio (time.time())
        num_filas: Número de filas procesadas

    Returns:
        Diccionario con métricas:
        - tiempo_segundos: Tiempo transcurrido
        - filas_por_segundo: Throughput del pipeline

    Examples:
        >>> inicio = time.time()
        >>> # ... procesar datos ...
        >>> metricas = calcular_metricas_pipeline(inicio, 1000)
        >>> metricas["tiempo_segundos"] > 0
        True
    """
    tiempo_fin = time.time()
    tiempo_segundos = round(tiempo_fin - tiempo_inicio, 2)

    if tiempo_segundos > 0:
        filas_por_segundo = round(num_filas / tiempo_segundos, 2)
    else:
        filas_por_segundo = 0

    return {
        "tiempo_segundos": tiempo_segundos,
        "filas_por_segundo": filas_por_segundo,
    }


def formatear_fecha(fecha_str: str) -> str:
    """
    Valida y formatea una fecha en formato YYYY-MM-DD.

    Args:
        fecha_str: String con fecha a validar

    Returns:
        Fecha validada en formato YYYY-MM-DD

    Raises:
        ValueError: Si el formato es inválido o la fecha no existe
        TypeError: Si fecha_str es None

    Examples:
        >>> formatear_fecha("2025-10-23")
        '2025-10-23'
        >>> formatear_fecha("23/10/2025")  # ValueError
    """
    if fecha_str is None:
        raise TypeError("fecha_str no puede ser None")

    if not fecha_str:
        raise ValueError("fecha_str no puede estar vacío")

    try:
        # Intentar parsear la fecha
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")

        # Verificar que la fecha es válida (por ejemplo, 2025-02-30 no existe)
        if fecha_obj.strftime("%Y-%m-%d") != fecha_str:
            raise ValueError(f"Fecha inválida: {fecha_str}")

        return fecha_str

    except ValueError as e:
        if "time data" in str(e) or "does not match" in str(e):
            raise ValueError(
                f"Formato de fecha inválido: {fecha_str}. " f"Use formato YYYY-MM-DD"
            )
        elif "day is out of range" in str(e):
            raise ValueError(f"Fecha inválida: {fecha_str}")
        else:
            raise
