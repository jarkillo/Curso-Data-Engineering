"""
Módulo de extracción de datos mediante Web Scraping.

Funciones para extraer datos de páginas web respetando robots.txt,
usando Beautiful Soup y manejando errores robustamente.
"""

import logging
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def verificar_robots_txt(url: str, user_agent: str = "*") -> bool:
    """
    Verifica si el scraping está permitido según robots.txt.

    Args:
        url: URL de la página a scrapear
        user_agent: User agent a verificar (default: '*')

    Returns:
        True si el scraping está permitido, False en caso contrario

    Examples:
        >>> permitido = verificar_robots_txt('https://ejemplo.com/datos')
    """
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()

        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logger.warning(f"Error al leer robots.txt: {e}. Asumiendo permitido.")
        return True


def extraer_html(
    url: str,
    user_agent: str = "DataExtractor/1.0",
    timeout: int = 30,
    verificar_robots: bool = True,
) -> str:
    """
    Extrae el HTML de una URL.

    Args:
        url: URL de la página
        user_agent: User agent a usar
        timeout: Timeout en segundos
        verificar_robots: Si True, verifica robots.txt primero

    Returns:
        HTML como string

    Raises:
        ValueError: Si el scraping no está permitido
        requests.HTTPError: Si la petición falla
    """
    if verificar_robots and not verificar_robots_txt(url, user_agent):
        raise ValueError(f"Scraping no permitido por robots.txt: {url}")

    headers = {"User-Agent": user_agent}
    respuesta = requests.get(url, headers=headers, timeout=timeout)
    respuesta.raise_for_status()

    return respuesta.text


def parsear_con_beautifulsoup(html: str, parser: str = "html.parser") -> BeautifulSoup:
    """
    Parsea HTML con Beautiful Soup.

    Args:
        html: String HTML
        parser: Parser a usar ('html.parser', 'lxml', 'html5lib')

    Returns:
        Objeto BeautifulSoup
    """
    return BeautifulSoup(html, parser)


def extraer_tabla_html(soup: BeautifulSoup, selector: str | None = None) -> list[dict]:
    """
    Extrae datos de una tabla HTML.

    Args:
        soup: Objeto BeautifulSoup
        selector: Selector CSS para la tabla (None = primera tabla)

    Returns:
        Lista de diccionarios con los datos
    """
    if selector:
        tabla = soup.select_one(selector)
    else:
        tabla = soup.find("table")

    if not tabla:
        return []

    headers = [th.get_text(strip=True) for th in tabla.find_all("th")]
    if not headers:
        # Si no hay headers, usar números
        primera_fila = tabla.find("tr")
        if primera_fila:
            headers = [f"col_{i}" for i in range(len(primera_fila.find_all("td")))]

    filas = []
    for tr in tabla.find_all("tr")[1 if tabla.find_all("th") else 0 :]:
        celdas = [td.get_text(strip=True) for td in tr.find_all("td")]
        if celdas:
            fila = dict(zip(headers, celdas))
            filas.append(fila)

    return filas


def extraer_elementos_por_selector(
    soup: BeautifulSoup,
    selector: str,
    extraer_texto: bool = True,
    extraer_atributo: str | None = None,
) -> list[str]:
    """
    Extrae elementos usando selector CSS.

    Args:
        soup: Objeto BeautifulSoup
        selector: Selector CSS
        extraer_texto: Si True, extrae el texto
        extraer_atributo: Atributo a extraer (ej: 'href', 'src')

    Returns:
        Lista de textos o atributos extraídos
    """
    elementos = soup.select(selector)

    if extraer_atributo:
        return [elem.get(extraer_atributo, "") for elem in elementos]
    elif extraer_texto:
        return [elem.get_text(strip=True) for elem in elementos]
    else:
        return [str(elem) for elem in elementos]
