"""
Ejemplo básico de uso de logging.

Este ejemplo muestra cómo configurar y usar un logger básico
para una aplicación simple.
"""

import sys
import os

# Añadir el directorio padre al path para poder importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logger_config import configurar_logger


def main():
    """Función principal del ejemplo."""
    # Configurar logger
    logger = configurar_logger("ejemplo_basico", "INFO")

    # Ejemplos de uso de diferentes niveles
    logger.info("Aplicación iniciada")
    logger.debug("Este mensaje no se verá porque el nivel es INFO")

    # Simular procesamiento
    logger.info("Procesando datos...")

    try:
        # Simular operación exitosa
        resultado = 42
        logger.info(f"Operación completada exitosamente. Resultado: {resultado}")

    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")

    logger.info("Aplicación finalizada")


if __name__ == "__main__":
    main()
