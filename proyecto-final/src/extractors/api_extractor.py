"""Extractor de datos desde APIs REST."""

from typing import Any

import pandas as pd
import requests


def validate_api_response(response: dict[str, Any]) -> dict[str, Any]:
    """
    Valida la estructura de una respuesta de API.

    Args:
        response: Diccionario con la respuesta de la API.

    Returns:
        Diccionario con resultado de validación:
        - valid: bool indicando si es válida
        - record_count: número de registros (si válida)
        - error: mensaje de error (si inválida)

    Examples:
        >>> resp = {"status": "success", "data": [{"id": 1}], "total_count": 1}
        >>> validate_api_response(resp)
        {'valid': True, 'record_count': 1}
    """
    # Verificar campo status
    if "status" not in response:
        return {"valid": False, "error": "Missing 'status' field in response"}

    # Verificar que status no sea error
    if response["status"] == "error":
        return {
            "valid": False,
            "error": f"API returned error status: {response.get('message', 'Unknown')}",
        }

    # Verificar campo data
    if "data" not in response:
        return {"valid": False, "error": "Missing 'data' field in response"}

    # Respuesta válida
    return {"valid": True, "record_count": len(response["data"])}


def parse_order_response(response: dict[str, Any]) -> pd.DataFrame:
    """
    Parsea la respuesta de API de pedidos a DataFrame.

    Args:
        response: Respuesta validada de la API de pedidos.

    Returns:
        DataFrame con los pedidos parseados.

    Examples:
        >>> resp = {"status": "success", "data": [{"order_id": "1"}]}
        >>> df = parse_order_response(resp)
        >>> len(df)
        1
    """
    data = response.get("data", [])

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Convertir fechas si existe la columna
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"])

    return df


def extract_orders_from_api(
    url: str,
    api_key: str | None = None,
    timeout: int = 30,
    params: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Extrae pedidos desde una API REST.

    Args:
        url: URL del endpoint de pedidos.
        api_key: Clave de API para autenticación (opcional).
        timeout: Timeout en segundos para la petición.
        params: Parámetros de query string opcionales.

    Returns:
        DataFrame con los pedidos extraídos.

    Raises:
        ConnectionError: Si hay error de conexión o HTTP.

    Examples:
        >>> df = extract_orders_from_api("http://api.example.com/orders")
        >>> "order_id" in df.columns
        True
    """
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.get(
            url, headers=headers, timeout=timeout, params=params or {}
        )
    except requests.Timeout:
        raise ConnectionError(f"API request timeout after {timeout}s")
    except requests.RequestException as e:
        raise ConnectionError(f"API request failed: {e}")

    if response.status_code != 200:
        raise ConnectionError(
            f"API request failed with status code {response.status_code}"
        )

    response_data = response.json()

    validation = validate_api_response(response_data)
    if not validation["valid"]:
        raise ConnectionError(f"Invalid API response: {validation['error']}")

    return parse_order_response(response_data)
