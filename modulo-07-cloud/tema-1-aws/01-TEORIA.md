# AWS para Data Engineering - Teoría

## Introducción: ¿Por qué AWS en Data Engineering?

### El Problema del Servidor Físico

Imagina que tienes una tienda online y necesitas guardar fotos de productos, procesar pedidos y generar reportes de ventas. Tradicionalmente, comprarías servidores físicos (computadoras potentes) que estarían en tu oficina 24/7.

**Problemas de esta aproach:**
- 💰 **Costo inicial alto**: Un servidor cuesta 3000-10000€
- 🔧 **Mantenimiento**: Necesitas personal técnico
- ⚡ **Electricidad**: Servidores consumen mucha energía
- 📈 **Escalabilidad**: Si creces, necesitas comprar más servidores
- 🔥 **Riesgo**: Si se rompe o hay un incendio, pierdes todo

### La Solución: La Nube (Cloud Computing)

**Cloud computing** es como alquilar apartamentos en lugar de comprar casa:
- Pagas solo por lo que usas (pay-as-you-go)
- No te preocupas del mantenimiento (lo hace el proveedor)
- Puedes crecer o reducir fácilmente
- Tus datos están replicados (no se pierden)

**AWS (Amazon Web Services)** es el proveedor de cloud más grande del mundo. Es la misma infraestructura que usa Amazon.com para vender millones de productos.

### ¿Por qué AWS para Data Engineering?

En Data Engineering, manejamos **grandes volúmenes de datos**:
- Millones de eventos por segundo
- Petabytes de almacenamiento
- Procesamiento intensivo

AWS nos da herramientas **serverless** (sin servidor): tú solo escribes código Python, y AWS se encarga de ejecutarlo, escalarlo y mantenerlo.

---

## Concepto 1: Amazon S3 (Simple Storage Service)

### ¿Qué es S3?

**S3** es el servicio de almacenamiento de archivos de AWS. Piensa en S3 como **Google Drive o Dropbox para empresas**.

**Analogía:** S3 es como un almacén gigante de cajas:
- Cada **bucket** (cubo) es un almacén completo
- Cada **object** (archivo) es una caja dentro del almacén
- Puedes guardar cualquier tipo de archivo: CSV, JSON, Parquet, imágenes, videos
- No hay límite de espacio (puedes guardar petabytes)

### Características Clave de S3

#### 1. Durabilidad: 99.999999999% (11 nueves)

AWS promete que **no perderás tus archivos**. Replican automáticamente tus datos en múltiples data centers.

**Analogía:** Es como si hicieras 3 copias de tu archivo y las guardaras en 3 ciudades diferentes. Si una ciudad tiene un terremoto, tus datos siguen seguros en las otras dos.

#### 2. Storage Classes (Clases de Almacenamiento)

No todos los datos se acceden igual:
- Datos "hot" (calientes): Se leen frecuentemente → **S3 Standard**
- Datos "warm": Se leen ocasionalmente → **S3 Infrequent Access**
- Datos "cold" (fríos): Casi nunca se leen → **S3 Glacier** (muy barato)

**Analogía:**
- **S3 Standard** = Ropa en tu armario (acceso inmediato)
- **S3 IA** = Ropa en el trastero (tardas 5 min en sacarla)
- **S3 Glacier** = Ropa guardada en el sótano de tus padres (tardas 12h en recuperarla)

#### 3. Versionado de Archivos

Puedes activar **versioning** para guardar todas las versiones de un archivo.

**Analogía:** Como Google Docs que guarda el historial de cambios. Si subes `ventas.csv` hoy y mañana, S3 guarda ambas versiones.

#### 4. Lifecycle Policies (Políticas de Ciclo de Vida)

Puedes automatizar qué hacer con archivos antiguos:

**Ejemplo real:**
```
Regla: "Logs de más de 30 días" → Mover a Glacier
Regla: "Logs de más de 1 año" → Eliminar permanentemente
```

Esto **ahorra mucho dinero** porque Glacier cuesta 20x menos que S3 Standard.

### S3 en Data Engineering

**Casos de uso principales:**

1. **Data Lake**: Guarda datos raw (en bruto) antes de procesarlos
   - Logs de aplicaciones (JSON)
   - Archivos CSV de ventas
   - Datos de sensores IOT

2. **Data Warehouse**: Guarda datos procesados (Parquet, ORC)
   - Tablas limpias y transformadas
   - Datos agregados para analytics

3. **Backup**: Copia de seguridad de bases de datos

**Ventaja clave:** S3 es **escalable infinitamente**. Si hoy guardas 1GB y mañana 1PB, no necesitas cambiar nada.

### Estructura de S3

```
S3 Bucket: mi-data-lake-produccion
│
├── raw/                          (Datos sin procesar)
│   ├── ventas/
│   │   ├── 2025-01-01.csv
│   │   └── 2025-01-02.csv
│   └── logs/
│       └── app-2025-01-01.json
│
├── processed/                    (Datos procesados)
│   └── ventas_agregadas/
│       └── ventas_por_mes.parquet
│
└── models/                       (Modelos de ML)
    └── modelo_prediccion.pkl
```

### Costos de S3

**Precios aproximados (región us-east-1):**
- S3 Standard: 0.023 $/GB/mes
- S3 IA: 0.0125 $/GB/mes
- S3 Glacier: 0.004 $/GB/mes

**Ejemplo real:**
- 100GB en S3 Standard = 2.30 $/mes
- 100GB en Glacier = 0.40 $/mes

**Free Tier (primer año gratis):**
- 5GB de almacenamiento S3 Standard
- 20,000 GET requests
- 2,000 PUT requests

---

## Concepto 2: AWS Lambda (Funciones Serverless)

### ¿Qué es Lambda?

**Lambda** te permite ejecutar código Python sin gestionar servidores.

**Analogía:** Lambda es como un restaurante de delivery:
- Tú escribes la receta (código Python)
- AWS cocina el plato cuando alguien pide (trigger)
- Pagas solo por los platos servidos (ejecuciones)
- No te preocupas de la cocina, estufa, lavaplatos (infraestructura)

### Cómo Funciona Lambda

1. Tú subes tu **código Python** (o Node.js, Java, Go...)
2. Defines un **trigger** (evento que ejecuta la función):
   - Nuevo archivo en S3
   - Mensaje en una cola (SQS)
   - Request HTTP (API Gateway)
   - Cron schedule (cada hora, cada día...)

3. Lambda **ejecuta tu código automáticamente**
4. Pagas **solo por el tiempo de ejecución** (milisegundos)

### Ejemplo Real: Validar CSV al Subir a S3

**Escenario:**
Cada vez que alguien sube un archivo CSV a S3, queremos validar que:
- Tiene las columnas correctas
- No tiene filas vacías
- Los tipos de datos son correctos

**Solución con Lambda:**

```python
# lambda_function.py

import boto3
import csv
from io import StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Función Lambda que valida CSV al subir a S3.

    Event contiene información del archivo subido:
    - bucket name
    - file key (path)
    """

    # Obtener información del evento
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Descargar archivo desde S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    # Validar CSV
    reader = csv.DictReader(StringIO(content))
    rows = list(reader)

    # Validación 1: Columnas requeridas
    required_columns = ['fecha', 'producto', 'cantidad', 'precio']
    if not all(col in reader.fieldnames for col in required_columns):
        raise ValueError(f"Faltan columnas requeridas")

    # Validación 2: No hay filas vacías
    if len(rows) == 0:
        raise ValueError("El archivo está vacío")

    # Validación 3: Tipos de datos correctos
    for row in rows:
        try:
            float(row['cantidad'])
            float(row['precio'])
        except ValueError:
            raise ValueError(f"Tipo de dato incorrecto en fila {row}")

    print(f"✅ Archivo {key} validado correctamente")
    return {
        'statusCode': 200,
        'body': f'Validado {len(rows)} filas'
    }
```

**¿Qué pasa cuando subes un CSV a S3?**
1. S3 detecta nuevo archivo → trigger
2. Lambda ejecuta `lambda_handler()`
3. Descarga archivo, valida
4. Si pasa → OK
5. Si falla → Error (puedes enviar email, Slack notification...)

### Ventajas de Lambda

✅ **No gestionas servidores**: AWS se encarga de TODO
✅ **Auto-scaling**: Si llegan 1 o 1,000 archivos, Lambda escala automáticamente
✅ **Pay-per-use**: Pagas solo los milisegundos que ejecuta
✅ **Integración fácil**: Se conecta con S3, Glue, Athena, DynamoDB...

### Límites de Lambda

⚠️ **Timeout máximo**: 15 minutos
- Para jobs largos, usa AWS Glue o Batch

⚠️ **Memoria máxima**: 10GB
- Para procesamiento intensivo, usa EC2 o Fargate

⚠️ **Tamaño del deployment package**: 50MB (comprimido)
- Si tu código + dependencias pesan más, usa Lambda Layers o Docker

### Costos de Lambda

**Precios:**
- Primeros 1M requests/mes: **GRATIS**
- Después: 0.20 $ por 1M requests
- Compute: 0.0000166667 $/GB-segundo

**Ejemplo real:**
- 1M ejecuciones de 512MB que tardan 1 segundo cada una
- Costo: (1M * 1 segundo * 0.5GB * 0.0000166667) + (1M requests * 0.20/1M)
- = 8.33 $ + 0.20 $ = **8.53 $/mes**

**Free Tier (permanente):**
- 1M requests gratis/mes
- 400,000 GB-segundos de compute gratis/mes

---

## Concepto 3: AWS Glue (Servicio ETL Managed)

### ¿Qué es AWS Glue?

**AWS Glue** es un servicio **ETL (Extract, Transform, Load) completamente gestionado**.

**Analogía:** Glue es como un robot de cocina industrial:
- Le das ingredientes (datos raw en S3)
- Le dices qué receta seguir (script PySpark)
- Él cocina el plato (transforma los datos)
- Sirve el resultado (datos procesados en S3)

Tú NO gestionas servidores, Glue lo hace por ti.

### Componentes de AWS Glue

#### 1. Glue Data Catalog

Es un **metastore** (base de datos de metadatos) que guarda información sobre tus tablas.

**Analogía:** El catálogo de una biblioteca:
- No guarda los libros (datos), solo metadatos (título, autor, ubicación)
- Tú defines schemas de tus tablas
- Athena, Glue, Redshift lo usan para saber qué tablas existen

**Ejemplo:**
```
Tabla: ventas_2025
Schema:
  - fecha: date
  - producto: string
  - cantidad: int
  - precio: decimal
Ubicación: s3://mi-bucket/processed/ventas/
Formato: Parquet
```

#### 2. Glue Crawlers

Un **crawler** es un robot que escanea tus datos en S3 y **infiere el schema automáticamente**.

**Analogía:** Como un bibliotecario que revisa libros nuevos, lee su título y autor, y actualiza el catálogo.

**Proceso:**
1. Le dices al crawler: "Escanea s3://mi-bucket/raw/ventas/"
2. El crawler lee los archivos (CSV, JSON, Parquet...)
3. Infiere el schema (columnas, tipos de datos)
4. Crea/actualiza la tabla en el Data Catalog

Esto te ahorra escribir el schema manualmente.

#### 3. Glue ETL Jobs

Un **Glue Job** es un script PySpark que transforma datos.

**Tipos de Jobs:**
- **Python Shell**: Scripts Python simples (pandas)
- **Spark**: Para procesar millones/billones de filas
- **Spark Streaming**: Para datos en tiempo real

**Ejemplo real: Limpiar datos de ventas**

```python
# glue_job.py (PySpark)

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Inicializar Glue Context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. Leer datos raw desde S3
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="mi_database",
    table_name="ventas_raw"
)

# 2. Transformar datos
# Filtrar filas con cantidad > 0
filtered = Filter.apply(
    frame=datasource,
    f=lambda x: x["cantidad"] > 0
)

# Eliminar duplicados
deduplicated = filtered.toDF().dropDuplicates(['fecha', 'producto'])

# Agregar columna calculada: total = cantidad * precio
from pyspark.sql.functions import col
transformed = deduplicated.withColumn(
    "total",
    col("cantidad") * col("precio")
)

# 3. Guardar datos procesados en S3 (formato Parquet)
transformed.write\
    .mode("overwrite")\
    .partitionBy("fecha")\
    .parquet("s3://mi-bucket/processed/ventas/")

job.commit()
```

**¿Qué hace este job?**
1. Lee CSV de S3 (tabla `ventas_raw` en el Catalog)
2. Filtra filas inválidas (cantidad ≤ 0)
3. Elimina duplicados
4. Calcula columna "total"
5. Guarda en Parquet particionado por fecha

**Ventaja:** Glue escala automáticamente. Si tienes 1GB o 1TB, Glue asigna los recursos necesarios.

### Glue Workflows

Puedes encadenar múltiples jobs:

```
Crawler → Job 1 (limpiar) → Job 2 (agregar) → Job 3 (cargar a Redshift)
```

### Costos de Glue

**Precios:**
- **DPU (Data Processing Unit)**: 0.44 $/hora
- **Crawler**: 0.44 $/hora (facturado por segundo, mínimo 10 min)

**Ejemplo:**
- Glue Job con 5 DPUs que tarda 30 minutos
- Costo: 5 DPUs * 0.5 horas * 0.44 $/DPU-hora = **1.10 $**

**Free Tier (primeros 30 días):**
- 1M objects catalogados gratis
- Después: 1 $/100,000 objects/mes

---

## Concepto 4: Amazon Athena (Query Engine SQL)

### ¿Qué es Athena?

**Athena** es un servicio que te permite hacer queries SQL directamente sobre archivos en S3, **sin cargar los datos a una base de datos**.

**Analogía:** Athena es como buscar palabras en un libro SIN necesidad de escribirlas en un cuaderno primero. Lees directamente del libro (S3).

### Ventajas de Athena

✅ **Serverless**: No gestionas servidores
✅ **Pay-per-query**: Pagas solo por los datos escaneados
✅ **Compatible con SQL estándar**: Si sabes SQL, ya sabes Athena
✅ **Integrado con Glue Catalog**: Usa las tablas del Catalog
✅ **Formatos optimizados**: Lee Parquet, ORC, Avro (muy rápido)

### Ejemplo: Query sobre S3

Imagina que tienes ventas en S3 (formato Parquet):

```
s3://mi-bucket/processed/ventas/
├── fecha=2025-01-01/ventas.parquet
├── fecha=2025-01-02/ventas.parquet
└── fecha=2025-01-03/ventas.parquet
```

**Query en Athena:**

```sql
-- Ventas totales por producto en enero 2025

SELECT
    producto,
    SUM(cantidad) as total_unidades,
    SUM(total) as total_ingresos
FROM ventas
WHERE fecha BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY producto
ORDER BY total_ingresos DESC
LIMIT 10;
```

**¿Qué pasa?**
1. Athena lee los archivos Parquet desde S3
2. Ejecuta el query (agregaciones, filtros...)
3. Retorna resultados en segundos

**No necesitas:**
- Cargar datos a Redshift o MySQL
- Crear índices
- Gestionar un servidor de base de datos

### Particionamiento para Optimizar Costos

Athena cobra por **datos escaneados**. Particionamiento reduce los datos leídos.

**Sin particiones:**
```sql
SELECT * FROM ventas WHERE fecha = '2025-01-15';
```
→ Escanea TODO el bucket (1TB) → 5 $

**Con particiones:**
```sql
SELECT * FROM ventas WHERE fecha = '2025-01-15';
```
→ Escanea SOLO `fecha=2025-01-15/` (100MB) → 0.005 $

**1000x más barato!**

### Formatos: CSV vs Parquet

| Formato  | Tamaño | Velocidad | Costo Query |
|----------|--------|-----------|-------------|
| CSV      | 1GB    | Lento     | 0.005 $/query |
| Parquet  | 200MB  | Rápido    | 0.001 $/query |

**Conclusión:** Siempre usa Parquet o ORC para datos de analytics.

### Costos de Athena

**Precios:**
- 5 $/TB de datos escaneados
- Primer 1TB/mes en Free Tier

**Ejemplo:**
- Query que escanea 100GB → 0.50 $
- Query que escanea 10GB (Parquet comprimido) → 0.05 $

---

## Concepto 5: IAM (Identity and Access Management)

### ¿Qué es IAM?

**IAM** es el servicio de seguridad y permisos de AWS.

**Analogía:** IAM es como el sistema de llaves y cerraduras de un edificio:
- **Users** = Personas con llave
- **Roles** = Tipos de llave (limpieza, residente, administrador)
- **Policies** = Qué puertas puede abrir cada llave

### Principio de Least Privilege

**Nunca des más permisos de los necesarios.**

**Ejemplo:**
- Lambda solo necesita leer S3 → Dale permiso `s3:GetObject`, NO `s3:*`

### Ejemplo de Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::mi-bucket/raw/*"
    }
  ]
}
```

**Significa:**
- Permite (`Allow`)
- Leer (`GetObject`) y escribir (`PutObject`)
- SOLO en el path `mi-bucket/raw/*`

---

## Aplicaciones Prácticas en Data Engineering

### Pipeline Completo

**Escenario real:**
Una startup de ecommerce necesita analizar ventas en tiempo real.

**Arquitectura:**

```
┌───────────────┐
│   API Ventas  │ (genera eventos JSON)
└───────┬───────┘
        │
        v
┌───────────────┐
│  S3 Raw Data  │ (s3://ventas/raw/)
└───────┬───────┘
        │ (trigger cada 1h)
        v
┌───────────────┐
│  Lambda       │ (valida JSON)
└───────┬───────┘
        │
        v
┌───────────────┐
│  Glue Job     │ (limpia, agrega)
└───────┬───────┘
        │
        v
┌───────────────┐
│S3 Processed   │ (s3://ventas/processed/ - Parquet)
└───────┬───────┘
        │
        v
┌───────────────┐
│   Athena      │ (queries SQL para BI)
└───────────────┘
```

**Beneficios:**
- ✅ **Serverless**: No servidores que mantener
- ✅ **Escalable**: Maneja 1 o 1M eventos/segundo
- ✅ **Cost-effective**: Pagas solo por uso
- ✅ **Rápido**: Resultados en minutos

---

## Comparaciones

### AWS vs On-Premise

| Aspecto       | On-Premise | AWS |
|---------------|------------|-----|
| Costo inicial | 50,000€+   | 0€ (Free Tier) |
| Mantenimiento | Tu equipo  | AWS |
| Escalabilidad | Manual     | Automática |
| Backup        | Tú lo haces | AWS (replicado) |
| Actualización | Manual     | Automática |

### Lambda vs EC2

| Aspecto | Lambda | EC2 |
|---------|--------|-----|
| Gestión | Serverless | Gestionas tú |
| Pago    | Por ejecución | Por hora |
| Escalado | Automático | Manual |
| Límite tiempo | 15 min | Ilimitado |
| Uso ideal | Jobs cortos | Jobs largos, servers |

---

## Errores Comunes

### Error 1: No Usar Particiones en S3

**Problema:** Guardas todo en una carpeta plana:
```
s3://bucket/ventas.parquet (1TB)
```

**Solución:** Particiona por fecha:
```
s3://bucket/ventas/
├── year=2025/month=01/day=01/ventas.parquet
└── year=2025/month=01/day=02/ventas.parquet
```

**Beneficio:** Queries 100x más rápidas y baratas.

### Error 2: Usar CSV en Lugar de Parquet

CSV es lento y caro para analytics.

**Siempre convierte a Parquet:**
```python
df = pd.read_csv("ventas.csv")
df.to_parquet("ventas.parquet", compression="snappy")
```

**Reducción típica:** 80-90% de tamaño.

### Error 3: No Configurar Billing Alerts

**Configura alarmas desde día 1:**
- Alert a 0.50€
- Alert a 1€
- Alert a 5€

**Cómo:** AWS Billing Dashboard → Budgets → Create Budget

---

## Checklist de Aprendizaje

- [ ] Entiendo qué es cloud computing y por qué es útil
- [ ] Puedo explicar S3 con mis propias palabras
- [ ] Sé qué son buckets, objects y storage classes
- [ ] Entiendo cómo funciona Lambda (trigger + código)
- [ ] Sé qué es serverless y sus ventajas
- [ ] Puedo explicar los componentes de Glue (Catalog, Crawlers, Jobs)
- [ ] Entiendo la diferencia entre CSV y Parquet
- [ ] Sé cómo Athena hace queries sobre S3
- [ ] Entiendo el concepto de particionamiento
- [ ] Conozco las mejores prácticas de IAM

---

## Recursos Adicionales

### Documentación Oficial
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)

### Cursos Gratuitos
- AWS Free Training: https://aws.amazon.com/training/
- AWS Skill Builder (Learning Paths)

### Herramientas
- AWS CLI: https://aws.amazon.com/cli/
- boto3 (Python SDK): https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- AWS SAM (Serverless Application Model)

---

**Siguiente paso:** [02-EJEMPLOS.md](./02-EJEMPLOS.md) - Ejemplos trabajados de pipelines AWS

**Última actualización:** 2025-11-09
