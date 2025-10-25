"""
Funciones para manejo de autenticación en APIs REST.

Soporta API Key, Bearer Token y Basic Auth.
"""

import base64
from typing import Dict


def crear_headers_api_key(
    api_key: str, header_name: str = "X-API-Key"
) -> Dict[str, str]:
    """
    Crea headers con API Key.

    Args:
        api_key: API key para autenticación
        header_name: Nombre del header (default: "X-API-Key")

    Returns:
        Diccionario de headers con la API key

    Raises:
        TypeError: Si api_key no es string
        ValueError: Si api_key o header_name están vacíos

    Example:
        >>> headers = crear_headers_api_key("mi-api-key-123")
        >>> headers["X-API-Key"]
        'mi-api-key-123'
    """
    if not isinstance(api_key, str):
        raise TypeError("La API key debe ser string")

    if not api_key:
        raise ValueError("La API key no puede estar vacía")

    if not header_name:
        raise ValueError("El nombre del header no puede estar vacío")

    return {header_name: api_key}


def crear_headers_bearer(token: str) -> Dict[str, str]:
    """
    Crea headers con Bearer token.

    Args:
        token: Bearer token (JWT u otro)

    Returns:
        Diccionario de headers con Authorization Bearer

    Raises:
        TypeError: Si token no es string
        ValueError: Si token está vacío

    Example:
        >>> headers = crear_headers_bearer("eyJhbGc...")
        >>> headers["Authorization"]
        'Bearer eyJhbGc...'
    """
    if not isinstance(token, str):
        raise TypeError("El token debe ser string")

    if not token:
        raise ValueError("El token no puede estar vacío")

    return {"Authorization": f"Bearer {token}"}


def crear_headers_basic_auth(username: str, password: str) -> Dict[str, str]:
    """
    Crea headers con Basic Authentication.

    Args:
        username: Nombre de usuario
        password: Contraseña

    Returns:
        Diccionario de headers con Authorization Basic

    Raises:
        TypeError: Si username o password no son strings
        ValueError: Si username o password están vacíos

    Example:
        >>> headers = crear_headers_basic_auth("admin", "pass123")
        >>> "Authorization" in headers
        True
        >>> headers["Authorization"].startswith("Basic ")
        True
    """
    if not isinstance(username, str):
        raise TypeError("El username debe ser string")

    if not isinstance(password, str):
        raise TypeError("El password debe ser string")

    if not username:
        raise ValueError("El username no puede estar vacío")

    if not password:
        raise ValueError("La password no puede estar vacía")

    # Codificar credenciales en base64
    credenciales = f"{username}:{password}"
    credenciales_encoded = base64.b64encode(credenciales.encode()).decode()

    return {"Authorization": f"Basic {credenciales_encoded}"}


def combinar_headers(
    headers_base: Dict[str, str], headers_extra: Dict[str, str]
) -> Dict[str, str]:
    """
    Combina dos diccionarios de headers.

    Si hay claves duplicadas, headers_extra tiene prioridad.
    No modifica los diccionarios originales.

    Args:
        headers_base: Headers base
        headers_extra: Headers adicionales (sobrescriben si hay duplicados)

    Returns:
        Diccionario combinado de headers

    Example:
        >>> base = {"Content-Type": "application/json"}
        >>> extra = {"Authorization": "Bearer token"}
        >>> resultado = combinar_headers(base, extra)
        >>> len(resultado)
        2
        >>> resultado["Content-Type"]
        'application/json'
        >>> resultado["Authorization"]
        'Bearer token'
    """
    # Crear copia para no modificar originales
    resultado = headers_base.copy()
    resultado.update(headers_extra)

    return resultado
