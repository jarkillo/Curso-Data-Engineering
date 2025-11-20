"""
Módulo para estrategia de carga upsert (insert + update).

Implementa funciones para insertar registros nuevos y actualizar existentes.
"""

import pandas as pd
from sqlalchemy import Engine, text


def upsert(df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str) -> None:
    """
    Upsert: inserta registros nuevos y actualiza existentes.

    Estrategia: DELETE registros con claves existentes + INSERT todos.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna que identifica registros únicos

    Raises:
        ValueError: Si la columna clave no existe

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})
        >>> upsert(df, engine, "tabla", "id")
    """
    if columna_clave not in df.columns:
        raise ValueError(f"Columna clave '{columna_clave}' no existe en el DataFrame")

    with engine.begin() as conn:
        # Verificar si tabla existe
        try:
            conn.execute(text(f"SELECT 1 FROM {tabla} LIMIT 1"))
            tabla_existe = True
        except Exception:
            tabla_existe = False

        if tabla_existe:
            # Eliminar registros con claves que vamos a insertar
            # Usar bound parameters para evitar SQL injection
            claves = df[columna_clave].tolist()

            if claves:  # Solo ejecutar si hay claves
                # Crear placeholders para bound parameters
                placeholders = ",".join([f":key_{i}" for i in range(len(claves))])
                # Crear dict de parámetros
                params = {f"key_{i}": clave for i, clave in enumerate(claves)}

                conn.execute(
                    text(
                        f"DELETE FROM {tabla} WHERE {columna_clave} IN ({placeholders})"
                    ),
                    params,
                )

        # Insertar todos los registros
        df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")


def upsert_con_metricas(
    df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str
) -> dict:
    """
    Upsert con métricas de inserts vs updates.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna clave

    Returns:
        Dict con métricas: {"inserts": int, "updates": int, "total": int}

    Examples:
        >>> resultado = upsert_con_metricas(df, engine, "tabla", "id")
        >>> print(f"Inserts: {resultado['inserts']}, Updates: {resultado['updates']}")
    """
    # Contar registros antes
    try:
        total_antes = pd.read_sql(
            f"SELECT COUNT(*) as total FROM {tabla}", engine
        ).iloc[0]["total"]
    except Exception:
        total_antes = 0

    # Ejecutar upsert
    upsert(df, engine, tabla, columna_clave)

    # Contar después
    total_despues = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", engine).iloc[
        0
    ]["total"]

    # Calcular métricas
    inserts = total_despues - total_antes
    updates = len(df) - inserts

    return {"inserts": inserts, "updates": updates, "total": len(df)}


def detectar_cambios(
    df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detecta qué registros son nuevos vs existentes.

    Args:
        df: DataFrame a analizar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna clave

    Returns:
        Tupla (df_nuevos, df_existentes)

    Examples:
        >>> df_nuevos, df_existentes = detectar_cambios(df, engine, "tabla", "id")
        >>> print(f"Nuevos: {len(df_nuevos)}, Existentes: {len(df_existentes)}")
    """
    # Intentar leer claves existentes
    try:
        claves_bd = pd.read_sql(f"SELECT {columna_clave} FROM {tabla}", engine)[
            columna_clave
        ].tolist()
    except Exception:
        # Tabla no existe, todos son nuevos
        return df, pd.DataFrame()

    # Separar nuevos de existentes
    mask_nuevos = ~df[columna_clave].isin(claves_bd)
    df_nuevos = df[mask_nuevos].copy()
    df_existentes = df[~mask_nuevos].copy()

    return df_nuevos, df_existentes
