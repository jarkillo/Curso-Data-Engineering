# 🗺️ Orden de Implementación del Master - Roadmap

Este documento define el orden lógico y pedagógico para implementar todo el contenido del Master en Ingeniería de Datos con IA.

---

## 📊 Resumen de Prioridades

- **🔴 Prioridad 1 (URGENT)**: 8 issues - Módulo 1 completo + Guía setup
- **🟠 Prioridad 2 (HIGH)**: 9 issues - Módulos 2-10
- **🟡 Prioridad 3 (MEDIUM)**: 3 issues - Expansiones y certificación
- **🟢 Prioridad 4 (LOW)**: 1 issue - Mejoras estéticas

---

## 🎯 Fase 1: Fundamentos y Setup (Prioridad 1 - URGENT)

> **Objetivo**: Completar el Módulo 1 y permitir que los estudiantes puedan empezar.

### 1️⃣ JAR-200: Guía de Instalación y Setup Completa
- **Por qué primero**: Los estudiantes necesitan configurar su entorno antes de comenzar
- **Duración estimada**: 1-2 días
- **Archivos clave**:
  - `documentacion/GUIA_INSTALACION.md`
  - `scripts/setup_windows.ps1`
  - `scripts/setup_linux.sh`
  - `scripts/setup_mac.sh`
  - `docker-compose.yml`
- **Incluye**: Python, Git, Docker, PostgreSQL, MongoDB, Airflow, AWS/GCP, Spark

---

### 2️⃣ JAR-185: Módulo 1 - Tema 1 - Crear 03-EJERCICIOS.md
- **Por qué ahora**: Completar el Tema 1 (teoría y ejemplos ya están listos)
- **Duración estimada**: 4-6 horas
- **Archivos clave**:
  - `modulo-01-fundamentos/tema-1-python-estadistica/03-EJERCICIOS.md`
- **Contenido**: 10-15 ejercicios de estadística descriptiva con soluciones

---

### 3️⃣ JAR-180 a JAR-183: Juego Web - Misiones 2-5 del Módulo 1
- **Por qué ahora**: Reforzar el aprendizaje del Módulo 1 de forma interactiva
- **Duración estimada**: 2-3 días en total
- **Issues**:
  - **JAR-180**: Misión 2 - Calcular Mediana con Outliers (6-8h)
  - **JAR-181**: Misión 3 - Calcular Moda Bimodal (6-8h)
  - **JAR-182**: Misión 4 - Percentiles y Cuartiles (6-8h)
  - **JAR-183**: Misión 5 - Varianza y Desviación Estándar (6-8h)
- **Archivos clave**:
  - `game.html`
  - `README_JUEGO_WEB.md`
- **Incluye**: Explicaciones pedagógicas, visualizaciones, sistema de XP

---

### 4️⃣ JAR-186: Módulo 1 - Tema 2 - Procesamiento de Archivos CSV
- **Por qué ahora**: Continuar con el Módulo 1 de forma secuencial
- **Duración estimada**: 2-3 días
- **Estructura completa**:
  - `01-TEORIA.md`: CSV, encoding, delimitadores
  - `02-EJEMPLOS.md`: Casos reales
  - `03-EJERCICIOS.md`: Ejercicios prácticos
  - `04-proyecto-practico/`: Procesador CSV con tests (TDD)
- **Funciones**: `leer_csv`, `escribir_csv`, `validar_csv`, `transformar_csv`

---

### 5️⃣ JAR-187: Módulo 1 - Tema 3 - Sistema de Logs y Debugging
- **Por qué ahora**: Completar el Módulo 1
- **Duración estimada**: 2-3 días
- **Estructura completa**:
  - `01-TEORIA.md`: logging, niveles, handlers
  - `02-EJEMPLOS.md`: Casos reales de logging en ETL
  - `03-EJERCICIOS.md`: Ejercicios de debugging
  - `04-proyecto-practico/`: Logger reutilizable con rotación
- **Funciones**: Logger configurable, rotación automática, tests

---

## 🚀 Fase 2: Módulos Intermedios (Prioridad 2 - HIGH)

> **Objetivo**: Construir conocimientos avanzados de forma progresiva.

### 6️⃣ JAR-188: Módulo 2 - SQL Básico e Intermedio
- **Duración estimada**: 1-2 semanas
- **Temas**: SQL básico, JOINs, subconsultas, optimización
- **Proyectos**: Análisis exploratorio, queries complejas, optimización

---

### 7️⃣ JAR-189: Módulo 3 - Python para Data Engineering
- **Duración estimada**: 1-2 semanas
- **Temas**: Pandas, NumPy, procesamiento paralelo
- **Proyectos**: Análisis de ventas, procesamiento numérico, pipeline paralelo

---

### 8️⃣ ✅ JAR-190: Módulo 4 - APIs y Web Scraping (COMPLETADO 2025-10-25)
- **Duración real**: 2 semanas (2025-10-23 a 2025-10-25)
- **Temas completados**:
  - ✅ Tema 1: APIs REST (100%)
  - ✅ Tema 2: Web Scraping (100%)
  - ✅ Tema 3: Rate Limiting y Caching (100%)
- **Proyectos completados**:
  - ✅ Cliente HTTP robusto (98 tests, 100% cobertura)
  - ✅ Scraper completo (71 tests, 90% cobertura)
  - ✅ Scraper optimizado (41 tests, 88% cobertura)
- **Tests totales**: 210 tests (100% pasando)
- **Calificación pedagógica**: 9.3/10 ⭐⭐⭐⭐⭐

---

### 9️⃣ JAR-191: Módulo 5 - Bases de Datos Avanzadas
- **Duración estimada**: 1-2 semanas
- **Temas**: PostgreSQL avanzado, MongoDB, modelado de datos
- **Proyectos**: Base transaccional, sistema de logs NoSQL, data warehouse

---

### 🔟 JAR-192: Módulo 6 - Apache Airflow y Orquestación
- **Duración estimada**: 1-2 semanas
- **Temas**: Introducción Airflow, nivel intermedio, producción
- **Proyectos**: Pipeline ETL simple, pipeline complejo, pipeline productivo

---

### 1️⃣1️⃣ JAR-193: Módulo 7 - Cloud Computing (AWS/GCP)
- **Duración estimada**: 1-2 semanas
- **Temas**: AWS, GCP, Infraestructura como Código
- **Proyectos**: Pipeline serverless AWS, pipeline GCP, despliegue IaC

---

### 1️⃣2️⃣ JAR-194: Módulo 8 - Data Warehousing y Analytics
- **Duración estimada**: 1-2 semanas
- **Temas**: Dimensional modeling, dbt, analytics y BI
- **Proyectos**: Diseñar DWH, transformaciones dbt, dashboard analítico

---

### 1️⃣3️⃣ JAR-195: Módulo 9 - Spark y Big Data
- **Duración estimada**: 1-2 semanas
- **Temas**: Introducción Spark, optimización, streaming
- **Proyectos**: Procesamiento batch, queries optimizadas, pipeline real-time

---

### 1️⃣4️⃣ JAR-196: Módulo 10 - Machine Learning para Data Engineers
- **Duración estimada**: 1-2 semanas
- **Temas**: Feature engineering, pipelines ML, MLOps
- **Proyectos**: Pipeline de features, pipeline ML, deployment en producción

---

## 🎓 Fase 3: Proyectos Integradores (Prioridad 3 - MEDIUM)

> **Objetivo**: Consolidar conocimientos y ofrecer valor añadido.

### 1️⃣5️⃣ JAR-198: Integrar Misiones de Módulos 2-10 en el Juego
- **Duración estimada**: 2-3 semanas
- **Por qué ahora**: Una vez terminado el contenido teórico, gamificar todo
- **Incluye**:
  - Misiones SQL con editor integrado
  - Misiones Pandas con visualizador de DataFrames
  - Misiones API con simulador
  - Misiones de bases de datos
  - Sistema de desbloqueo progresivo
  - Logros por completar módulos

---

### 1️⃣6️⃣ JAR-199: Sistema de Evaluación y Certificación
- **Duración estimada**: 1 semana
- **Por qué ahora**: Los estudiantes han completado módulos y necesitan evaluación
- **Incluye**:
  - Exámenes por módulo (10-15 preguntas)
  - Sistema de puntuación
  - Certificado PDF
  - Dashboard de progreso

---

### 1️⃣7️⃣ JAR-197: Proyecto Final - Pipeline ETL Completo
- **Duración estimada**: 2-4 semanas
- **Por qué al final**: Integra TODOS los módulos
- **Incluye**:
  - Extracción de múltiples fuentes
  - Transformaciones complejas
  - Data warehouse dimensional
  - Orquestación con Airflow
  - Despliegue en cloud
  - Monitoreo y alertas
  - Tests (>80% cobertura)
  - Documentación completa

---

## 🎨 Fase 4: Polish y Mejoras (Prioridad 4 - LOW)

> **Objetivo**: Mejorar la experiencia del usuario (opcional).

### 1️⃣8️⃣ JAR-184: Mejoras UX del Juego - Sonidos y Animaciones
- **Duración estimada**: 2-3 días
- **Por qué al final**: Es estético, no afecta el aprendizaje
- **Incluye**:
  - Sonidos sutiles
  - Animación de confetti
  - Transiciones suaves
  - Partículas al ganar XP
  - Opción para desactivar sonidos

---

## 📈 Resumen Temporal Estimado

| Fase                     | Issues        | Duración Estimada  | Acumulado       |
| ------------------------ | ------------- | ------------------ | --------------- |
| **Fase 1: Fundamentos**  | 8 issues      | 2-3 semanas        | 2-3 semanas     |
| **Fase 2: Módulos 2-10** | 9 issues      | 9-18 semanas       | 11-21 semanas   |
| **Fase 3: Integradores** | 3 issues      | 5-8 semanas        | 16-29 semanas   |
| **Fase 4: Polish**       | 1 issue       | 2-3 días           | ~16-30 semanas  |
| **TOTAL**                | **21 issues** | **~16-30 semanas** | **4-7.5 meses** |

*Nota: Las duraciones asumen trabajo a tiempo completo (40h/semana). Para trabajo parcial (10-20h/semana), multiplicar por 2-4.*

---

## 🎯 Próximos Pasos Inmediatos

### Opción A: Seguir el orden estricto
1. **Empezar por JAR-200**: Guía de Instalación
2. Luego JAR-185: Ejercicios del Tema 1
3. Continuar secuencialmente

### Opción B: Priorizar el juego (más motivador)
1. **Empezar por JAR-180-183**: Completar todas las misiones del Módulo 1
2. Luego JAR-185: Ejercicios
3. Luego JAR-186-187: Temas 2 y 3

### Opción C: Contenido teórico primero
1. **Empezar por JAR-185**: Ejercicios Tema 1
2. Luego JAR-186-187: Temas 2 y 3 completos
3. Luego JAR-180-183: Juego para reforzar

---

## 🤖 Workflows de Sub-Agentes

Cada issue en Linear incluye ahora una sección **"🤖 Workflow de Comandos"** que especifica el orden exacto de sub-agentes a invocar para completarla.

### Cómo Usar los Workflows

Los workflows están diseñados para usarse con el sistema de sub-agentes del proyecto:
- **En Cursor**: Usa los comandos en `.cursor/commands/` (ej: `@teaching`, `@development`, `@game-design`)
- **En Claude Code**: Usa los agentes en `.claude/agents/` (ej: `pedagogo.md`, `desarrollador-tdd.md`)

### Tipos de Workflows

#### Workflow Tipo 1: Contenido Teórico (Módulos)
```
@project-management → @teaching [pedagogo] → @teaching [profesor] →
@teaching [psicólogo] → @development [arquitecto] → @development [tdd] →
@quality → @documentation → @project-management
```
**Aplica a**: JAR-185, JAR-186, JAR-187, JAR-188-196

#### Workflow Tipo 2: Misiones del Juego
```
@project-management → @game-design [diseñador] → @teaching [pedagogo] →
@game-design [frontend] → @game-design [ux] → @quality →
@documentation → @project-management
```
**Aplica a**: JAR-180, JAR-181, JAR-182, JAR-183

#### Workflow Tipo 3: Infraestructura/Setup
```
@project-management → @infrastructure → @infrastructure →
@quality → @documentation → @project-management
```
**Aplica a**: JAR-200

#### Workflow Tipo 4: Expansiones del Juego
```
@project-management → @game-design [diseñador] → @game-design [frontend] →
@game-design [ux] → @quality → @documentation → @project-management
```
**Aplica a**: JAR-198, JAR-184

#### Workflow Tipo 5: Sistema de Evaluación
```
@project-management → @teaching [profesor] → @development [tdd] →
@development [arquitecto] → @quality → @documentation → @project-management
```
**Aplica a**: JAR-199

#### Workflow Tipo 6: Proyecto Final
```
@project-management → @development [arquitecto] → @teaching [pedagogo] →
@development [tdd] → @infrastructure → @quality →
@documentation → @project-management
```
**Aplica a**: JAR-197

### Ejemplo Práctico: JAR-186 (Tema CSV)

1. Abre la issue en Linear: [JAR-186](https://linear.app/jarko/issue/JAR-186)
2. Lee la sección "🤖 Workflow de Comandos"
3. Invoca cada sub-agente en orden:
   ```
   1. @project-management - "Revisar JAR-186 y planificar Tema 2: CSV"
   2. @teaching [pedagogo] - "Crear 01-TEORIA.md para CSV desde cero"
   3. @teaching [profesor] - "Crear 02-EJEMPLOS.md con casos reales"
   4. @teaching [profesor] - "Crear 03-EJERCICIOS.md"
   5. @teaching [psicólogo] - "Validar progresión pedagógica"
   6. @development [arquitecto] - "Diseñar estructura procesador CSV"
   7. @development [tdd] - "Escribir tests para procesador CSV"
   8. @development [tdd] - "Implementar funciones CSV"
   9. @quality - "Ejecutar black, flake8, pytest"
   10. @documentation - "Actualizar README y CHANGELOG"
   11. @project-management - "Marcar JAR-186 como Done"
   ```

### Notas sobre Workflows
- Los workflows son **guías**, no reglas estrictas
- Puedes adaptar el orden según el contexto
- Algunos pasos pueden ejecutarse en paralelo
- El orden general es: **Planificación → Creación → Calidad → Documentación → Cierre**

---

## 📝 Notas Importantes

### Filosofía de Implementación
- ✅ **Calidad sobre velocidad**: Mejor hacer bien que hacer rápido
- ✅ **TDD siempre**: Escribir tests primero
- ✅ **Documentar mientras creas**: No dejar documentación para después
- ✅ **Validar con usuarios**: Pedir feedback temprano y frecuente
- ✅ **Seguir los workflows**: Invocar sub-agentes en el orden especificado

### Flexibilidad
Este orden es una **recomendación**, no una regla estricta. Puedes:
- Trabajar en paralelo en varias issues si tienes un equipo
- Ajustar prioridades según feedback de estudiantes
- Saltarte issues que no aporten valor inmediato
- Adaptar workflows según necesidad

### Tracking
- Ver todas las issues en Linear: https://linear.app/jarko/project/master-ingenieria-de-datos-3041b5471239
- Cada issue contiene su workflow de sub-agentes específico
- Actualizar el CHANGELOG.md al completar cada issue
- Marcar issues como "In Progress" → "Done" en Linear

---

**¡Éxito con la implementación!** 🚀

*Última actualización: 2025-10-18*
