# Ejercicios Prácticos: SQL Intermedio

> **Instrucciones:** Intenta resolver cada ejercicio por tu cuenta antes de ver la solución. Usa la base de datos de TechStore creada en `02-EJEMPLOS.md`.

> **Tip:** Si te atascas, revisa la sección de **Ayuda** antes de ver la solución completa.

---

## 📋 Preparación

Asegúrate de haber ejecutado los scripts de creación de tablas del archivo `02-EJEMPLOS.md` antes de comenzar.

---

## Ejercicios Básicos (1-5)

### Ejercicio 1: Listar Productos con Precio de Categoría

**Dificultad:** ⭐ Fácil
**Conceptos:** INNER JOIN, agregación

**Contexto:**
El equipo de pricing de TechStore necesita comparar el precio de cada producto con el precio promedio de su categoría para identificar productos que están por encima o por debajo del promedio.

**Datos:**
Usa las tablas `productos` y `categorias`.

**Tu tarea:**
Escribe una query que muestre:
- Nombre del producto
- Categoría
- Precio del producto
- Precio promedio de la categoría (con 2 decimales)

**Ayuda:**
- Necesitarás un JOIN entre productos y categorías
- Usa una subconsulta en SELECT o un self-join con GROUP BY

---

### Ejercicio 2: Clientes que Han Comprado en Últimos 60 Días

**Dificultad:** ⭐ Fácil
**Conceptos:** INNER JOIN, filtros de fecha

**Contexto:**
Marketing quiere enviar una encuesta de satisfacción solo a clientes que compraron recientemente (últimos 60 días).

**Datos:**
Usa las tablas `clientes` y `ventas`.

**Tu tarea:**
Lista de clientes únicos que han comprado en los últimos 60 días, mostrando:
- Nombre del cliente
- Email
- Fecha de última compra
- Total gastado en ese período

**Ayuda:**
- Usa `DATE('now', '-60 days')` para calcular la fecha límite
- Agrupa por cliente para evitar duplicados
- Usa `MAX(fecha)` para la última compra

---

### Ejercicio 3: Productos Sin Ventas

**Dificultad:** ⭐ Fácil
**Conceptos:** LEFT JOIN, IS NULL

**Contexto:**
El gerente de inventario quiere identificar productos activos que nunca se han vendido para evaluar si deben descontinuarse o necesitan promoción.

**Datos:**
Usa las tablas `productos` y `ventas`.

**Tu tarea:**
Lista productos activos que NO tienen ninguna venta registrada:
- Nombre del producto
- Categoría (usa JOIN con categorías)
- Precio
- Stock actual

**Ayuda:**
- LEFT JOIN desde productos hacia ventas
- Filtra con `WHERE ventas.id IS NULL`
- No olvides el filtro `activo = 1`

---

### Ejercicio 4: Categorías Ordenadas por Ingresos

**Dificultad:** ⭐ Fácil
**Conceptos:** INNER JOIN múltiple, agregación, ORDER BY

**Contexto:**
El CFO necesita un reporte simple de qué categorías generan más ingresos para priorizar inventario.

**Datos:**
Usa `categorias`, `productos` y `ventas`.

**Tu tarea:**
Muestra categorías ordenadas por ingresos totales (de mayor a menor):
- Nombre de categoría
- Ingresos totales
- Número de productos vendidos (suma de cantidades)

**Ayuda:**
- Une las 3 tablas: categorias → productos → ventas
- Usa `SUM(ventas.total)` y `SUM(ventas.cantidad)`
- Agrupa por categoría

---

### Ejercicio 5: Top 3 Productos Más Vendidos

**Dificultad:** ⭐ Fácil
**Conceptos:** INNER JOIN, agregación, LIMIT

**Contexto:**
El equipo de compras quiere saber qué 3 productos se venden más (por cantidad de unidades) para priorizar reabastecimiento.

**Datos:**
Usa `productos` y `ventas`.

**Tu tarea:**
Lista los 3 productos más vendidos:
- Nombre del producto
- Unidades vendidas (suma de cantidad)
- Ingresos generados
- Stock actual

**Ayuda:**
- Agrupa por producto
- Ordena por `SUM(cantidad) DESC`
- Usa `LIMIT 3`

---

## Ejercicios Intermedios (6-10)

### Ejercicio 6: Subconsulta para Productos Caros

**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Subconsulta en WHERE

**Contexto:**
El equipo de marketing quiere crear una campaña premium dirigida solo a productos que cuestan más del doble del precio promedio.

**Datos:**
Usa la tabla `productos`.

**Tu tarea:**
Lista productos cuyo precio sea mayor a 2 veces el precio promedio de TODOS los productos:
- Nombre del producto
- Precio
- Precio promedio general (como columna de referencia)
- Diferencia entre precio del producto y promedio

**Ayuda:**
- Usa una subconsulta en WHERE: `WHERE precio > (SELECT AVG(precio) * 2 FROM productos)`
- Usa otra subconsulta en SELECT para mostrar el promedio

---

### Ejercicio 7: Clientes con Gasto Promedio Alto

**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Subconsulta en HAVING

**Contexto:**
El programa de lealtad quiere identificar clientes cuyo ticket promedio sea superior al ticket promedio general para darles beneficios especiales.

**Datos:**
Usa `clientes` y `ventas`.

**Tu tarea:**
Lista clientes cuyo ticket promedio (gasto promedio por pedido) sea mayor al ticket promedio de todos los clientes:
- Nombre del cliente
- Número de pedidos
- Ticket promedio del cliente
- Ticket promedio general (columna de referencia)

**Ayuda:**
- Calcula ticket promedio por cliente: `AVG(total)`
- Usa subconsulta en HAVING: `HAVING AVG(total) > (SELECT AVG(total) FROM ventas)`
- Agrupa por cliente

---

### Ejercicio 8: Clasificación de Stock con CASE WHEN

**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** CASE WHEN, múltiples condiciones

**Contexto:**
El sistema de alertas de TechStore necesita clasificar productos en 4 niveles según su stock y generar recomendaciones automáticas.

**Datos:**
Usa `productos` y `categorias`.

**Tu tarea:**
Crea una clasificación con estas reglas:
- Stock = 0 → "Agotado"
- Stock 1-10 → "Crítico"
- Stock 11-30 → "Bajo"
- Stock 31-50 → "Óptimo"
- Stock > 50 → "Exceso"

Muestra:
- Nombre del producto
- Categoría
- Stock actual
- Clasificación
- Recomendación (columna calculada):
  - Agotado/Crítico → "Reabastecer urgente"
  - Bajo → "Monitorear"
  - Óptimo → "OK"
  - Exceso → "Reducir órdenes"

**Ayuda:**
- Usa dos columnas con CASE WHEN (una para clasificación, otra para recomendación)
- Ordena por nivel de urgencia (Agotado primero)

---

### Ejercicio 9: RIGHT JOIN (o LEFT JOIN Invertido)

**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** RIGHT JOIN o LEFT JOIN

**Contexto:**
Auditoría encontró inconsistencias: hay ventas registradas pero los productos correspondientes fueron eliminados de la base de datos. Necesitas identificar estas ventas "huérfanas".

**Datos:**
Usa `ventas` y `productos`.

**Tu tarea:**
Encuentra ventas que NO tienen un producto correspondiente (producto fue eliminado):
- ID de venta
- ID de producto (de la venta)
- Fecha de venta
- Total de venta

**Ayuda:**
- Usa LEFT JOIN desde ventas hacia productos
- Filtra con `WHERE productos.id IS NULL`
- Esto mostrará ventas sin producto asociado

**Nota:** Si usas la base de datos limpia de los ejemplos, no habrá resultados (es correcto). Puedes insertar una venta con producto_id = 999 para probar:
```sql
INSERT INTO ventas (id, cliente_id, producto_id, cantidad, fecha, total)
VALUES (999, 1, 999, 1, '2025-01-01', 100.00);
```

---

### Ejercicio 10: Análisis de Tendencia con CASE WHEN

**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** CASE WHEN, agregación por fecha

**Contexto:**
El equipo de analytics quiere ver la distribución de ventas por mes para identificar temporalidad.

**Datos:**
Usa `ventas`.

**Tu tarea:**
Agrupa ventas por mes usando CASE WHEN (sin usar funciones de fecha avanzadas):
- Mes (extraído de fecha)
- Número de transacciones
- Ingresos totales
- Clasificación del mes:
  - Ingresos > $1,000 → "Mes fuerte"
  - Ingresos $500-$1,000 → "Mes regular"
  - Ingresos < $500 → "Mes débil"

**Ayuda:**
- Usa `STRFTIME('%m', fecha)` para extraer mes
- Agrupa por mes
- Usa CASE WHEN en la columna de clasificación

---

## Ejercicios Avanzados (11-15)

### Ejercicio 11: Análisis de Productos por Rendimiento Multi-Dimensional

**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** JOIN múltiple, subconsultas, CASE WHEN combinado

**Contexto:**
El CEO quiere un dashboard que clasifique productos en una matriz 2x2:
- Eje X: Margen (alto/bajo) basado en precio
- Eje Y: Volumen de ventas (alto/bajo)

Esto ayudará a identificar:
- **Estrellas**: Alto margen + Alto volumen
- **Vacas lecheras**: Bajo margen + Alto volumen
- **Interrogantes**: Alto margen + Bajo volumen
- **Perros**: Bajo margen + Bajo volumen

**Datos:**
Usa `productos`, `categorias` y `ventas`.

**Tu tarea:**
Clasifica productos en la matriz BCG simplificada:
- Nombre del producto
- Categoría
- Precio (proxy de margen)
- Unidades vendidas
- Ingresos totales
- Clasificación:
  - Precio > promedio Y unidades > promedio → "Estrella"
  - Precio ≤ promedio Y unidades > promedio → "Vaca lechera"
  - Precio > promedio Y unidades ≤ promedio → "Interrogante"
  - Precio ≤ promedio Y unidades ≤ promedio → "Perro"

**Ayuda:**
- Usa CTEs (WITH) para calcular promedios primero
- Usa CASE WHEN anidado para la clasificación
- Ejemplo de estructura:
```sql
WITH promedios AS (
    SELECT AVG(precio) AS precio_promedio,
           AVG(cantidad_total) AS volumen_promedio
    FROM ...
)
SELECT ..., CASE WHEN ... THEN ... END
```

---

### Ejercicio 12: Cohorte de Clientes por Mes de Registro

**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** JOIN, GROUP BY complejo, subconsultas

**Contexto:**
El equipo de growth quiere analizar cohortes: ¿Los clientes que se registraron en enero gastan más que los de febrero? Esto ayudará a evaluar la calidad de las campañas de adquisición por mes.

**Datos:**
Usa `clientes` y `ventas`.

**Tu tarea:**
Análisis de cohortes por mes de registro:
- Mes de registro (formato YYYY-MM)
- Número de clientes registrados en ese mes
- Número de clientes que hicieron al menos 1 compra
- Tasa de conversión (%)
- Gasto promedio por cliente registrado (incluyendo los que no compraron = $0)
- Gasto promedio por cliente activo (solo los que compraron)

**Ayuda:**
- Extrae mes de registro con `STRFTIME('%Y-%m', fecha_registro)`
- Usa LEFT JOIN para incluir clientes sin compras
- Usa CASE WHEN para contar clientes activos
- Calcula tasas con `COUNT(DISTINCT ...) * 100.0 / COUNT(*)`

---

### Ejercicio 13: Detección de Oportunidades de Cross-Selling

**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Self-JOIN, subconsultas complejas

**Contexto:**
Marketing quiere identificar clientes que compraron laptops pero NO compraron accesorios (mouse, teclado, webcam) para enviarles una campaña de cross-selling.

**Datos:**
Usa `clientes`, `ventas`, `productos` y `categorias`.

**Tu tarea:**
Lista de clientes que:
- Compraron al menos 1 producto de categoría "Computadoras"
- NO compraron ningún producto de categoría "Accesorios"

Muestra:
- Nombre del cliente
- Email
- Laptop(s) comprada(s)
- Total gastado en computadoras
- Mensaje sugerido: "¡Completa tu setup con un mouse y teclado!"

**Ayuda:**
- Usa dos subconsultas:
  - Una para clientes que compraron Computadoras
  - Otra para clientes que compraron Accesorios
- Usa `NOT IN` o `NOT EXISTS` para la exclusión
- Ejemplo de estructura:
```sql
SELECT ...
FROM clientes c
WHERE c.id IN (SELECT cliente_id FROM ... WHERE categoria = 'Computadoras')
  AND c.id NOT IN (SELECT cliente_id FROM ... WHERE categoria = 'Accesorios')
```

---

### Ejercicio 14: Análisis de Retención (Clientes Recurrentes)

**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Self-JOIN, fechas, subconsultas

**Contexto:**
El equipo de CRM quiere medir la retención: ¿Cuántos clientes que compraron en enero volvieron a comprar en febrero? ¿Y en marzo? Esto se llama "análisis de retención mensual".

**Datos:**
Usa `clientes` y `ventas`.

**Tu tarea:**
Crea un reporte de retención por mes:
- Mes (formato YYYY-MM)
- Clientes que compraron ese mes (únicos)
- Clientes que volvieron a comprar el mes siguiente (retención)
- Tasa de retención (%)

**Ayuda:**
- Esta query es compleja, usa CTEs (WITH)
- Identifica clientes por mes
- Usa self-join de ventas para comparar mes N con mes N+1
- Ejemplo conceptual:
```sql
WITH ventas_mensuales AS (
    SELECT DISTINCT cliente_id, STRFTIME('%Y-%m', fecha) AS mes
    FROM ventas
)
SELECT
    vm1.mes,
    COUNT(DISTINCT vm1.cliente_id) AS clientes,
    COUNT(DISTINCT vm2.cliente_id) AS retornaron
FROM ventas_mensuales vm1
LEFT JOIN ventas_mensuales vm2
    ON vm1.cliente_id = vm2.cliente_id
    AND vm2.mes = DATE(vm1.mes || '-01', '+1 month')
GROUP BY vm1.mes
```

---

### Ejercicio 15: Reporte Ejecutivo Multi-Dimensional

**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** JOIN múltiple (4+ tablas), CTEs, subconsultas, agregaciones complejas

**Contexto:**
El board de directores quiere un reporte ÚNICO que responda estas 5 preguntas simultáneamente:
1. ¿Cuál es la categoría más rentable?
2. ¿Qué ciudad genera más ingresos?
3. ¿Cuántos clientes VIP tenemos? (>$1,000 gastados)
4. ¿Cuál es la tasa de conversión general?
5. ¿Cuál es el ticket promedio por transacción?

**Datos:**
Usa todas las tablas: `clientes`, `ventas`, `productos`, `categorias`.

**Tu tarea:**
Crea un reporte ejecutivo con métricas clave:
- Categoría más rentable (nombre + ingresos)
- Ciudad con más ingresos (nombre + ingresos)
- Número de clientes VIP
- Tasa de conversión (clientes con compras / clientes totales × 100%)
- Ticket promedio general
- Ingreso total de toda la empresa

**Ayuda:**
- Usa múltiples CTEs (WITH) para calcular cada métrica por separado
- Luego combínalas con CROSS JOIN o UNION ALL
- Estructura sugerida:
```sql
WITH
categoria_top AS (
    SELECT ... LIMIT 1
),
ciudad_top AS (
    SELECT ... LIMIT 1
),
metricas AS (
    SELECT ...
)
SELECT
    categoria_top.*,
    ciudad_top.*,
    metricas.*
FROM categoria_top
CROSS JOIN ciudad_top
CROSS JOIN metricas;
```

---

## Soluciones

### Solución Ejercicio 1

```sql
-- Productos con precio promedio de su categoría

SELECT
    p.nombre AS producto,
    c.nombre AS categoria,
    p.precio AS precio_producto,
    ROUND(AVG(p2.precio), 2) AS precio_promedio_categoria
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
INNER JOIN productos p2 ON p.categoria_id = p2.categoria_id
WHERE p.activo = 1
GROUP BY p.id, p.nombre, c.nombre, p.precio
ORDER BY c.nombre, p.precio DESC;
```

**Explicación:**
- Self-join de productos (p2) para calcular promedio por categoría
- GROUP BY incluye p.id para agregar correctamente
- Resultado muestra si un producto está por encima o por debajo del promedio de su categoría

**Resultado esperado:**
```
| producto         | categoria      | precio_producto | precio_promedio_categoria |
| ---------------- | -------------- | --------------- | ------------------------- |
| Bocina Bluetooth | Audio          | 89.99           | 144.99                    |
| Audífonos Sony   | Audio          | 199.99          | 144.99                    |
| SSD 1TB Samsung  | Almacenamiento | 149.99          | 119.99                    |
| Disco Duro 2TB   | Almacenamiento | 89.99           | 119.99                    |
```

---

### Solución Ejercicio 2

```sql
-- Clientes con compras en últimos 60 días

SELECT
    c.nombre,
    c.email,
    MAX(v.fecha) AS ultima_compra,
    ROUND(SUM(v.total), 2) AS total_gastado
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
WHERE v.fecha >= DATE('now', '-60 days')
GROUP BY c.id, c.nombre, c.email
ORDER BY ultima_compra DESC;
```

**Explicación:**
- INNER JOIN porque solo queremos clientes con compras
- DATE('now', '-60 days') calcula la fecha límite dinámicamente
- MAX(fecha) obtiene la compra más reciente por cliente
- GROUP BY cliente para evitar duplicados

**Resultado esperado:**
Dependiendo de la fecha actual, puede no haber resultados si todas las ventas son antiguas. Para probar, modifica el filtro a `-360 days`.

---

### Solución Ejercicio 3

```sql
-- Productos activos sin ventas

SELECT
    p.nombre AS producto,
    c.nombre AS categoria,
    p.precio,
    p.stock
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN ventas v ON p.id = v.producto_id
WHERE p.activo = 1
  AND v.id IS NULL
ORDER BY p.stock DESC;
```

**Explicación:**
- LEFT JOIN desde productos hacia ventas
- WHERE v.id IS NULL identifica productos sin ventas
- Solo productos activos (activo = 1)
- Ordenado por stock para ver primero productos con más inventario inmovilizado

**Resultado esperado:**
```
| producto                                                                         | categoria | precio | stock |
| -------------------------------------------------------------------------------- | --------- | ------ | ----- |
| (Sin resultados en base limpia - todos los productos han vendido al menos 1 vez) |
```

---

### Solución Ejercicio 4

```sql
-- Categorías ordenadas por ingresos

SELECT
    c.nombre AS categoria,
    ROUND(SUM(v.total), 2) AS ingresos_totales,
    SUM(v.cantidad) AS unidades_vendidas
FROM categorias c
INNER JOIN productos p ON c.id = p.categoria_id
INNER JOIN ventas v ON p.id = v.producto_id
GROUP BY c.id, c.nombre
ORDER BY ingresos_totales DESC;
```

**Explicación:**
- JOIN de 3 tablas: categorias → productos → ventas
- SUM(v.total) para ingresos totales
- SUM(v.cantidad) para unidades vendidas
- ORDER BY ingresos DESC muestra las más rentables primero

**Resultado esperado:**
```
| categoria      | ingresos_totales | unidades_vendidas |
| -------------- | ---------------- | ----------------- |
| Computadoras   | 2199.98          | 2                 |
| Accesorios     | 529.94           | 6                 |
| Almacenamiento | 389.97           | 4                 |
| Audio          | 289.98           | 2                 |
```

---

### Solución Ejercicio 5

```sql
-- Top 3 productos más vendidos

SELECT
    p.nombre AS producto,
    SUM(v.cantidad) AS unidades_vendidas,
    ROUND(SUM(v.total), 2) AS ingresos_generados,
    p.stock AS stock_actual
FROM productos p
INNER JOIN ventas v ON p.id = v.producto_id
GROUP BY p.id, p.nombre, p.stock
ORDER BY unidades_vendidas DESC
LIMIT 3;
```

**Explicación:**
- GROUP BY producto para sumar ventas
- ORDER BY unidades DESC para ordenar por volumen
- LIMIT 3 para solo los top 3

**Resultado esperado:**
```
| producto           | unidades_vendidas | ingresos_generados | stock_actual |
| ------------------ | ----------------- | ------------------ | ------------ |
| Mouse Logitech MX  | 5                 | 399.95             | 50           |
| SSD 1TB Samsung    | 2                 | 299.98             | 40           |
| Laptop HP Pavilion | 1                 | 899.99             | 15           |
```

---

### Solución Ejercicio 6

```sql
-- Productos caros (más de 2x el precio promedio)

SELECT
    p.nombre AS producto,
    p.precio,
    (SELECT ROUND(AVG(precio), 2) FROM productos WHERE activo = 1) AS precio_promedio_general,
    ROUND(p.precio - (SELECT AVG(precio) FROM productos WHERE activo = 1), 2) AS diferencia
FROM productos p
WHERE p.activo = 1
  AND p.precio > (SELECT AVG(precio) * 2 FROM productos WHERE activo = 1)
ORDER BY p.precio DESC;
```

**Explicación:**
- Subconsulta en WHERE para filtrar productos > 2 × promedio
- Subconsulta en SELECT para mostrar el promedio como referencia
- Diferencia calculada para ver cuánto más caro es

**Resultado esperado:**
```
| producto        | precio  | precio_promedio_general | diferencia |
| --------------- | ------- | ----------------------- | ---------- |
| Laptop Dell XPS | 1299.99 | 197.77                  | 1102.22    |
| Laptop HP       | 899.99  | 197.77                  | 702.22     |
```

---

### Solución Ejercicio 7

```sql
-- Clientes con ticket promedio alto

SELECT
    c.nombre AS cliente,
    COUNT(v.id) AS pedidos,
    ROUND(AVG(v.total), 2) AS ticket_promedio_cliente,
    (SELECT ROUND(AVG(total), 2) FROM ventas) AS ticket_promedio_general
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.id, c.nombre
HAVING AVG(v.total) > (SELECT AVG(total) FROM ventas)
ORDER BY ticket_promedio_cliente DESC;
```

**Explicación:**
- Subconsulta en HAVING para filtrar clientes con ticket > promedio
- AVG(v.total) calcula ticket promedio por cliente
- Solo clientes que superan el promedio general

**Resultado esperado:**
```
| cliente      | pedidos | ticket_promedio_cliente | ticket_promedio_general |
| ------------ | ------- | ----------------------- | ----------------------- |
| Carlos López | 3       | 529.99                  | 360.99                  |
| Ana García   | 4       | 302.49                  | 360.99                  |
```

---

### Solución Ejercicio 8

```sql
-- Clasificación de stock con recomendaciones

SELECT
    p.nombre AS producto,
    c.nombre AS categoria,
    p.stock,
    CASE
        WHEN p.stock = 0 THEN 'Agotado'
        WHEN p.stock BETWEEN 1 AND 10 THEN 'Crítico'
        WHEN p.stock BETWEEN 11 AND 30 THEN 'Bajo'
        WHEN p.stock BETWEEN 31 AND 50 THEN 'Óptimo'
        ELSE 'Exceso'
    END AS clasificacion,
    CASE
        WHEN p.stock <= 10 THEN 'Reabastecer urgente'
        WHEN p.stock BETWEEN 11 AND 30 THEN 'Monitorear'
        WHEN p.stock BETWEEN 31 AND 50 THEN 'OK'
        ELSE 'Reducir órdenes'
    END AS recomendacion
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = 1
ORDER BY
    CASE
        WHEN p.stock = 0 THEN 1
        WHEN p.stock BETWEEN 1 AND 10 THEN 2
        WHEN p.stock BETWEEN 11 AND 30 THEN 3
        WHEN p.stock BETWEEN 31 AND 50 THEN 4
        ELSE 5
    END,
    p.stock ASC;
```

**Explicación:**
- Dos columnas con CASE WHEN: una para clasificación, otra para recomendación
- ORDER BY con CASE WHEN prioriza productos urgentes primero
- Lógica de negocio implementada directamente en SQL

**Resultado esperado:**
```
| producto           | categoria    | stock | clasificacion | recomendacion       |
| ------------------ | ------------ | ----- | ------------- | ------------------- |
| Laptop Dell XPS    | Computadoras | 8     | Crítico       | Reabastecer urgente |
| Laptop HP Pavilion | Computadoras | 15    | Bajo          | Monitorear          |
| Audífonos Sony     | Audio        | 20    | Bajo          | Monitorear          |
```

---

### Solución Ejercicio 9

```sql
-- Ventas huérfanas (sin producto correspondiente)

SELECT
    v.id AS venta_id,
    v.producto_id,
    v.fecha,
    v.total
FROM ventas v
LEFT JOIN productos p ON v.producto_id = p.id
WHERE p.id IS NULL;
```

**Explicación:**
- LEFT JOIN desde ventas hacia productos
- WHERE p.id IS NULL identifica ventas sin producto
- En una base de datos limpia, no habrá resultados

**Para probar, inserta una venta huérfana:**
```sql
INSERT INTO ventas (id, cliente_id, producto_id, cantidad, fecha, total)
VALUES (999, 1, 999, 1, '2025-01-01', 100.00);

-- Ahora ejecuta la query anterior
```

**Resultado esperado (después de insertar venta de prueba):**
```
| venta_id | producto_id | fecha      | total  |
| -------- | ----------- | ---------- | ------ |
| 999      | 999         | 2025-01-01 | 100.00 |
```

---

### Solución Ejercicio 10

```sql
-- Análisis de ventas por mes

SELECT
    STRFTIME('%Y-%m', fecha) AS mes,
    COUNT(*) AS transacciones,
    ROUND(SUM(total), 2) AS ingresos_totales,
    CASE
        WHEN SUM(total) > 1000 THEN 'Mes fuerte'
        WHEN SUM(total) BETWEEN 500 AND 1000 THEN 'Mes regular'
        ELSE 'Mes débil'
    END AS clasificacion
FROM ventas
GROUP BY mes
ORDER BY mes;
```

**Explicación:**
- STRFTIME('%Y-%m', fecha) extrae año-mes
- GROUP BY mes para agregar ventas mensuales
- CASE WHEN clasifica meses según ingresos

**Resultado esperado:**
```
| mes     | transacciones | ingresos_totales | clasificacion |
| ------- | ------------- | ---------------- | ------------- |
| 2025-01 | 4             | 2559.95          | Mes fuerte    |
| 2025-02 | 4             | 759.93           | Mes regular   |
| 2025-03 | 2             | 149.98           | Mes débil     |
```

---

### Solución Ejercicio 11

```sql
-- Matriz BCG de productos

WITH promedios AS (
    SELECT
        AVG(p.precio) AS precio_promedio,
        AVG(ventas_por_producto.unidades) AS volumen_promedio
    FROM productos p
    CROSS JOIN (
        SELECT AVG(cantidad_total) AS unidades
        FROM (
            SELECT producto_id, SUM(cantidad) AS cantidad_total
            FROM ventas
            GROUP BY producto_id
        )
    ) AS ventas_por_producto
    WHERE p.activo = 1
),
productos_con_ventas AS (
    SELECT
        p.id,
        p.nombre,
        c.nombre AS categoria,
        p.precio,
        COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
        COALESCE(SUM(v.total), 0) AS ingresos_totales
    FROM productos p
    INNER JOIN categorias c ON p.categoria_id = c.id
    LEFT JOIN ventas v ON p.id = v.producto_id
    WHERE p.activo = 1
    GROUP BY p.id, p.nombre, c.nombre, p.precio
)
SELECT
    pcv.nombre AS producto,
    pcv.categoria,
    pcv.precio,
    pcv.unidades_vendidas,
    ROUND(pcv.ingresos_totales, 2) AS ingresos_totales,
    CASE
        WHEN pcv.precio > pr.precio_promedio AND pcv.unidades_vendidas > pr.volumen_promedio
            THEN 'Estrella'
        WHEN pcv.precio <= pr.precio_promedio AND pcv.unidades_vendidas > pr.volumen_promedio
            THEN 'Vaca lechera'
        WHEN pcv.precio > pr.precio_promedio AND pcv.unidades_vendidas <= pr.volumen_promedio
            THEN 'Interrogante'
        ELSE 'Perro'
    END AS clasificacion_bcg
FROM productos_con_ventas pcv
CROSS JOIN promedios pr
ORDER BY
    CASE clasificacion_bcg
        WHEN 'Estrella' THEN 1
        WHEN 'Vaca lechera' THEN 2
        WHEN 'Interrogante' THEN 3
        ELSE 4
    END,
    pcv.ingresos_totales DESC;
```

**Explicación:**
- CTE `promedios` calcula precio promedio y volumen promedio
- CTE `productos_con_ventas` prepara datos de productos con ventas
- CASE WHEN anidado clasifica productos en matriz 2x2
- Ordenado por prioridad estratégica (Estrellas primero)

**Resultado esperado:**
```
| producto          | categoria    | precio  | unidades_vendidas | ingresos_totales | clasificacion_bcg |
| ----------------- | ------------ | ------- | ----------------- | ---------------- | ----------------- |
| Laptop Dell XPS   | Computadoras | 1299.99 | 1                 | 1299.99          | Interrogante      |
| Mouse Logitech MX | Accesorios   | 79.99   | 5                 | 399.95           | Vaca lechera      |
```

---

### Solución Ejercicio 12

```sql
-- Análisis de cohortes por mes de registro

SELECT
    STRFTIME('%Y-%m', c.fecha_registro) AS mes_registro,
    COUNT(DISTINCT c.id) AS clientes_registrados,
    COUNT(DISTINCT CASE WHEN v.id IS NOT NULL THEN c.id END) AS clientes_activos,
    ROUND(COUNT(DISTINCT CASE WHEN v.id IS NOT NULL THEN c.id END) * 100.0 / COUNT(DISTINCT c.id), 2) AS tasa_conversion,
    ROUND(COALESCE(SUM(v.total), 0) / COUNT(DISTINCT c.id), 2) AS gasto_promedio_registrado,
    ROUND(AVG(CASE WHEN v.id IS NOT NULL THEN gasto_por_cliente END), 2) AS gasto_promedio_activo
FROM clientes c
LEFT JOIN (
    SELECT cliente_id, SUM(total) AS gasto_por_cliente
    FROM ventas
    GROUP BY cliente_id
) AS v ON c.id = v.cliente_id
GROUP BY mes_registro
ORDER BY mes_registro;
```

**Explicación:**
- Extrae mes de registro con STRFTIME
- LEFT JOIN para incluir clientes sin compras
- CASE WHEN cuenta solo clientes activos
- Dos tipos de gasto promedio: uno incluye clientes inactivos ($0), otro solo activos

**Resultado esperado:**
```
| mes_registro | clientes_registrados | clientes_activos | tasa_conversion | gasto_promedio_registrado | gasto_promedio_activo |
| ------------ | -------------------- | ---------------- | --------------- | ------------------------- | --------------------- |
| 2024-01      | 1                    | 1                | 100.00          | 1210.94                   | 1210.94               |
| 2024-02      | 1                    | 1                | 100.00          | 1589.97                   | 1589.97               |
| 2024-03      | 1                    | 1                | 100.00          | 429.97                    | 429.97                |
| 2024-04      | 1                    | 1                | 100.00          | 239.97                    | 239.97                |
| 2024-10      | 1                    | 0                | 0.00            | 0.00                      | NULL                  |
```

---

### Solución Ejercicio 13

```sql
-- Oportunidades de cross-selling (compraron laptops pero no accesorios)

SELECT
    c.nombre AS cliente,
    c.email,
    GROUP_CONCAT(p.nombre, ', ') AS laptops_compradas,
    ROUND(SUM(v.total), 2) AS gastado_en_computadoras,
    '¡Completa tu setup con un mouse y teclado!' AS mensaje_sugerido
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
INNER JOIN productos p ON v.producto_id = p.id
INNER JOIN categorias cat ON p.categoria_id = cat.id
WHERE cat.nombre = 'Computadoras'
  AND c.id NOT IN (
      SELECT DISTINCT v2.cliente_id
      FROM ventas v2
      INNER JOIN productos p2 ON v2.producto_id = p2.id
      INNER JOIN categorias cat2 ON p2.categoria_id = cat2.id
      WHERE cat2.nombre = 'Accesorios'
  )
GROUP BY c.id, c.nombre, c.email
ORDER BY gastado_en_computadoras DESC;
```

**Explicación:**
- JOIN para obtener clientes que compraron Computadoras
- Subconsulta NOT IN excluye clientes que compraron Accesorios
- GROUP_CONCAT lista productos comprados
- Mensaje personalizado de cross-selling

**Resultado esperado:**
```
| cliente      | email            | laptops_compradas | gastado_en_computadoras | mensaje_sugerido                           |
| ------------ | ---------------- | ----------------- | ----------------------- | ------------------------------------------ |
| Carlos López | carlos@email.com | Laptop Dell XPS   | 1299.99                 | ¡Completa tu setup con un mouse y teclado! |
```

---

### Solución Ejercicio 14

```sql
-- Análisis de retención mensual

WITH ventas_mensuales AS (
    SELECT DISTINCT
        cliente_id,
        STRFTIME('%Y-%m', fecha) AS mes
    FROM ventas
),
clientes_por_mes AS (
    SELECT
        mes,
        COUNT(DISTINCT cliente_id) AS clientes_compraron
    FROM ventas_mensuales
    GROUP BY mes
),
retornaron AS (
    SELECT
        vm1.mes,
        COUNT(DISTINCT vm2.cliente_id) AS clientes_retornaron
    FROM ventas_mensuales vm1
    LEFT JOIN ventas_mensuales vm2
        ON vm1.cliente_id = vm2.cliente_id
        AND vm2.mes = STRFTIME('%Y-%m', DATE(vm1.mes || '-01', '+1 month'))
    GROUP BY vm1.mes
)
SELECT
    cpm.mes,
    cpm.clientes_compraron,
    COALESCE(r.clientes_retornaron, 0) AS clientes_retornaron,
    ROUND(COALESCE(r.clientes_retornaron, 0) * 100.0 / cpm.clientes_compraron, 2) AS tasa_retencion
FROM clientes_por_mes cpm
LEFT JOIN retornaron r ON cpm.mes = r.mes
ORDER BY cpm.mes;
```

**Explicación:**
- CTE `ventas_mensuales` identifica clientes únicos por mes
- CTE `clientes_por_mes` cuenta clientes por mes
- CTE `retornaron` usa self-join para encontrar clientes que volvieron el mes siguiente
- Tasa de retención = (retornaron / compraron mes anterior) × 100%

**Resultado esperado:**
```
| mes     | clientes_compraron | clientes_retornaron | tasa_retencion |
| ------- | ------------------ | ------------------- | -------------- |
| 2025-01 | 2                  | 2                   | 100.00         |
| 2025-02 | 3                  | 1                   | 33.33          |
| 2025-03 | 2                  | 0                   | 0.00           |
```

---

### Solución Ejercicio 15

```sql
-- Reporte ejecutivo multi-dimensional

WITH
categoria_top AS (
    SELECT
        'Categoría más rentable' AS metrica,
        c.nombre AS valor,
        ROUND(SUM(v.total), 2) AS monto
    FROM categorias c
    INNER JOIN productos p ON c.id = p.categoria_id
    INNER JOIN ventas v ON p.id = v.producto_id
    GROUP BY c.nombre
    ORDER BY monto DESC
    LIMIT 1
),
ciudad_top AS (
    SELECT
        'Ciudad con más ingresos' AS metrica,
        cl.ciudad AS valor,
        ROUND(SUM(v.total), 2) AS monto
    FROM clientes cl
    INNER JOIN ventas v ON cl.id = v.cliente_id
    GROUP BY cl.ciudad
    ORDER BY monto DESC
    LIMIT 1
),
clientes_vip AS (
    SELECT
        'Clientes VIP (>$1,000)' AS metrica,
        CAST(COUNT(DISTINCT cliente_id) AS TEXT) AS valor,
        NULL AS monto
    FROM (
        SELECT cliente_id, SUM(total) AS gasto_total
        FROM ventas
        GROUP BY cliente_id
        HAVING gasto_total > 1000
    )
),
tasa_conversion AS (
    SELECT
        'Tasa de conversión' AS metrica,
        ROUND(COUNT(DISTINCT v.cliente_id) * 100.0 / COUNT(DISTINCT c.id), 2) || '%' AS valor,
        NULL AS monto
    FROM clientes c
    LEFT JOIN ventas v ON c.id = v.cliente_id
),
ticket_promedio AS (
    SELECT
        'Ticket promedio' AS metrica,
        '$' || ROUND(AVG(total), 2) AS valor,
        ROUND(AVG(total), 2) AS monto
    FROM ventas
),
ingreso_total AS (
    SELECT
        'Ingreso total empresa' AS metrica,
        '$' || ROUND(SUM(total), 2) AS valor,
        ROUND(SUM(total), 2) AS monto
    FROM ventas
)
SELECT * FROM categoria_top
UNION ALL SELECT * FROM ciudad_top
UNION ALL SELECT * FROM clientes_vip
UNION ALL SELECT * FROM tasa_conversion
UNION ALL SELECT * FROM ticket_promedio
UNION ALL SELECT * FROM ingreso_total;
```

**Explicación:**
- 6 CTEs calculan cada métrica independientemente
- UNION ALL combina todas las métricas en un reporte unificado
- Formato consistente: metrica, valor, monto (NULL si no aplica)

**Resultado esperado:**
```
| metrica                 | valor        | monto   |
| ----------------------- | ------------ | ------- |
| Categoría más rentable  | Computadoras | 2199.98 |
| Ciudad con más ingresos | Barcelona    | 1589.97 |
| Clientes VIP (>$1,000)  | 2            | NULL    |
| Tasa de conversión      | 80.00%       | NULL    |
| Ticket promedio         | $360.99      | 360.99  |
| Ingreso total empresa   | $3609.87     | 3609.87 |
```

---

## Tabla de Autoevaluación

Marca cada ejercicio a medida que lo completes:

| Ejercicio | Título                               | Completado | Correcto | Notas |
| --------- | ------------------------------------ | ---------- | -------- | ----- |
| 1         | Productos con precio de categoría    | [ ]        | [ ]      |       |
| 2         | Clientes con compras recientes       | [ ]        | [ ]      |       |
| 3         | Productos sin ventas                 | [ ]        | [ ]      |       |
| 4         | Categorías por ingresos              | [ ]        | [ ]      |       |
| 5         | Top 3 productos más vendidos         | [ ]        | [ ]      |       |
| 6         | Subconsulta productos caros          | [ ]        | [ ]      |       |
| 7         | Clientes con ticket promedio alto    | [ ]        | [ ]      |       |
| 8         | Clasificación de stock con CASE WHEN | [ ]        | [ ]      |       |
| 9         | Ventas huérfanas (RIGHT JOIN)        | [ ]        | [ ]      |       |
| 10        | Análisis de tendencia por mes        | [ ]        | [ ]      |       |
| 11        | Matriz BCG de productos              | [ ]        | [ ]      |       |
| 12        | Cohortes de clientes                 | [ ]        | [ ]      |       |
| 13        | Oportunidades de cross-selling       | [ ]        | [ ]      |       |
| 14        | Análisis de retención                | [ ]        | [ ]      |       |
| 15        | Reporte ejecutivo multi-dimensional  | [ ]        | [ ]      |       |

---

## Criterios de Completitud

Has completado este tema cuando:

- [x] Resolviste al menos 12 de 15 ejercicios correctamente
- [x] Entiendes cuándo usar INNER JOIN vs LEFT JOIN
- [x] Puedes escribir subconsultas en WHERE, FROM y HAVING
- [x] Dominas CASE WHEN para categorización
- [x] Puedes unir 3+ tablas en queries complejas
- [x] Entiendes el orden de ejecución (FROM → WHERE → GROUP BY → HAVING)

---

## Próximos Pasos

1. **Proyecto práctico TDD**: `04-proyecto-practico/`
2. **Tema 3**: Optimización SQL (índices, EXPLAIN, performance)
3. **Práctica real**: Aplica estos conceptos en tus propios proyectos

---

**Última actualización:** 2025-10-25
**Tiempo estimado:** 4-6 horas (todos los ejercicios)
**Nivel:** Básico a Avanzado

---

**¡Felicidades!** 🎉 Has completado los ejercicios de SQL Intermedio. Ahora dominas JOINs, subconsultas y CASE WHEN como un profesional.
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
