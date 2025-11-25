# 📝 Ejercicios: Infrastructure as Code (Terraform y CloudFormation)

Este documento contiene **15 ejercicios prácticos** de Infrastructure as Code, desde nivel básico hasta avanzado.

---

## 📋 Estructura de Ejercicios

- **Ejercicios 1-5**: ⭐ Básico (Terraform y CloudFormation fundamentales)
- **Ejercicios 6-10**: ⭐⭐ Intermedio (Arquitecturas de datos)
- **Ejercicios 11-15**: ⭐⭐⭐ Avanzado (Multi-cloud, módulos, CI/CD)

---

## ⭐ Ejercicios Básicos

### Ejercicio 1: Primer Bucket S3 con Terraform

**Objetivo**: Crear un bucket S3 con tags usando Terraform.

**Requisitos**:
- Bucket name: `mi-primer-bucket-terraform-<TU_NOMBRE>`
- Tags: `Environment=dev`, `ManagedBy=Terraform`, `Owner=<TU_NOMBRE>`
- Region: `us-east-1`

**Archivos a crear**:
- `main.tf`
- `variables.tf`
- `outputs.tf`

**Validación**:
```bash
terraform init
terraform plan
terraform apply
aws s3 ls | grep mi-primer-bucket
```

---

### Ejercicio 2: Lifecycle Policy con Terraform

**Objetivo**: Añadir lifecycle policy al bucket del Ejercicio 1.

**Requisitos**:
- Mover a `STANDARD_IA` después de 30 días
- Mover a `GLACIER` después de 90 días
- Eliminar después de 365 días

**Validación**:
```bash
terraform plan  # Debe mostrar 1 cambio (lifecycle)
terraform apply
aws s3api get-bucket-lifecycle-configuration --bucket NOMBRE_BUCKET
```

---

### Ejercicio 3: Lambda Function con CloudFormation

**Objetivo**: Crear una función Lambda que retorne "Hello from Lambda!".

**Requisitos**:
- Runtime: `python3.11`
- Handler: `index.lambda_handler`
- Timeout: 10 segundos
- Memory: 128 MB
- IAM role con permisos básicos de ejecución

**Template**: `lambda-hello.yaml`

**Validación**:
```bash
aws cloudformation create-stack \
  --stack-name lambda-hello \
  --template-body file://lambda-hello.yaml \
  --capabilities CAPABILITY_IAM

aws lambda invoke --function-name NOMBRE_FUNCION output.json
cat output.json
```

**Salida esperada**:
```json
{
  "statusCode": 200,
  "body": "Hello from Lambda!"
}
```

---

### Ejercicio 4: Variables y Outputs en Terraform

**Objetivo**: Refactorizar Ejercicio 1 usando variables.

**Requisitos**:
Crear `variables.tf` con:
- `bucket_name` (string, sin default)
- `environment` (string, default: "dev")
- `owner_name` (string, sin default)
- `region` (string, default: "us-east-1")

Crear `outputs.tf` con:
- `bucket_name`
- `bucket_arn`
- `bucket_region`

**Validación**:
```bash
terraform plan -var="bucket_name=mi-bucket" -var="owner_name=Juan"
terraform output
```

---

### Ejercicio 5: Stack Parameters en CloudFormation

**Objetivo**: Crear stack de S3 con parámetros.

**Requisitos**:
Parameters:
- `BucketNamePrefix` (String)
- `Environment` (String, AllowedValues: dev, staging, prod)
- `EnableVersioning` (String, AllowedValues: Enabled, Suspended)

Resources:
- S3 Bucket con versionado configurable

Outputs:
- `BucketName`
- `BucketArn`

**Validación**:
```bash
aws cloudformation create-stack \
  --stack-name s3-parametrizado \
  --template-body file://s3-params.yaml \
  --parameters \
    ParameterKey=BucketNamePrefix,ParameterValue=data-lake \
    ParameterKey=Environment,ParameterValue=dev \
    ParameterKey=EnableVersioning,ParameterValue=Enabled
```

---

## ⭐⭐ Ejercicios Intermedios

### Ejercicio 6: Data Pipeline S3 + Lambda con Terraform

**Objetivo**: Crear pipeline que procese archivos CSV subidos a S3.

**Requisitos**:
- Bucket S3 para input
- Bucket S3 para output
- Lambda function con Python 3.11
- Lambda debe leer CSV, contar filas, escribir resultado
- S3 trigger: invocar Lambda cuando se cree archivo `.csv`
- IAM role con permisos mínimos

**Validación**:
```bash
# Subir CSV
aws s3 cp test.csv s3://BUCKET_INPUT/test.csv

# Verificar output
aws s3 ls s3://BUCKET_OUTPUT/
aws s3 cp s3://BUCKET_OUTPUT/test_result.json -
```

**Output esperado**:
```json
{
  "input_file": "test.csv",
  "row_count": 100,
  "processed_at": "2025-11-09T10:00:00Z"
}
```

---

### Ejercicio 7: BigQuery Dataset con Terraform

**Objetivo**: Crear dataset de BigQuery con 2 tablas.

**Requisitos**:
- Dataset: `ecommerce_analytics`
- Tabla 1: `orders` (particionada por `order_date`, clusterizada por `customer_id`)
- Tabla 2: `customers` (sin particionamiento)
- Service account con permisos de lectura

**Schema Orders**:
```
- order_id: STRING (REQUIRED)
- order_date: DATE (REQUIRED)
- customer_id: STRING (REQUIRED)
- total_amount: NUMERIC (REQUIRED)
- status: STRING (REQUIRED)
```

**Schema Customers**:
```
- customer_id: STRING (REQUIRED)
- name: STRING (REQUIRED)
- email: STRING (REQUIRED)
- signup_date: DATE (REQUIRED)
```

**Validación**:
```bash
terraform apply
bq show ecommerce_analytics
bq show ecommerce_analytics.orders
```

---

### Ejercicio 8: Multi-Environment con Terraform Workspaces

**Objetivo**: Desplegar mismo código en 3 ambientes (dev, staging, prod).

**Requisitos**:
- Usar Terraform workspaces
- S3 bucket con sufijo del ambiente
- Tags diferentes por ambiente
- Variables condicionales según workspace

**Comandos**:
```bash
# Dev
terraform workspace new dev
terraform apply

# Staging
terraform workspace new staging
terraform apply -var="bucket_size=medium"

# Prod
terraform workspace new prod
terraform apply -var="bucket_size=large" -var="enable_backup=true"

# Listar workspaces
terraform workspace list

# Ver recursos por ambiente
terraform workspace select dev
terraform state list
```

---

### Ejercicio 9: Scheduled Query con CloudFormation

**Objetivo**: Crear tabla BigQuery y scheduled query.

**Requisitos**:
- Tabla `sales_raw` (particionada por fecha)
- Tabla `sales_daily_summary` (agregaciones)
- Scheduled Query que corra todos los días a las 2 AM
- Query: agrupar ventas por día, calcular totales

**CloudFormation**: Usar `AWS::Events::Rule` + Lambda + BigQuery API

**Validación**:
- Verificar que query se ejecute automáticamente
- Revisar logs en CloudWatch

---

### Ejercicio 10: Networking para Data Pipeline

**Objetivo**: Crear VPC con subnets para pipeline de datos.

**Requisitos con Terraform**:
- VPC con CIDR `10.0.0.0/16`
- 2 subnets públicas (para NAT Gateway)
- 2 subnets privadas (para Lambda, RDS)
- Internet Gateway
- NAT Gateway
- Route Tables
- Security Groups:
  - SG para Lambda (egress a internet)
  - SG para RDS (ingress desde Lambda)

**Validación**:
```bash
terraform apply
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=data-pipeline-vpc"
aws ec2 describe-subnets --filters "Name=vpc-id,Values=VPC_ID"
```

---

## ⭐⭐⭐ Ejercicios Avanzados

### Ejercicio 11: Módulo Reutilizable de Terraform

**Objetivo**: Crear módulo de Terraform para "Data Lake Estándar".

**Estructura del módulo**:
```
modules/
└── data-lake/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

**Recursos del módulo**:
- 3 buckets S3 (raw, processed, analytics)
- Lifecycle policies configurables
- Tags estandarizados
- IAM roles para lectura/escritura
- KMS key para encriptación

**Variables**:
- `project_name`
- `environment`
- `enable_encryption`
- `raw_retention_days`
- `processed_retention_days`

**Uso**:
```hcl
module "data_lake_dev" {
  source = "./modules/data-lake"

  project_name            = "my-project"
  environment             = "dev"
  enable_encryption       = true
  raw_retention_days      = 90
  processed_retention_days = 365
}

module "data_lake_prod" {
  source = "./modules/data-lake"

  project_name            = "my-project"
  environment             = "prod"
  enable_encryption       = true
  raw_retention_days      = 730
  processed_retention_days = 1825
}
```

**Validación**:
```bash
terraform init
terraform plan  # Debe mostrar 2 data lakes
terraform apply
```

---

### Ejercicio 12: Estado Remoto con S3 Backend

**Objetivo**: Configurar Terraform para usar S3 como backend remoto.

**Requisitos**:
1. Crear bucket S3 para estado: `terraform-state-<TU_NOMBRE>`
2. Crear DynamoDB table para lock: `terraform-locks`
3. Configurar backend en `backend.tf`
4. Migrar estado local a remoto
5. Probar lock con 2 terminales simultáneas

**backend.tf**:
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-NOMBRE"
    key            = "data-pipeline/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Validación**:
```bash
terraform init -migrate-state
aws s3 ls s3://terraform-state-NOMBRE/data-pipeline/
aws dynamodb scan --table-name terraform-locks

# En terminal 1:
terraform plan  # Debe adquirir lock

# En terminal 2 (simultánea):
terraform plan  # Debe esperar al lock
```

---

### Ejercicio 13: Multi-Cloud Pipeline (AWS + GCP)

**Objetivo**: Pipeline que usa AWS S3 y GCP BigQuery.

**Arquitectura**:
```
AWS S3 (raw data)
    ↓ (trigger)
AWS Lambda (transform)
    ↓ (API call)
GCP BigQuery (load)
    ↓
GCP Data Studio (visualize)
```

**Requisitos**:
- Terraform con 2 providers (AWS + GCP)
- S3 bucket en AWS
- Lambda con credenciales GCP
- BigQuery dataset en GCP
- Service account con permisos
- Secret Manager para credenciales

**Validación**:
```bash
# Subir CSV a S3
aws s3 cp data.csv s3://multi-cloud-input/data.csv

# Verificar que llegó a BigQuery
bq query "SELECT COUNT(*) FROM dataset.table"
```

---

### Ejercicio 14: CI/CD para Terraform con GitHub Actions

**Objetivo**: Automatizar despliegue de infraestructura con GitHub Actions.

**Requisitos**:
1. Repositorio GitHub con código Terraform
2. Workflow `.github/workflows/terraform.yml`
3. Stages:
   - `terraform fmt -check`
   - `terraform validate`
   - `terraform plan` (en PR)
   - `terraform apply` (en merge a main)
4. Secrets en GitHub:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
5. Protección de branch `main`

**Workflow**:
```yaml
name: Terraform CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Format
        run: terraform fmt -check

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Validación**:
1. Crear PR con cambio en Terraform
2. Verificar que `terraform plan` corra
3. Hacer merge
4. Verificar que `terraform apply` corra
5. Ver logs en GitHub Actions

---

### Ejercicio 15: Disaster Recovery con Terraform

**Objetivo**: Infraestructura replicada en 2 regiones para DR.

**Arquitectura**:
```
Primary Region (us-east-1):
- S3 bucket (source)
- Lambda processor
- RDS database

DR Region (us-west-2):
- S3 bucket (replica)
- Lambda processor (standby)
- RDS replica (read replica)
```

**Requisitos**:
- S3 Cross-Region Replication
- RDS Read Replica en otra región
- Lambda deployado en ambas regiones
- Route53 health checks
- Failover automático con Route53
- Variables para seleccionar región primaria/DR

**Casos a probar**:
1. **Operación normal**: Todo en us-east-1
2. **Failover manual**: Switch a us-west-2
3. **Failback**: Regresar a us-east-1
4. **Data sync**: Verificar que datos se repliquen

**Validación**:
```bash
# Desplegar en ambas regiones
terraform apply -var="primary_region=us-east-1" -var="dr_region=us-west-2"

# Simular failover
terraform apply -var="active_region=us-west-2"

# Verificar RDS replica
aws rds describe-db-instances --region us-west-2

# Verificar S3 replication
aws s3api get-bucket-replication --bucket BUCKET_NAME
```

---

## 📊 Resumen de Ejercicios

| Ejercicio | Dificultad | Herramienta | Conceptos Clave |
|-----------|------------|-------------|-----------------|
| 1 | ⭐ | Terraform | Recursos básicos |
| 2 | ⭐ | Terraform | Lifecycle policies |
| 3 | ⭐ | CloudFormation | Lambda básico |
| 4 | ⭐ | Terraform | Variables y outputs |
| 5 | ⭐ | CloudFormation | Parameters |
| 6 | ⭐⭐ | Terraform | S3 + Lambda pipeline |
| 7 | ⭐⭐ | Terraform | BigQuery |
| 8 | ⭐⭐ | Terraform | Workspaces |
| 9 | ⭐⭐ | CloudFormation | Scheduled queries |
| 10 | ⭐⭐ | Terraform | Networking |
| 11 | ⭐⭐⭐ | Terraform | Módulos reutilizables |
| 12 | ⭐⭐⭐ | Terraform | Estado remoto |
| 13 | ⭐⭐⭐ | Terraform | Multi-cloud |
| 14 | ⭐⭐⭐ | Terraform + CI/CD | GitHub Actions |
| 15 | ⭐⭐⭐ | Terraform | Disaster Recovery |

---

## 🎯 Soluciones

Las soluciones completas están disponibles en el directorio `04-proyecto-practico/ejercicios-resueltos/`.

---

## ✅ Checklist de Progreso

Marca los ejercicios que vayas completando:

- [ ] Ejercicio 1: Primer Bucket S3
- [ ] Ejercicio 2: Lifecycle Policy
- [ ] Ejercicio 3: Lambda con CloudFormation
- [ ] Ejercicio 4: Variables y Outputs
- [ ] Ejercicio 5: Stack Parameters
- [ ] Ejercicio 6: Data Pipeline S3 + Lambda
- [ ] Ejercicio 7: BigQuery Dataset
- [ ] Ejercicio 8: Multi-Environment
- [ ] Ejercicio 9: Scheduled Query
- [ ] Ejercicio 10: Networking
- [ ] Ejercicio 11: Módulo Reutilizable
- [ ] Ejercicio 12: Estado Remoto
- [ ] Ejercicio 13: Multi-Cloud
- [ ] Ejercicio 14: CI/CD
- [ ] Ejercicio 15: Disaster Recovery

---

## 📚 Recursos Adicionales

- [Terraform Registry](https://registry.terraform.io/)
- [AWS CloudFormation Templates](https://aws.amazon.com/cloudformation/resources/templates/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

**¡Felicidades!** Has completado los ejercicios de Infrastructure as Code. 🎉

Ahora continúa con el **proyecto práctico** en `04-proyecto-practico/`.
