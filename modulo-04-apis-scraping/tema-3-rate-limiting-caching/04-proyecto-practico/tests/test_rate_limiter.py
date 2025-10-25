"""
Tests para rate_limiter.py - Rate Limiting (TDD)

Módulo 4 - Tema 3: Scraper Masivo Optimizado
Total de tests: 15
Cobertura objetivo: >85%
"""

import time

import pytest
from src.rate_limiter import (
    crear_rate_limiter_fixed_window,
    crear_rate_limiter_token_bucket,
    esperar_disponibilidad,
    puede_hacer_request,
)

# ===============================
# Tests: Fixed Window Rate Limiter
# ===============================


def test_crear_fixed_window_parametros_validos():
    """Test: Crear rate limiter Fixed Window con parámetros válidos."""
    limiter = crear_rate_limiter_fixed_window(max_requests=100, window_seconds=60)

    assert limiter is not None
    assert limiter["tipo"] == "fixed_window"
    assert limiter["max_requests"] == 100
    assert limiter["window_seconds"] == 60
    assert limiter["requests_en_ventana"] == 0
    assert "inicio_ventana" in limiter


def test_fixed_window_limite_maximo_requests():
    """Test: Validar límite máximo de requests por ventana."""
    limiter = crear_rate_limiter_fixed_window(max_requests=5, window_seconds=1)

    # Primer request debe permitirse
    assert puede_hacer_request(limiter) is True
    assert limiter["requests_en_ventana"] == 1

    # Requests 2-5 permitidos
    for i in range(4):
        assert puede_hacer_request(limiter) is True

    assert limiter["requests_en_ventana"] == 5

    # Request 6 debe ser rechazado (límite alcanzado)
    assert puede_hacer_request(limiter) is False
    assert limiter["requests_en_ventana"] == 5  # No incrementa


def test_fixed_window_reseteo_automatico():
    """Test: Reseteo automático al cambiar de ventana."""
    limiter = crear_rate_limiter_fixed_window(max_requests=3, window_seconds=1)

    # Consumir todos los requests
    for _ in range(3):
        assert puede_hacer_request(limiter) is True

    # No hay más disponibles
    assert puede_hacer_request(limiter) is False

    # Esperar a que expire la ventana
    time.sleep(1.1)

    # Ahora debe permitir de nuevo
    assert puede_hacer_request(limiter) is True
    assert limiter["requests_en_ventana"] == 1


def test_fixed_window_parametros_invalidos():
    """Test: Parámetros inválidos lanzan ValueError."""
    with pytest.raises(ValueError, match="max_requests debe ser mayor a 0"):
        crear_rate_limiter_fixed_window(max_requests=0, window_seconds=60)

    with pytest.raises(ValueError, match="max_requests debe ser mayor a 0"):
        crear_rate_limiter_fixed_window(max_requests=-1, window_seconds=60)

    with pytest.raises(ValueError, match="window_seconds debe ser mayor a 0"):
        crear_rate_limiter_fixed_window(max_requests=100, window_seconds=0)

    with pytest.raises(ValueError, match="window_seconds debe ser mayor a 0"):
        crear_rate_limiter_fixed_window(max_requests=100, window_seconds=-1)


# ===============================
# Tests: Token Bucket Rate Limiter
# ===============================


def test_crear_token_bucket_parametros_validos():
    """Test: Crear Token Bucket con capacidad y tasa válidas."""
    limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=10.0)

    assert limiter is not None
    assert limiter["tipo"] == "token_bucket"
    assert limiter["capacidad"] == 20
    assert limiter["tasa_reposicion"] == 10.0
    assert limiter["tokens"] == 20  # Inicia lleno
    assert "ultima_actualizacion" in limiter


def test_token_bucket_consumir_tokens_gradualmente():
    """Test: Consumir tokens gradualmente."""
    limiter = crear_rate_limiter_token_bucket(capacidad=10, tasa_reposicion=5.0)

    # Consumir 5 tokens
    for i in range(5):
        assert puede_hacer_request(limiter) is True
        # Usar aproximación por posible reposición de tokens en el tiempo
        assert 9 - i <= limiter["tokens"] < 11 - i

    # Quedan aproximadamente 5 tokens
    assert 4 <= limiter["tokens"] <= 6


def test_token_bucket_reposicion_automatica():
    """Test: Reposición automática de tokens."""
    limiter = crear_rate_limiter_token_bucket(capacidad=10, tasa_reposicion=10.0)

    # Consumir 5 tokens
    for _ in range(5):
        puede_hacer_request(limiter)

    assert 4 <= limiter["tokens"] <= 6  # Aproximadamente 5 tokens

    # Esperar 0.5 segundos (debería generar 5 tokens: 10 tokens/seg * 0.5 seg)
    time.sleep(0.5)

    # Verificar que se repusieron tokens
    puede_hacer_request(limiter)  # Esto activa la reposición
    assert limiter["tokens"] >= 8  # 5 + 5 - 1 ≈ 9, con margen


def test_token_bucket_burst_inicial():
    """Test: Permitir burst inicial (consumir todos los tokens)."""
    limiter = crear_rate_limiter_token_bucket(capacidad=20, tasa_reposicion=5.0)

    # Consumir todos los 20 tokens en burst
    for i in range(20):
        assert puede_hacer_request(limiter) is True

    assert limiter["tokens"] < 1  # Prácticamente 0 (puede haber micro-reposición)

    # Request 21 debe ser rechazado (o aceptado si hubo reposición significativa)
    # Debido a tiempo de ejecución, puede haber tokens repuestos
    if limiter["tokens"] < 1:
        assert puede_hacer_request(limiter) is False


def test_token_bucket_bloqueo_sin_tokens():
    """Test: Bloqueo cuando no hay tokens disponibles."""
    limiter = crear_rate_limiter_token_bucket(capacidad=2, tasa_reposicion=1.0)

    # Consumir todos los tokens
    assert puede_hacer_request(limiter) is True
    assert puede_hacer_request(limiter) is True

    # No hay más tokens (o muy pocos por micro-reposición)
    if limiter["tokens"] < 1:
        assert puede_hacer_request(limiter) is False
    assert limiter["tokens"] < 1  # Prácticamente 0


def test_token_bucket_parametros_invalidos():
    """Test: Parámetros inválidos lanzan ValueError."""
    with pytest.raises(ValueError, match="capacidad debe ser mayor a 0"):
        crear_rate_limiter_token_bucket(capacidad=0, tasa_reposicion=5.0)

    with pytest.raises(ValueError, match="tasa_reposicion debe ser mayor a 0"):
        crear_rate_limiter_token_bucket(capacidad=10, tasa_reposicion=0.0)

    with pytest.raises(ValueError, match="tasa_reposicion debe ser mayor a 0"):
        crear_rate_limiter_token_bucket(capacidad=10, tasa_reposicion=-1.0)


# ===============================
# Tests: Funciones Generales
# ===============================


def test_esperar_disponibilidad_fixed_window():
    """Test: Esperar hasta que haya requests disponibles (Fixed Window)."""
    limiter = crear_rate_limiter_fixed_window(max_requests=2, window_seconds=1)

    # Consumir todos los requests
    puede_hacer_request(limiter)
    puede_hacer_request(limiter)

    # Esperar disponibilidad (debe bloquear ~1 segundo)
    inicio = time.time()
    tiempo_espera = esperar_disponibilidad(limiter)
    fin = time.time()

    assert tiempo_espera >= 0.9  # Al menos 0.9 segundos de espera
    assert (fin - inicio) >= 0.9
    assert limiter["requests_en_ventana"] == 1  # Consumió 1 después de esperar


def test_esperar_disponibilidad_token_bucket():
    """Test: Esperar hasta que se repongan tokens (Token Bucket)."""
    limiter = crear_rate_limiter_token_bucket(capacidad=1, tasa_reposicion=10.0)

    # Consumir el único token
    assert puede_hacer_request(limiter) is True

    # Esperar que se reponga (0.1 seg para 1 token a 10 tokens/seg)
    inicio = time.time()
    tiempo_espera = esperar_disponibilidad(limiter)
    fin = time.time()

    assert tiempo_espera >= 0.05  # Al menos 50ms
    assert (fin - inicio) >= 0.05
    assert limiter["tokens"] >= 0  # Debería tener tokens


def test_rate_limiter_independientes():
    """Test: Múltiples rate limiters son independientes."""
    limiter1 = crear_rate_limiter_token_bucket(capacidad=5, tasa_reposicion=5.0)
    limiter2 = crear_rate_limiter_token_bucket(capacidad=10, tasa_reposicion=10.0)

    # Consumir tokens en limiter1
    for _ in range(3):
        puede_hacer_request(limiter1)

    # limiter2 no debe verse afectado
    assert 1 <= limiter1["tokens"] <= 3  # Aproximadamente 2 tokens
    assert 9 <= limiter2["tokens"] <= 11  # Aproximadamente 10 tokens


def test_calcular_tiempo_espera_correctamente():
    """Test: Calcular tiempo de espera correctamente."""
    limiter = crear_rate_limiter_token_bucket(capacidad=1, tasa_reposicion=2.0)

    # Consumir token
    puede_hacer_request(limiter)

    # Necesita 0.5 seg para reponer 1 token (2 tokens/seg)
    tiempo_espera = esperar_disponibilidad(limiter, timeout=1.0)

    # Debe ser aproximadamente 0.5 segundos
    assert 0.4 <= tiempo_espera <= 0.6
