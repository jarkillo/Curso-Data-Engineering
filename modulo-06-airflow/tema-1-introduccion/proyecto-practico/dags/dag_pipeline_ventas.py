"""
DAG Principal: Pipeline de Monitoreo de Ventas E-Commerce

Este DAG orquesta el pipeline completo de ETL para ventas:
1. Extraer datos de CSV
2. Validar integridad de datos
3. Transformar y calcular métricas
4. Detectar anomalías en ventas
5. Generar reportes (CSV y TXT en paralelo)
6. Enviar notificación simulada

Autor: @development [tdd]
Fecha: 2025-10-25
Módulo: 6 - Apache Airflow y Orquestación
Tema: 1 - Introducción a Airflow - Proyecto Práctico
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from airflow import DAG

# Añadir src al path para imports
proyecto_dir = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_dir))

from src.carga import guardar_reporte_csv, guardar_reporte_txt
from src.deteccion_anomalias import calcular_promedio_historico, detectar_caida_ventas
from src.extraccion import extraer_ventas_csv, obtener_ruta_archivo
from src.notificaciones import simular_envio_email
from src.transformacion import calcular_metricas_ventas
from src.validacion import validar_datos_ventas

# Configuración
FECHA_PROCESO = "{{ ds }}"  # Templating de Airflow (fecha de ejecución)
UMBRAL_ANOMALIA = 0.3  # 30% de caída
DIAS_HISTORICOS = 7  # Últimos 7 días para calcular promedio


def task_extraer_datos(**context):
    """
    Tarea 1: Extrae datos de ventas del CSV
    """
    # En producción, usar fecha de ejecución
    # Por ahora usar fecha fija para desarrollo
    fecha = "2025-10-25"

    ruta = obtener_ruta_archivo(fecha)
    df = extraer_ventas_csv(ruta)

    # Guardar en XCom para siguiente tarea
    context["ti"].xcom_push(key="df_shape", value=df.shape)
    context["ti"].xcom_push(key="fecha", value=fecha)

    # Guardar DataFrame temporalmente
    df.to_csv("/tmp/ventas_temp.csv", index=False)

    return f"Extraídos {len(df)} registros"


def task_validar_datos(**context):
    """
    Tarea 2: Valida integridad de los datos
    """
    import pandas as pd

    df = pd.read_csv("/tmp/ventas_temp.csv")

    resultado = validar_datos_ventas(df)

    if not resultado["valido"]:
        errores = resultado["errores"]
        raise ValueError(
            f"Validación fallida: {len(errores)} errores encontrados. "
            f"Detalles: {errores}"
        )

    return "Validación exitosa"


def task_calcular_metricas(**context):
    """
    Tarea 3: Calcula métricas de ventas
    """
    import pandas as pd

    df = pd.read_csv("/tmp/ventas_temp.csv")
    fecha = context["ti"].xcom_pull(key="fecha", task_ids="extraer_datos")

    metricas = calcular_metricas_ventas(df)
    metricas["fecha"] = fecha

    # Guardar métricas en XCom
    context["ti"].xcom_push(key="metricas", value=metricas)

    return f"Métricas calculadas: ${metricas['total_ventas']:,.2f}"


def task_detectar_anomalias(**context):
    """
    Tarea 4: Detecta anomalías en ventas
    """
    metricas = context["ti"].xcom_pull(key="metricas", task_ids="calcular_metricas")

    total_actual = metricas["total_ventas"]

    # Calcular promedio histórico (últimos 7 días)
    # En producción, esto usaría fechas reales
    # Por ahora simular con valor fijo
    total_historico = 1000.0  # Simulado

    anomalia = detectar_caida_ventas(total_actual, total_historico, UMBRAL_ANOMALIA)

    # Guardar en XCom
    context["ti"].xcom_push(key="anomalia", value=anomalia)

    return anomalia["mensaje"]


def task_generar_reporte_csv(**context):
    """
    Tarea 4a: Genera reporte en formato CSV
    """
    metricas = context["ti"].xcom_pull(key="metricas", task_ids="calcular_metricas")
    fecha = metricas.get("fecha", "2025-10-25")

    ruta = guardar_reporte_csv(metricas, fecha)

    return f"Reporte CSV guardado: {ruta}"


def task_generar_reporte_txt(**context):
    """
    Tarea 4b: Genera reporte en formato TXT
    """
    metricas = context["ti"].xcom_pull(key="metricas", task_ids="calcular_metricas")
    fecha = metricas.get("fecha", "2025-10-25")

    ruta = guardar_reporte_txt(metricas, fecha)

    return f"Reporte TXT guardado: {ruta}"


def task_notificar(**context):
    """
    Tarea 5: Envía notificación con resumen
    """
    metricas = context["ti"].xcom_pull(key="metricas", task_ids="calcular_metricas")
    anomalia = context["ti"].xcom_pull(key="anomalia", task_ids="detectar_anomalias")

    email = simular_envio_email(metricas, anomalia)

    return f"Notificación enviada: {email['asunto']}"


# Definición del DAG
default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "email": ["data-engineering@cloudmart.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="pipeline_ventas_cloudmart",
    description="Pipeline ETL completo para monitoreo de ventas diarias con detección de anomalías",
    default_args=default_args,
    start_date=datetime(2025, 10, 1),
    schedule="0 7 * * *",  # Diario a las 7 AM
    catchup=False,
    tags=["proyecto-practico", "etl", "ventas", "cloudmart"],
) as dag:

    # Inicio
    inicio = DummyOperator(
        task_id="inicio",
    )

    # Tarea 1: Extracción
    extraer = PythonOperator(
        task_id="extraer_datos",
        python_callable=task_extraer_datos,
        provide_context=True,
    )

    # Tarea 2: Validación
    validar = PythonOperator(
        task_id="validar_datos",
        python_callable=task_validar_datos,
        provide_context=True,
    )

    # Tarea 3: Transformación
    calcular = PythonOperator(
        task_id="calcular_metricas",
        python_callable=task_calcular_metricas,
        provide_context=True,
    )

    # Tarea 4: Detección de anomalías
    detectar = PythonOperator(
        task_id="detectar_anomalias",
        python_callable=task_detectar_anomalias,
        provide_context=True,
    )

    # Tareas 4a y 4b: Generar reportes en paralelo
    reporte_csv = PythonOperator(
        task_id="generar_reporte_csv",
        python_callable=task_generar_reporte_csv,
        provide_context=True,
    )

    reporte_txt = PythonOperator(
        task_id="generar_reporte_txt",
        python_callable=task_generar_reporte_txt,
        provide_context=True,
    )

    # Tarea 5: Notificación
    notificar = PythonOperator(
        task_id="notificar",
        python_callable=task_notificar,
        provide_context=True,
    )

    # Tarea de limpieza (Bash)
    limpiar = BashOperator(
        task_id="limpiar_archivos_temporales",
        bash_command="""
        echo "🧹 Limpiando archivos temporales..."
        rm -f /tmp/ventas_temp.csv
        echo "✅ Limpieza completada"
        """,
    )

    # Fin
    fin = DummyOperator(
        task_id="fin",
    )

    # Definir dependencias (flujo del pipeline)
    inicio >> extraer >> validar >> calcular

    # Fan-out: De calcular a detectar y reportes en paralelo
    calcular >> detectar
    calcular >> [reporte_csv, reporte_txt]

    # Fan-in: Todos convergen a notificar
    [detectar, reporte_csv, reporte_txt] >> notificar

    # Notificar → limpiar → fin
    notificar >> limpiar >> fin
