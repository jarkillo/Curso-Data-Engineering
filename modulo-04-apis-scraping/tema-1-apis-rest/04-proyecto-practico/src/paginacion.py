"""
Funciones para manejar paginación automática de APIs REST.

Soporta:
- Paginación Offset/Limit
- Paginación basada en Cursor
"""

from typing import Any, Dict, List, Optional

import requests
from src.cliente_http import hacer_get
from src.validaciones import extraer_json_seguro, validar_url


def paginar_offset_limit(
    url: str,
    limite_por_pagina: int = 100,
    nombre_param_offset: str = "offset",
    nombre_param_limit: str = "limit",
    params_extra: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    max_paginas: Optional[int] = None,
    timeout: int = 30,
) -> List[Dict[str, Any]]:
    """
    Itera automáticamente sobre todas las páginas usando Offset/Limit.

    La paginación se detiene cuando:
    - La respuesta está vacía (lista vacía)
    - Se alcanza max_paginas (si está definido)

    Args:
        url: URL base del endpoint
        limite_por_pagina: Cantidad de elementos por página
        nombre_param_offset: Nombre del parámetro de offset
        nombre_param_limit: Nombre del parámetro de limit
        params_extra: Parámetros adicionales para incluir en cada request
        headers: Headers HTTP
        max_paginas: Límite de páginas a extraer (None = sin límite)
        timeout: Timeout en segundos

    Returns:
        Lista con todos los elementos recolectados

    Raises:
        ValueError: Si parámetros son inválidos
        requests.exceptions.RequestException: Si hay error en requests

    Example:
        >>> # Requiere internet y API real
        >>> usuarios = paginar_offset_limit(
        ...     url="https://jsonplaceholder.typicode.com/users",
        ...     limite_por_pagina=5
        ... )
        >>> len(usuarios) > 0
        True
    """
    validar_url(url)

    if limite_por_pagina < 1:
        raise ValueError("limite_por_pagina debe ser al menos 1")

    if max_paginas is not None and max_paginas < 1:
        raise ValueError("max_paginas debe ser al menos 1")

    todos_resultados = []
    pagina_actual = 0
    offset_actual = 0

    while True:
        # Verificar límite de páginas
        if max_paginas is not None and pagina_actual >= max_paginas:
            break

        # Preparar parámetros
        params = params_extra.copy() if params_extra else {}
        params[nombre_param_offset] = offset_actual
        params[nombre_param_limit] = limite_por_pagina

        # Hacer request
        response = hacer_get(url=url, params=params, headers=headers, timeout=timeout)

        # Extraer datos
        datos = extraer_json_seguro(response)

        # Verificar si hay datos
        if not datos or len(datos) == 0:
            break

        # Agregar a resultados
        todos_resultados.extend(datos)

        # Avanzar a siguiente página
        pagina_actual += 1
        offset_actual += limite_por_pagina

    return todos_resultados


def paginar_cursor(
    url: str,
    campo_datos: str,
    campo_cursor: str,
    nombre_param_cursor: str = "cursor",
    params_extra: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    max_paginas: Optional[int] = None,
    timeout: int = 30,
) -> List[Dict[str, Any]]:
    """
    Itera automáticamente sobre todas las páginas usando Cursor.

    La paginación se detiene cuando:
    - El cursor es None o está vacío
    - Se alcanza max_paginas (si está definido)

    Args:
        url: URL base del endpoint
        campo_datos: Ruta al campo que contiene los datos (ej: "data", "results")
        campo_cursor: Ruta al campo del cursor (ej: "next_cursor", "pagination.next")
        nombre_param_cursor: Nombre del parámetro de cursor en la URL
        params_extra: Parámetros adicionales para incluir en cada request
        headers: Headers HTTP
        max_paginas: Límite de páginas a extraer (None = sin límite)
        timeout: Timeout en segundos

    Returns:
        Lista con todos los elementos recolectados

    Raises:
        ValueError: Si parámetros son inválidos
        requests.exceptions.RequestException: Si hay error en requests

    Note:
        Soporta campos anidados usando notación de punto (ej: "pagination.next")

    Example:
        >>> # Ejemplo con estructura típica:
        >>> # {
        >>> #   "data": [{"id": 1}, {"id": 2}],
        >>> #   "pagination": {"next_cursor": "abc123"}
        >>> # }
        >>> # resultados = paginar_cursor(
        >>> #     url="https://api.ejemplo.com/users",
        >>> #     campo_datos="data",
        >>> #     campo_cursor="pagination.next_cursor"
        >>> # )
    """
    validar_url(url)

    if not campo_datos:
        raise ValueError("campo_datos no puede estar vacío")

    if not campo_cursor:
        raise ValueError("campo_cursor no puede estar vacío")

    if max_paginas is not None and max_paginas < 1:
        raise ValueError("max_paginas debe ser al menos 1")

    todos_resultados = []
    pagina_actual = 0
    cursor_actual = None

    while True:
        # Verificar límite de páginas
        if max_paginas is not None and pagina_actual >= max_paginas:
            break

        # Preparar parámetros
        params = params_extra.copy() if params_extra else {}
        if cursor_actual:
            params[nombre_param_cursor] = cursor_actual

        # Hacer request
        response = hacer_get(url=url, params=params, headers=headers, timeout=timeout)

        # Extraer datos
        response_json = extraer_json_seguro(response)

        # Extraer campo de datos (puede ser anidado)
        datos = _extraer_campo_anidado(response_json, campo_datos)

        if not datos or len(datos) == 0:
            break

        # Agregar a resultados
        todos_resultados.extend(datos)

        # Extraer cursor para siguiente página
        cursor_actual = _extraer_campo_anidado(response_json, campo_cursor)

        # Si no hay cursor, terminamos
        if not cursor_actual:
            break

        pagina_actual += 1

    return todos_resultados


def _extraer_campo_anidado(data: dict, campo: str) -> Any:
    """
    Extrae un campo anidado usando notación de punto.

    Args:
        data: Diccionario de datos
        campo: Ruta al campo (ej: "data", "pagination.next")

    Returns:
        Valor del campo o None si no existe

    Example:
        >>> data = {"pagination": {"next": "abc"}}
        >>> _extraer_campo_anidado(data, "pagination.next")
        'abc'
        >>> _extraer_campo_anidado(data, "data")
    """
    partes = campo.split(".")
    valor_actual = data

    for parte in partes:
        if isinstance(valor_actual, dict) and parte in valor_actual:
            valor_actual = valor_actual[parte]
        else:
            return None

    return valor_actual
