# Examen Módulo 2: SQL

**Tiempo recomendado:** 45 minutos
**Puntuación mínima para aprobar:** 70/100

---

## Parte A: Preguntas de Opción Múltiple (50 puntos)

*Selecciona la respuesta correcta para cada pregunta (5 puntos cada una)*

### Pregunta 1
¿Qué comando SQL se utiliza para recuperar datos de una tabla?

a) GET
b) SELECT
c) FETCH
d) RETRIEVE

---

### Pregunta 2
¿Cuál es la diferencia principal entre `WHERE` y `HAVING`?

a) No hay diferencia, son sinónimos
b) `WHERE` filtra antes de agrupar, `HAVING` después de agrupar
c) `WHERE` es para números, `HAVING` para texto
d) `HAVING` es más rápido que `WHERE`

---

### Pregunta 3
¿Qué tipo de JOIN devuelve **todas** las filas de la tabla izquierda, incluso si no hay coincidencias?

a) INNER JOIN
b) RIGHT JOIN
c) LEFT JOIN
d) CROSS JOIN

---

### Pregunta 4
Dada la query: `SELECT COUNT(*) FROM ventas WHERE total > 100`, ¿qué devuelve?

a) La suma de todos los totales mayores a 100
b) El número de filas donde total > 100
c) El valor máximo de total
d) Todas las filas donde total > 100

---

### Pregunta 5
¿Qué cláusula se usa para ordenar resultados en SQL?

a) SORT BY
b) ORDER BY
c) ARRANGE BY
d) GROUP BY

---

### Pregunta 6
¿Cuál es el resultado de `SELECT DISTINCT departamento FROM empleados`?

a) Todos los departamentos, incluyendo duplicados
b) Cada departamento único, sin duplicados
c) El conteo de departamentos
d) Error de sintaxis

---

### Pregunta 7
En SQL, ¿qué función de agregación ignora valores NULL?

a) COUNT(*)
b) COUNT(columna)
c) SUM(columna)
d) Tanto b como c

---

### Pregunta 8
¿Qué hace la cláusula `LIMIT 10`?

a) Filtra filas donde el valor es menor a 10
b) Devuelve solo las primeras 10 filas
c) Limita el tiempo de ejecución a 10 segundos
d) Agrupa en conjuntos de 10

---

### Pregunta 9
¿Cuál es la forma correcta de buscar valores que contengan "data"?

a) `WHERE nombre = 'data'`
b) `WHERE nombre LIKE '%data%'`
c) `WHERE nombre CONTAINS 'data'`
d) `WHERE nombre IN ('data')`

---

### Pregunta 10
¿Qué tipo de índice es más eficiente para columnas con muchos valores únicos?

a) Índice bitmap
b) Índice B-tree
c) Índice hash
d) Sin índice

---

## Parte B: Preguntas de Respuesta Corta (50 puntos)

*Responde con explicación o código SQL según corresponda (10 puntos cada una)*

### Pregunta 11
Escribe una query SQL que obtenga el **nombre** y **salario** de los 5 empleados mejor pagados, ordenados de mayor a menor salario.

**Tu respuesta:**

```sql
-- Escribe tu query aquí

```

---

### Pregunta 12
Explica la diferencia entre `INNER JOIN`, `LEFT JOIN` y `FULL OUTER JOIN`. Proporciona un ejemplo de cuándo usar cada uno.

**Tu respuesta:**

```
(Escribe tu respuesta aquí)
```

---

### Pregunta 13
Escribe una query que calcule el **total de ventas por categoría** y muestre solo las categorías con ventas totales superiores a 10,000.

**Tu respuesta:**

```sql
-- Escribe tu query aquí

```

---

### Pregunta 14
¿Qué es una **subquery** (subconsulta)? Escribe un ejemplo que use una subquery para encontrar empleados que ganan más que el promedio.

**Tu respuesta:**

```sql
-- Escribe tu query aquí

```

---

### Pregunta 15
Explica qué es la **normalización** en bases de datos y describe las tres primeras formas normales (1NF, 2NF, 3NF).

**Tu respuesta:**

```
(Escribe tu respuesta aquí)
```

---

## Hoja de Respuestas - Parte A

| Pregunta | Tu Respuesta |
|----------|--------------|
| 1        |              |
| 2        |              |
| 3        |              |
| 4        |              |
| 5        |              |
| 6        |              |
| 7        |              |
| 8        |              |
| 9        |              |
| 10       |              |

---

**Nombre del estudiante:** _______________________

**Fecha:** _______________________

**Puntuación Total:** _______ / 100
