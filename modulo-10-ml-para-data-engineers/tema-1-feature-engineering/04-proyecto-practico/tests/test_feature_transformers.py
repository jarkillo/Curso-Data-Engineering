"""
Tests para el módulo de transformadores de features.

Estos tests siguen el enfoque TDD: se escriben ANTES de la implementación.
Cubren casos de éxito, edge cases y errores esperados.
"""

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_almost_equal

from src.feature_transformers import (
    cap_outliers,
    detect_outliers_iqr,
    detect_outliers_zscore,
    encode_cyclic,
    encode_onehot,
    encode_ordinal,
    impute_categorical,
    impute_numeric,
    scale_minmax,
    scale_robust,
    scale_standard,
)


class TestEncodeOrdinal:
    """Tests para encode_ordinal."""

    def test_encode_ordinal_basic(self):
        """Debe convertir categorías ordenadas a números."""
        values = ["bajo", "medio", "alto", "medio", "bajo"]
        order = ["bajo", "medio", "alto"]

        result = encode_ordinal(values, order)

        assert result == [0, 1, 2, 1, 0]

    def test_encode_ordinal_with_pandas_series(self):
        """Debe funcionar con pandas Series."""
        values = pd.Series(["a", "b", "c", "a"])
        order = ["a", "b", "c"]

        result = encode_ordinal(values, order)

        assert result == [0, 1, 2, 0]

    def test_encode_ordinal_unknown_category_raises(self):
        """Debe lanzar ValueError si hay categoría desconocida."""
        values = ["bajo", "medio", "DESCONOCIDO"]
        order = ["bajo", "medio", "alto"]

        with pytest.raises(ValueError, match="Categoría desconocida"):
            encode_ordinal(values, order)

    def test_encode_ordinal_empty_list(self):
        """Debe retornar lista vacía para entrada vacía."""
        result = encode_ordinal([], ["a", "b"])
        assert result == []

    def test_encode_ordinal_empty_order_raises(self):
        """Debe lanzar ValueError si el orden está vacío."""
        with pytest.raises(ValueError, match="El orden no puede estar vacío"):
            encode_ordinal(["a"], [])


class TestEncodeOnehot:
    """Tests para encode_onehot."""

    def test_encode_onehot_basic(self):
        """Debe crear columnas binarias para cada categoría."""
        values = ["A", "B", "A", "C"]

        result = encode_onehot(values)

        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["A", "B", "C"]
        assert result.iloc[0].tolist() == [1, 0, 0]  # A
        assert result.iloc[1].tolist() == [0, 1, 0]  # B
        assert result.iloc[3].tolist() == [0, 0, 1]  # C

    def test_encode_onehot_with_prefix(self):
        """Debe añadir prefijo a los nombres de columnas."""
        values = ["rojo", "azul"]

        result = encode_onehot(values, prefix="color")

        assert list(result.columns) == ["color_azul", "color_rojo"]

    def test_encode_onehot_empty_list(self):
        """Debe retornar DataFrame vacío para entrada vacía."""
        result = encode_onehot([])
        assert len(result) == 0


class TestEncodeCyclic:
    """Tests para encode_cyclic."""

    def test_encode_cyclic_hour_midnight(self):
        """Hora 0 y hora 24 deben tener el mismo encoding."""
        sin_0, cos_0 = encode_cyclic(0, 24)
        sin_24, cos_24 = encode_cyclic(24, 24)

        assert_array_almost_equal([sin_0, cos_0], [sin_24, cos_24], decimal=5)

    def test_encode_cyclic_hour_opposite(self):
        """Hora 0 y hora 12 deben tener cosenos opuestos."""
        _, cos_0 = encode_cyclic(0, 24)
        _, cos_12 = encode_cyclic(12, 24)

        assert_array_almost_equal(cos_0, 1.0, decimal=5)
        assert_array_almost_equal(cos_12, -1.0, decimal=5)

    def test_encode_cyclic_day_of_week(self):
        """Debe funcionar para días de la semana (0-6)."""
        sin_0, cos_0 = encode_cyclic(0, 7)  # Lunes
        sin_6, cos_6 = encode_cyclic(6, 7)  # Domingo

        # Deben estar cerca en el espacio cíclico (día 6 está a 1/7 del ciclo de día 0)
        assert abs(cos_0 - cos_6) < 0.5  # Umbral más realista para ciclo de 7

    def test_encode_cyclic_batch(self):
        """Debe procesar múltiples valores."""
        values = [0, 6, 12, 18]

        result = encode_cyclic(values, 24)

        assert result.shape == (4, 2)  # 4 valores, 2 columnas (sin, cos)

    def test_encode_cyclic_max_val_zero_raises(self):
        """Debe lanzar ValueError si max_val es cero."""
        with pytest.raises(ValueError, match="max_val debe ser mayor que cero"):
            encode_cyclic(5, 0)


class TestScaleStandard:
    """Tests para scale_standard."""

    def test_scale_standard_basic(self):
        """Debe escalar a media=0, std=1."""
        values = [10, 20, 30, 40, 50]

        result, params = scale_standard(values)

        assert_array_almost_equal(np.mean(result), 0.0, decimal=5)
        assert_array_almost_equal(np.std(result), 1.0, decimal=5)

    def test_scale_standard_returns_params(self):
        """Debe retornar media y std para uso en producción."""
        values = [10, 20, 30]

        _, params = scale_standard(values)

        assert "mean" in params
        assert "std" in params
        assert params["mean"] == 20.0
        assert_array_almost_equal(params["std"], 8.165, decimal=2)

    def test_scale_standard_apply_params(self):
        """Debe poder aplicar parámetros a nuevos datos."""
        train = [10, 20, 30]
        test = [15, 25]

        _, params = scale_standard(train)
        result = scale_standard(test, params=params)[0]

        # 15 está entre 10 y 20, debería estar entre -1.22 y 0
        assert result[0] < 0
        assert result[0] > -1.5

    def test_scale_standard_empty_raises(self):
        """Debe lanzar ValueError para lista vacía."""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            scale_standard([])

    def test_scale_standard_constant_raises(self):
        """Debe lanzar ValueError si todos los valores son iguales (std=0)."""
        with pytest.raises(ValueError, match="desviación estándar es cero"):
            scale_standard([5, 5, 5, 5])


class TestScaleMinmax:
    """Tests para scale_minmax."""

    def test_scale_minmax_basic(self):
        """Debe escalar a rango [0, 1]."""
        values = [10, 20, 30, 40, 50]

        result, _ = scale_minmax(values)

        assert min(result) == 0.0
        assert max(result) == 1.0

    def test_scale_minmax_custom_range(self):
        """Debe permitir rango personalizado."""
        values = [0, 50, 100]

        result, _ = scale_minmax(values, feature_range=(-1, 1))

        assert result[0] == -1.0
        assert result[1] == 0.0
        assert result[2] == 1.0

    def test_scale_minmax_returns_params(self):
        """Debe retornar min y max para uso en producción."""
        values = [10, 50]

        _, params = scale_minmax(values)

        assert params["min"] == 10
        assert params["max"] == 50


class TestScaleRobust:
    """Tests para scale_robust."""

    def test_scale_robust_with_outlier(self):
        """Debe ser robusto ante outliers."""
        values_normal = [10, 20, 30, 40, 50]
        values_outlier = [10, 20, 30, 40, 50, 1000]

        result_normal, _ = scale_robust(values_normal)
        result_outlier, _ = scale_robust(values_outlier)

        # Los primeros 5 valores deben tener escalados similares
        # aunque haya un outlier
        assert_array_almost_equal(
            result_normal[:5],
            result_outlier[:5],
            decimal=0,  # Permitimos algo de diferencia
        )

    def test_scale_robust_returns_params(self):
        """Debe retornar mediana e IQR."""
        values = [10, 20, 30, 40, 50]

        _, params = scale_robust(values)

        assert "median" in params
        assert "iqr" in params


class TestImputeNumeric:
    """Tests para impute_numeric."""

    def test_impute_numeric_mean(self):
        """Debe imputar con la media."""
        values = [10, np.nan, 30, np.nan, 50]

        result = impute_numeric(values, strategy="mean")

        assert not np.isnan(result).any()
        assert result[1] == 30.0  # (10+30+50)/3

    def test_impute_numeric_median(self):
        """Debe imputar con la mediana."""
        values = [10, np.nan, 30, 40, 50]

        result = impute_numeric(values, strategy="median")

        assert result[1] == 35.0  # mediana de [10, 30, 40, 50]

    def test_impute_numeric_constant(self):
        """Debe imputar con valor constante."""
        values = [10, np.nan, 30]

        result = impute_numeric(values, strategy="constant", fill_value=0)

        assert result[1] == 0

    def test_impute_numeric_all_nan_raises(self):
        """Debe lanzar error si todos son NaN."""
        with pytest.raises(ValueError, match="Todos los valores son NaN"):
            impute_numeric([np.nan, np.nan], strategy="mean")

    def test_impute_numeric_invalid_strategy_raises(self):
        """Debe lanzar error para estrategia inválida."""
        with pytest.raises(ValueError, match="Estrategia no válida"):
            impute_numeric([1, np.nan], strategy="invalid")


class TestImputeCategorical:
    """Tests para impute_categorical."""

    def test_impute_categorical_mode(self):
        """Debe imputar con la moda."""
        values = ["A", None, "B", "A", None, "A"]

        result = impute_categorical(values, strategy="mode")

        assert result[1] == "A"
        assert result[4] == "A"

    def test_impute_categorical_constant(self):
        """Debe imputar con valor constante."""
        values = ["A", None, "B"]

        result = impute_categorical(values, strategy="constant", fill_value="MISSING")

        assert result[1] == "MISSING"

    def test_impute_categorical_preserves_non_null(self):
        """No debe modificar valores no nulos."""
        values = ["A", None, "B"]

        result = impute_categorical(values, strategy="constant", fill_value="X")

        assert result[0] == "A"
        assert result[2] == "B"


class TestDetectOutliersIqr:
    """Tests para detect_outliers_iqr."""

    def test_detect_outliers_iqr_finds_outliers(self):
        """Debe detectar outliers usando IQR."""
        values = np.array([10, 20, 30, 40, 50, 200])  # 200 es outlier

        outliers = detect_outliers_iqr(values)

        assert 200 in values[outliers]
        assert len(values[outliers]) == 1

    def test_detect_outliers_iqr_no_outliers(self):
        """Debe retornar máscara vacía si no hay outliers."""
        values = [10, 20, 30, 40, 50]

        outliers = detect_outliers_iqr(values)

        assert outliers.sum() == 0

    def test_detect_outliers_iqr_custom_multiplier(self):
        """Debe permitir multiplicador personalizado."""
        values = [10, 20, 30, 40, 100]

        # Con multiplier=1.5 (default), 100 es outlier
        outliers_strict = detect_outliers_iqr(values, multiplier=1.5)
        # Con multiplier=3.0, es más permisivo
        outliers_loose = detect_outliers_iqr(values, multiplier=3.0)

        assert outliers_strict.sum() >= outliers_loose.sum()


class TestDetectOutliersZscore:
    """Tests para detect_outliers_zscore."""

    def test_detect_outliers_zscore_finds_outliers(self):
        """Debe detectar outliers usando Z-score."""
        # Crear datos con outlier obvio
        values = [10, 12, 11, 13, 10, 12, 11, 100]

        outliers = detect_outliers_zscore(values, threshold=2)

        assert outliers[-1]  # 100 es outlier

    def test_detect_outliers_zscore_default_threshold(self):
        """Threshold por defecto debe ser 3."""
        values = list(range(100))

        # Con distribución uniforme, ninguno debería ser outlier
        outliers = detect_outliers_zscore(values)

        assert outliers.sum() == 0


class TestCapOutliers:
    """Tests para cap_outliers."""

    def test_cap_outliers_basic(self):
        """Debe limitar valores extremos."""
        values = [10, 20, 30, 40, 1000]

        result = cap_outliers(values, lower_percentile=5, upper_percentile=95)

        assert max(result) < 1000

    def test_cap_outliers_preserves_normal_values(self):
        """No debe modificar valores dentro de los percentiles."""
        values = [10, 20, 30, 40, 50]

        result = cap_outliers(values, lower_percentile=0, upper_percentile=100)

        assert_array_almost_equal(values, result)

    def test_cap_outliers_symmetric(self):
        """Debe aplicar límites tanto superior como inferior."""
        values = [-1000, 10, 20, 30, 1000]

        result = cap_outliers(values, lower_percentile=10, upper_percentile=90)

        assert min(result) > -1000
        assert max(result) < 1000


class TestIntegration:
    """Tests de integración entre funciones."""

    def test_pipeline_encoding_scaling(self):
        """Debe poder encadenar encoding y scaling."""
        # Datos de entrada
        categorias = ["bajo", "medio", "alto"]
        encoded = encode_ordinal(categorias, ["bajo", "medio", "alto"])
        scaled, _ = scale_standard(encoded)

        # El resultado debe estar escalado
        assert_array_almost_equal(np.mean(scaled), 0.0, decimal=5)

    def test_pipeline_impute_then_scale(self):
        """Debe poder imputar y luego escalar."""
        values = [10, np.nan, 30, np.nan, 50]

        imputed = impute_numeric(values, strategy="median")
        scaled, _ = scale_standard(imputed)

        assert not np.isnan(scaled).any()
        assert_array_almost_equal(np.mean(scaled), 0.0, decimal=5)
