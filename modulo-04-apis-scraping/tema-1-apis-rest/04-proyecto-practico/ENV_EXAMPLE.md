# Variables de Entorno - Ejemplo

Este proyecto soporta configuración mediante variables de entorno para mayor seguridad.

## 📋 Crear archivo .env

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```bash
# APIs de Ejemplo (públicas)
JSONPLACEHOLDER_URL=https://jsonplaceholder.typicode.com
OPENWEATHER_API_KEY=tu-api-key-aqui
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
GITHUB_TOKEN=ghp_tu-token-aqui
GITHUB_API_URL=https://api.github.com

# Configuración General
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
DEFAULT_PAGE_SIZE=100
```

## 🔐 Usar en tu código

```python
from dotenv import load_dotenv
import os

# Cargar variables
load_dotenv()

# Usar variables
api_key = os.getenv("OPENWEATHER_API_KEY")
timeout = int(os.getenv("DEFAULT_TIMEOUT", 30))
```

## ⚠️  Seguridad

- ✅ El archivo `.env` ya está en `.gitignore`
- ✅ NUNCA subas `.env` a Git
- ✅ Usa valores diferentes para dev/staging/prod
- ✅ Rota las keys regularmente

## 📚 Obtener API Keys

### OpenWeatherMap (gratuita)
1. Ir a: https://openweathermap.org/api
2. Crear cuenta gratuita
3. Obtener API key

### GitHub Personal Access Token
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Seleccionar scopes necesarios
