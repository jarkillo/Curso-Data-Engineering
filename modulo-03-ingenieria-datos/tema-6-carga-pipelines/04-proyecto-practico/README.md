# Proyecto Práctico: Carga de Datos y Pipelines Completos

Sistema completo de carga de datos con múltiples estrategias, batch processing, logging y métricas para pipelines de producción.

## 🎯 Objetivos

- Implementar **3 estrategias de carga**: full load, incremental, upsert
- Procesar grandes datasets con **batch processing**
- Recolectar **métricas de rendimiento** (throughput, duración, éxito/fallo)
- Sistema de **checkpoint** para reanudar cargas
- **Selección automática** de estrategia según características del dataset
- Logging y manejo robusto de errores

## 📚 Conceptos Clave

### Full Load (Carga Completa)
Reemplaza todos los datos existentes con los nuevos. Simple pero costoso.

**Ventajas**: Simplicidad, consistencia garantizada
**Desventajas**: Lento, consume muchos recursos

### Incremental Load (Carga Incremental)
Solo procesa y carga registros nuevos desde el último checkpoint.

**Ventajas**: Rápido, eficiente, escalable
**Desventajas**: Requiere columna temporal, no maneja updates

### Upsert (Insert + Update)
Inserta registros nuevos y actualiza existentes.

**Ventajas**: Completo (inserts + updates), flexible
**Desventajas**: Más complejo, requiere clave única

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── cargador_full.py          # Estrategia full load
│   ├── cargador_incremental.py   # Estrategia incremental con checkpoint
│   ├── cargador_upsert.py        # Estrategia upsert
│   ├── batch_processor.py        # Procesamiento en lotes
│   ├── metrics_collector.py      # Recolección de métricas
│   └── pipeline_manager.py       # Orquestador principal
├── tests/
│   ├── conftest.py               # Fixtures compartidos
│   ├── test_cargador_full.py
│   ├── test_cargador_incremental.py
│   ├── test_cargador_upsert.py
│   ├── test_batch_processor.py
│   ├── test_metrics_collector.py
│   └── test_pipeline_manager.py
├── README.md
└── requirements.txt
```

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

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
pytest tests/test_cargador_full.py -v
```

## 📦 Funciones Implementadas

### 1. Cargador Full Load

```python
from sqlalchemy import create_engine
import pandas as pd
from src.cargador_full import full_load

# Crear engine
engine = create_engine("sqlite:///db.db")

# Datos
df = pd.DataFrame({
    "id": [1, 2, 3],
    "nombre": ["Ana", "Luis", "María"],
    "valor": [100, 200, 150]
})

# Full load
num_cargados = full_load(df, engine, "clientes")
print(f"Cargados: {num_cargados} registros")
```

### 2. Cargador Incremental

```python
from src.cargador_incremental import incremental_load

# Datos con timestamp
df = pd.DataFrame({
    "id": [1, 2, 3],
    "timestamp": pd.date_range("2024-01-15", periods=3, freq="h"),
    "valor": [100, 200, 300]
})

# Incremental load con checkpoint
resultado = incremental_load(
    df,
    engine,
    "logs",
    "timestamp",
    checkpoint_file="checkpoint_logs.txt"
)

print(f"Cargados: {resultado['cargados']}")
print(f"Omitidos: {resultado['omitidos']}")
```

### 3. Cargador Upsert

```python
from src.cargador_upsert import upsert_con_metricas

# Datos con ID único
df = pd.DataFrame({
    "id": [1, 2, 3],
    "nombre": ["Ana", "Luis Updated", "María"],
    "email": ["ana@email.com", "luis_new@email.com", "maria@email.com"]
})

# Upsert
resultado = upsert_con_metricas(df, engine, "usuarios", "id")

print(f"Inserts: {resultado['inserts']}")
print(f"Updates: {resultado['updates']}")
```

### 4. Batch Processing

```python
from src.batch_processor import procesar_en_lotes

# Dataset grande (10K filas)
df_grande = pd.DataFrame({
    "id": range(10000),
    "valor": range(10000)
})

# Procesar en lotes de 1K
resultado = procesar_en_lotes(
    df_grande,
    engine,
    "datos",
    batch_size=1000
)

print(f"Filas: {resultado['total_filas']}")
print(f"Lotes: {resultado['num_lotes']}")
print(f"Duración: {resultado['duration_seconds']}s")
```

### 5. Pipeline Completo

```python
from src.pipeline_manager import ejecutar_pipeline

# Pipeline automático (selecciona estrategia)
resultado = ejecutar_pipeline(
    df,
    engine,
    "ventas",
    estrategia="auto",        # Selección automática
    validar=True,             # Validar datos
    columnas_requeridas=["id", "fecha", "monto"],
    columnas_no_nulas=["id", "monto"]
)

print(f"Éxito: {resultado.success}")
print(f"Extraídos: {resultado.rows_extracted}")
print(f"Validados: {resultado.rows_validated}")
print(f"Cargados: {resultado.rows_loaded}")
print(f"Fallidos: {resultado.rows_failed}")
print(f"Duración: {resultado.duration_seconds:.2f}s")
```

## 🎓 Ejemplos de Uso

### Ejemplo 1: Pipeline de Ventas Diarias (Full Load)

```python
from sqlalchemy import create_engine
import pandas as pd
from src.cargador_full import full_load_con_validacion

# Datos de ventas del día
ventas = pd.DataFrame({
    "id_venta": [1, 2, 3],
    "fecha": ["2024-01-15"] * 3,
    "producto": ["Laptop", "Mouse", "Teclado"],
    "monto": [1200.00, 25.00, 80.00]
})

engine = create_engine("sqlite:///ventas.db")

# Full load con validación
resultado = full_load_con_validacion(
    ventas,
    engine,
    "ventas_diarias",
    columnas_requeridas=["id_venta", "fecha", "producto", "monto"]
)

if resultado["valido"]:
    print(f"✅ {resultado['cargados']} ventas cargadas")
else:
    print(f"❌ Error: {resultado['mensaje']}")
```

### Ejemplo 2: Logs de Aplicación (Incremental)

```python
from src.cargador_incremental import incremental_load_con_validacion

# Logs nuevos cada hora
logs = pd.DataFrame({
    "id_log": range(1, 101),
    "timestamp": pd.date_range("2024-01-15 10:00", periods=100, freq="min"),
    "nivel": ["INFO"] * 100,
    "mensaje": [f"Log {i}" for i in range(100)]
})

# Carga incremental
resultado = incremental_load_con_validacion(
    logs,
    engine,
    "logs_aplicacion",
    "timestamp",
    "checkpoint_logs.txt",
    columnas_requeridas=["id_log", "timestamp", "nivel"]
)

print(f"Cargados: {resultado['cargados']}")
print(f"Inválidos: {resultado['invalidos']}")
```

### Ejemplo 3: Base de Datos de Clientes (Upsert)

```python
from src.cargador_upsert import upsert_con_metricas

# Clientes (nuevos + actualizados)
clientes = pd.DataFrame({
    "id_cliente": [1, 2, 3, 4],
    "nombre": ["Ana García", "Luis Pérez Updated", "María López", "Carlos Nuevo"],
    "email": ["ana@email.com", "luis_nuevo@email.com", "maria@email.com", "carlos@email.com"],
    "ciudad": ["CDMX", "Guadalajara", "Monterrey", "Puebla"]
})

# Upsert
resultado = upsert_con_metricas(clientes, engine, "clientes", "id_cliente")

print(f"Inserts: {resultado['inserts']} (clientes nuevos)")
print(f"Updates: {resultado['updates']} (clientes actualizados)")
```

## 🧪 Cobertura de Tests

El proyecto tiene >80% de cobertura con 70+ tests:

- `test_cargador_full.py`: 15 tests
- `test_cargador_incremental.py`: 15 tests
- `test_cargador_upsert.py`: 12 tests
- `test_batch_processor.py`: 9 tests
- `test_metrics_collector.py`: 9 tests
- `test_pipeline_manager.py`: 14 tests

```bash
# Ver reporte de cobertura
pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html
```

## 🛠️ Troubleshooting

### Problema: Error "table already exists"
**Solución**: Usa `if_exists="append"` o `if_exists="replace"` en `to_sql()`

### Problema: Checkpoint no se actualiza
**Solución**: Verifica que el checkpoint_file tenga permisos de escritura

### Problema: Memoria insuficiente con datasets grandes
**Solución**: Usa `procesar_en_lotes()` con batch_size más pequeño (ej: 1000)

## 📚 Recursos Adicionales

- [Teoría: 01-TEORIA.md](../01-TEORIA.md)
- [Ejemplos: 02-EJEMPLOS.md](../02-EJEMPLOS.md)
- [Ejercicios: 03-EJERCICIOS.md](../03-EJERCICIOS.md)

## 🎯 Próximos Pasos

1. Completar todos los ejercicios en `03-EJERCICIOS.md`
2. Experimentar con diferentes estrategias
3. Medir rendimiento con datasets de diferentes tamaños
4. Implementar logging personalizado
5. Agregar retry logic para mayor robustez

---

**¡Éxito con tu aprendizaje de Data Engineering!** 🚀
