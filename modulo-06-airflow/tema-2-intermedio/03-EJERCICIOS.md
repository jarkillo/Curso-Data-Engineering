# 📚 Tema 2: Airflow Intermedio - Ejercicios Prácticos

**Módulo 6: Apache Airflow y Orquestación**
**Nivel:** Intermedio
**Duración estimada:** 4-6 horas
**Prerequisitos:** 01-TEORIA.md y 02-EJEMPLOS.md completados

---

## 📖 Índice

### Ejercicios Básicos ⭐
1. [Ejercicio 1: TaskGroup con 3 Tasks](#ejercicio-1-taskgroup-con-3-tasks-⭐)
2. [Ejercicio 2: XCom para Pasar un Número](#ejercicio-2-xcom-para-pasar-un-número-⭐)
3. [Ejercicio 3: BranchPythonOperator Simple](#ejercicio-3-branchpythonoperator-simple-⭐)
4. [Ejercicio 4: FileSensor con Timeout 30s](#ejercicio-4-filesensor-con-timeout-30s-⭐)
5. [Ejercicio 5: Crear 3 Tasks Dinámicamente](#ejercicio-5-crear-3-tasks-dinámicamente-⭐)

### Ejercicios Intermedios ⭐⭐
6. [Ejercicio 6: TaskGroup Anidado](#ejercicio-6-taskgroup-anidado-⭐⭐)
7. [Ejercicio 7: XComs con Diccionario Completo](#ejercicio-7-xcoms-con-diccionario-completo-⭐⭐)
8. [Ejercicio 8: Branch con 3 Caminos](#ejercicio-8-branch-con-3-caminos-⭐⭐)
9. [Ejercicio 9: TimeSensor (Esperar hasta 9 AM)](#ejercicio-9-timesensor-esperar-hasta-9-am-⭐⭐)
10. [Ejercicio 10: Dynamic DAG con 10 Tasks](#ejercicio-10-dynamic-dag-con-10-tasks-⭐⭐)

### Ejercicios Avanzados ⭐⭐⭐
11. [Ejercicio 11: Pipeline con TaskGroups + XComs + Branch](#ejercicio-11-pipeline-con-taskgroups--xcoms--branch-⭐⭐⭐)
12. [Ejercicio 12: ExternalTaskSensor](#ejercicio-12-externaltasksensor-⭐⭐⭐)
13. [Ejercicio 13: TriggerDagRunOperator con Parámetros](#ejercicio-13-triggerdagrunoperator-con-parámetros-⭐⭐⭐)
14. [Ejercicio 14: Dynamic DAG que Lee Directorio](#ejercicio-14-dynamic-dag-que-lee-directorio-⭐⭐⭐)
15. [Ejercicio 15: Pipeline Completo Integrando Todos los Conceptos](#ejercicio-15-pipeline-completo-integrando-todos-los-conceptos-⭐⭐⭐)

---

## Ejercicios Básicos ⭐

---

## Ejercicio 1: TaskGroup con 3 Tasks ⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_01_taskgroup` que tenga:
- Una task de inicio (`DummyOperator`)
- Un TaskGroup llamado `grupo_proceso` con 3 tasks dentro:
  - `task_a`: Imprime "Ejecutando Task A"
  - `task_b`: Imprime "Ejecutando Task B" (depende de task_a)
  - `task_c`: Imprime "Ejecutando Task C" (depende de task_b)
- Una task de fin (`DummyOperator`)

**Flujo:**
```
inicio → [grupo_proceso] → fin
         ├─ task_a
         ├─ task_b
         └─ task_c
```

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 1: TaskGroup con 3 Tasks"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime


def task_a():
    print("Ejecutando Task A")


def task_b():
    print("Ejecutando Task B")


def task_c():
    print("Ejecutando Task C")


with DAG(
    dag_id="ejercicio_01_taskgroup",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    with TaskGroup("grupo_proceso") as grupo_proceso:
        a = PythonOperator(task_id="task_a", python_callable=task_a)
        b = PythonOperator(task_id="task_b", python_callable=task_b)
        c = PythonOperator(task_id="task_c", python_callable=task_c)

        a >> b >> c

    fin = DummyOperator(task_id="fin")

    inicio >> grupo_proceso >> fin
```

**Verificación:**
- En Airflow UI, el grupo debe aparecer colapsado como `📁 grupo_proceso`
- Al expandirlo, debe mostrar `task_a → task_b → task_c`
- Los logs deben mostrar los 3 mensajes en orden

</details>

---

## Ejercicio 2: XCom para Pasar un Número ⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_02_xcom` que tenga 2 tasks:
1. `generar_numero`: Genera un número aleatorio entre 1 y 100 y lo retorna
2. `imprimir_numero`: Lee el número de XCom y lo imprime con el mensaje "El número generado es: X"

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 2: XCom para Pasar un Número"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import random


def generar_numero():
    """Genera un número aleatorio entre 1 y 100"""
    numero = random.randint(1, 100)
    print(f"[GENERAR] Número generado: {numero}")
    return numero


def imprimir_numero(**context):
    """Lee el número de XCom y lo imprime"""
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[IMPRIMIR] El número generado es: {numero}")


with DAG(
    dag_id="ejercicio_02_xcom",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    generar = PythonOperator(
        task_id="generar_numero",
        python_callable=generar_numero
    )

    imprimir = PythonOperator(
        task_id="imprimir_numero",
        python_callable=imprimir_numero
    )

    generar >> imprimir
```

**Verificación:**
- La task `generar_numero` debe generar un número diferente cada vez
- La task `imprimir_numero` debe mostrar el mismo número que generó la anterior

</details>

---

## Ejercicio 3: BranchPythonOperator Simple ⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_03_branch` que:
1. Genera un número aleatorio entre 1 y 10
2. Usa BranchPythonOperator para decidir:
   - Si número ≥ 5: ejecutar `tarea_alta`
   - Si número < 5: ejecutar `tarea_baja`
3. Tiene una task final que se ejecuta siempre (`DummyOperator` con `trigger_rule` adecuado)

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 3: BranchPythonOperator Simple"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
import random


def generar_numero():
    """Genera un número aleatorio entre 1 y 10"""
    numero = random.randint(1, 10)
    print(f"[GENERAR] Número generado: {numero}")
    return numero


def decidir_camino(**context):
    """Decide qué task ejecutar según el número"""
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")

    print(f"[DECIDIR] Número: {numero}")

    if numero >= 5:
        print("[DECIDIR] → Ruta ALTA")
        return "tarea_alta"
    else:
        print("[DECIDIR] → Ruta BAJA")
        return "tarea_baja"


def tarea_alta(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[ALTA] Número {numero} es >= 5")


def tarea_baja(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[BAJA] Número {numero} es < 5")


with DAG(
    dag_id="ejercicio_03_branch",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    generar = PythonOperator(
        task_id="generar_numero",
        python_callable=generar_numero
    )

    decidir = BranchPythonOperator(
        task_id="decidir_camino",
        python_callable=decidir_camino
    )

    alta = PythonOperator(
        task_id="tarea_alta",
        python_callable=tarea_alta
    )

    baja = PythonOperator(
        task_id="tarea_baja",
        python_callable=tarea_baja
    )

    fin = DummyOperator(
        task_id="fin",
        trigger_rule="none_failed_min_one_success"
    )

    generar >> decidir >> [alta, baja] >> fin
```

**Verificación:**
- Ejecuta el DAG varias veces para ver diferentes caminos
- Una task siempre estará "skipped"
- La task `fin` siempre se debe ejecutar

</details>

---

## Ejercicio 4: FileSensor con Timeout 30s ⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_04_sensor` que:
1. Usa un FileSensor para esperar el archivo `/tmp/ejercicio_04.txt`
2. Configurar:
   - `poke_interval=5` (cada 5 segundos)
   - `timeout=30` (máximo 30 segundos)
   - `mode="reschedule"`
3. Una vez detectado el archivo, imprime su contenido

**Nota:** Para probar, crea el archivo manualmente:
```bash
echo "Hola desde el archivo" > /tmp/ejercicio_04.txt
```

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 4: FileSensor con Timeout 30s"""

from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime


def leer_archivo():
    """Lee y muestra el contenido del archivo"""
    ruta = "/tmp/ejercicio_04.txt"

    print(f"[LEER] Leyendo archivo: {ruta}")

    try:
        with open(ruta, "r") as f:
            contenido = f.read()

        print(f"[LEER] Contenido: {contenido}")
        print(f"[LEER] ✅ Archivo leído exitosamente")

    except Exception as e:
        print(f"[LEER] ❌ Error al leer archivo: {e}")
        raise


with DAG(
    dag_id="ejercicio_04_sensor",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    esperar = FileSensor(
        task_id="esperar_archivo",
        filepath="/tmp/ejercicio_04.txt",
        poke_interval=5,
        timeout=30,
        mode="reschedule"
    )

    leer = PythonOperator(
        task_id="leer_archivo",
        python_callable=leer_archivo
    )

    esperar >> leer
```

**Verificación:**
1. Ejecuta el DAG sin crear el archivo → debe fallar por timeout después de 30s
2. Ejecuta el DAG y crea el archivo dentro de 30s → debe leerlo exitosamente

</details>

---

## Ejercicio 5: Crear 3 Tasks Dinámicamente ⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_05_dynamic` que:
1. Genera dinámicamente 3 tasks que procesan las ciudades: `["Madrid", "Barcelona", "Valencia"]`
2. Cada task debe imprimir: "Procesando datos de {ciudad}"
3. Las 3 tasks deben ejecutarse en paralelo
4. Después de todas, ejecutar una task `finalizar`

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 5: Crear 3 Tasks Dinámicamente"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime


def procesar_ciudad(ciudad: str):
    """Procesa datos de una ciudad"""
    print(f"[{ciudad.upper()}] Procesando datos de {ciudad}")
    print(f"[{ciudad.upper()}] ✅ Procesamiento completado")


def finalizar():
    """Finaliza el procesamiento"""
    print("[FINALIZAR] Todas las ciudades procesadas")


with DAG(
    dag_id="ejercicio_05_dynamic",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    ciudades = ["Madrid", "Barcelona", "Valencia"]

    tasks_ciudades = []

    for ciudad in ciudades:
        task = PythonOperator(
            task_id=f"procesar_{ciudad.lower()}",
            python_callable=procesar_ciudad,
            op_kwargs={"ciudad": ciudad}
        )
        tasks_ciudades.append(task)
        inicio >> task

    fin = PythonOperator(
        task_id="finalizar",
        python_callable=finalizar
    )

    tasks_ciudades >> fin
```

**Verificación:**
- En el Graph View, las 3 tasks deben estar en paralelo
- Los logs deben mostrar los 3 mensajes de procesamiento
- La task `finalizar` debe ejecutarse al final

</details>

---

## Ejercicios Intermedios ⭐⭐

---

## Ejercicio 6: TaskGroup Anidado ⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_06_taskgroup_anidado` con TaskGroups anidados:
```
grupo_principal/
  ├─ grupo_extraccion/
  │   ├─ extraer_a
  │   └─ extraer_b
  └─ grupo_transformacion/
      ├─ transformar_a
      └─ transformar_b
```

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 6: TaskGroup Anidado"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime


def extraer_a():
    print("[EXTRAER_A] Extrayendo datos A")


def extraer_b():
    print("[EXTRAER_B] Extrayendo datos B")


def transformar_a():
    print("[TRANSFORMAR_A] Transformando datos A")


def transformar_b():
    print("[TRANSFORMAR_B] Transformando datos B")


with DAG(
    dag_id="ejercicio_06_taskgroup_anidado",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    with TaskGroup("grupo_principal") as grupo_principal:

        with TaskGroup("grupo_extraccion") as grupo_ext:
            ext_a = PythonOperator(task_id="extraer_a", python_callable=extraer_a)
            ext_b = PythonOperator(task_id="extraer_b", python_callable=extraer_b)

            ext_a >> ext_b

        with TaskGroup("grupo_transformacion") as grupo_trans:
            trans_a = PythonOperator(task_id="transformar_a", python_callable=transformar_a)
            trans_b = PythonOperator(task_id="transformar_b", python_callable=transformar_b)

            trans_a >> trans_b

        grupo_ext >> grupo_trans

    fin = DummyOperator(task_id="fin")

    inicio >> grupo_principal >> fin
```

**Verificación:**
- En Airflow UI, al colapsar, debe mostrar solo `📁 grupo_principal`
- Al expandirlo, debe mostrar `📁 grupo_extraccion` y `📁 grupo_transformacion`
- Al expandir esos grupos, deben aparecer las tasks individuales

</details>

---

## Ejercicio 7: XComs con Diccionario Completo ⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_07_xcom_dict` que:
1. `calcular_estadisticas`: Calcula y retorna un diccionario con:
   - `total`: Suma de una lista de números [10, 20, 30, 40, 50]
   - `promedio`: Promedio de esos números
   - `maximo`: Valor máximo
   - `minimo`: Valor mínimo
2. `mostrar_estadisticas`: Lee el diccionario y muestra cada valor formateado

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 7: XComs con Diccionario Completo"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def calcular_estadisticas():
    """Calcula estadísticas de una lista de números"""
    numeros = [10, 20, 30, 40, 50]

    total = sum(numeros)
    promedio = total / len(numeros)
    maximo = max(numeros)
    minimo = min(numeros)

    estadisticas = {
        "total": total,
        "promedio": promedio,
        "maximo": maximo,
        "minimo": minimo
    }

    print(f"[CALCULAR] Estadísticas calculadas: {estadisticas}")

    return estadisticas


def mostrar_estadisticas(**context):
    """Muestra las estadísticas formateadas"""
    ti = context["ti"]
    stats = ti.xcom_pull(task_ids="calcular_estadisticas")

    print("="*40)
    print("     ESTADÍSTICAS")
    print("="*40)
    print(f"Total:      {stats['total']:>10}")
    print(f"Promedio:   {stats['promedio']:>10.2f}")
    print(f"Máximo:     {stats['maximo']:>10}")
    print(f"Mínimo:     {stats['minimo']:>10}")
    print("="*40)


with DAG(
    dag_id="ejercicio_07_xcom_dict",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio"],
) as dag:

    calcular = PythonOperator(
        task_id="calcular_estadisticas",
        python_callable=calcular_estadisticas
    )

    mostrar = PythonOperator(
        task_id="mostrar_estadisticas",
        python_callable=mostrar_estadisticas
    )

    calcular >> mostrar
```

**Verificación:**
- La task `mostrar_estadisticas` debe mostrar una tabla formateada
- Los valores deben ser: Total=150, Promedio=30.00, Máximo=50, Mínimo=10

</details>

---

## Ejercicio 8: Branch con 3 Caminos ⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_08_branch_3` con un branch que elige entre 3 caminos:
- Si número < 30: ruta `baja`
- Si 30 ≤ número < 70: ruta `media`
- Si número ≥ 70: ruta `alta`

Cada ruta debe tener su propia task, y todas convergen en una task `consolidar` con trigger_rule adecuado.

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 8: Branch con 3 Caminos"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
import random


def generar_numero():
    """Genera un número entre 0 y 100"""
    numero = random.randint(0, 100)
    print(f"[GENERAR] Número generado: {numero}")
    return numero


def decidir_camino(**context):
    """Decide qué camino tomar según el número"""
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")

    print(f"[DECIDIR] Número: {numero}")

    if numero < 30:
        print("[DECIDIR] → Ruta BAJA")
        return "ruta_baja"
    elif numero < 70:
        print("[DECIDIR] → Ruta MEDIA")
        return "ruta_media"
    else:
        print("[DECIDIR] → Ruta ALTA")
        return "ruta_alta"


def ruta_baja(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[BAJA] Procesando número bajo: {numero}")


def ruta_media(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[MEDIA] Procesando número medio: {numero}")


def ruta_alta(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[ALTA] Procesando número alto: {numero}")


def consolidar(**context):
    ti = context["ti"]
    numero = ti.xcom_pull(task_ids="generar_numero")
    print(f"[CONSOLIDAR] Número {numero} procesado exitosamente")


with DAG(
    dag_id="ejercicio_08_branch_3",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio"],
) as dag:

    generar = PythonOperator(
        task_id="generar_numero",
        python_callable=generar_numero
    )

    decidir = BranchPythonOperator(
        task_id="decidir_camino",
        python_callable=decidir_camino
    )

    baja = PythonOperator(task_id="ruta_baja", python_callable=ruta_baja)
    media = PythonOperator(task_id="ruta_media", python_callable=ruta_media)
    alta = PythonOperator(task_id="ruta_alta", python_callable=ruta_alta)

    consolidar_task = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar,
        trigger_rule="none_failed_min_one_success"
    )

    generar >> decidir >> [baja, media, alta] >> consolidar_task
```

**Verificación:**
- Ejecuta múltiples veces para ver las 3 rutas diferentes
- Solo una ruta debe ejecutarse cada vez
- `consolidar` siempre se debe ejecutar

</details>

---

## Ejercicio 9: TimeSensor (Esperar hasta 9 AM) ⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_09_timesensor` que:
1. Use un TimeSensor para esperar hasta las 09:00:00
2. Después ejecute una task que imprime "¡Buenos días! Son las 9 AM"

**Nota:** Para probar rápidamente, ajusta el `target_time` a la hora actual + 1 minuto.

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 9: TimeSensor (Esperar hasta 9 AM)"""

from airflow import DAG
from airflow.sensors.time_sensor import TimeSensor
from airflow.operators.python import PythonOperator
from datetime import datetime, time


def saludar_matutino():
    """Saludo matutino"""
    hora_actual = datetime.now().strftime("%H:%M:%S")
    print(f"[SALUDAR] ¡Buenos días! Son las {hora_actual}")
    print(f"[SALUDAR] Es hora de empezar a trabajar")


with DAG(
    dag_id="ejercicio_09_timesensor",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio"],
) as dag:

    # Para pruebas rápidas, ajusta esta hora a la actual + 1 minuto
    # Por ejemplo, si son las 14:30, pon time(14, 31, 0)
    esperar_hora = TimeSensor(
        task_id="esperar_9am",
        target_time=time(9, 0, 0)  # 09:00:00
    )

    saludar = PythonOperator(
        task_id="saludar_matutino",
        python_callable=saludar_matutino
    )

    esperar_hora >> saludar
```

**Verificación:**
- Si ejecutas antes de las 9 AM, el sensor esperará hasta las 9
- Si ejecutas después de las 9 AM, el sensor pasará inmediatamente
- Para pruebas, ajusta `target_time` a la hora actual + 1 minuto

</details>

---

## Ejercicio 10: Dynamic DAG con 10 Tasks ⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_10_dynamic_10` que:
1. Genera dinámicamente 10 tasks numeradas del 1 al 10
2. Cada task imprime: "Procesando item {número}"
3. Las 10 tasks se ejecutan en paralelo
4. Después de todas, una task `resumen` imprime "10 items procesados"

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 10: Dynamic DAG con 10 Tasks"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime


def procesar_item(numero: int):
    """Procesa un item numerado"""
    print(f"[ITEM_{numero}] Procesando item {numero}")
    print(f"[ITEM_{numero}] ✅ Item {numero} completado")


def resumen():
    """Muestra resumen final"""
    print("[RESUMEN] =" * 30)
    print("[RESUMEN] 10 items procesados exitosamente")
    print("[RESUMEN] =" * 30)


with DAG(
    dag_id="ejercicio_10_dynamic_10",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    tasks_items = []

    for i in range(1, 11):  # 1 a 10
        task = PythonOperator(
            task_id=f"procesar_item_{i}",
            python_callable=procesar_item,
            op_kwargs={"numero": i}
        )
        tasks_items.append(task)
        inicio >> task

    resumen_task = PythonOperator(
        task_id="resumen",
        python_callable=resumen
    )

    tasks_items >> resumen_task
```

**Verificación:**
- En el Graph View, deben aparecer 10 tasks en paralelo
- Los logs deben mostrar mensajes del 1 al 10
- La task `resumen` debe ejecutarse al final

</details>

---

## Ejercicios Avanzados ⭐⭐⭐

---

## Ejercicio 11: Pipeline con TaskGroups + XComs + Branch ⭐⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_11_complejo` que integre múltiples conceptos:

1. **TaskGroup "extraccion"** con 2 tasks:
   - `extraer_ventas`: Retorna un número aleatorio entre 5000 y 15000
   - `extraer_gastos`: Retorna un número aleatorio entre 3000 y 10000

2. **Task "calcular_beneficio"**:
   - Lee ventas y gastos de XCom
   - Calcula beneficio = ventas - gastos
   - Retorna el beneficio

3. **BranchPythonOperator "decidir_accion"**:
   - Si beneficio > 2000: ejecutar `reporte_positivo`
   - Si beneficio ≤ 2000: ejecutar `reporte_negativo`

4. **Task "consolidar"** (trigger_rule adecuado):
   - Muestra un resumen final

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 11: Pipeline con TaskGroups + XComs + Branch"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import random


def extraer_ventas():
    """Extrae el total de ventas"""
    ventas = random.uniform(5000, 15000)
    print(f"[VENTAS] Total extraído: {ventas:.2f}€")
    return ventas


def extraer_gastos():
    """Extrae el total de gastos"""
    gastos = random.uniform(3000, 10000)
    print(f"[GASTOS] Total extraído: {gastos:.2f}€")
    return gastos


def calcular_beneficio(**context):
    """Calcula el beneficio"""
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="grupo_extraccion.extraer_ventas")
    gastos = ti.xcom_pull(task_ids="grupo_extraccion.extraer_gastos")

    beneficio = ventas - gastos

    print(f"[BENEFICIO] Ventas: {ventas:.2f}€")
    print(f"[BENEFICIO] Gastos: {gastos:.2f}€")
    print(f"[BENEFICIO] Beneficio: {beneficio:.2f}€")

    return beneficio


def decidir_accion(**context):
    """Decide qué reporte generar"""
    ti = context["ti"]
    beneficio = ti.xcom_pull(task_ids="calcular_beneficio")

    umbral = 2000

    print(f"[DECIDIR] Beneficio: {beneficio:.2f}€")
    print(f"[DECIDIR] Umbral: {umbral:.2f}€")

    if beneficio > umbral:
        print("[DECIDIR] → Reporte POSITIVO")
        return "reporte_positivo"
    else:
        print("[DECIDIR] → Reporte NEGATIVO")
        return "reporte_negativo"


def reporte_positivo(**context):
    ti = context["ti"]
    beneficio = ti.xcom_pull(task_ids="calcular_beneficio")

    print("="*50)
    print("✅ REPORTE POSITIVO")
    print("="*50)
    print(f"Beneficio: {beneficio:.2f}€")
    print("El mes ha sido exitoso!")
    print("="*50)


def reporte_negativo(**context):
    ti = context["ti"]
    beneficio = ti.xcom_pull(task_ids="calcular_beneficio")

    print("="*50)
    print("⚠️ REPORTE NEGATIVO")
    print("="*50)
    print(f"Beneficio: {beneficio:.2f}€")
    print("Se requieren medidas correctivas")
    print("="*50)


def consolidar(**context):
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="grupo_extraccion.extraer_ventas")
    gastos = ti.xcom_pull(task_ids="grupo_extraccion.extraer_gastos")
    beneficio = ti.xcom_pull(task_ids="calcular_beneficio")

    print("[CONSOLIDAR] Resumen Final:")
    print(f"  - Ventas:    {ventas:.2f}€")
    print(f"  - Gastos:    {gastos:.2f}€")
    print(f"  - Beneficio: {beneficio:.2f}€")
    print("[CONSOLIDAR] ✅ Consolidación completada")


with DAG(
    dag_id="ejercicio_11_complejo",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    with TaskGroup("grupo_extraccion") as grupo_ext:
        ventas_task = PythonOperator(
            task_id="extraer_ventas",
            python_callable=extraer_ventas
        )
        gastos_task = PythonOperator(
            task_id="extraer_gastos",
            python_callable=extraer_gastos
        )

        [ventas_task, gastos_task]

    calcular = PythonOperator(
        task_id="calcular_beneficio",
        python_callable=calcular_beneficio
    )

    decidir = BranchPythonOperator(
        task_id="decidir_accion",
        python_callable=decidir_accion
    )

    positivo = PythonOperator(
        task_id="reporte_positivo",
        python_callable=reporte_positivo
    )

    negativo = PythonOperator(
        task_id="reporte_negativo",
        python_callable=reporte_negativo
    )

    consolidar_task = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar,
        trigger_rule="none_failed_min_one_success"
    )

    fin = DummyOperator(task_id="fin")

    inicio >> grupo_ext >> calcular >> decidir >> [positivo, negativo] >> consolidar_task >> fin
```

**Verificación:**
- El TaskGroup debe colapsar las 2 extracciones
- El branch debe elegir un reporte según el beneficio
- La consolidación debe mostrar todos los valores

</details>

---

## Ejercicio 12: ExternalTaskSensor ⭐⭐⭐

### 📝 Enunciado

Crea 2 DAGs:
1. `ejercicio_12_dag_a`: Tiene una task `procesar` que imprime "DAG A completado"
2. `ejercicio_12_dag_b`: Tiene un ExternalTaskSensor que espera a que `dag_a` complete, y luego ejecuta una task que imprime "DAG B ejecutado después de DAG A"

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

**Archivo 1: ejercicio_12_dag_a.py**
```python
"""Ejercicio 12 - DAG A: DAG que será esperado"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def procesar():
    """Procesa datos en DAG A"""
    print("[DAG_A] Procesando datos...")
    print("[DAG_A] ✅ DAG A completado")


with DAG(
    dag_id="ejercicio_12_dag_a",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "dag_a"],
) as dag:

    procesar_task = PythonOperator(
        task_id="procesar",
        python_callable=procesar
    )
```

**Archivo 2: ejercicio_12_dag_b.py**
```python
"""Ejercicio 12 - DAG B: DAG que espera al DAG A"""

from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import PythonOperator
from datetime import datetime


def procesar_despues():
    """Procesa datos después de que DAG A termine"""
    print("[DAG_B] DAG A ha completado")
    print("[DAG_B] ✅ DAG B ejecutado después de DAG A")


with DAG(
    dag_id="ejercicio_12_dag_b",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "dag_b"],
) as dag:

    esperar_dag_a = ExternalTaskSensor(
        task_id="esperar_dag_a",
        external_dag_id="ejercicio_12_dag_a",
        external_task_id="procesar",
        timeout=300,  # 5 minutos
        poke_interval=10
    )

    procesar_task = PythonOperator(
        task_id="procesar_despues",
        python_callable=procesar_despues
    )

    esperar_dag_a >> procesar_task
```

**Verificación:**
1. Ejecuta `ejercicio_12_dag_a` primero
2. Luego ejecuta `ejercicio_12_dag_b`
3. El DAG B debe esperar hasta que el DAG A complete

</details>

---

## Ejercicio 13: TriggerDagRunOperator con Parámetros ⭐⭐⭐

### 📝 Enunciado

Crea 2 DAGs:
1. `ejercicio_13_dag_trigger`: Usa TriggerDagRunOperator para ejecutar el `dag_target` y le pasa un parámetro `numero: 42`
2. `ejercicio_13_dag_target`: Lee el parámetro del conf y lo imprime

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

**Archivo 1: ejercicio_13_dag_trigger.py**
```python
"""Ejercicio 13 - DAG Trigger: Dispara otro DAG"""

from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator
from datetime import datetime


def preparar():
    """Prepara datos antes de disparar"""
    print("[TRIGGER] Preparando para disparar DAG Target")
    print("[TRIGGER] Parámetro a enviar: numero=42")


with DAG(
    dag_id="ejercicio_13_dag_trigger",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "trigger"],
) as dag:

    preparar_task = PythonOperator(
        task_id="preparar",
        python_callable=preparar
    )

    disparar = TriggerDagRunOperator(
        task_id="disparar_dag_target",
        trigger_dag_id="ejercicio_13_dag_target",
        conf={"numero": 42}  # Parámetros a pasar
    )

    preparar_task >> disparar
```

**Archivo 2: ejercicio_13_dag_target.py**
```python
"""Ejercicio 13 - DAG Target: Recibe parámetros"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def procesar_con_parametro(**context):
    """Procesa usando el parámetro recibido"""
    conf = context["dag_run"].conf or {}
    numero = conf.get("numero", None)

    print(f"[TARGET] Parámetro recibido: numero={numero}")

    if numero:
        resultado = numero * 2
        print(f"[TARGET] Resultado: {numero} * 2 = {resultado}")
    else:
        print("[TARGET] ⚠️ No se recibió parámetro")


with DAG(
    dag_id="ejercicio_13_dag_target",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "target"],
) as dag:

    procesar = PythonOperator(
        task_id="procesar_con_parametro",
        python_callable=procesar_con_parametro
    )
```

**Verificación:**
1. Ejecuta `ejercicio_13_dag_trigger`
2. Debe disparar automáticamente `ejercicio_13_dag_target`
3. El DAG Target debe recibir e imprimir `numero=42` y calcular `42 * 2 = 84`

</details>

---

## Ejercicio 14: Dynamic DAG que Lee Directorio ⭐⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_14_dynamic_dir` que:
1. Lee todos los archivos `.txt` del directorio `/tmp/datos/`
2. Genera dinámicamente una task por cada archivo encontrado
3. Cada task imprime el nombre del archivo y su tamaño

**Prerequisito:** Crea algunos archivos de prueba:
```bash
mkdir -p /tmp/datos
echo "contenido 1" > /tmp/datos/archivo1.txt
echo "contenido 2" > /tmp/datos/archivo2.txt
echo "contenido 3" > /tmp/datos/archivo3.txt
```

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 14: Dynamic DAG que Lee Directorio"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from pathlib import Path


def procesar_archivo(ruta: str):
    """Procesa un archivo individual"""
    archivo = Path(ruta)

    if archivo.exists():
        tamano = archivo.stat().st_size
        print(f"[ARCHIVO] Nombre: {archivo.name}")
        print(f"[ARCHIVO] Ruta: {archivo}")
        print(f"[ARCHIVO] Tamaño: {tamano} bytes")
        print(f"[ARCHIVO] ✅ Procesado exitosamente")
    else:
        print(f"[ARCHIVO] ❌ Archivo no encontrado: {ruta}")


def consolidar():
    """Consolida el procesamiento"""
    print("[CONSOLIDAR] Todos los archivos procesados")


with DAG(
    dag_id="ejercicio_14_dynamic_dir",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    # Leer archivos del directorio
    directorio = Path("/tmp/datos")
    directorio.mkdir(exist_ok=True)

    archivos_txt = list(directorio.glob("*.txt"))

    if archivos_txt:
        tasks_archivos = []

        for archivo in archivos_txt:
            task = PythonOperator(
                task_id=f"procesar_{archivo.stem}",
                python_callable=procesar_archivo,
                op_kwargs={"ruta": str(archivo)}
            )
            tasks_archivos.append(task)
            inicio >> task

        consolidar_task = PythonOperator(
            task_id="consolidar",
            python_callable=consolidar
        )

        tasks_archivos >> consolidar_task
    else:
        # Si no hay archivos, crear una task dummy
        sin_archivos = DummyOperator(
            task_id="sin_archivos_encontrados"
        )
        inicio >> sin_archivos
```

**Verificación:**
1. Crea los archivos de prueba en `/tmp/datos/`
2. Ejecuta el DAG
3. Debe crear tantas tasks como archivos `.txt` encuentre
4. Cada task debe mostrar el nombre y tamaño del archivo

</details>

---

## Ejercicio 15: Pipeline Completo Integrando Todos los Conceptos ⭐⭐⭐

### 📝 Enunciado

Crea un DAG llamado `ejercicio_15_pipeline_completo` que integre TODOS los conceptos del Tema 2:

1. **TaskGroup "extraccion"** con 2 tasks en paralelo:
   - `extraer_ventas`: Genera lista de 5 ventas aleatorias
   - `extraer_clientes`: Genera lista de 3 clientes

2. **TaskGroup "procesamiento"**:
   - `calcular_total`: Suma todas las ventas (usando XCom)
   - `contar_clientes`: Cuenta clientes (usando XCom)

3. **BranchPythonOperator "decidir_reporte"**:
   - Si total > 1000: `reporte_detallado`
   - Si total ≤ 1000: `reporte_simple`

4. **FileSensor** (opcional): Espera archivo de configuración (con timeout corto para no bloquear)

5. **Dynamic tasks**: Genera 3 tasks de notificación dinámicamente (`notificar_email`, `notificar_slack`, `notificar_sms`)

6. **Task final "consolidar"** con trigger_rule adecuado

### ✅ Solución

<details>
<summary>👉 Haz clic para ver la solución</summary>

```python
"""Ejercicio 15: Pipeline Completo Integrando Todos los Conceptos"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import random


# ========== EXTRACCIÓN ==========

def extraer_ventas():
    """Genera ventas aleatorias"""
    ventas = [random.uniform(100, 500) for _ in range(5)]
    print(f"[VENTAS] Extraídas {len(ventas)} ventas")
    print(f"[VENTAS] Valores: {[f'{v:.2f}€' for v in ventas]}")
    return ventas


def extraer_clientes():
    """Genera lista de clientes"""
    clientes = [f"Cliente_{i}" for i in range(1, 4)]
    print(f"[CLIENTES] Extraídos {len(clientes)} clientes")
    print(f"[CLIENTES] Lista: {clientes}")
    return clientes


# ========== PROCESAMIENTO ==========

def calcular_total(**context):
    """Calcula el total de ventas"""
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="grupo_extraccion.extraer_ventas")

    total = sum(ventas)
    print(f"[TOTAL] Total calculado: {total:.2f}€")

    return total


def contar_clientes(**context):
    """Cuenta los clientes"""
    ti = context["ti"]
    clientes = ti.xcom_pull(task_ids="grupo_extraccion.extraer_clientes")

    cantidad = len(clientes)
    print(f"[CONTAR] Clientes contados: {cantidad}")

    return cantidad


# ========== BRANCHING ==========

def decidir_reporte(**context):
    """Decide qué tipo de reporte generar"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_total")

    umbral = 1000

    print(f"[DECIDIR] Total: {total:.2f}€")
    print(f"[DECIDIR] Umbral: {umbral:.2f}€")

    if total > umbral:
        print("[DECIDIR] → Reporte DETALLADO")
        return "reporte_detallado"
    else:
        print("[DECIDIR] → Reporte SIMPLE")
        return "reporte_simple"


def reporte_detallado(**context):
    """Genera reporte detallado"""
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="grupo_extraccion.extraer_ventas")
    total = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_total")
    clientes = ti.xcom_pull(task_ids="grupo_procesamiento.contar_clientes")

    print("="*60)
    print("          REPORTE DETALLADO DE VENTAS")
    print("="*60)
    print(f"Total de Ventas:     {total:>10.2f}€")
    print(f"Cantidad de Ventas:  {len(ventas):>10}")
    print(f"Promedio por Venta:  {(total/len(ventas)):>10.2f}€")
    print(f"Clientes:            {clientes:>10}")
    print("")
    print("Ventas Individuales:")
    for i, venta in enumerate(ventas, 1):
        print(f"  {i}. {venta:.2f}€")
    print("="*60)


def reporte_simple(**context):
    """Genera reporte simple"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_total")

    print("="*40)
    print("     REPORTE SIMPLE")
    print("="*40)
    print(f"Total: {total:.2f}€")
    print("="*40)


# ========== NOTIFICACIONES DINÁMICAS ==========

def notificar(canal: str, **context):
    """Envía notificación por un canal específico"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_total")

    print(f"[{canal.upper()}] 📧 Enviando notificación...")
    print(f"[{canal.upper()}] Mensaje: Total de ventas: {total:.2f}€")
    print(f"[{canal.upper()}] ✅ Notificación enviada por {canal}")


# ========== CONSOLIDACIÓN ==========

def consolidar(**context):
    """Consolida todos los resultados"""
    ti = context["ti"]

    ventas = ti.xcom_pull(task_ids="grupo_extraccion.extraer_ventas")
    clientes = ti.xcom_pull(task_ids="grupo_extraccion.extraer_clientes")
    total = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_total")
    num_clientes = ti.xcom_pull(task_ids="grupo_procesamiento.contar_clientes")

    print("[CONSOLIDAR] Resumen Final del Pipeline:")
    print(f"  - Ventas procesadas:  {len(ventas)}")
    print(f"  - Clientes:           {num_clientes}")
    print(f"  - Total:              {total:.2f}€")
    print("[CONSOLIDAR] ✅ Pipeline completado exitosamente")


# ========== DAG ==========

with DAG(
    dag_id="ejercicio_15_pipeline_completo",
    description="Pipeline completo integrando todos los conceptos del Tema 2",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "completo"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    # TaskGroup: Extracción
    with TaskGroup("grupo_extraccion") as grupo_ext:
        ventas_task = PythonOperator(
            task_id="extraer_ventas",
            python_callable=extraer_ventas
        )
        clientes_task = PythonOperator(
            task_id="extraer_clientes",
            python_callable=extraer_clientes
        )

        [ventas_task, clientes_task]

    # TaskGroup: Procesamiento
    with TaskGroup("grupo_procesamiento") as grupo_proc:
        total_task = PythonOperator(
            task_id="calcular_total",
            python_callable=calcular_total
        )
        contar_task = PythonOperator(
            task_id="contar_clientes",
            python_callable=contar_clientes
        )

        [total_task, contar_task]

    # Branching
    decidir = BranchPythonOperator(
        task_id="decidir_reporte",
        python_callable=decidir_reporte
    )

    detallado = PythonOperator(
        task_id="reporte_detallado",
        python_callable=reporte_detallado
    )

    simple = PythonOperator(
        task_id="reporte_simple",
        python_callable=reporte_simple
    )

    # Punto de convergencia después del branch
    convergencia = DummyOperator(
        task_id="convergencia",
        trigger_rule="none_failed_min_one_success"
    )

    # Dynamic tasks: Notificaciones
    canales = ["email", "slack", "sms"]
    tasks_notificaciones = []

    for canal in canales:
        task = PythonOperator(
            task_id=f"notificar_{canal}",
            python_callable=notificar,
            op_kwargs={"canal": canal}
        )
        tasks_notificaciones.append(task)

    # Consolidación final
    consolidar_task = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar
    )

    fin = DummyOperator(task_id="fin")

    # Dependencias
    inicio >> grupo_ext >> grupo_proc >> decidir
    decidir >> [detallado, simple] >> convergencia

    for task in tasks_notificaciones:
        convergencia >> task

    tasks_notificaciones >> consolidar_task >> fin
```

**Verificación:**

Este DAG integra:
- ✅ TaskGroups (extraccion, procesamiento)
- ✅ XComs (compartir ventas, clientes, total)
- ✅ BranchPythonOperator (decidir tipo de reporte)
- ✅ Dynamic DAG Generation (3 notificaciones)
- ✅ Trigger rules (convergencia, consolidación)

**Flujo visual:**
```
inicio → grupo_extraccion → grupo_procesamiento → decidir_reporte
          (ventas, clientes)  (calcular, contar)      ├──→ reporte_detallado
                                                       └──→ reporte_simple
                                                              ↓
                                                         convergencia
                                                              ↓
                                                    [notificar_email]
                                                    [notificar_slack] → consolidar → fin
                                                    [notificar_sms]
```

Ejecuta el DAG varias veces para ver diferentes flujos según el total de ventas.

</details>

---

## 🎯 Resumen de Ejercicios

### Progresión de Dificultad

| Nivel | Ejercicios | Conceptos Principales |
|-------|------------|----------------------|
| **Básico ⭐** | 1-5 | TaskGroups, XComs simples, Branch 2 caminos, Sensors, Dynamic DAG básico |
| **Intermedio ⭐⭐** | 6-10 | TaskGroups anidados, XComs complejos, Branch 3 caminos, TimeSensor, Dynamic 10 tasks |
| **Avanzado ⭐⭐⭐** | 11-15 | Integración múltiple, ExternalTaskSensor, TriggerDagRun, Dynamic con directorio, Pipeline completo |

---

### 🏆 Checklist de Completitud

Marca los ejercicios que hayas completado:

- [ ] **Ejercicio 1:** TaskGroup con 3 Tasks
- [ ] **Ejercicio 2:** XCom para Pasar un Número
- [ ] **Ejercicio 3:** BranchPythonOperator Simple
- [ ] **Ejercicio 4:** FileSensor con Timeout 30s
- [ ] **Ejercicio 5:** Crear 3 Tasks Dinámicamente
- [ ] **Ejercicio 6:** TaskGroup Anidado
- [ ] **Ejercicio 7:** XComs con Diccionario Completo
- [ ] **Ejercicio 8:** Branch con 3 Caminos
- [ ] **Ejercicio 9:** TimeSensor (Esperar hasta 9 AM)
- [ ] **Ejercicio 10:** Dynamic DAG con 10 Tasks
- [ ] **Ejercicio 11:** Pipeline con TaskGroups + XComs + Branch
- [ ] **Ejercicio 12:** ExternalTaskSensor
- [ ] **Ejercicio 13:** TriggerDagRunOperator con Parámetros
- [ ] **Ejercicio 14:** Dynamic DAG que Lee Directorio
- [ ] **Ejercicio 15:** Pipeline Completo Integrando Todos los Conceptos

---

### 📚 Próximos Pasos

Una vez completados todos los ejercicios:

1. ✅ **Revisa tus soluciones:** Compara con las soluciones proporcionadas
2. ✅ **Experimenta:** Modifica los ejercicios y añade funcionalidades
3. ✅ **Combina conceptos:** Crea tus propios DAGs integrando múltiples conceptos
4. ✅ **Continúa con el Proyecto Práctico:** Aplica todo lo aprendido en un proyecto real

---

**¡Felicitaciones por completar los ejercicios del Tema 2!** 🎉

Has dominado los conceptos intermedios de Apache Airflow. Ahora estás listo para construir pipelines complejos y productivos.

**🚀 Continúa con el Proyecto Práctico para aplicar todo lo aprendido.**
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](proyecto-practico/README.md)
