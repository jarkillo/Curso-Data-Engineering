"""
Módulo de cálculo de KPIs de negocio.

Este módulo proporciona funciones para calcular métricas clave de rendimiento
utilizadas en dashboards de Analytics y Business Intelligence.

Funciones principales:
- calculate_aov: Average Order Value
- calculate_conversion_rate: Tasa de conversión
- calculate_cac: Customer Acquisition Cost
- calculate_ltv: Customer Lifetime Value
- calculate_churn_rate: Tasa de abandono
- calculate_retention_rate: Tasa de retención
- calculate_mrr: Monthly Recurring Revenue
- calculate_arr: Annual Recurring Revenue
- calculate_nrr: Net Revenue Retention
"""

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass
class KPIResult:
    """
    Resultado de cálculo de un KPI.

    Attributes:
        name: Nombre del KPI
        value: Valor calculado
        unit: Unidad de medida ('currency', 'percent', 'count', 'ratio')
        period_start: Inicio del periodo de cálculo (opcional)
        period_end: Fin del periodo de cálculo (opcional)

    Examples:
        >>> result = KPIResult(name="AOV", value=45.50, unit="currency")
        >>> result.value
        45.5
    """

    name: str
    value: float
    unit: str
    period_start: date | None = None
    period_end: date | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte el KPIResult a diccionario.

        Returns:
            Diccionario con los campos del KPI.
        """
        return asdict(self)


def calculate_aov(total_revenue: float, total_orders: int) -> KPIResult:
    """
    Calcula el Average Order Value (AOV).

    AOV = Total Revenue / Total Orders

    Args:
        total_revenue: Ingresos totales del periodo
        total_orders: Número total de pedidos

    Returns:
        KPIResult con el valor del AOV

    Raises:
        ValueError: Si total_orders <= 0 o total_revenue < 0

    Examples:
        >>> result = calculate_aov(10000.0, 200)
        >>> result.value
        50.0
    """
    if total_orders <= 0:
        raise ValueError("Total orders must be greater than zero")
    if total_revenue < 0:
        raise ValueError("Total revenue cannot be negative")

    aov = total_revenue / total_orders

    return KPIResult(name="AOV", value=aov, unit="currency")


def calculate_conversion_rate(conversions: int, total_visitors: int) -> KPIResult:
    """
    Calcula la tasa de conversión.

    Conversion Rate = (Conversions / Total Visitors) * 100

    Args:
        conversions: Número de conversiones
        total_visitors: Total de visitantes

    Returns:
        KPIResult con la tasa de conversión en porcentaje

    Raises:
        ValueError: Si total_visitors <= 0 o conversions > total_visitors

    Examples:
        >>> result = calculate_conversion_rate(50, 1000)
        >>> result.value
        5.0
    """
    if total_visitors <= 0:
        raise ValueError("Total visitors must be greater than zero")
    if conversions > total_visitors:
        raise ValueError("Conversions cannot exceed total visitors")
    if conversions < 0:
        raise ValueError("Conversions cannot be negative")

    rate = (conversions / total_visitors) * 100

    return KPIResult(name="Conversion Rate", value=rate, unit="percent")


def calculate_cac(marketing_spend: float, new_customers: int) -> KPIResult:
    """
    Calcula el Customer Acquisition Cost (CAC).

    CAC = Marketing Spend / New Customers

    Args:
        marketing_spend: Gasto total en marketing
        new_customers: Número de nuevos clientes adquiridos

    Returns:
        KPIResult con el costo de adquisición por cliente

    Raises:
        ValueError: Si new_customers <= 0 o marketing_spend < 0

    Examples:
        >>> result = calculate_cac(10000.0, 100)
        >>> result.value
        100.0
    """
    if new_customers <= 0:
        raise ValueError("New customers must be greater than zero")
    if marketing_spend < 0:
        raise ValueError("Marketing spend cannot be negative")

    cac = marketing_spend / new_customers

    return KPIResult(name="CAC", value=cac, unit="currency")


def calculate_ltv(
    avg_order_value: float,
    purchase_frequency: float,
    customer_lifespan: float,
    gross_margin: float = 1.0,
) -> KPIResult:
    """
    Calcula el Customer Lifetime Value (LTV).

    LTV = AOV * Purchase Frequency * Customer Lifespan * Gross Margin

    Args:
        avg_order_value: Valor promedio de pedido
        purchase_frequency: Frecuencia de compra (por año)
        customer_lifespan: Duración promedio del cliente (en años)
        gross_margin: Margen bruto (0-1), por defecto 1.0

    Returns:
        KPIResult con el valor de vida del cliente

    Raises:
        ValueError: Si algún parámetro es inválido

    Examples:
        >>> result = calculate_ltv(50.0, 4.0, 3.0)
        >>> result.value
        600.0
        >>> result = calculate_ltv(100.0, 2.0, 5.0, gross_margin=0.3)
        >>> result.value
        300.0
    """
    if avg_order_value < 0:
        raise ValueError("Average order value cannot be negative")
    if purchase_frequency <= 0:
        raise ValueError("Purchase frequency must be positive")
    if customer_lifespan <= 0:
        raise ValueError("Customer lifespan must be positive")
    if not 0 <= gross_margin <= 1:
        raise ValueError("Gross margin must be between 0 and 1")

    ltv = avg_order_value * purchase_frequency * customer_lifespan * gross_margin

    return KPIResult(name="LTV", value=ltv, unit="currency")


def calculate_churn_rate(lost_customers: int, total_customers_start: int) -> KPIResult:
    """
    Calcula la tasa de abandono (churn rate).

    Churn Rate = (Lost Customers / Starting Customers) * 100

    Args:
        lost_customers: Clientes perdidos en el periodo
        total_customers_start: Total de clientes al inicio del periodo

    Returns:
        KPIResult con la tasa de abandono en porcentaje

    Raises:
        ValueError: Si total_customers_start <= 0 o lost > total

    Examples:
        >>> result = calculate_churn_rate(50, 1000)
        >>> result.value
        5.0
    """
    if total_customers_start <= 0:
        raise ValueError("Starting customers must be greater than zero")
    if lost_customers > total_customers_start:
        raise ValueError("Lost customers cannot exceed starting customers")
    if lost_customers < 0:
        raise ValueError("Lost customers cannot be negative")

    rate = (lost_customers / total_customers_start) * 100

    return KPIResult(name="Churn Rate", value=rate, unit="percent")


def calculate_retention_rate(
    retained_customers: int, total_customers_start: int
) -> KPIResult:
    """
    Calcula la tasa de retención.

    Retention Rate = (Retained Customers / Starting Customers) * 100

    Args:
        retained_customers: Clientes retenidos en el periodo
        total_customers_start: Total de clientes al inicio del periodo

    Returns:
        KPIResult con la tasa de retención en porcentaje

    Raises:
        ValueError: Si total_customers_start <= 0 o retained > total

    Examples:
        >>> result = calculate_retention_rate(850, 1000)
        >>> result.value
        85.0
    """
    if total_customers_start <= 0:
        raise ValueError("Starting customers must be greater than zero")
    if retained_customers > total_customers_start:
        raise ValueError("Retained customers cannot exceed starting customers")
    if retained_customers < 0:
        raise ValueError("Retained customers cannot be negative")

    rate = (retained_customers / total_customers_start) * 100

    return KPIResult(name="Retention Rate", value=rate, unit="percent")


def calculate_mrr(subscriptions: list[dict]) -> KPIResult:
    """
    Calcula el Monthly Recurring Revenue (MRR).

    MRR = Suma de todos los montos mensuales de suscripciones activas

    Args:
        subscriptions: Lista de suscripciones con campos:
            - customer_id: ID del cliente
            - monthly_amount: Monto mensual
            - status: Estado ('active', 'cancelled', etc.)

    Returns:
        KPIResult con el MRR total

    Examples:
        >>> subs = [
        ...     {"customer_id": 1, "monthly_amount": 99.0, "status": "active"},
        ...     {"customer_id": 2, "monthly_amount": 49.0, "status": "cancelled"},
        ... ]
        >>> result = calculate_mrr(subs)
        >>> result.value
        99.0
    """
    mrr = sum(
        sub.get("monthly_amount", 0.0)
        for sub in subscriptions
        if sub.get("status") == "active"
    )

    return KPIResult(name="MRR", value=mrr, unit="currency")


def calculate_arr(mrr: float) -> KPIResult:
    """
    Calcula el Annual Recurring Revenue (ARR).

    ARR = MRR * 12

    Args:
        mrr: Monthly Recurring Revenue

    Returns:
        KPIResult con el ARR

    Raises:
        ValueError: Si MRR es negativo

    Examples:
        >>> result = calculate_arr(10000.0)
        >>> result.value
        120000.0
    """
    if mrr < 0:
        raise ValueError("MRR cannot be negative")

    arr = mrr * 12

    return KPIResult(name="ARR", value=arr, unit="currency")


def calculate_nrr(
    starting_mrr: float,
    expansion: float,
    contraction: float,
    churn: float,
) -> KPIResult:
    """
    Calcula el Net Revenue Retention (NRR).

    NRR = (Starting MRR - Churn - Contraction + Expansion) / Starting MRR * 100

    Args:
        starting_mrr: MRR al inicio del periodo
        expansion: Ingresos adicionales de clientes existentes
        contraction: Reducción de ingresos de clientes existentes
        churn: Ingresos perdidos por cancelaciones

    Returns:
        KPIResult con el NRR en porcentaje

    Raises:
        ValueError: Si starting_mrr <= 0

    Examples:
        >>> result = calculate_nrr(100000.0, 15000.0, 5000.0, 8000.0)
        >>> result.value
        102.0
    """
    if starting_mrr <= 0:
        raise ValueError("Starting MRR must be greater than zero")
    if expansion < 0:
        raise ValueError("Expansion cannot be negative")
    if contraction < 0:
        raise ValueError("Contraction cannot be negative")
    if churn < 0:
        raise ValueError("Churn cannot be negative")

    ending_mrr = starting_mrr - churn - contraction + expansion
    nrr = (ending_mrr / starting_mrr) * 100

    return KPIResult(name="NRR", value=nrr, unit="percent")
