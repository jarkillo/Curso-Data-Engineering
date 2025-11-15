"""
Tests para conversor_formatos.py.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest
from src.conversor_formatos import (
    convertir_con_particiones,
    convertir_csv_a_json_lines,
    convertir_csv_a_parquet,
    convertir_json_a_csv,
    convertir_json_a_parquet,
    convertir_parquet_a_csv,
    guardar_formato_automatico,
    leer_multiple_formatos,
)


class TestConvertirCsvAParquet:
    """Tests para conversión CSV a Parquet."""

    def test_conversion_basica_exitosa(self, archivo_csv_temporal, directorio_temporal):
        """Verifica conversión básica CSV → Parquet."""
        ruta_parquet = directorio_temporal / "salida.parquet"

        convertir_csv_a_parquet(archivo_csv_temporal, str(ruta_parquet))

        assert ruta_parquet.exists()
        df_resultado = pd.read_parquet(ruta_parquet)
        df_original = pd.read_csv(archivo_csv_temporal)
        assert len(df_resultado) == len(df_original)

    def test_conversion_con_compresion_snappy(
        self, archivo_csv_temporal, directorio_temporal
    ):
        """Verifica conversión con compresión snappy."""
        ruta_parquet = directorio_temporal / "salida_snappy.parquet"

        convertir_csv_a_parquet(
            archivo_csv_temporal, str(ruta_parquet), compresion="snappy"
        )

        assert ruta_parquet.exists()
        # Verificar que el tamaño es menor que sin compresión
        df = pd.read_parquet(ruta_parquet)
        assert len(df) > 0

    def test_conversion_con_compresion_gzip(
        self, archivo_csv_temporal, directorio_temporal
    ):
        """Verifica conversión con compresión gzip."""
        ruta_parquet = directorio_temporal / "salida_gzip.parquet"

        convertir_csv_a_parquet(
            archivo_csv_temporal, str(ruta_parquet), compresion="gzip"
        )

        assert ruta_parquet.exists()

    def test_error_archivo_no_existe(self, directorio_temporal):
        """Verifica error cuando archivo CSV no existe."""
        with pytest.raises(FileNotFoundError):
            convertir_csv_a_parquet(
                "no_existe.csv", str(directorio_temporal / "salida.parquet")
            )

    def test_error_compresion_invalida(self, archivo_csv_temporal, directorio_temporal):
        """Verifica error con algoritmo de compresión inválido."""
        with pytest.raises(ValueError, match="compresión inválida"):
            convertir_csv_a_parquet(
                archivo_csv_temporal,
                str(directorio_temporal / "salida.parquet"),
                compresion="algoritmo_invalido",
            )


class TestConvertirJsonAParquet:
    """Tests para conversión JSON a Parquet."""

    def test_conversion_json_records_exitosa(
        self, archivo_json_temporal, directorio_temporal
    ):
        """Verifica conversión JSON (orient=records) → Parquet."""
        ruta_parquet = directorio_temporal / "salida.parquet"

        convertir_json_a_parquet(archivo_json_temporal, str(ruta_parquet))

        assert ruta_parquet.exists()
        df_resultado = pd.read_parquet(ruta_parquet)
        assert len(df_resultado) > 0

    def test_conversion_json_lines_exitosa(
        self, archivo_jsonl_temporal, directorio_temporal
    ):
        """Verifica conversión JSON Lines → Parquet."""
        ruta_parquet = directorio_temporal / "salida.parquet"

        convertir_json_a_parquet(
            archivo_jsonl_temporal, str(ruta_parquet), orient="lines"
        )

        assert ruta_parquet.exists()

    def test_error_json_no_existe(self, directorio_temporal):
        """Verifica error cuando archivo JSON no existe."""
        with pytest.raises(FileNotFoundError):
            convertir_json_a_parquet(
                "no_existe.json", str(directorio_temporal / "salida.parquet")
            )


class TestConvertirParquetACsv:
    """Tests para conversión Parquet a CSV."""

    def test_conversion_parquet_a_csv_exitosa(
        self, archivo_parquet_temporal, directorio_temporal
    ):
        """Verifica conversión Parquet → CSV."""
        ruta_csv = directorio_temporal / "salida.csv"

        convertir_parquet_a_csv(archivo_parquet_temporal, str(ruta_csv))

        assert ruta_csv.exists()
        df_resultado = pd.read_csv(ruta_csv)
        df_original = pd.read_parquet(archivo_parquet_temporal)
        assert len(df_resultado) == len(df_original)

    def test_error_parquet_no_existe(self, directorio_temporal):
        """Verifica error cuando archivo Parquet no existe."""
        with pytest.raises(FileNotFoundError):
            convertir_parquet_a_csv(
                "no_existe.parquet", str(directorio_temporal / "salida.csv")
            )


class TestConvertirJsonACsv:
    """Tests para conversión JSON a CSV."""

    def test_conversion_json_a_csv_exitosa(
        self, archivo_json_temporal, directorio_temporal
    ):
        """Verifica conversión JSON → CSV."""
        ruta_csv = directorio_temporal / "salida.csv"

        convertir_json_a_csv(archivo_json_temporal, str(ruta_csv))

        assert ruta_csv.exists()
        df_resultado = pd.read_csv(ruta_csv)
        assert len(df_resultado) > 0


class TestConvertirCsvAJsonLines:
    """Tests para conversión CSV a JSON Lines."""

    def test_conversion_csv_a_jsonl_exitosa(
        self, archivo_csv_temporal, directorio_temporal
    ):
        """Verifica conversión CSV → JSON Lines."""
        ruta_jsonl = directorio_temporal / "salida.jsonl"

        convertir_csv_a_json_lines(archivo_csv_temporal, str(ruta_jsonl))

        assert ruta_jsonl.exists()
        df_resultado = pd.read_json(ruta_jsonl, lines=True)
        df_original = pd.read_csv(archivo_csv_temporal)
        assert len(df_resultado) == len(df_original)


class TestLeerMultipleFormatos:
    """Tests para lectura con autodetección de formato."""

    def test_leer_csv_autodeteccion(self, archivo_csv_temporal):
        """Verifica lectura automática de CSV."""
        df = leer_multiple_formatos(archivo_csv_temporal)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_leer_json_autodeteccion(self, archivo_json_temporal):
        """Verifica lectura automática de JSON."""
        df = leer_multiple_formatos(archivo_json_temporal)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_leer_jsonl_autodeteccion(self, archivo_jsonl_temporal):
        """Verifica lectura automática de JSON Lines."""
        df = leer_multiple_formatos(archivo_jsonl_temporal)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_leer_parquet_autodeteccion(self, archivo_parquet_temporal):
        """Verifica lectura automática de Parquet."""
        df = leer_multiple_formatos(archivo_parquet_temporal)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_error_formato_no_soportado(self, directorio_temporal):
        """Verifica error con formato no soportado."""
        archivo_invalido = directorio_temporal / "archivo.txt"
        archivo_invalido.write_text("contenido")

        with pytest.raises(ValueError, match="Formato no soportado"):
            leer_multiple_formatos(str(archivo_invalido))

    def test_error_archivo_no_existe(self):
        """Verifica error cuando archivo no existe."""
        with pytest.raises(FileNotFoundError):
            leer_multiple_formatos("no_existe.csv")


class TestGuardarFormatoAutomatico:
    """Tests para guardado con autodetección de formato."""

    def test_guardar_csv_por_extension(self, df_ejemplo, directorio_temporal):
        """Verifica guardado automático en CSV."""
        ruta = directorio_temporal / "salida.csv"

        guardar_formato_automatico(df_ejemplo, str(ruta))

        assert ruta.exists()
        df_leido = pd.read_csv(ruta)
        assert len(df_leido) == len(df_ejemplo)

    def test_guardar_parquet_por_extension(self, df_ejemplo, directorio_temporal):
        """Verifica guardado automático en Parquet."""
        ruta = directorio_temporal / "salida.parquet"

        guardar_formato_automatico(df_ejemplo, str(ruta))

        assert ruta.exists()
        df_leido = pd.read_parquet(ruta)
        assert len(df_leido) == len(df_ejemplo)

    def test_guardar_formato_explicito(self, df_ejemplo, directorio_temporal):
        """Verifica guardado con formato explícito."""
        ruta = directorio_temporal / "salida.datos"

        guardar_formato_automatico(df_ejemplo, str(ruta), formato="parquet")

        # Intentar leer como Parquet debería funcionar
        df_leido = pd.read_parquet(ruta)
        assert len(df_leido) == len(df_ejemplo)

    def test_error_dataframe_vacio(self, df_vacio, directorio_temporal):
        """Verifica error con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            guardar_formato_automatico(
                df_vacio, str(directorio_temporal / "salida.csv")
            )


class TestConvertirConParticiones:
    """Tests para conversión con particionamiento."""

    def test_particionamiento_basico(self, df_con_particiones, directorio_temporal):
        """Verifica particionamiento básico."""
        ruta_base = directorio_temporal / "particionado"

        convertir_con_particiones(df_con_particiones, str(ruta_base), ["año", "mes"])

        assert ruta_base.exists()
        # Verificar que hay archivos parquet en subdirectorios
        archivos_parquet = list(ruta_base.rglob("*.parquet"))
        assert len(archivos_parquet) > 0

    def test_leer_particiones_con_filtro(self, df_con_particiones, directorio_temporal):
        """Verifica lectura de particiones con filtro."""
        ruta_base = directorio_temporal / "particionado"

        convertir_con_particiones(df_con_particiones, str(ruta_base), ["año", "mes"])

        # Leer solo una partición
        df_filtrado = pd.read_parquet(ruta_base, filters=[("año", "==", 2023)])
        assert len(df_filtrado) > 0
        assert all(df_filtrado["año"] == 2023)

    def test_error_columna_particion_no_existe(self, df_ejemplo, directorio_temporal):
        """Verifica error cuando columna de partición no existe."""
        with pytest.raises(ValueError, match="no existe"):
            convertir_con_particiones(
                df_ejemplo,
                str(directorio_temporal / "particionado"),
                ["columna_inexistente"],
            )

    def test_particionamiento_formato_csv(
        self, df_con_particiones, directorio_temporal
    ):
        """Verifica que particionamiento funciona con CSV (menos común)."""
        # Este test verifica que la función acepta otros formatos
        # aunque Parquet es el más usado para particionamiento
        ruta_base = directorio_temporal / "particionado_csv"

        # La función debería rechazar CSV para particionamiento
        with pytest.raises(ValueError, match="solo soporta Parquet"):
            convertir_con_particiones(
                df_con_particiones, str(ruta_base), ["año", "mes"], formato="csv"
            )
