"""
Tests para el módulo de transformación de datos

Calcula métricas de ventas: totales, promedios, top productos.
"""

import pandas as pd
import pytest


def test_calcular_ticket_promedio():
    """
    Test: calcular_ticket_promedio debe retornar el promedio correcto

    Given: Un DataFrame con ventas
    When: Se llama a calcular_ticket_promedio
    Then: Retorna el promedio de la columna "total"
    """
    from src.transformacion import calcular_ticket_promedio

    df = pd.DataFrame({"total": [100.0, 200.0, 300.0]})

    promedio = calcular_ticket_promedio(df)

    assert promedio == 200.0
    assert isinstance(promedio, float)


def test_calcular_ticket_promedio_dataframe_vacio():
    """
    Test: calcular_ticket_promedio debe fallar con DataFrame vacío

    Given: Un DataFrame vacío
    When: Se llama a calcular_ticket_promedio
    Then: Lanza ValueError
    """
    from src.transformacion import calcular_ticket_promedio

    df = pd.DataFrame({"total": []})

    with pytest.raises(ValueError, match="DataFrame está vacío"):
        calcular_ticket_promedio(df)


def test_obtener_top_productos():
    """
    Test: obtener_top_productos debe retornar los N productos más vendidos

    Given: Un DataFrame con ventas por producto
    When: Se llama a obtener_top_productos con n=2
    Then: Retorna lista de 2 productos con mayor cantidad vendida
    """
    from src.transformacion import obtener_top_productos

    df = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Cable"],
            "cantidad": [5, 50, 30, 10, 100],
        }
    )

    top = obtener_top_productos(df, n=2)

    assert isinstance(top, list)
    assert len(top) == 2
    assert top[0]["producto"] == "Cable"
    assert top[0]["cantidad"] == 100
    assert top[1]["producto"] == "Mouse"
    assert top[1]["cantidad"] == 50


def test_obtener_top_productos_n_mayor_que_filas():
    """
    Test: obtener_top_productos debe retornar todas las filas si n > cantidad

    Given: Un DataFrame con 3 productos
    When: Se llama a obtener_top_productos con n=10
    Then: Retorna solo los 3 productos disponibles
    """
    from src.transformacion import obtener_top_productos

    df = pd.DataFrame(
        {"producto": ["Laptop", "Mouse", "Teclado"], "cantidad": [5, 50, 30]}
    )

    top = obtener_top_productos(df, n=10)

    assert len(top) == 3


def test_calcular_metricas_ventas():
    """
    Test: calcular_metricas_ventas debe retornar dict con todas las métricas

    Given: Un DataFrame de ventas
    When: Se llama a calcular_metricas_ventas
    Then: Retorna dict con total, promedio, cantidad_ventas, top_productos
    """
    from src.transformacion import calcular_metricas_ventas

    df = pd.DataFrame(
        {
            "venta_id": [1, 2, 3],
            "producto": ["Laptop", "Mouse", "Teclado"],
            "cantidad": [1, 2, 1],
            "total": [600.0, 40.0, 90.0],
        }
    )

    metricas = calcular_metricas_ventas(df)

    assert isinstance(metricas, dict)
    assert "total_ventas" in metricas
    assert "ticket_promedio" in metricas
    assert "cantidad_ventas" in metricas
    assert "top_productos" in metricas

    assert metricas["total_ventas"] == 730.0
    assert metricas["ticket_promedio"] == pytest.approx(243.33, rel=0.01)
    assert metricas["cantidad_ventas"] == 3
    assert isinstance(metricas["top_productos"], list)


def test_calcular_metricas_ventas_dataframe_vacio():
    """
    Test: calcular_metricas_ventas debe fallar con DataFrame vacío

    Given: Un DataFrame vacío
    When: Se llama a calcular_metricas_ventas
    Then: Lanza ValueError
    """
    from src.transformacion import calcular_metricas_ventas

    df = pd.DataFrame()

    with pytest.raises(ValueError, match="DataFrame está vacío"):
        calcular_metricas_ventas(df)
