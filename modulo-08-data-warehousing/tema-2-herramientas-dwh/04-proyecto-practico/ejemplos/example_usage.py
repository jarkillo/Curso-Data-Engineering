"""Script de ejemplo para dbt de TechMart Analytics.

Este script NO es para ejecutar dbt (eso se hace con comandos dbt),
sino para demostrar cómo interactuar con los resultados del pipeline.
"""

import subprocess  # nosec B404
import sys
from pathlib import Path


def run_dbt_command(command: str) -> int:
    """
    Ejecuta un comando dbt y retorna el código de salida.

    Args:
        command: Comando dbt a ejecutar (ej: "dbt run")

    Returns:
        Código de salida del comando (0 = éxito)
    """
    print(f"\n{'=' * 60}")
    print(f"Ejecutando: {command}")
    print(f"{'=' * 60}\n")

    result = subprocess.run(  # nosec B602
        command,
        shell=True,
        cwd=Path(__file__).parent.parent,  # Directorio del proyecto
        capture_output=False,
    )

    return result.returncode


def main():
    """Ejecuta el pipeline completo de dbt y muestra los pasos."""
    print(
        """
╔════════════════════════════════════════════════════════════╗
║      TechMart Analytics - Pipeline dbt Completo            ║
╚════════════════════════════════════════════════════════════╝

Este script demuestra el flujo completo de trabajo con dbt:
1. Instalar dependencias (dbt-utils)
2. Cargar seeds (datos CSV)
3. Ejecutar modelos (staging + marts)
4. Ejecutar tests
5. Generar documentación
6. Crear snapshots (SCD Type 2)
    """
    )

    # Paso 1: Instalar dependencias
    print("\n📦 PASO 1: Instalar dependencias de dbt")
    if run_dbt_command("dbt deps") != 0:
        print("❌ Error instalando dependencias")
        sys.exit(1)

    # Paso 2: Cargar seeds
    print("\n📊 PASO 2: Cargar datos de seeds (CSV → Tablas)")
    if run_dbt_command("dbt seed") != 0:
        print("❌ Error cargando seeds")
        sys.exit(1)

    # Paso 3: Ejecutar modelos
    print("\n🔄 PASO 3: Ejecutar transformaciones (models)")
    print("   - Staging: Limpieza y estandarización")
    print("   - Marts: Dimensiones y hechos")
    if run_dbt_command("dbt run") != 0:
        print("❌ Error ejecutando modelos")
        sys.exit(1)

    # Paso 4: Ejecutar tests
    print("\n✅ PASO 4: Ejecutar tests de calidad de datos")
    if run_dbt_command("dbt test") != 0:
        print("⚠️  Algunos tests fallaron (revisar logs)")
        # No salimos, continuamos para ver resultados

    # Paso 5: Generar documentación
    print("\n📚 PASO 5: Generar documentación del proyecto")
    if run_dbt_command("dbt docs generate") != 0:
        print("❌ Error generando documentación")
        sys.exit(1)

    # Paso 6: Snapshots
    print("\n📸 PASO 6: Crear snapshots (SCD Type 2)")
    if run_dbt_command("dbt snapshot") != 0:
        print("❌ Error creando snapshots")
        sys.exit(1)

    print(
        """
╔════════════════════════════════════════════════════════════╗
║                    ✅ PIPELINE COMPLETO                    ║
╚════════════════════════════════════════════════════════════╝

El pipeline ha ejecutado exitosamente:

✅ Seeds cargados:
   - raw_customers (15 registros)
   - raw_products (15 versiones de 12 productos)
   - raw_orders (25 pedidos)

✅ Modelos staging:
   - stg_customers (limpieza de clientes)
   - stg_products (deduplicación de productos)
   - stg_orders (enriquecimiento de pedidos)

✅ Modelos marts:
   - dim_customers (segmentación RFM)
   - dim_products (clasificación por ventas)
   - fct_orders (hechos con métricas)

✅ Tests ejecutados (genéricos + personalizados)

✅ Snapshots creados:
   - products_snapshot (historial de cambios)

📖 Para ver la documentación:
   dbt docs serve

🔍 Para explorar los datos (ejemplo con DuckDB):
   SELECT * FROM dbt_dev.dim_customers WHERE customer_segment = 'Platinum';

📊 Para análisis específicos:
   - Clientes por segmento: SELECT customer_segment, COUNT(*) FROM dbt_dev.dim_customers GROUP BY 1;
   - Productos más vendidos: SELECT product_name, total_units_sold FROM dbt_dev.dim_products ORDER BY 2 DESC LIMIT 5;
   - Revenue por categoría: SELECT product_category, SUM(total_amount) FROM dbt_dev.fct_orders GROUP BY 1;
    """
    )


if __name__ == "__main__":
    main()
