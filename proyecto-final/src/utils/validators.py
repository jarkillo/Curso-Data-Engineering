"""Funciones de validación de datos."""

from typing import Any

import pandas as pd


def validate_dataframe_not_empty(df: pd.DataFrame) -> dict[str, Any]:
    """
    Valida que un DataFrame no esté vacío.

    Args:
        df: DataFrame a validar.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"a": [1, 2]})
        >>> validate_dataframe_not_empty(df)
        {'valid': True, 'row_count': 2}
    """
    if df.empty or len(df) == 0:
        return {
            "valid": False,
            "error": "DataFrame is empty",
            "row_count": 0,
        }

    return {"valid": True, "row_count": len(df)}


def validate_required_columns(df: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    """
    Valida que un DataFrame tenga las columnas requeridas.

    Args:
        df: DataFrame a validar.
        columns: Lista de columnas requeridas.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"a": [1], "b": [2]})
        >>> validate_required_columns(df, ["a", "b"])
        {'valid': True}
    """
    actual_columns = set(df.columns)
    required_columns = set(columns)
    missing = required_columns - actual_columns

    if missing:
        return {
            "valid": False,
            "error": f"Missing columns: {missing}",
            "missing_columns": list(missing),
        }

    return {"valid": True}


def validate_no_nulls_in_columns(
    df: pd.DataFrame, columns: list[str]
) -> dict[str, Any]:
    """
    Valida que no haya valores nulos en columnas específicas.

    Args:
        df: DataFrame a validar.
        columns: Columnas que no deben tener nulos.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"a": [1, 2], "b": [3, None]})
        >>> validate_no_nulls_in_columns(df, ["a"])
        {'valid': True}
    """
    columns_with_nulls = {}

    for col in columns:
        if col in df.columns:
            null_count = df[col].isna().sum()
            if null_count > 0:
                columns_with_nulls[col] = int(null_count)

    if columns_with_nulls:
        return {
            "valid": False,
            "error": f"Found nulls in columns: {list(columns_with_nulls.keys())}",
            "columns_with_nulls": columns_with_nulls,
        }

    return {"valid": True}


def validate_numeric_range(
    df: pd.DataFrame,
    column: str,
    min_val: float | None = None,
    max_val: float | None = None,
) -> dict[str, Any]:
    """
    Valida que valores numéricos estén en un rango.

    Args:
        df: DataFrame a validar.
        column: Columna a verificar.
        min_val: Valor mínimo permitido.
        max_val: Valor máximo permitido.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"age": [25, 30, 35]})
        >>> validate_numeric_range(df, "age", min_val=20, max_val=40)
        {'valid': True, 'min': 25, 'max': 35}
    """
    if column not in df.columns:
        return {"valid": False, "error": f"Column '{column}' not found"}

    values = df[column]
    below_min = 0
    above_max = 0

    if min_val is not None:
        below_min = int((values < min_val).sum())

    if max_val is not None:
        above_max = int((values > max_val).sum())

    if below_min > 0 or above_max > 0:
        return {
            "valid": False,
            "error": f"Values out of range in column '{column}'",
            "below_min": below_min,
            "above_max": above_max,
            "min": float(values.min()),
            "max": float(values.max()),
        }

    return {
        "valid": True,
        "min": float(values.min()),
        "max": float(values.max()),
    }


def validate_date_range(
    df: pd.DataFrame,
    column: str,
    min_date: str | None = None,
    max_date: str | None = None,
) -> dict[str, Any]:
    """
    Valida que fechas estén en un rango.

    Args:
        df: DataFrame a validar.
        column: Columna de fecha a verificar.
        min_date: Fecha mínima permitida (YYYY-MM-DD).
        max_date: Fecha máxima permitida (YYYY-MM-DD).

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"date": pd.to_datetime(["2024-01-15"])})
        >>> validate_date_range(df, "date", "2024-01-01", "2024-02-01")
        {'valid': True}
    """
    if column not in df.columns:
        return {"valid": False, "error": f"Column '{column}' not found"}

    dates = pd.to_datetime(df[column])
    before_min = 0
    after_max = 0

    if min_date is not None:
        min_dt = pd.to_datetime(min_date)
        before_min = int((dates < min_dt).sum())

    if max_date is not None:
        max_dt = pd.to_datetime(max_date)
        after_max = int((dates > max_dt).sum())

    if before_min > 0 or after_max > 0:
        return {
            "valid": False,
            "error": f"Dates out of range in column '{column}'",
            "before_min": before_min,
            "after_max": after_max,
        }

    return {"valid": True}


def validate_unique_values(df: pd.DataFrame, column: str) -> dict[str, Any]:
    """
    Valida que una columna tenga valores únicos.

    Args:
        df: DataFrame a validar.
        column: Columna que debe tener valores únicos.

    Returns:
        Diccionario con resultado de validación.

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2, 3]})
        >>> validate_unique_values(df, "id")
        {'valid': True, 'unique_count': 3}
    """
    if column not in df.columns:
        return {"valid": False, "error": f"Column '{column}' not found"}

    duplicate_count = int(df[column].duplicated().sum())

    if duplicate_count > 0:
        return {
            "valid": False,
            "error": f"Found {duplicate_count} duplicate values in column '{column}'",
            "duplicate_count": duplicate_count,
            "unique_count": df[column].nunique(),
        }

    return {"valid": True, "unique_count": df[column].nunique()}


def run_all_validations(
    validations: list[tuple[str, dict[str, Any]]],
) -> dict[str, Any]:
    """
    Ejecuta múltiples validaciones y retorna resumen.

    Args:
        validations: Lista de tuplas (nombre_validacion, params).
            Validaciones disponibles:
            - "not_empty": {"df": DataFrame}
            - "required_columns": {"df": DataFrame, "columns": list}
            - "no_nulls": {"df": DataFrame, "columns": list}
            - "numeric_range": {"df": DataFrame, "column": str, ...}
            - "date_range": {"df": DataFrame, "column": str, ...}
            - "unique": {"df": DataFrame, "column": str}

    Returns:
        Diccionario con resumen de validaciones.

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
        >>> validations = [("not_empty", {"df": df})]
        >>> result = run_all_validations(validations)
        >>> result["all_passed"]
        True
    """
    validation_funcs = {
        "not_empty": lambda p: validate_dataframe_not_empty(p["df"]),
        "required_columns": lambda p: validate_required_columns(p["df"], p["columns"]),
        "no_nulls": lambda p: validate_no_nulls_in_columns(p["df"], p["columns"]),
        "numeric_range": lambda p: validate_numeric_range(
            p["df"], p["column"], p.get("min_val"), p.get("max_val")
        ),
        "date_range": lambda p: validate_date_range(
            p["df"], p["column"], p.get("min_date"), p.get("max_date")
        ),
        "unique": lambda p: validate_unique_values(p["df"], p["column"]),
    }

    results = {}
    passed = 0
    failed = 0

    for name, params in validations:
        if name in validation_funcs:
            result = validation_funcs[name](params)
            results[name] = result
            if result["valid"]:
                passed += 1
            else:
                failed += 1
        else:
            results[name] = {"valid": False, "error": f"Unknown validation: {name}"}
            failed += 1

    return {
        "all_passed": failed == 0,
        "passed_count": passed,
        "failed_count": failed,
        "total": passed + failed,
        "details": results,
    }
