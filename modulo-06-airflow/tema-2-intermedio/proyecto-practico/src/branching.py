"""
Módulo de branching (decisiones condicionales).

Este módulo proporciona funciones para tomar decisiones sobre qué ruta
seguir en el pipeline basándose en métricas calculadas.
"""


def decidir_ruta_procesamiento(**context) -> list[str]:
    """
    Decide si seguir la ruta premium o normal basándose en el total de ventas.

    Lógica:
    - Si total_ventas > 5000€ → Ruta PREMIUM (reporte detallado + notificar gerente)
    - Si total_ventas ≤ 5000€ → Ruta NORMAL (reporte simple + guardar log)

    Args:
        context: Contexto de Airflow con TaskInstance (ti)

    Returns:
        Lista de task_ids a ejecutar

    Examples:
        En Airflow DAG:
        >>> branch = BranchPythonOperator(
        ...     task_id="decidir_ruta",
        ...     python_callable=decidir_ruta_procesamiento
        ... )
    """
    ti = context["ti"]

    # Leer el total de ventas del XCom
    total_ventas = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")

    umbral = 5000.0

    if total_ventas > umbral:
        print(f"[BRANCH] Total {total_ventas:.2f}€ > {umbral:.2f}€ → RUTA PREMIUM")
        return ["generar_reporte_detallado", "notificar_gerente"]
    else:
        print(f"[BRANCH] Total {total_ventas:.2f}€ ≤ {umbral:.2f}€ → RUTA NORMAL")
        return ["generar_reporte_simple", "guardar_log"]
