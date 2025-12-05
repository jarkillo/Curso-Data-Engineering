# Proyecto Práctico: Procesamiento Batch con PySpark

Sistema de procesamiento batch para análisis de ventas de e-commerce usando Apache Spark.

## Objetivos

- Procesar datos de ventas en formato CSV/Parquet
- Calcular métricas de negocio (revenue, AOV, top productos)
- Generar reportes agregados por diferentes dimensiones
- Escribir resultados optimizados para análisis

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── spark_session.py      # Configuración de SparkSession
│   ├── transformations.py    # Transformaciones de datos
│   ├── aggregations.py       # Agregaciones y métricas
│   └── io_utils.py           # Lectura/escritura de datos
├── tests/
│   ├── __init__.py
│   ├── test_transformations.py
│   └── test_aggregations.py
├── data/
│   └── sample_sales.csv      # Datos de ejemplo
├── output/                   # Resultados procesados
├── requirements.txt
└── README.md
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\Activate.ps1

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```python
from src.spark_session import create_spark_session
from src.transformations import clean_sales_data
from src.aggregations import calculate_revenue_metrics

# Crear sesión
spark = create_spark_session("SalesAnalysis")

# Leer datos
df = spark.read.csv("data/sample_sales.csv", header=True, inferSchema=True)

# Procesar
df_clean = clean_sales_data(df)
metrics = calculate_revenue_metrics(df_clean)

# Guardar
metrics.write.parquet("output/revenue_metrics.parquet")
```

## Ejecutar Tests

```bash
pytest -v --cov=src tests/
```

## Tecnologías

- Python 3.11+
- PySpark 3.5.0
- pytest

## Estado

🚧 En desarrollo
