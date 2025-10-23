"""
Módulo de consultas SQL con funciones agregadas.

Este módulo contiene funciones para realizar consultas con
COUNT, SUM, AVG, MAX y MIN.
"""

from src.conexion_db import ConexionSQLite


def contar_productos(conexion: ConexionSQLite) -> int:
    """
    Cuenta el total de productos en la base de datos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Número total de productos

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> total = contar_productos(conn)
        >>> isinstance(total, int)
        True
        >>> total > 0
        True
    """
    query = "SELECT COUNT(*) AS total FROM productos"
    resultado = conexion.ejecutar_query(query)
    return int(resultado[0]["total"])


def calcular_precio_promedio(conexion: ConexionSQLite) -> float:
    """
    Calcula el precio promedio de todos los productos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Precio promedio redondeado a 2 decimales

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> promedio = calcular_precio_promedio(conn)
        >>> isinstance(promedio, float)
        True
        >>> promedio > 0
        True
    """
    query = "SELECT ROUND(AVG(precio), 2) AS promedio FROM productos"
    resultado = conexion.ejecutar_query(query)
    return float(resultado[0]["promedio"])


def obtener_estadisticas_precios(conexion: ConexionSQLite) -> dict:
    """
    Obtiene estadísticas de precios (min, max, avg, count).

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Diccionario con claves: 'minimo', 'maximo', 'promedio', 'total'

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> stats = obtener_estadisticas_precios(conn)
        >>> stats.keys()
        dict_keys(['minimo', 'maximo', 'promedio', 'total'])
        >>> stats['minimo'] <= stats['maximo']
        True
        >>> stats['total'] > 0
        True
    """
    query = """
        SELECT
            MIN(precio) AS minimo,
            MAX(precio) AS maximo,
            ROUND(AVG(precio), 2) AS promedio,
            COUNT(*) AS total
        FROM productos
    """
    resultado = conexion.ejecutar_query(query)
    return {
        "minimo": float(resultado[0]["minimo"]),
        "maximo": float(resultado[0]["maximo"]),
        "promedio": float(resultado[0]["promedio"]),
        "total": int(resultado[0]["total"]),
    }


def calcular_ingresos_totales(conexion: ConexionSQLite) -> float:
    """
    Calcula los ingresos totales de todas las ventas.

    Los ingresos se calculan como: cantidad * precio_unitario

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Ingresos totales redondeados a 2 decimales

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> ingresos = calcular_ingresos_totales(conn)
        >>> isinstance(ingresos, float)
        True
        >>> ingresos > 0
        True
    """
    query = """
        SELECT ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos
        FROM ventas
    """
    resultado = conexion.ejecutar_query(query)
    return float(resultado[0]["ingresos"])
