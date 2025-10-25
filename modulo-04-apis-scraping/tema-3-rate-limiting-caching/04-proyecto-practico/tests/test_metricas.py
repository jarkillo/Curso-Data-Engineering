"""
Tests para metricas.py - Monitoreo y Métricas (TDD)

Módulo 4 - Tema 3: Scraper Masivo Optimizado
Total de tests: 10
Cobertura objetivo: >85%
"""

import json
import os

from src.metricas import (
    crear_monitor_metricas,
    exportar_metricas_json,
    obtener_reporte_metricas,
    registrar_request,
)

# ===============================
# Tests: Crear Monitor
# ===============================


def test_crear_monitor_inicializado_en_cero():
    """Test: Crear monitor inicializado en cero."""
    monitor = crear_monitor_metricas()

    assert monitor is not None
    assert monitor["total_requests"] == 0
    assert monitor["cache_hits"] == 0
    assert monitor["cache_misses"] == 0
    assert monitor["tiempos_ms"] == []
    assert "inicio" in monitor


# ===============================
# Tests: Registrar Requests
# ===============================


def test_registrar_cache_hit_incrementa_contador():
    """Test: Registrar cache hit incrementa contador."""
    monitor = crear_monitor_metricas()

    registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.5)

    assert monitor["total_requests"] == 1
    assert monitor["cache_hits"] == 1
    assert monitor["cache_misses"] == 0
    assert 10.5 in monitor["tiempos_ms"]


def test_registrar_cache_miss_incrementa_contador():
    """Test: Registrar cache miss incrementa contador."""
    monitor = crear_monitor_metricas()

    registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500.0)

    assert monitor["total_requests"] == 1
    assert monitor["cache_hits"] == 0
    assert monitor["cache_misses"] == 1
    assert 500.0 in monitor["tiempos_ms"]


def test_calcular_cache_hit_rate_correctamente():
    """Test: Calcular cache hit rate correctamente."""
    monitor = crear_monitor_metricas()

    # 7 cache hits, 3 cache misses = 70% hit rate
    for _ in range(7):
        registrar_request(monitor, fue_cache_hit=True, tiempo_ms=5.0)

    for _ in range(3):
        registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500.0)

    reporte = obtener_reporte_metricas(monitor)

    assert "70.0%" in reporte  # Hit rate debe ser 70%
    assert monitor["cache_hits"] == 7
    assert monitor["cache_misses"] == 3
    assert monitor["total_requests"] == 10


# ===============================
# Tests: Cálculos de Métricas
# ===============================


def test_calcular_throughput_requests_por_segundo():
    """Test: Calcular throughput (requests/segundo)."""
    import time

    monitor = crear_monitor_metricas()

    # Simular 10 requests
    for _ in range(10):
        registrar_request(monitor, fue_cache_hit=False, tiempo_ms=100.0)
        time.sleep(0.1)  # Esperar 0.1 seg entre requests

    reporte = obtener_reporte_metricas(monitor)

    # Debe calcular throughput
    assert "req/seg" in reporte or "requests/segundo" in reporte.lower()
    assert monitor["total_requests"] == 10


def test_calcular_latencia_promedio():
    """Test: Calcular latencia promedio."""
    monitor = crear_monitor_metricas()

    # Registrar requests con diferentes tiempos
    tiempos = [100.0, 200.0, 300.0, 400.0, 500.0]
    for tiempo in tiempos:
        registrar_request(monitor, fue_cache_hit=False, tiempo_ms=tiempo)

    reporte = obtener_reporte_metricas(monitor)

    # Latencia promedio debe ser 300ms
    assert "300" in reporte  # Buscar "300" en el reporte
    assert len(monitor["tiempos_ms"]) == 5


# ===============================
# Tests: Reporte de Métricas
# ===============================


def test_reporte_incluye_todas_las_metricas():
    """Test: Reporte incluye todas las métricas."""
    monitor = crear_monitor_metricas()

    # Registrar algunas métricas
    registrar_request(monitor, fue_cache_hit=True, tiempo_ms=5.0)
    registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500.0)
    registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.0)

    reporte = obtener_reporte_metricas(monitor)

    # Verificar que incluye métricas clave
    assert "Total requests" in reporte or "total" in reporte.lower()
    assert "Cache" in reporte or "cache" in reporte.lower()
    assert "Throughput" in reporte or "throughput" in reporte.lower()
    assert "Latencia" in reporte or "latencia" in reporte.lower()


def test_reporte_formateado_legible_ascii_art():
    """Test: Reporte formateado legible (ASCII art)."""
    monitor = crear_monitor_metricas()

    for i in range(5):
        registrar_request(monitor, fue_cache_hit=(i % 2 == 0), tiempo_ms=100.0)

    reporte = obtener_reporte_metricas(monitor)

    # Verificar formato ASCII (bordes, líneas)
    assert "═" in reporte or "─" in reporte or "+" in reporte
    assert "\n" in reporte  # Múltiples líneas
    assert len(reporte) > 100  # Reporte debe ser sustancial


# ===============================
# Tests: Exportar Métricas
# ===============================


def test_exportar_metricas_a_json_valido(tmp_path):
    """Test: Exportar métricas a JSON válido."""
    monitor = crear_monitor_metricas()

    # Registrar métricas
    registrar_request(monitor, fue_cache_hit=True, tiempo_ms=10.0)
    registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500.0)

    archivo_json = str(tmp_path / "metricas.json")
    exportar_metricas_json(monitor, archivo_json)

    # Verificar que se creó el archivo
    assert os.path.exists(archivo_json)

    # Verificar que es JSON válido
    with open(archivo_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    assert datos["total_requests"] == 2
    assert datos["cache_hits"] == 1
    assert datos["cache_misses"] == 1


def test_metricas_con_alta_carga_1000_requests():
    """Test: Métricas con alta carga (1000+ requests)."""
    monitor = crear_monitor_metricas()

    # Simular 1000 requests
    for i in range(1000):
        # 60% cache hits, 40% cache misses
        fue_hit = (i % 10) < 6
        tiempo = 5.0 if fue_hit else 500.0
        registrar_request(monitor, fue_cache_hit=fue_hit, tiempo_ms=tiempo)

    assert monitor["total_requests"] == 1000
    assert monitor["cache_hits"] == 600
    assert monitor["cache_misses"] == 400

    reporte = obtener_reporte_metricas(monitor)

    # Verificar que el reporte se genera sin errores
    assert len(reporte) > 0
    assert "1000" in reporte or "1,000" in reporte
