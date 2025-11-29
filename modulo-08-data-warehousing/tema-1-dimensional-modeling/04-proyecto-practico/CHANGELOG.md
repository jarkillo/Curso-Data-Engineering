# Changelog - Proyecto Práctico: Data Warehouse con Star Schema

Todos los cambios importantes a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [1.0.0] - 2025-11-29

### Added
- **JAR-325**: Proyecto práctico de Dimensional Modeling completado al 100%

### Modules Implemented
- `generador_dim_fecha.py` - Generador de dimensión de fechas con festivos
- `generador_dim_producto.py` - Generador de catálogo de productos con Faker
- `generador_dim_cliente.py` - Generador de clientes con SCD Type 2
- `generador_dim_vendedor.py` - Generador de vendedores con jerarquía
- `generador_fact_ventas.py` - Generador de tabla de hechos FactVentas
- `scd_tipo2.py` - Lógica genérica de Slowly Changing Dimension Type 2
- `validaciones.py` - 5 funciones de validación de calidad de datos
- `database.py` - Context manager para conexión SQLite
- `queries_analiticos.py` - 6 queries OLAP (drill-down, roll-up, slice, dice)
- `utilidades.py` - Logging, formateo de números, medición de tiempo

### Quality Metrics
- **156 tests passing** (100% success rate)
- **93% code coverage** (exceeds 80% requirement)
- **0 flake8 errors** (E501 line length issues fixed)
- **100% black formatting** compliance

### Documentation
- README.md completo con ~900 líneas
- ARQUITECTURA.md con diseño técnico
- schema.sql con DDL del Star Schema
- Docstrings completas en todas las funciones

---

## [0.9.0] - 2025-11-10

### Added
- Implementación inicial de todos los módulos
- Tests unitarios siguiendo TDD
- main.py con pipeline end-to-end

### Fixed
- Integridad referencial en FactVentas
- SCD Type 2 con múltiples versiones

---

## [0.5.0] - 2025-11-09

### Added
- Estructura inicial del proyecto
- Módulos DimFecha y DimProducto
- Schema SQL del Star Schema

---

**Última actualización:** 2025-11-29
**Issue:** JAR-325
**Estado:** COMPLETADO
