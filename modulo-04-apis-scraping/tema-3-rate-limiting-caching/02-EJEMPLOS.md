# 📝 Ejemplos Trabajados - Tema 3: Rate Limiting y Caching

**Módulo 4:** APIs y Web Scraping
**Duración estimada:** 45-60 minutos
**Prerequisitos:** Haber leído 01-TEORIA.md del Tema 3

---

## 🎯 Introducción

En este archivo encontrarás **4 ejemplos completos y ejecutables** que demuestran cómo optimizar scrapers y clientes de APIs mediante:

1. **Rate limiting básico** (cortesía y evitar bans)
2. **Cache persistente** (ahorrar requests costosos)
3. **Async requests** (velocidad 20x)
4. **Scraper optimizado completo** (combo de todas las técnicas)

Todos los ejemplos son **código real** que puedes copiar, pegar y ejecutar directamente en Python 3.8+.

---

## 📦 Dependencias

Antes de empezar, instala las dependencias necesarias:

```bash
pip install requests aiohttp
```

---

## 📘 Ejemplo 1: Rate Limiting Básico con `time.sleep()`

### 🎯 Objetivo
Aprender a implementar rate limiting simple para evitar sobrecargar servidores y respetar límites de APIs.

### 🏢 Contexto Empresarial
Trabajas en **DataHub Inc.** y necesitas scrapear 100 URLs de un sitio web que no tiene API. Para ser respetuoso con el servidor, decides limitar tus requests a **1 request cada 2 segundos** (máximo 30 requests/minuto).

### 📊 Datos de Ejemplo
```python
# 100 URLs ficticias para scrapear
urls = [f"https://example.com/productos/{i}" for i in range(1, 101)]
```

### 💻 Código Completo

```python
import requests
import time
from typing import List, Dict

def scrapear_con_rate_limiting(
    urls: List[str],
    delay_seconds: float = 2.0
) -> List[Dict]:
    """
    Scrapea múltiples URLs con rate limiting.

    Args:
        urls: Lista de URLs a scrapear
        delay_seconds: Segundos a esperar entre cada request

    Returns:
        Lista de datos scrapeados
    """
    resultados = []
    inicio_total = time.time()

    print(f"🚀 Iniciando scraping de {len(urls)} URLs")
    print(f"⏱️  Rate limit: 1 request cada {delay_seconds}s")
    print(f"⏱️  Tiempo estimado: {len(urls) * delay_seconds / 60:.1f} minutos\n")

    for i, url in enumerate(urls, 1):
        # Medir tiempo del request
        inicio_request = time.time()

        try:
            # Hacer request HTTP
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Simular extracción de datos (en realidad parsearías HTML)
            datos = {
                "url": url,
                "status_code": response.status_code,
                "content_length": len(response.content),
                "timestamp": time.time()
            }

            resultados.append(datos)

            fin_request = time.time()
            tiempo_request = fin_request - inicio_request

            # Log de progreso
            print(f"✅ [{i}/{len(urls)}] {url} - {tiempo_request*1000:.0f}ms")

        except requests.RequestException as e:
            print(f"❌ [{i}/{len(urls)}] {url} - Error: {e}")

        # RATE LIMITING: Esperar antes del siguiente request
        # (excepto en el último)
        if i < len(urls):
            time.sleep(delay_seconds)

    fin_total = time.time()
    tiempo_total = fin_total - inicio_total

    # Resumen
    print(f"\n📊 Resumen:")
    print(f"✅ Completados: {len(resultados)}/{len(urls)}")
    print(f"⏱️  Tiempo total: {tiempo_total:.1f}s ({tiempo_total/60:.1f} min)")
    print(f"⚡ Velocidad: {len(resultados)/tiempo_total:.2f} URLs/seg")

    return resultados


# ===============================
# EJECUCIÓN DEL EJEMPLO
# ===============================

if __name__ == "__main__":
    # URLs de ejemplo (usando JSONPlaceholder, API pública)
    urls_ejemplo = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]

    # Scrapear con rate limiting de 1 segundo
    resultados = scrapear_con_rate_limiting(urls_ejemplo, delay_seconds=1.0)

    # Mostrar muestra de resultados
    print(f"\n📄 Muestra de datos scrapeados:")
    for dato in resultados[:3]:
        print(f"  - {dato['url']}: {dato['content_length']} bytes")
```

### 📤 Output Esperado

```
🚀 Iniciando scraping de 20 URLs
⏱️  Rate limit: 1 request cada 1.0s
⏱️  Tiempo estimado: 0.3 minutos

✅ [1/20] https://jsonplaceholder.typicode.com/posts/1 - 234ms
✅ [2/20] https://jsonplaceholder.typicode.com/posts/2 - 187ms
✅ [3/20] https://jsonplaceholder.typicode.com/posts/3 - 195ms
...
✅ [20/20] https://jsonplaceholder.typicode.com/posts/20 - 203ms

📊 Resumen:
✅ Completados: 20/20
⏱️  Tiempo total: 23.1s (0.4 min)
⚡ Velocidad: 0.87 URLs/seg

📄 Muestra de datos scrapeados:
  - https://jsonplaceholder.typicode.com/posts/1: 292 bytes
  - https://jsonplaceholder.typicode.com/posts/2: 277 bytes
  - https://jsonplaceholder.typicode.com/posts/3: 285 bytes
```

### 🔍 Conceptos Clave

1. **`time.sleep(delay_seconds)`**: Pausa la ejecución durante N segundos
2. **Rate limiting respetuoso**: 1-2 requests/segundo es considerado cortés
3. **Medición de tiempo**: Usar `time.time()` para calcular duraciones
4. **Progreso visual**: Logs que muestran el avance del scraping
5. **Manejo de errores**: Try/except para que un error no detenga todo

### 🎓 Lecciones Aprendidas

- ✅ Rate limiting simple pero efectivo con `time.sleep()`
- ✅ 20 URLs en ~23 segundos (1 req/seg incluyendo tiempo de request)
- ✅ Ético y respetuoso con el servidor
- ❌ **Lento** para grandes volúmenes (100 URLs = 3+ minutos)
- 💡 **Mejora posible:** Usar async para paralelizar (Ejemplo 3)

---

## 📘 Ejemplo 2: Cache Persistente con `shelve`

### 🎯 Objetivo
Implementar un sistema de cache persistente que ahorre requests costosos a APIs de pago.

### 🏢 Contexto Empresarial
Tu empresa paga **$0.01 por cada request** a una API de datos financieros. El pipeline ETL se ejecuta 10 veces al día durante desarrollo. Sin cache, cada ejecución cuesta $10 (1,000 requests × $0.01). Con cache, solo la primera ejecución hace requests reales.

**Ahorro:** $90/día en desarrollo ($27,000/año) 💰

### 📊 Datos de Ejemplo
```python
# Simular API costosa que retorna cotizaciones de acciones
def api_costosa(simbolo: str) -> dict:
    """Simula una API de pago ($0.01 por request)."""
    time.sleep(0.5)  # Simular latencia
    return {
        "simbolo": simbolo,
        "precio": round(random.uniform(10, 500), 2),
        "timestamp": time.time()
    }
```

### 💻 Código Completo

```python
import shelve
import time
import random
from typing import Optional, Dict

class CacheAPI:
    """Cliente de API con cache persistente en disco."""

    def __init__(self, archivo_cache: str = "cache_api.db", ttl: int = 3600):
        """
        Args:
            archivo_cache: Nombre del archivo de cache (shelve)
            ttl: Tiempo de vida del cache en segundos (default: 1 hora)
        """
        self.archivo_cache = archivo_cache
        self.ttl = ttl
        self.hits = 0
        self.misses = 0

    def obtener_dato(self, clave: str, funcion_api) -> dict:
        """
        Obtiene datos de API con cache.

        Args:
            clave: Identificador único del dato (ej: símbolo de acción)
            funcion_api: Función a llamar si no hay cache

        Returns:
            Datos del API (desde cache o request real)
        """
        with shelve.open(self.archivo_cache) as cache:
            # Verificar si existe en cache y no ha expirado
            if clave in cache:
                datos_cache, timestamp = cache[clave]
                edad = time.time() - timestamp

                # Cache válido (no expirado)
                if edad < self.ttl:
                    self.hits += 1
                    print(f"✅ Cache HIT: {clave} (edad: {edad:.0f}s)")
                    return datos_cache
                else:
                    print(f"⏰ Cache EXPIRADO: {clave} (edad: {edad:.0f}s > TTL: {self.ttl}s)")

            # Cache MISS: hacer request real
            self.misses += 1
            print(f"🌐 Cache MISS: {clave} - Haciendo request...")
            datos = funcion_api(clave)

            # Guardar en cache con timestamp
            cache[clave] = (datos, time.time())

            return datos

    def estadisticas(self) -> str:
        """Retorna estadísticas de uso del cache."""
        total = self.hits + self.misses
        hit_rate = self.hits / total * 100 if total > 0 else 0

        return f"""
📊 Estadísticas de Cache:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cache Hits: {self.hits}
🌐 Cache Misses: {self.misses}
📈 Hit Rate: {hit_rate:.1f}%
💰 Requests ahorrados: {self.hits} × $0.01 = ${self.hits * 0.01:.2f}
        """


def obtener_cotizacion_accion(simbolo: str) -> dict:
    """Simula API costosa de cotizaciones ($0.01/request)."""
    print(f"   💸 Cobrando $0.01...")
    time.sleep(0.5)  # Simular latencia de API
    return {
        "simbolo": simbolo,
        "precio": round(random.uniform(10, 500), 2),
        "volumen": random.randint(1000, 100000),
        "timestamp": time.time()
    }


# ===============================
# EJECUCIÓN DEL EJEMPLO
# ===============================

if __name__ == "__main__":
    # Lista de acciones a consultar
    acciones = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

    # Crear cliente con cache (TTL: 30 segundos para demo)
    cliente = CacheAPI(archivo_cache="cache_finanzas.db", ttl=30)

    print("=" * 50)
    print("PRIMERA EJECUCIÓN (Sin cache)")
    print("=" * 50)
    for accion in acciones:
        dato = cliente.obtener_dato(accion, obtener_cotizacion_accion)
        print(f"  → {accion}: ${dato['precio']:.2f}\n")

    print(cliente.estadisticas())

    # Simular segunda ejecución (debería usar cache)
    print("\n" + "=" * 50)
    print("SEGUNDA EJECUCIÓN (Con cache - instantáneo)")
    print("=" * 50)

    # Resetear contadores para segunda ejecución
    cliente_2da = CacheAPI(archivo_cache="cache_finanzas.db", ttl=30)

    for accion in acciones:
        dato = cliente_2da.obtener_dato(accion, obtener_cotizacion_accion)
        print(f"  → {accion}: ${dato['precio']:.2f}\n")

    print(cliente_2da.estadisticas())

    # Simular expiración del cache
    print("\n" + "=" * 50)
    print("TERCERA EJECUCIÓN (Después de 35 segundos)")
    print("=" * 50)
    print("⏳ Esperando 35 segundos para que expire el cache...")
    time.sleep(35)

    cliente_3ra = CacheAPI(archivo_cache="cache_finanzas.db", ttl=30)

    for accion in acciones[:2]:  # Solo 2 para no hacer muy largo el ejemplo
        dato = cliente_3ra.obtener_dato(accion, obtener_cotizacion_accion)
        print(f"  → {accion}: ${dato['precio']:.2f}\n")

    print(cliente_3ra.estadisticas())
```

### 📤 Output Esperado

```
==================================================
PRIMERA EJECUCIÓN (Sin cache)
==================================================
🌐 Cache MISS: AAPL - Haciendo request...
   💸 Cobrando $0.01...
  → AAPL: $145.23

🌐 Cache MISS: GOOGL - Haciendo request...
   💸 Cobrando $0.01...
  → GOOGL: $102.45

... (3 más)

📊 Estadísticas de Cache:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cache Hits: 0
🌐 Cache Misses: 5
📈 Hit Rate: 0.0%
💰 Requests ahorrados: 0 × $0.01 = $0.00

==================================================
SEGUNDA EJECUCIÓN (Con cache - instantáneo)
==================================================
✅ Cache HIT: AAPL (edad: 3s)
  → AAPL: $145.23

✅ Cache HIT: GOOGL (edad: 3s)
  → GOOGL: $102.45

... (3 más)

📊 Estadísticas de Cache:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cache Hits: 5
🌐 Cache Misses: 0
📈 Hit Rate: 100.0%
💰 Requests ahorrados: 5 × $0.01 = $0.05

==================================================
TERCERA EJECUCIÓN (Después de 35 segundos)
==================================================
⏳ Esperando 35 segundos para que expire el cache...
⏰ Cache EXPIRADO: AAPL (edad: 38s > TTL: 30s)
🌐 Cache MISS: AAPL - Haciendo request...
   💸 Cobrando $0.01...
  → AAPL: $147.89
```

### 🔍 Conceptos Clave

1. **`shelve`**: Base de datos simple tipo diccionario persistente
2. **TTL (Time To Live)**: Cache expira automáticamente después de N segundos
3. **Cache Hit Rate**: Métrica clave (100% = todos los requests desde cache)
4. **Persistencia**: El cache sobrevive entre ejecuciones del programa
5. **ROI**: Calcular ahorro monetario del cache ($0.05 en este ejemplo)

### 🎓 Lecciones Aprendidas

- ✅ Cache reduce costos de APIs de pago dramáticamente
- ✅ `shelve` es perfecto para cache simple persistente
- ✅ TTL evita datos obsoletos
- ✅ Segunda ejecución es **instantánea** (sin esperar 0.5s por request)
- 💡 **En producción:** Usar Redis para cache distribuido

---

## 📘 Ejemplo 3: Async Requests con `aiohttp` (20x Más Rápido)

### 🎯 Objetivo
Demostrar el poder de la programación asíncrona para hacer múltiples requests HTTP en paralelo.

### 🏢 Contexto Empresarial
Necesitas actualizar el catálogo completo de **1,000 productos** consultando una API. Cada request tarda ~0.5 segundos.

- **Síncrono:** 1,000 × 0.5s = 500s = **8.3 minutos** ⏰
- **Async (20 concurrentes):** 1,000 ÷ 20 × 0.5s = 25s = **25 segundos** ⚡ (20x más rápido)

### 💻 Código Completo

```python
import aiohttp
import asyncio
import time
from typing import List, Dict

# =========================================
# VERSIÓN SÍNCRONA (Para comparación)
# =========================================

import requests

def scrapear_sincrono(urls: List[str]) -> List[Dict]:
    """Versión síncrona: hace requests UNO POR UNO."""
    print(f"🐢 SÍNCRONO: Scrapeando {len(urls)} URLs...")
    inicio = time.time()

    resultados = []
    for i, url in enumerate(urls, 1):
        response = requests.get(url)
        datos = response.json()
        resultados.append(datos)

        if i % 10 == 0:
            print(f"   Progreso: {i}/{len(urls)}")

    fin = time.time()
    print(f"✅ Completado en {fin-inicio:.1f}s\n")

    return resultados


# =========================================
# VERSIÓN ASÍNCRONA (Rápida)
# =========================================

async def obtener_url_async(session: aiohttp.ClientSession, url: str, semaforo: asyncio.Semaphore) -> dict:
    """
    Hace un request asíncrono con rate limiting.

    Args:
        session: Sesión HTTP reutilizable
        url: URL a consultar
        semaforo: Limita requests concurrentes
    """
    async with semaforo:  # Limita a N requests concurrentes
        async with session.get(url) as response:
            return await response.json()


async def scrapear_async(urls: List[str], max_concurrente: int = 20) -> List[Dict]:
    """
    Versión asíncrona: hace MÚLTIPLES requests EN PARALELO.

    Args:
        urls: Lista de URLs
        max_concurrente: Máximo número de requests simultáneos
    """
    print(f"⚡ ASYNC: Scrapeando {len(urls)} URLs ({max_concurrente} concurrentes)...")
    inicio = time.time()

    # Semáforo para limitar concurrencia
    semaforo = asyncio.Semaphore(max_concurrente)

    # Crear sesión HTTP reutilizable
    async with aiohttp.ClientSession() as session:
        # Lanzar todos los requests EN PARALELO
        tareas = [obtener_url_async(session, url, semaforo) for url in urls]
        resultados = await asyncio.gather(*tareas)

    fin = time.time()
    print(f"✅ Completado en {fin-inicio:.1f}s\n")

    return resultados


# ===============================
# COMPARACIÓN LADO A LADO
# ===============================

def comparar_sincrono_vs_async(n_urls: int = 50):
    """Compara rendimiento síncrono vs asíncrono."""
    # URLs de ejemplo (API pública)
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, n_urls + 1)]

    print("=" * 60)
    print(f"COMPARACIÓN: Scraping de {n_urls} URLs")
    print("=" * 60)
    print()

    # 1. Versión síncrona
    inicio_sinc = time.time()
    resultados_sinc = scrapear_sincrono(urls)
    tiempo_sinc = time.time() - inicio_sinc

    # 2. Versión asíncrona
    inicio_async = time.time()
    resultados_async = asyncio.run(scrapear_async(urls, max_concurrente=20))
    tiempo_async = time.time() - inicio_async

    # 3. Comparación
    mejora = tiempo_sinc / tiempo_async

    print("=" * 60)
    print("📊 RESULTADOS:")
    print("=" * 60)
    print(f"🐢 Síncrono:  {tiempo_sinc:.1f}s")
    print(f"⚡ Async:     {tiempo_async:.1f}s")
    print(f"🚀 Mejora:    {mejora:.1f}x más rápido")
    print(f"⏱️  Ahorro:    {tiempo_sinc - tiempo_async:.1f}s ({(1 - tiempo_async/tiempo_sinc)*100:.0f}% menos tiempo)")
    print("=" * 60)


# ===============================
# EJECUCIÓN DEL EJEMPLO
# ===============================

if __name__ == "__main__":
    # Comparar con 50 URLs (ajusta según tu conexión)
    comparar_sincrono_vs_async(n_urls=50)

    # Extra: Demostrar escalabilidad
    print("\n\n" + "=" * 60)
    print("🔬 EXPERIMENTO: ¿Cuánto mejora con más URLs?")
    print("=" * 60)
    print()

    for n in [10, 25, 50, 100]:
        urls = [f"https://jsonplaceholder.typicode.com/posts/{i % 100 + 1}" for i in range(n)]

        # Síncrono
        inicio = time.time()
        _ = scrapear_sincrono(urls)
        tiempo_sinc = time.time() - inicio

        # Async
        inicio = time.time()
        _ = asyncio.run(scrapear_async(urls, max_concurrente=20))
        tiempo_async = time.time() - inicio

        mejora = tiempo_sinc / tiempo_async
        print(f"📊 {n} URLs: Síncrono {tiempo_sinc:.1f}s | Async {tiempo_async:.1f}s | Mejora: {mejora:.1f}x")
```

### 📤 Output Esperado

```
============================================================
COMPARACIÓN: Scraping de 50 URLs
============================================================

🐢 SÍNCRONO: Scrapeando 50 URLs...
   Progreso: 10/50
   Progreso: 20/50
   Progreso: 30/50
   Progreso: 40/50
   Progreso: 50/50
✅ Completado en 27.3s

⚡ ASYNC: Scrapeando 50 URLs (20 concurrentes)...
✅ Completado en 1.4s

============================================================
📊 RESULTADOS:
============================================================
🐢 Síncrono:  27.3s
⚡ Async:     1.4s
🚀 Mejora:    19.5x más rápido
⏱️  Ahorro:    25.9s (95% menos tiempo)
============================================================


============================================================
🔬 EXPERIMENTO: ¿Cuánto mejora con más URLs?
============================================================

📊 10 URLs: Síncrono 5.1s | Async 0.6s | Mejora: 8.5x
📊 25 URLs: Síncrono 13.2s | Async 1.0s | Mejora: 13.2x
📊 50 URLs: Síncrono 27.8s | Async 1.5s | Mejora: 18.5x
📊 100 URLs: Síncrono 54.3s | Async 2.9s | Mejora: 18.7x
```

### 🔍 Conceptos Clave

1. **`async`/`await`**: Palabras clave para funciones asíncronas
2. **`aiohttp`**: Librería HTTP asíncrona (alternativa async a `requests`)
3. **`asyncio.Semaphore`**: Limita cuántas tareas corren simultáneamente
4. **`asyncio.gather()`**: Ejecuta múltiples coroutines en paralelo
5. **Concurrencia vs Paralelismo**: Async = concurrencia (1 thread, muchas tareas esperando I/O)

### 🎓 Lecciones Aprendidas

- ✅ Async puede ser **10-20x más rápido** para I/O-bound (requests HTTP)
- ✅ Crucial usar `Semaphore` para limitar concurrencia (evitar sobrecarga)
- ✅ Más URLs = mayor mejora relativa (asymptotically mejor)
- ❌ **Cuidado:** Async sin rate limiting = posible ban
- 💡 **Mejor práctica:** Combinar async + semáforo + delay mínimo

---

## 📘 Ejemplo 4: Scraper Optimizado Completo (Async + Cache + Rate Limiting + Métricas)

### 🎯 Objetivo
Integrar **todas** las técnicas de optimización en un scraper de producción completo.

### 🏢 Contexto Empresarial
Necesitas scrapear 500 productos de una API para un dashboard que se actualiza cada hora. Cada request cuesta $0.01.

**Requisitos:**
- ✅ Máximo 50 requests/minuto (cortesía)
- ✅ Cachear datos por 1 hora (evitar requests innecesarios)
- ✅ Máxima velocidad posible (dentro de límites)
- ✅ Métricas detalladas (throughput, cache hit rate, costos)

### 💻 Código Completo

```python
import aiohttp
import asyncio
import time
import shelve
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Metricas:
    """Contenedor de métricas del scraper."""
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    errores: int = 0
    inicio: float = field(default_factory=time.time)

    @property
    def tiempo_transcurrido(self) -> float:
        return time.time() - self.inicio

    @property
    def throughput(self) -> float:
        """Requests por segundo."""
        return self.total_requests / self.tiempo_transcurrido if self.tiempo_transcurrido > 0 else 0

    @property
    def cache_hit_rate(self) -> float:
        """Porcentaje de hits en cache."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total * 100 if total > 0 else 0

    @property
    def error_rate(self) -> float:
        """Porcentaje de errores."""
        return self.errores / self.total_requests * 100 if self.total_requests > 0 else 0

    @property
    def costo_estimado(self) -> float:
        """Costo en $ (asumiendo $0.01 por request real)."""
        return self.cache_misses * 0.01

    @property
    def ahorro_estimado(self) -> float:
        """Ahorro en $ gracias al cache."""
        return self.cache_hits * 0.01

    def reporte(self) -> str:
        """Genera reporte detallado."""
        return f"""
╔══════════════════════════════════════════════════════════╗
║          📊 MÉTRICAS DEL SCRAPER OPTIMIZADO              ║
╠══════════════════════════════════════════════════════════╣
║ ⏱️  Tiempo total:        {self.tiempo_transcurrido:>6.1f}s                      ║
║ 📝 Total requests:       {self.total_requests:>6}                          ║
║ ⚡ Throughput:           {self.throughput:>6.1f} req/seg                  ║
╠══════════════════════════════════════════════════════════╣
║ ✅ Cache HITS:           {self.cache_hits:>6} ({self.cache_hit_rate:>5.1f}%)                ║
║ 🌐 Cache MISSES:         {self.cache_misses:>6}                          ║
║ ❌ Errores:              {self.errores:>6} ({self.error_rate:>5.2f}%)                 ║
╠══════════════════════════════════════════════════════════╣
║ 💰 Costo (requests):     ${self.costo_estimado:>6.2f}                        ║
║ 💵 Ahorro (cache):       ${self.ahorro_estimado:>6.2f}                        ║
║ 📊 ROI del cache:        {self.ahorro_estimado/(self.ahorro_estimado+self.costo_estimado)*100 if (self.ahorro_estimado+self.costo_estimado) > 0 else 0:>5.1f}%                         ║
╚══════════════════════════════════════════════════════════╝
        """


class ScraperOptimizado:
    """Scraper de producción con async, cache, rate limiting y métricas."""

    def __init__(
        self,
        archivo_cache: str = "cache_scraper.db",
        ttl: int = 3600,
        max_concurrente: int = 20,
        delay_minimo: float = 0.1
    ):
        """
        Args:
            archivo_cache: Archivo del cache persistente
            ttl: Tiempo de vida del cache (segundos)
            max_concurrente: Máximo requests simultáneos
            delay_minimo: Delay mínimo entre requests (segundos)
        """
        self.archivo_cache = archivo_cache
        self.ttl = ttl
        self.max_concurrente = max_concurrente
        self.delay_minimo = delay_minimo
        self.metricas = Metricas()

    def _verificar_cache(self, clave: str) -> Optional[dict]:
        """Verifica si existe en cache y es válido."""
        with shelve.open(self.archivo_cache) as cache:
            if clave in cache:
                datos, timestamp = cache[clave]
                edad = time.time() - timestamp

                if edad < self.ttl:
                    self.metricas.total_requests += 1
                    self.metricas.cache_hits += 1
                    return datos

        return None

    def _guardar_en_cache(self, clave: str, datos: dict):
        """Guarda datos en cache."""
        with shelve.open(self.archivo_cache) as cache:
            cache[clave] = (datos, time.time())

    async def _obtener_con_cache(
        self,
        session: aiohttp.ClientSession,
        url: str,
        semaforo: asyncio.Semaphore
    ) -> dict:
        """Obtiene datos con cache, async y rate limiting."""
        # 1. Verificar cache
        datos_cache = self._verificar_cache(url)
        if datos_cache is not None:
            return datos_cache

        # 2. Request real con rate limiting
        async with semaforo:
            try:
                # Delay mínimo (cortesía)
                await asyncio.sleep(self.delay_minimo)

                # Request HTTP
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    datos = await response.json()

                    # Guardar en cache
                    self._guardar_en_cache(url, datos)

                    # Actualizar métricas
                    self.metricas.total_requests += 1
                    self.metricas.cache_misses += 1

                    return datos

            except Exception as e:
                self.metricas.errores += 1
                print(f"❌ Error en {url}: {e}")
                return {"error": str(e), "url": url}

    async def scrapear(self, urls: List[str]) -> List[dict]:
        """
        Scrape masivo optimizado.

        Args:
            urls: Lista de URLs a scrapear

        Returns:
            Lista de datos scrapeados
        """
        print(f"🚀 Iniciando scraper optimizado")
        print(f"📝 URLs: {len(urls)}")
        print(f"⚡ Concurrencia: {self.max_concurrente}")
        print(f"⏱️  Delay mínimo: {self.delay_minimo}s")
        print(f"💾 Cache TTL: {self.ttl}s ({self.ttl/3600:.1f}h)")
        print()

        # Semáforo para limitar concurrencia
        semaforo = asyncio.Semaphore(self.max_concurrente)

        # Sesión HTTP reutilizable
        async with aiohttp.ClientSession() as session:
            tareas = [
                self._obtener_con_cache(session, url, semaforo)
                for url in urls
            ]
            resultados = await asyncio.gather(*tareas)

        return resultados


# ===============================
# DEMOSTRACIÓN COMPLETA
# ===============================

async def demo_completa():
    """Demuestra el scraper optimizado con múltiples ejecuciones."""
    # URLs de ejemplo (API pública)
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 101)]

    # Crear scraper
    scraper = ScraperOptimizado(
        archivo_cache="demo_cache.db",
        ttl=60,  # Cache de 1 minuto (para demo)
        max_concurrente=20,
        delay_minimo=0.05  # 50ms delay
    )

    print("=" * 70)
    print("PRIMERA EJECUCIÓN (Sin cache - todos los requests son reales)")
    print("=" * 70)
    print()

    resultados_1 = await scraper.scrapear(urls)
    print(scraper.metricas.reporte())

    # Segunda ejecución (debería usar cache al 100%)
    print("\n" + "=" * 70)
    print("SEGUNDA EJECUCIÓN (Con cache - debería ser instantáneo)")
    print("=" * 70)
    print()

    scraper_2 = ScraperOptimizado(
        archivo_cache="demo_cache.db",
        ttl=60,
        max_concurrente=20,
        delay_minimo=0.05
    )

    resultados_2 = await scraper_2.scrapear(urls)
    print(scraper_2.metricas.reporte())

    # Comparación
    mejora = scraper.metricas.tiempo_transcurrido / scraper_2.metricas.tiempo_transcurrido

    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN:")
    print("=" * 70)
    print(f"1ra ejecución: {scraper.metricas.tiempo_transcurrido:.1f}s (sin cache)")
    print(f"2da ejecución: {scraper_2.metricas.tiempo_transcurrido:.1f}s (100% cache)")
    print(f"Mejora: {mejora:.0f}x más rápido")
    print(f"Ahorro acumulado: ${scraper_2.metricas.ahorro_estimado:.2f}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_completa())
```

### 📤 Output Esperado

```
======================================================================
PRIMERA EJECUCIÓN (Sin cache - todos los requests son reales)
======================================================================

🚀 Iniciando scraper optimizado
📝 URLs: 100
⚡ Concurrencia: 20
⏱️  Delay mínimo: 0.05s
💾 Cache TTL: 60s (0.0h)

╔══════════════════════════════════════════════════════════╗
║          📊 MÉTRICAS DEL SCRAPER OPTIMIZADO              ║
╠══════════════════════════════════════════════════════════╣
║ ⏱️  Tiempo total:           8.3s                         ║
║ 📝 Total requests:          100                          ║
║ ⚡ Throughput:             12.0 req/seg                   ║
╠══════════════════════════════════════════════════════════╣
║ ✅ Cache HITS:                0 (  0.0%)                  ║
║ 🌐 Cache MISSES:            100                          ║
║ ❌ Errores:                   0 ( 0.00%)                  ║
╠══════════════════════════════════════════════════════════╣
║ 💰 Costo (requests):      $ 1.00                         ║
║ 💵 Ahorro (cache):        $ 0.00                         ║
║ 📊 ROI del cache:          0.0%                          ║
╚══════════════════════════════════════════════════════════╝

======================================================================
SEGUNDA EJECUCIÓN (Con cache - debería ser instantáneo)
======================================================================

🚀 Iniciando scraper optimizado
📝 URLs: 100
⚡ Concurrencia: 20
⏱️  Delay mínimo: 0.05s
💾 Cache TTL: 60s (0.0h)

╔══════════════════════════════════════════════════════════╗
║          📊 MÉTRICAS DEL SCRAPER OPTIMIZADO              ║
╠══════════════════════════════════════════════════════════╣
║ ⏱️  Tiempo total:           0.2s                         ║
║ 📝 Total requests:          100                          ║
║ ⚡ Throughput:           500.0 req/seg                    ║
╠══════════════════════════════════════════════════════════╣
║ ✅ Cache HITS:              100 (100.0%)                  ║
║ 🌐 Cache MISSES:              0                          ║
║ ❌ Errores:                   0 ( 0.00%)                  ║
╠══════════════════════════════════════════════════════════╣
║ 💰 Costo (requests):      $ 0.00                         ║
║ 💵 Ahorro (cache):        $ 1.00                         ║
║ 📊 ROI del cache:        100.0%                          ║
╚══════════════════════════════════════════════════════════╝

======================================================================
📊 COMPARACIÓN:
======================================================================
1ra ejecución: 8.3s (sin cache)
2da ejecución: 0.2s (100% cache)
Mejora: 42x más rápido
Ahorro acumulado: $1.00
======================================================================
```

### 🔍 Conceptos Clave Integrados

1. **Async + Semaphore**: Máxima velocidad con control de concurrencia
2. **Cache persistente**: Ahorra requests entre ejecuciones
3. **TTL**: Datos siempre frescos (expiración automática)
4. **Métricas completas**: Throughput, hit rate, costos, ROI
5. **Manejo de errores**: No detiene el scraping completo si falla 1 URL

### 🎓 Lecciones Aprendidas

- ✅ **Primera ejecución:** 8.3s, $1.00 de costo
- ✅ **Segunda ejecución:** 0.2s, $0 de costo (100% cache)
- ✅ **Mejora:** 42x más rápido en segunda ejecución
- ✅ **ROI del cache:** 100% (todo el costo evitado)
- ✅ **Throughput:** De 12 req/seg (sin cache) a 500 req/seg (con cache)
- 💡 **Producción:** Este patrón es ideal para pipelines ETL que corren cada hora

---

## 🎯 Resumen y Próximos Pasos

### Lo que aprendiste:

| Ejemplo | Técnica              | Mejora             | Caso de Uso     |
| ------- | -------------------- | ------------------ | --------------- |
| **1**   | Rate limiting básico | Ético ✅            | Scraping cortés |
| **2**   | Cache persistente    | 90% menos requests | APIs de pago    |
| **3**   | Async requests       | 20x más rápido     | Volumen masivo  |
| **4**   | Combo completo       | 42x + 100% ROI     | Producción      |

### Próximos pasos:

1. ✅ **Ejercicios:** Resuelve los 12 ejercicios del archivo `03-EJERCICIOS.md`
2. ✅ **Proyecto práctico:** Implementa un scraper optimizado completo con TDD
3. ✅ **Experimenta:** Prueba diferentes configuraciones (TTL, concurrencia, delay)
4. ✅ **Mide:** Siempre mide throughput, cache hit rate y costos

---

**Última actualización:** 2025-10-24
**Tiempo total:** 45-60 minutos de lectura/práctica
**Nivel:** Intermedio-Avanzado
