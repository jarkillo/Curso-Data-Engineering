"""
Fixtures compartidas para tests del proyecto SQL Básico.

Este módulo contiene fixtures de pytest que se comparten entre
todos los archivos de tests.
"""

import sqlite3

import pytest


@pytest.fixture
def db_en_memoria():
    """
    Crea una base de datos SQLite en memoria para tests.

    Yields:
        sqlite3.Connection: Conexión a la base de datos de prueba

    Examples:
        >>> def test_algo(db_en_memoria):
        ...     cursor = db_en_memoria.cursor()
        ...     cursor.execute("SELECT * FROM productos")
        ...     resultados = cursor.fetchall()
    """
    conexion = sqlite3.connect(":memory:")
    conexion.row_factory = sqlite3.Row  # Para acceder por nombre de columna

    # Crear tablas
    cursor = conexion.cursor()

    # Tabla productos
    cursor.execute(
        """
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock_actual INTEGER NOT NULL,
            proveedor TEXT
        )
    """
    )

    # Tabla ventas
    cursor.execute(
        """
        CREATE TABLE ventas (
            id INTEGER PRIMARY KEY,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """
    )

    # Insertar datos de prueba
    productos = [
        (1, "Laptop HP Pavilion", 899.99, "Computadoras", 15, "HP Inc"),
        (2, "Mouse Logitech MX Master", 99.99, "Accesorios", 45, "Logitech"),
        (3, "Teclado Mecánico Corsair", 149.99, "Accesorios", 30, "Corsair"),
        (4, 'Monitor Samsung 27"', 299.99, "Monitores", 20, "Samsung"),
        (5, 'MacBook Pro 14"', 1999.99, "Computadoras", 8, "Apple"),
        (6, "iPhone 15 Pro", 1199.99, "Smartphones", 25, "Apple"),
        (7, "iPad Air", 599.99, "Tablets", 18, "Apple"),
        (8, "AirPods Pro", 249.99, "Accesorios", 50, "Apple"),
        (9, "Dell XPS 15", 1499.99, "Computadoras", 12, "Dell"),
        (10, "Webcam Logitech C920", 79.99, "Accesorios", 35, "Logitech"),
    ]

    cursor.executemany("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?)", productos)

    ventas = [
        (1, 1, 2, "2025-10-01", 899.99),
        (2, 2, 5, "2025-10-02", 99.99),
        (3, 3, 3, "2025-10-03", 149.99),
        (4, 6, 1, "2025-10-05", 1199.99),
        (5, 8, 4, "2025-10-07", 249.99),
        (6, 1, 1, "2025-10-10", 899.99),
        (7, 5, 1, "2025-10-12", 1999.99),
        (8, 2, 3, "2025-10-15", 99.99),
        (9, 4, 2, "2025-10-18", 299.99),
        (10, 9, 1, "2025-10-20", 1499.99),
    ]

    cursor.executemany("INSERT INTO ventas VALUES (?, ?, ?, ?, ?)", ventas)

    conexion.commit()

    yield conexion

    conexion.close()


@pytest.fixture
def productos_esperados():
    """
    Retorna lista de productos esperados para validación.

    Returns:
        list[dict]: Lista de productos con todos los campos
    """
    return [
        {
            "id": 1,
            "nombre": "Laptop HP Pavilion",
            "precio": 899.99,
            "categoria": "Computadoras",
            "stock_actual": 15,
            "proveedor": "HP Inc",
        },
        {
            "id": 2,
            "nombre": "Mouse Logitech MX Master",
            "precio": 99.99,
            "categoria": "Accesorios",
            "stock_actual": 45,
            "proveedor": "Logitech",
        },
        {
            "id": 3,
            "nombre": "Teclado Mecánico Corsair",
            "precio": 149.99,
            "categoria": "Accesorios",
            "stock_actual": 30,
            "proveedor": "Corsair",
        },
        {
            "id": 4,
            "nombre": 'Monitor Samsung 27"',
            "precio": 299.99,
            "categoria": "Monitores",
            "stock_actual": 20,
            "proveedor": "Samsung",
        },
        {
            "id": 5,
            "nombre": 'MacBook Pro 14"',
            "precio": 1999.99,
            "categoria": "Computadoras",
            "stock_actual": 8,
            "proveedor": "Apple",
        },
        {
            "id": 6,
            "nombre": "iPhone 15 Pro",
            "precio": 1199.99,
            "categoria": "Smartphones",
            "stock_actual": 25,
            "proveedor": "Apple",
        },
        {
            "id": 7,
            "nombre": "iPad Air",
            "precio": 599.99,
            "categoria": "Tablets",
            "stock_actual": 18,
            "proveedor": "Apple",
        },
        {
            "id": 8,
            "nombre": "AirPods Pro",
            "precio": 249.99,
            "categoria": "Accesorios",
            "stock_actual": 50,
            "proveedor": "Apple",
        },
        {
            "id": 9,
            "nombre": "Dell XPS 15",
            "precio": 1499.99,
            "categoria": "Computadoras",
            "stock_actual": 12,
            "proveedor": "Dell",
        },
        {
            "id": 10,
            "nombre": "Webcam Logitech C920",
            "precio": 79.99,
            "categoria": "Accesorios",
            "stock_actual": 35,
            "proveedor": "Logitech",
        },
    ]


@pytest.fixture
def ventas_esperadas():
    """
    Retorna lista de ventas esperadas para validación.

    Returns:
        list[dict]: Lista de ventas con todos los campos
    """
    return [
        {
            "id": 1,
            "producto_id": 1,
            "cantidad": 2,
            "fecha": "2025-10-01",
            "precio_unitario": 899.99,
        },
        {
            "id": 2,
            "producto_id": 2,
            "cantidad": 5,
            "fecha": "2025-10-02",
            "precio_unitario": 99.99,
        },
        {
            "id": 3,
            "producto_id": 3,
            "cantidad": 3,
            "fecha": "2025-10-03",
            "precio_unitario": 149.99,
        },
        {
            "id": 4,
            "producto_id": 6,
            "cantidad": 1,
            "fecha": "2025-10-05",
            "precio_unitario": 1199.99,
        },
        {
            "id": 5,
            "producto_id": 8,
            "cantidad": 4,
            "fecha": "2025-10-07",
            "precio_unitario": 249.99,
        },
        {
            "id": 6,
            "producto_id": 1,
            "cantidad": 1,
            "fecha": "2025-10-10",
            "precio_unitario": 899.99,
        },
        {
            "id": 7,
            "producto_id": 5,
            "cantidad": 1,
            "fecha": "2025-10-12",
            "precio_unitario": 1999.99,
        },
        {
            "id": 8,
            "producto_id": 2,
            "cantidad": 3,
            "fecha": "2025-10-15",
            "precio_unitario": 99.99,
        },
        {
            "id": 9,
            "producto_id": 4,
            "cantidad": 2,
            "fecha": "2025-10-18",
            "precio_unitario": 299.99,
        },
        {
            "id": 10,
            "producto_id": 9,
            "cantidad": 1,
            "fecha": "2025-10-20",
            "precio_unitario": 1499.99,
        },
    ]
