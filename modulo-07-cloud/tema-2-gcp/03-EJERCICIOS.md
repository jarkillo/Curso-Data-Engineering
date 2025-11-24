# 🎯 Ejercicios Prácticos: GCP para Data Engineering

## Introducción

Esta sección contiene **15 ejercicios prácticos** para que practiques los conceptos de GCP aprendidos en la teoría y ejemplos. Los ejercicios aumentan progresivamente en dificultad:

- ⭐ **Ejercicios 1-5**: Básicos (Cloud Storage, BigQuery simple)
- ⭐⭐ **Ejercicios 6-10**: Intermedios (Dataflow, Pub/Sub)
- ⭐⭐⭐ **Ejercicios 11-15**: Avanzados (Cloud Composer, integración end-to-end)

Cada ejercicio incluye:
- Enunciado claro
- Datos de entrada (si aplica)
- Pistas para ayudarte
- **Solución completa al final**

---

## Tabla de Contenidos

1. [Ejercicios Básicos (1-5)](#ejercicios-básicos)
2. [Ejercicios Intermedios (6-10)](#ejercicios-intermedios)
3. [Ejercicios Avanzados (11-15)](#ejercicios-avanzados)
4. [Soluciones](#soluciones)

---

## Ejercicios Básicos

### ⭐ Ejercicio 1: Subir y Descargar Archivos a Cloud Storage

**Contexto**: Eres el Data Engineer de **HealthTech Inc.** (startup de salud digital). Necesitas implementar funciones para subir archivos CSV de pacientes a Cloud Storage y descargarlos cuando sea necesario.

**Requisitos**:
1. Implementar función `subir_csv_a_gcs(bucket_name: str, archivo_local: str, ruta_destino: str) -> str` que retorne la URI del archivo subido
2. Implementar función `descargar_csv_desde_gcs(uri: str, archivo_local: str) -> None` que descargue el archivo
3. La función de subida debe configurar metadata: `tipo: "pacientes"`, `fecha_subida: <timestamp>`

**Datos de prueba**:
```csv
# pacientes.csv
paciente_id,nombre,edad,diagnostico
P001,Juan Pérez,45,Diabetes
P002,María García,32,Hipertensión
P003,Carlos López,58,Colesterol Alto
```

**Pistas**:
- Usa `google.cloud.storage.Client`
- URI de GCS tiene formato: `gs://bucket/path/file.csv`
- Para metadata usa `blob.metadata = {...}` y luego `blob.patch()`

---

### ⭐ Ejercicio 2: Lifecycle Policy para Optimizar Costos

**Contexto**: **HealthTech Inc.** almacena reportes diarios de pacientes en Cloud Storage. Los reportes son:
- Muy accedidos los primeros 7 días
- Ocasionalmente accedidos entre 7-30 días
- Raramente accedidos después de 30 días
- Deben conservarse 2 años por ley

**Requisitos**:
Crear una función `crear_bucket_con_lifecycle_healthcare(project_id: str, bucket_name: str) -> storage.Bucket` que configure el bucket con lifecycle policies óptimas para este caso.

**Pistas**:
- STANDARD para 0-7 días
- NEARLINE para 7-30 días
- COLDLINE para 30+ días
- ARCHIVE para >1 año
- Eliminar después de 2 años (730 días)

---

### ⭐ Ejercicio 3: Crear Tabla en BigQuery con Schema

**Contexto**: Necesitas crear una tabla `pacientes` en BigQuery para almacenar los datos de los pacientes de HealthTech Inc.

**Requisitos**:
Implementar `crear_tabla_pacientes(project_id: str, dataset_id: str, tabla_id: str) -> bigquery.Table` con el siguiente schema:
- `paciente_id` (STRING, REQUIRED)
- `nombre` (STRING, REQUIRED)
- `edad` (INTEGER, REQUIRED)
- `diagnostico` (STRING, NULLABLE)
- `fecha_registro` (DATE, REQUIRED) ← Para particionamiento
- `ultima_visita` (TIMESTAMP, NULLABLE)

**Pistas**:
- Usa `bigquery.SchemaField` para cada campo
- Configura particionamiento por `fecha_registro`
- Usa `bigquery.TimePartitioning`

---

### ⭐ Ejercicio 4: Query SQL Básica en BigQuery

**Contexto**: Ya tienes datos en BigQuery y necesitas analizar la distribución de diagnósticos.

**Datos en tabla** (ya cargados):
```
paciente_id | nombre | edad | diagnostico | fecha_registro
P001 | Juan Pérez | 45 | Diabetes | 2025-01-15
P002 | María García | 32 | Hipertensión | 2025-01-15
P003 | Carlos López | 58 | Colesterol Alto | 2025-01-15
P004 | Ana Martínez | 41 | Diabetes | 2025-01-16
P005 | Pedro Sánchez | 50 | Hipertensión | 2025-01-16
```

**Requisitos**:
Escribir función `obtener_distribucion_diagnosticos(project_id: str, dataset_id: str, tabla_id: str) -> list[dict]` que retorne:
```python
[
    {"diagnostico": "Diabetes", "total_pacientes": 2, "porcentaje": 40.0},
    {"diagnostico": "Hipertensión", "total_pacientes": 2, "porcentaje": 40.0},
    {"diagnostico": "Colesterol Alto", "total_pacientes": 1, "porcentaje": 20.0}
]
```

**Pistas**:
- Usa `GROUP BY diagnostico`
- Calcula porcentaje con: `COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()`
- Ordena por `total_pacientes DESC`

---

### ⭐ Ejercicio 5: Cargar CSV desde GCS a BigQuery

**Contexto**: Tienes archivos CSV en Cloud Storage y necesitas cargarlos en BigQuery automáticamente.

**Requisitos**:
Implementar `cargar_csv_gcs_a_bigquery(project_id: str, dataset_id: str, tabla_id: str, uri_gcs: str) -> int` que:
1. Cargue el CSV desde GCS a BigQuery
2. Configure el job para saltar la primera fila (header)
3. Use `WRITE_APPEND` (agregar datos)
4. Retorne el número de filas cargadas

**Pistas**:
- Usa `bigquery.LoadJobConfig`
- `source_format=bigquery.SourceFormat.CSV`
- `skip_leading_rows=1`
- `load_job.output_rows` para contar filas

---

## Ejercicios Intermedios

### ⭐⭐ Ejercicio 6: Pipeline Dataflow para Limpiar Datos

**Contexto**: Los archivos CSV de pacientes vienen con datos sucios (nulls, formatos incorrectos). Necesitas un pipeline Dataflow para limpiarlos.

**Datos de entrada** (CSV sucio):
```csv
paciente_id,nombre,edad,diagnostico
P001,Juan Pérez,45,Diabetes
P002,,32,  # Nombre vacío (inválido)
P003,Carlos López,invalid,Colesterol Alto  # Edad inválida
P004,Ana Martínez,41,
P005,Pedro Sánchez,50,Hipertensión
```

**Requisitos**:
Implementar pipeline Dataflow con:
1. `ValidarPaciente(beam.DoFn)` que descarte registros con:
   - `paciente_id` vacío
   - `nombre` vacío
   - `edad` no numérica o <0
2. `EnriquecerPaciente(beam.DoFn)` que agregue:
   - `fecha_procesamiento` (timestamp actual)
   - `es_mayor_50` (boolean, True si edad >= 50)

**Salida esperada**:
```python
[
    {"paciente_id": "P001", "nombre": "Juan Pérez", "edad": 45, "diagnostico": "Diabetes", "fecha_procesamiento": "2025-01-15T10:30:00Z", "es_mayor_50": False},
    {"paciente_id": "P005", "nombre": "Pedro Sánchez", "edad": 50, "diagnostico": "Hipertensión", "fecha_procesamiento": "2025-01-15T10:30:00Z", "es_mayor_50": True}
]
```

**Pistas**:
- Usa `beam.ParDo(ValidarPaciente())`
- Para validar edad: `int(paciente["edad"])` en try/except
- Para enriquecer: `datetime.utcnow().isoformat() + "Z"`

---

### ⭐⭐ Ejercicio 7: Aggregaciones en Dataflow

**Contexto**: Necesitas calcular estadísticas agregadas de pacientes por diagnóstico usando Dataflow.

**Datos de entrada**:
```python
pacientes = [
    {"diagnostico": "Diabetes", "edad": 45},
    {"diagnostico": "Diabetes", "edad": 50},
    {"diagnostico": "Hipertensión", "edad": 32},
    {"diagnostico": "Hipertensión", "edad": 60},
    {"diagnostico": "Hipertensión", "edad": 55},
]
```

**Requisitos**:
Implementar pipeline con:
1. Agrupar por `diagnostico`
2. Calcular para cada grupo:
   - `total_pacientes`: Count
   - `edad_promedio`: Promedio de edades
   - `edad_min`: Edad mínima
   - `edad_max`: Edad máxima

**Salida esperada**:
```python
[
    {"diagnostico": "Diabetes", "total_pacientes": 2, "edad_promedio": 47.5, "edad_min": 45, "edad_max": 50},
    {"diagnostico": "Hipertensión", "total_pacientes": 3, "edad_promedio": 49.0, "edad_min": 32, "edad_max": 60}
]
```

**Pistas**:
- Usa `beam.Map(lambda p: (p["diagnostico"], p))`
- Usa `beam.GroupByKey()`
- Implementa `CalcularEstadisticas(beam.DoFn)` para procesar grupos

---

### ⭐⭐ Ejercicio 8: Pub/Sub - Publicar Eventos de Pacientes

**Contexto**: Cada vez que un paciente es registrado en el sistema, necesitas publicar un evento a Pub/Sub para notificar a otros servicios.

**Requisitos**:
Implementar:
1. `publicar_evento_paciente(project_id: str, topic_id: str, paciente: dict) -> str` que publique un evento con formato:
   ```json
   {
     "tipo_evento": "paciente_registrado",
     "paciente_id": "P001",
     "timestamp": "2025-01-15T10:30:45Z",
     "datos": {"nombre": "Juan Pérez", "edad": 45}
   }
   ```
2. Retornar el `message_id`

**Datos de prueba**:
```python
paciente = {"paciente_id": "P001", "nombre": "Juan Pérez", "edad": 45, "diagnostico": "Diabetes"}
```

**Pistas**:
- Usa `pubsub_v1.PublisherClient()`
- Serializa a JSON con `json.dumps(evento)`
- Publica con `publisher.publish(topic_path, mensaje_bytes)`

---

### ⭐⭐ Ejercicio 9: Pub/Sub - Consumir Eventos en Batch

**Contexto**: Necesitas consumir eventos de Pub/Sub y procesarlos en batches de 10 mensajes.

**Requisitos**:
Implementar `consumir_eventos_batch(project_id: str, subscription_id: str, callback: Callable, max_mensajes: int = 10) -> int` que:
1. Consuma hasta `max_mensajes` mensajes
2. Ejecute `callback(mensaje)` para cada uno
3. Haga ACK de mensajes procesados correctamente
4. Retorne el número de mensajes procesados

**Pistas**:
- Usa `subscriber.pull()` en lugar de `subscribe()` (para control manual)
- `subscriber.acknowledge()` para hacer ACK
- Iterar sobre `response.received_messages`

---

### ⭐⭐ Ejercicio 10: Query Analítica en BigQuery con Window Functions

**Contexto**: Necesitas analizar la evolución temporal de pacientes registrados por día.

**Datos en tabla**:
```
fecha_registro | diagnostico | total_pacientes
2025-01-10 | Diabetes | 5
2025-01-11 | Diabetes | 8
2025-01-12 | Diabetes | 6
2025-01-10 | Hipertensión | 3
2025-01-11 | Hipertensión | 4
2025-01-12 | Hipertensión | 7
```

**Requisitos**:
Escribir query SQL que calcule:
1. Para cada `(fecha, diagnostico)`:
   - `total_pacientes`
   - `total_acumulado` (suma acumulada por diagnóstico)
   - `cambio_vs_dia_anterior` (diferencia con día previo)

**Salida esperada**:
```
fecha_registro | diagnostico | total_pacientes | total_acumulado | cambio_vs_dia_anterior
2025-01-10 | Diabetes | 5 | 5 | NULL
2025-01-11 | Diabetes | 8 | 13 | +3
2025-01-12 | Diabetes | 6 | 19 | -2
```

**Pistas**:
- Usa `SUM(total_pacientes) OVER (PARTITION BY diagnostico ORDER BY fecha_registro)`
- Usa `LAG(total_pacientes) OVER (PARTITION BY diagnostico ORDER BY fecha_registro)`

---

## Ejercicios Avanzados

### ⭐⭐⭐ Ejercicio 11: Pipeline Dataflow Streaming con Pub/Sub

**Contexto**: Necesitas procesar eventos de pacientes en tiempo real usando Dataflow Streaming.

**Requisitos**:
Implementar pipeline Dataflow Streaming que:
1. Lea de Pub/Sub (`subscription_id`)
2. Parsee JSON
3. Valide datos (edad > 0, nombre no vacío)
4. Enriquezca con timestamp de procesamiento
5. Escriba a BigQuery en tabla `pacientes_streaming`

**Arquitectura**:
```
Pub/Sub → Dataflow Streaming → BigQuery (tabla particionada por fecha)
```

**Pistas**:
- Usa `beam.io.ReadFromPubSub(subscription=...)`
- Configura `streaming=True` en `PipelineOptions`
- Usa `beam.io.WriteToBigQuery()` con `write_disposition=WRITE_APPEND`

---

### ⭐⭐⭐ Ejercicio 12: Dataflow con Windowing (Agregaciones por Tiempo)

**Contexto**: Necesitas calcular métricas de eventos de pacientes cada 5 minutos (ventanas deslizantes).

**Requisitos**:
Implementar pipeline Dataflow Streaming que:
1. Lea eventos de Pub/Sub
2. Aplique ventanas de 5 minutos (`beam.WindowInto(beam.window.FixedWindows(300))`)
3. Calcule por ventana:
   - Total de eventos
   - Distribución por diagnóstico
4. Escriba resultados a BigQuery

**Salida esperada** (cada 5 min):
```
window_start | window_end | diagnostico | total_eventos
2025-01-15 10:00:00 | 2025-01-15 10:05:00 | Diabetes | 12
2025-01-15 10:00:00 | 2025-01-15 10:05:00 | Hipertensión | 8
2025-01-15 10:05:00 | 2025-01-15 10:10:00 | Diabetes | 15
```

**Pistas**:
- Usa `beam.WindowInto(beam.window.FixedWindows(5 * 60))`
- Accede a window con `beam.DoFn` y `window=beam.DoFn.WindowParam`
- Convierte window a timestamp: `window.start.to_utc_datetime()`

---

### ⭐⭐⭐ Ejercicio 13: Cloud Composer DAG para Pipeline Diario

**Contexto**: Necesitas crear un DAG de Airflow que ejecute un pipeline completo de procesamiento diario.

**Requisitos**:
Crear DAG `healthtech_daily_pipeline` que:
1. Verifique que existan archivos CSV en GCS (path: `gs://healthtech-data/raw/YYYY-MM-DD/*.csv`)
2. Si existen, ejecute job Dataflow para procesar
3. Calcule métricas KPI en BigQuery:
   - Total de nuevos pacientes
   - Distribución por diagnóstico
   - Edad promedio por diagnóstico
4. Guarde métricas en tabla `kpis_diarios`
5. Envíe email con resumen si hay >100 nuevos pacientes

**Schedule**: Todos los días a las 6:00 AM

**Pistas**:
- Usa `PythonOperator` para verificar archivos
- Usa `DataflowTemplatedJobStartOperator` para Dataflow
- Usa `BigQueryInsertJobOperator` para KPIs
- Usa `EmailOperator` con condición

---

### ⭐⭐⭐ Ejercicio 14: Sistema de Alertas en Tiempo Real

**Contexto**: Necesitas un sistema que detecte pacientes de alto riesgo en tiempo real y envíe alertas.

**Definición de alto riesgo**:
- Edad > 60 Y (Diabetes O Hipertensión)

**Requisitos**:
Implementar:
1. Pipeline Dataflow Streaming que:
   - Lea eventos de Pub/Sub (`pacientes-eventos`)
   - Filtre pacientes de alto riesgo
   - Publique alertas a otro topic Pub/Sub (`pacientes-alertas-alto-riesgo`)
2. Consumer que lea alertas y envíe email (simulado con print)

**Datos de prueba**:
```python
eventos = [
    {"paciente_id": "P001", "nombre": "Juan Pérez", "edad": 65, "diagnostico": "Diabetes"},  # ALERTA
    {"paciente_id": "P002", "nombre": "María García", "edad": 32, "diagnostico": "Hipertensión"},  # No alerta (edad)
    {"paciente_id": "P003", "nombre": "Carlos López", "edad": 62, "diagnostico": "Colesterol Alto"}  # No alerta (diagnóstico)
]
```

**Salida esperada** (alertas):
```
🚨 ALERTA: Paciente de alto riesgo
   ID: P001
   Nombre: Juan Pérez
   Edad: 65
   Diagnóstico: Diabetes
```

**Pistas**:
- Usa `beam.Filter(lambda p: es_alto_riesgo(p))`
- Publica a segundo topic con `beam.io.WriteToPubSub()`
- Consumer usa `subscriber.subscribe()`

---

### ⭐⭐⭐ Ejercicio 15: Pipeline End-to-End con Monitoreo

**Contexto**: Crear un pipeline completo de producción con monitoreo y manejo de errores.

**Requisitos**:
Implementar sistema completo:

1. **Ingesta** (Pub/Sub):
   - Recibir eventos de pacientes

2. **Procesamiento** (Dataflow Streaming):
   - Validar datos
   - Enriquecer con información adicional (timestamp, categoría de riesgo)
   - Filtrar registros inválidos

3. **Almacenamiento** (BigQuery):
   - Guardar en tabla particionada
   - Separar registros válidos e inválidos en tablas distintas

4. **Alertas** (Pub/Sub + Cloud Functions):
   - Detectar pacientes de alto riesgo
   - Publicar alertas

5. **Monitoreo** (Cloud Logging):
   - Loggear métricas cada 1 minuto:
     - Total de eventos procesados
     - Total de eventos inválidos
     - Total de alertas generadas
     - Latencia promedio (tiempo desde ingesta hasta BQ)

6. **Orquestación** (Cloud Composer):
   - DAG que ejecute job Dataflow
   - Monitoree estado del job
   - Envíe notificación si falla

**Arquitectura**:
```
Eventos → Pub/Sub → Dataflow Streaming → BigQuery
                          ↓                  ↓
                    (Alertas)           (Métricas)
                          ↓                  ↓
                    Pub/Sub            Cloud Logging
                          ↓
                  Cloud Function
                          ↓
                    Email/Slack
```

**Métricas esperadas** (cada minuto):
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "eventos_procesados": 1250,
  "eventos_invalidos": 45,
  "alertas_generadas": 12,
  "latencia_promedio_ms": 320
}
```

**Pistas**:
- Usa `beam.metrics.Metrics.counter()` para contadores
- Usa `beam.metrics.Metrics.distribution()` para latencia
- Usa `logging.info()` para loggear en Cloud Logging
- Cloud Function usa trigger Pub/Sub

---

## Soluciones

### Solución Ejercicio 1

```python
from google.cloud import storage
from datetime import datetime
from pathlib import Path


def subir_csv_a_gcs(bucket_name: str, archivo_local: str, ruta_destino: str) -> str:
    """
    Sube un archivo CSV a Cloud Storage.

    Args:
        bucket_name: Nombre del bucket
        archivo_local: Ruta al archivo local
        ruta_destino: Ruta destino en GCS (sin gs://)

    Returns:
        URI del archivo subido (gs://...)
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(ruta_destino)

    # Subir archivo
    blob.upload_from_filename(archivo_local)

    # Configurar metadata
    blob.metadata = {
        "tipo": "pacientes",
        "fecha_subida": datetime.utcnow().isoformat() + "Z"
    }
    blob.patch()

    uri = f"gs://{bucket_name}/{ruta_destino}"
    print(f"✅ Archivo subido: {uri}")

    return uri


def descargar_csv_desde_gcs(uri: str, archivo_local: str) -> None:
    """
    Descarga un archivo desde Cloud Storage.

    Args:
        uri: URI del archivo (gs://bucket/path)
        archivo_local: Ruta local destino
    """
    # Parsear URI
    uri_parts = uri.replace("gs://", "").split("/", 1)
    bucket_name = uri_parts[0]
    blob_path = uri_parts[1]

    # Descargar
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.download_to_filename(archivo_local)

    print(f"✅ Archivo descargado: {archivo_local}")


# Uso
if __name__ == "__main__":
    # Subir
    uri = subir_csv_a_gcs(
        bucket_name="healthtech-data",
        archivo_local="pacientes.csv",
        ruta_destino="raw/pacientes/pacientes_2025-01-15.csv"
    )

    # Descargar
    descargar_csv_desde_gcs(
        uri=uri,
        archivo_local="/tmp/pacientes_descargado.csv"
    )
```

---

### Solución Ejercicio 2

```python
from google.cloud import storage


def crear_bucket_con_lifecycle_healthcare(
    project_id: str,
    bucket_name: str
) -> storage.Bucket:
    """
    Crea bucket con lifecycle policies optimizadas para healthcare.
    """
    client = storage.Client(project=project_id)

    bucket = client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    bucket.location = "us-central1"

    # Rule 1: STANDARD → NEARLINE después de 7 días
    rule_nearline = storage.bucket.LifecycleRule(
        action={"type": "SetStorageClass", "storageClass": "NEARLINE"},
        condition={"age": 7}
    )

    # Rule 2: NEARLINE → COLDLINE después de 30 días
    rule_coldline = storage.bucket.LifecycleRule(
        action={"type": "SetStorageClass", "storageClass": "COLDLINE"},
        condition={"age": 30}
    )

    # Rule 3: COLDLINE → ARCHIVE después de 365 días
    rule_archive = storage.bucket.LifecycleRule(
        action={"type": "SetStorageClass", "storageClass": "ARCHIVE"},
        condition={"age": 365}
    )

    # Rule 4: Eliminar después de 730 días (2 años)
    rule_delete = storage.bucket.LifecycleRule(
        action={"type": "Delete"},
        condition={"age": 730}
    )

    bucket.lifecycle_rules = [rule_nearline, rule_coldline, rule_archive, rule_delete]

    bucket.create()

    print(f"✅ Bucket '{bucket_name}' creado con lifecycle policies healthcare")
    return bucket


# Uso
bucket = crear_bucket_con_lifecycle_healthcare(
    project_id="healthtech-prod",
    bucket_name="healthtech-reportes"
)
```

**Ahorro de costos**:
- Sin lifecycle: 100 GB × $0.020/GB × 12 = **$24/año**
- Con lifecycle: ~**$8/año** (ahorro de 67%)

---

### Solución Ejercicio 3

```python
from google.cloud import bigquery


def crear_tabla_pacientes(
    project_id: str,
    dataset_id: str,
    tabla_id: str
) -> bigquery.Table:
    """
    Crea tabla de pacientes en BigQuery.
    """
    client = bigquery.Client(project=project_id)

    # Definir schema
    schema = [
        bigquery.SchemaField("paciente_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nombre", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("edad", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("diagnostico", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("fecha_registro", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("ultima_visita", "TIMESTAMP", mode="NULLABLE"),
    ]

    # Crear tabla
    table_ref = f"{project_id}.{dataset_id}.{tabla_id}"
    tabla = bigquery.Table(table_ref, schema=schema)

    # Configurar particionamiento por fecha_registro
    tabla.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="fecha_registro"
    )

    # Configurar clustering (opcional, mejora queries)
    tabla.clustering_fields = ["diagnostico"]

    tabla = client.create_table(tabla, exists_ok=True)

    print(f"✅ Tabla '{tabla_id}' creada con particionamiento")
    return tabla


# Uso
tabla = crear_tabla_pacientes(
    project_id="healthtech-prod",
    dataset_id="analytics",
    tabla_id="pacientes"
)
```

---

### Solución Ejercicio 4

```python
from google.cloud import bigquery


def obtener_distribucion_diagnosticos(
    project_id: str,
    dataset_id: str,
    tabla_id: str
) -> list[dict]:
    """
    Obtiene distribución de diagnósticos.
    """
    client = bigquery.Client(project=project_id)

    query = f"""
    SELECT
        diagnostico,
        COUNT(*) as total_pacientes,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
    FROM `{project_id}.{dataset_id}.{tabla_id}`
    GROUP BY diagnostico
    ORDER BY total_pacientes DESC
    """

    query_job = client.query(query)

    resultados = []
    for row in query_job:
        resultados.append({
            "diagnostico": row.diagnostico,
            "total_pacientes": row.total_pacientes,
            "porcentaje": float(row.porcentaje)
        })

    return resultados


# Uso
distribucion = obtener_distribucion_diagnosticos(
    project_id="healthtech-prod",
    dataset_id="analytics",
    tabla_id="pacientes"
)

for item in distribucion:
    print(f"{item['diagnostico']}: {item['total_pacientes']} pacientes ({item['porcentaje']}%)")
```

**Salida**:
```
Diabetes: 2 pacientes (40.0%)
Hipertensión: 2 pacientes (40.0%)
Colesterol Alto: 1 pacientes (20.0%)
```

---

### Solución Ejercicio 5

```python
from google.cloud import bigquery


def cargar_csv_gcs_a_bigquery(
    project_id: str,
    dataset_id: str,
    tabla_id: str,
    uri_gcs: str
) -> int:
    """
    Carga CSV desde GCS a BigQuery.
    """
    client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset_id}.{tabla_id}"

    # Configurar job de carga
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Saltar header
        autodetect=False,  # Usar schema existente
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    # Iniciar carga
    load_job = client.load_table_from_uri(
        uri_gcs,
        table_ref,
        job_config=job_config
    )

    # Esperar a que termine
    load_job.result()

    filas_cargadas = load_job.output_rows

    print(f"✅ Cargadas {filas_cargadas} filas desde {uri_gcs}")

    return filas_cargadas


# Uso
filas = cargar_csv_gcs_a_bigquery(
    project_id="healthtech-prod",
    dataset_id="analytics",
    tabla_id="pacientes",
    uri_gcs="gs://healthtech-data/raw/pacientes/pacientes_2025-01-15.csv"
)
```

---

### Solución Ejercicio 6

```python
import apache_beam as beam
from datetime import datetime


class ValidarPaciente(beam.DoFn):
    """Valida registros de pacientes."""

    def process(self, paciente: dict):
        # Validar paciente_id
        if not paciente.get("paciente_id"):
            return  # Descartar

        # Validar nombre
        if not paciente.get("nombre") or not paciente.get("nombre").strip():
            return  # Descartar

        # Validar edad
        try:
            edad = int(paciente.get("edad", -1))
            if edad < 0:
                return  # Descartar
            paciente["edad"] = edad
        except (ValueError, TypeError):
            return  # Descartar

        yield paciente


class EnriquecerPaciente(beam.DoFn):
    """Enriquece registros con campos calculados."""

    def process(self, paciente: dict):
        # Agregar timestamp de procesamiento
        paciente["fecha_procesamiento"] = datetime.utcnow().isoformat() + "Z"

        # Agregar flag de mayor de 50
        paciente["es_mayor_50"] = paciente["edad"] >= 50

        yield paciente


def run_pipeline():
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | "Leer CSV" >> beam.io.ReadFromText("pacientes_sucio.csv", skip_header_lines=1)
            | "Parsear CSV" >> beam.Map(lambda line: dict(zip(
                ["paciente_id", "nombre", "edad", "diagnostico"],
                line.split(",")
            )))
            | "Validar" >> beam.ParDo(ValidarPaciente())
            | "Enriquecer" >> beam.ParDo(EnriquecerPaciente())
            | "Imprimir" >> beam.Map(print)
        )


# Ejecutar
run_pipeline()
```

**Salida**:
```
{'paciente_id': 'P001', 'nombre': 'Juan Pérez', 'edad': 45, 'diagnostico': 'Diabetes', 'fecha_procesamiento': '2025-01-15T10:30:00Z', 'es_mayor_50': False}
{'paciente_id': 'P005', 'nombre': 'Pedro Sánchez', 'edad': 50, 'diagnostico': 'Hipertensión', 'fecha_procesamiento': '2025-01-15T10:30:00Z', 'es_mayor_50': True}
```

---

### Solución Ejercicio 7

```python
import apache_beam as beam
import statistics


class CalcularEstadisticas(beam.DoFn):
    """Calcula estadísticas por diagnóstico."""

    def process(self, element):
        diagnostico, pacientes = element

        edades = [p["edad"] for p in pacientes]

        yield {
            "diagnostico": diagnostico,
            "total_pacientes": len(pacientes),
            "edad_promedio": round(statistics.mean(edades), 2),
            "edad_min": min(edades),
            "edad_max": max(edades)
        }


def run_pipeline():
    pacientes = [
        {"diagnostico": "Diabetes", "edad": 45},
        {"diagnostico": "Diabetes", "edad": 50},
        {"diagnostico": "Hipertensión", "edad": 32},
        {"diagnostico": "Hipertensión", "edad": 60},
        {"diagnostico": "Hipertensión", "edad": 55},
    ]

    with beam.Pipeline() as pipeline:
        (
            pipeline
            | "Crear datos" >> beam.Create(pacientes)
            | "Extraer key" >> beam.Map(lambda p: (p["diagnostico"], p))
            | "Agrupar" >> beam.GroupByKey()
            | "Calcular stats" >> beam.ParDo(CalcularEstadisticas())
            | "Imprimir" >> beam.Map(print)
        )


run_pipeline()
```

**Salida**:
```
{'diagnostico': 'Diabetes', 'total_pacientes': 2, 'edad_promedio': 47.5, 'edad_min': 45, 'edad_max': 50}
{'diagnostico': 'Hipertensión', 'total_pacientes': 3, 'edad_promedio': 49.0, 'edad_min': 32, 'edad_max': 60}
```

---

### Solución Ejercicio 8

```python
from google.cloud import pubsub_v1
import json
from datetime import datetime


def publicar_evento_paciente(
    project_id: str,
    topic_id: str,
    paciente: dict
) -> str:
    """
    Publica evento de paciente a Pub/Sub.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Construir evento
    evento = {
        "tipo_evento": "paciente_registrado",
        "paciente_id": paciente["paciente_id"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "datos": {
            "nombre": paciente["nombre"],
            "edad": paciente["edad"]
        }
    }

    # Serializar y publicar
    mensaje_json = json.dumps(evento)
    mensaje_bytes = mensaje_json.encode("utf-8")

    future = publisher.publish(topic_path, mensaje_bytes)
    message_id = future.result()

    print(f"✅ Evento publicado: {message_id}")

    return message_id


# Uso
paciente = {
    "paciente_id": "P001",
    "nombre": "Juan Pérez",
    "edad": 45,
    "diagnostico": "Diabetes"
}

message_id = publicar_evento_paciente(
    project_id="healthtech-prod",
    topic_id="pacientes-eventos",
    paciente=paciente
)
```

---

### Solución Ejercicio 9

```python
from google.cloud import pubsub_v1
from typing import Callable


def consumir_eventos_batch(
    project_id: str,
    subscription_id: str,
    callback: Callable,
    max_mensajes: int = 10
) -> int:
    """
    Consume eventos en batch desde Pub/Sub.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Pull manual de mensajes
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": max_mensajes
        }
    )

    mensajes_procesados = 0
    ack_ids = []

    for received_message in response.received_messages:
        try:
            # Procesar mensaje
            callback(received_message.message)

            # Marcar para ACK
            ack_ids.append(received_message.ack_id)
            mensajes_procesados += 1

        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")

    # ACK de todos los mensajes procesados
    if ack_ids:
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": ack_ids
            }
        )

    print(f"✅ Procesados {mensajes_procesados} mensajes")

    return mensajes_procesados


# Uso
def procesar_mensaje(message):
    data = json.loads(message.data)
    print(f"📨 Evento: {data['tipo_evento']} - Paciente: {data['paciente_id']}")


mensajes = consumir_eventos_batch(
    project_id="healthtech-prod",
    subscription_id="pacientes-subscription",
    callback=procesar_mensaje,
    max_mensajes=10
)
```

---

### Solución Ejercicio 10

```sql
-- Query con window functions
SELECT
    fecha_registro,
    diagnostico,
    total_pacientes,

    -- Total acumulado por diagnóstico
    SUM(total_pacientes) OVER (
        PARTITION BY diagnostico
        ORDER BY fecha_registro
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as total_acumulado,

    -- Cambio vs día anterior
    total_pacientes - LAG(total_pacientes) OVER (
        PARTITION BY diagnostico
        ORDER BY fecha_registro
    ) as cambio_vs_dia_anterior

FROM (
    SELECT
        fecha_registro,
        diagnostico,
        COUNT(*) as total_pacientes
    FROM `healthtech-prod.analytics.pacientes`
    GROUP BY fecha_registro, diagnostico
)

ORDER BY diagnostico, fecha_registro
```

**Resultado**:
```
fecha_registro | diagnostico | total_pacientes | total_acumulado | cambio_vs_dia_anterior
2025-01-10 | Diabetes | 5 | 5 | NULL
2025-01-11 | Diabetes | 8 | 13 | 3
2025-01-12 | Diabetes | 6 | 19 | -2
2025-01-10 | Hipertensión | 3 | 3 | NULL
2025-01-11 | Hipertensión | 4 | 7 | 1
2025-01-12 | Hipertensión | 7 | 14 | 3
```

---

### Soluciones Ejercicios 11-15

Debido a la complejidad de los ejercicios avanzados (11-15), aquí están las **soluciones conceptuales** con código parcial. Para implementaciones completas, se recomienda revisar los ejemplos trabajados en `02-EJEMPLOS.md`.

#### Solución Ejercicio 11 (Streaming básico)

```python
# Pipeline Dataflow Streaming
with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(
            subscription=f"projects/{project_id}/subscriptions/{subscription_id}"
        )
        | "Parse JSON" >> beam.Map(lambda msg: json.loads(msg))
        | "Validate" >> beam.ParDo(ValidarPaciente())
        | "Enrich" >> beam.ParDo(EnriquecerPaciente())
        | "Write to BQ" >> beam.io.WriteToBigQuery(
            f"{project_id}:analytics.pacientes_streaming",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )
```

#### Solución Ejercicio 12 (Windowing)

```python
# Aplicar ventanas de 5 minutos
(
    pipeline
    | "Read" >> beam.io.ReadFromPubSub(...)
    | "Window" >> beam.WindowInto(beam.window.FixedWindows(5 * 60))
    | "Extract key" >> beam.Map(lambda p: (p["diagnostico"], 1))
    | "Group" >> beam.CombinePerKey(sum)
    | "Format" >> beam.ParDo(FormatearConWindow())  # Accede a window
    | "Write" >> beam.io.WriteToBigQuery(...)
)
```

#### Solución Ejercicio 13 (Cloud Composer DAG)

Ver ejemplo completo en `02-EJEMPLOS.md`, Ejemplo 5 (Cloud Composer).

#### Solución Ejercicio 14 (Sistema de Alertas)

```python
# Pipeline con filtro y segundo topic
(
    pipeline
    | "Read" >> beam.io.ReadFromPubSub(subscription="pacientes-eventos")
    | "Parse" >> beam.Map(lambda msg: json.loads(msg))
    | "Filter High Risk" >> beam.Filter(es_alto_riesgo)
    | "Format Alert" >> beam.Map(formatear_alerta)
    | "Publish Alert" >> beam.io.WriteToPubSub(topic="pacientes-alertas-alto-riesgo")
)

def es_alto_riesgo(paciente: dict) -> bool:
    return (
        paciente["edad"] > 60 and
        paciente["diagnostico"] in ["Diabetes", "Hipertensión"]
    )
```

#### Solución Ejercicio 15 (Pipeline End-to-End)

Combina todos los elementos anteriores:
1. Pub/Sub para ingesta
2. Dataflow Streaming con métricas
3. BigQuery para almacenamiento
4. Cloud Logging para monitoreo
5. Cloud Functions para notificaciones
6. Cloud Composer para orquestación

Ver arquitectura completa en `02-EJEMPLOS.md`, Ejemplo 5.

---

## 🎯 Checklist de Progreso

Marca los ejercicios que hayas completado:

**Básicos**:
- [ ] Ejercicio 1: Subir/Descargar archivos a GCS
- [ ] Ejercicio 2: Lifecycle policies
- [ ] Ejercicio 3: Crear tabla en BigQuery
- [ ] Ejercicio 4: Query SQL básica
- [ ] Ejercicio 5: Cargar CSV a BigQuery

**Intermedios**:
- [ ] Ejercicio 6: Pipeline Dataflow de limpieza
- [ ] Ejercicio 7: Agregaciones en Dataflow
- [ ] Ejercicio 8: Publicar eventos a Pub/Sub
- [ ] Ejercicio 9: Consumir eventos en batch
- [ ] Ejercicio 10: Window functions en BigQuery

**Avanzados**:
- [ ] Ejercicio 11: Dataflow Streaming
- [ ] Ejercicio 12: Windowing en Dataflow
- [ ] Ejercicio 13: Cloud Composer DAG
- [ ] Ejercicio 14: Sistema de alertas
- [ ] Ejercicio 15: Pipeline end-to-end

---

## 🚀 Siguiente Paso

Una vez completes todos los ejercicios, estás listo para el **proyecto práctico final** donde integrarás todos estos conceptos en un sistema de producción real.

**👉 Continúa con**: `04-proyecto-practico/`

---

*Última actualización: 2025-01-15*
