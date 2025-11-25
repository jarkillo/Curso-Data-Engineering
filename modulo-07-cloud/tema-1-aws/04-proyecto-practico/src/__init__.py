"""
Pipeline ETL Serverless en AWS - Módulo 7: Cloud Computing

Este paquete implementa un pipeline completo de Data Engineering
en AWS usando servicios serverless:
- Amazon S3 para almacenamiento
- AWS Lambda para procesamiento serverless
- AWS Glue para transformaciones ETL
- Amazon Athena para análisis SQL
- IAM para seguridad

Empresa ficticia: CloudAPI Systems
"""

__version__ = "1.0.0"
__author__ = "Master en Ingeniería de Datos con IA"

from src.athena_queries import generar_query_metricas_basicas, generar_query_percentiles

# Importar funciones principales para acceso directo
from src.config import cargar_configuracion, obtener_ruta_proyecto
from src.glue_transformations import (
    agregar_columna_fecha,
    calcular_metricas_por_endpoint,
    limpiar_nulls,
)
from src.iam_utils import generar_policy_lambda_s3, validar_permisos_s3
from src.lambda_handler import lambda_handler
from src.s3_operations import (
    descargar_archivo_s3,
    listar_objetos_s3,
    subir_archivo_a_s3,
)
from src.validation import validar_log_api, validar_lote_logs

__all__ = [
    # Config
    "cargar_configuracion",
    "obtener_ruta_proyecto",
    # Validation
    "validar_log_api",
    "validar_lote_logs",
    # S3
    "subir_archivo_a_s3",
    "descargar_archivo_s3",
    "listar_objetos_s3",
    # Lambda
    "lambda_handler",
    # Glue
    "limpiar_nulls",
    "calcular_metricas_por_endpoint",
    "agregar_columna_fecha",
    # Athena
    "generar_query_metricas_basicas",
    "generar_query_percentiles",
    # IAM
    "validar_permisos_s3",
    "generar_policy_lambda_s3",
]
