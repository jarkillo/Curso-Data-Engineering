"""
Módulo de detección de anomalías en métricas.

Este módulo proporciona funciones para detectar valores anómalos
en series temporales de métricas, utilizando métodos estadísticos robustos.

Funciones principales:
- detect_anomaly: Detecta si un valor es anómalo
- calculate_rolling_stats: Calcula estadísticas rolling
- detect_anomalies_batch: Detecta anomalías en un batch de datos
"""

from dataclasses import asdict, dataclass
from datetime import date
from statistics import mean, median, stdev
from typing import Any


@dataclass
class MetricDataPoint:
    """
    Punto de datos de una métrica.

    Attributes:
        date: Fecha del punto de datos
        value: Valor de la métrica
        metric_name: Nombre de la métrica (opcional)

    Examples:
        >>> point = MetricDataPoint(date=date(2024, 1, 15), value=42.5)
    """

    date: date
    value: float
    metric_name: str = ""


@dataclass
class AnomalyResult:
    """
    Resultado de detección de anomalía.

    Attributes:
        date: Fecha del punto analizado
        value: Valor actual
        is_anomaly: Si es una anomalía
        severity: Severidad ('warning', 'critical', None)
        lower_bound: Límite inferior esperado
        upper_bound: Límite superior esperado
        deviation: Desviación del valor esperado (en MADs o std)

    Examples:
        >>> result = AnomalyResult(
        ...     date=date(2024, 1, 15),
        ...     value=150.0,
        ...     is_anomaly=True,
        ...     severity="warning",
        ...     lower_bound=80.0,
        ...     upper_bound=120.0,
        ...     deviation=2.5
        ... )
    """

    date: date
    value: float
    is_anomaly: bool
    severity: str | None
    lower_bound: float
    upper_bound: float
    deviation: float

    def to_dict(self) -> dict[str, Any]:
        """Convierte el resultado a diccionario."""
        return asdict(self)


def calculate_rolling_stats(
    data: list[float], window_size: int = 7
) -> dict[str, float]:
    """
    Calcula estadísticas rolling sobre una ventana de datos.

    Args:
        data: Lista de valores históricos
        window_size: Tamaño de la ventana (default 7)

    Returns:
        Diccionario con mean, std, median, min, max

    Examples:
        >>> stats = calculate_rolling_stats([10, 20, 30, 40, 50], window_size=3)
        >>> stats["mean"]
        40.0
    """
    # Use last window_size elements, or all if fewer
    window = data[-window_size:] if len(data) >= window_size else data

    if len(window) < 2:
        return {
            "mean": window[0] if window else 0.0,
            "std": 0.0,
            "median": window[0] if window else 0.0,
            "min": window[0] if window else 0.0,
            "max": window[0] if window else 0.0,
        }

    return {
        "mean": mean(window),
        "std": stdev(window) if len(window) > 1 else 0.0,
        "median": median(window),
        "min": min(window),
        "max": max(window),
    }


def _calculate_mad(data: list[float]) -> float:
    """
    Calcula Median Absolute Deviation (MAD).

    MAD es más robusto que la desviación estándar ante outliers.

    Args:
        data: Lista de valores

    Returns:
        MAD value
    """
    if len(data) < 2:
        return 0.0

    med = median(data)
    deviations = [abs(x - med) for x in data]
    return median(deviations)


def detect_anomaly(
    current_value: float,
    historical_data: list[float],
    threshold: float = 3.0,
    use_mad: bool = True,
) -> AnomalyResult:
    """
    Detecta si un valor es anómalo basándose en datos históricos.

    Utiliza MAD (Median Absolute Deviation) por defecto, que es más robusto
    que la desviación estándar ante outliers existentes.

    Args:
        current_value: Valor actual a evaluar
        historical_data: Lista de valores históricos
        threshold: Multiplicador para determinar anomalía (default 3.0)
        use_mad: Si usar MAD en lugar de std (default True)

    Returns:
        AnomalyResult con detalles de la detección

    Raises:
        ValueError: Si historical_data está vacío o tiene menos de 3 elementos

    Examples:
        >>> historical = [100, 102, 98, 101, 99, 103, 97, 100]
        >>> result = detect_anomaly(150.0, historical)
        >>> result.is_anomaly
        True
    """
    if not historical_data:
        raise ValueError("Historical data cannot be empty")
    if len(historical_data) < 3:
        raise ValueError("Need at least 3 data points for anomaly detection")

    med = median(historical_data)

    if use_mad:
        # Use MAD with normalization factor for consistency with std
        mad = _calculate_mad(historical_data)
        # 1.4826 normalizes MAD to be comparable to std for normal distributions
        normalized_scale = mad * 1.4826 if mad > 0 else 0.0
    else:
        normalized_scale = stdev(historical_data)

    # Handle case where all values are identical
    if normalized_scale == 0:
        is_anomaly = current_value != med
        deviation = float("inf") if is_anomaly else 0.0
    else:
        deviation = abs(current_value - med) / normalized_scale
        is_anomaly = deviation > threshold

    # Calculate bounds
    bound_range = threshold * normalized_scale if normalized_scale > 0 else 0.0
    lower_bound = med - bound_range
    upper_bound = med + bound_range

    # Determine severity
    severity: str | None = None
    if is_anomaly:
        if deviation > threshold * 1.5:
            severity = "critical"
        else:
            severity = "warning"

    return AnomalyResult(
        date=date.today(),  # Will be overwritten in batch processing
        value=current_value,
        is_anomaly=is_anomaly,
        severity=severity,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        deviation=deviation,
    )


def detect_anomalies_batch(
    data_points: list[MetricDataPoint],
    min_history: int = 5,
    threshold: float = 3.0,
    same_weekday: bool = False,
) -> list[AnomalyResult]:
    """
    Detecta anomalías en un batch de puntos de datos.

    Args:
        data_points: Lista de puntos de datos ordenados por fecha
        min_history: Mínimo de puntos históricos necesarios
        threshold: Multiplicador para determinar anomalía
        same_weekday: Si True, solo compara con el mismo día de la semana

    Returns:
        Lista de AnomalyResult para cada punto evaluado

    Examples:
        >>> points = [
        ...     MetricDataPoint(date=date(2024, 1, i), value=100.0)
        ...     for i in range(1, 10)
        ... ]
        >>> results = detect_anomalies_batch(points, min_history=5)
    """
    # Sort by date
    sorted_points = sorted(data_points, key=lambda p: p.date)

    results: list[AnomalyResult] = []

    for i, point in enumerate(sorted_points):
        # Get historical data before this point
        if same_weekday:
            # Only use points from same weekday
            target_weekday = point.date.weekday()
            historical = [
                p.value for p in sorted_points[:i] if p.date.weekday() == target_weekday
            ]
        else:
            historical = [p.value for p in sorted_points[:i]]

        # Skip if insufficient history
        if len(historical) < min_history:
            continue

        # Detect anomaly
        anomaly_result = detect_anomaly(point.value, historical, threshold=threshold)

        # Update date in result
        result = AnomalyResult(
            date=point.date,
            value=anomaly_result.value,
            is_anomaly=anomaly_result.is_anomaly,
            severity=anomaly_result.severity,
            lower_bound=anomaly_result.lower_bound,
            upper_bound=anomaly_result.upper_bound,
            deviation=anomaly_result.deviation,
        )
        results.append(result)

    return results
