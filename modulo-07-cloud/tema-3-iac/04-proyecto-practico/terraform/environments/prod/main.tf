# Configuración de Terraform
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider AWS
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
      Workspace   = terraform.workspace
    }
  }
}

# Módulo Data Lake
module "data_lake" {
  source = "../../modules/data-lake"

  project_name             = var.project_name
  environment              = var.environment
  enable_encryption        = var.enable_encryption
  enable_versioning        = var.enable_versioning
  raw_retention_days       = var.raw_retention_days
  processed_retention_days = var.processed_retention_days

  common_tags = var.common_tags
}

# Outputs
output "raw_bucket" {
  description = "Bucket de datos RAW"
  value       = module.data_lake.raw_bucket_name
}

output "processed_bucket" {
  description = "Bucket de datos PROCESSED"
  value       = module.data_lake.processed_bucket_name
}

output "analytics_bucket" {
  description = "Bucket de datos ANALYTICS"
  value       = module.data_lake.analytics_bucket_name
}

output "all_buckets" {
  description = "Todos los buckets creados"
  value       = module.data_lake.all_bucket_names
}
