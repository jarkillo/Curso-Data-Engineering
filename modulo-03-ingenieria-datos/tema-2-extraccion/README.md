# Tema 2: Extracción de Datos

**Módulo**: 3 - Ingeniería de Datos Core
**Duración estimada**: 1-2 semanas
**Nivel**: Intermedio
**Prerrequisitos**: Tema 1 (Conceptos ETL)

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. **Extraer datos de archivos** (CSV, JSON, Excel) manejando encodings y estructuras complejas
2. **Consumir APIs REST** con autenticación, paginación y manejo robusto de errores
3. **Realizar web scraping ético** respetando robots.txt y rate limits
4. **Implementar reintentos automáticos** con backoff exponencial
5. **Consolidar datos de múltiples fuentes** en pipelines robustos
6. **Aplicar logging y monitoreo** en procesos de extracción

---

## 📚 Contenido del Tema

### 📖 Material Teórico

#### [01-TEORIA.md](01-TEORIA.md) (~6,500 palabras, 45-60 min)
**Contenido**:
- **Parte 1: Archivos**
  - CSV (encoding, delimitadores, headers)
  - JSON (plano, nested, JSON Lines)
  - Excel (múltiples sheets)
- **Parte 2: APIs REST**
  - Conceptos fundamentales (endpoints, métodos HTTP, headers)
  - Autenticación (API keys, Bearer tokens, Basic Auth)
  - Rate limiting y paginación
  - Manejo de errores y reintentos
- **Parte 3: Web Scraping**
  - Ética del scraping (robots.txt, User-Agent)
  - Beautiful Soup basics
  - Extracción de tablas HTML
  - Contenido dinámico vs estático
- **Parte 4: Logging y Monitoreo**
- **Parte 5: 5 Errores Comunes y Cómo Evitarlos**

**Características**:
- ✅ Explicaciones desde cero (sin asumir conocimientos previos)
- ✅ Analogías del mundo real para conceptos técnicos
- ✅ Buenas prácticas de Data Engineering
- ✅ Énfasis en seguridad y ética

---

#### [02-EJEMPLOS.md](02-EJEMPLOS.md) (5 ejemplos, 60-90 min)
**Ejemplos trabajados paso a paso**:

1. **CSV con Encoding Problemático** (⭐ Básico)
   - Detectar encoding automáticamente con `chardet`
   - Leer archivos Latin-1, UTF-8-BOM
   - Función reutilizable

2. **JSON Nested con Múltiples Niveles** (⭐⭐ Intermedio)
   - Aplanar estructuras complejas con `json_normalize()`
   - Extraer listas anidadas en tablas separadas
   - Calcular campos derivados

3. **API Paginada con Reintentos Automáticos** (⭐⭐ Intermedio)
   - Implementar reintentos con backoff exponencial
   - Paginación offset-based completa
   - Rate limiting y logging

4. **Scraping Básico con Beautiful Soup** (⭐ Básico)
   - Parsear HTML y extraer elementos
   - Scraping de tablas
   - Limpiar y estructurar datos

5. **Extracción Multi-Fuente** (⭐⭐⭐ Avanzado)
   - Consolidar CSV + API + Web scraping
   - Merge de múltiples DataFrames
   - Calcular KPIs y generar reportes

**Todas las soluciones son ejecutables y testeadas**.

---

#### [03-EJERCICIOS.md](03-EJERCICIOS.md) (15 ejercicios, 4-8 horas)
**Ejercicios graduados con soluciones completas**:

**Básicos (1-5)** - ⭐
- Detección automática de encoding
- Lectura de JSON Lines
- Múltiples hojas de Excel
- Limpieza de CSV con valores nulos
- Validación de estructura

**Intermedios (6-10)** - ⭐⭐
- API con autenticación Bearer
- Paginación offset-based
- Manejo de rate limit 429
- Scraping de tablas HTML
- Verificar robots.txt

**Avanzados (11-15)** - ⭐⭐⭐
- Pipeline multi-fuente completo
- Extracción con logging robusto
- API oculta vs scraping
- Sistema de caché
- Pipeline orquestado end-to-end

**Incluye**: Tabla de autoevaluación y criterios de éxito

---

### 💻 Proyecto Práctico (4-6 días)

#### [04-proyecto-practico/](04-proyecto-practico/) - Sistema de Extracción Multi-Fuente
**Contexto**: Construir un sistema profesional de extracción de datos para análisis de mercado.

**Arquitectura** (TDD estricto):
```
src/
├── extractor_archivos.py    (6 funciones - CSV, JSON, Excel)
├── extractor_apis.py         (5 funciones - REST, auth, paginación)
├── extractor_web.py          (4 funciones - Scraping ético)
├── gestor_extracciones.py    (4 funciones - Orquestación, logging)
└── validadores.py            (5 funciones - Validación de datos)

tests/
├── test_extractor_archivos.py    (~15 tests)
├── test_extractor_apis.py        (~15 tests)
├── test_extractor_web.py         (~12 tests)
├── test_gestor_extracciones.py   (~12 tests)
└── test_validadores.py           (~15 tests)
```

**Características**:
- ✅ 70+ tests unitarios (TDD)
- ✅ >85% cobertura de código
- ✅ Logging completo
- ✅ Manejo robusto de errores
- ✅ Datos de ejemplo incluidos
- ✅ Configuración completa (pytest, requirements)

---

## 🗺️ Ruta de Aprendizaje Recomendada

### Opción A: Secuencial Completo (Recomendado)
**Duración**: 1-2 semanas

```
Día 1-2: Leer 01-TEORIA.md + 02-EJEMPLOS.md
         Ejecutar todos los ejemplos

Día 3:   Hacer ejercicios 1-5 (básicos)
         Revisar soluciones

Día 4:   Hacer ejercicios 6-10 (intermedios)
         Revisar soluciones

Día 5:   Hacer ejercicios 11-15 (avanzados)
         Revisar soluciones

Día 6-10: Proyecto práctico TDD
          Implementar los 5 módulos
          Escribir tests (>85% cobertura)
```

### Opción B: Solo Teoría y Ejemplos (Rápido)
**Duración**: 2-3 días

```
Día 1: Leer 01-TEORIA.md (45-60 min)
       Ejecutar 5 ejemplos de 02-EJEMPLOS.md (2-3 horas)

Día 2: Hacer ejercicios seleccionados: 1, 3, 6, 9, 11, 15 (4 horas)

Día 3: Revisar código del proyecto práctico (2 horas)
```

### Opción C: Solo Proyecto (Experiencia Previa)
**Duración**: 4-6 días

Si ya tienes experiencia con extracción de datos:
```
Día 1: Leer 01-TEORIA.md (enfoque en buenas prácticas)
       Revisar 02-EJEMPLOS.md como referencia

Día 2-6: Implementar proyecto práctico completo con TDD
```

---

## 🛠️ Requisitos Técnicos

### Librerías Necesarias
```bash
pip install requests beautifulsoup4 pandas openpyxl chardet pytest pytest-cov
```

### Versiones Recomendadas
- Python: 3.11+
- requests: >=2.32.4
- beautifulsoup4: >=4.12.0
- pandas: >=2.1.0
- openpyxl: >=3.1.0
- chardet: >=5.2.0

### Herramientas Opcionales
- Postman/Insomnia (para probar APIs)
- DB Browser for SQLite (para inspeccionar datos)
- Jupyter Notebook (para experimentar)

---

## 📊 Evaluación y Calidad

### Revisión Pedagógica
- **Calificación**: 9.5/10 ⭐⭐⭐⭐⭐
- **Progresión**: Sin saltos conceptuales
- **Claridad**: Analogías efectivas
- **Aplicabilidad**: Casos reales de Data Engineering
- Ver [REVISION_PEDAGOGICA.md](REVISION_PEDAGOGICA.md) para detalles

### Criterios de Éxito

Has completado exitosamente este tema si:
- ✅ Puedes extraer datos de CSV con cualquier encoding
- ✅ Puedes consumir APIs REST con paginación y reintentos
- ✅ Puedes hacer scraping respetando ética y rate limits
- ✅ Puedes consolidar datos de múltiples fuentes
- ✅ Implementas logging en tus extracciones
- ✅ Manejas errores de forma robusta

**Validación práctica**: Completa el ejercicio 15 (Pipeline completo) exitosamente.

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [requests](https://requests.readthedocs.io/) - HTTP library
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraping
- [pandas](https://pandas.pydata.org/docs/) - Data manipulation
- [chardet](https://chardet.readthedocs.io/) - Encoding detection

### APIs Públicas para Practicar
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - API de prueba gratuita
- [OpenWeatherMap](https://openweathermap.org/api) - API de clima
- [REST Countries](https://restcountries.com/) - Datos de países

### Ética de Web Scraping
- [robots.txt checker](https://en.ryte.com/free-tools/robots-txt/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

### Lecturas Complementarias
- "Web Scraping with Python" - Ryan Mitchell
- "RESTful Web APIs" - Leonard Richardson

---

## 💡 Tips para el Éxito

### Durante el Estudio
1. **Ejecuta todo el código**: No solo leas, prueba cada ejemplo
2. **Modifica los ejemplos**: Cambia parámetros, añade funcionalidad
3. **Usa debugging**: Pon breakpoints, inspecciona variables
4. **Toma notas**: Documenta patrones que encuentres útiles

### Durante los Ejercicios
1. **Lee el contexto**: Entender el problema es clave
2. **Intenta primero**: Dedica 15-30 min antes de ver la solución
3. **Compara soluciones**: Aprende de las diferencias con tu código
4. **Refactoriza**: Mejora tu código después de ver la solución

### Durante el Proyecto
1. **TDD estricto**: Test primero, código después
2. **Commits pequeños**: Commitea cada función que completes
3. **Refactoriza**: Limpia código después de que los tests pasen
4. **Documenta**: Escribe docstrings para todas las funciones

---

## 🚨 Troubleshooting

### Problema: UnicodeDecodeError al leer CSV
**Solución**: Usa `chardet` para detectar el encoding automáticamente
```python
import chardet
with open('file.csv', 'rb') as f:
    encoding = chardet.detect(f.read())['encoding']
df = pd.read_csv('file.csv', encoding=encoding)
```

### Problema: Error 429 (Too Many Requests) en API
**Solución**: Implementa rate limiting con `time.sleep()`
```python
import time
response = requests.get(url)
time.sleep(1)  # 1 segundo entre peticiones
```

### Problema: Beautiful Soup no encuentra elementos
**Solución**: Verifica el HTML real (puede ser diferente al esperado)
```python
print(soup.prettify())  # Ver estructura HTML
```

### Problema: Tests fallan en proyecto
**Solución**: Verifica que estás en el directorio correcto
```bash
cd 04-proyecto-practico
pytest -v
```

---

## 📞 Soporte

### ¿Dudas sobre conceptos?
- Revisa la sección correspondiente en 01-TEORIA.md
- Busca en "Errores Comunes" (Parte 5)
- Consulta las soluciones de ejercicios similares

### ¿Problemas técnicos?
- Verifica versiones de librerías
- Consulta la sección Troubleshooting arriba
- Revisa logs de error completos

### ¿Necesitas más práctica?
- Repite ejercicios modificando el contexto
- Busca APIs públicas adicionales para practicar
- Implementa variaciones del proyecto práctico

---

## ✅ Checklist de Completitud

- [ ] Leí 01-TEORIA.md completamente
- [ ] Ejecuté los 5 ejemplos de 02-EJEMPLOS.md
- [ ] Completé ejercicios básicos (1-5)
- [ ] Completé ejercicios intermedios (6-10)
- [ ] Completé ejercicios avanzados (11-15)
- [ ] Implementé proyecto práctico con TDD
- [ ] Tests del proyecto >85% cobertura
- [ ] Todos los tests pasan
- [ ] Código sin errores de linting
- [ ] Documenté funciones principales

**Si completaste 9+ items**: ¡Felicidades! Dominas extracción de datos 🎉

---

## 🔜 Próximos Pasos

Después de completar este tema:

1. **Tema 3: Transformación con Pandas** (modulo-03-ingenieria-datos/tema-3-transformacion/)
   - DataFrames avanzados
   - Operaciones: filter, map, apply, groupby
   - Merge, join, concat
   - Limpieza y preparación de datos

2. **Tema 4: Calidad de Datos** (modulo-03-ingenieria-datos/tema-4-calidad/)
   - Validación de esquemas
   - Detección de duplicados y outliers
   - Data profiling
   - Frameworks de calidad

3. **Proyecto Integrador del Módulo 3**
   - Pipeline ETL completo end-to-end
   - Integra extracción, transformación y calidad
   - Arquitectura Bronze/Silver/Gold

---

**¡Éxito en tu aprendizaje de extracción de datos!** 🚀📊

---

**Última actualización**: 2025-10-30
**Versión**: 1.0.0
**Issue Linear**: [JAR-265](https://linear.app/jarko/issue/JAR-265)
**Calificación Pedagógica**: 9.5/10 ⭐⭐⭐⭐⭐
