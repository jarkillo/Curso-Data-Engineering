"""
Módulo de análisis de cohortes.

Este módulo proporciona funciones para realizar análisis de cohortes,
incluyendo retención, LTV por cohorte, y visualización de matrices de cohorte.

Funciones principales:
- build_cohort_table: Construye tabla de cohortes a partir de eventos
- calculate_retention_by_cohort: Calcula retención por cohorte
- calculate_cohort_ltv: Calcula LTV por cohorte
- CohortAnalysis: Clase para análisis completo de cohortes
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Any

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


@dataclass
class UserEvent:
    """
    Evento de usuario para análisis de cohortes.

    Attributes:
        user_id: Identificador único del usuario
        event_date: Fecha del evento
        event_type: Tipo de evento ('signup', 'login', 'purchase', etc.)
        revenue: Ingresos asociados al evento (default 0.0)

    Examples:
        >>> event = UserEvent(user_id=1, event_date=date(2024, 1, 15),
        ...                   event_type="purchase", revenue=99.99)
    """

    user_id: int
    event_date: date
    event_type: str
    revenue: float = 0.0


def _get_cohort_key(event_date: date, period: str) -> str:
    """
    Genera la clave de cohorte basada en el periodo.

    Args:
        event_date: Fecha del evento
        period: Periodo de cohorte ('week', 'month')

    Returns:
        Clave de cohorte como string (ej: '2024-01', '2024-W01')
    """
    if period == "month":
        return event_date.strftime("%Y-%m")
    elif period == "week":
        # ISO week number
        iso_calendar = event_date.isocalendar()
        return f"{iso_calendar.year}-W{iso_calendar.week:02d}"
    else:
        raise ValueError(f"Invalid cohort period: {period}. Use 'week' or 'month'.")


def build_cohort_table(
    events: list[UserEvent], cohort_period: str = "month"
) -> dict[str, dict[str, Any]]:
    """
    Construye una tabla de cohortes a partir de eventos de usuario.

    Agrupa usuarios por su fecha de registro (signup) en cohortes
    semanales o mensuales.

    Args:
        events: Lista de eventos de usuario
        cohort_period: Periodo de cohorte ('week' o 'month')

    Returns:
        Diccionario con cohortes y sus métricas básicas

    Raises:
        ValueError: Si cohort_period no es válido

    Examples:
        >>> events = [
        ...     UserEvent(user_id=1, event_date=date(2024, 1, 5),
        ...               event_type="signup"),
        ...     UserEvent(user_id=2, event_date=date(2024, 1, 10),
        ...               event_type="signup"),
        ... ]
        >>> result = build_cohort_table(events, cohort_period="month")
        >>> result["2024-01"]["cohort_size"]
        2
    """
    if not events:
        return {}

    # Validate period
    if cohort_period not in ("week", "month"):
        raise ValueError(
            f"Invalid cohort period: {cohort_period}. Use 'week' or 'month'."
        )

    # Find signup events to determine cohorts
    user_cohorts: dict[int, str] = {}
    cohort_users: dict[str, set[int]] = defaultdict(set)

    for event in events:
        if event.event_type == "signup":
            cohort_key = _get_cohort_key(event.event_date, cohort_period)
            user_cohorts[event.user_id] = cohort_key
            cohort_users[cohort_key].add(event.user_id)

    # Build result table
    result: dict[str, dict[str, Any]] = {}
    for cohort_key in sorted(cohort_users.keys()):
        result[cohort_key] = {
            "cohort_size": len(cohort_users[cohort_key]),
            "users": cohort_users[cohort_key],
        }

    return result


def calculate_retention_by_cohort(
    events: list[UserEvent],
    retention_days: list[int] | None = None,
    cohort_period: str = "month",
) -> dict[str, dict[str, Any]]:
    """
    Calcula tasas de retención por cohorte para diferentes intervalos de días.

    Args:
        events: Lista de eventos de usuario
        retention_days: Lista de días para calcular retención (default [7, 14, 30])
        cohort_period: Periodo de cohorte ('week' o 'month')

    Returns:
        Diccionario con cohortes y sus tasas de retención

    Examples:
        >>> events = [
        ...     UserEvent(user_id=1, event_date=date(2024, 1, 1),
        ...               event_type="signup"),
        ...     UserEvent(user_id=1, event_date=date(2024, 1, 8),
        ...               event_type="login"),
        ... ]
        >>> result = calculate_retention_by_cohort(events, retention_days=[7])
        >>> result["2024-01"]["d7_retention"]
        100.0
    """
    if retention_days is None:
        retention_days = [7, 14, 30]

    # First, build cohort table and get user signup dates
    user_signup_dates: dict[int, date] = {}
    cohort_users: dict[str, set[int]] = defaultdict(set)

    for event in events:
        if event.event_type == "signup":
            cohort_key = _get_cohort_key(event.event_date, cohort_period)
            user_signup_dates[event.user_id] = event.event_date
            cohort_users[cohort_key].add(event.user_id)

    # Track which users returned on each retention day
    user_return_days: dict[int, set[int]] = defaultdict(set)

    for event in events:
        if event.event_type != "signup" and event.user_id in user_signup_dates:
            signup_date = user_signup_dates[event.user_id]
            days_since_signup = (event.event_date - signup_date).days

            # Check if this matches any retention day
            for ret_day in retention_days:
                if days_since_signup == ret_day:
                    user_return_days[event.user_id].add(ret_day)

    # Calculate retention rates per cohort
    result: dict[str, dict[str, Any]] = {}

    for cohort_key in sorted(cohort_users.keys()):
        users = cohort_users[cohort_key]
        cohort_size = len(users)

        cohort_data: dict[str, Any] = {
            "cohort_size": cohort_size,
        }

        for ret_day in retention_days:
            # Count users from this cohort who returned on this day
            returned_count = sum(
                1 for user_id in users if ret_day in user_return_days[user_id]
            )

            retention_pct = (
                (returned_count / cohort_size * 100) if cohort_size > 0 else 0.0
            )
            cohort_data[f"d{ret_day}_retention"] = round(retention_pct, 2)

        result[cohort_key] = cohort_data

    return result


def calculate_cohort_ltv(
    events: list[UserEvent], cohort_period: str = "month"
) -> dict[str, dict[str, Any]]:
    """
    Calcula el LTV por cohorte.

    Args:
        events: Lista de eventos de usuario (debe incluir signups y purchases)
        cohort_period: Periodo de cohorte ('week' o 'month')

    Returns:
        Diccionario con cohortes y sus métricas de LTV

    Examples:
        >>> events = [
        ...     UserEvent(user_id=1, event_date=date(2024, 1, 1),
        ...               event_type="signup", revenue=0),
        ...     UserEvent(user_id=1, event_date=date(2024, 1, 15),
        ...               event_type="purchase", revenue=100.0),
        ... ]
        >>> result = calculate_cohort_ltv(events)
        >>> result["2024-01"]["avg_ltv"]
        100.0
    """
    # Build user cohort mapping
    user_cohorts: dict[int, str] = {}
    cohort_users: dict[str, set[int]] = defaultdict(set)

    for event in events:
        if event.event_type == "signup":
            cohort_key = _get_cohort_key(event.event_date, cohort_period)
            user_cohorts[event.user_id] = cohort_key
            cohort_users[cohort_key].add(event.user_id)

    # Calculate revenue per user (includes negative revenue for refunds/chargebacks)
    user_revenue: dict[int, float] = defaultdict(float)

    for event in events:
        if event.user_id in user_cohorts:
            user_revenue[event.user_id] += event.revenue

    # Aggregate by cohort
    result: dict[str, dict[str, Any]] = {}

    for cohort_key in sorted(cohort_users.keys()):
        users = cohort_users[cohort_key]
        cohort_size = len(users)

        total_revenue = sum(user_revenue[user_id] for user_id in users)
        avg_ltv = total_revenue / cohort_size if cohort_size > 0 else 0.0

        result[cohort_key] = {
            "cohort_size": cohort_size,
            "total_revenue": total_revenue,
            "avg_ltv": avg_ltv,
        }

    return result


class CohortAnalysis:
    """
    Clase para análisis completo de cohortes.

    Proporciona métodos para analizar retención, LTV, y generar
    visualizaciones de cohortes.

    Attributes:
        events: Lista de eventos de usuario
        cohorts: Diccionario de cohortes construidas
        retention_days: Días para análisis de retención
    """

    def __init__(
        self,
        events: list[UserEvent],
        cohort_period: str = "month",
        retention_days: list[int] | None = None,
    ):
        """
        Inicializa el análisis de cohortes.

        Args:
            events: Lista de eventos de usuario
            cohort_period: Periodo de cohorte ('week' o 'month')
            retention_days: Días para análisis de retención
        """
        self.events = events
        self.cohort_period = cohort_period
        self.retention_days = retention_days or [7, 14, 30]
        self.cohorts = build_cohort_table(events, cohort_period)
        self._retention_matrix: dict[str, dict[str, Any]] | None = None
        self._ltv_data: dict[str, dict[str, Any]] | None = None

    @classmethod
    def from_events(
        cls,
        events: list[UserEvent],
        cohort_period: str = "month",
        retention_days: list[int] | None = None,
    ) -> "CohortAnalysis":
        """
        Crea instancia de CohortAnalysis desde eventos.

        Args:
            events: Lista de eventos de usuario
            cohort_period: Periodo de cohorte
            retention_days: Días para análisis de retención

        Returns:
            Instancia de CohortAnalysis
        """
        return cls(events, cohort_period, retention_days)

    def get_retention_matrix(self) -> dict[str, dict[str, Any]]:
        """
        Obtiene la matriz de retención por cohorte.

        Returns:
            Diccionario con cohortes y sus tasas de retención
        """
        if self._retention_matrix is None:
            self._retention_matrix = calculate_retention_by_cohort(
                self.events, self.retention_days, self.cohort_period
            )
        return self._retention_matrix

    def get_ltv_analysis(self) -> dict[str, dict[str, Any]]:
        """
        Obtiene el análisis de LTV por cohorte.

        Returns:
            Diccionario con cohortes y sus métricas de LTV
        """
        if self._ltv_data is None:
            self._ltv_data = calculate_cohort_ltv(self.events, self.cohort_period)
        return self._ltv_data

    def to_dataframe(self) -> Any:
        """
        Convierte el análisis a DataFrame de pandas.

        Returns:
            DataFrame con datos de cohortes

        Raises:
            ImportError: Si pandas no está instalado
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for to_dataframe()")

        retention = self.get_retention_matrix()
        ltv = self.get_ltv_analysis()

        rows = []
        for cohort_key in retention:
            row = {"cohort": cohort_key}
            row.update(retention[cohort_key])
            if cohort_key in ltv:
                row["avg_ltv"] = ltv[cohort_key]["avg_ltv"]
                row["total_revenue"] = ltv[cohort_key]["total_revenue"]
            rows.append(row)

        return pd.DataFrame(rows)
