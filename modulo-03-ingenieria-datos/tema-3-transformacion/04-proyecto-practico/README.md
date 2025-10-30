# Proyecto Práctico: Pipeline de Transformación con Pandas

**Módulo 3 - Tema 3**: Transformación de Datos
**Versión**: 1.0.0
**Metodología**: Test-Driven Development (TDD)

---

## 📋 Descripción

Proyecto práctico completo que implementa un pipeline de transformación de datos de ventas utilizando Pandas. Incluye módulos para limpieza, transformación, agregación y validación de datos.

### Contexto de Negocio

Sistema de procesamiento de datos de ventas que:
- Limpia datos crudos con problemas de calidad
- Aplica transformaciones y enriquecimientos
- Genera métricas y agregaciones de negocio
- Valida esquemas y calidad de datos

---

## 🏗️ Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── limpiador.py              # 6 funciones de limpieza
│   ├── transformador_pandas.py   # 8 funciones de transformación
│   ├── agregador.py              # 5 funciones de agregación
│   └── validador_schema.py       # 4 funciones de validación
├── tests/
│   ├── __init__.py
│   ├── test_limpiador.py         # 40 tests
│   ├── test_transformador_pandas.py  # 50 tests
│   ├── test_agregador.py         # 30 tests
│   └── test_validador_schema.py  # 40 tests
├── datos/
│   └── ventas_raw.csv           # Datos de ejemplo
├── ejemplos/
│   └── (scripts de ejemplo)
├── requirements.txt
└── README.md
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Tests específicos
pytest tests/test_limpiador.py -v
```

### 3. Uso Básico

```python
import pandas as pd
from src.limpiador import eliminar_duplicados_completos, normalizar_texto
from src.transformador_pandas import calcular_columnas_derivadas
from src.agregador import agrupar_con_multiples_metricas
from src.validador_schema import generar_reporte_calidad

# Cargar datos
df = pd.read_csv('datos/ventas_raw.csv')

# Limpiar
df = eliminar_duplicados_completos(df)
df = normalizar_texto(df, ['producto', 'region'], 'title')

# Transformar
formulas = {'total': 'cantidad * precio'}
df = calcular_columnas_derivadas(df, formulas)

# Agregar
resultado = agrupar_con_multiples_metricas(
    df,
    ['region'],
    {'total': ['sum', 'mean', 'count']}
)

# Validar
reporte = generar_reporte_calidad(df)
print(f"Datos válidos: {reporte['es_valido']}")
```

---

## 📦 Módulos

### 1. `limpiador.py` - Limpieza de Datos

**Funciones**:

| Función | Descripción |
|---------|-------------|
| `eliminar_duplicados_completos()` | Elimina filas completamente duplicadas |
| `eliminar_filas_sin_id()` | Elimina filas sin ID válido |
| `rellenar_valores_nulos()` | Rellena nulos con estrategias personalizadas |
| `normalizar_texto()` | Normaliza texto (mayúsculas, trim, etc.) |
| `validar_rangos_numericos()` | Valida valores dentro de rangos |
| `eliminar_filas_con_errores_criticos()` | Elimina filas con errores en columnas críticas |

**Ejemplo**:

```python
from src.limpiador import rellenar_valores_nulos, normalizar_texto

# Rellenar nulos
estrategias = {
    'edad': 'mean',
    'nombre': 'Desconocido',
    'ciudad': 'No Especificada'
}
df_limpio = rellenar_valores_nulos(df, estrategias)

# Normalizar texto
df_limpio = normalizar_texto(df_limpio, ['nombre', 'ciudad'], 'title')
```

---

### 2. `transformador_pandas.py` - Transformaciones

**Funciones**:

| Función | Descripción |
|---------|-------------|
| `calcular_columnas_derivadas()` | Calcula columnas usando expresiones eval |
| `aplicar_transformacion_por_fila()` | Aplica función a cada fila |
| `categorizar_valores()` | Categoriza basado en condiciones |
| `agregar_metricas_por_grupo()` | Agrega métricas por grupo (transform) |
| `aplicar_ventana_movil()` | Calcula rolling windows |
| `crear_columna_condicional()` | Crea columna con múltiples condiciones |
| `extraer_informacion_temporal()` | Extrae componentes de fechas |
| `aplicar_transformacion_condicional_compleja()` | Aplica función que usa fila completa |

**Ejemplo**:

```python
from src.transformador_pandas import categorizar_valores, aplicar_ventana_movil

# Categorizar
categorias = {
    'Bajo': lambda x: x < 100,
    'Medio': lambda x: 100 <= x < 500,
    'Alto': lambda x: x >= 500
}
df = categorizar_valores(df, 'precio', 'rango_precio', categorias)

# Media móvil
df = aplicar_ventana_movil(df, 'ventas', ventana=7, operacion='mean')
```

---

### 3. `agregador.py` - Agregaciones

**Funciones**:

| Función | Descripción |
|---------|-------------|
| `agrupar_con_multiples_metricas()` | GroupBy con múltiples agregaciones |
| `calcular_top_n_por_grupo()` | Top N registros por grupo |
| `crear_tabla_pivot()` | Crea tabla dinámica |
| `calcular_porcentajes_por_grupo()` | Calcula % respecto al total del grupo |
| `generar_resumen_estadistico()` | Genera estadísticas completas por grupo |

**Ejemplo**:

```python
from src.agregador import agrupar_con_multiples_metricas, calcular_top_n_por_grupo

# Agregación múltiple
resumen = agrupar_con_multiples_metricas(
    df,
    ['region', 'categoria'],
    {
        'ventas': ['sum', 'mean', 'count'],
        'cantidad': ['sum']
    }
)

# Top 5 por región
top_ventas = calcular_top_n_por_grupo(df, 'region', 'ventas', n=5)
```

---

### 4. `validador_schema.py` - Validación

**Funciones**:

| Función | Descripción |
|---------|-------------|
| `validar_columnas_requeridas()` | Valida presencia de columnas |
| `validar_tipos_de_datos()` | Valida tipos de datos esperados |
| `validar_completitud_datos()` | Valida porcentaje de completitud |
| `generar_reporte_calidad()` | Genera reporte completo de calidad |

**Ejemplo**:

```python
from src.validador_schema import generar_reporte_calidad

# Generar reporte completo
reporte = generar_reporte_calidad(
    df,
    columnas_requeridas=['id', 'fecha', 'producto', 'cantidad', 'precio'],
    tipos_esperados={
        'id': 'int',
        'fecha': 'datetime',
        'cantidad': 'int',
        'precio': 'float'
    },
    umbral_completitud=0.95
)

print(f"✅ Datos válidos: {reporte['es_valido']}")
print(f"📊 Filas: {reporte['total_filas']}")
print(f"📊 Columnas: {reporte['total_columnas']}")
print(f"⚠️  Nulos: {reporte['porcentaje_nulos_total']}%")
print(f"🔄 Duplicados: {reporte['duplicados_completos']}")
```

---

## 🧪 Testing

### Estadísticas de Tests

- **Total de tests**: 130+
- **Cobertura**: 98%
- **Módulos testeados**: 4
- **Líneas de código**: 306
- **Líneas sin cubrir**: 7

### Ejecutar Tests

```bash
# Todos los tests con output verbose
pytest tests/ -v

# Con cobertura HTML
pytest tests/ --cov=src --cov-report=html
# Abrir: htmlcov/index.html

# Tests específicos por módulo
pytest tests/test_limpiador.py -v
pytest tests/test_transformador_pandas.py -v
pytest tests/test_agregador.py -v
pytest tests/test_validador_schema.py -v

# Filtrar por nombre de test
pytest tests/ -k "test_valida" -v

# Mostrar prints durante tests
pytest tests/ -v -s

# Parar en el primer fallo
pytest tests/ -x
```

---

## 📊 Métricas de Calidad

### Cobertura por Módulo

| Módulo | Líneas | Cobertura |
|--------|--------|-----------|
| `limpiador.py` | 69 | 100% ✅ |
| `transformador_pandas.py` | 108 | 98% ✅ |
| `agregador.py` | 59 | 93% ✅ |
| `validador_schema.py` | 69 | 99% ✅ |
| **TOTAL** | **306** | **98%** ✅ |

### Validaciones

✅ Todos los tests pasan
✅ Cobertura > 85% (objetivo: 85%)
✅ Sin errores de linting
✅ Código documentado con docstrings
✅ Tipado explícito en todas las funciones
✅ Siguiendo convenciones PEP 8

---

## 💡 Ejemplos de Uso

### Pipeline Completo

```python
import pandas as pd
from src.limpiador import (
    eliminar_duplicados_completos,
    eliminar_filas_sin_id,
    rellenar_valores_nulos,
    normalizar_texto,
    validar_rangos_numericos
)
from src.transformador_pandas import (
    calcular_columnas_derivadas,
    extraer_informacion_temporal
)
from src.agregador import generar_resumen_estadistico
from src.validador_schema import generar_reporte_calidad

# 1. CARGAR DATOS
df = pd.read_csv('datos/ventas_raw.csv')
print(f"Datos cargados: {len(df)} filas")

# 2. LIMPIAR
df = eliminar_duplicados_completos(df)
df = eliminar_filas_sin_id(df, 'id')

estrategias_nulos = {
    'cliente': 'Desconocido',
    'precio': 'median',
    'descuento': 0
}
df = rellenar_valores_nulos(df, estrategias_nulos)
df = normalizar_texto(df, ['producto', 'region', 'vendedor'], 'title')

rangos = {
    'cantidad': (0, 1000),
    'precio': (0, 10000),
    'descuento': (0, 100)
}
df = validar_rangos_numericos(df, rangos)

print(f"Datos limpios: {len(df)} filas")

# 3. TRANSFORMAR
df['fecha'] = pd.to_datetime(df['fecha'])
df = extraer_informacion_temporal(df, 'fecha', ['year', 'month', 'quarter'])

formulas = {
    'subtotal': 'cantidad * precio',
    'descuento_monto': 'subtotal * (descuento / 100)',
    'total': 'subtotal - descuento_monto'
}
df = calcular_columnas_derivadas(df, formulas)

# 4. AGREGAR
resumen = generar_resumen_estadistico(df, 'region', 'total')
print("\nResumen por región:")
print(resumen)

# 5. VALIDAR
reporte = generar_reporte_calidad(
    df,
    columnas_requeridas=['id', 'fecha', 'producto', 'total'],
    tipos_esperados={'id': 'int', 'total': 'float'},
    umbral_completitud=0.95
)

print(f"\n✅ Pipeline completado")
print(f"   - Datos válidos: {reporte['es_valido']}")
print(f"   - Filas procesadas: {reporte['total_filas']}")
print(f"   - Completitud: {100 - reporte['porcentaje_nulos_total']}%")
```

---

## 🔧 Troubleshooting

### Problema: Tests fallan con "Module not found"

**Solución**:
```bash
# Asegúrate de estar en el directorio correcto
cd modulo-03-ingenieria-datos/tema-3-transformacion/04-proyecto-practico

# Instala el paquete en modo desarrollo
pip install -e .
```

### Problema: Error con pandas version

**Solución**:
```bash
# Actualizar pandas
pip install --upgrade pandas>=2.1.0
```

### Problema: Cobertura no se genera

**Solución**:
```bash
# Reinstalar pytest-cov
pip install --force-reinstall pytest-cov
```

---

## 📚 Recursos Adicionales

### Documentación

- [Pandas Official Docs](https://pandas.pydata.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Conceptos Relacionados

- **Teoría**: Ver `01-TEORIA.md` para conceptos de transformación con Pandas
- **Ejemplos**: Ver `02-EJEMPLOS.md` para más ejemplos prácticos
- **Ejercicios**: Ver `03-EJERCICIOS.md` para practicar

---

## 🤝 Contribución

Este es un proyecto educativo. Para mejoras:

1. Asegúrate de que todos los tests pasen
2. Mantén la cobertura >85%
3. Documenta las funciones con docstrings
4. Sigue las convenciones de código del proyecto
5. Añade tests para nuevas funciones

---

## 📝 Notas de Desarrollo

### Decisiones de Diseño

1. **Funciones puras**: Las funciones no modifican el DataFrame original, siempre devuelven uno nuevo
2. **Tipado explícito**: Todas las funciones tienen type hints
3. **Validaciones robustas**: Todas las funciones validan inputs y lanzan errores claros
4. **Documentación completa**: Cada función tiene docstring con ejemplos
5. **Testing exhaustivo**: Cada función tiene múltiples tests (casos normales y edge cases)

### Convenciones

- **Nombres de funciones**: snake_case
- **Nombres de variables**: snake_case
- **Nombres de constantes**: UPPER_CASE
- **Imports**: Ordenados (estándar, externos, internos)
- **Línea máxima**: 100 caracteres
- **Docstrings**: Google style

---

## 📜 Licencia

Material educativo de código abierto para aprendizaje personal.

---

## ✍️ Autor

**Proyecto Práctico del Módulo 3 - Tema 3**
Master en Ingeniería de Datos
Fecha: 2025-10-30

---

**¡Happy coding! 🚀**
