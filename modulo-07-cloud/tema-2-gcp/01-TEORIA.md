# Tema 2: GCP para Data Engineering

## 📋 Información del Tema

- **Duración estimada:** 3-4 semanas
- **Nivel:** Intermedio-Avanzado
- **Prerrequisitos:** Tema 1 (AWS) completado, conocimientos de SQL
- **Proyecto práctico:** Pipeline de datos en tiempo real con GCP

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

- ✅ Almacenar y gestionar datos en **Cloud Storage**
- ✅ Ejecutar queries analíticas SQL con **BigQuery**
- ✅ Procesar datos batch y streaming con **Dataflow** (Apache Beam)
- ✅ Implementar ingesta en tiempo real con **Pub/Sub**
- ✅ Orquestar workflows con **Cloud Composer** (Apache Airflow managed)
- ✅ Calcular costos y optimizar uso de GCP
- ✅ Aplicar mejores prácticas de seguridad en GCP

---

## 📚 Contenido

### 1. Introducción a GCP para Data Engineering
### 2. Cloud Storage: El Data Lake de GCP
### 3. BigQuery: Data Warehouse Serverless
### 4. Dataflow: Procesamiento con Apache Beam
### 5. Pub/Sub: Mensajería para Streaming
### 6. Cloud Composer: Orquestación Managed

---

## 1. Introducción a GCP para Data Engineering

### ¿Qué es Google Cloud Platform (GCP)?

**Google Cloud Platform** es la plataforma cloud de Google que ofrece servicios de computación, almacenamiento, bases de datos, machine learning y más.

**¿Por qué GCP para Data Engineering?**

GCP destaca especialmente en:
- **BigQuery**: El data warehouse más rápido y escalable del mercado
- **Integración nativa**: Todos los servicios están diseñados para trabajar juntos
- **Serverless por defecto**: Menos gestión de infraestructura
- **Machine Learning**: Integración profunda con TensorFlow y Vertex AI
- **Costos competitivos**: Descuentos automáticos por uso sostenido

### Comparación GCP vs AWS

| Característica | GCP | AWS |
|----------------|-----|-----|
| **Data Warehouse** | BigQuery (serverless) | Redshift (con servidores) |
| **Procesamiento** | Dataflow (managed Beam) | Glue + EMR |
| **Object Storage** | Cloud Storage | S3 |
| **Streaming** | Pub/Sub | Kinesis |
| **Orquestación** | Cloud Composer (Airflow) | MWAA (Airflow) |
| **Filosofía** | Serverless-first | Más opciones, más complejidad |

**Analogía:** Si AWS es como un supermercado gigante con 1000 productos, GCP es como un restaurante gourmet con 50 platos perfectamente ejecutados.

---

## 2. Cloud Storage: El Data Lake de GCP

### ¿Qué es Cloud Storage?

**Cloud Storage** es el servicio de almacenamiento de objetos de GCP, equivalente a Amazon S3.

### Analogía: Cloud Storage como un almacén gigante

Imagina Cloud Storage como un **almacén de Amazon**:
- **Buckets**: Son como los almacenes físicos (uno en Madrid, otro en Barcelona)
- **Objetos**: Son las cajas que guardas (archivos CSV, JSON, Parquet)
- **Clases de almacenamiento**: Como diferentes secciones del almacén:
  - **Standard**: Caja en estantería de acceso rápido (0.01€/GB/mes más operaciones)
  - **Nearline**: Caja en sótano nivel 1 (0.004€/GB/mes, acces cada 30 días)
  - **Coldline**: Caja en sótano nivel 2 (0.002€/GB/mes, acceso cada 90 días)
  - **Archive**: Caja en almacén externo (0.0005€/GB/mes, acceso cada 365 días)

### Conceptos Clave

#### 1. Buckets (Cubos)

```python
# Crear un bucket
from google.cloud import storage

client = storage.Client()
bucket = client.create_bucket("cloudapi-data-lake-prod", location="europe-west1")

# Configurar clase de almacenamiento
bucket.storage_class = "STANDARD"
bucket.patch()
```

**Naming rules:**
- Globalmente único (como dominios web)
- Solo minúsculas, números, guiones
- Entre 3-63 caracteres

#### 2. Objetos (Objects)

```python
# Subir archivo
bucket = client.bucket("cloudapi-data-lake-prod")
blob = bucket.blob("data/raw/2025/01/15/logs.csv")
blob.upload_from_filename("local_logs.csv")

# Descargar archivo
blob.download_to_filename("downloaded_logs.csv")
```

#### 3. Lifecycle Policies

**Automatiza la gestión de datos:**

```json
{
  "rule": [
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 90}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 365}
    }
  ]
}
```

**Traducción:**
- Después de 30 días → Mover a Nearline (más barato)
- Después de 90 días → Mover a Coldline (aún más barato)
- Después de 365 días → Eliminar (liberar espacio)

### Casos de Uso Reales

**1. Data Lake para RestaurantData Co.**

```
gs://restaurantdata-datalake/
├── raw/                    # Datos sin procesar (Standard)
│   ├── 2025/01/15/
│   │   └── ventas.csv
│   └── 2025/01/16/
├── processed/              # Datos procesados (Standard)
│   └── 2025/01/15/
│       └── ventas.parquet
└── archive/                # Datos históricos (Archive)
    └── 2024/
```

**2. Optimización de costos**

Dato real: **10 TB de datos históricos**

| Estrategia | Costo mensual |
|------------|---------------|
| Todo en Standard | 10,000 GB × 0.01€ = **100€** |
| 1 TB Standard + 9 TB Archive | (1000×0.01) + (9000×0.0005) = **14.50€** |
| **Ahorro:** | **85.50€/mes = 1,026€/año** |

---

## 3. BigQuery: Data Warehouse Serverless

### ¿Qué es BigQuery?

**BigQuery** es el data warehouse completamente serverless de GCP. Es el servicio estrella para analytics.

### Analogía: BigQuery como una biblioteca mágica

Imagina una **biblioteca infinita**:
- **No necesitas estanterías**: No gestionas servidores (serverless)
- **Búsqueda instantánea**: Queries sobre petabytes en segundos
- **Pagas por leer**: Solo pagas por los datos escaneados, no por almacenamiento de infraestructura
- **Separación storage/compute**: Almacenamiento barato, compute solo cuando lo usas

### Conceptos Clave

#### 1. Datasets y Tablas

```sql
-- Crear dataset
CREATE SCHEMA IF NOT EXISTS `cloudapi_analytics`
OPTIONS(
  location="europe-west1",
  description="Analytics para CloudAPI Systems"
);

-- Crear tabla
CREATE TABLE `cloudapi_analytics.logs_api` (
  timestamp TIMESTAMP,
  endpoint STRING,
  method STRING,
  status_code INT64,
  response_time_ms FLOAT64,
  user_id STRING,
  ip_address STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY endpoint, status_code;
```

#### 2. Particionamiento (Partitioning)

**¿Por qué particionar?**

Reduce costos escaneando solo las particiones necesarias.

**Ejemplo sin particionamiento:**
```sql
-- Escanea 100 GB (todo el histórico)
SELECT * FROM logs_api
WHERE timestamp >= '2025-01-15'
  AND timestamp < '2025-01-16';

-- Costo: 100 GB × $5/TB = $0.50
```

**Ejemplo con particionamiento por fecha:**
```sql
-- Escanea solo 500 MB (una partición)
SELECT * FROM logs_api
WHERE timestamp >= '2025-01-15'
  AND timestamp < '2025-01-16';

-- Costo: 0.5 GB × $5/TB = $0.0025 (200x más barato!)
```

#### 3. Clustering

Organiza datos dentro de cada partición para queries aún más rápidas.

```sql
CREATE TABLE logs_api
PARTITION BY DATE(timestamp)
CLUSTER BY endpoint, status_code;  -- Agrupa por estos campos
```

**Beneficio:** Queries filtradas por `endpoint` escanean menos datos.

#### 4. Queries SQL

BigQuery usa **SQL estándar** con extensiones potentes:

```sql
-- Calcular percentiles de response time
SELECT
  endpoint,
  APPROX_QUANTILES(response_time_ms, 100)[OFFSET(50)] AS p50,
  APPROX_QUANTILES(response_time_ms, 100)[OFFSET(95)] AS p95,
  APPROX_QUANTILES(response_time_ms, 100)[OFFSET(99)] AS p99,
  COUNT(*) AS total_requests
FROM `cloudapi_analytics.logs_api`
WHERE DATE(timestamp) = '2025-01-15'
GROUP BY endpoint
ORDER BY p99 DESC;
```

### Costos de BigQuery

**2 tipos de costos:**

1. **Almacenamiento** (muy barato):
   - Active storage: $0.02/GB/mes
   - Long-term storage (>90 días sin modificar): $0.01/GB/mes

2. **Queries** (pagas por datos escaneados):
   - On-demand: $5 por TB escaneado
   - Flat-rate: $2,000/mes por 100 slots (para uso intensivo)

**Ejemplo real de CloudAPI Systems:**

```
Datos: 1 TB de logs
Queries diarias: 10 queries escaneando 10 GB cada una

Costo mensual:
- Storage: 1000 GB × $0.02 = $20
- Queries: (10 queries × 10 GB × 30 días) / 1000 GB × $5 = $15
- TOTAL: $35/mes

Con particionamiento (escanea solo 1 GB por query):
- Storage: $20
- Queries: (10 × 1 GB × 30) / 1000 × $5 = $1.50
- TOTAL: $21.50/mes (38% ahorro)
```

### Optimizaciones Clave

#### 1. Solo SELECT columnas necesarias

```sql
-- ❌ MAL: Escanea toda la tabla
SELECT * FROM logs_api;

-- ✅ BIEN: Escanea solo 3 columnas
SELECT endpoint, status_code, response_time_ms
FROM logs_api;
```

#### 2. Usa LIMIT con precaución

```sql
-- ❌ MAL: LIMIT no reduce datos escaneados
SELECT * FROM logs_api LIMIT 100;  -- Escanea toda la tabla

-- ✅ BIEN: Filtra primero
SELECT * FROM logs_api
WHERE DATE(timestamp) = CURRENT_DATE()
LIMIT 100;
```

#### 3. Materializa resultados frecuentes

```sql
-- Crear tabla materializada (se actualiza automáticamente)
CREATE MATERIALIZED VIEW daily_metrics AS
SELECT
  DATE(timestamp) AS dia,
  endpoint,
  COUNT(*) AS requests,
  AVG(response_time_ms) AS avg_response_time
FROM logs_api
GROUP BY dia, endpoint;
```

---

## 4. Dataflow: Procesamiento con Apache Beam

### ¿Qué es Dataflow?

**Dataflow** es el servicio managed de GCP para ejecutar pipelines de **Apache Beam**.

### Analogía: Dataflow como una fábrica automatizada

Imagina una **fábrica de Toyota** (procesamiento batch) que también puede funcionar **24/7** (streaming):
- **Apache Beam**: El plano de la fábrica (tu código Python)
- **Dataflow**: La fábrica física que ejecuta el plano (infraestructura)
- **Workers**: Los trabajadores (máquinas que GCP gestiona automáticamente)
- **Autoscaling**: Contratar/despedir trabajadores según la carga

### Conceptos Clave

#### 1. Pipeline Básico de Apache Beam

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# Definir opciones para Dataflow
options = PipelineOptions(
    project='mi-proyecto-gcp',
    job_name='procesar-logs-api',
    temp_location='gs://mi-bucket/temp',
    region='europe-west1',
    runner='DataflowRunner'  # Ejecutar en Dataflow (no local)
)

# Definir pipeline
with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | 'Leer de GCS' >> beam.io.ReadFromText('gs://logs-raw/*.csv')
        | 'Parsear CSV' >> beam.Map(parse_csv_line)
        | 'Filtrar válidos' >> beam.Filter(lambda x: x['status_code'] < 500)
        | 'Calcular métricas' >> beam.CombinePerKey(calcular_promedio)
        | 'Escribir a BigQuery' >> beam.io.WriteToBigQuery(
              table='cloudapi_analytics.metricas_diarias',
              schema='endpoint:STRING,avg_response_time:FLOAT'
          )
    )
```

#### 2. Transformaciones Comunes

**Map**: 1 input → 1 output
```python
| 'Convertir a mayúsculas' >> beam.Map(lambda x: x.upper())
```

**Filter**: Mantener solo elementos que cumplan condición
```python
| 'Solo éxitos' >> beam.Filter(lambda x: x['status_code'] == 200)
```

**GroupByKey**: Agrupar por clave
```python
| 'Agrupar por endpoint' >> beam.GroupByKey()
```

**CombinePerKey**: Agregar valores por clave
```python
| 'Promedio por endpoint' >> beam.CombinePerKey(beam.combiners.MeanCombineFn())
```

#### 3. Windowing para Streaming

Cuando procesas datos en tiempo real, necesitas **ventanas** para agregar:

```python
from apache_beam import window

(
    pipeline
    | 'Leer de Pub/Sub' >> beam.io.ReadFromPubSub(topic='projects/my-project/topics/logs')
    | 'Parsear JSON' >> beam.Map(json.loads)
    | 'Ventanas de 1 minuto' >> beam.WindowInto(window.FixedWindows(60))
    | 'Contar por endpoint' >> beam.combiners.Count.PerKey()
    | 'Escribir resultados' >> beam.io.WriteToBigQuery(...)
)
```

**Tipos de ventanas:**
- **Fixed**: Ventanas de tamaño fijo (ej: cada minuto)
- **Sliding**: Ventanas deslizantes con overlap
- **Session**: Ventanas basadas en actividad del usuario

### Batch vs Streaming

| Aspecto | Batch | Streaming |
|---------|-------|-----------|
| **Entrada** | Archivos en GCS | Pub/Sub topics |
| **Procesamiento** | Todo de una vez | Continuo (24/7) |
| **Latencia** | Minutos-horas | Segundos |
| **Costo** | Más barato | Más caro (workers siempre activos) |
| **Caso de uso** | Reportes diarios | Dashboards en tiempo real |

---

## 5. Pub/Sub: Mensajería para Streaming

### ¿Qué es Pub/Sub?

**Pub/Sub** (Publish/Subscribe) es el servicio de mensajería de GCP para comunicar sistemas en tiempo real.

### Analogía: Pub/Sub como un sistema de correo

Imagina el **sistema de correo postal**:
- **Publishers**: Personas que envían cartas (productores de datos)
- **Topics**: Buzones específicos (ej: "buzón de logs", "buzón de ventas")
- **Subscriptions**: Suscripciones para recibir copias (varios consumidores pueden suscribirse al mismo topic)
- **Subscribers**: Personas que reciben las cartas (consumidores de datos)

### Conceptos Clave

#### 1. Topics (Temas)

```python
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('mi-proyecto', 'logs-api')

# Crear topic
publisher.create_topic(request={"name": topic_path})
```

#### 2. Publicar Mensajes

```python
import json

# Publicar un log
log_data = {
    'timestamp': '2025-01-15T10:30:45Z',
    'endpoint': '/api/users',
    'status_code': 200,
    'response_time_ms': 145
}

# Convertir a bytes
data = json.dumps(log_data).encode('utf-8')

# Publicar
future = publisher.publish(topic_path, data)
message_id = future.result()  # Esperar confirmación

print(f"Mensaje publicado con ID: {message_id}")
```

#### 3. Subscriptions (Suscripciones)

```python
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('mi-proyecto', 'procesar-logs')

# Crear subscription
subscriber.create_subscription(
    request={
        "name": subscription_path,
        "topic": topic_path,
        "ack_deadline_seconds": 60  # Timeout para procesar
    }
)
```

#### 4. Consumir Mensajes

```python
def callback(message):
    """Función que procesa cada mensaje"""
    log = json.loads(message.data.decode('utf-8'))

    # Procesar log
    if log['status_code'] >= 500:
        print(f"ERROR: {log['endpoint']} retornó {log['status_code']}")

    # Confirmar procesamiento (ACK)
    message.ack()

# Suscribirse y escuchar mensajes
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result()  # Bloquea y escucha infinitamente
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

### At-Least-Once Delivery

**Pub/Sub garantiza** que cada mensaje se entrega **al menos una vez**:
- ✅ **Ventaja**: Nunca pierdes mensajes
- ⚠️ **Cuidado**: Puedes recibir duplicados

**Solución**: Hacer tu procesamiento **idempotente**:
```python
# ❌ MAL: Incrementar contador
contador += 1

# ✅ BIEN: Usar ID único para deduplicar
if mensaje_id not in procesados:
    contador += 1
    procesados.add(mensaje_id)
```

### Casos de Uso Reales

**1. Ingesta en tiempo real**
```
API REST → Pub/Sub Topic "logs-api" → Dataflow → BigQuery
```

**2. Arquitectura Event-Driven**
```
Usuario hace pedido → Pub/Sub "pedidos" → 3 subscriptions:
  - Subscription "inventario" → Actualizar stock
  - Subscription "facturacion" → Generar factura
  - Subscription "analytics" → Registrar métrica
```

**3. Backpressure**

Pub/Sub actúa como **buffer** cuando el consumidor es más lento que el productor:
```
API produce 1000 msg/s → Pub/Sub → Dataflow procesa 500 msg/s
                           ↑ Buffer (hasta 7 días de retención)
```

---

## 6. Cloud Composer: Orquestación Managed

### ¿Qué es Cloud Composer?

**Cloud Composer** es **Apache Airflow completamente managed** por GCP.

### Analogía: Cloud Composer como un director de orquesta

Imagina un **director de orquesta**:
- **DAG (Directed Acyclic Graph)**: La partitura musical
- **Tasks**: Cada instrumento (violín, piano, flauta)
- **Operators**: Los músicos que tocan cada instrumento
- **Scheduler**: El director que indica cuándo toca cada uno
- **Cloud Composer**: El teatro que proporciona todo (infraestructura)

### Conceptos Clave

#### 1. DAG Básico

```python
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['alerts@cloudapi.com'],
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pipeline_diario_logs',
    default_args=default_args,
    description='Procesa logs diarios de API',
    schedule_interval='0 2 * * *',  # 2 AM diario
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['logs', 'analytics'],
) as dag:

    # Task 1: Cargar CSV de GCS a BigQuery
    load_to_bq = GCSToBigQueryOperator(
        task_id='load_csv_to_bigquery',
        bucket='cloudapi-logs-raw',
        source_objects=['{{ ds }}/logs-*.csv'],  # Fecha de ejecución
        destination_project_dataset_table='cloudapi_analytics.logs_raw',
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,
    )

    # Task 2: Limpiar y transformar datos
    transform = BigQueryInsertJobOperator(
        task_id='transform_data',
        configuration={
            'query': {
                'query': '''
                    INSERT INTO cloudapi_analytics.logs_processed
                    SELECT
                      timestamp,
                      endpoint,
                      method,
                      status_code,
                      response_time_ms
                    FROM cloudapi_analytics.logs_raw
                    WHERE status_code IS NOT NULL
                      AND response_time_ms > 0
                ''',
                'useLegacySql': False,
            }
        },
    )

    # Task 3: Calcular métricas agregadas
    calculate_metrics = BigQueryInsertJobOperator(
        task_id='calculate_daily_metrics',
        configuration={
            'query': {
                'query': '''
                    INSERT INTO cloudapi_analytics.metricas_diarias
                    SELECT
                      DATE(timestamp) as dia,
                      endpoint,
                      COUNT(*) as total_requests,
                      AVG(response_time_ms) as avg_response_time,
                      APPROX_QUANTILES(response_time_ms, 100)[OFFSET(95)] as p95
                    FROM cloudapi_analytics.logs_processed
                    WHERE DATE(timestamp) = '{{ ds }}'
                    GROUP BY dia, endpoint
                ''',
                'useLegacySql': False,
            }
        },
    )

    # Definir dependencias
    load_to_bq >> transform >> calculate_metrics
```

#### 2. Operators Comunes

**GCP Operators:**
- `BigQueryInsertJobOperator`: Ejecutar queries SQL
- `GCSToBigQueryOperator`: Cargar CSV/JSON a BigQuery
- `DataflowTemplatedJobStartOperator`: Ejecutar job de Dataflow
- `PubSubPublishMessageOperator`: Publicar mensajes a Pub/Sub

**Sensores:**
- `GCSObjectExistenceSensor`: Esperar a que exista un archivo
- `BigQueryTableExistenceSensor`: Esperar a que exista una tabla

#### 3. XComs para pasar datos entre tasks

```python
# Task 1: Calcular y retornar resultado
def calcular_total(**context):
    total = 12345
    context['ti'].xcom_push(key='total_registros', value=total)

# Task 2: Leer resultado de Task 1
def enviar_notificacion(**context):
    total = context['ti'].xcom_pull(key='total_registros', task_ids='calcular_total')
    print(f"Se procesaron {total} registros")
```

### Mejores Prácticas

#### 1. Idempotencia

Tu DAG debe poder ejecutarse múltiples veces sin efectos secundarios:

```sql
-- ❌ MAL: Duplica datos en cada ejecución
INSERT INTO tabla
SELECT * FROM otra_tabla;

-- ✅ BIEN: Reemplaza datos de la fecha específica
DELETE FROM tabla WHERE DATE(timestamp) = '{{ ds }}';
INSERT INTO tabla
SELECT * FROM otra_tabla WHERE DATE(timestamp) = '{{ ds }}';

-- ✅ MEJOR: Usa MERGE para upsert
MERGE tabla AS target
USING otra_tabla AS source
ON target.id = source.id AND DATE(target.timestamp) = '{{ ds }}'
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

#### 2. Parametrización con Jinja

```python
query = '''
    SELECT * FROM logs
    WHERE DATE(timestamp) = '{{ ds }}'           -- Fecha de ejecución
      AND timestamp >= '{{ ds }} 00:00:00'
      AND timestamp < '{{ next_ds }} 00:00:00'   -- Siguiente día
'''
```

#### 3. Alertas

```python
def alert_on_failure(context):
    """Envía alerta cuando un task falla"""
    task_instance = context.get('task_instance')
    dag_id = context.get('dag_id')

    # Enviar a Slack, email, PagerDuty, etc.
    send_slack_message(
        f"❌ Task {task_instance.task_id} falló en DAG {dag_id}"
    )

default_args = {
    'on_failure_callback': alert_on_failure,
}
```

---

## 📊 Comparación de Servicios GCP

| Servicio | Equivalente AWS | Cuándo Usarlo | Costo Relativo |
|----------|-----------------|---------------|----------------|
| **Cloud Storage** | S3 | Data lake, almacenamiento de objetos | $ |
| **BigQuery** | Redshift/Athena | Data warehouse, analytics SQL | $$ |
| **Dataflow** | Glue + EMR | Procesamiento batch/streaming escalable | $$$ |
| **Pub/Sub** | Kinesis/SQS | Ingesta en tiempo real, event-driven | $ |
| **Cloud Composer** | MWAA | Orquestar workflows complejos | $$$ |

---

## 💰 Estimación de Costos - Proyecto Real

**CloudAPI Systems - Pipeline completo GCP:**

### Arquitectura
```
API REST (1000 req/s) → Pub/Sub → Dataflow → BigQuery
                                     ↓
                               Cloud Storage (backup)
                                     ↓
                           Cloud Composer (orquestación)
```

### Costos Mensuales (estimado)

| Servicio | Uso | Costo |
|----------|-----|-------|
| **Cloud Storage** | 500 GB | 500 × $0.02 = **$10** |
| **Pub/Sub** | 1M msg/día × 30 = 30M msg | 30M × $40/millón = **$12** |
| **Dataflow** | 10 workers × 24h × 30d | 7,200 vCPU-hours × $0.056 = **$403** |
| **BigQuery Storage** | 1 TB | 1000 × $0.02 = **$20** |
| **BigQuery Queries** | 100 GB/día escaneado | 3 TB/mes × $5/TB = **$15** |
| **Cloud Composer** | 1 environment (small) | **$300** |
| **TOTAL** |  | **$760/mes** |

**Con optimizaciones:**
- Usar Dataflow solo batch (no 24/7): $403 → $50
- Particionar BigQuery: $15 → $3
- **TOTAL optimizado: $410/mes**

---

## ✅ Checklist de Aprendizaje

Verifica que puedes hacer lo siguiente:

- [ ] Crear buckets en Cloud Storage y subir archivos
- [ ] Configurar lifecycle policies para optimizar costos
- [ ] Crear datasets y tablas en BigQuery con particionamiento
- [ ] Escribir queries SQL optimizadas para BigQuery
- [ ] Diseñar un pipeline de Apache Beam para batch
- [ ] Implementar procesamiento streaming con ventanas
- [ ] Crear topics y subscriptions en Pub/Sub
- [ ] Publicar y consumir mensajes en tiempo real
- [ ] Escribir un DAG de Airflow con operators de GCP
- [ ] Calcular costos estimados de un pipeline GCP
- [ ] Aplicar mejores prácticas de seguridad (IAM, encryption)

---

## 🎓 Próximos Pasos

Has completado la teoría de GCP. Ahora:

1. **Practica con ejemplos** → `02-EJEMPLOS.md`
2. **Resuelve ejercicios** → `03-EJERCICIOS.md`
3. **Implementa el proyecto** → `04-proyecto-practico/`

**En el proyecto práctico construirás:**
- Pipeline completo de ingesta → procesamiento → analytics
- Integración de todos los servicios GCP
- Monitoreo y alertas
- Optimización de costos

---

**¡Éxito con GCP!** 🚀

*Última actualización: 2025-11-09*
*Módulo 7 - Tema 2: GCP para Data Engineering*
