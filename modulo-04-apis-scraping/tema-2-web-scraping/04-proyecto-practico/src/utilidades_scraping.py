"""
Módulo de Utilidades de Scraping
=================================

Funciones auxiliares para logging, headers y manejo de errores.
"""

import logging
import random


def configurar_logging(
    nivel: str = "INFO", archivo: str | None = None
) -> logging.Logger:
    """
    Configura el sistema de logging para el scraper.

    Args:
        nivel: Nivel de logging ("DEBUG", "INFO", "WARNING", "ERROR")
        archivo: Ruta opcional para guardar logs en archivo

    Returns:
        Logger configurado

    Raises:
        ValueError: Si el nivel es inválido
    """
    niveles_validos = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if nivel.upper() not in niveles_validos:
        raise ValueError(f"Nivel inválido. Debe ser uno de: {niveles_validos}")

    # Crear logger
    logger = logging.getLogger("scraper")
    logger.setLevel(getattr(logging, nivel.upper()))

    # Limpiar handlers existentes
    logger.handlers.clear()

    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo (opcional)
    if archivo:
        import os

        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        file_handler = logging.FileHandler(archivo, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def crear_headers_aleatorios() -> dict[str, str]:
    """
    Genera headers HTTP con User-Agent aleatorio para evitar bloqueos.

    Returns:
        Diccionario con headers (User-Agent, Accept, Accept-Language, etc.)

    Nota:
        Rota entre varios User-Agents realistas de navegadores modernos
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    ]

    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def limpiar_texto(texto: str) -> str:
    """
    Limpia texto extraído de HTML (espacios extra, saltos de línea, tabs).

    Args:
        texto: Texto crudo a limpiar

    Returns:
        Texto limpio sin espacios/saltos innecesarios

    Raises:
        ValueError: Si texto es None
    """
    if texto is None:
        raise ValueError("El texto no puede ser None")

    import re

    # Reemplazar saltos de línea y tabs por espacios
    texto = texto.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Eliminar espacios múltiples
    texto = re.sub(r"\s+", " ", texto)

    # Eliminar espacios al inicio y final
    texto = texto.strip()

    return texto


def extraer_dominio(url: str) -> str:
    """
    Extrae el dominio base de una URL completa.

    Args:
        url: URL completa (ej: "https://example.com/page?id=123")

    Returns:
        Dominio base (ej: "example.com")

    Raises:
        ValueError: Si la URL es inválida o vacía

    Ejemplo:
        >>> extraer_dominio("https://www.example.com/path")
        "www.example.com"
    """
    if not url or url.strip() == "":
        raise ValueError("La URL no puede estar vacía")

    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)

        # Validar protocolo (solo http o https)
        if parsed.scheme not in ["http", "https"]:
            raise ValueError("URL inválida: protocolo no soportado")

        # Validar que tenga dominio
        if not parsed.netloc:
            raise ValueError("URL inválida: sin dominio")

        # Retornar dominio (sin puerto)
        dominio = parsed.netloc
        if ":" in dominio:
            dominio = dominio.split(":")[0]

        return dominio

    except ValueError:
        raise
    except Exception:
        raise ValueError("URL inválida")
