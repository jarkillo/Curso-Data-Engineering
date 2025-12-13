"""Funciones de agregación de datos."""

from typing import Any

import pandas as pd


def aggregate_sales_by_product(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega ventas por producto.

    Args:
        orders_df: DataFrame de pedidos con order_total calculado.

    Returns:
        DataFrame agregado por producto.

    Examples:
        >>> orders = pd.DataFrame({
        ...     "product_id": ["P1", "P1", "P2"],
        ...     "quantity": [2, 3, 1],
        ...     "order_total": [20.0, 30.0, 10.0]
        ... })
        >>> aggregate_sales_by_product(orders)
          product_id  total_quantity  total_revenue  order_count
        0         P1               5           50.0            2
        1         P2               1           10.0            1
    """
    agg = (
        orders_df.groupby("product_id")
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("order_total", "sum"),
            order_count=("order_total", "count"),
            avg_unit_price=("unit_price", "mean"),
        )
        .reset_index()
    )

    return agg


def aggregate_sales_by_customer(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega ventas por cliente.

    Args:
        orders_df: DataFrame de pedidos con order_total calculado.

    Returns:
        DataFrame agregado por cliente.

    Examples:
        >>> orders = pd.DataFrame({
        ...     "customer_id": ["C1", "C1", "C2"],
        ...     "order_total": [100.0, 150.0, 200.0]
        ... })
        >>> aggregate_sales_by_customer(orders)
          customer_id  total_spent  order_count  avg_order_value
        0          C1        250.0            2            125.0
        1          C2        200.0            1            200.0
    """
    agg = (
        orders_df.groupby("customer_id")
        .agg(
            total_spent=("order_total", "sum"),
            order_count=("order_total", "count"),
        )
        .reset_index()
    )

    # Calcular AOV
    agg["avg_order_value"] = agg["total_spent"] / agg["order_count"]

    return agg


def aggregate_sales_by_date(
    orders_df: pd.DataFrame,
    frequency: str = "D",
    date_column: str = "order_date",
) -> pd.DataFrame:
    """
    Agrega ventas por período temporal.

    Args:
        orders_df: DataFrame de pedidos con order_total y fecha.
        frequency: Frecuencia de agregación ('D'=día, 'W'=semana, 'M'=mes).
        date_column: Nombre de la columna de fecha.

    Returns:
        DataFrame agregado por fecha.

    Examples:
        >>> orders = pd.DataFrame({
        ...     "order_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        ...     "order_total": [100.0, 150.0]
        ... })
        >>> aggregate_sales_by_date(orders, frequency="D")
                date  daily_revenue  order_count
        0 2024-01-01          250.0            2
    """
    df = orders_df.copy()

    # Asegurar que la columna de fecha es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

    # Agrupar por período
    df["date"] = df[date_column].dt.to_period(frequency).dt.to_timestamp()

    agg = (
        df.groupby("date")
        .agg(
            daily_revenue=("order_total", "sum"),
            order_count=("order_total", "count"),
        )
        .reset_index()
    )

    return agg


def calculate_kpis(orders_df: pd.DataFrame) -> dict[str, Any]:
    """
    Calcula KPIs de negocio.

    Args:
        orders_df: DataFrame de pedidos con métricas calculadas.

    Returns:
        Diccionario con KPIs calculados.

    Examples:
        >>> orders = pd.DataFrame({
        ...     "order_total": [100.0, 200.0],
        ...     "status": ["completed", "pending"]
        ... })
        >>> kpis = calculate_kpis(orders)
        >>> kpis["total_revenue"]
        300.0
    """
    total_revenue = orders_df["order_total"].sum()
    total_orders = len(orders_df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Tasa de completados
    completed_count = len(orders_df[orders_df["status"] == "completed"])
    completion_rate = (completed_count / total_orders * 100) if total_orders > 0 else 0

    # Clientes únicos
    unique_customers = orders_df["customer_id"].nunique()

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "completion_rate": round(completion_rate, 2),
        "unique_customers": unique_customers,
    }
