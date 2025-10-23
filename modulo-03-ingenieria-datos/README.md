# Módulo 3: Ingeniería de Datos Core (ETL/ELT y Pipelines)

**Duración estimada**: 10-12 semanas
**Nivel**: Intermedio
**Prerrequisitos**: Módulo 1 (Fundamentos) y Módulo 2 (SQL Básico)

---

## 🎯 Objetivos del Módulo

Al completar este módulo, serás capaz de:

1. **Diseñar y construir pipelines ETL/ELT** robustos y escalables
2. **Extraer datos** de múltiples fuentes (archivos, APIs, web scraping)
3. **Transformar datos** con Pandas de forma eficiente
4. **Validar la calidad** de los datos con frameworks profesionales
5. **Trabajar con formatos modernos** (JSON, Parquet, Avro)
6. **Implementar estrategias de carga** optimizadas (full, incremental, upsert)
7. **Aplicar logging y monitoreo** en pipelines de producción

---

## 📚 Estructura del Módulo

### Tema 1: Conceptos de ETL/ELT ✅
- **Duración**: 1 semana
- **Estado**: ✅ **COMPLETADO 100%** (2025-10-23)
- **Calificación pedagógica**: 9.2/10 ⭐⭐⭐⭐⭐
- **Contenido**:
  - ✅ `01-TEORIA.md`: ~4,500 palabras, 7 conceptos fundamentales
  - ✅ `02-EJEMPLOS.md`: 5 ejemplos progresivos (código ejecutable)
  - ✅ `03-EJERCICIOS.md`: 15 ejercicios con soluciones completas
  - ✅ `REVISION_PEDAGOGICA.md`: Validación pedagógica aprobada
  - ✅ `04-proyecto-practico/`: Pipeline ETL completo con TDD (64 tests)
- **Proyecto**: Pipeline ETL de Ventas de E-commerce con validación, logging, métricas e idempotencia

### Tema 2: Extracción de Datos ⏳
- **Duración**: 1-2 semanas
- **Estado**: ⏳ Pendiente
- **Contenido**:
  - Lectura de archivos (CSV, JSON, Excel)
  - Consumo de APIs REST
  - Web scraping ético
  - Rate limiting y paginación
  - Manejo de errores y retries
- **Proyecto**: Sistema de extracción multi-fuente

### Tema 3: Transformación con Pandas ⏳
- **Duración**: 1-2 semanas
- **Estado**: ⏳ Pendiente
- **Contenido**:
  - DataFrames y Series
  - Operaciones comunes (filter, map, apply, groupby)
  - Merge, join, concat
  - Manejo de valores nulos
  - Pivoting y reshape
- **Proyecto**: Pipeline de transformación

### Tema 4: Calidad de Datos ⏳
- **Duración**: 1 semana
- **Estado**: ⏳ Pendiente
- **Contenido**:
  - Dimensiones de calidad
  - Validación de esquemas
  - Detección de duplicados
  - Manejo de outliers
  - Data profiling
- **Proyecto**: Framework de calidad reutilizable

### Tema 5: Formatos de Datos Modernos ⏳
- **Duración**: 1 semana
- **Estado**: ⏳ Pendiente
- **Contenido**:
  - JSON y JSON Lines
  - Parquet (columnar storage)
  - Avro (schemas evolutivos)
  - Comparación de formatos
- **Proyecto**: Conversor multi-formato

### Tema 6: Carga de Datos y Pipelines Completos ⏳
- **Duración**: 1-2 semanas
- **Estado**: ⏳ Pendiente
- **Contenido**:
  - Estrategias de carga (full load, incremental, upsert)
  - Bulk inserts optimizados
  - Particionamiento de datos
  - Logging y monitoreo
- **Proyecto**: Pipeline ETL completo

### Proyecto Integrador ⏳
- **Duración**: 2 semanas
- **Estado**: ⏳ Pendiente
- **Descripción**: Pipeline de análisis de noticias
  - Extracción desde API de noticias
  - Transformación con Pandas
  - Validación de calidad
  - Carga en PostgreSQL + Parquet
  - Arquitectura Bronze/Silver/Gold
  - CLI para ejecución
  - Tests: >80% cobertura

---

## 🗺️ Progreso del Módulo

```
Tema 1: ████████████████████ 100% ✅ COMPLETADO
Tema 2: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Tema 3: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Tema 4: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Tema 5: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Tema 6: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Integrador: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
───────────────────────────────────────────────
Total:  ███░░░░░░░░░░░░░░░░░  17% 🔄 En progreso
```

---

## 🛠️ Tecnologías y Herramientas

### Utilizadas en este módulo
- **Python 3.13+**: Lenguaje principal
- **Pandas**: Transformación de datos
- **Requests**: Consumo de APIs REST
- **Beautiful Soup**: Web scraping
- **Parquet (pyarrow)**: Formato columnar
- **Great Expectations**: Calidad de datos
- **SQLite/PostgreSQL**: Almacenamiento
- **pytest**: Testing (TDD)

### Aprenderás a usar
- ETL/ELT patterns
- Data validation frameworks
- Modern data formats (Parquet, Avro)
- Bulk loading strategies
- Logging y monitoreo
- Pipeline orchestration concepts

---

## 📋 Metodología de Aprendizaje

Cada tema sigue la misma estructura probada:

1. **Teoría** (`01-TEORIA.md`):
   - Conceptos explicados desde cero
   - Analogías del mundo real
   - Aplicaciones en Data Engineering
   - ~4,000 palabras, 30-45 min lectura

2. **Ejemplos** (`02-EJEMPLOS.md`):
   - 5 ejemplos trabajados paso a paso
   - Código ejecutable
   - Contexto empresarial realista
   - ~45-60 min lectura

3. **Ejercicios** (`03-EJERCICIOS.md`):
   - 15 ejercicios con dificultad progresiva
   - Soluciones completas
   - Autoevaluación
   - ~2-4 horas de práctica

4. **Proyecto Práctico** (`04-proyecto-practico/`):
   - Implementación TDD
   - Tests: >80% cobertura
   - Código limpio y documentado
   - ~3-5 días de trabajo

5. **Revisión Pedagógica** (`REVISION_PEDAGOGICA.md`):
   - Validación por Psicólogo Educativo
   - Objetivo: >9.0/10
   - Garantía de calidad pedagógica

---

## ✅ Criterios de Calidad

### Por Tema
- ✅ Contenido educativo completo (teoría, ejemplos, ejercicios)
- ✅ Revisión pedagógica aprobada (>9.0/10)
- ✅ Proyecto práctico con TDD
- ✅ Cobertura de tests >80%
- ✅ 0 errores de linting (flake8)
- ✅ Código formateado (black)
- ✅ Documentación completa

### Módulo Completo
- ✅ 6 temas completados con calidad excelente
- ✅ Proyecto integrador funcional
- ✅ Cobertura promedio >80%
- ✅ Revisión pedagógica final: >9.0/10
- ✅ CHANGELOG actualizado

---

## 🚀 Cómo Usar Este Módulo

### 1. Secuencial (Recomendado)
Completa los temas en orden:
```
Tema 1 → Tema 2 → Tema 3 → Tema 4 → Tema 5 → Tema 6 → Proyecto Integrador
```

**Por qué**: Cada tema se construye sobre el anterior. El Tema 1 es fundamental para entender los siguientes.

### 2. Por Necesidad
Si ya tienes experiencia, puedes ir directamente a un tema específico:
- **Extracción de datos**: Tema 2
- **Transformación con Pandas**: Tema 3
- **Calidad de datos**: Tema 4
- **Formatos modernos**: Tema 5

### 3. Solo Proyectos
Si prefieres aprender haciendo:
1. Lee la teoría rápidamente
2. Salta directamente al proyecto práctico
3. Vuelve a la teoría cuando tengas dudas

---

## 📊 Estimación de Tiempo

### Por Tema
- Lectura de teoría: 30-45 min
- Revisión de ejemplos: 45-60 min
- Ejercicios prácticos: 2-4 horas
- Proyecto práctico: 3-5 días
- **Total por tema**: 1-2 semanas

### Módulo Completo
- 6 temas: 6-12 semanas
- Proyecto integrador: 2 semanas
- **Total**: 8-14 semanas

**Nota**: Los tiempos varían según tu dedicación (10-20 horas/semana)

---

## 🎓 Prerequisitos Verificados

Antes de empezar este módulo, deberías haber completado:

### Del Módulo 1 (Fundamentos)
- ✅ Python básico (funciones, variables, tipos de datos)
- ✅ Manejo de errores (try/except)
- ✅ Lectura/escritura de archivos
- ✅ Tests básicos con pytest
- ✅ Procesamiento de CSV

### Del Módulo 2 (SQL)
- ✅ SELECT, WHERE, ORDER BY
- ✅ Funciones agregadas (COUNT, SUM, AVG)
- ✅ GROUP BY, HAVING
- ✅ Conexión a bases de datos desde Python

Si no has completado estos módulos, te recomendamos hacerlo primero.

---

## 💡 Consejos de Estudio

1. **No te saltes la teoría**: Parece tentador ir directo al código, pero la teoría te ahorrará tiempo después
2. **Experimenta con los ejemplos**: Modifica el código, prueba cosas diferentes
3. **Haz todos los ejercicios**: La práctica es fundamental
4. **Construye el proyecto paso a paso**: No intentes hacerlo todo de golpe
5. **Usa TDD**: Escribir tests primero te ayuda a pensar mejor
6. **Pide ayuda**: Usa Stack Overflow, comunidades de Data Engineering
7. **Construye tu portafolio**: Sube tus proyectos a GitHub

---

## 🔗 Recursos Adicionales

### Libros Recomendados
- "Data Pipelines Pocket Reference" - James Densmore
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Python for Data Analysis" - Wes McKinney

### Comunidades
- r/dataengineering (Reddit)
- Data Engineering Weekly (Newsletter)
- Stack Overflow (tag: data-engineering)

### Herramientas Online
- Kaggle (datasets para practicar)
- Google Colab (notebooks gratis)
- DB Fiddle (practicar SQL online)

---

## 📞 Soporte

### Problemas Técnicos
- Revisa la sección "Troubleshooting" en cada README
- Consulta la documentación oficial de cada herramienta
- Pregunta en Stack Overflow

### Dudas Pedagógicas
- Revisa la sección "Errores Comunes" en cada teoría
- Consulta los ejemplos trabajados
- Revisa los ejercicios resueltos

---

## 📝 Licencia

Este módulo es material educativo de código abierto para aprendizaje personal.

---

**Última actualización**: 2025-10-23
**Versión**: 1.0.0
**Issue Linear**: [JAR-189](https://linear.app/jarko/issue/JAR-189)

**¡Bienvenido al Módulo 3! Prepárate para convertirte en un experto en pipelines de datos 🚀📊**
