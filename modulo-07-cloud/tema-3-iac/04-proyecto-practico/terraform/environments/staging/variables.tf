# Variables para ambiente dev

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente (siempre dev para este directorio)"
  type        = string
  default     = "dev"
}

variable "enable_encryption" {
  description = "Habilitar encriptación"
  type        = bool
  default     = false  # En dev podemos desactivar para reducir costos
}

variable "enable_versioning" {
  description = "Habilitar versionado"
  type        = bool
  default     = false
}

variable "raw_retention_days" {
  description = "Días de retención para datos RAW"
  type        = number
  default     = 30  # En dev, retención corta
}

variable "processed_retention_days" {
  description = "Días de retención para datos PROCESSED"
  type        = number
  default     = 30
}

variable "common_tags" {
  description = "Tags comunes"
  type        = map(string)
  default = {
    Team      = "DataEngineering"
    ManagedBy = "Terraform"
  }
}
