"""
Módulo para operaciones con JSONB en PostgreSQL.

Proporciona funciones para insertar, consultar y manipular datos JSONB.
"""

import json
from typing import Any

import psycopg2
from psycopg2.extensions import connection


def insertar_json(conn: connection, tabla: str, columna_json: str, datos: dict) -> int:
    """
    Inserta un documento JSON en una tabla.

    Args:
        conn: Conexión a PostgreSQL
        tabla: Nombre de la tabla
        columna_json: Nombre de la columna JSONB
        datos: Diccionario con los datos a insertar

    Returns:
        ID del registro insertado

    Raises:
        TypeError: Si datos no es un diccionario
        ValueError: Si tabla o columna_json están vacíos
        psycopg2.Error: Si falla la inserción

    Examples:
        >>> conn = crear_conexion()
        >>> id = insertar_json(conn, "eventos", "datos", {"user": "ana"})
        >>> id > 0
        True
    """
    if not isinstance(datos, dict):
        raise TypeError("Los datos deben ser un diccionario")

    if not tabla or not columna_json:
        raise ValueError("Tabla y columna_json no pueden estar vacíos")

    try:
        json_str = json.dumps(datos)

        with conn.cursor() as cursor:
            query = f"""
                INSERT INTO {tabla} ({columna_json})
                VALUES (%s)
                RETURNING id
            """
            cursor.execute(query, (json_str,))
            result = cursor.fetchone()
            conn.commit()

            if result:
                return result[0]  # type: ignore[no-any-return]
            raise psycopg2.Error("No se pudo obtener el ID insertado")

    except (json.JSONDecodeError, psycopg2.Error) as e:
        conn.rollback()
        raise psycopg2.Error(f"Error al insertar JSON: {e}")


def consultar_json_por_campo(
    conn: connection, tabla: str, columna_json: str, campo: str, valor: Any
) -> list[dict]:
    """
    Consulta registros donde un campo JSON tiene un valor específico.

    Args:
        conn: Conexión a PostgreSQL
        tabla: Nombre de la tabla
        columna_json: Nombre de la columna JSONB
        campo: Campo dentro del JSON
        valor: Valor a buscar

    Returns:
        Lista de diccionarios con los resultados

    Raises:
        ValueError: Si los parámetros están vacíos
        psycopg2.Error: Si falla la consulta

    Examples:
        >>> resultados = consultar_json_por_campo(
        ...     conn, "eventos", "datos", "user", "ana"
        ... )
        >>> len(resultados) >= 0
        True
    """
    if not all([tabla, columna_json, campo]):
        raise ValueError("Tabla, columna_json y campo no pueden estar vacíos")

    try:
        with conn.cursor() as cursor:
            query = f"""
                SELECT id, {columna_json}
                FROM {tabla}
                WHERE {columna_json}->>%s = %s
            """
            cursor.execute(query, (campo, str(valor)))
            resultados = cursor.fetchall()

            return [{"id": row[0], "datos": row[1]} for row in resultados]

    except psycopg2.Error as e:
        raise psycopg2.Error(f"Error al consultar JSON: {e}")


def actualizar_campo_json(
    conn: connection,
    tabla: str,
    columna_json: str,
    id_registro: int,
    campo: str,
    nuevo_valor: Any,
) -> bool:
    """
    Actualiza un campo específico dentro de un JSON.

    Args:
        conn: Conexión a PostgreSQL
        tabla: Nombre de la tabla
        columna_json: Nombre de la columna JSONB
        id_registro: ID del registro a actualizar
        campo: Campo dentro del JSON a actualizar
        nuevo_valor: Nuevo valor para el campo

    Returns:
        True si se actualizó correctamente

    Raises:
        ValueError: Si los parámetros son inválidos
        psycopg2.Error: Si falla la actualización

    Examples:
        >>> actualizado = actualizar_campo_json(
        ...     conn, "eventos", "datos", 1, "status", "procesado"
        ... )
        >>> actualizado
        True
    """
    if not all([tabla, columna_json, campo]):
        raise ValueError("Tabla, columna_json y campo no pueden estar vacíos")

    if id_registro <= 0:
        raise ValueError("El ID debe ser mayor a 0")

    try:
        with conn.cursor() as cursor:
            query = f"""
                UPDATE {tabla}
                SET {columna_json} = jsonb_set(
                    {columna_json},
                    '{{{campo}}}',
                    %s::jsonb
                )
                WHERE id = %s
            """
            cursor.execute(query, (json.dumps(nuevo_valor), id_registro))
            conn.commit()

            return cursor.rowcount > 0  # type: ignore[no-any-return]

    except (json.JSONDecodeError, psycopg2.Error) as e:
        conn.rollback()
        raise psycopg2.Error(f"Error al actualizar campo JSON: {e}")
