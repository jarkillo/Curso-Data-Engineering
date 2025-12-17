# Cliente API REST Robusto

**Biblioteca funcional para consumir APIs REST con reintentos automáticos, paginación y manejo robusto de errores.**

Desarrollado como parte del **Módulo 4: APIs y Web Scraping** del Master en Data Engineering.

## 📋 Características

✅ **Validaciones exhaustivas** de URLs, timeouts y contenido JSON
✅ **Múltiples métodos de autenticación**: API Key, Bearer Token, Basic Auth
✅ **Cliente HTTP simple**: GET, POST, PUT, DELETE
✅ **Reintentos con exponential backoff** para errores temporales (5xx, 429)
✅ **Paginación automática**: Offset/Limit y Cursor-based
✅ **100% testeado** con 98 tests usando TDD
✅ **Type hints completos** para mejor autocompletado
✅ **Sin dependencias externas** excepto `requests`

## 🚀 Instalación

```bash
# Clonar o descargar el proyecto
cd 04-proyecto-practico

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso Rápido

### 1. GET Request Básico

```python
from src.cliente_http import hacer_get

response = hacer_get("https://jsonplaceholder.typicode.com/users/1")
print(response.json())
```

### 2. POST con Autenticación

```python
from src.cliente_http import hacer_post
from src.autenticacion import crear_headers_api_key

headers = crear_headers_api_key("tu-api-key-aqui")
data = {"title": "Nuevo post", "body": "Contenido"}

response = hacer_post(
    url="https://api.ejemplo.com/posts",
    json=data,
    headers=headers
)
```

### 3. Reintentos Automáticos

```python
from src.reintentos import reintentar_con_backoff

# Reintenta automáticamente ante errores 5xx y 429
response = reintentar_con_backoff(
    url="https://api.ejemplo.com/users",
    max_intentos=3
)
```

### 4. Paginación Automática (Offset/Limit)

```python
from src.paginacion import paginar_offset_limit

# Itera automáticamente todas las páginas
todos_usuarios = paginar_offset_limit(
    url="https://api.ejemplo.com/users",
    limite_por_pagina=100
)
print(f"Total usuarios: {len(todos_usuarios)}")
```

### 5. Paginación con Cursor

```python
from src.paginacion import paginar_cursor

todos_resultados = paginar_cursor(
    url="https://api.ejemplo.com/posts",
    campo_datos="data",
    campo_cursor="pagination.next_cursor"
)
```

## 📚 API Completa

### Módulo: `validaciones`

#### `validar_url(url: str) -> None`
Valida que una URL sea HTTPS y tenga formato correcto.

**Lanza:**
- `TypeError` si url no es string
- `ValueError` si url está vacía o no es HTTPS

#### `validar_timeout(timeout: int) -> None`
Valida que un timeout sea entero positivo.

#### `validar_status_code(response: Response, codigos_validos: Tuple[int, ...]) -> None`
Valida que el status code esté en los códigos válidos.

#### `validar_contenido_json(response: Response) -> None`
Valida que una respuesta contenga JSON válido.

#### `extraer_json_seguro(response: Response) -> dict | list`
Extrae JSON de forma segura con validaciones.

---

### Módulo: `autenticacion`

#### `crear_headers_api_key(api_key: str, header_name: str = "X-API-Key") -> Dict[str, str]`
Crea headers con API Key.

**Ejemplo:**
```python
headers = crear_headers_api_key("mi-key-123")
# {'X-API-Key': 'mi-key-123'}
```

#### `crear_headers_bearer(token: str) -> Dict[str, str]`
Crea headers con Bearer token (JWT).

**Ejemplo:**
```python
headers = crear_headers_bearer("eyJhbGc...")
# {'Authorization': 'Bearer eyJhbGc...'}
```

#### `crear_headers_basic_auth(username: str, password: str) -> Dict[str, str]`
Crea headers con Basic Authentication.

**Ejemplo:**
```python
headers = crear_headers_basic_auth("admin", "pass123")
# {'Authorization': 'Basic YWRtaW46cGFzczEyMw=='}
```

#### `combinar_headers(headers_base: Dict, headers_extra: Dict) -> Dict[str, str]`
Combina dos diccionarios de headers sin modificar originales.

---

### Módulo: `cliente_http`

#### `hacer_get(url: str, headers: Dict = None, params: Dict = None, timeout: int = 30) -> Response`
Hace GET request con validaciones.

#### `hacer_post(url: str, json: Dict = None, data: Dict = None, headers: Dict = None, timeout: int = 30) -> Response`
Hace POST request con validaciones.

#### `hacer_put(url: str, json: Dict = None, data: Dict = None, headers: Dict = None, timeout: int = 30) -> Response`
Hace PUT request con validaciones.

#### `hacer_delete(url: str, headers: Dict = None, timeout: int = 30) -> Response`
Hace DELETE request con validaciones.

---

### Módulo: `reintentos`

#### `calcular_delay_exponencial(intento: int, base: int = 2, max_delay: int = 60) -> int`
Calcula delay exponencial: `base^intento`, limitado por `max_delay`.

**Ejemplo:**
```python
calcular_delay_exponencial(1)  # 2 segundos
calcular_delay_exponencial(2)  # 4 segundos
calcular_delay_exponencial(3)  # 8 segundos
```

#### `reintentar_con_backoff(url: str, metodo: str = "GET", max_intentos: int = 3, ...) -> Response`
Hace request HTTP con reintentos automáticos usando exponential backoff.

**Reintenta ante:**
- Errores 5xx (500, 502, 503, 504)
- Error 429 (Rate Limit)

**NO reintenta ante:**
- Errores 4xx (400, 401, 403, 404...) - Son errores de cliente

**Ejemplo:**
```python
response = reintentar_con_backoff(
    url="https://api.ejemplo.com/users",
    metodo="GET",
    max_intentos=3
)
```

---

### Módulo: `paginacion`

#### `paginar_offset_limit(url: str, limite_por_pagina: int = 100, ...) -> List[Dict]`
Itera automáticamente todas las páginas usando Offset/Limit.

**Parámetros:**
- `url`: URL base del endpoint
- `limite_por_pagina`: Elementos por página
- `nombre_param_offset`: Nombre del parámetro offset (default: "offset")
- `nombre_param_limit`: Nombre del parámetro limit (default: "limit")
- `params_extra`: Parámetros adicionales
- `headers`: Headers HTTP
- `max_paginas`: Límite de páginas (None = sin límite)

**Ejemplo:**
```python
usuarios = paginar_offset_limit(
    url="https://api.ejemplo.com/users",
    limite_por_pagina=50,
    params_extra={"status": "active"}
)
```

#### `paginar_cursor(url: str, campo_datos: str, campo_cursor: str, ...) -> List[Dict]`
Itera automáticamente todas las páginas usando Cursor.

**Parámetros:**
- `url`: URL base
- `campo_datos`: Ruta al campo de datos (ej: "data", "results")
- `campo_cursor`: Ruta al cursor (ej: "next_cursor", "pagination.next")
- `nombre_param_cursor`: Nombre del parámetro (default: "cursor")
- `params_extra`: Parámetros adicionales
- `max_paginas`: Límite de páginas

**Ejemplo:**
```python
posts = paginar_cursor(
    url="https://api.ejemplo.com/posts",
    campo_datos="data",
    campo_cursor="pagination.next_cursor"
)
```

## 🧪 Tests

El proyecto sigue **TDD estricto**: tests escritos primero, implementación después.

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Solo un módulo
pytest tests/test_validaciones.py -v
```

**Cobertura actual: 98 tests, 100% de funciones cubiertas**

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── validaciones.py      # Validación de URLs, timeouts, JSON
│   ├── autenticacion.py     # API Key, Bearer, Basic Auth
│   ├── cliente_http.py      # GET, POST, PUT, DELETE
│   ├── reintentos.py        # Exponential backoff
│   └── paginacion.py        # Offset/Limit y Cursor
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_validaciones.py
│   ├── test_autenticacion.py
│   ├── test_cliente_http.py
│   ├── test_reintentos.py
│   └── test_paginacion.py
├── ejemplos/
│   ├── ejemplo_01_get_basico.py
│   ├── ejemplo_02_autenticacion.py
│   ├── ejemplo_03_reintentos.py
│   ├── ejemplo_04_paginacion_offset.py
│   └── ejemplo_05_paginacion_cursor.py
├── datos/                   # Datos temporales (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔒 Seguridad

Este proyecto sigue **principios de seguridad por defecto**:

✅ **Solo HTTPS**: Rechaza URLs HTTP automáticamente
✅ **Validación exhaustiva**: Todos los inputs son validados
✅ **Sin secretos en código**: Usa variables de entorno
✅ **Errores explícitos**: No hay errores silenciosos
✅ **Type hints**: Previene errores de tipos
✅ **Tests robustos**: 98 tests cubren casos extremos

### Variables de Entorno

Crea un archivo `.env`:

```bash
API_KEY=tu-api-key-aqui
BEARER_TOKEN=tu-token-jwt-aqui
API_BASE_URL=https://api.ejemplo.com
```

Luego cárgalas:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
```

## 🎓 Conceptos Aprendidos

Este proyecto enseña:

1. **Consumo de APIs REST**: GET, POST, PUT, DELETE
2. **Autenticación**: API Key, Bearer Token, Basic Auth
3. **Manejo de errores**: Status codes 2xx, 4xx, 5xx
4. **Reintentos inteligentes**: Exponential backoff
5. **Rate limiting**: Manejo de 429 Too Many Requests
6. **Paginación**: Offset/Limit y Cursor-based
7. **TDD**: Test-Driven Development estricto
8. **Type hints**: Python tipado para mejor código
9. **Código funcional**: Sin clases, solo funciones puras
10. **Arquitectura limpia**: Módulos separados por responsabilidad

## 📊 Métricas de Calidad

- **Tests**: 98 tests (100% funciones cubiertas)
- **Linting**: Compatible con `flake8` y `black`
- **Type hints**: 100% de funciones tipadas
- **Documentación**: Docstrings en todas las funciones
- **Complejidad**: Ciclo máximo < 10 (código simple)

## 🤝 Contribuir

Este es un proyecto educativo. Para mejoras:

1. Escribe el test primero (TDD)
2. Implementa la solución
3. Verifica que todos los tests pasen
4. Actualiza el README si añades funcionalidad

## 📝 Licencia

Proyecto educativo del Master en Data Engineering.
Empresa ficticia: **DataHub Inc.**

## 🆘 Soporte

Si encuentras errores o tienes dudas:

1. Revisa los ejemplos en `ejemplos/`
2. Lee los tests en `tests/` (son documentación ejecutable)
3. Consulta este README

---

**Desarrollado con ❤️ siguiendo TDD y principios de código limpio**
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Web Scraping - 01 Teoria](../../tema-2-web-scraping/01-TEORIA.md)
