# 📚 Tema 2: Airflow Intermedio - Ejemplos Prácticos

**Módulo 6: Apache Airflow y Orquestación**
**Nivel:** Intermedio
**Duración estimada:** 2-3 horas
**Prerequisitos:** 01-TEORIA.md completado

---

## 📖 Índice de Ejemplos

1. [Ejemplo 1: TaskGroup Básico](#ejemplo-1-taskgroup-básico-⭐⭐)
2. [Ejemplo 2: XComs - Pasar Datos entre Tasks](#ejemplo-2-xcoms---pasar-datos-entre-tasks-⭐⭐)
3. [Ejemplo 3: BranchPythonOperator - Flujos Condicionales](#ejemplo-3-branchpythonoperator---flujos-condicionales-⭐⭐⭐)
4. [Ejemplo 4: FileSensor - Esperar por Archivos](#ejemplo-4-filesensor---esperar-por-archivos-⭐⭐)
5. [Ejemplo 5: Dynamic DAG - Generar Tasks Dinámicamente](#ejemplo-5-dynamic-dag---generar-tasks-dinámicamente-⭐⭐)

---

## Ejemplo 1: TaskGroup Básico ⭐⭐

### 🎯 Objetivo

Aprender a organizar tasks relacionadas usando **TaskGroups** para mejorar la legibilidad del DAG.

### 📝 Descripción

Crearemos un pipeline ETL simple que:
1. **Extrae** datos de ventas
2. **Procesa** los datos en un TaskGroup con 3 sub-tasks:
   - Validar datos
   - Transformar datos
   - Calcular métricas
3. **Carga** los resultados

### 💻 Código Completo

```python
"""
DAG que demuestra el uso de TaskGroups para organizar un pipeline ETL.

Estructura:
    inicio → grupo_procesamiento → cargar_resultados → fin
              ├─ validar_datos
              ├─ transformar_datos
              └─ calcular_metricas
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime


def extraer_ventas():
    """Simula la extracción de datos de ventas"""
    print("[EXTRAER] Extrayendo datos de ventas desde la base de datos...")
    ventas = [
        {"producto": "Laptop", "cantidad": 3, "precio": 1200},
        {"producto": "Mouse", "cantidad": 10, "precio": 25},
        {"producto": "Teclado", "cantidad": 5, "precio": 75},
    ]
    print(f"[EXTRAER] ✅ Extraídas {len(ventas)} ventas")
    return ventas


def validar_datos(**context):
    """Valida que los datos extraídos tienen el formato correcto"""
    print("[VALIDAR] Validando estructura de datos...")
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="extraer_ventas")

    for venta in ventas:
        assert "producto" in venta, "Falta campo 'producto'"
        assert "cantidad" in venta, "Falta campo 'cantidad'"
        assert "precio" in venta, "Falta campo 'precio'"

    print(f"[VALIDAR] ✅ Validadas {len(ventas)} ventas correctamente")


def transformar_datos(**context):
    """Calcula el total por producto"""
    print("[TRANSFORMAR] Calculando totales por producto...")
    ti = context["ti"]
    ventas = ti.xcom_pull(task_ids="extraer_ventas")

    ventas_transformadas = []
    for venta in ventas:
        total = venta["cantidad"] * venta["precio"]
        ventas_transformadas.append({
            "producto": venta["producto"],
            "total": total
        })

    print(f"[TRANSFORMAR] ✅ Transformadas {len(ventas_transformadas)} ventas")
    return ventas_transformadas


def calcular_metricas(**context):
    """Calcula métricas agregadas"""
    print("[METRICAS] Calculando métricas globales...")
    ti = context["ti"]

    # Leer del grupo: necesitamos especificar el full task_id
    ventas = ti.xcom_pull(task_ids="grupo_procesamiento.transformar_datos")

    total_general = sum(v["total"] for v in ventas)
    num_productos = len(ventas)
    promedio = total_general / num_productos if num_productos > 0 else 0

    metricas = {
        "total_general": total_general,
        "num_productos": num_productos,
        "promedio": promedio
    }

    print(f"[METRICAS] Total General: {total_general}€")
    print(f"[METRICAS] Número de Productos: {num_productos}")
    print(f"[METRICAS] Promedio por Producto: {promedio:.2f}€")

    return metricas


def cargar_resultados(**context):
    """Simula la carga de resultados a una base de datos"""
    print("[CARGAR] Cargando resultados...")
    ti = context["ti"]

    metricas = ti.xcom_pull(task_ids="grupo_procesamiento.calcular_metricas")

    print(f"[CARGAR] ✅ Guardando métricas en BD:")
    print(f"  - Total: {metricas['total_general']}€")
    print(f"  - Productos: {metricas['num_productos']}")
    print(f"  - Promedio: {metricas['promedio']:.2f}€")


# Definición del DAG
with DAG(
    dag_id="ejemplo_01_taskgroup",
    description="Ejemplo de uso de TaskGroups para organizar un ETL",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo", "tema2", "taskgroup"],
) as dag:

    # Task inicial
    inicio = DummyOperator(task_id="inicio")

    # Task de extracción
    extraer = PythonOperator(
        task_id="extraer_ventas",
        python_callable=extraer_ventas
    )

    # TaskGroup para agrupar el procesamiento
    with TaskGroup("grupo_procesamiento") as grupo_procesamiento:

        validar = PythonOperator(
            task_id="validar_datos",
            python_callable=validar_datos
        )

        transformar = PythonOperator(
            task_id="transformar_datos",
            python_callable=transformar_datos
        )

        metricas = PythonOperator(
            task_id="calcular_metricas",
            python_callable=calcular_metricas
        )

        # Dependencias dentro del grupo
        validar >> transformar >> metricas

    # Task de carga
    cargar = PythonOperator(
        task_id="cargar_resultados",
        python_callable=cargar_resultados
    )

    # Task final
    fin = DummyOperator(task_id="fin")

    # Dependencias del DAG
    inicio >> extraer >> grupo_procesamiento >> cargar >> fin
```

### 📊 Ejecución y Resultados

**Cómo ejecutar:**
1. Guardar el código en `dags/ejemplo_01_taskgroup.py`
2. Ir a Airflow UI: http://localhost:8080
3. Buscar el DAG `ejemplo_01_taskgroup`
4. Hacer clic en el botón ▶️ (Trigger DAG)

**Salida esperada en logs:**
```
[EXTRAER] Extrayendo datos de ventas desde la base de datos...
[EXTRAER] ✅ Extraídas 3 ventas
[VALIDAR] Validando estructura de datos...
[VALIDAR] ✅ Validadas 3 ventas correctamente
[TRANSFORMAR] Calculando totales por producto...
[TRANSFORMAR] ✅ Transformadas 3 ventas
[METRICAS] Calculando métricas globales...
[METRICAS] Total General: 4175€
[METRICAS] Número de Productos: 3
[METRICAS] Promedio por Producto: 1391.67€
[CARGAR] Cargando resultados...
[CARGAR] ✅ Guardando métricas en BD:
  - Total: 4175€
  - Productos: 3
  - Promedio: 1391.67€
```

### 🔍 Vista en Airflow UI

**Graph View (colapsado):**
```
inicio → extraer_ventas → [📁 grupo_procesamiento] → cargar_resultados → fin
```

**Graph View (expandido):**
```
inicio → extraer_ventas → grupo_procesamiento.validar_datos
                         → grupo_procesamiento.transformar_datos
                         → grupo_procesamiento.calcular_metricas
                         → cargar_resultados → fin
```

### 💡 Puntos Clave

1. **TaskGroup con context manager:** Usamos `with TaskGroup(...)` para agrupar tasks
2. **Namespace automático:** Las tasks dentro del grupo tienen prefijo `grupo_procesamiento.`
3. **XCom entre grupos:** Para leer XComs de tasks dentro de un grupo, usa el full task_id: `grupo_procesamiento.transformar_datos`
4. **Legibilidad:** El Graph View se ve mucho más limpio con el grupo colapsado

---

## Ejemplo 2: XComs - Pasar Datos entre Tasks ⭐⭐

### 🎯 Objetivo

Aprender a usar **XComs** para compartir datos entre tasks de forma segura y eficiente.

### 📝 Descripción

Crearemos un pipeline que:
1. **Calcula** métricas de ventas y las guarda en XCom
2. **Evalúa** si las métricas superan umbrales definidos
3. **Genera** un reporte usando todos los datos compartidos

### 💻 Código Completo

```python
"""
DAG que demuestra el uso de XComs para compartir datos entre tasks.

Flujo:
    calcular_ventas → evaluar_metricas → generar_reporte → enviar_resumen

XComs compartidos:
    - total_ventas (float)
    - num_ventas (int)
    - promedio_venta (float)
    - supera_objetivo (bool)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import random


def calcular_ventas(**context):
    """
    Calcula métricas de ventas y las guarda en XCom.

    XComs producidos:
        - total_ventas: Suma de todas las ventas
        - num_ventas: Cantidad de ventas procesadas
        - promedio_venta: Promedio por venta
    """
    ti = context["ti"]

    # Simular cálculo de ventas
    num_ventas = random.randint(20, 50)
    ventas = [random.uniform(50, 500) for _ in range(num_ventas)]

    total = sum(ventas)
    promedio = total / num_ventas

    print(f"[CALCULAR] Procesadas {num_ventas} ventas")
    print(f"[CALCULAR] Total: {total:.2f}€")
    print(f"[CALCULAR] Promedio: {promedio:.2f}€")

    # Guardar en XCom con keys específicas
    ti.xcom_push(key="total_ventas", value=total)
    ti.xcom_push(key="num_ventas", value=num_ventas)
    ti.xcom_push(key="promedio_venta", value=promedio)

    # También se puede retornar un valor (se guarda en key "return_value")
    return {
        "mensaje": "Cálculo completado exitosamente",
        "timestamp": str(datetime.now())
    }


def evaluar_metricas(**context):
    """
    Lee métricas de XCom y evalúa si superan los objetivos.

    XComs consumidos:
        - total_ventas
        - num_ventas

    XComs producidos:
        - supera_objetivo: True si se superó el objetivo
        - porcentaje_cumplimiento: % de cumplimiento del objetivo
    """
    ti = context["ti"]

    # Leer XComs de la task anterior
    total = ti.xcom_pull(task_ids="calcular_ventas", key="total_ventas")
    num_ventas = ti.xcom_pull(task_ids="calcular_ventas", key="num_ventas")

    # Definir objetivos
    objetivo_total = 10000
    objetivo_cantidad = 30

    # Evaluar
    supera_total = total >= objetivo_total
    supera_cantidad = num_ventas >= objetivo_cantidad
    supera_objetivo = supera_total and supera_cantidad

    porcentaje = (total / objetivo_total) * 100

    print(f"[EVALUAR] Objetivo de Total: {objetivo_total}€")
    print(f"[EVALUAR] Total Alcanzado: {total:.2f}€ ({porcentaje:.1f}%)")
    print(f"[EVALUAR] Objetivo de Cantidad: {objetivo_cantidad}")
    print(f"[EVALUAR] Cantidad Alcanzada: {num_ventas}")

    if supera_objetivo:
        print(f"[EVALUAR] ✅ ¡OBJETIVO SUPERADO!")
    else:
        print(f"[EVALUAR] ❌ Objetivo no alcanzado")

    # Guardar resultado de evaluación
    ti.xcom_push(key="supera_objetivo", value=supera_objetivo)
    ti.xcom_push(key="porcentaje_cumplimiento", value=porcentaje)


def generar_reporte(**context):
    """
    Genera un reporte consolidado con todos los datos compartidos.

    XComs consumidos:
        - total_ventas
        - num_ventas
        - promedio_venta
        - supera_objetivo
        - porcentaje_cumplimiento
    """
    ti = context["ti"]

    # Leer todos los XComs
    total = ti.xcom_pull(task_ids="calcular_ventas", key="total_ventas")
    num_ventas = ti.xcom_pull(task_ids="calcular_ventas", key="num_ventas")
    promedio = ti.xcom_pull(task_ids="calcular_ventas", key="promedio_venta")
    supera = ti.xcom_pull(task_ids="evaluar_metricas", key="supera_objetivo")
    porcentaje = ti.xcom_pull(task_ids="evaluar_metricas", key="porcentaje_cumplimiento")

    # Generar reporte
    print("="*60)
    print("          REPORTE DE VENTAS - DIARIO")
    print("="*60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    print("MÉTRICAS:")
    print(f"  • Total de Ventas:     {total:>10.2f}€")
    print(f"  • Cantidad de Ventas:  {num_ventas:>10}")
    print(f"  • Promedio por Venta:  {promedio:>10.2f}€")
    print("")
    print("EVALUACIÓN:")
    print(f"  • Cumplimiento:        {porcentaje:>10.1f}%")

    if supera:
        print(f"  • Estado:              {'OBJETIVO CUMPLIDO':>20} ✅")
    else:
        print(f"  • Estado:              {'Objetivo No Cumplido':>20} ❌")

    print("="*60)

    # Retornar resumen (se guarda en XCom automáticamente)
    return {
        "total": total,
        "num_ventas": num_ventas,
        "cumplimiento": porcentaje,
        "exitoso": supera
    }


def enviar_resumen(**context):
    """
    Simula el envío del resumen por email.
    Lee el return_value de la task anterior.
    """
    ti = context["ti"]

    # Leer el return_value de generar_reporte
    resumen = ti.xcom_pull(task_ids="generar_reporte", key="return_value")

    print("[EMAIL] Preparando email...")
    print(f"[EMAIL] Destinatario: gerente@empresa.com")
    print(f"[EMAIL] Asunto: Reporte Diario de Ventas")
    print(f"[EMAIL] Contenido:")
    print(f"  - Total: {resumen['total']:.2f}€")
    print(f"  - Ventas: {resumen['num_ventas']}")
    print(f"  - Cumplimiento: {resumen['cumplimiento']:.1f}%")
    print(f"  - Exitoso: {'Sí' if resumen['exitoso'] else 'No'}")
    print(f"[EMAIL] ✅ Email enviado exitosamente")


# Definición del DAG
with DAG(
    dag_id="ejemplo_02_xcoms",
    description="Ejemplo de uso de XComs para compartir datos entre tasks",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo", "tema2", "xcoms"],
) as dag:

    calcular = PythonOperator(
        task_id="calcular_ventas",
        python_callable=calcular_ventas
    )

    evaluar = PythonOperator(
        task_id="evaluar_metricas",
        python_callable=evaluar_metricas
    )

    reportar = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte
    )

    enviar = PythonOperator(
        task_id="enviar_resumen",
        python_callable=enviar_resumen
    )

    calcular >> evaluar >> reportar >> enviar
```

### 📊 Ejecución y Resultados

**Salida esperada en logs:**
```
[CALCULAR] Procesadas 37 ventas
[CALCULAR] Total: 11234.56€
[CALCULAR] Promedio: 303.64€

[EVALUAR] Objetivo de Total: 10000€
[EVALUAR] Total Alcanzado: 11234.56€ (112.3%)
[EVALUAR] Objetivo de Cantidad: 30
[EVALUAR] Cantidad Alcanzada: 37
[EVALUAR] ✅ ¡OBJETIVO SUPERADO!

============================================================
          REPORTE DE VENTAS - DIARIO
============================================================
Fecha: 2025-01-27 14:30:45

MÉTRICAS:
  • Total de Ventas:       11234.56€
  • Cantidad de Ventas:           37
  • Promedio por Venta:       303.64€

EVALUACIÓN:
  • Cumplimiento:              112.3%
  • Estado:          OBJETIVO CUMPLIDO ✅
============================================================

[EMAIL] Preparando email...
[EMAIL] ✅ Email enviado exitosamente
```

### 💡 Puntos Clave

1. **xcom_push con keys:** Usa keys descriptivas para múltiples valores
2. **xcom_pull específico:** Lee XComs especificando `task_ids` y `key`
3. **return automático:** Si retornas un valor, se guarda en key `return_value`
4. **Tipos serializables:** Usa dict, list, int, float, str, bool (serializables en JSON)
5. **Documentación:** Documenta qué XComs produce/consume cada función

---

## Ejemplo 3: BranchPythonOperator - Flujos Condicionales ⭐⭐⭐

### 🎯 Objetivo

Aprender a crear **flujos condicionales** (if-else) en DAGs usando **BranchPythonOperator**.

### 📝 Descripción

Crearemos un pipeline que:
1. **Calcula** el total de ventas
2. **Decide** qué procesamiento aplicar según el monto:
   - Si ventas > 15,000€ → Procesamiento PREMIUM
   - Si ventas ≤ 15,000€ → Procesamiento NORMAL
3. **Consolida** los resultados (join)

### 💻 Código Completo

```python
"""
DAG que demuestra el uso de BranchPythonOperator para flujos condicionales.

Flujo:
    inicio → calcular_ventas → decidir_procesamiento
                                    ├──→ (ventas > 15000) procesar_premium → alerta_gerente
                                    └──→ (ventas ≤ 15000) procesar_normal → guardar_log
                                                                                    ↓
                                                                        consolidar_resultados → fin
"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
import random


def calcular_ventas():
    """Simula el cálculo de ventas totales"""
    total = random.uniform(8000, 20000)
    print(f"[CALCULAR] Total de ventas calculado: {total:.2f}€")
    return total


def decidir_procesamiento(**context):
    """
    Función de branching que decide qué camino tomar.

    Retorna:
        - "procesar_premium" si ventas > 15000
        - "procesar_normal" si ventas ≤ 15000
    """
    ti = context["ti"]
    total_ventas = ti.xcom_pull(task_ids="calcular_ventas")

    umbral = 15000

    print(f"[BRANCH] Total de ventas: {total_ventas:.2f}€")
    print(f"[BRANCH] Umbral: {umbral:.2f}€")

    if total_ventas > umbral:
        print(f"[BRANCH] ✅ Ventas superan umbral → Ruta PREMIUM")
        return "procesar_premium"
    else:
        print(f"[BRANCH] 📝 Ventas no superan umbral → Ruta NORMAL")
        return "procesar_normal"


def procesar_premium(**context):
    """Procesamiento para ventas PREMIUM (altas)"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="calcular_ventas")

    print("="*60)
    print("🌟 PROCESAMIENTO PREMIUM 🌟")
    print("="*60)
    print(f"Total de Ventas: {total:.2f}€")
    print("Aplicando descuentos exclusivos...")
    print("Calculando comisiones especiales...")
    print("Actualizando ranking de clientes VIP...")
    print("✅ Procesamiento PREMIUM completado")
    print("="*60)

    return {"tipo": "premium", "total": total, "descuento": 0.15}


def alerta_gerente(**context):
    """Envía alerta al gerente sobre ventas altas"""
    ti = context["ti"]
    resultado = ti.xcom_pull(task_ids="procesar_premium")

    print("[ALERTA] 📧 Enviando alerta al gerente...")
    print(f"[ALERTA] Asunto: ¡Ventas excepcionales del día!")
    print(f"[ALERTA] Total: {resultado['total']:.2f}€")
    print(f"[ALERTA] Descuento aplicado: {resultado['descuento']*100}%")
    print("[ALERTA] ✅ Alerta enviada exitosamente")


def procesar_normal(**context):
    """Procesamiento para ventas NORMALES"""
    ti = context["ti"]
    total = ti.xcom_pull(task_ids="calcular_ventas")

    print("="*60)
    print("📋 PROCESAMIENTO NORMAL")
    print("="*60)
    print(f"Total de Ventas: {total:.2f}€")
    print("Aplicando proceso estándar...")
    print("Calculando comisiones regulares...")
    print("✅ Procesamiento NORMAL completado")
    print("="*60)

    return {"tipo": "normal", "total": total, "descuento": 0.05}


def guardar_log(**context):
    """Guarda un log de las ventas normales"""
    ti = context["ti"]
    resultado = ti.xcom_pull(task_ids="procesar_normal")

    print("[LOG] 📝 Guardando log de ventas...")
    print(f"[LOG] Tipo: {resultado['tipo']}")
    print(f"[LOG] Total: {resultado['total']:.2f}€")
    print(f"[LOG] Descuento: {resultado['descuento']*100}%")
    print("[LOG] ✅ Log guardado en /logs/ventas.log")


def consolidar_resultados(**context):
    """
    Consolida los resultados de ambos caminos.

    Nota: Esta task tiene trigger_rule="none_failed_min_one_success"
    para que se ejecute incluso si una de las rutas fue saltada.
    """
    ti = context["ti"]

    print("[CONSOLIDAR] Consolidando resultados...")

    # Intentar leer de ambos caminos
    resultado_premium = ti.xcom_pull(task_ids="procesar_premium")
    resultado_normal = ti.xcom_pull(task_ids="procesar_normal")

    if resultado_premium is not None:
        print(f"[CONSOLIDAR] Ruta PREMIUM ejecutada")
        print(f"[CONSOLIDAR]   - Total: {resultado_premium['total']:.2f}€")
        print(f"[CONSOLIDAR]   - Descuento: {resultado_premium['descuento']*100}%")

    if resultado_normal is not None:
        print(f"[CONSOLIDAR] Ruta NORMAL ejecutada")
        print(f"[CONSOLIDAR]   - Total: {resultado_normal['total']:.2f}€")
        print(f"[CONSOLIDAR]   - Descuento: {resultado_normal['descuento']*100}%")

    print("[CONSOLIDAR] ✅ Consolidación completada")


# Definición del DAG
with DAG(
    dag_id="ejemplo_03_branching",
    description="Ejemplo de uso de BranchPythonOperator para flujos condicionales",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo", "tema2", "branching"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    calcular = PythonOperator(
        task_id="calcular_ventas",
        python_callable=calcular_ventas
    )

    # BranchPythonOperator - decide qué camino tomar
    decidir = BranchPythonOperator(
        task_id="decidir_procesamiento",
        python_callable=decidir_procesamiento
    )

    # Ruta PREMIUM
    premium = PythonOperator(
        task_id="procesar_premium",
        python_callable=procesar_premium
    )

    alerta = PythonOperator(
        task_id="alerta_gerente",
        python_callable=alerta_gerente
    )

    # Ruta NORMAL
    normal = PythonOperator(
        task_id="procesar_normal",
        python_callable=procesar_normal
    )

    log = PythonOperator(
        task_id="guardar_log",
        python_callable=guardar_log
    )

    # Consolidación (join)
    consolidar = PythonOperator(
        task_id="consolidar_resultados",
        python_callable=consolidar_resultados,
        trigger_rule="none_failed_min_one_success"  # ← Importante!
    )

    fin = DummyOperator(task_id="fin")

    # Dependencias
    inicio >> calcular >> decidir
    decidir >> premium >> alerta >> consolidar
    decidir >> normal >> log >> consolidar
    consolidar >> fin
```

### 📊 Ejecución y Resultados

**Escenario 1: Ventas Altas (>15,000€)**
```
[CALCULAR] Total de ventas calculado: 17543.21€
[BRANCH] Total de ventas: 17543.21€
[BRANCH] Umbral: 15000.00€
[BRANCH] ✅ Ventas superan umbral → Ruta PREMIUM

============================================================
🌟 PROCESAMIENTO PREMIUM 🌟
============================================================
Total de Ventas: 17543.21€
Aplicando descuentos exclusivos...
Calculando comisiones especiales...
Actualizando ranking de clientes VIP...
✅ Procesamiento PREMIUM completado
============================================================

[ALERTA] 📧 Enviando alerta al gerente...
[ALERTA] Asunto: ¡Ventas excepcionales del día!
[ALERTA] Total: 17543.21€
[ALERTA] Descuento aplicado: 15.0%
[ALERTA] ✅ Alerta enviada exitosamente

[CONSOLIDAR] Consolidando resultados...
[CONSOLIDAR] Ruta PREMIUM ejecutada
[CONSOLIDAR]   - Total: 17543.21€
[CONSOLIDAR]   - Descuento: 15.0%
[CONSOLIDAR] ✅ Consolidación completada
```

**Estados de las tasks:**
- ✅ inicio: success
- ✅ calcular_ventas: success
- ✅ decidir_procesamiento: success (retornó "procesar_premium")
- ✅ procesar_premium: success
- ✅ alerta_gerente: success
- ⏭️ procesar_normal: **skipped** (no ejecutada)
- ⏭️ guardar_log: **skipped** (no ejecutada)
- ✅ consolidar_resultados: success
- ✅ fin: success

---

**Escenario 2: Ventas Normales (≤15,000€)**
```
[CALCULAR] Total de ventas calculado: 12345.67€
[BRANCH] Total de ventas: 12345.67€
[BRANCH] Umbral: 15000.00€
[BRANCH] 📝 Ventas no superan umbral → Ruta NORMAL

============================================================
📋 PROCESAMIENTO NORMAL
============================================================
Total de Ventas: 12345.67€
Aplicando proceso estándar...
Calculando comisiones regulares...
✅ Procesamiento NORMAL completado
============================================================

[LOG] 📝 Guardando log de ventas...
[LOG] Tipo: normal
[LOG] Total: 12345.67€
[LOG] Descuento: 5.0%
[LOG] ✅ Log guardado en /logs/ventas.log

[CONSOLIDAR] Consolidando resultados...
[CONSOLIDAR] Ruta NORMAL ejecutada
[CONSOLIDAR]   - Total: 12345.67€
[CONSOLIDAR]   - Descuento: 5.0%
[CONSOLIDAR] ✅ Consolidación completada
```

**Estados de las tasks:**
- ✅ inicio: success
- ✅ calcular_ventas: success
- ✅ decidir_procesamiento: success (retornó "procesar_normal")
- ⏭️ procesar_premium: **skipped**
- ⏭️ alerta_gerente: **skipped**
- ✅ procesar_normal: success
- ✅ guardar_log: success
- ✅ consolidar_resultados: success
- ✅ fin: success

### 💡 Puntos Clave

1. **BranchPythonOperator:** La función debe retornar el `task_id` a ejecutar
2. **Tasks saltadas:** Las rutas no elegidas se marcan como "skipped"
3. **Trigger rule:** La task de consolidación necesita `trigger_rule="none_failed_min_one_success"` para ejecutarse aunque haya tasks saltadas
4. **Múltiples caminos:** Puedes tener 2, 3 o más rutas diferentes
5. **Logging:** Siempre loggea qué camino se tomó y por qué

---

## Ejemplo 4: FileSensor - Esperar por Archivos ⭐⭐

### 🎯 Objetivo

Aprender a usar **FileSensor** para esperar por la llegada de archivos antes de procesarlos.

### 📝 Descripción

Crearemos un pipeline que:
1. **Espera** hasta que un archivo CSV aparezca en el sistema
2. **Procesa** el archivo una vez que está disponible
3. **Limpia** los archivos temporales

### 💻 Código Completo

```python
"""
DAG que demuestra el uso de FileSensor para esperar por archivos.

Flujo:
    preparar_directorio → esperar_datos → procesar_archivo → limpiar_temporales

Prerequisito:
    - Crear el archivo /tmp/datos_ventas.csv para que el sensor lo detecte
"""

from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pandas as pd
from pathlib import Path


def preparar_directorio():
    """Prepara el directorio para recibir archivos"""
    directorio = Path("/tmp")
    directorio.mkdir(exist_ok=True)

    print(f"[PREPARAR] Directorio preparado: {directorio}")
    print(f"[PREPARAR] Esperando archivo: /tmp/datos_ventas.csv")
    print("[PREPARAR] Para simular la llegada del archivo, ejecuta:")
    print("  echo 'producto,cantidad,precio' > /tmp/datos_ventas.csv")
    print("  echo 'Laptop,3,1200' >> /tmp/datos_ventas.csv")
    print("  echo 'Mouse,10,25' >> /tmp/datos_ventas.csv")


def procesar_archivo():
    """Procesa el archivo CSV una vez que ha llegado"""
    ruta_archivo = "/tmp/datos_ventas.csv"

    print(f"[PROCESAR] ✅ Archivo detectado: {ruta_archivo}")
    print(f"[PROCESAR] Leyendo archivo...")

    try:
        df = pd.read_csv(ruta_archivo)

        print(f"[PROCESAR] Filas encontradas: {len(df)}")
        print(f"[PROCESAR] Columnas: {list(df.columns)}")
        print("")
        print("[PROCESAR] Contenido:")
        print(df.to_string(index=False))
        print("")

        # Calcular total
        if 'cantidad' in df.columns and 'precio' in df.columns:
            df['total'] = df['cantidad'] * df['precio']
            total_general = df['total'].sum()
            print(f"[PROCESAR] Total General: {total_general:.2f}€")

        print("[PROCESAR] ✅ Procesamiento completado")

    except Exception as e:
        print(f"[PROCESAR] ❌ Error al procesar archivo: {e}")
        raise


def limpiar_temporales():
    """Limpia los archivos temporales"""
    ruta_archivo = Path("/tmp/datos_ventas.csv")

    if ruta_archivo.exists():
        ruta_archivo.unlink()
        print(f"[LIMPIAR] ✅ Archivo eliminado: {ruta_archivo}")
    else:
        print(f"[LIMPIAR] ⚠️ Archivo no encontrado: {ruta_archivo}")


# Definición del DAG
with DAG(
    dag_id="ejemplo_04_filesensor",
    description="Ejemplo de uso de FileSensor para esperar por archivos",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo", "tema2", "sensor"],
) as dag:

    preparar = PythonOperator(
        task_id="preparar_directorio",
        python_callable=preparar_directorio
    )

    # FileSensor - espera hasta que el archivo exista
    esperar = FileSensor(
        task_id="esperar_datos",
        filepath="/tmp/datos_ventas.csv",
        poke_interval=10,  # Verificar cada 10 segundos
        timeout=120,  # Esperar máximo 2 minutos
        mode="reschedule",  # No bloquear el worker
        soft_fail=False  # Fallar el DAG si timeout
    )

    procesar = PythonOperator(
        task_id="procesar_archivo",
        python_callable=procesar_archivo
    )

    limpiar = PythonOperator(
        task_id="limpiar_temporales",
        python_callable=limpiar_temporales
    )

    preparar >> esperar >> procesar >> limpiar
```

### 📊 Cómo Probar

**Paso 1: Ejecutar el DAG**
1. Guardar el código en `dags/ejemplo_04_filesensor.py`
2. Ir a Airflow UI: http://localhost:8080
3. Trigger el DAG `ejemplo_04_filesensor`

**Paso 2: Crear el archivo (en otra terminal)**

Mientras el sensor está esperando, crea el archivo:

```bash
# En Linux/Mac:
echo 'producto,cantidad,precio' > /tmp/datos_ventas.csv
echo 'Laptop,3,1200' >> /tmp/datos_ventas.csv
echo 'Mouse,10,25' >> /tmp/datos_ventas.csv
echo 'Teclado,5,75' >> /tmp/datos_ventas.csv

# En Windows (PowerShell):
"producto,cantidad,precio" | Out-File -FilePath C:\Temp\datos_ventas.csv
"Laptop,3,1200" | Out-File -Append -FilePath C:\Temp\datos_ventas.csv
"Mouse,10,25" | Out-File -Append -FilePath C:\Temp\datos_ventas.csv
"Teclado,5,75" | Out-File -Append -FilePath C:\Temp\datos_ventas.csv
```

**Paso 3: Ver los Resultados**

El sensor detectará el archivo y continuará con el procesamiento:

```
[PREPARAR] Directorio preparado: /tmp
[PREPARAR] Esperando archivo: /tmp/datos_ventas.csv

[SENSOR] Esperando archivo... (intento 1)
[SENSOR] Esperando archivo... (intento 2)
[SENSOR] ✅ Archivo detectado!

[PROCESAR] ✅ Archivo detectado: /tmp/datos_ventas.csv
[PROCESAR] Leyendo archivo...
[PROCESAR] Filas encontradas: 3
[PROCESAR] Columnas: ['producto', 'cantidad', 'precio']

[PROCESAR] Contenido:
 producto  cantidad  precio
   Laptop         3    1200
    Mouse        10      25
  Teclado         5      75

[PROCESAR] Total General: 4175.00€
[PROCESAR] ✅ Procesamiento completado

[LIMPIAR] ✅ Archivo eliminado: /tmp/datos_ventas.csv
```

### 💡 Puntos Clave

1. **Poke interval:** `poke_interval=10` verifica cada 10 segundos
2. **Timeout:** `timeout=120` espera máximo 2 minutos antes de fallar
3. **Mode reschedule:** `mode="reschedule"` libera el worker entre verificaciones
4. **Soft fail:** `soft_fail=False` hace que el DAG falle si el archivo no llega (ajusta según necesidad)
5. **Uso real:** En producción, archivos externos (SFTP, S3, etc.) llegan periódicamente

---

## Ejemplo 5: Dynamic DAG - Generar Tasks Dinámicamente ⭐⭐

### 🎯 Objetivo

Aprender a **generar tasks dinámicamente** usando bucles para procesar múltiples items sin código repetitivo.

### 📝 Descripción

Crearemos un pipeline que:
1. **Procesa** 5 regiones de España en paralelo
2. **Consolida** los resultados de todas las regiones
3. **Genera** un reporte final

### 💻 Código Completo

```python
"""
DAG que demuestra la generación dinámica de tasks.

Flujo:
    inicio → [procesar_madrid, procesar_barcelona, ..., procesar_valencia] → consolidar → generar_reporte → fin

    5 tasks de procesamiento se crean dinámicamente en paralelo
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
import random


def procesar_region(region: str, **context):
    """
    Procesa los datos de una región específica.

    Args:
        region: Nombre de la región a procesar
    """
    ti = context["ti"]

    # Simular procesamiento de datos
    num_ventas = random.randint(50, 200)
    total_ventas = random.uniform(5000, 20000)
    promedio = total_ventas / num_ventas

    print(f"[{region.upper()}] Procesando datos de la región {region}")
    print(f"[{region.upper()}] Número de ventas: {num_ventas}")
    print(f"[{region.upper()}] Total de ventas: {total_ventas:.2f}€")
    print(f"[{region.upper()}] Promedio por venta: {promedio:.2f}€")
    print(f"[{region.upper()}] ✅ Procesamiento completado")

    # Retornar resultado para consolidación
    return {
        "region": region,
        "num_ventas": num_ventas,
        "total": total_ventas,
        "promedio": promedio
    }


def consolidar_resultados(**context):
    """Consolida los resultados de todas las regiones"""
    ti = context["ti"]

    regiones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]

    print("[CONSOLIDAR] Consolidando resultados de todas las regiones...")
    print("="*70)

    resultados = []
    total_general = 0
    ventas_totales = 0

    for region in regiones:
        task_id = f"procesar_{region.lower()}"
        resultado = ti.xcom_pull(task_ids=task_id)

        if resultado:
            resultados.append(resultado)
            total_general += resultado["total"]
            ventas_totales += resultado["num_ventas"]

            print(f"{region:15} | Ventas: {resultado['num_ventas']:4} | "
                  f"Total: {resultado['total']:>10.2f}€ | "
                  f"Promedio: {resultado['promedio']:>7.2f}€")

    print("="*70)
    print(f"{'TOTAL':15} | Ventas: {ventas_totales:4} | "
          f"Total: {total_general:>10.2f}€ | "
          f"Promedio: {(total_general/ventas_totales):>7.2f}€")
    print("="*70)

    print(f"[CONSOLIDAR] ✅ Consolidadas {len(resultados)} regiones")

    return {
        "regiones": len(resultados),
        "total_ventas": ventas_totales,
        "total_general": total_general,
        "promedio_general": total_general / ventas_totales if ventas_totales > 0 else 0
    }


def generar_reporte(**context):
    """Genera un reporte final con los datos consolidados"""
    ti = context["ti"]
    consolidado = ti.xcom_pull(task_ids="consolidar")

    print("")
    print("╔"+"═"*68+"╗")
    print("║" + " "*20 + "REPORTE NACIONAL DE VENTAS" + " "*22 + "║")
    print("╠"+"═"*68+"╣")
    print(f"║ Fecha:            {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):45} ║")
    print(f"║ Regiones:         {consolidado['regiones']:45} ║")
    print(f"║ Ventas Totales:   {consolidado['total_ventas']:45} ║")
    print(f"║ Facturación:      {consolidado['total_general']:>43.2f}€ ║")
    print(f"║ Promedio:         {consolidado['promedio_general']:>43.2f}€ ║")
    print("╚"+"═"*68+"╝")
    print("")
    print("[REPORTE] ✅ Reporte generado exitosamente")


# Definición del DAG
with DAG(
    dag_id="ejemplo_05_dynamic_dag",
    description="Ejemplo de generación dinámica de tasks",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo", "tema2", "dynamic"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    # Lista de regiones a procesar
    regiones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]

    # Generar tasks dinámicamente
    tasks_procesamiento = []

    for region in regiones:
        task = PythonOperator(
            task_id=f"procesar_{region.lower()}",
            python_callable=procesar_region,
            op_kwargs={"region": region}
        )
        tasks_procesamiento.append(task)

        # Conectar inicio → task
        inicio >> task

    # Tasks de consolidación y reporte
    consolidar = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar_resultados
    )

    reportar = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte
    )

    fin = DummyOperator(task_id="fin")

    # Conectar todas las tasks de procesamiento → consolidar
    tasks_procesamiento >> consolidar >> reportar >> fin
```

### 📊 Ejecución y Resultados

**Salida esperada:**
```
[MADRID] Procesando datos de la región Madrid
[MADRID] Número de ventas: 142
[MADRID] Total de ventas: 15234.56€
[MADRID] Promedio por venta: 107.28€
[MADRID] ✅ Procesamiento completado

[BARCELONA] Procesando datos de la región Barcelona
[BARCELONA] Número de ventas: 178
[BARCELONA] Total de ventas: 18765.43€
[BARCELONA] Promedio por venta: 105.42€
[BARCELONA] ✅ Procesamiento completado

[VALENCIA] Procesando datos de la región Valencia
[VALENCIA] Número de ventas: 95
[VALENCIA] Total de ventas: 9876.54€
[VALENCIA] Promedio por venta: 103.96€
[VALENCIA] ✅ Procesamiento completado

[SEVILLA] Procesando datos de la región Sevilla
[SEVILLA] Número de ventas: 123
[SEVILLA] Total de ventas: 12345.67€
[SEVILLA] Promedio por venta: 100.37€
[SEVILLA] ✅ Procesamiento completado

[BILBAO] Procesando datos de la región Bilbao
[BILBAO] Número de ventas: 87
[BILBAO] Total de ventas: 8765.43€
[BILBAO] Promedio por venta: 100.75€
[BILBAO] ✅ Procesamiento completado

[CONSOLIDAR] Consolidando resultados de todas las regiones...
======================================================================
Madrid          | Ventas:  142 | Total:   15234.56€ | Promedio:  107.28€
Barcelona       | Ventas:  178 | Total:   18765.43€ | Promedio:  105.42€
Valencia        | Ventas:   95 | Total:    9876.54€ | Promedio:  103.96€
Sevilla         | Ventas:  123 | Total:   12345.67€ | Promedio:  100.37€
Bilbao          | Ventas:   87 | Total:    8765.43€ | Promedio:  100.75€
======================================================================
TOTAL           | Ventas:  625 | Total:   64987.63€ | Promedio:  103.98€
======================================================================
[CONSOLIDAR] ✅ Consolidadas 5 regiones

╔════════════════════════════════════════════════════════════════════╗
║                    REPORTE NACIONAL DE VENTAS                      ║
╠════════════════════════════════════════════════════════════════════╣
║ Fecha:            2025-01-27 15:45:30                              ║
║ Regiones:         5                                                ║
║ Ventas Totales:   625                                              ║
║ Facturación:                                           64987.63€   ║
║ Promedio:                                                103.98€   ║
╚════════════════════════════════════════════════════════════════════╝

[REPORTE] ✅ Reporte generado exitosamente
```

### 🔍 Vista en Airflow UI (Graph View)

```
inicio → [procesar_madrid]
      → [procesar_barcelona]
      → [procesar_valencia]     → consolidar → generar_reporte → fin
      → [procesar_sevilla]
      → [procesar_bilbao]
```

Las 5 tasks de procesamiento se ejecutan **en paralelo**, y solo cuando todas terminan, se ejecuta la consolidación.

### 💡 Puntos Clave

1. **Lista de items:** Define una lista clara de los items a procesar
2. **Bucle for:** Genera tasks dinámicamente con un bucle
3. **op_kwargs:** Pasa parámetros específicos a cada task con `op_kwargs`
4. **Task IDs únicos:** Usa f-strings para crear IDs únicos: `f"procesar_{region}"`
5. **Dependencias dinámicas:** Conecta las tasks generadas con `>>` dentro del bucle
6. **Consolidación:** La task de consolidación lee los XComs de todas las tasks dinámicas
7. **Escalabilidad:** Si mañana son 10 regiones, solo cambias la lista

---

## 🎯 Resumen de Ejemplos

### Conceptos Cubiertos

| Ejemplo | Concepto Principal | Dificultad | Tiempo Estimado |
|---------|-------------------|------------|-----------------|
| Ejemplo 1 | TaskGroups | ⭐⭐ | 20 min |
| Ejemplo 2 | XComs | ⭐⭐ | 20 min |
| Ejemplo 3 | BranchPythonOperator | ⭐⭐⭐ | 25 min |
| Ejemplo 4 | FileSensor | ⭐⭐ | 20 min |
| Ejemplo 5 | Dynamic DAG Generation | ⭐⭐ | 15 min |

---

### 🚀 Próximos Pasos

Ahora que has visto los ejemplos prácticos, es momento de **practicar por tu cuenta**:

1. **Ejecuta todos los ejemplos** en tu entorno de Airflow local
2. **Modifica los ejemplos:** Cambia parámetros, añade funcionalidades
3. **Combina conceptos:** Crea un DAG que use TaskGroups + XComs + Branching
4. **Continúa con 03-EJERCICIOS.md:** Practica con 15 ejercicios graduados

---

**¡Felicitaciones por completar los ejemplos del Tema 2!** 🎉
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
