# ===============================================
# Setup del Master en Ingeniería de Datos
# Sistema: Windows
# ===============================================

Write-Host "=== Setup del Master en Ingeniería de Datos ===" -ForegroundColor Cyan
Write-Host "Sistema: Windows" -ForegroundColor Cyan
Write-Host ""

# ===============================================
# 1. Verificar Python
# ===============================================
Write-Host "==> Paso 1: Verificando Python..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
        Write-Host "    [OK] Python instalado: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] Python 3.11+ no encontrado." -ForegroundColor Red
        Write-Host "    Por favor, instala Python 3.11+ desde: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "    IMPORTANTE: Marca la opción 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "    [ERROR] Python no encontrado en el PATH." -ForegroundColor Red
    Write-Host "    Por favor, instala Python 3.11+ desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# ===============================================
# 2. Verificar pip
# ===============================================
Write-Host "`n==> Paso 2: Verificando pip..." -ForegroundColor Yellow

try {
    $pipVersion = pip --version 2>&1
    Write-Host "    [OK] pip instalado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] pip no encontrado." -ForegroundColor Red
    Write-Host "    Instalando pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# ===============================================
# 3. Verificar Git
# ===============================================
Write-Host "`n==> Paso 3: Verificando Git..." -ForegroundColor Yellow

try {
    $gitVersion = git --version 2>&1
    Write-Host "    [OK] Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "    [WARNING] Git no encontrado." -ForegroundColor Yellow
    Write-Host "    Recomendado: Instala Git desde https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "    Puedes continuar sin Git, pero será necesario para el curso." -ForegroundColor Yellow
}

# ===============================================
# 4. Crear directorio venv si no existe
# ===============================================
Write-Host "`n==> Paso 4: Preparando entorno virtual..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "    [INFO] Entorno virtual ya existe. Eliminando para crear uno limpio..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force venv
}

# ===============================================
# 5. Crear entorno virtual
# ===============================================
Write-Host "`n==> Paso 5: Creando entorno virtual..." -ForegroundColor Yellow

try {
    python -m venv venv
    Write-Host "    [OK] Entorno virtual creado" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] No se pudo crear el entorno virtual." -ForegroundColor Red
    Write-Host "    Intenta: python -m pip install --upgrade pip setuptools" -ForegroundColor Yellow
    exit 1
}

# ===============================================
# 6. Activar entorno virtual
# ===============================================
Write-Host "`n==> Paso 6: Activando entorno virtual..." -ForegroundColor Yellow

try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "    [OK] Entorno virtual activado" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] No se pudo activar el entorno virtual." -ForegroundColor Red
    Write-Host "    Puedes activarlo manualmente: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}

# ===============================================
# 7. Actualizar pip
# ===============================================
Write-Host "`n==> Paso 7: Actualizando pip..." -ForegroundColor Yellow

python -m pip install --upgrade pip
Write-Host "    [OK] pip actualizado" -ForegroundColor Green

# ===============================================
# 8. Instalar dependencias básicas
# ===============================================
Write-Host "`n==> Paso 8: Instalando dependencias básicas..." -ForegroundColor Yellow

$basicPackages = @(
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0"
)

foreach ($package in $basicPackages) {
    Write-Host "    Instalando $package..." -ForegroundColor Cyan
    pip install $package --quiet
}

Write-Host "    [OK] Dependencias básicas instaladas" -ForegroundColor Green

# ===============================================
# 9. Verificar instalación
# ===============================================
Write-Host "`n==> Paso 9: Verificando instalación..." -ForegroundColor Yellow

$allOk = $true

# Verificar pytest
try {
    $pytestVersion = pytest --version 2>&1
    Write-Host "    [OK] pytest: $pytestVersion" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] pytest no se instaló correctamente" -ForegroundColor Red
    $allOk = $false
}

# Verificar black
try {
    $blackVersion = black --version 2>&1
    Write-Host "    [OK] black instalado" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] black no se instaló correctamente" -ForegroundColor Red
    $allOk = $false
}

# Verificar flake8
try {
    $flake8Version = flake8 --version 2>&1
    Write-Host "    [OK] flake8 instalado" -ForegroundColor Green
} catch {
    Write-Host "    [ERROR] flake8 no se instaló correctamente" -ForegroundColor Red
    $allOk = $false
}

# ===============================================
# 10. Resumen
# ===============================================
Write-Host "`n===============================================" -ForegroundColor Cyan
if ($allOk) {
    Write-Host "[SUCCESS] Setup completado correctamente!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Setup completado con algunos errores" -ForegroundColor Yellow
}
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "`nPróximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Activa el entorno: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Ejecuta los tests: pytest" -ForegroundColor White
Write-Host "  3. Para Módulos 5+, instala Docker Desktop" -ForegroundColor White
Write-Host ""
Write-Host "Para instalar todas las dependencias del Master:" -ForegroundColor Yellow
Write-Host "  pip install -r requirements.txt" -ForegroundColor White
Write-Host ""

# ===============================================
# Seguridad: Recordatorio
# ===============================================
Write-Host "[SEGURIDAD] Recuerda:" -ForegroundColor Magenta
Write-Host "  - Nunca compartas tus credenciales en repositorios públicos" -ForegroundColor White
Write-Host "  - Usa variables de entorno para secrets (.env)" -ForegroundColor White
Write-Host "  - Añade .env al .gitignore" -ForegroundColor White
Write-Host ""

