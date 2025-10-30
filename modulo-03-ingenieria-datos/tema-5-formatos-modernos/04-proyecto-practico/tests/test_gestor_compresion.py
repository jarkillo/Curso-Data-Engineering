"""
Tests para gestor_compresion.py

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import gzip
import os
from pathlib import Path

import pandas as pd
import pytest
from src.gestor_compresion import (
    comparar_compresiones,
    comprimir_archivo,
    comprimir_dataframe_memoria,
    descomprimir_archivo,
)


class TestComprimirArchivo:
    """Tests para compresión de archivos."""

    def test_comprimir_con_gzip(self, archivo_csv_temporal, directorio_temporal):
        """Verifica compresión con gzip."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="gzip")

        assert Path(ruta_comprimida).exists()
        assert ruta_comprimida.endswith(".gz")
        # Verificar que está comprimido (tamaño menor)
        tamanio_original = os.path.getsize(archivo_csv_temporal)
        tamanio_comprimido = os.path.getsize(ruta_comprimida)
        assert tamanio_comprimido < tamanio_original

    def test_comprimir_con_bz2(self, archivo_csv_temporal, directorio_temporal):
        """Verifica compresión con bz2."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="bz2")

        assert Path(ruta_comprimida).exists()
        assert ruta_comprimida.endswith(".bz2")

    def test_comprimir_con_xz(self, archivo_csv_temporal, directorio_temporal):
        """Verifica compresión con xz."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="xz")

        assert Path(ruta_comprimida).exists()
        assert ruta_comprimida.endswith(".xz")

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo no existe."""
        with pytest.raises(FileNotFoundError):
            comprimir_archivo("no_existe.csv", algoritmo="gzip")

    def test_error_algoritmo_invalido(self, archivo_csv_temporal):
        """Verifica error con algoritmo inválido."""
        with pytest.raises(ValueError, match="Algoritmo de compresión no soportado"):
            comprimir_archivo(archivo_csv_temporal, algoritmo="algoritmo_invalido")

    def test_retorna_ruta_correcta(self, archivo_csv_temporal):
        """Verifica que retorna la ruta del archivo comprimido."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="gzip")

        assert isinstance(ruta_comprimida, str)
        assert Path(ruta_comprimida).exists()


class TestDescomprimirArchivo:
    """Tests para descompresión de archivos."""

    def test_descomprimir_gzip(self, archivo_csv_temporal):
        """Verifica descompresión de archivo gzip."""
        # Comprimir primero
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="gzip")

        # Descomprimir
        ruta_descomprimida = descomprimir_archivo(ruta_comprimida)

        assert Path(ruta_descomprimida).exists()
        assert not ruta_descomprimida.endswith(".gz")

        # Verificar contenido
        with open(archivo_csv_temporal, "rb") as f_original:
            with open(ruta_descomprimida, "rb") as f_descomprimido:
                assert f_original.read() == f_descomprimido.read()

    def test_descomprimir_bz2(self, archivo_csv_temporal):
        """Verifica descompresión de archivo bz2."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="bz2")
        ruta_descomprimida = descomprimir_archivo(ruta_comprimida)

        assert Path(ruta_descomprimida).exists()

    def test_descomprimir_xz(self, archivo_csv_temporal):
        """Verifica descompresión de archivo xz."""
        ruta_comprimida = comprimir_archivo(archivo_csv_temporal, algoritmo="xz")
        ruta_descomprimida = descomprimir_archivo(ruta_comprimida)

        assert Path(ruta_descomprimida).exists()

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo comprimido no existe."""
        with pytest.raises(FileNotFoundError):
            descomprimir_archivo("no_existe.gz")

    def test_error_formato_no_reconocido(self, archivo_csv_temporal):
        """Verifica error con archivo sin extensión de compresión."""
        with pytest.raises(ValueError, match="Formato de compresión no reconocido"):
            descomprimir_archivo(archivo_csv_temporal)


class TestCompararCompresiones:
    """Tests para comparación de algoritmos de compresión."""

    def test_comparar_multiples_algoritmos(self, archivo_csv_temporal):
        """Verifica comparación de múltiples algoritmos."""
        algoritmos = ["gzip", "bz2", "xz"]

        resultados = comparar_compresiones(archivo_csv_temporal, algoritmos)

        assert isinstance(resultados, dict)
        assert len(resultados) == len(algoritmos)

        for algoritmo in algoritmos:
            assert algoritmo in resultados
            assert "tamanio_original_kb" in resultados[algoritmo]
            assert "tamanio_comprimido_kb" in resultados[algoritmo]
            assert "ratio_compresion" in resultados[algoritmo]
            assert "reduccion_pct" in resultados[algoritmo]
            assert "tiempo_compresion_s" in resultados[algoritmo]

    def test_resultados_tienen_metricas_correctas(self, archivo_csv_temporal):
        """Verifica que los resultados tienen las métricas correctas."""
        resultados = comparar_compresiones(archivo_csv_temporal, ["gzip"])

        metricas = resultados["gzip"]
        assert metricas["tamanio_original_kb"] > 0
        assert metricas["tamanio_comprimido_kb"] > 0
        assert metricas["tamanio_comprimido_kb"] < metricas["tamanio_original_kb"]
        assert metricas["ratio_compresion"] > 1.0
        assert 0 < metricas["reduccion_pct"] < 100
        assert metricas["tiempo_compresion_s"] >= 0

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo no existe."""
        with pytest.raises(FileNotFoundError):
            comparar_compresiones("no_existe.csv", ["gzip"])

    def test_error_lista_vacia_algoritmos(self, archivo_csv_temporal):
        """Verifica error con lista vacía de algoritmos."""
        with pytest.raises(ValueError, match="debe proporcionar al menos un algoritmo"):
            comparar_compresiones(archivo_csv_temporal, [])

    def test_limpieza_archivos_temporales(self, archivo_csv_temporal):
        """Verifica que se limpian archivos temporales después de comparar."""
        directorio = Path(archivo_csv_temporal).parent
        archivos_antes = set(directorio.glob("*"))

        comparar_compresiones(archivo_csv_temporal, ["gzip"])

        archivos_despues = set(directorio.glob("*"))
        # Los archivos comprimidos temporales deberían haberse limpiado
        # (solo debería quedar el archivo original)
        assert archivos_antes == archivos_despues


class TestComprimirDataframeMemoria:
    """Tests para compresión de DataFrame en memoria."""

    def test_comprimir_dataframe_gzip(self, df_ejemplo):
        """Verifica compresión de DataFrame en memoria con gzip."""
        bytes_comprimidos = comprimir_dataframe_memoria(df_ejemplo, algoritmo="gzip")

        assert isinstance(bytes_comprimidos, bytes)
        assert len(bytes_comprimidos) > 0

    def test_comprimir_dataframe_bz2(self, df_ejemplo):
        """Verifica compresión de DataFrame en memoria con bz2."""
        bytes_comprimidos = comprimir_dataframe_memoria(df_ejemplo, algoritmo="bz2")

        assert isinstance(bytes_comprimidos, bytes)
        assert len(bytes_comprimidos) > 0

    def test_bytes_comprimidos_son_menores(self, df_ejemplo):
        """Verifica que los bytes comprimidos son menores que sin comprimir."""
        import io

        # Serializar sin compresión
        buffer_sin = io.BytesIO()
        df_ejemplo.to_csv(buffer_sin, index=False)
        tamanio_sin = len(buffer_sin.getvalue())

        # Comprimir
        bytes_comprimidos = comprimir_dataframe_memoria(df_ejemplo, algoritmo="gzip")
        tamanio_con = len(bytes_comprimidos)

        assert tamanio_con < tamanio_sin

    def test_descomprimir_y_reconstruir(self, df_ejemplo):
        """Verifica que se puede descomprimir y reconstruir el DataFrame."""
        import io

        # Comprimir
        bytes_comprimidos = comprimir_dataframe_memoria(df_ejemplo, algoritmo="gzip")

        # Descomprimir y leer
        buffer_decomprimido = io.BytesIO(gzip.decompress(bytes_comprimidos))
        df_reconstruido = pd.read_csv(buffer_decomprimido)

        assert len(df_reconstruido) == len(df_ejemplo)
        assert list(df_reconstruido.columns) == list(df_ejemplo.columns)

    def test_error_dataframe_vacio(self, df_vacio):
        """Verifica error con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            comprimir_dataframe_memoria(df_vacio, algoritmo="gzip")

    def test_error_algoritmo_invalido(self, df_ejemplo):
        """Verifica error con algoritmo inválido."""
        with pytest.raises(ValueError, match="no soportado"):
            comprimir_dataframe_memoria(df_ejemplo, algoritmo="algoritmo_invalido")
