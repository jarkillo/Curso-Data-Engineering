# Ejemplos Prácticos: PostgreSQL Avanzado

> **Nota**: Asegúrate de tener PostgreSQL corriendo: `docker-compose up -d postgres`

## Ejemplo 1: Trabajar con JSON/JSONB - Nivel: Básico

### Contexto
DataFlow Analytics necesita almacenar eventos de usuario con estructuras variables. Cada evento puede tener propiedades diferentes según el tipo.

### Objetivo
Crear tabla con JSONB y realizar consultas sobre campos JSON.

### Paso 1: Crear tabla
```sql
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    datos JSONB
);
```

### Paso 2: Insertar eventos
```sql
-- Evento de página vista
INSERT INTO eventos (tipo, datos) VALUES (
    'page_view',
    '{"url": "/productos", "referrer": "google.com", "user_id": 123}'
);

-- Evento de compra (estructura diferente)
INSERT INTO eventos (tipo, datos) VALUES (
    'purchase',
    '{"product_id": 456, "amount": 99.99, "currency": "USD", "payment_method": "credit_card"}'
);

-- Evento de registro
INSERT INTO eventos (tipo, datos) VALUES (
    'signup',
    '{"email": "usuario@example.com", "plan": "premium", "referral_code": "SAVE20"}'
);
```

### Paso 3: Consultar datos JSON
```sql
-- Obtener user_id de eventos (operador ->>'  extrae como texto)
SELECT
    id,
    tipo,
    datos->>'user_id' AS user_id,
    datos->>'url' AS url
FROM eventos
WHERE tipo = 'page_view';

-- Buscar por campo dentro del JSON
SELECT * FROM eventos
WHERE datos->>'plan' = 'premium';

-- Buscar valores numéricos (operador -> mantiene tipo JSON)
SELECT * FROM eventos
WHERE (datos->>'amount')::numeric > 50;
```

### Paso 4: Crear índice GIN para búsquedas rápidas
```sql
CREATE INDEX idx_eventos_datos ON eventos USING GIN (datos);

-- Ahora las búsquedas en JSON son mucho más rápidas
```

### Resultado
```
id | tipo      | user_id | url
1  | page_view | 123     | /productos
```

### Interpretación
JSONB permite flexibilidad total: cada evento puede tener estructura diferente sin cambiar la tabla. El índice GIN hace que las búsquedas sean eficientes incluso con millones de eventos.

---

## Ejemplo 2: Arrays en PostgreSQL - Nivel: Intermedio

### Contexto
TechJobs necesita almacenar habilidades requeridas para cada posición (lista variable de skills).

### Código completo
```sql
-- Crear tabla
CREATE TABLE posiciones (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200),
    empresa VARCHAR(200),
    habilidades TEXT[],
    salario_rango INTEGER[]
);

-- Insertar datos
INSERT INTO posiciones (titulo, empresa, habilidades, salario_rango) VALUES
    ('Data Engineer', 'DataFlow Analytics',
     ARRAY['Python', 'SQL', 'Spark', 'Airflow'],
     ARRAY[70000, 90000]),
    ('Backend Developer', 'CodeCraft Studios',
     ARRAY['Python', 'Django', 'PostgreSQL'],
     ARRAY[60000, 80000]),
    ('ML Engineer', 'AI Innovations',
     ARRAY['Python', 'TensorFlow', 'SQL', 'Docker'],
     ARRAY[80000, 110000]);

-- Buscar posiciones que requieren Python
SELECT titulo, empresa FROM posiciones
WHERE 'Python' = ANY(habilidades);

-- Buscar posiciones que requieren Python Y SQL
SELECT titulo, empresa FROM posiciones
WHERE habilidades @> ARRAY['Python', 'SQL'];

-- Contar habilidades por posición
SELECT
    titulo,
    array_length(habilidades, 1) AS num_habilidades,
    habilidades
FROM posiciones;

-- Obtener salario mínimo y máximo
SELECT
    titulo,
    salario_rango[1] AS salario_min,
    salario_rango[2] AS salario_max
FROM posiciones;
```

### Resultado
```
titulo          | empresa              | num_habilidades
Data Engineer   | DataFlow Analytics   | 4
Backend Developer| CodeCraft Studios   | 3
ML Engineer     | AI Innovations       | 4
```

---

## Ejemplo 3: Funciones Almacenadas - Nivel: Intermedio

### Contexto
E-Shop Online necesita calcular descuentos con lógica de negocio: 10% para clientes regulares, 20% para VIP.

### Código completo
```sql
-- Crear función
CREATE OR REPLACE FUNCTION calcular_precio_con_descuento(
    precio_base NUMERIC,
    tipo_cliente VARCHAR
) RETURNS NUMERIC AS $$
DECLARE
    descuento NUMERIC;
    precio_final NUMERIC;
BEGIN
    -- Determinar descuento según tipo de cliente
    CASE tipo_cliente
        WHEN 'VIP' THEN descuento := 0.20;
        WHEN 'Regular' THEN descuento := 0.10;
        ELSE descuento := 0;
    END CASE;

    -- Calcular precio final
    precio_final := precio_base * (1 - descuento);

    -- Redondear a 2 decimales
    RETURN ROUND(precio_final, 2);
END;
$$ LANGUAGE plpgsql;

-- Usar la función
SELECT
    'Laptop' AS producto,
    1000 AS precio_base,
    'VIP' AS tipo_cliente,
    calcular_precio_con_descuento(1000, 'VIP') AS precio_final;

SELECT
    'Mouse' AS producto,
    50 AS precio_base,
    'Regular' AS tipo_cliente,
    calcular_precio_con_descuento(50, 'Regular') AS precio_final;

SELECT
    'Teclado' AS producto,
    80 AS precio_base,
    'Nuevo' AS tipo_cliente,
    calcular_precio_con_descuento(80, 'Nuevo') AS precio_final;
```

### Resultado
```
producto | precio_base | tipo_cliente | precio_final
Laptop   | 1000        | VIP          | 800.00
Mouse    | 50          | Regular      | 45.00
Teclado  | 80          | Nuevo        | 80.00
```

---

## Ejemplo 4: Triggers para Auditoría - Nivel: Avanzado

### Contexto
SecureBank necesita auditar todos los cambios en la tabla de cuentas bancarias.

### Código completo
```sql
-- Tabla principal
CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY,
    titular VARCHAR(200),
    saldo NUMERIC(12,2),
    tipo VARCHAR(50),
    activa BOOLEAN DEFAULT TRUE
);

-- Tabla de auditoría
CREATE TABLE auditoria_cuentas (
    audit_id SERIAL PRIMARY KEY,
    cuenta_id INTEGER,
    accion VARCHAR(10),
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    usuario VARCHAR(100),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Función trigger
CREATE OR REPLACE FUNCTION auditar_cuentas()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO auditoria_cuentas (cuenta_id, accion, datos_nuevos, usuario)
        VALUES (NEW.id, 'INSERT', row_to_json(NEW)::jsonb, current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria_cuentas (cuenta_id, accion, datos_anteriores, datos_nuevos, usuario)
        VALUES (OLD.id, 'UPDATE', row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb, current_user);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO auditoria_cuentas (cuenta_id, accion, datos_anteriores, usuario)
        VALUES (OLD.id, 'DELETE', row_to_json(OLD)::jsonb, current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
CREATE TRIGGER trigger_auditar_cuentas
AFTER INSERT OR UPDATE OR DELETE ON cuentas
FOR EACH ROW EXECUTE FUNCTION auditar_cuentas();

-- Probar
INSERT INTO cuentas (titular, saldo, tipo) VALUES ('Ana García', 1000.00, 'Ahorro');
UPDATE cuentas SET saldo = 1500.00 WHERE titular = 'Ana García';
DELETE FROM cuentas WHERE titular = 'Ana García';

-- Ver auditoría
SELECT * FROM auditoria_cuentas ORDER BY audit_id;
```

### Resultado
```
audit_id | cuenta_id | accion | datos_anteriores          | datos_nuevos
1        | 1         | INSERT | null                      | {"titular":"Ana García", "saldo":1000}
2        | 1         | UPDATE | {"saldo":1000}            | {"saldo":1500}
3        | 1         | DELETE | {"titular":"Ana García"}  | null
```

---

## Ejemplo 5: Transacciones ACID - Nivel: Avanzado

### Contexto
BankTransfer necesita garantizar que las transferencias sean atómicas: o se completa todo, o nada.

### Código completo
```sql
-- Crear tabla
CREATE TABLE cuentas_bancarias (
    id SERIAL PRIMARY KEY,
    titular VARCHAR(200),
    saldo NUMERIC(12,2) CHECK (saldo >= 0)
);

-- Insertar datos iniciales
INSERT INTO cuentas_bancarias (titular, saldo) VALUES
    ('Carlos López', 1000.00),
    ('María Fernández', 500.00);

-- Función de transferencia con transacción
CREATE OR REPLACE FUNCTION transferir(
    cuenta_origen_id INTEGER,
    cuenta_destino_id INTEGER,
    monto NUMERIC
) RETURNS BOOLEAN AS $$
DECLARE
    saldo_origen NUMERIC;
BEGIN
    -- Obtener saldo de cuenta origen (con lock)
    SELECT saldo INTO saldo_origen
    FROM cuentas_bancarias
    WHERE id = cuenta_origen_id
    FOR UPDATE;

    -- Validar saldo suficiente
    IF saldo_origen < monto THEN
        RAISE EXCEPTION 'Saldo insuficiente. Saldo actual: %, Monto solicitado: %', saldo_origen, monto;
    END IF;

    -- Descontar de origen
    UPDATE cuentas_bancarias
    SET saldo = saldo - monto
    WHERE id = cuenta_origen_id;

    -- Sumar a destino
    UPDATE cuentas_bancarias
    SET saldo = saldo + monto
    WHERE id = cuenta_destino_id;

    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error en transferencia: %', SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Caso exitoso
SELECT transferir(1, 2, 200);  -- Carlos → María: $200
SELECT * FROM cuentas_bancarias;

-- Caso fallido (saldo insuficiente)
SELECT transferir(2, 1, 10000);  -- María no tiene $10,000
SELECT * FROM cuentas_bancarias;  -- Los saldos no cambiaron
```

### Resultado exitoso
```
titular          | saldo
Carlos López     | 800.00   (1000 - 200)
María Fernández  | 700.00   (500 + 200)
```

### Resultado fallido
```
NOTICE: Error en transferencia: Saldo insuficiente...

titular          | saldo
Carlos López     | 800.00   (Sin cambios)
María Fernández  | 700.00   (Sin cambios)
```

### Interpretación
La transacción garantiza ACID: si falla cualquier paso, TODO se deshace. El dinero nunca desaparece ni se duplica.

---

## Resumen

Has visto PostgreSQL avanzado en acción:

1. **JSONB**: Flexibilidad de NoSQL en SQL
2. **Arrays**: Listas sin tablas relacionadas
3. **Funciones**: Lógica de negocio en la BD
4. **Triggers**: Automatización y auditoría
5. **Transacciones**: Garantías ACID para operaciones críticas

**Próximos pasos**: Resuelve los ejercicios en `03-EJERCICIOS.md` para practicar estos conceptos.

**Tiempo estimado:** 45-60 minutos

---

**Última actualización:** 2025-10-25
