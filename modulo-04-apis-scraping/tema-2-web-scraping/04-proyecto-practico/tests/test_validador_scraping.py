"""
Tests para el módulo validador_scraping.py
===========================================

16 tests que cubren validaciones de scraping ético.
"""

import time
from unittest.mock import Mock, patch

import pytest

from src.validador_scraping import (
    calcular_delay_rate_limit,
    validar_contenido_html,
    validar_robots_txt,
    validar_url,
)

# ============================================================================
# Tests para validar_robots_txt() - 4 tests
# ============================================================================


def test_validar_robots_txt_permitido():
    """Test 28: URL permitida según robots.txt"""
    url = "https://example.com/page"

    with patch("src.validador_scraping.RobotFileParser") as mock_parser:
        mock_instance = Mock()
        mock_instance.can_fetch.return_value = True
        mock_parser.return_value = mock_instance

        resultado = validar_robots_txt(url)
        assert resultado is True


def test_validar_robots_txt_bloqueado():
    """Test 29: URL bloqueada según robots.txt"""
    url = "https://example.com/admin"

    with patch("src.validador_scraping.RobotFileParser") as mock_parser:
        mock_instance = Mock()
        mock_instance.can_fetch.return_value = False
        mock_parser.return_value = mock_instance

        resultado = validar_robots_txt(url, user_agent="MyBot")
        assert resultado is False


def test_validar_robots_txt_url_invalida():
    """Test 30: Error con URL vacía"""
    with pytest.raises(ValueError, match="URL|vacía"):
        validar_robots_txt("")


def test_validar_robots_txt_error_de_red():
    """Test 31: Si no se puede leer robots.txt, permite por defecto"""
    url = "https://sitio-sin-robots.com/page"

    with patch("src.validador_scraping.RobotFileParser") as mock_parser:
        mock_instance = Mock()
        mock_instance.read.side_effect = Exception("Network error")
        mock_instance.can_fetch.return_value = True  # Default: permitir
        mock_parser.return_value = mock_instance

        resultado = validar_robots_txt(url)
        assert resultado is True  # Por defecto permite si hay error


# ============================================================================
# Tests para validar_url() - 4 tests
# ============================================================================


def test_validar_url_valida_http():
    """Test 32: URL HTTP válida"""
    assert validar_url("http://example.com") is True
    assert validar_url("http://example.com/path/to/page") is True


def test_validar_url_valida_https():
    """Test 33: URL HTTPS válida"""
    assert validar_url("https://www.example.com") is True
    assert validar_url("https://api.example.com/v1/users?id=123") is True


def test_validar_url_invalida():
    """Test 34: URLs inválidas"""
    assert validar_url("ftp://example.com") is False  # Protocolo no soportado
    assert validar_url("not-a-url") is False
    assert validar_url("example.com") is False  # Sin protocolo
    assert validar_url("://missing-scheme") is False


def test_validar_url_vacia_o_none():
    """Test 35: Error con URL vacía o None"""
    with pytest.raises(ValueError):
        validar_url("")

    with pytest.raises(ValueError):
        validar_url(None)


# ============================================================================
# Tests para calcular_delay_rate_limit() - 4 tests
# ============================================================================


def test_calcular_delay_rate_limit_debe_esperar():
    """Test 36: Calcula correctamente el delay necesario"""
    ahora = time.time()
    hace_medio_segundo = ahora - 0.5

    delay = calcular_delay_rate_limit(hace_medio_segundo, delay_minimo=1.0)

    assert delay > 0
    assert delay <= 0.6  # Debe esperar ~0.5 segundos más


def test_calcular_delay_rate_limit_no_debe_esperar():
    """Test 37: No requiere espera si ya pasó suficiente tiempo"""
    ahora = time.time()
    hace_dos_segundos = ahora - 2.0

    delay = calcular_delay_rate_limit(hace_dos_segundos, delay_minimo=1.0)

    assert delay == 0


def test_calcular_delay_rate_limit_delay_personalizado():
    """Test 38: Respeta delay_minimo personalizado"""
    ahora = time.time()
    hace_un_segundo = ahora - 1.0

    delay = calcular_delay_rate_limit(hace_un_segundo, delay_minimo=3.0)

    assert delay > 1.5  # Debe esperar ~2 segundos más


def test_calcular_delay_rate_limit_parametros_invalidos():
    """Test 39: Error con parámetros inválidos"""
    with pytest.raises(ValueError):
        calcular_delay_rate_limit(time.time(), delay_minimo=-1.0)

    with pytest.raises(ValueError):
        calcular_delay_rate_limit(-1.0, delay_minimo=1.0)  # Timestamp negativo


# ============================================================================
# Tests para validar_contenido_html() - 4 tests
# ============================================================================


def test_validar_contenido_html_valido():
    """Test 40: HTML válido y suficiente"""
    html = """
    <html>
        <body>
            <h1>Título de Prueba</h1>
            <p>Este es un contenido HTML válido con suficiente longitud para pasar la validación.</p>
        </body>
    </html>
    """

    resultado = validar_contenido_html(html, min_length=50)

    assert resultado["valido"] is True
    assert resultado["longitud"] > 50
    assert resultado["tiene_html"] is True
    assert (
        "válido" in resultado["mensaje"].lower()
        or "correcto" in resultado["mensaje"].lower()
    )


def test_validar_contenido_html_muy_corto():
    """Test 41: HTML muy corto (posible error)"""
    html = "<html><body></body></html>"

    resultado = validar_contenido_html(html, min_length=100)

    assert resultado["valido"] is False
    assert resultado["longitud"] < 100
    assert (
        "corto" in resultado["mensaje"].lower()
        or "insuficiente" in resultado["mensaje"].lower()
    )


def test_validar_contenido_html_sin_tags():
    """Test 42: Contenido sin tags HTML (texto plano)"""
    texto = "Este es solo texto plano sin ningún tag HTML."

    resultado = validar_contenido_html(texto, min_length=20)

    assert resultado["tiene_html"] is False
    assert (
        "html" in resultado["mensaje"].lower() or "tags" in resultado["mensaje"].lower()
    )


def test_validar_contenido_html_parametros_invalidos():
    """Test 43: Error con parámetros inválidos"""
    with pytest.raises(ValueError):
        validar_contenido_html(None)

    with pytest.raises(ValueError):
        validar_contenido_html("<html></html>", min_length=-1)
