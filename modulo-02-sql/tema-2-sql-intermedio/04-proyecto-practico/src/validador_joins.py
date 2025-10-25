"""
Módulo validador_joins: Valida integridad de resultados de JOINs.

Este módulo proporciona funciones para detectar problemas comunes en JOINs
como productos cartesianos, pérdida de datos y duplicación de filas.
"""

import logging
import sqlite3
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JOINS_VALIDOS = ["INNER", "LEFT", "RIGHT", "FULL"]


def validar_resultado_join(  # noqa: C901
    filas_tabla_izq: int,
    filas_tabla_der: int,
    filas_resultado: int,
    tipo_join: str,
) -> tuple[bool, str]:
    """
    Detecta pérdida o duplicación de datos en JOIN.

    Args:
        filas_tabla_izq: Filas de tabla izquierda
        filas_tabla_der: Filas de tabla derecha
        filas_resultado: Filas del resultado
        tipo_join: Tipo de JOIN ejecutado

    Returns:
        (es_valido, mensaje_diagnostico)

    Logic:
        - INNER: resultado <= min(izq, der)
        - LEFT: resultado >= izq
        - RIGHT: resultado >= der
        - FULL: resultado >= max(izq, der)
        - Alerta si resultado >> (izq * der) → producto cartesiano

    Example:
        >>> validar_resultado_join(100, 10, 1000, 'INNER')
        (False, 'Posible producto cartesiano: 1000 >> 100')
    """
    # Validar tipo_join
    if tipo_join not in JOINS_VALIDOS:
        raise ValueError(
            f"tipo_join inválido: '{tipo_join}'. "
            f"Debe ser uno de: {', '.join(JOINS_VALIDOS)}"
        )

    # Detectar producto cartesiano primero
    es_cartesiano, _ = detectar_producto_cartesiano(
        filas_tabla_izq, filas_tabla_der, filas_resultado
    )

    if es_cartesiano:
        return (
            False,
            f"Posible producto cartesiano detectado: "
            f"{filas_resultado} filas >> esperado",
        )

    # Validación específica por tipo de JOIN
    if tipo_join == "INNER":
        # INNER JOIN debe retornar <= min(izq, der)
        max_esperado = min(filas_tabla_izq, filas_tabla_der)
        if filas_resultado > max_esperado:
            return (
                False,
                f"INNER JOIN retornó {filas_resultado} filas, "
                f"pero máximo esperado es {max_esperado}. "
                f"Posible duplicación.",
            )
        return (True, "INNER JOIN: Resultado válido")

    elif tipo_join == "LEFT":
        # LEFT JOIN debe retornar >= filas_izq
        if filas_resultado < filas_tabla_izq:
            return (
                False,
                f"LEFT JOIN retornó {filas_resultado} filas, "
                f"pero debe ser >= {filas_tabla_izq} (tabla izquierda). "
                f"Posible pérdida de datos.",
            )
        return (True, "LEFT JOIN: Resultado válido")

    elif tipo_join == "RIGHT":
        # RIGHT JOIN debe retornar >= filas_der
        if filas_resultado < filas_tabla_der:
            return (
                False,
                f"RIGHT JOIN retornó {filas_resultado} filas, "
                f"pero debe ser >= {filas_tabla_der} (tabla derecha). "
                f"Posible pérdida de datos.",
            )
        return (True, "RIGHT JOIN: Resultado válido")

    elif tipo_join == "FULL":
        # FULL JOIN debe retornar >= max(izq, der)
        min_esperado = max(filas_tabla_izq, filas_tabla_der)
        if filas_resultado < min_esperado:
            return (
                False,
                f"FULL JOIN retornó {filas_resultado} filas, "
                f"pero debe ser >= {min_esperado}. "
                f"Posible pérdida de datos.",
            )
        return (True, "FULL JOIN: Resultado válido")

    return (False, "Tipo de JOIN no reconocido")


def detectar_producto_cartesiano(
    filas_izq: int,
    filas_der: int,
    filas_resultado: int,
    umbral: float = 0.8,
) -> tuple[bool, str]:
    """
    Detecta si el JOIN generó un producto cartesiano accidental.

    Args:
        filas_izq: Filas tabla izquierda
        filas_der: Filas tabla derecha
        filas_resultado: Filas resultado
        umbral: Umbral de alerta (0.8 = 80% del producto total)

    Returns:
        (es_producto_cartesiano, mensaje)

    Logic:
        Si filas_resultado > (filas_izq * filas_der * umbral):
            Producto cartesiano detectado

    Example:
        >>> detectar_producto_cartesiano(100, 50, 5000)
        (True, 'Producto cartesiano: 5000 >= 4000 (80% de 100×50)')
    """
    # Manejar casos especiales
    if filas_izq == 0 or filas_der == 0:
        return (False, "Una de las tablas está vacía")

    if filas_resultado == 0:
        return (False, "Resultado vacío, no hay producto cartesiano")

    # Calcular producto total y umbral
    producto_total = filas_izq * filas_der
    umbral_absoluto = producto_total * umbral

    # Detectar
    if filas_resultado >= umbral_absoluto:
        porcentaje = (filas_resultado / producto_total) * 100
        return (
            True,
            f"Producto cartesiano detectado: {filas_resultado} filas "
            f"({porcentaje:.1f}% de {filas_izq}×{filas_der}={producto_total}). "
            f"Verifica la condición ON del JOIN.",
        )

    return (False, "No se detectó producto cartesiano")


def contar_filas_join(
    conexion: sqlite3.Connection,
    tabla_izq: str,
    tabla_der: str,
    query_join: str,
) -> dict[str, Any]:
    """
    Cuenta filas de tablas base y resultado para verificar integridad.

    Args:
        conexion: Conexión SQLite activa
        tabla_izq: Tabla izquierda
        tabla_der: Tabla derecha
        query_join: Query completa del JOIN

    Returns:
        {
            'filas_izq': int,
            'filas_der': int,
            'filas_resultado': int,
            'ratio': float  # resultado / (izq * der)
        }

    Raises:
        sqlite3.Error: Si hay error en alguna query

    Example:
        >>> conteo = contar_filas_join(
        ...     conn, 'productos', 'categorias',
        ...     'SELECT * FROM productos p JOIN categorias c ON p.cat_id=c.id'
        ... )
        >>> conteo['ratio'] < 0.1  # No es producto cartesiano
        True
    """
    try:
        cursor = conexion.cursor()

        # Contar tabla izquierda
        cursor.execute(f"SELECT COUNT(*) FROM {tabla_izq}")
        filas_izq = cursor.fetchone()[0]

        # Contar tabla derecha
        cursor.execute(f"SELECT COUNT(*) FROM {tabla_der}")
        filas_der = cursor.fetchone()[0]

        # Contar resultado del JOIN
        cursor.execute(query_join)
        filas_resultado = len(cursor.fetchall())

        # Calcular ratio
        producto_total = filas_izq * filas_der
        ratio = filas_resultado / producto_total if producto_total > 0 else 0.0

        logger.info(
            f"Conteo JOIN: izq={filas_izq}, der={filas_der}, "
            f"resultado={filas_resultado}, ratio={ratio:.3f}"
        )

        return {
            "filas_izq": filas_izq,
            "filas_der": filas_der,
            "filas_resultado": filas_resultado,
            "ratio": ratio,
        }

    except sqlite3.Error as e:
        logger.error(f"Error al contar filas: {str(e)}")
        raise sqlite3.Error(f"Error al contar filas: {str(e)}")
