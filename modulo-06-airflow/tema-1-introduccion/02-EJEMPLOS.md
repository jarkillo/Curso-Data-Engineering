# Ejemplos Prácticos: Introducción a Apache Airflow

**Tiempo estimado:** 90-120 minutos
**Prerequisitos:** Haber leído `01-TEORIA.md` y tener Airflow corriendo

---

## 📋 Índice de Ejemplos

1. [Ejemplo 1: DAG Básico "Hola Mundo" ⭐](#ejemplo-1-dag-básico-hola-mundo-)
2. [Ejemplo 2: Pipeline ETL Simple (Extract → Transform → Load) ⭐⭐](#ejemplo-2-pipeline-etl-simple-extract--transform--load-)
3. [Ejemplo 3: Pipeline con BashOperator ⭐](#ejemplo-3-pipeline-con-bashoperator-)
4. [Ejemplo 4: Dependencias en Paralelo (Fan-out, Fan-in) ⭐⭐](#ejemplo-4-dependencias-en-paralelo-fan-out-fan-in-)
5. [Ejemplo 5: Schedule con Cron ⭐⭐](#ejemplo-5-schedule-con-cron-)

---

## Ejemplo 1: DAG Básico "Hola Mundo" ⭐

**Nivel:** Principiante
**Duración:** 15 minutos
**Objetivo:** Crear tu primer DAG funcional

### Contexto

Trabajas en **DataFlow Industries** y necesitas verificar que Airflow está configurado correctamente. La mejor forma es crear un DAG simple que imprima un mensaje.

### Paso 1: Crear el Archivo del DAG

Crea `airflow/dags/ejemplo_01_hola_mundo.py`:

```python
"""
DAG Ejemplo 1: Hola Mundo
Autor: Tu Nombre
Empresa: DataFlow Industries
Descripción: DAG simple para verificar que Airflow funciona correctamente
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def saludar():
    """
    Función simple que imprime un saludo.
    """
    nombre = "Data Engineer"
    empresa = "DataFlow Industries"

    mensaje = f"¡Hola {nombre}!"
    mensaje += f"\nBienvenido a {empresa}"
    mensaje += f"\nAirflow está funcionando correctamente ✅"

    print(mensaje)
    return "Saludo completado exitosamente"


# Definir el DAG
with DAG(
    dag_id="ejemplo_01_hola_mundo",
    description="DAG simple para verificar configuración de Airflow",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # Solo ejecución manual
    catchup=False,
    tags=["tutorial", "ejemplo", "nivel-basico"],
) as dag:

    # Crear la tarea
    task_saludar = PythonOperator(
        task_id="saludar",
        python_callable=saludar,
    )
```

### Paso 2: Guardar y Verificar

1. Guarda el archivo
2. Espera 30-60 segundos (Airflow detecta nuevos DAGs automáticamente)
3. Ve a http://localhost:8080
4. Busca "ejemplo_01_hola_mundo" en la lista

### Paso 3: Ejecutar el DAG

1. Haz clic en el botón **▶️ (play)** a la derecha del DAG
2. Confirma "Trigger DAG"
3. Espera unos segundos
4. Verás un círculo **verde** (éxito) en la columna "Runs"

### Paso 4: Ver los Logs

1. Haz clic en el nombre del DAG "ejemplo_01_hola_mundo"
2. Verás el **Graph View** con un cuadro "saludar"
3. Haz clic en el cuadro "saludar"
4. Haz clic en "Logs"

### Resultado Esperado

En los logs verás:

```
[INFO] - ¡Hola Data Engineer!
[INFO] - Bienvenido a DataFlow Industries
[INFO] - Airflow está funcionando correctamente ✅
[INFO] - Función retornó: Saludo completado exitosamente
```

### Interpretación

Este DAG simple confirma que:
- ✅ Airflow puede detectar nuevos DAGs
- ✅ El Scheduler está ejecutando tareas
- ✅ Puedes ver logs correctamente
- ✅ Las funciones Python se ejecutan dentro de Airflow

**Siguiente nivel:** Ahora que sabes que funciona, vamos a algo más útil.

---

## Ejemplo 2: Pipeline ETL Simple (Extract → Transform → Load) ⭐⭐

**Nivel:** Intermedio
**Duración:** 20 minutos
**Objetivo:** Crear un pipeline ETL completo con 3 pasos

### Contexto

Tu cliente **RestaurantData Co.** tiene un archivo CSV con las ventas del día. Necesitan:
1. **Extraer** los datos del CSV
2. **Transformar** calculando el total por producto
3. **Cargar** el resultado en un nuevo CSV para el reporte

### Paso 1: Crear Datos de Prueba

Primero, crea un archivo `airflow/dags/data/ventas_dia.csv`:

```csv
producto,cantidad,precio_unitario
Hamburguesa,15,8.50
Pizza,23,12.00
Ensalada,8,6.00
Refresco,35,2.50
Hamburguesa,10,8.50
Pizza,18,12.00
```

### Paso 2: Crear el DAG ETL

Crea `airflow/dags/ejemplo_02_etl_simple.py`:

```python
"""
DAG Ejemplo 2: Pipeline ETL Simple
Cliente: RestaurantData Co.
Descripción: Procesa ventas diarias: Extract → Transform → Load
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os


def extract():
    """
    EXTRACT: Lee el archivo CSV de ventas
    """
    # Ruta relativa al directorio de DAGs
    ruta_archivo = os.path.join(os.path.dirname(__file__), "data", "ventas_dia.csv")

    print(f"📥 Extrayendo datos de: {ruta_archivo}")

    # Leer CSV
    df = pd.read_csv(ruta_archivo)

    print(f"✅ Datos extraídos: {len(df)} filas")
    print(f"Columnas: {list(df.columns)}")
    print(f"Primeras filas:\n{df.head()}")

    # Guardar temporalmente para la siguiente tarea
    df.to_csv("/tmp/ventas_raw.csv", index=False)

    return f"Extraídas {len(df)} filas"


def transform():
    """
    TRANSFORM: Calcula total por producto (cantidad * precio)
    """
    print("🔧 Transformando datos...")

    # Leer datos de la etapa anterior
    df = pd.read_csv("/tmp/ventas_raw.csv")

    # Calcular total por fila
    df["total"] = df["cantidad"] * df["precio_unitario"]

    # Agrupar por producto y sumar
    df_agrupado = df.groupby("producto").agg({
        "cantidad": "sum",
        "total": "sum"
    }).reset_index()

    # Renombrar columnas
    df_agrupado.columns = ["producto", "cantidad_total", "ventas_total"]

    # Ordenar por ventas (mayor a menor)
    df_agrupado = df_agrupado.sort_values("ventas_total", ascending=False)

    print(f"✅ Transformación completada")
    print(f"Productos únicos: {len(df_agrupado)}")
    print(f"Resultado:\n{df_agrupado}")

    # Guardar para la siguiente tarea
    df_agrupado.to_csv("/tmp/ventas_transformed.csv", index=False)

    return f"Procesados {len(df_agrupado)} productos"


def load():
    """
    LOAD: Guarda el resultado final
    """
    print("📤 Cargando resultado final...")

    # Leer datos transformados
    df = pd.read_csv("/tmp/ventas_transformed.csv")

    # Guardar en la ubicación final
    ruta_salida = os.path.join(os.path.dirname(__file__), "data", "reporte_ventas.csv")
    df.to_csv(ruta_salida, index=False)

    print(f"✅ Resultado guardado en: {ruta_salida}")
    print(f"Total registros: {len(df)}")

    # Mostrar resumen
    total_ventas = df["ventas_total"].sum()
    print(f"\n💰 Resumen del día:")
    print(f"   Total ventas: ${total_ventas:.2f}")
    print(f"   Productos vendidos: {len(df)}")

    return f"Reporte guardado con {len(df)} productos"


# Definir el DAG
with DAG(
    dag_id="ejemplo_02_etl_simple",
    description="Pipeline ETL para procesar ventas de RestaurantData Co.",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # Ejecución manual por ahora
    catchup=False,
    tags=["tutorial", "etl", "restaurantdata"],
) as dag:

    # Definir las 3 tareas del pipeline
    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    # Definir el flujo: Extract → Transform → Load
    task_extract >> task_transform >> task_load
```

### Paso 3: Ejecutar el Pipeline

1. Guarda ambos archivos (CSV y DAG)
2. Espera a que Airflow detecte el DAG
3. Ejecuta "ejemplo_02_etl_simple"
4. Observa el Graph View: verás 3 cuadros conectados en línea

### Resultado

Después de ejecutarse, tendrás un nuevo archivo `reporte_ventas.csv`:

```csv
producto,cantidad_total,ventas_total
Pizza,41,492.00
Refresco,35,87.50
Hamburguesa,25,212.50
Ensalada,8,48.00
```

### Interpretación

**Qué aprendimos**:
1. **Dependencias secuenciales**: `extract >> transform >> load`
2. **Pasar datos entre tasks**: Usando archivos temporales (`/tmp/`)
3. **Pipeline ETL real**: Extraer, transformar, cargar
4. **Logging útil**: Imprimir información en cada paso

**Aplicación real**:
- En producción, usarías una base de datos en vez de archivos temporales
- Podrías añadir validaciones (¿el CSV está vacío?)
- Podrías enviar el reporte por email

---

## Ejemplo 3: Pipeline con BashOperator ⭐

**Nivel:** Básico
**Duración:** 15 minutos
**Objetivo:** Usar comandos shell en Airflow

### Contexto

**CloudAPI Systems** necesita un pipeline que:
1. Cree un directorio para logs del día
2. Copie archivos de log antiguos
3. Comprima los archivos para ahorrar espacio

### DAG Completo

Crea `airflow/dags/ejemplo_03_bash_pipeline.py`:

```python
"""
DAG Ejemplo 3: Pipeline con BashOperator
Cliente: CloudAPI Systems
Descripción: Gestión de logs usando comandos shell
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


# Definir el DAG
with DAG(
    dag_id="ejemplo_03_bash_pipeline",
    description="Pipeline de gestión de logs con comandos shell",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["tutorial", "bash", "cloudapi"],
) as dag:

    # Tarea 1: Crear directorio para logs de hoy
    task_crear_directorio = BashOperator(
        task_id="crear_directorio",
        bash_command="""
        # Crear directorio con fecha actual
        fecha=$(date +%Y%m%d)
        mkdir -p /tmp/logs_cloudapi/$fecha
        echo "✅ Directorio creado: /tmp/logs_cloudapi/$fecha"
        ls -la /tmp/logs_cloudapi/
        """,
    )

    # Tarea 2: Generar archivos de log de ejemplo
    task_generar_logs = BashOperator(
        task_id="generar_logs",
        bash_command="""
        fecha=$(date +%Y%m%d)

        # Crear archivos de log de ejemplo
        echo "2025-10-25 10:30:00 INFO API request to /users" > /tmp/logs_cloudapi/$fecha/api.log
        echo "2025-10-25 10:31:00 INFO Database query executed" > /tmp/logs_cloudapi/$fecha/db.log
        echo "2025-10-25 10:32:00 ERROR Connection timeout" >> /tmp/logs_cloudapi/$fecha/api.log

        echo "✅ Logs generados"
        ls -lh /tmp/logs_cloudapi/$fecha/
        """,
    )

    # Tarea 3: Comprimir logs
    task_comprimir = BashOperator(
        task_id="comprimir_logs",
        bash_command="""
        fecha=$(date +%Y%m%d)
        cd /tmp/logs_cloudapi/$fecha/

        # Comprimir todos los archivos .log
        tar -czf logs_$fecha.tar.gz *.log

        # Mostrar resultado
        echo "✅ Logs comprimidos"
        ls -lh logs_$fecha.tar.gz

        # Eliminar archivos originales (descomprimidos)
        rm *.log

        echo "📦 Compresión completada. Archivos originales eliminados."
        """,
    )

    # Tarea 4: Reporte final
    task_reporte = BashOperator(
        task_id="reporte_final",
        bash_command="""
        fecha=$(date +%Y%m%d)

        echo "📊 Reporte de Gestión de Logs - CloudAPI Systems"
        echo "================================================"
        echo "Fecha: $fecha"
        echo ""

        # Mostrar tamaño del archivo comprimido
        tamanio=$(du -h /tmp/logs_cloudapi/$fecha/logs_$fecha.tar.gz | cut -f1)
        echo "Archivo comprimido: logs_$fecha.tar.gz ($tamanio)"

        echo ""
        echo "✅ Pipeline completado exitosamente"
        """,
    )

    # Definir flujo secuencial
    task_crear_directorio >> task_generar_logs >> task_comprimir >> task_reporte
```

### Ejecutar y Verificar

1. Ejecuta el DAG
2. Ve al Graph View: verás 4 tareas en línea
3. Revisa los logs de cada tarea

### Resultado Esperado

En los logs de `reporte_final` verás:

```
📊 Reporte de Gestión de Logs - CloudAPI Systems
================================================
Fecha: 20251025

Archivo comprimido: logs_20251025.tar.gz (248B)

✅ Pipeline completado exitosamente
```

### Interpretación

**Qué aprendimos**:
1. **BashOperator** para ejecutar comandos shell
2. **Comandos multi-línea** usando triple comillas `"""`
3. **Variables shell** como `$fecha`
4. **Operaciones de sistema**: mkdir, tar, rm, ls

**Cuándo usar BashOperator**:
- Manipulación de archivos del sistema
- Comandos de backup/restore
- Llamadas a CLI tools (aws cli, gcloud, curl)
- Scripts shell existentes

**Cuándo NO usarlo**:
- Lógica compleja (mejor PythonOperator)
- Necesitas retornar datos complejos
- Quieres portabilidad (Bash no funciona igual en Windows)

---

## Ejemplo 4: Dependencias en Paralelo (Fan-out, Fan-in) ⭐⭐

**Nivel:** Intermedio
**Duración:** 20 minutos
**Objetivo:** Ejecutar tareas en paralelo y luego converger

### Contexto

**LogisticFlow** necesita un reporte diario que procese 3 fuentes de datos en paralelo:
1. **Entregas completadas** del día
2. **Pedidos pendientes**
3. **Rendimiento de repartidores**

Una vez que las 3 están listas, generar un reporte consolidado.

### Visualización del Flujo

```
           inicio
              |
       ┌──────┼──────┐
       ↓      ↓      ↓
   entregas  pedidos  repartidores
       ↓      ↓      ↓
       └──────┼──────┘
              |
        generar_reporte
              |
             fin
```

### DAG Completo

Crea `airflow/dags/ejemplo_04_paralelo.py`:

```python
"""
DAG Ejemplo 4: Procesamiento en Paralelo
Cliente: LogisticFlow
Descripción: Procesar 3 fuentes de datos en paralelo y luego consolidar
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
import time


def procesar_entregas():
    """
    Procesa datos de entregas completadas del día
    """
    print("📦 Procesando entregas completadas...")
    time.sleep(2)  # Simula procesamiento

    # Simulación de datos
    entregas = {
        "total": 156,
        "a_tiempo": 142,
        "retrasadas": 14,
        "tasa_exito": 91.0
    }

    print(f"✅ Entregas procesadas: {entregas['total']}")
    print(f"   - A tiempo: {entregas['a_tiempo']} ({entregas['tasa_exito']}%)")
    print(f"   - Retrasadas: {entregas['retrasadas']}")

    return entregas


def procesar_pedidos():
    """
    Procesa pedidos pendientes de entrega
    """
    print("📋 Procesando pedidos pendientes...")
    time.sleep(3)  # Simula procesamiento más largo

    # Simulación de datos
    pedidos = {
        "total": 89,
        "alta_prioridad": 12,
        "normal": 77,
        "tiempo_promedio_espera": 2.5  # horas
    }

    print(f"✅ Pedidos procesados: {pedidos['total']}")
    print(f"   - Alta prioridad: {pedidos['alta_prioridad']}")
    print(f"   - Normal: {pedidos['normal']}")
    print(f"   - Tiempo promedio de espera: {pedidos['tiempo_promedio_espera']} horas")

    return pedidos


def procesar_repartidores():
    """
    Procesa rendimiento de repartidores
    """
    print("👤 Procesando datos de repartidores...")
    time.sleep(1.5)  # Simula procesamiento

    # Simulación de datos
    repartidores = {
        "activos": 34,
        "entregas_promedio": 4.6,
        "mejor_repartidor": "Juan García",
        "peor_repartidor": "María López"
    }

    print(f"✅ Repartidores procesados: {repartidores['activos']}")
    print(f"   - Entregas promedio por repartidor: {repartidores['entregas_promedio']}")
    print(f"   - Mejor repartidor: {repartidores['mejor_repartidor']}")

    return repartidores


def generar_reporte():
    """
    Genera reporte consolidado con todos los datos
    """
    print("📊 Generando reporte consolidado de LogisticFlow...")
    time.sleep(1)

    # En un caso real, aquí leerías los datos de las tareas anteriores
    # Por ahora, simulamos el reporte

    reporte = """
    ================================================
    REPORTE DIARIO - LogisticFlow
    ================================================
    Fecha: 2025-10-25

    📦 ENTREGAS
    - Total completadas: 156
    - Tasa de éxito: 91.0%

    📋 PEDIDOS PENDIENTES
    - Total: 89
    - Alta prioridad: 12

    👤 REPARTIDORES
    - Activos: 34
    - Entregas promedio: 4.6

    ✅ Status general: OPERACIÓN NORMAL
    ================================================
    """

    print(reporte)

    return "Reporte generado exitosamente"


# Definir el DAG
with DAG(
    dag_id="ejemplo_04_paralelo",
    description="Pipeline con procesamiento en paralelo - LogisticFlow",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["tutorial", "paralelo", "logisticflow"],
) as dag:

    # Punto de inicio (organización visual)
    inicio = DummyOperator(task_id="inicio")

    # 3 tareas en paralelo
    task_entregas = PythonOperator(
        task_id="procesar_entregas",
        python_callable=procesar_entregas,
    )

    task_pedidos = PythonOperator(
        task_id="procesar_pedidos",
        python_callable=procesar_pedidos,
    )

    task_repartidores = PythonOperator(
        task_id="procesar_repartidores",
        python_callable=procesar_repartidores,
    )

    # Tarea de consolidación
    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte,
    )

    # Punto de fin (organización visual)
    fin = DummyOperator(task_id="fin")

    # Definir dependencias:
    # inicio → 3 tareas en paralelo → generar_reporte → fin
    inicio >> [task_entregas, task_pedidos, task_repartidores] >> task_reporte >> fin
```

### Ejecutar y Observar

1. Ejecuta el DAG
2. **En el Graph View**: Verás claramente la estructura de fan-out y fan-in
3. **En tiempo real**: Las 3 tareas del medio se ejecutan simultáneamente
4. Observa los tiempos: `procesar_pedidos` tarda 3 segundos, pero las otras 2 terminan antes

### Resultado

En los logs de `generar_reporte`:

```
📊 Generando reporte consolidado de LogisticFlow...

================================================
REPORTE DIARIO - LogisticFlow
================================================
Fecha: 2025-10-25

📦 ENTREGAS
- Total completadas: 156
- Tasa de éxito: 91.0%

📋 PEDIDOS PENDIENTES
- Total: 89
- Alta prioridad: 12

👤 REPARTIDORES
- Activos: 34
- Entregas promedio: 4.6

✅ Status general: OPERACIÓN NORMAL
================================================
```

### Interpretación

**Qué aprendimos**:
1. **Fan-out**: Una tarea divide en múltiples (inicio → 3 tareas)
2. **Fan-in**: Múltiples tareas convergen en una (3 tareas → reporte)
3. **Paralelización**: Las 3 tareas se ejecutan al mismo tiempo (si el Executor lo permite)
4. **DummyOperator**: Útil para organización visual (inicio, fin)

**Beneficios de la paralelización**:
- **Tiempo total**: ~3 segundos (la más lenta)
- **Sin paralelización**: ~6.5 segundos (suma de todas)
- **Ganancia**: ~50% más rápido

**Aplicaciones reales**:
- Procesar múltiples archivos CSV en paralelo
- Consultar varias APIs simultáneamente
- Entrenar múltiples modelos de ML en paralelo
- Generar reportes de diferentes clientes simultáneamente

---

## Ejemplo 5: Schedule con Cron ⭐⭐

**Nivel:** Intermedio
**Duración:** 20 minutos
**Objetivo:** Programar DAGs para ejecución automática

### Contexto

**FinTech Analytics** necesita varios reportes automatizados:
1. **Reporte diario** de transacciones (todos los días a las 8 AM)
2. **Reporte semanal** de fraudes (cada lunes a las 9 AM)
3. **Reporte cada 30 minutos** de alertas de seguridad

Vamos a crear 3 DAGs con diferentes schedules.

### DAG 1: Reporte Diario

Crea `airflow/dags/ejemplo_05a_reporte_diario.py`:

```python
"""
DAG Ejemplo 5A: Reporte Diario
Cliente: FinTech Analytics
Schedule: Todos los días a las 8:00 AM
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def generar_reporte_diario():
    """
    Genera reporte diario de transacciones
    """
    print("💳 Generando reporte diario de transacciones...")

    # Simulación
    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "transacciones": 15432,
        "monto_total": 2450000,
        "promedio": 158.77
    }

    print(f"📊 Reporte del día {datos['fecha']}:")
    print(f"   - Transacciones: {datos['transacciones']:,}")
    print(f"   - Monto total: ${datos['monto_total']:,}")
    print(f"   - Promedio por transacción: ${datos['promedio']:.2f}")

    return "Reporte diario generado"


with DAG(
    dag_id="ejemplo_05a_reporte_diario",
    description="Reporte diario de transacciones a las 8 AM",
    start_date=datetime(2025, 1, 1),
    schedule="0 8 * * *",  # Cron: Todos los días a las 8 AM
    catchup=False,
    tags=["tutorial", "schedule", "fintech", "diario"],
) as dag:

    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte_diario,
    )
```

**Explicación del schedule**: `"0 8 * * *"`
- `0`: Minuto 0
- `8`: Hora 8 (8 AM)
- `*`: Cualquier día del mes
- `*`: Cualquier mes
- `*`: Cualquier día de la semana

**Resultado**: Se ejecuta todos los días a las 8:00 AM.

---

### DAG 2: Reporte Semanal

Crea `airflow/dags/ejemplo_05b_reporte_semanal.py`:

```python
"""
DAG Ejemplo 5B: Reporte Semanal
Cliente: FinTech Analytics
Schedule: Cada lunes a las 9:00 AM
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def generar_reporte_semanal():
    """
    Genera reporte semanal de detección de fraudes
    """
    print("🚨 Generando reporte semanal de fraudes...")

    # Simulación
    datos = {
        "semana": datetime.now().strftime("Semana del %Y-%m-%d"),
        "alertas_generadas": 156,
        "fraudes_confirmados": 8,
        "monto_bloqueado": 45000,
        "tasa_precision": 5.1
    }

    print(f"📊 Reporte semanal - {datos['semana']}:")
    print(f"   - Alertas generadas: {datos['alertas_generadas']}")
    print(f"   - Fraudes confirmados: {datos['fraudes_confirmados']}")
    print(f"   - Monto bloqueado: ${datos['monto_bloqueado']:,}")
    print(f"   - Tasa de precisión: {datos['tasa_precision']}%")

    return "Reporte semanal generado"


with DAG(
    dag_id="ejemplo_05b_reporte_semanal",
    description="Reporte semanal de fraudes cada lunes a las 9 AM",
    start_date=datetime(2025, 1, 1),
    schedule="0 9 * * 1",  # Cron: Cada lunes a las 9 AM
    catchup=False,
    tags=["tutorial", "schedule", "fintech", "semanal"],
) as dag:

    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte_semanal,
    )
```

**Explicación del schedule**: `"0 9 * * 1"`
- `0`: Minuto 0
- `9`: Hora 9 (9 AM)
- `*`: Cualquier día del mes
- `*`: Cualquier mes
- `1`: Lunes (0=Domingo, 1=Lunes, ..., 6=Sábado)

**Resultado**: Se ejecuta cada lunes a las 9:00 AM.

---

### DAG 3: Alertas Cada 30 Minutos

Crea `airflow/dags/ejemplo_05c_alertas_frecuentes.py`:

```python
"""
DAG Ejemplo 5C: Alertas Frecuentes
Cliente: FinTech Analytics
Schedule: Cada 30 minutos
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def verificar_alertas():
    """
    Verifica alertas de seguridad cada 30 minutos
    """
    hora_actual = datetime.now().strftime("%H:%M")
    print(f"🔔 Verificando alertas de seguridad a las {hora_actual}...")

    # Simulación
    alertas_activas = 3

    if alertas_activas > 0:
        print(f"⚠️ ATENCIÓN: {alertas_activas} alertas activas requieren revisión")
    else:
        print("✅ Todo normal, sin alertas activas")

    return f"Verificación completada a las {hora_actual}"


with DAG(
    dag_id="ejemplo_05c_alertas_frecuentes",
    description="Verificación de alertas cada 30 minutos",
    start_date=datetime(2025, 1, 1),
    schedule="*/30 * * * *",  # Cron: Cada 30 minutos
    catchup=False,
    tags=["tutorial", "schedule", "fintech", "alertas"],
) as dag:

    task_verificar = PythonOperator(
        task_id="verificar_alertas",
        python_callable=verificar_alertas,
    )
```

**Explicación del schedule**: `"*/30 * * * *"`
- `*/30`: Cada 30 minutos (0, 30)
- `*`: Cualquier hora
- `*`: Cualquier día del mes
- `*`: Cualquier mes
- `*`: Cualquier día de la semana

**Resultado**: Se ejecuta cada 30 minutos (8:00, 8:30, 9:00, 9:30, ...).

---

### Tabla de Referencia de Cron

| Schedule                   | Significado                 | Cron Expression |
| -------------------------- | --------------------------- | --------------- |
| Cada hora                  | En el minuto 0 de cada hora | `0 * * * *`     |
| Cada 15 minutos            | A los 0, 15, 30, 45 minutos | `*/15 * * * *`  |
| Diario a medianoche        | Todos los días a las 00:00  | `0 0 * * *`     |
| Diario a las 3 PM          | Todos los días a las 15:00  | `0 15 * * *`    |
| Lunes a viernes a las 8 AM | Días laborables             | `0 8 * * 1-5`   |
| Primer día del mes         | A las 00:00 del día 1       | `0 0 1 * *`     |
| Cada domingo               | A medianoche del domingo    | `0 0 * * 0`     |

**Herramientas útiles**:
- [crontab.guru](https://crontab.guru/) - Validar expresiones cron
- [crontab-generator.org](https://crontab-generator.org/) - Generar crons visualmente

---

### Verificar Próximas Ejecuciones

En la UI de Airflow:

1. Ve a la lista de DAGs
2. Haz clic en el DAG que tiene schedule
3. En la pestaña "Details", verás "Next Run"
4. También puedes ver el historial en "Tree View"

---

### Interpretación

**Qué aprendimos**:
1. **Cron expressions** para schedules personalizados
2. **Diferentes frecuencias**: Diaria, semanal, cada X minutos
3. **`catchup=False`**: Evitar ejecuciones de fechas pasadas
4. **Tags**: Organizar DAGs por frecuencia (diario, semanal, alertas)

**Cuándo usar cada frecuencia**:
- **Cada minuto/hora**: Monitoreo en tiempo real, alertas
- **Diaria**: Reportes diarios, ETL de ventas, backups
- **Semanal**: Reportes ejecutivos, análisis de tendencias
- **Mensual**: Cierre de mes, reportes financieros

---

## Resumen de Ejemplos

| Ejemplo          | Concepto Clave | Aplicación Real            |
| ---------------- | -------------- | -------------------------- |
| 1. Hola Mundo    | DAG básico     | Verificar configuración    |
| 2. ETL Simple    | Pipeline E→T→L | Procesar datos diarios     |
| 3. Bash Pipeline | BashOperator   | Gestión de archivos/logs   |
| 4. Paralelo      | Fan-out/Fan-in | Procesar múltiples fuentes |
| 5. Cron Schedule | Automatización | Reportes programados       |

---

## ✅ Checklist de Progreso

Marca cada ejemplo que hayas completado y ejecutado exitosamente:

- [ ] **Ejemplo 1: Hola Mundo** - He creado y ejecutado mi primer DAG
- [ ] **Ejemplo 2: ETL Simple** - He procesado un CSV completo (Extract → Transform → Load)
- [ ] **Ejemplo 3: Bash Pipeline** - He usado BashOperator para comandos del sistema
- [ ] **Ejemplo 4: Paralelo** - He ejecutado tareas en paralelo (fan-out/fan-in)
- [ ] **Ejemplo 5: Cron Schedule** - He configurado schedules automáticos

**Autoevaluación adicional:**
- [ ] He visto los logs de cada ejemplo en la UI de Airflow
- [ ] He modificado al menos un ejemplo con mis propios datos
- [ ] Entiendo cómo definir dependencias con `>>`
- [ ] He verificado el grafo visual de cada DAG en la UI
- [ ] Puedo explicar la diferencia entre PythonOperator y BashOperator

---

## Próximos Pasos

Ahora que has visto estos 5 ejemplos:

1. **Practica**: Modifica cada ejemplo con tus propios datos
2. **Combina**: Crea un DAG que use BashOperator Y PythonOperator
3. **Experimenta**: Prueba diferentes schedules
4. **Avanza**: Ve a `03-EJERCICIOS.md` para consolidar tu aprendizaje

---

**¡Felicitaciones!** Has completado los ejemplos prácticos de Airflow. 🎉

Ahora entiendes cómo crear pipelines reales de Data Engineering con orquestación automática.

---

**Fecha de creación**: 2025-10-25
**Autor**: @teaching [profesor]
**Módulo**: 6 - Apache Airflow y Orquestación
**Tema**: 1 - Introducción a Airflow
