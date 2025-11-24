# Proyecto Integrador: Pipeline de Análisis de Noticias

Pipeline completo de datos con arquitectura Bronze/Silver/Gold para extracción, transformación, validación y carga de noticias.

## 🎯 Objetivos

- Implementar pipeline completo **ETL** con arquitectura **Bronze/Silver/Gold**
- **Extraer** datos desde API simulada
- **Transformar** datos con limpieza, normalización y agregaciones
- **Validar** calidad de datos con Pandera
- **Cargar** datos en **Parquet** y **bases de datos relacionales**
- Aplicar **TDD** con >80% de cobertura
- Crear **CLI** para ejecución fácil

## 📚 Arquitectura Bronze/Silver/Gold

### Bronze (Raw Data)
- Datos crudos tal como llegan de la fuente
- Sin transformaciones
- Guardado en Parquet para trazabilidad
- Columnas: `id`, `title`, `content`, `author`, `published_date`, `source`, `category`, `url`

### Silver (Cleaned Data)
- Datos limpios y normalizados
- Validados contra esquema
- Tipos de datos correctos
- Registros inválidos eliminados
- Columnas en español, fechas como datetime
- Métricas básicas agregadas (longitud de contenido/título)

### Gold (Analytics-Ready Data)
- Datos agregados y optimizados para análisis
- Agregaciones por fuente y categoría
- Estadísticas descriptivas
- Cargado en BD para consultas rápidas

## 📁 Estructura del Proyecto

```
05-proyecto-integrador/
├── src/
│   ├── __init__.py
│   ├── extractor.py              # Extracción de noticias
│   ├── transformador_bronze.py   # Bronze → Silver
│   ├── transformador_silver.py   # Silver → Gold
│   ├── validador.py              # Validación de calidad
│   ├── cargador.py               # Carga en Parquet/BD
│   ├── pipeline.py               # Orquestador principal
│   └── cli.py                    # Interface de línea de comandos
├── tests/
│   ├── conftest.py               # Fixtures compartidos
│   ├── test_extractor.py         # 11 tests
│   ├── test_transformador_bronze.py  # 17 tests
│   ├── test_transformador_silver.py  # 15 tests
│   ├── test_validador.py         # 12 tests
│   ├── test_cargador.py          # 14 tests
│   └── test_pipeline.py          # 3 tests
├── data/
│   ├── bronze/                   # Datos crudos
│   ├── silver/                   # Datos limpios
│   └── gold/                     # Datos agregados
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Instalación

```bash
# Activar entorno virtual
cd modulo-03-ingenieria-datos/05-proyecto-integrador

# En Windows:
..\..\..\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html --cov-report=term

# Solo un módulo
pytest tests/test_pipeline.py -v
```

**Resultados**:
- ✅ **72 tests pasando** (100% success rate)
- ✅ **83% cobertura** (objetivo: ≥80%)

## 🎮 Uso del Pipeline

### Opción 1: CLI (Recomendado)

```bash
# Uso básico
python -m src.cli

# Personalizar parámetros
python -m src.cli --num-noticias 500 --db-url sqlite:///mi_base.db --output-dir mi_data

# Ver ayuda
python -m src.cli --help
```

**Parámetros CLI**:
- `--num-noticias`: Número de noticias a generar (default: 100)
- `--db-url`: URL de conexión a BD (default: `sqlite:///noticias.db`)
- `--output-dir`: Directorio de salida (default: `data`)
- `--guardar-intermedios/--no-guardar-intermedios`: Guardar capas intermedias (default: True)

### Opción 2: Desde Python

```python
from sqlalchemy import create_engine
from pathlib import Path
from src.pipeline import ejecutar_pipeline_completo

# Configurar
engine = create_engine("sqlite:///noticias.db")
directorio = Path("data")

# Ejecutar pipeline
resultado = ejecutar_pipeline_completo(
    num_noticias=100,
    engine=engine,
    directorio_salida=directorio,
    guardar_intermedios=True
)

# Ver resultados
print(f"Éxito: {resultado['exito']}")
print(f"Registros extraídos: {resultado['registros_extraidos']}")
print(f"Registros Silver: {resultado['registros_silver']}")
print(f"Registros Gold: {resultado['registros_gold']}")
```

## 📦 Módulos Implementados

### 1. Extractor (`extractor.py`)

Extrae noticias desde API simulada y las guarda en capa Bronze.

```python
from src.extractor import extraer_noticias_api_simulada, guardar_en_bronze
from pathlib import Path

# Generar 50 noticias simuladas
df_bronze = extraer_noticias_api_simulada(num_noticias=50)

# Guardar en Bronze
guardar_en_bronze(df_bronze, Path("data/bronze/noticias.parquet"))
```

### 2. Transformador Bronze (`transformador_bronze.py`)

Transforma datos crudos a datos limpios (Bronze → Silver).

```python
from src.transformador_bronze import transformar_bronze_a_silver

# Transformar
df_silver = transformar_bronze_a_silver(df_bronze)

# Ahora tiene:
# - Columnas en español
# - Fechas como datetime
# - Textos limpios
# - Registros inválidos eliminados
# - Métricas de longitud
```

### 3. Transformador Silver (`transformador_silver.py`)

Transforma datos limpios a datos analíticos (Silver → Gold).

```python
from src.transformador_silver import transformar_silver_a_gold

# Transformar
datos_gold = transformar_silver_a_gold(df_silver)

# Retorna dict con:
# - datos_gold["por_fuente"]: DataFrame agregado por fuente
# - datos_gold["por_categoria"]: DataFrame agregado por categoría
# - datos_gold["estadisticas"]: Dict con estadísticas descriptivas
```

### 4. Validador (`validador.py`)

Valida calidad de datos con Pandera.

```python
from src.validador import generar_reporte_calidad

# Generar reporte de calidad
reporte = generar_reporte_calidad(df_silver)

print(f"Esquema válido: {reporte['esquema_valido']}")
print(f"Duplicados: {reporte['duplicados']['total']}")
print(f"Longitudes válidas (contenido): {reporte['longitudes_validas']['contenido']}")
```

### 5. Cargador (`cargador.py`)

Carga datos en Parquet y bases de datos.

```python
from src.cargador import cargar_a_parquet, cargar_a_base_datos
from pathlib import Path

# Cargar en Parquet
cargar_a_parquet(df_gold, Path("data/gold/noticias_gold.parquet"))

# Cargar en base de datos
num_cargados = cargar_a_base_datos(
    df_gold,
    engine,
    tabla="noticias_gold",
    if_exists="replace"
)
```

## 🧪 Cobertura de Tests

Módulo | Tests | Cobertura
-------|-------|----------
`extractor.py` | 11 | 100%
`transformador_bronze.py` | 17 | 100%
`transformador_silver.py` | 15 | 100%
`validador.py` | 12 | 100%
`cargador.py` | 14 | 94%
`pipeline.py` | 3 | 100%
**TOTAL** | **72** | **83%**

## 🎓 Conceptos Aplicados

### Arquitectura de Datos
- **Bronze/Silver/Gold** (Medallion Architecture)
- Separación de capas por nivel de procesamiento
- Trazabilidad completa de datos

### Calidad de Datos
- Validación de esquemas con **Pandera**
- Detección de duplicados
- Validación de rangos
- Reporte completo de calidad

### Buenas Prácticas
- **TDD** (Test-Driven Development)
- Type hints en todas las funciones
- Docstrings con ejemplos
- Logging estructurado
- Manejo robusto de errores
- Cobertura >80%

### Data Engineering
- ETL completo
- Procesamiento por lotes
- Persistencia dual (Parquet + BD)
- Pipeline idempotente
- Métricas de ejecución

## 🔧 Tecnologías Utilizadas

- **Python 3.13+**
- **Pandas**: Manipulación de datos
- **Pandera**: Validación de esquemas
- **SQLAlchemy**: ORM y conexión a BD
- **PyArrow**: Formato Parquet
- **Click**: CLI
- **Faker**: Generación de datos sintéticos
- **pytest**: Testing

## 📊 Ejemplo de Salida

```bash
$ python -m src.cli --num-noticias 100

============================================================
Pipeline de Análisis de Noticias
============================================================
Noticias: 100
Base de datos: sqlite:///noticias.db
Directorio salida: data
============================================================

▶ Ejecutando pipeline...
2025-11-11 15:30:00 - INFO - === Iniciando pipeline completo ===
2025-11-11 15:30:00 - INFO - Extrayendo 100 noticias...
2025-11-11 15:30:00 - INFO - Bronze guardado en data\bronze\noticias.parquet
2025-11-11 15:30:01 - INFO - Transformando Bronze → Silver...
2025-11-11 15:30:01 - INFO - Silver guardado in data\silver\noticias.parquet
2025-11-11 15:30:01 - INFO - Validando calidad de datos...
2025-11-11 15:30:01 - INFO - Esquema válido: True
2025-11-11 15:30:01 - INFO - Transformando Silver → Gold...
2025-11-11 15:30:01 - INFO - Cargando datos Gold...
2025-11-11 15:30:02 - INFO - === Pipeline completado exitosamente ===

✅ Pipeline completado exitosamente

📊 Métricas:
  - Registros extraídos: 100
  - Registros Silver: 98
  - Registros Gold: 5

🔍 Calidad de datos:
  - Esquema válido: ✅
  - Duplicados: 0

📁 Datos guardados en: data
```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandera'"
**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'data/...'"
**Solución**: Los directorios se crean automáticamente. Verificar permisos de escritura.

### Error: Base de datos bloqueada
**Solución**: Cerrar todas las conexiones antes de ejecutar nuevamente:
```python
engine.dispose()
```

## 📚 Recursos Adicionales

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandera Validation](https://pandera.readthedocs.io/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/)
- [Parquet Format](https://parquet.apache.org/)

## 🎯 Próximos Pasos

1. Conectar a API real de noticias (NewsAPI, Guardian, etc.)
2. Implementar procesamiento incremental
3. Agregar análisis de sentimiento
4. Crear dashboard con visualizaciones
5. Desplegar en producción (Airflow, Prefect)

---

**Proyecto completado** ✅
**Tests**: 72/72 pasando
**Cobertura**: 83%
**Calidad**: Excelente

**¡Éxito con tu aprendizaje de Data Engineering!** 🚀📊
