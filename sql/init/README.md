# 🗄️ Scripts de Inicialización SQL

Este directorio contiene scripts SQL que se ejecutan automáticamente al iniciar PostgreSQL por primera vez en Docker.

---

## 📋 Uso

Los archivos `.sql` en este directorio se ejecutan en orden alfabético cuando se crea el contenedor de PostgreSQL por primera vez.

---

## 🔢 Convención de Nombres

Usa prefijos numéricos para controlar el orden de ejecución:

```
01-create-tables.sql
02-insert-seed-data.sql
03-create-views.sql
04-create-functions.sql
```

---

## ⚙️ Cómo Funciona

1. Docker Compose monta este directorio en `/docker-entrypoint-initdb.d/` del contenedor PostgreSQL
2. Al crear el contenedor por primera vez, PostgreSQL ejecuta todos los `.sql` y `.sh` en orden alfabético
3. Los scripts solo se ejecutan una vez (en la primera creación)

---

## 🔄 Reiniciar Base de Datos

Si necesitas volver a ejecutar los scripts de inicialización:

```bash
# Detener y eliminar volúmenes
docker-compose down -v

# Volver a iniciar (ejecutará los scripts nuevamente)
docker-compose up -d
```

⚠️ **ADVERTENCIA**: Esto eliminará todos los datos de la base de datos.

---

## 📝 Ejemplo: `01-create-tables.sql`

```sql
-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de eventos
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_created_at ON events(created_at);
```

---

## 🔒 Seguridad

- No incluyas contraseñas reales en estos scripts
- No commitees datos sensibles
- Usa variables de entorno cuando sea posible

---

*Última actualización: 2025-10-18*

