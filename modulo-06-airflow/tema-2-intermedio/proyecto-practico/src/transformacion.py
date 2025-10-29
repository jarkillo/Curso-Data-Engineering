"""
Módulo de transformación de datos.

Este módulo proporciona funciones para calcular métricas, enriquecer datos
y realizar agregaciones sobre ventas y clientes.
"""

import pandas as pd


def calcular_total_ventas(df: pd.DataFrame) -> float:
    """
    Calcula el total de ventas (cantidad * precio).

    Args:
        df: DataFrame de ventas con columnas cantidad y precio

    Returns:
        Total de ventas (suma de cantidad * precio)

    Examples:
        >>> df = pd.DataFrame({
        ...     'producto': ['Laptop', 'Mouse'],
        ...     'cantidad': [3, 10],
        ...     'precio': [1200.0, 25.5],
        ...     'cliente_id': ['C001', 'C002']
        ... })
        >>> calcular_total_ventas(df)
        3855.0
    """
    if len(df) == 0:
        return 0.0

    df["venta_total"] = df["cantidad"] * df["precio"]
    total = df["venta_total"].sum()

    print(f"[CALCULAR_TOTAL] Total de ventas: {total:.2f}€")
    return float(total)


def enriquecer_ventas_con_clientes(
    df_ventas: pd.DataFrame, df_clientes: pd.DataFrame
) -> pd.DataFrame:
    """
    Combina datos de ventas con información de clientes.

    Hace un merge (left join) entre ventas y clientes usando cliente_id.

    Args:
        df_ventas: DataFrame de ventas
        df_clientes: DataFrame de clientes

    Returns:
        DataFrame enriquecido con información de clientes

    Examples:
        >>> df_ventas = pd.DataFrame({
        ...     'producto': ['Laptop'],
        ...     'cantidad': [3],
        ...     'precio': [1200.0],
        ...     'cliente_id': ['C001']
        ... })
        >>> df_clientes = pd.DataFrame({
        ...     'cliente_id': ['C001'],
        ...     'nombre': ['Alice'],
        ...     'nivel': ['premium']
        ... })
        >>> df = enriquecer_ventas_con_clientes(df_ventas, df_clientes)
        >>> 'nombre' in df.columns
        True
    """
    df_enriquecido = df_ventas.merge(df_clientes, on="cliente_id", how="left")

    print(f"[ENRIQUECER] Enriquecidos {len(df_enriquecido)} registros")
    return df_enriquecido


def calcular_metricas_por_cliente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas agregadas por cliente.

    Agrupa por cliente_id y calcula:
    - total_ventas: suma de cantidad * precio
    - num_productos: cantidad de productos comprados

    Args:
        df: DataFrame enriquecido con ventas y clientes

    Returns:
        DataFrame con métricas por cliente

    Examples:
        >>> df = pd.DataFrame({
        ...     'producto': ['Laptop', 'Mouse', 'Teclado'],
        ...     'cantidad': [3, 10, 5],
        ...     'precio': [1200.0, 25.5, 75.0],
        ...     'cliente_id': ['C001', 'C002', 'C001'],
        ...     'nombre': ['Alice', 'Bob', 'Alice'],
        ...     'nivel': ['premium', 'normal', 'premium']
        ... })
        >>> df_metricas = calcular_metricas_por_cliente(df)
        >>> len(df_metricas)
        2
    """
    df["venta_total"] = df["cantidad"] * df["precio"]

    df_metricas = (
        df.groupby("cliente_id")
        .agg(
            {
                "venta_total": "sum",
                "producto": "count",
                "nombre": "first",
                "nivel": "first",
            }
        )
        .reset_index()
    )

    df_metricas.rename(
        columns={"venta_total": "total_ventas", "producto": "num_productos"},
        inplace=True,
    )

    print(f"[METRICAS_CLIENTE] Calculadas métricas para {len(df_metricas)} clientes")
    return df_metricas
