"""
Módulo de queries analíticos para Data Warehouse.

Este módulo provee funciones para ejecutar queries OLAP (Online Analytical Processing)
sobre el Data Warehouse, soportando operaciones de drill-down, slice-and-dice y roll-up.

Funciones:
    ventas_por_categoria: Agrega ventas por categoría de producto
    top_productos: Obtiene productos más vendidos
    ventas_por_mes: Serie temporal de ventas mensuales
    analisis_vendedores: Performance de vendedores
    clientes_frecuentes: Top clientes por frecuencia de compra
    kpis_dashboard: KPIs principales para dashboard
"""

from typing import Optional

import pandas as pd


def ventas_por_categoria(db, anio: Optional[int] = None) -> pd.DataFrame:
    """
    Calcula ventas totales agrupadas por categoría de producto.

    Args:
        db: Instancia de DatabaseConnection
        anio: Filtrar por año específico (opcional)

    Returns:
        DataFrame con columnas:
            - categoria (str): Categoría del producto
            - total_ventas (float): Monto total vendido
            - cantidad_productos (int): Cantidad de productos vendidos
        Ordenado por total_ventas DESC

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     resultado = ventas_por_categoria(db)
        ...     print(resultado.head())
                    categoria  total_ventas  cantidad_productos
        0      Electrónica      50000.00                 120
        1            Hogar      30000.00                  80
    """
    query = """
        SELECT
            p.categoria,
            SUM(f.monto_neto) as total_ventas,
            SUM(f.cantidad) as cantidad_productos
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
    """

    # Agregar filtro de año si se especifica
    if anio is not None:
        query += """
        JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
        WHERE fe.anio = ?
        """

    query += """
        GROUP BY p.categoria
        ORDER BY total_ventas DESC
    """

    if anio is not None:
        return db.ejecutar_query(query, params=(anio,))
    else:
        return db.ejecutar_query(query)


def top_productos(db, top_n: int = 10) -> pd.DataFrame:
    """
    Obtiene los productos más vendidos por monto total.

    Args:
        db: Instancia de DatabaseConnection
        top_n: Cantidad de productos a retornar (default: 10)

    Returns:
        DataFrame con columnas:
            - nombre_producto (str): Nombre del producto
            - categoria (str): Categoría
            - total_ventas (float): Monto total vendido
            - cantidad_vendida (int): Unidades vendidas
        Ordenado por total_ventas DESC, limitado a top_n

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     top_5 = top_productos(db, top_n=5)
        ...     print(top_5)
    """
    query = """
        SELECT
            p.nombre_producto,
            p.categoria,
            SUM(f.monto_neto) as total_ventas,
            SUM(f.cantidad) as cantidad_vendida
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
        GROUP BY p.producto_id, p.nombre_producto, p.categoria
        ORDER BY total_ventas DESC
        LIMIT ?
    """

    return db.ejecutar_query(query, params=(top_n,))


def ventas_por_mes(db, trimestre: Optional[int] = None) -> pd.DataFrame:
    """
    Serie temporal de ventas agrupadas por mes.

    Args:
        db: Instancia de DatabaseConnection
        trimestre: Filtrar por trimestre (1-4, opcional)

    Returns:
        DataFrame con columnas:
            - anio (int): Año
            - mes (int): Mes (1-12)
            - mes_nombre (str): Nombre del mes en español
            - total_ventas (float): Monto total vendido
            - num_transacciones (int): Cantidad de transacciones
        Ordenado cronológicamente (anio, mes)

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     ventas_q1 = ventas_por_mes(db, trimestre=1)
        ...     print(ventas_q1)
    """
    query = """
        SELECT
            fe.anio,
            fe.mes,
            fe.mes_nombre,
            SUM(f.monto_neto) as total_ventas,
            COUNT(f.venta_id) as num_transacciones
        FROM FactVentas f
        JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
    """

    # Agregar filtro de trimestre si se especifica
    if trimestre is not None:
        query += """
        WHERE fe.trimestre = ?
        """

    query += """
        GROUP BY fe.anio, fe.mes, fe.mes_nombre
        ORDER BY fe.anio, fe.mes
    """

    if trimestre is not None:
        return db.ejecutar_query(query, params=(trimestre,))
    else:
        return db.ejecutar_query(query)


def analisis_vendedores(db) -> pd.DataFrame:
    """
    Análisis de performance de vendedores.

    Args:
        db: Instancia de DatabaseConnection

    Returns:
        DataFrame con columnas:
            - nombre (str): Nombre del vendedor
            - region (str): Región asignada
            - total_ventas (float): Monto total vendido
            - num_transacciones (int): Cantidad de ventas
            - ticket_promedio (float): Venta promedio por transacción
        Ordenado por total_ventas DESC

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     performance = analisis_vendedores(db)
        ...     print(performance)
    """
    query = """
        SELECT
            v.nombre,
            v.region,
            SUM(f.monto_neto) as total_ventas,
            COUNT(f.venta_id) as num_transacciones,
            AVG(f.monto_neto) as ticket_promedio
        FROM FactVentas f
        JOIN DimVendedor v ON f.vendedor_id = v.vendedor_id
        GROUP BY v.vendedor_id, v.nombre, v.region
        ORDER BY total_ventas DESC
    """

    return db.ejecutar_query(query)


def clientes_frecuentes(db, top_n: int = 10) -> pd.DataFrame:
    """
    Obtiene clientes más frecuentes por monto total de compras.

    Args:
        db: Instancia de DatabaseConnection
        top_n: Cantidad de clientes a retornar (default: 10)

    Returns:
        DataFrame con columnas:
            - nombre (str): Nombre del cliente
            - segmento (str): Segmento del cliente
            - ciudad (str): Ciudad
            - total_compras (float): Monto total comprado
            - num_transacciones (int): Cantidad de compras
        Ordenado por total_compras DESC, limitado a top_n

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     top_clientes = clientes_frecuentes(db, top_n=20)
        ...     print(top_clientes)
    """
    query = """
        SELECT
            c.nombre,
            c.segmento,
            c.ciudad,
            SUM(f.monto_neto) as total_compras,
            COUNT(f.venta_id) as num_transacciones
        FROM FactVentas f
        JOIN DimCliente c ON f.cliente_id = c.cliente_sk
        WHERE c.es_actual = 1
        GROUP BY c.cliente_sk, c.nombre, c.segmento, c.ciudad
        ORDER BY total_compras DESC
        LIMIT ?
    """

    return db.ejecutar_query(query, params=(top_n,))


def kpis_dashboard(db) -> dict[str, float | int | str | None]:
    """
    Calcula KPIs principales para dashboard ejecutivo.

    Args:
        db: Instancia de DatabaseConnection

    Returns:
        Diccionario con KPIs:
            - total_ventas (float): Suma total de ventas
            - num_transacciones (int): Cantidad de transacciones
            - ticket_promedio (float): Venta promedio por transacción
            - num_clientes_activos (int): Clientes únicos con compras
            - num_productos_vendidos (int): Productos únicos vendidos
            - categoria_top (str): Categoría con mayores ventas

    Examples:
        >>> with DatabaseConnection("dwh.db") as db:
        ...     kpis = kpis_dashboard(db)
        ...     print(f"Total Ventas: ${kpis['total_ventas']:,.2f}")
        Total Ventas: $150,000.00
    """
    # Query para métricas básicas
    query_metricas = """
        SELECT
            SUM(monto_neto) as total_ventas,
            COUNT(venta_id) as num_transacciones,
            AVG(monto_neto) as ticket_promedio,
            COUNT(DISTINCT cliente_id) as num_clientes_activos,
            COUNT(DISTINCT producto_id) as num_productos_vendidos
        FROM FactVentas
    """

    df_metricas = db.ejecutar_query(query_metricas)
    metricas = df_metricas.iloc[0].to_dict()

    # Query para categoría top
    query_categoria_top = """
        SELECT
            p.categoria,
            SUM(f.monto_neto) as total
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
        GROUP BY p.categoria
        ORDER BY total DESC
        LIMIT 1
    """

    df_categoria = db.ejecutar_query(query_categoria_top)

    # Construir diccionario de KPIs
    kpis = {
        "total_ventas": float(metricas["total_ventas"]),
        "num_transacciones": int(metricas["num_transacciones"]),
        "ticket_promedio": float(metricas["ticket_promedio"]),
        "num_clientes_activos": int(metricas["num_clientes_activos"]),
        "num_productos_vendidos": int(metricas["num_productos_vendidos"]),
        "categoria_top": (
            df_categoria.iloc[0]["categoria"] if len(df_categoria) > 0 else None
        ),
    }

    return kpis
