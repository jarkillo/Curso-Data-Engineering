"""
Módulo de notificaciones.

Este módulo proporciona funciones para simular el envío de notificaciones
por email y guardar logs de ejecución.
"""

from datetime import datetime
from pathlib import Path


def simular_notificacion_gerente(total: float, cliente_top: str) -> None:
    """
    Simula el envío de un email al gerente con métricas clave.

    En un entorno real, esto enviaría un email usando EmailOperator o similar.

    Args:
        total: Total de ventas del periodo
        cliente_top: ID del cliente con más ventas

    Examples:
        >>> simular_notificacion_gerente(6500.0, "C001")
        [NOTIFICACIÓN] 📧 Enviando email al gerente...
    """
    print("[NOTIFICACIÓN] 📧 Enviando email al gerente...")
    print("[NOTIFICACIÓN] Asunto: Alerta - Ventas elevadas detectadas")
    print(f"[NOTIFICACIÓN] Total de ventas: {total:.2f}€")
    print(f"[NOTIFICACIÓN] Cliente top: {cliente_top}")
    print("[NOTIFICACIÓN] ✅ Email simulado enviado")


def guardar_log_ejecucion(mensaje: str, ruta: str) -> None:
    """
    Guarda un mensaje en un archivo de log.

    Crea el directorio padre si no existe.
    Añade timestamp al mensaje.

    Args:
        mensaje: Mensaje a guardar en el log
        ruta: Ruta donde guardar el archivo de log

    Examples:
        >>> guardar_log_ejecucion("Pipeline completado", "/tmp/ejecucion.log")
    """
    ruta_path = Path(ruta)

    # Crear directorio padre si no existe
    ruta_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_con_timestamp = f"[{timestamp}] {mensaje}\n"

    with open(ruta_path, "a", encoding="utf-8") as f:
        f.write(mensaje_con_timestamp)

    print(f"[LOG] Guardado en: {ruta}")
