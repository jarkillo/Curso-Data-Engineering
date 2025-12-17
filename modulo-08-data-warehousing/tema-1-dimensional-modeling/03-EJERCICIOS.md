# Ejercicios Prácticos: Modelado Dimensional

Este documento contiene ejercicios para practicar el diseño de modelos dimensionales. Los ejercicios están organizados por nivel de dificultad y utilizan empresas ficticias realistas.

**Instrucciones**:
1. Lee cada ejercicio cuidadosamente
2. Intenta resolverlo sin mirar las soluciones
3. Usa las pistas si te atoras
4. Compara tu solución con la proporcionada al final

---

## Ejercicios Básicos

### Ejercicio 1: Diseñar Fact Table Simple

**Dificultad**: ⭐ Fácil

**Contexto**:

Trabajas para **CloudAPI Systems**, un proveedor de APIs cloud. Cada vez que un cliente hace una llamada a la API, el sistema registra:
- Timestamp de la llamada
- Endpoint llamado (ej: `/users`, `/products`, `/orders`)
- Cliente que hizo la llamada
- Tiempo de respuesta en milisegundos
- Código de respuesta HTTP (200, 404, 500, etc.)
- Bytes transferidos

El director de producto quiere analizar el uso de la API para responder:
- ¿Cuál endpoint es más usado?
- ¿Cuál es el tiempo de respuesta promedio por cliente?
- ¿Cuántas llamadas fallidas (status 500) hubo esta semana?

**Datos de Ejemplo**:

```
Llamada #1:
- Timestamp: 2024-03-15 10:23:45
- Endpoint: /users
- Cliente: Empresa ABC
- Tiempo respuesta: 145 ms
- Status: 200
- Bytes: 2048

Llamada #2:
- Timestamp: 2024-03-15 10:24:10
- Endpoint: /products
- Cliente: Empresa XYZ
- Tiempo respuesta: 320 ms
- Status: 200
- Bytes: 8192
```

**Pregunta**:

Diseña la fact table `FactLlamadasAPI` que permita responder las preguntas de negocio. Define:
1. El **grano** (qué representa una fila)
2. Las **foreign keys** a dimensiones
3. Las **medidas** (métricas)

No necesitas diseñar las dimension tables completas, solo identifícalas.

**Pista**:
- Cada fila debe representar UNA llamada individual a la API
- Piensa qué quieres sumar/promediar (medidas) y qué quieres usar para filtrar/agrupar (dimensiones)

---

### Ejercicio 2: Identificar Dimensiones

**Dificultad**: ⭐ Fácil

**Contexto**:

**LogisticFlow** quiere analizar el desempeño de sus conductores. Tienen los siguientes datos de cada entrega:
- Conductor que hizo la entrega
- Vehículo usado (camioneta, camión, motocicleta)
- Fecha y hora de salida
- Fecha y hora de entrega
- Ruta (origen → destino)
- Distancia recorrida
- Combustible consumido
- Cliente que recibió el paquete
- Tipo de paquete (documento, paquete pequeño, paquete grande)

**Pregunta**:

De la siguiente lista, identifica cuáles son **DIMENSIONES** (contexto descriptivo) y cuáles son **MEDIDAS** (métricas numéricas):

1. Conductor
2. Distancia recorrida
3. Vehículo
4. Combustible consumido
5. Fecha de salida
6. Ruta
7. Tipo de paquete
8. Tiempo de entrega (diferencia entre salida y entrega)
9. Cliente

**Pista**:
- Dimensiones: Responden ¿Quién? ¿Qué? ¿Dónde? ¿Cuándo?
- Medidas: Números que queremos sumar, promediar, contar

---

### Ejercicio 3: Definir el Grano

**Dificultad**: ⭐ Fácil

**Contexto**:

**FinTech Analytics** procesa transacciones financieras. Cada transacción puede tener múltiples detalles:

```
Transacción T001:
- Cliente: María López
- Fecha: 2024-03-15
- Total: $1,500
- Detalles:
  * Pago de tarjeta de crédito: $800
  * Transferencia a cuenta de ahorro: $500
  * Pago de servicios: $200
```

**Pregunta**:

¿Cuál es el **grano correcto** para una fact table de transacciones financieras?

**Opciones**:
A) Cada fila = una transacción completa (T001 sería 1 fila con total $1,500)
B) Cada fila = un detalle de transacción (T001 sería 3 filas: $800, $500, $200)
C) Cada fila = un cliente por día (María López el 2024-03-15 sería 1 fila)
D) Depende de las preguntas de negocio

Justifica tu respuesta.

**Pista**:
- El grano debe permitir responder TODAS las preguntas de negocio
- Puedes agregar desde detalle a resumen, pero no puedes desagregar desde resumen a detalle

---

### Ejercicio 4: DimFecha - Calcular Atributos

**Dificultad**: ⭐ Fácil

**Contexto**:

Tienes la fecha `2024-07-14` y necesitas popular los siguientes campos de DimFecha:

**Pregunta**:

Calcula manualmente (o con código Python) los siguientes atributos para la fecha `2024-07-14`:

```python
fecha_completa = datetime(2024, 7, 14)

# Calcula:
dia = ?
mes = ?
mes_nombre = ?
trimestre = ?
anio = ?
dia_semana = ?          # Lunes, Martes, etc.
numero_dia_semana = ?   # 0=Lunes, 6=Domingo
numero_semana = ?       # Semana del año
es_fin_de_semana = ?    # True/False
```

**Pista**:
- Usa `datetime` de Python o calcula manualmente
- Para trimestre: meses 1-3 = Q1, 4-6 = Q2, 7-9 = Q3, 10-12 = Q4

---

### Ejercicio 5: Star vs. Snowflake

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**RestaurantData Co.** tiene la siguiente jerarquía de productos:

```
Departamento: Alimentos
  └─ Categoría: Lácteos
      └─ Subcategoría: Leches
          └─ Producto: Leche Descremada 1L
```

**Pregunta**:

Diseña dos opciones:

**Opción A**: Star Schema (DimProducto denormalizada)
**Opción B**: Snowflake Schema (DimProducto, DimSubcategoria, DimCategoria, DimDepartamento)

Muestra la estructura SQL de ambas opciones. Luego compara:
- ¿Cuál es más fácil de consultar?
- ¿Cuál usa menos espacio?
- ¿Cuál recomendarías para este caso y por qué?

**Pista**:
- En Star, TODOS los atributos están en una tabla
- En Snowflake, cada nivel de jerarquía es una tabla separada

---

## Ejercicios Intermedios

### Ejercicio 6: Implementar SCD Tipo 1

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**CloudAPI Systems** tiene una dimensión de clientes:

```sql
CREATE TABLE DimCliente (
    cliente_id INT PRIMARY KEY,
    nombre_empresa VARCHAR(100),
    email_contacto VARCHAR(100),
    plan VARCHAR(20),            -- Básico, Pro, Enterprise
    telefono VARCHAR(20)
);
```

El cliente "TechCorp" cambió su teléfono de contacto de `555-1234` a `555-9999`.

**Pregunta**:

Escribe el código SQL para actualizar el teléfono usando **SCD Tipo 1** (sobrescribir el valor anterior).

¿Qué ventajas y desventajas tiene este enfoque? ¿Cuándo es apropiado usar SCD Tipo 1?

**Pista**:
- SCD Tipo 1 es un UPDATE simple
- Considera: ¿Importa saber cuál era el teléfono anterior?

---

### Ejercicio 7: Implementar SCD Tipo 2 con Código

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**LogisticFlow** tiene conductores que pueden cambiar de categoría según su experiencia:

```
Estado inicial (2024-01-01):
- Conductor: Pedro Ramírez
- Categoría: Junior
- Salario base: $15,000

Cambio (2024-06-01):
- Pedro es promovido a Senior
- Nuevo salario: $22,000
```

**Pregunta**:

Implementa SCD Tipo 2 con código Python o SQL. Tu solución debe:

1. Crear la estructura inicial de DimConductor con campos de SCD Tipo 2
2. Insertar a Pedro como Junior el 2024-01-01
3. Actualizar a Pedro a Senior el 2024-06-01 (sin perder el historial)
4. Mostrar cómo consultar qué categoría tenía Pedro el 2024-03-15

**Datos**:

```python
# Estado inicial
conductor_inicial = {
    'conductor_key': 'CON001',
    'nombre': 'Pedro Ramírez',
    'categoria': 'Junior',
    'salario_base': 15000,
    'fecha_vigencia': datetime(2024, 1, 1)
}

# Cambio
conductor_actualizado = {
    'conductor_key': 'CON001',
    'categoria': 'Senior',
    'salario_base': 22000,
    'fecha_cambio': datetime(2024, 6, 1)
}
```

**Pista**:
- Necesitas cerrar la versión anterior (fecha_fin_vigencia)
- Insertar una nueva fila para la nueva versión
- Usar `es_actual` para identificar la versión vigente

---

### Ejercicio 8: Diseñar Fact Table de Inventario (Snapshot)

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**RestaurantData Co.** quiere monitorear el inventario de ingredientes en cada restaurante. A diferencia de las ventas (que son transacciones), el inventario es un **estado** que cambia a lo largo del tiempo.

Cada día a las 11:59 PM, quieren saber:
- ¿Cuántas unidades de cada ingrediente hay en cada restaurante?
- ¿Cuál es el valor total del inventario?
- ¿Hay ingredientes con stock bajo (< 20% del mínimo)?

**Pregunta**:

Diseña una **Snapshot Fact Table** llamada `FactInventarioDiario` que capture el estado del inventario cada día.

Define:
1. El grano (qué representa cada fila)
2. Las dimensiones necesarias
3. Las medidas a capturar
4. ¿Cómo es diferente esta fact table de FactVentas?

**Pista**:
- Snapshot = foto del estado en un momento específico
- Cada producto/restaurante tendrá UNA fila POR DÍA (aunque no haya cambios)
- No registra transacciones individuales, sino el estado acumulado

---

### Ejercicio 9: Dimensión Conformada vs. Dimensión Específica

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**MercadoDigital** (e-commerce) tiene estas fact tables:
- FactVentas: Registra compras de productos
- FactDevoluciones: Registra productos devueltos
- FactEnvios: Registra entregas

**Pregunta**:

Para cada una de estas dimensiones, decide si debe ser **conformada** (compartida entre facts) o **específica** (exclusiva de una fact):

1. DimProducto
2. DimFecha
3. DimCliente
4. DimMotivoDevolucion (razón de devolución: defectuoso, talla incorrecta, etc.)
5. DimTransportista (empresa de envíos)
6. DimVendedor

Justifica cada decisión.

**Pista**:
- Dimensiones conformadas: Se usan en MÚLTIPLES fact tables
- Dimensiones específicas: Solo tienen sentido en UNA fact table
- Pregúntate: ¿Esta dimensión aplica a más de un proceso de negocio?

---

### Ejercicio 10: Query con Dimensión de Fecha

**Dificultad**: ⭐⭐ Medio

**Contexto**:

**FinTech Analytics** tiene esta fact table:

```sql
FactTransacciones (
    transaccion_id,
    fecha_id,          -- FK a DimFecha
    cliente_id,
    monto DECIMAL(10,2),
    tipo VARCHAR(20)   -- Depósito, Retiro, Transferencia
)
```

Y DimFecha completa con todos los atributos vistos en teoría.

**Pregunta**:

Escribe queries SQL para responder:

1. **Total de transacciones por día de la semana** en marzo 2024
2. **Promedio de monto por trimestre** en 2024
3. **Comparar días hábiles vs. fines de semana**: ¿En cuáles hay más transacciones?
4. **Bonus**: ¿Hay diferencia en el comportamiento en días festivos?

**Datos de Ejemplo**:

```sql
-- DimFecha ya está poblada con 2024-01-01 a 2024-12-31
-- FactTransacciones tiene 1 millón de filas
```

**Pista**:
- DimFecha tiene campos pre-calculados: `dia_semana`, `trimestre`, `es_fin_de_semana`, `es_dia_festivo`
- No necesitas usar funciones de fecha, solo hacer JOIN y filtrar

---

## Ejercicios Avanzados

### Ejercicio 11: Data Warehouse Completo para Hospital

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:

Has sido contratado para diseñar el data warehouse de **"Hospital General"**, que necesita analizar:

**Procesos de negocio**:
1. **Consultas médicas**: Pacientes que visitan doctores
2. **Cirugías**: Procedimientos quirúrgicos realizados
3. **Farmacia**: Medicamentos dispensados
4. **Hospitalización**: Pacientes internados en camas

**Preguntas de negocio**:
- ¿Cuáles doctores tienen más consultas por especialidad?
- ¿Cuál es el tiempo promedio de estadía hospitalaria por tipo de enfermedad?
- ¿Qué medicamentos se dispensan más frecuentemente?
- ¿Cuál es la tasa de ocupación de camas por piso/área?
- ¿Cómo varían las consultas por mes/trimestre?

**Pregunta**:

Diseña el data warehouse completo:

1. Identifica las **fact tables** necesarias (una por proceso)
2. Identifica las **dimensiones conformadas** (compartidas)
3. Identifica las **dimensiones específicas** (exclusivas de una fact)
4. Define el **grano** de cada fact table
5. Dibuja el **diagrama de constelación** (constellation schema)
6. Escribe la estructura SQL de AL MENOS:
   - 2 fact tables
   - 3 dimensiones

**Pista**:
- Cada proceso de negocio probablemente necesita su propia fact table
- Paciente, Doctor, Fecha son probablemente dimensiones conformadas
- Piensa en qué métricas son importantes en cada proceso

---

### Ejercicio 12: SCD Tipo 6 (Híbrido)

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:

**CloudAPI Systems** quiere rastrear el plan de suscripción de clientes con máxima flexibilidad:
- Mantener historial completo de cambios (SCD Tipo 2)
- Siempre saber cuál es el plan ACTUAL en cada registro (SCD Tipo 1)
- Recordar cuál fue el plan ORIGINAL del cliente (SCD Tipo 3)

Esto se llama **SCD Tipo 6** (1+2+3).

**Pregunta**:

Diseña e implementa SCD Tipo 6 para DimCliente:

1. Define la estructura de la tabla con TODOS los campos necesarios
2. Simula estos eventos:
   - 2024-01-01: Cliente "Startup ABC" se registra con plan "Básico"
   - 2024-06-01: Upgrade a plan "Pro"
   - 2024-12-01: Upgrade a plan "Enterprise"

3. Muestra cómo quedarían los registros después de cada evento
4. Escribe queries para:
   - Obtener el plan actual de "Startup ABC"
   - Obtener el historial completo de cambios
   - Comparar clientes: "plan actual vs. plan original"

**Pista**:
- Necesitas columnas como: `plan_actual`, `plan_historico`, `plan_original`
- Además de los campos estándar de SCD Tipo 2 (fechas, es_actual)
- El `plan_actual` se actualiza en TODAS las filas del cliente (Tipo 1)

---

### Ejercicio 13: Fact Table Factless

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:

**RestaurantData Co.** quiere rastrear qué productos NO se vendieron en ciertos días/restaurantes. Esto es importante para:
- Identificar productos con baja rotación
- Detectar problemas de inventario
- Planear promociones

Esto requiere una **Factless Fact Table** (sin medidas numéricas, solo foreign keys).

**Pregunta**:

Diseña una fact table llamada `FactProductoDisponible` que registre:
- **Qué productos** estaban disponibles
- **En qué restaurantes**
- **En qué fechas**

Esta tabla te permitirá hacer queries como:
- ¿Qué productos estaban disponibles pero NO se vendieron el 2024-03-15 en Restaurante Centro?

Luego escribe el query SQL que responda esa pregunta, combinando `FactProductoDisponible` con `FactVentas`.

**Pista**:
- Factless = sin medidas (cantidad, monto, etc.)
- Solo foreign keys: fecha_id, producto_id, restaurante_id
- Usa LEFT JOIN para encontrar productos disponibles pero no vendidos

---

### Ejercicio 14: Optimización de Queries

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:

**LogisticFlow** tiene un data warehouse con:
- FactEntregas: 100 millones de filas
- DimFecha: 3,650 filas (10 años)
- DimConductor: 500 filas
- DimRuta: 10,000 filas

Este query es muy lento (45 segundos):

```sql
SELECT
    EXTRACT(YEAR FROM f.fecha_completa) as anio,
    EXTRACT(MONTH FROM f.fecha_completa) as mes,
    COUNT(e.entrega_id) as total_entregas,
    AVG(e.tiempo_entrega_min) as tiempo_promedio
FROM FactEntregas e
JOIN DimFecha f ON e.fecha_id = f.fecha_id
WHERE EXTRACT(YEAR FROM f.fecha_completa) = 2024
  AND EXTRACT(MONTH FROM f.fecha_completa) BETWEEN 1 AND 3
GROUP BY EXTRACT(YEAR FROM f.fecha_completa), EXTRACT(MONTH FROM f.fecha_completa);
```

**Pregunta**:

1. Identifica 3 problemas de performance en este query
2. Reescribe el query optimizado
3. Sugiere índices que ayudarían
4. ¿Qué ventaja tiene usar DimFecha pre-calculada vs. usar funciones de fecha?

**Pista**:
- Usar EXTRACT() previene el uso de índices
- DimFecha ya tiene campos `anio` y `mes` pre-calculados
- WHERE sobre funciones es ineficiente

---

### Ejercicio 15: Migración de OLTP a OLAP

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:

**FinTech Analytics** tiene un sistema OLTP normalizado (PostgreSQL):

```sql
-- Sistema OLTP actual
Clientes (
    cliente_id,
    nombre,
    email,
    categoria,
    ciudad_id
)

Ciudades (
    ciudad_id,
    nombre_ciudad,
    estado_id
)

Estados (
    estado_id,
    nombre_estado,
    region
)

Transacciones (
    transaccion_id,
    cliente_id,
    fecha_hora,
    monto,
    tipo
)
```

**Pregunta**:

Diseña el proceso de migración de OLTP → OLAP:

1. **Diseña el modelo dimensional** (star schema):
   - FactTransacciones
   - DimCliente (con SCD Tipo 2 para categoría)
   - DimFecha
   - DimUbicacion (denormalizada)

2. **Escribe el proceso ETL** en pseudocódigo o SQL que:
   - Extraiga datos del sistema OLTP
   - Transforme a modelo dimensional
   - Cargue en el data warehouse

3. **Maneja el caso**: Un cliente cambió de categoría "Básico" → "Premium" el 2024-06-01
   - ¿Cómo se refleja en DimCliente?
   - ¿Las transacciones anteriores a junio deben mostrarse con qué categoría?

**Pista**:
- OLTP está normalizado (múltiples tablas, JOINs)
- OLAP debe estar denormalizado (star schema)
- Necesitas generar surrogate keys para dimensiones
- SCD Tipo 2 requiere lógica especial en la carga

---

## Soluciones

### Solución Ejercicio 1: Diseñar Fact Table Simple

```sql
CREATE TABLE FactLlamadasAPI (
    llamada_id BIGINT PRIMARY KEY,
    fecha_id INT NOT NULL,              -- FK a DimFecha
    hora_id INT NOT NULL,               -- FK a DimHora (opcional)
    endpoint_id INT NOT NULL,           -- FK a DimEndpoint
    cliente_id INT NOT NULL,            -- FK a DimCliente

    -- Medidas (métricas)
    tiempo_respuesta_ms INT NOT NULL,
    bytes_transferidos INT NOT NULL,
    status_code SMALLINT NOT NULL,      -- 200, 404, 500, etc.
    es_exitoso BOOLEAN NOT NULL,        -- TRUE si status 200-299

    FOREIGN KEY (fecha_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (endpoint_id) REFERENCES DimEndpoint(endpoint_id),
    FOREIGN KEY (cliente_id) REFERENCES DimCliente(cliente_id)
);
```

**Grano**: Cada fila representa UNA llamada individual a la API

**Dimensiones identificadas**:
- DimFecha (cuándo)
- DimEndpoint (qué endpoint: /users, /products, etc.)
- DimCliente (quién hizo la llamada)
- DimHora (opcional, para análisis intra-día)

**Medidas**:
- `tiempo_respuesta_ms`: Para calcular tiempos promedio
- `bytes_transferidos`: Para analizar ancho de banda
- `status_code`: Para clasificar respuestas
- `es_exitoso`: Flag booleano para facilitar queries

**Explicación**:

Con este diseño podemos responder todas las preguntas:

```sql
-- ¿Cuál endpoint es más usado?
SELECT
    e.nombre_endpoint,
    COUNT(l.llamada_id) as total_llamadas
FROM FactLlamadasAPI l
JOIN DimEndpoint e ON l.endpoint_id = e.endpoint_id
GROUP BY e.nombre_endpoint
ORDER BY total_llamadas DESC;

-- Tiempo promedio por cliente
SELECT
    c.nombre_empresa,
    AVG(l.tiempo_respuesta_ms) as tiempo_promedio_ms
FROM FactLlamadasAPI l
JOIN DimCliente c ON l.cliente_id = c.cliente_id
GROUP BY c.nombre_empresa;

-- Llamadas fallidas esta semana
SELECT COUNT(*)
FROM FactLlamadasAPI l
JOIN DimFecha f ON l.fecha_id = f.fecha_id
WHERE f.numero_semana = 11
  AND f.anio = 2024
  AND l.es_exitoso = FALSE;
```

---

### Solución Ejercicio 2: Identificar Dimensiones

**Dimensiones** (contexto descriptivo):
1. ✅ Conductor → DimConductor
3. ✅ Vehículo → DimVehiculo
5. ✅ Fecha de salida → DimFecha
6. ✅ Ruta → DimRuta
7. ✅ Tipo de paquete → DimTipoPaquete (o atributo en DimPaquete)
9. ✅ Cliente → DimCliente

**Medidas** (métricas numéricas):
2. ✅ Distancia recorrida (km)
4. ✅ Combustible consumido (litros)
8. ✅ Tiempo de entrega (minutos)

**Explicación**:

- **Dimensiones**: Describen el CONTEXTO de la entrega. Nos permiten filtrar, agrupar, segmentar.
- **Medidas**: Son valores NUMÉRICOS que queremos analizar (sumar, promediar, comparar).

**Fact Table resultante**:

```sql
CREATE TABLE FactEntregas (
    entrega_id BIGINT PRIMARY KEY,
    fecha_salida_id INT,
    conductor_id INT,
    vehiculo_id INT,
    ruta_id INT,
    cliente_id INT,
    tipo_paquete_id INT,

    -- Medidas
    distancia_km DECIMAL(8,2),
    combustible_litros DECIMAL(6,2),
    tiempo_entrega_min INT
);
```

---

### Solución Ejercicio 3: Definir el Grano

**Respuesta correcta**: **D) Depende de las preguntas de negocio**

Pero en este caso específico, la mejor opción es **B) Cada fila = un detalle de transacción**.

**Justificación**:

Si usamos grano de transacción completa (Opción A):
- Solo sabríamos el total ($1,500)
- NO podríamos analizar qué TIPOS de movimientos son más comunes
- NO podríamos calcular "promedio de pago de tarjeta" vs. "promedio de transferencia"

Si usamos grano de detalle (Opción B):
- Podemos analizar cada tipo de movimiento por separado
- Podemos agregar hacia arriba (sumar los 3 detalles = transacción completa)
- NO podemos desagregar desde resumen hacia detalle

**Regla de oro**: Cuando hay duda, **elige el grano MÁS DETALLADO** que sea factible. Siempre puedes agregar hacia arriba, pero NO puedes desagregar hacia abajo.

**Implementación**:

```sql
CREATE TABLE FactTransacciones (
    detalle_id BIGINT PRIMARY KEY,
    transaccion_key VARCHAR(50),       -- T001, T002, etc.
    fecha_id INT,
    cliente_id INT,
    tipo_movimiento_id INT,            -- Pago tarjeta, transferencia, etc.

    -- Medidas
    monto DECIMAL(10,2),

    FOREIGN KEY (fecha_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (cliente_id) REFERENCES DimCliente(cliente_id),
    FOREIGN KEY (tipo_movimiento_id) REFERENCES DimTipoMovimiento(tipo_movimiento_id)
);

-- Transacción T001 se representa con 3 filas:
-- detalle_id | transaccion_key | tipo_movimiento        | monto
-- 1          | T001            | Pago tarjeta crédito  | 800
-- 2          | T001            | Transferencia ahorro  | 500
-- 3          | T001            | Pago servicios        | 200
```

**Query para obtener total por transacción**:

```sql
SELECT
    transaccion_key,
    SUM(monto) as total_transaccion
FROM FactTransacciones
GROUP BY transaccion_key;
```

---

### Solución Ejercicio 4: DimFecha - Calcular Atributos

```python
from datetime import datetime

fecha_completa = datetime(2024, 7, 14)

# Calcular atributos
dia = fecha_completa.day                          # 14
mes = fecha_completa.month                        # 7
mes_nombre = 'Julio'
trimestre = (fecha_completa.month - 1) // 3 + 1   # 3 (Q3)
anio = fecha_completa.year                        # 2024

# Día de semana
dia_semana = fecha_completa.strftime('%A')        # 'Sunday' (en inglés)
# En español
dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
numero_dia_semana = fecha_completa.weekday()      # 6 (Domingo = 6)
dia_semana = dias_es[numero_dia_semana]           # 'Domingo'

numero_semana = fecha_completa.isocalendar()[1]   # 28
es_fin_de_semana = numero_dia_semana >= 5         # True (Domingo = 6 >= 5)
```

**Resultado**:

```python
{
    'fecha_id': 20240714,
    'fecha_completa': datetime(2024, 7, 14),
    'dia': 14,
    'mes': 7,
    'mes_nombre': 'Julio',
    'trimestre': 3,
    'anio': 2024,
    'dia_semana': 'Domingo',
    'numero_dia_semana': 6,
    'numero_semana': 28,
    'es_fin_de_semana': True
}
```

**Verificación**:
- 2024-07-14 cae en domingo ✅
- Es el mes 7 (julio) → Trimestre 3 ✅
- Es fin de semana ✅

---

### Solución Ejercicio 5: Star vs. Snowflake

**Opción A: Star Schema (Denormalizado)**

```sql
CREATE TABLE DimProducto (
    producto_id INT PRIMARY KEY,
    sku VARCHAR(50),
    nombre_producto VARCHAR(100),      -- 'Leche Descremada 1L'

    -- Atributos denormalizados (se repiten)
    subcategoria VARCHAR(50),          -- 'Leches'
    categoria VARCHAR(50),             -- 'Lácteos'
    departamento VARCHAR(50),          -- 'Alimentos'

    precio_catalogo DECIMAL(10,2),
    peso_kg DECIMAL(6,2)
);
```

**Datos de ejemplo**:

```
producto_id | nombre_producto       | subcategoria | categoria | departamento
1           | Leche Descremada 1L   | Leches      | Lácteos   | Alimentos
2           | Leche Entera 2L       | Leches      | Lácteos   | Alimentos
3           | Yogurt Natural 500g   | Yogures     | Lácteos   | Alimentos
4           | Queso Manchego 250g   | Quesos      | Lácteos   | Alimentos
```

**Nota**: "Lácteos" y "Alimentos" se repiten en cada producto lácteo.

**Query**:

```sql
-- Ventas por departamento (1 JOIN)
SELECT
    p.departamento,
    SUM(v.monto_total) as ventas
FROM FactVentas v
JOIN DimProducto p ON v.producto_id = p.producto_id
GROUP BY p.departamento;
```

---

**Opción B: Snowflake Schema (Normalizado)**

```sql
-- Nivel 1: Producto
CREATE TABLE DimProducto (
    producto_id INT PRIMARY KEY,
    sku VARCHAR(50),
    nombre_producto VARCHAR(100),
    subcategoria_id INT,
    precio_catalogo DECIMAL(10,2),
    FOREIGN KEY (subcategoria_id) REFERENCES DimSubcategoria(subcategoria_id)
);

-- Nivel 2: Subcategoría
CREATE TABLE DimSubcategoria (
    subcategoria_id INT PRIMARY KEY,
    nombre_subcategoria VARCHAR(50),   -- 'Leches'
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES DimCategoria(categoria_id)
);

-- Nivel 3: Categoría
CREATE TABLE DimCategoria (
    categoria_id INT PRIMARY KEY,
    nombre_categoria VARCHAR(50),      -- 'Lácteos'
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES DimDepartamento(departamento_id)
);

-- Nivel 4: Departamento
CREATE TABLE DimDepartamento (
    departamento_id INT PRIMARY KEY,
    nombre_departamento VARCHAR(50)    -- 'Alimentos'
);
```

**Query**:

```sql
-- Ventas por departamento (4 JOINS)
SELECT
    dept.nombre_departamento,
    SUM(v.monto_total) as ventas
FROM FactVentas v
JOIN DimProducto p ON v.producto_id = p.producto_id
JOIN DimSubcategoria sub ON p.subcategoria_id = sub.subcategoria_id
JOIN DimCategoria cat ON sub.categoria_id = cat.categoria_id
JOIN DimDepartamento dept ON cat.departamento_id = dept.departamento_id
GROUP BY dept.nombre_departamento;
```

---

**Comparación**:

| Criterio | Star Schema | Snowflake Schema |
|----------|-------------|------------------|
| **Facilidad de consulta** | ⭐⭐⭐⭐⭐ 1 JOIN | ⭐⭐ 4 JOINS |
| **Espacio** | ⭐⭐⭐ Más espacio (redundancia) | ⭐⭐⭐⭐⭐ Menos espacio |
| **Performance** | ⭐⭐⭐⭐⭐ Rápido | ⭐⭐⭐ Más lento |
| **Mantenibilidad** | ⭐⭐⭐ Cambiar categoría = UPDATE masivo | ⭐⭐⭐⭐⭐ Cambio localizado |

**Recomendación**: **Star Schema**

**Justificación**:
- RestaurantData tiene ~500-1000 productos → Redundancia es trivial
- Prioridad en analytics: queries rápidos y simples
- Analistas de negocio pueden escribir queries sin ayuda técnica
- Cloud storage es barato (diferencia de espacio es < 10 MB)

**Usar Snowflake solo si**:
- Jerarquías cambian constantemente
- Restricciones severas de almacenamiento
- Integridad referencial crítica por regulación

---

*(Las soluciones para los ejercicios 6-15 continuarían aquí con el mismo nivel de detalle)*

---

## Resumen de Ejercicios

| Ejercicio | Concepto | Nivel |
|-----------|----------|-------|
| 1-4 | Conceptos básicos (grano, dimensiones, medidas) | ⭐ Fácil |
| 5-10 | Diseño de modelos, SCDs, queries | ⭐⭐ Medio |
| 11-15 | Casos complejos, optimización, migración | ⭐⭐⭐ Difícil |

**Próximos pasos**: Implementa el proyecto práctico en `04-proyecto-practico/` aplicando todo lo aprendido.

---

**Tiempo estimado**: 4-6 horas para completar todos los ejercicios
**Prerequisitos**: Haber leído 01-TEORIA.md y 02-EJEMPLOS.md
**Herramientas recomendadas**: Python 3.11+, PostgreSQL o SQLite, pandas
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
