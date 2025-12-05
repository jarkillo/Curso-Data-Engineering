# Introducción a Apache Spark: Procesamiento Distribuido de Datos

## Introducción

### ¿Por qué necesitamos Spark?

Imagina que eres el Data Engineer de **StreamFlix**, una plataforma de streaming con 50 millones de usuarios. Cada día generas:

- **500 millones** de eventos de reproducción
- **100 millones** de búsquedas
- **50 GB** de logs de servidor

Tu script de Python con Pandas funciona perfectamente con 1 millón de filas... pero con 500 millones, tu laptop se queda sin memoria y el proceso tardaría **días**.

**¿La solución?** Distribuir el trabajo entre muchas máquinas que trabajan en paralelo. Eso es exactamente lo que hace Apache Spark.

### Analogía del Mundo Real: La Fábrica de Pizzas

Piensa en una pizzería:

| Escenario | Pandas (1 cocinero) | Spark (Equipo de cocineros) |
|-----------|---------------------|----------------------------|
| 10 pizzas | ✅ Fácil, 30 min | ⚠️ Overkill, setup innecesario |
| 100 pizzas | 😓 5 horas, agotador | ✅ 1 hora, 5 cocineros en paralelo |
| 10,000 pizzas | ❌ Imposible | ✅ 2 horas, 50 cocineros coordinados |

Spark es como tener un **chef ejecutivo** (Driver) que coordina a muchos **cocineros** (Executors) trabajando en paralelo.

### Contexto en Data Engineering

```
Fuentes de Datos    →    Procesamiento    →    Destino
(TB de datos)            (Spark)               (Data Warehouse)

┌─────────────┐         ┌─────────────┐        ┌─────────────┐
│   Kafka     │         │   Spark     │        │  Snowflake  │
│   S3/HDFS   │ ──────► │   Cluster   │ ─────► │  Delta Lake │
│   APIs      │         │ (Distribuido)│        │  PostgreSQL │
└─────────────┘         └─────────────┘        └─────────────┘
```

---

## Fundamentos de Spark

### ¿Qué es Apache Spark?

Apache Spark es un **motor de procesamiento distribuido** diseñado para:

1. **Velocidad**: Procesa datos en memoria (100x más rápido que Hadoop MapReduce)
2. **Facilidad**: APIs en Python, Scala, Java y R
3. **Generalidad**: Batch, streaming, ML, grafos - todo en una plataforma
4. **Escalabilidad**: De laptop a miles de nodos

### Arquitectura de Spark

```
┌────────────────────────────────────────────────────────────┐
│                      DRIVER PROGRAM                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   SparkSession                        │  │
│  │  - Punto de entrada a Spark                          │  │
│  │  - Coordina la ejecución                             │  │
│  │  - Divide el trabajo en tasks                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│                   CLUSTER MANAGER                           │
│         (Standalone / YARN / Kubernetes / Mesos)            │
└────────────────────────┬───────────────────────────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌────────────┐    ┌────────────┐    ┌────────────┐
│  EXECUTOR  │    │  EXECUTOR  │    │  EXECUTOR  │
│ ┌────────┐ │    │ ┌────────┐ │    │ ┌────────┐ │
│ │  Task  │ │    │ │  Task  │ │    │ │  Task  │ │
│ │  Task  │ │    │ │  Task  │ │    │ │  Task  │ │
│ │  Cache │ │    │ │  Cache │ │    │ │  Cache │ │
│ └────────┘ │    │ └────────┘ │    │ └────────┘ │
└────────────┘    └────────────┘    └────────────┘
   Worker 1          Worker 2          Worker 3
```

**Componentes clave:**

| Componente | Rol | Analogía Pizzería |
|------------|-----|-------------------|
| **Driver** | Programa principal que coordina | Chef ejecutivo |
| **SparkSession** | Punto de entrada a Spark | Cocina central |
| **Cluster Manager** | Asigna recursos (CPU, RAM) | Gerente de personal |
| **Executor** | Proceso que ejecuta tasks | Cocinero |
| **Task** | Unidad mínima de trabajo | Preparar 1 pizza |
| **Partition** | Fragmento de datos | Bandeja de ingredientes |

### SparkSession: Tu Punto de Entrada

```python
from pyspark.sql import SparkSession

# Crear SparkSession (siempre es el primer paso)
spark = SparkSession.builder \
    .appName("MiPrimerJob") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Verificar que funciona
print(f"Spark version: {spark.version}")
print(f"App name: {spark.sparkContext.appName}")
```

**Modos de ejecución:**

| Modo | Descripción | Uso |
|------|-------------|-----|
| `local` | 1 thread en tu máquina | Testing básico |
| `local[4]` | 4 threads en tu máquina | Desarrollo local |
| `local[*]` | Todos los cores disponibles | Desarrollo local |
| `yarn` | Cluster Hadoop YARN | Producción |
| `k8s://...` | Cluster Kubernetes | Producción cloud |

---

## RDDs, DataFrames y Datasets

### Evolución de las APIs de Spark

```
                    Spark 1.0          Spark 1.3          Spark 2.0+
                    ─────────          ─────────          ──────────
Abstracción:          RDD      →      DataFrame     →      Dataset
                   (bajo nivel)      (alto nivel)       (tipado fuerte)

Rendimiento:         Básico     →      Optimizado    →     Optimizado
                   (sin Catalyst)    (Catalyst)          (Catalyst)
```

### RDD (Resilient Distributed Dataset)

El RDD es la abstracción fundamental de Spark: una colección distribuida e inmutable de objetos.

```python
# Crear RDD desde una lista
numeros_rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Crear RDD desde archivo
logs_rdd = spark.sparkContext.textFile("hdfs://logs/*.txt")

# Operaciones básicas
resultado = numeros_rdd \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x * 2) \
    .collect()

print(resultado)  # [4, 8, 12, 16, 20]
```

**Características del RDD:**

| Característica | Significado |
|----------------|-------------|
| **Resilient** | Tolerante a fallos (se puede reconstruir) |
| **Distributed** | Dividido en particiones en múltiples nodos |
| **Dataset** | Colección de elementos |
| **Immutable** | No se modifica, se crean nuevos RDDs |

### DataFrame: La API Moderna

El DataFrame es una colección distribuida organizada en **columnas con nombre** (como una tabla SQL o un DataFrame de Pandas).

```python
# Crear DataFrame desde lista de diccionarios
datos = [
    {"nombre": "Ana", "edad": 28, "ciudad": "Madrid"},
    {"nombre": "Luis", "edad": 35, "ciudad": "Barcelona"},
    {"nombre": "María", "edad": 42, "ciudad": "Madrid"},
]

df = spark.createDataFrame(datos)
df.show()
# +------+----+---------+
# |nombre|edad|   ciudad|
# +------+----+---------+
# |   Ana|  28|   Madrid|
# |  Luis|  35|Barcelona|
# | María|  42|   Madrid|
# +------+----+---------+

# Ver esquema
df.printSchema()
# root
#  |-- nombre: string (nullable = true)
#  |-- edad: long (nullable = true)
#  |-- ciudad: string (nullable = true)
```

**¿Por qué usar DataFrames en lugar de RDDs?**

| Aspecto | RDD | DataFrame |
|---------|-----|-----------|
| **Optimización** | Manual | Automática (Catalyst) |
| **Serialización** | Python objects (lento) | Tungsten binary (rápido) |
| **Sintaxis** | Funcional (lambda) | Declarativa (SQL-like) |
| **Esquema** | Implícito | Explícito |
| **Interoperabilidad** | Limitada | SQL, Pandas, Parquet |

### Leer Datos en DataFrames

```python
# Desde CSV
df_csv = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("datos/ventas.csv")

# Desde Parquet (formato columnar optimizado)
df_parquet = spark.read.parquet("datos/ventas.parquet")

# Desde JSON
df_json = spark.read.json("datos/eventos.json")

# Desde base de datos JDBC
df_jdbc = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost/db") \
    .option("dbtable", "ventas") \
    .option("user", "usuario") \
    .option("password", "contraseña") \
    .load()
```

---

## Transformaciones vs Acciones

### El Concepto Más Importante: Lazy Evaluation

Spark **NO ejecuta nada** hasta que realmente necesitas el resultado. Esto permite optimizar toda la cadena de operaciones.

```python
# Estas líneas NO ejecutan nada todavía
df_filtrado = df.filter(df.edad > 30)           # Transformación
df_proyectado = df_filtrado.select("nombre")    # Transformación
df_ordenado = df_proyectado.orderBy("nombre")   # Transformación

# AQUÍ es cuando Spark ejecuta TODO el plan
resultado = df_ordenado.collect()  # Acción - ¡AHORA se ejecuta!
```

**Analogía**: Es como escribir una receta de cocina. Escribir los pasos no cocina nada; solo cuando dices "¡Cocina!" se ejecuta todo.

### Transformaciones (Lazy)

Las transformaciones crean un **nuevo DataFrame** sin ejecutar nada:

| Transformación | Descripción | Ejemplo |
|----------------|-------------|---------|
| `select()` | Seleccionar columnas | `df.select("nombre", "edad")` |
| `filter()` / `where()` | Filtrar filas | `df.filter(df.edad > 30)` |
| `withColumn()` | Añadir/modificar columna | `df.withColumn("mayor", df.edad > 18)` |
| `drop()` | Eliminar columnas | `df.drop("columna_temp")` |
| `groupBy()` | Agrupar por columna | `df.groupBy("ciudad")` |
| `orderBy()` | Ordenar | `df.orderBy("edad", ascending=False)` |
| `join()` | Unir DataFrames | `df1.join(df2, "id")` |
| `distinct()` | Eliminar duplicados | `df.distinct()` |
| `limit()` | Limitar filas | `df.limit(100)` |

**Tipos de transformaciones:**

```
Narrow Transformations (sin shuffle):
┌─────────┐     ┌─────────┐
│Partition│ ──► │Partition│   Datos permanecen en el mismo nodo
│   1     │     │   1'    │   Ejemplos: filter, map, select
└─────────┘     └─────────┘

Wide Transformations (con shuffle):
┌─────────┐
│Partition│ ──┐
│   1     │   │   ┌─────────┐
└─────────┘   ├─► │ New     │   Datos se redistribuyen entre nodos
┌─────────┐   │   │Partition│   Ejemplos: groupBy, join, orderBy
│Partition│ ──┘   └─────────┘
│   2     │
└─────────┘
```

### Acciones (Trigger Execution)

Las acciones **disparan la ejecución** y devuelven un resultado:

| Acción | Descripción | Retorna |
|--------|-------------|---------|
| `show()` | Mostrar primeras filas | Nada (imprime) |
| `collect()` | Traer todos los datos al driver | Lista Python |
| `count()` | Contar filas | Entero |
| `first()` | Primera fila | Row |
| `take(n)` | Primeras n filas | Lista de Rows |
| `write` | Escribir a archivo/BD | Nada |
| `foreach()` | Aplicar función a cada fila | Nada |

```python
# Ejemplo completo
from pyspark.sql.functions import col, avg, count

# Transformaciones (no ejecutan nada)
ventas_madrid = df_ventas \
    .filter(col("ciudad") == "Madrid") \
    .filter(col("monto") > 100) \
    .groupBy("categoria") \
    .agg(
        count("*").alias("num_ventas"),
        avg("monto").alias("monto_promedio")
    ) \
    .orderBy(col("num_ventas").desc())

# Acción - AHORA se ejecuta todo
ventas_madrid.show()
```

---

## Spark UI: Monitoreo y Debugging

Cuando ejecutas Spark, puedes acceder a la **Spark UI** en `http://localhost:4040`:

```
┌─────────────────────────────────────────────────────────────┐
│                      SPARK UI                                │
├─────────────────────────────────────────────────────────────┤
│  Jobs    │  Stages   │  Storage  │  Environment │  SQL      │
├──────────┴───────────┴───────────┴──────────────┴───────────┤
│                                                             │
│  Job 0: count at script.py:25                               │
│  ├── Stage 0: scan parquet ████████████ 100%               │
│  └── Stage 1: aggregate    ████████░░░░  67%               │
│                                                             │
│  DAG Visualization:                                         │
│  [Scan] → [Filter] → [Project] → [Aggregate] → [Collect]   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Conceptos clave:**

| Concepto | Descripción |
|----------|-------------|
| **Job** | Conjunto de stages para una acción |
| **Stage** | Conjunto de tasks que pueden ejecutarse en paralelo |
| **Task** | Unidad mínima de trabajo (1 task por partición) |
| **DAG** | Grafo Dirigido Acíclico del plan de ejecución |

---

## Particionamiento

### ¿Qué es una Partición?

Una partición es un **fragmento de datos** que se procesa en un executor. El número de particiones determina el paralelismo.

```python
# Ver número de particiones
df = spark.read.parquet("datos/ventas.parquet")
print(f"Particiones: {df.rdd.getNumPartitions()}")

# Reparticionar (redistribuye datos - shuffle)
df_reparticionado = df.repartition(100)

# Coalesce (reduce particiones sin shuffle completo)
df_reducido = df.coalesce(10)
```

**Reglas generales:**

| Situación | Recomendación |
|-----------|---------------|
| Lectura inicial | 2-4 particiones por core |
| Después de filtrar mucho | `coalesce()` para reducir |
| Antes de join grande | `repartition()` por clave de join |
| Escribir archivos | Controlar particiones = controlar archivos |

### Particionamiento por Columna

```python
# Escribir particionado por fecha
df_ventas.write \
    .partitionBy("año", "mes") \
    .parquet("output/ventas_particionadas")

# Estructura resultante:
# output/ventas_particionadas/
# ├── año=2024/
# │   ├── mes=01/
# │   │   ├── part-00000.parquet
# │   │   └── part-00001.parquet
# │   ├── mes=02/
# │   │   └── ...
```

---

## Operaciones Comunes

### Funciones de Columna

```python
from pyspark.sql.functions import (
    col, lit, when, coalesce,
    upper, lower, trim, concat,
    year, month, dayofmonth, current_date,
    sum, avg, count, max, min,
    explode, array, struct
)

# Crear/modificar columnas
df = df.withColumn("nombre_upper", upper(col("nombre")))
df = df.withColumn("edad_categoria",
    when(col("edad") < 30, "joven")
    .when(col("edad") < 50, "adulto")
    .otherwise("senior")
)

# Extraer fecha
df = df.withColumn("año", year(col("fecha")))
df = df.withColumn("mes", month(col("fecha")))
```

### Agregaciones

```python
from pyspark.sql.functions import sum, avg, count, countDistinct

# Agregación simple
df.groupBy("ciudad") \
    .agg(
        count("*").alias("total_registros"),
        countDistinct("cliente_id").alias("clientes_unicos"),
        sum("monto").alias("monto_total"),
        avg("monto").alias("monto_promedio")
    ) \
    .show()
```

### Joins

```python
# Inner join (default)
df_resultado = df_ventas.join(df_clientes, "cliente_id")

# Left join
df_resultado = df_ventas.join(df_clientes, "cliente_id", "left")

# Join con condición compleja
from pyspark.sql.functions import col

df_resultado = df_ventas.join(
    df_clientes,
    (df_ventas.cliente_id == df_clientes.id) &
    (df_ventas.fecha >= df_clientes.fecha_registro),
    "inner"
)
```

---

## Escribir Datos

```python
# A Parquet (recomendado)
df.write \
    .mode("overwrite") \
    .parquet("output/datos.parquet")

# A CSV
df.write \
    .mode("append") \
    .option("header", "true") \
    .csv("output/datos.csv")

# A tabla Hive/Delta
df.write \
    .mode("overwrite") \
    .saveAsTable("database.tabla")

# Modos de escritura:
# - overwrite: Reemplaza todo
# - append: Añade al final
# - ignore: No hace nada si existe
# - error: Error si existe (default)
```

---

## Errores Comunes y Soluciones

### 1. OutOfMemoryError

```python
# ❌ Mal: traer todo al driver
todos_los_datos = df_gigante.collect()  # OOM!

# ✅ Bien: procesar en chunks o agregar primero
resultado = df_gigante.groupBy("categoria").count().collect()
```

### 2. Shuffle Excesivo

```python
# ❌ Mal: múltiples shuffles
df.groupBy("a").count().groupBy("b").count()

# ✅ Bien: minimizar shuffles
df.groupBy("a", "b").count()
```

### 3. Pequeños Archivos

```python
# ❌ Mal: 1000 particiones = 1000 archivos pequeños
df.repartition(1000).write.parquet("output/")

# ✅ Bien: coalesce antes de escribir
df.coalesce(10).write.parquet("output/")
```

---

## Checklist de Aprendizaje

- [ ] Entiendo por qué Spark es necesario para Big Data
- [ ] Puedo crear una SparkSession correctamente
- [ ] Conozco la diferencia entre Driver y Executors
- [ ] Entiendo la diferencia entre RDD y DataFrame
- [ ] Sé cuándo usar transformaciones vs acciones
- [ ] Comprendo lazy evaluation y por qué es importante
- [ ] Puedo leer datos de CSV, Parquet y JSON
- [ ] Sé usar filter, select, groupBy, join
- [ ] Entiendo el concepto de particiones
- [ ] Puedo usar la Spark UI para debugging básico

---

## Recursos Adicionales

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Functions Reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Databricks Learning](https://www.databricks.com/learn)
- [Learning Spark, 2nd Edition (O'Reilly)](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050049/)

---

**Siguiente**: [02-EJEMPLOS.md](02-EJEMPLOS.md) - Ejemplos prácticos con PySpark
