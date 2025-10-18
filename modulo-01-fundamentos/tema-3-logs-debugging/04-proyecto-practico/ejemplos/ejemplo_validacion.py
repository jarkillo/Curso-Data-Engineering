"""
Ejemplo de validación de datos con logging.

Este ejemplo muestra cómo validar datos con logging detallado
de errores y advertencias.
"""

import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline_logs import validar_datos_con_logs
from src.logger_config import configurar_logger


def main():
    """Función principal del ejemplo."""
    print("=" * 60)
    print("Ejemplo: Validación de Datos con Logging")
    print("=" * 60)

    # Configurar logger
    logger = configurar_logger("validacion_ejemplo", "INFO")

    # Datos de ejemplo (algunos válidos, algunos inválidos)
    datos = [
        {"id": "1", "nombre": "Juan Pérez", "edad": "25", "email": "juan@example.com"},
        {
            "id": "2",
            "nombre": "María García",
            "edad": "30",
            "email": "maria@example.com",
        },
        {
            "id": "3",
            "nombre": "",  # Nombre vacío - INVÁLIDO
            "edad": "28",
            "email": "pedro@example.com",
        },
        {
            "id": "4",
            "nombre": "Ana López",
            "edad": "-5",  # Edad negativa - INVÁLIDO
            "email": "ana@example.com",
        },
        {
            "id": "5",
            "nombre": "Carlos Ruiz",
            "edad": "35",
            "email": "carlos-sin-arroba.com",  # Email inválido - INVÁLIDO
        },
        {
            "id": "6",
            "nombre": "Laura Martínez",
            "edad": "22",
            "email": "laura@example.com",
        },
    ]

    print(f"\nValidando {len(datos)} registros...\n")

    # Validar datos
    resultado = validar_datos_con_logs(
        datos, campos_requeridos=["id", "nombre", "edad", "email"], logger=logger
    )

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DE LA VALIDACIÓN")
    print("=" * 60)
    print(f"Total de registros: {resultado['total']}")
    print(f"Registros válidos: {resultado['validos']}")
    print(f"Registros inválidos: {resultado['invalidos']}")
    print(f"Porcentaje de éxito: {resultado['porcentaje_validos']:.1f}%")

    if resultado["errores"]:
        print("\nErrores encontrados:")
        for error in resultado["errores"]:
            print(f"  - {error}")

    print("=" * 60)


if __name__ == "__main__":
    main()
