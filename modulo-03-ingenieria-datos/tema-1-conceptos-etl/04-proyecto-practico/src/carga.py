"""
Módulo de carga de datos en SQLite.

Este módulo contiene funciones para crear tablas, cargar datos de forma
idempotente y consultar datos desde una base de datos SQLite.
"""

import sqlite3
from typing import Any


def crear_tabla_ventas(db_path: str) -> None:
    """
    Crea la tabla ventas_procesadas si no existe.

    Args:
        db_path: Ruta a la base de datos SQLite

    Examples:
        >>> crear_tabla_ventas("ventas.db")
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas_procesadas (
            venta_id INTEGER,
            fecha TEXT,
            producto_id INTEGER,
            cliente_id INTEGER,
            cantidad INTEGER,
            precio_unitario REAL,
            total REAL,
            nombre_producto TEXT,
            categoria TEXT,
            nombre_cliente TEXT,
            ciudad TEXT,
            PRIMARY KEY (venta_id, fecha)
        )
    """
    )

    conn.commit()
    conn.close()


def cargar_ventas_idempotente(
    ventas: list[dict[str, Any]], fecha: str, db_path: str
) -> int:
    """
    Carga ventas en la base de datos de forma idempotente.

    Borra las ventas de la fecha especificada antes de insertar las nuevas,
    asegurando que ejecutar múltiples veces no duplique datos.

    Args:
        ventas: Lista de diccionarios con ventas a cargar
        fecha: Fecha de las ventas (formato: YYYY-MM-DD)
        db_path: Ruta a la base de datos SQLite

    Returns:
        Número de filas cargadas

    Examples:
        >>> ventas = [{"venta_id": 1, "fecha": "2025-10-01", ...}]
        >>> num_cargadas = cargar_ventas_idempotente(ventas, "2025-10-01", "ventas.db")
        >>> num_cargadas
        1
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # PASO 1: Borrar ventas de esa fecha (idempotencia)
        cursor.execute("DELETE FROM ventas_procesadas WHERE fecha = ?", (fecha,))

        # PASO 2: Insertar nuevas ventas
        for venta in ventas:
            cursor.execute(
                """
                INSERT INTO ventas_procesadas (
                    venta_id, fecha, producto_id, cliente_id,
                    cantidad, precio_unitario, total,
                    nombre_producto, categoria,
                    nombre_cliente, ciudad
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    venta["venta_id"],
                    venta["fecha"],
                    venta["producto_id"],
                    venta["cliente_id"],
                    venta["cantidad"],
                    venta["precio_unitario"],
                    venta["total"],
                    venta["nombre_producto"],
                    venta["categoria"],
                    venta["nombre_cliente"],
                    venta["ciudad"],
                ),
            )

        conn.commit()
        return len(ventas)

    finally:
        conn.close()


def consultar_ventas_por_fecha(fecha: str, db_path: str) -> list[dict[str, Any]]:
    """
    Consulta ventas de una fecha específica desde la base de datos.

    Args:
        fecha: Fecha a consultar (formato: YYYY-MM-DD)
        db_path: Ruta a la base de datos SQLite

    Returns:
        Lista de diccionarios con las ventas de esa fecha

    Examples:
        >>> ventas = consultar_ventas_por_fecha("2025-10-01", "ventas.db")
        >>> len(ventas) > 0
        True
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para retornar diccionarios
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT * FROM ventas_procesadas
            WHERE fecha = ?
            ORDER BY venta_id
            """,
            (fecha,),
        )

        rows = cursor.fetchall()
        # Convertir Row objects a diccionarios
        resultado = [dict(row) for row in rows]
        return resultado

    finally:
        conn.close()
