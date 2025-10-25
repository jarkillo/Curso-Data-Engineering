"""
Módulo de conexión a PostgreSQL.

Proporciona funciones para conectar y desconectar de PostgreSQL de forma segura.
"""

import os
from typing import Optional

import psycopg2
from psycopg2.extensions import connection


def crear_conexion(
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
) -> connection:
    """
    Crea una conexión a PostgreSQL.

    Args:
        host: Hostname del servidor (por defecto desde ENV)
        port: Puerto del servidor (por defecto desde ENV)
        user: Usuario de la base de datos (por defecto desde ENV)
        password: Contraseña (por defecto desde ENV)
        database: Nombre de la base de datos (por defecto desde ENV)

    Returns:
        Objeto de conexión psycopg2

    Raises:
        ValueError: Si faltan credenciales
        psycopg2.Error: Si falla la conexión

    Examples:
        >>> conn = crear_conexion()
        >>> conn.closed
        0
    """
    # Usar valores de ENV si no se proporcionan
    host = host or os.getenv("POSTGRES_HOST", "localhost")
    port = port or int(os.getenv("POSTGRES_PORT", "5432"))
    user = user or os.getenv("POSTGRES_USER")
    password = password or os.getenv("POSTGRES_PASSWORD")
    database = database or os.getenv("POSTGRES_DB")

    # Validar que tenemos todas las credenciales
    if not all([host, user, password, database]):
        raise ValueError(
            "Faltan credenciales de conexión. "
            "Proporciónalas como parámetros o en variables de entorno."
        )

    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        return conn
    except psycopg2.Error as e:
        raise psycopg2.Error(f"Error al conectar a PostgreSQL: {e}")


def cerrar_conexion(conn: connection) -> None:
    """
    Cierra una conexión a PostgreSQL de forma segura.

    Args:
        conn: Conexión a cerrar

    Raises:
        TypeError: Si conn no es una conexión válida

    Examples:
        >>> conn = crear_conexion()
        >>> cerrar_conexion(conn)
        >>> conn.closed
        1
    """
    if not hasattr(conn, "close") or not hasattr(conn, "closed"):
        raise TypeError("El parámetro debe ser una conexión psycopg2")

    if not conn.closed:
        conn.close()


def ejecutar_query(
    conn: connection, query: str, params: Optional[tuple] = None
) -> list[tuple]:
    """
    Ejecuta una query SELECT y retorna los resultados.

    Args:
        conn: Conexión a PostgreSQL
        query: Query SQL a ejecutar
        params: Parámetros para la query (prevención SQL injection)

    Returns:
        Lista de tuplas con los resultados

    Raises:
        TypeError: Si conn no es una conexión válida
        psycopg2.Error: Si falla la ejecución

    Examples:
        >>> conn = crear_conexion()
        >>> resultados = ejecutar_query(conn, "SELECT 1 + 1 AS suma")
        >>> resultados[0][0]
        2
    """
    if not hasattr(conn, "cursor"):
        raise TypeError("El parámetro conn debe ser una conexión psycopg2")

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # type: ignore[no-any-return]
    except psycopg2.Error as e:
        conn.rollback()
        raise psycopg2.Error(f"Error al ejecutar query: {e}")
