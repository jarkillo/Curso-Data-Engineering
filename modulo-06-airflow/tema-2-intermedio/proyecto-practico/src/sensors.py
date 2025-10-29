"""
Módulo de sensors para verificación de archivos.

Este módulo proporciona utilidades para verificar la existencia de archivos,
útiles para testing de FileSensor.
"""

from pathlib import Path


def verificar_archivo_existe(ruta: str) -> bool:
    """
    Verifica si un archivo existe en el sistema de archivos.

    Args:
        ruta: Ruta al archivo (str o Path)

    Returns:
        True si el archivo existe, False en caso contrario

    Examples:
        >>> verificar_archivo_existe("/tmp/datos.csv")
        True
        >>> verificar_archivo_existe("/ruta/inexistente.csv")
        False
    """
    try:
        return Path(ruta).exists()
    except Exception:
        return False
