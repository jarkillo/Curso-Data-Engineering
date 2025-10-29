"""
DAG Pipeline Intermedio - Proyecto Práctico Tema 2.

Pipeline multi-fuente que demuestra conceptos intermedios de Airflow:
- Sensors: Esperar por archivos de entrada
- TaskGroups: Organizar tasks visualmente
- XComs: Compartir datos entre tasks
- Branching: Flujos condicionales
- Templating: Variables dinámicas con Jinja2
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup

from airflow import DAG

# Agregar src/ al path para importar nuestros módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar nuestros módulos  # noqa: E402
from src.branching import decidir_ruta_procesamiento  # noqa: E402
from src.extraccion import (  # noqa: E402
    contar_registros_extraidos,
    extraer_clientes_json,
    extraer_ventas_csv,
)
from src.notificaciones import (  # noqa: E402
    guardar_log_ejecucion,
    simular_notificacion_gerente,
)
from src.reportes import (  # noqa: E402
    exportar_reporte_csv,
    exportar_reporte_json,
    generar_reporte_detallado,
    generar_reporte_simple,
)
from src.transformacion import (  # noqa: E402
    calcular_metricas_por_cliente,
    calcular_total_ventas,
    enriquecer_ventas_con_clientes,
)
from src.validacion import (  # noqa: E402
    validar_datos_clientes,
    validar_datos_ventas,
    validar_schema_clientes,
    validar_schema_ventas,
)

# Configuración de rutas
BASE_DIR = project_root
DATA_INPUT = BASE_DIR / "data" / "input"
DATA_OUTPUT = BASE_DIR / "data" / "output"

# Argumentos por defecto del DAG
default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Definir el DAG
with DAG(
    dag_id="dag_pipeline_intermedio",
    default_args=default_args,
    description="Pipeline intermedio con Sensors, TaskGroups, XComs y Branching",
    schedule_interval=None,  # Manual trigger
    start_date=datetime(2025, 10, 29),
    catchup=False,
    tags=["intermedio", "tema2", "proyecto"],
) as dag:

    # ===== INICIO =====
    inicio = DummyOperator(task_id="inicio")

    # ===== SENSORS: Esperar por archivos de entrada =====
    with TaskGroup("sensores") as grupo_sensores:
        esperar_ventas = FileSensor(
            task_id="esperar_ventas_csv",
            filepath=str(DATA_INPUT / "ventas.csv"),
            poke_interval=10,
            timeout=60,
            mode="reschedule",
        )

        esperar_clientes = FileSensor(
            task_id="esperar_clientes_json",
            filepath=str(DATA_INPUT / "clientes.json"),
            poke_interval=10,
            timeout=60,
            mode="reschedule",
        )

    # ===== TASKGROUP: VENTAS =====
    with TaskGroup("grupo_ventas") as grupo_ventas:

        def extraer_ventas_wrapper(**context):
            """Wrapper para extraer ventas y guardar count en XCom"""
            ti = context["ti"]
            df = extraer_ventas_csv(str(DATA_INPUT / "ventas.csv"))
            count = contar_registros_extraidos(df)
            ti.xcom_push(key="df_ventas", value=df.to_dict("records"))
            ti.xcom_push(key="num_ventas", value=count)
            return count

        extraer_ventas = PythonOperator(
            task_id="extraer_ventas",
            python_callable=extraer_ventas_wrapper,
        )

        def validar_ventas_wrapper(**context):
            """Wrapper para validar ventas"""
            import pandas as pd

            ti = context["ti"]
            ventas_dict = ti.xcom_pull(
                task_ids="grupo_ventas.extraer_ventas", key="df_ventas"
            )
            df = pd.DataFrame(ventas_dict)
            validar_schema_ventas(df)
            validar_datos_ventas(df)

        validar_ventas = PythonOperator(
            task_id="validar_ventas",
            python_callable=validar_ventas_wrapper,
        )

        extraer_ventas >> validar_ventas

    # ===== TASKGROUP: CLIENTES =====
    with TaskGroup("grupo_clientes") as grupo_clientes:

        def extraer_clientes_wrapper(**context):
            """Wrapper para extraer clientes y guardar count en XCom"""
            ti = context["ti"]
            df = extraer_clientes_json(str(DATA_INPUT / "clientes.json"))
            count = contar_registros_extraidos(df)
            ti.xcom_push(key="df_clientes", value=df.to_dict("records"))
            ti.xcom_push(key="num_clientes", value=count)
            return count

        extraer_clientes = PythonOperator(
            task_id="extraer_clientes",
            python_callable=extraer_clientes_wrapper,
        )

        def validar_clientes_wrapper(**context):
            """Wrapper para validar clientes"""
            import pandas as pd

            ti = context["ti"]
            clientes_dict = ti.xcom_pull(
                task_ids="grupo_clientes.extraer_clientes", key="df_clientes"
            )
            df = pd.DataFrame(clientes_dict)
            validar_schema_clientes(df)
            validar_datos_clientes(df)

        validar_clientes = PythonOperator(
            task_id="validar_clientes",
            python_callable=validar_clientes_wrapper,
        )

        extraer_clientes >> validar_clientes

    # ===== TRANSFORMACIÓN =====
    def combinar_datos_wrapper(**context):
        """Combina ventas y clientes"""
        import pandas as pd

        ti = context["ti"]
        ventas_dict = ti.xcom_pull(
            task_ids="grupo_ventas.extraer_ventas", key="df_ventas"
        )
        clientes_dict = ti.xcom_pull(
            task_ids="grupo_clientes.extraer_clientes", key="df_clientes"
        )

        df_ventas = pd.DataFrame(ventas_dict)
        df_clientes = pd.DataFrame(clientes_dict)

        df_enriquecido = enriquecer_ventas_con_clientes(df_ventas, df_clientes)

        ti.xcom_push(key="df_enriquecido", value=df_enriquecido.to_dict("records"))
        print(f"[COMBINAR] Datos enriquecidos: {len(df_enriquecido)} registros")

    combinar_datos = PythonOperator(
        task_id="combinar_datos",
        python_callable=combinar_datos_wrapper,
    )

    def calcular_metricas_wrapper(**context):
        """Calcula métricas globales y por cliente"""
        import pandas as pd

        ti = context["ti"]
        enriquecido_dict = ti.xcom_pull(task_ids="combinar_datos", key="df_enriquecido")
        df = pd.DataFrame(enriquecido_dict)

        # Calcular total de ventas
        total = calcular_total_ventas(df)

        # Calcular métricas por cliente
        df_metricas = calcular_metricas_por_cliente(df)

        # Obtener cliente top
        cliente_top = df_metricas.sort_values("total_ventas", ascending=False).iloc[0]
        cliente_top_id = cliente_top["cliente_id"]

        # Guardar en XCom
        ti.xcom_push(key="total_ventas", value=total)
        ti.xcom_push(key="cliente_top", value=cliente_top_id)
        ti.xcom_push(key="df_metricas", value=df_metricas.to_dict("records"))

        print(f"[METRICAS] Total: {total:.2f}€, Cliente top: {cliente_top_id}")

    calcular_metricas = PythonOperator(
        task_id="calcular_metricas",
        python_callable=calcular_metricas_wrapper,
    )

    # ===== BRANCHING =====
    branch = BranchPythonOperator(
        task_id="decidir_ruta",
        python_callable=decidir_ruta_procesamiento,
    )

    # ===== RUTA PREMIUM =====
    def generar_reporte_detallado_wrapper(**context):
        """Genera reporte detallado para ruta premium"""
        import pandas as pd

        ti = context["ti"]
        metricas_dict = ti.xcom_pull(task_ids="calcular_metricas", key="df_metricas")
        total = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")

        df = pd.DataFrame(metricas_dict)
        reporte = generar_reporte_detallado(df, total)

        ti.xcom_push(key="reporte", value=reporte)
        print(f"[REPORTE_DETALLADO] Generado: {reporte['tipo']}")

    generar_detallado = PythonOperator(
        task_id="generar_reporte_detallado",
        python_callable=generar_reporte_detallado_wrapper,
    )

    def notificar_gerente_wrapper(**context):
        """Simula notificación al gerente"""
        ti = context["ti"]
        total = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")
        cliente_top = ti.xcom_pull(task_ids="calcular_metricas", key="cliente_top")

        simular_notificacion_gerente(total, cliente_top)

    notificar_gerente = PythonOperator(
        task_id="notificar_gerente",
        python_callable=notificar_gerente_wrapper,
    )

    # ===== RUTA NORMAL =====
    def generar_reporte_simple_wrapper(**context):
        """Genera reporte simple para ruta normal"""
        import pandas as pd

        ti = context["ti"]
        metricas_dict = ti.xcom_pull(task_ids="calcular_metricas", key="df_metricas")
        total = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")

        df = pd.DataFrame(metricas_dict)
        reporte = generar_reporte_simple(df, total)

        ti.xcom_push(key="reporte", value=reporte)
        print(f"[REPORTE_SIMPLE] Generado: {reporte['tipo']}")

    generar_simple = PythonOperator(
        task_id="generar_reporte_simple",
        python_callable=generar_reporte_simple_wrapper,
    )

    def guardar_log_wrapper(**context):
        """Guarda log de ejecución"""
        ti = context["ti"]
        total = ti.xcom_pull(task_ids="calcular_metricas", key="total_ventas")

        # Usar templating para el nombre del archivo
        fecha = context["ds_nodash"]
        log_path = DATA_OUTPUT / "logs" / f"ejecucion_{fecha}.log"

        mensaje = f"Ejecución completada. Total: {total:.2f}€"
        guardar_log_ejecucion(mensaje, str(log_path))

    guardar_log = PythonOperator(
        task_id="guardar_log",
        python_callable=guardar_log_wrapper,
    )

    # ===== CONVERGENCIA POST-BRANCH =====
    convergencia = DummyOperator(
        task_id="convergencia",
        trigger_rule="none_failed_min_one_success",
    )

    # ===== TASKGROUP: EXPORTAR =====
    with TaskGroup("grupo_exportar") as grupo_exportar:

        def exportar_csv_wrapper(**context):
            """Exporta métricas a CSV"""
            import pandas as pd

            ti = context["ti"]
            metricas_dict = ti.xcom_pull(
                task_ids="calcular_metricas", key="df_metricas"
            )
            df = pd.DataFrame(metricas_dict)

            # Usar templating para el nombre del archivo
            fecha = context["ds_nodash"]
            csv_path = DATA_OUTPUT / f"metricas_{fecha}.csv"

            exportar_reporte_csv(df, str(csv_path))
            ti.xcom_push(key="ruta_csv", value=str(csv_path))

        exportar_csv = PythonOperator(
            task_id="exportar_csv",
            python_callable=exportar_csv_wrapper,
        )

        def exportar_json_wrapper(**context):
            """Exporta reporte a JSON"""
            ti = context["ti"]

            # Leer reporte de cualquiera de las dos rutas
            reporte_detallado = ti.xcom_pull(
                task_ids="generar_reporte_detallado", key="reporte"
            )
            reporte_simple = ti.xcom_pull(
                task_ids="generar_reporte_simple", key="reporte"
            )

            reporte = reporte_detallado if reporte_detallado else reporte_simple

            # Usar templating para el nombre del archivo
            fecha = context["ds_nodash"]
            json_path = DATA_OUTPUT / f"reporte_{fecha}.json"

            exportar_reporte_json(reporte, str(json_path))
            ti.xcom_push(key="ruta_json", value=str(json_path))

        exportar_json = PythonOperator(
            task_id="exportar_json",
            python_callable=exportar_json_wrapper,
        )

        exportar_csv >> exportar_json

    # ===== FIN =====
    fin = DummyOperator(task_id="fin")

    # ===== DEPENDENCIAS =====
    inicio >> grupo_sensores >> [grupo_ventas, grupo_clientes]
    [grupo_ventas, grupo_clientes] >> combinar_datos
    combinar_datos >> calcular_metricas >> branch

    # Ruta premium
    branch >> [generar_detallado, notificar_gerente] >> convergencia

    # Ruta normal
    branch >> [generar_simple, guardar_log] >> convergencia

    # Exportación y fin
    convergencia >> grupo_exportar >> fin
