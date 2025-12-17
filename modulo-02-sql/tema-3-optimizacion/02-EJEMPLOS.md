# Ejemplos Prácticos: Optimización de Consultas SQL

Este documento contiene 5 ejemplos progresivos que demuestran técnicas de optimización SQL en contextos empresariales realistas.

---

## Ejemplo 1: Primer Índice y EXPLAIN - Nivel: Básico ⭐

### Contexto

Trabajas para **TechFlow Solutions**, una startup de software. La tabla `usuarios` tiene 500,000 registros y las consultas de búsqueda por email tardan 3 segundos. El equipo de producto se queja de que el login es muy lento.

### Situación Inicial

**Tabla**: `usuarios`
- Columnas: `id`, `nombre`, `email`, `fecha_registro`, `activo`, `plan`
- Registros: 500,000
- Índices: Solo PRIMARY KEY en `id`

### Consulta problemática

```sql
SELECT id, nombre, email
FROM usuarios
WHERE email = 'maria.garcia@example.com';
```

**Tiempo de ejecución**: 2.8 segundos ❌

### Paso 1: Diagnosticar con EXPLAIN

```sql
EXPLAIN SELECT id, nombre, email
FROM usuarios
WHERE email = 'maria.garcia@example.com';
```

**Resultado**:
```
Seq Scan on usuarios  (cost=0.00..12500.00 rows=1 width=120)
  Filter: (email = 'maria.garcia@example.com'::text)
```

**Interpretación**:
- `Seq Scan`: Está leyendo TODA la tabla (500,000 filas)
- `cost=12500.00`: Costo alto (proporcional al tamaño de la tabla)
- `rows=1`: Estima que encontrará 1 fila (correcto, email es único)
- `Filter`: Aplica el filtro DESPUÉS de leer todas las filas

**Diagnóstico**: No hay índice en `email` → la BD debe escanear todos los registros uno por uno.

### Paso 2: Crear índice

```sql
CREATE INDEX idx_usuarios_email ON usuarios(email);
```

**Tiempo de creación**: ~8 segundos (para 500,000 registros)

### Paso 3: Verificar mejora con EXPLAIN

```sql
EXPLAIN SELECT id, nombre, email
FROM usuarios
WHERE email = 'maria.garcia@example.com';
```

**Resultado MEJORADO**:
```
Index Scan using idx_usuarios_email on usuarios  (cost=0.42..8.44 rows=1 width=120)
  Index Cond: (email = 'maria.garcia@example.com'::text)
```

**Interpretación**:
- `Index Scan`: ¡Ahora usa el índice! ✅
- `cost=8.44`: Costo **1,483x menor** (de 12,500 a 8.44)
- `Index Cond`: Filtra usando el índice (eficiente)

### Paso 4: Medir tiempo real con EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT id, nombre, email
FROM usuarios
WHERE email = 'maria.garcia@example.com';
```

**Resultado**:
```
Index Scan using idx_usuarios_email on usuarios
  (cost=0.42..8.44 rows=1 width=120)
  (actual time=0.034..0.036 rows=1 loops=1)
Planning Time: 0.122 ms
Execution Time: 0.058 ms
```

**Métricas clave**:
- `actual time=0.034..0.036`: **0.036 ms** (antes: 2,800 ms)
- `Execution Time: 0.058 ms`

### Resultado Final

- **Antes**: 2.8 segundos
- **Después**: 0.058 ms (0.000058 segundos)
- **Mejora**: **48,275x más rápido** 🚀

### Código Python para verificar

```python
import psycopg2
import time
from sqlalchemy import create_engine

# Conectar a PostgreSQL
engine = create_engine("postgresql://user:password@localhost/techflow_db")

# Medir tiempo sin índice (antes de crearlo)
query = """
SELECT id, nombre, email
FROM usuarios
WHERE email = 'maria.garcia@example.com'
"""

start = time.time()
with engine.connect() as conn:
    result = conn.execute(query)
    row = result.fetchone()
end = time.time()

print(f"Tiempo: {(end - start) * 1000:.2f} ms")
# Output después del índice: Tiempo: 0.06 ms
```

### Lección Aprendida

**Un solo índice bien colocado puede acelerar consultas 10,000x+**. Siempre usa `EXPLAIN` antes de crear índices para confirmar que la BD los usará.

---

## Ejemplo 2: Optimizando JOINs Lentos - Nivel: Intermedio ⭐⭐

### Contexto

Trabajas para **DataMart Express**, una cadena de supermercados. El dashboard de ventas ejecuta una consulta que tarda 12 segundos, y se ejecuta cada vez que un gerente abre el reporte (50 veces por día).

### Datos

**Tabla `ventas`**: 5,000,000 registros
- Columnas: `id`, `producto_id`, `tienda_id`, `cantidad`, `monto`, `fecha`

**Tabla `productos`**: 10,000 registros
- Columnas: `id`, `nombre`, `categoria`, `precio_unitario`

**Tabla `tiendas`**: 50 registros
- Columnas: `id`, `nombre`, `ciudad`, `region`

### Consulta problemática

```sql
SELECT t.ciudad,
       p.categoria,
       SUM(v.monto) as total_ventas,
       COUNT(*) as num_transacciones
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN tiendas t ON v.tienda_id = t.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY t.ciudad, p.categoria
ORDER BY total_ventas DESC;
```

**Tiempo actual**: 12.3 segundos ❌

### Paso 1: Analizar con EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT t.ciudad, p.categoria, SUM(v.monto) as total_ventas, COUNT(*) as num_transacciones
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN tiendas t ON v.tienda_id = t.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY t.ciudad, p.categoria
ORDER BY total_ventas DESC;
```

**Resultado (simplificado)**:
```
Sort  (cost=450000..455000 rows=2000) (actual time=12234..12256 rows=150 loops=1)
  -> GroupAggregate  (cost=420000..448000 rows=2000) (actual time=8500..12100 rows=150 loops=1)
       -> Hash Join  (cost=3500..410000 rows=1250000) (actual time=45..7800 rows=1250000 loops=1)
            -> Seq Scan on ventas v  (cost=0..380000 rows=1250000) (actual time=0..6500 rows=1250000 loops=1)
                 Filter: (fecha >= '2024-01-01' AND fecha <= '2024-03-31')
                 Rows Removed by Filter: 3750000
            -> Hash  (cost=2000..2000 rows=10000) (actual time=22..22 rows=10000 loops=1)
                 -> Seq Scan on productos p
Execution Time: 12278 ms
```

**Problemas identificados**:
1. `Seq Scan on ventas`: Lee **toda** la tabla (5 millones) y filtra después → elimina 3.75 millones
2. No usa índice en `fecha` → filtrado lento
3. JOINs potencialmente lentos por falta de índices en foreign keys

### Paso 2: Crear índices estratégicos

```sql
-- Índice en columna de filtro (fecha)
CREATE INDEX idx_ventas_fecha ON ventas(fecha);

-- Índices en columnas de JOIN (foreign keys)
CREATE INDEX idx_ventas_producto_id ON ventas(producto_id);
CREATE INDEX idx_ventas_tienda_id ON ventas(tienda_id);
```

**Tiempo de creación**: ~25 segundos total

### Paso 3: Verificar mejora

```sql
EXPLAIN ANALYZE
SELECT t.ciudad, p.categoria, SUM(v.monto) as total_ventas, COUNT(*) as num_transacciones
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN tiendas t ON v.tienda_id = t.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY t.ciudad, p.categoria
ORDER BY total_ventas DESC;
```

**Resultado MEJORADO**:
```
Sort  (cost=85000..85500 rows=2000) (actual time=1456..1462 rows=150 loops=1)
  -> GroupAggregate  (cost=78000..84000 rows=2000) (actual time=1200..1450 rows=150 loops=1)
       -> Hash Join  (cost=2500..75000 rows=1250000) (actual time=12..980 rows=1250000 loops=1)
            -> Index Scan using idx_ventas_fecha on ventas v  (cost=0..68000 rows=1250000) (actual time=0.05..850 rows=1250000 loops=1)
                 Index Cond: (fecha >= '2024-01-01' AND fecha <= '2024-03-31')
            -> Hash  (cost=2000..2000 rows=10000) (actual time=11..11 rows=10000 loops=1)
                 -> Seq Scan on productos p
Execution Time: 1468 ms
```

**Mejoras observadas**:
- `Index Scan using idx_ventas_fecha`: ¡Ahora usa índice en fecha! ✅
- `Execution Time: 1468 ms` (antes: 12,278 ms) → **8.4x más rápido**

### Paso 4: Optimización adicional con índice compuesto

Podemos hacerlo aún mejor con un índice que cubra fecha + foreign keys:

```sql
-- Índice compuesto para evitar leer la tabla
CREATE INDEX idx_ventas_fecha_producto_tienda_monto
ON ventas(fecha, producto_id, tienda_id, monto);
```

### Paso 5: Verificar optimización final

```sql
EXPLAIN ANALYZE
SELECT t.ciudad, p.categoria, SUM(v.monto) as total_ventas, COUNT(*) as num_transacciones
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN tiendas t ON v.tienda_id = t.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY t.ciudad, p.categoria
ORDER BY total_ventas DESC;
```

**Resultado FINAL**:
```
Execution Time: 385 ms
```

### Resultado Final

- **Antes**: 12,278 ms (12.3 segundos)
- **Con índices simples**: 1,468 ms (1.5 segundos) → 8.4x más rápido
- **Con índice compuesto**: 385 ms (0.4 segundos) → **31.9x más rápido** 🚀

### Código Python

```python
from sqlalchemy import create_engine, text
import time

engine = create_engine("postgresql://user:password@localhost/datamart_db")

query = text("""
SELECT t.ciudad, p.categoria, SUM(v.monto) as total_ventas, COUNT(*) as num_transacciones
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN tiendas t ON v.tienda_id = t.id
WHERE v.fecha BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY t.ciudad, p.categoria
ORDER BY total_ventas DESC
""")

# Medir tiempo
start = time.time()
with engine.connect() as conn:
    result = conn.execute(query)
    rows = result.fetchall()
end = time.time()

print(f"Tiempo: {(end - start) * 1000:.0f} ms")
print(f"Resultados: {len(rows)} filas")
# Output: Tiempo: 385 ms, Resultados: 150 filas
```

### Lección Aprendida

**Para consultas con JOINs**:
1. Indexa columnas en `WHERE` (especialmente rangos de fechas)
2. Indexa columnas de `JOIN` (foreign keys)
3. Considera índices compuestos que cubran múltiples columnas usadas juntas

---

## Ejemplo 3: Índice Compuesto Eficiente - Nivel: Intermedio ⭐⭐

### Contexto

Trabajas para **LogiTrans**, una empresa de logística. La aplicación móvil de conductores consulta entregas pendientes por conductor y zona, pero es lenta.

### Datos

**Tabla `entregas`**: 2,000,000 registros
- Columnas: `id`, `conductor_id`, `zona`, `estado`, `fecha_asignada`, `direccion`, `prioridad`

### Consultas frecuentes

```sql
-- Consulta 1: Entregas pendientes de un conductor en una zona (80% de consultas)
SELECT * FROM entregas
WHERE conductor_id = 42 AND zona = 'Norte' AND estado = 'pendiente';

-- Consulta 2: Entregas pendientes de un conductor (15% de consultas)
SELECT * FROM entregas
WHERE conductor_id = 42 AND estado = 'pendiente';

-- Consulta 3: Entregas de una zona (5% de consultas)
SELECT * FROM entregas
WHERE zona = 'Norte' AND estado = 'pendiente';
```

### Paso 1: Intentar índices simples (enfoque ingenuo)

```sql
CREATE INDEX idx_entregas_conductor ON entregas(conductor_id);
CREATE INDEX idx_entregas_zona ON entregas(zona);
CREATE INDEX idx_entregas_estado ON entregas(estado);
```

### Paso 2: Verificar con EXPLAIN (Consulta 1)

```sql
EXPLAIN ANALYZE
SELECT * FROM entregas
WHERE conductor_id = 42 AND zona = 'Norte' AND estado = 'pendiente';
```

**Resultado**:
```
Bitmap Heap Scan on entregas  (cost=500..8500 rows=250) (actual time=45..120 rows=250 loops=1)
  Recheck Cond: (conductor_id = 42)
  Filter: (zona = 'Norte' AND estado = 'pendiente')
  -> Bitmap Index Scan on idx_entregas_conductor  (cost=0..500 rows=2000) (actual time=12..12 rows=2000 loops=1)
Execution Time: 125 ms
```

**Problema**: Solo usa el índice de `conductor_id`, luego filtra `zona` y `estado` manualmente → lee 2,000 filas para devolver 250.

### Paso 3: Crear índice compuesto estratégico

**Análisis**:
- Consulta 1 (80%): filtra por `conductor_id` + `zona` + `estado`
- Consulta 2 (15%): filtra por `conductor_id` + `estado`
- Consulta 3 (5%): filtra por `zona` + `estado`

**Decisión**: Crear índice compuesto con orden: `conductor_id`, `zona`, `estado`

**¿Por qué ese orden?**
1. `conductor_id` primero: Alta cardinalidad (500 conductores únicos)
2. `zona` segundo: Media cardinalidad (10 zonas)
3. `estado` último: Baja cardinalidad (3 estados: pendiente, en_curso, completada)

```sql
-- Eliminar índices simples
DROP INDEX idx_entregas_conductor;
DROP INDEX idx_entregas_zona;
DROP INDEX idx_entregas_estado;

-- Crear índice compuesto
CREATE INDEX idx_entregas_conductor_zona_estado
ON entregas(conductor_id, zona, estado);
```

### Paso 4: Verificar mejora (Consulta 1)

```sql
EXPLAIN ANALYZE
SELECT * FROM entregas
WHERE conductor_id = 42 AND zona = 'Norte' AND estado = 'pendiente';
```

**Resultado MEJORADO**:
```
Index Scan using idx_entregas_conductor_zona_estado on entregas
  (cost=0.42..125.50 rows=250 width=200)
  (actual time=0.05..2.34 rows=250 loops=1)
  Index Cond: (conductor_id = 42 AND zona = 'Norte' AND estado = 'pendiente')
Execution Time: 2.45 ms
```

**Mejora**: 125 ms → 2.45 ms = **51x más rápido** ✅

### Paso 5: Verificar otras consultas

**Consulta 2** (sin `zona`):
```sql
EXPLAIN ANALYZE
SELECT * FROM entregas
WHERE conductor_id = 42 AND estado = 'pendiente';
```

**Resultado**:
```
Index Scan using idx_entregas_conductor_zona_estado on entregas
  (cost=0.42..450.00 rows=800 width=200)
  (actual time=0.05..8.50 rows=800 loops=1)
  Index Cond: (conductor_id = 42)
  Filter: (estado = 'pendiente')
Execution Time: 8.75 ms
```

**Interpretación**: Usa el índice parcialmente (solo `conductor_id`), filtra `estado` después. Aún es rápido (8.75 ms) ✅

**Consulta 3** (sin `conductor_id`):
```sql
EXPLAIN ANALYZE
SELECT * FROM entregas
WHERE zona = 'Norte' AND estado = 'pendiente';
```

**Resultado**:
```
Seq Scan on entregas  (cost=0..45000 rows=25000 width=200)
  Filter: (zona = 'Norte' AND estado = 'pendiente')
Execution Time: 850 ms
```

**Problema**: No usa el índice porque `zona` no es la primera columna. Pero es solo el 5% de consultas → aceptable.

**Opción**: Si Consulta 3 se vuelve frecuente, crear índice adicional en `(zona, estado)`.

### Resultado Final

| Consulta | Antes | Después | Mejora |
|----------|-------|---------|--------|
| Consulta 1 (80%) | 125 ms | 2.45 ms | 51x ✅ |
| Consulta 2 (15%) | 95 ms | 8.75 ms | 11x ✅ |
| Consulta 3 (5%) | 850 ms | 850 ms | 1x (sin cambio) |

**Promedio ponderado**: (0.80 × 51) + (0.15 × 11) + (0.05 × 1) = **42.5x más rápido** en promedio 🚀

### Código Python

```python
from sqlalchemy import create_engine, text
import time

engine = create_engine("postgresql://user:password@localhost/logitrans_db")

# Consulta 1 (más frecuente)
query1 = text("""
SELECT * FROM entregas
WHERE conductor_id = 42 AND zona = 'Norte' AND estado = 'pendiente'
""")

start = time.time()
with engine.connect() as conn:
    result = conn.execute(query1)
    rows = result.fetchall()
end = time.time()

print(f"Consulta 1 - Tiempo: {(end - start) * 1000:.2f} ms, Filas: {len(rows)}")
# Output: Consulta 1 - Tiempo: 2.45 ms, Filas: 250
```

### Lección Aprendida

**Para índices compuestos**:
1. **Orden importa**: Columna más selectiva primero (alta cardinalidad)
2. **Uso parcial**: Si filtras solo primeras columnas, el índice se usa parcialmente
3. **Prioriza consultas frecuentes**: Optimiza el 80% de consultas, no el 5%
4. **Un índice compuesto puede reemplazar múltiples índices simples**

---

## Ejemplo 4: Optimizando Pipeline ETL - Nivel: Avanzado ⭐⭐⭐

### Contexto

Trabajas para **FinTech Global**, procesando transacciones bancarias. Tu pipeline ETL extrae transacciones del día anterior cada mañana a las 6 AM, pero últimamente tarda 45 minutos y bloquea otros pipelines.

### Datos

**Tabla `transacciones`**: 500,000,000 registros (500 millones)
- Columnas: `id`, `cuenta_origen`, `cuenta_destino`, `monto`, `tipo`, `fecha_hora`, `estado`, `pais`
- Crecimiento: +2,000,000 registros/día

### Pipeline actual (Python)

```python
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine("postgresql://user:password@localhost/fintech_db")

# Extraer transacciones de ayer
ayer = (datetime.now() - timedelta(days=1)).date()

# ❌ Consulta lenta
query = f"""
SELECT *
FROM transacciones
WHERE DATE(fecha_hora) = '{ayer}'
"""

print(f"Extrayendo transacciones de {ayer}...")
df = pd.read_sql(query, engine)
print(f"Extraídos {len(df)} registros")

# Transformaciones...
df_resumen = df.groupby(['cuenta_origen', 'tipo']).agg({
    'monto': 'sum',
    'id': 'count'
}).reset_index()

# Cargar a data warehouse...
df_resumen.to_sql('transacciones_diarias', engine, if_exists='append', index=False)
```

**Tiempo actual**: 45 minutos ❌

### Paso 1: Diagnosticar con EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT *
FROM transacciones
WHERE DATE(fecha_hora) = '2024-03-15';
```

**Resultado**:
```
Seq Scan on transacciones  (cost=0..15000000 rows=2000000) (actual time=0..285000 rows=2000000 loops=1)
  Filter: (DATE(fecha_hora) = '2024-03-15')
  Rows Removed by Filter: 498000000
Planning Time: 2.5 ms
Execution Time: 287450 ms  -- ❌ 4.8 minutos solo en consulta SQL
```

**Problemas identificados**:
1. `Seq Scan`: Lee **500 millones de registros** completos
2. `Rows Removed by Filter: 498000000`: Descarta 498 millones después de leerlos
3. `DATE(fecha_hora)`: Función en columna indexada → **no usa índice**

### Paso 2: Crear índice (intento ingenuo - INCORRECTO)

```sql
-- ❌ Esto NO ayudará
CREATE INDEX idx_transacciones_fecha ON transacciones(fecha_hora);
```

**Verificar**:
```sql
EXPLAIN ANALYZE
SELECT *
FROM transacciones
WHERE DATE(fecha_hora) = '2024-03-15';
```

**Resultado**:
```
Seq Scan on transacciones  (cost=0..15000000 rows=2000000)
  Filter: (DATE(fecha_hora) = '2024-03-15')
```

**Problema**: Sigue siendo `Seq Scan` porque `DATE(fecha_hora)` es una función → desactiva el índice.

### Paso 3: Reescribir consulta SIN funciones

```sql
-- ✅ Usa rango en lugar de función DATE()
EXPLAIN ANALYZE
SELECT *
FROM transacciones
WHERE fecha_hora >= '2024-03-15 00:00:00'
  AND fecha_hora < '2024-03-16 00:00:00';
```

**Resultado MEJORADO**:
```
Index Scan using idx_transacciones_fecha on transacciones
  (cost=0.56..125000 rows=2000000) (actual time=0.05..8500 rows=2000000 loops=1)
  Index Cond: (fecha_hora >= '2024-03-15 00:00:00' AND fecha_hora < '2024-03-16 00:00:00')
Planning Time: 0.8 ms
Execution Time: 8950 ms  -- ✅ 8.9 segundos (antes: 287 segundos)
```

**Mejora en consulta SQL**: 287 segundos → 8.9 segundos = **32x más rápido** 🚀

### Paso 4: Optimizar transferencia de datos (SELECT *)

```python
# ❌ ANTES: Trae TODO (30 columnas)
query = f"SELECT * FROM transacciones WHERE fecha_hora >= '{ayer} 00:00:00' AND fecha_hora < '{ayer + timedelta(days=1)} 00:00:00'"

# ✅ DESPUÉS: Solo columnas necesarias
query = f"""
SELECT cuenta_origen, tipo, monto, id
FROM transacciones
WHERE fecha_hora >= '{ayer} 00:00:00'
  AND fecha_hora < '{ayer + timedelta(days=1)} 00:00:00'
"""
```

**Impacto**:
- Antes: 2,000,000 filas × 30 columnas × 50 bytes = 3 GB de datos transferidos
- Después: 2,000,000 filas × 4 columnas × 20 bytes = 160 MB transferidos

**Tiempo de transferencia**: 3 GB @ 50 MB/s = 60 segundos → 160 MB @ 50 MB/s = 3.2 segundos

### Paso 5: Agregar en SQL en lugar de Pandas

```python
# ❌ ANTES: Agrega en Pandas (en memoria)
df = pd.read_sql(query, engine)  # Lee 2M registros
df_resumen = df.groupby(['cuenta_origen', 'tipo']).agg({
    'monto': 'sum',
    'id': 'count'
}).reset_index()

# ✅ DESPUÉS: Agrega en SQL (en base de datos)
query = f"""
SELECT cuenta_origen,
       tipo,
       SUM(monto) as monto_total,
       COUNT(id) as num_transacciones
FROM transacciones
WHERE fecha_hora >= '{ayer} 00:00:00'
  AND fecha_hora < '{ayer + timedelta(days=1)} 00:00:00'
GROUP BY cuenta_origen, tipo
"""

df_resumen = pd.read_sql(query, engine)  # Lee solo ~50,000 registros agregados
```

**Impacto**:
- Antes: Transfiere 2,000,000 registros → agrupa en Python
- Después: Agrega en BD → transfiere solo 50,000 registros agregados

**Mejora**: 40x menos datos transferidos

### Pipeline optimizado completo

```python
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine("postgresql://user:password@localhost/fintech_db")

ayer = (datetime.now() - timedelta(days=1)).date()
hoy = datetime.now().date()

# ✅ Consulta optimizada: filtra con rango, selecciona columnas necesarias, agrega en SQL
query = f"""
SELECT cuenta_origen,
       tipo,
       SUM(monto) as monto_total,
       COUNT(id) as num_transacciones
FROM transacciones
WHERE fecha_hora >= '{ayer} 00:00:00'
  AND fecha_hora < '{hoy} 00:00:00'
GROUP BY cuenta_origen, tipo
"""

print(f"Extrayendo transacciones de {ayer}...")
start = time.time()
df_resumen = pd.read_sql(query, engine)
end = time.time()

print(f"Tiempo de extracción: {end - start:.1f} segundos")
print(f"Registros agregados: {len(df_resumen)}")

# Cargar a data warehouse
df_resumen.to_sql('transacciones_diarias', engine, if_exists='append', index=False)
```

### Resultado Final

| Etapa | Antes | Después | Mejora |
|-------|-------|---------|--------|
| Consulta SQL | 287 s | 8.9 s | 32x |
| Transferencia | 60 s | 3.2 s | 19x |
| Agregación | 120 s | 0 s (en BD) | ∞ |
| **TOTAL** | **45 min** | **12 s** | **225x** 🚀 |

### Lecciones Aprendidas

**Para pipelines ETL**:
1. **Nunca uses funciones en columnas indexadas del WHERE**: `DATE(fecha)` → `fecha >= X AND fecha < Y`
2. **Selecciona solo columnas necesarias**: Evita `SELECT *`
3. **Agrega en SQL, no en Python/Pandas**: La BD es mucho más eficiente
4. **Filtra lo antes posible**: En SQL, no después de extraer
5. **Indexa columnas de filtro**: Especialmente fechas en tablas grandes

---

## Ejemplo 5: Debugging Producción con EXPLAIN ANALYZE - Nivel: Avanzado ⭐⭐⭐

### Contexto

Trabajas para **SocialHub**, una red social. A las 2 AM, empiezan a llegar alertas: el feed de noticias carga en 15+ segundos. Los usuarios se quejan en Twitter. Debes encontrar y solucionar el problema **AHORA**.

### Datos

**Tabla `publicaciones`**: 200,000,000 registros
**Tabla `usuarios`**: 50,000,000 registros
**Tabla `seguidores`**: 1,000,000,000 registros (relación muchos-a-muchos)

### Consulta del feed (simplificada)

```sql
SELECT p.id, p.contenido, p.fecha_creacion, u.nombre, u.foto_perfil
FROM publicaciones p
JOIN usuarios u ON p.usuario_id = u.id
WHERE p.usuario_id IN (
    SELECT seguido_id
    FROM seguidores
    WHERE seguidor_id = 12345
)
ORDER BY p.fecha_creacion DESC
LIMIT 50;
```

### Paso 1: Reproducir el problema

```sql
EXPLAIN ANALYZE
SELECT p.id, p.contenido, p.fecha_creacion, u.nombre, u.foto_perfil
FROM publicaciones p
JOIN usuarios u ON p.usuario_id = u.id
WHERE p.usuario_id IN (
    SELECT seguido_id
    FROM seguidores
    WHERE seguidor_id = 12345
)
ORDER BY p.fecha_creacion DESC
LIMIT 50;
```

**Resultado (problemas marcados con ⚠️)**:
```
Limit  (cost=2500000..2500050 rows=50) (actual time=18456..18478 rows=50 loops=1)
  -> Sort  (cost=2500000..2510000 rows=500000) (actual time=18456..18470 rows=50 loops=1)
       Sort Key: p.fecha_creacion DESC
       Sort Method: top-N heapsort  Memory: 45kB
       -> Hash Join  (cost=850000..2450000 rows=500000) (actual time=3200..17890 rows=500000 loops=1)
            Hash Cond: (p.usuario_id = u.id)
            -> Seq Scan on publicaciones p  ⚠️ (cost=0..1580000 rows=500000) (actual time=0..14500 rows=500000 loops=1)
                 Filter: (usuario_id = ANY ('{list of 500 IDs}'))
                 Rows Removed by Filter: 199500000  ⚠️
            -> Hash  (cost=800000..800000 rows=50000000) (actual time=2800..2800 rows=500 loops=1)
                 -> Seq Scan on usuarios u  (cost=0..800000 rows=50000000)
Planning Time: 15.2 ms
Execution Time: 18512 ms  ⚠️ 18.5 segundos
```

**Problemas críticos identificados**:
1. ⚠️ `Seq Scan on publicaciones`: Lee **200 millones de publicaciones**
2. ⚠️ `Rows Removed by Filter: 199500000`: Descarta 199.5 millones de filas
3. ⚠️ Subconsulta `IN` con 500 IDs (usuario sigue a 500 personas)
4. ⚠️ `Sort` de 500,000 filas antes de aplicar `LIMIT 50`

### Paso 2: Verificar índices existentes

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'publicaciones';
```

**Resultado**:
```
idx_publicaciones_id  -- Solo PRIMARY KEY
```

**Problema**: No hay índice en `usuario_id` ni `fecha_creacion`

### Paso 3: Crear índices faltantes

```sql
-- Índice en usuario_id para filtrar publicaciones por usuario
CREATE INDEX idx_publicaciones_usuario_id ON publicaciones(usuario_id);

-- Índice compuesto para usuario_id + fecha (para ORDER BY)
CREATE INDEX idx_publicaciones_usuario_fecha
ON publicaciones(usuario_id, fecha_creacion DESC);

-- Índice en seguidores para la subconsulta
CREATE INDEX idx_seguidores_seguidor_id ON seguidores(seguidor_id);
```

**Tiempo de creación**: ~8 minutos (tabla grande) → Ejecutar en ventana de mantenimiento

### Paso 4: Reescribir consulta con EXISTS

```sql
-- ✅ Reescribir con EXISTS en lugar de IN
EXPLAIN ANALYZE
SELECT p.id, p.contenido, p.fecha_creacion, u.nombre, u.foto_perfil
FROM publicaciones p
JOIN usuarios u ON p.usuario_id = u.id
WHERE EXISTS (
    SELECT 1
    FROM seguidores s
    WHERE s.seguidor_id = 12345
      AND s.seguido_id = p.usuario_id
)
ORDER BY p.fecha_creacion DESC
LIMIT 50;
```

**Resultado MEJORADO**:
```
Limit  (cost=0.56..850 rows=50) (actual time=0.05..45 rows=50 loops=1)
  -> Nested Loop  (cost=0.56..8500 rows=500000) (actual time=0.05..44 rows=50 loops=1)
       -> Index Scan Backward using idx_publicaciones_usuario_fecha on publicaciones p
            (cost=0.56..6500 rows=500000) (actual time=0.03..22 rows=50 loops=1)
            Filter: (EXISTS SubPlan)
            Rows Removed by Filter: 125
       -> Index Scan using usuarios_pkey on usuarios u
            (cost=0..0.5 rows=1) (actual time=0.01..0.01 rows=1 loops=50)
Planning Time: 2.1 ms
Execution Time: 48 ms  ✅ 0.048 segundos
```

**Mejoras observadas**:
- `Index Scan Backward`: Usa índice en orden descendente (perfecto para `ORDER BY DESC`)
- `Rows Removed by Filter: 125`: Solo lee 175 filas (antes: 200 millones) para devolver 50
- `Execution Time: 48 ms`: **385x más rápido** (18,512 ms → 48 ms) 🚀

### Paso 5: Optimización adicional - Tabla de feed pre-calculado

Para usuarios con muchos seguidores, pre-calcular el feed:

```sql
-- Tabla de feed materializado (se actualiza cada minuto)
CREATE TABLE feed_cache (
    usuario_id INT,
    publicacion_id INT,
    fecha_agregado TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (usuario_id, publicacion_id)
);

CREATE INDEX idx_feed_cache_usuario_fecha
ON feed_cache(usuario_id, fecha_agregado DESC);

-- Poblar con trigger o job cada minuto
INSERT INTO feed_cache (usuario_id, publicacion_id)
SELECT s.seguidor_id, p.id
FROM publicaciones p
JOIN seguidores s ON p.usuario_id = s.seguido_id
WHERE p.fecha_creacion >= NOW() - INTERVAL '1 minute';
```

**Consulta desde cache**:
```sql
SELECT p.id, p.contenido, p.fecha_creacion, u.nombre, u.foto_perfil
FROM feed_cache fc
JOIN publicaciones p ON fc.publicacion_id = p.id
JOIN usuarios u ON p.usuario_id = u.id
WHERE fc.usuario_id = 12345
ORDER BY fc.fecha_agregado DESC
LIMIT 50;
```

**Tiempo con cache**: <5 ms (960x más rápido que la versión optimizada)

### Resultado Final

| Versión | Tiempo | Mejora |
|---------|--------|--------|
| Original (sin índices) | 18,512 ms | Baseline |
| Con índices + EXISTS | 48 ms | 385x ✅ |
| Con feed cache | <5 ms | 3,702x 🚀 |

### Código Python para monitoreo

```python
from sqlalchemy import create_engine, text
import time

engine = create_engine("postgresql://user:password@localhost/socialhub_db")

def medir_query_feed(usuario_id: int):
    query = text("""
    SELECT p.id, p.contenido, p.fecha_creacion, u.nombre, u.foto_perfil
    FROM publicaciones p
    JOIN usuarios u ON p.usuario_id = u.id
    WHERE EXISTS (
        SELECT 1
        FROM seguidores s
        WHERE s.seguidor_id = :usuario_id
          AND s.seguido_id = p.usuario_id
    )
    ORDER BY p.fecha_creacion DESC
    LIMIT 50
    """)

    start = time.time()
    with engine.connect() as conn:
        result = conn.execute(query, {"usuario_id": usuario_id})
        rows = result.fetchall()
    end = time.time()

    tiempo_ms = (end - start) * 1000
    print(f"Usuario {usuario_id}: {tiempo_ms:.1f} ms ({len(rows)} publicaciones)")

    # Alertar si >100 ms
    if tiempo_ms > 100:
        print(f"⚠️ ALERTA: Query lenta para usuario {usuario_id}")

# Monitorear usuarios aleatorios cada minuto
medir_query_feed(12345)
# Output: Usuario 12345: 48.2 ms (50 publicaciones)
```

### Lecciones Aprendidas

**Para debugging en producción**:
1. **EXPLAIN ANALYZE es tu mejor amigo**: Muestra exactamente dónde está el problema
2. **Busca Seq Scans en tablas grandes**: Son el culpable #1
3. **Rows Removed by Filter >> Rows returned**: Señal de índice faltante
4. **EXISTS > IN**: Especialmente con subconsultas grandes
5. **Índices compuestos**: Pueden servir ORDER BY + filtro simultáneamente
6. **Considera caching**: Para consultas muy frecuentes, pre-calcular es válido

---

## Resumen de los 5 Ejemplos

| Ejemplo | Técnica Principal | Mejora |
|---------|-------------------|--------|
| 1. Primer Índice | Crear índice en columna filtrada | 48,275x |
| 2. JOINs Lentos | Índices en foreign keys + compuesto | 31.9x |
| 3. Índice Compuesto | Orden correcto de columnas | 51x |
| 4. Pipeline ETL | Evitar funciones, agregar en SQL | 225x |
| 5. Debugging Producción | EXISTS, índices, caching | 3,702x |

---

**¡Ahora practica con ejercicios reales en `03-EJERCICIOS.md`!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
