"""
Fixtures compartidas para todos los tests.

Este archivo define fixtures de pytest que se usan en múltiples tests.
"""

import sqlite3
from typing import Any, Generator

import pytest


@pytest.fixture
def conexion_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Crea una base de datos SQLite en memoria con datos de TechStore.

    Yields:
        Conexión SQLite activa con datos de prueba
    """
    conn = sqlite3.Connection(":memory:")
    conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna

    # Crear tablas
    crear_tablas(conn)

    # Insertar datos de prueba
    insertar_datos(conn)

    yield conn

    # Cleanup
    conn.close()


def crear_tablas(conn: sqlite3.Connection) -> None:
    """Crea todas las tablas necesarias para los tests."""
    cursor = conn.cursor()

    # Tabla categorias
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    """
    )

    # Tabla productos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria_id INTEGER,
            stock INTEGER DEFAULT 0,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """
    )

    # Tabla clientes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            fecha_registro DATE NOT NULL,
            ciudad TEXT
        )
    """
    )

    # Tabla ventas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY,
            cliente_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha DATE NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """
    )

    conn.commit()


def insertar_datos(conn: sqlite3.Connection) -> None:
    """Inserta datos de prueba de TechStore."""
    cursor = conn.cursor()

    # Categorías
    cursor.executemany(
        "INSERT INTO categorias (id, nombre, descripcion) VALUES (?, ?, ?)",
        [
            (1, "Computadoras", "Laptops, desktops y componentes"),
            (2, "Accesorios", "Mouse, teclados, webcams"),
            (3, "Audio", "Audífonos, bocinas, micrófonos"),
            (4, "Almacenamiento", "Discos duros, SSDs, USB"),
        ],
    )

    # Productos
    cursor.executemany(
        """
        INSERT INTO productos (id, nombre, precio, categoria_id, stock, activo)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "Laptop HP Pavilion", 899.99, 1, 15, 1),
            (2, "Laptop Dell XPS", 1299.99, 1, 8, 1),
            (3, "Mouse Logitech MX", 79.99, 2, 50, 1),
            (4, "Teclado Mecánico", 129.99, 2, 30, 1),
            (5, "Webcam HD", 59.99, 2, 25, 1),
            (6, "Audífonos Sony", 199.99, 3, 20, 1),
            (7, "Bocina Bluetooth", 89.99, 3, 35, 1),
            (8, "SSD 1TB Samsung", 149.99, 4, 40, 1),
            (9, "Disco Duro 2TB", 89.99, 4, 45, 1),
            (10, "Tablet obsoleta", 299.99, 1, 0, 0),
        ],
    )

    # Clientes
    cursor.executemany(
        """
        INSERT INTO clientes (id, nombre, email, fecha_registro, ciudad)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "Ana García", "ana@email.com", "2024-01-15", "Madrid"),
            (2, "Carlos López", "carlos@email.com", "2024-02-20", "Barcelona"),
            (3, "María Rodríguez", "maria@email.com", "2024-03-10", "Valencia"),
            (4, "Juan Martínez", "juan@email.com", "2024-04-05", "Sevilla"),
            (5, "Laura Sánchez", "laura@email.com", "2024-10-01", "Madrid"),
        ],
    )

    # Ventas
    cursor.executemany(
        """
        INSERT INTO ventas (id, cliente_id, producto_id, cantidad, fecha, total)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, 1, 1, 1, "2025-01-15", 899.99),
            (2, 1, 3, 2, "2025-01-16", 159.98),
            (3, 2, 2, 1, "2025-01-20", 1299.99),
            (4, 2, 6, 1, "2025-01-21", 199.99),
            (5, 3, 4, 1, "2025-02-05", 129.99),
            (6, 3, 8, 2, "2025-02-05", 299.98),
            (7, 1, 7, 1, "2025-02-10", 89.99),
            (8, 4, 3, 3, "2025-02-15", 239.97),
            (9, 2, 9, 1, "2025-03-01", 89.99),
            (10, 1, 5, 1, "2025-03-05", 59.99),
        ],
    )

    conn.commit()


@pytest.fixture
def datos_productos() -> list[dict[str, Any]]:
    """
    Datos de prueba de productos.

    Returns:
        Lista de diccionarios con información de productos
    """
    return [
        {
            "id": 1,
            "nombre": "Laptop HP Pavilion",
            "precio": 899.99,
            "categoria_id": 1,
            "stock": 15,
            "activo": 1,
        },
        {
            "id": 2,
            "nombre": "Laptop Dell XPS",
            "precio": 1299.99,
            "categoria_id": 1,
            "stock": 8,
            "activo": 1,
        },
        {
            "id": 3,
            "nombre": "Mouse Logitech MX",
            "precio": 79.99,
            "categoria_id": 2,
            "stock": 50,
            "activo": 1,
        },
    ]


@pytest.fixture
def datos_categorias() -> list[dict[str, Any]]:
    """
    Datos de prueba de categorías.

    Returns:
        Lista de diccionarios con información de categorías
    """
    return [
        {"id": 1, "nombre": "Computadoras", "descripcion": "Laptops y componentes"},
        {"id": 2, "nombre": "Accesorios", "descripcion": "Mouse, teclados, webcams"},
        {"id": 3, "nombre": "Audio", "descripcion": "Audífonos y bocinas"},
    ]


@pytest.fixture
def datos_clientes() -> list[dict[str, Any]]:
    """
    Datos de prueba de clientes.

    Returns:
        Lista de diccionarios con información de clientes
    """
    return [
        {
            "id": 1,
            "nombre": "Ana García",
            "email": "ana@email.com",
            "fecha_registro": "2024-01-15",
            "ciudad": "Madrid",
        },
        {
            "id": 2,
            "nombre": "Carlos López",
            "email": "carlos@email.com",
            "fecha_registro": "2024-02-20",
            "ciudad": "Barcelona",
        },
        {
            "id": 5,
            "nombre": "Laura Sánchez",
            "email": "laura@email.com",
            "fecha_registro": "2024-10-01",
            "ciudad": "Madrid",
        },
    ]


@pytest.fixture
def datos_ventas() -> list[dict[str, Any]]:
    """
    Datos de prueba de ventas.

    Returns:
        Lista de diccionarios con información de ventas
    """
    return [
        {
            "id": 1,
            "cliente_id": 1,
            "producto_id": 1,
            "cantidad": 1,
            "fecha": "2025-01-15",
            "total": 899.99,
        },
        {
            "id": 2,
            "cliente_id": 1,
            "producto_id": 3,
            "cantidad": 2,
            "fecha": "2025-01-16",
            "total": 159.98,
        },
        {
            "id": 3,
            "cliente_id": 2,
            "producto_id": 2,
            "cantidad": 1,
            "fecha": "2025-01-20",
            "total": 1299.99,
        },
    ]
