"""
Rate Limiter - Módulo para controlar la tasa de requests HTTP

Este módulo implementa dos algoritmos de rate limiting:
1. Fixed Window: Límite fijo de requests por ventana de tiempo
2. Token Bucket: Permite bursts controlados con reposición gradual

Ejemplo de uso:
    # Token Bucket (recomendado)
    limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=10.0)

    if puede_hacer_request(limiter):
        # hacer request HTTP
        pass
    else:
        tiempo_espera = esperar_disponibilidad(limiter)
        print(f"Esperando {tiempo_espera:.2f}s...")
"""

import time
from typing import Dict


def crear_rate_limiter_fixed_window(max_requests: int, window_seconds: int) -> Dict:
    """
    Crea un rate limiter con algoritmo Fixed Window.

    Args:
        max_requests: Número máximo de requests permitidos por ventana
        window_seconds: Duración de la ventana en segundos

    Returns:
        Diccionario con configuración del rate limiter

    Raises:
        ValueError: Si los parámetros no son válidos

    Ejemplo:
        >>> limiter = crear_rate_limiter_fixed_window(max_requests=100, window_seconds=60)
        >>> limiter["tipo"]
        'fixed_window'
    """
    if max_requests <= 0:
        raise ValueError("max_requests debe ser mayor a 0")

    if window_seconds <= 0:
        raise ValueError("window_seconds debe ser mayor a 0")

    return {
        "tipo": "fixed_window",
        "max_requests": max_requests,
        "window_seconds": window_seconds,
        "requests_en_ventana": 0,
        "inicio_ventana": time.time(),
    }


def crear_rate_limiter_token_bucket(capacidad: int, tasa_reposicion: float) -> Dict:
    """
    Crea un rate limiter con algoritmo Token Bucket.

    Este algoritmo permite bursts controlados y es más flexible que Fixed Window.

    Args:
        capacidad: Número máximo de tokens (burst size)
        tasa_reposicion: Tokens añadidos por segundo

    Returns:
        Diccionario con configuración del rate limiter

    Raises:
        ValueError: Si los parámetros no son válidos

    Ejemplo:
        >>> limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=10.0)
        >>> limiter["tokens"]
        20
    """
    if capacidad <= 0:
        raise ValueError("capacidad debe ser mayor a 0")

    if tasa_reposicion <= 0:
        raise ValueError("tasa_reposicion debe ser mayor a 0")

    return {
        "tipo": "token_bucket",
        "capacidad": capacidad,
        "tasa_reposicion": tasa_reposicion,
        "tokens": capacidad,  # Inicia con el bucket lleno
        "ultima_actualizacion": time.time(),
    }


def puede_hacer_request(rate_limiter: Dict) -> bool:
    """
    Verifica si se puede hacer un request según el rate limiter.

    Si puede hacer el request, consume un token/slot automáticamente.

    Args:
        rate_limiter: Configuración del rate limiter

    Returns:
        True si puede hacer el request, False en caso contrario

    Ejemplo:
        >>> limiter = crear_rate_limiter_token_bucket(capacidad=5, tasa_reposicion=5.0)
        >>> puede_hacer_request(limiter)
        True
        >>> limiter["tokens"]
        4
    """
    tipo = rate_limiter["tipo"]

    if tipo == "fixed_window":
        return _puede_hacer_request_fixed_window(rate_limiter)
    elif tipo == "token_bucket":
        return _puede_hacer_request_token_bucket(rate_limiter)
    else:
        raise ValueError(f"Tipo de rate limiter desconocido: {tipo}")


def esperar_disponibilidad(rate_limiter: Dict, timeout: float = 60.0) -> float:
    """
    Espera hasta que haya disponibilidad para hacer un request.

    Args:
        rate_limiter: Configuración del rate limiter
        timeout: Tiempo máximo de espera en segundos (default: 60s)

    Returns:
        Tiempo total esperado en segundos

    Raises:
        TimeoutError: Si se excede el timeout sin obtener disponibilidad

    Ejemplo:
        >>> limiter = crear_rate_limiter_token_bucket(capacidad=1, tasa_reposicion=10.0)
        >>> puede_hacer_request(limiter)  # Consume el único token
        True
        >>> tiempo = esperar_disponibilidad(limiter, timeout=1.0)
        >>> tiempo >= 0.1  # Esperó al menos 0.1 segundos
        True
    """
    tipo = rate_limiter["tipo"]
    inicio = time.time()

    if tipo == "fixed_window":
        tiempo_espera = _calcular_espera_fixed_window(rate_limiter)
    elif tipo == "token_bucket":
        tiempo_espera = _calcular_espera_token_bucket(rate_limiter)
    else:
        raise ValueError(f"Tipo de rate limiter desconocido: {tipo}")

    if tiempo_espera > timeout:
        raise TimeoutError(
            f"Tiempo de espera ({tiempo_espera:.2f}s) excede timeout ({timeout}s)"
        )

    # Esperar el tiempo calculado
    time.sleep(tiempo_espera)

    # Intentar consumir token/slot después de esperar
    if not puede_hacer_request(rate_limiter):
        # Si aún no hay disponibilidad, esperar un poco más
        time.sleep(0.1)
        puede_hacer_request(rate_limiter)

    tiempo_total = time.time() - inicio
    return tiempo_total


# ===============================
# Funciones Privadas - Fixed Window
# ===============================


def _puede_hacer_request_fixed_window(rate_limiter: Dict) -> bool:
    """
    Verifica disponibilidad para Fixed Window.
    """
    ahora = time.time()
    tiempo_transcurrido = ahora - rate_limiter["inicio_ventana"]

    # Si pasó la ventana, resetear contador
    if tiempo_transcurrido >= rate_limiter["window_seconds"]:
        rate_limiter["requests_en_ventana"] = 0
        rate_limiter["inicio_ventana"] = ahora

    # Verificar si hay cupo disponible
    if rate_limiter["requests_en_ventana"] < rate_limiter["max_requests"]:
        rate_limiter["requests_en_ventana"] += 1
        return True

    return False


def _calcular_espera_fixed_window(rate_limiter: Dict) -> float:
    """
    Calcula tiempo de espera para Fixed Window.
    """
    ahora = time.time()
    tiempo_transcurrido = ahora - rate_limiter["inicio_ventana"]
    tiempo_restante = rate_limiter["window_seconds"] - tiempo_transcurrido

    # Si ya pasó la ventana, no hay que esperar
    if tiempo_restante <= 0:
        return 0.0

    return tiempo_restante


# ===============================
# Funciones Privadas - Token Bucket
# ===============================


def _puede_hacer_request_token_bucket(rate_limiter: Dict) -> bool:
    """
    Verifica disponibilidad para Token Bucket.
    """
    # Reponer tokens según tiempo transcurrido
    _reponer_tokens(rate_limiter)

    # Verificar si hay al menos 1 token disponible
    if rate_limiter["tokens"] >= 1:
        rate_limiter["tokens"] -= 1
        return True

    return False


def _reponer_tokens(rate_limiter: Dict) -> None:
    """
    Repone tokens según el tiempo transcurrido.
    """
    ahora = time.time()
    tiempo_transcurrido = ahora - rate_limiter["ultima_actualizacion"]

    # Calcular tokens a reponer
    tokens_a_reponer = tiempo_transcurrido * rate_limiter["tasa_reposicion"]

    # Añadir tokens sin exceder la capacidad
    rate_limiter["tokens"] = min(
        rate_limiter["capacidad"], rate_limiter["tokens"] + tokens_a_reponer
    )

    rate_limiter["ultima_actualizacion"] = ahora


def _calcular_espera_token_bucket(rate_limiter: Dict) -> float:
    """
    Calcula tiempo de espera para Token Bucket.
    """
    # Reponer tokens primero
    _reponer_tokens(rate_limiter)

    # Si ya hay tokens, no esperar
    if rate_limiter["tokens"] >= 1:
        return 0.0

    # Calcular tiempo necesario para reponer 1 token
    tokens_faltantes = 1 - rate_limiter["tokens"]
    tiempo_espera = tokens_faltantes / rate_limiter["tasa_reposicion"]

    return tiempo_espera
