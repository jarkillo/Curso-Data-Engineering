"""
Tests para el módulo de autenticación.

TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

import base64

import pytest

from src.autenticacion import (
    combinar_headers,
    crear_headers_api_key,
    crear_headers_basic_auth,
    crear_headers_bearer,
)

# Tests de crear_headers_api_key()


def test_crear_headers_api_key_default(api_key):
    """Debe crear headers con API key en X-API-Key (default)."""
    headers = crear_headers_api_key(api_key)

    assert "X-API-Key" in headers
    assert headers["X-API-Key"] == api_key


def test_crear_headers_api_key_personalizado(api_key):
    """Debe crear headers con nombre de header personalizado."""
    headers = crear_headers_api_key(api_key, header_name="Authorization")

    assert "Authorization" in headers
    assert headers["Authorization"] == api_key


def test_crear_headers_api_key_vacia():
    """Debe rechazar API key vacía."""
    with pytest.raises(ValueError, match="no puede estar vacía"):
        crear_headers_api_key("")


def test_crear_headers_api_key_none():
    """Debe rechazar API key None."""
    with pytest.raises(TypeError, match="debe ser string"):
        crear_headers_api_key(None)


def test_crear_headers_api_key_header_name_vacio(api_key):
    """Debe rechazar nombre de header vacío."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        crear_headers_api_key(api_key, header_name="")


# Tests de crear_headers_bearer()


def test_crear_headers_bearer_token(bearer_token):
    """Debe crear headers con Bearer token."""
    headers = crear_headers_bearer(bearer_token)

    assert "Authorization" in headers
    assert headers["Authorization"] == f"Bearer {bearer_token}"


def test_crear_headers_bearer_token_vacio():
    """Debe rechazar token vacío."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        crear_headers_bearer("")


def test_crear_headers_bearer_token_none():
    """Debe rechazar token None."""
    with pytest.raises(TypeError, match="debe ser string"):
        crear_headers_bearer(None)


# Tests de crear_headers_basic_auth()


def test_crear_headers_basic_auth_valido(credenciales_basic):
    """Debe crear headers con Basic Auth correctamente."""
    headers = crear_headers_basic_auth(
        credenciales_basic["username"], credenciales_basic["password"]
    )

    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ")

    # Decodificar y verificar
    encoded = headers["Authorization"].split(" ")[1]
    decoded = base64.b64decode(encoded).decode()
    expected = f"{credenciales_basic['username']}:{credenciales_basic['password']}"
    assert decoded == expected


def test_crear_headers_basic_auth_username_vacio():
    """Debe rechazar username vacío."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        crear_headers_basic_auth("", "password123")


def test_crear_headers_basic_auth_password_vacio():
    """Debe rechazar password vacío."""
    with pytest.raises(ValueError, match="no puede estar vacía"):
        crear_headers_basic_auth("user", "")


def test_crear_headers_basic_auth_username_none():
    """Debe rechazar username None."""
    with pytest.raises(TypeError, match="debe ser string"):
        crear_headers_basic_auth(None, "password")


def test_crear_headers_basic_auth_password_none():
    """Debe rechazar password None."""
    with pytest.raises(TypeError, match="debe ser string"):
        crear_headers_basic_auth("user", None)


# Tests de combinar_headers()


def test_combinar_headers_dos_dicts():
    """Debe combinar dos diccionarios de headers."""
    headers_base = {"Content-Type": "application/json"}
    headers_extra = {"X-Custom": "value"}

    resultado = combinar_headers(headers_base, headers_extra)

    assert "Content-Type" in resultado
    assert "X-Custom" in resultado
    assert resultado["Content-Type"] == "application/json"
    assert resultado["X-Custom"] == "value"


def test_combinar_headers_sobrescribir():
    """Debe sobrescribir headers duplicados con el valor de headers_extra."""
    headers_base = {"Authorization": "old"}
    headers_extra = {"Authorization": "new"}

    resultado = combinar_headers(headers_base, headers_extra)

    assert resultado["Authorization"] == "new"


def test_combinar_headers_base_vacio():
    """Debe funcionar con headers_base vacío."""
    headers_extra = {"X-Custom": "value"}

    resultado = combinar_headers({}, headers_extra)

    assert resultado == headers_extra


def test_combinar_headers_extra_vacio():
    """Debe funcionar con headers_extra vacío."""
    headers_base = {"Content-Type": "application/json"}

    resultado = combinar_headers(headers_base, {})

    assert resultado == headers_base


def test_combinar_headers_ambos_vacios():
    """Debe funcionar con ambos vacíos."""
    resultado = combinar_headers({}, {})

    assert resultado == {}


def test_combinar_headers_no_modifica_originales():
    """No debe modificar los diccionarios originales."""
    headers_base = {"Content-Type": "application/json"}
    headers_extra = {"X-Custom": "value"}

    combinar_headers(headers_base, headers_extra)

    # Originales no deben cambiar
    assert len(headers_base) == 1
    assert len(headers_extra) == 1
