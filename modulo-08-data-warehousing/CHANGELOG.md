# Changelog - Módulo 8: Data Warehousing y Analytics

Historial de cambios del Módulo 8 del Master en Ingeniería de Datos.

---

## [2.0.0] - 2024-12-04

### Added - Tema 3: Dashboard Streamlit Completo

#### Dashboard Interactivo (`tema-3-analytics-bi/04-proyecto-practico/dashboard/`)
- `app.py`: Aplicación Streamlit con 4 páginas y 22+ visualizaciones
- `database.py`: Conexión al Data Warehouse del Tema 1
- `queries.py`: 20+ consultas analíticas optimizadas

#### Páginas del Dashboard
- **Overview**: KPIs ejecutivos, tendencias, distribución por categoría/región
- **Análisis de Ventas**: Series temporales, top productos, treemap, heatmap
- **Análisis de Clientes**: Segmentación RFM, distribución, top clientes
- **Performance Vendedores**: Rankings, evolución, comisiones

#### Revisiones Pedagógicas
- `REVISION_PEDAGOGICA.md` para los 3 temas
- Score promedio: 9.4/10 - APROBADO

### Issues
- JAR-346: Dashboard Analytics completo
- JAR-347: Revisión pedagógica

---

## [1.2.0] - 2024-12-01

### Added - Tema 3: Sistema de Métricas Analíticas

#### Contenido Educativo
- `01-TEORIA.md`: ~4,000 palabras sobre Analytics y BI
- `02-EJEMPLOS.md`: 4 ejemplos progresivos con Plotly
- `03-EJERCICIOS.md`: 15 ejercicios con soluciones

#### Proyecto Práctico (`tema-3-analytics-bi/04-proyecto-practico/src/`)
- `kpis.py`: 9 funciones de KPIs (AOV, CAC, LTV, NRR, etc.)
- `cohorts.py`: Análisis de cohortes con retención D7/D14/D30
- `anomaly_detection.py`: Detección con MAD
- `exporters.py`: Exportación JSON/CSV para BI

#### Métricas
- 84 tests unitarios
- 92% cobertura de código

### Issues
- JAR-343: Teoría Analytics y BI
- JAR-344: Ejemplos Analytics
- JAR-345: Ejercicios Analytics

---

## [1.1.0] - 2024-11-13

### Added - Tema 2: Pipeline dbt Completo

#### Contenido Educativo
- `01-TEORIA.md`: ~7,500 palabras sobre dbt
- `02-EJEMPLOS.md`: 5 ejemplos progresivos
- `03-EJERCICIOS.md`: 15 ejercicios con soluciones

#### Proyecto Práctico - TechMart Analytics
- 3 modelos staging (views)
- 2 dimensiones (dim_customers, dim_products)
- 2 hechos (fct_orders, fct_daily_revenue)
- 10 macros reutilizables
- 1 snapshot SCD Type 2
- ~44 tests (genéricos + personalizados)

#### Tecnologías
- dbt-core, dbt-utils, PostgreSQL/DuckDB, Jinja2

### Issues
- JAR-338 a JAR-342

---

## [1.0.0] - 2024-11-09

### Added - Tema 1: Modelado Dimensional

#### Contenido Educativo
- `01-TEORIA.md`: Star Schema, Snowflake, SCD Types
- `02-EJEMPLOS.md`: Ejemplos de diseños completos
- `03-EJERCICIOS.md`: Ejercicios con soluciones

#### Proyecto Práctico
- Sistema de validación de Data Warehouse
- Generación de DDL automático
- 156 tests, 93% cobertura

#### Tecnologías
- Python, pytest, TDD

### Issues
- JAR-194: Módulo 8 inicial
- JAR-328 a JAR-337

---

## Resumen del Módulo

| Tema | Tests | Cobertura | Estado |
|------|-------|-----------|--------|
| Tema 1: Modelado Dimensional | 156 | 93% | ✅ |
| Tema 2: Herramientas dbt | ~44 | N/A | ✅ |
| Tema 3: Analytics y BI | 84 | 92% | ✅ |
| **Total** | **280+** | **91%** | **✅ COMPLETO** |

---

**Módulo completado**: 2024-12-04
**Versión final**: 2.0.0
