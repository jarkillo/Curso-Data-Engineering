# Ejercicios Prácticos: Introducción a PySpark

## Ejercicios Básicos

### Ejercicio 1: Crear y Explorar un DataFrame

**Dificultad**: ⭐ Fácil

**Contexto**: **RetailMax** tiene datos de productos que necesitan analizar.

**Datos**:
```python
productos = [
    {"id": 1, "nombre": "Laptop HP", "categoria": "Electrónica", "precio": 899.99, "stock": 45},
    {"id": 2, "nombre": "Mouse Logitech", "categoria": "Electrónica", "precio": 29.99, "stock": 150},
    {"id": 3, "nombre": "Escritorio Oak", "categoria": "Muebles", "precio": 349.99, "stock": 20},
    {"id": 4, "nombre": "Silla Ergonómica", "categoria": "Muebles", "precio": 199.99, "stock": 35},
    {"id": 5, "nombre": "Monitor 27in", "categoria": "Electrónica", "precio": 299.99, "stock": 60},
    {"id": 6, "nombre": "Teclado Mecánico", "categoria": "Electrónica", "precio": 79.99, "stock": 80},
    {"id": 7, "nombre": "Lámpara LED", "categoria": "Iluminación", "precio": 45.99, "stock": 100},
]
```

**Tareas**:
1. Crear un DataFrame con estos datos
2. Mostrar el esquema
3. Contar el número total de productos
4. Mostrar los primeros 3 productos

**Pista**: Usa `spark.createDataFrame()`, `printSchema()`, `count()` y `show(3)`

---

### Ejercicio 2: Filtrar y Seleccionar

**Dificultad**: ⭐ Fácil

**Contexto**: Usando el DataFrame del Ejercicio 1.

**Tareas**:
1. Filtrar productos con precio mayor a $100
2. Seleccionar solo las columnas `nombre` y `precio`
3. Filtrar productos de la categoría "Electrónica" con stock menor a 100

**Pista**: Usa `filter()`, `select()` y condiciones con `&`

---

### Ejercicio 3: Añadir Columnas Calculadas

**Dificultad**: ⭐ Fácil

**Contexto**: Usando el DataFrame del Ejercicio 1.

**Tareas**:
1. Añadir columna `valor_inventario` = precio × stock
2. Añadir columna `precio_con_iva` = precio × 1.21
3. Añadir columna `nivel_stock` que sea "Alto" si stock > 50, "Medio" si > 20, "Bajo" en otro caso

**Pista**: Usa `withColumn()`, `col()` y `when().otherwise()`

---

### Ejercicio 4: Agregaciones Básicas

**Dificultad**: ⭐ Fácil

**Contexto**: Usando el DataFrame del Ejercicio 1.

**Tareas**:
1. Calcular el precio promedio de todos los productos
2. Encontrar el producto más caro y el más barato
3. Calcular el stock total por categoría

**Pista**: Usa `agg()`, `avg()`, `max()`, `min()`, `sum()` y `groupBy()`

---

## Ejercicios Intermedios

### Ejercicio 5: Joins entre DataFrames

**Dificultad**: ⭐⭐ Intermedio

**Contexto**: **OrderFlow** tiene datos de pedidos y clientes separados.

**Datos**:
```python
clientes = [
    {"cliente_id": 101, "nombre": "Ana García", "ciudad": "Madrid"},
    {"cliente_id": 102, "nombre": "Luis Pérez", "ciudad": "Barcelona"},
    {"cliente_id": 103, "nombre": "María López", "ciudad": "Valencia"},
    {"cliente_id": 104, "nombre": "Carlos Ruiz", "ciudad": "Sevilla"},
]

pedidos = [
    {"pedido_id": "P001", "cliente_id": 101, "monto": 250.0},
    {"pedido_id": "P002", "cliente_id": 101, "monto": 180.0},
    {"pedido_id": "P003", "cliente_id": 102, "monto": 420.0},
    {"pedido_id": "P004", "cliente_id": 103, "monto": 75.0},
    {"pedido_id": "P005", "cliente_id": 101, "monto": 320.0},
    {"pedido_id": "P006", "cliente_id": 105, "monto": 150.0},  # Cliente no existe
]
```

**Tareas**:
1. Hacer INNER JOIN entre pedidos y clientes
2. Hacer LEFT JOIN para ver todos los pedidos (incluso sin cliente)
3. Calcular el total gastado por cada cliente (nombre, ciudad, total)
4. Encontrar clientes sin pedidos

**Pista**: Usa `join()` con diferentes tipos, `groupBy()` y `isNull()`

---

### Ejercicio 6: Lectura y Escritura de Archivos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**: **DataStore** necesita convertir archivos CSV a Parquet.

**Tareas**:
1. Crear un archivo CSV con los datos de productos del Ejercicio 1
2. Leer el CSV con Spark (con header e inferencia de esquema)
3. Añadir una columna `fecha_carga` con la fecha actual
4. Guardar como Parquet particionado por categoría
5. Leer el Parquet y verificar las particiones

**Pista**: Usa `write.csv()`, `read.csv()`, `current_date()`, `partitionBy()`

---

### Ejercicio 7: Window Functions

**Dificultad**: ⭐⭐ Intermedio

**Contexto**: **SalesTrack** quiere analizar ventas mensuales por vendedor.

**Datos**:
```python
ventas = [
    {"vendedor": "Ana", "mes": "2024-01", "ventas": 12000},
    {"vendedor": "Ana", "mes": "2024-02", "ventas": 15000},
    {"vendedor": "Ana", "mes": "2024-03", "ventas": 11000},
    {"vendedor": "Luis", "mes": "2024-01", "ventas": 18000},
    {"vendedor": "Luis", "mes": "2024-02", "ventas": 16000},
    {"vendedor": "Luis", "mes": "2024-03", "ventas": 20000},
    {"vendedor": "María", "mes": "2024-01", "ventas": 14000},
    {"vendedor": "María", "mes": "2024-02", "ventas": 17000},
    {"vendedor": "María", "mes": "2024-03", "ventas": 15000},
]
```

**Tareas**:
1. Calcular ventas acumuladas por vendedor
2. Calcular el cambio vs mes anterior
3. Ranking de vendedores por mes
4. Promedio móvil de 2 meses

**Pista**: Usa `Window.partitionBy()`, `sum().over()`, `lag()`, `rank()`

---

### Ejercicio 8: Transformaciones con Strings y Fechas

**Dificultad**: ⭐⭐ Intermedio

**Contexto**: **CleanData** necesita limpiar y transformar datos sucios.

**Datos**:
```python
usuarios = [
    {"id": 1, "email": "  ANA@GMAIL.COM  ", "registro": "2024-01-15"},
    {"id": 2, "email": "luis.perez@yahoo.es", "registro": "2024-02-20"},
    {"id": 3, "email": "MARIA@HOTMAIL.COM", "registro": "2024-01-10"},
    {"id": 4, "email": "  carlos@empresa.com  ", "registro": "2024-03-05"},
]
```

**Tareas**:
1. Limpiar emails: quitar espacios y convertir a minúsculas
2. Extraer el dominio del email (parte después de @)
3. Convertir registro a tipo fecha
4. Calcular días desde el registro hasta hoy
5. Extraer año y mes del registro

**Pista**: Usa `trim()`, `lower()`, `split()`, `to_date()`, `datediff()`, `year()`, `month()`

---

## Ejercicios Avanzados

### Ejercicio 9: Análisis de Logs

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**: **ServerMetrics** necesita analizar logs de acceso.

**Datos**:
```python
logs = [
    "192.168.1.1 GET /api/users 200 0.045",
    "192.168.1.2 POST /api/orders 201 0.123",
    "192.168.1.1 GET /api/products 200 0.067",
    "192.168.1.3 GET /api/users/123 404 0.012",
    "192.168.1.2 POST /api/orders 500 0.534",
    "192.168.1.4 GET /api/products 200 0.078",
    "192.168.1.1 DELETE /api/users/456 403 0.023",
    "192.168.1.5 GET /api/orders/789 200 0.089",
    "192.168.1.2 PUT /api/products/101 200 0.156",
    "192.168.1.3 GET /api/users 503 5.234",
]
```

**Tareas**:
1. Parsear cada línea para extraer: IP, método, endpoint, status, tiempo
2. Clasificar status en: success (2xx), client_error (4xx), server_error (5xx)
3. Calcular requests por endpoint
4. Calcular tiempo promedio y P95 por endpoint
5. Encontrar las IPs con más errores

**Pista**: Usa `split()`, `regexp_extract()`, `when()`, `percentile_approx()`

---

### Ejercicio 10: Optimización de Particiones

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**: **BigDataCorp** tiene un DataFrame grande que necesita optimizar.

**Tareas**:
1. Crear un DataFrame grande (10,000+ filas) con datos aleatorios
2. Ver el número de particiones inicial
3. Reparticionar por una columna clave
4. Usar coalesce para reducir particiones antes de escribir
5. Comparar tiempos de ejecución con diferentes números de particiones

**Pista**: Usa `repartition()`, `coalesce()`, `getNumPartitions()`, `time` module

---

## Soluciones

### Solución Ejercicio 1

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Ejercicio1").master("local[*]").getOrCreate()

productos = [
    {"id": 1, "nombre": "Laptop HP", "categoria": "Electrónica", "precio": 899.99, "stock": 45},
    {"id": 2, "nombre": "Mouse Logitech", "categoria": "Electrónica", "precio": 29.99, "stock": 150},
    {"id": 3, "nombre": "Escritorio Oak", "categoria": "Muebles", "precio": 349.99, "stock": 20},
    {"id": 4, "nombre": "Silla Ergonómica", "categoria": "Muebles", "precio": 199.99, "stock": 35},
    {"id": 5, "nombre": "Monitor 27in", "categoria": "Electrónica", "precio": 299.99, "stock": 60},
    {"id": 6, "nombre": "Teclado Mecánico", "categoria": "Electrónica", "precio": 79.99, "stock": 80},
    {"id": 7, "nombre": "Lámpara LED", "categoria": "Iluminación", "precio": 45.99, "stock": 100},
]

# 1. Crear DataFrame
df = spark.createDataFrame(productos)

# 2. Mostrar esquema
df.printSchema()

# 3. Contar productos
print(f"Total productos: {df.count()}")

# 4. Primeros 3
df.show(3)

spark.stop()
```

---

### Solución Ejercicio 2

```python
from pyspark.sql.functions import col

# 1. Precio > $100
df.filter(col("precio") > 100).show()

# 2. Solo nombre y precio
df.select("nombre", "precio").show()

# 3. Electrónica con stock < 100
df.filter(
    (col("categoria") == "Electrónica") & (col("stock") < 100)
).show()
```

---

### Solución Ejercicio 3

```python
from pyspark.sql.functions import col, when

# 1. Valor inventario
df = df.withColumn("valor_inventario", col("precio") * col("stock"))

# 2. Precio con IVA
df = df.withColumn("precio_con_iva", col("precio") * 1.21)

# 3. Nivel de stock
df = df.withColumn("nivel_stock",
    when(col("stock") > 50, "Alto")
    .when(col("stock") > 20, "Medio")
    .otherwise("Bajo")
)

df.show()
```

---

### Solución Ejercicio 4

```python
from pyspark.sql.functions import avg, max, min, sum

# 1. Precio promedio
df.agg(avg("precio").alias("precio_promedio")).show()

# 2. Más caro y más barato
df.agg(
    max("precio").alias("mas_caro"),
    min("precio").alias("mas_barato")
).show()

# 3. Stock por categoría
df.groupBy("categoria").agg(sum("stock").alias("stock_total")).show()
```

---

### Solución Ejercicio 5

```python
from pyspark.sql.functions import col, sum as spark_sum, count

df_clientes = spark.createDataFrame(clientes)
df_pedidos = spark.createDataFrame(pedidos)

# 1. INNER JOIN
df_inner = df_pedidos.join(df_clientes, "cliente_id", "inner")
df_inner.show()

# 2. LEFT JOIN
df_left = df_pedidos.join(df_clientes, "cliente_id", "left")
df_left.show()

# 3. Total por cliente
df_pedidos.join(df_clientes, "cliente_id") \
    .groupBy("nombre", "ciudad") \
    .agg(spark_sum("monto").alias("total_gastado")) \
    .show()

# 4. Clientes sin pedidos
df_clientes.join(df_pedidos, "cliente_id", "left_anti").show()
```

---

### Solución Ejercicio 7

```python
from pyspark.sql.functions import sum as spark_sum, lag, rank, avg
from pyspark.sql.window import Window

df = spark.createDataFrame(ventas)

window_vendedor = Window.partitionBy("vendedor").orderBy("mes")
window_mes = Window.partitionBy("mes").orderBy(col("ventas").desc())

df_analytics = df \
    .withColumn("acumulado", spark_sum("ventas").over(window_vendedor)) \
    .withColumn("cambio", col("ventas") - lag("ventas", 1).over(window_vendedor)) \
    .withColumn("ranking", rank().over(window_mes)) \
    .withColumn("promedio_movil", avg("ventas").over(
        window_vendedor.rowsBetween(-1, 0)
    ))

df_analytics.orderBy("vendedor", "mes").show()
```

---

### Solución Ejercicio 9

```python
from pyspark.sql.functions import split, col, when, count, avg, percentile_approx

# Crear DataFrame
rdd = spark.sparkContext.parallelize(logs)
df = spark.createDataFrame(rdd.map(lambda x: (x,)), ["line"])

# Parsear
df_parsed = df \
    .withColumn("parts", split("line", " ")) \
    .withColumn("ip", col("parts")[0]) \
    .withColumn("method", col("parts")[1]) \
    .withColumn("endpoint", col("parts")[2]) \
    .withColumn("status", col("parts")[3].cast("int")) \
    .withColumn("time", col("parts")[4].cast("double")) \
    .drop("parts", "line")

# Clasificar
df_classified = df_parsed.withColumn("status_type",
    when(col("status") < 300, "success")
    .when(col("status") < 500, "client_error")
    .otherwise("server_error")
)

# Métricas por endpoint
df_classified.groupBy("endpoint") \
    .agg(
        count("*").alias("requests"),
        avg("time").alias("avg_time"),
        percentile_approx("time", 0.95).alias("p95_time")
    ).show()

# IPs con más errores
df_classified.filter(col("status") >= 400) \
    .groupBy("ip") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()
```

---

## Checklist de Completitud

- [ ] Ejercicio 1: Crear y explorar DataFrame
- [ ] Ejercicio 2: Filtrar y seleccionar
- [ ] Ejercicio 3: Columnas calculadas
- [ ] Ejercicio 4: Agregaciones básicas
- [ ] Ejercicio 5: Joins
- [ ] Ejercicio 6: Archivos CSV/Parquet
- [ ] Ejercicio 7: Window functions
- [ ] Ejercicio 8: Strings y fechas
- [ ] Ejercicio 9: Análisis de logs
- [ ] Ejercicio 10: Optimización de particiones

---

**Siguiente**: [04-proyecto-practico/](04-proyecto-practico/) - Proyecto de procesamiento batch
