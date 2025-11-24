"""
Módulo con transformaciones ETL para AWS Glue.

Contiene funciones de transformación que se ejecutarían en Glue Jobs.
En local, se pueden ejecutar con PySpark o pandas.
"""

import statistics
from datetime import datetime
from typing import Any


def limpiar_nulls(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Elimina registros que contengan valores nulos en campos críticos.

    Campos críticos: timestamp, endpoint, method, status_code, response_time_ms

    Args:
        datos: Lista de diccionarios representando logs

    Returns:
        Lista de diccionarios sin registros con nulls en campos críticos

    Examples:
        >>> logs = [
        ...     {'timestamp': '2025-01-15T10:30:45Z', 'endpoint': '/api/users',
        ...      'method': 'GET', 'status_code': 200, 'response_time_ms': 145},
        ...     {'timestamp': None, 'endpoint': '/api/posts'}
        ... ]
        >>> limpios = limpiar_nulls(logs)
        >>> len(limpios)
        1
    """
    campos_criticos = [
        "timestamp",
        "endpoint",
        "method",
        "status_code",
        "response_time_ms",
    ]

    resultado = []
    for registro in datos:
        # Verificar que todos los campos críticos existan y no sean None
        es_valido = all(
            campo in registro and registro[campo] is not None
            for campo in campos_criticos
        )

        if es_valido:
            resultado.append(registro.copy())  # Copiar para no modificar original

    return resultado


def normalizar_timestamps(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Normaliza timestamps a formato ISO 8601 UTC.

    Args:
        datos: Lista de diccionarios con campo 'timestamp'

    Returns:
        Lista de diccionarios con timestamps normalizados

    Examples:
        >>> logs = [{'timestamp': '2025-01-15 10:30:45', 'endpoint': '/api/users'}]
        >>> normalizados = normalizar_timestamps(logs)
        >>> 'T' in normalizados[0]['timestamp']
        True
    """
    resultado = []

    for registro in datos:
        nuevo_registro = registro.copy()

        if "timestamp" in registro and registro["timestamp"]:
            timestamp_str = registro["timestamp"]

            # Intentar parsear diferentes formatos
            formatos = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%S",
            ]

            timestamp_obj = None
            for formato in formatos:
                try:
                    timestamp_obj = datetime.strptime(timestamp_str, formato)
                    break
                except ValueError:
                    continue

            if timestamp_obj:
                # Convertir a formato ISO 8601 UTC
                nuevo_registro["timestamp"] = timestamp_obj.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )

        resultado.append(nuevo_registro)

    return resultado


def calcular_metricas_por_endpoint(
    logs: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    """
    Calcula métricas agregadas por endpoint.

    Métricas calculadas:
    - avg_response_time: Promedio de response_time_ms
    - p50_response_time: Percentil 50 (mediana)
    - p95_response_time: Percentil 95
    - p99_response_time: Percentil 99
    - total_requests: Número total de requests
    - error_rate: Porcentaje de requests con status_code >= 400

    Args:
        logs: Lista de logs de API

    Returns:
        Diccionario con endpoint como key y métricas como value

    Examples:
        >>> logs = [
        ...     {'endpoint': '/api/users', 'response_time_ms': 100, 'status_code': 200},
        ...     {'endpoint': '/api/users', 'response_time_ms': 150, 'status_code': 200},
        ...     {'endpoint': '/api/users', 'response_time_ms': 200, 'status_code': 500}
        ... ]
        >>> metricas = calcular_metricas_por_endpoint(logs)
        >>> metricas['/api/users']['avg_response_time']
        150.0
        >>> metricas['/api/users']['error_rate']
        33.33
    """
    # Agrupar logs por endpoint
    logs_por_endpoint: dict[str, list[dict[str, Any]]] = {}

    for log in logs:
        endpoint = log.get("endpoint", "unknown")
        if endpoint not in logs_por_endpoint:
            logs_por_endpoint[endpoint] = []
        logs_por_endpoint[endpoint].append(log)

    # Calcular métricas para cada endpoint
    metricas: dict[str, dict[str, float]] = {}

    for endpoint, logs_endpoint in logs_por_endpoint.items():
        response_times = [log["response_time_ms"] for log in logs_endpoint]
        total_requests = len(logs_endpoint)
        errores = sum(1 for log in logs_endpoint if log["status_code"] >= 400)

        metricas[endpoint] = {
            "avg_response_time": round(statistics.mean(response_times), 2),
            "p50_response_time": round(statistics.median(response_times), 2),
            "p95_response_time": (
                round(statistics.quantiles(response_times, n=20)[18], 2)  # Percentil 95
                if len(response_times) >= 20
                else round(max(response_times), 2)
            ),
            "p99_response_time": (
                round(
                    statistics.quantiles(response_times, n=100)[98],
                    2,  # Percentil 99
                )
                if len(response_times) >= 100
                else round(max(response_times), 2)
            ),
            "total_requests": total_requests,
            "error_rate": round((errores / total_requests) * 100, 2),
        }

    return metricas


def agregar_columna_fecha(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Agrega columnas de fecha para particionamiento.

    Añade columnas: year, month, day extraídas del timestamp.

    Args:
        datos: Lista de diccionarios con campo 'timestamp'

    Returns:
        Lista de diccionarios con columnas year, month, day añadidas

    Examples:
        >>> logs = [{'timestamp': '2025-01-15T10:30:45Z', 'endpoint': '/api/users'}]
        >>> con_fecha = agregar_columna_fecha(logs)
        >>> con_fecha[0]['year']
        '2025'
        >>> con_fecha[0]['month']
        '01'
        >>> con_fecha[0]['day']
        '15'
    """
    resultado = []

    for registro in datos:
        nuevo_registro = registro.copy()

        if "timestamp" in registro and registro["timestamp"]:
            timestamp_str = registro["timestamp"]

            # Parsear timestamp
            try:
                # Intentar formato ISO 8601
                if "T" in timestamp_str:
                    timestamp_obj = datetime.fromisoformat(
                        timestamp_str.replace("Z", "+00:00")
                    )
                else:
                    timestamp_obj = datetime.strptime(
                        timestamp_str, "%Y-%m-%d %H:%M:%S"
                    )

                # Extraer componentes de fecha
                nuevo_registro["year"] = timestamp_obj.strftime("%Y")
                nuevo_registro["month"] = timestamp_obj.strftime("%m")
                nuevo_registro["day"] = timestamp_obj.strftime("%d")
            except (ValueError, AttributeError):
                # Si no se puede parsear, no agregar columnas
                pass

        resultado.append(nuevo_registro)

    return resultado


def convertir_a_parquet_schema(datos: list[dict[str, Any]]) -> dict[str, list[Any]]:
    """
    Convierte lista de diccionarios a formato columnar (schema Parquet).

    Args:
        datos: Lista de diccionarios

    Returns:
        Diccionario con columnas como keys y listas de valores como values

    Examples:
        >>> logs = [
        ...     {'endpoint': '/api/users', 'status_code': 200},
        ...     {'endpoint': '/api/posts', 'status_code': 404}
        ... ]
        >>> columnar = convertir_a_parquet_schema(logs)
        >>> columnar['endpoint']
        ['/api/users', '/api/posts']
        >>> columnar['status_code']
        [200, 404]
    """
    if not datos:
        return {}

    # Obtener todas las columnas de todos los registros
    columnas: set[str] = set()
    for registro in datos:
        columnas.update(registro.keys())

    # Crear diccionario columnar
    resultado: dict[str, list[Any]] = {columna: [] for columna in columnas}

    for registro in datos:
        for columna in columnas:
            resultado[columna].append(registro.get(columna, None))

    return resultado


def filtrar_por_rango_fechas(
    datos: list[dict[str, Any]], fecha_inicio: str, fecha_fin: str
) -> list[dict[str, Any]]:
    """
    Filtra logs por rango de fechas.

    Args:
        datos: Lista de logs con campo 'timestamp'
        fecha_inicio: Fecha inicio en formato YYYY-MM-DD
        fecha_fin: Fecha fin en formato YYYY-MM-DD

    Returns:
        Lista filtrada de logs dentro del rango

    Examples:
        >>> logs = [
        ...     {'timestamp': '2025-01-15T10:30:45Z'},
        ...     {'timestamp': '2025-01-20T10:30:45Z'},
        ...     {'timestamp': '2025-01-25T10:30:45Z'}
        ... ]
        >>> filtrados = filtrar_por_rango_fechas(logs, '2025-01-14', '2025-01-20')
        >>> len(filtrados)
        2
    """
    # Parsear fechas límite
    fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d")
    fecha_fin_obj = fecha_fin_obj.replace(hour=23, minute=59, second=59)

    resultado = []

    for registro in datos:
        if "timestamp" in registro and registro["timestamp"]:
            timestamp_str = registro["timestamp"]

            try:
                # Parsear timestamp
                if "T" in timestamp_str:
                    timestamp_obj = datetime.fromisoformat(
                        timestamp_str.replace("Z", "+00:00")
                    )
                    # Convertir a naive datetime (sin timezone info)
                    timestamp_obj = timestamp_obj.replace(tzinfo=None)
                else:
                    timestamp_obj = datetime.strptime(
                        timestamp_str, "%Y-%m-%d %H:%M:%S"
                    )

                # Verificar si está dentro del rango
                if fecha_inicio_obj <= timestamp_obj <= fecha_fin_obj:
                    resultado.append(registro.copy())
            except (ValueError, AttributeError):
                # Si no se puede parsear, ignorar registro
                pass

    return resultado


def agregar_categoria_status(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Agrega una columna 'status_category' basada en status_code.

    Categorías:
    - '1xx': Informativos (100-199)
    - '2xx': Éxito (200-299)
    - '3xx': Redirección (300-399)
    - '4xx': Error del cliente (400-499)
    - '5xx': Error del servidor (500-599)

    Args:
        datos: Lista de logs con campo 'status_code'

    Returns:
        Lista de logs con campo 'status_category' añadido

    Examples:
        >>> logs = [
        ...     {'status_code': 200},
        ...     {'status_code': 404},
        ...     {'status_code': 500}
        ... ]
        >>> con_categoria = agregar_categoria_status(logs)
        >>> con_categoria[0]['status_category']
        '2xx'
        >>> con_categoria[1]['status_category']
        '4xx'
    """
    resultado = []

    for registro in datos:
        nuevo_registro = registro.copy()

        if "status_code" in registro:
            status_code = registro["status_code"]

            if 100 <= status_code < 200:
                categoria = "1xx"
            elif 200 <= status_code < 300:
                categoria = "2xx"
            elif 300 <= status_code < 400:
                categoria = "3xx"
            elif 400 <= status_code < 500:
                categoria = "4xx"
            elif 500 <= status_code < 600:
                categoria = "5xx"
            else:
                categoria = "unknown"

            nuevo_registro["status_category"] = categoria

        resultado.append(nuevo_registro)

    return resultado


def eliminar_duplicados(
    datos: list[dict[str, Any]], campos_clave: list[str]
) -> list[dict[str, Any]]:
    """
    Elimina registros duplicados basándose en campos clave.

    Args:
        datos: Lista de registros
        campos_clave: Lista de nombres de campos para identificar duplicados

    Returns:
        Lista sin duplicados

    Examples:
        >>> logs = [
        ...     {'timestamp': '2025-01-15T10:30:45Z', 'user_id': 'user_1'},
        ...     {'timestamp': '2025-01-15T10:30:45Z', 'user_id': 'user_1'},  # Duplicado
        ...     {'timestamp': '2025-01-15T10:30:46Z', 'user_id': 'user_2'}
        ... ]
        >>> sin_dups = eliminar_duplicados(logs, ['timestamp', 'user_id'])
        >>> len(sin_dups)
        2
    """
    vistos: set[tuple] = set()
    resultado = []

    for registro in datos:
        # Crear tupla con valores de campos clave
        clave = tuple(registro.get(campo) for campo in campos_clave)

        if clave not in vistos:
            vistos.add(clave)
            resultado.append(registro.copy())

    return resultado
