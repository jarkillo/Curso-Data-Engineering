"""
Sistema de Evaluación y Certificación
Master en Ingeniería de Datos con IA

Este paquete proporciona:
- Exámenes por módulo (10-15 preguntas cada uno)
- Sistema de puntuación (>70% para aprobar)
- Generación de certificados PDF
- Tracking de progreso del estudiante
"""

from evaluaciones.generar_certificado import crear_certificado, verificar_certificado
from evaluaciones.tracking_progreso import (
    calcular_nota_media,
    cargar_progreso,
    generar_dashboard,
    guardar_progreso,
    puede_obtener_certificado,
    registrar_examen,
)

__all__ = [
    "crear_certificado",
    "verificar_certificado",
    "cargar_progreso",
    "guardar_progreso",
    "registrar_examen",
    "calcular_nota_media",
    "puede_obtener_certificado",
    "generar_dashboard",
]

__version__ = "1.0.0"
