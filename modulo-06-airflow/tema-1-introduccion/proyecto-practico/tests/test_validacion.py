"""
Tests para el módulo de validación de datos

Valida que los datos de ventas cumplan con las reglas de negocio.
"""

import pandas as pd
import pytest


def test_verificar_columnas_requeridas_correctas():
    """
    Test: verificar_columnas_requeridas debe pasar con columnas correctas

    Given: Un DataFrame con todas las columnas requeridas
    When: Se llama a verificar_columnas_requeridas
    Then: Retorna True
    """
    from src.validacion import verificar_columnas_requeridas

    df = pd.DataFrame(
        {
            "venta_id": [1, 2],
            "fecha": ["2025-10-25", "2025-10-25"],
            "cliente_id": ["C001", "C002"],
            "producto": ["Laptop", "Mouse"],
            "categoria": ["Computadoras", "Accesorios"],
            "cantidad": [1, 2],
            "precio_unitario": [599.99, 19.99],
            "total": [599.99, 39.98],
        }
    )

    resultado = verificar_columnas_requeridas(df)

    assert resultado is True


def test_verificar_columnas_requeridas_faltante():
    """
    Test: verificar_columnas_requeridas debe fallar si falta una columna

    Given: Un DataFrame sin la columna "total"
    When: Se llama a verificar_columnas_requeridas
    Then: Lanza ValueError con mensaje claro
    """
    from src.validacion import verificar_columnas_requeridas

    df = pd.DataFrame(
        {
            "venta_id": [1, 2],
            "fecha": ["2025-10-25", "2025-10-25"],
            "producto": ["Laptop", "Mouse"],
        }
    )

    with pytest.raises(ValueError, match="Falta.*columna"):
        verificar_columnas_requeridas(df)


def test_verificar_tipos_datos_correctos():
    """
    Test: verificar_tipos_datos debe validar tipos correctos

    Given: Un DataFrame con tipos de datos correctos
    When: Se llama a verificar_tipos_datos
    Then: Retorna True
    """
    from src.validacion import verificar_tipos_datos

    df = pd.DataFrame(
        {
            "venta_id": [1, 2],
            "fecha": ["2025-10-25", "2025-10-25"],
            "cliente_id": ["C001", "C002"],
            "producto": ["Laptop", "Mouse"],
            "categoria": ["Computadoras", "Accesorios"],
            "cantidad": [1, 2],
            "precio_unitario": [599.99, 19.99],
            "total": [599.99, 39.98],
        }
    )

    resultado = verificar_tipos_datos(df)

    assert resultado is True


def test_verificar_tipos_datos_cantidad_negativa():
    """
    Test: verificar_tipos_datos debe detectar cantidades negativas

    Given: Un DataFrame con cantidad negativa
    When: Se llama a verificar_tipos_datos
    Then: Lanza ValueError
    """
    from src.validacion import verificar_tipos_datos

    df = pd.DataFrame(
        {
            "venta_id": [1, 2],
            "fecha": ["2025-10-25", "2025-10-25"],
            "cliente_id": ["C001", "C002"],
            "producto": ["Laptop", "Mouse"],
            "categoria": ["Computadoras", "Accesorios"],
            "cantidad": [1, -2],  # Cantidad negativa inválida
            "precio_unitario": [599.99, 19.99],
            "total": [599.99, 39.98],
        }
    )

    with pytest.raises(ValueError, match="cantidad.*negativa"):
        verificar_tipos_datos(df)


def test_validar_datos_ventas_completo_correcto():
    """
    Test: validar_datos_ventas debe ejecutar todas las validaciones

    Given: Un DataFrame válido
    When: Se llama a validar_datos_ventas
    Then: Retorna dict con estado "valido" = True
    """
    from src.validacion import validar_datos_ventas

    df = pd.DataFrame(
        {
            "venta_id": [1, 2, 3],
            "fecha": ["2025-10-25", "2025-10-25", "2025-10-25"],
            "cliente_id": ["C001", "C002", "C003"],
            "producto": ["Laptop", "Mouse", "Teclado"],
            "categoria": ["Computadoras", "Accesorios", "Accesorios"],
            "cantidad": [1, 2, 1],
            "precio_unitario": [599.99, 19.99, 89.99],
            "total": [599.99, 39.98, 89.99],
        }
    )

    resultado = validar_datos_ventas(df)

    assert isinstance(resultado, dict)
    assert resultado["valido"] is True
    assert "errores" in resultado
    assert len(resultado["errores"]) == 0


def test_validar_datos_ventas_con_errores():
    """
    Test: validar_datos_ventas debe detectar múltiples errores

    Given: Un DataFrame con varios errores
    When: Se llama a validar_datos_ventas
    Then: Retorna dict con estado "valido" = False y lista de errores
    """
    from src.validacion import validar_datos_ventas

    df = pd.DataFrame(
        {
            "venta_id": [1],
            "fecha": ["2025-10-25"],
            "cantidad": [-1],  # Cantidad negativa
            "precio_unitario": [599.99],
            "total": [599.99],
            # Faltan columnas
        }
    )

    resultado = validar_datos_ventas(df)

    assert isinstance(resultado, dict)
    assert resultado["valido"] is False
    assert len(resultado["errores"]) > 0
