# Arquitectura Técnica: Sistema de Análisis de JOINs SQL

## Visión General

Este proyecto implementa un sistema modular para ejecutar, validar y analizar queries SQL con JOINs de forma robusta. La arquitectura sigue principios de **programación funcional** y **arquitectura limpia**.

---

## Principios de Diseño

### 1. Funcional First
- **Sin clases innecesarias**: Solo funciones puras donde sea posible
- **Inmutabilidad**: No modificar parámetros de entrada
- **Sin efectos secundarios**: Funciones predecibles

### 2. Modularidad
- **Separación de responsabilidades**: Cada módulo tiene un propósito claro
- **Alta cohesión**: Funciones relacionadas juntas
- **Bajo acoplamiento**: Módulos independientes

### 3. Calidad del Código
- **Type hints 100%**: Tipado explícito en todo el código
- **Docstrings completos**: Documentación en español con ejemplos
- **Tests primero**: TDD estricto

---

## Módulos del Sistema

### Módulo 1: `ejecutor_joins.py`

**Responsabilidad:** Ejecutar queries con JOINs de forma segura y con logging.

#### Funciones

##### 1.1. `ejecutar_join_simple()`

```python
def ejecutar_join_simple(
    conexion: sqlite3.Connection,
    tabla_izq: str,
    tabla_der: str,
    columna_union_izq: str,
    columna_union_der: str,
    tipo_join: str = "INNER",
    columnas_select: list[str] | None = None
) -> list[dict[str, any]]:
    """
    Ejecuta un JOIN simple entre dos tablas.

    Args:
        conexion: Conexión SQLite activa
        tabla_izq: Nombre de tabla izquierda
        tabla_der: Nombre de tabla derecha
        columna_union_izq: Columna de join en tabla izquierda
        columna_union_der: Columna de join en tabla derecha
        tipo_join: Tipo de JOIN ('INNER', 'LEFT', 'RIGHT', 'FULL')
        columnas_select: Columnas a seleccionar (None = todas)

    Returns:
        Lista de diccionarios con resultados

    Raises:
        ValueError: Si tipo_join no es válido
        sqlite3.Error: Si hay error en la query

    Example:
        >>> resultado = ejecutar_join_simple(
        ...     conn, 'productos', 'categorias',
        ...     'categoria_id', 'id', 'INNER'
        ... )
        >>> len(resultado) > 0
        True
    """
```

**Lógica interna:**
1. Validar parámetros (tipo_join válido, conexión activa)
2. Construir query SQL con parámetros seguros
3. Ejecutar query con manejo de excepciones
4. Convertir resultados a lista de diccionarios
5. Logging de operación (tiempo, filas)

##### 1.2. `ejecutar_join_multiple()`

```python
def ejecutar_join_multiple(
    conexion: sqlite3.Connection,
    tablas: list[dict[str, str]],
    columnas_select: list[str] | None = None
) -> list[dict[str, any]]:
    """
    Ejecuta JOIN de 3+ tablas.

    Args:
        conexion: Conexión SQLite activa
        tablas: Lista de dicts con info de JOIN:
            [
                {'nombre': 'productos', 'alias': 'p'},
                {'nombre': 'categorias', 'alias': 'c',
                 'join': 'INNER', 'on': 'p.categoria_id = c.id'},
                {'nombre': 'ventas', 'alias': 'v',
                 'join': 'LEFT', 'on': 'p.id = v.producto_id'}
            ]
        columnas_select: Columnas a seleccionar

    Returns:
        Lista de diccionarios con resultados

    Raises:
        ValueError: Si tablas está vacía o formato incorrecto
        sqlite3.Error: Si hay error en la query
    """
```

**Lógica interna:**
1. Validar formato de parámetro `tablas`
2. Construir query dinámica con múltiples JOINs
3. Ejecutar con manejo de errores
4. Logging detallado

##### 1.3. `ejecutar_join_con_subconsulta()`

```python
def ejecutar_join_con_subconsulta(
    conexion: sqlite3.Connection,
    query_principal: str,
    subconsulta: str,
    tipo_subconsulta: str = "WHERE"
) -> list[dict[str, any]]:
    """
    Ejecuta JOIN con subconsulta en WHERE, FROM o SELECT.

    Args:
        conexion: Conexión SQLite activa
        query_principal: Query base con placeholder {subconsulta}
        subconsulta: Query interna
        tipo_subconsulta: Ubicación ('WHERE', 'FROM', 'SELECT')

    Returns:
        Lista de diccionarios con resultados
    """
```

---

### Módulo 2: `detector_tipo_join.py`

**Responsabilidad:** Analizar requerimientos y sugerir el tipo de JOIN adecuado.

#### Funciones

##### 2.1. `detectar_tipo_join_necesario()`

```python
def detectar_tipo_join_necesario(
    requerimiento: str,
    incluir_nulls_izq: bool = False,
    incluir_nulls_der: bool = False
) -> str:
    """
    Sugiere tipo de JOIN basándose en requerimiento.

    Args:
        requerimiento: Descripción del problema
        incluir_nulls_izq: ¿Incluir filas sin coincidencia de tabla izq?
        incluir_nulls_der: ¿Incluir filas sin coincidencia de tabla der?

    Returns:
        Tipo de JOIN recomendado ('INNER', 'LEFT', 'RIGHT', 'FULL')

    Logic:
        - INNER: Solo coincidencias (ambos False)
        - LEFT: Todos de izquierda (incluir_nulls_izq=True)
        - RIGHT: Todos de derecha (incluir_nulls_der=True)
        - FULL: Todos de ambos (ambos True)

    Example:
        >>> detectar_tipo_join_necesario(
        ...     "Listar todos los clientes, con o sin pedidos",
        ...     incluir_nulls_izq=True
        ... )
        'LEFT'
    """
```

##### 2.2. `validar_tipo_join()`

```python
def validar_tipo_join(
    tipo_join: str,
    esperado_incluir_nulls: bool
) -> tuple[bool, str]:
    """
    Valida si el tipo de JOIN elegido es correcto.

    Args:
        tipo_join: JOIN elegido ('INNER', 'LEFT', etc.)
        esperado_incluir_nulls: ¿Se espera incluir NULLs?

    Returns:
        (es_valido, mensaje_explicativo)

    Example:
        >>> validar_tipo_join('INNER', esperado_incluir_nulls=True)
        (False, 'INNER JOIN no incluye NULLs, usa LEFT o FULL')
    """
```

---

### Módulo 3: `validador_joins.py`

**Responsabilidad:** Validar integridad de resultados de JOINs.

#### Funciones

##### 3.1. `validar_resultado_join()`

```python
def validar_resultado_join(
    filas_tabla_izq: int,
    filas_tabla_der: int,
    filas_resultado: int,
    tipo_join: str
) -> tuple[bool, str]:
    """
    Detecta pérdida o duplicación de datos en JOIN.

    Args:
        filas_tabla_izq: Filas de tabla izquierda
        filas_tabla_der: Filas de tabla derecha
        filas_resultado: Filas del resultado
        tipo_join: Tipo de JOIN ejecutado

    Returns:
        (es_valido, mensaje_diagnostico)

    Logic:
        - INNER: resultado <= min(izq, der)
        - LEFT: resultado >= izq
        - RIGHT: resultado >= der
        - FULL: resultado >= max(izq, der)
        - Alerta si resultado >> (izq * der) → producto cartesiano

    Example:
        >>> validar_resultado_join(100, 10, 1000, 'INNER')
        (False, 'Posible producto cartesiano: 1000 >> 100')
    """
```

##### 3.2. `contar_filas_join()`

```python
def contar_filas_join(
    conexion: sqlite3.Connection,
    tabla_izq: str,
    tabla_der: str,
    query_join: str
) -> dict[str, int]:
    """
    Cuenta filas de tablas base y resultado para verificar integridad.

    Args:
        conexion: Conexión SQLite activa
        tabla_izq: Tabla izquierda
        tabla_der: Tabla derecha
        query_join: Query completa del JOIN

    Returns:
        {
            'filas_izq': int,
            'filas_der': int,
            'filas_resultado': int,
            'ratio': float  # resultado / (izq * der)
        }
    """
```

##### 3.3. `detectar_producto_cartesiano()`

```python
def detectar_producto_cartesiano(
    filas_izq: int,
    filas_der: int,
    filas_resultado: int,
    umbral: float = 0.8
) -> tuple[bool, str]:
    """
    Detecta si el JOIN generó un producto cartesiano accidental.

    Args:
        filas_izq: Filas tabla izquierda
        filas_der: Filas tabla derecha
        filas_resultado: Filas resultado
        umbral: Umbral de alerta (0.8 = 80% del producto total)

    Returns:
        (es_producto_cartesiano, mensaje)

    Logic:
        Si filas_resultado > (filas_izq * filas_der * umbral):
            Producto cartesiano detectado
    """
```

---

### Módulo 4: `generador_reportes.py`

**Responsabilidad:** Generar reportes complejos con JOINs múltiples.

#### Funciones

##### 4.1. `generar_reporte_ventas()`

```python
def generar_reporte_ventas(
    conexion: sqlite3.Connection,
    fecha_inicio: str,
    fecha_fin: str,
    agrupar_por: str = "categoria"
) -> list[dict[str, any]]:
    """
    Genera reporte de ventas con múltiples JOINs.

    Args:
        conexion: Conexión SQLite activa
        fecha_inicio: Fecha inicial (YYYY-MM-DD)
        fecha_fin: Fecha final (YYYY-MM-DD)
        agrupar_por: 'categoria', 'producto', 'cliente', 'ciudad'

    Returns:
        Lista de dicts con:
            - nombre: str (categoría/producto/cliente)
            - total_ventas: float
            - unidades_vendidas: int
            - ticket_promedio: float
            - porcentaje_total: float

    SQL Interno:
        - JOIN: categorias + productos + ventas + clientes
        - GROUP BY: Según agrupar_por
        - CASE WHEN: Para calcular porcentajes
        - ORDER BY: total_ventas DESC
    """
```

##### 4.2. `generar_top_clientes()`

```python
def generar_top_clientes(
    conexion: sqlite3.Connection,
    top_n: int = 10,
    metrica: str = "gasto_total"
) -> list[dict[str, any]]:
    """
    Genera top N clientes usando subconsultas.

    Args:
        conexion: Conexión SQLite activa
        top_n: Número de clientes a retornar
        metrica: 'gasto_total', 'num_pedidos', 'ticket_promedio'

    Returns:
        Lista de dicts con:
            - nombre: str
            - email: str
            - gasto_total: float
            - num_pedidos: int
            - ticket_promedio: float
            - segmento: str ('VIP', 'Regular', 'Nuevo')

    SQL Interno:
        - Subconsulta en HAVING: Filtrar por percentil
        - CASE WHEN: Segmentación de clientes
        - ORDER BY + LIMIT: Top N
    """
```

##### 4.3. `generar_analisis_categorias()`

```python
def generar_analisis_categorias(
    conexion: sqlite3.Connection
) -> list[dict[str, any]]:
    """
    Análisis completo de categorías con CASE WHEN y GROUP BY.

    Args:
        conexion: Conexión SQLite activa

    Returns:
        Lista de dicts con:
            - categoria: str
            - num_productos: int
            - stock_total: int
            - valor_inventario: float
            - ingresos_totales: float
            - clasificacion: str ('Alta rentabilidad', 'Media', 'Baja')
            - estado_stock: str ('Crítico', 'Normal', 'Sobrecargado')

    SQL Interno:
        - LEFT JOIN: categorias + productos + ventas
        - CASE WHEN anidado: Clasificación dual
        - GROUP BY: categoria
        - ORDER BY: ingresos_totales DESC
    """
```

---

## Flujo de Datos

```
┌─────────────────┐
│  Usuario/Test   │
└────────┬────────┘
         │
         ▼
┌────────────────────────────────┐
│  1. ejecutor_joins.py          │
│  - ejecutar_join_simple()      │
│  - ejecutar_join_multiple()    │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  2. detector_tipo_join.py      │
│  - detectar_tipo_join_...()    │
│  - validar_tipo_join()         │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  3. validador_joins.py         │
│  - validar_resultado_join()    │
│  - detectar_producto_...()     │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  4. generador_reportes.py      │
│  - generar_reporte_ventas()    │
│  - generar_top_clientes()      │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────┐
│  Resultado Final   │
└────────────────────┘
```

---

## Manejo de Errores

### Estrategia

1. **Validación de parámetros**: Al inicio de cada función
2. **Excepciones específicas**: ValueError, TypeError, sqlite3.Error
3. **Mensajes claros**: Indicar qué salió mal y por qué
4. **No silenciar errores**: Siempre propagar o lanzar nuevos

### Ejemplo de Manejo

```python
def ejecutar_join_simple(...) -> list[dict]:
    # 1. Validación
    if tipo_join not in ['INNER', 'LEFT', 'RIGHT', 'FULL']:
        raise ValueError(
            f"tipo_join inválido: '{tipo_join}'. "
            f"Debe ser: INNER, LEFT, RIGHT o FULL"
        )

    if conexion is None or not isinstance(conexion, sqlite3.Connection):
        raise TypeError("conexion debe ser sqlite3.Connection válida")

    # 2. Ejecución con try-except
    try:
        cursor = conexion.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error al ejecutar JOIN: {str(e)}")

    # 3. Post-validación
    if not resultado:
        logging.warning(f"JOIN retornó 0 filas")

    return resultado
```

---

## Logging

### Estrategia

- **Nivel INFO**: Operaciones exitosas
- **Nivel WARNING**: Situaciones inusuales pero no errores
- **Nivel ERROR**: Errores capturados

### Formato

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Ejemplo de Logs

```
2025-10-25 10:15:30 - ejecutor_joins - INFO - Ejecutando INNER JOIN: productos + categorias
2025-10-25 10:15:30 - ejecutor_joins - INFO - JOIN completado: 9 filas en 0.002s
2025-10-25 10:15:31 - validador_joins - WARNING - Resultado de JOIN mayor a esperado (posible duplicación)
```

---

## Base de Datos de Prueba

### Estructura

```sql
-- Tablas principales
CREATE TABLE categorias (id, nombre, descripcion);
CREATE TABLE productos (id, nombre, precio, categoria_id, stock, activo);
CREATE TABLE clientes (id, nombre, email, fecha_registro, ciudad);
CREATE TABLE ventas (id, cliente_id, producto_id, cantidad, fecha, total);

-- Datos de prueba
- 4 categorías
- 10 productos
- 5 clientes
- 10 ventas
```

Ver `conftest.py` para scripts completos de setup.

---

## Testing Strategy

### Pirámide de Tests

```
         /\
        /  \     5 tests de integración
       /────\
      /      \   15 tests de módulo
     /────────\
    /          \ 30 tests unitarios
   /────────────\
```

**Total: 50 tests**

### Fixtures de pytest (conftest.py)

```python
@pytest.fixture
def conexion_db():
    """Base de datos SQLite en memoria con datos de prueba."""
    conn = sqlite3.connect(':memory:')
    # Crear tablas y datos
    yield conn
    conn.close()

@pytest.fixture
def datos_productos():
    """Datos de prueba de productos."""
    return [
        {'id': 1, 'nombre': 'Laptop', 'precio': 899.99},
        # ...
    ]
```

### Nomenclatura de Tests

```python
# Patrón: test_<funcion>_<escenario>_<resultado_esperado>

def test_ejecutar_join_simple_inner_join_devuelve_solo_coincidencias():
    ...

def test_ejecutar_join_simple_left_join_incluye_nulls():
    ...

def test_validar_resultado_join_producto_cartesiano_detecta_error():
    ...
```

---

## Dependencias

### Producción

```
# requirements.txt
# (SQLite3 viene con Python estándar)
```

### Desarrollo

```
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0
```

---

## Decisiones de Diseño

### ¿Por qué funciones en vez de clases?

- **Simplicidad**: El problema no requiere estado persistente
- **Testabilidad**: Funciones puras son más fáciles de testear
- **Composición**: Funciones se pueden combinar fácilmente
- **YAGNI**: No necesitamos herencia ni polimorfismo

### ¿Por qué SQLite?

- **Embebido**: No requiere servidor externo
- **Portable**: Archivo único o en memoria
- **Suficiente**: Soporta JOINs complejos
- **Pedagógico**: Fácil de configurar para estudiantes

### ¿Por qué Type Hints?

- **Documentación**: El tipo es auto-documentación
- **Seguridad**: Detecta errores antes de ejecución
- **IDE Support**: Autocompletado mejor
- **Estándar**: PEP 484

---

## Mejoras Futuras (Opcional)

1. **Soporte para PostgreSQL/MySQL**: Agregar adaptadores
2. **Visualización de resultados**: Generar gráficos con matplotlib
3. **CLI**: Interfaz de línea de comandos
4. **API REST**: Servir funciones vía FastAPI
5. **Optimización**: Caché de queries repetidas

---

## Referencias

- **PEP 8**: Guía de estilo de Python
- **PEP 484**: Type Hints
- **Clean Code** (Robert C. Martin)
- **Test-Driven Development** (Kent Beck)
- **Effective Python** (Brett Slatkin)

---

**Última actualización:** 2025-10-25
**Versión:** 1.0.0
**Autor:** Arquitecto de Software (Sub-Agente Master Data Engineering)
