"""
Tests para el módulo de validaciones.

TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

import pytest
import requests

from src.validaciones import (
    extraer_json_seguro,
    validar_contenido_json,
    validar_status_code,
    validar_timeout,
    validar_url,
)

# Tests de validar_url()


def test_validar_url_https_valida(url_valida):
    """Debe aceptar URL HTTPS válida sin lanzar excepción."""
    validar_url(url_valida)  # No debe lanzar excepción


def test_validar_url_http_rechazada(url_http):
    """Debe rechazar URL HTTP (no segura)."""
    with pytest.raises(ValueError, match="debe usar HTTPS"):
        validar_url(url_http)


def test_validar_url_vacia():
    """Debe rechazar URL vacía."""
    with pytest.raises(ValueError, match="no puede estar vacía"):
        validar_url("")


def test_validar_url_sin_protocolo():
    """Debe rechazar URL sin protocolo."""
    with pytest.raises(ValueError, match="debe empezar con https://"):
        validar_url("api.ejemplo.com/users")


def test_validar_url_none():
    """Debe rechazar URL None."""
    with pytest.raises(TypeError, match="debe ser string"):
        validar_url(None)


# Tests de validar_timeout()


def test_validar_timeout_valido():
    """Debe aceptar timeout válido (entero positivo)."""
    validar_timeout(30)  # No debe lanzar excepción


def test_validar_timeout_negativo():
    """Debe rechazar timeout negativo."""
    with pytest.raises(ValueError, match="debe ser positivo"):
        validar_timeout(-1)


def test_validar_timeout_cero():
    """Debe rechazar timeout cero."""
    with pytest.raises(ValueError, match="debe ser positivo"):
        validar_timeout(0)


def test_validar_timeout_no_entero():
    """Debe rechazar timeout que no sea entero."""
    with pytest.raises(TypeError, match="debe ser entero"):
        validar_timeout(30.5)


def test_validar_timeout_none():
    """Debe rechazar timeout None."""
    with pytest.raises(TypeError, match="debe ser entero"):
        validar_timeout(None)


# Tests de validar_status_code()


def test_validar_status_code_200_exitoso():
    """Debe aceptar status code 200 (por defecto)."""
    response = requests.Response()
    response.status_code = 200
    validar_status_code(response)  # No debe lanzar excepción


def test_validar_status_code_201_exitoso():
    """Debe aceptar status code 201 si está en códigos válidos."""
    response = requests.Response()
    response.status_code = 201
    validar_status_code(response, codigos_validos=(200, 201))


def test_validar_status_code_404_rechazado():
    """Debe rechazar status code 404."""
    response = requests.Response()
    response.status_code = 404
    with pytest.raises(ValueError, match="Status code 404 no es válido"):
        validar_status_code(response)


def test_validar_status_code_500_rechazado():
    """Debe rechazar status code 500."""
    response = requests.Response()
    response.status_code = 500
    with pytest.raises(ValueError, match="Status code 500 no es válido"):
        validar_status_code(response)


def test_validar_status_code_personalizado():
    """Debe validar contra códigos personalizados."""
    response = requests.Response()
    response.status_code = 204
    validar_status_code(response, codigos_validos=(204,))


# Tests de validar_contenido_json()


def test_validar_contenido_json_valido():
    """Debe aceptar response con JSON válido."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b'{"test": "data"}'
    validar_contenido_json(response)


def test_validar_contenido_json_invalido():
    """Debe rechazar response con JSON inválido."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b'{"invalid json'
    with pytest.raises(ValueError, match="no es JSON válido"):
        validar_contenido_json(response)


def test_validar_contenido_json_sin_content_type():
    """Debe rechazar response sin Content-Type JSON."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "text/html"
    response._content = b'{"test": "data"}'
    with pytest.raises(ValueError, match="no es JSON"):
        validar_contenido_json(response)


# Tests de extraer_json_seguro()


def test_extraer_json_seguro_dict():
    """Debe extraer JSON que es un diccionario."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b'{"id": 1, "name": "Test"}'

    resultado = extraer_json_seguro(response)

    assert isinstance(resultado, dict)
    assert resultado["id"] == 1
    assert resultado["name"] == "Test"


def test_extraer_json_seguro_lista():
    """Debe extraer JSON que es una lista."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b'[{"id": 1}, {"id": 2}]'

    resultado = extraer_json_seguro(response)

    assert isinstance(resultado, list)
    assert len(resultado) == 2


def test_extraer_json_seguro_invalido():
    """Debe lanzar excepción si JSON es inválido."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b"invalid json"

    with pytest.raises(ValueError, match="no es JSON válido"):
        extraer_json_seguro(response)


def test_extraer_json_seguro_vacio():
    """Debe manejar respuesta vacía."""
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = b""

    with pytest.raises(ValueError, match="está vacío"):
        extraer_json_seguro(response)
