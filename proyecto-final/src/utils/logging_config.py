"""Configuración de logging estructurado para el pipeline ETL."""

import json
import logging
import sys
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Formatter que produce logs en formato JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea un registro de log como JSON.

        Args:
            record: Registro de log a formatear.

        Returns:
            String JSON del registro.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Añadir campos extra si existen
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        # Añadir info de excepción si existe
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def get_logger(
    name: str,
    level: int = logging.INFO,
    json_format: bool = True,
) -> logging.Logger:
    """
    Obtiene un logger configurado.

    Args:
        name: Nombre del logger.
        level: Nivel de logging (default INFO).
        json_format: Si usar formato JSON (default True).

    Returns:
        Logger configurado.

    Examples:
        >>> logger = get_logger("etl_pipeline")
        >>> logger.info("Starting pipeline")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if json_format:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    logger.addHandler(handler)

    return logger


def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    **context: Any,
) -> None:
    """
    Registra un mensaje con contexto adicional.

    Args:
        logger: Logger a usar.
        level: Nivel de log.
        message: Mensaje a registrar.
        **context: Campos de contexto adicionales.

    Examples:
        >>> logger = get_logger("test")
        >>> log_with_context(logger, logging.INFO, "Processing", batch_id=123)
    """
    extra = {"extra_fields": context}
    logger.log(level, message, extra=extra)


def log_pipeline_start(logger: logging.Logger, pipeline_name: str) -> None:
    """
    Registra inicio de pipeline.

    Args:
        logger: Logger a usar.
        pipeline_name: Nombre del pipeline.

    Examples:
        >>> logger = get_logger("etl")
        >>> log_pipeline_start(logger, "daily_etl")
    """
    log_with_context(
        logger,
        logging.INFO,
        f"Pipeline '{pipeline_name}' started",
        pipeline=pipeline_name,
        event="pipeline_start",
    )


def log_pipeline_end(
    logger: logging.Logger,
    pipeline_name: str,
    success: bool,
    duration_seconds: float,
    records_processed: int = 0,
) -> None:
    """
    Registra fin de pipeline.

    Args:
        logger: Logger a usar.
        pipeline_name: Nombre del pipeline.
        success: Si el pipeline terminó exitosamente.
        duration_seconds: Duración en segundos.
        records_processed: Registros procesados.

    Examples:
        >>> logger = get_logger("etl")
        >>> log_pipeline_end(logger, "daily_etl", True, 120.5, 10000)
    """
    level = logging.INFO if success else logging.ERROR
    status = "completed" if success else "failed"

    log_with_context(
        logger,
        level,
        f"Pipeline '{pipeline_name}' {status}",
        pipeline=pipeline_name,
        event="pipeline_end",
        success=success,
        duration_seconds=duration_seconds,
        records_processed=records_processed,
    )


def log_step(
    logger: logging.Logger,
    step_name: str,
    status: str,
    **metrics: Any,
) -> None:
    """
    Registra un paso del pipeline.

    Args:
        logger: Logger a usar.
        step_name: Nombre del paso.
        status: Estado (started, completed, failed).
        **metrics: Métricas adicionales del paso.

    Examples:
        >>> logger = get_logger("etl")
        >>> log_step(logger, "extract", "completed", rows=1000)
    """
    level = logging.INFO if status != "failed" else logging.ERROR

    log_with_context(
        logger,
        level,
        f"Step '{step_name}': {status}",
        step=step_name,
        status=status,
        event="step",
        **metrics,
    )
