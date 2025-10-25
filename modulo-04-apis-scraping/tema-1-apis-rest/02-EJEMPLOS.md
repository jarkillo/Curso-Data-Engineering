# Tema 1: APIs REST - Ejemplos Trabajados

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📚 Introducción

En este documento encontrarás **5 ejemplos completos** de cómo consumir APIs REST con Python. Cada ejemplo está trabajado paso a paso con código ejecutable y explicaciones detalladas.

**Empresa ficticia:** DataHub Inc. - Empresa de consultoría en Data Engineering
**Contexto:** Eres un Data Engineer trabajando en diferentes proyectos de extracción de datos.

**Progresión de dificultad:**
- 📗 **Ejemplos 1-2:** Básico (principiantes)
- 📙 **Ejemplos 3-4:** Intermedio (con experiencia)
- 📕 **Ejemplo 5:** Avanzado (manejo robusto de errores)

---

## 📗 Ejemplo 1: GET Request Básico a API Pública

**Nivel:** Básico
**Duración:** 10-15 minutos
**Objetivo:** Aprender a hacer tu primer GET request y explorar la respuesta

### Contexto Empresarial

Tu jefe en DataHub Inc. te pide hacer un prototipo rápido para probar la API de JSONPlaceholder (una API pública de testing) antes de integrarla en un proyecto real.

**Requerimiento:** Obtener la lista de usuarios y mostrar sus datos básicos.

---

### Paso 1: Entender la API

**API a usar:** [JSONPlaceholder](https://jsonplaceholder.typicode.com/)

**Endpoint:** `GET https://jsonplaceholder.typicode.com/users`

**Características:**
- ✅ API gratuita y pública
- ✅ No requiere autenticación
- ✅ Devuelve datos ficticios para testing
- ✅ Siempre disponible (alta confiabilidad)

---

### Paso 2: Hacer el Request Simple

**Código:**

```python
import requests

# URL del endpoint
url = "https://jsonplaceholder.typicode.com/users"

# Hacer GET request
response = requests.get(url)

# Mostrar información básica
print(f"Status Code: {response.status_code}")
print(f"Tipo de contenido: {response.headers['Content-Type']}")
print(f"Tiempo de respuesta: {response.elapsed.total_seconds()} segundos")
```

**Salida esperada:**
```
Status Code: 200
Tipo de contenido: application/json; charset=utf-8
Tiempo de respuesta: 0.234 segundos
```

**Interpretación:**
- **200:** ✅ Éxito - El servidor respondió correctamente
- **application/json:** La respuesta está en formato JSON
- **0.234 segundos:** Tiempo que tardó la API en responder

---

### Paso 3: Parsear y Explorar el JSON

```python
import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

# Convertir respuesta a JSON (dict/list de Python)
usuarios = response.json()

# Ver cuántos usuarios hay
print(f"Total de usuarios: {len(usuarios)}")

# Mostrar el primer usuario completo
print("\n=== Primer Usuario ===")
import json
print(json.dumps(usuarios[0], indent=2, ensure_ascii=False))
```

**Salida esperada:**
```
Total de usuarios: 10

=== Primer Usuario ===
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-network",
    "bs": "harness real-time e-markets"
  }
}
```

**Observaciones:**
- La API devuelve una **lista** de usuarios (array en JSON)
- Cada usuario es un **diccionario** con múltiples campos
- Los datos están **anidados** (address dentro de usuario, geo dentro de address)

---

### Paso 4: Extraer Campos Específicos

En la vida real, rara vez necesitas todos los campos. Vamos a extraer solo lo importante:

```python
import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    usuarios = response.json()

    print("=== Usuarios de JSONPlaceholder ===\n")

    for usuario in usuarios:
        print(f"ID: {usuario['id']}")
        print(f"Nombre: {usuario['name']}")
        print(f"Email: {usuario['email']}")
        print(f"Ciudad: {usuario['address']['city']}")
        print(f"Empresa: {usuario['company']['name']}")
        print("-" * 50)
else:
    print(f"Error: Status code {response.status_code}")
```

**Salida esperada:**
```
=== Usuarios de JSONPlaceholder ===

ID: 1
Nombre: Leanne Graham
Email: Sincere@april.biz
Ciudad: Gwenborough
Empresa: Romaguera-Crona
--------------------------------------------------
ID: 2
Nombre: Ervin Howell
Email: Shanna@melissa.tv
Ciudad: Wisokyburgh
Empresa: Deckow-Crist
--------------------------------------------------
...
```

---

### Paso 5: Guardar en CSV para Análisis

Como Data Engineer, querrás guardar estos datos para procesamiento posterior:

```python
import requests
import csv

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    usuarios = response.json()

    # Guardar en CSV
    with open("usuarios_jsonplaceholder.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["id", "nombre", "email", "ciudad", "empresa"])

        # Datos
        for usuario in usuarios:
            writer.writerow([
                usuario["id"],
                usuario["name"],
                usuario["email"],
                usuario["address"]["city"],
                usuario["company"]["name"]
            ])

    print(f"✅ {len(usuarios)} usuarios guardados en usuarios_jsonplaceholder.csv")
else:
    print(f"❌ Error: Status code {response.status_code}")
```

**Archivo generado:** `usuarios_jsonplaceholder.csv`

```csv
id,nombre,email,ciudad,empresa
1,Leanne Graham,Sincere@april.biz,Gwenborough,Romaguera-Crona
2,Ervin Howell,Shanna@melissa.tv,Wisokyburgh,Deckow-Crist
...
```

---

### 💡 Lecciones Aprendidas

1. ✅ **GET requests son simples:** Solo necesitas la URL
2. ✅ **Siempre valida status code:** Verifica que sea 200 antes de procesar
3. ✅ **`.json()` parsea automáticamente:** Convierte JSON a Python dict/list
4. ✅ **Datos anidados:** Usa notación de corchetes para acceder (`usuario['address']['city']`)
5. ✅ **Guarda para procesamiento:** CSV es un formato universal para análisis

---

## 📗 Ejemplo 2: Autenticación con API Key

**Nivel:** Básico
**Duración:** 15-20 minutos
**Objetivo:** Aprender a autenticarte con una API usando API Key

### Contexto Empresarial

DataHub Inc. tiene un cliente que necesita datos del clima en tiempo real para optimizar sus operaciones logísticas. Te asignan integrar la API de OpenWeather.

**Requerimiento:** Obtener el clima actual de varias ciudades españolas.

---

### Paso 1: Obtener tu API Key

**API a usar:** [OpenWeather API](https://openweathermap.org/api)

**Pasos para obtener la clave:**
1. Ve a https://openweathermap.org/api
2. Crea una cuenta gratuita
3. Ve a "API keys" en tu perfil
4. Copia tu API key (ej: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Plan gratuito:**
- ✅ 1,000 requests/día
- ✅ Datos actuales del clima
- ⚠️ Actualización cada 2 horas

---

### Paso 2: Configurar la API Key de Forma Segura

**❌ NUNCA hagas esto:**
```python
API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"  # ¡MAL! Hardcodeada
```

**✅ Forma correcta (con variable de entorno):**

**En tu terminal (Windows PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

**En tu código Python:**
```python
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("❌ ERROR: Variable de entorno OPENWEATHER_API_KEY no configurada")

print(f"✅ API Key cargada (primeros 8 caracteres): {API_KEY[:8]}...")
```

**Salida:**
```
✅ API Key cargada (primeros 8 caracteres): a1b2c3d4...
```

---

### Paso 3: Hacer Request con Autenticación

```python
import os
import requests

# Cargar API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# URL base de la API
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Ciudad a consultar
ciudad = "Madrid"

# Parámetros del request (incluye la API key)
params = {
    "q": ciudad,
    "appid": API_KEY,  # Autenticación
    "units": "metric",  # Celsius
    "lang": "es"  # Español
}

# Hacer request
response = requests.get(base_url, params=params)

print(f"Status Code: {response.status_code}")
print(f"URL completa: {response.url}")
```

**Salida:**
```
Status Code: 200
URL completa: https://api.openweathermap.org/data/2.5/weather?q=Madrid&appid=a1b2c3d4...&units=metric&lang=es
```

**Nota:** La URL incluye la API key como query parameter (`appid=...`)

---

### Paso 4: Manejar Error 401 (No Autenticado)

¿Qué pasa si la API key es incorrecta?

```python
import os
import requests

API_KEY = "clave_incorrecta_123"  # ⚠️ API key inválida a propósito

base_url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "Madrid",
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(base_url, params=params)

print(f"Status Code: {response.status_code}")

if response.status_code == 401:
    print("❌ ERROR 401: No autenticado")
    print("Mensaje del servidor:")
    print(response.json())
```

**Salida:**
```
Status Code: 401
❌ ERROR 401: No autenticado
Mensaje del servidor:
{
  'cod': 401,
  'message': 'Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.'
}
```

**💡 Lección:** Siempre valida que tu API key sea correcta antes de hacer múltiples requests.

---

### Paso 5: Parsear Datos del Clima

```python
import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Lista de ciudades a consultar
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]

print("=== Clima en Tiempo Real ===\n")

for ciudad in ciudades:
    params = {
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        datos = response.json()

        print(f"📍 {datos['name']}")
        print(f"   Temperatura: {datos['main']['temp']}°C")
        print(f"   Sensación térmica: {datos['main']['feels_like']}°C")
        print(f"   Humedad: {datos['main']['humidity']}%")
        print(f"   Descripción: {datos['weather'][0]['description'].capitalize()}")
        print(f"   Viento: {datos['wind']['speed']} m/s")
        print()
    elif response.status_code == 401:
        print(f"❌ Error 401: API key inválida")
        break
    elif response.status_code == 404:
        print(f"❌ Ciudad '{ciudad}' no encontrada")
    else:
        print(f"❌ Error {response.status_code} al consultar {ciudad}")
```

**Salida esperada:**
```
=== Clima en Tiempo Real ===

📍 Madrid
   Temperatura: 18.5°C
   Sensación térmica: 17.8°C
   Humedad: 65%
   Descripción: Cielo despejado
   Viento: 3.2 m/s

📍 Barcelona
   Temperatura: 21.3°C
   Sensación térmica: 20.9°C
   Humedad: 72%
   Descripción: Nubes dispersas
   Viento: 4.1 m/s

...
```

---

### 💡 Lecciones Aprendidas

1. ✅ **API Key en variable de entorno:** Nunca hardcodees credenciales
2. ✅ **Valida status codes:** 401 = problema de autenticación
3. ✅ **Query parameters:** La API key se pasa como parámetro (`appid=...`)
4. ✅ **Maneja múltiples ciudades:** Itera y llama la API para cada una
5. ✅ **Datos anidados:** `datos['main']['temp']` para acceder a temperatura

---

## 📙 Ejemplo 3: POST Request para Crear Recursos

**Nivel:** Intermedio
**Duración:** 20-25 minutos
**Objetivo:** Aprender a crear recursos con POST requests

### Contexto Empresarial

DataHub Inc. está desarrollando un sistema de gestión de tareas para un cliente. Necesitas implementar la funcionalidad de crear nuevas tareas mediante la API.

**Requerimiento:** Crear tareas de prueba usando la API de JSONPlaceholder.

---

### Paso 1: Entender la Diferencia entre GET y POST

**GET (Leer):**
- No modifica datos en el servidor
- No tiene body (solo URL y query params)
- Idempotente (puedes llamarlo 100 veces sin problemas)

**POST (Crear):**
- Crea un **nuevo recurso** en el servidor
- Tiene **body** con los datos del nuevo recurso
- **NO idempotente** (llamarlo 5 veces crea 5 recursos)

---

### Paso 2: POST Request Básico

```python
import requests
import json

# URL del endpoint
url = "https://jsonplaceholder.typicode.com/posts"

# Datos de la nueva tarea (body del request)
nueva_tarea = {
    "title": "Implementar extracción de datos de API",
    "body": "Crear script Python que extraiga datos de la API de clima cada hora",
    "userId": 1
}

# Hacer POST request
response = requests.post(
    url,
    json=nueva_tarea  # requests convierte el dict a JSON automáticamente
)

print(f"Status Code: {response.status_code}")
print(f"\nRecurso creado:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

**Salida esperada:**
```
Status Code: 201

Recurso creado:
{
  "title": "Implementar extracción de datos de API",
  "body": "Crear script Python que extraiga datos de la API de clima cada hora",
  "userId": 1,
  "id": 101
}
```

**Observaciones:**
- **Status 201 Created:** Indica que el recurso fue creado exitosamente
- **ID asignado:** El servidor asignó `id: 101` automáticamente
- **Body devuelto:** El servidor devuelve el recurso completo (con el ID)

---

### Paso 3: Diferencia entre `json=` y `data=`

**Opción 1: `json=` (RECOMENDADO para APIs REST)**

```python
import requests

nueva_tarea = {"title": "Tarea 1", "userId": 1}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=nueva_tarea  # ✅ Convierte a JSON automáticamente
)

print(f"Content-Type enviado: {response.request.headers['Content-Type']}")
# application/json
```

**Qué hace `json=`:**
1. Convierte el dict a string JSON
2. Añade el header `Content-Type: application/json`
3. Envía el body como JSON

---

**Opción 2: `data=` (para form data, NO para APIs REST)**

```python
import requests

nueva_tarea = {"title": "Tarea 1", "userId": 1}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    data=nueva_tarea  # ⚠️ Envía como form-urlencoded
)

print(f"Content-Type enviado: {response.request.headers['Content-Type']}")
# application/x-www-form-urlencoded
```

**Qué hace `data=`:**
1. Envía como `key1=value1&key2=value2`
2. Añade el header `Content-Type: application/x-www-form-urlencoded`
3. Usado para formularios HTML, NO para APIs REST

**💡 Regla de oro:** Usa `json=` para APIs REST, `data=` para formularios web.

---

### Paso 4: Validar Status Code 201

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

nueva_tarea = {
    "title": "Configurar pipeline de datos",
    "body": "Diseñar y implementar pipeline ETL con Airflow",
    "userId": 1
}

response = requests.post(url, json=nueva_tarea)

# Validar que fue creado exitosamente
if response.status_code == 201:
    tarea_creada = response.json()
    print(f"✅ Tarea creada exitosamente")
    print(f"   ID asignado: {tarea_creada['id']}")
    print(f"   Título: {tarea_creada['title']}")
elif response.status_code == 400:
    print(f"❌ Error 400: Request malformado")
    print(f"   Detalles: {response.json()}")
elif response.status_code == 401:
    print(f"❌ Error 401: No autenticado")
else:
    print(f"❌ Error inesperado: {response.status_code}")
```

**Salida:**
```
✅ Tarea creada exitosamente
   ID asignado: 101
   Título: Configurar pipeline de datos
```

---

### Paso 5: Crear Múltiples Recursos

```python
import requests
import time

url = "https://jsonplaceholder.typicode.com/posts"

# Lista de tareas a crear
tareas = [
    {
        "title": "Extracción de datos de API de clima",
        "body": "Implementar script que extraiga datos horarios",
        "userId": 1
    },
    {
        "title": "Limpieza de datos con Pandas",
        "body": "Eliminar duplicados y valores nulos",
        "userId": 1
    },
    {
        "title": "Carga en Data Warehouse",
        "body": "Cargar datos procesados en Snowflake",
        "userId": 1
    }
]

print("=== Creando Tareas ===\n")

ids_creados = []

for i, tarea in enumerate(tareas, 1):
    response = requests.post(url, json=tarea)

    if response.status_code == 201:
        tarea_creada = response.json()
        ids_creados.append(tarea_creada['id'])
        print(f"✅ Tarea {i}/{len(tareas)}: ID {tarea_creada['id']} - {tarea_creada['title']}")
    else:
        print(f"❌ Error al crear tarea {i}: Status {response.status_code}")

    # Esperar 0.5 segundos entre requests (respeto al servidor)
    time.sleep(0.5)

print(f"\n📊 Resumen: {len(ids_creados)} tareas creadas")
print(f"   IDs: {ids_creados}")
```

**Salida:**
```
=== Creando Tareas ===

✅ Tarea 1/3: ID 101 - Extracción de datos de API de clima
✅ Tarea 2/3: ID 102 - Limpieza de datos con Pandas
✅ Tarea 3/3: ID 103 - Carga en Data Warehouse

📊 Resumen: 3 tareas creadas
   IDs: [101, 102, 103]
```

---

### 💡 Lecciones Aprendidas

1. ✅ **POST crea recursos:** Status 201 indica éxito
2. ✅ **Usa `json=`** para APIs REST (no `data=`)
3. ✅ **El servidor asigna el ID:** No lo envíes en el body
4. ✅ **Valida status codes:** 201=creado, 400=mal request, 401=no autenticado
5. ✅ **Respeta rate limiting:** Añade delays entre múltiples requests

---

## 📙 Ejemplo 4: Paginación Automática

**Nivel:** Intermedio
**Duración:** 25-30 minutos
**Objetivo:** Iterar automáticamente todas las páginas de una API

### Contexto Empresarial

DataHub Inc. necesita extraer **todos** los posts de JSONPlaceholder para análisis. La API devuelve 10 posts por página, y hay 100 posts en total. Necesitas implementar paginación automática.

**Requerimiento:** Descargar los 100 posts iterando las páginas automáticamente.

---

### Paso 1: Entender la Paginación de la API

**Endpoint:** `GET https://jsonplaceholder.typicode.com/posts`

**Parámetros de paginación:**
- `_page`: Número de página (1, 2, 3...)
- `_limit`: Posts por página (default: 10)

**Ejemplos:**
```
# Página 1 (posts 1-10)
GET /posts?_page=1&_limit=10

# Página 2 (posts 11-20)
GET /posts?_page=2&_limit=10

# Página 3 (posts 21-30)
GET /posts?_page=3&_limit=10
```

---

### Paso 2: Paginar Manualmente (3 Páginas)

```python
import requests

base_url = "https://jsonplaceholder.typicode.com/posts"

todos_posts = []

# Iterar manualmente 3 páginas
for pagina in range(1, 4):  # 1, 2, 3
    params = {
        "_page": pagina,
        "_limit": 10
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        posts = response.json()
        todos_posts.extend(posts)
        print(f"✅ Página {pagina}: {len(posts)} posts descargados")
    else:
        print(f"❌ Error en página {pagina}: Status {response.status_code}")

print(f"\n📊 Total descargado: {len(todos_posts)} posts")
```

**Salida:**
```
✅ Página 1: 10 posts descargados
✅ Página 2: 10 posts descargados
✅ Página 3: 10 posts descargados

📊 Total descargado: 30 posts
```

**Problema:** ¿Cómo saber cuántas páginas hay sin hardcodear el número?

---

### Paso 3: Paginar Automáticamente (Todas las Páginas)

```python
import requests

base_url = "https://jsonplaceholder.typicode.com/posts"

todos_posts = []
pagina = 1
limite_por_pagina = 10

print("=== Paginación Automática ===\n")

while True:
    params = {
        "_page": pagina,
        "_limit": limite_por_pagina
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        posts = response.json()

        # Si no hay más posts, salir del loop
        if not posts:
            print(f"✅ No hay más posts. Paginación completa.")
            break

        todos_posts.extend(posts)
        print(f"✅ Página {pagina}: {len(posts)} posts descargados")

        pagina += 1  # Siguiente página
    else:
        print(f"❌ Error: Status {response.status_code}")
        break

print(f"\n📊 Resumen:")
print(f"   Total páginas: {pagina - 1}")
print(f"   Total posts: {len(todos_posts)}")
```

**Salida:**
```
=== Paginación Automática ===

✅ Página 1: 10 posts descargados
✅ Página 2: 10 posts descargados
✅ Página 3: 10 posts descargados
✅ Página 4: 10 posts descargados
✅ Página 5: 10 posts descargados
✅ Página 6: 10 posts descargados
✅ Página 7: 10 posts descargados
✅ Página 8: 10 posts descargados
✅ Página 9: 10 posts descargados
✅ Página 10: 10 posts descargados
✅ No hay más posts. Paginación completa.

📊 Resumen:
   Total páginas: 10
   Total posts: 100
```

**Lógica:**
1. Empieza en página 1
2. Haz request
3. Si la respuesta está vacía (`not posts`), termina
4. Si hay datos, guárdalos e incrementa el número de página
5. Repite hasta que no haya más datos

---

### Paso 4: Usar Función del Proyecto Práctico

Reutilicemos la función `paginar_offset_limit()` del proyecto práctico:

```python
import requests

def paginar_offset_limit(url, limite_por_pagina=100, max_paginas=None):
    """
    Itera automáticamente todas las páginas usando Offset/Limit.

    Args:
        url: URL base del endpoint
        limite_por_pagina: Elementos por página (default: 100)
        max_paginas: Límite de páginas a iterar (None = sin límite)

    Returns:
        Lista con todos los elementos de todas las páginas
    """
    todos_elementos = []
    offset = 0
    pagina_actual = 1

    while True:
        # Construir parámetros
        params = {"_start": offset, "_limit": limite_por_pagina}

        # Hacer request
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")

        elementos = response.json()

        # Si no hay más elementos, terminar
        if not elementos:
            break

        todos_elementos.extend(elementos)
        print(f"✅ Página {pagina_actual}: {len(elementos)} elementos")

        # Actualizar para siguiente página
        offset += limite_por_pagina
        pagina_actual += 1

        # Verificar límite de páginas
        if max_paginas and pagina_actual > max_paginas:
            print(f"⚠️  Límite de {max_paginas} páginas alcanzado")
            break

    return todos_elementos


# Usar la función
url = "https://jsonplaceholder.typicode.com/posts"
posts = paginar_offset_limit(url, limite_por_pagina=10)

print(f"\n📊 Total posts descargados: {len(posts)}")
```

**Salida:**
```
✅ Página 1: 10 elementos
✅ Página 2: 10 elementos
...
✅ Página 10: 10 elementos

📊 Total posts descargados: 100
```

---

### Paso 5: Análisis de Eficiencia

**Comparación:**

**Sin paginación (1 request gigante):**
```python
# Intentar obtener todos los posts en 1 request
response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = response.json()

# Problema: ¿Qué pasa si hay 10,000 posts?
# - Request muy lento (muchos segundos)
# - Puede fallar por timeout
# - Consume mucha memoria
```

**Con paginación (10 requests pequeños):**
```python
# 10 requests de 10 posts cada uno
posts = paginar_offset_limit(url, limite_por_pagina=10)

# Ventajas:
# - ✅ Cada request es rápido (<0.5 seg)
# - ✅ Procesas datos incrementalmente
# - ✅ Puedes reintentar páginas individuales si fallan
# - ✅ No explotas la memoria
```

**Análisis:**

| Métrica                    | Sin Paginación | Con Paginación (10 págs) |
| -------------------------- | -------------- | ------------------------ |
| **Número de requests**     | 1              | 10                       |
| **Tiempo por request**     | 5 segundos     | 0.5 segundos             |
| **Tiempo total**           | 5 segundos     | 5 segundos (paralelo)    |
| **Memoria usada**          | 10 MB          | 1 MB por página          |
| **Recuperable de errores** | ❌ No           | ✅ Sí (reintenta páginas) |

**💡 Conclusión:** La paginación es **obligatoria** para APIs con muchos datos.

---

### 💡 Lecciones Aprendidas

1. ✅ **Paginación es esencial:** No cargues todo en un request
2. ✅ **Loop hasta que no haya más datos:** `while True` + `if not datos: break`
3. ✅ **Reutiliza funciones:** El proyecto práctico tiene `paginar_offset_limit()`
4. ✅ **Eficiencia:** 10 requests pequeños > 1 request gigante
5. ✅ **Robustez:** Puedes reintentar páginas individuales si fallan

---

## 📕 Ejemplo 5: Reintentos ante Errores Temporales

**Nivel:** Avanzado
**Duración:** 30-35 minutos
**Objetivo:** Implementar reintentos inteligentes con exponential backoff

### Contexto Empresarial

DataHub Inc. está extrayendo datos de una API externa que a veces falla con errores 503 (servidor sobrecargado). Tu jefe te pide implementar un sistema robusto que reintente automáticamente sin sobrecargar más el servidor.

**Requerimiento:** Sistema de reintentos con exponential backoff para APIs inestables.

---

### Paso 1: Simular API Inestable

Primero, vamos a entender qué errores pueden ocurrir:

```python
import requests

# API que a veces falla
url = "https://httpstat.us/503"  # Simula un error 503

response = requests.get(url)
print(f"Status Code: {response.status_code}")
print(f"Texto: {response.text}")
```

**Salida:**
```
Status Code: 503
Texto: 503 Service Unavailable
```

**Errores comunes en APIs:**
- **500** Internal Server Error (bug en su código)
- **502** Bad Gateway (problema de red intermedio)
- **503** Service Unavailable (servidor sobrecargado)
- **504** Gateway Timeout (request tardó demasiado)
- **429** Too Many Requests (superaste rate limit)

**Todos estos son temporales y se pueden reintentar.**

---

### Paso 2: Reintentos Simples (Sin Backoff)

```python
import requests
import time

url = "https://httpstat.us/503"  # Simula error 503

max_intentos = 3

for intento in range(1, max_intentos + 1):
    print(f"Intento {intento}/{max_intentos}...")

    response = requests.get(url)

    if response.status_code == 200:
        print("✅ Éxito!")
        break
    elif response.status_code in [500, 502, 503, 504, 429]:
        print(f"❌ Error temporal {response.status_code}")

        if intento < max_intentos:
            print("   Reintentando en 2 segundos...")
            time.sleep(2)  # Espera fija
    else:
        print(f"❌ Error permanente {response.status_code} - No reintentar")
        break
```

**Salida:**
```
Intento 1/3...
❌ Error temporal 503
   Reintentando en 2 segundos...
Intento 2/3...
❌ Error temporal 503
   Reintentando en 2 segundos...
Intento 3/3...
❌ Error temporal 503
```

**Problema:** Espera siempre 2 segundos. Si el servidor está muy sobrecargado, 2 segundos no son suficientes.

---

### Paso 3: Exponential Backoff (Espera Inteligente)

**Concepto:** Espera cada vez **más tiempo** entre reintentos:
- Intento 1: Falla → Espera 2 segundos
- Intento 2: Falla → Espera 4 segundos
- Intento 3: Falla → Espera 8 segundos
- Intento 4: Falla → Espera 16 segundos

**Fórmula:** `delay = base^intento` (ej: `2^1 = 2`, `2^2 = 4`, `2^3 = 8`)

```python
import requests
import time

def hacer_request_con_reintentos(url, max_intentos=3):
    """
    Hace request con reintentos exponenciales.

    Args:
        url: URL del endpoint
        max_intentos: Máximo número de reintentos

    Returns:
        Response exitoso o lanza excepción
    """
    for intento in range(1, max_intentos + 1):
        print(f"\n🔄 Intento {intento}/{max_intentos}...")

        try:
            response = requests.get(url, timeout=30)

            # Éxito
            if response.status_code == 200:
                print("✅ Éxito!")
                return response

            # Error temporal (reintentar)
            if response.status_code in [500, 502, 503, 504, 429]:
                if intento < max_intentos:
                    delay = 2 ** intento  # Exponential backoff
                    print(f"❌ Error {response.status_code} - Esperando {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise RuntimeError(f"Falló después de {max_intentos} intentos")

            # Error permanente (no reintentar)
            if 400 <= response.status_code < 500:
                raise ValueError(f"Error permanente {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"⏱️  Timeout - Esperando {delay}s...")
                time.sleep(delay)
                continue
            else:
                raise RuntimeError("Timeout después de múltiples reintentos")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error de conexión: {e}")

    raise RuntimeError(f"Falló después de {max_intentos} intentos")


# Probar con API que simula 503
url = "https://httpstat.us/503"

try:
    response = hacer_request_con_reintentos(url, max_intentos=3)
    print(f"\nRespuesta: {response.text}")
except Exception as e:
    print(f"\n❌ Error final: {e}")
```

**Salida:**
```
🔄 Intento 1/3...
❌ Error 503 - Esperando 2s...

🔄 Intento 2/3...
❌ Error 503 - Esperando 4s...

🔄 Intento 3/3...

❌ Error final: Falló después de 3 intentos
```

**Ventaja:** Si el servidor se recupera en el intento 2, ahorraste 4 segundos de espera.

---

### Paso 4: Integrar con API Real

```python
import requests
import time

def hacer_request_con_reintentos(url, max_intentos=3):
    """Versión completa con logging detallado."""
    for intento in range(1, max_intentos + 1):
        print(f"\n{'='*50}")
        print(f"🔄 Intento {intento}/{max_intentos}")
        print(f"   URL: {url}")

        try:
            inicio = time.time()
            response = requests.get(url, timeout=30)
            duracion = time.time() - inicio

            print(f"   Status: {response.status_code}")
            print(f"   Tiempo: {duracion:.2f}s")

            if response.status_code == 200:
                print("   ✅ Éxito")
                return response

            if response.status_code in [500, 502, 503, 504, 429]:
                if intento < max_intentos:
                    delay = 2 ** intento
                    print(f"   ❌ Error temporal {response.status_code}")
                    print(f"   ⏳ Esperando {delay}s antes del siguiente intento...")
                    time.sleep(delay)
                    continue

            if 400 <= response.status_code < 500:
                print(f"   ❌ Error permanente {response.status_code}")
                raise ValueError(f"Error del cliente: {response.text[:200]}")

        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout ({30}s)")
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"   ⏳ Esperando {delay}s...")
                time.sleep(delay)
                continue

        except requests.exceptions.ConnectionError:
            print(f"   ❌ Error de conexión")
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"   ⏳ Esperando {delay}s...")
                time.sleep(delay)
                continue

    raise RuntimeError(f"Falló después de {max_intentos} intentos")


# Probar con API real (JSONPlaceholder)
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = hacer_request_con_reintentos(url, max_intentos=3)
    post = response.json()
    print(f"\n✅ Post obtenido:")
    print(f"   ID: {post['id']}")
    print(f"   Título: {post['title']}")
except Exception as e:
    print(f"\n❌ Error final: {e}")
```

**Salida (caso exitoso):**
```
==================================================
🔄 Intento 1/3
   URL: https://jsonplaceholder.typicode.com/posts/1
   Status: 200
   Tiempo: 0.23s
   ✅ Éxito

✅ Post obtenido:
   ID: 1
   Título: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

---

### Paso 5: Versión Productiva Reutilizable

Esta es la función que usarías en producción:

```python
import requests
import time
from typing import Optional

def reintentar_con_backoff(
    url: str,
    metodo: str = "GET",
    max_intentos: int = 3,
    timeout: int = 30,
    json: Optional[dict] = None,
    headers: Optional[dict] = None,
    params: Optional[dict] = None
):
    """
    Hace request HTTP con reintentos automáticos usando exponential backoff.

    Args:
        url: URL del endpoint
        metodo: Método HTTP (GET, POST, PUT, DELETE)
        max_intentos: Máximo número de reintentos (default: 3)
        timeout: Timeout en segundos (default: 30)
        json: Body en formato JSON (para POST/PUT)
        headers: Headers HTTP
        params: Query parameters

    Returns:
        Response exitoso

    Raises:
        ValueError: Si el error es permanente (4xx)
        RuntimeError: Si falla después de todos los reintentos
    """
    for intento in range(1, max_intentos + 1):
        try:
            # Hacer request según el método
            if metodo == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif metodo == "POST":
                response = requests.post(url, json=json, headers=headers, params=params, timeout=timeout)
            elif metodo == "PUT":
                response = requests.put(url, json=json, headers=headers, params=params, timeout=timeout)
            elif metodo == "DELETE":
                response = requests.delete(url, headers=headers, params=params, timeout=timeout)
            else:
                raise ValueError(f"Método no soportado: {metodo}")

            # Éxito (2xx)
            if 200 <= response.status_code < 300:
                return response

            # Error temporal (5xx o 429) - Reintentar
            if response.status_code in [500, 502, 503, 504, 429]:
                if intento < max_intentos:
                    delay = 2 ** intento
                    print(f"⚠️  Error {response.status_code} (intento {intento}/{max_intentos}). Reintentando en {delay}s...")
                    time.sleep(delay)
                    continue

            # Error permanente (4xx) - No reintentar
            if 400 <= response.status_code < 500:
                raise ValueError(f"Error permanente {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"⏱️  Timeout (intento {intento}/{max_intentos}). Reintentando en {delay}s...")
                time.sleep(delay)
                continue

        except requests.exceptions.RequestException as e:
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"❌ Error de conexión (intento {intento}/{max_intentos}). Reintentando en {delay}s...")
                time.sleep(delay)
                continue
            else:
                raise RuntimeError(f"Error de conexión: {e}")

    raise RuntimeError(f"Falló después de {max_intentos} intentos")


# Ejemplo de uso
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = reintentar_con_backoff(url, metodo="GET", max_intentos=3)
    post = response.json()
    print(f"✅ Post obtenido: {post['title']}")
except ValueError as e:
    print(f"❌ Error permanente: {e}")
except RuntimeError as e:
    print(f"❌ Error después de reintentos: {e}")
```

---

### 💡 Lecciones Aprendidas

1. ✅ **Exponential backoff:** Espera 2^intento segundos (2s, 4s, 8s...)
2. ✅ **Reintenta 5xx y 429:** Son errores temporales
3. ✅ **NO reintentes 4xx:** Son errores permanentes (excepto 429)
4. ✅ **Maneja timeouts:** También son temporales y recuperables
5. ✅ **Logging detallado:** Ayuda a debuggear en producción
6. ✅ **Función reutilizable:** Úsala en todos tus proyectos

---

## 📊 Resumen de los 5 Ejemplos

| Ejemplo | Nivel        | Concepto Principal      | API Usada       | Duración |
| ------- | ------------ | ----------------------- | --------------- | -------- |
| **1**   | 📗 Básico     | GET request básico      | JSONPlaceholder | 10-15min |
| **2**   | 📗 Básico     | Autenticación (API Key) | OpenWeather     | 15-20min |
| **3**   | 📙 Intermedio | POST request (crear)    | JSONPlaceholder | 20-25min |
| **4**   | 📙 Intermedio | Paginación automática   | JSONPlaceholder | 25-30min |
| **5**   | 📕 Avanzado   | Reintentos con backoff  | HTTP Status     | 30-35min |

---

## ✅ Checklist de Verificación

Asegúrate de que puedes hacer lo siguiente:

- [ ] Hacer un GET request y parsear el JSON
- [ ] Guardar datos de API en CSV
- [ ] Configurar API key como variable de entorno
- [ ] Manejar error 401 (no autenticado)
- [ ] Hacer POST request con `json=` (no `data=`)
- [ ] Validar status code 201 (creado)
- [ ] Implementar paginación automática con `while True`
- [ ] Distinguir errores temporales (5xx) de permanentes (4xx)
- [ ] Implementar exponential backoff
- [ ] Crear función reutilizable de reintentos

**Si puedes hacer todo esto, ¡estás listo para el proyecto práctico del Tema 1!** 🎉

---

## 🚀 Próximo Paso

Ve a `03-EJERCICIOS.md` para practicar estos conceptos con 15 ejercicios progresivos.

---

*Última actualización: 2025-10-23*
*Tiempo total de lectura/práctica: 100-125 minutos*
