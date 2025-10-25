# 📘 Tema 2: Web Scraping - Extracción Ética de Datos Web

**Módulo 4:** APIs y Web Scraping
**Duración estimada:** 1-1.5 semanas (12-18 horas)
**Nivel:** Intermedio
**Prerequisitos:** Tema 1 (APIs REST), Python básico, HTTP básico

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

✅ **Parsear HTML** con BeautifulSoup para extraer datos estructurados
✅ **Scrapear contenido dinámico** cargado con JavaScript usando Selenium
✅ **Respetar robots.txt** y aplicar rate limiting ético
✅ **Extraer tablas, enlaces y atributos** de páginas web complejas
✅ **Almacenar datos scrapeados** en SQLite con validación
✅ **Decidir cuándo usar APIs vs Web Scraping** según el caso de uso
✅ **Construir scrapers completos** con manejo de errores, logging y TDD

---

## 📚 Conceptos Clave

### 🔍 Web Scraping
> **Analogía:** Es como ser un bibliotecario que extrae información específica de libros (páginas web) y la organiza en un catálogo estructurado (base de datos).

**Cuándo usar Web Scraping:**
- ❌ El sitio NO tiene API pública
- ✅ Los datos están en HTML accesible
- ✅ El sitio lo permite (robots.txt)
- ✅ Tienes caso de uso legítimo (análisis, investigación)

### 🧱 Conceptos Fundamentales

| Concepto          | Descripción                         | Herramienta                  |
| ----------------- | ----------------------------------- | ---------------------------- |
| **HTML/DOM**      | Estructura de la página web         | Navegador DevTools           |
| **BeautifulSoup** | Parseo de HTML estático             | `beautifulsoup4`             |
| **Selenium**      | Scraping de contenido dinámico (JS) | `selenium`                   |
| **Robots.txt**    | Reglas de scraping del sitio        | `urllib.robotparser`         |
| **Rate Limiting** | Respetar límites del servidor       | `time.sleep()`               |
| **CSS Selectors** | Selección de elementos HTML         | `.select()`, `.select_one()` |
| **XPath**         | Alternativa a CSS Selectors         | `lxml` (opcional)            |
| **User-Agent**    | Identificación en requests HTTP     | `requests.headers`           |

---

## 📁 Estructura del Tema

```
tema-2-web-scraping/
├── 01-TEORIA.md                  # ~5,200 palabras (40-50 min)
│   ├── HTML, CSS, DOM
│   ├── BeautifulSoup
│   ├── Selenium
│   ├── Robots.txt y ética
│   └── Comparación Scraping vs APIs
│
├── 02-EJEMPLOS.md                # 5 ejemplos trabajados (60-90 min)
│   ├── Ejemplo 1: Scraping básico con BeautifulSoup
│   ├── Ejemplo 2: Extraer tabla HTML → CSV
│   ├── Ejemplo 3: Navegación multi-página
│   ├── Ejemplo 4: Selenium para contenido dinámico
│   └── Ejemplo 5: Scraper completo con SQLite
│
├── 03-EJERCICIOS.md              # 15 ejercicios con soluciones (8-12 horas)
│   ├── Básicos (1-5): HTML, BeautifulSoup, robots.txt
│   ├── Intermedios (6-10): Tablas, navegación, Selenium
│   └── Avanzados (11-15): Rate limiting, pipelines completos
│
├── 04-proyecto-practico/         # Proyecto TDD completo (4-6 horas)
│   ├── src/
│   │   ├── scraper_html.py       # BeautifulSoup (5 funciones)
│   │   ├── scraper_selenium.py   # Selenium (3 funciones)
│   │   ├── validador_scraping.py # Robots.txt, rate limiting (4 funciones)
│   │   ├── almacenamiento.py     # SQLite (3 funciones)
│   │   └── utilidades_scraping.py # Logging, headers (4 funciones)
│   ├── tests/                    # 71 tests, 90% cobertura
│   ├── ejemplos/                 # HTML de ejemplo
│   ├── datos/                    # Base de datos SQLite
│   └── README.md                 # Documentación completa
│
├── REVISION_PEDAGOGICA.md        # Evaluación: 9.3/10 ⭐
└── README.md                     # Este archivo

```

---

## 🚀 Cómo Estudiar Este Tema

### Ruta de Aprendizaje Recomendada

```
1️⃣ TEORÍA (40-50 min)
   └─> Lee 01-TEORIA.md completo
   └─> Prueba los snippets en Jupyter/Python REPL
   └─> Instala: beautifulsoup4, selenium, webdriver-manager

2️⃣ EJEMPLOS (60-90 min)
   └─> Sigue 02-EJEMPLOS.md paso a paso
   └─> Ejecuta cada ejemplo completo
   └─> Modifica variables para experimentar

3️⃣ EJERCICIOS BÁSICOS (2-3 horas)
   └─> Resuelve ejercicios 1-5 en 03-EJERCICIOS.md
   └─> Consulta hints si te atascas
   └─> Compara con soluciones al final

4️⃣ EJERCICIOS INTERMEDIOS (3-4 horas)
   └─> Resuelve ejercicios 6-10
   └─> Introduce Selenium en ejercicio 10
   └─> Practica navegación multi-página

5️⃣ EJERCICIOS AVANZADOS (3-5 horas)
   └─> Resuelve ejercicios 11-15
   └─> Implementa rate limiting y robots.txt
   └─> Construye pipeline completo (scrape → clean → store)

6️⃣ PROYECTO PRÁCTICO (4-6 horas)
   └─> Estudia arquitectura en 04-proyecto-practico/README.md
   └─> Lee los tests para entender requisitos
   └─> Ejecuta pytest -v para ver 71 tests pasando
   └─> Modifica y extiende funciones para tu caso de uso

7️⃣ PRÁCTICA PERSONAL (Opcional, 2-4 horas)
   └─> Elige un sitio web que te interese (revisa robots.txt)
   └─> Construye tu propio scraper desde cero
   └─> Aplica TDD: escribe tests primero
```

**Tiempo total estimado:** 12-18 horas (1-1.5 semanas a ritmo cómodo)

---

## 📦 Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Navegar al directorio del proyecto práctico
cd modulo-04-apis-scraping/tema-2-web-scraping/04-proyecto-practico/

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Verificar Instalación de ChromeDriver (Selenium)

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Esto descargará ChromeDriver automáticamente si no existe
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

### 3. Ejecutar Tests del Proyecto

```bash
# En el directorio del proyecto práctico
pytest -v --cov=src --cov-report=term-missing

# Salida esperada:
# 71 tests passed, 90% coverage ✅
```

---

## ✅ Criterios de Éxito

Habrás completado exitosamente este tema cuando puedas:

### Nivel Básico ✅
- [ ] Parsear HTML con BeautifulSoup (`find()`, `find_all()`, `select()`)
- [ ] Extraer textos, enlaces y atributos de elementos HTML
- [ ] Validar si un sitio permite scraping consultando `robots.txt`
- [ ] Implementar rate limiting básico con `time.sleep()`

### Nivel Intermedio ✅
- [ ] Extraer tablas HTML y convertirlas a DataFrames de Pandas
- [ ] Navegar múltiples páginas y consolidar datos
- [ ] Usar Selenium para scrapear contenido cargado con JavaScript
- [ ] Almacenar datos scrapeados en SQLite con validación

### Nivel Avanzado ✅
- [ ] Construir scrapers completos con logging y manejo de errores
- [ ] Implementar scrapers que respetan `robots.txt` automáticamente
- [ ] Decidir cuándo usar scraping vs APIs según el caso de uso
- [ ] Integrar scraping en pipelines ETL (Extracción → Transformación → Carga)

### Proyecto Práctico ✅
- [ ] Comprender arquitectura de 5 módulos del proyecto
- [ ] Ejecutar 71 tests con 90% cobertura exitosamente
- [ ] Modificar funciones existentes para nuevos casos de uso
- [ ] Extender proyecto con nuevas funcionalidades (ej: scraping de imágenes)

---

## 🐛 Troubleshooting Común

### Problema 1: "ModuleNotFoundError: No module named 'bs4'"

**Solución:**
```bash
pip install beautifulsoup4
```

### Problema 2: "selenium.common.exceptions.SessionNotCreatedException"

**Causa:** ChromeDriver desactualizado o no instalado.

**Solución:**
```bash
pip install --upgrade selenium webdriver-manager
```

Luego usa `webdriver-manager` en tu código:
```python
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

### Problema 3: "ValueError: No se encontró la tabla en el HTML"

**Causa:** El HTML no contiene `<table>` o los selectores son incorrectos.

**Solución:**
- Usa DevTools (F12) para inspeccionar el HTML real
- Verifica que `robots.txt` permite scraping
- Asegúrate de que no es contenido dinámico (usa Selenium si aplica)

### Problema 4: "Request bloqueado por el sitio (403 Forbidden)"

**Causa:** El sitio detecta que eres un bot (falta User-Agent).

**Solución:**
```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)
```

### Problema 5: "Tests de Selenium fallan: TimeoutException"

**Causa:** Elementos no cargan a tiempo o selectores incorrectos.

**Solución:**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Esperar hasta que el elemento esté presente
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
```

---

## 📊 Métricas del Tema

| Métrica                     | Valor                               |
| --------------------------- | ----------------------------------- |
| **Palabras en teoría**      | ~5,200                              |
| **Tiempo de lectura**       | 40-50 min                           |
| **Ejemplos trabajados**     | 5 (BeautifulSoup + Selenium)        |
| **Ejercicios totales**      | 15 (Básico → Intermedio → Avanzado) |
| **Funciones en proyecto**   | 19 funciones (5 módulos)            |
| **Tests en proyecto**       | 71 tests                            |
| **Cobertura de código**     | 90%                                 |
| **Calificación pedagógica** | 9.3/10 ⭐                            |

---

## 🎓 Competencias Desarrolladas

Después de completar este tema, habrás desarrollado:

✅ **Extracción de datos web** con BeautifulSoup y Selenium
✅ **Scraping ético** respetando robots.txt y rate limits
✅ **Navegación programática** de sitios web complejos
✅ **Almacenamiento estructurado** en SQLite
✅ **Manejo de contenido dinámico** con JavaScript
✅ **Validación de datos** scrapeados
✅ **TDD aplicado** a proyectos de scraping
✅ **Toma de decisiones técnicas** (API vs Scraping)

---

## 🔗 Relación con Otros Temas

### Prerequisitos
- **Tema 1 (APIs REST):** Comprender HTTP, status codes, headers
- **Módulo 1 (Python Básico):** Funciones, diccionarios, listas, CSV
- **Módulo 3 (ETL):** Conceptos de extracción y transformación

### Siguiente Tema
- **Tema 3 (Rate Limiting y Caching):** Optimizar scrapers para escala

### Aplicaciones Futuras
- **Módulo 6 (Apache Airflow):** Programar scrapers periódicos
- **Módulo 8 (Data Warehousing):** Cargar datos scrapeados a DWH
- **Proyectos Finales:** Pipelines completos de datos web

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Robots.txt Specification](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

### Sitios para Practicar Scraping (Legalmente)
- [https://quotes.toscrape.com/](https://quotes.toscrape.com/) - Sitio educativo para scraping
- [https://books.toscrape.com/](https://books.toscrape.com/) - E-commerce ficticio
- [https://scrapethissite.com/](https://scrapethissite.com/) - Ejercicios de scraping

### Herramientas Útiles
- **SelectorGadget:** Extensión Chrome para generar CSS Selectors
- **XPath Helper:** Extensión Chrome para probar XPath
- **DevTools (F12):** Inspector de HTML nativo del navegador

### Lecturas Recomendadas
- [Web Scraping with Python (2nd Edition)](https://www.oreilly.com/library/view/web-scraping-with/9781491985564/) - Ryan Mitchell
- [Legal aspects of web scraping](https://www.eff.org/issues/coders/web-scraping) - Electronic Frontier Foundation

---

## ⚖️ Consideraciones Legales y Éticas

### ✅ Buenas Prácticas

- Respetar `robots.txt` **SIEMPRE**
- Implementar rate limiting (mínimo 1 segundo entre requests)
- Identificarte con User-Agent descriptivo
- No sobrecargar servidores (máx 1-2 requests/seg)
- Almacenar solo datos públicamente accesibles
- Respetar términos de servicio del sitio

### ❌ Malas Prácticas (NO HACER)

- Ignorar `robots.txt`
- Scraping masivo sin rate limiting (DDoS)
- Falsificar User-Agent para evadir bloqueos
- Scraping de contenido protegido por login (sin permiso)
- Reventa de datos scrapeados
- Scraping de datos personales sin consentimiento (GDPR)

### 📜 Marco Legal

- **GDPR (Europa):** No scrapear datos personales sin base legal
- **CFAA (EE.UU.):** No "acceder sin autorización" (términos difusos)
- **Casos relevantes:** hiQ Labs vs LinkedIn (scraping de datos públicos es legal)

**Regla de oro:** Si no lo puedes ver públicamente en un navegador, no lo scrapees.

---

## 🎉 Proyecto Final Sugerido

Una vez domines este tema, intenta:

### "Scraper de Inmobiliaria Ficticia"

**Objetivo:** Extraer 100 propiedades de un sitio inmobiliario de ejemplo.

**Requisitos:**
1. Validar `robots.txt` antes de empezar
2. Extraer: dirección, precio, habitaciones, m², descripción
3. Implementar rate limiting (2 seg entre requests)
4. Almacenar en SQLite con validación (precio > 0, habitaciones > 0)
5. Logging completo en archivo `.log`
6. TDD: escribir 20+ tests primero
7. README con instrucciones de uso

**Entregables:**
- Código Python modular (3-5 módulos)
- Base de datos SQLite con 100 propiedades
- Tests con >80% cobertura
- README con análisis de datos (precio promedio, etc.)

---

## 📞 Soporte

Si tienes dudas o problemas:

1. **Revisa:** Sección de Troubleshooting arriba
2. **Consulta:** REVISION_PEDAGOGICA.md para entender objetivos
3. **Experimenta:** Modifica ejemplos para aprender haciendo
4. **Practica:** Los 15 ejercicios cubren casos comunes

---

## 🏆 Siguiente Paso

Una vez completes este tema:

➡️ **Tema 3: Rate Limiting y Caching** - Optimiza tus scrapers para escala

Aprenderás:
- Estrategias avanzadas de rate limiting (token bucket, sliding window)
- Caching en memoria y disco (Redis, shelve)
- Async requests con `aiohttp` (10x más rápido)
- Monitoreo de throughput y métricas

---

**¡Feliz Scraping Ético! 🕷️✨**

*Última actualización: 2025-10-24*
*Calificación pedagógica: 9.3/10 ⭐*
*Duración estimada: 12-18 horas*
