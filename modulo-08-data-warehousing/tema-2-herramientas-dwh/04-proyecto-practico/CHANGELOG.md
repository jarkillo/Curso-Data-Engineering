# Changelog - Proyecto Práctico: Pipeline dbt TechMart Analytics

Todos los cambios importantes a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [1.0.0] - 2025-11-29

### Added
- **JAR-326**: Proyecto práctico de dbt completado al 100%

### Project Structure
- `dbt_project.yml` - Configuración del proyecto dbt
- `profiles.yml` - Configuración de conexión (PostgreSQL/DuckDB)
- `packages.yml` - Dependencias (dbt-utils)

### Models Implemented

**Staging Layer (3 models)**:
- `stg_customers.sql` - Limpieza de emails, nombres, teléfonos
- `stg_products.sql` - Deduplicación por updated_at
- `stg_orders.sql` - Cálculo de days_to_ship, flags

**Dimensions (2 models)**:
- `dim_customers.sql` - Segmentación RFM (Bronze/Silver/Gold/Platinum)
- `dim_products.sql` - Clasificación por popularidad e ingresos

**Facts (2 models)**:
- `fct_orders.sql` - Pedidos con dimensiones desnormalizadas
- `fct_daily_revenue.sql` - Análisis diario con pivotes

### Seeds
- `raw_customers.csv` - 15 clientes con datos realistas
- `raw_products.csv` - 15 versiones de 12 productos
- `raw_orders.csv` - 25 pedidos con diferentes estados

### Macros (10 macros)
- `cents_to_dollars()` - Conversión de centavos a dólares
- `pivot_payment_methods()` - Pivote dinámico de métodos de pago
- `pivot_categories()` - Pivote dinámico de categorías
- `age_in_years()` - Cálculo de edad en años
- `generate_surrogate_key()` - Generación de claves subrogadas
- `normalize_text()` - Normalización de texto
- Y más...

### Tests
- 4 tests personalizados (SQL):
  - Validación de montos positivos
  - Verificación de cálculos (quantity × unit_price)
  - Consistencia estado vs fechas
  - Coherencia lifetime_value vs total_orders
- ~40 tests genéricos (schema.yml):
  - unique, not_null, accepted_values, relationships
  - dbt_utils.expression_is_true

### Snapshots
- `products_snapshot.sql` - SCD Type 2 para historial de productos

### Documentation
- README.md completo (~500 líneas)
- schema.yml con descripción de todas las columnas
- example_usage.py - Script de demostración

---

## [0.5.0] - 2025-11-13

### Added
- Estructura inicial del proyecto dbt
- Seeds con datos de ejemplo
- Modelos staging básicos
- Primeros tests genéricos

---

**Última actualización:** 2025-11-29
**Issue:** JAR-326
**Estado:** COMPLETADO
