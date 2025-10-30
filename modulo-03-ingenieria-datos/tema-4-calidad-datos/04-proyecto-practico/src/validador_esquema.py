"""Módulo de Validación de Esquemas y Reglas de Negocio.

Funciones para validar tipos, rangos, valores permitidos y esquemas completos.
"""

from typing import Dict, List, Tuple

import pandas as pd


def validar_tipos_columnas(
    df: pd.DataFrame, esquema: Dict[str, str]
) -> Tuple[bool, List[str]]:
    """
    Valida que las columnas del DataFrame tengan los tipos esperados.

    Args:
        df: DataFrame a validar
        esquema: Dict con nombre_columna: tipo_esperado
                Tipos soportados: 'int', 'float', 'str', 'bool'

    Returns:
        Tupla (es_valido, lista_errores)

    Raises:
        ValueError: Si DataFrame está vacío

    Example:
        >>> df = pd.DataFrame({'id': [1, 2], 'nombre': ['A', 'B']})
        >>> esquema = {'id': 'int', 'nombre': 'str'}
        >>> es_valido, errores = validar_tipos_columnas(df, esquema)
        >>> assert es_valido is True
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    errores = []

    # Mapeo de tipos esperados a tipos de pandas
    mapeo_tipos = {
        "int": ["int64", "int32", "int16", "int8"],
        "float": ["float64", "float32"],
        "str": ["object"],
        "bool": ["bool"],
    }

    for columna, tipo_esperado in esquema.items():
        # Verificar que columna existe
        if columna not in df.columns:
            errores.append(f"Columna '{columna}' no encontrada en DataFrame")
            continue

        # Verificar que tipo esperado es reconocido
        if tipo_esperado not in mapeo_tipos:
            errores.append(
                f"Tipo '{tipo_esperado}' no reconocido para columna '{columna}'"
            )
            continue

        # Obtener tipo actual
        tipo_actual = str(df[columna].dtype)

        # Verificar tipo
        tipos_validos = mapeo_tipos[tipo_esperado]
        if tipo_actual not in tipos_validos:
            errores.append(
                f"Columna '{columna}': esperado {tipo_esperado}, encontrado {tipo_actual}"
            )

    es_valido = len(errores) == 0
    return es_valido, errores


def validar_rangos_numericos(
    df: pd.DataFrame, rangos: Dict[str, Tuple[float, float]]
) -> Dict:
    """
    Valida que valores numéricos estén en rangos válidos.

    Args:
        df: DataFrame a validar
        rangos: Dict con columna: (min, max)

    Returns:
        Dict con:
        - es_valido: bool
        - errores: List[str]
        - valores_fuera_rango: Dict[str, pd.DataFrame]

    Raises:
        ValueError: Si DataFrame está vacío

    Example:
        >>> df = pd.DataFrame({'edad': [25, 30, 35]})
        >>> rangos = {'edad': (18, 70)}
        >>> resultado = validar_rangos_numericos(df, rangos)
        >>> assert resultado['es_valido'] is True
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    resultado = {"es_valido": True, "errores": [], "valores_fuera_rango": {}}

    for columna, (minimo, maximo) in rangos.items():
        if columna not in df.columns:
            resultado["errores"].append(f"Columna '{columna}' no existe")  # type: ignore[attr-defined]
            resultado["es_valido"] = False
            continue

        if not pd.api.types.is_numeric_dtype(df[columna]):
            resultado["errores"].append(f"Columna '{columna}' no es numérica")  # type: ignore[attr-defined]
            resultado["es_valido"] = False
            continue

        # Detectar valores fuera de rango
        fuera_rango = df[(df[columna] < minimo) | (df[columna] > maximo)]

        if not fuera_rango.empty:
            resultado["es_valido"] = False
            resultado["valores_fuera_rango"][columna] = fuera_rango  # type: ignore[index]
            resultado["errores"].append(  # type: ignore[attr-defined]
                f"Columna '{columna}': {len(fuera_rango)} valores fuera del rango [{minimo}, {maximo}]"
            )

    return resultado


def validar_valores_unicos(df: pd.DataFrame, columnas: List[str]) -> Tuple[bool, Dict]:
    """
    Verifica que columnas especificadas no tengan duplicados.

    Args:
        df: DataFrame a validar
        columnas: Lista de columnas que deben tener valores únicos

    Returns:
        Tupla (es_valido, dict_con_estadisticas)

    Raises:
        KeyError: Si alguna columna no existe

    Example:
        >>> df = pd.DataFrame({'id': [1, 2, 3]})
        >>> es_valido, resultado = validar_valores_unicos(df, ['id'])
        >>> assert es_valido is True
    """
    resultado = {}
    es_valido = True

    for columna in columnas:
        if columna not in df.columns:
            raise KeyError(f"Columna '{columna}' no existe en DataFrame")

        duplicados_count = df[columna].duplicated().sum()

        resultado[columna] = {
            "duplicados": duplicados_count,
            "valores_unicos": df[columna].nunique(),
            "total_valores": len(df[columna]),
        }

        if duplicados_count > 0:
            es_valido = False

    return es_valido, resultado


def validar_valores_permitidos(df: pd.DataFrame, reglas: Dict[str, List]) -> Dict:
    """
    Valida que valores estén en listas permitidas (enums).

    Args:
        df: DataFrame a validar
        reglas: Dict con columna: lista_valores_permitidos

    Returns:
        Dict con:
        - es_valido: bool
        - errores: List[str]
        - valores_invalidos: Dict[str, List]

    Example:
        >>> df = pd.DataFrame({'categoria': ['A', 'B', 'A']})
        >>> reglas = {'categoria': ['A', 'B', 'C']}
        >>> resultado = validar_valores_permitidos(df, reglas)
        >>> assert resultado['es_valido'] is True
    """
    resultado = {"es_valido": True, "errores": [], "valores_invalidos": {}}

    for columna, valores_permitidos in reglas.items():
        if columna not in df.columns:
            resultado["errores"].append(f"Columna '{columna}' no existe")  # type: ignore[attr-defined]
            resultado["es_valido"] = False
            continue

        # Encontrar valores no permitidos
        valores_actuales = df[columna].dropna().unique()
        valores_no_permitidos = [
            valor for valor in valores_actuales if valor not in valores_permitidos
        ]

        if valores_no_permitidos:
            resultado["es_valido"] = False
            resultado["valores_invalidos"][columna] = valores_no_permitidos  # type: ignore[index]
            resultado["errores"].append(  # type: ignore[attr-defined]
                f"Columna '{columna}': valores no permitidos encontrados: {valores_no_permitidos}"
            )

    return resultado


def validar_nulls_permitidos(df: pd.DataFrame, columnas_requeridas: List[str]) -> Dict:
    """
    Verifica que columnas requeridas no tengan valores nulos.

    Args:
        df: DataFrame a validar
        columnas_requeridas: Lista de columnas que no pueden tener nulls

    Returns:
        Dict con:
        - es_valido: bool
        - errores: List[str]
        - columnas_con_nulls: Dict[str, int]

    Raises:
        KeyError: Si alguna columna no existe

    Example:
        >>> df = pd.DataFrame({'id': [1, 2, 3], 'nombre': ['A', 'B', 'C']})
        >>> resultado = validar_nulls_permitidos(df, ['id', 'nombre'])
        >>> assert resultado['es_valido'] is True
    """
    resultado = {"es_valido": True, "errores": [], "columnas_con_nulls": {}}

    for columna in columnas_requeridas:
        if columna not in df.columns:
            raise KeyError(f"Columna '{columna}' no existe en DataFrame")

        nulls_count = df[columna].isnull().sum()

        if nulls_count > 0:
            resultado["es_valido"] = False
            resultado["columnas_con_nulls"][columna] = int(nulls_count)  # type: ignore[index]
            resultado["errores"].append(  # type: ignore[attr-defined]
                f"Columna '{columna}': {nulls_count} valores nulos encontrados"
            )

    return resultado


def validar_esquema_completo(
    df: pd.DataFrame, configuracion: Dict
) -> Tuple[bool, Dict]:
    """
    Ejecuta todas las validaciones de forma integrada.

    Args:
        df: DataFrame a validar
        configuracion: Dict con configuraciones de validación:
            - tipos: Dict[str, str] - Esquema de tipos
            - rangos: Dict[str, Tuple[float, float]] - Rangos válidos
            - columnas_requeridas: List[str] - Columnas sin nulls
            - valores_unicos: List[str] - Columnas con valores únicos
            - valores_permitidos: Dict[str, List] - Valores enum

    Returns:
        Tupla (es_valido, reporte_completo)

    Example:
        >>> df = pd.DataFrame({'id': [1, 2, 3], 'edad': [25, 30, 35]})
        >>> config = {
        ...     'tipos': {'id': 'int', 'edad': 'int'},
        ...     'rangos': {'edad': (18, 70)}
        ... }
        >>> es_valido, reporte = validar_esquema_completo(df, config)
        >>> assert es_valido is True
    """
    reporte = {}
    es_valido_global = True

    # Validar tipos
    if "tipos" in configuracion:
        es_valido, errores = validar_tipos_columnas(df, configuracion["tipos"])
        reporte["validacion_tipos"] = {"es_valido": es_valido, "errores": errores}
        es_valido_global = es_valido_global and es_valido

    # Validar rangos
    if "rangos" in configuracion:
        resultado = validar_rangos_numericos(df, configuracion["rangos"])
        reporte["validacion_rangos"] = resultado
        es_valido_global = es_valido_global and resultado["es_valido"]

    # Validar nulls
    if "columnas_requeridas" in configuracion:
        resultado = validar_nulls_permitidos(df, configuracion["columnas_requeridas"])
        reporte["validacion_nulls"] = resultado
        es_valido_global = es_valido_global and resultado["es_valido"]

    # Validar unicidad
    if "valores_unicos" in configuracion:
        es_valido, resultado = validar_valores_unicos(
            df, configuracion["valores_unicos"]
        )
        reporte["validacion_unicidad"] = {
            "es_valido": es_valido,
            "resultado": resultado,
        }
        es_valido_global = es_valido_global and es_valido

    # Validar valores permitidos
    if "valores_permitidos" in configuracion:
        resultado = validar_valores_permitidos(df, configuracion["valores_permitidos"])
        reporte["validacion_valores_permitidos"] = resultado
        es_valido_global = es_valido_global and resultado["es_valido"]

    return es_valido_global, reporte


def generar_reporte_validacion(resultados_validacion: Dict) -> str:
    """
    Genera reporte legible de resultados de validación.

    Args:
        resultados_validacion: Dict con resultados de validaciones

    Returns:
        String con reporte formateado

    Example:
        >>> resultados = {
        ...     'validacion_tipos': {'es_valido': True, 'errores': []}
        ... }
        >>> reporte = generar_reporte_validacion(resultados)
        >>> assert isinstance(reporte, str)
    """
    lineas = []
    lineas.append("=" * 60)
    lineas.append("REPORTE DE VALIDACIÓN DE ESQUEMA")
    lineas.append("=" * 60)
    lineas.append("")

    # Contador de validaciones
    total_validaciones = len(resultados_validacion)
    validaciones_exitosas = 0

    # Procesar cada validación
    for nombre_validacion, resultado in resultados_validacion.items():
        titulo = nombre_validacion.replace("_", " ").title()
        lineas.append(f"{titulo}:")
        lineas.append("-" * 60)

        if isinstance(resultado, dict):
            es_valido = resultado.get("es_valido", False)

            if es_valido:
                lineas.append("  ✓ Validación exitosa")
                validaciones_exitosas += 1
            else:
                lineas.append("  ✗ Validación fallida")

                # Mostrar errores
                errores = resultado.get("errores", [])
                if errores:
                    lineas.append("  Errores:")
                    for error in errores:
                        lineas.append(f"    - {error}")

        lineas.append("")

    # Resumen final
    lineas.append("=" * 60)
    lineas.append("RESUMEN")
    lineas.append("=" * 60)
    lineas.append(f"Total de validaciones: {total_validaciones}")
    lineas.append(f"Exitosas: {validaciones_exitosas}")
    lineas.append(f"Fallidas: {total_validaciones - validaciones_exitosas}")

    if validaciones_exitosas == total_validaciones:
        lineas.append("")
        lineas.append("✓ Todas las validaciones pasaron correctamente")
    else:
        lineas.append("")
        lineas.append("✗ Algunas validaciones fallaron. Revisar errores arriba.")

    return "\n".join(lineas)
