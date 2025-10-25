"""
Funciones de validación para requests HTTP.

Valida URLs, timeouts, status codes y contenido JSON de forma robusta.
"""

import json
from typing import Tuple

import requests


def validar_url(url: str) -> None:
    """
    Valida que una URL sea HTTPS y tenga formato correcto.

    Args:
        url: URL a validar

    Raises:
        TypeError: Si url no es string
        ValueError: Si url está vacía, no es HTTPS o tiene formato inválido

    Example:
        >>> validar_url("https://api.ejemplo.com/users")
        >>> validar_url("http://api.ejemplo.com")  # doctest: +SKIP
        ValueError: La URL debe usar HTTPS para mayor seguridad
    """
    if not isinstance(url, str):
        raise TypeError("La URL debe ser string")

    if not url:
        raise ValueError("La URL no puede estar vacía")

    if not url.startswith("https://"):
        if url.startswith("http://"):
            raise ValueError("La URL debe usar HTTPS para mayor seguridad, no HTTP")
        else:
            raise ValueError("La URL debe empezar con https://")


def validar_timeout(timeout: int) -> None:
    """
    Valida que un timeout sea un entero positivo.

    Args:
        timeout: Timeout en segundos

    Raises:
        TypeError: Si timeout no es entero
        ValueError: Si timeout no es positivo

    Example:
        >>> validar_timeout(30)
        >>> validar_timeout(-5)  # doctest: +SKIP
        ValueError: El timeout debe ser positivo
    """
    if not isinstance(timeout, int):
        raise TypeError("El timeout debe ser entero")

    if timeout <= 0:
        raise ValueError("El timeout debe ser positivo")


def validar_status_code(
    response: requests.Response, codigos_validos: Tuple[int, ...] = (200,)
) -> None:
    """
    Valida que el status code de una respuesta esté en los códigos válidos.

    Args:
        response: Response de requests
        codigos_validos: Tupla de status codes aceptables

    Raises:
        ValueError: Si el status code no está en codigos_validos

    Example:
        >>> import requests
        >>> r = requests.Response()
        >>> r.status_code = 200
        >>> validar_status_code(r)
        >>> r.status_code = 404
        >>> validar_status_code(r)  # doctest: +SKIP
        ValueError: Status code 404 no es válido
    """
    if response.status_code not in codigos_validos:
        raise ValueError(
            f"Status code {response.status_code} no es válido. "
            f"Códigos esperados: {codigos_validos}"
        )


def validar_contenido_json(response: requests.Response) -> None:
    """
    Valida que una respuesta contenga JSON válido.

    Args:
        response: Response de requests

    Raises:
        ValueError: Si el Content-Type no es JSON o el contenido es inválido

    Example:
        >>> import requests
        >>> r = requests.Response()
        >>> r.headers["Content-Type"] = "application/json"
        >>> r._content = b'{"test": "data"}'
        >>> validar_contenido_json(r)
    """
    content_type = response.headers.get("Content-Type", "")

    if "application/json" not in content_type:
        raise ValueError(
            f"El Content-Type '{content_type}' no es JSON. "
            f"Se esperaba 'application/json'"
        )

    try:
        response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"El contenido no es JSON válido: {e}")


def extraer_json_seguro(response: requests.Response) -> dict | list:
    """
    Extrae JSON de una respuesta de forma segura.

    Args:
        response: Response de requests

    Returns:
        Datos JSON parseados (dict o list)

    Raises:
        ValueError: Si el contenido está vacío o no es JSON válido

    Example:
        >>> import requests
        >>> r = requests.Response()
        >>> r.headers["Content-Type"] = "application/json"
        >>> r._content = b'{"id": 1, "name": "Test"}'
        >>> data = extraer_json_seguro(r)
        >>> data["id"]
        1
    """
    if not response.content:
        raise ValueError("El contenido de la respuesta está vacío")

    try:
        return response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"El contenido no es JSON válido: {e}")
