# Teoría: MongoDB y NoSQL

## Introducción: El Cambio de Paradigma

Imagina que tienes una biblioteca tradicional donde cada libro debe seguir exactamente el mismo formato: mismo tamaño, misma estructura de capítulos, mismas categorías. Esto es SQL: estructurado, rígido, predecible.

Ahora imagina una biblioteca donde puedes guardar libros, revistas, mapas, fotografías y objetos 3D, cada uno con su propia estructura única. Esto es **MongoDB**: flexible, adaptable, schema-free.

### ¿Por qué necesitamos NoSQL?

En el mundo real de Data Engineering:

- **Netflix** usa NoSQL para catálogos de películas (cada película tiene atributos diferentes)
- **Uber** usa NoSQL para tracking en tiempo real (millones de escrituras/segundo)
- **Instagram** usa NoSQL para posts y comentarios (esquema variable, escalabilidad horizontal)

**No es que NoSQL sea "mejor" que SQL**. Son herramientas diferentes para problemas diferentes.

---

## Parte 1: Fundamentos de MongoDB

### Concepto 1: Documentos y Colecciones

#### ¿Qué es un documento?

Un **documento** en MongoDB es un objeto JSON (técnicamente BSON - Binary JSON) que contiene datos.

**Analogía**: Es como una ficha de un archivo. Cada ficha puede tener diferentes campos. Una ficha de cliente puede tener teléfono, otra no. Una ficha puede tener lista de compras, otra no.

```javascript
// Documento de usuario
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nombre": "Ana García",
  "email": "ana@example.com",
  "edad": 30,
  "tags": ["premium", "activo"],
  "direccion": {
    "calle": "Main St 123",
    "ciudad": "Madrid",
    "pais": "ES"
  }
}
```

**Características**:
- Cada documento tiene un `_id` único (PK automático)
- Puede contener subdocumentos (objetos anidados)
- Puede contener arrays
- Flexible: cada documento puede tener campos diferentes

#### ¿Qué es una colección?

Una **colección** es un grupo de documentos. Es equivalente a una "tabla" en SQL, pero sin esquema fijo.

```
Database: ecommerce
├── Collection: usuarios
│   ├── {"_id": 1, "nombre": "Ana", "email": "..."}
│   ├── {"_id": 2, "nombre": "Bob", "tipo": "empresa"}
│   └── {"_id": 3, "nombre": "Carlos", "vip": true}
│
└── Collection: productos
    ├── {"_id": 101, "nombre": "Laptop", "precio": 999}
    └── {"_id": 102, "nombre": "Mouse", "color": "negro"}
```

**Nota**: Documentos en la misma colección pueden tener estructuras totalmente diferentes.

---

### Concepto 2: SQL vs MongoDB

#### Terminología

| SQL         | MongoDB                |
| ----------- | ---------------------- |
| Database    | Database               |
| Table       | Collection             |
| Row         | Document               |
| Column      | Field                  |
| Primary Key | _id                    |
| Index       | Index                  |
| JOIN        | $lookup o embedding    |
| Foreign Key | Referencias (manuales) |

#### Ejemplo comparativo

**SQL:**
```sql
-- Tabla usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    email VARCHAR(200)
);

INSERT INTO usuarios VALUES (1, 'Ana', 'ana@example.com');
```

**MongoDB:**
```javascript
// Colección usuarios (no necesita CREATE)
db.usuarios.insertOne({
  nombre: "Ana",
  email: "ana@example.com"
});
// _id se genera automáticamente
```

#### Esquema flexible vs rígido

**SQL (rígido)**:
```sql
-- Si quieres añadir campo "telefono", debes:
ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20);
-- Afecta a TODOS los usuarios existentes (NULL o valor default)
```

**MongoDB (flexible)**:
```javascript
// Simplemente inserta con el nuevo campo
db.usuarios.insertOne({
  nombre: "Bob",
  email: "bob@example.com",
  telefono: "+34 600 000 000"  // ¡Nuevo campo!
});
// Los documentos anteriores no se ven afectados
```

---

### Concepto 3: CRUD en MongoDB

#### Create (Insertar)

```javascript
// Insertar un documento
db.productos.insertOne({
  nombre: "Laptop Pro",
  precio: 1299,
  stock: 50,
  categoria: "electrónica"
});

// Insertar múltiples
db.productos.insertMany([
  {nombre: "Mouse", precio: 25},
  {nombre: "Teclado", precio: 89},
  {nombre: "Monitor", precio: 299}
]);
```

#### Read (Consultar)

```javascript
// Encontrar todos
db.productos.find();

// Encontrar con condición
db.productos.find({categoria: "electrónica"});

// Encontrar uno
db.productos.findOne({nombre: "Laptop Pro"});

// Con operadores
db.productos.find({precio: {$gt: 100}});  // precio > 100

// Múltiples condiciones
db.productos.find({
  categoria: "electrónica",
  precio: {$lt: 500},
  stock: {$gte: 10}
});
```

#### Update (Actualizar)

```javascript
// Actualizar uno
db.productos.updateOne(
  {nombre: "Laptop Pro"},              // Filtro
  {$set: {precio: 1199, stock: 45}}    // Cambios
);

// Actualizar múltiples
db.productos.updateMany(
  {categoria: "electrónica"},
  {$inc: {precio: -50}}  // Decrementar 50
);

// Reemplazar documento completo
db.productos.replaceOne(
  {_id: ObjectId("...")},
  {nombre: "Nuevo", precio: 999}
);
```

#### Delete (Eliminar)

```javascript
// Eliminar uno
db.productos.deleteOne({nombre: "Mouse"});

// Eliminar múltiples
db.productos.deleteMany({stock: 0});

// Eliminar todos (¡cuidado!)
db.productos.deleteMany({});
```

---

## Parte 2: Operadores de MongoDB

### Concepto 4: Operadores de Comparación

```javascript
// $eq - Igual (raramente usado, es el default)
db.productos.find({precio: {$eq: 100}});
// Equivalente a:
db.productos.find({precio: 100});

// $ne - No igual
db.productos.find({categoria: {$ne: "electrónica"}});

// $gt, $gte - Mayor que, Mayor o igual
db.productos.find({precio: {$gt: 500}});
db.productos.find({stock: {$gte: 10}});

// $lt, $lte - Menor que, Menor o igual
db.productos.find({precio: {$lt: 100}});

// $in - En lista
db.productos.find({
  categoria: {$in: ["electrónica", "hogar", "deporte"]}
});

// $nin - No en lista
db.productos.find({
  estado: {$nin: ["agotado", "descatalogado"]}
});
```

### Concepto 5: Operadores Lógicos

```javascript
// $and - Y lógico (default si pones múltiples campos)
db.productos.find({
  $and: [
    {precio: {$gt: 100}},
    {stock: {$gt: 0}},
    {categoria: "electrónica"}
  ]
});

// Más simple (equivalente):
db.productos.find({
  precio: {$gt: 100},
  stock: {$gt: 0},
  categoria: "electrónica"
});

// $or - O lógico
db.productos.find({
  $or: [
    {categoria: "electrónica"},
    {precio: {$lt: 50}}
  ]
});

// $nor - Ni esto ni aquello
db.productos.find({
  $nor: [
    {stock: 0},
    {precio: {$gt: 1000}}
  ]
});

// $not - Negación
db.productos.find({
  precio: {$not: {$gt: 100}}
});
// Es lo mismo que $lte: 100
```

### Concepto 6: Operadores de Arrays

```javascript
// $all - Contiene todos los elementos
db.productos.find({
  tags: {$all: ["oferta", "destacado"]}
});

// $elemMatch - Al menos un elemento cumple todas las condiciones
db.productos.find({
  valoraciones: {
    $elemMatch: {puntuacion: {$gte: 4}, verificado: true}
  }
});

// $size - Tamaño exacto del array
db.productos.find({
  imagenes: {$size: 3}
});
```

### Concepto 7: Operadores de Actualización

```javascript
// $set - Asignar valor
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$set: {precio: 999, stock: 100}}
);

// $unset - Eliminar campo
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$unset: {descuento: ""}}  // Elimina el campo "descuento"
);

// $inc - Incrementar/decrementar
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$inc: {stock: -1, ventas: 1}}  // stock-1, ventas+1
);

// $push - Añadir a array
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$push: {tags: "nuevo"}}
);

// $pull - Quitar de array
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$pull: {tags: "viejo"}}
);

// $addToSet - Añadir si no existe (evita duplicados)
db.productos.updateOne(
  {_id: ObjectId("...")},
  {$addToSet: {tags: "destacado"}}
);
```

---

## Parte 3: Agregaciones

### Concepto 8: Pipeline de Agregación

El **aggregation pipeline** es como una cadena de montaje donde los datos pasan por múltiples etapas de transformación.

**Analogía**: Es como preparar un jugo:
1. **$match**: Selecciona las frutas (filtrar)
2. **$group**: Agrupa por tipo (agrupar)
3. **$sort**: Ordena por dulzura (ordenar)
4. **$limit**: Toma las 5 mejores (limitar)

```javascript
db.ventas.aggregate([
  // Etapa 1: Filtrar ventas de 2024
  {$match: {fecha: {$gte: ISODate("2024-01-01")}}},

  // Etapa 2: Agrupar por producto
  {$group: {
    _id: "$producto",
    total_vendido: {$sum: "$cantidad"},
    ingreso_total: {$sum: "$monto"}
  }},

  // Etapa 3: Ordenar por ingreso
  {$sort: {ingreso_total: -1}},

  // Etapa 4: Top 10
  {$limit: 10}
]);
```

### Concepto 9: Etapas Comunes del Pipeline

#### $match - Filtrar

```javascript
// Equivalente a WHERE en SQL
{$match: {
  categoria: "electrónica",
  precio: {$lt: 500}
}}
```

#### $group - Agrupar

```javascript
// Equivalente a GROUP BY en SQL
{$group: {
  _id: "$categoria",              // GROUP BY categoria
  total: {$sum: 1},               // COUNT(*)
  precio_promedio: {$avg: "$precio"},  // AVG(precio)
  precio_max: {$max: "$precio"},       // MAX(precio)
  precio_min: {$min: "$precio"}        // MIN(precio)
}}
```

#### $project - Seleccionar campos

```javascript
// Equivalente a SELECT en SQL
{$project: {
  nombre: 1,              // Incluir
  precio: 1,              // Incluir
  _id: 0,                 // Excluir
  precio_con_iva: {$multiply: ["$precio", 1.21]}  // Calculado
}}
```

#### $sort - Ordenar

```javascript
// Equivalente a ORDER BY en SQL
{$sort: {
  precio: -1,    // Descendente
  nombre: 1      // Ascendente
}}
```

#### $limit y $skip - Paginación

```javascript
// Equivalente a LIMIT y OFFSET en SQL
{$skip: 20},   // Saltar primeros 20
{$limit: 10}   // Tomar siguiente 10
```

#### $lookup - JOIN

```javascript
// Equivalente a LEFT JOIN en SQL
{$lookup: {
  from: "productos",           // Tabla a joinear
  localField: "producto_id",   // Campo local
  foreignField: "_id",         // Campo foráneo
  as: "detalle_producto"       // Alias resultado
}}
```

### Concepto 10: Agregaciones Complejas

#### Ejemplo realista: Analytics de ventas

```javascript
db.ventas.aggregate([
  // 1. Filtrar ventas de último mes
  {$match: {
    fecha: {$gte: new Date("2024-10-01")}
  }},

  // 2. Join con productos
  {$lookup: {
    from: "productos",
    localField: "producto_id",
    foreignField: "_id",
    as: "producto"
  }},

  // 3. Descomponer array de producto
  {$unwind: "$producto"},

  // 4. Agrupar por categoría
  {$group: {
    _id: "$producto.categoria",
    total_ventas: {$sum: "$cantidad"},
    ingreso_total: {$sum: {$multiply: ["$cantidad", "$precio"]}},
    ticket_promedio: {$avg: {$multiply: ["$cantidad", "$precio"]}}
  }},

  // 5. Calcular campos adicionales
  {$project: {
    categoria: "$_id",
    total_ventas: 1,
    ingreso_total: 1,
    ticket_promedio: {$round: ["$ticket_promedio", 2]}
  }},

  // 6. Ordenar por ingreso
  {$sort: {ingreso_total: -1}}
]);
```

---

## Parte 4: Índices y Performance

### Concepto 11: Índices en MongoDB

**Analogía**: Un índice es como el índice de un libro. Sin él, tienes que leer todo el libro para encontrar algo. Con él, vas directamente a la página.

```javascript
// Crear índice simple
db.productos.createIndex({nombre: 1});  // 1 = ascendente

// Índice compuesto
db.productos.createIndex({categoria: 1, precio: -1});

// Índice único
db.usuarios.createIndex({email: 1}, {unique: true});

// Ver índices
db.productos.getIndexes();

// Eliminar índice
db.productos.dropIndex("nombre_1");
```

#### Cuándo crear índices

✅ **Crea índices en**:
- Campos que usas frecuentemente en `find()`
- Campos que usas en `sort()`
- Campos únicos (email, username)

❌ **No indices**:
- Campos que raramente consultas
- Campos con baja cardinalidad (pocos valores únicos)
- Colecciones muy pequeñas (<1000 documentos)

---

## Parte 5: Modelado de Datos en MongoDB

### Concepto 12: Embedding vs Referencing

Esta es LA decisión más importante al diseñar en MongoDB.

#### Embedding (Embeber)

Guardar datos relacionados DENTRO del mismo documento.

```javascript
// Usuario con direcciones embebidas
{
  _id: ObjectId("..."),
  nombre: "Ana García",
  email: "ana@example.com",
  direcciones: [
    {
      tipo: "casa",
      calle: "Main St 123",
      ciudad: "Madrid"
    },
    {
      tipo: "trabajo",
      calle: "Office Blvd 456",
      ciudad: "Barcelona"
    }
  ]
}
```

**Ventajas**:
- Una sola query para obtener todo
- Atómico (todo se actualiza junto)
- Performance excelente para lectura

**Desventajas**:
- Duplicación si los datos se comparten
- Documentos pueden crecer mucho (límite 16MB)

#### Referencing (Referenciar)

Guardar datos relacionados en documentos separados (como FK en SQL).

```javascript
// Colección usuarios
{
  _id: ObjectId("user123"),
  nombre: "Ana García",
  email: "ana@example.com"
}

// Colección órdenes (referencias a usuarios)
{
  _id: ObjectId("order456"),
  usuario_id: ObjectId("user123"),  // Referencia
  producto: "Laptop",
  monto: 999
}
```

**Ventajas**:
- No hay duplicación
- Documentos más pequeños
- Fácil actualizar datos compartidos

**Desventajas**:
- Requiere múltiples queries (o $lookup)
- No es atómico entre colecciones

#### Regla general

**Embebe cuando**:
- Relación 1:pocos (usuario → 3 direcciones)
- Los datos siempre se consultan juntos
- Los datos no se comparten con otros documentos

**Referencia cuando**:
- Relación 1:muchos (usuario → 1000 órdenes)
- Los datos se consultan independientemente
- Los datos se comparten entre documentos

---

## Comparaciones y Decisiones

### ¿Cuándo usar MongoDB vs PostgreSQL?

#### Usa MongoDB cuando:

✅ **Datos semi-estructurados**
```javascript
// Cada producto tiene atributos diferentes
{producto: "Laptop", ram: "16GB", pantalla: "15inch"}
{producto: "Libro", paginas: 300, autor: "..."}
{producto: "Camisa", talla: "M", color: "azul"}
```

✅ **Escalabilidad horizontal crítica**
- Necesitas manejar terabytes de datos
- Sharding distribuido entre servidores

✅ **Esquema cambiante**
- Startup en rápida evolución
- Prototipado ágil

✅ **Escritura intensiva**
- Logs, eventos, métricas
- Millones de inserts por segundo

#### Usa PostgreSQL cuando:

✅ **Datos estructurados**
- Estructura fija y bien definida
- Integridad relacional importante

✅ **Transacciones complejas**
- Operaciones financieras
- Consistency crítico

✅ **Queries complejas con JOINs**
- Reportes con múltiples tablas relacionadas
- Análisis relacional profundo

---

## Errores Comunes

### Error 1: Embedar todo

**Problema**:
```javascript
// ❌ MAL: Embedar 10,000 órdenes en un usuario
{
  _id: ObjectId("..."),
  nombre: "Ana",
  ordenes: [
    {...}, {...}, ... // 10,000 documentos
  ]
}
// Excederá límite de 16MB
```

**Solución**: Usa referencias para relaciones 1:muchos grandes.

### Error 2: Referenciar todo (usar MongoDB como SQL)

**Problema**:
```javascript
// ❌ MAL: Referenciar dirección cuando siempre se consulta con usuario
// Usuario
{_id: 1, nombre: "Ana", direccion_id: 101}
// Dirección
{_id: 101, calle: "Main St"}
// Requiere 2 queries siempre
```

**Solución**: Embebe si siempre se consultan juntos.

### Error 3: No usar índices

**Problema**:
```javascript
// ❌ MAL: Query sin índice en colección de 1M documentos
db.usuarios.find({email: "ana@example.com"});
// Escanea 1M documentos
```

**Solución**:
```javascript
// ✅ BIEN: Crear índice
db.usuarios.createIndex({email: 1}, {unique: true});
// Ahora es instantáneo
```

---

## Checklist de Aprendizaje

- [ ] Entiendo qué es un documento y una colección
- [ ] Puedo hacer CRUD básico
- [ ] Conozco operadores de comparación ($gt, $lt, $in)
- [ ] Puedo usar operadores lógicos ($and, $or)
- [ ] Entiendo el aggregation pipeline
- [ ] Puedo hacer $match, $group, $sort
- [ ] Sé cuándo embedar vs referenciar
- [ ] Puedo crear índices
- [ ] Sé cuándo usar MongoDB vs PostgreSQL

---

## Recursos Adicionales

### Documentación Oficial
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query/)
- [Aggregation Pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)

### Cursos Gratuitos
- [MongoDB University](https://university.mongodb.com/)
- [M001: MongoDB Basics](https://university.mongodb.com/courses/M001/about)

### Herramientas
- [MongoDB Compass](https://www.mongodb.com/products/compass) - GUI oficial
- [Studio 3T](https://studio3t.com/) - IDE avanzado

---

**Próximos pasos**: Lee **02-EJEMPLOS.md** para ver MongoDB en acción con ejemplos reales.

**Tiempo de lectura:** 35-45 minutos
**Última actualización:** 2025-10-25

¡Bienvenido al mundo NoSQL! 🍃
---

## 🧭 Navegación

⬅️ **Anterior**: [PostgreSQL Avanzado - Proyecto Práctico](../tema-1-postgresql-avanzado/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
