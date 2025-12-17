# SQL Intermedio: Combinando Datos como un Profesional

## Introducción: Más Allá de Una Sola Tabla

Imagina que trabajas en TechStore y tu jefe te pide: "Muéstrame las ventas de cada producto junto con su categoría". El problema es que tienes dos archivos Excel separados: uno con las ventas y otro con la información de productos. ¿Qué haces? Los combinas manualmente buscando coincidencias, ¿verdad?

**Esto es exactamente lo que hacen los JOINs en SQL**: combinan información de múltiples tablas relacionadas automáticamente.

### ¿Por qué necesitamos JOINs?

En el mundo real, los datos no viven en una sola tabla gigante. Esto sería ineficiente y causaría mucha duplicación. En vez de eso, dividimos la información en tablas especializadas:

- **Tabla `productos`**: id, nombre, precio, categoria_id
- **Tabla `categorias`**: id, nombre, descripción
- **Tabla `ventas`**: id, producto_id, cantidad, fecha

**Analogía del archivador de oficina:**
- Tienes un archivador con 3 cajones diferentes
- Cada cajón guarda un tipo de información
- Cuando necesitas información completa, vas de cajón en cajón "uniendo" los papeles relacionados
- **JOIN = El proceso de reunir papeles de diferentes cajones usando un identificador común**

### ¿Por qué es crítico en Data Engineering?

Como Data Engineer, el 90% de las queries que escribirás involucran múltiples tablas:

1. **Reportes de negocio**: "Ventas por categoría del último trimestre"
2. **ETL Pipelines**: Extraer y combinar datos de sistemas diferentes
3. **Data Warehouses**: Tablas de hechos (ventas) + dimensiones (productos, clientes)
4. **Análisis complejos**: Clientes que compraron X pero no Y
5. **Validación de datos**: Detectar inconsistencias entre tablas relacionadas

**Ejemplo real en TechStore:** El equipo de marketing quiere saber cuántos ingresos generó cada categoría de productos. Sin JOINs, tendrías que exportar dos tablas a Excel, usar VLOOKUP (¡error común!), y rezar para que no haya errores. Con JOINs, obtienes la respuesta en 5 segundos con una query de 8 líneas.

---

## Conceptos Fundamentales

### 1. INNER JOIN: La Intersección

**¿Qué hace?**
`INNER JOIN` combina dos tablas y devuelve **solo las filas donde hay coincidencias en ambas tablas**. Si algo existe en una tabla pero no en la otra, se descarta.

**Analogía del club exclusivo:**
Imagina dos listas:
- **Lista A**: Personas invitadas a una fiesta
- **Lista B**: Personas que confirmaron asistencia

Un **INNER JOIN** te da solo las personas que están en AMBAS listas (invitadas Y confirmaron).

**Sintaxis:**
```sql
SELECT columnas
FROM tabla_izquierda
INNER JOIN tabla_derecha
    ON tabla_izquierda.columna_comun = tabla_derecha.columna_comun;
```

**Ejemplo mental:**
```sql
-- Tabla productos
| id  | nombre           | categoria_id |
| --- | ---------------- | ------------ |
| 1   | Laptop HP        | 10           |
| 2   | Mouse Logitech   | 20           |
| 3   | Teclado Mecánico | 20           |

-- Tabla categorias
| id  | nombre       |
| --- | ------------ |
| 10  | Computadoras |
| 20  | Accesorios   |

-- INNER JOIN
SELECT productos.nombre, categorias.nombre AS categoria
FROM productos
INNER JOIN categorias
    ON productos.categoria_id = categorias.id;

-- Resultado: SOLO productos que tienen categoría
| nombre           | categoria    |
| ---------------- | ------------ |
| Laptop HP        | Computadoras |
| Mouse Logitech   | Accesorios   |
| Teclado Mecánico | Accesorios   |
```

**¿Cuándo usar INNER JOIN?**
- Cuando solo te interesan los registros que tienen coincidencia
- Cuando quieres "filtrar" datos incompletos
- Cuando necesitas datos relacionados que DEBEN existir en ambas tablas

**⚠️ Riesgo:** Si un producto no tiene categoría asignada (categoria_id = NULL), **no aparecerá en el resultado**.

---

### 2. LEFT JOIN: Todos de la Izquierda

**¿Qué hace?**
`LEFT JOIN` devuelve **todas las filas de la tabla izquierda**, y las filas coincidentes de la tabla derecha. Si no hay coincidencia, rellena con NULL.

**Analogía de la lista de asistencia:**
Imagina una lista de todos los estudiantes de una clase (tabla izquierda) y una lista de quienes entregaron la tarea (tabla derecha).

Un **LEFT JOIN** te muestra:
- **Todos los estudiantes** (están en la izquierda)
- Si entregaron tarea, ves su nota
- Si NO entregaron, ves NULL (vacío)

Esto te permite identificar **quién NO entregó**.

**Sintaxis:**
```sql
SELECT columnas
FROM tabla_izquierda
LEFT JOIN tabla_derecha
    ON tabla_izquierda.columna_comun = tabla_derecha.columna_comun;
```

**Ejemplo mental:**
```sql
-- Tabla clientes
| id  | nombre | email            |
| --- | ------ | ---------------- |
| 1   | Ana    | ana@email.com    |
| 2   | Carlos | carlos@email.com |
| 3   | María  | maria@email.com  |

-- Tabla pedidos
| id  | cliente_id | total  |
| --- | ---------- | ------ |
| 1   | 1          | 150.00 |
| 2   | 1          | 200.00 |

-- LEFT JOIN (¿Quiénes han comprado?)
SELECT clientes.nombre, pedidos.total
FROM clientes
LEFT JOIN pedidos
    ON clientes.id = pedidos.cliente_id;

-- Resultado: TODOS los clientes, con o sin pedidos
| nombre | total  |
| ------ | ------ |
| Ana    | 150.00 |
| Ana    | 200.00 |
| Carlos | NULL   | ← No ha comprado nada |
| María  | NULL   | ← No ha comprado nada |
```

**¿Cuándo usar LEFT JOIN?**
- Cuando necesitas **todos** los registros de la tabla principal
- Para identificar **ausencias** (clientes sin pedidos, productos sin ventas)
- Para reportes que no deben "perder" información de la tabla izquierda

**✅ Buena práctica:** Si quieres solo los clientes SIN pedidos, agrega `WHERE pedidos.id IS NULL`.

---

### 3. RIGHT JOIN: Todos de la Derecha

**¿Qué hace?**
`RIGHT JOIN` es el opuesto de LEFT JOIN: devuelve **todas las filas de la tabla derecha** y las coincidencias de la izquierda.

**Analogía:**
Es como LEFT JOIN pero mirando desde el otro lado. En la práctica, casi nunca se usa porque puedes reescribirlo como LEFT JOIN invirtiendo el orden de las tablas.

**Sintaxis:**
```sql
SELECT columnas
FROM tabla_izquierda
RIGHT JOIN tabla_derecha
    ON tabla_izquierda.columna_comun = tabla_derecha.columna_comun;
```

**Equivalencia:**
```sql
-- Estos dos queries son idénticos:

-- RIGHT JOIN
SELECT clientes.nombre, pedidos.total
FROM pedidos
RIGHT JOIN clientes
    ON pedidos.cliente_id = clientes.id;

-- LEFT JOIN (recomendado, más claro)
SELECT clientes.nombre, pedidos.total
FROM clientes
LEFT JOIN pedidos
    ON clientes.id = pedidos.cliente_id;
```

**⚠️ Consejo profesional:** En la industria, el 95% de los Data Engineers usa LEFT JOIN y evita RIGHT JOIN porque es más fácil de leer. Solo úsalo si el orden de las tablas está fijo por alguna razón.

---

### 4. FULL OUTER JOIN: Todos de Ambos Lados

**¿Qué hace?**
`FULL OUTER JOIN` devuelve **todas las filas de ambas tablas**, coincidan o no. Si no hay coincidencia, rellena con NULL en el lado que falta.

**Analogía del registro de invitados:**
- **Lista A**: Personas invitadas
- **Lista B**: Personas que llegaron

FULL OUTER JOIN te muestra:
- Invitados que llegaron (coincidencia)
- Invitados que NO llegaron (solo en A)
- Personas que llegaron sin invitación (solo en B)

**Sintaxis:**
```sql
SELECT columnas
FROM tabla_izquierda
FULL OUTER JOIN tabla_derecha
    ON tabla_izquierda.columna_comun = tabla_derecha.columna_comun;
```

**Ejemplo mental:**
```sql
-- Tabla empleados
| id  | nombre |
| --- | ------ |
| 1   | Ana    |
| 2   | Carlos |

-- Tabla asignaciones_proyecto
| id  | empleado_id | proyecto |
| --- | ----------- | -------- |
| 1   | 1           | Web      |
| 2   | 3           | App      |

-- FULL OUTER JOIN
SELECT empleados.nombre, asignaciones_proyecto.proyecto
FROM empleados
FULL OUTER JOIN asignaciones_proyecto
    ON empleados.id = asignaciones_proyecto.empleado_id;

-- Resultado: TODOS de ambas tablas
| nombre | proyecto |
| ------ | -------- |
| Ana    | Web      | ← Coincidencia                                    |
| Carlos | NULL     | ← Empleado sin proyecto                           |
| NULL   | App      | ← Proyecto asignado a empleado id=3 que no existe |
```

**¿Cuándo usar FULL OUTER JOIN?**
- Auditorías: detectar inconsistencias entre sistemas
- Reconciliación de datos: comparar dos fuentes
- Análisis de diferencias: qué está en A pero no en B, y viceversa

**⚠️ Nota:** SQLite NO soporta FULL OUTER JOIN directamente. Debes emularlo con UNION de LEFT y RIGHT JOIN.

---

### 5. CROSS JOIN: El Producto Cartesiano

**¿Qué hace?**
`CROSS JOIN` combina **cada fila de la tabla izquierda con cada fila de la derecha**. Es como multiplicar las tablas.

**Analogía de combinaciones:**
Tienes 3 camisetas (roja, azul, verde) y 2 pantalones (negro, gris). ¿Cuántos outfits puedes hacer? 3 × 2 = 6 combinaciones.

**CROSS JOIN hace exactamente eso**: todas las combinaciones posibles.

**Sintaxis:**
```sql
SELECT columnas
FROM tabla_izquierda
CROSS JOIN tabla_derecha;
-- No hay ON porque no necesitas condición de coincidencia
```

**Ejemplo mental:**
```sql
-- Tabla colores
| id  | nombre |
| --- | ------ |
| 1   | Rojo   |
| 2   | Azul   |

-- Tabla tallas
| id  | nombre |
| --- | ------ |
| 1   | S      |
| 2   | M      |
| 3   | L      |

-- CROSS JOIN
SELECT colores.nombre AS color, tallas.nombre AS talla
FROM colores
CROSS JOIN tallas;

-- Resultado: 2 × 3 = 6 filas (todas las combinaciones)
| color | talla |
| ----- | ----- |
| Rojo  | S     |
| Rojo  | M     |
| Rojo  | L     |
| Azul  | S     |
| Azul  | M     |
| Azul  | L     |
```

**¿Cuándo usar CROSS JOIN?**
- Generar todas las combinaciones posibles (ej: variantes de productos)
- Crear calendarios (años × meses × días)
- Simulaciones o análisis de escenarios

**⚠️ PELIGRO:** Si cruzas una tabla de 1,000 filas con otra de 1,000, obtienes 1,000,000 de filas. Úsalo con cuidado.

---

### 6. Subconsultas (Subqueries): Queries Anidadas

**¿Qué son?**
Una **subconsulta** es una query SQL dentro de otra query. Es como hacer una pregunta cuya respuesta usas para hacer otra pregunta.

**Analogía del investigador:**
Imagina que quieres saber quiénes ganaron más que el salario promedio.

**Paso 1** (subconsulta): "¿Cuál es el salario promedio?" → $50,000
**Paso 2** (query principal): "¿Quiénes ganan más de $50,000?"

La subconsulta hace el Paso 1 automáticamente dentro de la query principal.

#### 6.1. Subconsulta en WHERE

**Uso más común:** Filtrar basándose en un cálculo previo.

**Sintaxis:**
```sql
SELECT columnas
FROM tabla
WHERE columna OPERADOR (
    SELECT calculo
    FROM otra_tabla
    WHERE condicion
);
```

**Ejemplo:**
```sql
-- ¿Qué productos cuestan más que el precio promedio?

SELECT nombre, precio
FROM productos
WHERE precio > (
    SELECT AVG(precio)
    FROM productos
);

-- La subconsulta devuelve un SOLO valor: el promedio
-- La query principal lo usa para filtrar
```

#### 6.2. Subconsulta en FROM

**Uso:** Tratar el resultado de una query como si fuera una tabla temporal.

**Analogía:** Es como hacer un resumen en Excel y luego trabajar con ese resumen.

**Sintaxis:**
```sql
SELECT columnas
FROM (
    SELECT columnas
    FROM tabla
    WHERE condicion
) AS tabla_temporal;
```

**Ejemplo:**
```sql
-- Top 3 categorías por ingresos totales

SELECT categoria, ingresos_totales
FROM (
    SELECT categoria, SUM(ventas) AS ingresos_totales
    FROM ventas_por_categoria
    GROUP BY categoria
) AS resumen
ORDER BY ingresos_totales DESC
LIMIT 3;
```

#### 6.3. Subconsulta en SELECT

**Uso:** Calcular un valor específico para cada fila.

**Sintaxis:**
```sql
SELECT
    columna1,
    (SELECT calculo FROM otra_tabla WHERE condicion) AS columna_calculada
FROM tabla;
```

**Ejemplo:**
```sql
-- Mostrar cada producto con el precio promedio de su categoría

SELECT
    nombre,
    precio,
    (
        SELECT AVG(precio)
        FROM productos AS p2
        WHERE p2.categoria_id = productos.categoria_id
    ) AS precio_promedio_categoria
FROM productos;
```

**⚠️ Nota de performance:** Las subconsultas en SELECT pueden ser lentas si hay muchas filas. A veces es mejor usar JOINs + GROUP BY.

---

### 7. CASE WHEN: Condicionales en SQL

**¿Qué hace?**
`CASE WHEN` es como un `if-else` en programación: te permite crear columnas calculadas basadas en condiciones.

**Analogía de calificaciones:**
Si tienes notas numéricas (0-100), puedes convertirlas a letras:
- 90-100 → A
- 80-89 → B
- 70-79 → C
- <70 → F

**CASE WHEN hace exactamente eso**: transforma valores basándose en reglas.

**Sintaxis:**
```sql
SELECT
    columna,
    CASE
        WHEN condicion1 THEN valor1
        WHEN condicion2 THEN valor2
        WHEN condicion3 THEN valor3
        ELSE valor_por_defecto
    END AS nombre_columna_nueva
FROM tabla;
```

**Ejemplo básico:**
```sql
-- Clasificar productos por rango de precio

SELECT
    nombre,
    precio,
    CASE
        WHEN precio < 50 THEN 'Económico'
        WHEN precio BETWEEN 50 AND 200 THEN 'Medio'
        WHEN precio > 200 THEN 'Premium'
        ELSE 'Sin clasificar'
    END AS rango_precio
FROM productos;

-- Resultado:
| nombre           | precio | rango_precio |
| ---------------- | ------ | ------------ |
| Mouse Logitech   | 25.50  | Económico    |
| Teclado Mecánico | 89.99  | Medio        |
| Laptop HP        | 899.99 | Premium      |
```

**Ejemplo avanzado con agregación:**
```sql
-- Contar productos por rango de precio

SELECT
    CASE
        WHEN precio < 50 THEN 'Económico'
        WHEN precio BETWEEN 50 AND 200 THEN 'Medio'
        ELSE 'Premium'
    END AS rango,
    COUNT(*) AS cantidad
FROM productos
GROUP BY rango;

-- Resultado:
| rango     | cantidad |
| --------- | -------- |
| Económico | 5        |
| Medio     | 8        |
| Premium   | 3        |
```

**¿Cuándo usar CASE WHEN?**
- Categorizar datos (rangos, segmentos, grupos)
- Transformar valores (códigos → descripciones)
- Lógica de negocio en queries (descuentos, comisiones)
- Crear columnas derivadas para reportes

---

### 8. WHERE vs HAVING con JOINs

**Diferencia clave:**
- **WHERE**: Filtra **filas individuales** ANTES de agrupar
- **HAVING**: Filtra **grupos** DESPUÉS de agrupar

**Analogía del censo escolar:**
- **WHERE**: "Solo cuenten estudiantes mayores de 18 años" (filtras personas)
- **HAVING**: "Solo muestren salones con más de 30 estudiantes" (filtras grupos)

**Ejemplo con JOIN:**
```sql
-- Categorías con ventas totales > $1,000 (solo productos activos)

SELECT
    categorias.nombre,
    SUM(ventas.total) AS ingresos_totales
FROM categorias
INNER JOIN productos
    ON categorias.id = productos.categoria_id
INNER JOIN ventas
    ON productos.id = ventas.producto_id
WHERE productos.activo = 1  -- Filtro ANTES de agrupar
GROUP BY categorias.nombre
HAVING ingresos_totales > 1000;  -- Filtro DESPUÉS de agrupar
```

**Orden de ejecución SQL (importante):**
```
1. FROM + JOINs   → Combinar tablas
2. WHERE          → Filtrar filas
3. GROUP BY       → Agrupar
4. HAVING         → Filtrar grupos
5. SELECT         → Seleccionar columnas
6. ORDER BY       → Ordenar resultado
7. LIMIT          → Limitar cantidad
```

---

## Aplicaciones Prácticas en Data Engineering

### Caso de Uso 1: Análisis de Ventas Multi-Tabla

**Contexto:** TechStore necesita un reporte mensual de ventas por categoría, incluyendo productos que no se han vendido.

**Problema:** Los datos están en 3 tablas separadas (productos, categorías, ventas).

**Solución con JOINs:**
```sql
SELECT
    c.nombre AS categoria,
    p.nombre AS producto,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
    COALESCE(SUM(v.total), 0) AS ingresos
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id
LEFT JOIN ventas v ON p.id = v.producto_id
WHERE v.fecha >= '2025-01-01' OR v.fecha IS NULL
GROUP BY c.nombre, p.nombre
ORDER BY ingresos DESC;
```

**Decisión de negocio:** Identificar productos sin ventas para decidir si descontinuarlos o promocionarlos.

---

### Caso de Uso 2: Segmentación de Clientes

**Contexto:** Marketing quiere segmentar clientes en "VIP", "Regular", "Nuevo" basándose en sus compras.

**Solución con CASE WHEN:**
```sql
SELECT
    c.nombre,
    c.email,
    COUNT(v.id) AS total_pedidos,
    SUM(v.total) AS gasto_total,
    CASE
        WHEN SUM(v.total) > 5000 THEN 'VIP'
        WHEN COUNT(v.id) >= 5 THEN 'Regular'
        ELSE 'Nuevo'
    END AS segmento
FROM clientes c
LEFT JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.id, c.nombre, c.email
ORDER BY gasto_total DESC;
```

**Decisión de negocio:** Crear campañas personalizadas para cada segmento.

---

### Caso de Uso 3: Detección de Inconsistencias

**Contexto:** Auditoría detecta que hay ventas registradas de productos que no existen en el catálogo.

**Solución con FULL OUTER JOIN:**
```sql
-- Encontrar ventas huérfanas y productos sin ventas

SELECT
    v.id AS venta_id,
    v.producto_id,
    p.nombre AS producto
FROM ventas v
FULL OUTER JOIN productos p ON v.producto_id = p.id
WHERE v.id IS NULL OR p.id IS NULL;
```

**Decisión de negocio:** Limpiar datos inconsistentes antes de migraciones o reportes.

---

## Comparaciones Importantes

### INNER JOIN vs LEFT JOIN vs FULL JOIN

| Aspecto             | INNER JOIN                      | LEFT JOIN                           | FULL OUTER JOIN                    |
| ------------------- | ------------------------------- | ----------------------------------- | ---------------------------------- |
| **Filas devueltas** | Solo coincidencias              | Todas de izq. + coincidencias       | Todas de ambas                     |
| **NULLs**           | No aparecen                     | Aparecen en tabla derecha           | Aparecen en ambos lados            |
| **Uso común**       | Datos relacionados obligatorios | Identificar ausencias               | Auditorías y reconciliaciones      |
| **Ejemplo**         | Productos CON categoría         | Todos los productos (con o sin cat) | Todos productos y todas categorías |

### Cuándo Usar Cada JOIN

**Usa INNER JOIN cuando:**
- Solo te interesan registros que tienen relación confirmada
- Quieres "filtrar" datos incompletos
- Ejemplo: "Ventas de productos activos"

**Usa LEFT JOIN cuando:**
- Necesitas todos los registros de la tabla principal
- Quieres identificar ausencias (ej: clientes sin pedidos)
- Ejemplo: "Todos los clientes, muestren si han comprado"

**Usa FULL OUTER JOIN cuando:**
- Auditas inconsistencias
- Comparas dos fuentes de datos
- Ejemplo: "Productos en catálogo vs productos vendidos"

**Usa CROSS JOIN cuando:**
- Generas combinaciones (variantes de productos)
- Creas calendarios o grids
- **¡Cuidado!** Solo con tablas pequeñas

---

### Subconsulta vs JOIN

| Aspecto         | Subconsulta                      | JOIN                                |
| --------------- | -------------------------------- | ----------------------------------- |
| **Legibilidad** | Más clara para lógica simple     | Mejor para relaciones múltiples     |
| **Performance** | Puede ser más lenta              | Generalmente más rápida             |
| **Cuándo usar** | Cálculos simples (AVG, MAX)      | Combinar múltiples tablas           |
| **Ejemplo**     | `WHERE precio > (SELECT AVG...)` | `FROM productos JOIN categorias...` |

**Regla de oro:** Si puedes usar JOIN en vez de subconsulta, úsalo (mejor performance).

---

## Errores Comunes y Cómo Evitarlos

### Error 1: Producto Cartesiano Accidental

**Problema:** Olvidas el `ON` en un JOIN y obtienes millones de filas.

```sql
-- ❌ MAL (sin ON)
SELECT *
FROM productos, categorias;  -- 100 productos × 10 categorías = 1,000 filas

-- ✅ BIEN (con ON)
SELECT *
FROM productos
INNER JOIN categorias ON productos.categoria_id = categorias.id;
```

**Cómo detectarlo:** Si tu query devuelve muchas más filas de lo esperado, probablemente olvidaste el `ON`.

---

### Error 2: Confundir LEFT JOIN con INNER JOIN

**Problema:** Usas LEFT JOIN pero luego filtras la tabla derecha en WHERE, convirtiendo efectivamente en INNER JOIN.

```sql
-- ❌ MAL (LEFT JOIN inútil)
SELECT c.nombre, p.nombre
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
WHERE p.total > 100;  -- Esto elimina clientes sin pedidos

-- ✅ BIEN (dos opciones)

-- Opción 1: Si quieres clientes CON pedidos > 100, usa INNER JOIN
SELECT c.nombre, p.nombre
FROM clientes c
INNER JOIN pedidos p ON c.id = p.cliente_id
WHERE p.total > 100;

-- Opción 2: Si quieres todos los clientes, filtra NULL
SELECT c.nombre, p.nombre
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
WHERE p.total > 100 OR p.total IS NULL;
```

---

### Error 3: No Usar Alias en JOINs Múltiples

**Problema:** Con 3+ tablas, el código se vuelve ilegible sin alias.

```sql
-- ❌ MAL (sin alias)
SELECT productos.nombre, categorias.nombre, ventas.cantidad
FROM productos
INNER JOIN categorias ON productos.categoria_id = categorias.id
INNER JOIN ventas ON productos.id = ventas.producto_id;
-- ¿Cuál "nombre" es cuál?

-- ✅ BIEN (con alias claros)
SELECT
    p.nombre AS producto,
    c.nombre AS categoria,
    v.cantidad
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
INNER JOIN ventas v ON p.id = v.producto_id;
```

---

### Error 4: Subconsulta en SELECT Devuelve Múltiples Filas

**Problema:** Una subconsulta en SELECT debe devolver UN SOLO valor por fila.

```sql
-- ❌ MAL (subconsulta devuelve múltiples filas)
SELECT
    p.nombre,
    (SELECT v.total FROM ventas v WHERE v.producto_id = p.id) AS total_ventas
FROM productos p;
-- Error: subquery devuelve más de 1 fila

-- ✅ BIEN (usa agregación)
SELECT
    p.nombre,
    (SELECT SUM(v.total) FROM ventas v WHERE v.producto_id = p.id) AS total_ventas
FROM productos p;
```

---

### Error 5: Olvidar ELSE en CASE WHEN

**Problema:** Si ninguna condición se cumple, devuelve NULL (puede no ser lo que quieres).

```sql
-- ❌ MAL (sin ELSE)
SELECT
    nombre,
    CASE
        WHEN precio < 50 THEN 'Económico'
        WHEN precio > 200 THEN 'Premium'
    END AS rango
FROM productos;
-- Productos entre $50-$200 → NULL

-- ✅ BIEN (con ELSE)
SELECT
    nombre,
    CASE
        WHEN precio < 50 THEN 'Económico'
        WHEN precio > 200 THEN 'Premium'
        ELSE 'Medio'  -- Valor por defecto
    END AS rango
FROM productos;
```

---

## Buenas Prácticas

### 1. Usa JOIN explícito, no el viejo estilo

```sql
-- ❌ Viejo estilo (confuso)
SELECT *
FROM productos, categorias
WHERE productos.categoria_id = categorias.id;

-- ✅ Estilo moderno (claro)
SELECT *
FROM productos
INNER JOIN categorias ON productos.categoria_id = categorias.id;
```

### 2. Siempre usa alias con tablas múltiples

```sql
-- Hace el código más legible y evita ambigüedades
SELECT
    p.nombre AS producto,
    c.nombre AS categoria
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id;
```

### 3. Ordena JOINs de lo general a lo específico

```sql
-- ✅ Lógico: cliente → pedido → detalle
SELECT ...
FROM clientes c
INNER JOIN pedidos p ON c.id = p.cliente_id
INNER JOIN detalles_pedido dp ON p.id = dp.pedido_id;
```

### 4. Comenta queries complejas

```sql
-- Reporte de ventas por categoría (últimos 30 días)
-- Incluye productos sin ventas para análisis
SELECT
    c.nombre AS categoria,
    COALESCE(SUM(v.total), 0) AS ingresos
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id
LEFT JOIN ventas v ON p.id = v.producto_id AND v.fecha >= DATE('now', '-30 days')
GROUP BY c.nombre;
```

### 5. Usa COALESCE para manejar NULLs de LEFT JOIN

```sql
SELECT
    p.nombre,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.nombre;
```

---

## Checklist de Aprendizaje

Completa este checklist para asegurarte de que dominas SQL Intermedio:

- [ ] Entiendo la diferencia entre INNER, LEFT, RIGHT y FULL JOIN
- [ ] Puedo explicar con mis propias palabras qué hace cada tipo de JOIN
- [ ] Sé cuándo usar LEFT JOIN vs INNER JOIN
- [ ] Puedo escribir queries con 3+ tablas usando JOINs
- [ ] Entiendo qué es un producto cartesiano y cómo evitarlo
- [ ] Puedo usar subconsultas en WHERE, FROM y SELECT
- [ ] Sé cuándo usar subconsulta vs JOIN
- [ ] Puedo usar CASE WHEN para categorizar datos
- [ ] Entiendo la diferencia entre WHERE y HAVING con JOINs
- [ ] Puedo identificar y corregir los 5 errores comunes mencionados
- [ ] He practicado con los ejemplos del archivo 02-EJEMPLOS.md
- [ ] He resuelto al menos 10 de los 15 ejercicios del archivo 03-EJERCICIOS.md

---

## Recursos Adicionales

### Documentación Oficial
- [SQLite JOINS](https://www.sqlitetutorial.net/sqlite-join/)
- [PostgreSQL JOINS](https://www.postgresql.org/docs/current/tutorial-join.html)
- [W3Schools SQL JOIN](https://www.w3schools.com/sql/sql_join.asp)

### Visualización de JOINs
- [Visual JOIN Guide](https://joins.spathon.com/) - Diagramas interactivos
- [SQL Joins Explained](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins) - Diagramas de Venn

### Práctica Interactiva
- [SQLZoo JOINs Tutorial](https://sqlzoo.net/wiki/The_JOIN_operation)
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/sql-joins/)
- [LeetCode SQL Problems](https://leetcode.com/problemset/database/) - Filtra por "JOIN"

---

**¡Felicidades!** 🎉 Has completado la teoría de SQL Intermedio. Ahora es momento de practicar con ejemplos reales en `02-EJEMPLOS.md`.

**Siguiente paso:** Abre `02-EJEMPLOS.md` y trabaja los 5 ejemplos paso a paso para consolidar tu aprendizaje.

---

**Última actualización:** 2025-10-25
**Tiempo estimado de lectura:** 30-45 minutos
**Nivel:** Intermedio
---

## 🧭 Navegación

⬅️ **Anterior**: [SQL Básico - Proyecto Práctico](../tema-1-sql-basico/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
