# 🔄 GUÍA DE CI/CD - Integración y Despliegue Continuo

## 📋 Índice

1. [Introducción](#introducción)
2. [Pre-commit Hooks](#pre-commit-hooks)
3. [Pre-push Hooks](#pre-push-hooks)
4. [GitHub Actions](#github-actions)
5. [Configuración Local](#configuración-local)
6. [Comandos Útiles](#comandos-útiles)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este proyecto implementa un sistema completo de CI/CD que garantiza:

- ✅ **Calidad de código** mediante linting y formateo automático
- ✅ **Seguridad** con análisis de vulnerabilidades
- ✅ **Cobertura de tests** mínima del 80%
- ✅ **Type checking** con MyPy
- ✅ **Prevención de errores** antes del commit

### Flujo de Trabajo

```
┌─────────────┐
│   Código    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Pre-commit  │ ← Black, Flake8, MyPy, Tests rápidos
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Commit    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Pre-push   │ ← Tests completos + Cobertura
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Push     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │ ← CI/CD completo + Seguridad
│   Actions   │
└─────────────┘
```

---

## 🪝 Pre-commit Hooks

### ¿Qué son?

Los **pre-commit hooks** se ejecutan **antes de cada commit** y verifican:

1. 🚫 **No commits a main** - Previene commits directos a main
2. ⚫ **Black** - Formatea el código automáticamente
3. 📚 **isort** - Ordena los imports
4. 🔍 **Flake8** - Linting de código
5. 🔎 **MyPy** - Verificación de tipos
6. 🔒 **Bandit** - Análisis de seguridad
7. 🧪 **Pytest** - Tests rápidos (solo archivos modificados)

### Instalación

```bash
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 2. Instalar pre-commit
pip install pre-commit

# 3. Instalar hooks
pre-commit install
```

### Uso Automático

Los hooks se ejecutan **automáticamente** en cada commit:

```bash
git add archivo.py
git commit -m "feat: nueva funcionalidad"

# ↓ Se ejecutan automáticamente:
# ⚫ Black - Formatear código
# 📚 isort - Ordenar imports
# 🔍 Flake8 - Linting
# 🔎 MyPy - Type checking
# 🔒 Bandit - Seguridad
# 🧪 Pytest - Tests
```

### Uso Manual

Ejecutar todos los hooks manualmente:

```bash
# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar en archivos staged
pre-commit run

# Ejecutar un hook específico
pre-commit run black
pre-commit run flake8
pre-commit run pytest-quick
```

### Saltar Hooks (NO RECOMENDADO)

```bash
# ⚠️ Solo en casos excepcionales
git commit -m "mensaje" --no-verify
```

**IMPORTANTE:** Solo usar `--no-verify` si:
- Es una emergencia crítica
- Los hooks tienen un falso positivo
- Vas a arreglarlo en el siguiente commit

---

## 🚀 Pre-push Hooks

### ¿Qué son?

Los **pre-push hooks** se ejecutan **antes de cada push** y verifican:

1. 🧪 **Tests completos** - Ejecuta toda la suite de tests
2. 📊 **Cobertura mínima** - Verifica cobertura >= 80%

### Instalación

```bash
# Instalar hooks de pre-push
pre-commit install --hook-type pre-push
```

### Uso Automático

Se ejecutan automáticamente en cada push:

```bash
git push origin feature/mi-rama

# ↓ Se ejecutan automáticamente:
# 🧪 Tests completos
# 📊 Verificación de cobertura >= 80%
```

### Saltar Pre-push (NO RECOMENDADO)

```bash
# ⚠️ Solo en casos excepcionales
git push --no-verify
```

---

## 🤖 GitHub Actions

### Workflows Configurados

#### 1. **CI - Integración Continua** (`.github/workflows/ci.yml`)

Se ejecuta en:
- Push a `main` o `dev`
- Pull Requests a `main` o `dev`

**Jobs:**

1. **🔍 Linting y Formateo**
   - Black (verificación de formato)
   - isort (verificación de imports)
   - Flake8 (linting)
   - MyPy (type checking)

2. **🧪 Tests**
   - Ejecuta toda la suite de tests
   - Genera reporte de cobertura
   - Sube cobertura a Codecov

3. **🔒 Seguridad**
   - Bandit (análisis de código)
   - Safety (vulnerabilidades en dependencias)

4. **🏗️ Build y Validación**
   - Build del paquete
   - Verificación de distribución

5. **📊 Reporte Final**
   - Resumen de todos los checks

#### 2. **PR Checks** (`.github/workflows/pr-checks.yml`)

Se ejecuta en:
- Pull Requests a `main` o `dev`

**Jobs:**

1. **📋 Validación de PR**
   - Verifica título (Conventional Commits)
   - Verifica descripción mínima
   - Analiza archivos modificados

2. **📊 Análisis de Cambios**
   - Detecta tipos de archivos modificados
   - Comenta en el PR los cambios detectados

3. **🧪 Cobertura de Tests**
   - Ejecuta tests con cobertura
   - Comenta el porcentaje en el PR

4. **🔒 Verificación de Seguridad**
   - Ejecuta Bandit
   - Comenta resultados en el PR

#### 3. **CodeQL** (`.github/workflows/codeql.yml`)

Se ejecuta en:
- Push a `main` o `dev`
- Pull Requests
- Semanalmente (lunes 00:00 UTC)

**Análisis:**
- Seguridad avanzada con CodeQL
- Detección de vulnerabilidades
- Análisis de calidad de código

---

## ⚙️ Configuración Local

### 1. Clonar el Repositorio

```bash
git clone https://github.com/jarkillo/Curso-Data-Engineering.git
cd Curso-Data-Engineering
```

### 2. Crear y Activar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar
.\venv\Scripts\Activate.ps1  # Windows PowerShell
.\venv\Scripts\activate.bat  # Windows CMD
source venv/bin/activate      # Linux/Mac
```

### 3. Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Instalar pre-commit
pip install pre-commit
```

### 4. Configurar Pre-commit

```bash
# Instalar hooks de pre-commit
pre-commit install

# Instalar hooks de pre-push
pre-commit install --hook-type pre-push

# Verificar instalación
pre-commit run --all-files
```

### 5. Verificar Configuración

```bash
# Verificar que el entorno virtual está activado
which python  # Linux/Mac
where python  # Windows
# Debe mostrar la ruta del venv

# Verificar pre-commit
pre-commit --version

# Verificar pytest
pytest --version

# Ejecutar tests
pytest tests/ -v
```

---

## 🛠️ Comandos Útiles

### Pre-commit

```bash
# Ejecutar todos los hooks
pre-commit run --all-files

# Ejecutar hook específico
pre-commit run black
pre-commit run flake8
pre-commit run mypy
pre-commit run pytest-quick

# Actualizar hooks a última versión
pre-commit autoupdate

# Desinstalar hooks
pre-commit uninstall
```

### Tests

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con verbosidad
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_estadisticas.py

# Ejecutar con cobertura
pytest tests/ --cov=. --cov-report=term-missing

# Ejecutar con cobertura HTML
pytest tests/ --cov=. --cov-report=html
# Abrir htmlcov/index.html en el navegador

# Parar en el primer fallo
pytest tests/ -x

# Parar después de N fallos
pytest tests/ --maxfail=3
```

### Linting

```bash
# Black - Formatear
black .

# Black - Solo verificar
black --check .

# Flake8 - Linting
flake8 .

# isort - Ordenar imports
isort .

# isort - Solo verificar
isort --check-only .

# MyPy - Type checking
mypy .
```

### Seguridad

```bash
# Bandit - Análisis de seguridad
bandit -r . -c pyproject.toml

# Safety - Vulnerabilidades en dependencias
pip install safety
safety check

# Safety - Formato JSON
safety check --json
```

---

## 🔧 Troubleshooting

### Problema: Pre-commit muy lento

**Solución 1: Ejecutar solo en archivos modificados**
```bash
# En lugar de --all-files
pre-commit run
```

**Solución 2: Saltar tests en pre-commit**
```bash
# Editar .pre-commit-config.yaml
# Cambiar pytest-quick a stages: [manual]
```

**Solución 3: Usar cache**
```bash
# Pre-commit usa cache automáticamente
# Limpiar cache si hay problemas
pre-commit clean
```

### Problema: Tests fallan en pre-commit pero pasan localmente

**Causa:** Diferencias en el entorno

**Solución:**
```bash
# 1. Verificar que el entorno virtual está activado
which python  # Debe mostrar venv

# 2. Reinstalar dependencias
pip install -r requirements.txt

# 3. Limpiar cache de pytest
pytest --cache-clear

# 4. Ejecutar tests manualmente
pytest tests/ -v
```

### Problema: Black y Flake8 en conflicto

**Solución:** Ya está configurado en `.flake8`:
```ini
[flake8]
extend-ignore = E203, E501, W503
```

Si hay conflictos:
```bash
# 1. Ejecutar black primero
black .

# 2. Luego flake8
flake8 .
```

### Problema: MyPy reporta muchos errores

**Solución temporal:**
```bash
# Ignorar imports faltantes
mypy . --ignore-missing-imports

# O añadir al archivo:
# type: ignore
```

**Solución permanente:**
- Añadir type hints progresivamente
- Usar `# type: ignore` solo cuando sea necesario

### Problema: Bandit reporta falsos positivos

**Solución:**
```python
# Ignorar línea específica
password = "test"  # nosec B105

# Ignorar función
def test_function():  # nosec
    pass
```

O configurar en `pyproject.toml`:
```toml
[tool.bandit]
skips = ["B101", "B601"]
```

### Problema: Cobertura < 80%

**Solución:**
```bash
# 1. Ver qué falta cubrir
pytest tests/ --cov=. --cov-report=term-missing

# 2. Ver reporte HTML detallado
pytest tests/ --cov=. --cov-report=html
# Abrir htmlcov/index.html

# 3. Añadir tests para líneas faltantes
```

### Problema: GitHub Actions falla pero local pasa

**Causas comunes:**
1. Dependencias faltantes en `requirements.txt`
2. Rutas hardcodeadas (usar `Path` o `os.path`)
3. Diferencias Windows/Linux

**Solución:**
```bash
# 1. Verificar requirements.txt actualizado
pip freeze > requirements-freeze.txt
# Comparar con requirements.txt

# 2. Usar rutas relativas
from pathlib import Path
BASE_DIR = Path(__file__).parent

# 3. Probar en contenedor Docker
docker run -it python:3.13 bash
```

---

## 📚 Referencias

- [Pre-commit Documentation](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🎯 Mejores Prácticas

### 1. Commits Pequeños y Frecuentes

```bash
# ✅ BIEN
git add archivo1.py
git commit -m "feat: añadir función calcular_media"

git add archivo2.py
git commit -m "test: añadir tests para calcular_media"

# ❌ MAL
git add .
git commit -m "cambios varios"
```

### 2. Ejecutar Tests Antes de Commit

```bash
# Siempre ejecutar tests antes
pytest tests/ -v

# Luego commit
git add .
git commit -m "feat: nueva funcionalidad"
```

### 3. Revisar Cambios Antes de Commit

```bash
# Ver cambios
git diff

# Ver cambios staged
git diff --staged

# Luego commit
git commit -m "mensaje"
```

### 4. Usar Conventional Commits

```bash
# Formato: tipo: descripción

# Tipos válidos:
feat:     # Nueva funcionalidad
fix:      # Corrección de bug
docs:     # Documentación
style:    # Formato (no afecta código)
refactor: # Refactorización
perf:     # Mejora de rendimiento
test:     # Tests
build:    # Sistema de build
ci:       # CI/CD
chore:    # Mantenimiento
revert:   # Revertir cambio
```

### 5. Mantener Cobertura Alta

```bash
# Objetivo: >= 80%
pytest tests/ --cov=. --cov-report=term-missing

# Si baja de 80%, añadir tests
```

---

**Última actualización:** 2025-10-18
**Versión:** 1.0.0
**Autor:** Master Data Engineering
