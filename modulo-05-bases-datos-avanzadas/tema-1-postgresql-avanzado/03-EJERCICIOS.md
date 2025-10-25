# 03 - Ejercicios: PostgreSQL Avanzado

## 📝 Introducción

Estos ejercicios te ayudarán a dominar las características avanzadas de PostgreSQL. Están organizados por dificultad creciente y cubren todos los conceptos del tema.

### Estructura de los Ejercicios

Cada ejercicio incluye:
- **Enunciado**: Qué debes hacer
- **Datos de ejemplo**: Si es necesario
- **Ayuda**: Pista si te atascas
- **Solución**: Solución completa con explicaciones

### Cómo Usar Estos Ejercicios

1. **Lee el enunciado** completo
2. **Intenta resolverlo** sin mirar la ayuda (15 minutos mínimo)
3. **Si te atascas**, lee la ayuda
4. **Solo mira la solución** después de intentarlo seriamente
5. **Verifica** que tu solución funciona
6. **Compara** tu solución con la oficial

---

## ⭐ Ejercicios Básicos (1-6)

### Ejercicio 1: Almacenar Configuración en JSON ⭐

**Objetivo**: Practicar inserción y consulta básica con JSONB.

**Enunciado**:

Crea una tabla `configuraciones` para almacenar configuración de aplicaciones en formato JSON. Cada configuración tiene:
- `id` (serial, PK)
- `app_nombre` (varchar)
- `config` (jsonb) - contendrá settings como theme, language, notifications

Inserta 3 configuraciones de ejemplo y luego consulta:
1. Todas las apps con theme "dark"
2. Todas las apps con notificaciones activadas

**Datos de ejemplo**:
```json
App: "web-dashboard"
Config: {"theme": "dark", "language": "es", "notifications": true}

App: "mobile-app"
Config: {"theme": "light", "language": "en", "notifications": false}

App: "admin-panel"
Config: {"theme": "dark", "language": "es", "notifications": true}
```

<details>
<summary>💡 Ayuda</summary>

```sql
-- Usar JSONB para almacenar, no JSON
-- Operador ->> para extraer valores como texto
-- WHERE config->>'theme' = 'dark'
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE configuraciones (
    id SERIAL PRIMARY KEY,
    app_nombre VARCHAR(100) NOT NULL,
    config JSONB NOT NULL
);

-- Insertar datos
INSERT INTO configuraciones (app_nombre, config) VALUES
('web-dashboard', '{"theme": "dark", "language": "es", "notifications": true}'),
('mobile-app', '{"theme": "light", "language": "en", "notifications": false}'),
('admin-panel', '{"theme": "dark", "language": "es", "notifications": true}');

-- Consulta 1: Apps con theme dark
SELECT app_nombre, config
FROM configuraciones
WHERE config->>'theme' = 'dark';

-- Resultado esperado:
-- web-dashboard
-- admin-panel

-- Consulta 2: Apps con notificaciones activadas
SELECT app_nombre, config
FROM configuraciones
WHERE (config->>'notifications')::boolean = true;

-- Resultado esperado:
-- web-dashboard
-- admin-panel

-- Explicación:
-- ->> extrae el valor como TEXT
-- ::boolean convierte el texto a booleano para comparación correcta
```

**Lecciones clave**:
- JSONB permite almacenar estructuras complejas
- Operador `->` extrae JSON, `->>` extrae como texto
- `::boolean` convierte string a booleano
</details>

---

### Ejercicio 2: Arrays de Tags ⭐

**Objetivo**: Trabajar con arrays en PostgreSQL.

**Enunciado**:

Crea una tabla `articulos` con:
- `id` (serial, PK)
- `titulo` (varchar)
- `tags` (text[]) - array de tags

Inserta 4 artículos con diferentes tags. Luego:
1. Encuentra todos los artículos que contienen el tag "postgresql"
2. Cuenta cuántos tags tiene cada artículo
3. Lista todos los tags únicos en la base de datos

**Datos de ejemplo**:
```
"Intro a SQL" → ['sql', 'database', 'beginner']
"PostgreSQL Avanzado" → ['postgresql', 'sql', 'advanced']
"NoSQL vs SQL" → ['nosql', 'mongodb', 'postgresql']
"Bases de Datos" → ['database', 'sql', 'nosql']
```

<details>
<summary>💡 Ayuda</summary>

```sql
-- Usar @> para verificar si array contiene elemento
-- array_length(array, 1) para contar elementos
-- unnest() para "desempaquetar" arrays
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE articulos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    tags TEXT[] NOT NULL
);

-- Insertar datos
INSERT INTO articulos (titulo, tags) VALUES
('Intro a SQL', ARRAY['sql', 'database', 'beginner']),
('PostgreSQL Avanzado', ARRAY['postgresql', 'sql', 'advanced']),
('NoSQL vs SQL', ARRAY['nosql', 'mongodb', 'postgresql']),
('Bases de Datos', ARRAY['database', 'sql', 'nosql']);

-- Consulta 1: Artículos con tag "postgresql"
SELECT titulo, tags
FROM articulos
WHERE tags @> ARRAY['postgresql'];

-- Resultado:
-- PostgreSQL Avanzado
-- NoSQL vs SQL

-- Consulta 2: Contar tags por artículo
SELECT
    titulo,
    array_length(tags, 1) AS num_tags
FROM articulos
ORDER BY num_tags DESC;

-- Resultado:
-- Intro a SQL: 3
-- PostgreSQL Avanzado: 3
-- NoSQL vs SQL: 3
-- Bases de Datos: 3

-- Consulta 3: Todos los tags únicos
SELECT DISTINCT unnest(tags) AS tag
FROM articulos
ORDER BY tag;

-- Resultado:
-- advanced
-- beginner
-- database
-- mongodb
-- nosql
-- postgresql
-- sql

-- Explicación:
-- @> verifica si array izquierdo contiene array derecho
-- array_length(arr, 1) retorna longitud de la primera dimensión
-- unnest() convierte array en filas
-- DISTINCT elimina duplicados
```

**Lecciones clave**:
- Arrays almacenan múltiples valores en una columna
- @> es el operador "contiene"
- unnest() es útil para análisis de arrays
</details>

---

### Ejercicio 3: Generar UUIDs Únicos ⭐

**Objetivo**: Usar UUIDs como identificadores.

**Enunciado**:

Crea una tabla `sesiones` con:
- `session_id` (UUID, PK)
- `usuario_id` (integer)
- `creado_en` (timestamp)

Inserta 3 sesiones con UUIDs generados automáticamente. Luego:
1. Consulta todas las sesiones de un usuario específico
2. Verifica que los UUIDs son únicos y válidos

<details>
<summary>💡 Ayuda</summary>

```sql
-- Habilitar extensión: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Generar UUID: uuid_generate_v4()
-- DEFAULT uuid_generate_v4() para auto-generación
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla
CREATE TABLE sesiones (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id INTEGER NOT NULL,
    creado_en TIMESTAMP DEFAULT NOW()
);

-- Insertar datos (UUID se genera automáticamente)
INSERT INTO sesiones (usuario_id) VALUES
(1),
(2),
(1);

-- Consulta 1: Sesiones del usuario 1
SELECT session_id, usuario_id, creado_en
FROM sesiones
WHERE usuario_id = 1;

-- Resultado:
-- Dos registros con UUIDs únicos del usuario 1

-- Consulta 2: Verificar unicidad
SELECT
    COUNT(*) AS total_sesiones,
    COUNT(DISTINCT session_id) AS sesiones_unicas
FROM sesiones;

-- Resultado:
-- total_sesiones: 3
-- sesiones_unicas: 3
-- (Ambos deben ser iguales)

-- Ver formato de UUID
SELECT session_id::text AS uuid_string
FROM sesiones
LIMIT 1;

-- Ejemplo de salida:
-- 550e8400-e29b-41d4-a716-446655440000

-- Explicación:
-- uuid_generate_v4() genera UUIDs aleatorios (versión 4)
-- UUID es tipo de dato nativo en PostgreSQL
-- DEFAULT hace generación automática al insertar
-- ::text convierte UUID a string para visualización
```

**Lecciones clave**:
- UUIDs garantizan unicidad global
- No requieren secuencias centralizadas
- Útiles en sistemas distribuidos
- 128 bits vs 32/64 de INTEGER
</details>

---

### Ejercicio 4: Función Simple - Calcular IVA ⭐

**Objetivo**: Crear tu primera función almacenada.

**Enunciado**:

Crea una función `calcular_iva(monto NUMERIC)` que:
- Reciba un monto base
- Calcule el IVA (21%)
- Retorne el monto total (base + IVA)

Prueba la función con montos: 100, 500, 1250.50

<details>
<summary>💡 Ayuda</summary>

```sql
-- Sintaxis:
CREATE OR REPLACE FUNCTION nombre(param tipo) RETURNS tipo AS $$
BEGIN
    -- lógica
    RETURN valor;
END;
$$ LANGUAGE plpgsql;
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear función
CREATE OR REPLACE FUNCTION calcular_iva(monto NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    iva CONSTANT NUMERIC := 0.21;
    total NUMERIC;
BEGIN
    -- Calcular total = monto + (monto * 21%)
    total := monto + (monto * iva);

    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Pruebas
SELECT calcular_iva(100) AS total;
-- Resultado: 121.00

SELECT calcular_iva(500) AS total;
-- Resultado: 605.00

SELECT calcular_iva(1250.50) AS total;
-- Resultado: 1513.11

-- Usar en queries
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC(10,2)
);

INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1000),
('Mouse', 25),
('Teclado', 75);

-- Calcular precios con IVA
SELECT
    nombre,
    precio AS precio_base,
    calcular_iva(precio) AS precio_con_iva
FROM productos;

-- Resultado:
-- Laptop:  1000.00 → 1210.00
-- Mouse:   25.00 → 30.25
-- Teclado: 75.00 → 90.75

-- Explicación:
-- DECLARE define variables locales
-- CONSTANT previene modificación
-- := es asignación en PL/pgSQL
-- RETURNS define tipo de retorno
-- LANGUAGE plpgsql indica el lenguaje
```

**Lecciones clave**:
- Funciones encapsulan lógica reutilizable
- DECLARE para variables locales
- := para asignación
- Funciones pueden usarse en SELECTs
</details>

---

### Ejercicio 5: Trigger de Auditoría Básico ⭐

**Objetivo**: Crear un trigger simple.

**Enunciado**:

Crea una tabla `usuarios` con `id`, `nombre`, `email`. Crea también una tabla `auditoria_usuarios` con:
- `id` (serial, PK)
- `usuario_id` (integer)
- `accion` (varchar) - 'INSERT', 'UPDATE', 'DELETE'
- `timestamp` (timestamp)

Implementa un trigger que registre en `auditoria_usuarios` cada vez que se inserta un nuevo usuario.

<details>
<summary>💡 Ayuda</summary>

```sql
-- Primero crear la función del trigger
-- Luego crear el trigger que la ejecuta
-- Usar NEW para acceder al registro nuevo
-- TG_OP contiene el tipo de operación
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tablas
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE auditoria_usuarios (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    accion VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Crear función del trigger
CREATE OR REPLACE FUNCTION registrar_auditoria_usuario()
RETURNS TRIGGER AS $$
BEGIN
    -- Insertar registro de auditoría
    INSERT INTO auditoria_usuarios (usuario_id, accion)
    VALUES (NEW.id, TG_OP);

    -- Retornar NEW para permitir la operación
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
CREATE TRIGGER trigger_auditoria_insert
AFTER INSERT ON usuarios
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_usuario();

-- Pruebas
INSERT INTO usuarios (nombre, email) VALUES
('Ana García', 'ana@example.com'),
('Luis Pérez', 'luis@example.com'),
('María López', 'maria@example.com');

-- Ver registros de auditoría
SELECT * FROM auditoria_usuarios;

-- Resultado:
-- id | usuario_id | accion | timestamp
-- 1  | 1          | INSERT | 2025-10-25 10:30:00
-- 2  | 2          | INSERT | 2025-10-25 10:30:01
-- 3  | 3          | INSERT | 2025-10-25 10:30:02

-- Ver usuarios con su auditoría
SELECT
    u.id,
    u.nombre,
    u.email,
    a.accion,
    a.timestamp
FROM usuarios u
LEFT JOIN auditoria_usuarios a ON u.id = a.usuario_id
ORDER BY u.id;

-- Explicación:
-- TRIGGER se ejecuta automáticamente
-- AFTER INSERT indica cuándo ejecutar
-- FOR EACH ROW ejecuta por cada fila afectada
-- NEW contiene los valores del registro nuevo
-- TG_OP contiene el nombre de la operación ('INSERT')
-- RETURN NEW permite que la operación continúe
```

**Lecciones clave**:
- Triggers automatizan acciones
- Útiles para auditoría y logging
- NEW = registro después de la operación
- OLD = registro antes de la operación
</details>

---

### Ejercicio 6: Transacción Simple ⭐

**Objetivo**: Usar transacciones básicas.

**Enunciado**:

Crea una tabla `cuentas` con `id`, `titular`, `saldo`. Inserta 2 cuentas con saldo inicial.

Implementa una transferencia de 100 unidades de la cuenta 1 a la cuenta 2 usando una transacción. La transacción debe:
1. Restar 100 de la cuenta 1
2. Sumar 100 a la cuenta 2
3. Si algo falla, revertir todo (ROLLBACK)

<details>
<summary>💡 Ayuda</summary>

```sql
BEGIN; -- Iniciar transacción
-- ... operaciones ...
COMMIT; -- Confirmar cambios
-- o
ROLLBACK; -- Revertir cambios
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY,
    titular VARCHAR(100) NOT NULL,
    saldo NUMERIC(10,2) NOT NULL CHECK (saldo >= 0)
);

-- Insertar cuentas iniciales
INSERT INTO cuentas (titular, saldo) VALUES
('Ana García', 1000.00),
('Luis Pérez', 500.00);

-- Ver estado inicial
SELECT * FROM cuentas;
-- Ana: 1000.00
-- Luis: 500.00

-- TRANSFERENCIA EXITOSA
BEGIN;

-- Restar de cuenta origen
UPDATE cuentas
SET saldo = saldo - 100
WHERE id = 1;

-- Sumar a cuenta destino
UPDATE cuentas
SET saldo = saldo + 100
WHERE id = 2;

-- Confirmar transacción
COMMIT;

-- Ver resultado
SELECT * FROM cuentas;
-- Ana: 900.00
-- Luis: 600.00

-- TRANSFERENCIA CON ERROR (ROLLBACK)
BEGIN;

-- Intentar restar más de lo disponible
UPDATE cuentas
SET saldo = saldo - 2000
WHERE id = 1;
-- ERROR: violación de CHECK constraint (saldo >= 0)

-- Transacción automáticamente abortada
ROLLBACK;

-- Ver que no cambió nada
SELECT * FROM cuentas;
-- Ana: 900.00 (sin cambios)
-- Luis: 600.00 (sin cambios)

-- VERSIÓN CON VALIDACIÓN
BEGIN;

-- Verificar saldo suficiente
DO $$
DECLARE
    saldo_actual NUMERIC;
    monto_transferir NUMERIC := 100;
BEGIN
    -- Obtener saldo actual
    SELECT saldo INTO saldo_actual
    FROM cuentas
    WHERE id = 1;

    -- Validar saldo suficiente
    IF saldo_actual < monto_transferir THEN
        RAISE EXCEPTION 'Saldo insuficiente';
    END IF;

    -- Realizar transferencia
    UPDATE cuentas SET saldo = saldo - monto_transferir WHERE id = 1;
    UPDATE cuentas SET saldo = saldo + monto_transferir WHERE id = 2;
END $$;

COMMIT;

-- Explicación:
-- BEGIN inicia una transacción
-- Todas las operaciones son tentativas hasta COMMIT
-- ROLLBACK revierte todos los cambios
-- CHECK constraint previene saldos negativos
-- Transacciones garantizan atomicidad (todo o nada)
```

**Lecciones clave**:
- Transacciones garantizan atomicidad
- Todo o nada (ACID)
- ROLLBACK revierte cambios
- Constraints protegen integridad
</details>

---

## ⭐⭐ Ejercicios Intermedios (7-12)

### Ejercicio 7: Consultas Complejas con JSONB ⭐⭐

**Objetivo**: Queries avanzadas con operadores JSONB.

**Enunciado**:

Crea una tabla `eventos` para tracking de analytics:
- `id` (serial, PK)
- `usuario_id` (integer)
- `evento` (varchar) - tipo de evento
- `datos` (jsonb) - datos del evento
- `timestamp` (timestamp)

Inserta eventos de ejemplo (page_view, click, purchase) con diferentes estructuras en `datos`. Luego:
1. Encuentra todos los eventos donde datos.valor > 100
2. Lista todos los eventos que tienen la clave "producto_id"
3. Calcula el valor promedio de todas las compras

**Datos de ejemplo**:
```json
{evento: "page_view", datos: {"url": "/home", "tiempo": 30}}
{evento: "click", datos: {"elemento": "boton_comprar", "posicion": {"x": 100, "y": 200}}}
{evento: "purchase", datos: {"producto_id": "ABC123", "valor": 150.50}}
{evento: "purchase", datos: {"producto_id": "DEF456", "valor": 75.00}}
{evento: "page_view", datos: {"url": "/productos", "tiempo": 45}}
```

<details>
<summary>💡 Ayuda</summary>

```sql
-- ? verifica existencia de clave
-- ->> extrae valor como texto, necesita castear para comparar números
-- jsonb_typeof() indica tipo de valor
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    evento VARCHAR(50) NOT NULL,
    datos JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Insertar datos
INSERT INTO eventos (usuario_id, evento, datos) VALUES
(1, 'page_view', '{"url": "/home", "tiempo": 30}'),
(1, 'click', '{"elemento": "boton_comprar", "posicion": {"x": 100, "y": 200}}'),
(2, 'purchase', '{"producto_id": "ABC123", "valor": 150.50}'),
(3, 'purchase', '{"producto_id": "DEF456", "valor": 75.00}'),
(2, 'page_view', '{"url": "/productos", "tiempo": 45}'),
(1, 'purchase', '{"producto_id": "GHI789", "valor": 200.00}');

-- Consulta 1: Eventos con valor > 100
SELECT
    id,
    usuario_id,
    evento,
    datos
FROM eventos
WHERE evento = 'purchase'
  AND (datos->>'valor')::NUMERIC > 100;

-- Resultado:
-- purchase con producto_id ABC123 (valor 150.50)
-- purchase con producto_id GHI789 (valor 200.00)

-- Consulta 2: Eventos con clave "producto_id"
SELECT
    id,
    evento,
    datos->>'producto_id' AS producto_id,
    datos
FROM eventos
WHERE datos ? 'producto_id';

-- Resultado:
-- Todos los eventos de tipo purchase

-- Consulta 3: Valor promedio de compras
SELECT
    AVG((datos->>'valor')::NUMERIC) AS valor_promedio,
    SUM((datos->>'valor')::NUMERIC) AS valor_total,
    COUNT(*) AS num_compras
FROM eventos
WHERE evento = 'purchase';

-- Resultado:
-- valor_promedio: 141.83
-- valor_total: 425.50
-- num_compras: 3

-- BONUS: Análisis por usuario
SELECT
    usuario_id,
    COUNT(*) FILTER (WHERE evento = 'purchase') AS compras,
    COALESCE(SUM((datos->>'valor')::NUMERIC), 0) AS total_gastado
FROM eventos
GROUP BY usuario_id
ORDER BY total_gastado DESC;

-- Resultado:
-- usuario 2: 1 compra, 150.50
-- usuario 1: 1 compra, 200.00
-- usuario 3: 1 compra, 75.00

-- Explicación:
-- ? operador verifica si JSONB contiene clave
-- ->> extrae como TEXT, requiere ::NUMERIC para operaciones
-- COUNT(*) FILTER es agregación condicional
-- COALESCE maneja valores NULL
```

**Lecciones clave**:
- ? verifica existencia de claves
- Casteo necesario para operaciones numéricas
- JSONB permite esquemas flexibles
- Útil para analytics y eventos
</details>

---

### Ejercicio 8: Arrays con Operadores Avanzados ⭐⭐

**Objetivo**: Manipular arrays con operadores y funciones.

**Enunciado**:

Crea una tabla `proyectos` con:
- `id`, `nombre`, `tecnologias` (text[]), `desarrolladores` (text[])

Inserta 5 proyectos. Luego:
1. Encuentra proyectos que usen "Python" Y "PostgreSQL"
2. Lista proyectos con más de 3 desarrolladores
3. Combina todas las tecnologías únicas usadas en todos los proyectos
4. Encuentra proyectos donde algún desarrollador aparezca en múltiples proyectos

<details>
<summary>💡 Ayuda</summary>

```sql
-- @> contiene todos los elementos
-- && tiene algún elemento en común
-- array_length() cuenta elementos
-- unnest() + GROUP BY para análisis
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tecnologias TEXT[] NOT NULL,
    desarrolladores TEXT[] NOT NULL
);

-- Insertar datos
INSERT INTO proyectos (nombre, tecnologias, desarrolladores) VALUES
('E-commerce API',
 ARRAY['Python', 'PostgreSQL', 'Docker'],
 ARRAY['Ana', 'Luis', 'María']),
('Dashboard Analytics',
 ARRAY['Python', 'MongoDB', 'React'],
 ARRAY['Luis', 'Carlos', 'Elena', 'Pedro']),
('Mobile App Backend',
 ARRAY['Node.js', 'PostgreSQL', 'Redis'],
 ARRAY['Ana', 'Carlos']),
('Data Pipeline',
 ARRAY['Python', 'Airflow', 'PostgreSQL'],
 ARRAY['María', 'Elena']),
('Website CMS',
 ARRAY['PHP', 'MySQL', 'WordPress'],
 ARRAY['Pedro', 'Juan']);

-- Consulta 1: Proyectos con Python Y PostgreSQL
SELECT nombre, tecnologias
FROM proyectos
WHERE tecnologias @> ARRAY['Python', 'PostgreSQL'];

-- Resultado:
-- E-commerce API
-- Data Pipeline

-- Consulta 2: Proyectos con más de 3 desarrolladores
SELECT
    nombre,
    desarrolladores,
    array_length(desarrolladores, 1) AS num_devs
FROM proyectos
WHERE array_length(desarrolladores, 1) > 3;

-- Resultado:
-- Dashboard Analytics (4 devs)

-- Consulta 3: Todas las tecnologías únicas
SELECT DISTINCT unnest(tecnologias) AS tecnologia
FROM proyectos
ORDER BY tecnologia;

-- Resultado:
-- Airflow, Docker, MongoDB, MySQL, Node.js, PHP,
-- PostgreSQL, Python, React, Redis, WordPress

-- Consulta 4: Desarrolladores en múltiples proyectos
SELECT
    dev,
    COUNT(*) AS num_proyectos,
    array_agg(nombre) AS proyectos
FROM (
    SELECT nombre, unnest(desarrolladores) AS dev
    FROM proyectos
) AS devs_expandidos
GROUP BY dev
HAVING COUNT(*) > 1
ORDER BY num_proyectos DESC;

-- Resultado:
-- Ana: 2 proyectos (E-commerce API, Mobile App Backend)
-- Luis: 2 proyectos (E-commerce API, Dashboard Analytics)
-- María: 2 proyectos (E-commerce API, Data Pipeline)
-- Carlos: 2 proyectos (Dashboard Analytics, Mobile App Backend)
-- Elena: 2 proyectos (Dashboard Analytics, Data Pipeline)
-- Pedro: 2 proyectos (Dashboard Analytics, Website CMS)

-- BONUS: Análisis de tecnologías más usadas
SELECT
    tecnologia,
    COUNT(*) AS veces_usada
FROM (
    SELECT unnest(tecnologias) AS tecnologia
    FROM proyectos
) AS techs
GROUP BY tecnologia
ORDER BY veces_usada DESC
LIMIT 3;

-- Resultado:
-- PostgreSQL: 3
-- Python: 3
-- (otras tecnologías)

-- Explicación:
-- @> "contiene" verifica todos los elementos
-- unnest() convierte array en filas
-- array_agg() agrupa valores en array
-- HAVING filtra después de GROUP BY
```

**Lecciones clave**:
- Arrays potentes para relaciones M:N
- unnest() fundamental para análisis
- Operadores @>, &&, = simplifican queries
- array_agg() reconstruye arrays
</details>

---

### Ejercicio 9: Función con Múltiples Retornos ⭐⭐

**Objetivo**: Crear función que retorna múltiples valores.

**Enunciado**:

Crea una función `estadisticas_ventas(fecha_inicio DATE, fecha_fin DATE)` que retorne:
- Total de ventas
- Número de transacciones
- Ticket promedio
- Venta máxima
- Venta mínima

La función debe retornar estos valores como un tipo compuesto.

Primero crea una tabla `ventas` con `id`, `monto`, `fecha`. Inserta datos de ejemplo y prueba la función.

<details>
<summary>💡 Ayuda</summary>

```sql
-- CREATE TYPE para definir tipo compuesto
-- RETURNS tipo_compuesto
-- Retornar con ROW(...) o asignación directa
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tipo compuesto para el retorno
CREATE TYPE stats_ventas AS (
    total_ventas NUMERIC,
    num_transacciones INTEGER,
    ticket_promedio NUMERIC,
    venta_maxima NUMERIC,
    venta_minima NUMERIC
);

-- Crear tabla
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    monto NUMERIC(10,2) NOT NULL,
    fecha DATE NOT NULL
);

-- Insertar datos de ejemplo
INSERT INTO ventas (monto, fecha) VALUES
(100.00, '2025-10-01'),
(250.50, '2025-10-02'),
(75.00, '2025-10-03'),
(500.00, '2025-10-05'),
(150.00, '2025-10-06'),
(300.00, '2025-10-08'),
(425.75, '2025-10-10');

-- Crear función
CREATE OR REPLACE FUNCTION estadisticas_ventas(
    fecha_inicio DATE,
    fecha_fin DATE
) RETURNS stats_ventas AS $$
DECLARE
    resultado stats_ventas;
BEGIN
    SELECT
        SUM(monto),
        COUNT(*),
        AVG(monto),
        MAX(monto),
        MIN(monto)
    INTO resultado
    FROM ventas
    WHERE fecha BETWEEN fecha_inicio AND fecha_fin;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

-- Prueba 1: Todo el mes de octubre
SELECT * FROM estadisticas_ventas('2025-10-01', '2025-10-31');

-- Resultado:
-- total_ventas: 1801.25
-- num_transacciones: 7
-- ticket_promedio: 257.32
-- venta_maxima: 500.00
-- venta_minima: 75.00

-- Prueba 2: Primera semana
SELECT * FROM estadisticas_ventas('2025-10-01', '2025-10-07');

-- Resultado:
-- total_ventas: 1075.50
-- num_transacciones: 5
-- ticket_promedio: 215.10
-- venta_maxima: 500.00
-- venta_minima: 75.00

-- Usar campos individuales
SELECT
    (estadisticas_ventas('2025-10-01', '2025-10-31')).total_ventas AS total,
    (estadisticas_ventas('2025-10-01', '2025-10-31')).num_transacciones AS transacciones;

-- Nota: Esto ejecuta la función 2 veces. Mejor usar WITH:
WITH stats AS (
    SELECT estadisticas_ventas('2025-10-01', '2025-10-31') AS s
)
SELECT
    (s).total_ventas,
    (s).num_transacciones,
    (s).ticket_promedio
FROM stats;

-- BONUS: Función mejorada con manejo de casos sin datos
CREATE OR REPLACE FUNCTION estadisticas_ventas_v2(
    fecha_inicio DATE,
    fecha_fin DATE
) RETURNS stats_ventas AS $$
DECLARE
    resultado stats_ventas;
    hay_datos BOOLEAN;
BEGIN
    -- Verificar si hay datos
    SELECT COUNT(*) > 0 INTO hay_datos
    FROM ventas
    WHERE fecha BETWEEN fecha_inicio AND fecha_fin;

    IF NOT hay_datos THEN
        -- Retornar valores en cero
        resultado.total_ventas := 0;
        resultado.num_transacciones := 0;
        resultado.ticket_promedio := 0;
        resultado.venta_maxima := 0;
        resultado.venta_minima := 0;
    ELSE
        -- Calcular estadísticas
        SELECT
            SUM(monto),
            COUNT(*),
            AVG(monto),
            MAX(monto),
            MIN(monto)
        INTO resultado
        FROM ventas
        WHERE fecha BETWEEN fecha_inicio AND fecha_fin;
    END IF;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

-- Explicación:
-- CREATE TYPE define estructura de retorno
-- INTO asigna resultados de SELECT a variable
-- (funcion()).campo accede a campo específico
-- WITH evita ejecutar función múltiples veces
```

**Lecciones clave**:
- Tipos compuestos permiten retornos complejos
- INTO asigna resultados a variables
- Acceso a campos con (funcion()).campo
- WITH optimiza múltiples accesos
</details>

---

### Ejercicio 10: Trigger con Validación ⭐⭐

**Objetivo**: Trigger que valida y modifica datos.

**Enunciado**:

Crea una tabla `productos` con `id`, `nombre`, `precio`, `descuento`, `precio_final`.

Implementa un trigger que:
1. Antes de INSERT/UPDATE, valide que descuento esté entre 0 y 100
2. Calcule automáticamente `precio_final` = precio * (1 - descuento/100)
3. Si descuento > 50%, registre en tabla `descuentos_especiales`

<details>
<summary>💡 Ayuda</summary>

```sql
-- BEFORE TRIGGER puede modificar NEW antes de insertar
-- RAISE EXCEPTION para rechazar operación
-- IF NEW.campo ... para validar
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tablas
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    descuento NUMERIC(5,2) DEFAULT 0,
    precio_final NUMERIC(10,2)
);

CREATE TABLE descuentos_especiales (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER REFERENCES productos(id),
    descuento NUMERIC(5,2),
    registrado_en TIMESTAMP DEFAULT NOW()
);

-- Crear función del trigger
CREATE OR REPLACE FUNCTION validar_y_calcular_precio()
RETURNS TRIGGER AS $$
BEGIN
    -- Validación 1: Descuento entre 0 y 100
    IF NEW.descuento < 0 OR NEW.descuento > 100 THEN
        RAISE EXCEPTION 'Descuento debe estar entre 0 y 100. Valor recibido: %', NEW.descuento;
    END IF;

    -- Cálculo: precio_final
    NEW.precio_final := NEW.precio * (1 - NEW.descuento / 100);

    -- Registrar descuentos especiales (>50%)
    IF NEW.descuento > 50 THEN
        -- Solo en INSERT, no en UPDATE para evitar duplicados
        IF TG_OP = 'INSERT' THEN
            INSERT INTO descuentos_especiales (producto_id, descuento)
            VALUES (NEW.id, NEW.descuento);
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
CREATE TRIGGER trigger_validar_precio
BEFORE INSERT OR UPDATE ON productos
FOR EACH ROW
EXECUTE FUNCTION validar_y_calcular_precio();

-- Prueba 1: Inserción válida con descuento normal
INSERT INTO productos (nombre, precio, descuento) VALUES
('Laptop', 1000, 10);

SELECT * FROM productos;
-- precio_final calculado: 900.00

-- Prueba 2: Inserción con descuento especial (>50%)
INSERT INTO productos (nombre, precio, descuento) VALUES
('Mouse', 50, 60);

SELECT * FROM productos;
-- precio_final: 20.00

SELECT * FROM descuentos_especiales;
-- Registro del descuento especial

-- Prueba 3: Intento de descuento inválido (debe fallar)
INSERT INTO productos (nombre, precio, descuento) VALUES
('Teclado', 75, 120);
-- ERROR: Descuento debe estar entre 0 y 100

-- Prueba 4: UPDATE modifica precio_final automáticamente
UPDATE productos
SET descuento = 20
WHERE nombre = 'Laptop';

SELECT * FROM productos WHERE nombre = 'Laptop';
-- precio_final actualizado: 800.00 (1000 * 0.8)

-- Prueba 5: Producto sin descuento
INSERT INTO productos (nombre, precio) VALUES
('Monitor', 300);
-- descuento: 0 (default)
-- precio_final: 300.00

-- BONUS: Vista de productos con descuento activo
CREATE VIEW productos_con_descuento AS
SELECT
    id,
    nombre,
    precio,
    descuento,
    precio_final,
    precio - precio_final AS ahorro,
    ROUND((precio - precio_final) / precio * 100, 2) AS porcentaje_ahorro
FROM productos
WHERE descuento > 0
ORDER BY descuento DESC;

SELECT * FROM productos_con_descuento;

-- Explicación:
-- BEFORE TRIGGER ejecuta antes de guardar
-- Puede modificar NEW para cambiar valores
-- RAISE EXCEPTION cancela la operación
-- TG_OP distingue INSERT de UPDATE
-- NEW.id disponible incluso antes de INSERT (será asignado)
```

**Lecciones clave**:
- BEFORE permite modificar datos antes de guardar
- RAISE EXCEPTION valida y rechaza operaciones
- Triggers pueden insertar en otras tablas
- TG_OP diferencia tipo de operación
</details>

---

### Ejercicio 11: Transacción con Savepoints ⭐⭐

**Objetivo**: Usar savepoints para control fino.

**Enunciado**:

Simula un proceso de importación de datos que:
1. Inserta un lote de productos
2. Crea un savepoint
3. Intenta insertar otro lote
4. Si el segundo lote falla, rollback solo al savepoint (mantiene el primer lote)
5. Continúa con un tercer lote

Crea tabla `productos_importados` y demuestra el flujo completo.

<details>
<summary>💡 Ayuda</summary>

```sql
SAVEPOINT nombre; -- Crear punto de guardado
ROLLBACK TO nombre; -- Volver al savepoint
RELEASE SAVEPOINT nombre; -- Liberar savepoint
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE productos_importados (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) CHECK (precio > 0),
    lote INTEGER NOT NULL
);

-- PROCESO DE IMPORTACIÓN CON SAVEPOINTS
BEGIN;

-- LOTE 1: Productos válidos
INSERT INTO productos_importados (codigo, nombre, precio, lote) VALUES
('PROD-001', 'Laptop HP', 899.99, 1),
('PROD-002', 'Mouse Logitech', 29.99, 1),
('PROD-003', 'Teclado Mecánico', 79.99, 1);

SELECT 'Lote 1 insertado' AS status;

-- Crear savepoint después del lote 1
SAVEPOINT lote1_completo;

-- LOTE 2: Contiene un error (código duplicado)
BEGIN; -- Bloque interno para capturar error
    INSERT INTO productos_importados (codigo, nombre, precio, lote) VALUES
    ('PROD-004', 'Monitor Samsung', 299.99, 2),
    ('PROD-001', 'Producto Duplicado', 19.99, 2), -- ¡ERROR! Código duplicado
    ('PROD-005', 'Webcam HD', 59.99, 2);
EXCEPTION
    WHEN unique_violation THEN
        -- Rollback solo al savepoint, mantiene lote 1
        ROLLBACK TO lote1_completo;
        SELECT 'Lote 2 rechazado - código duplicado detectado' AS status;
END;

-- LOTE 3: Productos válidos (después de error en lote 2)
INSERT INTO productos_importados (codigo, nombre, precio, lote) VALUES
('PROD-006', 'Auriculares Bluetooth', 49.99, 3),
('PROD-007', 'Hub USB', 15.99, 3);

SELECT 'Lote 3 insertado' AS status;

-- Confirmar transacción
COMMIT;

-- Ver resultados finales
SELECT
    lote,
    COUNT(*) AS productos_importados,
    SUM(precio) AS valor_total
FROM productos_importados
GROUP BY lote
ORDER BY lote;

-- Resultado:
-- Lote 1: 3 productos (Laptop, Mouse, Teclado)
-- Lote 3: 2 productos (Auriculares, Hub)
-- Lote 2: 0 productos (rollback completo)

SELECT * FROM productos_importados ORDER BY id;

-- VERSIÓN MEJORADA: Con logging
CREATE TABLE log_importacion (
    id SERIAL PRIMARY KEY,
    lote INTEGER,
    estado VARCHAR(20), -- 'EXITO', 'ERROR'
    mensaje TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Proceso mejorado
DO $$
DECLARE
    lotes INTEGER[] := ARRAY[1, 2, 3];
    lote_actual INTEGER;
    productos_insertados INTEGER;
BEGIN
    -- Iniciar transacción implícitamente

    FOR lote_actual IN SELECT unnest(lotes) LOOP
        BEGIN
            -- Crear savepoint por lote
            EXECUTE format('SAVEPOINT lote_%s', lote_actual);

            -- Intentar insertar lote (simulado)
            IF lote_actual = 2 THEN
                -- Simular error en lote 2
                RAISE EXCEPTION 'Error en lote %', lote_actual;
            END IF;

            -- Si llegamos aquí, lote exitoso
            INSERT INTO log_importacion (lote, estado, mensaje)
            VALUES (lote_actual, 'EXITO', format('Lote % importado correctamente', lote_actual));

        EXCEPTION
            WHEN OTHERS THEN
                -- Rollback a savepoint
                EXECUTE format('ROLLBACK TO lote_%s', lote_actual);

                -- Registrar error
                INSERT INTO log_importacion (lote, estado, mensaje)
                VALUES (lote_actual, 'ERROR', SQLERRM);

                RAISE NOTICE 'Lote % falló: %', lote_actual, SQLERRM;
        END;
    END LOOP;

    -- Si todo OK, commit implícito al terminar
END $$;

SELECT * FROM log_importacion ORDER BY id;

-- Explicación:
-- SAVEPOINT crea punto de retorno dentro de transacción
-- ROLLBACK TO regresa al savepoint sin afectar lo anterior
-- RELEASE SAVEPOINT libera el savepoint (opcional)
-- Útil para procesos de importación/ETL
-- Permite continuar después de errores parciales
```

**Lecciones clave**:
- Savepoints permiten rollback parcial
- Transacción principal continúa después de rollback
- Útil para procesos batch/ETL
- Control fino de errores en importaciones
</details>

---

### Ejercicio 12: Índices en JSONB y Arrays ⭐⭐

**Objetivo**: Crear índices para optimizar queries.

**Enunciado**:

Crea una tabla `documentos` con millones de registros simulados (usa `generate_series`). Mide el tiempo de queries antes y después de crear índices en:
1. Columna JSONB
2. Columna de arrays

Compara performance con `EXPLAIN ANALYZE`.

<details>
<summary>💡 Ayuda</summary>

```sql
-- GIN index para JSONB
CREATE INDEX idx_nombre ON tabla USING GIN (columna_jsonb);
-- GIN index para Arrays
CREATE INDEX idx_nombre ON tabla USING GIN (columna_array);
-- EXPLAIN ANALYZE muestra plan de ejecución y tiempo real
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200),
    metadatos JSONB,
    tags TEXT[]
);

-- Insertar datos de prueba (100,000 registros)
INSERT INTO documentos (titulo, metadatos, tags)
SELECT
    'Documento ' || i,
    jsonb_build_object(
        'categoria', CASE (i % 5)
            WHEN 0 THEN 'tecnologia'
            WHEN 1 THEN 'ciencia'
            WHEN 2 THEN 'arte'
            WHEN 3 THEN 'deportes'
            ELSE 'cultura'
        END,
        'vistas', (random() * 1000)::int,
        'autor_id', (random() * 100)::int
    ),
    ARRAY[
        'tag' || (i % 10),
        'tag' || ((i+1) % 10),
        'tag' || ((i+2) % 10)
    ]
FROM generate_series(1, 100000) AS i;

-- Verificar cantidad de datos
SELECT COUNT(*) FROM documentos;
-- 100,000

-- TEST 1: Query JSONB SIN índice
EXPLAIN ANALYZE
SELECT id, titulo, metadatos
FROM documentos
WHERE metadatos->>'categoria' = 'tecnologia';

-- Resultado esperado:
-- Seq Scan (escaneo secuencial)
-- Tiempo: ~200-500ms

-- TEST 2: Query Array SIN índice
EXPLAIN ANALYZE
SELECT id, titulo, tags
FROM documentos
WHERE tags @> ARRAY['tag5'];

-- Resultado esperado:
-- Seq Scan
-- Tiempo: ~200-500ms

-- CREAR ÍNDICES
-- Índice GIN para JSONB
CREATE INDEX idx_documentos_metadatos ON documentos USING GIN (metadatos);

-- Índice GIN para Arrays
CREATE INDEX idx_documentos_tags ON documentos USING GIN (tags);

-- Esperar a que se construyan los índices
-- (puede tardar unos segundos)

-- TEST 3: Query JSONB CON índice
EXPLAIN ANALYZE
SELECT id, titulo, metadatos
FROM documentos
WHERE metadatos->>'categoria' = 'tecnologia';

-- Resultado esperado:
-- Bitmap Index Scan (usa índice)
-- Tiempo: ~10-50ms (10x más rápido)

-- TEST 4: Query Array CON índice
EXPLAIN ANALYZE
SELECT id, titulo, tags
FROM documentos
WHERE tags @> ARRAY['tag5'];

-- Resultado esperado:
-- Bitmap Index Scan
-- Tiempo: ~10-50ms (10x más rápido)

-- ANÁLISIS DE TAMAÑO DE ÍNDICES
SELECT
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes
WHERE tablename = 'documentos';

-- Resultado:
-- idx_documentos_metadatos: ~5-10MB
-- idx_documentos_tags: ~3-5MB

-- BONUS: Índice parcial (solo documentos con muchas vistas)
CREATE INDEX idx_documentos_populares
ON documentos USING GIN (metadatos)
WHERE (metadatos->>'vistas')::int > 500;

-- Query aprovechando índice parcial
EXPLAIN ANALYZE
SELECT id, titulo
FROM documentos
WHERE metadatos->>'categoria' = 'tecnologia'
  AND (metadatos->>'vistas')::int > 500;

-- Más rápido y ocupa menos espacio

-- COMPARATIVA DE PERFORMANCE
CREATE TABLE benchmark_results (
    test VARCHAR(50),
    con_indice BOOLEAN,
    tiempo_ms NUMERIC
);

-- Ejecutar múltiples veces y promediar
DO $$
DECLARE
    inicio TIMESTAMP;
    fin TIMESTAMP;
    i INTEGER;
BEGIN
    -- Sin índice (drop temporalmente)
    DROP INDEX IF EXISTS idx_documentos_metadatos;

    FOR i IN 1..10 LOOP
        inicio := clock_timestamp();
        PERFORM COUNT(*) FROM documentos WHERE metadatos->>'categoria' = 'tecnologia';
        fin := clock_timestamp();

        INSERT INTO benchmark_results VALUES
            ('JSONB query', false, EXTRACT(milliseconds FROM (fin - inicio)));
    END LOOP;

    -- Recrear índice
    CREATE INDEX idx_documentos_metadatos ON documentos USING GIN (metadatos);

    -- Con índice
    FOR i IN 1..10 LOOP
        inicio := clock_timestamp();
        PERFORM COUNT(*) FROM documentos WHERE metadatos->>'categoria' = 'tecnologia';
        fin := clock_timestamp();

        INSERT INTO benchmark_results VALUES
            ('JSONB query', true, EXTRACT(milliseconds FROM (fin - inicio)));
    END LOOP;
END $$;

-- Ver resultados
SELECT
    con_indice,
    ROUND(AVG(tiempo_ms), 2) AS tiempo_promedio_ms,
    ROUND(MIN(tiempo_ms), 2) AS tiempo_minimo_ms,
    ROUND(MAX(tiempo_ms), 2) AS tiempo_maximo_ms
FROM benchmark_results
GROUP BY con_indice;

-- Resultado esperado:
-- sin índice: ~250ms promedio
-- con índice: ~25ms promedio
-- Mejora: 10x más rápido

-- Explicación:
-- GIN (Generalized Inverted Index) ideal para JSONB y Arrays
-- Permite búsquedas rápidas en estructuras complejas
-- Ocupa espacio adicional pero mejora dramaticamente performance
-- Índices parciales útiles para subconjuntos específicos
-- EXPLAIN ANALYZE muestra plan y tiempo real de ejecución
```

**Lecciones clave**:
- GIN índices para JSONB y Arrays
- Performance mejora 10-100x
- EXPLAIN ANALYZE para análisis
- Índices parciales ahorran espacio
- Trade-off: velocidad vs espacio
</details>

---

## ⭐⭐⭐ Ejercicios Avanzados (13-15)

### Ejercicio 13: Función Recursiva con CTE ⭐⭐⭐

**Objetivo**: Combinar PL/pgSQL con CTEs recursivos.

**Enunciado**:

Crea una tabla `empleados` con estructura jerárquica (empleado → supervisor). Implementa una función `obtener_jerarquia(empleado_id INT)` que retorne:
- El empleado y todos sus subordinados (directos e indirectos)
- Nivel de profundidad en la jerarquía
- Ruta completa desde el empleado hasta cada subordinado

Usa CTE recursivo dentro de la función.

<details>
<summary>💡 Ayuda</summary>

```sql
WITH RECURSIVE nombre AS (
    -- Caso base
    SELECT ...
    UNION ALL
    -- Caso recursivo
    SELECT ... FROM nombre JOIN ...
)
-- Retornar en función con RETURN QUERY
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    puesto VARCHAR(100),
    supervisor_id INTEGER REFERENCES empleados(id)
);

-- Insertar jerarquía de ejemplo
INSERT INTO empleados (id, nombre, puesto, supervisor_id) VALUES
(1, 'CEO Ana García', 'CEO', NULL),
(2, 'Director Luis Pérez', 'Director TI', 1),
(3, 'Director María López', 'Director RRHH', 1),
(4, 'Manager Carlos Ruiz', 'Manager Dev', 2),
(5, 'Manager Elena Torres', 'Manager QA', 2),
(6, 'Manager Pedro Sánchez', 'Manager Rec', 3),
(7, 'Dev Juan Martínez', 'Desarrollador', 4),
(8, 'Dev Laura González', 'Desarrolladora', 4),
(9, 'QA Sofia Ramírez', 'QA Engineer', 5),
(10, 'QA Diego Fernández', 'QA Engineer', 5);

-- Crear tipo para el retorno
CREATE TYPE jerarquia_empleado AS (
    empleado_id INTEGER,
    nombre VARCHAR(100),
    puesto VARCHAR(100),
    nivel INTEGER,
    ruta TEXT
);

-- Función que retorna jerarquía
CREATE OR REPLACE FUNCTION obtener_jerarquia(empleado_raiz INT)
RETURNS SETOF jerarquia_empleado AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE jerarquia AS (
        -- Caso base: el empleado raíz
        SELECT
            id,
            nombre,
            puesto,
            0 AS nivel,
            nombre::TEXT AS ruta
        FROM empleados
        WHERE id = empleado_raiz

        UNION ALL

        -- Caso recursivo: subordinados
        SELECT
            e.id,
            e.nombre,
            e.puesto,
            j.nivel + 1,
            j.ruta || ' → ' || e.nombre
        FROM empleados e
        INNER JOIN jerarquia j ON e.supervisor_id = j.id
    )
    SELECT
        id AS empleado_id,
        nombre,
        puesto,
        nivel,
        ruta
    FROM jerarquia
    ORDER BY nivel, nombre;
END;
$$ LANGUAGE plpgsql;

-- Prueba 1: Jerarquía desde CEO
SELECT * FROM obtener_jerarquia(1);

-- Resultado:
-- Nivel 0: CEO Ana García
-- Nivel 1: Director Luis Pérez, Director María López
-- Nivel 2: Manager Carlos Ruiz, Manager Elena Torres, Manager Pedro Sánchez
-- Nivel 3: Desarrolladores y QA Engineers

-- Prueba 2: Jerarquía desde Director TI
SELECT * FROM obtener_jerarquia(2);

-- Resultado:
-- Nivel 0: Director Luis Pérez
-- Nivel 1: Manager Carlos Ruiz, Manager Elena Torres
-- Nivel 2: Desarrolladores y QA Engineers

-- Prueba 3: Empleado sin subordinados
SELECT * FROM obtener_jerarquia(7);

-- Resultado:
-- Nivel 0: Dev Juan Martínez (solo él mismo)

-- BONUS: Función para contar subordinados por nivel
CREATE OR REPLACE FUNCTION contar_subordinados_por_nivel(empleado_id INT)
RETURNS TABLE(nivel INT, cantidad BIGINT) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE jerarquia AS (
        SELECT
            id,
            0 AS nivel
        FROM empleados
        WHERE id = empleado_id

        UNION ALL

        SELECT
            e.id,
            j.nivel + 1
        FROM empleados e
        INNER JOIN jerarquia j ON e.supervisor_id = j.id
    )
    SELECT
        jerarquia.nivel,
        COUNT(*) AS cantidad
    FROM jerarquia
    GROUP BY jerarquia.nivel
    ORDER BY jerarquia.nivel;
END;
$$ LANGUAGE plpgsql;

-- Probar
SELECT * FROM contar_subordinados_por_nivel(1);

-- Resultado:
-- Nivel 0: 1 (CEO)
-- Nivel 1: 2 (Directores)
-- Nivel 2: 3 (Managers)
-- Nivel 3: 4 (Empleados junior)
-- Total: 10 empleados

-- BONUS 2: Vista materializada para performance
CREATE MATERIALIZED VIEW vista_jerarquia_completa AS
SELECT
    e.id,
    e.nombre,
    e.puesto,
    s.nombre AS supervisor_nombre,
    (SELECT COUNT(*) - 1 FROM obtener_jerarquia(e.id)) AS num_subordinados
FROM empleados e
LEFT JOIN empleados s ON e.supervisor_id = s.id;

-- Refresh cuando cambien datos
REFRESH MATERIALIZED VIEW vista_jerarquia_completa;

SELECT * FROM vista_jerarquia_completa ORDER BY id;

-- Explicación:
-- WITH RECURSIVE permite queries jerárquicos
-- Caso base inicia la recursión
-- UNION ALL conecta base con recursivo
-- RETURN QUERY retorna resultado de query directamente
-- SETOF permite retornar múltiples filas
-- Vista materializada cachea resultados caros
```

**Lecciones clave**:
- CTEs recursivos para jerarquías
- RETURN QUERY simplifica funciones
- SETOF retorna múltiples filas
- Vistas materializadas para performance
</details>

---

### Ejercicio 14: Sistema Completo con Triggers ACID ⭐⭐⭐

**Objetivo**: Sistema bancario completo con múltiples triggers y transacciones.

**Enunciado**:

Implementa un sistema bancario con:
1. Tabla `cuentas`: id, titular, saldo, estado
2. Tabla `transacciones`: id, cuenta_origen, cuenta_destino, monto, tipo, timestamp
3. Tabla `auditoria`: registro de todos los cambios

Triggers necesarios:
- Validar saldo suficiente antes de transferencia
- Actualizar saldos automáticamente
- Registrar en auditoría
- Bloquear cuentas con saldo negativo

Función: `transferir(origen, destino, monto)` que ejecute todo en una transacción ACID.

<details>
<summary>💡 Ayuda</summary>

```sql
-- BEFORE trigger para validar
-- AFTER trigger para auditoría
-- PERFORM dentro de función para ejecutar sin retornar
-- LOCK TABLE para evitar race conditions
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tablas
CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY,
    titular VARCHAR(100) NOT NULL,
    saldo NUMERIC(12,2) NOT NULL DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'bloqueada', 'cerrada')),
    creada_en TIMESTAMP DEFAULT NOW(),
    actualizada_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transacciones (
    id SERIAL PRIMARY KEY,
    cuenta_origen INTEGER REFERENCES cuentas(id),
    cuenta_destino INTEGER REFERENCES cuentas(id),
    monto NUMERIC(12,2) NOT NULL CHECK (monto > 0),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('transferencia', 'deposito', 'retiro')),
    estado VARCHAR(20) DEFAULT 'completada' CHECK (estado IN ('completada', 'fallida', 'pendiente')),
    creada_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    tabla VARCHAR(50),
    operacion VARCHAR(10),
    cuenta_id INTEGER,
    datos_antiguos JSONB,
    datos_nuevos JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Trigger 1: Validar saldo antes de transacción
CREATE OR REPLACE FUNCTION validar_saldo_transferencia()
RETURNS TRIGGER AS $$
DECLARE
    saldo_actual NUMERIC;
    estado_cuenta VARCHAR(20);
BEGIN
    -- Solo para transferencias y retiros
    IF NEW.tipo IN ('transferencia', 'retiro') THEN
        -- Obtener saldo y estado de cuenta origen
        SELECT saldo, estado INTO saldo_actual, estado_cuenta
        FROM cuentas
        WHERE id = NEW.cuenta_origen;

        -- Validar cuenta activa
        IF estado_cuenta != 'activa' THEN
            RAISE EXCEPTION 'Cuenta origen % está %', NEW.cuenta_origen, estado_cuenta;
        END IF;

        -- Validar saldo suficiente
        IF saldo_actual < NEW.monto THEN
            NEW.estado := 'fallida';
            RAISE EXCEPTION 'Saldo insuficiente. Disponible: %, Requerido: %',
                saldo_actual, NEW.monto;
        END IF;
    END IF;

    -- Validar cuenta destino (si aplica)
    IF NEW.cuenta_destino IS NOT NULL THEN
        SELECT estado INTO estado_cuenta
        FROM cuentas
        WHERE id = NEW.cuenta_destino;

        IF estado_cuenta != 'activa' THEN
            RAISE EXCEPTION 'Cuenta destino % está %', NEW.cuenta_destino, estado_cuenta;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_saldo
BEFORE INSERT ON transacciones
FOR EACH ROW
EXECUTE FUNCTION validar_saldo_transferencia();

-- Trigger 2: Actualizar saldos después de transacción
CREATE OR REPLACE FUNCTION actualizar_saldos()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado = 'completada' THEN
        -- Actualizar cuenta origen (restar)
        IF NEW.cuenta_origen IS NOT NULL THEN
            UPDATE cuentas
            SET saldo = saldo - NEW.monto,
                actualizada_en = NOW()
            WHERE id = NEW.cuenta_origen;
        END IF;

        -- Actualizar cuenta destino (sumar)
        IF NEW.cuenta_destino IS NOT NULL THEN
            UPDATE cuentas
            SET saldo = saldo + NEW.monto,
                actualizada_en = NOW()
            WHERE id = NEW.cuenta_destino;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_saldos
AFTER INSERT ON transacciones
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldos();

-- Trigger 3: Auditoría de cambios en cuentas
CREATE OR REPLACE FUNCTION auditar_cambios_cuentas()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria (tabla, operacion, cuenta_id, datos_antiguos, datos_nuevos)
        VALUES (
            'cuentas',
            'UPDATE',
            NEW.id,
            row_to_json(OLD)::jsonb,
            row_to_json(NEW)::jsonb
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auditar_cuentas
AFTER UPDATE ON cuentas
FOR EACH ROW
EXECUTE FUNCTION auditar_cambios_cuentas();

-- Trigger 4: Bloquear cuentas con saldo negativo
CREATE OR REPLACE FUNCTION bloquear_cuenta_saldo_negativo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.saldo < 0 AND OLD.estado = 'activa' THEN
        NEW.estado := 'bloqueada';
        RAISE NOTICE 'Cuenta % bloqueada por saldo negativo', NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_bloquear_saldo_negativo
BEFORE UPDATE OF saldo ON cuentas
FOR EACH ROW
EXECUTE FUNCTION bloquear_cuenta_saldo_negativo();

-- Función principal: Transferir con ACID
CREATE OR REPLACE FUNCTION transferir(
    p_cuenta_origen INT,
    p_cuenta_destino INT,
    p_monto NUMERIC
) RETURNS TEXT AS $$
DECLARE
    transaccion_id INTEGER;
BEGIN
    -- Lock de cuentas para evitar race conditions
    PERFORM * FROM cuentas
    WHERE id IN (p_cuenta_origen, p_cuenta_destino)
    FOR UPDATE;

    -- Insertar transacción (triggers se ejecutan automáticamente)
    INSERT INTO transacciones (cuenta_origen, cuenta_destino, monto, tipo)
    VALUES (p_cuenta_origen, p_cuenta_destino, p_monto, 'transferencia')
    RETURNING id INTO transaccion_id;

    RETURN format('Transferencia exitosa. ID: %s', transaccion_id);

EXCEPTION
    WHEN OTHERS THEN
        -- Registrar transacción fallida
        INSERT INTO transacciones (cuenta_origen, cuenta_destino, monto, tipo, estado)
        VALUES (p_cuenta_origen, p_cuenta_destino, p_monto, 'transferencia', 'fallida');

        -- Re-lanzar error
        RAISE;
END;
$$ LANGUAGE plpgsql;

-- Insertar cuentas de prueba
INSERT INTO cuentas (titular, saldo) VALUES
('Ana García', 1000.00),
('Luis Pérez', 500.00),
('María López', 250.00);

-- Prueba 1: Transferencia exitosa
SELECT transferir(1, 2, 100);

SELECT id, titular, saldo, estado FROM cuentas;
-- Ana: 900, Luis: 600

SELECT * FROM transacciones;
-- 1 transacción completada

-- Prueba 2: Transferencia fallida (saldo insuficiente)
SELECT transferir(3, 1, 500);
-- ERROR: Saldo insuficiente

SELECT * FROM transacciones WHERE estado = 'fallida';
-- 1 transacción fallida registrada

-- Prueba 3: Ver auditoría
SELECT
    tabla,
    operacion,
    datos_antiguos->>'saldo' AS saldo_anterior,
    datos_nuevos->>'saldo' AS saldo_nuevo,
    timestamp
FROM auditoria
ORDER BY timestamp DESC;

-- Prueba 4: Transferencia que deja saldo negativo (debe bloquear)
UPDATE cuentas SET saldo = 50 WHERE id = 3;

SELECT transferir(3, 1, 100);
-- ERROR: Saldo insuficiente (trigger previene)

-- Prueba 5: Múltiples transferencias concurrentes (race condition protegido)
BEGIN;
SELECT transferir(1, 2, 50);
SELECT transferir(1, 3, 50);
COMMIT;

-- Ver estado final
SELECT id, titular, saldo, estado FROM cuentas ORDER BY id;

-- Explicación:
-- PERFORM ejecuta query sin retornar resultado
-- FOR UPDATE bloquea filas durante transacción
-- row_to_json convierte registro a JSON
-- EXCEPTION captura todos los errores
-- format() crea strings formateados
-- Triggers se ejecutan automáticamente en orden
```

**Lecciones clave**:
- Múltiples triggers para sistema complejo
- FOR UPDATE previene race conditions
- EXCEPTION maneja errores gracefully
- Triggers BEFORE validan, AFTER actualizan
- ACID garantiza consistencia total
</details>

---

### Ejercicio 15: Optimización Extrema con Particionamiento ⭐⭐⭐

**Objetivo**: Particionar tabla masiva para performance.

**Enunciado**:

Crea sistema de logs con particionamiento por rango (mensual). Implementa:
1. Tabla padre `logs`
2. Particiones mensuales automáticas
3. Función para crear particiones futuras
4. Índices en cada partición
5. Política de retención (eliminar particiones antiguas)

Compara performance entre tabla particionada vs no particionada con 1M+ registros.

<details>
<summary>💡 Ayuda</summary>

```sql
-- Particionamiento nativo (PostgreSQL 10+)
CREATE TABLE nombre (...) PARTITION BY RANGE (columna);
CREATE TABLE partition_name PARTITION OF nombre FOR VALUES FROM ('...') TO ('...');
```
</details>

<details>
<summary>✅ Solución</summary>

```sql
-- Crear tabla particionada
CREATE TABLE logs (
    id BIGSERIAL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    nivel VARCHAR(10) NOT NULL,
    servicio VARCHAR(50) NOT NULL,
    mensaje TEXT,
    datos JSONB
) PARTITION BY RANGE (timestamp);

-- Crear particiones para 3 meses
CREATE TABLE logs_2025_10 PARTITION OF logs
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE TABLE logs_2025_11 PARTITION OF logs
FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

CREATE TABLE logs_2025_12 PARTITION OF logs
FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- Función para crear particiones automáticamente
CREATE OR REPLACE FUNCTION crear_particion_logs(fecha DATE)
RETURNS VOID AS $$
DECLARE
    inicio DATE;
    fin DATE;
    nombre_particion TEXT;
BEGIN
    -- Calcular inicio y fin del mes
    inicio := DATE_TRUNC('month', fecha);
    fin := inicio + INTERVAL '1 month';

    -- Nombre de la partición
    nombre_particion := 'logs_' || TO_CHAR(fecha, 'YYYY_MM');

    -- Crear partición si no existe
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF logs FOR VALUES FROM (%L) TO (%L)',
        nombre_particion,
        inicio,
        fin
    );

    -- Crear índices en la partición
    EXECUTE format(
        'CREATE INDEX IF NOT EXISTS %I ON %I (nivel, servicio)',
        nombre_particion || '_nivel_servicio_idx',
        nombre_particion
    );

    EXECUTE format(
        'CREATE INDEX IF NOT EXISTS %I ON %I USING GIN (datos)',
        nombre_particion || '_datos_idx',
        nombre_particion
    );

    RAISE NOTICE 'Partición % creada exitosamente', nombre_particion;
END;
$$ LANGUAGE plpgsql;

-- Crear particiones para los próximos 6 meses
DO $$
DECLARE
    fecha_actual DATE := CURRENT_DATE;
    i INTEGER;
BEGIN
    FOR i IN 0..5 LOOP
        PERFORM crear_particion_logs(fecha_actual + (i || ' months')::INTERVAL);
    END LOOP;
END $$;

-- Insertar datos de prueba (1 millón de registros)
INSERT INTO logs (timestamp, nivel, servicio, mensaje, datos)
SELECT
    timestamp '2025-10-01' + (random() * (timestamp '2025-12-31' - timestamp '2025-10-01')),
    (ARRAY['INFO', 'WARNING', 'ERROR', 'DEBUG'])[1 + floor(random() * 4)],
    'servicio' || (1 + floor(random() * 10)),
    'Mensaje de prueba ' || i,
    jsonb_build_object(
        'request_id', gen_random_uuid(),
        'duration_ms', (random() * 1000)::int,
        'status_code', (ARRAY[200, 201, 400, 404, 500])[1 + floor(random() * 5)]
    )
FROM generate_series(1, 1000000) AS i;

-- Ver distribución por partición
SELECT
    tableoid::regclass AS particion,
    COUNT(*) AS num_registros,
    pg_size_pretty(pg_relation_size(tableoid)) AS tamaño
FROM logs
GROUP BY tableoid
ORDER BY particion;

-- TEST 1: Query sin filtro de fecha (escanea todas las particiones)
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM logs
WHERE nivel = 'ERROR';

-- TEST 2: Query con filtro de fecha (solo 1 partición)
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM logs
WHERE timestamp >= '2025-10-01'
  AND timestamp < '2025-11-01'
  AND nivel = 'ERROR';

-- Resultado: Partition Pruning reduce escaneo a 1 partición

-- COMPARATIVA: Tabla sin particionar
CREATE TABLE logs_sin_particionar (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    nivel VARCHAR(10) NOT NULL,
    servicio VARCHAR(50) NOT NULL,
    mensaje TEXT,
    datos JSONB
);

-- Copiar mismos datos
INSERT INTO logs_sin_particionar
SELECT * FROM logs;

-- Crear índices comparables
CREATE INDEX idx_logs_sin_part_nivel ON logs_sin_particionar(nivel, servicio);
CREATE INDEX idx_logs_sin_part_datos ON logs_sin_particionar USING GIN(datos);

-- Comparar queries
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM logs_sin_particionar
WHERE timestamp >= '2025-10-01'
  AND timestamp < '2025-11-01'
  AND nivel = 'ERROR';

-- Función de retención (eliminar particiones antiguas)
CREATE OR REPLACE FUNCTION eliminar_particiones_antiguas(meses_retener INT DEFAULT 3)
RETURNS TABLE(particion_eliminada TEXT, registros_eliminados BIGINT) AS $$
DECLARE
    rec RECORD;
    fecha_limite DATE;
BEGIN
    fecha_limite := DATE_TRUNC('month', CURRENT_DATE) - (meses_retener || ' months')::INTERVAL;

    FOR rec IN
        SELECT
            tablename,
            (regexp_matches(tablename, 'logs_(\d{4})_(\d{2})'))[1]::INT AS anio,
            (regexp_matches(tablename, 'logs_(\d{4})_(\d{2})'))[2]::INT AS mes
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'logs_%'
    LOOP
        IF MAKE_DATE(rec.anio, rec.mes, 1) < fecha_limite THEN
            -- Contar registros antes de eliminar
            EXECUTE format('SELECT COUNT(*) FROM %I', rec.tablename) INTO registros_eliminados;

            -- Eliminar partición
            EXECUTE format('DROP TABLE IF EXISTS %I', rec.tablename);

            particion_eliminada := rec.tablename;

            RETURN NEXT;

            RAISE NOTICE 'Partición % eliminada (% registros)', rec.tablename, registros_eliminados;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Probar retención
SELECT * FROM eliminar_particiones_antiguas(1);

-- Trigger para crear particiones automáticamente
CREATE OR REPLACE FUNCTION auto_crear_particion()
RETURNS TRIGGER AS $$
BEGIN
    -- Intentar crear partición para la fecha del nuevo registro
    BEGIN
        PERFORM crear_particion_logs(NEW.timestamp::DATE);
    EXCEPTION
        WHEN duplicate_table THEN
            -- Partición ya existe, continuar
            NULL;
    END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- No se puede crear trigger en tabla particionada directamente
-- Alternativa: Crear en cada partición o usar reglas

-- ANÁLISIS FINAL
SELECT
    'Particionada' AS tipo_tabla,
    COUNT(*) AS total_registros,
    pg_size_pretty(pg_total_relation_size('logs')) AS tamaño_total
FROM logs
UNION ALL
SELECT
    'Sin particionar',
    COUNT(*),
    pg_size_pretty(pg_total_relation_size('logs_sin_particionar'))
FROM logs_sin_particionar;

-- Benchmark de queries
CREATE TABLE benchmark_particionamiento (
    tipo_tabla VARCHAR(20),
    query_tipo VARCHAR(50),
    tiempo_ms NUMERIC,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Ejecutar múltiples queries y comparar
DO $$
DECLARE
    inicio TIMESTAMP;
    fin TIMESTAMP;
    i INT;
BEGIN
    FOR i IN 1..20 LOOP
        -- Particionada con fecha
        inicio := clock_timestamp();
        PERFORM COUNT(*) FROM logs
        WHERE timestamp >= '2025-10-01' AND timestamp < '2025-11-01' AND nivel = 'ERROR';
        fin := clock_timestamp();
        INSERT INTO benchmark_particionamiento (tipo_tabla, query_tipo, tiempo_ms)
        VALUES ('Particionada', 'Con filtro fecha', EXTRACT(milliseconds FROM (fin - inicio)));

        -- Sin particionar con fecha
        inicio := clock_timestamp();
        PERFORM COUNT(*) FROM logs_sin_particionar
        WHERE timestamp >= '2025-10-01' AND timestamp < '2025-11-01' AND nivel = 'ERROR';
        fin := clock_timestamp();
        INSERT INTO benchmark_particionamiento (tipo_tabla, query_tipo, tiempo_ms)
        VALUES ('Sin particionar', 'Con filtro fecha', EXTRACT(milliseconds FROM (fin - inicio)));
    END LOOP;
END $$;

-- Ver resultados
SELECT
    tipo_tabla,
    query_tipo,
    ROUND(AVG(tiempo_ms), 2) AS tiempo_promedio_ms,
    ROUND(MIN(tiempo_ms), 2) AS tiempo_minimo_ms,
    ROUND(MAX(tiempo_ms), 2) AS tiempo_maximo_ms
FROM benchmark_particionamiento
GROUP BY tipo_tabla, query_tipo;

-- Resultado esperado:
-- Particionada: ~50-100ms promedio
-- Sin particionar: ~200-500ms promedio
-- Mejora: 3-5x más rápido con particionamiento

-- Explicación:
-- PARTITION BY RANGE divide tabla por rangos
-- Partition Pruning omite particiones irrelevantes
-- Cada partición es tabla física independiente
-- Índices por partición mejoran performance
-- Útil para datos time-series y grandes volúmenes
-- Facilita mantenimiento (drop partition vs delete)
```

**Lecciones clave**:
- Particionamiento para tablas masivas
- Partition Pruning optimiza automáticamente
- Mantenimiento simplificado (DROP partition)
- 3-10x mejor performance en queries filtradas
- Ideal para logs, métricas, time-series
</details>

---

## 🎓 Conclusión

¡Felicitaciones! Has completado los 15 ejercicios de PostgreSQL Avanzado.

### Resumen de Conceptos Practicados

✅ **JSONB**: Almacenamiento y consultas de documentos
✅ **Arrays**: Operadores (@>, &&) y funciones (unnest, array_agg)
✅ **UUIDs**: Identificadores únicos globales
✅ **Funciones almacenadas**: PL/pgSQL, tipos compuestos, SETOF
✅ **Triggers**: BEFORE/AFTER, validación, auditoría
✅ **Transacciones**: ACID, savepoints, locks
✅ **CTEs Recursivos**: Jerarquías y queries complejos
✅ **Índices**: GIN para JSONB/Arrays, performance
✅ **Particionamiento**: Tablas masivas, partition pruning

### Próximos Pasos

1. **Proyecto Práctico**: Implementa el proyecto completo en `04-proyecto-practico/`
2. **MongoDB**: Continúa con el Tema 2
3. **Profundiza**: Lee la documentación oficial de PostgreSQL
4. **Practica**: Crea tus propios proyectos usando estas técnicas

### Recursos para Seguir Aprendiendo

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PL/pgSQL Tutorial](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)

---

**Siguiente:** [Proyecto Práctico →](./04-proyecto-practico/)

**Última actualización:** 2025-10-25
