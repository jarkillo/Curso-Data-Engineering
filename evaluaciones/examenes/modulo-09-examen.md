# Examen Módulo 9: Spark y Big Data

**Tiempo recomendado:** 60 minutos
**Puntuación mínima para aprobar:** 70/100

---

## Parte A: Preguntas de Opción Múltiple (50 puntos)

### Pregunta 1
¿Qué es un **DataFrame** en Spark?

a) Un archivo de datos
b) Una colección distribuida con schema
c) Una base de datos
d) Un tipo de cluster

---

### Pregunta 2
¿Qué tipo de transformación es `groupBy()` en Spark?

a) Narrow transformation
b) Wide transformation
c) Action
d) Ninguna

---

### Pregunta 3
¿Cuál es la diferencia entre transformaciones y acciones en Spark?

a) Las transformaciones ejecutan inmediatamente
b) Las acciones son lazy, transformaciones no
c) Las transformaciones son lazy, acciones ejecutan el plan
d) No hay diferencia

---

### Pregunta 4
¿Qué es **shuffle** en Spark?

a) Ordenar datos
b) Redistribuir datos entre particiones
c) Comprimir datos
d) Eliminar duplicados

---

### Pregunta 5
¿Qué método persiste un DataFrame en memoria?

a) `save()`
b) `cache()` / `persist()`
c) `store()`
d) `write()`

---

### Pregunta 6
¿Qué tipo de join envía la tabla pequeña a todos los workers?

a) Shuffle join
b) Sort-merge join
c) Broadcast join
d) Cross join

---

### Pregunta 7
¿Qué es un **partition** en Spark?

a) Una división lógica del cluster
b) Un chunk de datos procesado en paralelo
c) Un tipo de archivo
d) Una base de datos

---

### Pregunta 8
¿Qué componente de Spark permite SQL sobre DataFrames?

a) Spark Core
b) Spark SQL
c) Spark MLlib
d) Spark Streaming

---

### Pregunta 9
¿Cuál es el tamaño recomendado de partición en Spark?

a) 1 MB
b) 10 MB
c) 128-200 MB
d) 1 GB

---

### Pregunta 10
¿Qué es **lazy evaluation**?

a) Ejecución inmediata de todas las operaciones
b) Retrasar ejecución hasta que se necesite el resultado
c) Ejecución en segundo plano
d) Ejecución sin optimización

---

## Parte B: Preguntas de Respuesta Corta (50 puntos)

### Pregunta 11
Escribe código PySpark para leer un CSV, filtrar filas, agrupar y calcular la suma.

```python
# Escribe tu código aquí

```

---

### Pregunta 12
Explica cómo optimizar un job de Spark que está tardando mucho. Menciona al menos 5 técnicas.

```
(Escribe tu respuesta aquí)
```

---

### Pregunta 13
¿Cuál es la diferencia entre `repartition()` y `coalesce()`? ¿Cuándo usar cada uno?

```
(Escribe tu respuesta aquí)
```

---

### Pregunta 14
Escribe código para hacer un broadcast join entre una tabla grande y una pequeña.

```python
# Escribe tu código aquí

```

---

### Pregunta 15
Describe la arquitectura de un cluster Spark: Driver, Executors, Cluster Manager.

```
(Escribe tu respuesta aquí)
```

---

## Hoja de Respuestas - Parte A

| Pregunta | Tu Respuesta |
|----------|--------------|
| 1-10     |              |

---

**Nombre:** _______________________ **Fecha:** _______________________ **Puntuación:** ___/100
