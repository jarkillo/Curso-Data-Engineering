"""
Tests para el módulo de carga/guardado de reportes

Guarda reportes en formato CSV y TXT.
"""

import os
from pathlib import Path


def test_guardar_reporte_csv(tmp_path):
    """
    Test: guardar_reporte_csv debe crear archivo CSV con métricas

    Given: Un dict de métricas y una fecha
    When: Se llama a guardar_reporte_csv
    Then: Crea archivo CSV en data/output/ y retorna la ruta
    """
    from src.carga import guardar_reporte_csv

    metricas = {
        "total_ventas": 1250.50,
        "ticket_promedio": 208.42,
        "cantidad_ventas": 6,
        "top_productos": [
            {"producto": "Laptop", "cantidad": 5},
            {"producto": "Mouse", "cantidad": 10},
        ],
    }
    fecha = "2025-10-25"

    # Usar tmp_path para tests
    ruta = guardar_reporte_csv(metricas, fecha, directorio_base=str(tmp_path))

    assert os.path.exists(ruta)
    assert ruta.endswith(".csv")

    # Verificar contenido
    with open(ruta, "r") as f:
        contenido = f.read()
        assert "total_ventas" in contenido
        assert "1250.5" in contenido or "1250.50" in contenido


def test_guardar_reporte_csv_sin_directorio(tmp_path):
    """
    Test: guardar_reporte_csv debe crear directorio si no existe

    Given: Directorio de salida no existe
    When: Se llama a guardar_reporte_csv
    Then: Crea el directorio y guarda el archivo
    """
    from src.carga import guardar_reporte_csv

    metricas = {"total_ventas": 1000.0}
    fecha = "2025-10-25"

    directorio_nuevo = tmp_path / "nuevo" / "directorio"
    ruta = guardar_reporte_csv(metricas, fecha, directorio_base=str(directorio_nuevo))

    assert os.path.exists(ruta)


def test_guardar_reporte_txt(tmp_path):
    """
    Test: guardar_reporte_txt debe crear archivo TXT legible

    Given: Un dict de métricas y una fecha
    When: Se llama a guardar_reporte_txt
    Then: Crea archivo TXT formateado y retorna la ruta
    """
    from src.carga import guardar_reporte_txt

    metricas = {
        "total_ventas": 1250.50,
        "ticket_promedio": 208.42,
        "cantidad_ventas": 6,
        "top_productos": [
            {"producto": "Laptop", "cantidad": 5},
            {"producto": "Mouse", "cantidad": 10},
        ],
    }
    fecha = "2025-10-25"

    ruta = guardar_reporte_txt(metricas, fecha, directorio_base=str(tmp_path))

    assert os.path.exists(ruta)
    assert ruta.endswith(".txt")

    # Verificar contenido legible
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
        assert "REPORTE DE VENTAS" in contenido
        # El número puede aparecer con o sin ceros decimales y con formato de miles
        assert (
            "1,250.50" in contenido or "1250.50" in contenido or "1,250.5" in contenido
        )


def test_guardar_reporte_txt_formato_humano(tmp_path):
    """
    Test: guardar_reporte_txt debe tener formato legible para humanos

    Given: Métricas con top productos
    When: Se llama a guardar_reporte_txt
    Then: El archivo tiene formato con separadores y secciones claras
    """
    from src.carga import guardar_reporte_txt

    metricas = {
        "total_ventas": 5000.0,
        "ticket_promedio": 250.0,
        "cantidad_ventas": 20,
        "top_productos": [
            {"producto": "Laptop", "cantidad": 5},
            {"producto": "Monitor", "cantidad": 8},
            {"producto": "Teclado", "cantidad": 12},
        ],
    }
    fecha = "2025-10-25"

    ruta = guardar_reporte_txt(metricas, fecha, directorio_base=str(tmp_path))

    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
        # Verificar que tiene secciones
        assert "=" in contenido or "-" in contenido  # Separadores
        assert "TOP" in contenido or "productos" in contenido.lower()


def test_guardar_ambos_reportes_mismo_directorio(tmp_path):
    """
    Test: Guardar CSV y TXT en el mismo directorio con mismo nombre base

    Given: Métricas y fecha
    When: Se llaman ambas funciones
    Then: Se crean ambos archivos con el mismo nombre base
    """
    from src.carga import guardar_reporte_csv, guardar_reporte_txt

    metricas = {"total_ventas": 1000.0}
    fecha = "2025-10-25"

    ruta_csv = guardar_reporte_csv(metricas, fecha, directorio_base=str(tmp_path))
    ruta_txt = guardar_reporte_txt(metricas, fecha, directorio_base=str(tmp_path))

    # Ambos deben existir
    assert os.path.exists(ruta_csv)
    assert os.path.exists(ruta_txt)

    # Deben tener el mismo nombre base
    nombre_csv = Path(ruta_csv).stem
    nombre_txt = Path(ruta_txt).stem
    assert nombre_csv == nombre_txt
