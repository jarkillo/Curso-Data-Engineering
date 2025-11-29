"""Tests para el módulo de exportación de métricas."""

import json
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from src.exporters import (
    MetricDefinition,
    create_metric_definition,
    export_to_csv,
    export_to_json,
)
from src.kpis import KPIResult


class TestExportToJSON:
    """Tests para exportación a JSON."""

    def test_export_kpi_results(self) -> None:
        """Should export KPI results to JSON."""
        kpis = [
            KPIResult(name="AOV", value=45.50, unit="currency"),
            KPIResult(name="Conversion Rate", value=3.2, unit="percent"),
        ]

        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics.json"
            export_to_json(kpis, output_path)

            assert output_path.exists()

            with open(output_path) as f:
                data = json.load(f)

            assert len(data) == 2
            assert data[0]["name"] == "AOV"
            assert data[0]["value"] == 45.50

    def test_export_with_metadata(self) -> None:
        """Should include metadata in export."""
        kpis = [KPIResult(name="Revenue", value=100000.0, unit="currency")]

        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics.json"
            metadata = {
                "dashboard": "Executive",
                "generated_at": "2024-03-15T10:00:00Z",
            }
            export_to_json(kpis, output_path, metadata=metadata)

            with open(output_path) as f:
                data = json.load(f)

            assert "metadata" in data
            assert data["metadata"]["dashboard"] == "Executive"

    def test_export_empty_list(self) -> None:
        """Should handle empty list."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "empty.json"
            export_to_json([], output_path)

            with open(output_path) as f:
                data = json.load(f)

            assert data == []


class TestExportToCSV:
    """Tests para exportación a CSV."""

    def test_export_kpi_results(self) -> None:
        """Should export KPI results to CSV."""
        kpis = [
            KPIResult(name="AOV", value=45.50, unit="currency"),
            KPIResult(name="Conversion Rate", value=3.2, unit="percent"),
        ]

        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics.csv"
            export_to_csv(kpis, output_path)

            assert output_path.exists()

            with open(output_path) as f:
                lines = f.readlines()

            # Header + 2 data rows
            assert len(lines) == 3
            assert "name" in lines[0]
            assert "AOV" in lines[1]

    def test_export_with_period(self) -> None:
        """Should include period dates in CSV."""
        kpis = [
            KPIResult(
                name="Revenue",
                value=100000.0,
                unit="currency",
                period_start=date(2024, 1, 1),
                period_end=date(2024, 1, 31),
            ),
        ]

        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics.csv"
            export_to_csv(kpis, output_path)

            with open(output_path) as f:
                content = f.read()

            assert "2024-01-01" in content
            assert "2024-01-31" in content

    def test_export_empty_list(self) -> None:
        """Should create file with only header for empty list."""
        with TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "empty.csv"
            export_to_csv([], output_path)

            assert output_path.exists()


class TestMetricDefinition:
    """Tests para definición de métricas."""

    def test_create_metric_definition(self) -> None:
        """Should create metric definition."""
        definition = create_metric_definition(
            name="MRR",
            description="Monthly Recurring Revenue",
            formula="SUM(monthly_amount) WHERE status = 'active'",
            unit="currency",
            owner="Finance Team",
        )

        assert definition.name == "MRR"
        assert definition.description == "Monthly Recurring Revenue"
        assert definition.unit == "currency"

    def test_metric_definition_to_dict(self) -> None:
        """Should convert definition to dictionary."""
        definition = MetricDefinition(
            name="CAC",
            description="Customer Acquisition Cost",
            formula="marketing_spend / new_customers",
            unit="currency",
            owner="Marketing",
            source_table="analytics.cac_daily",
        )

        d = definition.to_dict()

        assert d["name"] == "CAC"
        assert d["source_table"] == "analytics.cac_daily"

    def test_metric_definition_to_yaml(self) -> None:
        """Should convert definition to YAML format."""
        definition = MetricDefinition(
            name="Churn Rate",
            description="Monthly customer churn rate",
            formula="lost_customers / total_customers * 100",
            unit="percent",
            owner="Success Team",
        )

        yaml_str = definition.to_yaml()

        assert "name: Churn Rate" in yaml_str
        assert "unit: percent" in yaml_str

    def test_metric_definition_with_thresholds(self) -> None:
        """Should include thresholds in definition."""
        definition = MetricDefinition(
            name="NPS",
            description="Net Promoter Score",
            formula="promoters - detractors",
            unit="score",
            owner="Product",
            thresholds={
                "green": {"min": 50},
                "yellow": {"min": 30, "max": 50},
                "red": {"max": 30},
            },
        )

        assert definition.thresholds is not None
        assert definition.thresholds["green"]["min"] == 50
