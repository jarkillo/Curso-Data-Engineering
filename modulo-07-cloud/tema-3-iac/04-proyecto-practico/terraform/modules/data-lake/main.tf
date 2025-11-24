# Módulo: Data Lake
# Crea 3 buckets S3 con lifecycle policies para optimización de costos

# Bucket RAW - Datos sin procesar
resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-raw-${var.environment}"

  tags = merge(
    var.common_tags,
    {
      Name  = "Raw Data Bucket"
      Layer = "raw"
    }
  )
}

# Lifecycle policy para bucket RAW
resource "aws_s3_bucket_lifecycle_configuration" "raw_lifecycle" {
  bucket = aws_s3_bucket.raw.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = var.raw_retention_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.raw_retention_days * 10
    }
  }
}

# Versionado para bucket RAW (opcional)
resource "aws_s3_bucket_versioning" "raw_versioning" {
  count  = var.enable_versioning ? 1 : 0
  bucket = aws_s3_bucket.raw.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encriptación para bucket RAW
resource "aws_s3_bucket_server_side_encryption_configuration" "raw_encryption" {
  count  = var.enable_encryption ? 1 : 0
  bucket = aws_s3_bucket.raw.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Bucket PROCESSED - Datos procesados
resource "aws_s3_bucket" "processed" {
  bucket = "${var.project_name}-processed-${var.environment}"

  tags = merge(
    var.common_tags,
    {
      Name  = "Processed Data Bucket"
      Layer = "processed"
    }
  )
}

# Lifecycle policy para bucket PROCESSED
resource "aws_s3_bucket_lifecycle_configuration" "processed_lifecycle" {
  bucket = aws_s3_bucket.processed.id

  rule {
    id     = "optimize-storage"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = var.processed_retention_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.processed_retention_days * 2
    }
  }
}

# Encriptación para bucket PROCESSED
resource "aws_s3_bucket_server_side_encryption_configuration" "processed_encryption" {
  count  = var.enable_encryption ? 1 : 0
  bucket = aws_s3_bucket.processed.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Bucket ANALYTICS - Resultados de análisis
resource "aws_s3_bucket" "analytics" {
  bucket = "${var.project_name}-analytics-${var.environment}"

  tags = merge(
    var.common_tags,
    {
      Name  = "Analytics Data Bucket"
      Layer = "analytics"
    }
  )
}

# Lifecycle policy para bucket ANALYTICS (corto plazo)
resource "aws_s3_bucket_lifecycle_configuration" "analytics_lifecycle" {
  bucket = aws_s3_bucket.analytics.id

  rule {
    id     = "cleanup-analytics"
    status = "Enabled"

    expiration {
      days = 365
    }
  }
}

# Encriptación para bucket ANALYTICS
resource "aws_s3_bucket_server_side_encryption_configuration" "analytics_encryption" {
  count  = var.enable_encryption ? 1 : 0
  bucket = aws_s3_bucket.analytics.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
