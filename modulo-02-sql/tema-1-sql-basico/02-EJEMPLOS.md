# Ejemplos Prácticos: SQL Básico

> **Objetivo**: Consolidar los conceptos de SQL básico a través de ejemplos trabajados paso a paso con contextos empresariales reales.

En este archivo trabajaremos con **TechStore**, una tienda de electrónica ficticia que necesita analizar sus datos de ventas, productos y clientes.

---

## Preparación: Crear la Base de Datos de Ejemplo

Antes de comenzar con los ejemplos, vamos a crear las tablas que usaremos. Ejecuta estos scripts SQL en tu base de datos (SQLite o PostgreSQL):

```sql
-- Tabla de productos
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    stock_actual INTEGER NOT NULL,
    proveedor VARCHAR(100)
);

-- Insertar datos de ejemplo
INSERT INTO productos (id, nombre, precio, categoria, stock_actual, proveedor) VALUES
(1, 'Laptop HP Pavilion', 899.99, 'Computadoras', 15, 'HP Inc'),
(2, 'Mouse Logitech MX Master', 99.99, 'Accesorios', 45, 'Logitech'),
(3, 'Teclado Mecánico Corsair', 149.99, 'Accesorios', 30, 'Corsair'),
(4, 'Monitor Samsung 27"', 299.99, 'Monitores', 20, 'Samsung'),
(5, 'MacBook Pro 14"', 1999.99, 'Computadoras', 8, 'Apple'),
(6, 'iPhone 15 Pro', 1199.99, 'Smartphones', 25, 'Apple'),
(7, 'iPad Air', 599.99, 'Tablets', 18, 'Apple'),
(8, 'AirPods Pro', 249.99, 'Accesorios', 50, 'Apple'),
(9, 'Dell XPS 15', 1499.99, 'Computadoras', 12, 'Dell'),
(10, 'Webcam Logitech C920', 79.99, 'Accesorios', 35, 'Logitech');

-- Tabla de ventas
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Insertar ventas de ejemplo (octubre 2025)
INSERT INTO ventas (id, producto_id, cantidad, fecha, precio_unitario) VALUES
(1, 1, 2, '2025-10-01', 899.99),
(2, 2, 5, '2025-10-02', 99.99),
(3, 3, 3, '2025-10-03', 149.99),
(4, 6, 1, '2025-10-05', 1199.99),
(5, 8, 4, '2025-10-07', 249.99),
(6, 1, 1, '2025-10-10', 899.99),
(7, 5, 1, '2025-10-12', 1999.99),
(8, 2, 3, '2025-10-15', 99.99),
(9, 4, 2, '2025-10-18', 299.99),
(10, 9, 1, '2025-10-20', 1499.99);
```

---

## Ejemplo 1: Consultas Básicas y Filtrado - Nivel: Básico

### Contexto

El gerente de TechStore quiere un reporte de todos los productos de la categoría "Accesorios" ordenados por precio, para revisar la estrategia de precios de esa categoría.

### Objetivo

Listar todos los productos de accesorios con su nombre, precio y stock actual, ordenados de más caro a más barato.

### Paso 1: Identificar qué datos necesitamos

Necesitamos:
- **Columnas**: `nombre`, `precio`, `stock_actual`
- **Tabla**: `productos`
- **Filtro**: Solo categoría "Accesorios"
- **Ordenamiento**: Por precio descendente

### Paso 2: Escribir la query básica

Empecemos con una query simple para ver todos los accesorios:

```sql
SELECT nombre, precio, stock_actual
FROM productos
WHERE categoria = 'Accesorios';
```

**Resultado:**
| nombre                   | precio | stock_actual |
| ------------------------ | ------ | ------------ |
| Mouse Logitech MX Master | 99.99  | 45           |
| Teclado Mecánico Corsair | 149.99 | 30           |
| AirPods Pro              | 249.99 | 50           |
| Webcam Logitech C920     | 79.99  | 35           |

### Paso 3: Agregar ordenamiento

Ahora ordenamos por precio de mayor a menor:

```sql
SELECT nombre, precio, stock_actual
FROM productos
WHERE categoria = 'Accesorios'
ORDER BY precio DESC;
```

**Resultado ordenado:**
| nombre                   | precio | stock_actual |
| ------------------------ | ------ | ------------ |
| AirPods Pro              | 249.99 | 50           |
| Teclado Mecánico Corsair | 149.99 | 30           |
| Mouse Logitech MX Master | 99.99  | 45           |
| Webcam Logitech C920     | 79.99  | 35           |

### Paso 4: Mejorar con alias

Hagamos los nombres de columnas más descriptivos:

```sql
SELECT
    nombre AS producto,
    precio AS precio_venta,
    stock_actual AS unidades_disponibles
FROM productos
WHERE categoria = 'Accesorios'
ORDER BY precio DESC;
```

**Resultado final:**
| producto                 | precio_venta | unidades_disponibles |
| ------------------------ | ------------ | -------------------- |
| AirPods Pro              | 249.99       | 50                   |
| Teclado Mecánico Corsair | 149.99       | 30                   |
| Mouse Logitech MX Master | 99.99        | 45                   |
| Webcam Logitech C920     | 79.99        | 35                   |

### Interpretación de Resultados

**Hallazgos:**
1. Los AirPods Pro son el accesorio más caro ($249.99)
2. Tenemos 4 productos en la categoría de accesorios
3. Todos tienen buen stock (30-50 unidades)

**Decisión de negocio:**
- Los accesorios tienen precios variados ($79.99 - $249.99)
- Podríamos crear una promoción "Bundle de accesorios" combinando mouse + teclado + webcam
- El stock está saludable, no hay necesidad de reorden inmediato

---

## Ejemplo 2: Funciones Agregadas - Nivel: Básico

### Contexto

El equipo financiero de TechStore necesita un reporte rápido con métricas clave del inventario: cuántos productos hay en total, cuál es el precio promedio, el producto más caro y el más barato.

### Objetivo

Calcular estadísticas resumidas del catálogo de productos.

### Paso 1: Contar productos totales

```sql
SELECT COUNT(*) AS total_productos
FROM productos;
```

**Resultado:**
| total_productos |
| --------------- |
| 10              |

**Interpretación:** TechStore tiene 10 productos diferentes en su catálogo.

### Paso 2: Calcular precio promedio

```sql
SELECT AVG(precio) AS precio_promedio
FROM productos;
```

**Resultado:**
| precio_promedio |
| --------------- |
| 697.99          |

**Interpretación:** El precio promedio de los productos es $697.99.

### Paso 3: Encontrar precio máximo y mínimo

```sql
SELECT
    MAX(precio) AS precio_maximo,
    MIN(precio) AS precio_minimo
FROM productos;
```

**Resultado:**
| precio_maximo | precio_minimo |
| ------------- | ------------- |
| 1999.99       | 79.99         |

**Interpretación:**
- Producto más caro: $1,999.99
- Producto más barato: $79.99
- Rango de precios: $1,920 de diferencia

### Paso 4: Combinar todas las métricas en una sola query

```sql
SELECT
    COUNT(*) AS total_productos,
    AVG(precio) AS precio_promedio,
    MAX(precio) AS precio_maximo,
    MIN(precio) AS precio_minimo,
    SUM(stock_actual) AS unidades_totales_stock
FROM productos;
```

**Resultado:**
| total_productos | precio_promedio | precio_maximo | precio_minimo | unidades_totales_stock |
| --------------- | --------------- | ------------- | ------------- | ---------------------- |
| 10              | 697.99          | 1999.99       | 79.99         | 258                    |

### Paso 5: Agregar formato con ROUND

Los decimales largos son difíciles de leer. Usemos `ROUND()` para redondear:

```sql
SELECT
    COUNT(*) AS total_productos,
    ROUND(AVG(precio), 2) AS precio_promedio,
    MAX(precio) AS precio_maximo,
    MIN(precio) AS precio_minimo,
    SUM(stock_actual) AS unidades_totales_stock
FROM productos;
```

**Resultado:**
| total_productos | precio_promedio | precio_maximo | precio_minimo | unidades_totales_stock |
| --------------- | --------------- | ------------- | ------------- | ---------------------- |
| 10              | 697.99          | 1999.99       | 79.99         | 258                    |

### Interpretación de Resultados

**Hallazgos clave:**
1. **Catálogo pequeño**: Solo 10 productos (oportunidad de expansión)
2. **Precio promedio alto**: $697.99 indica que vendemos productos premium
3. **Gran rango de precios**: $79.99 - $1,999.99 (diversidad de segmentos)
4. **Stock saludable**: 258 unidades totales en inventario

**Decisiones de negocio:**
- Considerar agregar más productos en el rango medio ($300-$600) para capturar más mercado
- El stock total de 258 unidades parece adecuado para una tienda pequeña
- El precio promedio alto sugiere que nuestro target son clientes premium

---

## Ejemplo 3: GROUP BY y HAVING - Nivel: Intermedio

### Contexto

El gerente de categorías de TechStore quiere analizar el inventario por categoría para identificar qué categorías tienen más productos, mayor valor de inventario y cuáles necesitan atención.

### Objetivo

Agrupar productos por categoría y calcular métricas clave para cada una.

### Paso 1: Contar productos por categoría

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos
FROM productos
GROUP BY categoria
ORDER BY cantidad_productos DESC;
```

**Resultado:**
| categoria    | cantidad_productos |
| ------------ | ------------------ |
| Accesorios   | 4                  |
| Computadoras | 3                  |
| Monitores    | 1                  |
| Smartphones  | 1                  |
| Tablets      | 1                  |

**Interpretación:** Accesorios es la categoría con más variedad (4 productos).

### Paso 2: Agregar precio promedio por categoría

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos,
    ROUND(AVG(precio), 2) AS precio_promedio
FROM productos
GROUP BY categoria
ORDER BY precio_promedio DESC;
```

**Resultado:**
| categoria    | cantidad_productos | precio_promedio |
| ------------ | ------------------ | --------------- |
| Computadoras | 3                  | 1466.66         |
| Smartphones  | 1                  | 1199.99         |
| Tablets      | 1                  | 599.99          |
| Monitores    | 1                  | 299.99          |
| Accesorios   | 4                  | 144.99          |

**Interpretación:** Las computadoras tienen el precio promedio más alto ($1,466.66).

### Paso 3: Calcular valor total de inventario por categoría

El valor de inventario es: `precio * stock_actual`

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos,
    ROUND(AVG(precio), 2) AS precio_promedio,
    SUM(stock_actual) AS unidades_totales,
    ROUND(SUM(precio * stock_actual), 2) AS valor_inventario
FROM productos
GROUP BY categoria
ORDER BY valor_inventario DESC;
```

**Resultado:**
| categoria    | cantidad_productos | precio_promedio | unidades_totales | valor_inventario |
| ------------ | ------------------ | --------------- | ---------------- | ---------------- |
| Computadoras | 3                  | 1466.66         | 35               | 51299.65         |
| Smartphones  | 1                  | 1199.99         | 25               | 29999.75         |
| Accesorios   | 4                  | 144.99          | 160              | 23199.40         |
| Tablets      | 1                  | 599.99          | 18               | 10799.82         |
| Monitores    | 1                  | 299.99          | 20               | 5999.80          |

**Interpretación:**
- Computadoras representan el mayor valor de inventario ($51,299.65)
- Aunque Accesorios tiene más unidades (160), su valor es menor por precios bajos

### Paso 4: Filtrar categorías con más de 1 producto usando HAVING

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos,
    ROUND(AVG(precio), 2) AS precio_promedio,
    SUM(stock_actual) AS unidades_totales
FROM productos
GROUP BY categoria
HAVING COUNT(*) > 1  -- Solo categorías con más de 1 producto
ORDER BY cantidad_productos DESC;
```

**Resultado:**
| categoria    | cantidad_productos | precio_promedio | unidades_totales |
| ------------ | ------------------ | --------------- | ---------------- |
| Accesorios   | 4                  | 144.99          | 160              |
| Computadoras | 3                  | 1466.66         | 35               |

**Interpretación:** Solo 2 categorías tienen múltiples productos. Las demás necesitan expansión.

### Paso 5: Identificar categorías con bajo stock promedio

```sql
SELECT
    categoria,
    COUNT(*) AS cantidad_productos,
    ROUND(AVG(stock_actual), 2) AS stock_promedio
FROM productos
GROUP BY categoria
HAVING AVG(stock_actual) < 25  -- Stock promedio bajo
ORDER BY stock_promedio ASC;
```

**Resultado:**
| categoria    | cantidad_productos | stock_promedio |
| ------------ | ------------------ | -------------- |
| Computadoras | 3                  | 11.67          |
| Tablets      | 1                  | 18.00          |
| Monitores    | 1                  | 20.00          |

**Interpretación:** Las computadoras tienen el stock promedio más bajo (11.67 unidades).

### Interpretación de Resultados

**Hallazgos clave:**
1. **Diversidad desigual**: Accesorios tiene 4 productos, otras categorías solo 1
2. **Valor concentrado**: Computadoras representan 42% del valor total de inventario
3. **Stock crítico**: Computadoras tienen stock promedio de solo 11.67 unidades
4. **Oportunidad**: Categorías con 1 solo producto necesitan expansión

**Decisiones de negocio:**
- **Urgente**: Reordenar computadoras (stock bajo + alto valor)
- **Estratégico**: Agregar más productos en Smartphones, Tablets y Monitores
- **Operativo**: Considerar reducir stock de Accesorios (160 unidades es mucho)
- **Financiero**: Diversificar para no depender tanto de Computadoras

---

## Ejemplo 4: Análisis de Ventas - Nivel: Intermedio

### Contexto

El equipo de ventas de TechStore quiere analizar las ventas de octubre 2025 para identificar productos más vendidos, ingresos por producto y tendencias.

### Objetivo

Analizar las ventas del mes usando la tabla `ventas` y combinar con información de `productos`.

### Paso 1: Ver las ventas totales del mes

```sql
SELECT
    COUNT(*) AS total_transacciones,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos_totales
FROM ventas
WHERE fecha >= '2025-10-01' AND fecha < '2025-11-01';
```

**Resultado:**
| total_transacciones | unidades_vendidas | ingresos_totales |
| ------------------- | ----------------- | ---------------- |
| 10                  | 23                | 10299.67         |

**Interpretación:**
- 10 transacciones en octubre
- 23 unidades vendidas en total
- Ingresos de $10,299.67

### Paso 2: Productos más vendidos (por cantidad)

```sql
SELECT
    producto_id,
    SUM(cantidad) AS unidades_vendidas
FROM ventas
GROUP BY producto_id
ORDER BY unidades_vendidas DESC
LIMIT 5;
```

**Resultado:**
| producto_id | unidades_vendidas |
| ----------- | ----------------- |
| 2           | 8                 |
| 8           | 4                 |
| 1           | 3                 |
| 3           | 3                 |
| 4           | 2                 |

**Interpretación:** El producto #2 (Mouse Logitech) es el más vendido con 8 unidades.

### Paso 3: Productos con mayores ingresos

```sql
SELECT
    producto_id,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos_totales
FROM ventas
GROUP BY producto_id
ORDER BY ingresos_totales DESC
LIMIT 5;
```

**Resultado:**
| producto_id | unidades_vendidas | ingresos_totales |
| ----------- | ----------------- | ---------------- |
| 1           | 3                 | 2699.97          |
| 5           | 1                 | 1999.99          |
| 9           | 1                 | 1499.99          |
| 6           | 1                 | 1199.99          |
| 8           | 4                 | 999.96           |

**Interpretación:**
- Laptop HP (#1) generó más ingresos ($2,699.97) aunque solo vendió 3 unidades
- MacBook Pro (#5) generó $1,999.99 con solo 1 venta

### Paso 4: Análisis por día de la semana

```sql
SELECT
    fecha,
    COUNT(*) AS transacciones,
    SUM(cantidad) AS unidades,
    ROUND(SUM(cantidad * precio_unitario), 2) AS ingresos
FROM ventas
GROUP BY fecha
ORDER BY fecha;
```

**Resultado:**
| fecha      | transacciones | unidades | ingresos |
| ---------- | ------------- | -------- | -------- |
| 2025-10-01 | 1             | 2        | 1799.98  |
| 2025-10-02 | 1             | 5        | 499.95   |
| 2025-10-03 | 1             | 3        | 449.97   |
| 2025-10-05 | 1             | 1        | 1199.99  |
| 2025-10-07 | 1             | 4        | 999.96   |
| 2025-10-10 | 1             | 1        | 899.99   |
| 2025-10-12 | 1             | 1        | 1999.99  |
| 2025-10-15 | 1             | 3        | 299.97   |
| 2025-10-18 | 1             | 2        | 599.98   |
| 2025-10-20 | 1             | 1        | 1499.99  |

**Interpretación:** Las ventas están distribuidas a lo largo del mes, sin un patrón claro de días específicos.

### Paso 5: Identificar productos sin ventas

Esto requiere un concepto avanzado (LEFT JOIN), pero podemos aproximarlo:

```sql
SELECT
    p.id,
    p.nombre,
    p.categoria,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.id, p.nombre, p.categoria
HAVING COALESCE(SUM(v.cantidad), 0) = 0;
```

**Nota:** Este ejemplo usa LEFT JOIN que veremos en el Tema 2. Por ahora, enfoquémonos en los productos que SÍ se vendieron.

### Interpretación de Resultados

**Hallazgos clave:**
1. **Volumen vs Valor**: Mouse Logitech lidera en unidades (8), pero Laptop HP en ingresos ($2,699.97)
2. **Productos premium**: MacBook Pro generó $1,999.99 con solo 1 venta
3. **Distribución temporal**: Ventas distribuidas uniformemente en el mes
4. **Ticket promedio**: $10,299.67 / 10 transacciones = $1,029.97 por transacción

**Decisiones de negocio:**
- **Marketing**: Promocionar productos de alto valor (laptops) para maximizar ingresos
- **Stock**: Reabastecer Mouse Logitech (producto más popular)
- **Estrategia**: Combinar productos de alto volumen con alto valor en bundles
- **Análisis futuro**: Investigar por qué algunos productos no se vendieron

---

## Ejemplo 5: Dashboard de Métricas Ejecutivas - Nivel: Avanzado

### Contexto

El CEO de TechStore necesita un dashboard con las métricas más importantes del negocio en una sola vista: productos, ventas, inventario y performance por categoría.

### Objetivo

Crear queries que generen un reporte ejecutivo completo.

### Métrica 1: Resumen General del Negocio

```sql
SELECT
    'Productos' AS metrica,
    COUNT(*) AS valor
FROM productos
UNION ALL
SELECT
    'Categorías Únicas',
    COUNT(DISTINCT categoria)
FROM productos
UNION ALL
SELECT
    'Valor Total Inventario',
    ROUND(SUM(precio * stock_actual), 2)
FROM productos
UNION ALL
SELECT
    'Transacciones Octubre',
    COUNT(*)
FROM ventas
WHERE fecha >= '2025-10-01'
UNION ALL
SELECT
    'Ingresos Octubre',
    ROUND(SUM(cantidad * precio_unitario), 2)
FROM ventas
WHERE fecha >= '2025-10-01';
```

**Resultado:**
| metrica                | valor     |
| ---------------------- | --------- |
| Productos              | 10        |
| Categorías Únicas      | 5         |
| Valor Total Inventario | 121298.42 |
| Transacciones Octubre  | 10        |
| Ingresos Octubre       | 10299.67  |

**Interpretación:** Vista rápida de las métricas clave del negocio.

### Métrica 2: Top 5 Productos por Ingresos

```sql
SELECT
    p.nombre AS producto,
    p.categoria,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0), 2) AS ingresos_totales
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.id, p.nombre, p.categoria
ORDER BY ingresos_totales DESC
LIMIT 5;
```

**Resultado:**
| producto           | categoria    | unidades_vendidas | ingresos_totales |
| ------------------ | ------------ | ----------------- | ---------------- |
| Laptop HP Pavilion | Computadoras | 3                 | 2699.97          |
| MacBook Pro 14"    | Computadoras | 1                 | 1999.99          |
| Dell XPS 15        | Computadoras | 1                 | 1499.99          |
| iPhone 15 Pro      | Smartphones  | 1                 | 1199.99          |
| AirPods Pro        | Accesorios   | 4                 | 999.96           |

**Interpretación:** Las computadoras dominan el top 5 de ingresos.

### Métrica 3: Performance por Categoría

```sql
SELECT
    p.categoria,
    COUNT(DISTINCT p.id) AS productos_en_catalogo,
    COALESCE(SUM(v.cantidad), 0) AS unidades_vendidas,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0), 2) AS ingresos,
    ROUND(COALESCE(SUM(v.cantidad * v.precio_unitario), 0) /
          NULLIF(SUM(v.cantidad), 0), 2) AS precio_promedio_venta
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.categoria
ORDER BY ingresos DESC;
```

**Resultado:**
| categoria    | productos_en_catalogo | unidades_vendidas | ingresos | precio_promedio_venta |
| ------------ | --------------------- | ----------------- | -------- | --------------------- |
| Computadoras | 3                     | 5                 | 6199.95  | 1239.99               |
| Accesorios   | 4                     | 12                | 1749.93  | 145.83                |
| Smartphones  | 1                     | 1                 | 1199.99  | 1199.99               |
| Monitores    | 1                     | 2                 | 599.98   | 299.99                |
| Tablets      | 1                     | 0                 | 0.00     | NULL                  |

**Interpretación:**
- Computadoras: 60% de los ingresos con solo 3 productos
- Tablets: 0 ventas en octubre (¡alerta!)
- Accesorios: Alto volumen (12 unidades) pero bajo valor

### Métrica 4: Productos con Stock Crítico

```sql
SELECT
    nombre AS producto,
    categoria,
    stock_actual,
    COALESCE(SUM(v.cantidad), 0) AS vendido_octubre,
    CASE
        WHEN stock_actual < 10 THEN 'CRÍTICO'
        WHEN stock_actual < 20 THEN 'BAJO'
        ELSE 'OK'
    END AS estado_stock
FROM productos p
LEFT JOIN ventas v ON p.id = v.producto_id
GROUP BY p.id, p.nombre, p.categoria, p.stock_actual
HAVING estado_stock IN ('CRÍTICO', 'BAJO')
ORDER BY stock_actual ASC;
```

**Resultado:**
| producto           | categoria    | stock_actual | vendido_octubre | estado_stock |
| ------------------ | ------------ | ------------ | --------------- | ------------ |
| MacBook Pro 14"    | Computadoras | 8            | 1               | CRÍTICO      |
| Dell XPS 15        | Computadoras | 12           | 1               | BAJO         |
| Laptop HP Pavilion | Computadoras | 15           | 3               | BAJO         |
| iPad Air           | Tablets      | 18           | 0               | BAJO         |

**Interpretación:** 4 productos necesitan reorden, especialmente MacBook Pro (solo 8 unidades).

### Interpretación de Resultados del Dashboard

**Hallazgos ejecutivos:**

1. **Salud del negocio**:
   - Inventario valorado en $121,298.42
   - Ingresos de octubre: $10,299.67 (8.5% del valor de inventario)

2. **Concentración de riesgo**:
   - 60% de ingresos vienen de computadoras
   - Necesitamos diversificar categorías

3. **Alertas operativas**:
   - MacBook Pro con stock crítico (8 unidades)
   - iPad Air sin ventas en octubre

4. **Oportunidades**:
   - Accesorios tienen alto volumen pero bajo valor → oportunidad de upselling
   - Tablets necesitan campaña de marketing

**Decisiones estratégicas:**
- **Inmediato**: Reordenar MacBook Pro y otras computadoras
- **Corto plazo**: Lanzar campaña para iPad Air
- **Mediano plazo**: Expandir catálogo de Smartphones y Monitores
- **Largo plazo**: Reducir dependencia de categoría Computadoras

---

## Resumen de Aprendizajes

### Patrones Comunes

1. **Exploración básica**: `SELECT` + `WHERE` + `ORDER BY`
2. **Agregaciones simples**: `COUNT`, `SUM`, `AVG` sin agrupar
3. **Análisis por grupos**: `GROUP BY` + funciones agregadas
4. **Filtrado de grupos**: `HAVING` después de `GROUP BY`
5. **Top N**: `ORDER BY` + `LIMIT`

### Buenas Prácticas Aplicadas

- ✅ Usar alias descriptivos (`AS precio_promedio`)
- ✅ Redondear decimales con `ROUND()`
- ✅ Ordenar resultados para facilitar interpretación
- ✅ Comentar queries complejas
- ✅ Indentar SQL para legibilidad

### Próximos Pasos

Ahora que has visto ejemplos trabajados:

1. **Practica** resolviendo los ejercicios en `03-EJERCICIOS.md`
2. **Experimenta** modificando estas queries con tus propios filtros
3. **Crea** tus propias tablas de prueba con datos ficticios
4. **Comparte** tus hallazgos con otros estudiantes

---

**¡Felicidades por completar los ejemplos de SQL Básico!** 🎉

Ahora tienes las herramientas para analizar datos reales y tomar decisiones de negocio basadas en evidencia.

---

**Última actualización:** 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
