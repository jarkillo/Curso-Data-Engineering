"""Extractor de datos desde bases de datos."""

import pandas as pd
from sqlalchemy import create_engine


def build_customer_query(
    since_date: str | None = None,
    region: str | None = None,
    limit: int | None = None,
) -> str:
    """
    Construye query SQL para extraer clientes.

    Args:
        since_date: Filtrar clientes creados desde esta fecha (YYYY-MM-DD).
        region: Filtrar por región específica.
        limit: Límite de registros a retornar.

    Returns:
        Query SQL como string.

    Examples:
        >>> query = build_customer_query(region="Madrid", limit=100)
        >>> "WHERE" in query and "LIMIT 100" in query
        True
    """
    query = """
        SELECT
            customer_id,
            name,
            email,
            region,
            created_at
        FROM customers
    """

    conditions = []

    if since_date:
        conditions.append(f"created_at >= '{since_date}'")

    if region:
        conditions.append(f"region = '{region}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if limit:
        query += f" LIMIT {limit}"

    return query


def extract_customers_from_db(
    connection_string: str,
    since_date: str | None = None,
    region: str | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """
    Extrae clientes desde base de datos PostgreSQL.

    Args:
        connection_string: String de conexión SQLAlchemy.
        since_date: Filtrar clientes creados desde esta fecha.
        region: Filtrar por región específica.
        limit: Límite de registros.

    Returns:
        DataFrame con los clientes extraídos.

    Raises:
        ValueError: Si connection_string está vacía.
        ConnectionError: Si hay error de conexión a la base de datos.

    Examples:
        >>> df = extract_customers_from_db("postgresql://user:pass@host/db")
        >>> "customer_id" in df.columns
        True
    """
    if not connection_string:
        raise ValueError("Invalid connection string: cannot be empty")

    query = build_customer_query(since_date=since_date, region=region, limit=limit)

    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        raise ConnectionError(f"Failed to connect to database: {e}")
