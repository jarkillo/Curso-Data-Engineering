"""Tests para los módulos de extracción."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.extractors.api_extractor import (
    extract_orders_from_api,
    parse_order_response,
    validate_api_response,
)
from src.extractors.csv_extractor import (
    extract_products_from_csv,
    validate_csv_schema,
)
from src.extractors.db_extractor import (
    build_customer_query,
    extract_customers_from_db,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def sample_api_response():
    """Respuesta de API de pedidos simulada."""
    return {
        "status": "success",
        "data": [
            {
                "order_id": "ORD-001",
                "customer_id": "CUST-001",
                "product_id": "PROD-001",
                "quantity": 2,
                "unit_price": 99.99,
                "order_date": "2024-01-15T10:30:00Z",
                "status": "completed",
            },
            {
                "order_id": "ORD-002",
                "customer_id": "CUST-002",
                "product_id": "PROD-003",
                "quantity": 1,
                "unit_price": 149.99,
                "order_date": "2024-01-15T11:45:00Z",
                "status": "pending",
            },
        ],
        "total_count": 2,
    }


@pytest.fixture
def sample_products_csv(tmp_path):
    """Archivo CSV de productos temporal."""
    csv_content = """product_id,name,category,price,stock
PROD-001,Laptop Pro 15,Electronics,999.99,50
PROD-002,Wireless Mouse,Accessories,29.99,200
PROD-003,USB-C Hub,Accessories,49.99,150
PROD-004,Monitor 27",Electronics,349.99,30
"""
    csv_path = tmp_path / "products.csv"
    csv_path.write_text(csv_content)
    return csv_path


@pytest.fixture
def sample_customers_df():
    """DataFrame de clientes simulado."""
    return pd.DataFrame(
        {
            "customer_id": ["CUST-001", "CUST-002", "CUST-003"],
            "name": ["Juan García", "María López", "Carlos Ruiz"],
            "email": ["juan@email.com", "maria@email.com", "carlos@email.com"],
            "region": ["Madrid", "Barcelona", "Valencia"],
            "created_at": pd.to_datetime(["2023-01-15", "2023-03-20", "2023-06-10"]),
        }
    )


# ============================================================================
# Tests: API Extractor
# ============================================================================


class TestValidateApiResponse:
    """Tests para validate_api_response."""

    def test_valid_response_passes(self, sample_api_response):
        """Respuesta válida debe pasar validación."""
        result = validate_api_response(sample_api_response)
        assert result["valid"] is True
        assert result["record_count"] == 2

    def test_missing_status_fails(self):
        """Respuesta sin status debe fallar."""
        response = {"data": []}
        result = validate_api_response(response)
        assert result["valid"] is False
        assert "status" in result["error"].lower()

    def test_error_status_fails(self):
        """Respuesta con status error debe fallar."""
        response = {"status": "error", "message": "API error"}
        result = validate_api_response(response)
        assert result["valid"] is False
        assert "error" in result["error"].lower()

    def test_missing_data_fails(self):
        """Respuesta sin campo data debe fallar."""
        response = {"status": "success"}
        result = validate_api_response(response)
        assert result["valid"] is False
        assert "data" in result["error"].lower()

    def test_empty_data_is_valid(self):
        """Respuesta con data vacío es válida."""
        response = {"status": "success", "data": [], "total_count": 0}
        result = validate_api_response(response)
        assert result["valid"] is True
        assert result["record_count"] == 0


class TestParseOrderResponse:
    """Tests para parse_order_response."""

    def test_parses_to_dataframe(self, sample_api_response):
        """Debe convertir respuesta a DataFrame."""
        df = parse_order_response(sample_api_response)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_has_required_columns(self, sample_api_response):
        """DataFrame debe tener columnas requeridas."""
        df = parse_order_response(sample_api_response)
        required_cols = [
            "order_id",
            "customer_id",
            "product_id",
            "quantity",
            "unit_price",
        ]
        for col in required_cols:
            assert col in df.columns

    def test_parses_dates(self, sample_api_response):
        """Debe parsear fechas correctamente."""
        df = parse_order_response(sample_api_response)
        assert pd.api.types.is_datetime64_any_dtype(df["order_date"])

    def test_empty_response_returns_empty_df(self):
        """Respuesta vacía debe retornar DataFrame vacío."""
        response = {"status": "success", "data": [], "total_count": 0}
        df = parse_order_response(response)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestExtractOrdersFromApi:
    """Tests para extract_orders_from_api."""

    @patch("src.extractors.api_extractor.requests.get")
    def test_successful_extraction(self, mock_get, sample_api_response):
        """Extracción exitosa debe retornar DataFrame."""
        mock_get.return_value = MagicMock(
            status_code=200, json=lambda: sample_api_response
        )

        df = extract_orders_from_api("http://api.test.com/orders")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    @patch("src.extractors.api_extractor.requests.get")
    def test_handles_http_error(self, mock_get):
        """Debe manejar errores HTTP."""
        mock_get.return_value = MagicMock(status_code=500)

        with pytest.raises(ConnectionError, match="API request failed"):
            extract_orders_from_api("http://api.test.com/orders")

    @patch("src.extractors.api_extractor.requests.get")
    def test_handles_timeout(self, mock_get):
        """Debe manejar timeouts."""
        import requests

        mock_get.side_effect = requests.Timeout()

        with pytest.raises(ConnectionError, match="timeout"):
            extract_orders_from_api("http://api.test.com/orders", timeout=5)

    @patch("src.extractors.api_extractor.requests.get")
    def test_passes_auth_headers(self, mock_get, sample_api_response):
        """Debe pasar headers de autenticación."""
        mock_get.return_value = MagicMock(
            status_code=200, json=lambda: sample_api_response
        )

        extract_orders_from_api("http://api.test.com/orders", api_key="test-key-123")

        call_args = mock_get.call_args
        assert "Authorization" in call_args.kwargs.get("headers", {})


# ============================================================================
# Tests: CSV Extractor
# ============================================================================


class TestValidateCsvSchema:
    """Tests para validate_csv_schema."""

    def test_valid_schema_passes(self, sample_products_csv):
        """CSV con schema válido debe pasar."""
        required_cols = ["product_id", "name", "category", "price"]
        result = validate_csv_schema(sample_products_csv, required_cols)
        assert result["valid"] is True

    def test_missing_column_fails(self, sample_products_csv):
        """CSV con columna faltante debe fallar."""
        required_cols = ["product_id", "name", "nonexistent_column"]
        result = validate_csv_schema(sample_products_csv, required_cols)
        assert result["valid"] is False
        assert "nonexistent_column" in result["missing_columns"]

    def test_extra_columns_allowed(self, sample_products_csv):
        """CSV con columnas extra debe pasar."""
        required_cols = ["product_id", "name"]
        result = validate_csv_schema(sample_products_csv, required_cols)
        assert result["valid"] is True
        assert len(result.get("extra_columns", [])) > 0


class TestExtractProductsFromCsv:
    """Tests para extract_products_from_csv."""

    def test_extracts_all_products(self, sample_products_csv):
        """Debe extraer todos los productos."""
        df = extract_products_from_csv(sample_products_csv)
        assert len(df) == 4

    def test_correct_dtypes(self, sample_products_csv):
        """Debe tener tipos de datos correctos."""
        df = extract_products_from_csv(sample_products_csv)
        assert df["price"].dtype == float
        assert df["stock"].dtype == int

    def test_handles_file_not_found(self):
        """Debe manejar archivo no encontrado."""
        with pytest.raises(FileNotFoundError):
            extract_products_from_csv(Path("/nonexistent/path.csv"))

    def test_handles_encoding(self, tmp_path):
        """Debe manejar diferentes encodings."""
        csv_content = "product_id,name\nPROD-001,Cámara\n"
        csv_path = tmp_path / "products_utf8.csv"
        csv_path.write_text(csv_content, encoding="utf-8")

        df = extract_products_from_csv(csv_path, encoding="utf-8")
        assert "Cámara" in df["name"].values

    def test_filters_by_category(self, sample_products_csv):
        """Debe poder filtrar por categoría."""
        df = extract_products_from_csv(
            sample_products_csv, category_filter="Electronics"
        )
        assert len(df) == 2
        assert all(df["category"] == "Electronics")


# ============================================================================
# Tests: DB Extractor
# ============================================================================


class TestBuildCustomerQuery:
    """Tests para build_customer_query."""

    def test_basic_query(self):
        """Query básica sin filtros."""
        query = build_customer_query()
        assert "SELECT" in query
        assert "FROM customers" in query

    def test_query_with_date_filter(self):
        """Query con filtro de fecha."""
        query = build_customer_query(since_date="2024-01-01")
        assert "WHERE" in query
        assert "created_at" in query

    def test_query_with_region_filter(self):
        """Query con filtro de región."""
        query = build_customer_query(region="Madrid")
        assert "WHERE" in query
        assert "region" in query

    def test_query_with_multiple_filters(self):
        """Query con múltiples filtros."""
        query = build_customer_query(since_date="2024-01-01", region="Madrid")
        assert "AND" in query

    def test_query_with_limit(self):
        """Query con límite."""
        query = build_customer_query(limit=100)
        assert "LIMIT 100" in query


class TestExtractCustomersFromDb:
    """Tests para extract_customers_from_db."""

    @patch("src.extractors.db_extractor.create_engine")
    def test_successful_extraction(self, mock_engine, sample_customers_df):
        """Extracción exitosa debe retornar DataFrame."""
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = MagicMock(
            return_value=mock_conn
        )
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(
            return_value=False
        )

        with patch("src.extractors.db_extractor.pd.read_sql") as mock_read:
            mock_read.return_value = sample_customers_df
            df = extract_customers_from_db("postgresql://test/db")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_invalid_connection_string(self):
        """Debe fallar con connection string inválida."""
        with pytest.raises(ValueError, match="connection string"):
            extract_customers_from_db("")

    @patch("src.extractors.db_extractor.create_engine")
    def test_handles_db_error(self, mock_engine):
        """Debe manejar errores de base de datos."""
        mock_engine.side_effect = Exception("Connection failed")

        with pytest.raises(ConnectionError, match="database"):
            extract_customers_from_db("postgresql://test/db")


# ============================================================================
# Integration Tests
# ============================================================================


class TestExtractorsIntegration:
    """Tests de integración para extractores."""

    @patch("src.extractors.api_extractor.requests.get")
    @patch("src.extractors.db_extractor.create_engine")
    def test_all_extractors_return_dataframes(
        self,
        mock_engine,
        mock_get,
        sample_api_response,
        sample_products_csv,
        sample_customers_df,
    ):
        """Todos los extractores deben retornar DataFrames compatibles."""
        # Setup mocks
        mock_get.return_value = MagicMock(
            status_code=200, json=lambda: sample_api_response
        )
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__ = MagicMock(
            return_value=mock_conn
        )
        mock_engine.return_value.connect.return_value.__exit__ = MagicMock(
            return_value=False
        )

        with patch("src.extractors.db_extractor.pd.read_sql") as mock_read:
            mock_read.return_value = sample_customers_df

            # Extract from all sources
            orders_df = extract_orders_from_api("http://api.test.com")
            products_df = extract_products_from_csv(sample_products_csv)
            customers_df = extract_customers_from_db("postgresql://test/db")

        # All should be DataFrames
        assert all(
            isinstance(df, pd.DataFrame)
            for df in [orders_df, products_df, customers_df]
        )

        # Should have expected ID columns for joining
        assert "product_id" in orders_df.columns
        assert "product_id" in products_df.columns
        assert "customer_id" in orders_df.columns
        assert "customer_id" in customers_df.columns
