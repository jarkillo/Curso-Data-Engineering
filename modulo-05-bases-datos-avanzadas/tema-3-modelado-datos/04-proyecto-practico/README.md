# Proyecto Práctico: Sistema de Diseño y Validación de Data Warehouse

Sistema para validar esquemas dimensionales (Star Schema) y generar DDL automáticamente para Data Warehouses.

## 🎯 Objetivos

- **Validar esquemas dimensionales** (Star Schema) programáticamente
- **Generar DDL automáticamente** a partir de definiciones de esquemas
- **Identificar fact tables y dimensiones** en esquemas complejos
- **Aplicar best practices** de modelado dimensional
- **Dominar TDD** con >80% de cobertura

## 📚 Conceptos Aplicados

### Modelado Dimensional
- **Star Schema**: Esquema estrella con fact table central y dimensiones
- **Fact Table**: Tabla de hechos con métricas numéricas y FKs a dimensiones
- **Dimension Tables**: Tablas descriptivas con contexto de negocio
- **Foreign Keys**: Relaciones entre fact table y dimensiones

### Generación de DDL
- **CREATE TABLE**: Generación automática de esquemas SQL
- **Índices**: Optimización automática con índices en FKs
- **Constraints**: Validación de integridad referencial

### Buenas Prácticas
- **TDD**: Test-Driven Development con 98% cobertura
- **Type Hints**: Tipado explícito en Python
- **Validación**: Verificación programática de esquemas
- **Funciones puras**: Sin efectos secundarios

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── schema_validator.py       # Validación de esquemas (57 líneas, 96% cov)
│   └── ddl_generator.py          # Generación de DDL (63 líneas, 100% cov)
├── tests/
│   ├── __init__.py
│   ├── test_schema_validator.py  # 14 tests
│   └── test_ddl_generator.py     # 11 tests
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 Instalación

```bash
# Activar entorno virtual
cd modulo-05-bases-datos-avanzadas/tema-3-modelado-datos/04-proyecto-practico

# En Windows:
..\..\..\.venv\Scripts\Activate.ps1

# En Linux/Mac:
source ../../../.venv/bin/activate

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
pytest tests/test_schema_validator.py -v
```

**Resultados**:
- ✅ **25 tests pasando** (100% success rate)
- ✅ **98% cobertura** (supera objetivo ≥80%)
- ✅ **121 statements**, solo 2 misses

## 📦 Módulos Implementados

### 1. Schema Validator (`schema_validator.py`)

Funciones para validar esquemas dimensionales.

#### `identificar_fact_table(schema: dict) -> str`

Identifica la tabla de hechos en un esquema.

```python
from src.schema_validator import identificar_fact_table

schema = {
    "fact_ventas": {
        "tipo": "fact",
        "columnas": {
            "venta_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "monto": "NUMERIC(10,2)"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {"fecha_id": "INTEGER PRIMARY KEY"}
    }
}

fact_table = identificar_fact_table(schema)
print(fact_table)  # 'fact_ventas'
```

#### `identificar_dimension_tables(schema: dict) -> list[str]`

Identifica todas las tablas de dimensión.

```python
from src.schema_validator import identificar_dimension_tables

dimensions = identificar_dimension_tables(schema)
print(dimensions)  # ['dim_fecha']
```

#### `validar_foreign_keys(fact_table: dict, dimension_tables: list) -> None`

Valida que las FKs de la fact table referencien dimensiones existentes.

```python
from src.schema_validator import validar_foreign_keys

fact_def = {
    "columnas": {
        "venta_id": "BIGSERIAL PRIMARY KEY",
        "fecha_id": "INTEGER REFERENCES dim_fecha",
        "cliente_id": "INTEGER REFERENCES dim_cliente"
    }
}

dims = ["dim_fecha", "dim_cliente"]

validar_foreign_keys(fact_def, dims)  # No lanza error si es válido
```

#### `validar_star_schema(schema: dict) -> dict`

Valida completamente un Star Schema.

```python
from src.schema_validator import validar_star_schema

schema = {
    "fact_ventas": {
        "tipo": "fact",
        "columnas": {
            "venta_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "cliente_id": "INTEGER REFERENCES dim_cliente",
            "monto": "NUMERIC(10,2)"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {
            "fecha_id": "INTEGER PRIMARY KEY",
            "fecha": "DATE",
            "anio": "INTEGER"
        }
    },
    "dim_cliente": {
        "tipo": "dimension",
        "columnas": {
            "cliente_id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(200)"
        }
    }
}

resultado = validar_star_schema(schema)

print(resultado)
# {
#     'valido': True,
#     'fact_table': 'fact_ventas',
#     'dimension_tables': ['dim_fecha', 'dim_cliente'],
#     'errores': []
# }
```

---

### 2. DDL Generator (`ddl_generator.py`)

Funciones para generar DDL (SQL CREATE TABLE statements).

#### `generar_create_dim_table(table_name: str, table_def: dict) -> str`

Genera CREATE TABLE para una dimensión.

```python
from src.ddl_generator import generar_create_dim_table

dim_def = {
    "columnas": {
        "fecha_id": "INTEGER PRIMARY KEY",
        "fecha": "DATE NOT NULL",
        "anio": "INTEGER",
        "mes": "INTEGER"
    }
}

ddl = generar_create_dim_table("dim_fecha", dim_def)
print(ddl)
```

**Salida**:
```sql
CREATE TABLE dim_fecha (
    fecha_id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    anio INTEGER,
    mes INTEGER
);
```

#### `generar_create_fact_table(table_name: str, table_def: dict) -> str`

Genera CREATE TABLE para tabla de hechos (valida que tenga FKs).

```python
from src.ddl_generator import generar_create_fact_table

fact_def = {
    "columnas": {
        "venta_id": "BIGSERIAL PRIMARY KEY",
        "fecha_id": "INTEGER REFERENCES dim_fecha",
        "cliente_id": "INTEGER REFERENCES dim_cliente",
        "cantidad": "INTEGER NOT NULL",
        "monto_venta": "NUMERIC(10,2) NOT NULL"
    }
}

ddl = generar_create_fact_table("fact_ventas", fact_def)
print(ddl)
```

**Salida**:
```sql
CREATE TABLE fact_ventas (
    venta_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER REFERENCES dim_fecha,
    cliente_id INTEGER REFERENCES dim_cliente,
    cantidad INTEGER NOT NULL,
    monto_venta NUMERIC(10,2) NOT NULL
);
```

#### `generar_indices(table_name: str, table_def: dict, es_fact_table: bool) -> list[str]`

Genera índices para optimizar queries.

```python
from src.ddl_generator import generar_indices

fact_def = {
    "columnas": {
        "venta_id": "BIGSERIAL PRIMARY KEY",
        "fecha_id": "INTEGER REFERENCES dim_fecha",
        "cliente_id": "INTEGER REFERENCES dim_cliente"
    }
}

indices = generar_indices("fact_ventas", fact_def, es_fact_table=True)

for idx in indices:
    print(idx)
```

**Salida**:
```sql
CREATE INDEX idx_fact_ventas_fecha ON fact_ventas(fecha_id);
CREATE INDEX idx_fact_ventas_cliente ON fact_ventas(cliente_id);
```

#### `generar_ddl_completo(schema: dict) -> str`

Genera DDL completo (dimensiones + fact table + índices) con orden correcto.

```python
from src.ddl_generator import generar_ddl_completo

schema = {
    "fact_ventas": {
        "tipo": "fact",
        "columnas": {
            "venta_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "cliente_id": "INTEGER REFERENCES dim_cliente",
            "monto": "NUMERIC(10,2)"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {
            "fecha_id": "INTEGER PRIMARY KEY",
            "fecha": "DATE"
        }
    },
    "dim_cliente": {
        "tipo": "dimension",
        "columnas": {
            "cliente_id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(200)"
        }
    }
}

ddl = generar_ddl_completo(schema)
print(ddl)
```

**Salida**:
```sql
-- Dimensiones

CREATE TABLE dim_fecha (
    fecha_id INTEGER PRIMARY KEY,
    fecha DATE
);

CREATE TABLE dim_cliente (
    cliente_id INTEGER PRIMARY KEY,
    nombre VARCHAR(200)
);

-- Tabla de Hechos

CREATE TABLE fact_ventas (
    venta_id BIGSERIAL PRIMARY KEY,
    fecha_id INTEGER REFERENCES dim_fecha,
    cliente_id INTEGER REFERENCES dim_cliente,
    monto NUMERIC(10,2)
);

-- Índices para optimización de queries

CREATE INDEX idx_fact_ventas_fecha ON fact_ventas(fecha_id);
CREATE INDEX idx_fact_ventas_cliente ON fact_ventas(cliente_id);
```

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Validar Star Schema de E-commerce

```python
from src.schema_validator import validar_star_schema

# Definir esquema de ventas online
ecommerce_schema = {
    "fact_pedidos": {
        "tipo": "fact",
        "columnas": {
            "pedido_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "cliente_id": "INTEGER REFERENCES dim_cliente",
            "producto_id": "INTEGER REFERENCES dim_producto",
            "cantidad": "INTEGER NOT NULL CHECK (cantidad > 0)",
            "precio_unitario": "NUMERIC(8,2) NOT NULL",
            "monto_total": "NUMERIC(10,2) NOT NULL",
            "costo_total": "NUMERIC(10,2)",
            "ganancia": "NUMERIC(10,2)"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {
            "fecha_id": "INTEGER PRIMARY KEY",
            "fecha": "DATE NOT NULL",
            "anio": "INTEGER",
            "mes": "INTEGER",
            "trimestre": "INTEGER",
            "dia_semana": "VARCHAR(20)"
        }
    },
    "dim_cliente": {
        "tipo": "dimension",
        "columnas": {
            "cliente_id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(200) NOT NULL",
            "email": "VARCHAR(150)",
            "ciudad": "VARCHAR(100)",
            "pais": "VARCHAR(100)"
        }
    },
    "dim_producto": {
        "tipo": "dimension",
        "columnas": {
            "producto_id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(300) NOT NULL",
            "categoria": "VARCHAR(100)",
            "marca": "VARCHAR(100)",
            "precio_lista": "NUMERIC(8,2)"
        }
    }
}

# Validar esquema
resultado = validar_star_schema(ecommerce_schema)

if resultado["valido"]:
    print("✅ Esquema Star Schema válido")
    print(f"   Fact table: {resultado['fact_table']}")
    print(f"   Dimensiones: {', '.join(resultado['dimension_tables'])}")
else:
    print("❌ Esquema inválido. Errores:")
    for error in resultado["errores"]:
        print(f"   - {error}")
```

**Salida**:
```
✅ Esquema Star Schema válido
   Fact table: fact_pedidos
   Dimensiones: dim_fecha, dim_cliente, dim_producto
```

---

### Ejemplo 2: Generar DDL completo y ejecutar en PostgreSQL

```python
from src.schema_validator import validar_star_schema
from src.ddl_generator import generar_ddl_completo

# Definir esquema
schema = {
    "fact_ventas": {
        "tipo": "fact",
        "columnas": {
            "venta_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "tienda_id": "INTEGER REFERENCES dim_tienda",
            "monto": "NUMERIC(10,2) NOT NULL"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {
            "fecha_id": "INTEGER PRIMARY KEY",
            "fecha": "DATE NOT NULL UNIQUE"
        }
    },
    "dim_tienda": {
        "tipo": "dimension",
        "columnas": {
            "tienda_id": "INTEGER PRIMARY KEY",
            "nombre": "VARCHAR(200) NOT NULL",
            "ciudad": "VARCHAR(100)"
        }
    }
}

# 1. Validar
resultado = validar_star_schema(schema)

if not resultado["valido"]:
    print("Error: Esquema inválido")
    for error in resultado["errores"]:
        print(f"  - {error}")
    exit(1)

# 2. Generar DDL
ddl = generar_ddl_completo(schema)

# 3. Guardar en archivo
with open("data_warehouse.sql", "w") as f:
    f.write(ddl)

print("✅ DDL generado en data_warehouse.sql")

# 4. Opcionalmente, ejecutar en PostgreSQL
# import psycopg2
# conn = psycopg2.connect("postgresql://user:pass@localhost/dwh")
# cur = conn.cursor()
# cur.execute(ddl)
# conn.commit()
# print("✅ Esquema creado en PostgreSQL")
```

---

### Ejemplo 3: Detectar errores en esquemas inválidos

```python
from src.schema_validator import validar_star_schema

# Esquema con problemas
esquema_malo = {
    "fact_ventas": {
        "tipo": "fact",
        "columnas": {
            "venta_id": "BIGSERIAL PRIMARY KEY",
            "fecha_id": "INTEGER REFERENCES dim_fecha",
            "producto_id": "INTEGER REFERENCES dim_producto",  # Dimensión no existe!
            "monto": "NUMERIC"
        }
    },
    "dim_fecha": {
        "tipo": "dimension",
        "columnas": {"fecha_id": "INTEGER PRIMARY KEY"}
    }
    # Falta dim_producto!
}

resultado = validar_star_schema(esquema_malo)

if not resultado["valido"]:
    print("❌ Errores detectados:")
    for i, error in enumerate(resultado["errores"], 1):
        print(f"   {i}. {error}")

# Salida:
# ❌ Errores detectados:
#    1. Star Schema debe tener al menos 2 dimensiones, encontradas: 1
#    2. Clave foránea 'producto_id' referencia tabla 'dim_producto' que no es una dimensión del esquema
```

---

## 🧪 Cobertura de Tests

```
Name                      Stmts   Miss  Cover
---------------------------------------------
src/__init__.py               1      0   100%
src/ddl_generator.py         63      0   100%
src/schema_validator.py      57      2    96%
---------------------------------------------
TOTAL                       121      2    98%
```

**Detalle por módulo**:

| Módulo | Tests | Cobertura | Estado |
|--------|-------|-----------|--------|
| `schema_validator.py` | 14 | 96% | ✅ |
| `ddl_generator.py` | 11 | 100% | ✅ |
| **TOTAL** | **25** | **98%** | ✅ **SUPERADO** |

---

## 🔧 Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **sqlparse**: Parsing de SQL (para futuras extensiones)
- **black**: Formateo automático
- **flake8**: Linting
- **mypy**: Type checking

---

## 📊 Arquitectura

### Diseño Funcional

El proyecto sigue un diseño **funcional puro**:
- **Sin clases** (solo funciones)
- **Funciones pequeñas** (<70 líneas)
- **Sin efectos secundarios**: Funciones predecibles
- **Composabilidad**: Funciones se combinan fácilmente

### Flujo de Validación

```
┌─────────────────────┐
│ Esquema JSON/Dict   │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│ identificar_fact_table()     │
│ identificar_dimension_tables │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────┐
│ validar_foreign_keys()   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ validar_star_schema()    │  ← Función principal
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Resultado: {valido,      │
│            errores,       │
│            fact_table,    │
│            dimensions}    │
└───────────────────────────┘
```

### Flujo de Generación DDL

```
┌─────────────────────┐
│ Esquema validado    │
└──────────┬──────────┘
           │
           ▼
┌───────────────────────────────┐
│ Separar dimensiones y facts   │
└──────────┬────────────────────┘
           │
           ├──────────────────────────┐
           │                          │
           ▼                          ▼
┌──────────────────────┐   ┌──────────────────────┐
│ generar_create_dim   │   │ generar_create_fact  │
└──────────┬───────────┘   └──────────┬───────────┘
           │                          │
           └──────────┬───────────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ generar_indices()    │
           └──────────┬───────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ DDL completo         │
           │ (CREATE TABLEs +     │
           │  CREATE INDEXes)     │
           └──────────────────────┘
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'src'"
**Solución**: Ejecutar desde el directorio del proyecto
```bash
cd modulo-05-bases-datos-avanzadas/tema-3-modelado-datos/04-proyecto-practico
pytest -v
```

### Error: "No se encontró tabla de hechos"
**Solución**: Asegurarse de que al menos una tabla tenga:
- `"tipo": "fact"` en su definición, O
- Nombre que empiece con `"fact_"`

### Error: "Star Schema debe tener al menos 2 dimensiones"
**Solución**: Un Star Schema típico requiere mínimo 2 dimensiones para análisis multidimensional.

---

## 📚 Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Fundamentos de modelado dimensional
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - 4 ejemplos de Star Schema
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - 12 ejercicios de diseño

### Libros Recomendados
- **"The Data Warehouse Toolkit"** - Ralph Kimball ⭐⭐⭐⭐⭐
- **"Database Design for Mere Mortals"** - Michael J. Hernandez

### Herramientas
- [dbdiagram.io](https://dbdiagram.io/) - Diseño visual de esquemas
- [draw.io](https://app.diagrams.net/) - Diagramas ER
- [DBeaver](https://dbeaver.io/) - Cliente SQL universal

---

## 🎯 Próximos Pasos

1. **Extensión**: Agregar soporte para Snowflake Schema
2. **SCD**: Implementar validación de Slowly Changing Dimensions Type 2
3. **ETL**: Crear transformador OLTP → OLAP
4. **Métricas**: Validar que métricas sean aditivas
5. **Visualización**: Generar diagramas ER automáticamente

---

**Proyecto completado** ✅
**Tests**: 25/25 pasando (100%)
**Cobertura**: 98% (supera objetivo ≥80%)
**Calidad**: TDD con funciones puras

**¡Éxito en tu aprendizaje de Modelado de Datos!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Módulo 6: Apache Airflow: Introducción a Airflow](../../../modulo-06-airflow/tema-1-introduccion/01-TEORIA.md)
