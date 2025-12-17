# 💻 Tema 2: Web Scraping - Ejemplos Prácticos

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📋 Índice de Ejemplos

1. [Ejemplo 1: Scraping Básico con BeautifulSoup](#ejemplo-1-scraping-básico-con-beautifulsoup) 📗
2. [Ejemplo 2: Extraer Tabla de Datos](#ejemplo-2-extraer-tabla-de-datos) 📗
3. [Ejemplo 3: Scraping con Navegación](#ejemplo-3-scraping-con-navegación) 📙
4. [Ejemplo 4: Scraping Dinámico con Selenium](#ejemplo-4-scraping-dinámico-con-selenium) 📙
5. [Ejemplo 5: Scraper Masivo con Almacenamiento](#ejemplo-5-scraper-masivo-con-almacenamiento) 📕

**Leyenda:**
- 📗 **Básico** - Conceptos fundamentales (15-20 min)
- 📙 **Intermedio** - Integración de conceptos (25-35 min)
- 📕 **Avanzado** - Soluciones completas (40-60 min)

---

## 🎯 Objetivos de este Documento

Al completar estos ejemplos, habrás:

✅ Scrapeado páginas HTML estáticas con BeautifulSoup
✅ Extraído datos de tablas HTML a CSV
✅ Navegado múltiples páginas para scraping masivo
✅ Usado Selenium para páginas con JavaScript
✅ Creado un scraper completo con almacenamiento en SQLite

---

## 📗 Ejemplo 1: Scraping Básico con BeautifulSoup

### 🎯 Objetivo

Extraer **títulos de noticias** de una página HTML estática.

### 📝 Contexto Empresarial

**DataHub Inc.** necesita analizar las noticias del sector tech para detectar tendencias. Tu tarea es scrapear los titulares de un blog de tecnología.

---

### 🌐 HTML de Ejemplo

Para este ejemplo, usaremos este HTML simulado (guardado como `noticias_ejemplo.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog de Tecnología - DataHub Inc.</title>
</head>
<body>
    <header>
        <h1>Últimas Noticias de Tech</h1>
    </header>

    <main>
        <article class="noticia" data-id="1">
            <h2 class="titulo">Python 3.12 mejora el rendimiento en un 25%</h2>
            <p class="autor">Por Ana García</p>
            <time class="fecha">2025-10-20</time>
            <p class="resumen">
                La nueva versión de Python incluye optimizaciones significativas...
            </p>
        </article>

        <article class="noticia" data-id="2">
            <h2 class="titulo">AWS lanza nuevo servicio de IA Generativa</h2>
            <p class="autor">Por Carlos Méndez</p>
            <time class="fecha">2025-10-19</time>
            <p class="resumen">
                Amazon Web Services presenta Bedrock Studio para desarrolladores...
            </p>
        </article>

        <article class="noticia" data-id="3">
            <h2 class="titulo">ChatGPT alcanza 200 millones de usuarios activos</h2>
            <p class="autor">Por María López</p>
            <time class="fecha">2025-10-18</time>
            <p class="resumen">
                OpenAI anuncia que su modelo supera las expectativas de adopción...
            </p>
        </article>
    </main>
</body>
</html>
```

---

### 💻 Código Python Completo

```python
from bs4 import BeautifulSoup

# 1️⃣ LEER EL ARCHIVO HTML
with open('noticias_ejemplo.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2️⃣ PARSEAR CON BEAUTIFULSOUP
soup = BeautifulSoup(html, 'html.parser')

# 3️⃣ EXTRAER TODAS LAS NOTICIAS
noticias = soup.find_all('article', class_='noticia')

print(f"📰 Encontradas {len(noticias)} noticias\n")

# 4️⃣ ITERAR Y EXTRAER DATOS
for i, noticia in enumerate(noticias, 1):
    # Extraer elementos individuales
    titulo = noticia.find('h2', class_='titulo').text.strip()
    autor = noticia.find('p', class_='autor').text.strip()
    fecha = noticia.find('time', class_='fecha').text.strip()
    resumen = noticia.find('p', class_='resumen').text.strip()

    # Extraer atributo data-id
    data_id = noticia.get('data-id')

    # Mostrar resultados
    print(f"📌 Noticia {i} (ID: {data_id})")
    print(f"   Título: {titulo}")
    print(f"   Autor: {autor}")
    print(f"   Fecha: {fecha}")
    print(f"   Resumen: {resumen[:50]}...")
    print()
```

---

### 📤 Salida Esperada

```
📰 Encontradas 3 noticias

📌 Noticia 1 (ID: 1)
   Título: Python 3.12 mejora el rendimiento en un 25%
   Autor: Por Ana García
   Fecha: 2025-10-20
   Resumen: La nueva versión de Python incluye optimizaci...

📌 Noticia 2 (ID: 2)
   Título: AWS lanza nuevo servicio de IA Generativa
   Autor: Por Carlos Méndez
   Fecha: 2025-10-19
   Resumen: Amazon Web Services presenta Bedrock Studio p...

📌 Noticia 3 (ID: 3)
   Título: ChatGPT alcanza 200 millones de usuarios activos
   Autor: Por María López
   Fecha: 2025-10-18
   Resumen: OpenAI anuncia que su modelo supera las expec...
```

---

### 🎓 Conceptos Clave

| Concepto     | Explicación                                     |
| ------------ | ----------------------------------------------- |
| `find_all()` | Encuentra **todos** los elementos que coincidan |
| `.text`      | Extrae el **texto** dentro del elemento         |
| `.strip()`   | Elimina **espacios** al inicio y final          |
| `.get()`     | Extrae el **valor de un atributo** HTML         |

**Tip:** Usa `.text.strip()` siempre para limpiar espacios innecesarios.

---

## 📗 Ejemplo 2: Extraer Tabla de Datos

### 🎯 Objetivo

Scrapear una **tabla HTML de productos** y convertirla a **CSV**.

### 📝 Contexto Empresarial

**DataHub Inc.** necesita analizar la competencia. Tu tarea es extraer la tabla de productos de un e-commerce y guardarla en CSV para análisis con Excel.

---

### 🌐 HTML de Ejemplo

```html
<!DOCTYPE html>
<html>
<head>
    <title>Productos - E-Commerce</title>
</head>
<body>
    <h1>Catálogo de Laptops</h1>

    <table id="productos">
        <thead>
            <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Rating</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>001</td>
                <td>Dell XPS 13</td>
                <td>$1,299</td>
                <td>15</td>
                <td>4.8</td>
            </tr>
            <tr>
                <td>002</td>
                <td>MacBook Pro M3</td>
                <td>$2,499</td>
                <td>8</td>
                <td>4.9</td>
            </tr>
            <tr>
                <td>003</td>
                <td>Lenovo ThinkPad X1</td>
                <td>$1,799</td>
                <td>12</td>
                <td>4.7</td>
            </tr>
            <tr>
                <td>004</td>
                <td>HP Spectre x360</td>
                <td>$1,599</td>
                <td>0</td>
                <td>4.6</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

---

### 💻 Código Python Completo

```python
from bs4 import BeautifulSoup
import csv

# 1️⃣ LEER HTML
with open('productos_tabla.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2️⃣ PARSEAR
soup = BeautifulSoup(html, 'html.parser')

# 3️⃣ ENCONTRAR LA TABLA
tabla = soup.find('table', id='productos')

# 4️⃣ EXTRAER ENCABEZADOS
encabezados = []
for th in tabla.find('thead').find_all('th'):
    encabezados.append(th.text.strip())

print(f"📊 Encabezados: {encabezados}\n")

# 5️⃣ EXTRAER FILAS
productos = []
tbody = tabla.find('tbody')

for tr in tbody.find_all('tr'):
    fila = []
    for td in tr.find_all('td'):
        fila.append(td.text.strip())
    productos.append(fila)

print(f"✅ Extraídos {len(productos)} productos\n")

# 6️⃣ MOSTRAR PRIMEROS 3
for i, producto in enumerate(productos[:3], 1):
    print(f"📦 Producto {i}: {producto}")

# 7️⃣ GUARDAR EN CSV
with open('productos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(encabezados)  # Header
    writer.writerows(productos)   # Datos

print("\n💾 Datos guardados en 'productos.csv'")
```

---

### 📤 Salida Esperada

```
📊 Encabezados: ['ID', 'Producto', 'Precio', 'Stock', 'Rating']

✅ Extraídos 4 productos

📦 Producto 1: ['001', 'Dell XPS 13', '$1,299', '15', '4.8']
📦 Producto 2: ['002', 'MacBook Pro M3', '$2,499', '8', '4.9']
📦 Producto 3: ['003', 'Lenovo ThinkPad X1', '$1,799', '12', '4.7']

💾 Datos guardados en 'productos.csv'
```

---

### 📄 Contenido de `productos.csv`

```csv
ID,Producto,Precio,Stock,Rating
001,Dell XPS 13,$1,299,15,4.8
002,MacBook Pro M3,$2,499,8,4.9
003,Lenovo ThinkPad X1,$1,799,12,4.7
004,HP Spectre x360,$1,599,0,4.6
```

---

### 🎓 Conceptos Clave

| Concepto         | Explicación                                 |
| ---------------- | ------------------------------------------- |
| `find('table')`  | Encuentra la **tabla** HTML                 |
| `find_all('tr')` | Encuentra todas las **filas** (table row)   |
| `find_all('td')` | Encuentra todas las **celdas** (table data) |
| `csv.writer()`   | Escribe datos en formato **CSV**            |

**Tip:** Las tablas HTML tienen estructura predecible: `<table>` → `<thead>` / `<tbody>` → `<tr>` → `<th>` / `<td>`.

---

## 📙 Ejemplo 3: Scraping con Navegación

### 🎯 Objetivo

Scrapear **múltiples páginas** de un sitio web siguiendo enlaces.

### 📝 Contexto Empresarial

**DataHub Inc.** quiere analizar las publicaciones de su blog. El blog tiene 3 páginas de artículos. Tu tarea es scrapear **todas las páginas** automáticamente.

---

### 🌐 Estructura del Sitio

```
https://ejemplo.com/blog?page=1  ← 3 artículos
https://ejemplo.com/blog?page=2  ← 3 artículos
https://ejemplo.com/blog?page=3  ← 2 artículos

Total: 8 artículos
```

---

### 💻 Código Python Completo

```python
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

# Usaremos JSONPlaceholder como API de prueba
# pero simularemos scraping con paginación

def scrapear_pagina(numero_pagina):
    """
    Simula scraping de una página específica.
    En la realidad, harías requests a URLs diferentes.
    """
    print(f"\n🔍 Scraping página {numero_pagina}...")

    # Simular paginación: obtener posts del 1-3, 4-6, 7-9
    inicio = (numero_pagina - 1) * 3 + 1
    fin = inicio + 2

    articulos = []
    for post_id in range(inicio, fin + 1):
        url = f"{BASE_URL}/{post_id}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            articulo = {
                'id': data['id'],
                'titulo': data['title'],
                'cuerpo': data['body'][:50] + '...'  # Primeros 50 chars
            }

            articulos.append(articulo)
            print(f"   ✅ Artículo {post_id}: {articulo['titulo'][:40]}...")

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error en artículo {post_id}: {e}")

    # ⚠️ RATE LIMITING: Esperar entre páginas
    time.sleep(1)  # 1 segundo entre páginas

    return articulos


# 🚀 SCRAPING DE MÚLTIPLES PÁGINAS
print("=" * 60)
print("📰 SCRAPER MULTI-PÁGINA - DataHub Inc.")
print("=" * 60)

total_articulos = []
NUM_PAGINAS = 3

for pagina in range(1, NUM_PAGINAS + 1):
    articulos_pagina = scrapear_pagina(pagina)
    total_articulos.extend(articulos_pagina)

# 📊 RESUMEN
print("\n" + "=" * 60)
print(f"✅ SCRAPING COMPLETADO")
print(f"📊 Total de páginas scrapeadas: {NUM_PAGINAS}")
print(f"📄 Total de artículos extraídos: {len(total_articulos)}")
print("=" * 60)

# Mostrar primeros 3 artículos
print("\n📋 Primeros 3 artículos:")
for i, art in enumerate(total_articulos[:3], 1):
    print(f"\n{i}. {art['titulo']}")
    print(f"   ID: {art['id']}")
    print(f"   Extracto: {art['cuerpo']}")

# 💾 GUARDAR EN JSON
import json

with open('articulos_scrapeados.json', 'w', encoding='utf-8') as f:
    json.dump(total_articulos, f, indent=2, ensure_ascii=False)

print("\n💾 Datos guardados en 'articulos_scrapeados.json'")
```

---

### 📤 Salida Esperada

```
============================================================
📰 SCRAPER MULTI-PÁGINA - DataHub Inc.
============================================================

🔍 Scraping página 1...
   ✅ Artículo 1: sunt aut facere repellat provident occ...
   ✅ Artículo 2: qui est esse...
   ✅ Artículo 3: ea molestias quasi exercitationem rep...

🔍 Scraping página 2...
   ✅ Artículo 4: eum et est occaecati...
   ✅ Artículo 5: nesciunt quas odio...
   ✅ Artículo 6: dolorem eum magni eos aperiam quia...

🔍 Scraping página 3...
   ✅ Artículo 7: magnam facilis autem...
   ✅ Artículo 8: dolorem dolore est ipsam...
   ✅ Artículo 9: nesciunt iure omnis dolorem tempora...

============================================================
✅ SCRAPING COMPLETADO
📊 Total de páginas scrapeadas: 3
📄 Total de artículos extraídos: 9
============================================================

📋 Primeros 3 artículos:

1. sunt aut facere repellat provident occaecati excepturi optio reprehenderit
   ID: 1
   Extracto: quia et suscipit\nsuscipit recusandae consequuntur...

2. qui est esse
   ID: 2
   Extracto: est rerum tempore vitae\nsequi sint nihil repr...

3. ea molestias quasi exercitationem repellat qui ipsa sit aut
   ID: 3
   Extracto: et iusto sed quo iure\nvoluptatem occaecati om...

💾 Datos guardados en 'articulos_scrapeados.json'
```

---

### 🎓 Conceptos Clave

| Concepto              | Explicación                                |
| --------------------- | ------------------------------------------ |
| **Loop de páginas**   | `for pagina in range(1, NUM_PAGINAS + 1)`  |
| **Rate limiting**     | `time.sleep(1)` entre requests             |
| **Acumulación**       | `total_articulos.extend(articulos_pagina)` |
| **Manejo de errores** | `try/except` para requests fallidos        |

**Tip:** Siempre usa `time.sleep()` entre requests para no sobrecargar el servidor.

---

## 📙 Ejemplo 4: Scraping Dinámico con Selenium

### 🎯 Objetivo

Scrapear una página que carga contenido con **JavaScript dinámico** usando Selenium.

### 📝 Contexto Empresarial

**DataHub Inc.** necesita datos de un sitio con **carga lazy** (scroll infinito). BeautifulSoup NO puede ver el contenido porque se genera con JavaScript. Usaremos Selenium.

---

### 💻 Código Python Completo

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def scrapear_con_selenium():
    """
    Scrapea una página con JavaScript dinámico.
    Ejemplo: Quotes to Scrape (página de práctica)
    """
    print("🚀 Iniciando navegador...")

    # 1️⃣ INICIALIZAR DRIVER
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Descomenta para modo sin GUI
    driver = webdriver.Chrome(options=options)

    try:
        # 2️⃣ NAVEGAR A LA PÁGINA
        url = "http://quotes.toscrape.com/js/"  # Página con JS
        print(f"🌐 Abriendo: {url}")
        driver.get(url)

        # 3️⃣ ESPERAR A QUE CARGUE EL CONTENIDO
        print("⏳ Esperando a que cargue el contenido JavaScript...")
        wait = WebDriverWait(driver, 10)

        # Esperar a que aparezcan las quotes
        quotes = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
        )

        print(f"✅ Página cargada. Encontradas {len(quotes)} quotes.\n")

        # 4️⃣ EXTRAER DATOS
        datos = []

        for i, quote_elem in enumerate(quotes, 1):
            try:
                # Extraer texto de la quote
                texto = quote_elem.find_element(By.CLASS_NAME, "text").text

                # Extraer autor
                autor = quote_elem.find_element(By.CLASS_NAME, "author").text

                # Extraer tags
                tag_elems = quote_elem.find_elements(By.CLASS_NAME, "tag")
                tags = [tag.text for tag in tag_elems]

                dato = {
                    'numero': i,
                    'texto': texto,
                    'autor': autor,
                    'tags': tags
                }

                datos.append(dato)

                print(f"📝 Quote {i}")
                print(f"   Texto: {texto[:50]}...")
                print(f"   Autor: {autor}")
                print(f"   Tags: {', '.join(tags)}")
                print()

            except Exception as e:
                print(f"⚠️ Error al extraer quote {i}: {e}")

        # 5️⃣ HACER CLIC EN "NEXT" (OPCIONAL)
        try:
            print("🔄 Intentando ir a la página siguiente...")
            next_button = driver.find_element(By.CLASS_NAME, "next")
            next_link = next_button.find_element(By.TAG_NAME, "a")
            next_link.click()

            time.sleep(2)  # Esperar a que cargue

            print("✅ Navegación exitosa a página 2")

        except Exception:
            print("ℹ️ No hay botón 'Next' o ya estamos en la última página")

        return datos

    except TimeoutException:
        print("❌ Timeout: El contenido no cargó a tiempo")
        return []

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return []

    finally:
        # 6️⃣ SIEMPRE CERRAR EL NAVEGADOR
        print("\n🔒 Cerrando navegador...")
        driver.quit()


# 🚀 EJECUTAR
print("=" * 70)
print("🕷️ SELENIUM SCRAPER - Contenido JavaScript Dinámico")
print("=" * 70)
print()

quotes = scrapear_con_selenium()

print("\n" + "=" * 70)
print(f"✅ Scraping completado: {len(quotes)} quotes extraídas")
print("=" * 70)

# Guardar en JSON
import json

with open('quotes_selenium.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, indent=2, ensure_ascii=False)

print("\n💾 Datos guardados en 'quotes_selenium.json'")
```

---

### 📤 Salida Esperada

```
======================================================================
🕷️ SELENIUM SCRAPER - Contenido JavaScript Dinámico
======================================================================

🚀 Iniciando navegador...
🌐 Abriendo: http://quotes.toscrape.com/js/
⏳ Esperando a que cargue el contenido JavaScript...
✅ Página cargada. Encontradas 10 quotes.

📝 Quote 1
   Texto: "The world as we have created it is a process...
   Autor: Albert Einstein
   Tags: change, deep-thoughts, thinking, world

📝 Quote 2
   Texto: "It is our choices, Harry, that show what we...
   Autor: J.K. Rowling
   Tags: abilities, choices

📝 Quote 3
   Texto: "There are only two ways to live your life. O...
   Autor: Albert Einstein
   Tags: inspirational, life, live, miracle, miracles

[... más quotes ...]

🔄 Intentando ir a la página siguiente...
✅ Navegación exitosa a página 2

🔒 Cerrando navegador...

======================================================================
✅ Scraping completado: 10 quotes extraídas
======================================================================

💾 Datos guardados en 'quotes_selenium.json'
```

---

### 🎓 Conceptos Clave

| Concepto                              | Explicación                                        |
| ------------------------------------- | -------------------------------------------------- |
| `WebDriverWait`                       | Espera **inteligente** hasta que aparezca elemento |
| `EC.presence_of_all_elements_located` | Condición: elementos **presentes** en DOM          |
| `.click()`                            | Simula **clic** de usuario                         |
| `driver.quit()`                       | **Cierra** el navegador (importante en `finally`)  |

**Tip:** Usa `--headless` en opciones para ejecutar sin abrir ventana (más rápido en servidores).

---

## 📕 Ejemplo 5: Scraper Masivo con Almacenamiento

### 🎯 Objetivo

Crear un **scraper completo** que:
1. Scrapea múltiples productos
2. Valida datos
3. Almacena en **SQLite**
4. Maneja errores y logging

### 📝 Contexto Empresarial

**DataHub Inc.** necesita monitorear precios de competidores diariamente. Tu tarea es crear un scraper robusto que almacene datos en base de datos para análisis histórico.

---

### 💻 Código Python Completo

```python
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import logging

# 🔧 CONFIGURACIÓN DE LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProductoScraper:
    """
    Scraper robusto para extraer productos de e-commerce.
    """

    def __init__(self, db_name='productos.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        """Crea la tabla de productos si no existe."""
        logger.info(f"📂 Configurando base de datos: {self.db_name}")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL,
                stock INTEGER,
                rating REAL,
                url TEXT,
                fecha_scraping TEXT NOT NULL,
                UNIQUE(nombre, fecha_scraping)
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("✅ Base de datos configurada")

    def validar_precio(self, precio_str):
        """
        Valida y convierte precio de string a float.
        Ejemplo: "$1,299.99" -> 1299.99
        """
        try:
            # Eliminar $, comas y espacios
            precio_limpio = precio_str.replace('$', '').replace(',', '').strip()
            precio = float(precio_limpio)

            if precio < 0:
                logger.warning(f"⚠️ Precio negativo detectado: {precio}")
                return None

            return precio

        except (ValueError, AttributeError) as e:
            logger.error(f"❌ Error al validar precio '{precio_str}': {e}")
            return None

    def validar_stock(self, stock_str):
        """Valida stock."""
        try:
            stock = int(stock_str)
            return stock if stock >= 0 else 0
        except (ValueError, TypeError):
            return 0

    def validar_rating(self, rating_str):
        """Valida rating (0-5)."""
        try:
            rating = float(rating_str)
            if 0 <= rating <= 5:
                return rating
            return None
        except (ValueError, TypeError):
            return None

    def scrapear_productos(self, url, max_productos=10):
        """
        Scrapea productos de una URL.
        """
        logger.info(f"🔍 Iniciando scraping: {url}")

        headers = {
            'User-Agent': 'DataHubScraper/1.0 (contacto@datahub.com)'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # En un caso real, aquí adaptarías los selectores
            # Para este ejemplo, usaremos datos simulados
            productos_scrapeados = self._simular_scraping(max_productos)

            logger.info(f"✅ Scraping exitoso: {len(productos_scrapeados)} productos")
            return productos_scrapeados

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error en request: {e}")
            return []

    def _simular_scraping(self, cantidad):
        """Simula scraping de productos (para demo)."""
        productos = [
            {'nombre': 'Dell XPS 13', 'precio': '$1,299.99', 'stock': '15', 'rating': '4.8'},
            {'nombre': 'MacBook Pro M3', 'precio': '$2,499.00', 'stock': '8', 'rating': '4.9'},
            {'nombre': 'Lenovo ThinkPad', 'precio': '$1,799.50', 'stock': '12', 'rating': '4.7'},
            {'nombre': 'HP Spectre x360', 'precio': '$1,599.99', 'stock': '0', 'rating': '4.6'},
            {'nombre': 'ASUS ZenBook', 'precio': '$1,099.00', 'stock': '20', 'rating': '4.5'},
        ]
        return productos[:cantidad]

    def guardar_productos(self, productos):
        """Guarda productos en SQLite."""
        logger.info(f"💾 Guardando {len(productos)} productos en DB...")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        fecha_actual = datetime.now().isoformat()
        guardados = 0
        errores = 0

        for prod in productos:
            try:
                # Validar datos
                nombre = prod['nombre']
                precio = self.validar_precio(prod['precio'])
                stock = self.validar_stock(prod['stock'])
                rating = self.validar_rating(prod['rating'])

                if precio is None:
                    logger.warning(f"⚠️ Producto '{nombre}' tiene precio inválido")
                    errores += 1
                    continue

                # Insertar en DB
                cursor.execute('''
                    INSERT OR IGNORE INTO productos
                    (nombre, precio, stock, rating, url, fecha_scraping)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nombre, precio, stock, rating, None, fecha_actual))

                if cursor.rowcount > 0:
                    guardados += 1
                    logger.info(f"   ✅ {nombre}: ${precio} (stock: {stock})")
                else:
                    logger.info(f"   ℹ️ {nombre}: Ya existe para hoy")

            except sqlite3.Error as e:
                logger.error(f"   ❌ Error DB al guardar {prod['nombre']}: {e}")
                errores += 1

        conn.commit()
        conn.close()

        logger.info(f"✅ Guardados: {guardados} | ⚠️ Errores: {errores}")
        return guardados

    def obtener_estadisticas(self):
        """Obtiene estadísticas de la DB."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Total de productos
        cursor.execute('SELECT COUNT(*) FROM productos')
        total = cursor.fetchone()[0]

        # Precio promedio
        cursor.execute('SELECT AVG(precio) FROM productos WHERE precio IS NOT NULL')
        precio_avg = cursor.fetchone()[0]

        # Producto más caro
        cursor.execute('''
            SELECT nombre, precio
            FROM productos
            WHERE precio IS NOT NULL
            ORDER BY precio DESC
            LIMIT 1
        ''')
        mas_caro = cursor.fetchone()

        conn.close()

        return {
            'total_productos': total,
            'precio_promedio': round(precio_avg, 2) if precio_avg else 0,
            'producto_mas_caro': mas_caro if mas_caro else ('N/A', 0)
        }


# 🚀 EJECUTAR SCRAPER
if __name__ == '__main__':
    print("=" * 70)
    print("🕷️ SCRAPER MASIVO CON ALMACENAMIENTO - DataHub Inc.")
    print("=" * 70)
    print()

    # Crear scraper
    scraper = ProductoScraper(db_name='productos_competencia.db')

    # Scrapear (en la realidad, aquí irían URLs reales)
    url_simulada = "https://ejemplo-ecommerce.com/laptops"
    productos = scraper.scrapear_productos(url_simulada, max_productos=5)

    # Guardar en DB
    if productos:
        scraper.guardar_productos(productos)

        # Mostrar estadísticas
        stats = scraper.obtener_estadisticas()
        print("\n" + "=" * 70)
        print("📊 ESTADÍSTICAS")
        print("=" * 70)
        print(f"📦 Total de productos en DB: {stats['total_productos']}")
        print(f"💰 Precio promedio: ${stats['precio_promedio']}")
        print(f"👑 Producto más caro: {stats['producto_mas_caro'][0]} "
              f"(${stats['producto_mas_caro'][1]})")
        print("=" * 70)

    else:
        print("❌ No se pudieron scrapear productos")
```

---

### 📤 Salida Esperada

```
======================================================================
🕷️ SCRAPER MASIVO CON ALMACENAMIENTO - DataHub Inc.
======================================================================

2025-10-23 14:35:22 - INFO - 📂 Configurando base de datos: productos_competencia.db
2025-10-23 14:35:22 - INFO - ✅ Base de datos configurada
2025-10-23 14:35:22 - INFO - 🔍 Iniciando scraping: https://ejemplo-ecommerce.com/laptops
2025-10-23 14:35:22 - INFO - ✅ Scraping exitoso: 5 productos
2025-10-23 14:35:22 - INFO - 💾 Guardando 5 productos en DB...
2025-10-23 14:35:22 - INFO -    ✅ Dell XPS 13: $1299.99 (stock: 15)
2025-10-23 14:35:22 - INFO -    ✅ MacBook Pro M3: $2499.0 (stock: 8)
2025-10-23 14:35:22 - INFO -    ✅ Lenovo ThinkPad: $1799.5 (stock: 12)
2025-10-23 14:35:22 - INFO -    ✅ HP Spectre x360: $1599.99 (stock: 0)
2025-10-23 14:35:22 - INFO -    ✅ ASUS ZenBook: $1099.0 (stock: 20)
2025-10-23 14:35:22 - INFO - ✅ Guardados: 5 | ⚠️ Errores: 0

======================================================================
📊 ESTADÍSTICAS
======================================================================
📦 Total de productos en DB: 5
💰 Precio promedio: $1659.5
👑 Producto más caro: MacBook Pro M3 ($2499.0)
======================================================================
```

---

### 🎓 Conceptos Clave

| Concepto                | Explicación                                |
| ----------------------- | ------------------------------------------ |
| **Clase scraper**       | Encapsula lógica en una clase reutilizable |
| **Validación de datos** | Limpia y valida antes de guardar           |
| **SQLite**              | Base de datos local sin servidor           |
| **Logging**             | Registra eventos para debugging            |
| **UNIQUE constraint**   | Evita duplicados en DB                     |

**Tip:** Usa clases para scrapers complejos, funciones simples para scrapers pequeños.

---

## 📊 Comparación de Métodos

| Característica  | BeautifulSoup           | Selenium                       |
| --------------- | ----------------------- | ------------------------------ |
| **Velocidad**   | ⚡ Muy rápido (segundos) | 🐌 Lento (abre navegador real)  |
| **Memoria**     | 💚 Baja (~50 MB)         | 🔴 Alta (~500 MB)               |
| **JavaScript**  | ❌ No puede ejecutar     | ✅ Ejecuta JS completo          |
| **Interacción** | ❌ No puede hacer clic   | ✅ Simula usuario real          |
| **Uso típico**  | Páginas estáticas       | Páginas dinámicas (React, Vue) |

**Regla general:**
1. Intenta con **BeautifulSoup** primero
2. Si no funciona (contenido dinámico), usa **Selenium**

---

## ✅ Resumen de Conceptos

### BeautifulSoup
- `find()` - Primer elemento
- `find_all()` - Todos los elementos
- `.text` - Extraer texto
- `.get('atributo')` - Extraer atributo

### Selenium
- `WebDriverWait` - Esperas inteligentes
- `find_element(By.CLASS_NAME)` - Encontrar por clase
- `.click()` - Simular clic
- `driver.quit()` - Cerrar navegador

### Buenas Prácticas
- ✅ Rate limiting con `time.sleep()`
- ✅ User-Agent identificable
- ✅ Validación de datos antes de guardar
- ✅ Manejo de errores con try/except
- ✅ Logging para debugging

---

## 🎯 Siguiente Paso

¡Excelente trabajo! 🎉 Ahora dominas los conceptos fundamentales de web scraping.

**Próximo paso:** [03-EJERCICIOS.md](03-EJERCICIOS.md) - 15 ejercicios progresivos para practicar.

---

*Última actualización: 2025-10-23*
*Tema 2 - Módulo 4 - Master en Ingeniería de Datos*
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
