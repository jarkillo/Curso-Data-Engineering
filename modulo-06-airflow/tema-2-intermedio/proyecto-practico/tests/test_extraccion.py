"""
Tests para el módulo de extracción.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest


def test_extraer_ventas_csv_con_datos_validos():
    """Test: extraer_ventas_csv lee correctamente un CSV válido"""
    from src.extraccion import extraer_ventas_csv

    # Crear CSV temporal
    contenido_csv = """producto,cantidad,precio,cliente_id
Laptop,3,1200.00,C001
Mouse,10,25.50,C002"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        tmp.write(contenido_csv)
        ruta_tmp = tmp.name

    try:
        df = extraer_ventas_csv(ruta_tmp)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["producto", "cantidad", "precio", "cliente_id"]
        assert df.iloc[0]["producto"] == "Laptop"
        assert df.iloc[0]["cantidad"] == 3
        assert df.iloc[0]["precio"] == 1200.00
    finally:
        Path(ruta_tmp).unlink()


def test_extraer_ventas_csv_archivo_inexistente():
    """Test: extraer_ventas_csv lanza FileNotFoundError si el archivo no existe"""
    from src.extraccion import extraer_ventas_csv

    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        extraer_ventas_csv("/ruta/inexistente.csv")


def test_extraer_clientes_json_con_datos_validos():
    """Test: extraer_clientes_json lee correctamente un JSON válido"""
    from src.extraccion import extraer_clientes_json

    # Crear JSON temporal
    datos = [
        {"cliente_id": "C001", "nombre": "Alice", "nivel": "premium"},
        {"cliente_id": "C002", "nombre": "Bob", "nivel": "normal"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    try:
        df = extraer_clientes_json(ruta_tmp)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["cliente_id", "nombre", "nivel"]
        assert df.iloc[0]["nombre"] == "Alice"
        assert df.iloc[1]["nivel"] == "normal"
    finally:
        Path(ruta_tmp).unlink()


def test_extraer_clientes_json_archivo_inexistente():
    """Test: extraer_clientes_json lanza FileNotFoundError si el archivo no existe"""
    from src.extraccion import extraer_clientes_json

    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        extraer_clientes_json("/ruta/inexistente.json")


def test_contar_registros_extraidos():
    """Test: contar_registros_extraidos retorna la cantidad correcta de filas"""
    from src.extraccion import contar_registros_extraidos

    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})

    count = contar_registros_extraidos(df)
    assert count == 3


def test_contar_registros_extraidos_dataframe_vacio():
    """Test: contar_registros_extraidos retorna 0 para DataFrame vacío"""
    from src.extraccion import contar_registros_extraidos

    df = pd.DataFrame(columns=["col1", "col2"])

    count = contar_registros_extraidos(df)
    assert count == 0
