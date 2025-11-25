"""
Fixtures compartidos para tests del proyecto integrador.
"""

import tempfile
from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import create_engine


@pytest.fixture
def df_noticias_bronze():
    """DataFrame con noticias en formato Bronze (datos crudos)."""
    return pd.DataFrame(
        {
            "id": ["1", "2", "3", "4", "5"],
            "title": [
                "Nueva tecnología revoluciona el mercado",
                "  Empresa anuncia resultados  ",
                "Breaking: Important Update",
                None,
                "Análisis del sector financiero",
            ],
            "content": [
                "La empresa TechCorp lanza producto innovador...",
                "Los resultados del Q4 superaron expectativas...",
                "Major announcement coming soon...",
                "Content missing",
                "El sector financiero muestra crecimiento...",
            ],
            "author": ["Ana García", "Luis Pérez", None, "María López", "Carlos Ruiz"],
            "published_date": [
                "2024-01-15 10:30:00",
                "2024-01-15 14:00:00",
                "invalid_date",
                "2024-01-16 09:00:00",
                "2024-01-16 11:30:00",
            ],
            "source": [
                "TechNews",
                "BusinessDaily",
                "NewsHub",
                "FinanceTimes",
                "EconomicReview",
            ],
            "category": ["tecnología", "negocios", "general", None, "finanzas"],
            "url": [
                "https://technews.com/article1",
                "https://businessdaily.com/article2",
                "https://newshub.com/article3",
                "https://financetimes.com/article4",
                "https://economicreview.com/article5",
            ],
        }
    )


@pytest.fixture
def df_noticias_silver():
    """DataFrame con noticias en formato Silver (limpias y validadas)."""
    return pd.DataFrame(
        {
            "id": [1, 2, 4, 5],
            "titulo": [
                "Nueva tecnología revoluciona el mercado",
                "Empresa anuncia resultados",
                "Análisis del sector financiero",
                "Análisis del sector financiero",
            ],
            "contenido": [
                "La empresa TechCorp lanza producto innovador...",
                "Los resultados del Q4 superaron expectativas...",
                "Content missing",
                "El sector financiero muestra crecimiento...",
            ],
            "autor": ["Ana García", "Luis Pérez", "María López", "Carlos Ruiz"],
            "fecha_publicacion": pd.to_datetime(
                [
                    "2024-01-15 10:30:00",
                    "2024-01-15 14:00:00",
                    "2024-01-16 09:00:00",
                    "2024-01-16 11:30:00",
                ]
            ),
            "fuente": ["TechNews", "BusinessDaily", "FinanceTimes", "EconomicReview"],
            "categoria": ["tecnología", "negocios", "finanzas", "finanzas"],
            "url": [
                "https://technews.com/article1",
                "https://businessdaily.com/article2",
                "https://financetimes.com/article4",
                "https://economicreview.com/article5",
            ],
            "longitud_contenido": [45, 46, 15, 45],
            "longitud_titulo": [41, 26, 34, 34],
        }
    )


@pytest.fixture
def engine_temporal():
    """Engine de SQLite en memoria para tests."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def directorio_temporal():
    """Directorio temporal para tests de archivos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear subdirectorios bronze, silver, gold
        base = Path(tmpdir)
        (base / "bronze").mkdir()
        (base / "silver").mkdir()
        (base / "gold").mkdir()
        yield base


@pytest.fixture
def archivo_parquet_temporal(directorio_temporal, df_noticias_bronze):
    """Archivo Parquet temporal con datos Bronze."""
    ruta = directorio_temporal / "bronze" / "noticias_test.parquet"
    df_noticias_bronze.to_parquet(ruta, index=False)
    return ruta


@pytest.fixture
def api_response_mock():
    """Mock de respuesta de API de noticias."""
    return {
        "status": "ok",
        "totalResults": 3,
        "articles": [
            {
                "source": {"id": "tech-news", "name": "TechNews"},
                "author": "Ana García",
                "title": "Nueva tecnología revoluciona el mercado",
                "description": "Descripción breve...",
                "url": "https://technews.com/article1",
                "urlToImage": "https://technews.com/img1.jpg",
                "publishedAt": "2024-01-15T10:30:00Z",
                "content": "La empresa TechCorp lanza producto innovador...",
            },
            {
                "source": {"id": "business-daily", "name": "BusinessDaily"},
                "author": "Luis Pérez",
                "title": "Empresa anuncia resultados",
                "description": "Resultados Q4...",
                "url": "https://businessdaily.com/article2",
                "urlToImage": "https://businessdaily.com/img2.jpg",
                "publishedAt": "2024-01-15T14:00:00Z",
                "content": "Los resultados del Q4 superaron expectativas...",
            },
            {
                "source": {"id": "news-hub", "name": "NewsHub"},
                "author": None,
                "title": "Breaking: Important Update",
                "description": "Major update...",
                "url": "https://newshub.com/article3",
                "urlToImage": None,
                "publishedAt": "2024-01-16T09:00:00Z",
                "content": "Major announcement coming soon...",
            },
        ],
    }
