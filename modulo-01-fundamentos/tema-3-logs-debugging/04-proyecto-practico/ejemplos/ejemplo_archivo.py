"""
Ejemplo de logging a archivo con rotación.

Este ejemplo muestra cómo configurar logging para escribir
en archivos con rotación automática.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logger_config import configurar_logger_archivo


def main():
    """Función principal del ejemplo."""
    # Crear directorio de logs si no existe
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Configurar logger con archivo
    logger = configurar_logger_archivo(
        nombre="ejemplo_archivo",
        ruta_archivo=str(logs_dir / "aplicacion.log"),
        nivel="DEBUG",
        max_bytes=1024 * 1024,  # 1 MB
        backup_count=3,
    )

    # Ejemplos de uso
    logger.debug("Mensaje de debug - útil para desarrollo")
    logger.info("Mensaje informativo - operación normal")
    logger.warning("Mensaje de advertencia - algo inusual pero no crítico")

    try:
        # Simular operación con error
        resultado = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Error matemático: {str(e)}")
        logger.exception("Detalles completos del error:")

    logger.critical("Mensaje crítico - requiere atención inmediata")

    print(f"\nLogs guardados en: {logs_dir / 'aplicacion.log'}")
    print("Abre el archivo para ver los logs detallados.")


if __name__ == "__main__":
    main()
