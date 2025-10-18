# Módulo 1: Fundamentos de Programación y Herramientas

## Información del Módulo

- **Duración:** 8-10 semanas
- **Nivel:** Principiante
- **Estado:** En progreso (1/3 proyectos completados)

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Escribir programas en Python con sintaxis correcta y estilo limpio
- ✅ Utilizar tipado explícito para mejor documentación y detección de errores
- ✅ Aplicar TDD (Test-Driven Development) escribiendo tests antes del código
- ✅ Validar inputs de manera robusta para garantizar seguridad
- ✅ Manejar errores con excepciones específicas
- ✅ Formatear código con black y validar con flake8
- 🔄 Utilizar Git y GitHub para control de versiones (en progreso)
- 🔄 Configurar entornos virtuales profesionales
- ⏳ Escribir funciones puras sin efectos secundarios
- ⏳ Implementar logging profesional

**Leyenda:** ✅ Completado | 🔄 En progreso | ⏳ Pendiente

## Proyectos del Módulo

### 1. ✅ Calculadora de Estadísticas Básicas (COMPLETADO)

**Duración:** 1 semana  
**Estado:** ✅ Completado el 2025-10-18

**Descripción:**  
Implementación de funciones estadísticas básicas aplicando TDD, tipado explícito y validación robusta.

**Funciones implementadas:**
- `calcular_media()` - Media aritmética
- `calcular_mediana()` - Mediana (robusto ante outliers)
- `calcular_moda()` - Moda con soporte multimodal
- `calcular_varianza()` - Varianza poblacional
- `calcular_desviacion_estandar()` - Desviación estándar
- `calcular_percentiles()` - Percentiles con interpolación

**Métricas de calidad:**
- 51 tests unitarios (100% pasando)
- Coverage: 89%
- 0 errores de flake8
- Código formateado con black
- Docstrings completos

**Conceptos aprendidos:**
- Test-Driven Development (TDD)
- Tipado explícito con type hints
- Validación exhaustiva de inputs
- Manejo de excepciones específicas
- Funciones puras sin efectos secundarios
- Documentación profesional con docstrings
- Ejemplos reales de uso (Yurest/Agora)

**Ir al proyecto:** [`proyecto-1-estadisticas/`](./proyecto-1-estadisticas/)

---

### 2. ⏳ Procesador de Archivos CSV (PENDIENTE)

**Duración estimada:** 1-2 semanas  
**Estado:** ⏳ Por comenzar

**Descripción:**  
Leer, validar y transformar archivos CSV con manejo robusto de errores.

**Funcionalidades planeadas:**
- Leer archivos CSV con diferentes delimitadores
- Validar estructura y tipos de datos
- Limpiar datos (duplicados, valores nulos)
- Transformar datos (formatos, normalización)
- Logging profesional con diferentes niveles
- Tests con archivos fixture

**Conceptos a aprender:**
- Manejo de archivos con `pathlib.Path`
- Módulo `csv` de Python
- Logging profesional
- Validación de esquemas
- Transformaciones de datos
- Tests con fixtures

---

### 3. ⏳ Sistema de Logs Configurable (PENDIENTE)

**Duración estimada:** 1 semana  
**Estado:** ⏳ Por comenzar

**Descripción:**  
Implementar un sistema de logging profesional y configurable.

**Funcionalidades planeadas:**
- Logger singleton
- Niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Múltiples outputs (consola, archivo)
- Rotación de archivos
- Logs estructurados (JSON)
- Decoradores para logging automático

**Conceptos a aprender:**
- Módulo `logging` de Python
- Patrones de diseño (Singleton)
- Configuración desde archivos
- Decoradores
- Context managers

---

## Progreso del Módulo

```
Proyecto 1: ████████████████████ 100% ✅ Completado
Proyecto 2: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
Proyecto 3: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
─────────────────────────────────────────────────
Total:      ██████░░░░░░░░░░░░░░  33% 🔄 En progreso
```

## Herramientas Utilizadas

- ✅ **Python 3.13+** - Lenguaje de programación
- ✅ **pytest** - Framework de testing
- ✅ **black** - Formateador de código
- ✅ **flake8** - Linter para validación de estilo
- ✅ **mypy** - Type checking estático
- 🔄 **Git** - Control de versiones
- ⏳ **venv** - Entornos virtuales

## Recursos de Aprendizaje

### Libros recomendados
- "Python Crash Course" - Eric Matthes
- "Clean Code in Python" - Mariano Anaya

### Cursos online
- Real Python - Python Basics
- DataCamp - Introduction to Python

### Documentación
- [Python Official Docs](https://docs.python.org/3/)
- [pytest Documentation](https://docs.pytest.org/)
- [black Documentation](https://black.readthedocs.io/)

## Criterios de Evaluación del Módulo

Para considerar este módulo completado, debes:

- [ ] Completar los 3 proyectos prácticos
- [x] Escribir código con tipado explícito
- [x] Alcanzar >80% de coverage en tests
- [x] Código sin errores de flake8
- [x] Código formateado con black
- [x] Manejar errores con excepciones específicas
- [ ] Usar Git con commits descriptivos
- [ ] Documentar todo el código con docstrings
- [ ] Aplicar TDD consistentemente

## Próximo Paso

Una vez completado este módulo, continuarás con:

**Módulo 2: Bases de Datos y SQL**
- Diseño de modelos relacionales
- SQL avanzado (JOINs, CTEs, Window Functions)
- Integración de Python con bases de datos
- NoSQL básico

---

## Notas

### Metodología de Trabajo

Este módulo sigue estrictamente:
- **TDD**: Tests se escriben ANTES del código
- **Seguridad**: Validación exhaustiva de todos los inputs
- **Código limpio**: Funciones simples, sin efectos secundarios
- **Documentación**: Docstrings completos con ejemplos

### Ejemplos Reales

Los proyectos incluyen ejemplos basados en casos de uso reales:
- **Yurest**: Sistema de ventas de restaurantes
- **Agora**: Sistema de gestión empresarial
- **SLAs**: Medición de tiempos de respuesta de APIs

Estos ejemplos ayudan a entender la aplicación práctica de los conceptos.

---

**Última actualización:** 2025-10-18

