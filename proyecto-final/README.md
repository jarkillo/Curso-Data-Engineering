# Proyecto Final: Pipeline ETL de E-commerce Analytics

Pipeline ETL completo end-to-end que extrae datos de múltiples fuentes, los transforma y carga en un data warehouse dimensional para análisis de negocio.

## Caso de Uso: TechMart Analytics

**TechMart** es un e-commerce de tecnología que necesita consolidar datos de:
- **API de pedidos**: Sistema de ventas en tiempo real
- **CSV de productos**: Catálogo actualizado diariamente
- **Base de datos de clientes**: PostgreSQL con información de usuarios

El objetivo es construir un data warehouse que permita:
- Análisis de ventas por producto, categoría y región
- Segmentación de clientes por comportamiento de compra
- Detección de tendencias y patrones estacionales
- KPIs de negocio: revenue, AOV, conversion rate

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FUENTES DE DATOS                            │
├─────────────────┬─────────────────┬─────────────────────────────────┤
│   API Pedidos   │   CSV Productos │      PostgreSQL Clientes        │
│   (REST JSON)   │   (catálogo)    │         (transaccional)         │
└────────┬────────┴────────┬────────┴────────────────┬────────────────┘
         │                 │                         │
         ▼                 ▼                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTRACCIÓN (Extract)                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────────┐ │
│  │ api_extractor│ │ csv_extractor│ │      db_extractor            │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TRANSFORMACIÓN (Transform)                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────────┐ │
│  │   cleaning   │ │  enrichment  │ │      aggregations            │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CARGA (Load)                                │
│           Data Warehouse Dimensional (Star Schema)                  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────┐   │
│  │ dim_product│ │dim_customer│ │  dim_date  │ │  fact_sales    │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ORQUESTACIÓN                                  │
│                     Apache Airflow DAGs                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  daily_etl_dag: extract → transform → load → validate        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Estructura del Proyecto

```
proyecto-final/
├── src/
│   ├── __init__.py
│   ├── extractors/           # Módulos de extracción
│   │   ├── __init__.py
│   │   ├── api_extractor.py
│   │   ├── csv_extractor.py
│   │   └── db_extractor.py
│   ├── transformers/         # Módulos de transformación
│   │   ├── __init__.py
│   │   ├── cleaning.py
│   │   ├── enrichment.py
│   │   └── aggregations.py
│   ├── loaders/              # Módulos de carga
│   │   ├── __init__.py
│   │   └── warehouse_loader.py
│   ├── models/               # Modelos de datos
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/                # Utilidades
│       ├── __init__.py
│       ├── logging_config.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_extractors.py
│   ├── test_transformers.py
│   ├── test_loaders.py
│   └── test_validators.py
├── dags/
│   └── daily_etl_dag.py      # DAG de Airflow
├── data/                     # Creado durante setup
│   ├── raw/                  # Datos crudos
│   └── processed/            # Datos procesados
├── docker/                   # Creado durante despliegue
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── architecture.md
│   └── deployment_guide.md
├── requirements.txt
└── README.md
```

## Instalación

### Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- PostgreSQL 15+ (o usar Docker)

### Setup Local

```bash
# Clonar repositorio
cd proyecto-final

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Levantar servicios con Docker
docker-compose -f docker/docker-compose.yml up -d
```

## Ejecutar Tests

```bash
# Tests con cobertura
pytest --cov=src --cov-report=html --cov-report=term-missing

# Solo tests unitarios
pytest tests/ -v

# Tests con marcadores específicos
pytest -m "not integration"
```

## Uso

### Ejecutar Pipeline Completo

```python
from src.extractors import (
    extract_orders_from_api,
    extract_products_from_csv,
    extract_customers_from_db,
)
from src.transformers import (
    clean_orders, clean_products, clean_customers,
    enrich_orders_with_products, enrich_orders_with_customers,
    add_date_id, calculate_order_metrics,
)
from src.loaders import load_dimension, load_fact_table, create_dim_date

# 1. Extracción
orders_df = extract_orders_from_api("http://api.techmart.local/orders")
products_df = extract_products_from_csv("data/raw/products.csv")
customers_df = extract_customers_from_db("postgresql://...")

# 2. Transformación
clean_orders_df = clean_orders(orders_df)
clean_products_df = clean_products(products_df)
clean_customers_df = clean_customers(customers_df)

enriched_df = enrich_orders_with_products(clean_orders_df, clean_products_df)
enriched_df = enrich_orders_with_customers(enriched_df, clean_customers_df)
enriched_df = add_date_id(enriched_df)  # Genera date_id para dim_date
enriched_df = calculate_order_metrics(enriched_df)

# 3. Carga
dim_date = create_dim_date("2024-01-01", "2024-12-31")
load_dimension(clean_products_df, "warehouse/dim_product.parquet", "product_id", "dim_product")
load_dimension(clean_customers_df, "warehouse/dim_customer.parquet", "customer_id", "dim_customer")
load_dimension(dim_date, "warehouse/dim_date.parquet", "date_id", "dim_date")
load_fact_table(
    enriched_df,
    "warehouse/fact_sales.parquet",
    foreign_keys=["product_id", "customer_id", "date_id"],
    measures=["quantity", "order_total"],
    fact_name="fact_sales",
)
```

### Ejecutar con Airflow

```bash
# Iniciar Airflow
airflow standalone

# El DAG daily_etl_dag se ejecutará automáticamente
# o puedes dispararlo manualmente desde la UI
```

## Módulos Implementados

### Extractores

| Módulo | Descripción | Fuente |
|--------|-------------|--------|
| `api_extractor` | Extrae pedidos de API REST | JSON API |
| `csv_extractor` | Lee catálogo de productos | CSV files |
| `db_extractor` | Consulta datos de clientes | PostgreSQL |

### Transformadores

| Módulo | Descripción | Operaciones |
|--------|-------------|-------------|
| `cleaning` | Limpieza de datos | Nulls, duplicados, tipos |
| `enrichment` | Enriquecimiento | Joins, date_id, métricas |
| `aggregations` | Agregaciones | Métricas, KPIs, rollups |

**Funciones principales de enrichment:**
- `enrich_orders_with_products()` - Join con catálogo de productos
- `enrich_orders_with_customers()` - Join con datos de clientes
- `add_date_id()` - Genera `date_id` (YYYYMMDD) para enlace con `dim_date`
- `calculate_order_metrics()` - Calcula totales y descuentos

### Cargadores

| Módulo | Descripción | Destino |
|--------|-------------|---------|
| `warehouse_loader` | Carga dimensional | Star schema DW |

## Data Warehouse Schema (Star Schema)

### Dimensiones

- **dim_product**: Productos con categorías y atributos (`product_id` PK)
- **dim_customer**: Clientes con segmentación (`customer_id` PK)
- **dim_date**: Calendario con atributos temporales (`date_id` PK, formato YYYYMMDD)

### Tabla de Hechos

- **fact_sales**: Ventas con métricas
  - Foreign Keys: `product_id`, `customer_id`, `date_id`
  - Measures: `quantity`, `order_total`, `discount_amount`

```
            dim_product
                 │
                 │ product_id
                 ▼
dim_date ──── fact_sales ──── dim_customer
  date_id        │              customer_id
                 │
            (measures)
```

## Monitoreo

El pipeline incluye:
- **Logging estructurado**: JSON logs con contexto
- **Métricas**: Contadores de registros, tiempos de ejecución
- **Alertas**: Notificaciones por email/Slack en errores
- **Validación**: Checks de calidad de datos post-carga

## Documentación Adicional

- [Arquitectura Detallada](docs/architecture.md)
- [Guía de Despliegue](docs/deployment_guide.md)

## Tecnologías Utilizadas

- **Python 3.11**: Lenguaje principal
- **pandas**: Manipulación de datos
- **SQLAlchemy**: ORM y conexiones DB
- **Apache Airflow**: Orquestación
- **PostgreSQL**: Base de datos
- **Docker**: Containerización
- **pytest**: Testing

## Autor

Proyecto Final del Máster en Ingeniería de Datos con IA
