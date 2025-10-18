#!/bin/bash
# ===============================================
# Setup del Master en Ingeniería de Datos
# Sistema: Linux
# ===============================================

set -e  # Salir si hay errores

echo "=== Setup del Master en Ingeniería de Datos ==="
echo "Sistema: Linux"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# ===============================================
# 1. Verificar Python
# ===============================================
echo -e "${YELLOW}==> Paso 1: Verificando Python...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        echo -e "    ${GREEN}[OK] Python instalado: $PYTHON_VERSION${NC}"
    else
        echo -e "    ${RED}[ERROR] Python 3.11+ requerido. Versión actual: $PYTHON_VERSION${NC}"
        echo -e "    ${YELLOW}Instala Python 3.11+:${NC}"
        echo "    sudo apt update"
        echo "    sudo apt install python3.11 python3.11-venv python3-pip"
        exit 1
    fi
else
    echo -e "    ${RED}[ERROR] Python 3 no encontrado.${NC}"
    echo -e "    ${YELLOW}Instala Python:${NC}"
    echo "    sudo apt update"
    echo "    sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

# ===============================================
# 2. Verificar pip
# ===============================================
echo -e "\n${YELLOW}==> Paso 2: Verificando pip...${NC}"

if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1)
    echo -e "    ${GREEN}[OK] pip instalado: $PIP_VERSION${NC}"
else
    echo -e "    ${YELLOW}[WARNING] pip no encontrado. Instalando...${NC}"
    sudo apt install python3-pip -y
fi

# ===============================================
# 3. Verificar Git
# ===============================================
echo -e "\n${YELLOW}==> Paso 3: Verificando Git...${NC}"

if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1)
    echo -e "    ${GREEN}[OK] Git instalado: $GIT_VERSION${NC}"
else
    echo -e "    ${YELLOW}[WARNING] Git no encontrado.${NC}"
    echo -e "    ${YELLOW}Recomendado: sudo apt install git${NC}"
    echo "    Puedes continuar sin Git, pero será necesario para el curso."
fi

# ===============================================
# 4. Preparar entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 4: Preparando entorno virtual...${NC}"

if [ -d "venv" ]; then
    echo -e "    ${CYAN}[INFO] Entorno virtual ya existe. Eliminando para crear uno limpio...${NC}"
    rm -rf venv
fi

# ===============================================
# 5. Crear entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 5: Creando entorno virtual...${NC}"

python3 -m venv venv
if [ $? -eq 0 ]; then
    echo -e "    ${GREEN}[OK] Entorno virtual creado${NC}"
else
    echo -e "    ${RED}[ERROR] No se pudo crear el entorno virtual.${NC}"
    echo -e "    ${YELLOW}Intenta: sudo apt install python3-venv${NC}"
    exit 1
fi

# ===============================================
# 6. Activar entorno virtual
# ===============================================
echo -e "\n${YELLOW}==> Paso 6: Activando entorno virtual...${NC}"

source venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "    ${GREEN}[OK] Entorno virtual activado${NC}"
else
    echo -e "    ${RED}[ERROR] No se pudo activar el entorno virtual.${NC}"
    exit 1
fi

# ===============================================
# 7. Actualizar pip
# ===============================================
echo -e "\n${YELLOW}==> Paso 7: Actualizando pip...${NC}"

pip install --upgrade pip > /dev/null 2>&1
echo -e "    ${GREEN}[OK] pip actualizado${NC}"

# ===============================================
# 8. Instalar dependencias básicas
# ===============================================
echo -e "\n${YELLOW}==> Paso 8: Instalando dependencias básicas...${NC}"

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
# 9. Verificar instalación
# ===============================================
echo -e "\n${YELLOW}==> Paso 9: Verificando instalación...${NC}"

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
# 10. Resumen
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
echo "  3. Para Módulos 5+, instala Docker"
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

