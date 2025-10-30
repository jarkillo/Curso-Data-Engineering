# Tema 1: SQL Básico

**Duración estimada**: 2-3 semanas
**Nivel**: Principiante
**Estado**: ✅ **COMPLETADO** (2025-10-23)

---

## 📋 Descripción

Introducción a SQL desde cero. Aprenderás a consultar datos, filtrar, ordenar y realizar análisis básicos con funciones agregadas. Este tema está diseñado para personas sin conocimientos previos de SQL.

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

- ✅ Escribir consultas SQL básicas con `SELECT`, `FROM`, `WHERE`
- ✅ Ordenar y limitar resultados con `ORDER BY` y `LIMIT`
- ✅ Usar funciones de agregación (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`)
- ✅ Agrupar datos con `GROUP BY` y filtrar grupos con `HAVING`
- ✅ Conectar Python con bases de datos SQLite
- ✅ Prevenir SQL injection con queries parametrizadas
- ✅ Implementar funciones Python para análisis de datos SQL

---

## 📚 Contenido del Tema

### 1. Teoría (01-TEORIA.md)

**Duración**: 30-45 minutos de lectura
**Palabras**: ~4,000

**Contenido**:
- Introducción a SQL y bases de datos relacionales
- Analogía: Base de datos como biblioteca
- 7 conceptos fundamentales:
  1. `SELECT` y `FROM` - Pedir datos
  2. `WHERE` - Filtrar filas
  3. `ORDER BY` - Ordenar resultados
  4. `LIMIT` - Limitar resultados
  5. Funciones agregadas - Análisis numérico
  6. `GROUP BY` - Agrupar datos
  7. `HAVING` - Filtrar grupos
- Aplicaciones prácticas en Data Engineering
- Errores comunes y cómo evitarlos
- Buenas prácticas de SQL
- Checklist de aprendizaje

**Características pedagógicas**:
- ✅ Explicaciones desde cero (sin asumir conocimientos previos)
- ✅ Analogías efectivas y memorables
- ✅ Contexto empresarial realista
- ✅ Progresión lógica de conceptos

---

### 2. Ejemplos (02-EJEMPLOS.md)

**Duración**: 45-60 minutos de lectura
**Ejemplos**: 5 trabajados paso a paso

**Contenido**:
- Scripts SQL para crear base de datos de ejemplo (TechStore)
- **Ejemplo 1**: Consultas básicas y filtrado (Nivel: Básico)
- **Ejemplo 2**: Funciones agregadas (Nivel: Básico)
- **Ejemplo 3**: `GROUP BY` y `HAVING` (Nivel: Intermedio)
- **Ejemplo 4**: Análisis de ventas (Nivel: Intermedio)
- **Ejemplo 5**: Dashboard de métricas ejecutivas (Nivel: Avanzado)

**Características**:
- ✅ Contexto empresarial (TechStore, tienda de tecnología)
- ✅ Pasos detallados con explicaciones
- ✅ Código SQL completo y ejecutable
- ✅ Interpretación de resultados
- ✅ Decisiones de negocio basadas en datos

---

### 3. Ejercicios (03-EJERCICIOS.md)

**Duración**: 2-4 horas de práctica
**Ejercicios**: 15 con soluciones completas

**Contenido**:
- **5 ejercicios básicos (⭐)**: `SELECT`, `WHERE`, funciones simples
- **5 ejercicios intermedios (⭐⭐)**: `GROUP BY`, `HAVING`, análisis
- **5 ejercicios avanzados (⭐⭐⭐)**: Queries complejas, dashboards

**Características**:
- ✅ Dificultad progresiva
- ✅ Contextos empresariales variados (e-commerce, streaming, fitness, logística, educación)
- ✅ Soluciones completas con explicaciones paso a paso
- ✅ Tabla de autoevaluación
- ✅ Consejos para mejorar

---

### 4. Proyecto Práctico (04-proyecto-practico/)

**Duración**: 4-6 horas de implementación
**Nivel**: Intermedio
**Estado**: ✅ **COMPLETADO CON CALIDAD EXCELENTE**

**Descripción**:
Implementación de funciones Python para interactuar con una base de datos SQLite, aplicando los conceptos de SQL básico aprendidos en la teoría.

**Estructura del proyecto**:
```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── conexion_db.py          # Clase ConexionSQLite con context manager
│   ├── validaciones.py         # Funciones de validación de inputs
│   ├── consultas_basicas.py    # SELECT, WHERE, ORDER BY, LIMIT
│   ├── consultas_agregadas.py  # COUNT, SUM, AVG, MAX, MIN
│   └── consultas_agrupadas.py  # GROUP BY, HAVING
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures compartidas (DB en memoria)
│   ├── test_conexion_db.py     # 12 tests
│   ├── test_validaciones.py    # 18 tests
│   ├── test_consultas_basicas.py    # 20 tests
│   ├── test_consultas_agregadas.py  # 8 tests
│   └── test_consultas_agrupadas.py  # 12 tests
├── README.md                   # Guía de uso del proyecto
├── ARQUITECTURA.md             # Diseño detallado
├── RESUMEN_DESARROLLO.md       # Proceso TDD
├── REPORTE_CALIDAD_FINAL.md    # Métricas de calidad
├── requirements.txt            # Dependencias
└── .gitignore                  # Archivos a ignorar
```

**Funciones implementadas** (16 funciones):
1. **Validaciones** (4 funciones):
   - `validar_precio_positivo()`
   - `validar_categoria_no_vacia()`
   - `validar_numero_positivo()`
   - `validar_ruta_db_existe()`

2. **Consultas básicas** (4 funciones):
   - `obtener_todos_los_productos()`
   - `filtrar_productos_por_categoria()`
   - `obtener_productos_caros()`
   - `obtener_top_n_productos_mas_caros()`

3. **Consultas agregadas** (4 funciones):
   - `contar_productos()`
   - `calcular_precio_promedio()`
   - `obtener_estadisticas_precios()`
   - `calcular_ingresos_totales()`

4. **Consultas agrupadas** (4 funciones):
   - `contar_productos_por_categoria()`
   - `calcular_valor_inventario_por_categoria()`
   - `obtener_categorias_con_mas_de_n_productos()`
   - `analizar_ventas_por_producto()`

**Características técnicas**:
- ✅ **TDD estricto**: Tests escritos primero (Red-Green-Refactor)
- ✅ **Arquitectura funcional**: Sin clases innecesarias
- ✅ **Tipado explícito**: Type hints en todas las funciones
- ✅ **Docstrings completos**: Documentación clara y ejemplos
- ✅ **Prevención de SQL injection**: Queries parametrizadas
- ✅ **Context manager**: Gestión automática de conexiones
- ✅ **Funciones puras**: Sin efectos colaterales
- ✅ **Código limpio**: <50 líneas por función

**Métricas de calidad**:
- ✅ **pytest**: 69/69 tests pasados (100%)
- ✅ **Cobertura**: 96% (objetivo: >80%)
- ✅ **black**: Código formateado correctamente
- ✅ **flake8**: 0 errores de linting
- ✅ **Tiempo de tests**: 0.31s (muy rápido)

**Base de datos**:
- SQLite (no requiere Docker)
- 10 productos de TechStore
- 10 ventas de octubre 2025
- Datos realistas pero ficticios

**Beneficios pedagógicos**:
- ✅ Los estudiantes practican SQL desde Python
- ✅ Aprenden a prevenir SQL injection
- ✅ Ven TDD en acción (tests primero)
- ✅ Código de calidad profesional como ejemplo
- ✅ Funciones reutilizables y composables

---

## 🎓 Revisión Pedagógica

**Archivo**: `REVISION_PEDAGOGICA.md`
**Estado**: ✅ **APROBADO PARA PRODUCCIÓN**
**Calificación**: **9.3/10** ⭐⭐⭐⭐⭐

**Fortalezas identificadas**:
1. ✅ Progresión pedagógica impecable
2. ✅ Analogías efectivas y memorables
3. ✅ Contexto empresarial realista
4. ✅ Ejercicios bien diseñados con dificultad progresiva
5. ✅ Cumple con todos los estándares pedagógicos (Bloom, ZDP, Ausubel)

**Áreas de mejora sugeridas** (no bloqueantes):
1. Agregar diagramas visuales para `GROUP BY`
2. Agregar tabla resumen "Cuándo usar qué"
3. Agregar ejercicios de debugging
4. Agregar sección FAQ

---

## 📊 Progreso del Tema

```
Teoría:           ████████████████████ 100% ✅ Completado
Ejemplos:         ████████████████████ 100% ✅ Completado
Ejercicios:       ████████████████████ 100% ✅ Completado
Proyecto:         ████████████████████ 100% ✅ Completado
Revisión:         ████████████████████ 100% ✅ Aprobado
─────────────────────────────────────────────────────────
Total:            ████████████████████ 100% ✅ Completado
```

---

## 🛠️ Herramientas Utilizadas

- ✅ **Python 3.13+** - Lenguaje de programación
- ✅ **SQLite** - Base de datos ligera
- ✅ **pytest** - Framework de testing
- ✅ **pytest-cov** - Cobertura de tests
- ✅ **black** - Formateador de código
- ✅ **flake8** - Linter para validación de estilo

---

## 📖 Cómo Usar Este Tema

### Ruta de Aprendizaje Recomendada

1. **Leer la teoría** (01-TEORIA.md) - 30-45 min
   - Lee con calma, toma notas
   - Usa el checklist de aprendizaje al final

2. **Estudiar los ejemplos** (02-EJEMPLOS.md) - 45-60 min
   - Ejecuta los scripts SQL en tu entorno
   - Intenta modificar las queries y ver qué pasa

3. **Practicar con ejercicios** (03-EJERCICIOS.md) - 2-4 horas
   - Intenta resolver sin ver las soluciones
   - Compara tus soluciones con las proporcionadas
   - Usa la tabla de autoevaluación

4. **Implementar el proyecto práctico** (04-proyecto-practico/) - 4-6 horas
   - Instala las dependencias
   - Lee el README y ARQUITECTURA
   - Ejecuta los tests y estudia el código
   - Intenta crear tus propias funciones

---

## 🎯 Criterios de Completitud

Has completado este tema cuando puedas:

- ✅ Escribir queries SQL básicas sin ayuda
- ✅ Usar funciones de agregación correctamente
- ✅ Agrupar datos con `GROUP BY` y filtrar con `HAVING`
- ✅ Conectar Python con SQLite
- ✅ Implementar funciones Python que ejecuten queries SQL
- ✅ Prevenir SQL injection con queries parametrizadas
- ✅ Escribir tests para funciones que interactúan con bases de datos

---

## 📝 Próximos Pasos

Después de completar este tema, estarás listo para:

1. **Tema 2: SQL Intermedio**
   - JOINs (INNER, LEFT, RIGHT, FULL)
   - Subconsultas y CTEs
   - Funciones de ventana (ROW_NUMBER, RANK, LAG, LEAD)

2. **Tema 3: Optimización SQL**
   - Índices y su impacto
   - Análisis de planes de ejecución (`EXPLAIN ANALYZE`)
   - Buenas prácticas de optimización

---

## 🤝 Contribuciones

Si encuentras errores, tienes sugerencias o quieres agregar más ejemplos/ejercicios, por favor:

1. Abre un issue en el repositorio
2. Propón cambios mediante pull request
3. Sigue las reglas del proyecto (TDD, arquitectura limpia, etc.)

---

## 📚 Recursos Adicionales

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQL Tutorial - W3Schools](https://www.w3schools.com/sql/)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [SQL for Data Analysis - Mode Analytics](https://mode.com/sql-tutorial/)

---

**Fecha de completitud**: 2025-10-23
**Última actualización**: 2025-10-23
**Estado**: ✅ **COMPLETADO Y APROBADO**


