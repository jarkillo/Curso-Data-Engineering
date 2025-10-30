"""Tests para validador_esquema.py - Metodología TDD - Cobertura >90%."""

import pandas as pd
import pytest

# Imports que se implementarán
from src.validador_esquema import (
    generar_reporte_validacion,
    validar_esquema_completo,
    validar_nulls_permitidos,
    validar_rangos_numericos,
    validar_tipos_columnas,
    validar_valores_permitidos,
    validar_valores_unicos,
)


class TestValidarTiposColumnas:
    """Tests para validar_tipos_columnas."""

    def test_tipos_validos(self, df_basico, esquema_basico):
        """Verifica validación correcta con tipos válidos."""
        es_valido, errores = validar_tipos_columnas(df_basico, esquema_basico)

        assert es_valido is True
        assert len(errores) == 0

    def test_tipo_incorrecto(self):
        """Verifica detección de tipo incorrecto."""
        df = pd.DataFrame(
            {"id": ["1", "2", "3"], "nombre": ["A", "B", "C"]}  # String en lugar de int
        )
        esquema = {"id": "int", "nombre": "str"}

        es_valido, errores = validar_tipos_columnas(df, esquema)

        assert es_valido is False
        assert len(errores) > 0
        assert any("id" in error for error in errores)

    def test_columna_faltante(self, df_basico):
        """Verifica detección de columna faltante."""
        esquema = {"id": "int", "columna_inexistente": "str"}

        es_valido, errores = validar_tipos_columnas(df_basico, esquema)

        assert es_valido is False
        assert any("columna_inexistente" in error for error in errores)

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        esquema = {"id": "int"}

        with pytest.raises(ValueError, match="vacío"):
            validar_tipos_columnas(df_vacio, esquema)

    def test_tipo_no_reconocido(self, df_basico):
        """Verifica manejo de tipo no reconocido."""
        esquema = {"id": "tipo_invalido"}

        es_valido, errores = validar_tipos_columnas(df_basico, esquema)

        assert es_valido is False
        assert any("tipo_invalido" in error.lower() for error in errores)


class TestValidarRangosNumericos:
    """Tests para validar_rangos_numericos."""

    def test_rangos_validos(self, df_basico):
        """Verifica validación correcta con rangos válidos."""
        rangos = {"edad": (18, 70), "salario": (1000, 10000)}

        resultado = validar_rangos_numericos(df_basico, rangos)

        assert resultado["es_valido"] is True
        assert len(resultado["errores"]) == 0

    def test_valor_fuera_rango_inferior(self):
        """Verifica detección de valor por debajo del mínimo."""
        df = pd.DataFrame({"edad": [25, 30, 10, 40]})
        rangos = {"edad": (18, 70)}

        resultado = validar_rangos_numericos(df, rangos)

        assert resultado["es_valido"] is False
        assert "edad" in resultado["valores_fuera_rango"]
        assert len(resultado["valores_fuera_rango"]["edad"]) == 1

    def test_valor_fuera_rango_superior(self):
        """Verifica detección de valor por encima del máximo."""
        df = pd.DataFrame({"edad": [25, 30, 150, 40]})
        rangos = {"edad": (18, 70)}

        resultado = validar_rangos_numericos(df, rangos)

        assert resultado["es_valido"] is False
        assert "edad" in resultado["valores_fuera_rango"]

    def test_columna_no_numerica(self):
        """Verifica manejo de columna no numérica."""
        df = pd.DataFrame({"nombre": ["Ana", "Luis", "Pedro"]})
        rangos = {"nombre": (0, 100)}

        resultado = validar_rangos_numericos(df, rangos)

        assert resultado["es_valido"] is False
        assert any("numéric" in error.lower() for error in resultado["errores"])

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        rangos = {"edad": (18, 70)}

        with pytest.raises(ValueError, match="vacío"):
            validar_rangos_numericos(df_vacio, rangos)


class TestValidarValoresUnicos:
    """Tests para validar_valores_unicos."""

    def test_valores_unicos_correctos(self, df_basico):
        """Verifica validación correcta con valores únicos."""
        es_valido, resultado = validar_valores_unicos(df_basico, ["id"])

        assert es_valido is True
        assert resultado["id"]["duplicados"] == 0

    def test_deteccion_duplicados(self, df_con_duplicados):
        """Verifica detección de valores duplicados."""
        es_valido, resultado = validar_valores_unicos(df_con_duplicados, ["id"])

        assert es_valido is False
        assert resultado["id"]["duplicados"] > 0

    def test_multiples_columnas(self):
        """Verifica validación de múltiples columnas."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "email": ["a@test.com", "b@test.com", "c@test.com", "a@test.com"],
            }
        )

        es_valido, resultado = validar_valores_unicos(df, ["id", "email"])

        assert es_valido is False
        assert resultado["id"]["duplicados"] == 0
        assert resultado["email"]["duplicados"] > 0

    def test_columna_no_existe(self, df_basico):
        """Verifica manejo de columna inexistente."""
        with pytest.raises(KeyError, match="no existe"):
            validar_valores_unicos(df_basico, ["columna_inexistente"])


class TestValidarValoresPermitidos:
    """Tests para validar_valores_permitidos."""

    def test_valores_permitidos_correctos(self):
        """Verifica validación correcta con valores permitidos."""
        df = pd.DataFrame({"categoria": ["A", "B", "C", "A", "B"]})
        reglas = {"categoria": ["A", "B", "C"]}

        resultado = validar_valores_permitidos(df, reglas)

        assert resultado["es_valido"] is True
        assert len(resultado["errores"]) == 0

    def test_valores_no_permitidos(self):
        """Verifica detección de valores no permitidos."""
        df = pd.DataFrame({"categoria": ["A", "B", "D", "E"]})
        reglas = {"categoria": ["A", "B", "C"]}

        resultado = validar_valores_permitidos(df, reglas)

        assert resultado["es_valido"] is False
        assert "categoria" in resultado["valores_invalidos"]
        assert "D" in resultado["valores_invalidos"]["categoria"]
        assert "E" in resultado["valores_invalidos"]["categoria"]

    def test_multiples_columnas(self):
        """Verifica validación de múltiples columnas."""
        df = pd.DataFrame(
            {"categoria": ["A", "B", "X"], "estado": ["Activo", "Inactivo", "Invalido"]}
        )
        reglas = {"categoria": ["A", "B", "C"], "estado": ["Activo", "Inactivo"]}

        resultado = validar_valores_permitidos(df, reglas)

        assert resultado["es_valido"] is False
        assert "categoria" in resultado["valores_invalidos"]
        assert "estado" in resultado["valores_invalidos"]


class TestValidarNullsPermitidos:
    """Tests para validar_nulls_permitidos."""

    def test_sin_nulls_en_requeridas(self, df_basico):
        """Verifica validación correcta sin nulls en columnas requeridas."""
        resultado = validar_nulls_permitidos(df_basico, ["id", "nombre"])

        assert resultado["es_valido"] is True
        assert len(resultado["errores"]) == 0

    def test_nulls_en_columnas_requeridas(self, df_con_nulos):
        """Verifica detección de nulls en columnas requeridas."""
        resultado = validar_nulls_permitidos(df_con_nulos, ["id", "nombre", "email"])

        assert resultado["es_valido"] is False
        assert "nombre" in resultado["columnas_con_nulls"]
        assert "email" in resultado["columnas_con_nulls"]

    def test_conteo_nulls(self, df_con_nulos):
        """Verifica conteo correcto de nulls."""
        resultado = validar_nulls_permitidos(df_con_nulos, ["nombre"])

        assert resultado["columnas_con_nulls"]["nombre"] == 1

    def test_columna_no_existe(self, df_basico):
        """Verifica manejo de columna inexistente."""
        with pytest.raises(KeyError, match="no existe"):
            validar_nulls_permitidos(df_basico, ["columna_inexistente"])


class TestValidarEsquemaCompleto:
    """Tests para validar_esquema_completo."""

    def test_esquema_valido_completo(self, df_basico):
        """Verifica validación completa exitosa."""
        config = {
            "tipos": {"id": "int", "nombre": "str", "edad": "int"},
            "rangos": {"edad": (18, 70)},
            "columnas_requeridas": ["id", "nombre"],
            "valores_unicos": ["id"],
        }

        es_valido, reporte = validar_esquema_completo(df_basico, config)

        assert es_valido is True
        assert "validacion_tipos" in reporte
        assert "validacion_rangos" in reporte

    def test_fallo_en_tipos(self):
        """Verifica detección de fallo en validación de tipos."""
        df = pd.DataFrame(
            {"id": ["1", "2", "3"], "nombre": ["A", "B", "C"]}  # String en lugar de int
        )
        config = {"tipos": {"id": "int", "nombre": "str"}}

        es_valido, reporte = validar_esquema_completo(df, config)

        assert es_valido is False
        assert reporte["validacion_tipos"]["es_valido"] is False

    def test_fallo_en_rangos(self):
        """Verifica detección de fallo en validación de rangos."""
        df = pd.DataFrame({"edad": [25, 30, 150]})
        config = {"rangos": {"edad": (18, 70)}}

        es_valido, reporte = validar_esquema_completo(df, config)

        assert es_valido is False
        assert reporte["validacion_rangos"]["es_valido"] is False

    def test_configuracion_vacia(self, df_basico):
        """Verifica manejo de configuración vacía."""
        config = {}

        es_valido, reporte = validar_esquema_completo(df_basico, config)

        # Con configuración vacía, debe ser válido por defecto
        assert es_valido is True


class TestGenerarReporteValidacion:
    """Tests para generar_reporte_validacion."""

    def test_reporte_sin_errores(self):
        """Verifica generación de reporte sin errores."""
        resultados = {
            "validacion_tipos": {"es_valido": True, "errores": []},
            "validacion_rangos": {"es_valido": True, "errores": []},
        }

        reporte = generar_reporte_validacion(resultados)

        assert isinstance(reporte, str)
        assert "exitosa" in reporte.lower() or "correctamente" in reporte.lower()

    def test_reporte_con_errores(self):
        """Verifica generación de reporte con errores."""
        resultados = {
            "validacion_tipos": {
                "es_valido": False,
                "errores": ["Error tipo 1", "Error tipo 2"],
            },
            "validacion_rangos": {"es_valido": False, "errores": ["Error rango 1"]},
        }

        reporte = generar_reporte_validacion(resultados)

        assert isinstance(reporte, str)
        assert "Error tipo 1" in reporte
        assert "Error tipo 2" in reporte
        assert "Error rango 1" in reporte

    def test_reporte_formato_legible(self):
        """Verifica que el reporte es legible."""
        resultados = {"validacion_tipos": {"es_valido": True, "errores": []}}

        reporte = generar_reporte_validacion(resultados)

        # Verificar que tiene estructura (líneas, secciones, etc.)
        assert "\n" in reporte
        assert len(reporte) > 0
