"""Módulo para recolección de métricas del pipeline."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PipelineMetrics:
    """Métricas de ejecución del pipeline."""

    start_time: datetime
    end_time: Optional[datetime] = None
    rows_extracted: int = 0
    rows_validated: int = 0
    rows_loaded: int = 0
    rows_failed: int = 0
    duration_seconds: float = 0.0
    success: bool = False
    error_message: str = ""

    def finalize(self) -> None:
        """Finaliza métricas calculando duración."""
        self.end_time = datetime.now()
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> dict:
        """Convierte métricas a diccionario."""
        data = asdict(self)
        # Convertir datetimes a ISO format
        data["start_time"] = self.start_time.isoformat()
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
        return data


def calcular_throughput(rows: int, duration_seconds: float) -> float:
    """
    Calcula throughput (filas/segundo).

    Args:
        rows: Número de filas procesadas
        duration_seconds: Duración en segundos

    Returns:
        Throughput (filas/segundo)

    Examples:
        >>> calcular_throughput(1000, 10.0)
        100.0
    """
    if duration_seconds == 0:
        return 0.0
    return round(rows / duration_seconds, 2)


def exportar_metricas_json(metricas: PipelineMetrics, archivo: str) -> None:
    """
    Exporta métricas a archivo JSON.

    Args:
        metricas: Métricas del pipeline
        archivo: Ruta al archivo de salida

    Examples:
        >>> metricas = PipelineMetrics(start_time=datetime.now())
        >>> metricas.finalize()
        >>> exportar_metricas_json(metricas, "metricas.json")
    """
    Path(archivo).write_text(json.dumps(metricas.to_dict(), indent=2))
