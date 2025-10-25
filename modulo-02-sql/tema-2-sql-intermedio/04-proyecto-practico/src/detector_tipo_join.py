"""
Módulo detector_tipo_join: Sugiere qué tipo de JOIN usar.

Este módulo analiza requerimientos y sugiere el tipo de JOIN más adecuado
basándose en si se deben incluir registros sin coincidencia (NULLs).
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JOINS_VALIDOS = ["INNER", "LEFT", "RIGHT", "FULL"]


def detectar_tipo_join_necesario(
    requerimiento: str,
    incluir_nulls_izq: bool = False,
    incluir_nulls_der: bool = False,
) -> str:
    """
    Sugiere tipo de JOIN basándose en requerimiento.

    Args:
        requerimiento: Descripción del problema
        incluir_nulls_izq: ¿Incluir filas sin coincidencia de tabla izq?
        incluir_nulls_der: ¿Incluir filas sin coincidencia de tabla der?

    Returns:
        Tipo de JOIN recomendado ('INNER', 'LEFT', 'RIGHT', 'FULL')

    Logic:
        - INNER: Solo coincidencias (ambos False)
        - LEFT: Todos de izquierda (incluir_nulls_izq=True)
        - RIGHT: Todos de derecha (incluir_nulls_der=True)
        - FULL: Todos de ambos (ambos True)

    Example:
        >>> detectar_tipo_join_necesario(
        ...     "Listar todos los clientes, con o sin pedidos",
        ...     incluir_nulls_izq=True
        ... )
        'LEFT'
    """
    # Lógica basada en flags
    if incluir_nulls_izq and incluir_nulls_der:
        logger.info("Detectado: FULL JOIN (todos de ambas tablas)")
        return "FULL"
    elif incluir_nulls_izq and not incluir_nulls_der:
        logger.info("Detectado: LEFT JOIN (todos de tabla izquierda)")
        return "LEFT"
    elif not incluir_nulls_izq and incluir_nulls_der:
        logger.info("Detectado: RIGHT JOIN (todos de tabla derecha)")
        return "RIGHT"
    else:
        logger.info("Detectado: INNER JOIN (solo coincidencias)")
        return "INNER"


def validar_tipo_join(tipo_join: str, esperado_incluir_nulls: bool) -> tuple[bool, str]:
    """
    Valida si el tipo de JOIN elegido es correcto.

    Args:
        tipo_join: JOIN elegido ('INNER', 'LEFT', etc.)
        esperado_incluir_nulls: ¿Se espera incluir NULLs?

    Returns:
        (es_valido, mensaje_explicativo)

    Example:
        >>> validar_tipo_join('INNER', esperado_incluir_nulls=True)
        (False, 'INNER JOIN no incluye NULLs, usa LEFT o FULL')
    """
    # Validar que tipo_join sea válido
    if tipo_join not in JOINS_VALIDOS:
        raise ValueError(
            f"tipo_join inválido: '{tipo_join}'. "
            f"Debe ser uno de: {', '.join(JOINS_VALIDOS)}"
        )

    # Lógica de validación
    if tipo_join == "INNER":
        if esperado_incluir_nulls:
            return (
                False,
                "INNER JOIN no incluye NULLs, usa LEFT, RIGHT o FULL",
            )
        else:
            return (True, "INNER JOIN es correcto para solo coincidencias")

    elif tipo_join == "LEFT":
        if esperado_incluir_nulls:
            return (
                True,
                "LEFT JOIN es correcto para incluir todos de la izquierda",
            )
        else:
            return (
                True,
                "LEFT JOIN funciona, pero INNER JOIN sería más optimizado "
                "si no esperas NULLs",
            )

    elif tipo_join == "RIGHT":
        if esperado_incluir_nulls:
            return (
                True,
                "RIGHT JOIN es correcto para incluir todos de la derecha",
            )
        else:
            return (
                True,
                "RIGHT JOIN funciona, pero INNER JOIN sería más optimizado",
            )

    elif tipo_join == "FULL":
        if esperado_incluir_nulls:
            return (
                True,
                "FULL JOIN es correcto para incluir todos de ambos lados",
            )
        else:
            return (
                True,
                "FULL JOIN funciona, pero INNER JOIN sería suficiente",
            )

    return (False, "Caso no contemplado")
