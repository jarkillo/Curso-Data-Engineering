"""
Módulo de Scraping HTML con BeautifulSoup
==========================================

Funciones para extraer datos de páginas web estáticas.
"""

from bs4 import BeautifulSoup


def extraer_titulos(html: str, selector: str) -> list[str]:
    """
    Extrae todos los textos de elementos que coinciden con un selector CSS.

    Args:
        html: Contenido HTML como string
        selector: Selector CSS (ej: "h1", ".clase", "#id")

    Returns:
        Lista de textos extraídos (sin espacios extra)

    Raises:
        ValueError: Si html está vacío o selector es inválido
    """
    if not html or html.strip() == "":
        raise ValueError("El HTML no puede estar vacío")

    if not selector or selector.strip() == "":
        raise ValueError("El selector no puede estar vacío")

    soup = BeautifulSoup(html, "html.parser")
    elementos = soup.select(selector)

    return [elem.get_text(strip=True) for elem in elementos]


def extraer_enlaces(html: str, selector: str = "a") -> list[dict[str, str]]:
    """
    Extrae enlaces (href) y sus textos asociados.

    Args:
        html: Contenido HTML como string
        selector: Selector CSS para los enlaces (default: "a")

    Returns:
        Lista de diccionarios con keys: "texto", "url"

    Raises:
        ValueError: Si html está vacío
    """
    if not html or html.strip() == "":
        raise ValueError("El HTML no puede estar vacío")

    soup = BeautifulSoup(html, "html.parser")
    enlaces = soup.select(selector)

    resultado = []
    for enlace in enlaces:
        href = enlace.get("href")
        if href:  # Solo incluir enlaces con href
            resultado.append({"texto": enlace.get_text(strip=True), "url": href})

    return resultado


def extraer_tabla(  # noqa: C901
    html: str, selector: str = "table"
) -> list[dict[str, str]]:
    """
    Convierte una tabla HTML en lista de diccionarios.

    Args:
        html: Contenido HTML como string
        selector: Selector CSS de la tabla

    Returns:
        Lista de diccionarios donde keys son los headers de la tabla

    Raises:
        ValueError: Si no encuentra la tabla o no tiene headers
    """
    if not html or html.strip() == "":
        raise ValueError("El HTML no puede estar vacío")

    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.select_one(selector)

    if not tabla:
        raise ValueError(f"No se encontró la tabla con selector '{selector}'")

    # Intentar extraer headers de <thead> o primera fila
    headers = []
    thead = tabla.find("thead")
    skip_first_row = False

    if thead:
        headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
    else:
        # Buscar primera fila
        primera_fila = tabla.find("tr")
        if primera_fila:
            # Verificar si tiene elementos <th> o <strong> (indicadores de headers)
            ths = primera_fila.find_all("th")
            if ths:
                headers = [th.get_text(strip=True) for th in ths]
                skip_first_row = True
            else:
                # Buscar <strong> dentro de <td>
                strongs = primera_fila.find_all("strong")
                if strongs:
                    headers = [strong.get_text(strip=True) for strong in strongs]
                    skip_first_row = True
                else:
                    # Si no hay indicadores, intentar con todas las celdas de la primera fila
                    celdas = primera_fila.find_all(["td", "th"])
                    if celdas:
                        # Solo considerar headers si parece razonable (no son datos)
                        # Si todas las celdas tienen texto corto, podrían ser headers
                        textos = [c.get_text(strip=True) for c in celdas]
                        if all(len(t) < 50 and t for t in textos):
                            headers = textos
                            skip_first_row = True

    if not headers:
        raise ValueError("La tabla no tiene headers válidos")

    # Extraer filas de datos
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


def extraer_atributo(html: str, selector: str, atributo: str) -> list[str]:
    """
    Extrae un atributo específico de elementos seleccionados.

    Args:
        html: Contenido HTML como string
        selector: Selector CSS
        atributo: Nombre del atributo (ej: "href", "src", "data-id")

    Returns:
        Lista de valores del atributo

    Raises:
        ValueError: Si html vacío o selector inválido
    """
    if not html or html.strip() == "":
        raise ValueError("El HTML no puede estar vacío")

    if not selector or selector.strip() == "":
        raise ValueError("El selector no puede estar vacío")

    soup = BeautifulSoup(html, "html.parser")
    elementos = soup.select(selector)

    resultado = []
    for elem in elementos:
        valor = elem.get(atributo)
        if valor:
            resultado.append(valor)

    return resultado


def extraer_datos_estructurados(  # noqa: C901
    html: str, selectores: dict[str, str]
) -> list[dict[str, str]]:
    """
    Extrae múltiples datos estructurados usando un mapa de selectores.

    Args:
        html: Contenido HTML como string
        selectores: Dict con formato {"campo": "selector_css"}

    Returns:
        Lista de diccionarios con los datos extraídos

    Raises:
        ValueError: Si html vacío o selectores inválido
    """
    if not html or html.strip() == "":
        raise ValueError("El HTML no puede estar vacío")

    if not selectores or len(selectores) == 0:
        raise ValueError("El diccionario de selectores no puede estar vacío")

    soup = BeautifulSoup(html, "html.parser")

    # Detectar contenedores principales (ej: divs con clase común)
    # Asumimos que el primer selector nos da la "estructura" de items
    primer_campo = list(selectores.keys())[0]
    primer_selector = selectores[primer_campo]
    elementos_principales = soup.select(primer_selector)

    if not elementos_principales:
        return []

    # Encontrar el contenedor padre común
    # Estrategia: buscar todos los elementos que tengan hijos con los selectores
    contenedores = set()
    for elem in elementos_principales:
        parent = elem.parent
        while parent and parent.name != "html":
            contenedores.add(parent)
            parent = parent.parent

    # Intentar encontrar el contenedor más específico que se repite
    soup_items = soup.find_all(class_=True)
    posibles_contenedores = []

    for tag in soup_items:
        # Verificar si este tag contiene AL MENOS UN elemento de cada selector
        tiene_alguno = False
        for selector in selectores.values():
            if tag.select_one(selector):
                tiene_alguno = True
                break
        if tiene_alguno:
            posibles_contenedores.append(tag)

    # Filtrar contenedores que realmente tengan al menos un campo
    contenedores_validos = []
    for cont in posibles_contenedores:
        tiene_campo = False
        for selector in selectores.values():
            if cont.select_one(selector):
                tiene_campo = True
                break
        if tiene_campo:
            contenedores_validos.append(cont)

    if not contenedores_validos:
        # Estrategia alternativa: asumir estructura plana
        resultado = {}
        for campo, selector in selectores.items():
            elementos = soup.select(selector)
            resultado[campo] = elementos[0].get_text(strip=True) if elementos else ""
        return [resultado] if resultado else []

    # Extraer datos de cada contenedor
    resultado = []
    for contenedor in contenedores_validos:
        item = {}
        for campo, selector in selectores.items():
            elem = contenedor.select_one(selector)
            item[campo] = elem.get_text(strip=True) if elem else ""
        resultado.append(item)

    return resultado
