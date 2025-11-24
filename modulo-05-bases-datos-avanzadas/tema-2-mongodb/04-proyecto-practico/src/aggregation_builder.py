"""
Módulo para construir pipelines de agregación de MongoDB.

Funciones para crear pipelines complejos de agregación para análisis de logs.
"""

from datetime import datetime
from typing import Any


def construir_pipeline_errores(
    fecha_inicio: str, fecha_fin: str
) -> list[dict[str, Any]]:
    """
    Construye pipeline de agregación para filtrar y agrupar errores por período.

    Args:
        fecha_inicio: Fecha de inicio en formato "YYYY-MM-DD"
        fecha_fin: Fecha de fin en formato "YYYY-MM-DD"

    Returns:
        Lista de etapas del pipeline de agregación

    Raises:
        ValueError: Si las fechas están vacías o tienen formato inválido

    Examples:
        >>> pipeline = construir_pipeline_errores("2024-11-01", "2024-11-30")
        >>> len(pipeline) >= 2
        True
    """
    if not fecha_inicio or not fecha_inicio.strip():
        raise ValueError("Fecha de inicio no puede estar vacía")

    if not fecha_fin or not fecha_fin.strip():
        raise ValueError("Fecha de fin no puede estar vacía")

    # Validar formato de fechas
    try:
        datetime.strptime(fecha_inicio, "%Y-%m-%d")
        datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Fecha de inicio inválida. Formato esperado: YYYY-MM-DD")

    pipeline = [
        # Filtrar solo errores y por rango de fechas
        {
            "$match": {
                "nivel": "ERROR",
                "timestamp": {
                    "$gte": fecha_inicio,
                    "$lte": fecha_fin,
                },
            }
        },
        # Agrupar por servicio y contar errores
        {
            "$group": {
                "_id": "$servicio",
                "total_errores": {"$sum": 1},
                "mensajes": {"$push": "$mensaje"},
            }
        },
        # Ordenar por cantidad de errores (descendente)
        {"$sort": {"total_errores": -1}},
    ]

    return pipeline


def construir_pipeline_por_servicio() -> list[dict[str, Any]]:
    """
    Construye pipeline para agrupar logs por servicio.

    Returns:
        Lista de etapas del pipeline de agregación

    Examples:
        >>> pipeline = construir_pipeline_por_servicio()
        >>> any('$group' in stage for stage in pipeline)
        True
    """
    pipeline = [
        # Agrupar por servicio
        {
            "$group": {
                "_id": "$servicio",
                "total_logs": {"$sum": 1},
                "nivel_error": {
                    "$sum": {"$cond": [{"$eq": ["$nivel", "ERROR"]}, 1, 0]}
                },
                "nivel_warning": {
                    "$sum": {"$cond": [{"$eq": ["$nivel", "WARNING"]}, 1, 0]}
                },
                "nivel_info": {"$sum": {"$cond": [{"$eq": ["$nivel", "INFO"]}, 1, 0]}},
            }
        },
        # Calcular porcentaje de errores
        {
            "$project": {
                "servicio": "$_id",
                "total_logs": 1,
                "nivel_error": 1,
                "nivel_warning": 1,
                "nivel_info": 1,
                "porcentaje_error": {
                    "$multiply": [
                        {"$divide": ["$nivel_error", "$total_logs"]},
                        100,
                    ]
                },
            }
        },
        # Ordenar por total de logs (descendente)
        {"$sort": {"total_logs": -1}},
    ]

    return pipeline


def construir_pipeline_top_usuarios(limite: int) -> list[dict[str, Any]]:
    """
    Construye pipeline para obtener top usuarios con más actividad.

    Args:
        limite: Número máximo de usuarios a retornar

    Returns:
        Lista de etapas del pipeline de agregación

    Raises:
        ValueError: Si límite es menor o igual a 0

    Examples:
        >>> pipeline = construir_pipeline_top_usuarios(10)
        >>> any('$limit' in stage for stage in pipeline)
        True
    """
    if limite <= 0:
        raise ValueError("Límite debe ser mayor que 0")

    pipeline = [
        # Agrupar por usuario
        {
            "$group": {
                "_id": "$usuario_id",
                "total_acciones": {"$sum": 1},
                "servicios_usados": {"$addToSet": "$servicio"},
                "ultimo_acceso": {"$max": "$timestamp"},
            }
        },
        # Ordenar por cantidad de acciones (descendente)
        {"$sort": {"total_acciones": -1}},
        # Limitar resultados
        {"$limit": limite},
        # Proyectar campos finales
        {
            "$project": {
                "usuario_id": "$_id",
                "total_acciones": 1,
                "cantidad_servicios": {"$size": "$servicios_usados"},
                "ultimo_acceso": 1,
                "_id": 0,
            }
        },
    ]

    return pipeline


def construir_pipeline_metricas_tiempo() -> list[dict[str, Any]]:
    """
    Construye pipeline para analizar métricas por período de tiempo.

    Returns:
        Lista de etapas del pipeline de agregación

    Examples:
        >>> pipeline = construir_pipeline_metricas_tiempo()
        >>> any('$project' in stage for stage in pipeline)
        True
    """
    pipeline = [
        # Extraer componentes de fecha del timestamp
        {
            "$project": {
                "fecha": {
                    "$dateFromString": {
                        "dateString": "$timestamp",
                        "format": "%Y-%m-%d %H:%M:%S",
                    }
                },
                "nivel": 1,
                "servicio": 1,
            }
        },
        # Agregar campos de tiempo
        {
            "$project": {
                "hora": {"$hour": "$fecha"},
                "dia_semana": {"$dayOfWeek": "$fecha"},
                "dia_mes": {"$dayOfMonth": "$fecha"},
                "nivel": 1,
                "servicio": 1,
            }
        },
        # Agrupar por hora del día
        {
            "$group": {
                "_id": "$hora",
                "total_logs": {"$sum": 1},
                "errores": {"$sum": {"$cond": [{"$eq": ["$nivel", "ERROR"]}, 1, 0]}},
                "warnings": {"$sum": {"$cond": [{"$eq": ["$nivel", "WARNING"]}, 1, 0]}},
            }
        },
        # Ordenar por hora
        {"$sort": {"_id": 1}},
    ]

    return pipeline
