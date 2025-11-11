-- Schema del Data Warehouse - Star Schema para E-commerce
-- SQLite Database

-- ============================================================================
-- TABLA DE DIMENSIÓN: DimFecha
-- ============================================================================
CREATE TABLE IF NOT EXISTS DimFecha (
    fecha_id INTEGER PRIMARY KEY,           -- YYYYMMDD format (ej: 20240101)
    fecha_completa DATE NOT NULL,           -- Fecha completa
    dia INTEGER NOT NULL,                   -- Día del mes (1-31)
    mes INTEGER NOT NULL,                   -- Mes (1-12)
    mes_nombre TEXT NOT NULL,               -- Nombre del mes en español
    trimestre INTEGER NOT NULL,             -- Trimestre (1-4)
    anio INTEGER NOT NULL,                  -- Año
    dia_semana TEXT NOT NULL,               -- Nombre del día en español
    numero_dia_semana INTEGER NOT NULL,     -- 0=Lunes, 6=Domingo
    numero_semana INTEGER NOT NULL,         -- Número de semana del año
    es_fin_de_semana BOOLEAN NOT NULL,      -- True si sábado o domingo
    es_dia_festivo BOOLEAN NOT NULL,        -- True si es día festivo
    nombre_festivo TEXT                     -- Nombre del festivo (NULL si no es festivo)
);

-- ============================================================================
-- TABLA DE DIMENSIÓN: DimProducto
-- ============================================================================
CREATE TABLE IF NOT EXISTS DimProducto (
    producto_id INTEGER PRIMARY KEY,        -- ID único del producto
    sku TEXT NOT NULL UNIQUE,               -- Stock Keeping Unit
    nombre_producto TEXT NOT NULL,          -- Nombre del producto
    marca TEXT NOT NULL,                    -- Marca
    categoria TEXT NOT NULL,                -- Categoría (denormalizada)
    subcategoria TEXT NOT NULL,             -- Subcategoría (denormalizada)
    precio_catalogo REAL NOT NULL,          -- Precio de catálogo
    peso_kg REAL NOT NULL,                  -- Peso en kilogramos
    requiere_refrigeracion BOOLEAN NOT NULL -- Si requiere refrigeración
);

-- ============================================================================
-- TABLA DE DIMENSIÓN: DimCliente (con SCD Type 2)
-- ============================================================================
CREATE TABLE IF NOT EXISTS DimCliente (
    cliente_sk INTEGER PRIMARY KEY AUTOINCREMENT,  -- Surrogate key
    cliente_id INTEGER NOT NULL,            -- ID natural del cliente
    nombre TEXT NOT NULL,                   -- Nombre completo
    email TEXT NOT NULL,                    -- Email
    telefono TEXT NOT NULL,                 -- Teléfono
    direccion TEXT NOT NULL,                -- Dirección completa
    ciudad TEXT NOT NULL,                   -- Ciudad
    estado TEXT NOT NULL,                   -- Estado/Provincia
    codigo_postal TEXT NOT NULL,            -- Código postal
    fecha_registro DATE NOT NULL,           -- Fecha de registro original
    segmento TEXT NOT NULL,                 -- Segmento (Premium, Regular, Nuevo)
    -- Campos SCD Type 2
    fecha_inicio DATE NOT NULL,             -- Fecha inicio validez
    fecha_fin DATE,                         -- Fecha fin validez (NULL si actual)
    version INTEGER NOT NULL,               -- Versión del registro
    es_actual BOOLEAN NOT NULL              -- True si es versión actual
);

-- Índices para búsquedas eficientes en SCD Type 2
CREATE INDEX IF NOT EXISTS idx_cliente_natural_id ON DimCliente(cliente_id);
CREATE INDEX IF NOT EXISTS idx_cliente_actual ON DimCliente(es_actual) WHERE es_actual = 1;

-- ============================================================================
-- TABLA DE DIMENSIÓN: DimVendedor
-- ============================================================================
CREATE TABLE IF NOT EXISTS DimVendedor (
    vendedor_id INTEGER PRIMARY KEY,        -- ID único del vendedor
    nombre TEXT NOT NULL,                   -- Nombre completo
    email TEXT NOT NULL,                    -- Email
    telefono TEXT NOT NULL,                 -- Teléfono
    region TEXT NOT NULL,                   -- Región asignada
    comision_porcentaje REAL NOT NULL,      -- Porcentaje de comisión (5-15%)
    supervisor_id INTEGER,                  -- ID del supervisor (jerarquía)
    gerente_regional TEXT                   -- Nombre del gerente regional
);

-- ============================================================================
-- TABLA DE HECHOS: FactVentas
-- ============================================================================
CREATE TABLE IF NOT EXISTS FactVentas (
    venta_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único de la venta
    fecha_id INTEGER NOT NULL,              -- FK a DimFecha
    producto_id INTEGER NOT NULL,           -- FK a DimProducto
    cliente_id INTEGER NOT NULL,            -- FK a DimCliente
    vendedor_id INTEGER NOT NULL,           -- FK a DimVendedor
    -- Métricas aditivas
    cantidad INTEGER NOT NULL,              -- Cantidad vendida
    precio_unitario REAL NOT NULL,          -- Precio unitario
    descuento REAL NOT NULL,                -- Descuento aplicado
    impuesto REAL NOT NULL,                 -- Impuesto aplicado
    monto_neto REAL NOT NULL,               -- Monto neto = (precio * cantidad) - descuento + impuesto
    -- Claves foráneas
    FOREIGN KEY (fecha_id) REFERENCES DimFecha(fecha_id),
    FOREIGN KEY (producto_id) REFERENCES DimProducto(producto_id),
    FOREIGN KEY (cliente_id) REFERENCES DimCliente(cliente_sk),
    FOREIGN KEY (vendedor_id) REFERENCES DimVendedor(vendedor_id)
);

-- Índices para optimizar queries analíticos (OLAP)
CREATE INDEX IF NOT EXISTS idx_fact_fecha ON FactVentas(fecha_id);
CREATE INDEX IF NOT EXISTS idx_fact_producto ON FactVentas(producto_id);
CREATE INDEX IF NOT EXISTS idx_fact_cliente ON FactVentas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_fact_vendedor ON FactVentas(vendedor_id);

-- Índice compuesto para análisis temporal por producto
CREATE INDEX IF NOT EXISTS idx_fact_fecha_producto ON FactVentas(fecha_id, producto_id);
