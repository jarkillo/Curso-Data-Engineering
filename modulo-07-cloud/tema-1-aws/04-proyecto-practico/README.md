# Pipeline ETL Serverless en AWS

## 📋 Descripción del Proyecto

Este proyecto implementa un **pipeline ETL completamente serverless** en AWS, diseñado para demostrar las mejores prácticas de Data Engineering en la nube.

**Empresa ficticia:** CloudAPI Systems necesita procesar logs de API requests para análisis de performance.

## 🎯 Objetivos del Proyecto

Al completar este proyecto, habrás implementado:

1. **Ingesta de datos** a S3 desde múltiples fuentes
2. **Validación automática** con Lambda triggers
3. **Transformación ETL** con AWS Glue
4. **Análisis SQL** con Amazon Athena
5. **Seguridad** con IAM policies

## 🏗️ Arquitectura del Pipeline

```
┌─────────────┐
│   Sources   │ (API Logs, CSV, JSON)
└──────┬──────┘
       │
       v
┌─────────────┐
│  S3 Bucket  │ (s3://cloudapi-logs-raw/)
│   (Raw)     │
└──────┬──────┘
       │ (trigger)
       v
┌─────────────┐
│   Lambda    │ (Validation Function)
│  Validator  │ - Check schema
└──────┬──────┘ - Validate data types
       │        - Log errors
       v
┌─────────────┐
│  AWS Glue   │ (ETL Job)
│   ETL Job   │ - Clean nulls
└──────┬──────┘ - Aggregate metrics
       │        - Convert to Parquet
       v
┌─────────────┐
│  S3 Bucket  │ (s3://cloudapi-logs-processed/)
│ (Processed) │ Partitioned by date
└──────┬──────┘
       │
       v
┌─────────────┐
│   Athena    │ (SQL Analytics)
│  Database   │ - Query performance
└─────────────┘ - Generate reports
```

## 📦 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── s3_operations.py      # Operaciones con S3
│   ├── lambda_handler.py     # Lambda functions
│   ├── glue_transformations.py # Glue ETL logic
│   ├── athena_queries.py     # Athena SQL queries
│   ├── iam_utils.py          # IAM validations
│   ├── validation.py         # Data validators
│   └── config.py             # Configuration
│
├── tests/
│   ├── test_s3_operations.py
│   ├── test_lambda_handler.py
│   ├── test_glue_transformations.py
│   ├── test_athena_queries.py
│   ├── test_iam_utils.py
│   └── test_validation.py
│
├── examples/
│   ├── 01_subir_datos_s3.py
│   ├── 02_ejecutar_validacion.py
│   ├── 03_ejecutar_glue_job.py
│   └── 04_consultar_athena.py
│
├── data/
│   ├── raw/                  # Datos de entrada (CSV, JSON)
│   └── processed/            # Datos transformados (Parquet)
│
├── README.md
├── requirements.txt
└── .env.example              # Template de variables de entorno
```

## 🔧 Conceptos Clave Implementados

### 1. S3 Operations (s3_operations.py)
Funciones para interactuar con Amazon S3:
- `subir_archivo_a_s3()`: Sube archivos al bucket
- `listar_objetos_s3()`: Lista contenido de un bucket
- `descargar_archivo_s3()`: Descarga archivos localmente
- `generar_url_prefirmada()`: Genera URLs temporales

### 2. Lambda Handler (lambda_handler.py)
Función serverless que valida datos al llegar a S3:
- `lambda_handler()`: Entry point de Lambda
- `validar_schema_csv()`: Valida estructura CSV
- `validar_schema_json()`: Valida estructura JSON
- `enviar_alerta()`: Notifica errores

### 3. Glue Transformations (glue_transformations.py)
Transformaciones ETL:
- `limpiar_nulls()`: Elimina valores nulos
- `calcular_metricas_por_endpoint()`: Agrega por endpoint
- `convertir_a_parquet()`: Convierte CSV/JSON a Parquet
- `particionar_por_fecha()`: Crea particiones temporales

### 4. Athena Queries (athena_queries.py)
Consultas SQL analíticas:
- `ejecutar_query_athena()`: Ejecuta query SQL
- `obtener_resultados()`: Recupera resultados
- `crear_vista_metricas()`: Crea vistas SQL
- `calcular_percentiles()`: Calcula p50, p95, p99

### 5. IAM Utils (iam_utils.py)
Utilidades de seguridad:
- `validar_permisos_s3()`: Verifica acceso a buckets
- `generar_policy_lambda()`: Genera IAM policy para Lambda
- `validar_rol_glue()`: Verifica permisos de Glue

### 6. Validation (validation.py)
Validadores de datos:
- `validar_log_api()`: Valida formato de log
- `validar_timestamp()`: Valida formato ISO 8601
- `validar_status_code()`: Valida HTTP status codes
- `validar_response_time()`: Valida tiempo de respuesta

## 🚀 Instalación

### Prerrequisitos

1. **Cuenta AWS** con Free Tier activado
2. **AWS CLI** configurado:
   ```bash
   aws configure
   # AWS Access Key ID: [tu_access_key]
   # AWS Secret Access Key: [tu_secret_key]
   # Default region: us-east-1
   # Default output format: json
   ```
3. **Python 3.9+**
4. **boto3** (AWS SDK para Python)

### Setup

1. Clonar el repositorio:
   ```bash
   cd modulo-07-cloud/tema-1-aws/04-proyecto-practico/
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tus valores
   ```

5. Crear buckets S3 (desde AWS CLI):
   ```bash
   aws s3 mb s3://cloudapi-logs-raw --region us-east-1
   aws s3 mb s3://cloudapi-logs-processed --region us-east-1
   ```

## ▶️ Cómo Ejecutar

### 1. Subir Datos a S3

```bash
python examples/01_subir_datos_s3.py
```

Esto sube los archivos de `data/raw/` al bucket `s3://cloudapi-logs-raw/`.

### 2. Ejecutar Validación Local (sin Lambda)

```bash
python examples/02_ejecutar_validacion.py
```

Valida los datos localmente antes de desplegar Lambda.

### 3. Ejecutar Transformación Glue (local)

```bash
python examples/03_ejecutar_glue_job.py
```

Ejecuta las transformaciones ETL localmente (simula Glue).

### 4. Consultar con Athena (simulado)

```bash
python examples/04_consultar_athena.py
```

Genera queries SQL que se ejecutarían en Athena.

## 🧪 Ejecutar Tests

### Ejecutar todos los tests:
```bash
pytest tests/ -v
```

### Con cobertura:
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### Ver reporte de cobertura:
```bash
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

**Objetivo de cobertura:** >80%

## 📊 Dataset de Ejemplo

El proyecto incluye logs de API de CloudAPI Systems:

**Estructura del log:**
```json
{
  "timestamp": "2025-01-15T10:30:45Z",
  "endpoint": "/api/users",
  "method": "GET",
  "status_code": 200,
  "response_time_ms": 145,
  "user_id": "user_12345",
  "ip_address": "192.168.1.100"
}
```

**Métricas calculadas:**
- Promedio de response_time por endpoint
- Percentiles p50, p95, p99
- Tasa de errores (status_code >= 400)
- Requests por minuto

## 🔐 Seguridad y Mejores Prácticas

### ⚠️ NO Hacer
- ❌ **NO** commits credenciales AWS (Access Key, Secret Key)
- ❌ **NO** guardes contraseñas en código
- ❌ **NO** uses `root` user para operaciones diarias

### ✅ SÍ Hacer
- ✅ **SÍ** usa variables de entorno (`.env`)
- ✅ **SÍ** usa IAM roles con least privilege
- ✅ **SÍ** encripta datos sensibles en S3
- ✅ **SÍ** habilita versionado de buckets
- ✅ **SÍ** usa `.gitignore` para `.env`

### IAM Policy Mínima

Para ejecutar este proyecto, necesitas permisos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::cloudapi-logs-raw/*",
        "arn:aws:s3:::cloudapi-logs-processed/*"
      ]
    }
  ]
}
```

## 💰 Costos Estimados (Free Tier)

Con **Free Tier de AWS** (primeros 12 meses):

| Servicio | Uso Mensual | Costo Free Tier | Costo Real |
|----------|-------------|-----------------|------------|
| S3       | 1 GB storage | 5 GB gratis    | $0.00      |
| Lambda   | 100 ejecuciones | 1M gratis   | $0.00      |
| Glue     | 10 jobs     | 1M objects     | $0.00      |
| Athena   | 100 MB scanned | 5 TB gratis (30 días) | $0.00 |
| **TOTAL** |            |                | **$0.00**  |

**⚠️ Importante:** Si superas el Free Tier, los costos son:
- S3: $0.023/GB/mes
- Lambda: $0.20 por 1M requests
- Athena: $5 por TB escaneado

**Tip:** Elimina recursos con `terraform destroy` al terminar de practicar.

## 📚 Funciones Implementadas

### s3_operations.py

#### `subir_archivo_a_s3(ruta_local: str, bucket: str, key: str) -> dict`
Sube un archivo local a S3.

**Argumentos:**
- `ruta_local`: Ruta del archivo local
- `bucket`: Nombre del bucket S3
- `key`: Ruta del objeto en S3

**Retorna:** Metadata del objeto subido

**Ejemplo:**
```python
resultado = subir_archivo_a_s3(
    ruta_local="data/raw/logs.csv",
    bucket="cloudapi-logs-raw",
    key="2025/01/15/logs.csv"
)
# {'bucket': 'cloudapi-logs-raw', 'key': '2025/01/15/logs.csv', 'size': 1024}
```

#### `descargar_archivo_s3(bucket: str, key: str, ruta_destino: str) -> bool`
Descarga un archivo desde S3.

**Argumentos:**
- `bucket`: Nombre del bucket S3
- `key`: Ruta del objeto en S3
- `ruta_destino`: Ruta local de destino

**Retorna:** `True` si descarga exitosa, `False` si hay error

#### `listar_objetos_s3(bucket: str, prefijo: str = "") -> list[dict]`
Lista objetos en un bucket S3.

**Argumentos:**
- `bucket`: Nombre del bucket
- `prefijo`: Filtro de prefijo (opcional)

**Retorna:** Lista de diccionarios con metadata de objetos

---

### lambda_handler.py

#### `lambda_handler(event: dict, context: dict) -> dict`
Entry point de AWS Lambda para validar archivos S3.

**Argumentos:**
- `event`: Evento de S3 con bucket y key
- `context`: Contexto de Lambda (runtime)

**Retorna:** Response con status y mensaje

**Ejemplo:**
```python
event = {
    'Records': [{
        's3': {
            'bucket': {'name': 'cloudapi-logs-raw'},
            'object': {'key': 'logs.csv'}
        }
    }]
}
resultado = lambda_handler(event, {})
# {'statusCode': 200, 'body': 'Validation successful'}
```

---

### glue_transformations.py

#### `limpiar_nulls(datos: list[dict]) -> list[dict]`
Elimina filas con valores nulos.

**Argumentos:**
- `datos`: Lista de diccionarios (registros)

**Retorna:** Datos sin nulls

#### `calcular_metricas_por_endpoint(logs: list[dict]) -> dict[str, dict]`
Agrega métricas por endpoint.

**Argumentos:**
- `logs`: Lista de logs de API

**Retorna:** Diccionario con métricas por endpoint

**Ejemplo:**
```python
logs = [
    {'endpoint': '/api/users', 'response_time_ms': 100, 'status_code': 200},
    {'endpoint': '/api/users', 'response_time_ms': 150, 'status_code': 200},
]
resultado = calcular_metricas_por_endpoint(logs)
# {
#   '/api/users': {
#     'avg_response_time': 125.0,
#     'total_requests': 2,
#     'error_rate': 0.0
#   }
# }
```

---

### athena_queries.py

#### `generar_query_metricas(tabla: str, fecha_inicio: str, fecha_fin: str) -> str`
Genera query SQL para Athena.

**Argumentos:**
- `tabla`: Nombre de la tabla en Athena
- `fecha_inicio`: Fecha inicial (YYYY-MM-DD)
- `fecha_fin`: Fecha final (YYYY-MM-DD)

**Retorna:** Query SQL como string

---

### validation.py

#### `validar_log_api(log: dict) -> tuple[bool, str]`
Valida que un log tenga el formato correcto.

**Argumentos:**
- `log`: Diccionario con campos del log

**Retorna:** Tupla (es_valido, mensaje_error)

**Ejemplo:**
```python
log = {
    'timestamp': '2025-01-15T10:30:45Z',
    'endpoint': '/api/users',
    'status_code': 200
}
valido, error = validar_log_api(log)
# (True, '')
```

## 🎓 Conceptos de Data Engineering Aplicados

1. **Separation of Concerns**: Cada módulo tiene una responsabilidad única
2. **Idempotencia**: Las funciones pueden ejecutarse múltiples veces sin efectos duplicados
3. **Testability**: Todas las funciones son puras y fáciles de testear
4. **Type Safety**: Type hints en todas las funciones
5. **Error Handling**: Manejo explícito de errores con excepciones específicas
6. **Logging**: Trazabilidad de operaciones
7. **Serverless Architecture**: Sin gestión de servidores
8. **Cost Optimization**: Uso de Free Tier y servicios managed

## 🚀 Despliegue a AWS (Opcional)

Para desplegar el pipeline completo a AWS:

1. Crear función Lambda:
   ```bash
   aws lambda create-function \
     --function-name ValidarLogsAPI \
     --runtime python3.9 \
     --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
     --handler lambda_handler.lambda_handler \
     --zip-file fileb://lambda_function.zip
   ```

2. Configurar trigger S3 → Lambda:
   ```bash
   aws s3api put-bucket-notification-configuration \
     --bucket cloudapi-logs-raw \
     --notification-configuration file://s3-trigger-config.json
   ```

3. Crear Glue Job (desde consola AWS o CLI)

4. Configurar Glue Crawler para Athena

**Nota:** El despliegue completo se cubre en el **Tema 3: Infraestructura como Código (IaC)** con Terraform.

## 📖 Recursos Adicionales

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 🤝 Contribuciones

Este proyecto es parte del **Master en Ingeniería de Datos con IA**.

Para reportar errores o sugerencias, abre un issue en el repositorio.

## 📝 Licencia

MIT License - Proyecto educativo

---

**¡Éxito con tu pipeline serverless en AWS!** 🚀

**Siguiente paso:** Completa el Tema 2 (GCP) y Tema 3 (IaC) para dominar Cloud Data Engineering.

---

*Última actualización: 2025-11-09*
*Módulo 7 - Tema 1: AWS para Data Engineering*
