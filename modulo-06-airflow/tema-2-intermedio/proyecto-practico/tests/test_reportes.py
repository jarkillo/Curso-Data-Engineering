"""
Tests para el módulo de reportes.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import json
import tempfile
from pathlib import Path

import pandas as pd


def test_generar_reporte_detallado():
    """Test: generar_reporte_detallado crea dict con métricas completas"""
    from src.reportes import generar_reporte_detallado

    df = pd.DataFrame(
        {
            "cliente_id": ["C001", "C002"],
            "nombre": ["Alice", "Bob"],
            "total_ventas": [3600.0, 255.0],
            "num_productos": [2, 1],
        }
    )

    reporte = generar_reporte_detallado(df, total=3855.0)

    assert isinstance(reporte, dict)
    assert "tipo" in reporte
    assert reporte["tipo"] == "detallado"
    assert "total_ventas" in reporte
    assert reporte["total_ventas"] == 3855.0
    assert "num_clientes" in reporte
    assert reporte["num_clientes"] == 2
    assert "clientes" in reporte
    assert len(reporte["clientes"]) == 2


def test_generar_reporte_simple():
    """Test: generar_reporte_simple crea dict con métricas básicas"""
    from src.reportes import generar_reporte_simple

    df = pd.DataFrame(
        {
            "cliente_id": ["C001", "C002"],
            "nombre": ["Alice", "Bob"],
            "total_ventas": [3600.0, 255.0],
        }
    )

    reporte = generar_reporte_simple(df, total=3855.0)

    assert isinstance(reporte, dict)
    assert "tipo" in reporte
    assert reporte["tipo"] == "simple"
    assert "total_ventas" in reporte
    assert reporte["total_ventas"] == 3855.0
    assert "num_clientes" in reporte
    assert reporte["num_clientes"] == 2
    # No debe incluir detalles de clientes
    assert "clientes" not in reporte


def test_exportar_reporte_csv():
    """Test: exportar_reporte_csv guarda DataFrame correctamente"""
    from src.reportes import exportar_reporte_csv

    df = pd.DataFrame(
        {
            "cliente_id": ["C001", "C002"],
            "nombre": ["Alice", "Bob"],
            "total_ventas": [3600.0, 255.0],
        }
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        ruta_tmp = tmp.name

    try:
        exportar_reporte_csv(df, ruta_tmp)

        # Verificar que el archivo existe y es válido
        assert Path(ruta_tmp).exists()
        df_leido = pd.read_csv(ruta_tmp)
        assert len(df_leido) == 2
        assert list(df_leido.columns) == ["cliente_id", "nombre", "total_ventas"]
    finally:
        Path(ruta_tmp).unlink()


def test_exportar_reporte_json():
    """Test: exportar_reporte_json guarda dict correctamente"""
    from src.reportes import exportar_reporte_json

    reporte = {
        "tipo": "detallado",
        "total_ventas": 3855.0,
        "num_clientes": 2,
        "clientes": [
            {"cliente_id": "C001", "nombre": "Alice"},
            {"cliente_id": "C002", "nombre": "Bob"},
        ],
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        ruta_tmp = tmp.name

    try:
        exportar_reporte_json(reporte, ruta_tmp)

        # Verificar que el archivo existe y es válido
        assert Path(ruta_tmp).exists()
        with open(ruta_tmp) as f:
            reporte_leido = json.load(f)
        assert reporte_leido["tipo"] == "detallado"
        assert reporte_leido["num_clientes"] == 2
    finally:
        Path(ruta_tmp).unlink()


def test_exportar_reporte_csv_crea_directorio_si_no_existe():
    """Test: exportar_reporte_csv crea el directorio padre si no existe"""
    from src.reportes import exportar_reporte_csv

    df = pd.DataFrame({"col": [1, 2, 3]})

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_tmp = Path(tmpdir) / "subdir" / "no_existe" / "reporte.csv"

        exportar_reporte_csv(df, str(ruta_tmp))

        assert ruta_tmp.exists()
        df_leido = pd.read_csv(ruta_tmp)
        assert len(df_leido) == 3
