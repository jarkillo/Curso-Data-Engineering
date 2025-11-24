# Ejemplos Prácticos: MongoDB

Este documento contiene 5 ejemplos progresivos que demuestran el uso de MongoDB en contextos empresariales realistas.

---

## Ejemplo 1: CRUD Básico - Catálogo de Productos - Nivel: Básico ⭐

### Contexto

Trabajas para **TechStore**, una tienda de electrónica. Necesitan un catálogo de productos flexible porque cada categoría tiene atributos diferentes (ej: laptops tienen RAM y CPU, cables tienen longitud).

### Situación Inicial

**Problema con SQL**: Necesitarías múltiples tablas o columnas NULL para atributos específicos.

**Solución con MongoDB**: Documentos flexibles que se adaptan a cada producto.

### Paso 1: Conectar y crear base de datos

```javascript
// Conectar a MongoDB
use techstore;

// Ver base de datos actual
db;  // techstore
```

### Paso 2: Insertar productos (Create)

```javascript
// Insertar un producto (laptop)
db.productos.insertOne({
  nombre: "Laptop Pro 15",
  categoria: "laptops",
  precio: 1299,
  stock: 15,
  especificaciones: {
    ram: "16GB",
    cpu: "Intel i7",
    almacenamiento: "512GB SSD"
  },
  tags: ["premium", "oferta"],
  fecha_agregado: new Date()
});

// Insertar otro producto (cable - atributos diferentes)
db.productos.insertOne({
  nombre: "Cable HDMI 2.0",
  categoria: "accesorios",
  precio: 15,
  stock: 200,
  especificaciones: {
    longitud: "2m",
    tipo_conector: "HDMI Type A"
  },
  tags: ["basico"]
});

// Insertar múltiples productos
db.productos.insertMany([
  {
    nombre: "Mouse Inalámbrico",
    categoria: "accesorios",
    precio: 29,
    stock: 75
  },
  {
    nombre: "Teclado Mecánico RGB",
    categoria: "accesorios",
    precio: 89,
    stock: 30,
    especificaciones: {
      tipo_switches: "Cherry MX Blue",
      rgb: true
    }
  }
]);
```

**Output**:
```javascript
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("65a1234..."),
    '1': ObjectId("65a1235...")
  }
}
```

### Paso 3: Consultar productos (Read)

```javascript
// Todos los productos
db.productos.find();

// Productos de una categoría
db.productos.find({categoria: "accesorios"});

// Productos con precio menor a $50
db.productos.find({precio: {$lt: 50}});

// Un solo producto
db.productos.findOne({nombre: "Laptop Pro 15"});

// Productos con stock bajo (menos de 20)
db.productos.find({stock: {$lt: 20}});

// Formato legible
db.productos.find({categoria: "accesorios"}).pretty();
```

### Paso 4: Actualizar productos (Update)

```javascript
// Actualizar precio de un producto
db.productos.updateOne(
  {nombre: "Laptop Pro 15"},
  {$set: {precio: 1199, stock: 20}}
);

// Incrementar stock
db.productos.updateOne(
  {nombre: "Mouse Inalámbrico"},
  {$inc: {stock: 50}}  // Añade 50 al stock actual
);

// Agregar tag a un producto
db.productos.updateOne(
  {nombre: "Cable HDMI 2.0"},
  {$push: {tags: "bestseller"}}  // Añade a array
);

// Actualizar múltiples productos (descuento 10% en accesorios)
db.productos.updateMany(
  {categoria: "accesorios"},
  {$mul: {precio: 0.9}}  // Multiplica precio por 0.9
);
```

### Paso 5: Eliminar productos (Delete)

```javascript
// Eliminar productos sin stock
db.productos.deleteMany({stock: 0});

// Eliminar un producto específico
db.productos.deleteOne({nombre: "Cable HDMI 2.0"});
```

### Resultado Final

```javascript
// Verificar productos restantes
db.productos.countDocuments();  // 3

db.productos.find({}, {nombre: 1, precio: 1, stock: 1});
```

**Output**:
```javascript
[
  {_id: ObjectId("..."), nombre: "Laptop Pro 15", precio: 1199, stock: 20},
  {_id: ObjectId("..."), nombre: "Mouse Inalámbrico", precio: 26.1, stock: 125},
  {_id: ObjectId("..."), nombre: "Teclado Mecánico RGB", precio: 80.1, stock: 30}
]
```

### Lección Aprendida

MongoDB permite **flexibilidad de esquema**: cada producto puede tener campos únicos sin modificar la estructura de la colección.

---

## Ejemplo 2: Queries Avanzadas con Operadores - Nivel: Intermedio ⭐⭐

### Contexto

Trabajas para **StreamFlix**, una plataforma de streaming. Necesitas consultar películas con criterios complejos para recomendaciones y búsquedas.

### Datos

```javascript
use streamflix;

db.peliculas.insertMany([
  {
    titulo: "Inception",
    año: 2010,
    director: "Christopher Nolan",
    generos: ["Sci-Fi", "Thriller", "Action"],
    rating: 8.8,
    duracion_min: 148,
    idiomas: ["en", "es", "fr"],
    premios: {oscars: 4, globos: 1}
  },
  {
    titulo: "The Matrix",
    año: 1999,
    director: "Wachowski",
    generos: ["Sci-Fi", "Action"],
    rating: 8.7,
    duracion_min: 136,
    idiomas: ["en", "es"]
  },
  {
    titulo: "Parasite",
    año: 2019,
    director: "Bong Joon-ho",
    generos: ["Thriller", "Drama"],
    rating: 8.6,
    duracion_min: 132,
    idiomas: ["ko", "en"],
    premios: {oscars: 4, cannes: 1}
  },
  {
    titulo: "Toy Story",
    año: 1995,
    director: "John Lasseter",
    generos: ["Animation", "Family"],
    rating: 8.3,
    duracion_min: 81,
    idiomas: ["en", "es"]
  },
  {
    titulo: "The Dark Knight",
    año: 2008,
    director: "Christopher Nolan",
    generos: ["Action", "Crime", "Drama"],
    rating: 9.0,
    duracion_min: 152,
    idiomas: ["en"]
  }
]);
```

### Consultas Avanzadas

**1. Películas con rating alto (>8.5)**
```javascript
db.peliculas.find({rating: {$gt: 8.5}}, {titulo: 1, rating: 1});
```

**2. Películas de Sci-Fi O Thriller**
```javascript
db.peliculas.find({
  generos: {$in: ["Sci-Fi", "Thriller"]}
});
```

**3. Películas de Christopher Nolan con rating >8.5**
```javascript
db.peliculas.find({
  director: "Christopher Nolan",
  rating: {$gt: 8.5}
});
```

**4. Películas entre 2008 y 2019 (inclusive)**
```javascript
db.peliculas.find({
  año: {$gte: 2008, $lte: 2019}
}, {titulo: 1, año: 1});
```

**5. Películas cortas (<100 min) o largas (>150 min)**
```javascript
db.peliculas.find({
  $or: [
    {duracion_min: {$lt: 100}},
    {duracion_min: {$gt: 150}}
  ]
}, {titulo: 1, duracion_min: 1});
```

**6. Películas disponibles en español**
```javascript
db.peliculas.find({
  idiomas: "es"  // Busca en array
}, {titulo: 1, idiomas: 1});
```

**7. Películas con premios Oscar**
```javascript
db.peliculas.find({
  "premios.oscars": {$exists: true}
}, {titulo: 1, "premios.oscars": 1});
```

**8. Películas que NO son de animación**
```javascript
db.peliculas.find({
  generos: {$ne: "Animation"}
}, {titulo: 1, generos: 1});
```

**9. Query compleja: Películas de acción, rating >8.5, después de 2005**
```javascript
db.peliculas.find({
  generos: "Action",
  rating: {$gt: 8.5},
  año: {$gt: 2005}
});
```

### Proyecciones (seleccionar campos)

```javascript
// Solo título y rating
db.peliculas.find(
  {rating: {$gte: 8.5}},
  {titulo: 1, rating: 1, _id: 0}  // 0 = excluir, 1 = incluir
);
```

### Ordenamiento y límites

```javascript
// Top 3 películas por rating
db.peliculas.find()
  .sort({rating: -1})  // -1 = descendente
  .limit(3);

// Películas más recientes primero
db.peliculas.find()
  .sort({año: -1, rating: -1})
  .limit(5);
```

### Lección Aprendida

Los **operadores de MongoDB** (`$gt`, `$in`, `$or`, etc.) permiten queries complejas sin necesidad de JOINs. Los arrays son nativamente consultables.

---

## Ejemplo 3: Documentos Anidados y Arrays - Nivel: Intermedio ⭐⭐

### Contexto

Trabajas para **BlogHub**, una plataforma de blogs. Los posts tienen comentarios anidados y tags, necesitas consultar y actualizar estas estructuras complejas.

### Datos

```javascript
use bloghub;

db.posts.insertMany([
  {
    titulo: "Introducción a MongoDB",
    autor: "Ana García",
    fecha: new Date("2024-01-15"),
    contenido: "MongoDB es una base de datos NoSQL...",
    tags: ["mongodb", "nosql", "tutorial"],
    likes: 45,
    comentarios: [
      {
        usuario: "Carlos",
        texto: "¡Excelente tutorial!",
        fecha: new Date("2024-01-16"),
        likes: 3
      },
      {
        usuario: "María",
        texto: "Muy útil, gracias",
        fecha: new Date("2024-01-17"),
        likes: 1
      }
    ],
    estadisticas: {
      visitas: 1250,
      compartidos: 23,
      guardados: 8
    }
  },
  {
    titulo: "Python para Data Engineering",
    autor: "Bob Smith",
    fecha: new Date("2024-01-20"),
    contenido: "Python es el lenguaje #1 para datos...",
    tags: ["python", "data-engineering", "pandas"],
    likes: 89,
    comentarios: [
      {
        usuario: "Laura",
        texto: "Me ayudó mucho",
        fecha: new Date("2024-01-21"),
        likes: 5
      }
    ],
    estadisticas: {
      visitas: 2100,
      compartidos: 45,
      guardados: 15
    }
  }
]);
```

### Consultas en Documentos Anidados

**1. Posts con más de 1000 visitas**
```javascript
db.posts.find({
  "estadisticas.visitas": {$gt: 1000}
}, {titulo: 1, "estadisticas.visitas": 1});
```

**2. Posts con tag específico**
```javascript
db.posts.find({
  tags: "mongodb"
}, {titulo: 1, tags: 1});
```

**3. Posts con múltiples tags**
```javascript
db.posts.find({
  tags: {$all: ["python", "pandas"]}  // Tiene AMBOS tags
}, {titulo: 1, tags: 1});
```

**4. Posts con comentarios de un usuario**
```javascript
db.posts.find({
  "comentarios.usuario": "Carlos"
}, {titulo: 1, "comentarios.$": 1});  // $ proyecta solo el comentario que coincide
```

**5. Posts con al menos un comentario con >2 likes**
```javascript
db.posts.find({
  "comentarios.likes": {$gt: 2}
}, {titulo: 1, comentarios: 1});
```

### Actualizaciones en Arrays

**1. Agregar nuevo comentario**
```javascript
db.posts.updateOne(
  {titulo: "Introducción a MongoDB"},
  {
    $push: {
      comentarios: {
        usuario: "Pedro",
        texto: "Muy claro",
        fecha: new Date(),
        likes: 0
      }
    }
  }
);
```

**2. Incrementar likes de un post**
```javascript
db.posts.updateOne(
  {titulo: "Python para Data Engineering"},
  {$inc: {likes: 1, "estadisticas.visitas": 1}}
);
```

**3. Agregar tag (sin duplicados)**
```javascript
db.posts.updateOne(
  {titulo: "Introducción a MongoDB"},
  {$addToSet: {tags: "beginner"}}  // Solo agrega si no existe
);
```

**4. Eliminar tag**
```javascript
db.posts.updateOne(
  {titulo: "Python para Data Engineering"},
  {$pull: {tags: "pandas"}}  // Elimina del array
);
```

**5. Actualizar comentario específico**
```javascript
db.posts.updateOne(
  {
    titulo: "Introducción a MongoDB",
    "comentarios.usuario": "Carlos"
  },
  {
    $inc: {"comentarios.$.likes": 1}  // $ = elemento que coincide con filtro
  }
);
```

### Consultas con $elemMatch

```javascript
// Posts con comentario de "Carlos" con >2 likes
db.posts.find({
  comentarios: {
    $elemMatch: {
      usuario: "Carlos",
      likes: {$gt: 2}
    }
  }
});
```

### Lección Aprendida

MongoDB permite **almacenar datos jerárquicos** directamente sin necesidad de JOINs. Los operadores `$push`, `$pull`, `$addToSet` facilitan trabajar con arrays.

---

## Ejemplo 4: Agregaciones Básicas - Nivel: Avanzado ⭐⭐⭐

### Contexto

Trabajas para **EcommerceX**, un marketplace. Necesitas generar reportes de ventas por categoría, producto top, y estadísticas.

### Datos

```javascript
use ecommercex;

db.ventas.insertMany([
  {
    fecha: new Date("2024-01-10"),
    producto: "Laptop Pro",
    categoria: "electrónica",
    cantidad: 2,
    precio_unitario: 1200,
    cliente: "Ana",
    ciudad: "Madrid"
  },
  {
    fecha: new Date("2024-01-10"),
    producto: "Mouse",
    categoria: "accesorios",
    cantidad: 5,
    precio_unitario: 25,
    cliente: "Carlos",
    ciudad: "Barcelona"
  },
  {
    fecha: new Date("2024-01-11"),
    producto: "Teclado",
    categoria: "accesorios",
    cantidad: 3,
    precio_unitario: 80,
    cliente: "María",
    ciudad: "Madrid"
  },
  {
    fecha: new Date("2024-01-11"),
    producto: "Laptop Pro",
    categoria: "electrónica",
    cantidad: 1,
    precio_unitario: 1200,
    cliente: "Pedro",
    ciudad: "Valencia"
  },
  {
    fecha: new Date("2024-01-12"),
    producto: "Monitor 4K",
    categoria: "electrónica",
    cantidad: 2,
    precio_unitario: 450,
    cliente: "Laura",
    ciudad: "Madrid"
  }
]);
```

### Agregación 1: Total de ventas por categoría

```javascript
db.ventas.aggregate([
  {
    $group: {
      _id: "$categoria",
      total_ventas: {
        $sum: {$multiply: ["$cantidad", "$precio_unitario"]}
      },
      num_transacciones: {$sum: 1}
    }
  },
  {
    $sort: {total_ventas: -1}
  }
]);
```

**Output**:
```javascript
[
  {_id: "electrónica", total_ventas: 4200, num_transacciones: 3},
  {_id: "accesorios", total_ventas: 365, num_transacciones: 2}
]
```

### Agregación 2: Producto más vendido

```javascript
db.ventas.aggregate([
  {
    $group: {
      _id: "$producto",
      cantidad_total: {$sum: "$cantidad"},
      ingresos: {$sum: {$multiply: ["$cantidad", "$precio_unitario"]}}
    }
  },
  {
    $sort: {cantidad_total: -1}
  },
  {
    $limit: 1
  }
]);
```

**Output**:
```javascript
[
  {_id: "Mouse", cantidad_total: 5, ingresos: 125}
]
```

### Agregación 3: Ventas por ciudad

```javascript
db.ventas.aggregate([
  {
    $group: {
      _id: "$ciudad",
      total: {$sum: {$multiply: ["$cantidad", "$precio_unitario"]}},
      clientes_unicos: {$addToSet: "$cliente"}
    }
  },
  {
    $project: {
      ciudad: "$_id",
      total: 1,
      num_clientes: {$size: "$clientes_unicos"},
      _id: 0
    }
  }
]);
```

**Output**:
```javascript
[
  {ciudad: "Madrid", total: 3540, num_clientes: 3},
  {ciudad: "Barcelona", total: 125, num_clientes: 1},
  {ciudad: "Valencia", total: 1200, num_clientes: 1}
]
```

### Agregación 4: Estadísticas de precios

```javascript
db.ventas.aggregate([
  {
    $group: {
      _id: null,  // Agrupar todo
      precio_promedio: {$avg: "$precio_unitario"},
      precio_max: {$max: "$precio_unitario"},
      precio_min: {$min: "$precio_unitario"},
      total_productos_vendidos: {$sum: "$cantidad"}
    }
  }
]);
```

**Output**:
```javascript
[
  {
    _id: null,
    precio_promedio: 591,
    precio_max: 1200,
    precio_min: 25,
    total_productos_vendidos: 13
  }
]
```

### Lección Aprendida

El **aggregation pipeline** de MongoDB es extremadamente poderoso para análisis de datos, similar a `GROUP BY` en SQL pero mucho más flexible.

---

## Ejemplo 5: Pipeline de Agregación Complejo - Nivel: Avanzado ⭐⭐⭐

### Contexto

Trabajas para **SocialNet**, una red social. Necesitas generar un reporte complejo: usuarios más activos por país, con sus estadísticas de posts y engagement.

### Datos

```javascript
use socialnet;

db.usuarios.insertMany([
  {
    _id: 1,
    nombre: "Ana",
    pais: "España",
    ciudad: "Madrid",
    fecha_registro: new Date("2023-01-15"),
    seguidores: 1200,
    siguiendo: 450
  },
  {
    _id: 2,
    nombre: "Carlos",
    pais: "España",
    ciudad: "Barcelona",
    fecha_registro: new Date("2023-03-20"),
    seguidores: 850,
    siguiendo: 320
  },
  {
    _id: 3,
    nombre: "María",
    pais: "México",
    ciudad: "CDMX",
    fecha_registro: new Date("2023-02-10"),
    seguidores: 2500,
    siguiendo: 180
  }
]);

db.posts.insertMany([
  {usuario_id: 1, likes: 45, comentarios: 12, compartidos: 5, fecha: new Date("2024-01-10")},
  {usuario_id: 1, likes: 89, comentarios: 23, compartidos: 8, fecha: new Date("2024-01-12")},
  {usuario_id: 2, likes: 34, comentarios: 7, compartidos: 2, fecha: new Date("2024-01-11")},
  {usuario_id: 2, likes: 56, comentarios: 15, compartidos: 4, fecha: new Date("2024-01-13")},
  {usuario_id: 3, likes: 234, comentarios: 67, compartarios: 23, fecha: new Date("2024-01-11")},
  {usuario_id: 3, likes: 189, comentarios: 45, compartidos: 15, fecha: new Date("2024-01-14")}
]);
```

### Pipeline Complejo: Reporte de Usuarios Activos

```javascript
db.posts.aggregate([
  // Stage 1: Calcular engagement total por post
  {
    $addFields: {
      engagement: {
        $add: ["$likes", "$comentarios", {$multiply: ["$compartidos", 2]}]
      }
    }
  },

  // Stage 2: Agrupar por usuario
  {
    $group: {
      _id: "$usuario_id",
      total_posts: {$sum: 1},
      total_likes: {$sum: "$likes"},
      total_comentarios: {$sum: "$comentarios"},
      total_compartidos: {$sum: "$compartidos"},
      engagement_promedio: {$avg: "$engagement"},
      mejor_post_likes: {$max: "$likes"}
    }
  },

  // Stage 3: JOIN con usuarios (lookup)
  {
    $lookup: {
      from: "usuarios",
      localField: "_id",
      foreignField: "_id",
      as: "usuario_info"
    }
  },

  // Stage 4: Desempaquetar array de lookup
  {
    $unwind: "$usuario_info"
  },

  // Stage 5: Proyectar campos finales
  {
    $project: {
      _id: 0,
      nombre: "$usuario_info.nombre",
      pais: "$usuario_info.pais",
      ciudad: "$usuario_info.ciudad",
      seguidores: "$usuario_info.seguidores",
      estadisticas: {
        posts: "$total_posts",
        likes: "$total_likes",
        comentarios: "$total_comentarios",
        compartidos: "$total_compartidos",
        engagement_promedio: {$round: ["$engagement_promedio", 2]},
        mejor_post: "$mejor_post_likes"
      },
      ratio_engagement: {
        $round: [
          {$divide: ["$engagement_promedio", "$usuario_info.seguidores"]},
          4
        ]
      }
    }
  },

  // Stage 6: Ordenar por engagement
  {
    $sort: {"estadisticas.engagement_promedio": -1}
  }
]);
```

**Output**:
```javascript
[
  {
    nombre: "María",
    pais: "México",
    ciudad: "CDMX",
    seguidores: 2500,
    estadisticas: {
      posts: 2,
      likes: 423,
      comentarios: 112,
      compartidos: 38,
      engagement_promedio: 305.5,
      mejor_post: 234
    },
    ratio_engagement: 0.1222
  },
  {
    nombre: "Ana",
    pais: "España",
    ciudad: "Madrid",
    seguidores: 1200,
    estadisticas: {
      posts: 2,
      likes: 134,
      comentarios: 35,
      compartidos: 13,
      engagement_promedio: 104,
      mejor_post: 89
    },
    ratio_engagement: 0.0867
  },
  ...
]
```

### Pipeline Alternativo: Top 3 Usuarios por País

```javascript
db.posts.aggregate([
  {$group: {
    _id: "$usuario_id",
    total_engagement: {
      $sum: {$add: ["$likes", "$comentarios", {$multiply: ["$compartidos", 2]}]}
    }
  }},
  {$lookup: {
    from: "usuarios",
    localField: "_id",
    foreignField: "_id",
    as: "usuario"
  }},
  {$unwind: "$usuario"},
  {$group: {
    _id: "$usuario.pais",
    usuarios: {
      $push: {
        nombre: "$usuario.nombre",
        engagement: "$total_engagement"
      }
    }
  }},
  {$project: {
    pais: "$_id",
    top_usuarios: {$slice: [{$sortArray: {input: "$usuarios", sortBy: {engagement: -1}}}, 3]}
  }}
]);
```

### Lección Aprendida

MongoDB permite **pipelines complejos** con múltiples stages (`$group`, `$lookup`, `$project`, `$sort`) que pueden reemplazar JOINs y agregaciones de SQL, con la ventaja de trabajar con documentos flexibles.

---

## Resumen de los 5 Ejemplos

| Ejemplo | Concepto Principal | Dificultad | Caso de Uso |
|---------|-------------------|------------|-------------|
| 1 | CRUD Básico | ⭐ | Catálogo de productos flexible |
| 2 | Operadores de Query | ⭐⭐ | Búsqueda y filtrado avanzado |
| 3 | Documentos Anidados | ⭐⭐ | Datos jerárquicos (posts + comentarios) |
| 4 | Agregaciones Básicas | ⭐⭐⭐ | Reportes de ventas |
| 5 | Pipeline Complejo | ⭐⭐⭐ | Analytics de usuarios (JOIN + agregación) |

**¡Continúa con los ejercicios en `03-EJERCICIOS.md`!** 🚀
