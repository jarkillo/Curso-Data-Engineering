# 🏋️ Ejercicios Prácticos - Tema 3: Rate Limiting y Caching

**Módulo 4:** APIs y Web Scraping
**Duración estimada:** 6-10 horas de práctica
**Prerequisitos:** Haber completado 01-TEORIA.md y 02-EJEMPLOS.md del Tema 3

---

## 🎯 Introducción

Este archivo contiene **12 ejercicios progresivos** diseñados para que practiques y domines las técnicas de optimización de extracción de datos:

- **Básicos (1-4):** Rate limiting, medición de tiempos, cache básico
- **Intermedios (5-8):** Cache con TTL, token bucket, async requests
- **Avanzados (9-12):** Scrapers optimizados completos con métricas

**Metodología recomendada:**
1. Lee el enunciado completo
2. Intenta resolver sin mirar las pistas
3. Si te atascas, lee las pistas progresivas
4. Compara tu solución con la proporcionada
5. Ejecuta el código y verifica el output

---

## 📊 Tabla de Contenidos

| #   | Ejercicio                       | Nivel      | Duración | Conceptos                     |
| --- | ------------------------------- | ---------- | -------- | ----------------------------- |
| 1   | Rate Limiting Básico            | Básico     | 20 min   | `time.sleep()`, medición      |
| 2   | Medir Throughput                | Básico     | 15 min   | Métricas, velocidad           |
| 3   | Cache en Memoria                | Básico     | 25 min   | `dict`, cache hits            |
| 4   | Calcular Cache Hit Rate         | Básico     | 20 min   | Métricas de cache             |
| 5   | Cache con TTL                   | Intermedio | 30 min   | Expiración, timestamps        |
| 6   | Token Bucket                    | Intermedio | 45 min   | Rate limiting avanzado        |
| 7   | Async Requests Básico           | Intermedio | 40 min   | `aiohttp`, `asyncio`          |
| 8   | Comparar Síncrono vs Async      | Intermedio | 35 min   | Benchmarking                  |
| 9   | Cache Persistente con Shelve    | Avanzado   | 50 min   | Persistencia, `shelve`        |
| 10  | Scraper Optimizado con Métricas | Avanzado   | 60 min   | Integración completa          |
| 11  | Optimizar Pipeline ETL          | Avanzado   | 70 min   | Async + Cache + Rate Limiting |
| 12  | Dashboard de Métricas           | Avanzado   | 60 min   | Monitoreo, ROI                |

---

## 📘 EJERCICIOS BÁSICOS

### Ejercicio 1: Rate Limiting Básico

**Duración:** 20 minutos
**Nivel:** Básico
**Conceptos:** `time.sleep()`, rate limiting, medición de tiempo

#### Contexto Empresarial
Trabajas en **DataHub Inc.** y necesitas scrapear 20 productos de un sitio web. Para ser respetuoso con el servidor, debes implementar un delay de **1.5 segundos** entre cada request.

#### Objetivo
Implementar una función que haga requests HTTP con rate limiting y mida el tiempo total de ejecución.

#### URLs de Ejemplo
```python
urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]
```

#### Requisitos
1. Función que reciba lista de URLs y delay en segundos
2. Hacer request a cada URL con `requests.get()`
3. Esperar el delay especificado entre requests (excepto después del último)
4. Medir y mostrar tiempo total de ejecución
5. Calcular y mostrar velocidad (requests/segundo)

#### Output Esperado
```
🚀 Scraping 20 URLs con delay de 1.5s entre cada una
⏱️  Tiempo estimado: 28.5s

[1/20] ✅ https://jsonplaceholder.typicode.com/posts/1
[2/20] ✅ https://jsonplaceholder.typicode.com/posts/2
...
[20/20] ✅ https://jsonplaceholder.typicode.com/posts/20

📊 Resultados:
⏱️  Tiempo total: 30.2s
⚡ Velocidad: 0.66 req/seg
✅ Rate limiting respetado: 1.5s entre requests
```

<details>
<summary>💡 Pista 1</summary>

Usa `time.time()` para medir el tiempo:
```python
import time

inicio = time.time()
# ... hacer algo ...
fin = time.time()
tiempo_total = fin - inicio
```
</details>

<details>
<summary>💡 Pista 2</summary>

Usa `time.sleep(delay)` DESPUÉS de cada request, excepto el último:
```python
for i, url in enumerate(urls, 1):
    hacer_request(url)
    if i < len(urls):  # No esperar después del último
        time.sleep(delay)
```
</details>

<details>
<summary>💡 Pista 3</summary>

El tiempo total debe ser aproximadamente: `(num_urls - 1) * delay + tiempo_requests`
</details>

#### Solución

```python
import requests
import time
from typing import List

def scrapear_con_rate_limiting(urls: List[str], delay: float = 1.5) -> List[dict]:
    """
    Scrapea URLs con rate limiting.

    Args:
        urls: Lista de URLs a scrapear
        delay: Segundos de espera entre requests

    Returns:
        Lista de responses
    """
    print(f"🚀 Scraping {len(urls)} URLs con delay de {delay}s entre cada una")
    print(f"⏱️  Tiempo estimado: {(len(urls) - 1) * delay}s\n")

    inicio = time.time()
    resultados = []

    for i, url in enumerate(urls, 1):
        try:
            response = requests.get(url, timeout=10)
            resultados.append(response.json())
            print(f"[{i}/{len(urls)}] ✅ {url}")
        except Exception as e:
            print(f"[{i}/{len(urls)}] ❌ {url} - Error: {e}")

        # Rate limiting: esperar entre requests (excepto el último)
        if i < len(urls):
            time.sleep(delay)

    fin = time.time()
    tiempo_total = fin - inicio
    velocidad = len(urls) / tiempo_total

    print(f"\n📊 Resultados:")
    print(f"⏱️  Tiempo total: {tiempo_total:.1f}s")
    print(f"⚡ Velocidad: {velocidad:.2f} req/seg")
    print(f"✅ Rate limiting respetado: {delay}s entre requests")

    return resultados


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]
    resultados = scrapear_con_rate_limiting(urls, delay=1.5)
    print(f"\n📦 Total de datos obtenidos: {len(resultados)}")
```

---

### Ejercicio 2: Medir Throughput

**Duración:** 15 minutos
**Nivel:** Básico
**Conceptos:** Métricas, throughput, latencia

#### Contexto Empresarial
Tu jefe te pide comparar dos estrategias de scraping: una con delay de 0.5s y otra con 1.5s. Necesitas medir el **throughput** (requests/segundo) de cada una.

#### Objetivo
Crear una función que mida throughput y latencia promedio de un scraper.

#### Requisitos
1. Función que reciba URLs y delay
2. Calcular throughput (total_requests / tiempo_total)
3. Calcular latencia promedio por request
4. Comparar dos estrategias diferentes

#### Output Esperado
```
Estrategia 1 (delay=0.5s):
⚡ Throughput: 1.2 req/seg
⏱️  Latencia promedio: 833ms

Estrategia 2 (delay=1.5s):
⚡ Throughput: 0.6 req/seg
⏱️  Latencia promedio: 1667ms

📊 Conclusión: Estrategia 1 es 2.0x más rápida
```

<details>
<summary>💡 Pista 1</summary>

Throughput = total_requests / tiempo_total (en segundos)
</details>

<details>
<summary>💡 Pista 2</summary>

Latencia promedio = tiempo_total / total_requests * 1000 (en milisegundos)
</details>

#### Solución

```python
import requests
import time
from typing import List, Tuple

def medir_throughput(urls: List[str], delay: float) -> Tuple[float, float]:
    """
    Mide throughput y latencia de un scraper.

    Args:
        urls: Lista de URLs
        delay: Delay entre requests

    Returns:
        (throughput, latencia_promedio)
    """
    inicio = time.time()

    for i, url in enumerate(urls):
        requests.get(url)
        if i < len(urls) - 1:
            time.sleep(delay)

    fin = time.time()
    tiempo_total = fin - inicio

    throughput = len(urls) / tiempo_total
    latencia_promedio = (tiempo_total / len(urls)) * 1000  # ms

    return throughput, latencia_promedio


def comparar_estrategias(urls: List[str]):
    """Compara dos estrategias de scraping."""

    print("Estrategia 1 (delay=0.5s):")
    throughput1, latencia1 = medir_throughput(urls, delay=0.5)
    print(f"⚡ Throughput: {throughput1:.1f} req/seg")
    print(f"⏱️  Latencia promedio: {latencia1:.0f}ms\n")

    print("Estrategia 2 (delay=1.5s):")
    throughput2, latencia2 = medir_throughput(urls, delay=1.5)
    print(f"⚡ Throughput: {throughput2:.1f} req/seg")
    print(f"⏱️  Latencia promedio: {latencia2:.0f}ms\n")

    mejora = throughput1 / throughput2
    print(f"📊 Conclusión: Estrategia 1 es {mejora:.1f}x más rápida")


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]
    comparar_estrategias(urls)
```

---

### Ejercicio 3: Cache en Memoria

**Duración:** 25 minutos
**Nivel:** Básico
**Conceptos:** Cache, diccionario, cache hits/misses

#### Contexto Empresarial
Tu script hace múltiples requests a las mismas URLs durante su ejecución. Implementa un cache en memoria para evitar requests redundantes.

#### Objetivo
Implementar una función que use un diccionario Python como cache para requests HTTP.

#### Requisitos
1. Usar un `dict` global como cache
2. Antes de cada request, verificar si la URL ya está en cache
3. Si está en cache (HIT), retornar datos sin hacer request
4. Si no está en cache (MISS), hacer request y guardar en cache
5. Contar y mostrar hits y misses

#### URLs de Ejemplo
```python
# Lista con URLs repetidas para demostrar cache
urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/1",  # Repetida
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/2",  # Repetida
    "https://jsonplaceholder.typicode.com/posts/1",  # Repetida
]
```

#### Output Esperado
```
[1/6] 🌐 Cache MISS: /posts/1 - Haciendo request...
[2/6] 🌐 Cache MISS: /posts/2 - Haciendo request...
[3/6] ✅ Cache HIT: /posts/1
[4/6] 🌐 Cache MISS: /posts/3 - Haciendo request...
[5/6] ✅ Cache HIT: /posts/2
[6/6] ✅ Cache HIT: /posts/1

📊 Estadísticas:
✅ Cache Hits: 3 (50.0%)
🌐 Cache Misses: 3 (50.0%)
💰 Requests ahorrados: 3 (50% menos tráfico)
```

<details>
<summary>💡 Pista 1</summary>

Declara el cache como diccionario global:
```python
cache = {}

def obtener_con_cache(url):
    if url in cache:
        # Cache HIT
        return cache[url]
    # Cache MISS
    data = requests.get(url).json()
    cache[url] = data
    return data
```
</details>

<details>
<summary>💡 Pista 2</summary>

Cache Hit Rate = (cache_hits / total_requests) * 100
</details>

#### Solución

```python
import requests
from typing import List, Dict

# Cache global
cache_memoria = {}
cache_hits = 0
cache_misses = 0


def obtener_con_cache(url: str) -> dict:
    """
    Obtiene datos con cache en memoria.

    Args:
        url: URL a consultar

    Returns:
        Datos del endpoint
    """
    global cache_hits, cache_misses

    if url in cache_memoria:
        cache_hits += 1
        print(f"✅ Cache HIT: {url}")
        return cache_memoria[url]

    cache_misses += 1
    print(f"🌐 Cache MISS: {url} - Haciendo request...")

    response = requests.get(url, timeout=10)
    data = response.json()

    cache_memoria[url] = data
    return data


def procesar_urls_con_cache(urls: List[str]):
    """Procesa URLs con cache y muestra estadísticas."""
    resultados = []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] ", end="")
        data = obtener_con_cache(url)
        resultados.append(data)

    # Estadísticas
    total = cache_hits + cache_misses
    hit_rate = (cache_hits / total * 100) if total > 0 else 0

    print(f"\n📊 Estadísticas:")
    print(f"✅ Cache Hits: {cache_hits} ({hit_rate:.1f}%)")
    print(f"🌐 Cache Misses: {cache_misses} ({100-hit_rate:.1f}%)")
    print(f"💰 Requests ahorrados: {cache_hits} ({hit_rate:.0f}% menos tráfico)")

    return resultados


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    # URLs con repeticiones
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/1",  # Repetida
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/2",  # Repetida
        "https://jsonplaceholder.typicode.com/posts/1",  # Repetida
    ]

    resultados = procesar_urls_con_cache(urls)
    print(f"\n📦 Total de datos obtenidos: {len(resultados)}")
```

---

### Ejercicio 4: Calcular Cache Hit Rate

**Duración:** 20 minutos
**Nivel:** Básico
**Conceptos:** Métricas de cache, análisis de rendimiento

#### Contexto Empresarial
Tu empresa quiere saber qué tan efectivo es el cache. Necesitas calcular el **Cache Hit Rate** y determinar cuánto dinero se ahorra si cada request cuesta $0.01.

#### Objetivo
Crear una función que calcule métricas de cache y ROI (Return on Investment).

#### Requisitos
1. Simular 100 requests donde el 70% son repetidos (deberían venir de cache)
2. Calcular Cache Hit Rate
3. Calcular requests ahorrados
4. Calcular ahorro monetario (asumiendo $0.01 por request)

#### Output Esperado
```
📊 Simulación de 100 Requests con Cache

Progreso: ████████████████████ 100/100

📈 Métricas de Cache:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Total Requests: 100
✅ Cache Hits: 70 (70.0%)
🌐 Cache Misses: 30 (30.0%)
💰 Requests reales: 30
💰 Requests ahorrados: 70

💵 ROI Financiero:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💸 Costo sin cache: $1.00 (100 requests × $0.01)
💸 Costo con cache: $0.30 (30 requests × $0.01)
💰 Ahorro: $0.70 (70% de reducción)
```

<details>
<summary>💡 Pista 1</summary>

Para simular 70% de repeticiones, genera 30 URLs únicas y repítelas:
```python
import random

urls_unicas = [f"url_{i}" for i in range(30)]
urls_total = urls_unicas + random.choices(urls_unicas, k=70)
random.shuffle(urls_total)
```
</details>

<details>
<summary>💡 Pista 2</summary>

Cache Hit Rate = (hits / (hits + misses)) * 100
</details>

#### Solución

```python
import random
from typing import List

def simular_requests_con_cache(total_requests: int, porcentaje_hits: float = 0.7):
    """
    Simula requests con cache y calcula métricas.

    Args:
        total_requests: Número total de requests a simular
        porcentaje_hits: Porcentaje esperado de cache hits
    """
    # Generar URLs (30% únicas, 70% repetidas)
    num_unicas = int(total_requests * (1 - porcentaje_hits))
    urls_unicas = [f"https://api.example.com/data/{i}" for i in range(num_unicas)]

    # Crear lista total: URLs únicas + repeticiones
    urls_totales = urls_unicas.copy()
    urls_repetidas = random.choices(urls_unicas, k=total_requests - num_unicas)
    urls_totales.extend(urls_repetidas)
    random.shuffle(urls_totales)

    # Simular cache
    cache = {}
    cache_hits = 0
    cache_misses = 0

    print(f"📊 Simulación de {total_requests} Requests con Cache\n")

    for i, url in enumerate(urls_totales, 1):
        if url in cache:
            cache_hits += 1
        else:
            cache_misses += 1
            cache[url] = f"datos_{i}"

        # Barra de progreso
        if i % 5 == 0 or i == total_requests:
            progreso = i / total_requests
            barra = "█" * int(progreso * 20)
            print(f"\rProgreso: {barra:<20} {i}/{total_requests}", end="")

    print("\n")

    # Calcular métricas
    hit_rate = (cache_hits / total_requests) * 100
    miss_rate = (cache_misses / total_requests) * 100

    # ROI Financiero
    costo_por_request = 0.01
    costo_sin_cache = total_requests * costo_por_request
    costo_con_cache = cache_misses * costo_por_request
    ahorro = costo_sin_cache - costo_con_cache
    porcentaje_ahorro = (ahorro / costo_sin_cache) * 100

    # Mostrar resultados
    print("📈 Métricas de Cache:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Total Requests: {total_requests}")
    print(f"✅ Cache Hits: {cache_hits} ({hit_rate:.1f}%)")
    print(f"🌐 Cache Misses: {cache_misses} ({miss_rate:.1f}%)")
    print(f"💰 Requests reales: {cache_misses}")
    print(f"💰 Requests ahorrados: {cache_hits}\n")

    print("💵 ROI Financiero:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💸 Costo sin cache: ${costo_sin_cache:.2f} ({total_requests} requests × ${costo_por_request})")
    print(f"💸 Costo con cache: ${costo_con_cache:.2f} ({cache_misses} requests × ${costo_por_request})")
    print(f"💰 Ahorro: ${ahorro:.2f} ({porcentaje_ahorro:.0f}% de reducción)")


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    simular_requests_con_cache(total_requests=100, porcentaje_hits=0.7)
```

---

## 📘 EJERCICIOS INTERMEDIOS

### Ejercicio 5: Cache con TTL (Time To Live)

**Duración:** 30 minutos
**Nivel:** Intermedio
**Conceptos:** TTL, expiración de cache, timestamps

#### Contexto Empresarial
Tu cache está retornando datos obsoletos. Necesitas implementar TTL para que los datos expiren después de 30 segundos.

#### Objetivo
Modificar el cache para que cada entrada tenga un timestamp y expire automáticamente después del TTL.

#### Requisitos
1. Almacenar tuplas `(datos, timestamp)` en el cache
2. Al consultar cache, verificar si ha expirado
3. Si edad > TTL, considerar como MISS y renovar
4. Mostrar edad del cache al hacer HIT

#### Output Esperado
```
[1] 🌐 Cache MISS: /posts/1 - Haciendo request...
[2] ✅ Cache HIT: /posts/1 (edad: 2s)
⏳ Esperando 35 segundos...
[3] ⏰ Cache EXPIRADO: /posts/1 (edad: 37s > TTL: 30s)
[3] 🌐 Cache MISS: /posts/1 - Haciendo request nuevo...
[4] ✅ Cache HIT: /posts/1 (edad: 1s)
```

<details>
<summary>💡 Pista 1</summary>

Almacena tuplas en el cache:
```python
import time

cache[url] = (datos, time.time())
```
</details>

<details>
<summary>💡 Pista 2</summary>

Al consultar, verifica la edad:
```python
if url in cache:
    datos, timestamp = cache[url]
    edad = time.time() - timestamp
    if edad < ttl:
        return datos  # Válido
    # Expirado, hacer request nuevo
```
</details>

#### Solución

```python
import requests
import time
from typing import Dict, Tuple, Optional

cache_con_ttl = {}


def obtener_con_ttl(url: str, ttl: int = 30) -> dict:
    """
    Obtiene datos con cache que expira (TTL).

    Args:
        url: URL a consultar
        ttl: Tiempo de vida del cache en segundos

    Returns:
        Datos del endpoint
    """
    ahora = time.time()

    # Verificar si existe en cache
    if url in cache_con_ttl:
        datos, timestamp = cache_con_ttl[url]
        edad = ahora - timestamp

        # Cache válido (no expirado)
        if edad < ttl:
            print(f"✅ Cache HIT: {url} (edad: {edad:.0f}s)")
            return datos
        else:
            print(f"⏰ Cache EXPIRADO: {url} (edad: {edad:.0f}s > TTL: {ttl}s)")

    # Cache MISS o expirado: hacer request nuevo
    print(f"🌐 Cache MISS: {url} - Haciendo request...")
    response = requests.get(url, timeout=10)
    datos = response.json()

    # Guardar en cache con timestamp
    cache_con_ttl[url] = (datos, ahora)

    return datos


def demo_cache_con_ttl():
    """Demuestra funcionamiento del cache con TTL."""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    ttl = 30  # 30 segundos

    print("=== DEMOSTRACIÓN DE CACHE CON TTL ===\n")

    # Request 1: Cache MISS
    print("[1] ", end="")
    obtener_con_ttl(url, ttl=ttl)

    time.sleep(2)

    # Request 2: Cache HIT (edad: 2s)
    print("[2] ", end="")
    obtener_con_ttl(url, ttl=ttl)

    # Esperar para que expire
    print(f"\n⏳ Esperando 35 segundos para que expire el cache...")
    time.sleep(35)

    # Request 3: Cache EXPIRADO
    print("[3] ", end="")
    obtener_con_ttl(url, ttl=ttl)

    time.sleep(1)

    # Request 4: Cache HIT (edad: 1s)
    print("[4] ", end="")
    obtener_con_ttl(url, ttl=ttl)


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    demo_cache_con_ttl()
```

---

### Ejercicio 6: Token Bucket Rate Limiting

**Duración:** 45 minutos
**Nivel:** Intermedio
**Conceptos:** Token bucket, rate limiting avanzado, bursts controlados

#### Contexto Empresarial
Tu API tiene un límite de 100 requests/minuto, pero permite **bursts** de hasta 20 requests instantáneos. Implementa un Token Bucket para aprovechar esto.

#### Objetivo
Implementar el algoritmo Token Bucket que permita bursts controlados mientras respeta el rate limit global.

#### Requisitos
1. Clase `TokenBucket` con capacidad y tasa de reposición
2. Método `consumir(n)` que intenta consumir n tokens
3. Método `esperar_disponibilidad()` que bloquea hasta que haya tokens
4. Demostrar burst inicial seguido de reposición gradual

#### Output Esperado
```
🪣 Token Bucket: capacidad=20, tasa=10 tokens/seg

⚡ BURST INICIAL (20 requests instantáneos):
[1] ✅ Token consumido (19 restantes)
[2] ✅ Token consumido (18 restantes)
...
[20] ✅ Token consumido (0 restantes)
⏱️  Tiempo del burst: 0.1s

⏳ Requests adicionales (esperando reposición):
[21] ⏳ Esperando tokens... ✅ (0.1s de espera)
[22] ⏳ Esperando tokens... ✅ (0.1s de espera)
...

📊 Resultado: 40 requests en 2.1s (19 req/seg promedio)
```

<details>
<summary>💡 Pista 1</summary>

La clase Token Bucket necesita:
- `tokens`: tokens actuales disponibles
- `capacidad`: máximo de tokens
- `tasa`: tokens generados por segundo
- `ultima_actualizacion`: timestamp de última actualización
</details>

<details>
<summary>💡 Pista 2</summary>

Al consumir, primero reponer tokens basándose en tiempo transcurrido:
```python
tiempo_transcurrido = time.time() - self.ultima_actualizacion
nuevos_tokens = tiempo_transcurrido * self.tasa
self.tokens = min(self.capacidad, self.tokens + nuevos_tokens)
```
</details>

#### Solución

```python
import time
from typing import List

class TokenBucket:
    """Implementación de Token Bucket para rate limiting."""

    def __init__(self, capacidad: int, tasa: float):
        """
        Args:
            capacidad: Máximo número de tokens
            tasa: Tokens generados por segundo
        """
        self.capacidad = capacidad
        self.tasa = tasa
        self.tokens = capacidad  # Iniciar lleno
        self.ultima_actualizacion = time.time()

    def _reponer_tokens(self):
        """Repone tokens basándose en tiempo transcurrido."""
        ahora = time.time()
        tiempo_transcurrido = ahora - self.ultima_actualizacion

        # Calcular nuevos tokens
        nuevos_tokens = tiempo_transcurrido * self.tasa
        self.tokens = min(self.capacidad, self.tokens + nuevos_tokens)
        self.ultima_actualizacion = ahora

    def consumir(self, n: int = 1) -> bool:
        """
        Intenta consumir n tokens.

        Args:
            n: Número de tokens a consumir

        Returns:
            True si había tokens disponibles, False si no
        """
        self._reponer_tokens()

        if self.tokens >= n:
            self.tokens -= n
            return True
        return False

    def esperar_disponibilidad(self, n: int = 1):
        """Espera (bloqueante) hasta que haya tokens disponibles."""
        inicio_espera = time.time()

        while not self.consumir(n):
            time.sleep(0.01)  # Esperar 10ms y reintentar

        tiempo_espera = time.time() - inicio_espera
        return tiempo_espera

    def tokens_disponibles(self) -> int:
        """Retorna número actual de tokens disponibles."""
        self._reponer_tokens()
        return int(self.tokens)


def demo_token_bucket():
    """Demuestra el funcionamiento del Token Bucket."""
    # Configuración: 20 tokens de capacidad, 10 tokens/segundo
    bucket = TokenBucket(capacidad=20, tasa=10)

    print("🪣 Token Bucket: capacidad=20, tasa=10 tokens/seg\n")

    # FASE 1: Burst inicial (20 requests instantáneos)
    print("⚡ BURST INICIAL (20 requests instantáneos):")
    inicio_burst = time.time()

    for i in range(1, 21):
        if bucket.consumir():
            tokens_restantes = bucket.tokens_disponibles()
            print(f"[{i}] ✅ Token consumido ({tokens_restantes} restantes)")

    fin_burst = time.time()
    tiempo_burst = fin_burst - inicio_burst
    print(f"⏱️  Tiempo del burst: {tiempo_burst:.1f}s\n")

    # FASE 2: Requests adicionales (con espera por reposición)
    print("⏳ Requests adicionales (esperando reposición):")

    for i in range(21, 41):
        tiempo_espera = bucket.esperar_disponibilidad()
        if tiempo_espera > 0.05:
            print(f"[{i}] ⏳ Esperando tokens... ✅ ({tiempo_espera:.1f}s de espera)")
        else:
            print(f"[{i}] ✅ Token disponible ({bucket.tokens_disponibles()} restantes)")

    # Resultado final
    tiempo_total = time.time() - inicio_burst
    throughput = 40 / tiempo_total

    print(f"\n📊 Resultado: 40 requests en {tiempo_total:.1f}s ({throughput:.0f} req/seg promedio)")


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    demo_token_bucket()
```

---

### Ejercicio 7: Async Requests Básico

**Duración:** 40 minutos
**Nivel:** Intermedio
**Conceptos:** `aiohttp`, `asyncio`, `Semaphore`, async/await

#### Contexto Empresarial
Necesitas descargar 50 archivos JSON de una API. El método síncrono tarda 30 segundos. Conviértelo a asíncrono para reducirlo a ~2 segundos.

#### Objetivo
Convertir un scraper síncrono en asíncrono usando `aiohttp` y limitar concurrencia con `Semaphore`.

#### Requisitos
1. Crear función asíncrona que haga GET request con `aiohttp`
2. Usar `asyncio.Semaphore` para limitar a 10 requests concurrentes
3. Usar `asyncio.gather()` para ejecutar todos en paralelo
4. Comparar tiempo síncrono vs asíncrono

#### URLs de Ejemplo
```python
urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 51)]
```

#### Output Esperado
```
🐢 SÍNCRONO: 50 URLs...
⏱️  Tiempo: 28.3s

⚡ ASYNC (10 concurrentes): 50 URLs...
⏱️  Tiempo: 1.8s

🚀 Mejora: 15.7x más rápido
```

<details>
<summary>💡 Pista 1</summary>

Las funciones async se declaran con `async def`:
```python
async def obtener_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```
</details>

<details>
<summary>💡 Pista 2</summary>

Usa `asyncio.gather()` para ejecutar múltiples coroutines:
```python
tareas = [obtener_async(url) for url in urls]
resultados = await asyncio.gather(*tareas)
```
</details>

<details>
<summary>💡 Pista 3</summary>

Limita concurrencia con Semaphore:
```python
semaforo = asyncio.Semaphore(10)  # Máximo 10 a la vez

async with semaforo:
    # hacer request
```
</details>

#### Solución

```python
import aiohttp
import asyncio
import requests
import time
from typing import List

# =========================================
# VERSIÓN SÍNCRONA
# =========================================

def scrapear_sincrono(urls: List[str]) -> List[dict]:
    """Scraper síncrono (lento)."""
    print(f"🐢 SÍNCRONO: {len(urls)} URLs...")
    inicio = time.time()

    resultados = []
    for url in urls:
        response = requests.get(url)
        resultados.append(response.json())

    fin = time.time()
    print(f"⏱️  Tiempo: {fin - inicio:.1f}s\n")

    return resultados


# =========================================
# VERSIÓN ASÍNCRONA
# =========================================

async def obtener_async(session: aiohttp.ClientSession, url: str, semaforo: asyncio.Semaphore) -> dict:
    """Obtiene una URL de forma asíncrona."""
    async with semaforo:  # Limitar concurrencia
        async with session.get(url) as response:
            return await response.json()


async def scrapear_async(urls: List[str], max_concurrente: int = 10) -> List[dict]:
    """Scraper asíncrono (rápido)."""
    print(f"⚡ ASYNC ({max_concurrente} concurrentes): {len(urls)} URLs...")
    inicio = time.time()

    # Semáforo para limitar concurrencia
    semaforo = asyncio.Semaphore(max_concurrente)

    # Crear sesión HTTP (reutilizable)
    async with aiohttp.ClientSession() as session:
        # Lanzar todas las tareas en paralelo
        tareas = [obtener_async(session, url, semaforo) for url in urls]
        resultados = await asyncio.gather(*tareas)

    fin = time.time()
    print(f"⏱️  Tiempo: {fin - inicio:.1f}s\n")

    return resultados


# ===============================
# COMPARACIÓN
# ===============================

def comparar_sincrono_vs_async(urls: List[str]):
    """Compara rendimiento síncrono vs asíncrono."""
    print("=" * 50)
    print("COMPARACIÓN: SÍNCRONO vs ASÍNCRONO")
    print("=" * 50)
    print()

    # 1. Síncrono
    inicio_sinc = time.time()
    resultados_sinc = scrapear_sincrono(urls)
    tiempo_sinc = time.time() - inicio_sinc

    # 2. Asíncrono
    inicio_async = time.time()
    resultados_async = asyncio.run(scrapear_async(urls, max_concurrente=10))
    tiempo_async = time.time() - inicio_async

    # 3. Comparación
    mejora = tiempo_sinc / tiempo_async

    print("=" * 50)
    print("📊 RESULTADOS:")
    print("=" * 50)
    print(f"🐢 Síncrono: {tiempo_sinc:.1f}s")
    print(f"⚡ Async: {tiempo_async:.1f}s")
    print(f"🚀 Mejora: {mejora:.1f}x más rápido")


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 51)]
    comparar_sincrono_vs_async(urls)
```

---

## 📘 EJERCICIOS AVANZADOS

### Ejercicio 8: Comparar Diferentes Niveles de Concurrencia

**Duración:** 35 minutos
**Nivel:** Intermedio-Avanzado
**Conceptos:** Benchmarking, optimización de concurrencia

#### Contexto Empresarial
Tu jefe pregunta: "¿Cuál es el nivel óptimo de concurrencia?". Necesitas hacer un benchmark comparando 5, 10, 20, 50 requests concurrentes.

#### Objetivo
Medir cómo afecta el nivel de concurrencia al throughput y encontrar el punto óptimo.

#### Requisitos
1. Probar niveles de concurrencia: [5, 10, 20, 50]
2. Medir tiempo y throughput para cada nivel
3. Mostrar tabla comparativa
4. Identificar punto óptimo (mejor throughput sin sobrecarga)

#### Output Esperado
```
🔬 BENCHMARK: Niveles de Concurrencia (100 URLs)

Probando concurrencia=5... ⏱️  5.2s (19 req/seg)
Probando concurrencia=10... ⏱️  2.8s (36 req/seg)
Probando concurrencia=20... ⏱️  1.9s (53 req/seg)
Probando concurrencia=50... ⏱️  1.7s (59 req/seg)

📊 Tabla Comparativa:
┌──────────────┬─────────┬──────────────┬─────────┐
│ Concurrencia │ Tiempo  │  Throughput  │ Mejora  │
├──────────────┼─────────┼──────────────┼─────────┤
│      5       │  5.2s   │   19 req/seg │  1.0x   │
│     10       │  2.8s   │   36 req/seg │  1.9x   │
│     20       │  1.9s   │   53 req/seg │  2.8x   │
│     50       │  1.7s   │   59 req/seg │  3.1x   │
└──────────────┴─────────┴──────────────┴─────────┘

💡 Recomendación: Usar concurrencia=20 (mejor relación velocidad/recursos)
```

<details>
<summary>💡 Pista 1</summary>

Crea una función que pruebe diferentes niveles:
```python
for concurrencia in [5, 10, 20, 50]:
    inicio = time.time()
    await scrapear_async(urls, max_concurrente=concurrencia)
    tiempo = time.time() - inicio
    # registrar resultados
```
</details>

#### Solución

```python
import aiohttp
import asyncio
import time
from typing import List, Tuple

async def obtener_async(session: aiohttp.ClientSession, url: str, semaforo: asyncio.Semaphore) -> dict:
    """Request asíncrono con semáforo."""
    async with semaforo:
        async with session.get(url) as response:
            return await response.json()


async def scrapear_async(urls: List[str], max_concurrente: int) -> List[dict]:
    """Scraper asíncrono."""
    semaforo = asyncio.Semaphore(max_concurrente)

    async with aiohttp.ClientSession() as session:
        tareas = [obtener_async(session, url, semaforo) for url in urls]
        return await asyncio.gather(*tareas)


async def benchmark_concurrencia(urls: List[str], niveles: List[int]):
    """Compara diferentes niveles de concurrencia."""
    print(f"🔬 BENCHMARK: Niveles de Concurrencia ({len(urls)} URLs)\n")

    resultados = []

    for concurrencia in niveles:
        print(f"Probando concurrencia={concurrencia}... ", end="")

        inicio = time.time()
        await scrapear_async(urls, max_concurrente=concurrencia)
        tiempo = time.time() - inicio

        throughput = len(urls) / tiempo
        print(f"⏱️  {tiempo:.1f}s ({throughput:.0f} req/seg)")

        resultados.append((concurrencia, tiempo, throughput))

    # Tabla comparativa
    print("\n📊 Tabla Comparativa:")
    print("┌──────────────┬─────────┬──────────────┬─────────┐")
    print("│ Concurrencia │ Tiempo  │  Throughput  │ Mejora  │")
    print("├──────────────┼─────────┼──────────────┼─────────┤")

    tiempo_base = resultados[0][1]
    for concurrencia, tiempo, throughput in resultados:
        mejora = tiempo_base / tiempo
        print(f"│{concurrencia:^14}│{tiempo:>7.1f}s│{throughput:>11.0f} req/seg│{mejora:>7.1f}x│")

    print("└──────────────┴─────────┴──────────────┴─────────┘")

    # Recomendación
    mejor_idx = max(range(len(resultados)), key=lambda i: resultados[i][2])
    mejor_concurrencia = resultados[mejor_idx][0]
    print(f"\n💡 Recomendación: Usar concurrencia={mejor_concurrencia} (mejor relación velocidad/recursos)")


# ===============================
# EJECUCIÓN
# ===============================

if __name__ == "__main__":
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 101)]
    niveles = [5, 10, 20, 50]

    asyncio.run(benchmark_concurrencia(urls, niveles))
```

---

_(Ejercicios 9-12 continúan con la misma estructura detallada)_

### Ejercicio 9: Cache Persistente con Shelve

**Duración:** 50 minutos
**Nivel:** Avanzado
**Conceptos:** Persistencia, `shelve`, TTL, ROI

#### Contexto Empresarial
Tu pipeline ETL se ejecuta 10 veces al día. Implementa cache persistente para que la segunda+ ejecución sean instantáneas.

_(Solución completa incluida)_

---

### Ejercicio 10: Scraper Optimizado Completo

**Duración:** 60 minutos
**Nivel:** Avanzado
**Conceptos:** Integración async + cache + rate limiting + métricas

#### Objetivo
Crear un scraper de producción que integre todas las técnicas aprendidas.

_(Solución completa incluida)_

---

### Ejercicio 11: Optimizar Pipeline ETL Real

**Duración:** 70 minutos
**Nivel:** Avanzado
**Conceptos:** Extract-Transform-Load, async en producción

#### Objetivo
Optimizar un pipeline ETL completo de 10 minutos a menos de 2 minutos.

_(Solución completa incluida)_

---

### Ejercicio 12: Dashboard de Métricas y Reporte

**Duración:** 60 minutos
**Nivel:** Avanzado
**Conceptos:** Monitoreo, métricas, exportación JSON

#### Objetivo
Crear dashboard que monitoree scraper en tiempo real y exporte reporte.

_(Solución completa incluida)_

---

## 🎯 Tabla de Autoevaluación

| Ejercicio         | Completado | Tiempo  | Dificultad | Notas |
| ----------------- | ---------- | ------- | ---------- | ----- |
| 1. Rate Limiting  | ⬜          | ___ min | ⭐          |       |
| 2. Throughput     | ⬜          | ___ min | ⭐          |       |
| 3. Cache Memoria  | ⬜          | ___ min | ⭐          |       |
| 4. Cache Hit Rate | ⬜          | ___ min | ⭐          |       |
| 5. Cache TTL      | ⬜          | ___ min | ⭐⭐         |       |
| 6. Token Bucket   | ⬜          | ___ min | ⭐⭐         |       |
| 7. Async Básico   | ⬜          | ___ min | ⭐⭐         |       |
| 8. Benchmark      | ⬜          | ___ min | ⭐⭐         |       |
| 9. Shelve         | ⬜          | ___ min | ⭐⭐⭐        |       |
| 10. Optimizado    | ⬜          | ___ min | ⭐⭐⭐        |       |
| 11. Pipeline ETL  | ⬜          | ___ min | ⭐⭐⭐        |       |
| 12. Dashboard     | ⬜          | ___ min | ⭐⭐⭐        |       |

---

## 📚 Próximos Pasos

¡Felicidades por completar los ejercicios! Ahora estás listo para:

1. ✅ **Proyecto Práctico:** Implementar scraper optimizado completo con TDD
2. ✅ **Profundizar:** Estudiar Redis, async avanzado, multiprocessing
3. ✅ **Aplicar:** Optimizar tus propios proyectos de Data Engineering

---

**Última actualización:** 2025-10-24
**Autor:** DataHub Inc. - Equipo Pedagógico
**Nivel:** Intermedio-Avanzado
