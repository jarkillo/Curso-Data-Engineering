# SQL Básico: Tu Primer Lenguaje para Hablar con Bases de Datos

## Introducción: ¿Por qué SQL?

Imagina que tienes una biblioteca enorme con millones de libros. Necesitas encontrar todos los libros de ciencia ficción publicados después del año 2000, ordenados por popularidad. ¿Cómo lo harías?

Podrías revisar libro por libro manualmente (tardarías años), o podrías pedirle a un bibliotecario experto que te ayude usando el sistema de catalogación. **SQL es ese sistema de catalogación para datos**.

### ¿Qué es SQL?

**SQL** (Structured Query Language, pronunciado "ese-cu-ele" o "sequel") es el lenguaje universal para comunicarte con bases de datos relacionales. Es como el inglés para hablar con personas, pero diseñado específicamente para pedir, filtrar, ordenar y analizar datos.

**Analogía simple:**
- **Base de datos** = Biblioteca gigante
- **Tabla** = Estantería con un tipo específico de libros
- **Fila** = Un libro individual
- **Columna** = Una característica del libro (título, autor, año)
- **SQL** = El lenguaje que usas para pedir libros específicos

### ¿Por qué es importante en Data Engineering?

Como Data Engineer, el 80% de tu trabajo involucra datos almacenados en bases de datos. Necesitas SQL para:

1. **Extraer datos** de sistemas de producción (E en ETL)
2. **Analizar datos** para entender patrones de negocio
3. **Transformar datos** antes de cargarlos en un Data Warehouse
4. **Validar calidad** de datos (contar nulos, duplicados, etc.)
5. **Crear reportes** para equipos de negocio

**Ejemplo real:** En TechStore (nuestra tienda de electrónica ficticia), el equipo de marketing quiere saber cuáles son los 10 productos más vendidos del último mes. Sin SQL, tendrías que exportar millones de registros a Excel y procesarlos manualmente. Con SQL, obtienes la respuesta en 2 segundos con una query de 5 líneas.

---

## Conceptos Fundamentales

### 1. SELECT y FROM: Pidiendo Datos

**¿Qué hace?**
`SELECT` te permite "seleccionar" qué columnas quieres ver de una tabla. `FROM` indica de qué tabla quieres esos datos.

**Analogía:**
Es como decirle al bibliotecario: "Quiero ver el **título** y el **autor** de los libros que están en la estantería de **ciencia ficción**".

**Sintaxis básica:**
```sql
SELECT columna1, columna2
FROM nombre_tabla;
```

**Ejemplo mental:**
Tienes una tabla llamada `productos` con información de productos de TechStore:

| id  | nombre           | precio | categoria    |
| --- | ---------------- | ------ | ------------ |
| 1   | Laptop HP        | 899.99 | Computadoras |
| 2   | Mouse Logitech   | 25.50  | Accesorios   |
| 3   | Teclado Mecánico | 89.99  | Accesorios   |

Si ejecutas:
```sql
SELECT nombre, precio
FROM productos;
```

Obtienes:
| nombre           | precio |
| ---------------- | ------ |
| Laptop HP        | 899.99 |
| Mouse Logitech   | 25.50  |
| Teclado Mecánico | 89.99  |

**Nota:** El punto y coma (`;`) al final indica que la query terminó. Es como el punto final de una oración.

#### SELECT * (Seleccionar todo)

Si quieres ver **todas** las columnas, usa el asterisco `*`:

```sql
SELECT *
FROM productos;
```

Esto devuelve todas las columnas: `id`, `nombre`, `precio`, `categoria`.

**⚠️ Buena práctica:** En producción, evita `SELECT *` porque puede ser lento si la tabla tiene muchas columnas. Especifica solo las columnas que necesitas.

---

### 2. WHERE: Filtrando Datos

**¿Qué hace?**
`WHERE` filtra las filas que cumplen una condición específica. Es como poner un filtro en una búsqueda.

**Analogía:**
Es como decirle al bibliotecario: "Quiero libros de ciencia ficción, **pero solo los que cuestan menos de $20**".

**Sintaxis:**
```sql
SELECT columnas
FROM tabla
WHERE condicion;
```

**Ejemplo:**
```sql
SELECT nombre, precio
FROM productos
WHERE precio < 100;
```

Resultado:
| nombre           | precio |
| ---------------- | ------ |
| Mouse Logitech   | 25.50  |
| Teclado Mecánico | 89.99  |

**Operadores de comparación:**

| Operador    | Significado   | Ejemplo                     |
| ----------- | ------------- | --------------------------- |
| `=`         | Igual a       | `precio = 25.50`            |
| `!=` o `<>` | Diferente de  | `categoria != 'Accesorios'` |
| `>`         | Mayor que     | `precio > 50`               |
| `<`         | Menor que     | `precio < 100`              |
| `>=`        | Mayor o igual | `precio >= 89.99`           |
| `<=`        | Menor o igual | `precio <= 100`             |

#### Operadores Lógicos (AND, OR, NOT)

Puedes combinar múltiples condiciones:

**AND (Y):** Ambas condiciones deben cumplirse
```sql
SELECT nombre, precio
FROM productos
WHERE precio < 100 AND categoria = 'Accesorios';
```

**OR (O):** Al menos una condición debe cumplirse
```sql
SELECT nombre, precio
FROM productos
WHERE precio < 50 OR categoria = 'Computadoras';
```

**NOT (NO):** Invierte la condición
```sql
SELECT nombre, precio
FROM productos
WHERE NOT categoria = 'Accesorios';
-- Equivalente a: WHERE categoria != 'Accesorios'
```

#### Operador LIKE (Búsqueda de patrones)

Para buscar texto que contenga ciertas letras:

```sql
SELECT nombre
FROM productos
WHERE nombre LIKE '%Logitech%';
```

- `%` = Cualquier cantidad de caracteres
- `_` = Exactamente un carácter

Ejemplos:
- `LIKE 'Laptop%'` → Empieza con "Laptop"
- `LIKE '%HP'` → Termina con "HP"
- `LIKE '%Mouse%'` → Contiene "Mouse"

#### Operador IN (Lista de valores)

Para verificar si un valor está en una lista:

```sql
SELECT nombre, categoria
FROM productos
WHERE categoria IN ('Computadoras', 'Tablets', 'Smartphones');
```

Es más limpio que usar múltiples `OR`:
```sql
-- Equivalente pero más largo:
WHERE categoria = 'Computadoras'
   OR categoria = 'Tablets'
   OR categoria = 'Smartphones'
```

#### Operador BETWEEN (Rango de valores)

Para valores en un rango:

```sql
SELECT nombre, precio
FROM productos
WHERE precio BETWEEN 50 AND 200;
```

Equivalente a:
```sql
WHERE precio >= 50 AND precio <= 200
```

---

### 3. ORDER BY: Ordenando Resultados

**¿Qué hace?**
`ORDER BY` ordena los resultados por una o más columnas.

**Analogía:**
Es como pedirle al bibliotecario: "Dame los libros de ciencia ficción **ordenados por fecha de publicación, del más reciente al más antiguo**".

**Sintaxis:**
```sql
SELECT columnas
FROM tabla
WHERE condicion
ORDER BY columna [ASC|DESC];
```

- `ASC` = Ascendente (de menor a mayor) - **por defecto**
- `DESC` = Descendente (de mayor a menor)

**Ejemplo:**
```sql
SELECT nombre, precio
FROM productos
ORDER BY precio DESC;
```

Resultado (ordenado de más caro a más barato):
| nombre           | precio |
| ---------------- | ------ |
| Laptop HP        | 899.99 |
| Teclado Mecánico | 89.99  |
| Mouse Logitech   | 25.50  |

#### Ordenar por múltiples columnas

Puedes ordenar por varias columnas. La segunda columna se usa como "desempate":

```sql
SELECT nombre, categoria, precio
FROM productos
ORDER BY categoria ASC, precio DESC;
```

Esto ordena primero por categoría (alfabéticamente), y dentro de cada categoría, por precio (de mayor a menor).

---

### 4. LIMIT: Limitando Resultados

**¿Qué hace?**
`LIMIT` te da solo las primeras N filas del resultado.

**Analogía:**
Es como decirle al bibliotecario: "Dame solo los **primeros 10 libros** de la lista".

**Sintaxis:**
```sql
SELECT columnas
FROM tabla
ORDER BY columna
LIMIT numero;
```

**Ejemplo:** Top 3 productos más caros
```sql
SELECT nombre, precio
FROM productos
ORDER BY precio DESC
LIMIT 3;
```

**⚠️ Importante:** `LIMIT` se usa casi siempre con `ORDER BY`. Sin ordenar, obtienes las primeras N filas en el orden que estén almacenadas (que puede ser impredecible).

**Uso en Data Engineering:**
- Explorar datos rápidamente (`LIMIT 10` para ver una muestra)
- Obtener top N elementos (productos más vendidos, usuarios más activos)
- Paginar resultados en APIs (LIMIT + OFFSET)

---

### 5. Funciones Agregadas: Resumiendo Datos

**¿Qué son?**
Funciones que toman múltiples filas y devuelven **un solo valor** resumido.

**Analogía:**
Es como preguntarle al bibliotecario: "¿**Cuántos** libros hay en total?" o "¿Cuál es el **precio promedio** de los libros?".

#### COUNT: Contar filas

Cuenta cuántas filas hay:

```sql
SELECT COUNT(*)
FROM productos;
```

Resultado: `3` (hay 3 productos en total)

**COUNT con condición:**
```sql
SELECT COUNT(*)
FROM productos
WHERE precio < 100;
```

Resultado: `2` (hay 2 productos con precio menor a 100)

**COUNT(columna) vs COUNT(*):**
- `COUNT(*)` cuenta todas las filas
- `COUNT(columna)` cuenta solo filas donde esa columna NO es NULL

#### SUM: Sumar valores

Suma valores numéricos:

```sql
SELECT SUM(precio)
FROM productos;
```

Resultado: `1015.48` (899.99 + 25.50 + 89.99)

**Uso real:** Calcular ingresos totales, cantidad total de stock, etc.

#### AVG: Promedio

Calcula el promedio (media aritmética):

```sql
SELECT AVG(precio)
FROM productos;
```

Resultado: `338.49` (promedio de los 3 precios)

**Uso real:** Precio promedio de productos, tiempo promedio de entrega, etc.

#### MAX y MIN: Máximo y mínimo

Encuentra el valor más alto o más bajo:

```sql
SELECT MAX(precio) AS precio_maximo,
       MIN(precio) AS precio_minimo
FROM productos;
```

Resultado:
| precio_maximo | precio_minimo |
| ------------- | ------------- |
| 899.99        | 25.50         |

**Nota:** `AS` crea un alias (nombre alternativo) para la columna en el resultado.

---

### 6. GROUP BY: Agrupando Datos

**¿Qué hace?**
`GROUP BY` agrupa filas que tienen el mismo valor en una columna, y luego aplica funciones agregadas a cada grupo.

**Analogía:**
Es como decirle al bibliotecario: "Agrupa los libros **por género**, y dime **cuántos libros hay en cada género**".

**Sintaxis:**
```sql
SELECT columna_agrupacion, funcion_agregada(columna)
FROM tabla
GROUP BY columna_agrupacion;
```

**Ejemplo:** Contar productos por categoría

Tabla `productos`:
| id  | nombre           | precio  | categoria    |
| --- | ---------------- | ------- | ------------ |
| 1   | Laptop HP        | 899.99  | Computadoras |
| 2   | Mouse Logitech   | 25.50   | Accesorios   |
| 3   | Teclado Mecánico | 89.99   | Accesorios   |
| 4   | MacBook Pro      | 1999.99 | Computadoras |

Query:
```sql
SELECT categoria, COUNT(*) AS cantidad_productos
FROM productos
GROUP BY categoria;
```

Resultado:
| categoria    | cantidad_productos |
| ------------ | ------------------ |
| Computadoras | 2                  |
| Accesorios   | 2                  |

**¿Qué pasó?**
1. SQL agrupó las filas por `categoria`
2. Para cada grupo, contó cuántas filas hay
3. Devolvió un resultado por cada grupo

**Ejemplo más complejo:** Precio promedio por categoría
```sql
SELECT categoria,
       COUNT(*) AS cantidad,
       AVG(precio) AS precio_promedio
FROM productos
GROUP BY categoria
ORDER BY precio_promedio DESC;
```

Resultado:
| categoria    | cantidad | precio_promedio |
| ------------ | -------- | --------------- |
| Computadoras | 2        | 1449.99         |
| Accesorios   | 2        | 57.75           |

**⚠️ Regla importante:** Si usas `GROUP BY`, **todas las columnas en el SELECT deben estar en el GROUP BY o dentro de una función agregada**.

**Incorrecto:**
```sql
SELECT categoria, nombre, COUNT(*)
FROM productos
GROUP BY categoria;
-- ERROR: 'nombre' debe estar en GROUP BY o en una función agregada
```

**Correcto:**
```sql
SELECT categoria, COUNT(*)
FROM productos
GROUP BY categoria;
```

---

### 7. HAVING: Filtrando Grupos

**¿Qué hace?**
`HAVING` filtra grupos **después** de agrupar. Es como `WHERE`, pero para grupos en lugar de filas individuales.

**Analogía:**
Es como decirle al bibliotecario: "Agrupa los libros por género, y **muéstrame solo los géneros que tienen más de 100 libros**".

**Diferencia con WHERE:**
- `WHERE` filtra **filas** antes de agrupar
- `HAVING` filtra **grupos** después de agrupar

**Sintaxis:**
```sql
SELECT columna_agrupacion, funcion_agregada(columna)
FROM tabla
WHERE condicion_filas
GROUP BY columna_agrupacion
HAVING condicion_grupos;
```

**Ejemplo:** Categorías con más de 1 producto

```sql
SELECT categoria, COUNT(*) AS cantidad
FROM productos
GROUP BY categoria
HAVING COUNT(*) > 1;
```

Resultado:
| categoria    | cantidad |
| ------------ | -------- |
| Computadoras | 2        |
| Accesorios   | 2        |

**Ejemplo combinado (WHERE + HAVING):**

```sql
SELECT categoria, AVG(precio) AS precio_promedio
FROM productos
WHERE precio > 50  -- Filtrar filas: solo productos caros
GROUP BY categoria
HAVING AVG(precio) > 100  -- Filtrar grupos: solo categorías con promedio > 100
ORDER BY precio_promedio DESC;
```

**Orden de ejecución:**
1. `FROM` - Selecciona la tabla
2. `WHERE` - Filtra filas individuales
3. `GROUP BY` - Agrupa las filas filtradas
4. `HAVING` - Filtra grupos
5. `SELECT` - Selecciona columnas a mostrar
6. `ORDER BY` - Ordena el resultado final
7. `LIMIT` - Limita la cantidad de resultados

---

## Aplicaciones Prácticas en Data Engineering

### Caso de Uso 1: Análisis de Ventas

**Contexto:** TechStore quiere saber cuánto vendió cada categoría el último mes.

**Tabla `ventas`:**
| id  | producto_id | cantidad | fecha      | precio_unitario |
| --- | ----------- | -------- | ---------- | --------------- |
| 1   | 1           | 2        | 2025-10-15 | 899.99          |
| 2   | 2           | 5        | 2025-10-16 | 25.50           |
| 3   | 1           | 1        | 2025-10-20 | 899.99          |

**Query:**
```sql
SELECT
    p.categoria,
    COUNT(v.id) AS total_ventas,
    SUM(v.cantidad * v.precio_unitario) AS ingresos_totales
FROM ventas v
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha >= '2025-10-01'
GROUP BY p.categoria
ORDER BY ingresos_totales DESC;
```

**Decisión de negocio:** La categoría con más ingresos debería tener más stock y promociones.

---

### Caso de Uso 2: Reporte de Usuarios Activos

**Contexto:** CloudAPI Systems quiere saber cuántos usuarios usaron su API cada día.

**Query:**
```sql
SELECT
    DATE(fecha_request) AS dia,
    COUNT(DISTINCT usuario_id) AS usuarios_activos,
    COUNT(*) AS total_requests
FROM api_logs
WHERE fecha_request >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(fecha_request)
ORDER BY dia DESC;
```

**Decisión de negocio:** Si los usuarios activos bajan, investigar problemas técnicos o de UX.

---

### Caso de Uso 3: Detección de Productos Sin Stock

**Contexto:** TechStore necesita saber qué productos tienen stock bajo para reordenar.

**Query:**
```sql
SELECT
    nombre,
    stock_actual,
    categoria
FROM productos
WHERE stock_actual < 10
ORDER BY stock_actual ASC
LIMIT 20;
```

**Decisión de negocio:** Contactar proveedores para reabastecer estos productos.

---

## Errores Comunes y Cómo Evitarlos

### Error 1: Olvidar GROUP BY con funciones agregadas

**Incorrecto:**
```sql
SELECT categoria, COUNT(*)
FROM productos;
-- ERROR: 'categoria' debe estar en GROUP BY
```

**Correcto:**
```sql
SELECT categoria, COUNT(*)
FROM productos
GROUP BY categoria;
```

**Por qué pasa:** SQL no sabe cómo combinar múltiples valores de `categoria` en una sola fila sin agrupar.

---

### Error 2: Confundir WHERE con HAVING

**Incorrecto:**
```sql
SELECT categoria, COUNT(*) AS cantidad
FROM productos
GROUP BY categoria
WHERE COUNT(*) > 1;  -- ERROR: WHERE no puede usar funciones agregadas
```

**Correcto:**
```sql
SELECT categoria, COUNT(*) AS cantidad
FROM productos
GROUP BY categoria
HAVING COUNT(*) > 1;
```

**Regla:** Usa `WHERE` para filtrar filas, `HAVING` para filtrar grupos.

---

### Error 3: No usar alias claros

**Poco claro:**
```sql
SELECT categoria, COUNT(*), AVG(precio)
FROM productos
GROUP BY categoria;
```

Resultado:
| categoria    | COUNT(*) | AVG(precio) |
| ------------ | -------- | ----------- |
| Computadoras | 2        | 1449.99     |

**Mejor:**
```sql
SELECT
    categoria,
    COUNT(*) AS total_productos,
    AVG(precio) AS precio_promedio
FROM productos
GROUP BY categoria;
```

Resultado:
| categoria    | total_productos | precio_promedio |
| ------------ | --------------- | --------------- |
| Computadoras | 2               | 1449.99         |

**Beneficio:** Los nombres de columnas son autodescriptivos.

---

### Error 4: Usar LIMIT sin ORDER BY

**Impredecible:**
```sql
SELECT nombre, precio
FROM productos
LIMIT 5;
-- Devuelve 5 productos en orden aleatorio
```

**Predecible:**
```sql
SELECT nombre, precio
FROM productos
ORDER BY precio DESC
LIMIT 5;
-- Devuelve los 5 productos más caros
```

**Por qué:** Sin `ORDER BY`, el orden de las filas es impredecible (depende de cómo estén almacenadas físicamente).

---

### Error 5: Comparar NULL con =

**Incorrecto:**
```sql
SELECT nombre
FROM productos
WHERE descripcion = NULL;  -- Siempre devuelve 0 filas
```

**Correcto:**
```sql
SELECT nombre
FROM productos
WHERE descripcion IS NULL;
```

**Por qué:** `NULL` significa "valor desconocido", y no puedes comparar algo desconocido con `=`. Usa `IS NULL` o `IS NOT NULL`.

---

## Buenas Prácticas

### 1. Usa nombres de columnas descriptivos con alias

**Malo:**
```sql
SELECT COUNT(*), AVG(p)
FROM productos;
```

**Bueno:**
```sql
SELECT
    COUNT(*) AS total_productos,
    AVG(precio) AS precio_promedio
FROM productos;
```

---

### 2. Indenta tu SQL para legibilidad

**Malo:**
```sql
SELECT categoria,COUNT(*) AS cantidad FROM productos WHERE precio>50 GROUP BY categoria HAVING COUNT(*)>1 ORDER BY cantidad DESC;
```

**Bueno:**
```sql
SELECT
    categoria,
    COUNT(*) AS cantidad
FROM productos
WHERE precio > 50
GROUP BY categoria
HAVING COUNT(*) > 1
ORDER BY cantidad DESC;
```

---

### 3. Usa LIMIT para explorar datos grandes

Antes de ejecutar una query en una tabla con millones de filas:

```sql
SELECT *
FROM tabla_gigante
LIMIT 10;
```

Esto te da una muestra rápida sin esperar minutos.

---

### 4. Comenta queries complejas

```sql
-- Análisis de ventas por categoría del último mes
-- Objetivo: Identificar categorías con más ingresos
SELECT
    p.categoria,
    COUNT(v.id) AS total_ventas,
    SUM(v.cantidad * v.precio_unitario) AS ingresos_totales
FROM ventas v
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha >= '2025-10-01'  -- Solo octubre 2025
GROUP BY p.categoria
ORDER BY ingresos_totales DESC;
```

---

## Checklist de Aprendizaje

Antes de continuar al siguiente tema, asegúrate de que puedes:

- [ ] Explicar qué es SQL y por qué es importante en Data Engineering
- [ ] Escribir queries con `SELECT` y `FROM` para obtener datos de una tabla
- [ ] Usar `WHERE` para filtrar filas con diferentes operadores (=, >, <, LIKE, IN, BETWEEN)
- [ ] Ordenar resultados con `ORDER BY` (ASC y DESC)
- [ ] Limitar resultados con `LIMIT`
- [ ] Usar funciones agregadas (COUNT, SUM, AVG, MAX, MIN)
- [ ] Agrupar datos con `GROUP BY`
- [ ] Filtrar grupos con `HAVING`
- [ ] Explicar la diferencia entre `WHERE` y `HAVING`
- [ ] Entender el orden de ejecución de una query SQL
- [ ] Escribir queries con alias claros y buena indentación
- [ ] Identificar y corregir errores comunes

**Si respondiste "sí" a todo, estás listo para los ejemplos prácticos.**

---

## Recursos Adicionales

### Documentación Oficial
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SQLite Documentation](https://www.sqlite.org/lang.html)

### Práctica Interactiva
- [SQLZoo](https://sqlzoo.net/) - Tutoriales interactivos
- [LeetCode SQL](https://leetcode.com/problemset/database/) - Problemas de práctica
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) - Casos reales

### Videos Recomendados
- "SQL Tutorial for Beginners" - Programming with Mosh (YouTube)
- "SQL for Data Analysis" - Coursera

---

## Próximos Pasos

Ahora que entiendes los fundamentos de SQL, es hora de practicar:

1. **Ver ejemplos trabajados** en `02-EJEMPLOS.md`
2. **Resolver ejercicios** en `03-EJERCICIOS.md`
3. **Implementar el proyecto práctico** (análisis exploratorio de base de datos)

**¡Felicidades por completar la teoría de SQL Básico!** 🎉

---

**Última actualización:** 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [Módulo 1: Fundamentos: Logs y Debugging](../../modulo-01-fundamentos/tema-3-logs-debugging/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
