"""
Fixtures compartidas para tests del conversor multi-formato.
"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def df_ejemplo():
    """Crea un DataFrame de ejemplo para tests."""
    np.random.seed(42)

    return pd.DataFrame(
        {
            "id": range(1, 101),
            "nombre": [f"Usuario_{i}" for i in range(100)],
            "edad": np.random.randint(18, 80, 100),
            "salario": np.round(np.random.uniform(20000, 100000, 100), 2),
            "activo": np.random.choice([True, False], 100),
            "fecha": pd.date_range("2024-01-01", periods=100, freq="D"),
        }
    )


@pytest.fixture
def df_vacio():
    """Crea un DataFrame vacío."""
    return pd.DataFrame()


@pytest.fixture
def directorio_temporal(tmp_path):
    """
    Crea un directorio temporal para tests.

    El directorio se limpia automáticamente al finalizar el test.
    """
    return tmp_path


@pytest.fixture
def archivo_csv_temporal(df_ejemplo, directorio_temporal):
    """Crea un archivo CSV temporal con datos de ejemplo."""
    ruta_csv = directorio_temporal / "datos.csv"
    df_ejemplo.to_csv(ruta_csv, index=False)
    return str(ruta_csv)


@pytest.fixture
def archivo_json_temporal(df_ejemplo, directorio_temporal):
    """Crea un archivo JSON temporal con datos de ejemplo."""
    ruta_json = directorio_temporal / "datos.json"
    df_ejemplo.to_json(ruta_json, orient="records", date_format="iso")
    return str(ruta_json)


@pytest.fixture
def archivo_jsonl_temporal(df_ejemplo, directorio_temporal):
    """Crea un archivo JSON Lines temporal con datos de ejemplo."""
    ruta_jsonl = directorio_temporal / "datos.jsonl"
    df_ejemplo.to_json(ruta_jsonl, orient="records", lines=True, date_format="iso")
    return str(ruta_jsonl)


@pytest.fixture
def archivo_parquet_temporal(df_ejemplo, directorio_temporal):
    """Crea un archivo Parquet temporal con datos de ejemplo."""
    ruta_parquet = directorio_temporal / "datos.parquet"
    df_ejemplo.to_parquet(ruta_parquet, index=False)
    return str(ruta_parquet)


@pytest.fixture
def df_con_particiones():
    """Crea un DataFrame con columnas para particionar."""
    np.random.seed(42)

    df = pd.DataFrame(
        {
            "id": range(1, 201),
            "fecha": pd.date_range("2023-01-01", periods=200, freq="D"),
            "producto": np.random.choice(["A", "B", "C"], 200),
            "monto": np.round(np.random.uniform(10, 1000, 200), 2),
        }
    )

    # Añadir columnas de partición
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month

    return df


@pytest.fixture
def df_json_nested():
    """Crea datos con estructura nested para tests."""
    return [
        {
            "pedido_id": 1,
            "cliente": {"nombre": "Juan", "email": "juan@email.com"},
            "items": [
                {"producto": "Laptop", "cantidad": 1, "precio": 899.99},
                {"producto": "Mouse", "cantidad": 2, "precio": 24.99},
            ],
        },
        {
            "pedido_id": 2,
            "cliente": {"nombre": "María", "email": "maria@email.com"},
            "items": [{"producto": "Teclado", "cantidad": 1, "precio": 79.99}],
        },
    ]
