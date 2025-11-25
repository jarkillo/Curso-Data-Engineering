"""
Tests para el módulo glue_transformations.py

Tests exhaustivos para funciones de transformación ETL.
"""

import pytest

from src.glue_transformations import (
    agregar_categoria_status,
    agregar_columna_fecha,
    calcular_metricas_por_endpoint,
    convertir_a_parquet_schema,
    eliminar_duplicados,
    filtrar_por_rango_fechas,
    limpiar_nulls,
    normalizar_timestamps,
)


class TestLimpiarNulls:
    """Tests para limpiar_nulls()"""

    def test_limpiar_nulls_sin_nulls(self):
        """Debe mantener todos los registros si no hay nulls"""
        datos = [
            {
                "timestamp": "2025-01-15T10:30:45Z",
                "endpoint": "/api/users",
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 145,
            },
            {
                "timestamp": "2025-01-15T10:30:46Z",
                "endpoint": "/api/posts",
                "method": "POST",
                "status_code": 201,
                "response_time_ms": 234,
            },
        ]

        resultado = limpiar_nulls(datos)

        assert len(resultado) == 2
        assert resultado == datos

    def test_limpiar_nulls_con_nulls_en_campos_criticos(self):
        """Debe eliminar registros con nulls en campos críticos"""
        datos = [
            {
                "timestamp": "2025-01-15T10:30:45Z",
                "endpoint": "/api/users",
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 145,
            },
            {
                "timestamp": None,  # Null en campo crítico
                "endpoint": "/api/posts",
                "method": "POST",
                "status_code": 201,
                "response_time_ms": 234,
            },
            {
                "timestamp": "2025-01-15T10:30:47Z",
                "endpoint": None,  # Null en campo crítico
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 89,
            },
        ]

        resultado = limpiar_nulls(datos)

        assert len(resultado) == 1
        assert resultado[0]["timestamp"] == "2025-01-15T10:30:45Z"

    def test_limpiar_nulls_lista_vacia(self):
        """Debe manejar lista vacía correctamente"""
        datos = []

        resultado = limpiar_nulls(datos)

        assert resultado == []


class TestNormalizarTimestamps:
    """Tests para normalizar_timestamps()"""

    def test_normalizar_timestamps_formato_estandar(self):
        """Debe normalizar timestamps al formato ISO 8601 UTC"""
        datos = [
            {"timestamp": "2025-01-15 10:30:45", "endpoint": "/api/users"},
            {"timestamp": "2025-01-15T10:30:46Z", "endpoint": "/api/posts"},
        ]

        resultado = normalizar_timestamps(datos)

        # Ambos deben tener formato ISO 8601
        assert "T" in resultado[0]["timestamp"]
        assert "Z" in resultado[0]["timestamp"] or "+" in resultado[0]["timestamp"]

    def test_normalizar_timestamps_ya_normalizados(self):
        """Debe mantener timestamps ya normalizados"""
        datos = [
            {"timestamp": "2025-01-15T10:30:45Z", "endpoint": "/api/users"},
        ]

        resultado = normalizar_timestamps(datos)

        assert resultado[0]["timestamp"] == "2025-01-15T10:30:45Z"


class TestCalcularMetricasPorEndpoint:
    """Tests para calcular_metricas_por_endpoint()"""

    def test_calcular_metricas_basicas(self):
        """Debe calcular métricas básicas correctamente"""
        logs = [
            {
                "endpoint": "/api/users",
                "response_time_ms": 100,
                "status_code": 200,
            },
            {
                "endpoint": "/api/users",
                "response_time_ms": 150,
                "status_code": 200,
            },
            {
                "endpoint": "/api/users",
                "response_time_ms": 200,
                "status_code": 200,
            },
        ]

        metricas = calcular_metricas_por_endpoint(logs)

        assert "/api/users" in metricas
        assert metricas["/api/users"]["avg_response_time"] == 150.0
        assert metricas["/api/users"]["total_requests"] == 3
        assert metricas["/api/users"]["error_rate"] == 0.0

    def test_calcular_metricas_con_errores(self):
        """Debe calcular correctamente la tasa de errores"""
        logs = [
            {"endpoint": "/api/users", "response_time_ms": 100, "status_code": 200},
            {"endpoint": "/api/users", "response_time_ms": 150, "status_code": 404},
            {"endpoint": "/api/users", "response_time_ms": 200, "status_code": 500},
        ]

        metricas = calcular_metricas_por_endpoint(logs)

        # 2 de 3 son errores (404, 500) = 66.67%
        assert abs(metricas["/api/users"]["error_rate"] - 66.67) < 0.1

    def test_calcular_metricas_multiples_endpoints(self):
        """Debe calcular métricas para múltiples endpoints"""
        logs = [
            {"endpoint": "/api/users", "response_time_ms": 100, "status_code": 200},
            {"endpoint": "/api/posts", "response_time_ms": 50, "status_code": 200},
            {"endpoint": "/api/users", "response_time_ms": 150, "status_code": 200},
        ]

        metricas = calcular_metricas_por_endpoint(logs)

        assert "/api/users" in metricas
        assert "/api/posts" in metricas
        assert metricas["/api/users"]["total_requests"] == 2
        assert metricas["/api/posts"]["total_requests"] == 1

    def test_calcular_percentiles(self):
        """Debe calcular percentiles correctamente"""
        logs = [
            {
                "endpoint": "/api/users",
                "response_time_ms": i * 10,
                "status_code": 200,
            }
            for i in range(1, 101)  # 10, 20, 30, ..., 1000
        ]

        metricas = calcular_metricas_por_endpoint(logs)

        assert "p50_response_time" in metricas["/api/users"]
        assert "p95_response_time" in metricas["/api/users"]
        assert "p99_response_time" in metricas["/api/users"]


class TestAgregarColumnaFecha:
    """Tests para agregar_columna_fecha()"""

    def test_agregar_columnas_fecha_correctamente(self):
        """Debe extraer year, month, day del timestamp"""
        datos = [
            {"timestamp": "2025-01-15T10:30:45Z", "endpoint": "/api/users"},
            {"timestamp": "2025-12-31T23:59:59Z", "endpoint": "/api/posts"},
        ]

        resultado = agregar_columna_fecha(datos)

        assert resultado[0]["year"] == "2025"
        assert resultado[0]["month"] == "01"
        assert resultado[0]["day"] == "15"

        assert resultado[1]["year"] == "2025"
        assert resultado[1]["month"] == "12"
        assert resultado[1]["day"] == "31"

    def test_agregar_columna_fecha_no_modifica_original(self):
        """No debe modificar los datos originales (función pura)"""
        datos = [{"timestamp": "2025-01-15T10:30:45Z", "endpoint": "/api/users"}]

        resultado = agregar_columna_fecha(datos)

        assert "year" not in datos[0]  # Original no modificado
        assert "year" in resultado[0]  # Resultado sí tiene year


class TestConvertirAParquetSchema:
    """Tests para convertir_a_parquet_schema()"""

    def test_convertir_a_formato_columnar(self):
        """Debe convertir de row-oriented a columnar"""
        datos = [
            {"endpoint": "/api/users", "status_code": 200},
            {"endpoint": "/api/posts", "status_code": 404},
        ]

        columnar = convertir_a_parquet_schema(datos)

        assert "endpoint" in columnar
        assert "status_code" in columnar
        assert columnar["endpoint"] == ["/api/users", "/api/posts"]
        assert columnar["status_code"] == [200, 404]

    def test_convertir_lista_vacia(self):
        """Debe manejar lista vacía"""
        datos = []

        columnar = convertir_a_parquet_schema(datos)

        assert columnar == {}


class TestFiltrarPorRangoFechas:
    """Tests para filtrar_por_rango_fechas()"""

    def test_filtrar_dentro_del_rango(self):
        """Debe mantener solo registros dentro del rango"""
        datos = [
            {"timestamp": "2025-01-10T10:30:45Z"},
            {"timestamp": "2025-01-15T10:30:45Z"},
            {"timestamp": "2025-01-20T10:30:45Z"},
            {"timestamp": "2025-01-25T10:30:45Z"},
        ]

        resultado = filtrar_por_rango_fechas(datos, "2025-01-14", "2025-01-20")

        assert len(resultado) == 2
        assert "2025-01-15" in resultado[0]["timestamp"]
        assert "2025-01-20" in resultado[1]["timestamp"]

    def test_filtrar_rango_vacio(self):
        """Debe retornar lista vacía si no hay registros en el rango"""
        datos = [
            {"timestamp": "2025-01-10T10:30:45Z"},
        ]

        resultado = filtrar_por_rango_fechas(datos, "2025-01-20", "2025-01-25")

        assert len(resultado) == 0


class TestAgregarCategoriaStatus:
    """Tests para agregar_categoria_status()"""

    @pytest.mark.parametrize(
        "status_code,categoria_esperada",
        [
            (100, "1xx"),
            (200, "2xx"),
            (201, "2xx"),
            (301, "3xx"),
            (404, "4xx"),
            (500, "5xx"),
        ],
    )
    def test_agregar_categoria_correcta(self, status_code, categoria_esperada):
        """Debe asignar la categoría correcta según status code"""
        datos = [{"status_code": status_code}]

        resultado = agregar_categoria_status(datos)

        assert resultado[0]["status_category"] == categoria_esperada


class TestEliminarDuplicados:
    """Tests para eliminar_duplicados()"""

    def test_eliminar_duplicados_por_campos_clave(self):
        """Debe eliminar registros duplicados según campos clave"""
        datos = [
            {"timestamp": "2025-01-15T10:30:45Z", "user_id": "user_1"},
            {"timestamp": "2025-01-15T10:30:45Z", "user_id": "user_1"},  # Duplicado
            {"timestamp": "2025-01-15T10:30:46Z", "user_id": "user_2"},
        ]

        resultado = eliminar_duplicados(datos, ["timestamp", "user_id"])

        assert len(resultado) == 2

    def test_eliminar_duplicados_sin_duplicados(self):
        """Debe mantener todos si no hay duplicados"""
        datos = [
            {"timestamp": "2025-01-15T10:30:45Z", "user_id": "user_1"},
            {"timestamp": "2025-01-15T10:30:46Z", "user_id": "user_2"},
        ]

        resultado = eliminar_duplicados(datos, ["timestamp", "user_id"])

        assert len(resultado) == 2

    def test_eliminar_duplicados_orden_preservado(self):
        """Debe preservar el orden original (primer registro)"""
        datos = [
            {"id": 1, "user_id": "user_1"},
            {"id": 2, "user_id": "user_1"},  # Duplicado
            {"id": 3, "user_id": "user_2"},
        ]

        resultado = eliminar_duplicados(datos, ["user_id"])

        assert resultado[0]["id"] == 1  # Primer registro se mantiene
        assert resultado[1]["id"] == 3


# Fixtures
@pytest.fixture
def logs_sample():
    """Fixture con logs de ejemplo"""
    return [
        {
            "timestamp": "2025-01-15T10:30:45Z",
            "endpoint": "/api/users",
            "method": "GET",
            "status_code": 200,
            "response_time_ms": 145,
            "user_id": "user_1",
            "ip_address": "192.168.1.1",
        },
        {
            "timestamp": "2025-01-15T10:30:46Z",
            "endpoint": "/api/posts",
            "method": "GET",
            "status_code": 200,
            "response_time_ms": 89,
            "user_id": "user_2",
            "ip_address": "192.168.1.2",
        },
    ]
