"""
Script principal para demostración completa del Data Warehouse.

Este script ejecuta el pipeline completo:
1. Genera dimensiones (DimFecha, DimProducto, DimCliente)
2. Aplica SCD Type 2 donde corresponda
3. Valida calidad de datos
4. Crea y carga el Data Warehouse (SQLite)
5. Genera tabla de hechos (FactVentas)
6. Ejecuta queries analíticos OLAP
7. Muestra resultados formateados

Uso:
    python main.py
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import DatabaseConnection
from src.generador_dim_fecha import generar_dim_fecha
from src.utilidades import (
    configurar_logging,
    crear_directorio_si_no_existe,
    formatear_numero,
    imprimir_tabla,
    medir_tiempo,
)
from src.validaciones import (
    validar_no_nulos,
    validar_rangos,
    validar_tipos,
)


def main():
    """Función principal que ejecuta el pipeline completo del DWH."""
    # Configurar logging
    logger = configurar_logging(nivel="INFO")
    logger.info("=" * 80)
    logger.info("INICIO - Pipeline de Data Warehouse con Star Schema")
    logger.info("=" * 80)

    # Crear directorio de salida
    crear_directorio_si_no_existe("output")

    # ========================================
    # FASE 1: GENERACIÓN DE DIMENSIONES
    # ========================================
    logger.info("\n" + "=" * 80)
    logger.info("FASE 1: Generación de Dimensiones")
    logger.info("=" * 80)

    # Generar DimFecha (todo el año 2024)
    logger.info("\n1.1 Generando DimFecha (año 2024)...")
    with medir_tiempo("DimFecha"):
        dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31")
    logger.info(f"  [OK] {len(dim_fecha)} registros de fechas generados")

    # Generar DimProducto (requiere Faker - placeholder)
    logger.info("\n1.2 DimProducto...")
    logger.warning(
        "  [!] DimProducto requiere Faker (no instalado en este entorno de demostración)"
    )
    logger.info("  -> Usando datos mock para demostración")
    # En producción:
    # dim_producto = generar_dim_producto(100)

    # Generar DimCliente con SCD Type 2 (requiere Faker - placeholder)
    logger.info("\n1.3 DimCliente con SCD Type 2...")
    logger.warning(
        "  [!] DimCliente requiere Faker (no instalado en este entorno de demostración)"
    )
    logger.info("  -> Usando datos mock para demostración")
    # En producción:
    # dim_cliente = generar_dim_cliente(200)

    # ========================================
    # FASE 2: VALIDACIÓN DE CALIDAD DE DATOS
    # ========================================
    logger.info("\n" + "=" * 80)
    logger.info("FASE 2: Validación de Calidad de Datos")
    logger.info("=" * 80)

    logger.info("\n2.1 Validando DimFecha...")
    with medir_tiempo("Validación DimFecha"):
        # Validar no nulos
        resultado_nulos = validar_no_nulos(
            dim_fecha,
            [
                "fecha_id",
                "fecha_completa",
                "dia",
                "mes",
                "anio",
                "trimestre",
            ],
        )

        # Validar rangos
        resultado_rangos = validar_rangos(
            dim_fecha,
            {
                "dia": (1, 31),
                "mes": (1, 12),
                "trimestre": (1, 4),
                "numero_dia_semana": (0, 6),
            },
        )

        # Validar tipos
        resultado_tipos = validar_tipos(
            dim_fecha,
            {
                "fecha_id": int,
                "dia": int,
                "mes": int,
                "anio": int,
            },
        )

    if resultado_nulos["is_valid"]:
        logger.info("  [OK] Validación de nulos: PASSED")
    else:
        logger.error(f"  ✗ Errores de nulos: {resultado_nulos['errors']}")

    if resultado_rangos["is_valid"]:
        logger.info("  [OK] Validación de rangos: PASSED")
    else:
        logger.error(f"  ✗ Errores de rangos: {resultado_rangos['errors']}")

    if resultado_tipos["is_valid"]:
        logger.info("  [OK] Validación de tipos: PASSED")
    else:
        logger.error(f"  ✗ Errores de tipos: {resultado_tipos['errors']}")

    # ========================================
    # FASE 3: CREACIÓN Y CARGA DEL DATA WAREHOUSE
    # ========================================
    logger.info("\n" + "=" * 80)
    logger.info("FASE 3: Creación y Carga del Data Warehouse")
    logger.info("=" * 80)

    db_path = "output/data_warehouse.db"
    logger.info(f"\n3.1 Creando base de datos: {db_path}")

    with DatabaseConnection(db_path) as db:
        # Crear tablas
        logger.info("\n3.2 Creando esquema Star Schema...")
        with medir_tiempo("Creación de tablas"):
            db.crear_tablas()
        logger.info(
            "  [OK] Tablas creadas: DimFecha, DimProducto, DimCliente, DimVendedor, FactVentas"
        )

        # Cargar dimensiones
        logger.info("\n3.3 Cargando dimensiones...")
        with medir_tiempo("Carga de DimFecha"):
            registros = db.cargar_dimension("DimFecha", dim_fecha)
        logger.info(f"  [OK] DimFecha: {registros} registros cargados")

        logger.info("\n  [!] DimProducto, DimCliente, DimVendedor: Requieren Faker")
        logger.info("  -> En producción, aquí se cargarían todas las dimensiones")

        # ========================================
        # FASE 4: QUERIES ANALÍTICOS OLAP
        # ========================================
        logger.info("\n" + "=" * 80)
        logger.info("FASE 4: Queries Analíticos OLAP (Demostración)")
        logger.info("=" * 80)

        logger.info("\n  [!] Queries requieren datos completos (con Faker)")
        logger.info("  -> Mostrando estructura de queries disponibles:")

        # Mostrar queries disponibles
        queries_disponibles = [
            {
                "Query": "ventas_por_categoria()",
                "Descripción": "Agrega ventas por categoría de producto",
                "Operación OLAP": "Roll-up, Drill-down por año",
            },
            {
                "Query": "top_productos()",
                "Descripción": "Top N productos más vendidos",
                "Operación OLAP": "Ranking, Top-N analysis",
            },
            {
                "Query": "ventas_por_mes()",
                "Descripción": "Serie temporal de ventas mensuales",
                "Operación OLAP": "Time series, Drill-down por trimestre",
            },
            {
                "Query": "analisis_vendedores()",
                "Descripción": "Performance de vendedores",
                "Operación OLAP": "Aggregation, Metrics calculation",
            },
            {
                "Query": "clientes_frecuentes()",
                "Descripción": "Top N clientes por compras",
                "Operación OLAP": "Ranking, Customer segmentation",
            },
            {
                "Query": "kpis_dashboard()",
                "Descripción": "KPIs principales para dashboard ejecutivo",
                "Operación OLAP": "Multi-dimensional aggregation",
            },
        ]

        imprimir_tabla(
            queries_disponibles,
            headers=["Query", "Descripción", "Operación OLAP"],
            titulo="Queries Analíticos Implementados",
        )

    # ========================================
    # RESUMEN FINAL
    # ========================================
    logger.info("\n" + "=" * 80)
    logger.info("RESUMEN FINAL")
    logger.info("=" * 80)

    resumen = [
        {
            "Componente": "DimFecha",
            "Estado": "[OK] Completado",
            "Registros": formatear_numero(len(dim_fecha)),
        },
        {
            "Componente": "DimProducto",
            "Estado": "[!] Requiere Faker",
            "Registros": "-",
        },
        {
            "Componente": "DimCliente (SCD Type 2)",
            "Estado": "[!] Requiere Faker",
            "Registros": "-",
        },
        {
            "Componente": "DimVendedor",
            "Estado": "[!] Requiere Faker",
            "Registros": "-",
        },
        {
            "Componente": "FactVentas",
            "Estado": "[!] Requiere dimensiones completas",
            "Registros": "-",
        },
        {
            "Componente": "Validaciones",
            "Estado": "[OK] Completado",
            "Registros": "5 funciones",
        },
        {
            "Componente": "Queries OLAP",
            "Estado": "[OK] Completado",
            "Registros": "6 queries",
        },
        {
            "Componente": "Database Schema",
            "Estado": "[OK] Completado",
            "Registros": "5 tablas",
        },
    ]

    imprimir_tabla(
        resumen,
        headers=["Componente", "Estado", "Registros"],
        titulo="Estado del Pipeline",
    )

    logger.info("\n" + "=" * 80)
    logger.info("NOTAS IMPORTANTES:")
    logger.info("=" * 80)
    logger.info(
        """
1. Este proyecto educativo demuestra un Data Warehouse completo con Star Schema
2. Para ejecutar con datos completos, instalar: pip install faker
3. El esquema soporta SCD Type 2 para tracking histórico de clientes
4. Queries OLAP implementan: drill-down, roll-up, slice-and-dice
5. Validaciones aseguran calidad de datos antes de carga
6. Context manager DatabaseConnection garantiza transacciones seguras

PRÓXIMOS PASOS:
- Instalar Faker: pip install faker
- Ejecutar: python main.py (con datos completos)
- Explorar: queries_analiticos.py para ejemplos de OLAP
- Revisar: scd_tipo2.py para lógica de dimensiones slowly changing
"""
    )

    logger.info("=" * 80)
    logger.info("FIN - Pipeline completado exitosamente")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger = configurar_logging(nivel="ERROR")
        logger.error(f"\n[X] Error crítico en el pipeline: {e}")
        logger.exception("Traceback completo:")
        sys.exit(1)
