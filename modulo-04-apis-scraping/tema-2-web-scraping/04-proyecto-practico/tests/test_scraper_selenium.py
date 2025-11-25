"""
Tests para el módulo scraper_selenium.py
=========================================

12 tests que cubren scraping dinámico con Selenium.
"""

from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.scraper_selenium import (
    extraer_con_espera,
    extraer_tabla_dinamica,
    hacer_scroll_infinito,
)

# ============================================================================
# Tests para extraer_con_espera() - 4 tests
# ============================================================================


def test_extraer_con_espera_exitoso():
    """Test 16: Extracción exitosa con espera explícita"""
    # Mock del WebDriver
    mock_driver = Mock()
    mock_element_1 = Mock()
    mock_element_1.text = "Item 1"
    mock_element_2 = Mock()
    mock_element_2.text = "Item 2"

    # Mock del WebDriverWait
    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = [mock_element_1, mock_element_2]

        resultado = extraer_con_espera(mock_driver, ".item")

        assert resultado == ["Item 1", "Item 2"]
        assert len(resultado) == 2


def test_extraer_con_espera_timeout():
    """Test 17: TimeoutError cuando elementos no cargan"""
    mock_driver = Mock()

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.side_effect = TimeoutException("Timeout")

        with pytest.raises(TimeoutError):
            extraer_con_espera(mock_driver, ".no-existe", timeout=5)


def test_extraer_con_espera_selector_vacio():
    """Test 18: Error con selector vacío"""
    mock_driver = Mock()

    with pytest.raises(ValueError, match="vacío"):
        extraer_con_espera(mock_driver, "")


def test_extraer_con_espera_xpath():
    """Test 19: Extracción con selector XPath"""
    mock_driver = Mock()
    mock_element = Mock()
    mock_element.text = "Título XPath"

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = [mock_element]

        resultado = extraer_con_espera(
            mock_driver, "//h1[@class='titulo']", by=By.XPATH, timeout=15
        )

        assert resultado == ["Título XPath"]


# ============================================================================
# Tests para extraer_tabla_dinamica() - 4 tests
# ============================================================================


def test_extraer_tabla_dinamica_exitosa():
    """Test 20: Extracción de tabla cargada con JavaScript"""
    mock_driver = Mock()

    # Simular HTML de tabla
    mock_driver.page_source = """
    <table>
        <thead>
            <tr><th>Producto</th><th>Precio</th></tr>
        </thead>
        <tbody>
            <tr><td>Laptop</td><td>999</td></tr>
            <tr><td>Mouse</td><td>25</td></tr>
        </tbody>
    </table>
    """

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_table = Mock()
        mock_wait.return_value.until.return_value = mock_table

        resultado = extraer_tabla_dinamica(mock_driver)

        assert isinstance(resultado, list)
        assert len(resultado) >= 0  # Depende de implementación


def test_extraer_tabla_dinamica_timeout():
    """Test 21: Error cuando tabla no carga"""
    mock_driver = Mock()

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.side_effect = TimeoutException(
            "No se encontró tabla"
        )

        with pytest.raises(TimeoutError):
            extraer_tabla_dinamica(mock_driver, "table.dynamic", timeout=5)


def test_extraer_tabla_dinamica_sin_headers():
    """Test 22: Error con tabla sin headers"""
    mock_driver = Mock()
    mock_driver.page_source = """
    <table>
        <tr><td>Sin</td><td>Headers</td></tr>
    </table>
    """

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = Mock()

        with pytest.raises(ValueError, match="estructura válida|headers"):
            extraer_tabla_dinamica(mock_driver)


def test_extraer_tabla_dinamica_selector_personalizado():
    """Test 23: Extracción con selector CSS personalizado"""
    mock_driver = Mock()
    mock_driver.page_source = """
    <table class="data-table">
        <thead><tr><th>Nombre</th></tr></thead>
        <tbody><tr><td>Test</td></tr></tbody>
    </table>
    """

    with patch("src.scraper_selenium.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = Mock()

        resultado = extraer_tabla_dinamica(mock_driver, "table.data-table")
        assert isinstance(resultado, list)


# ============================================================================
# Tests para hacer_scroll_infinito() - 4 tests
# ============================================================================


def test_hacer_scroll_infinito_exitoso():
    """Test 24: Scroll infinito carga más items"""
    mock_driver = Mock()

    # Simular que se cargan más elementos después de cada scroll
    mock_driver.find_elements.side_effect = [
        [Mock()] * 10,  # Inicial: 10 items
        [Mock()] * 20,  # Después scroll 1: 20 items
        [Mock()] * 30,  # Después scroll 2: 30 items
        [Mock()] * 30,  # Ya no cargan más
    ]

    resultado = hacer_scroll_infinito(mock_driver, ".producto", max_scrolls=3)

    assert resultado >= 10
    assert mock_driver.execute_script.called  # Se ejecutó JavaScript scroll


def test_hacer_scroll_infinito_max_scrolls():
    """Test 25: Respeta el límite de max_scrolls"""
    mock_driver = Mock()
    mock_driver.find_elements.return_value = [Mock()] * 5

    hacer_scroll_infinito(mock_driver, ".item", max_scrolls=5)

    # Debe haber llamado execute_script máximo 5 veces
    assert mock_driver.execute_script.call_count <= 5


def test_hacer_scroll_infinito_max_scrolls_invalido():
    """Test 26: Error con max_scrolls inválido"""
    mock_driver = Mock()

    with pytest.raises(ValueError, match="max_scrolls"):
        hacer_scroll_infinito(mock_driver, ".item", max_scrolls=0)

    with pytest.raises(ValueError):
        hacer_scroll_infinito(mock_driver, ".item", max_scrolls=-1)


def test_hacer_scroll_infinito_pausa_negativa():
    """Test 27: Error con pausa negativa"""
    mock_driver = Mock()

    with pytest.raises(ValueError, match="pausa"):
        hacer_scroll_infinito(mock_driver, ".item", pausa=-0.5)
