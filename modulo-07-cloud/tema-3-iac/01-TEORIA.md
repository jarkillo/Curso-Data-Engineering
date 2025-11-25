# 📚 Infraestructura como Código (IaC)

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [¿Qué es IaC?](#qué-es-iac)
3. [Terraform](#terraform)
4. [AWS CloudFormation](#aws-cloudformation)
5. [Comparación Terraform vs CloudFormation](#comparación-terraform-vs-cloudformation)
6. [Best Practices](#best-practices)
7. [Checklist de Aprendizaje](#checklist-de-aprendizaje)

---

## Introducción

**Imagina que tienes que montar una infraestructura en la nube**: buckets S3, tablas BigQuery, instancias EC2, redes VPC, roles IAM... Si lo haces manualmente (clickeando en la consola web), tardarías horas y sería imposible de replicar sin errores.

**Infraestructura como Código (IaC)** es la práctica de **gestionar infraestructura usando archivos de configuración** en lugar de hacerlo manualmente.

### Analogía: La Receta de Cocina

**Sin IaC** (manual):
- "Clickea aquí, luego aquí, ahora copia este ARN, pégalo allá..."
- Si quieres replicar en otro entorno: vuelve a clickear todo
- Si alguien más lo hace: puede equivocarse
- Si necesitas documentar: tomas screenshots 📸

**Con IaC** (automatizado):
- Escribes una "receta" (archivo de configuración)
- Ejecutas un comando: `terraform apply`
- La infraestructura se crea automáticamente
- La "receta" sirve como documentación
- Puedes versionarla en Git

---

## ¿Qué es IaC?

### Definición

**Infraestructura como Código** es el proceso de **gestionar y provisionar infraestructura mediante archivos de configuración legibles** en lugar de configuración manual o herramientas interactivas.

### Beneficios

1. **Reproducibilidad**: La misma configuración produce la misma infraestructura
2. **Versionado**: Usas Git para trackear cambios
3. **Documentación automática**: El código ES la documentación
4. **Testing**: Puedes testear infraestructura antes de deployar
5. **Colaboración**: Equipos trabajan juntos con pull requests
6. **Rollback fácil**: Si algo falla, vuelves a la versión anterior
7. **Consistencia**: Dev, staging y prod son idénticos

### Tipos de IaC

#### 1. **Declarativo** (lo que quieres, no cómo hacerlo)

```hcl
# Terraform (declarativo)
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-lake"
  acl    = "private"
}
```

**Descripción**: "Quiero un bucket S3 llamado 'my-data-lake' con ACL privado"

El sistema se encarga de:
- Verificar si ya existe
- Crearlo si no existe
- Actualizarlo si cambió la configuración

#### 2. **Imperativo** (paso a paso, cómo hacerlo)

```python
# Python boto3 (imperativo)
import boto3

s3 = boto3.client('s3')

# Paso 1: Verificar si existe
try:
    s3.head_bucket(Bucket='my-data-lake')
except:
    # Paso 2: Crear si no existe
    s3.create_bucket(Bucket='my-data-lake')

# Paso 3: Configurar ACL
s3.put_bucket_acl(Bucket='my-data-lake', ACL='private')
```

**IaC moderno prefiere declarativo** porque es más simple y menos propenso a errores.

---

## Terraform

### ¿Qué es Terraform?

**Terraform** es una herramienta de **IaC open-source** creada por HashiCorp que permite:
- Provisionar infraestructura en **múltiples clouds** (AWS, GCP, Azure)
- Usar un lenguaje declarativo (HCL - HashiCorp Configuration Language)
- Gestionar el estado de la infraestructura

### Analogía: El Constructor Universal

Terraform es como un **constructor que habla varios idiomas**:
- AWS = español
- GCP = inglés
- Azure = francés

Tú le das instrucciones en **un solo idioma (HCL)** y él se encarga de comunicarse con cada cloud en su idioma nativo.

### Arquitectura de Terraform

```
┌─────────────────────────────────────────────────────────┐
│                  Terraform Workflow                      │
└─────────────────────────────────────────────────────────┘

1. WRITE (.tf files)
   ↓
   main.tf
   variables.tf
   outputs.tf

2. INIT (terraform init)
   ↓
   Descarga providers (AWS, GCP, etc.)

3. PLAN (terraform plan)
   ↓
   Muestra qué va a cambiar (preview)

4. APPLY (terraform apply)
   ↓
   Crea/modifica/elimina recursos

5. STATE (terraform.tfstate)
   ↓
   Guarda el estado actual de la infraestructura
```

### Conceptos Clave

#### 1. **Providers**

Son "plugins" que permiten a Terraform comunicarse con APIs de clouds.

```hcl
# Provider de AWS
provider "aws" {
  region = "us-east-1"
}

# Provider de GCP
provider "google" {
  project = "my-project"
  region  = "us-central1"
}
```

#### 2. **Resources**

Son los componentes de infraestructura que quieres crear.

```hcl
# Recurso: S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "healthtech-data-lake"

  tags = {
    Environment = "Production"
    Team        = "Data Engineering"
  }
}

# Recurso: BigQuery Dataset
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "healthtech_analytics"
  location   = "US"
}
```

#### 3. **Variables**

Permiten parametrizar la configuración.

```hcl
# variables.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

# Uso en main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.bucket_name}-${var.environment}"
}
```

#### 4. **Outputs**

Exponen información útil después del `apply`.

```hcl
# outputs.tf
output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "bucket_url" {
  value = "s3://${aws_s3_bucket.data_lake.bucket}"
}
```

**Uso**:
```bash
$ terraform apply
...
Outputs:

bucket_arn = "arn:aws:s3:::healthtech-data-lake-prod"
bucket_url = "s3://healthtech-data-lake-prod"
```

#### 5. **State**

Terraform mantiene un archivo `terraform.tfstate` que contiene:
- Qué recursos ha creado
- IDs de esos recursos en la cloud
- Metadatos

**Importante**:
- ⚠️ NO commitear `terraform.tfstate` a Git (contiene secretos)
- ✅ Usar **remote state** en S3 o GCS para colaboración

```hcl
# Backend remoto en S3
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Ejemplo Completo: Data Lake en AWS

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

# S3 Bucket para Raw Data
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-data-${var.environment}"

  tags = {
    Environment = var.environment
    Layer       = "raw"
    ManagedBy   = "Terraform"
  }
}

# Versionado del bucket
resource "aws_s3_bucket_versioning" "raw_data_versioning" {
  bucket = aws_s3_bucket.raw_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle policy
resource "aws_s3_bucket_lifecycle_configuration" "raw_data_lifecycle" {
  bucket = aws_s3_bucket.raw_data.id

  rule {
    id     = "move-to-glacier"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

# S3 Bucket para Processed Data
resource "aws_s3_bucket" "processed_data" {
  bucket = "${var.project_name}-processed-data-${var.environment}"

  tags = {
    Environment = var.environment
    Layer       = "processed"
    ManagedBy   = "Terraform"
  }
}

# Glue Database
resource "aws_glue_catalog_database" "analytics_db" {
  name        = "${var.project_name}_analytics_${var.environment}"
  description = "Database for analytics workloads"
}

# Glue Table
resource "aws_glue_catalog_table" "logs_table" {
  name          = "api_logs"
  database_name = aws_glue_catalog_database.analytics_db.name

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.processed_data.bucket}/logs/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"

      parameters = {
        "field.delim" = ","
      }
    }

    columns {
      name = "timestamp"
      type = "string"
    }

    columns {
      name = "endpoint"
      type = "string"
    }

    columns {
      name = "status_code"
      type = "int"
    }
  }
}

# IAM Role para Glue Jobs
resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-glue-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Policy para Glue
resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Policy para acceso a S3
resource "aws_iam_role_policy" "glue_s3_policy" {
  name = "glue-s3-access"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.raw_data.arn}/*",
          "${aws_s3_bucket.processed_data.arn}/*"
        ]
      }
    ]
  })
}
```

```hcl
# variables.tf

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "healthtech"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
```

```hcl
# outputs.tf

output "raw_bucket_name" {
  description = "Name of the raw data bucket"
  value       = aws_s3_bucket.raw_data.bucket
}

output "processed_bucket_name" {
  description = "Name of the processed data bucket"
  value       = aws_s3_bucket.processed_data.bucket
}

output "glue_database_name" {
  description = "Name of the Glue database"
  value       = aws_glue_catalog_database.analytics_db.name
}

output "glue_role_arn" {
  description = "ARN of the Glue IAM role"
  value       = aws_iam_role.glue_role.arn
}
```

### Comandos Terraform

```bash
# 1. Inicializar proyecto (descarga providers)
terraform init

# 2. Formatear código
terraform fmt

# 3. Validar sintaxis
terraform validate

# 4. Ver plan de ejecución (preview)
terraform plan

# 5. Aplicar cambios (crear infraestructura)
terraform apply

# 6. Aplicar sin confirmación (para CI/CD)
terraform apply -auto-approve

# 7. Ver estado actual
terraform show

# 8. Listar recursos creados
terraform state list

# 9. Ver outputs
terraform output

# 10. Destruir toda la infraestructura
terraform destroy
```

---

## AWS CloudFormation

### ¿Qué es CloudFormation?

**CloudFormation** es el servicio de IaC nativo de AWS. Permite:
- Provisionar recursos de AWS usando templates JSON o YAML
- Gestionar infraestructura como "stacks"
- Rollback automático si algo falla

### Analogía: El Arquitecto de AWS

CloudFormation es como un **arquitecto especializado en AWS**:
- Solo construye en AWS (no multi-cloud)
- Habla el idioma nativo de AWS
- Está profundamente integrado con todos los servicios AWS

### Arquitectura de CloudFormation

```
┌─────────────────────────────────────────────────────────┐
│              CloudFormation Workflow                     │
└─────────────────────────────────────────────────────────┘

1. WRITE (template.yaml)
   ↓
   Define recursos en YAML/JSON

2. CREATE STACK
   ↓
   aws cloudformation create-stack

3. CLOUDFORMATION SERVICE
   ↓
   Provisiona recursos en orden correcto

4. EVENTS
   ↓
   CloudFormation emite eventos de progreso

5. OUTPUTS
   ↓
   Expone valores útiles (ARNs, URLs, etc.)

6. UPDATE STACK (si cambias template)
   ↓
   CloudFormation calcula el diff y aplica cambios

7. DELETE STACK (limpieza)
   ↓
   Elimina todos los recursos creados
```

### Conceptos Clave

#### 1. **Template**

Archivo YAML o JSON que define la infraestructura.

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Data Lake Infrastructure'

Parameters:
  EnvironmentName:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod

Resources:
  RawDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${EnvironmentName}-raw-data-bucket'
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: MoveToGlacier
            Status: Enabled
            Transitions:
              - StorageClass: GLACIER
                TransitionInDays: 90
            ExpirationInDays: 365

Outputs:
  RawBucketName:
    Description: Name of the raw data bucket
    Value: !Ref RawDataBucket
    Export:
      Name: !Sub '${EnvironmentName}-RawBucketName'
```

#### 2. **Intrinsic Functions**

Funciones especiales para manipular valores.

```yaml
# !Ref - Referencia a otro recurso o parámetro
BucketName: !Ref RawDataBucket

# !Sub - Sustitución de variables
BucketName: !Sub '${EnvironmentName}-data-${AWS::Region}'

# !GetAtt - Obtener atributo de un recurso
BucketArn: !GetAtt RawDataBucket.Arn

# !Join - Unir strings
FullName: !Join ['-', [!Ref ProjectName, !Ref EnvironmentName]]

# !If - Condicional
BucketName: !If [IsProduction, 'prod-bucket', 'dev-bucket']
```

#### 3. **Parameters**

Valores que se pasan al crear el stack.

```yaml
Parameters:
  EnvironmentName:
    Type: String
    Description: Environment name
    Default: dev

  RetentionDays:
    Type: Number
    Description: Days to retain data
    Default: 90
    MinValue: 30
    MaxValue: 365
```

#### 4. **Outputs**

Valores expuestos después de crear el stack.

```yaml
Outputs:
  BucketARN:
    Description: ARN of the S3 bucket
    Value: !GetAtt RawDataBucket.Arn

  GlueDatabaseName:
    Description: Name of the Glue database
    Value: !Ref GlueDatabase
    Export:
      Name: !Sub '${AWS::StackName}-GlueDB'
```

#### 5. **Stack**

Un conjunto de recursos gestionados como una unidad.

```bash
# Crear stack
aws cloudformation create-stack \
  --stack-name healthtech-data-lake \
  --template-body file://template.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=prod

# Ver estado del stack
aws cloudformation describe-stacks \
  --stack-name healthtech-data-lake

# Actualizar stack
aws cloudformation update-stack \
  --stack-name healthtech-data-lake \
  --template-body file://template.yaml

# Eliminar stack
aws cloudformation delete-stack \
  --stack-name healthtech-data-lake
```

### Ejemplo Completo: Pipeline ETL en CloudFormation

```yaml
# data-pipeline.yaml

AWSTemplateFormatVersion: '2010-09-09'
Description: 'ETL Pipeline for HealthTech Analytics'

Parameters:
  ProjectName:
    Type: String
    Default: healthtech
    Description: Name of the project

  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod
    Description: Environment name

Conditions:
  IsProduction: !Equals [!Ref Environment, prod]

Resources:
  # S3 Bucket para datos raw
  RawDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-raw-${Environment}-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToGlacier
            Status: Enabled
            Transitions:
              - StorageClass: GLACIER
                TransitionInDays: !If [IsProduction, 90, 30]
            ExpirationInDays: !If [IsProduction, 365, 180]
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation

  # S3 Bucket para datos procesados
  ProcessedDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-processed-${Environment}-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation

  # Glue Database
  GlueDatabase:
    Type: AWS::Glue::Database
    Properties:
      CatalogId: !Ref AWS::AccountId
      DatabaseInput:
        Name: !Sub '${ProjectName}_${Environment}'
        Description: !Sub 'Analytics database for ${Environment}'

  # Glue Crawler
  GlueCrawler:
    Type: AWS::Glue::Crawler
    Properties:
      Name: !Sub '${ProjectName}-crawler-${Environment}'
      Role: !GetAtt GlueCrawlerRole.Arn
      DatabaseName: !Ref GlueDatabase
      Targets:
        S3Targets:
          - Path: !Sub 's3://${ProcessedDataBucket}/logs/'
      SchemaChangePolicy:
        UpdateBehavior: UPDATE_IN_DATABASE
        DeleteBehavior: LOG
      Schedule:
        ScheduleExpression: 'cron(0 1 * * ? *)'  # 1 AM diario

  # IAM Role para Glue Crawler
  GlueCrawlerRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: glue.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource:
                  - !Sub '${ProcessedDataBucket.Arn}/*'

  # Lambda Function para procesamiento
  ProcessorLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-processor-${Environment}'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LambdaRole.Arn
      Timeout: 300
      MemorySize: 512
      Environment:
        Variables:
          RAW_BUCKET: !Ref RawDataBucket
          PROCESSED_BUCKET: !Ref ProcessedDataBucket
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import json
          import boto3
          import os

          def lambda_handler(event, context):
              print(f"Processing event: {json.dumps(event)}")

              # Lógica de procesamiento aquí

              return {
                  'statusCode': 200,
                  'body': json.dumps('Processing complete')
              }

  # IAM Role para Lambda
  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
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
                  - s3:PutObject
                Resource:
                  - !Sub '${RawDataBucket.Arn}/*'
                  - !Sub '${ProcessedDataBucket.Arn}/*'

  # S3 Event para trigger Lambda
  LambdaTriggerPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ProcessorLambda
      Action: lambda:InvokeFunction
      Principal: s3.amazonaws.com
      SourceArn: !GetAtt RawDataBucket.Arn

  # Athena Workgroup
  AthenaWorkgroup:
    Type: AWS::Athena::WorkGroup
    Properties:
      Name: !Sub '${ProjectName}-${Environment}'
      Description: !Sub 'Athena workgroup for ${Environment}'
      WorkGroupConfiguration:
        ResultConfigurationUpdates:
          OutputLocation: !Sub 's3://${ProcessedDataBucket}/athena-results/'
        EnforceWorkGroupConfiguration: true
        PublishCloudWatchMetricsEnabled: true

Outputs:
  RawBucketName:
    Description: Name of raw data bucket
    Value: !Ref RawDataBucket
    Export:
      Name: !Sub '${AWS::StackName}-RawBucket'

  ProcessedBucketName:
    Description: Name of processed data bucket
    Value: !Ref ProcessedDataBucket
    Export:
      Name: !Sub '${AWS::StackName}-ProcessedBucket'

  GlueDatabaseName:
    Description: Name of Glue database
    Value: !Ref GlueDatabase

  LambdaFunctionArn:
    Description: ARN of processor Lambda
    Value: !GetAtt ProcessorLambda.Arn

  AthenaWorkgroupName:
    Description: Name of Athena workgroup
    Value: !Ref AthenaWorkgroup
```

---

## Comparación Terraform vs CloudFormation

| Aspecto | Terraform | CloudFormation |
|---------|-----------|----------------|
| **Proveedor** | HashiCorp (open-source) | AWS (nativo) |
| **Multi-cloud** | ✅ Sí (AWS, GCP, Azure, +) | ❌ Solo AWS |
| **Lenguaje** | HCL (declarativo) | JSON/YAML (declarativo) |
| **State Management** | Manual (local o S3/GCS) | Automático (AWS gestiona) |
| **Preview** | `terraform plan` | `aws cloudformation create-change-set` |
| **Rollback** | Manual | ✅ Automático si falla |
| **Costo** | Gratis (open-source) | Gratis (incluido en AWS) |
| **Comunidad** | Enorme (muchos módulos) | Grande (AWS docs) |
| **Learning Curve** | Media | Media-Alta |
| **Integración AWS** | Buena | ✅ Perfecta (nativo) |
| **Testing** | Terratest, Kitchen-Terraform | TaskCat, cfn-lint |
| **IDE Support** | Excelente (VS Code, IntelliJ) | Bueno (VS Code) |

### ¿Cuándo usar Terraform?

✅ **Usa Terraform si**:
- Necesitas multi-cloud (AWS + GCP + Azure)
- Quieres una herramienta unificada
- Prefieres HCL sobre YAML
- Valoras la comunidad open-source
- Quieres módulos reutilizables (Terraform Registry)

### ¿Cuándo usar CloudFormation?

✅ **Usa CloudFormation si**:
- Solo usas AWS
- Quieres integración nativa perfecta
- Prefieres que AWS gestione el state
- Necesitas rollback automático
- Usas servicios AWS muy nuevos (CloudFormation los soporta primero)

### Caso Real: Combinación

Muchas empresas usan **ambos**:
- **Terraform**: Para infraestructura base (VPC, IAM, S3)
- **CloudFormation**: Para stacks de aplicaciones específicas

---

## Best Practices

### 1. Estructura de Proyecto

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── data-lake/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── etl-pipeline/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── README.md
```

### 2. Usar Módulos

**Módulo reutilizable** (`modules/s3-bucket/`):
```hcl
# modules/s3-bucket/main.tf
resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.bucket.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}
```

**Uso del módulo**:
```hcl
# environments/prod/main.tf
module "data_lake" {
  source = "../../modules/s3-bucket"

  bucket_name        = "my-data-lake-prod"
  enable_versioning  = true

  tags = {
    Environment = "prod"
    Team        = "Data"
  }
}
```

### 3. Separar Entornos

**NO hacer**:
```hcl
# ❌ Un solo archivo para todos los entornos
resource "aws_s3_bucket" "dev_bucket" { ... }
resource "aws_s3_bucket" "prod_bucket" { ... }
```

**SÍ hacer**:
```
✅ Entornos separados con workspaces o directorios
environments/dev/
environments/prod/
```

### 4. Usar Variables

```hcl
# variables.tf
variable "environment" {
  type    = string
  default = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket"

  # No default - obligatorio
}
```

```hcl
# terraform.tfvars (dev)
environment = "dev"
bucket_name = "my-bucket-dev"
```

### 5. Remote State

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"  # Para locking
  }
}
```

### 6. Naming Conventions

```hcl
# ✅ Naming consistente
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project}-raw-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

# Ejemplo: healthtech-raw-prod-123456789012
```

### 7. Tagging Obligatorio

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Owner       = "Data Team"
    CostCenter  = "Engineering"
  }
}

resource "aws_s3_bucket" "data_lake" {
  bucket = var.bucket_name
  tags   = local.common_tags
}
```

### 8. Versionado de Providers

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # 5.x.x
    }
  }
}
```

### 9. Testing

**Terratest** (Go):
```go
// test/data_lake_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestDataLake(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../environments/dev",
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    bucketName := terraform.Output(t, terraformOptions, "raw_bucket_name")
    assert.Contains(t, bucketName, "healthtech-raw-dev")
}
```

### 10. CI/CD Integration

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Terraform Init
        run: terraform init

      - name: Terraform Format
        run: terraform fmt -check

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
```

---

## Checklist de Aprendizaje

Marca lo que ya dominas:

### Conceptos
- [ ] Entiendo qué es IaC y por qué es importante
- [ ] Conozco la diferencia entre declarativo e imperativo
- [ ] Sé cuándo usar Terraform vs CloudFormation

### Terraform
- [ ] Puedo escribir un archivo `.tf` básico
- [ ] Entiendo providers, resources, variables, outputs
- [ ] Sé usar `terraform init`, `plan`, `apply`, `destroy`
- [ ] Entiendo el concepto de state
- [ ] Puedo configurar remote state en S3/GCS
- [ ] Sé crear módulos reutilizables
- [ ] Puedo usar workspaces para múltiples entornos

### CloudFormation
- [ ] Puedo escribir un template YAML básico
- [ ] Entiendo Parameters, Resources, Outputs
- [ ] Sé usar intrinsic functions (!Ref, !Sub, !GetAtt)
- [ ] Puedo crear y actualizar stacks
- [ ] Entiendo cómo funciona el rollback automático

### Best Practices
- [ ] Uso versionado de providers
- [ ] Separo entornos (dev/staging/prod)
- [ ] Uso tagging consistente
- [ ] Implemento naming conventions
- [ ] Uso remote state para colaboración
- [ ] Nunca commiteo credenciales o state files

---

## Recursos Adicionales

- **Terraform Docs**: https://www.terraform.io/docs
- **Terraform Registry**: https://registry.terraform.io/ (módulos)
- **CloudFormation Docs**: https://docs.aws.amazon.com/cloudformation/
- **Terratest**: https://terratest.gruntwork.io/
- **Libro**: "Terraform: Up & Running" por Yevgeniy Brikman

---

*Última actualización: 2025-01-15*
