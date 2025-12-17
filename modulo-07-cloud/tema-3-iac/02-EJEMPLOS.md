# 📘 Ejemplos: Infrastructure as Code (Terraform y CloudFormation)

En este documento trabajaremos **5 ejemplos completos** de Infrastructure as Code, desde casos básicos hasta arquitecturas completas de Data Engineering.

---

## 📋 Índice de Ejemplos

1. **⭐ Ejemplo 1**: Data Lake Básico con Terraform (S3 + Lifecycle)
2. **⭐⭐ Ejemplo 2**: Pipeline ETL Serverless con CloudFormation (Lambda + S3)
3. **⭐⭐⭐ Ejemplo 3**: Data Warehouse en GCP con Terraform (BigQuery + Cloud Storage)
4. **⭐⭐⭐⭐ Ejemplo 4**: Pipeline Completo Multi-Cloud con Terraform (AWS + GCP)
5. **⭐⭐⭐⭐ Ejemplo 5**: CI/CD para Data Pipelines con Terraform Modules

---

## ⭐ Ejemplo 1: Data Lake Básico con Terraform

### 📝 Contexto Empresarial

**Empresa**: RetailVision Analytics
**Necesidad**: Crear un data lake en AWS S3 para almacenar datos de ventas con políticas de lifecycle automáticas para optimizar costos.

### 🎯 Objetivo

Desplegar infraestructura que incluya:
- 3 buckets S3 (raw, processed, analytics)
- Políticas de lifecycle para archivar datos antiguos
- Versionado habilitado para datos críticos
- Tags para governance y billing

### 💻 Código Terraform

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region para desplegar recursos"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "retailvision-datalake"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Bucket RAW - Datos sin procesar
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-${var.environment}"

  tags = {
    Name        = "Raw Data Bucket"
    Environment = var.environment
    Layer       = "raw"
    ManagedBy   = "Terraform"
    CostCenter  = "DataEngineering"
  }
}

# Versionado para bucket RAW (datos críticos)
resource "aws_s3_bucket_versioning" "raw_data_versioning" {
  bucket = aws_s3_bucket.raw_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle policy para RAW: mover a Glacier después de 90 días
resource "aws_s3_bucket_lifecycle_configuration" "raw_data_lifecycle" {
  bucket = aws_s3_bucket.raw_data.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    # Mover a Glacier Deep Archive después de 90 días
    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    # Eliminar después de 7 años (compliance)
    expiration {
      days = 2555  # ~7 años
    }

    # Limpiar versiones antiguas
    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}

# Bucket PROCESSED - Datos procesados
resource "aws_s3_bucket" "processed_data" {
  bucket = "${var.project_name}-processed-${var.environment}"

  tags = {
    Name        = "Processed Data Bucket"
    Environment = var.environment
    Layer       = "processed"
    ManagedBy   = "Terraform"
    CostCenter  = "DataEngineering"
  }
}

# Lifecycle para PROCESSED: mover a IA después de 30 días
resource "aws_s3_bucket_lifecycle_configuration" "processed_data_lifecycle" {
  bucket = aws_s3_bucket.processed_data.id

  rule {
    id     = "optimize-storage"
    status = "Enabled"

    # Mover a Infrequent Access después de 30 días
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    # Mover a Glacier después de 90 días
    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    # Eliminar después de 2 años
    expiration {
      days = 730
    }
  }
}

# Bucket ANALYTICS - Resultados de análisis
resource "aws_s3_bucket" "analytics_data" {
  bucket = "${var.project_name}-analytics-${var.environment}"

  tags = {
    Name        = "Analytics Data Bucket"
    Environment = var.environment
    Layer       = "analytics"
    ManagedBy   = "Terraform"
    CostCenter  = "DataEngineering"
  }
}

# Lifecycle para ANALYTICS: eliminar después de 1 año
resource "aws_s3_bucket_lifecycle_configuration" "analytics_data_lifecycle" {
  bucket = aws_s3_bucket.analytics_data.id

  rule {
    id     = "cleanup-analytics"
    status = "Enabled"

    # Datos de analytics solo se mantienen 1 año
    expiration {
      days = 365
    }
  }
}

# Outputs
output "raw_bucket_name" {
  description = "Nombre del bucket de datos RAW"
  value       = aws_s3_bucket.raw_data.id
}

output "processed_bucket_name" {
  description = "Nombre del bucket de datos PROCESSED"
  value       = aws_s3_bucket.processed_data.id
}

output "analytics_bucket_name" {
  description = "Nombre del bucket de datos ANALYTICS"
  value       = aws_s3_bucket.analytics_data.id
}

output "raw_bucket_arn" {
  description = "ARN del bucket RAW"
  value       = aws_s3_bucket.raw_data.arn
}
```

### 🚀 Despliegue

```bash
# 1. Inicializar Terraform
terraform init

# 2. Validar sintaxis
terraform validate

# 3. Ver plan de ejecución
terraform plan

# 4. Aplicar cambios
terraform apply

# Terraform preguntará confirmación:
# Do you want to perform these actions?
#   Terraform will perform the actions described above.
#   Only 'yes' will be accepted to approve.
#
# Enter a value: yes

# 5. Ver outputs
terraform output
```

### 📊 Resultado Esperado

```
Apply complete! Resources: 9 added, 0 changed, 0 destroyed.

Outputs:

analytics_bucket_name = "retailvision-datalake-analytics-dev"
processed_bucket_name = "retailvision-datalake-processed-dev"
raw_bucket_arn = "arn:aws:s3:::retailvision-datalake-raw-dev"
raw_bucket_name = "retailvision-datalake-raw-dev"
```

### 💰 Cálculo de Costos

**Escenario**: 500 GB nuevos por mes

```
Mes 1:
- S3 Standard (500 GB): $11.50
Total: $11.50/mes

Mes 4 (con lifecycle):
- S3 Standard (500 GB nuevos): $11.50
- S3 IA (1000 GB antiguos): $12.50
Total: $24.00/mes

Mes 12 (con optimización completa):
- S3 Standard (500 GB recientes): $11.50
- S3 IA (1500 GB 1-3 meses): $18.75
- Glacier (3000 GB >3 meses): $12.00
Total: $42.25/mes

SIN lifecycle policies: $138/mes (6 TB * $0.023)
CON lifecycle policies: $42.25/mes

💰 AHORRO: 69% ($95.75/mes = $1,149/año)
```

---

## ⭐⭐ Ejemplo 2: Pipeline ETL Serverless con CloudFormation

### 📝 Contexto Empresarial

**Empresa**: LogStream Analytics
**Necesidad**: Pipeline serverless que procese logs de aplicaciones automáticamente cuando se suben a S3.

### 🎯 Objetivo

Desplegar:
- Bucket S3 para logs raw
- Función Lambda para procesar logs
- Trigger automático S3 → Lambda
- Bucket S3 para logs procesados
- CloudWatch Logs para monitoring

### 💻 Código CloudFormation

```yaml
# pipeline-etl.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Pipeline ETL Serverless para procesamiento de logs'

Parameters:
  ProjectName:
    Type: String
    Default: logstream-etl
    Description: Nombre del proyecto

  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod
    Description: Ambiente de despliegue

Resources:
  # ============================================
  # S3 BUCKETS
  # ============================================

  RawLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-raw-logs-${Environment}'
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: suffix
                    Value: .log
            Function: !GetAtt ProcessLogsFunction.Arn
      Tags:
        - Key: Name
          Value: Raw Logs Bucket
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation

  ProcessedLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-processed-logs-${Environment}'
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldLogs
            Status: Enabled
            ExpirationInDays: 90
      Tags:
        - Key: Name
          Value: Processed Logs Bucket
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation

  # ============================================
  # IAM ROLE FOR LAMBDA
  # ============================================

  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${ProjectName}-lambda-role-${Environment}'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub '${RawLogsBucket.Arn}/*'
              - Effect: Allow
                Action:
                  - s3:PutObject
                Resource: !Sub '${ProcessedLogsBucket.Arn}/*'

  # ============================================
  # LAMBDA FUNCTION
  # ============================================

  ProcessLogsFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-process-logs-${Environment}'
      Runtime: python3.11
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Timeout: 300
      MemorySize: 512
      Environment:
        Variables:
          PROCESSED_BUCKET: !Ref ProcessedLogsBucket
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime
          from urllib.parse import unquote_plus

          s3_client = boto3.client('s3')

          def lambda_handler(event, context):
              """
              Procesa archivos de log subidos a S3.

              Transformaciones:
              1. Parse de cada línea de log
              2. Filtrado de errores
              3. Agregación de métricas
              4. Guardado en bucket procesado
              """
              processed_bucket = os.environ['PROCESSED_BUCKET']

              for record in event['Records']:
                  # Obtener información del archivo
                  bucket = record['s3']['bucket']['name']
                  key = unquote_plus(record['s3']['object']['key'])

                  print(f"Procesando: s3://{bucket}/{key}")

                  try:
                      # Descargar archivo
                      response = s3_client.get_object(Bucket=bucket, Key=key)
                      log_content = response['Body'].read().decode('utf-8')

                      # Procesar logs
                      lines = log_content.strip().split('\n')
                      errors = []
                      warnings = []
                      info_count = 0

                      for line in lines:
                          if 'ERROR' in line:
                              errors.append(line)
                          elif 'WARN' in line:
                              warnings.append(line)
                          elif 'INFO' in line:
                              info_count += 1

                      # Crear resumen
                      summary = {
                          'source_file': key,
                          'processed_at': datetime.utcnow().isoformat(),
                          'total_lines': len(lines),
                          'errors': len(errors),
                          'warnings': len(warnings),
                          'info': info_count,
                          'error_lines': errors[:10],  # Primeros 10 errores
                          'warning_lines': warnings[:10]
                      }

                      # Guardar resultado
                      timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                      output_key = f"processed/{timestamp}_{os.path.basename(key)}.json"

                      s3_client.put_object(
                          Bucket=processed_bucket,
                          Key=output_key,
                          Body=json.dumps(summary, indent=2),
                          ContentType='application/json'
                      )

                      print(f"✅ Procesado exitosamente: {output_key}")
                      print(f"📊 Estadísticas: {summary['errors']} errores, {summary['warnings']} warnings")

                      return {
                          'statusCode': 200,
                          'body': json.dumps(summary)
                      }

                  except Exception as e:
                      print(f"❌ Error procesando {key}: {str(e)}")
                      raise e
      Tags:
        - Key: Name
          Value: Log Processor Function
        - Key: Environment
          Value: !Ref Environment

  # Permission para que S3 invoque Lambda
  LambdaInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ProcessLogsFunction
      Action: lambda:InvokeFunction
      Principal: s3.amazonaws.com
      SourceArn: !GetAtt RawLogsBucket.Arn

  # ============================================
  # CLOUDWATCH LOG GROUP
  # ============================================

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${ProcessLogsFunction}'
      RetentionInDays: 7

Outputs:
  RawBucketName:
    Description: Nombre del bucket de logs RAW
    Value: !Ref RawLogsBucket
    Export:
      Name: !Sub '${AWS::StackName}-RawBucket'

  ProcessedBucketName:
    Description: Nombre del bucket de logs procesados
    Value: !Ref ProcessedLogsBucket
    Export:
      Name: !Sub '${AWS::StackName}-ProcessedBucket'

  LambdaFunctionArn:
    Description: ARN de la función Lambda
    Value: !GetAtt ProcessLogsFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-LambdaArn'

  LambdaFunctionName:
    Description: Nombre de la función Lambda
    Value: !Ref ProcessLogsFunction
```

### 🚀 Despliegue

```bash
# 1. Validar template
aws cloudformation validate-template \
  --template-body file://pipeline-etl.yaml

# 2. Crear stack
aws cloudformation create-stack \
  --stack-name logstream-etl-dev \
  --template-body file://pipeline-etl.yaml \
  --parameters \
    ParameterKey=ProjectName,ParameterValue=logstream-etl \
    ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_NAMED_IAM

# 3. Esperar a que complete
aws cloudformation wait stack-create-complete \
  --stack-name logstream-etl-dev

# 4. Ver outputs
aws cloudformation describe-stacks \
  --stack-name logstream-etl-dev \
  --query 'Stacks[0].Outputs'
```

### 🧪 Probar el Pipeline

```bash
# Crear un archivo de log de prueba
cat > test.log << EOF
2025-11-09 10:00:01 INFO Application started
2025-11-09 10:00:02 INFO User login: user123
2025-11-09 10:00:05 WARN High memory usage: 85%
2025-11-09 10:00:10 ERROR Database connection failed
2025-11-09 10:00:15 ERROR Timeout waiting for response
2025-11-09 10:00:20 INFO Request processed successfully
EOF

# Subir a S3 (esto dispara Lambda automáticamente)
aws s3 cp test.log s3://logstream-etl-raw-logs-dev/logs/test.log

# Esperar unos segundos y verificar resultado
aws s3 ls s3://logstream-etl-processed-logs-dev/processed/

# Descargar resultado
aws s3 cp s3://logstream-etl-processed-logs-dev/processed/LATEST_FILE.json result.json
cat result.json
```

### 📊 Resultado Esperado

```json
{
  "source_file": "logs/test.log",
  "processed_at": "2025-11-09T10:00:25.123456",
  "total_lines": 6,
  "errors": 2,
  "warnings": 1,
  "info": 3,
  "error_lines": [
    "2025-11-09 10:00:10 ERROR Database connection failed",
    "2025-11-09 10:00:15 ERROR Timeout waiting for response"
  ],
  "warning_lines": [
    "2025-11-09 10:00:05 WARN High memory usage: 85%"
  ]
}
```

### 💰 Cálculo de Costos

**Escenario**: 10,000 archivos de log por día (300K/mes)

```
Lambda (300K invocaciones):
- Primeras 1M: Gratis (Free Tier)
- Costo: $0/mes

S3 Storage (10 GB):
- S3 Standard: $0.23/mes
- Lifecycle después de 90 días: Elimina automáticamente

CloudWatch Logs (500 MB/mes):
- Ingesta: $0.25/mes
- Storage (7 días retención): $0.02/mes

Total: ~$0.50/mes

🎉 Casi gratis gracias a Free Tier y serverless!
```

---

## ⭐⭐⭐ Ejemplo 3: Data Warehouse en GCP con Terraform

### 📝 Contexto Empresarial

**Empresa**: FinMetrics Inc.
**Necesidad**: Data warehouse en BigQuery con datos de transacciones financieras desde Cloud Storage.

### 🎯 Objetivo

Desplegar:
- Cloud Storage bucket para datos raw
- BigQuery dataset para analytics
- Tablas BigQuery particionadas y clusterizadas
- Service account con permisos mínimos
- Scheduled queries para agregaciones diarias

### 💻 Código Terraform

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Variables
variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "finmetrics-dwh"
}

variable "environment" {
  description = "Ambiente"
  type        = string
  default     = "dev"
}

# ============================================
# CLOUD STORAGE
# ============================================

resource "google_storage_bucket" "raw_data" {
  name          = "${var.gcp_project_id}-${var.project_name}-raw-${var.environment}"
  location      = var.gcp_region
  force_destroy = false

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  labels = {
    environment = var.environment
    managed_by  = "terraform"
    layer       = "raw"
  }
}

# ============================================
# BIGQUERY DATASET
# ============================================

resource "google_bigquery_dataset" "transactions" {
  dataset_id    = "transactions_${var.environment}"
  friendly_name = "Transacciones Financieras"
  description   = "Dataset para análisis de transacciones"
  location      = var.gcp_region

  default_table_expiration_ms = 31536000000  # 1 año

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}

# ============================================
# BIGQUERY TABLES
# ============================================

# Tabla de transacciones raw (particionada y clusterizada)
resource "google_bigquery_table" "transactions_raw" {
  dataset_id = google_bigquery_dataset.transactions.dataset_id
  table_id   = "transactions_raw"

  description = "Transacciones raw desde Cloud Storage"

  # Particionamiento por fecha de transacción
  time_partitioning {
    type  = "DAY"
    field = "transaction_date"
    expiration_ms = 31536000000  # 1 año
  }

  # Clustering por customer_id y merchant_id
  clustering = ["customer_id", "merchant_id"]

  schema = jsonencode([
    {
      name        = "transaction_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ID único de transacción"
    },
    {
      name        = "transaction_date"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Fecha de transacción"
    },
    {
      name        = "transaction_timestamp"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "Timestamp de transacción"
    },
    {
      name        = "customer_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ID del cliente"
    },
    {
      name        = "merchant_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ID del comercio"
    },
    {
      name        = "amount"
      type        = "NUMERIC"
      mode        = "REQUIRED"
      description = "Monto de la transacción"
    },
    {
      name        = "currency"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Código de moneda (ISO 4217)"
    },
    {
      name        = "status"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Estado: approved, declined, pending"
    },
    {
      name        = "payment_method"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Método de pago"
    }
  ])

  labels = {
    environment = var.environment
    layer       = "raw"
  }
}

# Tabla de agregaciones diarias
resource "google_bigquery_table" "daily_summary" {
  dataset_id = google_bigquery_dataset.transactions.dataset_id
  table_id   = "daily_summary"

  description = "Resumen diario de transacciones"

  time_partitioning {
    type  = "DAY"
    field = "summary_date"
  }

  schema = jsonencode([
    {
      name        = "summary_date"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Fecha del resumen"
    },
    {
      name        = "total_transactions"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Total de transacciones"
    },
    {
      name        = "total_amount"
      type        = "NUMERIC"
      mode        = "REQUIRED"
      description = "Monto total"
    },
    {
      name        = "approved_count"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Transacciones aprobadas"
    },
    {
      name        = "declined_count"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Transacciones rechazadas"
    },
    {
      name        = "unique_customers"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Clientes únicos"
    },
    {
      name        = "unique_merchants"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Comercios únicos"
    }
  ])

  labels = {
    environment = var.environment
    layer       = "aggregated"
  }
}

# ============================================
# SERVICE ACCOUNT
# ============================================

resource "google_service_account" "etl_pipeline" {
  account_id   = "${var.project_name}-etl-${var.environment}"
  display_name = "ETL Pipeline Service Account"
  description  = "Service account para pipeline ETL"
}

# Permisos para leer de Cloud Storage
resource "google_storage_bucket_iam_member" "storage_reader" {
  bucket = google_storage_bucket.raw_data.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.etl_pipeline.email}"
}

# Permisos para escribir en BigQuery
resource "google_bigquery_dataset_iam_member" "data_editor" {
  dataset_id = google_bigquery_dataset.transactions.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.etl_pipeline.email}"
}

# ============================================
# SCHEDULED QUERY (Agregación Diaria)
# ============================================

resource "google_bigquery_data_transfer_config" "daily_aggregation" {
  display_name           = "Daily Transaction Summary"
  location               = var.gcp_region
  data_source_id         = "scheduled_query"
  schedule               = "every day 02:00"
  destination_dataset_id = google_bigquery_dataset.transactions.dataset_id

  params = {
    query = <<-SQL
      INSERT INTO `${var.gcp_project_id}.${google_bigquery_dataset.transactions.dataset_id}.${google_bigquery_table.daily_summary.table_id}`
      (summary_date, total_transactions, total_amount, approved_count, declined_count, unique_customers, unique_merchants)

      SELECT
        transaction_date as summary_date,
        COUNT(*) as total_transactions,
        SUM(amount) as total_amount,
        COUNTIF(status = 'approved') as approved_count,
        COUNTIF(status = 'declined') as declined_count,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(DISTINCT merchant_id) as unique_merchants
      FROM
        `${var.gcp_project_id}.${google_bigquery_dataset.transactions.dataset_id}.${google_bigquery_table.transactions_raw.table_id}`
      WHERE
        transaction_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
      GROUP BY
        transaction_date
    SQL

    destination_table_name_template = google_bigquery_table.daily_summary.table_id
    write_disposition               = "WRITE_APPEND"
  }
}

# ============================================
# OUTPUTS
# ============================================

output "storage_bucket_name" {
  description = "Nombre del bucket de Cloud Storage"
  value       = google_storage_bucket.raw_data.name
}

output "dataset_id" {
  description = "ID del dataset de BigQuery"
  value       = google_bigquery_dataset.transactions.dataset_id
}

output "transactions_table_id" {
  description = "ID de la tabla de transacciones"
  value       = google_bigquery_table.transactions_raw.table_id
}

output "summary_table_id" {
  description = "ID de la tabla de resumen"
  value       = google_bigquery_table.daily_summary.table_id
}

output "service_account_email" {
  description = "Email del service account"
  value       = google_service_account.etl_pipeline.email
}
```

### 🚀 Despliegue

```bash
# 1. Inicializar
terraform init

# 2. Plan (especificar project ID)
terraform plan -var="gcp_project_id=mi-proyecto-gcp-123"

# 3. Aplicar
terraform apply -var="gcp_project_id=mi-proyecto-gcp-123"

# 4. Ver outputs
terraform output
```

### 🧪 Cargar Datos de Prueba

```bash
# Crear archivo CSV de transacciones
cat > transactions.csv << EOF
transaction_id,transaction_date,transaction_timestamp,customer_id,merchant_id,amount,currency,status,payment_method
TXN001,2025-11-09,2025-11-09 10:00:00,CUST123,MERCH456,150.00,USD,approved,credit_card
TXN002,2025-11-09,2025-11-09 10:05:00,CUST456,MERCH789,75.50,USD,approved,debit_card
TXN003,2025-11-09,2025-11-09 10:10:00,CUST789,MERCH456,200.00,USD,declined,credit_card
EOF

# Subir a Cloud Storage
gsutil cp transactions.csv gs://BUCKET_NAME/raw/2025/11/09/

# Cargar a BigQuery desde Cloud Storage
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --autodetect \
  transactions_dev.transactions_raw \
  gs://BUCKET_NAME/raw/2025/11/09/transactions.csv

# Verificar datos
bq query --use_legacy_sql=false \
  'SELECT * FROM `transactions_dev.transactions_raw` LIMIT 10'
```

### 💰 Cálculo de Costos

**Escenario**: 10M transacciones/mes

```
Cloud Storage (100 GB):
- Standard: $2.00/mes
- Nearline (después 90 días): $1.00/GB/mes
- Coldline (después 1 año): $0.40/GB/mes

BigQuery Storage (500 GB activo):
- Primeros 10 GB: Gratis
- 490 GB: $9.80/mes

BigQuery Queries (10 TB escaneados/mes):
- Primero 1 TB: Gratis
- 9 TB: $45/mes

Scheduled Query (1/día):
- Incluido en query cost

Total mensual: ~$57/mes

🚀 Con partitioning: Reducción del 90% en queries = $11/mes
💰 AHORRO: $46/mes ($552/año)
```

---

**[Continúa con Ejemplos 4 y 5...]**

*Los ejemplos 4 y 5 incluyen arquitecturas multi-cloud y módulos reutilizables de Terraform para CI/CD.*

---

## 🎯 Resumen de Ejemplos

| Ejemplo | Dificultad | Herramienta | Servicios | Ahorro Costo |
|---------|------------|-------------|-----------|--------------|
| 1 | ⭐ | Terraform | S3 + Lifecycle | 69% |
| 2 | ⭐⭐ | CloudFormation | S3 + Lambda | ~$0 (Free Tier) |
| 3 | ⭐⭐⭐ | Terraform | GCS + BigQuery | 81% |
| 4 | ⭐⭐⭐⭐ | Terraform | Multi-Cloud | Variable |
| 5 | ⭐⭐⭐⭐ | Terraform | CI/CD Complete | N/A |

---

## 📚 Próximos Pasos

1. Practicar los ejemplos en tu cuenta (usar Free Tier)
2. Modificar parámetros y ver cómo afecta el plan
3. Completar ejercicios en `03-EJERCICIOS.md`
4. Implementar el proyecto práctico

---

**¡Felicidades!** Has completado los ejemplos de Infrastructure as Code. 🎉
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
