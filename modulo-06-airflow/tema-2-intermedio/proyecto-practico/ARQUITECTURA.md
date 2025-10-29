# 🏗️ Arquitectura del Proyecto Práctico - Tema 2

**Pipeline Multi-Fuente con Conceptos Intermedios de Airflow**

---

## 📋 Índice

1. [Visión General](#visión-general)
2. [Objetivos de Aprendizaje](#objetivos-de-aprendizaje)
3. [Estructura del Pipeline](#estructura-del-pipeline)
4. [Componentes del Sistema](#componentes-del-sistema)
5. [Flujo de Datos](#flujo-de-datos)
6. [Decisiones Técnicas](#decisiones-técnicas)
7. [Estructura de Archivos](#estructura-de-archivos)

---

## Visión General

### 🎯 Descripción del Proyecto

Sistema de análisis de ventas que procesa datos de **múltiples fuentes** (CSV de ventas + JSON de clientes), aplica validaciones, detecta patrones, y genera reportes con decisiones condicionales basadas en el volumen de ventas.

### 🔑 Conceptos Aplicados

| Concepto | Aplicación en el Proyecto |
|----------|---------------------------|
| **TaskGroups** | Agrupar extracción, transformación, validación y carga |
| **XComs** | Compartir métricas (total ventas, clientes procesados) entre tasks |
| **Branching** | Decidir ruta de procesamiento según volumen de ventas |
| **Sensors** | Esperar archivos de entrada antes de procesar |
| **Dynamic DAGs** | Generar tasks de validación dinámicamente |
| **Templating** | Usar fechas en nombres de archivos de salida |

---

## Objetivos de Aprendizaje

Al completar este proyecto, serás capaz de:

✅ Organizar pipelines complejos con **TaskGroups** anidados  
✅ Usar **XComs** para pasar metadatos entre tasks  
✅ Implementar **Branching** con múltiples rutas condicionales  
✅ Configurar **Sensors** para esperar por recursos externos  
✅ Generar **tasks dinámicamente** basadas en configuraciones  
✅ Aplicar **templating Jinja2** en paths y configuraciones

---

## Estructura del Pipeline

### 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────────┐
│                            INICIO                                    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   SENSORES PARALELOS   │
                    │  (esperar_ventas_csv)  │
                    │  (esperar_clientes_json)│
                    └───────────┬────────────┘
                                │
            ┌───────────────────┴──────────────────┐
            │                                       │
    ┌───────▼────────┐                    ┌────────▼───────┐
    │  TaskGroup:     │                    │  TaskGroup:     │
    │  VENTAS         │                    │  CLIENTES       │
    │  - extraer      │                    │  - extraer      │
    │  - validar      │                    │  - validar      │
    │  - transformar  │                    │  - transformar  │
    └───────┬─────────┘                    └────────┬────────┘
            │                                       │
            └───────────────┬───────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  COMBINAR DATOS │
                    │  (merge ventas  │
                    │   + clientes)   │
                    └───────┬─────────┘
                            │
                    ┌───────▼────────┐
                    │  CALCULAR       │
                    │  MÉTRICAS       │
                    └───────┬─────────┘
                            │
                    ┌───────▼────────┐
                    │  BRANCHING:     │
                    │  ¿Volumen alto? │
                    └───┬────────┬────┘
                        │        │
            ┌───────────┘        └──────────┐
            │                                │
    ┌───────▼─────────┐          ┌──────────▼────────┐
    │ RUTA PREMIUM     │          │ RUTA NORMAL       │
    │ (ventas > 5000€) │          │ (ventas ≤ 5000€)  │
    │ - reporte_detallado│        │ - reporte_simple  │
    │ - notificar_gerente│        │ - guardar_log     │
    └───────┬──────────┘          └──────────┬────────┘
            │                                │
            └───────────┬────────────────────┘
                        │
                ┌───────▼────────┐
                │  TaskGroup:     │
                │  EXPORTAR       │
                │  - csv          │
                │  - json         │
                │  - comprimir    │
                └───────┬─────────┘
                        │
                ┌───────▼────────┐
                │  FIN            │
                └─────────────────┘
```

---

## Componentes del Sistema

### 1️⃣ Módulo: Sensors

**Archivo:** `src/sensors.py`

```python
Funciones:
- verificar_archivo_existe(ruta: str) -> bool
  """Verifica si un archivo existe (para testing de FileSensor)"""
```

**Implementación en DAG:**
```python
esperar_ventas = FileSensor(
    task_id="esperar_ventas_csv",
    filepath="data/input/ventas.csv",
    poke_interval=10,
    timeout=60,
    mode="reschedule"
)
```

---

### 2️⃣ Módulo: Extracción

**Archivo:** `src/extraccion.py`

```python
Funciones:
- extraer_ventas_csv(ruta_csv: str) -> pd.DataFrame
  """Extrae datos de ventas desde CSV"""

- extraer_clientes_json(ruta_json: str) -> pd.DataFrame
  """Extrae datos de clientes desde JSON"""

- contar_registros_extraidos(df: pd.DataFrame) -> int
  """Cuenta registros (para XCom)"""
```

**XCom producido:**
- Key: `num_ventas` → int (cantidad de registros de ventas)
- Key: `num_clientes` → int (cantidad de clientes)

---

### 3️⃣ Módulo: Validación

**Archivo:** `src/validacion.py`

```python
Funciones:
- validar_schema_ventas(df: pd.DataFrame) -> None
  """Valida que el DataFrame tenga las columnas requeridas"""

- validar_datos_ventas(df: pd.DataFrame) -> None
  """Valida tipos de datos, valores nulos, rangos"""

- validar_schema_clientes(df: pd.DataFrame) -> None
  """Valida schema de clientes"""

- validar_datos_clientes(df: pd.DataFrame) -> None
  """Valida datos de clientes"""
```

**Validaciones dinámicas:**
- Se generan tasks de validación dinámicamente para cada columna crítica

---

### 4️⃣ Módulo: Transformación

**Archivo:** `src/transformacion.py`

```python
Funciones:
- calcular_total_ventas(df: pd.DataFrame) -> float
  """Calcula el total de ventas (columna cantidad * precio)"""

- enriquecer_ventas_con_clientes(df_ventas: pd.DataFrame,
                                  df_clientes: pd.DataFrame) -> pd.DataFrame
  """Combina ventas con información de clientes (merge)"""

- calcular_metricas_por_cliente(df: pd.DataFrame) -> pd.DataFrame
  """Calcula métricas agregadas por cliente"""
```

**XCom producido:**
- Key: `total_ventas` → float
- Key: `cliente_top` → str (ID del cliente con más ventas)

---

### 5️⃣ Módulo: Branching

**Archivo:** `src/branching.py`

```python
Funciones:
- decidir_ruta_procesamiento(**context) -> str
  """
  Decide si seguir ruta premium o normal basado en total_ventas

  Lógica:
  - Si total_ventas > 5000€ → "ruta_premium"
  - Si total_ventas ≤ 5000€ → "ruta_normal"
  """
```

**Rutas:**
1. **Ruta Premium:** Genera reporte detallado + notifica gerente
2. **Ruta Normal:** Genera reporte simple + guarda log

---

### 6️⃣ Módulo: Reportes

**Archivo:** `src/reportes.py`

```python
Funciones:
- generar_reporte_detallado(df: pd.DataFrame, total: float) -> dict
  """Genera reporte JSON con métricas detalladas"""

- generar_reporte_simple(df: pd.DataFrame, total: float) -> dict
  """Genera reporte JSON con métricas básicas"""

- exportar_reporte_csv(df: pd.DataFrame, ruta: str) -> None
  """Exporta DataFrame a CSV"""

- exportar_reporte_json(reporte: dict, ruta: str) -> None
  """Exporta reporte a JSON"""
```

**Templating aplicado:**
```python
ruta_csv = "data/output/reporte_{{ ds_nodash }}.csv"
ruta_json = "data/output/metricas_{{ ds_nodash }}.json"
```

---

### 7️⃣ Módulo: Notificaciones

**Archivo:** `src/notificaciones.py`

```python
Funciones:
- simular_notificacion_gerente(total: float, cliente_top: str) -> None
  """Simula envío de email al gerente con métricas clave"""

- guardar_log_ejecucion(mensaje: str, ruta: str) -> None
  """Guarda log de ejecución en archivo"""
```

---

### 8️⃣ Módulo: Utilidades

**Archivo:** `src/utils.py`

```python
Funciones:
- comprimir_archivos(directorio: str, nombre_zip: str) -> str
  """Comprime archivos de salida en ZIP"""

- limpiar_archivos_temporales(directorio: str) -> None
  """Elimina archivos temporales"""

- obtener_ruta_con_fecha(base: str, extension: str, fecha: str) -> str
  """Genera ruta con fecha templated"""
```

---

## Flujo de Datos

### 🔄 Paso a Paso

#### Fase 1: Espera y Extracción (Paralelo)

```
1. FileSensor espera ventas.csv (timeout 60s)
2. FileSensor espera clientes.json (timeout 60s)
3. Una vez disponibles → extraer en paralelo
```

**XComs generados:**
- `num_ventas`: 5 (ejemplo)
- `num_clientes`: 3 (ejemplo)

---

#### Fase 2: Validación (TaskGroups)

**TaskGroup: ventas**
```
- validar_schema_ventas
- validar_datos_ventas (dinámico: producto, cantidad, precio, cliente_id)
```

**TaskGroup: clientes**
```
- validar_schema_clientes
- validar_datos_clientes (dinámico: cliente_id, nombre, nivel)
```

---

#### Fase 3: Transformación

```
1. Combinar ventas + clientes (merge on cliente_id)
2. Calcular métricas:
   - total_ventas = sum(cantidad * precio)
   - cliente_top = cliente con más ventas
```

**XComs generados:**
- `total_ventas`: 4512.50 (ejemplo)
- `cliente_top`: "C001" (ejemplo)

---

#### Fase 4: Branching

```python
if total_ventas > 5000:
    return ["generar_reporte_detallado", "notificar_gerente"]
else:
    return ["generar_reporte_simple", "guardar_log"]
```

**Ejemplo:**
- Si `total_ventas = 4512.50` → Ruta Normal

---

#### Fase 5: Generación de Reportes

**Ruta Normal (ejemplo):**
```
1. generar_reporte_simple
   → data/output/reporte_20251029.csv
   → data/output/metricas_20251029.json

2. guardar_log
   → data/output/logs/ejecucion_20251029.log
```

---

#### Fase 6: Exportación (TaskGroup)

```
TaskGroup: exportar
  - exportar_csv (usa templating {{ ds_nodash }})
  - exportar_json (usa templating {{ ds_nodash }})
  - comprimir_archivos (genera reporte_20251029.zip)
```

---

## Decisiones Técnicas

### 🎨 TaskGroups

**Agrupaciones definidas:**

1. **grupo_ventas:**
   - extraer_ventas
   - validar_ventas
   - transformar_ventas

2. **grupo_clientes:**
   - extraer_clientes
   - validar_clientes
   - transformar_clientes

3. **grupo_exportar:**
   - exportar_csv
   - exportar_json
   - comprimir_archivos

**Ventaja:** DAG con 20+ tasks reducido visualmente a 6-7 nodos principales.

---

### 🔗 XComs

**Keys definidas:**

| Key | Tipo | Productor | Consumidor |
|-----|------|-----------|------------|
| `num_ventas` | int | extraer_ventas | validar_ventas |
| `num_clientes` | int | extraer_clientes | validar_clientes |
| `total_ventas` | float | calcular_metricas | decidir_ruta |
| `cliente_top` | str | calcular_metricas | generar_reporte |
| `ruta_reporte_csv` | str | exportar_csv | comprimir_archivos |
| `ruta_reporte_json` | str | exportar_json | comprimir_archivos |

**Tamaños:** Todos <1 KB (metadatos pequeños, no DataFrames completos)

---

### 🔀 Branching

**Lógica de decisión:**

```python
def decidir_ruta_procesamiento(**context):
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")

    umbral = 5000.0

    if total > umbral:
        print(f"[BRANCH] Total {total}€ > {umbral}€ → RUTA PREMIUM")
        return ["generar_reporte_detallado", "notificar_gerente"]
    else:
        print(f"[BRANCH] Total {total}€ ≤ {umbral}€ → RUTA NORMAL")
        return ["generar_reporte_simple", "guardar_log"]
```

**Trigger Rule en convergencia:**
```python
task_exportar = DummyOperator(
    task_id="inicio_exportar",
    trigger_rule="none_failed_min_one_success"
)
```

---

### 📡 Sensors

**Configuración:**

```python
FileSensor(
    task_id="esperar_ventas_csv",
    filepath="modulo-06-airflow/tema-2-intermedio/proyecto-practico/data/input/ventas.csv",
    poke_interval=10,  # Cada 10 segundos
    timeout=60,        # Máximo 1 minuto
    mode="reschedule"  # No bloquear worker
)
```

**Razón:** En un entorno real, los archivos pueden llegar con retraso. El sensor espera sin consumir recursos.

---

### 🔄 Dynamic Task Generation

**Validaciones dinámicas:**

```python
# Validar dinámicamente cada columna
columnas_criticas = ["producto", "cantidad", "precio", "cliente_id"]

for columna in columnas_criticas:
    task = PythonOperator(
        task_id=f"validar_columna_{columna}",
        python_callable=validar_columna,
        op_kwargs={"df": df, "columna": columna}
    )
    # ... agregar al flujo
```

**Ventaja:** Fácil agregar nuevas columnas sin duplicar código.

---

### 🧩 Templating Jinja2

**Aplicaciones:**

1. **Rutas de archivos:**
```python
ruta_csv = "data/output/reporte_{{ ds_nodash }}.csv"
# → data/output/reporte_20251029.csv
```

2. **Logs con fecha:**
```python
log_file = "data/output/logs/ejecucion_{{ ds }}.log"
# → data/output/logs/ejecucion_2025-10-29.log
```

3. **Nombres de archivos ZIP:**
```python
zip_name = "reporte_{{ ds_nodash }}.zip"
# → reporte_20251029.zip
```

---

## Estructura de Archivos

```
proyecto-practico/
├── dags/
│   └── dag_pipeline_intermedio.py   # DAG principal
├── src/
│   ├── __init__.py
│   ├── sensors.py                    # Lógica de sensors
│   ├── extraccion.py                 # Extraer CSV/JSON
│   ├── validacion.py                 # Validar schemas y datos
│   ├── transformacion.py             # Calcular métricas
│   ├── branching.py                  # Lógica de decisión
│   ├── reportes.py                   # Generar reportes
│   ├── notificaciones.py             # Simular emails/logs
│   └── utils.py                      # Utilidades (comprimir, etc.)
├── tests/
│   ├── __init__.py
│   ├── test_sensors.py               # 3-4 tests
│   ├── test_extraccion.py            # 4-5 tests
│   ├── test_validacion.py            # 6-8 tests
│   ├── test_transformacion.py        # 4-5 tests
│   ├── test_branching.py             # 3-4 tests
│   ├── test_reportes.py              # 4-5 tests
│   ├── test_notificaciones.py        # 2-3 tests
│   └── test_dag.py                   # 2-3 tests (DAG parsing)
├── data/
│   ├── input/
│   │   ├── ventas.csv
│   │   └── clientes.json
│   └── output/                       # Generados por el pipeline
│       ├── reporte_YYYYMMDD.csv
│       ├── metricas_YYYYMMDD.json
│       ├── reporte_YYYYMMDD.zip
│       └── logs/
│           └── ejecucion_YYYY-MM-DD.log
├── requirements.txt
├── README.md
├── ARQUITECTURA.md                   # Este archivo
└── CHANGELOG.md                      # A crear
```

---

## Métricas de Calidad

### ✅ Tests

**Objetivo:** 35-40 tests distribuidos en:
- Sensors: 3 tests
- Extracción: 5 tests (2 por fuente + 1 error)
- Validación: 8 tests (schema + datos + errores)
- Transformación: 5 tests (cálculos + merge)
- Branching: 4 tests (2 rutas + edge cases)
- Reportes: 5 tests (CSV + JSON + formatos)
- Notificaciones: 3 tests (email + log)
- DAG: 2 tests (parsing + estructura)

**Cobertura objetivo:** >85%

---

### 🧹 Linters

**Herramientas:**
- `black`: Formateo automático
- `isort`: Ordenar imports
- `flake8`: 0 errores permitidos
- `mypy`: Type hints correctos

---

### 🚀 Ejecución en Airflow

**Verificación:**
1. DAG parsea sin errores
2. Todas las tasks aparecen en UI
3. TaskGroups se visualizan correctamente colapsados
4. Ejecución manual completa exitosamente
5. XComs se guardan y leen correctamente
6. Branching toma decisiones correctas
7. Archivos de salida se generan con nombres correctos

---

## Próximos Pasos

1. ✅ Arquitectura definida
2. ⏳ Escribir tests (35-40 tests TDD)
3. ⏳ Implementar funciones en `src/`
4. ⏳ Crear DAG principal
5. ⏳ Quality check (black, flake8, pytest)
6. ⏳ Ejecutar en Airflow local
7. ⏳ Documentar troubleshooting en README

---

**🎯 Esta arquitectura garantiza:**
- ✅ Aplicación práctica de todos los conceptos de Tema 2
- ✅ Código modular y testeable
- ✅ Pipeline realista y escalable
- ✅ Fácil de entender y mantener
- ✅ Preparado para producción

---

**Fecha de diseño:** 2025-10-29  
**Versión:** 1.0
