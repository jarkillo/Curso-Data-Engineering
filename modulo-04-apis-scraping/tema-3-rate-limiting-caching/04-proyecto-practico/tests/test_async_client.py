"""
Tests para async_client.py - Cliente HTTP Asíncrono (TDD)

Módulo 4 - Tema 3: Scraper Masivo Optimizado
Total de tests: 12
Cobertura objetivo: >80%
"""

import asyncio

import aiohttp
import pytest
from src.async_client import (
    cerrar_sesion,
    crear_sesion_http,
    obtener_url_async,
    obtener_urls_batch,
)

# ===============================
# Tests: Crear Sesión HTTP
# ===============================


@pytest.mark.asyncio
async def test_crear_sesion_http_con_headers_por_defecto():
    """Test: Crear sesión HTTP con headers por defecto."""
    session = await crear_sesion_http()

    assert session is not None
    assert isinstance(session, aiohttp.ClientSession)

    # Verificar User-Agent por defecto
    assert "User-Agent" in session.headers

    await cerrar_sesion(session)


@pytest.mark.asyncio
async def test_crear_sesion_con_headers_personalizados():
    """Test: Crear sesión con headers personalizados."""
    headers_custom = {"User-Agent": "TestBot/1.0", "Authorization": "Bearer test_token"}

    session = await crear_sesion_http(headers=headers_custom)

    assert session is not None
    assert session.headers["User-Agent"] == "TestBot/1.0"
    assert session.headers["Authorization"] == "Bearer test_token"

    await cerrar_sesion(session)


# ===============================
# Tests: Obtener URL Async
# ===============================


@pytest.mark.asyncio
async def test_get_request_async_exitoso():
    """Test: GET request async exitoso (200)."""
    session = await crear_sesion_http()

    # Usar API pública de prueba
    url = "https://jsonplaceholder.typicode.com/posts/1"
    resultado = await obtener_url_async(session, url, timeout=10)

    assert resultado is not None
    assert resultado["status"] == 200
    assert "datos" in resultado
    assert resultado["datos"]["id"] == 1
    assert "title" in resultado["datos"]

    await cerrar_sesion(session)


@pytest.mark.asyncio
async def test_retornar_json_parseado_automaticamente():
    """Test: Retornar JSON parseado automáticamente."""
    session = await crear_sesion_http()

    url = "https://jsonplaceholder.typicode.com/users/1"
    resultado = await obtener_url_async(session, url, timeout=10)

    # Verificar que el JSON fue parseado
    assert isinstance(resultado["datos"], dict)
    assert "name" in resultado["datos"]
    assert "email" in resultado["datos"]

    await cerrar_sesion(session)


@pytest.mark.asyncio
async def test_timeout_si_request_tarda_mucho():
    """Test: Timeout si request tarda más de N segundos."""
    session = await crear_sesion_http()

    # URL que simula delay (httpbin con delay de 10 segundos)
    url = "https://httpbin.org/delay/10"

    with pytest.raises(asyncio.TimeoutError):
        await obtener_url_async(session, url, timeout=2)  # Timeout de 2 seg

    await cerrar_sesion(session)


@pytest.mark.asyncio
async def test_manejo_error_404():
    """Test: Manejo de error 404."""
    session = await crear_sesion_http()

    url = "https://jsonplaceholder.typicode.com/posts/999999"
    resultado = await obtener_url_async(session, url, timeout=10)

    assert resultado["status"] == 404
    assert resultado["error"] is True

    await cerrar_sesion(session)


@pytest.mark.asyncio
async def test_manejo_error_500():
    """Test: Manejo de error 500."""
    session = await crear_sesion_http()

    # httpbin puede simular error 500
    url = "https://httpbin.org/status/500"
    resultado = await obtener_url_async(session, url, timeout=10)

    assert resultado["status"] == 500
    assert resultado["error"] is True

    await cerrar_sesion(session)


# ===============================
# Tests: Obtener URLs en Batch
# ===============================


@pytest.mark.asyncio
async def test_obtener_batch_urls_en_paralelo():
    """Test: Obtener batch de URLs en paralelo."""
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]

    resultados = await obtener_urls_batch(urls, max_concurrente=3, timeout=10)

    assert len(resultados) == 3
    assert all(r["status"] == 200 for r in resultados)
    assert all("datos" in r for r in resultados)


@pytest.mark.asyncio
async def test_limitar_concurrencia_con_semaforo():
    """Test: Limitar concurrencia con semáforo."""
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]

    # Limitar a 5 requests concurrentes
    resultados = await obtener_urls_batch(urls, max_concurrente=5, timeout=10)

    assert len(resultados) == 10
    # Verificar que se procesaron todas las URLs
    exitosos = [r for r in resultados if r["status"] == 200]
    assert len(exitosos) >= 8  # Al menos 8 de 10 deben ser exitosos


@pytest.mark.asyncio
async def test_batch_con_urls_mixtas_algunas_fallan():
    """Test: Batch con URLs mixtas (algunas fallan)."""
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",  # Exitosa
        "https://jsonplaceholder.typicode.com/posts/999999",  # 404
        "https://jsonplaceholder.typicode.com/posts/2",  # Exitosa
    ]

    resultados = await obtener_urls_batch(urls, max_concurrente=3, timeout=10)

    assert len(resultados) == 3

    # Verificar que hay éxitos y fallos
    exitosos = [r for r in resultados if r["status"] == 200]
    fallidos = [r for r in resultados if r["status"] == 404]

    assert len(exitosos) == 2
    assert len(fallidos) == 1


@pytest.mark.asyncio
async def test_cerrar_sesion_correctamente():
    """Test: Cerrar sesión correctamente."""
    session = await crear_sesion_http()

    assert not session.closed

    await cerrar_sesion(session)

    assert session.closed


@pytest.mark.asyncio
@pytest.mark.slow
async def test_performance_50_urls_en_menos_5_segundos():
    """Test: Performance - 50 URLs en <5 segundos."""
    import time

    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 51)]

    inicio = time.time()
    resultados = await obtener_urls_batch(urls, max_concurrente=20, timeout=10)
    fin = time.time()

    tiempo_total = fin - inicio

    assert len(resultados) == 50
    assert tiempo_total < 10  # Debe completarse en menos de 10 segundos

    # Verificar que la mayoría fueron exitosos
    exitosos = [r for r in resultados if r.get("status") == 200]
    assert len(exitosos) >= 40  # Al menos 40 de 50 exitosos
