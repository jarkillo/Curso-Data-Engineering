# 🚀 Tema 3: Rate Limiting y Caching

**Módulo:** 4 - APIs y Web Scraping
**Nivel:** Intermedio-Avanzado
**Duración estimada:** 1-2 semanas
**Pre-requisitos:** Tema 1 (APIs REST) y Tema 2 (Web Scraping)

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. ✅ **Implementar rate limiting** con diferentes algoritmos (Fixed Window, Token Bucket)
2. ✅ **Diseñar sistemas de cache** eficientes (memoria, disco, TTL)
3. ✅ **Programar requests asíncronos** con `aiohttp` y `asyncio`
4. ✅ **Medir y optimizar performance** (throughput, latencia, cache hit rate)
5. ✅ **Calcular ROI** de optimizaciones con métricas reales
6. ✅ **Integrar múltiples técnicas** en un scraper de producción

---

## 📚 Conceptos Clave

### 🚦 Rate Limiting (Cortesía)

> **Analogía:** Es como respetar el límite de velocidad en una carretera. No sobrecargas el servidor ajeno.

**Algoritmos:**

- **Fixed Window:** 100 requests por minuto (simple)
- **Token Bucket:** 20 requests/segundo con bursts de 50 (flexible)
- **Sliding Window:** 100 requests en ventana móvil de 60 segundos (preciso)

**Ejemplo:**

```python
from src.rate_limiter import crear_rate_limiter_token_bucket, puede_hacer_request

limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=10)

if puede_hacer_request(limiter):
    # Hacer request HTTP
    pass
```

---

### 💾 Caching (Eficiencia)

> **Analogía:** Es como guardar fotocopias de documentos que consultas frecuentemente. No tienes que ir al archivo cada vez.

**Tipos:**

- **Cache en memoria:** Diccionario Python (ultra rápido, volátil)
- **Cache en disco:** `shelve` (persistente, sobrevive reinicios)
- **Cache distribuido:** Redis (múltiples servidores, avanzado)

**TTL (Time To Live):**

```python
cache = crear_cache_disco("datos/cache.db", ttl=3600)  # 1 hora

datos = obtener_de_cache(cache, "https://api.example.com/products")
if datos is None:
    datos = requests.get(url).json()
    guardar_en_cache(cache, url, datos)
```

---

### ⚡ Async Requests (Velocidad)

> **Analogía:** Es como lavar platos mientras se cocina el arroz. Aprovechas el tiempo de espera haciendo otras cosas.

**Comparación:**

| Tipo          | 100 URLs     | Velocidad  |
| ------------- | ------------ | ---------- |
| **Síncrono**  | 100 segundos | 1 req/seg  |
| **Asíncrono** | 5 segundos   | 20 req/seg |

**Mejora:** **20x más rápido** ⚡

**Ejemplo:**

```python
import asyncio
from src.async_client import obtener_urls_batch

urls = ["https://api.example.com/1", "https://api.example.com/2", ...]

# Async con límite de concurrencia
resultados = await obtener_urls_batch(urls, max_concurrente=20)
```

---

### 📊 Métricas de Performance

> **Lo que no se mide, no se puede mejorar.**

**Métricas clave:**

1. **Throughput:** Requests por segundo (req/seg)
2. **Latencia:** Tiempo promedio por request (ms)
3. **Cache Hit Rate:** % de requests servidos desde cache
4. **ROI:** Ahorro de tiempo y dinero

**Dashboard:**

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

## 📁 Estructura del Tema

```
tema-3-rate-limiting-caching/
├── 01-TEORIA.md                     # ~3,500 palabras (20-25 min lectura)
│   ├── Rate Limiting (3 algoritmos)
│   ├── Caching (memoria, disco, Redis)
│   ├── Async requests (aiohttp, asyncio)
│   ├── Métricas de performance
│   └── Casos de uso en Data Engineering
│
├── 02-EJEMPLOS.md                   # 4 ejemplos trabajados
│   ├── Ejemplo 1: Rate limiting básico con time.sleep()
│   ├── Ejemplo 2: Cache persistente con shelve y TTL
│   ├── Ejemplo 3: Async requests (20x mejora)
│   └── Ejemplo 4: Scraper optimizado completo
│
├── 03-EJERCICIOS.md                 # 12 ejercicios con soluciones
│   ├── Básicos (1-4): Rate limiting, cache en memoria
│   ├── Intermedios (5-8): Token Bucket, async, comparaciones
│   └── Avanzados (9-12): Integración completa, dashboard
│
├── 04-proyecto-practico/            # Scraper masivo optimizado (TDD)
│   ├── src/
│   │   ├── rate_limiter.py          # 4 funciones
│   │   ├── cache_manager.py         # 5 funciones
│   │   ├── async_client.py          # 4 funciones
│   │   └── metricas.py              # 4 funciones
│   ├── tests/                       # 55 tests (41 ejecutables)
│   ├── ejemplos/                    # Ejemplos ejecutables
│   └── README.md                    # Documentación completa
│
├── REVISION_PEDAGOGICA.md           # Calificación: 9.4/10 ⭐⭐⭐⭐⭐
└── README.md                        # Este archivo
```

---

## 🚀 Cómo Estudiar Este Tema

### Orden Recomendado

#### 1. **Teoría (Día 1-2)** 📖

- Leer `01-TEORIA.md` (20-25 minutos)
- Tomar notas sobre algoritmos de rate limiting
- Ejecutar ejemplos de código incluidos
- Completar checklist de aprendizaje

**Criterio de éxito:**

- [ ] Explico qué es Fixed Window vs Token Bucket
- [ ] Entiendo diferencia entre cache en memoria vs disco
- [ ] Comprendo por qué async es más rápido
- [ ] Identifico métricas clave (throughput, latencia, cache hit rate)

---

#### 2. **Ejemplos (Día 3-4)** 💻

- Ejecutar `02-EJEMPLOS.md` línea por línea
- **Ejemplo 1:** Rate limiting básico (15 min)
- **Ejemplo 2:** Cache con `shelve` (20 min)
- **Ejemplo 3:** Async requests (30 min) ⭐
- **Ejemplo 4:** Scraper optimizado (45 min) ⭐⭐⭐

**Criterio de éxito:**

- [ ] Ejecuté los 4 ejemplos sin errores
- [ ] Medí mejora de velocidad en Ejemplo 3
- [ ] Entendí Dashboard de métricas en Ejemplo 4
- [ ] Puedo explicar por qué async es 20x más rápido

---

#### 3. **Ejercicios (Día 5-7)** ✍️

- Resolver `03-EJERCICIOS.md` progresivamente
- **Básicos (1-4):** 2-3 horas
- **Intermedios (5-8):** 4-5 horas
- **Avanzados (9-12):** 6-8 horas (opcionales)

**Criterio de éxito:**

- [ ] Completé ejercicios básicos (1-4)
- [ ] Completé al menos 2 ejercicios intermedios (5-8)
- [ ] Intenté 1 ejercicio avanzado (9-12)
- [ ] Comparé mis soluciones con las proporcionadas

---

#### 4. **Proyecto Práctico (Día 8-14)** 🏗️

- Leer `04-proyecto-practico/README.md`
- Instalar dependencias: `pip install -r requirements.txt`
- **Enfoque TDD:**
  1. Leer tests en `tests/test_rate_limiter.py`
  2. Ejecutar tests: `pytest tests/ -v`
  3. Estudiar implementación en `src/rate_limiter.py`
  4. Repetir para otros 3 módulos

**Criterio de éxito:**

- [ ] Instalé dependencias correctamente
- [ ] Ejecuté 41/41 tests (100% passing)
- [ ] Entendí implementación de Token Bucket
- [ ] Ejecuté ejemplo completo de scraper optimizado
- [ ] Medí métricas (throughput, cache hit rate)

---

## ✅ Criterios de Éxito

### Nivel Básico (Mínimo)

- [ ] Implemento rate limiting con `time.sleep()`
- [ ] Creo cache en memoria con diccionario
- [ ] Mido tiempo de ejecución de un scraper
- [ ] Calculo throughput (requests/segundo)
- [ ] Explico qué es TTL y por qué es importante

### Nivel Intermedio (Recomendado)

- [ ] Implemento Token Bucket rate limiting
- [ ] Creo cache persistente con `shelve` y TTL
- [ ] Implemento async requests con `aiohttp`
- [ ] Comparo velocidad: síncrono vs asíncrono
- [ ] Calculo cache hit rate y ROI

### Nivel Avanzado (Opcional)

- [ ] Integro async + cache + rate limiting + métricas
- [ ] Creo dashboard de métricas en tiempo real
- [ ] Optimizo scraper: 100 seg → <10 seg
- [ ] Documento decisiones de optimización con datos
- [ ] Implemento monitoreo de throughput y latencia

---

## 🛠️ Instalación y Configuración

### Requisitos

- Python 3.8+ (3.11+ recomendado)
- pip
- *(Opcional)* Docker para ejecutar Redis

### Instalar Dependencias

```bash
cd modulo-04-apis-scraping/tema-3-rate-limiting-caching/04-proyecto-practico
pip install -r requirements.txt
```

**Nota:** En Windows, `aiohttp` puede requerir compilador C. Ver sección [Troubleshooting](#-troubleshooting) más abajo.

### Ejecutar Tests

```bash
pytest tests/ -v
```

**Output esperado:**

```
======================== 41 passed in 7.02s ========================
```

### Ejecutar con Cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

Abrir `htmlcov/index.html` en el navegador para ver cobertura detallada.

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'aiohttp'`

**Problema:** `aiohttp` requiere compilador C en Windows.

**Solución 1 (Recomendada):** Usar Docker

```bash
docker build -t scraper-optimizado .
docker run -it scraper-optimizado pytest tests/ -v
```

**Solución 2:** Instalar Microsoft Visual C++ Build Tools

- Descargar: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Instalar componentes de C++
- Reintentar: `pip install aiohttp`

**Solución 3:** Usar Linux/Mac

- Los tests async funcionan sin problemas en Linux/Mac
- Alternativa: WSL2 en Windows

**Nota:** Los 3 módulos principales (`rate_limiter`, `cache_manager`, `metricas`) funcionan perfectamente sin `aiohttp`.

---

### Error: `RuntimeError: Event loop is closed`

**Problema:** Mal uso de `asyncio` en Python 3.10+.

**Solución:**

```python
# ❌ MAL
loop = asyncio.get_event_loop()
loop.run_until_complete(mi_funcion())

# ✅ BIEN
asyncio.run(mi_funcion())
```

---

### Tests Tardan Mucho

**Problema:** Tests con `time.sleep()` son lentos por diseño.

**Solución:**

- Ejecutar solo tests rápidos: `pytest tests/ -m "not slow"`
- Reducir timeouts en tests (solo para desarrollo)

---

## 📊 Métricas del Tema

| Métrica                     | Valor                     | Comparación                |
| --------------------------- | ------------------------- | -------------------------- |
| **Teoría**                  | 3,500 palabras            | +500 vs objetivo           |
| **Ejemplos**                | 4 ejemplos completos      | Objetivo cumplido          |
| **Ejercicios**              | 12 ejercicios             | 8 con soluciones completas |
| **Proyecto práctico**       | 4 módulos, 17 funciones   | TDD estricto               |
| **Tests**                   | 55 tests (41 ejecutables) | 100% passing               |
| **Cobertura**               | 88% (módulos principales) | >80% ✅                     |
| **Calificación pedagógica** | 9.4/10 ⭐⭐⭐⭐⭐              | Aprobado para producción   |

---

## 🎓 Competencias Desarrolladas

Al completar este tema, habrás desarrollado:

### Competencias Técnicas

1. ✅ **Rate Limiting:** Implementar algoritmos (Fixed Window, Token Bucket)
2. ✅ **Caching:** Diseñar sistemas de cache con TTL y persistencia
3. ✅ **Async Programming:** Programar con `aiohttp` y `asyncio`
4. ✅ **Performance Tuning:** Medir y optimizar scrapers (10x-20x mejora)
5. ✅ **TDD:** Test-Driven Development en optimización

### Competencias Profesionales

6. ✅ **Análisis de Métricas:** Interpretar throughput, latencia, cache hit rate
7. ✅ **Cálculo de ROI:** Justificar optimizaciones con datos económicos
8. ✅ **Toma de Decisiones:** Trade-offs (velocidad vs costo vs cortesía)
9. ✅ **Documentación Técnica:** README, docstrings, métricas
10. ✅ **Trabajo con Restricciones:** Respetar rate limits, robots.txt

---

## 🔗 Relación con Otros Temas

### Pre-requisitos

- **Tema 1 (APIs REST):** Requests HTTP, autenticación, reintentos
- **Tema 2 (Web Scraping):** BeautifulSoup, Selenium, almacenamiento

### Integración

Este tema **optimiza** los scrapers de los Temas 1 y 2:

- **Tema 1 + Tema 3:** API client optimizado con cache y async
- **Tema 2 + Tema 3:** Web scraper masivo con rate limiting y métricas

### Próximos Pasos

- **Módulo 5:** Bases de Datos Avanzadas (almacenar datos optimizados)
- **Módulo 6:** Apache Airflow (orquestar scrapers optimizados)
- **Módulo 7:** Cloud (desplegar scrapers en AWS Lambda)

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [aiohttp Documentation](https://docs.aiohttp.org/)
- [asyncio Python Docs](https://docs.python.org/3/library/asyncio.html)
- [Python shelve](https://docs.python.org/3/library/shelve.html)

### Artículos Recomendados

- [Rate Limiting Algorithms](https://en.wikipedia.org/wiki/Rate_limiting)
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket)
- [Cache Strategies](https://www.cloudflare.com/learning/cdn/caching-strategies/)
- [Async Python: The Complete Walkthrough](https://realpython.com/async-io-python/)

### Videos (Externos)

- "Async Python in 15 minutes" (YouTube)
- "Understanding Token Bucket" (YouTube)
- "Cache Strategies Explained" (YouTube)

---

## 🎯 Proyecto Final Sugerido

**Desafío:** Optimiza tu pipeline de Data Engineering favorito.

### Requisitos

1. **Selecciona un scraper lento** (del Tema 1 o 2)
2. **Mide performance inicial:**
   - Tiempo total de ejecución
   - Throughput (req/seg)
   - Latencia promedio
3. **Aplica 3 optimizaciones:**
   - Rate limiting (respetar términos de servicio)
   - Cache (reducir requests redundantes)
   - Async (aumentar throughput)
4. **Mide performance final:**
   - Tiempo total
   - Throughput
   - Cache hit rate
5. **Calcula ROI:**
   - Ahorro de tiempo (%)
   - Ahorro de costos ($)
   - Mejora de throughput (x veces)

### Entrega

- README con métricas antes/después
- Dashboard ASCII art con métricas
- Código con >80% cobertura
- Análisis de trade-offs

---

## 💡 Consejos de Estudio

1. **No te saltes los ejemplos:** Son la base del aprendizaje
2. **Mide todo:** Usa `time.time()` para comparar velocidades
3. **Empieza simple:** `time.sleep()` antes de Token Bucket
4. **Async es avanzado:** Está bien si toma tiempo dominarlo
5. **TDD es tu amigo:** Los tests te guían en el proyecto práctico
6. **Métricas importan:** Aprende a justificar optimizaciones con datos
7. **Practica con APIs reales:** JSONPlaceholder, OpenWeather, etc.
8. **Documenta decisiones:** Por qué elegiste X cache strategy o Y rate limit

---

## 🔐 Consideraciones de Seguridad y Ética

### Seguridad

- ✅ **Nunca expongas API keys** en código
- ✅ **Usa `.env` para credenciales**
- ✅ **Valida inputs** en funciones de cache
- ✅ **Limita tamaño de cache** (evitar memory leaks)

### Ética

- ✅ **Respeta rate limits** de APIs y sitios web
- ✅ **Identifícate con User-Agent** apropiado
- ✅ **No sobrecargues servidores** ajenos
- ✅ **Cache responsable:** Respeta TTL de APIs
- ✅ **Monitorea impacto:** Si tus requests causan problemas, reduce concurrencia

---

**Última actualización:** 2025-10-25
**Autor:** DataHub Inc. - Equipo de Data Engineering
**Calificación pedagógica:** 9.4/10 ⭐⭐⭐⭐⭐
**Estado:** ✅ Aprobado para Producción
**Nivel:** Intermedio-Avanzado
