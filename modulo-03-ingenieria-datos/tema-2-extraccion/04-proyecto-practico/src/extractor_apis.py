"""
Módulo de extracción de datos desde APIs REST.

Este módulo proporciona funciones para:
- Realizar peticiones HTTP con reintentos automáticos
- Manejar paginación de APIs
- Gestionar rate limiting
- Autenticación (API Key, Bearer Token)

Todas las funciones manejan errores de forma robusta y están completamente testeadas.
"""

import logging
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def configurar_sesion_con_reintentos(
    max_reintentos: int = 3,
    backoff_factor: float = 0.3,
    status_forcelist: tuple[int, ...] = (500, 502, 503, 504),
) -> requests.Session:
    """
    Configura una sesión de requests con estrategia de reintentos.

    Implementa reintentos automáticos con backoff exponencial para
    peticiones que fallan por errores temporales del servidor.

    Args:
        max_reintentos: Número máximo de reintentos (default: 3)
        backoff_factor: Factor multiplicador para el tiempo de espera
                       (0.3 = espera 0.3s, 0.6s, 1.2s, etc.)
        status_forcelist: Tupla de códigos HTTP que disparan reintento

    Returns:
        Sesión configurada con estrategia de reintentos

    Examples:
        >>> sesion = configurar_sesion_con_reintentos()
        >>> respuesta = sesion.get('https://api.ejemplo.com/datos')
    """
    if max_reintentos < 0:
        raise ValueError("max_reintentos debe ser >= 0")

    if backoff_factor < 0:
        raise ValueError("backoff_factor debe ser >= 0")

    sesion = requests.Session()

    estrategia_reintentos = Retry(
        total=max_reintentos,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST", "PUT", "DELETE"],
    )

    adaptador = HTTPAdapter(max_retries=estrategia_reintentos)
    sesion.mount("http://", adaptador)
    sesion.mount("https://", adaptador)

    return sesion


def hacer_peticion_con_autenticacion(
    url: str,
    metodo: str = "GET",
    auth_type: str | None = None,
    auth_token: str | None = None,
    params: dict | None = None,
    json_data: dict | None = None,
    headers: dict | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """
    Realiza una petición HTTP con autenticación.

    Soporta varios tipos de autenticación comunes en APIs REST.

    Args:
        url: URL de la API
        metodo: Método HTTP ('GET', 'POST', 'PUT', 'DELETE')
        auth_type: Tipo de autenticación ('api_key', 'bearer', None)
        auth_token: Token de autenticación
        params: Parámetros de query string
        json_data: Datos JSON para el body (POST/PUT)
        headers: Headers HTTP adicionales
        timeout: Timeout en segundos (default: 30)

    Returns:
        Respuesta JSON parseada como diccionario

    Raises:
        ValueError: Si los parámetros son inválidos
        requests.HTTPError: Si la petición falla (4xx, 5xx)
        requests.Timeout: Si se excede el timeout

    Examples:
        >>> respuesta = hacer_peticion_con_autenticacion(
        ...     'https://api.ejemplo.com/datos',
        ...     auth_type='bearer',
        ...     auth_token='mi_token'
        ... )
    """
    if not url:
        raise ValueError("La URL no puede estar vacía")

    if metodo.upper() not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        raise ValueError(f"Método HTTP no soportado: {metodo}")

    if auth_type and not auth_token:
        raise ValueError("Si se especifica auth_type, se debe proporcionar auth_token")

    # Configurar headers
    headers_peticion = headers.copy() if headers else {}

    if auth_type == "bearer":
        headers_peticion["Authorization"] = f"Bearer {auth_token}"
    elif auth_type == "api_key":
        # Común que API key vaya en header o en params
        headers_peticion["X-API-Key"] = auth_token

    # Configurar sesión con reintentos
    sesion = configurar_sesion_con_reintentos()

    try:
        logger.info(f"Realizando petición {metodo} a {url}")

        respuesta = sesion.request(
            method=metodo,
            url=url,
            params=params,
            json=json_data,
            headers=headers_peticion,
            timeout=timeout,
        )

        respuesta.raise_for_status()

        # Intentar parsear como JSON
        try:
            return respuesta.json()
        except Exception:
            # Si no es JSON, retornar texto
            return {"content": respuesta.text}

    except requests.exceptions.Timeout:
        logger.error(f"Timeout al hacer petición a {url}")
        raise
    except requests.exceptions.HTTPError:
        logger.error(f"Error HTTP {respuesta.status_code}: {respuesta.text}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise


def manejar_paginacion_offset_limit(
    url_base: str,
    param_offset: str = "offset",
    param_limit: str = "limit",
    limite_por_pagina: int = 100,
    max_resultados: int | None = None,
    **kwargs: Any,
) -> list[dict]:
    """
    Maneja paginación tipo offset/limit.

    Itera automáticamente por todas las páginas de una API que usa
    paginación offset/limit hasta obtener todos los resultados.

    Args:
        url_base: URL base de la API
        param_offset: Nombre del parámetro de offset (default: 'offset')
        param_limit: Nombre del parámetro de limit (default: 'limit')
        limite_por_pagina: Resultados por página (default: 100)
        max_resultados: Máximo número de resultados totales (None = todos)
        **kwargs: Argumentos adicionales para hacer_peticion_con_autenticacion

    Returns:
        Lista con todos los resultados combinados

    Raises:
        ValueError: Si los parámetros son inválidos

    Examples:
        >>> resultados = manejar_paginacion_offset_limit(
        ...     'https://api.ejemplo.com/usuarios',
        ...     limite_por_pagina=50,
        ...     auth_type='bearer',
        ...     auth_token='mi_token'
        ... )
    """
    if limite_por_pagina <= 0:
        raise ValueError("limite_por_pagina debe ser > 0")

    if max_resultados is not None and max_resultados <= 0:
        raise ValueError("max_resultados debe ser > 0 o None")

    resultados = []
    offset = 0

    while True:
        # Preparar params
        params = kwargs.get("params", {}).copy()
        params[param_offset] = offset
        params[param_limit] = limite_por_pagina
        kwargs["params"] = params

        logger.info(f"Obteniendo página con offset={offset}, limit={limite_por_pagina}")

        # Hacer petición
        respuesta = hacer_peticion_con_autenticacion(url_base, **kwargs)

        # Extraer datos (asumimos que están en 'data', 'results', o en root)
        if "data" in respuesta:
            datos_pagina = respuesta["data"]
        elif "results" in respuesta:
            datos_pagina = respuesta["results"]
        elif isinstance(respuesta, list):
            datos_pagina = respuesta
        else:
            # Si no encontramos estructura conocida, retornamos la respuesta completa
            datos_pagina = [respuesta]

        if not datos_pagina:
            # No hay más resultados
            break

        resultados.extend(datos_pagina)

        # Verificar si alcanzamos max_resultados
        if max_resultados and len(resultados) >= max_resultados:
            resultados = resultados[:max_resultados]
            break

        # Si recibimos menos resultados que el límite, no hay más páginas
        if len(datos_pagina) < limite_por_pagina:
            break

        offset += limite_por_pagina

    logger.info(f"Paginación completada. Total resultados: {len(resultados)}")
    return resultados


def manejar_paginacion_cursor(
    url_base: str,
    param_cursor: str = "cursor",
    campo_cursor_respuesta: str = "next_cursor",
    campo_datos_respuesta: str = "data",
    **kwargs: Any,
) -> list[dict]:
    """
    Maneja paginación tipo cursor.

    Itera por páginas usando cursores (común en APIs modernas como Twitter, Facebook).

    Args:
        url_base: URL base de la API
        param_cursor: Nombre del parámetro de cursor en la petición
        campo_cursor_respuesta: Campo en la respuesta que contiene el siguiente cursor
        campo_datos_respuesta: Campo en la respuesta que contiene los datos
        **kwargs: Argumentos adicionales para hacer_peticion_con_autenticacion

    Returns:
        Lista con todos los resultados combinados

    Examples:
        >>> resultados = manejar_paginacion_cursor(
        ...     'https://api.ejemplo.com/tweets',
        ...     param_cursor='next_token',
        ...     campo_cursor_respuesta='meta.next_token',
        ...     auth_type='bearer',
        ...     auth_token='mi_token'
        ... )
    """
    resultados = []
    cursor = None

    while True:
        # Preparar params
        params = kwargs.get("params", {}).copy()
        if cursor:
            params[param_cursor] = cursor
        kwargs["params"] = params

        logger.info(f"Obteniendo página con cursor={cursor}")

        # Hacer petición
        respuesta = hacer_peticion_con_autenticacion(url_base, **kwargs)

        # Extraer datos
        datos_pagina = respuesta.get(campo_datos_respuesta, [])
        resultados.extend(datos_pagina)

        # Obtener siguiente cursor (puede estar nested)
        if "." in campo_cursor_respuesta:
            # Cursor nested (ej: 'meta.next_cursor')
            partes = campo_cursor_respuesta.split(".")
            siguiente_cursor = respuesta
            for parte in partes:
                siguiente_cursor = siguiente_cursor.get(parte)
                if siguiente_cursor is None:
                    break
        else:
            siguiente_cursor = respuesta.get(campo_cursor_respuesta)

        if not siguiente_cursor:
            # No hay más páginas
            break

        cursor = siguiente_cursor

    logger.info(f"Paginación completada. Total resultados: {len(resultados)}")
    return resultados


def respetar_rate_limit(
    peticiones_por_minuto: int, tiempo_ultima_peticion: float | None = None
) -> None:
    """
    Espera el tiempo necesario para respetar el rate limit.

    Implementa throttling para no exceder el límite de peticiones por minuto
    de una API.

    Args:
        peticiones_por_minuto: Máximo número de peticiones permitidas por minuto
        tiempo_ultima_peticion: Timestamp de la última petición (None si es la primera)

    Raises:
        ValueError: Si peticiones_por_minuto <= 0

    Examples:
        >>> ultima = time.time()
        >>> respetar_rate_limit(60, ultima)  # Max 60 peticiones/minuto
        >>> # Espera automáticamente si es necesario
    """
    if peticiones_por_minuto <= 0:
        raise ValueError("peticiones_por_minuto debe ser > 0")

    if tiempo_ultima_peticion is None:
        # Primera petición, no hay que esperar
        return

    segundos_por_peticion = 60.0 / peticiones_por_minuto
    tiempo_transcurrido = time.time() - tiempo_ultima_peticion

    if tiempo_transcurrido < segundos_por_peticion:
        tiempo_espera = segundos_por_peticion - tiempo_transcurrido
        logger.debug(f"Rate limit: esperando {tiempo_espera:.2f} segundos")
        time.sleep(tiempo_espera)


def extraer_api_completa(
    url: str,
    tipo_paginacion: str = "offset",
    rate_limit: int | None = None,
    **kwargs: Any,
) -> list[dict]:
    """
    Función de alto nivel para extraer datos completos de una API.

    Combina paginación, rate limiting y manejo de errores en una sola función.

    Args:
        url: URL de la API
        tipo_paginacion: Tipo de paginación ('offset', 'cursor', 'none')
        rate_limit: Peticiones por minuto permitidas (None = sin límite)
        **kwargs: Argumentos para las funciones de paginación

    Returns:
        Lista con todos los resultados

    Raises:
        ValueError: Si tipo_paginacion no es válido

    Examples:
        >>> datos = extraer_api_completa(
        ...     'https://api.ejemplo.com/productos',
        ...     tipo_paginacion='offset',
        ...     rate_limit=60,
        ...     auth_type='bearer',
        ...     auth_token='mi_token'
        ... )
    """
    if tipo_paginacion not in ["offset", "cursor", "none"]:
        raise ValueError("tipo_paginacion debe ser 'offset', 'cursor' o 'none'")

    logger.info(f"Iniciando extracción completa de {url}")

    if tipo_paginacion == "none":
        # Sin paginación, una sola petición
        resultado = hacer_peticion_con_autenticacion(url, **kwargs)
        if isinstance(resultado, list):
            return resultado
        return [resultado]

    elif tipo_paginacion == "offset":
        return manejar_paginacion_offset_limit(url, **kwargs)

    else:  # cursor
        return manejar_paginacion_cursor(url, **kwargs)
