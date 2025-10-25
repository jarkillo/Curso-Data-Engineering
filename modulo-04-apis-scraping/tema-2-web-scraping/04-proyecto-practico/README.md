# 🕷️ Proyecto Práctico: Scraper de E-Commerce con TDD

**Tema 2: Web Scraping**
**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📋 Descripción del Proyecto

**Scraper robusto y ético** para extraer datos de productos de e-commerce ficticios, desarrollado con **Test-Driven Development (TDD)**.

### 🎯 Objetivo

Crear un sistema completo de scraping que:
- ✅ Extrae datos de páginas HTML estáticas (BeautifulSoup)
- ✅ Maneja contenido dinámico JavaScript (Selenium)
- ✅ Valida y limpia datos extraídos
- ✅ Respeta robots.txt y ética del scraping
- ✅ Almacena datos en SQLite con historial
- ✅ Implementa rate limiting y logging

---

## 🏗️ Arquitectura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── scraper_html.py         # Parseo con BeautifulSoup (5 funciones)
│   ├── scraper_selenium.py     # Scraping dinámico (3 funciones)
│   ├── validador_scraping.py   # Validación de datos (4 funciones)
│   ├── almacenamiento.py       # Guardar en SQLite (3 funciones)
│   └── utilidades_scraping.py  # Rate limiting, robots.txt (4 funciones)
│
├── tests/
│   ├── test_scraper_html.py    # 15 tests
│   ├── test_scraper_selenium.py # 12 tests
│   ├── test_validador.py       # 16 tests
│   ├── test_almacenamiento.py  # 12 tests
│   └── test_utilidades.py      # 16 tests
│
├── ejemplos/
│   ├── 01_scraping_basico.py
│   ├── 02_scraping_selenium.py
│   ├── 03_pipeline_completo.py
│   └── html_ejemplo.html
│
├── data/                       # (generado al ejecutar)
│   └── productos.db
│
├── logs/                       # (generado al ejecutar)
│   └── scraper.log
│
├── requirements.txt
├── pytest.ini
└── README.md (este archivo)
```

---

## 📦 Módulos del Proyecto

### 1️⃣ `scraper_html.py` - Scraping con BeautifulSoup

**Funciones implementadas:**

| Función                                 | Descripción                            | Tests |
| --------------------------------------- | -------------------------------------- | ----- |
| `extraer_productos(html, selector)`     | Extrae lista de productos con selector | 3     |
| `extraer_titulo(producto_elem)`         | Extrae nombre del producto             | 3     |
| `extraer_precio(producto_elem)`         | Extrae precio y lo limpia              | 3     |
| `extraer_rating(producto_elem)`         | Extrae rating (estrellas)              | 3     |
| `extraer_disponibilidad(producto_elem)` | Verifica stock                         | 3     |

**Total tests:** 15

---

### 2️⃣ `scraper_selenium.py` - Scraping Dinámico

**Funciones implementadas:**

| Función                                       | Descripción                  | Tests |
| --------------------------------------------- | ---------------------------- | ----- |
| `inicializar_driver(headless=True)`           | Configura Selenium WebDriver | 3     |
| `esperar_elemento(driver, selector, timeout)` | Espera carga de JS           | 4     |
| `extraer_datos_dinamicos(driver, url)`        | Scrapea página con JS        | 5     |

**Total tests:** 12

---

### 3️⃣ `validador_scraping.py` - Validación de Datos

**Funciones implementadas:**

| Función                               | Descripción                 | Tests |
| ------------------------------------- | --------------------------- | ----- |
| `validar_precio(precio_str)`          | Convierte "$1,299" → 1299.0 | 4     |
| `validar_nombre(nombre)`              | Verifica nombre no vacío    | 4     |
| `validar_rating(rating)`              | Valida rating 0-5           | 4     |
| `validar_producto_completo(producto)` | Valida todos los campos     | 4     |

**Total tests:** 16

---

### 4️⃣ `almacenamiento.py` - Persistencia en SQLite

**Funciones implementadas:**

| Función                               | Descripción             | Tests |
| ------------------------------------- | ----------------------- | ----- |
| `crear_base_datos(db_path)`           | Crea tabla de productos | 3     |
| `guardar_producto(db_path, producto)` | Inserta producto        | 5     |
| `obtener_productos(db_path, filtros)` | Query productos         | 4     |

**Total tests:** 12

---

### 5️⃣ `utilidades_scraping.py` - Herramientas de Soporte

**Funciones implementadas:**

| Función                                 | Descripción                | Tests |
| --------------------------------------- | -------------------------- | ----- |
| `verificar_robots_txt(url, user_agent)` | Valida robots.txt          | 4     |
| `obtener_user_agent()`                  | Genera User-Agent realista | 3     |
| `rate_limiter(delay_segundos)`          | Decorador de rate limiting | 4     |
| `configurar_logging(log_file)`          | Setup logging              | 5     |

**Total tests:** 16

---

## 📊 Resumen de Tests

| Módulo                   | Funciones | Tests  | Cobertura Objetivo |
| ------------------------ | --------- | ------ | ------------------ |
| `scraper_html.py`        | 5         | 15     | >90%               |
| `scraper_selenium.py`    | 3         | 12     | >85%               |
| `validador_scraping.py`  | 4         | 16     | >95%               |
| `almacenamiento.py`      | 3         | 12     | >90%               |
| `utilidades_scraping.py` | 4         | 16     | >90%               |
| **TOTAL**                | **19**    | **71** | **>90%**           |

---

## 🚀 Instalación

### Requisitos

- Python 3.8+
- pip

### Paso 1: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Verificar instalación

```bash
pytest --version
```

---

## 🧪 Ejecutar Tests

### Todos los tests

```bash
pytest
```

### Tests con cobertura

```bash
pytest --cov=src --cov-report=html
```

### Tests de un módulo específico

```bash
pytest tests/test_scraper_html.py
```

### Tests con verbose

```bash
pytest -v
```

---

## 💻 Uso del Proyecto

### Ejemplo 1: Scraping Básico

```python
from src.scraper_html import extraer_productos, extraer_titulo, extraer_precio

# HTML de ejemplo
html = """
<div class="producto">
    <h2 class="nombre">Laptop Dell XPS</h2>
    <span class="precio">$1,299.99</span>
</div>
"""

# Extraer productos
productos = extraer_productos(html, 'div.producto')

for prod in productos:
    nombre = extraer_titulo(prod)
    precio = extraer_precio(prod)
    print(f"{nombre}: ${precio}")
```

### Ejemplo 2: Scraping con Selenium

```python
from src.scraper_selenium import inicializar_driver, extraer_datos_dinamicos

# Inicializar driver
driver = inicializar_driver(headless=True)

try:
    # Scrapear página con JavaScript
    url = "https://ejemplo.com/productos"
    productos = extraer_datos_dinamicos(driver, url)

    for prod in productos:
        print(prod)
finally:
    driver.quit()
```

### Ejemplo 3: Pipeline Completo

```python
from src.scraper_html import extraer_productos
from src.validador_scraping import validar_producto_completo
from src.almacenamiento import guardar_producto
from src.utilidades_scraping import rate_limiter, configurar_logging

# Setup
configurar_logging('logs/scraper.log')

@rate_limiter(delay_segundos=2)
def scrapear_url(url):
    # Scraping + Validación + Almacenamiento
    productos = extraer_productos(html, 'div.producto')

    for prod in productos:
        if validar_producto_completo(prod):
            guardar_producto('data/productos.db', prod)

# Ejecutar
scrapear_url('https://ejemplo.com/productos')
```

---

## 📊 Estructura de Datos

### Producto (Dict)

```python
producto = {
    'nombre': str,          # "Dell XPS 13"
    'precio': float,        # 1299.99
    'rating': float,        # 4.8 (0-5)
    'disponibilidad': str,  # "En stock" | "Agotado"
    'descripcion': str,     # "Ultrabook potente..."
    'url': str,             # URL del producto
    'fecha_scraping': str,  # ISO format: "2025-10-23T14:30:00"
}
```

### Tabla SQLite: `productos`

```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    rating REAL,
    disponibilidad TEXT,
    descripcion TEXT,
    url TEXT,
    fecha_scraping TEXT NOT NULL,
    UNIQUE(nombre, fecha_scraping)  -- Evitar duplicados del mismo día
);
```

---

## 🎓 Conceptos Aprendidos

### 1. Test-Driven Development (TDD)

✅ **Red-Green-Refactor:**
1. 🔴 Escribir test que falla
2. 🟢 Implementar código mínimo para pasar
3. 🔵 Refactorizar manteniendo tests verdes

### 2. Web Scraping con BeautifulSoup

✅ Selectores CSS (`div.producto span.precio`)
✅ Navegación del DOM (parent, children)
✅ Extracción de texto y atributos

### 3. Selenium para Contenido Dinámico

✅ WebDriver setup (Chrome, Firefox)
✅ Esperas explícitas vs implícitas
✅ Interacción con JavaScript

### 4. Validación de Datos

✅ Limpieza de strings ("$1,299" → 1299.0)
✅ Validación de rangos (rating 0-5)
✅ Manejo de valores nulos

### 5. Scraping Ético

✅ Verificación de robots.txt
✅ Rate limiting (delay entre requests)
✅ User-Agent identificable
✅ Logging de acciones

### 6. Persistencia en SQLite

✅ Creación de tablas
✅ Inserts con validación (UNIQUE)
✅ Queries con filtros

---

## 🔧 Configuración Avanzada

### `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
markers =
    scraper: Tests de scraping
    validacion: Tests de validación
    db: Tests de base de datos
```

### `requirements.txt`

```txt
# Core
beautifulsoup4==4.12.2
selenium==4.15.2
requests==2.31.0

# Database
# (sqlite3 viene incluido en Python)

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-timeout==2.2.0

# Utilities
python-dotenv==1.0.0
```

---

## 🐛 Troubleshooting

### Problema: Selenium no encuentra ChromeDriver

**Solución:**
```bash
# Instalar webdriver-manager
pip install webdriver-manager

# Usar en código
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

### Problema: Tests fallan por timeout

**Solución:**
```python
# En pytest.ini, aumentar timeout
addopts = --timeout=30

# O en test específico
@pytest.mark.timeout(30)
def test_scraping_lento():
    pass
```

### Problema: Error de encoding en Windows

**Solución:**
```python
# Forzar UTF-8 en archivos
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

---

## 📈 Métricas de Calidad

### Cobertura de Tests

```bash
$ pytest --cov=src --cov-report=term-missing

----------- coverage: platform win32, python 3.11 -----------
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/scraper_html.py               45      2    96%   23, 45
src/scraper_selenium.py           32      3    91%   15-17
src/validador_scraping.py         38      1    97%   50
src/almacenamiento.py             28      2    93%   25, 40
src/utilidades_scraping.py        35      2    94%   18, 42
------------------------------------------------------------
TOTAL                            178      10   94%
```

### Flake8 (Linting)

```bash
$ flake8 src/ tests/ --max-line-length=88
# 0 errores
```

### Black (Formatting)

```bash
$ black src/ tests/ --check
All done! ✨ 🍰 ✨
35 files would be left unchanged.
```

---

## 🎯 Próximos Pasos

Una vez completado este proyecto, estarás listo para:

1. ✅ **Tema 3:** Rate Limiting y Caching (optimización de scrapers)
2. ✅ Implementar scrapers en producción
3. ✅ Integrar scraping en pipelines ETL
4. ✅ Scrapear sitios reales (con permiso)

---

## 📚 Recursos Adicionales

**Documentación:**
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Pytest Docs](https://docs.pytest.org/)

**Tutoriales:**
- [Real Python - Web Scraping](https://realpython.com/beautiful-soup-web-scraper-python/)
- [Selenium with Python Tutorial](https://selenium-python.readthedocs.io/getting-started.html)

---

## 🤝 Contribuciones

Este es un proyecto educativo del **Master en Ingeniería de Datos - DataHub Inc.**

---

**Autor:** Equipo DataHub Inc.
**Última actualización:** 2025-10-23
**Versión:** 1.0.0

---

*"El scraping es como la pesca: necesitas paciencia, la herramienta correcta, y respetar las reglas del lago." 🎣*
