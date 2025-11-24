"""
Módulo de Validación de Scraping
=================================

Funciones para validar robots.txt, rate limiting y buenas prácticas.
"""

import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


def validar_robots_txt(url: str, user_agent: str = "*") -> bool:
    """
    Verifica si una URL puede ser scrapeada según robots.txt.

    Args:
        url: URL completa a validar (ej: "https://example.com/page")
        user_agent: User-Agent del scraper (default: "*")

    Returns:
        True si está permitido scrapear, False si no

    Raises:
        ValueError: Si la URL es inválida o vacía
    """
    if not url or url.strip() == "":
        raise ValueError("La URL no puede estar vacía")

    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("URL inválida")

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        rp = RobotFileParser()
        rp.set_url(robots_url)

        try:
            rp.read()
        except Exception:
            # Si no se puede leer robots.txt, permitir por defecto (más permisivo)
            return True

        return rp.can_fetch(user_agent, url)

    except Exception:
        # En caso de error, ser permisivo
        return True


def validar_url(url: str) -> bool:
    """
    Valida que una URL tenga formato correcto y protocolo válido.

    Args:
        url: URL a validar

    Returns:
        True si la URL es válida, False si no

    Raises:
        ValueError: Si url es None o vacía
    """
    if url is None or (isinstance(url, str) and url.strip() == ""):
        raise ValueError("La URL no puede estar vacía o ser None")

    try:
        parsed = urlparse(url)

        # Validar protocolo (solo http o https)
        if parsed.scheme not in ["http", "https"]:
            return False

        # Validar que tenga dominio
        return parsed.netloc

    except Exception:
        return False


def calcular_delay_rate_limit(
    tiempo_ultima_peticion: float, delay_minimo: float = 1.0
) -> float:
    """
    Calcula cuántos segundos esperar antes de la siguiente petición.

    Args:
        tiempo_ultima_peticion: Timestamp de la última petición (time.time())
        delay_minimo: Segundos mínimos entre peticiones

    Returns:
        Segundos a esperar (0 si ya pasó suficiente tiempo)

    Raises:
        ValueError: Si delay_minimo es negativo o tiempo_ultima_peticion es inválido
    """
    if delay_minimo < 0:
        raise ValueError("delay_minimo no puede ser negativo")

    if tiempo_ultima_peticion < 0:
        raise ValueError("tiempo_ultima_peticion no puede ser negativo")

    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_ultima_peticion

    tiempo_a_esperar = delay_minimo - tiempo_transcurrido

    return max(0, tiempo_a_esperar)


def validar_contenido_html(html: str, min_length: int = 100) -> dict:
    """
    Valida que el contenido HTML sea válido y suficiente.

    Args:
        html: Contenido HTML a validar
        min_length: Longitud mínima esperada en caracteres

    Returns:
        Dict con keys:
            - "valido": bool
            - "longitud": int
            - "tiene_html": bool (contiene tags HTML)
            - "mensaje": str (descripción del resultado)

    Raises:
        ValueError: Si html es None o min_length < 0
    """
    if html is None:
        raise ValueError("El HTML no puede ser None")

    if min_length < 0:
        raise ValueError("min_length no puede ser negativo")

    longitud = len(html)

    # Verificar si contiene tags HTML
    tiene_html = "<" in html and ">" in html

    # Validar longitud
    longitud_valida = longitud >= min_length

    # Determinar validez general
    valido = longitud_valida and tiene_html

    # Mensaje descriptivo
    if valido:
        mensaje = "Contenido HTML válido y suficiente"
    elif not longitud_valida:
        mensaje = (
            f"Contenido muy corto o insuficiente ({longitud} < {min_length} caracteres)"
        )
    elif not tiene_html:
        mensaje = "El contenido no contiene tags HTML válidos"
    else:
        mensaje = "Contenido inválido"

    return {
        "valido": valido,
        "longitud": longitud,
        "tiene_html": tiene_html,
        "mensaje": mensaje,
    }
