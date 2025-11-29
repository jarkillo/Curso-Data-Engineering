"""Tests para el módulo de cálculo de KPIs."""

from datetime import date

import pytest

from src.kpis import (
    KPIResult,
    calculate_aov,
    calculate_arr,
    calculate_cac,
    calculate_churn_rate,
    calculate_conversion_rate,
    calculate_ltv,
    calculate_mrr,
    calculate_nrr,
    calculate_retention_rate,
)


class TestCalculateAOV:
    """Tests para Average Order Value (AOV)."""

    def test_aov_with_valid_data(self) -> None:
        """Should calculate AOV correctly with valid inputs."""
        total_revenue = 10000.0
        total_orders = 200

        result = calculate_aov(total_revenue, total_orders)

        assert result.value == 50.0
        assert result.name == "AOV"
        assert result.unit == "currency"

    def test_aov_with_decimal_result(self) -> None:
        """Should return precise decimal result."""
        total_revenue = 1000.0
        total_orders = 3

        result = calculate_aov(total_revenue, total_orders)

        assert round(result.value, 2) == 333.33

    def test_aov_with_zero_orders_raises_error(self) -> None:
        """Should raise ValueError when orders is zero."""
        with pytest.raises(ValueError, match="Total orders must be greater than zero"):
            calculate_aov(1000.0, 0)

    def test_aov_with_negative_orders_raises_error(self) -> None:
        """Should raise ValueError when orders is negative."""
        with pytest.raises(ValueError, match="Total orders must be greater than zero"):
            calculate_aov(1000.0, -5)

    def test_aov_with_negative_revenue_raises_error(self) -> None:
        """Should raise ValueError when revenue is negative."""
        with pytest.raises(ValueError, match="Total revenue cannot be negative"):
            calculate_aov(-1000.0, 100)

    def test_aov_with_zero_revenue(self) -> None:
        """Should return 0 when revenue is zero."""
        result = calculate_aov(0.0, 100)
        assert result.value == 0.0


class TestCalculateConversionRate:
    """Tests para Conversion Rate."""

    def test_conversion_rate_basic(self) -> None:
        """Should calculate conversion rate correctly."""
        conversions = 50
        total_visitors = 1000

        result = calculate_conversion_rate(conversions, total_visitors)

        assert result.value == 5.0
        assert result.name == "Conversion Rate"
        assert result.unit == "percent"

    def test_conversion_rate_100_percent(self) -> None:
        """Should handle 100% conversion rate."""
        result = calculate_conversion_rate(100, 100)
        assert result.value == 100.0

    def test_conversion_rate_zero_conversions(self) -> None:
        """Should return 0 when no conversions."""
        result = calculate_conversion_rate(0, 1000)
        assert result.value == 0.0

    def test_conversion_rate_zero_visitors_raises_error(self) -> None:
        """Should raise ValueError when visitors is zero."""
        with pytest.raises(
            ValueError, match="Total visitors must be greater than zero"
        ):
            calculate_conversion_rate(10, 0)

    def test_conversion_rate_more_conversions_than_visitors_raises_error(self) -> None:
        """Should raise ValueError when conversions exceed visitors."""
        with pytest.raises(
            ValueError, match="Conversions cannot exceed total visitors"
        ):
            calculate_conversion_rate(150, 100)


class TestCalculateCAC:
    """Tests para Customer Acquisition Cost (CAC)."""

    def test_cac_basic(self) -> None:
        """Should calculate CAC correctly."""
        marketing_spend = 10000.0
        new_customers = 100

        result = calculate_cac(marketing_spend, new_customers)

        assert result.value == 100.0
        assert result.name == "CAC"
        assert result.unit == "currency"

    def test_cac_zero_customers_raises_error(self) -> None:
        """Should raise ValueError when customers is zero."""
        with pytest.raises(ValueError, match="New customers must be greater than zero"):
            calculate_cac(10000.0, 0)

    def test_cac_zero_spend(self) -> None:
        """Should return 0 when marketing spend is zero."""
        result = calculate_cac(0.0, 100)
        assert result.value == 0.0

    def test_cac_negative_spend_raises_error(self) -> None:
        """Should raise ValueError when spend is negative."""
        with pytest.raises(ValueError, match="Marketing spend cannot be negative"):
            calculate_cac(-1000.0, 100)


class TestCalculateLTV:
    """Tests para Customer Lifetime Value (LTV)."""

    def test_ltv_basic(self) -> None:
        """Should calculate LTV correctly."""
        avg_order_value = 50.0
        purchase_frequency = 4.0  # per year
        customer_lifespan = 3.0  # years

        result = calculate_ltv(avg_order_value, purchase_frequency, customer_lifespan)

        assert result.value == 600.0  # 50 * 4 * 3
        assert result.name == "LTV"
        assert result.unit == "currency"

    def test_ltv_with_margin(self) -> None:
        """Should calculate LTV with gross margin."""
        result = calculate_ltv(
            avg_order_value=100.0,
            purchase_frequency=2.0,
            customer_lifespan=5.0,
            gross_margin=0.3,
        )

        assert result.value == 300.0  # 100 * 2 * 5 * 0.3

    def test_ltv_zero_frequency_raises_error(self) -> None:
        """Should raise ValueError when frequency is zero or negative."""
        with pytest.raises(ValueError, match="Purchase frequency must be positive"):
            calculate_ltv(50.0, 0.0, 3.0)

    def test_ltv_invalid_margin_raises_error(self) -> None:
        """Should raise ValueError when margin is outside 0-1 range."""
        with pytest.raises(ValueError, match="Gross margin must be between 0 and 1"):
            calculate_ltv(50.0, 4.0, 3.0, gross_margin=1.5)


class TestCalculateChurnRate:
    """Tests para Churn Rate."""

    def test_churn_rate_basic(self) -> None:
        """Should calculate churn rate correctly."""
        lost_customers = 50
        total_customers_start = 1000

        result = calculate_churn_rate(lost_customers, total_customers_start)

        assert result.value == 5.0
        assert result.name == "Churn Rate"
        assert result.unit == "percent"

    def test_churn_rate_zero_lost(self) -> None:
        """Should return 0 when no customers lost."""
        result = calculate_churn_rate(0, 1000)
        assert result.value == 0.0

    def test_churn_rate_zero_start_raises_error(self) -> None:
        """Should raise ValueError when starting customers is zero."""
        with pytest.raises(
            ValueError, match="Starting customers must be greater than zero"
        ):
            calculate_churn_rate(50, 0)

    def test_churn_rate_more_lost_than_total_raises_error(self) -> None:
        """Should raise ValueError when lost exceeds total."""
        with pytest.raises(
            ValueError, match="Lost customers cannot exceed starting customers"
        ):
            calculate_churn_rate(150, 100)


class TestCalculateRetentionRate:
    """Tests para Retention Rate."""

    def test_retention_rate_basic(self) -> None:
        """Should calculate retention rate correctly."""
        retained = 850
        total_start = 1000

        result = calculate_retention_rate(retained, total_start)

        assert result.value == 85.0
        assert result.name == "Retention Rate"
        assert result.unit == "percent"

    def test_retention_rate_complement_of_churn(self) -> None:
        """Retention + Churn should equal 100%."""
        total = 1000
        lost = 150
        retained = total - lost

        retention = calculate_retention_rate(retained, total)
        churn = calculate_churn_rate(lost, total)

        assert retention.value + churn.value == 100.0

    def test_retention_rate_100_percent(self) -> None:
        """Should handle 100% retention."""
        result = calculate_retention_rate(1000, 1000)
        assert result.value == 100.0


class TestCalculateMRR:
    """Tests para Monthly Recurring Revenue (MRR)."""

    def test_mrr_from_subscriptions(self) -> None:
        """Should calculate MRR from subscription list."""
        subscriptions = [
            {"customer_id": 1, "monthly_amount": 99.0, "status": "active"},
            {"customer_id": 2, "monthly_amount": 199.0, "status": "active"},
            {"customer_id": 3, "monthly_amount": 49.0, "status": "cancelled"},
            {"customer_id": 4, "monthly_amount": 99.0, "status": "active"},
        ]

        result = calculate_mrr(subscriptions)

        assert result.value == 397.0  # 99 + 199 + 99 (excluye cancelled)
        assert result.name == "MRR"

    def test_mrr_empty_list(self) -> None:
        """Should return 0 for empty subscription list."""
        result = calculate_mrr([])
        assert result.value == 0.0

    def test_mrr_all_cancelled(self) -> None:
        """Should return 0 when all subscriptions are cancelled."""
        subscriptions = [
            {"customer_id": 1, "monthly_amount": 99.0, "status": "cancelled"},
        ]

        result = calculate_mrr(subscriptions)
        assert result.value == 0.0


class TestCalculateARR:
    """Tests para Annual Recurring Revenue (ARR)."""

    def test_arr_from_mrr(self) -> None:
        """Should calculate ARR as MRR * 12."""
        mrr = 10000.0

        result = calculate_arr(mrr)

        assert result.value == 120000.0
        assert result.name == "ARR"

    def test_arr_zero(self) -> None:
        """Should return 0 for zero MRR."""
        result = calculate_arr(0.0)
        assert result.value == 0.0


class TestCalculateNRR:
    """Tests para Net Revenue Retention (NRR)."""

    def test_nrr_basic(self) -> None:
        """Should calculate NRR correctly."""
        starting_mrr = 100000.0
        expansion = 15000.0
        contraction = 5000.0
        churn = 8000.0

        result = calculate_nrr(starting_mrr, expansion, contraction, churn)

        # NRR = (100000 - 8000 - 5000 + 15000) / 100000 * 100 = 102%
        assert result.value == 102.0
        assert result.name == "NRR"
        assert result.unit == "percent"

    def test_nrr_above_100_indicates_growth(self) -> None:
        """NRR > 100% indicates net expansion from existing customers."""
        result = calculate_nrr(
            starting_mrr=100000.0,
            expansion=25000.0,
            contraction=2000.0,
            churn=3000.0,
        )

        assert result.value > 100.0  # 120%

    def test_nrr_below_100_indicates_contraction(self) -> None:
        """NRR < 100% indicates net contraction from existing customers."""
        result = calculate_nrr(
            starting_mrr=100000.0,
            expansion=5000.0,
            contraction=10000.0,
            churn=15000.0,
        )

        assert result.value < 100.0  # 80%

    def test_nrr_zero_starting_mrr_raises_error(self) -> None:
        """Should raise ValueError when starting MRR is zero."""
        with pytest.raises(ValueError, match="Starting MRR must be greater than zero"):
            calculate_nrr(0.0, 1000.0, 500.0, 200.0)


class TestKPIResult:
    """Tests para la dataclass KPIResult."""

    def test_kpi_result_creation(self) -> None:
        """Should create KPIResult with all fields."""
        result = KPIResult(
            name="Test KPI",
            value=42.5,
            unit="percent",
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
        )

        assert result.name == "Test KPI"
        assert result.value == 42.5
        assert result.unit == "percent"
        assert result.period_start == date(2024, 1, 1)
        assert result.period_end == date(2024, 1, 31)

    def test_kpi_result_to_dict(self) -> None:
        """Should convert KPIResult to dictionary."""
        result = KPIResult(
            name="Revenue",
            value=100000.0,
            unit="currency",
        )

        d = result.to_dict()

        assert d["name"] == "Revenue"
        assert d["value"] == 100000.0
        assert d["unit"] == "currency"
