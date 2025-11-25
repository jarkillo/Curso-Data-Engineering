# Ejercicios Prácticos: Modelado de Datos

## Ejercicios Básicos

### Ejercicio 1: Identificar Violaciones de 1NF ⭐

**Dificultad**: Fácil

**Contexto**:
**GymFit** tiene una tabla de socios con sus entrenamientos.

**Tabla actual**:
```
socios
id | nombre      | email             | entrenamientos_semana
1  | Pedro Ruiz  | pedro@email.com   | "Lunes: Pesas, Miércoles: Cardio, Viernes: Yoga"
2  | Laura Gómez | laura@email.com   | "Martes: Natación, Jueves: Spinning"
```

**Pregunta**:
1. ¿Esta tabla está en 1NF? ¿Por qué sí o por qué no?
2. Si no está en 1NF, ¿cómo la normalizarías?

**Hint**: Recuerda que 1NF requiere valores atómicos (un solo valor por celda).

---

### Ejercicio 2: Identificar Violaciones de 2NF ⭐

**Dificultad**: Fácil

**Contexto**:
**OnlineAcademy** tiene una tabla de inscripciones de estudiantes a cursos.

**Tabla actual**:
```sql
CREATE TABLE inscripciones (
    estudiante_id INTEGER,
    curso_id INTEGER,
    fecha_inscripcion DATE,
    nombre_curso VARCHAR(200),
    duracion_horas INTEGER,
    calificacion INTEGER,
    PRIMARY KEY (estudiante_id, curso_id)
);
```

**Datos ejemplo**:
```
estudiante_id | curso_id | fecha_inscripcion | nombre_curso          | duracion_horas | calificacion
1             | 101      | 2024-01-15        | Python Básico         | 40             | 85
1             | 102      | 2024-02-01        | SQL Intermedio        | 30             | 90
2             | 101      | 2024-01-20        | Python Básico         | 40             | 78
```

**Pregunta**:
1. ¿Esta tabla está en 2NF? ¿Por qué?
2. Identifica las columnas con dependencia parcial de la PK compuesta
3. Propón las tablas necesarias para alcanzar 2NF

**Hint**: 2NF requiere que columnas no-PK dependan de TODA la clave primaria, no solo de parte.

---

### Ejercicio 3: Identificar Cardinalidades ⭐

**Dificultad**: Fácil

**Contexto**:
**HospitalCare** está diseñando su base de datos.

**Relaciones del sistema**:
1. Un **paciente** puede tener muchas **citas**. Una cita pertenece a un paciente.
2. Un **doctor** puede atender muchas **citas**. Una cita es atendida por un doctor.
3. Un **doctor** puede tener muchas **especialidades** (ej: Cardiología + Medicina General). Una especialidad puede ser practicada por muchos doctores.
4. Un **paciente** tiene una **historia clínica**. Una historia clínica pertenece a un paciente.

**Pregunta**:
Para cada relación, identifica la cardinalidad:
- a) Paciente ↔ Citas
- b) Doctor ↔ Citas
- c) Doctor ↔ Especialidades
- d) Paciente ↔ Historia Clínica

**Opciones**: 1:1, 1:N, N:M

---

### Ejercicio 4: OLTP vs OLAP ⭐

**Dificultad**: Fácil

**Contexto**:
**BankCorp** está decidiendo cómo diseñar dos sistemas:
- **Sistema A**: App móvil de banca donde clientes hacen transferencias, consultan saldos, pagan servicios
- **Sistema B**: Dashboard de ejecutivos con reportes de "Total préstamos por región en 2024", "Clientes más rentables", etc.

**Pregunta**:
1. ¿Sistema A debe ser OLTP u OLAP? ¿Por qué?
2. ¿Sistema B debe ser OLTP u OLAP? ¿Por qué?
3. ¿Sistema A debe estar normalizado (3NF) o desnormalizado (Star Schema)?
4. ¿Sistema B debe estar normalizado (3NF) o desnormalizado (Star Schema)?

---

## Ejercicios Intermedios

### Ejercicio 5: Normalizar de 1NF a 3NF ⭐⭐

**Dificultad**: Intermedio

**Contexto**:
**RestaurantApp** tiene una tabla de órdenes que ya cumple 1NF pero no 2NF ni 3NF.

**Tabla actual (1NF)**:
```sql
CREATE TABLE ordenes_1nf (
    orden_id INTEGER PRIMARY KEY,
    cliente_nombre VARCHAR(200),
    cliente_email VARCHAR(150),
    cliente_ciudad VARCHAR(100),
    cliente_pais VARCHAR(100),
    producto_nombre VARCHAR(200),
    producto_categoria VARCHAR(100),
    producto_precio NUMERIC(6,2),
    cantidad INTEGER,
    fecha_orden TIMESTAMP
);
```

**Datos ejemplo**:
```
orden_id | cliente_nombre | cliente_email    | cliente_ciudad | cliente_pais | producto_nombre | producto_categoria | producto_precio | cantidad
1        | Ana Martínez   | ana@email.com    | Madrid         | España       | Hamburguesa     | Comida Rápida      | 8.50            | 2
2        | Ana Martínez   | ana@email.com    | Madrid         | España       | Coca-Cola       | Bebidas            | 2.50            | 1
3        | Carlos López   | carlos@email.com | Barcelona      | España       | Pizza Margherita| Pizza              | 12.00           | 1
```

**Pregunta**:
Diseña las tablas necesarias para alcanzar 3NF. Proporciona:
1. CREATE TABLE para cada tabla
2. Diagrama ER textual mostrando las relaciones
3. INSERT statements para los datos ejemplo

**Hint**: Identifica dependencias transitivas (cliente_ciudad → cliente_pais).

---

### Ejercicio 6: Diseñar Esquema ER con N:M ⭐⭐

**Dificultad**: Intermedio

**Contexto**:
**EventTickets** vende entradas para eventos.

**Requisitos**:
- Un **evento** (concierto, teatro, etc.) ocurre en una fecha y lugar específicos
- Un **cliente** puede comprar entradas para múltiples eventos
- Un evento puede tener múltiples clientes que compraron entradas
- Cada **compra** debe registrar: fecha de compra, cantidad de entradas, precio unitario pagado, asiento asignado
- Los eventos tienen información: nombre, fecha, ubicación, capacidad máxima, precio_base

**Pregunta**:
1. Diseña el esquema ER con todas las entidades y relaciones
2. Identifica las cardinalidades
3. Escribe los CREATE TABLE statements (incluye FKs y constraints)
4. ¿Necesitas tabla intermedia? ¿Por qué?

---

### Ejercicio 7: Identificar Dependencias Transitivas ⭐⭐

**Dificultad**: Intermedio

**Contexto**:
**EmployeeDB** tiene una tabla de empleados.

**Tabla actual (cumple 1NF y 2NF)**:
```sql
CREATE TABLE empleados (
    empleado_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200),
    email VARCHAR(150),
    departamento_id INTEGER,
    departamento_nombre VARCHAR(100),
    jefe_departamento VARCHAR(200),
    edificio VARCHAR(50)
);
```

**Datos ejemplo**:
```
empleado_id | nombre        | email             | dept_id | dept_nombre | jefe_dept      | edificio
1           | María López   | maria@co.com      | 10      | Ventas      | Carlos Ruiz    | Edificio A
2           | Pedro Gómez   | pedro@co.com      | 10      | Ventas      | Carlos Ruiz    | Edificio A
3           | Ana Martínez  | ana@co.com        | 20      | IT          | Laura García   | Edificio B
```

**Pregunta**:
1. Identifica TODAS las dependencias funcionales en esta tabla
2. ¿Cuáles son dependencias transitivas?
3. Diseña las tablas normalizadas en 3NF
4. Bonus: ¿Qué pasa si un departamento se muda de edificio? ¿Cuántos UPDATEs necesitas antes y después de normalizar?

---

### Ejercicio 8: Diseñar Dimensión Fecha ⭐⭐

**Dificultad**: Intermedio

**Contexto**:
Estás diseñando un Data Warehouse para **RetailCorp**. Necesitas una dimensión de fecha que permita análisis por:
- Día, mes, año, trimestre
- Día de la semana (para identificar patrones fin de semana)
- Festivos (para analizar ventas en días especiales)
- Semanas del año
- Nombre del mes en español

**Pregunta**:
1. Diseña la tabla `dim_fecha` con TODOS los campos necesarios
2. Escribe el CREATE TABLE con tipos de datos apropiados
3. Escribe la query INSERT que pobla esta tabla para el año 2024 (usa `generate_series` o equivalente)
4. ¿Qué debería ser la PK? ¿Un SERIAL o un formato especial? Justifica.

**Hint**: PK común es `fecha_id` con formato YYYYMMDD (ej: 20241115).

---

### Ejercicio 9: Star Schema Básico ⭐⭐

**Dificultad**: Intermedio

**Contexto**:
**VideoGameStore** vende videojuegos online. El equipo de analytics necesita responder:
- ¿Qué géneros de juegos venden más?
- ¿En qué plataforma (PS5, Xbox, PC) se vende más?
- ¿Qué países generan más ingresos?
- ¿Cuál es la venta promedio por día de la semana?

**Datos disponibles**:
- Cada **venta** tiene: fecha, cliente, juego vendido, plataforma, cantidad, precio unitario
- Cada **juego** tiene: título, género (RPG, FPS, Strategy), desarrollador, año lanzamiento
- Cada **cliente** tiene: nombre, email, país, fecha registro

**Pregunta**:
1. Diseña un Star Schema con:
   - Una tabla de hechos (fact table)
   - Al menos 3 dimensiones
2. Especifica qué métricas (measures) tendrá la tabla de hechos
3. Escribe los CREATE TABLE statements
4. Escribe una query analítica: "Total ventas por género en Q4 2024"

---

## Ejercicios Avanzados

### Ejercicio 10: Normalización Completa con Caso Real ⭐⭐⭐

**Dificultad**: Avanzado

**Contexto**:
**MedicalClinic** tiene actualmente esta tabla horrible que combina todo:

```sql
CREATE TABLE citas_denormalizadas (
    cita_id INTEGER PRIMARY KEY,
    fecha_cita TIMESTAMP,
    paciente_nombre VARCHAR(200),
    paciente_dni VARCHAR(20),
    paciente_email VARCHAR(150),
    paciente_ciudad VARCHAR(100),
    doctor_nombre VARCHAR(200),
    doctor_especialidades VARCHAR(500),  -- "Cardiología, Medicina General"
    diagnostico TEXT,
    medicamentos_recetados VARCHAR(1000),  -- "Ibuprofeno 600mg, Omeprazol 20mg"
    costo_consulta NUMERIC(6,2),
    seguro_nombre VARCHAR(100),
    seguro_cobertura_porcentaje INTEGER
);
```

**Problemas**:
- Datos de paciente repetidos en cada cita
- Datos de doctor repetidos
- `doctor_especialidades` y `medicamentos_recetados` violan 1NF
- Datos de seguro repetidos para cada paciente con el mismo seguro

**Pregunta**:
1. Diseña el esquema COMPLETO normalizado en 3NF con TODAS las tablas necesarias
2. Maneja correctamente:
   - La relación N:M entre Doctor y Especialidades
   - La relación N:M entre Cita y Medicamentos
   - La relación entre Paciente y Seguro (un paciente tiene un seguro, muchos pacientes pueden tener el mismo seguro)
3. Incluye constraints apropiados (NOT NULL, CHECK, UNIQUE donde corresponda)
4. Escribe una query que obtuviera los mismos datos que una fila de la tabla desnormalizada (requiere múltiples JOINs)

---

### Ejercicio 11: Star Schema con SCD Type 2 ⭐⭐⭐

**Dificultad**: Avanzado

**Contexto**:
**StreamingPlatform** (como Netflix) necesita un Data Warehouse para analizar:
- Ingresos mensuales por plan (Básico, Estándar, Premium)
- Retención de clientes
- Análisis de upgrades/downgrades de planes

**Requisitos especiales**:
- Los clientes cambian de plan frecuentemente (upgrade/downgrade)
- **Necesitas analizar histórico**: "¿Cuántos ingresos generó el plan Básico en Q1 2024?" debe incluir clientes que ENTONCES eran Básico, aunque ahora sean Premium
- Fact table registra ingresos mensuales

**Pregunta**:
1. Diseña un Star Schema con SCD Type 2 en la dimensión cliente:
   - Tabla de hechos: `fact_ingresos_mensuales`
   - Dimensión con SCD: `dim_cliente` (maneja cambios de plan históricos)
   - Otras dimensiones necesarias
2. Muestra el proceso completo cuando un cliente cambia de plan:
   - Estado inicial: Ana con plan Básico
   - Ana hace upgrade a Premium el 2024-07-01
   - Estado final: Dos versiones de Ana en `dim_cliente`
3. Escribe la query: "Ingresos por plan en Enero 2024" que correctamente usa el historial SCD

---

### Ejercicio 12: Snowflake Schema y Decisión de Diseño ⭐⭐⭐

**Dificultad**: Avanzado

**Contexto**:
**GlobalRetail** tiene 50,000 productos en 500 categorías que pertenecen a 20 super-categorías. Su Data Warehouse Star Schema actual tiene esta dimensión:

```sql
CREATE TABLE dim_producto (
    producto_id INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(200),
    subcategoria VARCHAR(100),
    categoria VARCHAR(100),
    super_categoria VARCHAR(100),
    marca VARCHAR(100),
    precio_lista NUMERIC(10,2)
);
```

**Datos ejemplo**:
```
producto_id | nombre_producto | subcategoria      | categoria    | super_categoria | marca
1001        | iPhone 15       | Smartphones       | Electrónica  | Tecnología      | Apple
1002        | AirPods Pro     | Auriculares       | Electrónica  | Tecnología      | Apple
1003        | Adidas Ultraboost| Zapatillas Running| Ropa Deportiva| Deportes       | Adidas
```

**Problema**: Con 50,000 productos, hay MUCHA redundancia en `categoria`, `super_categoria` y `marca`.

**Pregunta**:
1. **Diseña dos versiones**:
   - Versión A: Star Schema actual (desnormalizado)
   - Versión B: Snowflake Schema (normalizar categorías y marcas)

2. **Analiza trade-offs**:
   - Calcula la redundancia estimada de datos (filas duplicadas de categorías/marcas)
   - Compara número de JOINs para query: "Total ventas por super_categoría"
   - ¿Cuánto espacio ahorras con Snowflake? (estimación)

3. **Decisión final**: ¿Qué esquema recomiendas? Justifica considerando:
   - Performance de queries
   - Espacio en disco
   - Complejidad de queries para analistas
   - Facilidad de mantenimiento

4. **Implementación**: Escribe los CREATE TABLE de tu diseño recomendado

---

## Soluciones

### Solución Ejercicio 1

**Respuesta**:
1. ❌ **No está en 1NF** porque la columna `entrenamientos_semana` contiene múltiples valores (lista de entrenamientos) en una sola celda.

2. **Normalización a 1NF**:

```sql
-- Tabla: socios
CREATE TABLE socios (
    socio_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

-- Tabla: entrenamientos (relación 1:N)
CREATE TABLE entrenamientos (
    entrenamiento_id SERIAL PRIMARY KEY,
    socio_id INTEGER REFERENCES socios(socio_id),
    dia_semana VARCHAR(20) NOT NULL,
    tipo_entrenamiento VARCHAR(100) NOT NULL,
    CHECK (dia_semana IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'))
);

-- Datos:
INSERT INTO socios (nombre, email) VALUES
('Pedro Ruiz', 'pedro@email.com'),
('Laura Gómez', 'laura@email.com');

INSERT INTO entrenamientos (socio_id, dia_semana, tipo_entrenamiento) VALUES
(1, 'Lunes', 'Pesas'),
(1, 'Miércoles', 'Cardio'),
(1, 'Viernes', 'Yoga'),
(2, 'Martes', 'Natación'),
(2, 'Jueves', 'Spinning');
```

**✅ Ahora cumple 1NF**: Cada celda tiene un valor atómico.

---

### Solución Ejercicio 2

**Respuesta**:
1. ❌ **No está en 2NF** porque tiene dependencia parcial de la PK compuesta.

2. **Columnas con dependencia parcial**:
   - `nombre_curso` solo depende de `curso_id` (no de `estudiante_id`)
   - `duracion_horas` solo depende de `curso_id`

3. **Normalización a 2NF**:

```sql
-- Tabla: estudiantes
CREATE TABLE estudiantes (
    estudiante_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

-- Tabla: cursos (separa atributos que solo dependen de curso_id)
CREATE TABLE cursos (
    curso_id INTEGER PRIMARY KEY,
    nombre_curso VARCHAR(200) NOT NULL,
    duracion_horas INTEGER NOT NULL CHECK (duracion_horas > 0)
);

-- Tabla: inscripciones (solo columnas que dependen de AMBAS PKs)
CREATE TABLE inscripciones (
    inscripcion_id SERIAL PRIMARY KEY,
    estudiante_id INTEGER REFERENCES estudiantes(estudiante_id),
    curso_id INTEGER REFERENCES cursos(curso_id),
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    calificacion INTEGER CHECK (calificacion BETWEEN 0 AND 100),
    UNIQUE (estudiante_id, curso_id)  -- Un estudiante no puede inscribirse dos veces al mismo curso
);

-- Datos:
INSERT INTO cursos VALUES
(101, 'Python Básico', 40),
(102, 'SQL Intermedio', 30);

INSERT INTO estudiantes (estudiante_id, nombre, email) VALUES
(1, 'Estudiante 1', 'est1@email.com'),
(2, 'Estudiante 2', 'est2@email.com');

INSERT INTO inscripciones (estudiante_id, curso_id, fecha_inscripcion, calificacion) VALUES
(1, 101, '2024-01-15', 85),
(1, 102, '2024-02-01', 90),
(2, 101, '2024-01-20', 78);
```

**✅ Ahora cumple 2NF**: No hay dependencias parciales.

---

### Solución Ejercicio 3

**Respuesta**:

a) **Paciente ↔ Citas**: **1:N** (Uno a Muchos)
   - Un paciente puede tener muchas citas
   - Una cita pertenece a un paciente

b) **Doctor ↔ Citas**: **1:N** (Uno a Muchos)
   - Un doctor puede atender muchas citas
   - Una cita es atendida por un doctor

c) **Doctor ↔ Especialidades**: **N:M** (Muchos a Muchos)
   - Un doctor puede tener muchas especialidades
   - Una especialidad puede ser practicada por muchos doctores
   - **Requiere tabla intermedia**: `doctor_especialidad`

d) **Paciente ↔ Historia Clínica**: **1:1** (Uno a Uno)
   - Un paciente tiene una historia clínica
   - Una historia clínica pertenece a un paciente

---

### Solución Ejercicio 4

**Respuesta**:

1. **Sistema A (App móvil)**: **OLTP**
   - **Por qué**: Muchas transacciones concurrentes (transferencias, consultas), requiere escrituras rápidas, queries simples

2. **Sistema B (Dashboard ejecutivos)**: **OLAP**
   - **Por qué**: Pocas escrituras, queries complejas de agregación, lee grandes volúmenes de datos

3. **Sistema A diseño**: **Normalizado (3NF)**
   - **Por qué**: OLTP requiere normalización para integridad y eficiencia en escrituras

4. **Sistema B diseño**: **Desnormalizado (Star Schema)**
   - **Por qué**: OLAP requiere desnormalización para performance en queries analíticas

---

### Solución Ejercicio 5

**Análisis de dependencias**:
- `orden_id` → todo (es PK)
- `cliente_email` → `cliente_nombre`, `cliente_ciudad`, `cliente_pais`
- `cliente_ciudad` → `cliente_pais` (dependencia transitiva!)
- `producto_nombre` → `producto_categoria`, `producto_precio`

**Esquema 3NF**:

```sql
-- Tabla: paises
CREATE TABLE paises (
    pais_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: ciudades
CREATE TABLE ciudades (
    ciudad_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais_id INTEGER REFERENCES paises(pais_id)
);

-- Tabla: clientes
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    ciudad_id INTEGER REFERENCES ciudades(ciudad_id)
);

-- Tabla: categorias
CREATE TABLE categorias (
    categoria_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: productos
CREATE TABLE productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(categoria_id),
    precio NUMERIC(6,2) NOT NULL CHECK (precio > 0)
);

-- Tabla: ordenes
CREATE TABLE ordenes (
    orden_id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id),
    fecha_orden TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: items_orden (detalle de productos en cada orden)
CREATE TABLE items_orden (
    item_id SERIAL PRIMARY KEY,
    orden_id INTEGER REFERENCES ordenes(orden_id),
    producto_id INTEGER REFERENCES productos(producto_id),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(6,2) NOT NULL  -- Precio al momento de la orden
);

-- Datos:
INSERT INTO paises (nombre) VALUES ('España');
INSERT INTO ciudades (nombre, pais_id) VALUES ('Madrid', 1), ('Barcelona', 1);

INSERT INTO clientes (nombre, email, ciudad_id) VALUES
('Ana Martínez', 'ana@email.com', 1),
('Carlos López', 'carlos@email.com', 2);

INSERT INTO categorias (nombre) VALUES ('Comida Rápida'), ('Bebidas'), ('Pizza');

INSERT INTO productos (nombre, categoria_id, precio) VALUES
('Hamburguesa', 1, 8.50),
('Coca-Cola', 2, 2.50),
('Pizza Margherita', 3, 12.00);

INSERT INTO ordenes (orden_id, cliente_id, fecha_orden) VALUES
(1, 1, '2024-11-01 12:30:00'),
(2, 1, '2024-11-01 12:30:00'),  -- Misma orden para cliente 1
(3, 2, '2024-11-02 14:00:00');

INSERT INTO items_orden (orden_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 2, 8.50),   -- Orden 1: 2 Hamburguesas
(2, 2, 1, 2.50),   -- Orden 2: 1 Coca-Cola (misma orden física)
(3, 3, 1, 12.00);  -- Orden 3: 1 Pizza
```

**Diagrama ER**:
```
paises ←─ ciudades ←─ clientes ─→ ordenes ←─ items_orden ─→ productos ─→ categorias
 (1:N)      (1:N)      (1:N)         (1:N)           (N:1)        (N:1)
```

---

### Solución Ejercicio 6

**Diseño ER**:

```
clientes ──── compras ──── eventos
  (1)          (N:M)          (1)
```

**Relación N:M**: Cliente ↔ Evento requiere tabla intermedia `compras`

```sql
-- Tabla: clientes
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- Tabla: eventos
CREATE TABLE eventos (
    evento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(300) NOT NULL,
    fecha_evento TIMESTAMP NOT NULL,
    ubicacion VARCHAR(200) NOT NULL,
    capacidad_maxima INTEGER NOT NULL CHECK (capacidad_maxima > 0),
    precio_base NUMERIC(8,2) NOT NULL CHECK (precio_base >= 0)
);

-- Tabla intermedia: compras (N:M entre clientes y eventos)
CREATE TABLE compras (
    compra_id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(cliente_id) NOT NULL,
    evento_id INTEGER REFERENCES eventos(evento_id) NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad_entradas INTEGER NOT NULL CHECK (cantidad_entradas > 0),
    precio_unitario_pagado NUMERIC(8,2) NOT NULL,  -- Puede ser diferente al precio_base (descuentos)
    asientos_asignados VARCHAR(200),  -- Ej: "A12, A13" para 2 entradas
    total_pagado NUMERIC(10,2) GENERATED ALWAYS AS (cantidad_entradas * precio_unitario_pagado) STORED
);

-- Índices para queries comunes
CREATE INDEX idx_compras_cliente ON compras(cliente_id);
CREATE INDEX idx_compras_evento ON compras(evento_id);
CREATE INDEX idx_eventos_fecha ON eventos(fecha_evento);
```

**Cardinalidades**:
- Cliente → Compras: **1:N** (un cliente puede hacer muchas compras)
- Evento → Compras: **1:N** (un evento puede tener muchas compras)
- **Resultado**: Cliente ↔ Evento es **N:M** a través de `compras`

**Sí necesitas tabla intermedia** porque:
- Un cliente puede comprar para múltiples eventos
- Un evento puede ser comprado por múltiples clientes
- Necesitas atributos de la relación misma (fecha_compra, cantidad, precio_pagado)

---

### Solución Ejercicio 7

**1. Dependencias funcionales**:
```
empleado_id → nombre, email, departamento_id
departamento_id → departamento_nombre, jefe_departamento, edificio
```

**2. Dependencias transitivas**:
```
empleado_id → departamento_id → departamento_nombre
empleado_id → departamento_id → jefe_departamento
empleado_id → departamento_id → edificio
```

Estas son transitivas porque `empleado_id` determina `departamento_id`, y `departamento_id` determina `departamento_nombre`, `jefe_departamento` y `edificio`.

**3. Diseño 3NF**:

```sql
-- Tabla: edificios (normalizar aún más)
CREATE TABLE edificios (
    edificio_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla: departamentos
CREATE TABLE departamentos (
    departamento_id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    jefe_nombre VARCHAR(200),  -- O mejor: jefe_empleado_id INTEGER REFERENCES empleados
    edificio_id INTEGER REFERENCES edificios(edificio_id)
);

-- Tabla: empleados (solo datos propios)
CREATE TABLE empleados (
    empleado_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    departamento_id INTEGER REFERENCES departamentos(departamento_id)
);

-- Datos:
INSERT INTO edificios (nombre) VALUES ('Edificio A'), ('Edificio B');

INSERT INTO departamentos VALUES
(10, 'Ventas', 'Carlos Ruiz', 1),
(20, 'IT', 'Laura García', 2);

INSERT INTO empleados VALUES
(1, 'María López', 'maria@co.com', 10),
(2, 'Pedro Gómez', 'pedro@co.com', 10),
(3, 'Ana Martínez', 'ana@co.com', 20);
```

**4. Bonus - Cambio de edificio**:

**Antes de normalizar** (tabla original):
```sql
-- Si "Ventas" se muda a Edificio B, necesitas actualizar TODAS las filas de empleados de Ventas
UPDATE empleados SET edificio = 'Edificio B' WHERE departamento_id = 10;
-- 2 UPDATEs (María y Pedro)
```

**Después de normalizar**:
```sql
-- Solo actualizas la tabla departamentos
UPDATE departamentos SET edificio_id = 2 WHERE departamento_id = 10;
-- 1 UPDATE (mucho más eficiente y sin riesgo de inconsistencias)
```

---

### Solución Ejercicio 8

```sql
CREATE TABLE dim_fecha (
    -- PK como YYYYMMDD para JOINs eficientes con integers
    fecha_id INTEGER PRIMARY KEY,  -- Ej: 20241115

    -- Fecha completa
    fecha DATE NOT NULL UNIQUE,

    -- Componentes de fecha
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    dia_mes INTEGER NOT NULL CHECK (dia_mes BETWEEN 1 AND 31),
    trimestre INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),

    -- Nombres descriptivos
    mes_nombre VARCHAR(20) NOT NULL,  -- 'Enero', 'Febrero', etc.
    mes_nombre_corto CHAR(3) NOT NULL,  -- 'Ene', 'Feb', etc.

    -- Día de la semana
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),  -- 1=Lunes, 7=Domingo
    dia_semana_nombre VARCHAR(20) NOT NULL,  -- 'Lunes', 'Martes', etc.
    dia_semana_nombre_corto CHAR(3) NOT NULL,  -- 'Lun', 'Mar', etc.

    -- Flags booleanos
    es_fin_semana BOOLEAN NOT NULL,
    es_festivo BOOLEAN NOT NULL DEFAULT FALSE,
    es_laboral BOOLEAN NOT NULL DEFAULT TRUE,

    -- Semana del año (ISO 8601)
    semana_anio INTEGER NOT NULL CHECK (semana_anio BETWEEN 1 AND 53)
);

-- Poblar dim_fecha para año 2024
INSERT INTO dim_fecha (
    fecha_id,
    fecha,
    anio,
    mes,
    dia_mes,
    trimestre,
    mes_nombre,
    mes_nombre_corto,
    dia_semana,
    dia_semana_nombre,
    dia_semana_nombre_corto,
    es_fin_semana,
    semana_anio
)
SELECT
    TO_CHAR(fecha, 'YYYYMMDD')::INTEGER as fecha_id,
    fecha,
    EXTRACT(YEAR FROM fecha)::INTEGER as anio,
    EXTRACT(MONTH FROM fecha)::INTEGER as mes,
    EXTRACT(DAY FROM fecha)::INTEGER as dia_mes,
    EXTRACT(QUARTER FROM fecha)::INTEGER as trimestre,
    CASE EXTRACT(MONTH FROM fecha)
        WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero' WHEN 3 THEN 'Marzo'
        WHEN 4 THEN 'Abril' WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
        WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto' WHEN 9 THEN 'Septiembre'
        WHEN 10 THEN 'Octubre' WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
    END as mes_nombre,
    CASE EXTRACT(MONTH FROM fecha)
        WHEN 1 THEN 'Ene' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
        WHEN 4 THEN 'Abr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
        WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago' WHEN 9 THEN 'Sep'
        WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dic'
    END as mes_nombre_corto,
    -- ISO: 1=Lunes, 7=Domingo (en PostgreSQL: 0=Domingo, ajustamos)
    CASE WHEN EXTRACT(DOW FROM fecha) = 0 THEN 7 ELSE EXTRACT(DOW FROM fecha)::INTEGER END as dia_semana,
    CASE EXTRACT(DOW FROM fecha)
        WHEN 0 THEN 'Domingo' WHEN 1 THEN 'Lunes' WHEN 2 THEN 'Martes'
        WHEN 3 THEN 'Miércoles' WHEN 4 THEN 'Jueves' WHEN 5 THEN 'Viernes' WHEN 6 THEN 'Sábado'
    END as dia_semana_nombre,
    CASE EXTRACT(DOW FROM fecha)
        WHEN 0 THEN 'Dom' WHEN 1 THEN 'Lun' WHEN 2 THEN 'Mar'
        WHEN 3 THEN 'Mié' WHEN 4 THEN 'Jue' WHEN 5 THEN 'Vie' WHEN 6 THEN 'Sáb'
    END as dia_semana_nombre_corto,
    EXTRACT(DOW FROM fecha) IN (0, 6) as es_fin_semana,
    EXTRACT(WEEK FROM fecha)::INTEGER as semana_anio
FROM generate_series('2024-01-01'::DATE, '2024-12-31'::DATE, '1 day'::INTERVAL) fecha;

-- Marcar festivos españoles manualmente (ejemplo)
UPDATE dim_fecha SET es_festivo = TRUE, es_laboral = FALSE
WHERE fecha IN ('2024-01-01', '2024-01-06', '2024-12-25', '2024-12-26');
```

**Justificación de PK**:
- **Formato YYYYMMDD como INTEGER** (ej: 20241115) es mejor que SERIAL porque:
  - ✅ JOIN más rápido (integers vs seriales)
  - ✅ Fácil de generar desde strings de fecha
  - ✅ Ordenamiento natural (20241101 < 20241102)
  - ✅ Legible para humanos

---

### Solución Ejercicio 9

**Star Schema**:

```sql
-- ===== DIMENSIONES =====

-- Dimensión: Fecha (reutilizar del ejercicio anterior)
-- CREATE TABLE dim_fecha (...);

-- Dimensión: Cliente
CREATE TABLE dim_cliente (
    cliente_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    pais VARCHAR(100) NOT NULL,
    fecha_registro DATE NOT NULL
);

-- Dimensión: Juego
CREATE TABLE dim_juego (
    juego_id INTEGER PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    genero VARCHAR(100) NOT NULL,  -- RPG, FPS, Strategy, etc.
    desarrollador VARCHAR(200),
    anio_lanzamiento INTEGER,
    plataforma VARCHAR(50) NOT NULL  -- PS5, Xbox, PC, Switch
);

-- ===== TABLA DE HECHOS =====

CREATE TABLE fact_ventas_juegos (
    venta_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER NOT NULL REFERENCES dim_fecha(fecha_id),
    cliente_id INTEGER REFERENCES dim_cliente(cliente_id),
    juego_id INTEGER REFERENCES dim_juego(juego_id),

    -- Métricas aditivas
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(8,2) NOT NULL,
    monto_venta NUMERIC(10,2) NOT NULL  -- cantidad * precio_unitario
);

-- Índices
CREATE INDEX idx_fact_ventas_juegos_fecha ON fact_ventas_juegos(fecha_id);
CREATE INDEX idx_fact_ventas_juegos_cliente ON fact_ventas_juegos(cliente_id);
CREATE INDEX idx_fact_ventas_juegos_juego ON fact_ventas_juegos(juego_id);
```

**Query Analítica: Total ventas por género en Q4 2024**:

```sql
SELECT
    j.genero,
    SUM(v.monto_venta) as total_ventas,
    COUNT(*) as num_transacciones,
    SUM(v.cantidad) as unidades_vendidas,
    AVG(v.precio_unitario) as precio_promedio
FROM fact_ventas_juegos v
JOIN dim_juego j ON v.juego_id = j.juego_id
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024 AND f.trimestre = 4
GROUP BY j.genero
ORDER BY total_ventas DESC;
```

**Resultado esperado**:
```
genero   | total_ventas | num_transacciones | unidades_vendidas | precio_promedio
RPG      | 450000.00    | 5234              | 8500              | 59.99
FPS      | 380000.00    | 6123              | 12000             | 49.99
Strategy | 125000.00    | 1890              | 3200              | 39.99
```

---

### Solución Ejercicio 10

**Esquema 3NF completo**:

```sql
-- Tabla: paises
CREATE TABLE paises (
    pais_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: ciudades
CREATE TABLE ciudades (
    ciudad_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais_id INTEGER REFERENCES paises(pais_id)
);

-- Tabla: seguros
CREATE TABLE seguros (
    seguro_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    cobertura_porcentaje INTEGER NOT NULL CHECK (cobertura_porcentaje BETWEEN 0 AND 100)
);

-- Tabla: pacientes
CREATE TABLE pacientes (
    paciente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(150),
    ciudad_id INTEGER REFERENCES ciudades(ciudad_id),
    seguro_id INTEGER REFERENCES seguros(seguro_id)
);

-- Tabla: especialidades
CREATE TABLE especialidades (
    especialidad_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: doctores
CREATE TABLE doctores (
    doctor_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    licencia_medica VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla intermedia: doctor_especialidad (N:M)
CREATE TABLE doctor_especialidad (
    doctor_id INTEGER REFERENCES doctores(doctor_id),
    especialidad_id INTEGER REFERENCES especialidades(especialidad_id),
    anios_experiencia INTEGER DEFAULT 0,
    PRIMARY KEY (doctor_id, especialidad_id)
);

-- Tabla: medicamentos
CREATE TABLE medicamentos (
    medicamento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) UNIQUE NOT NULL,
    dosis VARCHAR(50),  -- "600mg", "20mg", etc.
    tipo VARCHAR(100)   -- "Analgésico", "Antibiótico", etc.
);

-- Tabla: citas
CREATE TABLE citas (
    cita_id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(paciente_id) NOT NULL,
    doctor_id INTEGER REFERENCES doctores(doctor_id) NOT NULL,
    fecha_cita TIMESTAMP NOT NULL,
    diagnostico TEXT,
    costo_consulta NUMERIC(6,2) NOT NULL
);

-- Tabla intermedia: cita_medicamento (N:M)
CREATE TABLE cita_medicamento (
    cita_id INTEGER REFERENCES citas(cita_id),
    medicamento_id INTEGER REFERENCES medicamentos(medicamento_id),
    instrucciones TEXT,  -- "Tomar cada 8 horas después de comidas"
    PRIMARY KEY (cita_id, medicamento_id)
);

-- Índices
CREATE INDEX idx_citas_paciente ON citas(paciente_id);
CREATE INDEX idx_citas_doctor ON citas(doctor_id);
CREATE INDEX idx_citas_fecha ON citas(fecha_cita);
```

**Query que reconstruye una fila de la tabla desnormalizada**:

```sql
SELECT
    c.cita_id,
    c.fecha_cita,
    p.nombre as paciente_nombre,
    p.dni as paciente_dni,
    p.email as paciente_email,
    ci.nombre as paciente_ciudad,
    d.nombre as doctor_nombre,
    STRING_AGG(DISTINCT e.nombre, ', ') as doctor_especialidades,
    c.diagnostico,
    STRING_AGG(DISTINCT m.nombre || ' ' || m.dosis, ', ') as medicamentos_recetados,
    c.costo_consulta,
    s.nombre as seguro_nombre,
    s.cobertura_porcentaje as seguro_cobertura_porcentaje
FROM citas c
JOIN pacientes p ON c.paciente_id = p.paciente_id
LEFT JOIN ciudades ci ON p.ciudad_id = ci.ciudad_id
LEFT JOIN seguros s ON p.seguro_id = s.seguro_id
JOIN doctores d ON c.doctor_id = d.doctor_id
LEFT JOIN doctor_especialidad de ON d.doctor_id = de.doctor_id
LEFT JOIN especialidades e ON de.especialidad_id = e.especialidad_id
LEFT JOIN cita_medicamento cm ON c.cita_id = cm.cita_id
LEFT JOIN medicamentos m ON cm.medicamento_id = m.medicamento_id
WHERE c.cita_id = 1
GROUP BY c.cita_id, c.fecha_cita, p.nombre, p.dni, p.email, ci.nombre,
         d.nombre, c.diagnostico, c.costo_consulta, s.nombre, s.cobertura_porcentaje;
```

**Beneficios de normalización**:
- ✅ Cero redundancia
- ✅ Actualizar email de paciente = 1 UPDATE
- ✅ Cambiar cobertura de seguro = 1 UPDATE (afecta a todos los pacientes con ese seguro)
- ✅ Agregar nueva especialidad a un doctor = 1 INSERT

---

### Solución Ejercicio 11

**Star Schema con SCD Type 2**:

```sql
-- Dimensión: Fecha (reutilizar)
-- CREATE TABLE dim_fecha (...);

-- Dimensión: Cliente con SCD Type 2
CREATE TABLE dim_cliente (
    cliente_key SERIAL PRIMARY KEY,        -- Clave surrogada (única por versión)
    cliente_id INTEGER NOT NULL,           -- ID del cliente en sistema OLTP
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(150) NOT NULL,
    plan VARCHAR(50) NOT NULL,             -- 'Básico', 'Estándar', 'Premium'
    precio_plan NUMERIC(6,2) NOT NULL,

    -- Campos SCD Type 2
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    es_actual BOOLEAN NOT NULL DEFAULT TRUE,

    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio)
);

CREATE INDEX idx_dim_cliente_actual ON dim_cliente(cliente_id, es_actual);
CREATE INDEX idx_dim_cliente_periodo ON dim_cliente(fecha_inicio, fecha_fin);

-- Tabla de Hechos: Ingresos Mensuales
CREATE TABLE fact_ingresos_mensuales (
    ingreso_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER NOT NULL REFERENCES dim_fecha(fecha_id),  -- YYYYMM01 (primer día del mes)
    cliente_key INTEGER NOT NULL REFERENCES dim_cliente(cliente_key),  -- FK a versión específica
    monto_ingreso NUMERIC(8,2) NOT NULL,
    dias_activo INTEGER NOT NULL  -- Cuántos días del mes estuvo activo
);

CREATE INDEX idx_fact_ingresos_fecha ON fact_ingresos_mensuales(fecha_id);
CREATE INDEX idx_fact_ingresos_cliente ON fact_ingresos_mensuales(cliente_key);
```

**Proceso cuando cliente cambia de plan**:

```sql
-- ===== ESTADO INICIAL: Ana con plan Básico =====
INSERT INTO dim_cliente (cliente_id, nombre, email, plan, precio_plan, fecha_inicio, fecha_fin, es_actual)
VALUES (101, 'Ana López', 'ana@email.com', 'Básico', 9.99, '2023-01-15', NULL, TRUE);
-- cliente_key = 1

-- Ingresos de Ana (Enero-Junio 2024) con plan Básico
INSERT INTO fact_ingresos_mensuales (fecha_id, cliente_key, monto_ingreso, dias_activo) VALUES
(20240101, 1, 9.99, 31),   -- Enero
(20240201, 1, 9.99, 29),   -- Febrero
(20240301, 1, 9.99, 31),   -- Marzo
(20240401, 1, 9.99, 30),   -- Abril
(20240501, 1, 9.99, 31),   -- Mayo
(20240601, 1, 9.99, 30);   -- Junio


-- ===== ANA HACE UPGRADE A PREMIUM EL 2024-07-01 =====

-- Paso 1: Cerrar versión anterior (Básico)
UPDATE dim_cliente
SET fecha_fin = '2024-07-01',
    es_actual = FALSE
WHERE cliente_key = 1;

-- Paso 2: Insertar nueva versión (Premium)
INSERT INTO dim_cliente (cliente_id, nombre, email, plan, precio_plan, fecha_inicio, fecha_fin, es_actual)
VALUES (101, 'Ana López', 'ana@email.com', 'Premium', 15.99, '2024-07-01', NULL, TRUE);
-- cliente_key = 2 (nueva versión)

-- Ingresos de Ana (Julio-Diciembre 2024) con plan Premium
INSERT INTO fact_ingresos_mensuales (fecha_id, cliente_key, monto_ingreso, dias_activo) VALUES
(20240701, 2, 15.99, 31),  -- Julio
(20240801, 2, 15.99, 31),  -- Agosto
(20240901, 2, 15.99, 30),  -- Septiembre
(20241001, 2, 15.99, 31),  -- Octubre
(20241101, 2, 15.99, 30),  -- Noviembre
(20241201, 2, 15.99, 31);  -- Diciembre


-- ===== ESTADO FINAL: 2 versiones de Ana =====
SELECT * FROM dim_cliente WHERE cliente_id = 101;

-- Resultado:
-- cliente_key | cliente_id | nombre     | plan    | precio_plan | fecha_inicio | fecha_fin  | es_actual
-- 1           | 101        | Ana López  | Básico  | 9.99        | 2023-01-15   | 2024-07-01 | FALSE
-- 2           | 101        | Ana López  | Premium | 15.99       | 2024-07-01   | NULL       | TRUE
```

**Query: Ingresos por plan en Enero 2024 (usando historial SCD)**:

```sql
SELECT
    c.plan,
    SUM(i.monto_ingreso) as ingresos_totales,
    COUNT(DISTINCT c.cliente_id) as clientes_unicos,
    AVG(i.monto_ingreso) as ingreso_promedio
FROM fact_ingresos_mensuales i
JOIN dim_cliente c ON i.cliente_key = c.cliente_key
JOIN dim_fecha f ON i.fecha_id = f.fecha_id
WHERE f.anio = 2024 AND f.mes = 1
GROUP BY c.plan
ORDER BY ingresos_totales DESC;

-- Resultado correcto:
-- plan    | ingresos_totales | clientes_unicos | ingreso_promedio
-- Básico  | 9.99             | 1               | 9.99

-- Ana aparece como "Básico" porque en Enero 2024 tenía ese plan
-- (aunque ahora sea Premium)
```

**Sin SCD Type 2 (mal diseño)**:
Si hubiéramos sobrescrito el plan de Ana a "Premium", la query reportaría INCORRECTAMENTE:
```
plan    | ingresos_totales
Premium | 9.99  ← ¡ERROR! Ana no era Premium en Enero 2024
```

---

### Solución Ejercicio 12

**Versión A: Star Schema (desnormalizado)**:

```sql
CREATE TABLE dim_producto_star (
    producto_id INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(200) NOT NULL,
    subcategoria VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    super_categoria VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    precio_lista NUMERIC(10,2) NOT NULL
);
```

**Versión B: Snowflake Schema (normalizado)**:

```sql
-- Tabla: super_categorias
CREATE TABLE super_categorias (
    super_categoria_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: categorias
CREATE TABLE categorias (
    categoria_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    super_categoria_id INTEGER REFERENCES super_categorias(super_categoria_id)
);

-- Tabla: marcas
CREATE TABLE marcas (
    marca_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    pais_origen VARCHAR(100)
);

-- Tabla: productos (snowflake - normalizado)
CREATE TABLE dim_producto_snowflake (
    producto_id INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(200) NOT NULL,
    subcategoria VARCHAR(100) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(categoria_id),
    marca_id INTEGER REFERENCES marcas(marca_id),
    precio_lista NUMERIC(10,2) NOT NULL
);
```

**Análisis de trade-offs**:

**1. Redundancia de datos**:

Asumiendo:
- 50,000 productos
- 500 categorías únicas (promedio: 100 productos por categoría)
- 20 super-categorías
- 200 marcas únicas

**Star Schema** (desnormalizado):
- Cada producto repite categoría + super_categoría + marca
- Redundancia estimada:
  - `categoria`: 100 productos × "Electrónica" = ~100 bytes × 100 = 10KB por categoría × 500 = **5MB**
  - `super_categoria`: Similar = ~**2MB**
  - `marca`: ~**3MB**
- **Total redundancia**: ~10MB

**Snowflake Schema** (normalizado):
- Categorías: 500 filas = ~50KB
- Marcas: 200 filas = ~20KB
- Super-categorías: 20 filas = ~2KB
- **Total**: ~72KB

**Ahorro de espacio**: ~9.9MB (99% reducción en redundancia)

**2. Comparación de JOINs**:

Query: "Total ventas por super_categoría"

**Star Schema (2 JOINs)**:
```sql
SELECT
    p.super_categoria,
    SUM(v.monto_venta) as total
FROM fact_ventas v
JOIN dim_producto_star p ON v.producto_id = p.producto_id
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024
GROUP BY p.super_categoria;
```

**Snowflake Schema (4 JOINs)**:
```sql
SELECT
    sc.nombre as super_categoria,
    SUM(v.monto_venta) as total
FROM fact_ventas v
JOIN dim_producto_snowflake p ON v.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
JOIN super_categorias sc ON c.super_categoria_id = sc.super_categoria_id
JOIN dim_fecha f ON v.fecha_id = f.fecha_id
WHERE f.anio = 2024
GROUP BY sc.nombre;
```

**3. Performance**:
- Star: **Más rápido** (menos JOINs, datos en una tabla)
- Snowflake: **Más lento** (más JOINs, más lookups)
- Diferencia estimada: 15-30% más lento para Snowflake en queries típicas

**4. Complejidad para analistas**:
- Star: **Más simple** (todo en una tabla dimensional)
- Snowflake: **Más complejo** (requiere entender relaciones entre categorías)

**5. Mantenimiento**:
- Star: **Más difícil** (actualizar "Electrónica" = UPDATE 5,000 filas)
- Snowflake: **Más fácil** (actualizar "Electrónica" = UPDATE 1 fila en `categorias`)

---

**RECOMENDACIÓN FINAL**: **Star Schema**

**Justificación**:
1. ✅ **Performance es crítico**: Data Warehouse prioriza velocidad de lectura
2. ✅ **10MB de redundancia es insignificante**: En un DWH con GB/TB de datos
3. ✅ **Simplicidad para analistas**: Herramientas BI funcionan mejor con Star
4. ✅ **Categorías son estables**: Cambios son raros

**EXCEPCIÓN - Usar Snowflake cuando**:
- Dimensión es MASIVA (millones de filas)
- Espacio en disco es extremadamente limitado
- Dimensión cambia frecuentemente

**Para este caso específico (50K productos, 500 categorías)**: **Star Schema es la mejor opción** ⭐

---

**Implementación recomendada (Star Schema)**:

```sql
CREATE TABLE dim_producto (
    producto_id INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(200) NOT NULL,
    subcategoria VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    super_categoria VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    precio_lista NUMERIC(10,2) NOT NULL
);

-- Índices para queries comunes
CREATE INDEX idx_producto_categoria ON dim_producto(categoria);
CREATE INDEX idx_producto_super_categoria ON dim_producto(super_categoria);
CREATE INDEX idx_producto_marca ON dim_producto(marca);
```

---

## Conclusión

Has completado 12 ejercicios de modelado de datos:

- **Básicos (1-4)**: Identificar violaciones de formas normales, cardinalidades, OLTP vs OLAP
- **Intermedios (5-9)**: Normalizar esquemas, diseñar ER con N:M, crear Star Schemas
- **Avanzados (10-12)**: Normalización completa de sistemas reales, SCD Type 2, Snowflake vs Star

**Habilidades desarrolladas**:
- ✅ Normalización hasta 3NF
- ✅ Diseño de diagramas ER con cardinalidades correctas
- ✅ Creación de Star Schemas para Data Warehouses
- ✅ Implementación de SCD Type 2 para historial
- ✅ Decisiones de diseño basadas en trade-offs

**Próximo paso**: Implementa el proyecto práctico de Data Warehouse en `04-proyecto-practico/`

---

**Tiempo estimado de resolución**: 3-4 horas
**Revisado**: 2025-11-12
**Nivel alcanzado**: Intermedio-Avanzado en Modelado de Datos 🎓
