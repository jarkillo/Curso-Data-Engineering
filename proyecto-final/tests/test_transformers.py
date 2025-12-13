"""Tests para los módulos de transformación."""

import pandas as pd
import pytest

from src.transformers.aggregations import (
    aggregate_sales_by_customer,
    aggregate_sales_by_date,
    aggregate_sales_by_product,
    calculate_kpis,
)
from src.transformers.cleaning import (
    clean_customers,
    clean_orders,
    clean_products,
    handle_missing_values,
    remove_duplicates,
)
from src.transformers.enrichment import (
    calculate_order_metrics,
    enrich_orders_with_customers,
    enrich_orders_with_products,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def raw_orders_df():
    """DataFrame de pedidos sin limpiar."""
    return pd.DataFrame(
        {
            "order_id": ["ORD-001", "ORD-002", "ORD-002", "ORD-003", None],
            "customer_id": ["CUST-001", "CUST-002", "CUST-002", "CUST-001", "CUST-003"],
            "product_id": ["PROD-001", "PROD-002", "PROD-002", "PROD-001", "PROD-003"],
            "quantity": [2, 1, 1, 3, -1],
            "unit_price": [99.99, 29.99, 29.99, 99.99, 49.99],
            "order_date": pd.to_datetime(
                [
                    "2024-01-15",
                    "2024-01-16",
                    "2024-01-16",
                    "2024-01-17",
                    "2024-01-18",
                ]
            ),
            "status": ["completed", "pending", "pending", "completed", "cancelled"],
        }
    )


@pytest.fixture
def raw_products_df():
    """DataFrame de productos sin limpiar."""
    return pd.DataFrame(
        {
            "product_id": ["PROD-001", "PROD-002", "PROD-003", "PROD-004"],
            "name": ["Laptop Pro", "Mouse Wireless", None, "Monitor 27"],
            "category": ["Electronics", "Accessories", "Accessories", "Electronics"],
            "price": [999.99, 29.99, 49.99, 349.99],
            "stock": [50, 200, 150, -10],
        }
    )


@pytest.fixture
def raw_customers_df():
    """DataFrame de clientes sin limpiar."""
    return pd.DataFrame(
        {
            "customer_id": ["CUST-001", "CUST-002", "CUST-003", "CUST-001"],
            "name": ["Juan García", "María López", "  Carlos Ruiz  ", "Juan García"],
            "email": [
                "juan@email.com",
                "MARIA@EMAIL.COM",
                "carlos@email.com",
                "juan@email.com",
            ],
            "region": ["Madrid", "Barcelona", None, "Madrid"],
            "created_at": pd.to_datetime(
                ["2023-01-15", "2023-03-20", "2023-06-10", "2023-01-15"]
            ),
        }
    )


@pytest.fixture
def clean_orders_df():
    """DataFrame de pedidos limpio."""
    return pd.DataFrame(
        {
            "order_id": ["ORD-001", "ORD-002", "ORD-003"],
            "customer_id": ["CUST-001", "CUST-002", "CUST-001"],
            "product_id": ["PROD-001", "PROD-002", "PROD-001"],
            "quantity": [2, 1, 3],
            "unit_price": [99.99, 29.99, 99.99],
            "order_date": pd.to_datetime(["2024-01-15", "2024-01-16", "2024-01-17"]),
            "status": ["completed", "pending", "completed"],
        }
    )


@pytest.fixture
def clean_products_df():
    """DataFrame de productos limpio."""
    return pd.DataFrame(
        {
            "product_id": ["PROD-001", "PROD-002", "PROD-004"],
            "name": ["Laptop Pro", "Mouse Wireless", "Monitor 27"],
            "category": ["Electronics", "Accessories", "Electronics"],
            "price": [999.99, 29.99, 349.99],
            "stock": [50, 200, 0],
        }
    )


@pytest.fixture
def clean_customers_df():
    """DataFrame de clientes limpio."""
    return pd.DataFrame(
        {
            "customer_id": ["CUST-001", "CUST-002", "CUST-003"],
            "name": ["Juan García", "María López", "Carlos Ruiz"],
            "email": ["juan@email.com", "maria@email.com", "carlos@email.com"],
            "region": ["Madrid", "Barcelona", "Unknown"],
            "created_at": pd.to_datetime(["2023-01-15", "2023-03-20", "2023-06-10"]),
        }
    )


# ============================================================================
# Tests: Cleaning Functions
# ============================================================================


class TestRemoveDuplicates:
    """Tests para remove_duplicates."""

    def test_removes_exact_duplicates(self, raw_orders_df):
        """Debe eliminar filas completamente duplicadas."""
        df = remove_duplicates(raw_orders_df, subset=["order_id"])
        # ORD-002 aparece 2 veces, debe quedar 1
        assert len(df[df["order_id"] == "ORD-002"]) == 1

    def test_keeps_first_by_default(self, raw_orders_df):
        """Debe mantener primera ocurrencia por defecto."""
        df = remove_duplicates(raw_orders_df, subset=["order_id"], keep="first")
        assert len(df) < len(raw_orders_df)

    def test_custom_subset_columns(self, raw_customers_df):
        """Debe usar columnas personalizadas para detección."""
        df = remove_duplicates(raw_customers_df, subset=["customer_id"])
        # CUST-001 aparece 2 veces
        assert len(df[df["customer_id"] == "CUST-001"]) == 1


class TestHandleMissingValues:
    """Tests para handle_missing_values."""

    def test_fills_numeric_with_default(self, raw_products_df):
        """Debe rellenar numéricos con valor por defecto."""
        df = handle_missing_values(
            raw_products_df, numeric_fill=0, string_fill="Unknown"
        )
        assert df["stock"].isna().sum() == 0

    def test_fills_string_with_default(self, raw_products_df):
        """Debe rellenar strings con valor por defecto."""
        df = handle_missing_values(
            raw_products_df, numeric_fill=0, string_fill="Unknown"
        )
        assert "Unknown" in df["name"].values or df["name"].isna().sum() == 0

    def test_drops_rows_if_specified(self, raw_orders_df):
        """Debe eliminar filas si se especifica."""
        df = handle_missing_values(raw_orders_df, drop_if_null=["order_id"])
        assert df["order_id"].isna().sum() == 0


class TestCleanOrders:
    """Tests para clean_orders."""

    def test_removes_invalid_quantities(self, raw_orders_df):
        """Debe eliminar pedidos con cantidad <= 0."""
        df = clean_orders(raw_orders_df)
        assert (df["quantity"] > 0).all()

    def test_removes_null_order_ids(self, raw_orders_df):
        """Debe eliminar pedidos sin ID."""
        df = clean_orders(raw_orders_df)
        assert df["order_id"].isna().sum() == 0

    def test_removes_duplicate_orders(self, raw_orders_df):
        """Debe eliminar pedidos duplicados."""
        df = clean_orders(raw_orders_df)
        assert df["order_id"].is_unique


class TestCleanProducts:
    """Tests para clean_products."""

    def test_removes_products_without_name(self, raw_products_df):
        """Debe eliminar productos sin nombre."""
        df = clean_products(raw_products_df)
        assert df["name"].isna().sum() == 0

    def test_fixes_negative_stock(self, raw_products_df):
        """Debe corregir stock negativo a 0."""
        df = clean_products(raw_products_df)
        assert (df["stock"] >= 0).all()


class TestCleanCustomers:
    """Tests para clean_customers."""

    def test_trims_whitespace(self, raw_customers_df):
        """Debe eliminar espacios en blanco."""
        df = clean_customers(raw_customers_df)
        # Carlos Ruiz tenía espacios
        assert not df["name"].str.contains(r"^\s|\s$", regex=True).any()

    def test_normalizes_email_case(self, raw_customers_df):
        """Debe normalizar emails a minúsculas."""
        df = clean_customers(raw_customers_df)
        assert (df["email"] == df["email"].str.lower()).all()

    def test_fills_missing_region(self, raw_customers_df):
        """Debe rellenar región faltante."""
        df = clean_customers(raw_customers_df)
        assert df["region"].isna().sum() == 0


# ============================================================================
# Tests: Enrichment Functions
# ============================================================================


class TestEnrichOrdersWithProducts:
    """Tests para enrich_orders_with_products."""

    def test_adds_product_info(self, clean_orders_df, clean_products_df):
        """Debe añadir información del producto."""
        df = enrich_orders_with_products(clean_orders_df, clean_products_df)
        assert "product_name" in df.columns
        assert "category" in df.columns

    def test_handles_missing_products(self, clean_orders_df, clean_products_df):
        """Debe manejar productos no encontrados."""
        # Añadir pedido con producto inexistente
        orders = pd.concat(
            [
                clean_orders_df,
                pd.DataFrame(
                    {
                        "order_id": ["ORD-999"],
                        "customer_id": ["CUST-001"],
                        "product_id": ["PROD-999"],
                        "quantity": [1],
                        "unit_price": [10.0],
                        "order_date": [pd.Timestamp("2024-01-20")],
                        "status": ["completed"],
                    }
                ),
            ]
        )
        df = enrich_orders_with_products(orders, clean_products_df)
        # Debe mantener el pedido aunque no encuentre producto
        assert "ORD-999" in df["order_id"].values


class TestEnrichOrdersWithCustomers:
    """Tests para enrich_orders_with_customers."""

    def test_adds_customer_info(self, clean_orders_df, clean_customers_df):
        """Debe añadir información del cliente."""
        df = enrich_orders_with_customers(clean_orders_df, clean_customers_df)
        assert "customer_name" in df.columns
        assert "region" in df.columns


class TestCalculateOrderMetrics:
    """Tests para calculate_order_metrics."""

    def test_calculates_total(self, clean_orders_df):
        """Debe calcular total del pedido."""
        df = calculate_order_metrics(clean_orders_df)
        assert "order_total" in df.columns
        # order_total = quantity * unit_price
        first_order = df[df["order_id"] == "ORD-001"].iloc[0]
        expected = first_order["quantity"] * first_order["unit_price"]
        assert first_order["order_total"] == pytest.approx(expected)

    def test_calculates_discount(self, clean_orders_df):
        """Debe calcular descuento si aplica."""
        df = calculate_order_metrics(clean_orders_df, discount_threshold=100)
        assert "discount_amount" in df.columns


# ============================================================================
# Tests: Aggregation Functions
# ============================================================================


class TestAggregateSalesByProduct:
    """Tests para aggregate_sales_by_product."""

    def test_aggregates_by_product(self, clean_orders_df, clean_products_df):
        """Debe agregar ventas por producto."""
        enriched = enrich_orders_with_products(clean_orders_df, clean_products_df)
        enriched = calculate_order_metrics(enriched)
        agg = aggregate_sales_by_product(enriched)

        assert "product_id" in agg.columns
        assert "total_revenue" in agg.columns
        assert "total_quantity" in agg.columns
        assert "order_count" in agg.columns

    def test_calculates_correct_totals(self, clean_orders_df, clean_products_df):
        """Debe calcular totales correctos."""
        enriched = enrich_orders_with_products(clean_orders_df, clean_products_df)
        enriched = calculate_order_metrics(enriched)
        agg = aggregate_sales_by_product(enriched)

        # PROD-001 tiene 2 pedidos (qty 2 + 3 = 5)
        prod_001 = agg[agg["product_id"] == "PROD-001"].iloc[0]
        assert prod_001["total_quantity"] == 5


class TestAggregateSalesByCustomer:
    """Tests para aggregate_sales_by_customer."""

    def test_aggregates_by_customer(self, clean_orders_df):
        """Debe agregar ventas por cliente."""
        orders = calculate_order_metrics(clean_orders_df)
        agg = aggregate_sales_by_customer(orders)

        assert "customer_id" in agg.columns
        assert "total_spent" in agg.columns
        assert "order_count" in agg.columns

    def test_calculates_average_order_value(self, clean_orders_df):
        """Debe calcular AOV por cliente."""
        orders = calculate_order_metrics(clean_orders_df)
        agg = aggregate_sales_by_customer(orders)

        assert "avg_order_value" in agg.columns


class TestAggregateSalesByDate:
    """Tests para aggregate_sales_by_date."""

    def test_aggregates_by_day(self, clean_orders_df):
        """Debe agregar ventas por día."""
        orders = calculate_order_metrics(clean_orders_df)
        agg = aggregate_sales_by_date(orders, frequency="D")

        assert len(agg) == 3  # 3 días distintos

    def test_aggregates_by_week(self, clean_orders_df):
        """Debe agregar ventas por semana."""
        orders = calculate_order_metrics(clean_orders_df)
        agg = aggregate_sales_by_date(orders, frequency="W")

        assert "date" in agg.columns
        assert "daily_revenue" in agg.columns


class TestCalculateKpis:
    """Tests para calculate_kpis."""

    def test_returns_kpi_dict(self, clean_orders_df):
        """Debe retornar diccionario con KPIs."""
        orders = calculate_order_metrics(clean_orders_df)
        kpis = calculate_kpis(orders)

        assert isinstance(kpis, dict)
        assert "total_revenue" in kpis
        assert "total_orders" in kpis
        assert "avg_order_value" in kpis

    def test_calculates_conversion_rate(self, clean_orders_df):
        """Debe calcular tasa de completados."""
        orders = calculate_order_metrics(clean_orders_df)
        kpis = calculate_kpis(orders)

        assert "completion_rate" in kpis
        # 2 de 3 están completed = 66.67%
        assert kpis["completion_rate"] == pytest.approx(66.67, rel=0.01)


# ============================================================================
# Integration Tests
# ============================================================================


class TestTransformersIntegration:
    """Tests de integración para transformadores."""

    def test_full_transformation_pipeline(
        self, raw_orders_df, raw_products_df, raw_customers_df
    ):
        """Pipeline completo de transformación."""
        # 1. Limpiar datos
        cleaned_orders_df = clean_orders(raw_orders_df)
        cleaned_prods_df = clean_products(raw_products_df)
        cleaned_custs_df = clean_customers(raw_customers_df)

        # 2. Enriquecer
        enriched = enrich_orders_with_products(cleaned_orders_df, cleaned_prods_df)
        enriched = enrich_orders_with_customers(enriched, cleaned_custs_df)
        enriched = calculate_order_metrics(enriched)

        # 3. Agregar
        by_product = aggregate_sales_by_product(enriched)
        by_customer = aggregate_sales_by_customer(enriched)
        kpis = calculate_kpis(enriched)

        # Verificar resultados
        assert len(cleaned_orders_df) < len(raw_orders_df)  # Se eliminaron inválidos
        assert "product_name" in enriched.columns
        assert "customer_name" in enriched.columns
        assert "order_total" in enriched.columns
        assert len(by_product) > 0
        assert len(by_customer) > 0
        assert kpis["total_orders"] == len(cleaned_orders_df)
