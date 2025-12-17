# 🚀 Proyecto Práctico: Scraper Masivo Optimizado

**Módulo 4 - Tema 3:** Rate Limiting y Caching
**Enfoque:** Test-Driven Development (TDD)
**Cobertura objetivo:** >80%

---

## 🎯 Objetivo del Proyecto

Implementar un **scraper masivo optimizado** capaz de descargar 500 URLs en menos de 30 segundos, integrando:

- ⚡ **Async requests** con `aiohttp` (concurrencia)
- 💾 **Cache inteligente** (memoria y disco con `shelve`)
- 🚦 **Rate limiting** (Token Bucket y Fixed Window)
- 📊 **Métricas en tiempo real** (throughput, latencia, cache hit rate)
- 🔒 **Seguridad** (validaciones, timeouts, error handling)

---

## 🏢 Contexto Empresarial

**DataHub Inc.** necesita actualizar su catálogo de 500 productos cada hora consultando una API externa. El scraper actual tarda **8+ minutos** y hace requests redundantes.

**Requisitos del negocio:**
- ✅ Reducir tiempo de ejecución a **<30 segundos**
- ✅ Cachear respuestas para evitar requests duplicados
- ✅ Respetar rate limit de la API (50 requests/segundo máximo)
- ✅ Monitorear métricas para optimización continua
- ✅ Manejo robusto de errores (timeouts, 5xx, etc.)

**ROI esperado:**
- ⏱️ Tiempo: 8 min → 25 seg (**19x más rápido**)
- 💰 Costo: $5/ejecución → $0.50/ejecución (**90% de ahorro**)
- 📈 Throughput: 1 req/seg → 20 req/seg (**20x mejora**)

---

## 📁 Arquitectura del Proyecto

### Estructura de Archivos

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── rate_limiter.py          # Rate limiting (Token Bucket, Fixed Window)
│   ├── cache_manager.py         # Cache (memoria, disco, TTL)
│   ├── async_client.py          # Cliente HTTP asíncrono
│   └── metricas.py              # Monitoreo (throughput, latencia, hit rate)
│
├── tests/
│   ├── __init__.py
│   ├── test_rate_limiter.py     # 15 tests
│   ├── test_cache_manager.py    # 18 tests
│   ├── test_async_client.py     # 12 tests
│   └── test_metricas.py         # 10 tests
│
├── ejemplos/
│   ├── 01_rate_limiting_basico.py
│   ├── 02_cache_con_ttl.py
│   ├── 03_async_requests.py
│   └── 04_scraper_optimizado_completo.py
│
├── datos/                       # Cache persistente (*.db)
├── logs/                        # Archivos de log
├── README.md                    # Este archivo
├── requirements.txt
└── pytest.ini
```

---

## 🧩 Módulos a Implementar (TDD)

### 1. `rate_limiter.py` - Rate Limiting

**Funciones (4):**

```python
def crear_rate_limiter_fixed_window(max_requests: int, window_seconds: int) -> dict
def crear_rate_limiter_token_bucket(capacidad: int, tasa_reposicion: float) -> dict
def puede_hacer_request(rate_limiter: dict) -> bool
def esperar_disponibilidad(rate_limiter: dict) -> float
```

**Conceptos:**
- **Fixed Window:** Límite fijo de requests por ventana de tiempo
- **Token Bucket:** Permite bursts controlados, reposición gradual
- **Cortesía:** No sobrecargar APIs de terceros

**Tests (15):**
- ✅ Crear rate limiter Fixed Window con parámetros válidos
- ✅ Validar límite máximo de requests por ventana
- ✅ Reseteo automático al cambiar de ventana
- ✅ Crear Token Bucket con capacidad y tasa
- ✅ Consumir tokens gradualmente
- ✅ Reposición automática de tokens
- ✅ Permitir burst inicial (consumir todos los tokens)
- ✅ Bloqueo cuando no hay tokens disponibles
- ✅ Esperar hasta que haya tokens disponibles
- ✅ Calcular tiempo de espera correctamente
- ✅ Parámetros inválidos lanzan ValueError
- ✅ Rate limiter persiste estado entre calls
- ✅ Múltiples rate limiters independientes
- ✅ Manejo de clock drift (cambios de hora)
- ✅ Performance con alta concurrencia

---

### 2. `cache_manager.py` - Gestión de Cache

**Funciones (5):**

```python
def crear_cache_memoria(max_size: int = 1000) -> dict
def crear_cache_disco(archivo: str, ttl: int = 3600) -> dict
def obtener_de_cache(cache: dict, clave: str) -> Optional[Any]
def guardar_en_cache(cache: dict, clave: str, valor: Any) -> None
def limpiar_cache_expirado(cache: dict) -> int
```

**Conceptos:**
- **Cache en memoria:** Ultra rápido pero volátil (dict con LRU)
- **Cache en disco:** Persistente con `shelve`, sobrevive reinic

ios
- **TTL (Time To Live):** Expiración automática de datos obsoletos
- **Cache Hit Rate:** Métrica clave de eficiencia

**Tests (18):**
- ✅ Crear cache en memoria con tamaño máximo
- ✅ Guardar y recuperar valor simple
- ✅ Retornar None si clave no existe
- ✅ Sobrescribir valor existente
- ✅ Límite de tamaño (evitar memory leak)
- ✅ Crear cache en disco con archivo válido
- ✅ Cache en disco persiste entre ejecuciones
- ✅ TTL: dato válido retorna valor
- ✅ TTL: dato expirado retorna None
- ✅ Guardar con timestamp para TTL
- ✅ Limpiar cache expirado (retornar cantidad eliminada)
- ✅ Cache vacío no genera errores
- ✅ Valores complejos (dict, list) se almacenan correctamente
- ✅ Caracteres especiales en claves
- ✅ Claves muy largas (>1000 chars)
- ✅ Valores grandes (>1MB)
- ✅ Concurrencia: múltiples escrituras simultáneas
- ✅ Manejo de errores de I/O (disco lleno)

---

### 3. `async_client.py` - Cliente HTTP Asíncrono

**Funciones (4):**

```python
async def crear_sesion_http(headers: Optional[dict] = None) -> aiohttp.ClientSession
async def obtener_url_async(session: aiohttp.ClientSession, url: str, timeout: int = 10) -> dict
async def obtener_urls_batch(urls: List[str], max_concurrente: int = 20, timeout: int = 10) -> List[dict]
async def cerrar_sesion(session: aiohttp.ClientSession) -> None
```

**Conceptos:**
- **Async/Await:** Concurrencia sin multithreading
- **aiohttp:** Librería HTTP asíncrona
- **Semaphore:** Limitar requests concurrentes
- **Context managers:** Gestión automática de recursos

**Tests (12):**
- ✅ Crear sesión HTTP con headers por defecto
- ✅ Crear sesión con headers personalizados
- ✅ GET request async exitoso (200)
- ✅ Retornar JSON parseado automáticamente
- ✅ Timeout si request tarda >N segundos
- ✅ Manejo de error 404
- ✅ Manejo de error 500
- ✅ Obtener batch de URLs en paralelo
- ✅ Limitar concurrencia con semáforo
- ✅ Batch con URLs mixtas (algunas fallan)
- ✅ Cerrar sesión correctamente
- ✅ Performance: 50 URLs en <5 segundos

---

### 4. `metricas.py` - Monitoreo y Métricas

**Funciones (4):**

```python
def crear_monitor_metricas() -> dict
def registrar_request(monitor: dict, fue_cache_hit: bool, tiempo_ms: float) -> None
def obtener_reporte_metricas(monitor: dict) -> str
def exportar_metricas_json(monitor: dict, archivo: str) -> None
```

**Conceptos:**
- **Throughput:** Requests por segundo
- **Latencia:** Tiempo promedio por request
- **Cache Hit Rate:** % de requests servidos desde cache
- **Dashboard:** Visualización de métricas en tiempo real

**Tests (10):**
- ✅ Crear monitor inicializado en cero
- ✅ Registrar cache hit incrementa contador
- ✅ Registrar cache miss incrementa contador
- ✅ Calcular cache hit rate correctamente
- ✅ Calcular throughput (requests/segundo)
- ✅ Calcular latencia promedio
- ✅ Reporte incluye todas las métricas
- ✅ Reporte formateado legible (ASCII art)
- ✅ Exportar métricas a JSON válido
- ✅ Métricas con alta carga (1000+ requests)

---

## 📊 Resumen de Tests

| Módulo             | Funciones | Tests  | Objetivo Cobertura |
| ------------------ | --------- | ------ | ------------------ |
| `rate_limiter.py`  | 4         | 15     | >85%               |
| `cache_manager.py` | 5         | 18     | >90%               |
| `async_client.py`  | 4         | 12     | >80%               |
| `metricas.py`      | 4         | 10     | >85%               |
| **TOTAL**          | **17**    | **55** | **>85%**           |

---

## 🛠️ Instalación y Configuración

### Requisitos

- Python 3.8+
- pip

### Instalar Dependencias

```bash
cd modulo-04-apis-scraping/tema-3-rate-limiting-caching/04-proyecto-practico
pip install -r requirements.txt
```

### Dependencias Principales

```
aiohttp==3.9.1        # Cliente HTTP asíncrono
pytest==7.4.3         # Testing framework
pytest-cov==4.1.0     # Cobertura de tests
pytest-asyncio==0.21.1 # Tests asíncronos
```

---

## ✅ Ejecutar Tests (TDD)

### Todos los Tests

```bash
pytest tests/ -v
```

### Con Cobertura

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
```

### Output Esperado

```
tests/test_rate_limiter.py::test_crear_fixed_window ✓
tests/test_rate_limiter.py::test_token_bucket_burst ✓
...
tests/test_metricas.py::test_exportar_json ✓

======================== 55 passed in 3.2s ========================

---------- coverage: platform win32, python 3.11.5 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/rate_limiter.py        45      2    96%   78-79
src/cache_manager.py       58      3    95%   102, 156
src/async_client.py        38      4    89%   67-70
src/metricas.py            32      1    97%   89
-----------------------------------------------------
TOTAL                     173      10    94%
```

---

## 🚀 Uso del Proyecto

### Ejemplo Básico: Rate Limiting

```python
from src.rate_limiter import crear_rate_limiter_token_bucket, puede_hacer_request, esperar_disponibilidad

# Crear rate limiter: 20 requests/segundo
limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=20)

for i in range(100):
    if puede_hacer_request(limiter):
        print(f"Request {i+1} OK")
        # hacer_request_http()
    else:
        tiempo_espera = esperar_disponibilidad(limiter)
        print(f"Esperando {tiempo_espera:.2f}s...")
```

### Ejemplo Intermedio: Cache con TTL

```python
from src.cache_manager import crear_cache_disco, obtener_de_cache, guardar_en_cache

# Cache persistente con TTL de 1 hora
cache = crear_cache_disco(archivo="datos/cache_productos.db", ttl=3600)

# Intentar obtener de cache
url = "https://api.example.com/productos/123"
datos = obtener_de_cache(cache, url)

if datos is None:
    # Cache MISS: hacer request real
    datos = requests.get(url).json()
    guardar_en_cache(cache, url, datos)
    print("🌐 Request real")
else:
    print("✅ Cache HIT")
```

### Ejemplo Avanzado: Scraper Optimizado Completo

```python
import asyncio
from src.async_client import obtener_urls_batch
from src.cache_manager import crear_cache_disco, obtener_de_cache, guardar_en_cache
from src.rate_limiter import crear_rate_limiter_token_bucket
from src.metricas import crear_monitor_metricas, registrar_request, obtener_reporte_metricas

async def scraper_optimizado(urls: List[str]):
    # Configuración
    cache = crear_cache_disco("datos/cache.db", ttl=3600)
    limiter = crear_rate_limiter_token_bucket(capacidad=50, tasa_reposicion=50)
    monitor = crear_monitor_metricas()

    # Separar URLs en cache vs no-cache
    urls_no_cache = []
    for url in urls:
        datos = obtener_de_cache(cache, url)
        if datos is None:
            urls_no_cache.append(url)
        else:
            registrar_request(monitor, fue_cache_hit=True, tiempo_ms=0.1)

    # Async batch para URLs no cacheadas
    if urls_no_cache:
        resultados = await obtener_urls_batch(urls_no_cache, max_concurrente=20)

        for url, datos in zip(urls_no_cache, resultados):
            guardar_en_cache(cache, url, datos)
            registrar_request(monitor, fue_cache_hit=False, tiempo_ms=500)

    # Mostrar métricas
    print(obtener_reporte_metricas(monitor))

# Ejecutar
urls = [f"https://api.example.com/productos/{i}" for i in range(500)]
asyncio.run(scraper_optimizado(urls))
```

**Output esperado:**

```
╔════════════════════════════════════════════════╗
║          📊 MÉTRICAS DEL SCRAPER               ║
╠════════════════════════════════════════════════╣
║ ⏱️  Tiempo total:        24.3s                 ║
║ 📝 Total requests:       500                   ║
║ ⚡ Throughput:           20.6 req/seg          ║
╠════════════════════════════════════════════════╣
║ ✅ Cache HITS:           350 (70.0%)           ║
║ 🌐 Cache MISSES:         150 (30.0%)           ║
║ 💰 Requests ahorrados:   350                   ║
╠════════════════════════════════════════════════╣
║ 📊 Latencia promedio:    48ms                  ║
║ 💵 Costo estimado:       $0.15 (vs $0.50)     ║
║ 💰 Ahorro:               70% (cache)           ║
╚════════════════════════════════════════════════╝
```

---

## 📈 Ejemplos Incluidos

### `ejemplos/01_rate_limiting_basico.py`
Demuestra Fixed Window y Token Bucket con comparación de rendimiento.

### `ejemplos/02_cache_con_ttl.py`
Implementa cache con expiración automática y calcula ROI.

### `ejemplos/03_async_requests.py`
Compara scraping síncrono vs asíncrono (mejora de 20x).

### `ejemplos/04_scraper_optimizado_completo.py`
Integración completa: async + cache + rate limiting + métricas.

---

## 🎓 Conceptos Aprendidos

Al completar este proyecto, habrás dominado:

### Nivel Básico
- ✅ Rate limiting con `time.sleep()`
- ✅ Cache en memoria con `dict`
- ✅ Medir tiempos de ejecución
- ✅ Calcular throughput

### Nivel Intermedio
- ✅ Token Bucket rate limiting
- ✅ Cache persistente con `shelve`
- ✅ TTL (Time To Live) y expiración
- ✅ Async requests con `aiohttp`
- ✅ Semaphore para limitar concurrencia

### Nivel Avanzado
- ✅ Integración completa async + cache + rate limiting
- ✅ Monitoreo de métricas en tiempo real
- ✅ Optimización de pipelines (10x mejora)
- ✅ Dashboard de métricas
- ✅ Cálculo de ROI (Return on Investment)

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'aiohttp'`

```bash
pip install aiohttp
```

### Error: `RuntimeError: Event loop is closed`

Asegúrate de usar `asyncio.run()` para ejecutar funciones async:

```python
# ❌ MAL
loop = asyncio.get_event_loop()
loop.run_until_complete(mi_funcion())

# ✅ BIEN
asyncio.run(mi_funcion())
```

### Tests fallan con `TimeoutError`

Aumenta el timeout en `pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
timeout = 30
```

### Cache crece sin límite (memory leak)

Usa `crear_cache_memoria(max_size=1000)` para limitar tamaño.

---

## 📊 Métricas del Proyecto

| Métrica                    | Valor | Objetivo | Estado |
| -------------------------- | ----- | -------- | ------ |
| **Tests totales**          | 55    | 50-60    | ✅      |
| **Cobertura**              | 94%   | >80%     | ✅      |
| **Funciones**              | 17    | 15-20    | ✅      |
| **Líneas de código**       | ~600  | 500-800  | ✅      |
| **Ejemplos**               | 4     | 3-4      | ✅      |
| **Tiempo ejecución tests** | 3.2s  | <10s     | ✅      |

---

## 🚀 Próximos Pasos

Después de dominar este proyecto:

1. ✅ **Integrar con Tema 2:** Combinar scraping + optimización
2. ✅ **Redis:** Reemplazar `shelve` con Redis para cache distribuido
3. ✅ **Monitoring:** Integrar con Grafana/Prometheus
4. ✅ **Multiprocessing:** Combinar async con procesos paralelos
5. ✅ **Cloud:** Desplegar en AWS Lambda con API Gateway

---

## 📚 Recursos Adicionales

- [aiohttp Documentation](https://docs.aiohttp.org/)
- [asyncio Python Docs](https://docs.python.org/3/library/asyncio.html)
- [Rate Limiting Algorithms](https://en.wikipedia.org/wiki/Rate_limiting)
- [Cache Strategies](https://www.cloudflare.com/learning/cdn/caching-strategies/)
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket)

---

**Última actualización:** 2025-10-24
**Autor:** DataHub Inc. - Equipo de Data Engineering
**Licencia:** MIT
**Nivel:** Intermedio-Avanzado
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Módulo 5: Bases de Datos Avanzadas: PostgreSQL Avanzado](../../../modulo-05-bases-datos-avanzadas/tema-1-postgresql-avanzado/01-TEORIA.md)
