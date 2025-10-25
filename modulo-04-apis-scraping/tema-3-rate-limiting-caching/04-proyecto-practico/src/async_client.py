"""
Async Client - Cliente HTTP asíncrono con aiohttp

Este módulo implementa un cliente HTTP asíncrono para realizar
múltiples requests en paralelo de forma eficiente.

Características:
- Requests asíncronos con aiohttp
- Control de concurrencia con Semaphore
- Manejo robusto de errores y timeouts
- Gestión automática de sesiones HTTP

Ejemplo de uso:
    import asyncio

    async def main():
        # Crear sesión
        session = await crear_sesion_http()

        # Obtener una URL
        resultado = await obtener_url_async(session, "https://api.example.com/data")

        # Obtener múltiples URLs en paralelo
        urls = ["https://api.example.com/1", "https://api.example.com/2"]
        resultados = await obtener_urls_batch(urls, max_concurrente=10)

        # Cerrar sesión
        await cerrar_sesion(session)

    asyncio.run(main())
"""

import asyncio
from typing import Dict, List, Optional

import aiohttp


async def crear_sesion_http(headers: Optional[Dict] = None) -> aiohttp.ClientSession:
    """
    Crea una sesión HTTP asíncrona con aiohttp.

    Args:
        headers: Headers HTTP personalizados (opcional)

    Returns:
        Sesión HTTP de aiohttp

    Ejemplo:
        >>> async def test():
        ...     session = await crear_sesion_http()
        ...     assert isinstance(session, aiohttp.ClientSession)
        ...     await cerrar_sesion(session)
        >>> asyncio.run(test())
    """
    if headers is None:
        headers = {"User-Agent": "DataHub-Scraper/1.0 (Optimized Async Client)"}

    # Configurar timeout por defecto
    timeout = aiohttp.ClientTimeout(total=30)

    session = aiohttp.ClientSession(headers=headers, timeout=timeout)

    return session


async def obtener_url_async(
    session: aiohttp.ClientSession, url: str, timeout: int = 10
) -> Dict:
    """
    Obtiene una URL de forma asíncrona.

    Args:
        session: Sesión HTTP de aiohttp
        url: URL a consultar
        timeout: Timeout en segundos (default: 10)

    Returns:
        Diccionario con status, datos, y posible error

    Raises:
        asyncio.TimeoutError: Si el request excede el timeout

    Ejemplo:
        >>> async def test():
        ...     session = await crear_sesion_http()
        ...     resultado = await obtener_url_async(
        ...         session,
        ...         "https://jsonplaceholder.typicode.com/posts/1"
        ...     )
        ...     assert resultado["status"] == 200
        ...     await cerrar_sesion(session)
        >>> asyncio.run(test())
    """
    try:
        async with asyncio.timeout(timeout):
            async with session.get(url) as response:
                status = response.status

                # Intentar parsear JSON
                try:
                    datos = await response.json()
                except Exception:
                    # Si no es JSON, obtener texto
                    datos = await response.text()

                return {
                    "url": url,
                    "status": status,
                    "datos": datos,
                    "error": status >= 400,
                }

    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(f"Timeout al obtener URL: {url}")

    except Exception as e:
        return {
            "url": url,
            "status": 0,
            "datos": None,
            "error": True,
            "mensaje_error": str(e),
        }


async def obtener_urls_batch(
    urls: List[str], max_concurrente: int = 20, timeout: int = 10
) -> List[Dict]:
    """
    Obtiene múltiples URLs en paralelo con control de concurrencia.

    Args:
        urls: Lista de URLs a consultar
        max_concurrente: Número máximo de requests simultáneos (default: 20)
        timeout: Timeout por request en segundos (default: 10)

    Returns:
        Lista de resultados (uno por cada URL)

    Ejemplo:
        >>> async def test():
        ...     urls = [
        ...         "https://jsonplaceholder.typicode.com/posts/1",
        ...         "https://jsonplaceholder.typicode.com/posts/2"
        ...     ]
        ...     resultados = await obtener_urls_batch(urls, max_concurrente=5)
        ...     assert len(resultados) == 2
        >>> asyncio.run(test())
    """
    # Crear sesión compartida
    session = await crear_sesion_http()

    # Crear semáforo para limitar concurrencia
    semaforo = asyncio.Semaphore(max_concurrente)

    async def obtener_con_semaforo(url: str) -> Dict:
        """
        Wrapper para obtener URL respetando el semáforo.
        """
        async with semaforo:
            try:
                return await obtener_url_async(session, url, timeout)
            except asyncio.TimeoutError:
                return {
                    "url": url,
                    "status": 0,
                    "datos": None,
                    "error": True,
                    "mensaje_error": "Timeout",
                }
            except Exception as e:
                return {
                    "url": url,
                    "status": 0,
                    "datos": None,
                    "error": True,
                    "mensaje_error": str(e),
                }

    # Ejecutar todas las tareas en paralelo
    tareas = [obtener_con_semaforo(url) for url in urls]
    resultados = await asyncio.gather(*tareas, return_exceptions=False)

    # Cerrar sesión
    await cerrar_sesion(session)

    return resultados


async def cerrar_sesion(session: aiohttp.ClientSession) -> None:
    """
    Cierra la sesión HTTP de forma segura.

    Args:
        session: Sesión HTTP de aiohttp

    Ejemplo:
        >>> async def test():
        ...     session = await crear_sesion_http()
        ...     await cerrar_sesion(session)
        ...     assert session.closed
        >>> asyncio.run(test())
    """
    if session and not session.closed:
        await session.close()
        # Esperar un poco para que se cierren las conexiones
        await asyncio.sleep(0.1)
