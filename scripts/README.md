# 🛠️ Scripts de Setup - Master en Ingeniería de Datos

Este directorio contiene scripts automatizados para configurar el entorno de desarrollo del Master.

---

## 📋 Scripts Disponibles

### `setup_windows.ps1`
**Sistema**: Windows 10+ con PowerShell
**Duración**: 5-10 minutos

**Qué hace**:
- ✅ Verifica Python 3.11+ está instalado
- ✅ Verifica pip y Git
- ✅ Crea entorno virtual (`venv`)
- ✅ Instala dependencias básicas (pytest, black, flake8, mypy)
- ✅ Muestra recordatorios de seguridad

**Uso**:
```powershell
# Si aparece error de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar
.\scripts\setup_windows.ps1
```

---

### `setup_linux.sh`
**Sistema**: Linux (Ubuntu 20.04+, Debian, etc.)
**Duración**: 5-10 minutos

**Qué hace**:
- ✅ Verifica Python 3.11+ está instalado
- ✅ Verifica pip3 y Git
- ✅ Crea entorno virtual (`venv`)
- ✅ Instala dependencias básicas
- ✅ Muestra recordatorios de seguridad

**Uso**:
```bash
# Dar permisos
chmod +x scripts/setup_linux.sh

# Ejecutar
bash scripts/setup_linux.sh
```

---

### `setup_mac.sh`
**Sistema**: macOS 10.15+ (Intel o Apple Silicon)
**Duración**: 5-10 minutos

**Qué hace**:
- ✅ Verifica Homebrew (recomendado)
- ✅ Verifica Python 3.11+ está instalado
- ✅ Verifica pip3 y Git
- ✅ Crea entorno virtual (`venv`)
- ✅ Instala dependencias básicas
- ✅ Muestra recordatorios de seguridad
- ✅ Nota especial para Mac M1/M2

**Uso**:
```bash
# Dar permisos
chmod +x scripts/setup_mac.sh

# Ejecutar
bash scripts/setup_mac.sh
```

---

## ✅ Verificación Post-Setup

Después de ejecutar el script correspondiente:

```bash
# 1. Activar el entorno virtual
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# 2. Verificar instalaciones
python --version  # Debe ser 3.11+
pytest --version
black --version
flake8 --version

# 3. Ejecutar tests del Módulo 1
cd modulo-01-fundamentos/tema-1-python-estadistica/04-proyecto-practico
pytest tests/ -v
```

---

## 🐛 Troubleshooting

### Error: "python no reconocido" (Windows)
**Causa**: Python no está en el PATH

**Solución**:
1. Busca "Variables de entorno" en Windows
2. Edita "Path" en Variables del sistema
3. Añade las rutas de Python
4. Reinicia PowerShell

### Error: "Permission denied" (Linux/Mac)
**Causa**: El script no tiene permisos de ejecución

**Solución**:
```bash
chmod +x scripts/setup_*.sh
```

### Error: "pip not found"
**Causa**: pip no está instalado o no está en el PATH

**Solución**:
```bash
# Linux/Mac:
sudo apt install python3-pip  # Ubuntu/Debian
brew install python@3.11      # macOS

# Windows:
python -m ensurepip --upgrade
```

### Error: "venv creation failed"
**Causa**: Módulo venv no está instalado

**Solución**:
```bash
# Linux:
sudo apt install python3.11-venv

# Windows/Mac:
python -m pip install --upgrade pip setuptools
```

---

## 📦 Dependencias Instaladas por los Scripts

### Básicas (Todos los módulos)
- `pytest>=7.4.0`: Testing framework
- `pytest-cov>=4.1.0`: Code coverage
- `black>=23.7.0`: Code formatter
- `flake8>=6.1.0`: Linter
- `mypy>=1.5.0`: Type checker

### Adicionales
Para instalar todas las dependencias del Master:
```bash
pip install -r requirements.txt
```

---

## 🔒 Seguridad

Los scripts incluyen recordatorios de seguridad:

1. **No compartir credenciales** en repositorios públicos
2. **Usar variables de entorno** para secrets (archivo `.env`)
3. **Añadir `.env` al `.gitignore`**
4. **Usar contraseñas fuertes** (12+ caracteres, mixtas)
5. **Implementar límite de intentos fallidos**

---

## 🆘 Soporte

Si los scripts fallan:

1. Lee el mensaje de error completo
2. Consulta el [Troubleshooting](#-troubleshooting) de arriba
3. Consulta `documentacion/GUIA_INSTALACION.md` para setup manual
4. Busca el error en Google/Stack Overflow
5. Pregunta en el foro del curso

---

## 📝 Notas

- Los scripts son **idempotentes**: puedes ejecutarlos varias veces sin problemas
- Si ya existe `venv`, se eliminará y creará uno nuevo
- Los scripts **no modifican** tu sistema más allá del proyecto
- Puedes revisar el código de los scripts antes de ejecutarlos

---

*Última actualización: 2025-10-18*
