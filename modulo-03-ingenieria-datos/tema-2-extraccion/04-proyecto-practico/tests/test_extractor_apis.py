"""
Tests para el módulo extractor_apis.

Usa mocks para simular respuestas HTTP sin hacer peticiones reales.
"""

import time
from unittest.mock import Mock, patch

import pytest
import requests
from src.extractor_apis import (
    configurar_sesion_con_reintentos,
    extraer_api_completa,
    hacer_peticion_con_autenticacion,
    manejar_paginacion_cursor,
    manejar_paginacion_offset_limit,
    respetar_rate_limit,
)

# ============================================================================
# Tests para configurar_sesion_con_reintentos
# ============================================================================


class TestConfigurarSesionConReintentos:
    """Tests para la función configurar_sesion_con_reintentos."""

    def test_retorna_sesion_valida(self):
        """Debe retornar una sesión de requests válida."""
        sesion = configurar_sesion_con_reintentos()

        assert isinstance(sesion, requests.Session)

    def test_configura_con_parametros_personalizados(self):
        """Debe aceptar parámetros personalizados."""
        sesion = configurar_sesion_con_reintentos(
            max_reintentos=5, backoff_factor=0.5, status_forcelist=(429, 500, 502)
        )

        assert isinstance(sesion, requests.Session)

    def test_lanza_error_con_reintentos_negativos(self):
        """Debe lanzar ValueError si max_reintentos es negativo."""
        with pytest.raises(ValueError, match="max_reintentos"):
            configurar_sesion_con_reintentos(max_reintentos=-1)

    def test_lanza_error_con_backoff_negativo(self):
        """Debe lanzar ValueError si backoff_factor es negativo."""
        with pytest.raises(ValueError, match="backoff_factor"):
            configurar_sesion_con_reintentos(backoff_factor=-0.1)


# ============================================================================
# Tests para hacer_peticion_con_autenticacion
# ============================================================================


class TestHacerPeticionConAutenticacion:
    """Tests para la función hacer_peticion_con_autenticacion."""

    @patch("src.extractor_apis.configurar_sesion_con_reintentos")
    def test_peticion_get_exitosa(self, mock_sesion):
        """Debe realizar petición GET exitosa."""
        # Configurar mock
        mock_respuesta = Mock()
        mock_respuesta.json.return_value = {"data": "test"}
        mock_respuesta.raise_for_status = Mock()

        mock_sesion_instance = Mock()
        mock_sesion_instance.request.return_value = mock_respuesta
        mock_sesion.return_value = mock_sesion_instance

        # Ejecutar
        resultado = hacer_peticion_con_autenticacion("https://api.test.com/data")

        # Verificar
        assert resultado == {"data": "test"}
        mock_sesion_instance.request.assert_called_once()

    @patch("src.extractor_apis.configurar_sesion_con_reintentos")
    def test_peticion_con_auth_bearer(self, mock_sesion):
        """Debe agregar header Authorization con Bearer token."""
        mock_respuesta = Mock()
        mock_respuesta.json.return_value = {"data": "test"}
        mock_respuesta.raise_for_status = Mock()

        mock_sesion_instance = Mock()
        mock_sesion_instance.request.return_value = mock_respuesta
        mock_sesion.return_value = mock_sesion_instance

        # Ejecutar
        hacer_peticion_con_autenticacion(
            "https://api.test.com/data", auth_type="bearer", auth_token="mi_token"
        )

        # Verificar que se llamó con el header correcto
        call_kwargs = mock_sesion_instance.request.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
        assert call_kwargs["headers"]["Authorization"] == "Bearer mi_token"

    @patch("src.extractor_apis.configurar_sesion_con_reintentos")
    def test_peticion_con_auth_api_key(self, mock_sesion):
        """Debe agregar header X-API-Key."""
        mock_respuesta = Mock()
        mock_respuesta.json.return_value = {"data": "test"}
        mock_respuesta.raise_for_status = Mock()

        mock_sesion_instance = Mock()
        mock_sesion_instance.request.return_value = mock_respuesta
        mock_sesion.return_value = mock_sesion_instance

        # Ejecutar
        hacer_peticion_con_autenticacion(
            "https://api.test.com/data", auth_type="api_key", auth_token="mi_api_key"
        )

        # Verificar
        call_kwargs = mock_sesion_instance.request.call_args[1]
        assert "X-API-Key" in call_kwargs["headers"]

    def test_lanza_error_con_url_vacia(self):
        """Debe lanzar ValueError si la URL está vacía."""
        with pytest.raises(ValueError, match="URL no puede estar vacía"):
            hacer_peticion_con_autenticacion("")

    def test_lanza_error_con_metodo_invalido(self):
        """Debe lanzar ValueError con método HTTP no soportado."""
        with pytest.raises(ValueError, match="no soportado"):
            hacer_peticion_con_autenticacion(
                "https://api.test.com/data", metodo="INVALID"
            )

    def test_lanza_error_auth_type_sin_token(self):
        """Debe lanzar ValueError si se especifica auth_type sin token."""
        with pytest.raises(ValueError, match="auth_token"):
            hacer_peticion_con_autenticacion(
                "https://api.test.com/data", auth_type="bearer"
            )

    @patch("src.extractor_apis.configurar_sesion_con_reintentos")
    def test_maneja_respuesta_no_json(self, mock_sesion):
        """Debe manejar respuestas que no son JSON."""
        mock_respuesta = Mock()
        mock_respuesta.json.side_effect = Exception("No es JSON")
        mock_respuesta.text = "Respuesta en texto plano"
        mock_respuesta.raise_for_status = Mock()

        mock_sesion_instance = Mock()
        mock_sesion_instance.request.return_value = mock_respuesta
        mock_sesion.return_value = mock_sesion_instance

        # Ejecutar
        resultado = hacer_peticion_con_autenticacion("https://api.test.com/data")

        # Verificar
        assert resultado == {"content": "Respuesta en texto plano"}


# ============================================================================
# Tests para manejar_paginacion_offset_limit
# ============================================================================


class TestManejarPaginacionOffsetLimit:
    """Tests para la función manejar_paginacion_offset_limit."""

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_paginacion_una_sola_pagina(self, mock_peticion):
        """Debe manejar correctamente una sola página."""
        mock_peticion.return_value = {"data": [{"id": 1}, {"id": 2}]}

        resultados = manejar_paginacion_offset_limit(
            "https://api.test.com/data", limite_por_pagina=10
        )

        assert len(resultados) == 2
        assert resultados[0]["id"] == 1

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_paginacion_multiples_paginas(self, mock_peticion):
        """Debe iterar por múltiples páginas."""
        # Primera página: 3 resultados
        # Segunda página: 2 resultados (menos que el límite, última página)
        mock_peticion.side_effect = [
            {"data": [{"id": 1}, {"id": 2}, {"id": 3}]},
            {"data": [{"id": 4}, {"id": 5}]},
        ]

        resultados = manejar_paginacion_offset_limit(
            "https://api.test.com/data", limite_por_pagina=3
        )

        assert len(resultados) == 5
        assert resultados[-1]["id"] == 5

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_respeta_max_resultados(self, mock_peticion):
        """Debe respetar el límite de max_resultados."""
        mock_peticion.side_effect = [
            {"data": [{"id": 1}, {"id": 2}, {"id": 3}]},
            {"data": [{"id": 4}, {"id": 5}, {"id": 6}]},
        ]

        resultados = manejar_paginacion_offset_limit(
            "https://api.test.com/data", limite_por_pagina=3, max_resultados=4
        )

        assert len(resultados) == 4

    def test_lanza_error_con_limite_invalido(self):
        """Debe lanzar ValueError si limite_por_pagina <= 0."""
        with pytest.raises(ValueError, match="limite_por_pagina"):
            manejar_paginacion_offset_limit(
                "https://api.test.com/data", limite_por_pagina=0
            )

    def test_lanza_error_con_max_resultados_invalido(self):
        """Debe lanzar ValueError si max_resultados <= 0."""
        with pytest.raises(ValueError, match="max_resultados"):
            manejar_paginacion_offset_limit(
                "https://api.test.com/data", max_resultados=0
            )


# ============================================================================
# Tests para manejar_paginacion_cursor
# ============================================================================


class TestManejarPaginacionCursor:
    """Tests para la función manejar_paginacion_cursor."""

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_paginacion_cursor_simple(self, mock_peticion):
        """Debe manejar paginación con cursor correctamente."""
        mock_peticion.side_effect = [
            {"data": [{"id": 1}, {"id": 2}], "next_cursor": "cursor2"},
            {"data": [{"id": 3}], "next_cursor": None},
        ]

        resultados = manejar_paginacion_cursor("https://api.test.com/data")

        assert len(resultados) == 3
        assert resultados[-1]["id"] == 3

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_paginacion_cursor_nested(self, mock_peticion):
        """Debe manejar cursor en estructura nested."""
        mock_peticion.side_effect = [
            {"data": [{"id": 1}], "meta": {"next_cursor": "cursor2"}},
            {"data": [{"id": 2}], "meta": {"next_cursor": None}},
        ]

        resultados = manejar_paginacion_cursor(
            "https://api.test.com/data", campo_cursor_respuesta="meta.next_cursor"
        )

        assert len(resultados) == 2


# ============================================================================
# Tests para respetar_rate_limit
# ============================================================================


class TestRespetarRateLimit:
    """Tests para la función respetar_rate_limit."""

    def test_primera_peticion_no_espera(self):
        """Primera petición no debe esperar."""
        inicio = time.time()
        respetar_rate_limit(60, tiempo_ultima_peticion=None)
        duracion = time.time() - inicio

        # Debe ser casi instantáneo
        assert duracion < 0.1

    def test_espera_si_es_necesario(self):
        """Debe esperar si no ha pasado suficiente tiempo."""
        tiempo_ultima = time.time()
        inicio = time.time()

        # Con 120 peticiones/minuto, debe esperar ~0.5s entre peticiones
        respetar_rate_limit(120, tiempo_ultima_peticion=tiempo_ultima)

        duracion = time.time() - inicio
        # Debe haber esperado aproximadamente 0.5s
        assert duracion >= 0.4

    def test_lanza_error_con_rate_limit_invalido(self):
        """Debe lanzar ValueError si peticiones_por_minuto <= 0."""
        with pytest.raises(ValueError, match="peticiones_por_minuto"):
            respetar_rate_limit(0)


# ============================================================================
# Tests para extraer_api_completa
# ============================================================================


class TestExtraerApiCompleta:
    """Tests para la función extraer_api_completa."""

    @patch("src.extractor_apis.hacer_peticion_con_autenticacion")
    def test_extraccion_sin_paginacion(self, mock_peticion):
        """Debe manejar APIs sin paginación."""
        mock_peticion.return_value = {"id": 1, "nombre": "Test"}

        resultados = extraer_api_completa(
            "https://api.test.com/data", tipo_paginacion="none"
        )

        assert len(resultados) == 1
        assert resultados[0]["id"] == 1

    @patch("src.extractor_apis.manejar_paginacion_offset_limit")
    def test_extraccion_con_paginacion_offset(self, mock_paginacion):
        """Debe usar paginación offset correctamente."""
        mock_paginacion.return_value = [{"id": 1}, {"id": 2}]

        resultados = extraer_api_completa(
            "https://api.test.com/data", tipo_paginacion="offset"
        )

        assert len(resultados) == 2
        mock_paginacion.assert_called_once()

    @patch("src.extractor_apis.manejar_paginacion_cursor")
    def test_extraccion_con_paginacion_cursor(self, mock_paginacion):
        """Debe usar paginación cursor correctamente."""
        mock_paginacion.return_value = [{"id": 1}, {"id": 2}]

        resultados = extraer_api_completa(
            "https://api.test.com/data", tipo_paginacion="cursor"
        )

        assert len(resultados) == 2
        mock_paginacion.assert_called_once()

    def test_lanza_error_con_tipo_paginacion_invalido(self):
        """Debe lanzar ValueError con tipo de paginación inválido."""
        with pytest.raises(ValueError, match="tipo_paginacion"):
            extraer_api_completa(
                "https://api.test.com/data", tipo_paginacion="invalido"
            )


# ============================================================================
# Tests de Integración
# ============================================================================


class TestIntegracionAPIs:
    """Tests de integración entre funciones de APIs."""

    @patch("src.extractor_apis.configurar_sesion_con_reintentos")
    def test_flujo_completo_api_con_auth(self, mock_sesion):
        """Test del flujo completo con autenticación."""
        # Configurar mock
        mock_respuesta = Mock()
        mock_respuesta.json.return_value = {"data": [{"id": 1, "nombre": "Test"}]}
        mock_respuesta.raise_for_status = Mock()

        mock_sesion_instance = Mock()
        mock_sesion_instance.request.return_value = mock_respuesta
        mock_sesion.return_value = mock_sesion_instance

        # Ejecutar flujo
        resultado = hacer_peticion_con_autenticacion(
            "https://api.test.com/data",
            auth_type="bearer",
            auth_token="test_token",
            params={"filtro": "activo"},
        )

        # Verificar
        assert "data" in resultado
        assert len(resultado["data"]) == 1
