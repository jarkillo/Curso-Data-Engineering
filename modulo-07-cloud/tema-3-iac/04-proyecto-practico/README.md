# 🏗️ Proyecto Práctico: Data Lake Multi-Ambiente con Terraform

## 📋 Descripción

Este proyecto implementa un **Data Lake completo** en AWS usando **Terraform** con las mejores prácticas de Infrastructure as Code:

- ✅ **Multi-ambiente**: Dev, Staging, Prod
- ✅ **Modular**: Código reutilizable con módulos
- ✅ **Validado**: Tests automáticos con Terratest
- ✅ **Documentado**: Auto-generación de docs
- ✅ **Seguro**: Encriptación, IAM least privilege, secrets management
- ✅ **Cost-optimized**: Lifecycle policies, tags para billing

---

## 🎯 Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS ACCOUNT                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  VPC (10.0.0.0/16)                    │  │
│  │                                                        │  │
│  │  ┌─────────────────┐      ┌─────────────────┐       │  │
│  │  │ Public Subnet   │      │ Private Subnet  │       │  │
│  │  │  - NAT Gateway  │      │  - Lambda       │       │  │
│  │  │  - Bastion      │      │  - RDS (future) │       │  │
│  │  └─────────────────┘      └─────────────────┘       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                S3 DATA LAKE                          │   │
│  │                                                       │   │
│  │  ┌─────────────┐   ┌─────────────┐  ┌─────────────┐│   │
│  │  │ raw/        │──>│ processed/  │──>│ analytics/  ││   │
│  │  │ (90d→Glacier│   │ (30d→IA)    │   │ (365d TTL)  ││   │
│  │  └─────────────┘   └─────────────┘  └─────────────┘│   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                LAMBDA PIPELINE                        │   │
│  │  - Trigger: S3 ObjectCreated (raw/)                  │   │
│  │  - Process: Transform CSV → Parquet                  │   │
│  │  - Output: S3 processed/                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              GLUE CATALOG                             │   │
│  │  - Database: data_lake                                │   │
│  │  - Tables: raw_data, processed_data                  │   │
│  │  - Crawler: Auto-discovery schemas                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ATHENA QUERIES                           │   │
│  │  - Query processed data with SQL                     │   │
│  │  - Results → analytics/                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              CLOUDWATCH MONITORING                    │   │
│  │  - Lambda logs (7 days retention)                    │   │
│  │  - Alarms: Lambda errors, S3 metrics                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── README.md                    ← Este archivo
├── requirements.txt             ← Python dependencies para scripts
│
├── terraform/                   ← Código Terraform
│   ├── environments/            ← Configuración por ambiente
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── backend.tf
│   │   ├── staging/
│   │   │   ├── main.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── backend.tf
│   │   └── prod/
│   │       ├── main.tf
│   │       ├── terraform.tfvars
│   │       └── backend.tf
│   │
│   └── modules/                 ← Módulos reutilizables
│       ├── data-lake/           ← Módulo S3 buckets + lifecycle
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       ├── lambda-etl/          ← Módulo Lambda function
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   ├── lambda_function.py
│       │   └── README.md
│       ├── networking/          ← Módulo VPC + subnets
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── README.md
│       └── glue-catalog/        ← Módulo Glue database + crawler
│           ├── main.tf
│           ├── variables.tf
│           ├── outputs.tf
│           └── README.md
│
├── tests/                       ← Tests de infraestructura
│   ├── test_terraform_validate.py
│   ├── test_terraform_format.py
│   ├── test_terraform_plan.py
│   └── test_module_structure.py
│
├── scripts/                     ← Scripts de automatización
│   ├── deploy.sh                ← Despliegue automatizado
│   ├── destroy.sh               ← Destrucción segura
│   ├── validate_all.sh          ← Validación de todos los ambientes
│   └── generate_docs.sh         ← Auto-generación de documentación
│
├── docs/                        ← Documentación generada
│   ├── architecture.md
│   ├── cost-estimation.md
│   └── runbook.md
│
├── .tflint.hcl                  ← Configuración de linter
├── .pre-commit-config.yaml      ← Pre-commit hooks
└── pytest.ini                   ← Configuración de pytest
```

---

## 🚀 Quick Start

### Prerequisitos

```bash
# 1. Instalar herramientas
brew install terraform      # macOS
# o
choco install terraform     # Windows
# o
sudo apt-get install terraform  # Linux

# 2. Configurar AWS CLI
aws configure

# 3. Instalar Python dependencies
pip install -r requirements.txt

# 4. Instalar pre-commit hooks
pre-commit install
```

### Despliegue en Dev

```bash
# 1. Navegar a ambiente dev
cd terraform/environments/dev

# 2. Inicializar Terraform
terraform init

# 3. Ver plan de ejecución
terraform plan

# 4. Aplicar (crear infraestructura)
terraform apply

# 5. Ver outputs
terraform output
```

### Despliegue Automatizado

```bash
# Script automatizado con validaciones
./scripts/deploy.sh dev
```

---

## 🧪 Testing

Este proyecto incluye **tests automatizados** para validar la infraestructura:

### Test 1: Validación de Sintaxis

```bash
# Ejecutar tests
pytest tests/test_terraform_validate.py -v

# Output esperado:
# tests/test_terraform_validate.py::test_validate_dev PASSED
# tests/test_terraform_validate.py::test_validate_staging PASSED
# tests/test_terraform_validate.py::test_validate_prod PASSED
```

### Test 2: Formato de Código

```bash
pytest tests/test_terraform_format.py -v

# Output esperado:
# tests/test_terraform_format.py::test_format_check PASSED
```

### Test 3: Plan Sin Errores

```bash
pytest tests/test_terraform_plan.py -v

# Output esperado:
# tests/test_terraform_plan.py::test_plan_dev PASSED
```

### Test 4: Estructura de Módulos

```bash
pytest tests/test_module_structure.py -v

# Output esperado:
# tests/test_module_structure.py::test_data_lake_module_structure PASSED
# tests/test_module_structure.py::test_lambda_etl_module_structure PASSED
```

### Ejecutar Todos los Tests

```bash
pytest tests/ -v --tb=short

# O con cobertura
pytest tests/ --cov=terraform --cov-report=html
```

---

## 📊 Módulos Implementados

### 1. Data Lake Module

Crea 3 buckets S3 con lifecycle policies:
- `raw/`: Datos sin procesar (90 días → Glacier)
- `processed/`: Datos transformados (30 días → IA)
- `analytics/`: Resultados de análisis (365 días TTL)

**Variables**:
- `project_name`: Nombre del proyecto
- `environment`: dev, staging, prod
- `enable_encryption`: true/false
- `raw_retention_days`: 90
- `processed_retention_days`: 365

### 2. Lambda ETL Module

Función Lambda que:
- Se dispara automáticamente cuando se sube archivo a `raw/`
- Lee CSV, transforma a Parquet
- Escribe resultado en `processed/`
- Logs en CloudWatch

**Variables**:
- `function_name`: Nombre de la función
- `runtime`: python3.11
- `timeout`: 300
- `memory_size`: 512
- `source_bucket`: Bucket de input
- `destination_bucket`: Bucket de output

### 3. Networking Module

VPC con subnets público/privado:
- VPC: `10.0.0.0/16`
- Public subnet: `10.0.1.0/24`
- Private subnet: `10.0.2.0/24`
- NAT Gateway
- Internet Gateway
- Route tables

**Variables**:
- `vpc_cidr`: CIDR de VPC
- `public_subnet_cidrs`: Lista de CIDRs públicos
- `private_subnet_cidrs`: Lista de CIDRs privados

### 4. Glue Catalog Module

Catálogo de Glue con:
- Database: `data_lake_<environment>`
- Crawler: Auto-discovery de schemas
- Tables: `raw_data`, `processed_data`

**Variables**:
- `database_name`: Nombre del database
- `crawler_schedule`: cron expression
- `data_location`: S3 path para crawlear

---

## 💰 Cálculo de Costos

### Dev Environment (Estimado)

```
S3 Storage (50 GB total):
- Standard (10 GB nuevos/mes): $0.23
- IA (20 GB): $0.25
- Glacier (20 GB): $0.08
Total S3: $0.56/mes

Lambda (1000 invocaciones/mes):
- Free Tier cubre
Total Lambda: $0

Glue Crawler (1x/día):
- $0.44/hora * 0.1 hora/día * 30 días = $1.32
Total Glue: $1.32/mes

CloudWatch Logs (100 MB):
- $0.50/GB = $0.05
Total Logs: $0.05/mes

VPC (NAT Gateway):
- $0.045/hora * 730 horas = $32.85
Total NAT: $32.85/mes

════════════════════════════════════
TOTAL DEV: ~$35/mes
════════════════════════════════════

💡 Para reducir costos en dev:
- Usar NAT Instance en vez de NAT Gateway: ~$3/mes
- Desactivar crawler cuando no se use
- Usar lifecycle agresivo (30 días → Glacier)

Total Dev Optimizado: ~$5/mes
```

### Production Environment (Estimado)

```
S3 Storage (1 TB total):
- Standard (100 GB): $2.30
- IA (400 GB): $5.00
- Glacier (500 GB): $2.00
Total S3: $9.30/mes

Lambda (100K invocaciones/mes):
- Compute: $0.83
- Requests: $0.02
Total Lambda: $0.85/mes

Glue Crawler (2x/día):
- $0.44/hora * 0.2 hora/día * 30 días * 2 = $5.28
Total Glue: $5.28/mes

Athena Queries (1 TB escaneado):
- $5/TB = $5
Total Athena: $5/mes

NAT Gateway (High Availability, 2 AZs):
- $0.045/hora * 730 * 2 = $65.70
- Data processing: $0.045/GB * 100GB = $4.50
Total NAT: $70.20/mes

RDS PostgreSQL (t3.micro reserved):
- $12/mes (1 year upfront)

Total Prod: ~$107.63/mes (~$1,291/año)

Con Reserved Instances y Savings Plans:
Total Prod Optimizado: ~$75/mes (~$900/año)
```

---

## 🔒 Seguridad

### Buenas Prácticas Implementadas

1. **Encriptación**:
   - S3: Server-side encryption (SSE-S3 o SSE-KMS)
   - RDS: Encryption at rest
   - Lambda: Variables de entorno encriptadas

2. **IAM Least Privilege**:
   - Roles específicos por servicio
   - Policies con recursos explícitos (no `*`)
   - Sin credenciales hardcodeadas

3. **Networking**:
   - Lambda en VPC privada
   - RDS sin acceso público
   - Security groups restrictivos

4. **Secrets Management**:
   - AWS Secrets Manager para credenciales
   - No secrets en código
   - Rotación automática de secrets

5. **Logging y Monitoring**:
   - CloudWatch Logs para todas las funciones
   - CloudTrail para auditoría
   - Alarms para eventos críticos

---

## 📚 Comandos Útiles

### Terraform

```bash
# Validar sintaxis
terraform validate

# Formatear código
terraform fmt -recursive

# Ver plan detallado
terraform plan -out=tfplan

# Aplicar plan guardado
terraform apply tfplan

# Ver estado
terraform show

# Listar recursos
terraform state list

# Ver output específico
terraform output bucket_name

# Destruir infraestructura
terraform destroy

# Importar recurso existente
terraform import aws_s3_bucket.example my-bucket-name

# Refrescar estado
terraform refresh
```

### Testing

```bash
# Ejecutar test específico
pytest tests/test_terraform_validate.py::test_validate_dev -v

# Ejecutar con verbose
pytest tests/ -vv

# Ejecutar con coverage
pytest tests/ --cov=terraform --cov-report=html

# Ver coverage report
open htmlcov/index.html
```

### Linting

```bash
# Ejecutar tflint
tflint --init
tflint terraform/

# Ejecutar checkov (security scanner)
checkov -d terraform/

# Ejecutar terraform-docs
terraform-docs markdown terraform/modules/data-lake/
```

---

## 🚀 CI/CD Pipeline

El proyecto incluye GitHub Actions workflow para automatizar:

1. **On Pull Request**:
   - `terraform fmt -check`
   - `terraform validate`
   - `tflint`
   - `checkov`
   - `terraform plan`
   - Comentar plan en PR

2. **On Merge to Main**:
   - Deploy a `dev` automáticamente
   - Tag de versión
   - Crear release notes

3. **On Release Tag**:
   - Deploy a `staging`
   - Esperar aprobación manual
   - Deploy a `prod`
   - Notificar en Slack

Configuración en `.github/workflows/terraform.yml`

---

## 📖 Documentación

### Auto-generada

```bash
# Generar documentación de módulos
./scripts/generate_docs.sh

# Output en docs/
```

### Manual

- **Architecture**: `docs/architecture.md`
- **Cost Estimation**: `docs/cost-estimation.md`
- **Runbook**: `docs/runbook.md` (procedimientos operativos)

---

## 🎓 Aprendizajes Clave

Después de completar este proyecto, habrás aprendido:

1. ✅ **Terraform Basics**: Resources, variables, outputs, state
2. ✅ **Terraform Modules**: Código reutilizable y DRY
3. ✅ **Multi-Environment**: Workspaces, tfvars, backends
4. ✅ **Testing IaC**: pytest, terraform validate, tflint
5. ✅ **Security**: IAM, encryption, secrets management
6. ✅ **Cost Optimization**: Lifecycle policies, reserved instances
7. ✅ **CI/CD**: GitHub Actions, automated deployments
8. ✅ **Monitoring**: CloudWatch, alarms, dashboards
9. ✅ **Documentation**: Auto-generation, runbooks
10. ✅ **Best Practices**: Naming, tagging, versioning

---

## 🐛 Troubleshooting

### Error: "Backend initialization required"

```bash
terraform init -reconfigure
```

### Error: "Resource already exists"

```bash
# Importar recurso existente
terraform import aws_s3_bucket.raw my-existing-bucket
```

### Error: "Permission denied"

```bash
# Verificar credenciales AWS
aws sts get-caller-identity

# Re-configurar si es necesario
aws configure
```

### Error: "State lock"

```bash
# Forzar unlock (solo si estás seguro)
terraform force-unlock LOCK_ID
```

---

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📝 Licencia

Este proyecto es parte del **Master en Ingeniería de Datos con IA** y está disponible bajo licencia MIT.

---

## 📞 Soporte

- **Documentación**: Ver `docs/`
- **Issues**: GitHub Issues
- **Slack**: Canal #terraform-help

---

**¡Felicidades!** Has completado el proyecto de Infrastructure as Code. 🎉

Ahora tienes una infraestructura de Data Lake completa, testeada y lista para producción.
