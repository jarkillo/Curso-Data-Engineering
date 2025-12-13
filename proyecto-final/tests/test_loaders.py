"""Tests para los módulos de carga al data warehouse."""

import pandas as pd
import pytest

from src.loaders.warehouse_loader import (
    create_dim_date,
    load_dimension,
    load_fact_table,
    upsert_records,
    validate_dimension_schema,
    validate_fact_schema,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def dim_product_df():
    """Dimensión de productos."""
    return pd.DataFrame(
        {
            "product_id": ["PROD-001", "PROD-002", "PROD-003"],
            "product_name": ["Laptop Pro", "Mouse Wireless", "Monitor 27"],
            "category": ["Electronics", "Accessories", "Electronics"],
            "price": [999.99, 29.99, 349.99],
        }
    )


@pytest.fixture
def dim_customer_df():
    """Dimensión de clientes."""
    return pd.DataFrame(
        {
            "customer_id": ["CUST-001", "CUST-002", "CUST-003"],
            "customer_name": ["Juan García", "María López", "Carlos Ruiz"],
            "region": ["Madrid", "Barcelona", "Valencia"],
            "segment": ["Gold", "Silver", "Bronze"],
        }
    )


@pytest.fixture
def fact_sales_df():
    """Hechos de ventas."""
    return pd.DataFrame(
        {
            "order_id": ["ORD-001", "ORD-002", "ORD-003"],
            "product_id": ["PROD-001", "PROD-002", "PROD-001"],
            "customer_id": ["CUST-001", "CUST-002", "CUST-001"],
            "date_id": [20240115, 20240116, 20240117],
            "quantity": [2, 1, 3],
            "unit_price": [99.99, 29.99, 99.99],
            "total_amount": [199.98, 29.99, 299.97],
        }
    )


# ============================================================================
# Tests: Dimension Date
# ============================================================================


class TestCreateDimDate:
    """Tests para create_dim_date."""

    def test_creates_date_range(self):
        """Debe crear rango de fechas correcto."""
        df = create_dim_date("2024-01-01", "2024-01-10")
        assert len(df) == 10

    def test_has_required_columns(self):
        """Debe tener columnas requeridas."""
        df = create_dim_date("2024-01-01", "2024-01-05")
        required = ["date_id", "date", "year", "month", "day", "day_of_week"]
        for col in required:
            assert col in df.columns

    def test_date_id_format(self):
        """date_id debe ser formato YYYYMMDD."""
        df = create_dim_date("2024-01-15", "2024-01-15")
        assert df["date_id"].iloc[0] == 20240115

    def test_extracts_date_parts(self):
        """Debe extraer partes de fecha correctamente."""
        df = create_dim_date("2024-03-15", "2024-03-15")
        row = df.iloc[0]
        assert row["year"] == 2024
        assert row["month"] == 3
        assert row["day"] == 15

    def test_identifies_weekends(self):
        """Debe identificar fin de semana."""
        df = create_dim_date("2024-01-13", "2024-01-14")  # Sáb-Dom
        assert df["is_weekend"].all()

    def test_identifies_weekdays(self):
        """Debe identificar días laborables."""
        df = create_dim_date("2024-01-15", "2024-01-16")  # Lun-Mar
        assert not df["is_weekend"].any()


# ============================================================================
# Tests: Dimension Validation
# ============================================================================


class TestValidateDimensionSchema:
    """Tests para validate_dimension_schema."""

    def test_valid_product_dimension(self, dim_product_df):
        """Dimensión válida debe pasar validación."""
        result = validate_dimension_schema(
            dim_product_df, key_column="product_id", name="dim_product"
        )
        assert result["valid"] is True

    def test_fails_with_duplicate_keys(self, dim_product_df):
        """Debe fallar con claves duplicadas."""
        df = pd.concat([dim_product_df, dim_product_df.iloc[[0]]])
        result = validate_dimension_schema(
            df, key_column="product_id", name="dim_product"
        )
        assert result["valid"] is False
        assert "duplicate" in result["error"].lower()

    def test_fails_with_null_keys(self, dim_product_df):
        """Debe fallar con claves nulas."""
        df = dim_product_df.copy()
        df.loc[0, "product_id"] = None
        result = validate_dimension_schema(
            df, key_column="product_id", name="dim_product"
        )
        assert result["valid"] is False
        assert "null" in result["error"].lower()

    def test_fails_with_missing_key_column(self, dim_product_df):
        """Debe fallar si falta columna clave."""
        df = dim_product_df.drop(columns=["product_id"])
        result = validate_dimension_schema(
            df, key_column="product_id", name="dim_product"
        )
        assert result["valid"] is False


# ============================================================================
# Tests: Fact Table Validation
# ============================================================================


class TestValidateFactSchema:
    """Tests para validate_fact_schema."""

    def test_valid_fact_table(self, fact_sales_df):
        """Tabla de hechos válida debe pasar validación."""
        foreign_keys = ["product_id", "customer_id", "date_id"]
        measures = ["quantity", "unit_price", "total_amount"]
        result = validate_fact_schema(
            fact_sales_df,
            foreign_keys=foreign_keys,
            measures=measures,
            name="fact_sales",
        )
        assert result["valid"] is True

    def test_fails_with_missing_foreign_key(self, fact_sales_df):
        """Debe fallar si falta foreign key."""
        df = fact_sales_df.drop(columns=["product_id"])
        result = validate_fact_schema(
            df,
            foreign_keys=["product_id", "customer_id"],
            measures=["quantity"],
            name="fact_sales",
        )
        assert result["valid"] is False
        assert "product_id" in result["error"]

    def test_fails_with_non_numeric_measure(self, fact_sales_df):
        """Debe fallar si medida no es numérica."""
        df = fact_sales_df.copy()
        df["quantity"] = ["two", "one", "three"]
        result = validate_fact_schema(
            df,
            foreign_keys=["product_id"],
            measures=["quantity"],
            name="fact_sales",
        )
        assert result["valid"] is False
        assert "numeric" in result["error"].lower()


# ============================================================================
# Tests: Load Functions
# ============================================================================


class TestLoadDimension:
    """Tests para load_dimension."""

    def test_returns_load_result(self, dim_product_df, tmp_path):
        """Debe retornar resultado de carga."""
        output_path = tmp_path / "dim_product.parquet"
        result = load_dimension(
            dim_product_df,
            output_path=str(output_path),
            key_column="product_id",
            dimension_name="dim_product",
        )
        assert result["status"] == "success"
        assert result["rows_loaded"] == 3
        assert output_path.exists()

    def test_fails_with_invalid_dimension(self, dim_product_df, tmp_path):
        """Debe fallar si dimensión es inválida."""
        df = dim_product_df.copy()
        df.loc[0, "product_id"] = None  # Clave nula
        output_path = tmp_path / "dim_product.parquet"

        result = load_dimension(
            df,
            output_path=str(output_path),
            key_column="product_id",
            dimension_name="dim_product",
        )
        assert result["status"] == "error"


class TestLoadFactTable:
    """Tests para load_fact_table."""

    def test_returns_load_result(self, fact_sales_df, tmp_path):
        """Debe retornar resultado de carga."""
        output_path = tmp_path / "fact_sales.parquet"
        result = load_fact_table(
            fact_sales_df,
            output_path=str(output_path),
            foreign_keys=["product_id", "customer_id"],
            measures=["quantity", "total_amount"],
            fact_name="fact_sales",
        )
        assert result["status"] == "success"
        assert result["rows_loaded"] == 3

    def test_calculates_metrics(self, fact_sales_df, tmp_path):
        """Debe calcular métricas de carga."""
        output_path = tmp_path / "fact_sales.parquet"
        result = load_fact_table(
            fact_sales_df,
            output_path=str(output_path),
            foreign_keys=["product_id"],
            measures=["quantity", "total_amount"],
            fact_name="fact_sales",
        )
        assert "metrics" in result
        assert "total_quantity" in result["metrics"]


# ============================================================================
# Tests: Upsert
# ============================================================================


class TestUpsertRecords:
    """Tests para upsert_records."""

    def test_inserts_new_records(self, dim_product_df, tmp_path):
        """Debe insertar registros nuevos."""
        output_path = tmp_path / "dim_product.parquet"

        # Primera carga
        load_dimension(
            dim_product_df,
            output_path=str(output_path),
            key_column="product_id",
            dimension_name="dim_product",
        )

        # Nuevos registros
        new_records = pd.DataFrame(
            {
                "product_id": ["PROD-004"],
                "product_name": ["Keyboard"],
                "category": ["Accessories"],
                "price": [79.99],
            }
        )

        result = upsert_records(
            new_records,
            existing_path=str(output_path),
            key_column="product_id",
        )

        assert result["inserted"] == 1
        assert result["updated"] == 0

    def test_updates_existing_records(self, dim_product_df, tmp_path):
        """Debe actualizar registros existentes."""
        output_path = tmp_path / "dim_product.parquet"

        # Primera carga
        load_dimension(
            dim_product_df,
            output_path=str(output_path),
            key_column="product_id",
            dimension_name="dim_product",
        )

        # Actualización de registro existente
        updated_records = pd.DataFrame(
            {
                "product_id": ["PROD-001"],
                "product_name": ["Laptop Pro V2"],  # Nombre actualizado
                "category": ["Electronics"],
                "price": [1099.99],  # Precio actualizado
            }
        )

        result = upsert_records(
            updated_records,
            existing_path=str(output_path),
            key_column="product_id",
        )

        assert result["inserted"] == 0
        assert result["updated"] == 1

    def test_handles_mixed_operations(self, dim_product_df, tmp_path):
        """Debe manejar inserts y updates mezclados."""
        output_path = tmp_path / "dim_product.parquet"

        load_dimension(
            dim_product_df,
            output_path=str(output_path),
            key_column="product_id",
            dimension_name="dim_product",
        )

        mixed_records = pd.DataFrame(
            {
                "product_id": ["PROD-001", "PROD-004"],  # 1 existente, 1 nuevo
                "product_name": ["Updated Laptop", "New Keyboard"],
                "category": ["Electronics", "Accessories"],
                "price": [1199.99, 79.99],
            }
        )

        result = upsert_records(
            mixed_records,
            existing_path=str(output_path),
            key_column="product_id",
        )

        assert result["inserted"] == 1
        assert result["updated"] == 1


# ============================================================================
# Integration Tests
# ============================================================================


class TestLoadersIntegration:
    """Tests de integración para loaders."""

    def test_full_warehouse_load(
        self, dim_product_df, dim_customer_df, fact_sales_df, tmp_path
    ):
        """Carga completa del data warehouse."""
        # Cargar dimensiones
        load_dimension(
            dim_product_df,
            output_path=str(tmp_path / "dim_product.parquet"),
            key_column="product_id",
            dimension_name="dim_product",
        )

        load_dimension(
            dim_customer_df,
            output_path=str(tmp_path / "dim_customer.parquet"),
            key_column="customer_id",
            dimension_name="dim_customer",
        )

        # Crear dimensión fecha
        dim_date = create_dim_date("2024-01-15", "2024-01-17")
        load_dimension(
            dim_date,
            output_path=str(tmp_path / "dim_date.parquet"),
            key_column="date_id",
            dimension_name="dim_date",
        )

        # Cargar hechos
        result = load_fact_table(
            fact_sales_df,
            output_path=str(tmp_path / "fact_sales.parquet"),
            foreign_keys=["product_id", "customer_id", "date_id"],
            measures=["quantity", "unit_price", "total_amount"],
            fact_name="fact_sales",
        )

        # Verificar archivos creados
        assert (tmp_path / "dim_product.parquet").exists()
        assert (tmp_path / "dim_customer.parquet").exists()
        assert (tmp_path / "dim_date.parquet").exists()
        assert (tmp_path / "fact_sales.parquet").exists()
        assert result["status"] == "success"
