# Proyecto Práctico: Sistema de Análisis de Logs con MongoDB

Sistema para procesar, analizar y detectar anomalías en logs de aplicaciones usando MongoDB y agregaciones complejas.

## 🎯 Objetivos

- **Procesar logs** con estructura flexible de MongoDB (documentos)
- **Construir pipelines de agregación** complejos ($match, $group, $project, $sort)
- **Analizar datos** para identificar servicios críticos y anomalías
- **Aplicar TDD** con >80% de cobertura de código
- **Dominar MongoDB** a través de un caso de uso real

## 📚 Conceptos Aplicados

### MongoDB
- **Documentos flexibles**: Logs con estructura variable
- **Operadores de agregación**: $group, $match, $project, $sort, $limit
- **Análisis temporal**: $hour, $dayOfWeek, $dateFromString
- **Operadores condicionales**: $cond, $eq para conteos selectivos

### Análisis de Logs
- **Parsing**: Extracción de componentes de logs estructurados
- **Validación**: Verificación de campos obligatorios
- **Métricas**: Tasa de error, servicios críticos
- **Detección de anomalías**: Tiempos de respuesta altos, errores concentrados

### Buenas Prácticas
- **TDD (Test-Driven Development)**: 56 tests implementados antes del código
- **Type Hints**: Tipado explícito en todas las funciones
- **Funciones puras**: Sin efectos secundarios
- **Cobertura >80%**: 99% alcanzado

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── log_processor.py         # Procesamiento de logs (33 líneas, 100% cov)
│   ├── aggregation_builder.py   # Construcción de pipelines (25 líneas, 96% cov)
│   └── analytics.py              # Análisis y métricas (62 líneas, 100% cov)
├── tests/
│   ├── __init__.py
│   ├── test_log_processor.py        # 19 tests
│   ├── test_aggregation_builder.py  # 18 tests
│   └── test_analytics.py            # 19 tests
├── data/
│   └── (logs de ejemplo)
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Instalación

```bash
# Activar entorno virtual
cd modulo-05-bases-datos-avanzadas/tema-2-mongodb/04-proyecto-practico

# En Windows:
..\..\..\..\.venv\Scripts\Activate.ps1

# En Linux/Mac:
source ../../../../.venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Ejecutar Tests

```bash
# Todos los tests
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html --cov-report=term

# Solo un módulo
pytest tests/test_log_processor.py -v
```

**Resultados**:
- ✅ **56 tests pasando** (100% success rate)
- ✅ **99% cobertura** (supera objetivo ≥80%)
- ✅ **121 statements**, solo 1 miss

## 📦 Módulos Implementados

### 1. Log Processor (`log_processor.py`)

Funciones para procesar entradas de logs.

#### `parsear_log_entry(log_string: str) -> dict[str, str]`

Parsea un string de log en documento estructurado.

```python
from src.log_processor import parsear_log_entry

# Ejemplo
log = "2024-11-12 14:30:45 | ERROR | UserService | Database connection failed"
resultado = parsear_log_entry(log)

print(resultado)
# {
#     'timestamp': '2024-11-12 14:30:45',
#     'nivel': 'ERROR',
#     'servicio': 'UserService',
#     'mensaje': 'Database connection failed'
# }
```

#### `validar_log_entry(log_entry: dict) -> None`

Valida que un log tenga todos los campos obligatorios.

```python
from src.log_processor import validar_log_entry

log_entry = {
    "timestamp": "2024-11-12 14:30:45",
    "nivel": "ERROR",
    "servicio": "UserService",
    "mensaje": "Test"
}

validar_log_entry(log_entry)  # No lanza error si es válido
```

#### `normalizar_timestamp(timestamp_str: str) -> datetime`

Convierte timestamp string a objeto datetime.

```python
from src.log_processor import normalizar_timestamp

timestamp_str = "2024-11-12 14:30:45"
dt = normalizar_timestamp(timestamp_str)

print(dt)  # datetime.datetime(2024, 11, 12, 14, 30, 45)
```

#### `extraer_nivel_severidad(log_entry: dict) -> str`

Extrae y valida el nivel de severidad.

```python
from src.log_processor import extraer_nivel_severidad

log_entry = {"nivel": "ERROR"}
nivel = extraer_nivel_severidad(log_entry)

print(nivel)  # 'ERROR'
```

---

### 2. Aggregation Builder (`aggregation_builder.py`)

Funciones para construir pipelines de agregación de MongoDB.

#### `construir_pipeline_errores(fecha_inicio: str, fecha_fin: str) -> list[dict]`

Construye pipeline para filtrar y agrupar errores por período.

```python
from src.aggregation_builder import construir_pipeline_errores

pipeline = construir_pipeline_errores("2024-11-01", "2024-11-30")

# Uso con MongoDB
# db.logs.aggregate(pipeline)

print(pipeline[0])
# {
#     '$match': {
#         'nivel': 'ERROR',
#         'timestamp': {'$gte': '2024-11-01', '$lte': '2024-11-30'}
#     }
# }
```

#### `construir_pipeline_por_servicio() -> list[dict]`

Construye pipeline para agrupar logs por servicio con métricas de error.

```python
from src.aggregation_builder import construir_pipeline_por_servicio

pipeline = construir_pipeline_por_servicio()

# Uso con MongoDB
# db.logs.aggregate(pipeline)

# Retorna:
# [
#     {'servicio': 'UserService', 'total_logs': 1500, 'porcentaje_error': 12.5},
#     {'servicio': 'PaymentService', 'total_logs': 800, 'porcentaje_error': 5.2},
#     ...
# ]
```

#### `construir_pipeline_top_usuarios(limite: int) -> list[dict]`

Construye pipeline para obtener top usuarios con más actividad.

```python
from src.aggregation_builder import construir_pipeline_top_usuarios

pipeline = construir_pipeline_top_usuarios(10)

# db.logs.aggregate(pipeline)

# Retorna top 10 usuarios:
# [
#     {'usuario_id': 'user_123', 'total_acciones': 450, 'cantidad_servicios': 8},
#     ...
# ]
```

#### `construir_pipeline_metricas_tiempo() -> list[dict]`

Construye pipeline para analizar métricas por período de tiempo.

```python
from src.aggregation_builder import construir_pipeline_metricas_tiempo

pipeline = construir_pipeline_metricas_tiempo()

# db.logs.aggregate(pipeline)

# Retorna métricas por hora:
# [
#     {'hora': 0, 'total_logs': 120, 'errores': 5, 'warnings': 15},
#     {'hora': 1, 'total_logs': 98, 'errores': 2, 'warnings': 8},
#     ...
# ]
```

---

### 3. Analytics (`analytics.py`)

Funciones para analizar logs y detectar problemas.

#### `calcular_tasa_error(logs: list[dict]) -> float`

Calcula la tasa de error como porcentaje del total.

```python
from src.analytics import calcular_tasa_error

logs = [
    {"nivel": "ERROR"},
    {"nivel": "ERROR"},
    {"nivel": "INFO"},
    {"nivel": "WARNING"},
    {"nivel": "INFO"},
]

tasa = calcular_tasa_error(logs)
print(tasa)  # 40.0 (2 errores de 5 logs)
```

#### `identificar_servicios_criticos(logs: list[dict], umbral_error: float) -> list[dict]`

Identifica servicios con tasa de error por encima del umbral.

```python
from src.analytics import identificar_servicios_criticos

logs = [
    {"servicio": "UserService", "nivel": "ERROR"},
    {"servicio": "UserService", "nivel": "ERROR"},
    {"servicio": "UserService", "nivel": "INFO"},
    {"servicio": "PaymentService", "nivel": "INFO"},
    {"servicio": "PaymentService", "nivel": "INFO"},
]

criticos = identificar_servicios_criticos(logs, umbral_error=50.0)

print(criticos)
# [
#     {
#         'servicio': 'UserService',
#         'total_logs': 3,
#         'total_errores': 2,
#         'tasa_error': 66.67
#     }
# ]
```

#### `generar_reporte_resumen(logs: list[dict]) -> dict`

Genera un reporte resumen con métricas generales.

```python
from src.analytics import generar_reporte_resumen

logs = [
    {"nivel": "ERROR", "servicio": "Service1"},
    {"nivel": "INFO", "servicio": "Service2"},
    {"nivel": "WARNING", "servicio": "Service1"},
    {"nivel": "INFO", "servicio": "Service2"},
]

reporte = generar_reporte_resumen(logs)

print(reporte)
# {
#     'total_logs': 4,
#     'errores': 1,
#     'warnings': 1,
#     'info': 2,
#     'servicios_unicos': 2,
#     'tasa_error': 25.0
# }
```

#### `detectar_anomalias(logs: list[dict], umbral_tiempo: int) -> list[dict]`

Detecta anomalías en logs (tiempos altos, errores concentrados).

```python
from src.analytics import detectar_anomalias

logs = [
    {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 100},
    {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 120},
    {"servicio": "Service1", "nivel": "WARNING", "tiempo_respuesta": 5000},
]

anomalias = detectar_anomalias(logs, umbral_tiempo=1000)

print(len(anomalias))  # 1
print(anomalias[0]["tiempo_respuesta"])  # 5000
```

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Análisis completo de logs de un servicio

```python
from src.log_processor import parsear_log_entry
from src.analytics import calcular_tasa_error, identificar_servicios_criticos

# Logs en formato string
logs_raw = [
    "2024-11-12 14:30:45 | ERROR | UserService | Connection timeout",
    "2024-11-12 14:31:12 | ERROR | UserService | Query failed",
    "2024-11-12 14:32:05 | INFO | UserService | Request processed",
    "2024-11-12 14:33:20 | WARNING | PaymentService | Slow response",
    "2024-11-12 14:34:15 | INFO | PaymentService | Payment completed",
]

# Parsear logs
logs = [parsear_log_entry(log) for log in logs_raw]

# Calcular tasa de error
tasa = calcular_tasa_error(logs)
print(f"Tasa de error: {tasa}%")  # 40.0%

# Identificar servicios críticos
criticos = identificar_servicios_criticos(logs, umbral_error=50.0)

for servicio in criticos:
    print(f"\n⚠️ Servicio Crítico: {servicio['servicio']}")
    print(f"   Total logs: {servicio['total_logs']}")
    print(f"   Errores: {servicio['total_errores']}")
    print(f"   Tasa error: {servicio['tasa_error']}%")
```

### Ejemplo 2: Construir pipeline para análisis en MongoDB

```python
from src.aggregation_builder import (
    construir_pipeline_errores,
    construir_pipeline_por_servicio
)
from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logs_db"]

# Pipeline para errores del último mes
pipeline_errores = construir_pipeline_errores("2024-11-01", "2024-11-30")
errores = list(db.logs.aggregate(pipeline_errores))

print("Servicios con más errores:")
for item in errores[:5]:
    print(f"- {item['_id']}: {item['total_errores']} errores")

# Pipeline para análisis por servicio
pipeline_servicios = construir_pipeline_por_servicio()
servicios = list(db.logs.aggregate(pipeline_servicios))

print("\nEstadísticas por servicio:")
for servicio in servicios:
    print(f"\n{servicio['servicio']}:")
    print(f"  Total logs: {servicio['total_logs']}")
    print(f"  % Error: {servicio['porcentaje_error']:.2f}%")
```

### Ejemplo 3: Detección de anomalías en tiempo real

```python
from src.analytics import detectar_anomalias, generar_reporte_resumen

# Simular logs en tiempo real
logs_tiempo_real = [
    {"servicio": "API", "nivel": "INFO", "tiempo_respuesta": 120},
    {"servicio": "API", "nivel": "INFO", "tiempo_respuesta": 135},
    {"servicio": "API", "nivel": "WARNING", "tiempo_respuesta": 4500},  # Anomalía
    {"servicio": "Database", "nivel": "INFO", "tiempo_respuesta": 50},
    {"servicio": "Database", "nivel": "ERROR", "tiempo_respuesta": 8000},  # Anomalía
]

# Detectar anomalías
anomalias = detectar_anomalias(logs_tiempo_real, umbral_tiempo=1000)

if anomalias:
    print(f"⚠️ Se detectaron {len(anomalias)} anomalías:")
    for anomalia in anomalias:
        print(f"\n  Servicio: {anomalia['servicio']}")
        print(f"  Nivel: {anomalia['nivel']}")
        print(f"  Tiempo: {anomalia['tiempo_respuesta']}ms")

# Generar reporte
reporte = generar_reporte_resumen(logs_tiempo_real)
print(f"\nReporte General:")
print(f"  Total logs: {reporte['total_logs']}")
print(f"  Tasa error: {reporte['tasa_error']}%")
print(f"  Servicios: {reporte['servicios_unicos']}")
```

---

## 🧪 Cobertura de Tests

```
Name                         Stmts   Miss  Cover
------------------------------------------------
src/__init__.py                  1      0   100%
src/aggregation_builder.py     25      1    96%
src/analytics.py                62      0   100%
src/log_processor.py            33      0   100%
------------------------------------------------
TOTAL                          121      1    99%
```

**Detalle por módulo**:

| Módulo | Tests | Cobertura | Estado |
|--------|-------|-----------|--------|
| `log_processor.py` | 19 | 100% | ✅ |
| `aggregation_builder.py` | 18 | 96% | ✅ |
| `analytics.py` | 19 | 100% | ✅ |
| **TOTAL** | **56** | **99%** | ✅ **SUPERADO** |

---

## 🔧 Tecnologías Utilizadas

- **Python 3.13+**: Lenguaje principal
- **pymongo**: Driver oficial de MongoDB para Python
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **faker**: Generación de datos de prueba
- **black**: Formateo automático
- **flake8**: Linting
- **mypy**: Type checking

---

## 📊 Arquitectura

### Diseño Funcional

El proyecto sigue un diseño **funcional puro**:
- **Sin clases** (solo funciones)
- **Funciones pequeñas** (<50 líneas)
- **Sin efectos secundarios**: Funciones predecibles
- **Composabilidad**: Funciones que se combinan fácilmente

### Flujo de Datos

```
┌──────────────────┐
│  Logs en string  │
└────────┬─────────┘
         │
         ▼
┌─────────────────────┐
│  log_processor.py   │  ← Parsea y valida
│  - parsear_log      │
│  - validar_log      │
│  - normalizar_fecha │
└────────┬────────────┘
         │
         ▼
┌────────────────────────┐
│  aggregation_builder   │  ← Construye pipelines
│  - pipeline_errores    │
│  - pipeline_servicios  │
│  - pipeline_usuarios   │
└────────┬───────────────┘
         │
         ▼
┌──────────────────┐
│   analytics.py   │  ← Analiza resultados
│  - tasa_error    │
│  - servicios     │
│  - anomalías     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Insights +      │
│  Reportes        │
└──────────────────┘
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pymongo'"
**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: Tests fallan con "ImportError"
**Solución**: Ejecutar desde el directorio del proyecto
```bash
cd modulo-05-bases-datos-avanzadas/tema-2-mongodb/04-proyecto-practico
pytest -v
```

### Error: "ValueError: Formato de log inválido"
**Solución**: Verificar formato del log
```python
# Formato correcto:
log = "YYYY-MM-DD HH:MM:SS | NIVEL | SERVICIO | MENSAJE"

# Ejemplo:
log = "2024-11-12 14:30:45 | ERROR | UserService | Connection failed"
```

---

## 📚 Recursos Adicionales

- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Aggregation Framework](https://www.mongodb.com/docs/manual/aggregation/)
- [MongoDB University](https://learn.mongodb.com/)
- [Aggregation Pipeline Builder](https://www.mongodb.com/docs/compass/current/aggregation-pipeline-builder/)

---

## 🎯 Próximos Pasos

1. Agregar **conexión real** a MongoDB
2. Implementar **streaming** de logs en tiempo real
3. Crear **dashboard** con visualizaciones
4. Agregar **alertas** automáticas por Slack/Email
5. Implementar **Machine Learning** para detección de anomalías avanzada
6. Exportar reportes a **PDF/Excel**

---

**Proyecto completado** ✅
**Tests**: 56/56 pasando (100%)
**Cobertura**: 99% (supera objetivo ≥80%)
**Calidad**: TDD con funciones puras

**¡Éxito en tu aprendizaje de MongoDB!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Modelado de Datos - 01 Teoria](../../tema-3-modelado-datos/01-TEORIA.md)
