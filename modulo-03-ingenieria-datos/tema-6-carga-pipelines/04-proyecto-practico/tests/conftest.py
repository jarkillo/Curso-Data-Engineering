"""
Fixtures compartidos para tests.

Siguiendo metodología TDD.
"""

import tempfile
from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import create_engine


@pytest.fixture
def df_simple():
    """DataFrame simple para tests básicos."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "nombre": ["Ana", "Luis", "María", "Carlos", "Sofia"],
            "valor": [100, 200, 150, 300, 250],
        }
    )


@pytest.fixture
def df_con_fecha():
    """DataFrame con columna de fecha para carga incremental."""
    return pd.DataFrame(
        {
            "id": range(1, 11),
            "timestamp": pd.date_range("2024-01-15", periods=10, freq="h"),
            "valor": range(100, 200, 10),
        }
    )


@pytest.fixture
def engine_temporal():
    """Engine de SQLite en memoria para tests."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def directorio_temporal():
    """Directorio temporal para tests de archivos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def archivo_checkpoint_temporal(directorio_temporal):
    """Archivo de checkpoint temporal."""
    checkpoint_file = directorio_temporal / "checkpoint.txt"
    yield str(checkpoint_file)


@pytest.fixture
def df_con_duplicados():
    """DataFrame con registros duplicados para tests de upsert."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 2, 4],  # ID 2 duplicado
            "nombre": ["Ana", "Luis", "María", "Luis Updated", "Carlos"],
            "valor": [100, 200, 150, 220, 300],
        }
    )


@pytest.fixture
def df_grande():
    """DataFrame grande para tests de batch processing."""
    return pd.DataFrame(
        {
            "id": range(1, 10001),  # 10K registros
            "valor_a": range(10000),
            "valor_b": range(10000, 20000),
        }
    )


@pytest.fixture
def df_invalido():
    """DataFrame con datos inválidos para tests de validación."""
    return pd.DataFrame(
        {
            "id": [1, 2, None, 4, 5],  # ID nulo
            "valor": [100, -50, 150, 200, None],  # Valor negativo y nulo
        }
    )


@pytest.fixture
def df_particionable():
    """DataFrame con múltiples fechas para particionamiento."""
    return pd.DataFrame(
        {
            "id": range(1, 31),
            "fecha": pd.to_datetime(
                ["2024-01-15"] * 10 + ["2024-01-16"] * 10 + ["2024-01-17"] * 10
            ),
            "valor": range(100, 130),
        }
    )
