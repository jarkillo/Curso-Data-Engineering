"""
Ejemplo 3: Reintentos con Exponential Backoff

Aprende a manejar errores temporales con reintentos automáticos.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

from src.reintentos import calcular_delay_exponencial, reintentar_con_backoff


def ejemplo_calcular_delays():
    """
    Entiende cómo funciona el exponential backoff.
    """
    print("=" * 60)
    print("EJEMPLO 3A: Exponential Backoff")
    print("=" * 60)

    print("\n📊 Delays entre reintentos (base=2):")
    for intento in range(1, 6):
        delay = calcular_delay_exponencial(intento)
        print(f"  Intento {intento}: esperar {delay} segundos")

    print("\n📊 Delays con base=3:")
    for intento in range(1, 5):
        delay = calcular_delay_exponencial(intento, base=3)
        print(f"  Intento {intento}: esperar {delay} segundos")

    print("\n📊 Delays con límite máximo:")
    for intento in range(1, 8):
        delay = calcular_delay_exponencial(intento, max_delay=30)
        print(f"  Intento {intento}: esperar {delay} segundos")

    print("\n💡 ¿Por qué exponencial?")
    print("  - Reduce carga en servidor con problemas")
    print("  - Da tiempo al servidor para recuperarse")
    print("  - Evita 'thundering herd' (muchos clientes reintentando a la vez)")


def ejemplo_request_con_reintentos():
    """
    Hace un request con reintentos automáticos.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3B: Request con Reintentos")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/users/1"

    print("\n📡 Haciendo request con hasta 3 intentos...")
    print(f"  URL: {url}")

    try:
        response = reintentar_con_backoff(url=url, max_intentos=3)

        print("\n✅ Request exitoso!")
        print(f"  Status Code: {response.status_code}")
        print(f"  Respuesta: {response.json()['name']}")

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Todos los intentos fallaron: {e}")


def ejemplo_que_se_reintenta():
    """
    Explica qué errores se reintentan y cuáles no.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3C: ¿Qué se Reintenta?")
    print("=" * 60)

    print("\n✅ SE REINTENTAN (errores temporales):")
    print("  - 500 Internal Server Error")
    print("  - 502 Bad Gateway")
    print("  - 503 Service Unavailable")
    print("  - 504 Gateway Timeout")
    print("  - 429 Too Many Requests (Rate Limit)")

    print("\n❌ NO SE REINTENTAN (errores permanentes):")
    print("  - 400 Bad Request → Tu request está mal")
    print("  - 401 Unauthorized → Falta/mala autenticación")
    print("  - 403 Forbidden → No tienes permiso")
    print("  - 404 Not Found → Recurso no existe")
    print("  - 422 Unprocessable Entity → Datos inválidos")

    print("\n💡 ¿Por qué esta distinción?")
    print("  - 4xx: Son errores TU código → reintentar no ayuda")
    print("  - 5xx: Son errores del servidor → puede recuperarse")
    print("  - 429: Rate limit → esperar y reintentar funciona")


def ejemplo_post_con_reintentos():
    """
    POST request con reintentos.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3D: POST con Reintentos")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    data = {"title": "Título de ejemplo", "body": "Contenido del post", "userId": 1}

    print("\n📡 Enviando POST con reintentos...")
    print(f"  URL: {url}")
    print(f"  Datos: {data}")

    try:
        response = reintentar_con_backoff(
            url=url, metodo="POST", json=data, max_intentos=3
        )

        print("\n✅ POST exitoso!")
        print(f"  Status Code: {response.status_code}")
        print(f"  ID creado: {response.json().get('id')}")

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error: {e}")


def ejemplo_mejores_practicas():
    """
    Mejores prácticas para reintentos.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3E: Mejores Prácticas")
    print("=" * 60)

    print("\n✅ HACER:")
    print("  1. Usar reintentos para APIs externas no confiables")
    print("  2. Configurar max_intentos razonable (3-5)")
    print("  3. Logear cada reintento para debugging")
    print("  4. Respetar header 'Retry-After' si la API lo envía")
    print("  5. Usar exponential backoff (no reintentos constantes)")

    print("\n❌ NO HACER:")
    print("  1. Reintentar indefinidamente (puede colgar tu app)")
    print("  2. Reintentar muy rápido (empeora el problema)")
    print("  3. Reintentar operaciones no-idempotentes sin cuidado")
    print("  4. Ignorar errores 4xx (no se solucionan reintentando)")
    print("  5. Usar reintentos para APIs internas confiables")

    print("\n💡 Idempotencia:")
    print("  - GET, PUT, DELETE → Seguros de reintentar")
    print("  - POST → Cuidado! Puede crear duplicados")
    print("  - Solución: usar IDs únicos o API idempotente")


if __name__ == "__main__":
    try:
        ejemplo_calcular_delays()
        ejemplo_request_con_reintentos()
        ejemplo_que_se_reintenta()
        ejemplo_post_con_reintentos()
        ejemplo_mejores_practicas()

        print("\n" + "=" * 60)
        print("✅ ¡Todos los ejemplos ejecutados correctamente!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
