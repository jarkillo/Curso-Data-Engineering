"""
Tests para el módulo de extracción web.

Tests exhaustivos para extractor_web.py con mocking de HTTP.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests
from bs4 import BeautifulSoup
from src.extractor_web import (
    extraer_elementos_por_selector,
    extraer_html,
    extraer_tabla_html,
    parsear_con_beautifulsoup,
    verificar_robots_txt,
)


class TestVerificarRobotsTxt:
    """Tests para verificar_robots_txt."""

    @patch("src.extractor_web.RobotFileParser")
    def test_scraping_permitido(self, mock_rp_class):
        """Cuando robots.txt permite el scraping, debe devolver True."""
        mock_rp = MagicMock()
        mock_rp.can_fetch.return_value = True
        mock_rp_class.return_value = mock_rp

        resultado = verificar_robots_txt("https://ejemplo.com/pagina")

        assert resultado is True
        mock_rp.set_url.assert_called_once_with("https://ejemplo.com/robots.txt")
        mock_rp.read.assert_called_once()
        mock_rp.can_fetch.assert_called_once()

    @patch("src.extractor_web.RobotFileParser")
    def test_scraping_no_permitido(self, mock_rp_class):
        """Cuando robots.txt bloquea el scraping, debe devolver False."""
        mock_rp = MagicMock()
        mock_rp.can_fetch.return_value = False
        mock_rp_class.return_value = mock_rp

        resultado = verificar_robots_txt("https://ejemplo.com/admin")

        assert resultado is False

    @patch("src.extractor_web.RobotFileParser")
    def test_error_al_leer_robots_asume_permitido(self, mock_rp_class):
        """Si hay error al leer robots.txt, debe asumir permitido."""
        mock_rp = MagicMock()
        mock_rp.read.side_effect = Exception("Network error")
        mock_rp_class.return_value = mock_rp

        resultado = verificar_robots_txt("https://ejemplo.com/pagina")

        # Debe devolver True por defecto cuando hay error
        assert resultado is True

    @patch("src.extractor_web.RobotFileParser")
    def test_user_agent_personalizado(self, mock_rp_class):
        """Debe poder verificar con user agent personalizado."""
        mock_rp = MagicMock()
        mock_rp.can_fetch.return_value = True
        mock_rp_class.return_value = mock_rp

        resultado = verificar_robots_txt(
            "https://ejemplo.com/pagina", user_agent="MiBot/1.0"
        )

        assert resultado is True
        mock_rp.can_fetch.assert_called_once_with(
            "MiBot/1.0", "https://ejemplo.com/pagina"
        )


class TestExtraerHtml:
    """Tests para extraer_html."""

    @patch("src.extractor_web.verificar_robots_txt")
    @patch("src.extractor_web.requests.get")
    def test_extraccion_exitosa(self, mock_get, mock_verificar):
        """Extracción exitosa debe devolver HTML."""
        mock_verificar.return_value = True
        mock_response = MagicMock()
        mock_response.text = "<html><body>Hola</body></html>"
        mock_get.return_value = mock_response

        resultado = extraer_html("https://ejemplo.com")

        assert resultado == "<html><body>Hola</body></html>"
        mock_verificar.assert_called_once()
        mock_get.assert_called_once()

    @patch("src.extractor_web.verificar_robots_txt")
    def test_robots_txt_bloquea_extraccion(self, mock_verificar):
        """Si robots.txt bloquea, debe lanzar ValueError."""
        mock_verificar.return_value = False

        with pytest.raises(ValueError, match="no permitido por robots.txt"):
            extraer_html("https://ejemplo.com/admin")

    @patch("src.extractor_web.verificar_robots_txt")
    @patch("src.extractor_web.requests.get")
    def test_omitir_verificacion_robots(self, mock_get, mock_verificar):
        """Puede omitir verificación de robots.txt."""
        mock_response = MagicMock()
        mock_response.text = "<html>Test</html>"
        mock_get.return_value = mock_response

        resultado = extraer_html("https://ejemplo.com", verificar_robots=False)

        assert resultado == "<html>Test</html>"
        mock_verificar.assert_not_called()

    @patch("src.extractor_web.verificar_robots_txt")
    @patch("src.extractor_web.requests.get")
    def test_error_http_lanza_excepcion(self, mock_get, mock_verificar):
        """Error HTTP debe propagar la excepción."""
        mock_verificar.return_value = True
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with pytest.raises(requests.HTTPError):
            extraer_html("https://ejemplo.com/noexiste")

    @patch("src.extractor_web.verificar_robots_txt")
    @patch("src.extractor_web.requests.get")
    def test_user_agent_personalizado_en_headers(self, mock_get, mock_verificar):
        """User agent personalizado debe enviarse en headers."""
        mock_verificar.return_value = True
        mock_response = MagicMock()
        mock_response.text = "<html>Test</html>"
        mock_get.return_value = mock_response

        extraer_html("https://ejemplo.com", user_agent="MiBot/2.0")

        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["headers"]["User-Agent"] == "MiBot/2.0"

    @patch("src.extractor_web.verificar_robots_txt")
    @patch("src.extractor_web.requests.get")
    def test_timeout_personalizado(self, mock_get, mock_verificar):
        """Timeout personalizado debe pasarse a requests."""
        mock_verificar.return_value = True
        mock_response = MagicMock()
        mock_response.text = "<html>Test</html>"
        mock_get.return_value = mock_response

        extraer_html("https://ejemplo.com", timeout=60)

        call_args = mock_get.call_args
        assert call_args[1]["timeout"] == 60


class TestParsearConBeautifulSoup:
    """Tests para parsear_con_beautifulsoup."""

    def test_parsea_html_simple(self):
        """Debe parsear HTML simple correctamente."""
        html = "<html><body><p>Hola</p></body></html>"

        soup = parsear_con_beautifulsoup(html)

        assert isinstance(soup, BeautifulSoup)
        assert soup.find("p").get_text() == "Hola"

    def test_usa_parser_por_defecto(self):
        """Debe usar html.parser por defecto."""
        html = "<div>Test</div>"

        soup = parsear_con_beautifulsoup(html)

        assert soup.find("div").get_text() == "Test"

    def test_html_vacio(self):
        """Debe manejar HTML vacío."""
        html = ""

        soup = parsear_con_beautifulsoup(html)

        assert isinstance(soup, BeautifulSoup)
        assert str(soup) == ""


class TestExtraerTablaHtml:
    """Tests para extraer_tabla_html."""

    def test_extrae_tabla_con_headers(self):
        """Debe extraer tabla con headers correctamente."""
        html = """
        <table>
            <tr><th>Nombre</th><th>Edad</th></tr>
            <tr><td>Ana</td><td>25</td></tr>
            <tr><td>Luis</td><td>30</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup)

        assert len(resultado) == 2
        assert resultado[0] == {"Nombre": "Ana", "Edad": "25"}
        assert resultado[1] == {"Nombre": "Luis", "Edad": "30"}

    def test_tabla_sin_headers_usa_nombres_genericos(self):
        """Tabla sin headers debe usar col_0, col_1, etc."""
        html = """
        <table>
            <tr><td>Ana</td><td>25</td></tr>
            <tr><td>Luis</td><td>30</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup)

        assert len(resultado) == 2
        assert resultado[0] == {"col_0": "Ana", "col_1": "25"}
        assert resultado[1] == {"col_0": "Luis", "col_1": "30"}

    def test_sin_tabla_devuelve_lista_vacia(self):
        """Si no hay tabla, debe devolver lista vacía."""
        html = "<div>No hay tabla aquí</div>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup)

        assert resultado == []

    def test_selector_css_para_tabla_especifica(self):
        """Debe poder seleccionar tabla específica con selector CSS."""
        html = """
        <table id="tabla1"><tr><td>Datos1</td></tr></table>
        <table id="tabla2"><tr><th>Nombre</th></tr><tr><td>Ana</td></tr></table>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup, selector="#tabla2")

        assert len(resultado) == 1
        assert resultado[0] == {"Nombre": "Ana"}

    def test_selector_no_encuentra_tabla(self):
        """Selector que no encuentra tabla debe devolver lista vacía."""
        html = "<table><tr><td>Datos</td></tr></table>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup, selector="#tabla-inexistente")

        assert resultado == []

    def test_tabla_vacia_devuelve_lista_vacia(self):
        """Tabla sin filas debe devolver lista vacía."""
        html = "<table></table>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup)

        assert resultado == []

    def test_tabla_con_filas_vacias_las_omite(self):
        """Filas sin celdas deben omitirse."""
        html = """
        <table>
            <tr><th>Nombre</th></tr>
            <tr></tr>
            <tr><td>Ana</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_tabla_html(soup)

        assert len(resultado) == 1
        assert resultado[0] == {"Nombre": "Ana"}


class TestExtraerElementosPorSelector:
    """Tests para extraer_elementos_por_selector."""

    def test_extrae_texto_por_defecto(self):
        """Debe extraer texto de elementos por defecto."""
        html = "<div><p>Texto 1</p><p>Texto 2</p></div>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "p")

        assert resultado == ["Texto 1", "Texto 2"]

    def test_extrae_atributo_especifico(self):
        """Debe poder extraer atributo específico."""
        html = """
        <div>
            <a href="/pagina1">Link 1</a>
            <a href="/pagina2">Link 2</a>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "a", extraer_atributo="href")

        assert resultado == ["/pagina1", "/pagina2"]

    def test_extrae_html_completo(self):
        """Cuando extraer_texto=False, debe devolver HTML completo."""
        html = "<div><span>Texto</span></div>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "span", extraer_texto=False)

        assert "<span>Texto</span>" in resultado[0]

    def test_selector_no_encuentra_elementos(self):
        """Selector que no encuentra nada debe devolver lista vacía."""
        html = "<div><p>Texto</p></div>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "span")

        assert resultado == []

    def test_atributo_no_existe_devuelve_string_vacio(self):
        """Si atributo no existe, debe devolver string vacío."""
        html = "<a>Link sin href</a>"
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "a", extraer_atributo="href")

        assert resultado == [""]

    def test_selectores_css_complejos(self):
        """Debe soportar selectores CSS complejos."""
        html = """
        <div class="contenido">
            <p class="destacado">Texto 1</p>
            <p>Texto 2</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "div.contenido p.destacado")

        assert resultado == ["Texto 1"]

    def test_multiples_atributos_extraidos(self):
        """Debe extraer atributo de múltiples elementos."""
        html = """
        <img src="img1.jpg" alt="Imagen 1">
        <img src="img2.jpg" alt="Imagen 2">
        <img src="img3.jpg" alt="Imagen 3">
        """
        soup = BeautifulSoup(html, "html.parser")

        resultado = extraer_elementos_por_selector(soup, "img", extraer_atributo="src")

        assert resultado == ["img1.jpg", "img2.jpg", "img3.jpg"]
