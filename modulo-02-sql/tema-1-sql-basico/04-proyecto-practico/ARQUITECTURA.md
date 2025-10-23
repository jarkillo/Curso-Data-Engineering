# Arquitectura: Proyecto Práctico SQL Básico

**Fecha**: 2025-10-23
**Tema**: SQL Básico - Análisis Exploratorio de Base de Datos
**Arquitecto**: Equipo Development

---

## Resumen Ejecutivo

**Objetivo del Proyecto**: Crear un analizador de base de datos SQLite que permita a los estudiantes practicar SQL básico mediante consultas programáticas desde Python.

**Enfoque**: Funcional, sin clases (excepto para conexión DB), con funciones puras y composables.

---

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── conexion_db.py        ← Clase ConexionSQLite (excepción válida)
│   ├── consultas_basicas.py  ← SELECT, WHERE, ORDER BY, LIMIT
│   ├── consultas_agregadas.py ← COUNT, SUM, AVG, MAX, MIN
│   ├── consultas_agrupadas.py ← GROUP BY, HAVING
│   └── validaciones.py        ← Validación de queries y resultados
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            ← Fixtures compartidas (DB de prueba)
│   ├── test_conexion_db.py
│   ├── test_consultas_basicas.py
│   ├── test_consultas_agregadas.py
│   ├── test_consultas_agrupadas.py
│   └── test_validaciones.py
│
├── datos/
│   ├── techstore.db           ← Base de datos SQLite de ejemplo
│   └── crear_db.sql           ← Script SQL para recrear la DB
│
├── ejemplos/
│   ├── ejemplo_01_consultas_basicas.py
│   ├── ejemplo_02_agregaciones.py
│   └── ejemplo_03_analisis_completo.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Módulos y Responsabilidades

### 1. `conexion_db.py` - Gestión de Conexión

**Propósito**: Manejar conexión a SQLite de forma segura.

**Excepción a la regla**: Usamos una clase porque gestiona un recurso externo (conexión DB).

**Funciones públicas**:
```python
class ConexionSQLite:
    """Gestiona conexión a base de datos SQLite."""

    def __init__(self, ruta_db: str) -> None:
        """Inicializa conexión."""

    def ejecutar_query(self, query: str, parametros: tuple = ()) -> list[dict]:
        """Ejecuta query y retorna resultados como lista de diccionarios."""

    def cerrar(self) -> None:
        """Cierra la conexión."""

    def __enter__(self):
        """Context manager."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager."""
```

**Justificación de la clase**:
- Maneja estado (conexión abierta/cerrada)
- Implementa context manager (`with`)
- Es un conector externo (excepción válida según reglas)

---

### 2. `consultas_basicas.py` - Queries SELECT Simples

**Propósito**: Funciones para consultas básicas (SELECT, WHERE, ORDER BY, LIMIT).

**Funciones**:
```python
def obtener_todos_los_productos(conexion: ConexionSQLite) -> list[dict]:
    """
    Obtiene todos los productos de la tabla productos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de diccionarios con todos los productos

    Examples:
        >>> conn = ConexionSQLite("techstore.db")
        >>> productos = obtener_todos_los_productos(conn)
        >>> len(productos)
        10
    """

def filtrar_productos_por_categoria(
    conexion: ConexionSQLite,
    categoria: str
) -> list[dict]:
    """
    Filtra productos por categoría.

    Args:
        conexion: Instancia de ConexionSQLite
        categoria: Nombre de la categoría (ej: "Accesorios")

    Returns:
        Lista de productos de esa categoría

    Raises:
        ValueError: Si la categoría está vacía
    """

def obtener_productos_caros(
    conexion: ConexionSQLite,
    precio_minimo: float
) -> list[dict]:
    """
    Obtiene productos con precio mayor al mínimo especificado.

    Args:
        conexion: Instancia de ConexionSQLite
        precio_minimo: Precio mínimo (debe ser > 0)

    Returns:
        Lista de productos ordenados por precio descendente

    Raises:
        ValueError: Si precio_minimo <= 0
    """

def obtener_top_n_productos_mas_caros(
    conexion: ConexionSQLite,
    n: int = 5
) -> list[dict]:
    """
    Obtiene los N productos más caros.

    Args:
        conexion: Instancia de ConexionSQLite
        n: Cantidad de productos a retornar (default: 5)

    Returns:
        Lista de N productos más caros

    Raises:
        ValueError: Si n <= 0
    """
```

---

### 3. `consultas_agregadas.py` - Funciones Agregadas

**Propósito**: Funciones para COUNT, SUM, AVG, MAX, MIN.

**Funciones**:
```python
def contar_productos(conexion: ConexionSQLite) -> int:
    """
    Cuenta el total de productos en la base de datos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Número total de productos
    """

def calcular_precio_promedio(conexion: ConexionSQLite) -> float:
    """
    Calcula el precio promedio de todos los productos.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Precio promedio redondeado a 2 decimales
    """

def obtener_estadisticas_precios(conexion: ConexionSQLite) -> dict:
    """
    Obtiene estadísticas de precios (min, max, avg, count).

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Diccionario con claves: 'minimo', 'maximo', 'promedio', 'total'

    Examples:
        >>> stats = obtener_estadisticas_precios(conn)
        >>> stats.keys()
        dict_keys(['minimo', 'maximo', 'promedio', 'total'])
    """

def calcular_ingresos_totales(conexion: ConexionSQLite) -> float:
    """
    Calcula los ingresos totales de todas las ventas.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Ingresos totales (cantidad * precio_unitario)
    """
```

---

### 4. `consultas_agrupadas.py` - GROUP BY y HAVING

**Propósito**: Funciones para agrupar y filtrar grupos.

**Funciones**:
```python
def contar_productos_por_categoria(conexion: ConexionSQLite) -> list[dict]:
    """
    Cuenta productos por categoría.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con 'categoria' y 'cantidad'
        Ordenado por cantidad descendente
    """

def calcular_valor_inventario_por_categoria(
    conexion: ConexionSQLite
) -> list[dict]:
    """
    Calcula el valor total de inventario por categoría.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con 'categoria', 'valor_inventario'
        Ordenado por valor descendente
    """

def obtener_categorias_con_mas_de_n_productos(
    conexion: ConexionSQLite,
    n: int = 1
) -> list[dict]:
    """
    Obtiene categorías que tienen más de N productos.

    Args:
        conexion: Instancia de ConexionSQLite
        n: Número mínimo de productos (default: 1)

    Returns:
        Lista de categorías con cantidad de productos

    Raises:
        ValueError: Si n < 0
    """

def analizar_ventas_por_producto(conexion: ConexionSQLite) -> list[dict]:
    """
    Analiza ventas agrupadas por producto.

    Args:
        conexion: Instancia de ConexionSQLite

    Returns:
        Lista de dicts con:
        - 'producto_id'
        - 'unidades_vendidas'
        - 'ingresos_totales'
        Ordenado por ingresos descendente
    """
```

---

### 5. `validaciones.py` - Validación de Inputs

**Propósito**: Funciones puras de validación (sin efectos colaterales).

**Funciones**:
```python
def validar_precio_positivo(precio: float) -> None:
    """
    Valida que el precio sea positivo.

    Args:
        precio: Precio a validar

    Raises:
        ValueError: Si precio <= 0
        TypeError: Si precio no es numérico
    """

def validar_categoria_no_vacia(categoria: str) -> None:
    """
    Valida que la categoría no esté vacía.

    Args:
        categoria: Nombre de categoría

    Raises:
        ValueError: Si categoría está vacía o es solo espacios
        TypeError: Si categoría no es string
    """

def validar_numero_positivo(numero: int, nombre_parametro: str) -> None:
    """
    Valida que un número sea positivo.

    Args:
        numero: Número a validar
        nombre_parametro: Nombre del parámetro (para mensaje de error)

    Raises:
        ValueError: Si numero <= 0
        TypeError: Si numero no es int
    """

def validar_ruta_db_existe(ruta: str) -> None:
    """
    Valida que la ruta de la base de datos exista.

    Args:
        ruta: Ruta al archivo .db

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si la ruta está vacía
    """
```

---

## Decisiones de Diseño

### 1. ¿Por qué una clase para ConexionSQLite?

**Justificación**:
- Maneja un recurso externo (conexión DB)
- Necesita estado (conexión abierta/cerrada)
- Implementa context manager (`with`)
- Es una **excepción válida** según las reglas del proyecto

**Alternativa descartada**: Funciones que abren/cierran conexión en cada llamada (ineficiente).

---

### 2. ¿Por qué separar en 3 módulos de consultas?

**Justificación**:
- **Modularidad**: Cada módulo corresponde a un concepto de SQL
- **Didáctico**: Los estudiantes aprenden progresivamente
- **Mantenibilidad**: Archivos <300 líneas cada uno

**Mapeo con contenido teórico**:
- `consultas_basicas.py` → Tema 1, Sección 1-4 de teoría
- `consultas_agregadas.py` → Tema 1, Sección 5 de teoría
- `consultas_agrupadas.py` → Tema 1, Sección 6-7 de teoría

---

### 3. ¿Por qué funciones puras en lugar de métodos?

**Justificación**:
- **Testabilidad**: Fácil de testear (input → output)
- **Composabilidad**: Se pueden combinar fácilmente
- **Sin efectos colaterales**: Predecibles y seguras
- **Alineado con reglas del proyecto**: Funcional first

**Ejemplo de composición**:
```python
# Composición de funciones
productos = obtener_todos_los_productos(conn)
caros = [p for p in productos if p['precio'] > 500]
top_5 = sorted(caros, key=lambda x: x['precio'], reverse=True)[:5]

# vs función específica
top_5 = obtener_top_n_productos_mas_caros(conn, 5)
```

---

### 4. ¿Por qué retornar `list[dict]` en lugar de tuplas?

**Justificación**:
- **Legibilidad**: `producto['nombre']` vs `producto[2]`
- **Flexibilidad**: Fácil agregar columnas sin romper código
- **Didáctico**: Los estudiantes entienden mejor la estructura

**Desventaja aceptada**: Ligeramente menos eficiente en memoria (aceptable para proyectos educativos).

---

### 5. ¿Por qué SQLite y no PostgreSQL?

**Justificación**:
- **Sin dependencias externas**: No requiere Docker ni instalación
- **Portable**: Archivo `.db` se puede compartir fácilmente
- **Didáctico**: Enfoque en SQL, no en configuración de DB
- **Suficiente para SQL básico**: Soporta todas las queries del tema

**Nota**: En Tema 2 (SQL Intermedio) se introducirá PostgreSQL.

---

## Flujo de Datos

### Flujo Típico de una Consulta

```
1. Usuario llama función de consulta
   ↓
2. Función valida inputs (validaciones.py)
   ↓
3. Función construye query SQL (string)
   ↓
4. Función llama conexion.ejecutar_query(query)
   ↓
5. ConexionSQLite ejecuta query en SQLite
   ↓
6. ConexionSQLite convierte resultados a list[dict]
   ↓
7. Función retorna resultados al usuario
```

### Ejemplo Concreto

```python
# 1. Usuario llama función
productos = filtrar_productos_por_categoria(conn, "Accesorios")

# 2. Dentro de la función: validar
validar_categoria_no_vacia("Accesorios")  # ✅ Pasa

# 3. Construir query
query = """
    SELECT id, nombre, precio, categoria
    FROM productos
    WHERE categoria = ?
    ORDER BY precio DESC
"""

# 4. Ejecutar query
resultados = conexion.ejecutar_query(query, ("Accesorios",))

# 5-6. SQLite ejecuta y retorna
# [
#   {'id': 8, 'nombre': 'AirPods Pro', 'precio': 249.99, ...},
#   {'id': 3, 'nombre': 'Teclado Mecánico', 'precio': 149.99, ...},
#   ...
# ]

# 7. Retornar al usuario
return resultados
```

---

## Seguridad

### Prevención de SQL Injection

**Regla**: SIEMPRE usar parámetros, NUNCA concatenar strings.

```python
# ✅ CORRECTO: Parámetros
query = "SELECT * FROM productos WHERE categoria = ?"
conexion.ejecutar_query(query, (categoria,))

# ❌ INCORRECTO: Concatenación (vulnerable a SQL injection)
query = f"SELECT * FROM productos WHERE categoria = '{categoria}'"
conexion.ejecutar_query(query)
```

**Implementación en ConexionSQLite**:
```python
def ejecutar_query(self, query: str, parametros: tuple = ()) -> list[dict]:
    """Ejecuta query con parámetros seguros."""
    cursor = self.conexion.cursor()
    cursor.execute(query, parametros)  # ← SQLite maneja sanitización
    # ...
```

---

## Base de Datos de Ejemplo

### Esquema

**Tabla `productos`**:
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT NOT NULL,
    stock_actual INTEGER NOT NULL,
    proveedor TEXT
);
```

**Tabla `ventas`**:
```sql
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
```

### Datos de Ejemplo

- **10 productos** de TechStore (mismos que en 02-EJEMPLOS.md)
- **10 ventas** de octubre 2025
- **Datos realistas** pero ficticios

---

## Testing Strategy

### Fixtures Compartidas (conftest.py)

```python
@pytest.fixture
def db_prueba_en_memoria():
    """Crea DB SQLite en memoria para tests."""
    conn = ConexionSQLite(":memory:")
    # Crear tablas
    # Insertar datos de prueba
    yield conn
    conn.cerrar()

@pytest.fixture
def productos_prueba():
    """Retorna lista de productos de prueba."""
    return [
        {'id': 1, 'nombre': 'Laptop', 'precio': 899.99, ...},
        # ...
    ]
```

### Estrategia de Tests

**Cada función debe tener**:
1. Test de caso feliz
2. Test de caso borde (lista vacía, 1 elemento, etc.)
3. Test de validación (inputs inválidos)

**Cobertura objetivo**: >90% (proyecto educativo, debe ser ejemplar)

---

## Dependencias

### requirements.txt

```
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Linting (opcional pero recomendado)
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0

# No se requieren librerías para SQLite (viene con Python)
```

---

## Entregables

### Fase Arquitectura (Actual)
- [x] `ARQUITECTURA.md` (este documento)
- [x] Diseño de estructura de carpetas
- [x] Firmas de funciones principales
- [x] Decisiones de diseño documentadas

### Fase TDD (Siguiente)
- [ ] `conftest.py` con fixtures
- [ ] Tests para todas las funciones
- [ ] Cobertura >90%

### Fase Implementación (Siguiente)
- [ ] Implementación de todos los módulos
- [ ] Base de datos de ejemplo
- [ ] Scripts de ejemplo
- [ ] README completo

---

## Próximos Pasos

1. **Crear fixtures de testing** (`conftest.py`)
2. **Escribir tests** (TDD: Red phase)
3. **Implementar funciones** (TDD: Green phase)
4. **Refactorizar** (TDD: Refactor phase)
5. **Crear ejemplos de uso**
6. **Documentar en README**

---

**Arquitecto**: Equipo Development
**Fecha**: 2025-10-23
**Versión**: 1.0
