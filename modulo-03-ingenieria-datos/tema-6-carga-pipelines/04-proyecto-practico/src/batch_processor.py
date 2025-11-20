"""Módulo para procesamiento en lotes (batch processing)."""

from collections.abc import Iterator

import pandas as pd
from sqlalchemy import Engine


def dividir_en_lotes(df: pd.DataFrame, batch_size: int) -> Iterator[pd.DataFrame]:
    """
    Divide DataFrame en lotes.

    Args:
        df: DataFrame a dividir
        batch_size: Tamaño de cada lote

    Yields:
        Lotes del DataFrame

    Examples:
        >>> for lote in dividir_en_lotes(df, batch_size=1000):
        ...     print(len(lote))
    """
    total_rows = len(df)

    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        yield df.iloc[start:end]


def procesar_en_lotes(
    df: pd.DataFrame, engine: Engine, tabla: str, batch_size: int = 10000
) -> dict:
    """
    Procesa y carga DataFrame en lotes.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        batch_size: Tamaño de cada lote

    Returns:
        Dict con métricas: {"total_filas": int, "num_lotes": int, "duration_seconds": float}

    Examples:
        >>> resultado = procesar_en_lotes(df_grande, engine, "tabla", batch_size=1000)
        >>> print(f"Procesados {resultado['num_lotes']} lotes")
    """
    from datetime import datetime

    start_time = datetime.now()
    total_rows = len(df)
    num_lotes = 0

    for lote in dividir_en_lotes(df, batch_size):
        with engine.begin() as conn:
            lote.to_sql(tabla, conn, if_exists="append", index=False, method="multi")
        num_lotes += 1

    duration = (datetime.now() - start_time).total_seconds()

    return {
        "total_filas": total_rows,
        "num_lotes": num_lotes,
        "duration_seconds": round(duration, 2),
    }


def calcular_num_lotes(total_filas: int, batch_size: int) -> int:
    """
    Calcula el número de lotes necesarios.

    Args:
        total_filas: Número total de filas
        batch_size: Tamaño del lote

    Returns:
        Número de lotes

    Examples:
        >>> calcular_num_lotes(1000, 100)
        10
    """
    return (total_filas + batch_size - 1) // batch_size
