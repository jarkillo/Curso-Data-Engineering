# Ejemplos Prácticos: AWS para Data Engineering

En esta sección trabajaremos 5 ejemplos reales de pipelines en AWS, desde lo más básico hasta arquitecturas completas de producción.

---

## Ejemplo 1: Subir Datos a S3 con boto3 - Nivel: Básico

### Contexto

**RestaurantData Co.** es una red de restaurantes que genera archivos CSV diarios con las ventas de cada local. Actualmente guardan estos archivos en un disco duro local, pero quieren migrar a la nube para:
- Acceso desde cualquier lugar
- Backup automático
- Reducir costos de almacenamiento

**Tu tarea:** Crear un script Python que suba automáticamente los archivos CSV a Amazon S3.

### Datos

Archivo de ventas del 2025-01-15:

```csv
fecha,local,producto,cantidad,precio_unitario
2025-01-15,Madrid Centro,Pizza Margarita,45,8.50
2025-01-15,Madrid Centro,Ensalada César,23,6.00
2025-01-15,Barcelona Born,Pizza Pepperoni,38,9.00
2025-01-15,Barcelona Born,Pasta Carbonara,41,7.50
2025-01-15,Valencia Centro,Pizza 4 Quesos,29,9.50
```

### Paso 1: Instalar boto3 (AWS SDK para Python)

```bash
pip install boto3
```

### Paso 2: Configurar credenciales de AWS

**Opción A: AWS CLI** (recomendado)
```bash
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region: us-east-1
# Default output format: json
```

**Opción B: Variables de entorno**
```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
```

### Paso 3: Crear bucket de S3

**Desde AWS CLI:**
```bash
aws s3 mb s3://restaurantdata-ventas-raw --region us-east-1
```

**Desde consola web:**
1. AWS Console → S3 → Create bucket
2. Bucket name: `restaurantdata-ventas-raw`
3. Region: `us-east-1`
4. Block all public access: ✅ (por seguridad)
5. Create bucket

### Paso 4: Script Python para subir archivo

```python
# upload_to_s3.py

import boto3
from pathlib import Path
from datetime import datetime
from typing import Optional

def subir_archivo_s3(
    archivo_local: str,
    bucket: str,
    prefijo: str = "raw",
    region: str = "us-east-1"
) -> dict:
    """
    Sube un archivo local a Amazon S3.

    Args:
        archivo_local: Ruta del archivo en tu PC
        bucket: Nombre del bucket S3
        prefijo: Prefijo/carpeta en S3 (ej: "raw", "processed")
        region: Región de AWS

    Returns:
        Diccionario con información de la subida

    Examples:
        >>> resultado = subir_archivo_s3(
        ...     "ventas_2025-01-15.csv",
        ...     "restaurantdata-ventas-raw"
        ... )
        >>> print(resultado['s3_key'])
        raw/2025/01/15/ventas_2025-01-15.csv
    """
    # Inicializar cliente S3
    s3_client = boto3.client('s3', region_name=region)

    # Obtener fecha actual para organizar por año/mes/día
    fecha = datetime.now()

    # Construir key (ruta) en S3 con particionamiento
    # Ejemplo: raw/2025/01/15/ventas_2025-01-15.csv
    archivo_path = Path(archivo_local)
    s3_key = f"{prefijo}/{fecha.year:04d}/{fecha.month:02d}/{fecha.day:02d}/{archivo_path.name}"

    try:
        # Subir archivo
        s3_client.upload_file(
            Filename=archivo_local,
            Bucket=bucket,
            Key=s3_key
        )

        # Obtener tamaño del archivo
        tamaño = archivo_path.stat().st_size

        print(f"✅ Archivo subido exitosamente")
        print(f"   S3 URI: s3://{bucket}/{s3_key}")
        print(f"   Tamaño: {tamaño:,} bytes")

        return {
            'success': True,
            'bucket': bucket,
            's3_key': s3_key,
            's3_uri': f"s3://{bucket}/{s3_key}",
            'tamaño_bytes': tamaño
        }

    except Exception as e:
        print(f"❌ Error al subir archivo: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def listar_archivos_bucket(bucket: str, prefijo: str = "") -> list[dict]:
    """
    Lista archivos en un bucket S3.

    Args:
        bucket: Nombre del bucket
        prefijo: Filtrar por prefijo (ej: "raw/2025/01/")

    Returns:
        Lista de diccionarios con información de cada archivo
    """
    s3_client = boto3.client('s3')

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefijo
        )

        archivos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                archivos.append({
                    'key': obj['Key'],
                    'tamaño_bytes': obj['Size'],
                    'ultima_modificacion': obj['LastModified']
                })

        print(f"📂 Archivos encontrados en s3://{bucket}/{prefijo}: {len(archivos)}")
        for archivo in archivos:
            print(f"   - {archivo['key']} ({archivo['tamaño_bytes']:,} bytes)")

        return archivos

    except Exception as e:
        print(f"❌ Error al listar archivos: {e}")
        return []


# Ejemplo de uso
if __name__ == "__main__":
    # Subir archivo de ventas
    resultado = subir_archivo_s3(
        archivo_local="ventas_2025-01-15.csv",
        bucket="restaurantdata-ventas-raw",
        prefijo="raw"
    )

    if resultado['success']:
        print(f"\n📍 Ubicación en S3: {resultado['s3_uri']}")

        # Listar archivos en el bucket
        print("\n" + "="*60)
        listar_archivos_bucket(
            bucket="restaurantdata-ventas-raw",
            prefijo="raw/2025/01/"
        )
```

### Resultado

```
✅ Archivo subido exitosamente
   S3 URI: s3://restaurantdata-ventas-raw/raw/2025/01/15/ventas_2025-01-15.csv
   Tamaño: 1,234 bytes

============================================================
📂 Archivos encontrados en s3://restaurantdata-ventas-raw/raw/2025/01/: 15
   - raw/2025/01/01/ventas_2025-01-01.csv (1,145 bytes)
   - raw/2025/01/02/ventas_2025-01-02.csv (1,287 bytes)
   ...
   - raw/2025/01/15/ventas_2025-01-15.csv (1,234 bytes)
```

### Interpretación

**Logros:**
1. ✅ Archivos organizados por fecha (año/mes/día) → fácil de buscar
2. ✅ Backup automático en S3 (durabilidad 99.999999999%)
3. ✅ Accesible desde cualquier lugar con credenciales AWS
4. ✅ Costo: ~0.02 $/mes para 1GB de datos

**Decisiones de negocio:**
- **Automatizar**: Ejecutar este script diariamente con cron/Task Scheduler
- **Monitorear**: Crear alerta si la subida falla
- **Siguiente paso**: Lambda para validar automáticamente los CSV

---

## Ejemplo 2: Lambda para Validar CSV en S3 - Nivel: Intermedio

### Contexto

**CloudAPI Systems** recibe logs de APIs de clientes en formato JSON. Algunos clientes envían archivos corruptos o con formato incorrecto, causando errores en el pipeline.

**Tu tarea:** Crear una función Lambda que se ejecute automáticamente cuando un archivo JSON llegue a S3, valide su estructura, y mueva archivos válidos a otra carpeta.

### Datos

Ejemplo de log válido (`api_logs_2025-01-15.json`):

```json
[
  {
    "timestamp": "2025-01-15T10:23:45Z",
    "endpoint": "/api/users",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 145
  },
  {
    "timestamp": "2025-01-15T10:24:12Z",
    "endpoint": "/api/products",
    "method": "POST",
    "status_code": 201,
    "response_time_ms": 230
  }
]
```

Ejemplo de log inválido (falta `status_code`):

```json
[
  {
    "timestamp": "2025-01-15T10:23:45Z",
    "endpoint": "/api/users",
    "method": "GET",
    "response_time_ms": 145
  }
]
```

### Paso 1: Crear bucket con carpetas

```bash
aws s3 mb s3://cloudapi-logs

# Estructura:
# s3://cloudapi-logs/
# ├── incoming/     (archivos que llegan)
# ├── validated/    (archivos válidos)
# └── invalid/      (archivos inválidos)
```

### Paso 2: Código de la función Lambda

```python
# lambda_validator.py

import boto3
import json
from datetime import datetime
from typing import Dict, List

s3_client = boto3.client('s3')

# Schema esperado
REQUIRED_FIELDS = ['timestamp', 'endpoint', 'method', 'status_code', 'response_time_ms']


def validar_log_api(log: dict) -> tuple[bool, str]:
    """
    Valida que un log tenga todos los campos requeridos.

    Args:
        log: Diccionario con un evento de log

    Returns:
        (es_valido, mensaje_error)
    """
    # Validar campos requeridos
    for field in REQUIRED_FIELDS:
        if field not in log:
            return False, f"Campo faltante: {field}"

    # Validar tipos de datos
    if not isinstance(log['status_code'], int):
        return False, "status_code debe ser entero"

    if not isinstance(log['response_time_ms'], (int, float)):
        return False, "response_time_ms debe ser numérico"

    # Validar rangos
    if log['status_code'] < 100 or log['status_code'] > 599:
        return False, f"status_code inválido: {log['status_code']}"

    if log['response_time_ms'] < 0:
        return False, "response_time_ms no puede ser negativo"

    return True, "OK"


def lambda_handler(event, context):
    """
    Handler de Lambda que se ejecuta al subir archivo a S3.

    Event structure (S3 trigger):
    {
        "Records": [{
            "s3": {
                "bucket": {"name": "cloudapi-logs"},
                "object": {"key": "incoming/api_logs_2025-01-15.json"}
            }
        }]
    }
    """
    # Obtener información del archivo subido
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    print(f"🔍 Validando archivo: s3://{bucket}/{key}")

    try:
        # 1. Descargar archivo desde S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        # 2. Parsear JSON
        logs = json.loads(content)

        # 3. Validar cada log
        logs_validos = 0
        logs_invalidos = 0
        errores = []

        for i, log in enumerate(logs):
            es_valido, mensaje = validar_log_api(log)
            if es_valido:
                logs_validos += 1
            else:
                logs_invalidos += 1
                errores.append(f"Log #{i+1}: {mensaje}")

        # 4. Decidir si el archivo es válido (tolerancia: <5% errores)
        total_logs = len(logs)
        porcentaje_error = (logs_invalidos / total_logs) * 100 if total_logs > 0 else 0

        if porcentaje_error < 5:
            # Archivo válido → mover a validated/
            nuevo_key = key.replace('incoming/', 'validated/')
            s3_client.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=nuevo_key
            )
            s3_client.delete_object(Bucket=bucket, Key=key)

            print(f"✅ Archivo válido movido a: s3://{bucket}/{nuevo_key}")
            print(f"   Logs válidos: {logs_validos}/{total_logs}")

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'valid',
                    'total_logs': total_logs,
                    'logs_validos': logs_validos,
                    'nuevo_ubicacion': f"s3://{bucket}/{nuevo_key}"
                })
            }
        else:
            # Archivo inválido → mover a invalid/
            nuevo_key = key.replace('incoming/', 'invalid/')
            s3_client.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=nuevo_key
            )
            s3_client.delete_object(Bucket=bucket, Key=key)

            # Guardar reporte de errores
            reporte_key = nuevo_key.replace('.json', '_errors.txt')
            reporte = f"Archivo inválido: {porcentaje_error:.1f}% de errores\n\n"
            reporte += "\n".join(errores)

            s3_client.put_object(
                Bucket=bucket,
                Key=reporte_key,
                Body=reporte.encode('utf-8')
            )

            print(f"❌ Archivo inválido movido a: s3://{bucket}/{nuevo_key}")
            print(f"   Reporte: s3://{bucket}/{reporte_key}")

            return {
                'statusCode': 400,
                'body': json.dumps({
                    'status': 'invalid',
                    'total_logs': total_logs,
                    'logs_invalidos': logs_invalidos,
                    'porcentaje_error': porcentaje_error,
                    'ubicacion_archivo': f"s3://{bucket}/{nuevo_key}",
                    'reporte_errores': f"s3://{bucket}/{reporte_key}"
                })
            }

    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON: {e}")
        # Mover a invalid/
        nuevo_key = key.replace('incoming/', 'invalid/')
        s3_client.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': key},
            Key=nuevo_key
        )
        s3_client.delete_object(Bucket=bucket, Key=key)

        return {
            'statusCode': 400,
            'body': json.dumps({
                'status': 'parse_error',
                'error': str(e)
            })
        }

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'error': str(e)
            })
        }
```

### Paso 3: Configurar Lambda en AWS

**Desde AWS Console:**

1. **Crear función Lambda:**
   - Lambda → Create function
   - Function name: `ValidarLogsAPI`
   - Runtime: Python 3.11
   - Execution role: Create new role with S3 permissions

2. **Subir código:**
   - Copiar `lambda_validator.py` en el editor de Lambda
   - Deploy

3. **Configurar trigger S3:**
   - Add trigger → S3
   - Bucket: `cloudapi-logs`
   - Event type: `PUT`
   - Prefix: `incoming/`
   - Suffix: `.json`

4. **Configurar permisos IAM:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject",
           "s3:CopyObject"
         ],
         "Resource": "arn:aws:s3:::cloudapi-logs/*"
       }
     ]
   }
   ```

### Paso 4: Probar

**Subir archivo válido:**
```bash
aws s3 cp api_logs_valido.json s3://cloudapi-logs/incoming/
```

**Logs de Lambda:**
```
🔍 Validando archivo: s3://cloudapi-logs/incoming/api_logs_valido.json
✅ Archivo válido movido a: s3://cloudapi-logs/validated/api_logs_valido.json
   Logs válidos: 150/150
```

**Subir archivo inválido:**
```bash
aws s3 cp api_logs_invalido.json s3://cloudapi-logs/incoming/
```

**Logs de Lambda:**
```
🔍 Validando archivo: s3://cloudapi-logs/incoming/api_logs_invalido.json
❌ Archivo inválido movido a: s3://cloudapi-logs/invalid/api_logs_invalido.json
   Reporte: s3://cloudapi-logs/invalid/api_logs_invalido_errors.txt
```

### Resultado

**Estructura final de S3:**
```
s3://cloudapi-logs/
├── incoming/              (vacío - archivos se mueven automáticamente)
├── validated/
│   ├── api_logs_2025-01-15.json
│   └── api_logs_2025-01-16.json
└── invalid/
    ├── api_logs_corrupto.json
    └── api_logs_corrupto_errors.txt
```

### Interpretación

**Logros:**
1. ✅ **Validación automática** - 0 intervención manual
2. ✅ **Separación de datos** - Válidos vs Inválidos
3. ✅ **Reportes de errores** - Fácil debugging
4. ✅ **Escalable** - Maneja 1 o 10,000 archivos/día

**Métricas de éxito:**
- Antes: 15% de archivos corruptos llegaban al pipeline → errores
- Después: 0% de archivos corruptos en pipeline

**Decisiones de negocio:**
- Notificar al cliente cuando su archivo es inválido (enviar email con SNS)
- Dashboard con % de archivos válidos por cliente
- SLA: "Validaremos tu archivo en <1 minuto"

**Costos:**
- Lambda: 1M ejecuciones gratis/mes → 0 $ (Free Tier)
- S3: ~0.05 $/mes para 10GB

---

## Ejemplo 3: Glue Job para Transformar Logs - Nivel: Intermedio-Avanzado

### Contexto

**LogisticFlow** tiene millones de registros de entregas en formato JSON. Necesitan:
- Convertir JSON a Parquet (reducir tamaño 80%)
- Calcular métricas (tiempo promedio de entrega por región)
- Particionar por fecha para queries rápidas en Athena

**Tu tarea:** Crear un Glue Job que procese 500GB de logs diarios.

### Datos

Formato JSON raw (`entregas_2025-01-15.json`):

```json
{
  "entrega_id": "E-2025-001234",
  "timestamp_recogida": "2025-01-15T08:30:00Z",
  "timestamp_entrega": "2025-01-15T10:45:00Z",
  "origen": "Madrid",
  "destino": "Barcelona",
  "distancia_km": 625,
  "estado": "entregado"
}
```

### Paso 1: Crear Glue Data Catalog con Crawler

**Configurar Crawler:**
```bash
# Crear crawler desde CLI
aws glue create-crawler \
  --name entregas-raw-crawler \
  --role AWSGlueServiceRole-LogisticFlow \
  --database-name logisticflow_db \
  --targets '{"S3Targets": [{"Path": "s3://logisticflow-data/raw/entregas/"}]}' \
  --schedule "cron(0 1 * * ? *)"  # Ejecutar diariamente a 1am
```

**Ejecutar crawler:**
```bash
aws glue start-crawler --name entregas-raw-crawler
```

**Resultado:** Tabla `entregas_raw` creada en Glue Catalog.

### Paso 2: Script PySpark para Glue Job

```python
# glue_job_transformar_entregas.py

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Inicializar Glue Context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("🚀 Iniciando transformación de entregas...")

# ============================================================================
# PASO 1: Leer datos raw desde S3 (usando Glue Catalog)
# ============================================================================

print("📥 Leyendo datos raw desde Glue Catalog...")

datasource = glueContext.create_dynamic_frame.from_catalog(
    database="logisticflow_db",
    table_name="entregas_raw"
)

# Convertir a Spark DataFrame para transformaciones complejas
df_raw = datasource.toDF()

print(f"   ✓ Leídos {df_raw.count():,} registros")
df_raw.printSchema()

# ============================================================================
# PASO 2: Transformaciones
# ============================================================================

print("🔧 Aplicando transformaciones...")

# 2.1 Calcular duración de entrega (minutos)
df_transformed = df_raw.withColumn(
    "duracion_minutos",
    (
        F.unix_timestamp("timestamp_entrega") -
        F.unix_timestamp("timestamp_recogida")
    ) / 60
)

# 2.2 Extraer fecha y hora para particionamiento
df_transformed = df_transformed\
    .withColumn("fecha", F.to_date("timestamp_entrega"))\
    .withColumn("año", F.year("timestamp_entrega"))\
    .withColumn("mes", F.month("timestamp_entrega"))\
    .withColumn("dia", F.day("timestamp_entrega"))

# 2.3 Categorizar por velocidad de entrega
df_transformed = df_transformed.withColumn(
    "velocidad_categoria",
    F.when(F.col("duracion_minutos") <= 60, "express")
     .when(F.col("duracion_minutos") <= 180, "standard")
     .otherwise("slow")
)

# 2.4 Filtrar entregas válidas (estado = 'entregado')
df_transformed = df_transformed.filter(F.col("estado") == "entregado")

# 2.5 Eliminar duplicados
df_transformed = df_transformed.dropDuplicates(["entrega_id"])

print(f"   ✓ Registros después de transformación: {df_transformed.count():,}")

# ============================================================================
# PASO 3: Calcular métricas agregadas
# ============================================================================

print("📊 Calculando métricas agregadas...")

df_metricas_region = df_transformed.groupBy("origen", "destino", "fecha").agg(
    F.count("entrega_id").alias("total_entregas"),
    F.avg("duracion_minutos").alias("duracion_promedio_min"),
    F.min("duracion_minutos").alias("duracion_min_min"),
    F.max("duracion_minutos").alias("duracion_max_min"),
    F.avg("distancia_km").alias("distancia_promedio_km"),
    F.countDistinct(
        F.when(F.col("velocidad_categoria") == "express", F.col("entrega_id"))
    ).alias("entregas_express")
)

print("   ✓ Métricas por región calculadas")
df_metricas_region.show(10, truncate=False)

# ============================================================================
# PASO 4: Guardar datos procesados en S3 (Parquet)
# ============================================================================

print("💾 Guardando datos procesados en S3...")

# 4.1 Guardar tabla detallada (particionada por fecha)
output_path_detalle = "s3://logisticflow-data/processed/entregas_detalle/"

df_transformed.write\
    .mode("overwrite")\
    .partitionBy("año", "mes", "dia")\
    .parquet(output_path_detalle)

print(f"   ✓ Entregas detalladas guardadas en: {output_path_detalle}")

# 4.2 Guardar tabla de métricas
output_path_metricas = "s3://logisticflow-data/processed/metricas_region/"

df_metricas_region.write\
    .mode("overwrite")\
    .partitionBy("fecha")\
    .parquet(output_path_metricas)

print(f"   ✓ Métricas guardadas en: {output_path_metricas}")

# ============================================================================
# PASO 5: Actualizar Glue Catalog con nuevas tablas
# ============================================================================

print("📚 Actualizando Glue Data Catalog...")

# Crear/actualizar tabla de entregas procesadas
glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [output_path_detalle]},
    format="parquet"
).toDF().createOrReplaceTempView("entregas_procesadas")

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS logisticflow_db.entregas_procesadas
    USING PARQUET
    PARTITIONED BY (año, mes, dia)
    LOCATION '{output_path_detalle}'
""")

print("   ✓ Tabla 'entregas_procesadas' actualizada en Catalog")

# Crear/actualizar tabla de métricas
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS logisticflow_db.metricas_region
    USING PARQUET
    PARTITIONED BY (fecha)
    LOCATION '{output_path_metricas}'
""")

print("   ✓ Tabla 'metricas_region' actualizada en Catalog")

# ============================================================================
# FINALIZAR
# ============================================================================

job.commit()
print("✅ Glue Job completado exitosamente!")
```

### Paso 3: Crear y Ejecutar Glue Job desde AWS Console

1. **AWS Glue → ETL → Jobs → Add Job**
   - Name: `TransformarEntregas`
   - IAM Role: `AWSGlueServiceRole-LogisticFlow`
   - Type: Spark
   - Glue version: 4.0
   - Language: Python 3
   - Script: Subir `glue_job_transformar_entregas.py`

2. **Configurar recursos:**
   - DPU (Data Processing Units): 10 (para 500GB)
   - Timeout: 60 minutos
   - Max retries: 1

3. **Ejecutar:**
   ```bash
   aws glue start-job-run --job-name TransformarEntregas
   ```

### Resultado

**CloudWatch Logs:**
```
🚀 Iniciando transformación de entregas...
📥 Leyendo datos raw desde Glue Catalog...
   ✓ Leídos 2,435,789 registros
🔧 Aplicando transformaciones...
   ✓ Registros después de transformación: 2,401,234
📊 Calculando métricas agregadas...
   ✓ Métricas por región calculadas
💾 Guardando datos procesados en S3...
   ✓ Entregas detalladas guardadas en: s3://logisticflow-data/processed/entregas_detalle/
   ✓ Métricas guardadas en: s3://logisticflow-data/processed/metricas_region/
📚 Actualizando Glue Data Catalog...
   ✓ Tabla 'entregas_procesadas' actualizada en Catalog
   ✓ Tabla 'metricas_region' actualizada en Catalog
✅ Glue Job completado exitosamente!

Duración: 18 minutos
DPUs consumidos: 10 DPUs * 0.3 horas = 3 DPU-hours
Costo: 3 * 0.44 $ = 1.32 $
```

**Estructura S3 después del job:**
```
s3://logisticflow-data/
├── raw/
│   └── entregas/
│       ├── 2025-01-15.json (500 GB JSON)
│       └── ...
└── processed/
    ├── entregas_detalle/ (100 GB Parquet - 80% reducción!)
    │   ├── año=2025/mes=01/dia=15/*.parquet
    │   └── ...
    └── metricas_region/ (500 MB Parquet)
        ├── fecha=2025-01-15/*.parquet
        └── ...
```

### Interpretación

**Logros:**
1. ✅ **Reducción de tamaño: 80%** (500GB → 100GB)
   - JSON sin comprimir: 500GB
   - Parquet comprimido: 100GB
   - **Ahorro anual:** ~180 $ en almacenamiento

2. ✅ **Velocidad de queries 50x mayor**
   - Query en JSON: 5 minutos
   - Query en Parquet particionado: 6 segundos

3. ✅ **Métricas precalculadas**
   - Antes: Calcular métricas en cada query (lento)
   - Después: Métricas ya calculadas (tabla `metricas_region`)

4. ✅ **Escalable**
   - Procesa 500GB en 18 minutos
   - Si mañana son 5TB, Glue escala automáticamente

**Decisiones de negocio:**
- **Automatizar**: Ejecutar este job diariamente a 2am
- **Monitorear**: Dashboard de Glue para ver jobs fallidos
- **Siguiente paso**: Athena para queries analíticas sobre Parquet

**ROI (Return on Investment):**
- **Costo Glue Job:** 1.32 $/día × 30 días = 39.60 $/mes
- **Ahorro en queries Athena:** ~200 $/mes (50x menos datos escaneados)
- **Ahorro neto:** 160 $/mes

---

## Ejemplo 4: Athena para Analytics sobre Parquet - Nivel: Avanzado

### Contexto

**FinTech Analytics** tiene transacciones financieras en S3 (Parquet, 2TB). El equipo de analytics necesita responder preguntas de negocio con SQL.

**Tu tarea:** Configurar Athena para hacer queries analíticas rápidas y baratas.

### Datos

Ya procesados por Glue Job (Parquet en S3):

```
s3://fintech-data/processed/transacciones/
├── año=2025/mes=01/dia=15/transacciones.parquet
└── ...
```

Schema:
```
transaccion_id: string
timestamp: timestamp
usuario_id: string
tipo: string (compra, transferencia, retiro)
monto: decimal(10,2)
moneda: string (EUR, USD)
comercio: string
categoria: string (alimentacion, transporte, etc.)
```

### Paso 1: Crear tabla en Athena desde Glue Catalog

La tabla ya existe en Glue Catalog (creada por Glue Job anterior). Athena la detecta automáticamente.

**Verificar tabla:**
```sql
-- Athena Query Editor

SHOW TABLES IN fintech_db;

-- Resultado:
-- transacciones
```

**Ver schema:**
```sql
DESCRIBE fintech_db.transacciones;

-- Resultado:
-- transaccion_id     string
-- timestamp          timestamp
-- usuario_id         string
-- tipo               string
-- monto              decimal(10,2)
-- moneda             string
-- comercio           string
-- categoria          string
-- año                int       (particion)
-- mes                int       (particion)
-- dia                int       (particion)
```

### Paso 2: Queries Analíticas

#### Query 1: Transacciones totales por categoría (enero 2025)

```sql
SELECT
    categoria,
    COUNT(*) as total_transacciones,
    SUM(monto) as monto_total_eur,
    AVG(monto) as monto_promedio_eur,
    ROUND(SUM(monto) / (SELECT SUM(monto) FROM transacciones WHERE año=2025 AND mes=1) * 100, 2) as porcentaje_total
FROM transacciones
WHERE año = 2025
  AND mes = 1
  AND moneda = 'EUR'
GROUP BY categoria
ORDER BY monto_total_eur DESC
LIMIT 10;
```

**Resultado:**
```
categoria        | total_transacciones | monto_total_eur | monto_promedio_eur | porcentaje_total
-----------------|---------------------|-----------------|--------------------|-----------------
Alimentación     |         1,234,567   |    12,456,789.50|              10.09 |            18.5%
Transporte       |           987,654   |     9,876,543.21|               9.99 |            14.7%
Ocio             |           765,432   |     8,765,432.10|              11.45 |            13.0%
Hogar            |           543,210   |     6,543,210.99|              12.04 |             9.7%
Salud            |           321,098   |     4,321,098.88|              13.46 |             6.4%
...
```

**Datos escaneados:** 50GB (solo particiones de enero)
**Costo:** 0.25 $ (5 $/TB × 0.05 TB)
**Tiempo:** 8 segundos

#### Query 2: Usuarios con mayor gasto en los últimos 7 días

```sql
WITH ultimos_7_dias AS (
    SELECT *
    FROM transacciones
    WHERE timestamp >= CURRENT_DATE - INTERVAL '7' DAY
      AND tipo = 'compra'
)
SELECT
    usuario_id,
    COUNT(*) as num_compras,
    SUM(monto) as gasto_total_eur,
    MAX(monto) as compra_maxima_eur,
    ROUND(AVG(monto), 2) as ticket_promedio_eur
FROM ultimos_7_dias
WHERE moneda = 'EUR'
GROUP BY usuario_id
HAVING SUM(monto) > 1000  -- Solo usuarios con >1000€ gastados
ORDER BY gasto_total_eur DESC
LIMIT 100;
```

**Resultado:**
```
usuario_id        | num_compras | gasto_total_eur | compra_maxima_eur | ticket_promedio_eur
------------------|-------------|-----------------|-------------------|--------------------
USR-001234        |         145 |        5,678.90 |            450.00 |               39.16
USR-005678        |          89 |        4,321.50 |            890.00 |               48.55
USR-009012        |         234 |        3,987.20 |            320.00 |               17.03
...
```

**Uso:** Detectar usuarios VIP para enviar ofertas personalizadas.

#### Query 3: Detección de anomalías (transacciones >3 desviaciones estándar)

```sql
WITH stats AS (
    SELECT
        categoria,
        AVG(monto) as media,
        STDDEV(monto) as desviacion_estandar
    FROM transacciones
    WHERE año = 2025 AND mes = 1
    GROUP BY categoria
),
transacciones_con_stats AS (
    SELECT
        t.*,
        s.media,
        s.desviacion_estandar,
        (t.monto - s.media) / s.desviacion_estandar as z_score
    FROM transacciones t
    JOIN stats s ON t.categoria = s.categoria
    WHERE t.año = 2025 AND t.mes = 1
)
SELECT
    transaccion_id,
    timestamp,
    usuario_id,
    categoria,
    monto,
    ROUND(z_score, 2) as z_score,
    CASE
        WHEN z_score > 3 THEN 'Posible fraude'
        WHEN z_score < -3 THEN 'Anomalía negativa'
        ELSE 'Normal'
    END as clasificacion
FROM transacciones_con_stats
WHERE ABS(z_score) > 3
ORDER BY ABS(z_score) DESC
LIMIT 50;
```

**Resultado:**
```
transaccion_id  | timestamp           | usuario_id | categoria     | monto    | z_score | clasificacion
----------------|---------------------|------------|---------------|----------|---------|---------------
TXN-987654      | 2025-01-15 14:23:45 | USR-555666 | Alimentación  | 8,950.00 |   45.67 | Posible fraude
TXN-876543      | 2025-01-14 22:15:30 | USR-777888 | Ocio          | 12,500.00|   38.92 | Posible fraude
TXN-765432      | 2025-01-13 19:08:12 | USR-999000 | Transporte    |  3,200.00|   12.45 | Posible fraude
...
```

**Uso:** Equipo de fraude revisa estas transacciones manualmente.

#### Query 4: Análisis de cohortes (usuarios por mes de registro)

```sql
WITH primer_transaccion AS (
    SELECT
        usuario_id,
        DATE_TRUNC('month', MIN(timestamp)) as mes_registro
    FROM transacciones
    GROUP BY usuario_id
),
actividad_mensual AS (
    SELECT
        pt.mes_registro,
        DATE_TRUNC('month', t.timestamp) as mes_actividad,
        COUNT(DISTINCT t.usuario_id) as usuarios_activos
    FROM primer_transaccion pt
    JOIN transacciones t ON pt.usuario_id = t.usuario_id
    WHERE t.año = 2025
    GROUP BY pt.mes_registro, DATE_TRUNC('month', t.timestamp)
)
SELECT
    mes_registro,
    mes_actividad,
    usuarios_activos,
    ROUND(
        usuarios_activos * 100.0 /
        FIRST_VALUE(usuarios_activos) OVER (PARTITION BY mes_registro ORDER BY mes_actividad),
        2
    ) as retention_porcentaje
FROM actividad_mensual
ORDER BY mes_registro, mes_actividad;
```

**Resultado:**
```
mes_registro | mes_actividad | usuarios_activos | retention_porcentaje
-------------|---------------|------------------|---------------------
2024-10-01   | 2024-10-01    |          10,000  |              100.00%
2024-10-01   | 2024-11-01    |           7,500  |               75.00%
2024-10-01   | 2024-12-01    |           6,200  |               62.00%
2024-10-01   | 2025-01-01    |           5,800  |               58.00%
2024-11-01   | 2024-11-01    |          12,000  |              100.00%
2024-11-01   | 2024-12-01    |           9,600  |               80.00%
2024-11-01   | 2025-01-01    |           8,400  |               70.00%
...
```

**Insight:** Usuarios de octubre 2024 tienen 58% de retención después de 3 meses.

### Paso 3: Optimizar Costos con Vistas Materializadas

Para queries que se ejecutan frecuentemente, crear vista materializada:

```sql
CREATE TABLE fintech_db.metricas_diarias_cache
WITH (
    format = 'PARQUET',
    external_location = 's3://fintech-data/cache/metricas_diarias/',
    partitioned_by = ARRAY['fecha']
) AS
SELECT
    DATE(timestamp) as fecha,
    categoria,
    COUNT(*) as total_transacciones,
    SUM(monto) as monto_total,
    AVG(monto) as monto_promedio
FROM transacciones
WHERE timestamp >= CURRENT_DATE - INTERVAL '90' DAY
GROUP BY DATE(timestamp), categoria;
```

**Beneficio:**
- Query original: Escanea 200GB → 1 $
- Query en vista materializada: Escanea 500MB → 0.0025 $
- **400x más barato!**

### Resultado Final

**Performance:**
- ✅ Queries complejas en segundos (antes: minutos en MySQL)
- ✅ Costo por query: 0.001 $ - 1 $ (vs 50-200 $ en Redshift para el mismo volumen)
- ✅ Escalable: Maneja petabytes sin cambios

**Dashboard de negocio powered by Athena:**
```
📊 Métricas Enero 2025
├── Transacciones totales: 45.6M
├── Volumen total: 456M €
├── Ticket promedio: 10.00 €
├── Usuarios activos: 2.3M
└── Tasa de fraude: 0.03%
```

### Interpretación

**Decisiones de negocio basadas en datos:**

1. **Categoría "Alimentación" = 18.5% del gasto**
   → Lanzar programa de cashback en supermercados

2. **100 usuarios VIP gastan 250,000 €/mes**
   → Crear tarjeta premium exclusiva

3. **Retención baja en cohorte octubre (58%)**
   → Campaña de re-engagement para usuarios inactivos

4. **50 transacciones sospechosas detectadas**
   → Equipo de fraude las revisa en <24h

**ROI de Athena:**
- **Costo mensual queries:** ~150 $ (500 queries/día × 0.01 $/query × 30 días)
- **Alternativa (Redshift):** ~3,000 $/mes (cluster always-on)
- **Ahorro:** 2,850 $/mes = **34,200 $/año**

---

## Ejemplo 5: Pipeline Completo End-to-End - Nivel: Experto

### Contexto

**RestaurantData Co.** quiere un pipeline completo para analizar ventas en tiempo real.

**Requisitos:**
1. Archivos CSV llegan cada hora a S3
2. Lambda valida formato
3. Glue transforma a Parquet
4. Athena permite queries
5. Dashboard en tiempo real

### Arquitectura

```
┌──────────────────┐
│  Fuente de Datos │ (POS systems de restaurantes)
└────────┬─────────┘
         │ (cada hora, CSV)
         v
┌──────────────────┐
│  S3: Raw Bucket  │ s3://restaurant-data/raw/
└────────┬─────────┘
         │ (trigger)
         v
┌──────────────────┐
│  Lambda:         │ (valida CSV, schema, duplicados)
│  ValidarVentas   │
└────────┬─────────┘
         │ (si válido → processed/)
         v
┌──────────────────┐
│ S3: Processed    │ s3://restaurant-data/validated/
└────────┬─────────┘
         │ (trigger cada 4h)
         v
┌──────────────────┐
│  Glue Job:       │ (convierte CSV → Parquet)
│  TransformarCSV  │ (agrega métricas)
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ S3: Analytics    │ s3://restaurant-data/analytics/ (Parquet)
└────────┬─────────┘
         │
         v
┌──────────────────┐
│  Athena          │ (queries SQL)
└────────┬─────────┘
         │
         v
┌──────────────────┐
│  QuickSight /    │ (Dashboard)
│  Grafana         │
└──────────────────┘
```

### Implementación Completa

**(Por brevedad, solo muestro las partes clave. El código completo está en el proyecto práctico)**

#### Lambda de Validación

```python
# lambda_validar_ventas.py (versión simplificada)

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # 1. Leer CSV
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj['Body'])

    # 2. Validar schema
    required_cols = ['fecha', 'local', 'producto', 'cantidad', 'precio_unitario']
    if not all(col in df.columns for col in required_cols):
        mover_a_invalido(bucket, key)
        return {'statusCode': 400, 'body': 'Schema inválido'}

    # 3. Validar datos
    if df['cantidad'].min() < 0 or df['precio_unitario'].min() < 0:
        mover_a_invalido(bucket, key)
        return {'statusCode': 400, 'body': 'Valores negativos'}

    # 4. Eliminar duplicados
    df_clean = df.drop_duplicates()

    # 5. Guardar en validated/
    nuevo_key = key.replace('raw/', 'validated/')
    df_clean.to_csv(f'/tmp/cleaned.csv', index=False)
    s3.upload_file('/tmp/cleaned.csv', bucket, nuevo_key)

    return {'statusCode': 200, 'body': f'{len(df_clean)} filas validadas'}
```

#### Glue Job de Transformación

```python
# glue_job_ventas.py (versión simplificada)

# Leer CSV validados
df = glueContext.create_dynamic_frame.from_catalog(
    database="restaurant_db",
    table_name="ventas_validated"
).toDF()

# Transformar
df = df.withColumn("total", F.col("cantidad") * F.col("precio_unitario"))
df = df.withColumn("fecha_dt", F.to_date("fecha"))

# Calcular métricas por local y fecha
df_metricas = df.groupBy("local", "fecha_dt").agg(
    F.sum("total").alias("ventas_total"),
    F.count("*").alias("num_transacciones"),
    F.avg("total").alias("ticket_promedio")
)

# Guardar Parquet particionado
df.write.partitionBy("año", "mes").parquet("s3://restaurant-data/analytics/ventas/")
df_metricas.write.parquet("s3://restaurant-data/analytics/metricas/")
```

#### Query en Athena

```sql
-- Top 10 productos más vendidos (últimos 30 días)

SELECT
    producto,
    SUM(cantidad) as unidades_vendidas,
    SUM(cantidad * precio_unitario) as ingresos_totales
FROM restaurant_db.ventas_analytics
WHERE fecha >= CURRENT_DATE - INTERVAL '30' DAY
GROUP BY producto
ORDER BY ingresos_totales DESC
LIMIT 10;
```

### Resultado: Dashboard en Tiempo Real

**Métricas visibles en QuickSight:**
- 📈 Ventas del día: 45,678 € (+12% vs ayer)
- 🏆 Producto top: Pizza Margarita (1,234 unidades)
- 📍 Local top: Madrid Centro (12,345 € hoy)
- ⏰ Hora pico: 13:00-15:00 (35% de ventas)
- 📊 Tendencia semanal: +8% vs semana pasada

**Costos mensuales:**
- Lambda: 0 $ (Free Tier)
- Glue: 50 $ (2 jobs/día × 10 DPU × 0.3h × 0.44 $/DPU-h × 30 días)
- S3: 5 $ (500GB datos)
- Athena: 20 $ (100 queries/día × 0.01 $/query × 30 días)
- **Total: 75 $/mes** (vs 500 $/mes con servidor tradicional)

---

## Resumen de Ejemplos

| Ejemplo | Nivel | Servicios AWS | Caso de Uso |
|---------|-------|---------------|-------------|
| 1. Subir a S3 | Básico | S3, boto3 | Migrar archivos locales a cloud |
| 2. Lambda Validator | Intermedio | Lambda, S3 | Validación automática de archivos |
| 3. Glue Job | Intermedio-Avanzado | Glue, S3, Catalog | Transformación batch de datos |
| 4. Athena Analytics | Avanzado | Athena, S3, Parquet | Queries SQL sobre data lake |
| 5. Pipeline Completo | Experto | Todo | Arquitectura end-to-end de producción |

---

**Siguiente paso:** [03-EJERCICIOS.md](./03-EJERCICIOS.md) - Ejercicios para practicar

**Última actualización:** 2025-11-09
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
