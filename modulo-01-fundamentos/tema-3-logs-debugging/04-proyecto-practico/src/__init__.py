"""
Módulo de logging profesional para Data Engineering.

Este módulo proporciona funciones para configurar y usar logging
de forma profesional en pipelines ETL y aplicaciones de datos.
"""

__version__ = "1.0.0"
__author__ = "Master en Ingeniería de Datos con IA"

from .logger_config import configurar_logger, configurar_logger_archivo

# Importar pipeline_logs solo si existe (se añadirá después)
try:
    from .pipeline_logs import (  # noqa: F401
        procesar_con_logs,
        validar_datos_con_logs,
    )

    __all__ = [
        "configurar_logger",
        "configurar_logger_archivo",
        "procesar_con_logs",
        "validar_datos_con_logs",
    ]
except ImportError:
    __all__ = [
        "configurar_logger",
        "configurar_logger_archivo",
    ]
