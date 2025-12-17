# Ejercicios Prácticos: MongoDB

Este documento contiene 15 ejercicios progresivos para dominar MongoDB.

**Distribución**:
- Básicos (⭐): Ejercicios 1-6
- Intermedios (⭐⭐): Ejercicios 7-12
- Avanzados (⭐⭐⭐): Ejercicios 13-15

---

## Ejercicios Básicos

### Ejercicio 1: Crear e Insertar Documentos
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **FitHub**, un gimnasio. Necesitan una base de datos de miembros.

**Tarea**:
1. Crea una base de datos `fithub`
2. Inserta 3 miembros con estos campos:
   - `nombre` (string)
   - `edad` (número)
   - `tipo_membresia` (string: "básica", "premium", "vip")
   - `fecha_inscripcion` (fecha)
   - `clases_favoritas` (array de strings)

**Pista**: Usa `insertMany()` y `new Date()` para fechas.

---

### Ejercicio 2: Consultas Simples
**Dificultad**: ⭐ Fácil

**Contexto**:
Continúas en **FitHub**. Necesitas consultar miembros.

**Datos** (ejecuta primero):
```javascript
db.miembros.insertMany([
  {nombre: "Ana", edad: 28, tipo_membresia: "premium", activo: true},
  {nombre: "Carlos", edad: 35, tipo_membresia: "básica", activo: true},
  {nombre: "María", edad: 42, tipo_membresia: "vip", activo: false},
  {nombre: "Pedro", edad: 31, tipo_membresia: "premium", activo: true}
]);
```

**Tarea**:
Escribe queries para:
1. Todos los miembros activos
2. Miembros con membresía "premium"
3. Miembros mayores de 30 años
4. Un solo miembro llamado "Ana"

**Pista**: Usa `find()` con filtros.

---

### Ejercicio 3: Actualizar Documentos
**Dificultad**: ⭐ Fácil

**Contexto**:
En **FitHub**, necesitas actualizar información de miembros.

**Datos**: Usa los datos del Ejercicio 2.

**Tarea**:
1. Actualiza la edad de "Ana" a 29
2. Cambia el tipo de membresía de "Carlos" a "premium"
3. Marca a "María" como activa (`activo: true`)
4. Incrementa la edad de todos los miembros mayores de 30 en 1 año

**Pista**: Usa `updateOne()` para individual, `updateMany()` para múltiples, y `$inc` para incrementar.

---

### Ejercicio 4: Eliminar Documentos
**Dificultad**: ⭐ Fácil

**Contexto**:
**FitHub** necesita limpiar registros inactivos.

**Datos**: Usa los datos del Ejercicio 2.

**Tarea**:
1. Elimina a "María" (membresía vip inactiva)
2. Cuenta cuántos miembros quedan

**Pista**: Usa `deleteOne()` y `countDocuments()`.

---

### Ejercicio 5: Operadores de Comparación
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **Librería Digital**, una tienda de eBooks.

**Datos**:
```javascript
db.libros.insertMany([
  {titulo: "1984", autor: "George Orwell", precio: 12.99, paginas: 328, año: 1949},
  {titulo: "Clean Code", autor: "Robert Martin", precio: 45.00, paginas: 464, año: 2008},
  {titulo: "Python Crash Course", autor: "Eric Matthes", precio: 39.95, paginas: 544, año: 2019},
  {titulo: "The Hobbit", autor: "J.R.R. Tolkien", precio: 15.99, paginas: 310, año: 1937}
]);
```

**Tarea**:
Encuentra:
1. Libros con precio menor a $20
2. Libros con más de 400 páginas
3. Libros publicados después del año 2000
4. Libros que cuesten entre $10 y $40 (inclusive)

**Pista**: Usa `$lt`, `$gt`, `$gte`, `$lte`.

---

### Ejercicio 6: Trabajar con Arrays
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **RecipeBox**, una app de recetas.

**Datos**:
```javascript
db.recetas.insertMany([
  {
    nombre: "Pasta Carbonara",
    ingredientes: ["pasta", "huevos", "bacon", "queso parmesano"],
    tiempo_min: 20,
    dificultad: "fácil"
  },
  {
    nombre: "Paella",
    ingredientes: ["arroz", "pollo", "mariscos", "azafrán", "guisantes"],
    tiempo_min: 60,
    dificultad: "intermedia"
  },
  {
    nombre: "Ensalada César",
    ingredientes: ["lechuga", "pollo", "queso parmesano", "crutones"],
    tiempo_min: 15,
    dificultad: "fácil"
  }
]);
```

**Tarea**:
1. Encuentra recetas que contengan "queso parmesano"
2. Encuentra recetas con tiempo menor a 30 minutos
3. Agrega "sal" a los ingredientes de "Paella"
4. Cuenta cuántas recetas tienen dificultad "fácil"

**Pista**: Para buscar en arrays, simplemente usa el campo. Para agregar usa `$push`.

---

## Ejercicios Intermedios

### Ejercicio 7: Operadores Lógicos
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **GameStore**, una tienda de videojuegos.

**Datos**:
```javascript
db.juegos.insertMany([
  {titulo: "The Witcher 3", genero: "RPG", precio: 39.99, rating: 9.3, año: 2015},
  {titulo: "FIFA 24", genero: "Deportes", precio: 59.99, rating: 7.5, año: 2023},
  {titulo: "Minecraft", genero: "Sandbox", precio: 26.95, rating: 9.0, año: 2011},
  {titulo: "Cyberpunk 2077", genero: "RPG", precio: 49.99, rating: 7.8, año: 2020},
  {titulo: "Stardew Valley", genero: "Simulación", precio: 14.99, rating: 9.1, año: 2016}
]);
```

**Tarea**:
Encuentra juegos que cumplan:
1. Género "RPG" **O** rating mayor a 9.0
2. Precio menor a $30 **Y** rating mayor a 8.5
3. Año entre 2015 y 2020 (inclusive) **Y** precio mayor a $30
4. **NO** sean del género "Deportes" **Y** tengan rating mayor a 8.0

**Pista**: Usa `$or`, `$and`, `$ne`.

---

### Ejercicio 8: Documentos Anidados
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **RealEstate**, una inmobiliaria.

**Datos**:
```javascript
db.propiedades.insertMany([
  {
    direccion: "Calle Mayor 123",
    ciudad: "Madrid",
    tipo: "apartamento",
    precio: 250000,
    caracteristicas: {
      habitaciones: 3,
      baños: 2,
      metros_cuadrados: 95,
      terraza: true
    },
    agente: {
      nombre: "Ana López",
      telefono: "+34 600 111 222"
    }
  },
  {
    direccion: "Avenida Libertad 45",
    ciudad: "Barcelona",
    tipo: "casa",
    precio: 450000,
    caracteristicas: {
      habitaciones: 4,
      baños: 3,
      metros_cuadrados: 150,
      jardin: true
    },
    agente: {
      nombre: "Carlos Ruiz",
      telefono: "+34 600 333 444"
    }
  }
]);
```

**Tarea**:
1. Encuentra propiedades con más de 2 baños
2. Encuentra propiedades con terraza
3. Encuentra propiedades del agente "Ana López"
4. Actualiza el precio de la propiedad en "Calle Mayor 123" a 240,000
5. Incrementa el número de habitaciones de todas las propiedades en Barcelona en 1

**Pista**: Para acceder a campos anidados usa notación de punto: `"caracteristicas.baños"`.

---

### Ejercicio 9: Proyecciones y Ordenamiento
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **JobBoard**, una bolsa de trabajo.

**Datos**:
```javascript
db.ofertas.insertMany([
  {
    titulo: "Data Engineer",
    empresa: "TechCorp",
    salario: 55000,
    ubicacion: "Madrid",
    experiencia_años: 3,
    remoto: true
  },
  {
    titulo: "Python Developer",
    empresa: "StartupXYZ",
    salario: 45000,
    ubicacion: "Barcelona",
    experiencia_años: 2,
    remoto: false
  },
  {
    titulo: "Senior Data Engineer",
    empresa: "DataCo",
    salario: 75000,
    ubicacion: "Madrid",
    experiencia_años: 5,
    remoto: true
  },
  {
    titulo: "Backend Developer",
    empresa: "WebServices",
    salario: 50000,
    ubicacion: "Valencia",
    experiencia_años: 3,
    remoto: true
  }
]);
```

**Tarea**:
1. Muestra solo título y salario de todas las ofertas (sin `_id`)
2. Encuentra las 2 ofertas con mayor salario (ordenadas descendente)
3. Encuentra ofertas en Madrid, mostrando solo título, empresa y si es remoto
4. Lista todas las ofertas ordenadas por experiencia requerida (ascendente) y luego por salario (descendente)

**Pista**: Usa segundo parámetro de `find()` para proyección, `.sort()` para ordenar, `.limit()` para limitar.

---

### Ejercicio 10: Actualizar Arrays
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **TaskManager**, una app de tareas.

**Datos**:
```javascript
db.proyectos.insertMany([
  {
    nombre: "Sitio Web Corporativo",
    estado: "en_progreso",
    tareas: ["Diseño", "Frontend", "Backend"],
    equipo: ["Ana", "Carlos"]
  },
  {
    nombre: "App Móvil",
    estado: "planificación",
    tareas: ["Wireframes", "UI/UX"],
    equipo: ["María"]
  }
]);
```

**Tarea**:
1. Agrega "Testing" a las tareas del proyecto "Sitio Web Corporativo"
2. Agrega "Pedro" al equipo del proyecto "App Móvil"
3. Elimina "Frontend" de las tareas del "Sitio Web Corporativo"
4. Agrega "Deployment" a las tareas del "Sitio Web Corporativo" (solo si no existe ya)

**Pista**: Usa `$push`, `$pull`, `$addToSet`.

---

### Ejercicio 11: Queries con $elemMatch
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **UniversityDB**, una base de datos universitaria.

**Datos**:
```javascript
db.estudiantes.insertMany([
  {
    nombre: "Ana",
    carrera: "Ingeniería Informática",
    calificaciones: [
      {asignatura: "Matemáticas", nota: 8.5},
      {asignatura: "Programación", nota: 9.0},
      {asignatura: "Física", nota: 7.0}
    ]
  },
  {
    nombre: "Carlos",
    carrera: "Data Science",
    calificaciones: [
      {asignatura: "Estadística", nota: 9.5},
      {asignatura: "Machine Learning", nota: 8.8},
      {asignatura: "Python", nota: 9.2}
    ]
  }
]);
```

**Tarea**:
1. Encuentra estudiantes que tienen una calificación en "Programación" mayor a 8.5
2. Encuentra estudiantes con al menos una nota mayor o igual a 9.5
3. Actualiza la nota de "Matemáticas" de Ana a 9.0

**Pista**: Usa `$elemMatch` para condiciones complejas en arrays de objetos. Para actualizar usa `$` posicional.

---

### Ejercicio 12: Operador $exists y tipos
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Trabajas para **CustomerDB**, actualizando base de datos de clientes.

**Datos**:
```javascript
db.clientes.insertMany([
  {nombre: "Ana", email: "ana@example.com", telefono: "+34600111222", vip: true},
  {nombre: "Carlos", email: "carlos@example.com", vip: false},
  {nombre: "María", telefono: "+34600333444", newsletter: true},
  {nombre: "Pedro", email: "pedro@example.com"}
]);
```

**Tarea**:
1. Encuentra clientes que **tienen** campo `telefono`
2. Encuentra clientes que **no tienen** campo `email`
3. Encuentra clientes VIP (campo `vip` es `true`)
4. Agrega `newsletter: false` a todos los clientes que no tienen ese campo

**Pista**: Usa `$exists` para verificar si campo existe.

---

## Ejercicios Avanzados

### Ejercicio 13: Agregaciones con $group
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **RetailChain**, una cadena de tiendas. Necesitas reportes de ventas.

**Datos**:
```javascript
db.transacciones.insertMany([
  {fecha: new Date("2024-01-10"), tienda: "Madrid Centro", categoria: "Electrónica", monto: 1200, productos_vendidos: 2},
  {fecha: new Date("2024-01-10"), tienda: "Barcelona Norte", categoria: "Ropa", monto: 450, productos_vendidos: 5},
  {fecha: new Date("2024-01-11"), tienda: "Madrid Centro", categoria: "Electrónica", monto: 800, productos_vendidos: 1},
  {fecha: new Date("2024-01-11"), tienda: "Madrid Centro", categoria: "Hogar", monto: 350, productos_vendidos: 3},
  {fecha: new Date("2024-01-12"), tienda: "Barcelona Norte", categoria: "Electrónica", monto: 950, productos_vendidos: 2},
  {fecha: new Date("2024-01-12"), tienda: "Valencia Sur", categoria: "Ropa", monto: 280, productos_vendidos: 4}
]);
```

**Tarea**:
Crea agregaciones para obtener:
1. **Total de ventas por tienda** (suma de `monto`)
2. **Total de productos vendidos por categoría**
3. **Venta promedio por categoría** (promedio de `monto`)
4. **Tienda con más transacciones**

**Pista**: Usa `aggregate()` con `$group`, `$sum`, `$avg`, `$count`.

---

### Ejercicio 14: Pipeline de Agregación con $lookup
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **LibraryApp**, necesitas unir datos de libros con sus préstamos.

**Datos**:
```javascript
db.libros.insertMany([
  {_id: 1, titulo: "1984", autor: "George Orwell", categoria: "Ficción"},
  {_id: 2, titulo: "Clean Code", autor: "Robert Martin", categoria: "Técnico"},
  {_id: 3, titulo: "Sapiens", autor: "Yuval Harari", categoria: "Historia"}
]);

db.prestamos.insertMany([
  {libro_id: 1, usuario: "Ana", fecha: new Date("2024-01-10"), devuelto: true},
  {libro_id: 1, usuario: "Carlos", fecha: new Date("2024-01-15"), devuelto: false},
  {libro_id: 2, usuario: "María", fecha: new Date("2024-01-12"), devuelto: true},
  {libro_id: 1, usuario: "Pedro", fecha: new Date("2024-01-18"), devuelto: false}
]);
```

**Tarea**:
Crea un pipeline que:
1. Una libros con sus préstamos (usando `$lookup`)
2. Cuente cuántos préstamos tiene cada libro
3. Muestre: título, autor, total de préstamos
4. Ordene por total de préstamos descendente

**Pista**: Usa `$lookup` para JOIN, `$unwind` para desempaquetar array, `$group` para contar.

---

### Ejercicio 15: Pipeline Complejo con Múltiples Stages
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Trabajas para **E-Learning Platform**. Necesitas un reporte de cursos más populares por categoría con estadísticas.

**Datos**:
```javascript
db.cursos.insertMany([
  {_id: 1, titulo: "Python Básico", categoria: "Programación", instructor: "Ana", precio: 49},
  {_id: 2, titulo: "Data Science", categoria: "Data", instructor: "Carlos", precio: 99},
  {_id: 3, titulo: "JavaScript Avanzado", categoria: "Programación", instructor: "María", precio: 79},
  {_id: 4, titulo: "Machine Learning", categoria: "Data", instructor: "Ana", precio: 129}
]);

db.inscripciones.insertMany([
  {curso_id: 1, estudiante: "User1", rating: 4.5, completado: true},
  {curso_id: 1, estudiante: "User2", rating: 5.0, completado: true},
  {curso_id: 2, estudiante: "User3", rating: 4.8, completado: false},
  {curso_id: 2, estudiante: "User4", rating: 4.9, completado: true},
  {curso_id: 3, estudiante: "User5", rating: 4.2, completado: true},
  {curso_id: 4, estudiante: "User6", rating: 5.0, completado: true},
  {curso_id: 4, estudiante: "User7", rating: 4.7, completado: true}
]);
```

**Tarea**:
Crea un reporte que muestre para cada categoría:
- Número de cursos
- Total de estudiantes inscritos
- Rating promedio
- Ingresos totales (estudiantes × precio)
- Curso más popular (el que tiene más inscripciones)

**Pista**: Necesitarás `$lookup`, `$group`, `$project`, `$sort`, y posiblemente `$addFields`.

---

## Soluciones

### Solución Ejercicio 1

```javascript
use fithub;

db.miembros.insertMany([
  {
    nombre: "Ana García",
    edad: 28,
    tipo_membresia: "premium",
    fecha_inscripcion: new Date("2024-01-15"),
    clases_favoritas: ["yoga", "spinning", "pilates"]
  },
  {
    nombre: "Carlos López",
    edad: 35,
    tipo_membresia: "básica",
    fecha_inscripcion: new Date("2023-11-20"),
    clases_favoritas: ["crossfit", "boxeo"]
  },
  {
    nombre: "María Rodríguez",
    edad: 42,
    tipo_membresia: "vip",
    fecha_inscripcion: new Date("2023-08-10"),
    clases_favoritas: ["yoga", "zumba", "natación"]
  }
]);
```

---

### Solución Ejercicio 2

```javascript
// 1. Todos los miembros activos
db.miembros.find({activo: true});

// 2. Miembros con membresía "premium"
db.miembros.find({tipo_membresia: "premium"});

// 3. Miembros mayores de 30 años
db.miembros.find({edad: {$gt: 30}});

// 4. Un solo miembro llamado "Ana"
db.miembros.findOne({nombre: "Ana"});
```

---

### Solución Ejercicio 3

```javascript
// 1. Actualizar edad de Ana
db.miembros.updateOne(
  {nombre: "Ana"},
  {$set: {edad: 29}}
);

// 2. Cambiar membresía de Carlos
db.miembros.updateOne(
  {nombre: "Carlos"},
  {$set: {tipo_membresia: "premium"}}
);

// 3. Marcar a María como activa
db.miembros.updateOne(
  {nombre: "María"},
  {$set: {activo: true}}
);

// 4. Incrementar edad de mayores de 30
db.miembros.updateMany(
  {edad: {$gt: 30}},
  {$inc: {edad: 1}}
);
```

---

### Solución Ejercicio 4

```javascript
// 1. Eliminar a María
db.miembros.deleteOne({nombre: "María"});

// 2. Contar miembros restantes
db.miembros.countDocuments();
// Resultado: 3
```

---

### Solución Ejercicio 5

```javascript
// 1. Libros con precio menor a $20
db.libros.find({precio: {$lt: 20}});

// 2. Libros con más de 400 páginas
db.libros.find({paginas: {$gt: 400}});

// 3. Libros publicados después del año 2000
db.libros.find({año: {$gt: 2000}});

// 4. Libros entre $10 y $40
db.libros.find({
  precio: {$gte: 10, $lte: 40}
});
```

---

### Solución Ejercicio 6

```javascript
// 1. Recetas con queso parmesano
db.recetas.find({ingredientes: "queso parmesano"});

// 2. Recetas con tiempo < 30 min
db.recetas.find({tiempo_min: {$lt: 30}});

// 3. Agregar "sal" a Paella
db.recetas.updateOne(
  {nombre: "Paella"},
  {$push: {ingredientes: "sal"}}
);

// 4. Contar recetas fáciles
db.recetas.countDocuments({dificultad: "fácil"});
// Resultado: 2
```

---

### Solución Ejercicio 7

```javascript
// 1. RPG O rating > 9.0
db.juegos.find({
  $or: [
    {genero: "RPG"},
    {rating: {$gt: 9.0}}
  ]
});

// 2. Precio < $30 Y rating > 8.5
db.juegos.find({
  precio: {$lt: 30},
  rating: {$gt: 8.5}
});

// 3. Año 2015-2020 Y precio > $30
db.juegos.find({
  año: {$gte: 2015, $lte: 2020},
  precio: {$gt: 30}
});

// 4. NO Deportes Y rating > 8.0
db.juegos.find({
  genero: {$ne: "Deportes"},
  rating: {$gt: 8.0}
});
```

---

### Solución Ejercicio 8

```javascript
// 1. Propiedades con más de 2 baños
db.propiedades.find({"caracteristicas.baños": {$gt: 2}});

// 2. Propiedades con terraza
db.propiedades.find({"caracteristicas.terraza": true});

// 3. Propiedades del agente Ana López
db.propiedades.find({"agente.nombre": "Ana López"});

// 4. Actualizar precio en Calle Mayor
db.propiedades.updateOne(
  {direccion: "Calle Mayor 123"},
  {$set: {precio: 240000}}
);

// 5. Incrementar habitaciones en Barcelona
db.propiedades.updateMany(
  {ciudad: "Barcelona"},
  {$inc: {"caracteristicas.habitaciones": 1}}
);
```

---

### Solución Ejercicio 9

```javascript
// 1. Solo título y salario (sin _id)
db.ofertas.find({}, {titulo: 1, salario: 1, _id: 0});

// 2. Top 2 por salario
db.ofertas.find().sort({salario: -1}).limit(2);

// 3. Ofertas en Madrid (título, empresa, remoto)
db.ofertas.find(
  {ubicacion: "Madrid"},
  {titulo: 1, empresa: 1, remoto: 1, _id: 0}
);

// 4. Ordenar por experiencia (asc) y salario (desc)
db.ofertas.find().sort({experiencia_años: 1, salario: -1});
```

---

### Solución Ejercicio 10

```javascript
// 1. Agregar "Testing"
db.proyectos.updateOne(
  {nombre: "Sitio Web Corporativo"},
  {$push: {tareas: "Testing"}}
);

// 2. Agregar "Pedro" al equipo
db.proyectos.updateOne(
  {nombre: "App Móvil"},
  {$push: {equipo: "Pedro"}}
);

// 3. Eliminar "Frontend"
db.proyectos.updateOne(
  {nombre: "Sitio Web Corporativo"},
  {$pull: {tareas: "Frontend"}}
);

// 4. Agregar "Deployment" solo si no existe
db.proyectos.updateOne(
  {nombre: "Sitio Web Corporativo"},
  {$addToSet: {tareas: "Deployment"}}
);
```

---

### Solución Ejercicio 11

```javascript
// 1. Estudiantes con Programación > 8.5
db.estudiantes.find({
  calificaciones: {
    $elemMatch: {
      asignatura: "Programación",
      nota: {$gt: 8.5}
    }
  }
});

// 2. Estudiantes con al menos una nota >= 9.5
db.estudiantes.find({
  "calificaciones.nota": {$gte: 9.5}
});

// 3. Actualizar nota de Matemáticas de Ana
db.estudiantes.updateOne(
  {
    nombre: "Ana",
    "calificaciones.asignatura": "Matemáticas"
  },
  {
    $set: {"calificaciones.$.nota": 9.0}
  }
);
```

---

### Solución Ejercicio 12

```javascript
// 1. Clientes que tienen teléfono
db.clientes.find({telefono: {$exists: true}});

// 2. Clientes que NO tienen email
db.clientes.find({email: {$exists: false}});

// 3. Clientes VIP
db.clientes.find({vip: true});

// 4. Agregar newsletter: false si no existe
db.clientes.updateMany(
  {newsletter: {$exists: false}},
  {$set: {newsletter: false}}
);
```

---

### Solución Ejercicio 13

```javascript
// 1. Total de ventas por tienda
db.transacciones.aggregate([
  {
    $group: {
      _id: "$tienda",
      total_ventas: {$sum: "$monto"}
    }
  },
  {
    $sort: {total_ventas: -1}
  }
]);

// 2. Total productos vendidos por categoría
db.transacciones.aggregate([
  {
    $group: {
      _id: "$categoria",
      total_productos: {$sum: "$productos_vendidos"}
    }
  }
]);

// 3. Venta promedio por categoría
db.transacciones.aggregate([
  {
    $group: {
      _id: "$categoria",
      venta_promedio: {$avg: "$monto"}
    }
  }
]);

// 4. Tienda con más transacciones
db.transacciones.aggregate([
  {
    $group: {
      _id: "$tienda",
      num_transacciones: {$sum: 1}
    }
  },
  {
    $sort: {num_transacciones: -1}
  },
  {
    $limit: 1
  }
]);
```

---

### Solución Ejercicio 14

```javascript
db.libros.aggregate([
  // Stage 1: Lookup - unir con préstamos
  {
    $lookup: {
      from: "prestamos",
      localField: "_id",
      foreignField: "libro_id",
      as: "prestamos"
    }
  },

  // Stage 2: Agregar campo con conteo
  {
    $addFields: {
      total_prestamos: {$size: "$prestamos"}
    }
  },

  // Stage 3: Proyectar campos finales
  {
    $project: {
      _id: 0,
      titulo: 1,
      autor: 1,
      total_prestamos: 1
    }
  },

  // Stage 4: Ordenar
  {
    $sort: {total_prestamos: -1}
  }
]);
```

**Output**:
```javascript
[
  {titulo: "1984", autor: "George Orwell", total_prestamos: 3},
  {titulo: "Clean Code", autor: "Robert Martin", total_prestamos: 1},
  {titulo: "Sapiens", autor: "Yuval Harari", total_prestamos: 0}
]
```

---

### Solución Ejercicio 15

```javascript
db.inscripciones.aggregate([
  // Stage 1: Lookup - unir con cursos
  {
    $lookup: {
      from: "cursos",
      localField: "curso_id",
      foreignField: "_id",
      as: "curso_info"
    }
  },

  // Stage 2: Unwind curso_info
  {
    $unwind: "$curso_info"
  },

  // Stage 3: Group por categoría
  {
    $group: {
      _id: "$curso_info.categoria",
      num_cursos: {$addToSet: "$curso_id"},
      total_estudiantes: {$sum: 1},
      rating_promedio: {$avg: "$rating"},
      precios: {$push: "$curso_info.precio"},
      cursos_info: {
        $push: {
          curso_id: "$curso_id",
          titulo: "$curso_info.titulo"
        }
      }
    }
  },

  // Stage 4: Proyectar con cálculos
  {
    $project: {
      categoria: "$_id",
      num_cursos: {$size: "$num_cursos"},
      total_estudiantes: 1,
      rating_promedio: {$round: ["$rating_promedio", 2]},
      ingresos_totales: {
        $multiply: ["$total_estudiantes", {$avg: "$precios"}]
      },
      _id: 0
    }
  },

  // Stage 5: Ordenar por ingresos
  {
    $sort: {ingresos_totales: -1}
  }
]);
```

**Output** (aproximado):
```javascript
[
  {
    categoria: "Data",
    num_cursos: 2,
    total_estudiantes: 4,
    rating_promedio: 4.85,
    ingresos_totales: 456
  },
  {
    categoria: "Programación",
    num_cursos: 2,
    total_estudiantes: 3,
    rating_promedio: 4.57,
    ingresos_totales: 192
  }
]
```

---

## Resumen de Conceptos Practicados

### Ejercicios Básicos (1-6)
✅ CRUD (Create, Read, Update, Delete)
✅ Operadores de comparación (`$gt`, `$lt`, `$gte`, `$lte`)
✅ Trabajar con arrays básicos

### Ejercicios Intermedios (7-12)
✅ Operadores lógicos (`$or`, `$and`, `$ne`)
✅ Documentos anidados y notación de punto
✅ Proyecciones y ordenamiento
✅ Actualizar arrays (`$push`, `$pull`, `$addToSet`)
✅ Operador `$elemMatch`
✅ Operador `$exists`

### Ejercicios Avanzados (13-15)
✅ Agregaciones con `$group`
✅ Operadores de agregación (`$sum`, `$avg`)
✅ Pipeline de agregación con `$lookup` (JOIN)
✅ Pipeline complejo multi-stage

**¡Continúa con el proyecto práctico en `04-proyecto-practico/`!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
