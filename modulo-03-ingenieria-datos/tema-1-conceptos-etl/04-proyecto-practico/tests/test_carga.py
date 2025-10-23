"""Tests para el módulo de carga de datos en SQLite."""

import sqlite3

from src.carga import (
    cargar_ventas_idempotente,
    consultar_ventas_por_fecha,
    crear_tabla_ventas,
)


class TestCrearTablaVentas:
    """Tests para la función crear_tabla_ventas."""

    def test_crea_tabla_si_no_existe(self, tmp_path):
        """Debe crear la tabla ventas_procesadas si no existe."""
        db_path = tmp_path / "test.db"

        crear_tabla_ventas(str(db_path))

        # Verificar que la tabla existe
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name='ventas_procesadas'"
        )
        resultado = cursor.fetchone()
        conn.close()

        assert resultado is not None
        assert resultado[0] == "ventas_procesadas"

    def test_no_falla_si_tabla_ya_existe(self, tmp_path):
        """No debe fallar si la tabla ya existe."""
        db_path = tmp_path / "test.db"

        # Crear tabla 2 veces
        crear_tabla_ventas(str(db_path))
        crear_tabla_ventas(str(db_path))  # No debe fallar


class TestCargarVentasIdempotente:
    """Tests para la función cargar_ventas_idempotente."""

    def test_carga_ventas_correctamente(self, tmp_path):
        """Debe cargar ventas en la base de datos."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        ventas = [
            {
                "venta_id": 1,
                "fecha": "2025-10-01",
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 2,
                "precio_unitario": 100.0,
                "total": 200.0,
                "nombre_producto": "Laptop",
                "categoria": "Computadoras",
                "nombre_cliente": "Juan",
                "ciudad": "Madrid",
            }
        ]

        num_cargadas = cargar_ventas_idempotente(ventas, "2025-10-01", str(db_path))

        assert num_cargadas == 1

        # Verificar que se cargó
        resultado = consultar_ventas_por_fecha("2025-10-01", str(db_path))
        assert len(resultado) == 1
        assert resultado[0]["venta_id"] == 1

    def test_es_idempotente_no_duplica(self, tmp_path):
        """Debe ser idempotente: ejecutar 2 veces no duplica datos."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        ventas = [
            {
                "venta_id": 1,
                "fecha": "2025-10-01",
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 2,
                "precio_unitario": 100.0,
                "total": 200.0,
                "nombre_producto": "Laptop",
                "categoria": "Computadoras",
                "nombre_cliente": "Juan",
                "ciudad": "Madrid",
            }
        ]

        # Cargar 2 veces
        cargar_ventas_idempotente(ventas, "2025-10-01", str(db_path))
        cargar_ventas_idempotente(ventas, "2025-10-01", str(db_path))

        # Debe haber solo 1 fila
        resultado = consultar_ventas_por_fecha("2025-10-01", str(db_path))
        assert len(resultado) == 1

    def test_solo_borra_fecha_especificada(self, tmp_path):
        """Debe borrar solo las ventas de la fecha especificada."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        venta_01 = {
            "venta_id": 1,
            "fecha": "2025-10-01",
            "producto_id": 101,
            "cliente_id": 1001,
            "cantidad": 2,
            "precio_unitario": 100.0,
            "total": 200.0,
            "nombre_producto": "Laptop",
            "categoria": "Computadoras",
            "nombre_cliente": "Juan",
            "ciudad": "Madrid",
        }
        venta_02 = {
            "venta_id": 2,
            "fecha": "2025-10-02",
            "producto_id": 102,
            "cliente_id": 1002,
            "cantidad": 5,
            "precio_unitario": 20.0,
            "total": 100.0,
            "nombre_producto": "Mouse",
            "categoria": "Accesorios",
            "nombre_cliente": "María",
            "ciudad": "Barcelona",
        }

        # Cargar ambas fechas
        cargar_ventas_idempotente([venta_01], "2025-10-01", str(db_path))
        cargar_ventas_idempotente([venta_02], "2025-10-02", str(db_path))

        # Reprocesar solo 2025-10-01
        cargar_ventas_idempotente([venta_01], "2025-10-01", str(db_path))

        # Debe seguir habiendo datos de 2025-10-02
        resultado_02 = consultar_ventas_por_fecha("2025-10-02", str(db_path))
        assert len(resultado_02) == 1


class TestConsultarVentasPorFecha:
    """Tests para la función consultar_ventas_por_fecha."""

    def test_consulta_ventas_de_fecha_especifica(self, tmp_path):
        """Debe retornar solo ventas de la fecha especificada."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        ventas = [
            {
                "venta_id": 1,
                "fecha": "2025-10-01",
                "producto_id": 101,
                "cliente_id": 1001,
                "cantidad": 2,
                "precio_unitario": 100.0,
                "total": 200.0,
                "nombre_producto": "Laptop",
                "categoria": "Computadoras",
                "nombre_cliente": "Juan",
                "ciudad": "Madrid",
            },
            {
                "venta_id": 2,
                "fecha": "2025-10-02",
                "producto_id": 102,
                "cliente_id": 1002,
                "cantidad": 5,
                "precio_unitario": 20.0,
                "total": 100.0,
                "nombre_producto": "Mouse",
                "categoria": "Accesorios",
                "nombre_cliente": "María",
                "ciudad": "Barcelona",
            },
        ]

        cargar_ventas_idempotente(ventas[:1], "2025-10-01", str(db_path))
        cargar_ventas_idempotente(ventas[1:], "2025-10-02", str(db_path))

        # Consultar solo 2025-10-01
        resultado = consultar_ventas_por_fecha("2025-10-01", str(db_path))

        assert len(resultado) == 1
        assert resultado[0]["fecha"] == "2025-10-01"

    def test_retorna_lista_vacia_si_no_hay_datos(self, tmp_path):
        """Debe retornar lista vacía si no hay ventas en esa fecha."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        resultado = consultar_ventas_por_fecha("2025-10-01", str(db_path))

        assert resultado == []
