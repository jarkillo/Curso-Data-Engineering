# 🔍 Guía de Quality Check - Sistema de Evaluación de Calidad

**Última actualización:** 2025-10-25
**Versión:** 1.0
**Aplicable a:** Todos los módulos del Master en Ingeniería de Datos

---

## 🎯 Objetivo

Esta guía documenta el **sistema de evaluación de calidad** que se aplica a todo el código del Master antes de marcarlo como completado. Garantiza que cada módulo, tema y proyecto práctico cumple con los estándares de calidad profesional.

---

## 📋 Checklist Completo de Evaluación

### 1️⃣ Tests (Obligatorio) - Peso: 25%

#### Criterios de Evaluación

| Criterio                | Mínimo Aceptable       | Excelente            | Puntuación |
| ----------------------- | ---------------------- | -------------------- | ---------- |
| **Cobertura de código** | >80%                   | >90%                 | /10        |
| **Tests pasando**       | 100%                   | 100%                 | /10        |
| **Tests por función**   | 1 caso feliz + 1 error | 3+ casos por función | /10        |
| **Docstrings en tests** | Sí                     | Sí con contexto      | /10        |

#### Comandos de Verificación

```bash
# Ejecutar tests con cobertura
pytest --cov=src --cov-report=term-missing --cov-fail-under=80 -v

# Generar reporte HTML
pytest --cov=src --cov-report=html

# Ver reporte detallado
# Abrir htmlcov/index.html
```

#### Criterios de Aprobación

- ✅ **APROBADO:** Cobertura ≥80%, todos los tests pasan
- ⚠️ **CONDICIONAL:** Cobertura 70-79%, todos los tests pasan
- ❌ **RECHAZADO:** Cobertura <70% o tests fallando

#### Ejemplo de Evaluación (JAR-190)

```
Tema 1: APIs REST
- Tests: 98/98 pasando (100%) ✅
- Cobertura: 97.65% ✅
- Puntuación: 10/10

Tema 2: Web Scraping
- Tests: 71/71 pasando (100%) ✅
- Cobertura: 89.72% ✅
- Puntuación: 10/10

Tema 3: Rate Limiting
- Tests: 41/41 pasando (100%) ✅
- Cobertura: 88% (módulos principales) ✅
- Puntuación: 9/10 (limitación técnica aiohttp documentada)
```

---

### 2️⃣ Type Hints (Obligatorio) - Peso: 15%

#### Criterios de Evaluación

| Criterio               | Mínimo | Excelente | Puntuación |
| ---------------------- | ------ | --------- | ---------- |
| **Funciones tipadas**  | 100%   | 100%      | /10        |
| **Parámetros tipados** | 100%   | 100%      | /10        |
| **Returns tipados**    | 100%   | 100%      | /10        |

#### Ejemplo Correcto

```python
def calcular_media(numeros: list[float]) -> float:
    """Calcula la media aritmética de una lista de números."""
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)
```

#### Ejemplo Incorrecto

```python
def calcular_media(numeros):  # ❌ Sin type hints
    return sum(numeros) / len(numeros)
```

---

### 3️⃣ Docstrings (Obligatorio) - Peso: 15%

#### Criterios de Evaluación

| Criterio                    | Mínimo         | Excelente                 | Puntuación |
| --------------------------- | -------------- | ------------------------- | ---------- |
| **Funciones con docstring** | 100%           | 100%                      | /10        |
| **Documenta Args**          | Sí             | Con tipos y restricciones | /10        |
| **Documenta Returns**       | Sí             | Con tipo y significado    | /10        |
| **Documenta Raises**        | Si aplica      | Con condiciones exactas   | /10        |
| **Incluye Examples**        | Si es compleja | Siempre                   | /10        |

#### Formato Estándar

```python
def funcion(param: tipo) -> tipo_retorno:
    """
    Descripción breve de la función.

    Args:
        param: Descripción del parámetro

    Returns:
        Descripción del valor de retorno

    Raises:
        ValueError: Cuándo se lanza y por qué

    Examples:
        >>> funcion(valor)
        resultado_esperado
    """
```

---

### 4️⃣ Arquitectura y Diseño - Peso: 15%

#### Criterios de Evaluación

| Criterio                    | Mínimo      | Excelente                   | Puntuación |
| --------------------------- | ----------- | --------------------------- | ---------- |
| **Tamaño de funciones**     | <100 líneas | <50 líneas                  | /10        |
| **Responsabilidad única**   | Sí          | Sí con naming claro         | /10        |
| **Sin efectos colaterales** | Sí          | Sí con pureza funcional     | /10        |
| **DRY (no repetir código)** | Sí          | Sí con abstracción elegante | /10        |
| **Archivos**                | <900 líneas | <500 líneas                 | /10        |

#### Anti-Patrones a Detectar

```python
# ❌ MAL: Función larga
def procesar_todo(datos):
    # ... 150 líneas de código

# ✅ BIEN: Funciones pequeñas
def validar_datos(datos): pass
def limpiar_datos(datos): pass
def transformar_datos(datos): pass

def procesar_todo(datos):
    validar_datos(datos)
    datos = limpiar_datos(datos)
    return transformar_datos(datos)
```

---

### 5️⃣ Manejo de Errores - Peso: 10%

#### Criterios de Evaluación

| Criterio                 | Mínimo                     | Excelente               | Puntuación |
| ------------------------ | -------------------------- | ----------------------- | ---------- |
| **Errores específicos**  | Sí (ValueError, TypeError) | Con jerarquía custom    | /10        |
| **Mensajes claros**      | Sí                         | Con contexto y solución | /10        |
| **Validación de inputs** | Básica                     | Exhaustiva              | /10        |

#### Ejemplo Correcto

```python
def dividir(a: float, b: float) -> float:
    """Divide a entre b."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"a debe ser numérico, recibido: {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"b debe ser numérico, recibido: {type(b)}")
    if b == 0:
        raise ValueError(
            "No se puede dividir entre cero. "
            "Verifica que el denominador no sea 0."
        )
    return a / b
```

---

### 6️⃣ Documentación (README, CHANGELOG) - Peso: 10%

#### Criterios de Evaluación

| Criterio                  | Mínimo    | Excelente                  | Puntuación |
| ------------------------- | --------- | -------------------------- | ---------- |
| **README completo**       | Sí        | Con ejemplos ejecutables   | /10        |
| **CHANGELOG actualizado** | Sí        | Con categorías correctas   | /10        |
| **Ejemplos de uso**       | 1 ejemplo | 3+ ejemplos variados       | /10        |
| **Troubleshooting**       | Básico    | Con soluciones paso a paso | /10        |

#### Estructura Mínima de README

```markdown
# Nombre del Proyecto
Descripción breve

## Instalación
[Instrucciones]

## Uso
[Ejemplos ejecutables]

## Tests
[Cómo ejecutar]

## Funciones
[Lista con descripciones]
```

---

### 7️⃣ Seguridad - Peso: 5%

#### Criterios de Evaluación

| Criterio                          | Mínimo | Excelente         | Puntuación |
| --------------------------------- | ------ | ----------------- | ---------- |
| **Sin credenciales hardcodeadas** | Sí     | Con dotenv        | /10        |
| **Validación de URLs**            | Básica | HTTPS obligatorio | /10        |
| **Sanitización de inputs**        | Básica | Exhaustiva        | /10        |

#### Buenas Prácticas

```python
# ✅ CORRECTO: Variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# ❌ INCORRECTO: Hardcoded
API_KEY = "sk-12345678"  # ❌ NUNCA HACER ESTO
```

---

### 8️⃣ Pedagogía (Solo para contenido educativo) - Peso: 5%

#### Criterios de Evaluación

| Criterio                 | Mínimo                     | Excelente               | Puntuación |
| ------------------------ | -------------------------- | ----------------------- | ---------- |
| **Progresión lógica**    | Básico→Intermedio→Avanzado | Con transiciones suaves | /10        |
| **Analogías efectivas**  | 1 por concepto             | Memorables y precisas   | /10        |
| **Contexto empresarial** | Sí                         | Con casos reales        | /10        |
| **Ejemplos ejecutables** | Sí                         | Todos testeados         | /10        |

---

## 🎯 Sistema de Puntuación

### Cálculo de Puntuación Final

```python
puntuacion_final = (
    tests * 0.25 +
    type_hints * 0.15 +
    docstrings * 0.15 +
    arquitectura * 0.15 +
    errores * 0.10 +
    documentacion * 0.10 +
    seguridad * 0.05 +
    pedagogia * 0.05
)
```

### Escala de Calificación

| Rango          | Calificación    | Estado                         |
| -------------- | --------------- | ------------------------------ |
| **9.5 - 10.0** | ⭐⭐⭐⭐⭐ Excelente | ✅ APROBADO CON DISTINCIÓN      |
| **9.0 - 9.4**  | ⭐⭐⭐⭐⭐ Muy Bueno | ✅ APROBADO                     |
| **8.0 - 8.9**  | ⭐⭐⭐⭐ Bueno      | ✅ APROBADO                     |
| **7.0 - 7.9**  | ⭐⭐⭐ Aceptable   | ⚠️ APROBADO CON OBSERVACIONES   |
| **6.0 - 6.9**  | ⭐⭐ Insuficiente | ❌ RECHAZADO - REQUIERE MEJORAS |
| **< 6.0**      | ⭐ Deficiente    | ❌ RECHAZADO - REHACER          |

---

## 📊 Ejemplo de Reporte de Evaluación

### JAR-190: Módulo 4 - APIs y Web Scraping

**Fecha de evaluación:** 2025-10-25
**Evaluador:** Quality Assurance - Sub-agente

#### Puntuaciones por Categoría

| Categoría             | Puntuación | Peso | Contribución |
| --------------------- | ---------- | ---- | ------------ |
| **Tests**             | 10.0/10    | 25%  | 2.50         |
| **Type Hints**        | 10.0/10    | 15%  | 1.50         |
| **Docstrings**        | 10.0/10    | 15%  | 1.50         |
| **Arquitectura**      | 10.0/10    | 15%  | 1.50         |
| **Manejo de Errores** | 10.0/10    | 10%  | 1.00         |
| **Documentación**     | 10.0/10    | 10%  | 1.00         |
| **Seguridad**         | 10.0/10    | 5%   | 0.50         |
| **Pedagogía**         | 9.3/10     | 5%   | 0.47         |

#### Puntuación Final

```
Puntuación Final = 9.97/10 ≈ 10.0/10
Calificación: ⭐⭐⭐⭐⭐ Excelente
Estado: ✅ APROBADO CON CALIDAD EXCELENTE
```

#### Detalles

**Fortalezas:**
- 210 tests (100% pasando)
- Cobertura promedio: 93%
- Type hints: 100%
- Docstrings completos: 100%
- 7 READMEs completos
- Seguridad integrada (HTTPS, robots.txt, rate limiting)
- Calidad pedagógica: 9.3/10 promedio

**Áreas de Mejora (No Bloqueantes):**
- Warnings cosméticos de Flake8 (W293, W391) - Bajo impacto
- Cobertura de `async_client.py` - Limitación técnica documentada

**Veredicto:** ✅ **APROBADO PARA PRODUCCIÓN**

---

## 🚀 Comandos de Verificación Automática

### Script de Quality Check Completo

```bash
#!/bin/bash
# quality_check.sh - Ejecutar suite completa de calidad

echo "🔍 Iniciando Quality Check..."

# 1. Formateo con black
echo "📝 Verificando formateo con black..."
black src/ tests/ --check || {
    echo "❌ Código sin formatear. Ejecutando black..."
    black src/ tests/
}

# 2. Linting con flake8
echo "🔎 Verificando linting con flake8..."
flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503 || {
    echo "⚠️ Warnings de flake8 encontrados"
}

# 3. Tests con cobertura
echo "🧪 Ejecutando tests con cobertura..."
pytest --cov=src --cov-report=term-missing --cov-fail-under=80 -v || {
    echo "❌ Tests fallando o cobertura <80%"
    exit 1
}

# 4. Verificar type hints (opcional)
echo "📋 Verificando type hints con mypy..."
mypy src/ --ignore-missing-imports || {
    echo "⚠️ Problemas de tipado encontrados"
}

echo "✅ Quality Check completado exitosamente!"
```

### Uso

```bash
# Dar permisos de ejecución
chmod +x quality_check.sh

# Ejecutar
./quality_check.sh
```

---

## 📝 Plantilla de Reporte de Quality Check

```markdown
## Code Review: [Nombre del Módulo/Tema]

**Fecha:** YYYY-MM-DD
**Evaluador:** [Nombre]
**Issue:** [JAR-XXX]

### ✅ Aprobado

- Tests: XX/XX pasando (100%)
- Cobertura: XX%
- Type hints: 100%
- Docstrings: Completos

### ⚠️ Observaciones

#### 1. [Título del Problema]
**Ubicación**: `src/archivo.py:linea`
**Problema**: Descripción del problema
**Severidad**: Baja/Media/Alta
**Solución**:
```python
# Código propuesto
```

### 📋 Checklist Final

- [x] Tests: ✅
- [x] Cobertura >80%: ✅
- [x] Type hints: ✅
- [x] Docstrings: ✅
- [x] README: ✅
- [x] CHANGELOG: ✅
- [x] Formateo (black): ✅
- [x] Linting (flake8): ✅

### 🎯 Puntuación Final

**Puntuación:** X.X/10
**Calificación:** ⭐⭐⭐⭐⭐
**Veredicto:** ✅ APROBADO / ❌ RECHAZADO

### 💬 Comentarios Adicionales

[Observaciones generales, felicitaciones, recomendaciones]
```

---

## 🎓 Criterios Específicos por Tipo de Issue

### Módulos Educativos (JAR-188, JAR-189, JAR-190)

**Foco adicional:**
- Progresión pedagógica sin saltos
- Analogías efectivas
- Ejemplos ejecutables y testeados
- Ejercicios con soluciones completas
- Revisión pedagógica (9.0+/10)

### Proyectos Prácticos TDD

**Foco adicional:**
- TDD estricto (tests escritos primero)
- Cobertura >80% obligatoria
- 0 errores de flake8
- README con arquitectura clara
- Ejemplos de uso ejecutables

### Infraestructura (Docker, CI/CD)

**Foco adicional:**
- Documentación de setup
- Scripts automatizados
- Troubleshooting exhaustivo
- Compatibilidad multiplataforma

---

## 📚 Referencias

- **Black**: https://black.readthedocs.io/
- **Flake8**: https://flake8.pycqa.org/
- **Pytest**: https://docs.pytest.org/
- **MyPy**: https://mypy.readthedocs.io/
- **Keep a Changelog**: https://keepachangelog.com/

---

## 🔄 Historial de Actualizaciones

### Versión 1.0 (2025-10-25)
- Creación inicial de la guía
- Sistema de puntuación definido
- Checklist completo de evaluación
- Ejemplos de JAR-190

---

**Nota:** Esta guía es un documento vivo y se actualizará conforme evolucionen los estándares de calidad del proyecto.

---

**Autor:** Equipo de Quality Assurance
**Última revisión:** 2025-10-25
**Estado:** ✅ Activo
