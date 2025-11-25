# Configuración del backend remoto (comentado por defecto)
# Descomentar y configurar cuando estés listo para usar S3 como backend

# terraform {
#   backend "s3" {
#     bucket         = "terraform-state-YOUR-PROJECT"
#     key            = "data-lake/dev/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "terraform-locks"
#     encrypt        = true
#   }
# }

# Para empezar, Terraform usará backend local (terraform.tfstate en este directorio)
