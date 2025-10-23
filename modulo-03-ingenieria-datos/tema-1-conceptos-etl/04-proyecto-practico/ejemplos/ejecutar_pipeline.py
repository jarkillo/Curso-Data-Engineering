"""
Script de ejemplo para ejecutar el pipeline ETL de ventas.

Este script demuestra cómo usar el pipeline ETL completo para procesar
ventas de diferentes fechas.
"""

import sys
from pathlib import Path

# Añadir el directorio src/ al path para importar los módulos
proyecto_root = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_root))

from src.pipeline import pipeline_etl  # noqa: E402
from src.utilidades import configurar_logging  # noqa: E402


def main():
    """Función principal que ejecuta el pipeline para múltiples fechas."""
    print("=" * 60)
    print("Pipeline ETL de Ventas de E-commerce")
    print("=" * 60)

    # Configurar logging
    configurar_logging("INFO")

    # Configuración
    directorio_datos = proyecto_root / "datos"
    db_path = proyecto_root / "ventas.db"

    # Fechas a procesar
    fechas = ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05"]

    resultados = []

    print(f"\n📂 Directorio de datos: {directorio_datos}")
    print(f"💾 Base de datos: {db_path}")
    print(f"📅 Fechas a procesar: {len(fechas)}")
    print("\n" + "-" * 60)

    # Procesar cada fecha
    for i, fecha in enumerate(fechas, 1):
        print(f"\n[{i}/{len(fechas)}] Procesando fecha: {fecha}")
        print("-" * 40)

        try:
            # Ejecutar pipeline sin reintentos
            metricas = pipeline_etl(
                fecha=fecha,
                directorio_datos=str(directorio_datos),
                db_path=str(db_path),
            )

            # Para usar reintentos, importar y usar pipeline_etl_con_reintentos:
            # from src.pipeline import pipeline_etl_con_reintentos
            # metricas = pipeline_etl_con_reintentos(
            #     fecha=fecha,
            #     directorio_datos=str(directorio_datos),
            #     db_path=str(db_path),
            #     max_intentos=3
            # )

            resultados.append(metricas)

            # Mostrar resultados
            print(f"\n✅ Estado: {metricas['estado']}")
            print(f"📊 Filas extraídas: {metricas['filas_extraidas']}")
            print(f"✓ Filas válidas: {metricas['filas_validas']}")
            print(f"💾 Filas cargadas: {metricas['filas_cargadas']}")
            print(f"⏱️ Tiempo: {metricas['tiempo_segundos']}s")

            if metricas["errores"]:
                print(f"⚠️ Errores: {metricas['errores']}")

        except Exception as e:
            print(f"\n❌ Error procesando {fecha}: {e}")
            resultados.append(
                {
                    "fecha": fecha,
                    "estado": "ERROR",
                    "errores": [str(e)],
                }
            )

    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)

    total_procesadas = len([r for r in resultados if r["estado"] == "EXITOSO"])
    total_errores = len([r for r in resultados if r["estado"] == "ERROR"])
    total_sin_datos = len([r for r in resultados if r["estado"] == "SIN_DATOS"])

    print(f"\n📊 Total de fechas: {len(fechas)}")
    print(f"✅ Exitosas: {total_procesadas}")
    print(f"⚠️ Sin datos: {total_sin_datos}")
    print(f"❌ Con errores: {total_errores}")

    if total_procesadas > 0:
        total_filas = sum(
            r["filas_cargadas"] for r in resultados if r["estado"] == "EXITOSO"
        )
        tiempo_total = sum(
            r["tiempo_segundos"] for r in resultados if r["estado"] == "EXITOSO"
        )
        print(f"\n💾 Total de filas cargadas: {total_filas}")
        print(f"⏱️ Tiempo total: {tiempo_total:.2f}s")

        if tiempo_total > 0:
            throughput = total_filas / tiempo_total
            print(f"🚀 Throughput: {throughput:.2f} filas/s")

    print("\n" + "=" * 60)
    print("Pipeline completado!")
    print("=" * 60)


if __name__ == "__main__":
    main()
