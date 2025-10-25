"""
Cache Manager - Módulo para gestionar cache de requests HTTP

Este módulo implementa dos tipos de cache:
1. Cache en memoria: Ultra rápido pero volátil (dict con LRU)
2. Cache en disco: Persistente con shelve, sobrevive reinicios

Características:
- TTL (Time To Live) configurable
- Límite de tamaño para evitar memory leaks
- Limpieza automática de datos expirados

Ejemplo de uso:
    # Cache en memoria
    cache = crear_cache_memoria(max_size=1000)
    guardar_en_cache(cache, "url", {"datos": "..."})
    datos = obtener_de_cache(cache, "url")

    # Cache en disco con TTL
    cache = crear_cache_disco("datos/cache.db", ttl=3600)
    guardar_en_cache(cache, "url", {"datos": "..."})
"""

import shelve
import time
from typing import Any, Dict, Optional


def crear_cache_memoria(max_size: int = 1000) -> Dict:
    """
    Crea un cache en memoria con límite de tamaño (LRU).

    Args:
        max_size: Tamaño máximo del cache (default: 1000 elementos)

    Returns:
        Diccionario con configuración del cache

    Raises:
        ValueError: Si max_size no es válido

    Ejemplo:
        >>> cache = crear_cache_memoria(max_size=100)
        >>> cache["tipo"]
        'memoria'
    """
    if max_size <= 0:
        raise ValueError("max_size debe ser mayor a 0")

    return {
        "tipo": "memoria",
        "max_size": max_size,
        "datos": {},
        "orden": [],  # Para implementar LRU (Least Recently Used)
    }


def crear_cache_disco(archivo: str, ttl: int = 3600) -> Dict:
    """
    Crea un cache persistente en disco usando shelve.

    Args:
        archivo: Ruta al archivo de cache (sin extensión)
        ttl: Time To Live en segundos (default: 3600 = 1 hora)

    Returns:
        Diccionario con configuración del cache

    Raises:
        ValueError: Si ttl no es válido

    Ejemplo:
        >>> cache = crear_cache_disco("datos/cache.db", ttl=3600)
        >>> cache["tipo"]
        'disco'
    """
    if ttl <= 0:
        raise ValueError("ttl debe ser mayor a 0")

    # Cargar datos existentes si existen
    try:
        with shelve.open(archivo) as db:
            datos = dict(db)
    except Exception:
        datos = {}

    return {"tipo": "disco", "archivo": archivo, "ttl": ttl, "datos": datos}


def obtener_de_cache(cache: Dict, clave: str) -> Optional[Any]:
    """
    Obtiene un valor del cache.

    Args:
        cache: Configuración del cache
        clave: Clave a buscar

    Returns:
        Valor almacenado o None si no existe o expiró

    Ejemplo:
        >>> cache = crear_cache_memoria()
        >>> guardar_en_cache(cache, "clave1", "valor1")
        >>> obtener_de_cache(cache, "clave1")
        'valor1'
    """
    tipo = cache["tipo"]

    if tipo == "memoria":
        return _obtener_de_memoria(cache, clave)
    elif tipo == "disco":
        return _obtener_de_disco(cache, clave)
    else:
        raise ValueError(f"Tipo de cache desconocido: {tipo}")


def guardar_en_cache(cache: Dict, clave: str, valor: Any) -> None:
    """
    Guarda un valor en el cache.

    Args:
        cache: Configuración del cache
        clave: Clave para identificar el valor
        valor: Valor a almacenar (puede ser cualquier tipo)

    Ejemplo:
        >>> cache = crear_cache_memoria()
        >>> guardar_en_cache(cache, "usuario1", {"nombre": "Juan", "edad": 30})
        >>> obtener_de_cache(cache, "usuario1")
        {'nombre': 'Juan', 'edad': 30}
    """
    tipo = cache["tipo"]

    if tipo == "memoria":
        _guardar_en_memoria(cache, clave, valor)
    elif tipo == "disco":
        _guardar_en_disco(cache, clave, valor)
    else:
        raise ValueError(f"Tipo de cache desconocido: {tipo}")


def limpiar_cache_expirado(cache: Dict) -> int:
    """
    Limpia elementos expirados del cache.

    Args:
        cache: Configuración del cache

    Returns:
        Cantidad de elementos eliminados

    Ejemplo:
        >>> cache = crear_cache_disco("test.db", ttl=1)
        >>> guardar_en_cache(cache, "a", 1)
        >>> import time; time.sleep(1.2)
        >>> limpiar_cache_expirado(cache)
        1
    """
    tipo = cache["tipo"]

    if tipo == "memoria":
        # Cache en memoria no usa TTL, pero podemos limpiar si excede max_size
        return 0
    elif tipo == "disco":
        return _limpiar_disco_expirado(cache)
    else:
        raise ValueError(f"Tipo de cache desconocido: {tipo}")


# ===============================
# Funciones Privadas - Cache en Memoria
# ===============================


def _obtener_de_memoria(cache: Dict, clave: str) -> Optional[Any]:
    """
    Obtiene valor del cache en memoria con LRU.
    """
    if clave not in cache["datos"]:
        return None

    # Actualizar orden para LRU (mover al final = más reciente)
    if clave in cache["orden"]:
        cache["orden"].remove(clave)
    cache["orden"].append(clave)

    return cache["datos"][clave]


def _guardar_en_memoria(cache: Dict, clave: str, valor: Any) -> None:
    """
    Guarda valor en cache en memoria con LRU.
    """
    # Si ya existe, actualizar
    if clave in cache["datos"]:
        cache["datos"][clave] = valor
        # Actualizar orden LRU
        if clave in cache["orden"]:
            cache["orden"].remove(clave)
        cache["orden"].append(clave)
        return

    # Si se excede max_size, eliminar el menos usado (LRU)
    if len(cache["datos"]) >= cache["max_size"]:
        # Eliminar el primero de la lista (menos usado)
        if cache["orden"]:
            clave_antigua = cache["orden"].pop(0)
            if clave_antigua in cache["datos"]:
                del cache["datos"][clave_antigua]

    # Guardar nuevo valor
    cache["datos"][clave] = valor
    cache["orden"].append(clave)


# ===============================
# Funciones Privadas - Cache en Disco
# ===============================


def _obtener_de_disco(cache: Dict, clave: str) -> Optional[Any]:
    """
    Obtiene valor del cache en disco verificando TTL.
    """
    if clave not in cache["datos"]:
        return None

    entrada = cache["datos"][clave]

    # Verificar si es una entrada con timestamp (nueva estructura)
    if isinstance(entrada, dict) and "timestamp" in entrada:
        timestamp = entrada["timestamp"]
        valor = entrada["valor"]

        # Verificar si expiró
        tiempo_transcurrido = time.time() - timestamp
        if tiempo_transcurrido > cache["ttl"]:
            # Expirado, eliminar
            del cache["datos"][clave]
            _sincronizar_disco(cache)
            return None

        return valor

    # Entrada antigua sin timestamp, retornar directamente
    return entrada


def _guardar_en_disco(cache: Dict, clave: str, valor: Any) -> None:
    """
    Guarda valor en cache en disco con timestamp para TTL.
    """
    entrada = {"valor": valor, "timestamp": time.time()}

    cache["datos"][clave] = entrada

    # Sincronizar con archivo en disco
    _sincronizar_disco(cache)


def _sincronizar_disco(cache: Dict) -> None:
    """
    Sincroniza el cache en memoria con el archivo en disco.
    """
    try:
        with shelve.open(cache["archivo"]) as db:
            # Limpiar archivo
            db.clear()
            # Guardar todos los datos
            for clave, valor in cache["datos"].items():
                db[clave] = valor
    except Exception as e:
        # Si falla la escritura, continuar (no es crítico)
        print(f"Advertencia: No se pudo sincronizar cache en disco: {e}")


def _limpiar_disco_expirado(cache: Dict) -> int:
    """
    Limpia elementos expirados del cache en disco.
    """
    ahora = time.time()
    claves_a_eliminar = []

    for clave, entrada in cache["datos"].items():
        # Verificar si tiene timestamp
        if isinstance(entrada, dict) and "timestamp" in entrada:
            timestamp = entrada["timestamp"]
            tiempo_transcurrido = ahora - timestamp

            if tiempo_transcurrido > cache["ttl"]:
                claves_a_eliminar.append(clave)

    # Eliminar claves expiradas
    for clave in claves_a_eliminar:
        del cache["datos"][clave]

    # Sincronizar con disco si hubo cambios
    if claves_a_eliminar:
        _sincronizar_disco(cache)

    return len(claves_a_eliminar)
