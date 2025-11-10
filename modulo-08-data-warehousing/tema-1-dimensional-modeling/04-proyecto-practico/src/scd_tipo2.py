"""
Módulo de lógica genérica para Slowly Changing Dimension Type 2.

Este módulo provee funciones reutilizables para implementar SCD Type 2
en cualquier tabla de dimensión, manteniendo el historial completo de cambios.

Funciones:
    detectar_cambios: Detecta si hubo cambios en campos rastreables
    cerrar_version_anterior: Cierra una versión antigua con fecha_fin
    generar_nueva_version: Crea nueva versión con datos actualizados
    aplicar_scd_tipo2: Función principal para aplicar SCD Type 2 a un DataFrame
"""

from datetime import date

import pandas as pd


def detectar_cambios(
    registro_actual: dict, registro_nuevo: dict, campos_rastreables: list[str]
) -> bool:
    """
    Detecta si hubo cambios en los campos rastreables entre dos registros.

    Args:
        registro_actual: Diccionario con datos actuales
        registro_nuevo: Diccionario con datos nuevos
        campos_rastreables: Lista de campos a comparar

    Returns:
        True si hay cambios, False si los datos son idénticos

    Examples:
        >>> actual = {"email": "old@test.com", "telefono": "555-1234"}
        >>> nuevo = {"email": "new@test.com", "telefono": "555-1234"}
        >>> detectar_cambios(actual, nuevo, ["email", "telefono"])
        True

        >>> actual = {"email": "same@test.com", "telefono": "555-1234"}
        >>> nuevo = {"email": "same@test.com", "telefono": "555-1234"}
        >>> detectar_cambios(actual, nuevo, ["email", "telefono"])
        False
    """
    for campo in campos_rastreables:
        valor_actual = registro_actual.get(campo)
        valor_nuevo = registro_nuevo.get(campo)

        if valor_actual != valor_nuevo:
            return True

    return False


def cerrar_version_anterior(registro: dict, fecha_cierre: date) -> dict:
    """
    Cierra una versión anterior estableciendo fecha_fin y es_actual=False.

    Args:
        registro: Diccionario con versión a cerrar
        fecha_cierre: Fecha de cierre de la versión

    Returns:
        Diccionario con versión cerrada

    Examples:
        >>> registro = {
        ...     "cliente_id": 1,
        ...     "email": "old@test.com",
        ...     "fecha_inicio": date(2023, 1, 1),
        ...     "fecha_fin": None,
        ...     "version": 1,
        ...     "es_actual": True
        ... }
        >>> cerrado = cerrar_version_anterior(registro, date(2024, 6, 1))
        >>> cerrado["fecha_fin"]
        datetime.date(2024, 6, 1)
        >>> cerrado["es_actual"]
        False
    """
    registro_cerrado = registro.copy()

    # Solo cerrar si aún está abierto
    if registro_cerrado.get("es_actual") and registro_cerrado.get("fecha_fin") is None:
        registro_cerrado["fecha_fin"] = fecha_cierre
        registro_cerrado["es_actual"] = False

    return registro_cerrado


def generar_nueva_version(
    registro_anterior: dict, datos_nuevos: dict, fecha_inicio: date
) -> dict:
    """
    Genera una nueva versión con datos actualizados.

    Args:
        registro_anterior: Diccionario con versión anterior
        datos_nuevos: Diccionario con datos actualizados
        fecha_inicio: Fecha de inicio de la nueva versión

    Returns:
        Diccionario con nueva versión

    Examples:
        >>> anterior = {
        ...     "cliente_id": 1,
        ...     "email": "old@test.com",
        ...     "version": 1
        ... }
        >>> nuevos = {
        ...     "cliente_id": 1,
        ...     "email": "new@test.com"
        ... }
        >>> nueva = generar_nueva_version(anterior, nuevos, date(2024, 6, 1))
        >>> nueva["version"]
        2
        >>> nueva["email"]
        'new@test.com'
        >>> nueva["es_actual"]
        True
    """
    nueva_version = datos_nuevos.copy()

    # Incrementar versión
    version_anterior = registro_anterior.get("version", 0)
    nueva_version["version"] = version_anterior + 1

    # Campos SCD Type 2
    nueva_version["fecha_inicio"] = fecha_inicio
    nueva_version["fecha_fin"] = None
    nueva_version["es_actual"] = True

    return nueva_version


def aplicar_scd_tipo2(  # noqa: C901
    df_actual: pd.DataFrame,
    df_nuevos: pd.DataFrame,
    campo_id: str,
    campos_rastreables: list[str],
    fecha_proceso: date,
) -> pd.DataFrame:
    """
    Aplica lógica SCD Type 2 a un DataFrame de dimensión.

    Procesa:
    - Nuevos registros: Crea versión 1 con es_actual=True
    - Registros sin cambios: Mantiene versión actual
    - Registros con cambios: Cierra versión anterior y crea nueva versión

    Args:
        df_actual: DataFrame con dimensión actual (puede estar vacío)
        df_nuevos: DataFrame con datos nuevos a procesar
        campo_id: Nombre del campo ID (ej: "cliente_id")
        campos_rastreables: Lista de campos a rastrear cambios
        fecha_proceso: Fecha de procesamiento

    Returns:
        DataFrame con dimensión actualizada incluyendo historial

    Examples:
        >>> # Nuevo cliente
        >>> df_actual = pd.DataFrame()
        >>> df_nuevos = pd.DataFrame([
        ...     {"cliente_id": 1, "email": "juan@test.com"}
        ... ])
        >>> result = aplicar_scd_tipo2(
        ...     df_actual, df_nuevos, "cliente_id", ["email"], date(2024, 1, 1)
        ... )
        >>> len(result)
        1
        >>> result.iloc[0]["version"]
        1

        >>> # Cliente con cambio
        >>> df_actual = pd.DataFrame([
        ...     {
        ...         "cliente_id": 1,
        ...         "email": "old@test.com",
        ...         "fecha_inicio": date(2024, 1, 1),
        ...         "fecha_fin": None,
        ...         "version": 1,
        ...         "es_actual": True
        ...     }
        ... ])
        >>> df_nuevos = pd.DataFrame([
        ...     {"cliente_id": 1, "email": "new@test.com"}
        ... ])
        >>> result = aplicar_scd_tipo2(
        ...     df_actual, df_nuevos, "cliente_id", ["email"], date(2024, 6, 1)
        ... )
        >>> len(result)
        2
        >>> sum(result["es_actual"])
        1
    """
    resultado = []

    # Si no hay datos actuales, todos los nuevos son versión 1
    if df_actual.empty:
        for _, row in df_nuevos.iterrows():
            nuevo_registro = row.to_dict()
            nuevo_registro["fecha_inicio"] = fecha_proceso
            nuevo_registro["fecha_fin"] = None
            nuevo_registro["version"] = 1
            nuevo_registro["es_actual"] = True
            resultado.append(nuevo_registro)

        return pd.DataFrame(resultado)

    # Procesar cada registro nuevo
    for _, row_nuevo in df_nuevos.iterrows():
        id_valor = row_nuevo[campo_id]

        # Buscar si existe en datos actuales
        df_actual_id = df_actual[df_actual[campo_id] == id_valor]

        if df_actual_id.empty:
            # Es un registro NUEVO (no existía antes)
            nuevo_registro = row_nuevo.to_dict()
            nuevo_registro["fecha_inicio"] = fecha_proceso
            nuevo_registro["fecha_fin"] = None
            nuevo_registro["version"] = 1
            nuevo_registro["es_actual"] = True
            resultado.append(nuevo_registro)

        else:
            # Registro EXISTENTE - obtener versión actual
            df_version_actual = df_actual_id[df_actual_id["es_actual"]]

            if df_version_actual.empty:
                # No debería pasar, pero manejar caso edge
                # Crear versión 1 si no hay actual
                nuevo_registro = row_nuevo.to_dict()
                nuevo_registro["fecha_inicio"] = fecha_proceso
                nuevo_registro["fecha_fin"] = None
                nuevo_registro["version"] = 1
                nuevo_registro["es_actual"] = True
                resultado.append(nuevo_registro)
            else:
                version_actual = df_version_actual.iloc[0].to_dict()

                # Detectar si hay cambios
                hay_cambios = detectar_cambios(
                    version_actual, row_nuevo.to_dict(), campos_rastreables
                )

                if hay_cambios:
                    # HAY CAMBIOS: Cerrar versión anterior y crear nueva
                    version_cerrada = cerrar_version_anterior(
                        version_actual, fecha_proceso
                    )
                    resultado.append(version_cerrada)

                    # Generar nueva versión
                    nueva_version = generar_nueva_version(
                        version_actual, row_nuevo.to_dict(), fecha_proceso
                    )
                    resultado.append(nueva_version)

                else:
                    # SIN CAMBIOS: Mantener versión actual
                    resultado.append(version_actual)

    # Agregar registros históricos (versiones cerradas) que no están en nuevos
    for _, row_actual in df_actual.iterrows():
        id_valor = row_actual[campo_id]
        es_actual = row_actual["es_actual"]

        # Solo agregar si NO es actual (es histórico) y no está ya en resultado
        if not es_actual:
            # Verificar que no esté ya procesado
            ya_existe = any(
                r[campo_id] == id_valor and r["version"] == row_actual["version"]
                for r in resultado
            )

            if not ya_existe:
                resultado.append(row_actual.to_dict())

    # Agregar registros actuales que NO aparecen en df_nuevos (se mantienen sin cambios)
    for _, row_actual in df_actual.iterrows():
        id_valor = row_actual[campo_id]
        es_actual = row_actual["es_actual"]

        if es_actual:
            # Verificar si este ID está en df_nuevos
            esta_en_nuevos = id_valor in df_nuevos[campo_id].values

            if not esta_en_nuevos:
                # No está en nuevos, mantener registro actual
                ya_existe = any(
                    r[campo_id] == id_valor
                    and r["version"] == row_actual["version"]
                    and r["es_actual"]
                    for r in resultado
                )

                if not ya_existe:
                    resultado.append(row_actual.to_dict())

    return pd.DataFrame(resultado)
