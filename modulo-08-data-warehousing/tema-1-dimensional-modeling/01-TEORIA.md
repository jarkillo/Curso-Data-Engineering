# Modelado Dimensional: Diseñando Data Warehouses para Analytics

## Introducción

### ¿Por qué es importante el modelado dimensional?

Imagina que eres el data engineer de una gran cadena de supermercados con 500 tiendas en todo el país. Cada día se procesan millones de transacciones: ventas, devoluciones, inventario, promociones. Tu CEO te llama un lunes por la mañana y te pregunta:

- "¿Cuáles fueron nuestras ventas totales el mes pasado por categoría de producto?"
- "¿Qué tiendas tuvieron mejor desempeño en la región norte?"
- "¿Cómo impactó la promoción de descuento del 20% en lácteos?"

Si tus datos están guardados tal cual los generan los sistemas transaccionales (bases de datos normalizadas), responder estas preguntas requeriría hacer **joins complejos entre decenas de tablas**, queries que tardarían minutos u horas, y un código difícil de mantener.

**El modelado dimensional resuelve exactamente este problema**: organiza los datos de forma que sean fáciles y rápidos de consultar para análisis de negocio, sin sacrificar la integridad de la información.

### Contexto en Data Engineering

En el mundo del Data Engineering, trabajamos con dos tipos principales de sistemas:

1. **Sistemas OLTP (Online Transaction Processing)**: Sistemas operacionales como tu aplicación de ventas, sistema de inventario, CRM. Están optimizados para muchas transacciones pequeñas y rápidas (INSERT, UPDATE, DELETE).

2. **Sistemas OLAP (Online Analytical Processing)**: Data warehouses y data marts diseñados para consultas analíticas complejas que leen grandes volúmenes de datos para generar reportes, dashboards y análisis.

**El modelado dimensional es la técnica estándar para diseñar sistemas OLAP**.

### Analogía: La Biblioteca vs. El Archivo Histórico

Piensa en la diferencia entre:

- **Una biblioteca pública** (sistema transaccional/OLTP): Organizada para que muchas personas puedan buscar, prestar y devolver libros rápidamente. Los libros están categorizados por autor, género, ISBN. Todo está normalizado para evitar duplicación.

- **Un archivo histórico de investigación** (data warehouse/OLAP): Organizado para que investigadores puedan analizar patrones a lo largo del tiempo. Los documentos están agrupados por época, tema, región. Se permite cierta redundancia si facilita la búsqueda. Hay índices cruzados que permiten responder preguntas complejas rápidamente.

**El modelado dimensional es el arte de organizar tu "archivo histórico" de datos para que analistas e investigadores (data analysts, data scientists, ejecutivos) encuentren respuestas rápidamente**.

---

## Conceptos Fundamentales

### Concepto 1: Fact Tables (Tablas de Hechos)

**Definición Simple**: Una fact table es una tabla que contiene **medidas cuantitativas** (números que queremos analizar) sobre **eventos de negocio** que ocurrieron.

**Analogía del Mundo Real**:

Imagina el ticket de compra de un supermercado. Cada línea del ticket representa un "hecho" (fact):
- Compraste 2 litros de leche por $5.00
- Compraste 1 kilo de arroz por $3.50
- Compraste 3 manzanas por $2.00

Cada una de estas líneas es un **hecho** que contiene:
- **Medidas** (lo que queremos sumar/promediar): cantidad vendida, monto total, descuento aplicado
- **Referencias** a dimensiones (contexto): ¿qué producto? ¿qué tienda? ¿qué fecha? ¿qué cliente?

**Ejemplo Visual (Fact Table de Ventas)**:

```
FactVentas
├── venta_id (PK)
├── fecha_id (FK → DimFecha)
├── producto_id (FK → DimProducto)
├── tienda_id (FK → DimTienda)
├── cliente_id (FK → DimCliente)
├── cantidad_vendida (MEASURE)
├── monto_venta (MEASURE)
├── costo (MEASURE)
└── descuento (MEASURE)
```

**Por qué lo usamos en Data Engineering**:

1. **Granularidad clara**: Cada fila representa UN evento de negocio al nivel de detalle más fino posible (ej: una línea de venta).
2. **Métricas calculables**: Podemos sumar ventas, promediar cantidades, calcular márgenes.
3. **Optimización de queries**: Las fact tables contienen principalmente números y foreign keys (muy eficiente para agregaciones).
4. **Escalabilidad**: Las fact tables pueden crecer a billones de filas y seguir siendo consultables con buena performance.

**Características clave de una Fact Table**:
- **Gran volumen**: Contiene la mayoría de las filas del data warehouse (70-90% del total).
- **Foreign keys a dimensiones**: Se conecta con dimension tables a través de claves foráneas.
- **Medidas aditivas**: Idealmente, las métricas se pueden sumar a través de cualquier dimensión (ventas, cantidad, etc.).
- **Grano definido**: Cada fila representa exactamente un nivel de detalle (ej: "una línea de venta en un ticket").

---

### Concepto 2: Dimension Tables (Tablas de Dimensiones)

**Definición Simple**: Una dimension table contiene **atributos descriptivos** que dan **contexto** a los hechos. Responden a las preguntas: ¿Quién? ¿Qué? ¿Dónde? ¿Cuándo?

**Analogía del Mundo Real**:

Volviendo al ejemplo del ticket del supermercado, cuando el ticket dice "2 litros de leche", necesitas más información para entender el contexto:
- **¿Qué leche?**: Marca Lala, leche descremada, presentación de 2 litros, categoría lácteos
- **¿Dónde?**: Tienda "Supermercado Centro", ubicada en Av. Principal #123, ciudad: CDMX, región: Centro
- **¿Cuándo?**: 15 de marzo de 2024, viernes, semana 11, trimestre 1, temporada: no festivo
- **¿Quién?**: Cliente #12345, María González, segmento: cliente frecuente, edad: 35-44

Toda esta información descriptiva vive en **dimension tables**.

**Ejemplo Visual (Dimension de Producto)**:

```
DimProducto
├── producto_id (PK)
├── nombre_producto
├── marca
├── categoria
├── subcategoria
├── proveedor
├── precio_sugerido
├── peso_unitario
├── unidad_medida
├── es_perecedero
└── fecha_alta_catalogo
```

**Por qué lo usamos en Data Engineering**:

1. **Contexto de negocio**: Las dimensiones dan significado a los números de la fact table.
2. **Capacidad de filtrado**: Permiten segmentar análisis ("ventas solo de la categoría lácteos").
3. **Agrupamiento y drill-down**: Permiten analizar datos a diferentes niveles (por marca → categoría → departamento).
4. **Información descriptiva rica**: Pueden tener muchas columnas descriptivas sin afectar performance.

**Características clave de una Dimension Table**:
- **Bajo volumen relativo**: Menos filas que las fact tables (decenas de miles vs. millones/billones).
- **Muchas columnas**: Contienen atributos descriptivos, texto, categorías.
- **Denormalizadas**: A diferencia de sistemas transaccionales, aquí aceptamos redundancia para facilitar consultas.
- **Cambios lentos**: Generalmente cambian poco y de forma controlada (SCD, que veremos más adelante).

---

### Concepto 3: Star Schema (Esquema de Estrella)

**Definición Simple**: El star schema es un diseño donde una fact table central está rodeada de dimension tables, formando visualmente una estrella.

**Analogía del Mundo Real**:

Imagina el sistema solar:
- **El Sol** (fact table): El centro con toda la energía (los hechos/medidas)
- **Los planetas** (dimension tables): Giran alrededor del sol, cada uno con sus características propias

Cuando quieres analizar algo (ej: "ventas totales por región"), empiezas en el centro (fact table) y te conectas directamente con la dimensión que necesitas (DimTienda que contiene región). **Un solo join, directo y simple**.

**Diagrama Conceptual**:

```
         DimFecha
             │
             │
DimCliente ─┼─ FactVentas ─┼─ DimProducto
             │
             │
         DimTienda
```

**Ejemplo Concreto**:

```sql
-- Query simple en Star Schema: Ventas totales por categoría de producto
SELECT
    p.categoria,
    SUM(v.monto_venta) as ventas_totales,
    SUM(v.cantidad_vendida) as unidades_vendidas
FROM FactVentas v
INNER JOIN DimProducto p ON v.producto_id = p.producto_id
GROUP BY p.categoria
ORDER BY ventas_totales DESC;
```

**¡Solo UN join!** Esto es extremadamente rápido incluso con millones de filas.

**Por qué lo usamos en Data Engineering**:

1. **Queries simples y rápidos**: Menos joins = mejor performance.
2. **Fácil de entender**: Analistas de negocio pueden navegar el modelo sin ser expertos en SQL.
3. **Optimizable**: Los motores de bases de datos pueden optimizar estas estructuras agresivamente.
4. **Mantenimiento sencillo**: Agregar nuevas dimensiones o métricas es directo.

**Ventajas del Star Schema**:
- Performance excelente para queries analíticos
- Simplicidad conceptual
- Fácil de documentar y explicar a stakeholders
- Compatible con herramientas de BI (Power BI, Tableau, Looker)

**Desventajas del Star Schema**:
- Redundancia de datos en dimensiones (por diseño, aceptable)
- Uso de más espacio de almacenamiento que modelos normalizados
- Requiere procesos ETL para desnormalizar y cargar datos

---

### Concepto 4: Snowflake Schema (Esquema de Copo de Nieve)

**Definición Simple**: El snowflake schema es una variación del star schema donde las dimension tables están **normalizadas** (divididas en sub-tablas), formando ramificaciones como un copo de nieve.

**Analogía del Mundo Real**:

Imagina una empresa con estructura jerárquica:
- **CEO** (fact table)
- **Directores** (dimensiones nivel 1)
- **Gerentes** (dimensiones nivel 2)
- **Supervisores** (dimensiones nivel 3)
- **Empleados** (dimensiones nivel 4)

En el snowflake schema, en lugar de tener toda la información jerárquica en UNA tabla de dimensión, la divides en múltiples tablas relacionadas.

**Ejemplo Comparativo**:

**Star Schema (DimProducto denormalizada)**:
```
DimProducto
├── producto_id (PK)
├── nombre_producto
├── categoria          ← Repetido para cada producto
├── nombre_categoria   ← Repetido
├── departamento       ← Repetido
├── nombre_departamento ← Repetido
```

**Snowflake Schema (DimProducto normalizada)**:
```
DimProducto                  DimCategoria              DimDepartamento
├── producto_id (PK)         ├── categoria_id (PK)     ├── departamento_id (PK)
├── nombre_producto          ├── nombre_categoria      └── nombre_departamento
└── categoria_id (FK) ───────┤
                             └── departamento_id (FK) ──┘
```

**Query en Snowflake Schema**:

```sql
-- Ahora necesitamos 3 joins en lugar de 1
SELECT
    d.nombre_departamento,
    SUM(v.monto_venta) as ventas_totales
FROM FactVentas v
INNER JOIN DimProducto p ON v.producto_id = p.producto_id
INNER JOIN DimCategoria c ON p.categoria_id = c.categoria_id  -- Join extra
INNER JOIN DimDepartamento d ON c.departamento_id = d.departamento_id  -- Join extra
GROUP BY d.nombre_departamento;
```

**Por qué podríamos usarlo en Data Engineering**:

1. **Ahorro de espacio**: Reduce redundancia (importante si tienes millones de productos).
2. **Integridad referencial**: Más fácil mantener consistencia en jerarquías.
3. **Dimensiones muy grandes**: Cuando una dimensión tiene cientos de columnas y jerarquías complejas.

**Cuándo usar Star vs. Snowflake**:

| Criterio | Star Schema | Snowflake Schema |
|----------|-------------|------------------|
| Performance de queries | ⭐⭐⭐⭐⭐ Excelente | ⭐⭐⭐ Bueno |
| Simplicidad para analistas | ⭐⭐⭐⭐⭐ Muy simple | ⭐⭐ Complejo |
| Espacio de almacenamiento | ⭐⭐⭐ Usa más espacio | ⭐⭐⭐⭐⭐ Eficiente |
| Mantenibilidad | ⭐⭐⭐⭐ Fácil | ⭐⭐⭐ Moderado |
| Integridad referencial | ⭐⭐⭐ Aceptable | ⭐⭐⭐⭐⭐ Excelente |

**Recomendación en Data Engineering moderno**:
Con el almacenamiento barato en cloud (S3, Blob Storage) y motores columnares eficientes (Snowflake, BigQuery, Redshift), **star schema es casi siempre preferible** para data warehouses analíticos. Usa snowflake schema solo si tienes restricciones severas de almacenamiento o jerarquías extremadamente complejas.

---

### Concepto 5: Slowly Changing Dimensions (SCD) - Dimensiones de Cambio Lento

**Definición Simple**: SCD es la estrategia para manejar cambios en los atributos de las dimensiones a lo largo del tiempo, manteniendo (o no) el historial de cambios.

**Analogía del Mundo Real**:

Imagina el historial de un empleado en una empresa:
- **2020**: Juan Pérez, Analista Junior, Departamento de Ventas
- **2022**: Juan Pérez, Analista Senior, Departamento de Marketing (¡cambió de puesto!)
- **2024**: Juan Pérez García, Gerente de Marketing, Departamento de Marketing (¡cambió su nombre y fue promovido!)

**¿Cómo registras estos cambios?** Depende de las necesidades de negocio. Las SCD definen diferentes estrategias.

#### SCD Tipo 0: Sin cambios permitidos

**Concepto**: Los atributos NUNCA cambian. Si cambia, es un nuevo registro.

**Ejemplo**: Número de seguridad social, fecha de nacimiento.

```
DimPersona
├── persona_id (PK)
├── numero_seguro_social  ← NUNCA cambia
├── fecha_nacimiento      ← NUNCA cambia
```

**Cuándo usar**: Atributos inmutables por naturaleza o por regulación.

---

#### SCD Tipo 1: Sobrescribir

**Concepto**: Se sobrescribe el valor anterior, **NO se mantiene historial**.

**Ejemplo**: Corrección de errores tipográficos, actualización de teléfono.

```
-- ANTES
DimCliente
cliente_id | nombre         | telefono
1         | María Gonzalez | 5551234567

-- DESPUÉS (se sobrescribe)
DimCliente
cliente_id | nombre         | telefono
1         | María González | 5559876543
```

**Ventajas**:
- Simplicidad total
- No crece la tabla de dimensión
- Siempre tienes datos "actuales"

**Desventajas**:
- **Pierdes historial** (las ventas pasadas ahora muestran el teléfono nuevo)
- No puedes hacer análisis de "cómo era antes"

**Cuándo usar**:
- Corrección de errores de captura
- Atributos que no importan históricamente (teléfono, email)
- Atributos descriptivos que cambian raramente y no afectan análisis

---

#### SCD Tipo 2: Agregar nueva fila (versionado)

**Concepto**: Se crea una **nueva fila** para el cambio, manteniendo historial completo con fechas de vigencia.

**Ejemplo**: Cambio de categoría de cliente.

```
DimCliente
cliente_id | cliente_key | nombre  | categoria    | fecha_inicio | fecha_fin    | es_actual
1          | C001        | María   | Bronce      | 2020-01-01  | 2022-05-31  | 0
2          | C001        | María   | Plata       | 2022-06-01  | 2024-02-29  | 0
3          | C001        | María   | Oro         | 2024-03-01  | 9999-12-31  | 1
```

**Nota importante**:
- `cliente_id` es la clave primaria (surrogate key) única para cada fila
- `cliente_key` es la clave de negocio (natural key) que se repite
- `fecha_fin = 9999-12-31` indica que es la versión actual

**Ventajas**:
- **Historial completo** de cambios
- Análisis históricos precisos ("¿cómo se veían las ventas cuando el cliente era Bronce?")
- Auditoría total

**Desventajas**:
- Tabla crece con el tiempo
- Queries ligeramente más complejos (necesitas filtrar por `es_actual = 1`)
- Más espacio de almacenamiento

**Cuándo usar**:
- Atributos que cambian y **SÍ importa** el historial (categoría, región, segmento)
- Industrias reguladas que requieren auditoría
- Análisis de tendencias temporales

**Query ejemplo**:

```sql
-- Ventas actuales por categoría actual de cliente
SELECT
    c.categoria,
    SUM(v.monto_venta) as ventas_totales
FROM FactVentas v
INNER JOIN DimCliente c ON v.cliente_id = c.cliente_id
WHERE c.es_actual = 1  -- Solo versión actual
GROUP BY c.categoria;

-- Ventas históricas con categoría que tenía el cliente EN ESE MOMENTO
SELECT
    c.categoria,
    f.fecha,
    SUM(v.monto_venta) as ventas_totales
FROM FactVentas v
INNER JOIN DimCliente c ON v.cliente_id = c.cliente_id
INNER JOIN DimFecha f ON v.fecha_id = f.fecha_id
WHERE f.fecha BETWEEN c.fecha_inicio AND c.fecha_fin  -- Versión vigente en esa fecha
GROUP BY c.categoria, f.fecha;
```

---

#### SCD Tipo 3: Agregar nueva columna

**Concepto**: Se agrega una columna para el valor anterior, manteniendo **solo UNA versión histórica**.

**Ejemplo**: Cambio de región de una tienda.

```
DimTienda
tienda_id | nombre_tienda | region_actual | region_anterior
1         | Sucursal Centro | Norte      | Sur
```

**Ventajas**:
- Fácil de consultar
- No crece la tabla
- Tienes "antes y después"

**Desventajas**:
- Solo guardas 1 cambio histórico (no múltiples)
- Si hay más de 2 cambios, pierdes historial antiguo

**Cuándo usar**:
- Cambios muy raros
- Solo te interesa "antes vs. después" (no todo el historial)
- Comparaciones específicas (ej: reorganización territorial)

---

#### SCD Tipo 4: Tabla de historial separada

**Concepto**: Mantienes la tabla de dimensión actual pequeña, y creas una tabla de historial separada.

**Ejemplo**:

```
-- Tabla actual (solo versión vigente)
DimProducto_Actual
producto_id | nombre_producto | precio_actual

-- Tabla de historial (todos los cambios)
DimProducto_Historial
producto_id | nombre_producto | precio | fecha_inicio | fecha_fin
```

**Cuándo usar**:
- Dimensiones muy grandes con muchos cambios
- Separar queries de análisis actual (rápidos) vs. análisis histórico (menos frecuentes)

---

#### SCD Tipo 6: Híbrido (1+2+3)

**Concepto**: Combina Tipo 1 + Tipo 2 + Tipo 3 para tener flexibilidad total.

**Ejemplo**:

```
DimCliente
cliente_id | cliente_key | nombre | categoria_actual | categoria_original | categoria_historica | fecha_inicio | fecha_fin | es_actual
1          | C001        | María  | Oro             | Bronce            | Bronce             | 2020-01-01  | 2022-05-31 | 0
2          | C001        | María  | Oro             | Bronce            | Plata              | 2022-06-01  | 2024-02-29 | 0
3          | C001        | María  | Oro             | Bronce            | Oro                | 2024-03-01  | 9999-12-31 | 1
```

- `categoria_actual`: Siempre tiene el valor más reciente (Tipo 1)
- Múltiples filas con historial (Tipo 2)
- `categoria_original`: Mantiene el valor inicial (Tipo 3)

**Cuándo usar**: Casos muy específicos donde necesitas comparar "situación original vs. actual vs. histórica".

---

### Resumen de SCDs: ¿Cuál usar?

| Tipo | Mantiene historial | Complejidad | Uso típico |
|------|-------------------|-------------|------------|
| Tipo 0 | ❌ No | ⭐ Trivial | Atributos inmutables (SSN, fecha nacimiento) |
| Tipo 1 | ❌ No | ⭐ Trivial | Correcciones, datos no críticos (teléfono, email) |
| Tipo 2 | ✅ Sí (completo) | ⭐⭐⭐ Moderado | **Más común**: categorías, regiones, segmentos |
| Tipo 3 | ✅ Sí (limitado) | ⭐⭐ Fácil | Cambios raros, comparación antes/después |
| Tipo 4 | ✅ Sí (separado) | ⭐⭐⭐⭐ Complejo | Dimensiones grandes con muchos cambios |
| Tipo 6 | ✅ Sí (híbrido) | ⭐⭐⭐⭐⭐ Complejo | Casos muy específicos |

**Recomendación**: En la mayoría de proyectos de Data Engineering, **SCD Tipo 2** es la opción más común y versátil.

---

## Aplicaciones Prácticas

### Caso de Uso 1: Data Warehouse de E-commerce

**Contexto de Negocio**:
Eres data engineer en "MercadoLibre Digital", un e-commerce con 100,000 productos, 50,000 clientes activos y 10,000 ventas diarias.

**Problema a Resolver**:
El equipo de analytics necesita responder preguntas como:
- ¿Cuáles son los productos más vendidos por categoría en el último trimestre?
- ¿Cómo varían las ventas por día de la semana?
- ¿Qué clientes cambiaron de segmento "Básico" a "Premium" y cómo cambió su comportamiento de compra?

**Cómo ayuda el Modelado Dimensional**:

Diseñas un star schema:

```
FactVentas (grano: una línea de orden de compra)
├── venta_id (PK)
├── fecha_id (FK)
├── producto_id (FK)
├── cliente_id (FK)
├── vendedor_id (FK)
├── cantidad
├── precio_unitario
├── descuento
├── impuestos
└── monto_total

DimFecha
├── fecha_id (PK)
├── fecha_completa
├── dia_semana
├── mes
├── trimestre
├── anio
├── es_fin_de_semana
└── es_dia_festivo

DimProducto
├── producto_id (PK)
├── sku
├── nombre_producto
├── marca
├── categoria
├── subcategoria
├── precio_catalogo
└── peso_kg

DimCliente (SCD Tipo 2)
├── cliente_id (PK)
├── cliente_key (natural key)
├── nombre_cliente
├── email
├── segmento (Básico/Premium/VIP)
├── fecha_registro
├── fecha_inicio_vigencia
├── fecha_fin_vigencia
└── es_actual

DimVendedor
├── vendedor_id (PK)
├── nombre_vendedor
├── region
└── tipo_vendedor
```

**Queries de Negocio Resueltas**:

```sql
-- 1. Top 10 productos más vendidos por categoría en Q1 2024
SELECT
    p.categoria,
    p.nombre_producto,
    SUM(v.cantidad) as unidades_vendidas,
    SUM(v.monto_total) as ingresos
FROM FactVentas v
JOIN DimProducto p ON v.producto_id = p.producto_id
JOIN DimFecha f ON v.fecha_id = f.fecha_id
WHERE f.trimestre = 1 AND f.anio = 2024
GROUP BY p.categoria, p.nombre_producto
ORDER BY ingresos DESC
LIMIT 10;

-- 2. Ventas por día de semana
SELECT
    f.dia_semana,
    COUNT(DISTINCT v.venta_id) as num_ventas,
    SUM(v.monto_total) as ingresos_totales,
    AVG(v.monto_total) as ticket_promedio
FROM FactVentas v
JOIN DimFecha f ON v.fecha_id = f.fecha_id
GROUP BY f.dia_semana
ORDER BY ingresos_totales DESC;

-- 3. Análisis de cambio de segmento de clientes (SCD Tipo 2)
WITH cambios_segmento AS (
    SELECT
        cliente_key,
        segmento AS segmento_anterior,
        LEAD(segmento) OVER (PARTITION BY cliente_key ORDER BY fecha_inicio_vigencia) AS segmento_nuevo
    FROM DimCliente
)
SELECT
    cs.segmento_anterior,
    cs.segmento_nuevo,
    COUNT(DISTINCT cs.cliente_key) as num_clientes_cambiaron
FROM cambios_segmento cs
WHERE cs.segmento_nuevo IS NOT NULL
GROUP BY cs.segmento_anterior, cs.segmento_nuevo;
```

**Resultado**: Queries que antes tardaban 2-3 minutos en OLTP ahora toman segundos. Analistas pueden crear dashboards sin depender de data engineers.

---

### Caso de Uso 2: Data Warehouse de Logística

**Contexto de Negocio**:
"EnvíoRápido Express" es una empresa de logística con 500 vehículos, 50 centros de distribución y 20,000 entregas diarias.

**Problema a Resolver**:
- ¿Cuál es el tiempo promedio de entrega por región?
- ¿Qué rutas son más eficientes?
- ¿Cómo afectan las condiciones climáticas los tiempos de entrega?
- Identificar conductores con mejor desempeño

**Modelado Dimensional Propuesto**:

```
FactEntregas (grano: una entrega individual)
├── entrega_id (PK)
├── fecha_salida_id (FK)
├── fecha_entrega_id (FK)
├── paquete_id (FK)
├── ruta_id (FK)
├── vehiculo_id (FK)
├── conductor_id (FK)
├── cliente_id (FK)
├── tiempo_entrega_minutos (MEASURE)
├── distancia_km (MEASURE)
├── costo_combustible (MEASURE)
└── fue_a_tiempo (0/1)

DimRuta
├── ruta_id (PK)
├── origen
├── destino
├── region
├── distancia_estimada_km
└── tipo_ruta (urbana/rural/interestatal)

DimConductor (SCD Tipo 2)
├── conductor_id (PK)
├── conductor_key
├── nombre
├── categoria (junior/senior/expert)
├── años_experiencia
├── fecha_inicio_vigencia
├── fecha_fin_vigencia
└── es_actual

DimClima
├── clima_id (PK)
├── fecha_id (FK)
├── region
├── condicion (soleado/lluvioso/nevado)
├── temperatura_c
└── visibilidad_km
```

**Insight de Negocio**:

```sql
-- Análisis de eficiencia: Conductores con mejor ratio de entregas a tiempo
SELECT
    c.nombre,
    c.categoria,
    COUNT(e.entrega_id) as total_entregas,
    SUM(e.fue_a_tiempo) as entregas_a_tiempo,
    ROUND(100.0 * SUM(e.fue_a_tiempo) / COUNT(e.entrega_id), 2) as porcentaje_exito,
    AVG(e.tiempo_entrega_minutos) as tiempo_promedio_min
FROM FactEntregas e
JOIN DimConductor c ON e.conductor_id = c.conductor_id
WHERE c.es_actual = 1
GROUP BY c.nombre, c.categoria
HAVING COUNT(e.entrega_id) > 100
ORDER BY porcentaje_exito DESC
LIMIT 10;
```

---

## Errores Comunes

### Error 1: Confundir OLTP con OLAP y normalizar el Data Warehouse

**Por qué ocurre**:
Muchos desarrolladores vienen de experiencia con bases de datos transaccionales (PostgreSQL, MySQL) donde la normalización (3NF, BCNF) es la práctica estándar para evitar redundancia y garantizar integridad.

**Ejemplo del error**:

En lugar de crear un star schema simple, crean un modelo súper-normalizado:

```
-- MAL: Modelo normalizado en DWH (complica queries)
FactVentas
├── venta_id
├── producto_id → DimProducto
│                 ├── categoria_id → DimCategoria
│                                    ├── departamento_id → DimDepartamento
```

Ahora necesitas 4 joins solo para agrupar por departamento.

**Cómo evitarlo**:
- **OLTP = Normalización** (evitar redundancia, optimizar escritura)
- **OLAP = Denormalización** (optimizar lectura, aceptar redundancia)
- En Data Warehouses, **duplicar datos es BUENO** si mejora performance de queries

**Solución correcta**: Star schema con dimensiones denormalizadas.

---

### Error 2: No definir claramente el GRANO de la Fact Table

**Por qué ocurre**:
No pensar detenidamente "¿qué representa exactamente UNA fila de mi fact table?" lleva a modelos confusos e inconsistentes.

**Ejemplo del error**:

Mezclar granularidades diferentes en la misma fact table:

```
FactVentas
venta_id | fecha_id | producto_id | cliente_id | monto
1        | 20240101 | 100         | 500        | 1000   ← Una venta individual
2        | 20240101 | NULL        | NULL       | 50000  ← Total del día (????)
```

Ahora tus sumas estarán mal porque mezclas niveles.

**Cómo evitarlo**:
1. **Definir grano explícitamente**: "Cada fila = una línea de ticket de compra"
2. **Ser consistente**: TODAS las filas deben ser del mismo nivel
3. Si necesitas agregados pre-calculados (totales diarios), crea OTRA fact table: `FactVentasDiarias`

---

### Error 3: Usar SCD Tipo 2 sin planear el crecimiento

**Por qué ocurre**:
Implementar SCD Tipo 2 en dimensiones que cambian constantemente sin considerar el impacto en tamaño.

**Ejemplo del error**:

DimProducto con SCD Tipo 2 donde el precio cambia diariamente:

```
DimProducto
producto_id | producto_key | nombre | precio | fecha_inicio | fecha_fin | es_actual
1           | P001         | Leche  | 10.00  | 2024-01-01  | 2024-01-01 | 0
2           | P001         | Leche  | 10.50  | 2024-01-02  | 2024-01-02 | 0
3           | P001         | Leche  | 10.25  | 2024-01-03  | 2024-01-03 | 0
...
365         | P001         | Leche  | 11.00  | 2024-12-31  | 9999-12-31 | 1
```

**1 producto con cambio diario = 365 filas al año**. Si tienes 100,000 productos = 36.5 millones de filas solo en la dimensión.

**Cómo evitarlo**:
- **Evaluar frecuencia de cambio**: Si cambia constantemente, quizás el atributo debería ser una métrica en la fact table, no una dimensión
- **Usar SCD Tipo 1** para atributos que cambian mucho y no requieren historial (precio actual)
- **Crear fact table de cambios** si necesitas historial de precios: `FactCambioPrecio`

---

### Error 4: Olvidar la DimFecha (Date Dimension)

**Por qué ocurre**:
Pensar "tengo un campo DATE en la fact table, ¿para qué necesito una dimensión?"

**Ejemplo del error**:

```
FactVentas
├── fecha (DATE)  ← Solo la fecha
```

Ahora para hacer análisis necesitas funciones complejas:

```sql
-- Complejo: sacar día de semana, trimestre, etc.
SELECT
    DAYOFWEEK(fecha) as dia,
    QUARTER(fecha) as trimestre,
    ...
```

**Cómo evitarlo**:
SIEMPRE crear DimFecha con atributos pre-calculados:

```
DimFecha
├── fecha_id (PK: 20240315)
├── fecha_completa (2024-03-15)
├── dia_mes (15)
├── mes (3)
├── nombre_mes ('Marzo')
├── trimestre (1)
├── anio (2024)
├── dia_semana ('Viernes')
├── numero_semana (11)
├── es_fin_de_semana (0)
├── es_dia_festivo (0)
└── nombre_festivo (NULL)
```

**Beneficio**: Queries se simplifican drásticamente y son más rápidos.

---

## Checklist de Aprendizaje

Antes de continuar al siguiente tema, verifica que puedas responder:

- [ ] **Entiendo qué es el modelado dimensional y por qué existe**
  - ¿Puedo explicar la diferencia entre OLTP y OLAP?
  - ¿Entiendo por qué no usamos normalización en data warehouses?

- [ ] **Puedo explicar fact tables con mis propias palabras**
  - ¿Sé qué son las "medidas" (measures)?
  - ¿Entiendo qué significa "grano" (grain) de una fact table?
  - ¿Puedo dar ejemplos de fact tables de diferentes industrias?

- [ ] **Puedo explicar dimension tables con mis propias palabras**
  - ¿Sé qué tipo de información va en una dimensión?
  - ¿Entiendo la diferencia entre surrogate key y natural key?
  - ¿Puedo identificar si un atributo debe ser dimensión o medida?

- [ ] **Sé cuándo usar Star Schema vs. Snowflake Schema**
  - ¿Entiendo las ventajas y desventajas de cada uno?
  - ¿Puedo diseñar un star schema simple para un caso de uso?
  - ¿Sé por qué star schema es generalmente preferido en la industria?

- [ ] **Comprendo Slowly Changing Dimensions (SCD)**
  - ¿Puedo explicar las diferencias entre SCD Tipo 1, 2 y 3?
  - ¿Sé cuándo usar cada tipo de SCD?
  - ¿Entiendo cómo implementar SCD Tipo 2 con fechas de vigencia?

- [ ] **Puedo identificar errores comunes**
  - ¿Reconozco cuándo alguien está sobre-normalizando un DWH?
  - ¿Sé por qué es crítico definir el grano de una fact table?
  - ¿Entiendo la importancia de DimFecha?

- [ ] **Puedo aplicar estos conceptos a casos de negocio reales**
  - ¿Puedo diseñar un modelo dimensional para un e-commerce?
  - ¿Puedo diseñar un modelo dimensional para logística o manufactura?
  - ¿Sé escribir queries SQL básicos contra un star schema?

---

## Próximos Pasos

Ahora que comprendes los fundamentos teóricos del modelado dimensional, en los siguientes documentos verás:

1. **02-EJEMPLOS.md**: Casos completos trabajados paso a paso (e-commerce, logística, educación)
2. **03-EJERCICIOS.md**: Ejercicios prácticos para diseñar tus propios modelos dimensionales
3. **04-proyecto-practico**: Implementar un data warehouse dimensional completo en Python

**Recuerda**: El modelado dimensional es una de las habilidades más valiosas de un Data Engineer. Dominar star schemas, fact/dimension tables y SCDs te permitirá diseñar data warehouses que realmente ayuden a las empresas a tomar decisiones basadas en datos.

---

**Tiempo estimado de lectura**: 35-40 minutos
**Nivel**: Intermedio
**Prerequisitos**: SQL básico, conceptos de bases de datos relacionales
