"""
Módulo ejecutor_joins: Ejecuta queries SQL con JOINs de forma segura.

Este módulo proporciona funciones para ejecutar diferentes tipos de JOINs
con validación de parámetros, manejo de errores y logging.
"""

import logging
import sqlite3
from typing import Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tipos de JOIN válidos
JOINS_VALIDOS = ["INNER", "LEFT", "RIGHT", "FULL"]


def ejecutar_join_simple(
    conexion: sqlite3.Connection,
    tabla_izq: str,
    tabla_der: str,
    columna_union_izq: str,
    columna_union_der: str,
    tipo_join: str = "INNER",
    columnas_select: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Ejecuta un JOIN simple entre dos tablas.

    Args:
        conexion: Conexión SQLite activa
        tabla_izq: Nombre de tabla izquierda
        tabla_der: Nombre de tabla derecha
        columna_union_izq: Columna de join en tabla izquierda
        columna_union_der: Columna de join en tabla derecha
        tipo_join: Tipo de JOIN ('INNER', 'LEFT', 'RIGHT', 'FULL')
        columnas_select: Columnas a seleccionar (None = todas)

    Returns:
        Lista de diccionarios con resultados

    Raises:
        ValueError: Si tipo_join no es válido
        TypeError: Si conexion no es válida
        sqlite3.Error: Si hay error en la query

    Example:
        >>> conn = sqlite3.connect(':memory:')
        >>> # ... crear tablas ...
        >>> resultado = ejecutar_join_simple(
        ...     conn, 'productos', 'categorias',
        ...     'categoria_id', 'id', 'INNER'
        ... )
        >>> len(resultado) > 0
        True
    """
    # Validación de parámetros
    if tipo_join not in JOINS_VALIDOS:
        raise ValueError(
            f"tipo_join inválido: '{tipo_join}'. "
            f"Debe ser uno de: {', '.join(JOINS_VALIDOS)}"
        )

    if conexion is None or not isinstance(conexion, sqlite3.Connection):
        raise TypeError("conexion debe ser sqlite3.Connection válida")

    # Construir SELECT
    select_clause = "*" if columnas_select is None else ", ".join(columnas_select)

    # Construir query
    query = f"""
        SELECT {select_clause}
        FROM {tabla_izq}
        {tipo_join} JOIN {tabla_der}
            ON {tabla_izq}.{columna_union_izq} = {tabla_der}.{columna_union_der}
    """

    # Ejecutar query
    try:
        logger.info(f"Ejecutando {tipo_join} JOIN: {tabla_izq} + {tabla_der}")
        cursor = conexion.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        # Convertir a lista de diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"JOIN completado: {len(resultado_dict)} filas retornadas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error al ejecutar JOIN: {str(e)}")
        raise sqlite3.Error(f"Error al ejecutar JOIN: {str(e)}")


def ejecutar_join_multiple(
    conexion: sqlite3.Connection,
    tablas: list[dict[str, str]],
    columnas_select: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Ejecuta JOIN de 3+ tablas.

    Args:
        conexion: Conexión SQLite activa
        tablas: Lista de dicts con info de JOIN:
            [
                {'nombre': 'productos', 'alias': 'p'},
                {'nombre': 'categorias', 'alias': 'c',
                 'join': 'INNER', 'on': 'p.categoria_id = c.id'},
                ...
            ]
        columnas_select: Columnas a seleccionar (None = todas)

    Returns:
        Lista de diccionarios con resultados

    Raises:
        ValueError: Si tablas está vacía o formato incorrecto
        sqlite3.Error: Si hay error en la query

    Example:
        >>> tablas = [
        ...     {'nombre': 'productos', 'alias': 'p'},
        ...     {'nombre': 'categorias', 'alias': 'c',
        ...      'join': 'INNER', 'on': 'p.categoria_id = c.id'}
        ... ]
        >>> resultado = ejecutar_join_multiple(conn, tablas)
    """
    # Validación
    if not tablas or len(tablas) == 0:
        raise ValueError("tablas no puede estar vacía")

    # Validar formato de primera tabla
    if "nombre" not in tablas[0] or "alias" not in tablas[0]:
        raise ValueError("Primera tabla debe contener 'nombre' y 'alias'")

    # Validar formato de tablas restantes
    for tabla in tablas[1:]:
        if not all(k in tabla for k in ["nombre", "alias", "join", "on"]):
            raise ValueError(
                "Tablas adicionales deben contener: nombre, alias, join, on"
            )

    # Construir SELECT
    select_clause = "*" if columnas_select is None else ", ".join(columnas_select)

    # Construir FROM con primera tabla
    from_clause = f"{tablas[0]['nombre']} {tablas[0]['alias']}"

    # Construir JOINs
    joins = []
    for tabla in tablas[1:]:
        join_clause = (
            f"{tabla['join']} JOIN {tabla['nombre']} {tabla['alias']} ON {tabla['on']}"
        )
        joins.append(join_clause)

    # Query completa
    query = f"""
        SELECT {select_clause}
        FROM {from_clause}
        {" ".join(joins)}
    """

    # Ejecutar
    try:
        logger.info(f"Ejecutando JOIN múltiple: {len(tablas)} tablas")
        cursor = conexion.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        # Convertir a diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"JOIN múltiple completado: {len(resultado_dict)} filas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error en JOIN múltiple: {str(e)}")
        raise sqlite3.Error(f"Error en JOIN múltiple: {str(e)}")


def ejecutar_join_con_subconsulta(
    conexion: sqlite3.Connection,
    query_principal: str,
    subconsulta: str,
    tipo_subconsulta: str = "WHERE",
) -> list[dict[str, Any]]:
    """
    Ejecuta JOIN con subconsulta en WHERE, FROM o SELECT.

    Args:
        conexion: Conexión SQLite activa
        query_principal: Query base con placeholder {subconsulta}
        subconsulta: Query interna
        tipo_subconsulta: Ubicación ('WHERE', 'FROM', 'SELECT')

    Returns:
        Lista de diccionarios con resultados

    Raises:
        ValueError: Si tipo_subconsulta inválido o falta placeholder
        sqlite3.Error: Si hay error en la query

    Example:
        >>> query = "SELECT * FROM productos WHERE precio > {subconsulta}"
        >>> sub = "(SELECT AVG(precio) FROM productos)"
        >>> resultado = ejecutar_join_con_subconsulta(conn, query, sub, "WHERE")
    """
    # Validación
    tipos_validos = ["WHERE", "FROM", "SELECT"]
    if tipo_subconsulta not in tipos_validos:
        raise ValueError(
            f"tipo_subconsulta inválido: '{tipo_subconsulta}'. "
            f"Debe ser uno de: {', '.join(tipos_validos)}"
        )

    if "{subconsulta}" not in query_principal:
        raise ValueError("query_principal debe contener placeholder {subconsulta}")

    # Reemplazar placeholder
    query_final = query_principal.replace("{subconsulta}", subconsulta)

    # Ejecutar
    try:
        logger.info(f"Ejecutando query con subconsulta en {tipo_subconsulta}")
        cursor = conexion.cursor()
        cursor.execute(query_final)
        resultado = cursor.fetchall()

        # Convertir a diccionarios
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultado_dict = [dict(zip(columnas, fila, strict=False)) for fila in resultado]

        logger.info(f"Query con subconsulta completada: {len(resultado_dict)} filas")

        return resultado_dict

    except sqlite3.Error as e:
        logger.error(f"Error en query con subconsulta: {str(e)}")
        raise sqlite3.Error(f"Error en query con subconsulta: {str(e)}")
