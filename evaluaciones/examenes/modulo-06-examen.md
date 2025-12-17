# Examen Módulo 6: Apache Airflow

**Tiempo recomendado:** 60 minutos
**Puntuación mínima para aprobar:** 70/100

---

## Parte A: Preguntas de Opción Múltiple (50 puntos)

### Pregunta 1
¿Qué significa **DAG** en Apache Airflow?

a) Data Analysis Graph
b) Directed Acyclic Graph
c) Dynamic Automated Generator
d) Data Aggregation Gateway

---

### Pregunta 2
¿Qué componente de Airflow ejecuta las tareas?

a) Scheduler
b) Webserver
c) Worker/Executor
d) Metadata Database

---

### Pregunta 3
¿Qué operador se usa para ejecutar código Python en Airflow?

a) BashOperator
b) PythonOperator
c) SQLOperator
d) TaskOperator

---

### Pregunta 4
¿Qué expresión cron representa "todos los días a las 6 AM"?

a) `0 6 * * *`
b) `6 0 * * *`
c) `* 6 * * *`
d) `0 * 6 * *`

---

### Pregunta 5
¿Qué son los **XComs** en Airflow?

a) Comandos externos
b) Mecanismo para compartir datos entre tareas
c) Tipo de operador
d) Logs de ejecución

---

### Pregunta 6
¿Qué parámetro define cuántas veces se reintenta una tarea fallida?

a) `max_attempts`
b) `retries`
c) `retry_count`
d) `attempts`

---

### Pregunta 7
¿Cuál es el propósito del operador `BranchPythonOperator`?

a) Ejecutar código en paralelo
b) Decidir qué rama del DAG ejecutar
c) Conectar con APIs externas
d) Manejar errores

---

### Pregunta 8
¿Qué significa `depends_on_past=True` en una tarea?

a) La tarea depende de datos históricos
b) La tarea solo corre si la ejecución anterior fue exitosa
c) La tarea se ejecuta en orden cronológico
d) La tarea guarda historial

---

### Pregunta 9
¿Qué es un **Sensor** en Airflow?

a) Un operador que espera una condición antes de continuar
b) Un monitor de recursos
c) Un tipo de log
d) Una conexión externa

---

### Pregunta 10
¿Dónde se almacenan las credenciales de conexión en Airflow?

a) En el código del DAG
b) En variables de entorno solamente
c) En Connections (metadata database)
d) En archivos de texto

---

## Parte B: Preguntas de Respuesta Corta (50 puntos)

### Pregunta 11
Escribe un DAG básico con 3 tareas: extract → transform → load, que se ejecute diariamente a las 8 AM.

```python
# Escribe tu código aquí

```

---

### Pregunta 12
Explica la diferencia entre `SequentialExecutor`, `LocalExecutor` y `CeleryExecutor`. ¿Cuándo usar cada uno?

```
(Escribe tu respuesta aquí)
```

---

### Pregunta 13
¿Cómo implementarías manejo de errores en un DAG? Incluye retries, alertas y fallback.

```
(Escribe tu respuesta aquí)
```

---

### Pregunta 14
Escribe código para usar XComs: una tarea que genere datos y otra que los consuma.

```python
# Escribe tu código aquí

```

---

### Pregunta 15
Describe cómo configurarías un DAG para procesar datos de los últimos 30 días (backfill) de forma eficiente.

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
