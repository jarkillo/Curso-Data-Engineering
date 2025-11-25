"""
Tests para el módulo athena_queries.py

Tests exhaustivos para generación de queries SQL de Athena.
"""

import pytest

from src.athena_queries import (
    ejecutar_query_athena_simulado,
    generar_query_distribucion_errores,
    generar_query_metricas_basicas,
    generar_query_percentiles,
    generar_query_tendencia_temporal,
    generar_query_top_endpoints_lentos,
    generar_vista_metricas_diarias,
    parsear_resultados_athena,
)


class TestGenerarQueryMetricasBasicas:
    """Tests para generar_query_metricas_basicas()"""

    def test_generar_query_con_parametros_validos(self):
        """Debe generar una query SQL válida"""
        query = generar_query_metricas_basicas(
            "cloudapi_analytics", "logs_processed", "2025-01-15", "2025-01-20"
        )

        assert "SELECT" in query
        assert "FROM cloudapi_analytics.logs_processed" in query
        assert "2025-01-15" in query
        assert "2025-01-20" in query

    def test_query_contiene_metricas_esperadas(self):
        """Debe incluir cálculo de métricas básicas"""
        query = generar_query_metricas_basicas(
            "db", "tabla", "2025-01-01", "2025-01-31"
        )

        # Verificar que incluya métricas básicas
        assert "COUNT" in query.upper()
        assert "AVG" in query.upper() or "AVERAGE" in query.upper()

    def test_query_incluye_filtro_de_fechas(self):
        """Debe incluir WHERE clause para filtrar por fechas"""
        query = generar_query_metricas_basicas(
            "db", "tabla", "2025-01-15", "2025-01-20"
        )

        assert "WHERE" in query
        assert "timestamp" in query.lower() or "date" in query.lower()


class TestGenerarQueryPercentiles:
    """Tests para generar_query_percentiles()"""

    def test_generar_query_percentiles_general(self):
        """Debe generar query para percentiles de todos los endpoints"""
        query = generar_query_percentiles("cloudapi_analytics", "logs_processed")

        assert "SELECT" in query
        assert "FROM cloudapi_analytics.logs_processed" in query
        # Debe contener funciones de percentil
        assert (
            "APPROX_PERCENTILE" in query.upper()
            or "PERCENTILE" in query.upper()
            or "QUANTILE" in query.upper()
        )

    def test_generar_query_percentiles_endpoint_especifico(self):
        """Debe generar query para un endpoint específico"""
        query = generar_query_percentiles(
            "cloudapi_analytics", "logs_processed", endpoint="/api/users"
        )

        assert "/api/users" in query
        assert "WHERE" in query

    def test_query_incluye_p50_p95_p99(self):
        """Debe calcular p50, p95 y p99"""
        query = generar_query_percentiles("db", "tabla")

        # Verificar que mencione los percentiles clave
        assert "50" in query or "0.5" in query  # p50
        assert "95" in query or "0.95" in query  # p95
        assert "99" in query or "0.99" in query  # p99


class TestGenerarQueryTopEndpointsLentos:
    """Tests para generar_query_top_endpoints_lentos()"""

    def test_generar_query_con_limite(self):
        """Debe generar query con LIMIT"""
        query = generar_query_top_endpoints_lentos(
            "cloudapi_analytics", "logs_processed", limite=10
        )

        assert "LIMIT 10" in query
        assert "ORDER BY" in query

    def test_query_ordena_por_response_time(self):
        """Debe ordenar por response time descendente"""
        query = generar_query_top_endpoints_lentos("db", "tabla", limite=5)

        assert "ORDER BY" in query
        assert "DESC" in query or "desc" in query
        assert "response_time" in query.lower()


class TestGenerarQueryTendenciaTemporal:
    """Tests para generar_query_tendencia_temporal()"""

    @pytest.mark.parametrize("intervalo", ["hour", "day", "minute"])
    def test_generar_query_con_diferentes_intervalos(self, intervalo):
        """Debe generar query con diferentes intervalos temporales"""
        query = generar_query_tendencia_temporal("db", "tabla", intervalo=intervalo)

        assert "SELECT" in query
        assert "GROUP BY" in query

    def test_query_incluye_funcion_temporal(self):
        """Debe incluir funciones de truncamiento temporal"""
        query = generar_query_tendencia_temporal("db", "tabla", "hour")

        # Debe incluir alguna función de tiempo
        funciones_tiempo = ["DATE_TRUNC", "TRUNC", "HOUR", "DAY", "DATE_FORMAT"]
        assert any(func in query.upper() for func in funciones_tiempo)


class TestGenerarQueryDistribucionErrores:
    """Tests para generar_query_distribucion_errores()"""

    def test_generar_query_distribucion_errores(self):
        """Debe generar query para analizar distribución de errores"""
        query = generar_query_distribucion_errores(
            "cloudapi_analytics", "logs_processed"
        )

        assert "SELECT" in query
        assert "status_code" in query.lower()
        assert "GROUP BY" in query

    def test_query_agrupa_por_status_code(self):
        """Debe agrupar por status_code"""
        query = generar_query_distribucion_errores("db", "tabla")

        assert "GROUP BY" in query
        assert "status_code" in query.lower()


class TestGenerarVistaMetricasDiarias:
    """Tests para generar_vista_metricas_diarias()"""

    def test_generar_vista_con_create_or_replace(self):
        """Debe incluir CREATE OR REPLACE VIEW"""
        query = generar_vista_metricas_diarias("cloudapi_analytics", "logs_processed")

        assert "CREATE" in query.upper()
        assert "VIEW" in query.upper()
        assert "OR REPLACE" in query.upper()

    def test_vista_incluye_metricas_agregadas(self):
        """Debe incluir métricas agregadas por día"""
        query = generar_vista_metricas_diarias("db", "tabla")

        assert "SELECT" in query
        assert "GROUP BY" in query
        # Debe incluir alguna función de agregación
        funciones_agregacion = ["SUM", "AVG", "COUNT", "MAX", "MIN"]
        assert any(func in query.upper() for func in funciones_agregacion)


class TestEjecutarQueryAthenaSimulado:
    """Tests para ejecutar_query_athena_simulado()"""

    def test_ejecutar_query_retorna_estructura_correcta(self):
        """Debe retornar estructura de respuesta simulada"""
        resultado = ejecutar_query_athena_simulado("SELECT * FROM tabla")

        assert "query_execution_id" in resultado
        assert "status" in resultado
        assert isinstance(resultado["query_execution_id"], str)

    def test_ejecutar_query_status_succeeded(self):
        """Debe retornar status SUCCEEDED para queries válidas"""
        resultado = ejecutar_query_athena_simulado("SELECT * FROM tabla")

        assert resultado["status"] == "SUCCEEDED"

    def test_ejecutar_query_con_diferentes_queries(self):
        """Debe funcionar con diferentes tipos de queries"""
        queries = [
            "SELECT * FROM tabla",
            "SELECT COUNT(*) FROM tabla WHERE status_code = 200",
            "CREATE VIEW vista AS SELECT * FROM tabla",
        ]

        for query in queries:
            resultado = ejecutar_query_athena_simulado(query)
            assert resultado["status"] == "SUCCEEDED"


class TestParsearResultadosAthena:
    """Tests para parsear_resultados_athena()"""

    def test_parsear_resultados_formato_athena(self):
        """Debe parsear formato de respuesta de Athena"""
        raw = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "endpoint"},
                            {"VarCharValue": "count"},
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "/api/users"},
                            {"VarCharValue": "100"},
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "/api/posts"},
                            {"VarCharValue": "50"},
                        ]
                    },
                ]
            }
        }

        resultados = parsear_resultados_athena(raw)

        assert len(resultados) == 2  # Sin header
        assert resultados[0]["endpoint"] == "/api/users"
        assert resultados[0]["count"] == "100"

    def test_parsear_resultados_lista_vacia(self):
        """Debe manejar respuesta vacía"""
        raw = {"ResultSet": {"Rows": []}}

        resultados = parsear_resultados_athena(raw)

        assert resultados == []

    def test_parsear_resultados_con_una_fila_header(self):
        """Debe ignorar la primera fila (header)"""
        raw = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "col1"}, {"VarCharValue": "col2"}]},
                ]
            }
        }

        resultados = parsear_resultados_athena(raw)

        # Solo header, sin datos
        assert len(resultados) == 0


# Fixtures
@pytest.fixture
def database_test():
    """Fixture con nombre de database de prueba"""
    return "test_analytics_db"


@pytest.fixture
def tabla_test():
    """Fixture con nombre de tabla de prueba"""
    return "test_logs_table"
