-- ===============================================
-- Inicialización de PostgreSQL
-- Master en Ingeniería de Datos
-- ===============================================
-- Este script se ejecuta automáticamente al iniciar
-- el contenedor de PostgreSQL por primera vez
-- ===============================================

-- ===============================================
-- Base de Datos y Extensiones
-- ===============================================

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ===============================================
-- Tablas de Ejemplo para Módulos 2-5
-- ===============================================

-- Tabla: usuarios (ejemplo para Módulo 2)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: productos (ejemplo para Módulo 2)
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    categoria VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: ventas (ejemplo para Módulo 3)
CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    producto_id INTEGER REFERENCES productos(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL,
    precio_total NUMERIC(10, 2) NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente'
);

-- Tabla: logs (ejemplo para Módulo 5)
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    nivel VARCHAR(20) NOT NULL,
    mensaje TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================
-- Índices para Optimización
-- ===============================================

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios(activo);
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria);
CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX IF NOT EXISTS idx_ventas_usuario ON ventas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_logs_nivel ON logs(nivel);

-- ===============================================
-- Triggers para updated_at automático
-- ===============================================

CREATE OR REPLACE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_updated_at();

CREATE TRIGGER trigger_productos_updated_at
    BEFORE UPDATE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_updated_at();

-- ===============================================
-- Datos de Ejemplo
-- ===============================================

-- Insertar usuarios de ejemplo
INSERT INTO usuarios (nombre, email, metadata) VALUES
('Juan Pérez', 'juan@example.com', '{"pais": "España", "ciudad": "Madrid"}'),
('María García', 'maria@example.com', '{"pais": "México", "ciudad": "CDMX"}'),
('Carlos López', 'carlos@example.com', '{"pais": "Argentina", "ciudad": "Buenos Aires"}')
ON CONFLICT (email) DO NOTHING;

-- Insertar productos de ejemplo
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Laptop HP', 'Laptop HP 15 pulgadas, 8GB RAM', 799.99, 50, 'Electrónica'),
('Mouse Logitech', 'Mouse inalámbrico Logitech', 29.99, 200, 'Accesorios'),
('Teclado Mecánico', 'Teclado mecánico RGB', 89.99, 100, 'Accesorios'),
('Monitor Samsung', 'Monitor Samsung 24 pulgadas', 199.99, 75, 'Electrónica')
ON CONFLICT DO NOTHING;

-- Insertar ventas de ejemplo
INSERT INTO ventas (usuario_id, producto_id, cantidad, precio_unitario, precio_total, estado)
SELECT
    1,
    p.id,
    2,
    p.precio,
    p.precio * 2,
    'completada'
FROM productos p
WHERE p.nombre = 'Mouse Logitech'
ON CONFLICT DO NOTHING;

-- Insertar logs de ejemplo
INSERT INTO logs (nivel, mensaje, metadata) VALUES
('INFO', 'Aplicación iniciada correctamente', '{"version": "1.0.0"}'),
('WARNING', 'Conexión lenta detectada', '{"latency_ms": 350}'),
('ERROR', 'Error al procesar solicitud', '{"error_code": 500}')
ON CONFLICT DO NOTHING;

-- ===============================================
-- Vistas Útiles
-- ===============================================

-- Vista: resumen de ventas por usuario
CREATE OR REPLACE VIEW vista_ventas_usuario AS
SELECT
    u.id AS usuario_id,
    u.nombre,
    u.email,
    COUNT(v.id) AS total_ventas,
    SUM(v.precio_total) AS total_gastado,
    AVG(v.precio_total) AS promedio_venta
FROM usuarios u
LEFT JOIN ventas v ON u.id = v.usuario_id
GROUP BY u.id, u.nombre, u.email;

-- Vista: productos con bajo stock
CREATE OR REPLACE VIEW vista_bajo_stock AS
SELECT
    id,
    nombre,
    stock,
    precio,
    categoria
FROM productos
WHERE stock < 100 AND activo = TRUE
ORDER BY stock ASC;

-- ===============================================
-- Permisos (para seguridad)
-- ===============================================

-- Revocar acceso público por defecto
REVOKE ALL ON SCHEMA public FROM PUBLIC;

-- Otorgar permisos solo al usuario de la aplicación
GRANT USAGE ON SCHEMA public TO dataeng_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dataeng_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dataeng_user;

-- ===============================================
-- Comentarios (documentación)
-- ===============================================

COMMENT ON TABLE usuarios IS 'Tabla de usuarios del sistema';
COMMENT ON TABLE productos IS 'Catálogo de productos disponibles';
COMMENT ON TABLE ventas IS 'Registro de transacciones de venta';
COMMENT ON TABLE logs IS 'Logs de aplicación para monitoreo';

-- ===============================================
-- Finalización
-- ===============================================

-- Análisis de tablas para optimizar queries
ANALYZE usuarios;
ANALYZE productos;
ANALYZE ventas;
ANALYZE logs;

-- Mensaje de finalización (aparecerá en logs de Docker)
DO $$
BEGIN
    RAISE NOTICE 'Base de datos inicializada correctamente para el Master en Ingeniería de Datos';
END $$;

