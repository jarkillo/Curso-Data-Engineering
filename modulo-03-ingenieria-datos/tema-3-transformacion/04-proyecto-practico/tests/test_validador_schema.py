"""Tests para el módulo validador_schema."""

import pandas as pd
import pytest

from src.validador_schema import (
    generar_reporte_calidad,
    validar_columnas_requeridas,
    validar_completitud_datos,
    validar_tipos_de_datos,
)


class TestValidarColumnasRequeridas:
    """Tests para validar_columnas_requeridas."""

    def test_valida_todas_columnas_presentes(self):
        """Debe validar correctamente cuando todas las columnas están presentes."""
        df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
        es_valido, faltantes = validar_columnas_requeridas(df, ["a", "b"])
        assert es_valido is True
        assert faltantes == []

    def test_detecta_columnas_faltantes(self):
        """Debe detectar columnas faltantes."""
        df = pd.DataFrame({"a": [1], "b": [2]})
        es_valido, faltantes = validar_columnas_requeridas(df, ["a", "b", "c", "d"])
        assert es_valido is False
        assert set(faltantes) == {"c", "d"}

    def test_valida_todas_faltantes(self):
        """Debe detectar si todas las columnas faltan."""
        df = pd.DataFrame({"x": [1]})
        es_valido, faltantes = validar_columnas_requeridas(df, ["a", "b"])
        assert es_valido is False
        assert set(faltantes) == {"a", "b"}

    def test_lista_vacia_es_valido(self):
        """Debe ser válido si no se requieren columnas."""
        df = pd.DataFrame({"a": [1]})
        es_valido, faltantes = validar_columnas_requeridas(df, [])
        assert es_valido is True
        assert faltantes == []

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            validar_columnas_requeridas(df, ["a"])


class TestValidarTiposDeDatos:
    """Tests para validar_tipos_de_datos."""

    def test_valida_tipos_correctos(self):
        """Debe validar correctamente tipos esperados."""
        df = pd.DataFrame(
            {"edad": [25, 30], "nombre": ["Ana", "Juan"], "activo": [True, False]}
        )
        tipos = {"edad": "int", "nombre": "string", "activo": "bool"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is True
        assert errores == {}

    def test_detecta_tipo_incorrecto(self):
        """Debe detectar tipos incorrectos."""
        df = pd.DataFrame(
            {"edad": ["25", "30"], "precio": [10.5, 20.3]}  # string en vez de int
        )
        tipos = {"edad": "int", "precio": "float"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is False
        assert "edad" in errores
        assert errores["edad"]["esperado"] == "int"

    def test_valida_float(self):
        """Debe validar correctamente tipos float."""
        df = pd.DataFrame({"precio": [10.5, 20.3]})
        tipos = {"precio": "float"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is True

    def test_valida_datetime(self):
        """Debe validar correctamente tipos datetime."""
        df = pd.DataFrame({"fecha": pd.to_datetime(["2024-01-15", "2024-02-20"])})
        tipos = {"fecha": "datetime"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is True

    def test_detecta_columna_inexistente(self):
        """Debe detectar columnas que no existen."""
        df = pd.DataFrame({"a": [1, 2]})
        tipos = {"a": "int", "b": "int"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is False
        assert "b" in errores
        assert errores["b"]["actual"] == "COLUMNA_NO_EXISTE"

    def test_multiples_errores(self):
        """Debe detectar múltiples errores."""
        df = pd.DataFrame({"a": ["texto", "mas_texto"], "b": [1, 2]})
        tipos = {"a": "int", "b": "string", "c": "float"}
        es_valido, errores = validar_tipos_de_datos(df, tipos)
        assert es_valido is False
        assert len(errores) == 3  # a, b, c

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            validar_tipos_de_datos(df, {"a": "int"})


class TestValidarCompletitudDatos:
    """Tests para validar_completitud_datos."""

    def test_valida_completitud_100(self):
        """Debe validar correctamente datos 100% completos."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
        es_valido, completitud = validar_completitud_datos(df, 0.8)
        assert es_valido is True
        assert completitud["a"] == 1.0
        assert completitud["b"] == 1.0

    def test_detecta_completitud_insuficiente(self):
        """Debe detectar completitud insuficiente."""
        df = pd.DataFrame(
            {
                "a": [1, None, None, 4],  # 50% completo
                "b": [10, 20, 30, 40],  # 100% completo
            }
        )
        es_valido, completitud = validar_completitud_datos(df, 0.8)
        assert es_valido is False  # 'a' no cumple el 80%
        assert completitud["a"] == 0.5
        assert completitud["b"] == 1.0

    def test_umbral_personalizado(self):
        """Debe respetar umbral personalizado."""
        df = pd.DataFrame({"a": [1, None, 3]})  # 66.67% completo
        # Con umbral 0.5 debe ser válido
        es_valido1, _ = validar_completitud_datos(df, 0.5)
        assert es_valido1 is True

        # Con umbral 0.9 no debe ser válido
        es_valido2, _ = validar_completitud_datos(df, 0.9)
        assert es_valido2 is False

    def test_todas_columnas_vacias(self):
        """Debe detectar si todas las columnas están vacías."""
        df = pd.DataFrame({"a": [None, None], "b": [None, None]})
        es_valido, completitud = validar_completitud_datos(df, 0.1)
        assert es_valido is False
        assert completitud["a"] == 0.0
        assert completitud["b"] == 0.0

    def test_error_umbral_invalido(self):
        """Debe lanzar error si el umbral es inválido."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="umbral debe estar entre 0 y 1"):
            validar_completitud_datos(df, 1.5)
        with pytest.raises(ValueError, match="umbral debe estar entre 0 y 1"):
            validar_completitud_datos(df, -0.1)

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            validar_completitud_datos(df, 0.8)


class TestGenerarReporteCalidad:
    """Tests para generar_reporte_calidad."""

    def test_genera_metricas_basicas(self):
        """Debe generar métricas básicas."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
        reporte = generar_reporte_calidad(df)

        assert reporte["total_filas"] == 3
        assert reporte["total_columnas"] == 2
        assert "columnas_con_nulos" in reporte
        assert "porcentaje_nulos_total" in reporte
        assert "duplicados_completos" in reporte

    def test_detecta_nulos(self):
        """Debe detectar y reportar valores nulos."""
        df = pd.DataFrame({"a": [1, None, 3], "b": [10, 20, None]})
        reporte = generar_reporte_calidad(df)

        assert reporte["columnas_con_nulos"] == 2
        assert reporte["porcentaje_nulos_total"] > 0

    def test_detecta_duplicados(self):
        """Debe detectar y reportar duplicados."""
        df = pd.DataFrame({"a": [1, 1, 2], "b": [10, 10, 20]})
        reporte = generar_reporte_calidad(df)

        assert reporte["duplicados_completos"] == 1
        assert reporte["porcentaje_duplicados"] > 0

    def test_valida_columnas_requeridas(self):
        """Debe validar columnas requeridas cuando se proporciona."""
        df = pd.DataFrame({"a": [1], "b": [2]})
        reporte = generar_reporte_calidad(df, columnas_requeridas=["a", "b", "c"])

        assert "validacion_columnas" in reporte
        assert reporte["validacion_columnas"]["es_valido"] is False
        assert "c" in reporte["validacion_columnas"]["columnas_faltantes"]
        assert reporte["es_valido"] is False

    def test_valida_tipos_esperados(self):
        """Debe validar tipos cuando se proporciona."""
        df = pd.DataFrame(
            {"edad": ["25", "30"], "nombre": ["Ana", "Juan"]}  # string en vez de int
        )
        reporte = generar_reporte_calidad(
            df, tipos_esperados={"edad": "int", "nombre": "string"}
        )

        assert "validacion_tipos" in reporte
        assert reporte["validacion_tipos"]["es_valido"] is False
        assert "edad" in reporte["validacion_tipos"]["errores"]
        assert reporte["es_valido"] is False

    def test_valida_completitud(self):
        """Debe validar completitud de datos."""
        df = pd.DataFrame(
            {
                "a": [1, None, None, 4],  # 50% completo
                "b": [10, 20, 30, 40],  # 100% completo
            }
        )
        reporte = generar_reporte_calidad(df, umbral_completitud=0.8)

        assert "validacion_completitud" in reporte
        assert reporte["validacion_completitud"]["es_valido"] is False
        assert reporte["es_valido"] is False

    def test_reporte_completo_valido(self):
        """Debe generar reporte completamente válido."""
        df = pd.DataFrame({"id": [1, 2, 3], "nombre": ["Ana", "Juan", "Pedro"]})
        reporte = generar_reporte_calidad(
            df,
            columnas_requeridas=["id", "nombre"],
            tipos_esperados={"id": "int", "nombre": "string"},
            umbral_completitud=0.8,
        )

        assert reporte["es_valido"] is True
        assert reporte["problemas_encontrados"] == []
        assert reporte["validacion_columnas"]["es_valido"] is True
        assert reporte["validacion_tipos"]["es_valido"] is True
        assert reporte["validacion_completitud"]["es_valido"] is True

    def test_identifica_todos_los_problemas(self):
        """Debe identificar todos los problemas encontrados."""
        df = pd.DataFrame({"a": ["texto", None]})  # tipo incorrecto y nulo
        reporte = generar_reporte_calidad(
            df,
            columnas_requeridas=["a", "b"],  # Falta 'b'
            tipos_esperados={"a": "int"},  # 'a' es string
            umbral_completitud=0.9,  # Solo 50% completo
        )

        assert reporte["es_valido"] is False
        assert len(reporte["problemas_encontrados"]) == 3
        assert "columnas_faltantes" in reporte["problemas_encontrados"]
        assert "tipos_incorrectos" in reporte["problemas_encontrados"]
        assert "completitud_insuficiente" in reporte["problemas_encontrados"]

    def test_sin_validaciones_opcionales(self):
        """Debe funcionar sin validaciones opcionales."""
        df = pd.DataFrame({"a": [1, 2]})
        reporte = generar_reporte_calidad(df)

        assert "total_filas" in reporte
        assert "total_columnas" in reporte
        assert "validacion_completitud" in reporte
        assert "validacion_columnas" not in reporte
        assert "validacion_tipos" not in reporte

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            generar_reporte_calidad(df)
