# 🍃 Scripts de Inicialización MongoDB

Este directorio contiene scripts JavaScript que se ejecutan automáticamente al iniciar MongoDB por primera vez en Docker.

---

## 📋 Uso

Los archivos `.js` en este directorio se ejecutan en orden alfabético cuando se crea el contenedor de MongoDB por primera vez.

---

## 🔢 Convención de Nombres

Usa prefijos numéricos para controlar el orden de ejecución:

```
01-create-collections.js
02-insert-seed-data.js
03-create-indexes.js
```

---

## ⚙️ Cómo Funciona

1. Docker Compose monta este directorio en `/docker-entrypoint-initdb.d/` del contenedor MongoDB
2. Al crear el contenedor por primera vez, MongoDB ejecuta todos los `.js` en orden alfabético
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

## 📝 Ejemplo: `01-create-collections.js`

```javascript
// Conectar a la base de datos
db = db.getSiblingDB('dataeng_db');

// Crear colección de usuarios con validación
db.createCollection('users', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['username', 'email', 'created_at'],
            properties: {
                username: {
                    bsonType: 'string',
                    description: 'Username is required and must be a string'
                },
                email: {
                    bsonType: 'string',
                    pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
                    description: 'Email is required and must be a valid email'
                },
                created_at: {
                    bsonType: 'date',
                    description: 'Created at is required and must be a date'
                }
            }
        }
    }
});

// Crear índices
db.users.createIndex({ username: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ created_at: -1 });

// Crear colección de eventos
db.createCollection('events');
db.events.createIndex({ user_id: 1 });
db.events.createIndex({ event_type: 1 });
db.events.createIndex({ created_at: -1 });

print('✅ Colecciones e índices creados exitosamente');
```

---

## 📝 Ejemplo: `02-insert-seed-data.js`

```javascript
// Conectar a la base de datos
db = db.getSiblingDB('dataeng_db');

// Insertar datos de ejemplo
db.users.insertMany([
    {
        username: 'admin',
        email: 'admin@dataeng.com',
        role: 'admin',
        created_at: new Date()
    },
    {
        username: 'user1',
        email: 'user1@dataeng.com',
        role: 'user',
        created_at: new Date()
    }
]);

print('✅ Datos de ejemplo insertados exitosamente');
```

---

## 🔒 Seguridad

- No incluyas contraseñas reales en estos scripts
- No commitees datos sensibles
- Usa variables de entorno cuando sea posible
- Los datos de ejemplo deben ser ficticios

---

## 📚 Documentación Oficial

- [MongoDB Docker Hub](https://hub.docker.com/_/mongo)
- [MongoDB Initialization Scripts](https://github.com/docker-library/docs/blob/master/mongo/README.md#initializing-a-fresh-instance)

---

*Última actualización: 2025-10-18*

