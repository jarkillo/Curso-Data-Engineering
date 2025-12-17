# Teoría: Modelado de Datos

## Introducción: El Arte del Diseño

Imagina que estás diseñando el plano de una ciudad. Puedes hacerlo de dos formas:

1. **Ciudad residencial** (OLTP): Calles estrechas, casas pequeñas, muchas esquinas. Perfecto para vivir (transacciones diarias).
2. **Centro comercial** (OLAP): Pasillos anchos, tiendas grandes, todo a la vista. Perfecto para comprar rápido (análisis).

El **modelado de datos** es diseñar el "plano" de tu base de datos según su propósito.

### ¿Por qué importa?

En Data Engineering:
- **Airbnb** usa modelado OLTP para reservas (normalizado, transaccional)
- **Airbnb** usa modelado OLAP para analytics (desnormalizado, dimensional)
- Un mal diseño = queries lentas, bugs, costos altos

---

## Parte 1: Normalización (OLTP)

### Concepto 1: ¿Qué es Normalización?

**Normalización** es organizar datos para eliminar redundancia y anomalías.

**Analogía**: Es como organizar tu cocina. En lugar de tener sal en 5 lugares diferentes, tienes UN frasco de sal en UN lugar específico. Cuando se acaba, lo sabes. Cuando lo rellenas, todos lo tienen.

#### Problemas sin normalización

```
Tabla: ventas
id | cliente | email_cliente | producto | precio_producto | cantidad
1  | Ana     | ana@ex.com    | Laptop   | 999            | 2
2  | Ana     | ana@ex.com    | Mouse    | 25             | 1
3  | Bob     | bob@ex.com    | Laptop   | 999            | 1
```

**Problemas**:
1. **Redundancia**: Email de Ana repetido, precio de Laptop repetido
2. **Anomalía de actualización**: Si Ana cambia su email, hay que actualizar múltiples filas
3. **Anomalía de inserción**: No puedo añadir un cliente sin una venta
4. **Anomalía de eliminación**: Si borro venta de Bob, pierdo su información

---

### Concepto 2: Primera Forma Normal (1NF)

**Regla**: Cada celda debe contener UN solo valor atómico. No listas ni grupos.

**Incorrecto (No está en 1NF)**:
```
id | cliente | telefonos
1  | Ana     | "555-1234, 555-5678"  ← ¡Múltiples valores!
```

**Correcto (Está en 1NF)**:
```
Tabla: clientes
id | nombre
1  | Ana

Tabla: telefonos_clientes
id | cliente_id | telefono
1  | 1          | 555-1234
2  | 1          | 555-5678
```

**Reglas 1NF**:
- ✅ Valores atómicos (indivisibles)
- ✅ Sin arrays ni listas en una celda
- ✅ Cada columna tiene un tipo de dato consistente
- ✅ Cada fila es única (tiene PK)

---

### Concepto 3: Segunda Forma Normal (2NF)

**Regla**: Debe estar en 1NF + cada columna no-PK debe depender de TODA la clave primaria.

**Problema**: Dependencia parcial de la PK compuesta.

**Incorrecto (No está en 2NF)**:
```
Tabla: items_orden
orden_id | producto_id | cantidad | nombre_producto | precio_producto
1        | 101         | 2        | Laptop          | 999
1        | 102         | 1        | Mouse           | 25

PK compuesta: (orden_id, producto_id)
Problema: nombre_producto y precio_producto solo dependen de producto_id, no de toda la PK
```

**Correcto (Está en 2NF)**:
```
Tabla: items_orden
orden_id | producto_id | cantidad
1        | 101         | 2
1        | 102         | 1
PK: (orden_id, producto_id)

Tabla: productos
producto_id | nombre   | precio
101         | Laptop   | 999
102         | Mouse    | 25
PK: producto_id
```

---

### Concepto 4: Tercera Forma Normal (3NF)

**Regla**: Debe estar en 2NF + no debe haber dependencias transitivas.

**Dependencia transitiva**: A → B → C (si A determina B, y B determina C, entonces A determina C indirectamente).

**Incorrecto (No está en 3NF)**:
```
Tabla: empleados
id | nombre | departamento_id | departamento_nombre | jefe_departamento
1  | Ana    | 10              | Ventas              | Carlos
2  | Bob    | 10              | Ventas              | Carlos

Problema: id → departamento_id → departamento_nombre
         id → departamento_id → jefe_departamento
```

**Correcto (Está en 3NF)**:
```
Tabla: empleados
id | nombre | departamento_id
1  | Ana    | 10
2  | Bob    | 10

Tabla: departamentos
departamento_id | nombre | jefe
10              | Ventas | Carlos
```

---

### Concepto 5: Forma Normal de Boyce-Codd (BCNF)

**Regla**: Está en 3NF + toda dependencia funcional debe venir de una superclave.

**Raramente necesitas BCNF** en la práctica. 3NF es suficiente para 99% de casos OLTP.

---

## Parte 2: Diagramas Entidad-Relación (ER)

### Concepto 6: Componentes de un Diagrama ER

```
┌──────────────┐
│   ENTIDAD    │  ← Rectángulo
└──────────────┘

───────────────   ← Línea (relación)

◊ Atributo      ← Rombo/óvalo

Cardinalidad:
─────── 1:1 (uno a uno)
───<   1:N (uno a muchos)
>──<   N:M (muchos a muchos)
```

### Concepto 7: Cardinalidades

**1:1 (Uno a Uno)**
```
Usuario ─── Perfil
Cada usuario tiene 1 perfil
Cada perfil pertenece a 1 usuario
```

**1:N (Uno a Muchos)**
```
Cliente ───< Orden
Cada cliente puede tener muchas órdenes
Cada orden pertenece a 1 cliente
```

**N:M (Muchos a Muchos)**
```
Estudiante >──< Curso
Cada estudiante puede tomar muchos cursos
Cada curso puede tener muchos estudiantes

Requiere tabla intermedia:
estudiante_id | curso_id
1             | 101
1             | 102
2             | 101
```

---

## Parte 3: Modelado Dimensional (OLAP)

### Concepto 8: OLTP vs OLAP

| Aspecto    | OLTP                   | OLAP                            |
| ---------- | ---------------------- | ------------------------------- |
| Propósito  | Transacciones diarias  | Análisis y reportes             |
| Usuarios   | Miles (app users)      | Pocos (analistas)               |
| Queries    | Simples, rápidas       | Complejas, lentas               |
| Escrituras | Muchas (INSERT/UPDATE) | Pocas (batch loads)             |
| Lecturas   | Por ID, pocas filas    | Agregaciones, millones de filas |
| Diseño     | Normalizado (3NF)      | Desnormalizado (Star/Snowflake) |
| Ejemplo    | Sistema de ventas      | Data Warehouse de ventas        |

**Analogía**:
- **OLTP**: Caja registradora (transacciones rápidas individuales)
- **OLAP**: Hoja de Excel con gráficos (análisis agregado)

---

### Concepto 9: Star Schema (Esquema Estrella)

El diseño más común para Data Warehouses.

**Estructura**:
- **1 tabla de hechos** (centro): Métricas numéricas
- **N tablas de dimensiones** (puntas): Contexto descriptivo

```
       ┌─────────────┐
       │  dim_fecha  │
       └──────┬──────┘
              │
┌──────────┐  │  ┌──────────────┐
│dim_cliente├──┼──┤ fact_ventas  │
└──────────┘  │  └──────┬───────┘
              │         │
       ┌──────┴──────┐  │
       │ dim_producto├──┘
       └─────────────┘
```

**Tabla de Hechos (Fact Table)**:
```sql
CREATE TABLE fact_ventas (
    venta_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER REFERENCES dim_fecha(fecha_id),
    cliente_id INTEGER REFERENCES dim_cliente(cliente_id),
    producto_id INTEGER REFERENCES dim_producto(producto_id),
    -- Métricas (aditivas)
    cantidad INTEGER,
    monto_venta NUMERIC(10,2),
    costo NUMERIC(10,2),
    ganancia NUMERIC(10,2)
);
```

**Tablas de Dimensiones**:
```sql
CREATE TABLE dim_cliente (
    cliente_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    email VARCHAR(200),
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    segmento VARCHAR(50)  -- 'Premium', 'Regular', 'Nuevo'
);

CREATE TABLE dim_producto (
    producto_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    categoria VARCHAR(100),
    subcategoria VARCHAR(100),
    marca VARCHAR(100),
    precio_lista NUMERIC(10,2)
);

CREATE TABLE dim_fecha (
    fecha_id INTEGER PRIMARY KEY,
    fecha DATE,
    dia INTEGER,
    mes INTEGER,
    anio INTEGER,
    trimestre INTEGER,
    nombre_mes VARCHAR(20),
    dia_semana VARCHAR(20),
    es_fin_semana BOOLEAN
);
```

**Query ejemplo**:
```sql
-- Total ventas por categoría en Q4 2024
SELECT
    p.categoria,
    SUM(v.monto_venta) as total_ventas,
    COUNT(*) as num_transacciones
FROM fact_ventas v
JOIN dim_producto p ON v.producto_id = p.producto_id
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024 AND f.trimestre = 4
GROUP BY p.categoria
ORDER BY total_ventas DESC;
```

**Ventajas Star Schema**:
- ✅ Queries simples (pocos JOINs)
- ✅ Performance excelente (desnormalizado)
- ✅ Fácil de entender para analistas
- ✅ Compatible con herramientas BI

---

### Concepto 10: Snowflake Schema

Star Schema pero con dimensiones **normalizadas**.

```
              ┌──────────┐
              │dim_fecha │
              └────┬─────┘
                   │
┌──────────┐       │      ┌─────────────┐
│dim_ciudad├───────┼──────┤ fact_ventas │
└────┬─────┘       │      └──────┬──────┘
     │             │             │
┌────┴────┐  ┌─────┴──────┐  ┌──┴────────┐
│dim_pais │  │dim_producto│  │dim_marca  │
└─────────┘  └────┬───────┘  └───────────┘
                  │
             ┌────┴──────┐
             │dim_categoria│
             └───────────┘
```

**Ventajas**:
- ✅ Menor redundancia (más normalizado)
- ✅ Usa menos espacio

**Desventajas**:
- ❌ Más JOINs (queries más complejas)
- ❌ Ligeramente más lento

**Regla general**: **Usa Star Schema** en la mayoría de casos. Solo usa Snowflake si el espacio es muy limitado.

---

### Concepto 11: Métricas Aditivas, Semi-aditivas y No-aditivas

#### Aditivas (se pueden sumar en todas dimensiones)
```sql
-- Cantidad de ventas: puedes sumarla por fecha, producto, cliente
SUM(cantidad)  ✅
SUM(monto_venta)  ✅
```

#### Semi-aditivas (solo se suman en algunas dimensiones)
```sql
-- Balance de cuenta: puedes sumarlo por clientes, NO por fechas
-- (sumar balance del lunes + martes no tiene sentido)
AVG(balance) por fecha  ✅
SUM(balance) por cliente  ✅
SUM(balance) por fecha  ❌
```

#### No-aditivas (nunca se suman)
```sql
-- Precio unitario, ratios, porcentajes
AVG(precio_unitario)  ✅
SUM(precio_unitario)  ❌ (sin sentido)

-- Margen (ratio)
AVG(margen_porcentaje)  ✅
SUM(margen_porcentaje)  ❌
```

---

### Concepto 12: Slowly Changing Dimensions (SCD)

**Problema**: Los datos de dimensiones cambian con el tiempo.

Ejemplo: Cliente "Ana" vivía en "Madrid", ahora vive en "Barcelona". ¿Cómo manejarlo?

#### SCD Type 1: Sobrescribir

```sql
-- Antes
cliente_id | nombre | ciudad
1          | Ana    | Madrid

-- Después (UPDATE)
cliente_id | nombre | ciudad
1          | Ana    | Barcelona

-- Se pierde historial
```

**Cuándo usar**: No te importa el historial (ej: correcciones de typos).

#### SCD Type 2: Agregar nueva fila

```sql
-- Antes
cliente_id | nombre | ciudad   | valido_desde | valido_hasta | es_actual
1          | Ana    | Madrid   | 2020-01-01   | 2024-10-31   | FALSE
```

```sql
-- Después (INSERT nueva fila)
cliente_id | nombre | ciudad     | valido_desde | valido_hasta | es_actual
1          | Ana    | Madrid     | 2020-01-01   | 2024-10-31   | FALSE
2          | Ana    | Barcelona  | 2024-11-01   | 9999-12-31   | TRUE
```

**Ventajas**: Historial completo preservado.

**Cuándo usar**: Necesitas análisis histórico preciso (ej: "¿cuántas ventas en Madrid cuando Ana vivía ahí?").

#### SCD Type 3: Agregar columna

```sql
cliente_id | nombre | ciudad_actual | ciudad_anterior
1          | Ana    | Barcelona     | Madrid
```

**Cuándo usar**: Solo necesitas el valor anterior inmediato.

---

## Parte 4: Decisiones de Diseño

### Concepto 13: Normalizar vs Desnormalizar

#### Normalizar (3NF) cuando:
- ✅ Sistema OLTP (transacciones)
- ✅ Muchas escrituras
- ✅ Integridad referencial crítica
- ✅ Datos cambian frecuentemente

#### Desnormalizar (Star) cuando:
- ✅ Sistema OLAP (análisis)
- ✅ Pocas escrituras, muchas lecturas
- ✅ Performance de queries crítica
- ✅ Datos son históricamente estables

---

## Checklist de Aprendizaje

### Normalización
- [ ] Entiendo qué es normalización y por qué existe
- [ ] Puedo identificar si una tabla está en 1NF
- [ ] Puedo identificar si una tabla está en 2NF
- [ ] Puedo identificar si una tabla está en 3NF
- [ ] Sé cuándo NO normalizar (OLAP)

### Diagramas ER
- [ ] Puedo dibujar un diagrama ER básico
- [ ] Entiendo cardinalidades (1:1, 1:N, N:M)
- [ ] Sé cómo manejar N:M con tabla intermedia

### Modelado Dimensional
- [ ] Entiendo diferencia entre OLTP y OLAP
- [ ] Puedo diseñar un Star Schema básico
- [ ] Sé qué es una tabla de hechos vs dimensión
- [ ] Entiendo SCD Type 1 vs Type 2
- [ ] Sé cuándo desnormalizar

---

## Errores Comunes

### Error 1: Normalizar un Data Warehouse

```sql
-- ❌ MAL: DWH en 3NF requiere 7 JOINs para un reporte simple
-- Lento e innecesario

-- ✅ BIEN: Star Schema, 2-3 JOINs máximo
```

### Error 2: Desnormalizar un sistema transaccional

```sql
-- ❌ MAL: OLTP desnormalizado = anomalías de actualización

-- ✅ BIEN: OLTP normalizado (3NF)
```

### Error 3: No considerar el crecimiento

```sql
-- ❌ MAL: Diseño que funciona con 10K filas pero no con 10M

-- ✅ BIEN: Considerar volumen futuro desde el diseño
```

---

## Recursos Adicionales

### Libros (altamente recomendados)
- **"The Data Warehouse Toolkit"** - Ralph Kimball ⭐⭐⭐⭐⭐
- **"Database Design for Mere Mortals"** - Michael J. Hernandez

### Herramientas
- [draw.io](https://app.diagrams.net/) - Diagramas ER
- [dbdiagram.io](https://dbdiagram.io/) - Diseño de esquemas
- [Lucidchart](https://www.lucidchart.com/) - Diagramas profesionales

### Tutoriales
- [Database Normalization Explained](https://www.guru99.com/database-normalization.html)
- [Star Schema Tutorial](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/)

---

**Próximos pasos**: Lee **02-EJEMPLOS.md** para ver modelado de datos en acción.

**Tiempo de lectura:** 30-40 minutos
**Última actualización:** 2025-10-25

¡Domina el arte del modelado! 📐
---

## 🧭 Navegación

⬅️ **Anterior**: [MongoDB - Proyecto Práctico](../tema-2-mongodb/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
