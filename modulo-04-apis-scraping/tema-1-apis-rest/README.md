# Tema 1: APIs REST

**Módulo 4: APIs y Web Scraping**
**Master en Ingeniería de Datos**

---

## 📖 Descripción

Este tema te enseñará a **consumir APIs REST de forma profesional**, una habilidad fundamental para cualquier Data Engineer. Aprenderás a extraer datos de APIs públicas y privadas, manejar errores, implementar reintentos inteligentes, y crear clientes HTTP robustos y escalables.

**Empresa ficticia:** DataHub Inc. - Empresa de consultoría en Data Engineering

**Duración estimada:** 2-3 días (20-30 horas)

**Nivel de dificultad:** Intermedio

**Calificación pedagógica:** 9.2/10 ⭐ (Ver [REVISION_PEDAGOGICA.md](REVISION_PEDAGOGICA.md))

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este tema, serás capaz de:

1. ✅ **Entender APIs REST:** Comprender qué son, cómo funcionan y por qué son fundamentales en Data Engineering
2. ✅ **Dominar HTTP:** Usar los 4 métodos principales (GET, POST, PUT, DELETE) correctamente
3. ✅ **Interpretar respuestas:** Entender status codes (2xx, 3xx, 4xx, 5xx) y actuar en consecuencia
4. ✅ **Autenticar:** Implementar los 3 métodos principales (API Key, Bearer Token, Basic Auth)
5. ✅ **Manejar errores:** Crear sistemas robustos con reintentos inteligentes (exponential backoff)
6. ✅ **Trabajar con volumen:** Implementar paginación automática (Offset/Limit y Cursor)
7. ✅ **Respetar límites:** Aplicar rate limiting para no sobrecargar servidores
8. ✅ **Garantizar seguridad:** Consumir APIs de forma segura (solo HTTPS)

---

## 📚 Conceptos Clave

### 1. API REST = Restaurante con Menú 🍽️

Una API REST es como un restaurante:
- **Tú (cliente)** pides datos → Haces un **request**
- **El servidor** prepara los datos → Devuelve un **response**
- **El menú** lista qué puedes pedir → La **documentación**

### 2. Status Codes = Semáforos 🚦

Los códigos de estado son como semáforos:
- 🟢 **2xx:** Verde - Todo bien, sigue adelante
- 🟡 **3xx:** Amarillo - Redirección, ajusta tu ruta
- 🔴 **4xx:** Rojo - Tú hiciste algo mal
- 🔴 **5xx:** Rojo - Ellos tienen problemas

### 3. Rate Limiting = Límite de Velocidad 🚗

El rate limiting es como el límite de velocidad:
- No puedes ir más rápido de X requests por minuto
- Si lo haces, recibes una "multa" (error 429)
- Es para proteger la "carretera" (el servidor)

### 4. Paginación = Páginas de Google 📄

Dividir resultados en páginas:
- **Offset/Limit:** Como Google (página 1, 2, 3...)
- **Cursor:** Como un marcador de libro (guarda tu lugar)

---

## 📁 Estructura del Tema

```
tema-1-apis-rest/
├── 01-TEORIA.md              (~4,500 palabras, 30-45 min)
│   └── 9 conceptos fundamentales
│
├── 02-EJEMPLOS.md             (5 ejemplos, 100-125 min)
│   ├── 📗 Ejemplo 1: GET request básico
│   ├── 📗 Ejemplo 2: Autenticación con API Key
│   ├── 📙 Ejemplo 3: POST request
│   ├── 📙 Ejemplo 4: Paginación automática
│   └── 📕 Ejemplo 5: Reintentos con exponential backoff
│
├── 03-EJERCICIOS.md           (15 ejercicios, 6-10 horas)
│   ├── 📗 Ejercicios 1-5: Básicos
│   ├── 📙 Ejercicios 6-10: Intermedios
│   └── 📕 Ejercicios 11-15: Avanzados
│
├── 04-proyecto-practico/      (98 tests, 100% cobertura)
│   ├── src/
│   │   ├── validaciones.py    (validar URLs, timeouts, JSON)
│   │   ├── autenticacion.py   (API Key, Bearer, Basic Auth)
│   │   ├── cliente_http.py    (GET, POST, PUT, DELETE)
│   │   ├── reintentos.py      (exponential backoff)
│   │   └── paginacion.py      (Offset/Limit, Cursor)
│   ├── tests/                 (98 tests con pytest)
│   └── README.md              (documentación completa)
│
├── REVISION_PEDAGOGICA.md     (Calificación: 9.2/10)
└── README.md                  (este archivo)
```

---

## 🚀 Cómo Estudiar Este Tema

### Ruta Recomendada (Paso a Paso)

**Día 1: Fundamentos (4-6 horas)**

1. **Lee 01-TEORIA.md** (30-45 min)
   - Enfócate en entender los conceptos, no memorizar
   - Haz pausas cada 15 minutos
   - Marca secciones que no entiendas para revisar después

2. **Practica con 02-EJEMPLOS.md** (2-3 horas)
   - Ejecuta cada ejemplo en tu computadora
   - Modifica el código para experimentar
   - Progresión: Ejemplo 1 → 2 → 3

3. **Resuelve Ejercicios Básicos 1-5** (1-2 horas)
   - Intenta resolverlos sin ver las soluciones
   - Usa las pistas si te atascas
   - Valida con las soluciones al final

**Día 2: Práctica Intermedia (6-8 horas)**

4. **Continúa con Ejemplos 4-5** (1-2 horas)
   - Ejemplo 4: Paginación automática
   - Ejemplo 5: Reintentos inteligentes

5. **Resuelve Ejercicios Intermedios 6-10** (3-4 horas)
   - POST, PUT, DELETE requests
   - Paginación manual
   - Manejo de error 429

6. **Explora el Proyecto Práctico** (2 horas)
   - Lee `04-proyecto-practico/README.md`
   - Revisa el código en `src/`
   - Ejecuta los tests: `pytest tests/`

**Día 3: Integración Avanzada (6-8 horas)**

7. **Resuelve Ejercicios Avanzados 11-15** (4-6 horas)
   - Exponential backoff
   - Paginación automática completa
   - Pipeline ETL completo

8. **Profundiza en el Proyecto Práctico** (2-3 horas)
   - Estudia las funciones principales
   - Entiende cómo funcionan los tests (TDD)
   - Ejecuta los ejemplos en `04-proyecto-practico/ejemplos/`

9. **Autoevaluación** (30 min)
   - Completa el checklist en 01-TEORIA.md
   - Marca ejercicios completados en 03-EJERCICIOS.md
   - Verifica que puedes explicar cada concepto

---

### Orden Alternativo (Si tienes experiencia con APIs)

**Ruta Rápida (1 día, 8-10 horas):**

1. Lee 01-TEORIA.md en diagonal (15 min) - Solo refresca conceptos
2. Salta directo a Ejercicios Avanzados 11-15 (4-5 horas)
3. Estudia el Proyecto Práctico completo (3-4 horas)
4. Ejecuta todos los ejemplos del proyecto (1 hora)

---

## ✅ Criterios de Éxito

### Conocimientos (Puedes explicar)

- [ ] ¿Qué es una API REST y por qué es importante en Data Engineering?
- [ ] ¿Cuál es la diferencia entre GET, POST, PUT y DELETE?
- [ ] ¿Qué significa un status code 429 y cómo lo manejas?
- [ ] ¿Cuándo usarías Offset/Limit vs Cursor-based pagination?
- [ ] ¿Qué es exponential backoff y por qué se usa?

### Habilidades (Puedes hacer)

- [ ] Hacer GET request a una API pública (ej: JSONPlaceholder)
- [ ] Autenticar con API Key en headers
- [ ] Crear un recurso con POST request
- [ ] Implementar paginación automática
- [ ] Manejar errores 5xx con reintentos
- [ ] Respetar rate limiting en tu código
- [ ] Validar que solo usas HTTPS (rechazar HTTP)

### Proyecto (Puedes aplicar)

- [ ] Ejecutar todos los tests del proyecto: `pytest tests/` (98/98 pasando)
- [ ] Ejecutar todos los ejemplos en `04-proyecto-practico/ejemplos/`
- [ ] Modificar el proyecto para consumir una API diferente
- [ ] Explicar cómo funcionan los 5 módulos principales

---

## 🐛 Troubleshooting Común

### Problema 1: Error 401 (Unauthorized)

**Síntoma:** La API devuelve status code 401

**Causas comunes:**
- API key incorrecta o expirada
- API key no está en el header correcto
- Falta el prefijo `Bearer` en el token

**Solución:**
```python
# ❌ Mal
headers = {"Authorization": "mi-token"}

# ✅ Bien
headers = {"Authorization": "Bearer mi-token"}
```

---

### Problema 2: Error 429 (Too Many Requests)

**Síntoma:** Después de varios requests, recibes 429

**Causa:** Superaste el rate limit de la API

**Solución:**
```python
import time

# Añade delay entre requests
time.sleep(1)  # Espera 1 segundo

# O implementa exponential backoff (ver reintentos.py)
```

---

### Problema 3: Timeout en Requests

**Síntoma:** El request nunca termina (espera infinitamente)

**Causa:** No especificaste timeout

**Solución:**
```python
# ❌ Mal (puede esperar para siempre)
response = requests.get(url)

# ✅ Bien (falla después de 30 segundos)
response = requests.get(url, timeout=30)
```

---

### Problema 4: Error SSL Certificate

**Síntoma:** `SSLError: certificate verify failed`

**Causa:** Problema con certificados SSL

**Solución:**
```python
# Opción 1: Actualizar certifi
# pip install --upgrade certifi

# Opción 2 (solo para desarrollo, NUNCA en producción):
response = requests.get(url, verify=False)
```

---

### Problema 5: JSON Decode Error

**Síntoma:** `json.decoder.JSONDecodeError`

**Causa:** La respuesta no es JSON válido

**Solución:**
```python
# ✅ Valida el Content-Type primero
if response.headers.get('Content-Type') == 'application/json':
    data = response.json()
else:
    print(f"Respuesta no es JSON: {response.text[:200]}")
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Requests Library (Python)](https://requests.readthedocs.io/) - Librería principal usada
- [HTTP Status Codes - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) - Referencia completa
- [REST API Tutorial](https://restfulapi.net/) - Guía conceptual

### APIs Públicas para Practicar

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - API fake perfecta para testing
- [OpenWeather API](https://openweathermap.org/api) - Datos del clima (1,000 req/día gratis)
- [GitHub API](https://docs.github.com/en/rest) - Datos de repositorios
- [The Cat API](https://thecatapi.com/) - API de gatos (sí, en serio)
- [JSONbin.io](https://jsonbin.io/) - Almacenamiento JSON gratuito

### Herramientas Útiles

- [Postman](https://www.postman.com/) - Cliente visual para probar APIs
- [httpie](https://httpie.io/) - Cliente HTTP en CLI (mejor que curl)
- [RequestBin](https://requestbin.com/) - Inspecciona requests en tiempo real
- [JWT.io](https://jwt.io/) - Decodifica tokens JWT

### Lecturas Complementarias

- [Best Practices for REST API Design](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)
- [HTTP Status Dogs](https://httpstatusdogs.com/) - Status codes explicados con perros 🐕
- [Public APIs Repository](https://github.com/public-apis/public-apis) - Lista de 1,400+ APIs públicas

---

## 🔗 Navegación del Tema

### Archivos Principales

| Archivo                                          | Descripción                        | Tiempo Estimado |
| ------------------------------------------------ | ---------------------------------- | --------------- |
| [01-TEORIA.md](01-TEORIA.md)                     | Fundamentos teóricos (9 conceptos) | 30-45 min       |
| [02-EJEMPLOS.md](02-EJEMPLOS.md)                 | 5 ejemplos trabajados paso a paso  | 100-125 min     |
| [03-EJERCICIOS.md](03-EJERCICIOS.md)             | 15 ejercicios con soluciones       | 6-10 horas      |
| [04-proyecto-practico/](04-proyecto-practico/)   | Cliente HTTP robusto (TDD)         | 2-3 horas       |
| [REVISION_PEDAGOGICA.md](REVISION_PEDAGOGICA.md) | Validación pedagógica (9.2/10)     | 15 min lectura  |

### Navegación Rápida

```
📚 Fundamentos → 01-TEORIA.md
🔬 Ejemplos    → 02-EJEMPLOS.md
💪 Práctica    → 03-EJERCICIOS.md
🚀 Proyecto    → 04-proyecto-practico/README.md
🎓 Validación  → REVISION_PEDAGOGICA.md
```

---

## 📊 Métricas del Tema

| Métrica                     | Valor                   |
| --------------------------- | ----------------------- |
| **Archivos educativos**     | 5 archivos              |
| **Palabras totales**        | ~18,500 palabras        |
| **Ejemplos**                | 5 ejemplos completos    |
| **Ejercicios**              | 15 ejercicios           |
| **Tests**                   | 98 tests (100% pasando) |
| **Cobertura**               | 100%                    |
| **Calificación pedagógica** | 9.2/10 ⭐                |
| **Duración estimada**       | 20-30 horas             |
| **Nivel**                   | Intermedio              |

---

## 🎯 Próximo Paso

Después de completar este tema:

1. **Si dominas el contenido:** Avanza a **Tema 2: Web Scraping**
2. **Si necesitas más práctica:** Revisa los ejercicios que te costaron más
3. **Si quieres profundizar:** Implementa un cliente para una API real de tu elección

---

## 💡 Consejos de Estudio

### Para Principiantes

1. **No te apresures:** Tómate 3 días completos
2. **Ejecuta todo el código:** No solo leas, escribe y ejecuta
3. **Usa las pistas:** Están ahí para ayudarte
4. **Pide ayuda:** Si te atascas >30 min, busca ayuda

### Para Estudiantes con Experiencia

1. **Enfócate en lo nuevo:** Salta lo que ya sabes
2. **Desafíate:** Resuelve los ejercicios avanzados sin ver las pistas
3. **Mejora el proyecto:** Añade funcionalidades al proyecto práctico
4. **Enseña a otros:** La mejor forma de consolidar conocimiento

### Para Todos

1. **Haz pausas:** 15 min de descanso cada hora
2. **Toma notas:** Escribe tus propias analogías y ejemplos
3. **Experimenta:** Modifica el código, rompe cosas, arregla cosas
4. **Celebra logros:** Completar un ejercicio difícil merece reconocimiento 🎉

---

## 🆘 Soporte

Si tienes dudas o problemas:

1. **Revisa el Troubleshooting** en este README
2. **Lee la documentación** de `requests` o la API que uses
3. **Busca el error en Google** (probablemente alguien más lo tuvo)
4. **Pregunta en foros** como Stack Overflow

---

## 📝 Última Actualización

**Fecha:** 2025-10-23
**Versión:** 1.0
**Autor:** Equipo Master en Ingeniería de Datos
**Calificación pedagógica:** 9.2/10 ⭐

---

## 🎉 ¡Buena Suerte!

Estás a punto de dominar una de las habilidades más importantes en Data Engineering: **consumir APIs REST de forma profesional**.

**Este tema te preparará para:**
- ✅ Extraer datos de APIs públicas y privadas
- ✅ Manejar errores y reintentos de forma robusta
- ✅ Implementar paginación y rate limiting
- ✅ Crear clientes HTTP escalables
- ✅ Integrar APIs en pipelines ETL

**¡Disfruta el aprendizaje!** 🚀

---

*Este material es parte del Master en Ingeniería de Datos. Para más información, consulta el [README principal](../../README.md) del curso.*
