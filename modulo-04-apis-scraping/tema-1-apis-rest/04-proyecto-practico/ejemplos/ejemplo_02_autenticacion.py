"""
Ejemplo 2: Autenticación en APIs REST

Aprende diferentes métodos de autenticación.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.autenticacion import (
    combinar_headers,
    crear_headers_api_key,
    crear_headers_basic_auth,
    crear_headers_bearer,
)


def ejemplo_api_key():
    """
    Autenticación con API Key.

    Común en APIs públicas (OpenWeatherMap, NewsAPI, etc.)
    """
    print("=" * 60)
    print("EJEMPLO 2A: Autenticación con API Key")
    print("=" * 60)

    api_key = "tu-api-key-aqui-12345"

    # Header default: X-API-Key
    headers = crear_headers_api_key(api_key)
    print(f"\n✅ Headers con API Key (default):")
    for key, value in headers.items():
        print(f"  {key}: {value}")

    # Header personalizado
    headers_custom = crear_headers_api_key(api_key, header_name="Authorization")
    print(f"\n✅ Headers con API Key (personalizado):")
    for key, value in headers_custom.items():
        print(f"  {key}: {value}")

    print("\n💡 Uso típico:")
    print("  import requests")
    print("  response = requests.get(url, headers=headers)")


def ejemplo_bearer_token():
    """
    Autenticación con Bearer Token (JWT).

    Común en APIs modernas que usan OAuth 2.0.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2B: Autenticación con Bearer Token")
    print("=" * 60)

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ejemplo.token"

    headers = crear_headers_bearer(token)
    print(f"\n✅ Headers con Bearer Token:")
    for key, value in headers.items():
        print(f"  {key}: {value[:50]}...")

    print("\n💡 Uso típico:")
    print("  1. Login: POST /auth/login → recibe token")
    print("  2. Usar token: GET /api/recursos (con headers)")
    print("  3. Token expira → repetir login")


def ejemplo_basic_auth():
    """
    Autenticación Basic (usuario:contraseña en base64).

    NOTA: Solo usar con HTTPS (nunca HTTP).
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2C: Autenticación Basic")
    print("=" * 60)

    username = "admin"
    password = "secreto123"

    headers = crear_headers_basic_auth(username, password)
    print(f"\n✅ Headers con Basic Auth:")
    for key, value in headers.items():
        print(f"  {key}: {value}")

    print("\n⚠️  IMPORTANTE:")
    print("  - Basic Auth envía credenciales en CADA request")
    print("  - Solo usar con HTTPS (este cliente lo valida)")
    print("  - Preferir Bearer Token para APIs modernas")


def ejemplo_combinar_headers():
    """
    Combina headers de autenticación con otros headers.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2D: Combinar Headers")
    print("=" * 60)

    # Headers de autenticación
    auth_headers = crear_headers_api_key("mi-api-key-123")

    # Headers adicionales
    extra_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "MiApp/1.0",
    }

    # Combinar
    headers_completos = combinar_headers(auth_headers, extra_headers)

    print(f"\n✅ Headers combinados:")
    for key, value in headers_completos.items():
        print(f"  {key}: {value}")

    print("\n💡 Útil cuando necesitas:")
    print("  - Autenticación + Content-Type")
    print("  - API Key + User-Agent personalizado")
    print("  - Bearer Token + Accept headers")


def ejemplo_seguridad_variables_entorno():
    """
    Buenas prácticas: usar variables de entorno.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2E: Seguridad - Variables de Entorno")
    print("=" * 60)

    print("\n🔒 ¡NUNCA hagas esto!")
    print("  ❌ api_key = 'mi-key-secreta-123'")
    print("  ❌ password = 'admin123'")
    print("  ❌ token = 'eyJhbGc....'")

    print("\n✅ Hacer esto en su lugar:")
    print("\n  1. Crear archivo .env:")
    print("     API_KEY=tu-key-aqui")
    print("     BEARER_TOKEN=tu-token-aqui")
    print()
    print("  2. En tu código:")
    print("     from dotenv import load_dotenv")
    print("     import os")
    print()
    print("     load_dotenv()")
    print("     api_key = os.getenv('API_KEY')")
    print("     headers = crear_headers_api_key(api_key)")

    print("\n💡 Beneficios:")
    print("  - No expones secretos en Git")
    print("  - Diferentes keys para dev/prod")
    print("  - Más seguro y profesional")


if __name__ == "__main__":
    try:
        ejemplo_api_key()
        ejemplo_bearer_token()
        ejemplo_basic_auth()
        ejemplo_combinar_headers()
        ejemplo_seguridad_variables_entorno()

        print("\n" + "=" * 60)
        print("✅ ¡Todos los ejemplos ejecutados correctamente!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
