"""Extractor de datos desde archivos CSV."""

from pathlib import Path
from typing import Any

import pandas as pd


def validate_csv_schema(
    file_path: Path | str, required_columns: list[str]
) -> dict[str, Any]:
    """
    Valida que un CSV tenga las columnas requeridas.

    Args:
        file_path: Ruta al archivo CSV.
        required_columns: Lista de columnas que deben existir.

    Returns:
        Diccionario con resultado de validación:
        - valid: bool indicando si schema es válido
        - missing_columns: columnas faltantes (si inválido)
        - extra_columns: columnas adicionales encontradas

    Examples:
        >>> result = validate_csv_schema("products.csv", ["id", "name"])
        >>> result["valid"]
        True
    """
    file_path = Path(file_path)

    # Leer solo headers
    df = pd.read_csv(file_path, nrows=0)
    actual_columns = set(df.columns)
    required_set = set(required_columns)

    missing = required_set - actual_columns
    extra = actual_columns - required_set

    if missing:
        return {
            "valid": False,
            "missing_columns": list(missing),
            "extra_columns": list(extra),
        }

    return {"valid": True, "extra_columns": list(extra)}


def extract_products_from_csv(
    file_path: Path | str,
    encoding: str = "utf-8",
    category_filter: str | None = None,
) -> pd.DataFrame:
    """
    Extrae productos desde un archivo CSV.

    Args:
        file_path: Ruta al archivo CSV de productos.
        encoding: Encoding del archivo (default utf-8).
        category_filter: Filtrar por categoría específica (opcional).

    Returns:
        DataFrame con los productos extraídos.

    Raises:
        FileNotFoundError: Si el archivo no existe.

    Examples:
        >>> df = extract_products_from_csv("data/products.csv")
        >>> "product_id" in df.columns
        True
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    df = pd.read_csv(file_path, encoding=encoding)

    # Convertir tipos de datos
    if "price" in df.columns:
        df["price"] = df["price"].astype(float)
    if "stock" in df.columns:
        df["stock"] = df["stock"].astype(int)

    # Aplicar filtro de categoría si se especifica
    if category_filter and "category" in df.columns:
        df = df[df["category"] == category_filter]

    return df
