"""
Tests para el módulo de validación de datos.

Tests exhaustivos para validadores.py con >95% cobertura.
"""

import pandas as pd
import pytest
from src.validadores import (
    generar_reporte_validacion,
    validar_columnas_requeridas,
    validar_no_vacio,
    validar_tipos_datos,
    validar_valores_duplicados,
    validar_valores_nulos,
)


class TestValidarNoVacio:
    """Tests para validar_no_vacio."""

    def test_dataframe_con_datos_es_valido(self):
        """El DataFrame con datos debe ser válido."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        resultado = validar_no_vacio(df)

        assert resultado["valido"] is True
        assert resultado["mensaje"] == "OK"
        assert resultado["num_filas"] == 3

    def test_dataframe_vacio_no_es_valido(self):
        """El DataFrame vacío debe fallar validación."""
        df = pd.DataFrame()
        resultado = validar_no_vacio(df)

        assert resultado["valido"] is False
        assert resultado["mensaje"] == "DataFrame vacío"
        assert resultado["num_filas"] == 0

    def test_dataframe_con_una_fila_es_valido(self):
        """El DataFrame con una sola fila debe ser válido."""
        df = pd.DataFrame({"col1": [1]})
        resultado = validar_no_vacio(df)

        assert resultado["valido"] is True
        assert resultado["num_filas"] == 1


class TestValidarColumnasRequeridas:
    """Tests para validar_columnas_requeridas."""

    def test_todas_columnas_presentes_es_valido(self):
        """Cuando todas las columnas están presentes, debe ser válido."""
        df = pd.DataFrame({"nombre": ["Ana"], "edad": [25], "ciudad": ["CDMX"]})
        columnas = ["nombre", "edad", "ciudad"]

        resultado = validar_columnas_requeridas(df, columnas)

        assert resultado["valido"] is True
        assert resultado["mensaje"] == "OK"
        assert resultado["columnas_faltantes"] == []

    def test_columnas_faltantes_no_es_valido(self):
        """Si faltan columnas, debe fallar validación."""
        df = pd.DataFrame({"nombre": ["Ana"], "edad": [25]})
        columnas = ["nombre", "edad", "ciudad", "pais"]

        resultado = validar_columnas_requeridas(df, columnas)

        assert resultado["valido"] is False
        assert "Faltan columnas:" in resultado["mensaje"]
        assert set(resultado["columnas_faltantes"]) == {"ciudad", "pais"}

    def test_columnas_extra_no_causan_error(self):
        """Columnas adicionales no deben causar error."""
        df = pd.DataFrame(
            {"nombre": ["Ana"], "edad": [25], "ciudad": ["CDMX"], "extra": [1]}
        )
        columnas = ["nombre", "edad"]

        resultado = validar_columnas_requeridas(df, columnas)

        assert resultado["valido"] is True

    def test_lista_vacia_de_columnas_es_valido(self):
        """Lista vacía de columnas requeridas debe ser válido."""
        df = pd.DataFrame({"col1": [1]})
        columnas = []

        resultado = validar_columnas_requeridas(df, columnas)

        assert resultado["valido"] is True
        assert resultado["columnas_faltantes"] == []


class TestValidarTiposDatos:
    """Tests para validar_tipos_datos."""

    def test_tipos_correctos_es_valido(self):
        """Tipos de datos correctos deben pasar validación."""
        df = pd.DataFrame(
            {"edad": [25, 30], "nombre": ["Ana", "Luis"], "saldo": [100.5, 200.3]}
        )
        schema = {"edad": int, "nombre": str, "saldo": float}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is True
        assert resultado["mensaje"] == "OK"
        assert resultado["errores"] == []

    def test_tipo_incorrecto_numerico_no_es_valido(self):
        """Columna no numérica cuando se espera int/float debe fallar."""
        df = pd.DataFrame({"edad": ["veinticinco", "treinta"]})
        schema = {"edad": int}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is False
        assert len(resultado["errores"]) == 1
        assert "debe ser numérica" in resultado["errores"][0]

    def test_tipo_incorrecto_string_no_es_valido(self):
        """Columna numérica cuando se espera str debe fallar."""
        df = pd.DataFrame({"nombre": [123, 456]})
        schema = {"nombre": str}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is False
        assert len(resultado["errores"]) == 1
        assert "debe ser string" in resultado["errores"][0]

    def test_columna_no_existe_genera_error(self):
        """Validar columna que no existe debe generar error."""
        df = pd.DataFrame({"edad": [25]})
        schema = {"nombre": str, "edad": int}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is False
        assert any("no existe" in err for err in resultado["errores"])

    def test_multiples_errores_se_reportan(self):
        """Múltiples errores de tipo deben reportarse todos."""
        df = pd.DataFrame({"edad": ["abc"], "saldo": ["xyz"]})
        schema = {"edad": int, "saldo": float}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is False
        assert len(resultado["errores"]) == 2

    def test_schema_vacio_es_valido(self):
        """Schema vacío debe ser válido."""
        df = pd.DataFrame({"col1": [1]})
        schema = {}

        resultado = validar_tipos_datos(df, schema)

        assert resultado["valido"] is True


class TestValidarValoresNulos:
    """Tests para validar_valores_nulos."""

    def test_sin_nulos_es_valido(self):
        """El DataFrame sin nulos debe ser válido."""
        df = pd.DataFrame({"nombre": ["Ana", "Luis"], "edad": [25, 30]})

        resultado = validar_valores_nulos(df)

        assert resultado["valido"] is True
        assert resultado["mensaje"] == "OK"
        assert resultado["errores"] == []
        assert resultado["porcentaje_nulos"] == 0.0

    def test_nulos_en_columna_no_permitida_no_es_valido(self):
        """Nulos en columna que no debe tener nulos debe fallar."""
        df = pd.DataFrame({"id": [1, None, 3], "nombre": ["Ana", "Luis", "Maria"]})
        columnas_no_nulas = ["id"]

        resultado = validar_valores_nulos(df, columnas_no_nulas=columnas_no_nulas)

        assert resultado["valido"] is False
        assert any("id" in err and "nulos" in err for err in resultado["errores"])

    def test_porcentaje_nulos_excede_maximo_no_es_valido(self):
        """Porcentaje de nulos superior al máximo debe fallar."""
        df = pd.DataFrame(
            {
                "col1": [1, None, None],
                "col2": [None, None, 3],
            }
        )
        # 4 nulos de 6 valores = 66.6% > 10%

        resultado = validar_valores_nulos(df, porcentaje_max_nulos=0.1)

        assert resultado["valido"] is False
        assert any("excede máximo" in err for err in resultado["errores"])
        assert resultado["porcentaje_nulos"] > 0.1

    def test_porcentaje_nulos_dentro_rango_es_valido(self):
        """Porcentaje de nulos dentro del rango permitido debe ser válido."""
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": [None, 2, 3, 4, 5],
            }
        )
        # 1 nulo de 10 valores = 10% <= 10%

        resultado = validar_valores_nulos(df, porcentaje_max_nulos=0.1)

        assert resultado["valido"] is True

    def test_columna_no_existe_no_genera_error(self):
        """Validar columna que no existe no debe generar error."""
        df = pd.DataFrame({"col1": [1, 2]})
        columnas_no_nulas = ["col_inexistente"]

        resultado = validar_valores_nulos(df, columnas_no_nulas=columnas_no_nulas)

        # No debe fallar porque la columna no existe
        assert resultado["valido"] is True

    def test_multiples_columnas_sin_nulos(self):
        """Múltiples columnas sin nulos deben ser válidas."""
        df = pd.DataFrame({"id": [1, 2], "nombre": ["Ana", "Luis"], "edad": [25, 30]})
        columnas_no_nulas = ["id", "nombre", "edad"]

        resultado = validar_valores_nulos(df, columnas_no_nulas=columnas_no_nulas)

        assert resultado["valido"] is True


class TestValidarValoresDuplicados:
    """Tests para validar_valores_duplicados."""

    def test_sin_duplicados_es_valido(self):
        """El DataFrame sin duplicados debe ser válido."""
        df = pd.DataFrame({"id": [1, 2, 3], "nombre": ["Ana", "Luis", "Maria"]})

        resultado = validar_valores_duplicados(df)

        assert resultado["valido"]
        assert resultado["mensaje"] == "OK"
        assert resultado["num_duplicados"] == 0

    def test_con_duplicados_completos_no_es_valido(self):
        """Filas completamente duplicadas deben fallar."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 1],
                "nombre": ["Ana", "Luis", "Ana"],
            }
        )

        resultado = validar_valores_duplicados(df)

        assert not resultado["valido"]
        assert resultado["num_duplicados"] == 1
        assert "duplicados" in resultado["mensaje"]

    def test_duplicados_por_columnas_clave_no_es_valido(self):
        """Duplicados en columnas clave específicas deben fallar."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 1],
                "nombre": ["Ana", "Luis", "Maria"],  # Diferentes nombres
            }
        )
        columnas_clave = ["id"]

        resultado = validar_valores_duplicados(df, columnas_clave=columnas_clave)

        assert not resultado["valido"]
        assert resultado["num_duplicados"] == 1

    def test_duplicados_en_otras_columnas_pero_no_clave_es_valido(self):
        """Duplicados en columnas no-clave no deben fallar."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "nombre": ["Ana", "Ana", "Luis"],  # Nombres duplicados
            }
        )
        columnas_clave = ["id"]

        resultado = validar_valores_duplicados(df, columnas_clave=columnas_clave)

        assert resultado["valido"]

    def test_multiples_duplicados_se_cuentan(self):
        """Múltiples filas duplicadas deben contarse correctamente."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 1, 2, 3],
                "nombre": ["Ana", "Luis", "Ana", "Luis", "Maria"],
            }
        )

        resultado = validar_valores_duplicados(df)

        assert not resultado["valido"]
        assert resultado["num_duplicados"] == 2  # 2 duplicados


class TestGenerarReporteValidacion:
    """Tests para generar_reporte_validacion."""

    def test_todas_validaciones_exitosas(self):
        """Reporte con todas validaciones exitosas."""
        df = pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})
        validaciones = {
            "no_vacio": {"valido": True, "mensaje": "OK"},
            "columnas": {"valido": True, "mensaje": "OK"},
            "tipos": {"valido": True, "mensaje": "OK"},
        }

        resultado = generar_reporte_validacion(df, validaciones)

        assert resultado["todo_valido"] is True
        assert resultado["resumen"]["validaciones_exitosas"] == 3
        assert resultado["resumen"]["validaciones_fallidas"] == 0
        assert resultado["resumen"]["porcentaje_exito"] == 1.0
        assert resultado["resumen"]["num_filas"] == 2
        assert resultado["resumen"]["num_columnas"] == 2
        assert resultado["detalle"] == validaciones

    def test_algunas_validaciones_fallidas(self):
        """Reporte con algunas validaciones fallidas."""
        df = pd.DataFrame({"col1": [1]})
        validaciones = {
            "no_vacio": {"valido": True, "mensaje": "OK"},
            "columnas": {"valido": False, "mensaje": "Error"},
            "tipos": {"valido": False, "mensaje": "Error"},
        }

        resultado = generar_reporte_validacion(df, validaciones)

        assert resultado["todo_valido"] is False
        assert resultado["resumen"]["validaciones_exitosas"] == 1
        assert resultado["resumen"]["validaciones_fallidas"] == 2
        assert resultado["resumen"]["porcentaje_exito"] == pytest.approx(
            0.333, abs=0.01
        )

    def test_todas_validaciones_fallidas(self):
        """Reporte con todas validaciones fallidas."""
        df = pd.DataFrame({"col1": [1]})
        validaciones = {
            "val1": {"valido": False, "mensaje": "Error 1"},
            "val2": {"valido": False, "mensaje": "Error 2"},
        }

        resultado = generar_reporte_validacion(df, validaciones)

        assert resultado["todo_valido"] is False
        assert resultado["resumen"]["validaciones_exitosas"] == 0
        assert resultado["resumen"]["validaciones_fallidas"] == 2
        assert resultado["resumen"]["porcentaje_exito"] == 0.0

    def test_sin_validaciones_reporta_correctamente(self):
        """Reporte sin validaciones debe manejar caso vacío."""
        df = pd.DataFrame({"col1": [1, 2]})
        validaciones = {}

        resultado = generar_reporte_validacion(df, validaciones)

        assert resultado["todo_valido"] is True  # No hay validaciones fallidas
        assert resultado["resumen"]["validaciones_exitosas"] == 0
        assert resultado["resumen"]["validaciones_fallidas"] == 0
        assert resultado["resumen"]["porcentaje_exito"] == 0  # División por cero

    def test_dataframe_vacio_reporta_dimensiones(self):
        """Reporte con DataFrame vacío debe reportar dimensiones correctas."""
        df = pd.DataFrame()
        validaciones = {
            "val1": {"valido": True, "mensaje": "OK"},
        }

        resultado = generar_reporte_validacion(df, validaciones)

        assert resultado["resumen"]["num_filas"] == 0
        assert resultado["resumen"]["num_columnas"] == 0
