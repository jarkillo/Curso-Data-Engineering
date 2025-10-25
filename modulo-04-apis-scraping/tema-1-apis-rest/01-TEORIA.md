# Tema 1: APIs REST - Teoría Fundamental

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este tema, serás capaz de:

1. ✅ Entender qué es una API REST y por qué es fundamental en Data Engineering
2. ✅ Conocer los métodos HTTP (GET, POST, PUT, DELETE) y cuándo usar cada uno
3. ✅ Interpretar status codes (2xx, 3xx, 4xx, 5xx) y actuar en consecuencia
4. ✅ Implementar diferentes métodos de autenticación (API Key, Bearer, Basic Auth)
5. ✅ Manejar errores temporales con reintentos inteligentes (exponential backoff)
6. ✅ Trabajar con APIs paginadas (Offset/Limit y Cursor)
7. ✅ Aplicar rate limiting para no sobrecargar servidores
8. ✅ Consumir APIs de forma segura (solo HTTPS)

---

## 📚 Introducción: ¿Qué es una API REST?

### Definición Simple

Una **API REST** (Application Programming Interface - Representational State Transfer) es como un **restaurante con menú**:

- **Tú (cliente)** quieres datos → Haces un pedido (request)
- **El servidor** tiene los datos → Prepara y entrega tu pedido (response)
- **El menú** lista qué puedes pedir → La documentación de la API

**Ejemplo del mundo real:**

```
🍕 Restaurante tradicional:
Cliente: "Quiero una pizza margarita"
Mesero: Toma el pedido, lo lleva a cocina
Cocina: Prepara la pizza
Mesero: Entrega la pizza al cliente

🌐 API REST:
Cliente (tu código Python): GET https://api.ejemplo.com/users/123
Servidor: Busca el usuario 123 en la base de datos
Servidor: Devuelve los datos en formato JSON
Cliente: Recibe {"id": 123, "name": "Ana", "email": "ana@ejemplo.com"}
```

### ¿Por qué importa en Data Engineering?

Como Data Engineer, **el 80% de tu extracción de datos** vendrá de APIs:

1. **APIs de terceros:** Twitter, Google Analytics, Stripe, Salesforce
2. **APIs internas:** Sistemas de tu empresa (ERP, CRM, inventario)
3. **APIs públicas:** Datos gubernamentales, clima, finanzas

**Ventajas de usar APIs vs scraping:**

| Aspecto           | API REST                   | Web Scraping                    |
| ----------------- | -------------------------- | ------------------------------- |
| **Velocidad**     | ⚡ Rápido (segundos)        | 🐢 Lento (minutos)               |
| **Confiabilidad** | ✅ Estructura fija          | ❌ Puede romperse si cambia HTML |
| **Legalidad**     | ✅ Permitido (con términos) | ⚠️ Zona gris legal               |
| **Rate limiting** | ✅ Claro (ej: 100 req/min)  | ❌ Puedes ser bloqueado          |
| **Formato**       | ✅ JSON/XML estructurado    | ❌ HTML desordenado              |

**Conclusión:** Siempre usa APIs cuando estén disponibles. Solo usa web scraping como último recurso.

---

## 1️⃣ HTTP Básico: Los 4 Métodos Fundamentales

HTTP es el protocolo que usan las APIs para comunicarse. Piensa en los métodos HTTP como **acciones que puedes hacer en un restaurante:**

### GET - Consultar/Leer 📖

**Analogía:** Pedir el menú para ver qué hay disponible.

**Qué hace:** Obtiene datos del servidor **sin modificar nada**.

**Ejemplo:**
```python
GET https://api.tienda.com/productos
# Devuelve lista de todos los productos

GET https://api.tienda.com/productos/123
# Devuelve el producto con ID 123
```

**Características:**
- ✅ **Seguro:** No cambia datos en el servidor
- ✅ **Idempotente:** Puedes llamarlo 1000 veces, siempre obtienes lo mismo
- ✅ **Cacheable:** Los navegadores/proxies pueden guardar la respuesta

**Cuándo usarlo:**
- Buscar usuarios, productos, pedidos
- Obtener reportes, métricas, estadísticas
- Listar recursos disponibles

---

### POST - Crear ➕

**Analogía:** Hacer un nuevo pedido en el restaurante.

**Qué hace:** Crea un **nuevo recurso** en el servidor.

**Ejemplo:**
```python
POST https://api.tienda.com/productos
Body: {
    "nombre": "Laptop HP",
    "precio": 599.99,
    "stock": 15
}

# Respuesta: 201 Created
# {"id": 456, "nombre": "Laptop HP", "precio": 599.99, "stock": 15}
```

**Características:**
- ❌ **No seguro:** Crea datos nuevos en el servidor
- ❌ **No idempotente:** Llamarlo 5 veces crea 5 productos duplicados
- ✅ **Devuelve el recurso creado** con su ID asignado

**Cuándo usarlo:**
- Registrar un nuevo usuario
- Crear un nuevo pedido
- Subir un archivo
- Enviar un formulario

---

### PUT - Actualizar/Reemplazar 🔄

**Analogía:** Modificar tu pedido ("Cambia mi pizza por una vegetariana").

**Qué hace:** Actualiza un recurso **existente** reemplazándolo completamente.

**Ejemplo:**
```python
PUT https://api.tienda.com/productos/456
Body: {
    "nombre": "Laptop HP (actualizado)",
    "precio": 549.99,  # Precio rebajado
    "stock": 10        # Stock reducido
}

# Respuesta: 200 OK
# Devuelve el producto actualizado
```

**Características:**
- ❌ **No seguro:** Modifica datos en el servidor
- ✅ **Idempotente:** Llamarlo 10 veces con los mismos datos = mismo resultado
- ⚠️ **Reemplaza todo:** Si no envías un campo, se borra (o pone en null)

**Cuándo usarlo:**
- Actualizar perfil de usuario completo
- Cambiar configuración de cuenta
- Reemplazar un documento

**Nota:** Existe también **PATCH** que actualiza solo campos específicos (no reemplaza todo).

---

### DELETE - Eliminar 🗑️

**Analogía:** Cancelar tu pedido antes de que lo cocinen.

**Qué hace:** Elimina un recurso del servidor.

**Ejemplo:**
```python
DELETE https://api.tienda.com/productos/456

# Respuesta: 204 No Content (éxito, sin body en la respuesta)
# o 200 OK con mensaje de confirmación
```

**Características:**
- ❌ **No seguro:** Elimina datos en el servidor
- ✅ **Idempotente:** Llamarlo 5 veces = mismo resultado (el recurso ya no existe)
- ⚠️ **Irreversible:** No hay "deshacer" (a menos que la API lo implemente)

**Cuándo usarlo:**
- Eliminar un pedido cancelado
- Borrar un usuario
- Remover un archivo

---

### 📊 Resumen de Métodos HTTP

| Método     | Acción     | Seguro | Idempotente | Ejemplo                     |
| ---------- | ---------- | ------ | ----------- | --------------------------- |
| **GET**    | Leer       | ✅      | ✅           | Obtener lista de usuarios   |
| **POST**   | Crear      | ❌      | ❌           | Crear nuevo usuario         |
| **PUT**    | Actualizar | ❌      | ✅           | Reemplazar usuario completo |
| **PATCH**  | Modificar  | ❌      | ✅           | Actualizar solo email       |
| **DELETE** | Eliminar   | ❌      | ✅           | Borrar usuario              |

**💡 Regla de oro:** GET para leer, POST para crear, PUT/PATCH para actualizar, DELETE para borrar.

---

## 2️⃣ Status Codes: El Semáforo de las APIs 🚦

Los **status codes** son números de 3 dígitos que indican el resultado de tu request.

**Analogía:** Son como **semáforos en la carretera**:
- 🟢 **2xx:** Verde - Todo bien, sigue adelante
- 🟡 **3xx:** Amarillo - Redirección, ajusta tu ruta
- 🔴 **4xx:** Rojo - Error del cliente (tú hiciste algo mal)
- 🔴 **5xx:** Rojo - Error del servidor (ellos tienen problemas)

### 2xx - Éxito ✅

El request fue exitoso.

| Code               | Significado         | Cuándo ocurre             |
| ------------------ | ------------------- | ------------------------- |
| **200 OK**         | Éxito general       | GET, PUT, DELETE exitosos |
| **201 Created**    | Recurso creado      | POST exitoso              |
| **204 No Content** | Éxito sin respuesta | DELETE exitoso            |

**Ejemplo:**
```python
response = requests.get("https://api.tienda.com/productos/123")
print(response.status_code)  # 200
print(response.json())       # {"id": 123, "nombre": "Laptop", ...}
```

---

### 3xx - Redirección 🔀

El recurso se movió a otra URL.

| Code                      | Significado             | Qué hacer                            |
| ------------------------- | ----------------------- | ------------------------------------ |
| **301 Moved Permanently** | URL cambió para siempre | Actualiza tu código con la nueva URL |
| **302 Found**             | Redirección temporal    | Sigue el redirect automáticamente    |

**Ejemplo:**
```python
# La librería requests sigue redirects automáticamente
response = requests.get("https://api-vieja.com/productos")
print(response.url)  # https://api-nueva.com/productos (redirect automático)
```

**💡 Tip:** `requests` maneja redirects automáticamente, no necesitas preocuparte.

---

### 4xx - Error del Cliente ❌ (Tú hiciste algo mal)

**Estos errores NO se deben reintentar** (no se solucionarán solos).

| Code                      | Significado         | Causa común                          | Solución                              |
| ------------------------- | ------------------- | ------------------------------------ | ------------------------------------- |
| **400 Bad Request**       | Request malformado  | JSON inválido, campo requerido falta | Revisar el body y headers             |
| **401 Unauthorized**      | No autenticado      | API key falta o inválida             | Añadir/corregir API key               |
| **403 Forbidden**         | No autorizado       | Tienes permiso pero no para esto     | Verificar permisos de tu cuenta       |
| **404 Not Found**         | Recurso no existe   | URL incorrecta o recurso borrado     | Verificar URL y que el recurso exista |
| **429 Too Many Requests** | Demasiados requests | Superaste rate limit                 | **Esperar y reintentar**              |

**Ejemplo 401 (no autenticado):**
```python
response = requests.get("https://api.clima.com/weather")
print(response.status_code)  # 401
print(response.json())
# {"error": "API key missing. Please provide X-API-Key header"}
```

**Ejemplo 404 (no encontrado):**
```python
response = requests.get("https://api.tienda.com/productos/999999")
print(response.status_code)  # 404
print(response.json())
# {"error": "Product with ID 999999 not found"}
```

**⚠️ Importante:** Los errores 4xx son **culpa del cliente** (tu código). Revisa tu request antes de reintentar.

**Excepción: 429 Too Many Requests**
- Este es el **único error 4xx que SÍ debes reintentar**
- Significa que hiciste muchos requests muy rápido
- Solución: Espera unos segundos (el servidor te dice cuánto en el header `Retry-After`)

---

### 5xx - Error del Servidor 🔥 (Ellos tienen problemas)

**Estos errores SÍ se pueden reintentar** (son temporales).

| Code                          | Significado                              | Causa común                | Qué hacer                       |
| ----------------------------- | ---------------------------------------- | -------------------------- | ------------------------------- |
| **500 Internal Server Error** | Error genérico del servidor              | Bug en su código           | **Reintentar** después          |
| **502 Bad Gateway**           | Servidor proxy falló                     | Problema de red intermedio | **Reintentar**                  |
| **503 Service Unavailable**   | Servidor sobrecargado o en mantenimiento | Mucho tráfico              | **Reintentar** con backoff      |
| **504 Gateway Timeout**       | Servidor tardó demasiado                 | Request muy pesado         | **Reintentar** o reducir tamaño |

**Ejemplo 503 (servicio no disponible):**
```python
response = requests.get("https://api.popular.com/datos")
print(response.status_code)  # 503
print(response.json())
# {"error": "Service temporarily unavailable. Please retry in 30 seconds"}
```

**✅ Estrategia para errores 5xx:**
1. **Espera** unos segundos (exponential backoff: 2s, 4s, 8s, 16s...)
2. **Reintenta** hasta 3-5 veces
3. Si sigue fallando, **registra el error** y notifica al equipo

---

### 📊 Resumen de Status Codes

```
2xx ✅ Éxito         → Procesa la respuesta
3xx 🔀 Redirect      → Sigue el redirect (automático con requests)
4xx ❌ Error cliente → NO REINTENTAR (excepto 429)
5xx 🔥 Error servidor → SÍ REINTENTAR (con backoff)
```

---

## 3️⃣ Headers y Body: Los Detalles del Request

### Headers - Metadatos del Request 📋

Los **headers** son como el **sobre de una carta**: contienen información sobre el mensaje.

**Headers comunes:**

```python
headers = {
    "Content-Type": "application/json",     # Formato del body
    "Authorization": "Bearer abc123...",    # Autenticación
    "User-Agent": "MiApp/1.0",             # Quién hace el request
    "Accept": "application/json",           # Qué formato quieres en respuesta
    "X-API-Key": "tu-api-key-aqui"         # API Key (custom header)
}
```

**Ejemplo:**
```python
import requests

response = requests.get(
    "https://api.ejemplo.com/users",
    headers={
        "Authorization": "Bearer mi-token-jwt",
        "Accept": "application/json"
    }
)
```

---

### Body - El Contenido del Request 📦

El **body** es el **contenido de la carta**: los datos que envías.

**Solo POST, PUT, PATCH tienen body** (GET y DELETE no).

**Formato más común: JSON**

```python
import requests

# POST con body JSON
nuevo_producto = {
    "nombre": "Teclado Mecánico",
    "precio": 89.99,
    "categoria": "Accesorios"
}

response = requests.post(
    "https://api.tienda.com/productos",
    json=nuevo_producto  # requests convierte a JSON automáticamente
)

print(response.status_code)  # 201 Created
print(response.json())       # {"id": 789, "nombre": "Teclado Mecánico", ...}
```

**💡 Tip:** Usa el parámetro `json=` en requests, no `data=`. Esto automáticamente:
- Convierte el dict a JSON
- Añade el header `Content-Type: application/json`

---

## 4️⃣ Query Parameters vs Path Parameters

### Path Parameters - Parte de la URL 🛤️

Se usan para **identificar un recurso específico**.

**Formato:** `/recurso/{id}`

```python
# Obtener el usuario con ID 123
GET https://api.ejemplo.com/users/123
                                 ^^^
                            Path parameter

# Obtener el pedido 456 del usuario 123
GET https://api.ejemplo.com/users/123/orders/456
                                 ^^^        ^^^
                          Path parameters
```

---

### Query Parameters - Filtros y Opciones 🔍

Se usan para **filtrar, ordenar o configurar** la respuesta.

**Formato:** `?key1=value1&key2=value2`

```python
# Filtrar usuarios activos, ordenados por nombre, máximo 50 resultados
GET https://api.ejemplo.com/users?status=active&sort=name&limit=50
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                     Query parameters

# Paginación con offset/limit
GET https://api.ejemplo.com/products?offset=100&limit=50
# Devuelve productos 101-150
```

**En Python con requests:**
```python
params = {
    "status": "active",
    "sort": "name",
    "limit": 50
}

response = requests.get(
    "https://api.ejemplo.com/users",
    params=params  # requests construye la URL automáticamente
)

# URL final: https://api.ejemplo.com/users?status=active&sort=name&limit=50
```

**💡 Regla práctica:**
- **Path parameters:** Identificar recursos (`/users/123`)
- **Query parameters:** Filtrar, ordenar, paginar (`?status=active&limit=10`)

---

## 5️⃣ Autenticación: Quién Eres en la API 🔐

Las APIs necesitan saber **quién eres** para:
1. Controlar el acceso (no todos pueden ver todo)
2. Aplicar rate limiting (X requests por usuario)
3. Cobrar según uso (APIs de pago)

### Método 1: API Key 🔑

**Analogía:** Como una tarjeta de socio de un club.

La **API Key** es un string único que te identifica.

**Ejemplo:**
```python
import requests

headers = {
    "X-API-Key": "sk_live_51abc123def456..."  # Tu API key
}

response = requests.get(
    "https://api.clima.com/weather?city=Madrid",
    headers=headers
)
```

**Dónde se pone:**
- **Header** (más común): `X-API-Key: tu-key`
- **Query parameter** (menos seguro): `?api_key=tu-key`

**✅ Ventajas:**
- Muy simple de implementar
- No expira (dura años)

**❌ Desventajas:**
- Si se filtra, alguien puede usarla
- No tiene fecha de expiración automática

**💡 Tip:** Guarda tu API key en una variable de entorno, **nunca en el código:**

```python
import os

API_KEY = os.getenv("WEATHER_API_KEY")  # Lee de variable de entorno
headers = {"X-API-Key": API_KEY}
```

---

### Método 2: Bearer Token (JWT) 🎫

**Analogía:** Como un ticket de concierto con fecha de expiración.

El **Bearer Token** (generalmente JWT - JSON Web Token) es un token **temporal**.

**Ejemplo:**
```python
import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

response = requests.get(
    "https://api.ejemplo.com/users/me",
    headers=headers
)
```

**Flujo típico:**
1. Haces login con usuario/contraseña
2. El servidor te da un token (válido por 1 hora, 1 día, etc.)
3. Usas ese token en todos los requests
4. Cuando expira, vuelves a hacer login para obtener uno nuevo

**✅ Ventajas:**
- Más seguro (expira automáticamente)
- Puede contener información (roles, permisos)
- Usado en OAuth 2.0

**❌ Desventajas:**
- Más complejo de implementar
- Necesitas refrescar el token periódicamente

---

### Método 3: Basic Auth 🔒

**Analogía:** Como dar tu usuario y contraseña cada vez que entras.

Envías **usuario:contraseña** codificados en base64 en cada request.

**Ejemplo:**
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    "https://api.ejemplo.com/data",
    auth=HTTPBasicAuth("usuario", "contraseña")
)

# Equivalente manual:
import base64

credentials = base64.b64encode(b"usuario:contraseña").decode()
headers = {
    "Authorization": f"Basic {credentials}"
}
```

**⚠️ Problema de seguridad:**
- Envías tus credenciales en **cada request**
- Si alguien intercepta el tráfico, obtiene tu usuario y contraseña
- **Solo usar con HTTPS** (nunca con HTTP)

**Cuándo se usa:**
- APIs internas corporativas
- Servicios legacy (antiguos)
- No recomendado para APIs públicas modernas

---

### 📊 Comparación de Métodos de Autenticación

| Método           | Seguridad | Expiración | Complejidad | Uso común             |
| ---------------- | --------- | ---------- | ----------- | --------------------- |
| **API Key**      | Media     | No         | Baja        | APIs públicas simples |
| **Bearer Token** | Alta      | Sí         | Media       | APIs modernas (OAuth) |
| **Basic Auth**   | Baja      | No         | Baja        | APIs internas/legacy  |

**💡 Recomendación:** Usa **Bearer Token** para APIs nuevas, **API Key** para APIs públicas simples.

---

## 6️⃣ Rate Limiting: No Sobrecargues el Servidor 🚦

**Analogía:** Como el **límite de velocidad en una carretera**.

El **rate limiting** es una restricción de cuántos requests puedes hacer en un período de tiempo.

**Ejemplo típico:**
- 100 requests por minuto
- 1,000 requests por hora
- 10,000 requests por día

### ¿Por qué existe?

1. **Proteger el servidor** de sobrecarga
2. **Distribuir recursos** equitativamente entre usuarios
3. **Evitar abuso** (bots maliciosos)
4. **Monetizar** (planes gratuitos tienen límites bajos, planes pagos más altos)

### ¿Qué pasa si superas el límite?

El servidor responde con **429 Too Many Requests**:

```python
response = requests.get("https://api.ejemplo.com/data")
print(response.status_code)  # 429

print(response.headers)
# Retry-After: 60  (espera 60 segundos antes de reintentar)
# X-RateLimit-Limit: 100  (límite total)
# X-RateLimit-Remaining: 0  (requests restantes)
# X-RateLimit-Reset: 1698765432  (timestamp cuando se resetea)
```

### ✅ Buenas Prácticas

1. **Lee la documentación:** Cada API tiene sus propios límites
2. **Monitorea los headers:** `X-RateLimit-Remaining` te dice cuántos requests te quedan
3. **Implementa backoff:** Si recibes 429, espera el tiempo indicado en `Retry-After`
4. **No hagas requests innecesarios:** Cachea respuestas cuando sea posible
5. **Usa batch endpoints:** Si la API lo permite, procesa múltiples items en un request

**Ejemplo de código respetuoso:**
```python
import time
import requests

def hacer_request_con_rate_limit(url, max_requests_por_segundo=2):
    """Hace requests respetando rate limit."""
    tiempo_entre_requests = 1.0 / max_requests_por_segundo

    response = requests.get(url)

    if response.status_code == 429:
        # Espera el tiempo indicado por el servidor
        retry_after = int(response.headers.get("Retry-After", 60))
        print(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
        time.sleep(retry_after)
        return hacer_request_con_rate_limit(url)  # Reintenta

    time.sleep(tiempo_entre_requests)  # Espera antes del siguiente request
    return response
```

---

## 7️⃣ Paginación: Manejando Grandes Cantidades de Datos 📄

**Problema:** Una API tiene 10,000 usuarios. No puedes devolver todos en un solo request (sería demasiado lento y pesado).

**Solución:** **Paginación** - Dividir los resultados en "páginas" más pequeñas.

### Método 1: Offset/Limit (Paginación por Número) 🔢

**Analogía:** Como los resultados de Google (página 1, 2, 3...).

**Parámetros:**
- `limit`: Cuántos resultados por página (ej: 50)
- `offset`: Desde qué posición empezar (ej: 100 = empezar desde el elemento 101)

**Ejemplo:**
```python
# Página 1 (usuarios 1-50)
GET /users?limit=50&offset=0

# Página 2 (usuarios 51-100)
GET /users?limit=50&offset=50

# Página 3 (usuarios 101-150)
GET /users?limit=50&offset=100
```

**En Python:**
```python
def obtener_todos_usuarios_offset(base_url, limite_por_pagina=100):
    """Itera todas las páginas usando offset/limit."""
    todos_usuarios = []
    offset = 0

    while True:
        response = requests.get(
            f"{base_url}/users",
            params={"limit": limite_por_pagina, "offset": offset}
        )

        usuarios = response.json()

        if not usuarios:  # No hay más resultados
            break

        todos_usuarios.extend(usuarios)
        offset += limite_por_pagina

    return todos_usuarios
```

**✅ Ventajas:**
- Simple de entender
- Puedes saltar a cualquier página directamente

**❌ Desventajas:**
- Problemas si los datos cambian mientras paginas (puedes perder o duplicar registros)
- Ineficiente en bases de datos grandes (OFFSET es lento)

---

### Método 2: Cursor-based (Paginación por Cursor) 🔗

**Analogía:** Como marcar tu lugar en un libro con un marcador.

**Parámetros:**
- `cursor`: Un token único que indica "desde dónde seguir"

**Ejemplo:**
```python
# Primera página
GET /users?limit=50
Response: {
    "data": [...50 usuarios...],
    "pagination": {
        "next_cursor": "eyJpZCI6MTUwfQ=="
    }
}

# Segunda página (usa el cursor de la respuesta anterior)
GET /users?limit=50&cursor=eyJpZCI6MTUwfQ==
Response: {
    "data": [...50 usuarios...],
    "pagination": {
        "next_cursor": "eyJpZCI6MjAwfQ=="
    }
}

# Última página (no hay next_cursor)
Response: {
    "data": [...23 usuarios...],
    "pagination": {
        "next_cursor": null
    }
}
```

**En Python:**
```python
def obtener_todos_usuarios_cursor(base_url):
    """Itera todas las páginas usando cursores."""
    todos_usuarios = []
    cursor = None

    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(f"{base_url}/users", params=params)
        data = response.json()

        todos_usuarios.extend(data["data"])

        cursor = data.get("pagination", {}).get("next_cursor")
        if not cursor:  # No hay más páginas
            break

    return todos_usuarios
```

**✅ Ventajas:**
- Consistente (no se pierden registros si los datos cambian)
- Eficiente en bases de datos grandes
- Usado por APIs modernas (Facebook, Twitter, Stripe)

**❌ Desventajas:**
- No puedes saltar a una página específica (ej: página 10)
- Más complejo de implementar

---

### 📊 Comparación: Offset vs Cursor

| Aspecto              | Offset/Limit                  | Cursor                     |
| -------------------- | ----------------------------- | -------------------------- |
| **Simplicidad**      | ✅ Muy simple                  | ⚠️ Más complejo             |
| **Saltar páginas**   | ✅ Sí (`offset=500`)           | ❌ No (secuencial)          |
| **Consistencia**     | ❌ Puede duplicar/perder datos | ✅ Consistente              |
| **Performance**      | ❌ Lento en tablas grandes     | ✅ Rápido                   |
| **APIs que lo usan** | Antiguas, simples             | Modernas (Twitter, Stripe) |

**💡 Recomendación:** Usa **Cursor** si la API lo soporta (más robusto).

---

## 8️⃣ Manejo de Errores y Reintentos 🔄

### Errores Temporales vs Permanentes

**Errores temporales (reintentar):**
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout
- 429 Too Many Requests

**Errores permanentes (NO reintentar):**
- 400 Bad Request (tu request está mal)
- 401 Unauthorized (falta autenticación)
- 403 Forbidden (no tienes permiso)
- 404 Not Found (el recurso no existe)

### Exponential Backoff: La Estrategia Inteligente ⏱️

**Problema:** Si el servidor está sobrecargado, reintentar inmediatamente lo empeora.

**Solución:** Espera cada vez más tiempo entre reintentos (2s → 4s → 8s → 16s...).

**Fórmula:**
```
delay = base^intento
delay = 2^1 = 2 segundos
delay = 2^2 = 4 segundos
delay = 2^3 = 8 segundos
delay = 2^4 = 16 segundos
```

**Implementación:**
```python
import time
import requests

def hacer_request_con_reintentos(url, max_intentos=3):
    """Hace request con reintentos exponenciales."""
    for intento in range(1, max_intentos + 1):
        try:
            response = requests.get(url, timeout=30)

            # Éxito
            if response.status_code == 200:
                return response

            # Error temporal (reintentar)
            if response.status_code in [500, 502, 503, 504, 429]:
                if intento < max_intentos:
                    delay = 2 ** intento  # Exponential backoff
                    print(f"Error {response.status_code}. Reintentando en {delay}s...")
                    time.sleep(delay)
                    continue

            # Error permanente (no reintentar)
            if 400 <= response.status_code < 500:
                raise ValueError(f"Error permanente {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            if intento < max_intentos:
                delay = 2 ** intento
                print(f"Timeout. Reintentando en {delay}s...")
                time.sleep(delay)
                continue

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error de conexión: {e}")

    raise RuntimeError(f"Falló después de {max_intentos} intentos")
```

**💡 Mejoras opcionales:**
- **Jitter:** Añade un random de ±10% al delay para evitar que todos los clientes reintentan al mismo tiempo
- **Max delay:** Limita el delay máximo (ej: 60 segundos)
- **Retry-After header:** Si el servidor lo envía, úsalo en lugar de exponential backoff

---

## 9️⃣ HTTPS Obligatorio: Seguridad Primero 🔒

**Regla de oro:** **NUNCA uses HTTP en producción. Solo HTTPS.**

### ¿Por qué?

**HTTP (inseguro):**
```
Cliente ----[datos en texto plano]----> Servidor
       ^
       |
    Hacker puede leer TODO (contraseñas, datos personales, API keys)
```

**HTTPS (seguro):**
```
Cliente ----[datos ENCRIPTADOS]----> Servidor
       ^
       |
    Hacker solo ve "basura encriptada" (no puede leer nada)
```

### En tu código

**✅ Correcto:**
```python
response = requests.get("https://api.ejemplo.com/users")  # HTTPS ✅
```

**❌ NUNCA hagas esto:**
```python
response = requests.get("http://api.ejemplo.com/users")  # HTTP ❌ INSEGURO
```

### Validación automática

**Implementa validación en tu código:**
```python
def validar_url(url: str) -> None:
    """Valida que la URL sea HTTPS."""
    if not url.startswith("https://"):
        raise ValueError(f"URL insegura. Solo se permite HTTPS: {url}")

# Uso
validar_url("http://api.com/data")  # ❌ Lanza error
validar_url("https://api.com/data")  # ✅ OK
```

**💡 Esto previene errores de seguridad accidentales en tu equipo.**

---

## 📚 Aplicaciones Prácticas en Data Engineering

### Caso de Uso 1: Extracción Diaria de Ventas

**Contexto:** Necesitas extraer las ventas de ayer de la API de tu e-commerce.

**Implementación:**
```python
import requests
from datetime import datetime, timedelta

def extraer_ventas_ayer():
    """Extrae ventas de ayer de la API."""
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    response = requests.get(
        "https://api.tienda.com/ventas",
        params={
            "fecha_inicio": ayer,
            "fecha_fin": ayer,
            "limit": 1000
        },
        headers={"X-API-Key": os.getenv("API_KEY")},
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"Error al extraer ventas: {response.status_code}")

    return response.json()
```

**Pipeline ETL:**
```
1. EXTRACT: Llamar API → obtener ventas
2. TRANSFORM: Limpiar datos (nulos, duplicados)
3. LOAD: Guardar en data warehouse (Snowflake, BigQuery)
```

---

### Caso de Uso 2: Sincronización de Datos de CRM

**Contexto:** Tu empresa usa Salesforce. Necesitas sincronizar contactos cada hora.

**Implementación:**
```python
def sincronizar_contactos_salesforce():
    """Sincroniza contactos de Salesforce a tu base de datos."""
    # 1. Autenticación OAuth (obtener token)
    token = obtener_token_salesforce()

    # 2. Obtener contactos modificados en la última hora
    hora_atras = (datetime.now() - timedelta(hours=1)).isoformat()

    response = requests.get(
        "https://api.salesforce.com/data/v58.0/contacts",
        params={
            "modifiedAfter": hora_atras,
            "limit": 500
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    contactos = response.json()["data"]

    # 3. Guardar en tu base de datos
    guardar_en_postgres(contactos)
```

**Ventajas de usar API:**
- Solo extraes cambios recientes (incremental)
- No sobrecargas el sistema
- Más rápido que full refresh

---

### Caso de Uso 3: Monitoreo de Métricas en Tiempo Real

**Contexto:** Dashboard que muestra métricas cada 5 minutos.

**Implementación:**
```python
import time

def monitorear_metricas():
    """Consulta métricas cada 5 minutos."""
    while True:
        response = requests.get(
            "https://api.analytics.com/metricas/tiempo-real",
            headers={"Authorization": f"Bearer {token}"}
        )

        metricas = response.json()

        # Actualizar dashboard
        actualizar_dashboard(metricas)

        # Esperar 5 minutos antes del siguiente request
        time.sleep(300)
```

---

## ❌ 5 Errores Comunes al Consumir APIs

### Error 1: No Validar Status Codes ⚠️

**❌ Mal:**
```python
response = requests.get(url)
data = response.json()  # ¡Puede fallar si status != 200!
```

**✅ Bien:**
```python
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    raise RuntimeError(f"Error {response.status_code}: {response.text}")
```

---

### Error 2: Hardcodear API Keys en el Código 🔐

**❌ Mal:**
```python
API_KEY = "sk_live_51abc123..."  # ¡Expuesto en Git!
```

**✅ Bien:**
```python
import os
API_KEY = os.getenv("API_KEY")  # Lee de variable de entorno
if not API_KEY:
    raise ValueError("API_KEY no configurada")
```

---

### Error 3: No Respetar Rate Limiting 🚦

**❌ Mal:**
```python
for i in range(1000):
    requests.get(f"https://api.com/users/{i}")  # ¡1000 requests instantáneos!
```

**✅ Bien:**
```python
import time
for i in range(1000):
    requests.get(f"https://api.com/users/{i}")
    time.sleep(0.5)  # Espera 0.5s entre requests (2 req/segundo)
```

---

### Error 4: No Manejar Timeouts ⏱️

**❌ Mal:**
```python
response = requests.get(url)  # Puede esperar PARA SIEMPRE
```

**✅ Bien:**
```python
response = requests.get(url, timeout=30)  # Falla después de 30 segundos
```

---

### Error 5: Procesar Todo en Memoria 💾

**❌ Mal:**
```python
response = requests.get("https://api.com/users")  # 1 millón de usuarios
users = response.json()  # ¡Explota la memoria!
```

**✅ Bien:**
```python
# Procesar en lotes con paginación
for pagina in range(total_paginas):
    response = requests.get(f"https://api.com/users?page={pagina}&limit=100")
    users = response.json()
    procesar_lote(users)  # Procesa 100 a la vez
```

---

## ✅ Buenas Prácticas al Consumir APIs

1. **✅ Valida siempre status codes** antes de procesar la respuesta
2. **✅ Usa HTTPS** exclusivamente (nunca HTTP)
3. **✅ Guarda API keys en variables de entorno**, no en el código
4. **✅ Implementa timeouts** en todos los requests (30 segundos recomendado)
5. **✅ Respeta rate limiting** (lee la documentación de la API)
6. **✅ Implementa reintentos con exponential backoff** para errores 5xx
7. **✅ Usa paginación** para datasets grandes (no cargues todo en memoria)
8. **✅ Cachea respuestas** cuando sea posible (reduce requests innecesarios)
9. **✅ Loggea errores** para debugging (no falles silenciosamente)
10. **✅ Lee la documentación** de la API antes de empezar

---

## 🎓 Checklist de Aprendizaje

Verifica que puedes hacer lo siguiente:

- [ ] Explicar qué es una API REST y por qué es importante en Data Engineering
- [ ] Usar los 4 métodos HTTP (GET, POST, PUT, DELETE) correctamente
- [ ] Interpretar status codes (2xx, 3xx, 4xx, 5xx) y actuar en consecuencia
- [ ] Enviar headers y body en un request
- [ ] Diferenciar entre path parameters y query parameters
- [ ] Autenticar con API Key, Bearer Token y Basic Auth
- [ ] Implementar rate limiting en tu código
- [ ] Iterar páginas de resultados (offset/limit y cursor)
- [ ] Implementar reintentos con exponential backoff
- [ ] Validar que solo usas HTTPS (nunca HTTP)
- [ ] Guardar API keys en variables de entorno
- [ ] Manejar errores correctamente (no fallar silenciosamente)

**Si puedes hacer todo esto, ¡estás listo para el proyecto práctico!** 🚀

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Requests Library (Python)](https://requests.readthedocs.io/)
- [HTTP Status Codes - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Tutorial](https://restfulapi.net/)

### APIs Públicas para Practicar
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - API fake para testing
- [OpenWeather API](https://openweathermap.org/api) - Datos del clima (gratuita)
- [GitHub API](https://docs.github.com/en/rest) - Datos de repositorios
- [The Cat API](https://thecatapi.com/) - API de gatos (sí, en serio)

### Herramientas Útiles
- [Postman](https://www.postman.com/) - Cliente para probar APIs visualmente
- [httpie](https://httpie.io/) - Cliente HTTP en línea de comandos (más amigable que curl)
- [RequestBin](https://requestbin.com/) - Inspecciona requests HTTP en tiempo real

---

**¡Felicidades!** Has completado la teoría fundamental de APIs REST. 🎉

**Próximo paso:** Ve a `02-EJEMPLOS.md` para ver ejemplos trabajados paso a paso.

---

*Última actualización: 2025-10-23*
*Tiempo de lectura: 30-45 minutos*
