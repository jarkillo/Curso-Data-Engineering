"""
Ejemplo de pipeline completo de procesamiento CSV.

Este ejemplo muestra cómo combinar múltiples operaciones:
lectura, validación, transformación y escritura.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lector_csv import leer_csv
from src.escritor_csv import escribir_csv
from src.validador_csv import validar_fila
from src.transformador_csv import filtrar_filas, agregar_columna


def main():
    """Pipeline completo de procesamiento CSV."""
    print("=" * 60)
    print("EJEMPLO: Pipeline Completo de Procesamiento CSV")
    print("=" * 60)
    print()

    # Ruta al archivo de muestra
    archivo_entrada = Path(__file__).parent.parent / "datos" / "muestra.csv"

    # FASE 1: EXTRACT (Leer datos)
    print("FASE 1: EXTRACT - Leyendo datos...")
    print("-" * 60)
    datos = leer_csv(str(archivo_entrada))
    print(f"   ✅ {len(datos)} filas leídas")
    print()

    # FASE 2: VALIDATE (Validar datos)
    print("FASE 2: VALIDATE - Validando datos...")
    print("-" * 60)
    validaciones = {
        "nombre": str,
        "edad": int,
        "ciudad": str,
        "profesion": str
    }

    datos_validos = []
    datos_invalidos = []

    for fila in datos:
        errores = validar_fila(fila, validaciones)
        if errores:
            datos_invalidos.append(fila)
        else:
            datos_validos.append(fila)

    print(f"   ✅ {len(datos_validos)} filas válidas")
    print(f"   ⚠️ {len(datos_invalidos)} filas inválidas")
    print()

    # FASE 3: TRANSFORM (Transformar datos)
    print("FASE 3: TRANSFORM - Transformando datos...")
    print("-" * 60)

    # 3.1. Filtrar personas mayores de 26 años
    datos_filtrados = filtrar_filas(
        datos_validos,
        lambda fila: int(fila["edad"]) > 26
    )
    print(f"   ✅ Filtradas {len(datos_filtrados)} personas > 26 años")

    # 3.2. Agregar columna "mayor_edad"
    datos_transformados = agregar_columna(
        datos_filtrados,
        "mayor_edad",
        lambda fila: "Sí" if int(fila["edad"]) >= 18 else "No"
    )
    print(f"   ✅ Añadida columna 'mayor_edad'")

    # 3.3. Agregar columna "rango_edad"
    datos_transformados = agregar_columna(
        datos_transformados,
        "rango_edad",
        lambda fila: (
            "Joven" if int(fila["edad"]) < 30
            else "Adulto" if int(fila["edad"]) < 50
            else "Senior"
        )
    )
    print(f"   ✅ Añadida columna 'rango_edad'")
    print()

    # FASE 4: LOAD (Guardar resultados)
    print("FASE 4: LOAD - Guardando resultados...")
    print("-" * 60)

    archivo_salida = Path(__file__).parent.parent / "datos" / "procesado.csv"
    escribir_csv(datos_transformados, str(archivo_salida))
    print(f"   ✅ Datos guardados en: {archivo_salida.name}")
    print()

    # Mostrar muestra de datos procesados
    print("MUESTRA DE DATOS PROCESADOS:")
    print("-" * 60)
    for fila in datos_transformados[:3]:
        print(f"   {fila['nombre']}: {fila['edad']} años, {fila['rango_edad']}")
    print()

    print("✅ Pipeline completado exitosamente")


if __name__ == "__main__":
    main()
