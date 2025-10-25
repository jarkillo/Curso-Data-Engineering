"""
Tests para el módulo de reintentos con exponential backoff.

TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

from unittest.mock import patch

import pytest
import requests
import responses
from src.reintentos import calcular_delay_exponencial, reintentar_con_backoff

# Tests de calcular_delay_exponencial()


def test_calcular_delay_intento_1():
    """Debe calcular delay para intento 1: 2^1 = 2 segundos."""
    delay = calcular_delay_exponencial(intento=1)
    assert delay == 2


def test_calcular_delay_intento_2():
    """Debe calcular delay para intento 2: 2^2 = 4 segundos."""
    delay = calcular_delay_exponencial(intento=2)
    assert delay == 4


def test_calcular_delay_intento_3():
    """Debe calcular delay para intento 3: 2^3 = 8 segundos."""
    delay = calcular_delay_exponencial(intento=3)
    assert delay == 8


def test_calcular_delay_base_personalizada():
    """Debe usar base personalizada."""
    delay = calcular_delay_exponencial(intento=2, base=3)
    assert delay == 9  # 3^2


def test_calcular_delay_max_delay():
    """Debe respetar max_delay."""
    delay = calcular_delay_exponencial(intento=10, max_delay=30)
    assert delay <= 30


def test_calcular_delay_intento_cero():
    """Debe retornar 1 para intento 0."""
    delay = calcular_delay_exponencial(intento=0)
    assert delay == 1


def test_calcular_delay_intento_negativo():
    """Debe rechazar intento negativo."""
    with pytest.raises(ValueError, match="debe ser no negativo"):
        calcular_delay_exponencial(intento=-1)


def test_calcular_delay_base_invalida():
    """Debe rechazar base menor o igual a 1."""
    with pytest.raises(ValueError, match="debe ser mayor que 1"):
        calcular_delay_exponencial(intento=1, base=1)


def test_calcular_delay_max_delay_invalido():
    """Debe rechazar max_delay no positivo."""
    with pytest.raises(ValueError, match="debe ser positivo"):
        calcular_delay_exponencial(intento=1, max_delay=0)


# Tests de reintentar_con_backoff()


@responses.activate
def test_reintentar_exitoso_primer_intento(url_base):
    """Debe retornar response exitoso en el primer intento."""
    responses.add(responses.GET, url_base + "/users", json={"data": "ok"}, status=200)

    response = reintentar_con_backoff(url=url_base + "/users", max_intentos=3)

    assert response.status_code == 200
    assert len(responses.calls) == 1  # Solo 1 intento


@responses.activate
def test_reintentar_exitoso_segundo_intento(url_base):
    """Debe reintentar y tener éxito en el segundo intento."""
    # Primer intento: 500
    responses.add(
        responses.GET, url_base + "/users", json={"error": "Server Error"}, status=500
    )
    # Segundo intento: 200
    responses.add(responses.GET, url_base + "/users", json={"data": "ok"}, status=200)

    with patch("time.sleep"):  # Mockear sleep para acelerar tests
        response = reintentar_con_backoff(url=url_base + "/users", max_intentos=3)

    assert response.status_code == 200
    assert len(responses.calls) == 2  # 2 intentos


@responses.activate
def test_reintentar_todos_fallan(url_base):
    """Debe agotar reintentos y lanzar excepción."""
    # Todos los intentos fallan con 500
    for _ in range(3):
        responses.add(
            responses.GET,
            url_base + "/users",
            json={"error": "Server Error"},
            status=500,
        )

    with patch("time.sleep"):
        with pytest.raises(
            requests.exceptions.HTTPError, match="Todos los intentos fallaron"
        ):
            reintentar_con_backoff(url=url_base + "/users", max_intentos=3)

    assert len(responses.calls) == 3  # 3 intentos


@responses.activate
def test_reintentar_con_metodo_post(url_base):
    """Debe funcionar con método POST."""
    responses.add(responses.POST, url_base + "/users", json={"id": 1}, status=201)

    response = reintentar_con_backoff(
        url=url_base + "/users", metodo="POST", json={"name": "Test"}
    )

    assert response.status_code == 201


@responses.activate
def test_reintentar_con_headers(url_base):
    """Debe enviar headers en reintentos."""
    responses.add(responses.GET, url_base + "/users", json={"data": "ok"}, status=200)

    headers = {"Authorization": "Bearer token"}
    _ = reintentar_con_backoff(url=url_base + "/users", headers=headers)

    assert "Authorization" in responses.calls[0].request.headers


@responses.activate
def test_reintentar_429_rate_limit(url_base):
    """Debe reintentar con 429 (Rate Limit)."""
    # Primer intento: 429
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"error": "Rate limit exceeded"},
        status=429,
    )
    # Segundo intento: 200
    responses.add(responses.GET, url_base + "/users", json={"data": "ok"}, status=200)

    with patch("time.sleep"):
        response = reintentar_con_backoff(url=url_base + "/users")

    assert response.status_code == 200
    assert len(responses.calls) == 2


@responses.activate
def test_reintentar_503_service_unavailable(url_base):
    """Debe reintentar con 503 (Service Unavailable)."""
    # Primer intento: 503
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"error": "Service Unavailable"},
        status=503,
    )
    # Segundo intento: 200
    responses.add(responses.GET, url_base + "/users", json={"data": "ok"}, status=200)

    with patch("time.sleep"):
        response = reintentar_con_backoff(url=url_base + "/users")

    assert response.status_code == 200


@responses.activate
def test_reintentar_no_reintenta_404(url_base):
    """NO debe reintentar con 404 (error de cliente)."""
    responses.add(
        responses.GET, url_base + "/users/999", json={"error": "Not Found"}, status=404
    )

    with pytest.raises(requests.exceptions.HTTPError):
        reintentar_con_backoff(url=url_base + "/users/999")

    # Solo debe haber intentado 1 vez (404 no se reintenta)
    assert len(responses.calls) == 1


@responses.activate
def test_reintentar_no_reintenta_400(url_base):
    """NO debe reintentar con 400 (error de cliente)."""
    responses.add(
        responses.GET, url_base + "/users", json={"error": "Bad Request"}, status=400
    )

    with pytest.raises(requests.exceptions.HTTPError):
        reintentar_con_backoff(url=url_base + "/users")

    assert len(responses.calls) == 1


def test_reintentar_max_intentos_invalido(url_base):
    """Debe rechazar max_intentos inválido."""
    with pytest.raises(ValueError, match="debe ser al menos 1"):
        reintentar_con_backoff(url=url_base + "/users", max_intentos=0)


def test_reintentar_metodo_invalido(url_base):
    """Debe rechazar método HTTP inválido."""
    with pytest.raises(ValueError, match="no es un método HTTP válido"):
        reintentar_con_backoff(url=url_base + "/users", metodo="INVALID")


@responses.activate
@patch("time.sleep")
def test_reintentar_usa_exponential_backoff(mock_sleep, url_base):
    """Debe usar exponential backoff entre reintentos."""
    # 3 intentos fallidos
    for _ in range(3):
        responses.add(
            responses.GET,
            url_base + "/users",
            json={"error": "Server Error"},
            status=500,
        )

    with pytest.raises(requests.exceptions.HTTPError):
        reintentar_con_backoff(url=url_base + "/users", max_intentos=3)

    # Verificar que sleep fue llamado con delays crecientes
    assert mock_sleep.call_count == 2  # 2 sleeps (entre 3 intentos)

    # Primer sleep: ~2 segundos
    primer_sleep = mock_sleep.call_args_list[0][0][0]
    assert 1 <= primer_sleep <= 3

    # Segundo sleep: ~4 segundos
    segundo_sleep = mock_sleep.call_args_list[1][0][0]
    assert 3 <= segundo_sleep <= 5
