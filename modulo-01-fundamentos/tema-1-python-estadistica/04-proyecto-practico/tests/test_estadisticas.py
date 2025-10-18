"""
Tests para el módulo de estadísticas.

Implementación siguiendo TDD (Test-Driven Development):
Los tests se escriben ANTES de implementar las funciones.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest  # noqa: E402
from estadisticas import (  # noqa: E402
    calcular_media,
    calcular_mediana,
    calcular_moda,
    calcular_varianza,
    calcular_desviacion_estandar,
    calcular_percentiles,
)


class TestCalcularMedia:
    """Tests para la función calcular_media()."""

    def test_media_lista_simple(self):
        """Test con una lista simple de números positivos."""
        datos = [1.0, 2.0, 3.0, 4.0, 5.0]
        resultado = calcular_media(datos)
        assert resultado == 3.0, "La media de [1,2,3,4,5] debe ser 3.0"

    def test_media_lista_un_elemento(self):
        """Test con una lista de un solo elemento."""
        datos = [42.0]
        resultado = calcular_media(datos)
        assert resultado == 42.0, "La media de un solo elemento debe ser ese elemento"

    def test_media_numeros_negativos(self):
        """Test con números negativos."""
        datos = [-1.0, -2.0, -3.0, -4.0, -5.0]
        resultado = calcular_media(datos)
        assert resultado == -3.0, "La media debe funcionar con números negativos"

    def test_media_numeros_mixtos(self):
        """Test con números positivos y negativos."""
        datos = [-10.0, 10.0, -5.0, 5.0]
        resultado = calcular_media(datos)
        assert resultado == 0.0, "La media de números balanceados debe ser 0"

    def test_media_numeros_decimales(self):
        """Test con números decimales."""
        datos = [1.5, 2.5, 3.5]
        resultado = calcular_media(datos)
        assert (
            abs(resultado - 2.5) < 0.0001
        ), "La media debe manejar decimales correctamente"

    def test_media_lista_vacia_lanza_error(self):
        """Test que verifica que una lista vacía lanza ValueError."""
        with pytest.raises(ValueError, match="La lista de datos no puede estar vacía"):
            calcular_media([])

    def test_media_none_lanza_error(self):
        """Test que verifica que None lanza TypeError."""
        with pytest.raises(TypeError, match="Los datos deben ser una lista"):
            calcular_media(None)  # type: ignore

    def test_media_no_lista_lanza_error(self):
        """Test que verifica que un tipo incorrecto lanza TypeError."""
        with pytest.raises(TypeError, match="Los datos deben ser una lista"):
            calcular_media("no es una lista")  # type: ignore

    def test_media_valores_no_numericos_lanza_error(self):
        """Test que verifica que valores no numéricos lanzan TypeError."""
        with pytest.raises(TypeError, match="Todos los elementos deben ser números"):
            calcular_media([1, 2, "tres", 4])  # type: ignore

    def test_media_con_none_en_lista_lanza_error(self):
        """Test que verifica que None dentro de la lista lanza TypeError."""
        with pytest.raises(TypeError, match="Todos los elementos deben ser números"):
            calcular_media([1.0, 2.0, None, 4.0])  # type: ignore

    def test_media_ejemplo_real_ventas(self):
        """
        Test con ejemplo real: ventas diarias de un restaurante (Yurest).

        Caso de uso: Calcular la venta promedio de una semana.
        """
        ventas_semana = [150.50, 180.75, 200.00, 165.25, 195.80, 210.50, 175.30]
        resultado = calcular_media(ventas_semana)
        esperado = sum(ventas_semana) / len(ventas_semana)
        assert abs(resultado - esperado) < 0.01, "La media de ventas debe ser correcta"

    def test_media_numeros_muy_grandes(self):
        """Test con números muy grandes para verificar precisión."""
        datos = [1e10, 2e10, 3e10]
        resultado = calcular_media(datos)
        assert abs(resultado - 2e10) < 1e5, "Debe manejar números grandes correctamente"

    def test_media_numeros_muy_pequenos(self):
        """Test con números muy pequeños."""
        datos = [0.0001, 0.0002, 0.0003]
        resultado = calcular_media(datos)
        assert abs(resultado - 0.0002) < 0.000001, "Debe manejar números pequeños"

    def test_media_con_ceros(self):
        """Test con ceros en la lista."""
        datos = [0.0, 0.0, 0.0, 5.0, 10.0]
        resultado = calcular_media(datos)
        assert resultado == 3.0, "Debe manejar ceros correctamente"

    def test_media_acepta_enteros(self):
        """Test que verifica que acepta enteros y devuelve float."""
        datos = [1, 2, 3, 4, 5]
        resultado = calcular_media(datos)
        assert isinstance(resultado, float), "Debe devolver float"
        assert resultado == 3.0


class TestCalcularMediana:
    """Tests para la función calcular_mediana()."""

    def test_mediana_lista_impar(self):
        """Test con una lista de cantidad impar de elementos."""
        datos = [1.0, 2.0, 3.0, 4.0, 5.0]
        resultado = calcular_mediana(datos)
        assert resultado == 3.0, "La mediana de [1,2,3,4,5] debe ser 3.0"

    def test_mediana_lista_par(self):
        """Test con una lista de cantidad par de elementos."""
        datos = [1.0, 2.0, 3.0, 4.0]
        resultado = calcular_mediana(datos)
        assert resultado == 2.5, "La mediana de [1,2,3,4] debe ser (2+3)/2 = 2.5"

    def test_mediana_lista_desordenada(self):
        """Test que verifica que ordena la lista antes de calcular."""
        datos = [5.0, 1.0, 3.0, 2.0, 4.0]
        resultado = calcular_mediana(datos)
        assert resultado == 3.0, "Debe ordenar la lista antes de calcular"

    def test_mediana_un_elemento(self):
        """Test con un solo elemento."""
        datos = [42.0]
        resultado = calcular_mediana(datos)
        assert resultado == 42.0

    def test_mediana_dos_elementos(self):
        """Test con dos elementos."""
        datos = [10.0, 20.0]
        resultado = calcular_mediana(datos)
        assert resultado == 15.0, "La mediana de dos elementos es su promedio"

    def test_mediana_numeros_negativos(self):
        """Test con números negativos."""
        datos = [-5.0, -3.0, -1.0, 0.0, 1.0]
        resultado = calcular_mediana(datos)
        assert resultado == -1.0

    def test_mediana_con_duplicados(self):
        """Test con valores duplicados."""
        datos = [1.0, 2.0, 2.0, 3.0, 4.0]
        resultado = calcular_mediana(datos)
        assert resultado == 2.0

    def test_mediana_lista_vacia_lanza_error(self):
        """Test que verifica que una lista vacía lanza ValueError."""
        with pytest.raises(ValueError, match="La lista de datos no puede estar vacía"):
            calcular_mediana([])

    def test_mediana_none_lanza_error(self):
        """Test que verifica que None lanza TypeError."""
        with pytest.raises(TypeError, match="Los datos deben ser una lista"):
            calcular_mediana(None)  # type: ignore

    def test_mediana_valores_no_numericos_lanza_error(self):
        """Test que verifica que valores no numéricos lanzan TypeError."""
        with pytest.raises(TypeError, match="Todos los elementos deben ser números"):
            calcular_mediana([1, 2, "tres", 4])  # type: ignore

    def test_mediana_no_modifica_lista_original(self):
        """Test que verifica que la función no modifica la lista original."""
        datos = [5.0, 1.0, 3.0, 2.0, 4.0]
        datos_originales = datos.copy()
        calcular_mediana(datos)
        assert datos == datos_originales, "No debe modificar la lista original"

    def test_mediana_ejemplo_real_tiempos_respuesta(self):
        """
        Test con ejemplo real: tiempos de respuesta de API (en ms).

        Caso de uso: En Agora/Yurest, la mediana es mejor que la media
        para medir tiempos de respuesta porque no se ve afectada por
        outliers (peticiones muy lentas ocasionales).
        """
        tiempos_ms = [10.0, 12.0, 15.0, 18.0, 20.0, 25.0, 500.0]
        resultado = calcular_mediana(tiempos_ms)
        assert resultado == 18.0, "La mediana no se ve afectada por el outlier (500ms)"

        # Comparar con media para demostrar la diferencia
        media = calcular_media(tiempos_ms)
        assert media > 80, "La media sí se ve muy afectada por el outlier"

    def test_mediana_numeros_decimales_precision(self):
        """Test con números decimales y verificación de precisión."""
        datos = [1.1, 2.2, 3.3, 4.4, 5.5]
        resultado = calcular_mediana(datos)
        assert abs(resultado - 3.3) < 0.0001


class TestCalcularModa:
    """Tests para la función calcular_moda()."""

    def test_moda_unica(self):
        """Test con una única moda clara."""
        datos = [1.0, 2.0, 2.0, 2.0, 3.0, 4.0]
        resultado = calcular_moda(datos)
        assert resultado == [2.0], "La moda debe ser [2.0]"

    def test_moda_multiple(self):
        """Test con múltiples modas (bimodal)."""
        datos = [1.0, 1.0, 2.0, 2.0, 3.0]
        resultado = calcular_moda(datos)
        assert sorted(resultado) == [1.0, 2.0], "Debe devolver ambas modas"

    def test_moda_todos_unicos(self):
        """Test cuando todos los valores aparecen la misma cantidad de veces."""
        datos = [1.0, 2.0, 3.0, 4.0, 5.0]
        resultado = calcular_moda(datos)
        assert sorted(resultado) == [1.0, 2.0, 3.0, 4.0, 5.0], "Todos son modas"

    def test_moda_un_elemento(self):
        """Test con un solo elemento."""
        datos = [42.0]
        resultado = calcular_moda(datos)
        assert resultado == [42.0]

    def test_moda_todos_iguales(self):
        """Test cuando todos los elementos son iguales."""
        datos = [5.0, 5.0, 5.0, 5.0]
        resultado = calcular_moda(datos)
        assert resultado == [5.0]

    def test_moda_lista_vacia_lanza_error(self):
        """Test que verifica que una lista vacía lanza ValueError."""
        with pytest.raises(ValueError):
            calcular_moda([])

    def test_moda_none_lanza_error(self):
        """Test que verifica que None lanza TypeError."""
        with pytest.raises(TypeError):
            calcular_moda(None)  # type: ignore

    def test_moda_ejemplo_real_productos(self):
        """
        Test con ejemplo real: productos más vendidos.

        Caso de uso: En Yurest, identificar el producto más pedido.
        """
        # IDs de productos vendidos en un día
        productos = [101, 102, 101, 103, 101, 102, 104]
        resultado = calcular_moda(productos)
        assert resultado == [101], "El producto 101 es el más vendido"


class TestCalcularVarianza:
    """Tests para la función calcular_varianza()."""

    def test_varianza_basica(self):
        """Test con valores conocidos."""
        datos = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        resultado = calcular_varianza(datos)
        # Varianza poblacional de estos datos es 4.0
        assert abs(resultado - 4.0) < 0.0001

    def test_varianza_sin_variacion(self):
        """Test cuando todos los valores son iguales (varianza = 0)."""
        datos = [5.0, 5.0, 5.0, 5.0]
        resultado = calcular_varianza(datos)
        assert resultado == 0.0, "La varianza debe ser 0 cuando no hay variación"

    def test_varianza_dos_valores(self):
        """Test con dos valores."""
        datos = [1.0, 3.0]
        resultado = calcular_varianza(datos)
        # Varianza = ((1-2)^2 + (3-2)^2) / 2 = (1 + 1) / 2 = 1.0
        assert abs(resultado - 1.0) < 0.0001

    def test_varianza_lista_vacia_lanza_error(self):
        """Test que verifica que una lista vacía lanza ValueError."""
        with pytest.raises(ValueError):
            calcular_varianza([])


class TestCalcularDesviacionEstandar:
    """Tests para la función calcular_desviacion_estandar()."""

    def test_desviacion_basica(self):
        """Test con valores conocidos."""
        datos = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        resultado = calcular_desviacion_estandar(datos)
        # Desviación estándar es raíz cuadrada de varianza (4.0) = 2.0
        assert abs(resultado - 2.0) < 0.0001

    def test_desviacion_sin_variacion(self):
        """Test cuando todos los valores son iguales."""
        datos = [5.0, 5.0, 5.0, 5.0]
        resultado = calcular_desviacion_estandar(datos)
        assert resultado == 0.0

    def test_desviacion_relacion_con_varianza(self):
        """Test que verifica la relación matemática entre desviación y varianza."""
        datos = [1.0, 2.0, 3.0, 4.0, 5.0]
        varianza = calcular_varianza(datos)
        desviacion = calcular_desviacion_estandar(datos)
        assert (
            abs(desviacion**2 - varianza) < 0.0001
        ), "desv^2 debe ser igual a varianza"

    def test_desviacion_ejemplo_real_ventas(self):
        """
        Test con ejemplo real: volatilidad de ventas.

        Caso de uso: Medir qué tan estables son las ventas diarias.
        Alta desviación = ventas muy variables, baja desviación = ventas estables.
        """
        ventas_estables = [100.0, 102.0, 98.0, 101.0, 99.0]
        ventas_volatiles = [50.0, 150.0, 75.0, 125.0, 100.0]

        desv_estables = calcular_desviacion_estandar(ventas_estables)
        desv_volatiles = calcular_desviacion_estandar(ventas_volatiles)

        assert (
            desv_volatiles > desv_estables
        ), "Ventas volátiles deben tener mayor desviación"


class TestCalcularPercentiles:
    """Tests para la función calcular_percentiles()."""

    def test_percentiles_cuartiles(self):
        """Test calculando cuartiles (25, 50, 75)."""
        datos = list(range(1, 11))  # [1, 2, 3, ..., 10]
        resultado = calcular_percentiles(datos, [25, 50, 75])

        assert 25 in resultado
        assert 50 in resultado
        assert 75 in resultado
        assert abs(resultado[50] - 5.5) < 0.1  # Mediana aproximada

    def test_percentiles_limites(self):
        """Test con percentiles en los límites (0, 100)."""
        datos = [1.0, 2.0, 3.0, 4.0, 5.0]
        resultado = calcular_percentiles(datos, [0, 100])

        assert abs(resultado[0] - 1.0) < 0.1  # Mínimo
        assert abs(resultado[100] - 5.0) < 0.1  # Máximo

    def test_percentiles_un_valor(self):
        """Test pidiendo un solo percentil."""
        datos = list(range(1, 101))  # 1 a 100
        resultado = calcular_percentiles(datos, [50])

        assert 50 in resultado
        assert abs(resultado[50] - 50.5) < 1.0

    def test_percentiles_lista_vacia_lanza_error(self):
        """Test que verifica que una lista vacía lanza ValueError."""
        with pytest.raises(ValueError):
            calcular_percentiles([], [50])

    def test_percentiles_percentiles_invalidos_lanza_error(self):
        """Test que verifica que percentiles fuera de rango lanzan ValueError."""
        datos = [1.0, 2.0, 3.0]

        with pytest.raises(ValueError, match="entre 0 y 100"):
            calcular_percentiles(datos, [-1])

        with pytest.raises(ValueError, match="entre 0 y 100"):
            calcular_percentiles(datos, [101])

    def test_percentiles_no_lista_lanza_error(self):
        """Test que verifica validación de tipos."""
        with pytest.raises(TypeError):
            calcular_percentiles([1, 2, 3], "50")  # type: ignore

    def test_percentiles_ejemplo_real_sla(self):
        """
        Test con ejemplo real: SLA de tiempos de respuesta.

        Caso de uso: En Agora/Yurest, medir que el 95% de las peticiones
        respondan en menos de X ms (percentil 95).
        """
        tiempos_ms = [10, 12, 15, 18, 20, 22, 25, 30, 35, 200]
        resultado = calcular_percentiles(tiempos_ms, [50, 95, 99])

        # El percentil 95 no debe verse muy afectado por el outlier (200ms)
        assert resultado[95] < 150, "P95 debe ser razonable incluso con outlier"
        assert resultado[50] < 30, "P50 (mediana) debe ser bajo"
