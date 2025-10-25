"""
Tests para el módulo de cliente HTTP.

TDD: Tests escritos PRIMERO, implementación DESPUÉS.
Usa 'responses' para mockear HTTP requests.
"""

import pytest
import requests
import responses
from src.cliente_http import hacer_delete, hacer_get, hacer_post, hacer_put

# Tests de hacer_get()


@responses.activate
def test_hacer_get_exitoso(url_base, mock_response_exitoso):
    """Debe hacer GET request exitoso."""
    responses.add(
        responses.GET, url_base + "/users", json=mock_response_exitoso, status=200
    )

    response = hacer_get(url_base + "/users")

    assert response.status_code == 200
    assert response.json() == mock_response_exitoso


@responses.activate
def test_hacer_get_con_headers(url_base):
    """Debe enviar headers correctamente."""
    responses.add(responses.GET, url_base + "/users", json={"status": "ok"}, status=200)

    headers = {"X-Custom-Header": "test-value"}
    response = hacer_get(url_base + "/users", headers=headers)

    # Verificar que el header fue enviado
    assert len(responses.calls) == 1
    assert "X-Custom-Header" in responses.calls[0].request.headers
    assert responses.calls[0].request.headers["X-Custom-Header"] == "test-value"


@responses.activate
def test_hacer_get_con_params(url_base):
    """Debe enviar query parameters correctamente."""
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    params = {"page": 1, "limit": 10}
    response = hacer_get(url_base + "/users", params=params)

    # Verificar que params fueron enviados
    assert "page=1" in responses.calls[0].request.url
    assert "limit=10" in responses.calls[0].request.url


@responses.activate
def test_hacer_get_timeout(url_base):
    """Debe usar timeout especificado."""
    responses.add(
        responses.GET,
        url_base + "/users",
        body=requests.exceptions.Timeout("Connection timeout"),
    )

    with pytest.raises(requests.exceptions.Timeout):
        hacer_get(url_base + "/users", timeout=5)


@responses.activate
def test_hacer_get_404(url_base):
    """Debe retornar response con status 404."""
    responses.add(
        responses.GET, url_base + "/users/999", json={"error": "Not Found"}, status=404
    )

    response = hacer_get(url_base + "/users/999")

    assert response.status_code == 404


def test_hacer_get_url_invalida():
    """Debe rechazar URL inválida (HTTP en lugar de HTTPS)."""
    with pytest.raises(ValueError, match="debe usar HTTPS"):
        hacer_get("http://api.ejemplo.com/users")


# Tests de hacer_post()


@responses.activate
def test_hacer_post_exitoso(url_base):
    """Debe hacer POST request exitoso."""
    responses.add(
        responses.POST,
        url_base + "/users",
        json={"id": 123, "created": True},
        status=201,
    )

    data = {"name": "Test User", "email": "test@example.com"}
    response = hacer_post(url_base + "/users", json=data)

    assert response.status_code == 201
    assert response.json()["created"] is True


@responses.activate
def test_hacer_post_con_json(url_base):
    """Debe enviar datos como JSON correctamente."""
    responses.add(responses.POST, url_base + "/users", json={"id": 1}, status=201)

    data = {"name": "Test"}
    response = hacer_post(url_base + "/users", json=data)

    # Verificar que se envió como JSON
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


@responses.activate
def test_hacer_post_con_data(url_base):
    """Debe enviar datos como form data."""
    responses.add(responses.POST, url_base + "/users", json={"id": 1}, status=201)

    data = {"name": "Test"}
    response = hacer_post(url_base + "/users", data=data)

    assert response.status_code == 201


@responses.activate
def test_hacer_post_con_headers(url_base):
    """Debe enviar headers correctamente."""
    responses.add(responses.POST, url_base + "/users", json={"id": 1}, status=201)

    headers = {"Authorization": "Bearer token123"}
    response = hacer_post(url_base + "/users", json={"test": "data"}, headers=headers)

    assert "Authorization" in responses.calls[0].request.headers


# Tests de hacer_put()


@responses.activate
def test_hacer_put_exitoso(url_base):
    """Debe hacer PUT request exitoso."""
    responses.add(
        responses.PUT,
        url_base + "/users/1",
        json={"id": 1, "updated": True},
        status=200,
    )

    data = {"name": "Updated Name"}
    response = hacer_put(url_base + "/users/1", json=data)

    assert response.status_code == 200
    assert response.json()["updated"] is True


@responses.activate
def test_hacer_put_con_json(url_base):
    """Debe enviar datos como JSON correctamente."""
    responses.add(responses.PUT, url_base + "/users/1", json={"id": 1}, status=200)

    data = {"name": "Updated"}
    response = hacer_put(url_base + "/users/1", json=data)

    # Verificar que se envió como JSON
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


# Tests de hacer_delete()


@responses.activate
def test_hacer_delete_exitoso(url_base):
    """Debe hacer DELETE request exitoso."""
    responses.add(responses.DELETE, url_base + "/users/1", status=204)

    response = hacer_delete(url_base + "/users/1")

    assert response.status_code == 204


@responses.activate
def test_hacer_delete_con_headers(url_base):
    """Debe enviar headers correctamente."""
    responses.add(responses.DELETE, url_base + "/users/1", status=204)

    headers = {"Authorization": "Bearer token123"}
    response = hacer_delete(url_base + "/users/1", headers=headers)

    assert "Authorization" in responses.calls[0].request.headers


@responses.activate
def test_hacer_delete_404(url_base):
    """Debe retornar response con status 404."""
    responses.add(
        responses.DELETE,
        url_base + "/users/999",
        json={"error": "Not Found"},
        status=404,
    )

    response = hacer_delete(url_base + "/users/999")

    assert response.status_code == 404


# Tests de manejo de errores comunes


@responses.activate
def test_connection_error(url_base):
    """Debe propagar ConnectionError."""
    responses.add(
        responses.GET,
        url_base + "/users",
        body=requests.exceptions.ConnectionError("Connection failed"),
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        hacer_get(url_base + "/users")


def test_timeout_invalido(url_base):
    """Debe rechazar timeout inválido."""
    with pytest.raises(ValueError, match="debe ser positivo"):
        hacer_get(url_base + "/users", timeout=-1)
