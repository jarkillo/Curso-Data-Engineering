"""
Fixtures compartidas para todos los tests.
"""

import pytest
import requests


@pytest.fixture
def url_base():
    """URL base para tests."""
    return "https://api.ejemplo.com"


@pytest.fixture
def url_valida():
    """URL válida HTTPS."""
    return "https://jsonplaceholder.typicode.com/users"


@pytest.fixture
def url_http():
    """URL HTTP (no segura)."""
    return "http://api.ejemplo.com/users"


@pytest.fixture
def api_key():
    """API key de prueba."""
    return "test-api-key-12345"


@pytest.fixture
def bearer_token():
    """Bearer token de prueba."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"


@pytest.fixture
def credenciales_basic():
    """Credenciales para Basic Auth."""
    return {"username": "testuser", "password": "testpass123"}


@pytest.fixture
def mock_response_exitoso():
    """Response exitoso simulado."""
    return {"id": 1, "nombre": "Test", "status": "success"}


@pytest.fixture
def mock_usuarios():
    """Lista de usuarios para tests."""
    return [
        {"id": 1, "name": "Usuario 1", "email": "user1@test.com"},
        {"id": 2, "name": "Usuario 2", "email": "user2@test.com"},
        {"id": 3, "name": "Usuario 3", "email": "user3@test.com"},
    ]


@pytest.fixture
def mock_response_paginado():
    """Datos paginados simulados."""
    return {
        "data": [{"id": 1}, {"id": 2}, {"id": 3}],
        "pagination": {"next_cursor": "abc123", "has_more": True},
    }


@pytest.fixture
def response_mock_200(mock_response_exitoso):
    """Response mock con status 200."""
    response = requests.Response()
    response.status_code = 200
    response._content = str(mock_response_exitoso).encode()
    return response


@pytest.fixture
def response_mock_404():
    """Response mock con status 404."""
    response = requests.Response()
    response.status_code = 404
    response._content = b'{"error": "Not Found"}'
    return response


@pytest.fixture
def response_mock_500():
    """Response mock con status 500."""
    response = requests.Response()
    response.status_code = 500
    response._content = b'{"error": "Internal Server Error"}'
    return response
