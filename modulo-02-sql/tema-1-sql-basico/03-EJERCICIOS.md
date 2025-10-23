# Ejercicios Prácticos: SQL Básico

> **Instrucciones**: Intenta resolver cada ejercicio por tu cuenta antes de ver la solución. Usa las tablas de ejemplo del archivo `02-EJEMPLOS.md`. Si no las has creado aún, ejecuta los scripts SQL de ese archivo primero.

> **Consejo**: Escribe tus queries en un archivo `.sql` y ejecútalas en tu base de datos (SQLite o PostgreSQL) para verificar los resultados.

---

## 📊 Tablas Disponibles

Tienes acceso a dos tablas:

**`productos`**: 10 productos de TechStore
- Columnas: `id`, `nombre`, `precio`, `categoria`, `stock_actual`, `proveedor`

**`ventas`**: 10 transacciones de octubre 2025
- Columnas: `id`, `producto_id`, `cantidad`, `fecha`, `precio_unitario`

---

## Ejercicios Básicos (⭐ Fácil)

### Ejercicio 1: Listar Todos los Productos
**Dificultad**: ⭐ Fácil

**Contexto**:
Eres el nuevo Data Analyst de TechStore y necesitas familiarizarte con el catálogo de productos.

**Tu tarea**:
Escribe una query que muestre todos los productos con sus nombres y precios.

**Columnas esperadas**: `nombre`, `precio`

**Ayuda**:
Usa `SELECT` y `FROM`. No necesitas filtros.

---

### Ejercicio 2: Productos Caros
**Dificultad**: ⭐ Fácil

**Contexto**:
El gerente quiere enfocarse en productos premium para una campaña de marketing.

**Tu tarea**:
Lista todos los productos que cuestan más de $500, ordenados de más caro a más barato.

**Columnas esperadas**: `nombre`, `precio`, `categoria`

**Ayuda**:
Usa `WHERE` con el operador `>` y `ORDER BY DESC`.

---

### Ejercicio 3: Contar Productos por Proveedor
**Dificultad**: ⭐ Fácil

**Contexto**:
El equipo de compras quiere saber cuántos productos tenemos de cada proveedor.

**Tu tarea**:
Cuenta cuántos productos hay de cada proveedor, ordenados de mayor a menor.

**Columnas esperadas**: `proveedor`, `cantidad_productos`

**Ayuda**:
Usa `GROUP BY` con `COUNT(*)`.

---

### Ejercicio 4: Productos de Apple
**Dificultad**: ⭐ Fácil

**Contexto**:
El equipo de ventas quiere hacer una promoción especial de productos Apple.

**Tu tarea**:
Lista todos los productos del proveedor "Apple" con su nombre, precio y categoría.

**Columnas esperadas**: `nombre`, `precio`, `categoria`

**Ayuda**:
Usa `WHERE proveedor = 'Apple'`.

---

### Ejercicio 5: Precio Promedio de Accesorios
**Dificultad**: ⭐ Fácil

**Contexto**:
El gerente de categorías quiere saber el precio promedio de los accesorios.

**Tu tarea**:
Calcula el precio promedio de todos los productos en la categoría "Accesorios".

**Columnas esperadas**: `precio_promedio`

**Ayuda**:
Usa `AVG(precio)` con `WHERE categoria = 'Accesorios'`.

---

## Ejercicios Intermedios (⭐⭐ Intermedio)

### Ejercicio 6: Top 3 Categorías por Valor de Inventario
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
El CFO quiere saber qué categorías representan más valor en el inventario.

**Tu tarea**:
Calcula el valor total de inventario por categoría (precio × stock_actual) y muestra las top 3 categorías.

**Columnas esperadas**: `categoria`, `valor_inventario`

**Ayuda**:
Usa `SUM(precio * stock_actual)`, `GROUP BY`, `ORDER BY DESC` y `LIMIT 3`.

---

### Ejercicio 7: Productos con Stock Bajo
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
El equipo de logística necesita identificar productos con stock crítico para reordenar.

**Tu tarea**:
Lista todos los productos con menos de 20 unidades en stock, ordenados de menor a mayor stock.

**Columnas esperadas**: `nombre`, `categoria`, `stock_actual`, `proveedor`

**Ayuda**:
Usa `WHERE stock_actual < 20` y `ORDER BY stock_actual ASC`.

---

### Ejercicio 8: Ventas por Día
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
El equipo de ventas quiere analizar el patrón de ventas diarias de octubre.

**Tu tarea**:
Muestra cuántas transacciones y cuántas unidades se vendieron cada día, ordenadas por fecha.

**Columnas esperadas**: `fecha`, `transacciones`, `unidades_vendidas`

**Ayuda**:
Usa `GROUP BY fecha`, `COUNT(*)` y `SUM(cantidad)`.

---

### Ejercicio 9: Categorías con Más de 2 Productos
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
El gerente de producto quiere identificar categorías maduras (con múltiples productos).

**Tu tarea**:
Lista las categorías que tienen más de 2 productos, con el conteo de productos y precio promedio.

**Columnas esperadas**: `categoria`, `cantidad_productos`, `precio_promedio`

**Ayuda**:
Usa `GROUP BY categoria` con `HAVING COUNT(*) > 2`.

---

### Ejercicio 10: Ingresos Totales de Octubre
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
El equipo financiero necesita el reporte de ingresos del mes.

**Tu tarea**:
Calcula los ingresos totales de octubre 2025 (cantidad × precio_unitario).

**Columnas esperadas**: `ingresos_totales`

**Ayuda**:
Usa `SUM(cantidad * precio_unitario)` con `WHERE fecha >= '2025-10-01'`.

---

## Ejercicios Avanzados (⭐⭐⭐ Avanzado)

### Ejercicio 11: Análisis de Rentabilidad por Categoría
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
El CEO quiere entender qué categorías son más rentables considerando tanto ventas como inventario.

**Tu tarea**:
Para cada categoría, calcula:
- Cantidad de productos en catálogo
- Unidades vendidas en octubre
- Ingresos totales
- Porcentaje de ingresos sobre el total

Ordena por ingresos descendente.

**Columnas esperadas**: `categoria`, `productos`, `unidades_vendidas`, `ingresos`, `porcentaje_ingresos`

**Ayuda**:
Necesitarás una subconsulta o calcular el total de ingresos primero. Usa `LEFT JOIN` para incluir categorías sin ventas.

---

### Ejercicio 12: Productos Sin Ventas
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
El equipo de marketing quiere identificar productos que no se vendieron en octubre para crear promociones.

**Tu tarea**:
Lista todos los productos que NO tuvieron ventas en octubre, con su nombre, categoría y stock actual.

**Columnas esperadas**: `nombre`, `categoria`, `stock_actual`

**Ayuda**:
Usa `LEFT JOIN` entre `productos` y `ventas`, luego filtra donde `ventas.id IS NULL`.

---

### Ejercicio 13: Top 5 Días con Más Ingresos
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
El equipo de operaciones quiere identificar los días más exitosos para replicar estrategias.

**Tu tarea**:
Muestra los 5 días con mayores ingresos de octubre, incluyendo fecha, transacciones, unidades vendidas e ingresos.

**Columnas esperadas**: `fecha`, `transacciones`, `unidades`, `ingresos`

**Ayuda**:
Agrupa por fecha, calcula ingresos con `SUM(cantidad * precio_unitario)`, ordena y limita a 5.

---

### Ejercicio 14: Comparación de Performance de Proveedores
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
El gerente de compras quiere evaluar qué proveedores tienen productos más exitosos.

**Tu tarea**:
Para cada proveedor, calcula:
- Cantidad de productos en catálogo
- Unidades totales vendidas
- Ingresos totales
- Precio promedio de venta

Ordena por ingresos descendente.

**Columnas esperadas**: `proveedor`, `productos`, `unidades_vendidas`, `ingresos`, `precio_promedio_venta`

**Ayuda**:
Usa `LEFT JOIN`, `GROUP BY proveedor`, y calcula `ingresos / unidades` para el precio promedio.

---

### Ejercicio 15: Dashboard Ejecutivo Completo
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
El CEO necesita un reporte ejecutivo con las métricas más importantes del negocio.

**Tu tarea**:
Crea una query que devuelva:
- Total de productos en catálogo
- Total de categorías
- Valor total de inventario
- Transacciones de octubre
- Ingresos de octubre
- Ticket promedio (ingresos / transacciones)

**Columnas esperadas**: `metrica`, `valor`

**Ayuda**:
Usa `UNION ALL` para combinar múltiples queries en una sola tabla de resultados.

---

## Soluciones

### Solución Ejercicio 1

```sql
SELECT nombre, precio
FROM productos;
```

**Explicación**:
Query simple que selecciona dos columnas de la tabla productos. No requiere filtros ni ordenamiento.

**Resultado esperado**: 10 filas con todos los productos.

---

### Solución Ejercicio 2

```sql
SELECT nombre, precio, categoria
FROM productos
WHERE precio > 500
ORDER BY precio DESC;
```

**Explicación**:
Filtramos productos con precio mayor a $500 usando `WHERE`, y ordenamos de más caro a más barato con `ORDER BY precio DESC`.

**Resultado esperado**: 5 productos (MacBook Pro, Dell XPS, iPhone 15 Pro, Laptop HP, iPad Air).

---

### Solución Ejercicio 3

```sql
SELECT
    proveedor,
    COUNT(*) AS cantidad_productos
FROM productos
GROUP BY proveedor
ORDER BY cantidad_productos DESC;
```

**Explicación**:
Agrupamos por proveedor y contamos productos en cada grupo. Ordenamos de mayor a menor cantidad.

**Resultado esperado**:
- Apple: 4 productos
- Logitech: 2 productos
- HP Inc, Corsair, Samsung, Dell: 1 producto cada uno

---

### Solución Ejercicio 4

```sql
SELECT nombre, precio, categoria
FROM productos
WHERE proveedor = 'Apple';
```

**Explicación**:
Filtro simple por proveedor usando `WHERE` con igualdad.

**Resultado esperado**: 4 productos de Apple (MacBook Pro, iPhone 15 Pro, iPad Air, AirPods Pro).

---

### Solución Ejercicio 5

```sql
SELECT ROUND(AVG(precio), 2) AS precio_promedio
FROM productos
WHERE categoria = 'Accesorios';
```

**Explicación**:
Calculamos el promedio de precios solo para accesorios. Usamos `ROUND()` para 2 decimales.

**Resultado esperado**: $144.99

---

### Solución Ejercicio 6

```sql
SELECT
    categoria,
    ROUND(SUM(precio * stock_actual), 2) AS valor_inventario
FROM productos
GROUP BY categoria
ORDER BY valor_inventario DESC
LIMIT 3;
```

**Explicación**:
Calculamos el valor de inventario multiplicando precio por stock para cada producto, luego sumamos por categoría. Limitamos a top 3.

**Resultado esperado**:
1. Computadoras: $51,299.65
2. Smartphones: $29,999.75
3. Accesorios: $23,199.40

---

### Solución Ejercicio 7

```sql
SELECT nombre, categoria, stock_actual, proveedor
FROM productos
WHERE stock_actual < 20
ORDER BY stock_actual ASC;
```

**Explicación**:
Filtramos productos con menos de 20 unidades y ordenamos de menor a mayor stock.

**Resultado esperado**: 4 productos (MacBook Pro: 8, Dell XPS: 12, Laptop HP: 15, iPad Air: 18).

---

### Solución Ejercicio 8

```sql
SELECT
    fecha,
    COUNT(*) AS transacciones,
    SUM(cantidad) AS unidades_vendidas
FROM ventas
GROUP BY fecha
ORDER BY fecha;
```

**Explicación**:
Agrupamos ventas por fecha y contamos transacciones y sumamos unidades. Ordenamos cronológicamente.

**Resultado esperado**: 10 filas, una por cada día con ventas en octubre.

---

### Solución Ejercicio 9

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos,
    ROUND(AVG(precio), 2) AS precio_promedio
FROM productos
GROUP BY categoria
HAVING COUNT(*) > 2
ORDER BY cantidad_productos DESC;
```

**Explicación**:
Agrupamos por categoría, contamos productos y calculamos promedio. Usamos `HAVING` para filtrar grupos con más de 2 productos.

**Resultado esperado**:
- Accesorios: 4 productos, $144.99 promedio
- Computadoras: 3 productos, $1,466.66 promedio

---

### Solución Ejercicio 10

```sql
SELECT ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos_totales
FROM ventas
WHERE fecha >= '2025-10-01' AND fecha < '2025-11-01';
```

**Explicación**:
Multiplicamos cantidad por precio unitario para cada venta, sumamos todo, y filtramos por octubre.

**Resultado esperado**: $10,299.67

---

### Solución Ejercicio 11

```sql
SELECT
    p.categoria,
    COUNT(DISTINCT p.id) AS productos,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0), 2) AS ingresos,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0) * 100.0 /
          (SELECT SUM(cantidad * precio_unitario) FROM ventas), 2) AS porcentaje_ingresos
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.categoria
ORDER BY ingresos DESC;
```

**Explicación**:
Usamos `LEFT JOIN` para incluir categorías sin ventas. Calculamos porcentaje dividiendo ingresos de la categoría entre el total (subconsulta).

**Resultado esperado**:
- Computadoras: 60.2% de ingresos
- Accesorios: 17.0% de ingresos
- Smartphones: 11.7% de ingresos
- Monitores: 5.8% de ingresos
- Tablets: 0% de ingresos

---

### Solución Ejercicio 12

```sql
SELECT
    p.nombre,
    p.categoria,
    p.stock_actual
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
WHERE v.id IS NULL
ORDER BY p.categoria, p.nombre;
```

**Explicación**:
`LEFT JOIN` trae todos los productos. Los que no tienen ventas tendrán `NULL` en las columnas de ventas. Filtramos con `WHERE v.id IS NULL`.

**Resultado esperado**:
- Monitor Samsung 27"
- Teclado Mecánico Corsair
- iPad Air
- Webcam Logitech C920

---

### Solución Ejercicio 13

```sql
SELECT
    fecha,
    COUNT(*) AS transacciones,
    SUM(cantidad) AS unidades,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos
FROM ventas
GROUP BY fecha
ORDER BY ingresos DESC
LIMIT 5;
```

**Explicación**:
Agrupamos por fecha, calculamos métricas, ordenamos por ingresos descendente y limitamos a 5.

**Resultado esperado (top 5 días)**:
1. 2025-10-12: $1,999.99
2. 2025-10-01: $1,799.98
3. 2025-10-20: $1,499.99
4. 2025-10-05: $1,199.99
5. 2025-10-07: $999.96

---

### Solución Ejercicio 14

```sql
SELECT
    p.proveedor,
    COUNT(DISTINCT p.id) AS productos,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0), 2) AS ingresos,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0) /
          NULLIF(SUM(v.cantidad), 0), 2) AS precio_promedio_venta
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.proveedor
ORDER BY ingresos DESC;
```

**Explicación**:
Agrupamos por proveedor, usamos `LEFT JOIN` para incluir proveedores sin ventas. Calculamos precio promedio dividiendo ingresos entre unidades (usando `NULLIF` para evitar división por cero).

**Resultado esperado**:
- HP Inc: $2,699.97 ingresos, $899.99 precio promedio
- Apple: $2,199.95 ingresos, $366.66 precio promedio
- Dell: $1,499.99 ingresos, $1,499.99 precio promedio
- Logitech: $799.92 ingresos, $99.99 precio promedio
- Samsung: $599.98 ingresos, $299.99 precio promedio
- Corsair: $0 ingresos (sin ventas)

---

### Solución Ejercicio 15

```sql
SELECT 'Total Productos' AS metrica, COUNT(*) AS valor FROM productos
UNION ALL
SELECT 'Total Categorías', COUNT(DISTINCT categoria) FROM productos
UNION ALL
SELECT 'Valor Inventario', ROUND(SUM(precio * stock_actual), 2) FROM productos
UNION ALL
SELECT 'Transacciones Octubre', COUNT(*) FROM ventas WHERE fecha >= '2025-10-01'
UNION ALL
SELECT 'Ingresos Octubre', ROUND(SUM(cantidad * precio_unitario), 2) FROM ventas WHERE fecha >= '2025-10-01'
UNION ALL
SELECT 'Ticket Promedio', ROUND(SUM(cantidad * precio_unitario) / COUNT(*), 2) FROM ventas WHERE fecha >= '2025-10-01';
```

**Explicación**:
Usamos `UNION ALL` para combinar múltiples queries en una sola tabla. Cada query calcula una métrica diferente.

**Resultado esperado**:
| metrica               | valor     |
| --------------------- | --------- |
| Total Productos       | 10        |
| Total Categorías      | 5         |
| Valor Inventario      | 121298.42 |
| Transacciones Octubre | 10        |
| Ingresos Octubre      | 10299.67  |
| Ticket Promedio       | 1029.97   |

---

## Tabla de Autoevaluación

Marca los ejercicios que completaste correctamente:

| Ejercicio                       | Completado | Correcto | Notas |
| ------------------------------- | ---------- | -------- | ----- |
| 1 - Listar productos            | [ ]        | [ ]      |       |
| 2 - Productos caros             | [ ]        | [ ]      |       |
| 3 - Contar por proveedor        | [ ]        | [ ]      |       |
| 4 - Productos Apple             | [ ]        | [ ]      |       |
| 5 - Precio promedio accesorios  | [ ]        | [ ]      |       |
| 6 - Top 3 categorías            | [ ]        | [ ]      |       |
| 7 - Stock bajo                  | [ ]        | [ ]      |       |
| 8 - Ventas por día              | [ ]        | [ ]      |       |
| 9 - Categorías con >2 productos | [ ]        | [ ]      |       |
| 10 - Ingresos octubre           | [ ]        | [ ]      |       |
| 11 - Rentabilidad por categoría | [ ]        | [ ]      |       |
| 12 - Productos sin ventas       | [ ]        | [ ]      |       |
| 13 - Top 5 días                 | [ ]        | [ ]      |       |
| 14 - Performance proveedores    | [ ]        | [ ]      |       |
| 15 - Dashboard ejecutivo        | [ ]        | [ ]      |       |

---

## Desafíos Adicionales (Opcional)

Si completaste todos los ejercicios, intenta estos desafíos:

### Desafío 1: Análisis de Tendencias
Crea una query que muestre si las ventas están aumentando o disminuyendo comparando la primera quincena vs la segunda quincena de octubre.

### Desafío 2: Segmentación de Productos
Clasifica los productos en 3 segmentos según precio:
- Premium: > $1000
- Medio: $100 - $1000
- Económico: < $100

Cuenta cuántos productos hay en cada segmento.

### Desafío 3: Rotación de Inventario
Calcula cuántos días de inventario quedan para cada producto basándote en las ventas de octubre (asumiendo que el patrón se mantiene).

---

## Próximos Pasos

**¡Felicidades por completar los ejercicios de SQL Básico!** 🎉

Ahora estás listo para:

1. **Proyecto Práctico**: Implementar un análisis exploratorio completo de una base de datos
2. **Tema 2**: SQL Intermedio (JOINs, subconsultas, CTEs)
3. **Integrar SQL con Python**: Usar SQLAlchemy para ejecutar queries desde código

### Recursos para Seguir Practicando

- **SQLZoo**: Ejercicios interactivos de SQL
- **LeetCode SQL**: Problemas de entrevistas técnicas
- **Mode Analytics**: Tutoriales con datos reales
- **HackerRank SQL**: Desafíos de programación

---

**Última actualización:** 2025-10-23
