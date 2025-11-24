# Valores de variables para ambiente staging

# IMPORTANTE: Cambiar este valor a un nombre único
project_name = "data-lake-demo"

# Region AWS
aws_region = "us-east-1"

# Configuración de staging (balance costo/seguridad)
enable_encryption = true   # Activado en staging
enable_versioning = false  # No crítico en staging
raw_retention_days = 60    # Retención media
processed_retention_days = 60

# Tags adicionales
common_tags = {
  Team        = "DataEngineering"
  Environment = "staging"
  ManagedBy   = "Terraform"
  CostCenter  = "Development"
}
