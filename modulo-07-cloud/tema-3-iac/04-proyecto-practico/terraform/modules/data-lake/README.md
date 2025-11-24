# Módulo: Data Lake

## Descripción

Este módulo crea un Data Lake completo en AWS S3 con 3 capas:

- **RAW**: Datos sin procesar
- **PROCESSED**: Datos transformados
- **ANALYTICS**: Resultados de análisis

Incluye lifecycle policies para optimizar costos automáticamente.

---

## Recursos Creados

- 3 buckets S3 (raw, processed, analytics)
- Lifecycle policies para cada bucket
- Encriptación (opcional)
- Versionado en bucket RAW (opcional)

---

## Uso

```hcl
module "data_lake" {
  source = "../../modules/data-lake"

  project_name             = "mi-proyecto"
  environment              = "dev"
  enable_encryption        = true
  enable_versioning        = false
  raw_retention_days       = 90
  processed_retention_days = 90

  common_tags = {
    Team      = "Data Engineering"
    CostCenter = "Analytics"
    ManagedBy  = "Terraform"
  }
}
```

---

## Variables

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `project_name` | string | (requerido) | Nombre del proyecto |
| `environment` | string | (requerido) | Ambiente: dev, staging, prod |
| `enable_encryption` | bool | true | Habilitar encriptación S3 |
| `enable_versioning` | bool | false | Habilitar versionado en RAW |
| `raw_retention_days` | number | 90 | Días antes de mover a Glacier |
| `processed_retention_days` | number | 90 | Días antes de mover a Glacier |
| `common_tags` | map(string) | {...} | Tags comunes para recursos |

---

## Outputs

| Output | Descripción |
|--------|-------------|
| `raw_bucket_name` | Nombre del bucket RAW |
| `raw_bucket_arn` | ARN del bucket RAW |
| `processed_bucket_name` | Nombre del bucket PROCESSED |
| `processed_bucket_arn` | ARN del bucket PROCESSED |
| `analytics_bucket_name` | Nombre del bucket ANALYTICS |
| `analytics_bucket_arn` | ARN del bucket ANALYTICS |
| `all_bucket_names` | Lista de todos los buckets |

---

## Lifecycle Policies

### Bucket RAW

```
0-90 días: S3 Standard
90+ días: Glacier
900+ días: Eliminado
```

### Bucket PROCESSED

```
0-30 días: S3 Standard
30-90 días: S3 IA
90+ días: Glacier
180+ días: Eliminado
```

### Bucket ANALYTICS

```
0-365 días: S3 Standard
365+ días: Eliminado
```

---

## Costo Estimado

**Escenario**: 100 GB nuevos por mes

```
Mes 1:
- S3 Standard (100 GB): $2.30
Total: $2.30/mes

Mes 4 (con lifecycle):
- S3 Standard (100 GB nuevos): $2.30
- S3 IA (200 GB antiguos): $2.50
Total: $4.80/mes

Mes 12 (optimizado):
- S3 Standard (100 GB recientes): $2.30
- S3 IA (300 GB 1-3 meses): $3.75
- Glacier (600 GB >3 meses): $2.40
Total: $8.45/mes

SIN lifecycle: $27.60/mes (1.2 TB * $0.023)
CON lifecycle: $8.45/mes

💰 AHORRO: 69% ($19.15/mes = $230/año)
```

---

## Ejemplos

### Ejemplo 1: Desarrollo

```hcl
module "data_lake_dev" {
  source = "./modules/data-lake"

  project_name             = "my-app"
  environment              = "dev"
  enable_encryption        = false  # No crítico en dev
  enable_versioning        = false
  raw_retention_days       = 30     # Retención corta en dev
  processed_retention_days = 30
}
```

### Ejemplo 2: Producción

```hcl
module "data_lake_prod" {
  source = "./modules/data-lake"

  project_name             = "my-app"
  environment              = "prod"
  enable_encryption        = true   # Siempre en prod
  enable_versioning        = true   # Para compliance
  raw_retention_days       = 365    # Retención larga
  processed_retention_days = 365

  common_tags = {
    Compliance = "SOC2"
    DataClass  = "Confidential"
    ManagedBy  = "Terraform"
  }
}
```

---

## Testing

```bash
# Validar sintaxis
terraform validate

# Ver plan
terraform plan

# Aplicar
terraform apply
```

---

## Notas

- Los nombres de buckets deben ser únicos globalmente en AWS
- Si el proyecto ya tiene buckets con estos nombres, el apply fallará
- Para destruir, ejecutar `terraform destroy`
- Los buckets con datos NO se eliminarán automáticamente (force_destroy = false)
