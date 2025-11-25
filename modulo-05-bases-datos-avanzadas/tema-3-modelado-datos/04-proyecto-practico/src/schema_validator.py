"""
Módulo para validar esquemas dimensionales (Star Schema).

Funciones para verificar que un esquema cumpla con las características
de un Data Warehouse dimensional válido.
"""

from typing import Any


def identificar_fact_table(schema: dict[str, Any]) -> str:
    """
    Identifica la tabla de hechos en un esquema.

    Args:
        schema: Diccionario con definición de tablas

    Returns:
        Nombre de la tabla de hechos

    Raises:
        ValueError: Si no hay tabla de hechos o hay múltiples

    Examples:
        >>> schema = {"fact_ventas": {"tipo": "fact", "columnas": {}}}
        >>> identificar_fact_table(schema)
        'fact_ventas'
    """
    fact_tables = []

    for table_name, table_def in schema.items():
        # Identificar por tipo explícito
        if table_def.get("tipo") == "fact" or table_name.startswith("fact_"):
            fact_tables.append(table_name)

    if len(fact_tables) == 0:
        raise ValueError("No se encontró tabla de hechos en el esquema")

    if len(fact_tables) > 1:
        raise ValueError(
            f"Se encontraron múltiples tablas de hechos: {', '.join(fact_tables)}"
        )

    return fact_tables[0]


def identificar_dimension_tables(schema: dict[str, Any]) -> list[str]:
    """
    Identifica las tablas de dimensión en un esquema.

    Args:
        schema: Diccionario con definición de tablas

    Returns:
        Lista de nombres de tablas de dimensión

    Examples:
        >>> schema = {"dim_fecha": {"tipo": "dimension", "columnas": {}}}
        >>> identificar_dimension_tables(schema)
        ['dim_fecha']
    """
    dimension_tables = []

    for table_name, table_def in schema.items():
        # Identificar por tipo explícito
        if (
            table_def.get("tipo") == "dimension"
            or table_name.startswith("dim_")
            and table_def.get("tipo") != "fact"
        ):
            dimension_tables.append(table_name)

    return dimension_tables


def validar_foreign_keys(
    fact_table: dict[str, Any], dimension_tables: list[str]
) -> None:
    """
    Valida que las FKs de la fact table referencien dimensiones existentes.

    Args:
        fact_table: Definición de la tabla de hechos
        dimension_tables: Lista de nombres de tablas de dimensión

    Raises:
        ValueError: Si hay FKs inválidas o no hay suficientes FKs

    Examples:
        >>> fact = {"columnas": {"fecha_id": "INTEGER REFERENCES dim_fecha"}}
        >>> dims = ["dim_fecha"]
        >>> validar_foreign_keys(fact, dims)
        # No lanza error
    """
    columnas = fact_table.get("columnas", {})

    # Extraer columnas con REFERENCES
    foreign_keys = {}

    for col_name, col_def in columnas.items():
        if "REFERENCES" in col_def.upper():
            # Extraer nombre de tabla referenciada
            parts = col_def.upper().split("REFERENCES")
            if len(parts) > 1:
                referenced_table = parts[1].strip().split()[0].lower()
                foreign_keys[col_name] = referenced_table

    # Validar que haya al menos una FK (fact table debe conectarse a dimensiones)
    if len(foreign_keys) == 0:
        raise ValueError(
            "Tabla de hechos debe tener al menos una clave foránea a dimensiones"
        )

    # Validar que todas las FKs referencien dimensiones existentes
    for fk_col, referenced_table in foreign_keys.items():
        if referenced_table not in dimension_tables:
            raise ValueError(
                f"Clave foránea '{fk_col}' referencia tabla '{referenced_table}' "
                f"que no es una dimensión del esquema"
            )


def validar_star_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Valida que un esquema cumpla con las características de un Star Schema.

    Args:
        schema: Diccionario con definición completa del esquema

    Returns:
        Diccionario con resultado de validación:
        {
            "valido": bool,
            "fact_table": str,
            "dimension_tables": list[str],
            "errores": list[str]
        }

    Examples:
        >>> schema = {
        ...     "fact_ventas": {"tipo": "fact", "columnas": {...}},
        ...     "dim_fecha": {"tipo": "dimension", "columnas": {...}}
        ... }
        >>> resultado = validar_star_schema(schema)
        >>> resultado["valido"]
        True
    """
    errores = []
    fact_table_name = None
    dimension_tables = []

    # 1. Identificar fact table
    try:
        fact_table_name = identificar_fact_table(schema)
    except ValueError as e:
        errores.append(str(e))

    # 2. Identificar dimension tables
    try:
        dimension_tables = identificar_dimension_tables(schema)
    except ValueError as e:
        errores.append(str(e))

    # 3. Validar mínimo de dimensiones (Star Schema típico tiene >= 2)
    if len(dimension_tables) < 2:
        errores.append(
            f"Star Schema debe tener al menos 2 dimensiones, encontradas: {len(dimension_tables)}"
        )

    # 4. Validar FKs si tenemos fact table y dimensiones
    if fact_table_name and len(dimension_tables) > 0:
        try:
            fact_table_def = schema[fact_table_name]
            validar_foreign_keys(fact_table_def, dimension_tables)
        except ValueError as e:
            errores.append(str(e))

    # Determinar si es válido
    valido = len(errores) == 0

    return {
        "valido": valido,
        "fact_table": fact_table_name,
        "dimension_tables": dimension_tables,
        "errores": errores,
    }
