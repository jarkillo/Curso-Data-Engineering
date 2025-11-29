"""
Módulo de exportación de métricas para herramientas de BI.

Este módulo proporciona funciones para exportar métricas y KPIs
a diferentes formatos para consumo por herramientas de BI.

Formatos soportados:
- JSON: Para APIs y dashboards dinámicos
- CSV: Para análisis en Excel/Google Sheets
- YAML: Para documentación de métricas
"""

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from src.kpis import KPIResult


@dataclass
class MetricDefinition:
    """
    Definición formal de una métrica.

    Documenta todos los aspectos de una métrica para asegurar
    consistencia en su cálculo e interpretación.

    Attributes:
        name: Nombre de la métrica
        description: Descripción detallada
        formula: Fórmula de cálculo
        unit: Unidad de medida
        owner: Equipo responsable
        source_table: Tabla fuente en el DWH
        refresh_frequency: Frecuencia de actualización
        thresholds: Umbrales de alerta (green/yellow/red)

    Examples:
        >>> definition = MetricDefinition(
        ...     name="MRR",
        ...     description="Monthly Recurring Revenue",
        ...     formula="SUM(monthly_amount) WHERE status = 'active'",
        ...     unit="currency",
        ...     owner="Finance Team"
        ... )
    """

    name: str
    description: str
    formula: str
    unit: str
    owner: str
    source_table: str = ""
    refresh_frequency: str = "daily"
    thresholds: dict[str, dict[str, float]] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convierte la definición a diccionario."""
        return asdict(self)

    def to_yaml(self) -> str:
        """
        Convierte la definición a formato YAML.

        Returns:
            String en formato YAML
        """
        lines = [
            f"name: {self.name}",
            f"description: {self.description}",
            f"formula: {self.formula}",
            f"unit: {self.unit}",
            f"owner: {self.owner}",
        ]

        if self.source_table:
            lines.append(f"source_table: {self.source_table}")

        lines.append(f"refresh_frequency: {self.refresh_frequency}")

        if self.thresholds:
            lines.append("thresholds:")
            for level, values in self.thresholds.items():
                lines.append(f"  {level}:")
                for key, val in values.items():
                    lines.append(f"    {key}: {val}")

        return "\n".join(lines)


def create_metric_definition(
    name: str,
    description: str,
    formula: str,
    unit: str,
    owner: str,
    source_table: str = "",
    refresh_frequency: str = "daily",
    thresholds: dict[str, dict[str, float]] | None = None,
) -> MetricDefinition:
    """
    Crea una definición de métrica.

    Args:
        name: Nombre de la métrica
        description: Descripción detallada
        formula: Fórmula de cálculo
        unit: Unidad de medida
        owner: Equipo responsable
        source_table: Tabla fuente en el DWH
        refresh_frequency: Frecuencia de actualización
        thresholds: Umbrales de alerta

    Returns:
        MetricDefinition configurada

    Examples:
        >>> definition = create_metric_definition(
        ...     name="CAC",
        ...     description="Customer Acquisition Cost",
        ...     formula="marketing_spend / new_customers",
        ...     unit="currency",
        ...     owner="Marketing"
        ... )
    """
    return MetricDefinition(
        name=name,
        description=description,
        formula=formula,
        unit=unit,
        owner=owner,
        source_table=source_table,
        refresh_frequency=refresh_frequency,
        thresholds=thresholds,
    )


def export_to_json(
    kpis: list[KPIResult],
    output_path: Path | str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """
    Exporta KPIs a formato JSON.

    Args:
        kpis: Lista de KPIResult a exportar
        output_path: Ruta del archivo de salida
        metadata: Metadatos adicionales (opcional)

    Examples:
        >>> kpis = [KPIResult(name="AOV", value=45.50, unit="currency")]
        >>> export_to_json(kpis, Path("metrics.json"))
    """
    output_path = Path(output_path)

    # Convert KPIs to dictionaries
    kpi_data = []
    for kpi in kpis:
        kpi_dict = kpi.to_dict()
        # Convert date objects to strings
        if kpi_dict.get("period_start"):
            kpi_dict["period_start"] = str(kpi_dict["period_start"])
        if kpi_dict.get("period_end"):
            kpi_dict["period_end"] = str(kpi_dict["period_end"])
        kpi_data.append(kpi_dict)

    # Add metadata if provided
    if metadata:
        output = {
            "metadata": metadata,
            "kpis": kpi_data,
        }
    else:
        output = kpi_data

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def export_to_csv(
    kpis: list[KPIResult],
    output_path: Path | str,
) -> None:
    """
    Exporta KPIs a formato CSV.

    Args:
        kpis: Lista de KPIResult a exportar
        output_path: Ruta del archivo de salida

    Examples:
        >>> kpis = [KPIResult(name="Revenue", value=100000.0, unit="currency")]
        >>> export_to_csv(kpis, Path("metrics.csv"))
    """
    output_path = Path(output_path)

    fieldnames = ["name", "value", "unit", "period_start", "period_end"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for kpi in kpis:
            row = {
                "name": kpi.name,
                "value": kpi.value,
                "unit": kpi.unit,
                "period_start": str(kpi.period_start) if kpi.period_start else "",
                "period_end": str(kpi.period_end) if kpi.period_end else "",
            }
            writer.writerow(row)
