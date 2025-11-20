"""
Utilidades de logging para el proyecto.

Proporciona funciones estandarizadas para logging que facilitan:
- Debugging con contexto estructurado
- Tracking de errores en producción (Sentry)
- Eventos de analytics (Statsig)
"""

import logging
from typing import Any

# Configurar logger base
logger = logging.getLogger(__name__)


def log_for_debugging(message: str, context: dict[str, Any] | None = None) -> None:
    """
    Log información de debugging visible para el usuario.

    Útil para mensajes que ayudan a entender el flujo del programa
    durante desarrollo o troubleshooting.

    Args:
        message: Mensaje descriptivo del evento
        context: Diccionario con contexto adicional (opcional)

    Examples:
        >>> log_for_debugging("Procesando lote 3 de 10", {"rows": 1000})
        >>> log_for_debugging("Checkpoint no encontrado, usando default")
    """
    context = context or {}
    if context:
        logger.info(f"{message} | Context: {context}")
    else:
        logger.info(message)


def log_error(
    message: str, context: dict[str, Any] | None = None, exc_info: bool = True
) -> None:
    """
    Log errores con contexto para tracking en producción.

    En producción, estos errores deberían enviarse a Sentry para
    monitoreo y alertas.

    Args:
        message: Descripción del error
        context: Contexto con error_id, detalles técnicos, etc.
        exc_info: Si incluir traceback completo (default: True)

    Examples:
        >>> log_error("Database connection failed", {
        ...     "error_id": "DB_CONN_001",
        ...     "host": "localhost",
        ...     "port": 5432
        ... })
    """
    context = context or {}
    logger.error(f"{message} | Context: {context}", extra=context, exc_info=exc_info)


def log_event(event_name: str, properties: dict[str, Any] | None = None) -> None:
    """
    Log eventos para analytics (Statsig, Mixpanel, etc.).

    Útil para tracking de métricas de negocio y comportamiento de usuarios.

    Args:
        event_name: Nombre del evento (ej: "pipeline_completed")
        properties: Propiedades del evento (ej: rows_processed, duration_ms)

    Examples:
        >>> log_event("incremental_load_completed", {
        ...     "rows_loaded": 1500,
        ...     "duration_ms": 234,
        ...     "strategy": "incremental"
        ... })
    """
    properties = properties or {}
    logger.info(f"Event: {event_name} | Properties: {properties}")
