# Proyecto Práctico: Sistema de Análisis de JOINs SQL

## Descripción

Este proyecto implementa un conjunto de funciones para ejecutar, validar y analizar queries SQL con JOINs de forma robusta y segura. Es ideal para pipelines de ETL, reportes automáticos y análisis de datos.

**Empresa ficticia:** TechStore (e-commerce de electrónica)

---

## Objetivos de Aprendizaje

Al completar este proyecto, habrás practicado:

1. **JOINs múltiples**: INNER, LEFT, RIGHT, FULL OUTER JOIN
2. **Subconsultas**: En WHERE, FROM, SELECT
3. **CASE WHEN**: Lógica condicional en SQL
4. **Validación de resultados**: Detección de productos cartesianos, pérdida de datos
5. **Generación de reportes**: Queries complejas para dashboards
6. **TDD**: Desarrollo guiado por tests
7. **Arquitectura funcional**: Sin clases innecesarias

---

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── ejecutor_joins.py       # Ejecuta queries con JOINs
│   ├── detector_tipo_join.py   # Detecta qué JOIN usar
│   ├── validador_joins.py      # Valida resultados de JOINs
│   └── generador_reportes.py   # Genera reportes complejos
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures compartidos
│   ├── test_ejecutor_joins.py
│   ├── test_detector_tipo_join.py
│   ├── test_validador_joins.py
│   └── test_generador_reportes.py
├── README.md                    # Este archivo
├── ARQUITECTURA.md              # Diseño técnico
├── requirements.txt             # Dependencias
└── .gitignore
```

---

## Instalación

### 1. Clonar el repositorio (si aplica)

```bash
cd modulo-02-sql/tema-2-sql-intermedio/04-proyecto-practico/
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Uso

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=src --cov-report=term-missing

# Tests de un módulo específico
pytest tests/test_ejecutor_joins.py -v
```

### Usar las Funciones

```python
from src.ejecutor_joins import ejecutar_join_simple
from src.validador_joins import validar_resultado_join
from src.generador_reportes import generar_reporte_ventas

# Ejemplo 1: Ejecutar un JOIN simple
resultado = ejecutar_join_simple(
    conexion=conn,
    tabla_izq='productos',
    tabla_der='categorias',
    columna_union_izq='categoria_id',
    columna_union_der='id',
    tipo_join='INNER'
)

# Ejemplo 2: Validar resultado
es_valido, mensaje = validar_resultado_join(
    filas_tabla_izq=100,
    filas_tabla_der=10,
    filas_resultado=100,
    tipo_join='INNER'
)

# Ejemplo 3: Generar reporte de ventas
reporte = generar_reporte_ventas(
    conexion=conn,
    fecha_inicio='2025-01-01',
    fecha_fin='2025-12-31'
)
```

---

## Funciones Principales

### Módulo: `ejecutor_joins.py`

| Función                           | Descripción                             | Tipo de Retorno |
| --------------------------------- | --------------------------------------- | --------------- |
| `ejecutar_join_simple()`          | Ejecuta JOIN entre 2 tablas con logging | `list[dict]`    |
| `ejecutar_join_multiple()`        | JOIN de 3+ tablas                       | `list[dict]`    |
| `ejecutar_join_con_subconsulta()` | JOIN con subquery en WHERE/FROM         | `list[dict]`    |

### Módulo: `detector_tipo_join.py`

| Función                          | Descripción                           | Tipo de Retorno    |
| -------------------------------- | ------------------------------------- | ------------------ |
| `detectar_tipo_join_necesario()` | Sugiere JOIN según requerimiento      | `str`              |
| `validar_tipo_join()`            | Valida si el JOIN elegido es correcto | `tuple[bool, str]` |

### Módulo: `validador_joins.py`

| Función                          | Descripción                          | Tipo de Retorno    |
| -------------------------------- | ------------------------------------ | ------------------ |
| `validar_resultado_join()`       | Detecta pérdida/duplicación de datos | `tuple[bool, str]` |
| `contar_filas_join()`            | Verifica integridad                  | `dict[str, int]`   |
| `detectar_producto_cartesiano()` | Alerta si hay demasiadas filas       | `tuple[bool, str]` |

### Módulo: `generador_reportes.py`

| Función                         | Descripción                        | Tipo de Retorno |
| ------------------------------- | ---------------------------------- | --------------- |
| `generar_reporte_ventas()`      | Query compleja con múltiples JOINs | `list[dict]`    |
| `generar_top_clientes()`        | Top N clientes con subconsultas    | `list[dict]`    |
| `generar_analisis_categorias()` | Análisis con CASE WHEN y GROUP BY  | `list[dict]`    |

Ver `ARQUITECTURA.md` para detalles técnicos completos.

---

## Criterios de Calidad

### Tests
- ✅ **40-50 tests** escritos PRIMERO (TDD)
- ✅ **100% tests pasando**
- ✅ **Cobertura >90%**

### Código
- ✅ **Type hints 100%**: Todos los parámetros y retornos tipados
- ✅ **Docstrings completos**: En español, con ejemplos
- ✅ **Funciones <50 líneas**: Código modular y legible
- ✅ **0 errores flake8**: Cumple estándares PEP 8
- ✅ **Formateado con black**: Estilo consistente

### Arquitectura
- ✅ **Funcional**: Sin clases innecesarias
- ✅ **Sin efectos secundarios**: Funciones puras donde sea posible
- ✅ **DRY**: Sin duplicación de lógica
- ✅ **KISS**: Código simple y directo

---

## Metodología TDD

Este proyecto fue desarrollado siguiendo **Test-Driven Development**:

1. ✅ **Red**: Escribir test que falla
2. ✅ **Green**: Escribir código mínimo para que pase
3. ✅ **Refactor**: Mejorar código sin romper tests

**Orden de implementación:**
1. Tests de `ejecutor_joins.py` (~15 tests)
2. Implementación de `ejecutor_joins.py`
3. Tests de `detector_tipo_join.py` (~10 tests)
4. Implementación de `detector_tipo_join.py`
5. Tests de `validador_joins.py` (~12 tests)
6. Implementación de `validador_joins.py`
7. Tests de `generador_reportes.py` (~13 tests)
8. Implementación de `generador_reportes.py`

---

## Herramientas Utilizadas

- **Python 3.10+**: Lenguaje principal
- **SQLite3**: Base de datos embebida
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **black**: Formateador de código
- **flake8**: Linter

---

## Cómo Contribuir

Si encuentras bugs o tienes sugerencias:

1. **Reporta el issue**: Describe el problema con ejemplo
2. **Escribe el test**: Crea test que reproduzca el bug
3. **Fix el código**: Implementa solución
4. **Verifica calidad**: `pytest`, `black`, `flake8`

---

## Contexto Empresarial

Todas las funciones están diseñadas para casos de uso reales en **TechStore**:

- **Análisis de ventas**: Reportes para CFO
- **Segmentación de clientes**: Campañas de marketing
- **Gestión de inventario**: Alertas de stock crítico
- **Auditorías**: Detección de inconsistencias

---

## Próximos Pasos

Después de completar este proyecto:

1. **Tema 3**: Optimización SQL (índices, EXPLAIN, performance)
2. **Proyecto integrador**: Pipeline ETL completo con Airflow
3. **Módulo 3**: Ingeniería de Datos avanzada

---

## Licencia

Este proyecto es parte del **Master en Ingeniería de Datos** y tiene fines educativos.

---

**Última actualización:** 2025-10-25
**Versión:** 1.0.0
**Autor:** Equipo Pedagógico Master Data Engineering
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Optimización SQL - 01 Teoria](../../tema-3-optimizacion/01-TEORIA.md)
