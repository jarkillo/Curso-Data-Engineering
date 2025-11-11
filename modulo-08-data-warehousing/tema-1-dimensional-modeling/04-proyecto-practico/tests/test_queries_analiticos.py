"""
Tests para queries_analiticos.py.

Tests escritos PRIMERO siguiendo TDD para módulo de queries analíticos OLAP.
Cobertura objetivo: ≥80%.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def db_con_datos():
    """
    Fixture que crea base de datos en memoria con datos de prueba.

    Retorna DatabaseConnection con:
    - 3 fechas (enero, febrero, marzo 2024)
    - 3 productos (2 Electrónica, 1 Hogar)
    - 2 vendedores
    - 3 clientes
    - 5 ventas
    """
    from src.database import DatabaseConnection

    db = DatabaseConnection(":memory:")
    db.__enter__()

    # Crear tablas
    db.crear_tablas()

    # Cargar DimFecha (3 fechas)
    df_fecha = pd.DataFrame(
        [
            {
                "fecha_id": 20240115,
                "fecha_completa": date(2024, 1, 15),
                "dia": 15,
                "mes": 1,
                "mes_nombre": "Enero",
                "trimestre": 1,
                "anio": 2024,
                "dia_semana": "Lunes",
                "numero_dia_semana": 0,
                "numero_semana": 3,
                "es_fin_de_semana": False,
                "es_dia_festivo": False,
                "nombre_festivo": None,
            },
            {
                "fecha_id": 20240220,
                "fecha_completa": date(2024, 2, 20),
                "dia": 20,
                "mes": 2,
                "mes_nombre": "Febrero",
                "trimestre": 1,
                "anio": 2024,
                "dia_semana": "Martes",
                "numero_dia_semana": 1,
                "numero_semana": 8,
                "es_fin_de_semana": False,
                "es_dia_festivo": False,
                "nombre_festivo": None,
            },
            {
                "fecha_id": 20240310,
                "fecha_completa": date(2024, 3, 10),
                "dia": 10,
                "mes": 3,
                "mes_nombre": "Marzo",
                "trimestre": 1,
                "anio": 2024,
                "dia_semana": "Domingo",
                "numero_dia_semana": 6,
                "numero_semana": 10,
                "es_fin_de_semana": True,
                "es_dia_festivo": False,
                "nombre_festivo": None,
            },
        ]
    )
    db.cargar_dimension("DimFecha", df_fecha)

    # Cargar DimProducto (3 productos)
    df_producto = pd.DataFrame(
        [
            {
                "producto_id": 1,
                "sku": "LAPTOP-001",
                "nombre_producto": "Laptop Dell XPS",
                "marca": "Dell",
                "categoria": "Electrónica",
                "subcategoria": "Computadoras",
                "precio_catalogo": 1500.0,
                "peso_kg": 2.5,
                "requiere_refrigeracion": False,
            },
            {
                "producto_id": 2,
                "sku": "MOUSE-001",
                "nombre_producto": "Mouse Logitech MX",
                "marca": "Logitech",
                "categoria": "Electrónica",
                "subcategoria": "Accesorios",
                "precio_catalogo": 80.0,
                "peso_kg": 0.2,
                "requiere_refrigeracion": False,
            },
            {
                "producto_id": 3,
                "sku": "SILLA-001",
                "nombre_producto": "Silla Ergonómica",
                "marca": "Herman Miller",
                "categoria": "Hogar",
                "subcategoria": "Mobiliario",
                "precio_catalogo": 600.0,
                "peso_kg": 15.0,
                "requiere_refrigeracion": False,
            },
        ]
    )
    db.cargar_dimension("DimProducto", df_producto)

    # Cargar DimVendedor (2 vendedores)
    df_vendedor = pd.DataFrame(
        [
            {
                "vendedor_id": 1,
                "nombre": "Juan Pérez",
                "email": "juan@empresa.com",
                "telefono": "555-1001",
                "region": "Norte",
                "comision_porcentaje": 10.0,
                "supervisor_id": None,
                "gerente_regional": "Ana García",
            },
            {
                "vendedor_id": 2,
                "nombre": "María López",
                "email": "maria@empresa.com",
                "telefono": "555-1002",
                "region": "Sur",
                "comision_porcentaje": 12.0,
                "supervisor_id": None,
                "gerente_regional": "Carlos Ruiz",
            },
        ]
    )
    db.cargar_dimension("DimVendedor", df_vendedor)

    # Cargar DimCliente (3 clientes)
    db.ejecutar_comando(
        """
        INSERT INTO DimCliente
        (cliente_id, nombre, email, telefono, direccion, ciudad, estado,
         codigo_postal, fecha_registro, segmento, fecha_inicio, fecha_fin, version, es_actual)
        VALUES
        (1, 'Cliente A', 'clienteA@test.com', '555-2001', 'Calle 1', 'CDMX', 'CDMX', '01000',
         '2024-01-01', 'Premium', '2024-01-01', NULL, 1, 1),
        (2, 'Cliente B', 'clienteB@test.com', '555-2002', 'Calle 2', 'Guadalajara', 'Jalisco', '44100',
         '2024-01-01', 'Regular', '2024-01-01', NULL, 1, 1),
        (3, 'Cliente C', 'clienteC@test.com', '555-2003', 'Calle 3', 'Monterrey', 'Nuevo León', '64000',
         '2024-01-01', 'Regular', '2024-01-01', NULL, 1, 1)
    """
    )

    # Cargar FactVentas (5 ventas)
    df_ventas = pd.DataFrame(
        [
            # Enero: 2 ventas
            {
                "fecha_id": 20240115,
                "producto_id": 1,
                "cliente_id": 1,
                "vendedor_id": 1,
                "cantidad": 2,
                "precio_unitario": 1500.0,
                "descuento": 100.0,
                "impuesto": 540.0,
                "monto_neto": 2940.0,
            },
            {
                "fecha_id": 20240115,
                "producto_id": 2,
                "cliente_id": 2,
                "vendedor_id": 1,
                "cantidad": 5,
                "precio_unitario": 80.0,
                "descuento": 20.0,
                "impuesto": 60.8,
                "monto_neto": 440.8,
            },
            # Febrero: 2 ventas
            {
                "fecha_id": 20240220,
                "producto_id": 1,
                "cliente_id": 1,
                "vendedor_id": 2,
                "cantidad": 1,
                "precio_unitario": 1500.0,
                "descuento": 0.0,
                "impuesto": 270.0,
                "monto_neto": 1770.0,
            },
            {
                "fecha_id": 20240220,
                "producto_id": 3,
                "cliente_id": 3,
                "vendedor_id": 2,
                "cantidad": 3,
                "precio_unitario": 600.0,
                "descuento": 50.0,
                "impuesto": 313.2,
                "monto_neto": 2063.2,
            },
            # Marzo: 1 venta
            {
                "fecha_id": 20240310,
                "producto_id": 2,
                "cliente_id": 2,
                "vendedor_id": 1,
                "cantidad": 10,
                "precio_unitario": 80.0,
                "descuento": 40.0,
                "impuesto": 133.6,
                "monto_neto": 893.6,
            },
        ]
    )
    db.cargar_fact("FactVentas", df_ventas)

    yield db

    # Cleanup
    db.__exit__(None, None, None)


class TestVentasPorCategoria:
    """Tests para ventas_por_categoria()."""

    def test_retorna_dataframe(self, db_con_datos):
        """Should return a DataFrame."""
        from src.queries_analiticos import ventas_por_categoria

        resultado = ventas_por_categoria(db_con_datos)

        assert isinstance(resultado, pd.DataFrame)

    def test_columnas_esperadas(self, db_con_datos):
        """Should have expected columns."""
        from src.queries_analiticos import ventas_por_categoria

        resultado = ventas_por_categoria(db_con_datos)

        assert "categoria" in resultado.columns
        assert "total_ventas" in resultado.columns
        assert "cantidad_productos" in resultado.columns

    def test_calcula_ventas_por_categoria_correctamente(self, db_con_datos):
        """Should calculate sales by category correctly."""
        from src.queries_analiticos import ventas_por_categoria

        resultado = ventas_por_categoria(db_con_datos)

        # Electrónica: 2 laptops (2940 + 1770) + 2 mouse (440.8 + 893.6) = 6044.4
        # Hogar: 1 silla (2063.2)
        electronica = resultado[resultado["categoria"] == "Electrónica"].iloc[0]
        assert electronica["total_ventas"] == pytest.approx(6044.4, abs=0.1)

        hogar = resultado[resultado["categoria"] == "Hogar"].iloc[0]
        assert hogar["total_ventas"] == pytest.approx(2063.2, abs=0.1)

    def test_ordena_por_total_descendente(self, db_con_datos):
        """Should order by total_ventas descending."""
        from src.queries_analiticos import ventas_por_categoria

        resultado = ventas_por_categoria(db_con_datos)

        # Electrónica (6044.4) debe estar primero que Hogar (2063.2)
        assert resultado.iloc[0]["categoria"] == "Electrónica"


class TestTopProductos:
    """Tests para top_productos()."""

    def test_retorna_dataframe(self, db_con_datos):
        """Should return a DataFrame."""
        from src.queries_analiticos import top_productos

        resultado = top_productos(db_con_datos, top_n=3)

        assert isinstance(resultado, pd.DataFrame)

    def test_limita_cantidad_resultados(self, db_con_datos):
        """Should limit results to top_n."""
        from src.queries_analiticos import top_productos

        resultado = top_productos(db_con_datos, top_n=2)

        assert len(resultado) == 2

    def test_columnas_esperadas(self, db_con_datos):
        """Should have expected columns."""
        from src.queries_analiticos import top_productos

        resultado = top_productos(db_con_datos, top_n=3)

        assert "nombre_producto" in resultado.columns
        assert "categoria" in resultado.columns
        assert "total_ventas" in resultado.columns
        assert "cantidad_vendida" in resultado.columns

    def test_ordena_por_total_ventas(self, db_con_datos):
        """Should order by total sales descending."""
        from src.queries_analiticos import top_productos

        resultado = top_productos(db_con_datos, top_n=3)

        # Laptop: 2940 + 1770 = 4710
        # Silla: 2063.2
        # Mouse: 440.8 + 893.6 = 1334.4
        assert resultado.iloc[0]["nombre_producto"] == "Laptop Dell XPS"
        assert resultado.iloc[1]["nombre_producto"] == "Silla Ergonómica"
        assert resultado.iloc[2]["nombre_producto"] == "Mouse Logitech MX"


class TestVentasPorMes:
    """Tests para ventas_por_mes()."""

    def test_retorna_dataframe(self, db_con_datos):
        """Should return a DataFrame."""
        from src.queries_analiticos import ventas_por_mes

        resultado = ventas_por_mes(db_con_datos)

        assert isinstance(resultado, pd.DataFrame)

    def test_columnas_esperadas(self, db_con_datos):
        """Should have expected columns."""
        from src.queries_analiticos import ventas_por_mes

        resultado = ventas_por_mes(db_con_datos)

        assert "anio" in resultado.columns
        assert "mes" in resultado.columns
        assert "mes_nombre" in resultado.columns
        assert "total_ventas" in resultado.columns
        assert "num_transacciones" in resultado.columns

    def test_agrupa_por_mes_correctamente(self, db_con_datos):
        """Should group by month correctly."""
        from src.queries_analiticos import ventas_por_mes

        resultado = ventas_por_mes(db_con_datos)

        assert len(resultado) == 3  # 3 meses

        # Enero: 2940 + 440.8 = 3380.8
        enero = resultado[resultado["mes"] == 1].iloc[0]
        assert enero["total_ventas"] == pytest.approx(3380.8, abs=0.1)
        assert enero["num_transacciones"] == 2

        # Febrero: 1770 + 2063.2 = 3833.2
        febrero = resultado[resultado["mes"] == 2].iloc[0]
        assert febrero["total_ventas"] == pytest.approx(3833.2, abs=0.1)

        # Marzo: 893.6
        marzo = resultado[resultado["mes"] == 3].iloc[0]
        assert marzo["total_ventas"] == pytest.approx(893.6, abs=0.1)

    def test_ordena_por_fecha_cronologica(self, db_con_datos):
        """Should order by date chronologically."""
        from src.queries_analiticos import ventas_por_mes

        resultado = ventas_por_mes(db_con_datos)

        assert resultado.iloc[0]["mes"] == 1
        assert resultado.iloc[1]["mes"] == 2
        assert resultado.iloc[2]["mes"] == 3


class TestAnalisisVendedores:
    """Tests para analisis_vendedores()."""

    def test_retorna_dataframe(self, db_con_datos):
        """Should return a DataFrame."""
        from src.queries_analiticos import analisis_vendedores

        resultado = analisis_vendedores(db_con_datos)

        assert isinstance(resultado, pd.DataFrame)

    def test_columnas_esperadas(self, db_con_datos):
        """Should have expected columns."""
        from src.queries_analiticos import analisis_vendedores

        resultado = analisis_vendedores(db_con_datos)

        assert "nombre" in resultado.columns
        assert "region" in resultado.columns
        assert "total_ventas" in resultado.columns
        assert "num_transacciones" in resultado.columns
        assert "ticket_promedio" in resultado.columns

    def test_calcula_metricas_vendedores(self, db_con_datos):
        """Should calculate vendor metrics correctly."""
        from src.queries_analiticos import analisis_vendedores

        resultado = analisis_vendedores(db_con_datos)

        # Juan (vendedor_id=1): 2940 + 440.8 + 893.6 = 4274.4 (3 transacciones)
        juan = resultado[resultado["nombre"] == "Juan Pérez"].iloc[0]
        assert juan["total_ventas"] == pytest.approx(4274.4, abs=0.1)
        assert juan["num_transacciones"] == 3
        assert juan["ticket_promedio"] == pytest.approx(4274.4 / 3, abs=0.1)

        # María (vendedor_id=2): 1770 + 2063.2 = 3833.2 (2 transacciones)
        maria = resultado[resultado["nombre"] == "María López"].iloc[0]
        assert maria["total_ventas"] == pytest.approx(3833.2, abs=0.1)
        assert maria["num_transacciones"] == 2

    def test_ordena_por_total_ventas(self, db_con_datos):
        """Should order by total sales descending."""
        from src.queries_analiticos import analisis_vendedores

        resultado = analisis_vendedores(db_con_datos)

        assert resultado.iloc[0]["nombre"] == "Juan Pérez"


class TestClientesFrecuentes:
    """Tests para clientes_frecuentes()."""

    def test_retorna_dataframe(self, db_con_datos):
        """Should return a DataFrame."""
        from src.queries_analiticos import clientes_frecuentes

        resultado = clientes_frecuentes(db_con_datos, top_n=3)

        assert isinstance(resultado, pd.DataFrame)

    def test_limita_resultados(self, db_con_datos):
        """Should limit results to top_n."""
        from src.queries_analiticos import clientes_frecuentes

        resultado = clientes_frecuentes(db_con_datos, top_n=2)

        assert len(resultado) <= 2

    def test_columnas_esperadas(self, db_con_datos):
        """Should have expected columns."""
        from src.queries_analiticos import clientes_frecuentes

        resultado = clientes_frecuentes(db_con_datos, top_n=3)

        assert "nombre" in resultado.columns
        assert "segmento" in resultado.columns
        assert "ciudad" in resultado.columns
        assert "total_compras" in resultado.columns
        assert "num_transacciones" in resultado.columns

    def test_calcula_metricas_clientes(self, db_con_datos):
        """Should calculate customer metrics correctly."""
        from src.queries_analiticos import clientes_frecuentes

        resultado = clientes_frecuentes(db_con_datos, top_n=3)

        # Cliente A: 2 transacciones (2940 + 1770 = 4710)
        # Cliente B: 2 transacciones (440.8 + 893.6 = 1334.4)
        # Cliente C: 1 transacción (2063.2)
        cliente_a = resultado[resultado["nombre"] == "Cliente A"].iloc[0]
        assert cliente_a["num_transacciones"] == 2
        assert cliente_a["total_compras"] == pytest.approx(4710.0, abs=0.1)

    def test_ordena_por_total_compras(self, db_con_datos):
        """Should order by total purchases descending."""
        from src.queries_analiticos import clientes_frecuentes

        resultado = clientes_frecuentes(db_con_datos, top_n=3)

        assert resultado.iloc[0]["nombre"] == "Cliente A"


class TestKPIsDashboard:
    """Tests para kpis_dashboard()."""

    def test_retorna_diccionario(self, db_con_datos):
        """Should return a dictionary."""
        from src.queries_analiticos import kpis_dashboard

        resultado = kpis_dashboard(db_con_datos)

        assert isinstance(resultado, dict)

    def test_contiene_kpis_esperados(self, db_con_datos):
        """Should contain expected KPIs."""
        from src.queries_analiticos import kpis_dashboard

        resultado = kpis_dashboard(db_con_datos)

        assert "total_ventas" in resultado
        assert "num_transacciones" in resultado
        assert "ticket_promedio" in resultado
        assert "num_clientes_activos" in resultado
        assert "num_productos_vendidos" in resultado
        assert "categoria_top" in resultado

    def test_calcula_kpis_correctamente(self, db_con_datos):
        """Should calculate KPIs correctly."""
        from src.queries_analiticos import kpis_dashboard

        resultado = kpis_dashboard(db_con_datos)

        # Total ventas: 2940 + 440.8 + 1770 + 2063.2 + 893.6 = 8107.6
        assert resultado["total_ventas"] == pytest.approx(8107.6, abs=0.1)

        # Transacciones: 5
        assert resultado["num_transacciones"] == 5

        # Ticket promedio: 8107.6 / 5 = 1621.52
        assert resultado["ticket_promedio"] == pytest.approx(1621.52, abs=0.1)

        # Clientes activos: 3 (Cliente A, B, C)
        assert resultado["num_clientes_activos"] == 3

        # Productos vendidos únicos: 3 (Laptop, Mouse, Silla)
        assert resultado["num_productos_vendidos"] == 3

        # Categoría top: Electrónica (6044.4)
        assert resultado["categoria_top"] == "Electrónica"


class TestFiltrosYDrillDown:
    """Tests para capacidades de drill-down y filtros."""

    def test_ventas_por_categoria_con_filtro_anio(self, db_con_datos):
        """Should support year filtering."""
        from src.queries_analiticos import ventas_por_categoria

        # Esta funcionalidad se puede agregar opcionalmente
        # Por ahora, verificar que acepta parámetros adicionales
        resultado = ventas_por_categoria(db_con_datos, anio=2024)

        assert isinstance(resultado, pd.DataFrame)

    def test_ventas_por_mes_con_filtro_trimestre(self, db_con_datos):
        """Should support quarter filtering."""
        from src.queries_analiticos import ventas_por_mes

        resultado = ventas_por_mes(db_con_datos, trimestre=1)

        assert isinstance(resultado, pd.DataFrame)
        assert len(resultado) <= 3  # Max 3 meses en trimestre
