"""
Cliente API REST Robusto.

Biblioteca funcional para consumir APIs REST con reintentos automáticos,
paginación, caché y manejo robusto de errores.

Empresa ficticia: DataHub Inc.
"""

from src.autenticacion import (
    combinar_headers,
    crear_headers_api_key,
    crear_headers_basic_auth,
    crear_headers_bearer,
)
from src.cliente_http import hacer_delete, hacer_get, hacer_post, hacer_put
from src.paginacion import paginar_cursor, paginar_offset_limit
from src.reintentos import calcular_delay_exponencial, reintentar_con_backoff
from src.validaciones import (
    extraer_json_seguro,
    validar_contenido_json,
    validar_status_code,
    validar_timeout,
    validar_url,
)

__version__ = "1.0.0"
__all__ = [
    # Cliente HTTP
    "hacer_get",
    "hacer_post",
    "hacer_put",
    "hacer_delete",
    # Autenticación
    "crear_headers_api_key",
    "crear_headers_bearer",
    "crear_headers_basic_auth",
    "combinar_headers",
    # Reintentos
    "reintentar_con_backoff",
    "calcular_delay_exponencial",
    # Paginación
    "paginar_offset_limit",
    "paginar_cursor",
    # Validaciones
    "validar_url",
    "validar_timeout",
    "validar_status_code",
    "validar_contenido_json",
    "extraer_json_seguro",
]
