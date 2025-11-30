#!/usr/bin/env python
"""
Script principal de ETL para cargar el Data Warehouse.

Orquesta la generación de dimensiones, validación de datos y carga
al Star Schema. Soporta argumentos CLI para configuración flexible.

Uso:
    python cargar_datawarehouse.py --help
    python cargar_datawarehouse.py --db output/dwh.db --ventas 1000
    python cargar_datawarehouse.py --db output/dwh.db --ventas 5000 --log-file logs/etl.log
"""

import argparse
import sys
import time
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import DatabaseConnection
from src.generador_dim_cliente import generar_dim_cliente
from src.generador_dim_fecha import generar_dim_fecha
from src.generador_dim_producto import generar_dim_producto
from src.generador_dim_vendedor import generar_dim_vendedor
from src.generador_fact_ventas import generar_fact_ventas
from src.utilidades import (
    configurar_logging,
    crear_directorio_si_no_existe,
    formatear_numero,
    generar_reporte_resumen,
    medir_tiempo,
)
from src.validaciones import (
    validar_no_nulos,
    validar_rangos,
)


def crear_parser() -> argparse.ArgumentParser:
    """
    Crea el parser de argumentos CLI.

    Returns:
        ArgumentParser configurado con todas las opciones
    """
    parser = argparse.ArgumentParser(
        description="Carga el Data Warehouse con datos sintéticos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --db output/dwh.db --ventas 1000
  %(prog)s --db output/dwh.db --ventas 5000 --productos 200 --clientes 500
  %(prog)s --db output/dwh.db --ventas 10000 --log-file logs/etl.log --log-level DEBUG
        """,
    )

    parser.add_argument(
        "--db",
        type=str,
        default="output/data_warehouse.db",
        help="Ruta de la base de datos SQLite (default: output/data_warehouse.db)",
    )

    parser.add_argument(
        "--ventas",
        type=int,
        default=1000,
        help="Número de ventas a generar (default: 1000)",
    )

    parser.add_argument(
        "--productos",
        type=int,
        default=100,
        help="Número de productos a generar (default: 100)",
    )

    parser.add_argument(
        "--clientes",
        type=int,
        default=200,
        help="Número de clientes a generar (default: 200)",
    )

    parser.add_argument(
        "--vendedores",
        type=int,
        default=50,
        help="Número de vendedores a generar (default: 50)",
    )

    parser.add_argument(
        "--fecha-inicio",
        type=str,
        default="2024-01-01",
        help="Fecha inicio para DimFecha (default: 2024-01-01)",
    )

    parser.add_argument(
        "--fecha-fin",
        type=str,
        default="2024-12-31",
        help="Fecha fin para DimFecha (default: 2024-12-31)",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Archivo para guardar logs (default: solo consola)",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Nivel de logging (default: INFO)",
    )

    parser.add_argument(
        "--skip-validacion",
        action="store_true",
        help="Omitir validación de datos (no recomendado)",
    )

    return parser


def validar_dimensiones(
    logger, dim_fecha, dim_producto, dim_cliente, dim_vendedor
) -> bool:
    """
    Valida las dimensiones generadas.

    Args:
        logger: Logger configurado
        dim_fecha: DataFrame de fechas
        dim_producto: DataFrame de productos
        dim_cliente: DataFrame de clientes
        dim_vendedor: DataFrame de vendedores

    Returns:
        True si todas las validaciones pasan
    """
    logger.info("Validando dimensiones...")
    errores = []

    # Validar DimFecha
    resultado = validar_no_nulos(
        dim_fecha, ["fecha_id", "fecha_completa", "dia", "mes", "anio"]
    )
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    resultado = validar_rangos(
        dim_fecha, {"dia": (1, 31), "mes": (1, 12), "trimestre": (1, 4)}
    )
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    # Validar DimProducto
    resultado = validar_no_nulos(
        dim_producto, ["producto_id", "nombre_producto", "precio_catalogo"]
    )
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    resultado = validar_rangos(dim_producto, {"precio_catalogo": (0.01, 100000)})
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    # Validar DimCliente
    resultado = validar_no_nulos(dim_cliente, ["cliente_id", "nombre", "email"])
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    # Validar DimVendedor
    resultado = validar_no_nulos(dim_vendedor, ["vendedor_id", "nombre", "region"])
    if not resultado["is_valid"]:
        errores.extend(resultado["errors"])

    if errores:
        for error in errores:
            logger.error(f"  ✗ {error}")
        return False

    logger.info("  ✓ Todas las validaciones pasaron")
    return True


def ejecutar_etl(args: argparse.Namespace) -> int:
    """
    Ejecuta el pipeline ETL completo.

    Args:
        args: Argumentos parseados del CLI

    Returns:
        Código de salida (0 = éxito, 1 = error)
    """
    inicio_total = time.time()
    estadisticas = {
        "dimensiones": {},
        "fact_tables": {},
        "tiempo_total": 0,
        "errores": [],
    }

    # Configurar logging
    logger = configurar_logging(
        nivel=args.log_level,
        archivo=args.log_file,
    )

    logger.info("=" * 60)
    logger.info("INICIO - Pipeline ETL Data Warehouse")
    logger.info("=" * 60)
    logger.info(f"Base de datos: {args.db}")
    logger.info(f"Ventas a generar: {formatear_numero(args.ventas)}")

    # Crear directorio de salida
    db_path = Path(args.db)
    crear_directorio_si_no_existe(str(db_path.parent))

    try:
        # FASE 1: Generar dimensiones
        logger.info("")
        logger.info("FASE 1: Generación de Dimensiones")
        logger.info("-" * 40)

        logger.info("Generando DimFecha...")
        with medir_tiempo("DimFecha"):
            dim_fecha = generar_dim_fecha(args.fecha_inicio, args.fecha_fin)
        estadisticas["dimensiones"]["DimFecha"] = len(dim_fecha)
        logger.info(f"  ✓ {formatear_numero(len(dim_fecha))} fechas generadas")

        logger.info("Generando DimProducto...")
        with medir_tiempo("DimProducto"):
            dim_producto = generar_dim_producto(args.productos)
        estadisticas["dimensiones"]["DimProducto"] = len(dim_producto)
        logger.info(f"  ✓ {formatear_numero(len(dim_producto))} productos generados")

        logger.info("Generando DimCliente...")
        with medir_tiempo("DimCliente"):
            dim_cliente = generar_dim_cliente(args.clientes)
        estadisticas["dimensiones"]["DimCliente"] = len(dim_cliente)
        logger.info(f"  ✓ {formatear_numero(len(dim_cliente))} clientes generados")

        logger.info("Generando DimVendedor...")
        with medir_tiempo("DimVendedor"):
            dim_vendedor = generar_dim_vendedor(args.vendedores)
        estadisticas["dimensiones"]["DimVendedor"] = len(dim_vendedor)
        logger.info(f"  ✓ {formatear_numero(len(dim_vendedor))} vendedores generados")

        # FASE 2: Validación
        if not args.skip_validacion:
            logger.info("")
            logger.info("FASE 2: Validación de Datos")
            logger.info("-" * 40)

            if not validar_dimensiones(
                logger, dim_fecha, dim_producto, dim_cliente, dim_vendedor
            ):
                estadisticas["errores"].append("Validación de dimensiones fallida")
                raise ValueError("Validación de dimensiones fallida")
        else:
            logger.warning("FASE 2: Validación OMITIDA (--skip-validacion)")

        # FASE 3: Cargar Data Warehouse
        logger.info("")
        logger.info("FASE 3: Carga del Data Warehouse")
        logger.info("-" * 40)

        with DatabaseConnection(args.db) as db:
            logger.info("Creando esquema...")
            with medir_tiempo("Crear tablas"):
                db.crear_tablas()
            logger.info("  ✓ Esquema Star Schema creado")

            logger.info("Cargando DimFecha...")
            with medir_tiempo("Cargar DimFecha"):
                db.cargar_dimension("DimFecha", dim_fecha)

            logger.info("Cargando DimProducto...")
            with medir_tiempo("Cargar DimProducto"):
                db.cargar_dimension("DimProducto", dim_producto)

            # DimCliente necesita adaptación para el esquema SCD Type 2
            logger.info("Cargando DimCliente...")
            with medir_tiempo("Cargar DimCliente"):
                # Preparar datos para esquema SCD Type 2
                dim_cliente_carga = dim_cliente.copy()
                # Renombrar columnas si es necesario
                if "cliente_sk" not in dim_cliente_carga.columns:
                    dim_cliente_carga = dim_cliente_carga.rename(
                        columns={"cliente_id": "cliente_id"}
                    )
                # Añadir campos SCD si no existen
                if "version" not in dim_cliente_carga.columns:
                    dim_cliente_carga["version"] = 1
                if "es_actual" not in dim_cliente_carga.columns:
                    dim_cliente_carga["es_actual"] = True
                if "fecha_inicio" not in dim_cliente_carga.columns:
                    dim_cliente_carga["fecha_inicio"] = args.fecha_inicio
                if "fecha_fin" not in dim_cliente_carga.columns:
                    dim_cliente_carga["fecha_fin"] = None

                db.cargar_dimension("DimCliente", dim_cliente_carga)

            logger.info("Cargando DimVendedor...")
            with medir_tiempo("Cargar DimVendedor"):
                db.cargar_dimension("DimVendedor", dim_vendedor)

            # FASE 4: Generar y cargar FactVentas
            logger.info("")
            logger.info("FASE 4: Generación de Tabla de Hechos")
            logger.info("-" * 40)

            logger.info(f"Generando {formatear_numero(args.ventas)} ventas...")

            # Preparar dimensiones para generar ventas
            # Obtener cliente_sk del DimCliente cargado
            df_clientes_cargados = db.ejecutar_query(
                "SELECT cliente_sk as cliente_id FROM DimCliente"
            )

            with medir_tiempo("Generar FactVentas"):
                fact_ventas = generar_fact_ventas(
                    args.ventas,
                    dim_fecha[["fecha_id"]],
                    dim_producto[["producto_id", "precio_catalogo"]],
                    df_clientes_cargados,
                    dim_vendedor[["vendedor_id"]],
                )
            estadisticas["fact_tables"]["FactVentas"] = len(fact_ventas)
            logger.info(f"  ✓ {formatear_numero(len(fact_ventas))} ventas generadas")

            logger.info("Cargando FactVentas...")
            with medir_tiempo("Cargar FactVentas"):
                db.cargar_fact("FactVentas", fact_ventas)
            logger.info("  ✓ Tabla de hechos cargada")

        # Calcular tiempo total
        estadisticas["tiempo_total"] = time.time() - inicio_total

        # Generar reporte
        logger.info("")
        reporte = generar_reporte_resumen(estadisticas)
        print(reporte)

        if args.log_file:
            logger.info(f"Logs guardados en: {args.log_file}")

        return 0

    except Exception as e:
        estadisticas["errores"].append(str(e))
        estadisticas["tiempo_total"] = time.time() - inicio_total
        logger.error(f"Error en pipeline: {e}")
        logger.exception("Traceback:")

        reporte = generar_reporte_resumen(estadisticas)
        print(reporte)

        return 1


def main() -> int:
    """
    Punto de entrada principal.

    Returns:
        Código de salida
    """
    parser = crear_parser()
    args = parser.parse_args()
    return ejecutar_etl(args)


if __name__ == "__main__":
    sys.exit(main())
