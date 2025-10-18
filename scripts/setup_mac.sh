#!/bin/bash
# ===============================================
# Setup del Master en Ingeniería de Datos
# Sistema: macOS
# ===============================================

set -e  # Salir si hay errores

echo "=== Setup del Master en Ingeniería de Datos ==="
echo "Sistema: macOS"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# ===============================================
# 1. Verificar Homebrew (recomendado)
# ===============================================
echo -e "${YELLOW}==> Paso 1: Verificando Homebrew...${NC}"

if command -v brew &> /dev/null; then
    BREW_VERSION=$(brew --version 2>&1 | head -n 1)
    echo -e "    ${GREEN}[OK] Homebrew instalado: $BREW_VERSION${NC}"
else
    echo -e "    ${YELLOW}[WARNING] Homebrew no encontrado.${NC}"
    echo -e "    ${YELLOW}Recomendado para gestionar dependencias en macOS${NC}"
    echo "    Instalar: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
fi

# ===============================================
# 2. Verificar Python
# ===============================================
echo -e "${YELLOW}==> Paso 2: Verificando Python...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        echo -e "    ${GREEN}[OK] Python instalado: $PYTHON_VERSION${NC}"
    else
        echo -e "    ${RED}[ERROR] Python 3.11+ requerido. Versión actual: $PYTHON_VERSION${NC}"
        echo -e "    ${YELLOW}Instala Python 3.11+ con Homebrew:${NC}"
        echo "    brew install python@3.11"
        echo -e "    ${YELLOW}O descarga desde: https://www.python.org/downloads/macos/${NC}"
        exit 1
    fi
else
    echo -e "    ${RED}[ERROR] Python 3 no encontrado.${NC}"
    echo -e "    ${YELLOW}Instala Python con Homebrew:${NC}"
    echo "    brew install python@3.11"
    echo -e "    ${YELLOW}O descarga desde: https://www.python.org/downloads/macos/${NC}"
    exit 1
fi

# ===============================================
# 3. Verificar pip
# ===============================================
echo -e "\n${YELLOW}==> Paso 3: Verificando pip...${NC}"

if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1)
    echo -e "    ${GREEN}[OK] pip instalado: $PIP_VERSION${NC}"
else
    echo -e "    ${YELLOW}[WARNING] pip no encontrado. Instalando...${NC}"
    python3 -m ensurepip --upgrade
fi

# ===============================================
# 4. Verificar Git
# ===============================================
echo -e "\n${YELLOW}==> Paso 4: Verificando Git...${NC}"

if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1)
    echo -e "    ${GREEN}[OK] Git instalado: $GIT_VERSION${NC}"
else
    echo -e "    ${YELLOW}[WARNING] Git no encontrado.${NC}"
    echo -e "    ${YELLOW}Recomendado: brew install git${NC}"
    echo "    Puedes continuar sin Git, pero será necesario para el curso."
fi

# ===============================================
# 5. Preparar entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 5: Preparando entorno virtual...${NC}"

if [ -d "venv" ]; then
    echo -e "    ${CYAN}[INFO] Entorno virtual ya existe. Eliminando para crear uno limpio...${NC}"
    rm -rf venv
fi

# ===============================================
# 6. Crear entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 6: Creando entorno virtual...${NC}"

python3 -m venv venv
if [ $? -eq 0 ]; then
    echo -e "    ${GREEN}[OK] Entorno virtual creado${NC}"
else
    echo -e "    ${RED}[ERROR] No se pudo crear el entorno virtual.${NC}"
    echo -e "    ${YELLOW}Intenta: python3 -m pip install --upgrade pip setuptools${NC}"
    exit 1
fi

# ===============================================
# 7. Activar entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 7: Activando entorno virtual...${NC}"

source venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "    ${GREEN}[OK] Entorno virtual activado${NC}"
else
    echo -e "    ${RED}[ERROR] No se pudo activar el entorno virtual.${NC}"
    exit 1
fi

# ===============================================
# 8. Actualizar pip
# ===============================================
echo -e "\n${YELLOW}==> Paso 8: Actualizando pip...${NC}"

pip install --upgrade pip > /dev/null 2>&1
echo -e "    ${GREEN}[OK] pip actualizado${NC}"

# ===============================================
# 9. Instalar dependencias básicas
# ===============================================
echo -e "\n${YELLOW}==> Paso 9: Instalando dependencias básicas...${NC}"

BASIC_PACKAGES=(
    "pytest>=7.4.0"
    "pytest-cov>=4.1.0"
    "black>=23.7.0"
    "flake8>=6.1.0"
    "mypy>=1.5.0"
)

for package in "${BASIC_PACKAGES[@]}"; do
    echo -e "    ${CYAN}Instalando $package...${NC}"
    pip install "$package" --quiet
done

echo -e "    ${GREEN}[OK] Dependencias básicas instaladas${NC}"

# ===============================================
# 10. Verificar instalación
# ===============================================
echo -e "\n${YELLOW}==> Paso 10: Verificando instalación...${NC}"

ALL_OK=true

# Verificar pytest
if command -v pytest &> /dev/null; then
    PYTEST_VERSION=$(pytest --version 2>&1)
    echo -e "    ${GREEN}[OK] pytest: $PYTEST_VERSION${NC}"
else
    echo -e "    ${RED}[ERROR] pytest no se instaló correctamente${NC}"
    ALL_OK=false
fi

# Verificar black
if command -v black &> /dev/null; then
    echo -e "    ${GREEN}[OK] black instalado${NC}"
else
    echo -e "    ${RED}[ERROR] black no se instaló correctamente${NC}"
    ALL_OK=false
fi

# Verificar flake8
if command -v flake8 &> /dev/null; then
    echo -e "    ${GREEN}[OK] flake8 instalado${NC}"
else
    echo -e "    ${RED}[ERROR] flake8 no se instaló correctamente${NC}"
    ALL_OK=false
fi

# ===============================================
# 11. Resumen
# ===============================================
echo ""
echo -e "${CYAN}===============================================${NC}"
if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}[SUCCESS] Setup completado correctamente!${NC}"
else
    echo -e "${YELLOW}[WARNING] Setup completado con algunos errores${NC}"
fi
echo -e "${CYAN}===============================================${NC}"

echo -e "\n${YELLOW}Próximos pasos:${NC}"
echo "  1. Activa el entorno: source venv/bin/activate"
echo "  2. Ejecuta los tests: pytest"
echo "  3. Para Módulos 5+, instala Docker Desktop"
echo ""
echo -e "${YELLOW}Para instalar todas las dependencias del Master:${NC}"
echo "  pip install -r requirements.txt"
echo ""

# ===============================================
# Seguridad: Recordatorio
# ===============================================
echo -e "${MAGENTA}[SEGURIDAD] Recuerda:${NC}"
echo "  - Nunca compartas tus credenciales en repositorios públicos"
echo "  - Usa variables de entorno para secrets (.env)"
echo "  - Añade .env al .gitignore"
echo ""

# ===============================================
# Nota sobre macOS específico
# ===============================================
echo -e "${CYAN}[NOTA macOS]${NC}"
echo "  - Si usas un Mac con chip M1/M2, algunas librerías pueden requerir"
echo "    instalación específica (especialmente para Spark y ML)"
echo "  - Usa Rosetta 2 si encuentras problemas de compatibilidad"
echo ""

