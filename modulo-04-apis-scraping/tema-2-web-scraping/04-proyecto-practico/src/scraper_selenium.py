"""
Módulo de Scraping con Selenium
================================

Funciones para extraer datos de páginas web dinámicas (JavaScript).
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extraer_con_espera(
    driver: webdriver.Chrome, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10
) -> list[str]:
    """
    Extrae textos de elementos esperando a que se carguen (JS dinámico).

    Args:
        driver: Instancia de Selenium WebDriver
        selector: Selector del elemento (CSS, XPath, etc.)
        by: Tipo de selector (default: CSS_SELECTOR)
        timeout: Segundos máximos de espera

    Returns:
        Lista de textos extraídos de los elementos

    Raises:
        TimeoutError: Si los elementos no aparecen en el tiempo límite
        ValueError: Si selector está vacío
    """
    if not selector or selector.strip() == "":
        raise ValueError("El selector no puede estar vacío")

    try:
        wait = WebDriverWait(driver, timeout)
        elementos = wait.until(EC.presence_of_all_elements_located((by, selector)))
        return [elem.text for elem in elementos]
    except Exception as e:
        raise TimeoutError(
            f"Timeout esperando elementos con selector '{selector}': {e}"
        )


def extraer_tabla_dinamica(  # noqa: C901
    driver: webdriver.Chrome, selector_tabla: str = "table", timeout: int = 10
) -> list[dict[str, str]]:
    """
    Extrae una tabla cargada dinámicamente con JavaScript.

    Args:
        driver: Instancia de Selenium WebDriver
        selector_tabla: Selector CSS de la tabla
        timeout: Segundos máximos de espera

    Returns:
        Lista de diccionarios con los datos de la tabla

    Raises:
        TimeoutError: Si la tabla no se carga
        ValueError: Si la tabla no tiene estructura válida
    """
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_tabla)))

        # Obtener el HTML de la página y parsearlo con BeautifulSoup
        from bs4 import BeautifulSoup

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        tabla = soup.select_one(selector_tabla)
        if not tabla:
            raise TimeoutError(
                f"No se encontró la tabla con selector '{selector_tabla}'"
            )

        # Extraer headers (usando la misma lógica que extraer_tabla)
        headers = []
        thead = tabla.find("thead")
        skip_first_row = False

        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
        else:
            primera_fila = tabla.find("tr")
            if primera_fila:
                ths = primera_fila.find_all("th")
                if ths:
                    headers = [th.get_text(strip=True) for th in ths]
                    skip_first_row = True
                else:
                    strongs = primera_fila.find_all("strong")
                    if strongs:
                        headers = [strong.get_text(strip=True) for strong in strongs]
                        skip_first_row = True

        if not headers:
            raise ValueError("La tabla no tiene estructura válida (sin headers)")

        # Extraer filas
        tbody = tabla.find("tbody") or tabla
        all_filas = tbody.find_all("tr")
        filas = all_filas[1:] if (skip_first_row and not thead) else all_filas

        resultado = []
        for fila in filas:
            celdas = fila.find_all(["td", "th"])
            if celdas:
                fila_dict = {}
                for i, celda in enumerate(celdas):
                    if i < len(headers):
                        fila_dict[headers[i]] = celda.get_text(strip=True)
                if fila_dict:
                    resultado.append(fila_dict)

        return resultado

    except TimeoutException as e:
        raise TimeoutError(f"Timeout esperando tabla: {e}")
    except Exception as e:
        if "Timeout" in str(e) or "timeout" in str(e):
            raise TimeoutError(f"Timeout esperando tabla: {e}")
        raise


def hacer_scroll_infinito(
    driver: webdriver.Chrome,
    selector_items: str,
    max_scrolls: int = 10,
    pausa: float = 2.0,
) -> int:
    """
    Hace scroll infinito para cargar más contenido dinámico.

    Args:
        driver: Instancia de Selenium WebDriver
        selector_items: Selector CSS de los items a contar
        max_scrolls: Número máximo de scrolls
        pausa: Segundos de pausa entre scrolls

    Returns:
        Número total de items cargados después del scroll

    Raises:
        ValueError: Si max_scrolls < 1 o pausa < 0
    """
    if max_scrolls < 1:
        raise ValueError("max_scrolls debe ser mayor o igual a 1")

    if pausa < 0:
        raise ValueError("pausa no puede ser negativa")

    import time

    items_anteriores = 0
    for _i in range(max_scrolls):
        # Hacer scroll al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pausa)

        # Contar items actuales
        items_actuales = len(driver.find_elements(By.CSS_SELECTOR, selector_items))

        # Si no se cargaron más items, detener
        if items_actuales == items_anteriores:
            break

        items_anteriores = items_actuales

    return items_anteriores
