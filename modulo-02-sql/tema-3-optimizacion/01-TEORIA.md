# Tema 3: Optimización de Consultas SQL

## Introducción

Imagina que tienes una biblioteca con 10 millones de libros. Si alguien te pide encontrar un libro específico y no tienes ningún sistema de organización, tendrías que revisar cada libro uno por uno. Podrías tardar años. Pero si tienes un catálogo por autor, género y título, encontrar cualquier libro toma solo minutos.

**Esto es exactamente lo que hace la optimización SQL**: organiza y estructura tus consultas para que la base de datos encuentre los datos en segundos en lugar de horas.

### ¿Por qué es importante la optimización?

En Data Engineering, trabajarás con:
- **Millones de registros** en tablas transaccionales
- **Billones de eventos** en sistemas de analytics
- **Petabytes de datos** en data warehouses
- **Consultas que se ejecutan miles de veces por día**

Una consulta mal optimizada que tarda 10 segundos en lugar de 0.1 segundos puede:
- **Bloquear tu pipeline ETL** y retrasar todo el procesamiento
- **Costar miles de dólares** en recursos de nube (AWS RDS cobra por tiempo de CPU)
- **Frustrar a usuarios** esperando reportes
- **Causar caídas de servicio** por saturación de recursos

**Ejemplo real**: En una empresa de e-commerce, optimizar una consulta de "productos relacionados" de 8 segundos a 0.3 segundos aumentó las ventas en un 12% porque los usuarios no abandonaban la página mientras cargaba.

### Contexto en Data Engineering

Como Data Engineer, optimizarás consultas SQL en:

1. **Pipelines ETL**: Consultas que extraen millones de registros cada hora
2. **Data Warehouses**: Agregaciones sobre billones de eventos para reportes
3. **APIs de Datos**: Endpoints que consultan bases de datos en tiempo real
4. **Dashboards**: Consultas que alimentan visualizaciones ejecutándose cada minuto

La optimización SQL es una de las habilidades más valiosas y rentables en Data Engineering.

---

## Conceptos Fundamentales

### 1. ¿Cómo Ejecuta una Consulta la Base de Datos?

Cuando escribes una consulta SQL, la base de datos NO la ejecuta directamente. Primero pasa por 4 etapas:

#### Etapa 1: Parsing (Análisis Sintáctico)
La BD verifica que tu SQL sea válido:
```sql
SELECT * FORM users;  -- ❌ Error: "FORM" no existe
SELECT * FROM users;  -- ✅ Sintaxis válida
```

#### Etapa 2: Query Planning (Planificación)
La BD genera **múltiples planes** de cómo ejecutar tu consulta:
- Plan A: Leer toda la tabla secuencialmente (Seq Scan)
- Plan B: Usar índice en columna X (Index Scan)
- Plan C: Usar índice en columna Y y filtrar después

**Analogía**: Como Google Maps mostrándote 3 rutas diferentes para llegar a tu destino.

#### Etapa 3: Query Optimization (Optimización)
El **Query Optimizer** elige el plan más eficiente basándose en:
- **Estadísticas de la tabla** (cuántos registros tiene)
- **Índices disponibles** (qué "atajos" existen)
- **Distribución de datos** (qué tan únicos son los valores)
- **Costo estimado** (cuánto tardará cada plan)

**Analogía**: Google Maps eligiendo la ruta más rápida considerando tráfico, distancia y tipo de vías.

#### Etapa 4: Execution (Ejecución)
La BD ejecuta el plan elegido y devuelve los resultados.

**Punto clave**: Tu trabajo como Data Engineer es entender qué plan elige la BD y si es el óptimo.

---

### 2. Índices: Los "Atajos" de la Base de Datos

#### ¿Qué es un índice?

Un **índice** es una estructura de datos adicional que permite buscar registros sin leer toda la tabla.

**Analogía perfecta**: Un índice SQL es como el índice al final de un libro de texto:
- Sin índice: lees las 500 páginas para encontrar "Machine Learning"
- Con índice: vas directamente al índice, ves "Machine Learning - página 234", y saltas ahí

#### ¿Cómo funciona internamente?

Los índices más comunes usan **árboles B-Tree** (Balanced Tree):

```
Índice en columna 'edad':

            [50]
           /    \
        [25]    [75]
       /  \     /  \
    [10][35] [60][90]
```

Buscar `edad = 35`:
- Sin índice: Lee 1,000,000 registros → **1,000,000 operaciones**
- Con índice: Lee 1 nodo raíz + 1 nodo intermedio + 1 nodo hoja → **3 operaciones**

**¡333,333 veces más rápido!**

#### Tipos de índices

**1. Índice Simple (Single-Column Index)**
```sql
CREATE INDEX idx_usuarios_email ON usuarios(email);
```
Acelera consultas que filtran por UNA columna:
```sql
SELECT * FROM usuarios WHERE email = 'juan@example.com';  -- ✅ Usa índice
```

**2. Índice Compuesto (Multi-Column Index)**
```sql
CREATE INDEX idx_ventas_fecha_tienda ON ventas(fecha, tienda_id);
```
Acelera consultas que filtran por MÚLTIPLES columnas en ese orden:
```sql
-- ✅ Usa índice (fecha es la primera columna del índice)
SELECT * FROM ventas WHERE fecha = '2024-01-15' AND tienda_id = 5;

-- ✅ Usa índice parcialmente (solo la parte de fecha)
SELECT * FROM ventas WHERE fecha = '2024-01-15';

-- ❌ NO usa índice (tienda_id no es la primera columna)
SELECT * FROM ventas WHERE tienda_id = 5;
```

**Regla de oro**: En índices compuestos, el orden importa. Usa primero las columnas que filtras más seguido.

**3. Índice Único (Unique Index)**
```sql
CREATE UNIQUE INDEX idx_usuarios_email_unico ON usuarios(email);
```
Garantiza que no haya duplicados Y acelera búsquedas:
```sql
-- ✅ Usa índice + garantiza email único
SELECT * FROM usuarios WHERE email = 'maria@example.com';
```

**Uso en Data Engineering**: Claves primarias siempre tienen índice único automático.

**4. Índice Parcial (Partial Index)**
```sql
CREATE INDEX idx_pedidos_pendientes
ON pedidos(fecha)
WHERE estado = 'pendiente';
```
Solo indexa registros que cumplen una condición. Más pequeño y rápido.

**Ejemplo real**: Si solo el 5% de tus pedidos están pendientes, ¿por qué indexar el 100%?

#### ¿Cuándo crear un índice?

✅ **SÍ crear índice si**:
- La columna aparece frecuentemente en `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`
- La tabla tiene >10,000 registros
- La columna tiene alta cardinalidad (muchos valores únicos)
- La consulta es lenta (>1 segundo) y se ejecuta frecuentemente

❌ **NO crear índice si**:
- La tabla tiene <10,000 registros (full scan es rápido)
- La columna tiene baja cardinalidad (ejemplo: columna `genero` con solo 'M'/'F')
- La tabla recibe muchas escrituras (`INSERT`/`UPDATE`) porque índices ralentizan escrituras
- Ya existe un índice compuesto que cubre esa columna

**Analogía**: Crear índices es como agregar señales de tráfico. Muy pocas = te pierdes. Demasiadas = saturación y confusión.

#### Costo de los índices

Los índices NO son gratis:

1. **Espacio en disco**: Un índice puede ocupar 20-50% del tamaño de la tabla
2. **Escrituras más lentas**: Cada `INSERT`/`UPDATE`/`DELETE` debe actualizar todos los índices
3. **Mantenimiento**: Índices pueden fragmentarse y necesitar reconstrucción

**Regla práctica**: Una tabla puede tener 3-7 índices. Más de 10 índices es sospechoso.

---

### 3. EXPLAIN: La Radiografía de tus Consultas

#### ¿Qué es EXPLAIN?

`EXPLAIN` te muestra el **plan de ejecución** que la base de datos eligió para tu consulta.

**Analogía**: Es como pedirle a Google Maps que te explique POR QUÉ eligió esa ruta en lugar de las otras.

#### EXPLAIN vs EXPLAIN ANALYZE

**EXPLAIN** (sin ejecutar):
```sql
EXPLAIN SELECT * FROM usuarios WHERE email = 'test@example.com';
```
- Muestra el plan **estimado** (predicción)
- **NO ejecuta** la consulta
- Usa estadísticas de la tabla
- **Rápido**: Toma milisegundos

**EXPLAIN ANALYZE** (ejecuta de verdad):
```sql
EXPLAIN ANALYZE SELECT * FROM usuarios WHERE email = 'test@example.com';
```
- Muestra el plan **real** (lo que realmente pasó)
- **SÍ ejecuta** la consulta (¡cuidado en producción!)
- Incluye tiempos reales de ejecución
- **Lento**: Toma lo que tarde la consulta

**Cuándo usar cada uno**:
- Desarrollo/Testing: `EXPLAIN ANALYZE` (quieres datos reales)
- Producción: `EXPLAIN` (no quieres ejecutar consultas peligrosas)

#### Interpretando EXPLAIN (PostgreSQL)

```sql
EXPLAIN SELECT * FROM usuarios WHERE edad > 25;
```

**Salida sin índice**:
```
Seq Scan on usuarios  (cost=0.00..1808.00 rows=50000 width=200)
  Filter: (edad > 25)
```

**Lectura**:
- `Seq Scan`: Lectura secuencial (lee TODA la tabla, fila por fila)
- `cost=0.00..1808.00`: Costo estimado de 0 a 1808 unidades
- `rows=50000`: Estima que devolverá 50,000 filas
- `width=200`: Cada fila ocupa ~200 bytes
- `Filter: (edad > 25)`: Filtra registros DESPUÉS de leerlos

**Salida con índice**:
```
Index Scan using idx_usuarios_edad on usuarios  (cost=0.29..1234.50 rows=50000 width=200)
  Index Cond: (edad > 25)
```

**Lectura**:
- `Index Scan`: Usa el índice (¡mucho mejor!)
- `cost=0.29..1234.50`: **Costo menor** que Seq Scan
- `Index Cond: (edad > 25)`: Filtra usando el índice (más eficiente)

**Tipos de escaneo de mejor a peor**:

1. **Index Only Scan** (⭐⭐⭐⭐⭐): Lee SOLO el índice, ni siquiera toca la tabla
   ```sql
   SELECT edad FROM usuarios WHERE edad > 25;  -- Solo pide 'edad' que está en el índice
   ```

2. **Index Scan** (⭐⭐⭐⭐): Usa índice para encontrar registros, luego lee la tabla
   ```sql
   SELECT * FROM usuarios WHERE edad > 25;  -- Necesita otras columnas de la tabla
   ```

3. **Bitmap Index Scan** (⭐⭐⭐): Crea un "mapa" de dónde están los registros antes de leerlos
   ```sql
   SELECT * FROM usuarios WHERE edad > 25 OR ciudad = 'Madrid';  -- Combina índices
   ```

4. **Seq Scan** (⭐): Lee toda la tabla secuencialmente (lento para tablas grandes)
   ```sql
   SELECT * FROM usuarios;  -- Sin filtros, debe leer todo
   ```

#### EXPLAIN ANALYZE con métricas reales (PostgreSQL)

```sql
EXPLAIN ANALYZE SELECT * FROM ventas WHERE fecha >= '2024-01-01';
```

**Salida**:
```
Index Scan using idx_ventas_fecha on ventas
  (cost=0.43..8523.67 rows=125000 width=120)
  (actual time=0.052..45.234 rows=128543 loops=1)
  Index Cond: (fecha >= '2024-01-01'::date)
Planning Time: 0.234 ms
Execution Time: 52.123 ms
```

**Métricas clave**:
- `actual time=0.052..45.234`: Tiempo real en **milisegundos**
  - `0.052 ms`: Tiempo hasta el primer registro
  - `45.234 ms`: Tiempo hasta el último registro
- `rows=128543`: Devolvió 128,543 filas (vs. estimado 125,000 → buena estimación)
- `Planning Time: 0.234 ms`: Tiempo que tardó en generar el plan
- `Execution Time: 52.123 ms`: Tiempo total de ejecución real

**Qué buscar**:
- ✅ **Execution Time < 100 ms**: Consulta rápida
- ⚠️ **Execution Time 100-1000 ms**: Consulta lenta, considera optimizar
- ❌ **Execution Time > 1000 ms**: Consulta muy lenta, DEBES optimizar

---

### 4. Técnicas de Optimización de Consultas

#### Técnica 1: Seleccionar solo columnas necesarias

❌ **MAL** (trae TODO):
```sql
SELECT * FROM usuarios;  -- Trae 50 columnas que no necesitas
```

✅ **BIEN** (trae solo lo que necesitas):
```sql
SELECT id, nombre, email FROM usuarios;  -- Solo 3 columnas
```

**Por qué importa**:
- Menos datos = menos tiempo de transferencia
- Puede permitir **Index Only Scan** si las columnas están en el índice
- Reduce uso de red y memoria

**Impacto real**: En una tabla con 20 columnas, `SELECT *` puede ser 5-10x más lento que seleccionar 2 columnas.

#### Técnica 2: Filtrar lo antes posible

❌ **MAL** (filtra en Python después):
```python
# Lee 10 millones de registros
df = pd.read_sql("SELECT * FROM ventas", conn)
# Filtra en memoria (lento)
df_2024 = df[df['fecha'] >= '2024-01-01']
```

✅ **BIEN** (filtra en SQL):
```python
# Lee solo 500,000 registros relevantes
df = pd.read_sql(
    "SELECT * FROM ventas WHERE fecha >= '2024-01-01'",
    conn
)
```

**Por qué importa**:
- SQL filtra antes de transferir datos
- Reduce uso de red y memoria
- Aprovecha índices

#### Técnica 3: Usar LIMIT para exploración

❌ **MAL** (cuando solo quieres ver datos):
```sql
SELECT * FROM logs_acceso;  -- Lee 50 millones de registros
```

✅ **BIEN**:
```sql
SELECT * FROM logs_acceso LIMIT 100;  -- Lee solo 100 registros
```

**Uso en Data Engineering**: Cuando exploras una tabla nueva, SIEMPRE usa `LIMIT` primero.

#### Técnica 4: Evitar funciones en columnas del WHERE

❌ **MAL** (no usa índice):
```sql
-- Aplica UPPER() a CADA fila antes de comparar
SELECT * FROM usuarios WHERE UPPER(email) = 'TEST@EXAMPLE.COM';
```

✅ **BIEN** (usa índice):
```sql
-- Normaliza el valor que buscas, no la columna
SELECT * FROM usuarios WHERE email = LOWER('TEST@EXAMPLE.COM');
```

**Por qué**: Funciones en columnas indexadas **desactivan el índice**.

**Excepciones**: Índices funcionales (PostgreSQL):
```sql
CREATE INDEX idx_usuarios_email_upper ON usuarios(UPPER(email));
-- Ahora SÍ usará este índice:
SELECT * FROM usuarios WHERE UPPER(email) = 'TEST@EXAMPLE.COM';
```

#### Técnica 5: JOINs eficientes

❌ **MAL** (Cartesian Product):
```sql
SELECT *
FROM usuarios, pedidos
WHERE usuarios.ciudad = 'Madrid';  -- ❌ Olvida relacionar las tablas
```
Resultado: Si usuarios tiene 1000 filas y pedidos tiene 10,000 filas → **10,000,000 filas** (explosión combinatoria)

✅ **BIEN**:
```sql
SELECT *
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id
WHERE u.ciudad = 'Madrid';
```

**Reglas de oro para JOINs**:

1. **Siempre especifica la condición de JOIN**:
   ```sql
   FROM tabla1 JOIN tabla2 ON tabla1.id = tabla2.tabla1_id
   ```

2. **Indexa las columnas de JOIN**:
   ```sql
   CREATE INDEX idx_pedidos_usuario ON pedidos(usuario_id);
   ```

3. **Filtra ANTES del JOIN cuando sea posible**:
   ```sql
   -- ✅ Filtra usuarios primero, luego JOIN
   SELECT *
   FROM (SELECT * FROM usuarios WHERE ciudad = 'Madrid') u
   INNER JOIN pedidos p ON u.id = p.usuario_id;
   ```

4. **Usa el tipo de JOIN correcto**:
   - `INNER JOIN`: Solo registros que coinciden en ambas tablas (más rápido)
   - `LEFT JOIN`: Todos de la izquierda + coincidencias (más lento)
   - `FULL OUTER JOIN`: Todos de ambas tablas (más lento aún)

#### Técnica 6: Evitar subconsultas correlacionadas

❌ **MAL** (subconsulta ejecutada por CADA fila):
```sql
SELECT u.nombre,
       (SELECT COUNT(*) FROM pedidos p WHERE p.usuario_id = u.id) as total_pedidos
FROM usuarios u;
```
Si hay 10,000 usuarios → ejecuta la subconsulta **10,000 veces**

✅ **BIEN** (JOIN + agregación):
```sql
SELECT u.nombre, COUNT(p.id) as total_pedidos
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
GROUP BY u.id, u.nombre;
```
Ejecuta **una sola vez**, agrupa al final.

**Impacto**: Puede ser 100-1000x más rápido.

#### Técnica 7: EXISTS vs IN para subconsultas

❌ **LENTO** (con IN y muchos valores):
```sql
SELECT * FROM usuarios
WHERE id IN (SELECT usuario_id FROM pedidos WHERE fecha >= '2024-01-01');
```

✅ **RÁPIDO** (con EXISTS):
```sql
SELECT * FROM usuarios u
WHERE EXISTS (
    SELECT 1 FROM pedidos p
    WHERE p.usuario_id = u.id AND p.fecha >= '2024-01-01'
);
```

**Por qué EXISTS es mejor**:
- `IN`: Ejecuta la subconsulta completa, crea una lista, busca en ella
- `EXISTS`: Se detiene en cuanto encuentra UNA coincidencia (early exit)

**Regla**: Usa `EXISTS` cuando solo te importa si hay coincidencia (sí/no). Usa `IN` cuando la subconsulta devuelve pocos valores (<1000).

#### Técnica 8: UNION vs UNION ALL

❌ **LENTO** (elimina duplicados):
```sql
SELECT nombre FROM usuarios_activos
UNION
SELECT nombre FROM usuarios_inactivos;
```
`UNION`: Ordena y elimina duplicados (costoso)

✅ **RÁPIDO** (si sabes que no hay duplicados):
```sql
SELECT nombre FROM usuarios_activos
UNION ALL
SELECT nombre FROM usuarios_inactivos;
```
`UNION ALL`: Solo concatena (rápido)

**Regla**: Usa `UNION ALL` siempre que NO necesites eliminar duplicados.

---

### 5. Mantenimiento de Índices

Los índices no son "crea y olvida". Necesitan mantenimiento.

#### Problema: Fragmentación de índices

Con el tiempo, `INSERT`/`UPDATE`/`DELETE` fragmentan los índices:

**Analogía**: Como un libro donde arrancas páginas y pegas páginas nuevas. Eventualmente, el índice al final del libro ya no refleja correctamente dónde están los temas.

#### Solución: Reconstruir índices

**PostgreSQL**:
```sql
-- Reconstruir un índice específico
REINDEX INDEX idx_usuarios_email;

-- Reconstruir todos los índices de una tabla
REINDEX TABLE usuarios;
```

**Cuándo hacerlo**:
- Después de cargas masivas de datos
- Si las consultas se vuelven lentas gradualmente
- Una vez por semana/mes en tablas con muchas escrituras

#### Actualizar estadísticas

La BD usa estadísticas para elegir planes de ejecución. Si están desactualizadas, elegirá mal.

**PostgreSQL**:
```sql
ANALYZE usuarios;  -- Actualiza estadísticas de 'usuarios'
VACUUM ANALYZE;    -- Limpia espacio muerto + actualiza estadísticas
```

**MySQL**:
```sql
ANALYZE TABLE usuarios;
```

**Cuándo hacerlo**:
- Después de cargar muchos datos nuevos
- Si `EXPLAIN` muestra estimaciones muy incorrectas (rows estimado ≠ rows real)
- Automático en PostgreSQL (autovacuum), pero puedes forzarlo

---

## Aplicaciones en Data Engineering

### 1. Optimización de Pipelines ETL

**Escenario**: Pipeline que extrae 10 millones de registros diarios.

**Problema**:
```python
# ❌ Lee TODO, filtra después
df = pd.read_sql("SELECT * FROM transacciones", conn)
df_hoy = df[df['fecha'] == date.today()]
```
Lee 10 millones de registros → 5 GB de datos → tarda 10 minutos

**Solución optimizada**:
```python
# ✅ Filtra en SQL, usa índice
query = """
SELECT id, monto, cliente_id, fecha
FROM transacciones
WHERE fecha = CURRENT_DATE
"""
df_hoy = pd.read_sql(query, conn)
```
Lee 30,000 registros → 15 MB de datos → tarda 2 segundos

**Técnicas aplicadas**:
- Filtro en SQL (no en Pandas)
- Solo columnas necesarias
- Índice en columna `fecha`

**Impacto**: 300x más rápido (10 min → 2 seg)

### 2. Optimización de Data Warehouses

**Escenario**: Dashboard de ventas ejecuta esta consulta cada minuto:

```sql
SELECT p.categoria, SUM(v.monto) as total_ventas
FROM ventas v
INNER JOIN productos p ON v.producto_id = p.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY p.categoria;
```

**Optimizaciones**:

1. **Índice compuesto**:
   ```sql
   CREATE INDEX idx_ventas_fecha_producto ON ventas(fecha, producto_id);
   ```

2. **Tabla materializada** (pre-calculada):
   ```sql
   CREATE MATERIALIZED VIEW ventas_por_categoria AS
   SELECT p.categoria, DATE_TRUNC('day', v.fecha) as fecha, SUM(v.monto) as total
   FROM ventas v
   INNER JOIN productos p ON v.producto_id = p.id
   GROUP BY p.categoria, DATE_TRUNC('day', v.fecha);

   CREATE INDEX idx_ventas_cat_fecha ON ventas_por_categoria(fecha);
   ```

3. **Consulta optimizada**:
   ```sql
   SELECT categoria, SUM(total) as total_ventas
   FROM ventas_por_categoria
   WHERE fecha BETWEEN '2024-01-01' AND '2024-12-31'
   GROUP BY categoria;
   ```

**Resultado**: Consulta que tardaba 8 segundos → 0.05 segundos (160x más rápida)

### 3. Optimización de APIs de Datos

**Escenario**: API que devuelve productos filtrados por usuario.

**Sin optimización**:
```sql
SELECT * FROM productos WHERE id IN (
    SELECT producto_id FROM favoritos WHERE usuario_id = 12345
);
```
Tarda 2.5 segundos → usuarios abandonan

**Con optimización**:
```sql
SELECT p.id, p.nombre, p.precio
FROM productos p
WHERE EXISTS (
    SELECT 1 FROM favoritos f
    WHERE f.producto_id = p.id AND f.usuario_id = 12345
);
```
Tarda 0.1 segundos → experiencia fluida

**Técnicas aplicadas**:
- `EXISTS` en lugar de `IN`
- Solo columnas necesarias
- Índices en `favoritos(usuario_id, producto_id)`

---

## Errores Comunes

### Error 1: "Más índices = Más rápido"

❌ **Falso**. Demasiados índices ralentizan escrituras y confunden al optimizer.

**Escenario real**: Una tabla con 15 índices donde cada `INSERT` tardaba 500 ms. Eliminando 8 índices innecesarios → `INSERT` en 50 ms.

**Regla**: 3-7 índices por tabla es razonable. Más de 10 es sospechoso.

### Error 2: No usar EXPLAIN antes de crear índices

❌ **Mal enfoque**: "Esta consulta es lenta, creo un índice en todas las columnas del WHERE"

✅ **Buen enfoque**:
1. Ejecuta `EXPLAIN ANALYZE`
2. Identifica el cuello de botella (Seq Scan, subconsulta lenta, JOIN pesado)
3. Crea el índice específico que resuelve ESE problema
4. Verifica con `EXPLAIN ANALYZE` que ahora usa el índice

### Error 3: Crear índices en columnas de baja cardinalidad

❌ **Inútil**:
```sql
CREATE INDEX idx_usuarios_activo ON usuarios(activo);  -- Solo valores: true/false
```
Un índice en una columna con 2 valores únicos no ayuda. La BD igual debe leer ~50% de la tabla.

**Regla**: Solo indexa columnas con alta cardinalidad (muchos valores únicos). Columnas con <100 valores únicos rara vez necesitan índice.

### Error 4: Usar SELECT * en producción

❌ **Nunca en producción**:
```sql
SELECT * FROM logs;  -- Puede devolver 50 columnas y 10 GB
```

✅ **Específico**:
```sql
SELECT timestamp, level, message FROM logs WHERE timestamp >= NOW() - INTERVAL '1 hour';
```

### Error 5: No mantener estadísticas actualizadas

**Síntoma**: `EXPLAIN` dice "rows=100" pero la consulta devuelve 1,000,000 registros.

**Causa**: Estadísticas desactualizadas. La BD piensa que la tabla es pequeña cuando en realidad creció 10,000x.

**Solución**:
```sql
ANALYZE tabla;  -- PostgreSQL
ANALYZE TABLE tabla;  -- MySQL
```

### Error 6: Ignorar el Query Plan

❌ **Mal hábito**: Escribir consulta, ejecutarla, si funciona → listo.

✅ **Buen hábito**:
1. Escribe consulta
2. `EXPLAIN ANALYZE` en desarrollo
3. Verifica que usa índices correctos
4. Si tarda >100 ms → optimiza

---

## Checklist de Aprendizaje

Al final de este tema, deberías poder responder SÍ a todas estas preguntas:

### Conceptos Básicos
- [ ] ¿Puedo explicar qué es un índice y por qué acelera las consultas?
- [ ] ¿Entiendo la diferencia entre Seq Scan e Index Scan?
- [ ] ¿Sé cuándo crear un índice y cuándo NO crearlo?
- [ ] ¿Puedo explicar qué hace el Query Optimizer?

### EXPLAIN
- [ ] ¿Sé usar `EXPLAIN` y `EXPLAIN ANALYZE`?
- [ ] ¿Puedo interpretar el output de EXPLAIN (Seq Scan vs Index Scan)?
- [ ] ¿Entiendo qué significa "cost" y "rows"?
- [ ] ¿Puedo identificar si una consulta está usando un índice?

### Índices
- [ ] ¿Sé crear índices simples y compuestos?
- [ ] ¿Entiendo que el orden de columnas importa en índices compuestos?
- [ ] ¿Puedo identificar cuándo un índice NO ayuda (baja cardinalidad)?
- [ ] ¿Sé que los índices ralentizan escrituras?

### Optimización
- [ ] ¿Puedo optimizar una consulta lenta usando EXPLAIN?
- [ ] ¿Sé cuándo usar `EXISTS` vs `IN`?
- [ ] ¿Entiendo por qué `SELECT *` es malo en producción?
- [ ] ¿Puedo evitar subconsultas correlacionadas?

### Mantenimiento
- [ ] ¿Sé cuándo reconstruir índices (REINDEX)?
- [ ] ¿Sé cuándo actualizar estadísticas (ANALYZE)?
- [ ] ¿Entiendo que los índices necesitan mantenimiento?

### Data Engineering
- [ ] ¿Puedo optimizar pipelines ETL filtrando en SQL?
- [ ] ¿Sé cuándo usar tablas materializadas?
- [ ] ¿Puedo diseñar índices para un data warehouse?

---

## Resumen Ejecutivo

### Conceptos Clave

1. **Índices = Atajos**: Permiten buscar sin leer toda la tabla
2. **EXPLAIN = Radiografía**: Muestra cómo la BD ejecutará tu consulta
3. **Optimizar = Entender el plan**: Usa EXPLAIN para saber qué optimizar
4. **No siempre más índices = mejor**: Balance entre lecturas y escrituras
5. **Filtrar en SQL, no en código**: Reduce transferencia de datos

### Reglas de Oro

1. **Usa EXPLAIN** antes de crear índices
2. **Indexa columnas** en WHERE, JOIN, ORDER BY, GROUP BY
3. **Evita SELECT *** en producción
4. **Filtra lo antes posible** (en SQL, no en Python)
5. **Mantén índices** (REINDEX + ANALYZE periódicamente)
6. **3-7 índices por tabla** es razonable
7. **Usa EXISTS** en lugar de IN para subconsultas grandes
8. **Evita funciones** en columnas indexadas del WHERE

### Prioridades de Optimización

1. **Primero**: Verifica con EXPLAIN que la consulta usa índices
2. **Segundo**: Crea índices faltantes en columnas clave
3. **Tercero**: Reescribe consultas ineficientes (subconsultas correlacionadas, SELECT *)
4. **Cuarto**: Considera tablas materializadas para agregaciones pesadas

---

## Próximos Pasos

1. **Lee los Ejemplos** (`02-EJEMPLOS.md`): Verás casos reales de optimización
2. **Practica los Ejercicios** (`03-EJERCICIOS.md`): 15 ejercicios progresivos
3. **Construye el Proyecto** (`04-proyecto-practico/`): Sistema de optimización SQL con TDD

---

**¡Estás listo para escribir SQL que escale a millones de registros!** 🚀

**Tiempo estimado de lectura**: 35-40 minutos
**Palabras**: ~4,200
---

## 🧭 Navegación

⬅️ **Anterior**: [SQL Intermedio - Proyecto Práctico](../tema-2-sql-intermedio/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
