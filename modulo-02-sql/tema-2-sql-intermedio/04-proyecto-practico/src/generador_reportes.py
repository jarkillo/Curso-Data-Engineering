"""
Módulo generador_reportes: Genera reportes complejos con JOINs múltiples.

Este módulo proporciona funciones para generar reportes de negocio
usando queries SQL complejas con múltiples JOINs, subconsultas y CASE WHEN.
"""

import logging
import sqlite3
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generar_reporte_ventas(
    conexion: sqlite3.Connection,
    fecha_inicio: str,
    fecha_fin: str,
    agrupar_por: str = "categoria",
) -> list[dict[str, Any]]:
    """
    Genera reporte de ventas con múltiples JOINs.

    Args:
        conexion: Conexión SQLite activa
        fecha_inicio: Fecha inicial (YYYY-MM-DD)
        fecha_fin: Fecha final (YYYY-MM-DD)
        agrupar_por: 'categoria', 'producto', 'cliente', 'ciudad'

    Returns:
        Lista de dicts con:
            - nombre: str (categoría/producto/cliente)
            - total_ventas: float
            - unidades_vendidas: int
            - ticket_promedio: float

    Raises:
        ValueError: Si agrupar_por inválido o fechas incorrectas
        sqlite3.Error: Si hay error en la query

    Example:
        >>> reporte = generar_reporte_ventas(
        ...     conn, '2025-01-01', '2025-12-31', 'categoria'
        ... )
        >>> len(reporte) > 0
        True
    """
    # Validación
    agrupaciones_validas = ["categoria", "producto", "cliente", "ciudad"]
    if agrupar_por not in agrupaciones_validas:
        raise ValueError(
            f"agrupar_por inválido: '{agrupar_por}'. "
            f"Debe ser uno de: {', '.join(agrupaciones_validas)}"
        )

    if fecha_inicio > fecha_fin:
        raise ValueError("fecha_inicio debe ser menor o igual a fecha_fin")

    # Construir query según agrupación
    if agrupar_por == "categoria":
        query = """
            SELECT
                c.nombre AS nombre,
                ROUND(SUM(v.total), 2) AS total_ventas,
                SUM(v.cantidad) AS unidades_vendidas,
                ROUND(AVG(v.total), 2) AS ticket_promedio
            FROM categorias c
            INNER JOIN productos p ON c.id = p.categoria_id
            INNER JOIN ventas v ON p.id = v.producto_id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY c.nombre
            ORDER BY total_ventas DESC
        """
    elif agrupar_por == "producto":
        query = """
            SELECT
                p.nombre AS nombre,
                ROUND(SUM(v.total), 2) AS total_ventas,
                SUM(v.cantidad) AS unidades_vendidas,
                ROUND(AVG(v.total), 2) AS ticket_promedio
            FROM productos p
            INNER JOIN ventas v ON p.id = v.producto_id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY p.nombre
            ORDER BY total_ventas DESC
        """
    elif agrupar_por == "cliente":
        query = """
            SELECT
                cl.nombre AS nombre,
                ROUND(SUM(v.total), 2) AS total_ventas,
                SUM(v.cantidad) AS unidades_vendidas,
                ROUND(AVG(v.total), 2) AS ticket_promedio
            FROM clientes cl
            INNER JOIN ventas v ON cl.id = v.cliente_id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY cl.nombre
            ORDER BY total_ventas DESC
        """
    elif agrupar_por == "ciudad":
        query = """
            SELECT
                cl.ciudad AS nombre,
                ROUND(SUM(v.total), 2) AS total_ventas,
                SUM(v.cantidad) AS unidades_vendidas,
                ROUND(AVG(v.total), 2) AS ticket_promedio
            FROM clientes cl
            INNER JOIN ventas v ON cl.id = v.cliente_id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY cl.ciudad
            ORDER BY total_ventas DESC
        """

    # Ejecutar
    try:
        logger.info(
            f"Generando reporte de ventas por {agrupar_por} "
            f"({fecha_inicio} a {fecha_fin})"
        )
        cursor = conexion.cursor()
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultado = cursor.fetchall()

        # Convertir a diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"Reporte generado: {len(resultado_dict)} filas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error generando reporte: {str(e)}")
        raise sqlite3.Error(f"Error generando reporte: {str(e)}")


def generar_top_clientes(
    conexion: sqlite3.Connection,
    top_n: int = 10,
    metrica: str = "gasto_total",
) -> list[dict[str, Any]]:
    """
    Genera top N clientes usando subconsultas.

    Args:
        conexion: Conexión SQLite activa
        top_n: Número de clientes a retornar
        metrica: 'gasto_total', 'num_pedidos', 'ticket_promedio'

    Returns:
        Lista de dicts con:
            - nombre: str
            - email: str
            - gasto_total: float
            - num_pedidos: int
            - ticket_promedio: float
            - segmento: str ('VIP', 'Regular', 'Nuevo')

    Raises:
        ValueError: Si metrica inválida o top_n negativo
        sqlite3.Error: Si hay error en la query

    Example:
        >>> top = generar_top_clientes(conn, 5, 'gasto_total')
        >>> len(top) <= 5
        True
    """
    # Validación
    metricas_validas = ["gasto_total", "num_pedidos", "ticket_promedio"]
    if metrica not in metricas_validas:
        raise ValueError(
            f"metrica inválida: '{metrica}'. "
            f"Debe ser uno de: {', '.join(metricas_validas)}"
        )

    if top_n <= 0:
        raise ValueError("top_n debe ser positivo")

    # Query con segmentación CASE WHEN
    query = """
        SELECT
            c.nombre,
            c.email,
            ROUND(COALESCE(SUM(v.total), 0), 2) AS gasto_total,
            COUNT(v.id) AS num_pedidos,
            ROUND(COALESCE(AVG(v.total), 0), 2) AS ticket_promedio,
            CASE
                WHEN COALESCE(SUM(v.total), 0) >= 1000 THEN 'VIP'
                WHEN COUNT(v.id) >= 2 THEN 'Regular'
                WHEN COUNT(v.id) = 1 THEN 'Nuevo'
                ELSE 'Sin compras'
            END AS segmento
        FROM clientes c
        LEFT JOIN ventas v ON c.id = v.cliente_id
        GROUP BY c.id, c.nombre, c.email
        HAVING COUNT(v.id) > 0
        ORDER BY {order_by} DESC
        LIMIT ?
    """

    # Determinar ORDER BY según métrica
    if metrica == "gasto_total":
        order_by = "gasto_total"
    elif metrica == "num_pedidos":
        order_by = "num_pedidos"
    elif metrica == "ticket_promedio":
        order_by = "ticket_promedio"

    query_final = query.format(order_by=order_by)

    # Ejecutar
    try:
        logger.info(f"Generando top {top_n} clientes por {metrica}")
        cursor = conexion.cursor()
        cursor.execute(query_final, (top_n,))
        resultado = cursor.fetchall()

        # Convertir a diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"Top clientes generado: {len(resultado_dict)} filas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error generando top clientes: {str(e)}")
        raise sqlite3.Error(f"Error generando top clientes: {str(e)}")


def generar_analisis_categorias(
    conexion: sqlite3.Connection,
) -> list[dict[str, Any]]:
    """
    Análisis completo de categorías con CASE WHEN y GROUP BY.

    Args:
        conexion: Conexión SQLite activa

    Returns:
        Lista de dicts con:
            - categoria: str
            - num_productos: int
            - stock_total: int
            - valor_inventario: float
            - ingresos_totales: float
            - clasificacion: str ('Alta/Media/Baja rentabilidad')
            - estado_stock: str ('Crítico', 'Normal', 'Sobrecargado')

    Raises:
        sqlite3.Error: Si hay error en la query

    Example:
        >>> analisis = generar_analisis_categorias(conn)
        >>> len(analisis) == 4  # 4 categorías
        True
    """
    query = """
        SELECT
            c.nombre AS categoria,
            COUNT(p.id) AS num_productos,
            COALESCE(SUM(p.stock), 0) AS stock_total,
            ROUND(COALESCE(SUM(p.stock * p.precio), 0), 2) AS valor_inventario,
            ROUND(COALESCE(SUM(v.total), 0), 2) AS ingresos_totales,
            CASE
                WHEN COALESCE(SUM(v.total), 0) >= 1000
                    THEN 'Alta rentabilidad'
                WHEN COALESCE(SUM(v.total), 0) BETWEEN 300 AND 999
                    THEN 'Media rentabilidad'
                ELSE 'Baja rentabilidad'
            END AS clasificacion,
            CASE
                WHEN COALESCE(SUM(p.stock), 0) = 0 THEN 'Sin stock'
                WHEN COALESCE(SUM(p.stock), 0) < 50 THEN 'Crítico'
                WHEN COALESCE(SUM(p.stock), 0) BETWEEN 50 AND 150 THEN 'Normal'
                ELSE 'Sobrecargado'
            END AS estado_stock
        FROM categorias c
        LEFT JOIN productos p ON c.id = p.categoria_id AND p.activo = 1
        LEFT JOIN ventas v ON p.id = v.producto_id
        GROUP BY c.id, c.nombre
        ORDER BY ingresos_totales DESC
    """

    # Ejecutar
    try:
        logger.info("Generando análisis completo de categorías")
        cursor = conexion.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        # Convertir a diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"Análisis de categorías generado: {len(resultado_dict)} filas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error generando análisis de categorías: {str(e)}")
        raise sqlite3.Error(f"Error generando análisis de categorías: {str(e)}")
