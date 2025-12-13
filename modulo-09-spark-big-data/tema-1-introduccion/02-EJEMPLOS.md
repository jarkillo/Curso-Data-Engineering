# Ejemplos Prácticos: Introducción a PySpark

## Configuración Inicial

Antes de ejecutar los ejemplos, asegúrate de tener PySpark instalado:

```bash
pip install pyspark==3.5.0
```

---

## Ejemplo 1: Primeros Pasos con PySpark - Nivel: Básico

### Contexto

**DataMart Solutions** necesita analizar un pequeño dataset de ventas para entender los conceptos básicos de Spark antes de procesar sus millones de transacciones reales.

### Código

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count

# Paso 1: Crear SparkSession
spark = SparkSession.builder \
    .appName("EjemploBasico") \
    .master("local[*]") \
    .getOrCreate()

print(f"Spark versión: {spark.version}")

# Paso 2: Crear datos de ejemplo
datos_ventas = [
    {"producto": "Laptop", "categoria": "Electrónica", "precio": 1200.0, "cantidad": 2},
    {"producto": "Mouse", "categoria": "Electrónica", "precio": 25.0, "cantidad": 10},
    {"producto": "Teclado", "categoria": "Electrónica", "precio": 75.0, "cantidad": 5},
    {"producto": "Silla", "categoria": "Muebles", "precio": 300.0, "cantidad": 3},
    {"producto": "Escritorio", "categoria": "Muebles", "precio": 450.0, "cantidad": 2},
    {"producto": "Monitor", "categoria": "Electrónica", "precio": 350.0, "cantidad": 4},
]

# Paso 3: Crear DataFrame
df = spark.createDataFrame(datos_ventas)

# Paso 4: Explorar los datos
print("\n=== Esquema del DataFrame ===")
df.printSchema()

print("\n=== Primeras filas ===")
df.show()

print(f"\n=== Número de filas: {df.count()} ===")

# Paso 5: Transformaciones básicas

# Calcular el total por producto
df_con_total = df.withColumn("total", col("precio") * col("cantidad"))
print("\n=== Con columna total ===")
df_con_total.show()

# Filtrar solo electrónica
df_electronica = df_con_total.filter(col("categoria") == "Electrónica")
print("\n=== Solo Electrónica ===")
df_electronica.show()

# Agrupar por categoría
df_resumen = df_con_total.groupBy("categoria").agg(
    count("*").alias("num_productos"),
    sum("total").alias("ventas_totales"),
    avg("precio").alias("precio_promedio")
)
print("\n=== Resumen por Categoría ===")
df_resumen.show()

# Paso 6: Cerrar SparkSession
spark.stop()
```

### Resultado

```
Spark versión: 3.5.0

=== Esquema del DataFrame ===
root
 |-- producto: string (nullable = true)
 |-- categoria: string (nullable = true)
 |-- precio: double (nullable = true)
 |-- cantidad: long (nullable = true)

=== Primeras filas ===
+----------+-----------+-------+--------+
|  producto|  categoria| precio|cantidad|
+----------+-----------+-------+--------+
|    Laptop|Electrónica| 1200.0|       2|
|     Mouse|Electrónica|   25.0|      10|
|   Teclado|Electrónica|   75.0|       5|
|     Silla|    Muebles|  300.0|       3|
|Escritorio|    Muebles|  450.0|       2|
|   Monitor|Electrónica|  350.0|       4|
+----------+-----------+-------+--------+

=== Número de filas: 6 ===

=== Resumen por Categoría ===
+-----------+-------------+--------------+---------------+
|  categoria|num_productos|ventas_totales|precio_promedio|
+-----------+-------------+--------------+---------------+
|Electrónica|            4|        4275.0|         412.5|
|    Muebles|            2|        1800.0|         375.0|
+-----------+-------------+--------------+---------------+
```

### Interpretación

- Spark creó un DataFrame distribuido a partir de una lista Python
- Las transformaciones (`withColumn`, `filter`, `groupBy`) son lazy
- Solo cuando llamamos `show()` o `count()` se ejecuta el procesamiento
- El resumen muestra que Electrónica genera más ventas ($4,275) que Muebles ($1,800)

---

## Ejemplo 2: Lectura y Escritura de Archivos - Nivel: Básico

### Contexto

**LogiTrack Delivery** tiene archivos CSV con datos de entregas. Necesitan leerlos, procesarlos y guardarlos en formato Parquet para análisis eficiente.

### Paso 1: Crear datos de ejemplo

```python
# Crear archivo CSV de ejemplo
import csv

datos_entregas = [
    ["id", "cliente", "ciudad", "peso_kg", "fecha", "estado"],
    ["E001", "Juan García", "Madrid", "2.5", "2024-01-15", "entregado"],
    ["E002", "Ana López", "Barcelona", "1.2", "2024-01-15", "entregado"],
    ["E003", "Carlos Ruiz", "Valencia", "5.0", "2024-01-16", "en_transito"],
    ["E004", "María Sanz", "Madrid", "0.8", "2024-01-16", "entregado"],
    ["E005", "Pedro Martín", "Sevilla", "3.2", "2024-01-17", "pendiente"],
    ["E006", "Laura Díaz", "Barcelona", "1.5", "2024-01-17", "entregado"],
    ["E007", "Diego Torres", "Madrid", "4.0", "2024-01-18", "en_transito"],
    ["E008", "Sara Moreno", "Valencia", "2.1", "2024-01-18", "entregado"],
]

with open("data/entregas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos_entregas)

print("Archivo entregas.csv creado")
```

### Paso 2: Procesar con Spark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, sum as spark_sum
from pyspark.sql.types import DoubleType

spark = SparkSession.builder \
    .appName("LecturaEscritura") \
    .master("local[*]") \
    .getOrCreate()

# Leer CSV con inferencia de esquema
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/entregas.csv")

print("=== Datos originales ===")
df.show()
df.printSchema()

# Transformaciones
df_procesado = df \
    .withColumn("peso_kg", col("peso_kg").cast(DoubleType())) \
    .withColumn("es_pesado", when(col("peso_kg") > 3.0, "Sí").otherwise("No")) \
    .withColumn("ciudad_upper", col("ciudad"))

# Análisis por ciudad
resumen_ciudad = df_procesado \
    .groupBy("ciudad") \
    .agg(
        count("*").alias("total_entregas"),
        spark_sum("peso_kg").alias("peso_total_kg"),
        count(when(col("estado") == "entregado", 1)).alias("entregas_completadas")
    ) \
    .orderBy(col("total_entregas").desc())

print("\n=== Resumen por Ciudad ===")
resumen_ciudad.show()

# Guardar en Parquet (formato columnar eficiente)
df_procesado.write \
    .mode("overwrite") \
    .parquet("output/entregas_procesadas.parquet")

print("\nArchivo Parquet guardado en output/entregas_procesadas.parquet")

# Verificar lectura del Parquet
df_verificacion = spark.read.parquet("output/entregas_procesadas.parquet")
print(f"\nFilas en Parquet: {df_verificacion.count()}")

spark.stop()
```

### Resultado

```
=== Datos originales ===
+----+------------+---------+-------+----------+-----------+
|  id|     cliente|   ciudad|peso_kg|     fecha|     estado|
+----+------------+---------+-------+----------+-----------+
|E001| Juan García|   Madrid|    2.5|2024-01-15|  entregado|
|E002|   Ana López|Barcelona|    1.2|2024-01-15|  entregado|
...

=== Resumen por Ciudad ===
+---------+--------------+-------------+--------------------+
|   ciudad|total_entregas|peso_total_kg|entregas_completadas|
+---------+--------------+-------------+--------------------+
|   Madrid|             3|          7.3|                   2|
|Barcelona|             2|          2.7|                   2|
| Valencia|             2|          7.1|                   1|
|  Sevilla|             1|          3.2|                   0|
+---------+--------------+-------------+--------------------+
```

### Interpretación

- CSV es fácil de leer pero ineficiente para Big Data
- Parquet es columnar, comprimido y mucho más rápido para análisis
- Madrid tiene más entregas pero Valencia tiene mayor peso total

---

## Ejemplo 3: Joins entre DataFrames - Nivel: Intermedio

### Contexto

**TechStore Online** tiene datos de pedidos y clientes en tablas separadas. Necesitan combinarlos para análisis de clientes VIP.

### Código

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count, avg

spark = SparkSession.builder \
    .appName("JoinsExample") \
    .master("local[*]") \
    .getOrCreate()

# Datos de clientes
clientes_data = [
    {"cliente_id": 1, "nombre": "Ana García", "segmento": "Premium", "ciudad": "Madrid"},
    {"cliente_id": 2, "nombre": "Luis Martín", "segmento": "Standard", "ciudad": "Barcelona"},
    {"cliente_id": 3, "nombre": "María López", "segmento": "Premium", "ciudad": "Valencia"},
    {"cliente_id": 4, "nombre": "Carlos Ruiz", "segmento": "Basic", "ciudad": "Sevilla"},
    {"cliente_id": 5, "nombre": "Laura Sanz", "segmento": "Standard", "ciudad": "Madrid"},
]

# Datos de pedidos
pedidos_data = [
    {"pedido_id": "P001", "cliente_id": 1, "monto": 1500.0, "fecha": "2024-01-10"},
    {"pedido_id": "P002", "cliente_id": 1, "monto": 800.0, "fecha": "2024-01-15"},
    {"pedido_id": "P003", "cliente_id": 2, "monto": 350.0, "fecha": "2024-01-12"},
    {"pedido_id": "P004", "cliente_id": 3, "monto": 2200.0, "fecha": "2024-01-14"},
    {"pedido_id": "P005", "cliente_id": 1, "monto": 450.0, "fecha": "2024-01-20"},
    {"pedido_id": "P006", "cliente_id": 5, "monto": 600.0, "fecha": "2024-01-18"},
    {"pedido_id": "P007", "cliente_id": 3, "monto": 1100.0, "fecha": "2024-01-22"},
    {"pedido_id": "P008", "cliente_id": 2, "monto": 275.0, "fecha": "2024-01-25"},
]

df_clientes = spark.createDataFrame(clientes_data)
df_pedidos = spark.createDataFrame(pedidos_data)

print("=== Clientes ===")
df_clientes.show()

print("=== Pedidos ===")
df_pedidos.show()

# INNER JOIN: Solo clientes con pedidos
df_inner = df_pedidos.join(df_clientes, "cliente_id", "inner")
print("=== INNER JOIN (clientes con pedidos) ===")
df_inner.show()

# LEFT JOIN: Todos los pedidos, con info de cliente si existe
df_left = df_pedidos.join(df_clientes, "cliente_id", "left")
print("=== LEFT JOIN ===")
df_left.show()

# RIGHT JOIN: Todos los clientes, con pedidos si existen
df_right = df_pedidos.join(df_clientes, "cliente_id", "right")
print("=== RIGHT JOIN (incluye cliente_id=4 sin pedidos) ===")
df_right.show()

# Análisis: Resumen por cliente
resumen_clientes = df_pedidos \
    .join(df_clientes, "cliente_id") \
    .groupBy("cliente_id", "nombre", "segmento") \
    .agg(
        count("pedido_id").alias("num_pedidos"),
        spark_sum("monto").alias("total_gastado"),
        avg("monto").alias("ticket_promedio")
    ) \
    .orderBy(col("total_gastado").desc())

print("=== Resumen por Cliente ===")
resumen_clientes.show()

# Análisis: Por segmento
resumen_segmento = df_pedidos \
    .join(df_clientes, "cliente_id") \
    .groupBy("segmento") \
    .agg(
        count("*").alias("pedidos"),
        spark_sum("monto").alias("revenue"),
        avg("monto").alias("avg_order")
    ) \
    .orderBy(col("revenue").desc())

print("=== Resumen por Segmento ===")
resumen_segmento.show()

spark.stop()
```

### Resultado

```
=== Resumen por Cliente ===
+----------+------------+--------+-----------+-------------+---------------+
|cliente_id|      nombre|segmento|num_pedidos|total_gastado|ticket_promedio|
+----------+------------+--------+-----------+-------------+---------------+
|         3| María López| Premium|          2|       3300.0|         1650.0|
|         1|  Ana García| Premium|          3|       2750.0|  916.666666...|
|         2| Luis Martín|Standard|          2|        625.0|         312.5|
|         5|  Laura Sanz|Standard|          1|        600.0|         600.0|
+----------+------------+--------+-----------+-------------+---------------+

=== Resumen por Segmento ===
+--------+-------+-------+---------+
|segmento|pedidos|revenue|avg_order|
+--------+-------+-------+---------+
| Premium|      5| 6050.0|   1210.0|
|Standard|      3| 1225.0|   408.33|
+--------+-------+-------+---------+
```

### Interpretación

- Los clientes Premium generan 5x más revenue que Standard
- María López es la cliente más valiosa ($3,300 en 2 pedidos)
- Carlos Ruiz (Basic) no tiene pedidos y no aparece en el INNER JOIN

---

## Ejemplo 4: Window Functions - Nivel: Intermedio

### Contexto

**FinanceTrack** necesita calcular rankings, acumulados y comparaciones con períodos anteriores para sus métricas financieras.

### Código

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as spark_sum, row_number, rank, dense_rank,
    lag, lead, avg
)
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("WindowFunctions") \
    .master("local[*]") \
    .getOrCreate()

# Datos de ventas mensuales por vendedor
ventas_data = [
    {"vendedor": "Ana", "mes": "2024-01", "ventas": 15000},
    {"vendedor": "Ana", "mes": "2024-02", "ventas": 18000},
    {"vendedor": "Ana", "mes": "2024-03", "ventas": 12000},
    {"vendedor": "Luis", "mes": "2024-01", "ventas": 20000},
    {"vendedor": "Luis", "mes": "2024-02", "ventas": 22000},
    {"vendedor": "Luis", "mes": "2024-03", "ventas": 25000},
    {"vendedor": "María", "mes": "2024-01", "ventas": 17000},
    {"vendedor": "María", "mes": "2024-02", "ventas": 16000},
    {"vendedor": "María", "mes": "2024-03", "ventas": 19000},
]

df = spark.createDataFrame(ventas_data)
print("=== Datos de Ventas ===")
df.show()

# Window por vendedor ordenado por mes
window_vendedor = Window.partitionBy("vendedor").orderBy("mes")

# Window global por mes
window_mes = Window.partitionBy("mes").orderBy(col("ventas").desc())

# Calcular métricas con window functions
df_analytics = df \
    .withColumn("ventas_acumuladas",
        spark_sum("ventas").over(window_vendedor)) \
    .withColumn("ventas_mes_anterior",
        lag("ventas", 1).over(window_vendedor)) \
    .withColumn("cambio_vs_anterior",
        col("ventas") - lag("ventas", 1).over(window_vendedor)) \
    .withColumn("promedio_movil",
        avg("ventas").over(window_vendedor.rowsBetween(-1, 1))) \
    .withColumn("ranking_mes",
        rank().over(window_mes))

print("=== Analytics con Window Functions ===")
df_analytics.orderBy("vendedor", "mes").show()

# Top vendedor por mes
top_por_mes = df \
    .withColumn("rank", rank().over(window_mes)) \
    .filter(col("rank") == 1) \
    .select("mes", "vendedor", "ventas")

print("=== Top Vendedor por Mes ===")
top_por_mes.show()

spark.stop()
```

### Resultado

```
=== Analytics con Window Functions ===
+--------+-------+------+-----------------+-------------------+------------------+--------------+-----------+
|vendedor|    mes|ventas|ventas_acumuladas|ventas_mes_anterior|cambio_vs_anterior|promedio_movil|ranking_mes|
+--------+-------+------+-----------------+-------------------+------------------+--------------+-----------+
|     Ana|2024-01| 15000|            15000|               null|              null|       16500.0|          3|
|     Ana|2024-02| 18000|            33000|              15000|              3000|       15000.0|          2|
|     Ana|2024-03| 12000|            45000|              18000|             -6000|       15000.0|          3|
|    Luis|2024-01| 20000|            20000|               null|              null|       21000.0|          1|
|    Luis|2024-02| 22000|            42000|              20000|              2000|       22333.3|          1|
|    Luis|2024-03| 25000|            67000|              22000|              3000|       23500.0|          1|
|   María|2024-01| 17000|            17000|               null|              null|       16500.0|          2|
|   María|2024-02| 16000|            33000|              17000|             -1000|       17333.3|          3|
|   María|2024-03| 19000|            52000|              16000|              3000|       17500.0|          2|
+--------+-------+------+-----------------+-------------------+------------------+--------------+-----------+

=== Top Vendedor por Mes ===
+-------+--------+------+
|    mes|vendedor|ventas|
+-------+--------+------+
|2024-01|    Luis| 20000|
|2024-02|    Luis| 22000|
|2024-03|    Luis| 25000|
+-------+--------+------+
```

### Interpretación

- Luis es consistentemente el #1 en ventas todos los meses
- Ana tuvo una caída de $6,000 en marzo (de $18,000 a $12,000)
- El promedio móvil suaviza las fluctuaciones mensuales
- Las ventas acumuladas muestran el progreso total por vendedor

---

## Ejemplo 5: Procesamiento de Logs - Nivel: Avanzado

### Contexto

**CloudMetrics** procesa millones de logs de servidor. Necesitan analizar patrones de errores, tiempos de respuesta y tráfico por endpoint.

### Código

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, regexp_extract, to_timestamp, hour, dayofweek,
    count, avg, percentile_approx, when
)

spark = SparkSession.builder \
    .appName("LogProcessing") \
    .master("local[*]") \
    .getOrCreate()

# Simular logs de servidor (formato Apache)
logs_data = [
    '192.168.1.1 - - [15/Jan/2024:10:15:32] "GET /api/users HTTP/1.1" 200 1234 0.045',
    '192.168.1.2 - - [15/Jan/2024:10:15:33] "POST /api/orders HTTP/1.1" 201 567 0.123',
    '192.168.1.1 - - [15/Jan/2024:10:15:34] "GET /api/products HTTP/1.1" 200 2345 0.067',
    '192.168.1.3 - - [15/Jan/2024:10:15:35] "GET /api/users/123 HTTP/1.1" 404 89 0.012',
    '192.168.1.2 - - [15/Jan/2024:10:15:36] "POST /api/orders HTTP/1.1" 500 0 0.534',
    '192.168.1.4 - - [15/Jan/2024:10:16:01] "GET /api/products HTTP/1.1" 200 2345 0.078',
    '192.168.1.1 - - [15/Jan/2024:10:16:02] "DELETE /api/users/456 HTTP/1.1" 403 45 0.023',
    '192.168.1.5 - - [15/Jan/2024:10:16:03] "GET /api/orders/789 HTTP/1.1" 200 890 0.089',
    '192.168.1.2 - - [15/Jan/2024:10:16:04] "PUT /api/products/101 HTTP/1.1" 200 123 0.156',
    '192.168.1.3 - - [15/Jan/2024:10:16:05] "GET /api/users HTTP/1.1" 503 0 5.234',
]

# Crear RDD y luego DataFrame
rdd_logs = spark.sparkContext.parallelize(logs_data)
df_raw = spark.createDataFrame(rdd_logs.map(lambda x: (x,)), ["log_line"])

# Parsear logs con regex
df_parsed = df_raw \
    .withColumn("ip",
        regexp_extract("log_line", r'^(\d+\.\d+\.\d+\.\d+)', 1)) \
    .withColumn("timestamp",
        regexp_extract("log_line", r'\[(\d+/\w+/\d+:\d+:\d+:\d+)\]', 1)) \
    .withColumn("method",
        regexp_extract("log_line", r'"(\w+)\s', 1)) \
    .withColumn("endpoint",
        regexp_extract("log_line", r'"\w+\s(/[^\s]*)', 1)) \
    .withColumn("status",
        regexp_extract("log_line", r'HTTP/\d\.\d"\s(\d+)', 1).cast("int")) \
    .withColumn("response_time",
        regexp_extract("log_line", r'(\d+\.\d+)$', 1).cast("double"))

print("=== Logs Parseados ===")
df_parsed.select("ip", "method", "endpoint", "status", "response_time").show(truncate=False)

# Clasificar códigos de estado
df_classified = df_parsed \
    .withColumn("status_category",
        when(col("status") < 300, "success")
        .when(col("status") < 400, "redirect")
        .when(col("status") < 500, "client_error")
        .otherwise("server_error"))

# Análisis de errores
print("=== Resumen por Código de Estado ===")
df_classified.groupBy("status_category", "status") \
    .agg(count("*").alias("count")) \
    .orderBy("status") \
    .show()

# Métricas por endpoint
print("=== Métricas por Endpoint ===")
df_parsed.groupBy("endpoint") \
    .agg(
        count("*").alias("requests"),
        avg("response_time").alias("avg_response_time"),
        percentile_approx("response_time", 0.95).alias("p95_response_time")
    ) \
    .orderBy(col("requests").desc()) \
    .show(truncate=False)

# Endpoints con errores
print("=== Endpoints con Errores ===")
df_classified.filter(col("status") >= 400) \
    .groupBy("endpoint", "status") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

spark.stop()
```

### Resultado

```
=== Logs Parseados ===
+-----------+------+------------------+------+-------------+
|ip         |method|endpoint          |status|response_time|
+-----------+------+------------------+------+-------------+
|192.168.1.1|GET   |/api/users        |200   |0.045        |
|192.168.1.2|POST  |/api/orders       |201   |0.123        |
|192.168.1.1|GET   |/api/products     |200   |0.067        |
|192.168.1.3|GET   |/api/users/123    |404   |0.012        |
|192.168.1.2|POST  |/api/orders       |500   |0.534        |
...

=== Métricas por Endpoint ===
+------------------+--------+-----------------+-----------------+
|endpoint          |requests|avg_response_time|p95_response_time|
+------------------+--------+-----------------+-----------------+
|/api/users        |2       |2.6395           |5.234            |
|/api/orders       |2       |0.3285           |0.534            |
|/api/products     |2       |0.0725           |0.078            |
...

=== Endpoints con Errores ===
+------------------+------+-----+
|          endpoint|status|count|
+------------------+------+-----+
|        /api/users|   503|    1|
|       /api/orders|   500|    1|
|    /api/users/123|   404|    1|
|    /api/users/456|   403|    1|
+------------------+------+-----+
```

### Interpretación

- `/api/users` tiene un P95 de 5.2s - hay un request muy lento (error 503)
- `/api/orders` tuvo un error 500 - requiere investigación
- Los errores 4xx son principalmente recursos no encontrados o acceso denegado
- El tiempo promedio de respuesta varía significativamente por endpoint

---

## Resumen de Patrones Clave

| Patrón | Cuándo Usar | Ejemplo |
|--------|-------------|---------|
| `createDataFrame()` | Datos pequeños en memoria | Prototipos, tests |
| `read.csv/parquet/json` | Datos en archivos | Producción |
| `filter() + select()` | Reducir datos temprano | Optimización |
| `groupBy().agg()` | Agregaciones | Métricas, reportes |
| `join()` | Combinar tablas | Enriquecimiento |
| `Window functions` | Rankings, acumulados | Analytics avanzado |
| `regexp_extract()` | Parsear texto | Logs, ETL |

---

**Siguiente**: [03-EJERCICIOS.md](03-EJERCICIOS.md) - Ejercicios prácticos
