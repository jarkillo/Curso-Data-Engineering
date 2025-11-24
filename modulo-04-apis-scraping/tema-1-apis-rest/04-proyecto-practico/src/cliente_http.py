"""
Cliente HTTP para consumir APIs REST.

Funciones básicas GET, POST, PUT, DELETE con validación robusta.
"""

from typing import Any

import requests

from src.validaciones import validar_timeout, validar_url


def hacer_get(
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: int = 30,
) -> requests.Response:
    """
    Hace un GET request a una URL.

    Args:
        url: URL del endpoint (debe ser HTTPS)
        headers: Headers HTTP opcionales
        params: Query parameters opcionales
        timeout: Timeout en segundos (default: 30)

    Returns:
        Response de requests

    Raises:
        ValueError: Si url o timeout son inválidos
        requests.exceptions.RequestException: Si hay error en la request

    Example:
        >>> # Requiere internet y API real
        >>> response = hacer_get("https://jsonplaceholder.typicode.com/users/1")
        >>> response.status_code
        200
    """
    validar_url(url)
    validar_timeout(timeout)

    return requests.get(url, headers=headers, params=params, timeout=timeout)


def hacer_post(
    url: str,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> requests.Response:
    """
    Hace un POST request a una URL.

    Args:
        url: URL del endpoint (debe ser HTTPS)
        json: Datos a enviar como JSON
        data: Datos a enviar como form data
        headers: Headers HTTP opcionales
        timeout: Timeout en segundos (default: 30)

    Returns:
        Response de requests

    Raises:
        ValueError: Si url o timeout son inválidos
        requests.exceptions.RequestException: Si hay error en la request

    Note:
        Si se proporciona 'json', 'data' es ignorado.

    Example:
        >>> # Requiere internet y API real
        >>> data = {"title": "Test", "body": "Content", "userId": 1}
        >>> response = hacer_post(
        ...     "https://jsonplaceholder.typicode.com/posts",
        ...     json=data
        ... )
        >>> response.status_code in (200, 201)
        True
    """
    validar_url(url)
    validar_timeout(timeout)

    return requests.post(url, json=json, data=data, headers=headers, timeout=timeout)


def hacer_put(
    url: str,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> requests.Response:
    """
    Hace un PUT request a una URL.

    Args:
        url: URL del endpoint (debe ser HTTPS)
        json: Datos a enviar como JSON
        data: Datos a enviar como form data
        headers: Headers HTTP opcionales
        timeout: Timeout en segundos (default: 30)

    Returns:
        Response de requests

    Raises:
        ValueError: Si url o timeout son inválidos
        requests.exceptions.RequestException: Si hay error en la request

    Note:
        Si se proporciona 'json', 'data' es ignorado.

    Example:
        >>> # Requiere internet y API real
        >>> data = {"title": "Updated", "body": "New content", "userId": 1}
        >>> response = hacer_put(
        ...     "https://jsonplaceholder.typicode.com/posts/1",
        ...     json=data
        ... )
        >>> response.status_code == 200
        True
    """
    validar_url(url)
    validar_timeout(timeout)

    return requests.put(url, json=json, data=data, headers=headers, timeout=timeout)


def hacer_delete(
    url: str, headers: dict[str, str] | None = None, timeout: int = 30
) -> requests.Response:
    """
    Hace un DELETE request a una URL.

    Args:
        url: URL del endpoint (debe ser HTTPS)
        headers: Headers HTTP opcionales
        timeout: Timeout en segundos (default: 30)

    Returns:
        Response de requests

    Raises:
        ValueError: Si url o timeout son inválidos
        requests.exceptions.RequestException: Si hay error en la request

    Example:
        >>> # Requiere internet y API real
        >>> response = hacer_delete(
        ...     "https://jsonplaceholder.typicode.com/posts/1"
        ... )
        >>> response.status_code == 200
        True
    """
    validar_url(url)
    validar_timeout(timeout)

    return requests.delete(url, headers=headers, timeout=timeout)
