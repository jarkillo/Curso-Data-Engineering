"""
Tests para analizador_formatos.py

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import os
from pathlib import Path

import pandas as pd
import pytest
from src.analizador_formatos import (
    benchmark_lectura_escritura,
    comparar_tamanios_formatos,
    detectar_formato_archivo,
    generar_reporte_formato,
    obtener_metadata_parquet,
)


class TestDetectarFormatoArchivo:
    """Tests para detección automática de formato."""

    def test_detectar_csv(self, archivo_csv_temporal):
        """Verifica detección de formato CSV."""
        formato = detectar_formato_archivo(archivo_csv_temporal)
        assert formato == "csv"

    def test_detectar_json(self, archivo_json_temporal):
        """Verifica detección de formato JSON."""
        formato = detectar_formato_archivo(archivo_json_temporal)
        assert formato in [
            "json",
            "jsonl",
        ]  # Puede ser cualquiera dependiendo del contenido

    def test_detectar_jsonl(self, archivo_jsonl_temporal):
        """Verifica detección de formato JSON Lines."""
        formato = detectar_formato_archivo(archivo_jsonl_temporal)
        assert formato == "jsonl"

    def test_detectar_parquet(self, archivo_parquet_temporal):
        """Verifica detección de formato Parquet."""
        formato = detectar_formato_archivo(archivo_parquet_temporal)
        assert formato == "parquet"

    def test_detectar_csv_comprimido(self, archivo_csv_temporal, directorio_temporal):
        """Verifica detección de CSV comprimido (.csv.gz)."""
        import gzip

        ruta_gz = directorio_temporal / "datos.csv.gz"
        with open(archivo_csv_temporal, "rb") as f_in:
            with gzip.open(ruta_gz, "wb") as f_out:
                f_out.write(f_in.read())

        formato = detectar_formato_archivo(str(ruta_gz))
        assert formato == "csv"

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo no existe."""
        with pytest.raises(FileNotFoundError):
            detectar_formato_archivo("no_existe.csv")

    def test_error_formato_no_soportado(self, directorio_temporal):
        """Verifica error con formato no soportado."""
        archivo_txt = directorio_temporal / "archivo.txt"
        archivo_txt.write_text("contenido")

        with pytest.raises(ValueError, match="Formato no soportado"):
            detectar_formato_archivo(str(archivo_txt))


class TestObtenerMetadataParquet:
    """Tests para obtención de metadata de archivos Parquet."""

    def test_metadata_basica(self, archivo_parquet_temporal):
        """Verifica obtención de metadata básica."""
        metadata = obtener_metadata_parquet(archivo_parquet_temporal)

        assert isinstance(metadata, dict)
        assert "num_filas" in metadata
        assert "num_columnas" in metadata
        assert "columnas" in metadata
        assert "tamanio_archivo_mb" in metadata
        assert "compresion" in metadata

    def test_metadata_columnas_correctas(self, df_ejemplo, directorio_temporal):
        """Verifica que las columnas en metadata son correctas."""
        ruta_parquet = directorio_temporal / "datos.parquet"
        df_ejemplo.to_parquet(ruta_parquet, index=False)

        metadata = obtener_metadata_parquet(str(ruta_parquet))

        assert metadata["num_columnas"] == len(df_ejemplo.columns)
        assert set(metadata["columnas"]) == set(df_ejemplo.columns)

    def test_metadata_num_filas_correcto(self, df_ejemplo, directorio_temporal):
        """Verifica que el número de filas en metadata es correcto."""
        ruta_parquet = directorio_temporal / "datos.parquet"
        df_ejemplo.to_parquet(ruta_parquet, index=False)

        metadata = obtener_metadata_parquet(str(ruta_parquet))

        assert metadata["num_filas"] == len(df_ejemplo)

    def test_metadata_incluye_tipos(self, archivo_parquet_temporal):
        """Verifica que metadata incluye tipos de datos."""
        metadata = obtener_metadata_parquet(archivo_parquet_temporal)

        assert "tipos_datos" in metadata
        assert isinstance(metadata["tipos_datos"], dict)

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo Parquet no existe."""
        with pytest.raises(FileNotFoundError):
            obtener_metadata_parquet("no_existe.parquet")

    def test_error_archivo_no_es_parquet(self, archivo_csv_temporal):
        """Verifica error cuando archivo no es Parquet."""
        with pytest.raises(Exception):  # PyArrow lanzará error
            obtener_metadata_parquet(archivo_csv_temporal)


class TestCompararTamaniosFormatos:
    """Tests para comparación de tamaños entre formatos."""

    def test_comparar_formatos_basicos(self, df_ejemplo):
        """Verifica comparación de tamaños entre formatos."""
        resultados = comparar_tamanios_formatos(df_ejemplo)

        assert isinstance(resultados, dict)
        assert "csv" in resultados
        assert "json" in resultados
        assert "jsonl" in resultados
        assert "parquet_snappy" in resultados

    def test_todos_formatos_tienen_tamanio(self, df_ejemplo):
        """Verifica que todos los formatos tienen tamaño en KB."""
        resultados = comparar_tamanios_formatos(df_ejemplo)

        for formato, tamanio in resultados.items():
            assert isinstance(tamanio, (int, float))
            assert tamanio > 0

    def test_parquet_es_mas_pequenio_que_csv(self, df_ejemplo):
        """Verifica que Parquet es más pequeño que CSV."""
        resultados = comparar_tamanios_formatos(df_ejemplo)

        assert resultados["parquet_snappy"] < resultados["csv"]

    def test_json_es_mas_grande_que_csv(self, df_ejemplo):
        """Verifica que JSON típicamente es más grande que CSV."""
        resultados = comparar_tamanios_formatos(df_ejemplo)

        # JSON suele ser más grande que CSV por la verbosidad
        assert resultados["json"] > resultados["csv"]

    def test_error_dataframe_vacio(self, df_vacio):
        """Verifica error con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            comparar_tamanios_formatos(df_vacio)


class TestBenchmarkLecturaEscritura:
    """Tests para benchmark de lectura/escritura."""

    def test_benchmark_formatos_basicos(self, df_ejemplo):
        """Verifica benchmark de formatos básicos."""
        formatos = ["csv", "parquet"]

        df_resultados = benchmark_lectura_escritura(df_ejemplo, formatos)

        assert isinstance(df_resultados, pd.DataFrame)
        assert len(df_resultados) == len(formatos)
        assert "formato" in df_resultados.columns
        assert "tiempo_escritura_s" in df_resultados.columns
        assert "tiempo_lectura_s" in df_resultados.columns
        assert "tamanio_kb" in df_resultados.columns

    def test_benchmark_todos_formatos(self, df_ejemplo):
        """Verifica benchmark con todos los formatos."""
        formatos = ["csv", "json", "jsonl", "parquet"]

        df_resultados = benchmark_lectura_escritura(df_ejemplo, formatos)

        assert len(df_resultados) == len(formatos)
        for formato in formatos:
            assert formato in df_resultados["formato"].values

    def test_tiempos_son_positivos(self, df_ejemplo):
        """Verifica que todos los tiempos son positivos."""
        df_resultados = benchmark_lectura_escritura(df_ejemplo, ["csv", "parquet"])

        assert all(df_resultados["tiempo_escritura_s"] > 0)
        assert all(df_resultados["tiempo_lectura_s"] > 0)

    def test_tamanios_son_positivos(self, df_ejemplo):
        """Verifica que todos los tamaños son positivos."""
        df_resultados = benchmark_lectura_escritura(df_ejemplo, ["csv", "parquet"])

        assert all(df_resultados["tamanio_kb"] > 0)

    def test_error_formato_no_soportado(self, df_ejemplo):
        """Verifica error con formato no soportado."""
        with pytest.raises(ValueError, match="no soportado"):
            benchmark_lectura_escritura(df_ejemplo, ["formato_invalido"])

    def test_error_dataframe_vacio(self, df_vacio):
        """Verifica error con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            benchmark_lectura_escritura(df_vacio, ["csv"])


class TestGenerarReporteFormato:
    """Tests para generación de reporte completo de formato."""

    def test_reporte_csv(self, archivo_csv_temporal):
        """Verifica generación de reporte para CSV."""
        reporte = generar_reporte_formato(archivo_csv_temporal)

        assert isinstance(reporte, dict)
        assert "formato" in reporte
        assert "tamanio_mb" in reporte
        assert "num_registros" in reporte
        assert "num_columnas" in reporte
        assert reporte["formato"] == "csv"

    def test_reporte_parquet(self, archivo_parquet_temporal):
        """Verifica generación de reporte para Parquet."""
        reporte = generar_reporte_formato(archivo_parquet_temporal)

        assert reporte["formato"] == "parquet"
        assert "compresion" in reporte
        assert "metadata_parquet" in reporte

    def test_reporte_json(self, archivo_json_temporal):
        """Verifica generación de reporte para JSON."""
        reporte = generar_reporte_formato(archivo_json_temporal)

        assert reporte["formato"] in ["json", "jsonl"]
        assert reporte["num_registros"] > 0

    def test_reporte_incluye_columnas(self, archivo_csv_temporal):
        """Verifica que el reporte incluye información de columnas."""
        reporte = generar_reporte_formato(archivo_csv_temporal)

        assert "columnas" in reporte
        assert isinstance(reporte["columnas"], list)
        assert len(reporte["columnas"]) > 0

    def test_reporte_incluye_tipos_datos(self, archivo_parquet_temporal):
        """Verifica que el reporte incluye tipos de datos."""
        reporte = generar_reporte_formato(archivo_parquet_temporal)

        assert "tipos_datos" in reporte
        assert isinstance(reporte["tipos_datos"], dict)

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo no existe."""
        with pytest.raises(FileNotFoundError):
            generar_reporte_formato("no_existe.csv")
