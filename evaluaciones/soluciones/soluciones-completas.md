# Soluciones Completas - Sistema de Evaluación

Este documento contiene las respuestas correctas y explicaciones detalladas para todos los exámenes.

---

## Módulo 1: Fundamentos de Python y Estadística

### Parte A - Respuestas

| Pregunta | Respuesta | Explicación |
|----------|-----------|-------------|
| 1 | b | Media = Suma / Cantidad |
| 2 | b | [10,20,**30**,40,50] - el valor central |
| 3 | b | La mediana no se ve afectada por valores extremos |
| 4 | b | `list` es mutable, `tuple` es inmutable |
| 5 | c | σ mide dispersión respecto a la media |
| 6 | c | `sum()/len()` = media aritmética |
| 7 | b | 5 aparece 3 veces (máxima frecuencia) |
| 8 | b | Segundo dataset tiene valores más dispersos |
| 9 | b | `open(file, "r")` para lectura |
| 10 | b | Mediana = Percentil 50 |

### Parte B - Respuestas Modelo

**Pregunta 11:** La media es el promedio aritmético, la mediana es el valor central. Usar mediana cuando hay outliers o distribución sesgada (ej: salarios).

**Pregunta 12:**
```python
def calcular_media(numeros: list[float]) -> float:
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)
```

**Pregunta 13:** Outlier: 900. Media con outlier: 271.4€, sin outlier: 166.7€. Mediana: 170€ (no cambia).

**Pregunta 14:** IQR = Q3 - Q1. Outliers: valores < Q1-1.5×IQR o > Q3+1.5×IQR.

**Pregunta 15:**
```python
def desviacion_estandar(numeros: list[float]) -> float:
    n = len(numeros)
    media = sum(numeros) / n
    suma_cuadrados = sum((x - media) ** 2 for x in numeros)
    return (suma_cuadrados / n) ** 0.5
```

---

## Módulo 2: SQL

### Parte A - Respuestas

| Pregunta | Respuesta | Explicación |
|----------|-----------|-------------|
| 1 | b | SELECT recupera datos |
| 2 | b | WHERE filtra filas, HAVING filtra grupos |
| 3 | c | LEFT JOIN mantiene todas las filas izquierdas |
| 4 | b | COUNT(*) cuenta filas |
| 5 | b | ORDER BY ordena resultados |
| 6 | b | DISTINCT elimina duplicados |
| 7 | d | COUNT(col) y SUM() ignoran NULL |
| 8 | b | LIMIT restringe filas devueltas |
| 9 | b | LIKE con % para patrones |
| 10 | b | B-tree para alta cardinalidad |

### Parte B - Respuestas Modelo

**Pregunta 11:**
```sql
SELECT nombre, salario
FROM empleados
ORDER BY salario DESC
LIMIT 5;
```

**Pregunta 12:** INNER: solo coincidencias. LEFT: todas izquierda + coincidencias. FULL: todas de ambas tablas.

**Pregunta 13:**
```sql
SELECT categoria, SUM(total) as total_ventas
FROM ventas
GROUP BY categoria
HAVING SUM(total) > 10000;
```

**Pregunta 14:**
```sql
SELECT * FROM empleados
WHERE salario > (SELECT AVG(salario) FROM empleados);
```

**Pregunta 15:** Normalización elimina redundancia. 1NF: valores atómicos. 2NF: sin dependencias parciales. 3NF: sin dependencias transitivas.

---

## Módulo 3: ETL

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | b |
| 3 | c |
| 4 | c |
| 5 | b |
| 6 | b |
| 7 | b |
| 8 | b |
| 9 | b |
| 10 | b |

---

## Módulo 4: APIs

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | c |
| 2 | b |
| 3 | b |
| 4 | c |
| 5 | c |
| 6 | b |
| 7 | c |
| 8 | b |
| 9 | b |
| 10 | b |

---

## Módulo 5: Bases de Datos Avanzadas

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | a |
| 2 | b |
| 3 | b |
| 4 | b |
| 5 | b |
| 6 | b |
| 7 | b |
| 8 | d |
| 9 | c |
| 10 | b |

---

## Módulo 6: Apache Airflow

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | c |
| 3 | b |
| 4 | a |
| 5 | b |
| 6 | b |
| 7 | b |
| 8 | b |
| 9 | a |
| 10 | c |

---

## Módulo 7: Cloud

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | b |
| 3 | b |
| 4 | b |
| 5 | b |
| 6 | b |
| 7 | b |
| 8 | b |
| 9 | b |
| 10 | b |

---

## Módulo 8: Data Warehousing

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | b |
| 3 | b |
| 4 | b |
| 5 | b |
| 6 | c |
| 7 | b |
| 8 | b |
| 9 | b |
| 10 | b |

---

## Módulo 9: Spark

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | b |
| 3 | c |
| 4 | b |
| 5 | b |
| 6 | c |
| 7 | b |
| 8 | b |
| 9 | c |
| 10 | b |

---

## Módulo 10: ML/MLOps

### Parte A - Respuestas

| Pregunta | Respuesta |
|----------|-----------|
| 1 | b |
| 2 | b |
| 3 | a |
| 4 | b |
| 5 | b |
| 6 | b |
| 7 | b |
| 8 | b |
| 9 | b |
| 10 | d |

---

## Criterios de Evaluación Parte B

Para las preguntas de respuesta corta, evaluar:

- **Código (0-10 puntos):**
  - Funciona correctamente: 4 puntos
  - Maneja errores: 2 puntos
  - Código limpio/legible: 2 puntos
  - Sigue buenas prácticas: 2 puntos

- **Explicaciones (0-10 puntos):**
  - Conceptos correctos: 4 puntos
  - Ejemplos relevantes: 3 puntos
  - Claridad: 3 puntos
