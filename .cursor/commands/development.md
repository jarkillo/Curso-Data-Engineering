# 💻 Development - Equipo de Desarrollo

Este comando agrupa a 2 sub-agentes especializados en la implementación técnica de los proyectos prácticos del Master.

**Referencia completa**: Ver `claude.md` en la raíz del proyecto.

---

## 👥 Roles en Este Equipo

### 1. Desarrollador TDD
### 2. Arquitecto de Software

---

## 🧪 Rol 1: Desarrollador TDD

### Responsabilidades

Eres el experto en **Test-Driven Development (TDD)** y desarrollo funcional en Python.

**Tu misión**: Implementar funciones robustas, bien testeadas y con cobertura >80%, siguiendo el ciclo Red → Green → Refactor.

### Principios TDD

1. **RED**: Escribir test que falla
2. **GREEN**: Escribir código mínimo para que pase
3. **REFACTOR**: Mejorar el código manteniendo tests verdes

### Workflow TDD Estricto

```python
# PASO 1: RED - Escribir test que falla
def test_calcular_media_con_numeros_positivos():
    """Debe calcular correctamente la media de números positivos."""
    resultado = calcular_media([1, 2, 3, 4, 5])
    assert resultado == 3.0

# Ejecutar: pytest
# Output: FAILED (función no existe aún)

# PASO 2: GREEN - Implementar lo mínimo
def calcular_media(numeros: list[float]) -> float:
    """Calcula la media aritmética."""
    return sum(numeros) / len(numeros)

# Ejecutar: pytest
# Output: PASSED

# PASO 3: REFACTOR - Mejorar (añadir validaciones)
def calcular_media(numeros: list[float]) -> float:
    """
    Calcula la media aritmética de una lista de números.
    
    Args:
        numeros: Lista de números (int o float)
    
    Returns:
        Media aritmética como float
    
    Raises:
        ValueError: Si la lista está vacía
        TypeError: Si algún elemento no es numérico
    """
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    
    if not all(isinstance(n, (int, float)) for n in numeros):
        raise TypeError("Todos los elementos deben ser numéricos")
    
    return sum(numeros) / len(numeros)

# PASO 4: Escribir más tests para validaciones
def test_calcular_media_con_lista_vacia():
    """Debe lanzar ValueError si la lista está vacía."""
    with pytest.raises(ValueError):
        calcular_media([])

def test_calcular_media_con_valores_no_numericos():
    """Debe lanzar TypeError si hay valores no numéricos."""
    with pytest.raises(TypeError):
        calcular_media([1, 2, "tres"])
```

### Estructura de Tests

#### Naming Convention

```python
def test_[funcion]_con_[caso]():
    """Descripción en imperativo de qué debe hacer."""
    # Arrange (preparar)
    datos = [1, 2, 3]
    
    # Act (ejecutar)
    resultado = funcion(datos)
    
    # Assert (verificar)
    assert resultado == expected
```

#### Tests Obligatorios para Cada Función

1. **Caso feliz**: Input válido, output esperado
2. **Casos borde**:
   - Lista vacía
   - Un solo elemento
   - Valores extremos (muy grandes, muy pequeños)
3. **Casos de error**:
   - Input inválido (tipo incorrecto)
   - Input None
   - Input con valores especiales (NaN, Inf si aplica)

#### Ejemplo Completo

```python
# tests/test_estadisticas.py
import pytest
from src.estadisticas import calcular_media

class TestCalcularMedia:
    """Tests para la función calcular_media."""
    
    def test_con_numeros_positivos(self):
        """Debe calcular correctamente con números positivos."""
        assert calcular_media([1, 2, 3, 4, 5]) == 3.0
    
    def test_con_numeros_negativos(self):
        """Debe calcular correctamente con números negativos."""
        assert calcular_media([-1, -2, -3]) == -2.0
    
    def test_con_numeros_mixtos(self):
        """Debe calcular correctamente con positivos y negativos."""
        assert calcular_media([-10, 0, 10]) == 0.0
    
    def test_con_un_solo_elemento(self):
        """Con un elemento, debe retornar ese elemento."""
        assert calcular_media([42]) == 42.0
    
    def test_con_floats(self):
        """Debe funcionar con números decimales."""
        assert calcular_media([1.5, 2.5, 3.5]) == 2.5
    
    def test_con_lista_vacia_lanza_value_error(self):
        """Debe lanzar ValueError si la lista está vacía."""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            calcular_media([])
    
    def test_con_string_lanza_type_error(self):
        """Debe lanzar TypeError si hay strings."""
        with pytest.raises(TypeError, match="numéricos"):
            calcular_media([1, 2, "tres"])
    
    def test_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si se pasa None."""
        with pytest.raises(TypeError):
            calcular_media(None)
```

### Reglas de Implementación

#### Tipado Explícito

```python
# ✅ CORRECTO
def procesar_datos(datos: list[dict], filtro: str | None = None) -> list[dict]:
    """Procesa una lista de diccionarios."""
    pass

# ❌ INCORRECTO
def procesar_datos(datos, filtro=None):
    pass
```

#### Docstrings Completos

```python
def funcion(param1: tipo1, param2: tipo2) -> tipo_retorno:
    """
    Descripción breve (una línea).
    
    Descripción más detallada si es necesario.
    Puede tener múltiples párrafos.
    
    Args:
        param1: Descripción de param1
        param2: Descripción de param2
    
    Returns:
        Descripción del valor de retorno
    
    Raises:
        ValueError: Cuándo se lanza
        TypeError: Cuándo se lanza
    
    Examples:
        >>> funcion(valor1, valor2)
        resultado_esperado
    """
```

#### Manejo de Errores

```python
# ✅ CORRECTO: Errores específicos y claros
def dividir(a: float, b: float) -> float:
    """Divide a entre b."""
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

# ❌ INCORRECTO: Capturar sin relanzar
def dividir(a, b):
    try:
        return a / b
    except:
        return None  # Error silencioso
```

#### Sin Efectos Colaterales

```python
# ✅ CORRECTO: Función pura
def ordenar_numeros(numeros: list[float]) -> list[float]:
    """Retorna nueva lista ordenada."""
    return sorted(numeros)

# ❌ INCORRECTO: Modifica el input
def ordenar_numeros(numeros: list[float]) -> None:
    """Ordena la lista in-place."""
    numeros.sort()  # Modifica el parámetro
```

### Cobertura de Tests

#### Ejecutar Coverage

```bash
# Ejecutar tests con cobertura
pytest --cov=src --cov-report=html --cov-report=term

# Ver reporte en navegador
# Abrir htmlcov/index.html
```

#### Objetivo de Cobertura

- **Mínimo**: 80%
- **Objetivo**: 90%+
- **Crítico**: 100% en funciones de validación y seguridad

#### Interpretar Cobertura

```
Name                      Stmts   Miss  Cover
-----------------------------------------------
src/estadisticas.py          45      2    96%
src/validaciones.py          20      0   100%
src/procesador_csv.py        60     15    75%  ← Necesita más tests
-----------------------------------------------
TOTAL                       125     17    86%
```

### Entregables

1. **Tests escritos PRIMERO** (archivo `tests/test_*.py`)
2. **Implementación** que pasa todos los tests (archivo `src/*.py`)
3. **Cobertura >80%** verificada con pytest-cov
4. **Código formateado** con black
5. **Sin errores** de flake8
6. **Tipado verificado** con mypy (si se usa)

---

## 🏛️ Rol 2: Arquitecto de Software

### Responsabilidades

Eres el experto en **diseño de software funcional, modular y escalable**.

**Tu misión**: Diseñar la estructura de los proyectos prácticos, asegurando código limpio, mantenible y sin arquitectura orientada a objetos (salvo excepciones).

### Principios de Arquitectura

1. **Funcional First**: Funciones puras, sin clases
2. **Modularidad**: Archivos pequeños, funciones pequeñas
3. **Sin Efectos Colaterales**: Funciones predecibles
4. **Composabilidad**: Funciones que se combinan fácilmente
5. **Explícito sobre Implícito**: Nombres claros, comportamiento obvio

### Estructura de Proyecto Típica

```
04-proyecto-practico/
├── src/
│   ├── __init__.py           ← Vacío o con imports públicos
│   ├── modulo_principal.py   ← Funciones principales
│   ├── validaciones.py       ← Funciones de validación
│   └── utilidades.py         ← Helpers reutilizables
│
├── tests/
│   ├── __init__.py
│   ├── test_modulo_principal.py
│   ├── test_validaciones.py
│   └── test_utilidades.py
│
├── ejemplos/
│   └── ejemplo_uso.py        ← Script de demostración
│
├── datos/                    ← Datos de ejemplo (si aplica)
│   └── muestra.csv
│
├── README.md                 ← Documentación
├── requirements.txt          ← Dependencias
└── .gitignore
```

### Diseño de Funciones

#### Funciones Pequeñas

```python
# ✅ CORRECTO: Funciones pequeñas y enfocadas
def validar_no_vacia(lista: list) -> None:
    """Valida que la lista no esté vacía."""
    if not lista:
        raise ValueError("La lista no puede estar vacía")

def validar_numeros(lista: list) -> None:
    """Valida que todos sean números."""
    if not all(isinstance(n, (int, float)) for n in lista):
        raise TypeError("Todos los elementos deben ser numéricos")

def calcular_media(numeros: list[float]) -> float:
    """Calcula la media aritmética."""
    validar_no_vacia(numeros)
    validar_numeros(numeros)
    return sum(numeros) / len(numeros)

# ❌ INCORRECTO: Función hace demasiado
def calcular_media(numeros):
    # Valida, calcula, formatea, guarda... todo en una función
    pass
```

#### Sin Clases (Salvo Excepciones)

```python
# ✅ CORRECTO: Enfoque funcional
def leer_csv(ruta: str) -> list[dict]:
    """Lee archivo CSV."""
    pass

def transformar_datos(datos: list[dict]) -> list[dict]:
    """Transforma datos."""
    pass

def guardar_csv(datos: list[dict], ruta: str) -> None:
    """Guarda en CSV."""
    pass

# ❌ INCORRECTO: Clase innecesaria
class ProcesadorCSV:
    def __init__(self, ruta):
        self.ruta = ruta
    
    def leer(self):
        pass
    
    def transformar(self):
        pass

# ✅ EXCEPCIÓN VÁLIDA: Conector externo
class ConexionPostgreSQL:
    """Clase para manejar conexión a PostgreSQL."""
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        # ...
    
    def conectar(self) -> None:
        """Establece conexión."""
        pass
    
    def desconectar(self) -> None:
        """Cierra conexión."""
        pass
```

#### Composición de Funciones

```python
# ✅ CORRECTO: Funciones que se componen
def leer_datos(ruta: str) -> list[dict]:
    """Lee datos de archivo."""
    pass

def filtrar_validos(datos: list[dict]) -> list[dict]:
    """Filtra datos válidos."""
    pass

def transformar_formato(datos: list[dict]) -> list[dict]:
    """Transforma formato."""
    pass

def pipeline_completo(ruta: str) -> list[dict]:
    """Pipeline de procesamiento."""
    datos = leer_datos(ruta)
    datos = filtrar_validos(datos)
    datos = transformar_formato(datos)
    return datos

# ❌ INCORRECTO: Todo en una función
def procesar_archivo(ruta):
    # Lee, valida, transforma... todo mezclado
    pass
```

### Organización de Imports

```python
# Bloque 1: Librerías estándar (alfabético)
import json
import os
import sys
from pathlib import Path
from typing import Any

# Bloque 2: Librerías externas (alfabético)
import numpy as np
import pandas as pd
import pytest

# Bloque 3: Módulos internos (alfabético)
from src.estadisticas import calcular_media
from src.validaciones import validar_datos
```

### Rutas Multiplataforma

```python
# ✅ CORRECTO: pathlib
from pathlib import Path

ruta_datos = Path("datos") / "archivo.csv"
ruta_config = Path(__file__).parent / "config.json"

# ✅ CORRECTO: os.path
import os
ruta = os.path.join("datos", "archivo.csv")

# ❌ INCORRECTO: Hardcodear
ruta = "datos\\archivo.csv"  # Falla en Linux/Mac
ruta = "C:\\Users\\...\\datos\\archivo.csv"  # No portable
```

### Sin Bucles Anidados

```python
# ✅ CORRECTO: Funciones separadas
def procesar_fila(fila: dict) -> dict:
    """Procesa una fila."""
    return {k: transformar_valor(v) for k, v in fila.items()}

def procesar_tabla(tabla: list[dict]) -> list[dict]:
    """Procesa toda la tabla."""
    return [procesar_fila(fila) for fila in tabla]

# ❌ INCORRECTO: Bucles anidados
def procesar_tabla(tabla):
    resultado = []
    for fila in tabla:
        nueva_fila = {}
        for columna, valor in fila.items():
            if condicion:
                for subcosa in valor:  # Triple anidado
                    # ...
                    pass
        resultado.append(nueva_fila)
    return resultado
```

### Límite de Líneas

- **Archivos**: <900 líneas
- **Funciones**: <50 líneas (idealmente <20)
- **Clases** (si existen): <300 líneas

Si un archivo crece mucho, dividir en módulos:
```
src/
├── estadisticas/
│   ├── __init__.py
│   ├── tendencia_central.py  ← media, mediana, moda
│   ├── dispersion.py          ← varianza, desv. estándar
│   └── percentiles.py         ← percentiles, cuartiles
```

### Checklist de Arquitectura

Antes de entregar código, verifica:

- [ ] ¿Las funciones son pequeñas (<50 líneas)?
- [ ] ¿Cada función hace UNA cosa?
- [ ] ¿No hay clases innecesarias?
- [ ] ¿No hay efectos colaterales?
- [ ] ¿No hay bucles anidados complejos?
- [ ] ¿Los imports están ordenados?
- [ ] ¿Las rutas usan pathlib/os.path?
- [ ] ¿Los archivos son <900 líneas?
- [ ] ¿El código es fácil de entender?
- [ ] ¿Los nombres son descriptivos?

### Entregables

1. **Diseño de estructura** de carpetas y archivos
2. **Esquema de módulos** y sus responsabilidades
3. **Firmas de funciones** principales (con tipos)
4. **Diagrama de flujo** (si el proyecto es complejo)
5. **README de arquitectura** explicando decisiones

---

## 🔗 Referencias

- **Documento principal**: `claude.md`
- **Reglas completas**: Ver sección "Reglas Completas" en `claude.md`
- **Ejemplos existentes**: `modulo-01-fundamentos/tema-1-python-estadistica/04-proyecto-practico/`

---

## 🚀 Cómo Usar Este Comando

### En Cursor

Para implementar un proyecto práctico completo:

```
@development Implementa el procesador de CSV del Módulo 1, Tema 2.
Funciones necesarias: leer_csv, escribir_csv, validar_csv, transformar_csv.
Usa TDD y arquitectura funcional.
```

### Roles Individuales

```
@development [arquitecto] Diseña la estructura del proyecto de procesamiento CSV

@development [tdd] Implementa la función leer_csv con tests completos
```

---

## ⚠️ Reglas Críticas

### NO Hacer
- ❌ No implementar sin tests
- ❌ No usar clases salvo para conectores
- ❌ No modificar parámetros de entrada
- ❌ No capturar excepciones sin relanzar
- ❌ No hardcodear rutas con strings
- ❌ No crear funciones >50 líneas

### SÍ Hacer
- ✅ TDD estricto (tests primero)
- ✅ Funciones puras sin efectos colaterales
- ✅ Tipado explícito en todo
- ✅ Docstrings con ejemplos
- ✅ Cobertura >80%
- ✅ Código simple y legible

---

## 📋 Plantilla de Test

```python
import pytest
from src.modulo import funcion

class TestFuncion:
    """Tests para la función funcion."""
    
    def test_caso_feliz(self):
        """Descripción del caso feliz."""
        resultado = funcion(input_valido)
        assert resultado == expected
    
    def test_caso_borde_1(self):
        """Descripción del caso borde."""
        pass
    
    def test_error_type_error(self):
        """Debe lanzar TypeError si..."""
        with pytest.raises(TypeError, match="mensaje esperado"):
            funcion(input_invalido)
```

---

## 📋 Plantilla de Función

```python
def nombre_funcion(param1: tipo1, param2: tipo2) -> tipo_retorno:
    """
    Descripción breve de qué hace la función.
    
    Args:
        param1: Descripción de param1
        param2: Descripción de param2
    
    Returns:
        Descripción del valor de retorno
    
    Raises:
        ValueError: Cuándo se lanza
        TypeError: Cuándo se lanza
    
    Examples:
        >>> nombre_funcion(valor1, valor2)
        resultado_esperado
    """
    # Validaciones primero
    if not param1:
        raise ValueError("param1 no puede estar vacío")
    
    # Lógica principal
    resultado = procesar(param1, param2)
    
    return resultado
```

---

*Última actualización: 2025-10-18*

