"""
Tests para el módulo de branching (decisiones condicionales).

Siguiendo metodología TDD - Red, Green, Refactor
"""


def test_decidir_ruta_procesamiento_ruta_premium():
    """Test: decidir_ruta_procesamiento retorna ruta premium si total > 5000"""
    from src.branching import decidir_ruta_procesamiento

    # Mock del contexto de Airflow
    class MockTaskInstance:
        def xcom_pull(self, task_ids, key):
            return 6500.0  # Total de ventas > 5000

    context = {"ti": MockTaskInstance()}

    resultado = decidir_ruta_procesamiento(**context)

    assert isinstance(resultado, list)
    assert "generar_reporte_detallado" in resultado
    assert "notificar_gerente" in resultado


def test_decidir_ruta_procesamiento_ruta_normal():
    """Test: decidir_ruta_procesamiento retorna ruta normal si total <= 5000"""
    from src.branching import decidir_ruta_procesamiento

    # Mock del contexto de Airflow
    class MockTaskInstance:
        def xcom_pull(self, task_ids, key):
            return 3500.0  # Total de ventas <= 5000

    context = {"ti": MockTaskInstance()}

    resultado = decidir_ruta_procesamiento(**context)

    assert isinstance(resultado, list)
    assert "generar_reporte_simple" in resultado
    assert "guardar_log" in resultado


def test_decidir_ruta_procesamiento_en_el_limite():
    """Test: decidir_ruta_procesamiento con total exactamente en 5000"""
    from src.branching import decidir_ruta_procesamiento

    # Mock del contexto de Airflow
    class MockTaskInstance:
        def xcom_pull(self, task_ids, key):
            return 5000.0  # Exactamente en el umbral

    context = {"ti": MockTaskInstance()}

    resultado = decidir_ruta_procesamiento(**context)

    # 5000 NO es > 5000, así que debe ir por ruta normal
    assert isinstance(resultado, list)
    assert "generar_reporte_simple" in resultado
    assert "guardar_log" in resultado


def test_decidir_ruta_procesamiento_con_total_cero():
    """Test: decidir_ruta_procesamiento con total = 0 va por ruta normal"""
    from src.branching import decidir_ruta_procesamiento

    # Mock del contexto de Airflow
    class MockTaskInstance:
        def xcom_pull(self, task_ids, key):
            return 0.0

    context = {"ti": MockTaskInstance()}

    resultado = decidir_ruta_procesamiento(**context)

    assert isinstance(resultado, list)
    assert "generar_reporte_simple" in resultado
    assert "guardar_log" in resultado
