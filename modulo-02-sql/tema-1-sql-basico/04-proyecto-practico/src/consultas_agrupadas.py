"""
Módulo de consultas SQL con GROUP BY y HAVING.

Este módulo contiene funciones para realizar consultas con
agrupamiento y filtrado de grupos.
"""

from src.conexion_db import ConexionSQLite


def contar_productos_por_categoria(conexion: ConexionSQLite) -> list[dict]:
    """
    Cuenta productos por categoría.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con 'categoria' y 'cantidad'
        Ordenado por cantidad descendente

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> resultados = contar_productos_por_categoria(conn)
        >>> all('categoria' in r and 'cantidad' in r for r in resultados)
        True
        >>> # Verificar que está ordenado descendente
        >>> cantidades = [r['cantidad'] for r in resultados]
        >>> cantidades == sorted(cantidades, reverse=True)
        True
    """
    query = """
        SELECT
            categoria,
            COUNT(*) AS cantidad
        FROM productos
        GROUP BY categoria
        ORDER BY cantidad DESC
    """
    return conexion.ejecutar_query(query)


def calcular_valor_inventario_por_categoria(conexion: ConexionSQLite) -> list[dict]:
    """
    Calcula el valor total de inventario por categoría.

    El valor se calcula como: precio * stock_actual

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con 'categoria', 'valor_inventario'
        Ordenado por valor descendente

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> resultados = calcular_valor_inventario_por_categoria(conn)
        >>> all('categoria' in r and 'valor_inventario' in r for r in resultados)
        True
        >>> # Verificar que está ordenado descendente
        >>> valores = [r['valor_inventario'] for r in resultados]
        >>> valores == sorted(valores, reverse=True)
        True
    """
    query = """
        SELECT
            categoria,
            ROUND(SUM(precio * stock_actual), 2) AS valor_inventario
        FROM productos
        GROUP BY categoria
        ORDER BY valor_inventario DESC
    """
    return conexion.ejecutar_query(query)


def obtener_categorias_con_mas_de_n_productos(
    conexion: ConexionSQLite, n: int = 1
) -> list[dict]:
    """
    Obtiene categorías que tienen más de N productos.

    Args:
        conexion: Instancia de ConexionSQLite
        n: Número mínimo de productos (default: 1)

    Returns:
        Lista de categorías con cantidad de productos

    Raises:
        ValueError: Si n < 0
        TypeError: Si n no es entero

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> # Categorías con más de 1 producto
        >>> resultados = obtener_categorias_con_mas_de_n_productos(conn, 1)
        >>> all(r['cantidad'] > 1 for r in resultados)
        True
    """
    if n < 0:
        raise ValueError("El parámetro 'n' no puede ser negativo")

    if not isinstance(n, int):
        raise TypeError("El parámetro 'n' debe ser un entero")

    query = """
        SELECT
            categoria,
            COUNT(*) AS cantidad
        FROM productos
        GROUP BY categoria
        HAVING COUNT(*) > ?
        ORDER BY cantidad DESC
    """
    return conexion.ejecutar_query(query, (n,))


def analizar_ventas_por_producto(conexion: ConexionSQLite) -> list[dict]:
    """
    Analiza ventas agrupadas por producto.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con:
        - 'producto_id'
        - 'unidades_vendidas'
        - 'ingresos_totales'
        Ordenado por ingresos descendente

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> resultados = analizar_ventas_por_producto(conn)
        >>> all('producto_id' in r for r in resultados)
        True
        >>> all('unidades_vendidas' in r for r in resultados)
        True
        >>> all('ingresos_totales' in r for r in resultados)
        True
        >>> # Verificar que está ordenado por ingresos descendente
        >>> ingresos = [r['ingresos_totales'] for r in resultados]
        >>> ingresos == sorted(ingresos, reverse=True)
        True
    """
    query = """
        SELECT
            producto_id,
            SUM(cantidad) AS unidades_vendidas,
            ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos_totales
        FROM ventas
        GROUP BY producto_id
        ORDER BY ingresos_totales DESC
    """
    return conexion.ejecutar_query(query)
