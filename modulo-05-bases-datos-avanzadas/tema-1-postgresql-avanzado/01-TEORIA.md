# Teoría: PostgreSQL Avanzado

## Introducción: ¿Por qué importa PostgreSQL Avanzado?

Imagina que estás construyendo una casa. Podrías hacerlo solo con ladrillos, cemento y madera (lo básico), pero si conoces técnicas avanzadas de construcción, puedes:

- Instalar ventanas inteligentes que se ajustan automáticamente (triggers)
- Usar materiales modernos que se adaptan mejor (JSON, Arrays)
- Tener planos predefinidos para tareas comunes (funciones almacenadas)
- Asegurar que toda la construcción sea sólida desde los cimientos (transacciones ACID)

**En Data Engineering**, PostgreSQL avanzado te permite construir sistemas de datos mucho más potentes, eficientes y mantenibles.

### ¿Qué aprenderás en esta teoría?

1. **Tipos de datos avanzados**: Más allá de números y textos
2. **Funciones almacenadas**: Código que vive en la base de datos
3. **Triggers**: Automatización inteligente
4. **Transacciones ACID**: Garantías de consistencia

### Contexto real

En el mundo real de Data Engineering:

- **Startups tecnológicas** usan JSON en PostgreSQL para iterar rápido sin cambiar esquemas
- **Bancos** usan funciones almacenadas y triggers para garantizar integridad financiera
- **E-commerce** usa Arrays para guardar listas de productos relacionados eficientemente
- **SaaS empresariales** usan transacciones ACID para garantizar que los datos nunca se corrompan

---

## Parte 1: Tipos de Datos Avanzados

### Concepto 1: JSON y JSONB

#### ¿Qué es JSON/JSONB?

**JSON** (JavaScript Object Notation) es un formato de texto para almacenar datos estructurados de forma flexible.

**Analogía**: Imagina que tienes una caja (tabla SQL) donde normalmente guardas libros perfectamente organizados en estantes (columnas fijas). JSON es como tener un cajón especial donde puedes meter objetos de cualquier forma: un control remoto, unas llaves, un mapa... no necesitas que todos sean del mismo tipo.

**JSONB** es la versión binaria y optimizada de JSON en PostgreSQL. Es como comprimir esa caja flexible para que ocupe menos espacio y sea más rápida de buscar.

#### ¿Por qué usar JSON/JSONB?

En SQL tradicional, si tu tabla `usuarios` tiene:
```sql
id | nombre | email | edad
```

Y de repente necesitas guardar "preferencias de usuario", tendrías que:
1. Alterar la tabla (añadir columnas)
2. Migrar datos existentes
3. Actualizar todo el código

**Con JSONB**:
```sql
id | nombre | email | datos_extra (JSONB)
```

El campo `datos_extra` puede contener CUALQUIER cosa:
```json
{
  "edad": 30,
  "preferencias": {
    "tema": "oscuro",
    "idioma": "es"
  },
  "tags": ["premium", "early-adopter"]
}
```

Y mañana puedes añadir campos nuevos sin modificar la tabla. ¡Flexibilidad total!

#### Diferencia: JSON vs JSONB

| Aspecto | JSON | JSONB |
|---------|------|-------|
| Almacenamiento | Texto plano | Binario (comprimido) |
| Velocidad de escritura | Más rápida | Ligeramente más lenta |
| Velocidad de lectura/consulta | Más lenta | Mucho más rápida |
| Indexable | No | Sí (con GIN indexes) |
| Orden de keys | Se preserva | No se preserva |
| **Recomendado** | Raramente | **Casi siempre** |

#### Ejemplo visual

```sql
-- Crear tabla con JSONB
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200),
    especificaciones JSONB
);

-- Insertar un smartphone
INSERT INTO productos (nombre, especificaciones) VALUES (
    'Smartphone X',
    '{
        "pantalla": "6.5 pulgadas",
        "ram": "8GB",
        "camaras": ["12MP", "48MP", "8MP"],
        "precio": {
            "monto": 699,
            "moneda": "USD"
        }
    }'
);

-- Consultar datos dentro del JSON
SELECT nombre,
       especificaciones->>'pantalla' AS pantalla,
       especificaciones->'precio'->>'monto' AS precio
FROM productos;
```

#### En Data Engineering

**Caso de uso real**: Sistema de eventos (event sourcing)

Imagina que estás construyendo un sistema de analytics que recibe eventos de múltiples fuentes (web, móvil, IoT). Cada fuente envía eventos con estructuras diferentes:

- Web: `{user_id, page, timestamp, referrer}`
- Móvil: `{user_id, screen, timestamp, device_info: {...}}`
- IoT: `{device_id, sensor_data: [...], timestamp}`

Con JSONB puedes almacenar todos en una sola tabla `eventos` sin perder flexibilidad:

```sql
CREATE TABLE eventos (
    id BIGSERIAL PRIMARY KEY,
    fuente VARCHAR(50),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    datos JSONB
);

-- Crear índice GIN para búsquedas rápidas
CREATE INDEX idx_eventos_datos ON eventos USING GIN (datos);
```

---

### Concepto 2: Arrays

#### ¿Qué son los Arrays?

Un **Array** es una lista ordenada de valores del mismo tipo que puedes almacenar en una sola columna.

**Analogía**: Imagina que tienes una agenda de contactos. En lugar de tener una entrada por cada número de teléfono de una persona (casa, trabajo, móvil), puedes tener un solo contacto con una lista de todos sus teléfonos.

#### ¿Por qué usar Arrays?

**Sin Arrays** (normalización tradicional):
```sql
-- Tabla usuarios
id | nombre

-- Tabla tags (relación muchos-a-muchos)
usuario_id | tag

-- Para 1 usuario con 5 tags = 5 filas en la tabla tags
```

**Con Arrays**:
```sql
-- Tabla usuarios
id | nombre | tags (ARRAY)

-- Para 1 usuario con 5 tags = 1 fila
1 | 'Ana' | {'python', 'data', 'sql', 'pandas', 'spark'}
```

#### Tipos de Arrays

PostgreSQL soporta arrays de casi cualquier tipo:
- `INTEGER[]` - Array de enteros
- `TEXT[]` - Array de textos
- `TIMESTAMP[]` - Array de fechas
- `NUMERIC[]` - Array de decimales

#### Ejemplo práctico

```sql
-- Tabla de productos con categorías
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200),
    categorias TEXT[],  -- Array de categorías
    precios_historicos NUMERIC[]  -- Array de precios
);

-- Insertar con arrays
INSERT INTO productos (nombre, categorias, precios_historicos) VALUES
    ('Laptop Pro', ARRAY['electrónica', 'computación', 'trabajo'], ARRAY[1200, 1150, 999]);

-- Buscar si una categoría está en el array
SELECT * FROM productos
WHERE 'electrónica' = ANY(categorias);

-- Obtener tamaño del array
SELECT nombre, array_length(precios_historicos, 1) AS num_precios
FROM productos;

-- Obtener elemento específico (índice comienza en 1)
SELECT nombre, precios_historicos[1] AS precio_mas_reciente
FROM productos;
```

#### Cuándo NO usar Arrays

⚠️ **No uses Arrays si**:
- Necesitas hacer JOIN con los elementos individuales
- Los elementos tienen más de 2-3 atributos cada uno (usa tabla relacionada o JSONB)
- El array puede crecer ilimitadamente (>100 elementos)

✅ **Usa Arrays cuando**:
- Tienes listas pequeñas (<50 elementos típicamente)
- No necesitas consultar elementos individuales frecuentemente
- El número de elementos es relativamente estable

#### En Data Engineering

**Caso de uso real**: ETL pipeline con tags

```sql
-- Tabla de procesos ETL
CREATE TABLE etl_jobs (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200),
    fuentes TEXT[],  -- ['api', 'csv', 's3']
    destinos TEXT[], -- ['postgres', 'redshift']
    tags TEXT[]      -- ['daily', 'critical', 'analytics']
);

-- Consultar todos los jobs que usan 'api' como fuente
SELECT nombre FROM etl_jobs
WHERE 'api' = ANY(fuentes);

-- Consultar jobs críticos y diarios
SELECT nombre FROM etl_jobs
WHERE tags @> ARRAY['critical', 'daily'];  -- @> es "contiene"
```

---

### Concepto 3: UUID

#### ¿Qué es UUID?

**UUID** (Universally Unique Identifier) es un identificador de 128 bits que es (prácticamente) único en el universo.

**Analogía**: Imagina que cada persona en la Tierra necesita una matrícula de coche única. Con números secuenciales (1, 2, 3...) eventualmente te quedarías sin números o dos países podrían asignar el mismo. UUID es como tener un número tan grande y aleatorio que nunca se repetirá, incluso si se genera en computadoras diferentes sin coordinación.

Ejemplo de UUID: `550e8400-e29b-41d4-a716-446655440000`

#### ¿Por qué usar UUID en lugar de SERIAL?

**SERIAL/BIGSERIAL** (autoincremental):
```sql
id | nombre
1  | Ana
2  | Bob
3  | Carlos
```

**Problemas**:
- Predecible (alguien puede adivinar IDs)
- No funciona bien en sistemas distribuidos
- Expone información (si ves ID 1523, sabes que hay ~1523 usuarios)

**UUID**:
```sql
id                                   | nombre
550e8400-e29b-41d4-a716-446655440000 | Ana
6ba7b810-9dad-11d1-80b4-00c04fd430c8 | Bob
123e4567-e89b-12d3-a456-426614174000 | Carlos
```

**Ventajas**:
- Impredecible (seguridad)
- Genera IDs en cualquier servidor sin colisiones
- Permite merge de bases de datos de diferentes orígenes
- No expone métricas de negocio

#### Ejemplo práctico

```sql
-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla con UUID
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(200),
    email VARCHAR(200) UNIQUE,
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar (el ID se genera automáticamente)
INSERT INTO usuarios (nombre, email) VALUES
    ('Ana García', 'ana@example.com'),
    ('Bob Smith', 'bob@example.com');

-- Consultar
SELECT * FROM usuarios;
```

#### UUID Versions

- **v1**: Basado en timestamp + MAC address (predecible, evitar)
- **v4**: Totalmente aleatorio (**recomendado**)
- **v5**: Basado en namespace + nombre (determinístico)

```sql
-- Generar UUID v4 (aleatorio)
SELECT uuid_generate_v4();
-- Output: 8f3c7d2a-9b5e-4f1c-a2d4-7e6f8a9b1c2d

-- Generar UUID v5 (determinístico)
SELECT uuid_generate_v5(uuid_ns_url(), 'https://example.com/user/123');
-- Siempre genera el mismo UUID para la misma URL
```

#### En Data Engineering

**Caso de uso real**: Sistema distribuido de IoT

```sql
-- Sensores en diferentes geografías generan datos
CREATE TABLE lecturas_sensores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperatura NUMERIC(5,2),
    humedad NUMERIC(5,2),
    ubicacion_datacenter VARCHAR(50)
);

-- Cada datacenter genera UUIDs independientemente
-- Luego se pueden consolidar sin conflictos de ID
```

**Beneficio**: Si tienes sensores en NY, Londres y Tokyo, todos pueden generar lecturas con IDs únicos sin necesidad de un servidor central de IDs.

---

### Concepto 4: HSTORE (Bonus)

#### ¿Qué es HSTORE?

**HSTORE** es un tipo de datos key-value (clave-valor) más simple que JSONB.

**Analogía**: Es como un diccionario Python o un objeto JavaScript plano: solo strings como keys y values, sin anidación.

```sql
-- Habilitar extensión
CREATE EXTENSION IF NOT EXISTS hstore;

-- Crear tabla con hstore
CREATE TABLE configuraciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    opciones HSTORE  -- Key-value store
);

-- Insertar
INSERT INTO configuraciones (nombre, opciones) VALUES
    ('App Principal', 'tema=>oscuro, idioma=>es, notificaciones=>true');

-- Consultar
SELECT nombre, opciones->'tema' AS tema
FROM configuraciones;
```

#### HSTORE vs JSONB

| Aspecto | HSTORE | JSONB |
|---------|--------|-------|
| Complejidad | Solo key-value plano | Anidación ilimitada |
| Tipos de datos | Solo strings | Strings, números, booleanos, arrays, objetos |
| Velocidad | Ligeramente más rápido | Muy rápido también |
| **Uso recomendado** | Settings simples | Datos complejos |

**Conclusión**: En Data Engineering moderno, JSONB ha reemplazado mayormente a HSTORE. Úsalo solo si necesitas máxima velocidad con datos muy simples.

---

## Parte 2: Funciones Almacenadas y PL/pgSQL

### Concepto 5: Funciones Almacenadas

#### ¿Qué son las funciones almacenadas?

Son **código que vive dentro de la base de datos** y se ejecuta cuando lo llamas.

**Analogía**: Imagina que tienes una calculadora que solo hace sumas. Las funciones almacenadas son como programar botones personalizados: presionas "Calcular IVA" y automáticamente multiplica por 1.21 y redondea a 2 decimales. El código está en la calculadora misma, no necesitas una app externa.

#### ¿Por qué usar funciones almacenadas?

1. **Performance**: El código está donde están los datos (sin red)
2. **Reutilización**: Escribes la lógica una vez, múltiples apps la usan
3. **Seguridad**: Los usuarios no ven el SQL interno, solo llaman la función
4. **Consistencia**: La lógica está centralizada, no duplicada en cada app

#### Ejemplo básico

```sql
-- Función simple: calcular descuento
CREATE OR REPLACE FUNCTION calcular_descuento(
    precio NUMERIC,
    porcentaje NUMERIC
) RETURNS NUMERIC AS $$
BEGIN
    RETURN precio - (precio * porcentaje / 100);
END;
$$ LANGUAGE plpgsql;

-- Usar la función
SELECT calcular_descuento(100, 20);  -- Returns 80
SELECT calcular_descuento(549.99, 15);  -- Returns 467.4915
```

#### Anatomía de una función

```sql
CREATE OR REPLACE FUNCTION nombre_funcion(
    param1 TIPO,
    param2 TIPO
) RETURNS TIPO_RETORNO AS $$
DECLARE
    -- Variables locales
    variable1 TIPO;
BEGIN
    -- Lógica
    variable1 := alguna_operacion;

    -- Retornar
    RETURN variable1;
END;
$$ LANGUAGE plpgsql;
```

**Partes**:
- `CREATE OR REPLACE`: Crea o sobreescribe si existe
- `FUNCTION nombre_funcion`: Nombre de la función
- `(param1 TIPO)`: Parámetros de entrada
- `RETURNS TIPO_RETORNO`: Qué tipo devuelve
- `$$...$$`: Delimitadores del código
- `LANGUAGE plpgsql`: Lenguaje usado (PL/pgSQL)

#### Ejemplo realista: Validación de inventario

```sql
CREATE OR REPLACE FUNCTION hay_stock_disponible(
    producto_id INTEGER,
    cantidad_solicitada INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    stock_actual INTEGER;
BEGIN
    -- Obtener stock actual
    SELECT stock INTO stock_actual
    FROM productos
    WHERE id = producto_id;

    -- Si no existe el producto
    IF stock_actual IS NULL THEN
        RAISE EXCEPTION 'Producto % no encontrado', producto_id;
    END IF;

    -- Verificar si hay suficiente
    RETURN stock_actual >= cantidad_solicitada;
END;
$$ LANGUAGE plpgsql;

-- Usar
SELECT hay_stock_disponible(123, 5);  -- true o false
```

### Concepto 6: PL/pgSQL

#### ¿Qué es PL/pgSQL?

**PL/pgSQL** (Procedural Language/PostgreSQL) es un lenguaje de programación completo dentro de PostgreSQL. Tiene:

- Variables
- Condicionales (IF/ELSE)
- Bucles (FOR, WHILE)
- Excepciones
- Cursores

Es como escribir Python o JavaScript, pero optimizado para bases de datos.

#### Condicionales

```sql
CREATE OR REPLACE FUNCTION evaluar_edad(edad INTEGER)
RETURNS TEXT AS $$
BEGIN
    IF edad < 18 THEN
        RETURN 'Menor de edad';
    ELSIF edad < 65 THEN
        RETURN 'Adulto';
    ELSE
        RETURN 'Adulto mayor';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

#### Bucles

```sql
CREATE OR REPLACE FUNCTION generar_secuencia(hasta INTEGER)
RETURNS TABLE(numero INTEGER, cuadrado INTEGER) AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..hasta LOOP
        numero := i;
        cuadrado := i * i;
        RETURN NEXT;  -- Devuelve esta fila
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Usar
SELECT * FROM generar_secuencia(5);
-- Returns:
-- 1 | 1
-- 2 | 4
-- 3 | 9
-- 4 | 16
-- 5 | 25
```

#### Manejo de excepciones

```sql
CREATE OR REPLACE FUNCTION dividir_seguro(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN a / b;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'No se puede dividir entre cero';
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT dividir_seguro(10, 0);  -- Returns NULL, muestra notice
```

#### En Data Engineering

**Caso de uso real**: Función de limpieza de datos

```sql
CREATE OR REPLACE FUNCTION limpiar_email(email_sucio TEXT)
RETURNS TEXT AS $$
DECLARE
    email_limpio TEXT;
BEGIN
    -- Quitar espacios
    email_limpio := TRIM(email_sucio);

    -- Convertir a minúsculas
    email_limpio := LOWER(email_limpio);

    -- Validar formato básico
    IF email_limpio !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Email inválido: %', email_sucio;
    END IF;

    RETURN email_limpio;
END;
$$ LANGUAGE plpgsql;

-- ETL: Limpiar emails al cargar
UPDATE usuarios_staging
SET email = limpiar_email(email);
```

---

## Parte 3: Triggers

### Concepto 7: Triggers

#### ¿Qué es un trigger?

Un **trigger** es código que se ejecuta automáticamente cuando ocurre un evento en una tabla (INSERT, UPDATE, DELETE).

**Analogía**: Es como una alarma de casa. No tienes que estar vigilando constantemente; cuando alguien abre la puerta (evento), la alarma se activa automáticamente (trigger ejecuta código).

#### ¿Por qué usar triggers?

1. **Auditoría automática**: Registrar quién cambió qué y cuándo
2. **Validación**: Forzar reglas de negocio
3. **Sincronización**: Actualizar tablas relacionadas automáticamente
4. **Notificaciones**: Alertar cuando pasa algo importante

#### Tipos de triggers

- **BEFORE**: Se ejecuta ANTES del evento (puede cancelar la acción)
- **AFTER**: Se ejecuta DESPUÉS del evento (la acción ya ocurrió)
- **FOR EACH ROW**: Se ejecuta por cada fila afectada
- **FOR EACH STATEMENT**: Se ejecuta una vez por el statement completo

#### Ejemplo: Auditoría automática

```sql
-- Tabla de auditoría
CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER,
    accion VARCHAR(10),  -- INSERT, UPDATE, DELETE
    datos_antiguos JSONB,
    datos_nuevos JSONB,
    usuario VARCHAR(100),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Función trigger
CREATE OR REPLACE FUNCTION auditar_productos()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_productos (
        producto_id, accion, datos_antiguos, datos_nuevos, usuario
    ) VALUES (
        COALESCE(NEW.id, OLD.id),
        TG_OP,  -- INSERT, UPDATE o DELETE
        row_to_json(OLD),
        row_to_json(NEW),
        current_user
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
CREATE TRIGGER trigger_auditar_productos
    AFTER INSERT OR UPDATE OR DELETE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION auditar_productos();
```

**Ahora**, cada vez que alguien modifica `productos`, se guarda automáticamente en `auditoria_productos`:

```sql
UPDATE productos SET precio = 99.99 WHERE id = 123;
-- Automáticamente crea registro en auditoria_productos con:
-- - producto_id: 123
-- - accion: UPDATE
-- - datos_antiguos: {precio: 89.99, ...}
-- - datos_nuevos: {precio: 99.99, ...}
```

#### Variables especiales en triggers

- `NEW`: Los datos nuevos (INSERT/UPDATE)
- `OLD`: Los datos antiguos (UPDATE/DELETE)
- `TG_OP`: Operación (INSERT/UPDATE/DELETE)
- `TG_TABLE_NAME`: Nombre de la tabla

#### Ejemplo: Validación con BEFORE trigger

```sql
-- Función que valida antes de insertar
CREATE OR REPLACE FUNCTION validar_precio()
RETURNS TRIGGER AS $$
BEGIN
    -- No permitir precios negativos
    IF NEW.precio < 0 THEN
        RAISE EXCEPTION 'El precio no puede ser negativo: %', NEW.precio;
    END IF;

    -- No permitir precio > 1 millón sin aprobación
    IF NEW.precio > 1000000 AND NEW.aprobado_por IS NULL THEN
        RAISE EXCEPTION 'Precios > 1M requieren aprobación';
    END IF;

    -- Si todo OK, permitir la inserción
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validar_precio_antes_insertar
    BEFORE INSERT OR UPDATE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION validar_precio();
```

#### ⚠️ Cuidado con triggers

**No abuses de triggers**:
- Pueden hacer el código difícil de debuggear (¡"acciones fantasma"!)
- Impactan performance si son complejos
- Pueden crear dependencias circulares (trigger A llama trigger B llama trigger A...)

**Úsalos para**:
- Auditoría
- Validaciones críticas de negocio
- Cálculos automáticos simples

---

## Parte 4: Transacciones ACID

### Concepto 8: Transacciones ACID

#### ¿Qué es una transacción?

Una **transacción** es un conjunto de operaciones que se ejecutan como una unidad: **todo o nada**.

**Analogía**: Es como comprar algo online con tu tarjeta:
1. Se descuenta dinero de tu cuenta
2. Se envía el producto

Si hay un error en el paso 2, el banco DEBE devolverte el dinero del paso 1. No puede quedarse a medias: o se completa todo, o se cancela todo.

#### ACID: Las garantías

**ACID** son las 4 propiedades que garantiza una transacción:

**A - Atomicity (Atomicidad)**
- Todo o nada
- Si falla algo, se deshace todo (rollback)

**C - Consistency (Consistencia)**
- Los datos siempre quedan en un estado válido
- Se respetan todas las constraints (PK, FK, CHECK, etc.)

**I - Isolation (Aislamiento)**
- Las transacciones no se interfieren entre sí
- Si dos personas modifican la misma fila a la vez, no se corrompe

**D - Durability (Durabilidad)**
- Una vez confirmada (COMMIT), los cambios persisten
- Incluso si se va la luz inmediatamente después

#### Ejemplo básico

```sql
-- Iniciar transacción
BEGIN;

    -- Operación 1: Descontar de cuenta origen
    UPDATE cuentas SET saldo = saldo - 100
    WHERE id = 1;

    -- Operación 2: Sumar a cuenta destino
    UPDATE cuentas SET saldo = saldo + 100
    WHERE id = 2;

    -- Si ambas OK, confirmar
    COMMIT;

-- Si algo falla:
-- ROLLBACK;  -- Deshace todo
```

**Sin transacción**: Podría ejecutarse el UPDATE 1, fallar el UPDATE 2, y el dinero desaparecería.

**Con transacción**: Si falla UPDATE 2, se deshace automáticamente UPDATE 1.

#### Ejemplo realista: Compra en e-commerce

```sql
CREATE OR REPLACE FUNCTION procesar_compra(
    usuario_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    precio_total NUMERIC;
    stock_actual INTEGER;
BEGIN
    -- La función corre dentro de una transacción automáticamente

    -- 1. Verificar stock
    SELECT stock INTO stock_actual
    FROM productos WHERE id = producto_id FOR UPDATE;  -- Lock

    IF stock_actual < cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente';
    END IF;

    -- 2. Calcular precio
    SELECT precio * cantidad INTO precio_total
    FROM productos WHERE id = producto_id;

    -- 3. Crear orden
    INSERT INTO ordenes (usuario_id, producto_id, cantidad, total)
    VALUES (usuario_id, producto_id, cantidad, precio_total);

    -- 4. Reducir stock
    UPDATE productos
    SET stock = stock - cantidad
    WHERE id = producto_id;

    -- 5. Registrar en historial
    INSERT INTO historial_compras (usuario_id, monto, timestamp)
    VALUES (usuario_id, precio_total, NOW());

    -- Si llegamos aquí, todo OK
    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        -- Si cualquier paso falla, todo se deshace
        RAISE NOTICE 'Error en compra: %', SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Usar
SELECT procesar_compra(123, 456, 2);
-- Si falla CUALQUIER paso, NINGÚN cambio se guarda
```

#### Niveles de aislamiento

PostgreSQL soporta 4 niveles de aislamiento (de menos a más estricto):

1. **READ UNCOMMITTED**: Lee datos no confirmados (no soportado realmente en PG)
2. **READ COMMITTED** (default): Solo lee datos confirmados
3. **REPEATABLE READ**: Misma query siempre devuelve lo mismo en una transacción
4. **SERIALIZABLE**: Como si las transacciones corrieran una por una

```sql
-- Cambiar nivel de aislamiento
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... operaciones ...
COMMIT;
```

**En Data Engineering**: Usa READ COMMITTED (default) para la mayoría de casos. Solo usa SERIALIZABLE si tienes lógica financiera crítica.

#### En Data Engineering

**Caso de uso real**: ETL con múltiples tablas

```sql
BEGIN;
    -- 1. Truncar staging
    TRUNCATE TABLE staging_ventas;

    -- 2. Cargar nuevos datos
    COPY staging_ventas FROM '/data/ventas.csv' CSV HEADER;

    -- 3. Validar datos
    DO $$
    DECLARE
        filas_invalidas INTEGER;
    BEGIN
        SELECT COUNT(*) INTO filas_invalidas
        FROM staging_ventas
        WHERE monto < 0 OR fecha IS NULL;

        IF filas_invalidas > 0 THEN
            RAISE EXCEPTION '% filas inválidas encontradas', filas_invalidas;
        END IF;
    END $$;

    -- 4. Insertar en producción
    INSERT INTO ventas
    SELECT * FROM staging_ventas;

    -- 5. Registrar metadata
    INSERT INTO etl_logs (tabla, filas_procesadas, timestamp)
    SELECT 'ventas', COUNT(*), NOW() FROM staging_ventas;

COMMIT;  -- Solo si TODOS los pasos fueron exitosos
```

**Beneficio**: Si la validación (paso 3) falla, no se trunca staging, no se carga nada a producción, y no se crea log falso.

---

## Comparaciones y Decisiones

### ¿Cuándo usar cada característica?

#### JSON/JSONB
✅ Úsalo cuando:
- La estructura de datos cambia frecuentemente
- Datos semi-estructurados (logs, eventos, configs)
- Prototipado rápido

❌ No lo uses cuando:
- Necesitas joins complejos con los campos internos
- Los datos tienen estructura fija y no cambiarán

#### Arrays
✅ Úsalo cuando:
- Listas pequeñas (<50 elementos) y estables
- No necesitas queries complejas sobre elementos individuales
- Tags, categorías, labels

❌ No lo uses cuando:
- Los elementos tienen múltiples atributos (usa tabla relacionada)
- Necesitas joins o aggregaciones sobre elementos

#### UUID
✅ Úsalo cuando:
- Sistema distribuido (múltiples bases de datos)
- Seguridad (no exponer conteos)
- Merge de datos de diferentes fuentes

❌ No lo uses cuando:
- Performance extrema (UUID es más lento que INTEGER)
- Tablas con muchos joins (INTEGER es más eficiente)

#### Funciones Almacenadas
✅ Úsalo cuando:
- Lógica de negocio compleja y reutilizable
- Performance crítico (evita round-trips)
- Necesitas centralizar validaciones

❌ No lo uses cuando:
- Lógica cambia muy frecuentemente (más difícil de versionar)
- Necesitas debuggear fácilmente (más difícil que Python)

#### Triggers
✅ Úsalo cuando:
- Auditoría automática
- Validaciones que DEBEN cumplirse siempre
- Actualizaciones de campos calculados

❌ No lo uses cuando:
- Lógica compleja de negocio (usa funciones)
- Puede resolverse en código de aplicación
- Performance es crítico

---

## Errores Comunes

### Error 1: No usar transacciones en operaciones múltiples
**Por qué pasa**: Los desarrolladores piensan que cada UPDATE automáticamente es seguro.

**Problema**:
```sql
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
-- ¡Si falla aquí, el dinero desapareció!
UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
```

**Solución**:
```sql
BEGIN;
    UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
    UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;
```

### Error 2: Usar JSON en lugar de JSONB
**Por qué pasa**: JSON es "más conocido" y aparece primero en tutoriales.

**Problema**: JSON es más lento para queries y no se puede indexar.

**Solución**: **Siempre usa JSONB** salvo que necesites preservar el orden de keys (rarísimo).

### Error 3: Arrays demasiado grandes
**Por qué pasa**: "Es más fácil que crear otra tabla".

**Problema**:
```sql
-- Array con 1000 productos relacionados
productos_relacionados INTEGER[1000]
-- Imposible de consultar eficientemente
```

**Solución**: Si tienes >50 elementos o necesitas consultas complejas, usa tabla relacionada.

### Error 4: Triggers que llaman triggers
**Por qué pasa**: No se documenta que una tabla tiene triggers.

**Problema**:
```
UPDATE productos → trigger_A → UPDATE inventario → trigger_B → UPDATE productos → ¡ciclo infinito!
```

**Solución**:
- Documenta todos los triggers
- Evita triggers que modifican otras tablas con triggers
- Usa `IF TG_DEPTH < 1` para evitar recursión

### Error 5: No manejar excepciones en funciones
**Por qué pasa**: Se asume que todo funcionará.

**Problema**:
```sql
CREATE FUNCTION dividir(a NUMERIC, b NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    RETURN a / b;  -- ¡Crash si b = 0!
END;
$$ LANGUAGE plpgsql;
```

**Solución**: Siempre manejar excepciones en funciones críticas.

---

## Checklist de Aprendizaje

Verifica que puedes hacer lo siguiente:

### Tipos de Datos Avanzados
- [ ] Crear tabla con columna JSONB
- [ ] Insertar y consultar datos JSON
- [ ] Crear tabla con columnas Array
- [ ] Buscar dentro de Arrays con ANY
- [ ] Crear tabla con UUID como PK
- [ ] Generar UUIDs con uuid_generate_v4()

### Funciones y PL/pgSQL
- [ ] Crear función básica con parámetros
- [ ] Usar variables locales (DECLARE)
- [ ] Implementar condicionales (IF/ELSIF/ELSE)
- [ ] Implementar bucles (FOR)
- [ ] Manejar excepciones (EXCEPTION WHEN)
- [ ] Retornar múltiples filas (RETURNS TABLE)

### Triggers
- [ ] Crear función trigger
- [ ] Crear trigger BEFORE
- [ ] Crear trigger AFTER
- [ ] Usar NEW y OLD en triggers
- [ ] Implementar auditoría con triggers

### Transacciones
- [ ] Usar BEGIN/COMMIT
- [ ] Usar ROLLBACK cuando hay error
- [ ] Implementar transacciones en funciones
- [ ] Usar FOR UPDATE para locks

---

## Recursos Adicionales

### Documentación Oficial
- [JSON Types](https://www.postgresql.org/docs/15/datatype-json.html)
- [Arrays](https://www.postgresql.org/docs/15/arrays.html)
- [PL/pgSQL](https://www.postgresql.org/docs/15/plpgsql.html)
- [Triggers](https://www.postgresql.org/docs/15/triggers.html)
- [Transactions](https://www.postgresql.org/docs/15/tutorial-transactions.html)

### Tutoriales Recomendados
- [PostgreSQL Tutorial - JSON](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-json/)
- [PL/pgSQL by Example](https://www.postgresql.org/docs/15/plpgsql-examples.html)

### Libros
- "PostgreSQL: Up and Running" - Regina Obe
- "The Art of PostgreSQL" - Dimitri Fontaine

### Comunidades
- [PostgreSQL Reddit](https://reddit.com/r/PostgreSQL)
- [Stack Overflow - PostgreSQL Tag](https://stackoverflow.com/questions/tagged/postgresql)

---

## Próximos Pasos

Ahora que entiendes la teoría:

1. **📖 Lee 02-EJEMPLOS.md** - Ver estos conceptos en acción con código real
2. **✍️ Resuelve 03-EJERCICIOS.md** - Practica con 15 ejercicios
3. **💻 Implementa 04-proyecto-practico/** - Construye un sistema completo con TDD

**Recuerda**: La teoría sin práctica es solo información. ¡Ve a ejecutar código!

---

**Tiempo de lectura:** 35-45 minutos  
**Última actualización:** 2025-10-25

¡Bienvenido al mundo de PostgreSQL Avanzado! 🐘🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [Módulo 4: APIs y Web Scraping: Rate Limiting y Caching](../../modulo-04-apis-scraping/tema-3-rate-limiting-caching/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
