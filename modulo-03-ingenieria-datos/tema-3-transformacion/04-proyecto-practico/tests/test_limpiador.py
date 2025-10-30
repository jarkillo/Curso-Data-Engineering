"""Tests para el módulo limpiador."""

import numpy as np
import pandas as pd
import pytest
from src.limpiador import (
    eliminar_duplicados_completos,
    eliminar_filas_con_errores_criticos,
    eliminar_filas_sin_id,
    normalizar_texto,
    rellenar_valores_nulos,
    validar_rangos_numericos,
)


class TestEliminarDuplicadosCompletos:
    """Tests para eliminar_duplicados_completos."""

    def test_elimina_duplicados_correctamente(self):
        """Debe eliminar filas completamente duplicadas."""
        df = pd.DataFrame({"a": [1, 1, 2, 3], "b": [10, 10, 20, 30]})
        resultado = eliminar_duplicados_completos(df)
        assert len(resultado) == 3
        assert not resultado.duplicated().any()

    def test_no_elimina_si_no_hay_duplicados(self):
        """No debe modificar si no hay duplicados."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
        resultado = eliminar_duplicados_completos(df)
        assert len(resultado) == 3

    def test_resetea_indice(self):
        """Debe resetear el índice después de eliminar."""
        df = pd.DataFrame({"a": [1, 1, 2], "b": [10, 10, 20]})
        resultado = eliminar_duplicados_completos(df)
        assert list(resultado.index) == [0, 1]

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            eliminar_duplicados_completos(df)


class TestEliminarFilasSinId:
    """Tests para eliminar_filas_sin_id."""

    def test_elimina_filas_sin_id(self):
        """Debe eliminar filas con ID nulo."""
        df = pd.DataFrame({"id": [1, None, 3, None, 5], "valor": [10, 20, 30, 40, 50]})
        resultado = eliminar_filas_sin_id(df)
        assert len(resultado) == 3
        assert resultado["id"].isnull().sum() == 0

    def test_no_elimina_si_todos_tienen_id(self):
        """No debe modificar si todos tienen ID."""
        df = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})
        resultado = eliminar_filas_sin_id(df)
        assert len(resultado) == 3

    def test_columna_personalizada(self):
        """Debe funcionar con nombre de columna personalizado."""
        df = pd.DataFrame({"cliente_id": [1, None, 3], "valor": [10, 20, 30]})
        resultado = eliminar_filas_sin_id(df, columna_id="cliente_id")
        assert len(resultado) == 2

    def test_error_si_columna_no_existe(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        with pytest.raises(ValueError, match="no existe"):
            eliminar_filas_sin_id(df, columna_id="id")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            eliminar_filas_sin_id(df)


class TestRellenarValoresNulos:
    """Tests para rellenar_valores_nulos."""

    def test_rellena_con_valor_fijo(self):
        """Debe rellenar con valor fijo."""
        df = pd.DataFrame({"a": [1, None, 3], "b": ["x", None, "z"]})
        estrategias = {"a": 0, "b": "desconocido"}
        resultado = rellenar_valores_nulos(df, estrategias)
        assert resultado["a"].isnull().sum() == 0
        assert resultado["b"].isnull().sum() == 0
        assert resultado.loc[1, "b"] == "desconocido"

    def test_rellena_con_media(self):
        """Debe rellenar con la media."""
        df = pd.DataFrame({"a": [10, None, 30]})
        estrategias = {"a": "mean"}
        resultado = rellenar_valores_nulos(df, estrategias)
        assert resultado.loc[1, "a"] == 20.0

    def test_rellena_con_mediana(self):
        """Debe rellenar con la mediana."""
        df = pd.DataFrame({"a": [10, None, 20, 100]})
        estrategias = {"a": "median"}
        resultado = rellenar_valores_nulos(df, estrategias)
        assert resultado.loc[1, "a"] == 20.0

    def test_rellena_con_moda(self):
        """Debe rellenar con la moda."""
        df = pd.DataFrame({"a": ["x", None, "x", "y"]})
        estrategias = {"a": "mode"}
        resultado = rellenar_valores_nulos(df, estrategias)
        assert resultado.loc[1, "a"] == "x"

    def test_ignora_columnas_inexistentes(self):
        """Debe ignorar columnas que no existen."""
        df = pd.DataFrame({"a": [1, None, 3]})
        estrategias = {"a": 0, "b": 0}  # 'b' no existe
        resultado = rellenar_valores_nulos(df, estrategias)
        assert resultado["a"].isnull().sum() == 0

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            rellenar_valores_nulos(df, {})


class TestNormalizarTexto:
    """Tests para normalizar_texto."""

    def test_normaliza_a_title_case(self):
        """Debe convertir a Title Case."""
        df = pd.DataFrame({"nombre": ["  JUAN  ", "maria", "ANA"]})
        resultado = normalizar_texto(df, ["nombre"], "title")
        assert resultado["nombre"].tolist() == ["Juan", "Maria", "Ana"]

    def test_normaliza_a_minusculas(self):
        """Debe convertir a minúsculas."""
        df = pd.DataFrame({"nombre": ["JUAN", "MARIA"]})
        resultado = normalizar_texto(df, ["nombre"], "lower")
        assert resultado["nombre"].tolist() == ["juan", "maria"]

    def test_normaliza_a_mayusculas(self):
        """Debe convertir a mayúsculas."""
        df = pd.DataFrame({"nombre": ["juan", "maria"]})
        resultado = normalizar_texto(df, ["nombre"], "upper")
        assert resultado["nombre"].tolist() == ["JUAN", "MARIA"]

    def test_elimina_espacios(self):
        """Debe eliminar espacios al inicio y final."""
        df = pd.DataFrame({"nombre": ["  juan  ", "  maria  "]})
        resultado = normalizar_texto(df, ["nombre"], "strip")
        assert resultado["nombre"].tolist() == ["juan", "maria"]

    def test_normaliza_multiples_columnas(self):
        """Debe normalizar múltiples columnas."""
        df = pd.DataFrame({"nombre": ["JUAN"], "apellido": ["PEREZ"]})
        resultado = normalizar_texto(df, ["nombre", "apellido"], "title")
        assert resultado["nombre"].iloc[0] == "Juan"
        assert resultado["apellido"].iloc[0] == "Perez"

    def test_error_si_columna_no_existe(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": ["test"]})
        with pytest.raises(ValueError, match="no existe"):
            normalizar_texto(df, ["b"], "lower")

    def test_error_si_tipo_invalido(self):
        """Debe lanzar error si el tipo de normalización es inválido."""
        df = pd.DataFrame({"a": ["test"]})
        with pytest.raises(TypeError, match="debe ser uno de"):
            normalizar_texto(df, ["a"], "invalido")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            normalizar_texto(df, ["a"], "lower")


class TestValidarRangosNumericos:
    """Tests para validar_rangos_numericos."""

    def test_convierte_fuera_de_rango_a_nan(self):
        """Debe convertir valores fuera de rango a NaN."""
        df = pd.DataFrame({"edad": [25, 150, 30, -5]})
        rangos = {"edad": (0, 120)}
        resultado = validar_rangos_numericos(df, rangos)
        assert pd.isna(resultado.loc[1, "edad"])
        assert pd.isna(resultado.loc[3, "edad"])
        assert resultado.loc[0, "edad"] == 25
        assert resultado.loc[2, "edad"] == 30

    def test_mantiene_valores_en_rango(self):
        """Debe mantener valores dentro del rango."""
        df = pd.DataFrame({"precio": [10, 50, 100]})
        rangos = {"precio": (0, 150)}
        resultado = validar_rangos_numericos(df, rangos)
        assert resultado["precio"].notna().all()

    def test_valida_multiples_columnas(self):
        """Debe validar múltiples columnas."""
        df = pd.DataFrame({"edad": [25, 150], "precio": [100, -10]})
        rangos = {"edad": (0, 120), "precio": (0, 10000)}
        resultado = validar_rangos_numericos(df, rangos)
        assert pd.isna(resultado.loc[1, "edad"])
        assert pd.isna(resultado.loc[1, "precio"])

    def test_convierte_a_numerico(self):
        """Debe convertir strings numéricos a números."""
        df = pd.DataFrame({"valor": ["10", "20", "30"]})
        rangos = {"valor": (0, 25)}
        resultado = validar_rangos_numericos(df, rangos)
        assert resultado["valor"].dtype in [np.float64, float]
        assert pd.isna(resultado.loc[2, "valor"])  # 30 fuera de rango

    def test_error_si_columna_no_existe(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        rangos = {"b": (0, 10)}
        with pytest.raises(ValueError, match="no existe"):
            validar_rangos_numericos(df, rangos)

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            validar_rangos_numericos(df, {})


class TestEliminarFilasConErroresCriticos:
    """Tests para eliminar_filas_con_errores_criticos."""

    def test_elimina_filas_con_nulos_en_criticas(self):
        """Debe eliminar filas con nulos en columnas críticas."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "nombre": ["Ana", None, "Carlos"],
                "email": ["a@test.com", "b@test.com", None],
            }
        )
        resultado = eliminar_filas_con_errores_criticos(df, ["nombre", "email"])
        assert len(resultado) == 1
        assert resultado.loc[0, "nombre"] == "Ana"

    def test_no_elimina_si_no_hay_errores(self):
        """No debe eliminar si no hay nulos en columnas críticas."""
        df = pd.DataFrame({"id": [1, 2, 3], "nombre": ["Ana", "Pedro", "Carlos"]})
        resultado = eliminar_filas_con_errores_criticos(df, ["nombre"])
        assert len(resultado) == 3

    def test_permite_nulos_en_no_criticas(self):
        """Debe permitir nulos en columnas no críticas."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "nombre": ["Ana", "Pedro", "Carlos"],
                "comentario": [None, "Bien", None],
            }
        )
        resultado = eliminar_filas_con_errores_criticos(df, ["nombre"])
        assert len(resultado) == 3

    def test_valida_multiples_columnas_criticas(self):
        """Debe validar múltiples columnas críticas."""
        df = pd.DataFrame(
            {"a": [1, None, 3], "b": [10, 20, None], "c": [100, 200, 300]}
        )
        resultado = eliminar_filas_con_errores_criticos(df, ["a", "b"])
        assert len(resultado) == 1
        assert resultado.loc[0, "a"] == 1

    def test_error_si_columna_no_existe(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        with pytest.raises(ValueError, match="no existe"):
            eliminar_filas_con_errores_criticos(df, ["b"])

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            eliminar_filas_con_errores_criticos(df, ["a"])
