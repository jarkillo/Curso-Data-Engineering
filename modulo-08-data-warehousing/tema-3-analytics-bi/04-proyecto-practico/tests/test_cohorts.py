"""Tests para el módulo de análisis de cohortes."""

from datetime import date

import pytest

from src.cohorts import (
    CohortAnalysis,
    UserEvent,
    build_cohort_table,
    calculate_cohort_ltv,
    calculate_retention_by_cohort,
)


class TestBuildCohortTable:
    """Tests para construcción de tabla de cohortes."""

    def test_build_cohort_table_basic(self) -> None:
        """Should build cohort table from user events."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 5), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 12), event_type="purchase"),
            UserEvent(user_id=2, event_date=date(2024, 1, 10), event_type="signup"),
            UserEvent(user_id=2, event_date=date(2024, 2, 5), event_type="purchase"),
            UserEvent(user_id=3, event_date=date(2024, 2, 1), event_type="signup"),
        ]

        result = build_cohort_table(events, cohort_period="month")

        assert len(result) == 2  # Enero y Febrero
        assert result["2024-01"]["cohort_size"] == 2
        assert result["2024-02"]["cohort_size"] == 1

    def test_build_cohort_table_weekly(self) -> None:
        """Should build weekly cohort table."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=2, event_date=date(2024, 1, 3), event_type="signup"),
            UserEvent(user_id=3, event_date=date(2024, 1, 10), event_type="signup"),
        ]

        result = build_cohort_table(events, cohort_period="week")

        assert len(result) == 2  # 2 semanas diferentes

    def test_build_cohort_table_empty_events(self) -> None:
        """Should return empty dict for no events."""
        result = build_cohort_table([], cohort_period="month")
        assert result == {}

    def test_build_cohort_table_invalid_period_raises_error(self) -> None:
        """Should raise ValueError for invalid period."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
        ]

        with pytest.raises(ValueError, match="Invalid cohort period"):
            build_cohort_table(events, cohort_period="invalid")


class TestCalculateRetentionByCohort:
    """Tests para cálculo de retención por cohorte."""

    def test_retention_d7(self) -> None:
        """Should calculate D7 retention correctly."""
        events = [
            # User 1: signup Jan 1, returns Jan 8 (D7)
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
            # User 2: signup Jan 1, does not return
            UserEvent(user_id=2, event_date=date(2024, 1, 1), event_type="signup"),
            # User 3: signup Jan 1, returns Jan 10 (D9, not D7)
            UserEvent(user_id=3, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=3, event_date=date(2024, 1, 10), event_type="login"),
        ]

        result = calculate_retention_by_cohort(events, retention_days=[7])

        # Only user 1 returned on exactly D7
        assert "2024-01" in result
        assert result["2024-01"]["d7_retention"] == pytest.approx(33.33, rel=0.01)

    def test_retention_multiple_days(self) -> None:
        """Should calculate retention for multiple day intervals."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),  # D7
            UserEvent(
                user_id=1, event_date=date(2024, 1, 31), event_type="login"
            ),  # D30
            UserEvent(user_id=2, event_date=date(2024, 1, 1), event_type="signup"),
        ]

        result = calculate_retention_by_cohort(events, retention_days=[7, 30])

        assert "d7_retention" in result["2024-01"]
        assert "d30_retention" in result["2024-01"]

    def test_retention_100_percent(self) -> None:
        """Should handle 100% retention."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
        ]

        result = calculate_retention_by_cohort(events, retention_days=[7])

        assert result["2024-01"]["d7_retention"] == 100.0

    def test_retention_zero_percent(self) -> None:
        """Should handle 0% retention."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            # No return events
        ]

        result = calculate_retention_by_cohort(events, retention_days=[7])

        assert result["2024-01"]["d7_retention"] == 0.0


class TestCalculateCohortLTV:
    """Tests para cálculo de LTV por cohorte."""

    def test_cohort_ltv_basic(self) -> None:
        """Should calculate LTV per cohort."""
        events = [
            # User 1: signup Jan, spends $100 + $50
            UserEvent(
                user_id=1,
                event_date=date(2024, 1, 1),
                event_type="signup",
                revenue=0,
            ),
            UserEvent(
                user_id=1,
                event_date=date(2024, 1, 15),
                event_type="purchase",
                revenue=100.0,
            ),
            UserEvent(
                user_id=1,
                event_date=date(2024, 2, 15),
                event_type="purchase",
                revenue=50.0,
            ),
            # User 2: signup Jan, spends $200
            UserEvent(
                user_id=2,
                event_date=date(2024, 1, 5),
                event_type="signup",
                revenue=0,
            ),
            UserEvent(
                user_id=2,
                event_date=date(2024, 1, 20),
                event_type="purchase",
                revenue=200.0,
            ),
        ]

        result = calculate_cohort_ltv(events)

        # Jan cohort: (150 + 200) / 2 = $175 avg LTV
        assert result["2024-01"]["avg_ltv"] == 175.0
        assert result["2024-01"]["total_revenue"] == 350.0
        assert result["2024-01"]["cohort_size"] == 2

    def test_cohort_ltv_no_revenue(self) -> None:
        """Should handle cohort with no revenue."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
        ]

        result = calculate_cohort_ltv(events)

        assert result["2024-01"]["avg_ltv"] == 0.0
        assert result["2024-01"]["total_revenue"] == 0.0

    def test_cohort_ltv_multiple_cohorts(self) -> None:
        """Should calculate LTV for multiple cohorts separately."""
        events = [
            UserEvent(
                user_id=1, event_date=date(2024, 1, 1), event_type="signup", revenue=0
            ),
            UserEvent(
                user_id=1,
                event_date=date(2024, 1, 10),
                event_type="purchase",
                revenue=100.0,
            ),
            UserEvent(
                user_id=2, event_date=date(2024, 2, 1), event_type="signup", revenue=0
            ),
            UserEvent(
                user_id=2,
                event_date=date(2024, 2, 10),
                event_type="purchase",
                revenue=200.0,
            ),
        ]

        result = calculate_cohort_ltv(events)

        assert result["2024-01"]["avg_ltv"] == 100.0
        assert result["2024-02"]["avg_ltv"] == 200.0


class TestCohortAnalysis:
    """Tests para la clase CohortAnalysis."""

    def test_cohort_analysis_from_events(self) -> None:
        """Should create CohortAnalysis from events."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
        ]

        analysis = CohortAnalysis.from_events(events)

        assert len(analysis.cohorts) > 0

    def test_cohort_analysis_get_retention_matrix(self) -> None:
        """Should return retention matrix."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
            UserEvent(user_id=2, event_date=date(2024, 2, 1), event_type="signup"),
            UserEvent(user_id=2, event_date=date(2024, 2, 8), event_type="login"),
        ]

        analysis = CohortAnalysis.from_events(events, retention_days=[7, 14, 30])
        matrix = analysis.get_retention_matrix()

        assert "2024-01" in matrix
        assert "d7_retention" in matrix["2024-01"]

    def test_cohort_analysis_to_dataframe(self) -> None:
        """Should convert to pandas DataFrame."""
        events = [
            UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
            UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
        ]

        analysis = CohortAnalysis.from_events(events)
        df = analysis.to_dataframe()

        assert "cohort" in df.columns
        assert "cohort_size" in df.columns


class TestUserEvent:
    """Tests para la dataclass UserEvent."""

    def test_user_event_creation(self) -> None:
        """Should create UserEvent with all fields."""
        event = UserEvent(
            user_id=1,
            event_date=date(2024, 1, 15),
            event_type="purchase",
            revenue=99.99,
        )

        assert event.user_id == 1
        assert event.event_date == date(2024, 1, 15)
        assert event.event_type == "purchase"
        assert event.revenue == 99.99

    def test_user_event_default_revenue(self) -> None:
        """Should default revenue to 0."""
        event = UserEvent(
            user_id=1,
            event_date=date(2024, 1, 1),
            event_type="signup",
        )

        assert event.revenue == 0.0
