# Changelog - Proyecto Analytics Dashboard

Todos los cambios notables en este proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [Unreleased]

### Added
- Nada pendiente

---

## [1.0.0] - 2024-11-29

### Added

#### Módulo KPIs (`src/kpis.py`)
- Función `calculate_aov` - Average Order Value
- Función `calculate_conversion_rate` - Tasa de conversión
- Función `calculate_cac` - Customer Acquisition Cost
- Función `calculate_ltv` - Customer Lifetime Value (con margen opcional)
- Función `calculate_churn_rate` - Tasa de abandono
- Función `calculate_retention_rate` - Tasa de retención
- Función `calculate_mrr` - Monthly Recurring Revenue
- Función `calculate_arr` - Annual Recurring Revenue
- Función `calculate_nrr` - Net Revenue Retention
- Dataclass `KPIResult` para resultados estructurados

#### Módulo Cohortes (`src/cohorts.py`)
- Función `build_cohort_table` - Construcción de tabla de cohortes
- Función `calculate_retention_by_cohort` - Retención D7/D14/D30
- Función `calculate_cohort_ltv` - LTV por cohorte
- Clase `CohortAnalysis` para análisis completo
- Dataclass `UserEvent` para eventos de usuario
- Soporte para cohortes semanales y mensuales

#### Módulo Detección de Anomalías (`src/anomaly_detection.py`)
- Función `detect_anomaly` - Detección individual con MAD
- Función `calculate_rolling_stats` - Estadísticas rolling
- Función `detect_anomalies_batch` - Detección en batch
- Soporte para filtrado por día de semana (estacionalidad)
- Clasificación de severidad (warning/critical)
- Dataclass `AnomalyResult` y `MetricDataPoint`

#### Módulo Exportadores (`src/exporters.py`)
- Función `export_to_json` - Exportación a JSON con metadata
- Función `export_to_csv` - Exportación a CSV
- Función `create_metric_definition` - Creación de definiciones
- Clase `MetricDefinition` con conversión a YAML

#### Tests
- 82 tests unitarios
- 92% de cobertura de código
- Tests para casos edge y errores

#### Documentación
- README.md completo con ejemplos de uso
- Docstrings en todas las funciones públicas
- Type hints en todas las funciones

### Technical Details
- Python 3.11+
- TDD (Test-Driven Development)
- Functional programming style
- No external dependencies for core (pandas optional)

---

## Issue Reference

- **JAR-327**: Módulo 8 - Tema 3: Analytics y BI (KPIs, Dashboards)
