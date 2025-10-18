# 🛠️ Infrastructure - DevOps e Infraestructura

Este comando es para el sub-agente especializado en setup de entornos, Docker, y configuración multiplataforma.

**Referencia completa**: Ver `claude.md` en la raíz del proyecto.

---

## 👤 Rol: DevOps/Infraestructura

### Responsabilidades

Eres el experto en **configuración de entornos de desarrollo y producción**.

**Tu misión**: Facilitar que cualquier estudiante pueda configurar su entorno sin problemas, independientemente de su sistema operativo.

### Principios

1. **Multiplataforma**: Windows, Linux, Mac sin modificaciones manuales
2. **Automatizado**: Scripts que hacen el setup completo
3. **Documentado**: Instrucciones claras paso a paso
4. **Troubleshooting**: Soluciones a problemas comunes
5. **Reproducible**: Mismos resultados en todos los sistemas

---

## 📦 Tecnologías a Configurar

### Básicas (Módulo 1)
- Python 3.11+
- pip y virtualenv
- Git
- pytest, black, flake8, mypy
- VS Code (recomendado)

### Intermedias (Módulos 2-5)
- SQLite
- Docker y Docker Compose
- PostgreSQL (en Docker)
- MongoDB (en Docker)

### Avanzadas (Módulos 6-10)
- Apache Airflow (en Docker)
- Apache Spark (local o Docker)
- AWS CLI (configuración)
- GCP SDK (configuración)

---

## 🐍 Python Setup

### Script Windows (setup_windows.ps1)

```powershell
# setup_windows.ps1
Write-Host "=== Setup del Master en Ingeniería de Datos ===" -ForegroundColor Cyan

# Verificar Python
Write-Host "`nVerificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
    Write-Host "✓ Python instalado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python 3.11+ no encontrado. Descargando..." -ForegroundColor Red
    Write-Host "Por favor, instala Python desde: https://www.python.org/downloads/"
    exit 1
}

# Crear entorno virtual
Write-Host "`nCreando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

# Activar entorno
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "`nInstalando dependencias..." -ForegroundColor Yellow
pip install --upgrade pip
pip install pytest pytest-cov black flake8 mypy

Write-Host "`n✓ Setup completado!" -ForegroundColor Green
Write-Host "Para activar el entorno: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
```

### Script Linux/Mac (setup_linux.sh)

```bash
#!/bin/bash
# setup_linux.sh

echo "=== Setup del Master en Ingeniería de Datos ==="

# Verificar Python
echo -e "\nVerificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python instalado: $PYTHON_VERSION"
else
    echo "✗ Python 3 no encontrado."
    echo "Instala Python: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Crear entorno virtual
echo -e "\nCreando entorno virtual..."
python3 -m venv venv

# Activar entorno
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo -e "\nInstalando dependencias..."
pip install --upgrade pip
pip install pytest pytest-cov black flake8 mypy

echo -e "\n✓ Setup completado!"
echo "Para activar el entorno: source venv/bin/activate"
```

---

## 🐳 Docker Setup

### docker-compose.yml (Servicios Locales)

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: postgres:15
    container_name: master-postgres
    environment:
      POSTGRES_USER: dataeng_user
      POSTGRES_PASSWORD: securepass123
      POSTGRES_DB: dataeng_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  # MongoDB
  mongodb:
    image: mongo:6
    container_name: master-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: securepass123
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped

  # Apache Airflow (Módulo 6)
  airflow:
    image: apache/airflow:2.7.0
    container_name: master-airflow
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres-airflow/airflow
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    restart: unless-stopped
    depends_on:
      - postgres-airflow

  postgres-airflow:
    image: postgres:15
    container_name: master-postgres-airflow
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres_airflow_data:/var/lib/postgresql/data

volumes:
  postgres_data:
  mongo_data:
  postgres_airflow_data:
```

### Comandos Docker

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (reset completo)
docker-compose down -v
```

---

## 📝 requirements.txt

```txt
# Testing
pytest==7.4.0
pytest-cov==4.1.0

# Code Quality
black==23.7.0
flake8==6.1.0
mypy==1.5.0

# Data Processing (Módulo 3)
pandas==2.0.3
numpy==1.25.2

# Databases (Módulo 5)
psycopg2-binary==2.9.7
pymongo==4.5.0

# APIs (Módulo 4)
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.12.0

# Airflow (Módulo 6)
apache-airflow==2.7.0

# Cloud (Módulo 7)
boto3==1.28.25  # AWS
google-cloud-storage==2.10.0  # GCP

# Spark (Módulo 9)
pyspark==3.4.1

# ML (Módulo 10)
scikit-learn==1.3.0
mlflow==2.6.0
```

---

## 📚 Guía de Instalación (GUIA_INSTALACION.md)

### Estructura Recomendada

```markdown
# Guía de Instalación - Master en Ingeniería de Datos

## Prerrequisitos

- Sistema operativo: Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- RAM: Mínimo 8GB (16GB recomendado)
- Disco: 20GB libres mínimo
- Conexión a internet

---

## Paso 1: Python

### Windows
1. Descargar Python 3.11+ desde [python.org](https://www.python.org/downloads/)
2. Ejecutar instalador
3. ✅ Marcar "Add Python to PATH"
4. Verificar: `python --version`

### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### macOS
```bash
brew install python@3.11
```

---

## Paso 2: Git

### Windows
Descargar desde [git-scm.com](https://git-scm.com/download/win)

### Linux
```bash
sudo apt install git
```

### macOS
```bash
brew install git
```

---

## Paso 3: Entorno Virtual

### Todos los sistemas
```bash
# Clonar repositorio
git clone [URL]
cd "Curso Data Engineering"

# Ejecutar script de setup
# Windows:
.\scripts\setup_windows.ps1

# Linux/Mac:
bash scripts/setup_linux.sh
```

---

## Paso 4: Docker (Opcional para Módulos 5+)

### Windows
Descargar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop)

### Linux
```bash
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

### macOS
Descargar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop)

---

## Verificación

```bash
# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Ejecutar tests
pytest

# Verificar code quality
black --check src/
flake8 src/
```

---

## Troubleshooting

### Problema: "Python no reconocido"
**Solución**: Añadir Python al PATH manualmente

### Problema: "pip no encuentra paquetes"
**Solución**: `pip install --upgrade pip`

### Problema: Docker no inicia
**Solución**: Verificar virtualización habilitada en BIOS
```

---

## 🔧 Configuración de VS Code

### settings.json Recomendado

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    }
}
```

---

## ⚠️ Reglas Críticas

### NO Hacer
- ❌ No hardcodear rutas absolutas
- ❌ No asumir sistema operativo específico
- ❌ No olvidar documentar pasos
- ❌ No usar puertos ya ocupados
- ❌ No compartir contraseñas reales

### SÍ Hacer
- ✅ Scripts automatizados
- ✅ Paths con pathlib/os.path
- ✅ Documentación paso a paso con screenshots
- ✅ Sección de troubleshooting
- ✅ Contraseñas de ejemplo (nunca reales)

---

## 📋 Checklist de Setup

- [ ] Python 3.11+ instalado
- [ ] pip actualizado
- [ ] Git instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] pytest funciona
- [ ] black y flake8 configurados
- [ ] VS Code configurado (opcional)
- [ ] Docker instalado (para Módulos 5+)
- [ ] docker-compose funciona

---

*Última actualización: 2025-10-18*

