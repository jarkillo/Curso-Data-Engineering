"""
Módulo de validación de datos para logs de API.

Contiene funciones para validar el formato y contenido de logs de API
antes de procesarlos en el pipeline ETL.
"""

import re
from datetime import datetime
from ipaddress import AddressValueError, ip_address
from typing import Any


def validar_log_api(log: dict[str, Any]) -> tuple[bool, str]:
    """
    Valida que un log de API tenga el formato correcto.

    Verifica que el log contenga todos los campos requeridos y que
    cada campo tenga el tipo de dato correcto.

    Campos requeridos:
    - timestamp: str (formato ISO 8601)
    - endpoint: str (ej: '/api/users')
    - method: str (GET, POST, PUT, DELETE)
    - status_code: int (100-599)
    - response_time_ms: int o float (>= 0)
    - user_id: str
    - ip_address: str

    Args:
        log: Diccionario con los campos del log

    Returns:
        Tupla (es_valido, mensaje_error):
        - es_valido: True si el log es válido
        - mensaje_error: Mensaje descriptivo del error (vacío si es válido)

    Examples:
        >>> log = {
        ...     'timestamp': '2025-01-15T10:30:45Z',
        ...     'endpoint': '/api/users',
        ...     'method': 'GET',
        ...     'status_code': 200,
        ...     'response_time_ms': 145,
        ...     'user_id': 'user_12345',
        ...     'ip_address': '192.168.1.100'
        ... }
        >>> valido, error = validar_log_api(log)
        >>> valido
        True
        >>> error
        ''
    """
    campos_requeridos = [
        "timestamp",
        "endpoint",
        "method",
        "status_code",
        "response_time_ms",
        "user_id",
        "ip_address",
    ]

    # Verificar campos faltantes
    for campo in campos_requeridos:
        if campo not in log:
            return False, f"Campo requerido faltante: {campo}"

    # Validar timestamp
    valido, error = validar_timestamp(log["timestamp"])
    if not valido:
        return False, f"Timestamp inválido: {error}"

    # Validar endpoint
    valido, error = validar_endpoint(log["endpoint"])
    if not valido:
        return False, f"Endpoint inválido: {error}"

    # Validar método HTTP
    valido, error = validar_metodo_http(log["method"])
    if not valido:
        return False, f"Método HTTP inválido: {error}"

    # Validar status code
    valido, error = validar_status_code(log["status_code"])
    if not valido:
        return False, f"Status code inválido: {error}"

    # Validar response time
    valido, error = validar_response_time(log["response_time_ms"])
    if not valido:
        return False, f"Response time inválido: {error}"

    # Validar IP address
    valido, error = validar_ip_address(log["ip_address"])
    if not valido:
        return False, f"IP address inválida: {error}"

    return True, ""


def validar_timestamp(timestamp: str) -> tuple[bool, str]:
    """
    Valida que un timestamp esté en formato ISO 8601.

    Args:
        timestamp: String con el timestamp a validar

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_timestamp('2025-01-15T10:30:45Z')
        >>> valido
        True
        >>> valido, error = validar_timestamp('2025-13-45')
        >>> valido
        False
    """
    if not timestamp or not isinstance(timestamp, str):
        return False, "Timestamp vacío o no es string"

    # Intentar parsear con diferentes formatos ISO 8601
    formatos = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]

    for formato in formatos:
        try:
            datetime.strptime(timestamp, formato)
            return True, ""
        except ValueError:
            continue

    return False, f"Timestamp no está en formato ISO 8601: {timestamp}"


def validar_endpoint(endpoint: str) -> tuple[bool, str]:
    """
    Valida que un endpoint tenga formato correcto.

    El endpoint debe:
    - Empezar con '/'
    - Contener solo caracteres alfanuméricos, guiones, barras y guiones bajos
    - No exceder 200 caracteres

    Args:
        endpoint: String con el endpoint a validar

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_endpoint('/api/users')
        >>> valido
        True
        >>> valido, _ = validar_endpoint('api/users')  # Sin barra inicial
        >>> valido
        False
    """
    if not endpoint or not isinstance(endpoint, str):
        return False, "Endpoint vacío o no es string"

    if not endpoint.startswith("/"):
        return False, "Endpoint debe empezar con '/'"

    if len(endpoint) > 200:
        return False, f"Endpoint muy largo ({len(endpoint)} caracteres, máximo 200)"

    # Validar caracteres permitidos: alfanuméricos, /, -, _
    patron = r"^[a-zA-Z0-9/_-]+$"
    if not re.match(patron, endpoint):
        return False, "Endpoint contiene caracteres no permitidos"

    return True, ""


def validar_metodo_http(metodo: str) -> tuple[bool, str]:
    """
    Valida que el método HTTP sea válido.

    Args:
        metodo: String con el método HTTP (GET, POST, PUT, DELETE, PATCH, etc.)

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_metodo_http('GET')
        >>> valido
        True
        >>> valido, _ = validar_metodo_http('INVALID')
        >>> valido
        False
    """
    if not metodo or not isinstance(metodo, str):
        return False, "Método HTTP vacío o no es string"

    metodos_validos = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "HEAD",
        "OPTIONS",
        "CONNECT",
        "TRACE",
    ]

    # Validar que el método esté en mayúsculas (no aceptar minúsculas)
    if metodo not in metodos_validos:
        return False, f"Método HTTP no válido: {metodo}"

    return True, ""


def validar_status_code(status_code: int) -> tuple[bool, str]:
    """
    Valida que el status code HTTP sea válido.

    Args:
        status_code: Código de estado HTTP (100-599)

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_status_code(200)
        >>> valido
        True
        >>> valido, _ = validar_status_code(999)
        >>> valido
        False
    """
    if not isinstance(status_code, int):
        return False, "Status code debe ser un entero"

    if status_code < 100 or status_code > 599:
        return (
            False,
            f"Status code fuera de rango: {status_code} (debe estar entre 100-599)",
        )

    return True, ""


def validar_response_time(response_time_ms: float) -> tuple[bool, str]:
    """
    Valida que el tiempo de respuesta sea válido.

    Args:
        response_time_ms: Tiempo de respuesta en milisegundos

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_response_time(145.5)
        >>> valido
        True
        >>> valido, _ = validar_response_time(-10)
        >>> valido
        False
    """
    if not isinstance(response_time_ms, (int, float)):
        return False, "Response time debe ser un número"

    if response_time_ms < 0:
        return False, f"Response time no puede ser negativo: {response_time_ms}"

    return True, ""


def validar_ip_address(ip: str) -> tuple[bool, str]:
    """
    Valida que una dirección IP tenga formato correcto.

    Soporta IPv4 e IPv6.

    Args:
        ip: String con la dirección IP

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> valido, _ = validar_ip_address('192.168.1.100')
        >>> valido
        True
        >>> valido, _ = validar_ip_address('999.999.999.999')
        >>> valido
        False
    """
    if not ip or not isinstance(ip, str):
        return False, "IP address vacía o no es string"

    try:
        # Usar el módulo ipaddress de Python
        ip_address(ip)
        return True, ""
    except (AddressValueError, ValueError):
        return False, f"IP address inválida: {ip}"


def validar_lote_logs(logs: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Valida un lote de logs y retorna estadísticas de validación.

    Args:
        logs: Lista de diccionarios con logs

    Returns:
        Diccionario con estadísticas:
        - total: Número total de logs
        - validos: Número de logs válidos
        - invalidos: Número de logs inválidos
        - tasa_validez: Porcentaje de logs válidos (0-100)
        - errores: Lista de mensajes de error únicos

    Examples:
        >>> logs = [
        ...     {'timestamp': '2025-01-15T10:30:45Z', 'endpoint': '/api/users',
        ...      'method': 'GET', 'status_code': 200, 'response_time_ms': 145,
        ...      'user_id': 'user_1', 'ip_address': '192.168.1.1'},
        ...     {'timestamp': 'invalid', 'endpoint': '/api/posts'}
        ... ]
        >>> stats = validar_lote_logs(logs)
        >>> stats['total']
        2
        >>> stats['validos']
        1
    """
    total = len(logs)
    validos = 0
    invalidos = 0
    errores_unicos: set[str] = set()

    for log in logs:
        es_valido, mensaje_error = validar_log_api(log)
        if es_valido:
            validos += 1
        else:
            invalidos += 1
            errores_unicos.add(mensaje_error)

    tasa_validez = (validos / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "validos": validos,
        "invalidos": invalidos,
        "tasa_validez": round(tasa_validez, 2),
        "errores": list(errores_unicos),
    }
