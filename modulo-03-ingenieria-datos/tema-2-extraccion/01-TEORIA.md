# Tema 2: Extracción de Datos - Fuentes y Técnicas

## Introducción: ¿Por qué importa la extracción de datos?

Imagina que eres un chef que necesita ingredientes para cocinar. Los ingredientes pueden estar en el supermercado (archivos CSV), en una tienda especializada que necesita pedido especial (APIs), o en el mercado local donde tienes que seleccionar producto por producto (web scraping). Cada fuente requiere una técnica diferente para obtener lo que necesitas.

En Data Engineering, la **extracción de datos** es el primer paso crítico de cualquier pipeline ETL/ELT. Sin datos, no hay transformación ni análisis posible. Pero los datos viven en lugares muy diferentes: archivos locales, APIs de terceros, páginas web, bases de datos, etc.

**¿Por qué es un desafío?**
- Cada fuente tiene su propio formato y protocolo
- Los datos pueden estar "sucios" o mal estructurados
- Las fuentes pueden ser inestables o lentas
- Necesitas manejar errores y reintentos
- Debes respetar límites de uso (rate limits)
- La seguridad y ética son fundamentales

En este tema aprenderás a extraer datos de las **3 fuentes más comunes** en Data Engineering:
1. **Archivos** (CSV, JSON, Excel)
2. **APIs REST** (requests, autenticación, paginación)
3. **Web Scraping** (Beautiful Soup, scraping ético)

---

## Parte 1: Extracción desde Archivos

### 1.1 Archivos CSV (Comma-Separated Values)

#### ¿Qué es un CSV?

Un CSV es un formato de texto plano donde cada línea representa una fila de datos y las columnas están separadas por un carácter delimitador (normalmente una coma).

**Analogía**: Es como una hoja de Excel guardada en formato de texto simple. Si abres un CSV con el Bloc de notas, verías algo así:

```
nombre,edad,ciudad
Ana,28,Madrid
Carlos,35,Barcelona
```

#### ¿Por qué CSV es popular en Data Engineering?

- ✅ **Universal**: Funciona en cualquier sistema operativo
- ✅ **Ligero**: Ocupa poco espacio
- ✅ **Fácil de leer**: Puedes abrirlo con cualquier editor de texto
- ✅ **Compatible**: Excel, Python, R, SQL... todos lo entienden

#### Desafíos comunes con CSV

**1. Encoding (Codificación de caracteres)**

El encoding determina cómo se guardan los caracteres especiales (tildes, eñes, emojis). Los encodings más comunes son:

- **UTF-8**: El estándar moderno, soporta todos los idiomas y emojis
- **Latin-1 (ISO-8859-1)**: Común en sistemas antiguos europeos
- **UTF-8-BOM**: UTF-8 con una marca especial al inicio del archivo

**Analogía**: Es como si un libro estuviera escrito en español pero con instrucciones en chino sobre cómo leerlo. Si no sabes las instrucciones correctas, las tildes y eñes se ven mal.

**Ejemplo de problema**:
```python
# Si intentas leer un CSV Latin-1 como UTF-8:
# "José" se vería como "José" o daría error
```

**Solución**:
```python
import csv

# Especificar el encoding correcto
with open('datos.csv', 'r', encoding='latin-1') as archivo:
    lector = csv.reader(archivo)
    for fila in lector:
        print(fila)
```

**2. Delimitadores**

Aunque se llaman "Comma-Separated", no siempre usan comas. Pueden usar:
- `,` (coma) - Lo más común en países anglosajones
- `;` (punto y coma) - Común en Europa (donde la coma es decimal)
- `\t` (tabulador) - Archivos TSV
- `|` (pipe) - Bases de datos

**3. Headers (Cabeceras)**

Algunos CSV tienen la primera fila con nombres de columnas, otros no:

```
# CON header
nombre,edad,ciudad
Ana,28,Madrid

# SIN header (solo datos)
Ana,28,Madrid
Carlos,35,Barcelona
```

#### Buenas prácticas para CSV

✅ **Detectar encoding automáticamente**:
```python
import chardet

with open('datos.csv', 'rb') as archivo:
    resultado = chardet.detect(archivo.read())
    encoding = resultado['encoding']
    print(f"Encoding detectado: {encoding}")
```

✅ **Usar pandas para lectura robusta**:
```python
import pandas as pd

# Pandas maneja muchos casos automáticamente
df = pd.read_csv(
    'datos.csv',
    encoding='utf-8',
    delimiter=';',
    header=0,  # Fila 0 es el header
    na_values=['', 'NULL', 'N/A']  # Valores que considerar como nulos
)
```

✅ **Validar estructura antes de procesar**:
```python
# Verificar que tiene las columnas esperadas
columnas_esperadas = ['nombre', 'edad', 'ciudad']
if not all(col in df.columns for col in columnas_esperadas):
    raise ValueError("El CSV no tiene la estructura esperada")
```

---

### 1.2 Archivos JSON (JavaScript Object Notation)

#### ¿Qué es JSON?

JSON es un formato de texto que representa datos estructurados usando pares clave-valor. Es el formato más usado en APIs web.

**Analogía**: JSON es como un diccionario donde cada cosa tiene una etiqueta. Es más flexible que CSV porque puede tener estructuras anidadas (como cajas dentro de cajas).

**Ejemplo simple**:
```json
{
  "nombre": "Ana",
  "edad": 28,
  "ciudad": "Madrid"
}
```

**Ejemplo anidado**:
```json
{
  "nombre": "Ana",
  "edad": 28,
  "direccion": {
    "calle": "Gran Vía 1",
    "ciudad": "Madrid",
    "codigo_postal": "28013"
  },
  "hobbies": ["lectura", "natación", "programación"]
}
```

#### Tipos de JSON

**1. JSON plano (flat)**
Cada registro es un objeto JSON completo:
```json
{"id": 1, "nombre": "Ana", "edad": 28}
{"id": 2, "nombre": "Carlos", "edad": 35}
```

**2. JSON nested (anidado)**
Contiene objetos dentro de objetos:
```json
{
  "usuario": {
    "id": 1,
    "perfil": {
      "nombre": "Ana",
      "edad": 28
    }
  }
}
```

**3. JSON Lines (JSONL)**
Cada línea es un JSON válido (muy común en logs y big data):
```jsonl
{"timestamp": "2025-01-01 10:00:00", "evento": "login", "usuario": "ana"}
{"timestamp": "2025-01-01 10:05:23", "evento": "compra", "usuario": "carlos"}
```

#### Lectura de JSON en Python

**JSON simple**:
```python
import json

with open('datos.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# datos es ahora un diccionario de Python
print(datos['nombre'])  # "Ana"
```

**JSON Lines**:
```python
import json

registros = []
with open('datos.jsonl', 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        registro = json.loads(linea)
        registros.append(registro)
```

**JSON nested con pandas**:
```python
import pandas as pd

# pandas puede aplanar estructuras anidadas
df = pd.read_json('datos.json')

# O normalizar JSON anidado
from pandas import json_normalize
with open('datos_nested.json') as f:
    datos = json.load(f)
df = json_normalize(datos)
```

#### Ventajas de JSON sobre CSV

- ✅ Soporta estructuras anidadas
- ✅ Tipos de datos explícitos (números, strings, booleanos, null)
- ✅ No necesita especificar delimitadores
- ✅ Estándar en APIs REST

#### Desafíos con JSON

- ⚠️ Más pesado que CSV (más caracteres)
- ⚠️ Estructuras muy anidadas son difíciles de procesar
- ⚠️ No todos los JSON son válidos (problemas de sintaxis)

---

### 1.3 Archivos Excel (.xlsx, .xls)

#### ¿Qué es Excel?

Excel es un formato binario (no texto plano) que puede contener múltiples hojas (sheets), fórmulas, estilos y gráficos.

**Analogía**: Es como un cuaderno con múltiples páginas, donde cada página puede tener tablas, notas y cálculos.

#### ¿Por qué Excel en Data Engineering?

Aunque preferimos CSV o JSON, Excel es muy común porque:
- Los usuarios de negocio lo usan constantemente
- Puede contener múltiples tablas relacionadas en diferentes hojas
- A veces incluye metadatos útiles

#### Lectura de Excel con Python

```python
import pandas as pd

# Leer la primera hoja
df = pd.read_excel('ventas.xlsx')

# Leer una hoja específica
df = pd.read_excel('ventas.xlsx', sheet_name='Enero')

# Leer todas las hojas
todas_las_hojas = pd.read_excel('ventas.xlsx', sheet_name=None)
for nombre_hoja, df in todas_las_hojas.items():
    print(f"Hoja: {nombre_hoja}, Filas: {len(df)}")
```

#### Desafíos con Excel

- ⚠️ Archivos grandes son lentos de leer
- ⚠️ Puede contener fórmulas en lugar de valores
- ⚠️ Formatos de fecha pueden ser problemáticos
- ⚠️ Necesita librería adicional (openpyxl)

#### Buenas prácticas

✅ **Especificar qué leer**:
```python
df = pd.read_excel(
    'ventas.xlsx',
    sheet_name='Enero',
    header=0,
    usecols='A:E',  # Solo columnas A a E
    skiprows=2,     # Saltar las 2 primeras filas
    nrows=100       # Leer solo 100 filas
)
```

✅ **Convertir a CSV para procesamiento masivo**:
```python
# Excel es lento, CSV es rápido
df = pd.read_excel('ventas.xlsx')
df.to_csv('ventas.csv', index=False)
# Ahora trabaja con el CSV
```

---

## Parte 2: Extracción desde APIs REST

### 2.1 ¿Qué es una API REST?

Una **API** (Application Programming Interface) es un puente que permite que dos programas se comuniquen. **REST** es un estilo de diseño de APIs que usa el protocolo HTTP (el mismo que usan los navegadores web).

**Analogía**: Una API REST es como un restaurante:
- Tú eres el cliente (tu programa)
- El menú son los endpoints disponibles
- El camarero es la API que lleva tu pedido a la cocina
- La cocina es el servidor que prepara los datos
- El plato que te trae es la respuesta JSON

#### Conceptos fundamentales

**1. Endpoint (URL)**
Es la dirección donde haces la petición:
```
https://api.ejemplo.com/v1/usuarios
```

**2. Métodos HTTP**
- **GET**: Obtener datos (el más usado en extracción)
- **POST**: Enviar datos nuevos
- **PUT**: Actualizar datos existentes
- **DELETE**: Eliminar datos

**3. Headers (Cabeceras)**
Información adicional de la petición:
```python
headers = {
    'Authorization': 'Bearer tu_token_aqui',
    'Content-Type': 'application/json',
    'User-Agent': 'MiApp/1.0'
}
```

**4. Query Parameters**
Parámetros en la URL para filtrar/personalizar:
```
https://api.ejemplo.com/v1/usuarios?edad=25&ciudad=Madrid
```

**5. Response (Respuesta)**
Los datos que devuelve la API, normalmente en JSON:
```json
{
  "status": "success",
  "data": [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Carlos"}
  ]
}
```

### 2.2 Hacer peticiones con requests

**Instalación**:
```bash
pip install requests
```

**GET simple**:
```python
import requests

response = requests.get('https://api.ejemplo.com/v1/usuarios')

# Verificar que fue exitosa (código 200)
if response.status_code == 200:
    datos = response.json()  # Convertir JSON a diccionario Python
    print(datos)
else:
    print(f"Error: {response.status_code}")
```

**GET con parámetros**:
```python
params = {
    'edad': 25,
    'ciudad': 'Madrid',
    'limit': 100
}

response = requests.get(
    'https://api.ejemplo.com/v1/usuarios',
    params=params
)
```

**GET con autenticación**:
```python
headers = {
    'Authorization': 'Bearer tu_token_secreto',
    'User-Agent': 'MiApp/1.0'
}

response = requests.get(
    'https://api.ejemplo.com/v1/usuarios',
    headers=headers
)
```

### 2.3 Autenticación en APIs

Las APIs necesitan saber quién eres para darte acceso. Los métodos más comunes:

**1. API Key (Clave de API)**
```python
headers = {'X-API-Key': 'tu_clave_aqui'}
response = requests.get(url, headers=headers)
```

**2. Bearer Token (Token de acceso)**
```python
headers = {'Authorization': 'Bearer tu_token_aqui'}
response = requests.get(url, headers=headers)
```

**3. Basic Auth (Usuario y contraseña)**
```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    url,
    auth=HTTPBasicAuth('usuario', 'contraseña')
)
```

**Regla de oro**: ¡NUNCA hardcodees las credenciales en el código! Usa variables de entorno:

```python
import os

API_KEY = os.getenv('MI_API_KEY')
if not API_KEY:
    raise ValueError("Falta la variable de entorno MI_API_KEY")

headers = {'X-API-Key': API_KEY}
```

### 2.4 Rate Limiting (Límites de uso)

Las APIs limitan cuántas peticiones puedes hacer en un periodo de tiempo para evitar sobrecarga.

**Ejemplo típico**: "100 peticiones por minuto"

Si superas el límite, recibes un error 429 (Too Many Requests).

**Cómo manejarlo**:

```python
import time
import requests

def hacer_peticion_con_rate_limit(url, peticiones_por_segundo=2):
    """Hace peticiones respetando rate limit"""
    tiempo_entre_peticiones = 1.0 / peticiones_por_segundo

    response = requests.get(url)
    time.sleep(tiempo_entre_peticiones)  # Esperar antes de la siguiente

    return response
```

**Leer el rate limit de la respuesta**:
```python
response = requests.get(url)

# Muchas APIs incluyen headers informativos
limite_restante = response.headers.get('X-RateLimit-Remaining')
tiempo_reset = response.headers.get('X-RateLimit-Reset')

print(f"Peticiones restantes: {limite_restante}")
```

### 2.5 Paginación

Las APIs no devuelven todos los datos de golpe (imagina millones de registros). Usan **paginación**.

**Tipos de paginación**:

**1. Offset/Limit (lo más común)**
```python
# Página 1: registros 0-99
response = requests.get('https://api.ejemplo.com/v1/usuarios?offset=0&limit=100')

# Página 2: registros 100-199
response = requests.get('https://api.ejemplo.com/v1/usuarios?offset=100&limit=100')
```

**2. Cursor-based**
```python
# Primera página
response = requests.get('https://api.ejemplo.com/v1/usuarios?limit=100')
datos = response.json()
cursor_siguiente = datos['next_cursor']

# Segunda página
response = requests.get(f'https://api.ejemplo.com/v1/usuarios?cursor={cursor_siguiente}&limit=100')
```

**3. Page/Per Page**
```python
response = requests.get('https://api.ejemplo.com/v1/usuarios?page=1&per_page=100')
```

**Patrón completo de paginación**:
```python
def extraer_todos_los_datos(url_base):
    """Extrae todos los datos paginados de una API"""
    todos_los_datos = []
    offset = 0
    limit = 100

    while True:
        response = requests.get(
            f"{url_base}?offset={offset}&limit={limit}"
        )
        datos = response.json()

        if not datos or len(datos) == 0:
            break  # No hay más datos

        todos_los_datos.extend(datos)
        offset += limit

        time.sleep(0.5)  # Rate limiting

    return todos_los_datos
```

### 2.6 Manejo de errores y reintentos

Las APIs pueden fallar temporalmente. Necesitas reintentos inteligentes.

**Códigos HTTP comunes**:
- `200`: OK (éxito)
- `400`: Bad Request (tu petición está mal)
- `401`: Unauthorized (falta autenticación)
- `403`: Forbidden (no tienes permiso)
- `404`: Not Found (el endpoint no existe)
- `429`: Too Many Requests (rate limit excedido)
- `500`: Internal Server Error (error del servidor)
- `503`: Service Unavailable (servicio caído temporalmente)

**Estrategia de reintentos**:

```python
import requests
import time

def hacer_peticion_con_reintentos(url, max_reintentos=3):
    """Reintenta peticiones con backoff exponencial"""

    for intento in range(max_reintentos):
        try:
            response = requests.get(url, timeout=30)

            # Si es exitoso, devolver
            if response.status_code == 200:
                return response.json()

            # Si es error del cliente (400-499), no reintentar
            if 400 <= response.status_code < 500:
                raise ValueError(f"Error del cliente: {response.status_code}")

            # Si es error del servidor (500-599), reintentar
            print(f"Intento {intento + 1} falló: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"Timeout en intento {intento + 1}")

        except requests.exceptions.ConnectionError:
            print(f"Error de conexión en intento {intento + 1}")

        # Backoff exponencial: 1s, 2s, 4s, 8s...
        tiempo_espera = 2 ** intento
        print(f"Esperando {tiempo_espera}s antes del siguiente intento")
        time.sleep(tiempo_espera)

    raise Exception(f"Falló después de {max_reintentos} intentos")
```

---

## Parte 3: Web Scraping Ético

### 3.1 ¿Qué es Web Scraping?

**Web scraping** es extraer datos de páginas web que no ofrecen una API. Es como copiar información de un libro página por página.

**Analogía**: Imagina que necesitas información de un catálogo en papel. El scraping es como leer cada página, tomar notas y organizarlas en una base de datos.

**¿Cuándo usar scraping?**
- ✅ No existe una API disponible
- ✅ La API está limitada o incompleta
- ✅ Necesitas datos públicos de sitios web

### 3.2 Ética y legalidad del scraping

**⚠️ IMPORTANTE**: No todo scraping es legal o ético.

**Reglas de oro**:

1. **Respeta robots.txt**
   - Es un archivo que indica qué se puede y no se puede scrapear
   - Ubicación: `https://ejemplo.com/robots.txt`

2. **Identifica tu User-Agent**
   - No te hagas pasar por un navegador normal
   - Incluye tu email o web para contacto

3. **Rate limiting**
   - No hagas peticiones tan rápido que sobrecargues el servidor
   - 1-2 segundos entre peticiones es razonable

4. **Términos de servicio**
   - Lee los términos del sitio web
   - Algunos prohíben explícitamente el scraping

5. **Datos personales**
   - No scrapes datos personales sensibles
   - Cumple con GDPR y leyes de privacidad

**Verificar robots.txt**:
```python
import requests

def verificar_robots_txt(url_base):
    """Verifica si el scraping está permitido"""
    robots_url = f"{url_base}/robots.txt"
    response = requests.get(robots_url)

    if response.status_code == 200:
        print("Contenido de robots.txt:")
        print(response.text)
    else:
        print("No hay robots.txt (scraping probablemente permitido)")
```

### 3.3 Beautiful Soup Basics

**Beautiful Soup** es una librería Python para parsear HTML y extraer datos.

**Instalación**:
```bash
pip install beautifulsoup4 requests
```

**Flujo básico**:
1. Hacer petición HTTP para obtener HTML
2. Parsear HTML con Beautiful Soup
3. Buscar elementos específicos (tablas, divs, etc.)
4. Extraer texto o atributos
5. Guardar datos estructurados

**Ejemplo simple**:
```python
import requests
from bs4 import BeautifulSoup

# 1. Obtener HTML
url = 'https://ejemplo.com/productos'
headers = {
    'User-Agent': 'MiScraper/1.0 (contacto@ejemplo.com)'
}
response = requests.get(url, headers=headers)

# 2. Parsear HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 3. Buscar elementos
productos = soup.find_all('div', class_='producto')

# 4. Extraer datos
for producto in productos:
    nombre = producto.find('h2', class_='nombre').text.strip()
    precio = producto.find('span', class_='precio').text.strip()
    print(f"{nombre}: {precio}")
```

**Selectores comunes**:
```python
# Por etiqueta
soup.find('h1')
soup.find_all('p')

# Por clase CSS
soup.find('div', class_='contenido')

# Por ID
soup.find('div', id='principal')

# Por atributo
soup.find('a', href='https://ejemplo.com')

# Selector CSS
soup.select('div.producto > h2')
```

**Extraer texto y atributos**:
```python
elemento = soup.find('a', class_='link')

# Texto
texto = elemento.text.strip()

# Atributo
url = elemento['href']
titulo = elemento.get('title', 'Sin título')
```

### 3.4 Scraping de tablas HTML

Las tablas son la estructura más común para datos estructurados en HTML.

```python
import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://ejemplo.com/tabla'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar tabla
tabla = soup.find('table', class_='datos')

# Opción 1: Manual
filas = tabla.find_all('tr')
datos = []
for fila in filas[1:]:  # Saltar header
    celdas = fila.find_all('td')
    datos.append([celda.text.strip() for celda in celdas])

# Opción 2: Con pandas (más fácil)
df = pd.read_html(str(tabla))[0]
print(df)
```

### 3.5 Manejo de contenido dinámico (JavaScript)

Algunos sitios usan JavaScript para cargar contenido. Beautiful Soup solo ve el HTML inicial.

**Soluciones**:

1. **Buscar API oculta** (recomendado)
   - Usa las DevTools del navegador (F12)
   - Pestaña Network → XHR/Fetch
   - Busca peticiones JSON que carguen los datos
   - Usa esa API directamente

2. **Selenium** (último recurso)
   - Controla un navegador real
   - Lento y pesado
   ```python
   from selenium import webdriver

   driver = webdriver.Chrome()
   driver.get('https://ejemplo.com')
   time.sleep(3)  # Esperar carga de JS
   html = driver.page_source
   soup = BeautifulSoup(html, 'html.parser')
   ```

---

## Parte 4: Logging y Monitoreo de Extracción

### 4.1 ¿Por qué logging en extracción?

Cuando extraes datos de múltiples fuentes, necesitas:
- Saber si la extracción fue exitosa
- Registrar errores para debug
- Medir tiempos de ejecución
- Auditar qué datos se extrajeron

**Ejemplo de log completo**:
```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/extraccion.log'),
        logging.StreamHandler()  # También en consola
    ]
)

logger = logging.getLogger(__name__)

def extraer_datos_api(url):
    """Extrae datos con logging completo"""
    inicio = datetime.now()
    logger.info(f"Iniciando extracción desde {url}")

    try:
        response = requests.get(url, timeout=30)
        datos = response.json()

        duracion = (datetime.now() - inicio).total_seconds()
        logger.info(f"Extracción exitosa: {len(datos)} registros en {duracion}s")

        return datos

    except Exception as e:
        logger.error(f"Error en extracción: {str(e)}")
        raise
```

### 4.2 Métricas importantes

**Registra siempre**:
- Timestamp de inicio y fin
- Fuente de datos (URL, archivo, etc.)
- Cantidad de registros extraídos
- Tiempo de ejecución
- Errores y excepciones
- Reintentos realizados

---

## Parte 5: Errores Comunes y Cómo Evitarlos

### Error 1: No validar encoding en CSV

**Problema**: Intentas leer un CSV con UTF-8 pero está en Latin-1.

**Síntoma**: UnicodeDecodeError o caracteres raros (�).

**Solución**:
```python
import chardet

# Detectar encoding automáticamente
with open('datos.csv', 'rb') as f:
    resultado = chardet.detect(f.read())
    encoding = resultado['encoding']

# Usar el encoding detectado
df = pd.read_csv('datos.csv', encoding=encoding)
```

### Error 2: No manejar rate limits en APIs

**Problema**: Haces 1000 peticiones por segundo, la API te bloquea.

**Síntoma**: Error 429 (Too Many Requests).

**Solución**:
```python
import time

for i in range(100):
    response = requests.get(url)
    time.sleep(1)  # 1 segundo entre peticiones
```

### Error 3: No identificarte en web scraping

**Problema**: Usas el User-Agent por defecto de requests.

**Síntoma**: El sitio te bloquea o devuelve contenido diferente.

**Solución**:
```python
headers = {
    'User-Agent': 'MiScraper/1.0 (contacto@ejemplo.com)'
}
response = requests.get(url, headers=headers)
```

### Error 4: No manejar reintentos en APIs inestables

**Problema**: La API falla temporalmente y tu script explota.

**Síntoma**: ConnectionError o Timeout sin reintentos.

**Solución**: Usar la función `hacer_peticion_con_reintentos()` mostrada anteriormente.

### Error 5: Hardcodear credenciales

**Problema**: Guardas API keys en el código:
```python
API_KEY = "sk_live_1234567890abcdef"  # ❌ NUNCA HAGAS ESTO
```

**Síntoma**: Credenciales expuestas en GitHub, riesgo de seguridad.

**Solución**:
```python
import os
API_KEY = os.getenv('MI_API_KEY')  # ✅ Usar variables de entorno
```

---

## Checklist de Aprendizaje

Al terminar este tema, deberías poder:

- [ ] Leer archivos CSV con diferentes encodings y delimitadores
- [ ] Procesar JSON simple, nested y JSON Lines
- [ ] Leer archivos Excel con múltiples hojas
- [ ] Hacer peticiones GET a APIs REST
- [ ] Autenticarte en APIs con API keys y tokens
- [ ] Implementar paginación para obtener todos los datos
- [ ] Manejar rate limits y reintentos
- [ ] Verificar robots.txt antes de hacer scraping
- [ ] Extraer datos de HTML con Beautiful Soup
- [ ] Scrapear tablas HTML
- [ ] Implementar logging en tus scripts de extracción
- [ ] Manejar errores de encoding, timeouts y conexión

---

## Recursos Adicionales

### Librerías Python
- **requests**: https://requests.readthedocs.io/
- **pandas**: https://pandas.pydata.org/docs/
- **beautifulsoup4**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **chardet**: https://chardet.readthedocs.io/

### APIs públicas para practicar
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/ (API de prueba)
- **OpenWeatherMap**: https://openweathermap.org/api (clima)
- **REST Countries**: https://restcountries.com/ (datos de países)

### Scraping ético
- **robots.txt checker**: https://en.ryte.com/free-tools/robots-txt/
- **Términos de servicio**: Lee siempre antes de scrapear

### Lecturas recomendadas
- "Web Scraping with Python" - Ryan Mitchell
- Documentación oficial de requests y Beautiful Soup

---

**¡Felicidades!** Has completado la teoría de extracción de datos. Ahora estás listo para ver ejemplos prácticos y hacer ejercicios.

**Próximo paso**: `02-EJEMPLOS.md` donde verás 5 casos reales de extracción de datos.
