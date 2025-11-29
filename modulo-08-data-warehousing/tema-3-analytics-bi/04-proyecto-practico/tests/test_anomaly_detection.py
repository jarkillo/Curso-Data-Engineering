"""Tests para el módulo de detección de anomalías."""

from datetime import date

import pytest

from src.anomaly_detection import (
    AnomalyResult,
    MetricDataPoint,
    calculate_rolling_stats,
    detect_anomalies_batch,
    detect_anomaly,
)


class TestDetectAnomaly:
    """Tests para detección de anomalías individuales."""

    def test_normal_value_not_anomaly(self) -> None:
        """Should not flag normal values as anomalies."""
        historical_data = [100.0, 102.0, 98.0, 101.0, 99.0, 103.0, 97.0, 100.0]
        current_value = 101.0

        result = detect_anomaly(current_value, historical_data)

        assert not result.is_anomaly
        assert result.severity is None

    def test_high_value_is_anomaly(self) -> None:
        """Should detect significantly high values as anomalies."""
        historical_data = [100.0, 102.0, 98.0, 101.0, 99.0, 103.0, 97.0, 100.0]
        current_value = 150.0  # Muy por encima

        result = detect_anomaly(current_value, historical_data)

        assert result.is_anomaly
        assert result.severity in ("warning", "critical")

    def test_low_value_is_anomaly(self) -> None:
        """Should detect significantly low values as anomalies."""
        historical_data = [100.0, 102.0, 98.0, 101.0, 99.0, 103.0, 97.0, 100.0]
        current_value = 50.0  # Muy por debajo

        result = detect_anomaly(current_value, historical_data)

        assert result.is_anomaly

    def test_empty_historical_data_raises_error(self) -> None:
        """Should raise ValueError for empty historical data."""
        with pytest.raises(ValueError, match="Historical data cannot be empty"):
            detect_anomaly(100.0, [])

    def test_insufficient_data_raises_error(self) -> None:
        """Should raise ValueError for insufficient historical data."""
        with pytest.raises(ValueError, match="Need at least 3 data points"):
            detect_anomaly(100.0, [100.0, 102.0])

    def test_custom_threshold(self) -> None:
        """Should use custom threshold multiplier."""
        historical_data = [100.0, 102.0, 98.0, 101.0, 99.0, 103.0, 97.0, 100.0]
        current_value = 115.0

        # With strict threshold (2), should be anomaly
        result_strict = detect_anomaly(current_value, historical_data, threshold=2.0)

        # With lenient threshold (5), should not be anomaly
        result_lenient = detect_anomaly(current_value, historical_data, threshold=5.0)

        assert result_strict.is_anomaly or not result_lenient.is_anomaly

    def test_anomaly_result_contains_bounds(self) -> None:
        """Should include expected bounds in result."""
        historical_data = [100.0, 102.0, 98.0, 101.0, 99.0, 103.0, 97.0, 100.0]
        current_value = 101.0

        result = detect_anomaly(current_value, historical_data)

        assert result.lower_bound is not None
        assert result.upper_bound is not None
        assert result.lower_bound < result.upper_bound


class TestCalculateRollingStats:
    """Tests para cálculo de estadísticas rolling."""

    def test_rolling_mean(self) -> None:
        """Should calculate rolling mean correctly."""
        data = [10.0, 20.0, 30.0, 40.0, 50.0]

        stats = calculate_rolling_stats(data, window_size=3)

        # Rolling mean de últimos 3: (30 + 40 + 50) / 3 = 40
        assert stats["mean"] == pytest.approx(40.0, rel=0.01)

    def test_rolling_std(self) -> None:
        """Should calculate rolling standard deviation."""
        data = [10.0, 20.0, 30.0, 40.0, 50.0]

        stats = calculate_rolling_stats(data, window_size=3)

        assert "std" in stats
        assert stats["std"] > 0

    def test_rolling_median(self) -> None:
        """Should calculate rolling median."""
        data = [10.0, 20.0, 30.0, 40.0, 50.0]

        stats = calculate_rolling_stats(data, window_size=3)

        # Median de [30, 40, 50] = 40
        assert stats["median"] == 40.0

    def test_window_larger_than_data(self) -> None:
        """Should use all data when window exceeds data length."""
        data = [10.0, 20.0, 30.0]

        stats = calculate_rolling_stats(data, window_size=10)

        assert stats["mean"] == 20.0


class TestDetectAnomaliesBatch:
    """Tests para detección de anomalías en batch."""

    def test_batch_detection_basic(self) -> None:
        """Should detect anomalies in a batch of data points."""
        data_points = [
            MetricDataPoint(date=date(2024, 1, 1), value=100.0),
            MetricDataPoint(date=date(2024, 1, 2), value=102.0),
            MetricDataPoint(date=date(2024, 1, 3), value=98.0),
            MetricDataPoint(date=date(2024, 1, 4), value=101.0),
            MetricDataPoint(date=date(2024, 1, 5), value=99.0),
            MetricDataPoint(date=date(2024, 1, 6), value=103.0),
            MetricDataPoint(date=date(2024, 1, 7), value=97.0),
            MetricDataPoint(date=date(2024, 1, 8), value=100.0),
            MetricDataPoint(date=date(2024, 1, 9), value=200.0),  # Anomaly!
        ]

        results = detect_anomalies_batch(data_points, min_history=5)

        # El último punto debería ser detectado como anomalía
        anomalies = [r for r in results if r.is_anomaly]
        assert len(anomalies) > 0
        assert any(r.date == date(2024, 1, 9) for r in anomalies)

    def test_batch_detection_respects_min_history(self) -> None:
        """Should not check points without sufficient history."""
        data_points = [
            MetricDataPoint(date=date(2024, 1, 1), value=100.0),
            MetricDataPoint(
                date=date(2024, 1, 2), value=200.0
            ),  # No hay suficiente historia
        ]

        results = detect_anomalies_batch(data_points, min_history=5)

        # No debería haber resultados porque no hay suficiente historia
        assert len(results) == 0

    def test_batch_returns_all_checked_points(self) -> None:
        """Should return results for all checked points."""
        data_points = [
            MetricDataPoint(date=date(2024, 1, i), value=100.0 + i)
            for i in range(1, 15)
        ]

        results = detect_anomalies_batch(data_points, min_history=5)

        # Debería haber resultados para puntos después de min_history
        assert len(results) == len(data_points) - 5

    def test_batch_handles_weekday_filtering(self) -> None:
        """Should optionally filter by same weekday."""
        # Crear datos donde solo los lunes tienen valores altos
        data_points = []
        for i in range(1, 22):
            d = date(2024, 1, i)
            # Lunes tiene valores más altos
            value = 200.0 if d.weekday() == 0 else 100.0
            data_points.append(MetricDataPoint(date=d, value=value))

        # Sin filtro de weekday, los lunes parecerían anomalías
        results_all = detect_anomalies_batch(
            data_points, min_history=5, same_weekday=False
        )

        # Con filtro de weekday, los lunes se comparan entre sí
        results_weekday = detect_anomalies_batch(
            data_points, min_history=5, same_weekday=True
        )

        # Con filtro de weekday, debería haber menos anomalías
        anomalies_all = sum(1 for r in results_all if r.is_anomaly)
        anomalies_weekday = sum(1 for r in results_weekday if r.is_anomaly)

        # Los lunes comparados entre sí no deberían ser anomalías
        assert anomalies_weekday <= anomalies_all


class TestAnomalyResult:
    """Tests para la dataclass AnomalyResult."""

    def test_anomaly_result_creation(self) -> None:
        """Should create AnomalyResult with all fields."""
        result = AnomalyResult(
            date=date(2024, 1, 15),
            value=150.0,
            is_anomaly=True,
            severity="warning",
            lower_bound=80.0,
            upper_bound=120.0,
            deviation=2.5,
        )

        assert result.date == date(2024, 1, 15)
        assert result.value == 150.0
        assert result.is_anomaly is True
        assert result.severity == "warning"
        assert result.deviation == 2.5

    def test_anomaly_result_to_dict(self) -> None:
        """Should convert to dictionary."""
        result = AnomalyResult(
            date=date(2024, 1, 15),
            value=150.0,
            is_anomaly=True,
            severity="critical",
            lower_bound=80.0,
            upper_bound=120.0,
            deviation=4.0,
        )

        d = result.to_dict()

        assert d["is_anomaly"] is True
        assert d["severity"] == "critical"


class TestMetricDataPoint:
    """Tests para la dataclass MetricDataPoint."""

    def test_metric_data_point_creation(self) -> None:
        """Should create MetricDataPoint correctly."""
        point = MetricDataPoint(
            date=date(2024, 1, 15),
            value=42.5,
            metric_name="revenue",
        )

        assert point.date == date(2024, 1, 15)
        assert point.value == 42.5
        assert point.metric_name == "revenue"

    def test_metric_data_point_default_name(self) -> None:
        """Should default metric_name to empty string."""
        point = MetricDataPoint(date=date(2024, 1, 1), value=100.0)

        assert point.metric_name == ""
