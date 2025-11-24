# Outputs del módulo data-lake

output "raw_bucket_name" {
  description = "Nombre del bucket de datos RAW"
  value       = aws_s3_bucket.raw.id
}

output "raw_bucket_arn" {
  description = "ARN del bucket de datos RAW"
  value       = aws_s3_bucket.raw.arn
}

output "processed_bucket_name" {
  description = "Nombre del bucket de datos PROCESSED"
  value       = aws_s3_bucket.processed.id
}

output "processed_bucket_arn" {
  description = "ARN del bucket de datos PROCESSED"
  value       = aws_s3_bucket.processed.arn
}

output "analytics_bucket_name" {
  description = "Nombre del bucket de datos ANALYTICS"
  value       = aws_s3_bucket.analytics.id
}

output "analytics_bucket_arn" {
  description = "ARN del bucket de datos ANALYTICS"
  value       = aws_s3_bucket.analytics.arn
}

output "all_bucket_names" {
  description = "Lista de todos los buckets creados"
  value = [
    aws_s3_bucket.raw.id,
    aws_s3_bucket.processed.id,
    aws_s3_bucket.analytics.id
  ]
}
