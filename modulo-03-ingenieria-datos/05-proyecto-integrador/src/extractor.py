"""
Módulo de extracción de noticias (capa Bronze).

Extrae datos de API simulada y los guarda en formato Parquet.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import pandas as pd
from faker import Faker


def extraer_noticias_api_simulada(num_noticias: int = 100) -> pd.DataFrame:
    """
    Simula extracción de noticias desde API.

    Args:
        num_noticias: Número de noticias a generar

    Returns:
        DataFrame con noticias simuladas

    Raises:
        ValueError: Si num_noticias <= 0

    Examples:
        >>> df = extraer_noticias_api_simulada(num_noticias=10)
        >>> len(df)
        10
        >>> 'title' in df.columns
        True
    """
    if num_noticias <= 0:
        raise ValueError("num_noticias debe ser mayor que 0")

    fake = Faker("es_ES")
    Faker.seed(42)  # Para reproducibilidad en tests

    categorias = ["tecnología", "negocios", "finanzas", "deportes", "cultura"]
    fuentes = ["TechNews", "BusinessDaily", "FinanceTimes", "SportsHub", "CultureMag"]

    noticias = []
    fecha_base = datetime.now()

    for i in range(num_noticias):
        noticia = {
            "id": str(uuid4()),
            "title": fake.sentence(nb_words=8).rstrip("."),
            "content": fake.text(max_nb_chars=200),
            "author": fake.name(),
            "published_date": (fecha_base - timedelta(hours=i)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "source": fake.random_element(fuentes),
            "category": fake.random_element(categorias),
            "url": f"https://{fake.domain_name()}/article-{i+1}",
        }
        noticias.append(noticia)

    return pd.DataFrame(noticias)


def normalizar_respuesta_api(respuesta: dict[str, Any]) -> pd.DataFrame:
    """
    Normaliza respuesta de API a DataFrame.

    Args:
        respuesta: Diccionario con respuesta de API de noticias

    Returns:
        DataFrame normalizado

    Examples:
        >>> respuesta = {"articles": [{"title": "Test", "source": {"name": "TestNews"}}]}
        >>> df = normalizar_respuesta_api(respuesta)
        >>> 'title' in df.columns
        True
    """
    if not respuesta.get("articles"):
        return pd.DataFrame()

    noticias = []
    for _idx, articulo in enumerate(respuesta["articles"]):
        noticia = {
            "id": str(uuid4()),
            "title": articulo.get("title"),
            "content": articulo.get("content"),
            "author": articulo.get("author"),
            "published_date": articulo.get("publishedAt"),
            "source": articulo.get("source", {}).get("name"),
            "category": "general",  # API real no siempre provee categoría
            "url": articulo.get("url"),
        }
        noticias.append(noticia)

    return pd.DataFrame(noticias)


def guardar_en_bronze(df: pd.DataFrame, ruta: Path) -> None:
    """
    Guarda DataFrame en capa Bronze (formato Parquet).

    Args:
        df: DataFrame a guardar
        ruta: Ruta del archivo Parquet

    Raises:
        ValueError: Si DataFrame está vacío

    Examples:
        >>> from pathlib import Path
        >>> df = pd.DataFrame({"col": [1, 2, 3]})
        >>> guardar_en_bronze(df, Path("test.parquet"))  # doctest: +SKIP
    """
    if df.empty:
        raise ValueError("No se puede guardar DataFrame vacío")

    # Crear directorio si no existe
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # Guardar en Parquet con compresión
    df.to_parquet(ruta, index=False, compression="snappy")


def extraer_noticias_desde_parquet(ruta: Path) -> pd.DataFrame:
    """
    Extrae noticias desde archivo Parquet en capa Bronze.

    Args:
        ruta: Ruta del archivo Parquet

    Returns:
        DataFrame con noticias

    Raises:
        FileNotFoundError: Si archivo no existe

    Examples:
        >>> from pathlib import Path
        >>> df = extraer_noticias_desde_parquet(Path("noticias.parquet"))  # doctest: +SKIP
    """
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    return pd.read_parquet(ruta)
