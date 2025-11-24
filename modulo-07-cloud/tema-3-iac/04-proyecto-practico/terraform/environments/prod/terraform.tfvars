# Valores de variables para ambiente producción

# IMPORTANTE: Cambiar este valor a un nombre único
project_name = "data-lake-demo"

# Region AWS
aws_region = "us-east-1"

# Configuración de producción (máxima seguridad y compliance)
enable_encryption = true   # OBLIGATORIO en producción
enable_versioning = true   # OBLIGATORIO para compliance
raw_retention_days = 365   # Retención larga (1 año)
processed_retention_days = 365

# Tags adicionales (incluye compliance y criticidad)
common_tags = {
  Team        = "DataEngineering"
  Environment = "production"
  ManagedBy   = "Terraform"
  CostCenter  = "Production"
  Criticality = "High"
  Compliance  = "Required"
}
