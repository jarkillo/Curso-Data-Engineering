"""
Módulo de Almacenamiento
=========================

Funciones para guardar datos scrapeados en SQLite.
"""

import sqlite3
from typing import Dict, List, Optional


def crear_tabla_productos(db_path: str = "datos/productos.db") -> None:
    """
    Crea la tabla 'productos' en SQLite si no existe.

    Schema:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - nombre: TEXT NOT NULL
        - precio: REAL
        - url: TEXT
        - descripcion: TEXT
        - fecha_scraping: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    Args:
        db_path: Ruta al archivo de base de datos

    Raises:
        ValueError: Si db_path está vacío
        sqlite3.Error: Si hay error de BD
    """
    if not db_path or db_path.strip() == "":
        raise ValueError("db_path no puede estar vacío")

    # Crear directorio si no existe
    import os

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL,
            url TEXT,
            descripcion TEXT,
            fecha_scraping TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def guardar_productos(
    productos: List[Dict[str, str]], db_path: str = "datos/productos.db"
) -> int:
    """
    Guarda una lista de productos en la base de datos.

    Args:
        productos: Lista de diccionarios con keys: nombre, precio, url, descripcion
        db_path: Ruta al archivo de base de datos

    Returns:
        Número de productos insertados exitosamente

    Raises:
        ValueError: Si la lista está vacía o productos mal formados
        sqlite3.Error: Si hay error en la inserción
    """
    if not productos or len(productos) == 0:
        raise ValueError("La lista de productos no puede estar vacía")

    # Validar que todos los productos tengan los campos requeridos
    campos_requeridos = ["nombre", "precio", "url", "descripcion"]
    for producto in productos:
        for campo in campos_requeridos:
            if campo not in producto:
                raise ValueError(f"Producto mal formado: falta el campo '{campo}'")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insertados = 0
    for producto in productos:
        cursor.execute(
            """
            INSERT INTO productos (nombre, precio, url, descripcion)
            VALUES (?, ?, ?, ?)
        """,
            (
                producto["nombre"],
                float(producto["precio"]) if producto["precio"] else None,
                producto["url"],
                producto["descripcion"],
            ),
        )
        insertados += 1

    conn.commit()
    conn.close()

    return insertados


def obtener_productos(
    db_path: str = "datos/productos.db", limite: Optional[int] = None
) -> List[Dict[str, str]]:
    """
    Obtiene productos de la base de datos.

    Args:
        db_path: Ruta al archivo de base de datos
        limite: Número máximo de productos a retornar (None = todos)

    Returns:
        Lista de diccionarios con los productos

    Raises:
        ValueError: Si limite es negativo
        sqlite3.Error: Si hay error en la consulta
    """
    if limite is not None and limite < 0:
        raise ValueError("El límite no puede ser negativo")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
    cursor = conn.cursor()

    if limite is not None:
        cursor.execute("SELECT * FROM productos LIMIT ?", (limite,))
    else:
        cursor.execute("SELECT * FROM productos")

    filas = cursor.fetchall()
    conn.close()

    # Convertir Row a diccionarios
    resultado = []
    for fila in filas:
        resultado.append(
            {
                "id": str(fila["id"]),
                "nombre": fila["nombre"],
                "precio": str(fila["precio"]) if fila["precio"] else "",
                "url": fila["url"] or "",
                "descripcion": fila["descripcion"] or "",
                "fecha_scraping": fila["fecha_scraping"] or "",
            }
        )

    return resultado
