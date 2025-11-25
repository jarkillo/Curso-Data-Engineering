"""Fixtures compartidas para tests del Framework de Calidad de Datos."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def df_basico() -> pd.DataFrame:
    """Proporciona un DataFrame básico para tests simples."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "nombre": ["Ana", "Luis", "Pedro", "María", "Juan"],
            "edad": [25, 30, 35, 28, 40],
            "salario": [3000.0, 3500.0, 3200.0, 4000.0, 3800.0],
            "activo": [True, False, True, True, False],
        }
    )


@pytest.fixture
def df_con_nulos() -> pd.DataFrame:
    """Proporciona un DataFrame con valores nulos para testing."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "nombre": ["Ana", "Luis", None, "María", "Juan"],
            "email": [
                "ana@email.com",
                None,
                "pedro@email.com",
                "maria@email.com",
                None,
            ],
            "telefono": ["611111111", "622222222", None, None, "655555555"],
        }
    )


@pytest.fixture
def df_con_duplicados() -> pd.DataFrame:
    """Proporciona un DataFrame con duplicados exactos para testing."""
    return pd.DataFrame(
        {
            "id": [1, 2, 2, 3, 4, 4, 5],
            "nombre": ["Ana", "Luis", "Luis", "Pedro", "María", "María", "Juan"],
            "email": [
                "ana@email.com",
                "luis@email.com",
                "luis@email.com",
                "pedro@email.com",
                "maria@email.com",
                "maria@email.com",
                "juan@email.com",
            ],
        }
    )


@pytest.fixture
def df_con_outliers() -> pd.DataFrame:
    """Proporciona un DataFrame con outliers conocidos para testing."""
    np.random.seed(42)
    valores_normales = np.random.normal(100, 10, 95)
    outliers = [-50, 500, 1000, 2000, -100]

    return pd.DataFrame(
        {"id": range(1, 101), "valor": np.concatenate([valores_normales, outliers])}
    )


@pytest.fixture
def df_ventas() -> pd.DataFrame:
    """Proporciona un DataFrame de ventas para tests de validación."""
    return pd.DataFrame(
        {
            "venta_id": [1, 2, 3, 4, 5],
            "producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Cable"],
            "cantidad": [1, 5, 2, 1, 10],
            "precio_unitario": [850.50, 25.99, 89.99, 320.00, 12.50],
            "descuento": [0.1, 0.0, 0.15, 0.05, 0.2],
            "fecha": [
                "2024-10-20",
                "2024-10-21",
                "2024-10-22",
                "2024-10-23",
                "2024-10-24",
            ],
        }
    )


@pytest.fixture
def df_vacio() -> pd.DataFrame:
    """Proporciona un DataFrame vacío para tests de edge cases."""
    return pd.DataFrame()


@pytest.fixture
def esquema_basico() -> dict[str, str]:
    """Esquema de tipos básico."""
    return {
        "id": "int",
        "nombre": "str",
        "edad": "int",
        "salario": "float",
        "activo": "bool",
    }


@pytest.fixture
def rangos_validos() -> dict[str, tuple]:
    """Rangos válidos para validación numérica."""
    return {
        "edad": (18, 70),
        "salario": (1000, 10000),
        "cantidad": (1, 100),
        "descuento": (0, 1),
    }


@pytest.fixture
def valores_permitidos() -> dict[str, list]:
    """Valores permitidos para validación categórica."""
    return {
        "categoria": ["A", "B", "C"],
        "estado": ["Activo", "Inactivo", "Suspendido"],
        "region": ["Norte", "Sur", "Este", "Oeste"],
    }


@pytest.fixture
def df_nombres_similares() -> pd.DataFrame:
    """Proporciona un DataFrame con nombres similares para fuzzy matching."""
    return pd.DataFrame(
        {
            "id": range(1, 9),
            "nombre": [
                "Juan Pérez García",
                "Juan Perez Garcia",
                "María López Martínez",
                "Maria Lopez Martinez",
                "Pedro Sánchez",
                "Pedro Sanchez",
                "Ana García",
                "Carlos Martín",
            ],
            "email": [
                "juan.perez@email.com",
                "juan.perez@email.com",
                "maria.lopez@email.com",
                "mlopez@email.com",
                "pedro.sanchez@email.com",
                "p.sanchez@email.com",
                "ana.garcia@email.com",
                "carlos.martin@email.com",
            ],
        }
    )


@pytest.fixture
def df_multivariado() -> pd.DataFrame:
    """Proporciona un DataFrame para tests de outliers multivariados."""
    np.random.seed(42)
    n = 100

    return pd.DataFrame(
        {
            "id": range(1, n + 1),
            "precio": np.concatenate(
                [np.random.normal(100, 20, 95), [500, 600, -10, 1000, 800]]  # Outliers
            ),
            "cantidad": np.concatenate(
                [np.random.normal(50, 10, 95), [200, 250, 0, 300, 280]]  # Outliers
            ),
            "descuento": np.random.uniform(0, 0.3, n),
        }
    )


@pytest.fixture
def configuracion_completa() -> dict:
    """Configuración completa para validación de esquema."""
    return {
        "tipos": {"id": "int", "nombre": "str", "edad": "int", "salario": "float"},
        "rangos": {"edad": (18, 70), "salario": (1000, 10000)},
        "columnas_requeridas": ["id", "nombre"],
        "valores_unicos": ["id"],
        "valores_permitidos": {"categoria": ["A", "B", "C"]},
    }
