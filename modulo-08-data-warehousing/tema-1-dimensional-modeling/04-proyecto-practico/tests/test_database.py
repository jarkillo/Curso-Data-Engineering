"""
Tests para database.py.

Tests escritos PRIMERO siguiendo TDD para módulo de conexión a base de datos.
Cobertura objetivo: ≥85%.
"""

import sqlite3
from datetime import date

import pandas as pd


class TestDatabaseConnection:
    """Tests para la clase DatabaseConnection."""

    def test_conexion_con_context_manager(self):
        """Should connect and disconnect properly with context manager."""
        from src.database import DatabaseConnection

        with DatabaseConnection(":memory:") as db:
            assert db.connection is not None
            assert isinstance(db.connection, sqlite3.Connection)

        # Después del context manager, conexión debe estar cerrada
        # (no podemos verificar directamente, pero no debe tirar error)

    def test_crear_tablas_ejecuta_sin_error(self):
        """Should create tables from schema without error."""
        from src.database import DatabaseConnection

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()

            # Verificar que al menos una tabla fue creada
            cursor = db.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()

            assert len(tablas) > 0

    def test_crear_tablas_crea_dim_fecha(self):
        """Should create DimFecha table."""
        from src.database import DatabaseConnection

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()

            cursor = db.connection.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='DimFecha'"
            )
            tabla = cursor.fetchone()

            assert tabla is not None
            assert tabla[0] == "DimFecha"


class TestCargarDimension:
    """Tests para la función cargar_dimension."""

    def test_cargar_dimension_fecha(self):
        """Should load DimFecha successfully."""
        from src.database import DatabaseConnection

        # Crear datos de prueba
        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101,
                    "fecha_completa": date(2024, 1, 1),
                    "dia": 1,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                }
            ]
        )

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            registros_insertados = db.cargar_dimension("DimFecha", df_fecha)

            assert registros_insertados == 1

            # Verificar que se insertó correctamente
            cursor = db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM DimFecha")
            count = cursor.fetchone()[0]

            assert count == 1

    def test_cargar_dimension_multiples_registros(self):
        """Should load multiple records."""
        from src.database import DatabaseConnection

        # Crear 10 fechas
        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101 + i,
                    "fecha_completa": date(2024, 1, 1 + i),
                    "dia": 1 + i,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                }
                for i in range(10)
            ]
        )

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            registros_insertados = db.cargar_dimension("DimFecha", df_fecha)

            assert registros_insertados == 10

    def test_cargar_dimension_vacia_retorna_cero(self):
        """Should return 0 when DataFrame is empty."""
        from src.database import DatabaseConnection

        df_vacio = pd.DataFrame()

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            registros_insertados = db.cargar_dimension("DimFecha", df_vacio)

            assert registros_insertados == 0


class TestCargarFact:
    """Tests para la función cargar_fact."""

    def test_cargar_fact_ventas(self):
        """Should load FactVentas successfully."""
        from src.database import DatabaseConnection

        # Primero cargar dimensiones necesarias (para FK)
        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101,
                    "fecha_completa": date(2024, 1, 1),
                    "dia": 1,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                }
            ]
        )

        df_producto = pd.DataFrame(
            [
                {
                    "producto_id": 100,
                    "sku": "SKU-100",
                    "nombre_producto": "Producto Test",
                    "marca": "Marca Test",
                    "categoria": "Test",
                    "subcategoria": "Test",
                    "precio_catalogo": 100.0,
                    "peso_kg": 1.0,
                    "requiere_refrigeracion": False,
                }
            ]
        )

        df_vendedor = pd.DataFrame(
            [
                {
                    "vendedor_id": 10,
                    "nombre": "Vendedor Test",
                    "email": "vendedor@test.com",
                    "telefono": "555-1234",
                    "region": "Test",
                    "comision_porcentaje": 10.0,
                    "supervisor_id": None,
                    "gerente_regional": "Gerente Test",
                }
            ]
        )

        # Nota: DimCliente usa cliente_sk (autoincrement), así que insertamos y obtenemos el ID
        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()

            # Cargar dimensiones
            db.cargar_dimension("DimFecha", df_fecha)
            db.cargar_dimension("DimProducto", df_producto)
            db.cargar_dimension("DimVendedor", df_vendedor)

            # Insertar cliente manualmente para obtener cliente_sk
            db.ejecutar_comando(
                """
                INSERT INTO DimCliente
                (cliente_id, nombre, email, telefono, direccion, ciudad, estado,
                 codigo_postal, fecha_registro, segmento, fecha_inicio, fecha_fin, version, es_actual)
                VALUES (1, 'Cliente Test', 'cliente@test.com', '555-1234',
                        'Dirección Test', 'Ciudad Test', 'Estado Test', '12345',
                        '2024-01-01', 'Regular', '2024-01-01', NULL, 1, 1)
            """
            )

            # Ahora cargar FactVentas (usa cliente_sk = 1 autoincrement)
            df_ventas = pd.DataFrame(
                [
                    {
                        "fecha_id": 20240101,
                        "producto_id": 100,
                        "cliente_id": 1,  # Este es el cliente_sk generado
                        "vendedor_id": 10,
                        "cantidad": 2,
                        "precio_unitario": 100.0,
                        "descuento": 10.0,
                        "impuesto": 18.0,
                        "monto_neto": 208.0,
                    }
                ]
            )

            registros_insertados = db.cargar_fact("FactVentas", df_ventas)

            assert registros_insertados == 1

            # Verificar inserción
            cursor = db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM FactVentas")
            count = cursor.fetchone()[0]

            assert count == 1


class TestEjecutarQuery:
    """Tests para la función ejecutar_query."""

    def test_ejecutar_query_select(self):
        """Should execute SELECT query and return DataFrame."""
        from src.database import DatabaseConnection

        # Cargar datos primero
        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101,
                    "fecha_completa": date(2024, 1, 1),
                    "dia": 1,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                },
                {
                    "fecha_id": 20240102,
                    "fecha_completa": date(2024, 1, 2),
                    "dia": 2,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Martes",
                    "numero_dia_semana": 1,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                },
            ]
        )

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            db.cargar_dimension("DimFecha", df_fecha)

            # Ejecutar query
            resultado = db.ejecutar_query("SELECT * FROM DimFecha WHERE mes = 1")

            assert isinstance(resultado, pd.DataFrame)
            assert len(resultado) == 2
            assert "fecha_id" in resultado.columns

    def test_ejecutar_query_agregacion(self):
        """Should execute aggregation query."""
        from src.database import DatabaseConnection

        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101 + i,
                    "fecha_completa": date(2024, 1, 1 + i),
                    "dia": 1 + i,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                }
                for i in range(31)
            ]
        )

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            db.cargar_dimension("DimFecha", df_fecha)

            # Query de agregación
            resultado = db.ejecutar_query(
                "SELECT mes, COUNT(*) as total FROM DimFecha GROUP BY mes"
            )

            assert isinstance(resultado, pd.DataFrame)
            assert len(resultado) == 1
            assert resultado.iloc[0]["total"] == 31

    def test_ejecutar_query_vacia_retorna_dataframe_vacio(self):
        """Should return empty DataFrame when no results."""
        from src.database import DatabaseConnection

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()

            resultado = db.ejecutar_query("SELECT * FROM DimFecha WHERE 1=0")

            assert isinstance(resultado, pd.DataFrame)
            assert len(resultado) == 0


class TestTransacciones:
    """Tests para manejo de transacciones."""

    def test_commit_despues_de_insertar(self):
        """Should commit transaction after insert."""
        from src.database import DatabaseConnection

        df_fecha = pd.DataFrame(
            [
                {
                    "fecha_id": 20240101,
                    "fecha_completa": date(2024, 1, 1),
                    "dia": 1,
                    "mes": 1,
                    "mes_nombre": "Enero",
                    "trimestre": 1,
                    "anio": 2024,
                    "dia_semana": "Lunes",
                    "numero_dia_semana": 0,
                    "numero_semana": 1,
                    "es_fin_de_semana": False,
                    "es_dia_festivo": False,
                    "nombre_festivo": None,
                }
            ]
        )

        with DatabaseConnection(":memory:") as db:
            db.crear_tablas()
            db.cargar_dimension("DimFecha", df_fecha)

            # Verificar que se hizo commit (los datos persisten)
            cursor = db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM DimFecha")
            count = cursor.fetchone()[0]

            assert count == 1
