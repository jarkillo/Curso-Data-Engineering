"""
Módulo para estrategia de carga incremental.

Implementa funciones para cargar solo registros nuevos desde el último checkpoint.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import Engine


def guardar_checkpoint(valor: str | int, archivo: str) -> None:
    """
    Guarda un checkpoint en archivo.

    Args:
        valor: Valor del checkpoint (ID, timestamp, etc.)
        archivo: Ruta al archivo de checkpoint

    Examples:
        >>> guardar_checkpoint(100, "checkpoint.txt")
        >>> guardar_checkpoint("2024-01-15 10:30:00", "checkpoint.txt")
    """
    Path(archivo).write_text(str(valor))


def leer_checkpoint(archivo: str) -> str | int:
    """
    Lee el último checkpoint desde archivo.

    Args:
        archivo: Ruta al archivo de checkpoint

    Returns:
        Valor del checkpoint, o 0 si el archivo no existe

    Examples:
        >>> ultimo_id = leer_checkpoint("checkpoint.txt")
        >>> print(ultimo_id)
        100
    """
    checkpoint_path = Path(archivo)

    if checkpoint_path.exists():
        contenido = checkpoint_path.read_text().strip()
        # Intentar convertir a int, si no, retornar como string
        try:
            return int(contenido)
        except ValueError:
            return contenido
    else:
        return 0


def incremental_load(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    columna_timestamp: str,
    checkpoint_file: str,
) -> dict:
    """
    Carga incremental: solo registros nuevos desde último checkpoint.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_timestamp: Nombre de la columna temporal para filtrar
        checkpoint_file: Archivo de checkpoint

    Returns:
        Dict con métricas: {"procesados": int, "cargados": int, "omitidos": int}

    Raises:
        ValueError: Si la columna de timestamp no existe

    Examples:
        >>> df = pd.DataFrame({
        ...     "id": [1, 2, 3],
        ...     "timestamp": pd.date_range("2024-01-15", periods=3, freq="h"),
        ...     "valor": [100, 200, 300]
        ... })
        >>> resultado = incremental_load(df, engine, "tabla", "timestamp", "checkpoint.txt")
        >>> print(resultado["cargados"])
        3
    """
    if columna_timestamp not in df.columns:
        raise ValueError(f"Columna '{columna_timestamp}' no existe en el DataFrame")

    # Leer último checkpoint
    checkpoint = leer_checkpoint(checkpoint_file)

    # Convertir a timestamp si es string
    if isinstance(checkpoint, str) and checkpoint != "0":
        try:
            last_timestamp = pd.Timestamp(checkpoint)
        except Exception:
            last_timestamp = pd.Timestamp("2000-01-01")
    elif checkpoint == 0:
        last_timestamp = pd.Timestamp("2000-01-01")
    else:
        last_timestamp = checkpoint

    # Filtrar solo registros nuevos
    if pd.api.types.is_datetime64_any_dtype(df[columna_timestamp]):
        df_nuevos = df[df[columna_timestamp] > last_timestamp].copy()
    else:
        df_nuevos = df[df[columna_timestamp] > checkpoint].copy()

    procesados = len(df)
    cargados = len(df_nuevos)
    omitidos = procesados - cargados

    if cargados > 0:
        # Cargar solo registros nuevos
        with engine.begin() as conn:
            df_nuevos.to_sql(
                tabla, conn, if_exists="append", index=False, method="multi"
            )

        # Actualizar checkpoint con el valor máximo
        nuevo_checkpoint = df_nuevos[columna_timestamp].max()
        guardar_checkpoint(str(nuevo_checkpoint), checkpoint_file)

    return {"procesados": procesados, "cargados": cargados, "omitidos": omitidos}


def incremental_load_con_validacion(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    columna_timestamp: str,
    checkpoint_file: str,
    columnas_requeridas: list[str] | None = None,
    columnas_no_nulas: list[str] | None = None,
) -> dict:
    """
    Carga incremental con validación previa.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_timestamp: Columna temporal para filtrar
        checkpoint_file: Archivo de checkpoint
        columnas_requeridas: Columnas que deben existir
        columnas_no_nulas: Columnas que no deben tener nulos

    Returns:
        Dict con resultado: {"valido": bool, "cargados": int, "invalidos": int, "mensaje": str}

    Examples:
        >>> resultado = incremental_load_con_validacion(
        ...     df,
        ...     engine,
        ...     "tabla",
        ...     "timestamp",
        ...     "checkpoint.txt",
        ...     columnas_requeridas=["id", "timestamp"]
        ... )
        >>> print(resultado["valido"])
        True
    """
    resultado = {"valido": True, "cargados": 0, "invalidos": 0, "mensaje": "OK"}

    # Validar columnas requeridas
    if columnas_requeridas:
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if columnas_faltantes:
            resultado["valido"] = False
            resultado["mensaje"] = f"Faltan columnas: {columnas_faltantes}"
            return resultado

    # Filtrar registros inválidos (con nulos en columnas críticas)
    df_valido = df.copy()

    if columnas_no_nulas:
        mask_valido = pd.Series([True] * len(df))
        for col in columnas_no_nulas:
            if col in df.columns:
                mask_valido &= df[col].notna()

        df_valido = df[mask_valido].copy()
        resultado["invalidos"] = len(df) - len(df_valido)

    # Cargar registros válidos
    try:
        metricas = incremental_load(
            df_valido, engine, tabla, columna_timestamp, checkpoint_file
        )
        resultado["cargados"] = metricas["cargados"]
    except Exception as e:
        resultado["valido"] = False
        resultado["mensaje"] = f"Error durante carga: {str(e)}"

    return resultado
