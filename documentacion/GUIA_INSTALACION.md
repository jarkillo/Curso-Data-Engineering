# 📖 Guía de Instalación - Master en Ingeniería de Datos

**Versión:** 1.0.0
**Última actualización:** 2025-10-18

---

## 📋 Tabla de Contenidos

1. [Prerrequisitos](#-prerrequisitos)
2. [Instalación de Python](#-instalación-de-python)
3. [Instalación de Git](#-instalación-de-git)
4. [Configuración del Proyecto](#-configuración-del-proyecto)
5. [Instalación de Docker](#-instalación-de-docker-módulos-5)
6. [Configuración de VS Code](#-configuración-de-vs-code-opcional)
7. [Verificación del Setup](#-verificación-del-setup)
8. [Troubleshooting](#-troubleshooting)
9. [Recursos Adicionales](#-recursos-adicionales)

---

## 🎯 Prerrequisitos

### Requisitos del Sistema

- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- **RAM**: Mínimo 8GB (16GB recomendado para Módulos 6+)
- **Disco**: 20GB libres mínimo
- **Conexión a Internet**: Necesaria para descargar dependencias

### Conocimientos Previos

- Conocimientos básicos de terminal/línea de comandos
- Familiaridad con editores de texto
- (Opcional) Conocimientos básicos de Git

---

## 🐍 Instalación de Python

Python 3.11+ es **obligatorio** para este Master.

### Windows

1. **Descargar Python**:
   - Ve a [python.org/downloads](https://www.python.org/downloads/)
   - Descarga Python 3.11 o superior (recomendado: 3.11.7)

2. **Ejecutar el Instalador**:
   - Ejecuta el archivo descargado
   - ⚠️ **IMPORTANTE**: Marca la casilla **"Add Python to PATH"**
   - Selecciona "Install Now"
   - Espera a que finalice la instalación

3. **Verificar la Instalación**:
   ```powershell
   python --version
   # Debe mostrar: Python 3.11.x

   pip --version
   # Debe mostrar la versión de pip
   ```

#### Solución de Problemas en Windows

- **Error "python no reconocido"**: Añade Python manualmente al PATH
  1. Busca "Variables de entorno" en el menú de inicio
  2. En "Variables del sistema", busca "Path"
  3. Añade: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311`
  4. Añade: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311\Scripts`
  5. Reinicia la terminal

### Linux (Ubuntu/Debian)

1. **Actualizar el Sistema**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Instalar Python 3.11**:
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip -y
   ```

3. **Verificar la Instalación**:
   ```bash
   python3 --version
   # Debe mostrar: Python 3.11.x

   pip3 --version
   ```

4. **Crear un Alias (Opcional)**:
   ```bash
   echo "alias python=python3" >> ~/.bashrc
   echo "alias pip=pip3" >> ~/.bashrc
   source ~/.bashrc
   ```

### macOS

#### Opción 1: Homebrew (Recomendado)

1. **Instalar Homebrew** (si no lo tienes):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Instalar Python**:
   ```bash
   brew install python@3.11
   ```

3. **Verificar la Instalación**:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Opción 2: Instalador Oficial

1. Descarga desde [python.org/downloads/macos](https://www.python.org/downloads/macos/)
2. Ejecuta el instalador `.pkg`
3. Sigue las instrucciones en pantalla

---

## 🔧 Instalación de Git

Git es necesario para clonar el repositorio y gestionar versiones.

### Windows

1. **Descargar Git**:
   - Ve a [git-scm.com/download/win](https://git-scm.com/download/win)
   - Descarga el instalador (64-bit recomendado)

2. **Ejecutar el Instalador**:
   - Ejecuta el archivo descargado
   - Configuración recomendada:
     - Editor: VS Code (si lo tienes instalado)
     - PATH: "Git from the command line and also from 3rd-party software"
     - Line endings: "Checkout Windows-style, commit Unix-style"
     - Terminal: "Use Windows' default console window"

3. **Verificar**:
   ```powershell
   git --version
   # Debe mostrar: git version 2.x.x
   ```

4. **Configurar Git**:
   ```powershell
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@email.com"
   ```

### Linux

```bash
sudo apt install git -y
git --version

# Configurar
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### macOS

```bash
# Con Homebrew
brew install git

# O usar el que viene con Xcode Command Line Tools
xcode-select --install

# Verificar
git --version

# Configurar
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## 🚀 Configuración del Proyecto

### 1. Clonar el Repositorio

```bash
# Navega al directorio donde quieres el proyecto
cd ~/Documentos  # o la carpeta que prefieras

# Clona el repositorio
git clone <URL_DEL_REPOSITORIO>

# Entra al directorio
cd "Curso Data Engineering"
```

### 2. Ejecutar Script de Setup

El proyecto incluye scripts automatizados para configurar el entorno.

#### Windows

```powershell
# Ejecutar script
.\scripts\setup_windows.ps1

# Si aparece error de ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Volver a ejecutar
.\scripts\setup_windows.ps1
```

#### Linux

```bash
# Dar permisos de ejecución
chmod +x scripts/setup_linux.sh

# Ejecutar script
bash scripts/setup_linux.sh
```

#### macOS

```bash
# Dar permisos de ejecución
chmod +x scripts/setup_mac.sh

# Ejecutar script
bash scripts/setup_mac.sh
```

### 3. Activar Entorno Virtual

Después de ejecutar el script de setup, activa el entorno virtual:

#### Windows

```powershell
.\venv\Scripts\Activate.ps1

# Tu prompt debe cambiar a mostrar (venv) al inicio
```

#### Linux/macOS

```bash
source venv/bin/activate

# Tu prompt debe cambiar a mostrar (venv) al inicio
```

### 4. Instalar Dependencias Adicionales

Para instalar todas las dependencias del Master:

```bash
pip install -r requirements.txt
```

**Nota**: Esto puede tardar varios minutos dependiendo de tu conexión.

---

## 🐳 Instalación de Docker (Módulos 5+)

Docker es necesario para los Módulos 5 en adelante (Bases de Datos, Airflow, Spark).

### Windows

1. **Descargar Docker Desktop**:
   - Ve a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Descarga Docker Desktop para Windows

2. **Requisitos**:
   - Windows 10 64-bit: Pro, Enterprise o Education (Build 16299 o superior)
   - WSL 2 habilitado (el instalador lo habilita automáticamente)
   - Virtualización habilitada en BIOS

3. **Instalar**:
   - Ejecuta el instalador
   - Reinicia el PC cuando se solicite
   - Abre Docker Desktop

4. **Verificar**:
   ```powershell
   docker --version
   docker-compose --version
   ```

5. **Iniciar Servicios**:
   ```powershell
   docker-compose up -d
   ```

### Linux

1. **Instalar Docker**:
   ```bash
   # Actualizar repositorios
   sudo apt update

   # Instalar dependencias
   sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

   # Añadir repositorio de Docker
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   # Instalar Docker
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

   # Añadir tu usuario al grupo docker
   sudo usermod -aG docker $USER

   # Cerrar sesión y volver a entrar para aplicar cambios
   ```

2. **Verificar**:
   ```bash
   docker --version
   docker compose version
   ```

3. **Iniciar Servicios**:
   ```bash
   docker compose up -d
   ```

### macOS

1. **Descargar Docker Desktop**:
   - Ve a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Descarga Docker Desktop para Mac (Intel o Apple Silicon)

2. **Instalar**:
   - Abre el archivo `.dmg`
   - Arrastra Docker a Aplicaciones
   - Abre Docker desde Aplicaciones
   - Acepta los permisos necesarios

3. **Verificar**:
   ```bash
   docker --version
   docker compose version
   ```

4. **Iniciar Servicios**:
   ```bash
   docker compose up -d
   ```

### Servicios Disponibles en Docker

El archivo `docker-compose.yml` incluye:

- **PostgreSQL** (puerto 5432): Base de datos relacional
- **MongoDB** (puerto 27017): Base de datos NoSQL
- **Apache Airflow** (puerto 8080): Orquestación de pipelines
- **Redis** (puerto 6379): Cache

#### Credenciales por Defecto

⚠️ **IMPORTANTE**: Estas son credenciales de desarrollo. **Cámbialas en producción**.

**PostgreSQL**:
- Usuario: `dataeng_user`
- Contraseña: `DataEng2025!SecurePass`
- Base de datos: `dataeng_db`

**MongoDB**:
- Usuario: `admin`
- Contraseña: `MongoAdmin2025!SecurePass`

**Airflow Web**:
- URL: http://localhost:8080
- Usuario: `admin`
- Contraseña: `Airflow2025!Admin`

---

## 💻 Configuración de VS Code (Opcional)

VS Code es el editor recomendado para este Master.

### Instalación

1. Descarga desde [code.visualstudio.com](https://code.visualstudio.com/)
2. Instala en tu sistema
3. Abre VS Code

### Extensiones Recomendadas

Instala las siguientes extensiones:

1. **Python** (Microsoft)
2. **Pylance** (Microsoft)
3. **Jupyter** (Microsoft)
4. **GitLens** (GitKraken)
5. **Docker** (Microsoft)
6. **Better Comments** (Aaron Bond)
7. **autoDocstring** (Nils Werner)
8. **Path Intellisense** (Christian Kohler)

### Configuración Automática

El proyecto incluye configuración de VS Code en `.vscode/settings.json`:

- Formateo automático con Black al guardar
- Linting con flake8 habilitado
- Type checking con mypy
- Tests con pytest

### Abrir el Proyecto

```bash
# Desde la terminal, en el directorio del proyecto
code .
```

---

## ✅ Verificación del Setup

### 1. Verificar Python y Pip

```bash
python --version  # Debe ser 3.11+
pip --version
```

### 2. Verificar Entorno Virtual

```bash
# Debe estar activado (venv) en el prompt
which python  # Linux/Mac
where python  # Windows

# Debe apuntar a venv/bin/python o venv\Scripts\python.exe
```

### 3. Ejecutar Tests

```bash
# Activar entorno si no está activado
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

# Ejecutar tests del Módulo 1
cd modulo-01-fundamentos/tema-1-python-estadistica/04-proyecto-practico
pytest tests/ -v
```

Si todos los tests pasan ✅, tu setup está correcto.

### 4. Verificar Code Quality

```bash
# Verificar formato con Black
black --check src/

# Verificar linting con flake8
flake8 src/

# Verificar tipos con mypy
mypy src/
```

### 5. Verificar Docker (si instalado)

```bash
# Verificar que Docker está corriendo
docker ps

# Iniciar servicios
docker compose up -d

# Verificar que los servicios están corriendo
docker compose ps

# Debe mostrar postgres, mongodb, airflow, etc. en estado "running"
```

---

## 🔧 Troubleshooting

### Problema: "python no reconocido" (Windows)

**Solución 1**: Añadir Python al PATH manualmente
1. Busca "Variables de entorno" en el menú de inicio
2. Edita "Path" en Variables del sistema
3. Añade las rutas de Python y Scripts
4. Reinicia la terminal

**Solución 2**: Reinstalar Python marcando "Add to PATH"

### Problema: "pip no encuentra paquetes"

**Solución**:
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Limpiar caché
pip cache purge

# Reinstalar
pip install -r requirements.txt
```

### Problema: Error al crear entorno virtual

**Solución**:
```bash
# Instalar/actualizar virtualenv
pip install --upgrade virtualenv

# Crear entorno manualmente
python -m venv venv --clear
```

### Problema: Docker no inicia

**Solución Windows**:
1. Verificar que WSL 2 está instalado
2. Habilitar virtualización en BIOS
3. Reiniciar Docker Desktop

**Solución Linux**:
```bash
# Verificar que el servicio está corriendo
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker

# Habilitar inicio automático
sudo systemctl enable docker
```

### Problema: Tests fallan

**Solución**:
```bash
# Verificar que estás en el directorio correcto
pwd  # Linux/Mac
cd  # Windows

# Verificar que el entorno virtual está activado
# Debe mostrar (venv) en el prompt

# Reinstalar dependencias de testing
pip install pytest pytest-cov pytest-mock

# Ejecutar tests con más información
pytest -vv
```

### Problema: Permission denied en scripts (Linux/Mac)

**Solución**:
```bash
# Dar permisos de ejecución
chmod +x scripts/setup_linux.sh
chmod +x scripts/setup_mac.sh

# Ejecutar
bash scripts/setup_linux.sh
```

### Problema: Ports ya en uso (Docker)

**Solución**:
```bash
# Ver qué está usando el puerto
# Linux/Mac:
lsof -i :5432  # PostgreSQL
lsof -i :27017  # MongoDB
lsof -i :8080  # Airflow

# Windows:
netstat -ano | findstr :5432

# Detener servicios locales de PostgreSQL/MongoDB
# o cambiar los puertos en docker-compose.yml
```

### Problema: Mac M1/M2 - Errores de compatibilidad

**Solución**:
```bash
# Instalar con arquitectura específica
arch -arm64 brew install python@3.11

# Para paquetes problemáticos, usar Rosetta
arch -x86_64 pip install [paquete]
```

---

## 🔒 Mejoras de Seguridad

### 1. Usar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
POSTGRES_USER=dataeng_user
POSTGRES_PASSWORD=TuContraseñaSegura123!
POSTGRES_DB=dataeng_db

MONGO_USER=admin
MONGO_PASSWORD=OtraContraseñaSegura456!

AIRFLOW_USER=admin
AIRFLOW_PASSWORD=AirflowSeguro789!
```

Añade `.env` al `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 2. Contraseñas Fuertes

Las contraseñas deben tener:
- Mínimo 12 caracteres
- Letras mayúsculas y minúsculas
- Números
- Símbolos especiales
- No palabras del diccionario

### 3. Límite de Intentos Fallidos

Para producción, configura:
- Bloqueo temporal después de 3-5 intentos fallidos
- Monitoreo de accesos sospechosos
- Autenticación de dos factores (2FA)

### 4. Actualizar Dependencias Regularmente

```bash
# Verificar paquetes desactualizados
pip list --outdated

# Actualizar un paquete
pip install --upgrade [paquete]

# Auditoría de seguridad
pip install safety
safety check
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Python Docs](https://docs.python.org/3/)
- [Docker Docs](https://docs.docker.com/)
- [Git Docs](https://git-scm.com/doc)
- [VS Code Docs](https://code.visualstudio.com/docs)

### Tutoriales

- [Real Python](https://realpython.com/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Docker Getting Started](https://docs.docker.com/get-started/)

### Comunidad

- [Python Discord](https://discord.gg/python)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [GitHub Discussions](https://github.com/discussions)

---

## 📞 Soporte

Si tienes problemas no resueltos en esta guía:

1. Revisa los logs de error completos
2. Busca el error en Google/Stack Overflow
3. Consulta la documentación oficial
4. Pregunta en el foro del curso
5. Contacta al instructor

---

## ✅ Checklist de Instalación

Marca cuando completes cada paso:

- [ ] Python 3.11+ instalado
- [ ] pip actualizado
- [ ] Git instalado y configurado
- [ ] Repositorio clonado
- [ ] Script de setup ejecutado correctamente
- [ ] Entorno virtual creado y activado
- [ ] Dependencias básicas instaladas
- [ ] Tests del Módulo 1 ejecutados exitosamente
- [ ] Black y flake8 funcionan
- [ ] VS Code instalado y configurado (opcional)
- [ ] Docker instalado (para Módulos 5+)
- [ ] Servicios Docker funcionando (para Módulos 5+)

---

**¡Felicidades! 🎉 Estás listo para empezar el Master en Ingeniería de Datos.**

---

*Última actualización: 2025-10-18*
*Versión: 1.0.0*

