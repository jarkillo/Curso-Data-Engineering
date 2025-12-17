# Proyecto Práctico: Sistema de Extracción Multi-Fuente

**Contexto**: **DataMarket Analytics Inc.** te contrata para construir un sistema robusto de extracción de datos que consolide información de múltiples fuentes para análisis de mercado.

**Nivel**: Intermedio-Avanzado
**Duración estimada**: 4-6 días
**Metodología**: TDD (Test-Driven Development)

---

## 🎯 Objetivos del Proyecto

Construir un sistema profesional de extracción que:

1. **Extraiga** datos de archivos (CSV, JSON, Excel)
2. **Consuma** APIs REST con autenticación y paginación
3. **Scrapee** datos de sitios web de forma ética
4. **Orqueste** múltiples extracciones en paralelo
5. **Valide** la calidad de datos extraídos
6. **Registre** logs completos de todas las operaciones

---

## 📐 Arquitectura del Sistema

```
Sistema de Extracción Multi-Fuente
│
├── extractor_archivos.py       (6 funciones)
│   ├── leer_csv_con_encoding_auto()
│   ├── leer_json_nested()
│   ├── leer_excel_multiple_sheets()
│   ├── detectar_encoding_archivo()
│   ├── validar_estructura_archivo()
│   └── convertir_formato_archivo()
│
├── extractor_apis.py            (5 funciones)
│   ├── hacer_peticion_con_reintentos()
│   ├── manejar_paginacion_completa()
│   ├── autenticar_api()
│   ├── validar_respuesta_api()
│   └── cachear_respuesta()
│
├── extractor_web.py             (4 funciones)
│   ├── verificar_robots_txt()
│   ├── extraer_con_beautifulsoup()
│   ├── manejar_rate_limit()
│   └── validar_html()
│
├── gestor_extracciones.py       (4 funciones)
│   ├── orquestar_extraccion()
│   ├── registrar_log_extraccion()
│   ├── manejar_errores_globales()
│   └── generar_reporte_extraccion()
│
└── validadores.py               (5 funciones)
    ├── validar_datos_csv()
    ├── validar_datos_json()
    ├── validar_datos_api()
    ├── validar_datos_web()
    └── generar_reporte_validacion()
```

**Total**: 24 funciones, 70+ tests unitarios

---

## 🧪 Metodología TDD

### Ciclo Red-Green-Refactor

```
1. RED    → Escribe test que falla
2. GREEN  → Implementa código mínimo para pasar
3. REFACTOR → Mejora el código manteniendo tests verdes
```

### Ejemplo Práctico

```python
# 1. RED - Test que falla
def test_detectar_encoding_utf8():
    """Test que verifica detección de UTF-8"""
    contenido = "nombre,edad\nJosé,28"
    encoding = detectar_encoding_archivo('test.csv')
    assert encoding == 'utf-8'

# 2. GREEN - Implementación mínima
def detectar_encoding_archivo(ruta):
    return 'utf-8'  # Hardcoded, pero test pasa

# 3. REFACTOR - Implementación real
def detectar_encoding_archivo(ruta: str) -> str:
    """Detecta encoding de un archivo"""
    import chardet
    with open(ruta, 'rb') as f:
        resultado = chardet.detect(f.read())
    return resultado['encoding']
```

---

## 📦 Estructura de Archivos

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── extractor_archivos.py      # Módulo 1
│   ├── extractor_apis.py          # Módulo 2
│   ├── extractor_web.py           # Módulo 3
│   ├── gestor_extracciones.py     # Módulo 4
│   └── validadores.py             # Módulo 5
│
├── tests/
│   ├── __init__.py
│   ├── test_extractor_archivos.py    (~15 tests)
│   ├── test_extractor_apis.py        (~15 tests)
│   ├── test_extractor_web.py         (~12 tests)
│   ├── test_gestor_extracciones.py   (~12 tests)
│   ├── test_validadores.py           (~15 tests)
│   └── conftest.py                   (fixtures comunes)
│
├── datos_ejemplo/
│   ├── productos_utf8.csv
│   ├── productos_latin1.csv
│   ├── pedidos_nested.json
│   ├── ventas.xlsx
│   └── catalogo.html
│
├── logs/
│   └── extracciones.log
│
├── README.md
├── requirements.txt
└── pytest.ini
```

---

## 🚀 Guía de Implementación

### Día 1: Módulo 1 - Extractor de Archivos

**Funciones a implementar**:
1. `detectar_encoding_archivo()` - Detecta encoding automáticamente
2. `leer_csv_con_encoding_auto()` - Lee CSV con encoding correcto
3. `leer_json_nested()` - Lee y aplana JSON nested
4. `leer_excel_multiple_sheets()` - Lee todas las hojas de Excel
5. `validar_estructura_archivo()` - Valida columnas esperadas
6. `convertir_formato_archivo()` - Convierte entre CSV/JSON/Excel

**Tests a escribir**: 15 tests (1 happy path + 1-2 edge cases por función)

**Comando**:
```bash
pytest tests/test_extractor_archivos.py -v --cov=src/extractor_archivos
```

---

### Día 2: Módulo 2 - Extractor de APIs

**Funciones a implementar**:
1. `hacer_peticion_con_reintentos()` - Peticiones con backoff exponencial
2. `manejar_paginacion_completa()` - Extrae todos los datos paginados
3. `autenticar_api()` - Maneja diferentes tipos de auth
4. `validar_respuesta_api()` - Valida estructura de respuesta
5. `cachear_respuesta()` - Sistema de caché con TTL

**Tests a escribir**: 15 tests (incluir mocks de requests)

**Comando**:
```bash
pytest tests/test_extractor_apis.py -v --cov=src/extractor_apis
```

---

### Día 3: Módulo 3 - Extractor Web

**Funciones a implementar**:
1. `verificar_robots_txt()` - Verifica si scraping permitido
2. `extraer_con_beautifulsoup()` - Extrae datos de HTML
3. `manejar_rate_limit()` - Implementa delays entre peticiones
4. `validar_html()` - Valida estructura HTML esperada

**Tests a escribir**: 12 tests (usar HTML de prueba)

---

### Día 4: Módulo 4 - Gestor de Extracciones

**Funciones a implementar**:
1. `orquestar_extraccion()` - Orquesta múltiples extracciones
2. `registrar_log_extraccion()` - Logging estructurado
3. `manejar_errores_globales()` - Try/except centralizado
4. `generar_reporte_extraccion()` - Reporte de ejecución

**Tests a escribir**: 12 tests (integración de módulos anteriores)

---

### Día 5: Módulo 5 - Validadores

**Funciones a implementar**:
1. `validar_datos_csv()` - Valida datos extraídos de CSV
2. `validar_datos_json()` - Valida datos JSON
3. `validar_datos_api()` - Valida respuestas de API
4. `validar_datos_web()` - Valida datos scrapeados
5. `generar_reporte_validacion()` - Reporte de calidad

**Tests a escribir**: 15 tests

---

### Día 6: Integration Testing y Refinamiento

- Tests de integración end-to-end
- Refactoring de código duplicado
- Optimización de performance
- Documentación final

---

## 🧰 Configuración del Entorno

### Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### requirements.txt

```txt
# Core
requests>=2.32.4
beautifulsoup4>=4.12.0
pandas>=2.1.0
openpyxl>=3.1.0
chardet>=5.2.0

# Testing
pytest>=8.0.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0

# Development
black>=24.0.0
flake8>=7.0.0
mypy>=1.8.0
```

---

## 🧪 Ejecución de Tests

### Todos los tests
```bash
pytest -v
```

### Con cobertura
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Un módulo específico
```bash
pytest tests/test_extractor_archivos.py -v
```

### Con detalles de fallos
```bash
pytest -vv --tb=short
```

### Solo tests que fallaron
```bash
pytest --lf
```

---

## 📊 Métricas de Calidad

### Objetivos

- ✅ **Cobertura**: >85%
- ✅ **Tests**: 70+ tests pasando
- ✅ **Linting**: 0 errores (flake8)
- ✅ **Formato**: 100% black
- ✅ **Type hints**: Todas las funciones

### Verificación

```bash
# Cobertura
pytest --cov=src --cov-report=term | grep TOTAL

# Linting
flake8 src/ tests/ --max-line-length=100

# Formato
black src/ tests/ --check

# Type checking
mypy src/ --strict
```

---

## 📝 Convenciones de Código

### Nombres

```python
# Funciones: snake_case, verbos
def extraer_datos_csv(ruta: str) -> pd.DataFrame:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_REINTENTOS = 3
TIMEOUT_SEGUNDOS = 30

# Clases: PascalCase (si las usas)
class ExtractorArchivos:
    pass
```

### Docstrings

```python
def leer_csv_con_encoding_auto(ruta: str, **kwargs) -> pd.DataFrame:
    """
    Lee un archivo CSV detectando automáticamente el encoding.

    Args:
        ruta (str): Ruta al archivo CSV
        **kwargs: Argumentos adicionales para pd.read_csv

    Returns:
        pd.DataFrame: Datos del CSV

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no es un CSV válido

    Example:
        >>> df = leer_csv_con_encoding_auto('datos.csv')
        >>> print(len(df))
        100
    """
    pass
```

### Type Hints

```python
from typing import Dict, List, Optional, Union
import pandas as pd

def consolidar_datos(
    csv_path: str,
    api_url: str,
    timeout: int = 30
) -> pd.DataFrame:
    """Consolida datos de múltiples fuentes"""
    pass
```

---

## 🔍 Debugging Tips

### Print Debugging
```python
# ❌ No uses print en producción
print(f"Debug: datos = {datos}")

# ✅ Usa logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Datos extraídos: {len(datos)} registros")
```

### Tests con pytest
```python
# Ejecutar un test específico
pytest tests/test_extractor_archivos.py::test_detectar_encoding_utf8 -v

# Con breakpoint
import pdb; pdb.set_trace()  # En el test
pytest tests/test_extractor_archivos.py -s
```

### Ver variables en tests
```python
def test_ejemplo():
    resultado = funcion_a_probar()
    print(f"\nResultado: {resultado}")  # Se verá con -s
    assert resultado == esperado
```

---

## ✅ Checklist de Completitud

### Por Módulo

**Módulo 1 - Archivos**:
- [ ] 6 funciones implementadas
- [ ] 15+ tests pasando
- [ ] Cobertura >85%
- [ ] 0 errores linting
- [ ] Docstrings completos

**Módulo 2 - APIs**:
- [ ] 5 funciones implementadas
- [ ] 15+ tests pasando
- [ ] Mocks de requests configurados
- [ ] Manejo de errores completo

**Módulo 3 - Web**:
- [ ] 4 funciones implementadas
- [ ] 12+ tests pasando
- [ ] Ética de scraping implementada
- [ ] HTML de prueba creado

**Módulo 4 - Gestor**:
- [ ] 4 funciones implementadas
- [ ] 12+ tests pasando
- [ ] Logging configurado
- [ ] Orquestación funcional

**Módulo 5 - Validadores**:
- [ ] 5 funciones implementadas
- [ ] 15+ tests pasando
- [ ] Validaciones robustas
- [ ] Reportes claros

### Global

- [ ] 70+ tests totales
- [ ] Cobertura >85%
- [ ] 0 errores linting
- [ ] Código formateado (black)
- [ ] Type hints en todas las funciones
- [ ] README completo
- [ ] requirements.txt actualizado
- [ ] Datos de ejemplo incluidos

---

## 🎯 Criterios de Éxito

Has completado exitosamente el proyecto si:

1. ✅ Implementaste las 24 funciones con TDD
2. ✅ 70+ tests pasan (100% de éxito)
3. ✅ Cobertura >85%
4. ✅ 0 errores de linting
5. ✅ Código limpio y documentado
6. ✅ Pipeline completo funciona end-to-end

**Validación final**: Ejecuta el script de ejemplo y genera un reporte consolidado de datos multi-fuente.

---

## 📚 Recursos de Referencia

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Test-Driven Development](https://testdriven.io/test-driven-development/)
- Ejemplos del Tema 2: `../02-EJEMPLOS.md`
- Soluciones de ejercicios: `../03-EJERCICIOS.md`

---

## 💡 Consejos Finales

1. **TDD es lento al principio**: Normal, te ahorrarás horas de debugging después
2. **Tests pequeños**: Un test por comportamiento
3. **Nombres descriptivos**: `test_leer_csv_con_latin1_encoding()` > `test_csv()`
4. **Refactoriza constantemente**: Mantén el código limpio
5. **Commitea frecuentemente**: Cada función que completes

---

**¡Éxito con tu proyecto!** 🚀

Si tienes dudas, consulta los ejemplos y ejercicios del tema. Todo el código que necesitas ya lo viste en acción.

---

**Empresa ficticia**: DataMarket Analytics Inc.
**Proyecto**: Sistema de Extracción Multi-Fuente
**Versión**: 1.0.0
**Última actualización**: 2025-10-30
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Transformación - 01 Teoria](../../tema-3-transformacion/01-TEORIA.md)
