"""
Configuración global de pytest y fixtures compartidos
======================================================

Fixtures disponibles para todos los tests.
"""

import os
import sys
from pathlib import Path

import pytest

# Agregar src/ al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def datos_dir(tmp_path_factory):
    """
    Directorio temporal para datos de prueba (session-scoped).
    """
    return tmp_path_factory.mktemp("datos")


@pytest.fixture(scope="session")
def logs_dir(tmp_path_factory):
    """
    Directorio temporal para logs de prueba (session-scoped).
    """
    return tmp_path_factory.mktemp("logs")


@pytest.fixture
def html_ejemplo_simple():
    """
    HTML de ejemplo simple para tests básicos.
    """
    return """
    <html>
        <head><title>Test</title></head>
        <body>
            <h1>Título de Prueba</h1>
            <p class="descripcion">Esta es una descripción de prueba.</p>
            <a href="https://example.com">Enlace de prueba</a>
        </body>
    </html>
    """


@pytest.fixture
def html_tabla_ejemplo():
    """
    HTML con tabla de ejemplo para tests de scraping de tablas.
    """
    return """
    <table>
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Precio</th>
                <th>Stock</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Laptop</td>
                <td>999.99</td>
                <td>15</td>
            </tr>
            <tr>
                <td>Mouse</td>
                <td>25.50</td>
                <td>50</td>
            </tr>
            <tr>
                <td>Teclado</td>
                <td>75.00</td>
                <td>30</td>
            </tr>
        </tbody>
    </table>
    """


@pytest.fixture
def productos_ejemplo():
    """
    Lista de productos de ejemplo para tests de almacenamiento.
    """
    return [
        {
            "nombre": "Laptop HP",
            "precio": "999.99",
            "url": "https://tienda.com/laptop-hp",
            "descripcion": "Laptop potente para profesionales",
        },
        {
            "nombre": "Mouse Logitech",
            "precio": "25.50",
            "url": "https://tienda.com/mouse",
            "descripcion": "Mouse ergonómico inalámbrico",
        },
        {
            "nombre": "Teclado Mecánico",
            "precio": "150.00",
            "url": "https://tienda.com/teclado",
            "descripcion": "Teclado mecánico RGB",
        },
    ]
