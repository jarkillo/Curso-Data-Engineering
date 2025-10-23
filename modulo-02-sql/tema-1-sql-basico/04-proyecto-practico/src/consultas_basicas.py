"""
Módulo de consultas SQL básicas.

Este módulo contiene funciones para realizar consultas básicas
usando SELECT, WHERE, ORDER BY y LIMIT.
"""

from src.conexion_db import ConexionSQLite
from src.validaciones import (
    validar_categoria_no_vacia,
    validar_numero_positivo,
    validar_precio_positivo,
)


def obtener_todos_los_productos(conexion: ConexionSQLite) -> list[dict]:
    """
    Obtiene todos los productos de la tabla productos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de diccionarios con todos los productos

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> productos = obtener_todos_los_productos(conn)
        >>> len(productos)
        10
        >>> productos[0].keys()
        dict_keys(['id', 'nombre', 'precio', 'categoria', 'stock_actual', 'proveedor'])
    """
    query = """
        SELECT id, nombre, precio, categoria, stock_actual, proveedor
        FROM productos
    """
    return conexion.ejecutar_query(query)


def filtrar_productos_por_categoria(
    conexion: ConexionSQLite, categoria: str
) -> list[dict]:
    """
    Filtra productos por categoría.

    Args:
        conexion: Instancia de ConexionSQLite
        categoria: Nombre de la categoría (ej: "Accesorios")

    Returns:
        Lista de productos de esa categoría

    Raises:
        ValueError: Si la categoría está vacía
        TypeError: Si la categoría no es string

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> accesorios = filtrar_productos_por_categoria(conn, "Accesorios")
        >>> all(p['categoria'] == 'Accesorios' for p in accesorios)
        True
    """
    validar_categoria_no_vacia(categoria)

    query = """
        SELECT id, nombre, precio, categoria, stock_actual, proveedor
        FROM productos
        WHERE categoria = ?
    """
    return conexion.ejecutar_query(query, (categoria,))


def obtener_productos_caros(
    conexion: ConexionSQLite, precio_minimo: float
) -> list[dict]:
    """
    Obtiene productos con precio mayor al mínimo especificado.

    Los resultados se ordenan por precio descendente (más caro primero).

    Args:
        conexion: Instancia de ConexionSQLite
        precio_minimo: Precio mínimo (debe ser > 0)

    Returns:
        Lista de productos ordenados por precio descendente

    Raises:
        ValueError: Si precio_minimo <= 0
        TypeError: Si precio_minimo no es numérico

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> caros = obtener_productos_caros(conn, 500.0)
        >>> all(p['precio'] > 500.0 for p in caros)
        True
        >>> # Verificar que están ordenados de más caro a más barato
        >>> precios = [p['precio'] for p in caros]
        >>> precios == sorted(precios, reverse=True)
        True
    """
    validar_precio_positivo(precio_minimo)

    query = """
        SELECT id, nombre, precio, categoria, stock_actual, proveedor
        FROM productos
        WHERE precio > ?
        ORDER BY precio DESC
    """
    return conexion.ejecutar_query(query, (precio_minimo,))


def obtener_top_n_productos_mas_caros(
    conexion: ConexionSQLite, n: int = 5
) -> list[dict]:
    """
    Obtiene los N productos más caros.

    Args:
        conexion: Instancia de ConexionSQLite
        n: Cantidad de productos a retornar (default: 5)

    Returns:
        Lista de N productos más caros, ordenados por precio descendente

    Raises:
        ValueError: Si n <= 0
        TypeError: Si n no es entero

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> top_5 = obtener_top_n_productos_mas_caros(conn, 5)
        >>> len(top_5)
        5
        >>> # El más caro debe ser el primero
        >>> top_5[0]['precio'] >= top_5[1]['precio']
        True
    """
    validar_numero_positivo(n, "n")

    query = """
        SELECT id, nombre, precio, categoria, stock_actual, proveedor
        FROM productos
        ORDER BY precio DESC
        LIMIT ?
    """
    return conexion.ejecutar_query(query, (n,))
