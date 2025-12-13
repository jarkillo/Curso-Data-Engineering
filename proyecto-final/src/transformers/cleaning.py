"""Funciones de limpieza de datos."""

import pandas as pd


def remove_duplicates(
    df: pd.DataFrame,
    subset: list[str] | None = None,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Elimina filas duplicadas de un DataFrame.

    Args:
        df: DataFrame con posibles duplicados.
        subset: Columnas a considerar para detectar duplicados.
        keep: Qué ocurrencia mantener ('first', 'last', False).

    Returns:
        DataFrame sin duplicados.

    Examples:
        >>> df = pd.DataFrame({"id": [1, 1, 2], "val": ["a", "a", "b"]})
        >>> remove_duplicates(df, subset=["id"])
           id val
        0   1   a
        2   2   b
    """
    return df.drop_duplicates(subset=subset, keep=keep).reset_index(drop=True)


def handle_missing_values(
    df: pd.DataFrame,
    numeric_fill: float | int = 0,
    string_fill: str = "Unknown",
    drop_if_null: list[str] | None = None,
) -> pd.DataFrame:
    """
    Maneja valores faltantes en un DataFrame.

    Args:
        df: DataFrame con valores faltantes.
        numeric_fill: Valor para rellenar columnas numéricas.
        string_fill: Valor para rellenar columnas de texto.
        drop_if_null: Columnas que si son null, eliminar la fila.

    Returns:
        DataFrame con valores faltantes tratados.

    Examples:
        >>> df = pd.DataFrame({"num": [1, None], "str": ["a", None]})
        >>> handle_missing_values(df, numeric_fill=0, string_fill="N/A")
           num  str
        0  1.0    a
        1  0.0  N/A
    """
    df = df.copy()

    # Primero eliminar filas si se especifica
    if drop_if_null:
        df = df.dropna(subset=drop_if_null)

    # Rellenar columnas numéricas
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(numeric_fill)

    # Rellenar columnas de texto
    string_cols = df.select_dtypes(include=["object", "string"]).columns
    df[string_cols] = df[string_cols].fillna(string_fill)

    return df.reset_index(drop=True)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia DataFrame de pedidos.

    Operaciones:
    - Elimina filas sin order_id
    - Elimina duplicados por order_id
    - Elimina pedidos con quantity <= 0

    Args:
        df: DataFrame de pedidos sin limpiar.

    Returns:
        DataFrame de pedidos limpio.

    Examples:
        >>> df = pd.DataFrame({"order_id": ["1", None], "quantity": [2, 1]})
        >>> clean_orders(df)
          order_id  quantity
        0        1         2
    """
    df = df.copy()

    # Eliminar filas sin order_id
    df = df.dropna(subset=["order_id"])

    # Eliminar duplicados
    df = remove_duplicates(df, subset=["order_id"], keep="first")

    # Eliminar cantidades inválidas
    df = df[df["quantity"] > 0]

    return df.reset_index(drop=True)


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia DataFrame de productos.

    Operaciones:
    - Elimina productos sin nombre
    - Corrige stock negativo a 0

    Args:
        df: DataFrame de productos sin limpiar.

    Returns:
        DataFrame de productos limpio.

    Examples:
        >>> df = pd.DataFrame({"product_id": ["1"], "name": ["Test"], "stock": [-5]})
        >>> clean_products(df)
          product_id  name  stock
        0          1  Test      0
    """
    df = df.copy()

    # Eliminar productos sin nombre
    df = df.dropna(subset=["name"])

    # Corregir stock negativo
    if "stock" in df.columns:
        df["stock"] = df["stock"].clip(lower=0)

    return df.reset_index(drop=True)


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia DataFrame de clientes.

    Operaciones:
    - Elimina duplicados por customer_id
    - Elimina espacios en blanco de strings
    - Normaliza emails a minúsculas
    - Rellena regiones faltantes con 'Unknown'

    Args:
        df: DataFrame de clientes sin limpiar.

    Returns:
        DataFrame de clientes limpio.

    Examples:
        >>> df = pd.DataFrame({
        ...     "customer_id": ["1"],
        ...     "name": ["  Test  "],
        ...     "email": ["TEST@EMAIL.COM"],
        ...     "region": [None]
        ... })
        >>> clean_customers(df)
          customer_id  name           email   region
        0           1  Test  test@email.com  Unknown
    """
    df = df.copy()

    # Eliminar duplicados
    df = remove_duplicates(df, subset=["customer_id"], keep="first")

    # Eliminar espacios en blanco
    string_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].str.strip()

    # Normalizar emails
    if "email" in df.columns:
        df["email"] = df["email"].str.lower()

    # Rellenar región faltante
    if "region" in df.columns:
        df["region"] = df["region"].fillna("Unknown")

    return df.reset_index(drop=True)
