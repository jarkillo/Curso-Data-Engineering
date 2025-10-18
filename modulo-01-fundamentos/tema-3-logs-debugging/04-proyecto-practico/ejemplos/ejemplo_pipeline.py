"""
Ejemplo de pipeline ETL con logging integrado.

Este ejemplo muestra cómo usar logging en un pipeline ETL real
para procesar archivos CSV.
"""

import sys
import os
import csv
from pathlib import Path

# Añadir el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline_logs import procesar_con_logs
from src.logger_config import configurar_logger


def crear_archivo_ejemplo():
    """Crea un archivo CSV de ejemplo para procesar."""
    datos_dir = Path(__file__).parent.parent / "datos"
    datos_dir.mkdir(exist_ok=True)

    archivo = datos_dir / "ventas_ejemplo.csv"

    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "producto", "precio", "cantidad", "fecha"]
        )
        writer.writeheader()
        writer.writerow(
            {
                "id": "1",
                "producto": "Laptop",
                "precio": "1200",
                "cantidad": "2",
                "fecha": "2025-10-18",
            }
        )
        writer.writerow(
            {
                "id": "2",
                "producto": "Mouse",
                "precio": "25",
                "cantidad": "10",
                "fecha": "2025-10-18",
            }
        )
        writer.writerow(
            {
                "id": "3",
                "producto": "Teclado",
                "precio": "75",
                "cantidad": "5",
                "fecha": "2025-10-18",
            }
        )
        writer.writerow(
            {
                "id": "4",
                "producto": "Monitor",
                "precio": "300",
                "cantidad": "3",
                "fecha": "2025-10-18",
            }
        )

    return str(archivo)


def main():
    """Función principal del ejemplo."""
    print("=" * 60)
    print("Ejemplo: Pipeline ETL con Logging")
    print("=" * 60)

    # Crear archivo de ejemplo
    archivo = crear_archivo_ejemplo()
    print(f"\nArchivo creado: {archivo}")

    # Configurar logger personalizado (opcional)
    logger = configurar_logger("pipeline_ejemplo", "INFO")

    # Procesar archivo con logs
    print("\n--- Procesando archivo ---\n")
    resultado = procesar_con_logs(archivo, logger=logger)

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DEL PROCESAMIENTO")
    print("=" * 60)
    print(f"Total de registros: {resultado['total_registros']}")
    print(f"Registros procesados: {resultado['registros_procesados']}")
    print(f"Registros con error: {resultado['registros_con_error']}")
    print(f"Tiempo de procesamiento: {resultado['tiempo_procesamiento']:.3f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
