# Procesador CSV - Proyecto Práctico

Proyecto práctico del **Tema 2: Procesamiento de Archivos CSV** del Master en Data Engineering.

Este proyecto implementa un procesador CSV robusto siguiendo **TDD estricto**, **arquitectura funcional** y **buenas prácticas de Data Engineering**.

---

## 📋 Contenido

- [Características](#características)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Documentación de Funciones](#documentación-de-funciones)
- [Ejemplos](#ejemplos)
- [Tests](#tests)
- [Arquitectura](#arquitectura)
- [Buenas Prácticas Implementadas](#buenas-prácticas-implementadas)

---

## ✨ Características

- ✅ **Lectura robusta de CSV** con validación de archivos
- ✅ **Detección automática de delimitadores** (`,`, `;`, `\t`)
- ✅ **Validación de datos** según tipos y reglas de negocio
- ✅ **Transformación de datos** (filtrado, columnas calculadas)
- ✅ **Consolidación de múltiples CSV** en uno solo
- ✅ **Soporte para múltiples encodings** (UTF-8, Latin-1, etc.)
- ✅ **Manejo robusto de errores** con mensajes claros
- ✅ **Cobertura de tests del 99%**
- ✅ **Funciones puras** sin efectos colaterales
- ✅ **Tipado explícito** en todas las funciones

---

## 🚀 Instalación

### Requisitos

- Python 3.8+
- pip

### Pasos

```bash
# 1. Clonar el repositorio (o navegar al directorio)
cd modulo-01-fundamentos/tema-2-procesamiento-csv/04-proyecto-practico

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## ⚡ Uso Rápido

### Ejemplo Básico

```python
from src.lector_csv import leer_csv
from src.escritor_csv import escribir_csv

# Leer CSV
datos = leer_csv("datos.csv")

# Procesar datos
datos_procesados = [fila for fila in datos if int(fila["edad"]) > 25]

# Escribir resultado
escribir_csv(datos_procesados, "resultado.csv")
```

### Ejemplo con Validación

```python
from src.lector_csv import leer_csv
from src.validador_csv import validar_fila

# Leer datos
datos = leer_csv("datos.csv")

# Validar cada fila
validaciones = {
    "nombre": str,
    "edad": int,
    "ciudad": str
}

for fila in datos:
    errores = validar_fila(fila, validaciones)
    if errores:
        print(f"Errores: {errores}")
```

---

## 📚 Documentación de Funciones

### Módulo: `lector_csv`

#### `leer_csv(ruta_archivo, delimitador=",", encoding="utf-8")`

Lee un archivo CSV y retorna una lista de diccionarios.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV
- `delimitador` (str): Delimitador usado (por defecto: `,`)
- `encoding` (str): Codificación del archivo (por defecto: `utf-8`)

**Retorna:**
- `List[Dict[str, str]]`: Lista de diccionarios con los datos

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si el archivo está vacío

**Ejemplo:**
```python
datos = leer_csv("ventas.csv")
# [{'producto': 'Laptop', 'precio': '899.99'}, ...]
```

---

#### `detectar_delimitador(ruta_archivo)`

Detecta automáticamente el delimitador usado en un archivo CSV.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV

**Retorna:**
- `str`: Delimitador detectado (`,`, `;`, `\t`, etc.)

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe

**Ejemplo:**
```python
delimitador = detectar_delimitador("datos.csv")
# ','
```

---

#### `validar_archivo_existe(ruta_archivo)`

Valida que un archivo existe y no está vacío.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si el archivo está vacío

**Ejemplo:**
```python
validar_archivo_existe("datos.csv")
# No lanza error si el archivo es válido
```

---

### Módulo: `escritor_csv`

#### `escribir_csv(datos, ruta_archivo, headers=None, delimitador=",", encoding="utf-8")`

Escribe una lista de diccionarios en un archivo CSV.

**Parámetros:**
- `datos` (List[Dict[str, str]]): Lista de diccionarios con los datos
- `ruta_archivo` (str): Ruta donde guardar el archivo
- `headers` (List[str], opcional): Lista de headers (se infiere si no se proporciona)
- `delimitador` (str): Delimitador a usar (por defecto: `,`)
- `encoding` (str): Codificación del archivo (por defecto: `utf-8`)

**Lanza:**
- `ValueError`: Si datos está vacío y no se proporcionan headers

**Ejemplo:**
```python
datos = [{"nombre": "Ana", "edad": "25"}]
escribir_csv(datos, "salida.csv")
```

---

### Módulo: `validador_csv`

#### `validar_headers(ruta_archivo, headers_esperados, delimitador=",")`

Valida que un archivo CSV tiene los headers esperados.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV
- `headers_esperados` (List[str]): Lista de headers que debe tener el archivo
- `delimitador` (str): Delimitador usado (por defecto: `,`)

**Retorna:**
- `bool`: True si los headers coinciden, False si no

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe

**Ejemplo:**
```python
valido = validar_headers("datos.csv", ["nombre", "edad", "ciudad"])
# True o False
```

---

#### `validar_tipo_dato(valor, tipo_esperado)`

Valida que un valor puede ser convertido al tipo esperado.

**Parámetros:**
- `valor` (str): Valor a validar
- `tipo_esperado` (Type): Tipo de dato esperado (int, float, str)

**Retorna:**
- `bool`: True si el valor puede ser convertido, False si no

**Ejemplo:**
```python
validar_tipo_dato("25", int)  # True
validar_tipo_dato("abc", int)  # False
```

---

#### `validar_fila(fila, validaciones)`

Valida una fila del CSV según reglas de validación.

**Parámetros:**
- `fila` (Dict[str, str]): Diccionario con los datos de la fila
- `validaciones` (Dict[str, Type]): Diccionario {columna: tipo_esperado}

**Retorna:**
- `List[str]`: Lista de errores encontrados (vacía si todo está bien)

**Ejemplo:**
```python
fila = {"nombre": "Ana", "edad": "25"}
validaciones = {"nombre": str, "edad": int}
errores = validar_fila(fila, validaciones)
# [] (sin errores)
```

---

### Módulo: `transformador_csv`

#### `filtrar_filas(datos, condicion)`

Filtra filas de datos según una condición.

**Parámetros:**
- `datos` (List[Dict[str, str]]): Lista de diccionarios con los datos
- `condicion` (Callable): Función que retorna True si la fila debe incluirse

**Retorna:**
- `List[Dict[str, str]]`: Nueva lista con solo las filas que cumplen la condición

**Ejemplo:**
```python
datos = [{"nombre": "Ana", "edad": "25"}, {"nombre": "Luis", "edad": "30"}]
mayores_25 = filtrar_filas(datos, lambda fila: int(fila["edad"]) > 25)
# [{"nombre": "Luis", "edad": "30"}]
```

---

#### `agregar_columna(datos, nombre_columna, funcion_calculo)`

Agrega una nueva columna calculada a los datos.

**Parámetros:**
- `datos` (List[Dict[str, str]]): Lista de diccionarios con los datos
- `nombre_columna` (str): Nombre de la nueva columna
- `funcion_calculo` (Callable): Función que calcula el valor de la nueva columna

**Retorna:**
- `List[Dict[str, str]]`: Nueva lista con la columna adicional

**Ejemplo:**
```python
datos = [{"precio": "10", "cantidad": "2"}]
resultado = agregar_columna(
    datos,
    "total",
    lambda f: str(float(f["precio"]) * int(f["cantidad"]))
)
# [{"precio": "10", "cantidad": "2", "total": "20.0"}]
```

---

#### `consolidar_csvs(archivos, archivo_salida, delimitador=",", encoding="utf-8")`

Consolida múltiples archivos CSV en uno solo.

**Parámetros:**
- `archivos` (List[str]): Lista de rutas a los archivos CSV
- `archivo_salida` (str): Ruta donde guardar el archivo consolidado
- `delimitador` (str): Delimitador usado (por defecto: `,`)
- `encoding` (str): Codificación de los archivos (por defecto: `utf-8`)

**Lanza:**
- `ValueError`: Si la lista está vacía o si los headers no coinciden
- `FileNotFoundError`: Si algún archivo no existe

**Ejemplo:**
```python
consolidar_csvs(["ventas_a.csv", "ventas_b.csv"], "consolidado.csv")
```

---

### Módulo: `utilidades`

#### `contar_filas(ruta_archivo)`

Cuenta el número de filas de datos en un archivo CSV (sin contar el header).

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV

**Retorna:**
- `int`: Número de filas de datos

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si el archivo está vacío

**Ejemplo:**
```python
num_filas = contar_filas("datos.csv")
# 10
```

---

#### `obtener_headers(ruta_archivo, delimitador=",")`

Obtiene la lista de headers (nombres de columnas) de un archivo CSV.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV
- `delimitador` (str): Delimitador usado (por defecto: `,`)

**Retorna:**
- `List[str]`: Lista con los nombres de las columnas

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si el archivo está vacío

**Ejemplo:**
```python
headers = obtener_headers("datos.csv")
# ['nombre', 'edad', 'ciudad']
```

---

## 💡 Ejemplos

El proyecto incluye 3 ejemplos ejecutables en la carpeta `ejemplos/`:

### 1. Ejemplo Básico (`ejemplo_basico.py`)

Muestra cómo leer, procesar y escribir archivos CSV.

```bash
python ejemplos/ejemplo_basico.py
```

### 2. Ejemplo de Validación (`ejemplo_validacion.py`)

Muestra cómo validar datos CSV según reglas de negocio.

```bash
python ejemplos/ejemplo_validacion.py
```

### 3. Ejemplo de Pipeline (`ejemplo_pipeline.py`)

Muestra un pipeline completo: Extract → Validate → Transform → Load.

```bash
python ejemplos/ejemplo_pipeline.py
```

---

## 🧪 Tests

El proyecto tiene **54 tests** con una **cobertura del 99%**.

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=term --cov-report=html

# Ejecutar tests de un módulo específico
pytest tests/test_lector_csv.py -v
```

### Cobertura de Tests

```
Name                       Stmts   Miss  Cover
----------------------------------------------
src/__init__.py                1      0   100%
src/escritor_csv.py           11      0   100%
src/lector_csv.py             24      0   100%
src/transformador_csv.py      30      0   100%
src/utilidades.py             22      0   100%
src/validador_csv.py          36      1    97%
----------------------------------------------
TOTAL                        124      1    99%
```

---

## 🏛️ Arquitectura

### Principios de Diseño

1. **Funcional First**: Funciones puras sin clases innecesarias
2. **Modularidad**: Cada módulo tiene una responsabilidad clara
3. **Sin Efectos Colaterales**: Las funciones no modifican sus parámetros
4. **Composabilidad**: Las funciones se pueden combinar fácilmente
5. **Explícito sobre Implícito**: Nombres claros, comportamiento obvio

### Estructura del Proyecto

```
04-proyecto-practico/
├── src/                      # Código fuente
│   ├── lector_csv.py        # Funciones de lectura
│   ├── escritor_csv.py      # Funciones de escritura
│   ├── validador_csv.py     # Funciones de validación
│   ├── transformador_csv.py # Funciones de transformación
│   └── utilidades.py        # Funciones auxiliares
│
├── tests/                    # Tests (cobertura 99%)
│   ├── test_lector_csv.py
│   ├── test_escritor_csv.py
│   ├── test_validador_csv.py
│   ├── test_transformador_csv.py
│   └── test_utilidades.py
│
├── ejemplos/                 # Ejemplos ejecutables
│   ├── ejemplo_basico.py
│   ├── ejemplo_validacion.py
│   └── ejemplo_pipeline.py
│
├── datos/                    # Datos de ejemplo
│   └── muestra.csv
│
├── README.md                 # Este archivo
└── requirements.txt          # Dependencias
```

---

## ✅ Buenas Prácticas Implementadas

### 1. TDD Estricto

- ✅ Tests escritos **PRIMERO**, implementación después
- ✅ Ciclo Red → Green → Refactor
- ✅ Cobertura del 99%

### 2. Tipado Explícito

```python
def leer_csv(
    ruta_archivo: str,
    delimitador: str = ",",
    encoding: str = "utf-8"
) -> List[Dict[str, str]]:
    ...
```

### 3. Docstrings Completos

Todas las funciones tienen docstrings con:
- Descripción
- Parámetros
- Retorno
- Excepciones
- Ejemplos

### 4. Manejo Robusto de Errores

```python
if not os.path.exists(ruta_archivo):
    raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")
```

### 5. Funciones Puras

```python
# ✅ CORRECTO: No modifica la lista original
def agregar_columna(datos, nombre, funcion):
    resultado = []
    for fila in datos:
        nueva_fila = fila.copy()  # Copia
        nueva_fila[nombre] = funcion(fila)
        resultado.append(nueva_fila)
    return resultado
```

### 6. Rutas Multiplataforma

```python
import os
from pathlib import Path

# Funciona en Windows, Linux y Mac
ruta = Path("datos") / "archivo.csv"
```

### 7. Context Managers

```python
# Cierre automático de archivos
with open(archivo, "r", encoding="utf-8") as f:
    datos = f.read()
```

### 8. Encoding Explícito

```python
# Siempre especificar encoding
with open(archivo, "r", encoding="utf-8") as f:
    ...
```

---

## 🔒 Seguridad

### Validaciones Implementadas

- ✅ Validación de existencia de archivos
- ✅ Validación de archivos vacíos
- ✅ Validación de tipos de datos
- ✅ Validación de headers esperados
- ✅ Manejo explícito de errores

### Mejoras de Seguridad Recomendadas

1. **Límite de tamaño de archivo**: Añadir validación para archivos muy grandes
2. **Sanitización de rutas**: Validar que las rutas no contengan `..` (path traversal)
3. **Límite de memoria**: Implementar procesamiento streaming para archivos grandes
4. **Validación de encoding**: Detectar y manejar encodings incorrectos

---

## 📝 Convenciones de Código

- **Funciones y variables**: `snake_case`
- **Constantes**: `MAYUSCULAS_CON_GUIONES`
- **Clases**: `PascalCase` (solo para conectores externos)
- **Archivos**: `snake_case.py`
- **Sin tildes ni espacios** en nombres

---

## 🤝 Contribuir

Este es un proyecto educativo del Master en Data Engineering. Para contribuir:

1. Seguir las reglas del archivo `REGLAS_CRITICAS_AGENTES.md`
2. Escribir tests PRIMERO (TDD)
3. Mantener cobertura >80%
4. Usar tipado explícito
5. Documentar con docstrings completos

---

## 📄 Licencia

Proyecto educativo del Master en Data Engineering.

---

## 👨‍💻 Autor

Proyecto práctico desarrollado siguiendo metodología TDD y arquitectura funcional.

---

**Última actualización:** 2025-10-19
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Logs y Debugging - 01 Teoria](../../tema-3-logs-debugging/01-TEORIA.md)
