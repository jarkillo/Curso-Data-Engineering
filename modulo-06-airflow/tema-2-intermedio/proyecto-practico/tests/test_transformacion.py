"""
Tests para el módulo de transformación.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import pandas as pd


def test_calcular_total_ventas_con_datos_validos():
    """Test: calcular_total_ventas retorna la suma de cantidad * precio"""
    from src.transformacion import calcular_total_ventas

    df = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse", "Teclado"],
            "cantidad": [3, 10, 5],
            "precio": [1200.0, 25.5, 75.0],
            "cliente_id": ["C001", "C002", "C001"],
        }
    )

    total = calcular_total_ventas(df)

    # 3*1200 + 10*25.5 + 5*75 = 3600 + 255 + 375 = 4230
    assert total == 4230.0


def test_calcular_total_ventas_con_dataframe_vacio():
    """Test: calcular_total_ventas retorna 0 para DataFrame vacío"""
    from src.transformacion import calcular_total_ventas

    df = pd.DataFrame(columns=["producto", "cantidad", "precio", "cliente_id"])

    total = calcular_total_ventas(df)
    assert total == 0.0


def test_enriquecer_ventas_con_clientes():
    """Test: enriquecer_ventas_con_clientes hace merge correcto"""
    from src.transformacion import enriquecer_ventas_con_clientes

    df_ventas = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse"],
            "cantidad": [3, 10],
            "precio": [1200.0, 25.5],
            "cliente_id": ["C001", "C002"],
        }
    )

    df_clientes = pd.DataFrame(
        {
            "cliente_id": ["C001", "C002"],
            "nombre": ["Alice", "Bob"],
            "nivel": ["premium", "normal"],
        }
    )

    df_enriquecido = enriquecer_ventas_con_clientes(df_ventas, df_clientes)

    assert len(df_enriquecido) == 2
    assert "nombre" in df_enriquecido.columns
    assert "nivel" in df_enriquecido.columns
    assert df_enriquecido.iloc[0]["nombre"] == "Alice"
    assert df_enriquecido.iloc[1]["nivel"] == "normal"


def test_calcular_metricas_por_cliente():
    """Test: calcular_metricas_por_cliente agrupa correctamente por cliente"""
    from src.transformacion import calcular_metricas_por_cliente

    df = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse", "Teclado"],
            "cantidad": [3, 10, 5],
            "precio": [1200.0, 25.5, 75.0],
            "cliente_id": ["C001", "C002", "C001"],
            "nombre": ["Alice", "Bob", "Alice"],
            "nivel": ["premium", "normal", "premium"],
        }
    )

    df_metricas = calcular_metricas_por_cliente(df)

    assert len(df_metricas) == 2  # 2 clientes únicos
    assert "total_ventas" in df_metricas.columns
    assert "num_productos" in df_metricas.columns

    # Alice: 3*1200 + 5*75 = 3975
    # Bob: 10*25.5 = 255
    alice_row = df_metricas[df_metricas["cliente_id"] == "C001"].iloc[0]
    assert alice_row["total_ventas"] == 3975.0
    assert alice_row["num_productos"] == 2


def test_calcular_metricas_por_cliente_retorna_cliente_top():
    """Test: calcular_metricas_por_cliente identifica al cliente con más ventas"""
    from src.transformacion import calcular_metricas_por_cliente

    df = pd.DataFrame(
        {
            "producto": ["Laptop", "Mouse"],
            "cantidad": [3, 10],
            "precio": [1200.0, 25.5],
            "cliente_id": ["C001", "C002"],
            "nombre": ["Alice", "Bob"],
            "nivel": ["premium", "normal"],
        }
    )

    df_metricas = calcular_metricas_por_cliente(df)

    # Alice tiene 3600€, Bob tiene 255€
    # El cliente top debe ser C001 (Alice)
    cliente_top = df_metricas.sort_values("total_ventas", ascending=False).iloc[0]
    assert cliente_top["cliente_id"] == "C001"
