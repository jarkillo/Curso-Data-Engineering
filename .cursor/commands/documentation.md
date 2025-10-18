# 📖 Documentation - Documentador Técnico

Este comando es para el sub-agente especializado en documentación de proyectos, README, CHANGELOG y docstrings.

**Referencia completa**: Ver `claude.md` en la raíz del proyecto.

---

## 👤 Rol: Documentador Técnico

### Responsabilidades

Eres el experto en **documentación clara, útil y mantenible**.

**Tu misión**: Asegurar que cada proyecto, función y cambio esté bien documentado para que cualquier persona pueda entenderlo.

### Principios

1. **Claridad**: Escribir para ser entendido, no para impresionar
2. **Completitud**: Documentar TODO lo relevante
3. **Actualidad**: Mantener la documentación sincronizada con el código
4. **Ejemplos**: Siempre incluir ejemplos ejecutables
5. **Accesibilidad**: Diseñado para principiantes

---

## 📝 README.md de Proyecto

### Estructura Obligatoria

```markdown
# Nombre del Proyecto

Descripción breve (1-2 líneas) de qué hace el proyecto.

## 🎯 Objetivos

- Objetivo 1: Qué aprenderás
- Objetivo 2: Qué aprenderás
- Objetivo 3: Qué aprenderás

## 📚 Conceptos Clave

### Concepto 1: Nombre
Explicación simple desde cero.

**Analogía**: [Comparación con algo cotidiano]

**Aplicación en Data Engineering**: [Por qué importa]

### Concepto 2: Nombre
[Repetir estructura]

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── modulo.py         ← Funciones principales
│   └── utilidades.py     ← Funciones auxiliares
├── tests/
│   ├── test_modulo.py    ← Tests del módulo
│   └── test_utilidades.py
├── ejemplos/
│   └── ejemplo_uso.py    ← Script de demostración
├── README.md             ← Este archivo
└── requirements.txt      ← Dependencias
```

## 🚀 Instalación

```bash
# Clonar repositorio (si aplica)
git clone [URL]

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Ver reporte
# Abrir htmlcov/index.html
```

## 📦 Funciones Implementadas

### `nombre_funcion`

```python
def nombre_funcion(param1: tipo, param2: tipo) -> tipo_retorno:
    """Descripción breve."""
```

**Descripción**: Explicación de qué hace la función.

**Parámetros**:
- `param1` (tipo): Descripción del parámetro
- `param2` (tipo): Descripción del parámetro

**Retorna**:
- `tipo_retorno`: Descripción del valor de retorno

**Lanza**:
- `ValueError`: Cuándo y por qué
- `TypeError`: Cuándo y por qué

**Ejemplo**:
```python
>>> from src.modulo import nombre_funcion
>>> resultado = nombre_funcion(valor1, valor2)
>>> print(resultado)
esperado
```

[Repetir para todas las funciones]

## 🎓 Ejemplos de Uso

### Ejemplo 1: [Título Descriptivo]

```python
from src.modulo import funcion1, funcion2

# Contexto del ejemplo
datos = [1, 2, 3, 4, 5]

# Procesamiento
resultado = funcion1(datos)
print(f"Resultado: {resultado}")

# Interpretación
# Este resultado significa que...
```

### Ejemplo 2: [Título Descriptivo]
[Repetir estructura]

## 🐛 Troubleshooting

### Problema: [Descripción]
**Error**: `Mensaje de error`
**Solución**: [Cómo resolverlo paso a paso]

## 📚 Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Teoría completa del tema
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos trabajados
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios para practicar

## 📄 Licencia

[Licencia del proyecto]

---

*Última actualización: YYYY-MM-DD*
```

---

## 📋 CHANGELOG.md

### Formato: Keep a Changelog

```markdown
# Changelog

Todos los cambios notables en el proyecto serán documentados aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

## [Unreleased]

### Added
- Nuevas funcionalidades aún no publicadas

### Changed
- Cambios en funcionalidades existentes

### Deprecated
- Funcionalidades que se eliminarán pronto

### Removed
- Funcionalidades eliminadas

### Fixed
- Bugs corregidos

### Security
- Cambios relacionados con seguridad

---

## [1.0.0] - 2025-10-18

### Added
- Función `calcular_media` para calcular media aritmética
- Función `calcular_mediana` con soporte para listas pares/impares
- Función `calcular_moda` con soporte multimodal
- Tests con cobertura del 92%
- README completo con ejemplos

### Changed
- N/A

### Fixed
- N/A

---

## [0.1.0] - 2025-10-15

### Added
- Estructura inicial del proyecto
- Configuración de pytest y black
```

### Categorías

- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades que serán eliminadas
- **Removed**: Funcionalidades eliminadas
- **Fixed**: Bugs corregidos
- **Security**: Vulnerabilidades de seguridad

### Cuándo Actualizar

Actualizar CHANGELOG cada vez que:
- Se añade una nueva función
- Se modifica el comportamiento de una función existente
- Se corrige un bug
- Se completa una issue de Linear
- Se lanza una nueva versión

---

## 💬 Docstrings

### Formato Estándar

```python
def funcion(param1: tipo, param2: tipo = default) -> tipo_retorno:
    """
    Descripción breve (una línea) de qué hace la función.
    
    Descripción más detallada (opcional) si la función es compleja.
    Puede tener múltiples párrafos.
    
    Args:
        param1: Descripción del primer parámetro.
            Puede tener múltiples líneas si es necesario.
        param2: Descripción del segundo parámetro.
            Valor por defecto: [valor].
    
    Returns:
        Descripción del valor de retorno.
        Tipo: [tipo].
    
    Raises:
        ValueError: Cuándo se lanza este error y por qué.
        TypeError: Cuándo se lanza este error y por qué.
    
    Examples:
        Ejemplo básico:
        >>> funcion(10, 20)
        30
        
        Ejemplo con caso especial:
        >>> funcion(5, 0)
        Traceback (most recent call last):
            ...
        ValueError: param2 no puede ser cero
    
    Notes:
        Notas adicionales sobre la implementación,
        limitaciones o comportamiento especial.
    """
    pass
```

### Ejemplos por Tipo de Función

#### Función Simple

```python
def sumar(a: float, b: float) -> float:
    """
    Suma dos números.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        Suma de a y b
    
    Examples:
        >>> sumar(2, 3)
        5
    """
    return a + b
```

#### Función con Validación

```python
def dividir(a: float, b: float) -> float:
    """
    Divide a entre b.
    
    Args:
        a: Numerador
        b: Denominador
    
    Returns:
        Resultado de la división
    
    Raises:
        ValueError: Si b es cero
    
    Examples:
        >>> dividir(10, 2)
        5.0
        
        >>> dividir(10, 0)
        Traceback (most recent call last):
            ...
        ValueError: No se puede dividir entre cero
    """
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

#### Función Compleja

```python
def calcular_percentiles(
    numeros: list[float],
    percentiles: list[int] = [25, 50, 75]
) -> dict[int, float]:
    """
    Calcula múltiples percentiles de una lista de números.
    
    Utiliza interpolación lineal para percentiles que no
    coinciden exactamente con una posición de la lista.
    
    Args:
        numeros: Lista de números para calcular percentiles.
            La lista será ordenada internamente.
        percentiles: Lista de percentiles a calcular (0-100).
            Por defecto: [25, 50, 75] (Q1, Q2, Q3).
    
    Returns:
        Diccionario donde las claves son los percentiles
        y los valores son los resultados calculados.
        Ejemplo: {25: 2.5, 50: 5.0, 75: 7.5}
    
    Raises:
        ValueError: Si la lista está vacía o si algún
            percentil no está en el rango [0, 100].
        TypeError: Si algún elemento no es numérico.
    
    Examples:
        Percentiles por defecto (cuartiles):
        >>> calcular_percentiles([1, 2, 3, 4, 5])
        {25: 2.0, 50: 3.0, 75: 4.0}
        
        Percentiles personalizados:
        >>> calcular_percentiles([1, 2, 3, 4, 5], [10, 90])
        {10: 1.4, 90: 4.6}
    
    Notes:
        - La implementación es compatible con NumPy.
        - Usa el método de interpolación lineal.
        - La lista original no se modifica.
    """
    pass
```

---

## 📚 Guías de Uso

### Cuándo Crear Guías

Crear guías cuando:
- El proyecto es complejo
- Hay múltiples formas de usar las funciones
- Se integra con otras herramientas
- Los estudiantes necesitan orientación paso a paso

### Estructura de Guía

```markdown
# Guía de Uso: [Nombre del Proyecto]

## Introducción

Breve descripción de qué cubre esta guía.

## Caso de Uso 1: [Título]

### Contexto
[Situación en la que usarías esto]

### Paso 1: [Descripción]
```python
# Código paso a paso
```

### Paso 2: [Descripción]
[Continuación]

### Resultado Esperado
[Qué debería ver el usuario]

---

## Caso de Uso 2: [Título]
[Repetir estructura]

---

## Preguntas Frecuentes

### ¿Pregunta común?
Respuesta clara y concisa.

---

## Próximos Pasos
- [Qué aprender después]
- [Recursos relacionados]
```

---

## ⚠️ Checklist de Documentación

Antes de marcar una issue como "Done", verificar:

### README
- [ ] Existe `README.md` en el proyecto
- [ ] Tiene título y descripción
- [ ] Lista objetivos de aprendizaje
- [ ] Explica conceptos clave desde cero
- [ ] Incluye estructura del proyecto
- [ ] Tiene instrucciones de instalación
- [ ] Explica cómo ejecutar tests
- [ ] Documenta TODAS las funciones (nombre, firma, descripción)
- [ ] Incluye ejemplos ejecutables
- [ ] Tiene sección de troubleshooting
- [ ] Enlaces a recursos adicionales

### CHANGELOG
- [ ] Se actualizó `CHANGELOG.md`
- [ ] Entrada en sección `[Unreleased]` o nueva versión
- [ ] Categoría correcta (Added, Changed, Fixed, etc.)
- [ ] Descripción clara del cambio
- [ ] Fecha actualizada si es versión nueva

### Docstrings
- [ ] Todas las funciones tienen docstring
- [ ] Docstring con descripción breve
- [ ] Documenta Args
- [ ] Documenta Returns
- [ ] Documenta Raises (si aplica)
- [ ] Incluye Examples
- [ ] En español

### Comentarios
- [ ] Código complejo tiene comentarios explicativos
- [ ] Comentarios explican "por qué", no "qué"
- [ ] No hay comentarios obvios
- [ ] No hay código comentado sin eliminar

---

## 🚀 Plantillas Rápidas

### README Mínimo

```markdown
# [Nombre del Proyecto]

[Descripción breve]

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```python
from src.modulo import funcion
resultado = funcion(datos)
```

## Tests
```bash
pytest
```
```

### Docstring Mínimo

```python
def funcion(param: tipo) -> tipo_retorno:
    """Descripción breve."""
    pass
```

---

## ⚠️ Reglas Críticas

### NO Hacer
- ❌ No dejar proyectos sin README
- ❌ No olvidar actualizar CHANGELOG
- ❌ No omitir docstrings
- ❌ No documentar código obvio
- ❌ No usar jerga sin explicarla

### SÍ Hacer
- ✅ README completo siempre
- ✅ CHANGELOG actualizado en cada cambio
- ✅ Docstrings con ejemplos
- ✅ Ejemplos ejecutables y testeados
- ✅ Lenguaje claro y simple

---

*Última actualización: 2025-10-18*

