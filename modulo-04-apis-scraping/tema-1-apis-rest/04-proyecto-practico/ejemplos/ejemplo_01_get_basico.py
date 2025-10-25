"""
Ejemplo 1: GET Request Básico

Aprende a hacer un GET request simple a una API pública.
"""

import io
import sys
from pathlib import Path

# Configurar UTF-8 para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cliente_http import hacer_get
from src.validaciones import extraer_json_seguro


def ejemplo_get_usuarios():
    """
    Obtiene la lista de usuarios de JSONPlaceholder.

    JSONPlaceholder es una API REST gratuita para testing.
    """
    print("=" * 60)
    print("EJEMPLO 1: GET Request Básico")
    print("=" * 60)

    # URL de la API pública
    url = "https://jsonplaceholder.typicode.com/users"

    print(f"\n📡 Haciendo GET a: {url}")

    # Hacer request
    response = hacer_get(url)

    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Content-Type: {response.headers.get('Content-Type')}")

    # Extraer JSON de forma segura
    usuarios = extraer_json_seguro(response)

    print(f"\n📊 Total usuarios recibidos: {len(usuarios)}")
    print("\n👥 Primeros 3 usuarios:")

    for usuario in usuarios[:3]:
        print(f"  - ID: {usuario['id']}")
        print(f"    Nombre: {usuario['name']}")
        print(f"    Email: {usuario['email']}")
        print()


def ejemplo_get_usuario_especifico():
    """
    Obtiene un usuario específico por ID.
    """
    print("\n" + "=" * 60)
    print("GET Request con parámetro en URL")
    print("=" * 60)

    user_id = 1
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    print(f"\n📡 Obteniendo usuario {user_id}...")

    response = hacer_get(url)
    usuario = extraer_json_seguro(response)

    print(f"\n✅ Usuario encontrado:")
    print(f"  ID: {usuario['id']}")
    print(f"  Nombre: {usuario['name']}")
    print(f"  Username: {usuario['username']}")
    print(f"  Email: {usuario['email']}")
    print(f"  Ciudad: {usuario['address']['city']}")


def ejemplo_get_con_query_params():
    """
    Usa query parameters para filtrar resultados.
    """
    print("\n" + "=" * 60)
    print("GET Request con Query Parameters")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    # Filtrar posts de un usuario específico
    params = {"userId": 1}

    print(f"\n📡 Obteniendo posts del usuario {params['userId']}...")

    response = hacer_get(url, params=params)
    posts = extraer_json_seguro(response)

    print(f"\n✅ Posts encontrados: {len(posts)}")
    print("\n📝 Primeros 3 posts:")

    for post in posts[:3]:
        print(f"  - Post #{post['id']}: {post['title'][:50]}...")


if __name__ == "__main__":
    try:
        ejemplo_get_usuarios()
        ejemplo_get_usuario_especifico()
        ejemplo_get_con_query_params()

        print("\n" + "=" * 60)
        print("✅ ¡Todos los ejemplos ejecutados correctamente!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
