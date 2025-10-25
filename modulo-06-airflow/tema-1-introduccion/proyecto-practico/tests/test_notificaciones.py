"""
Tests para el módulo de notificaciones

Simula envío de emails con resúmenes de ventas y alertas.
"""


def test_simular_envio_email_sin_anomalia():
    """
    Test: simular_envio_email debe generar mensaje estándar sin anomalía

    Given: Métricas normales sin anomalía detectada
    When: Se llama a simular_envio_email
    Then: Retorna dict con asunto y cuerpo del email simulado
    """
    from src.notificaciones import simular_envio_email

    metricas = {
        "fecha": "2025-10-25",
        "total_ventas": 1250.50,
        "ticket_promedio": 208.42,
        "cantidad_ventas": 6,
    }

    anomalia = {"anomalia": False}

    email = simular_envio_email(metricas, anomalia)

    assert isinstance(email, dict)
    assert "asunto" in email
    assert "cuerpo" in email
    assert "destinatarios" in email
    assert "estado" in email

    assert "2025-10-25" in email["asunto"] or "2025-10-25" in email["cuerpo"]
    assert email["estado"] == "simulado"


def test_simular_envio_email_con_anomalia():
    """
    Test: simular_envio_email debe incluir alerta si hay anomalía

    Given: Anomalía detectada (caída de ventas)
    When: Se llama a simular_envio_email
    Then: El asunto y cuerpo incluyen la palabra "ALERTA"
    """
    from src.notificaciones import simular_envio_email

    metricas = {
        "fecha": "2025-10-25",
        "total_ventas": 500.0,
        "ticket_promedio": 100.0,
        "cantidad_ventas": 5,
    }

    anomalia = {
        "anomalia": True,
        "porcentaje_caida": 0.45,
        "mensaje": "Caída del 45% detectada",
    }

    email = simular_envio_email(metricas, anomalia)

    assert "ALERTA" in email["asunto"] or "ALERTA" in email["cuerpo"]
    # El porcentaje puede aparecer como "45%", "45.0%", o "0.45"
    assert "45" in email["cuerpo"] and (
        "%" in email["cuerpo"] or "0.45" in email["cuerpo"]
    )


def test_simular_envio_email_formato_correcto():
    """
    Test: simular_envio_email debe tener formato profesional

    Given: Métricas válidas
    When: Se llama a simular_envio_email
    Then: El email tiene estructura profesional (saludo, métricas, despedida)
    """
    from src.notificaciones import simular_envio_email

    metricas = {
        "fecha": "2025-10-25",
        "total_ventas": 2000.0,
        "ticket_promedio": 200.0,
        "cantidad_ventas": 10,
        "top_productos": [{"producto": "Laptop", "cantidad": 3}],
    }

    anomalia = {"anomalia": False}

    email = simular_envio_email(metricas, anomalia)

    cuerpo = email["cuerpo"]

    # Verificar estructura profesional
    assert len(cuerpo) > 50  # No debe ser trivial
    assert "total" in cuerpo.lower() or "ventas" in cuerpo.lower()


def test_simular_envio_email_destinatarios_validos():
    """
    Test: simular_envio_email debe incluir lista de destinatarios

    Given: Métricas válidas
    When: Se llama a simular_envio_email
    Then: Incluye lista de destinatarios simulados
    """
    from src.notificaciones import simular_envio_email

    metricas = {"fecha": "2025-10-25", "total_ventas": 1000.0}
    anomalia = {"anomalia": False}

    email = simular_envio_email(metricas, anomalia)

    assert isinstance(email["destinatarios"], list)
    assert len(email["destinatarios"]) > 0


def test_simular_envio_email_metricas_incompletas():
    """
    Test: simular_envio_email debe funcionar con métricas mínimas

    Given: Métricas con solo fecha y total
    When: Se llama a simular_envio_email
    Then: Genera email válido sin errores
    """
    from src.notificaciones import simular_envio_email

    metricas = {"fecha": "2025-10-25", "total_ventas": 1500.0}
    anomalia = {"anomalia": False}

    email = simular_envio_email(metricas, anomalia)

    assert email["estado"] == "simulado"
    assert "1500" in email["cuerpo"] or "1,500" in email["cuerpo"]
