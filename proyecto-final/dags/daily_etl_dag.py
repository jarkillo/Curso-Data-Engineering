"""
DAG de Airflow para el pipeline ETL diario de TechMart Analytics.

Este DAG ejecuta el pipeline ETL completo:
1. Extracción de datos de múltiples fuentes
2. Transformación y limpieza
3. Carga al data warehouse
4. Validación de calidad de datos

Schedule: Diario a las 2:00 AM UTC
"""

from datetime import datetime, timedelta
from pathlib import Path

# Nota: Este archivo está diseñado para ejecutarse con Apache Airflow.
# Para desarrollo local sin Airflow, usar el módulo src directamente.

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.empty import EmptyOperator
    from airflow.utils.task_group import TaskGroup

    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False

# Configuración del DAG
DEFAULT_ARGS = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "email": ["alerts@techmart.local"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Configuración de rutas y conexiones
CONFIG = {
    "api_url": "http://api.techmart.local/orders",
    "csv_path": "/data/raw/products.csv",
    "db_connection": "postgresql://etl_user:password@postgres:5432/techmart",
    "warehouse_path": "/data/warehouse",
}


# ============================================================================
# Funciones de Tareas
# ============================================================================


def extract_orders_task(**context):
    """Extrae pedidos desde la API."""
    from src.extractors.api_extractor import extract_orders_from_api
    from src.utils.logging_config import get_logger, log_step

    logger = get_logger("etl.extract_orders")
    log_step(logger, "extract_orders", "started")

    try:
        # Obtener fecha de ejecución
        execution_date = context["ds"]

        # Extraer pedidos del día anterior
        df = extract_orders_from_api(
            url=CONFIG["api_url"],
            params={"date": execution_date},
        )

        # Guardar en staging
        output_path = Path(CONFIG["warehouse_path"]) / "staging" / "orders.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)

        log_step(logger, "extract_orders", "completed", rows=len(df))
        return str(output_path)

    except Exception as e:
        log_step(logger, "extract_orders", "failed", error=str(e))
        raise


def extract_products_task(**context):
    """Extrae productos desde CSV."""
    from src.extractors.csv_extractor import extract_products_from_csv
    from src.utils.logging_config import get_logger, log_step

    logger = get_logger("etl.extract_products")
    log_step(logger, "extract_products", "started")

    try:
        df = extract_products_from_csv(CONFIG["csv_path"])

        output_path = Path(CONFIG["warehouse_path"]) / "staging" / "products.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)

        log_step(logger, "extract_products", "completed", rows=len(df))
        return str(output_path)

    except Exception as e:
        log_step(logger, "extract_products", "failed", error=str(e))
        raise


def extract_customers_task(**context):
    """Extrae clientes desde base de datos."""
    from src.extractors.db_extractor import extract_customers_from_db
    from src.utils.logging_config import get_logger, log_step

    logger = get_logger("etl.extract_customers")
    log_step(logger, "extract_customers", "started")

    try:
        df = extract_customers_from_db(CONFIG["db_connection"])

        output_path = Path(CONFIG["warehouse_path"]) / "staging" / "customers.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)

        log_step(logger, "extract_customers", "completed", rows=len(df))
        return str(output_path)

    except Exception as e:
        log_step(logger, "extract_customers", "failed", error=str(e))
        raise


def transform_data_task(**context):
    """Transforma y limpia los datos."""
    import pandas as pd

    from src.transformers.cleaning import clean_customers, clean_orders, clean_products
    from src.transformers.enrichment import (
        calculate_order_metrics,
        enrich_orders_with_customers,
        enrich_orders_with_products,
    )
    from src.utils.logging_config import get_logger, log_step

    logger = get_logger("etl.transform")
    log_step(logger, "transform", "started")

    try:
        staging_path = Path(CONFIG["warehouse_path"]) / "staging"

        # Leer datos de staging
        orders_df = pd.read_parquet(staging_path / "orders.parquet")
        products_df = pd.read_parquet(staging_path / "products.parquet")
        customers_df = pd.read_parquet(staging_path / "customers.parquet")

        # Limpiar datos
        clean_orders_df = clean_orders(orders_df)
        clean_products_df = clean_products(products_df)
        clean_customers_df = clean_customers(customers_df)

        # Enriquecer pedidos
        enriched_df = enrich_orders_with_products(clean_orders_df, clean_products_df)
        enriched_df = enrich_orders_with_customers(enriched_df, clean_customers_df)
        enriched_df = calculate_order_metrics(enriched_df)

        # Guardar datos transformados
        transformed_path = Path(CONFIG["warehouse_path"]) / "transformed"
        transformed_path.mkdir(parents=True, exist_ok=True)

        enriched_df.to_parquet(transformed_path / "fact_sales.parquet", index=False)
        clean_products_df.to_parquet(
            transformed_path / "dim_product.parquet", index=False
        )
        clean_customers_df.to_parquet(
            transformed_path / "dim_customer.parquet", index=False
        )

        log_step(
            logger,
            "transform",
            "completed",
            orders=len(clean_orders_df),
            products=len(clean_products_df),
            customers=len(clean_customers_df),
        )

    except Exception as e:
        log_step(logger, "transform", "failed", error=str(e))
        raise


def load_warehouse_task(**context):
    """Carga datos al data warehouse."""
    import pandas as pd

    from src.loaders.warehouse_loader import (
        create_dim_date,
        load_dimension,
        load_fact_table,
    )
    from src.utils.logging_config import get_logger, log_step

    logger = get_logger("etl.load")
    log_step(logger, "load", "started")

    try:
        transformed_path = Path(CONFIG["warehouse_path"]) / "transformed"
        warehouse_path = Path(CONFIG["warehouse_path"]) / "warehouse"
        warehouse_path.mkdir(parents=True, exist_ok=True)

        # Leer datos transformados
        fact_sales = pd.read_parquet(transformed_path / "fact_sales.parquet")
        dim_product = pd.read_parquet(transformed_path / "dim_product.parquet")
        dim_customer = pd.read_parquet(transformed_path / "dim_customer.parquet")

        # Crear dimensión de fecha
        execution_date = context["ds"]
        dim_date = create_dim_date(
            start_date="2024-01-01",
            end_date=execution_date,
        )

        # Cargar dimensiones
        load_dimension(
            dim_product,
            output_path=str(warehouse_path / "dim_product.parquet"),
            key_column="product_id",
            dimension_name="dim_product",
        )

        load_dimension(
            dim_customer,
            output_path=str(warehouse_path / "dim_customer.parquet"),
            key_column="customer_id",
            dimension_name="dim_customer",
        )

        load_dimension(
            dim_date,
            output_path=str(warehouse_path / "dim_date.parquet"),
            key_column="date_id",
            dimension_name="dim_date",
        )

        # Cargar tabla de hechos
        result = load_fact_table(
            fact_sales,
            output_path=str(warehouse_path / "fact_sales.parquet"),
            foreign_keys=["product_id", "customer_id"],
            measures=["quantity", "order_total"],
            fact_name="fact_sales",
        )

        log_step(
            logger,
            "load",
            "completed",
            rows_loaded=result["rows_loaded"],
        )

    except Exception as e:
        log_step(logger, "load", "failed", error=str(e))
        raise


def validate_data_task(**context):
    """Valida la calidad de los datos cargados."""
    import pandas as pd

    from src.utils.logging_config import get_logger, log_step
    from src.utils.validators import run_all_validations

    logger = get_logger("etl.validate")
    log_step(logger, "validate", "started")

    try:
        warehouse_path = Path(CONFIG["warehouse_path"]) / "warehouse"

        # Leer datos del warehouse
        fact_sales = pd.read_parquet(warehouse_path / "fact_sales.parquet")
        dim_product = pd.read_parquet(warehouse_path / "dim_product.parquet")

        # Definir validaciones
        validations = [
            ("not_empty", {"df": fact_sales}),
            (
                "required_columns",
                {
                    "df": fact_sales,
                    "columns": ["order_id", "product_id", "customer_id"],
                },
            ),
            ("no_nulls", {"df": fact_sales, "columns": ["order_id"]}),
            ("numeric_range", {"df": fact_sales, "column": "quantity", "min_val": 0}),
            ("unique", {"df": dim_product, "column": "product_id"}),
        ]

        # Ejecutar validaciones
        result = run_all_validations(validations)

        if not result["all_passed"]:
            failed = [
                name
                for name, detail in result["details"].items()
                if not detail["valid"]
            ]
            raise ValueError(f"Data validation failed: {failed}")

        log_step(
            logger,
            "validate",
            "completed",
            validations_passed=result["passed_count"],
        )

    except Exception as e:
        log_step(logger, "validate", "failed", error=str(e))
        raise


# ============================================================================
# Definición del DAG
# ============================================================================

if AIRFLOW_AVAILABLE:
    with DAG(
        dag_id="daily_etl_techmart",
        default_args=DEFAULT_ARGS,
        description="Pipeline ETL diario para TechMart Analytics",
        schedule_interval="0 2 * * *",  # Diario a las 2:00 AM UTC
        start_date=datetime(2024, 1, 1),
        catchup=False,
        tags=["etl", "techmart", "data_warehouse"],
    ) as dag:
        start = EmptyOperator(task_id="start")
        end = EmptyOperator(task_id="end")

        # Grupo de extracción (paralelo)
        with TaskGroup(group_id="extract") as extract_group:
            extract_orders = PythonOperator(
                task_id="extract_orders",
                python_callable=extract_orders_task,
            )
            extract_products = PythonOperator(
                task_id="extract_products",
                python_callable=extract_products_task,
            )
            extract_customers = PythonOperator(
                task_id="extract_customers",
                python_callable=extract_customers_task,
            )

        # Transformación
        transform = PythonOperator(
            task_id="transform",
            python_callable=transform_data_task,
        )

        # Carga
        load = PythonOperator(
            task_id="load",
            python_callable=load_warehouse_task,
        )

        # Validación
        validate = PythonOperator(
            task_id="validate",
            python_callable=validate_data_task,
        )

        # Definir dependencias
        start >> extract_group >> transform >> load >> validate >> end
