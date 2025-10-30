"""
Fixtures compartidas para todos los tests del proyecto.

Este archivo contiene fixtures reutilizables que facilitan el testing
de todos los módulos del sistema de extracción.
"""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# ============================================================================
# Fixtures de Archivos Temporales
# ============================================================================


@pytest.fixture
def temp_dir():
    """Crea un directorio temporal para tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def csv_utf8_path(temp_dir):
    """Crea un CSV de prueba con encoding UTF-8"""
    csv_path = temp_dir / "test_utf8.csv"
    contenido = "nombre,edad,ciudad\nJosé,28,Madrid\nMaría,35,Barcelona\n"
    csv_path.write_text(contenido, encoding="utf-8")
    return csv_path


@pytest.fixture
def csv_latin1_path(temp_dir):
    """Crea un CSV de prueba con encoding Latin-1"""
    csv_path = temp_dir / "test_latin1.csv"
    contenido = "nombre,edad,ciudad\nJosé,28,Madrid\nMaría,35,Barcelona\n"
    csv_path.write_text(contenido, encoding="latin-1")
    return csv_path


@pytest.fixture
def json_simple_path(temp_dir):
    """Crea un JSON simple de prueba"""
    json_path = temp_dir / "test_simple.json"
    datos = [
        {"id": 1, "nombre": "Ana", "edad": 28},
        {"id": 2, "nombre": "Carlos", "edad": 35},
    ]
    json_path.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    return json_path


@pytest.fixture
def json_nested_path(temp_dir):
    """Crea un JSON anidado de prueba"""
    json_path = temp_dir / "test_nested.json"
    datos = [
        {
            "id": 1,
            "usuario": {
                "nombre": "Ana",
                "direccion": {"calle": "Gran Vía 1", "ciudad": "Madrid"},
            },
        },
        {
            "id": 2,
            "usuario": {
                "nombre": "Carlos",
                "direccion": {"calle": "Diagonal 123", "ciudad": "Barcelona"},
            },
        },
    ]
    json_path.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    return json_path


@pytest.fixture
def excel_path(temp_dir):
    """Crea un archivo Excel de prueba con múltiples hojas"""
    excel_path = temp_dir / "test.xlsx"

    df1 = pd.DataFrame({"producto": ["Laptop", "Mouse"], "ventas": [50, 200]})

    df2 = pd.DataFrame({"producto": ["Laptop", "Mouse"], "ventas": [60, 210]})

    with pd.ExcelWriter(excel_path) as writer:
        df1.to_excel(writer, sheet_name="Enero", index=False)
        df2.to_excel(writer, sheet_name="Febrero", index=False)

    return excel_path


# ============================================================================
# Fixtures de Datos de Prueba
# ============================================================================


@pytest.fixture
def sample_dataframe():
    """DataFrame de prueba"""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "nombre": ["Ana", "Carlos", "Laura"],
            "edad": [28, 35, 42],
            "ciudad": ["Madrid", "Barcelona", "Valencia"],
        }
    )


@pytest.fixture
def sample_dict():
    """Diccionario de prueba"""
    return {"id": 1, "nombre": "Ana", "edad": 28, "ciudad": "Madrid"}


@pytest.fixture
def sample_json_list():
    """Lista de diccionarios de prueba"""
    return [
        {"id": 1, "nombre": "Ana", "edad": 28},
        {"id": 2, "nombre": "Carlos", "edad": 35},
        {"id": 3, "nombre": "Laura", "edad": 42},
    ]


# ============================================================================
# Fixtures de HTML de Prueba
# ============================================================================


@pytest.fixture
def html_simple():
    """HTML simple para pruebas de scraping"""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <div class="producto" data-id="1">
            <h2 class="nombre">Laptop</h2>
            <span class="precio">1200</span>
        </div>
        <div class="producto" data-id="2">
            <h2 class="nombre">Mouse</h2>
            <span class="precio">25</span>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def html_tabla():
    """HTML con tabla para pruebas"""
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <table id="datos">
            <thead>
                <tr><th>ID</th><th>Nombre</th><th>Precio</th></tr>
            </thead>
            <tbody>
                <tr><td>1</td><td>Producto A</td><td>100</td></tr>
                <tr><td>2</td><td>Producto B</td><td>200</td></tr>
            </tbody>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def html_path(temp_dir, html_simple):
    """Archivo HTML de prueba"""
    html_path = temp_dir / "test.html"
    html_path.write_text(html_simple, encoding="utf-8")
    return html_path


# ============================================================================
# Fixtures de Configuración
# ============================================================================


@pytest.fixture
def mock_api_response():
    """Respuesta de API simulada"""
    return {
        "status": "success",
        "data": [{"id": 1, "nombre": "Item 1"}, {"id": 2, "nombre": "Item 2"}],
        "pagination": {"offset": 0, "limit": 10, "total": 2},
    }


@pytest.fixture
def columnas_esperadas():
    """Lista de columnas esperadas para validación"""
    return ["id", "nombre", "edad", "ciudad"]


# ============================================================================
# Fixtures de Limpieza
# ============================================================================


@pytest.fixture(autouse=True)
def reset_logging():
    """Limpia la configuración de logging entre tests"""
    import logging

    logging.getLogger().handlers = []
    yield
    logging.getLogger().handlers = []
