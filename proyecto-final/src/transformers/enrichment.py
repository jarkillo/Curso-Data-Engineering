"""Funciones de enriquecimiento de datos."""

import pandas as pd


def enrich_orders_with_products(
    orders_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Enriquece pedidos con información de productos.

    Args:
        orders_df: DataFrame de pedidos.
        products_df: DataFrame de productos.

    Returns:
        DataFrame de pedidos enriquecido con datos de productos.

    Examples:
        >>> orders = pd.DataFrame({"order_id": ["1"], "product_id": ["P1"]})
        >>> products = pd.DataFrame({"product_id": ["P1"], "name": ["Test"]})
        >>> enrich_orders_with_products(orders, products)
          order_id product_id product_name
        0        1         P1         Test
    """
    # Preparar productos para merge
    products_subset = products_df[["product_id", "name", "category"]].copy()
    products_subset = products_subset.rename(columns={"name": "product_name"})

    # Left join para mantener todos los pedidos
    enriched = orders_df.merge(products_subset, on="product_id", how="left")

    return enriched


def enrich_orders_with_customers(
    orders_df: pd.DataFrame,
    customers_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Enriquece pedidos con información de clientes.

    Args:
        orders_df: DataFrame de pedidos.
        customers_df: DataFrame de clientes.

    Returns:
        DataFrame de pedidos enriquecido con datos de clientes.

    Examples:
        >>> orders = pd.DataFrame({"order_id": ["1"], "customer_id": ["C1"]})
        >>> customers = pd.DataFrame({"customer_id": ["C1"], "name": ["Juan"]})
        >>> enrich_orders_with_customers(orders, customers)
          order_id customer_id customer_name
        0        1          C1          Juan
    """
    # Preparar clientes para merge
    customers_subset = customers_df[["customer_id", "name", "region"]].copy()
    customers_subset = customers_subset.rename(columns={"name": "customer_name"})

    # Left join para mantener todos los pedidos
    enriched = orders_df.merge(customers_subset, on="customer_id", how="left")

    return enriched


def add_date_id(
    orders_df: pd.DataFrame,
    date_column: str = "order_date",
) -> pd.DataFrame:
    """
    Añade columna date_id para enlazar con dim_date.

    El date_id se genera en formato YYYYMMDD como entero,
    coincidiendo con el formato usado en dim_date.

    Args:
        orders_df: DataFrame de pedidos con columna de fecha.
        date_column: Nombre de la columna de fecha.

    Returns:
        DataFrame con columna date_id añadida.

    Examples:
        >>> orders = pd.DataFrame({
        ...     "order_id": ["1"],
        ...     "order_date": pd.to_datetime(["2024-01-15"])
        ... })
        >>> add_date_id(orders)
          order_id order_date  date_id
        0        1 2024-01-15 20240115
    """
    df = orders_df.copy()

    # Asegurar que la columna es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

    # Generar date_id en formato YYYYMMDD
    df["date_id"] = df[date_column].dt.strftime("%Y%m%d").astype(int)

    return df


def calculate_order_metrics(
    orders_df: pd.DataFrame,
    discount_threshold: float = 0.0,
    discount_rate: float = 0.1,
) -> pd.DataFrame:
    """
    Calcula métricas de pedidos.

    Args:
        orders_df: DataFrame de pedidos.
        discount_threshold: Umbral de total para aplicar descuento.
        discount_rate: Tasa de descuento (0.1 = 10%).

    Returns:
        DataFrame con métricas calculadas.

    Examples:
        >>> orders = pd.DataFrame({"quantity": [2], "unit_price": [10.0]})
        >>> calculate_order_metrics(orders)
           quantity  unit_price  order_total  discount_amount
        0         2        10.0         20.0              0.0
    """
    df = orders_df.copy()

    # Calcular total del pedido
    df["order_total"] = df["quantity"] * df["unit_price"]

    # Calcular descuento si aplica
    df["discount_amount"] = 0.0
    if discount_threshold > 0:
        mask = df["order_total"] >= discount_threshold
        df.loc[mask, "discount_amount"] = df.loc[mask, "order_total"] * discount_rate

    # Total final después de descuento
    df["final_total"] = df["order_total"] - df["discount_amount"]

    return df
