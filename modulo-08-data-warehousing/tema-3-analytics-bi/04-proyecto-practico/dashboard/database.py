"""
Conexión al Data Warehouse para el dashboard de Analytics.

Este módulo provee la conexión a la base de datos SQLite del Data Warehouse
creado en el Tema 1 (Modelado Dimensional).
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

# Ruta al Data Warehouse del Tema 1
DWH_PATH = (
    Path(__file__).parent.parent.parent
    / "tema-1-dimensional-modeling"
    / "04-proyecto-practico"
    / "output"
    / "data_warehouse.db"
)


@contextmanager
def get_connection():
    """
    Context manager para obtener conexión a la base de datos.

    Yields:
        sqlite3.Connection: Conexión a la base de datos

    Examples:
        >>> with get_connection() as conn:
        ...     df = pd.read_sql("SELECT * FROM DimProducto", conn)
    """
    conn = sqlite3.connect(DWH_PATH)
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """
    Ejecuta una query SQL y retorna un DataFrame.

    Args:
        query: Query SQL a ejecutar
        params: Parámetros para la query (opcional)

    Returns:
        DataFrame con los resultados

    Examples:
        >>> df = execute_query("SELECT * FROM DimProducto LIMIT 5")
        >>> df = execute_query("SELECT * FROM DimFecha WHERE anio = ?", (2024,))
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn, params=params)


def check_dwh_exists() -> bool:
    """
    Verifica si el archivo del Data Warehouse existe.

    Returns:
        True si el archivo existe, False en caso contrario
    """
    return DWH_PATH.exists()


def get_dwh_info() -> dict:
    """
    Obtiene información básica sobre el Data Warehouse.

    Returns:
        Diccionario con información del DWH:
            - exists: bool
            - path: str
            - size_mb: float (si existe)
            - tables: list[str] (si existe)
    """
    info = {
        "exists": check_dwh_exists(),
        "path": str(DWH_PATH),
    }

    if info["exists"]:
        info["size_mb"] = DWH_PATH.stat().st_size / (1024 * 1024)

        # Obtener lista de tablas
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        df = execute_query(query)
        info["tables"] = df["name"].tolist()

    return info
