"""
Tests para el módulo de extracción de datos

Tests siguiendo metodología TDD:
- Red: Tests fallan (funciones no existen aún)
- Green: Implementar funciones para que pasen
- Refactor: Mejorar código
"""

import pandas as pd
import pytest


def test_obtener_ruta_archivo_formato_correcto():
    """
    Test: obtener_ruta_archivo debe retornar ruta en formato correcto

    Given: Una fecha en formato YYYY-MM-DD
    When: Se llama a obtener_ruta_archivo
    Then: Retorna ruta con formato data/input/ventas_YYYY_MM_DD.csv
    """
    from src.extraccion import obtener_ruta_archivo

    fecha = "2025-10-25"
    ruta = obtener_ruta_archivo(fecha)

    assert "ventas_2025_10_25.csv" in ruta
    assert "data" in ruta and "input" in ruta


def test_obtener_ruta_archivo_fecha_invalida():
    """
    Test: obtener_ruta_archivo debe fallar con formato de fecha incorrecto

    Given: Una fecha en formato inválido
    When: Se llama a obtener_ruta_archivo
    Then: Lanza ValueError con mensaje claro
    """
    from src.extraccion import obtener_ruta_archivo

    fecha_invalida = "25/10/2025"  # Formato incorrecto

    with pytest.raises(ValueError, match="Formato de fecha inválido"):
        obtener_ruta_archivo(fecha_invalida)


def test_extraer_ventas_csv_archivo_existe(tmp_path):
    """
    Test: extraer_ventas_csv debe leer CSV correctamente

    Given: Un archivo CSV de ventas válido existe
    When: Se llama a extraer_ventas_csv
    Then: Retorna DataFrame con las columnas esperadas
    """
    from src.extraccion import extraer_ventas_csv

    # Crear CSV de prueba
    csv_path = tmp_path / "ventas_2025_10_25.csv"
    contenido = (
        "venta_id,fecha,cliente_id,producto,categoria,cantidad,"
        "precio_unitario,total\n"
        "1,2025-10-25,C001,Laptop HP,Computadoras,1,599.99,599.99\n"
        "2,2025-10-25,C002,Mouse Logitech,Accesorios,2,19.99,39.98\n"
    )
    csv_path.write_text(contenido)

    # Extraer datos
    df = extraer_ventas_csv(str(csv_path))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "venta_id" in df.columns
    assert "total" in df.columns


def test_extraer_ventas_csv_archivo_no_existe():
    """
    Test: extraer_ventas_csv debe fallar si el archivo no existe

    Given: Una ruta a un archivo que no existe
    When: Se llama a extraer_ventas_csv
    Then: Lanza FileNotFoundError con mensaje claro
    """
    from src.extraccion import extraer_ventas_csv

    ruta_invalida = "data/input/ventas_inexistente.csv"

    with pytest.raises(FileNotFoundError, match="no existe"):
        extraer_ventas_csv(ruta_invalida)


def test_extraer_ventas_csv_archivo_vacio(tmp_path):
    """
    Test: extraer_ventas_csv debe fallar si el archivo está vacío

    Given: Un archivo CSV vacío o solo con headers
    When: Se llama a extraer_ventas_csv
    Then: Lanza ValueError indicando que no hay datos
    """
    from src.extraccion import extraer_ventas_csv

    # Crear CSV vacío (solo headers)
    csv_path = tmp_path / "ventas_vacio.csv"
    contenido = (
        "venta_id,fecha,cliente_id,producto,categoria,cantidad,precio_unitario,total\n"
    )
    csv_path.write_text(contenido)

    with pytest.raises(ValueError, match="archivo está vacío"):
        extraer_ventas_csv(str(csv_path))
