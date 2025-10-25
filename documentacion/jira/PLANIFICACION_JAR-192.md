# 📋 Planificación Detallada - JAR-192

**Issue:** Módulo 6: Apache Airflow y Orquestación
**Estado:** Backlog → Esperando decisión
**Prioridad:** High (2)
**URL:** https://linear.app/jarko/issue/JAR-192/modulo-6-apache-airflow-y-orquestacion
**Fecha de análisis:** 2025-10-25

---

## 📊 Resumen Ejecutivo

### Estimaciones

- **Duración total:** 16-19 días (3-4 semanas a tiempo completo)
- **Tests estimados:** 90-105 tests
- **Cobertura objetivo:** >80%
- **Contenido:** 3 temas, ~15,000 palabras, 14 ejemplos, 42 ejercicios
- **Calificación pedagógica objetivo:** >9.0/10

### Estado del Proyecto

- **Módulos completados:** 4/10 (40%)
- **Módulo 1:** 100% ✅
- **Módulo 2:** 33% 🔄
- **Módulo 3:** 33% 🔄
- **Módulo 4:** 100% ✅ (completado 2025-10-25)
- **Módulo 5:** 33% 🔄
- **Módulo 6:** 0% ⏳ ← Esta issue

---

## 🔗 Análisis de Dependencias

### ⬅️ Prerequisitos (Issues que deben completarse antes)

#### 1. JAR-191: Módulo 5 - Bases de Datos Avanzadas
- **Estado:** 33% completado (solo tema 1: PostgreSQL Avanzado)
- **Bloqueador:** ⚠️ NO COMPLETO
- **Impacto:** Medio
- **Razón:** Los pipelines de Airflow frecuentemente interactúan con bases de datos (PostgreSQL, MongoDB). Los estudiantes necesitan:
  - Conocimientos de JSONB, arrays, funciones almacenadas
  - Comprensión de transacciones y ACID
  - Experiencia con MongoDB para pipelines NoSQL
  - Modelado de datos (OLTP vs OLAP)

#### 2. JAR-189: Módulo 3 - Python para Data Engineering
- **Estado:** 33% completado
- **Bloqueador:** ⚠️ NO COMPLETO
- **Impacto:** Alto
- **Razón:** Los DAGs de Airflow están escritos en Python. Los estudiantes necesitan:
  - Pandas para transformaciones de datos
  - NumPy para operaciones numéricas
  - Procesamiento paralelo (multiprocessing, asyncio)
  - Manejo avanzado de excepciones
  - Context managers y decoradores (usados en Airflow)

#### 3. JAR-188: Módulo 2 - SQL Intermedio
- **Estado:** 33% completado (solo tema 1: SQL Básico)
- **Bloqueador:** ⚠️ NO COMPLETO
- **Impacto:** Medio-Alto
- **Razón:** Los pipelines ETL usan SQL intensivamente. Los estudiantes necesitan:
  - JOINs complejos (INNER, LEFT, RIGHT, FULL)
  - Subconsultas en WHERE, FROM, SELECT
  - CTEs (Common Table Expressions)
  - Window functions para análisis
  - Optimización de queries

### ➡️ Issues Bloqueadas (Dependen de JAR-192)

#### 1. JAR-193: Módulo 7 - Cloud Computing (AWS/GCP)
- **Razón:** Cloud pipelines usan Airflow para orquestación
- **Contenido bloqueado:**
  - AWS Step Functions vs Airflow
  - Cloud Composer (GCP)
  - Lambda functions orquestadas con Airflow

#### 2. JAR-197: Proyecto Final - Pipeline ETL Completo
- **Razón:** El proyecto final requiere orquestación con Airflow
- **Contenido bloqueado:**
  - Pipeline E2E con múltiples fuentes
  - Orquestación de transformaciones
  - Schedule y monitoreo

#### 3. JAR-198: Integración de Misiones del Juego (Módulos 6-10)
- **Razón:** Las misiones del juego para Módulo 6 requieren contenido completo
- **Contenido bloqueado:**
  - Misión: "Crear tu primer DAG"
  - Misión: "Rescatar datos con Airflow"
  - Gamificación del aprendizaje de orquestación

---

## 🚨 Análisis de Riesgos

### ⚠️ ADVERTENCIA: Dependencias Incompletas

Actualmente solo el **40% de los módulos están completados**. Implementar JAR-192 ahora presenta los siguientes riesgos:

#### 🔴 Riesgos Altos

1. **Curva de aprendizaje empinada**
   - **Descripción:** Airflow es una herramienta compleja que requiere conocimientos sólidos de Python, SQL y bases de datos
   - **Impacto:** Frustración de estudiantes, baja tasa de completitud
   - **Probabilidad:** Alta (70%)
   - **Mitigación:** Hacer el Tema 1 ultra-didáctico, con analogías efectivas y ejemplos desde cero

2. **Proyectos prácticos demasiado complejos**
   - **Descripción:** Los proyectos ETL con Airflow requieren integrar múltiples tecnologías
   - **Impacto:** Estudiantes no pueden completar proyectos, abandono
   - **Probabilidad:** Media-Alta (60%)
   - **Mitigación:** Proveer código base sólido, ejemplos ejecutables, troubleshooting detallado

3. **Falta de contexto de Data Engineering**
   - **Descripción:** Sin completar Módulos 2-5, los estudiantes no entienden POR QUÉ necesitan Airflow
   - **Impacto:** Aprendizaje superficial, no ven el valor
   - **Probabilidad:** Media (50%)
   - **Mitigación:** Incluir secciones "¿Por qué Airflow?" con casos de uso reales

#### 🟡 Riesgos Medios

4. **Problemas con Docker/Infraestructura**
   - **Descripción:** Airflow requiere Docker funcional, configuración compleja
   - **Impacto:** Estudiantes bloqueados en setup, no llegan al contenido
   - **Probabilidad:** Media (40%)
   - **Mitigación:** Validar Docker Compose antes de empezar, troubleshooting exhaustivo

5. **Testing de DAGs no-trivial**
   - **Descripción:** Testear DAGs de Airflow requiere conocimientos avanzados
   - **Impacto:** Proyectos sin tests, mala calidad
   - **Probabilidad:** Media (40%)
   - **Mitigación:** Proveer utilidades de testing, ejemplos de tests, fixtures

#### 🟢 Riesgos Bajos

6. **Tiempo de ejecución lento**
   - **Descripción:** DAGs pueden tardar minutos en ejecutarse
   - **Impacto:** Desarrollo lento, frustración
   - **Probabilidad:** Baja (20%)
   - **Mitigación:** Usar `schedule_interval=None` para desarrollo, DAGs pequeños

---

## 💡 Recomendaciones Estratégicas

### OPCIÓN A: Completar Dependencias Primero (⭐ RECOMENDADA)

#### Ventajas
1. ✅ **Estudiantes mejor preparados:** Tienen bases sólidas en Python, SQL, BD
2. ✅ **Mejor experiencia de aprendizaje:** Entienden el contexto y la utilidad
3. ✅ **Mayor tasa de completitud:** Menos frustración, más motivación
4. ✅ **Proyectos más ricos:** Pueden aplicar conocimientos previos
5. ✅ **Menor necesidad de remedial teaching:** No hay que re-explicar conceptos

#### Desventajas
1. ❌ **Retrasa este módulo ~3-4 semanas:** JAR-188, JAR-189, JAR-191 deben completarse
2. ❌ **Pierde momentum:** Después del éxito del Módulo 4, hay que esperar

#### Plan de Acción
1. Priorizar JAR-188 (Módulo 2: SQL Intermedio) - 1-2 semanas
2. Priorizar JAR-189 (Módulo 3: Python Avanzado) - 1-2 semanas
3. Completar JAR-191 (Módulo 5: Bases de Datos) - 1-1.5 semanas
4. **Entonces** iniciar JAR-192 (Módulo 6: Airflow)

#### Estimación Total
- **Tiempo hasta iniciar JAR-192:** 3-5.5 semanas
- **Tiempo total hasta completar JAR-192:** 6-9.5 semanas
- **Fecha estimada de inicio:** Mediados/finales de noviembre 2025

---

### OPCIÓN B: Implementar Ahora con Enfoque Ultra-Didáctico

#### Ventajas
1. ✅ **Avance inmediato:** El módulo está disponible antes
2. ✅ **Mantiene momentum:** Aprovecha el éxito del Módulo 4
3. ✅ **Contenido independiente:** Airflow puede enseñarse de forma aislada
4. ✅ **Infraestructura lista:** Docker Compose ya configurado
5. ✅ **Permite trabajo en paralelo:** Otros pueden trabajar en Módulos 2-5 simultáneamente

#### Desventajas
1. ❌ **Mayor riesgo de frustración:** Estudiantes sin bases sólidas
2. ❌ **Proyectos limitados:** No pueden aplicar conocimientos avanzados
3. ❌ **Más trabajo pedagógico:** Hay que explicar conceptos desde cero
4. ❌ **Posible re-work:** Si la experiencia no es buena, hay que ajustar

#### Estrategias de Mitigación

##### 1. Tema 1 Ultra-Didáctico (Nivel: Absoluto principiante)
- **Analogías poderosas:**
  - Airflow = Director de orquesta
  - DAG = Receta de cocina con pasos ordenados
  - Task = Un solo paso de la receta
  - Operator = Herramienta específica (batidora, horno)
  - Scheduler = Reloj despertador que inicia la receta
  - Executor = Chef que ejecuta el paso

- **Ejemplos ultra-simples:**
  - "Hola Mundo" con PythonOperator
  - Procesar un CSV pequeño (5 filas)
  - Insertar 3 registros en PostgreSQL

- **Sin prerequisitos:**
  - Explicar conceptos de Python cuando sea necesario
  - Proveer SQL básico en comentarios
  - Links a recursos externos (documentación Python/SQL)

##### 2. Proyectos Prácticos Graduales

**Tema 1: Proyecto Básico**
- **Entrada:** CSV con 10 filas (ventas simples)
- **Transformación:** Calcular total (precio * cantidad)
- **Salida:** CSV con totales
- **Sin base de datos** en el primer proyecto

**Tema 2: Proyecto Intermedio**
- **Entrada:** CSV + JSON (dos fuentes)
- **Transformación:** Merge con pandas
- **Salida:** PostgreSQL (conexión provista)

**Tema 3: Proyecto Avanzado**
- **Entrada:** API + CSV + PostgreSQL
- **Transformación:** Compleja con TaskGroups
- **Salida:** PostgreSQL + alertas

##### 3. Código Base Provisto

- **Templates de DAGs** listos para usar
- **Utilidades de testing** (`tests/utils/airflow_helpers.py`)
- **Fixtures de datos** pequeños y realistas
- **Scripts de setup** automatizados
- **Troubleshooting guide** exhaustivo

##### 4. Validación Pedagógica Rigurosa

- **Feedback de 2+ revisores** antes de publicar
- **Testing con estudiantes reales** si es posible
- **Iteración rápida** si algo no funciona
- **Encuestas de satisfacción** después de cada tema

#### Plan de Acción (Opción B)

1. **Día 0: Validación de infraestructura**
   ```bash
   docker-compose up -d postgres-airflow airflow-init airflow-webserver airflow-scheduler
   docker-compose ps
   # Verificar: http://localhost:8080 (admin / Airflow2025!Admin)
   ```

2. **Días 1-6: Tema 1 (Ultra-didáctico)**
   - Invocar `@teaching [pedagogo]` para 01-TEORIA.md
   - Invocar `@teaching [profesor]` para 02-EJEMPLOS.md y 03-EJERCICIOS.md
   - Invocar `@teaching [psicólogo]` para validación pedagógica
   - Invocar `@development [arquitecto]` para diseño de proyecto básico
   - Invocar `@development [tdd]` para tests e implementación
   - Invocar `@quality` para QA

3. **Días 7-12: Tema 2**
   - Repetir workflow con aumento gradual de complejidad

4. **Días 13-17: Tema 3**
   - Repetir workflow con casos productivos

5. **Días 18-19: Documentación y cierre**
   - READMEs, CHANGELOG, revisión final
   - Mover a "Done" en Linear

---

## 🎯 Decisión Recomendada

### ⭐ OPCIÓN A: COMPLETAR DEPENDENCIAS PRIMERO

**Razón principal:** La calidad pedagógica es más importante que la velocidad.

**Justificación:**
1. El Módulo 4 logró 9.3/10 porque los estudiantes tenían los fundamentos (Módulo 1 completo)
2. Airflow es complejo y requiere bases sólidas
3. El objetivo del Master es formar profesionales competentes, no solo entregar contenido rápido
4. Las issues JAR-188, JAR-189, JAR-191 también son High priority
5. 3-4 semanas de espera es razonable para asegurar calidad

**Próximos pasos si se elige Opción A:**
1. Mantener JAR-192 en Backlog con etiqueta "Ready to Start"
2. Comentar en Linear: "En espera de dependencias (JAR-188, JAR-189, JAR-191)"
3. Priorizar completar Módulos 2, 3, 5
4. Retomar JAR-192 cuando las bases estén sólidas

---

## 📚 Contenido Detallado

### 📁 Estructura de Carpetas

```
modulo-06-airflow/
├── README.md                           (~1,500 palabras)
│
├── tema-1-introduccion/
│   ├── 01-TEORIA.md                    (~5,000 palabras)
│   ├── 02-EJEMPLOS.md                  (5 ejemplos ejecutables)
│   ├── 03-EJERCICIOS.md                (15 ejercicios con soluciones)
│   └── 04-proyecto-practico/
│       ├── README.md                   (~1,000 palabras)
│       ├── requirements.txt            (apache-airflow, pytest, etc.)
│       ├── pyproject.toml              (configuración del proyecto)
│       ├── dags/
│       │   └── dag_etl_simple.py       (~150 líneas)
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py             (fixtures de Airflow)
│       │   ├── test_dag_etl_simple.py  (25-30 tests)
│       │   └── utils/
│       │       └── airflow_helpers.py  (utilidades de testing)
│       └── src/
│           ├── __init__.py
│           ├── extraccion.py           (funciones de extracción)
│           ├── transformacion.py       (funciones de transformación)
│           ├── carga.py                (funciones de carga)
│           └── utilidades_airflow.py   (helpers generales)
│
├── tema-2-intermedio/
│   ├── 01-TEORIA.md                    (~5,000 palabras)
│   ├── 02-EJEMPLOS.md                  (5 ejemplos ejecutables)
│   ├── 03-EJERCICIOS.md                (15 ejercicios con soluciones)
│   └── 04-proyecto-practico/
│       ├── README.md
│       ├── requirements.txt
│       ├── pyproject.toml
│       ├── dags/
│       │   └── dag_complejo.py         (~250 líneas)
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py
│       │   ├── test_dag_complejo.py    (30-35 tests)
│       │   ├── test_task_groups.py     (8-10 tests)
│       │   └── test_xcoms.py           (8-10 tests)
│       └── src/
│           ├── __init__.py
│           ├── task_groups.py          (definición de TaskGroups)
│           ├── xcoms.py                (manejo de XComs)
│           ├── branching.py            (lógica de branching)
│           └── sensors.py              (custom sensors)
│
└── tema-3-produccion/
    ├── 01-TEORIA.md                    (~5,000 palabras)
    ├── 02-EJEMPLOS.md                  (4 ejemplos ejecutables)
    ├── 03-EJERCICIOS.md                (12 ejercicios con soluciones)
    └── 04-proyecto-practico/
        ├── README.md
        ├── requirements.txt
        ├── pyproject.toml
        ├── dags/
        │   └── dag_productivo.py       (~300 líneas)
        ├── tests/
        │   ├── __init__.py
        │   ├── conftest.py
        │   ├── test_dag_productivo.py  (20-25 tests)
        │   ├── test_alertas.py         (8-10 tests)
        │   ├── test_monitoreo.py       (8-10 tests)
        │   └── test_integracion.py     (5-8 tests)
        └── src/
            ├── __init__.py
            ├── variables.py            (manejo de Variables)
            ├── connections.py          (manejo de Connections)
            ├── alertas.py              (sistema de alertas)
            ├── monitoreo.py            (monitoreo y SLAs)
            └── testing_utils.py        (utilidades para testing)
```

---

### 📖 Tema 1: Introducción a Airflow

#### 01-TEORIA.md (~5,000 palabras, ~35 minutos lectura)

**Estructura:**

1. **¿Qué es Apache Airflow?** (500 palabras)
   - Analogía: Director de orquesta
   - Problema que resuelve: Workflows complejos, dependencias, fallos
   - Casos de uso: ETL, ML pipelines, backups, reportes

2. **Conceptos Fundamentales** (1,500 palabras)
   - **DAG (Directed Acyclic Graph)**
     - Analogía: Receta de cocina con pasos ordenados
     - Ejemplo visual: `A → B → C → D`
     - Directed: Flechas indican dirección
     - Acyclic: Sin ciclos infinitos
   - **Task**
     - Un solo paso ejecutable
     - Ejemplo: "Descargar archivo", "Transformar datos"
   - **Operator**
     - Tipo de tarea
     - PythonOperator, BashOperator, DummyOperator
   - **Scheduler**
     - Reloj despertador del workflow
     - Revisa DAGs cada N segundos
   - **Executor**
     - Trabajador que ejecuta tasks
     - LocalExecutor, CeleryExecutor, KubernetesExecutor
   - **Webserver**
     - Interfaz visual (UI)
     - Monitoreo, logs, ejecución manual

3. **Instalación y Configuración** (800 palabras)
   - Docker Compose (ya configurado)
   - Verificar servicios: `docker-compose ps`
   - Acceso a UI: `http://localhost:8080`
   - Credenciales: `admin` / `Airflow2025!Admin`
   - Tour de la UI:
     - DAGs page
     - Graph View
     - Tree View
     - Logs
     - Admin → Variables/Connections

4. **Tu Primer DAG: "Hola Mundo"** (1,000 palabras)
   - Código comentado línea por línea
   ```python
   from datetime import datetime
   from airflow import DAG
   from airflow.operators.python import PythonOperator

   def saludar():
       print("¡Hola desde Airflow!")

   with DAG(
       dag_id="hola_mundo",
       start_date=datetime(2025, 1, 1),
       schedule="@daily",
       catchup=False,
   ) as dag:
       task_saludar = PythonOperator(
           task_id="saludar",
           python_callable=saludar,
       )
   ```
   - Explicación de cada parámetro
   - Cómo ejecutar desde UI
   - Cómo ver logs

5. **Operators Básicos** (800 palabras)
   - **PythonOperator:** Ejecutar función Python
   - **BashOperator:** Ejecutar comando shell
   - **DummyOperator:** Nodo de control (sin ejecución)
   - Cuándo usar cada uno

6. **Dependencias entre Tasks** (400 palabras)
   - Operador `>>` (downstream)
   - Operador `<<` (upstream)
   - Ejemplos:
     ```python
     A >> B >> C  # Secuencial
     A >> [B, C] >> D  # Paralelo
     ```

7. **Schedule Intervals** (500 palabras)
   - Cron expressions: `0 0 * * *` (diario a medianoche)
   - Presets: `@daily`, `@hourly`, `@weekly`
   - `None` para ejecución manual
   - `catchup=False` para no ejecutar histórico

8. **Mejores Prácticas** (500 palabras)
   - Un DAG por archivo Python
   - Nombres descriptivos (snake_case)
   - Docstrings en DAGs
   - `catchup=False` por defecto
   - Tasks idempotentes (misma entrada → misma salida)

#### 02-EJEMPLOS.md (5 ejemplos trabajados, ~90 minutos)

**Ejemplo 1: DAG Básico "Hola Mundo"** (15 min) ⭐
- Código completo y ejecutable
- Salida esperada en logs
- Captura de pantalla de UI

**Ejemplo 2: Pipeline ETL Simple (Extract → Transform → Load)** (20 min) ⭐⭐
- 3 tasks con PythonOperator
- Extract: Leer CSV con pandas
- Transform: Calcular totales
- Load: Escribir CSV resultante
- Dependencias: `extract >> transform >> load`

**Ejemplo 3: Pipeline con BashOperator** (15 min) ⭐
- Ejecutar script shell para crear directorio
- Copiar archivo con `cp`
- Comprimir con `gzip`
- Dependencias secuenciales

**Ejemplo 4: Dependencias en Paralelo (Fan-out, Fan-in)** (20 min) ⭐⭐
```
    start
    ↓
   ├──→ procesar_ventas
   ├──→ procesar_inventario
   └──→ procesar_clientes
       ↓
       → generar_reporte
```
- 4 tasks en paralelo (procesar_*)
- 1 task final que espera a todas (generar_reporte)
- DummyOperator para `start`

**Ejemplo 5: Schedule con Cron** (20 min) ⭐⭐
- DAG que se ejecuta diariamente a las 3 AM
- DAG que se ejecuta cada lunes
- DAG que se ejecuta cada 30 minutos
- Explicación de `start_date` y `schedule`
- Cómo ver próximas ejecuciones en UI

#### 03-EJERCICIOS.md (15 ejercicios, ~4-6 horas)

**Básicos (1-5):** ⭐
1. Crear DAG que imprima tu nombre con PythonOperator
2. Modificar schedule de "Hola Mundo" a cada hora (`@hourly`)
3. Crear DAG con 2 tasks secuenciales: `A >> B`
4. Crear DAG con BashOperator que liste archivos (`ls -la`)
5. Añadir docstring a un DAG existente

**Intermedios (6-10):** ⭐⭐
6. Crear pipeline ETL: leer CSV, filtrar filas, escribir resultado
7. Crear DAG con 3 tasks en paralelo
8. Usar PythonOperator para crear archivo de log con timestamp
9. Crear DAG que se ejecute solo lunes y viernes
10. Combinar PythonOperator y BashOperator en el mismo DAG

**Avanzados (11-15):** ⭐⭐⭐
11. Crear pipeline que procese 3 CSV diferentes y genere 1 consolidado
12. Implementar error handling: task que falla y se reintenta
13. Crear DAG con 10 tasks: 5 en paralelo, luego 3, luego 2
14. Pipeline que valida datos antes de procesar (si inválido, abortar)
15. DAG que genera archivo con timestamp y lo comprime con gzip

**Soluciones:** Código completo en cada ejercicio (toggle/details)

#### 04-proyecto-practico/ (TDD - 25-30 tests, ~16 horas)

**Descripción del Proyecto: Pipeline ETL Simple**

Un pipeline que:
1. **Extract:** Lee archivo CSV de ventas (`ventas.csv`)
2. **Transform:** Calcula total por producto (precio * cantidad)
3. **Load:** Escribe resultados en nuevo CSV (`ventas_totales.csv`)

**Archivo de entrada:** `ventas.csv`
```csv
producto,cantidad,precio_unitario
Laptop,3,1200.00
Mouse,10,25.50
Teclado,5,75.00
```

**Archivo de salida esperado:** `ventas_totales.csv`
```csv
producto,total
Laptop,3600.00
Mouse,255.00
Teclado,375.00
```

**Funciones a Implementar (TDD):**

`src/extraccion.py` (3 funciones, 8 tests)
- `leer_csv_ventas(ruta: str) -> pd.DataFrame`
- `validar_estructura_ventas(df: pd.DataFrame) -> bool`
- `obtener_ruta_archivo_entrada() -> str`

`src/transformacion.py` (2 funciones, 8 tests)
- `calcular_totales_por_producto(df: pd.DataFrame) -> pd.DataFrame`
- `validar_datos_numericos(df: pd.DataFrame) -> bool`

`src/carga.py` (2 funciones, 6 tests)
- `escribir_csv_resultados(df: pd.DataFrame, ruta: str) -> None`
- `obtener_ruta_archivo_salida() -> str`

`dags/dag_etl_simple.py` (1 DAG, 8 tests)
- Test: DAG existe y se puede importar
- Test: DAG tiene 3 tasks (extract, transform, load)
- Test: Dependencias correctas (extract >> transform >> load)
- Test: schedule es None (ejecución manual)
- Test: catchup es False
- Test: DAG es válido (no errores de sintaxis)
- Test de integración: Ejecutar DAG completo con datos de prueba
- Test de integración: Verificar archivo de salida creado

**Tecnologías:**
- apache-airflow==2.7.3
- pandas==2.1.3
- pytest==7.4.3
- pytest-cov==4.1.0

**Cobertura objetivo:** >80%

---

### 📖 Tema 2: Airflow Intermedio

#### 01-TEORIA.md (~5,000 palabras, ~35 minutos)

**Estructura:**

1. **TaskGroups: Organización Visual** (800 palabras)
   - Problema: DAGs con 20+ tasks son difíciles de leer
   - Solución: Agrupar tasks relacionadas
   - Ejemplo: TaskGroup "procesar_ventas" con 5 sub-tasks
   - Ventajas sobre SubDAGs (deprecado)

2. **SubDAGs (Contexto Histórico)** (400 palabras)
   - Qué eran SubDAGs (deprecado en Airflow 2.0+)
   - Por qué se deprecaron (problemas de scheduler)
   - Alternativa moderna: TaskGroups
   - Cuándo aún se encuentran en código legacy

3. **XComs: Comunicación entre Tasks** (1,000 palabras)
   - Problema: Tasks aisladas sin compartir datos
   - Solución: XComs (Cross-Communication)
   - `ti.xcom_push(key="resultado", value=42)`
   - `ti.xcom_pull(task_ids="tarea_anterior", key="resultado")`
   - Limitaciones: Solo datos serializables (JSON)
   - Tamaño máximo: 48KB en LocalExecutor
   - Alternativa para datos grandes: Archivos o base de datos

4. **Branching: Condicionales en DAGs** (1,000 palabras)
   - BranchPythonOperator: Elegir camino según condición
   - Ejemplo: Si ventas > 10000 → procesar_premium, sino → procesar_normal
   - `trigger_rule="none_failed_min_one_success"`
   - Cuidado con skip downstream

5. **Sensors: Esperar por Condiciones** (1,200 palabras)
   - FileSensor: Esperar que exista un archivo
   - TimeSensor: Esperar hasta hora específica
   - ExternalTaskSensor: Esperar que otro DAG termine
   - HttpSensor: Esperar que API responda
   - Parámetros:
     - `poke_interval`: Cada cuánto verificar (segundos)
     - `timeout`: Tiempo máximo de espera
     - `mode="reschedule"`: No bloquear worker slot

6. **Triggers: Iniciar DAGs desde Otros DAGs** (600 palabras)
   - TriggerDagRunOperator
   - Pasar parámetros con `conf`
   - Usar con ExternalTaskSensor

7. **Dynamic DAG Generation** (600 palabras)
   - Generar tasks en bucle
   - Ejemplo: Procesar 10 archivos con 1 task cada uno
   - Límites: No abusar (max 50-100 tasks)

8. **Templating con Jinja2** (400 palabras)
   - Variables dinámicas: `{{ ds }}` (fecha de ejecución)
   - Macros: `{{ macros.datetime.now() }}`
   - Personalización de paths con fechas

#### 02-EJEMPLOS.md (5 ejemplos, ~100 minutos)

**Ejemplo 1: TaskGroup para Organizar Pipeline** (20 min) ⭐⭐
```
dag
├── inicio
├── grupo_procesamiento
│   ├── validar_datos
│   ├── transformar_datos
│   └── calcular_metricas
└── cargar_resultados
```

**Ejemplo 2: XComs - Pasar Datos entre Tasks** (20 min) ⭐⭐
- Task 1: Calcular total de ventas → push con XCom
- Task 2: Leer total desde XCom → generar reporte

**Ejemplo 3: BranchPythonOperator - Elegir Camino** (25 min) ⭐⭐⭐
```
inicio
  ↓
validar_ventas (branch)
  ├──→ (ventas > 10000) procesar_premium → notificar_gerente
  └──→ (ventas ≤ 10000) procesar_normal → guardar_log
  ↓
fin (join)
```

**Ejemplo 4: FileSensor - Esperar Archivo** (20 min) ⭐⭐
- Sensor espera `datos.csv` (timeout 60 segundos)
- Cuando aparece → procesar archivo

**Ejemplo 5: Dynamic DAG - Generar Tasks en Loop** (15 min) ⭐⭐
```python
for i in range(5):
    task = PythonOperator(
        task_id=f"procesar_archivo_{i}",
        python_callable=procesar_archivo,
        op_kwargs={"archivo_id": i},
    )
    inicio >> task >> fin
```

#### 03-EJERCICIOS.md (15 ejercicios, ~5-7 horas)

**Básicos (1-5):** ⭐
1. Crear TaskGroup con 3 tasks dentro
2. Usar XCom para pasar un número entre 2 tasks
3. Crear BranchPythonOperator simple (if-else)
4. Usar FileSensor con timeout de 30 segundos
5. Crear 3 tasks dinámicamente con loop

**Intermedios (6-10):** ⭐⭐
6. TaskGroup anidado (grupo dentro de grupo)
7. XComs con diccionario completo (múltiples valores)
8. Branch con 3 caminos posibles
9. TimeSensor que espera hasta las 9 AM
10. Dynamic DAG con 10 tasks + dependencias

**Avanzados (11-15):** ⭐⭐⭐
11. Pipeline con TaskGroups, XComs y Branch
12. ExternalTaskSensor (DAG A espera a DAG B)
13. TriggerDagRunOperator con parámetros
14. Dynamic DAG que lee archivos de directorio
15. Pipeline completo: Sensor → Branch → TaskGroups → XComs

#### 04-proyecto-practico/ (TDD - 30-35 tests, ~18 horas)

**Descripción: Pipeline Complejo con Múltiples Fuentes**

Pipeline que:
1. Espera 2 archivos: `ventas.csv` y `clientes.json`
2. Procesa ambos en paralelo (TaskGroup para cada uno)
3. Combina resultados (JOIN con pandas)
4. Branching: Si total_ventas > 50000 → enviar_alerta_premium, sino → log_normal
5. Usa XComs para pasar métricas entre tasks

**Fuentes:**
- `ventas.csv`: producto, cantidad, precio, cliente_id
- `clientes.json`: cliente_id, nombre, nivel (normal, premium, VIP)

**Flujo:**
```
inicio
  ↓
[esperar_ventas, esperar_clientes] (FileSensors)
  ↓
[grupo_procesar_ventas, grupo_procesar_clientes] (TaskGroups)
  ↓
combinar_datos (JOIN)
  ↓
calcular_metricas (XCom push: total_ventas, count_clientes)
  ↓
decidir_accion (Branch)
  ├──→ (total > 50000) enviar_alerta_premium
  └──→ (total ≤ 50000) log_normal
  ↓
fin
```

**Cobertura objetivo:** >80%

---

### 📖 Tema 3: Airflow en Producción

#### 01-TEORIA.md (~5,000 palabras, ~35 minutos)

**Estructura:**

1. **Variables y Connections** (1,200 palabras)
   - Variables: Configuración global (`AIRFLOW_VAR_*)
   - Connections: Credenciales de BD/APIs
   - UI: Admin → Variables/Connections
   - Python API: `Variable.get("nombre")`, `Connection.get_connection_from_secrets("postgres")`
   - Secrets Backend: Integración con Vault, AWS Secrets Manager

2. **Logs y Monitoreo** (1,000 palabras)
   - Logs de tasks (stdout/stderr)
   - Logs del scheduler
   - Logs del webserver
   - Configurar log level (DEBUG, INFO, WARNING, ERROR)
   - Integración con ELK, Datadog, CloudWatch
   - Métricas de Airflow (task duration, success rate)

3. **Testing de DAGs** (1,200 palabras)
   - Unit tests: Validar estructura del DAG
   - Integration tests: Ejecutar DAG completo en ambiente de prueba
   - Fixtures: `pytest.fixture` para setup de Airflow
   - Utilidades: `DagBag`, `dag.test()`
   - Ejemplo:
   ```python
   def test_dag_loaded():
       from airflow.models import DagBag
       dagbag = DagBag()
       assert "mi_dag" in dagbag.dags
       assert dagbag.import_errors == {}
   ```

4. **Mejores Prácticas** (1,200 palabras)
   - **Idempotencia:** Mismo input → mismo output (crucial)
   - **Retry strategies:** `retries=3`, `retry_delay=timedelta(minutes=5)`
   - **SLAs (Service Level Agreements):** `sla=timedelta(hours=2)`
   - **Alertas:** Email/Slack en caso de fallo
   - **Resource management:** Pools, priority_weight
   - **Documentación:** `doc_md` en DAGs
   - **Versionado:** Git para DAGs

5. **Ejecutores** (800 palabras)
   - **LocalExecutor:** Desarrollo, 1 máquina
   - **CeleryExecutor:** Producción, múltiples workers
   - **KubernetesExecutor:** Cloud, escalado dinámico
   - **SequentialExecutor:** Solo 1 task a la vez (no recomendado)

6. **Performance Optimization** (600 palabras)
   - Paralelismo: `parallelism`, `max_active_runs`
   - Pools: Limitar concurrencia por tipo de recurso
   - DAG serialization: Reducir carga del scheduler
   - Task duration: Evitar tasks que tarden >1 hora

#### 02-EJEMPLOS.md (4 ejemplos, ~80 minutos)

**Ejemplo 1: Configurar Variables y Connections** (20 min) ⭐
- Crear Variable "ambiente" = "produccion"
- Crear Connection "postgres_prod"
- Usar en DAG: `Variable.get("ambiente")`

**Ejemplo 2: Alertas por Email en Caso de Fallo** (25 min) ⭐⭐
- Configurar `default_args` con `email`, `email_on_failure=True`
- Simular task que falla → recibir alerta (mock)

**Ejemplo 3: Tests Unitarios de un DAG** (20 min) ⭐⭐
```python
def test_dag_structure():
    dag = DagBag().get_dag("mi_dag")
    assert len(dag.tasks) == 5
    assert "extract" in dag.task_ids
```

**Ejemplo 4: SLA Monitoring** (15 min) ⭐⭐
- Configurar `sla=timedelta(minutes=30)`
- Task que tarda 40 minutos → SLA miss registrado

#### 03-EJERCICIOS.md (12 ejercicios, ~4-5 horas)

**Básicos (1-4):** ⭐
1. Crear Variable en UI y leerla en DAG
2. Configurar Connection a PostgreSQL local
3. Añadir `retries=2` a un task
4. Escribir test que valida que DAG tiene 3 tasks

**Intermedios (5-8):** ⭐⭐
5. Usar Variable para decidir branch (produccion vs desarrollo)
6. Configurar alertas por email (mock)
7. Escribir test de integración que ejecuta DAG
8. Configurar SLA de 10 minutos

**Avanzados (9-12):** ⭐⭐⭐
9. Implementar retry exponencial (1min, 2min, 4min)
10. Crear Pool "db_connections" con limit=3, asignar tasks
11. Pipeline con logs estructurados (JSON)
12. Test completo: DAG + integración + cobertura >85%

#### 04-proyecto-practico/ (TDD - 35-40 tests, ~20 horas)

**Descripción: Pipeline Productivo con Alertas y Monitoreo**

Pipeline E2E que:
1. Extrae datos de API (simulada)
2. Transforma con pandas
3. Carga a PostgreSQL
4. Monitorea SLAs
5. Envía alertas si algo falla
6. Usa Variables/Connections
7. Tests completos (>85% cobertura)

**Arquitectura:**
```
inicio
  ↓
validar_conexiones (Variable.get, Connection.get)
  ↓
extraer_datos_api (PythonOperator, retry=3)
  ↓
validar_datos (si inválido → alerta)
  ↓
transformar_datos (TaskGroup con 3 sub-tasks)
  ↓
cargar_postgres (Connection "postgres_prod")
  ↓
generar_metricas (XCom: rows_processed, duration)
  ↓
verificar_sla (SLA: 1 hora)
  ↓
enviar_alerta_exito (mock email)
```

**Variables:**
- `ambiente`: "produccion" | "desarrollo"
- `api_url`: URL de la API
- `max_retries`: Número de reintentos

**Connections:**
- `postgres_prod`: PostgreSQL local

**Funciones a Implementar:**

`src/variables.py` (3 funciones, 8 tests)
- `obtener_variable(nombre: str, default: Any) -> Any`
- `validar_ambiente() -> str`
- `obtener_configuracion() -> dict`

`src/connections.py` (3 funciones, 8 tests)
- `obtener_connection_postgres() -> Connection`
- `validar_connection(conn: Connection) -> bool`
- `obtener_credenciales_postgres() -> dict`

`src/alertas.py` (3 funciones, 10 tests)
- `enviar_alerta_fallo(contexto: dict) -> None`
- `enviar_alerta_exito(metricas: dict) -> None`
- `formatear_mensaje_alerta(tipo: str, datos: dict) -> str`

`src/monitoreo.py` (3 funciones, 9 tests)
- `calcular_duracion(start: datetime, end: datetime) -> float`
- `verificar_sla(duracion: float, sla_minutos: int) -> bool`
- `generar_reporte_metricas(datos: dict) -> dict`

**Cobertura objetivo:** >85%

---

## ⏱️ Estimación Detallada de Tiempo

### Desglose por Actividad y Tema

#### **Tema 1: Introducción a Airflow**

| Actividad                        | Tiempo Estimado        | Responsable               | Notas                             |
| -------------------------------- | ---------------------- | ------------------------- | --------------------------------- |
| 01-TEORIA.md (~5,000 palabras)   | 8 horas                | @teaching [pedagogo]      | Analogías, desde cero             |
| 02-EJEMPLOS.md (5 ejemplos)      | 6 horas                | @teaching [profesor]      | Ejecutables y documentados        |
| 03-EJERCICIOS.md (15 ejercicios) | 4 horas                | @teaching [profesor]      | Con soluciones completas          |
| Validación pedagógica            | 3 horas                | @teaching [psicólogo]     | Feedback y ajustes                |
| Diseño proyecto práctico         | 4 horas                | @development [arquitecto] | Estructura TDD                    |
| Tests proyecto (25-30 tests)     | 8 horas                | @development [tdd]        | Escribir tests PRIMERO            |
| Implementación proyecto          | 8 horas                | @development [tdd]        | Código hasta pasar tests          |
| Quality check                    | 3 horas                | @quality                  | Black, flake8, pytest             |
| README proyecto                  | 2 horas                | @documentation            | Instalación, uso, troubleshooting |
| **SUBTOTAL TEMA 1**              | **46 horas (~6 días)** |                           |                                   |

#### **Tema 2: Airflow Intermedio**

| Actividad                        | Tiempo Estimado          | Responsable               | Notas                      |
| -------------------------------- | ------------------------ | ------------------------- | -------------------------- |
| 01-TEORIA.md (~5,000 palabras)   | 8 horas                  | @teaching [pedagogo]      | TaskGroups, XComs, Sensors |
| 02-EJEMPLOS.md (5 ejemplos)      | 7 horas                  | @teaching [profesor]      | Casos más complejos        |
| 03-EJERCICIOS.md (15 ejercicios) | 4 horas                  | @teaching [profesor]      | Con soluciones             |
| Validación pedagógica            | 3 horas                  | @teaching [psicólogo]     | Feedback                   |
| Diseño proyecto práctico         | 5 horas                  | @development [arquitecto] | Multi-fuente, branching    |
| Tests proyecto (30-35 tests)     | 9 horas                  | @development [tdd]        | Tests primero              |
| Implementación proyecto          | 10 horas                 | @development [tdd]        | Código hasta pasar tests   |
| Quality check                    | 3 horas                  | @quality                  | Black, flake8, pytest      |
| README proyecto                  | 2 horas                  | @documentation            | Documentación completa     |
| **SUBTOTAL TEMA 2**              | **51 horas (~6.5 días)** |                           |                            |

#### **Tema 3: Airflow en Producción**

| Actividad                        | Tiempo Estimado          | Responsable               | Notas                                 |
| -------------------------------- | ------------------------ | ------------------------- | ------------------------------------- |
| 01-TEORIA.md (~5,000 palabras)   | 8 horas                  | @teaching [pedagogo]      | Variables, testing, mejores prácticas |
| 02-EJEMPLOS.md (4 ejemplos)      | 5 horas                  | @teaching [profesor]      | Testing, alertas, SLAs                |
| 03-EJERCICIOS.md (12 ejercicios) | 3 horas                  | @teaching [profesor]      | Casos productivos                     |
| Validación pedagógica            | 3 horas                  | @teaching [psicólogo]     | Feedback                              |
| Diseño proyecto práctico         | 6 horas                  | @development [arquitecto] | Pipeline productivo completo          |
| Tests proyecto (35-40 tests)     | 10 horas                 | @development [tdd]        | Cobertura >85%                        |
| Implementación proyecto          | 11 horas                 | @development [tdd]        | Código robusto                        |
| Quality check                    | 4 horas                  | @quality                  | Black, flake8, pytest                 |
| README proyecto                  | 2 horas                  | @documentation            | Guía de producción                    |
| **SUBTOTAL TEMA 3**              | **52 horas (~6.5 días)** |                           |                                       |

#### **Documentación Global y Cierre**

| Actividad                    | Tiempo Estimado          | Responsable           | Notas                |
| ---------------------------- | ------------------------ | --------------------- | -------------------- |
| README.md del módulo         | 3 horas                  | @documentation        | Visión general, guía |
| CHANGELOG.md actualización   | 1 hora                   | @documentation        | Añadir JAR-192       |
| README.md raíz actualización | 0.5 horas                | @documentation        | Módulo 6: 100%       |
| Revisión final pedagógica    | 4 horas                  | @teaching [psicólogo] | Review global        |
| Quality check global         | 3 horas                  | @quality              | Verificar todo       |
| Comentario en Linear         | 0.5 horas                | @project-management   | Marcar Done          |
| **SUBTOTAL DOCUMENTACIÓN**   | **12 horas (~1.5 días)** |                       |                      |

### 📊 Resumen de Estimación

| Fase                   | Tiempo Estimado | Días Hábiles  |
| ---------------------- | --------------- | ------------- |
| Tema 1: Introducción   | 46 horas        | 6 días        |
| Tema 2: Intermedio     | 51 horas        | 6.5 días      |
| Tema 3: Producción     | 52 horas        | 6.5 días      |
| Documentación y cierre | 12 horas        | 1.5 días      |
| **TOTAL**              | **161 horas**   | **20.5 días** |

**Asumiendo:**
- 8 horas/día de trabajo efectivo
- 1 persona trabajando full-time
- Sin bloqueadores mayores

**Estimación Final:** 3-4 semanas (incluyendo buffer para imprevistos)

---

## 🎯 Criterios de Aceptación Detallados

### ✅ Contenido Educativo

| Criterio                 | Objetivo          | Verificación                     |
| ------------------------ | ----------------- | -------------------------------- |
| Temas completados        | 3/3               | ✅ TEORIA + EJEMPLOS + EJERCICIOS |
| Palabras de teoría total | >12,000           | Contar con `wc -w`               |
| Ejemplos ejecutables     | >12               | Ejecutar cada uno                |
| Ejercicios totales       | >40               | Verificar archivo                |
| Soluciones de ejercicios | 100%              | Todas tienen solución            |
| Progresión pedagógica    | Básico → Avanzado | Validación psicólogo             |

### ✅ Proyectos Prácticos (TDD)

| Criterio              | Objetivo | Verificación              |
| --------------------- | -------- | ------------------------- |
| Proyectos completados | 3/3      | Tema 1, 2, 3              |
| Tests totales         | >90      | `pytest --collect-only`   |
| Tests pasando         | 100%     | `pytest -v`               |
| Cobertura global      | >80%     | `pytest --cov`            |
| Cobertura Tema 3      | >85%     | `pytest --cov` en tema 3  |
| DAGs ejecutables      | Todos    | Ejecutar en Airflow local |
| Type hints            | 100%     | Verificar con mypy        |
| Docstrings            | 100%     | Revisar manualmente       |

### ✅ Calidad de Código

| Criterio             | Objetivo     | Verificación                        |
| -------------------- | ------------ | ----------------------------------- |
| Black                | 0 errores    | `black --check .`                   |
| Flake8               | 0 errores    | `flake8 .`                          |
| Tests unitarios      | 100% pasando | `pytest tests/`                     |
| Tests integración    | 100% pasando | `pytest tests/test_integracion*.py` |
| Nombres descriptivos | 100%         | Code review                         |
| Imports ordenados    | 100%         | Estándar → Externo → Interno        |
| Funciones <50 líneas | >90%         | Revisar complejidad                 |

### ✅ Documentación

| Criterio              | Objetivo    | Verificación                      |
| --------------------- | ----------- | --------------------------------- |
| README.md módulo      | Completo    | Leer y verificar                  |
| 3 READMEs proyectos   | Completos   | Instalación, uso, troubleshooting |
| CHANGELOG.md          | Actualizado | Ver sección JAR-192               |
| README.md raíz        | Actualizado | Módulo 6: 100%                    |
| Docstrings en DAGs    | 100%        | Verificar `doc_md`                |
| Comentarios en código | Claros      | Code review                       |

### ✅ Validación Pedagógica

| Criterio                | Objetivo     | Verificación          |
| ----------------------- | ------------ | --------------------- |
| Calificación pedagógica | >9.0/10      | Validación psicólogo  |
| Analogías efectivas     | Sí           | Feedback revisor      |
| Ejemplos del mundo real | Sí           | Verificar ejemplos    |
| Progresión lógica       | Sí           | Validación pedagógica |
| Feedback de revisores   | 2+ revisores | Recopilar feedback    |

### ✅ Infraestructura

| Criterio                 | Objetivo  | Verificación           |
| ------------------------ | --------- | ---------------------- |
| Docker Compose funcional | Sí        | `docker-compose up -d` |
| Airflow UI accesible     | Sí        | http://localhost:8080  |
| PostgreSQL backend       | Operativo | `docker-compose ps`    |
| Scheduler ejecutándose   | Sí        | Logs sin errores       |
| DAGs detectados          | Todos     | Ver en UI              |

---

## 📋 Checklist de Implementación

### Fase 0: Preparación (1 día)

- [ ] Validar Docker Compose: `docker-compose up -d`
- [ ] Verificar Airflow UI: http://localhost:8080
- [ ] Login: `admin` / `Airflow2025!Admin`
- [ ] Crear estructura de carpetas:
  ```bash
  mkdir -p modulo-06-airflow/{tema-1-introduccion,tema-2-intermedio,tema-3-produccion}/04-proyecto-practico/{dags,tests,src}
  ```
- [ ] Comentar en Linear: "Iniciando JAR-192, infraestructura validada"
- [ ] Mover JAR-192 a "In Progress" en Linear

### Fase 1: Tema 1 - Introducción (6 días)

**Día 1-2: Contenido Educativo**
- [ ] Invocar `@teaching [pedagogo]` para crear `01-TEORIA.md`
  - [ ] ~5,000 palabras
  - [ ] Analogías efectivas (orquesta, receta)
  - [ ] Conceptos desde cero
- [ ] Invocar `@teaching [profesor]` para crear `02-EJEMPLOS.md`
  - [ ] 5 ejemplos ejecutables
  - [ ] Desde "Hola Mundo" hasta ETL simple
- [ ] Invocar `@teaching [profesor]` para crear `03-EJERCICIOS.md`
  - [ ] 15 ejercicios (5 básicos, 5 intermedios, 5 avanzados)
  - [ ] Soluciones completas

**Día 3: Validación Pedagógica**
- [ ] Invocar `@teaching [psicólogo]` para validar progresión
- [ ] Ajustar contenido según feedback

**Día 4: Diseño y Tests**
- [ ] Invocar `@development [arquitecto]` para diseñar proyecto práctico
  - [ ] Pipeline ETL simple (CSV → transformación → CSV)
- [ ] Invocar `@development [tdd]` para escribir tests PRIMERO
  - [ ] 25-30 tests
  - [ ] Tests de DAG, funciones, integración

**Día 5: Implementación**
- [ ] Invocar `@development [tdd]` para implementar código
  - [ ] `src/extraccion.py`
  - [ ] `src/transformacion.py`
  - [ ] `src/carga.py`
  - [ ] `dags/dag_etl_simple.py`
- [ ] Ejecutar tests: `pytest tests/`
- [ ] Verificar cobertura: `pytest --cov` (>80%)

**Día 6: QA**
- [ ] Invocar `@quality` para quality check
  - [ ] `black .`
  - [ ] `flake8 .`
  - [ ] `pytest tests/ -v`
  - [ ] Verificar cobertura >80%
- [ ] Ejecutar DAG en Airflow local
- [ ] Crear README.md del proyecto

### Fase 2: Tema 2 - Intermedio (6.5 días)

**Repite proceso similar:**
- [ ] Día 1-2: 01-TEORIA, 02-EJEMPLOS, 03-EJERCICIOS
- [ ] Día 3: Validación pedagógica
- [ ] Día 4: Diseño + Tests (30-35 tests)
- [ ] Día 5-6: Implementación (Pipeline complejo)
- [ ] Día 7: QA

### Fase 3: Tema 3 - Producción (6.5 días)

**Repite proceso similar:**
- [ ] Día 1-2: 01-TEORIA, 02-EJEMPLOS (4), 03-EJERCICIOS (12)
- [ ] Día 3: Validación pedagógica
- [ ] Día 4-5: Diseño + Tests (35-40 tests)
- [ ] Día 6: Implementación (Pipeline productivo)
- [ ] Día 7: QA (cobertura >85%)

### Fase 4: Documentación y Cierre (1.5 días)

- [ ] Crear `modulo-06-airflow/README.md`
- [ ] Actualizar `documentacion/CHANGELOG.md`:
  ```markdown
  ### Added
  - **JAR-192: Módulo 6 - Apache Airflow y Orquestación ✅ COMPLETADO** (2025-XX-XX):
    - Tema 1: Introducción (100%)
    - Tema 2: Intermedio (100%)
    - Tema 3: Producción (100%)
    - Tests totales: XX (100% pasando)
    - Cobertura: XX%
  ```
- [ ] Actualizar `README.md` raíz: Módulo 6: 100%
- [ ] Ejecutar quality check global:
  ```bash
  cd modulo-06-airflow
  black .
  flake8 .
  pytest --cov --cov-report=html
  ```
- [ ] Comentar en Linear:
  ```markdown
  ✅ JAR-192 COMPLETADO
  - 3 temas completados (100%)
  - XX tests (100% pasando)
  - Cobertura: XX% (>80%)
  - Calificación pedagógica: X.X/10
  - CHANGELOG actualizado
  - README actualizado
  ```
- [ ] Mover JAR-192 a "Done" en Linear
- [ ] Celebrar 🎉

---

## 📊 Métricas de Éxito

### Objetivo: Igualar o Superar el Módulo 4 (9.3/10)

| Métrica                      | Objetivo | Módulo 4 (Referencia) | Cómo Medir                      |
| ---------------------------- | -------- | --------------------- | ------------------------------- |
| **Calificación pedagógica**  | >9.0/10  | 9.3/10 ⭐⭐⭐⭐⭐          | Validación psicólogo + feedback |
| **Tests totales**            | >90      | 210                   | `pytest --collect-only`         |
| **Tests pasando**            | 100%     | 100%                  | `pytest -v`                     |
| **Cobertura promedio**       | >80%     | 93%                   | `pytest --cov`                  |
| **Cobertura Tema 3**         | >85%     | -                     | `pytest --cov` tema-3           |
| **Palabras de teoría**       | >12,000  | ~12,000               | `wc -w` en 01-TEORIA.md         |
| **Ejemplos ejecutables**     | >12      | 14                    | Contar en 02-EJEMPLOS.md        |
| **Ejercicios totales**       | >40      | 42                    | Contar en 03-EJERCICIOS.md      |
| **Funciones con type hints** | 100%     | 100%                  | Code review + mypy              |
| **Funciones con docstrings** | 100%     | 100%                  | Code review                     |
| **Proyectos prácticos**      | 3/3      | 3/3                   | Verificar TDD                   |
| **DAGs ejecutables**         | 100%     | -                     | Ejecutar en Airflow             |

### Métricas de Proceso

| Métrica                   | Objetivo    | Cómo Medir                |
| ------------------------- | ----------- | ------------------------- |
| **Duración total**        | 3-4 semanas | Fecha inicio → fecha fin  |
| **Bloqueadores críticos** | 0           | Tracking en Linear        |
| **Re-work necesario**     | <10%        | Commits después de QA     |
| **Feedback de revisores** | Positivo    | Comentarios en Linear     |
| **Errores en producción** | 0           | Issues reportadas después |

---

## 🚦 Bloqueadores Potenciales y Mitigaciones

### 🔴 Críticos (Alta probabilidad, alto impacto)

#### 1. Dependencias Incompletas (Módulos 2, 3, 5)
- **Probabilidad:** 100% (actualmente incompletos)
- **Impacto:** Alto - Estudiantes sin bases sólidas
- **Mitigación:**
  - **Opción A:** Completar JAR-188, JAR-189, JAR-191 primero (recomendada)
  - **Opción B:** Hacer Tema 1 ultra-didáctico, con remedial teaching
- **Plan B:** Proveer links a recursos externos (tutoriales Python/SQL)

#### 2. Docker Compose No Funcional
- **Probabilidad:** Media (20%)
- **Impacto:** Crítico - Sin Airflow, no hay módulo
- **Mitigación:**
  - Validar Docker **antes** de iniciar
  - Troubleshooting guide en README
  - Scripts de diagnóstico (`docker-compose ps`, `docker-compose logs`)
- **Plan B:** Proveer instalación alternativa (pip install apache-airflow)

### 🟡 Medios (Media probabilidad, medio impacto)

#### 3. Testing de DAGs Complejo
- **Probabilidad:** Media (40%)
- **Impacto:** Medio - Proyectos sin tests adecuados
- **Mitigación:**
  - Proveer utilidades de testing (`tests/utils/airflow_helpers.py`)
  - Fixtures reusables en `conftest.py`
  - Ejemplos de tests en 02-EJEMPLOS.md
- **Plan B:** Reducir requisitos de cobertura a 75% para Tema 1

#### 4. Airflow Complejo para Principiantes
- **Probabilidad:** Alta (60%)
- **Impacto:** Medio - Frustración, baja completitud
- **Mitigación:**
  - Analogías poderosas (orquesta, receta)
  - Ejemplos ultra-simples en Tema 1
  - Progresión gradual
  - Videos tutoriales (opcional)
- **Plan B:** Añadir sección "Conceptos Básicos de Python" en apéndice

#### 5. Tiempo de Ejecución de DAGs Lento
- **Probabilidad:** Media (30%)
- **Impacto:** Bajo - Desarrollo lento
- **Mitigación:**
  - `schedule_interval=None` para desarrollo
  - DAGs pequeños (< 10 tasks)
  - Explicar que en producción es normal esperar
- **Plan B:** No es crítico, parte del aprendizaje

### 🟢 Bajos (Baja probabilidad, bajo impacto)

#### 6. Estimación de Tiempo Incorrecta
- **Probabilidad:** Media (40%)
- **Impacto:** Bajo - Retraso de 1-2 días
- **Mitigación:**
  - Buffer de 20% ya incluido en estimaciones
  - Tracking diario de progreso
- **Plan B:** Extender deadline si es necesario

#### 7. Feedback Negativo de Revisores
- **Probabilidad:** Baja (15%)
- **Impacto:** Medio - Re-work necesario
- **Mitigación:**
  - Validación pedagógica temprana (después de cada tema)
  - Iterar rápido según feedback
- **Plan B:** Ajustar contenido y re-revisar

---

## 📋 Checklist de Calidad Final

### Antes de Marcar como "Done"

#### ✅ Contenido
- [ ] 3 temas completados (TEORIA + EJEMPLOS + EJERCICIOS)
- [ ] ~15,000 palabras de teoría total
- [ ] 14 ejemplos ejecutables (todos funcionan)
- [ ] 42 ejercicios con soluciones completas
- [ ] Progresión pedagógica validada

#### ✅ Proyectos Prácticos
- [ ] 3 proyectos implementados con TDD
- [ ] 90-105 tests totales
- [ ] 100% tests pasando
- [ ] Cobertura >80% (global)
- [ ] Cobertura >85% (Tema 3)
- [ ] Todos los DAGs ejecutables en Airflow

#### ✅ Calidad de Código
- [ ] `black .` sin errores
- [ ] `flake8 .` sin errores
- [ ] `pytest -v` 100% pasando
- [ ] Type hints en todas las funciones
- [ ] Docstrings en todas las funciones
- [ ] Imports ordenados (estándar → externo → interno)

#### ✅ Documentación
- [ ] `modulo-06-airflow/README.md` completo
- [ ] 3 READMEs de proyectos (instalación, uso, troubleshooting)
- [ ] `documentacion/CHANGELOG.md` actualizado con JAR-192
- [ ] `README.md` raíz actualizado (Módulo 6: 100%)
- [ ] Docstrings en DAGs (`doc_md`)

#### ✅ Validación
- [ ] Calificación pedagógica >9.0/10
- [ ] Feedback de 2+ revisores
- [ ] Tests ejecutados en ambiente limpio
- [ ] Docker Compose funcional
- [ ] DAGs ejecutables sin errores

#### ✅ Linear
- [ ] Comentario final en JAR-192 con métricas
- [ ] Mover a "Done"
- [ ] Verificar que JAR-193 (Módulo 7) puede iniciarse

---

## 🎓 Lecciones del Módulo 4 (Aplicables aquí)

### ✅ Qué Funcionó Bien en el Módulo 4

1. **TDD estricto:** Tests primero, código después
   - **Aplicar:** Mantener metodología TDD en todos los proyectos

2. **Progresión gradual:** Básico → Intermedio → Avanzado
   - **Aplicar:** Tema 1 ultra-simple, aumentar complejidad gradualmente

3. **Ejemplos ejecutables:** Código real que funciona
   - **Aplicar:** Todos los ejemplos deben ejecutarse sin errores

4. **Cobertura alta:** 93% promedio
   - **Aplicar:** Objetivo >80%, con >85% en Tema 3

5. **Validación pedagógica:** 9.3/10 por feedback riguroso
   - **Aplicar:** Validación después de cada tema, no al final

6. **Documentación completa:** READMEs detallados
   - **Aplicar:** README de proyecto con troubleshooting

### ⚠️ Qué Mejorar del Módulo 4

1. **Algunos ejercicios sin solución completa:**
   - **Mejorar:** Asegurar 100% de ejercicios con solución

2. **Ejemplos muy avanzados al inicio:**
   - **Mejorar:** Tema 1 debe ser ultra-básico, sin asumir conocimientos

3. **Poca mención de seguridad:**
   - **Mejorar:** Incluir secciones de seguridad (Variables seguras, Connections, no hardcodear credenciales)

---

## 📝 Notas Finales

### Comunicación con el Usuario

**Opción A elegida:** Mantener en Linear comentario recomendando esperar hasta completar dependencias.

**Opción B elegida:** Mover a "In Progress" y comunicar inicio con advertencia de dependencias.

### Próximos Pasos Inmediatos

1. **Esperar decisión del usuario:** ¿Opción A (esperar) u Opción B (implementar ahora)?
2. **Si Opción A:** Priorizar JAR-188, JAR-189, JAR-191
3. **Si Opción B:** Validar Docker y empezar con Tema 1

---

**Documento creado:** 2025-10-25
**Última actualización:** 2025-10-25
**Autor:** @project-management
**Estado:** ✅ Planificación completada - Esperando decisión

---

## 🔗 Referencias

- **Issue en Linear:** https://linear.app/jarko/issue/JAR-192/modulo-6-apache-airflow-y-orquestacion
- **ORDEN_DE_IMPLEMENTACION.md:** Sección JAR-192 (líneas 121-125)
- **Docker Compose:** `docker-compose.yml` (líneas 89-170)
- **Módulo 4 como referencia:** Calificación 9.3/10, 210 tests, 93% cobertura
- **Airflow Documentation:** https://airflow.apache.org/docs/
- **Testing Airflow DAGs:** https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

---

**FIN DEL DOCUMENTO DE PLANIFICACIÓN**
