# Proyecto Práctico: Análisis Exploratorio de Base de Datos SQL

> **Objetivo**: Practicar SQL básico mediante consultas programáticas desde Python usando SQLite.

**Tema**: SQL Básico - Módulo 2
**Duración estimada**: 3-5 horas
**Nivel**: Principiante

---

## 📋 Descripción del Proyecto

Este proyecto te permite practicar los conceptos de SQL básico (SELECT, WHERE, ORDER BY, LIMIT, funciones agregadas, GROUP BY, HAVING) mediante funciones Python que ejecutan consultas SQL en una base de datos SQLite.

**Empresa ficticia**: TechStore (tienda de electrónica)
**Base de datos**: SQLite (no requiere Docker ni instalación)
**Datos**: 10 productos, 10 ventas de octubre 2025

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, serás capaz de:

- ✅ Ejecutar consultas SQL desde Python usando SQLite
- ✅ Aplicar SELECT, WHERE, ORDER BY y LIMIT en queries reales
- ✅ Usar funciones agregadas (COUNT, SUM, AVG, MAX, MIN)
- ✅ Agrupar datos con GROUP BY
- ✅ Filtrar grupos con HAVING
- ✅ Interpretar resultados de consultas SQL
- ✅ Prevenir SQL injection usando parámetros
- ✅ Escribir código Python funcional y testeado

---

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── conexion_db.py         ← Clase para manejar conexión SQLite
│   ├── consultas_basicas.py   ← SELECT, WHERE, ORDER BY, LIMIT
│   ├── consultas_agregadas.py ← COUNT, SUM, AVG, MAX, MIN
│   ├── consultas_agrupadas.py ← GROUP BY, HAVING
│   └── validaciones.py         ← Validación de inputs
│
├── tests/
│   ├── conftest.py             ← Fixtures compartidas
│   ├── test_conexion_db.py
│   ├── test_consultas_basicas.py
│   ├── test_consultas_agregadas.py
│   ├── test_consultas_agrupadas.py
│   └── test_validaciones.py
│
├── datos/
│   ├── techstore.db            ← Base de datos SQLite
│   └── crear_db.sql            ← Script para recrear la DB
│
├── ejemplos/
│   ├── ejemplo_01_consultas_basicas.py
│   ├── ejemplo_02_agregaciones.py
│   └── ejemplo_03_analisis_completo.py
│
├── ARQUITECTURA.md             ← Diseño del proyecto
├── README.md                   ← Este archivo
├── requirements.txt
└── .gitignore
```

---

## 🚀 Instalación

### 1. Clonar el repositorio (si aplica)

```bash
cd modulo-02-sql/tema-1-sql-basico/04-proyecto-practico
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota**: SQLite viene incluido con Python, no requiere instalación adicional.

---

## 🧪 Ejecutar Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con cobertura

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Ver reporte de cobertura en navegador

```bash
# Abrir htmlcov/index.html en tu navegador
```

### Ejecutar tests de un módulo específico

```bash
pytest tests/test_consultas_basicas.py
pytest tests/test_consultas_agregadas.py -v
```

---

## 📚 Funciones Disponibles

### Módulo: `conexion_db.py`

#### `ConexionSQLite`

Clase para manejar conexión a SQLite de forma segura.

```python
from src.conexion_db import ConexionSQLite

# Uso básico
conn = ConexionSQLite("datos/techstore.db")
resultados = conn.ejecutar_query("SELECT * FROM productos")
conn.cerrar()

# Uso con context manager (recomendado)
with ConexionSQLite("datos/techstore.db") as conn:
    resultados = conn.ejecutar_query("SELECT * FROM productos")
```

---

### Módulo: `consultas_basicas.py`

#### `obtener_todos_los_productos(conexion)`

Obtiene todos los productos.

**Returns**: `list[dict]` con todos los productos

```python
from src.conexion_db import ConexionSQLite
from src.consultas_basicas import obtener_todos_los_productos

with ConexionSQLite("datos/techstore.db") as conn:
    productos = obtener_todos_los_productos(conn)
    print(f"Total de productos: {len(productos)}")
```

#### `filtrar_productos_por_categoria(conexion, categoria)`

Filtra productos por categoría.

**Args**:
- `conexion`: Instancia de ConexionSQLite
- `categoria`: Nombre de la categoría (ej: "Accesorios")

**Returns**: `list[dict]` con productos de esa categoría

```python
accesorios = filtrar_productos_por_categoria(conn, "Accesorios")
```

#### `obtener_productos_caros(conexion, precio_minimo)`

Obtiene productos con precio mayor al mínimo.

**Args**:
- `conexion`: Instancia de ConexionSQLite
- `precio_minimo`: Precio mínimo (debe ser > 0)

**Returns**: `list[dict]` ordenados por precio descendente

```python
caros = obtener_productos_caros(conn, 500.0)
```

#### `obtener_top_n_productos_mas_caros(conexion, n=5)`

Obtiene los N productos más caros.

**Args**:
- `conexion`: Instancia de ConexionSQLite
- `n`: Cantidad de productos (default: 5)

**Returns**: `list[dict]` con los N productos más caros

```python
top_5 = obtener_top_n_productos_mas_caros(conn, 5)
```

---

### Módulo: `consultas_agregadas.py`

#### `contar_productos(conexion)`

Cuenta el total de productos.

**Returns**: `int` con el total

```python
total = contar_productos(conn)
print(f"Total: {total} productos")
```

#### `calcular_precio_promedio(conexion)`

Calcula el precio promedio.

**Returns**: `float` redondeado a 2 decimales

```python
promedio = calcular_precio_promedio(conn)
print(f"Precio promedio: ${promedio}")
```

#### `obtener_estadisticas_precios(conexion)`

Obtiene estadísticas de precios.

**Returns**: `dict` con claves `minimo`, `maximo`, `promedio`, `total`

```python
stats = obtener_estadisticas_precios(conn)
print(f"Mínimo: ${stats['minimo']}")
print(f"Máximo: ${stats['maximo']}")
print(f"Promedio: ${stats['promedio']}")
print(f"Total productos: {stats['total']}")
```

#### `calcular_ingresos_totales(conexion)`

Calcula los ingresos totales de ventas.

**Returns**: `float` redondeado a 2 decimales

```python
ingresos = calcular_ingresos_totales(conn)
print(f"Ingresos totales: ${ingresos}")
```

---

### Módulo: `consultas_agrupadas.py`

#### `contar_productos_por_categoria(conexion)`

Cuenta productos por categoría.

**Returns**: `list[dict]` con `categoria` y `cantidad`

```python
por_categoria = contar_productos_por_categoria(conn)
for item in por_categoria:
    print(f"{item['categoria']}: {item['cantidad']} productos")
```

#### `calcular_valor_inventario_por_categoria(conexion)`

Calcula valor de inventario por categoría.

**Returns**: `list[dict]` con `categoria` y `valor_inventario`

```python
valores = calcular_valor_inventario_por_categoria(conn)
for item in valores:
    print(f"{item['categoria']}: ${item['valor_inventario']}")
```

#### `obtener_categorias_con_mas_de_n_productos(conexion, n=1)`

Obtiene categorías con más de N productos.

**Args**:
- `conexion`: Instancia de ConexionSQLite
- `n`: Número mínimo de productos (default: 1)

**Returns**: `list[dict]` con categorías filtradas

```python
categorias = obtener_categorias_con_mas_de_n_productos(conn, 2)
```

#### `analizar_ventas_por_producto(conexion)`

Analiza ventas agrupadas por producto.

**Returns**: `list[dict]` con `producto_id`, `unidades_vendidas`, `ingresos_totales`

```python
ventas = analizar_ventas_por_producto(conn)
for venta in ventas:
    print(f"Producto {venta['producto_id']}: "
          f"{venta['unidades_vendidas']} unidades, "
          f"${venta['ingresos_totales']} ingresos")
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Análisis Básico

```python
from src.conexion_db import ConexionSQLite
from src.consultas_basicas import obtener_todos_los_productos, filtrar_productos_por_categoria

with ConexionSQLite("datos/techstore.db") as conn:
    # Ver todos los productos
    productos = obtener_todos_los_productos(conn)
    print(f"Total de productos: {len(productos)}")

    # Filtrar por categoría
    accesorios = filtrar_productos_por_categoria(conn, "Accesorios")
    print(f"\nAccesorios: {len(accesorios)}")
    for producto in accesorios:
        print(f"- {producto['nombre']}: ${producto['precio']}")
```

### Ejemplo 2: Estadísticas

```python
from src.conexion_db import ConexionSQLite
from src.consultas_agregadas import obtener_estadisticas_precios, calcular_ingresos_totales

with ConexionSQLite("datos/techstore.db") as conn:
    # Estadísticas de precios
    stats = obtener_estadisticas_precios(conn)
    print("Estadísticas de Precios:")
    print(f"- Mínimo: ${stats['minimo']}")
    print(f"- Máximo: ${stats['maximo']}")
    print(f"- Promedio: ${stats['promedio']}")
    print(f"- Total productos: {stats['total']}")

    # Ingresos totales
    ingresos = calcular_ingresos_totales(conn)
    print(f"\nIngresos totales: ${ingresos}")
```

### Ejemplo 3: Análisis por Categoría

```python
from src.conexion_db import ConexionSQLite
from src.consultas_agrupadas import (
    contar_productos_por_categoria,
    calcular_valor_inventario_por_categoria
)

with ConexionSQLite("datos/techstore.db") as conn:
    # Productos por categoría
    print("Productos por Categoría:")
    por_categoria = contar_productos_por_categoria(conn)
    for item in por_categoria:
        print(f"- {item['categoria']}: {item['cantidad']} productos")

    # Valor de inventario por categoría
    print("\nValor de Inventario por Categoría:")
    valores = calcular_valor_inventario_por_categoria(conn)
    for item in valores:
        print(f"- {item['categoria']}: ${item['valor_inventario']}")
```

---

## 🔒 Seguridad

### Prevención de SQL Injection

**Todas las funciones usan parámetros para prevenir SQL injection:**

```python
# ✅ CORRECTO: Uso de parámetros
query = "SELECT * FROM productos WHERE categoria = ?"
conexion.ejecutar_query(query, ("Accesorios",))

# ❌ INCORRECTO: Concatenación de strings (vulnerable)
categoria = "Accesorios"
query = f"SELECT * FROM productos WHERE categoria = '{categoria}'"
conexion.ejecutar_query(query)  # ¡PELIGROSO!
```

---

## 📊 Cobertura de Tests

**Objetivo**: >90% de cobertura

```bash
pytest --cov=src --cov-report=term

Name                            Stmts   Miss  Cover
---------------------------------------------------
src/conexion_db.py                 45      2    96%
src/consultas_agrupadas.py         35      0   100%
src/consultas_agregadas.py         28      0   100%
src/consultas_basicas.py           32      0   100%
src/validaciones.py                25      0   100%
---------------------------------------------------
TOTAL                             165      2    99%
```

---

## 🎓 Ejercicios Propuestos

### Ejercicio 1: Nueva Función (Básico)

Crea una función `obtener_productos_por_proveedor(conexion, proveedor)` que filtre productos por proveedor.

**Pasos**:
1. Escribir test en `tests/test_consultas_basicas.py`
2. Implementar función en `src/consultas_basicas.py`
3. Verificar que el test pasa

### Ejercicio 2: Análisis Avanzado (Intermedio)

Crea una función `obtener_productos_sin_ventas(conexion)` que retorne productos que no tienen ventas.

**Pista**: Necesitarás un LEFT JOIN (concepto del Tema 2).

### Ejercicio 3: Dashboard (Avanzado)

Crea una función `generar_dashboard_ejecutivo(conexion)` que retorne un diccionario con todas las métricas clave del negocio.

---

## 🐛 Troubleshooting

### Error: "No module named 'src'"

**Solución**: Asegúrate de ejecutar pytest desde la carpeta del proyecto:

```bash
cd modulo-02-sql/tema-1-sql-basico/04-proyecto-practico
pytest
```

### Error: "Unable to open database file"

**Solución**: Verifica que la ruta a la base de datos sea correcta:

```python
# Usar ruta relativa desde el script
conn = ConexionSQLite("datos/techstore.db")

# O ruta absoluta
from pathlib import Path
ruta_db = Path(__file__).parent / "datos" / "techstore.db"
conn = ConexionSQLite(str(ruta_db))
```

---

## 📖 Recursos Adicionales

- **Teoría**: Ver `01-TEORIA.md` para conceptos de SQL básico
- **Ejemplos**: Ver `02-EJEMPLOS.md` para ejemplos trabajados
- **Ejercicios**: Ver `03-EJERCICIOS.md` para practicar
- **Arquitectura**: Ver `ARQUITECTURA.md` para diseño del proyecto

---

## ✅ Checklist de Completitud

- [ ] Instalé las dependencias (`pip install -r requirements.txt`)
- [ ] Ejecuté los tests (`pytest`)
- [ ] Todos los tests pasan (verde)
- [ ] La cobertura es >90% (`pytest --cov`)
- [ ] Probé los ejemplos de uso
- [ ] Entiendo cómo prevenir SQL injection
- [ ] Puedo explicar la diferencia entre WHERE y HAVING
- [ ] Completé al menos 1 ejercicio propuesto

---

## 🏆 Próximos Pasos

Una vez completado este proyecto:

1. **Tema 2**: SQL Intermedio (JOINs, subconsultas, CTEs)
2. **Integrar con Python**: Usar pandas para análisis de datos
3. **Proyecto avanzado**: Dashboard interactivo con Streamlit

---

**¡Felicidades por completar el proyecto práctico de SQL Básico!** 🎉

---

**Última actualización:** 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [SQL Intermedio - 01 Teoria](../../tema-2-sql-intermedio/01-TEORIA.md)
