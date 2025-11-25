"""
Módulo para recomendar índices basándose en análisis de consultas SQL.
"""

from typing import Any

from src.query_parser import (
    extraer_columnas_where,
    extraer_joins,
    extraer_tablas,
)


def recomendar_indices(query: str) -> list[dict[str, Any]]:
    """
    Recomienda índices para optimizar una consulta SQL.

    Analiza la consulta y sugiere índices en:
    - Columnas utilizadas en WHERE
    - Columnas utilizadas en JOIN
    - Combinaciones de columnas (índices compuestos)

    Args:
        query: Consulta SQL a analizar

    Returns:
        Lista de recomendaciones de índices ordenadas por prioridad

    Examples:
        >>> recomendar_indices("SELECT * FROM usuarios WHERE email = 'test@example.com'")
        [{'tabla': 'usuarios', 'columna': 'email', 'prioridad': 90, 'razon': '...'}]
    """
    try:
        tablas = extraer_tablas(query)
        columnas_where = extraer_columnas_where(query)
        joins = extraer_joins(query)
    except ValueError:
        # Query inválido, no hay recomendaciones
        return []

    if not tablas:
        return []

    tabla_principal = tablas[0]
    recomendaciones = []

    # Recomendación 1: Índices simples para columnas en WHERE
    for columna in columnas_where:
        prioridad = calcular_prioridad_indice(
            columna=columna,
            en_where=True,
            en_join=False,
            en_order_by=False,  # TODO: detectar ORDER BY
        )

        recomendaciones.append(
            {
                "tabla": tabla_principal,
                "columna": columna,
                "tipo": "simple",
                "prioridad": prioridad,
                "razon": f"Columna '{columna}' usada en WHERE",
            }
        )

    # Recomendación 2: Índices en columnas de JOIN
    for join in joins:
        for columna in join["columnas_join"]:
            prioridad = calcular_prioridad_indice(
                columna=columna, en_where=False, en_join=True, en_order_by=False
            )

            recomendaciones.append(
                {
                    "tabla": join["tabla"],
                    "columna": columna,
                    "tipo": "simple",
                    "prioridad": prioridad,
                    "razon": f"Columna '{columna}' usada en {join['tipo']}",
                }
            )

    # Recomendación 3: Índice compuesto si hay múltiples columnas en WHERE
    if len(columnas_where) >= 2:
        columnas_compuesto = ", ".join(columnas_where[:3])  # Máximo 3 columnas
        prioridad = calcular_prioridad_indice(
            columna=columnas_compuesto, en_where=True, en_join=False, en_order_by=False
        )

        recomendaciones.append(
            {
                "tabla": tabla_principal,
                "columna": columnas_compuesto,
                "tipo": "compuesto",
                "prioridad": prioridad + 5,  # Bonus por ser compuesto
                "razon": "Índice compuesto para múltiples filtros en WHERE",
            }
        )

    # Ordenar por prioridad (mayor primero)
    recomendaciones.sort(key=lambda x: x["prioridad"], reverse=True)

    return recomendaciones


def generar_sql_create_index(tabla: str, columna: str) -> str:
    """
    Genera el SQL para crear un índice.

    Args:
        tabla: Nombre de la tabla
        columna: Nombre de la columna o columnas (separadas por coma para compuestos)

    Returns:
        String con el comando CREATE INDEX

    Examples:
        >>> generar_sql_create_index("usuarios", "email")
        'CREATE INDEX idx_usuarios_email ON usuarios(email);'
        >>> generar_sql_create_index("ventas", "fecha, tienda_id")
        'CREATE INDEX idx_ventas_fecha_tienda_id ON ventas(fecha, tienda_id);'
    """
    # Generar nombre del índice
    columnas_limpias = columna.replace(" ", "").replace(",", "_")
    nombre_indice = f"idx_{tabla}_{columnas_limpias}"

    # Generar SQL
    sql = f"CREATE INDEX {nombre_indice} ON {tabla}({columna});"

    return sql


def calcular_prioridad_indice(
    columna: str, en_where: bool, en_join: bool, en_order_by: bool
) -> int:
    """
    Calcula la prioridad de crear un índice en una columna.

    La prioridad se basa en:
    - WHERE: +80 puntos (alta prioridad)
    - JOIN: +70 puntos (alta prioridad)
    - ORDER BY: +50 puntos (media prioridad)
    - Múltiples usos: acumulativo

    Args:
        columna: Nombre de la columna
        en_where: Si la columna aparece en WHERE
        en_join: Si la columna aparece en JOIN
        en_order_by: Si la columna aparece en ORDER BY

    Returns:
        Prioridad como entero (0-100+)

    Examples:
        >>> calcular_prioridad_indice("email", en_where=True, en_join=False, en_order_by=False)
        80
        >>> calcular_prioridad_indice("id", en_where=True, en_join=True, en_order_by=False)
        150
    """
    prioridad = 0

    if en_where:
        prioridad += 80

    if en_join:
        prioridad += 70

    if en_order_by:
        prioridad += 50

    # Bonus por nombre de columna (heurística)
    if "id" in columna.lower():
        prioridad += 10  # IDs suelen ser altamente selectivos

    if "_id" in columna.lower():
        prioridad += 5  # Foreign keys

    return prioridad
