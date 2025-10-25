# 📘 Tema 3: Rate Limiting y Caching - Optimización de Extracción de Datos

**Módulo 4:** APIs y Web Scraping
**Duración estimada:** 20-30 minutos de lectura
**Nivel:** Intermedio-Avanzado
**Prerequisitos:** Tema 1 (APIs REST), Tema 2 (Web Scraping)

---

## 🎯 Introducción

Imagina que has construido un scraper que extrae información de 10,000 productos de un e-commerce. Con los conocimientos de los temas anteriores, podrías tardar **3-4 horas** en completar la tarea. ¿Y si pudieras reducir ese tiempo a **menos de 10 minutos** sin violar ninguna regla ética?

Bienvenido al mundo de la **optimización de extracción de datos**.

### ¿Por qué optimizar?

En Data Engineering, frecuentemente necesitas:

- **Extraer millones de registros** de APIs REST
- **Actualizar datos cada hora** desde múltiples fuentes
- **Scrapear catálogos completos** de sitios web
- **Procesar datos en tiempo real** sin sobrecargar servidores

Sin optimización, estos procesos pueden ser:
- ❌ **Lentos** (días en completar)
- ❌ **Costosos** (miles de requests innecesarias)
- ❌ **Bloqueados** (exceder rate limits)
- ❌ **Poco éticos** (sobrecargar servidores)

Con optimización, puedes lograr:
- ✅ **10-100x más rápido** (con async)
- ✅ **90% menos requests** (con caching)
- ✅ **0 bloqueos** (respetando rate limits)
- ✅ **Ético y sostenible**

---

## 📚 Conceptos Fundamentales

### 1. Rate Limiting - Controlar la Velocidad de Requests

> **Analogía:** Es como el límite de velocidad en una carretera. Puedes conducir, pero no a cualquier velocidad. El objetivo es mantener el tráfico fluido y seguro para todos.

#### ¿Qué es Rate Limiting?

**Rate limiting** es la práctica de limitar el número de requests HTTP que puedes hacer en un período de tiempo determinado. Puede ser:

**Impuesto por el servidor:**
- "Máximo 100 requests por minuto"
- Si excedes el límite → recibes **429 Too Many Requests**
- Ejemplo: Twitter API permite 900 requests cada 15 minutos

**Auto-impuesto (cortesía):**
- Tú decides limitar tu velocidad para no sobrecargar el servidor
- Ejemplo: Esperar 2 segundos entre cada request de scraping
- **Es lo ético cuando scrapeas sitios sin API**

#### ¿Por qué existe?

**Desde el punto de vista del servidor:**
1. **Prevenir abuso:** Evitar que un solo cliente monopolice recursos
2. **Controlar costos:** Limitar uso de ancho de banda y procesamiento
3. **Seguridad:** Detectar y mitigar ataques DDoS
4. **Monetización:** APIs gratuitas con límites, premium sin límites

**Desde tu punto de vista (Data Engineer):**
1. **No ser bloqueado:** Evitar el error 429 y bloqueos de IP
2. **Cortesía:** No sobrecargar servidores de terceros
3. **Ética:** Scrapear responsablemente
4. **Sostenibilidad:** Mantener acceso a largo plazo

#### Estrategias de Rate Limiting

##### 1.1. Fixed Window (Ventana Fija)

**Concepto:** Límite fijo de requests por intervalo de tiempo.

```
Ejemplo: 100 requests por minuto
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Minuto 1   │ │  Minuto 2   │ │  Minuto 3   │
│  100 reqs   │ │  100 reqs   │ │  100 reqs   │
└─────────────┘ └─────────────┘ └─────────────┘
     ✅             ✅             ✅
```

**Ventajas:**
- ✅ Simple de implementar
- ✅ Fácil de entender

**Desventajas:**
- ❌ Puede permitir "burst" de requests al inicio del período
- ❌ Ejemplo: 100 requests a las 12:00:59, otros 100 a las 12:01:00 (200 requests en 2 segundos)

**Caso de uso:** APIs que usan este método (GitHub, Stripe)

##### 1.2. Sliding Window (Ventana Deslizante)

**Concepto:** Límite de requests en los **últimos** N segundos.

```
Límite: 100 requests en 60 segundos

Tiempo actual: 12:00:30
Cuenta requests desde: 12:00:30 - 60s = 11:59:30

Tiempo actual: 12:00:35
Cuenta requests desde: 12:00:35 - 60s = 11:59:35
```

**Ventajas:**
- ✅ Más justo, evita bursts
- ✅ Distribución más uniforme

**Desventajas:**
- ❌ Más complejo de implementar
- ❌ Requiere rastrear timestamp de cada request

**Caso de uso:** APIs más sofisticadas (AWS)

##### 1.3. Token Bucket (Cubeta de Tokens)

**Concepto:** Tienes una "cubeta" con tokens. Cada request consume 1 token. La cubeta se rellena a una velocidad constante.

```
Capacidad de cubeta: 100 tokens
Velocidad de relleno: 10 tokens/segundo

Inicio:     [●●●●●●●●●● ... 100 tokens]
Request 1:  [●●●●●●●●●● ... 99 tokens]  ✅
Request 2:  [●●●●●●●●●● ... 98 tokens]  ✅
...
Request 100:[●●●●●●●●●● ... 0 tokens]   ✅
Request 101:[]                          ❌ Esperar 0.1 seg
+0.1 seg:   [●]                         (1 token generado)
Request 101:[●]                         ✅
```

**Ventajas:**
- ✅ Permite bursts controlados (útil para cargas variables)
- ✅ Flexible y adaptable
- ✅ Usado por sistemas distribuidos (Redis, AWS Lambda)

**Desventajas:**
- ❌ Más complejo de implementar

**Caso de uso:** Sistemas de alto rendimiento, microservicios

#### Implementación Básica en Python

**Fixed Window simple con `time.sleep()`:**

```python
import time

def rate_limited_scraper(urls: list, delay_seconds: float = 1.0):
    """Scraper con rate limiting básico."""
    resultados = []

    for url in urls:
        # Hacer request
        data = hacer_request(url)
        resultados.append(data)

        # Esperar delay antes del siguiente request
        time.sleep(delay_seconds)

    return resultados

# Uso: 100 URLs con 2 segundos entre cada una
# Tiempo total: 100 * 2 = 200 segundos = 3.3 minutos
resultados = rate_limited_scraper(urls, delay_seconds=2.0)
```

**Token Bucket avanzado:**

```python
import time

class TokenBucket:
    def __init__(self, capacidad: int, tasa_reposicion: float):
        """
        capacidad: Máximo número de tokens
        tasa_reposicion: Tokens generados por segundo
        """
        self.capacidad = capacidad
        self.tasa = tasa_reposicion
        self.tokens = capacidad
        self.ultima_actualizacion = time.time()

    def consumir(self, tokens: int = 1) -> bool:
        """Intenta consumir tokens. Retorna True si hay disponibles."""
        ahora = time.time()

        # Generar nuevos tokens según tiempo transcurrido
        tiempo_transcurrido = ahora - self.ultima_actualizacion
        nuevos_tokens = tiempo_transcurrido * self.tasa
        self.tokens = min(self.capacidad, self.tokens + nuevos_tokens)
        self.ultima_actualizacion = ahora

        # Consumir tokens si hay disponibles
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def esperar_disponibilidad(self, tokens: int = 1):
        """Espera hasta que haya tokens disponibles."""
        while not self.consumir(tokens):
            time.sleep(0.1)

# Uso: 100 requests/minuto
bucket = TokenBucket(capacidad=100, tasa_reposicion=100/60)  # 1.67 tokens/seg

for url in urls:
    bucket.esperar_disponibilidad()
    hacer_request(url)
```

---

### 2. Caching - Almacenar Respuestas para Reutilizar

> **Analogía:** Es como tomar apuntes en clase. La primera vez, escuchas la explicación (request HTTP lento). Las siguientes veces, solo consultas tus apuntes (cache rápido). No necesitas volver a preguntar al profesor cada vez.

#### ¿Qué es Caching?

**Caching** es la práctica de **almacenar respuestas de requests HTTP** para reutilizarlas sin hacer el request nuevamente.

**Escenario sin cache:**
```
Request 1 → API → Response (500ms)
Request 2 → API → Response (500ms)  [MISMO dato que Request 1]
Request 3 → API → Response (500ms)  [MISMO dato que Request 1]

Tiempo total: 1,500ms
Requests realizadas: 3
```

**Escenario con cache:**
```
Request 1 → API → Response (500ms) → [Guardar en cache]
Request 2 → Cache → Response (1ms)   [Leer de cache]
Request 3 → Cache → Response (1ms)   [Leer de cache]

Tiempo total: 502ms (3x más rápido)
Requests realizadas: 1 (66% menos tráfico)
```

#### ¿Cuándo usar Cache?

**✅ Casos ideales para caching:**

1. **Datos que cambian poco**
   - Catálogo de productos (actualiza 1 vez al día)
   - Datos históricos (no cambian nunca)
   - Metadatos de configuración

2. **Requests costosos**
   - APIs de pago ($0.01 por request)
   - APIs lentas (>5 segundos por response)
   - Scraping de sitios lentos

3. **Requests repetidos**
   - Múltiples análisis sobre los mismos datos
   - Re-ejecuciones de scripts durante desarrollo
   - Pipelines que se ejecutan frecuentemente

**❌ Casos donde NO usar cache:**

1. **Datos en tiempo real**
   - Cotizaciones de bolsa (cambian cada segundo)
   - Clima actual (cambia cada minuto)
   - Estado de pedidos (cambia constantemente)

2. **Datos personalizados**
   - Dependen del usuario autenticado
   - Dependen de parámetros únicos

3. **Requests únicos**
   - Solo se hace una vez (no vale la pena el overhead)

#### Tipos de Cache

##### 2.1. Cache en Memoria (RAM)

**Almacenamiento:** Diccionario Python en memoria

**Ventajas:**
- ✅ **Ultra rápido** (acceso en nanosegundos)
- ✅ **Simple de implementar** (solo un `dict`)

**Desventajas:**
- ❌ **Se pierde al reiniciar** el programa
- ❌ **Limitado por RAM** disponible

**Caso de uso:** Cache temporal durante ejecución de un script

**Implementación:**

```python
# Cache simple con diccionario
cache_memoria = {}

def obtener_con_cache(url: str) -> dict:
    """Obtiene datos de API con cache en memoria."""
    if url in cache_memoria:
        print(f"✅ Cache HIT: {url}")
        return cache_memoria[url]

    print(f"🌐 Cache MISS: {url} - Haciendo request...")
    response = requests.get(url)
    data = response.json()

    cache_memoria[url] = data
    return data

# Uso
data1 = obtener_con_cache("https://api.example.com/users/1")  # Request real
data2 = obtener_con_cache("https://api.example.com/users/1")  # Desde cache (instantáneo)
```

##### 2.2. Cache en Disco (Persistente)

**Almacenamiento:** Archivos en disco (JSON, pickle, shelve, SQLite)

**Ventajas:**
- ✅ **Persiste entre ejecuciones** del programa
- ✅ **No limitado por RAM** (usa disco)
- ✅ **Compartible** entre procesos

**Desventajas:**
- ❌ **Más lento que memoria** (acceso en milisegundos)
- ❌ **Requiere gestión** de archivos

**Caso de uso:** Cache para datos de APIs costosas que cambian lentamente

**Implementación con `shelve`:**

```python
import shelve

def obtener_con_cache_disco(url: str) -> dict:
    """Obtiene datos con cache persistente en disco."""
    with shelve.open("cache_api.db") as cache:
        if url in cache:
            print(f"✅ Cache HIT: {url}")
            return cache[url]

        print(f"🌐 Cache MISS: {url} - Haciendo request...")
        response = requests.get(url)
        data = response.json()

        cache[url] = data
        return data

# Uso
data = obtener_con_cache_disco("https://api.example.com/products")
# Segunda ejecución (incluso después de reiniciar Python) → desde cache
```

##### 2.3. Cache Distribuido (Redis, Memcached)

**Almacenamiento:** Servidor de cache dedicado (Redis)

**Ventajas:**
- ✅ **Ultra rápido** (Redis en RAM)
- ✅ **Compartido** entre múltiples aplicaciones
- ✅ **TTL automático** (expiración)
- ✅ **Alta disponibilidad**

**Desventajas:**
- ❌ **Requiere servidor Redis** corriendo
- ❌ **Más complejo** de configurar

**Caso de uso:** Sistemas distribuidos, microservicios, producción

**Implementación con Redis:**

```python
import redis
import json

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def obtener_con_redis(url: str, ttl: int = 3600) -> dict:
    """
    Obtiene datos con cache en Redis.

    Args:
        url: URL de la API
        ttl: Tiempo de vida en segundos (3600 = 1 hora)
    """
    # Intentar obtener de Redis
    cached = r.get(url)
    if cached:
        print(f"✅ Cache HIT: {url}")
        return json.loads(cached)

    # Request real si no está en cache
    print(f"🌐 Cache MISS: {url}")
    response = requests.get(url)
    data = response.json()

    # Guardar en Redis con TTL
    r.setex(url, ttl, json.dumps(data))
    return data

# Uso
data = obtener_con_redis("https://api.example.com/data", ttl=7200)  # Cache 2 horas
```

#### TTL (Time To Live) - Tiempo de Expiración

**Concepto:** El cache no debe durar para siempre. Después de cierto tiempo, los datos se consideran "obsoletos" y se hace un request fresco.

```python
import time

cache_con_ttl = {}

def obtener_con_ttl(url: str, ttl: int = 60) -> dict:
    """
    Cache con expiración automática.

    Args:
        url: URL de la API
        ttl: Tiempo de vida en segundos
    """
    ahora = time.time()

    # Verificar si existe y no ha expirado
    if url in cache_con_ttl:
        datos, timestamp = cache_con_ttl[url]
        if ahora - timestamp < ttl:
            print(f"✅ Cache válido (edad: {int(ahora - timestamp)}s)")
            return datos
        else:
            print(f"⏰ Cache expirado (edad: {int(ahora - timestamp)}s > {ttl}s)")

    # Request fresco
    response = requests.get(url)
    data = response.json()
    cache_con_ttl[url] = (data, ahora)
    return data

# Uso
data1 = obtener_con_ttl("https://api.example.com/weather", ttl=300)  # Cache 5 min
time.sleep(60)
data2 = obtener_con_ttl("https://api.example.com/weather", ttl=300)  # Aún válido
time.sleep(300)
data3 = obtener_con_ttl("https://api.example.com/weather", ttl=300)  # Expiró, request nuevo
```

**Guía de TTL según tipo de dato:**

| Tipo de Dato        | TTL Recomendado  | Ejemplo                       |
| ------------------- | ---------------- | ----------------------------- |
| **Estático**        | 1 semana - 1 mes | Países, códigos postales      |
| **Semi-estático**   | 1 día - 1 semana | Catálogo de productos         |
| **Dinámico**        | 1 hora - 1 día   | Precios, inventario           |
| **Tiempo real**     | 1-5 minutos      | Clima, tráfico                |
| **Ultra real-time** | No cachear       | Cotizaciones de bolsa en vivo |

---

### 3. Async Requests - Concurrencia para Máxima Velocidad

> **Analogía:** Imagina que necesitas lavar 10 platos. Método **síncrono**: lavas uno, esperas que se seque, lavas el siguiente (10 minutos total). Método **asíncrono**: pones todos a lavar a la vez en el lavavajillas (2 minutos total). Mucho más eficiente cuando las tareas esperan (I/O).

#### ¿Qué es Async/Await?

**Async programming** permite hacer **múltiples requests HTTP en paralelo** sin bloquear el programa mientras espera respuestas.

**Problema con requests síncronos:**

```python
import requests
import time

# Síncrono: Hace 1 request, espera, hace el siguiente
urls = ["https://api.example.com/1", "https://api.example.com/2", ...]  # 100 URLs

inicio = time.time()
resultados = []
for url in urls:
    response = requests.get(url)  # Espera 0.5 seg por cada uno
    resultados.append(response.json())

fin = time.time()
print(f"Tiempo: {fin - inicio}s")  # ~50 segundos (100 * 0.5s)
```

**Solución con async:**

```python
import aiohttp
import asyncio
import time

async def obtener_async(session, url):
    """Hace un request asíncrono."""
    async with session.get(url) as response:
        return await response.json()

async def obtener_todos(urls):
    """Obtiene todas las URLs en paralelo."""
    async with aiohttp.ClientSession() as session:
        # Lanza todos los requests EN PARALELO
        tareas = [obtener_async(session, url) for url in urls]
        return await asyncio.gather(*tareas)

# Uso
urls = ["https://api.example.com/1", ...] * 100  # 100 URLs

inicio = time.time()
resultados = asyncio.run(obtener_todos(urls))
fin = time.time()

print(f"Tiempo: {fin - inicio}s")  # ~2-3 segundos (¡20x más rápido!)
```

#### ¿Cuándo usar Async?

**✅ Casos ideales:**

1. **Muchos requests a la vez** (>10)
2. **I/O bound** (mayor parte del tiempo esperando respuestas de red)
3. **APIs rápidas** (responden en <1 segundo)
4. **Scraping masivo** con rate limiting (ej: 100 requests/seg)

**❌ Cuando NO usarlo:**

1. **Pocos requests** (<5) - overhead no vale la pena
2. **CPU bound** (procesamiento intensivo local)
3. **Rate limiting estricto** (1 request/seg) - no hay beneficio de paralelismo

#### Combinando Async + Rate Limiting + Cache

**El combo perfecto para scraping masivo:**

```python
import aiohttp
import asyncio
from typing import List, Dict
import time

class ScraperOptimizado:
    def __init__(self, max_concurrente: int = 10):
        self.cache = {}
        self.max_concurrente = max_concurrente
        self.semaforo = asyncio.Semaphore(max_concurrente)

    async def obtener_con_cache(self, session, url: str) -> dict:
        """Request asíncrono con cache y rate limiting."""
        # 1. Verificar cache
        if url in self.cache:
            print(f"✅ Cache HIT: {url}")
            return self.cache[url]

        # 2. Rate limiting con semáforo (máximo N requests concurrentes)
        async with self.semaforo:
            print(f"🌐 Request: {url}")
            async with session.get(url) as response:
                data = await response.json()

                # 3. Guardar en cache
                self.cache[url] = data

                # 4. Cortesía: pequeño delay
                await asyncio.sleep(0.1)

                return data

    async def scrapear_masivo(self, urls: List[str]) -> List[dict]:
        """Scrape masivo optimizado."""
        async with aiohttp.ClientSession() as session:
            tareas = [self.obtener_con_cache(session, url) for url in urls]
            return await asyncio.gather(*tareas)

# Uso
scraper = ScraperOptimizado(max_concurrente=20)
urls = [f"https://api.example.com/products/{i}" for i in range(1000)]

inicio = time.time()
resultados = asyncio.run(scraper.scrapear_masivo(urls))
fin = time.time()

print(f"🎉 {len(resultados)} productos en {fin-inicio:.1f}s")
print(f"⚡ Velocidad: {len(resultados)/(fin-inicio):.1f} productos/seg")
```

---

### 4. Monitoreo y Métricas

> **Analogía:** Es como el velocímetro de un auto. Sin él, no sabes si vas a 50 km/h o 150 km/h. Con métricas, puedes **medir, optimizar y mejorar**.

#### Métricas Clave

**1. Throughput (Rendimiento)**
- **Qué mide:** Requests por segundo (req/seg)
- **Fórmula:** `throughput = total_requests / tiempo_total`
- **Objetivo:** Maximizar (más req/seg = más rápido)

```python
inicio = time.time()
hacer_1000_requests()
fin = time.time()

throughput = 1000 / (fin - inicio)
print(f"Throughput: {throughput:.1f} req/seg")
```

**2. Latencia (Latency)**
- **Qué mide:** Tiempo promedio por request (milisegundos)
- **Fórmula:** `latencia = tiempo_total / total_requests`
- **Objetivo:** Minimizar (menos ms = más rápido)

```python
latencias = []
for url in urls:
    inicio = time.time()
    hacer_request(url)
    fin = time.time()
    latencias.append((fin - inicio) * 1000)  # ms

print(f"Latencia promedio: {sum(latencias)/len(latencias):.0f}ms")
```

**3. Cache Hit Rate (Tasa de Aciertos)**
- **Qué mide:** % de requests servidos desde cache
- **Fórmula:** `hit_rate = cache_hits / total_requests * 100`
- **Objetivo:** Maximizar (90%+ es excelente)

```python
cache_hits = 0
cache_misses = 0

# ... después de N requests ...

hit_rate = cache_hits / (cache_hits + cache_misses) * 100
print(f"Cache Hit Rate: {hit_rate:.1f}%")
print(f"Requests ahorrados: {cache_hits}")
```

**4. Error Rate (Tasa de Errores)**
- **Qué mide:** % de requests que fallaron
- **Fórmula:** `error_rate = errores / total_requests * 100`
- **Objetivo:** Minimizar (<1% es bueno, <0.1% es excelente)

```python
errores = 0
exitos = 0

# ... después de N requests ...

error_rate = errores / (errores + exitos) * 100
print(f"Error Rate: {error_rate:.2f}%")
```

#### Dashboard de Métricas en Vivo

```python
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class Metricas:
    """Contenedor de métricas del scraper."""
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    errores: int = 0
    inicio: float = 0.0

    def registrar_cache_hit(self):
        self.total_requests += 1
        self.cache_hits += 1

    def registrar_cache_miss(self):
        self.total_requests += 1
        self.cache_misses += 1

    def registrar_error(self):
        self.errores += 1

    def reporte(self) -> str:
        """Genera reporte de métricas."""
        tiempo = time.time() - self.inicio
        throughput = self.total_requests / tiempo if tiempo > 0 else 0
        hit_rate = self.cache_hits / self.total_requests * 100 if self.total_requests > 0 else 0
        error_rate = self.errores / self.total_requests * 100 if self.total_requests > 0 else 0

        return f"""
        📊 Métricas del Scraper
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ⏱️  Tiempo: {tiempo:.1f}s
        📝 Requests: {self.total_requests}
        ⚡ Throughput: {throughput:.1f} req/seg
        ✅ Cache Hits: {self.cache_hits} ({hit_rate:.1f}%)
        🌐 Cache Misses: {self.cache_misses}
        ❌ Errores: {self.errores} ({error_rate:.2f}%)
        """

# Uso
metricas = Metricas(inicio=time.time())

for url in urls:
    if url in cache:
        metricas.registrar_cache_hit()
    else:
        try:
            hacer_request(url)
            metricas.registrar_cache_miss()
        except:
            metricas.registrar_error()

print(metricas.reporte())
```

---

## ⚖️ Comparación: Antes vs Después de Optimizar

### Caso de Estudio: Scraping de 1,000 Productos

**Escenario:** Necesitas extraer datos de 1,000 productos de una API. Cada request tarda ~500ms.

| Técnica                        | Requests Reales | Tiempo        | Throughput  | Mejora               |
| ------------------------------ | --------------- | ------------- | ----------- | -------------------- |
| **Síncrono sin cache**         | 1,000           | 500s (~8 min) | 2 req/seg   | Baseline             |
| **+ Cache (50% hit rate)**     | 500             | 250s (~4 min) | 4 req/seg   | 2x más rápido        |
| **+ Rate limiting (cortesía)** | 500             | 300s (~5 min) | 3.3 req/seg | Ético ✅              |
| **+ Async (20 concurrentes)**  | 500             | 15s           | 66 req/seg  | **33x más rápido** 🚀 |

**Resultado final:** De **8 minutos** a **15 segundos** (33x mejora) siendo **ético** y **respetando rate limits**.

---

## 🎯 Aplicaciones en Data Engineering

### 1. ETL Pipelines Optimizados

```python
# Pipeline ETL con optimización completa
async def pipeline_etl_optimizado():
    """Extrae, transforma y carga datos optimizadamente."""

    # EXTRACT (async + cache)
    urls = generar_urls(n=10000)
    scraper = ScraperOptimizado(max_concurrente=50)
    datos_raw = await scraper.scrapear_masivo(urls)

    # TRANSFORM (procesamiento local)
    datos_limpios = [limpiar(d) for d in datos_raw]

    # LOAD (batch insert)
    guardar_en_bd(datos_limpios, batch_size=1000)

    print("✅ ETL completado en tiempo récord")
```

### 2. Actualización Incremental

```python
# Solo actualizar datos que cambiaron (con cache inteligente)
def actualizar_incremental():
    """Actualiza solo datos modificados desde última ejecución."""
    ultima_ejecucion = obtener_timestamp_ultima_ejecucion()

    # Request solo endpoints que pueden haber cambiado
    urls_a_actualizar = []
    for producto in productos_en_bd:
        if producto.ultima_actualizacion < ultima_ejecucion:
            urls_a_actualizar.append(producto.url_api)

    # El resto viene de cache
    datos_actualizados = obtener_con_cache(urls_a_actualizar)
    actualizar_bd(datos_actualizados)
```

### 3. Monitoreo en Tiempo Real

```python
# Dashboard de métricas para monitorear scrapers de producción
def monitorear_scraper_produccion():
    """Envía métricas a sistema de monitoreo (ej: Grafana)."""
    metricas = obtener_metricas_actuales()

    enviar_metrica("scraper.throughput", metricas.throughput)
    enviar_metrica("scraper.cache_hit_rate", metricas.hit_rate)
    enviar_metrica("scraper.error_rate", metricas.error_rate)

    # Alertas
    if metricas.error_rate > 5.0:
        enviar_alerta("⚠️ Error rate alto en scraper")
```

---

## 🚨 Errores Comunes y Cómo Evitarlos

### Error 1: "Async sin Rate Limiting = Ban Inmediato"

❌ **Mal:**
```python
# Lanza 1,000 requests en 1 segundo → Ban instantáneo
async def scrapear_todo_rapido(urls):
    async with aiohttp.ClientSession() as session:
        tareas = [session.get(url) for url in urls]  # ¡1,000 requests paralelos!
        return await asyncio.gather(*tareas)
```

✅ **Bien:**
```python
# Limita a 20 requests concurrentes
async def scrapear_responsable(urls):
    semaforo = asyncio.Semaphore(20)  # Máximo 20 a la vez

    async def obtener_limitado(session, url):
        async with semaforo:
            await asyncio.sleep(0.1)  # 100ms de delay
            async with session.get(url) as response:
                return await response.json()

    async with aiohttp.ClientSession() as session:
        tareas = [obtener_limitado(session, url) for url in urls]
        return await asyncio.gather(*tareas)
```

### Error 2: "Cache sin Expiración = Datos Obsoletos"

❌ **Mal:**
```python
cache = {}
# Cache dura para siempre → datos obsoletos después de semanas
```

✅ **Bien:**
```python
# Cache con TTL de 24 horas
cache = {}
def obtener_con_ttl(url, ttl=86400):  # 86400 seg = 24 horas
    if url in cache:
        datos, timestamp = cache[url]
        if time.time() - timestamp < ttl:
            return datos

    datos = requests.get(url).json()
    cache[url] = (datos, time.time())
    return datos
```

### Error 3: "No Medir = No Saber Si Estás Optimizando"

❌ **Mal:**
```python
# No sabes si el código es lento o rápido
scrapear_datos(urls)
```

✅ **Bien:**
```python
inicio = time.time()
resultados = scrapear_datos(urls)
fin = time.time()

print(f"⏱️  Tiempo: {fin-inicio:.1f}s")
print(f"⚡ Throughput: {len(urls)/(fin-inicio):.1f} req/seg")
```

### Error 4: "Rate Limiting Demasiado Agresivo"

❌ **Mal:**
```python
# 10 segundos entre cada request = 10 horas para 3,600 productos
for url in urls:
    hacer_request(url)
    time.sleep(10)  # Demasiado lento
```

✅ **Bien:**
```python
# Usar async + semáforo para ser rápido Y respetuoso
# 20 requests concurrentes + 0.1s delay = rápido pero cortés
```

### Error 5: "Cache en Memoria sin Límite = Memory Leak"

❌ **Mal:**
```python
cache = {}  # Crece infinitamente hasta agotar RAM
for i in range(1000000):
    cache[f"url_{i}"] = "datos..."  # ¡Puede consumir 10+ GB RAM!
```

✅ **Bien:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)  # Máximo 1,000 entradas
def obtener_dato(url):
    return requests.get(url).json()

# O usar cache en disco con shelve/SQLite
```

---

## ✅ Buenas Prácticas

### 1. Principio del "Buen Vecino"

Cuando scrapeas sitios web (no APIs oficiales):
- ✅ Limita a **1-2 requests por segundo** máximo
- ✅ Identifícate con **User-Agent descriptivo**
- ✅ Respeta **robots.txt** siempre
- ✅ Scrape en **horarios de baja carga** (madrugada)
- ✅ Implementa **exponential backoff** ante errores

### 2. Estrategia de Cache Inteligente

```python
# TTL según volatilidad del dato
TTL_CONFIG = {
    "productos": 86400,      # 24 horas
    "precios": 3600,         # 1 hora
    "inventario": 300,       # 5 minutos
    "paises": 2592000,       # 30 días (datos estáticos)
}

def obtener_con_cache_inteligente(endpoint: str, recurso_id: int):
    url = f"https://api.example.com/{endpoint}/{recurso_id}"
    ttl = TTL_CONFIG.get(endpoint, 3600)  # Default 1 hora
    return obtener_con_ttl(url, ttl=ttl)
```

### 3. Logging Completo de Optimizaciones

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def scrapear_con_logs(urls):
    logger.info(f"🚀 Iniciando scraping de {len(urls)} URLs")

    inicio = time.time()
    metricas = Metricas(inicio=inicio)

    for url in urls:
        if url in cache:
            logger.debug(f"✅ Cache HIT: {url}")
            metricas.registrar_cache_hit()
        else:
            logger.debug(f"🌐 Request: {url}")
            metricas.registrar_cache_miss()

    fin = time.time()
    logger.info(f"✅ Completado en {fin-inicio:.1f}s")
    logger.info(metricas.reporte())
```

### 4. Fail-Safe: Degradación Elegante

```python
async def scrapear_con_fallback(urls):
    """Si async falla, fallback a síncrono."""
    try:
        # Intentar async (más rápido)
        return await scrapear_async(urls)
    except Exception as e:
        logger.warning(f"Async falló: {e}. Fallback a síncrono.")
        # Fallback a síncrono (más lento pero funciona)
        return scrapear_sincrono(urls)
```

---

## 📚 Checklist de Aprendizaje

Después de completar este tema, deberías poder:

### Nivel Básico ✅
- [ ] Explicar qué es rate limiting y por qué existe
- [ ] Implementar rate limiting básico con `time.sleep()`
- [ ] Crear un cache en memoria con un `dict`
- [ ] Calcular throughput (requests/segundo)
- [ ] Medir tiempo de ejecución de un scraper

### Nivel Intermedio ✅
- [ ] Implementar token bucket rate limiting
- [ ] Crear cache con TTL (expiración automática)
- [ ] Usar `shelve` para cache persistente
- [ ] Medir cache hit rate
- [ ] Comparar rendimiento síncrono vs asíncrono

### Nivel Avanzado ✅
- [ ] Implementar scraper asíncrono con `aiohttp` y `asyncio`
- [ ] Combinar async + rate limiting + cache
- [ ] Integrar Redis para cache distribuido
- [ ] Crear dashboard de métricas en vivo
- [ ] Optimizar pipeline ETL completo (Extract → Transform → Load)
- [ ] Calcular ROI de optimización (tiempo/costo ahorrado)

---

## 🎯 Conclusión

La optimización de extracción de datos es una **habilidad crítica** en Data Engineering. Con las técnicas de este tema, puedes:

✅ **Acelerar pipelines 10-100x** (de horas a minutos)
✅ **Reducir costos 90%** (menos requests = menos $$$)
✅ **Ser ético y sostenible** (respetar rate limits)
✅ **Escalar a millones de requests** (con async y cache)
✅ **Monitorear y mejorar continuamente** (con métricas)

**Recuerda:**
> "La optimización prematura es la raíz de todo mal" - Donald Knuth

Pero también:
> "La optimización informada con métricas es la raíz de todo bien" - Tú, ahora 😉

**Próximos pasos:**
1. Practica con los **ejemplos** del siguiente archivo
2. Resuelve los **12 ejercicios** progresivos
3. Implementa el **proyecto práctico** (scraper optimizado TDD)

---

**Palabras clave:** Rate limiting, token bucket, fixed window, sliding window, caching, TTL, cache invalidation, async, await, aiohttp, asyncio, concurrencia, throughput, latencia, métricas, optimización, I/O bound

**Última actualización:** 2025-10-24
**Tiempo de lectura:** 25-30 minutos
**Nivel:** Intermedio-Avanzado
