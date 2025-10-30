"""
Sistema de Extracción Multi-Fuente

Este paquete proporciona herramientas robustas para extraer datos de múltiples fuentes:
- Archivos (CSV, JSON, Excel)
- APIs REST
- Web Scraping

Todos los módulos siguen principios de Data Engineering profesional:
- Manejo robusto de errores
- Logging completo
- Validación de datos
- Código testeado (>85% cobertura)
"""

__version__ = "1.0.0"
__author__ = "DataFlow Inc."

# Imports principales para facilitar el uso
# (Se irán agregando conforme se implementen los módulos)
from .extractor_archivos import (
    convertir_formato_archivo,
    detectar_encoding_archivo,
    leer_csv_con_encoding_auto,
    leer_excel_multiple_sheets,
    leer_json_nested,
    validar_estructura_archivo,
)

__all__ = [
    # Archivos
    "leer_csv_con_encoding_auto",
    "leer_json_nested",
    "leer_excel_multiple_sheets",
    "detectar_encoding_archivo",
    "validar_estructura_archivo",
    "convertir_formato_archivo",
]
