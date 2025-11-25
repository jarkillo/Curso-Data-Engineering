"""
Módulo para análisis de logs.

Funciones para calcular métricas, identificar problemas y detectar anomalías.
"""

from typing import Any


def calcular_tasa_error(logs: list[dict[str, Any]]) -> float:
    """
    Calcula la tasa de error como porcentaje del total de logs.

    Args:
        logs: Lista de documentos de log

    Returns:
        Tasa de error como porcentaje (0-100)

    Raises:
        ValueError: Si la lista está vacía

    Examples:
        >>> logs = [{"nivel": "ERROR"}, {"nivel": "INFO"}, {"nivel": "INFO"}]
        >>> calcular_tasa_error(logs)
        33.33
    """
    if not logs:
        raise ValueError("Lista de logs no puede estar vacía")

    total_logs = len(logs)
    total_errores = sum(1 for log in logs if log.get("nivel") == "ERROR")

    tasa = (total_errores / total_logs) * 100
    return round(tasa, 2)


def identificar_servicios_criticos(
    logs: list[dict[str, Any]], umbral_error: float = 50.0
) -> list[dict[str, Any]]:
    """
    Identifica servicios con tasa de error por encima del umbral.

    Args:
        logs: Lista de documentos de log
        umbral_error: Umbral de tasa de error (%) para considerar crítico

    Returns:
        Lista de servicios críticos con sus métricas

    Raises:
        ValueError: Si la lista está vacía

    Examples:
        >>> logs = [
        ...     {"servicio": "Service1", "nivel": "ERROR"},
        ...     {"servicio": "Service1", "nivel": "ERROR"},
        ...     {"servicio": "Service1", "nivel": "INFO"}
        ... ]
        >>> criticos = identificar_servicios_criticos(logs, umbral_error=50.0)
        >>> len(criticos) >= 1
        True
    """
    if not logs:
        raise ValueError("Lista de logs no puede estar vacía")

    # Agrupar por servicio
    servicios: dict[str, dict[str, Any]] = {}

    for log in logs:
        servicio = log.get("servicio", "Unknown")

        if servicio not in servicios:
            servicios[servicio] = {
                "servicio": servicio,
                "total_logs": 0,
                "total_errores": 0,
            }

        servicios[servicio]["total_logs"] += 1

        if log.get("nivel") == "ERROR":
            servicios[servicio]["total_errores"] += 1

    # Calcular tasa de error y filtrar críticos
    servicios_criticos = []

    for servicio_data in servicios.values():
        tasa_error = (
            servicio_data["total_errores"] / servicio_data["total_logs"]
        ) * 100

        if tasa_error >= umbral_error:
            servicio_data["tasa_error"] = round(tasa_error, 2)
            servicios_criticos.append(servicio_data)

    # Ordenar por tasa de error (descendente)
    servicios_criticos.sort(key=lambda x: x["tasa_error"], reverse=True)

    return servicios_criticos


def generar_reporte_resumen(logs: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Genera un reporte resumen con métricas generales.

    Args:
        logs: Lista de documentos de log

    Returns:
        Diccionario con métricas del reporte

    Raises:
        ValueError: Si la lista está vacía

    Examples:
        >>> logs = [
        ...     {"nivel": "ERROR", "servicio": "Service1"},
        ...     {"nivel": "INFO", "servicio": "Service2"}
        ... ]
        >>> reporte = generar_reporte_resumen(logs)
        >>> reporte["total_logs"]
        2
    """
    if not logs:
        raise ValueError("Lista de logs no puede estar vacía")

    total_logs = len(logs)

    # Contar por nivel
    total_errores = sum(1 for log in logs if log.get("nivel") == "ERROR")
    total_warnings = sum(1 for log in logs if log.get("nivel") == "WARNING")
    total_info = sum(1 for log in logs if log.get("nivel") == "INFO")

    # Servicios únicos
    servicios_unicos = len({log.get("servicio", "Unknown") for log in logs})

    # Tasa de error
    tasa_error = (total_errores / total_logs) * 100

    reporte = {
        "total_logs": total_logs,
        "errores": total_errores,
        "warnings": total_warnings,
        "info": total_info,
        "servicios_unicos": servicios_unicos,
        "tasa_error": round(tasa_error, 2),
    }

    return reporte


def detectar_anomalias(
    logs: list[dict[str, Any]], umbral_tiempo: int = 1000
) -> list[dict[str, Any]]:
    """
    Detecta anomalías en los logs (tiempos altos, errores concentrados).

    Args:
        logs: Lista de documentos de log
        umbral_tiempo: Umbral de tiempo de respuesta en ms para considerar anomalía

    Returns:
        Lista de logs anómalos

    Examples:
        >>> logs = [
        ...     {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 100},
        ...     {"servicio": "Service1", "nivel": "WARNING", "tiempo_respuesta": 5000}
        ... ]
        >>> anomalias = detectar_anomalias(logs, umbral_tiempo=1000)
        >>> len(anomalias) >= 1
        True
    """
    if not logs:
        return []

    anomalias = []

    # Detectar tiempos de respuesta anormalmente altos
    for log in logs:
        tiempo_respuesta = log.get("tiempo_respuesta")

        if tiempo_respuesta is not None and tiempo_respuesta >= umbral_tiempo:
            anomalias.append(log)

    # Detectar servicios con cantidad anormal de errores
    # Consideramos "anormal" si un servicio tiene >80% de errores
    servicios: dict[str, dict[str, int]] = {}

    for log in logs:
        servicio = log.get("servicio", "Unknown")

        if servicio not in servicios:
            servicios[servicio] = {"total": 0, "errores": 0}

        servicios[servicio]["total"] += 1

        if log.get("nivel") == "ERROR":
            servicios[servicio]["errores"] += 1

    # Agregar logs de servicios anómalos si no están ya en anomalías
    for log in logs:
        servicio = log.get("servicio", "Unknown")
        stats = servicios.get(servicio)

        if stats and stats["total"] >= 10:  # Solo si hay suficientes logs
            tasa_error = (stats["errores"] / stats["total"]) * 100

            if tasa_error >= 80 and log not in anomalias:
                anomalias.append(log)

    return anomalias
