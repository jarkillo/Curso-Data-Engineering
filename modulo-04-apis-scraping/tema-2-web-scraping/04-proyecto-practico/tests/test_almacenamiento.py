"""
Tests para el módulo almacenamiento.py
=======================================

12 tests que cubren almacenamiento en SQLite.
"""

import os
import sqlite3
from pathlib import Path

import pytest
from src.almacenamiento import (
    crear_tabla_productos,
    guardar_productos,
    obtener_productos,
)


# Fixture para limpiar la BD de prueba
@pytest.fixture
def db_test_path(tmp_path):
    """Crea una ruta temporal para la BD de pruebas"""
    db_path = tmp_path / "test_productos.db"
    yield str(db_path)
    # Cleanup: eliminar archivo después del test
    if db_path.exists():
        db_path.unlink()


# ============================================================================
# Tests para crear_tabla_productos() - 4 tests
# ============================================================================


def test_crear_tabla_productos_exitoso(db_test_path):
    """Test 44: Creación exitosa de tabla"""
    crear_tabla_productos(db_test_path)

    # Verificar que la tabla existe
    conn = sqlite3.connect(db_test_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='productos'"
    )
    tabla = cursor.fetchone()
    conn.close()

    assert tabla is not None
    assert tabla[0] == "productos"


def test_crear_tabla_productos_idempotente(db_test_path):
    """Test 45: Llamar dos veces no genera error (IF NOT EXISTS)"""
    crear_tabla_productos(db_test_path)
    crear_tabla_productos(db_test_path)  # No debe fallar

    # Verificar que sigue existiendo
    conn = sqlite3.connect(db_test_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='productos'"
    )
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1


def test_crear_tabla_productos_schema_correcto(db_test_path):
    """Test 46: Verificar que el schema tiene las columnas correctas"""
    crear_tabla_productos(db_test_path)

    conn = sqlite3.connect(db_test_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(productos)")
    columnas = cursor.fetchall()
    conn.close()

    nombres_columnas = [col[1] for col in columnas]

    assert "id" in nombres_columnas
    assert "nombre" in nombres_columnas
    assert "precio" in nombres_columnas
    assert "url" in nombres_columnas
    assert "descripcion" in nombres_columnas
    assert "fecha_scraping" in nombres_columnas


def test_crear_tabla_productos_path_vacio():
    """Test 47: Error con path vacío"""
    with pytest.raises(ValueError):
        crear_tabla_productos("")


# ============================================================================
# Tests para guardar_productos() - 4 tests
# ============================================================================


def test_guardar_productos_exitoso(db_test_path):
    """Test 48: Guardar productos correctamente"""
    crear_tabla_productos(db_test_path)

    productos = [
        {
            "nombre": "Laptop",
            "precio": "999.99",
            "url": "https://shop.com/laptop",
            "descripcion": "Potente",
        },
        {
            "nombre": "Mouse",
            "precio": "25.50",
            "url": "https://shop.com/mouse",
            "descripcion": "Ergonómico",
        },
    ]

    insertados = guardar_productos(productos, db_test_path)

    assert insertados == 2


def test_guardar_productos_verifica_insercion(db_test_path):
    """Test 49: Verificar que los productos se guardaron correctamente"""
    crear_tabla_productos(db_test_path)

    productos = [
        {
            "nombre": "Teclado",
            "precio": "75.00",
            "url": "https://shop.com/kb",
            "descripcion": "Mecánico",
        }
    ]

    guardar_productos(productos, db_test_path)

    # Verificar en BD
    conn = sqlite3.connect(db_test_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE nombre='Teclado'")
    resultado = cursor.fetchone()
    conn.close()

    assert resultado is not None
    assert resultado[0] == "Teclado"
    assert float(resultado[1]) == 75.00


def test_guardar_productos_lista_vacia(db_test_path):
    """Test 50: Error con lista vacía"""
    crear_tabla_productos(db_test_path)

    with pytest.raises(ValueError, match="vacía"):
        guardar_productos([], db_test_path)


def test_guardar_productos_mal_formados(db_test_path):
    """Test 51: Error con productos mal formados (faltan campos)"""
    crear_tabla_productos(db_test_path)

    productos_invalidos = [{"nombre": "Sin precio"}]  # Falta precio, url, descripcion

    with pytest.raises(ValueError, match="mal formado|campos"):
        guardar_productos(productos_invalidos, db_test_path)


# ============================================================================
# Tests para obtener_productos() - 4 tests
# ============================================================================


def test_obtener_productos_todos(db_test_path):
    """Test 52: Obtener todos los productos"""
    crear_tabla_productos(db_test_path)

    productos = [
        {
            "nombre": "Producto A",
            "precio": "10",
            "url": "url-a",
            "descripcion": "desc-a",
        },
        {
            "nombre": "Producto B",
            "precio": "20",
            "url": "url-b",
            "descripcion": "desc-b",
        },
        {
            "nombre": "Producto C",
            "precio": "30",
            "url": "url-c",
            "descripcion": "desc-c",
        },
    ]
    guardar_productos(productos, db_test_path)

    resultado = obtener_productos(db_test_path)

    assert len(resultado) == 3
    assert resultado[0]["nombre"] == "Producto A"


def test_obtener_productos_con_limite(db_test_path):
    """Test 53: Obtener solo N productos (limite)"""
    crear_tabla_productos(db_test_path)

    productos = [
        {
            "nombre": f"Producto {i}",
            "precio": str(i * 10),
            "url": f"url-{i}",
            "descripcion": f"desc-{i}",
        }
        for i in range(10)
    ]
    guardar_productos(productos, db_test_path)

    resultado = obtener_productos(db_test_path, limite=5)

    assert len(resultado) == 5


def test_obtener_productos_bd_vacia(db_test_path):
    """Test 54: Obtener productos de BD vacía retorna lista vacía"""
    crear_tabla_productos(db_test_path)

    resultado = obtener_productos(db_test_path)

    assert resultado == []
    assert isinstance(resultado, list)


def test_obtener_productos_limite_negativo(db_test_path):
    """Test 55: Error con limite negativo"""
    crear_tabla_productos(db_test_path)

    with pytest.raises(ValueError, match="negativo"):
        obtener_productos(db_test_path, limite=-1)
