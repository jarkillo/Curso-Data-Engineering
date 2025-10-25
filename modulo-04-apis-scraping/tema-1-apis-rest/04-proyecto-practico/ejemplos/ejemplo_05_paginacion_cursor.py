"""
Ejemplo 5: Paginación con Cursor

Aprende paginación basada en cursor (más robusta para datos dinámicos).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def ejemplo_concepto_cursor():
    """
    Entiende qué es un cursor y por qué existe.
    """
    print("=" * 60)
    print("EJEMPLO 5A: ¿Qué es un Cursor?")
    print("=" * 60)

    print("\n📖 Concepto:")
    print("  Un cursor es un 'marcador' que indica dónde estás")
    print("  en un conjunto de resultados.")
    print()

    print("🔄 Flujo típico:")
    print("  1. Primera request → recibes datos + cursor")
    print("  2. Segunda request con cursor → más datos + nuevo cursor")
    print("  3. Repetir hasta cursor = null")
    print()

    print("📦 Estructura de respuesta típica:")
    print("  {")
    print('    "data": [')
    print('      {"id": 1, "name": "Item 1"},')
    print('      {"id": 2, "name": "Item 2"}')
    print("    ],")
    print('    "pagination": {')
    print('      "next_cursor": "eyJpZCI6Mn0=",')
    print('      "has_more": true')
    print("    }")
    print("  }")

    print("\n💡 El cursor es opaco:")
    print("  - No intentes leerlo o modificarlo")
    print("  - Solo pásalo a la siguiente request")
    print("  - La API decide su formato (base64, hash, etc.)")


def ejemplo_offset_vs_cursor():
    """
    Compara Offset/Limit vs Cursor.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5B: Offset/Limit vs Cursor")
    print("=" * 60)

    print("\n🎯 Escenario: API de tweets en tiempo real")
    print()

    print("❌ Problema con Offset/Limit:")
    print("  1. Request 1: GET /tweets?offset=0&limit=10")
    print("     → Recibes tweets 1-10")
    print()
    print("  2. ⏰ Mientras tanto: 5 tweets nuevos se publican")
    print()
    print("  3. Request 2: GET /tweets?offset=10&limit=10")
    print("     → ¡Recibes duplicados! (tweets 6-10 otra vez)")
    print()

    print("✅ Solución con Cursor:")
    print("  1. Request 1: GET /tweets")
    print("     → Recibes tweets + cursor='abc123'")
    print()
    print("  2. ⏰ Nuevos tweets se publican")
    print()
    print("  3. Request 2: GET /tweets?cursor=abc123")
    print("     → Recibes siguientes tweets (sin duplicados)")
    print("     El cursor 'recuerda' dónde quedaste")

    print("\n📊 Comparación:")
    print()
    print("  OFFSET/LIMIT          |  CURSOR")
    print("  -------------------- | --------------------")
    print("  ✅ Simple            | ✅ Sin duplicados")
    print("  ✅ Saltar a página N | ✅ Datos dinámicos")
    print("  ❌ Duplicados        | ✅ Más eficiente")
    print("  ❌ Menos eficiente   | ❌ No saltar páginas")


def ejemplo_apis_cursor():
    """
    Ejemplos de APIs reales que usan cursor.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5C: APIs Reales con Cursor")
    print("=" * 60)

    print("\n🌐 APIs que usan paginación por cursor:")
    print()

    print("1️⃣  Twitter API v2:")
    print("   GET /tweets?max_results=10")
    print("   Response: { data: [...], meta: { next_token: 'xyz' } }")
    print("   Next: GET /tweets?max_results=10&pagination_token=xyz")
    print()

    print("2️⃣  GitHub GraphQL API:")
    print("   { users(first: 10) { edges { cursor, node } } }")
    print("   Cursor en cada elemento")
    print()

    print("3️⃣  Slack API:")
    print("   GET /conversations.history")
    print("   Response: { messages: [...], response_metadata: {")
    print("              next_cursor: 'dXNlcj...' } }")
    print()

    print("4️⃣  Stripe API:")
    print("   GET /charges?limit=10")
    print("   Response: { data: [...], has_more: true,")
    print("              starting_after: 'ch_123' }")


def ejemplo_uso_cursor():
    """
    Ejemplo conceptual de uso de cursor.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5D: Uso de paginar_cursor()")
    print("=" * 60)

    print("\n💻 Código ejemplo:")
    print()
    print("  from src.paginacion import paginar_cursor")
    print()
    print("  # API hipotética con cursor")
    print("  resultados = paginar_cursor(")
    print('      url="https://api.ejemplo.com/posts",')
    print('      campo_datos="data",           # Dónde están los datos')
    print('      campo_cursor="pagination.next_cursor"  # Dónde está el cursor')
    print("  )")
    print()
    print("  print(f'Total: {len(resultados)}')")

    print("\n📦 Estructura esperada de respuesta:")
    print("  {")
    print('    "data": [...],        ← campo_datos')
    print('    "pagination": {')
    print('      "next_cursor": "..." ← campo_cursor (puede ser anidado)')
    print("    }")
    print("  }")

    print("\n🔧 Campos anidados:")
    print("  - Si cursor está en pagination.next → 'pagination.next'")
    print("  - Si está en meta.cursor → 'meta.cursor'")
    print("  - Si está en response_metadata.next_cursor →")
    print("    'response_metadata.next_cursor'")


def ejemplo_mejores_practicas():
    """
    Mejores prácticas para paginación.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5E: Mejores Prácticas")
    print("=" * 60)

    print("\n✅ HACER:")
    print("  1. Leer documentación de la API cuidadosamente")
    print("  2. Identificar tipo de paginación (offset vs cursor)")
    print("  3. Usar límites razonables (50-100 items/página)")
    print("  4. Implementar límite de páginas para testing")
    print("  5. Cachear resultados si no cambian frecuentemente")
    print("  6. Manejar errores en medio de paginación")

    print("\n❌ NO HACER:")
    print("  1. Asumir que todas las APIs paginan igual")
    print("  2. Pedir pages muy grandes (>1000 items)")
    print("  3. Ignorar campos has_more o next_cursor=null")
    print("  4. Intentar decodificar/modificar cursores")
    print("  5. Hacer paginación infinita sin límite")

    print("\n🎯 ¿Cuándo usar cada tipo?")
    print()
    print("  USA OFFSET/LIMIT cuando:")
    print("    - Datos estáticos o que cambian poco")
    print("    - Necesitas saltar a páginas específicas")
    print("    - API simple sin cursor disponible")
    print()
    print("  USA CURSOR cuando:")
    print("    - Datos en tiempo real")
    print("    - Consistencia es crítica")
    print("    - API moderna (Twitter, Slack, Stripe...)")
    print("    - Datasets muy grandes")


if __name__ == "__main__":
    try:
        ejemplo_concepto_cursor()
        ejemplo_offset_vs_cursor()
        ejemplo_apis_cursor()
        ejemplo_uso_cursor()
        ejemplo_mejores_practicas()

        print("\n" + "=" * 60)
        print("✅ ¡Todos los ejemplos ejecutados correctamente!")
        print("=" * 60)
        print("\n💡 Nota: Este ejemplo es conceptual.")
        print("   Para probarlo con API real, necesitas una que use cursor.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
