"""
Tests para el módulo utilidades_scraping.py
============================================

16 tests que cubren utilidades auxiliares del scraper.
"""

import logging

import pytest
from src.utilidades_scraping import (
    configurar_logging,
    crear_headers_aleatorios,
    extraer_dominio,
    limpiar_texto,
)

# ============================================================================
# Tests para configurar_logging() - 4 tests
# ============================================================================


def test_configurar_logging_nivel_info():
    """Test 56: Configuración básica con nivel INFO"""
    logger = configurar_logging(nivel="INFO")

    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO


def test_configurar_logging_nivel_debug():
    """Test 57: Configuración con nivel DEBUG"""
    logger = configurar_logging(nivel="DEBUG")

    assert logger.level == logging.DEBUG


def test_configurar_logging_con_archivo(tmp_path):
    """Test 58: Logging con archivo de salida"""
    archivo_log = tmp_path / "scraper.log"
    logger = configurar_logging(nivel="INFO", archivo=str(archivo_log))

    logger.info("Test message")

    assert archivo_log.exists()
    contenido = archivo_log.read_text()
    assert "Test message" in contenido


def test_configurar_logging_nivel_invalido():
    """Test 59: Error con nivel de logging inválido"""
    with pytest.raises(ValueError, match="nivel|inválido"):
        configurar_logging(nivel="INVALID_LEVEL")


# ============================================================================
# Tests para crear_headers_aleatorios() - 4 tests
# ============================================================================


def test_crear_headers_aleatorios_estructura():
    """Test 60: Headers tienen estructura correcta"""
    headers = crear_headers_aleatorios()

    assert isinstance(headers, dict)
    assert "User-Agent" in headers
    assert "Accept" in headers
    assert "Accept-Language" in headers


def test_crear_headers_aleatorios_user_agent_valido():
    """Test 61: User-Agent es realista"""
    headers = crear_headers_aleatorios()
    user_agent = headers["User-Agent"]

    # Debe contener indicadores de navegador real
    navegadores = ["Mozilla", "Chrome", "Safari", "Firefox", "Edge"]
    assert any(nav in user_agent for nav in navegadores)
    assert len(user_agent) > 20  # User-Agent realista es largo


def test_crear_headers_aleatorios_variacion():
    """Test 62: Headers varían entre llamadas (aleatorización)"""
    # Si llamamos varias veces, eventualmente debemos ver variación
    # (esto podría fallar ocasionalmente por aleatoriedad, pero es improbable)
    llamadas = [crear_headers_aleatorios()["User-Agent"] for _ in range(10)]
    assert len(set(llamadas)) > 1  # Al menos 2 User-Agents distintos en 10 llamadas


def test_crear_headers_aleatorios_accept_header():
    """Test 63: Header Accept tiene formato correcto"""
    headers = crear_headers_aleatorios()

    assert "text/html" in headers["Accept"]
    assert "application/xhtml+xml" in headers["Accept"]


# ============================================================================
# Tests para limpiar_texto() - 4 tests
# ============================================================================


def test_limpiar_texto_espacios_multiples():
    """Test 64: Elimina espacios múltiples"""
    texto = "Hola     mundo    con    espacios"
    resultado = limpiar_texto(texto)

    assert resultado == "Hola mundo con espacios"
    assert "  " not in resultado  # No debe haber espacios dobles


def test_limpiar_texto_saltos_de_linea():
    """Test 65: Elimina saltos de línea y tabs"""
    texto = "Primera línea\n\nSegunda línea\t\tcon tabs"
    resultado = limpiar_texto(texto)

    assert "\n\n" not in resultado
    assert "\t\t" not in resultado
    assert resultado == "Primera línea Segunda línea con tabs"


def test_limpiar_texto_espacios_laterales():
    """Test 66: Elimina espacios al inicio y final"""
    texto = "   Texto con espacios laterales   "
    resultado = limpiar_texto(texto)

    assert resultado == "Texto con espacios laterales"
    assert not resultado.startswith(" ")
    assert not resultado.endswith(" ")


def test_limpiar_texto_none():
    """Test 67: Error con None"""
    with pytest.raises(ValueError, match="None"):
        limpiar_texto(None)


# ============================================================================
# Tests para extraer_dominio() - 4 tests
# ============================================================================


def test_extraer_dominio_url_simple():
    """Test 68: Extracción de dominio simple"""
    assert extraer_dominio("https://example.com") == "example.com"
    assert extraer_dominio("http://example.com") == "example.com"


def test_extraer_dominio_url_compleja():
    """Test 69: Extracción con path, query params y puerto"""
    assert extraer_dominio("https://www.example.com/path/to/page") == "www.example.com"
    assert (
        extraer_dominio("https://api.example.com/v1/users?id=123") == "api.example.com"
    )
    assert extraer_dominio("http://localhost:8000/test") == "localhost"


def test_extraer_dominio_subdominios():
    """Test 70: Manejo de subdominios"""
    assert extraer_dominio("https://blog.empresa.com") == "blog.empresa.com"
    assert (
        extraer_dominio("https://api.v2.empresa.com/endpoint") == "api.v2.empresa.com"
    )


def test_extraer_dominio_url_invalida():
    """Test 71: Error con URL inválida o vacía"""
    with pytest.raises(ValueError):
        extraer_dominio("")

    with pytest.raises(ValueError):
        extraer_dominio("not-a-valid-url")

    with pytest.raises(ValueError):
        extraer_dominio("ftp://unsupported-protocol.com")
