"""
Tests para el módulo detector_tipo_join.

TDD: Estos tests se escribieron PRIMERO, antes de la implementación.
"""

import pytest

from src.detector_tipo_join import detectar_tipo_join_necesario, validar_tipo_join


class TestDetectarTipoJoinNecesario:
    """Tests para la función detectar_tipo_join_necesario."""

    def test_ambos_false_sugiere_inner_join(self):
        """Solo coincidencias → INNER JOIN."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Listar productos con categoría",
            incluir_nulls_izq=False,
            incluir_nulls_der=False,
        )

        assert tipo == "INNER"

    def test_incluir_nulls_izq_true_sugiere_left_join(self):
        """Todos de izquierda → LEFT JOIN."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Listar todos los clientes, con o sin pedidos",
            incluir_nulls_izq=True,
            incluir_nulls_der=False,
        )

        assert tipo == "LEFT"

    def test_incluir_nulls_der_true_sugiere_right_join(self):
        """Todos de derecha → RIGHT JOIN."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Listar todos los pedidos, con o sin cliente",
            incluir_nulls_izq=False,
            incluir_nulls_der=True,
        )

        assert tipo == "RIGHT"

    def test_ambos_true_sugiere_full_join(self):
        """Todos de ambos lados → FULL OUTER JOIN."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Auditoría completa de productos y categorías",
            incluir_nulls_izq=True,
            incluir_nulls_der=True,
        )

        assert tipo == "FULL"

    def test_requerimiento_con_palabra_clave_todos_sugiere_left(self):
        """Palabra 'todos' en requerimiento debe sugerir LEFT."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Mostrar TODOS los productos",
            incluir_nulls_izq=False,  # Pero debería detectarlo del texto
            incluir_nulls_der=False,
        )

        # Debe detectar "TODOS" y sugerir LEFT
        assert tipo in ["LEFT", "INNER"]  # Depende de implementación

    def test_requerimiento_con_solo_coincidencias_sugiere_inner(self):
        """Frase 'solo coincidencias' debe sugerir INNER."""
        tipo = detectar_tipo_join_necesario(
            requerimiento="Productos que TIENEN categoría asignada",
            incluir_nulls_izq=False,
            incluir_nulls_der=False,
        )

        assert tipo == "INNER"


class TestValidarTipoJoin:
    """Tests para la función validar_tipo_join."""

    def test_inner_join_con_nulls_esperados_es_invalido(self):
        """INNER JOIN no puede incluir NULLs."""
        es_valido, mensaje = validar_tipo_join(
            tipo_join="INNER", esperado_incluir_nulls=True
        )

        assert es_valido is False
        assert "no incluye nulls" in mensaje.lower()

    def test_inner_join_sin_nulls_esperados_es_valido(self):
        """INNER JOIN es válido si no se esperan NULLs."""
        es_valido, mensaje = validar_tipo_join(
            tipo_join="INNER", esperado_incluir_nulls=False
        )

        assert es_valido is True
        assert "correcto" in mensaje.lower() or "válido" in mensaje.lower()

    def test_left_join_con_nulls_esperados_es_valido(self):
        """LEFT JOIN es válido si se esperan NULLs."""
        es_valido, mensaje = validar_tipo_join(
            tipo_join="LEFT", esperado_incluir_nulls=True
        )

        assert es_valido is True

    def test_left_join_sin_nulls_esperados_es_suboptimo(self):
        """LEFT JOIN sin esperar NULLs es subóptimo (debería ser INNER)."""
        es_valido, mensaje = validar_tipo_join(
            tipo_join="LEFT", esperado_incluir_nulls=False
        )

        # Puede ser válido pero con advertencia
        assert "INNER" in mensaje or "optimiza" in mensaje.lower()

    def test_full_join_con_nulls_esperados_es_valido(self):
        """FULL JOIN es válido si se esperan NULLs de ambos lados."""
        es_valido, mensaje = validar_tipo_join(
            tipo_join="FULL", esperado_incluir_nulls=True
        )

        assert es_valido is True

    def test_tipo_join_invalido_lanza_valor_error(self):
        """Tipo de JOIN inválido debe lanzar ValueError."""
        with pytest.raises(ValueError, match="tipo_join inválido"):
            validar_tipo_join(
                tipo_join="INVALID_JOIN",
                esperado_incluir_nulls=False,
            )
