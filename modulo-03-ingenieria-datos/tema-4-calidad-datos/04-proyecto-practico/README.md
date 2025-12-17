# Proyecto Práctico: Framework de Calidad de Datos

**Módulo 3 - Tema 4**: Calidad de Datos
**Versión**: 1.0.0
**Metodología**: Test-Driven Development (TDD)

---

## 📋 Descripción

Framework completo para asegurar la calidad de datos en pipelines ETL. Incluye validación de esquemas, detección de duplicados (exactos y fuzzy), identificación de outliers y data profiling completo.

### Contexto de Negocio

Sistema de calidad de datos reutilizable que:
- Valida esquemas de datos con reglas personalizadas
- Detecta y elimina duplicados exactos y similares
- Identifica y trata outliers con múltiples métodos
- Genera perfiles de calidad automáticos
- Produce reportes ejecutivos de calidad

---

## 🏗️ Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── validador_esquema.py         # 7 funciones de validación
│   ├── detector_duplicados.py       # 5 funciones de detección
│   ├── detector_outliers.py         # 6 funciones de outliers
│   └── profiler.py                  # 4 funciones de profiling
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Fixtures compartidas
│   ├── test_validador_esquema.py    # 15 tests
│   ├── test_detector_duplicados.py  # 12 tests
│   ├── test_detector_outliers.py    # 18 tests
│   └── test_profiler.py             # 12 tests
├── datos/
│   └── transacciones_raw.csv        # Datos de ejemplo
├── ejemplos/
│   └── ejemplo_pipeline_completo.py # Ejemplo de uso
├── requirements.txt
├── pytest.ini
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
pytest tests/test_validador_esquema.py -v

# Ver cobertura en HTML
# Abrir: htmlcov/index.html
```

### 3. Uso Básico

```python
import pandas as pd
from src.validador_esquema import validar_tipos_columnas, validar_rangos_numericos
from src.detector_duplicados import detectar_duplicados_exactos, detectar_duplicados_fuzzy
from src.detector_outliers import detectar_outliers_iqr, tratar_outliers
from src.profiler import generar_perfil_basico, generar_reporte_calidad

# Cargar datos
df = pd.read_csv('datos/transacciones_raw.csv')

# Validar esquema
esquema = {'monto': 'float', 'fecha': 'str', 'cliente_id': 'int'}
es_valido, errores = validar_tipos_columnas(df, esquema)

# Detectar duplicados
duplicados = detectar_duplicados_exactos(df, ['cliente_id', 'fecha'])

# Detectar outliers
outliers = detectar_outliers_iqr(df, 'monto')

# Generar reporte
reporte = generar_reporte_calidad(df)
print(reporte)
```

---

## 📚 Módulos

### 1. validador_esquema.py

Validación de esquemas y reglas de negocio.

**Funciones**:

```python
def validar_tipos_columnas(df: pd.DataFrame, esquema: Dict[str, str]) -> Tuple[bool, List[str]]
```
Valida que columnas tengan los tipos esperados.

```python
def validar_rangos_numericos(df: pd.DataFrame, rangos: Dict[str, Tuple[float, float]]) -> Dict
```
Valida que valores numéricos estén en rangos válidos.

```python
def validar_valores_unicos(df: pd.DataFrame, columnas: List[str]) -> Tuple[bool, Dict]
```
Verifica que columnas especificadas no tengan duplicados.

```python
def validar_valores_permitidos(df: pd.DataFrame, reglas: Dict[str, List]) -> Dict
```
Valida que valores estén en listas permitidas (enums).

```python
def validar_nulls_permitidos(df: pd.DataFrame, columnas_requeridas: List[str]) -> Dict
```
Verifica que columnas requeridas no tengan valores nulos.

```python
def validar_esquema_completo(df: pd.DataFrame, configuracion: Dict) -> Tuple[bool, Dict]
```
Ejecuta todas las validaciones de forma integrada.

```python
def generar_reporte_validacion(resultados_validacion: Dict) -> str
```
Genera reporte legible de resultados de validación.

### 2. detector_duplicados.py

Detección y manejo de duplicados exactos y fuzzy.

**Funciones**:

```python
def detectar_duplicados_exactos(df: pd.DataFrame, columnas: List[str]) -> pd.Series
```
Identifica duplicados exactos en columnas especificadas.

```python
def detectar_duplicados_fuzzy(df: pd.DataFrame, columna: str, umbral: int = 85) -> pd.DataFrame
```
Encuentra valores similares usando fuzzy matching.

```python
def eliminar_duplicados_con_estrategia(df: pd.DataFrame, columnas: List[str], estrategia: str = 'primero') -> pd.DataFrame
```
Elimina duplicados según estrategia (primero/ultimo/mas_completo).

```python
def marcar_duplicados_probables(df: pd.DataFrame, columnas: List[str]) -> pd.DataFrame
```
Añade columna booleana marcando duplicados.

```python
def generar_reporte_duplicados(df: pd.DataFrame, columnas: List[str]) -> Dict
```
Genera estadísticas detalladas de duplicados.

### 3. detector_outliers.py

Identificación y tratamiento de valores atípicos.

**Funciones**:

```python
def detectar_outliers_iqr(df: pd.DataFrame, columna: str) -> Tuple[pd.Series, Dict]
```
Detecta outliers usando método IQR.

```python
def detectar_outliers_zscore(df: pd.DataFrame, columna: str, umbral: float = 3.0) -> Tuple[pd.Series, Dict]
```
Detecta outliers usando Z-score.

```python
def detectar_outliers_isolation_forest(df: pd.DataFrame, columnas: List[str], contamination: float = 0.1) -> pd.Series
```
Detecta outliers multivariados con Isolation Forest.

```python
def tratar_outliers(df: pd.DataFrame, columna: str, outliers: pd.Series, metodo: str = 'eliminar') -> pd.DataFrame
```
Aplica tratamiento a outliers (eliminar/imputar/capping).

```python
def visualizar_outliers(df: pd.DataFrame, columna: str, archivo_salida: str) -> None
```
Genera gráficos de análisis de outliers.

```python
def generar_reporte_outliers(df: pd.DataFrame, columnas_numericas: List[str]) -> Dict
```
Estadísticas de outliers por columna.

### 4. profiler.py

Análisis y profiling de calidad de datos.

**Funciones**:

```python
def generar_perfil_basico(df: pd.DataFrame) -> Dict
```
Estadísticas descriptivas básicas por columna.

```python
def generar_perfil_completo(df: pd.DataFrame, archivo_salida: str = None) -> Dict
```
Análisis completo de calidad con ydata-profiling opcional.

```python
def detectar_correlaciones(df: pd.DataFrame, umbral: float = 0.7) -> pd.DataFrame
```
Identifica variables altamente correlacionadas.

```python
def generar_reporte_calidad(df: pd.DataFrame) -> Dict
```
Dashboard completo con todas las métricas de calidad.

---

## 🧪 Testing

### Cobertura de Tests

- **validador_esquema.py**: 15 tests (~95% cobertura)
- **detector_duplicados.py**: 12 tests (~92% cobertura)
- **detector_outliers.py**: 18 tests (~90% cobertura)
- **profiler.py**: 12 tests (~88% cobertura)

**Total**: 57 tests, >90% cobertura global

### Convenciones de Tests

- Nombres de funciones: `test_<funcion>_<caso>`
- Fixtures compartidas en `conftest.py`
- Datos de prueba generados programáticamente
- Tests parametrizados para casos múltiples
- Verificación de excepciones con `pytest.raises`

### Ejemplos de Tests

```python
def test_validar_tipos_columnas_tipos_validos():
    """Verifica validación correcta con tipos válidos."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'nombre': ['A', 'B', 'C'],
        'precio': [10.5, 20.3, 15.7]
    })

    esquema = {'id': 'int', 'nombre': 'str', 'precio': 'float'}
    es_valido, errores = validar_tipos_columnas(df, esquema)

    assert es_valido is True
    assert len(errores) == 0


def test_detectar_outliers_iqr_con_outliers():
    """Verifica detección correcta de outliers con IQR."""
    df = pd.DataFrame({'valores': [1, 2, 3, 4, 5, 100]})

    outliers, stats = detectar_outliers_iqr(df, 'valores')

    assert outliers.sum() == 1
    assert outliers.iloc[-1] is True
```

---

## 📊 Datos de Ejemplo

### transacciones_raw.csv

Dataset con problemas de calidad conocidos para testing:

- **Registros**: 1000 transacciones
- **Problemas incluidos**:
  - 50 registros duplicados exactos
  - 20 registros con valores similares (fuzzy)
  - 30 outliers en montos
  - 15% de valores nulos
  - 10 registros con fechas futuras (inválidas)
  - 5 registros con tipos incorrectos

**Columnas**:
- `transaccion_id`: ID único (int)
- `cliente_id`: ID del cliente (int)
- `fecha`: Fecha de transacción (str YYYY-MM-DD)
- `monto`: Monto en euros (float)
- `categoria`: Categoría de transacción (str)
- `estado`: Estado del pago (str)

---

## 🔧 Configuración

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=85
```

### requirements.txt

```
pandas>=2.0.0
numpy>=1.24.0
pandera>=0.18.0
rapidfuzz>=3.0.0
ydata-profiling>=4.5.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

---

## 🎯 Casos de Uso

### Caso 1: Validación Rápida

```python
from src.validador_esquema import validar_esquema_completo

config = {
    'tipos': {'id': 'int', 'precio': 'float'},
    'rangos': {'precio': (0, 1000)},
    'columnas_requeridas': ['id', 'nombre'],
    'valores_permitidos': {'categoria': ['A', 'B', 'C']}
}

es_valido, reporte = validar_esquema_completo(df, config)
```

### Caso 2: Limpieza de Duplicados

```python
from src.detector_duplicados import eliminar_duplicados_con_estrategia

# Mantener el registro más completo
df_limpio = eliminar_duplicados_con_estrategia(
    df,
    columnas=['email'],
    estrategia='mas_completo'
)
```

### Caso 3: Pipeline Completo

```python
# 1. Validar
es_valido, errores = validar_esquema_completo(df, config)
if not es_valido:
    raise ValueError(f"Datos inválidos: {errores}")

# 2. Duplicados
df = eliminar_duplicados_con_estrategia(df, ['id'])

# 3. Outliers
for col in ['monto', 'cantidad']:
    outliers, _ = detectar_outliers_iqr(df, col)
    df = tratar_outliers(df, col, outliers, metodo='capping')

# 4. Reporte
reporte = generar_reporte_calidad(df)
print(reporte)
```

---

## 📈 Métricas de Calidad

El framework genera las siguientes métricas:

### Completitud
- Porcentaje de valores no nulos por columna
- Registros completamente llenos vs incompletos

### Unicidad
- Porcentaje de duplicados
- Grupos de registros duplicados
- Similitud fuzzy entre registros

### Validez
- Cumplimiento de tipos de datos
- Valores dentro de rangos válidos
- Conformidad con reglas de negocio

### Consistencia
- Outliers estadísticos
- Valores anómalos multivariados
- Correlaciones inesperadas

---

## 🚨 Manejo de Errores

Todas las funciones siguen estas convenciones:

- **Validación de inputs**: Verificar que DataFrame no esté vacío
- **Excepciones específicas**: `ValueError`, `TypeError`, `KeyError`
- **Mensajes claros**: Indicar exactamente qué falló y por qué
- **Sin fallos silenciosos**: Siempre lanzar excepción en errores

```python
def ejemplo_funcion(df: pd.DataFrame, columna: str) -> pd.Series:
    """Ejemplo con validaciones."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe en DataFrame")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"Columna '{columna}' debe ser numérica")

    # Lógica de la función...
```

---

## 🔐 Consideraciones de Seguridad

- **Validación de inputs**: Nunca confiar en datos externos
- **Sanitización**: Limpiar caracteres especiales en columnas de texto
- **Límites de tamaño**: Verificar que DataFrames no excedan memoria disponible
- **Logging**: Registrar todas las operaciones de calidad
- **Trazabilidad**: Mantener histórico de transformaciones

---

## 🎓 Mejores Prácticas

1. **Validar temprano**: Fallar rápido si datos son inválidos
2. **Documentar reglas**: Externalizar reglas de calidad en configuración
3. **Reportar claramente**: Generar reportes comprensibles para negocio
4. **Testear exhaustivamente**: Cobertura > 85%
5. **Versionar esquemas**: Mantener historial de cambios en validaciones

---

## 📝 Licencia

Este proyecto es parte del Master en Ingeniería de Datos.
Uso educativo exclusivamente.

---

## 👥 Contribuciones

Para contribuir:

1. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
2. Escribir tests primero (TDD)
3. Implementar funcionalidad
4. Asegurar cobertura > 85%
5. Actualizar documentación
6. Crear Pull Request

---

## 📞 Soporte

Para preguntas o problemas:
- Revisar ejemplos en `ejemplos/`
- Consultar tests en `tests/`
- Ver documentación en archivos fuente

---

*Última actualización: 2025-10-30*
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Formatos Modernos - 01 Teoria](../../tema-5-formatos-modernos/01-TEORIA.md)
