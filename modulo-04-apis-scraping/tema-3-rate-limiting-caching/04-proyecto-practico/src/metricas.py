"""
Métricas - Módulo para monitorear performance del scraper

Este módulo implementa un sistema de monitoreo de métricas para
analizar el rendimiento del scraper optimizado.

Métricas incluidas:
- Total de requests
- Cache hit rate (% de requests servidos desde cache)
- Throughput (requests por segundo)
- Latencia promedio
- Tiempo total de ejecución

Ejemplo de uso:
    monitor = crear_monitor_metricas()

    # Registrar requests
    registrar_request(monitor, fue_cache_hit=True, tiempo_ms=5.0)
    registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500.0)

    # Obtener reporte
    reporte = obtener_reporte_metricas(monitor)
    print(reporte)

    # Exportar a JSON
    exportar_metricas_json(monitor, "metricas.json")
"""

import json
import time
from typing import Dict


def crear_monitor_metricas() -> Dict:
    """
    Crea un monitor de métricas inicializado en cero.

    Returns:
        Diccionario con configuración del monitor

    Ejemplo:
        >>> monitor = crear_monitor_metricas()
        >>> monitor["total_requests"]
        0
    """
    return {
        "total_requests": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "tiempos_ms": [],
        "inicio": time.time(),
    }


def registrar_request(monitor: Dict, fue_cache_hit: bool, tiempo_ms: float) -> None:
    """
    Registra un request en el monitor de métricas.

    Args:
        monitor: Configuración del monitor
        fue_cache_hit: True si fue servido desde cache
        tiempo_ms: Tiempo de respuesta en milisegundos

    Ejemplo:
        >>> monitor = crear_monitor_metricas()
        >>> registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.5)
        >>> monitor["total_requests"]
        1
        >>> monitor["cache_hits"]
        1
    """
    monitor["total_requests"] += 1

    if fue_cache_hit:
        monitor["cache_hits"] += 1
    else:
        monitor["cache_misses"] += 1

    monitor["tiempos_ms"].append(tiempo_ms)


def obtener_reporte_metricas(monitor: Dict) -> str:
    """
    Genera un reporte legible de las métricas.

    Args:
        monitor: Configuración del monitor

    Returns:
        Reporte formateado con ASCII art

    Ejemplo:
        >>> monitor = crear_monitor_metricas()
        >>> registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.0)
        >>> reporte = obtener_reporte_metricas(monitor)
        >>> "Total requests" in reporte or "total" in reporte.lower()
        True
    """
    # Calcular métricas
    tiempo_total = time.time() - monitor["inicio"]
    total_requests = monitor["total_requests"]
    cache_hits = monitor["cache_hits"]
    cache_misses = monitor["cache_misses"]

    # Calcular cache hit rate
    if total_requests > 0:
        hit_rate = (cache_hits / total_requests) * 100
    else:
        hit_rate = 0.0

    # Calcular throughput
    if tiempo_total > 0:
        throughput = total_requests / tiempo_total
    else:
        throughput = 0.0

    # Calcular latencia promedio
    if monitor["tiempos_ms"]:
        latencia_promedio = sum(monitor["tiempos_ms"]) / len(monitor["tiempos_ms"])
    else:
        latencia_promedio = 0.0

    # Generar reporte con ASCII art
    reporte = f"""
╔════════════════════════════════════════════════╗
║          📊 MÉTRICAS DEL SCRAPER               ║
╠════════════════════════════════════════════════╣
║ ⏱️  Tiempo total:        {tiempo_total:>6.1f}s             ║
║ 📝 Total requests:       {total_requests:>6}               ║
║ ⚡ Throughput:           {throughput:>6.1f} req/seg        ║
╠════════════════════════════════════════════════╣
║ ✅ Cache HITS:           {cache_hits:>6} ({hit_rate:>5.1f}%)       ║
║ 🌐 Cache MISSES:         {cache_misses:>6} ({100-hit_rate:>5.1f}%)       ║
║ 💰 Requests ahorrados:   {cache_hits:>6}               ║
╠════════════════════════════════════════════════╣
║ 📊 Latencia promedio:    {latencia_promedio:>6.1f}ms            ║
║ 💵 Costo estimado:       ${(cache_misses * 0.001):>5.2f} (vs ${(total_requests * 0.001):.2f})    ║
║ 💰 Ahorro:               {hit_rate:>5.1f}% (cache)          ║
╚════════════════════════════════════════════════╝
"""

    return reporte


def exportar_metricas_json(monitor: Dict, archivo: str) -> None:
    """
    Exporta las métricas a un archivo JSON.

    Args:
        monitor: Configuración del monitor
        archivo: Ruta del archivo JSON a crear

    Ejemplo:
        >>> import tempfile
        >>> import os
        >>> monitor = crear_monitor_metricas()
        >>> registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.0)
        >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        ...     archivo = f.name
        >>> exportar_metricas_json(monitor, archivo)
        >>> os.path.exists(archivo)
        True
        >>> os.remove(archivo)  # Limpiar
    """
    # Calcular métricas adicionales
    tiempo_total = time.time() - monitor["inicio"]
    total_requests = monitor["total_requests"]

    if total_requests > 0:
        hit_rate = (monitor["cache_hits"] / total_requests) * 100
    else:
        hit_rate = 0.0

    if tiempo_total > 0:
        throughput = total_requests / tiempo_total
    else:
        throughput = 0.0

    if monitor["tiempos_ms"]:
        latencia_promedio = sum(monitor["tiempos_ms"]) / len(monitor["tiempos_ms"])
        latencia_min = min(monitor["tiempos_ms"])
        latencia_max = max(monitor["tiempos_ms"])
    else:
        latencia_promedio = 0.0
        latencia_min = 0.0
        latencia_max = 0.0

    # Preparar datos para JSON
    datos = {
        "timestamp": time.time(),
        "duracion_segundos": tiempo_total,
        "total_requests": total_requests,
        "cache_hits": monitor["cache_hits"],
        "cache_misses": monitor["cache_misses"],
        "cache_hit_rate_pct": round(hit_rate, 2),
        "throughput_req_seg": round(throughput, 2),
        "latencia": {
            "promedio_ms": round(latencia_promedio, 2),
            "min_ms": round(latencia_min, 2),
            "max_ms": round(latencia_max, 2),
        },
        "costo_estimado": {
            "total_usd": round(total_requests * 0.001, 4),
            "real_usd": round(monitor["cache_misses"] * 0.001, 4),
            "ahorro_usd": round(monitor["cache_hits"] * 0.001, 4),
            "ahorro_pct": round(hit_rate, 2),
        },
    }

    # Escribir a archivo
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
