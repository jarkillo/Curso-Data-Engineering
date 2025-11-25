"""
Módulo para procesar entradas de logs.

Funciones para parsear, validar y normalizar logs antes de insertarlos en MongoDB.
"""

from datetime import datetime
from typing import Any


def parsear_log_entry(log_string: str) -> dict[str, str]:
    """
    Parsea un string de log en un documento estructurado.

    Args:
        log_string: String con formato "YYYY-MM-DD HH:MM:SS | NIVEL | SERVICIO | MENSAJE"

    Returns:
        Diccionario con campos timestamp, nivel, servicio, mensaje

    Raises:
        ValueError: Si el log está vacío o tiene formato inválido

    Examples:
        >>> parsear_log_entry("2024-11-12 14:30:45 | ERROR | UserService | Connection failed")
        {'timestamp': '2024-11-12 14:30:45', 'nivel': 'ERROR', 'servicio': 'UserService', 'mensaje': 'Connection failed'}
    """
    if not log_string or not log_string.strip():
        raise ValueError("Log string no puede estar vacío")

    # Separar por pipe |
    partes = log_string.split(" | ")

    if len(partes) != 4:
        raise ValueError(
            "Formato de log inválido. Esperado: 'TIMESTAMP | NIVEL | SERVICIO | MENSAJE'"
        )

    timestamp, nivel, servicio, mensaje = partes

    return {
        "timestamp": timestamp.strip(),
        "nivel": nivel.strip(),
        "servicio": servicio.strip(),
        "mensaje": mensaje.strip(),
    }


def validar_log_entry(log_entry: dict[str, Any]) -> None:
    """
    Valida que un log entry tenga todos los campos obligatorios.

    Args:
        log_entry: Diccionario con campos del log

    Raises:
        ValueError: Si falta algún campo obligatorio

    Examples:
        >>> validar_log_entry({'timestamp': '2024-11-12 14:30:45', 'nivel': 'ERROR', 'servicio': 'UserService', 'mensaje': 'Test'})
        # No lanza error
    """
    campos_obligatorios = ["timestamp", "nivel", "servicio", "mensaje"]

    for campo in campos_obligatorios:
        if campo not in log_entry:
            raise ValueError(f"Campo '{campo}' es obligatorio")


def normalizar_timestamp(timestamp_str: str) -> datetime:
    """
    Convierte un timestamp string a objeto datetime.

    Args:
        timestamp_str: String con formato "YYYY-MM-DD HH:MM:SS" o ISO format

    Returns:
        Objeto datetime

    Raises:
        ValueError: Si el timestamp está vacío o tiene formato inválido

    Examples:
        >>> normalizar_timestamp("2024-11-12 14:30:45")
        datetime.datetime(2024, 11, 12, 14, 30, 45)
    """
    if not timestamp_str or not timestamp_str.strip():
        raise ValueError("Timestamp no puede estar vacío")

    # Intentar formato estándar primero
    formatos = [
        "%Y-%m-%d %H:%M:%S",  # Formato estándar
        "%Y-%m-%dT%H:%M:%S",  # Formato ISO sin timezone
    ]

    for formato in formatos:
        try:
            return datetime.strptime(timestamp_str.strip(), formato)
        except ValueError:
            continue

    # Si ningún formato funcionó
    raise ValueError(
        f"Formato de timestamp inválido: '{timestamp_str}'. "
        f"Esperado: 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DDTHH:MM:SS'"
    )


def extraer_nivel_severidad(log_entry: dict[str, Any]) -> str:
    """
    Extrae el nivel de severidad de un log entry.

    Args:
        log_entry: Diccionario con campos del log

    Returns:
        Nivel de severidad (INFO, WARNING, ERROR)

    Raises:
        KeyError: Si no existe el campo 'nivel'
        ValueError: Si el nivel no es válido

    Examples:
        >>> extraer_nivel_severidad({'nivel': 'ERROR'})
        'ERROR'
    """
    if "nivel" not in log_entry:
        raise KeyError("Campo 'nivel' no encontrado en log entry")

    nivel = log_entry["nivel"]
    niveles_validos = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]

    if nivel not in niveles_validos:
        raise ValueError(
            f"Nivel de severidad inválido: '{nivel}'. "
            f"Valores válidos: {', '.join(niveles_validos)}"
        )

    return nivel
