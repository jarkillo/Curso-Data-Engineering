"""Tests para el módulo de validación de datos."""

import pytest
from src.validacion import (
    validar_columnas_requeridas,
    validar_datos,
    validar_no_vacia,
    validar_tipos_ventas,
    validar_valores_positivos,
)


class TestValidarNoVacia:
    """Tests para la función validar_no_vacia."""

    def test_con_lista_con_datos_no_lanza_error(self):
        """No debe lanzar error si la lista tiene datos."""
        datos = [{"id": 1}, {"id": 2}]
        # No debe lanzar excepción
        validar_no_vacia(datos, "ventas")

    def test_con_lista_vacia_lanza_value_error(self):
        """Debe lanzar ValueError si la lista está vacía."""
        with pytest.raises(ValueError, match="ventas está vacía"):
            validar_no_vacia([], "ventas")


class TestValidarColumnasRequeridas:
    """Tests para la función validar_columnas_requeridas."""

    def test_con_todas_las_columnas_presentes_no_lanza_error(self):
        """No debe lanzar error si todas las columnas están presentes."""
        datos = [
            {"id": 1, "nombre": "A", "precio": 100},
            {"id": 2, "nombre": "B", "precio": 200},
        ]
        columnas = ["id", "nombre", "precio"]
        # No debe lanzar excepción
        validar_columnas_requeridas(datos, columnas)

    def test_con_columnas_faltantes_lanza_value_error(self):
        """Debe lanzar ValueError si faltan columnas."""
        datos = [{"id": 1, "nombre": "A"}]  # Falta 'precio'
        columnas = ["id", "nombre", "precio"]

        with pytest.raises(ValueError, match="columnas requeridas"):
            validar_columnas_requeridas(datos, columnas)

    def test_con_lista_vacia_no_lanza_error(self):
        """No debe lanzar error si la lista está vacía."""
        # (ya se validó con validar_no_vacia antes)
        validar_columnas_requeridas([], ["id", "nombre"])


class TestValidarTiposVentas:
    """Tests para la función validar_tipos_ventas."""

    def test_con_tipos_correctos_no_lanza_error(self):
        """No debe lanzar error si los tipos son correctos."""
        ventas = [
            {"venta_id": 1, "cantidad": 2, "precio_unitario": 100.5},
            {"venta_id": 2, "cantidad": 5, "precio_unitario": 50.0},
        ]
        # No debe lanzar excepción
        validar_tipos_ventas(ventas)

    def test_con_venta_id_no_entero_lanza_type_error(self):
        """Debe lanzar TypeError si venta_id no es int."""
        ventas = [{"venta_id": "1", "cantidad": 2, "precio_unitario": 100.0}]

        with pytest.raises(TypeError, match="venta_id debe ser int"):
            validar_tipos_ventas(ventas)

    def test_con_cantidad_no_entera_lanza_type_error(self):
        """Debe lanzar TypeError si cantidad no es int."""
        ventas = [{"venta_id": 1, "cantidad": "2", "precio_unitario": 100.0}]

        with pytest.raises(TypeError, match="cantidad debe ser int"):
            validar_tipos_ventas(ventas)

    def test_con_precio_no_float_lanza_type_error(self):
        """Debe lanzar TypeError si precio_unitario no es float o int."""
        ventas = [{"venta_id": 1, "cantidad": 2, "precio_unitario": "100"}]

        with pytest.raises(TypeError, match="precio_unitario debe ser"):
            validar_tipos_ventas(ventas)


class TestValidarValoresPositivos:
    """Tests para la función validar_valores_positivos."""

    def test_con_valores_positivos_no_lanza_error(self):
        """No debe lanzar error si todos los valores son positivos."""
        ventas = [
            {"cantidad": 2, "precio_unitario": 100.5},
            {"cantidad": 5, "precio_unitario": 50.0},
        ]
        # No debe lanzar excepción
        validar_valores_positivos(ventas)

    def test_con_cantidad_cero_lanza_value_error(self):
        """Debe lanzar ValueError si cantidad es 0."""
        ventas = [{"cantidad": 0, "precio_unitario": 100.0}]

        with pytest.raises(ValueError, match="cantidad debe ser mayor que 0"):
            validar_valores_positivos(ventas)

    def test_con_cantidad_negativa_lanza_value_error(self):
        """Debe lanzar ValueError si cantidad es negativa."""
        ventas = [{"cantidad": -1, "precio_unitario": 100.0}]

        with pytest.raises(ValueError, match="cantidad debe ser mayor que 0"):
            validar_valores_positivos(ventas)

    def test_con_precio_cero_lanza_value_error(self):
        """Debe lanzar ValueError si precio es 0."""
        ventas = [{"cantidad": 2, "precio_unitario": 0.0}]

        with pytest.raises(ValueError, match="precio_unitario debe ser mayor que 0"):
            validar_valores_positivos(ventas)

    def test_con_precio_negativo_lanza_value_error(self):
        """Debe lanzar ValueError si precio es negativo."""
        ventas = [{"cantidad": 2, "precio_unitario": -10.0}]

        with pytest.raises(ValueError, match="precio_unitario debe ser mayor que 0"):
            validar_valores_positivos(ventas)


class TestValidarDatos:
    """Tests para la función validar_datos."""

    def test_con_datos_validos_retorna_true_sin_errores(self):
        """Debe retornar (True, []) si los datos son válidos."""
        ventas = [
            {
                "venta_id": 1,
                "fecha": "2025-10-01",
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 2,
                "precio_unitario": 100.5,
            }
        ]

        es_valido, errores = validar_datos(ventas)

        assert es_valido is True
        assert errores == []

    def test_con_lista_vacia_retorna_false_con_errores(self):
        """Debe retornar (False, [error]) si la lista está vacía."""
        es_valido, errores = validar_datos([])

        assert es_valido is False
        assert len(errores) > 0
        assert "vacía" in errores[0]

    def test_con_multiples_errores_los_acumula(self):
        """Debe acumular múltiples errores si hay varios problemas."""
        ventas = [
            {
                "venta_id": "1",  # Tipo incorrecto
                "fecha": "2025-10-01",
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 0,  # Valor inválido
                "precio_unitario": -10.0,  # Valor inválido
            }
        ]

        es_valido, errores = validar_datos(ventas)

        assert es_valido is False
        assert len(errores) > 1  # Múltiples errores
