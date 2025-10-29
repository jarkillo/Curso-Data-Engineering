# 📋 Planificación Detallada - JAR-192 Tema 2

**Issue:** Módulo 6: Apache Airflow y Orquestación - Tema 2: Airflow Intermedio
**Estado:** Todo → In Progress
**Prioridad:** High (2)
**Fecha de inicio:** 2025-10-27
**Dependencias:** ✅ Tema 1 completado (2025-10-25)

---

## 📊 Resumen Ejecutivo

### Contexto
- **Tema 1:** ✅ Completado el 2025-10-25
  - Calificación pedagógica: 9.2/10
  - Tests: 33/33 (100% pasando)
  - Cobertura: 94%
- **Tema 2:** ⏳ Por iniciar (este documento)
- **Tema 3:** 🔜 Pendiente

### Estimaciones Tema 2

- **Duración total:** 6-7 días (48-56 horas)
- **Tests estimados:** 35-40 tests
- **Cobertura objetivo:** >85%
- **Contenido:** ~5,000 palabras teoría, 5 ejemplos, 15 ejercicios
- **Calificación pedagógica objetivo:** >9.0/10

---

## 🎯 Objetivos del Tema 2

### Conceptos a Cubrir

1. **TaskGroups** (vs SubDAGs deprecados)
   - Organización visual de DAGs complejos
   - Agrupación lógica de tasks relacionadas
   - Sintaxis y mejores prácticas

2. **XComs (Cross-Communication)**
   - Compartir datos entre tasks
   - `xcom_push` y `xcom_pull`
   - Limitaciones y alternativas

3. **Branching**
   - BranchPythonOperator
   - Condicionales en DAGs
   - Trigger rules

4. **Sensors**
   - FileSensor, TimeSensor, HttpSensor
   - ExternalTaskSensor
   - Parámetros: poke_interval, timeout, mode

5. **Dynamic DAG Generation**
   - Generar tasks en bucles
   - Casos de uso y límites

6. **Templating con Jinja2**
   - Variables dinámicas ({{ ds }}, {{ macros }})
   - Personalización de rutas

---

## 📁 Estructura de Archivos

```
modulo-06-airflow/tema-2-intermedio/
├── 01-TEORIA.md                    (~5,000 palabras)
├── 02-EJEMPLOS.md                  (5 ejemplos ejecutables)
├── 03-EJERCICIOS.md                (15 ejercicios con soluciones)
└── proyecto-practico/
    ├── README.md                   (~1,200 palabras)
    ├── requirements.txt            (dependencias)
    ├── CHANGELOG.md                (historial de cambios)
    ├── data/
    │   ├── input/
    │   │   ├── ventas.csv          (datos de prueba)
    │   │   └── clientes.json       (datos de prueba)
    │   └── output/                 (resultados)
    ├── dags/
    │   └── dag_pipeline_intermedio.py  (~250 líneas)
    ├── src/
    │   ├── __init__.py
    │   ├── task_groups.py          (definición de TaskGroups)
    │   ├── xcoms.py                (manejo de XComs)
    │   ├── branching.py            (lógica condicional)
    │   ├── sensors.py              (sensores personalizados)
    │   ├── extraccion.py           (funciones de extracción)
    │   ├── transformacion.py       (funciones de transformación)
    │   └── carga.py                (funciones de carga)
    └── tests/
        ├── __init__.py
        ├── conftest.py             (fixtures de Airflow)
        ├── test_task_groups.py     (8-10 tests)
        ├── test_xcoms.py           (8-10 tests)
        ├── test_branching.py       (8-10 tests)
        ├── test_sensors.py         (5-7 tests)
        └── test_dag_intermedio.py  (8-10 tests)
```

---

## 📖 Contenido Detallado

### 01-TEORIA.md (~5,000 palabras)

**Secciones:**

1. **Introducción al Tema 2** (300 palabras)
   - Recap del Tema 1
   - Por qué necesitamos conceptos intermedios
   - Qué aprenderemos

2. **TaskGroups: Organización Visual** (800 palabras)
   - Problema: DAGs con 20+ tasks ilegibles
   - Solución: Agrupar tasks relacionadas
   - Sintaxis y ejemplos
   - Ventajas sobre SubDAGs (deprecados)
   - Casos de uso reales

3. **SubDAGs (Contexto Histórico)** (400 palabras)
   - Qué eran SubDAGs
   - Por qué se deprecaron
   - Alternativa moderna: TaskGroups
   - Cuándo encontrarlos en código legacy

4. **XComs: Comunicación entre Tasks** (1,000 palabras)
   - Problema: Tasks aisladas
   - Solución: XComs (Cross-Communication)
   - API: xcom_push, xcom_pull
   - Limitaciones: tamaño, serialización
   - Alternativas para datos grandes
   - Mejores prácticas

5. **Branching: Condicionales en DAGs** (1,000 palabras)
   - BranchPythonOperator
   - Elegir caminos según condiciones
   - Trigger rules: all_success, none_failed, etc.
   - Cuidado con skip downstream
   - Ejemplos prácticos

6. **Sensors: Esperar por Condiciones** (1,200 palabras)
   - FileSensor: Esperar archivos
   - TimeSensor: Esperar hora específica
   - ExternalTaskSensor: Dependencias entre DAGs
   - HttpSensor: APIs
   - Parámetros: poke_interval, timeout, mode
   - Mejores prácticas

7. **Dynamic DAG Generation** (600 palabras)
   - Generar tasks en bucles
   - Ejemplo: Procesar N archivos
   - Límites: No abusar (max 50-100 tasks)
   - Cuándo usarlo

8. **Templating con Jinja2** (400 palabras)
   - Variables dinámicas: {{ ds }}, {{ ti }}
   - Macros útiles
   - Personalización de paths
   - Ejemplos

9. **Mejores Prácticas del Tema 2** (300 palabras)
   - Cuándo usar TaskGroups
   - Límites de XComs
   - Branching claro y documentado
   - Sensors con timeouts razonables

### 02-EJEMPLOS.md (5 ejemplos ejecutables)

**Ejemplo 1: TaskGroup Básico** (20 min) ⭐⭐
```python
with TaskGroup("grupo_procesamiento") as grupo:
    validar = PythonOperator(...)
    transformar = PythonOperator(...)
    calcular = PythonOperator(...)
    validar >> transformar >> calcular

inicio >> grupo >> fin
```

**Ejemplo 2: XComs - Pasar Datos** (20 min) ⭐⭐
- Task 1: Calcular total ventas → xcom_push
- Task 2: Leer total → xcom_pull → generar reporte

**Ejemplo 3: BranchPythonOperator** (25 min) ⭐⭐⭐
```
inicio → validar_ventas (branch)
  ├──→ (ventas > 10000) procesar_premium
  └──→ (ventas ≤ 10000) procesar_normal
fin (trigger_rule="none_failed_min_one_success")
```

**Ejemplo 4: FileSensor** (20 min) ⭐⭐
- Sensor espera `datos.csv` (timeout 60s)
- Cuando aparece → procesar

**Ejemplo 5: Dynamic DAG** (15 min) ⭐⭐
- Generar 5 tasks en loop
- Procesar múltiples archivos

### 03-EJERCICIOS.md (15 ejercicios)

**Básicos (1-5):** ⭐
1. Crear TaskGroup con 3 tasks
2. Usar XCom para pasar un número
3. BranchPythonOperator simple
4. FileSensor con timeout 30s
5. Crear 3 tasks dinámicamente

**Intermedios (6-10):** ⭐⭐
6. TaskGroup anidado
7. XComs con diccionario completo
8. Branch con 3 caminos
9. TimeSensor (esperar hasta 9 AM)
10. Dynamic DAG con 10 tasks

**Avanzados (11-15):** ⭐⭐⭐
11. Pipeline con TaskGroups + XComs + Branch
12. ExternalTaskSensor
13. TriggerDagRunOperator con parámetros
14. Dynamic DAG que lee directorio
15. Pipeline completo integrando todos los conceptos

---

## 🔧 Proyecto Práctico: Pipeline con Múltiples Fuentes

### Descripción

**Sistema de Análisis de Ventas y Clientes**

Un pipeline que:
1. **Espera** 2 archivos: `ventas.csv` y `clientes.json` (FileSensors)
2. **Procesa** ambos en paralelo (TaskGroups)
3. **Combina** datos (JOIN con pandas)
4. **Decide** acción según métricas (Branching)
5. **Comunica** resultados entre tasks (XComs)
6. **Genera** reportes finales

### Flujo del DAG

```
inicio (DummyOperator)
  ↓
[esperar_ventas_csv, esperar_clientes_json] (FileSensors, paralelo)
  ↓
[grupo_procesar_ventas, grupo_procesar_clientes] (TaskGroups, paralelo)
  │
  ├─ grupo_procesar_ventas:
  │    ├─ validar_ventas_csv
  │    ├─ transformar_ventas
  │    └─ calcular_metricas_ventas
  │
  └─ grupo_procesar_clientes:
       ├─ validar_clientes_json
       ├─ transformar_clientes
       └─ calcular_metricas_clientes
  ↓
combinar_datos (JOIN ventas + clientes)
  ↓
calcular_metricas_globales (XCom push: total_ventas, num_clientes, promedio)
  ↓
decidir_accion (BranchPythonOperator)
  ├──→ (total > 50000) enviar_alerta_premium
  └──→ (total ≤ 50000) guardar_log_normal
  ↓
generar_reporte_final (trigger_rule="none_failed_min_one_success")
  ↓
fin (DummyOperator)
```

### Archivos de Entrada

**ventas.csv**
```csv
venta_id,producto,cantidad,precio_unitario,cliente_id,fecha
1,Laptop,2,1200.00,101,2025-10-27
2,Mouse,5,25.50,102,2025-10-27
3,Teclado,3,75.00,101,2025-10-27
4,Monitor,1,350.00,103,2025-10-27
5,Webcam,2,80.00,102,2025-10-27
```

**clientes.json**
```json
[
    {"cliente_id": 101, "nombre": "TechCorp S.A.", "nivel": "premium", "pais": "España"},
    {"cliente_id": 102, "nombre": "StartupXYZ", "nivel": "normal", "pais": "México"},
    {"cliente_id": 103, "nombre": "Enterprise LLC", "nivel": "VIP", "pais": "Colombia"}
]
```

### Funciones a Implementar (TDD)

#### `src/sensors.py` (2 funciones, 5-7 tests)
```python
def verificar_archivo_existe(ruta: str) -> bool
def obtener_rutas_archivos_entrada() -> dict[str, str]
```

#### `src/task_groups.py` (4 funciones, 8-10 tests)
```python
def crear_task_group_ventas() -> TaskGroup
def crear_task_group_clientes() -> TaskGroup
def validar_estructura_task_group(task_group: TaskGroup) -> bool
def obtener_task_ids_en_grupo(task_group: TaskGroup) -> list[str]
```

#### `src/xcoms.py` (4 funciones, 8-10 tests)
```python
def push_metricas_xcom(ti: TaskInstance, metricas: dict) -> None
def pull_metricas_xcom(ti: TaskInstance, task_id: str) -> dict
def combinar_metricas(metricas_ventas: dict, metricas_clientes: dict) -> dict
def validar_metricas(metricas: dict) -> bool
```

#### `src/branching.py` (3 funciones, 8-10 tests)
```python
def decidir_accion_segun_ventas(total_ventas: float) -> str
def evaluar_condicion_branch(**context) -> str
def obtener_umbral_alerta() -> float
```

#### `src/extraccion.py` (4 funciones, 10-12 tests)
```python
def extraer_ventas_csv(ruta: str) -> pd.DataFrame
def extraer_clientes_json(ruta: str) -> pd.DataFrame
def validar_datos_ventas(df: pd.DataFrame) -> bool
def validar_datos_clientes(df: pd.DataFrame) -> bool
```

#### `src/transformacion.py` (5 funciones, 10-12 tests)
```python
def calcular_total_venta(df: pd.DataFrame) -> pd.DataFrame
def calcular_metricas_ventas(df: pd.DataFrame) -> dict
def calcular_metricas_clientes(df: pd.DataFrame) -> dict
def combinar_ventas_clientes(df_ventas: pd.DataFrame, df_clientes: pd.DataFrame) -> pd.DataFrame
def generar_resumen_global(df_combinado: pd.DataFrame) -> dict
```

#### `src/carga.py` (3 funciones, 6-8 tests)
```python
def guardar_reporte_csv(df: pd.DataFrame, ruta: str) -> None
def guardar_reporte_txt(metricas: dict, ruta: str) -> None
def limpiar_archivos_temporales(directorio: str) -> int
```

### Tests

**tests/test_sensors.py** (5-7 tests)
- Verificar archivo existe
- Verificar archivo no existe
- Obtener rutas correctas
- Manejo de rutas inválidas

**tests/test_task_groups.py** (8-10 tests)
- Crear TaskGroup ventas
- Crear TaskGroup clientes
- Validar estructura de TaskGroup
- Obtener task_ids correctos
- TaskGroups con dependencias internas

**tests/test_xcoms.py** (8-10 tests)
- Push métricas correctamente
- Pull métricas correctamente
- Combinar múltiples métricas
- Validar métricas correctas
- Manejo de métricas inválidas

**tests/test_branching.py** (8-10 tests)
- Decidir acción cuando ventas > umbral
- Decidir acción cuando ventas ≤ umbral
- Evaluar condición con contexto real
- Obtener umbral correcto
- Manejo de valores extremos

**tests/test_dag_intermedio.py** (8-10 tests)
- DAG se carga sin errores
- DAG tiene tasks esperadas
- Dependencias correctas
- TaskGroups creados
- Sensors configurados
- Branch configurado correctamente
- Trigger rules correctas
- Test de integración completo

---

## ⏱️ Estimación de Tiempo

### Desglose por Fase

| Fase                      | Actividad                        | Tiempo       | Responsable               |
| ------------------------- | -------------------------------- | ------------ | ------------------------- |
| **Fase 1: Contenido**     |                                  |              |                           |
|                           | 01-TEORIA.md (~5,000 palabras)   | 8 horas      | @teaching [pedagogo]      |
|                           | 02-EJEMPLOS.md (5 ejemplos)      | 7 horas      | @teaching [profesor]      |
|                           | 03-EJERCICIOS.md (15 ejercicios) | 4 horas      | @teaching [profesor]      |
|                           | Validación pedagógica            | 3 horas      | @teaching [psicólogo]     |
| **Subtotal Fase 1**       |                                  | **22 horas** |                           |
|                           |                                  |              |                           |
| **Fase 2: Proyecto**      |                                  |              |                           |
|                           | Diseño de arquitectura           | 5 horas      | @development [arquitecto] |
|                           | Escribir tests (35-40 tests)     | 9 horas      | @development [tdd]        |
|                           | Implementar funciones            | 10 horas     | @development [tdd]        |
|                           | Crear DAG completo               | 3 horas      | @development [tdd]        |
| **Subtotal Fase 2**       |                                  | **27 horas** |                           |
|                           |                                  |              |                           |
| **Fase 3: QA**            |                                  |              |                           |
|                           | Black, flake8, isort             | 2 horas      | @quality                  |
|                           | Ejecutar pytest (cobertura >85%) | 2 horas      | @quality                  |
|                           | Ejecutar DAG en Airflow          | 1 hora       | @quality                  |
|                           | Fix de errores encontrados       | 2 horas      | @quality                  |
| **Subtotal Fase 3**       |                                  | **7 horas**  |                           |
|                           |                                  |              |                           |
| **Fase 4: Documentación** |                                  |              |                           |
|                           | README del proyecto              | 2 horas      | @documentation            |
|                           | CHANGELOG del proyecto           | 0.5 horas    | @documentation            |
|                           | CHANGELOG del repositorio        | 0.5 horas    | @documentation            |
|                           | Validación final                 | 1 hora       | @documentation            |
| **Subtotal Fase 4**       |                                  | **4 horas**  |                           |

### Resumen Total

|                           | Horas        | Días (8h/día) |
| ------------------------- | ------------ | ------------- |
| **Fase 1: Contenido**     | 22           | 2.75          |
| **Fase 2: Proyecto**      | 27           | 3.4           |
| **Fase 3: QA**            | 7            | 0.9           |
| **Fase 4: Documentación** | 4            | 0.5           |
| **Buffer (15%)**          | 9            | 1.1           |
| **TOTAL**                 | **69 horas** | **8.6 días**  |

**Estimación final:** 8-9 días laborables

---

## 🎯 Criterios de Aceptación

### ✅ Contenido Educativo

- [ ] 01-TEORIA.md: ~5,000 palabras, todos los conceptos cubiertos
- [ ] 02-EJEMPLOS.md: 5 ejemplos ejecutables, todos funcionan
- [ ] 03-EJERCICIOS.md: 15 ejercicios con soluciones completas
- [ ] Progresión pedagógica validada (Básico → Intermedio → Avanzado)
- [ ] Calificación pedagógica: >9.0/10

### ✅ Proyecto Práctico

- [ ] 35-40 tests implementados
- [ ] 100% tests pasando
- [ ] Cobertura: >85%
- [ ] DAG ejecutable en Airflow
- [ ] TaskGroups funcionando
- [ ] XComs compartiendo datos
- [ ] Branching funcionando
- [ ] Sensors esperando archivos
- [ ] README completo con troubleshooting

### ✅ Calidad de Código

- [ ] `black .` sin errores
- [ ] `flake8 .` sin errores
- [ ] `isort .` sin errores
- [ ] Type hints en todas las funciones
- [ ] Docstrings en todas las funciones
- [ ] Convenciones de nombres: snake_case

### ✅ Documentación

- [ ] README del proyecto
- [ ] CHANGELOG del proyecto
- [ ] CHANGELOG del repositorio actualizado
- [ ] Comentarios claros en código
- [ ] Docstrings en DAG

---

## 📋 Checklist de Implementación

### Día 1-2: Contenido Educativo
- [ ] Crear `modulo-06-airflow/tema-2-intermedio/`
- [ ] Invocar @teaching [pedagogo] para 01-TEORIA.md
- [ ] Invocar @teaching [profesor] para 02-EJEMPLOS.md
- [ ] Invocar @teaching [profesor] para 03-EJERCICIOS.md
- [ ] Verificar que todos los ejemplos son ejecutables

### Día 3: Validación Pedagógica
- [ ] Invocar @teaching [psicólogo] para validación
- [ ] Ajustar contenido según feedback
- [ ] Confirmar calificación >9.0/10

### Día 4: Diseño del Proyecto
- [ ] Crear estructura de carpetas del proyecto
- [ ] Crear archivos de datos de prueba (ventas.csv, clientes.json)
- [ ] Invocar @development [arquitecto] para diseño
- [ ] Documentar arquitectura del DAG

### Día 5-6: Tests e Implementación (TDD)
- [ ] Invocar @development [tdd] para escribir tests primero
- [ ] Implementar `src/sensors.py` + tests
- [ ] Implementar `src/task_groups.py` + tests
- [ ] Implementar `src/xcoms.py` + tests
- [ ] Implementar `src/branching.py` + tests
- [ ] Implementar `src/extraccion.py` + tests
- [ ] Implementar `src/transformacion.py` + tests
- [ ] Implementar `src/carga.py` + tests
- [ ] Crear `dags/dag_pipeline_intermedio.py`
- [ ] Verificar: `pytest tests/ -v` (100% pasando)

### Día 7: Quality Check
- [ ] Invocar @quality para QA completo
- [ ] Ejecutar `black src/ tests/ dags/`
- [ ] Ejecutar `isort src/ tests/ dags/`
- [ ] Ejecutar `flake8 src/ tests/ dags/`
- [ ] Ejecutar `pytest --cov=src --cov-report=html`
- [ ] Verificar cobertura >85%
- [ ] Ejecutar DAG en Airflow local
- [ ] Verificar logs sin errores
- [ ] Fix de cualquier error encontrado

### Día 8: Documentación
- [ ] Crear README.md del proyecto
  - Instalación
  - Uso
  - Estructura
  - Troubleshooting
- [ ] Crear CHANGELOG.md del proyecto
- [ ] Actualizar CHANGELOG.md del repositorio
- [ ] Actualizar ORDEN_DE_IMPLEMENTACION.md
- [ ] Crear reporte de documentación

### Día 9: Revisión Final
- [ ] Validación final de todo el contenido
- [ ] Ejecutar todos los ejemplos manualmente
- [ ] Ejecutar el proyecto completo
- [ ] Verificar que todos los criterios se cumplen
- [ ] Commit y push de cambios
- [ ] Comentar en Linear
- [ ] Actualizar estado en Linear

---

## 🚨 Riesgos y Mitigaciones

### Riesgo 1: Complejidad de TaskGroups
- **Probabilidad:** Media (40%)
- **Impacto:** Medio
- **Mitigación:** Ejemplos ultra-claros, empezar simple y escalar

### Riesgo 2: XComs con Límites de Tamaño
- **Probabilidad:** Baja (20%)
- **Impacto:** Bajo
- **Mitigación:** Usar datos pequeños en ejemplos, explicar alternativas

### Riesgo 3: Sensors con Timeouts
- **Probabilidad:** Media (30%)
- **Impacto:** Bajo
- **Mitigación:** Timeouts cortos en tests (5-10s), explicar bien

### Riesgo 4: Tests de DAGs Complejos
- **Probabilidad:** Alta (50%)
- **Impacto:** Medio
- **Mitigación:** Fixtures reusables, ejemplos de tests en teoría

---

## 📈 Métricas de Éxito

| Métrica                 | Objetivo | Cómo Medir              |
| ----------------------- | -------- | ----------------------- |
| Calificación pedagógica | >9.0/10  | Validación psicólogo    |
| Tests totales           | 35-40    | `pytest --collect-only` |
| Tests pasando           | 100%     | `pytest -v`             |
| Cobertura               | >85%     | `pytest --cov`          |
| Ejemplos ejecutables    | 5/5      | Ejecutar manualmente    |
| Ejercicios con solución | 15/15    | Verificar archivo       |
| DAG ejecutable          | Sí       | Ejecutar en Airflow     |

---

## 🔗 Referencias

- **Tema 1 completado:** `modulo-06-airflow/tema-1-introduccion/`
- **Airflow Documentation - TaskGroups:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups
- **Airflow Documentation - XComs:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html
- **Airflow Documentation - Sensors:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
- **Calificación Tema 1:** 9.2/10 (baseline para superar)

---

**Documento creado:** 2025-10-27
**Autor:** @project-management
**Estado:** ✅ Planificación completada - Listo para iniciar

---

**FIN DEL DOCUMENTO DE PLANIFICACIÓN - TEMA 2**
