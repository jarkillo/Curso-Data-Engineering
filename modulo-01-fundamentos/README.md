# Módulo 1: Fundamentos de Programación y Herramientas

## Información del Módulo

- **Duración:** 8-10 semanas
- **Nivel:** Principiante
- **Estado:** ✅ **COMPLETADO** (3/3 temas terminados)
- **Tests totales:** 143 pasando (100%)
- **Última actualización:** 2025-11-10

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Escribir programas en Python con sintaxis correcta y estilo limpio
- ✅ Utilizar tipado explícito para mejor documentación y detección de errores
- ✅ Aplicar TDD (Test-Driven Development) escribiendo tests antes del código
- ✅ Validar inputs de manera robusta para garantizar seguridad
- ✅ Manejar errores con excepciones específicas
- ✅ Formatear código con black y validar con flake8
- ✅ Procesar archivos CSV con manejo robusto de errores
- ✅ Implementar logging profesional con diferentes niveles
- ✅ Escribir funciones puras sin efectos secundarios
- ✅ Utilizar context managers para recursos
- ✅ Configurar entornos virtuales profesionales

**Estado:** ✅ Todos los objetivos completados

---

## 📚 Contenido del Módulo

### Tema 1: Python y Estadística Básica ✅

**Estado:** ✅ Completado (2025-10-19)
**Ruta:** [`tema-1-python-estadistica/`](./tema-1-python-estadistica/)

#### Contenido Teórico

- **[01-TEORIA.md](./tema-1-python-estadistica/01-TEORIA.md)**: Fundamentos de estadística descriptiva
  - Media, mediana, moda
  - Varianza y desviación estándar
  - Percentiles y cuartiles
  - Interpretación de resultados

- **[02-EJEMPLOS.md](./tema-1-python-estadistica/02-EJEMPLOS.md)**: 5 ejemplos trabajados paso a paso
  - Análisis de ventas (DataBite)
  - Tiempos de respuesta de APIs (CloudMetrics)
  - Control de calidad
  - Análisis de salarios
  - Performance de servidores

- **[03-EJERCICIOS.md](./tema-1-python-estadistica/03-EJERCICIOS.md)**: 15 ejercicios graduados
  - 5 ejercicios básicos (⭐)
  - 5 ejercicios intermedios (⭐⭐)
  - 5 ejercicios avanzados (⭐⭐⭐)
  - Soluciones completas con explicaciones

#### Proyecto Práctico

**Ruta:** [`tema-1-python-estadistica/04-proyecto-practico/`](./tema-1-python-estadistica/04-proyecto-practico/)

**Descripción:** Calculadora de estadísticas básicas con TDD estricto

**Funciones implementadas:**
- `calcular_media()` - Media aritmética con validación
- `calcular_mediana()` - Mediana robusta (pares e impares)
- `calcular_moda()` - Moda con soporte multimodal
- `calcular_varianza()` - Varianza poblacional y muestral
- `calcular_desviacion_estandar()` - Desviación estándar
- `calcular_percentiles()` - Percentiles con interpolación lineal

**Métricas:**
- ✅ 51 tests unitarios (100% pasando)
- ✅ Coverage: 89%
- ✅ 0 errores flake8
- ✅ Código formateado con black
- ✅ Docstrings completos con ejemplos
- ✅ Type hints en todas las funciones

**Conceptos aplicados:**
- Test-Driven Development (TDD)
- Funciones puras sin efectos secundarios
- Validación exhaustiva de inputs
- Manejo de excepciones específicas
- Documentación profesional

---

### Tema 2: Procesamiento de Archivos CSV ✅

**Estado:** ✅ Completado
**Ruta:** [`tema-2-procesamiento-csv/`](./tema-2-procesamiento-csv/)

#### Contenido Teórico

- **[01-TEORIA.md](./tema-2-procesamiento-csv/01-TEORIA.md)**: Manejo de archivos y CSV
  - Módulo csv de Python
  - Pathlib para rutas multiplataforma
  - Manejo de encodings
  - Validación de esquemas
  - Limpieza de datos

- **[02-EJEMPLOS.md](./tema-2-procesamiento-csv/02-EJEMPLOS.md)**: Ejemplos prácticos
  - Lectura de CSV con diferentes delimitadores
  - Validación de tipos de datos
  - Limpieza de duplicados y nulos
  - Transformaciones de datos
  - Escritura de CSV procesados

- **[03-EJERCICIOS.md](./tema-2-procesamiento-csv/03-EJERCICIOS.md)**: Ejercicios graduados
  - Lectura y escritura básica
  - Validación de esquemas
  - Transformaciones complejas
  - Manejo de errores
  - Soluciones completas

- **[REVISION_PEDAGOGICA.md](./tema-2-procesamiento-csv/REVISION_PEDAGOGICA.md)**: Validación pedagógica ✅

#### Proyecto Práctico

**Ruta:** [`tema-2-procesamiento-csv/04-proyecto-practico/`](./tema-2-procesamiento-csv/04-proyecto-practico/)

**Descripción:** Sistema de procesamiento y validación de archivos CSV

**Módulos implementados:**
- `lector_csv.py` - Lectura robusta de CSV
- `escritor_csv.py` - Escritura con validación
- `validador_csv.py` - Validación de esquemas y tipos
- `transformador_csv.py` - Transformaciones de datos
- `limpiador_csv.py` - Limpieza de duplicados y nulos

**Métricas:**
- ✅ 54 tests unitarios (100% pasando)
- ✅ Coverage: >85%
- ✅ Manejo robusto de errores
- ✅ Soporte multiplataforma (Windows/Linux/Mac)
- ✅ Tests con archivos fixture

**Conceptos aplicados:**
- Manejo de archivos con pathlib
- Context managers
- Validación de esquemas
- Limpieza de datos
- Transformaciones funcionales

---

### Tema 3: Logging y Debugging ✅

**Estado:** ✅ Completado
**Ruta:** [`tema-3-logs-debugging/`](./tema-3-logs-debugging/)

#### Contenido Teórico

- **[01-TEORIA.md](./tema-3-logs-debugging/01-TEORIA.md)**: Sistema de logging profesional
  - Módulo logging de Python
  - Niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Handlers y Formatters
  - Logging estructurado
  - Best practices

- **[02-EJEMPLOS.md](./tema-3-logs-debugging/02-EJEMPLOS.md)**: Casos de uso reales
  - Logger básico
  - Múltiples outputs (consola + archivo)
  - Rotación de archivos
  - Logs estructurados (JSON)
  - Decoradores para logging

- **[03-EJERCICIOS.md](./tema-3-logs-debugging/03-EJERCICIOS.md)**: Práctica guiada
  - Configuración de loggers
  - Diferentes niveles de log
  - Formateo personalizado
  - Debugging con logs
  - Soluciones completas

- **[REVISION_PEDAGOGICA.md](./tema-3-logs-debugging/REVISION_PEDAGOGICA.md)**: Validación pedagógica ✅

#### Proyecto Práctico

**Ruta:** [`tema-3-logs-debugging/04-proyecto-practico/`](./tema-3-logs-debugging/04-proyecto-practico/)

**Descripción:** Sistema de logging configurable y pipeline con trazabilidad

**Módulos implementados:**
- `logger_config.py` - Configuración centralizada
- `custom_logger.py` - Logger personalizado
- `log_decorators.py` - Decoradores para logging automático
- `pipeline_logs.py` - Pipeline ETL con logging completo

**Métricas:**
- ✅ 38 tests unitarios (100% pasando)
- ✅ Coverage: >85%
- ✅ Múltiples outputs (consola, archivo, JSON)
- ✅ Decoradores reutilizables
- ✅ Trazabilidad completa de operaciones

**Conceptos aplicados:**
- Sistema de logging profesional
- Patrones de diseño (Decorator)
- Configuración desde código
- Context managers
- Structured logging

---

## 📊 Progreso del Módulo

```
Tema 1: Python y Estadística      ████████████████████ 100% ✅ (51 tests)
Tema 2: Procesamiento CSV          ████████████████████ 100% ✅ (54 tests)
Tema 3: Logging y Debugging        ████████████████████ 100% ✅ (38 tests)
────────────────────────────────────────────────────────────────────────
Total:                             ████████████████████ 100% ✅ (143 tests)
```

**Resumen de métricas:**
- ✅ **3/3 temas completados** (100%)
- ✅ **143 tests unitarios** pasando
- ✅ **Coverage promedio:** >85%
- ✅ **0 errores** de flake8
- ✅ **Código formateado** con black
- ✅ **Type hints** completos
- ✅ **Documentación** profesional

---

## 🛠️ Herramientas Utilizadas

- ✅ **Python 3.13+** - Lenguaje de programación
- ✅ **pytest** - Framework de testing (143 tests)
- ✅ **pytest-cov** - Medición de cobertura
- ✅ **black** - Formateador de código (estilo consistente)
- ✅ **flake8** - Linter para validación de estilo
- ✅ **mypy** - Type checking estático
- ✅ **pathlib** - Manejo de rutas multiplataforma
- ✅ **logging** - Sistema de logging profesional

---

## 🎓 Conceptos Clave Aprendidos

### Programación Funcional
- ✅ Funciones puras sin efectos secundarios
- ✅ Inmutabilidad de datos
- ✅ Composición de funciones
- ✅ Higher-order functions

### Calidad de Código
- ✅ Test-Driven Development (TDD)
- ✅ Coverage >80% como mínimo
- ✅ Tipado explícito (type hints)
- ✅ Docstrings con ejemplos
- ✅ Código autoexplicativo

### Seguridad
- ✅ Validación exhaustiva de inputs
- ✅ Manejo de excepciones específicas
- ✅ No confiar en datos externos
- ✅ Validación de tipos y rangos

### Best Practices
- ✅ DRY (Don't Repeat Yourself)
- ✅ KISS (Keep It Simple, Stupid)
- ✅ YAGNI (You Aren't Gonna Need It)
- ✅ Single Responsibility Principle

---

## 📖 Recursos de Aprendizaje

### Libros Recomendados
- **"Python Crash Course"** - Eric Matthes (principiantes)
- **"Clean Code in Python"** - Mariano Anaya (intermedios)
- **"Fluent Python"** - Luciano Ramalho (avanzados)
- **"Test-Driven Development with Python"** - Harry Percival

### Cursos Online
- [Real Python - Python Basics](https://realpython.com/)
- [DataCamp - Introduction to Python](https://www.datacamp.com/)
- [Test Automation University - Python](https://testautomationu.applitools.com/)

### Documentación Oficial
- [Python Official Docs](https://docs.python.org/3/) - Referencia completa
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [black Documentation](https://black.readthedocs.io/) - Code formatter
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Typing system

---

## ✅ Criterios de Evaluación

Para considerar este módulo completado:

- [x] **Completar los 3 temas** con teoría, ejemplos y ejercicios
- [x] **Implementar los 3 proyectos prácticos** funcionales
- [x] **Escribir código con tipado explícito** (type hints)
- [x] **Alcanzar >80% de coverage** en tests (logrado: >85%)
- [x] **Código sin errores de flake8** (0 errores)
- [x] **Código formateado con black** (estilo consistente)
- [x] **Manejar errores con excepciones específicas** (ValueError, TypeError)
- [x] **Documentar todo el código** con docstrings completos
- [x] **Aplicar TDD consistentemente** (tests escritos primero)
- [x] **Funciones puras** sin efectos secundarios
- [x] **Logging profesional** implementado

**Estado:** ✅ **TODOS LOS CRITERIOS CUMPLIDOS**

---

## 🚀 Próximos Pasos

Una vez completado este módulo (✅ COMPLETADO), continúa con:

### **Módulo 2: Bases de Datos y SQL**
- Diseño de modelos relacionales
- SQL avanzado (JOINs, CTEs, Window Functions)
- Integración de Python con bases de datos
- NoSQL básico (MongoDB)
- ORMs (SQLAlchemy)

### Preparación recomendada:
1. Revisar todos los proyectos completados
2. Reforzar conceptos débiles si los hay
3. Practicar con ejercicios adicionales
4. Configurar entorno para SQL (PostgreSQL/MySQL)

---

## 📝 Notas Importantes

### Metodología de Trabajo

Este módulo siguió estrictamente:

✅ **TDD (Test-Driven Development)**
- Tests escritos ANTES del código
- Ciclo RED → GREEN → REFACTOR
- 143 tests unitarios como evidencia

✅ **Seguridad by Default**
- Validación exhaustiva de todos los inputs
- Manejo de excepciones específicas
- No confianza en datos externos

✅ **Código Limpio**
- Funciones simples y puras
- Sin efectos secundarios
- Nombres descriptivos
- Máximo 50 líneas por función

✅ **Documentación Profesional**
- Docstrings completos en todas las funciones
- Ejemplos de uso en docstrings
- README en cada proyecto
- Comentarios solo cuando necesario

### Ejemplos Basados en Casos Reales

Los proyectos incluyen ejemplos de:
- **DataBite**: Sistema de ventas de restaurantes
- **CloudMetrics**: Sistema de gestión empresarial
- **APIs**: Análisis de tiempos de respuesta
- **Logs**: Sistemas de producción
- **CSV**: Datos de ventas y clientes

Estos ejemplos facilitan la comprensión de aplicaciones prácticas reales.

---

## 🏆 Logros del Módulo

- ✅ **143 tests unitarios** escritos y pasando
- ✅ **6 funciones estadísticas** implementadas
- ✅ **5 módulos de procesamiento CSV** completados
- ✅ **Sistema de logging** profesional funcional
- ✅ **Coverage promedio >85%** en todos los proyectos
- ✅ **0 errores de linting** (flake8)
- ✅ **100% código formateado** (black)
- ✅ **Type hints completos** en todo el código
- ✅ **3 revisiones pedagógicas** aprobadas

**¡Felicidades por completar el Módulo 1!** 🎉

---

**Última actualización:** 2025-11-10
**Versión del módulo:** 1.0.0 (COMPLETADO)
