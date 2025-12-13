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
├── data/
│   ├── raw/                  # Datos crudos
│   └── processed/            # Datos procesados
├── docker/
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
from src.extractors import extract_all_sources
from src.transformers import transform_data
from src.loaders import load_to_warehouse

# 1. Extracción
raw_data = extract_all_sources(
    api_url="http://api.techmart.local/orders",
    csv_path="data/raw/products.csv",
    db_connection_string="postgresql://..."
)

# 2. Transformación
transformed_data = transform_data(raw_data)

# 3. Carga
load_to_warehouse(transformed_data, target_schema="analytics")
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
| `enrichment` | Enriquecimiento | Joins, lookups, cálculos |
| `aggregations` | Agregaciones | Métricas, KPIs, rollups |

### Cargadores

| Módulo | Descripción | Destino |
|--------|-------------|---------|
| `warehouse_loader` | Carga dimensional | Star schema DW |

## Data Warehouse Schema

### Dimensiones

- **dim_product**: Productos con categorías y atributos
- **dim_customer**: Clientes con segmentación
- **dim_date**: Calendario con atributos temporales

### Hechos

- **fact_sales**: Ventas con métricas (cantidad, revenue, descuentos)

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
