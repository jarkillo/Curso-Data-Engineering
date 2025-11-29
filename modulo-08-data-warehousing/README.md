# Módulo 8: Data Warehousing

**Objetivo**: Dominar el diseño, implementación y mantenimiento de Data Warehouses modernos, incluyendo modelado dimensional, herramientas de transformación (dbt), y visualización de datos.

---

## 📋 Contenido del Módulo

| Tema | Estado | Tests | Cobertura | Descripción |
|------|--------|-------|-----------|-------------|
| **Tema 1**: Modelado Dimensional | ✅ 100% | 154/154 | 91% | Star Schema, Snowflake, dimensiones, hechos |
| **Tema 2**: Herramientas DWH (dbt) | ✅ 100% | ~44 | N/A | dbt, ELT, transformaciones, testing |
| **Tema 3**: Analytics y BI | ✅ 100% | 82/82 | 92% | KPIs, dashboards, detección de anomalías |

**Progreso Total**: 100% (3/3 temas completados)

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

### Modelado Dimensional (Tema 1)
- ✅ Diseñar esquemas Star Schema y Snowflake
- ✅ Identificar y modelar dimensiones (SCD Type 1, 2, 3)
- ✅ Crear tablas de hechos con métricas adecuadas
- ✅ Aplicar técnicas de normalización en dimensiones
- ✅ Implementar hechos sin hechos (factless fact tables)
- ✅ Validar diseños de Data Warehouse
- ✅ Generar DDL automático para esquemas dimensionales

### Herramientas DWH - dbt (Tema 2)
- ✅ Configurar y ejecutar proyectos dbt completos
- ✅ Aplicar filosofía ELT vs ETL tradicional
- ✅ Crear modelos de staging (limpieza inicial)
- ✅ Diseñar marts (dimensiones y hechos)
- ✅ Implementar tests de calidad de datos
- ✅ Escribir macros reutilizables con Jinja
- ✅ Usar snapshots para SCD Type 2 automático
- ✅ Generar documentación automática
- ✅ Crear modelos incrementales eficientes

### Analytics y BI (Tema 3)
- ✅ Diseñar dashboards efectivos para diferentes audiencias
- ✅ Definir y calcular KPIs de negocio (AOV, CAC, LTV, NRR)
- ✅ Realizar análisis de cohortes (retención, LTV por cohorte)
- ✅ Detectar anomalías en métricas con métodos estadísticos
- ✅ Exportar métricas para herramientas de BI (JSON, CSV)
- ✅ Implementar data storytelling efectivo

---

## 📊 Estadísticas Generales

```
Temas completados:    3/3  (100%)
Tests totales:        280
Tests pasando:        280  (100%)
Cobertura promedio:   91%
Tiempo estimado:      60-75 horas
Proyectos prácticos:  3/3
```

---

## 🏗️ Tema 1: Modelado Dimensional

**Directorio**: `tema-1-dimensional-modeling/`

### Contenido

- **01-TEORIA.md**: Conceptos de modelado dimensional, Star Schema, Snowflake
- **02-EJEMPLOS.md**: Ejemplos de diseños completos
- **03-EJERCICIOS.md**: Ejercicios con soluciones
- **04-proyecto-practico/**: Sistema de validación de Data Warehouse

### Proyecto Práctico

**Sistema de Diseño y Validación de Data Warehouse**

**Características**:
- Validación automática de Star Schema
- Identificación de fact tables y dimensiones
- Generación de DDL (CREATE TABLE + índices)
- 25 tests unitarios, 98% cobertura

**Tecnologías**: Python, pytest, TDD

**Ejecutar**:
```bash
cd tema-1-dimensional-modeling/04-proyecto-practico
pytest -v --cov=src --cov-report=html
```

**Detalles**: Ver [README del proyecto](tema-1-dimensional-modeling/04-proyecto-practico/README.md)

---

## 🔧 Tema 2: Herramientas DWH (dbt)

**Directorio**: `tema-2-herramientas-dwh/`

### Contenido

- **01-TEORIA.md** (~7,500 palabras): Fundamentos de dbt
  - ELT vs ETL
  - Materializaciones (view, table, incremental, ephemeral)
  - Referencias y sources ({{ ref() }}, {{ source() }})
  - Framework de testing
  - Jinja templating y macros
  - Snapshots (SCD Type 2)
  - Documentación automática

- **02-EJEMPLOS.md** (~7,000 palabras): 5 ejemplos progresivos
  - Staging básico
  - Referencias y tests
  - Macros reutilizables
  - Modelos incrementales
  - Snapshots

- **03-EJERCICIOS.md** (~8,000 palabras): 15 ejercicios con soluciones
  - Básicos (1-4): Staging, tests, refs
  - Intermedios (5-10): Macros, CTEs, custom tests
  - Avanzados (11-15): Incrementales, snapshots, debugging

### Proyecto Práctico

**Pipeline dbt Completo - TechMart Analytics**

**Arquitectura**:
```
Seeds (CSV)
    ↓
Staging Layer (views)
  ├── stg_customers
  ├── stg_products
  └── stg_orders
    ↓
Marts Layer (tables)
  ├── Dimensions
  │   ├── dim_customers (segmentación RFM)
  │   └── dim_products (clasificación ventas)
  └── Facts
      ├── fct_orders (pedidos)
      └── fct_daily_revenue (análisis diario)
    ↓
Snapshots (SCD Type 2)
  └── products_snapshot
```

**Características**:
- 3 modelos staging, 2 dimensiones, 2 hechos
- 10 macros reutilizables
- ~44 tests (40 genéricos + 4 personalizados)
- 1 snapshot SCD Type 2
- Documentación completa con schema.yml

**Tecnologías**: dbt-core, dbt-utils, PostgreSQL/DuckDB, Jinja2, SQL

**Ejecutar**:
```bash
cd tema-2-herramientas-dwh/04-proyecto-practico

# Instalar dependencias
pip install -r requirements.txt
dbt deps

# Ejecutar pipeline completo
dbt seed          # Cargar datos CSV
dbt run           # Ejecutar transformaciones
dbt test          # Validar calidad de datos
dbt docs generate # Generar documentación
dbt docs serve    # Ver docs en navegador
dbt snapshot      # Crear snapshots
```

**Detalles**: Ver [README del proyecto](tema-2-herramientas-dwh/04-proyecto-practico/README.md)

---

## 📈 Tema 3: Analytics y BI

**Directorio**: `tema-3-analytics-bi/`

### Contenido

- **01-TEORIA.md** (~4,000 palabras): Fundamentos de Analytics y BI
  - Business Intelligence: qué es y qué no es
  - Métricas vs KPIs vs Dimensiones
  - Pirámide de métricas (operativas, tácticas, estratégicas)
  - Principios de diseño de dashboards
  - Antipatrones en dashboards
  - Data storytelling
  - Herramientas de BI modernas

- **02-EJEMPLOS.md** (~6,000 palabras): 4 ejemplos progresivos
  - Definir KPIs para e-commerce
  - Diseñar dashboard ejecutivo
  - Métricas de producto SaaS
  - Sistema completo de OKRs

- **03-EJERCICIOS.md** (~8,000 palabras): 15 ejercicios con soluciones
  - Básicos (1-5): Identificación de KPIs, cálculos básicos
  - Intermedios (6-11): Diseño de dashboards, cohortes, funnels
  - Avanzados (12-15): Alertas ML, OKRs cascading, arquitectura

### Proyecto Práctico

**Sistema de Métricas Analíticas**

**Arquitectura**:
```
src/
├── kpis.py               # Cálculo de KPIs (AOV, CAC, LTV, NRR, etc.)
├── cohorts.py            # Análisis de cohortes y retención
├── anomaly_detection.py  # Detección de anomalías con MAD
└── exporters.py          # Exportación a JSON/CSV para BI
```

**Características**:
- 9 funciones de cálculo de KPIs
- Análisis de cohortes con retención D7/D14/D30
- Detección de anomalías con MAD (robusto a outliers)
- Exportadores para herramientas de BI
- 82 tests unitarios, 92% cobertura

**Tecnologías**: Python, pytest, TDD

**Ejecutar**:
```bash
cd tema-3-analytics-bi/04-proyecto-practico
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
pytest -v --cov=src --cov-report=term-missing
```

**Detalles**: Ver [README del proyecto](tema-3-analytics-bi/04-proyecto-practico/README.md)

---

## 🚀 Cómo Usar este Módulo

### Requisitos Previos

- **Completados**:
  - Módulo 1: Fundamentos de Python
  - Módulo 2: SQL Básico e Intermedio
  - Módulo 3: Ingeniería de Datos Core
  - Módulo 5: Bases de Datos Avanzadas (recomendado)

- **Conocimientos**:
  - SQL avanzado
  - Modelado de bases de datos
  - Python básico
  - Conceptos de data warehousing

### Ruta de Aprendizaje Recomendada

1. **Semana 1-2**: Tema 1 - Modelado Dimensional
   - Estudiar teoría (4-5 horas)
   - Trabajar ejemplos (3-4 horas)
   - Resolver ejercicios (4-5 horas)
   - Implementar proyecto práctico (6-8 horas)

2. **Semana 3-4**: Tema 2 - dbt
   - Estudiar teoría dbt (5-6 horas)
   - Trabajar ejemplos progresivos (4-5 horas)
   - Resolver ejercicios (5-6 horas)
   - Implementar pipeline dbt completo (8-10 horas)

3. **Semana 5-6**: Tema 3 - Analytics y BI
   - Estudiar teoría de KPIs y dashboards (4-5 horas)
   - Trabajar ejemplos prácticos (3-4 horas)
   - Resolver ejercicios (5-6 horas)
   - Implementar proyecto de métricas (6-8 horas)

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/jarkillo/Curso-Data-Engineering.git
cd Curso-Data-Engineering/modulo-08-data-warehousing

# Tema 1: Modelado Dimensional
cd tema-1-dimensional-modeling/04-proyecto-practico
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
pytest -v --cov=src

# Tema 2: dbt
cd ../tema-2-herramientas-dwh/04-proyecto-practico
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
dbt deps
dbt seed && dbt run && dbt test
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Kimball Group - Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [dbt Docs](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Star Schema Benchmark](http://www.cs.umb.edu/~poneil/StarSchemaB.PDF)

### Libros Recomendados

- "The Data Warehouse Toolkit" - Ralph Kimball
- "Building a Scalable Data Warehouse with Data Vault 2.0" - Dan Linstedt
- "Analytics Setup Guidebook" - Mikkel Dengsøe

### Herramientas

- **dbt**: https://www.getdbt.com/
- **DuckDB**: https://duckdb.org/ (para desarrollo local)
- **PostgreSQL**: https://www.postgresql.org/
- **SQLFluff**: https://www.sqlfluff.com/ (linting SQL)

---

## 🎓 Evaluación

### Criterios de Completitud

Para considerar el módulo completo:

- [x] ✅ Tema 1: 154 tests pasando, 91% cobertura
- [x] ✅ Tema 2: Pipeline dbt ejecutable con ~44 tests
- [x] ✅ Tema 3: 82 tests pasando, 92% cobertura
- [ ] Proyecto integrador final (TBD)
- [ ] Revisión de pares

### Proyecto Final (Planificado)

**Data Warehouse Completo End-to-End**:
- Diseño de esquema dimensional completo
- Pipeline dbt de transformación
- Dashboard con métricas clave
- Documentación completa
- Tests de calidad de datos

---

## 📝 Notas de Versión

**Versión**: 1.1.0
**Última Actualización**: 2024-11-29
**Mantenedor**: [Tu Nombre]

### Changelog

- **v1.1.0** (2024-11-29):
  - ✅ Tema 3 completado (82 tests, 92% cov)
  - Sistema de métricas analíticas
  - Análisis de cohortes
  - Detección de anomalías
  - Módulo 8 completo al 100%

- **v1.0.0** (2024-11-13):
  - ✅ Tema 1 completado (154 tests, 91% cov)
  - ✅ Tema 2 completado (pipeline dbt completo)

- **v0.2.0** (2024-11-12):
  - ✅ Tema 1 completado

- **v0.1.0** (2024-11-09):
  - 🚀 Inicio del módulo

---

## 🤝 Contribuciones

Este módulo es parte del **Master en Ingeniería de Datos con IA**.

Para reportar errores o sugerir mejoras:
- Abrir issue en GitHub
- Contactar al mantenedor

---

## 📜 Licencia

Este material es propiedad del Master en Ingeniería de Datos con IA.
Todos los derechos reservados.

---

**¡Bienvenido al mundo del Data Warehousing moderno!** 🚀

**Siguiente paso**: Comienza con [Tema 1: Modelado Dimensional](tema-1-dimensional-modeling/)
