# Sistema de Evaluación y Certificación

Sistema completo para evaluar conocimientos y emitir certificados del Máster en Ingeniería de Datos.

## Estructura

```
evaluaciones/
├── README.md                    # Este archivo
├── examenes/
│   ├── modulo-01-examen.md     # Estadística y Python
│   ├── modulo-02-examen.md     # SQL
│   ├── modulo-03-examen.md     # ETL/Ingeniería de Datos
│   ├── modulo-04-examen.md     # APIs y Web Scraping
│   ├── modulo-05-examen.md     # Bases de Datos Avanzadas
│   ├── modulo-06-examen.md     # Apache Airflow
│   ├── modulo-07-examen.md     # Cloud (AWS/GCP)
│   ├── modulo-08-examen.md     # Data Warehousing
│   ├── modulo-09-examen.md     # Spark/Big Data
│   └── modulo-10-examen.md     # ML para Data Engineers
├── soluciones/
│   └── soluciones-completas.md # Respuestas y explicaciones
├── certificados/
│   └── .gitkeep                # Carpeta para certificados generados
├── generar_certificado.py      # Script para generar PDF
└── tracking_progreso.py        # Sistema de seguimiento
```

## Criterios de Evaluación

### Puntuación por Módulo

| Tipo de Pregunta | Cantidad | Puntos c/u | Total |
|------------------|----------|------------|-------|
| Opción Múltiple  | 10       | 5          | 50    |
| Respuesta Corta  | 5        | 10         | 50    |
| **Total**        | **15**   | -          | **100** |

### Criterios de Aprobación

- **Aprobación por módulo:** ≥ 70 puntos (70%)
- **Certificación completa:** Aprobar los 10 módulos
- **Mención honorífica:** Promedio ≥ 90% en todos los módulos

## Formato de Exámenes

Cada examen contiene:

1. **10 preguntas de opción múltiple** (5 puntos cada una)
   - 4 opciones (a, b, c, d)
   - Solo una respuesta correcta
   - Cubren conceptos teóricos y prácticos

2. **5 preguntas de respuesta corta** (10 puntos cada una)
   - Requieren explicación o código
   - Evalúan comprensión profunda
   - Pueden incluir ejercicios prácticos

## Uso del Sistema

### 1. Realizar un Examen

```bash
# Los exámenes están en formato Markdown
# Responde en una copia del archivo o en papel
cat evaluaciones/examenes/modulo-01-examen.md
```

### 2. Verificar Respuestas

```bash
# Las soluciones incluyen explicaciones detalladas
cat evaluaciones/soluciones/soluciones-completas.md
```

### 3. Generar Certificado

```bash
# Requiere: pip install reportlab
python evaluaciones/generar_certificado.py \
    --nombre "Tu Nombre" \
    --calificaciones "95,88,92,85,90,87,91,89,93,88"
```

### 4. Tracking de Progreso

```bash
# Ver progreso actual
python evaluaciones/tracking_progreso.py --ver

# Registrar calificación
python evaluaciones/tracking_progreso.py \
    --registrar \
    --modulo 1 \
    --puntuacion 85
```

## Tiempo Recomendado

| Módulo | Tiempo Examen | Dificultad |
|--------|---------------|------------|
| 1. Estadística/Python | 45 min | ⭐⭐ |
| 2. SQL | 45 min | ⭐⭐ |
| 3. ETL | 60 min | ⭐⭐⭐ |
| 4. APIs | 45 min | ⭐⭐ |
| 5. BD Avanzadas | 60 min | ⭐⭐⭐ |
| 6. Airflow | 60 min | ⭐⭐⭐ |
| 7. Cloud | 60 min | ⭐⭐⭐ |
| 8. DWH | 60 min | ⭐⭐⭐⭐ |
| 9. Spark | 60 min | ⭐⭐⭐⭐ |
| 10. ML/MLOps | 60 min | ⭐⭐⭐⭐ |

## Certificado

Al completar todos los módulos con ≥70%, recibirás:

- **Certificado PDF** con:
  - Nombre del estudiante
  - Fecha de completación
  - Calificación promedio
  - Módulos completados
  - Código de verificación único

## Política de Reintentos

- Cada módulo puede repetirse **hasta 3 veces**
- Se registra la **mejor calificación**
- Esperar **24 horas** entre intentos
