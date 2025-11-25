"""
Tests para el módulo extractor_archivos.

Tests organizados por función, cada uno con:
- Casos felices (happy path)
- Casos borde (edge cases)
- Casos de error (error cases)
"""

from pathlib import Path

import pandas as pd
import pytest

from src.extractor_archivos import (
    convertir_formato_archivo,
    detectar_encoding_archivo,
    leer_csv_con_encoding_auto,
    leer_excel_multiple_sheets,
    leer_json_nested,
    validar_estructura_archivo,
)

# ============================================================================
# Tests para detectar_encoding_archivo
# ============================================================================


class TestDetectarEncodingArchivo:
    """Tests para la función detectar_encoding_archivo."""

    def test_detecta_utf8_correctamente(self, csv_utf8_path):
        """Debe detectar correctamente archivos UTF-8."""
        encoding = detectar_encoding_archivo(csv_utf8_path)
        assert encoding.lower() in ["utf-8", "ascii"]  # ASCII es subset de UTF-8

    def test_detecta_latin1_correctamente(self, csv_latin1_path):
        """Debe detectar correctamente archivos Latin-1."""
        encoding = detectar_encoding_archivo(csv_latin1_path)
        assert encoding.lower() in ["iso-8859-1", "latin-1", "windows-1252"]

    def test_acepta_path_como_string(self, csv_utf8_path):
        """Debe aceptar ruta como string."""
        encoding = detectar_encoding_archivo(str(csv_utf8_path))
        assert isinstance(encoding, str)

    def test_acepta_path_como_pathlib(self, csv_utf8_path):
        """Debe aceptar ruta como Path."""
        encoding = detectar_encoding_archivo(Path(csv_utf8_path))
        assert isinstance(encoding, str)

    def test_lanza_error_si_archivo_no_existe(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError, match="no existe"):
            detectar_encoding_archivo("archivo_inexistente.csv")

    def test_lanza_error_con_archivo_vacio(self, temp_dir):
        """Debe lanzar ValueError con archivo vacío."""
        archivo_vacio = temp_dir / "vacio.txt"
        archivo_vacio.touch()

        with pytest.raises(ValueError, match="confianza"):
            detectar_encoding_archivo(archivo_vacio)


# ============================================================================
# Tests para leer_csv_con_encoding_auto
# ============================================================================


class TestLeerCsvConEncodingAuto:
    """Tests para la función leer_csv_con_encoding_auto."""

    def test_lee_csv_utf8_correctamente(self, csv_utf8_path):
        """Debe leer CSV UTF-8 sin errores."""
        df = leer_csv_con_encoding_auto(csv_utf8_path)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "José" in df["nombre"].values

    def test_lee_csv_latin1_correctamente(self, csv_latin1_path):
        """Debe leer CSV Latin-1 detectando encoding automáticamente."""
        df = leer_csv_con_encoding_auto(csv_latin1_path)

        assert isinstance(df, pd.DataFrame)
        assert "José" in df["nombre"].values
        assert "María" in df["nombre"].values

    def test_acepta_parametros_adicionales(self, temp_dir):
        """Debe aceptar parámetros adicionales de pd.read_csv."""
        csv_path = temp_dir / "test_delim.csv"
        csv_path.write_text("nombre;edad\nAna;28\n", encoding="utf-8")

        df = leer_csv_con_encoding_auto(csv_path, delimiter=";")

        assert len(df.columns) == 2
        assert "nombre" in df.columns

    def test_maneja_valores_nulos(self, temp_dir):
        """Debe manejar valores nulos correctamente."""
        csv_path = temp_dir / "test_nulls.csv"
        csv_path.write_text("nombre,edad\nAna,28\nCarlos,\n", encoding="utf-8")

        df = leer_csv_con_encoding_auto(csv_path)

        assert pd.isna(df.loc[1, "edad"])

    def test_lanza_error_con_archivo_no_csv(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            leer_csv_con_encoding_auto("archivo_que_no_existe.csv")


# ============================================================================
# Tests para leer_json_nested
# ============================================================================


class TestLeerJsonNested:
    """Tests para la función leer_json_nested."""

    def test_lee_json_simple_correctamente(self, json_simple_path):
        """Debe leer JSON simple sin problemas."""
        df = leer_json_nested(json_simple_path, aplanar=False)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "nombre" in df.columns

    def test_aplana_json_nested(self, json_nested_path):
        """Debe aplanar estructuras nested automáticamente."""
        df = leer_json_nested(json_nested_path, aplanar=True)

        assert "usuario.nombre" in df.columns
        assert "usuario.direccion.ciudad" in df.columns

    def test_sin_aplanar_mantiene_estructuras(self, json_nested_path):
        """Sin aplanar, debe mantener estructuras nested."""
        df = leer_json_nested(json_nested_path, aplanar=False)

        assert "usuario" in df.columns
        assert isinstance(df["usuario"][0], dict)

    def test_lee_json_lines(self, temp_dir):
        """Debe leer JSON Lines correctamente."""
        jsonl_path = temp_dir / "test.jsonl"
        contenido = '{"id": 1, "nombre": "Ana"}\n{"id": 2, "nombre": "Carlos"}\n'
        jsonl_path.write_text(contenido, encoding="utf-8")

        df = leer_json_nested(jsonl_path)

        assert len(df) == 2
        assert "nombre" in df.columns

    def test_lanza_error_si_archivo_no_existe(self):
        """Debe lanzar FileNotFoundError si no existe."""
        with pytest.raises(FileNotFoundError, match="no existe"):
            leer_json_nested("inexistente.json")

    def test_lanza_error_con_json_invalido(self, temp_dir):
        """Debe lanzar ValueError con JSON inválido."""
        json_path = temp_dir / "invalido.json"
        json_path.write_text("{ esto no es json válido }", encoding="utf-8")

        with pytest.raises(ValueError, match="JSON válido"):
            leer_json_nested(json_path)


# ============================================================================
# Tests para leer_excel_multiple_sheets
# ============================================================================


class TestLeerExcelMultipleSheets:
    """Tests para la función leer_excel_multiple_sheets."""

    def test_lee_todas_las_hojas_como_diccionario(self, excel_path):
        """Debe leer todas las hojas y retornar diccionario."""
        hojas = leer_excel_multiple_sheets(excel_path, combinar=False)

        assert isinstance(hojas, dict)
        assert "Enero" in hojas
        assert "Febrero" in hojas
        assert isinstance(hojas["Enero"], pd.DataFrame)

    def test_combina_hojas_en_dataframe(self, excel_path):
        """Debe combinar todas las hojas en un DataFrame."""
        df = leer_excel_multiple_sheets(excel_path, combinar=True)

        assert isinstance(df, pd.DataFrame)
        assert "hoja" in df.columns
        assert "Enero" in df["hoja"].values
        assert "Febrero" in df["hoja"].values

    def test_nombre_columna_hoja_personalizado(self, excel_path):
        """Debe permitir personalizar nombre de columna de hoja."""
        df = leer_excel_multiple_sheets(
            excel_path, combinar=True, nombre_columna_hoja="mes"
        )

        assert "mes" in df.columns
        assert "hoja" not in df.columns

    def test_lanza_error_si_archivo_no_existe(self):
        """Debe lanzar FileNotFoundError si no existe."""
        with pytest.raises(FileNotFoundError, match="no existe"):
            leer_excel_multiple_sheets("inexistente.xlsx")


# ============================================================================
# Tests para validar_estructura_archivo
# ============================================================================


class TestValidarEstructuraArchivo:
    """Tests para la función validar_estructura_archivo."""

    def test_retorna_true_si_todas_las_columnas_existen(self, sample_dataframe):
        """Debe retornar True si todas las columnas existen."""
        resultado = validar_estructura_archivo(
            sample_dataframe, ["id", "nombre", "edad"]
        )

        assert resultado is True

    def test_retorna_false_si_faltan_columnas_sin_lanzar_error(self, sample_dataframe):
        """Debe retornar False si faltan columnas (lanzar_error=False)."""
        resultado = validar_estructura_archivo(
            sample_dataframe,
            ["id", "nombre", "email"],  # 'email' no existe
            lanzar_error=False,
        )

        assert resultado is False

    def test_lanza_error_si_faltan_columnas(self, sample_dataframe):
        """Debe lanzar ValueError si faltan columnas."""
        with pytest.raises(ValueError, match="Faltan columnas requeridas"):
            validar_estructura_archivo(
                sample_dataframe, ["id", "nombre", "email"], lanzar_error=True
            )

    def test_mensaje_error_indica_columnas_faltantes(self, sample_dataframe):
        """El mensaje de error debe indicar qué columnas faltan."""
        with pytest.raises(ValueError, match="email"):
            validar_estructura_archivo(sample_dataframe, ["id", "email", "telefono"])

    def test_lanza_type_error_si_no_es_dataframe(self):
        """Debe lanzar TypeError si no es un DataFrame."""
        with pytest.raises(TypeError, match="DataFrame"):
            validar_estructura_archivo([1, 2, 3], ["id"])  # No es DataFrame

    def test_acepta_lista_vacia_de_columnas(self, sample_dataframe):
        """Con lista vacía de columnas, debe retornar True."""
        resultado = validar_estructura_archivo(sample_dataframe, [])
        assert resultado is True


# ============================================================================
# Tests para convertir_formato_archivo
# ============================================================================


class TestConvertirFormatoArchivo:
    """Tests para la función convertir_formato_archivo."""

    def test_convierte_csv_a_json(self, csv_utf8_path, temp_dir):
        """Debe convertir CSV a JSON correctamente."""
        json_path = temp_dir / "output.json"

        convertir_formato_archivo(csv_utf8_path, json_path)

        assert json_path.exists()
        df = pd.read_json(json_path)
        assert len(df) == 2

    def test_convierte_json_a_csv(self, json_simple_path, temp_dir):
        """Debe convertir JSON a CSV correctamente."""
        csv_path = temp_dir / "output.csv"

        convertir_formato_archivo(json_simple_path, csv_path)

        assert csv_path.exists()
        df = pd.read_csv(csv_path)
        assert len(df) == 2

    def test_convierte_csv_a_excel(self, csv_utf8_path, temp_dir):
        """Debe convertir CSV a Excel correctamente."""
        excel_path = temp_dir / "output.xlsx"

        convertir_formato_archivo(csv_utf8_path, excel_path)

        assert excel_path.exists()
        df = pd.read_excel(excel_path)
        assert len(df) == 2

    def test_detecta_formato_destino_de_extension(self, csv_utf8_path, temp_dir):
        """Debe detectar formato de destino de la extensión."""
        json_path = temp_dir / "output.json"

        # No especificamos formato_destino, debe detectarlo
        convertir_formato_archivo(csv_utf8_path, json_path)

        assert json_path.exists()

    def test_formato_destino_explicito(self, csv_utf8_path, temp_dir):
        """Debe respetar formato_destino explícito."""
        output_path = temp_dir / "output.datos"

        convertir_formato_archivo(csv_utf8_path, output_path, formato_destino="json")

        assert output_path.exists()

    def test_crea_directorios_si_no_existen(self, csv_utf8_path, temp_dir):
        """Debe crear directorios si no existen."""
        output_path = temp_dir / "subdir1" / "subdir2" / "output.json"

        convertir_formato_archivo(csv_utf8_path, output_path)

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_lanza_error_si_origen_no_existe(self, temp_dir):
        """Debe lanzar FileNotFoundError si origen no existe."""
        with pytest.raises(FileNotFoundError, match="origen no existe"):
            convertir_formato_archivo("inexistente.csv", temp_dir / "output.json")

    def test_lanza_error_con_formato_no_soportado(self, csv_utf8_path, temp_dir):
        """Debe lanzar ValueError con formato no soportado."""
        output_path = temp_dir / "output.xyz"

        with pytest.raises(ValueError, match="no soportado"):
            convertir_formato_archivo(csv_utf8_path, output_path)


# ============================================================================
# Tests de Integración
# ============================================================================


class TestIntegracion:
    """Tests de integración entre funciones."""

    def test_flujo_completo_csv_validacion_conversion(self, csv_utf8_path, temp_dir):
        """Test del flujo completo: leer CSV, validar, convertir."""
        # 1. Leer CSV
        df = leer_csv_con_encoding_auto(csv_utf8_path)

        # 2. Validar estructura
        es_valido = validar_estructura_archivo(df, ["nombre", "edad", "ciudad"])
        assert es_valido

        # 3. Convertir a JSON
        json_path = temp_dir / "convertido.json"
        convertir_formato_archivo(csv_utf8_path, json_path)

        # 4. Verificar resultado
        df_json = pd.read_json(json_path)
        assert len(df_json) == len(df)
        assert list(df_json.columns) == list(df.columns)
