# Proyecto Práctico: Sistema de Métricas Analíticas

Sistema de cálculo de KPIs y métricas analíticas para dashboards de Business Intelligence.

## Objetivos

- Calcular KPIs de negocio (AOV, CAC, LTV, Churn, etc.)
- Realizar análisis de cohortes para retención y LTV
- Detectar anomalías en métricas usando métodos estadísticos
- Exportar métricas a formatos compatibles con herramientas de BI

## Conceptos Clave

### KPIs Implementados

| KPI | Descripción | Fórmula |
|-----|-------------|---------|
| AOV | Average Order Value | Revenue / Orders |
| CAC | Customer Acquisition Cost | Marketing Spend / New Customers |
| LTV | Customer Lifetime Value | AOV * Frequency * Lifespan |
| Churn Rate | Tasa de abandono | Lost Customers / Total * 100 |
| Retention Rate | Tasa de retención | Retained / Total * 100 |
| MRR | Monthly Recurring Revenue | Sum of active subscriptions |
| ARR | Annual Recurring Revenue | MRR * 12 |
| NRR | Net Revenue Retention | (MRR - Churn + Expansion) / MRR |

### Análisis de Cohortes

El módulo de cohortes permite:
- Agrupar usuarios por periodo de registro (semana/mes)
- Calcular retención D7, D14, D30
- Calcular LTV por cohorte
- Exportar matriz de retención

### Detección de Anomalías

Utiliza MAD (Median Absolute Deviation) para detección robusta:
- Más resistente a outliers que desviación estándar
- Soporte para estacionalidad (comparación por día de semana)
- Clasificación de severidad (warning/critical)

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py           # Documentación del módulo
│   ├── kpis.py               # Cálculo de KPIs de negocio
│   ├── cohorts.py            # Análisis de cohortes
│   ├── anomaly_detection.py  # Detección de anomalías
│   └── exporters.py          # Exportación a JSON/CSV
├── tests/
│   ├── __init__.py
│   ├── test_kpis.py          # Tests de KPIs
│   ├── test_cohorts.py       # Tests de cohortes
│   ├── test_anomaly_detection.py  # Tests de anomalías
│   └── test_exporters.py     # Tests de exportación
├── data/                     # Datos de ejemplo (opcional)
├── README.md
├── requirements.txt
└── .gitignore
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar Tests

```bash
# Tests con cobertura
pytest -v --cov=src --cov-report=term-missing --cov-report=html

# Solo tests
pytest -v

# Tests de un módulo específico
pytest tests/test_kpis.py -v
```

## Funciones Implementadas

### Módulo kpis.py

```python
from src.kpis import calculate_aov, calculate_cac, calculate_ltv

# Calcular AOV
result = calculate_aov(total_revenue=10000.0, total_orders=200)
print(f"AOV: ${result.value:.2f}")  # AOV: $50.00

# Calcular CAC
result = calculate_cac(marketing_spend=5000.0, new_customers=100)
print(f"CAC: ${result.value:.2f}")  # CAC: $50.00

# Calcular LTV
result = calculate_ltv(
    avg_order_value=50.0,
    purchase_frequency=4.0,  # compras por año
    customer_lifespan=3.0,   # años
    gross_margin=0.3         # 30% margen
)
print(f"LTV: ${result.value:.2f}")  # LTV: $180.00
```

### Módulo cohorts.py

```python
from datetime import date
from src.cohorts import CohortAnalysis, UserEvent

# Crear eventos de usuario
events = [
    UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
    UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
    UserEvent(user_id=1, event_date=date(2024, 1, 15), event_type="purchase", revenue=50.0),
    UserEvent(user_id=2, event_date=date(2024, 1, 5), event_type="signup"),
    # ... más eventos
]

# Crear análisis
analysis = CohortAnalysis.from_events(events, retention_days=[7, 14, 30])

# Obtener matriz de retención
retention = analysis.get_retention_matrix()
print(retention)
# {'2024-01': {'cohort_size': 2, 'd7_retention': 50.0, 'd14_retention': 50.0, ...}}

# Convertir a DataFrame
df = analysis.to_dataframe()
```

### Módulo anomaly_detection.py

```python
from datetime import date
from src.anomaly_detection import detect_anomaly, detect_anomalies_batch, MetricDataPoint

# Detección individual
historical = [100, 102, 98, 101, 99, 103, 97, 100]
result = detect_anomaly(current_value=150.0, historical_data=historical)

if result.is_anomaly:
    print(f"Anomalía detectada: {result.severity}")
    print(f"Rango esperado: {result.lower_bound:.2f} - {result.upper_bound:.2f}")

# Detección en batch
data_points = [
    MetricDataPoint(date=date(2024, 1, i), value=100.0 + i)
    for i in range(1, 30)
]
data_points.append(MetricDataPoint(date=date(2024, 1, 30), value=200.0))  # Anomalía

results = detect_anomalies_batch(data_points, min_history=7)
anomalies = [r for r in results if r.is_anomaly]
print(f"Anomalías encontradas: {len(anomalies)}")
```

### Módulo exporters.py

```python
from pathlib import Path
from src.kpis import calculate_aov, calculate_cac
from src.exporters import export_to_json, export_to_csv, create_metric_definition

# Calcular KPIs
kpis = [
    calculate_aov(10000.0, 200),
    calculate_cac(5000.0, 100),
]

# Exportar a JSON
export_to_json(kpis, Path("output/metrics.json"), metadata={"dashboard": "Executive"})

# Exportar a CSV
export_to_csv(kpis, Path("output/metrics.csv"))

# Crear definición de métrica
definition = create_metric_definition(
    name="MRR",
    description="Monthly Recurring Revenue",
    formula="SUM(monthly_amount) WHERE status = 'active'",
    unit="currency",
    owner="Finance Team",
    thresholds={
        "green": {"min": 0},
        "yellow": {"min": -5, "max": 0},
        "red": {"max": -5}
    }
)
print(definition.to_yaml())
```

## Troubleshooting

### Error: ModuleNotFoundError

Asegúrate de que el entorno virtual está activado y ejecutas desde el directorio del proyecto:

```bash
cd modulo-08-data-warehousing/tema-3-analytics-bi/04-proyecto-practico
python -m pytest tests/
```

### Error: pandas not found

pandas es opcional. Solo se necesita para `CohortAnalysis.to_dataframe()`:

```bash
pip install pandas
```

## Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Conceptos de Analytics y BI
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos prácticos
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios con soluciones

## Tecnologías

- **Python 3.11+**: Lenguaje principal
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **pandas**: Análisis de datos (opcional)

## Licencia

Material del Master en Ingeniería de Datos con IA.
