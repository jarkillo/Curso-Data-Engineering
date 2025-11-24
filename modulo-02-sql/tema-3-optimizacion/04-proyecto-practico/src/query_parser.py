"""
Módulo para parsear consultas SQL y extraer información relevante.
"""

import re
from typing import Any

import sqlparse
from sqlparse.sql import Function, Identifier, IdentifierList, Where
from sqlparse.tokens import Keyword, Wildcard


def extraer_tablas(query: str) -> list[str]:
    """
    Extrae nombres de tablas de una consulta SQL.

    Args:
        query: Consulta SQL como string

    Returns:
        Lista de nombres de tablas

    Raises:
        ValueError: Si query está vacío o no tiene FROM

    Examples:
        >>> extraer_tablas("SELECT * FROM usuarios")
        ['usuarios']
        >>> extraer_tablas("SELECT * FROM usuarios u JOIN pedidos p ON u.id = p.usuario_id")
        ['usuarios', 'pedidos']
    """
    if not query or not query.strip():
        raise ValueError("Query no puede estar vacío")

    # Parsear query
    parsed = sqlparse.parse(query)[0]

    # Buscar FROM
    from_seen = False
    tablas = []

    for token in parsed.tokens:
        if from_seen:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    tablas.append(_extraer_nombre_tabla(identifier))
            elif isinstance(token, Identifier):
                tablas.append(_extraer_nombre_tabla(token))
            elif token.ttype is Keyword and token.value.upper() in (
                "WHERE",
                "GROUP",
                "ORDER",
                "LIMIT",
            ):
                break

        if token.ttype is Keyword and token.value.upper() == "FROM":
            from_seen = True

    # Buscar JOINs
    for token in parsed.tokens:
        if token.ttype is Keyword and "JOIN" in token.value.upper():
            # Siguiente token después de JOIN es la tabla
            idx = parsed.tokens.index(token)
            if idx + 1 < len(parsed.tokens):
                next_token = parsed.tokens[idx + 1]
                while next_token.is_whitespace and idx + 1 < len(parsed.tokens):
                    idx += 1
                    next_token = parsed.tokens[idx + 1]
                if isinstance(next_token, Identifier):
                    tablas.append(_extraer_nombre_tabla(next_token))

    if not tablas:
        raise ValueError("Query debe contener FROM")

    return tablas


def _extraer_nombre_tabla(identifier: Identifier) -> str:
    """Extrae nombre de tabla de un Identifier, ignorando alias."""
    nombre = identifier.get_real_name()
    return nombre if nombre else str(identifier.get_name())


def extraer_columnas_where(query: str) -> list[str]:
    """
    Extrae nombres de columnas utilizadas en la cláusula WHERE.

    Args:
        query: Consulta SQL

    Returns:
        Lista de nombres de columnas en WHERE

    Examples:
        >>> extraer_columnas_where("SELECT * FROM usuarios WHERE email = 'test@example.com'")
        ['email']
    """
    parsed = sqlparse.parse(query)[0]

    columnas = []
    for token in parsed.tokens:
        if isinstance(token, Where):
            columnas.extend(_extraer_columnas_de_where(token))

    return columnas


def _extraer_columnas_de_where(where_clause: Where) -> list[str]:
    """Extrae columnas de una cláusula WHERE."""
    columnas = []

    for token in where_clause.tokens:
        if isinstance(token, Identifier):
            columnas.append(token.get_real_name() or str(token))
        elif isinstance(token, Function):
            # Extraer columna dentro de función
            for sub_token in token.tokens:
                if isinstance(sub_token, Identifier):
                    columnas.append(sub_token.get_real_name() or str(sub_token))
                elif hasattr(sub_token, "tokens"):
                    for sub_sub_token in sub_token.tokens:
                        if isinstance(sub_sub_token, Identifier):
                            columnas.append(
                                sub_sub_token.get_real_name() or str(sub_sub_token)
                            )
        elif hasattr(token, "tokens"):
            columnas.extend(_extraer_columnas_de_where(token))

    # Usar regex adicional para capturar columnas simples
    where_str = str(where_clause)
    # Buscar patrones: columna = valor, columna > valor, etc.
    pattern = r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|>|<|>=|<=|!=|LIKE|IN)"
    matches = re.findall(pattern, where_str, re.IGNORECASE)
    columnas.extend(matches)

    # Eliminar duplicados preservando orden
    seen = set()
    resultado = []
    for col in columnas:
        col_limpio = col.strip()
        if (
            col_limpio
            and col_limpio.upper() not in ("WHERE", "AND", "OR", "NOT")
            and col_limpio not in seen
        ):
            seen.add(col_limpio)
            resultado.append(col_limpio)

    return resultado


def extraer_columnas_select(query: str) -> list[str]:
    """
    Extrae nombres de columnas en la cláusula SELECT.

    Args:
        query: Consulta SQL

    Returns:
        Lista de nombres de columnas (o ['*'] si es SELECT *)

    Examples:
        >>> extraer_columnas_select("SELECT id, nombre FROM usuarios")
        ['id', 'nombre']
        >>> extraer_columnas_select("SELECT * FROM usuarios")
        ['*']
    """
    # Extraer la parte SELECT antes del FROM
    query_upper = query.upper()
    if "FROM" not in query_upper:
        return []

    select_part = query.split("FROM")[0].split("SELECT")[1].strip()

    # Detectar SELECT *
    if re.match(r"^\*\s*$", select_part) or re.match(r"^\w+\.\*\s*$", select_part):
        return ["*"]

    columnas = []

    # Parsear con sqlparse
    parsed = sqlparse.parse(query)[0]
    select_seen = False

    for token in parsed.tokens:
        if select_seen:
            if token.ttype is Wildcard:
                return ["*"]
            elif isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    col = _extraer_nombre_columna_select(identifier)
                    if col:
                        columnas.append(col)
            elif isinstance(token, Identifier):
                col = _extraer_nombre_columna_select(token)
                if col:
                    columnas.append(col)
            elif isinstance(token, Function):
                # Extraer columnas de funciones agregadas
                cols = _extraer_columnas_de_funcion(token)
                columnas.extend(cols)
            elif token.ttype is Keyword and token.value.upper() == "FROM":
                break

        if token.ttype is Keyword and token.value.upper() == "SELECT":
            select_seen = True

    # Fallback: usar regex si no encontró columnas
    if not columnas:
        # Extraer nombres de columnas simples
        pattern = r"\b([a-zA-Z_][\w\.]*)\b"
        matches = re.findall(pattern, select_part)

        # Filtrar keywords y funciones
        keywords = {"COUNT", "SUM", "AVG", "MIN", "MAX", "AS"}
        columnas = []
        for match in matches:
            if match.upper() not in keywords:
                # Extraer solo el nombre de columna (sin tabla.columna)
                col_name = match.split(".")[-1]
                columnas.append(col_name)

    return columnas


def _extraer_nombre_columna_select(identifier: Identifier | Function) -> str | None:
    """Extrae nombre de columna del SELECT, ignorando alias."""
    if isinstance(identifier, Function):
        cols = _extraer_columnas_de_funcion(identifier)
        return cols[0] if cols else None

    nombre_real = identifier.get_real_name()
    if nombre_real:
        return nombre_real

    # Si tiene alias (AS), extraer nombre original
    nombre_completo = str(identifier)
    if " as " in nombre_completo.lower():
        return nombre_completo.split(" as ")[0].strip()

    # Si tiene punto (tabla.columna), extraer solo columna
    if "." in nombre_completo:
        return nombre_completo.split(".")[-1].strip()

    return nombre_completo.strip() if nombre_completo.strip() else None


def _extraer_columnas_de_funcion(func: Function) -> list[str]:
    """Extrae columnas dentro de funciones agregadas (COUNT, SUM, etc.)."""
    columnas = []

    for token in func.tokens:
        if isinstance(token, Identifier):
            col = token.get_real_name() or str(token)
            columnas.append(col.strip())
        elif hasattr(token, "tokens"):
            for sub_token in token.tokens:
                if isinstance(sub_token, Identifier):
                    col = sub_token.get_real_name() or str(sub_token)
                    if col and col not in ("*",):
                        columnas.append(col.strip())

    return [c for c in columnas if c and c != "*"]


def detectar_select_asterisco(query: str) -> bool:
    """
    Detecta si la consulta usa SELECT *.

    Args:
        query: Consulta SQL

    Returns:
        True si usa SELECT *, False en caso contrario

    Examples:
        >>> detectar_select_asterisco("SELECT * FROM usuarios")
        True
        >>> detectar_select_asterisco("SELECT id, nombre FROM usuarios")
        False
    """
    # Método simple: buscar SELECT *
    query_upper = query.upper()
    patterns = [
        r"SELECT\s+\*",  # SELECT *
        r"SELECT\s+\w+\.\*",  # SELECT u.*
    ]

    return any(re.search(pattern, query_upper) for pattern in patterns)


def detectar_funciones_en_where(query: str) -> dict[str, list[str]]:
    """
    Detecta funciones aplicadas a columnas en WHERE.

    Args:
        query: Consulta SQL

    Returns:
        Diccionario con 'funciones' y 'columnas_afectadas'

    Examples:
        >>> detectar_funciones_en_where("SELECT * FROM ventas WHERE YEAR(fecha) = 2024")
        {'funciones': ['YEAR'], 'columnas_afectadas': ['fecha']}
    """
    parsed = sqlparse.parse(query)[0]

    funciones = []
    columnas_afectadas = []

    for token in parsed.tokens:
        if isinstance(token, Where):
            funcs, cols = _buscar_funciones_en_token(token)
            funciones.extend(funcs)
            columnas_afectadas.extend(cols)

    return {"funciones": funciones, "columnas_afectadas": columnas_afectadas}


def _buscar_funciones_en_token(token: Any) -> tuple[list[str], list[str]]:
    """Busca funciones recursivamente en un token."""
    funciones = []
    columnas = []

    if isinstance(token, Function):
        # Es una función
        func_name = token.get_name()
        if func_name:
            funciones.append(func_name.upper())

        # Extraer columnas dentro de la función
        for sub_token in token.tokens:
            if isinstance(sub_token, Identifier):
                col = sub_token.get_real_name() or str(sub_token)
                columnas.append(col.strip())
            elif hasattr(sub_token, "tokens"):
                for sub_sub_token in sub_token.tokens:
                    if isinstance(sub_sub_token, Identifier):
                        col = sub_sub_token.get_real_name() or str(sub_sub_token)
                        columnas.append(col.strip())

    elif hasattr(token, "tokens"):
        # Buscar recursivamente
        for sub_token in token.tokens:
            sub_funcs, sub_cols = _buscar_funciones_en_token(sub_token)
            funciones.extend(sub_funcs)
            columnas.extend(sub_cols)

    return funciones, columnas


def extraer_joins(query: str) -> list[dict[str, Any]]:
    """
    Extrae información sobre JOINs en la consulta.

    Args:
        query: Consulta SQL

    Returns:
        Lista de diccionarios con información de cada JOIN

    Examples:
        >>> extraer_joins("SELECT * FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id")
        [{'tipo': 'INNER JOIN', 'tabla': 'pedidos', 'columnas_join': ['id', 'usuario_id']}]
    """
    query_upper = query.upper()

    if "JOIN" not in query_upper:
        return []

    joins = []

    # Buscar todos los JOINs
    join_patterns = [
        (r"INNER\s+JOIN", "INNER JOIN"),
        (r"LEFT\s+(?:OUTER\s+)?JOIN", "LEFT JOIN"),
        (r"RIGHT\s+(?:OUTER\s+)?JOIN", "RIGHT JOIN"),
        (r"FULL\s+(?:OUTER\s+)?JOIN", "FULL JOIN"),
        (r"(?<!INNER\s)(?<!LEFT\s)(?<!RIGHT\s)(?<!FULL\s)JOIN", "JOIN"),
    ]

    for pattern, tipo in join_patterns:
        matches = re.finditer(pattern, query_upper)
        for match in matches:
            start = match.end()

            # Extraer tabla (siguiente palabra después de JOIN)
            tabla_match = re.search(r"(\w+)", query[start:])
            if not tabla_match:
                continue

            tabla = tabla_match.group(1)

            # Extraer condición ON
            on_match = re.search(
                r"ON\s+([\w\.]+)\s*=\s*([\w\.]+)", query[start:], re.IGNORECASE
            )
            columnas_join = []
            if on_match:
                col1 = on_match.group(1).split(".")[-1]
                col2 = on_match.group(2).split(".")[-1]
                columnas_join = [col1, col2]

            joins.append({"tipo": tipo, "tabla": tabla, "columnas_join": columnas_join})

    return joins
