"""
Tests para cache_manager.py - Gestión de Cache (TDD)

Módulo 4 - Tema 3: Scraper Masivo Optimizado
Total de tests: 18
Cobertura objetivo: >90%
"""

import os
import time

import pytest
from src.cache_manager import (
    crear_cache_disco,
    crear_cache_memoria,
    guardar_en_cache,
    limpiar_cache_expirado,
    obtener_de_cache,
)

# ===============================
# Tests: Cache en Memoria
# ===============================


def test_crear_cache_memoria_con_tamano_maximo():
    """Test: Crear cache en memoria con tamaño máximo."""
    cache = crear_cache_memoria(max_size=100)

    assert cache is not None
    assert cache["tipo"] == "memoria"
    assert cache["max_size"] == 100
    assert cache["datos"] == {}
    assert cache["orden"] == []  # Para LRU


def test_guardar_y_recuperar_valor_simple():
    """Test: Guardar y recuperar valor simple de cache en memoria."""
    cache = crear_cache_memoria()

    guardar_en_cache(cache, "clave1", "valor1")
    valor = obtener_de_cache(cache, "clave1")

    assert valor == "valor1"


def test_retornar_none_si_clave_no_existe():
    """Test: Retornar None si la clave no existe en cache."""
    cache = crear_cache_memoria()

    valor = obtener_de_cache(cache, "clave_inexistente")

    assert valor is None


def test_sobrescribir_valor_existente():
    """Test: Sobrescribir valor existente en cache."""
    cache = crear_cache_memoria()

    guardar_en_cache(cache, "clave1", "valor_original")
    guardar_en_cache(cache, "clave1", "valor_actualizado")

    valor = obtener_de_cache(cache, "clave1")
    assert valor == "valor_actualizado"


def test_limite_de_tamano_evitar_memory_leak():
    """Test: Límite de tamaño (evitar memory leak con LRU)."""
    cache = crear_cache_memoria(max_size=3)

    # Llenar cache al máximo
    guardar_en_cache(cache, "a", 1)
    guardar_en_cache(cache, "b", 2)
    guardar_en_cache(cache, "c", 3)

    assert len(cache["datos"]) == 3

    # Añadir cuarto elemento (debe eliminar "a" por LRU)
    guardar_en_cache(cache, "d", 4)

    assert len(cache["datos"]) == 3
    assert obtener_de_cache(cache, "a") is None  # Eliminado
    assert obtener_de_cache(cache, "d") == 4  # Añadido


def test_valores_complejos_almacenados_correctamente():
    """Test: Valores complejos (dict, list) se almacenan correctamente."""
    cache = crear_cache_memoria()

    # Guardar dict
    datos_dict = {"nombre": "Juan", "edad": 30}
    guardar_en_cache(cache, "usuario1", datos_dict)

    # Guardar list
    datos_list = [1, 2, 3, 4, 5]
    guardar_en_cache(cache, "numeros", datos_list)

    assert obtener_de_cache(cache, "usuario1") == datos_dict
    assert obtener_de_cache(cache, "numeros") == datos_list


# ===============================
# Tests: Cache en Disco
# ===============================


def test_crear_cache_disco_con_archivo_valido(tmp_path):
    """Test: Crear cache en disco con archivo válido."""
    archivo_cache = str(tmp_path / "test_cache.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    assert cache is not None
    assert cache["tipo"] == "disco"
    assert cache["archivo"] == archivo_cache
    assert cache["ttl"] == 3600
    assert "datos" in cache


def test_cache_disco_persiste_entre_ejecuciones(tmp_path):
    """Test: Cache en disco persiste entre ejecuciones."""
    archivo_cache = str(tmp_path / "persistente.db")

    # Primera ejecución: guardar datos
    cache1 = crear_cache_disco(archivo=archivo_cache, ttl=3600)
    guardar_en_cache(cache1, "clave_persistente", "valor_persistente")

    # Segunda ejecución: recuperar datos
    cache2 = crear_cache_disco(archivo=archivo_cache, ttl=3600)
    valor = obtener_de_cache(cache2, "clave_persistente")

    assert valor == "valor_persistente"


def test_ttl_dato_valido_retorna_valor(tmp_path):
    """Test: TTL - Dato válido retorna valor."""
    archivo_cache = str(tmp_path / "ttl_test.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=5)  # 5 segundos TTL

    guardar_en_cache(cache, "clave_ttl", "valor_ttl")

    # Leer inmediatamente (debe retornar valor)
    valor = obtener_de_cache(cache, "clave_ttl")
    assert valor == "valor_ttl"


def test_ttl_dato_expirado_retorna_none(tmp_path):
    """Test: TTL - Dato expirado retorna None."""
    archivo_cache = str(tmp_path / "ttl_expira.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=1)  # 1 segundo TTL

    guardar_en_cache(cache, "clave_expira", "valor_expira")

    # Esperar a que expire
    time.sleep(1.2)

    # Leer después de expiración (debe retornar None)
    valor = obtener_de_cache(cache, "clave_expira")
    assert valor is None


def test_guardar_con_timestamp_para_ttl(tmp_path):
    """Test: Guardar con timestamp para TTL."""
    archivo_cache = str(tmp_path / "timestamp.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    guardar_en_cache(cache, "clave_ts", {"datos": "test"})

    # Verificar que se guardó con timestamp
    assert "clave_ts" in cache["datos"]
    assert "timestamp" in cache["datos"]["clave_ts"]
    assert "valor" in cache["datos"]["clave_ts"]


def test_limpiar_cache_expirado_retorna_cantidad_eliminada(tmp_path):
    """Test: Limpiar cache expirado (retornar cantidad eliminada)."""
    archivo_cache = str(tmp_path / "limpiar.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=1)  # 1 segundo TTL

    # Guardar 3 elementos
    guardar_en_cache(cache, "a", 1)
    guardar_en_cache(cache, "b", 2)
    guardar_en_cache(cache, "c", 3)

    # Esperar a que expiren
    time.sleep(1.2)

    # Limpiar cache expirado
    cantidad_eliminada = limpiar_cache_expirado(cache)

    assert cantidad_eliminada == 3
    assert len(cache["datos"]) == 0


def test_cache_vacio_no_genera_errores(tmp_path):
    """Test: Cache vacío no genera errores."""
    archivo_cache = str(tmp_path / "vacio.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    # Limpiar cache vacío
    cantidad = limpiar_cache_expirado(cache)
    assert cantidad == 0

    # Obtener de cache vacío
    valor = obtener_de_cache(cache, "inexistente")
    assert valor is None


def test_caracteres_especiales_en_claves(tmp_path):
    """Test: Caracteres especiales en claves."""
    archivo_cache = str(tmp_path / "especiales.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    claves_especiales = [
        "clave con espacios",
        "clave_con_guiones-bajos",
        "clave/con/barras",
        "clave?con=params&query=1",
        "clave#con#hashes",
    ]

    for i, clave in enumerate(claves_especiales):
        guardar_en_cache(cache, clave, f"valor_{i}")

    for i, clave in enumerate(claves_especiales):
        valor = obtener_de_cache(cache, clave)
        assert valor == f"valor_{i}"


def test_claves_muy_largas(tmp_path):
    """Test: Claves muy largas (>1000 chars)."""
    archivo_cache = str(tmp_path / "largas.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    clave_larga = "a" * 2000  # 2000 caracteres
    valor = "valor_para_clave_larga"

    guardar_en_cache(cache, clave_larga, valor)
    resultado = obtener_de_cache(cache, clave_larga)

    assert resultado == valor


def test_valores_grandes(tmp_path):
    """Test: Valores grandes (>1MB)."""
    archivo_cache = str(tmp_path / "grandes.db")
    cache = crear_cache_disco(archivo=archivo_cache, ttl=3600)

    # Crear valor grande (~1.5 MB)
    valor_grande = {"datos": "x" * (1024 * 1024 * 2)}  # ~2MB string

    guardar_en_cache(cache, "clave_grande", valor_grande)
    resultado = obtener_de_cache(cache, "clave_grande")

    assert resultado == valor_grande


def test_cache_manager_parametros_invalidos():
    """Test: Parámetros inválidos lanzan ValueError."""
    with pytest.raises(ValueError, match="max_size debe ser mayor a 0"):
        crear_cache_memoria(max_size=0)

    with pytest.raises(ValueError, match="max_size debe ser mayor a 0"):
        crear_cache_memoria(max_size=-1)

    with pytest.raises(ValueError, match="ttl debe ser mayor a 0"):
        crear_cache_disco(archivo="test.db", ttl=0)

    with pytest.raises(ValueError, match="ttl debe ser mayor a 0"):
        crear_cache_disco(archivo="test.db", ttl=-1)
