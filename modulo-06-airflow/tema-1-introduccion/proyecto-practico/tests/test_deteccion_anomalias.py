"""
Tests para el módulo de detección de anomalías

Detecta caídas significativas en las ventas.
"""

import pytest


def test_detectar_caida_ventas_sin_anomalia():
    """
    Test: detectar_caida_ventas no debe detectar anomalía si ventas normales

    Given: Ventas actuales similares al promedio histórico
    When: Se llama a detectar_caida_ventas
    Then: Retorna dict con anomalia=False
    """
    from src.deteccion_anomalias import detectar_caida_ventas

    total_actual = 1000.0
    total_historico = 1050.0
    umbral = 0.3  # 30% de caída

    resultado = detectar_caida_ventas(total_actual, total_historico, umbral)

    assert isinstance(resultado, dict)
    assert resultado["anomalia"] is False
    assert "porcentaje_caida" in resultado


def test_detectar_caida_ventas_con_anomalia():
    """
    Test: detectar_caida_ventas debe detectar caída > umbral

    Given: Ventas actuales 40% menores que promedio histórico
    When: Se llama a detectar_caida_ventas con umbral=0.3
    Then: Retorna dict con anomalia=True
    """
    from src.deteccion_anomalias import detectar_caida_ventas

    total_actual = 600.0
    total_historico = 1000.0
    umbral = 0.3  # 30% de caída

    resultado = detectar_caida_ventas(total_actual, total_historico, umbral)

    assert resultado["anomalia"] is True
    assert resultado["porcentaje_caida"] == pytest.approx(0.4, rel=0.01)
    assert "mensaje" in resultado


def test_detectar_caida_ventas_exactamente_en_umbral():
    """
    Test: detectar_caida_ventas en el límite del umbral

    Given: Ventas actuales exactamente 30% menores (umbral=0.3)
    When: Se llama a detectar_caida_ventas
    Then: Retorna anomalia=False (<=umbral no es anomalía)
    """
    from src.deteccion_anomalias import detectar_caida_ventas

    total_actual = 700.0
    total_historico = 1000.0
    umbral = 0.3

    resultado = detectar_caida_ventas(total_actual, total_historico, umbral)

    # Justo en el umbral no debe ser anomalía
    assert resultado["anomalia"] is False


def test_detectar_caida_ventas_total_historico_cero():
    """
    Test: detectar_caida_ventas debe manejar total_historico=0

    Given: Total histórico es cero (sin datos previos)
    When: Se llama a detectar_caida_ventas
    Then: Lanza ValueError
    """
    from src.deteccion_anomalias import detectar_caida_ventas

    total_actual = 1000.0
    total_historico = 0.0
    umbral = 0.3

    with pytest.raises(ValueError, match="total histórico no puede ser cero"):
        detectar_caida_ventas(total_actual, total_historico, umbral)


def test_calcular_promedio_historico():
    """
    Test: calcular_promedio_historico debe calcular promedio de archivos CSVs

    Given: Una lista de fechas con CSVs de ventas
    When: Se llama a calcular_promedio_historico
    Then: Retorna el promedio de ventas totales
    """
    from src.deteccion_anomalias import calcular_promedio_historico

    fechas = ["2025-10-20", "2025-10-21", "2025-10-22"]

    # Esta función leerá los CSVs y calculará promedio
    # Por ahora, solo verificamos que retorna un float positivo
    promedio = calcular_promedio_historico(fechas)

    assert isinstance(promedio, float)
    assert promedio >= 0


def test_calcular_promedio_historico_lista_vacia():
    """
    Test: calcular_promedio_historico debe fallar con lista vacía

    Given: Una lista vacía de fechas
    When: Se llama a calcular_promedio_historico
    Then: Lanza ValueError
    """
    from src.deteccion_anomalias import calcular_promedio_historico

    fechas = []

    with pytest.raises(ValueError, match="lista de fechas no puede estar vacía"):
        calcular_promedio_historico(fechas)
