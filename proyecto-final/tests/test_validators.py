"""Tests para las funciones de validación."""

import pandas as pd
import pytest

from src.utils.validators import (
    run_all_validations,
    validate_dataframe_not_empty,
    validate_date_range,
    validate_no_nulls_in_columns,
    validate_numeric_range,
    validate_required_columns,
    validate_unique_values,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def sample_df():
    """DataFrame de ejemplo para tests."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "score": [85.5, 92.0, 78.5],
            "date": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-01-30"]),
        }
    )


@pytest.fixture
def df_with_nulls():
    """DataFrame con valores nulos."""
    return pd.DataFrame(
        {
            "id": [1, 2, None],
            "name": ["Alice", None, "Charlie"],
            "value": [10.0, 20.0, 30.0],
        }
    )


# ============================================================================
# Tests: validate_dataframe_not_empty
# ============================================================================


class TestValidateDataframeNotEmpty:
    """Tests para validate_dataframe_not_empty."""

    def test_non_empty_df_passes(self, sample_df):
        """DataFrame no vacío debe pasar."""
        result = validate_dataframe_not_empty(sample_df)
        assert result["valid"] is True

    def test_empty_df_fails(self):
        """DataFrame vacío debe fallar."""
        empty_df = pd.DataFrame()
        result = validate_dataframe_not_empty(empty_df)
        assert result["valid"] is False
        assert "empty" in result["error"].lower()

    def test_df_with_no_rows_fails(self):
        """DataFrame con columnas pero sin filas debe fallar."""
        df = pd.DataFrame(columns=["a", "b", "c"])
        result = validate_dataframe_not_empty(df)
        assert result["valid"] is False


# ============================================================================
# Tests: validate_required_columns
# ============================================================================


class TestValidateRequiredColumns:
    """Tests para validate_required_columns."""

    def test_all_columns_present_passes(self, sample_df):
        """Todas las columnas presentes debe pasar."""
        result = validate_required_columns(sample_df, ["id", "name", "age"])
        assert result["valid"] is True

    def test_missing_column_fails(self, sample_df):
        """Columna faltante debe fallar."""
        result = validate_required_columns(sample_df, ["id", "nonexistent"])
        assert result["valid"] is False
        assert "nonexistent" in result["missing_columns"]

    def test_returns_all_missing_columns(self, sample_df):
        """Debe retornar todas las columnas faltantes."""
        result = validate_required_columns(sample_df, ["id", "foo", "bar"])
        assert "foo" in result["missing_columns"]
        assert "bar" in result["missing_columns"]


# ============================================================================
# Tests: validate_no_nulls_in_columns
# ============================================================================


class TestValidateNoNullsInColumns:
    """Tests para validate_no_nulls_in_columns."""

    def test_no_nulls_passes(self, sample_df):
        """Sin nulos debe pasar."""
        result = validate_no_nulls_in_columns(sample_df, ["id", "name"])
        assert result["valid"] is True

    def test_nulls_present_fails(self, df_with_nulls):
        """Con nulos debe fallar."""
        result = validate_no_nulls_in_columns(df_with_nulls, ["id", "name"])
        assert result["valid"] is False
        assert "id" in result["columns_with_nulls"]
        assert "name" in result["columns_with_nulls"]

    def test_reports_null_counts(self, df_with_nulls):
        """Debe reportar conteo de nulos."""
        result = validate_no_nulls_in_columns(df_with_nulls, ["id", "name"])
        assert result["columns_with_nulls"]["id"] == 1
        assert result["columns_with_nulls"]["name"] == 1


# ============================================================================
# Tests: validate_numeric_range
# ============================================================================


class TestValidateNumericRange:
    """Tests para validate_numeric_range."""

    def test_values_in_range_passes(self, sample_df):
        """Valores en rango deben pasar."""
        result = validate_numeric_range(sample_df, "age", min_val=20, max_val=40)
        assert result["valid"] is True

    def test_values_below_min_fails(self, sample_df):
        """Valores por debajo del mínimo deben fallar."""
        result = validate_numeric_range(sample_df, "age", min_val=30, max_val=50)
        assert result["valid"] is False
        assert result["below_min"] > 0

    def test_values_above_max_fails(self, sample_df):
        """Valores por encima del máximo deben fallar."""
        result = validate_numeric_range(sample_df, "age", min_val=10, max_val=30)
        assert result["valid"] is False
        assert result["above_max"] > 0

    def test_only_min_constraint(self, sample_df):
        """Solo restricción de mínimo."""
        result = validate_numeric_range(sample_df, "age", min_val=20)
        assert result["valid"] is True


# ============================================================================
# Tests: validate_date_range
# ============================================================================


class TestValidateDateRange:
    """Tests para validate_date_range."""

    def test_dates_in_range_passes(self, sample_df):
        """Fechas en rango deben pasar."""
        result = validate_date_range(
            sample_df, "date", min_date="2024-01-01", max_date="2024-02-01"
        )
        assert result["valid"] is True

    def test_dates_before_min_fails(self, sample_df):
        """Fechas antes del mínimo deben fallar."""
        result = validate_date_range(
            sample_df, "date", min_date="2024-01-10", max_date="2024-02-01"
        )
        assert result["valid"] is False
        assert result["before_min"] > 0

    def test_dates_after_max_fails(self, sample_df):
        """Fechas después del máximo deben fallar."""
        result = validate_date_range(
            sample_df, "date", min_date="2024-01-01", max_date="2024-01-20"
        )
        assert result["valid"] is False
        assert result["after_max"] > 0


# ============================================================================
# Tests: validate_unique_values
# ============================================================================


class TestValidateUniqueValues:
    """Tests para validate_unique_values."""

    def test_unique_values_passes(self, sample_df):
        """Valores únicos deben pasar."""
        result = validate_unique_values(sample_df, "id")
        assert result["valid"] is True

    def test_duplicate_values_fails(self):
        """Valores duplicados deben fallar."""
        df = pd.DataFrame({"id": [1, 2, 2, 3]})
        result = validate_unique_values(df, "id")
        assert result["valid"] is False
        assert result["duplicate_count"] == 1


# ============================================================================
# Tests: run_all_validations
# ============================================================================


class TestRunAllValidations:
    """Tests para run_all_validations."""

    def test_all_validations_pass(self, sample_df):
        """Todas las validaciones pasando."""
        validations = [
            ("not_empty", {"df": sample_df}),
            ("required_columns", {"df": sample_df, "columns": ["id", "name"]}),
            ("no_nulls", {"df": sample_df, "columns": ["id"]}),
        ]
        result = run_all_validations(validations)
        assert result["all_passed"] is True
        assert result["passed_count"] == 3
        assert result["failed_count"] == 0

    def test_some_validations_fail(self, df_with_nulls):
        """Algunas validaciones fallando."""
        validations = [
            ("not_empty", {"df": df_with_nulls}),
            ("no_nulls", {"df": df_with_nulls, "columns": ["id", "name"]}),
        ]
        result = run_all_validations(validations)
        assert result["all_passed"] is False
        assert result["failed_count"] > 0

    def test_returns_detailed_results(self, sample_df):
        """Debe retornar resultados detallados."""
        validations = [
            ("not_empty", {"df": sample_df}),
        ]
        result = run_all_validations(validations)
        assert "details" in result
        assert "not_empty" in result["details"]
