# Variables para módulo data-lake

variable "project_name" {
  description = "Nombre del proyecto (se usa como prefijo para buckets)"
  type        = string

  validation {
    condition     = length(var.project_name) > 3 && length(var.project_name) < 30
    error_message = "project_name debe tener entre 3 y 30 caracteres"
  }
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment debe ser: dev, staging o prod"
  }
}

variable "enable_encryption" {
  description = "Habilitar encriptación en buckets S3"
  type        = bool
  default     = true
}

variable "enable_versioning" {
  description = "Habilitar versionado en bucket RAW"
  type        = bool
  default     = false
}

variable "raw_retention_days" {
  description = "Días antes de mover datos RAW a Glacier"
  type        = number
  default     = 90

  validation {
    condition     = var.raw_retention_days >= 30 && var.raw_retention_days <= 730
    error_message = "raw_retention_days debe estar entre 30 y 730 días"
  }
}

variable "processed_retention_days" {
  description = "Días antes de mover datos PROCESSED a Glacier"
  type        = number
  default     = 90

  validation {
    condition     = var.processed_retention_days >= 30 && var.processed_retention_days <= 730
    error_message = "processed_retention_days debe estar entre 30 y 730 días"
  }
}

variable "common_tags" {
  description = "Tags comunes para todos los recursos"
  type        = map(string)
  default = {
    ManagedBy = "Terraform"
    Project   = "DataLake"
  }
}
