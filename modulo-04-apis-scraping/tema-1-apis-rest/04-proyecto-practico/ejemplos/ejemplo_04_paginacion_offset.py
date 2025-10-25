"""
Ejemplo 4: Paginación Offset/Limit

Aprende a iterar automáticamente todas las páginas de una API.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cliente_http import hacer_get
from src.paginacion import paginar_offset_limit
from src.validaciones import extraer_json_seguro


def ejemplo_paginacion_manual():
    """
    Primero: entiende cómo funciona la paginación manualmente.
    """
    print("=" * 60)
    print("EJEMPLO 4A: Paginación Manual (Entendiendo el Concepto)")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    print("\n📖 Conceptos:")
    print("  - offset: cuántos elementos saltar")
    print("  - limit: cuántos elementos traer")
    print()

    # Página 1: Primeros 5 posts
    print("📄 Página 1 (offset=0, limit=5):")
    response = hacer_get(url, params={"_start": 0, "_limit": 5})
    posts_pagina1 = extraer_json_seguro(response)
    for post in posts_pagina1:
        print(f"  - Post #{post['id']}: {post['title'][:40]}...")

    # Página 2: Siguientes 5 posts
    print("\n📄 Página 2 (offset=5, limit=5):")
    response = hacer_get(url, params={"_start": 5, "_limit": 5})
    posts_pagina2 = extraer_json_seguro(response)
    for post in posts_pagina2:
        print(f"  - Post #{post['id']}: {post['title'][:40]}...")

    print(f"\n💡 Total manual: {len(posts_pagina1) + len(posts_pagina2)} posts")
    print("   Problema: ¿Y si hay 100 páginas? ¡Tedioso!")


def ejemplo_paginacion_automatica():
    """
    Ahora: usa paginación automática.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4B: Paginación Automática")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    print(f"\n📡 Obteniendo TODOS los posts automáticamente...")
    print(f"  (paginando de 20 en 20)")

    # ¡Una sola línea para obtener TODO!
    todos_posts = paginar_offset_limit(
        url=url,
        limite_por_pagina=20,
        nombre_param_offset="_start",
        nombre_param_limit="_limit",
    )

    print(f"\n✅ Total obtenido: {len(todos_posts)} posts")
    print("\n📝 Primeros 5:")
    for post in todos_posts[:5]:
        print(f"  - Post #{post['id']}: {post['title'][:40]}...")

    print("\n📝 Últimos 5:")
    for post in todos_posts[-5:]:
        print(f"  - Post #{post['id']}: {post['title'][:40]}...")


def ejemplo_paginacion_con_filtros():
    """
    Paginación + filtros adicionales.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4C: Paginación con Filtros")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/comments"

    print(f"\n📡 Obteniendo comentarios del post 1...")

    # Paginar + filtrar por postId
    comentarios = paginar_offset_limit(
        url=url,
        limite_por_pagina=10,
        params_extra={"postId": 1},  # ← Filtro adicional
        nombre_param_offset="_start",
        nombre_param_limit="_limit",
    )

    print(f"\n✅ Comentarios del post 1: {len(comentarios)}")
    for comentario in comentarios[:3]:
        print(f"\n  Comentario #{comentario['id']}:")
        print(f"    De: {comentario['name']}")
        print(f"    Email: {comentario['email']}")


def ejemplo_paginacion_limitada():
    """
    Limitar el número de páginas.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4D: Limitar Número de Páginas")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    print(f"\n📡 Obteniendo solo 2 páginas (máximo)...")

    posts_limitados = paginar_offset_limit(
        url=url,
        limite_por_pagina=10,
        max_paginas=2,  # ← Solo 2 páginas
        nombre_param_offset="_start",
        nombre_param_limit="_limit",
    )

    print(f"\n✅ Posts obtenidos: {len(posts_limitados)}")
    print("   (10 posts/página × 2 páginas = 20 posts)")

    print("\n💡 ¿Cuándo usar max_paginas?")
    print("  - APIs muy grandes (millones de registros)")
    print("  - Solo necesitas una muestra")
    print("  - Limitar tiempo de ejecución")
    print("  - Testing rápido")


def ejemplo_apis_reales():
    """
    Ejemplos de paginación en APIs reales.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4E: APIs Reales con Offset/Limit")
    print("=" * 60)

    print("\n🌐 Ejemplos de APIs que usan Offset/Limit:")
    print()

    print("1️⃣  PostgreSQL/MySQL:")
    print("   SELECT * FROM users LIMIT 10 OFFSET 20")
    print("   → API: GET /users?limit=10&offset=20")
    print()

    print("2️⃣  GitHub (algunos endpoints):")
    print("   GET /repos?per_page=30&page=2")
    print("   → page * per_page = offset")
    print()

    print("3️⃣  Spotify:")
    print("   GET /playlists?limit=20&offset=40")
    print()

    print("4️⃣  OpenWeatherMap:")
    print("   GET /data?limit=50&offset=100")

    print("\n📊 Ventajas de Offset/Limit:")
    print("  ✅ Simple de entender")
    print("  ✅ Puedes saltar a cualquier página")
    print("  ✅ Compatible con SQL directamente")

    print("\n⚠️  Desventajas:")
    print("  ❌ Problemas con datos cambiantes (items nuevos/eliminados)")
    print("  ❌ Menos eficiente con offsets grandes")
    print("  ❌ No funciona bien con datos en tiempo real")

    print("\n💡 Para esos casos → usa paginación con cursor")


if __name__ == "__main__":
    try:
        ejemplo_paginacion_manual()
        ejemplo_paginacion_automatica()
        ejemplo_paginacion_con_filtros()
        ejemplo_paginacion_limitada()
        ejemplo_apis_reales()

        print("\n" + "=" * 60)
        print("✅ ¡Todos los ejemplos ejecutados correctamente!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
