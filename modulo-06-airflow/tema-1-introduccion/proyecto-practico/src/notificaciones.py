"""
Módulo de notificaciones

Simula el envío de notificaciones por email con resúmenes de ventas y alertas.

Nota: En producción, esto se integraría con servicios reales como:
- SendGrid
- AWS SES
- SMTP
- Slack API
"""

DESTINATARIOS_DEFAULT = [
    "equipo-ventas@cloudmart.com",
    "director-comercial@cloudmart.com",
    "data-engineering@cloudmart.com",
]


def simular_envio_email(metricas: dict, anomalia: dict) -> dict:
    """
    Simula el envío de un email con el resumen de ventas.

    Args:
        metricas: Dict con métricas de ventas
        anomalia: Dict con resultado de detección de anomalías

    Returns:
        dict: Email simulado con estructura:
            {
                "asunto": str,
                "cuerpo": str,
                "destinatarios": list,
                "estado": str
            }

    Examples:
        >>> metricas = {"fecha": "2025-10-25", "total_ventas": 1250.50}
        >>> anomalia = {"anomalia": False}
        >>> email = simular_envio_email(metricas, anomalia)
        >>> email["estado"]
        'simulado'
    """
    fecha = metricas.get("fecha", "N/A")
    total_ventas = metricas.get("total_ventas", 0.0)

    # Determinar si es alerta o reporte normal
    es_alerta = anomalia.get("anomalia", False)

    # Construir asunto
    if es_alerta:
        asunto = f"🚨 ALERTA: Caída en Ventas - {fecha}"
    else:
        asunto = f"📊 Reporte Diario de Ventas - {fecha}"

    # Construir cuerpo del email
    cuerpo = []
    cuerpo.append("Hola equipo,\n")
    cuerpo.append(f"Aquí está el resumen de ventas para el día {fecha}:\n")
    cuerpo.append("=" * 60)
    cuerpo.append("\nMÉTRICAS PRINCIPALES:")
    cuerpo.append(f"  • Total de Ventas: ${total_ventas:,.2f}")

    if "ticket_promedio" in metricas:
        cuerpo.append(f"  • Ticket Promedio: ${metricas['ticket_promedio']:,.2f}")

    if "cantidad_ventas" in metricas:
        cuerpo.append(f"  • Cantidad de Ventas: {metricas['cantidad_ventas']}")

    # Añadir top productos si existen
    if "top_productos" in metricas and metricas["top_productos"]:
        cuerpo.append("\nTOP 3 PRODUCTOS:")
        for i, prod in enumerate(metricas["top_productos"][:3], 1):
            cuerpo.append(f"  {i}. {prod['producto']}: {prod['cantidad']} unidades")

    # Añadir alerta si existe
    if es_alerta:
        cuerpo.append("\n" + "=" * 60)
        cuerpo.append("\n⚠️  ALERTA DE ANOMALÍA:")
        porcentaje = anomalia.get("porcentaje_caida", 0) * 100
        cuerpo.append(f"Se detectó una caída del {porcentaje:.1f}% en las ventas.")
        cuerpo.append("Se recomienda revisar las causas inmediatamente.")
        cuerpo.append("\nPosibles causas a investigar:")
        cuerpo.append("  - Problemas técnicos en la plataforma")
        cuerpo.append("  - Cambios en la competencia")
        cuerpo.append("  - Falta de inventario")
        cuerpo.append("  - Problemas de marketing/publicidad")

    cuerpo.append("\n" + "=" * 60)
    cuerpo.append("\nSaludos,")
    cuerpo.append("Sistema Automático de Reportes - CloudMart")
    cuerpo.append("\nEste es un email automático generado por Apache Airflow.")

    # Construir email simulado
    email = {
        "asunto": asunto,
        "cuerpo": "\n".join(cuerpo),
        "destinatarios": DESTINATARIOS_DEFAULT,
        "estado": "simulado",  # En producción sería "enviado" o "fallido"
        "timestamp": metricas.get("fecha", "N/A"),
    }

    # Log de simulación
    print(f"\n{'=' * 60}")
    print("📧 SIMULACIÓN DE ENVÍO DE EMAIL")
    print(f"{'=' * 60}")
    print(f"Asunto: {email['asunto']}")
    print(f"Destinatarios: {len(email['destinatarios'])} personas")
    print(f"Estado: {email['estado']}")
    print(f"{'=' * 60}\n")

    return email
