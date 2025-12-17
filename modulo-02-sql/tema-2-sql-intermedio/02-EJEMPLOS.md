# Ejemplos Prácticos: SQL Intermedio

> **Contexto empresarial:** Todos los ejemplos usan datos de **TechStore**, una tienda de electrónica ficticia. Los datos son realistas pero no reales.

> **Instrucciones:** Lee cada ejemplo paso a paso, ejecuta las queries en tu entorno y compara resultados. Los scripts SQL para crear las tablas están al inicio.

---

## 📊 Preparación: Crear Base de Datos de Ejemplo

Antes de empezar con los ejemplos, ejecuta estos scripts para crear las tablas y datos de TechStore:

```sql
-- Crear base de datos de TechStore para ejemplos

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Computadoras', 'Laptops, desktops y componentes'),
(2, 'Accesorios', 'Mouse, teclados, webcams'),
(3, 'Audio', 'Audífonos, bocinas, micrófonos'),
(4, 'Almacenamiento', 'Discos duros, SSDs, USB');

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria_id INTEGER,
    stock INTEGER DEFAULT 0,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

INSERT INTO productos (id, nombre, precio, categoria_id, stock, activo) VALUES
(1, 'Laptop HP Pavilion', 899.99, 1, 15, 1),
(2, 'Laptop Dell XPS', 1299.99, 1, 8, 1),
(3, 'Mouse Logitech MX', 79.99, 2, 50, 1),
(4, 'Teclado Mecánico', 129.99, 2, 30, 1),
(5, 'Webcam HD', 59.99, 2, 25, 1),
(6, 'Audífonos Sony', 199.99, 3, 20, 1),
(7, 'Bocina Bluetooth', 89.99, 3, 35, 1),
(8, 'SSD 1TB Samsung', 149.99, 4, 40, 1),
(9, 'Disco Duro 2TB', 89.99, 4, 45, 1),
(10, 'Tablet obsoleta', 299.99, 1, 0, 0);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    fecha_registro DATE NOT NULL,
    ciudad TEXT
);

INSERT INTO clientes (id, nombre, email, fecha_registro, ciudad) VALUES
(1, 'Ana García', 'ana@email.com', '2024-01-15', 'Madrid'),
(2, 'Carlos López', 'carlos@email.com', '2024-02-20', 'Barcelona'),
(3, 'María Rodríguez', 'maria@email.com', '2024-03-10', 'Valencia'),
(4, 'Juan Martínez', 'juan@email.com', '2024-04-05', 'Sevilla'),
(5, 'Laura Sánchez', 'laura@email.com', '2024-10-01', 'Madrid');

-- Tabla de ventas (pedidos)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT INTO ventas (id, cliente_id, producto_id, cantidad, fecha, total) VALUES
(1, 1, 1, 1, '2025-01-15', 899.99),
(2, 1, 3, 2, '2025-01-16', 159.98),
(3, 2, 2, 1, '2025-01-20', 1299.99),
(4, 2, 6, 1, '2025-01-21', 199.99),
(5, 3, 4, 1, '2025-02-05', 129.99),
(6, 3, 8, 2, '2025-02-05', 299.98),
(7, 1, 7, 1, '2025-02-10', 89.99),
(8, 4, 3, 3, '2025-02-15', 239.97),
(9, 2, 9, 1, '2025-03-01', 89.99),
(10, 1, 5, 1, '2025-03-05', 59.99);
```

---

## Ejemplo 1: INNER JOIN Básico - Productos con Categorías

**Nivel:** Básico
**Duración:** 10-15 minutos
**Conceptos:** INNER JOIN, alias, selección de columnas

### Contexto

El equipo de inventario de TechStore necesita un reporte de todos los productos activos mostrando a qué categoría pertenecen. Necesitan esta información para reorganizar el almacén por secciones.

### Objetivo

Listar todos los productos activos con su nombre, precio y categoría correspondiente.

### Paso 1: Entender las Tablas Relacionadas

Tenemos dos tablas:
- **`productos`**: Contiene `categoria_id` (clave foránea)
- **`categorias`**: Contiene `id` (clave primaria)

**Relación:** Un producto pertenece a UNA categoría. Una categoría puede tener MUCHOS productos.

### Paso 2: Escribir la Query con INNER JOIN

```sql
-- Reporte de productos con su categoría
SELECT
    p.nombre AS producto,
    p.precio,
    c.nombre AS categoria,
    p.stock
FROM productos p
INNER JOIN categorias c
    ON p.categoria_id = c.id
WHERE p.activo = 1
ORDER BY c.nombre, p.nombre;
```

### Paso 3: Analizar el Resultado

```
| producto           | precio  | categoria      | stock |
| ------------------ | ------- | -------------- | ----- |
| Bocina Bluetooth   | 89.99   | Audio          | 35    |
| Audífonos Sony     | 199.99  | Audio          | 20    |
| Disco Duro 2TB     | 89.99   | Almacenamiento | 45    |
| SSD 1TB Samsung    | 149.99  | Almacenamiento | 40    |
| Mouse Logitech MX  | 79.99   | Accesorios     | 50    |
| Teclado Mecánico   | 129.99  | Accesorios     | 30    |
| Webcam HD          | 59.99   | Accesorios     | 25    |
| Laptop HP Pavilion | 899.99  | Computadoras   | 15    |
| Laptop Dell XPS    | 1299.99 | Computadoras   | 8     |
```

**Nota:** La "Tablet obsoleta" NO aparece porque tiene `activo = 0`.

### Interpretación de Negocio

1. **Organización física:** El equipo puede agrupar productos por categoría en el almacén
2. **Stock crítico:** Las laptops tienen poco stock (15 y 8 unidades) → Necesitan reabastecerse
3. **Inventario por categoría:** Accesorios tiene más productos (3 items), luego Computadoras, Audio y Almacenamiento (2 cada una)

### Decisión de Negocio

**Acción inmediata:** Reabastecer laptops antes de que se agoten. Considerar descontinuar la tablet obsoleta si no se vende.

---

## Ejemplo 2: LEFT JOIN - Clientes Sin Pedidos

**Nivel:** Básico
**Duración:** 15-20 minutos
**Conceptos:** LEFT JOIN, IS NULL, identificación de ausencias

### Contexto

El equipo de marketing de TechStore está planeando una campaña de reactivación. Necesitan identificar a los clientes registrados que **nunca han comprado nada** para enviarles un cupón de descuento especial del 20%.

### Objetivo

Listar TODOS los clientes mostrando cuántos pedidos han hecho. Identificar específicamente a los que tienen 0 pedidos.

### Paso 1: Entender el Problema

- **Tabla principal:** `clientes` (queremos TODOS los clientes)
- **Tabla secundaria:** `ventas` (puede o no tener registros para cada cliente)
- **JOIN correcto:** LEFT JOIN (no INNER, porque perderíamos clientes sin ventas)

### Paso 2: Query con LEFT JOIN (Versión 1)

```sql
-- Mostrar todos los clientes con su número de pedidos
SELECT
    c.nombre,
    c.email,
    c.fecha_registro,
    COUNT(v.id) AS total_pedidos,
    COALESCE(SUM(v.total), 0) AS gasto_total
FROM clientes c
LEFT JOIN ventas v
    ON c.id = v.cliente_id
GROUP BY c.id, c.nombre, c.email, c.fecha_registro
ORDER BY total_pedidos ASC, c.nombre;
```

### Paso 3: Resultado

```
| nombre          | email            | fecha_registro | total_pedidos | gasto_total |
| --------------- | ---------------- | -------------- | ------------- | ----------- |
| Juan Martínez   | juan@email.com   | 2024-04-05     | 1             | 239.97      |
| Laura Sánchez   | laura@email.com  | 2024-10-01     | 0             | 0.00        |
| María Rodríguez | maria@email.com  | 2024-03-10     | 2             | 429.97      |
| Carlos López    | carlos@email.com | 2024-02-20     | 3             | 1589.97     |
| Ana García      | ana@email.com    | 2024-01-15     | 4             | 1210.94     |
```

### Paso 4: Filtrar SOLO Clientes Sin Pedidos

Si solo queremos los clientes inactivos:

```sql
-- Clientes que NUNCA han comprado
SELECT
    c.nombre,
    c.email,
    c.fecha_registro,
    JULIANDAY('now') - JULIANDAY(c.fecha_registro) AS dias_registrado
FROM clientes c
LEFT JOIN ventas v
    ON c.id = v.cliente_id
WHERE v.id IS NULL
ORDER BY c.fecha_registro;
```

**Resultado:**
```
| nombre        | email           | fecha_registro | dias_registrado |
| ------------- | --------------- | -------------- | --------------- |
| Laura Sánchez | laura@email.com | 2024-10-01     | ~25 días        |
```

### Interpretación de Negocio

**Hallazgos clave:**
1. **1 cliente inactivo:** Laura Sánchez se registró hace ~25 días pero no ha comprado
2. **Cliente VIP:** Ana García tiene 4 pedidos con $1,210 en gasto total (mejor cliente)
3. **Tasa de conversión:** 80% (4 de 5 clientes han comprado)

### Decisión de Negocio

**Campaña de reactivación:**
1. Enviar cupón 20% a Laura Sánchez vía email
2. Crear programa VIP para Ana y Carlos (gastaron >$1,000)
3. Investigar por qué Laura no compró (encuesta, seguimiento telefónico)

---

## Ejemplo 3: Subconsulta en WHERE - Top 10% de Clientes

**Nivel:** Intermedio
**Duración:** 20-25 minutos
**Conceptos:** Subconsultas, percentiles, segmentación de clientes

### Contexto

El CEO de TechStore quiere lanzar un programa exclusivo "TechStore Elite" para el **top 10% de clientes por gasto total**. Necesita identificar quiénes califican y cuánto han gastado para calcular beneficios personalizados.

### Objetivo

Identificar clientes cuyo gasto total está en el percentil 90 o superior (top 10%).

### Paso 1: Calcular el Umbral (Percentil 90)

Primero necesitamos saber cuál es el gasto que marca el top 10%:

```sql
-- ¿Cuánto necesita gastar un cliente para estar en el top 10%?
-- (Usamos percentil 90 como aproximación)

SELECT
    cliente_id,
    SUM(total) AS gasto_total
FROM ventas
GROUP BY cliente_id
ORDER BY gasto_total DESC
LIMIT 1 OFFSET (
    SELECT COUNT(DISTINCT cliente_id) * 9 / 10
    FROM ventas
);
```

### Paso 2: Query Principal con Subconsulta

```sql
-- Clientes en el top 10% por gasto total
SELECT
    c.nombre,
    c.email,
    c.ciudad,
    SUM(v.total) AS gasto_total,
    COUNT(v.id) AS total_pedidos,
    ROUND(AVG(v.total), 2) AS ticket_promedio
FROM clientes c
INNER JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.id, c.nombre, c.email, c.ciudad
HAVING gasto_total >= (
    -- Subconsulta: Calcular umbral del top 10%
    SELECT
        PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY gasto_subtotal)
    FROM (
        SELECT SUM(total) AS gasto_subtotal
        FROM ventas
        GROUP BY cliente_id
    )
)
ORDER BY gasto_total DESC;
```

**Nota:** SQLite no soporta PERCENTILE_CONT. Versión simplificada:

```sql
-- Versión compatible con SQLite
-- Definimos umbral manual basado en datos
WITH gastos_clientes AS (
    SELECT
        c.id,
        c.nombre,
        c.email,
        c.ciudad,
        SUM(v.total) AS gasto_total,
        COUNT(v.id) AS total_pedidos
    FROM clientes c
    INNER JOIN ventas v ON c.id = v.cliente_id
    GROUP BY c.id, c.nombre, c.email, c.ciudad
)
SELECT
    nombre,
    email,
    ciudad,
    gasto_total,
    total_pedidos,
    ROUND(gasto_total / total_pedidos, 2) AS ticket_promedio
FROM gastos_clientes
WHERE gasto_total >= (
    -- Subconsulta: Promedio de gastos como umbral
    SELECT AVG(gasto_total) * 1.5
    FROM gastos_clientes
)
ORDER BY gasto_total DESC;
```

### Paso 3: Resultado

```
| nombre       | email            | ciudad    | gasto_total | total_pedidos | ticket_promedio |
| ------------ | ---------------- | --------- | ----------- | ------------- | --------------- |
| Carlos López | carlos@email.com | Barcelona | 1589.97     | 3             | 529.99          |
| Ana García   | ana@email.com    | Madrid    | 1210.94     | 4             | 302.74          |
```

### Interpretación de Negocio

**Perfil de clientes elite:**
1. **Carlos López:** Gasto más alto ($1,590), compra productos premium (laptop Dell $1,300)
2. **Ana García:** Más pedidos frecuentes (4 pedidos), ticket promedio menor pero lealtad alta
3. **Geografía:** Ambos en ciudades grandes (Barcelona, Madrid)

### Decisión de Negocio

**Programa TechStore Elite:**
1. **Beneficios exclusivos:**
   - Descuento 15% permanente
   - Envío gratis ilimitado
   - Acceso anticipado a nuevos productos
2. **Inversión:** ~$200 en beneficios por cliente VIP
3. **ROI esperado:** Incrementar gasto 20% anual ($300-400 adicionales por cliente)

---

## Ejemplo 4: CASE WHEN - Categorización de Productos

**Nivel:** Intermedio
**Duración:** 20-25 minutos
**Conceptos:** CASE WHEN, segmentación, lógica de negocio en SQL

### Contexto

El equipo de compras de TechStore necesita clasificar el inventario en categorías de gestión: **"Crítico"** (bajo stock), **"Normal"** (stock adecuado), y **"Sobrecargado"** (demasiado stock). Esto les ayudará a priorizar reabastecimientos y evitar capital inmovilizado.

### Objetivo

Clasificar productos por nivel de stock y calcular valor del inventario por segmento.

### Paso 1: Definir Reglas de Negocio

**Clasificación de stock:**
- **Crítico:** Stock < 15 unidades → Reabastecer urgente
- **Normal:** Stock entre 15-40 unidades → Monitorear
- **Sobrecargado:** Stock > 40 unidades → Reducir órdenes

### Paso 2: Query con CASE WHEN

```sql
-- Clasificación de inventario por nivel de stock
SELECT
    p.nombre AS producto,
    c.nombre AS categoria,
    p.stock,
    p.precio,
    p.stock * p.precio AS valor_inventario,
    CASE
        WHEN p.stock < 15 THEN 'Crítico'
        WHEN p.stock BETWEEN 15 AND 40 THEN 'Normal'
        WHEN p.stock > 40 THEN 'Sobrecargado'
        ELSE 'Sin clasificar'
    END AS nivel_stock
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = 1
ORDER BY
    CASE
        WHEN p.stock < 15 THEN 1  -- Críticos primero
        WHEN p.stock BETWEEN 15 AND 40 THEN 2
        ELSE 3
    END,
    p.stock ASC;
```

### Paso 3: Resultado

```
| producto           | categoria      | stock | precio  | valor_inventario | nivel_stock  |
| ------------------ | -------------- | ----- | ------- | ---------------- | ------------ |
| Laptop Dell XPS    | Computadoras   | 8     | 1299.99 | 10399.92         | Crítico      |
| Laptop HP Pavilion | Computadoras   | 15    | 899.99  | 13499.85         | Normal       |
| Audífonos Sony     | Audio          | 20    | 199.99  | 3999.80          | Normal       |
| Webcam HD          | Accesorios     | 25    | 59.99   | 1499.75          | Normal       |
| Teclado Mecánico   | Accesorios     | 30    | 129.99  | 3899.70          | Normal       |
| Bocina Bluetooth   | Audio          | 35    | 89.99   | 3149.65          | Normal       |
| SSD 1TB Samsung    | Almacenamiento | 40    | 149.99  | 5999.60          | Normal       |
| Disco Duro 2TB     | Almacenamiento | 45    | 89.99   | 4049.55          | Sobrecargado |
| Mouse Logitech MX  | Accesorios     | 50    | 79.99   | 3999.50          | Sobrecargado |
```

### Paso 4: Resumen Ejecutivo por Segmento

```sql
-- Resumen de inventario por nivel de stock
SELECT
    CASE
        WHEN stock < 15 THEN 'Crítico'
        WHEN stock BETWEEN 15 AND 40 THEN 'Normal'
        ELSE 'Sobrecargado'
    END AS nivel_stock,
    COUNT(*) AS productos,
    SUM(stock) AS unidades_totales,
    ROUND(SUM(stock * precio), 2) AS valor_total
FROM productos
WHERE activo = 1
GROUP BY nivel_stock
ORDER BY
    CASE nivel_stock
        WHEN 'Crítico' THEN 1
        WHEN 'Normal' THEN 2
        ELSE 3
    END;
```

**Resultado resumen:**
```
| nivel_stock  | productos | unidades_totales | valor_total |
| ------------ | --------- | ---------------- | ----------- |
| Crítico      | 1         | 8                | 10399.92    |
| Normal       | 6         | 165              | 32048.45    |
| Sobrecargado | 2         | 95               | 8049.05     |
```

### Interpretación de Negocio

**Análisis por segmento:**
1. **Crítico (1 producto):**
   - Laptop Dell XPS: Solo 8 unidades → **Reabastecer URGENTE**
   - Alto valor ($10,400 en inventario) → Riesgo de pérdida de ventas

2. **Normal (6 productos):**
   - 66% del catálogo → Nivel saludable
   - $32,048 en inventario → Capital bien utilizado

3. **Sobrecargado (2 productos):**
   - Disco Duro y Mouse → Más de 40 unidades cada uno
   - $8,049 en capital inmovilizado → Reducir próximas órdenes

### Decisión de Negocio

**Plan de acción inmediato:**
1. **Laptops Dell:** Ordenar 20 unidades más (lead time: 2 semanas)
2. **Discos duros y Mouse:** Detener nuevas órdenes por 2 meses
3. **Promoción flash:** Descuento 10% en productos sobrecargados para liberar capital

---

## Ejemplo 5: JOIN Múltiple - Análisis de Ventas Completo

**Nivel:** Avanzado
**Duración:** 30-40 minutos
**Conceptos:** JOINs múltiples (4 tablas), agregaciones, CASE WHEN combinado, reporting completo

### Contexto

El CFO de TechStore necesita un **dashboard ejecutivo mensual** que muestre:
1. Ventas por categoría
2. Productos más vendidos
3. Ciudades con más ingresos
4. Segmentación de clientes (VIP vs Regular vs Nuevo)

Este reporte se usa en la junta mensual para tomar decisiones estratégicas.

### Objetivo

Crear un reporte completo combinando clientes, ventas, productos y categorías en una sola query.

### Paso 1: Reporte de Ventas por Categoría

```sql
-- Ventas por categoría (últimos 3 meses)
SELECT
    c.nombre AS categoria,
    COUNT(DISTINCT v.id) AS total_transacciones,
    SUM(v.cantidad) AS unidades_vendidas,
    ROUND(SUM(v.total), 2) AS ingresos_totales,
    ROUND(AVG(v.total), 2) AS ticket_promedio,
    ROUND(SUM(v.total) * 100.0 / (SELECT SUM(total) FROM ventas), 2) AS porcentaje_ingresos
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id
LEFT JOIN ventas v ON p.id = v.producto_id AND v.fecha >= DATE('now', '-90 days')
GROUP BY c.id, c.nombre
HAVING ingresos_totales > 0
ORDER BY ingresos_totales DESC;
```

**Resultado:**
```
| categoria      | total_transacciones | unidades_vendidas | ingresos_totales | ticket_promedio | porcentaje_ingresos |
| -------------- | ------------------- | ----------------- | ---------------- | --------------- | ------------------- |
| Computadoras   | 2                   | 2                 | 2199.98          | 1099.99         | 45.83%              |
| Audio          | 2                   | 2                 | 289.98           | 144.99          | 6.04%               |
| Almacenamiento | 3                   | 4                 | 389.97           | 129.99          | 8.12%               |
| Accesorios     | 3                   | 6                 | 529.94           | 176.65          | 11.03%              |
```

### Paso 2: Reporte de Clientes Segmentados con Ventas

```sql
-- Dashboard ejecutivo completo
WITH cliente_stats AS (
    SELECT
        c.id,
        c.nombre,
        c.ciudad,
        COUNT(v.id) AS total_pedidos,
        SUM(v.total) AS gasto_total,
        MAX(v.fecha) AS ultima_compra,
        JULIANDAY('now') - JULIANDAY(MAX(v.fecha)) AS dias_desde_ultima_compra
    FROM clientes c
    LEFT JOIN ventas v ON c.id = v.cliente_id
    GROUP BY c.id, c.nombre, c.ciudad
)
SELECT
    cs.nombre AS cliente,
    cs.ciudad,
    cs.total_pedidos,
    ROUND(cs.gasto_total, 2) AS gasto_total,
    cs.ultima_compra,
    ROUND(cs.dias_desde_ultima_compra, 0) AS dias_inactivo,
    CASE
        WHEN cs.gasto_total >= 1000 THEN 'VIP'
        WHEN cs.total_pedidos >= 2 THEN 'Regular'
        WHEN cs.total_pedidos = 1 THEN 'Nuevo'
        ELSE 'Sin compras'
    END AS segmento,
    CASE
        WHEN cs.dias_desde_ultima_compra <= 30 THEN 'Activo'
        WHEN cs.dias_desde_ultima_compra <= 90 THEN 'En riesgo'
        ELSE 'Inactivo'
    END AS estado
FROM cliente_stats cs
ORDER BY cs.gasto_total DESC NULLS LAST;
```

**Resultado:**
```
| cliente         | ciudad    | total_pedidos | gasto_total | ultima_compra | dias_inactivo | segmento    | estado   |
| --------------- | --------- | ------------- | ----------- | ------------- | ------------- | ----------- | -------- |
| Carlos López    | Barcelona | 3             | 1589.97     | 2025-03-01    | ~238          | VIP         | Inactivo |
| Ana García      | Madrid    | 4             | 1210.94     | 2025-03-05    | ~234          | VIP         | Inactivo |
| María Rodríguez | Valencia  | 2             | 429.97      | 2025-02-05    | ~262          | Regular     | Inactivo |
| Juan Martínez   | Sevilla   | 1             | 239.97      | 2025-02-15    | ~252          | Nuevo       | Inactivo |
| Laura Sánchez   | Madrid    | 0             | NULL        | NULL          | NULL          | Sin compras | Inactivo |
```

### Paso 3: Análisis Geográfico

```sql
-- Ingresos por ciudad
SELECT
    c.ciudad,
    COUNT(DISTINCT c.id) AS clientes_totales,
    COUNT(DISTINCT v.id) AS pedidos_totales,
    COALESCE(SUM(v.total), 0) AS ingresos_totales,
    ROUND(COALESCE(AVG(v.total), 0), 2) AS ticket_promedio
FROM clientes c
LEFT JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.ciudad
ORDER BY ingresos_totales DESC;
```

**Resultado:**
```
| ciudad    | clientes_totales | pedidos_totales | ingresos_totales | ticket_promedio |
| --------- | ---------------- | --------------- | ---------------- | --------------- |
| Barcelona | 1                | 3               | 1589.97          | 529.99          |
| Madrid    | 2                | 4               | 1210.94          | 302.74          |
| Valencia  | 1                | 2               | 429.97           | 214.99          |
| Sevilla   | 1                | 1               | 239.97           | 239.97          |
```

### Interpretación de Negocio

**Hallazgos clave del dashboard:**

1. **Categorías más rentables:**
   - Computadoras genera 45.8% de ingresos (pero solo 2 transacciones)
   - Accesorios: Margen menor pero más volumen (6 unidades vendidas)

2. **Clientes VIP:**
   - 2 clientes (40%) generan 63% de ingresos totales ($2,800 de $4,800)
   - **Problema:** Ambos VIPs están inactivos (>230 días sin comprar)

3. **Geografía:**
   - Barcelona: Mejor cliente individual (Carlos: $1,590)
   - Madrid: Más clientes (2), pero uno inactivo (Laura)
   - Valencia y Sevilla: Potencial de crecimiento

4. **Tasa de conversión:**
   - 80% de clientes ha comprado al menos una vez
   - 40% ha comprado 2+ veces (fidelización)

### Decisiones de Negocio

**Plan estratégico Q1 2026:**

1. **Reactivación de VIPs (URGENTE):**
   - Llamar a Carlos y Ana directamente
   - Oferta personalizada: 20% descuento + envío gratis
   - Meta: Recuperar al menos 1 cliente VIP

2. **Expansión geográfica:**
   - Abrir punto de retiro en Barcelona (mejor ciudad)
   - Campaña digital en Valencia y Sevilla

3. **Mix de productos:**
   - Promocionar más laptops (alto margen, bajo volumen)
   - Combos: "Laptop + Accesorios" con descuento

4. **Nuevos clientes:**
   - Campaña de adquisición: Meta 10 clientes nuevos/mes
   - Cupón 10% primera compra

5. **Retención:**
   - Email automation: "Te extrañamos" a 60 días de inactividad
   - Programa de lealtad: 1 punto por cada $10 gastados

---

## Resumen de los Ejemplos

### Conceptos Aplicados

| Ejemplo | Concepto Principal       | Nivel      | Tablas Usadas | Líneas de Código |
| ------- | ------------------------ | ---------- | ------------- | ---------------- |
| 1       | INNER JOIN básico        | Básico     | 2 tablas      | 8 líneas         |
| 2       | LEFT JOIN + IS NULL      | Básico     | 2 tablas      | 10 líneas        |
| 3       | Subconsultas en HAVING   | Intermedio | 2 tablas      | 20 líneas        |
| 4       | CASE WHEN + ORDER BY     | Intermedio | 2 tablas      | 18 líneas        |
| 5       | JOIN múltiple (4 tablas) | Avanzado   | 4 tablas      | 35 líneas        |

### Patrones Comunes Identificados

1. **Siempre usa alias** en JOINs múltiples (p, c, v) para claridad
2. **COALESCE para NULLs** en LEFT JOINs: `COALESCE(SUM(v.total), 0)`
3. **ORDER BY inteligente** con CASE para priorizar resultados
4. **CTEs (WITH)** para queries complejas y legibles
5. **Filtros en WHERE vs ON**: WHERE filtra resultado final, ON filtra antes de JOIN

### Próximos Pasos

Has completado los 5 ejemplos prácticos. Ahora:

1. **Ejecuta las queries** en tu entorno local
2. **Modifica los datos** y observa cómo cambian los resultados
3. **Practica con ejercicios** en `03-EJERCICIOS.md`
4. **Implementa el proyecto práctico** en `04-proyecto-practico/`

---

**Última actualización:** 2025-10-25
**Tiempo estimado:** 90-120 minutos (todos los ejemplos)
**Nivel:** Básico a Avanzado
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
