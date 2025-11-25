"""
Módulo para generar y ejecutar queries de Amazon Athena.

Contiene funciones para construir queries SQL analíticas sobre
los datos procesados almacenados en S3.
"""

import uuid
from typing import Any


def generar_query_metricas_basicas(
    database: str, tabla: str, fecha_inicio: str, fecha_fin: str
) -> str:
    """
    Genera query SQL para métricas básicas de endpoints.

    Métricas:
    - Total de requests por endpoint
    - Promedio de response_time
    - Tasa de errores

    Args:
        database: Nombre de la base de datos en Athena
        tabla: Nombre de la tabla
        fecha_inicio: Fecha inicio (YYYY-MM-DD)
        fecha_fin: Fecha fin (YYYY-MM-DD)

    Returns:
        Query SQL como string

    Examples:
        >>> query = generar_query_metricas_basicas(
        ...     'cloudapi_analytics', 'logs_processed',
        ...     '2025-01-15', '2025-01-20'
        ... )
        >>> 'SELECT' in query
        True
        >>> 'FROM cloudapi_analytics.logs_processed' in query
        True
    """
    query = f"""
SELECT
    endpoint,
    COUNT(*) as total_requests,
    AVG(response_time_ms) as avg_response_time,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as error_rate
FROM {database}.{tabla}
WHERE timestamp >= TIMESTAMP '{fecha_inicio} 00:00:00'
  AND timestamp <= TIMESTAMP '{fecha_fin} 23:59:59'
GROUP BY endpoint
ORDER BY total_requests DESC
"""
    return query.strip()


def generar_query_percentiles(
    database: str, tabla: str, endpoint: str | None = None
) -> str:
    """
    Genera query para calcular percentiles de response_time.

    Calcula p50, p95, p99 para un endpoint específico o todos.

    Args:
        database: Nombre de la base de datos
        tabla: Nombre de la tabla
        endpoint: Endpoint específico (opcional, None para todos)

    Returns:
        Query SQL como string

    Examples:
        >>> query = generar_query_percentiles('cloudapi_analytics', 'logs_processed')
        >>> 'APPROX_PERCENTILE' in query or 'percentile_approx' in query
        True
    """
    where_clause = f"WHERE endpoint = '{endpoint}'" if endpoint else ""

    query = f"""
SELECT
    endpoint,
    APPROX_PERCENTILE(response_time_ms, 0.5) as p50_response_time,
    APPROX_PERCENTILE(response_time_ms, 0.95) as p95_response_time,
    APPROX_PERCENTILE(response_time_ms, 0.99) as p99_response_time,
    COUNT(*) as total_requests
FROM {database}.{tabla}
{where_clause}
GROUP BY endpoint
ORDER BY p99_response_time DESC
"""
    return query.strip()


def generar_query_top_endpoints_lentos(
    database: str, tabla: str, limite: int = 10
) -> str:
    """
    Genera query para obtener los endpoints más lentos.

    Args:
        database: Nombre de la base de datos
        tabla: Nombre de la tabla
        limite: Número de endpoints a retornar

    Returns:
        Query SQL como string

    Examples:
        >>> query = generar_query_top_endpoints_lentos(
        ...     'cloudapi_analytics', 'logs_processed', 5
        ... )
        >>> 'LIMIT 5' in query
        True
        >>> 'ORDER BY' in query
        True
    """
    query = f"""
SELECT
    endpoint,
    AVG(response_time_ms) as avg_response_time,
    MAX(response_time_ms) as max_response_time,
    COUNT(*) as total_requests
FROM {database}.{tabla}
GROUP BY endpoint
ORDER BY avg_response_time DESC
LIMIT {limite}
"""
    return query.strip()


def generar_query_tendencia_temporal(
    database: str, tabla: str, intervalo: str = "hour"
) -> str:
    """
    Genera query para analizar tendencias temporales.

    Args:
        database: Nombre de la base de datos
        tabla: Nombre de la tabla
        intervalo: Intervalo temporal ('hour', 'day', 'minute')

    Returns:
        Query SQL como string

    Examples:
        >>> query = generar_query_tendencia_temporal(
        ...     'cloudapi_analytics', 'logs_processed', 'hour'
        ... )
        >>> 'GROUP BY' in query
        True
    """
    # Mapear intervalo a función de truncamiento
    if intervalo == "hour":
        date_trunc = "DATE_TRUNC('hour', timestamp)"
    elif intervalo == "day":
        date_trunc = "DATE_TRUNC('day', timestamp)"
    elif intervalo == "minute":
        date_trunc = "DATE_TRUNC('minute', timestamp)"
    else:
        date_trunc = "DATE_TRUNC('hour', timestamp)"

    query = f"""
SELECT
    {date_trunc} as periodo,
    COUNT(*) as total_requests,
    AVG(response_time_ms) as avg_response_time,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as error_rate
FROM {database}.{tabla}
GROUP BY {date_trunc}
ORDER BY periodo ASC
"""
    return query.strip()


def generar_query_distribucion_errores(database: str, tabla: str) -> str:
    """
    Genera query para analizar distribución de errores HTTP.

    Args:
        database: Nombre de la base de datos
        tabla: Nombre de la tabla

    Returns:
        Query SQL como string

    Examples:
        >>> query = generar_query_distribucion_errores(
        ...     'cloudapi_analytics', 'logs_processed'
        ... )
        >>> 'status_code' in query
        True
    """
    query = f"""
SELECT
    status_code,
    COUNT(*) as occurrences,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage,
    CASE
        WHEN status_code BETWEEN 100 AND 199 THEN '1xx - Informational'
        WHEN status_code BETWEEN 200 AND 299 THEN '2xx - Success'
        WHEN status_code BETWEEN 300 AND 399 THEN '3xx - Redirection'
        WHEN status_code BETWEEN 400 AND 499 THEN '4xx - Client Error'
        WHEN status_code BETWEEN 500 AND 599 THEN '5xx - Server Error'
        ELSE 'Unknown'
    END as category
FROM {database}.{tabla}
GROUP BY status_code
ORDER BY occurrences DESC
"""
    return query.strip()


def generar_vista_metricas_diarias(database: str, tabla: str) -> str:
    """
    Genera query CREATE VIEW para métricas agregadas por día.

    Args:
        database: Nombre de la base de datos
        tabla: Nombre de la tabla

    Returns:
        Query CREATE VIEW como string

    Examples:
        >>> query = generar_vista_metricas_diarias(
        ...     'cloudapi_analytics', 'logs_processed'
        ... )
        >>> 'CREATE OR REPLACE VIEW' in query
        True
    """
    query = f"""
CREATE OR REPLACE VIEW {database}.daily_metrics AS
SELECT
    DATE_TRUNC('day', timestamp) as dia,
    endpoint,
    COUNT(*) as total_requests,
    AVG(response_time_ms) as avg_response_time,
    MIN(response_time_ms) as min_response_time,
    MAX(response_time_ms) as max_response_time,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as total_errors,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as error_rate
FROM {database}.{tabla}
GROUP BY DATE_TRUNC('day', timestamp), endpoint
ORDER BY dia DESC, total_requests DESC
"""
    return query.strip()


def ejecutar_query_athena_simulado(query: str) -> dict[str, Any]:
    """
    Simula la ejecución de una query de Athena (para testing local).

    En producción, esto usaría boto3 para ejecutar en Athena real.
    En local, retorna estructura de respuesta simulada.

    Args:
        query: Query SQL a ejecutar

    Returns:
        Diccionario con resultados simulados:
        - query_execution_id: ID de ejecución
        - status: Estado de la query
        - rows: Número de filas (simulado)

    Examples:
        >>> resultado = ejecutar_query_athena_simulado("SELECT * FROM tabla")
        >>> 'query_execution_id' in resultado
        True
        >>> resultado['status']
        'SUCCEEDED'
    """
    # Generar ID único para la ejecución
    execution_id = str(uuid.uuid4())

    # Simular respuesta exitosa
    return {
        "query_execution_id": execution_id,
        "status": "SUCCEEDED",
        "rows": 100,  # Simulado
        "query": query,
        "start_time": "2025-01-15T10:30:00Z",
        "end_time": "2025-01-15T10:30:05Z",
    }


def parsear_resultados_athena(resultados_raw: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Parsea resultados de Athena a formato estructurado.

    Args:
        resultados_raw: Respuesta raw de Athena

    Returns:
        Lista de diccionarios con resultados

    Examples:
        >>> raw = {
        ...     'ResultSet': {
        ...         'Rows': [
        ...             {'Data': [{'VarCharValue': 'endpoint'}, {'VarCharValue': 'count'}]},
        ...             {'Data': [{'VarCharValue': '/api/users'}, {'VarCharValue': '100'}]}
        ...         ]
        ...     }
        ... }
        >>> resultados = parsear_resultados_athena(raw)
        >>> len(resultados)
        1
        >>> resultados[0]['endpoint']
        '/api/users'
    """
    if "ResultSet" not in resultados_raw or "Rows" not in resultados_raw["ResultSet"]:
        return []

    rows = resultados_raw["ResultSet"]["Rows"]

    if not rows:
        return []

    # Primera fila es el header
    header_row = rows[0]
    headers = [col.get("VarCharValue", "") for col in header_row.get("Data", [])]

    # Resto son datos
    data_rows = rows[1:]

    resultados = []
    for row in data_rows:
        values = [col.get("VarCharValue", "") for col in row.get("Data", [])]
        resultado = dict(zip(headers, values, strict=False))
        resultados.append(resultado)

    return resultados
