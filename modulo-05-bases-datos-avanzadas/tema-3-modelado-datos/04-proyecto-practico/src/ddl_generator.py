"""
Módulo para generar DDL (Data Definition Language) de esquemas dimensionales.

Funciones para crear scripts SQL CREATE TABLE para Star Schemas.
"""

from typing import Any


def generar_create_dim_table(table_name: str, table_def: dict[str, Any]) -> str:
    """
    Genera statement CREATE TABLE para una tabla de dimensión.

    Args:
        table_name: Nombre de la tabla
        table_def: Definición de la tabla con columnas

    Returns:
        String con el statement SQL CREATE TABLE

    Raises:
        ValueError: Si la tabla no tiene columnas

    Examples:
        >>> dim_def = {"columnas": {"id": "INTEGER PRIMARY KEY"}}
        >>> ddl = generar_create_dim_table("dim_fecha", dim_def)
        >>> "CREATE TABLE dim_fecha" in ddl
        True
    """
    columnas = table_def.get("columnas", {})

    if not columnas:
        raise ValueError(f"Tabla '{table_name}' debe tener al menos una columna")

    # Construir statement CREATE TABLE
    ddl_parts = [f"CREATE TABLE {table_name} ("]

    # Agregar columnas
    col_definitions = []
    for col_name, col_type in columnas.items():
        col_definitions.append(f"    {col_name} {col_type}")

    ddl_parts.append(",\n".join(col_definitions))
    ddl_parts.append(");")

    return "\n".join(ddl_parts)


def generar_create_fact_table(table_name: str, table_def: dict[str, Any]) -> str:
    """
    Genera statement CREATE TABLE para una tabla de hechos.

    Args:
        table_name: Nombre de la tabla
        table_def: Definición de la tabla con columnas

    Returns:
        String con el statement SQL CREATE TABLE

    Raises:
        ValueError: Si la tabla no tiene FKs

    Examples:
        >>> fact_def = {"columnas": {"id": "INTEGER PRIMARY KEY", "fecha_id": "INTEGER REFERENCES dim_fecha"}}
        >>> ddl = generar_create_fact_table("fact_ventas", fact_def)
        >>> "CREATE TABLE fact_ventas" in ddl
        True
    """
    columnas = table_def.get("columnas", {})

    # Verificar que tenga al menos una FK
    tiene_fk = any(
        "REFERENCES" in str(col_def).upper() for col_def in columnas.values()
    )

    if not tiene_fk:
        raise ValueError(
            f"Tabla de hechos '{table_name}' debe tener al menos una FK a dimensiones"
        )

    # Usar misma lógica que dim table
    return generar_create_dim_table(table_name, table_def)


def generar_indices(
    table_name: str, table_def: dict[str, Any], es_fact_table: bool
) -> list[str]:
    """
    Genera statements CREATE INDEX para optimizar queries.

    Args:
        table_name: Nombre de la tabla
        table_def: Definición de la tabla
        es_fact_table: True si es tabla de hechos

    Returns:
        Lista de statements CREATE INDEX

    Examples:
        >>> fact_def = {"columnas": {"fecha_id": "INTEGER REFERENCES dim_fecha"}}
        >>> indices = generar_indices("fact_ventas", fact_def, True)
        >>> len(indices) >= 1
        True
    """
    indices = []

    if not es_fact_table:
        # Dimensiones típicamente no necesitan índices adicionales
        # (PK ya tiene índice automático)
        return indices

    # Para fact tables: crear índice en cada FK para JOINs rápidos
    columnas = table_def.get("columnas", {})

    for col_name, col_def in columnas.items():
        if "REFERENCES" in str(col_def).upper():
            # Es una FK, crear índice
            # Extraer última parte del nombre de columna (ej: fecha_id → fecha)
            col_base = col_name.replace("_id", "")

            index_name = f"idx_{table_name}_{col_base}"
            index_statement = f"CREATE INDEX {index_name} ON {table_name}({col_name});"
            indices.append(index_statement)

    return indices


def generar_ddl_completo(schema: dict[str, Any]) -> str:
    """
    Genera DDL completo para un esquema Star Schema.

    Args:
        schema: Diccionario con definición completa del esquema

    Returns:
        String con todo el DDL (CREATE TABLEs + índices)

    Examples:
        >>> schema = {"fact_ventas": {"tipo": "fact", "columnas": {...}}}
        >>> ddl = generar_ddl_completo(schema)
        >>> "CREATE TABLE" in ddl
        True
    """
    ddl_parts = []

    # Separar dimensiones y fact tables
    dim_tables = {}
    fact_tables = {}

    for table_name, table_def in schema.items():
        tipo = table_def.get("tipo", "")

        if tipo == "dimension" or table_name.startswith("dim_"):
            dim_tables[table_name] = table_def
        elif tipo == "fact" or table_name.startswith("fact_"):
            fact_tables[table_name] = table_def

    # 1. Generar dimensiones primero (para respetar FKs)
    if dim_tables:
        ddl_parts.append("-- Dimensiones")
        ddl_parts.append("")

        for dim_name, dim_def in dim_tables.items():
            ddl = generar_create_dim_table(dim_name, dim_def)
            ddl_parts.append(ddl)
            ddl_parts.append("")

    # 2. Generar fact tables
    if fact_tables:
        ddl_parts.append("-- Tabla de Hechos")
        ddl_parts.append("")

        for fact_name, fact_def in fact_tables.items():
            ddl = generar_create_fact_table(fact_name, fact_def)
            ddl_parts.append(ddl)
            ddl_parts.append("")

    # 3. Generar índices
    ddl_parts.append("-- Índices para optimización de queries")
    ddl_parts.append("")

    for fact_name, fact_def in fact_tables.items():
        indices = generar_indices(fact_name, fact_def, es_fact_table=True)
        for index_statement in indices:
            ddl_parts.append(index_statement)

    if fact_tables:
        ddl_parts.append("")

    return "\n".join(ddl_parts)
