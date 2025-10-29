# 📚 Tema 2: Airflow Intermedio - Teoría

**Módulo 6: Apache Airflow y Orquestación**
**Nivel:** Intermedio
**Duración estimada:** 6-8 horas
**Prerequisitos:** Tema 1 completado

---

## 📖 Índice

1. [Introducción al Tema 2](#1-introducción-al-tema-2)
2. [TaskGroups: Organización Visual de DAGs](#2-taskgroups-organización-visual-de-dags)
3. [SubDAGs: Contexto Histórico](#3-subdags-contexto-histórico)
4. [XComs: Comunicación entre Tasks](#4-xcoms-comunicación-entre-tasks)
5. [Branching: Condicionales en DAGs](#5-branching-condicionales-en-dags)
6. [Sensors: Esperar por Condiciones](#6-sensors-esperar-por-condiciones)
7. [Dynamic DAG Generation](#7-dynamic-dag-generation)
8. [Templating con Jinja2](#8-templating-con-jinja2)
9. [Mejores Prácticas del Tema 2](#9-mejores-prácticas-del-tema-2)
10. [Resumen y Próximos Pasos](#10-resumen-y-próximos-pasos)

---

## 1. Introducción al Tema 2

### 📌 ¿Qué aprendiste en el Tema 1?

En el Tema 1 aprendiste los **conceptos fundamentales** de Apache Airflow:

- ✅ **DAGs:** Flujos de trabajo dirigidos y acíclicos
- ✅ **Tasks:** Unidades individuales de trabajo
- ✅ **Operators:** PythonOperator, BashOperator, DummyOperator
- ✅ **Dependencias:** Usar `>>` para definir el orden de ejecución
- ✅ **Scheduling:** Ejecutar DAGs periódicamente con cron
- ✅ **Webserver UI:** Monitorear y ejecutar DAGs visualmente

Estos conceptos te permiten crear **pipelines simples** que extraen, transforman y cargan datos.

---

### 🚀 ¿Por qué necesitamos conceptos intermedios?

A medida que tus pipelines **crecen en complejidad**, te encontrarás con nuevos desafíos:

**Problema 1: DAGs Ilegibles**
```
inicio → tarea1 → tarea2 → tarea3 → tarea4 → tarea5 → tarea6 → tarea7 → fin
```
Cuando tienes **20+ tasks**, el DAG se vuelve **imposible de leer** en el Graph View de Airflow.

**Problema 2: Tasks Aisladas**
```python
# Task 1 calcula total_ventas
def calcular_ventas():
    return 50000  # ¿Cómo paso este valor a otra task?

# Task 2 necesita el total_ventas de Task 1
def generar_reporte():
    total = ???  # ¿Cómo lo obtengo?
```
Las tasks están **aisladas**, no pueden compartir datos fácilmente.

**Problema 3: Falta de Condicionales**
```python
# ¿Cómo hago if-else en un DAG?
if ventas > 10000:
    procesar_premium()
else:
    procesar_normal()
```
Los DAGs básicos no tienen **flujo condicional** (if-else).

**Problema 4: Esperas Activas**
```python
# ¿Cómo espero hasta que llegue un archivo?
while not archivo_existe("datos.csv"):
    time.sleep(60)  # ❌ Bloquea el worker
```
Necesitas **esperar por condiciones** sin bloquear recursos.

---

### 🎯 ¿Qué aprenderás en este tema?

En este tema aprenderás **conceptos intermedios** que resuelven estos problemas:

| Concepto         | Problema que Resuelve                  |
| ---------------- | -------------------------------------- |
| **TaskGroups**   | DAGs con 20+ tasks ilegibles           |
| **XComs**        | Tasks que necesitan compartir datos    |
| **Branching**    | Flujos condicionales (if-else)         |
| **Sensors**      | Esperar por archivos, APIs, horarios   |
| **Dynamic DAGs** | Crear tasks automáticamente en bucles  |
| **Templating**   | Variables dinámicas en configuraciones |

Al finalizar, podrás construir **pipelines complejos, legibles y mantenibles** que manejan flujos condicionales, esperan por recursos externos y procesan datos de forma dinámica.

---

## 2. TaskGroups: Organización Visual de DAGs

### 🎯 El Problema: DAGs Ilegibles

Imagina que tienes un pipeline ETL con estas tasks:

```python
inicio >> extraer_ventas >> validar_ventas >> transformar_ventas >> calcular_metricas_ventas >>
extraer_clientes >> validar_clientes >> transformar_clientes >> calcular_metricas_clientes >>
combinar_datos >> generar_reporte >> enviar_email >> fin
```

En el **Graph View** de Airflow, verías **12 tasks en una sola línea horizontal**. Es difícil entender:
- ¿Qué tasks están relacionadas?
- ¿Dónde empieza y termina el procesamiento de ventas?
- ¿Qué hace cada sección del pipeline?

---

### 💡 La Solución: TaskGroups

Los **TaskGroups** te permiten **agrupar tasks relacionadas** en un contenedor visual.

**Analogía:** Es como organizar archivos en carpetas

Imagina que tienes estos archivos en tu escritorio:
```
factura_enero.pdf
factura_febrero.pdf
factura_marzo.pdf
foto_vacaciones.jpg
foto_cumpleaños.jpg
```

Los organizarías en carpetas:
```
📁 Facturas/
  - factura_enero.pdf
  - factura_febrero.pdf
  - factura_marzo.pdf
📁 Fotos/
  - foto_vacaciones.jpg
  - foto_cumpleaños.jpg
```

Los **TaskGroups** hacen lo mismo con tasks de Airflow.

---

### 📝 Sintaxis de TaskGroups

```python
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG

with DAG("dag_con_taskgroups", start_date=datetime(2025, 1, 1), schedule=None) as dag:

    inicio = DummyOperator(task_id="inicio")

    # TaskGroup para procesar ventas
    with TaskGroup("procesar_ventas") as grupo_ventas:
        extraer = PythonOperator(task_id="extraer", python_callable=lambda: print("Extrayendo ventas"))
        validar = PythonOperator(task_id="validar", python_callable=lambda: print("Validando ventas"))
        transformar = PythonOperator(task_id="transformar", python_callable=lambda: print("Transformando ventas"))

        extraer >> validar >> transformar

    # TaskGroup para procesar clientes
    with TaskGroup("procesar_clientes") as grupo_clientes:
        extraer = PythonOperator(task_id="extraer", python_callable=lambda: print("Extrayendo clientes"))
        validar = PythonOperator(task_id="validar", python_callable=lambda: print("Validando clientes"))
        transformar = PythonOperator(task_id="transformar", python_callable=lambda: print("Transformando clientes"))

        extraer >> validar >> transformar

    fin = DummyOperator(task_id="fin")

    # Dependencias entre grupos
    inicio >> [grupo_ventas, grupo_clientes] >> fin
```

---

### 🔍 Cómo se ve en Airflow UI

**Sin TaskGroups:**
```
inicio → extraer_ventas → validar_ventas → transformar_ventas → extraer_clientes → validar_clientes → transformar_clientes → fin
```
(12 tasks visibles, difícil de leer)

**Con TaskGroups:**
```
inicio → [📁 procesar_ventas] → fin
         [📁 procesar_clientes]
```
(2 grupos + 2 tasks, mucho más legible)

Cuando haces clic en `📁 procesar_ventas`, se **expande** y muestra:
```
procesar_ventas.extraer → procesar_ventas.validar → procesar_ventas.transformar
```

---

### ✅ Ventajas de TaskGroups

| Ventaja          | Descripción                                                                         |
| ---------------- | ----------------------------------------------------------------------------------- |
| **Legibilidad**  | DAGs más fáciles de entender visualmente                                            |
| **Organización** | Agrupar tasks por funcionalidad (ETL, notificaciones, validaciones)                 |
| **Reusabilidad** | Puedes definir TaskGroups como funciones y reutilizarlos                            |
| **Namespace**    | Tasks dentro del grupo tienen prefijo `grupo.task_id` (evita colisiones de nombres) |

---

### 📦 TaskGroups Anidados

Puedes crear **TaskGroups dentro de TaskGroups** (como carpetas dentro de carpetas):

```python
with TaskGroup("etl") as grupo_etl:

    with TaskGroup("extraccion") as grupo_extraccion:
        extraer_ventas = PythonOperator(...)
        extraer_clientes = PythonOperator(...)

    with TaskGroup("transformacion") as grupo_transformacion:
        transformar_ventas = PythonOperator(...)
        transformar_clientes = PythonOperator(...)

    with TaskGroup("carga") as grupo_carga:
        cargar_bd = PythonOperator(...)
        cargar_s3 = PythonOperator(...)

    grupo_extraccion >> grupo_transformacion >> grupo_carga
```

**Estructura visual:**
```
📁 etl/
  ├── 📁 extraccion/
  │   ├── extraer_ventas
  │   └── extraer_clientes
  ├── 📁 transformacion/
  │   ├── transformar_ventas
  │   └── transformar_clientes
  └── 📁 carga/
      ├── cargar_bd
      └── cargar_s3
```

---

### 🎨 Casos de Uso Reales

**1. ETL Multi-Fuente**
```python
with TaskGroup("etl_fuente1") as etl_1:
    # Extraer, transformar, validar fuente 1

with TaskGroup("etl_fuente2") as etl_2:
    # Extraer, transformar, validar fuente 2

with TaskGroup("consolidar") as consolidar:
    # Combinar ambas fuentes
```

**2. Notificaciones**
```python
with TaskGroup("notificaciones") as notif:
    enviar_email = EmailOperator(...)
    enviar_slack = SlackOperator(...)
    actualizar_dashboard = PythonOperator(...)
```

**3. Validaciones**
```python
with TaskGroup("validaciones") as validar:
    validar_schema = PythonOperator(...)
    validar_duplicados = PythonOperator(...)
    validar_nulos = PythonOperator(...)
```

---

## 3. SubDAGs: Contexto Histórico

### 📜 ¿Qué eran los SubDAGs?

Antes de Airflow 2.0, existían los **SubDAGs** para agrupar tasks. Funcionaban como **DAGs dentro de DAGs**.

```python
from airflow.operators.subdag import SubDagOperator

def crear_subdag(dag_parent, subdag_name, default_args):
    subdag = DAG(
        f"{dag_parent}.{subdag_name}",
        default_args=default_args,
        schedule_interval=None
    )
    # Agregar tasks al subdag...
    return subdag

# Uso en el DAG principal
subdag_task = SubDagOperator(
    task_id="mi_subdag",
    subdag=crear_subdag("dag_principal", "mi_subdag", default_args),
    dag=dag
)
```

---

### ❌ ¿Por qué se deprecaron?

Los SubDAGs tenían **problemas graves**:

**Problema 1: Deadlocks del Scheduler**
- Los SubDAGs corrían en el mismo worker que el DAG padre
- Si el worker estaba lleno, el SubDAG no podía ejecutarse
- Esto causaba **bloqueos** (deadlocks)

**Problema 2: Complejidad Innecesaria**
- Requerían crear un DAG completo separado
- Difíciles de debuggear
- Logs separados del DAG principal

**Problema 3: Performance**
- El scheduler tenía que parsear múltiples DAGs
- Aumentaba el tiempo de procesamiento

---

### ✅ Alternativa Moderna: TaskGroups

**TaskGroups** reemplazan completamente a SubDAGs y resuelven todos sus problemas:

| Aspecto         | SubDAGs (deprecado)           | TaskGroups (actual)    |
| --------------- | ----------------------------- | ---------------------- |
| **Performance** | Lento (parsea múltiples DAGs) | Rápido (un solo DAG)   |
| **Deadlocks**   | Sí (worker pool compartido)   | No (tasks regulares)   |
| **Logs**        | Separados                     | Integrados             |
| **Complejidad** | Alta (DAG completo)           | Baja (context manager) |
| **UI**          | Confusa                       | Clara y colapsable     |

---

### 🔄 Migrar de SubDAGs a TaskGroups

**Antes (SubDAG):**
```python
def crear_subdag(dag_parent, subdag_name, default_args):
    subdag = DAG(f"{dag_parent}.{subdag_name}", default_args=default_args)
    task1 = PythonOperator(task_id="task1", python_callable=func1, dag=subdag)
    task2 = PythonOperator(task_id="task2", python_callable=func2, dag=subdag)
    task1 >> task2
    return subdag

subdag_operator = SubDagOperator(task_id="subdag", subdag=crear_subdag(...))
```

**Después (TaskGroup):**
```python
with TaskGroup("grupo") as grupo:
    task1 = PythonOperator(task_id="task1", python_callable=func1)
    task2 = PythonOperator(task_id="task2", python_callable=func2)
    task1 >> task2
```

**¡Mucho más simple!** ✨

---

### 📝 ¿Cuándo encontrarás SubDAGs?

Si trabajas con **código legacy** (código viejo) de Airflow 1.x, podrías encontrar SubDAGs. En ese caso:

1. **Identificar:** Busca `SubDagOperator` en el código
2. **Entender:** Lee qué hace el SubDAG
3. **Migrar:** Reescribir como TaskGroup
4. **Testear:** Verificar que funciona igual
5. **Eliminar:** Borrar el código viejo

**Regla de oro:** En código nuevo, **siempre usa TaskGroups**, nunca SubDAGs.

---

## 4. XComs: Comunicación entre Tasks

### 🎯 El Problema: Tasks Aisladas

Por defecto, las tasks en Airflow están **completamente aisladas**. Cada task se ejecuta en su propio proceso (o incluso en diferentes máquinas en producción).

```python
def calcular_total_ventas():
    total = 50000
    print(f"Total de ventas: {total}")
    return total  # ¿Cómo accede la siguiente task a este valor?

def generar_reporte():
    total = ???  # ❌ No tengo acceso al resultado de la task anterior
    print(f"Reporte generado con total: {total}")

task1 = PythonOperator(task_id="calcular", python_callable=calcular_total_ventas)
task2 = PythonOperator(task_id="reportar", python_callable=generar_reporte)

task1 >> task2
```

---

### 💡 La Solución: XComs (Cross-Communication)

**XComs** (Cross-Communications) es un mecanismo de Airflow para que las tasks **compartan pequeñas cantidades de datos**.

**Analogía:** XComs son como Post-It notes en una oficina

Imagina que trabajas en una oficina:
- **Task 1 (Ana):** Calcula el total de ventas y escribe "50,000€" en un Post-It
- **Post-It:** Ana pega el Post-It en una pizarra compartida con la etiqueta "total_ventas"
- **Task 2 (Carlos):** Lee el Post-It de la pizarra y usa ese valor para generar un reporte

XComs funciona igual: una task "pega" un dato, otra task "lee" ese dato.

---

### 📝 API de XComs

**Método 1: Return Automático**

Si una función **retorna un valor**, Airflow automáticamente lo guarda en XCom con la key `return_value`:

```python
def calcular_total_ventas():
    total = 50000
    return total  # ✅ Airflow guarda esto en XCom automáticamente

task1 = PythonOperator(task_id="calcular", python_callable=calcular_total_ventas)
```

**Método 2: xcom_push (Manual)**

Puedes guardar **múltiples valores** con keys específicas:

```python
def calcular_metricas(**context):
    ti = context["ti"]  # TaskInstance

    total = 50000
    promedio = 1250
    num_ventas = 40

    ti.xcom_push(key="total", value=total)
    ti.xcom_push(key="promedio", value=promedio)
    ti.xcom_push(key="num_ventas", value=num_ventas)

task1 = PythonOperator(task_id="calcular", python_callable=calcular_metricas)
```

---

**Método 3: xcom_pull (Leer)**

Para **leer** un XCom de otra task:

```python
def generar_reporte(**context):
    ti = context["ti"]

    # Leer el return_value de la task "calcular"
    total = ti.xcom_pull(task_ids="calcular", key="return_value")

    # O leer keys específicas
    promedio = ti.xcom_pull(task_ids="calcular", key="promedio")
    num_ventas = ti.xcom_pull(task_ids="calcular", key="num_ventas")

    print(f"Reporte: Total={total}, Promedio={promedio}, Cantidad={num_ventas}")

task2 = PythonOperator(task_id="reportar", python_callable=generar_reporte)
```

---

### 🔍 Ejemplo Completo

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def calcular_ventas(**context):
    """Simula cálculo de ventas y retorna el total"""
    import random
    total = random.randint(10000, 100000)
    print(f"[CALCULAR] Total de ventas: {total}")
    return total  # Se guarda en XCom con key "return_value"

def verificar_umbral(**context):
    """Lee el total de XCom y decide si supera el umbral"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="calcular_ventas", key="return_value")

    umbral = 50000
    if total > umbral:
        print(f"[VERIFICAR] ✅ Total {total} supera umbral {umbral}")
    else:
        print(f"[VERIFICAR] ❌ Total {total} NO supera umbral {umbral}")

    # Guardar resultado de la verificación
    ti.xcom_push(key="supera_umbral", value=total > umbral)

def enviar_notificacion(**context):
    """Lee el resultado de verificación y envía notificación"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="calcular_ventas", key="return_value")
    supera = ti.xcom_pull(task_ids="verificar_umbral", key="supera_umbral")

    if supera:
        print(f"[NOTIFICAR] 📧 Enviando alerta: Ventas de {total} superaron el umbral!")
    else:
        print(f"[NOTIFICAR] 📝 Log normal: Ventas de {total}")

with DAG("ejemplo_xcoms", start_date=datetime(2025, 1, 1), schedule=None) as dag:

    task_calcular = PythonOperator(
        task_id="calcular_ventas",
        python_callable=calcular_ventas
    )

    task_verificar = PythonOperator(
        task_id="verificar_umbral",
        python_callable=verificar_umbral
    )

    task_notificar = PythonOperator(
        task_id="enviar_notificacion",
        python_callable=enviar_notificacion
    )

    task_calcular >> task_verificar >> task_notificar
```

---

### ⚠️ Limitaciones de XComs

**Limitación 1: Tamaño Máximo**

XComs están pensados para **datos pequeños** (metadatos, IDs, contadores).

| Executor           | Tamaño Máximo (aprox)             |
| ------------------ | --------------------------------- |
| LocalExecutor      | 48 KB                             |
| CeleryExecutor     | 64 KB (depende de Redis/RabbitMQ) |
| KubernetesExecutor | Variable (depende del backend)    |

**❌ NO uses XComs para:**
- DataFrames completos (usa archivos temporales o una base de datos)
- Imágenes o archivos binarios grandes
- Listas con miles de elementos

**✅ SÍ usa XComs para:**
- IDs de registros procesados
- Contadores (número de filas, errores, éxitos)
- Paths a archivos
- Flags booleanos (True/False)
- Configuraciones pequeñas

---

**Limitación 2: Serialización**

XComs solo pueden guardar datos **serializables en JSON**:

**✅ Funciona:**
```python
ti.xcom_push(key="data", value={"total": 50000, "ventas": 40})  # Diccionario
ti.xcom_push(key="lista", value=[1, 2, 3, 4, 5])  # Lista
ti.xcom_push(key="numero", value=42)  # Número
ti.xcom_push(key="texto", value="Hola")  # String
ti.xcom_push(key="booleano", value=True)  # Boolean
```

**❌ NO funciona:**
```python
import pandas as pd
df = pd.DataFrame({"col": [1, 2, 3]})
ti.xcom_push(key="df", value=df)  # ❌ Error: DataFrame no es serializable
```

---

**Limitación 3: Performance**

Cada `xcom_pull` hace una **consulta a la base de datos** de Airflow. Si haces muchas lecturas, puede ser lento.

**❌ Malo (muchas consultas):**
```python
for i in range(100):
    valor = ti.xcom_pull(task_ids=f"task_{i}", key="resultado")
```

**✅ Bueno (una consulta):**
```python
# Leer múltiples task_ids a la vez
valores = ti.xcom_pull(task_ids=["task_1", "task_2", "task_3"], key="resultado")
```

---

### 🔄 Alternativas para Datos Grandes

Si necesitas compartir **datos grandes** entre tasks:

**Alternativa 1: Archivos Temporales**
```python
import pandas as pd
from pathlib import Path

def task_1():
    df = pd.DataFrame({"col": range(10000)})
    ruta = "/tmp/datos.csv"
    df.to_csv(ruta, index=False)
    return ruta  # Compartir solo la ruta (pequeño)

def task_2(**context):
    ti = context["ti"]
    ruta = ti.xcom_pull(task_ids="task_1")
    df = pd.read_csv(ruta)  # Leer desde el archivo
    print(f"DataFrame con {len(df)} filas")
```

**Alternativa 2: Base de Datos Intermedia**
```python
def task_1():
    df = pd.DataFrame(...)
    # Guardar en PostgreSQL o similar
    df.to_sql("tabla_temp", con=engine)
    return "tabla_temp"  # Compartir solo el nombre

def task_2(**context):
    ti = context["ti"]
    tabla = ti.xcom_pull(task_ids="task_1")
    df = pd.read_sql(f"SELECT * FROM {tabla}", con=engine)
```

**Alternativa 3: S3/GCS**
```python
def task_1():
    df = pd.DataFrame(...)
    ruta_s3 = "s3://mi-bucket/temp/datos.parquet"
    df.to_parquet(ruta_s3)
    return ruta_s3  # Compartir solo la ruta
```

---

### ✅ Mejores Prácticas con XComs

1. **Usa return para casos simples:** Si solo necesitas pasar un valor, usa `return`
2. **Usa keys descriptivas:** En lugar de "dato1", "dato2", usa "total_ventas", "num_errores"
3. **Documenta qué se comparte:** Comenta qué XComs produce cada task
4. **Validar antes de pull:** Verifica que el XCom existe y es del tipo esperado
5. **No abuses:** Si necesitas compartir muchos datos, usa alternativas (archivos, BD)

---

## 5. Branching: Condicionales en DAGs

### 🎯 El Problema: Falta de Flujo Condicional

Los DAGs que has visto hasta ahora son **lineales** o **paralelos**, pero **no tienen condicionales**:

```python
# Lineal
A >> B >> C >> D

# Paralelo
A >> [B, C, D] >> E
```

¿Qué pasa si quieres ejecutar **diferentes tasks según una condición**?

**Ejemplo del mundo real:**

```
Si ventas_totales > 10,000€:
    → Enviar alerta al gerente
    → Procesar con prioridad alta
Sino:
    → Guardar en log normal
    → Procesar con prioridad baja
```

---

### 💡 La Solución: BranchPythonOperator

El **BranchPythonOperator** te permite crear **flujos condicionales** (if-else) en tus DAGs.

**Analogía:** Es como un semáforo en una carretera

Imagina una carretera que se divide en dos:
- Si el semáforo está en verde a la izquierda → tomas el camino izquierdo
- Si el semáforo está en verde a la derecha → tomas el camino derecho

El **BranchPythonOperator** es ese semáforo: decide qué camino tomar según una condición.

---

### 📝 Sintaxis de BranchPythonOperator

```python
from airflow.operators.python import BranchPythonOperator

def decidir_camino(**context):
    """Función que decide qué task ejecutar a continuación"""
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="calcular_ventas")

    if ventas > 10000:
        return "procesar_premium"  # Task ID a ejecutar
    else:
        return "procesar_normal"  # Task ID a ejecutar

branch_task = BranchPythonOperator(
    task_id="decidir",
    python_callable=decidir_camino
)
```

**Reglas importantes:**
1. La función **debe retornar un task_id** (string) o una lista de task_ids
2. Solo las tasks retornadas se ejecutarán
3. Las demás tasks se **saltarán** (estado: "skipped")

---

### 🔍 Ejemplo Completo

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

def calcular_ventas():
    """Simula cálculo de ventas"""
    import random
    return random.randint(5000, 15000)

def decidir_procesamiento(**context):
    """Decide si procesar como premium o normal"""
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="calcular_ventas")

    print(f"[BRANCH] Ventas: {ventas}")

    if ventas > 10000:
        print("[BRANCH] → Ruta PREMIUM")
        return "procesar_premium"
    else:
        print("[BRANCH] → Ruta NORMAL")
        return "procesar_normal"

def procesar_premium(**context):
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="calcular_ventas")
    print(f"[PREMIUM] ⭐ Procesando {ventas}€ con prioridad ALTA")

def procesar_normal(**context):
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="calcular_ventas")
    print(f"[NORMAL] 📋 Procesando {ventas}€ con prioridad BAJA")

with DAG("ejemplo_branching", start_date=datetime(2025, 1, 1), schedule=None) as dag:

    inicio = DummyOperator(task_id="inicio")

    calcular = PythonOperator(
        task_id="calcular_ventas",
        python_callable=calcular_ventas
    )

    branch = BranchPythonOperator(
        task_id="decidir_procesamiento",
        python_callable=decidir_procesamiento
    )

    premium = PythonOperator(
        task_id="procesar_premium",
        python_callable=procesar_premium
    )

    normal = PythonOperator(
        task_id="procesar_normal",
        python_callable=procesar_normal
    )

    fin = DummyOperator(
        task_id="fin",
        trigger_rule="none_failed_min_one_success"  # ← Importante!
    )

    inicio >> calcular >> branch >> [premium, normal] >> fin
```

---

### 🔍 Flujo Visual

```
inicio → calcular_ventas → decidir_procesamiento
                                    ├──→ (ventas > 10000) procesar_premium → fin
                                    └──→ (ventas ≤ 10000) procesar_normal → fin
```

**¿Qué pasa en ejecución?**

Si ventas = 12,000:
- ✅ inicio: success
- ✅ calcular_ventas: success (retorna 12,000)
- ✅ decidir_procesamiento: success (retorna "procesar_premium")
- ✅ procesar_premium: success
- ⏭️ procesar_normal: **skipped** (no se ejecutó)
- ✅ fin: success

---

### ⚙️ Trigger Rules: Manejar Tasks Saltadas

Por defecto, una task solo se ejecuta si **todas** sus upstream tasks tienen éxito. Pero con branching, algunas tasks se **saltan**.

**Problema:**
```python
inicio >> branch >> [task_a, task_b] >> fin
```

Si `branch` retorna solo `task_a`:
- ✅ task_a: success
- ⏭️ task_b: skipped
- ❓ fin: ¿Se ejecuta o no?

**Solución:** Usar **trigger_rule** en la task `fin`:

```python
fin = DummyOperator(
    task_id="fin",
    trigger_rule="none_failed_min_one_success"
)
```

---

**Trigger Rules Comunes:**

| Trigger Rule                  | Se ejecuta si...                                                        |
| ----------------------------- | ----------------------------------------------------------------------- |
| `all_success`                 | **Todas** las upstream tasks fueron exitosas (default)                  |
| `all_failed`                  | **Todas** las upstream tasks fallaron                                   |
| `all_done`                    | **Todas** las upstream tasks terminaron (sin importar el estado)        |
| `one_success`                 | **Al menos una** upstream task fue exitosa                              |
| `one_failed`                  | **Al menos una** upstream task falló                                    |
| `none_failed`                 | **Ninguna** upstream task falló (incluye skipped)                       |
| `none_failed_min_one_success` | **Al menos una** exitosa y **ninguna** fallida (✅ ideal para branching) |
| `none_skipped`                | **Ninguna** upstream task fue saltada                                   |
| `always`                      | **Siempre** se ejecuta (sin importar nada)                              |

---

### 🔀 Branching con Múltiples Caminos

Puedes retornar **varios task_ids** para ejecutar múltiples tasks:

```python
def decidir_multiple(**context):
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="calcular_ventas")

    if ventas > 50000:
        return ["enviar_email_gerente", "enviar_slack_ceo", "actualizar_dashboard"]
    elif ventas > 10000:
        return ["enviar_email_equipo"]
    else:
        return ["guardar_log"]

branch = BranchPythonOperator(task_id="decidir", python_callable=decidir_multiple)
```

**Flujo:**
```
decidir
  ├──→ (ventas > 50000) [enviar_email_gerente, enviar_slack_ceo, actualizar_dashboard]
  ├──→ (10000 < ventas ≤ 50000) enviar_email_equipo
  └──→ (ventas ≤ 10000) guardar_log
```

---

### ✅ Mejores Prácticas de Branching

1. **Funciones de decisión claras:** La lógica del branch debe ser simple y bien documentada
2. **Loggear la decisión:** Usa `print()` para saber qué camino se tomó
3. **Usar trigger_rules:** Siempre configurar trigger_rule en tasks después del branch
4. **Evitar branches anidados:** Si necesitas muchos if-else, considera refactorizar
5. **Testing:** Testear que cada camino del branch funciona correctamente

---

## 6. Sensors: Esperar por Condiciones

### 🎯 El Problema: Esperas Activas Ineficientes

Imagina que necesitas procesar un archivo que se genera cada hora por un sistema externo:

**Solución Ingenua (❌ Mala):**
```python
import time
import os

def esperar_archivo():
    while not os.path.exists("datos.csv"):
        print("Archivo no existe, esperando...")
        time.sleep(60)  # ❌ Bloquea un worker durante todo el tiempo!
    print("Archivo encontrado, procesando...")

task = PythonOperator(task_id="esperar", python_callable=esperar_archivo)
```

**Problemas:**
1. **Bloquea un worker:** El worker no puede ejecutar otras tasks mientras espera
2. **Desperdicia recursos:** Consume CPU y memoria sin hacer nada útil
3. **Sin timeout:** Podría esperar infinitamente
4. **Difícil de monitorear:** No se ve en la UI que está esperando

---

### 💡 La Solución: Sensors

Los **Sensors** son operators especializados en **esperar por condiciones**. Verifican periódicamente si una condición se cumple, y cuando lo hace, la task tiene éxito.

**Analogía:** Un Sensor es como un guardia de seguridad

Imagina un guardia de seguridad en la entrada de un edificio:
- **Cada 2 minutos** (poke_interval), el guardia verifica si llegó una persona autorizada
- Si **no ha llegado en 30 minutos** (timeout), el guardia se va (task falla)
- Si **llega la persona**, el guardia abre la puerta (task success)
- Mientras espera, **no bloquea la entrada** (no bloquea el worker en mode="reschedule")

---

### 📝 FileSensor: Esperar por Archivos

El **FileSensor** espera hasta que un archivo exista en el sistema de archivos.

```python
from airflow.sensors.filesystem import FileSensor

esperar_archivo = FileSensor(
    task_id="esperar_datos",
    filepath="/ruta/absoluta/datos.csv",
    poke_interval=30,  # Verificar cada 30 segundos
    timeout=600,  # Esperar máximo 10 minutos (600 segundos)
    mode="reschedule"  # No bloquear el worker
)
```

**Parámetros importantes:**

| Parámetro       | Descripción                         | Default         |
| --------------- | ----------------------------------- | --------------- |
| `filepath`      | Ruta absoluta al archivo            | Requerido       |
| `poke_interval` | Cada cuántos segundos verificar     | 60              |
| `timeout`       | Tiempo máximo de espera (segundos)  | 604800 (7 días) |
| `mode`          | "poke" o "reschedule"               | "poke"          |
| `soft_fail`     | Si True, no falla el DAG si timeout | False           |

---

**Mode: "poke" vs "reschedule"**

**mode="poke"** (default):
- El sensor **ocupa un worker slot** durante toda la espera
- Usa menos consultas a la BD
- ✅ Bueno para esperas cortas (<5 minutos)
- ❌ Malo para esperas largas (desperdicia workers)

**mode="reschedule"**:
- El sensor **libera el worker slot** entre verificaciones
- Permite que otros tasks usen ese worker
- ✅ Bueno para esperas largas (>5 minutos)
- ⚠️ Hace más consultas a la BD (una por cada poke)

**Recomendación:** Usa `mode="reschedule"` siempre que esperes más de 5 minutos.

---

### 🔍 Ejemplo Completo con FileSensor

```python
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

def procesar_archivo():
    import pandas as pd
    df = pd.read_csv("/tmp/datos.csv")
    print(f"[PROCESAR] Procesando {len(df)} filas")

with DAG("ejemplo_filesensor", start_date=datetime(2025, 1, 1), schedule=None) as dag:

    esperar = FileSensor(
        task_id="esperar_datos",
        filepath="/tmp/datos.csv",
        poke_interval=10,  # Cada 10 segundos
        timeout=60,  # Máximo 1 minuto
        mode="reschedule"
    )

    procesar = PythonOperator(
        task_id="procesar_datos",
        python_callable=procesar_archivo
    )

    esperar >> procesar
```

**¿Cómo funciona?**

1. El DAG se ejecuta
2. Task `esperar_datos` comienza
3. Cada 10 segundos, verifica si `/tmp/datos.csv` existe
4. Si existe → ✅ Success → ejecuta `procesar_datos`
5. Si pasan 60 segundos sin encontrarlo → ❌ Fail (timeout)

---

### ⏰ TimeSensor: Esperar hasta una Hora Específica

El **TimeSensor** espera hasta una hora específica del día.

```python
from airflow.sensors.time_sensor import TimeSensor

esperar_hora = TimeSensor(
    task_id="esperar_9am",
    target_time=datetime.time(9, 0, 0),  # 09:00:00
)
```

**Caso de uso:** Procesar datos solo después de las 9 AM (cuando el sistema fuente termina de cargar datos).

---

### 🌐 HttpSensor: Esperar por una API

El **HttpSensor** espera hasta que una API responda correctamente.

```python
from airflow.providers.http.sensors.http import HttpSensor

esperar_api = HttpSensor(
    task_id="esperar_api",
    http_conn_id="mi_api",  # Connection configurada en Airflow UI
    endpoint="/status",
    request_params={},
    response_check=lambda response: "ready" in response.text,
    poke_interval=30,
    timeout=300
)
```

---

### 🔗 ExternalTaskSensor: Esperar por Otro DAG

El **ExternalTaskSensor** espera hasta que una task de **otro DAG** termine.

```python
from airflow.sensors.external_task import ExternalTaskSensor

esperar_otro_dag = ExternalTaskSensor(
    task_id="esperar_dag_ventas",
    external_dag_id="procesar_ventas",
    external_task_id="cargar_bd",
    timeout=1800,  # 30 minutos
    poke_interval=60
)
```

**Caso de uso:** DAG B depende de que DAG A termine primero.

---

### ⚠️ Cuidados con Sensors

**1. Timeouts Razonables**

❌ Malo:
```python
sensor = FileSensor(filepath="...", timeout=86400)  # 24 horas!
```

✅ Bueno:
```python
sensor = FileSensor(filepath="...", timeout=600)  # 10 minutos
```

**2. Poke Interval Apropiado**

❌ Malo (demasiado frecuente):
```python
sensor = FileSensor(filepath="...", poke_interval=1)  # Cada segundo!
```

✅ Bueno:
```python
sensor = FileSensor(filepath="...", poke_interval=30)  # Cada 30 segundos
```

**3. Usar Mode Reschedule para Esperas Largas**

❌ Malo:
```python
sensor = FileSensor(filepath="...", timeout=3600, mode="poke")  # 1 hora bloqueando worker!
```

✅ Bueno:
```python
sensor = FileSensor(filepath="...", timeout=3600, mode="reschedule")
```

---

### ✅ Mejores Prácticas de Sensors

1. **Timeouts realistas:** Configura timeouts basados en expectativas reales
2. **Mode reschedule:** Usa `mode="reschedule"` para esperas >5 minutos
3. **Poke interval apropiado:** 10-60 segundos suele ser razonable
4. **Soft fail:** Usa `soft_fail=True` si la ausencia del recurso no es crítica
5. **Alertas:** Configura alertas si un sensor falla frecuentemente

---

## 7. Dynamic DAG Generation

### 🎯 El Problema: Crear Múltiples Tasks Similares

Imagina que necesitas procesar **10 archivos CSV** diferentes, uno por cada región:

**Solución Ingenua (❌ Malo):**
```python
procesar_madrid = PythonOperator(task_id="procesar_madrid", ...)
procesar_barcelona = PythonOperator(task_id="procesar_barcelona", ...)
procesar_valencia = PythonOperator(task_id="procesar_valencia", ...)
procesar_sevilla = PythonOperator(task_id="procesar_sevilla", ...)
# ... 10 tasks más!

inicio >> [procesar_madrid, procesar_barcelona, procesar_valencia, ...] >> fin
```

**Problemas:**
1. **Código repetitivo:** Copiar-pegar 10 veces
2. **Difícil de mantener:** Si cambias algo, tienes que editar 10 lugares
3. **No escalable:** ¿Y si mañana son 50 regiones?

---

### 💡 La Solución: Dynamic DAG Generation

Puedes **generar tasks dinámicamente** usando bucles de Python:

```python
regiones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]

for region in regiones:
    task = PythonOperator(
        task_id=f"procesar_{region.lower()}",
        python_callable=procesar_region,
        op_kwargs={"region": region}
    )
    inicio >> task >> fin
```

**¡Mucho más limpio!** ✨

---

### 🔍 Ejemplo Completo

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

def procesar_region(region: str):
    """Procesa datos de una región específica"""
    print(f"[{region}] Procesando datos de la región {region}")
    # Aquí irían las transformaciones específicas

with DAG("ejemplo_dynamic", start_date=datetime(2025, 1, 1), schedule=None) as dag:

    inicio = DummyOperator(task_id="inicio")
    fin = DummyOperator(task_id="fin")

    regiones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao",
                "Zaragoza", "Málaga", "Murcia", "Palma", "Las_Palmas"]

    for region in regiones:
        task = PythonOperator(
            task_id=f"procesar_{region}",
            python_callable=procesar_region,
            op_kwargs={"region": region}
        )

        inicio >> task >> fin
```

**Flujo visual:**
```
inicio → [procesar_Madrid, procesar_Barcelona, ..., procesar_Las_Palmas] → fin
```

**✅ Ventajas:**
- 10 tasks creadas con 5 líneas de código
- Fácil de mantener: cambio en un lugar
- Escalable: agregar regiones es solo editar la lista

---

### 🔢 Generar Tasks con Rangos Numéricos

```python
# Procesar 365 días del año
for dia in range(1, 366):
    task = PythonOperator(
        task_id=f"procesar_dia_{dia}",
        python_callable=procesar_dia,
        op_kwargs={"dia": dia}
    )
    inicio >> task >> consolidar
```

---

### 📁 Generar Tasks desde Archivos en un Directorio

```python
import os
from pathlib import Path

# Leer todos los CSV de un directorio
data_dir = Path("/data/input")
archivos = list(data_dir.glob("*.csv"))

for archivo in archivos:
    task = PythonOperator(
        task_id=f"procesar_{archivo.stem}",  # .stem = nombre sin extensión
        python_callable=procesar_archivo,
        op_kwargs={"ruta": str(archivo)}
    )
    inicio >> task >> consolidar
```

---

### ⚠️ Límites y Cuidados

**Límite Recomendado: 50-100 Tasks**

Si generas **demasiadas tasks** (>100), el DAG se vuelve lento:
- El scheduler tarda más en parsear el DAG
- La UI se vuelve lenta
- Más tareas = más consultas a la BD

**Alternativa para >100 Tareas:**

En lugar de crear 1000 tasks, crea **10 tasks que procesen 100 items cada una**:

```python
def procesar_batch(inicio: int, fin: int):
    for i in range(inicio, fin):
        procesar_item(i)

# 10 tasks, cada una procesa 100 items
for batch in range(10):
    task = PythonOperator(
        task_id=f"batch_{batch}",
        python_callable=procesar_batch,
        op_kwargs={"inicio": batch * 100, "fin": (batch + 1) * 100}
    )
    inicio >> task >> fin
```

---

### ✅ Mejores Prácticas de Dynamic DAGs

1. **Listas explícitas:** Define las listas al inicio del DAG, no dentro del bucle
2. **Límite de tasks:** No generes más de 50-100 tasks
3. **Batching:** Si necesitas muchas tasks, agrúpalas en batches
4. **Task IDs únicos:** Asegúrate de que cada task tenga un ID único
5. **Op_kwargs:** Usa `op_kwargs` para pasar parámetros específicos a cada task

---

## 8. Templating con Jinja2

### 🎯 El Problema: Configuraciones Dinámicas

Imagina que quieres procesar archivos con nombres que incluyen la **fecha de ejecución**:

**Solución Ingenua (❌ Malo):**
```python
def procesar(**context):
    fecha = context["execution_date"].strftime("%Y-%m-%d")
    archivo = f"/data/ventas_{fecha}.csv"
    # ...
```

Tienes que acceder al contexto en cada función. ¿Hay una forma más simple?

---

### 💡 La Solución: Templating con Jinja2

Airflow usa **Jinja2** para permitirte usar **variables dinámicas** directamente en los parámetros de los operators.

**Ejemplo:**
```python
task = BashOperator(
    task_id="procesar",
    bash_command="python procesar.py /data/ventas_{{ ds }}.csv"
)
```

`{{ ds }}` se reemplaza automáticamente por la fecha de ejecución en formato `YYYY-MM-DD`.

---

### 📝 Variables Jinja2 Comunes

| Variable                      | Descripción                     | Ejemplo                            |
| ----------------------------- | ------------------------------- | ---------------------------------- |
| `{{ ds }}`                    | Fecha de ejecución (YYYY-MM-DD) | 2025-01-15                         |
| `{{ ds_nodash }}`             | Fecha sin guiones (YYYYMMDD)    | 20250115                           |
| `{{ ts }}`                    | Timestamp completo (ISO 8601)   | 2025-01-15T10:30:00+00:00          |
| `{{ execution_date }}`        | Objeto datetime de la ejecución | datetime(2025, 1, 15, 10, 30)      |
| `{{ dag }}`                   | Objeto DAG                      | <DAG: mi_dag>                      |
| `{{ task }}`                  | Objeto Task                     | <Task(PythonOperator): mi_task>    |
| `{{ ti }}`                    | Objeto TaskInstance             | <TaskInstance: mi_dag.mi_task ...> |
| `{{ var.value.mi_variable }}` | Variable de Airflow             | (valor configurado en UI)          |
| `{{ var.json.mi_json.key }}`  | Variable JSON de Airflow        | (valor de una key JSON)            |

---

### 🔍 Ejemplo con BashOperator

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("ejemplo_templating", start_date=datetime(2025, 1, 1), schedule="@daily") as dag:

    procesar = BashOperator(
        task_id="procesar_archivo",
        bash_command="""
        echo "Procesando datos del {{ ds }}"
        python procesar.py --fecha={{ ds }} --output=/data/resultado_{{ ds_nodash }}.csv
        """
    )
```

Si se ejecuta el **2025-01-15**, el comando será:
```bash
echo "Procesando datos del 2025-01-15"
python procesar.py --fecha=2025-01-15 --output=/data/resultado_20250115.csv
```

---

### 🐍 Templating en PythonOperator

Por defecto, PythonOperator **no hace templating** en `op_kwargs`. Debes usar `templates_dict`:

```python
def procesar_con_fecha(fecha: str, archivo: str):
    print(f"Procesando fecha: {fecha}")
    print(f"Leyendo archivo: {archivo}")

task = PythonOperator(
    task_id="procesar",
    python_callable=procesar_con_fecha,
    op_kwargs={
        "fecha": "{{ ds }}",
        "archivo": "/data/ventas_{{ ds }}.csv"
    }
)
```

**⚠️ Importante:** Los parámetros de `op_kwargs` **SÍ se templatian** (desde Airflow 2.0+).

---

### 🧮 Macros de Jinja2

Airflow incluye **macros útiles** para manipular fechas:

```python
bash_command="""
# Fecha de ayer
python procesar.py --fecha={{ macros.ds_add(ds, -1) }}

# Fecha de mañana
python procesar.py --fecha={{ macros.ds_add(ds, 1) }}

# Fecha de hace 7 días
python procesar.py --fecha={{ macros.ds_add(ds, -7) }}

# Formato personalizado
python procesar.py --mes={{ execution_date.strftime('%B') }}
"""
```

---

### ✅ Mejores Prácticas de Templating

1. **Usa templates para rutas:** Evita hardcodear fechas
2. **Documenta:** Comenta qué variables usas y por qué
3. **Verifica sintaxis:** Errores de Jinja2 solo aparecen en ejecución
4. **Variables de Airflow:** Usa Variables para configuraciones que cambian entre ambientes
5. **Testing:** Prueba el templating con diferentes fechas

---

## 9. Mejores Prácticas del Tema 2

### ✅ TaskGroups

- ✅ Usa TaskGroups cuando tengas >5 tasks relacionadas
- ✅ Nombres descriptivos: `grupo_extraccion`, no `grupo1`
- ✅ No anides más de 2 niveles (grupo dentro de grupo dentro de grupo es confuso)
- ❌ No uses TaskGroups para 2-3 tasks (innecesario)

---

### ✅ XComs

- ✅ Solo para datos pequeños (<10 KB)
- ✅ Keys descriptivas: `total_ventas`, no `data1`
- ✅ Documenta qué XComs produce cada task
- ✅ Valida que el XCom existe antes de usarlo
- ❌ No uses XComs para DataFrames completos
- ❌ No hagas muchos `xcom_pull` en bucles

---

### ✅ Branching

- ✅ Funciones de decisión simples y documentadas
- ✅ Loggear qué camino se tomó
- ✅ Usar `trigger_rule` en tasks después del branch
- ❌ Evita branches anidados complejos
- ❌ No uses branching si un simple if en Python es suficiente

---

### ✅ Sensors

- ✅ Timeouts realistas (5-30 minutos, no 24 horas)
- ✅ `mode="reschedule"` para esperas >5 minutos
- ✅ Poke interval de 10-60 segundos
- ✅ Configura alertas si fallan frecuentemente
- ❌ No uses `poke_interval=1` (demasiado frecuente)

---

### ✅ Dynamic DAGs

- ✅ Limita a 50-100 tasks generadas
- ✅ Usa batching para procesar muchos items
- ✅ Task IDs únicos y descriptivos
- ❌ No generes >100 tasks (usa batching)
- ❌ No leas archivos externos al generar el DAG (parseo lento)

---

### ✅ Templating

- ✅ Usa templates para rutas con fechas
- ✅ Documenta qué variables usas
- ✅ Usa Variables de Airflow para configuraciones
- ❌ No abuses de templates complejos (difícil de debuggear)

---

## 10. Resumen y Próximos Pasos

### 🎉 ¡Felicitaciones!

Has completado el **Tema 2: Airflow Intermedio**. Ahora sabes:

✅ **TaskGroups:** Organizar DAGs complejos visualmente
✅ **XComs:** Compartir datos pequeños entre tasks
✅ **Branching:** Crear flujos condicionales (if-else)
✅ **Sensors:** Esperar por archivos, APIs, horarios
✅ **Dynamic DAGs:** Generar tasks automáticamente
✅ **Templating:** Usar variables dinámicas con Jinja2

---

### 📚 ¿Qué sigue?

**Próximo Tema: Tema 3 - Airflow en Producción**

Aprenderás:
- **Variables y Connections:** Gestionar configuraciones y credenciales
- **Logs y Monitoreo:** Integración con ELK, Datadog, CloudWatch
- **Testing de DAGs:** Unit tests, integration tests
- **Mejores Prácticas Productivas:** Retries, SLAs, alertas
- **Ejecutores:** LocalExecutor, CeleryExecutor, KubernetesExecutor
- **Optimización:** Paralelismo, pools, performance tuning

---

### 🛠️ Práctica Recomendada

Antes de continuar al Tema 3, **practica** lo aprendido:

1. Crear un DAG con TaskGroups (agrupa 6+ tasks)
2. Usar XComs para pasar datos entre 3 tasks
3. Implementar Branching con 2 caminos
4. Usar un FileSensor para esperar un archivo
5. Generar 10 tasks dinámicamente
6. Usar templating para paths con fechas

---

### 📖 Recursos Adicionales

- **Documentación Oficial de Airflow:** https://airflow.apache.org/docs/
- **TaskGroups:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups
- **XComs:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html
- **Sensors:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
- **Jinja2 Templating:** https://jinja.palletsprojects.com/

---

**🚀 ¡Continúa con el Tema 3: Airflow en Producción!**
