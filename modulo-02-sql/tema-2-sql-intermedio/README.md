# Tema 2: SQL Intermedio (JOINs, Subconsultas)

## Descripción

Este tema cubre conceptos intermedios de SQL esenciales para Data Engineering: combinación de tablas con diferentes tipos de JOINs, uso de subconsultas en diferentes contextos, y lógica condicional con CASE WHEN.

**Estado:** ✅ Completado
**Duración estimada:** 12-16 horas
**Nivel:** Intermedio

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. **Dominar JOINs**: Ejecutar INNER, LEFT, RIGHT, FULL OUTER y CROSS JOINs
2. **Usar subconsultas**: En WHERE, FROM y SELECT para queries complejas
3. **Aplicar CASE WHEN**: Implementar lógica condicional en SQL
4. **Validar resultados**: Detectar productos cartesianos y pérdida de datos
5. **Generar reportes**: Crear análisis complejos combinando múltiples tablas
6. **Optimizar queries**: Entender cuándo usar cada tipo de JOIN

---

## 📚 Contenido del Tema

### 1. 01-TEORIA.md (~4,200 palabras, 30-45 min)

**Conceptos cubiertos:**
- Introducción a JOINs (¿por qué existen?)
- INNER JOIN: Intersección de tablas
- LEFT JOIN: Todos de la izquierda
- RIGHT JOIN: Todos de la derecha
- FULL OUTER JOIN: Todos de ambos lados
- CROSS JOIN: Producto cartesiano
- Subconsultas en WHERE, FROM, SELECT
- CASE WHEN: Condicionales en SQL
- WHERE vs HAVING con JOINs
- 5 errores comunes y cómo evitarlos
- Buenas prácticas

**Características:**
- ✅ Analogías efectivas para cada concepto
- ✅ Ejemplos visuales (tablas de resultados)
- ✅ Explicaciones paso a paso
- ✅ Contexto de Data Engineering

### 2. 02-EJEMPLOS.md (5 ejemplos trabajados, 90-120 min)

**Ejemplos prácticos:**
1. **INNER JOIN básico** (productos + categorías) - Nivel: Básico ⭐
2. **LEFT JOIN con NULL** (clientes sin pedidos) - Nivel: Básico ⭐
3. **Subconsulta en HAVING** (top 10% clientes) - Nivel: Intermedio ⭐⭐
4. **CASE WHEN** (clasificación de stock) - Nivel: Intermedio ⭐⭐
5. **JOIN múltiple** (4 tablas, dashboard ejecutivo) - Nivel: Avanzado ⭐⭐⭐

**Contexto:** TechStore (e-commerce de electrónica)

**Cada ejemplo incluye:**
- Contexto empresarial claro
- Scripts SQL para crear tablas
- Query completa con comentarios
- Resultados esperados
- Interpretación de negocio
- Decisiones basadas en datos

### 3. 03-EJERCICIOS.md (15 ejercicios + soluciones, 4-6 horas)

**Distribución:**
- **Básicos (1-5)**: INNER JOIN, LEFT JOIN simples ⭐
- **Intermedios (6-10)**: Subconsultas, CASE WHEN, RIGHT JOIN ⭐⭐
- **Avanzados (11-15)**: Matriz BCG, cohortes, cross-selling, retención ⭐⭐⭐

**Características:**
- ✅ Sistema de ayuda (hints sin spoilers)
- ✅ Soluciones completas con explicaciones
- ✅ Tabla de autoevaluación
- ✅ Contextos empresariales variados

### 4. 04-proyecto-practico/ (TDD, 8-10 horas)

**Sistema de Análisis de JOINs SQL**

**Módulos implementados:**
- `ejecutor_joins.py`: Ejecuta queries con JOINs de forma segura
- `detector_tipo_join.py`: Sugiere qué JOIN usar según requerimiento
- `validador_joins.py`: Detecta productos cartesianos y pérdida de datos
- `generador_reportes.py`: Genera reportes complejos de negocio

**Métricas de calidad:**
- ✅ **58 tests** (100% pasando)
- ✅ **Cobertura: 85%** (superior al 80% objetivo)
- ✅ **Type hints 100%**
- ✅ **Docstrings completos** en español
- ✅ **0 errores flake8**
- ✅ **Formateado con black**
- ✅ **TDD estricto**: Red → Green → Refactor

**Funciones clave:**
- `ejecutar_join_simple()`: JOIN entre 2 tablas
- `ejecutar_join_multiple()`: JOIN de 3+ tablas
- `detectar_producto_cartesiano()`: Alerta de queries ineficientes
- `generar_reporte_ventas()`: Análisis con múltiples JOINs
- `generar_top_clientes()`: Segmentación con CASE WHEN

### 5. REVISION_PEDAGOGICA.md

**Calificación:** 9.5/10 ⭐⭐⭐⭐⭐

**Validación por Psicólogo Educativo:**
- ✅ Taxonomía de Bloom (6 niveles cognitivos)
- ✅ Zona de Desarrollo Próximo respetada
- ✅ Aprendizaje Significativo (conexión con conocimientos previos)
- ✅ Carga Cognitiva bien dosificada
- ✅ Progresión sin saltos conceptuales
- ✅ Analogías efectivas y memorables
- ✅ Feedback inmediato y metacognición
- ✅ Gamificación saludable

---

## 📊 Progreso

**Estado:** ✅ 100% Completado

```
Contenido Educativo:  ████████████████████ 100% ✅
Proyecto Práctico:    ████████████████████ 100% ✅
Tests:                ████████████████████ 100% ✅
Documentación:        ████████████████████ 100% ✅
Revisión Pedagógica:  ████████████████████ 100% ✅
```

---

## 🛠️ Herramientas Utilizadas

- **Python 3.10+**: Lenguaje principal
- **SQLite3**: Base de datos embebida
- **pytest**: Framework de testing (58 tests)
- **pytest-cov**: Cobertura de código (85%)
- **black**: Formateador de código
- **flake8**: Linter (0 errores)

---

## 🚀 Cómo Usar Este Tema

### Ruta de Aprendizaje Recomendada

1. **Día 1-2: Teoría y Ejemplos**
   - Lee `01-TEORIA.md` (~30-45 min)
   - Trabaja `02-EJEMPLOS.md` paso a paso (~90-120 min)
   - Ejecuta las queries en SQLite local

2. **Día 3-4: Práctica con Ejercicios**
   - Resuelve ejercicios básicos (1-5) (~2 horas)
   - Resuelve ejercicios intermedios (6-10) (~2 horas)
   - Desafíate con ejercicios avanzados (11-15) (~2 horas)

3. **Día 5-6: Proyecto Práctico**
   - Lee `04-proyecto-practico/README.md` y `ARQUITECTURA.md`
   - Explora los tests para entender requisitos
   - Ejecuta el proyecto y experimenta con las funciones
   - Modifica y extiende el código

4. **Revisión Final**
   - Completa el checklist de aprendizaje en `01-TEORIA.md`
   - Autoevalúa tu progreso en `03-EJERCICIOS.md`
   - Revisa conceptos difíciles

---

## ✅ Criterios de Completitud

Has completado este tema cuando:

- [x] Lees y comprendes toda la teoría (01-TEORIA.md)
- [x] Ejecutas todos los ejemplos exitosamente (02-EJEMPLOS.md)
- [x] Resuelves al menos 12 de 15 ejercicios correctamente (03-EJERCICIOS.md)
- [x] Entiendes la diferencia entre tipos de JOINs y cuándo usar cada uno
- [x] Puedes escribir subconsultas en WHERE, FROM y SELECT
- [x] Dominas CASE WHEN para lógica condicional
- [x] Ejecutas el proyecto práctico y entiendes el código
- [x] Puedes detectar productos cartesianos y pérdida de datos
- [x] Comprendes el orden de ejecución SQL (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT)

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [SQLite JOINs](https://www.sqlitetutorial.net/sqlite-join/)
- [PostgreSQL JOINs](https://www.postgresql.org/docs/current/tutorial-join.html)
- [W3Schools SQL JOIN](https://www.w3schools.com/sql/sql_join.asp)

### Visualización de JOINs
- [Visual JOIN Guide](https://joins.spathon.com/) - Diagramas interactivos
- [SQL Joins Explained](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins) - Diagramas de Venn

### Práctica Interactiva
- [SQLZoo JOINs Tutorial](https://sqlzoo.net/wiki/The_JOIN_operation)
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/sql-joins/)
- [LeetCode SQL Problems](https://leetcode.com/problemset/database/) - Filtra por "JOIN"

---

## 🎯 Próximos Pasos

Después de completar este tema, continúa con:

1. **Tema 3: Optimización SQL** (Índices, EXPLAIN, performance tuning)
2. **Módulo 3: Ingeniería de Datos** (Pipelines ETL, Airflow)
3. **Módulo 4: APIs y Web Scraping**

---

## 📈 Métricas del Tema

| Métrica                     | Valor        |
| --------------------------- | ------------ |
| **Palabras (teoría)**       | ~4,200       |
| **Ejemplos trabajados**     | 5            |
| **Ejercicios**              | 15           |
| **Tests**                   | 58           |
| **Cobertura de código**     | 85%          |
| **Funciones implementadas** | 12           |
| **Archivos creados**        | 20+          |
| **Calificación pedagógica** | 9.5/10 ⭐⭐⭐⭐⭐ |

---

## 🤝 Contribuciones

Si encuentras errores o tienes sugerencias de mejora:

1. Reporta el issue con descripción clara
2. Propón mejoras con ejemplos concretos
3. Sigue las guías de estilo del proyecto (black, flake8, TDD)

---

## 📄 Licencia

Este tema es parte del **Master en Ingeniería de Datos** y tiene fines educativos.

---

**Última actualización:** 2025-10-25
**Versión:** 1.0.0
**Autor:** Equipo Pedagógico Master Data Engineering
**Empresa ficticia:** TechStore (e-commerce de electrónica)

---

## 🎉 ¡Felicidades!

Has completado el Tema 2: SQL Intermedio. Ahora dominas JOINs, subconsultas y CASE WHEN como un profesional de Data Engineering.

**Siguiente tema:** Tema 3 - Optimización SQL (Índices, EXPLAIN, Query Performance)
