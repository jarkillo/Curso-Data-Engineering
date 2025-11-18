"""
Tests para scd_tipo2.py.

Tests escritos PRIMERO siguiendo TDD para lógica genérica SCD Type 2.
Cobertura objetivo: ≥90% (módulo crítico para integridad histórica).
"""

from datetime import date

import pandas as pd


class TestDetectarCambios:
    """Tests para la función detectar_cambios."""

    def test_detecta_cambio_en_email(self):
        """Should detect change when email is different."""
        from src.scd_tipo2 import detectar_cambios

        registro_actual = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@old.com",
            "telefono": "555-1234",
        }

        registro_nuevo = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@new.com",
            "telefono": "555-1234",
        }

        campos_rastreables = ["email", "telefono"]

        tiene_cambios = detectar_cambios(
            registro_actual, registro_nuevo, campos_rastreables
        )

        assert tiene_cambios

    def test_no_detecta_cambio_si_datos_iguales(self):
        """Should not detect changes when data is identical."""
        from src.scd_tipo2 import detectar_cambios

        registro_actual = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "555-1234",
        }

        registro_nuevo = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "555-1234",
        }

        campos_rastreables = ["email", "telefono"]

        tiene_cambios = detectar_cambios(
            registro_actual, registro_nuevo, campos_rastreables
        )

        assert not tiene_cambios

    def test_detecta_cambio_en_telefono(self):
        """Should detect change when phone is different."""
        from src.scd_tipo2 import detectar_cambios

        registro_actual = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "555-1234",
        }

        registro_nuevo = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "555-5678",
        }

        campos_rastreables = ["email", "telefono"]

        tiene_cambios = detectar_cambios(
            registro_actual, registro_nuevo, campos_rastreables
        )

        assert tiene_cambios

    def test_ignora_campos_no_rastreables(self):
        """Should ignore changes in fields not being tracked."""
        from src.scd_tipo2 import detectar_cambios

        registro_actual = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "segmento": "Regular",
        }

        registro_nuevo = {
            "cliente_id": 1,
            "nombre": "Juan Pérez Modificado",  # Cambio no rastreable
            "email": "juan@example.com",
            "segmento": "Premium",  # Cambio no rastreable
        }

        campos_rastreables = ["email"]  # Solo rastreamos email

        tiene_cambios = detectar_cambios(
            registro_actual, registro_nuevo, campos_rastreables
        )

        assert not tiene_cambios


class TestCerrarVersionAnterior:
    """Tests para la función cerrar_version_anterior."""

    def test_cierra_version_anterior_con_fecha_fin(self):
        """Should set fecha_fin and es_actual=False for old version."""
        from src.scd_tipo2 import cerrar_version_anterior

        registro_anterior = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@old.com",
            "fecha_inicio": date(2023, 1, 1),
            "fecha_fin": None,
            "version": 1,
            "es_actual": True,
        }

        fecha_cierre = date(2024, 6, 15)

        registro_cerrado = cerrar_version_anterior(registro_anterior, fecha_cierre)

        assert registro_cerrado["fecha_fin"] == fecha_cierre
        assert not registro_cerrado["es_actual"]
        # Otros campos no deben cambiar
        assert registro_cerrado["version"] == 1
        assert registro_cerrado["cliente_id"] == 1

    def test_no_modifica_version_si_ya_cerrada(self):
        """Should not modify version if already closed."""
        from src.scd_tipo2 import cerrar_version_anterior

        registro_ya_cerrado = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@old.com",
            "fecha_inicio": date(2023, 1, 1),
            "fecha_fin": date(2024, 1, 1),
            "version": 1,
            "es_actual": False,
        }

        fecha_cierre = date(2024, 6, 15)

        registro_cerrado = cerrar_version_anterior(registro_ya_cerrado, fecha_cierre)

        # No debe cambiar nada si ya está cerrado
        assert registro_cerrado["fecha_fin"] == date(2024, 1, 1)  # Fecha original
        assert not registro_cerrado["es_actual"]


class TestGenerarNuevaVersion:
    """Tests para la función generar_nueva_version."""

    def test_genera_version_2_con_nuevos_datos(self):
        """Should create version 2 with updated data."""
        from src.scd_tipo2 import generar_nueva_version

        registro_anterior = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@old.com",
            "telefono": "555-1234",
            "fecha_inicio": date(2023, 1, 1),
            "fecha_fin": date(2024, 6, 15),
            "version": 1,
            "es_actual": False,
        }

        datos_nuevos = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@new.com",  # Cambio
            "telefono": "555-5678",  # Cambio
        }

        fecha_inicio_nueva = date(2024, 6, 15)

        nueva_version = generar_nueva_version(
            registro_anterior, datos_nuevos, fecha_inicio_nueva
        )

        assert nueva_version["version"] == 2
        assert nueva_version["email"] == "juan@new.com"
        assert nueva_version["telefono"] == "555-5678"
        assert nueva_version["fecha_inicio"] == fecha_inicio_nueva
        assert nueva_version["fecha_fin"] is None
        assert nueva_version["es_actual"]

    def test_genera_version_3_correctamente(self):
        """Should create version 3 from version 2."""
        from src.scd_tipo2 import generar_nueva_version

        registro_version2 = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@v2.com",
            "telefono": "555-5678",
            "fecha_inicio": date(2024, 1, 1),
            "fecha_fin": date(2024, 8, 1),
            "version": 2,
            "es_actual": False,
        }

        datos_nuevos = {
            "cliente_id": 1,
            "nombre": "Juan Pérez",
            "email": "juan@v3.com",
            "telefono": "555-9999",
        }

        fecha_inicio_nueva = date(2024, 8, 1)

        nueva_version = generar_nueva_version(
            registro_version2, datos_nuevos, fecha_inicio_nueva
        )

        assert nueva_version["version"] == 3
        assert nueva_version["es_actual"]


class TestAplicarSCDTipo2:
    """Tests para la función aplicar_scd_tipo2 (función principal)."""

    def test_nuevo_cliente_sin_historial(self):
        """Should create initial version for new customer."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # DataFrame vacío (sin historial)
        df_actual = pd.DataFrame()

        # Nuevo cliente
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@example.com",
                    "telefono": "555-1234",
                }
            ]
        )

        campos_rastreables = ["email", "telefono"]
        fecha_proceso = date(2024, 1, 1)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        assert len(df_result) == 1
        assert df_result.iloc[0]["version"] == 1
        assert df_result.iloc[0]["es_actual"]
        assert df_result.iloc[0]["fecha_inicio"] == fecha_proceso
        assert pd.isna(df_result.iloc[0]["fecha_fin"])

    def test_cliente_sin_cambios_no_crea_nueva_version(self):
        """Should not create new version if data hasn't changed."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # Cliente existente
        df_actual = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@example.com",
                    "telefono": "555-1234",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 1,
                    "es_actual": True,
                }
            ]
        )

        # Mismos datos (sin cambios)
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@example.com",
                    "telefono": "555-1234",
                }
            ]
        )

        campos_rastreables = ["email", "telefono"]
        fecha_proceso = date(2024, 6, 1)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        # Solo debe haber 1 registro (no se creó versión nueva)
        assert len(df_result) == 1
        assert df_result.iloc[0]["version"] == 1
        assert df_result.iloc[0]["es_actual"]

    def test_cliente_con_cambio_crea_nueva_version(self):
        """Should create version 2 when data changes."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # Cliente existente version 1
        df_actual = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@old.com",
                    "telefono": "555-1234",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 1,
                    "es_actual": True,
                }
            ]
        )

        # Datos con cambio en email
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan Pérez",
                    "email": "juan@new.com",  # CAMBIO
                    "telefono": "555-1234",
                }
            ]
        )

        campos_rastreables = ["email", "telefono"]
        fecha_proceso = date(2024, 6, 15)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        # Debe haber 2 registros (version 1 cerrada + version 2 actual)
        assert len(df_result) == 2

        # Verificar version 1 (cerrada)
        v1 = df_result[df_result["version"] == 1].iloc[0]
        assert v1["fecha_fin"] == fecha_proceso
        assert not v1["es_actual"]
        assert v1["email"] == "juan@old.com"

        # Verificar version 2 (actual)
        v2 = df_result[df_result["version"] == 2].iloc[0]
        assert v2["fecha_inicio"] == fecha_proceso
        assert pd.isna(v2["fecha_fin"])
        assert v2["es_actual"]
        assert v2["email"] == "juan@new.com"

    def test_multiples_clientes_con_cambios_mixtos(self):
        """Should handle multiple customers with mixed scenarios."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # 3 clientes existentes
        df_actual = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@old.com",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 1,
                    "es_actual": True,
                },
                {
                    "cliente_id": 2,
                    "nombre": "María",
                    "email": "maria@example.com",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 1,
                    "es_actual": True,
                },
                {
                    "cliente_id": 3,
                    "nombre": "Pedro",
                    "email": "pedro@example.com",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 1,
                    "es_actual": True,
                },
            ]
        )

        # Nuevos datos: Cliente 1 cambia, Cliente 2 sin cambios, Cliente 4 nuevo
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@new.com",  # CAMBIO
                },
                {
                    "cliente_id": 2,
                    "nombre": "María",
                    "email": "maria@example.com",  # SIN CAMBIO
                },
                {
                    "cliente_id": 4,
                    "nombre": "Ana",
                    "email": "ana@example.com",  # NUEVO
                },
            ]
        )

        campos_rastreables = ["email"]
        fecha_proceso = date(2024, 6, 1)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        # Cliente 1: 2 versiones (v1 cerrada + v2 nueva)
        # Cliente 2: 1 versión (sin cambios)
        # Cliente 3: 1 versión (no aparece en nuevos, se mantiene)
        # Cliente 4: 1 versión (nuevo)
        # Total: 2 + 1 + 1 + 1 = 5 registros

        assert len(df_result) == 5

        # Verificar cliente 1 tiene 2 versiones
        cliente1 = df_result[df_result["cliente_id"] == 1]
        assert len(cliente1) == 2
        assert (cliente1["version"] == [1, 2]).all()

        # Verificar cliente 4 es nuevo
        cliente4 = df_result[df_result["cliente_id"] == 4]
        assert len(cliente4) == 1
        assert cliente4.iloc[0]["version"] == 1
        assert cliente4.iloc[0]["es_actual"]

    def test_preserva_versiones_historicas(self):
        """Should preserve historical versions when processing new data."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # Cliente con 2 versiones (v1 cerrada + v2 actual)
        df_actual = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@v1.com",
                    "fecha_inicio": date(2023, 1, 1),
                    "fecha_fin": date(2024, 1, 1),
                    "version": 1,
                    "es_actual": False,  # Histórica
                },
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@v2.com",
                    "fecha_inicio": date(2024, 1, 1),
                    "fecha_fin": None,
                    "version": 2,
                    "es_actual": True,  # Actual
                },
            ]
        )

        # Datos nuevos con cambio (generará v3)
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@v3.com",  # CAMBIO
                }
            ]
        )

        campos_rastreables = ["email"]
        fecha_proceso = date(2024, 6, 1)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        # Debe tener 3 versiones: v1 histórica + v2 cerrada + v3 nueva
        assert len(df_result) == 3

        # Verificar v1 se preservó (histórica)
        v1 = df_result[df_result["version"] == 1].iloc[0]
        assert v1["fecha_fin"] == date(2024, 1, 1)
        assert not v1["es_actual"]
        assert v1["email"] == "juan@v1.com"

        # Verificar v2 se cerró
        v2 = df_result[df_result["version"] == 2].iloc[0]
        assert v2["fecha_fin"] == fecha_proceso
        assert not v2["es_actual"]

        # Verificar v3 es la actual
        v3 = df_result[df_result["version"] == 3].iloc[0]
        assert v3["es_actual"]
        assert v3["email"] == "juan@v3.com"

    def test_maneja_registro_sin_version_actual(self):
        """Should handle edge case where record exists but has no current version."""
        from src.scd_tipo2 import aplicar_scd_tipo2

        # Cliente con solo versión cerrada (sin es_actual=True)
        # Este es un caso anómalo pero el código debe manejarlo
        # IMPORTANTE: Debe preservar la versión histórica existente
        # y crear la siguiente versión, no sobrescribir
        df_actual = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@old.com",
                    "fecha_inicio": date(2023, 1, 1),
                    "fecha_fin": date(2024, 1, 1),
                    "version": 1,
                    "es_actual": False,  # No hay versión actual!
                }
            ]
        )

        # Datos nuevos para este cliente
        df_nuevos = pd.DataFrame(
            [
                {
                    "cliente_id": 1,
                    "nombre": "Juan",
                    "email": "juan@new.com",
                }
            ]
        )

        campos_rastreables = ["email"]
        fecha_proceso = date(2024, 6, 1)

        df_result = aplicar_scd_tipo2(
            df_actual, df_nuevos, "cliente_id", campos_rastreables, fecha_proceso
        )

        # Debe preservar la v1 histórica Y crear nueva v2
        assert len(df_result) == 2

        # Verificar que la versión histórica v1 se preservó
        v1_historica = df_result[df_result["version"] == 1]
        assert len(v1_historica) == 1
        assert v1_historica.iloc[0]["email"] == "juan@old.com"
        assert not v1_historica.iloc[0]["es_actual"]
        assert v1_historica.iloc[0]["fecha_fin"] == date(2024, 1, 1)

        # Verificar que se creó nueva versión 2 (siguiente a la máxima)
        v2_nueva = df_result[df_result["version"] == 2]
        assert len(v2_nueva) == 1
        assert v2_nueva.iloc[0]["email"] == "juan@new.com"
        assert v2_nueva.iloc[0]["es_actual"]
        assert v2_nueva.iloc[0]["fecha_inicio"] == fecha_proceso
        assert pd.isna(v2_nueva.iloc[0]["fecha_fin"])
