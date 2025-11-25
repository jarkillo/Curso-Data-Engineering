"""Tests para el módulo agregador."""

import pandas as pd
import pytest

from src.agregador import (
    agrupar_con_multiples_metricas,
    calcular_porcentajes_por_grupo,
    calcular_top_n_por_grupo,
    crear_tabla_pivot,
    generar_resumen_estadistico,
)


class TestAgruparConMultiplesMetricas:
    """Tests para agrupar_con_multiples_metricas."""

    def test_agrupa_con_una_metrica(self):
        """Debe agrupar y calcular una métrica."""
        df = pd.DataFrame({"categoria": ["A", "A", "B"], "ventas": [100, 200, 150]})
        aggs = {"ventas": ["sum"]}
        resultado = agrupar_con_multiples_metricas(df, ["categoria"], aggs)
        assert len(resultado) == 2
        assert "ventas_sum" in resultado.columns

    def test_agrupa_con_multiples_metricas(self):
        """Debe calcular múltiples métricas."""
        df = pd.DataFrame({"grupo": ["X", "X", "Y"], "valor": [10, 20, 30]})
        aggs = {"valor": ["sum", "mean", "count", "min", "max"]}
        resultado = agrupar_con_multiples_metricas(df, ["grupo"], aggs)
        assert "valor_sum" in resultado.columns
        assert "valor_mean" in resultado.columns
        assert "valor_count" in resultado.columns

    def test_agrupa_multiples_columnas(self):
        """Debe agrupar por múltiples columnas."""
        df = pd.DataFrame(
            {"cat1": ["A", "A", "B"], "cat2": ["X", "Y", "X"], "valor": [10, 20, 30]}
        )
        aggs = {"valor": ["sum"]}
        resultado = agrupar_con_multiples_metricas(df, ["cat1", "cat2"], aggs)
        assert len(resultado) == 3

    def test_error_columna_agrupacion_inexistente(self):
        """Debe lanzar error si columna de agrupación no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="agrupación.*no existe"):
            agrupar_con_multiples_metricas(df, ["b"], {"a": ["sum"]})

    def test_error_columna_agregacion_inexistente(self):
        """Debe lanzar error si columna a agregar no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="agregar.*no existe"):
            agrupar_con_multiples_metricas(df, ["a"], {"b": ["sum"]})

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            agrupar_con_multiples_metricas(df, ["a"], {"b": ["sum"]})


class TestCalcularTopNPorGrupo:
    """Tests para calcular_top_n_por_grupo."""

    def test_calcula_top_n_descendente(self):
        """Debe obtener top N valores más altos por grupo."""
        df = pd.DataFrame(
            {
                "categoria": ["A", "A", "A", "B", "B"],
                "ventas": [100, 200, 150, 250, 180],
            }
        )
        resultado = calcular_top_n_por_grupo(df, "categoria", "ventas", n=2)
        assert len(resultado) == 4  # 2 por cada grupo
        # Verificar que son los más altos
        top_a = resultado[resultado["categoria"] == "A"]["ventas"].tolist()
        assert 200 in top_a
        assert 150 in top_a

    def test_calcula_top_n_ascendente(self):
        """Debe obtener top N valores más bajos por grupo."""
        df = pd.DataFrame({"categoria": ["A", "A", "A"], "ventas": [100, 200, 150]})
        resultado = calcular_top_n_por_grupo(
            df, "categoria", "ventas", n=1, ascendente=True
        )
        assert len(resultado) == 1
        assert resultado["ventas"].iloc[0] == 100

    def test_n_mayor_que_grupo(self):
        """Debe devolver todos si N es mayor que el tamaño del grupo."""
        df = pd.DataFrame({"grupo": ["A", "A"], "valor": [10, 20]})
        resultado = calcular_top_n_por_grupo(df, "grupo", "valor", n=10)
        assert len(resultado) == 2

    def test_error_n_invalido(self):
        """Debe lanzar error si n < 1."""
        df = pd.DataFrame({"a": [1], "b": [2]})
        with pytest.raises(ValueError, match="n debe ser >= 1"):
            calcular_top_n_por_grupo(df, "a", "b", n=0)

    def test_error_columna_inexistente(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            calcular_top_n_por_grupo(df, "b", "a", n=1)

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            calcular_top_n_por_grupo(df, "a", "b", n=1)


class TestCrearTablaPivot:
    """Tests para crear_tabla_pivot."""

    def test_crea_pivot_basica(self):
        """Debe crear tabla pivot básica."""
        df = pd.DataFrame(
            {
                "producto": ["A", "A", "B"],
                "mes": ["Ene", "Feb", "Ene"],
                "ventas": [100, 200, 150],
            }
        )
        resultado = crear_tabla_pivot(df, "producto", "mes", "ventas")
        assert "Ene" in resultado.columns
        assert "Feb" in resultado.columns
        assert len(resultado) == 2  # 2 productos

    def test_usa_funcion_agregacion(self):
        """Debe usar la función de agregación especificada."""
        df = pd.DataFrame(
            {"cat": ["A", "A", "A"], "tipo": ["X", "X", "Y"], "valor": [10, 20, 30]}
        )
        resultado = crear_tabla_pivot(df, "cat", "tipo", "valor", "mean")
        assert resultado.loc[0, "X"] == 15  # Promedio de 10 y 20

    def test_rellena_nulos_con_valor(self):
        """Debe rellenar valores nulos."""
        df = pd.DataFrame(
            {"prod": ["A", "B"], "mes": ["Ene", "Feb"], "ventas": [100, 200]}
        )
        resultado = crear_tabla_pivot(df, "prod", "mes", "ventas", rellenar_nulos=-1)
        # Producto A no tiene ventas en Feb, debe ser -1
        assert resultado.loc[0, "Feb"] == -1

    def test_error_columna_inexistente(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            crear_tabla_pivot(df, "a", "b", "c")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            crear_tabla_pivot(df, "a", "b", "c")


class TestCalcularPorcentajesPorGrupo:
    """Tests para calcular_porcentajes_por_grupo."""

    def test_calcula_porcentajes_correctamente(self):
        """Debe calcular porcentajes respecto al total del grupo."""
        df = pd.DataFrame({"categoria": ["A", "A", "B"], "ventas": [100, 200, 150]})
        resultado = calcular_porcentajes_por_grupo(df, "categoria", "ventas")
        assert "ventas_pct" in resultado.columns
        # A: 100/(100+200) = 33.33%, 200/(100+200) = 66.67%
        assert resultado.loc[0, "ventas_pct"] == pytest.approx(33.33, rel=0.01)
        assert resultado.loc[1, "ventas_pct"] == pytest.approx(66.67, rel=0.01)
        # B: 150/150 = 100%
        assert resultado.loc[2, "ventas_pct"] == 100.0

    def test_suma_100_por_grupo(self):
        """Los porcentajes por grupo deben sumar 100."""
        df = pd.DataFrame(
            {"grupo": ["X", "X", "X", "Y", "Y"], "valor": [10, 20, 30, 40, 60]}
        )
        resultado = calcular_porcentajes_por_grupo(df, "grupo", "valor")
        suma_x = resultado[resultado["grupo"] == "X"]["valor_pct"].sum()
        suma_y = resultado[resultado["grupo"] == "Y"]["valor_pct"].sum()
        assert suma_x == pytest.approx(100.0, rel=0.1)
        assert suma_y == pytest.approx(100.0, rel=0.1)

    def test_no_modifica_dataframe_original(self):
        """No debe modificar el DataFrame original."""
        df = pd.DataFrame({"cat": ["A", "A"], "val": [10, 20]})
        columnas_originales = set(df.columns)
        resultado = calcular_porcentajes_por_grupo(df, "cat", "val")
        assert set(df.columns) == columnas_originales
        assert len(resultado.columns) > len(df.columns)

    def test_error_columna_inexistente(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            calcular_porcentajes_por_grupo(df, "b", "a")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            calcular_porcentajes_por_grupo(df, "a", "b")


class TestGenerarResumenEstadistico:
    """Tests para generar_resumen_estadistico."""

    def test_genera_todas_estadisticas(self):
        """Debe generar todas las estadísticas esperadas."""
        df = pd.DataFrame({"categoria": ["A", "A", "A"], "ventas": [100, 200, 150]})
        resultado = generar_resumen_estadistico(df, "categoria", "ventas")

        columnas_esperadas = [
            "count",
            "sum",
            "mean",
            "median",
            "std",
            "min",
            "max",
            "q25",
            "q75",
            "range",
            "cv",
        ]
        for col in columnas_esperadas:
            assert col in resultado.columns, f"Falta columna {col}"

    def test_calcula_estadisticas_correctamente(self):
        """Debe calcular estadísticas correctamente."""
        df = pd.DataFrame({"grupo": ["X", "X", "X"], "valor": [10, 20, 30]})
        resultado = generar_resumen_estadistico(df, "grupo", "valor")

        assert resultado.loc[0, "count"] == 3
        assert resultado.loc[0, "sum"] == 60
        assert resultado.loc[0, "mean"] == 20
        assert resultado.loc[0, "median"] == 20
        assert resultado.loc[0, "min"] == 10
        assert resultado.loc[0, "max"] == 30
        assert resultado.loc[0, "range"] == 20

    def test_calcula_percentiles(self):
        """Debe calcular percentiles 25 y 75."""
        df = pd.DataFrame({"cat": ["A"] * 4, "val": [10, 20, 30, 40]})
        resultado = generar_resumen_estadistico(df, "cat", "val")
        assert "q25" in resultado.columns
        assert "q75" in resultado.columns
        assert resultado.loc[0, "q25"] == 17.5  # Percentil 25
        assert resultado.loc[0, "q75"] == 32.5  # Percentil 75

    def test_calcula_coeficiente_variacion(self):
        """Debe calcular coeficiente de variación."""
        df = pd.DataFrame({"grupo": ["A", "A"], "valor": [100, 200]})
        resultado = generar_resumen_estadistico(df, "grupo", "valor")
        assert "cv" in resultado.columns
        # CV = (std / mean) * 100
        # std de [100, 200] = 70.71, mean = 150
        cv_esperado = (70.71 / 150) * 100  # 47.14
        assert resultado.loc[0, "cv"] == pytest.approx(cv_esperado, rel=0.1)

    def test_multiples_grupos(self):
        """Debe manejar múltiples grupos."""
        df = pd.DataFrame(
            {"categoria": ["A", "A", "B", "B"], "ventas": [100, 200, 150, 250]}
        )
        resultado = generar_resumen_estadistico(df, "categoria", "ventas")
        assert len(resultado) == 2
        assert resultado["categoria"].tolist() == ["A", "B"]

    def test_error_columna_inexistente(self):
        """Debe lanzar error si alguna columna no existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="no existe"):
            generar_resumen_estadistico(df, "b", "a")

    def test_error_si_dataframe_vacio(self):
        """Debe lanzar error si el DataFrame está vacío."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="no puede estar vacío"):
            generar_resumen_estadistico(df, "a", "b")
