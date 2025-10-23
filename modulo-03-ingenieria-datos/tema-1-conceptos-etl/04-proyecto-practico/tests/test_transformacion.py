"""Tests para el módulo de transformación de datos."""

import pytest
from src.transformacion import (
    calcular_total_venta,
    enriquecer_venta_con_cliente,
    enriquecer_venta_con_producto,
    transformar_ventas,
)


class TestCalcularTotalVenta:
    """Tests para la función calcular_total_venta."""

    def test_calcula_total_correctamente(self):
        """Debe calcular total = cantidad * precio_unitario."""
        venta = {"cantidad": 2, "precio_unitario": 100.50}

        resultado = calcular_total_venta(venta)

        assert resultado["total"] == 201.00

    def test_redondea_a_dos_decimales(self):
        """Debe redondear el total a 2 decimales."""
        venta = {"cantidad": 3, "precio_unitario": 10.333}

        resultado = calcular_total_venta(venta)

        assert resultado["total"] == 31.00

    def test_no_modifica_venta_original(self):
        """No debe modificar el diccionario original."""
        venta = {"cantidad": 2, "precio_unitario": 100.0}

        resultado = calcular_total_venta(venta)

        # La venta original no debe tener 'total'
        assert "total" not in venta
        # El resultado debe tener 'total'
        assert "total" in resultado
        # El resultado debe ser un nuevo diccionario
        assert resultado is not venta


class TestEnriquecerVentaConProducto:
    """Tests para la función enriquecer_venta_con_producto."""

    def test_añade_informacion_de_producto(self):
        """Debe añadir nombre y categoría del producto."""
        venta = {"producto_id": 101, "cantidad": 2}
        productos = [
            {"producto_id": 101, "nombre": "Laptop Dell", "categoria": "Computadoras"},
            {"producto_id": 102, "nombre": "Mouse", "categoria": "Accesorios"},
        ]

        resultado = enriquecer_venta_con_producto(venta, productos)

        assert resultado["nombre_producto"] == "Laptop Dell"
        assert resultado["categoria"] == "Computadoras"

    def test_lanza_value_error_si_producto_no_existe(self):
        """Debe lanzar ValueError si el producto no existe."""
        venta = {"producto_id": 999}
        productos = [{"producto_id": 101, "nombre": "Laptop"}]

        with pytest.raises(ValueError, match="Producto 999 no encontrado"):
            enriquecer_venta_con_producto(venta, productos)

    def test_no_modifica_venta_original(self):
        """No debe modificar el diccionario original."""
        venta = {"producto_id": 101}
        productos = [{"producto_id": 101, "nombre": "Laptop", "categoria": "Compu"}]

        resultado = enriquecer_venta_con_producto(venta, productos)

        assert "nombre_producto" not in venta
        assert "nombre_producto" in resultado


class TestEnriquecerVentaConCliente:
    """Tests para la función enriquecer_venta_con_cliente."""

    def test_añade_informacion_de_cliente(self):
        """Debe añadir nombre y ciudad del cliente."""
        venta = {"cliente_id": 1001}
        clientes = [
            {"cliente_id": 1001, "nombre": "Juan Pérez", "ciudad": "Madrid"},
            {"cliente_id": 1002, "nombre": "María", "ciudad": "Barcelona"},
        ]

        resultado = enriquecer_venta_con_cliente(venta, clientes)

        assert resultado["nombre_cliente"] == "Juan Pérez"
        assert resultado["ciudad"] == "Madrid"

    def test_lanza_value_error_si_cliente_no_existe(self):
        """Debe lanzar ValueError si el cliente no existe."""
        venta = {"cliente_id": 9999}
        clientes = [{"cliente_id": 1001, "nombre": "Juan"}]

        with pytest.raises(ValueError, match="Cliente 9999 no encontrado"):
            enriquecer_venta_con_cliente(venta, clientes)

    def test_no_modifica_venta_original(self):
        """No debe modificar el diccionario original."""
        venta = {"cliente_id": 1001}
        clientes = [{"cliente_id": 1001, "nombre": "Juan", "ciudad": "Madrid"}]

        resultado = enriquecer_venta_con_cliente(venta, clientes)

        assert "nombre_cliente" not in venta
        assert "nombre_cliente" in resultado


class TestTransformarVentas:
    """Tests para la función transformar_ventas."""

    def test_transforma_todas_las_ventas(self):
        """Debe transformar todas las ventas correctamente."""
        ventas = [
            {
                "venta_id": 1,
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 2,
                "precio_unitario": 100.0,
            },
            {
                "venta_id": 2,
                "producto_id": 102,
                "cliente_id": 1002,
                "cantidad": 5,
                "precio_unitario": 20.0,
            },
        ]
        productos = [
            {"producto_id": 101, "nombre": "Laptop", "categoria": "Computadoras"},
            {"producto_id": 102, "nombre": "Mouse", "categoria": "Accesorios"},
        ]
        clientes = [
            {"cliente_id": 1001, "nombre": "Juan", "ciudad": "Madrid"},
            {"cliente_id": 1002, "nombre": "María", "ciudad": "Barcelona"},
        ]

        resultado = transformar_ventas(ventas, productos, clientes)

        assert len(resultado) == 2
        # Primera venta
        assert resultado[0]["total"] == 200.0
        assert resultado[0]["nombre_producto"] == "Laptop"
        assert resultado[0]["categoria"] == "Computadoras"
        assert resultado[0]["nombre_cliente"] == "Juan"
        assert resultado[0]["ciudad"] == "Madrid"
        # Segunda venta
        assert resultado[1]["total"] == 100.0
        assert resultado[1]["nombre_producto"] == "Mouse"

    def test_con_lista_vacia_retorna_lista_vacia(self):
        """Debe retornar lista vacía si no hay ventas."""
        resultado = transformar_ventas([], [], [])

        assert resultado == []
