"""
Sistema de reintentos con exponential backoff para APIs REST.

Maneja errores temporales (5xx, 429) con reintentos automáticos.
"""

import time
from typing import Any, Dict, Optional

import requests
from src.cliente_http import hacer_delete, hacer_get, hacer_post, hacer_put
from src.validaciones import validar_url

METODOS_HTTP_VALIDOS = {"GET", "POST", "PUT", "DELETE", "PATCH"}
CODIGOS_REINTENTAR = {429, 500, 502, 503, 504}


def calcular_delay_exponencial(intento: int, base: int = 2, max_delay: int = 60) -> int:
    """
    Calcula delay exponencial para reintentos.

    Formula: base^intento, limitado por max_delay

    Args:
        intento: Número de intento (0, 1, 2, ...)
        base: Base exponencial (default: 2)
        max_delay: Delay máximo en segundos (default: 60)

    Returns:
        Delay en segundos

    Raises:
        ValueError: Si parámetros son inválidos

    Example:
        >>> calcular_delay_exponencial(1)
        2
        >>> calcular_delay_exponencial(2)
        4
        >>> calcular_delay_exponencial(3)
        8
        >>> calcular_delay_exponencial(10, max_delay=30)
        30
    """
    if intento < 0:
        raise ValueError("El intento debe ser no negativo")

    if base <= 1:
        raise ValueError("La base debe ser mayor que 1")

    if max_delay <= 0:
        raise ValueError("El max_delay debe ser positivo")

    if intento == 0:
        return 1

    delay = base**intento

    return min(delay, max_delay)


def reintentar_con_backoff(  # noqa: C901
    url: str,
    metodo: str = "GET",
    max_intentos: int = 3,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> requests.Response:
    """
    Hace request HTTP con reintentos automáticos usando exponential backoff.

    Reintenta automáticamente ante:
    - Errores 5xx (server errors)
    - Error 429 (rate limit)

    NO reintenta ante:
    - Errores 4xx (excepto 429) porque son errores de cliente

    Args:
        url: URL del endpoint
        metodo: Método HTTP (GET, POST, PUT, DELETE)
        max_intentos: Número máximo de intentos
        headers: Headers HTTP opcionales
        params: Query parameters opcionales
        json: Datos JSON para POST/PUT
        data: Form data para POST/PUT
        timeout: Timeout en segundos

    Returns:
        Response exitoso de requests

    Raises:
        ValueError: Si parámetros son inválidos
        requests.exceptions.HTTPError: Si todos los intentos fallan

    Example:
        >>> # Requiere internet y API real
        >>> response = reintentar_con_backoff(
        ...     "https://jsonplaceholder.typicode.com/users/1"
        ... )
        >>> response.status_code
        200
    """
    validar_url(url)

    if max_intentos < 1:
        raise ValueError("max_intentos debe ser al menos 1")

    metodo_upper = metodo.upper()
    if metodo_upper not in METODOS_HTTP_VALIDOS:
        raise ValueError(
            f"'{metodo}' no es un método HTTP válido. "
            f"Válidos: {METODOS_HTTP_VALIDOS}"
        )

    # Mapeo de métodos a funciones
    funciones = {
        "GET": hacer_get,
        "POST": hacer_post,
        "PUT": hacer_put,
        "DELETE": hacer_delete,
    }

    ultima_excepcion = None

    for intento in range(max_intentos):
        try:
            # Preparar kwargs según el método
            kwargs = {"url": url, "headers": headers, "timeout": timeout}

            if metodo_upper == "GET":
                kwargs["params"] = params
            elif metodo_upper in {"POST", "PUT"}:
                kwargs["json"] = json
                kwargs["data"] = data

            # Hacer request
            response = funciones[metodo_upper](**kwargs)

            # Si es 2xx, retornar inmediatamente
            if 200 <= response.status_code < 300:
                return response

            # Si es 4xx (excepto 429), NO reintentar - lanzar inmediatamente
            if 400 <= response.status_code < 500 and response.status_code != 429:
                response.raise_for_status()

            # Si es 5xx o 429, reintentar
            if response.status_code in CODIGOS_REINTENTAR:
                if intento < max_intentos - 1:  # No esperar en el último intento
                    delay = calcular_delay_exponencial(intento + 1)
                    time.sleep(delay)
                    continue
                else:
                    # Último intento falló
                    response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            ultima_excepcion = e

            # Verificar si es un error 4xx (excepto 429) - NO reintentar
            if hasattr(e, "response") and e.response is not None:
                status_code = e.response.status_code
                if 400 <= status_code < 500 and status_code != 429:
                    # Error de cliente - lanzar inmediatamente sin reintentar
                    raise

            # Si no quedan más intentos, lanzar excepción
            if intento >= max_intentos - 1:
                raise requests.exceptions.HTTPError(
                    f"Todos los intentos fallaron ({max_intentos}): {e}"
                ) from e

    # Si llegamos aquí, algo salió mal
    if ultima_excepcion:
        raise requests.exceptions.HTTPError(
            f"Todos los intentos fallaron ({max_intentos})"
        ) from ultima_excepcion

    raise requests.exceptions.HTTPError("Error inesperado en reintentos")
