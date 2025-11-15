"""
Ejemplo de pipeline completo de conversión entre formatos.

Demuestra el uso de todas las funciones del conversor multi-formato.
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from src.analizador_formatos import (
    benchmark_lectura_escritura,
    comparar_tamanios_formatos,
    generar_reporte_formato,
)
from src.conversor_formatos import (
    convertir_con_particiones,
    convertir_csv_a_parquet,
    guardar_formato_automatico,
    leer_multiple_formatos,
)
from src.gestor_compresion import comparar_compresiones


def generar_datos_ejemplo() -> pd.DataFrame:
    """Genera datos de ejemplo para demostración."""
    np.random.seed(42)

    df = pd.DataFrame(
        {
            "id": range(1, 1001),
            "fecha": pd.date_range("2024-01-01", periods=1000, freq="H"),
            "producto": np.random.choice(
                ["Laptop", "Mouse", "Teclado", "Monitor"], 1000
            ),
            "cantidad": np.random.randint(1, 10, 1000),
            "precio": np.round(np.random.uniform(10, 1000, 1000), 2),
        }
    )

    return df


def ejemplo_1_conversiones_basicas():
    """Ejemplo 1: Conversiones básicas entre formatos."""
    print("=" * 70)
    print("EJEMPLO 1: Conversiones Básicas")
    print("=" * 70)

    # Generar datos
    df = generar_datos_ejemplo()
    print(f"\n📊 Generados {len(df):,} registros")

    # Guardar en CSV
    df.to_csv("datos.csv", index=False)
    print("✅ Guardado como CSV")

    # Convertir CSV → Parquet
    convertir_csv_a_parquet("datos.csv", "datos.parquet", compresion="snappy")
    print("✅ Convertido CSV → Parquet")

    # Leer con autodetección
    df_parquet = leer_multiple_formatos("datos.parquet")
    print(f"✅ Leído Parquet: {len(df_parquet):,} registros")

    # Guardar en JSON Lines
    guardar_formato_automatico(df, "datos.jsonl")
    print("✅ Guardado como JSON Lines")


def ejemplo_2_comparacion_formatos():
    """Ejemplo 2: Comparación de tamaños y velocidades."""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Comparación de Formatos")
    print("=" * 70)

    # Generar datos
    df = generar_datos_ejemplo()

    # Comparar tamaños
    print("\n📊 Comparación de tamaños:")
    tamanios = comparar_tamanios_formatos(df)

    for formato, tamanio in tamanios.items():
        print(f"   {formato:20s}: {tamanio:8.2f} KB")

    # Benchmark lectura/escritura
    print("\n⏱️  Benchmark lectura/escritura:")
    benchmark = benchmark_lectura_escritura(df, ["csv", "parquet"])
    print(benchmark.to_string(index=False))


def ejemplo_3_compresion():
    """Ejemplo 3: Comparación de algoritmos de compresión."""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Comparación de Compresión")
    print("=" * 70)

    # Generar datos y guardar CSV
    df = generar_datos_ejemplo()
    df.to_csv("datos_grandes.csv", index=False)

    # Comparar algoritmos
    print("\n🗜️  Comparando algoritmos de compresión...")
    resultados = comparar_compresiones("datos_grandes.csv", ["gzip", "bz2", "xz"])

    print("\nResultados:")
    for algoritmo, metricas in resultados.items():
        print(f"\n{algoritmo.upper()}:")
        print(f"   Original:    {metricas['tamanio_original_kb']:8.2f} KB")
        print(f"   Comprimido:  {metricas['tamanio_comprimido_kb']:8.2f} KB")
        print(f"   Ratio:       {metricas['ratio_compresion']:8.2f}x")
        print(f"   Reducción:   {metricas['reduccion_pct']:8.1f}%")
        print(f"   Tiempo:      {metricas['tiempo_compresion_s']:8.4f}s")


def ejemplo_4_particionamiento():
    """Ejemplo 4: Guardado con particiones."""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Particionamiento de Datos")
    print("=" * 70)

    # Generar datos con fechas
    df = generar_datos_ejemplo()

    # Añadir columnas de partición
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month

    print(f"\n📊 Guardando {len(df):,} registros particionados...")

    # Guardar particionado
    convertir_con_particiones(df, "datos_particionado", ["año", "mes"])

    # Contar particiones
    particiones = list(Path("datos_particionado").rglob("*.parquet"))
    print(f"✅ Creadas {len(particiones)} particiones")

    # Leer partición específica
    df_filtrado = pd.read_parquet("datos_particionado", filters=[("mes", "==", 1)])
    print(f"✅ Leída partición mes=1: {len(df_filtrado):,} registros")


def ejemplo_5_reporte():
    """Ejemplo 5: Generación de reportes."""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Reporte de Formato")
    print("=" * 70)

    # Generar datos y guardar
    df = generar_datos_ejemplo()
    df.to_parquet("datos_final.parquet", compression="snappy", index=False)

    # Generar reporte
    print("\n📊 Generando reporte del archivo...")
    reporte = generar_reporte_formato("datos_final.parquet")

    print("\n📄 REPORTE:")
    print(f"   Formato:     {reporte['formato']}")
    print(f"   Tamaño:      {reporte['tamanio_mb']} MB")
    print(f"   Registros:   {reporte['num_registros']:,}")
    print(f"   Columnas:    {reporte['num_columnas']}")
    print(f"   Columnas:    {', '.join(reporte['columnas'])}")

    if "compresion" in reporte:
        print(f"   Compresión:  {reporte['compresion']}")


def limpiar_archivos():
    """Limpia archivos temporales generados."""
    import os
    import shutil

    print("\n" + "=" * 70)
    print("🧹 Limpiando archivos temporales...")

    archivos = [
        "datos.csv",
        "datos.parquet",
        "datos.jsonl",
        "datos_grandes.csv",
        "datos_final.parquet",
    ]

    for archivo in archivos:
        try:
            if os.path.exists(archivo):
                os.remove(archivo)
        except OSError:
            pass

    # Limpiar directorios
    directorios = ["datos_particionado"]

    for directorio in directorios:
        try:
            if os.path.exists(directorio):
                shutil.rmtree(directorio)
        except OSError:
            pass

    print("✅ Limpieza completada")


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "=" * 70)
    print("🚀 PIPELINE COMPLETO DE CONVERSIÓN MULTI-FORMATO")
    print("=" * 70)

    try:
        ejemplo_1_conversiones_basicas()
        ejemplo_2_comparacion_formatos()
        ejemplo_3_compresion()
        ejemplo_4_particionamiento()
        ejemplo_5_reporte()

        print("\n" + "=" * 70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        limpiar_archivos()


if __name__ == "__main__":
    main()
