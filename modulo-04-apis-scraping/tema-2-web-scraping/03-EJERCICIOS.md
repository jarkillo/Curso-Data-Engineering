# 🏋️ Tema 2: Web Scraping - Ejercicios Prácticos

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📋 Índice

- [Introducción](#introducción)
- [Ejercicios Básicos (1-5)](#ejercicios-básicos-1-5)
- [Ejercicios Intermedios (6-10)](#ejercicios-intermedios-6-10)
- [Ejercicios Avanzados (11-15)](#ejercicios-avanzados-11-15)
- [Soluciones](#soluciones)
- [Autoevaluación](#autoevaluación)

---

## 🎯 Introducción

Este documento contiene **15 ejercicios progresivos** para dominar web scraping con BeautifulSoup y Selenium.

**Estructura:**
- 📗 **Básicos (1-5):** Extracción simple con BeautifulSoup
- 📙 **Intermedios (6-10):** Navegación, tablas y manejo de errores
- 📕 **Avanzados (11-15):** Selenium, scrapers completos y almacenamiento

**Tiempo estimado total:** 8-12 horas

---

## 📝 Instrucciones Generales

1. **Lee el contexto** empresarial de cada ejercicio
2. **Intenta resolverlo** sin mirar las pistas
3. **Si te atascas**, revisa las pistas progresivas
4. **Compara tu solución** con la oficial al final
5. **Marca como completado** en la checklist

---

## 📗 Ejercicios Básicos (1-5)

### Ejercicio 1: Extraer Títulos de `<h1>`, `<h2>`, `<h3>`

**⏱️ Duración:** 10-15 minutos
**📦 Nivel:** Básico
**🛠️ Herramienta:** BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere analizar la estructura de contenido de blogs competidores. Tu tarea es extraer todos los encabezados (h1, h2, h3) de una página.

#### 🎯 Objetivo

Dado el siguiente HTML, extrae:
- Todos los `<h1>`
- Todos los `<h2>`
- Todos los `<h3>`

Y muéstralos organizados por nivel.

#### 📄 HTML de Entrada

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog DataHub</title>
</head>
<body>
    <h1>Tendencias en Data Engineering 2025</h1>

    <h2>Introducción</h2>
    <p>El mundo de los datos evoluciona rápidamente...</p>

    <h2>Principales Tendencias</h2>

    <h3>1. Auge de Data Lakehouses</h3>
    <p>Los data lakehouses combinan lo mejor de...</p>

    <h3>2. IA Generativa en ETL</h3>
    <p>La inteligencia artificial está transformando...</p>

    <h2>Conclusiones</h2>
    <p>El futuro es prometedor para...</p>
</body>
</html>
```

#### 📤 Salida Esperada

```
H1 (1):
  - Tendencias en Data Engineering 2025

H2 (3):
  - Introducción
  - Principales Tendencias
  - Conclusiones

H3 (2):
  - 1. Auge de Data Lakehouses
  - 2. IA Generativa en ETL
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Cómo empezar</summary>

Usa `soup.find_all()` con el nombre de la etiqueta:
```python
h1_tags = soup.find_all('h1')
```
</details>

<details>
<summary>🟡 Pista 2: Extraer texto</summary>

Para cada tag, extrae el texto con `.text.strip()`:
```python
for tag in h1_tags:
    print(tag.text.strip())
```
</details>

<details>
<summary>🔴 Pista 3: Estructura completa</summary>

```python
from bs4 import BeautifulSoup

# Parsear HTML
soup = BeautifulSoup(html, 'html.parser')

# Extraer cada nivel
for nivel in ['h1', 'h2', 'h3']:
    tags = soup.find_all(nivel)
    print(f"{nivel.upper()} ({len(tags)}):")
    for tag in tags:
        print(f"  - {tag.text.strip()}")
    print()
```
</details>

---

### Ejercicio 2: Extraer Todos los Enlaces (`<a href>`)

**⏱️ Duración:** 10-15 minutos
**📦 Nivel:** Básico
**🛠️ Herramienta:** BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere mapear la estructura de navegación de un sitio web. Tu tarea es extraer todos los enlaces de una página.

#### 🎯 Objetivo

Extrae:
1. El **texto del enlace** (anchor text)
2. La **URL** (atributo href)
3. Distingue entre **enlaces internos** y **externos**

#### 📄 HTML de Entrada

```html
<!DOCTYPE html>
<html>
<head>
    <title>DataHub - Navegación</title>
</head>
<body>
    <nav>
        <a href="/inicio">Inicio</a>
        <a href="/servicios">Servicios</a>
        <a href="/blog">Blog</a>
        <a href="https://github.com/datahub">GitHub</a>
        <a href="https://twitter.com/datahub">Twitter</a>
        <a href="/contacto">Contacto</a>
    </nav>
</body>
</html>
```

#### 📤 Salida Esperada

```
📊 Total de enlaces: 6

🔗 Enlaces Internos (4):
  - Inicio → /inicio
  - Servicios → /servicios
  - Blog → /blog
  - Contacto → /contacto

🌐 Enlaces Externos (2):
  - GitHub → https://github.com/datahub
  - Twitter → https://twitter.com/datahub
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Extraer enlaces</summary>

```python
enlaces = soup.find_all('a')
for enlace in enlaces:
    texto = enlace.text.strip()
    url = enlace.get('href')
```
</details>

<details>
<summary>🟡 Pista 2: Diferenciar interno/externo</summary>

Un enlace es externo si empieza con `http://` o `https://`:
```python
if url.startswith('http'):
    # Externo
else:
    # Interno
```
</details>

---

### Ejercicio 3: Extraer Texto de Párrafos con Clase Específica

**⏱️ Duración:** 10-15 minutos
**📦 Nivel:** Básico
**🛠️ Herramienta:** BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere extraer solo los **resúmenes** de artículos (párrafos con clase `resumen`), ignorando el resto del contenido.

#### 🎯 Objetivo

Extrae solo los párrafos `<p>` que tienen la clase `resumen`.

#### 📄 HTML de Entrada

```html
<!DOCTYPE html>
<html>
<body>
    <article>
        <h1>Python para Data Engineering</h1>
        <p class="resumen">Python es el lenguaje más usado en Data Engineering...</p>
        <p>El ecosistema de Python incluye Pandas, Dask, PySpark...</p>
        <p class="resumen">Las principales ventajas son su simplicidad y ecosistema.</p>
    </article>

    <article>
        <h1>SQL vs NoSQL</h1>
        <p class="resumen">SQL es ideal para datos estructurados y relacionales...</p>
        <p>Las bases NoSQL como MongoDB ofrecen flexibilidad...</p>
    </article>
</body>
</html>
```

#### 📤 Salida Esperada

```
📄 Resúmenes encontrados: 3

1. Python es el lenguaje más usado en Data Engineering...
2. Las principales ventajas son su simplicidad y ecosistema.
3. SQL es ideal para datos estructurados y relacionales...
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Buscar por clase</summary>

```python
resumenes = soup.find_all('p', class_='resumen')
```
</details>

---

### Ejercicio 4: Validar que `robots.txt` Permite Scraping

**⏱️ Duración:** 15-20 minutos
**📦 Nivel:** Básico
**🛠️ Herramienta:** urllib.robotparser

#### 📝 Contexto

**DataHub Inc.** quiere verificar **antes de scrapear** si un sitio permite el scraping según su `robots.txt`.

#### 🎯 Objetivo

Crea una función que:
1. Lea `robots.txt` de un sitio
2. Verifique si una URL específica puede ser scrapeada
3. Devuelva `True` (permitido) o `False` (prohibido)

#### 🧪 URLs de Prueba

```python
sitio = "https://www.python.org"
url_prueba = "https://www.python.org/downloads/"
user_agent = "DataHubBot/1.0"
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Usar robotparser</summary>

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url(f"{sitio}/robots.txt")
rp.read()
```
</details>

<details>
<summary>🟡 Pista 2: Verificar permiso</summary>

```python
permitido = rp.can_fetch(user_agent, url_prueba)
```
</details>

---

### Ejercicio 5: Extraer Meta Tags (title, description)

**⏱️ Duración:** 15-20 minutos
**📦 Nivel:** Básico
**🛠️ Herramienta:** BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere extraer los **meta tags SEO** de páginas web para análisis de marketing.

#### 🎯 Objetivo

Extrae:
- `<title>` del `<head>`
- Meta description (`<meta name="description">`)
- Meta keywords (`<meta name="keywords">`)

#### 📄 HTML de Entrada

```html
<!DOCTYPE html>
<html>
<head>
    <title>DataHub Inc. - Data Engineering Services</title>
    <meta name="description" content="We provide cutting-edge data engineering solutions for enterprises.">
    <meta name="keywords" content="data engineering, ETL, data pipelines, big data">
    <meta charset="UTF-8">
</head>
<body>
    <h1>Welcome to DataHub</h1>
</body>
</html>
```

#### 📤 Salida Esperada

```
📄 Meta Tags Extraídos:

Title: DataHub Inc. - Data Engineering Services
Description: We provide cutting-edge data engineering solutions for enterprises.
Keywords: data engineering, ETL, data pipelines, big data
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Extraer title</summary>

```python
title = soup.find('title').text.strip()
```
</details>

<details>
<summary>🟡 Pista 2: Extraer meta tags</summary>

```python
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc:
    description = meta_desc.get('content')
```
</details>

---

## 📙 Ejercicios Intermedios (6-10)

### Ejercicio 6: Scraping de Tabla HTML a DataFrame de Pandas

**⏱️ Duración:** 20-25 minutos
**📦 Nivel:** Intermedio
**🛠️ Herramienta:** BeautifulSoup + Pandas

#### 📝 Contexto

**DataHub Inc.** necesita extraer una tabla de precios de acciones y convertirla a DataFrame de Pandas para análisis.

#### 🎯 Objetivo

1. Extrae la tabla HTML
2. Conviértela a DataFrame de Pandas
3. Calcula estadísticas básicas (precio promedio, máximo, mínimo)

#### 📄 HTML de Entrada

```html
<table id="stocks">
    <thead>
        <tr>
            <th>Empresa</th>
            <th>Símbolo</th>
            <th>Precio</th>
            <th>Cambio</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Apple</td>
            <td>AAPL</td>
            <td>$175.50</td>
            <td>+2.3%</td>
        </tr>
        <tr>
            <td>Microsoft</td>
            <td>MSFT</td>
            <td>$380.00</td>
            <td>+1.5%</td>
        </tr>
        <tr>
            <td>Google</td>
            <td>GOOGL</td>
            <td>$140.25</td>
            <td>-0.8%</td>
        </tr>
    </tbody>
</table>
```

#### 📤 Salida Esperada

```
📊 DataFrame creado:

  Empresa Símbolo  Precio Cambio
0   Apple    AAPL  175.50  +2.3%
1 Microsoft    MSFT  380.00  +1.5%
2  Google  GOOGL  140.25  -0.8%

📈 Estadísticas:
Precio promedio: $231.92
Precio máximo: $380.00 (Microsoft)
Precio mínimo: $140.25 (Google)
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Usar pd.read_html()</summary>

Pandas puede leer tablas HTML directamente:
```python
import pandas as pd
df = pd.read_html(html)[0]  # [0] porque devuelve lista de DFs
```
</details>

<details>
<summary>🟡 Pista 2: Limpiar precios</summary>

Convierte "$175.50" a float:
```python
df['Precio'] = df['Precio'].str.replace('$', '').astype(float)
```
</details>

---

### Ejercicio 7: Navegar Múltiples Páginas (Paginación)

**⏱️ Duración:** 25-30 minutos
**📦 Nivel:** Intermedio
**🛠️ Herramienta:** BeautifulSoup + requests

#### 📝 Contexto

**DataHub Inc.** quiere scrapear un blog que tiene paginación (página 1, 2, 3...). Tu tarea es scrapear **todas las páginas** automáticamente.

#### 🎯 Objetivo

1. Scrapea páginas 1, 2 y 3
2. Extrae los títulos de artículos de cada página
3. Guarda todos los títulos en una lista
4. Implementa rate limiting (1 segundo entre páginas)

#### 🌐 URLs Simuladas

```
https://ejemplo.com/blog?page=1
https://ejemplo.com/blog?page=2
https://ejemplo.com/blog?page=3
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Loop de páginas</summary>

```python
import time

for pagina in range(1, 4):  # Páginas 1, 2, 3
    url = f"https://ejemplo.com/blog?page={pagina}"
    response = requests.get(url)
    # ... scrapear ...
    time.sleep(1)  # Rate limiting
```
</details>

---

### Ejercicio 8: Extraer Datos de Cards de Productos

**⏱️ Duración:** 25-30 minutos
**📦 Nivel:** Intermedio
**🛠️ Herramienta:** BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere analizar un e-commerce con layout de "cards" de productos.

#### 🎯 Objetivo

Extrae de cada card:
- Nombre del producto
- Precio
- Rating (estrellas)
- Disponibilidad (En stock / Agotado)

#### 📄 HTML de Entrada

```html
<div class="productos-grid">
    <div class="producto-card">
        <img src="laptop1.jpg" alt="Dell XPS">
        <h3 class="nombre">Dell XPS 13</h3>
        <div class="rating">★★★★★</div>
        <span class="precio">$1,299</span>
        <span class="stock disponible">En stock</span>
    </div>

    <div class="producto-card">
        <img src="laptop2.jpg" alt="MacBook">
        <h3 class="nombre">MacBook Pro M3</h3>
        <div class="rating">★★★★☆</div>
        <span class="precio">$2,499</span>
        <span class="stock agotado">Agotado</span>
    </div>
</div>
```

#### 📤 Salida Esperada

```
📦 Producto 1:
   Nombre: Dell XPS 13
   Precio: $1,299
   Rating: 5 estrellas
   Stock: En stock

📦 Producto 2:
   Nombre: MacBook Pro M3
   Precio: $2,499
   Rating: 4 estrellas
   Stock: Agotado
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Encontrar cards</summary>

```python
cards = soup.find_all('div', class_='producto-card')
```
</details>

<details>
<summary>🟡 Pista 2: Contar estrellas</summary>

```python
rating_text = card.find('div', class_='rating').text
num_estrellas = rating_text.count('★')
```
</details>

---

### Ejercicio 9: Manejo de Errores 404 en Scraping

**⏱️ Duración:** 20-25 minutos
**📦 Nivel:** Intermedio
**🛠️ Herramienta:** requests + try/except

#### 📝 Contexto

**DataHub Inc.** scrapea múltiples URLs, pero algunas ya no existen (404). Tu tarea es manejar errores gracefully.

#### 🎯 Objetivo

Crea una función que:
1. Intente scrapear una URL
2. Si da 404, registre el error y continúe
3. Si da otro error, también lo registre
4. Devuelva lista de URLs exitosas y fallidas

#### 🧪 URLs de Prueba

```python
urls = [
    "https://httpbin.org/html",          # ✅ Exitosa
    "https://httpbin.org/status/404",    # ❌ 404
    "https://httpbin.org/status/500",    # ❌ 500
    "https://httpbin.org/delay/1",       # ✅ Exitosa
]
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Try/except</summary>

```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Lanza excepción si status != 200
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
```
</details>

---

### Ejercicio 10: Selenium - Scraping de Página con JavaScript

**⏱️ Duración:** 30-40 minutos
**📦 Nivel:** Intermedio
**🛠️ Herramienta:** Selenium

#### 📝 Contexto

**DataHub Inc.** necesita scrapear un sitio moderno (React/Vue) donde el contenido se carga con JavaScript. BeautifulSoup NO funciona.

#### 🎯 Objetivo

Usa Selenium para:
1. Abrir la página http://quotes.toscrape.com/js/
2. Esperar a que cargue el contenido
3. Extraer las primeras 5 quotes
4. Cerrar el navegador correctamente

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Esperar elementos</summary>

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
quotes = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
)
```
</details>

---

## 📕 Ejercicios Avanzados (11-15)

### Ejercicio 11: Scraper con Rate Limiting

**⏱️ Duración:** 30-40 minutos
**📦 Nivel:** Avanzado
**🛠️ Herramienta:** BeautifulSoup + time

#### 📝 Contexto

**DataHub Inc.** quiere scrapear 20 productos de una tienda, pero debe respetar un rate limit de **1 request cada 2 segundos**.

#### 🎯 Objetivo

Implementa un scraper que:
1. Scrapea 20 URLs de productos
2. Espera 2 segundos entre cada request
3. Muestra progreso (ej: "5/20 completados")
4. Calcula tiempo total estimado

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Progress bar simple</summary>

```python
for i, url in enumerate(urls, 1):
    # Scrapear...
    print(f"Progreso: {i}/{len(urls)} completados")
    time.sleep(2)
```
</details>

---

### Ejercicio 12: Scraper que Respeta `robots.txt` Automáticamente

**⏱️ Duración:** 35-45 minutos
**📦 Nivel:** Avanzado
**🛠️ Herramienta:** urllib.robotparser + BeautifulSoup

#### 📝 Contexto

**DataHub Inc.** quiere un scraper que **SIEMPRE** verifique `robots.txt` antes de scrapear una URL.

#### 🎯 Objetivo

Crea una clase `EthicalScraper` que:
1. Verifique `robots.txt` automáticamente
2. Solo scrapee URLs permitidas
3. Registre URLs prohibidas en un log
4. Respete `Crawl-delay` si existe

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Clase básica</summary>

```python
class EthicalScraper:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.robot_parsers = {}  # Cache de robots.txt

    def puede_scrapear(self, url):
        # Verificar robots.txt
        pass
```
</details>

---

### Ejercicio 13: Scraping de Sitio con Login (Selenium)

**⏱️ Duración:** 40-50 minutos
**📦 Nivel:** Avanzado
**🛠️ Herramienta:** Selenium

#### 📝 Contexto

**DataHub Inc.** necesita scrapear datos de un portal interno que requiere login.

#### 🎯 Objetivo

Usa Selenium para:
1. Abrir página de login
2. Llenar formulario (usuario y contraseña)
3. Hacer clic en "Login"
4. Esperar a que cargue el dashboard
5. Scrapear datos del dashboard

#### 🌐 Sitio de Práctica

Usa: https://the-internet.herokuapp.com/login
- Usuario: `tomsmith`
- Password: `SuperSecretPassword!`

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Llenar formulario</summary>

```python
# Encontrar campos
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

# Llenar
username_field.send_keys("tomsmith")
password_field.send_keys("SuperSecretPassword!")

# Submit
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()
```
</details>

---

### Ejercicio 14: Pipeline Completo - Scrape → Limpieza → SQLite

**⏱️ Duración:** 50-60 minutos
**📦 Nivel:** Avanzado
**🛠️ Herramienta:** BeautifulSoup + SQLite + Logging

#### 📝 Contexto

**DataHub Inc.** quiere un pipeline completo de scraping con almacenamiento en base de datos.

#### 🎯 Objetivo

Crea un pipeline que:
1. **Scrapea** productos de una página
2. **Limpia** datos (precios a float, elimina espacios)
3. **Valida** datos (precio > 0, nombre no vacío)
4. **Almacena** en SQLite con timestamp
5. **Registra** todo en un log file

#### 📊 Estructura de la Tabla

```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    fecha_scraping TEXT NOT NULL,
    UNIQUE(nombre, fecha_scraping)
);
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Logging setup</summary>

```python
import logging

logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Scraping iniciado...")
```
</details>

---

### Ejercicio 15: Comparar Datos Scrapeados con API (Validación)

**⏱️ Duración:** 60+ minutos
**📦 Nivel:** Avanzado
**🛠️ Herramienta:** BeautifulSoup + requests + Pandas

#### 📝 Contexto

**DataHub Inc.** quiere validar si los datos scrapeados coinciden con los de una API. Si hay diferencias, reportarlas.

#### 🎯 Objetivo

1. Scrapea precios de productos de una página HTML
2. Obtén los mismos precios de una API
3. Compara ambos datasets
4. Reporta discrepancias (ej: precio en web ≠ precio en API)

#### 🌐 URLs de Prueba

- Web: https://fakestoreapi.com/ (scrapear HTML simulado)
- API: https://fakestoreapi.com/products

#### 📤 Salida Esperada

```
🔍 COMPARACIÓN WEB vs API

✅ Coincidencias: 8/10 productos
❌ Discrepancias: 2 productos

🚨 Producto con diferencia:
   Nombre: Fjallraven Backpack
   Precio Web: $109.95
   Precio API: $110.00
   Diferencia: $0.05

🚨 Producto con diferencia:
   Nombre: Mens Casual Premium Slim Fit T-Shirts
   Precio Web: $22.30
   Precio API: $22.00
   Diferencia: -$0.30
```

#### 💡 Pistas

<details>
<summary>🟢 Pista 1: Comparar DataFrames</summary>

```python
import pandas as pd

# Crear DataFrames
df_web = pd.DataFrame(productos_web)
df_api = pd.DataFrame(productos_api)

# Merge para comparar
df_merged = df_web.merge(df_api, on='nombre', suffixes=('_web', '_api'))

# Encontrar diferencias
df_merged['diferencia'] = df_merged['precio_web'] - df_merged['precio_api']
discrepancias = df_merged[df_merged['diferencia'] != 0]
```
</details>

---

## ✅ Soluciones

### Solución Ejercicio 1: Extraer Títulos

<details>
<summary>Ver solución completa</summary>

```python
from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Blog DataHub</title>
</head>
<body>
    <h1>Tendencias en Data Engineering 2025</h1>

    <h2>Introducción</h2>
    <p>El mundo de los datos evoluciona rápidamente...</p>

    <h2>Principales Tendencias</h2>

    <h3>1. Auge de Data Lakehouses</h3>
    <p>Los data lakehouses combinan lo mejor de...</p>

    <h3>2. IA Generativa en ETL</h3>
    <p>La inteligencia artificial está transformando...</p>

    <h2>Conclusiones</h2>
    <p>El futuro es prometedor para...</p>
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Extraer cada nivel
for nivel in ['h1', 'h2', 'h3']:
    tags = soup.find_all(nivel)
    print(f"{nivel.upper()} ({len(tags)}):")
    for tag in tags:
        print(f"  - {tag.text.strip()}")
    print()
```

</details>

---

### Solución Ejercicio 2: Extraer Enlaces

<details>
<summary>Ver solución completa</summary>

```python
from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html>
<head>
    <title>DataHub - Navegación</title>
</head>
<body>
    <nav>
        <a href="/inicio">Inicio</a>
        <a href="/servicios">Servicios</a>
        <a href="/blog">Blog</a>
        <a href="https://github.com/datahub">GitHub</a>
        <a href="https://twitter.com/datahub">Twitter</a>
        <a href="/contacto">Contacto</a>
    </nav>
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Encontrar todos los enlaces
enlaces = soup.find_all('a')

# Separar internos y externos
internos = []
externos = []

for enlace in enlaces:
    texto = enlace.text.strip()
    url = enlace.get('href')

    if url.startswith('http'):
        externos.append((texto, url))
    else:
        internos.append((texto, url))

# Mostrar resultados
print(f"📊 Total de enlaces: {len(enlaces)}\n")

print(f"🔗 Enlaces Internos ({len(internos)}):")
for texto, url in internos:
    print(f"  - {texto} → {url}")

print(f"\n🌐 Enlaces Externos ({len(externos)}):")
for texto, url in externos:
    print(f"  - {texto} → {url}")
```

</details>

---

### Solución Ejercicio 4: Validar robots.txt

<details>
<summary>Ver solución completa</summary>

```python
import urllib.robotparser

def puede_scrapear(sitio, url, user_agent):
    """
    Verifica si una URL puede ser scrapeada según robots.txt

    Args:
        sitio: URL base del sitio (ej: "https://www.python.org")
        url: URL específica a verificar
        user_agent: Identificador del bot

    Returns:
        bool: True si está permitido, False si no
    """
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{sitio}/robots.txt")
        rp.read()

        permitido = rp.can_fetch(user_agent, url)

        if permitido:
            print(f"✅ PERMITIDO scrapear: {url}")
        else:
            print(f"❌ PROHIBIDO scrapear: {url}")

        return permitido

    except Exception as e:
        print(f"⚠️ Error al leer robots.txt: {e}")
        return False


# PRUEBAS
sitio = "https://www.python.org"
user_agent = "DataHubBot/1.0"

urls_prueba = [
    "https://www.python.org/downloads/",
    "https://www.python.org/about/",
    "https://www.python.org/psf/",
]

print("🤖 VALIDADOR DE ROBOTS.TXT\n")
for url in urls_prueba:
    puede_scrapear(sitio, url, user_agent)
    print()
```

</details>

---

### Solución Ejercicio 6: Tabla a DataFrame

<details>
<summary>Ver solución completa</summary>

```python
from bs4 import BeautifulSoup
import pandas as pd

html = """
<table id="stocks">
    <thead>
        <tr>
            <th>Empresa</th>
            <th>Símbolo</th>
            <th>Precio</th>
            <th>Cambio</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Apple</td>
            <td>AAPL</td>
            <td>$175.50</td>
            <td>+2.3%</td>
        </tr>
        <tr>
            <td>Microsoft</td>
            <td>MSFT</td>
            <td>$380.00</td>
            <td>+1.5%</td>
        </tr>
        <tr>
            <td>Google</td>
            <td>GOOGL</td>
            <td>$140.25</td>
            <td>-0.8%</td>
        </tr>
    </tbody>
</table>
"""

# Método 1: Pandas (más fácil)
df = pd.read_html(html)[0]

# Limpiar columna Precio
df['Precio_Limpio'] = df['Precio'].str.replace('$', '').astype(float)

print("📊 DataFrame creado:")
print(df[['Empresa', 'Símbolo', 'Precio_Limpio', 'Cambio']])

# Estadísticas
print("\n📈 Estadísticas:")
print(f"Precio promedio: ${df['Precio_Limpio'].mean():.2f}")
print(f"Precio máximo: ${df['Precio_Limpio'].max():.2f} ({df.loc[df['Precio_Limpio'].idxmax(), 'Empresa']})")
print(f"Precio mínimo: ${df['Precio_Limpio'].min():.2f} ({df.loc[df['Precio_Limpio'].idxmin(), 'Empresa']})")
```

</details>

---

### Solución Ejercicio 10: Selenium

<details>
<summary>Ver solución completa</summary>

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapear_quotes_selenium():
    """
    Scrapea quotes de http://quotes.toscrape.com/js/ usando Selenium
    """
    driver = webdriver.Chrome()

    try:
        # Abrir página
        url = "http://quotes.toscrape.com/js/"
        print(f"🌐 Abriendo: {url}")
        driver.get(url)

        # Esperar a que cargue
        wait = WebDriverWait(driver, 10)
        quotes = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
        )

        print(f"✅ Encontradas {len(quotes)} quotes\n")

        # Extraer datos
        datos = []
        for i, quote_elem in enumerate(quotes[:5], 1):  # Solo primeras 5
            texto = quote_elem.find_element(By.CLASS_NAME, "text").text
            autor = quote_elem.find_element(By.CLASS_NAME, "author").text

            print(f"📝 Quote {i}:")
            print(f"   \"{texto}\"")
            print(f"   - {autor}\n")

            datos.append({'texto': texto, 'autor': autor})

        return datos

    finally:
        driver.quit()


# Ejecutar
scrapear_quotes_selenium()
```

</details>

---

### Solución Ejercicio 14: Pipeline Completo

<details>
<summary>Ver solución completa</summary>

```python
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='scraper_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScraperPipeline:
    """Pipeline completo: Scrape → Limpieza → Validación → SQLite"""

    def __init__(self, db_name='productos.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        """Crear tabla si no existe"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                fecha_scraping TEXT NOT NULL,
                UNIQUE(nombre, fecha_scraping)
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("Base de datos configurada")

    def scrapear(self, html):
        """Paso 1: Scrapear HTML"""
        logger.info("Iniciando scraping...")
        soup = BeautifulSoup(html, 'html.parser')

        productos = []
        for prod in soup.find_all('div', class_='producto'):
            nombre = prod.find('h2', class_='nombre').text.strip()
            precio = prod.find('span', class_='precio').text.strip()
            stock = prod.find('span', class_='stock').text.strip()

            productos.append({
                'nombre': nombre,
                'precio': precio,
                'stock': stock
            })

        logger.info(f"Scrapeados {len(productos)} productos")
        return productos

    def limpiar(self, productos):
        """Paso 2: Limpiar datos"""
        logger.info("Limpiando datos...")

        for prod in productos:
            # Limpiar precio
            prod['precio'] = float(
                prod['precio'].replace('$', '').replace(',', '')
            )

            # Limpiar stock
            try:
                prod['stock'] = int(prod['stock'])
            except ValueError:
                prod['stock'] = 0

        return productos

    def validar(self, productos):
        """Paso 3: Validar datos"""
        logger.info("Validando datos...")
        validos = []

        for prod in productos:
            if prod['nombre'] and prod['precio'] > 0:
                validos.append(prod)
            else:
                logger.warning(f"Producto inválido rechazado: {prod}")

        logger.info(f"Productos válidos: {len(validos)}/{len(productos)}")
        return validos

    def guardar(self, productos):
        """Paso 4: Guardar en SQLite"""
        logger.info("Guardando en base de datos...")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        fecha = datetime.now().isoformat()
        guardados = 0

        for prod in productos:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO productos
                    (nombre, precio, stock, fecha_scraping)
                    VALUES (?, ?, ?, ?)
                ''', (prod['nombre'], prod['precio'], prod['stock'], fecha))

                if cursor.rowcount > 0:
                    guardados += 1

            except sqlite3.Error as e:
                logger.error(f"Error al guardar {prod['nombre']}: {e}")

        conn.commit()
        conn.close()

        logger.info(f"Guardados {guardados} productos")
        return guardados

    def ejecutar(self, html):
        """Ejecutar pipeline completo"""
        print("🚀 INICIANDO PIPELINE DE SCRAPING\n")

        # 1. Scrapear
        productos = self.scrapear(html)
        print(f"✅ Scraping: {len(productos)} productos\n")

        # 2. Limpiar
        productos = self.limpiar(productos)
        print(f"✅ Limpieza: Completada\n")

        # 3. Validar
        productos = self.validar(productos)
        print(f"✅ Validación: {len(productos)} válidos\n")

        # 4. Guardar
        guardados = self.guardar(productos)
        print(f"✅ Almacenamiento: {guardados} guardados en DB\n")

        print("🎉 PIPELINE COMPLETADO")


# HTML de ejemplo
html_ejemplo = """
<html>
<body>
    <div class="producto">
        <h2 class="nombre">Laptop Dell XPS</h2>
        <span class="precio">$1,299.99</span>
        <span class="stock">15</span>
    </div>
    <div class="producto">
        <h2 class="nombre">MacBook Pro M3</h2>
        <span class="precio">$2,499.00</span>
        <span class="stock">8</span>
    </div>
</body>
</html>
"""

# Ejecutar
pipeline = ScraperPipeline('productos_pipeline.db')
pipeline.ejecutar(html_ejemplo)
```

</details>

---

## 📊 Autoevaluación

Marca los ejercicios completados:

### Básicos
- [ ] Ejercicio 1: Extraer títulos h1, h2, h3
- [ ] Ejercicio 2: Extraer todos los enlaces
- [ ] Ejercicio 3: Extraer párrafos con clase específica
- [ ] Ejercicio 4: Validar robots.txt
- [ ] Ejercicio 5: Extraer meta tags

### Intermedios
- [ ] Ejercicio 6: Tabla HTML a DataFrame
- [ ] Ejercicio 7: Navegar múltiples páginas
- [ ] Ejercicio 8: Extraer datos de cards
- [ ] Ejercicio 9: Manejo de errores 404
- [ ] Ejercicio 10: Selenium con JavaScript

### Avanzados
- [ ] Ejercicio 11: Scraper con rate limiting
- [ ] Ejercicio 12: Scraper que respeta robots.txt
- [ ] Ejercicio 13: Scraping con login (Selenium)
- [ ] Ejercicio 14: Pipeline completo con SQLite
- [ ] Ejercicio 15: Comparar scraping vs API

---

## 🎓 Resumen de Conceptos Clave

| Concepto                    | Ejercicios |
| --------------------------- | ---------- |
| **BeautifulSoup básico**    | 1, 2, 3    |
| **Validación ética**        | 4          |
| **Meta tags**               | 5          |
| **Pandas integration**      | 6          |
| **Paginación**              | 7          |
| **CSS Selectors avanzados** | 8          |
| **Manejo de errores**       | 9          |
| **Selenium**                | 10, 13     |
| **Rate limiting**           | 11         |
| **Scraping ético**          | 12         |
| **Pipeline completo**       | 14         |
| **Validación de datos**     | 15         |

---

## 🎯 Siguiente Paso

¡Felicidades! 🎉 Has completado los ejercicios de web scraping.

**Próximo paso:** Proyecto Práctico - Scraper completo con TDD en `04-proyecto-practico/`.

---

*Última actualización: 2025-10-23*
*Tema 2 - Módulo 4 - Master en Ingeniería de Datos*
