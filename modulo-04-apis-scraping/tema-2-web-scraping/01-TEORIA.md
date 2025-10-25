# 📖 Tema 2: Web Scraping - Teoría

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📋 Índice

1. [Introducción](#introducción)
2. [¿Qué es Web Scraping?](#qué-es-web-scraping)
3. [HTML, CSS y DOM](#html-css-y-dom)
4. [BeautifulSoup: Parsing de HTML](#beautifulsoup-parsing-de-html)
5. [Selenium: Scraping Dinámico](#selenium-scraping-dinámico)
6. [Robots.txt y Ética del Scraping](#robotstxt-y-ética-del-scraping)
7. [User-Agent y Headers](#user-agent-y-headers)
8. [XPath y CSS Selectors](#xpath-y-css-selectors)
9. [Almacenamiento de Datos Scrapeados](#almacenamiento-de-datos-scrapeados)
10. [Web Scraping vs APIs](#web-scraping-vs-apis)
11. [Legalidad y Ética](#legalidad-y-ética)
12. [Errores Comunes](#errores-comunes)
13. [Buenas Prácticas](#buenas-prácticas)
14. [Checklist de Aprendizaje](#checklist-de-aprendizaje)

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este tema, serás capaz de:

✅ **Entender qué es web scraping** y cuándo es la herramienta adecuada
✅ **Parsear HTML** con BeautifulSoup para extraer datos estructurados
✅ **Usar Selenium** para scraping de páginas con JavaScript dinámico
✅ **Respetar robots.txt** y aplicar scraping ético
✅ **Configurar User-Agent** y headers apropiados
✅ **Dominar selectores** (CSS y XPath) para extraer datos precisos
✅ **Almacenar datos scrapeados** de forma estructurada (CSV, JSON, SQLite)
✅ **Decidir entre scraping y APIs** según el contexto
✅ **Aplicar consideraciones legales** (GDPR, términos de servicio)

---

## 📚 Introducción

### ¿Por qué importa el Web Scraping en Data Engineering?

Imagina que necesitas analizar los precios de 10,000 productos de un e-commerce para un estudio de mercado, pero **no tienen una API pública**. O quieres monitorear las ofertas de empleo en LinkedIn para detectar tendencias del sector, pero su API está limitada. ¿Qué haces? 🤔

**Web scraping** es tu respuesta.

En **Data Engineering**, aproximadamente el **30-40% de la extracción de datos** proviene de scraping porque:
- Muchas fuentes NO tienen APIs
- Algunas APIs son muy costosas o restrictivas
- A veces necesitas datos que solo están en la interfaz visual

**Empresas que usan scraping masivo:**
- **Google**: Scrapers para indexar la web
- **Amazon**: Monitoreo de precios de competidores
- **DataHub Inc.**: Extracción de datos de mercado para análisis

---

## 🌐 ¿Qué es Web Scraping?

### Definición

> **Web scraping** es el proceso automatizado de extraer datos de sitios web mediante la descarga y análisis del HTML de las páginas.

### Analogía: La Biblioteca

Imagina que eres un investigador en una **biblioteca gigante sin sistema computarizado**:

- 📚 **Libros** = Páginas web
- 📖 **Páginas de libro** = HTML
- 🔍 **Tú buscando manualmente** = Navegador humano
- 🤖 **Tu asistente robot** = Web scraper

Tu robot:
1. Va a la estantería (hace request HTTP)
2. Abre el libro (descarga HTML)
3. Lee línea por línea (parsea HTML)
4. Anota lo importante en una ficha (extrae datos)
5. Guarda las fichas en un archivero (almacena en CSV/DB)

¡Hace en segundos lo que te tomaría horas! ⚡

---

### El Proceso de Web Scraping

```
1️⃣ REQUEST HTTP
   ↓
   GET https://ejemplo.com/productos

2️⃣ RESPUESTA HTML
   ↓
   <html><body><div class="producto">...</div></body></html>

3️⃣ PARSING
   ↓
   BeautifulSoup/Selenium parsea el HTML

4️⃣ EXTRACCIÓN
   ↓
   Encuentra elementos con selectores (CSS, XPath)

5️⃣ LIMPIEZA
   ↓
   Elimina espacios, formatea datos

6️⃣ ALMACENAMIENTO
   ↓
   Guarda en CSV, JSON, SQLite, etc.
```

---

## 🏗️ HTML, CSS y DOM

### ¿Qué es HTML?

**HTML** (HyperText Markup Language) es el lenguaje de estructura de las páginas web.

**Ejemplo de HTML simple:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Productos - DataHub Store</title>
</head>
<body>
    <h1>Nuestros Productos</h1>

    <div class="producto" id="prod-001">
        <h2 class="titulo">Laptop Dell XPS 13</h2>
        <span class="precio">$1,299.99</span>
        <p class="descripcion">Ultrabook potente para profesionales</p>
        <span class="stock">En stock</span>
    </div>

    <div class="producto" id="prod-002">
        <h2 class="titulo">Mouse Logitech MX</h2>
        <span class="precio">$99.99</span>
        <p class="descripcion">Mouse ergonómico inalámbrico</p>
        <span class="stock">Agotado</span>
    </div>
</body>
</html>
```

### Anatomía de una Etiqueta HTML

```html
<div class="producto" id="prod-001">
  ↑     ↑               ↑
  |     |               └─ Atributo: id (único)
  |     └─ Atributo: class (puede repetirse)
  └─ Tag (etiqueta)
```

**Etiquetas comunes en scraping:**

| Etiqueta       | Uso Típico          | Ejemplo                                 |
| -------------- | ------------------- | --------------------------------------- |
| `<div>`        | Contenedor genérico | `<div class="card">`                    |
| `<span>`       | Contenedor inline   | `<span class="price">$99</span>`        |
| `<h1>`, `<h2>` | Títulos             | `<h1>Producto</h1>`                     |
| `<p>`          | Párrafos            | `<p>Descripción...</p>`                 |
| `<a>`          | Enlaces             | `<a href="/producto">Ver</a>`           |
| `<table>`      | Tablas              | `<table><tr><td>Dato</td></tr></table>` |
| `<ul>`, `<li>` | Listas              | `<ul><li>Item 1</li></ul>`              |

---

### ¿Qué es el DOM?

**DOM** (Document Object Model) es la representación en forma de **árbol** del HTML.

**Analogía:** El DOM es como un **árbol genealógico** de una familia.

```
html (abuelo)
├── head (tío)
│   └── title (primo)
└── body (padre)
    ├── h1 (hermano mayor)
    └── div.producto (tú)
        ├── h2.titulo (hijo 1)
        ├── span.precio (hijo 2)
        └── p.descripcion (hijo 3)
```

**Terminología:**
- **Padre** (parent): Elemento que contiene a otro
- **Hijo** (child): Elemento contenido dentro de otro
- **Hermano** (sibling): Elementos al mismo nivel
- **Descendiente** (descendant): Cualquier elemento anidado (hijo, nieto, etc.)

---

### ¿Qué es CSS?

**CSS** (Cascading Style Sheets) define cómo se ven los elementos HTML.

**Para scraping, lo importante son los SELECTORES CSS:**

```css
/* Selector por clase */
.producto { color: blue; }

/* Selector por ID */
#prod-001 { font-weight: bold; }

/* Selector por etiqueta */
h2 { font-size: 20px; }

/* Selector combinado */
div.producto span.precio { color: green; }
```

Usaremos estos selectores para **encontrar elementos** al hacer scraping.

---

## 🥣 BeautifulSoup: Parsing de HTML

### ¿Qué es BeautifulSoup?

**BeautifulSoup** es una biblioteca de Python para parsear HTML/XML y extraer datos.

**Analogía:** Es como tener un **GPS inteligente** para navegar por el HTML.

### Instalación

```bash
pip install beautifulsoup4 requests
```

### Ejemplo Básico

```python
from bs4 import BeautifulSoup
import requests

# 1. Descargar HTML
url = "https://ejemplo.com/productos"
response = requests.get(url)
html = response.text

# 2. Parsear con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# 3. Extraer datos
titulo = soup.find('h1').text
print(titulo)  # "Nuestros Productos"

# 4. Encontrar todos los productos
productos = soup.find_all('div', class_='producto')
for prod in productos:
    nombre = prod.find('h2', class_='titulo').text
    precio = prod.find('span', class_='precio').text
    print(f"{nombre}: {precio}")
```

### Métodos Principales de BeautifulSoup

| Método         | Descripción                                 | Ejemplo                                   |
| -------------- | ------------------------------------------- | ----------------------------------------- |
| `find()`       | Encuentra EL PRIMER elemento que coincida   | `soup.find('h1')`                         |
| `find_all()`   | Encuentra TODOS los elementos que coincidan | `soup.find_all('div', class_='producto')` |
| `select()`     | Usa selectores CSS                          | `soup.select('div.producto span.precio')` |
| `select_one()` | Primer elemento con selector CSS            | `soup.select_one('#prod-001')`            |
| `.text`        | Extrae el texto dentro del elemento         | `elemento.text`                           |
| `.get()`       | Extrae el valor de un atributo              | `enlace.get('href')`                      |

---

### Navegación en el DOM

```python
# Obtener el padre
producto = soup.find('div', class_='producto')
body = producto.parent

# Obtener hijos directos
hijos = list(producto.children)

# Obtener todos los descendientes
descendientes = list(producto.descendants)

# Obtener el siguiente hermano
siguiente = producto.next_sibling

# Obtener el hermano anterior
anterior = producto.previous_sibling
```

---

## 🔧 Selenium: Scraping Dinámico

### ¿Qué es Selenium?

**Selenium** es una herramienta para **automatizar navegadores web**. Simula un usuario real interactuando con la página.

### ¿Cuándo usar Selenium?

✅ **Usa Selenium cuando:**
- La página carga contenido con **JavaScript** (React, Vue, Angular)
- Necesitas **hacer clic** en botones o llenar formularios
- La página tiene **scroll infinito** o carga lazy
- Necesitas **esperar** a que aparezcan elementos

❌ **NO uses Selenium si:**
- El HTML estático ya tiene los datos (usa BeautifulSoup, es más rápido)
- La página tiene una API oculta que puedes usar

**Analogía:** BeautifulSoup es como **leer el periódico**, Selenium es como **ver un video interactivo**.

---

### Instalación de Selenium

```bash
pip install selenium

# Descargar ChromeDriver (o Firefox geckodriver)
# https://chromedriver.chromium.org/
```

### Ejemplo Básico con Selenium

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Inicializar el navegador
driver = webdriver.Chrome()

# 2. Abrir página
driver.get("https://ejemplo.com/productos")

# 3. Esperar a que cargue el contenido JavaScript
wait = WebDriverWait(driver, 10)
productos = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "producto"))
)

# 4. Extraer datos
for prod in productos:
    titulo = prod.find_element(By.CLASS_NAME, "titulo").text
    precio = prod.find_element(By.CLASS_NAME, "precio").text
    print(f"{titulo}: {precio}")

# 5. Cerrar navegador
driver.quit()
```

---

### Estrategias de Espera en Selenium

**Problema:** JavaScript tarda en cargar, ¡no puedes extraer lo que no ha aparecido!

| Tipo de Espera | Descripción                    | Cuándo Usar         |
| -------------- | ------------------------------ | ------------------- |
| **Implícita**  | Espera global automática       | Para todo el script |
| **Explícita**  | Espera a condición específica  | Elementos críticos  |
| `time.sleep()` | ❌ NO RECOMENDADO (tiempo fijo) | Solo para debugging |

**Ejemplo de espera explícita:**

```python
from selenium.webdriver.support import expected_conditions as EC

# Esperar hasta que aparezca un elemento
elemento = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "producto-123"))
)

# Esperar hasta que sea clickeable
boton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "cargar-mas"))
)
boton.click()
```

---

## 🤖 Robots.txt y Ética del Scraping

### ¿Qué es robots.txt?

**robots.txt** es un archivo en la raíz del sitio web que indica qué partes pueden ser scrapeadas.

**Ubicación:** `https://ejemplo.com/robots.txt`

**Ejemplo de robots.txt:**

```txt
User-agent: *
Disallow: /admin/
Disallow: /carrito/
Crawl-delay: 2

User-agent: Googlebot
Allow: /

User-agent: BadBot
Disallow: /
```

**Interpretación:**
- `User-agent: *` = Para todos los bots
- `Disallow: /admin/` = NO scrapees /admin/
- `Crawl-delay: 2` = Espera 2 segundos entre requests
- `Allow: /` = SÍ puedes scrapear todo

---

### ¿Cómo respetar robots.txt en Python?

```python
import urllib.robotparser

# 1. Parsear robots.txt
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://ejemplo.com/robots.txt")
rp.read()

# 2. Verificar si puedes scrapear una URL
url = "https://ejemplo.com/productos"
user_agent = "MiScraper/1.0"

if rp.can_fetch(user_agent, url):
    print("✅ Permitido scrapear")
    # Hacer scraping...
else:
    print("❌ No permitido por robots.txt")
```

---

### Ética del Scraping

**Regla de oro:** 🥇 **Trata los servidores ajenos como te gustaría que trataran el tuyo.**

✅ **Haz:**
- Respeta robots.txt
- Limita velocidad (rate limiting)
- Identifícate con User-Agent claro
- Scrapea en horarios de baja demanda
- Cachea respuestas para no repetir requests

❌ **NO hagas:**
- Ignorar robots.txt
- Hacer cientos de requests por segundo
- Scraping de datos personales sensibles
- Revender datos scrapeados sin permiso
- Sobrecargar servidores pequeños

**Analogía:** Es como visitar una tienda física:
- ✅ Está bien mirar productos y anotar precios
- ❌ NO está bien entrar a la bodega ni robar
- ✅ Está bien tomar fotos (si está permitido)
- ❌ NO está bien bloquear la entrada para otros clientes

---

## 🕵️ User-Agent y Headers

### ¿Qué es un User-Agent?

**User-Agent** es una cadena de texto que identifica quién está haciendo el request (navegador, bot, etc.).

**Ejemplo de User-Agent de Chrome:**

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

### ¿Por qué importa?

Muchos sitios **bloquean requests sin User-Agent** o con User-Agents de bots conocidos.

**Ejemplo de bloqueo:**

```python
import requests

# ❌ Request sin User-Agent (puede ser bloqueado)
response = requests.get("https://ejemplo.com")

# ✅ Request con User-Agent (se ve como navegador)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get("https://ejemplo.com", headers=headers)
```

---

### Headers Importantes para Scraping

| Header            | Descripción                  | Ejemplo                      |
| ----------------- | ---------------------------- | ---------------------------- |
| `User-Agent`      | Identifica el cliente        | `Mozilla/5.0 ...`            |
| `Accept`          | Tipos de contenido aceptados | `text/html,application/json` |
| `Accept-Language` | Idioma preferido             | `es-ES,es;q=0.9,en;q=0.8`    |
| `Referer`         | De dónde vienes              | `https://google.com`         |
| `Cookie`          | Cookies de sesión            | `session_id=abc123`          |

**Ejemplo completo de headers:**

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://google.com",
    "DNT": "1",  # Do Not Track
}

response = requests.get("https://ejemplo.com", headers=headers)
```

---

## 🎯 XPath y CSS Selectors

### ¿Qué son los Selectores?

**Selectores** son patrones para encontrar elementos específicos en el HTML.

**Analogía:** Son como **direcciones postales** para encontrar casas en una ciudad.

---

### CSS Selectors

**Sintaxis más común:**

| Selector                | Significado            | Ejemplo               |
| ----------------------- | ---------------------- | --------------------- |
| `.clase`                | Por clase              | `.producto`           |
| `#id`                   | Por ID                 | `#prod-001`           |
| `elemento`              | Por etiqueta           | `div`, `span`, `h2`   |
| `padre > hijo`          | Hijo directo           | `div > span`          |
| `ancestro descendiente` | Cualquier descendiente | `div span`            |
| `[atributo]`            | Con atributo           | `[href]`, `[data-id]` |
| `[atributo="valor"]`    | Atributo con valor     | `[href="/productos"]` |

**Ejemplos prácticos:**

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# Seleccionar por clase
productos = soup.select('.producto')

# Seleccionar por ID
prod_001 = soup.select_one('#prod-001')

# Selector combinado: dentro de div.producto, todos los span.precio
precios = soup.select('div.producto span.precio')

# Elementos con atributo href
enlaces = soup.select('a[href]')

# Enlaces que empiezan con /productos
enlaces_productos = soup.select('a[href^="/productos"]')
```

---

### XPath

**XPath** es un lenguaje para navegar por XML/HTML (más potente pero más complejo).

**Sintaxis básica:**

| Expresión     | Significado        | Ejemplo                    |
| ------------- | ------------------ | -------------------------- |
| `/`           | Desde raíz         | `/html/body/div`           |
| `//`          | Cualquier nivel    | `//div[@class="producto"]` |
| `@atributo`   | Atributo           | `//a/@href`                |
| `text()`      | Texto del elemento | `//h2/text()`              |
| `[condición]` | Filtro             | `//div[@class="producto"]` |

**Ejemplos prácticos con Selenium:**

```python
from selenium.webdriver.common.by import By

# Por XPath absoluto (frágil, no recomendado)
elemento = driver.find_element(By.XPATH, "/html/body/div[1]/h2")

# Por XPath con clase
productos = driver.find_elements(By.XPATH, "//div[@class='producto']")

# Texto que contiene
titulo = driver.find_element(By.XPATH, "//h2[contains(text(), 'Laptop')]")

# Por atributo
enlace = driver.find_element(By.XPATH, "//a[@href='/productos']")

# Combinado: precio dentro de producto con ID específico
precio = driver.find_element(
    By.XPATH,
    "//div[@id='prod-001']//span[@class='precio']"
)
```

---

### CSS vs XPath: ¿Cuál usar?

| Aspecto                     | CSS Selectors | XPath            |
| --------------------------- | ------------- | ---------------- |
| **Sintaxis**                | ✅ Más simple  | ❌ Más compleja   |
| **Velocidad**               | ✅ Más rápido  | ❌ Más lento      |
| **Poder**                   | ❌ Limitado    | ✅ Muy potente    |
| **Navegación hacia arriba** | ❌ No puede    | ✅ Puede (parent) |
| **Texto exacto**            | ❌ Difícil     | ✅ Fácil          |

**Recomendación:** Usa **CSS Selectors** por defecto, solo usa **XPath** cuando necesites:
- Navegar hacia arriba (parent)
- Buscar por texto exacto
- Lógica compleja (AND, OR)

---

## 💾 Almacenamiento de Datos Scrapeados

### Opciones de Almacenamiento

| Formato              | Pros                     | Contras                     | Cuándo Usar                 |
| -------------------- | ------------------------ | --------------------------- | --------------------------- |
| **CSV**              | Simple, Excel-compatible | No soporta anidación        | Datos tabulares simples     |
| **JSON**             | Flexible, anidado        | Menos eficiente para tablas | Datos jerárquicos           |
| **SQLite**           | Relacional, queries SQL  | Más complejo                | Datos estructurados grandes |
| **Pandas DataFrame** | Análisis fácil           | En memoria                  | Análisis inmediato          |

---

### Ejemplo: Guardar en CSV

```python
import csv
from bs4 import BeautifulSoup

# Scrapear datos
productos = []
for prod in soup.find_all('div', class_='producto'):
    productos.append({
        'nombre': prod.find('h2', class_='titulo').text.strip(),
        'precio': prod.find('span', class_='precio').text.strip(),
        'stock': prod.find('span', class_='stock').text.strip()
    })

# Guardar en CSV
with open('productos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['nombre', 'precio', 'stock'])
    writer.writeheader()
    writer.writerows(productos)
```

---

### Ejemplo: Guardar en JSON

```python
import json

# Scrapear datos (igual que antes)
productos = [...]  # Lista de diccionarios

# Guardar en JSON
with open('productos.json', 'w', encoding='utf-8') as f:
    json.dump(productos, f, indent=2, ensure_ascii=False)
```

---

### Ejemplo: Guardar en SQLite

```python
import sqlite3

# Crear base de datos
conn = sqlite3.connect('productos.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio TEXT,
        stock TEXT,
        fecha_scraping TEXT
    )
''')

# Insertar datos
from datetime import datetime

for prod in productos:
    cursor.execute('''
        INSERT INTO productos (nombre, precio, stock, fecha_scraping)
        VALUES (?, ?, ?, ?)
    ''', (
        prod['nombre'],
        prod['precio'],
        prod['stock'],
        datetime.now().isoformat()
    ))

conn.commit()
conn.close()
```

---

## ⚖️ Web Scraping vs APIs

### ¿Cuándo usar cada uno?

| Criterio                | API REST                | Web Scraping           |
| ----------------------- | ----------------------- | ---------------------- |
| **Disponibilidad**      | ✅ Existe API pública    | ❌ No hay API           |
| **Costo**               | ❌ A veces pago          | ✅ Gratis (si es legal) |
| **Velocidad**           | ✅ Rápido (JSON)         | ❌ Más lento (HTML)     |
| **Estabilidad**         | ✅ Estable (versionado)  | ❌ Cambia con UI        |
| **Legalidad**           | ✅ Siempre legal         | ⚠️ Depende (TOS)        |
| **Límites**             | ⚠️ Rate limits estrictos | ⚠️ Puedes ser bloqueado |
| **Datos estructurados** | ✅ JSON estructurado     | ❌ HTML no estructurado |

**Regla general:**
1. 🥇 **Primero busca una API**
2. 🥈 Si no hay API, revisa **términos de servicio**
3. 🥉 Si es legal y ético, **usa scraping**

---

### Ejemplo de Decisión

**Caso 1: Twitter**
- ✅ Tiene API oficial (Twitter API v2)
- ❌ Scraping viola términos de servicio
- **Decisión:** Usa la API (aunque sea de pago)

**Caso 2: E-commerce local sin API**
- ❌ No tiene API pública
- ✅ Robots.txt permite scraping
- ✅ Términos de servicio no lo prohíben
- **Decisión:** Scraping ético con rate limiting

**Caso 3: Sitio de noticias**
- ✅ Tiene RSS feed (como API simple)
- ⚠️ Scraping técnicamente posible pero innecesario
- **Decisión:** Usa RSS feed (más eficiente)

---

## ⚖️ Legalidad y Ética

### Marco Legal

**GDPR (Europa):**
- ❌ NO scrapees datos personales sin consentimiento
- ❌ NO almacenes datos de ciudadanos EU sin cumplir GDPR
- ✅ Datos públicos de empresas suelen estar OK

**CCPA (California):**
- ❌ NO vendas datos scrapeados de residentes de California
- ✅ Derecho a eliminar datos si te lo piden

**CFAA (EE.UU.):**
- ❌ "Acceso no autorizado a sistemas" puede incluir scraping agresivo
- ⚠️ Violar términos de servicio puede tener consecuencias legales

---

### Términos de Servicio (TOS)

**Ejemplo de TOS que prohíbe scraping:**

> "Está prohibido el uso de bots, scrapers o cualquier método automatizado para acceder a nuestro sitio sin permiso explícito."

**¿Qué hacer?**
1. Lee SIEMPRE los términos de servicio
2. Si prohíben scraping, **NO lo hagas** (o pide permiso)
3. Si no dicen nada, procede con **ética y rate limiting**

---

### Casos Legales Importantes

**hiQ Labs vs LinkedIn (2019):**
- LinkedIn bloqueó scraping de perfiles públicos
- Corte decidió: **Datos públicos pueden ser scrapeados**
- Pero LinkedIn puede actualizar TOS y bloquear

**Conclusion:** Legal ≠ Ético. Incluso si es legal, respeta los servidores.

---

## ❌ Errores Comunes

### 1. No Verificar robots.txt

```python
# ❌ MAL: Scrapear sin verificar
response = requests.get("https://ejemplo.com/admin")

# ✅ BIEN: Verificar primero
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://ejemplo.com/robots.txt")
rp.read()

if rp.can_fetch("MiBot/1.0", url):
    response = requests.get(url)
```

---

### 2. No Usar User-Agent

```python
# ❌ MAL: Sin User-Agent (alto riesgo de bloqueo)
response = requests.get(url)

# ✅ BIEN: Con User-Agent realista
headers = {"User-Agent": "Mozilla/5.0 ..."}
response = requests.get(url, headers=headers)
```

---

### 3. Hacer Requests Demasiado Rápido

```python
# ❌ MAL: Sin rate limiting (abusivo)
for url in urls:
    response = requests.get(url)

# ✅ BIEN: Con rate limiting
import time

for url in urls:
    response = requests.get(url)
    time.sleep(2)  # Espera 2 segundos entre requests
```

---

### 4. No Manejar Errores

```python
# ❌ MAL: Sin manejo de errores
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
titulo = soup.find('h1').text  # ¡Puede fallar!

# ✅ BIEN: Con manejo de errores
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    titulo_elem = soup.find('h1')
    titulo = titulo_elem.text.strip() if titulo_elem else "Sin título"

except requests.exceptions.RequestException as e:
    print(f"Error al hacer request: {e}")
except AttributeError:
    print("Elemento no encontrado en HTML")
```

---

### 5. Usar Selenium cuando BeautifulSoup es Suficiente

```python
# ❌ MAL: Selenium innecesario (lento)
driver = webdriver.Chrome()
driver.get(url)
titulo = driver.find_element(By.TAG_NAME, "h1").text

# ✅ BIEN: BeautifulSoup si HTML es estático
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
titulo = soup.find('h1').text
```

**Regla:** Usa Selenium solo si BeautifulSoup no funciona (JavaScript dinámico).

---

## ✅ Buenas Prácticas

### 1. Limita la Velocidad (Rate Limiting)

```python
import time

DELAY_SECONDS = 2  # 2 segundos entre requests

for url in urls:
    response = requests.get(url)
    # Procesar...
    time.sleep(DELAY_SECONDS)
```

---

### 2. Identifícate con User-Agent Claro

```python
headers = {
    "User-Agent": "MiProyectoAnalisis/1.0 (contacto@ejemplo.com)"
}
```

Si eres identificable, el administrador puede contactarte en vez de bloquearte.

---

### 3. Cachea Respuestas

```python
import requests_cache

# Cachear por 1 hora
requests_cache.install_cache('scraper_cache', expire_after=3600)

# Ahora requests usa caché automáticamente
response = requests.get(url)  # Primera vez: request real
response = requests.get(url)  # Segunda vez: desde caché
```

---

### 4. Usa Timeouts

```python
response = requests.get(url, timeout=10)  # Falla si tarda >10 segundos
```

---

### 5. Logging Completo

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Scraping URL: {url}")
logger.warning(f"Elemento no encontrado: {selector}")
logger.error(f"Error HTTP {response.status_code}: {url}")
```

---

### 6. Respeta Horarios de Baja Demanda

Scrapea en:
- ✅ Madrugada (2am - 6am hora local del servidor)
- ✅ Fines de semana (si es sitio B2B)
- ❌ Evita horas pico (12pm - 2pm, 6pm - 9pm)

---

## ✅ Checklist de Aprendizaje

Marca lo que ya dominas:

### Conceptos Fundamentales
- [ ] Entiendo qué es web scraping y cuándo usarlo
- [ ] Conozco la estructura básica de HTML (tags, clases, IDs)
- [ ] Comprendo el DOM como árbol de elementos
- [ ] Sé qué es el CSS y cómo funcionan los selectores

### BeautifulSoup
- [ ] Puedo parsear HTML con BeautifulSoup
- [ ] Uso `find()` y `find_all()` correctamente
- [ ] Domino `select()` con CSS selectors
- [ ] Extraigo texto con `.text` y atributos con `.get()`

### Selenium
- [ ] Entiendo cuándo usar Selenium vs BeautifulSoup
- [ ] Puedo inicializar un navegador con WebDriver
- [ ] Uso esperas explícitas con `WebDriverWait`
- [ ] Extraigo datos de páginas con JavaScript dinámico

### Ética y Legalidad
- [ ] Sé verificar y respetar robots.txt
- [ ] Configuro User-Agent apropiado
- [ ] Aplico rate limiting en mis scrapers
- [ ] Conozco las implicaciones legales (GDPR, TOS)

### Selectores
- [ ] Domino selectores CSS básicos (`.clase`, `#id`, `elemento`)
- [ ] Uso selectores combinados (`padre > hijo`)
- [ ] Conozco selectores de atributos (`[href]`)
- [ ] Puedo usar XPath cuando CSS no es suficiente

### Almacenamiento
- [ ] Puedo guardar datos en CSV
- [ ] Puedo guardar datos en JSON
- [ ] Puedo guardar datos en SQLite
- [ ] Sé elegir el formato según el caso

### Buenas Prácticas
- [ ] Manejo errores con try/except
- [ ] Uso timeouts en requests
- [ ] Implemento logging en mis scrapers
- [ ] Cacheo respuestas para evitar requests duplicados
- [ ] Conozco la diferencia entre scraping y uso de APIs

---

## 🎓 Conclusión

**Web scraping** es una herramienta poderosa pero que **requiere responsabilidad**:

✅ **Usa scraping cuando:**
- No hay API disponible
- Es legal y ético según TOS
- Respetas robots.txt y rate limiting

❌ **NO uses scraping si:**
- Existe una API pública
- Los términos de servicio lo prohíben
- Extraes datos personales sin consentimiento

**Recuerda:** El scraping es como conducir un coche: puedes llegar lejos, pero debes **respetar las reglas de tráfico** (robots.txt, rate limiting, ética) para evitar accidentes (bloqueos, problemas legales).

---

## 📚 Recursos Adicionales

**Documentación Oficial:**
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)

**Herramientas Útiles:**
- [SelectorGadget](https://selectorgadget.com/) - Encontrar selectores CSS
- [Scrapy](https://scrapy.org/) - Framework avanzado de scraping
- [Requests-HTML](https://requests.readthedocs.io/projects/requests-html/) - Alternativa a BeautifulSoup

**Lecturas Recomendadas:**
- "Web Scraping with Python" - Ryan Mitchell
- Robots Exclusion Protocol: [robotstxt.org](https://www.robotstxt.org/)

---

**¡Ahora estás listo para los ejemplos prácticos! 🚀**

📝 **Siguiente paso:** [02-EJEMPLOS.md](02-EJEMPLOS.md) - 5 ejemplos trabajados de scraping con BeautifulSoup y Selenium.

---

*Última actualización: 2025-10-23*
*Tema 2 - Módulo 4 - Master en Ingeniería de Datos*
