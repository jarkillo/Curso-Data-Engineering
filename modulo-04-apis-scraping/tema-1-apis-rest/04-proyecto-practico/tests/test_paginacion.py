"""
Tests para el módulo de paginación.

TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

import pytest
import responses

from src.paginacion import paginar_cursor, paginar_offset_limit

# Tests de paginar_offset_limit()


@responses.activate
def test_paginar_offset_limit_una_pagina(url_base):
    """Debe extraer todos los datos de una sola página."""
    # Primera página con datos
    responses.add(
        responses.GET,
        url_base + "/users",
        json=[{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}],
        status=200,
    )
    # Segunda página vacía (fin de paginación)
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    resultados = paginar_offset_limit(url=url_base + "/users", limite_por_pagina=10)

    assert len(resultados) == 2
    assert resultados[0]["id"] == 1
    assert len(responses.calls) == 2  # Debe hacer 2 requests


@responses.activate
def test_paginar_offset_limit_multiples_paginas(url_base):
    """Debe iterar y combinar datos de múltiples páginas."""
    # Página 1 (offset=0)
    responses.add(
        responses.GET,
        url_base + "/users",
        json=[{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}],
        status=200,
    )
    # Página 2 (offset=2)
    responses.add(
        responses.GET,
        url_base + "/users",
        json=[{"id": 3, "name": "User 3"}, {"id": 4, "name": "User 4"}],
        status=200,
    )
    # Página 3 (offset=4) - vacía, fin de paginación
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    resultados = paginar_offset_limit(url=url_base + "/users", limite_por_pagina=2)

    assert len(resultados) == 4
    assert resultados[0]["id"] == 1
    assert resultados[3]["id"] == 4
    assert len(responses.calls) == 3


@responses.activate
def test_paginar_offset_limit_con_nombres_params_personalizados(url_base):
    """Debe usar nombres de parámetros personalizados."""
    responses.add(responses.GET, url_base + "/users", json=[{"id": 1}], status=200)
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    resultados = paginar_offset_limit(
        url=url_base + "/users",
        limite_por_pagina=10,
        nombre_param_offset="skip",
        nombre_param_limit="take",
    )

    assert len(resultados) == 1
    # Verificar que se usaron los nombres correctos
    primera_request = responses.calls[0].request.url
    assert "skip=0" in primera_request
    assert "take=10" in primera_request


@responses.activate
def test_paginar_offset_limit_con_params_adicionales(url_base):
    """Debe incluir parámetros adicionales en todas las requests."""
    responses.add(responses.GET, url_base + "/users", json=[{"id": 1}], status=200)
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    resultados = paginar_offset_limit(
        url=url_base + "/users",
        limite_por_pagina=10,
        params_extra={"status": "active", "role": "admin"},
    )

    assert len(resultados) == 1
    # Verificar params en todas las requests
    for call in responses.calls:
        assert "status=active" in call.request.url
        assert "role=admin" in call.request.url


@responses.activate
def test_paginar_offset_limit_max_paginas(url_base):
    """Debe respetar max_paginas."""
    # 3 páginas con datos
    for i in range(3):
        responses.add(responses.GET, url_base + "/users", json=[{"id": i}], status=200)

    resultados = paginar_offset_limit(
        url=url_base + "/users", limite_por_pagina=1, max_paginas=2
    )

    # Solo debe haber hecho 2 requests (max_paginas=2)
    assert len(responses.calls) == 2
    assert len(resultados) == 2


@responses.activate
def test_paginar_offset_limit_con_headers(url_base):
    """Debe enviar headers en todas las requests."""
    responses.add(responses.GET, url_base + "/users", json=[{"id": 1}], status=200)
    responses.add(responses.GET, url_base + "/users", json=[], status=200)

    headers = {"Authorization": "Bearer token123"}
    resultados = paginar_offset_limit(
        url=url_base + "/users", limite_por_pagina=10, headers=headers
    )

    assert len(resultados) == 1
    # Verificar headers en todas las requests
    for call in responses.calls:
        assert "Authorization" in call.request.headers


def test_paginar_offset_limit_url_invalida():
    """Debe rechazar URL inválida."""
    with pytest.raises(ValueError, match="debe usar HTTPS"):
        paginar_offset_limit(url="http://api.ejemplo.com/users", limite_por_pagina=10)


def test_paginar_offset_limit_limite_invalido(url_base):
    """Debe rechazar limite_por_pagina inválido."""
    with pytest.raises(ValueError, match="debe ser al menos 1"):
        paginar_offset_limit(url=url_base + "/users", limite_por_pagina=0)


def test_paginar_offset_limit_max_paginas_invalido(url_base):
    """Debe rechazar max_paginas inválido."""
    with pytest.raises(ValueError, match="debe ser al menos 1"):
        paginar_offset_limit(
            url=url_base + "/users", limite_por_pagina=10, max_paginas=0
        )


# Tests de paginar_cursor()


@responses.activate
def test_paginar_cursor_una_pagina(url_base):
    """Debe extraer todos los datos de una sola página."""
    responses.add(
        responses.GET,
        url_base + "/users",
        json={
            "data": [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}],
            "pagination": {"next_cursor": None},
        },
        status=200,
    )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="data",
        campo_cursor="pagination.next_cursor",
    )

    assert len(resultados) == 2
    assert resultados[0]["id"] == 1
    assert len(responses.calls) == 1


@responses.activate
def test_paginar_cursor_multiples_paginas(url_base):
    """Debe iterar y combinar datos de múltiples páginas."""
    # Página 1
    responses.add(
        responses.GET,
        url_base + "/users",
        json={
            "data": [{"id": 1}, {"id": 2}],
            "pagination": {"next_cursor": "cursor_abc"},
        },
        status=200,
    )
    # Página 2
    responses.add(
        responses.GET,
        url_base + "/users",
        json={
            "data": [{"id": 3}, {"id": 4}],
            "pagination": {"next_cursor": "cursor_def"},
        },
        status=200,
    )
    # Página 3 (última)
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"data": [{"id": 5}], "pagination": {"next_cursor": None}},
        status=200,
    )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="data",
        campo_cursor="pagination.next_cursor",
    )

    assert len(resultados) == 5
    assert len(responses.calls) == 3


@responses.activate
def test_paginar_cursor_nombres_params_personalizados(url_base):
    """Debe usar nombre de parámetro de cursor personalizado."""
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"items": [{"id": 1}], "next": None},
        status=200,
    )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="items",
        campo_cursor="next",
        nombre_param_cursor="after",
    )

    assert len(resultados) == 1
    assert len(responses.calls) == 1


@responses.activate
def test_paginar_cursor_con_params_adicionales(url_base):
    """Debe incluir parámetros adicionales en todas las requests."""
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"data": [{"id": 1}], "next_cursor": None},
        status=200,
    )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="data",
        campo_cursor="next_cursor",
        params_extra={"status": "active"},
    )

    assert len(resultados) == 1
    assert "status=active" in responses.calls[0].request.url


@responses.activate
def test_paginar_cursor_max_paginas(url_base):
    """Debe respetar max_paginas."""
    # 3 páginas con datos
    for i in range(3):
        responses.add(
            responses.GET,
            url_base + "/users",
            json={"data": [{"id": i}], "next_cursor": f"cursor_{i}"},
            status=200,
        )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="data",
        campo_cursor="next_cursor",
        max_paginas=2,
    )

    assert len(responses.calls) == 2
    assert len(resultados) == 2


@responses.activate
def test_paginar_cursor_campo_anidado(url_base):
    """Debe extraer cursor de campo anidado."""
    responses.add(
        responses.GET,
        url_base + "/users",
        json={"results": [{"id": 1}], "meta": {"pagination": {"next": None}}},
        status=200,
    )

    resultados = paginar_cursor(
        url=url_base + "/users",
        campo_datos="results",
        campo_cursor="meta.pagination.next",
    )

    assert len(resultados) == 1
    assert len(responses.calls) == 1


def test_paginar_cursor_url_invalida():
    """Debe rechazar URL inválida."""
    with pytest.raises(ValueError, match="debe usar HTTPS"):
        paginar_cursor(
            url="http://api.ejemplo.com/users",
            campo_datos="data",
            campo_cursor="next_cursor",
        )


def test_paginar_cursor_campo_datos_vacio(url_base):
    """Debe rechazar campo_datos vacío."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        paginar_cursor(
            url=url_base + "/users", campo_datos="", campo_cursor="next_cursor"
        )


def test_paginar_cursor_campo_cursor_vacio(url_base):
    """Debe rechazar campo_cursor vacío."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        paginar_cursor(url=url_base + "/users", campo_datos="data", campo_cursor="")


def test_paginar_cursor_max_paginas_invalido(url_base):
    """Debe rechazar max_paginas inválido."""
    with pytest.raises(ValueError, match="debe ser al menos 1"):
        paginar_cursor(
            url=url_base + "/users",
            campo_datos="data",
            campo_cursor="next_cursor",
            max_paginas=0,
        )
