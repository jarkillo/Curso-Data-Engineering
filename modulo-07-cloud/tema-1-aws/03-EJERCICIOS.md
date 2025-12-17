# Ejercicios Prácticos: AWS para Data Engineering

> **Instrucciones**: Intenta resolver cada ejercicio por tu cuenta antes de ver la solución. Usa las funciones y conceptos aprendidos en la teoría y ejemplos.

---

## Ejercicios Básicos

### Ejercicio 1: Crear Bucket S3 y Subir Archivo
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas en **CloudAPI Systems** y necesitas crear un bucket S3 para almacenar logs de APIs.

**Tu tarea**:
1. Crear un bucket llamado `cloudapi-logs-{tu-nombre}` (ej: `cloudapi-logs-juan`)
2. Subir un archivo `test.txt` con el contenido "Hello AWS S3"
3. Verificar que el archivo fue subido correctamente

**Ayuda**:
- Usa `boto3.client('s3')`
- Método para crear bucket: `create_bucket()`
- Método para subir archivo: `put_object()` o `upload_file()`

---

### Ejercicio 2: Listar Archivos con Prefijo
**Dificultad**: ⭐ Fácil

**Contexto**:
**RestaurantData Co.** guarda ventas en S3 organizadas por fecha:
```
s3://restaurant-sales/
├── 2025/01/15/ventas.csv
├── 2025/01/16/ventas.csv
└── 2025/01/17/ventas.csv
```

**Tu tarea**:
Listar SOLO los archivos del día 15 de enero (prefijo: `2025/01/15/`).

**Datos**:
```python
bucket = "restaurant-sales"
prefijo = "2025/01/15/"
```

**Pregunta**:
¿Cuántos archivos hay en esa fecha?

**Ayuda**:
- Método: `list_objects_v2(Bucket=..., Prefix=...)`

---

### Ejercicio 3: Descargar Archivo de S3
**Dificultad**: ⭐ Fácil

**Contexto**:
**FinTech Analytics** tiene un archivo `transacciones_2025-01-15.csv` en S3 que necesitas descargar a tu PC.

**Datos**:
```python
bucket = "fintech-data"
s3_key = "raw/transacciones_2025-01-15.csv"
archivo_local = "transacciones_descargadas.csv"
```

**Tu tarea**:
Descargar el archivo y mostrar las primeras 5 filas con pandas.

**Ayuda**:
- Método: `download_file(Bucket, Key, Filename)`
- Luego: `pd.read_csv(archivo_local).head()`

---

### Ejercicio 4: Lambda Simple
**Dificultad**: ⭐ Fácil

**Contexto**:
Crear una función Lambda que retorne "Hello from Lambda!" cuando se ejecute.

**Tu tarea**:
Escribe el código de la función Lambda.

**Ayuda**:
```python
def lambda_handler(event, context):
    # Tu código aquí
    pass
```

---

### Ejercicio 5: Lambda que Lee Parámetro
**Dificultad**: ⭐ Fácil

**Contexto**:
Modificar la Lambda anterior para que reciba un nombre en `event` y retorne "Hello {nombre}!".

**Datos de entrada**:
```json
{
  "nombre": "Juan"
}
```

**Resultado esperado**:
```json
{
  "mensaje": "Hello Juan!"
}
```

**Ayuda**:
- Accede a event con: `event['nombre']`

---

### Ejercicio 6: Query Simple en Athena
**Dificultad**: ⭐ Fácil

**Contexto**:
**LogisticFlow** tiene una tabla `entregas` en Athena con columnas:
- `entrega_id` (string)
- `origen` (string)
- `destino` (string)
- `distancia_km` (int)

**Tu tarea**:
Escribe un query SQL para contar cuántas entregas van de Madrid a Barcelona.

**Ayuda**:
```sql
SELECT COUNT(*) as total
FROM ...
WHERE ... AND ...
```

---

## Ejercicios Intermedios

### Ejercicio 7: Lambda para Extraer Métricas de CSV
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RestaurantData Co.** sube archivos CSV con ventas. Necesitas una Lambda que:
1. Lea el CSV desde S3
2. Calcule ventas totales (suma de `cantidad * precio`)
3. Retorne las métricas

**Datos**:
CSV en `s3://restaurant-data/ventas_2025-01-15.csv`:
```csv
producto,cantidad,precio
Pizza,10,8.50
Pasta,15,7.00
Ensalada,8,6.50
```

**Tu tarea**:
Implementar Lambda que retorne:
```json
{
  "total_productos": 3,
  "unidades_vendidas": 33,
  "ventas_totales": 242.50
}
```

**Ayuda**:
- Usa `pandas` para leer CSV desde S3
- `pd.read_csv(s3.get_object(...)['Body'])`

---

### Ejercicio 8: Glue Crawler
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**CloudAPI Systems** tiene logs JSON en `s3://cloudapi-logs/raw/`. Necesitas que Glue infiera el schema automáticamente.

**Tu tarea**:
1. Crear un Crawler que escanee `s3://cloudapi-logs/raw/`
2. Configurar para ejecutarse diariamente a las 2am
3. Guardar el schema en database `cloudapi_db`

**Pregunta**:
¿Qué comando AWS CLI usarías para crear el crawler?

**Ayuda**:
```bash
aws glue create-crawler \
  --name ... \
  --role ... \
  --database-name ... \
  --targets ...
```

---

### Ejercicio 9: Crear Tabla en Glue Catalog Manualmente
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Tienes datos Parquet en `s3://fintech-data/transacciones/` con este schema:
- `transaccion_id`: string
- `timestamp`: timestamp
- `usuario_id`: string
- `monto`: decimal(10,2)

**Tu tarea**:
Escribe el SQL de Athena para crear la tabla manualmente (sin Crawler).

**Ayuda**:
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS ...
(
  columna1 tipo1,
  columna2 tipo2,
  ...
)
STORED AS PARQUET
LOCATION '...'
```

---

### Ejercicio 10: Query con JOIN en Athena
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**FinTech Analytics** tiene dos tablas:

**Tabla `transacciones`**:
- `transaccion_id`
- `usuario_id`
- `monto`

**Tabla `usuarios`**:
- `usuario_id`
- `nombre`
- `pais`

**Tu tarea**:
Escribe un query que retorne el nombre del usuario y la suma de sus transacciones, ordenado por suma descendente.

**Resultado esperado**:
```
nombre     | total_transacciones
-----------|--------------------
Juan Pérez |          15,678.90
Ana García |          12,345.50
...
```

**Ayuda**:
```sql
SELECT u.nombre, SUM(t.monto) as total_transacciones
FROM transacciones t
JOIN usuarios u ON ...
GROUP BY ...
ORDER BY ...
```

---

### Ejercicio 11: Configurar Particiones en S3
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**LogisticFlow** guarda entregas en formato Parquet sin particiones:
```
s3://logistic-data/entregas.parquet (1 archivo de 500GB)
```

Esto hace que las queries en Athena sean lentas y costosas.

**Tu tarea**:
Reorganizar los datos con particionamiento por año/mes/día.

**Estructura deseada**:
```
s3://logistic-data/entregas/
├── año=2025/mes=01/dia=15/entregas.parquet
├── año=2025/mes=01/dia=16/entregas.parquet
└── ...
```

**Pregunta**:
¿Qué código PySpark (Glue) usarías para particionar?

**Ayuda**:
```python
df.write\
  .mode("overwrite")\
  .partitionBy(...)\
  .parquet(...)
```

---

### Ejercicio 12: Lifecycle Policy en S3
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**CloudAPI Systems** guarda logs que:
- Se acceden frecuentemente los primeros 30 días
- Se acceden ocasionalmente los siguientes 90 días
- Después de 1 año, ya no se necesitan

**Tu tarea**:
Diseñar una Lifecycle Policy para minimizar costos.

**Reglas**:
1. Días 0-30: S3 Standard
2. Días 31-120: S3 Infrequent Access
3. Después de 120 días: S3 Glacier
4. Después de 365 días: Eliminar

**Pregunta**:
¿Cuánto ahorrarías al año si tienes 100GB de logs nuevos cada mes?

**Ayuda**:
- S3 Standard: 0.023 $/GB/mes
- S3 IA: 0.0125 $/GB/mes
- S3 Glacier: 0.004 $/GB/mes

---

## Ejercicios Avanzados

### Ejercicio 13: Glue Job Completo
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**FinTech Analytics** necesita procesar transacciones diarias:

**Input**: JSON en `s3://fintech/raw/transacciones/`
```json
{
  "transaccion_id": "TXN-001",
  "timestamp": "2025-01-15T10:23:45Z",
  "usuario_id": "USR-123",
  "monto": 156.50,
  "moneda": "EUR",
  "comercio": "Amazon"
}
```

**Output**: Parquet en `s3://fintech/processed/transacciones/`

**Transformaciones requeridas**:
1. Filtrar transacciones con monto > 0
2. Convertir timestamp a fecha (solo date)
3. Agregar columna `año`, `mes`, `dia` para particionamiento
4. Calcular columna `categoria_monto`:
   - `< 10€` → "bajo"
   - `10-100€` → "medio"
   - `> 100€` → "alto"
5. Guardar en Parquet particionado por `año`, `mes`, `dia`

**Tu tarea**:
Escribe el código PySpark del Glue Job.

**Ayuda**:
```python
from pyspark.sql import functions as F

df = df.withColumn("fecha", F.to_date("timestamp"))
df = df.withColumn("año", F.year("timestamp"))
# ...
```

---

### Ejercicio 14: Pipeline Completo S3 → Lambda → Glue → Athena
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**RestaurantData Co.** quiere un pipeline automatizado:

1. CSV llega a `s3://restaurant/incoming/`
2. Lambda valida que tenga columnas: `fecha`, `local`, `producto`, `cantidad`, `precio`
3. Si válido → mover a `s3://restaurant/validated/`
4. Glue Job (cada 4 horas) transforma CSV → Parquet
5. Athena permite queries

**Tu tarea**:
Diseña la arquitectura completa y escribe el código de cada componente.

**Componentes a entregar**:
1. Código Lambda de validación
2. Configuración del trigger S3 → Lambda
3. Código Glue Job
4. SQL para crear tabla en Athena
5. Query de ejemplo: "Ventas totales por local"

**Ayuda**:
- Lambda: Valida con `df.columns`
- Glue: Lee de `validated/`, escribe a `processed/`
- Athena: Query sobre `processed/`

---

### Ejercicio 15: Optimizar Costos de Athena
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**LogisticFlow** hace 1000 queries al día en Athena sobre una tabla de 10TB.

**Query actual**:
```sql
SELECT *
FROM entregas
WHERE fecha = '2025-01-15';
```

**Problema**:
- Escanea 10TB completos (sin particiones)
- Formato: CSV (sin compresión)
- Costo: 1000 queries × 10TB × 5$/TB = **50,000 $/mes** 💸

**Tu tarea**:
Proponer mejoras para reducir el costo a **<500 $/mes**.

**Estrategias a considerar**:
1. Particionamiento
2. Formato de datos (CSV vs Parquet)
3. Compresión
4. Vistas materializadas
5. `SELECT *` vs columnas específicas

**Pregunta**:
Calcula el nuevo costo si:
- Particionas por fecha (solo escaneas 1 día = 35GB)
- Conviertes a Parquet con Snappy (reducción 80% → 7GB)
- Usas `SELECT columnas_necesarias` (30% de columnas → 2.1GB)

**Ayuda**:
```
Costo = num_queries × datos_escaneados_TB × 5 $/TB
```

---

## Soluciones

### Solución Ejercicio 1

```python
import boto3

# Crear cliente S3
s3_client = boto3.client('s3', region_name='us-east-1')

# 1. Crear bucket
bucket_name = "cloudapi-logs-juan"
s3_client.create_bucket(Bucket=bucket_name)
print(f"✅ Bucket creado: {bucket_name}")

# 2. Subir archivo
contenido = "Hello AWS S3"
s3_client.put_object(
    Bucket=bucket_name,
    Key="test.txt",
    Body=contenido.encode('utf-8')
)
print("✅ Archivo subido: test.txt")

# 3. Verificar
response = s3_client.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    for obj in response['Contents']:
        print(f"   Archivo: {obj['Key']}, Tamaño: {obj['Size']} bytes")
```

**Resultado esperado**:
```
✅ Bucket creado: cloudapi-logs-juan
✅ Archivo subido: test.txt
   Archivo: test.txt, Tamaño: 12 bytes
```

---

### Solución Ejercicio 2

```python
import boto3

s3_client = boto3.client('s3')

bucket = "restaurant-sales"
prefijo = "2025/01/15/"

response = s3_client.list_objects_v2(
    Bucket=bucket,
    Prefix=prefijo
)

if 'Contents' in response:
    archivos = response['Contents']
    print(f"📂 Archivos encontrados: {len(archivos)}")
    for obj in archivos:
        print(f"   - {obj['Key']}")
else:
    print("No se encontraron archivos con ese prefijo")
```

**Resultado esperado**:
```
📂 Archivos encontrados: 1
   - 2025/01/15/ventas.csv
```

---

### Solución Ejercicio 3

```python
import boto3
import pandas as pd

s3_client = boto3.client('s3')

bucket = "fintech-data"
s3_key = "raw/transacciones_2025-01-15.csv"
archivo_local = "transacciones_descargadas.csv"

# Descargar archivo
s3_client.download_file(bucket, s3_key, archivo_local)
print(f"✅ Archivo descargado: {archivo_local}")

# Leer con pandas
df = pd.read_csv(archivo_local)
print(f"\n📊 Primeras 5 filas:")
print(df.head())
```

---

### Solución Ejercicio 4

```python
def lambda_handler(event, context):
    """Lambda simple que retorna mensaje."""
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
```

---

### Solución Ejercicio 5

```python
def lambda_handler(event, context):
    """Lambda que lee parámetro."""
    nombre = event.get('nombre', 'Anónimo')

    return {
        'statusCode': 200,
        'body': {
            'mensaje': f'Hello {nombre}!'
        }
    }
```

---

### Solución Ejercicio 6

```sql
SELECT COUNT(*) as total_entregas
FROM entregas
WHERE origen = 'Madrid'
  AND destino = 'Barcelona';
```

---

### Solución Ejercicio 7

```python
import boto3
import pandas as pd
from io import StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda que calcula métricas de CSV."""

    bucket = "restaurant-data"
    key = "ventas_2025-01-15.csv"

    # Leer CSV desde S3
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    csv_content = obj['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_content))

    # Calcular métricas
    total_productos = len(df)
    unidades_vendidas = df['cantidad'].sum()
    ventas_totales = (df['cantidad'] * df['precio']).sum()

    return {
        'statusCode': 200,
        'body': {
            'total_productos': int(total_productos),
            'unidades_vendidas': int(unidades_vendidas),
            'ventas_totales': float(ventas_totales)
        }
    }
```

---

### Solución Ejercicio 8

```bash
aws glue create-crawler \
  --name cloudapi-crawler \
  --role AWSGlueServiceRole-CloudAPI \
  --database-name cloudapi_db \
  --targets '{"S3Targets": [{"Path": "s3://cloudapi-logs/raw/"}]}' \
  --schedule "cron(0 2 * * ? *)"
```

---

### Solución Ejercicio 9

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS fintech_db.transacciones (
    transaccion_id STRING,
    timestamp TIMESTAMP,
    usuario_id STRING,
    monto DECIMAL(10,2)
)
STORED AS PARQUET
LOCATION 's3://fintech-data/transacciones/';
```

---

### Solución Ejercicio 10

```sql
SELECT
    u.nombre,
    SUM(t.monto) as total_transacciones
FROM transacciones t
JOIN usuarios u ON t.usuario_id = u.usuario_id
GROUP BY u.nombre
ORDER BY total_transacciones DESC;
```

---

### Solución Ejercicio 11

```python
# Glue Job PySpark

from pyspark.sql import functions as F

# Leer datos
df = spark.read.parquet("s3://logistic-data/entregas.parquet")

# Agregar columnas de particionamiento
df = df.withColumn("año", F.year("fecha_entrega"))
df = df.withColumn("mes", F.month("fecha_entrega"))
df = df.withColumn("dia", F.day("fecha_entrega"))

# Escribir particionado
df.write\
  .mode("overwrite")\
  .partitionBy("año", "mes", "dia")\
  .parquet("s3://logistic-data/entregas/")
```

---

### Solución Ejercicio 12

**Lifecycle Policy (JSON)**:
```json
{
  "Rules": [
    {
      "Id": "TransicionarLogs",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 120,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**Cálculo de ahorro**:
```
100GB nuevos/mes durante 1 año = 1200GB total

Sin Lifecycle Policy (todo en S3 Standard):
1200GB × 0.023 $/GB/mes × 12 meses = 331.20 $/año

Con Lifecycle Policy:
- Mes 1: 100GB × 1 mes × 0.023 = 2.30 $
- Mes 2-4: 300GB × 3 meses × 0.0125 = 11.25 $
- Mes 5-12: 900GB × 8 meses × 0.004 = 28.80 $
Total: 42.35 $/año

Ahorro: 331.20 - 42.35 = 288.85 $/año (87% reducción!)
```

---

### Solución Ejercicio 13

```python
# glue_job_transacciones.py

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. Leer JSON
df = spark.read.json("s3://fintech/raw/transacciones/")

# 2. Filtrar monto > 0
df = df.filter(F.col("monto") > 0)

# 3. Convertir timestamp a fecha
df = df.withColumn("fecha", F.to_date("timestamp"))

# 4. Agregar columnas de particionamiento
df = df.withColumn("año", F.year("timestamp"))
df = df.withColumn("mes", F.month("timestamp"))
df = df.withColumn("dia", F.day("timestamp"))

# 5. Categoría de monto
df = df.withColumn(
    "categoria_monto",
    F.when(F.col("monto") < 10, "bajo")
     .when(F.col("monto") <= 100, "medio")
     .otherwise("alto")
)

# 6. Guardar en Parquet particionado
df.write\
  .mode("overwrite")\
  .partitionBy("año", "mes", "dia")\
  .parquet("s3://fintech/processed/transacciones/")

job.commit()
```

---

### Solución Ejercicio 14

**Ver Ejemplo 5 en [02-EJEMPLOS.md](./02-EJEMPLOS.md)** para la implementación completa.

Componentes:
1. ✅ Lambda de validación
2. ✅ Trigger S3
3. ✅ Glue Job
4. ✅ Tabla Athena
5. ✅ Query de ejemplo

---

### Solución Ejercicio 15

**Mejoras propuestas**:

1. **Particionamiento por fecha**
   - Reducción: 10TB → 35GB (1 día)
   - Factor: 285x

2. **Convertir a Parquet con Snappy**
   - Reducción: 35GB → 7GB
   - Factor: 5x

3. **SELECT solo columnas necesarias (30%)**
   - Reducción: 7GB → 2.1GB
   - Factor: 3.3x

**Cálculo de costo nuevo**:
```
1000 queries/día × 30 días = 30,000 queries/mes
30,000 queries × 2.1GB/query × 5 $/TB
= 30,000 × 0.0021 TB × 5 $
= 315 $/mes
```

**Reducción: 50,000 $ → 315 $ = 99.4% de ahorro!** 🎉

**Query optimizada**:
```sql
-- Antes (malo)
SELECT *
FROM entregas
WHERE fecha = '2025-01-15';

-- Después (bueno)
SELECT entrega_id, origen, destino, distancia_km
FROM entregas
WHERE año = 2025
  AND mes = 1
  AND dia = 15;
```

---

## Tabla de Autoevaluación

| Ejercicio | Completado | Correcto | Tiempo | Notas |
|-----------|------------|----------|--------|-------|
| 1         | [ ]        | [ ]      |        |       |
| 2         | [ ]        | [ ]      |        |       |
| 3         | [ ]        | [ ]      |        |       |
| 4         | [ ]        | [ ]      |        |       |
| 5         | [ ]        | [ ]      |        |       |
| 6         | [ ]        | [ ]      |        |       |
| 7         | [ ]        | [ ]      |        |       |
| 8         | [ ]        | [ ]      |        |       |
| 9         | [ ]        | [ ]      |        |       |
| 10        | [ ]        | [ ]      |        |       |
| 11        | [ ]        | [ ]      |        |       |
| 12        | [ ]        | [ ]      |        |       |
| 13        | [ ]        | [ ]      |        |       |
| 14        | [ ]        | [ ]      |        |       |
| 15        | [ ]        | [ ]      |        |       |

---

**Siguiente paso:** [04-proyecto-practico](./04-proyecto-practico/) - Proyecto final: Pipeline ETL Serverless

**Última actualización:** 2025-11-09
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
