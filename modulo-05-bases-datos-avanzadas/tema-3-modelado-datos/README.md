# Tema 3: Modelado de Datos

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

- Aplicar técnicas de normalización (1NF, 2NF, 3NF, BCNF)
- Diseñar diagramas Entidad-Relación (ER)
- Modelar esquemas dimensionales (Star Schema, Snowflake)
- Distinguir entre OLTP y OLAP
- Decidir cuándo normalizar vs desnormalizar
- Diseñar data warehouses eficientes
- Tomar decisiones informadas sobre modelado

## 📚 Contenido

### [01-TEORIA.md](./01-TEORIA.md)
**Duración:** 30-45 minutos

Conceptos fundamentales de modelado de datos para Data Engineering.

**Temas cubiertos:**
- Normalización (1NF, 2NF, 3NF, BCNF)
- Diagramas Entidad-Relación
- Star Schema y Snowflake Schema
- OLTP vs OLAP
- Cuándo desnormalizar
- Slowly Changing Dimensions (SCD)

### [02-EJEMPLOS.md](./02-EJEMPLOS.md)
**Duración:** 45-60 minutos

4 ejemplos trabajados de modelado con diagramas.

**Ejemplos incluidos:**
1. Normalizar base de datos de e-commerce
2. Diseñar diagrama ER para sistema de cursos
3. Modelar Star Schema para ventas
4. Implementar SCD Type 2

### [03-EJERCICIOS.md](./03-EJERCICIOS.md)
**Duración:** 2-3 horas

12 ejercicios de diseño con soluciones.

**Distribución:**
- 5 ejercicios básicos ⭐
- 4 ejercicios intermedios ⭐⭐
- 3 ejercicios avanzados ⭐⭐⭐

### [04-proyecto-practico/](./04-proyecto-practico/)
**Duración:** 4-6 horas

Proyecto completo: Diseño de Data Warehouse dimensional.

**Entregables:**
- Diagramas ER en formato visual
- Star Schema para analytics
- Scripts DDL para crear tablas
- Queries analíticas de ejemplo
- Documentación de decisiones de diseño

## 🚀 Cómo Estudiar Este Tema

### Paso 1: Preparar herramientas (10 min)
```bash
# Para diagramas, puedes usar:
# - draw.io (online, gratuito)
# - Lucidchart (online, freemium)
# - dbdiagram.io (online, especializado en BD)
# - Papel y lápiz (¡funciona!)

# Para SQL
docker-compose up -d postgres
```

### Paso 2: Leer teoría (30-45 min)
- Lee `01-TEORIA.md` completo
- Dibuja los diagramas mientras lees
- Entiende el POR QUÉ de cada técnica

### Paso 3: Estudiar ejemplos (45-60 min)
- Abre `02-EJEMPLOS.md`
- **Dibuja tú mismo** los diagramas antes de ver la solución
- Compara tu diseño con el propuesto
- Entiende las decisiones de diseño

### Paso 4: Resolver ejercicios (2-3 horas)
- Cada ejercicio requiere diseñar, no solo programar
- Usa papel, pizarra o herramienta digital
- No hay una sola solución correcta
- Compara tu solución con la propuesta

### Paso 5: Proyecto práctico (4-6 horas)
```bash
cd 04-proyecto-practico

# Crear diagramas (carpeta diagramas/)
# Escribir scripts DDL (carpeta scripts/)
# Documentar decisiones (README.md)
```

## 📊 Checklist de Progreso

- [ ] Herramientas de diagramado preparadas
- [ ] 01-TEORIA.md leído y comprendido
- [ ] Diferencia entre OLTP y OLAP clara
- [ ] 02-EJEMPLOS.md estudiado
- [ ] Ejercicios 1-5 (básicos) resueltos
- [ ] Ejercicios 6-9 (intermedios) resueltos
- [ ] Ejercicios 10-12 (avanzados) resueltos
- [ ] Proyecto práctico completado
- [ ] Diagramas creados y documentados

## 🔧 Requisitos Técnicos

### Software
- Herramienta de diagramado (draw.io, Lucidchart, etc.)
- PostgreSQL (para implementar diseños)
- Editor de texto

### Conocimientos Previos
- SQL básico
- Concepto de tablas y relaciones
- Conceptos básicos de bases de datos

## 💡 Tips para el Éxito

1. **Dibuja siempre**: El modelado es visual
2. **Piensa en el usuario final**: ¿Qué preguntas responderá?
3. **Itera**: El primer diseño raramente es perfecto
4. **Documenta**: Explica POR QUÉ tomaste cada decisión
5. **No sobre-normalices**: A veces desnormalizar está bien

## 🆘 Ayuda y Recursos

### Herramientas Recomendadas

**Diagramado:**
- [draw.io](https://app.diagrams.net/) - Gratis, potente
- [dbdiagram.io](https://dbdiagram.io/) - Especializado en BD
- [Lucidchart](https://www.lucidchart.com/) - Profesional

**Generación de DDL:**
- [QuickDBD](https://www.quickdatabasediagrams.com/)
- [SQLDBm](https://sqldbm.com/)

### Documentación y Guías
- [Database Design Tutorial](https://www.lucidchart.com/pages/database-diagram/database-design)
- [Star Schema vs Snowflake](https://www.holistics.io/blog/star-schema-vs-snowflake-schema/)
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

### Libros Recomendados
- "The Data Warehouse Toolkit" - Ralph Kimball ⭐⭐⭐⭐⭐
- "Database Design for Mere Mortals" - Michael J. Hernandez
- "Designing Data-Intensive Applications" - Martin Kleppmann

## ⚠️ Errores Comunes

### 1. Sobre-normalizar (OLTP cuando necesitas OLAP)
```
❌ MAL: 7 tablas relacionadas con 5 JOINs para un reporte simple
✅ BIEN: Star Schema desnormalizado optimizado para queries
```

### 2. No documentar decisiones
```
❌ MAL: Solo el diagrama, sin explicaciones
✅ BIEN: Diagrama + documento de decisiones arquitectónicas
```

### 3. Ignorar el volumen de datos
```
❌ MAL: Diseño que funciona con 1000 filas pero no con 1M
✅ BIEN: Considerar escalabilidad desde el inicio
```

### 4. No considerar las queries
```
❌ MAL: Diseñar sin saber qué preguntas se responderán
✅ BIEN: Primero las queries, luego el modelo
```

## 📐 Notación de Diagramas

### Entidad-Relación (ER)
```
┌─────────────┐
│   Usuario   │
├─────────────┤
│ id (PK)     │
│ nombre      │
│ email       │
└─────────────┘
      │
      │ 1:N
      ▼
┌─────────────┐
│   Orden     │
├─────────────┤
│ id (PK)     │
│ usuario_id (FK)│
│ fecha       │
└─────────────┘
```

### Cardinalidad
- **1:1** - Uno a uno
- **1:N** - Uno a muchos
- **N:M** - Muchos a muchos (requiere tabla intermedia)

### Símbolos comunes
- **(PK)** - Primary Key
- **(FK)** - Foreign Key
- **NOT NULL** - Campo obligatorio
- **UNIQUE** - Valor único

## 🎯 Checklist de Diseño

Antes de finalizar un diseño, verifica:

### Normalización (OLTP)
- [ ] ¿Está en 3NF mínimo?
- [ ] ¿Todas las PKs están definidas?
- [ ] ¿Todas las FKs son correctas?
- [ ] ¿No hay dependencias transitivas?
- [ ] ¿Los tipos de datos son apropiados?

### Dimensional (OLAP)
- [ ] ¿Tabla de hechos claramente identificada?
- [ ] ¿Dimensiones correctamente separadas?
- [ ] ¿Granularidad definida?
- [ ] ¿Métricas son aditivas?
- [ ] ¿Performance considerado?

### General
- [ ] ¿Nombres consistentes y descriptivos?
- [ ] ¿Índices necesarios identificados?
- [ ] ¿Decisiones documentadas?
- [ ] ¿Escalabilidad considerada?

---

**Volver:** [← README del Módulo](../README.md)

**Última actualización:** 2025-10-25
