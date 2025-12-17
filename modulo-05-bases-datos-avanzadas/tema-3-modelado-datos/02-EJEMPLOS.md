# Ejemplos Prácticos: Modelado de Datos

## Ejemplo 1: Normalización Completa (1NF → 3NF) - Nivel: Básico ⭐

### Contexto

**StreamFlix** es una plataforma de streaming de películas. Actualmente tienen una tabla desnormalizada con problemas de redundancia. Tu tarea es normalizarla hasta 3NF.

### Tabla Inicial (0NF - Sin Normalizar)

```
suscripciones
id | usuario_nombre | usuario_email    | plan_nombre | plan_precio | peliculas_vistas
1  | Ana López      | ana@email.com    | Premium     | 12.99       | "Inception, Matrix, Avatar"
2  | Carlos Ruiz    | carlos@email.com | Básico      | 7.99        | "Titanic"
3  | Ana López      | ana@email.com    | Premium     | 12.99       | "Interstellar, Dune"
```

**Problemas identificados**:
1. ❌ Datos de usuario repetidos (Ana aparece 2 veces)
2. ❌ Datos de plan repetidos
3. ❌ `peliculas_vistas` tiene múltiples valores en una celda (viola 1NF)
4. ❌ Si Ana cambia su email, hay que actualizar múltiples filas
5. ❌ Si el precio del plan Premium cambia, hay que actualizar muchas filas

---

### Paso 1: Aplicar Primera Forma Normal (1NF)

**Regla 1NF**: Cada celda debe contener UN valor atómico.

```sql
-- Tabla: suscripciones_1nf
CREATE TABLE suscripciones_1nf (
    id SERIAL PRIMARY KEY,
    usuario_nombre VARCHAR(100),
    usuario_email VARCHAR(150),
    plan_nombre VARCHAR(50),
    plan_precio NUMERIC(5,2),
    pelicula_vista VARCHAR(100)  -- ¡Un valor por fila!
);

-- Datos:
id | usuario_nombre | usuario_email    | plan_nombre | plan_precio | pelicula_vista
1  | Ana López      | ana@email.com    | Premium     | 12.99       | Inception
2  | Ana López      | ana@email.com    | Premium     | 12.99       | Matrix
3  | Ana López      | ana@email.com    | Premium     | 12.99       | Avatar
4  | Carlos Ruiz    | carlos@email.com | Básico      | 7.99        | Titanic
5  | Ana López      | ana@email.com    | Premium     | 12.99       | Interstellar
6  | Ana López      | ana@email.com    | Premium     | 12.99       | Dune
```

**✅ Cumple 1NF**: Valores atómicos, cada fila única.

**⚠️ Aún tiene problemas**: Redundancia masiva de datos de usuario y plan.

---

### Paso 2: Aplicar Segunda Forma Normal (2NF)

**Regla 2NF**: En 1NF + columnas no-PK deben depender de TODA la PK.

**Análisis**: Si usáramos PK compuesta `(usuario_email, pelicula_vista)`:
- `plan_nombre` y `plan_precio` solo dependen de `usuario_email`, no de `pelicula_vista`
- Esto viola 2NF

**Solución**: Separar en tablas según dependencias.

```sql
-- Tabla 1: usuarios
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    plan_nombre VARCHAR(50)
);

-- Datos:
usuario_id | nombre       | email            | plan_nombre
1          | Ana López    | ana@email.com    | Premium
2          | Carlos Ruiz  | carlos@email.com | Básico

-- Tabla 2: planes
CREATE TABLE planes (
    plan_nombre VARCHAR(50) PRIMARY KEY,
    precio NUMERIC(5,2) NOT NULL,
    descripcion TEXT
);

-- Datos:
plan_nombre | precio | descripcion
Premium     | 12.99  | Acceso completo + Ultra HD
Básico      | 7.99   | Catálogo limitado + HD

-- Tabla 3: vistas_peliculas (relación usuario-película)
CREATE TABLE vistas_peliculas (
    vista_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id),
    pelicula VARCHAR(100),
    fecha_vista TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos:
vista_id | usuario_id | pelicula      | fecha_vista
1        | 1          | Inception     | 2024-11-01 20:00:00
2        | 1          | Matrix        | 2024-11-02 21:30:00
3        | 1          | Avatar        | 2024-11-03 19:00:00
4        | 2          | Titanic       | 2024-11-01 22:00:00
5        | 1          | Interstellar  | 2024-11-05 20:15:00
6        | 1          | Dune          | 2024-11-06 21:00:00
```

**✅ Cumple 2NF**: Eliminamos dependencias parciales.

**⚠️ Aún tiene problema**: `plan_nombre` en `usuarios` depende transitivamente (usuario → plan_nombre → precio).

---

### Paso 3: Aplicar Tercera Forma Normal (3NF)

**Regla 3NF**: En 2NF + eliminar dependencias transitivas.

**Problema detectado**: `usuarios.plan_nombre` crea dependencia transitiva con `planes`.

**Solución Final**:

```sql
-- Tabla 1: usuarios (sin plan_nombre)
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

-- Tabla 2: planes
CREATE TABLE planes (
    plan_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    precio NUMERIC(5,2) NOT NULL,
    descripcion TEXT
);

-- Tabla 3: suscripciones (relación usuario-plan)
CREATE TABLE suscripciones (
    suscripcion_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id),
    plan_id INTEGER REFERENCES planes(plan_id),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activa BOOLEAN DEFAULT TRUE
);

-- Tabla 4: peliculas (nueva, normalizada)
CREATE TABLE peliculas (
    pelicula_id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) UNIQUE NOT NULL,
    director VARCHAR(100),
    anio INTEGER,
    duracion_min INTEGER
);

-- Tabla 5: vistas_peliculas (relación usuario-película)
CREATE TABLE vistas_peliculas (
    vista_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id),
    pelicula_id INTEGER REFERENCES peliculas(pelicula_id),
    fecha_vista TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    porcentaje_visto INTEGER CHECK (porcentaje_visto BETWEEN 0 AND 100)
);
```

**Datos finales**:

```sql
-- usuarios
usuario_id | nombre       | email
1          | Ana López    | ana@email.com
2          | Carlos Ruiz  | carlos@email.com

-- planes
plan_id | nombre   | precio | descripcion
1       | Premium  | 12.99  | Acceso completo + Ultra HD
2       | Básico   | 7.99   | Catálogo limitado + HD

-- suscripciones
suscripcion_id | usuario_id | plan_id | fecha_inicio | activa
1              | 1          | 1       | 2024-01-01   | TRUE
2              | 2          | 2       | 2024-06-15   | TRUE

-- peliculas
pelicula_id | titulo       | director            | anio | duracion_min
1           | Inception    | Christopher Nolan   | 2010 | 148
2           | Matrix       | Wachowski Sisters   | 1999 | 136
3           | Avatar       | James Cameron       | 2009 | 162
4           | Titanic      | James Cameron       | 1997 | 195
5           | Interstellar | Christopher Nolan   | 2014 | 169
6           | Dune         | Denis Villeneuve    | 2021 | 155

-- vistas_peliculas
vista_id | usuario_id | pelicula_id | fecha_vista          | porcentaje_visto
1        | 1          | 1           | 2024-11-01 20:00:00  | 100
2        | 1          | 2           | 2024-11-02 21:30:00  | 100
3        | 1          | 3           | 2024-11-03 19:00:00  | 75
4        | 2          | 4           | 2024-11-01 22:00:00  | 100
5        | 1          | 5           | 2024-11-05 20:15:00  | 100
6        | 1          | 6           | 2024-11-06 21:00:00  | 60
```

---

### Resultado: ✅ 3NF Alcanzado

**Beneficios**:
- ✅ **Cero redundancia**: Cada dato está en un solo lugar
- ✅ **Actualizaciones simples**: Cambiar email de Ana → 1 UPDATE
- ✅ **Integridad referencial**: FKs garantizan consistencia
- ✅ **Escalable**: Agregar nuevo plan → INSERT en `planes`

**Query ejemplo** (datos normalizados):
```sql
-- Películas vistas por Ana en Noviembre 2024
SELECT
    u.nombre,
    p.titulo,
    v.fecha_vista,
    v.porcentaje_visto
FROM vistas_peliculas v
JOIN usuarios u ON v.usuario_id = u.usuario_id
JOIN peliculas p ON v.pelicula_id = p.pelicula_id
WHERE u.email = 'ana@email.com'
    AND v.fecha_vista BETWEEN '2024-11-01' AND '2024-11-30'
ORDER BY v.fecha_vista;
```

---

## Ejemplo 2: Diagrama ER con Cardinalidades - Nivel: Intermedio ⭐⭐

### Contexto

**LibraryApp** necesita diseñar una base de datos para gestionar libros, autores, préstamos y usuarios.

**Requisitos**:
- Un libro puede tener múltiples autores (ej: libro co-escrito)
- Un autor puede escribir múltiples libros
- Un usuario puede tener múltiples préstamos activos
- Un préstamo es de UN libro a UN usuario
- Queremos rastrear cuándo se prestó y devolvió cada libro

---

### Análisis de Relaciones

1. **Libro ↔ Autor**: **N:M** (Muchos a Muchos)
   - Un libro puede tener varios autores
   - Un autor puede escribir varios libros
   - Requiere tabla intermedia

2. **Usuario → Préstamo**: **1:N** (Uno a Muchos)
   - Un usuario puede tener muchos préstamos
   - Un préstamo pertenece a un usuario

3. **Libro → Préstamo**: **1:N** (Uno a Muchos)
   - Un libro puede ser prestado muchas veces (histórico)
   - Cada préstamo es de un libro

---

### Diagrama ER (Textual)

```
┌──────────────┐                ┌──────────────┐
│   USUARIO    │                │    LIBRO     │
├──────────────┤                ├──────────────┤
│ usuario_id PK│                │ libro_id PK  │
│ nombre       │                │ titulo       │
│ email        │                │ isbn         │
│ telefono     │                │ editorial    │
│ fecha_alta   │                │ anio_pub     │
└──────┬───────┘                │ categoria    │
       │                        └──────┬───────┘
       │ 1                             │
       │                               │ N
       │ tiene                         │ escrito_por
       │                               │
       │ N                             │ N
       ▼                               ▼
┌──────────────┐                ┌──────────────┐
│  PRESTAMO    │                │ LIBRO_AUTOR  │
├──────────────┤                ├──────────────┤
│ prestamo_id  │                │ libro_id FK  │
│ usuario_id FK│                │ autor_id FK  │
│ libro_id FK  │                └──────┬───────┘
│ fecha_prest  │                       │ N
│ fecha_dev    │                       │
│ devuelto BOOL│                       │
└──────────────┘                       │
                                       │ 1
                                       ▼
                                ┌──────────────┐
                                │    AUTOR     │
                                ├──────────────┤
                                │ autor_id PK  │
                                │ nombre       │
                                │ nacionalidad │
                                │ anio_nac     │
                                └──────────────┘
```

---

### Implementación SQL

```sql
-- Tabla: usuarios
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_alta DATE DEFAULT CURRENT_DATE
);

-- Tabla: autores
CREATE TABLE autores (
    autor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    nacionalidad VARCHAR(100),
    anio_nacimiento INTEGER
);

-- Tabla: libros
CREATE TABLE libros (
    libro_id SERIAL PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    editorial VARCHAR(150),
    anio_publicacion INTEGER,
    categoria VARCHAR(100)
);

-- Tabla intermedia: libro_autor (N:M)
CREATE TABLE libro_autor (
    libro_id INTEGER REFERENCES libros(libro_id),
    autor_id INTEGER REFERENCES autores(autor_id),
    orden_autor INTEGER DEFAULT 1,  -- Para co-autores (1=primer autor, 2=segundo)
    PRIMARY KEY (libro_id, autor_id)
);

-- Tabla: prestamos (relación 1:N con usuarios y libros)
CREATE TABLE prestamos (
    prestamo_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id) NOT NULL,
    libro_id INTEGER REFERENCES libros(libro_id) NOT NULL,
    fecha_prestamo DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    devuelto BOOLEAN DEFAULT FALSE,

    -- Constraint: no se puede prestar un libro no devuelto
    CHECK (fecha_devolucion_esperada > fecha_prestamo)
);

-- Índices para mejorar queries comunes
CREATE INDEX idx_prestamos_usuario ON prestamos(usuario_id);
CREATE INDEX idx_prestamos_libro ON prestamos(libro_id);
CREATE INDEX idx_prestamos_devuelto ON prestamos(devuelto);
```

---

### Datos de Ejemplo

```sql
-- Usuarios
INSERT INTO usuarios (nombre, email, telefono) VALUES
('María García', 'maria@email.com', '555-1234'),
('Pedro López', 'pedro@email.com', '555-5678'),
('Laura Martínez', 'laura@email.com', '555-9012');

-- Autores
INSERT INTO autores (nombre, nacionalidad, anio_nacimiento) VALUES
('Gabriel García Márquez', 'Colombia', 1927),
('J.K. Rowling', 'Reino Unido', 1965),
('Isaac Asimov', 'Estados Unidos', 1920),
('Neil Gaiman', 'Reino Unido', 1960),
('Terry Pratchett', 'Reino Unido', 1948);

-- Libros
INSERT INTO libros (titulo, isbn, editorial, anio_publicacion, categoria) VALUES
('Cien años de soledad', '978-0307474728', 'Editorial Sudamericana', 1967, 'Ficción'),
('Harry Potter y la Piedra Filosofal', '978-0439708180', 'Bloomsbury', 1997, 'Fantasía'),
('Fundación', '978-0553293357', 'Gnome Press', 1951, 'Ciencia Ficción'),
('Buenos Presagios', '978-0060853983', 'Workman', 1990, 'Fantasía');

-- Relación libro-autor
-- (Libro 1 tiene 1 autor, Libro 4 tiene 2 co-autores)
INSERT INTO libro_autor (libro_id, autor_id, orden_autor) VALUES
(1, 1, 1),  -- Cien años de soledad - García Márquez
(2, 2, 1),  -- Harry Potter - Rowling
(3, 3, 1),  -- Fundación - Asimov
(4, 4, 1),  -- Buenos Presagios - Gaiman (primer autor)
(4, 5, 2);  -- Buenos Presagios - Pratchett (co-autor)

-- Préstamos
INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo, fecha_devolucion_esperada, devuelto) VALUES
(1, 1, '2024-11-01', '2024-11-15', TRUE),   -- María prestó Cien años (devuelto)
(1, 2, '2024-11-10', '2024-11-24', FALSE),  -- María prestó Harry Potter (activo)
(2, 3, '2024-11-05', '2024-11-19', FALSE),  -- Pedro prestó Fundación (activo)
(3, 4, '2024-10-20', '2024-11-03', TRUE);   -- Laura prestó Buenos Presagios (devuelto tarde)

-- Actualizar devolución de Laura (tarde)
UPDATE prestamos
SET devuelto = TRUE, fecha_devolucion_real = '2024-11-08'
WHERE prestamo_id = 4;
```

---

### Queries de Ejemplo

```sql
-- 1. Libros con sus autores (maneja co-autores)
SELECT
    l.titulo,
    STRING_AGG(a.nombre, ', ' ORDER BY la.orden_autor) as autores,
    l.anio_publicacion
FROM libros l
JOIN libro_autor la ON l.libro_id = la.libro_id
JOIN autores a ON la.autor_id = a.autor_id
GROUP BY l.libro_id, l.titulo, l.anio_publicacion;

-- Resultado:
-- titulo                                | autores                          | anio
-- Cien años de soledad                 | Gabriel García Márquez           | 1967
-- Harry Potter y la Piedra Filosofal   | J.K. Rowling                    | 1997
-- Fundación                            | Isaac Asimov                     | 1951
-- Buenos Presagios                     | Neil Gaiman, Terry Pratchett     | 1990


-- 2. Préstamos activos (no devueltos)
SELECT
    u.nombre as usuario,
    l.titulo as libro,
    p.fecha_prestamo,
    p.fecha_devolucion_esperada,
    CURRENT_DATE - p.fecha_devolucion_esperada as dias_retraso
FROM prestamos p
JOIN usuarios u ON p.usuario_id = u.usuario_id
JOIN libros l ON p.libro_id = l.libro_id
WHERE p.devuelto = FALSE;

-- Resultado:
-- usuario       | libro                            | fecha_prestamo | fecha_dev_esp | dias_retraso
-- María García  | Harry Potter y la Piedra...      | 2024-11-10     | 2024-11-24    | -12 (a tiempo)
-- Pedro López   | Fundación                        | 2024-11-05     | 2024-11-19    | -7 (a tiempo)


-- 3. Usuarios con préstamos retrasados
SELECT DISTINCT
    u.usuario_id,
    u.nombre,
    u.email,
    COUNT(*) as libros_retrasados
FROM prestamos p
JOIN usuarios u ON p.usuario_id = u.usuario_id
WHERE p.devuelto = FALSE
    AND p.fecha_devolucion_esperada < CURRENT_DATE
GROUP BY u.usuario_id, u.nombre, u.email;


-- 4. Historial de préstamos de un libro
SELECT
    l.titulo,
    u.nombre as prestado_a,
    p.fecha_prestamo,
    p.fecha_devolucion_real,
    CASE
        WHEN p.devuelto = FALSE THEN 'Actualmente prestado'
        WHEN p.fecha_devolucion_real <= p.fecha_devolucion_esperada THEN 'Devuelto a tiempo'
        ELSE 'Devuelto con retraso'
    END as estado
FROM prestamos p
JOIN libros l ON p.libro_id = l.libro_id
JOIN usuarios u ON p.usuario_id = u.usuario_id
WHERE l.libro_id = 4  -- Buenos Presagios
ORDER BY p.fecha_prestamo DESC;
```

---

### Interpretación del Diseño

**Ventajas de este modelo**:
1. ✅ **Flexibilidad**: Soporta co-autores sin problemas
2. ✅ **Historial completo**: Todos los préstamos se guardan
3. ✅ **Integridad**: FKs previenen inconsistencias
4. ✅ **Queries eficientes**: Índices en columnas clave

**Decisiones de diseño**:
- **N:M entre Libro-Autor**: Tabla intermedia `libro_autor` con campo `orden_autor` para co-autores
- **1:N Usuario-Préstamo**: FK `usuario_id` en `prestamos`
- **1:N Libro-Préstamo**: FK `libro_id` en `prestamos`
- **Soft delete**: Mantener historial de préstamos en lugar de borrar

---

## Ejemplo 3: Star Schema para Data Warehouse - Nivel: Intermedio ⭐⭐

### Contexto

**EcommerceX** es una tienda online con millones de transacciones. El equipo de analytics necesita un Data Warehouse para responder preguntas como:

- ¿Cuál fue la venta total por categoría en Q4 2024?
- ¿Qué productos generan más ganancia?
- ¿Cuál es el comportamiento de compra por día de la semana?
- ¿Qué ciudades generan más ingresos?

El sistema transaccional (OLTP) está normalizado en 3NF, pero es muy lento para análisis.

---

### Sistema OLTP Actual (Normalizado 3NF)

```sql
-- Sistema transaccional (simplificado)
CREATE TABLE clientes (
    cliente_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    email VARCHAR(150),
    ciudad_id INTEGER REFERENCES ciudades(ciudad_id)
);

CREATE TABLE ciudades (
    ciudad_id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    pais_id INTEGER REFERENCES paises(pais_id)
);

CREATE TABLE paises (
    pais_id INTEGER PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE productos (
    producto_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    categoria_id INTEGER REFERENCES categorias(categoria_id),
    precio NUMERIC(10,2),
    costo NUMERIC(10,2)
);

CREATE TABLE categorias (
    categoria_id INTEGER PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE ventas (
    venta_id INTEGER PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    producto_id INTEGER REFERENCES productos(producto_id),
    fecha TIMESTAMP,
    cantidad INTEGER,
    precio_unitario NUMERIC(10,2)
);
```

**Problema**: Query para "Ventas por país en 2024" requiere **6 JOINs**:
```sql
-- ❌ LENTO: 6 JOINs para una consulta simple
SELECT
    pais.nombre,
    SUM(v.cantidad * v.precio_unitario) as total_ventas
FROM ventas v
JOIN clientes c ON v.cliente_id = c.cliente_id
JOIN ciudades ci ON c.ciudad_id = ci.ciudad_id
JOIN paises p ON ci.pais_id = p.pais_id
JOIN productos pr ON v.producto_id = pr.producto_id
JOIN categorias cat ON pr.categoria_id = cat.categoria_id
WHERE EXTRACT(YEAR FROM v.fecha) = 2024
GROUP BY p.nombre;
```

---

### Diseño Star Schema (OLAP)

**Objetivo**: Reducir JOINs, desnormalizar, optimizar para lecturas analíticas.

```
                 ┌────────────────┐
                 │   dim_fecha    │
                 ├────────────────┤
                 │ fecha_id PK    │
                 │ fecha          │
                 │ anio           │
                 │ mes            │
                 │ trimestre      │
                 │ dia_semana     │
                 │ es_fin_semana  │
                 └────────┬───────┘
                          │
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        │                 │                 │
┌───────┴────────┐ ┌─────┴──────────┐ ┌────┴───────────┐
│ dim_cliente    │ │  fact_ventas   │ │ dim_producto   │
├────────────────┤ ├────────────────┤ ├────────────────┤
│ cliente_id PK  │ │ venta_id PK    │ │ producto_id PK │
│ nombre         │ │ fecha_id FK    │ │ nombre         │
│ email          │ │ cliente_id FK  │ │ categoria      │
│ ciudad         │ │ producto_id FK │ │ subcategoria   │
│ pais           │ │ cantidad       │ │ marca          │
│ segmento       │ │ precio_unit    │ │ precio_lista   │
└────────────────┘ │ costo_unit     │ │ costo          │
                   │ monto_venta    │ └────────────────┘
                   │ ganancia       │
                   └────────────────┘
```

---

### Implementación SQL del Star Schema

```sql
-- ===== DIMENSIONES =====

-- Dimensión: Fecha (pre-poblada con todos los días)
CREATE TABLE dim_fecha (
    fecha_id INTEGER PRIMARY KEY,  -- YYYYMMDD ej: 20241115
    fecha DATE NOT NULL UNIQUE,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    mes_nombre VARCHAR(20) NOT NULL,
    dia_mes INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,  -- 1=Lunes, 7=Domingo
    dia_semana_nombre VARCHAR(20) NOT NULL,
    es_fin_semana BOOLEAN NOT NULL,
    es_festivo BOOLEAN DEFAULT FALSE
);

-- Poblar con datos de 2020-2030
INSERT INTO dim_fecha (fecha_id, fecha, anio, mes, trimestre, mes_nombre, dia_mes, dia_semana, dia_semana_nombre, es_fin_semana)
SELECT
    TO_CHAR(fecha, 'YYYYMMDD')::INTEGER as fecha_id,
    fecha,
    EXTRACT(YEAR FROM fecha)::INTEGER as anio,
    EXTRACT(MONTH FROM fecha)::INTEGER as mes,
    EXTRACT(QUARTER FROM fecha)::INTEGER as trimestre,
    TO_CHAR(fecha, 'Month') as mes_nombre,
    EXTRACT(DAY FROM fecha)::INTEGER as dia_mes,
    EXTRACT(DOW FROM fecha)::INTEGER as dia_semana,
    TO_CHAR(fecha, 'Day') as dia_semana_nombre,
    EXTRACT(DOW FROM fecha) IN (0, 6) as es_fin_semana
FROM generate_series('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) fecha;


-- Dimensión: Cliente (desnormalizada - incluye ciudad y país)
CREATE TABLE dim_cliente (
    cliente_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150),
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    segmento VARCHAR(50),  -- 'Premium', 'Regular', 'Nuevo'
    fecha_registro DATE
);


-- Dimensión: Producto (desnormalizada - incluye categoría)
CREATE TABLE dim_producto (
    producto_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    subcategoria VARCHAR(100),
    marca VARCHAR(100),
    precio_lista NUMERIC(10,2) NOT NULL,
    costo NUMERIC(10,2) NOT NULL
);


-- ===== TABLA DE HECHOS =====

CREATE TABLE fact_ventas (
    venta_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER NOT NULL REFERENCES dim_fecha(fecha_id),
    cliente_id INTEGER NOT NULL REFERENCES dim_cliente(cliente_id),
    producto_id INTEGER NOT NULL REFERENCES dim_producto(producto_id),

    -- Métricas aditivas
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL,
    costo_unitario NUMERIC(10,2) NOT NULL,
    monto_venta NUMERIC(12,2) NOT NULL,  -- cantidad * precio_unitario
    costo_total NUMERIC(12,2) NOT NULL,  -- cantidad * costo_unitario
    ganancia NUMERIC(12,2) NOT NULL      -- monto_venta - costo_total
);

-- Índices para optimizar queries analíticas
CREATE INDEX idx_fact_ventas_fecha ON fact_ventas(fecha_id);
CREATE INDEX idx_fact_ventas_cliente ON fact_ventas(cliente_id);
CREATE INDEX idx_fact_ventas_producto ON fact_ventas(producto_id);

-- Índice compuesto para queries por período
CREATE INDEX idx_fact_ventas_fecha_producto ON fact_ventas(fecha_id, producto_id);
```

---

### Datos de Ejemplo

```sql
-- Dimensión Cliente
INSERT INTO dim_cliente VALUES
(1, 'María González', 'maria@email.com', 'Madrid', 'España', 'Premium', '2023-01-15'),
(2, 'Carlos López', 'carlos@email.com', 'Barcelona', 'España', 'Regular', '2023-06-20'),
(3, 'Ana Martínez', 'ana@email.com', 'Buenos Aires', 'Argentina', 'Premium', '2022-11-10'),
(4, 'Pedro Sánchez', 'pedro@email.com', 'Ciudad de México', 'México', 'Nuevo', '2024-10-01');

-- Dimensión Producto
INSERT INTO dim_producto VALUES
(101, 'Laptop Pro 15"', 'Electrónica', 'Computadoras', 'TechBrand', 1299.99, 800.00),
(102, 'Mouse Inalámbrico', 'Electrónica', 'Accesorios', 'TechBrand', 29.99, 12.00),
(103, 'Teclado Mecánico', 'Electrónica', 'Accesorios', 'KeyMaster', 89.99, 40.00),
(104, 'Monitor 27" 4K', 'Electrónica', 'Monitores', 'ViewPro', 449.99, 250.00),
(105, 'Auriculares Bluetooth', 'Electrónica', 'Audio', 'SoundMax', 149.99, 70.00);

-- Tabla de Hechos (ventas)
INSERT INTO fact_ventas (fecha_id, cliente_id, producto_id, cantidad, precio_unitario, costo_unitario, monto_venta, costo_total, ganancia) VALUES
-- Ventas de Noviembre 2024
(20241101, 1, 101, 1, 1299.99, 800.00, 1299.99, 800.00, 499.99),
(20241101, 1, 102, 2, 29.99, 12.00, 59.98, 24.00, 35.98),
(20241103, 2, 103, 1, 89.99, 40.00, 89.99, 40.00, 49.99),
(20241105, 3, 104, 1, 449.99, 250.00, 449.99, 250.00, 199.99),
(20241107, 1, 105, 1, 149.99, 70.00, 149.99, 70.00, 79.99),
(20241108, 4, 102, 3, 29.99, 12.00, 89.97, 36.00, 53.97),
(20241110, 2, 101, 1, 1299.99, 800.00, 1299.99, 800.00, 499.99),
(20241112, 3, 105, 2, 149.99, 70.00, 299.98, 140.00, 159.98);
```

---

### Queries Analíticas (Muy Rápidas)

```sql
-- 1. Ventas totales por categoría en Noviembre 2024
SELECT
    p.categoria,
    SUM(v.monto_venta) as total_ventas,
    SUM(v.ganancia) as total_ganancia,
    COUNT(*) as num_transacciones,
    ROUND(SUM(v.ganancia) / SUM(v.monto_venta) * 100, 2) as margen_porcentaje
FROM fact_ventas v
JOIN dim_producto p ON v.producto_id = p.producto_id
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024 AND f.mes = 11
GROUP BY p.categoria
ORDER BY total_ventas DESC;

-- Resultado:
-- categoria    | total_ventas | total_ganancia | num_transacciones | margen_porcentaje
-- Electrónica  | 3739.89      | 1579.89        | 8                 | 42.25


-- 2. Top 3 productos por ganancia
SELECT
    p.nombre,
    p.categoria,
    SUM(v.cantidad) as unidades_vendidas,
    SUM(v.monto_venta) as total_ventas,
    SUM(v.ganancia) as total_ganancia
FROM fact_ventas v
JOIN dim_producto p ON v.producto_id = p.producto_id
GROUP BY p.producto_id, p.nombre, p.categoria
ORDER BY total_ganancia DESC
LIMIT 3;

-- Resultado:
-- nombre                   | categoria    | unidades | total_ventas | total_ganancia
-- Laptop Pro 15"          | Electrónica  | 2        | 2599.98      | 999.98
-- Monitor 27" 4K          | Electrónica  | 1        | 449.99       | 199.99
-- Auriculares Bluetooth   | Electrónica  | 3        | 449.97       | 239.97


-- 3. Ventas por país (2 JOINs vs 6 en OLTP)
SELECT
    c.pais,
    COUNT(DISTINCT c.cliente_id) as clientes_activos,
    SUM(v.monto_venta) as total_ventas,
    AVG(v.monto_venta) as ticket_promedio
FROM fact_ventas v
JOIN dim_cliente c ON v.cliente_id = c.cliente_id
GROUP BY c.pais
ORDER BY total_ventas DESC;

-- Resultado:
-- pais        | clientes_activos | total_ventas | ticket_promedio
-- España      | 2                | 2899.94      | 644.43
-- Argentina   | 1                | 749.97       | 374.99
-- México      | 1                | 89.97        | 89.97


-- 4. Análisis por día de semana
SELECT
    f.dia_semana_nombre,
    f.es_fin_semana,
    COUNT(*) as num_ventas,
    SUM(v.monto_venta) as total_ventas,
    AVG(v.monto_venta) as ticket_promedio
FROM fact_ventas v
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
GROUP BY f.dia_semana, f.dia_semana_nombre, f.es_fin_semana
ORDER BY f.dia_semana;

-- Resultado:
-- dia_semana_nombre | es_fin_semana | num_ventas | total_ventas | ticket_promedio
-- Viernes          | TRUE          | 1          | 1299.99      | 1299.99
-- Sábado           | TRUE          | 1          | 59.98        | 59.98
-- Domingo          | TRUE          | 1          | 89.99        | 89.99
-- Martes           | FALSE         | 1          | 449.99       | 449.99
-- Jueves           | FALSE         | 2          | 239.96       | 119.98
-- ...
```

---

### Comparación OLTP vs OLAP

| Aspecto          | Sistema OLTP (Normalizado)         | Data Warehouse (Star Schema)   |
| ---------------- | ---------------------------------- | ------------------------------ |
| **JOINs**        | 6 JOINs para query simple          | 2-3 JOINs máximo               |
| **Performance**  | Lento en agregaciones              | Muy rápido                     |
| **Redundancia**  | Cero (3NF)                         | Alta (desnormalizado)          |
| **Tamaño**       | Menor                              | Mayor (por desnormalización)   |
| **Uso**          | Transacciones (INSERT/UPDATE)      | Analytics (SELECT con GROUP BY |
| **Actualizaciones** | Fáciles y frecuentes            | Batch loads periódicos         |

---

### Interpretación

**Ventajas del Star Schema**:
1. ✅ **Queries simples**: Pocos JOINs, fácil de entender
2. ✅ **Performance excelente**: Índices optimizados, pocos JOINs
3. ✅ **Dimensiones descriptivas**: Todo el contexto en una tabla
4. ✅ **Compatible con BI**: Herramientas como Tableau, Power BI lo entienden nativamente

**Proceso ETL (carga)**:
```python
# Pseudocódigo del proceso ETL
def cargar_fact_ventas(fecha):
    # Extraer de OLTP
    ventas_oltp = extraer_ventas_oltp(fecha)

    # Transformar
    for venta in ventas_oltp:
        # Lookup de claves surrogadas
        fecha_id = lookup_fecha_id(venta.fecha)
        cliente_id = lookup_cliente_id(venta.cliente_id)
        producto_id = lookup_producto_id(venta.producto_id)

        # Calcular métricas
        monto_venta = venta.cantidad * venta.precio_unitario
        costo_total = venta.cantidad * venta.costo_unitario
        ganancia = monto_venta - costo_total

        # Insertar en fact table
        insertar_fact_ventas(
            fecha_id, cliente_id, producto_id,
            venta.cantidad, venta.precio_unitario, venta.costo_unitario,
            monto_venta, costo_total, ganancia
        )
```

---

## Ejemplo 4: Slowly Changing Dimensions (SCD Type 2) - Nivel: Avanzado ⭐⭐⭐

### Contexto

**TelecomPro** es una empresa de telecomunicaciones con millones de clientes. Necesitan rastrear cambios en los planes de los clientes a lo largo del tiempo para análisis histórico preciso.

**Problema**:
- Cliente "Ana" contrató plan "Básico" en Enero 2023
- En Julio 2024 cambió a plan "Premium"
- **Pregunta analítica**: "¿Cuántos ingresos generaron clientes con plan Básico en Q1 2024?"
- Si sobreescribimos el plan de Ana (SCD Type 1), perdemos el hecho de que era "Básico" en Q1 2024

**Solución**: SCD Type 2 - Mantener historial completo de cambios.

---

### Diseño con SCD Type 2

```sql
-- Dimensión Cliente con SCD Type 2
CREATE TABLE dim_cliente_scd2 (
    cliente_key SERIAL PRIMARY KEY,          -- Clave surrogada (única por versión)
    cliente_id INTEGER NOT NULL,             -- ID del cliente en sistema OLTP
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150),
    plan VARCHAR(50) NOT NULL,
    ciudad VARCHAR(100),

    -- Campos de versionado SCD2
    fecha_inicio DATE NOT NULL,              -- Cuándo inició esta versión
    fecha_fin DATE,                          -- Cuándo terminó (NULL = activa)
    es_actual BOOLEAN NOT NULL DEFAULT TRUE,  -- TRUE solo para versión activa

    -- Constraint: solo una versión activa por cliente
    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio)
);

-- Índice para buscar versión actual de un cliente
CREATE INDEX idx_cliente_scd2_actual ON dim_cliente_scd2(cliente_id, es_actual);
CREATE INDEX idx_cliente_scd2_periodo ON dim_cliente_scd2(fecha_inicio, fecha_fin);


-- Tabla de hechos (ventas mensuales)
CREATE TABLE fact_ingresos_mensuales (
    ingreso_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER NOT NULL REFERENCES dim_fecha(fecha_id),
    cliente_key INTEGER NOT NULL REFERENCES dim_cliente_scd2(cliente_key),  -- FK a versión específica
    monto_ingreso NUMERIC(10,2) NOT NULL,
    minutos_usados INTEGER,
    datos_gb_usados NUMERIC(6,2)
);
```

---

### Escenario: Evolución de Cliente a lo largo del tiempo

```sql
-- ==== ENERO 2023: Ana se registra con plan Básico ====
INSERT INTO dim_cliente_scd2 (cliente_id, nombre, email, plan, ciudad, fecha_inicio, fecha_fin, es_actual) VALUES
(101, 'Ana López', 'ana@email.com', 'Básico', 'Madrid', '2023-01-15', NULL, TRUE);
-- cliente_key = 1

-- Ingresos de Ana con plan Básico (Enero-Junio 2024)
INSERT INTO fact_ingresos_mensuales (fecha_id, cliente_key, monto_ingreso, minutos_usados, datos_gb_usados) VALUES
(20240101, 1, 25.00, 300, 5.0),  -- Enero 2024
(20240201, 1, 25.00, 280, 4.5),  -- Febrero 2024
(20240301, 1, 25.00, 320, 6.2),  -- Marzo 2024
(20240401, 1, 25.00, 310, 5.8),  -- Abril 2024
(20240501, 1, 25.00, 290, 5.3),  -- Mayo 2024
(20240601, 1, 25.00, 305, 5.9);  -- Junio 2024


-- ==== JULIO 2024: Ana cambia a plan Premium ====

-- Paso 1: Cerrar versión anterior (Básico)
UPDATE dim_cliente_scd2
SET fecha_fin = '2024-07-01',
    es_actual = FALSE
WHERE cliente_key = 1;

-- Paso 2: Insertar nueva versión (Premium)
INSERT INTO dim_cliente_scd2 (cliente_id, nombre, email, plan, ciudad, fecha_inicio, fecha_fin, es_actual) VALUES
(101, 'Ana López', 'ana@email.com', 'Premium', 'Madrid', '2024-07-01', NULL, TRUE);
-- cliente_key = 2 (nueva versión)

-- Ingresos de Ana con plan Premium (Julio-Noviembre 2024)
INSERT INTO fact_ingresos_mensuales (fecha_id, cliente_key, monto_ingreso, minutos_usados, datos_gb_usados) VALUES
(20240701, 2, 45.00, 800, 25.0),   -- Julio 2024
(20240801, 2, 45.00, 820, 28.3),   -- Agosto 2024
(20240901, 2, 45.00, 790, 26.7),   -- Septiembre 2024
(20241001, 2, 45.00, 850, 30.1),   -- Octubre 2024
(20241101, 2, 45.00, 805, 27.8);   -- Noviembre 2024


-- ==== NOVIEMBRE 2024: Ana se muda a Barcelona ====

-- Paso 1: Cerrar versión actual (Premium Madrid)
UPDATE dim_cliente_scd2
SET fecha_fin = '2024-11-15',
    es_actual = FALSE
WHERE cliente_key = 2;

-- Paso 2: Insertar nueva versión (Premium Barcelona)
INSERT INTO dim_cliente_scd2 (cliente_id, nombre, email, plan, ciudad, fecha_inicio, fecha_fin, es_actual) VALUES
(101, 'Ana López', 'ana@email.com', 'Premium', 'Barcelona', '2024-11-15', NULL, TRUE);
-- cliente_key = 3 (nueva versión)
```

---

### Estado Final: 3 versiones históricas de Ana

```sql
SELECT * FROM dim_cliente_scd2 WHERE cliente_id = 101 ORDER BY cliente_key;
```

| cliente_key | cliente_id | nombre      | plan    | ciudad    | fecha_inicio | fecha_fin  | es_actual |
| ----------- | ---------- | ----------- | ------- | --------- | ------------ | ---------- | --------- |
| 1           | 101        | Ana López   | Básico  | Madrid    | 2023-01-15   | 2024-07-01 | FALSE     |
| 2           | 101        | Ana López   | Premium | Madrid    | 2024-07-01   | 2024-11-15 | FALSE     |
| 3           | 101        | Ana López   | Premium | Barcelona | 2024-11-15   | NULL       | TRUE      |

---

### Queries Analíticas con Historial

```sql
-- 1. Ingresos totales por plan en Q1 2024 (¡Incluye a Ana como "Básico"!)
SELECT
    c.plan,
    SUM(f.monto_ingreso) as ingresos_totales,
    COUNT(DISTINCT c.cliente_id) as clientes_unicos
FROM fact_ingresos_mensuales f
JOIN dim_cliente_scd2 c ON f.cliente_key = c.cliente_key
JOIN dim_fecha d ON f.fecha_id = d.fecha_id
WHERE d.anio = 2024
    AND d.trimestre = 1
GROUP BY c.plan;

-- Resultado:
-- plan    | ingresos_totales | clientes_unicos
-- Básico  | 75.00            | 1  (Ana con plan Básico)


-- 2. Ingresos de Ana a lo largo del tiempo (muestra cambio de plan)
SELECT
    c.plan,
    c.ciudad,
    d.anio,
    d.mes,
    f.monto_ingreso,
    f.datos_gb_usados
FROM fact_ingresos_mensuales f
JOIN dim_cliente_scd2 c ON f.cliente_key = c.cliente_key
JOIN dim_fecha d ON f.fecha_id = d.fecha_id
WHERE c.cliente_id = 101  -- Ana
ORDER BY d.fecha;

-- Resultado:
-- plan    | ciudad    | anio | mes | monto | datos_gb
-- Básico  | Madrid    | 2024 | 1   | 25.00 | 5.0
-- Básico  | Madrid    | 2024 | 2   | 25.00 | 4.5
-- Básico  | Madrid    | 2024 | 3   | 25.00 | 6.2
-- Básico  | Madrid    | 2024 | 4   | 25.00 | 5.8
-- Básico  | Madrid    | 2024 | 5   | 25.00 | 5.3
-- Básico  | Madrid    | 2024 | 6   | 25.00 | 5.9
-- Premium | Madrid    | 2024 | 7   | 45.00 | 25.0
-- Premium | Madrid    | 2024 | 8   | 45.00 | 28.3
-- Premium | Madrid    | 2024 | 9   | 45.00 | 26.7
-- Premium | Madrid    | 2024 | 10  | 45.00 | 30.1
-- Premium | Barcelona | 2024 | 11  | 45.00 | 27.8


-- 3. Clientes que cambiaron de plan Básico a Premium en 2024
SELECT DISTINCT
    basico.cliente_id,
    basico.nombre,
    basico.fecha_inicio as fecha_inicio_basico,
    premium.fecha_inicio as fecha_upgrade_premium,
    premium.fecha_inicio - basico.fecha_inicio as dias_en_basico
FROM dim_cliente_scd2 basico
JOIN dim_cliente_scd2 premium ON basico.cliente_id = premium.cliente_id
WHERE basico.plan = 'Básico'
    AND premium.plan = 'Premium'
    AND basico.fecha_fin IS NOT NULL
    AND premium.fecha_inicio >= '2024-01-01'
    AND premium.fecha_inicio = basico.fecha_fin;

-- Resultado:
-- cliente_id | nombre      | fecha_inicio_basico | fecha_upgrade_premium | dias_en_basico
-- 101        | Ana López   | 2023-01-15          | 2024-07-01            | 533


-- 4. Obtener versión actual de un cliente (para queries operacionales)
SELECT
    cliente_id,
    nombre,
    email,
    plan,
    ciudad,
    fecha_inicio
FROM dim_cliente_scd2
WHERE cliente_id = 101
    AND es_actual = TRUE;

-- Resultado:
-- cliente_id | nombre      | email          | plan    | ciudad    | fecha_inicio
-- 101        | Ana López   | ana@email.com  | Premium | Barcelona | 2024-11-15


-- 5. Clientes por plan en un punto específico del tiempo (ej: 2024-05-15)
SELECT
    plan,
    COUNT(*) as num_clientes
FROM dim_cliente_scd2
WHERE '2024-05-15' BETWEEN fecha_inicio AND COALESCE(fecha_fin, '9999-12-31')
GROUP BY plan;

-- Resultado muestra estado del mundo en 2024-05-15
-- (Ana tenía plan Básico en esa fecha)
```

---

### Proceso ETL para SCD Type 2

```python
# Pseudocódigo: Actualizar dimensión cliente con SCD Type 2
def actualizar_cliente_scd2(cliente_id, nuevos_datos):
    """
    Actualiza cliente aplicando SCD Type 2.
    """
    # Obtener versión actual del cliente
    version_actual = query(
        "SELECT * FROM dim_cliente_scd2 WHERE cliente_id = %s AND es_actual = TRUE",
        cliente_id
    )

    # Comparar atributos que rastreamos
    atributos_cambiados = []
    if version_actual.plan != nuevos_datos.plan:
        atributos_cambiados.append('plan')
    if version_actual.ciudad != nuevos_datos.ciudad:
        atributos_cambiados.append('ciudad')

    # Si hay cambios en atributos rastreados
    if atributos_cambiados:
        # Paso 1: Cerrar versión actual
        query(
            """
            UPDATE dim_cliente_scd2
            SET fecha_fin = CURRENT_DATE,
                es_actual = FALSE
            WHERE cliente_key = %s
            """,
            version_actual.cliente_key
        )

        # Paso 2: Insertar nueva versión
        nuevo_key = query(
            """
            INSERT INTO dim_cliente_scd2
            (cliente_id, nombre, email, plan, ciudad, fecha_inicio, fecha_fin, es_actual)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, NULL, TRUE)
            RETURNING cliente_key
            """,
            cliente_id, nuevos_datos.nombre, nuevos_datos.email,
            nuevos_datos.plan, nuevos_datos.ciudad
        )

        print(f"Cliente {cliente_id}: Creada nueva versión {nuevo_key}. Cambios: {atributos_cambiados}")
    else:
        # Si no hay cambios relevantes (ej: solo cambió email), hacer UPDATE simple
        query(
            """
            UPDATE dim_cliente_scd2
            SET email = %s
            WHERE cliente_key = %s
            """,
            nuevos_datos.email, version_actual.cliente_key
        )
```

---

### Comparación SCD Types

| Tipo           | Estrategia              | Historial | Complejidad | Uso                                    |
| -------------- | ----------------------- | --------- | ----------- | -------------------------------------- |
| **SCD Type 1** | Sobrescribir            | ❌ No     | Baja        | Correcciones, datos no importantes     |
| **SCD Type 2** | Nueva fila por cambio   | ✅ Completo | Alta      | Análisis histórico preciso             |
| **SCD Type 3** | Columnas previas/actual | ⚠️ Limitado | Media     | Solo último cambio (raro en práctica) |

---

### Interpretación

**Ventajas SCD Type 2**:
1. ✅ **Historial completo**: Puedes responder "¿Cómo eran las cosas en X fecha?"
2. ✅ **Análisis preciso**: Reportes históricos son exactos
3. ✅ **Auditoría**: Completo trail de cambios

**Desventajas SCD Type 2**:
1. ❌ **Complejidad**: Queries más complejas (JOIN con fechas)
2. ❌ **Tamaño**: Dimensión crece con cada cambio
3. ❌ **ETL complejo**: Lógica de actualización más sofisticada

**Cuándo usar SCD Type 2**:
- Necesitas análisis histórico preciso
- Cambios son relativamente infrecuentes
- Atributos importantes para análisis (plan, categoría, segmento)

**Cuándo NO usar SCD Type 2**:
- Atributos cambian muy frecuentemente (ej: balance de cuenta)
- No necesitas historial (ej: correcciones de typos)
- Dimensión se volvería demasiado grande

---

## Conclusión

Hemos visto:

1. **Normalización progresiva** (0NF → 1NF → 2NF → 3NF) para sistemas OLTP
2. **Diagramas ER** con cardinalidades 1:1, 1:N, N:M y tablas intermedias
3. **Star Schema** desnormalizado para Data Warehouses (OLAP)
4. **SCD Type 2** para mantener historial completo de cambios en dimensiones

**Regla de oro**:
- 🏪 **OLTP (Transaccional)** → Normalizar (3NF) → Integridad y eficiencia en escrituras
- 📊 **OLAP (Analítico)** → Desnormalizar (Star) → Performance en lecturas agregadas

---

**Tiempo estimado:** 90-120 minutos
**Próximos pasos**: Resuelve **03-EJERCICIOS.md** para practicar diseño de modelos de datos
**Recursos**: [dbdiagram.io](https://dbdiagram.io/) para crear diagramas ER visuales

¡Domina el modelado! 📐✨
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
