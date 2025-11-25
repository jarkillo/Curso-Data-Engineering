"""
Módulo para validar registros de pacientes.

Contiene funciones de validación para cada campo de un registro
de paciente en el sistema HealthTech Analytics.
"""

from datetime import datetime
from typing import Any


def validar_paciente_id(paciente_id: str) -> tuple[bool, str]:
    """
    Valida el formato del ID de paciente.

    Formato esperado: P seguido de números (ej: P001, P1234)

    Args:
        paciente_id: ID del paciente a validar

    Returns:
        Tupla (es_valido, mensaje_error)
        - es_valido: True si es válido, False si no
        - mensaje_error: Descripción del error si es inválido, "" si es válido

    Examples:
        >>> validar_paciente_id("P001")
        (True, '')
        >>> validar_paciente_id("invalid")
        (False, 'ID debe empezar con P mayúscula seguido de números')
        >>> validar_paciente_id("")
        (False, 'ID de paciente es requerido')
    """
    # Validar que no sea vacío
    if not paciente_id or not paciente_id.strip():
        return False, "ID de paciente es requerido"

    # Validar formato: P + números
    if not paciente_id.startswith("P"):
        return False, "ID debe empezar con P mayúscula seguido de números"

    # Verificar que después de P solo haya números
    resto = paciente_id[1:]
    if not resto:
        return False, "ID debe empezar con P mayúscula seguido de números"

    if not resto.isdigit():
        return False, "ID debe empezar con P mayúscula seguido de números"

    return True, ""


def validar_edad(edad: Any) -> tuple[bool, str]:
    """
    Valida que la edad sea un entero válido.

    Args:
        edad: Edad a validar (puede ser cualquier tipo)

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> validar_edad(25)
        (True, '')
        >>> validar_edad(-1)
        (False, 'Edad no puede ser negativa')
        >>> validar_edad(125)
        (False, 'Edad no puede ser mayor a 120 años')
        >>> validar_edad("25")
        (True, '')
    """
    # Validar que no sea None
    if edad is None:
        return False, "Edad es requerida"

    # Intentar convertir a int si es string
    if isinstance(edad, str):
        try:
            edad = int(edad)
        except ValueError:
            return False, "Edad debe ser un número entero válido"

    # Validar que sea int
    if not isinstance(edad, int):
        return False, "Edad debe ser un número entero"

    # Validar rango
    if edad < 0:
        return False, "Edad no puede ser negativa"

    if edad > 120:
        return False, "Edad no puede ser mayor a 120 años"

    return True, ""


def validar_diagnostico(diagnostico: str) -> tuple[bool, str]:
    """
    Valida que el diagnóstico sea válido.

    Args:
        diagnostico: Diagnóstico a validar

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> validar_diagnostico("Diabetes")
        (True, '')
        >>> validar_diagnostico("")
        (False, 'Diagnóstico es requerido')
        >>> validar_diagnostico("AB")
        (False, 'Diagnóstico debe tener al menos 3 caracteres')
    """
    # Validar que no sea None
    if diagnostico is None:
        return False, "Diagnóstico es requerido"

    # Validar que no sea vacío
    if not diagnostico or not diagnostico.strip():
        return False, "Diagnóstico es requerido"

    # Validar longitud mínima
    if len(diagnostico.strip()) < 3:
        return False, "Diagnostico debe tener al menos 3 caracteres (minimo)"

    return True, ""


def validar_fecha_nacimiento(fecha_str: str) -> tuple[bool, str]:
    """
    Valida que la fecha de nacimiento sea válida.

    Formato esperado: YYYY-MM-DD (ISO 8601)

    Args:
        fecha_str: Fecha como string

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> validar_fecha_nacimiento("1990-01-15")
        (True, '')
        >>> validar_fecha_nacimiento("15-01-1990")
        (False, 'Fecha debe estar en formato YYYY-MM-DD')
        >>> validar_fecha_nacimiento("2099-01-15")
        (False, 'Fecha de nacimiento no puede ser futura')
    """
    # Validar que no sea None o vacío
    if not fecha_str:
        return False, "Fecha de nacimiento es requerida"

    # Intentar parsear fecha
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return False, "Fecha debe estar en formato YYYY-MM-DD o es inválida"

    # Validar que no sea futura
    if fecha.date() > datetime.now().date():
        return False, "Fecha de nacimiento no puede ser futura"

    return True, ""


def validar_registro_completo(registro: dict[str, Any]) -> tuple[bool, str]:
    """
    Valida que un registro de paciente sea completo y válido.

    Campos requeridos:
    - paciente_id
    - nombre
    - edad
    - diagnostico

    Campos opcionales:
    - fecha_nacimiento

    Args:
        registro: Diccionario con datos del paciente

    Returns:
        Tupla (es_valido, mensaje_error)

    Examples:
        >>> registro = {
        ...     "paciente_id": "P001",
        ...     "nombre": "Juan Pérez",
        ...     "edad": 45,
        ...     "diagnostico": "Diabetes"
        ... }
        >>> validar_registro_completo(registro)
        (True, '')

        >>> registro_invalido = {"paciente_id": "invalid"}
        >>> validar_registro_completo(registro_invalido)
        (False, 'Campo requerido: nombre')
    """
    # Validar campos requeridos
    campos_requeridos = ["paciente_id", "nombre", "edad", "diagnostico"]

    for campo in campos_requeridos:
        if campo not in registro:
            return False, f"Campo requerido: {campo}"

    # Validar paciente_id
    es_valido, mensaje = validar_paciente_id(registro["paciente_id"])
    if not es_valido:
        return False, f"Error en paciente_id: {mensaje}"

    # Validar nombre
    if not registro["nombre"] or not str(registro["nombre"]).strip():
        return False, "Error en nombre: Nombre es requerido"

    # Validar edad
    es_valido, mensaje = validar_edad(registro["edad"])
    if not es_valido:
        return False, f"Error en edad: {mensaje}"

    # Validar diagnostico
    es_valido, mensaje = validar_diagnostico(registro["diagnostico"])
    if not es_valido:
        return False, f"Error en diagnostico: {mensaje}"

    # Validar fecha_nacimiento si existe
    if "fecha_nacimiento" in registro and registro["fecha_nacimiento"]:
        es_valido, mensaje = validar_fecha_nacimiento(registro["fecha_nacimiento"])
        if not es_valido:
            return False, f"Error en fecha_nacimiento: {mensaje}"

    return True, ""
