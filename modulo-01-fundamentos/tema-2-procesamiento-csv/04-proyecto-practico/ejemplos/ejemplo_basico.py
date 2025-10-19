"""
Ejemplo básico de uso del procesador CSV.

Este ejemplo muestra cómo leer, procesar y escribir archivos CSV.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lector_csv import leer_csv
from src.escritor_csv import escribir_csv
from src.utilidades import contar_filas, obtener_headers


def main():
    """Ejemplo básico de lectura y escritura de CSV."""
    print("=" * 60)
    print("EJEMPLO BÁSICO: Lectura y Escritura de CSV")
    print("=" * 60)
    print()

    # Ruta al archivo de muestra
    archivo_entrada = Path(__file__).parent.parent / "datos" / "muestra.csv"

    # 1. Obtener información del archivo
    print("1. Información del archivo:")
    print("-" * 60)
    headers = obtener_headers(str(archivo_entrada))
    num_filas = contar_filas(str(archivo_entrada))

    print(f"   Archivo: {archivo_entrada.name}")
    print(f"   Headers: {', '.join(headers)}")
    print(f"   Número de filas: {num_filas}")
    print()

    # 2. Leer el archivo
    print("2. Leyendo datos:")
    print("-" * 60)
    datos = leer_csv(str(archivo_entrada))

    for i, fila in enumerate(datos, 1):
        print(f"   Fila {i}: {fila['nombre']}, {fila['edad']} años, {fila['ciudad']}")
    print()

    # 3. Filtrar datos (solo personas de Madrid)
    print("3. Filtrando personas de Madrid:")
    print("-" * 60)
    personas_madrid = [fila for fila in datos if fila["ciudad"] == "Madrid"]

    for fila in personas_madrid:
        print(f"   - {fila['nombre']}: {fila['profesion']}")
    print()

    # 4. Escribir resultado en nuevo archivo
    archivo_salida = Path(__file__).parent.parent / "datos" / "madrid.csv"
    escribir_csv(personas_madrid, str(archivo_salida))

    print(f"4. Resultado guardado en: {archivo_salida.name}")
    print()

    print("✅ Ejemplo completado exitosamente")


if __name__ == "__main__":
    main()
