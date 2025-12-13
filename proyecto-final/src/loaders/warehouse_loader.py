"""Funciones de carga al data warehouse."""

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def create_dim_date(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Crea dimensión de fechas.

    Args:
        start_date: Fecha inicio (YYYY-MM-DD).
        end_date: Fecha fin (YYYY-MM-DD).

    Returns:
        DataFrame con dimensión de fechas.

    Examples:
        >>> df = create_dim_date("2024-01-01", "2024-01-03")
        >>> len(df)
        3
    """
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({"date": dates})

    # Extraer componentes
    df["date_id"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["quarter"] = df["date"].dt.quarter
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_name"] = df["date"].dt.day_name()
    df["month_name"] = df["date"].dt.month_name()
    df["is_weekend"] = df["day_of_week"].isin([5, 6])
    df["week_of_year"] = df["date"].dt.isocalendar().week

    return df


def validate_dimension_schema(
    df: pd.DataFrame,
    key_column: str,
    name: str,
) -> dict[str, Any]:
    """
    Valida schema de una dimensión.

    Args:
        df: DataFrame de la dimensión.
        key_column: Nombre de la columna clave.
        name: Nombre de la dimensión.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
        >>> validate_dimension_schema(df, "id", "dim_test")
        {'valid': True}
    """
    # Verificar que existe la columna clave
    if key_column not in df.columns:
        return {
            "valid": False,
            "error": f"Key column '{key_column}' not found in {name}",
        }

    # Verificar que no hay claves nulas
    if df[key_column].isna().any():
        null_count = df[key_column].isna().sum()
        return {
            "valid": False,
            "error": f"Found {null_count} null values in key column '{key_column}'",
        }

    # Verificar que no hay claves duplicadas
    if df[key_column].duplicated().any():
        dup_count = df[key_column].duplicated().sum()
        return {
            "valid": False,
            "error": f"Found {dup_count} duplicate keys in column '{key_column}'",
        }

    return {"valid": True}


def validate_fact_schema(
    df: pd.DataFrame,
    foreign_keys: list[str],
    measures: list[str],
    name: str,
) -> dict[str, Any]:
    """
    Valida schema de una tabla de hechos.

    Args:
        df: DataFrame de la tabla de hechos.
        foreign_keys: Lista de columnas de foreign keys.
        measures: Lista de columnas de medidas.
        name: Nombre de la tabla de hechos.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"fk1": [1], "measure1": [10.0]})
        >>> validate_fact_schema(df, ["fk1"], ["measure1"], "fact_test")
        {'valid': True}
    """
    # Verificar foreign keys
    for fk in foreign_keys:
        if fk not in df.columns:
            return {
                "valid": False,
                "error": f"Foreign key column '{fk}' not found in {name}",
            }

    # Verificar medidas
    for measure in measures:
        if measure not in df.columns:
            return {
                "valid": False,
                "error": f"Measure column '{measure}' not found in {name}",
            }
        # Verificar que las medidas son numéricas
        if not pd.api.types.is_numeric_dtype(df[measure]):
            return {
                "valid": False,
                "error": f"Measure column '{measure}' must be numeric in {name}",
            }

    return {"valid": True}


def load_dimension(
    df: pd.DataFrame,
    output_path: str,
    key_column: str,
    dimension_name: str,
) -> dict[str, Any]:
    """
    Carga una dimensión al data warehouse.

    Args:
        df: DataFrame de la dimensión.
        output_path: Ruta de salida (parquet).
        key_column: Columna clave de la dimensión.
        dimension_name: Nombre de la dimensión.

    Returns:
        Diccionario con resultado de la carga.

    Examples:
        >>> df = pd.DataFrame({"id": [1], "name": ["test"]})
        >>> result = load_dimension(df, "/tmp/dim.parquet", "id", "dim_test")
        >>> result["status"]
        'success'
    """
    # Validar schema
    validation = validate_dimension_schema(df, key_column, dimension_name)
    if not validation["valid"]:
        return {
            "status": "error",
            "dimension": dimension_name,
            "error": validation["error"],
            "rows_loaded": 0,
        }

    # Guardar como parquet
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    return {
        "status": "success",
        "dimension": dimension_name,
        "rows_loaded": len(df),
        "output_path": str(output_path),
        "loaded_at": datetime.now().isoformat(),
    }


def load_fact_table(
    df: pd.DataFrame,
    output_path: str,
    foreign_keys: list[str],
    measures: list[str],
    fact_name: str,
) -> dict[str, Any]:
    """
    Carga una tabla de hechos al data warehouse.

    Args:
        df: DataFrame de la tabla de hechos.
        output_path: Ruta de salida (parquet).
        foreign_keys: Columnas de foreign keys.
        measures: Columnas de medidas.
        fact_name: Nombre de la tabla de hechos.

    Returns:
        Diccionario con resultado de la carga.

    Examples:
        >>> df = pd.DataFrame({"fk": [1], "amount": [100.0]})
        >>> result = load_fact_table(
        ...     df, "/tmp/fact.parquet", ["fk"], ["amount"], "fact_test"
        ... )
        >>> result["status"]
        'success'
    """
    # Validar schema
    validation = validate_fact_schema(df, foreign_keys, measures, fact_name)
    if not validation["valid"]:
        return {
            "status": "error",
            "fact_table": fact_name,
            "error": validation["error"],
            "rows_loaded": 0,
        }

    # Calcular métricas
    metrics = {}
    for measure in measures:
        metrics[f"total_{measure}"] = float(df[measure].sum())
        metrics[f"avg_{measure}"] = float(df[measure].mean())

    # Guardar como parquet
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    return {
        "status": "success",
        "fact_table": fact_name,
        "rows_loaded": len(df),
        "output_path": str(output_path),
        "metrics": metrics,
        "loaded_at": datetime.now().isoformat(),
    }


def upsert_records(
    new_df: pd.DataFrame,
    existing_path: str,
    key_column: str,
) -> dict[str, Any]:
    """
    Inserta o actualiza registros en una tabla existente.

    Args:
        new_df: DataFrame con registros nuevos o actualizados.
        existing_path: Ruta al archivo parquet existente.
        key_column: Columna clave para identificar registros.

    Returns:
        Diccionario con estadísticas del upsert.

    Examples:
        >>> # Asumiendo un archivo existente
        >>> new_df = pd.DataFrame({"id": [1], "name": ["updated"]})
        >>> result = upsert_records(new_df, "/tmp/existing.parquet", "id")
        >>> "inserted" in result
        True
    """
    existing_path = Path(existing_path)

    if not existing_path.exists():
        return {
            "status": "error",
            "error": f"File not found: {existing_path}",
            "inserted": 0,
            "updated": 0,
        }

    # Leer datos existentes
    existing_df = pd.read_parquet(existing_path)

    # Identificar registros nuevos vs existentes
    existing_keys = set(existing_df[key_column])
    new_keys = set(new_df[key_column])

    keys_to_insert = new_keys - existing_keys
    keys_to_update = new_keys & existing_keys

    inserted_count = len(keys_to_insert)
    updated_count = len(keys_to_update)

    # Eliminar registros a actualizar del DataFrame existente
    if keys_to_update:
        existing_df = existing_df[~existing_df[key_column].isin(keys_to_update)]

    # Combinar con nuevos registros
    result_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Guardar resultado
    result_df.to_parquet(existing_path, index=False)

    return {
        "status": "success",
        "inserted": inserted_count,
        "updated": updated_count,
        "total_records": len(result_df),
    }
