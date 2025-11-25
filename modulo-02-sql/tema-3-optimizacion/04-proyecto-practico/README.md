# Proyecto Práctico: Sistema de Análisis y Optimización SQL

Sistema para analizar consultas SQL, detectar problemas de rendimiento y recomendar índices óptimos.

## 🎯 Objetivos

- **Parsear consultas SQL** y extraer tablas, columnas, JOINs
- **Detectar anti-patrones** como SELECT *, funciones en WHERE
- **Recomendar índices** basándose en análisis de la consulta
- **Generar SQL** para crear índices óptimos
- **Aplicar TDD** con >80% de cobertura

## 📚 Conceptos Aplicados

### Optimización SQL
- **Índices simples**: En columnas filtradas (WHERE, JOIN)
- **Índices compuestos**: Múltiples columnas usadas juntas
- **Priorización**: Basada en selectividad y uso

### Análisis de Consultas
- **Parsing**: Extracción de componentes SQL
- **Detección de patrones**: SELECT *, funciones en WHERE
- **Heurísticas**: Reglas para recomendar optimizaciones

### Buenas Prácticas
- **TDD (Test-Driven Development)**: Tests antes de implementación
- **Type Hints**: Tipado explícito en todas las funciones
- **Funciones puras**: Sin efectos secundarios
- **Cobertura >80%**: Garantía de calidad

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── query_parser.py         # Parser de consultas SQL
│   └── index_recommender.py    # Recomendador de índices
├── tests/
│   ├── __init__.py
│   ├── test_query_parser.py        # 26 tests
│   └── test_index_recommender.py   # 14 tests
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Instalación

```bash
# Activar entorno virtual
cd modulo-02-sql/tema-3-optimizacion/04-proyecto-practico

# En Windows:
..\..\..\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Ejecutar Tests

```bash
# Todos los tests
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html --cov-report=term

# Solo un módulo
pytest tests/test_query_parser.py -v
```

**Resultados**:
- ✅ **40 tests pasando** (100% success rate)
- ✅ **80% cobertura** (cumple objetivo ≥80%)

## 📦 Módulos Implementados

### 1. Query Parser (`query_parser.py`)

Parser de consultas SQL que extrae componentes clave.

#### Funciones Principales

**`extraer_tablas(query: str) -> list[str]`**
```python
from src.query_parser import extraer_tablas

# Ejemplo
query = "SELECT * FROM usuarios u JOIN pedidos p ON u.id = p.usuario_id"
tablas = extraer_tablas(query)
print(tablas)  # ['usuarios', 'pedidos']
```

**`extraer_columnas_where(query: str) -> list[str]`**
```python
from src.query_parser import extraer_columnas_where

query = "SELECT * FROM usuarios WHERE edad > 25 AND ciudad = 'Madrid'"
columnas = extraer_columnas_where(query)
print(columnas)  # ['edad', 'ciudad']
```

**`extraer_columnas_select(query: str) -> list[str]`**
```python
from src.query_parser import extraer_columnas_select

query = "SELECT id, nombre, email FROM usuarios"
columnas = extraer_columnas_select(query)
print(columnas)  # ['id', 'nombre', 'email']
```

**`detectar_select_asterisco(query: str) -> bool`**
```python
from src.query_parser import detectar_select_asterisco

detectar_select_asterisco("SELECT * FROM usuarios")  # True
detectar_select_asterisco("SELECT id, nombre FROM usuarios")  # False
```

**`detectar_funciones_en_where(query: str) -> dict`**
```python
from src.query_parser import detectar_funciones_en_where

query = "SELECT * FROM ventas WHERE YEAR(fecha) = 2024"
resultado = detectar_funciones_en_where(query)
print(resultado)
# {'funciones': ['YEAR'], 'columnas_afectadas': ['fecha']}
```

**`extraer_joins(query: str) -> list[dict]`**
```python
from src.query_parser import extraer_joins

query = "SELECT * FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id"
joins = extraer_joins(query)
print(joins[0])
# {'tipo': 'INNER JOIN', 'tabla': 'pedidos', 'columnas_join': ['id', 'usuario_id']}
```

---

### 2. Index Recommender (`index_recommender.py`)

Recomendador inteligente de índices basado en análisis de consultas.

#### Funciones Principales

**`recomendar_indices(query: str) -> list[dict]`**
```python
from src.index_recommender import recomendar_indices

query = "SELECT * FROM usuarios WHERE email = 'test@example.com'"
recomendaciones = recomendar_indices(query)

for rec in recomendaciones:
    print(f"Tabla: {rec['tabla']}")
    print(f"Columna: {rec['columna']}")
    print(f"Prioridad: {rec['prioridad']}")
    print(f"Razón: {rec['razon']}")
    print()

# Output:
# Tabla: usuarios
# Columna: email
# Prioridad: 80
# Razón: Columna 'email' usada en WHERE
```

**`generar_sql_create_index(tabla: str, columna: str) -> str`**
```python
from src.index_recommender import generar_sql_create_index

sql = generar_sql_create_index("usuarios", "email")
print(sql)
# CREATE INDEX idx_usuarios_email ON usuarios(email);

# Índice compuesto
sql = generar_sql_create_index("ventas", "fecha, tienda_id")
print(sql)
# CREATE INDEX idx_ventas_fecha_tienda_id ON ventas(fecha, tienda_id);
```

**`calcular_prioridad_indice(...) -> int`**
```python
from src.index_recommender import calcular_prioridad_indice

# Columna en WHERE
prioridad = calcular_prioridad_indice(
    columna="email",
    en_where=True,
    en_join=False,
    en_order_by=False
)
print(prioridad)  # 80

# Columna en WHERE y JOIN (máxima prioridad)
prioridad = calcular_prioridad_indice(
    columna="id",
    en_where=True,
    en_join=True,
    en_order_by=False
)
print(prioridad)  # 150
```

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Analizar consulta lenta

```python
from src.query_parser import extraer_tablas, extraer_columnas_where, detectar_select_asterisco
from src.index_recommender import recomendar_indices, generar_sql_create_index

# Consulta problemática
query = """
SELECT *
FROM usuarios
WHERE email = 'test@example.com' AND ciudad = 'Madrid'
"""

# Análisis
print("=== ANÁLISIS DE CONSULTA ===")
print(f"Tablas: {extraer_tablas(query)}")
print(f"Usa SELECT *: {detectar_select_asterisco(query)}")
print(f"Columnas filtradas: {extraer_columnas_where(query)}")

# Recomendaciones
print("\n=== RECOMENDACIONES ===")
recomendaciones = recomendar_indices(query)

for i, rec in enumerate(recomendaciones, 1):
    print(f"\n{i}. {rec['tipo'].upper()} en {rec['tabla']}.{rec['columna']}")
    print(f"   Prioridad: {rec['prioridad']}/100")
    print(f"   Razón: {rec['razon']}")
    print(f"   SQL: {generar_sql_create_index(rec['tabla'], rec['columna'])}")
```

**Output**:
```
=== ANÁLISIS DE CONSULTA ===
Tablas: ['usuarios']
Usa SELECT *: True
Columnas filtradas: ['email', 'ciudad']

=== RECOMENDACIONES ===

1. COMPUESTO en usuarios.email, ciudad
   Prioridad: 85/100
   Razón: Índice compuesto para múltiples filtros en WHERE
   SQL: CREATE INDEX idx_usuarios_email_ciudad ON usuarios(email, ciudad);

2. SIMPLE en usuarios.email
   Prioridad: 80/100
   Razón: Columna 'email' usada en WHERE
   SQL: CREATE INDEX idx_usuarios_email ON usuarios(email);

3. SIMPLE en usuarios.ciudad
   Prioridad: 80/100
   Razón: Columna 'ciudad' usada en WHERE
   SQL: CREATE INDEX idx_usuarios_ciudad ON usuarios(ciudad);
```

### Ejemplo 2: Detectar anti-patrones

```python
from src.query_parser import detectar_funciones_en_where

query_mala = "SELECT * FROM ventas WHERE YEAR(fecha) = 2024"

problemas = detectar_funciones_en_where(query_mala)

if problemas['funciones']:
    print("⚠️ ANTI-PATRÓN DETECTADO: Funciones en WHERE")
    print(f"Funciones: {problemas['funciones']}")
    print(f"Columnas afectadas: {problemas['columnas_afectadas']}")
    print("\n✅ SOLUCIÓN:")
    print("Reescribe como: WHERE fecha >= '2024-01-01' AND fecha < '2025-01-01'")
```

### Ejemplo 3: Optimizar consulta con JOIN

```python
query_join = """
SELECT u.nombre, COUNT(p.id) as total_pedidos
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE u.ciudad = 'Madrid'
GROUP BY u.id, u.nombre
"""

print("=== ANÁLISIS DE JOIN ===")

# Extraer componentes
tablas = extraer_tablas(query_join)
joins = extraer_joins(query_join)
columnas_where = extraer_columnas_where(query_join)

print(f"Tablas involucradas: {tablas}")
print(f"Tipo de JOIN: {joins[0]['tipo'] if joins else 'No JOIN'}")
print(f"Columnas de JOIN: {joins[0]['columnas_join'] if joins else []}")
print(f"Filtros: {columnas_where}")

# Recomendar índices
print("\n=== ÍNDICES RECOMENDADOS ===")
recomendaciones = recomendar_indices(query_join)

for rec in recomendaciones[:3]:  # Top 3
    sql = generar_sql_create_index(rec['tabla'], rec['columna'])
    print(f"• {sql}")
```

**Output**:
```
=== ANÁLISIS DE JOIN ===
Tablas involucradas: ['usuarios', 'pedidos']
Tipo de JOIN: LEFT JOIN
Columnas de JOIN: ['id', 'usuario_id']
Filtros: ['ciudad']

=== ÍNDICES RECOMENDADOS ===
• CREATE INDEX idx_usuarios_ciudad ON usuarios(ciudad);
• CREATE INDEX idx_pedidos_usuario_id ON pedidos(usuario_id);
```

---

## 🧪 Cobertura de Tests

```
Name                       Stmts   Miss  Cover
-----------------------------------------------
src/query_parser.py          199     46    77%
src/index_recommender.py      44      3    93%
-----------------------------------------------
TOTAL                        243     49    80%
```

**Detalle por módulo**:

| Módulo | Tests | Cobertura | Estado |
|--------|-------|-----------|--------|
| `query_parser.py` | 26 | 77% | ✅ |
| `index_recommender.py` | 14 | 93% | ✅ |
| **TOTAL** | **40** | **80%** | ✅ **APROBADO** |

---

## 🔧 Tecnologías Utilizadas

- **Python 3.13+**: Lenguaje principal
- **sqlparse**: Parsing de consultas SQL
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **black**: Formateo automático
- **flake8**: Linting
- **mypy**: Type checking

---

## 📊 Arquitectura

### Diseño Funcional

El proyecto sigue un diseño **funcional puro**:
- **Sin clases** (excepto para conectores externos)
- **Funciones pequeñas** (<50 líneas)
- **Sin efectos secundarios**: Funciones predecibles
- **Composabilidad**: Funciones que se combinan fácilmente

### Flujo de Datos

```
┌─────────────┐
│ Query SQL   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  query_parser.py    │  ← Extrae componentes
│  - Tablas           │
│  - Columnas         │
│  - JOINs            │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────┐
│ index_recommender.py │  ← Analiza y recomienda
│  - Calcula prioridad │
│  - Genera SQL        │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────┐
│ Recomendaciones     │
│ + SQL de índices    │
└─────────────────────┘
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'sqlparse'"
**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: Tests fallan con "ImportError"
**Solución**: Ejecutar desde el directorio del proyecto
```bash
cd modulo-02-sql/tema-3-optimizacion/04-proyecto-practico
pytest -v
```

### Error: Cobertura <80%
**Solución**: Verificar que todos los tests pasen
```bash
pytest --cov=src --cov-report=term
```

---

## 📚 Recursos Adicionales

- [sqlparse Documentation](https://sqlparse.readthedocs.io/)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [MySQL EXPLAIN](https://dev.mysql.com/doc/refman/8.0/en/explain.html)
- [SQL Indexing Best Practices](https://use-the-index-luke.com/)

---

## 🎯 Próximos Pasos

1. Agregar soporte para **ORDER BY** en recomendaciones
2. Detectar **subconsultas correlacionadas**
3. Analizar **cardinalidad** de columnas
4. Simular **EXPLAIN** output básico
5. Crear **CLI** para análisis en línea de comandos
6. Integrar con **bases de datos reales** para obtener estadísticas

---

**Proyecto completado** ✅
**Tests**: 40/40 pasando
**Cobertura**: 80%
**Calidad**: TDD con funciones puras

**¡Éxito en tu aprendizaje de Optimización SQL!** 🚀
