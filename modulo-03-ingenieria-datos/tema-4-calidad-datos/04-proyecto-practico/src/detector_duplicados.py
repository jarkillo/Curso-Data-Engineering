"""Módulo de Detección y Manejo de Duplicados.

Funciones para detectar duplicados exactos y fuzzy,
y para eliminarlos según diferentes estrategias.
"""

import pandas as pd
from rapidfuzz import fuzz


def detectar_duplicados_exactos(df: pd.DataFrame, columnas: list[str]) -> pd.Series:
    """
    Identifica duplicados exactos en columnas especificadas.

    Args:
        df: DataFrame a analizar
        columnas: Lista de columnas para identificar duplicados

    Returns:
        Serie booleana indicando qué registros son duplicados

    Raises:
        ValueError: Si DataFrame está vacío
        KeyError: Si alguna columna no existe

    Example:
        >>> df = pd.DataFrame({'id': [1, 2, 2, 3]})
        >>> duplicados = detectar_duplicados_exactos(df, ['id'])
        >>> assert duplicados.sum() == 2
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    for col in columnas:
        if col not in df.columns:
            raise KeyError(f"Columna '{col}' no existe en DataFrame")

    # Marcar duplicados (keep=False marca todos los duplicados, no solo el primero)
    mascara_duplicados = df.duplicated(subset=columnas, keep=False)

    return mascara_duplicados


def detectar_duplicados_fuzzy(
    df: pd.DataFrame, columna: str, umbral: int = 85
) -> pd.DataFrame:
    """
    Encuentra valores similares usando fuzzy matching.

    Args:
        df: DataFrame a analizar
        columna: Nombre de la columna para comparar
        umbral: Score mínimo para considerar match (0-100)

    Returns:
        DataFrame con pares de posibles duplicados y scores

    Raises:
        ValueError: Si DataFrame está vacío o columna no válida

    Example:
        >>> df = pd.DataFrame({'nombre': ['Juan Perez', 'Juan Pérez']})
        >>> duplicados = detectar_duplicados_fuzzy(df, 'nombre', umbral=90)
        >>> assert len(duplicados) == 1
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe")

    valores = df[columna].dropna().unique().tolist()
    duplicados_fuzzy = []

    for i, valor1 in enumerate(valores):
        for valor2 in valores[i + 1 :]:
            # Calcular similitud con RapidFuzz
            score = fuzz.ratio(str(valor1), str(valor2))

            if score >= umbral:
                duplicados_fuzzy.append(
                    {"valor1": valor1, "valor2": valor2, "score": score}
                )

    if duplicados_fuzzy:
        df_resultado = pd.DataFrame(duplicados_fuzzy)
        df_resultado = df_resultado.sort_values("score", ascending=False)
        return df_resultado
    else:
        return pd.DataFrame(columns=["valor1", "valor2", "score"])


def eliminar_duplicados_con_estrategia(
    df: pd.DataFrame, columnas: list[str], estrategia: str = "primero"
) -> pd.DataFrame:
    """
    Elimina duplicados según estrategia especificada.

    Args:
        df: DataFrame con posibles duplicados
        columnas: Columnas para identificar duplicados
        estrategia: 'primero', 'ultimo', o 'mas_completo'

    Returns:
        DataFrame sin duplicados

    Raises:
        ValueError: Si estrategia no es válida

    Example:
        >>> df = pd.DataFrame({'id': [1, 1, 2], 'nombre': ['Ana', 'Ana', 'Luis']})
        >>> df_limpio = eliminar_duplicados_con_estrategia(df, ['id'], 'primero')
        >>> assert len(df_limpio) == 2
    """
    if df.empty:
        return df.copy()

    estrategias_validas = ["primero", "ultimo", "mas_completo"]
    if estrategia not in estrategias_validas:
        raise ValueError(
            f"Estrategia '{estrategia}' no válida. Usar una de: {estrategias_validas}"
        )

    if estrategia == "primero":
        return df.drop_duplicates(subset=columnas, keep="first").reset_index(drop=True)

    elif estrategia == "ultimo":
        return df.drop_duplicates(subset=columnas, keep="last").reset_index(drop=True)

    elif estrategia == "mas_completo":
        # Identificar duplicados
        mascara_duplicados = df.duplicated(subset=columnas, keep=False)

        if not mascara_duplicados.any():
            return df.copy()

        # Separar únicos y duplicados
        df_unicos = df[~mascara_duplicados].copy()
        df_duplicados = df[mascara_duplicados].copy()

        # Para cada grupo de duplicados, elegir el más completo
        mejores_registros = []

        for _, grupo in df_duplicados.groupby(columnas):
            # Calcular score de completitud para cada registro
            scores = []

            for idx in grupo.index:
                # Contar valores no nulos
                score = grupo.loc[idx].notna().sum()
                scores.append((idx, score))

            # Elegir el registro con mayor score
            mejor_idx = max(scores, key=lambda x: x[1])[0]
            mejores_registros.append(grupo.loc[mejor_idx])

        # Combinar únicos con mejores duplicados
        if mejores_registros:
            df_consolidado = pd.concat(
                [df_unicos, pd.DataFrame(mejores_registros)], ignore_index=True
            )
        else:
            df_consolidado = df_unicos

        return df_consolidado


def marcar_duplicados_probables(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Añade columna booleana marcando duplicados.

    Args:
        df: DataFrame a analizar
        columnas: Columnas para identificar duplicados

    Returns:
        DataFrame con columna 'es_duplicado' añadida

    Example:
        >>> df = pd.DataFrame({'id': [1, 1, 2]})
        >>> df_marcado = marcar_duplicados_probables(df, ['id'])
        >>> assert 'es_duplicado' in df_marcado.columns
    """
    df_resultado = df.copy()

    # Marcar duplicados
    df_resultado["es_duplicado"] = df_resultado.duplicated(subset=columnas, keep=False)

    return df_resultado


def generar_reporte_duplicados(df: pd.DataFrame, columnas: list[str]) -> dict:
    """
    Genera estadísticas detalladas de duplicados.

    Args:
        df: DataFrame a analizar
        columnas: Columnas para identificar duplicados

    Returns:
        Dict con estadísticas:
        - total_registros
        - registros_duplicados
        - registros_unicos
        - porcentaje_duplicados
        - grupos_duplicados
        - duplicados_por_grupo

    Raises:
        ValueError: Si DataFrame está vacío

    Example:
        >>> df = pd.DataFrame({'id': [1, 2, 2, 3]})
        >>> reporte = generar_reporte_duplicados(df, ['id'])
        >>> assert reporte['registros_duplicados'] == 2
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    # Detectar duplicados
    mascara_duplicados = df.duplicated(subset=columnas, keep=False)
    df_duplicados = df[mascara_duplicados]

    reporte = {
        "total_registros": len(df),
        "registros_duplicados": mascara_duplicados.sum(),
        "registros_unicos": (~mascara_duplicados).sum(),
        "porcentaje_duplicados": round((mascara_duplicados.sum() / len(df)) * 100, 2),
        "grupos_duplicados": 0,
        "duplicados_por_grupo": {},
    }

    # Identificar grupos de duplicados
    if not df_duplicados.empty:
        grupos = df_duplicados.groupby(columnas).size()
        reporte["grupos_duplicados"] = len(grupos)
        reporte["duplicados_por_grupo"] = grupos.to_dict()

    return reporte
