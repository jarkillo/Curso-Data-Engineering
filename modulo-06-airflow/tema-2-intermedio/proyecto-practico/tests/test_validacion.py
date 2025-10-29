"""
Tests para el módulo de validación.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import pandas as pd
import pytest


def test_validar_schema_ventas_con_columnas_correctas():
    """Test: validar_schema_ventas no lanza error con schema correcto"""
    from src.validacion import validar_schema_ventas

    df = pd.DataFrame(
        {
            "producto": ["Laptop"],
            "cantidad": [3],
            "precio": [1200.0],
            "cliente_id": ["C001"],
        }
    )

    # No debe lanzar excepción
    validar_schema_ventas(df)


def test_validar_schema_ventas_con_columnas_faltantes():
    """Test: validar_schema_ventas lanza ValueError si faltan columnas"""
    from src.validacion import validar_schema_ventas

    df = pd.DataFrame({"producto": ["Laptop"], "cantidad": [3]})

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        validar_schema_ventas(df)


def test_validar_datos_ventas_con_datos_validos():
    """Test: validar_datos_ventas no lanza error con datos válidos"""
    from src.validacion import validar_datos_ventas

    df = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse"],
            "cantidad": [3, 10],
            "precio": [1200.0, 25.5],
            "cliente_id": ["C001", "C002"],
        }
    )

    # No debe lanzar excepción
    validar_datos_ventas(df)


def test_validar_datos_ventas_con_valores_nulos():
    """Test: validar_datos_ventas lanza ValueError si hay valores nulos"""
    from src.validacion import validar_datos_ventas

    df = pd.DataFrame(
        {
            "producto": ["Laptop", None],
            "cantidad": [3, 10],
            "precio": [1200.0, 25.5],
            "cliente_id": ["C001", "C002"],
        }
    )

    with pytest.raises(ValueError, match="contiene valores nulos"):
        validar_datos_ventas(df)


def test_validar_datos_ventas_con_cantidad_negativa():
    """Test: validar_datos_ventas lanza ValueError si cantidad es negativa"""
    from src.validacion import validar_datos_ventas

    df = pd.DataFrame(
        {
            "producto": ["Laptop"],
            "cantidad": [-3],
            "precio": [1200.0],
            "cliente_id": ["C001"],
        }
    )

    with pytest.raises(ValueError, match="cantidad.*debe ser positivo"):
        validar_datos_ventas(df)


def test_validar_schema_clientes_con_columnas_correctas():
    """Test: validar_schema_clientes no lanza error con schema correcto"""
    from src.validacion import validar_schema_clientes

    df = pd.DataFrame(
        {
            "cliente_id": ["C001"],
            "nombre": ["Alice"],
            "nivel": ["premium"],
        }
    )

    # No debe lanzar excepción
    validar_schema_clientes(df)


def test_validar_schema_clientes_con_columnas_faltantes():
    """Test: validar_schema_clientes lanza ValueError si faltan columnas"""
    from src.validacion import validar_schema_clientes

    df = pd.DataFrame({"cliente_id": ["C001"], "nombre": ["Alice"]})

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        validar_schema_clientes(df)


def test_validar_datos_clientes_con_nivel_invalido():
    """Test: validar_datos_clientes lanza ValueError si el nivel no es válido"""
    from src.validacion import validar_datos_clientes

    df = pd.DataFrame(
        {
            "cliente_id": ["C001"],
            "nombre": ["Alice"],
            "nivel": ["invalido"],
        }
    )

    with pytest.raises(
        ValueError, match="nivel.*debe ser uno de: premium, normal, vip"
    ):
        validar_datos_clientes(df)
