"""
Ejemplo de validación de datos CSV.

Este ejemplo muestra cómo validar datos CSV según reglas de negocio.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lector_csv import leer_csv
from src.validador_csv import validar_fila, validar_headers


def main():
    """Ejemplo de validación de datos CSV."""
    print("=" * 60)
    print("EJEMPLO: Validación de Datos CSV")
    print("=" * 60)
    print()

    # Ruta al archivo de muestra
    archivo = Path(__file__).parent.parent / "datos" / "muestra.csv"

    # 1. Validar headers
    print("1. Validando headers:")
    print("-" * 60)
    headers_esperados = ["nombre", "edad", "ciudad", "profesion"]

    if validar_headers(str(archivo), headers_esperados):
        print("   ✅ Headers correctos")
    else:
        print("   ❌ Headers incorrectos")
    print()

    # 2. Leer datos
    datos = leer_csv(str(archivo))

    # 3. Validar cada fila
    print("2. Validando filas:")
    print("-" * 60)

    validaciones = {
        "nombre": str,
        "edad": int,
        "ciudad": str,
        "profesion": str
    }

    filas_validas = 0
    filas_invalidas = 0

    for i, fila in enumerate(datos, 1):
        errores = validar_fila(fila, validaciones)

        if errores:
            filas_invalidas += 1
            print(f"   ❌ Fila {i}: {', '.join(errores)}")
        else:
            filas_validas += 1

    print()
    print("3. Resumen de validación:")
    print("-" * 60)
    print(f"   Filas válidas: {filas_validas}")
    print(f"   Filas inválidas: {filas_invalidas}")
    print(f"   Porcentaje de calidad: {(filas_validas / len(datos) * 100):.1f}%")
    print()

    if filas_invalidas == 0:
        print("✅ Todos los datos son válidos")
    else:
        print(f"⚠️ Se encontraron {filas_invalidas} filas con errores")


if __name__ == "__main__":
    main()
