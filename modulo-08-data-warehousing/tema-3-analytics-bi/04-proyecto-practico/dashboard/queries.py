"""
Queries analíticas para el Dashboard de BI.

Este módulo contiene todas las consultas SQL utilizadas por el dashboard,
organizadas por sección (Overview, Ventas, Clientes, Vendedores).
"""

import pandas as pd

from .database import execute_query

# =============================================================================
# QUERIES PARA OVERVIEW (KPIs Principales)
# =============================================================================


def get_kpis_principales() -> dict:
    """
    Obtiene los KPIs principales para el dashboard ejecutivo.

    Returns:
        Diccionario con KPIs:
            - total_revenue: float
            - num_transacciones: int
            - ticket_promedio: float
            - num_clientes: int
            - num_productos: int
    """
    query = """
        SELECT
            COALESCE(SUM(monto_neto), 0) as total_revenue,
            COUNT(venta_id) as num_transacciones,
            COALESCE(AVG(monto_neto), 0) as ticket_promedio,
            COUNT(DISTINCT cliente_id) as num_clientes,
            COUNT(DISTINCT producto_id) as num_productos
        FROM FactVentas
    """
    df = execute_query(query)
    return df.iloc[0].to_dict() if len(df) > 0 else {}


def get_ventas_por_mes() -> pd.DataFrame:
    """
    Obtiene ventas agrupadas por mes para gráfico de tendencia.

    Returns:
        DataFrame con columnas: anio, mes, mes_nombre, total_ventas, num_transacciones
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
        GROUP BY fe.anio, fe.mes, fe.mes_nombre
        ORDER BY fe.anio, fe.mes
    """
    return execute_query(query)


def get_ventas_por_categoria() -> pd.DataFrame:
    """
    Obtiene ventas agrupadas por categoría de producto.

    Returns:
        DataFrame con columnas: categoria, total_ventas, cantidad
    """
    query = """
        SELECT
            p.categoria,
            SUM(f.monto_neto) as total_ventas,
            SUM(f.cantidad) as cantidad
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
        GROUP BY p.categoria
        ORDER BY total_ventas DESC
    """
    return execute_query(query)


def get_ventas_por_region() -> pd.DataFrame:
    """
    Obtiene ventas agrupadas por región del vendedor.

    Returns:
        DataFrame con columnas: region, total_ventas, num_transacciones
    """
    query = """
        SELECT
            v.region,
            SUM(f.monto_neto) as total_ventas,
            COUNT(f.venta_id) as num_transacciones
        FROM FactVentas f
        JOIN DimVendedor v ON f.vendedor_id = v.vendedor_id
        GROUP BY v.region
        ORDER BY total_ventas DESC
    """
    return execute_query(query)


# =============================================================================
# QUERIES PARA ANÁLISIS DE VENTAS
# =============================================================================


def get_ventas_diarias(anio: int | None = None, mes: int | None = None) -> pd.DataFrame:
    """
    Obtiene ventas diarias con filtros opcionales.

    Args:
        anio: Filtrar por año (opcional)
        mes: Filtrar por mes (opcional)

    Returns:
        DataFrame con columnas: fecha, total_ventas, num_transacciones
    """
    query = """
        SELECT
            fe.fecha_completa as fecha,
            fe.dia_semana,
            SUM(f.monto_neto) as total_ventas,
            COUNT(f.venta_id) as num_transacciones,
            SUM(f.cantidad) as cantidad_productos
        FROM FactVentas f
        JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
        WHERE 1=1
    """
    params = []

    if anio is not None:
        query += " AND fe.anio = ?"
        params.append(anio)

    if mes is not None:
        query += " AND fe.mes = ?"
        params.append(mes)

    query += """
        GROUP BY fe.fecha_completa, fe.dia_semana
        ORDER BY fe.fecha_completa
    """

    return execute_query(query, tuple(params))


def get_top_productos(limit: int = 10, categoria: str | None = None) -> pd.DataFrame:
    """
    Obtiene los productos más vendidos.

    Args:
        limit: Número de productos a retornar
        categoria: Filtrar por categoría (opcional)

    Returns:
        DataFrame con columnas: nombre_producto, categoria, total_ventas, cantidad
    """
    query = """
        SELECT
            p.nombre_producto,
            p.categoria,
            p.marca,
            SUM(f.monto_neto) as total_ventas,
            SUM(f.cantidad) as cantidad_vendida
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
        WHERE 1=1
    """
    params = []

    if categoria is not None:
        query += " AND p.categoria = ?"
        params.append(categoria)

    query += f"""
        GROUP BY p.producto_id, p.nombre_producto, p.categoria, p.marca
        ORDER BY total_ventas DESC
        LIMIT {limit}
    """

    return execute_query(query, tuple(params))


def get_ventas_por_subcategoria() -> pd.DataFrame:
    """
    Obtiene ventas por categoría y subcategoría (para treemap).

    Returns:
        DataFrame con columnas: categoria, subcategoria, total_ventas
    """
    query = """
        SELECT
            p.categoria,
            p.subcategoria,
            SUM(f.monto_neto) as total_ventas,
            SUM(f.cantidad) as cantidad
        FROM FactVentas f
        JOIN DimProducto p ON f.producto_id = p.producto_id
        GROUP BY p.categoria, p.subcategoria
        ORDER BY p.categoria, total_ventas DESC
    """
    return execute_query(query)


def get_heatmap_dia_hora() -> pd.DataFrame:
    """
    Obtiene datos para heatmap de ventas por día de semana.

    Returns:
        DataFrame con columnas: dia_semana, mes, total_ventas
    """
    query = """
        SELECT
            fe.dia_semana,
            fe.numero_dia_semana,
            fe.mes_nombre,
            fe.mes,
            SUM(f.monto_neto) as total_ventas
        FROM FactVentas f
        JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
        GROUP BY fe.dia_semana, fe.numero_dia_semana, fe.mes_nombre, fe.mes
        ORDER BY fe.mes, fe.numero_dia_semana
    """
    return execute_query(query)


# =============================================================================
# QUERIES PARA ANÁLISIS DE CLIENTES
# =============================================================================


def get_clientes_por_segmento() -> pd.DataFrame:
    """
    Obtiene distribución de clientes por segmento.

    Returns:
        DataFrame con columnas: segmento, num_clientes, total_compras
    """
    query = """
        SELECT
            c.segmento,
            COUNT(DISTINCT c.cliente_sk) as num_clientes,
            COALESCE(SUM(f.monto_neto), 0) as total_compras,
            COUNT(f.venta_id) as num_transacciones
        FROM DimCliente c
        LEFT JOIN FactVentas f ON c.cliente_sk = f.cliente_id
        WHERE c.es_actual = 1
        GROUP BY c.segmento
        ORDER BY total_compras DESC
    """
    return execute_query(query)


def get_top_clientes(limit: int = 10) -> pd.DataFrame:
    """
    Obtiene los clientes con mayores compras.

    Args:
        limit: Número de clientes a retornar

    Returns:
        DataFrame con columnas: nombre, segmento, ciudad, total_compras, num_transacciones
    """
    query = f"""
        SELECT
            c.nombre,
            c.segmento,
            c.ciudad,
            c.estado,
            SUM(f.monto_neto) as total_compras,
            COUNT(f.venta_id) as num_transacciones,
            AVG(f.monto_neto) as ticket_promedio
        FROM FactVentas f
        JOIN DimCliente c ON f.cliente_id = c.cliente_sk
        WHERE c.es_actual = 1
        GROUP BY c.cliente_sk, c.nombre, c.segmento, c.ciudad, c.estado
        ORDER BY total_compras DESC
        LIMIT {limit}
    """
    return execute_query(query)


def get_clientes_por_ciudad() -> pd.DataFrame:
    """
    Obtiene distribución de clientes y ventas por ciudad.

    Returns:
        DataFrame con columnas: ciudad, estado, num_clientes, total_ventas
    """
    query = """
        SELECT
            c.ciudad,
            c.estado,
            COUNT(DISTINCT c.cliente_sk) as num_clientes,
            COALESCE(SUM(f.monto_neto), 0) as total_ventas
        FROM DimCliente c
        LEFT JOIN FactVentas f ON c.cliente_sk = f.cliente_id
        WHERE c.es_actual = 1
        GROUP BY c.ciudad, c.estado
        ORDER BY total_ventas DESC
    """
    return execute_query(query)


def get_rfm_analysis() -> pd.DataFrame:
    """
    Análisis RFM (Recency, Frequency, Monetary) de clientes.

    Returns:
        DataFrame con columnas: cliente, recency_days, frequency, monetary
    """
    query = """
        WITH cliente_stats AS (
            SELECT
                c.cliente_sk,
                c.nombre,
                c.segmento,
                MAX(fe.fecha_completa) as ultima_compra,
                COUNT(f.venta_id) as frequency,
                SUM(f.monto_neto) as monetary
            FROM FactVentas f
            JOIN DimCliente c ON f.cliente_id = c.cliente_sk
            JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
            WHERE c.es_actual = 1
            GROUP BY c.cliente_sk, c.nombre, c.segmento
        )
        SELECT
            nombre,
            segmento,
            ultima_compra,
            julianday('now') - julianday(ultima_compra) as recency_days,
            frequency,
            monetary,
            monetary / frequency as avg_order_value
        FROM cliente_stats
        ORDER BY monetary DESC
    """
    return execute_query(query)


# =============================================================================
# QUERIES PARA ANÁLISIS DE VENDEDORES
# =============================================================================


def get_performance_vendedores() -> pd.DataFrame:
    """
    Obtiene métricas de performance por vendedor.

    Returns:
        DataFrame con columnas: nombre, region, total_ventas, num_transacciones, ticket_promedio
    """
    query = """
        SELECT
            v.vendedor_id,
            v.nombre,
            v.region,
            v.comision_porcentaje,
            SUM(f.monto_neto) as total_ventas,
            COUNT(f.venta_id) as num_transacciones,
            AVG(f.monto_neto) as ticket_promedio,
            SUM(f.monto_neto) * v.comision_porcentaje / 100 as comision_total
        FROM FactVentas f
        JOIN DimVendedor v ON f.vendedor_id = v.vendedor_id
        GROUP BY v.vendedor_id, v.nombre, v.region, v.comision_porcentaje
        ORDER BY total_ventas DESC
    """
    return execute_query(query)


def get_ventas_por_vendedor_mes() -> pd.DataFrame:
    """
    Obtiene ventas por vendedor desglosadas por mes.

    Returns:
        DataFrame con columnas: vendedor, mes, total_ventas
    """
    query = """
        SELECT
            v.nombre as vendedor,
            fe.mes_nombre,
            fe.mes,
            SUM(f.monto_neto) as total_ventas
        FROM FactVentas f
        JOIN DimVendedor v ON f.vendedor_id = v.vendedor_id
        JOIN DimFecha fe ON f.fecha_id = fe.fecha_id
        GROUP BY v.nombre, fe.mes_nombre, fe.mes
        ORDER BY v.nombre, fe.mes
    """
    return execute_query(query)


def get_ranking_vendedores_por_region() -> pd.DataFrame:
    """
    Obtiene ranking de vendedores agrupados por región.

    Returns:
        DataFrame con columnas: region, vendedor, total_ventas, ranking
    """
    query = """
        WITH ventas_vendedor AS (
            SELECT
                v.region,
                v.nombre as vendedor,
                SUM(f.monto_neto) as total_ventas
            FROM FactVentas f
            JOIN DimVendedor v ON f.vendedor_id = v.vendedor_id
            GROUP BY v.region, v.vendedor_id, v.nombre
        )
        SELECT
            region,
            vendedor,
            total_ventas,
            RANK() OVER (PARTITION BY region ORDER BY total_ventas DESC) as ranking
        FROM ventas_vendedor
        ORDER BY region, ranking
    """
    return execute_query(query)


# =============================================================================
# QUERIES PARA FILTROS
# =============================================================================


def get_filtros_disponibles() -> dict:
    """
    Obtiene los valores disponibles para los filtros del dashboard.

    Returns:
        Diccionario con listas de valores para cada filtro:
            - anios: list[int]
            - meses: list[dict] (mes, mes_nombre)
            - categorias: list[str]
            - regiones: list[str]
            - segmentos: list[str]
    """
    filtros = {}

    # Años disponibles
    df_anios = execute_query("""
        SELECT DISTINCT anio FROM DimFecha ORDER BY anio
    """)
    filtros["anios"] = df_anios["anio"].tolist() if len(df_anios) > 0 else []

    # Meses
    df_meses = execute_query("""
        SELECT DISTINCT mes, mes_nombre FROM DimFecha ORDER BY mes
    """)
    filtros["meses"] = df_meses.to_dict("records") if len(df_meses) > 0 else []

    # Categorías
    df_cats = execute_query("""
        SELECT DISTINCT categoria FROM DimProducto ORDER BY categoria
    """)
    filtros["categorias"] = df_cats["categoria"].tolist() if len(df_cats) > 0 else []

    # Regiones
    df_regions = execute_query("""
        SELECT DISTINCT region FROM DimVendedor ORDER BY region
    """)
    filtros["regiones"] = df_regions["region"].tolist() if len(df_regions) > 0 else []

    # Segmentos de clientes
    df_segs = execute_query("""
        SELECT DISTINCT segmento FROM DimCliente WHERE es_actual = 1 ORDER BY segmento
    """)
    filtros["segmentos"] = df_segs["segmento"].tolist() if len(df_segs) > 0 else []

    return filtros
