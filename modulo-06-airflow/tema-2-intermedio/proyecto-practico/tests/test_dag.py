"""
Tests para el DAG principal.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import sys
from pathlib import Path

import pytest

# Agregar el directorio del DAG al path
dag_dir = Path(__file__).parent.parent / "dags"
sys.path.insert(0, str(dag_dir))

# Skip estos tests si Airflow no está instalado
airflow = pytest.importorskip("airflow", reason="Airflow no está instalado")


def test_dag_parsea_sin_errores():
    """Test: el DAG se puede importar sin errores de sintaxis"""
    from airflow.models import DagBag

    dagbag = DagBag(dag_folder=str(dag_dir), include_examples=False)

    # Verificar que no hay errores de parseo
    assert len(dagbag.import_errors) == 0, f"Errores de parseo: {dagbag.import_errors}"

    # Verificar que el DAG existe
    assert "dag_pipeline_intermedio" in dagbag.dags


def test_dag_tiene_estructura_correcta():
    """Test: el DAG tiene las tasks y grupos esperados"""
    from airflow.models import DagBag

    dagbag = DagBag(dag_folder=str(dag_dir), include_examples=False)
    dag = dagbag.get_dag("dag_pipeline_intermedio")

    assert dag is not None
    assert dag.dag_id == "dag_pipeline_intermedio"

    # Verificar que tiene tasks (al menos algunas principales)
    task_ids = [task.task_id for task in dag.tasks]

    # Debe tener los sensores
    assert any("esperar_ventas" in tid or "sensor" in tid for tid in task_ids)

    # Debe tener tasks de extracción o grupos
    assert any(
        "extraer" in tid or "ventas" in tid or "grupo" in tid for tid in task_ids
    )

    # Debe tener branching
    assert any("decidir" in tid or "branch" in tid for tid in task_ids)

    # Debe tener exportación o fin
    assert any("exportar" in tid or "fin" in tid for tid in task_ids)

    # Verificar que el DAG tiene al menos 10 tasks (número mínimo esperado)
    assert len(dag.tasks) >= 10, (
        f"El DAG tiene {len(dag.tasks)} tasks, se esperaban al menos 10"
    )
