"""
Tests para el módulo generador_reportes.

TDD: Estos tests se escribieron PRIMERO, antes de la implementación.
"""

import pytest
from src.generador_reportes import (
    generar_analisis_categorias,
    generar_reporte_ventas,
    generar_top_clientes,
)


class TestGenerarReporteVentas:
    """Tests para la función generar_reporte_ventas."""

    def test_reporte_por_categoria_agrupa_correctamente(self, conexion_db):
        """Reporte agrupado por categoría debe funcionar."""
        reporte = generar_reporte_ventas(
            conexion=conexion_db,
            fecha_inicio="2025-01-01",
            fecha_fin="2025-12-31",
            agrupar_por="categoria",
        )

        assert len(reporte) > 0

        # Verificar estructura
        for fila in reporte:
            assert "nombre" in fila
            assert "total_ventas" in fila
            assert "unidades_vendidas" in fila
            assert "ticket_promedio" in fila

    def test_reporte_por_producto_muestra_productos_individuales(self, conexion_db):
        """Reporte agrupado por producto debe mostrar cada producto."""
        reporte = generar_reporte_ventas(
            conexion=conexion_db,
            fecha_inicio="2025-01-01",
            fecha_fin="2025-12-31",
            agrupar_por="producto",
        )

        assert len(reporte) > 0

        # Debe haber al menos un producto vendido
        nombres_productos = [fila["nombre"] for fila in reporte]
        assert len(nombres_productos) > 0

    def test_reporte_con_rango_fechas_limita_resultados(self, conexion_db):
        """Rango de fechas debe filtrar ventas correctamente."""
        # Solo ventas de enero
        reporte_enero = generar_reporte_ventas(
            conexion=conexion_db,
            fecha_inicio="2025-01-01",
            fecha_fin="2025-01-31",
            agrupar_por="categoria",
        )

        # Todas las ventas
        reporte_completo = generar_reporte_ventas(
            conexion=conexion_db,
            fecha_inicio="2025-01-01",
            fecha_fin="2025-12-31",
            agrupar_por="categoria",
        )

        # Verificar que hay diferencia
        total_enero = sum(fila["total_ventas"] for fila in reporte_enero)
        total_completo = sum(fila["total_ventas"] for fila in reporte_completo)

        assert total_enero < total_completo

    def test_agrupar_por_invalido_lanza_valor_error(self, conexion_db):
        """Agrupación inválida debe lanzar ValueError."""
        with pytest.raises(ValueError, match="agrupar_por inválido"):
            generar_reporte_ventas(
                conexion=conexion_db,
                fecha_inicio="2025-01-01",
                fecha_fin="2025-12-31",
                agrupar_por="INVALID_GROUP",
            )

    def test_fecha_inicio_mayor_a_fin_lanza_valor_error(self, conexion_db):
        """Fecha inicio > fin debe lanzar ValueError."""
        with pytest.raises(ValueError, match="fecha_inicio debe ser menor"):
            generar_reporte_ventas(
                conexion=conexion_db,
                fecha_inicio="2025-12-31",
                fecha_fin="2025-01-01",
                agrupar_por="categoria",
            )

    def test_reporte_ordenado_por_ventas_desc(self, conexion_db):
        """Reporte debe estar ordenado por ventas DESC."""
        reporte = generar_reporte_ventas(
            conexion=conexion_db,
            fecha_inicio="2025-01-01",
            fecha_fin="2025-12-31",
            agrupar_por="categoria",
        )

        # Verificar orden descendente
        ventas = [fila["total_ventas"] for fila in reporte]
        assert ventas == sorted(ventas, reverse=True)


class TestGenerarTopClientes:
    """Tests para la función generar_top_clientes."""

    def test_top_3_clientes_retorna_3_filas(self, conexion_db):
        """Top 3 debe retornar máximo 3 clientes."""
        top_clientes = generar_top_clientes(
            conexion=conexion_db, top_n=3, metrica="gasto_total"
        )

        assert len(top_clientes) <= 3
        assert len(top_clientes) > 0

    def test_top_clientes_por_gasto_total_ordenado_desc(self, conexion_db):
        """Top clientes por gasto debe estar ordenado DESC."""
        top_clientes = generar_top_clientes(
            conexion=conexion_db, top_n=5, metrica="gasto_total"
        )

        gastos = [fila["gasto_total"] for fila in top_clientes]
        assert gastos == sorted(gastos, reverse=True)

    def test_top_clientes_incluye_segmentacion(self, conexion_db):
        """Resultado debe incluir segmento (VIP/Regular/Nuevo)."""
        top_clientes = generar_top_clientes(
            conexion=conexion_db, top_n=5, metrica="gasto_total"
        )

        for fila in top_clientes:
            assert "segmento" in fila
            assert fila["segmento"] in ["VIP", "Regular", "Nuevo"]

    def test_metrica_invalida_lanza_valor_error(self, conexion_db):
        """Métrica inválida debe lanzar ValueError."""
        with pytest.raises(ValueError, match="metrica inválida"):
            generar_top_clientes(
                conexion=conexion_db, top_n=5, metrica="INVALID_METRIC"
            )

    def test_top_n_negativo_lanza_valor_error(self, conexion_db):
        """top_n negativo debe lanzar ValueError."""
        with pytest.raises(ValueError, match="top_n debe ser positivo"):
            generar_top_clientes(conexion=conexion_db, top_n=-1, metrica="gasto_total")


class TestGenerarAnalisisCategorias:
    """Tests para la función generar_analisis_categorias."""

    def test_analisis_incluye_todas_categorias(self, conexion_db):
        """Análisis debe incluir todas las categorías."""
        analisis = generar_analisis_categorias(conexion=conexion_db)

        # Debe haber 4 categorías
        assert len(analisis) == 4

    def test_analisis_incluye_metricas_clave(self, conexion_db):
        """Análisis debe incluir todas las métricas esperadas."""
        analisis = generar_analisis_categorias(conexion=conexion_db)

        primera_fila = analisis[0]

        # Verificar columnas esperadas
        assert "categoria" in primera_fila
        assert "num_productos" in primera_fila
        assert "stock_total" in primera_fila
        assert "valor_inventario" in primera_fila
        assert "ingresos_totales" in primera_fila
        assert "clasificacion" in primera_fila
        assert "estado_stock" in primera_fila

    def test_clasificacion_rentabilidad_usa_case_when(self, conexion_db):
        """Clasificación debe usar lógica de CASE WHEN."""
        analisis = generar_analisis_categorias(conexion=conexion_db)

        clasificaciones = [fila["clasificacion"] for fila in analisis]

        # Debe haber clasificaciones definidas
        assert all(
            c in ["Alta rentabilidad", "Media rentabilidad", "Baja rentabilidad"]
            for c in clasificaciones
        )

    def test_estado_stock_categorizado(self, conexion_db):
        """Estado de stock debe estar categorizado."""
        analisis = generar_analisis_categorias(conexion=conexion_db)

        estados = [fila["estado_stock"] for fila in analisis]

        # Debe haber estados definidos
        assert all(
            e in ["Crítico", "Normal", "Sobrecargado", "Sin stock"] for e in estados
        )

    def test_analisis_ordenado_por_ingresos_desc(self, conexion_db):
        """Análisis debe estar ordenado por ingresos DESC."""
        analisis = generar_analisis_categorias(conexion=conexion_db)

        ingresos = [fila["ingresos_totales"] for fila in analisis]
        assert ingresos == sorted(ingresos, reverse=True)
