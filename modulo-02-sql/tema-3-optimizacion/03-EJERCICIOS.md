# Ejercicios Prácticos: Optimización SQL

Este documento contiene 15 ejercicios progresivos para dominar la optimización de consultas SQL.

**Distribución**:
- Básicos (⭐): Ejercicios 1-6
- Intermedios (⭐⭐): Ejercicios 7-12
- Avanzados (⭐⭐⭐): Ejercicios 13-15

---

## Ejercicios Básicos

### Ejercicio 1: Primer Índice
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **CloudStore**, una tienda en línea. La tabla `productos` tiene 800,000 registros y las búsquedas por categoría tardan 5 segundos.

**Datos**:
```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200),
    categoria VARCHAR(50),
    precio DECIMAL(10,2),
    stock INT,
    activo BOOLEAN
);
```

**Consulta problemática**:
```sql
SELECT id, nombre, precio
FROM productos
WHERE categoria = 'Electrónica';
```

**Tarea**:
1. Crea el índice apropiado para acelerar esta consulta
2. Explica por qué ese índice ayudará

**Pista**: ¿Qué columna aparece en el `WHERE`?

---

### Ejercicio 2: Usar EXPLAIN
**Dificultad**: ⭐ Fácil

**Contexto**:
Continúas en **CloudStore**. Quieres verificar si la consulta de pedidos de un cliente usa el índice correctamente.

**Datos**:
```sql
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT,
    fecha DATE,
    total DECIMAL(10,2),
    estado VARCHAR(20)
);

CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
```

**Consulta**:
```sql
SELECT * FROM pedidos WHERE cliente_id = 500;
```

**Tarea**:
1. Escribe el comando `EXPLAIN` para esta consulta
2. ¿Qué tipo de scan esperas ver? (Seq Scan o Index Scan)
3. ¿Qué te confirmaría que está usando el índice?

**Pista**: EXPLAIN muestra el plan sin ejecutar la consulta.

---

### Ejercicio 3: Identificar Tipo de Scan
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **EduOnline**, una plataforma educativa. Has ejecutado `EXPLAIN ANALYZE` y recibes este output:

```
Seq Scan on cursos  (cost=0.00..18500.00 rows=120 width=250)
  Filter: (instructor_id = 42)
  Rows Removed by Filter: 49880
Execution Time: 245 ms
```

**Tarea**:
1. ¿Qué problema indica este output?
2. ¿Cuántos registros tiene la tabla aproximadamente?
3. ¿Qué índice crearías para solucionar esto?

**Pista**: "Rows Removed by Filter" es una señal importante.

---

### Ejercicio 4: Elegir Columna para Índice
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **HealthTrack**, una app de salud. Tienes estas consultas frecuentes:

```sql
-- Consulta A (50% de consultas)
SELECT * FROM actividades WHERE usuario_id = 123;

-- Consulta B (30% de consultas)
SELECT * FROM actividades WHERE tipo = 'correr';

-- Consulta C (20% de consultas)
SELECT * FROM actividades WHERE fecha = '2024-03-15';
```

**Datos**:
- `actividades` tiene 10,000,000 registros
- `usuario_id`: 100,000 valores únicos (alta cardinalidad)
- `tipo`: 5 valores ('correr', 'nadar', 'ciclismo', 'caminar', 'yoga')
- `fecha`: 365 valores únicos

**Tarea**:
Si solo puedes crear **2 índices**, ¿cuáles crearías y por qué?

**Pista**: Considera cardinalidad y frecuencia de consultas.

---

### Ejercicio 5: Evitar SELECT *
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **NewsHub**, un portal de noticias. Esta consulta tarda 8 segundos:

```sql
SELECT *
FROM articulos
WHERE categoria = 'Tecnología'
  AND fecha_publicacion >= '2024-01-01';
```

La tabla `articulos` tiene 25 columnas, pero el dashboard solo muestra: `titulo`, `autor`, `fecha_publicacion`, `resumen`.

**Tarea**:
1. Reescribe la consulta seleccionando solo las columnas necesarias
2. Estima cuánto podrías reducir el tiempo si cada columna pesa similar

**Pista**: Transferir menos datos = más rápido.

---

### Ejercicio 6: Índice Único
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **AuthPro**, un servicio de autenticación. Necesitas garantizar que los emails sean únicos Y acelerar las búsquedas.

**Datos**:
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password_hash VARCHAR(255),
    activo BOOLEAN
);
```

**Consulta frecuente**:
```sql
SELECT id, password_hash FROM usuarios WHERE email = 'user@example.com';
```

**Tarea**:
1. Crea un índice que garantice emails únicos Y acelere búsquedas
2. ¿Qué error ocurriría si intentas insertar un email duplicado?

**Pista**: Usa `CREATE UNIQUE INDEX`.

---

## Ejercicios Intermedios

### Ejercicio 7: Índice Compuesto con Orden Correcto
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **RideShare**, una app de viajes. Tienes estas consultas:

```sql
-- Consulta 1 (70% de consultas)
SELECT * FROM viajes
WHERE conductor_id = 50 AND estado = 'completado' AND ciudad = 'Madrid';

-- Consulta 2 (20% de consultas)
SELECT * FROM viajes
WHERE conductor_id = 50 AND estado = 'completado';

-- Consulta 3 (10% de consultas)
SELECT * FROM viajes
WHERE ciudad = 'Madrid' AND estado = 'completado';
```

**Datos**:
- `viajes` tiene 20,000,000 registros
- `conductor_id`: 50,000 valores únicos (alta cardinalidad)
- `ciudad`: 20 valores únicos (media cardinalidad)
- `estado`: 3 valores ('pendiente', 'en_curso', 'completado')

**Tarea**:
1. Diseña UN índice compuesto que optimice las Consultas 1 y 2
2. Especifica el orden de las columnas en el índice
3. Explica por qué ese orden es el correcto
4. ¿La Consulta 3 usará tu índice? ¿Por qué sí o no?

**Pista**: Columna con mayor cardinalidad primero. El índice se usa de izquierda a derecha.

---

### Ejercicio 8: Optimizar JOIN Lento
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **StreamFlix**, una plataforma de streaming. Esta consulta tarda 15 segundos:

```sql
SELECT u.nombre, COUNT(v.id) as visualizaciones
FROM usuarios u
LEFT JOIN visualizaciones v ON u.id = v.usuario_id
WHERE v.fecha >= '2024-01-01'
GROUP BY u.id, u.nombre;
```

**Datos**:
- `usuarios`: 5,000,000 registros
- `visualizaciones`: 500,000,000 registros
- Solo existe índice PRIMARY KEY en cada tabla

**EXPLAIN muestra**:
```
Hash Left Join  (cost=...) (actual time=...15234 ms)
  -> Seq Scan on usuarios
  -> Seq Scan on visualizaciones
       Filter: (fecha >= '2024-01-01')
       Rows Removed by Filter: 400000000
```

**Tarea**:
1. Identifica los problemas en el plan de ejecución
2. Crea los índices necesarios para optimizar esta consulta
3. Explica cómo cada índice ayudará

**Pista**: Necesitas índices en la columna de JOIN y en la columna del filtro.

---

### Ejercicio 9: EXISTS vs IN
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **JobMatch**, una bolsa de trabajo. Esta consulta tarda 8 segundos:

```sql
SELECT *
FROM candidatos
WHERE id IN (
    SELECT candidato_id
    FROM postulaciones
    WHERE oferta_id = 500 AND estado = 'aceptado'
);
```

**Datos**:
- `candidatos`: 2,000,000 registros
- `postulaciones`: 50,000,000 registros
- Hay 200 candidatos aceptados para la oferta 500

**Tarea**:
1. Reescribe la consulta usando `EXISTS` en lugar de `IN`
2. Explica por qué `EXISTS` será más rápido en este caso

**Pista**: EXISTS se detiene al encontrar la primera coincidencia.

---

### Ejercicio 10: Evitar Funciones en WHERE
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **SalesTracker**, un CRM. Esta consulta no usa el índice:

```sql
CREATE INDEX idx_ventas_fecha ON ventas(fecha);

SELECT * FROM ventas
WHERE YEAR(fecha) = 2024 AND MONTH(fecha) = 3;
```

**EXPLAIN muestra**:
```
Seq Scan on ventas
  Filter: (YEAR(fecha) = 2024 AND MONTH(fecha) = 3)
```

**Tarea**:
1. Explica por qué no usa el índice en `fecha`
2. Reescribe la consulta sin usar funciones `YEAR()` y `MONTH()`
3. Verifica que ahora use el índice

**Pista**: Usa rangos: `fecha >= X AND fecha < Y`.

---

### Ejercicio 11: Analizar EXPLAIN ANALYZE
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **EventPro**, una plataforma de eventos. Has ejecutado `EXPLAIN ANALYZE`:

```
Limit  (cost=0.56..125.50 rows=100 width=200)
  (actual time=0.05..3450 rows=100 loops=1)
  -> Index Scan using idx_eventos_fecha on eventos
       (cost=0.56..125000 rows=100000 width=200)
       (actual time=0.05..3448 rows=100 loops=1)
       Index Cond: (fecha >= '2024-01-01')
       Filter: (ciudad = 'Barcelona' AND categoria = 'Música')
       Rows Removed by Filter: 99900
Planning Time: 2.1 ms
Execution Time: 3455 ms
```

**Tarea**:
1. ¿El query usa un índice? ¿Cuál?
2. Identifica el problema principal (observa "Rows Removed by Filter")
3. ¿Qué índice adicional crearías para mejorar esto?

**Pista**: Está filtrando 99,900 filas DESPUÉS de leer con el índice.

---

### Ejercicio 12: Decidir Cuándo NO Crear Índice
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **PayFast**, un procesador de pagos. Tu manager quiere crear índices en todas las columnas de `transacciones`:

```sql
CREATE TABLE transacciones (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    monto DECIMAL(10,2),
    estado VARCHAR(20),  -- Valores: 'aprobado', 'rechazado'
    tipo VARCHAR(10),    -- Valores: 'credito', 'debito'
    fecha TIMESTAMP
);
```

La tabla recibe **10,000 inserciones por minuto**.

**Propuesta del manager**:
```sql
CREATE INDEX idx_transacciones_usuario ON transacciones(usuario_id);
CREATE INDEX idx_transacciones_monto ON transacciones(monto);
CREATE INDEX idx_transacciones_estado ON transacciones(estado);
CREATE INDEX idx_transacciones_tipo ON transacciones(tipo);
CREATE INDEX idx_transacciones_fecha ON transacciones(fecha);
```

**Tarea**:
1. Identifica qué índices NO deberías crear y por qué
2. Explica el impacto de tener demasiados índices en una tabla con muchas escrituras
3. Recomienda solo los índices esenciales

**Pista**: Considera cardinalidad y volumen de escrituras.

---

## Ejercicios Avanzados

### Ejercicio 13: Optimizar Pipeline ETL Completo
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **AdTech Solutions**, procesando clicks publicitarios. Tu pipeline ETL tarda 2 horas:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost/adtech_db")

# Extraer clicks del último día
query = """
SELECT *
FROM clicks
WHERE DATE(timestamp) = CURRENT_DATE - INTERVAL '1 day'
"""

df = pd.read_sql(query, engine)  # 50 millones de registros

# Transformar: calcular métricas por campaña
metricas = df.groupby('campania_id').agg({
    'click_id': 'count',
    'costo': 'sum',
    'conversion': 'sum'
}).reset_index()

metricas['ctr'] = metricas['conversion'] / metricas['click_id']

# Cargar a tabla de reportes
metricas.to_sql('metricas_diarias', engine, if_exists='append', index=False)
```

**Datos**:
- `clicks` tiene 10,000,000,000 registros (10 mil millones)
- Se agregan 50,000,000 por día
- Columnas: `click_id`, `campania_id`, `timestamp`, `costo`, `conversion` (boolean)

**Problemas observados**:
- La consulta tarda 45 minutos
- Transferir 50M registros tarda 30 minutos
- Agregación en Pandas tarda 15 minutos

**Tarea**:
1. Reescribe la consulta para que use índice (evita `DATE()`)
2. Cambia la consulta para agregar en SQL, no en Pandas
3. Selecciona solo las columnas necesarias
4. Crea los índices necesarios
5. Estima la mejora de tiempo total

**Pista**: Agrega en SQL, filtra con rango de fechas, selecciona solo lo necesario.

---

### Ejercicio 14: Debugging Producción
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **ChatConnect**, una app de mensajería. A las 3 AM recibes alerta: los chats tardan 20 segundos en cargar. Debes encontrar y solucionar el problema.

**Consulta del chat**:
```sql
SELECT m.id, m.contenido, m.fecha_envio, u.nombre, u.foto
FROM mensajes m
JOIN usuarios u ON m.remitente_id = u.id
WHERE m.conversacion_id = 12345
ORDER BY m.fecha_envio DESC
LIMIT 100;
```

**EXPLAIN ANALYZE muestra**:
```
Limit  (cost=850000..850100 rows=100)
  (actual time=18456..18490 rows=100 loops=1)
  -> Sort  (cost=850000..855000 rows=500000)
       (actual time=18456..18485 rows=100 loops=1)
       Sort Key: m.fecha_envio DESC
       -> Hash Join  (cost=25000..845000 rows=500000)
            (actual time=450..17800 rows=500000 loops=1)
            -> Seq Scan on mensajes m
                 (cost=0..820000 rows=500000)
                 (actual time=0..16500 rows=500000 loops=1)
                 Filter: (conversacion_id = 12345)
                 Rows Removed by Filter: 99500000
```

**Datos**:
- `mensajes`: 100,000,000 registros
- Conversación 12345 tiene 500,000 mensajes (chat grupal muy activo)
- Solo existe PRIMARY KEY en `id`

**Tarea**:
1. Identifica todos los problemas en el plan de ejecución
2. Diseña la estrategia de índices para solucionarlo (puede ser más de un índice)
3. Explica cómo cada índice ayudará
4. Propón una optimización adicional para chats con muchos mensajes

**Pista**: Necesitas índice compuesto que cubra filtro + ordenamiento.

---

### Ejercicio 15: Estrategia de Índices para Tabla Compleja
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **GlobalShip**, una empresa de logística internacional. Debes diseñar la estrategia de índices para la tabla `envios`:

```sql
CREATE TABLE envios (
    id SERIAL PRIMARY KEY,
    codigo_rastreo VARCHAR(50) UNIQUE,
    remitente_id INT,
    destinatario_id INT,
    origen_pais VARCHAR(2),
    destino_pais VARCHAR(2),
    origen_ciudad VARCHAR(100),
    destino_ciudad VARCHAR(100),
    peso_kg DECIMAL(10,2),
    estado VARCHAR(20),
    fecha_creacion TIMESTAMP,
    fecha_entrega_estimada TIMESTAMP,
    fecha_entrega_real TIMESTAMP,
    transportista VARCHAR(50),
    precio DECIMAL(10,2)
);
```

**Consultas frecuentes** (con % de ejecución):

1. **40%**: Rastrear envío por código
   ```sql
   SELECT * FROM envios WHERE codigo_rastreo = 'ABC123XYZ';
   ```

2. **25%**: Envíos pendientes de un remitente
   ```sql
   SELECT * FROM envios
   WHERE remitente_id = 500 AND estado IN ('en_transito', 'pendiente')
   ORDER BY fecha_creacion DESC;
   ```

3. **15%**: Envíos por rango de fechas y país destino
   ```sql
   SELECT * FROM envios
   WHERE fecha_creacion >= '2024-01-01' AND fecha_creacion < '2024-02-01'
     AND destino_pais = 'ES';
   ```

4. **10%**: Dashboard de transportista
   ```sql
   SELECT transportista, estado, COUNT(*), AVG(precio)
   FROM envios
   WHERE fecha_creacion >= CURRENT_DATE - INTERVAL '30 days'
   GROUP BY transportista, estado;
   ```

5. **10%**: Búsqueda por ciudad destino
   ```sql
   SELECT * FROM envios
   WHERE destino_ciudad = 'Madrid' AND estado = 'en_transito';
   ```

**Restricciones**:
- La tabla tiene 50,000,000 registros
- Recibe 100,000 inserciones por día
- No puedes crear más de 7 índices (por rendimiento de escritura)

**Datos estadísticos**:
- `codigo_rastreo`: Único (50M valores)
- `remitente_id`: 500,000 valores únicos
- `destinatario_id`: 2,000,000 valores únicos
- `estado`: 5 valores ('pendiente', 'en_transito', 'entregado', 'devuelto', 'cancelado')
- `destino_pais`: 180 valores únicos
- `destino_ciudad`: 5,000 valores únicos
- `transportista`: 15 valores únicos

**Tarea**:
1. Diseña una estrategia de máximo 7 índices
2. Para cada índice, especifica:
   - Columna(s) del índice
   - Tipo (simple/compuesto/único)
   - Qué consultas beneficia
3. Justifica por qué NO crear índices en ciertas columnas
4. Propón una tabla adicional o vista materializada si ayudaría

**Pista**: Prioriza consultas frecuentes, considera cardinalidad, usa índices compuestos inteligentemente.

---

## Soluciones

### Solución Ejercicio 1

```sql
-- Crear índice en columna de filtro
CREATE INDEX idx_productos_categoria ON productos(categoria);
```

**Explicación**: La consulta filtra por `categoria` en el `WHERE`. Un índice en esta columna permite buscar directamente en los registros de "Electrónica" sin leer toda la tabla.

**Resultado esperado**: Consulta pasa de ~5 segundos a <50 ms (100x más rápido).

---

### Solución Ejercicio 2

```sql
-- Comando EXPLAIN
EXPLAIN SELECT * FROM pedidos WHERE cliente_id = 500;
```

**Tipo de scan esperado**: `Index Scan using idx_pedidos_cliente`

**Confirmación de uso de índice**:
- Aparece "Index Scan" (no "Seq Scan")
- Menciona el nombre del índice: `idx_pedidos_cliente`
- Bajo costo (cost < 100)

---

### Solución Ejercicio 3

**Respuestas**:

1. **Problema**: La consulta hace `Seq Scan` (lee toda la tabla secuencialmente) aunque solo necesita 120 de 50,000 registros. Está descartando 49,880 registros después de leerlos.

2. **Registros aproximados**: 50,000 registros (120 encontrados + 49,880 descartados)

3. **Índice a crear**:
   ```sql
   CREATE INDEX idx_cursos_instructor ON cursos(instructor_id);
   ```

**Justificación**: El filtro es por `instructor_id`, entonces indexar esa columna permitirá acceso directo.

---

### Solución Ejercicio 4

**Índices recomendados**:

```sql
-- Índice 1: usuario_id (prioridad alta)
CREATE INDEX idx_actividades_usuario ON actividades(usuario_id);

-- Índice 2: fecha (prioridad media)
CREATE INDEX idx_actividades_fecha ON actividades(fecha);
```

**Justificación**:
1. **usuario_id**: Alta cardinalidad (100K valores únicos) + consulta más frecuente (50%) = Máximo beneficio
2. **fecha**: Media cardinalidad (365 valores) + 20% de consultas = Buen beneficio
3. **tipo**: Baja cardinalidad (solo 5 valores) = NO crear índice. Un índice en una columna con 5 valores no ayuda mucho (cada valor aparece en ~20% de registros)

---

### Solución Ejercicio 5

```sql
-- Consulta optimizada
SELECT titulo, autor, fecha_publicacion, resumen
FROM articulos
WHERE categoria = 'Tecnología'
  AND fecha_publicacion >= '2024-01-01';
```

**Estimación de mejora**:
- Antes: 25 columnas transferidas
- Después: 4 columnas transferidas
- Reducción: 84% menos datos
- Mejora esperada: 3-5x más rápido (de 8s a 1.6-2.7s)

**Explicación**: Transferir datos desde BD al cliente es costoso. Menos columnas = menos bytes = más rápido.

---

### Solución Ejercicio 6

```sql
-- Índice único en email
CREATE UNIQUE INDEX idx_usuarios_email_unico ON usuarios(email);
```

**Beneficios**:
1. **Garantiza unicidad**: No se pueden insertar emails duplicados
2. **Acelera búsquedas**: Índice permite búsqueda rápida por email

**Error si hay duplicado**:
```
ERROR: duplicate key value violates unique constraint "idx_usuarios_email_unico"
DETAIL: Key (email)=(user@example.com) already exists.
```

---

### Solución Ejercicio 7

**Índice compuesto recomendado**:

```sql
CREATE INDEX idx_viajes_conductor_estado_ciudad
ON viajes(conductor_id, estado, ciudad);
```

**Orden de columnas**:
1. `conductor_id`: Alta cardinalidad (50,000 valores) → Primero
2. `estado`: Baja cardinalidad (3 valores) → Segundo
3. `ciudad`: Media cardinalidad (20 valores) → Tercero

**Explicación del orden**:
- Columna más selectiva primero (conductor_id reduce más el conjunto)
- Consulta 1 usa las 3 columnas → ✅ Usa índice completamente
- Consulta 2 usa primeras 2 columnas → ✅ Usa índice parcialmente
- Consulta 3 empieza con `ciudad` (no es primera columna) → ❌ NO usa índice

**Sobre Consulta 3**: Solo representa 10% de consultas, es aceptable que no use índice. Si se vuelve más frecuente, crear índice adicional `(ciudad, estado)`.

---

### Solución Ejercicio 8

**Problemas identificados**:
1. `Seq Scan on visualizaciones`: Lee 500M registros completos
2. Filtra fecha DESPUÉS de leer → descarta 400M registros
3. JOIN sin índice en `usuario_id`

**Índices necesarios**:

```sql
-- Índice 1: Columna de JOIN en visualizaciones
CREATE INDEX idx_visualizaciones_usuario ON visualizaciones(usuario_id);

-- Índice 2: Columna de filtro (fecha)
CREATE INDEX idx_visualizaciones_fecha ON visualizaciones(fecha);

-- Índice 3 (opcional): Compuesto para máxima eficiencia
CREATE INDEX idx_visualizaciones_fecha_usuario
ON visualizaciones(fecha, usuario_id);
```

**Cómo ayuda cada índice**:
- `idx_visualizaciones_usuario`: Acelera el JOIN (encuentra visualizaciones de cada usuario rápidamente)
- `idx_visualizaciones_fecha`: Filtra por fecha ANTES de leer registros
- Compuesto: Combina ambos beneficios (filtra por fecha + JOIN) en un solo índice

**Mejora esperada**: 15 segundos → 0.5-2 segundos (7-30x más rápido)

---

### Solución Ejercicio 9

**Consulta reescrita con EXISTS**:

```sql
SELECT *
FROM candidatos c
WHERE EXISTS (
    SELECT 1
    FROM postulaciones p
    WHERE p.candidato_id = c.id
      AND p.oferta_id = 500
      AND p.estado = 'aceptado'
);
```

**Por qué EXISTS es más rápido**:

1. **IN**:
   - Ejecuta la subconsulta completa
   - Genera lista de 200 IDs
   - Por cada candidato, busca si su ID está en la lista

2. **EXISTS**:
   - Por cada candidato, busca en postulaciones
   - Se detiene al encontrar la PRIMERA coincidencia
   - No necesita encontrar todas las coincidencias

**Mejora esperada**: 8 segundos → 0.2-1 segundos (8-40x más rápido)

**Índice recomendado**:
```sql
CREATE INDEX idx_postulaciones_candidato_oferta
ON postulaciones(candidato_id, oferta_id, estado);
```

---

### Solución Ejercicio 10

**Respuestas**:

1. **Por qué no usa índice**: Las funciones `YEAR()` y `MONTH()` se aplican a CADA valor de `fecha` antes de comparar. La BD no puede usar el índice porque debe calcular estas funciones para cada fila.

2. **Consulta reescrita sin funciones**:
   ```sql
   SELECT * FROM ventas
   WHERE fecha >= '2024-03-01' AND fecha < '2024-04-01';
   ```

3. **Verificación con EXPLAIN**:
   ```sql
   EXPLAIN SELECT * FROM ventas
   WHERE fecha >= '2024-03-01' AND fecha < '2024-04-01';
   ```

   **Output esperado**:
   ```
   Index Scan using idx_ventas_fecha on ventas
     Index Cond: (fecha >= '2024-03-01' AND fecha < '2024-04-01')
   ```

**Regla de oro**: Nunca uses funciones en columnas indexadas del WHERE. Usa rangos en su lugar.

---

### Solución Ejercicio 11

**Respuestas**:

1. **¿Usa índice?**: Sí, usa `idx_eventos_fecha`

2. **Problema principal**: Aunque usa el índice para filtrar por fecha, aplica los filtros de `ciudad` y `categoria` DESPUÉS de leer 100,000 filas con el índice. Descarta 99,900 filas y solo devuelve 100.

3. **Índice adicional recomendado**:
   ```sql
   CREATE INDEX idx_eventos_fecha_ciudad_categoria
   ON eventos(fecha, ciudad, categoria);
   ```

   **Por qué ayuda**: Este índice compuesto permite filtrar por las 3 columnas usando solo el índice, sin leer 99,900 filas innecesarias.

**Mejora esperada**: 3,455 ms → 50-150 ms (23-69x más rápido)

---

### Solución Ejercicio 12

**Índices que NO deberías crear**:

❌ **idx_transacciones_estado**:
- Baja cardinalidad (2 valores: 'aprobado', 'rechazado')
- Cada valor representa ~50% de registros
- El índice no reduce significativamente el conjunto

❌ **idx_transacciones_tipo**:
- Baja cardinalidad (2 valores: 'credito', 'debito')
- Mismo problema que `estado`

❌ **idx_transacciones_monto**:
- Alta cardinalidad pero NO se filtra frecuentemente
- Más común en rangos (>, <) donde índices son menos efectivos
- No justifica el costo

**Índices esenciales**:

✅ **idx_transacciones_usuario**: Alta cardinalidad + consultas frecuentes por usuario
✅ **idx_transacciones_fecha**: Filtros por rango de fechas son comunes en reportes

**Impacto de demasiados índices con 10,000 inserts/min**:
- Cada INSERT debe actualizar TODOS los índices
- 5 índices = 5x más tiempo de escritura
- Con 10,000 inserts/min, los índices innecesarios pueden causar:
  - Bloqueos de tabla
  - Acumulación de escrituras (backlog)
  - Degradación de rendimiento general

**Recomendación final**:
```sql
CREATE INDEX idx_transacciones_usuario ON transacciones(usuario_id);
CREATE INDEX idx_transacciones_fecha ON transacciones(fecha);
-- Solo 2 índices + PRIMARY KEY
```

---

### Solución Ejercicio 13

**Consulta optimizada completa**:

```python
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://user:pass@localhost/adtech_db")

# ✅ Consulta optimizada: agrega en SQL, usa rango, solo columnas necesarias
query = text("""
SELECT
    campania_id,
    COUNT(click_id) as total_clicks,
    SUM(costo) as costo_total,
    SUM(CASE WHEN conversion THEN 1 ELSE 0 END) as conversiones,
    CAST(SUM(CASE WHEN conversion THEN 1 ELSE 0 END) AS FLOAT) / COUNT(click_id) as ctr
FROM clicks
WHERE timestamp >= CURRENT_DATE - INTERVAL '1 day'
  AND timestamp < CURRENT_DATE
GROUP BY campania_id
""")

df_metricas = pd.read_sql(query, engine)

# Cargar (ya viene agregado, ~1,000 filas en lugar de 50M)
df_metricas.to_sql('metricas_diarias', engine, if_exists='append', index=False)
```

**Índices necesarios**:

```sql
-- Índice en timestamp para filtro de rango
CREATE INDEX idx_clicks_timestamp ON clicks(timestamp);

-- Índice compuesto para cubrir filtro + GROUP BY
CREATE INDEX idx_clicks_timestamp_campania
ON clicks(timestamp, campania_id);
```

**Mejora estimada**:

| Etapa | Antes | Después | Mejora |
|-------|-------|---------|--------|
| Consulta SQL | 45 min | 2 min | 22.5x |
| Transferencia | 30 min (50M registros) | 0.1 min (1K registros) | 300x |
| Agregación | 15 min (Pandas) | 0 (en SQL) | ∞ |
| **TOTAL** | **90 min** | **2-3 min** | **30-45x** 🚀 |

**Técnicas aplicadas**:
1. Rango en lugar de `DATE()` → usa índice
2. Agregación en SQL → evita transferir 50M registros
3. Solo columnas necesarias → reduce ancho de banda
4. Índice compuesto → cubre filtro + GROUP BY

---

### Solución Ejercicio 14

**Problemas identificados**:

1. **Seq Scan on mensajes**: Lee 100 millones de mensajes completos
2. **Rows Removed by Filter: 99,500,000**: Descarta 99.5M después de leerlos
3. **Sort de 500,000 filas**: Ordena en memoria antes de aplicar LIMIT
4. **Sin índice en conversacion_id**: No puede ir directamente a los mensajes de esa conversación

**Estrategia de índices**:

```sql
-- Índice compuesto: filtro + ordenamiento
CREATE INDEX idx_mensajes_conversacion_fecha
ON mensajes(conversacion_id, fecha_envio DESC);

-- Índice en remitente_id para el JOIN
CREATE INDEX idx_mensajes_remitente ON mensajes(remitente_id);
```

**Cómo ayuda**:
- `idx_mensajes_conversacion_fecha`: Filtra por conversación Y ordena por fecha usando solo el índice
- Devuelve los primeros 100 directamente sin leer 500,000
- `DESC` en el índice permite escaneo inverso eficiente

**Optimización adicional para chats grandes**:

```sql
-- Tabla de caché para conversaciones muy activas
CREATE TABLE mensajes_recientes (
    conversacion_id INT,
    mensaje_id INT,
    fecha_agregado TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (conversacion_id, mensaje_id)
);

-- Solo mantener últimos 1000 mensajes de cada conversación
-- Actualizar con trigger o job
```

**Consulta desde caché**:
```sql
SELECT m.id, m.contenido, m.fecha_envio, u.nombre, u.foto
FROM mensajes_recientes mr
JOIN mensajes m ON mr.mensaje_id = m.id
JOIN usuarios u ON m.remitente_id = u.id
WHERE mr.conversacion_id = 12345
ORDER BY m.fecha_envio DESC
LIMIT 100;
```

**Mejora esperada**:
- Con índice: 18,500 ms → 50-200 ms (92-370x más rápido)
- Con caché: < 10 ms (1,850x más rápido) 🚀

---

### Solución Ejercicio 15

**Estrategia de 7 índices**:

```sql
-- 1. Índice único en codigo_rastreo (40% de consultas)
CREATE UNIQUE INDEX idx_envios_codigo ON envios(codigo_rastreo);

-- 2. Índice compuesto para remitente + estado + fecha (25% de consultas)
CREATE INDEX idx_envios_remitente_estado_fecha
ON envios(remitente_id, estado, fecha_creacion DESC);

-- 3. Índice compuesto para fecha + país (15% de consultas)
CREATE INDEX idx_envios_fecha_pais
ON envios(fecha_creacion, destino_pais);

-- 4. Índice compuesto para ciudad + estado (10% de consultas)
CREATE INDEX idx_envios_ciudad_destino_estado
ON envios(destino_ciudad, estado);

-- 5. Índice en fecha para dashboard (10% de consultas)
CREATE INDEX idx_envios_fecha_transportista
ON envios(fecha_creacion, transportista, estado);

-- 6. Índice en remitente (para JOINs frecuentes)
CREATE INDEX idx_envios_remitente ON envios(remitente_id);

-- 7. Índice en destinatario (para JOINs)
CREATE INDEX idx_envios_destinatario ON envios(destinatario_id);
```

**Justificación por índice**:

1. **codigo_rastreo** (único): Consulta más frecuente (40%), alta cardinalidad → máxima prioridad
2. **remitente_estado_fecha**: Consulta 2 (25%), orden correcto para uso parcial
3. **fecha_pais**: Consulta 3 (15%), ambas columnas son selectivas
4. **ciudad_estado**: Consulta 5 (10%), ciudad tiene buena cardinalidad
5. **fecha_transportista_estado**: Dashboard (10%), soporta filtro + GROUP BY
6-7. **Foreign keys**: Para JOINs frecuentes con otras tablas

**Por qué NO crear índices en**:
- ❌ `peso_kg`: Alta cardinalidad pero no se filtra frecuentemente
- ❌ `precio`: Similar a peso
- ❌ `origen_*`: Las consultas priorizan destino, no origen
- ❌ `fecha_entrega_real`: Solo se llena DESPUÉS de entrega (muchos NULL)

**Tabla adicional recomendada**:

```sql
-- Vista materializada para dashboard (refresco cada hora)
CREATE MATERIALIZED VIEW dashboard_transportistas AS
SELECT
    transportista,
    estado,
    DATE(fecha_creacion) as fecha,
    COUNT(*) as total_envios,
    AVG(precio) as precio_promedio,
    SUM(peso_kg) as peso_total
FROM envios
WHERE fecha_creacion >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY transportista, estado, DATE(fecha_creacion);

CREATE INDEX idx_dashboard_fecha ON dashboard_transportistas(fecha);

-- Refrescar cada hora
REFRESH MATERIALIZED VIEW dashboard_transportistas;
```

**Beneficio**: Dashboard consulta vista pre-calculada (< 5 ms) en lugar de agregar 100K registros diarios (varios segundos).

---

## Resumen de Conceptos Practicados

### Ejercicios Básicos (1-6)
✅ Crear índices simples
✅ Usar EXPLAIN
✅ Interpretar planes de ejecución
✅ Elegir columnas para indexar
✅ Evitar SELECT *
✅ Índices únicos

### Ejercicios Intermedios (7-12)
✅ Índices compuestos con orden correcto
✅ Optimizar JOINs
✅ EXISTS vs IN
✅ Evitar funciones en WHERE
✅ Analizar EXPLAIN ANALYZE completo
✅ Decidir cuándo NO crear índices

### Ejercicios Avanzados (13-15)
✅ Optimizar pipelines ETL completos
✅ Debugging en producción
✅ Diseñar estrategias de índices complejas
✅ Balance entre lecturas y escrituras
✅ Vistas materializadas y caching

**¡Continúa con el proyecto práctico en `04-proyecto-practico/`!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
