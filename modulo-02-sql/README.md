# Módulo 2: SQL Básico e Intermedio

## Información del Módulo

- **Duración:** 8-10 semanas
- **Nivel:** Principiante a Intermedio
- **Estado:** En progreso (2/3 temas completados)

## Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ⏳ Diseñar modelos de datos relacionales normalizados
- ⏳ Escribir consultas SQL complejas con JOINs, subconsultas y CTEs
- ⏳ Crear y optimizar índices para mejorar performance
- ⏳ Conectar aplicaciones Python con bases de datos
- ⏳ Implementar transacciones y garantizar integridad de datos
- ⏳ Trabajar con bases de datos NoSQL básicas

**Leyenda:** ✅ Completado | 🔄 En progreso | ⏳ Pendiente

## Temas del Módulo

### Tema 1: SQL Básico ✅

**Duración estimada:** 2-3 semanas
**Estado:** ✅ Completado (2025-10-23)

**Descripción:**
Introducción a SQL desde cero. Aprenderás a consultar datos, filtrar, ordenar y realizar análisis básicos con funciones agregadas.

**Contenido:**
- SELECT, WHERE, ORDER BY, LIMIT
- Funciones agregadas (COUNT, SUM, AVG, MAX, MIN)
- GROUP BY y HAVING
- Análisis exploratorio de datos

**Proyecto práctico:**
Análisis exploratorio de base de datos de e-commerce

**Ir al tema:** [`tema-1-sql-basico/`](./tema-1-sql-basico/)

---

### Tema 2: SQL Intermedio ✅

**Duración estimada:** 3-4 semanas
**Estado:** ✅ Completado (2025-10-25)
**Calificación pedagógica:** 9.5/10 ⭐⭐⭐⭐⭐

**Descripción:**
SQL avanzado para combinar datos de múltiples tablas y realizar consultas complejas con JOINs, subconsultas y CASE WHEN.

**Contenido:**
- JOINs (INNER, LEFT, RIGHT, FULL OUTER, CROSS)
- Subconsultas en WHERE, FROM y SELECT
- CASE WHEN para lógica condicional
- Validación de resultados de JOINs
- Detección de productos cartesianos

**Proyecto práctico:**
Sistema de análisis de JOINs con 4 módulos funcionales, 58 tests y 85% de cobertura. Incluye validadores, detectores de tipo de JOIN y generadores de reportes complejos.

**Empresa ficticia:** TechStore (e-commerce de electrónica)

**Ir al tema:** [`tema-2-sql-intermedio/`](./tema-2-sql-intermedio/)

---

### Tema 3: Optimización SQL ⏳

**Duración estimada:** 2-3 semanas
**Estado:** ⏳ Por comenzar

**Descripción:**
Aprende a optimizar queries para mejorar el performance de tus aplicaciones.

**Contenido:**
- Índices (cuándo y cómo usarlos)
- EXPLAIN ANALYZE
- Buenas prácticas de SQL
- Optimización de queries lentas

**Proyecto práctico:**
Optimizar queries lentas en base de datos de producción

---

## Progreso del Módulo

```
Tema 1: ████████████████████ 100% ✅ Completado
Tema 2: ████████████████████ 100% ✅ Completado
Tema 3: ░░░░░░░░░░░░░░░░░░░░   0% ⏳ Pendiente
─────────────────────────────────────────────────
Total:  █████████████░░░░░░░  67% 🔄 En progreso
```

## Herramientas Utilizadas

- ⏳ **SQLite** - Base de datos ligera para proyectos locales
- ⏳ **PostgreSQL** - Base de datos relacional profesional
- ⏳ **DBeaver / pgAdmin** - Clientes GUI para bases de datos
- ⏳ **SQLAlchemy** - ORM de Python
- ⏳ **pytest** - Testing de queries

## Recursos de Aprendizaje

### Libros recomendados
- "SQL for Data Analysis" - Cathy Tanimura
- "Learning SQL" - Alan Beaulieu

### Cursos online
- Mode Analytics SQL Tutorial
- SQLZoo Interactive Tutorial
- LeetCode SQL Problems

### Documentación
- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Criterios de Evaluación del Módulo

Para considerar este módulo completado, debes:

- [ ] Completar los 3 temas con sus proyectos prácticos
- [ ] Escribir queries SQL correctas y optimizadas
- [ ] Entender cuándo usar cada tipo de JOIN
- [ ] Saber optimizar queries lentas con índices
- [ ] Conectar Python con bases de datos usando SQLAlchemy
- [ ] Prevenir SQL injection en aplicaciones
- [ ] Manejar transacciones correctamente

## Contexto Empresarial

En este módulo trabajarás con datos de **TechStore**, una tienda de electrónica ficticia que necesita analizar sus ventas, productos y clientes.

**Empresa ficticia:** TechStore
**Sector:** E-commerce de electrónica
**Datos:** Productos, ventas, clientes, categorías, pedidos

Todos los ejemplos y ejercicios usarán datos realistas pero ficticios de esta empresa.

## Próximo Paso

Una vez completado este módulo, continuarás con:

**Módulo 3: Ingeniería de Datos Core (ETL/ELT)**
- Pipelines de datos
- Pandas avanzado
- Calidad de datos
- Formatos modernos (Parquet, Avro)

---

## Notas

### Metodología de Trabajo

Este módulo sigue:
- **Progresión lógica**: De consultas simples a complejas
- **Ejemplos reales**: Casos de uso empresariales
- **Práctica constante**: Ejercicios en cada tema
- **Proyectos aplicados**: Implementaciones reales

### Base de Datos

- **SQLite** para proyectos locales (no requiere instalación)
- **PostgreSQL** para ejemplos avanzados (Docker disponible)
- Scripts SQL incluidos para crear tablas de ejemplo

### Empresas Ficticias

Usamos empresas ficticias para mantener ejemplos realistas:
- **TechStore**: E-commerce de electrónica (principal en este módulo)
- **RestaurantData Co.**: Red de restaurantes
- **CloudAPI Systems**: Proveedor de APIs

Ver lista completa en: `documentacion/juego/EMPRESAS_FICTICIAS.md`

---

**Última actualización:** 2025-10-23
