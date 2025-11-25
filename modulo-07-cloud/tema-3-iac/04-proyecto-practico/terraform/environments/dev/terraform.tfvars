# Valores de variables para ambiente dev

# IMPORTANTE: Cambiar este valor a un nombre único
project_name = "data-lake-demo"

# Region AWS
aws_region = "us-east-1"

# Configuración de desarrollo (costos reducidos)
enable_encryption = false
enable_versioning = false
raw_retention_days = 30
processed_retention_days = 30

# Tags adicionales
common_tags = {
  Team        = "DataEngineering"
  Environment = "dev"
  ManagedBy   = "Terraform"
  CostCenter  = "Development"
}
