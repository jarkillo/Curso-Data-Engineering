# 📚 Ejemplos Trabajados: GCP para Data Engineering

## Introducción

Esta sección contiene **5 ejemplos trabajados** que muestran cómo usar los servicios de GCP para resolver problemas reales de Data Engineering. Los ejemplos aumentan progresivamente en complejidad:

- ⭐ **Ejemplo 1**: Cloud Storage - Operaciones básicas (upload, download, list)
- ⭐⭐ **Ejemplo 2**: BigQuery - Queries analíticas y particionamiento
- ⭐⭐⭐ **Ejemplo 3**: Dataflow - Pipeline ETL con Apache Beam
- ⭐⭐⭐ **Ejemplo 4**: Pub/Sub - Ingesta en tiempo real
- ⭐⭐⭐⭐ **Ejemplo 5**: Cloud Composer - Orquestación end-to-end

Cada ejemplo incluye:
- Contexto empresarial
- Código completo
- Explicación paso a paso
- Resultados esperados
- Decisiones de negocio basadas en datos

---

## ⭐ Ejemplo 1: Cloud Storage - Sistema de Backups Automáticos

### Contexto Empresarial

**Empresa**: **RestaurantData Co.** (cadena de 50 restaurantes)

**Problema**: Los restaurantes generan archivos CSV diarios con ventas, inventario y pedidos. Necesitan un sistema de backups automático que:
1. Suba archivos locales a Cloud Storage
2. Organice por fecha (particionamiento)
3. Aplique lifecycle policy para mover a Cold Storage después de 30 días

### Arquitectura

```
Archivos locales → Cloud Storage (Standard) → [30 días] → Nearline → [90 días] → Coldline
```

### Código Completo

```python
"""
Módulo para gestionar backups en Cloud Storage.
"""

from google.cloud import storage
from pathlib import Path
from datetime import datetime
from typing import Optional


def crear_bucket_con_lifecycle(
    project_id: str,
    bucket_name: str,
    location: str = "us-central1"
) -> storage.Bucket:
    """
    Crea un bucket con lifecycle policy para optimizar costos.

    Args:
        project_id: ID del proyecto GCP
        bucket_name: Nombre del bucket (debe ser único globalmente)
        location: Región del bucket

    Returns:
        Objeto Bucket creado

    Examples:
        >>> bucket = crear_bucket_con_lifecycle(
        ...     "restaurantdata-prod",
        ...     "restaurantdata-backups",
        ...     "us-central1"
        ... )
        >>> bucket.name
        'restaurantdata-backups'
    """
    # Inicializar cliente
    client = storage.Client(project=project_id)

    # Crear bucket
    bucket = client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    bucket.location = location

    # Configurar lifecycle rules
    rule_nearline = storage.bucket.LifecycleRule(
        action={"type": "SetStorageClass", "storageClass": "NEARLINE"},
        condition={"age": 30}  # Después de 30 días
    )

    rule_coldline = storage.bucket.LifecycleRule(
        action={"type": "SetStorageClass", "storageClass": "COLDLINE"},
        condition={"age": 120}  # Después de 120 días
    )

    rule_delete = storage.bucket.LifecycleRule(
        action={"type": "Delete"},
        condition={"age": 365}  # Eliminar después de 1 año
    )

    bucket.lifecycle_rules = [rule_nearline, rule_coldline, rule_delete]

    # Crear bucket en GCP
    bucket.create()

    print(f"✅ Bucket '{bucket_name}' creado con lifecycle policies")

    return bucket


def subir_archivo_con_particionamiento(
    bucket_name: str,
    archivo_local: str,
    tipo_dato: str = "ventas"
) -> str:
    """
    Sube un archivo a Cloud Storage con particionamiento por fecha.

    Args:
        bucket_name: Nombre del bucket destino
        archivo_local: Ruta al archivo local
        tipo_dato: Tipo de dato (ventas, inventario, pedidos)

    Returns:
        URI del archivo en GCS (gs://...)

    Examples:
        >>> uri = subir_archivo_con_particionamiento(
        ...     "restaurantdata-backups",
        ...     "/data/ventas_2025-01-15.csv",
        ...     "ventas"
        ... )
        >>> uri
        'gs://restaurantdata-backups/ventas/year=2025/month=01/day=15/ventas_2025-01-15.csv'
    """
    # Inicializar cliente
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Obtener fecha actual
    fecha = datetime.now()
    year = fecha.strftime("%Y")
    month = fecha.strftime("%m")
    day = fecha.strftime("%d")

    # Construir ruta particionada (Hive-style)
    archivo_path = Path(archivo_local)
    nombre_archivo = archivo_path.name

    ruta_destino = (
        f"{tipo_dato}/year={year}/month={month}/day={day}/{nombre_archivo}"
    )

    # Subir archivo
    blob = bucket.blob(ruta_destino)
    blob.upload_from_filename(archivo_local)

    # Configurar metadata
    blob.metadata = {
        "tipo": tipo_dato,
        "fecha_subida": datetime.now().isoformat(),
        "origen": "backup_automatico"
    }
    blob.patch()

    uri = f"gs://{bucket_name}/{ruta_destino}"
    print(f"✅ Archivo subido: {uri}")

    return uri


def listar_archivos_por_fecha(
    bucket_name: str,
    tipo_dato: str,
    fecha_inicio: str,
    fecha_fin: str
) -> list[str]:
    """
    Lista archivos en un rango de fechas.

    Args:
        bucket_name: Nombre del bucket
        tipo_dato: Tipo de dato (ventas, inventario, pedidos)
        fecha_inicio: Fecha inicio (YYYY-MM-DD)
        fecha_fin: Fecha fin (YYYY-MM-DD)

    Returns:
        Lista de URIs de archivos

    Examples:
        >>> archivos = listar_archivos_por_fecha(
        ...     "restaurantdata-backups",
        ...     "ventas",
        ...     "2025-01-01",
        ...     "2025-01-15"
        ... )
        >>> len(archivos)
        15
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Convertir fechas
    fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d")

    archivos = []

    # Listar blobs con prefijo
    blobs = bucket.list_blobs(prefix=f"{tipo_dato}/")

    for blob in blobs:
        # Extraer fecha del path (ventas/year=2025/month=01/day=15/...)
        parts = blob.name.split("/")

        if len(parts) >= 4:
            year = parts[1].split("=")[1]
            month = parts[2].split("=")[1]
            day = parts[3].split("=")[1]

            fecha_blob = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

            if fecha_inicio_obj <= fecha_blob <= fecha_fin_obj:
                archivos.append(f"gs://{bucket_name}/{blob.name}")

    return archivos


def descargar_archivo(uri: str, destino_local: str) -> None:
    """
    Descarga un archivo desde Cloud Storage.

    Args:
        uri: URI del archivo (gs://bucket/path)
        destino_local: Ruta local destino

    Examples:
        >>> descargar_archivo(
        ...     "gs://restaurantdata-backups/ventas/year=2025/month=01/day=15/ventas.csv",
        ...     "/tmp/ventas_recuperado.csv"
        ... )
        ✅ Archivo descargado: /tmp/ventas_recuperado.csv
    """
    # Parsear URI
    uri_parts = uri.replace("gs://", "").split("/", 1)
    bucket_name = uri_parts[0]
    blob_path = uri_parts[1]

    # Descargar
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.download_to_filename(destino_local)

    print(f"✅ Archivo descargado: {destino_local}")
```

### Paso a Paso

#### 1. Crear Bucket con Lifecycle Policy

```python
bucket = crear_bucket_con_lifecycle(
    project_id="restaurantdata-prod",
    bucket_name="restaurantdata-backups",
    location="us-central1"
)
```

**Resultado**:
```
✅ Bucket 'restaurantdata-backups' creado con lifecycle policies
```

**Lifecycle configurado**:
- Día 0-30: STANDARD ($0.020/GB/mes)
- Día 30-120: NEARLINE ($0.010/GB/mes)
- Día 120-365: COLDLINE ($0.004/GB/mes)
- Día 365+: Eliminado

#### 2. Subir Archivo con Particionamiento

```python
uri = subir_archivo_con_particionamiento(
    bucket_name="restaurantdata-backups",
    archivo_local="/data/ventas_2025-01-15.csv",
    tipo_dato="ventas"
)

print(uri)
```

**Resultado**:
```
✅ Archivo subido: gs://restaurantdata-backups/ventas/year=2025/month=01/day=15/ventas_2025-01-15.csv
```

**Estructura en GCS**:
```
restaurantdata-backups/
└── ventas/
    └── year=2025/
        └── month=01/
            └── day=15/
                └── ventas_2025-01-15.csv
```

#### 3. Listar Archivos por Rango de Fechas

```python
archivos = listar_archivos_por_fecha(
    bucket_name="restaurantdata-backups",
    tipo_dato="ventas",
    fecha_inicio="2025-01-01",
    fecha_fin="2025-01-15"
)

for archivo in archivos:
    print(archivo)
```

**Resultado**:
```
gs://restaurantdata-backups/ventas/year=2025/month=01/day=01/ventas_2025-01-01.csv
gs://restaurantdata-backups/ventas/year=2025/month=01/day=02/ventas_2025-01-02.csv
...
gs://restaurantdata-backups/ventas/year=2025/month=01/day=15/ventas_2025-01-15.csv
```

#### 4. Recuperar Archivo

```python
descargar_archivo(
    uri="gs://restaurantdata-backups/ventas/year=2025/month=01/day=15/ventas_2025-01-15.csv",
    destino_local="/tmp/ventas_recuperado.csv"
)
```

**Resultado**:
```
✅ Archivo descargado: /tmp/ventas_recuperado.csv
```

### Cálculo de Costos

**Datos**:
- 50 restaurantes × 3 archivos/día (ventas, inventario, pedidos) × 100 KB = **15 MB/día**
- **450 MB/mes** (15 MB × 30 días)
- **5.4 GB/año**

**Costos mensuales**:
- Días 0-30: 450 MB × $0.020/GB = **$0.009**
- Días 30-120: 450 MB × 3 meses × $0.010/GB = **$0.014**
- Días 120-365: 450 MB × 8 meses × $0.004/GB = **$0.014**

**Total anual**: ~$0.44 (¡céntimos!)

**Sin lifecycle policy**: 5.4 GB × $0.020/GB × 12 = **$1.30/año**

**Ahorro**: 66% ($0.86/año)

### Decisiones de Negocio

1. ✅ **Implementar lifecycle policy**: Ahorra 66% en costos de almacenamiento
2. ✅ **Usar particionamiento Hive-style**: Facilita consultas futuras con BigQuery
3. ✅ **Mantener backups 1 año**: Suficiente para auditorías fiscales
4. ✅ **Región us-central1**: Más barata que multi-región

---

## ⭐⭐ Ejemplo 2: BigQuery - Análisis de Ventas con Particionamiento

### Contexto Empresarial

**Empresa**: **RestaurantData Co.** (misma del Ejemplo 1)

**Problema**: Ahora que los archivos están en Cloud Storage, necesitan:
1. Cargar datos en BigQuery para análisis
2. Crear tabla particionada por fecha
3. Ejecutar queries analíticas (métricas de ventas por restaurante)

### Arquitectura

```
Cloud Storage → BigQuery (tabla particionada) → Queries SQL → Visualización
```

### Código Completo

```python
"""
Módulo para análisis de ventas en BigQuery.
"""

from google.cloud import bigquery
from typing import Optional


def crear_dataset(
    project_id: str,
    dataset_id: str,
    location: str = "US"
) -> bigquery.Dataset:
    """
    Crea un dataset en BigQuery.

    Args:
        project_id: ID del proyecto GCP
        dataset_id: ID del dataset
        location: Ubicación del dataset

    Returns:
        Objeto Dataset creado

    Examples:
        >>> dataset = crear_dataset(
        ...     "restaurantdata-prod",
        ...     "analytics",
        ...     "US"
        ... )
        >>> dataset.dataset_id
        'analytics'
    """
    client = bigquery.Client(project=project_id)

    # Crear dataset
    dataset_ref = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = location

    # Configurar expiración por defecto (opcional)
    dataset.default_table_expiration_ms = None  # Sin expiración

    dataset = client.create_dataset(dataset, exists_ok=True)

    print(f"✅ Dataset '{dataset_id}' creado en {location}")

    return dataset


def crear_tabla_particionada_ventas(
    project_id: str,
    dataset_id: str,
    tabla_id: str
) -> bigquery.Table:
    """
    Crea tabla particionada para ventas.

    Args:
        project_id: ID del proyecto
        dataset_id: ID del dataset
        tabla_id: ID de la tabla

    Returns:
        Objeto Table creado

    Examples:
        >>> tabla = crear_tabla_particionada_ventas(
        ...     "restaurantdata-prod",
        ...     "analytics",
        ...     "ventas"
        ... )
        >>> tabla.table_id
        'ventas'
    """
    client = bigquery.Client(project=project_id)

    # Definir schema
    schema = [
        bigquery.SchemaField("fecha", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("restaurante_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("producto", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("cantidad", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("precio_unitario", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("total", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("metodo_pago", "STRING", mode="REQUIRED"),
    ]

    # Crear tabla
    table_ref = f"{project_id}.{dataset_id}.{tabla_id}"
    tabla = bigquery.Table(table_ref, schema=schema)

    # Configurar particionamiento por fecha
    tabla.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="fecha",  # Campo de fecha
        expiration_ms=None  # Sin expiración de particiones
    )

    # Configurar clustering (opcional, mejora performance)
    tabla.clustering_fields = ["restaurante_id", "producto"]

    tabla = client.create_table(tabla, exists_ok=True)

    print(f"✅ Tabla particionada '{tabla_id}' creada")

    return tabla


def cargar_desde_gcs_a_bigquery(
    project_id: str,
    dataset_id: str,
    tabla_id: str,
    uri_gcs: str
) -> bigquery.LoadJob:
    """
    Carga datos desde Cloud Storage a BigQuery.

    Args:
        project_id: ID del proyecto
        dataset_id: ID del dataset
        tabla_id: ID de la tabla
        uri_gcs: URI del archivo en GCS (gs://...)

    Returns:
        Job de carga completado

    Examples:
        >>> job = cargar_desde_gcs_a_bigquery(
        ...     "restaurantdata-prod",
        ...     "analytics",
        ...     "ventas",
        ...     "gs://restaurantdata-backups/ventas/year=2025/month=01/day=*/ventas_*.csv"
        ... )
        >>> job.state
        'DONE'
    """
    client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset_id}.{tabla_id}"

    # Configurar job de carga
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Header
        autodetect=False,  # Usamos schema definido
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # Agregar datos
    )

    # Iniciar carga
    load_job = client.load_table_from_uri(
        uri_gcs,
        table_ref,
        job_config=job_config
    )

    # Esperar a que termine
    load_job.result()

    print(f"✅ Datos cargados: {load_job.output_rows} filas")

    return load_job


def ejecutar_query_metricas_ventas(
    project_id: str,
    dataset_id: str,
    tabla_id: str,
    fecha_inicio: str,
    fecha_fin: str
) -> list[dict]:
    """
    Ejecuta query para calcular métricas de ventas.

    Args:
        project_id: ID del proyecto
        dataset_id: ID del dataset
        tabla_id: ID de la tabla
        fecha_inicio: Fecha inicio (YYYY-MM-DD)
        fecha_fin: Fecha fin (YYYY-MM-DD)

    Returns:
        Lista de resultados como diccionarios

    Examples:
        >>> resultados = ejecutar_query_metricas_ventas(
        ...     "restaurantdata-prod",
        ...     "analytics",
        ...     "ventas",
        ...     "2025-01-01",
        ...     "2025-01-31"
        ... )
        >>> resultados[0]['restaurante_id']
        'REST-001'
    """
    client = bigquery.Client(project=project_id)

    # Query SQL optimizada (usa particionamiento)
    query = f"""
    SELECT
        restaurante_id,
        COUNT(*) as total_transacciones,
        SUM(total) as ingresos_totales,
        AVG(total) as ticket_promedio,
        COUNT(DISTINCT fecha) as dias_activos,
        COUNT(DISTINCT producto) as productos_unicos
    FROM `{project_id}.{dataset_id}.{tabla_id}`
    WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    GROUP BY restaurante_id
    ORDER BY ingresos_totales DESC
    LIMIT 10
    """

    # Ejecutar query
    query_job = client.query(query)

    # Convertir a lista de diccionarios
    resultados = []
    for row in query_job:
        resultados.append({
            "restaurante_id": row.restaurante_id,
            "total_transacciones": row.total_transacciones,
            "ingresos_totales": round(row.ingresos_totales, 2),
            "ticket_promedio": round(row.ticket_promedio, 2),
            "dias_activos": row.dias_activos,
            "productos_unicos": row.productos_unicos
        })

    return resultados


def ejecutar_query_productos_top(
    project_id: str,
    dataset_id: str,
    tabla_id: str
) -> list[dict]:
    """
    Obtiene los productos más vendidos.

    Args:
        project_id: ID del proyecto
        dataset_id: ID del dataset
        tabla_id: ID de la tabla

    Returns:
        Top 10 productos por ingresos

    Examples:
        >>> productos = ejecutar_query_productos_top(
        ...     "restaurantdata-prod",
        ...     "analytics",
        ...     "ventas"
        ... )
        >>> productos[0]['producto']
        'Pizza Margherita'
    """
    client = bigquery.Client(project=project_id)

    query = f"""
    SELECT
        producto,
        SUM(cantidad) as unidades_vendidas,
        SUM(total) as ingresos_totales,
        AVG(precio_unitario) as precio_promedio,
        COUNT(DISTINCT restaurante_id) as restaurantes_vendiendo
    FROM `{project_id}.{dataset_id}.{tabla_id}`
    GROUP BY producto
    ORDER BY ingresos_totales DESC
    LIMIT 10
    """

    query_job = client.query(query)

    resultados = []
    for row in query_job:
        resultados.append({
            "producto": row.producto,
            "unidades_vendidas": row.unidades_vendidas,
            "ingresos_totales": round(row.ingresos_totales, 2),
            "precio_promedio": round(row.precio_promedio, 2),
            "restaurantes_vendiendo": row.restaurantes_vendiendo
        })

    return resultados
```

### Paso a Paso

#### 1. Crear Dataset

```python
dataset = crear_dataset(
    project_id="restaurantdata-prod",
    dataset_id="analytics",
    location="US"
)
```

**Resultado**:
```
✅ Dataset 'analytics' creado en US
```

#### 2. Crear Tabla Particionada

```python
tabla = crear_tabla_particionada_ventas(
    project_id="restaurantdata-prod",
    dataset_id="analytics",
    tabla_id="ventas"
)
```

**Resultado**:
```
✅ Tabla particionada 'ventas' creada
```

**Schema creado**:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| fecha | DATE | Fecha de la venta (particionamiento) |
| restaurante_id | STRING | ID del restaurante |
| producto | STRING | Nombre del producto |
| cantidad | INTEGER | Unidades vendidas |
| precio_unitario | FLOAT | Precio por unidad |
| total | FLOAT | Monto total de la transacción |
| metodo_pago | STRING | Efectivo, tarjeta, etc. |

**Clustering**: `restaurante_id`, `producto` (mejora queries filtradas por estos campos)

#### 3. Cargar Datos desde Cloud Storage

```python
job = cargar_desde_gcs_a_bigquery(
    project_id="restaurantdata-prod",
    dataset_id="analytics",
    tabla_id="ventas",
    uri_gcs="gs://restaurantdata-backups/ventas/year=2025/month=01/day=*/ventas_*.csv"
)
```

**Resultado**:
```
✅ Datos cargados: 45,000 filas
```

**Ventaja del particionamiento**: BigQuery solo escanea particiones relevantes, reduciendo costos.

#### 4. Ejecutar Query de Métricas

```python
resultados = ejecutar_query_metricas_ventas(
    project_id="restaurantdata-prod",
    dataset_id="analytics",
    tabla_id="ventas",
    fecha_inicio="2025-01-01",
    fecha_fin="2025-01-31"
)

import pandas as pd
df = pd.DataFrame(resultados)
print(df.to_string(index=False))
```

**Resultado**:
```
 restaurante_id  total_transacciones  ingresos_totales  ticket_promedio  dias_activos  productos_unicos
       REST-023                 1250          35420.50            28.34            31                42
       REST-007                 1180          33890.20            28.72            31                39
       REST-041                 1120          31250.80            27.90            30                41
       REST-015                 1090          30120.40            27.63            31                38
       REST-033                 1050          28950.60            27.57            29                40
```

**Bytes procesados**: ~15 MB (solo particiones de enero)

**Costo**: 15 MB / 1024 = 0.0146 GB × $5/TB = **$0.000073** (¡7 centavos de centavo!)

#### 5. Top Productos

```python
productos = ejecutar_query_productos_top(
    project_id="restaurantdata-prod",
    dataset_id="analytics",
    tabla_id="ventas"
)

df_productos = pd.DataFrame(productos)
print(df_productos.to_string(index=False))
```

**Resultado**:
```
           producto  unidades_vendidas  ingresos_totales  precio_promedio  restaurantes_vendiendo
  Pizza Margherita               8750         105000.00            12.00                        50
        Hamburguesa               7200          79200.00            11.00                        48
     Ensalada César               6500          58500.00             9.00                        45
    Pasta Carbonara               5800          69600.00            12.00                        47
  Refresco Coca-Cola              9200          27600.00             3.00                        50
```

### Cálculo de Costos

**Datos**:
- 50 restaurantes × 30 transacciones/día × 31 días = **46,500 transacciones/mes**
- Tamaño: ~15 MB/mes
- Queries: 100 queries/mes × 15 MB promedio = **1.5 GB procesados/mes**

**Costos mensuales**:
- **Almacenamiento**: 15 MB × $0.020/GB = **$0.0003** (¡céntimo de centavo!)
- **Queries**: 1.5 GB × $5/TB = 1.5/1024 × $5 = **$0.007**

**Total mensual**: **$0.0073** (¡menos de 1 centavo!)

**Beneficio del particionamiento**:
- Sin particionamiento: Escanearía TODA la tabla cada query
- Con particionamiento: Solo escanea particiones relevantes (ahorro de 90%+)

### Decisiones de Negocio

1. ✅ **REST-023 es el top performer**: Considerar replicar su modelo en otros restaurantes
2. ✅ **Pizza Margherita genera más ingresos**: Mantener en stock y promover
3. ✅ **Ticket promedio ~$28**: Ofrecer combos de $30-35 para aumentar ticket
4. ⚠️ **Algunos restaurantes con <30 días activos**: Investigar cierres o problemas

---

## ⭐⭐⭐ Ejemplo 3: Dataflow - Pipeline ETL con Apache Beam

### Contexto Empresarial

**Empresa**: **CloudAPI Systems** (empresa de monitoreo de APIs)

**Problema**: Reciben logs de APIs en formato JSON desordenado desde Cloud Storage. Necesitan:
1. Leer archivos JSON en batch
2. Limpiar y validar datos
3. Calcular métricas agregadas (response times, error rates)
4. Guardar en BigQuery para análisis

### Arquitectura

```
Cloud Storage (JSON logs) → Dataflow Pipeline → BigQuery (tabla limpia + métricas)
```

### Código Completo

```python
"""
Pipeline Dataflow para procesar logs de APIs.
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io import ReadFromText, WriteToBigQuery
import json
from datetime import datetime
from typing import Optional


class ParsearJSON(beam.DoFn):
    """
    DoFn para parsear líneas JSON.
    """

    def process(self, line: str):
        """
        Parsea una línea JSON.

        Args:
            line: Línea de texto JSON

        Yields:
            Diccionario parseado
        """
        try:
            data = json.loads(line)
            yield data
        except json.JSONDecodeError:
            # Log error y descartar línea
            pass


class ValidarLog(beam.DoFn):
    """
    DoFn para validar logs de API.
    """

    def process(self, log: dict):
        """
        Valida que un log tenga campos requeridos.

        Args:
            log: Diccionario con datos del log

        Yields:
            Log válido
        """
        campos_requeridos = [
            "timestamp", "endpoint", "method",
            "status_code", "response_time_ms"
        ]

        # Verificar campos requeridos
        if all(campo in log for campo in campos_requeridos):
            # Validar tipos
            try:
                log["status_code"] = int(log["status_code"])
                log["response_time_ms"] = float(log["response_time_ms"])
                yield log
            except (ValueError, TypeError):
                pass


class EnriquecerLog(beam.DoFn):
    """
    DoFn para enriquecer logs con campos calculados.
    """

    def process(self, log: dict):
        """
        Agrega campos calculados al log.

        Args:
            log: Log validado

        Yields:
            Log enriquecido
        """
        # Agregar categoría de status
        status = log["status_code"]
        if 200 <= status < 300:
            log["status_category"] = "success"
        elif 400 <= status < 500:
            log["status_category"] = "client_error"
        elif 500 <= status < 600:
            log["status_category"] = "server_error"
        else:
            log["status_category"] = "other"

        # Agregar fecha (para particionamiento en BigQuery)
        try:
            timestamp_obj = datetime.fromisoformat(
                log["timestamp"].replace("Z", "+00:00")
            )
            log["fecha"] = timestamp_obj.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            log["fecha"] = None

        # Agregar flag de error
        log["es_error"] = 1 if status >= 400 else 0

        yield log


class CalcularMetricasPorEndpoint(beam.DoFn):
    """
    DoFn para calcular métricas agregadas por endpoint.
    """

    def process(self, element):
        """
        Calcula métricas para un endpoint.

        Args:
            element: Tupla (endpoint, lista_de_logs)

        Yields:
            Diccionario con métricas agregadas
        """
        endpoint, logs = element

        total_requests = len(logs)
        errores = sum(1 for log in logs if log["es_error"] == 1)
        response_times = [log["response_time_ms"] for log in logs]

        metricas = {
            "endpoint": endpoint,
            "total_requests": total_requests,
            "total_errores": errores,
            "error_rate": round((errores / total_requests) * 100, 2) if total_requests > 0 else 0,
            "avg_response_time": round(sum(response_times) / len(response_times), 2) if response_times else 0,
            "p50_response_time": round(sorted(response_times)[len(response_times) // 2], 2) if response_times else 0,
            "p95_response_time": round(sorted(response_times)[int(len(response_times) * 0.95)], 2) if len(response_times) >= 20 else 0,
        }

        yield metricas


def run_pipeline(
    input_path: str,
    output_table_logs: str,
    output_table_metrics: str,
    project_id: str,
    runner: str = "DirectRunner"
):
    """
    Ejecuta el pipeline Dataflow.

    Args:
        input_path: Ruta a archivos de input (gs://...)
        output_table_logs: Tabla BigQuery para logs limpios
        output_table_metrics: Tabla BigQuery para métricas
        project_id: ID del proyecto GCP
        runner: DirectRunner (local) o DataflowRunner (GCP)

    Examples:
        >>> run_pipeline(
        ...     "gs://cloudapi-logs/raw/2025-01-*/*.json",
        ...     "cloudapi-analytics:logs.processed",
        ...     "cloudapi-analytics:logs.metrics_by_endpoint",
        ...     "cloudapi-prod",
        ...     "DirectRunner"
        ... )
    """
    # Configurar opciones del pipeline
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = runner

    # Schema para BigQuery - logs limpios
    schema_logs = {
        "fields": [
            {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "endpoint", "type": "STRING", "mode": "REQUIRED"},
            {"name": "method", "type": "STRING", "mode": "REQUIRED"},
            {"name": "status_code", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "response_time_ms", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "status_category", "type": "STRING", "mode": "NULLABLE"},
            {"name": "fecha", "type": "DATE", "mode": "NULLABLE"},
            {"name": "es_error", "type": "INTEGER", "mode": "NULLABLE"},
        ]
    }

    # Schema para BigQuery - métricas agregadas
    schema_metrics = {
        "fields": [
            {"name": "endpoint", "type": "STRING", "mode": "REQUIRED"},
            {"name": "total_requests", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_errores", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "error_rate", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "avg_response_time", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "p50_response_time", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "p95_response_time", "type": "FLOAT", "mode": "REQUIRED"},
        ]
    }

    # Crear pipeline
    with beam.Pipeline(options=options) as pipeline:

        # Branch 1: Logs limpios
        logs_limpios = (
            pipeline
            | "Leer archivos" >> ReadFromText(input_path)
            | "Parsear JSON" >> beam.ParDo(ParsearJSON())
            | "Validar logs" >> beam.ParDo(ValidarLog())
            | "Enriquecer logs" >> beam.ParDo(EnriquecerLog())
        )

        # Guardar logs limpios en BigQuery
        logs_limpios | "Escribir logs a BigQuery" >> WriteToBigQuery(
            output_table_logs,
            schema=schema_logs,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )

        # Branch 2: Métricas agregadas
        metricas = (
            logs_limpios
            | "Extraer endpoint" >> beam.Map(lambda log: (log["endpoint"], log))
            | "Agrupar por endpoint" >> beam.GroupByKey()
            | "Calcular métricas" >> beam.ParDo(CalcularMetricasPorEndpoint())
        )

        # Guardar métricas en BigQuery
        metricas | "Escribir métricas a BigQuery" >> WriteToBigQuery(
            output_table_metrics,
            schema=schema_metrics,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )


# Ejecutar pipeline
if __name__ == "__main__":
    run_pipeline(
        input_path="gs://cloudapi-logs/raw/2025-01-15/*.json",
        output_table_logs="cloudapi-prod:cloudapi_analytics.logs_processed",
        output_table_metrics="cloudapi-prod:cloudapi_analytics.metrics_by_endpoint",
        project_id="cloudapi-prod",
        runner="DirectRunner"  # Cambiar a "DataflowRunner" para producción
    )
```

### Paso a Paso

#### 1. Arquitectura del Pipeline

```
[ReadFromText] → [ParsearJSON] → [ValidarLog] → [EnriquecerLog]
                                                        |
                                                        ├→ [WriteToBigQuery (logs)]
                                                        |
                                                        └→ [GroupByKey] → [Métricas] → [WriteToBigQuery (metrics)]
```

**Branches**:
1. **Logs limpios**: Se guardan en `logs_processed`
2. **Métricas agregadas**: Se calculan y guardan en `metrics_by_endpoint`

#### 2. Datos de Input

**Archivo**: `gs://cloudapi-logs/raw/2025-01-15/logs_001.json`

```json
{"timestamp": "2025-01-15T10:30:45Z", "endpoint": "/api/users", "method": "GET", "status_code": 200, "response_time_ms": 145}
{"timestamp": "2025-01-15T10:30:46Z", "endpoint": "/api/posts", "method": "GET", "status_code": 404, "response_time_ms": 89}
{"timestamp": "2025-01-15T10:30:47Z", "endpoint": "/api/users", "method": "POST", "status_code": 201, "response_time_ms": 234}
{"timestamp": "2025-01-15T10:30:48Z", "endpoint": "/api/users", "method": "GET", "status_code": 500, "response_time_ms": 2000}
```

#### 3. Ejecución Local (Testing)

```bash
python pipeline_dataflow.py
```

**Output (logs)**:
```
INFO:root:Pipeline started
INFO:root:Reading files from gs://cloudapi-logs/raw/2025-01-15/*.json
INFO:root:Processing 10,000 records
INFO:root:Validated: 9,850 records (98.5%)
INFO:root:Invalid: 150 records (1.5%)
INFO:root:Writing to BigQuery: cloudapi-prod:cloudapi_analytics.logs_processed
INFO:root:Writing to BigQuery: cloudapi-prod:cloudapi_analytics.metrics_by_endpoint
INFO:root:Pipeline completed successfully
```

#### 4. Resultados en BigQuery

**Tabla `logs_processed`** (sample):

| timestamp | endpoint | method | status_code | response_time_ms | status_category | fecha | es_error |
|-----------|----------|--------|-------------|------------------|-----------------|-------|----------|
| 2025-01-15 10:30:45 | /api/users | GET | 200 | 145 | success | 2025-01-15 | 0 |
| 2025-01-15 10:30:46 | /api/posts | GET | 404 | 89 | client_error | 2025-01-15 | 1 |
| 2025-01-15 10:30:47 | /api/users | POST | 201 | 234 | success | 2025-01-15 | 0 |
| 2025-01-15 10:30:48 | /api/users | GET | 500 | 2000 | server_error | 2025-01-15 | 1 |

**Tabla `metrics_by_endpoint`**:

| endpoint | total_requests | total_errores | error_rate | avg_response_time | p50_response_time | p95_response_time |
|----------|----------------|---------------|------------|-------------------|-------------------|-------------------|
| /api/users | 3500 | 120 | 3.43 | 156.50 | 145.00 | 450.00 |
| /api/posts | 2800 | 450 | 16.07 | 98.20 | 89.00 | 250.00 |
| /api/products | 1200 | 50 | 4.17 | 203.40 | 190.00 | 520.00 |

#### 5. Deployment en Dataflow (Producción)

```bash
python pipeline_dataflow.py \
  --runner DataflowRunner \
  --project cloudapi-prod \
  --region us-central1 \
  --temp_location gs://cloudapi-temp/dataflow/ \
  --staging_location gs://cloudapi-staging/dataflow/ \
  --num_workers 2 \
  --max_num_workers 10 \
  --autoscaling_algorithm THROUGHPUT_BASED
```

**Resultado**:
```
INFO:root:Dataflow job submitted: https://console.cloud.google.com/dataflow/jobs/...
Job ID: 2025-01-15_10_30_45-12345678901234567890
Status: Running
Workers: 2 (autoscaling up to 10)
```

### Cálculo de Costos

**Escenario**: Procesar 10 GB de logs diarios

**Dataflow pricing**:
- **vCPUs**: $0.056/vCPU-hour
- **Memory**: $0.003557/GB-hour
- **Disk**: $0.000054/GB-hour

**Configuración**:
- 2 workers × 4 vCPUs × 15 GB RAM
- Duración: 30 minutos

**Cálculo**:
- vCPUs: 2 workers × 4 vCPUs × 0.5 hours × $0.056 = **$0.224**
- Memory: 2 workers × 15 GB × 0.5 hours × $0.003557 = **$0.053**
- Disk: 2 workers × 250 GB × 0.5 hours × $0.000054 = **$0.014**

**Total por ejecución**: **$0.291**

**Mensual** (1x/día × 30 días): **$8.73**

**Optimización**:
- Usar Batch Dataflow (50% más barato): **$4.37/mes**
- Procesar menos frecuente (3x/semana): **$3.74/mes**

### Decisiones de Negocio

1. ✅ **/api/posts tiene alta tasa de errores (16%)**: Investigar causas, posiblemente mal uso del cliente
2. ✅ **/api/users es el endpoint más usado**: Optimizar su performance
3. ⚠️ **500 errors en /api/users**: Bug crítico que genera response times de 2000ms
4. ✅ **Usar Batch Dataflow**: Ahorrar 50% en costos procesando de noche

---

## ⭐⭐⭐ Ejemplo 4: Pub/Sub - Ingesta en Tiempo Real

### Contexto Empresarial

**Empresa**: **IoT Sensors Inc.** (sensores IoT en fábricas)

**Problema**: 10,000 sensores envían datos cada 5 segundos (temperatura, humedad, vibración). Necesitan:
1. Ingestar datos en tiempo real con Pub/Sub
2. Procesar con Dataflow Streaming
3. Guardar en BigQuery para análisis
4. Enviar alertas si temperatura > 80°C

### Arquitectura

```
Sensores IoT → Pub/Sub Topic → Dataflow Streaming → BigQuery
                                     ↓
                                 Alertas (Pub/Sub)
```

### Código Completo

```python
"""
Sistema de ingesta en tiempo real con Pub/Sub.
"""

from google.cloud import pubsub_v1
from concurrent import futures
import json
from datetime import datetime
from typing import Callable


def crear_topic(project_id: str, topic_id: str) -> str:
    """
    Crea un topic en Pub/Sub.

    Args:
        project_id: ID del proyecto GCP
        topic_id: ID del topic

    Returns:
        Nombre completo del topic

    Examples:
        >>> topic_name = crear_topic("iotsensors-prod", "sensor-readings")
        >>> topic_name
        'projects/iotsensors-prod/topics/sensor-readings'
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"✅ Topic creado: {topic.name}")
        return topic.name
    except Exception as e:
        print(f"⚠️  Topic ya existe o error: {e}")
        return topic_path


def crear_subscription(
    project_id: str,
    topic_id: str,
    subscription_id: str
) -> str:
    """
    Crea una subscription para consumir mensajes.

    Args:
        project_id: ID del proyecto
        topic_id: ID del topic
        subscription_id: ID de la subscription

    Returns:
        Nombre completo de la subscription

    Examples:
        >>> sub_name = crear_subscription(
        ...     "iotsensors-prod",
        ...     "sensor-readings",
        ...     "dataflow-subscription"
        ... )
        >>> sub_name
        'projects/iotsensors-prod/subscriptions/dataflow-subscription'
    """
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    try:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "ack_deadline_seconds": 60  # Tiempo para procesar mensaje
            }
        )
        print(f"✅ Subscription creada: {subscription.name}")
        return subscription.name
    except Exception as e:
        print(f"⚠️  Subscription ya existe o error: {e}")
        return subscription_path


def publicar_mensaje_sensor(
    project_id: str,
    topic_id: str,
    sensor_id: str,
    temperatura: float,
    humedad: float,
    vibracion: float
) -> str:
    """
    Publica un mensaje de sensor a Pub/Sub.

    Args:
        project_id: ID del proyecto
        topic_id: ID del topic
        sensor_id: ID del sensor
        temperatura: Temperatura en °C
        humedad: Humedad relativa (%)
        vibracion: Nivel de vibración (Hz)

    Returns:
        Message ID del mensaje publicado

    Examples:
        >>> message_id = publicar_mensaje_sensor(
        ...     "iotsensors-prod",
        ...     "sensor-readings",
        ...     "SENSOR-001",
        ...     75.5,
        ...     60.2,
        ...     15.8
        ... )
        >>> len(message_id) > 0
        True
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Construir mensaje
    mensaje = {
        "sensor_id": sensor_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "temperatura": temperatura,
        "humedad": humedad,
        "vibracion": vibracion
    }

    # Serializar a JSON
    mensaje_json = json.dumps(mensaje)
    mensaje_bytes = mensaje_json.encode("utf-8")

    # Publicar
    future = publisher.publish(topic_path, mensaje_bytes)
    message_id = future.result()

    print(f"✅ Mensaje publicado: {message_id} (sensor: {sensor_id})")

    return message_id


def publicar_batch_sensores(
    project_id: str,
    topic_id: str,
    mensajes: list[dict]
) -> list[str]:
    """
    Publica múltiples mensajes en batch.

    Args:
        project_id: ID del proyecto
        topic_id: ID del topic
        mensajes: Lista de diccionarios con datos de sensores

    Returns:
        Lista de message IDs

    Examples:
        >>> mensajes = [
        ...     {"sensor_id": "SENSOR-001", "temperatura": 75.5, "humedad": 60.2, "vibracion": 15.8},
        ...     {"sensor_id": "SENSOR-002", "temperatura": 82.0, "humedad": 55.1, "vibracion": 20.3}
        ... ]
        >>> message_ids = publicar_batch_sensores("iotsensors-prod", "sensor-readings", mensajes)
        >>> len(message_ids)
        2
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Configurar batching
    batch_settings = pubsub_v1.types.BatchSettings(
        max_messages=100,  # Max mensajes por batch
        max_bytes=1024 * 1024,  # Max 1 MB por batch
        max_latency=0.1,  # Max 100ms de espera
    )

    publisher_with_batch = pubsub_v1.PublisherClient(batch_settings)

    publish_futures = []

    for mensaje in mensajes:
        # Agregar timestamp si no existe
        if "timestamp" not in mensaje:
            mensaje["timestamp"] = datetime.utcnow().isoformat() + "Z"

        mensaje_json = json.dumps(mensaje)
        mensaje_bytes = mensaje_json.encode("utf-8")

        # Publicar async
        future = publisher_with_batch.publish(topic_path, mensaje_bytes)
        publish_futures.append(future)

    # Esperar a que todos terminen
    message_ids = [future.result() for future in publish_futures]

    print(f"✅ {len(message_ids)} mensajes publicados en batch")

    return message_ids


def consumir_mensajes(
    project_id: str,
    subscription_id: str,
    callback: Callable,
    timeout: float = 10.0
) -> None:
    """
    Consume mensajes desde una subscription.

    Args:
        project_id: ID del proyecto
        subscription_id: ID de la subscription
        callback: Función a ejecutar por cada mensaje
        timeout: Tiempo máximo de espera (segundos)

    Examples:
        >>> def procesar_mensaje(message):
        ...     data = json.loads(message.data)
        ...     print(f"Sensor: {data['sensor_id']}, Temp: {data['temperatura']}°C")
        ...     message.ack()
        ...
        >>> consumir_mensajes(
        ...     "iotsensors-prod",
        ...     "dataflow-subscription",
        ...     procesar_mensaje,
        ...     timeout=30.0
        ... )
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Iniciar streaming pull
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    print(f"✅ Escuchando mensajes en {subscription_path}...")

    try:
        # Bloquear hasta timeout
        streaming_pull_future.result(timeout=timeout)
    except futures.TimeoutError:
        streaming_pull_future.cancel()
        print("⏱️  Timeout alcanzado, deteniendo consumer")


# Ejemplo de uso completo
if __name__ == "__main__":
    PROJECT_ID = "iotsensors-prod"
    TOPIC_ID = "sensor-readings"
    SUBSCRIPTION_ID = "dataflow-subscription"

    # 1. Crear topic y subscription
    crear_topic(PROJECT_ID, TOPIC_ID)
    crear_subscription(PROJECT_ID, TOPIC_ID, SUBSCRIPTION_ID)

    # 2. Simular publicación de sensores
    import random

    mensajes = []
    for i in range(100):
        sensor_id = f"SENSOR-{i:03d}"
        temperatura = random.uniform(60, 90)  # 60-90°C
        humedad = random.uniform(40, 70)  # 40-70%
        vibracion = random.uniform(10, 30)  # 10-30 Hz

        mensajes.append({
            "sensor_id": sensor_id,
            "temperatura": round(temperatura, 2),
            "humedad": round(humedad, 2),
            "vibracion": round(vibracion, 2)
        })

    # Publicar en batch
    message_ids = publicar_batch_sensores(PROJECT_ID, TOPIC_ID, mensajes)

    # 3. Consumir mensajes
    def procesar_mensaje(message):
        data = json.loads(message.data)

        print(f"📊 Sensor: {data['sensor_id']}")
        print(f"   Temperatura: {data['temperatura']}°C")
        print(f"   Humedad: {data['humedad']}%")
        print(f"   Vibración: {data['vibracion']} Hz")

        # Alerta si temperatura > 80°C
        if data["temperatura"] > 80:
            print(f"🚨 ALERTA: Temperatura alta en {data['sensor_id']}")

        # Acknowledge mensaje
        message.ack()

    consumir_mensajes(PROJECT_ID, SUBSCRIPTION_ID, procesar_mensaje, timeout=30.0)
```

### Paso a Paso

#### 1. Crear Infraestructura

```python
PROJECT_ID = "iotsensors-prod"
TOPIC_ID = "sensor-readings"
SUBSCRIPTION_ID = "dataflow-subscription"

# Crear topic
crear_topic(PROJECT_ID, TOPIC_ID)

# Crear subscription
crear_subscription(PROJECT_ID, TOPIC_ID, SUBSCRIPTION_ID)
```

**Resultado**:
```
✅ Topic creado: projects/iotsensors-prod/topics/sensor-readings
✅ Subscription creada: projects/iotsensors-prod/subscriptions/dataflow-subscription
```

#### 2. Publicar Mensajes (Simulación de Sensores)

```python
# Simular 100 sensores enviando datos
mensajes = []
for i in range(100):
    mensajes.append({
        "sensor_id": f"SENSOR-{i:03d}",
        "temperatura": round(random.uniform(60, 90), 2),
        "humedad": round(random.uniform(40, 70), 2),
        "vibracion": round(random.uniform(10, 30), 2)
    })

message_ids = publicar_batch_sensores(PROJECT_ID, TOPIC_ID, mensajes)
```

**Resultado**:
```
✅ 100 mensajes publicados en batch
```

**Throughput**: 100 mensajes/0.5 segundos = **200 mensajes/segundo**

#### 3. Consumir Mensajes

```python
def procesar_mensaje(message):
    data = json.loads(message.data)

    print(f"📊 Sensor: {data['sensor_id']}, Temp: {data['temperatura']}°C")

    if data["temperatura"] > 80:
        print(f"🚨 ALERTA: Temperatura alta en {data['sensor_id']}")

    message.ack()

consumir_mensajes(PROJECT_ID, SUBSCRIPTION_ID, procesar_mensaje, timeout=30.0)
```

**Resultado**:
```
✅ Escuchando mensajes en projects/iotsensors-prod/subscriptions/dataflow-subscription...
📊 Sensor: SENSOR-001, Temp: 75.3°C
📊 Sensor: SENSOR-002, Temp: 82.5°C
🚨 ALERTA: Temperatura alta en SENSOR-002
📊 Sensor: SENSOR-003, Temp: 68.2°C
...
```

#### 4. Integración con Dataflow Streaming

```python
# Pipeline Dataflow Streaming
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_streaming_pipeline():
    options = PipelineOptions(
        streaming=True,
        runner="DataflowRunner"
    )

    with beam.Pipeline(options=options) as pipeline:
        mensajes = (
            pipeline
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(
                subscription=f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"
            )
            | "Parse JSON" >> beam.Map(lambda msg: json.loads(msg.decode("utf-8")))
            | "Filter High Temp" >> beam.Filter(lambda data: data["temperatura"] > 80)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                f"{PROJECT_ID}:sensors.high_temp_alerts",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )
```

### Cálculo de Costos

**Escenario**: 10,000 sensores × 12 mensajes/hora (cada 5 min) × 24 horas = **2.88 millones mensajes/día**

**Pub/Sub pricing**:
- **Primeros 50 TB**: $40/TiB
- **Tamaño promedio mensaje**: 200 bytes

**Cálculo**:
- 2.88M mensajes × 200 bytes = **576 MB/día** = **17.3 GB/mes**
- 17.3 GB / 1024 = 0.0169 TiB
- 0.0169 TiB × $40/TiB = **$0.68/mes**

**Storage de mensajes no reconocidos**:
- Si los mensajes se procesan en <1 min: **$0 extra**
- Si se acumulan: $0.27/GB/mes

**Total mensual**: **$0.68 - $1.50** (dependiendo de latencia)

**Muy económico** para millones de mensajes/día

### Decisiones de Negocio

1. ✅ **SENSOR-002 envía alertas frecuentes**: Inspeccionar físicamente el sensor o equipo
2. ✅ **Pub/Sub maneja 200 msg/s fácilmente**: Escalar a 100K sensores sin problemas
3. ✅ **Latencia <100ms**: Alertas en tiempo real funcionando correctamente
4. ✅ **Costo <$2/mes**: Solución muy económica para monitoreo IoT

---

## ⭐⭐⭐⭐ Ejemplo 5: Cloud Composer - Orquestación End-to-End

### Contexto Empresarial

**Empresa**: **EcommerceData Co.** (plataforma de e-commerce)

**Problema**: Pipeline complejo que necesita orquestación:
1. Extraer ventas diarias de Cloud Storage
2. Procesar con Dataflow
3. Cargar en BigQuery
4. Calcular métricas KPI
5. Enviar reporte por email

**Requisitos**:
- Ejecutar todos los días a las 2:00 AM
- Manejo de errores (retry con backoff)
- Notificaciones si falla
- Dependencies entre tareas

### Arquitectura

```
Cloud Composer (Airflow)
  ↓
[Extract GCS] → [Dataflow Job] → [Load BQ] → [Calculate KPIs] → [Send Email]
```

### Código Completo (DAG de Airflow)

```python
"""
DAG de Airflow para pipeline end-to-end de e-commerce.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import logging


# Configuración
PROJECT_ID = "ecommercedata-prod"
BUCKET_NAME = "ecommercedata-sales"
DATASET_ID = "analytics"
TABLE_ID = "daily_sales"

# Argumentos por defecto del DAG
default_args = {
    "owner": "data-engineering-team",
    "depends_on_past": False,  # No depende de ejecuciones anteriores
    "email": ["alerts@ecommercedata.com"],
    "email_on_failure": True,  # Email si falla
    "email_on_retry": False,
    "retries": 3,  # Reintentar 3 veces
    "retry_delay": timedelta(minutes=5),  # Esperar 5 min entre reintentos
    "start_date": days_ago(1),
}

# Crear DAG
dag = DAG(
    dag_id="ecommerce_daily_pipeline",
    default_args=default_args,
    description="Pipeline end-to-end para procesar ventas diarias",
    schedule_interval="0 2 * * *",  # 2:00 AM todos los días (cron)
    catchup=False,  # No ejecutar fechas pasadas
    tags=["ecommerce", "daily", "production"],
)


def verificar_archivos_gcs(**context):
    """
    Verifica que existan archivos en GCS para procesar.
    """
    from google.cloud import storage

    execution_date = context["execution_date"]
    fecha_str = execution_date.strftime("%Y-%m-%d")

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    # Buscar archivos con la fecha
    prefix = f"raw/ventas/fecha={fecha_str}/"
    blobs = list(bucket.list_blobs(prefix=prefix))

    if not blobs:
        raise FileNotFoundError(f"No se encontraron archivos para {fecha_str}")

    logging.info(f"✅ Encontrados {len(blobs)} archivos para procesar")

    # Pasar lista de archivos al contexto
    context["task_instance"].xcom_push(key="archivos_gcs", value=[blob.name for blob in blobs])

    return len(blobs)


def calcular_kpis(**context):
    """
    Calcula KPIs diarios desde BigQuery.
    """
    from google.cloud import bigquery

    execution_date = context["execution_date"]
    fecha_str = execution_date.strftime("%Y-%m-%d")

    client = bigquery.Client(project=PROJECT_ID)

    # Query para KPIs
    query = f"""
    SELECT
        '{fecha_str}' as fecha,
        COUNT(*) as total_ordenes,
        SUM(total) as ingresos_totales,
        AVG(total) as ticket_promedio,
        COUNT(DISTINCT cliente_id) as clientes_unicos,
        SUM(CASE WHEN estado = 'cancelado' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as tasa_cancelacion
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE fecha = '{fecha_str}'
    """

    query_job = client.query(query)
    resultados = list(query_job.result())

    if not resultados:
        raise ValueError(f"No hay datos para {fecha_str}")

    kpis = dict(resultados[0])

    logging.info(f"✅ KPIs calculados para {fecha_str}")
    logging.info(f"   Ingresos: ${kpis['ingresos_totales']:,.2f}")
    logging.info(f"   Órdenes: {kpis['total_ordenes']}")
    logging.info(f"   Ticket promedio: ${kpis['ticket_promedio']:.2f}")

    # Pasar KPIs al contexto
    context["task_instance"].xcom_push(key="kpis", value=kpis)

    return kpis


def generar_reporte_html(**context):
    """
    Genera reporte HTML con los KPIs.
    """
    ti = context["task_instance"]
    kpis = ti.xcom_pull(task_ids="calcular_kpis", key="kpis")

    execution_date = context["execution_date"]
    fecha_str = execution_date.strftime("%Y-%m-%d")

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>📊 Reporte Diario - {fecha_str}</h1>

        <h2>KPIs del Día</h2>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td>Total Órdenes</td>
                <td>{kpis['total_ordenes']:,}</td>
            </tr>
            <tr>
                <td>Ingresos Totales</td>
                <td>${kpis['ingresos_totales']:,.2f}</td>
            </tr>
            <tr>
                <td>Ticket Promedio</td>
                <td>${kpis['ticket_promedio']:.2f}</td>
            </tr>
            <tr>
                <td>Clientes Únicos</td>
                <td>{kpis['clientes_unicos']:,}</td>
            </tr>
            <tr>
                <td>Tasa de Cancelación</td>
                <td>{kpis['tasa_cancelacion']:.2f}%</td>
            </tr>
        </table>

        <p><em>Generado automáticamente por Cloud Composer</em></p>
    </body>
    </html>
    """

    context["task_instance"].xcom_push(key="reporte_html", value=html)

    return html


# Tareas del DAG

# Tarea 1: Verificar archivos
verificar_archivos = PythonOperator(
    task_id="verificar_archivos_gcs",
    python_callable=verificar_archivos_gcs,
    provide_context=True,
    dag=dag,
)

# Tarea 2: Ejecutar Dataflow
ejecutar_dataflow = DataflowTemplatedJobStartOperator(
    task_id="ejecutar_dataflow_processing",
    template="gs://dataflow-templates/latest/GCS_Text_to_BigQuery",
    parameters={
        "javascriptTextTransformFunctionName": "transform",
        "JSONPath": f"gs://{BUCKET_NAME}/schemas/ventas_schema.json",
        "javascriptTextTransformGcsPath": f"gs://{BUCKET_NAME}/transformations/ventas_transform.js",
        "inputFilePattern": f"gs://{BUCKET_NAME}/raw/ventas/fecha={{{{ ds }}}}/*.json",
        "outputTable": f"{PROJECT_ID}:{DATASET_ID}.{TABLE_ID}",
        "bigQueryLoadingTemporaryDirectory": f"gs://{BUCKET_NAME}/temp/bq/",
    },
    location="us-central1",
    project_id=PROJECT_ID,
    dag=dag,
)

# Tarea 3: Calcular KPIs
calcular_kpis_task = PythonOperator(
    task_id="calcular_kpis",
    python_callable=calcular_kpis,
    provide_context=True,
    dag=dag,
)

# Tarea 4: Generar reporte
generar_reporte = PythonOperator(
    task_id="generar_reporte_html",
    python_callable=generar_reporte_html,
    provide_context=True,
    dag=dag,
)

# Tarea 5: Enviar email
enviar_email = EmailOperator(
    task_id="enviar_email_reporte",
    to=["business-intelligence@ecommercedata.com"],
    subject="📊 Reporte Diario de Ventas - {{ ds }}",
    html_content="{{ task_instance.xcom_pull(task_ids='generar_reporte_html', key='reporte_html') }}",
    dag=dag,
)

# Definir dependencies (orden de ejecución)
verificar_archivos >> ejecutar_dataflow >> calcular_kpis_task >> generar_reporte >> enviar_email
```

### Paso a Paso

#### 1. Visualización del DAG en Airflow UI

```
[verificar_archivos_gcs]
          ↓
[ejecutar_dataflow_processing]
          ↓
    [calcular_kpis]
          ↓
 [generar_reporte_html]
          ↓
  [enviar_email_reporte]
```

**Colores**:
- 🟢 Verde: Éxito
- 🔴 Rojo: Fallo
- 🟡 Amarillo: Corriendo
- ⚪ Gris: No ejecutado

#### 2. Ejecución Manual (Testing)

En Airflow UI:
1. Ir a DAGs
2. Buscar `ecommerce_daily_pipeline`
3. Click en "Trigger DAG"
4. Seleccionar fecha de ejecución

**Log de ejecución**:
```
[2025-01-15 02:00:00] INFO - Starting DAG ecommerce_daily_pipeline
[2025-01-15 02:00:01] INFO - Task verificar_archivos_gcs: Running
[2025-01-15 02:00:05] INFO - ✅ Encontrados 12 archivos para procesar
[2025-01-15 02:00:05] INFO - Task verificar_archivos_gcs: Success
[2025-01-15 02:00:06] INFO - Task ejecutar_dataflow_processing: Running
[2025-01-15 02:03:45] INFO - Dataflow job completed: job_id=2025-01-15_02_00_06-1234567890
[2025-01-15 02:03:45] INFO - Task ejecutar_dataflow_processing: Success
[2025-01-15 02:03:46] INFO - Task calcular_kpis: Running
[2025-01-15 02:03:50] INFO - ✅ KPIs calculados para 2025-01-15
[2025-01-15 02:03:50] INFO -    Ingresos: $1,234,567.89
[2025-01-15 02:03:50] INFO -    Órdenes: 8,456
[2025-01-15 02:03:50] INFO - Task calcular_kpis: Success
[2025-01-15 02:03:51] INFO - Task generar_reporte_html: Running
[2025-01-15 02:03:52] INFO - Task generar_reporte_html: Success
[2025-01-15 02:03:53] INFO - Task enviar_email_reporte: Running
[2025-01-15 02:03:55] INFO - Email enviado a business-intelligence@ecommercedata.com
[2025-01-15 02:03:55] INFO - Task enviar_email_reporte: Success
[2025-01-15 02:03:55] INFO - DAG ecommerce_daily_pipeline: Success
```

**Duración total**: 3 minutos 55 segundos

#### 3. Manejo de Errores

**Escenario**: No hay archivos para procesar

```
[2025-01-16 02:00:05] ERROR - Task verificar_archivos_gcs: Failed
[2025-01-16 02:00:05] ERROR - FileNotFoundError: No se encontraron archivos para 2025-01-16
[2025-01-16 02:05:05] INFO - Retry 1/3 for task verificar_archivos_gcs
[2025-01-16 02:05:10] ERROR - Task verificar_archivos_gcs: Failed (retry 1)
[2025-01-16 02:10:10] INFO - Retry 2/3 for task verificar_archivos_gcs
[2025-01-16 02:10:15] ERROR - Task verificar_archivos_gcs: Failed (retry 2)
[2025-01-16 02:15:15] INFO - Retry 3/3 for task verificar_archivos_gcs
[2025-01-16 02:15:20] ERROR - Task verificar_archivos_gcs: Failed (retry 3)
[2025-01-16 02:15:20] INFO - Sending failure email to alerts@ecommercedata.com
```

**Email de alerta**:
```
Subject: 🚨 DAG Failed: ecommerce_daily_pipeline
From: Airflow <airflow@ecommercedata.com>
To: alerts@ecommercedata.com

DAG ecommerce_daily_pipeline failed on 2025-01-16 02:15:20 UTC

Failed Task: verificar_archivos_gcs
Error: FileNotFoundError: No se encontraron archivos para 2025-01-16

Log: https://console.cloud.google.com/composer/...
```

#### 4. Email de Reporte (Éxito)

**Subject**: 📊 Reporte Diario de Ventas - 2025-01-15

**Body** (HTML renderizado):

---

# 📊 Reporte Diario - 2025-01-15

## KPIs del Día

| Métrica | Valor |
|---------|-------|
| Total Órdenes | 8,456 |
| Ingresos Totales | $1,234,567.89 |
| Ticket Promedio | $146.00 |
| Clientes Únicos | 5,234 |
| Tasa de Cancelación | 2.34% |

*Generado automáticamente por Cloud Composer*

---

### Cálculo de Costos

**Cloud Composer pricing**:
- **Entorno pequeño**: ~$300/mes (includes Airflow, workers, database)
- **Entorno mediano**: ~$500/mes
- **Entorno grande**: ~$800/mes

**Para este DAG**:
- Ejecuta 1x/día × 30 días = 30 ejecuciones/mes
- Duración: 4 minutos/ejecución
- Total: 120 minutos/mes

**Configuración recomendada**: Entorno pequeño

**Costo mensual**: **$300** (fijo, independiente de ejecuciones)

**Desglose**:
- Cloud Composer: $300
- Dataflow: ~$9 (30 ejecuciones × $0.30)
- BigQuery: ~$0.50 (storage + queries)
- Pub/Sub: ~$0 (volumen bajo)

**Total mensual**: **~$310**

**Alternativas más baratas**:
- **Cloud Functions + Cloud Scheduler**: ~$10/mes (pero menos features)
- **Cloud Run + Cloud Scheduler**: ~$15/mes (pero menos features)

### Decisiones de Negocio

1. ✅ **Ingresos de $1.2M/día**: Performance excelente
2. ✅ **Tasa de cancelación 2.34%**: Dentro del objetivo (<5%)
3. ⚠️ **Ticket promedio $146**: Objetivo es $150, considerar upselling
4. ✅ **Automatización completa**: Equipo de BI recibe reporte todos los días sin intervención manual
5. ✅ **Retry automático**: Resiliencia ante fallos temporales

---

## 🎯 Resumen de Ejemplos

| Ejemplo | Servicio Principal | Complejidad | Concepto Clave |
|---------|-------------------|-------------|----------------|
| 1 | Cloud Storage | ⭐ | Lifecycle policies, particionamiento |
| 2 | BigQuery | ⭐⭐ | Tablas particionadas, SQL analítico |
| 3 | Dataflow | ⭐⭐⭐ | Apache Beam, ETL batch |
| 4 | Pub/Sub | ⭐⭐⭐ | Mensajería, streaming, IoT |
| 5 | Cloud Composer | ⭐⭐⭐⭐ | Orquestación, DAGs, dependencies |

---

## 🚀 Siguiente Paso

Ahora que has visto cómo funcionan los servicios en ejemplos reales, es momento de practicar por tu cuenta.

**👉 Continúa con**: `03-EJERCICIOS.md`

---

*Última actualización: 2025-01-15*
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
