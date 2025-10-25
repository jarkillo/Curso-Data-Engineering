# Tema 1: APIs REST - Ejercicios Prácticos

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📚 Introducción

Este documento contiene **15 ejercicios progresivos** para practicar consumo de APIs REST. Cada ejercicio incluye:
- ✅ Enunciado claro
- ✅ Contexto empresarial
- ✅ Pistas para resolverlo
- ✅ Solución completa al final

**Empresa ficticia:** DataHub Inc.

**Progresión de dificultad:**
- 📗 **Ejercicios 1-5:** Básico (principiantes)
- 📙 **Ejercicios 6-10:** Intermedio (con experiencia)
- 📕 **Ejercicios 11-15:** Avanzado (integración completa)

---

## 🎯 Cómo Usar Este Documento

1. **Intenta resolver el ejercicio por tu cuenta** (15-30 minutos)
2. Si te atascas, lee las **pistas**
3. Si sigues atascado, consulta la **solución**
4. **Ejecuta el código** para verificar que funciona
5. **Modifica el código** para experimentar

**💡 Consejo:** No leas las soluciones directamente. Aprenderás mucho más resolviendo los ejercicios por tu cuenta.

---

## 📗 EJERCICIOS BÁSICOS (1-5)

### Ejercicio 1: GET Request a API Pública 🌟

**Nivel:** Básico
**Duración:** 10-15 minutos

**Contexto:**
Tu jefe en DataHub Inc. te pide extraer todos los posts de la API de JSONPlaceholder y contar cuántos hay.

**Requerimiento:**
1. Hacer GET request a `https://jsonplaceholder.typicode.com/posts`
2. Contar el total de posts
3. Mostrar el título del primer post

**Criterios de éxito:**
- ✅ El código imprime el total de posts (debe ser 100)
- ✅ El código imprime el título del primer post
- ✅ Validas el status code antes de procesar

**Pistas:**
- Usa `requests.get(url)`
- Usa `response.json()` para obtener la lista
- Usa `len()` para contar elementos

**Código base:**
```python
import requests

# Tu código aquí
```

---

### Ejercicio 2: Extraer Campos Específicos 🔍

**Nivel:** Básico
**Duración:** 10-15 minutos

**Contexto:**
DataHub Inc. necesita un reporte de los primeros 5 posts con solo el título y el body.

**Requerimiento:**
1. Obtener todos los posts de JSONPlaceholder
2. Extraer solo los primeros 5
3. Para cada uno, mostrar: ID, título (primeros 30 caracteres), body (primeros 50 caracteres)

**Criterios de éxito:**
- ✅ Muestra exactamente 5 posts
- ✅ Títulos truncados a 30 caracteres
- ✅ Body truncado a 50 caracteres
- ✅ Formato legible

**Pistas:**
- Usa slicing para limitar: `posts[:5]`
- Usa slicing para truncar strings: `titulo[:30]`
- Usa f-strings para formatear

---

### Ejercicio 3: Filtrar con Query Parameters 🎯

**Nivel:** Básico
**Duración:** 15-20 minutos

**Contexto:**
Tu equipo necesita solo los posts del usuario con ID 1.

**Requerimiento:**
1. Hacer GET request a `https://jsonplaceholder.typicode.com/posts`
2. Usar query parameter `userId=1` para filtrar
3. Contar cuántos posts tiene ese usuario
4. Mostrar los títulos de todos sus posts

**Criterios de éxito:**
- ✅ Solo obtienes posts del userId=1 (debe ser 10 posts)
- ✅ Usas `params` en requests
- ✅ Muestras todos los títulos

**Pistas:**
- Usa `params={"userId": 1}` en requests.get()
- La API filtra automáticamente

---

### Ejercicio 4: Validar Status Codes 🚦

**Nivel:** Básico
**Duración:** 15-20 minutos

**Contexto:**
DataHub Inc. necesita una función robusta que maneje diferentes status codes.

**Requerimiento:**
Crear una función que:
1. Recibe una URL
2. Hace GET request
3. Si status 200: imprime "✅ Éxito"
4. Si status 404: imprime "❌ Recurso no encontrado"
5. Si status 401: imprime "❌ No autenticado"
6. Cualquier otro: imprime "❌ Error {status_code}"
7. Prueba con estas URLs:
   - `https://jsonplaceholder.typicode.com/posts/1` (200)
   - `https://jsonplaceholder.typicode.com/posts/999` (404)

**Criterios de éxito:**
- ✅ Función con firma: `validar_status(url: str) -> None`
- ✅ Maneja los 3 status codes correctamente
- ✅ Muestra el status code en el mensaje

**Pistas:**
- Usa `if/elif/else` para los diferentes códigos
- Usa `response.status_code`

---

### Ejercicio 5: Guardar Datos en CSV 💾

**Nivel:** Básico
**Duración:** 20-25 minutos

**Contexto:**
Tu jefe quiere un CSV con los primeros 10 posts para análisis.

**Requerimiento:**
1. Obtener los primeros 10 posts
2. Guardarlos en `posts.csv` con columnas: `id, userId, title, body`
3. El título debe truncarse a 50 caracteres máximo
4. El body debe truncarse a 100 caracteres máximo

**Criterios de éxito:**
- ✅ Archivo `posts.csv` creado
- ✅ Contiene 10 filas (+ header)
- ✅ Títulos y body truncados correctamente
- ✅ CSV bien formateado (sin errores al abrirlo en Excel)

**Pistas:**
- Usa `import csv`
- Usa `with open("posts.csv", "w", newline="", encoding="utf-8") as f:`
- Usa `csv.writer(f)`

---

## 📙 EJERCICIOS INTERMEDIOS (6-10)

### Ejercicio 6: POST Request para Crear Recurso ➕

**Nivel:** Intermedio
**Duración:** 20-25 minutos

**Contexto:**
DataHub Inc. necesita crear un nuevo post en la API de prueba.

**Requerimiento:**
1. Crear un POST request a `https://jsonplaceholder.typicode.com/posts`
2. Enviar estos datos:
   ```python
   {
       "title": "ETL Pipeline con Python",
       "body": "Guía completa de implementación de pipelines ETL",
       "userId": 1
   }
   ```
3. Validar que el status code sea 201
4. Mostrar el ID asignado por el servidor

**Criterios de éxito:**
- ✅ Status code es 201
- ✅ Usas `json=` (no `data=`)
- ✅ Imprimes el ID del recurso creado

**Pistas:**
- Usa `requests.post(url, json=datos)`
- Verifica `response.status_code == 201`

---

### Ejercicio 7: PUT Request para Actualizar 🔄

**Nivel:** Intermedio
**Duración:** 20-25 minutos

**Contexto:**
Necesitas actualizar el post con ID 1.

**Requerimiento:**
1. Hacer GET a `https://jsonplaceholder.typicode.com/posts/1` para obtener el post actual
2. Modificar el título a "ACTUALIZADO: " + título_original
3. Hacer PUT a la misma URL con los datos modificados
4. Validar que el status code sea 200
5. Mostrar el título actualizado

**Criterios de éxito:**
- ✅ Haces GET primero
- ✅ Modificas el título correctamente
- ✅ Haces PUT con todos los datos
- ✅ Status code es 200

**Pistas:**
- GET primero: `post = requests.get(url).json()`
- Modifica: `post["title"] = "ACTUALIZADO: " + post["title"]`
- PUT: `requests.put(url, json=post)`

---

### Ejercicio 8: DELETE Request 🗑️

**Nivel:** Intermedio
**Duración:** 15-20 minutos

**Contexto:**
DataHub Inc. necesita eliminar el post con ID 1.

**Requerimiento:**
1. Hacer DELETE a `https://jsonplaceholder.typicode.com/posts/1`
2. Validar que el status code sea 200 o 204
3. Intentar hacer GET al mismo post
4. Verificar que devuelve 404 (nota: JSONPlaceholder no elimina realmente, así que devolverá 200, pero simula el flujo)

**Criterios de éxito:**
- ✅ DELETE request exitoso
- ✅ Validación de status code
- ✅ Intentas GET posterior

**Pistas:**
- Usa `requests.delete(url)`
- Status 200 o 204 indican éxito

---

### Ejercicio 9: Paginación Manual ⏭️

**Nivel:** Intermedio
**Duración:** 25-30 minutos

**Contexto:**
Tu equipo necesita los primeros 30 posts, pero la API devuelve solo 10 por página.

**Requerimiento:**
1. Iterar 3 páginas manualmente
2. Usar parámetros `_page` y `_limit`
3. Consolidar todos los posts en una sola lista
4. Mostrar el total de posts descargados

**Criterios de éxito:**
- ✅ Descargas exactamente 30 posts
- ✅ Usas un loop para las 3 páginas
- ✅ Usas `_page=1`, `_page=2`, `_page=3`
- ✅ Usas `_limit=10`

**Pistas:**
- Usa `for pagina in range(1, 4):`
- Usa `params={"_page": pagina, "_limit": 10}`
- Usa `todos_posts.extend(posts)` para consolidar

---

### Ejercicio 10: Detectar y Manejar Error 429 🚨

**Nivel:** Intermedio
**Duración:** 20-25 minutos

**Contexto:**
DataHub Inc. necesita un sistema que detecte rate limiting.

**Requerimiento:**
1. Crear función `hacer_request_con_rate_limit(url)`
2. Simula rate limit usando `https://httpstat.us/429`
3. Si recibe 429, espera 5 segundos y reintenta (máximo 2 veces)
4. Si recibe 200, devuelve la respuesta
5. Si falla después de 2 reintentos, lanza excepción

**Criterios de éxito:**
- ✅ Detecta status 429
- ✅ Espera 5 segundos antes de reintentar
- ✅ Máximo 2 reintentos
- ✅ Muestra mensajes informativos

**Pistas:**
- Usa `import time` y `time.sleep(5)`
- Usa un loop con contador de intentos
- Usa `if response.status_code == 429:`

---

## 📕 EJERCICIOS AVANZADOS (11-15)

### Ejercicio 11: Reintentos con Exponential Backoff ⏱️

**Nivel:** Avanzado
**Duración:** 30-35 minutos

**Contexto:**
Tu equipo necesita un cliente robusto que maneje errores 5xx.

**Requerimiento:**
Crear función `hacer_request_robusto(url, max_intentos=3)` que:
1. Hace GET request
2. Si recibe 200: devuelve response
3. Si recibe 5xx (500, 502, 503, 504): reintenta con exponential backoff
   - Intento 1: espera 2 segundos
   - Intento 2: espera 4 segundos
   - Intento 3: espera 8 segundos
4. Si recibe 4xx (excepto 429): lanza ValueError (error permanente)
5. Si recibe 429: reintenta como 5xx
6. Si falla después de max_intentos: lanza RuntimeError

**Criterios de éxito:**
- ✅ Implementa exponential backoff correctamente
- ✅ Distingue errores temporales (5xx) de permanentes (4xx)
- ✅ 429 se trata como temporal
- ✅ Muestra logs de cada intento

**Pistas:**
- Delay: `delay = 2 ** intento`
- Usa `time.sleep(delay)`
- Usa `try/except` para manejar errores

---

### Ejercicio 12: Paginación Automática Completa 🔄

**Nivel:** Avanzado
**Duración:** 30-35 minutos

**Contexto:**
DataHub Inc. necesita descargar TODOS los posts de la API sin saber cuántos hay.

**Requerimiento:**
Crear función `descargar_todos_posts()` que:
1. Itera páginas automáticamente (empieza en página 1)
2. Para cuando recibe lista vacía
3. Usa `_limit=10`
4. Devuelve lista con todos los posts
5. Muestra progreso: "Página X: Y posts descargados"

**Criterios de éxito:**
- ✅ Descarga los 100 posts
- ✅ No hardcodeas el número de páginas
- ✅ Para automáticamente cuando no hay más datos
- ✅ Muestra progreso en consola

**Pistas:**
- Usa `while True:` con `break` cuando `not posts`
- Incrementa página en cada iteración
- Usa `todos_posts.extend(posts)`

---

### Ejercicio 13: Paginación con Cursor 🔗

**Nivel:** Avanzado
**Duración:** 35-40 minutos

**Contexto:**
Una API avanzada usa cursor-based pagination.

**Requerimiento:**
Simula cursor-based pagination:
1. Primera página: `GET /posts?_start=0&_limit=10`
2. Segunda página: `GET /posts?_start=10&_limit=10`
3. Continúa hasta que la respuesta esté vacía
4. Implementa función `descargar_con_cursor(limite=10)`

**Criterios de éxito:**
- ✅ Usa `_start` como cursor
- ✅ Incrementa cursor correctamente: `cursor += limite`
- ✅ Para cuando no hay más datos
- ✅ Descarga todos los posts

**Pistas:**
- Cursor inicial: `cursor = 0`
- Parámetros: `{"_start": cursor, "_limit": limite}`
- Actualiza cursor: `cursor += limite`

---

### Ejercicio 14: Comparar Métodos de Autenticación 🔐

**Nivel:** Avanzado
**Duración:** 40-45 minutos

**Contexto:**
DataHub Inc. necesita documentación de los 3 métodos de autenticación.

**Requerimiento:**
Crear 3 funciones:
1. `crear_headers_api_key(api_key: str) -> dict`
   - Devuelve `{"X-API-Key": api_key}`
2. `crear_headers_bearer(token: str) -> dict`
   - Devuelve `{"Authorization": f"Bearer {token}"}`
3. `crear_headers_basic_auth(usuario: str, password: str) -> dict`
   - Codifica en base64: `usuario:password`
   - Devuelve `{"Authorization": f"Basic {encoded}"}`

Luego:
4. Prueba cada función imprimiendo los headers
5. Documenta ventajas y desventajas de cada método

**Criterios de éxito:**
- ✅ 3 funciones implementadas correctamente
- ✅ Basic Auth codifica en base64
- ✅ Headers formateados correctamente
- ✅ Documentación de ventajas/desventajas

**Pistas:**
- Usa `import base64`
- Codifica: `base64.b64encode(b"usuario:password").decode()`

---

### Ejercicio 15: Pipeline ETL Completo 🚀

**Nivel:** Avanzado
**Duración:** 45-60 minutos

**Contexto:**
DataHub Inc. necesita un pipeline ETL completo: Extraer de API → Transformar → Cargar en CSV.

**Requerimiento:**
Crear pipeline completo:

1. **EXTRACT:** Descargar todos los posts de JSONPlaceholder
2. **TRANSFORM:**
   - Añadir columna `titulo_largo` (True si título > 50 caracteres)
   - Añadir columna `body_largo` (True si body > 200 caracteres)
   - Filtrar solo posts del userId 1-3
   - Ordenar por userId, luego por id
3. **LOAD:** Guardar en `posts_procesados.csv`

**Estructura sugerida:**
```python
def extract() -> list:
    """Extrae posts de la API."""
    pass

def transform(posts: list) -> list:
    """Transforma los posts."""
    pass

def load(posts: list, filename: str) -> None:
    """Guarda en CSV."""
    pass

def pipeline():
    """Pipeline completo."""
    posts = extract()
    posts_transformados = transform(posts)
    load(posts_transformados, "posts_procesados.csv")
    print(f"✅ Pipeline completado: {len(posts_transformados)} posts procesados")

if __name__ == "__main__":
    pipeline()
```

**Criterios de éxito:**
- ✅ Extract descarga todos los posts (100)
- ✅ Transform añade 2 columnas calculadas
- ✅ Transform filtra correctamente (userId 1-3 = 30 posts)
- ✅ Transform ordena correctamente
- ✅ Load crea CSV válido con 6 columnas
- ✅ Pipeline se ejecuta sin errores

**Pistas:**
- Extract: Reutiliza ejercicio 12
- Transform: Usa list comprehension
- Load: Usa `csv.DictWriter` para mantener columnas

---

## ✅ Autoevaluación

Marca los ejercicios que completaste:

**Básicos (1-5):**
- [ ] Ejercicio 1: GET Request básico
- [ ] Ejercicio 2: Extraer campos específicos
- [ ] Ejercicio 3: Filtrar con query parameters
- [ ] Ejercicio 4: Validar status codes
- [ ] Ejercicio 5: Guardar en CSV

**Intermedios (6-10):**
- [ ] Ejercicio 6: POST request
- [ ] Ejercicio 7: PUT request
- [ ] Ejercicio 8: DELETE request
- [ ] Ejercicio 9: Paginación manual
- [ ] Ejercicio 10: Manejar error 429

**Avanzados (11-15):**
- [ ] Ejercicio 11: Exponential backoff
- [ ] Ejercicio 12: Paginación automática
- [ ] Ejercicio 13: Paginación con cursor
- [ ] Ejercicio 14: Comparar autenticación
- [ ] Ejercicio 15: Pipeline ETL completo

**Progreso:**
- **0-5 completados:** 📗 Principiante - ¡Sigue practicando!
- **6-10 completados:** 📙 Intermedio - ¡Buen progreso!
- **11-15 completados:** 📕 Avanzado - ¡Excelente dominio!

---

## 📚 SOLUCIONES

<details>
<summary><b>⚠️ SPOILER ALERT: Click para ver las soluciones</b></summary>

### Solución Ejercicio 1

```python
import requests

# Hacer GET request
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

# Validar status code
if response.status_code == 200:
    posts = response.json()

    # Contar total
    total = len(posts)
    print(f"Total de posts: {total}")

    # Primer post
    primer_post = posts[0]
    print(f"Título del primer post: {primer_post['title']}")
else:
    print(f"Error: Status code {response.status_code}")
```

**Salida esperada:**
```
Total de posts: 100
Título del primer post: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

---

### Solución Ejercicio 2

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()

    # Primeros 5 posts
    primeros_cinco = posts[:5]

    print("=== Primeros 5 Posts ===\n")

    for post in primeros_cinco:
        id_post = post['id']
        titulo = post['title'][:30]
        body = post['body'][:50]

        print(f"ID: {id_post}")
        print(f"Título: {titulo}...")
        print(f"Body: {body}...")
        print("-" * 50)
else:
    print(f"Error: Status code {response.status_code}")
```

**Salida esperada:**
```
=== Primeros 5 Posts ===

ID: 1
Título: sunt aut facere repellat pro...
Body: quia et suscipit
suscipit recusandae consequu...
--------------------------------------------------
...
```

---

### Solución Ejercicio 3

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

# Filtrar por userId con query parameter
params = {"userId": 1}
response = requests.get(url, params=params)

if response.status_code == 200:
    posts = response.json()

    print(f"Total de posts del usuario 1: {len(posts)}")
    print("\n=== Títulos ===\n")

    for post in posts:
        print(f"{post['id']}. {post['title']}")
else:
    print(f"Error: Status code {response.status_code}")
```

**Salida esperada:**
```
Total de posts del usuario 1: 10

=== Títulos ===

1. sunt aut facere repellat provident occaecati excepturi optio reprehenderit
2. qui est esse
3. ea molestias quasi exercitationem repellat qui ipsa sit aut
...
```

---

### Solución Ejercicio 4

```python
import requests

def validar_status(url: str) -> None:
    """Valida el status code de una URL."""
    response = requests.get(url)
    status = response.status_code

    if status == 200:
        print(f"✅ Éxito (status {status})")
    elif status == 404:
        print(f"❌ Recurso no encontrado (status {status})")
    elif status == 401:
        print(f"❌ No autenticado (status {status})")
    else:
        print(f"❌ Error {status}")

# Probar con diferentes URLs
print("Probando URL válida:")
validar_status("https://jsonplaceholder.typicode.com/posts/1")

print("\nProbando URL inexistente:")
validar_status("https://jsonplaceholder.typicode.com/posts/999")
```

**Salida esperada:**
```
Probando URL válida:
✅ Éxito (status 200)

Probando URL inexistente:
❌ Recurso no encontrado (status 404)
```

---

### Solución Ejercicio 5

```python
import requests
import csv

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()

    # Primeros 10 posts
    primeros_diez = posts[:10]

    # Guardar en CSV
    with open("posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["id", "userId", "title", "body"])

        # Datos
        for post in primeros_diez:
            writer.writerow([
                post["id"],
                post["userId"],
                post["title"][:50],  # Truncar a 50
                post["body"][:100]   # Truncar a 100
            ])

    print(f"✅ {len(primeros_diez)} posts guardados en posts.csv")
else:
    print(f"❌ Error: Status code {response.status_code}")
```

**Salida esperada:**
```
✅ 10 posts guardados en posts.csv
```

---

### Solución Ejercicio 6

```python
import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

# Datos a enviar
nuevo_post = {
    "title": "ETL Pipeline con Python",
    "body": "Guía completa de implementación de pipelines ETL",
    "userId": 1
}

# POST request
response = requests.post(url, json=nuevo_post)

# Validar status code
if response.status_code == 201:
    post_creado = response.json()
    print("✅ Post creado exitosamente")
    print(f"   ID asignado: {post_creado['id']}")
    print(f"   Título: {post_creado['title']}")
    print(f"\n   Respuesta completa:")
    print(json.dumps(post_creado, indent=2, ensure_ascii=False))
else:
    print(f"❌ Error: Status code {response.status_code}")
```

**Salida esperada:**
```
✅ Post creado exitosamente
   ID asignado: 101
   Título: ETL Pipeline con Python

   Respuesta completa:
{
  "title": "ETL Pipeline con Python",
  "body": "Guía completa de implementación de pipelines ETL",
  "userId": 1,
  "id": 101
}
```

---

### Solución Ejercicio 7

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

# 1. GET para obtener el post actual
response_get = requests.get(url)

if response_get.status_code == 200:
    post = response_get.json()
    print(f"Título original: {post['title']}")

    # 2. Modificar el título
    post["title"] = "ACTUALIZADO: " + post["title"]

    # 3. PUT para actualizar
    response_put = requests.put(url, json=post)

    if response_put.status_code == 200:
        post_actualizado = response_put.json()
        print(f"✅ Post actualizado")
        print(f"   Título nuevo: {post_actualizado['title']}")
    else:
        print(f"❌ Error en PUT: Status {response_put.status_code}")
else:
    print(f"❌ Error en GET: Status {response_get.status_code}")
```

**Salida esperada:**
```
Título original: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
✅ Post actualizado
   Título nuevo: ACTUALIZADO: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

---

### Solución Ejercicio 8

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

# 1. DELETE request
response_delete = requests.delete(url)

if response_delete.status_code in [200, 204]:
    print(f"✅ Post eliminado (status {response_delete.status_code})")

    # 2. Intentar GET para verificar (en JSONPlaceholder no se elimina realmente)
    response_get = requests.get(url)

    if response_get.status_code == 404:
        print("✅ Confirmado: Post no existe (404)")
    else:
        print(f"ℹ️  Nota: JSONPlaceholder es API de prueba, no elimina realmente")
        print(f"   Status GET: {response_get.status_code}")
else:
    print(f"❌ Error en DELETE: Status {response_delete.status_code}")
```

**Salida esperada:**
```
✅ Post eliminado (status 200)
ℹ️  Nota: JSONPlaceholder es API de prueba, no elimina realmente
   Status GET: 200
```

---

### Solución Ejercicio 9

```python
import requests

base_url = "https://jsonplaceholder.typicode.com/posts"

todos_posts = []

# Iterar 3 páginas
for pagina in range(1, 4):
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
        break

print(f"\n📊 Total descargado: {len(todos_posts)} posts")
```

**Salida esperada:**
```
✅ Página 1: 10 posts descargados
✅ Página 2: 10 posts descargados
✅ Página 3: 10 posts descargados

📊 Total descargado: 30 posts
```

---

### Solución Ejercicio 10

```python
import requests
import time

def hacer_request_con_rate_limit(url: str) -> requests.Response:
    """Hace request con manejo de rate limiting."""
    max_intentos = 2

    for intento in range(1, max_intentos + 1):
        print(f"Intento {intento}/{max_intentos}...")

        response = requests.get(url)

        if response.status_code == 200:
            print("✅ Éxito")
            return response
        elif response.status_code == 429:
            if intento < max_intentos:
                print(f"❌ Rate limit alcanzado (429). Esperando 5 segundos...")
                time.sleep(5)
            else:
                raise RuntimeError("Rate limit alcanzado después de reintentos")
        else:
            raise RuntimeError(f"Error inesperado: {response.status_code}")

    raise RuntimeError(f"Falló después de {max_intentos} intentos")

# Probar con API que simula 429
url = "https://httpstat.us/429"

try:
    response = hacer_request_con_rate_limit(url)
    print(f"Respuesta: {response.text}")
except RuntimeError as e:
    print(f"❌ Error: {e}")
```

**Salida esperada:**
```
Intento 1/2...
❌ Rate limit alcanzado (429). Esperando 5 segundos...
Intento 2/2...
❌ Error: Rate limit alcanzado después de reintentos
```

---

### Solución Ejercicio 11

```python
import requests
import time

def hacer_request_robusto(url: str, max_intentos: int = 3) -> requests.Response:
    """Hace request con exponential backoff."""
    for intento in range(1, max_intentos + 1):
        print(f"\n🔄 Intento {intento}/{max_intentos}")

        try:
            response = requests.get(url, timeout=30)

            # Éxito
            if response.status_code == 200:
                print("✅ Éxito")
                return response

            # Error temporal (reintentar)
            if response.status_code in [500, 502, 503, 504, 429]:
                if intento < max_intentos:
                    delay = 2 ** intento  # Exponential backoff
                    print(f"❌ Error temporal {response.status_code}")
                    print(f"⏳ Esperando {delay} segundos...")
                    time.sleep(delay)
                    continue
                else:
                    raise RuntimeError(f"Falló después de {max_intentos} intentos")

            # Error permanente (no reintentar)
            if 400 <= response.status_code < 500:
                raise ValueError(f"Error permanente {response.status_code}")

        except requests.exceptions.Timeout:
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"⏱️  Timeout")
                print(f"⏳ Esperando {delay} segundos...")
                time.sleep(delay)
                continue
            else:
                raise RuntimeError("Timeout después de múltiples reintentos")

    raise RuntimeError(f"Falló después de {max_intentos} intentos")

# Probar con API real
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = hacer_request_robusto(url)
    post = response.json()
    print(f"\n✅ Post obtenido: {post['title'][:50]}...")
except Exception as e:
    print(f"\n❌ Error: {e}")
```

**Salida esperada:**
```
🔄 Intento 1/3
✅ Éxito

✅ Post obtenido: sunt aut facere repellat provident occaecati...
```

---

### Solución Ejercicio 12

```python
import requests

def descargar_todos_posts() -> list:
    """Descarga todos los posts con paginación automática."""
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

            # Si no hay más posts, terminar
            if not posts:
                print(f"✅ Paginación completa")
                break

            todos_posts.extend(posts)
            print(f"Página {pagina}: {len(posts)} posts descargados")

            pagina += 1
        else:
            print(f"❌ Error: Status {response.status_code}")
            break

    return todos_posts

# Ejecutar
posts = descargar_todos_posts()
print(f"\n📊 Total: {len(posts)} posts")
```

**Salida esperada:**
```
=== Paginación Automática ===

Página 1: 10 posts descargados
Página 2: 10 posts descargados
...
Página 10: 10 posts descargados
✅ Paginación completa

📊 Total: 100 posts
```

---

### Solución Ejercicio 13

```python
import requests

def descargar_con_cursor(limite: int = 10) -> list:
    """Descarga posts usando cursor-based pagination."""
    base_url = "https://jsonplaceholder.typicode.com/posts"
    todos_posts = []
    cursor = 0
    pagina = 1

    print("=== Paginación con Cursor ===\n")

    while True:
        params = {
            "_start": cursor,
            "_limit": limite
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            posts = response.json()

            # Si no hay más posts, terminar
            if not posts:
                print(f"✅ Paginación completa")
                break

            todos_posts.extend(posts)
            print(f"Página {pagina} (cursor={cursor}): {len(posts)} posts")

            # Actualizar cursor
            cursor += limite
            pagina += 1
        else:
            print(f"❌ Error: Status {response.status_code}")
            break

    return todos_posts

# Ejecutar
posts = descargar_con_cursor(limite=10)
print(f"\n📊 Total: {len(posts)} posts")
```

**Salida esperada:**
```
=== Paginación con Cursor ===

Página 1 (cursor=0): 10 posts
Página 2 (cursor=10): 10 posts
...
Página 10 (cursor=90): 10 posts
✅ Paginación completa

📊 Total: 100 posts
```

---

### Solución Ejercicio 14

```python
import base64

def crear_headers_api_key(api_key: str) -> dict:
    """Crea headers con API Key."""
    return {"X-API-Key": api_key}

def crear_headers_bearer(token: str) -> dict:
    """Crea headers con Bearer Token."""
    return {"Authorization": f"Bearer {token}"}

def crear_headers_basic_auth(usuario: str, password: str) -> dict:
    """Crea headers con Basic Auth."""
    credentials = f"{usuario}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

# Probar las funciones
print("=== Métodos de Autenticación ===\n")

print("1. API Key:")
headers_api = crear_headers_api_key("sk_live_abc123")
print(f"   {headers_api}")

print("\n2. Bearer Token:")
headers_bearer = crear_headers_bearer("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
print(f"   {headers_bearer}")

print("\n3. Basic Auth:")
headers_basic = crear_headers_basic_auth("usuario", "contraseña123")
print(f"   {headers_basic}")

print("\n" + "="*60)
print("COMPARACIÓN DE MÉTODOS")
print("="*60)

print("""
| Método       | Seguridad | Expiración | Complejidad |
| ------------ | --------- | ---------- | ----------- |
| API Key      | Media     | No         | Baja        |
| Bearer Token | Alta      | Sí         | Media       |
| Basic Auth   | Baja      | No         | Baja        |

VENTAJAS:
- API Key: Simple, no expira
- Bearer Token: Muy seguro, expira automáticamente
- Basic Auth: Muy simple de implementar

DESVENTAJAS:
- API Key: Si se filtra, válida para siempre
- Bearer Token: Necesitas refrescar el token
- Basic Auth: Envías credenciales en cada request
""")
```

**Salida esperada:**
```
=== Métodos de Autenticación ===

1. API Key:
   {'X-API-Key': 'sk_live_abc123'}

2. Bearer Token:
   {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'}

3. Basic Auth:
   {'Authorization': 'Basic dXN1YXJpbzpjb250cmFzZcOxYTEyMw=='}

============================================================
COMPARACIÓN DE MÉTODOS
============================================================

| Método       | Seguridad | Expiración | Complejidad |
| ------------ | --------- | ---------- | ----------- |
| API Key      | Media     | No         | Baja        |
| Bearer Token | Alta      | Sí         | Media       |
| Basic Auth   | Baja      | No         | Baja        |
...
```

---

### Solución Ejercicio 15

```python
import requests
import csv

def extract() -> list:
    """Extrae posts de la API."""
    url = "https://jsonplaceholder.typicode.com/posts"
    todos_posts = []
    pagina = 1

    while True:
        params = {"_page": pagina, "_limit": 10}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            posts = response.json()
            if not posts:
                break
            todos_posts.extend(posts)
            pagina += 1
        else:
            raise RuntimeError(f"Error en extracción: {response.status_code}")

    print(f"✅ EXTRACT: {len(todos_posts)} posts descargados")
    return todos_posts

def transform(posts: list) -> list:
    """Transforma los posts."""
    posts_transformados = []

    for post in posts:
        # Filtrar solo userId 1-3
        if post["userId"] not in [1, 2, 3]:
            continue

        # Añadir columnas calculadas
        post["titulo_largo"] = len(post["title"]) > 50
        post["body_largo"] = len(post["body"]) > 200

        posts_transformados.append(post)

    # Ordenar por userId, luego por id
    posts_transformados.sort(key=lambda p: (p["userId"], p["id"]))

    print(f"✅ TRANSFORM: {len(posts_transformados)} posts procesados")
    return posts_transformados

def load(posts: list, filename: str) -> None:
    """Guarda en CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        if posts:
            fieldnames = ["id", "userId", "title", "body", "titulo_largo", "body_largo"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for post in posts:
                writer.writerow({
                    "id": post["id"],
                    "userId": post["userId"],
                    "title": post["title"],
                    "body": post["body"],
                    "titulo_largo": post["titulo_largo"],
                    "body_largo": post["body_largo"]
                })

    print(f"✅ LOAD: Guardado en {filename}")

def pipeline():
    """Pipeline ETL completo."""
    print("=== Pipeline ETL ===\n")

    # ETL
    posts = extract()
    posts_transformados = transform(posts)
    load(posts_transformados, "posts_procesados.csv")

    print(f"\n🎉 Pipeline completado: {len(posts_transformados)} posts procesados")

if __name__ == "__main__":
    pipeline()
```

**Salida esperada:**
```
=== Pipeline ETL ===

✅ EXTRACT: 100 posts descargados
✅ TRANSFORM: 30 posts procesados
✅ LOAD: Guardado en posts_procesados.csv

🎉 Pipeline completado: 30 posts procesados
```

</details>

---

## 🎓 ¿Qué Sigue?

Después de completar estos ejercicios:

1. **Proyecto Práctico:** Ve a `04-proyecto-practico/` para aplicar todo lo aprendido
2. **Revisión Pedagógica:** Lee `REVISION_PEDAGOGICA.md` para entender la progresión
3. **README del Tema:** Consulta `README.md` para resumen del tema

**¡Felicidades por completar los ejercicios!** 🎉

---

*Última actualización: 2025-10-23*
*Tiempo estimado total: 6-10 horas*
