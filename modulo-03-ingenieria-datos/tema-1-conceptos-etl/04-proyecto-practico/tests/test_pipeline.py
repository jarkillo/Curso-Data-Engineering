"""Tests para el módulo pipeline (orquestación completa)."""

import pytest

from src.carga import consultar_ventas_por_fecha, crear_tabla_ventas
from src.pipeline import pipeline_etl, pipeline_etl_con_reintentos


class TestPipelineEtl:
    """Tests para la función pipeline_etl."""

    def test_pipeline_completo_con_datos_validos(self, tmp_path):
        """Debe ejecutar el pipeline completo correctamente."""
        # Crear archivos CSV de prueba
        directorio_datos = tmp_path / "datos"
        directorio_datos.mkdir()

        (directorio_datos / "ventas.csv").write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-01,101,1001,2,100.0\n"
            "2,2025-10-01,102,1002,5,20.0\n",
            encoding="utf-8",
        )
        (directorio_datos / "productos.csv").write_text(
            "producto_id,nombre,categoria,stock\n"
            "101,Laptop,Computadoras,50\n"
            "102,Mouse,Accesorios,200\n",
            encoding="utf-8",
        )
        (directorio_datos / "clientes.csv").write_text(
            "cliente_id,nombre,email,ciudad\n"
            "1001,Juan Perez,juan@example.com,Madrid\n"
            "1002,Maria Garcia,maria@example.com,Barcelona\n",
            encoding="utf-8",
        )

        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        # Ejecutar pipeline
        metricas = pipeline_etl(
            fecha="2025-10-01",
            directorio_datos=str(directorio_datos),
            db_path=str(db_path),
        )

        # Verificar métricas
        assert metricas["fecha"] == "2025-10-01"
        assert metricas["filas_extraidas"] == 2
        assert metricas["filas_validas"] == 2
        assert metricas["filas_cargadas"] == 2
        assert metricas["estado"] == "EXITOSO"
        assert metricas["tiempo_segundos"] > 0

        # Verificar que los datos se cargaron
        ventas_cargadas = consultar_ventas_por_fecha("2025-10-01", str(db_path))
        assert len(ventas_cargadas) == 2
        assert ventas_cargadas[0]["total"] == 200.0
        assert ventas_cargadas[0]["nombre_producto"] == "Laptop"
        assert ventas_cargadas[0]["nombre_cliente"] == "Juan Perez"

    def test_pipeline_es_idempotente(self, tmp_path):
        """Debe ser idempotente: ejecutar 2 veces no duplica."""
        directorio_datos = tmp_path / "datos"
        directorio_datos.mkdir()

        (directorio_datos / "ventas.csv").write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-01,101,1001,2,100.0\n",
            encoding="utf-8",
        )
        (directorio_datos / "productos.csv").write_text(
            "producto_id,nombre,categoria,stock\n101,Laptop,Computadoras,50\n",
            encoding="utf-8",
        )
        (directorio_datos / "clientes.csv").write_text(
            "cliente_id,nombre,email,ciudad\n1001,Juan,juan@example.com,Madrid\n",
            encoding="utf-8",
        )

        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        # Ejecutar pipeline 2 veces
        pipeline_etl("2025-10-01", str(directorio_datos), str(db_path))
        pipeline_etl("2025-10-01", str(directorio_datos), str(db_path))

        # Debe haber solo 1 fila
        ventas = consultar_ventas_por_fecha("2025-10-01", str(db_path))
        assert len(ventas) == 1

    def test_pipeline_con_datos_invalidos_retorna_error(self, tmp_path):
        """Debe retornar estado ERROR si hay datos inválidos."""
        directorio_datos = tmp_path / "datos"
        directorio_datos.mkdir()

        # Ventas con cantidad negativa (inválido)
        (directorio_datos / "ventas.csv").write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-01,101,1001,-2,100.0\n",
            encoding="utf-8",
        )
        (directorio_datos / "productos.csv").write_text(
            "producto_id,nombre,categoria,stock\n101,Laptop,Computadoras,50\n",
            encoding="utf-8",
        )
        (directorio_datos / "clientes.csv").write_text(
            "cliente_id,nombre,email,ciudad\n1001,Juan,juan@example.com,Madrid\n",
            encoding="utf-8",
        )

        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        # Ejecutar pipeline
        metricas = pipeline_etl("2025-10-01", str(directorio_datos), str(db_path))

        # Debe retornar estado ERROR
        assert metricas["estado"] == "ERROR"
        assert len(metricas["errores"]) > 0

    def test_pipeline_sin_datos_para_fecha_retorna_sin_datos(self, tmp_path):
        """Debe retornar estado SIN_DATOS si no hay ventas para la fecha."""
        directorio_datos = tmp_path / "datos"
        directorio_datos.mkdir()

        # Ventas de otra fecha
        (directorio_datos / "ventas.csv").write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-02,101,1001,2,100.0\n",
            encoding="utf-8",
        )
        (directorio_datos / "productos.csv").write_text(
            "producto_id,nombre,categoria,stock\n101,Laptop,Computadoras,50\n",
            encoding="utf-8",
        )
        (directorio_datos / "clientes.csv").write_text(
            "cliente_id,nombre,email,ciudad\n1001,Juan,juan@example.com,Madrid\n",
            encoding="utf-8",
        )

        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        # Buscar fecha que no tiene datos
        metricas = pipeline_etl("2025-10-01", str(directorio_datos), str(db_path))

        assert metricas["estado"] == "SIN_DATOS"
        assert metricas["filas_extraidas"] == 0


class TestPipelineEtlConReintentos:
    """Tests para la función pipeline_etl_con_reintentos."""

    def test_ejecuta_pipeline_exitosamente(self, tmp_path):
        """Debe ejecutar el pipeline exitosamente sin reintentos."""
        directorio_datos = tmp_path / "datos"
        directorio_datos.mkdir()

        (directorio_datos / "ventas.csv").write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-01,101,1001,2,100.0\n",
            encoding="utf-8",
        )
        (directorio_datos / "productos.csv").write_text(
            "producto_id,nombre,categoria,stock\n101,Laptop,Computadoras,50\n",
            encoding="utf-8",
        )
        (directorio_datos / "clientes.csv").write_text(
            "cliente_id,nombre,email,ciudad\n1001,Juan,juan@example.com,Madrid\n",
            encoding="utf-8",
        )

        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        metricas = pipeline_etl_con_reintentos(
            fecha="2025-10-01",
            directorio_datos=str(directorio_datos),
            db_path=str(db_path),
            max_intentos=3,
        )

        assert metricas["estado"] == "EXITOSO"

    def test_reintenta_si_falla_por_archivo_inexistente(self, tmp_path):
        """Debe lanzar excepción después de reintentos si falla."""
        db_path = tmp_path / "test.db"
        crear_tabla_ventas(str(db_path))

        # Directorio que no existe
        directorio_inexistente = tmp_path / "datos_que_no_existen"

        with pytest.raises(FileNotFoundError):
            pipeline_etl_con_reintentos(
                fecha="2025-10-01",
                directorio_datos=str(directorio_inexistente),
                db_path=str(db_path),
                max_intentos=2,
            )
