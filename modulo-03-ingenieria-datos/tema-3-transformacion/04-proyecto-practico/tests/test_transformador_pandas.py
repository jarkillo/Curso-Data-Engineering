"""Tests para el módulo transformador_pandas."""

import pandas as pd
import pytest
from src.transformador_pandas import (
    agregar_metricas_por_grupo,
    aplicar_transformacion_condicional_compleja,
    aplicar_transformacion_por_fila,
    aplicar_ventana_movil,
    calcular_columnas_derivadas,
    categorizar_valores,
    crear_columna_condicional,
    extraer_informacion_temporal,
)


class TestCalcularColumnasDerivadas:
    """Tests para calcular_columnas_derivadas."""

    def test_calcula_columna_suma(self):
        """Debe calcular columna con suma."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
        formulas = {"c": "a + b"}
        resultado = calcular_columnas_derivadas(df, formulas)
        assert "c" in resultado.columns
        assert resultado["c"].tolist() == [11, 22, 33]

    def test_calcula_multiples_columnas(self):
        """Debe calcular múltiples columnas."""
        df = pd.DataFrame({"a": [2, 4], "b": [3, 5]})
        formulas = {"suma": "a + b", "producto": "a * b", "ratio": "a / b"}
        resultado = calcular_columnas_derivadas(df, formulas)
        assert "suma" in resultado.columns
        assert "producto" in resultado.columns
        assert "ratio" in resultado.columns

    def test_error_formula_invalida(self):
        """Debe lanzar error si la fórmula es inválida."""
        df = pd.DataFrame({"a": [1, 2]})
        formulas = {"b": "a + z"}  # 'z' no existe
        with pytest.raises(ValueError, match="Error al evaluar"):
            calcular_columnas_derivadas(df, formulas)

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            calcular_columnas_derivadas(df, {})


class TestAplicarTransformacionPorFila:
    """Tests para aplicar_transformacion_por_fila."""

    def test_aplica_funcion_simple(self):
        """Debe aplicar función simple."""
        df = pd.DataFrame({"precio": [100, 200, 300]})
        resultado = aplicar_transformacion_por_fila(df, "precio", lambda x: x * 1.21)
        assert resultado["precio"].tolist() == [121.0, 242.0, 363.0]

    def test_aplica_funcion_compleja(self):
        """Debe aplicar función con lógica compleja."""
        df = pd.DataFrame({"valor": [10, -5, 20]})

        def transformar(x):
            return x * 2 if x > 0 else 0

        resultado = aplicar_transformacion_por_fila(df, "valor", transformar)
        assert resultado["valor"].tolist() == [20, 0, 40]

    def test_error_columna_inexistente(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            aplicar_transformacion_por_fila(df, "b", lambda x: x * 2)

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            aplicar_transformacion_por_fila(df, "a", lambda x: x)


class TestCategorizarValores:
    """Tests para categorizar_valores."""

    def test_categoriza_correctamente(self):
        """Debe categorizar valores según condiciones."""
        df = pd.DataFrame({"edad": [10, 25, 60, 80]})
        categorias = {
            "Joven": lambda x: x < 30,
            "Adulto": lambda x: 30 <= x < 60,
            "Senior": lambda x: x >= 60,
        }
        resultado = categorizar_valores(df, "edad", "categoria", categorias)
        assert resultado["categoria"].tolist() == ["Joven", "Joven", "Senior", "Senior"]

    def test_usa_otros_si_no_cumple(self):
        """Debe usar 'Otros' si no cumple ninguna condición."""
        df = pd.DataFrame({"valor": [5, 15]})
        categorias = {
            "A": lambda x: x < 10,
        }
        resultado = categorizar_valores(df, "valor", "cat", categorias)
        assert resultado["cat"].tolist() == ["A", "Otros"]

    def test_error_columna_inexistente(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            categorizar_valores(df, "b", "cat", {})

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            categorizar_valores(df, "a", "cat", {})


class TestAgregarMetricasPorGrupo:
    """Tests para agregar_metricas_por_grupo."""

    def test_agrega_media_por_grupo(self):
        """Debe agregar media por grupo."""
        df = pd.DataFrame(
            {"categoria": ["A", "A", "B", "B"], "ventas": [100, 200, 150, 250]}
        )
        resultado = agregar_metricas_por_grupo(df, "categoria", "ventas", ["mean"])
        assert "ventas_mean" in resultado.columns
        assert resultado.loc[0, "ventas_mean"] == 150.0  # Media de A
        assert resultado.loc[2, "ventas_mean"] == 200.0  # Media de B

    def test_agrega_multiples_metricas(self):
        """Debe agregar múltiples métricas."""
        df = pd.DataFrame({"grupo": ["X", "X", "Y"], "valor": [10, 20, 30]})
        resultado = agregar_metricas_por_grupo(
            df, "grupo", "valor", ["mean", "sum", "count"]
        )
        assert "valor_mean" in resultado.columns
        assert "valor_sum" in resultado.columns
        assert "valor_count" in resultado.columns

    def test_error_columna_inexistente(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            agregar_metricas_por_grupo(df, "b", "a", ["mean"])

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            agregar_metricas_por_grupo(df, "a", "b", ["mean"])


class TestAplicarVentanaMovil:
    """Tests para aplicar_ventana_movil."""

    def test_calcula_media_movil(self):
        """Debe calcular media móvil."""
        df = pd.DataFrame({"ventas": [10, 20, 30, 40]})
        resultado = aplicar_ventana_movil(df, "ventas", 2, "mean")
        assert "ventas_rolling_mean" in resultado.columns
        assert pd.isna(resultado.loc[0, "ventas_rolling_mean"])
        assert resultado.loc[1, "ventas_rolling_mean"] == 15.0
        assert resultado.loc[2, "ventas_rolling_mean"] == 25.0

    def test_calcula_suma_movil(self):
        """Debe calcular suma móvil."""
        df = pd.DataFrame({"valor": [5, 10, 15]})
        resultado = aplicar_ventana_movil(df, "valor", 2, "sum")
        assert resultado.loc[1, "valor_rolling_sum"] == 15.0
        assert resultado.loc[2, "valor_rolling_sum"] == 25.0

    def test_diferentes_operaciones(self):
        """Debe soportar diferentes operaciones."""
        df = pd.DataFrame({"x": [10, 20, 30, 40]})
        for op in ["mean", "sum", "std", "min", "max"]:
            resultado = aplicar_ventana_movil(df, "x", 2, op)
            assert f"x_rolling_{op}" in resultado.columns

    def test_error_ventana_invalida(self):
        """Debe lanzar error si la ventana es inválida."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="ventana debe ser >= 1"):
            aplicar_ventana_movil(df, "a", 0, "mean")

    def test_error_operacion_invalida(self):
        """Debe lanzar error si la operación es inválida."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="Operación debe ser"):
            aplicar_ventana_movil(df, "a", 2, "invalida")

    def test_error_columna_inexistente(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            aplicar_ventana_movil(df, "b", 2, "mean")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            aplicar_ventana_movil(df, "a", 2, "mean")


class TestCrearColumnaCondicional:
    """Tests para crear_columna_condicional."""

    def test_crea_columna_con_condiciones(self):
        """Debe crear columna basada en condiciones."""
        df = pd.DataFrame({"precio": [10, 50, 150]})
        condiciones = [(df["precio"] < 50, "Bajo"), (df["precio"] < 100, "Medio")]
        resultado = crear_columna_condicional(df, "rango", condiciones, "Alto")
        assert resultado["rango"].tolist() == ["Bajo", "Medio", "Alto"]

    def test_usa_valor_default(self):
        """Debe usar valor default si no cumple ninguna condición."""
        df = pd.DataFrame({"valor": [100, 200]})
        condiciones = [(df["valor"] < 50, "Pequeño")]
        resultado = crear_columna_condicional(df, "categoria", condiciones, "Grande")
        assert all(resultado["categoria"] == "Grande")

    def test_multiples_condiciones(self):
        """Debe manejar múltiples condiciones."""
        df = pd.DataFrame({"edad": [15, 25, 45, 70]})
        condiciones = [
            (df["edad"] < 18, "Menor"),
            (df["edad"] < 30, "Joven"),
            (df["edad"] < 60, "Adulto"),
        ]
        resultado = crear_columna_condicional(df, "grupo", condiciones, "Senior")
        assert resultado["grupo"].tolist() == ["Menor", "Joven", "Adulto", "Senior"]

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            crear_columna_condicional(df, "nueva", [], None)


class TestExtraerInformacionTemporal:
    """Tests para extraer_informacion_temporal."""

    def test_extrae_year_month(self):
        """Debe extraer año y mes."""
        df = pd.DataFrame({"fecha": pd.to_datetime(["2024-01-15", "2024-02-20"])})
        resultado = extraer_informacion_temporal(df, "fecha", ["year", "month"])
        assert "fecha_year" in resultado.columns
        assert "fecha_month" in resultado.columns
        assert resultado["fecha_year"].tolist() == [2024, 2024]
        assert resultado["fecha_month"].tolist() == [1, 2]

    def test_extrae_dia_y_quarter(self):
        """Debe extraer día y trimestre."""
        df = pd.DataFrame({"fecha": pd.to_datetime(["2024-01-15", "2024-07-20"])})
        resultado = extraer_informacion_temporal(df, "fecha", ["day", "quarter"])
        assert resultado["fecha_day"].tolist() == [15, 20]
        assert resultado["fecha_quarter"].tolist() == [1, 3]

    def test_extrae_weekday(self):
        """Debe extraer nombre del día."""
        df = pd.DataFrame({"fecha": pd.to_datetime(["2024-01-15"])})  # Lunes
        resultado = extraer_informacion_temporal(df, "fecha", ["weekday"])
        assert "fecha_weekday" in resultado.columns

    def test_convierte_string_a_datetime(self):
        """Debe convertir strings a datetime."""
        df = pd.DataFrame({"fecha": ["2024-01-15", "2024-02-20"]})
        resultado = extraer_informacion_temporal(df, "fecha", ["year"])
        assert resultado["fecha_year"].tolist() == [2024, 2024]

    def test_error_componente_invalido(self):
        """Debe lanzar error si el componente es inválido."""
        df = pd.DataFrame({"fecha": pd.to_datetime(["2024-01-15"])})
        with pytest.raises(ValueError, match="no reconocido"):
            extraer_informacion_temporal(df, "fecha", ["invalido"])

    def test_error_columna_inexistente(self):
        """Debe lanzar error si la columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            extraer_informacion_temporal(df, "fecha", ["year"])

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            extraer_informacion_temporal(df, "fecha", ["year"])


class TestAplicarTransformacionCondicionalCompleja:
    """Tests para aplicar_transformacion_condicional_compleja."""

    def test_aplica_funcion_con_multiples_columnas(self):
        """Debe aplicar función que usa múltiples columnas."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})

        def calcular(row):
            return row["a"] + row["b"]

        resultado = aplicar_transformacion_condicional_compleja(df, "suma", calcular)
        assert resultado["suma"].tolist() == [11, 22, 33]

    def test_aplica_logica_condicional(self):
        """Debe aplicar lógica condicional compleja."""
        df = pd.DataFrame({"precio": [100, 200], "descuento": [10, 20]})

        def calcular_total(row):
            if row["descuento"] > 15:
                return row["precio"] * 0.8
            else:
                return row["precio"] * 0.9

        resultado = aplicar_transformacion_condicional_compleja(
            df, "total", calcular_total
        )
        assert resultado["total"].tolist() == [90.0, 160.0]

    def test_maneja_casos_especiales(self):
        """Debe manejar casos especiales en la función."""
        df = pd.DataFrame({"x": [0, 5, 10]})

        def procesar(row):
            return 100 / row["x"] if row["x"] != 0 else 0

        resultado = aplicar_transformacion_condicional_compleja(df, "y", procesar)
        assert resultado["y"].iloc[0] == 0
        assert resultado["y"].iloc[1] == 20.0

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            aplicar_transformacion_condicional_compleja(df, "nueva", lambda x: x)
