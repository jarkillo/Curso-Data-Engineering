# Ejercicios Prácticos: Introducción a Apache Airflow

**Tiempo estimado:** 4-6 horas
**Prerequisitos:** Haber completado `01-TEORIA.md` y `02-EJEMPLOS.md`

---

## 📋 Instrucciones Generales

1. **Intenta resolver cada ejercicio por tu cuenta** antes de ver la solución
2. **Crea los archivos en `airflow/dags/`** con nombres descriptivos
3. **Ejecuta cada DAG** en tu Airflow local
4. **Verifica los logs** para asegurarte de que funcionan correctamente
5. **Usa las soluciones** solo si te quedas atascado

---

## 📊 Distribución de Ejercicios

- **Ejercicios Básicos (1-5)**: ⭐ Principiante - 30-45 min cada uno
- **Ejercicios Intermedios (6-10)**: ⭐⭐ Intermedio - 45-60 min cada uno
- **Ejercicios Avanzados (11-15)**: ⭐⭐⭐ Avanzado - 60-90 min cada uno

---

## Ejercicios Básicos

### Ejercicio 1: Tu Nombre en Airflow ⭐

**Dificultad**: Fácil
**Tiempo estimado**: 30 minutos

**Contexto**:
Trabas en **DataFlow Industries** y quieres personalizar tu primer DAG para que imprima tu nombre y la fecha actual.

**Datos**: Ninguno (solo código)

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_01_mi_nombre`
2. Crea una función que imprima:
   - Tu nombre completo
   - La fecha y hora actual
   - Un mensaje de "Data Engineer en formación"
3. Usa `PythonOperator`
4. Schedule: Manual (`None`)

**Ayuda**:
- Usa `datetime.now()` para obtener la fecha actual
- Formatea la salida para que sea legible

---

### Ejercicio 2: Horario Semanal ⭐

**Dificultad**: Fácil
**Tiempo estimado**: 30 minutos

**Contexto**:
**RestaurantData Co.** necesita un DAG que se ejecute automáticamente cada lunes a las 6 AM para generar el reporte semanal de limpieza.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_02_limpieza_semanal`
2. Configura el schedule para **cada lunes a las 6 AM**
3. Crea una función que imprima "Reporte de limpieza generado"
4. Usa `catchup=False`

**Ayuda**:
- Cron expression para lunes: día de la semana = 1
- Hora 6 AM: hora = 6, minuto = 0

---

### Ejercicio 3: Dos Tareas Secuenciales ⭐

**Dificultad**: Fácil
**Tiempo estimado**: 35 minutos

**Contexto**:
**CloudAPI Systems** necesita un pipeline simple: primero validar la conexión a la API, luego obtener datos.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_03_secuencial`
2. Crea 2 funciones:
   - `validar_conexion()`: Imprime "Conexión validada"
   - `obtener_datos()`: Imprime "Datos obtenidos"
3. Define dependencia: `validar_conexion >> obtener_datos`
4. Ejecuta y verifica que se ejecutan en orden

**Ayuda**:
- Usa 2 `PythonOperator` diferentes
- El operador `>>` define la dependencia

---

### Ejercicio 4: Listar Archivos con Bash ⭐

**Dificultad**: Fácil
**Tiempo estimado**: 30 minutos

**Contexto**:
**LogisticFlow** necesita un DAG que liste todos los archivos en el directorio `/tmp/` para auditoría.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_04_listar_archivos`
2. Usa `BashOperator` para ejecutar `ls -lah /tmp/`
3. Añade una segunda tarea con `BashOperator` que ejecute `du -sh /tmp/` (tamaño del directorio)
4. Hazlas secuenciales: listar → calcular tamaño

**Ayuda**:
- Importa `from airflow.operators.bash import BashOperator`
- Usa `bash_command="comando aquí"`

---

### Ejercicio 5: Docstring y Tags ⭐

**Dificultad**: Fácil
**Tiempo estimado**: 25 minutos

**Contexto**:
**FinTech Analytics** quiere que todos los DAGs estén bien documentados y etiquetados.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_05_documentado`
2. Añade un `description` descriptivo
3. Añade estos tags: `["ejercicio", "basico", "fintech"]`
4. Crea una función simple que imprima "DAG bien documentado"
5. Añade un docstring a tu función Python

**Ayuda**:
- `description="Texto aquí"`
- `tags=["tag1", "tag2"]`
- Docstring: texto entre `"""` al inicio de la función

---

## Ejercicios Intermedios

### Ejercicio 6: Pipeline ETL con CSV Real ⭐⭐

**Dificultad**: Intermedia
**Tiempo estimado**: 60 minutos

**Contexto**:
**RestaurantData Co.** tiene un CSV con pedidos del día y necesita calcular el ticket promedio.

**Datos** (crea `airflow/dags/data/pedidos.csv`):
```csv
pedido_id,cliente,monto
1,Juan,25.50
2,María,42.00
3,Pedro,18.75
4,Ana,35.00
5,Luis,52.50
```

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_06_ticket_promedio`
2. Crea 3 funciones:
   - `extraer()`: Lee el CSV y muestra cuántas filas hay
   - `calcular_promedio()`: Calcula el monto promedio
   - `guardar_resultado()`: Guarda el promedio en un archivo de texto
3. Pipeline: extraer → calcular → guardar
4. Verifica el resultado final

**Ayuda**:
- Usa `pandas.read_csv()`
- Usa `df["monto"].mean()` para calcular promedio
- Guarda archivos temporales en `/tmp/` para pasar datos entre tasks

---

### Ejercicio 7: Tres Tareas en Paralelo ⭐⭐

**Dificultad**: Intermedia
**Tiempo estimado**: 50 minutos

**Contexto**:
**LogisticFlow** necesita procesar 3 rutas de entrega en paralelo: Norte, Sur, Centro.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_07_rutas_paralelo`
2. Crea 3 funciones:
   - `procesar_norte()`: Imprime "Ruta Norte procesada - 45 entregas"
   - `procesar_sur()`: Imprime "Ruta Sur procesada - 38 entregas"
   - `procesar_centro()`: Imprime "Ruta Centro procesada - 52 entregas"
3. Crea una función `consolidar()` que imprima "Todas las rutas consolidadas"
4. Flujo: inicio → [norte, sur, centro] → consolidar → fin
5. Usa `DummyOperator` para inicio y fin

**Ayuda**:
- `[task1, task2, task3]` para dependencias paralelas
- Importa `from airflow.operators.dummy import DummyOperator`

---

### Ejercicio 8: Timestamp en Archivos ⭐⭐

**Dificultad**: Intermedia
**Tiempo estimado**: 45 minutos

**Contexto**:
**CloudAPI Systems** necesita crear archivos de log con timestamp en el nombre.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_08_log_timestamp`
2. Crea una función que:
   - Obtenga la fecha y hora actual
   - Cree un archivo en `/tmp/log_YYYYMMDD_HHMMSS.txt`
   - Escriba "Log creado exitosamente" en el archivo
   - Imprima el nombre del archivo creado
3. Ejecuta varias veces y verifica que cada vez crea un archivo diferente

**Ayuda**:
- Usa `datetime.now().strftime("%Y%m%d_%H%M%S")` para el timestamp
- Usa `with open(ruta, "w") as f: f.write("texto")`

---

### Ejercicio 9: Schedule Personalizado ⭐⭐

**Dificultad**: Intermedia
**Tiempo estimado**: 40 minutos

**Contexto**:
**FinTech Analytics** necesita 3 DAGs con diferentes schedules para diferentes reportes.

**Tu tarea**:
Crea 3 DAGs separados:
1. `ejercicio_09a_cada_2_horas`: Se ejecuta cada 2 horas
2. `ejercicio_09b_dias_laborables`: Se ejecuta lunes a viernes a las 9 AM
3. `ejercicio_09c_fin_de_mes`: Se ejecuta el último día del mes a medianoche

Cada DAG debe tener una función simple que imprima su propósito.

**Ayuda**:
- Cada 2 horas: `"0 */2 * * *"`
- Lunes a viernes: `"0 9 * * 1-5"`
- Último día del mes: Investiga en crontab.guru (pista: día 28-31)

---

### Ejercicio 10: Combinar Bash y Python ⭐⭐

**Dificultad**: Intermedia
**Tiempo estimado**: 55 minutos

**Contexto**:
**DataFlow Industries** necesita un pipeline que use tanto comandos shell como Python.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_10_bash_python`
2. Pipeline de 4 pasos:
   - Tarea 1 (Bash): Crear directorio `/tmp/ejercicio10/`
   - Tarea 2 (Python): Generar un CSV con datos aleatorios en ese directorio
   - Tarea 3 (Python): Leer el CSV y mostrar estadísticas
   - Tarea 4 (Bash): Listar el contenido del directorio
3. Flujo secuencial: 1 → 2 → 3 → 4

**Ayuda**:
- Usa `BashOperator` para tareas 1 y 4
- Usa `PythonOperator` para tareas 2 y 3
- Para generar CSV aleatorio, usa: `pd.DataFrame({"valores": [1,2,3,4,5]}).to_csv(...)`

---

## Ejercicios Avanzados

### Ejercicio 11: Pipeline Completo con 3 CSVs ⭐⭐⭐

**Dificultad**: Avanzada
**Tiempo estimado**: 90 minutos

**Contexto**:
**RestaurantData Co.** tiene 3 archivos CSV de diferentes sucursales y necesita consolidarlos en uno solo.

**Datos** (crea 3 archivos):

`airflow/dags/data/sucursal_norte.csv`:
```csv
producto,cantidad,precio
Hamburguesa,30,8.50
Pizza,25,12.00
```

`airflow/dags/data/sucursal_sur.csv`:
```csv
producto,cantidad,precio
Hamburguesa,40,8.50
Ensalada,15,6.00
```

`airflow/dags/data/sucursal_centro.csv`:
```csv
producto,cantidad,precio
Pizza,35,12.00
Refresco,60,2.50
```

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_11_consolidar_sucursales`
2. Pipeline:
   - Leer los 3 CSV en paralelo (3 tareas)
   - Consolidar en un solo DataFrame
   - Agrupar por producto y sumar cantidad
   - Calcular total de ventas por producto
   - Guardar resultado final en `reporte_consolidado.csv`
3. Mostrar en logs: top 3 productos más vendidos

**Ayuda**:
- Usa `pd.concat([df1, df2, df3])` para consolidar
- Usa `df.groupby("producto").sum()`
- Guarda DataFrames temporales para pasar entre tasks

---

### Ejercicio 12: Error Handling y Reintentos ⭐⭐⭐

**Dificultad**: Avanzada
**Tiempo estimado**: 75 minutos

**Contexto**:
**CloudAPI Systems** necesita un DAG que maneje errores y reintente automáticamente.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_12_reintentos`
2. Crea una función `llamar_api_inestable()` que:
   - Genere un número aleatorio entre 1 y 10
   - Si el número es < 7, lance una excepción: `raise Exception("API no responde")`
   - Si el número es >= 7, imprima "API respondió correctamente"
3. Configura la tarea para:
   - Reintentar 3 veces si falla
   - Esperar 30 segundos entre reintentos
4. Ejecuta varias veces hasta que veas un reintento en acción

**Ayuda**:
- Importa `import random`
- Usa `random.randint(1, 10)`
- En `PythonOperator`, añade parámetros:
  ```python
  retries=3,
  retry_delay=timedelta(seconds=30),
  ```

---

### Ejercicio 13: DAG con 10 Tareas ⭐⭐⭐

**Dificultad**: Avanzada
**Tiempo estimado**: 80 minutos

**Contexto**:
**LogisticFlow** necesita un pipeline complejo con múltiples etapas.

**Tu tarea**:
Crea un DAG llamado `ejercicio_13_pipeline_complejo` con esta estructura:

```
              inicio
                |
         ┌──────┼──────┐
         ↓      ↓      ↓
      zona1  zona2  zona3  (procesar cada zona)
         ↓      ↓      ↓
         └──────┼──────┘
                |
         ┌──────┼──────┐
         ↓      ↓      ↓
    calcular consolidar optimizar
         ↓      ↓      ↓
         └──────┼──────┘
                |
            generar_reporte
                |
               fin
```

Cada tarea debe:
- Imprimir su nombre
- Simular procesamiento con `time.sleep(1)`
- Retornar un mensaje de éxito

**Ayuda**:
- Son 10 tareas en total
- Usa `DummyOperator` para inicio y fin
- Define dependencias cuidadosamente

---

### Ejercicio 14: Validación de Datos Antes de Procesar ⭐⭐⭐

**Dificultad**: Avanzada
**Tiempo estimado**: 85 minutos

**Contexto**:
**FinTech Analytics** necesita validar datos antes de procesarlos. Si los datos son inválidos, el pipeline debe abortar.

**Datos** (crea `airflow/dags/data/transacciones.csv`):
```csv
transaccion_id,monto,fecha
1,100.50,2025-10-25
2,200.00,2025-10-25
3,-50.00,2025-10-25
4,150.75,FECHA_INVALIDA
```

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_14_validacion`
2. Pipeline:
   - **Validar**: Lee el CSV y verifica:
     - No hay filas vacías
     - Todos los montos son > 0
     - Todas las fechas tienen formato válido
     - Si encuentra errores, imprime un reporte de errores y lanza excepción
   - **Procesar**: Si validación pasa, calcula total de transacciones
   - **Guardar**: Guarda el resultado
3. El DAG debe fallar si hay datos inválidos

**Ayuda**:
- Usa `try/except` para validar fechas: `datetime.strptime(fecha, "%Y-%m-%d")`
- Para abortar: `raise ValueError("Datos inválidos encontrados")`
- Los logs deben mostrar claramente qué está mal

---

### Ejercicio 15: Generar Archivo, Comprimir y Limpiar ⭐⭐⭐

**Dificultad**: Avanzada
**Tiempo estimado**: 90 minutos

**Contexto**:
**DataFlow Industries** necesita un pipeline que genere un reporte, lo comprima y limpie archivos temporales.

**Tu tarea**:
1. Crea un DAG llamado `ejercicio_15_generar_comprimir`
2. Pipeline de 5 pasos:
   - **Generar** (Python): Crea un CSV con 1000 filas de datos aleatorios en `/tmp/`
   - **Validar** (Python): Verifica que el CSV tiene exactamente 1000 filas
   - **Comprimir** (Bash): Usa `gzip` para comprimir el CSV
   - **Verificar** (Bash): Lista el archivo comprimido y muestra su tamaño
   - **Limpiar** (Bash): Elimina el CSV original (no el comprimido)
3. Flujo secuencial: generar → validar → comprimir → verificar → limpiar
4. Usa `BashOperator` Y `PythonOperator`

**Ayuda**:
- Para generar 1000 filas: `pd.DataFrame({"col": range(1000)})`
- Comando gzip: `gzip ruta_archivo.csv`
- Verificar tamaño: `ls -lh ruta_archivo.csv.gz`

---

## Soluciones

### Solución Ejercicio 1

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def imprimir_mi_info():
    """
    Imprime información personalizada
    """
    nombre = "Tu Nombre Completo"  # Cambia esto
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("="*50)
    print(f"Nombre: {nombre}")
    print(f"Fecha y hora: {fecha_actual}")
    print(f"Rol: Data Engineer en formación")
    print(f"Empresa: DataFlow Industries")
    print("="*50)

    return "Información mostrada correctamente"


with DAG(
    dag_id="ejercicio_01_mi_nombre",
    description="Mi primer DAG personalizado",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico"],
) as dag:

    task_info = PythonOperator(
        task_id="mostrar_informacion",
        python_callable=imprimir_mi_info,
    )
```

**Explicación**:
- `datetime.now()` obtiene fecha y hora actual
- `strftime()` formatea la fecha de forma legible
- Las funciones deben retornar algo (buena práctica)

---

### Solución Ejercicio 2

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def generar_reporte_limpieza():
    """
    Genera reporte semanal de limpieza
    """
    fecha = datetime.now().strftime("%Y-%m-%d")
    print(f"📋 Reporte de limpieza generado - {fecha}")
    print("Todas las áreas revisadas y limpias ✅")
    return "Reporte generado"


with DAG(
    dag_id="ejercicio_02_limpieza_semanal",
    description="Reporte semanal de limpieza cada lunes a las 6 AM",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * 1",  # Lunes a las 6 AM
    catchup=False,
    tags=["ejercicio", "basico", "restaurantdata"],
) as dag:

    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte_limpieza,
    )
```

**Explicación del Cron**:
- `0`: Minuto 0
- `6`: Hora 6 (6 AM)
- `*`: Cualquier día del mes
- `*`: Cualquier mes
- `1`: Lunes (0=Domingo, 1=Lunes, ..., 6=Sábado)

---

### Solución Ejercicio 3

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def validar_conexion():
    """
    Valida la conexión a la API
    """
    print("🔍 Validando conexión a CloudAPI Systems...")
    print("✅ Conexión validada correctamente")
    return "Validación exitosa"


def obtener_datos():
    """
    Obtiene datos de la API
    """
    print("📥 Obteniendo datos de la API...")
    print("✅ Datos obtenidos: 250 registros")
    return "Datos obtenidos"


with DAG(
    dag_id="ejercicio_03_secuencial",
    description="Pipeline secuencial: validar → obtener datos",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico", "cloudapi"],
) as dag:

    task_validar = PythonOperator(
        task_id="validar_conexion",
        python_callable=validar_conexion,
    )

    task_obtener = PythonOperator(
        task_id="obtener_datos",
        python_callable=obtener_datos,
    )

    # Definir dependencia secuencial
    task_validar >> task_obtener
```

**Explicación**:
- El operador `>>` significa "ejecutar después de"
- `task_validar` se ejecuta primero
- Solo cuando `task_validar` termina exitosamente, `task_obtener` se ejecuta

---

### Solución Ejercicio 4

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="ejercicio_04_listar_archivos",
    description="Auditoría de archivos en /tmp/",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico", "logisticflow"],
) as dag:

    task_listar = BashOperator(
        task_id="listar_archivos",
        bash_command="ls -lah /tmp/ | head -20",  # Limitar a 20 líneas
    )

    task_tamanio = BashOperator(
        task_id="calcular_tamanio",
        bash_command="""
        echo "Calculando tamaño del directorio /tmp/..."
        du -sh /tmp/
        echo "Auditoría completada"
        """,
    )

    # Flujo secuencial
    task_listar >> task_tamanio
```

**Explicación**:
- `bash_command` acepta cualquier comando shell
- Puedes usar comandos multi-línea con `"""`
- `|` (pipe) funciona normalmente en Bash

---

### Solución Ejercicio 5

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def generar_reporte():
    """
    Esta función genera un reporte de ejemplo.

    Docstring completo con descripción de qué hace la función,
    parámetros (ninguno en este caso) y valor de retorno.

    Returns:
        str: Mensaje de éxito
    """
    print("📄 Generando reporte para FinTech Analytics...")
    print("✅ DAG bien documentado y etiquetado")
    print("Este es un ejemplo de buenas prácticas en Airflow")

    return "Reporte generado con documentación completa"


with DAG(
    dag_id="ejercicio_05_documentado",
    description="""
    DAG de ejemplo que demuestra buenas prácticas de documentación.
    Incluye description detallado, tags apropiados y docstrings completos.
    Cliente: FinTech Analytics
    """,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "basico", "fintech", "documentacion"],
) as dag:

    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte,
    )
```

**Explicación**:
- **Docstring**: Texto entre `"""` que explica qué hace la función
- **Description**: Puede ser multi-línea para explicaciones detalladas
- **Tags**: Ayudan a filtrar DAGs en la UI (usa tags descriptivos)

---

### Solución Ejercicio 6

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os


def extraer():
    """
    Lee el CSV de pedidos
    """
    ruta = os.path.join(os.path.dirname(__file__), "data", "pedidos.csv")
    df = pd.read_csv(ruta)

    print(f"📥 Datos extraídos: {len(df)} pedidos")
    print(f"Columnas: {list(df.columns)}")

    # Guardar para la siguiente tarea
    df.to_csv("/tmp/pedidos_raw.csv", index=False)
    return f"Extraídos {len(df)} pedidos"


def calcular_promedio():
    """
    Calcula el ticket promedio
    """
    df = pd.read_csv("/tmp/pedidos_raw.csv")

    promedio = df["monto"].mean()

    print(f"🧮 Calculando ticket promedio...")
    print(f"Total pedidos: {len(df)}")
    print(f"Suma total: ${df['monto'].sum():.2f}")
    print(f"📊 Ticket promedio: ${promedio:.2f}")

    # Guardar resultado
    with open("/tmp/ticket_promedio.txt", "w") as f:
        f.write(f"Ticket promedio: ${promedio:.2f}\n")
        f.write(f"Total pedidos: {len(df)}\n")

    return promedio


def guardar_resultado():
    """
    Guarda el resultado final
    """
    # Leer resultado
    with open("/tmp/ticket_promedio.txt", "r") as f:
        contenido = f.read()

    print("📄 Resultado final:")
    print(contenido)

    # Copiar a ubicación final
    ruta_final = os.path.join(os.path.dirname(__file__), "data", "resultado_ejercicio_06.txt")
    with open(ruta_final, "w") as f:
        f.write(contenido)

    print(f"✅ Guardado en: {ruta_final}")
    return "Resultado guardado"


with DAG(
    dag_id="ejercicio_06_ticket_promedio",
    description="Pipeline ETL para calcular ticket promedio de RestaurantData Co.",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio", "restaurantdata", "etl"],
) as dag:

    task_extraer = PythonOperator(
        task_id="extraer",
        python_callable=extraer,
    )

    task_calcular = PythonOperator(
        task_id="calcular_promedio",
        python_callable=calcular_promedio,
    )

    task_guardar = PythonOperator(
        task_id="guardar_resultado",
        python_callable=guardar_resultado,
    )

    # Pipeline ETL
    task_extraer >> task_calcular >> task_guardar
```

**Explicación**:
- Usamos archivos temporales en `/tmp/` para pasar datos entre tasks
- `pandas` facilita el cálculo del promedio con `.mean()`
- Cada función tiene una responsabilidad clara (E, T, L)

---

### Solución Ejercicio 7

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


def procesar_norte():
    print("📍 Procesando Ruta Norte...")
    print("✅ Ruta Norte procesada - 45 entregas completadas")
    return 45


def procesar_sur():
    print("📍 Procesando Ruta Sur...")
    print("✅ Ruta Sur procesada - 38 entregas completadas")
    return 38


def procesar_centro():
    print("📍 Procesando Ruta Centro...")
    print("✅ Ruta Centro procesada - 52 entregas completadas")
    return 52


def consolidar():
    print("📊 Consolidando todas las rutas...")
    print("="*50)
    print("Ruta Norte: 45 entregas")
    print("Ruta Sur: 38 entregas")
    print("Ruta Centro: 52 entregas")
    print("="*50)
    print(f"TOTAL: {45+38+52} entregas completadas")
    return "Consolidación exitosa"


with DAG(
    dag_id="ejercicio_07_rutas_paralelo",
    description="Procesamiento paralelo de rutas de entrega - LogisticFlow",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio", "logisticflow", "paralelo"],
) as dag:

    inicio = DummyOperator(task_id="inicio")

    task_norte = PythonOperator(
        task_id="procesar_norte",
        python_callable=procesar_norte,
    )

    task_sur = PythonOperator(
        task_id="procesar_sur",
        python_callable=procesar_sur,
    )

    task_centro = PythonOperator(
        task_id="procesar_centro",
        python_callable=procesar_centro,
    )

    task_consolidar = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar,
    )

    fin = DummyOperator(task_id="fin")

    # Fan-out → Fan-in
    inicio >> [task_norte, task_sur, task_centro] >> task_consolidar >> fin
```

**Explicación**:
- `[task1, task2, task3]` ejecuta las 3 tareas en paralelo
- `task_consolidar` espera a que las 3 terminen
- `DummyOperator` solo para organización visual (no ejecuta nada)

---

### Solución Ejercicio 8

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def crear_log_con_timestamp():
    """
    Crea un archivo de log con timestamp en el nombre
    """
    # Generar timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Nombre del archivo
    nombre_archivo = f"/tmp/log_{timestamp}.txt"

    # Crear archivo
    with open(nombre_archivo, "w") as f:
        f.write("Log creado exitosamente\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Cliente: CloudAPI Systems\n")

    print(f"✅ Archivo creado: {nombre_archivo}")

    # Verificar que existe
    import os
    if os.path.exists(nombre_archivo):
        print(f"📁 Archivo verificado, tamaño: {os.path.getsize(nombre_archivo)} bytes")

    return nombre_archivo


with DAG(
    dag_id="ejercicio_08_log_timestamp",
    description="Crea archivos de log con timestamp - CloudAPI Systems",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio", "cloudapi"],
) as dag:

    task_crear_log = PythonOperator(
        task_id="crear_log",
        python_callable=crear_log_con_timestamp,
    )
```

**Explicación**:
- `strftime("%Y%m%d_%H%M%S")` formatea: 20251025_143025
- `f-strings` permiten interpolar variables en strings
- Cada ejecución crea un archivo diferente

---

### Solución Ejercicio 9

**Archivo 1**: `ejercicio_09a_cada_2_horas.py`
```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def reporte_cada_2_horas():
    hora = datetime.now().strftime("%H:%M")
    print(f"📊 Reporte de monitoreo cada 2 horas - {hora}")
    return "Reporte generado"


with DAG(
    dag_id="ejercicio_09a_cada_2_horas",
    description="Reporte cada 2 horas",
    start_date=datetime(2025, 1, 1),
    schedule="0 */2 * * *",  # Cada 2 horas
    catchup=False,
    tags=["ejercicio", "intermedio", "fintech", "schedule"],
) as dag:

    task = PythonOperator(
        task_id="generar_reporte",
        python_callable=reporte_cada_2_horas,
    )
```

**Archivo 2**: `ejercicio_09b_dias_laborables.py`
```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def reporte_dias_laborables():
    dia = datetime.now().strftime("%A")
    print(f"📊 Reporte de días laborables - {dia}")
    return "Reporte generado"


with DAG(
    dag_id="ejercicio_09b_dias_laborables",
    description="Reporte lunes a viernes a las 9 AM",
    start_date=datetime(2025, 1, 1),
    schedule="0 9 * * 1-5",  # Lunes a viernes a las 9 AM
    catchup=False,
    tags=["ejercicio", "intermedio", "fintech", "schedule"],
) as dag:

    task = PythonOperator(
        task_id="generar_reporte",
        python_callable=reporte_dias_laborables,
    )
```

**Archivo 3**: `ejercicio_09c_fin_de_mes.py`
```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def reporte_fin_de_mes():
    fecha = datetime.now().strftime("%Y-%m-%d")
    print(f"📊 Reporte de fin de mes - {fecha}")
    return "Reporte generado"


with DAG(
    dag_id="ejercicio_09c_fin_de_mes",
    description="Reporte el último día del mes a medianoche",
    start_date=datetime(2025, 1, 1),
    # Nota: El último día del mes varía (28-31)
    # Esta es una aproximación: día 28, 29, 30 o 31 a medianoche
    schedule="0 0 28-31 * *",  # Días 28-31 a medianoche
    catchup=False,
    tags=["ejercicio", "intermedio", "fintech", "schedule"],
) as dag:

    task = PythonOperator(
        task_id="generar_reporte",
        python_callable=reporte_fin_de_mes,
    )
```

**Explicación de Cron**:
- `*/2`: Cada 2 (horas, minutos, etc.)
- `1-5`: Rango del 1 al 5 (lunes a viernes)
- `28-31`: Últimos días del mes (no perfecto pero funcional)

---

### Solución Ejercicio 10

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import os


def generar_csv_aleatorio():
    """
    Genera un CSV con datos aleatorios
    """
    import random

    # Generar datos aleatorios
    datos = {
        "id": range(1, 101),
        "producto": [f"Producto_{random.randint(1, 20)}" for _ in range(100)],
        "cantidad": [random.randint(1, 50) for _ in range(100)],
        "precio": [round(random.uniform(5.0, 100.0), 2) for _ in range(100)]
    }

    df = pd.DataFrame(datos)

    # Guardar en el directorio creado por Bash
    ruta = "/tmp/ejercicio10/datos_aleatorios.csv"
    df.to_csv(ruta, index=False)

    print(f"✅ CSV generado: {ruta}")
    print(f"📊 Filas: {len(df)}, Columnas: {len(df.columns)}")

    return ruta


def leer_y_estadisticas():
    """
    Lee el CSV y muestra estadísticas
    """
    ruta = "/tmp/ejercicio10/datos_aleatorios.csv"
    df = pd.read_csv(ruta)

    print("="*60)
    print("📊 ESTADÍSTICAS DEL DATASET")
    print("="*60)
    print(f"\nFilas totales: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    print(f"\n--- Estadísticas de Cantidad ---")
    print(f"Media: {df['cantidad'].mean():.2f}")
    print(f"Mínimo: {df['cantidad'].min()}")
    print(f"Máximo: {df['cantidad'].max()}")
    print(f"\n--- Estadísticas de Precio ---")
    print(f"Media: ${df['precio'].mean():.2f}")
    print(f"Mínimo: ${df['precio'].min():.2f}")
    print(f"Máximo: ${df['precio'].max():.2f}")
    print(f"\n--- Top 5 Productos Más Frecuentes ---")
    print(df['producto'].value_counts().head())
    print("="*60)

    return "Estadísticas calculadas"


with DAG(
    dag_id="ejercicio_10_bash_python",
    description="Pipeline combinando Bash y Python - DataFlow Industries",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "intermedio", "dataflow", "bash-python"],
) as dag:

    task_crear_dir = BashOperator(
        task_id="crear_directorio",
        bash_command="""
        echo "📁 Creando directorio..."
        mkdir -p /tmp/ejercicio10/
        echo "✅ Directorio creado: /tmp/ejercicio10/"
        """,
    )

    task_generar = PythonOperator(
        task_id="generar_csv",
        python_callable=generar_csv_aleatorio,
    )

    task_estadisticas = PythonOperator(
        task_id="calcular_estadisticas",
        python_callable=leer_y_estadisticas,
    )

    task_listar = BashOperator(
        task_id="listar_contenido",
        bash_command="""
        echo "📂 Listando contenido del directorio..."
        ls -lh /tmp/ejercicio10/
        echo ""
        echo "📊 Tamaño del archivo CSV:"
        du -h /tmp/ejercicio10/datos_aleatorios.csv
        """,
    )

    # Pipeline secuencial
    task_crear_dir >> task_generar >> task_estadisticas >> task_listar
```

**Explicación**:
- Combina operadores Bash y Python en el mismo flujo
- Bash crea la infraestructura (directorios)
- Python procesa datos (generar y analizar)
- Bash verifica el resultado final

---

### Solución Ejercicio 11

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os


def leer_sucursal_norte():
    """Lee el CSV de la sucursal Norte"""
    ruta = os.path.join(os.path.dirname(__file__), "data", "sucursal_norte.csv")
    df = pd.read_csv(ruta)
    print(f"📥 Sucursal Norte: {len(df)} productos")
    df.to_csv("/tmp/norte_raw.csv", index=False)
    return f"Norte: {len(df)} filas"


def leer_sucursal_sur():
    """Lee el CSV de la sucursal Sur"""
    ruta = os.path.join(os.path.dirname(__file__), "data", "sucursal_sur.csv")
    df = pd.read_csv(ruta)
    print(f"📥 Sucursal Sur: {len(df)} productos")
    df.to_csv("/tmp/sur_raw.csv", index=False)
    return f"Sur: {len(df)} filas"


def leer_sucursal_centro():
    """Lee el CSV de la sucursal Centro"""
    ruta = os.path.join(os.path.dirname(__file__), "data", "sucursal_centro.csv")
    df = pd.read_csv(ruta)
    print(f"📥 Sucursal Centro: {len(df)} productos")
    df.to_csv("/tmp/centro_raw.csv", index=False)
    return f"Centro: {len(df)} filas"


def consolidar_y_procesar():
    """
    Consolida los 3 CSV, agrupa y calcula totales
    """
    # Leer los 3 archivos temporales
    df_norte = pd.read_csv("/tmp/norte_raw.csv")
    df_sur = pd.read_csv("/tmp/sur_raw.csv")
    df_centro = pd.read_csv("/tmp/centro_raw.csv")

    # Consolidar
    df_consolidado = pd.concat([df_norte, df_sur, df_centro], ignore_index=True)

    print(f"🔗 Consolidación: {len(df_consolidado)} filas totales")

    # Agrupar por producto y sumar cantidad
    df_agrupado = df_consolidado.groupby("producto", as_index=False).agg({
        "cantidad": "sum",
        "precio": "first"  # Asumimos que el precio es el mismo
    })

    # Calcular total de ventas por producto
    df_agrupado["total_ventas"] = df_agrupado["cantidad"] * df_agrupado["precio"]

    # Ordenar por total de ventas descendente
    df_agrupado = df_agrupado.sort_values("total_ventas", ascending=False)

    print("\n" + "="*60)
    print("📊 REPORTE CONSOLIDADO")
    print("="*60)
    print(df_agrupado.to_string(index=False))
    print("="*60)

    # Mostrar top 3
    print("\n🏆 TOP 3 PRODUCTOS MÁS VENDIDOS:")
    for i, row in df_agrupado.head(3).iterrows():
        print(f"{i+1}. {row['producto']}: {row['cantidad']} unidades - ${row['total_ventas']:.2f}")

    # Guardar resultado final
    ruta_final = os.path.join(os.path.dirname(__file__), "data", "reporte_consolidado.csv")
    df_agrupado.to_csv(ruta_final, index=False)

    print(f"\n✅ Reporte guardado en: {ruta_final}")

    return "Consolidación exitosa"


with DAG(
    dag_id="ejercicio_11_consolidar_sucursales",
    description="Pipeline completo con 3 CSVs - RestaurantData Co.",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "restaurantdata", "consolidacion"],
) as dag:

    task_norte = PythonOperator(
        task_id="leer_norte",
        python_callable=leer_sucursal_norte,
    )

    task_sur = PythonOperator(
        task_id="leer_sur",
        python_callable=leer_sucursal_sur,
    )

    task_centro = PythonOperator(
        task_id="leer_centro",
        python_callable=leer_sucursal_centro,
    )

    task_consolidar = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar_y_procesar,
    )

    # Leer en paralelo, luego consolidar
    [task_norte, task_sur, task_centro] >> task_consolidar
```

**Explicación**:
- 3 tareas se ejecutan en paralelo para leer cada sucursal
- Los resultados se guardan en archivos temporales
- La tarea de consolidación espera a que las 3 terminen
- Se agrupan datos con `groupby` y se calculan totales

---

### Solución Ejercicio 12

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import random


def llamar_api_inestable():
    """
    Simula llamada a API inestable que puede fallar
    """
    numero = random.randint(1, 10)

    print(f"🎲 Número generado: {numero}")

    if numero < 7:
        print("❌ API no responde (número < 7)")
        raise Exception("API no responde - Error de conexión simulado")
    else:
        print("✅ API respondió correctamente (número >= 7)")
        print("📦 Datos recibidos: {'status': 'success', 'records': 150}")
        return "API exitosa"


with DAG(
    dag_id="ejercicio_12_reintentos",
    description="Error handling y reintentos automáticos - CloudAPI Systems",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "cloudapi", "error-handling"],
) as dag:

    task_api = PythonOperator(
        task_id="llamar_api",
        python_callable=llamar_api_inestable,
        retries=3,                              # Reintentar 3 veces
        retry_delay=timedelta(seconds=30),      # Esperar 30 segundos entre reintentos
    )
```

**Explicación**:
- La función falla ~70% de las veces (números 1-6)
- `retries=3`: Airflow reintentará automáticamente hasta 3 veces
- `retry_delay=timedelta(seconds=30)`: Espera 30 segundos entre intentos
- En los logs verás los reintentos marcados claramente
- Si falla 4 veces consecutivas (intento original + 3 reintentos), la tarea se marca como fallida

**Para verificar**:
- Ejecuta el DAG varias veces
- En la UI de Airflow, ve a "Task Instance Details" → "Logs"
- Verás intentos numerados si hay fallos

---

### Solución Ejercicio 13

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
import time


def procesar_zona(nombre_zona):
    """
    Procesa una zona específica
    """
    def funcion():
        print(f"📍 Procesando {nombre_zona}...")
        time.sleep(1)  # Simular procesamiento
        print(f"✅ {nombre_zona} procesada correctamente")
        return f"{nombre_zona} exitosa"
    return funcion


def calcular():
    print("🧮 Calculando métricas...")
    time.sleep(1)
    print("✅ Métricas calculadas")
    return "Cálculo exitoso"


def consolidar():
    print("🔗 Consolidando resultados...")
    time.sleep(1)
    print("✅ Consolidación completada")
    return "Consolidación exitosa"


def optimizar():
    print("⚡ Optimizando rutas...")
    time.sleep(1)
    print("✅ Optimización completada")
    return "Optimización exitosa"


def generar_reporte():
    print("📄 Generando reporte final...")
    time.sleep(1)
    print("="*60)
    print("REPORTE FINAL - LOGISTICFLOW")
    print("="*60)
    print("Zonas procesadas: 3")
    print("Métricas calculadas: ✅")
    print("Datos consolidados: ✅")
    print("Optimización aplicada: ✅")
    print("Estado: ÉXITO")
    print("="*60)
    return "Reporte generado"


with DAG(
    dag_id="ejercicio_13_pipeline_complejo",
    description="Pipeline complejo con 10 tareas - LogisticFlow",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "logisticflow", "pipeline-complejo"],
) as dag:

    # Tarea 1: Inicio
    inicio = DummyOperator(task_id="inicio")

    # Tareas 2-4: Procesar zonas en paralelo
    zona1 = PythonOperator(
        task_id="procesar_zona1",
        python_callable=procesar_zona("Zona 1 - Norte"),
    )

    zona2 = PythonOperator(
        task_id="procesar_zona2",
        python_callable=procesar_zona("Zona 2 - Sur"),
    )

    zona3 = PythonOperator(
        task_id="procesar_zona3",
        python_callable=procesar_zona("Zona 3 - Centro"),
    )

    # Tareas 5-7: Procesamiento en paralelo
    task_calcular = PythonOperator(
        task_id="calcular",
        python_callable=calcular,
    )

    task_consolidar = PythonOperator(
        task_id="consolidar",
        python_callable=consolidar,
    )

    task_optimizar = PythonOperator(
        task_id="optimizar",
        python_callable=optimizar,
    )

    # Tarea 8: Generar reporte
    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte,
    )

    # Tarea 9: Fin
    fin = DummyOperator(task_id="fin")

    # Definir flujo completo (10 tareas)
    inicio >> [zona1, zona2, zona3]
    [zona1, zona2, zona3] >> [task_calcular, task_consolidar, task_optimizar]
    [task_calcular, task_consolidar, task_optimizar] >> task_reporte
    task_reporte >> fin
```

**Explicación**:
- **10 tareas totales**: inicio, 3 zonas, 3 procesamientos, reporte, fin
- **Primer fan-out**: inicio → 3 zonas en paralelo
- **Segundo fan-out**: 3 zonas → 3 procesamientos en paralelo
- **Consolidación**: 3 procesamientos → 1 reporte
- **Finalización**: reporte → fin
- `time.sleep(1)` simula procesamiento real
- En la UI de Airflow verás el grafo exactamente como se describe

---

### Solución Ejercicio 14

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os


def validar_datos():
    """
    Valida el CSV de transacciones y reporta errores
    """
    ruta = os.path.join(os.path.dirname(__file__), "data", "transacciones.csv")
    df = pd.read_csv(ruta)

    errores = []

    print("🔍 Iniciando validación de datos...")
    print(f"Total de filas: {len(df)}")

    # Validación 1: No hay filas vacías
    if df.isnull().any().any():
        errores.append("❌ Hay valores nulos en el dataset")
        print(f"Columnas con nulos: {df.columns[df.isnull().any()].tolist()}")

    # Validación 2: Todos los montos son > 0
    montos_invalidos = df[df["monto"] <= 0]
    if not montos_invalidos.empty:
        errores.append(f"❌ {len(montos_invalidos)} transacciones con monto <= 0")
        print(f"Transacciones inválidas:\n{montos_invalidos}")

    # Validación 3: Todas las fechas son válidas
    fechas_invalidas = []
    for idx, fecha in enumerate(df["fecha"]):
        try:
            datetime.strptime(str(fecha), "%Y-%m-%d")
        except ValueError:
            fechas_invalidas.append(f"Fila {idx}: '{fecha}'")
            errores.append(f"❌ Fecha inválida en fila {idx}: '{fecha}'")

    # Reporte de errores
    if errores:
        print("\n" + "="*60)
        print("⚠️  REPORTE DE ERRORES DE VALIDACIÓN")
        print("="*60)
        for error in errores:
            print(error)
        print("="*60)
        print("\n🚫 VALIDACIÓN FALLIDA - Abortando pipeline")

        # Lanzar excepción para detener el DAG
        raise ValueError(f"Validación fallida: {len(errores)} errores encontrados")
    else:
        print("\n✅ Validación exitosa - Todos los datos son válidos")

        # Guardar datos validados
        df.to_csv("/tmp/transacciones_validadas.csv", index=False)
        return "Validación exitosa"


def procesar_transacciones():
    """
    Procesa las transacciones validadas
    """
    df = pd.read_csv("/tmp/transacciones_validadas.csv")

    total = df["monto"].sum()
    promedio = df["monto"].mean()
    num_transacciones = len(df)

    print("="*60)
    print("💰 PROCESAMIENTO DE TRANSACCIONES")
    print("="*60)
    print(f"Total de transacciones: {num_transacciones}")
    print(f"Monto total: ${total:.2f}")
    print(f"Monto promedio: ${promedio:.2f}")
    print("="*60)

    # Guardar resultado
    resultado = {
        "num_transacciones": num_transacciones,
        "total": total,
        "promedio": promedio
    }

    with open("/tmp/resultado_transacciones.txt", "w") as f:
        f.write(f"Transacciones procesadas: {num_transacciones}\n")
        f.write(f"Total: ${total:.2f}\n")
        f.write(f"Promedio: ${promedio:.2f}\n")

    return resultado


def guardar_resultado():
    """
    Guarda el resultado final
    """
    with open("/tmp/resultado_transacciones.txt", "r") as f:
        contenido = f.read()

    print("📄 Resultado final guardado:")
    print(contenido)

    ruta_final = os.path.join(os.path.dirname(__file__), "data", "resultado_ejercicio_14.txt")
    with open(ruta_final, "w") as f:
        f.write(contenido)

    print(f"✅ Archivo guardado en: {ruta_final}")
    return "Guardado exitoso"


with DAG(
    dag_id="ejercicio_14_validacion",
    description="Validación de datos antes de procesar - FinTech Analytics",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "fintech", "validacion"],
) as dag:

    task_validar = PythonOperator(
        task_id="validar",
        python_callable=validar_datos,
    )

    task_procesar = PythonOperator(
        task_id="procesar",
        python_callable=procesar_transacciones,
    )

    task_guardar = PythonOperator(
        task_id="guardar",
        python_callable=guardar_resultado,
    )

    # Pipeline: validar → procesar → guardar
    # Si validar falla, el pipeline se detiene
    task_validar >> task_procesar >> task_guardar
```

**Explicación**:
- La función `validar_datos()` realiza 3 validaciones
- Si encuentra errores, imprime un reporte detallado
- Lanza `ValueError` para abortar el pipeline
- Solo si la validación pasa, se ejecutan las siguientes tareas
- El CSV de ejemplo tiene errores intencionalmente para demostrar la validación

---

### Solución Ejercicio 15

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd


def generar_csv_grande():
    """
    Genera un CSV con 1000 filas de datos aleatorios
    """
    import random

    print("📝 Generando CSV con 1000 filas...")

    datos = {
        "id": range(1, 1001),
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(1000)],
        "valor": [round(random.uniform(0, 100), 2) for _ in range(1000)],
        "categoria": [f"Cat_{random.randint(1, 10)}" for _ in range(1000)]
    }

    df = pd.DataFrame(datos)

    ruta = "/tmp/reporte_grande.csv"
    df.to_csv(ruta, index=False)

    print(f"✅ CSV generado: {ruta}")
    print(f"📊 Tamaño: {len(df)} filas, {len(df.columns)} columnas")

    return ruta


def validar_csv():
    """
    Verifica que el CSV tiene exactamente 1000 filas
    """
    ruta = "/tmp/reporte_grande.csv"
    df = pd.read_csv(ruta)

    num_filas = len(df)

    print(f"🔍 Validando CSV...")
    print(f"Filas encontradas: {num_filas}")

    if num_filas != 1000:
        raise ValueError(f"Error: Se esperaban 1000 filas, pero se encontraron {num_filas}")

    print("✅ Validación exitosa: 1000 filas confirmadas")
    return "Validación exitosa"


with DAG(
    dag_id="ejercicio_15_generar_comprimir",
    description="Generar, validar, comprimir y limpiar - DataFlow Industries",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejercicio", "avanzado", "dataflow", "pipeline-completo"],
) as dag:

    task_generar = PythonOperator(
        task_id="generar",
        python_callable=generar_csv_grande,
    )

    task_validar = PythonOperator(
        task_id="validar",
        python_callable=validar_csv,
    )

    task_comprimir = BashOperator(
        task_id="comprimir",
        bash_command="""
        echo "🗜️  Comprimiendo archivo CSV..."
        gzip -f /tmp/reporte_grande.csv
        echo "✅ Archivo comprimido: /tmp/reporte_grande.csv.gz"
        """,
    )

    task_verificar = BashOperator(
        task_id="verificar",
        bash_command="""
        echo "📂 Verificando archivo comprimido..."
        ls -lh /tmp/reporte_grande.csv.gz
        echo ""
        echo "📊 Tamaño del archivo comprimido:"
        du -h /tmp/reporte_grande.csv.gz
        """,
    )

    task_limpiar = BashOperator(
        task_id="limpiar",
        bash_command="""
        echo "🧹 Limpiando archivos temporales..."
        # Nota: gzip ya elimina el archivo original por defecto
        # Pero verificamos que no exista
        if [ -f /tmp/reporte_grande.csv ]; then
            rm /tmp/reporte_grande.csv
            echo "✅ Archivo CSV original eliminado"
        else
            echo "ℹ️  Archivo CSV original ya no existe (eliminado por gzip)"
        fi
        echo "✅ Limpieza completada"
        echo "📦 Archivo final disponible: /tmp/reporte_grande.csv.gz"
        """,
    )

    # Pipeline secuencial completo
    task_generar >> task_validar >> task_comprimir >> task_verificar >> task_limpiar
```

**Explicación**:
- **Generar**: Python crea CSV con 1000 filas
- **Validar**: Python verifica el número exacto de filas
- **Comprimir**: Bash usa `gzip` para comprimir (elimina original automáticamente)
- **Verificar**: Bash muestra información del archivo comprimido
- **Limpiar**: Bash verifica limpieza (redundante con gzip pero demuestra el concepto)
- Pipeline totalmente secuencial: cada paso depende del anterior
- Combina Python para lógica de datos y Bash para operaciones de sistema

---

## Tabla de Autoevaluación

| Ejercicio | Completado | Correcto | Tiempo (min) | Notas |
| --------- | ---------- | -------- | ------------ | ----- |
| 1         | [ ]        | [ ]      |              |       |
| 2         | [ ]        | [ ]      |              |       |
| 3         | [ ]        | [ ]      |              |       |
| 4         | [ ]        | [ ]      |              |       |
| 5         | [ ]        | [ ]      |              |       |
| 6         | [ ]        | [ ]      |              |       |
| 7         | [ ]        | [ ]      |              |       |
| 8         | [ ]        | [ ]      |              |       |
| 9         | [ ]        | [ ]      |              |       |
| 10        | [ ]        | [ ]      |              |       |
| 11        | [ ]        | [ ]      |              |       |
| 12        | [ ]        | [ ]      |              |       |
| 13        | [ ]        | [ ]      |              |       |
| 14        | [ ]        | [ ]      |              |       |
| 15        | [ ]        | [ ]      |              |       |

---

## Próximos Pasos

Una vez completados estos ejercicios:

1. ✅ **Dominas los conceptos básicos** de Airflow
2. 🎯 **Puedes crear DAGs** para casos reales
3. 📚 **Estás listo** para el Tema 2: Airflow Intermedio
4. 💼 **Puedes aplicar** estos conocimientos en proyectos reales

---

**¡Felicitaciones por completar los ejercicios!** 🎉

Has consolidado tu aprendizaje de Apache Airflow con práctica real.

---

**Fecha de creación**: 2025-10-25
**Autor**: @teaching [profesor]
**Módulo**: 6 - Apache Airflow y Orquestación
**Tema**: 1 - Introducción a Airflow
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](proyecto-practico/README.md)
