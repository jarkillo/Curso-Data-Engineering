"""
Tests para el módulo scraper_html.py
=====================================

15 tests que cubren todas las funciones de scraping HTML.
"""

import pytest
from src.scraper_html import (
    extraer_atributo,
    extraer_datos_estructurados,
    extraer_enlaces,
    extraer_tabla,
    extraer_titulos,
)

# ============================================================================
# Tests para extraer_titulos() - 3 tests
# ============================================================================


def test_extraer_titulos_basico():
    """Test 1: Extracción básica de títulos h1"""
    html = """
    <html>
        <body>
            <h1>Título 1</h1>
            <h1>Título 2</h1>
            <h1>Título 3</h1>
        </body>
    </html>
    """
    resultado = extraer_titulos(html, "h1")
    assert resultado == ["Título 1", "Título 2", "Título 3"]


def test_extraer_titulos_con_clases():
    """Test 2: Extracción con selector de clase"""
    html = """
    <div class="producto">Laptop</div>
    <div class="producto">Mouse</div>
    <div class="oferta">Descuento</div>
    """
    resultado = extraer_titulos(html, ".producto")
    assert resultado == ["Laptop", "Mouse"]
    assert len(resultado) == 2


def test_extraer_titulos_html_vacio():
    """Test 3: Error con HTML vacío"""
    with pytest.raises(ValueError, match="vacío"):
        extraer_titulos("", "h1")


# ============================================================================
# Tests para extraer_enlaces() - 3 tests
# ============================================================================


def test_extraer_enlaces_basico():
    """Test 4: Extracción básica de enlaces"""
    html = """
    <a href="https://ejemplo.com">Ejemplo</a>
    <a href="/contacto">Contacto</a>
    """
    resultado = extraer_enlaces(html)
    assert len(resultado) == 2
    assert resultado[0] == {"texto": "Ejemplo", "url": "https://ejemplo.com"}
    assert resultado[1] == {"texto": "Contacto", "url": "/contacto"}


def test_extraer_enlaces_sin_href():
    """Test 5: Enlaces sin href se omiten"""
    html = """
    <a href="https://valido.com">Válido</a>
    <a>Sin href</a>
    """
    resultado = extraer_enlaces(html)
    assert len(resultado) == 1
    assert resultado[0]["url"] == "https://valido.com"


def test_extraer_enlaces_con_selector():
    """Test 6: Extracción con selector específico"""
    html = """
    <a href="/home" class="nav">Home</a>
    <a href="/blog" class="nav">Blog</a>
    <a href="/ad">Anuncio</a>
    """
    resultado = extraer_enlaces(html, "a.nav")
    assert len(resultado) == 2
    assert resultado[0]["texto"] == "Home"


# ============================================================================
# Tests para extraer_tabla() - 3 tests
# ============================================================================


def test_extraer_tabla_basica():
    """Test 7: Conversión de tabla HTML simple"""
    html = """
    <table>
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Precio</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Laptop</td>
                <td>999</td>
            </tr>
            <tr>
                <td>Mouse</td>
                <td>25</td>
            </tr>
        </tbody>
    </table>
    """
    resultado = extraer_tabla(html)
    assert len(resultado) == 2
    assert resultado[0] == {"Nombre": "Laptop", "Precio": "999"}
    assert resultado[1] == {"Nombre": "Mouse", "Precio": "25"}


def test_extraer_tabla_sin_thead():
    """Test 8: Tabla donde primera fila son headers"""
    html = """
    <table>
        <tr>
            <td><strong>Producto</strong></td>
            <td><strong>Stock</strong></td>
        </tr>
        <tr>
            <td>Teclado</td>
            <td>50</td>
        </tr>
    </table>
    """
    resultado = extraer_tabla(html)
    assert len(resultado) == 1
    assert "Producto" in resultado[0]
    assert resultado[0]["Producto"] == "Teclado"


def test_extraer_tabla_no_encontrada():
    """Test 9: Error cuando no existe la tabla"""
    html = "<div>No hay tabla aquí</div>"
    with pytest.raises(ValueError, match="tabla"):
        extraer_tabla(html)


# ============================================================================
# Tests para extraer_atributo() - 3 tests
# ============================================================================


def test_extraer_atributo_imagenes():
    """Test 10: Extraer src de imágenes"""
    html = """
    <img src="logo.png" alt="Logo">
    <img src="banner.jpg" alt="Banner">
    """
    resultado = extraer_atributo(html, "img", "src")
    assert resultado == ["logo.png", "banner.jpg"]


def test_extraer_atributo_data():
    """Test 11: Extraer atributos data-*"""
    html = """
    <div class="producto" data-id="101" data-price="50">Laptop</div>
    <div class="producto" data-id="102" data-price="25">Mouse</div>
    """
    resultado = extraer_atributo(html, ".producto", "data-id")
    assert resultado == ["101", "102"]


def test_extraer_atributo_inexistente():
    """Test 12: Atributos inexistentes retornan lista vacía"""
    html = '<div class="test">Contenido</div>'
    resultado = extraer_atributo(html, ".test", "data-missing")
    assert resultado == []


# ============================================================================
# Tests para extraer_datos_estructurados() - 3 tests
# ============================================================================


def test_extraer_datos_estructurados_productos():
    """Test 13: Extracción de productos con múltiples campos"""
    html = """
    <div class="producto">
        <h2 class="titulo">Laptop</h2>
        <span class="precio">$999</span>
        <p class="descripcion">Potente y rápida</p>
    </div>
    <div class="producto">
        <h2 class="titulo">Mouse</h2>
        <span class="precio">$25</span>
        <p class="descripcion">Ergonómico</p>
    </div>
    """
    selectores = {
        "nombre": ".titulo",
        "precio": ".precio",
        "descripcion": ".descripcion",
    }
    resultado = extraer_datos_estructurados(html, selectores)

    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Laptop"
    assert resultado[0]["precio"] == "$999"
    assert resultado[1]["nombre"] == "Mouse"


def test_extraer_datos_estructurados_campos_faltantes():
    """Test 14: Manejo de campos opcionales faltantes"""
    html = """
    <div class="item">
        <h3 class="titulo">Producto A</h3>
    </div>
    <div class="item">
        <h3 class="titulo">Producto B</h3>
        <span class="descuento">20%</span>
    </div>
    """
    selectores = {"nombre": ".titulo", "descuento": ".descuento"}
    resultado = extraer_datos_estructurados(html, selectores)

    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Producto A"
    assert resultado[0]["descuento"] == ""  # Campo faltante como string vacío
    assert resultado[1]["descuento"] == "20%"


def test_extraer_datos_estructurados_selectores_invalidos():
    """Test 15: Error con selectores vacíos"""
    html = "<div>Contenido</div>"
    with pytest.raises(ValueError):
        extraer_datos_estructurados(html, {})
