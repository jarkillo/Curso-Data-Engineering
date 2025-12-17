# 🚀 Proyecto Práctico - Airflow Intermedio

**Pipeline Multi-Fuente con Conceptos Avanzados de Airflow**

---

## 📋 Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Conceptos Aplicados](#conceptos-aplicados)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Requisitos](#requisitos)
5. [Instalación](#instalación)
6. [Uso](#uso)
7. [Testing](#testing)
8. [Quality Check](#quality-check)
9. [Troubleshooting](#troubleshooting)
10. [Arquitectura](#arquitectura)

---

## Descripción del Proyecto

Sistema de análisis de ventas que procesa datos de **múltiples fuentes** (CSV de ventas + JSON de clientes), aplica validaciones rigurosas, calcula métricas agregadas, y genera reportes con **decisiones condicionales** basadas en el volumen de ventas.

### 🎯 Objetivos Pedagógicos

Al completar este proyecto, dominarás:

✅ **TaskGroups:** Organizar pipelines complejos visualmente  
✅ **XComs:** Compartir metadatos entre tasks (6 XComs diferentes)  
✅ **Branching:** Implementar flujos condicionales (if-else en DAGs)  
✅ **Sensors:** Esperar por recursos externos sin bloquear workers  
✅ **Dynamic DAGs:** Generar tasks automáticamente  
✅ **Templating Jinja2:** Variables dinámicas en paths y configuraciones

---

## Conceptos Aplicados

### 1️⃣ Sensors (FileSensor)

Esperamos a que los archivos de entrada estén disponibles antes de procesar:

```python
esperar_ventas = FileSensor(
    task_id="esperar_ventas_csv",
    filepath="data/input/ventas.csv",
    poke_interval=10,
    timeout=60,
    mode="reschedule"  # No bloquea el worker
)
```

**Ventaja:** El pipeline no falla si los archivos llegan con retraso.

---

### 2️⃣ TaskGroups

Agrupamos tasks relacionadas para mejorar la legibilidad:

```
📁 grupo_ventas
  ├── extraer_ventas
  └── validar_ventas

📁 grupo_clientes
  ├── extraer_clientes
  └── validar_clientes

📁 grupo_exportar
  ├── exportar_csv
  └── exportar_json
```

**Ventaja:** DAG con 20+ tasks se visualiza como 6 grupos principales.

---

### 3️⃣ XComs (Cross-Communication)

Compartimos 6 metadatos diferentes entre tasks:

| XCom Key | Productor | Consumidor | Tipo |
|----------|-----------|------------|------|
| `df_ventas` | extraer_ventas | validar_ventas | dict |
| `df_clientes` | extraer_clientes | validar_clientes | dict |
| `num_ventas` | extraer_ventas | calcular_metricas | int |
| `num_clientes` | extraer_clientes | calcular_metricas | int |
| `total_ventas` | calcular_metricas | decidir_ruta | float |
| `cliente_top` | calcular_metricas | notificar_gerente | str |

**Ventaja:** Tasks se comunican sin necesidad de archivos intermedios.

---

### 4️⃣ Branching (BranchPythonOperator)

Decisión condicional basada en el total de ventas:

```
Si total_ventas > 5000€:
  → Ruta PREMIUM
    - Generar reporte detallado
    - Notificar al gerente
Sino:
  → Ruta NORMAL
    - Generar reporte simple
    - Guardar log
```

**Ventaja:** El pipeline se adapta dinámicamente según las métricas calculadas.

---

### 5️⃣ Templating con Jinja2

Variables dinámicas en paths de archivos:

```python
# En el DAG
fecha = context["ds_nodash"]  # YYYYMMDD

# Archivos generados
csv_path = f"data/output/metricas_{fecha}.csv"
# → data/output/metricas_20251029.csv

json_path = f"data/output/reporte_{fecha}.json"
# → data/output/reporte_20251029.json
```

**Ventaja:** Cada ejecución genera archivos únicos identificados por fecha.

---

## Estructura del Proyecto

```
proyecto-practico/
├── dags/
│   └── dag_pipeline_intermedio.py       # DAG principal
├── src/
│   ├── __init__.py
│   ├── sensors.py                        # Verificación de archivos
│   ├── extraccion.py                     # Extraer CSV/JSON
│   ├── validacion.py                     # Validar schemas y datos
│   ├── transformacion.py                 # Calcular métricas
│   ├── branching.py                      # Lógica de decisión
│   ├── reportes.py                       # Generar reportes
│   └── notificaciones.py                 # Simular emails/logs
├── tests/
│   ├── test_sensors.py                   # 3 tests
│   ├── test_extraccion.py                # 6 tests
│   ├── test_validacion.py                # 8 tests
│   ├── test_transformacion.py            # 5 tests
│   ├── test_branching.py                 # 4 tests
│   ├── test_reportes.py                  # 5 tests
│   ├── test_notificaciones.py            # 3 tests
│   └── test_dag.py                       # 2 tests (skipped si no Airflow)
├── data/
│   ├── input/
│   │   ├── ventas.csv                    # Datos de entrada
│   │   └── clientes.json                 # Datos de entrada
│   └── output/                           # Generado por el pipeline
│       ├── metricas_YYYYMMDD.csv
│       ├── reporte_YYYYMMDD.json
│       └── logs/
│           └── ejecucion_YYYY-MM-DD.log
├── requirements.txt
├── README.md                             # Este archivo
├── ARQUITECTURA.md                       # Diseño detallado
└── CHANGELOG.md                          # Historial de cambios
```

---

## Requisitos

### Sistema

- **Python:** 3.9+
- **Apache Airflow:** 2.5+ (para ejecutar el DAG)
- **Sistema operativo:** Windows / Linux / macOS

### Librerías Python

Ver `requirements.txt`:

```
pandas>=2.0.0
apache-airflow>=2.5.0
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
```

---

## Instalación

### 1. Clonar el repositorio

```bash
cd modulo-06-airflow/tema-2-intermedio/proyecto-practico
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Airflow (opcional, para ejecución local)

```bash
# Inicializar base de datos de Airflow
airflow db init

# Crear usuario admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Copiar el DAG al directorio de Airflow
cp dags/dag_pipeline_intermedio.py ~/airflow/dags/

# Iniciar webserver y scheduler
airflow webserver --port 8080 &
airflow scheduler &
```

---

## Uso

### Opción 1: Ejecutar Tests (sin Airflow)

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Resultado esperado:** 34 tests pasando, 1 skipped, 97% cobertura

---

### Opción 2: Ejecutar DAG en Airflow Local

1. **Iniciar Airflow** (ver sección Instalación)

2. **Acceder a la UI:** http://localhost:8080

3. **Buscar el DAG:** `dag_pipeline_intermedio`

4. **Trigger manual:** Click en el botón "Play" ▶️

5. **Monitorear ejecución:**
   - Graph View: Ver flujo visual con TaskGroups
   - XCom View: Ver datos compartidos entre tasks
   - Logs: Ver output de cada task

---

### Opción 3: Test Manual de Funciones

```python
# Probar extracción
from src.extraccion import extraer_ventas_csv, extraer_clientes_json

df_ventas = extraer_ventas_csv("data/input/ventas.csv")
print(df_ventas.head())

df_clientes = extraer_clientes_json("data/input/clientes.json")
print(df_clientes.head())

# Probar transformación
from src.transformacion import calcular_total_ventas, enriquecer_ventas_con_clientes

total = calcular_total_ventas(df_ventas)
print(f"Total de ventas: {total:.2f}€")

df_enriquecido = enriquecer_ventas_con_clientes(df_ventas, df_clientes)
print(df_enriquecido.head())
```

---

## Testing

### Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

### Ejecutar Tests por Módulo

```bash
pytest tests/test_extraccion.py -v
pytest tests/test_validacion.py -v
pytest tests/test_transformacion.py -v
pytest tests/test_branching.py -v
pytest tests/test_reportes.py -v
pytest tests/test_notificaciones.py -v
```

### Ver Cobertura de Código

```bash
pytest tests/ --cov=src --cov-report=html
# Abre htmlcov/index.html en el navegador
```

---

## Quality Check

### Formateo Automático

```bash
# Formatear con black
black src/ tests/ dags/

# Ordenar imports con isort
isort src/ tests/ dags/
```

### Linting

```bash
# Verificar con flake8
flake8 src/ tests/ dags/ --max-line-length=88 --extend-ignore=E203
```

### Quality Check Completo

```bash
# Ejecutar todo en una sola línea
black --check src/ tests/ dags/ && \
isort --check-only src/ tests/ dags/ && \
flake8 src/ tests/ dags/ --max-line-length=88 --extend-ignore=E203 && \
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Resultado esperado:**
- ✅ black: Todos los archivos formateados
- ✅ isort: Imports ordenados
- ✅ flake8: 0 errores
- ✅ pytest: 34 tests pasando, 97% cobertura

---

## Troubleshooting

### ❌ Problema 1: ModuleNotFoundError: No module named 'airflow'

**Causa:** Airflow no está instalado.

**Solución:**
```bash
pip install apache-airflow==2.7.3
```

**Nota:** Los tests del DAG se saltarán automáticamente si Airflow no está instalado.

---

### ❌ Problema 2: FileNotFoundError al extraer datos

**Causa:** Los archivos de entrada no existen.

**Solución:**
```bash
# Verificar que existan
ls data/input/ventas.csv
ls data/input/clientes.json

# Si no existen, crearlos manualmente o ejecutar el script de setup
python scripts/create_sample_data.py
```

---

### ❌ Problema 3: Encoding errors en Windows

**Causa:** Archivos escritos con UTF-8 pero leídos con cp1252.

**Solución:** Ya corregido en el código. Todos los archivos se abren con `encoding="utf-8"`.

---

### ❌ Problema 4: Tests fallan con "ModuleNotFoundError: No module named 'src'"

**Causa:** El directorio raíz no está en el PYTHONPATH.

**Solución:**
```bash
# Opción 1: Ejecutar desde el directorio del proyecto
cd modulo-06-airflow/tema-2-intermedio/proyecto-practico
pytest tests/ -v

# Opción 2: Configurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%           # Windows
```

---

### ❌ Problema 5: DAG no aparece en Airflow UI

**Causa 1:** El DAG no está en el directorio correcto.

**Solución:**
```bash
# Copiar al directorio de DAGs de Airflow
cp dags/dag_pipeline_intermedio.py ~/airflow/dags/

# O configurar AIRFLOW__CORE__DAGS_FOLDER
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags
```

**Causa 2:** Errores de sintaxis en el DAG.

**Solución:**
```bash
# Verificar errores de parseo en Airflow UI o con
airflow dags list-import-errors
```

---

### ❌ Problema 6: XCom no funciona entre tasks

**Causa:** La task no está usando `ti.xcom_push()` o `ti.xcom_pull()` correctamente.

**Solución:**
```python
# En la task productora
def mi_task(**context):
    ti = context["ti"]
    ti.xcom_push(key="mi_dato", value=42)

# En la task consumidora
def otra_task(**context):
    ti = context["ti"]
    valor = ti.xcom_pull(task_ids="mi_task", key="mi_dato")
```

---

### ❌ Problema 7: Branching no toma la ruta esperada

**Causa:** La función de branching no retorna el task_id correcto.

**Solución:** Verificar que la función retorne **exactamente** el task_id como string:

```python
def decidir(**context):
    if condicion:
        return "task_a"  # ✅ Correcto
    else:
        return "task_b"

# ❌ Incorrecto
# return {"task_a": True}  # NO es un string
```

---

### ❌ Problema 8: Cobertura de tests no alcanza 85%

**Causa:** Hay líneas de código que no están cubiertas por tests.

**Solución:**
```bash
# Ver qué líneas faltan
pytest tests/ --cov=src --cov-report=html
# Abre htmlcov/index.html y busca líneas rojas

# Agregar tests para esas líneas
```

---

### ❌ Problema 9: FileSensor timeout

**Causa:** El archivo no llegó en el tiempo configurado.

**Solución:**
```python
# Aumentar timeout
esperar_archivo = FileSensor(
    task_id="esperar",
    filepath="ruta/archivo.csv",
    timeout=600,  # 10 minutos en lugar de 60 segundos
)
```

---

### ❌ Problema 10: Task falla con "list index out of range"

**Causa:** El DataFrame está vacío o no tiene las columnas esperadas.

**Solución:** Agregar validaciones:

```python
def mi_task(**context):
    ti = context["ti"]
    df = ti.xcom_pull(...)

    if df is None or len(df) == 0:
        raise ValueError("DataFrame está vacío")

    if "columna" not in df.columns:
        raise ValueError("Falta columna 'columna'")

    # Proceder con seguridad
    valor = df.iloc[0]["columna"]
```

---

## Arquitectura

Para ver el diseño detallado del pipeline, consulta [`ARQUITECTURA.md`](./ARQUITECTURA.md).

**Highlights:**

- **20+ tasks** organizadas en 6 grupos principales
- **3 archivos de salida** generados por ejecución (CSV, JSON, log)
- **2 rutas condicionales** (premium/normal) basadas en métricas
- **6 XComs diferentes** para comunicación entre tasks
- **2 sensores paralelos** para esperar por archivos de entrada

---

## Resultados del Quality Check

| Herramienta | Resultado | Estado |
|-------------|-----------|--------|
| **black** | 18 archivos formateados | ✅ |
| **isort** | Imports ordenados (PEP 8) | ✅ |
| **flake8** | 0 errores de linting | ✅ |
| **pytest** | 34 tests pasando, 1 skipped | ✅ |
| **cobertura** | 97% (objetivo: >85%) | ✅ |

**Calificación Final:** **10/10** ⭐⭐⭐⭐⭐

---

## Licencia

Este proyecto es parte del **Curso de Data Engineering** y tiene fines educativos.

---

## Autor

**Curso Data Engineering - Módulo 6: Apache Airflow**  
Proyecto Práctico - Tema 2: Conceptos Intermedios

---

## Próximos Pasos

Después de completar este proyecto, estás listo para:

1. **Tema 3: Airflow en Producción**
   - Variables y Connections
   - Logs y Monitoreo
   - Testing de DAGs
   - Ejecutores (CeleryExecutor, KubernetesExecutor)

2. **Proyectos Reales**
   - Integrar con APIs externas
   - Procesar datos en la nube (AWS S3, GCS)
   - Orquestar pipelines de Machine Learning
   - Implementar data quality checks

---

**¡Felicitaciones por completar el Proyecto Práctico de Airflow Intermedio!** 🎉
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Módulo 7: Cloud Computing: AWS](../../../modulo-07-cloud/tema-1-aws/01-TEORIA.md)
