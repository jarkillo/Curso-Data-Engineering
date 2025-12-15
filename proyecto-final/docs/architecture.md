# Arquitectura del Pipeline ETL - TechMart Analytics

## Visión General

Este documento describe la arquitectura del pipeline ETL de TechMart Analytics, diseñado para procesar datos de e-commerce y cargarlos en un data warehouse dimensional.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FUENTES DE DATOS                               │
├──────────────────┬───────────────────┬──────────────────────────────────────┤
│   API REST       │   Archivos CSV    │         PostgreSQL                   │
│   (Pedidos)      │   (Productos)     │         (Clientes)                   │
│                  │                   │                                      │
│  ┌────────────┐  │  ┌─────────────┐  │  ┌──────────────────────────────┐   │
│  │ /orders    │  │  │ products.csv│  │  │ customers table              │   │
│  │ endpoint   │  │  │             │  │  │                              │   │
│  └─────┬──────┘  │  └──────┬──────┘  │  └────────────┬─────────────────┘   │
└────────┼─────────┴─────────┼────────┴───────────────┼───────────────────────┘
         │                   │                        │
         ▼                   ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CAPA DE EXTRACCIÓN                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ api_extractor   │  │ csv_extractor   │  │ db_extractor                │  │
│  │                 │  │                 │  │                             │  │
│  │ - Retry logic   │  │ - Schema valid. │  │ - Connection pooling        │  │
│  │ - Rate limiting │  │ - Type casting  │  │ - Query optimization        │  │
│  │ - Auth headers  │  │ - Encoding      │  │ - Incremental extraction    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────────┬────────────────┘  │
└───────────┼────────────────────┼────────────────────────┼───────────────────┘
            │                    │                        │
            └────────────────────┼────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              STAGING AREA                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    /warehouse/staging/                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │orders.parquet│  │products.     │  │customers.parquet         │  │   │
│  │  │              │  │parquet       │  │                          │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE TRANSFORMACIÓN                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         CLEANING                                    │   │
│  │  • Eliminación de duplicados                                        │   │
│  │  • Manejo de valores nulos                                          │   │
│  │  • Normalización de strings                                         │   │
│  │  • Validación de rangos                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        ENRICHMENT                                   │   │
│  │  • Join pedidos + productos                                         │   │
│  │  • Join pedidos + clientes                                          │   │
│  │  • Generación de date_id (YYYYMMDD) para enlace con dim_date        │   │
│  │  • Cálculo de métricas (totales, descuentos)                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       AGGREGATIONS                                  │   │
│  │  • Ventas por producto                                              │   │
│  │  • Ventas por cliente                                               │   │
│  │  • Ventas por período                                               │   │
│  │  • KPIs de negocio                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CAPA DE CARGA                                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   DATA WAREHOUSE (Star Schema)                      │   │
│  │                                                                     │   │
│  │   ┌──────────────┐       ┌──────────────────────┐                  │   │
│  │   │ dim_product  │       │     fact_sales       │                  │   │
│  │   │──────────────│       │──────────────────────│                  │   │
│  │   │ product_id   │◄──────│ order_id (PK)        │                  │   │
│  │   │ product_name │       │ product_id (FK)      │                  │   │
│  │   │ category     │       │ customer_id (FK)     │──────►           │   │
│  │   │ price        │       │ date_id (FK)         │                  │   │
│  │   └──────────────┘       │ quantity             │                  │   │
│  │                          │ unit_price           │   ┌────────────┐ │   │
│  │   ┌──────────────┐       │ order_total          │   │dim_customer│ │   │
│  │   │  dim_date    │       │ discount_amount      │   │────────────│ │   │
│  │   │──────────────│       └──────────────────────┘   │customer_id │ │   │
│  │   │ date_id      │◄─────────────────────────────────│customer_   │ │   │
│  │   │ date         │                                  │  name      │ │   │
│  │   │ year         │                                  │region      │ │   │
│  │   │ month        │                                  │segment     │ │   │
│  │   │ day          │                                  └────────────┘ │   │
│  │   │ day_of_week  │                                                 │   │
│  │   │ is_weekend   │                                                 │   │
│  │   └──────────────┘                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE VALIDACIÓN                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • Validación de schema                                             │   │
│  │  • Verificación de integridad referencial                           │   │
│  │  • Checks de calidad de datos                                       │   │
│  │  • Alertas por anomalías                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. Extractores (`src/extractors/`)

| Componente | Responsabilidad | Fuente |
|------------|-----------------|--------|
| `api_extractor` | Extraer pedidos vía REST API | Sistema de ventas |
| `csv_extractor` | Leer catálogo de productos | Archivos CSV |
| `db_extractor` | Consultar clientes | PostgreSQL |

**Características comunes:**
- Manejo de errores y reintentos
- Logging estructurado
- Validación de respuestas

### 2. Transformadores (`src/transformers/`)

| Componente | Responsabilidad |
|------------|-----------------|
| `cleaning` | Limpieza y normalización de datos |
| `enrichment` | Joins, generación de date_id y cálculo de métricas |
| `aggregations` | Agregaciones y KPIs |

**Funciones de enrichment:**
- `enrich_orders_with_products()` - Join con catálogo
- `enrich_orders_with_customers()` - Join con clientes
- `add_date_id()` - Genera `date_id` (formato YYYYMMDD) para enlace con `dim_date`
- `calculate_order_metrics()` - Calcula totales y descuentos

**Pipeline de transformación:**
```
Raw Data → Clean → Enrich (joins + date_id) → Metrics → Aggregate → Ready for Load
```

### 3. Cargadores (`src/loaders/`)

| Componente | Responsabilidad |
|------------|-----------------|
| `warehouse_loader` | Carga de dimensiones y hechos |

**Operaciones soportadas:**
- Carga inicial (full load)
- Carga incremental (upsert)
- Validación de schema

### 4. Utilidades (`src/utils/`)

| Componente | Responsabilidad |
|------------|-----------------|
| `validators` | Validaciones de calidad de datos |
| `logging_config` | Logging estructurado JSON |

## Modelo de Datos

### Star Schema

El data warehouse usa un modelo dimensional (star schema) optimizado para consultas analíticas.

#### Tabla de Hechos: `fact_sales`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| order_id | VARCHAR | PK - Identificador del pedido |
| product_id | VARCHAR | FK → dim_product |
| customer_id | VARCHAR | FK → dim_customer |
| date_id | INTEGER | FK → dim_date |
| quantity | INTEGER | Cantidad vendida |
| unit_price | DECIMAL | Precio unitario |
| order_total | DECIMAL | Total del pedido |
| discount_amount | DECIMAL | Descuento aplicado |
| status | VARCHAR | Estado del pedido |

#### Dimensión: `dim_product`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| product_id | VARCHAR | PK - Identificador del producto |
| product_name | VARCHAR | Nombre del producto |
| category | VARCHAR | Categoría |
| price | DECIMAL | Precio de catálogo |
| stock | INTEGER | Stock disponible |

#### Dimensión: `dim_customer`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| customer_id | VARCHAR | PK - Identificador del cliente |
| customer_name | VARCHAR | Nombre |
| email | VARCHAR | Email |
| region | VARCHAR | Región geográfica |
| segment | VARCHAR | Segmento de cliente |

#### Dimensión: `dim_date`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| date_id | INTEGER | PK - Formato YYYYMMDD |
| date | DATE | Fecha |
| year | INTEGER | Año |
| month | INTEGER | Mes |
| day | INTEGER | Día |
| quarter | INTEGER | Trimestre |
| day_of_week | INTEGER | Día de la semana (0-6) |
| day_name | VARCHAR | Nombre del día |
| month_name | VARCHAR | Nombre del mes |
| is_weekend | BOOLEAN | Es fin de semana |
| week_of_year | INTEGER | Semana del año |

## Orquestación con Airflow

### DAG: `daily_etl_techmart`

```
start
  │
  ▼
┌─────────────────────────────────────┐
│           EXTRACT GROUP             │
│  (Ejecución paralela)               │
│  ┌───────────┐ ┌───────────┐       │
│  │extract_   │ │extract_   │       │
│  │orders     │ │products   │       │
│  └───────────┘ └───────────┘       │
│        ┌───────────┐               │
│        │extract_   │               │
│        │customers  │               │
│        └───────────┘               │
└─────────────────────────────────────┘
  │
  ▼
transform
  │
  ▼
load
  │
  ▼
validate
  │
  ▼
end
```

**Configuración:**
- **Schedule**: Diario a las 2:00 AM UTC
- **Retries**: 2 intentos con 5 minutos de espera
- **Alertas**: Email en caso de fallo

## Flujo de Datos

### Extracción

1. **Pedidos (API)**:
   - Endpoint: `GET /orders?date={execution_date}`
   - Autenticación: Bearer token
   - Timeout: 30 segundos
   - Reintentos: 3

2. **Productos (CSV)**:
   - Ruta: `/data/raw/products.csv`
   - Encoding: UTF-8
   - Validación de schema antes de procesamiento

3. **Clientes (PostgreSQL)**:
   - Query: Selección de clientes activos
   - Filtros opcionales: región, fecha de creación

### Transformación

1. **Limpieza**:
   - Eliminar duplicados por clave primaria
   - Corregir valores inválidos (ej: stock negativo → 0)
   - Normalizar strings (trim, lowercase emails)
   - Rellenar valores nulos con defaults

2. **Enriquecimiento**:
   - Join pedidos + productos (por product_id)
   - Join pedidos + clientes (por customer_id)
   - Generar `date_id` (YYYYMMDD) a partir de `order_date` para enlace con `dim_date`
   - Calcular order_total = quantity × unit_price
   - Calcular descuentos según reglas de negocio

3. **Agregaciones**:
   - Ventas por producto (total_quantity, total_revenue)
   - Ventas por cliente (total_spent, order_count, AOV)
   - KPIs: total_revenue, completion_rate, unique_customers

### Carga

1. **Validación de dimensiones**:
   - Claves únicas y no nulas
   - Schema correcto

2. **Carga de dimensiones**:
   - Upsert (insert nuevos, update existentes)
   - Generación de dim_date para rango de fechas

3. **Carga de hechos**:
   - Validación de foreign keys (`product_id`, `customer_id`, `date_id`)
   - Cálculo de métricas agregadas

### Validación Post-Carga

- DataFrame no vacío
- Columnas requeridas presentes
- Sin nulos en columnas críticas
- Valores en rangos válidos
- Claves únicas en dimensiones

## Manejo de Errores

### Estrategia de Reintentos

```python
{
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
```

### Logging

Todos los componentes usan logging estructurado JSON:

```json
{
    "timestamp": "2024-01-15T10:30:00.000Z",
    "level": "INFO",
    "logger": "etl.extract_orders",
    "message": "Step 'extract_orders': completed",
    "step": "extract_orders",
    "status": "completed",
    "rows": 1500
}
```

### Alertas

- **Email**: Notificación automática en fallos
- **Métricas**: Contadores de registros procesados
- **Validación**: Checks de calidad con umbral de error

## Consideraciones de Rendimiento

### Optimizaciones Aplicadas

1. **Extracción paralela**: Los 3 extractores corren simultáneamente
2. **Formato Parquet**: Compresión eficiente para staging
3. **Batch processing**: Procesamiento en lotes para grandes volúmenes
4. **Indexación**: Claves primarias y foreign keys indexadas

### Escalabilidad

- **Horizontal**: Múltiples workers de Airflow
- **Vertical**: Incremento de recursos por tarea
- **Particionado**: Tablas particionadas por fecha (futuro)

## Seguridad

- **Credenciales**: Variables de Airflow (no hardcoded)
- **Conexiones**: SSL/TLS para todas las fuentes
- **Logs**: Sin información sensible (PII sanitizado)
- **Acceso**: RBAC en Airflow para control de usuarios
