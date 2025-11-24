"""
Módulo de validación de calidad de datos.

Valida esquemas, duplicados y rangos de datos Silver.
"""

import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema

# Esquema para capa Silver
ESQUEMA_SILVER = DataFrameSchema(
    {
        "id": Column(int, nullable=False),
        "titulo": Column(str, nullable=False),
        "contenido": Column(str, nullable=True),
        "autor": Column(str, nullable=True),
        "fecha_publicacion": Column(pa.DateTime, nullable=False),
        "fuente": Column(str, nullable=False),
        "categoria": Column(str, nullable=True),
        "url": Column(str, nullable=True),
        "longitud_contenido": Column(float, nullable=True),
        "longitud_titulo": Column(float, nullable=True),
    },
    strict=False,  # Permitir columnas adicionales
    coerce=True,  # Coerce tipos si es posible
)


def validar_esquema_silver(df: pd.DataFrame) -> None:
    """
    Valida que DataFrame cumpla con esquema Silver.

    Args:
        df: DataFrame a validar

    Raises:
        pandera.errors.SchemaError: Si validación falla

    Examples:
        >>> df = pd.DataFrame({
        ...     "id": [1],
        ...     "titulo": ["Test"],
        ...     "fecha_publicacion": pd.to_datetime(["2024-01-01"])
        ... })
        >>> validar_esquema_silver(df)  # doctest: +SKIP
    """
    ESQUEMA_SILVER.validate(df)


def validar_sin_duplicados(df: pd.DataFrame, columna: str) -> dict:
    """
    Valida que no existan duplicados en una columna.

    Args:
        df: DataFrame a validar
        columna: Columna a verificar duplicados

    Returns:
        Dict con resultado: {"valido": bool, "duplicados": int}

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2, 3]})
        >>> resultado = validar_sin_duplicados(df, "id")
        >>> resultado["valido"]
        True
    """
    num_duplicados = df[columna].duplicated().sum()

    return {"valido": num_duplicados == 0, "duplicados": int(num_duplicados)}


def validar_rangos_longitud(
    df: pd.DataFrame, columna: str, min_val: int, max_val: int
) -> dict:
    """
    Valida que valores de longitud estén dentro de un rango.

    Args:
        df: DataFrame a validar
        columna: Columna a verificar
        min_val: Valor mínimo permitido
        max_val: Valor máximo permitido

    Returns:
        Dict con resultado: {"valido": bool, "fuera_de_rango": int}

    Examples:
        >>> df = pd.DataFrame({"longitud": [10, 20, 30]})
        >>> resultado = validar_rangos_longitud(df, "longitud", 5, 50)
        >>> resultado["valido"]
        True
    """
    # Contar valores fuera de rango (excluyendo nulos)
    mask_valido = (df[columna].notna()) & (
        (df[columna] < min_val) | (df[columna] > max_val)
    )
    fuera_de_rango = mask_valido.sum()

    return {"valido": fuera_de_rango == 0, "fuera_de_rango": int(fuera_de_rango)}


def generar_reporte_calidad(df: pd.DataFrame) -> dict:
    """
    Genera reporte completo de calidad de datos.

    Valida:
    - Esquema Silver
    - Duplicados en ID
    - Rangos de longitud de contenido y título

    Args:
        df: DataFrame Silver a analizar

    Returns:
        Dict con reporte de calidad

    Examples:
        >>> df = pd.DataFrame({
        ...     "id": [1, 2],
        ...     "titulo": ["A", "B"],
        ...     "fecha_publicacion": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        ...     "fuente": ["X", "Y"],
        ...     "longitud_contenido": [100, 200],
        ...     "longitud_titulo": [10, 20]
        ... })
        >>> reporte = generar_reporte_calidad(df)
        >>> "total_registros" in reporte
        True
    """
    reporte = {"total_registros": len(df)}

    # Validar esquema
    try:
        validar_esquema_silver(df)
        reporte["esquema_valido"] = True
    except Exception as e:
        reporte["esquema_valido"] = False
        reporte["error_esquema"] = str(e)

    # Validar duplicados
    duplicados_id = validar_sin_duplicados(df, "id")
    reporte["duplicados"] = {
        "valido": duplicados_id["valido"],
        "total": duplicados_id["duplicados"],
    }

    # Validar rangos de longitud
    reporte["longitudes_validas"] = {}

    if "longitud_contenido" in df.columns:
        val_contenido = validar_rangos_longitud(
            df, "longitud_contenido", min_val=10, max_val=10000
        )
        reporte["longitudes_validas"]["contenido"] = val_contenido

    if "longitud_titulo" in df.columns:
        val_titulo = validar_rangos_longitud(
            df, "longitud_titulo", min_val=5, max_val=200
        )
        reporte["longitudes_validas"]["titulo"] = val_titulo

    return reporte
