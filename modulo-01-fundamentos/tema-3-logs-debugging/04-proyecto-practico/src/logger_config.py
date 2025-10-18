"""
Módulo de configuración de logging profesional.

Este módulo proporciona funciones para configurar loggers de forma
consistente y profesional, tanto para consola como para archivos.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


# Niveles de log válidos
NIVELES_VALIDOS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def configurar_logger(
    nombre: str, nivel: str = "INFO", formato: Optional[str] = None
) -> logging.Logger:
    """
    Configura un logger para salida en consola.

    Esta función crea y configura un logger con un handler de consola,
    formato profesional y el nivel de log especificado.

    Args:
        nombre: Nombre del logger (debe ser único y descriptivo)
        nivel: Nivel de log ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        formato: Formato personalizado (opcional). Si no se proporciona,
                usa formato estándar con timestamp, nivel y mensaje

    Returns:
        Logger configurado y listo para usar

    Raises:
        ValueError: Si el nombre está vacío o el nivel es inválido
        TypeError: Si el nombre no es string

    Examples:
        >>> logger = configurar_logger("mi_pipeline", "INFO")
        >>> logger.info("Pipeline iniciado")
        2025-10-18 12:00:00 - INFO - Pipeline iniciado

        >>> logger_debug = configurar_logger("debug_app", "DEBUG")
        >>> logger_debug.debug("Valor de variable: 42")
        2025-10-18 12:00:01 - DEBUG - Valor de variable: 42
    """
    # Validación de inputs
    if not isinstance(nombre, str):
        raise TypeError("El nombre del logger debe ser un string")

    if not nombre or nombre.strip() == "":
        raise ValueError("El nombre del logger no puede estar vacío")

    nivel_upper = nivel.upper()
    if nivel_upper not in NIVELES_VALIDOS:
        raise ValueError(
            f"Nivel de log inválido: '{nivel}'. "
            f"Niveles válidos: {', '.join(NIVELES_VALIDOS.keys())}"
        )

    # Obtener o crear el logger
    logger = logging.getLogger(nombre)

    # Limpiar handlers existentes para evitar duplicados
    logger.handlers.clear()

    # Configurar nivel
    logger.setLevel(NIVELES_VALIDOS[nivel_upper])

    # Crear handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(NIVELES_VALIDOS[nivel_upper])

    # Configurar formato
    if formato is None:
        formato = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    formatter = logging.Formatter(formato, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)

    # Añadir handler al logger
    logger.addHandler(console_handler)

    # Evitar propagación a loggers padres (evita duplicados)
    logger.propagate = False

    return logger


def configurar_logger_archivo(
    nombre: str,
    ruta_archivo: str,
    nivel: str = "INFO",
    formato: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB por defecto
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configura un logger para escribir en archivo con rotación automática.

    Esta función crea un logger que escribe en archivo con rotación
    automática cuando el archivo alcanza un tamaño máximo. Mantiene
    copias de backup de archivos antiguos.

    Args:
        nombre: Nombre del logger (debe ser único y descriptivo)
        ruta_archivo: Ruta completa del archivo de log
        nivel: Nivel de log ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        formato: Formato personalizado (opcional)
        max_bytes: Tamaño máximo del archivo antes de rotar (en bytes)
        backup_count: Número de archivos de backup a mantener

    Returns:
        Logger configurado para escribir en archivo

    Raises:
        ValueError: Si el nombre está vacío, nivel inválido o ruta inválida
        TypeError: Si los tipos de parámetros son incorrectos
        OSError: Si no se puede crear el archivo o directorio

    Examples:
        >>> logger = configurar_logger_archivo(
        ...     "pipeline_etl",
        ...     "logs/pipeline.log",
        ...     "INFO"
        ... )
        >>> logger.info("Proceso iniciado")
        # Escribe en logs/pipeline.log

        >>> # Con rotación personalizada
        >>> logger = configurar_logger_archivo(
        ...     "api_logs",
        ...     "logs/api.log",
        ...     "DEBUG",
        ...     max_bytes=1024*1024,  # 1 MB
        ...     backup_count=10
        ... )
    """
    # Validación de inputs
    if not isinstance(nombre, str):
        raise TypeError("El nombre del logger debe ser un string")

    if not nombre or nombre.strip() == "":
        raise ValueError("El nombre del logger no puede estar vacío")

    nivel_upper = nivel.upper()
    if nivel_upper not in NIVELES_VALIDOS:
        raise ValueError(
            f"Nivel de log inválido: '{nivel}'. "
            f"Niveles válidos: {', '.join(NIVELES_VALIDOS.keys())}"
        )

    # Validar y crear directorio si no existe
    ruta = Path(ruta_archivo)

    # Verificar que la ruta no sea un directorio existente
    if ruta.exists() and ruta.is_dir():
        raise ValueError(f"La ruta especificada es un directorio: {ruta_archivo}")

    # Crear directorio padre si no existe
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"No se pudo crear el directorio para logs: {e}")

    # Obtener o crear el logger
    logger = logging.getLogger(nombre)

    # Limpiar handlers existentes
    logger.handlers.clear()

    # Configurar nivel
    logger.setLevel(NIVELES_VALIDOS[nivel_upper])

    # Crear handler de archivo con rotación
    try:
        file_handler = RotatingFileHandler(
            filename=str(ruta),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
    except OSError as e:
        raise OSError(f"No se pudo crear el archivo de log: {e}")

    file_handler.setLevel(NIVELES_VALIDOS[nivel_upper])

    # Configurar formato
    if formato is None:
        formato = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    formatter = logging.Formatter(formato, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Añadir handler al logger
    logger.addHandler(file_handler)

    # Evitar propagación a loggers padres
    logger.propagate = False

    return logger
