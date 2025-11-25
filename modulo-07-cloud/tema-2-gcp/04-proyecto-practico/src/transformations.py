"""
Módulo para transformaciones ETL de registros de pacientes.

Contiene funciones para limpiar, normalizar y enriquecer datos
de pacientes en el sistema HealthTech Analytics.
"""

from datetime import datetime
from typing import Any


def limpiar_nulls(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Elimina registros con nulls en campos críticos.

    Campos críticos: paciente_id, nombre, edad, diagnostico

    Args:
        datos: Lista de registros de pacientes

    Returns:
        Lista de registros sin nulls en campos críticos

    Examples:
        >>> datos = [
        ...     {"paciente_id": "P001", "nombre": "Juan", "edad": 45, "diagnostico": "Diabetes"},
        ...     {"paciente_id": None, "nombre": "María", "edad": 32, "diagnostico": "Hipertensión"}
        ... ]
        >>> limpios = limpiar_nulls(datos)
        >>> len(limpios)
        1
        >>> limpios[0]["paciente_id"]
        'P001'
    """
    campos_criticos = ["paciente_id", "nombre", "edad", "diagnostico"]

    resultado = []

    for registro in datos:
        # Verificar que todos los campos críticos existan y no sean None
        es_valido = all(
            campo in registro and registro[campo] is not None
            for campo in campos_criticos
        )

        if es_valido:
            # Copiar para no modificar original
            resultado.append(registro.copy())

    return resultado


def normalizar_fechas(datos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Normaliza fechas al formato ISO 8601 (YYYY-MM-DD).

    Args:
        datos: Lista de registros con campo 'fecha_registro'

    Returns:
        Lista de registros con fechas normalizadas

    Examples:
        >>> datos = [{"paciente_id": "P001", "fecha_registro": "15/01/2025"}]
        >>> normalizados = normalizar_fechas(datos)
        >>> normalizados[0]["fecha_registro"]
        '2025-01-15'
    """
    resultado = []

    for registro in datos:
        nuevo_registro = registro.copy()

        if "fecha_registro" in registro and registro["fecha_registro"]:
            fecha_str = registro["fecha_registro"]

            # Intentar parsear diferentes formatos
            formatos = [
                "%Y-%m-%d",  # 2025-01-15 (ya normalizado)
                "%d/%m/%Y",  # 15/01/2025
                "%m/%d/%Y",  # 01/15/2025
                "%Y/%m/%d",  # 2025/01/15
            ]

            fecha_obj = None
            for formato in formatos:
                try:
                    fecha_obj = datetime.strptime(fecha_str, formato)
                    break
                except ValueError:
                    continue

            if fecha_obj:
                # Convertir a formato ISO 8601
                nuevo_registro["fecha_registro"] = fecha_obj.strftime("%Y-%m-%d")

        resultado.append(nuevo_registro)

    return resultado


def calcular_edad_desde_fecha_nacimiento(fecha_nacimiento: str) -> int | None:
    """
    Calcula la edad actual desde una fecha de nacimiento.

    Args:
        fecha_nacimiento: Fecha de nacimiento en formato YYYY-MM-DD

    Returns:
        Edad en años, o None si la fecha es inválida

    Examples:
        >>> # Nota: Este test depende de la fecha actual
        >>> edad = calcular_edad_desde_fecha_nacimiento("1980-01-15")
        >>> edad is not None
        True
        >>> edad >= 40  # Asumiendo año >= 2020
        True
    """
    try:
        fecha_nac_obj = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        hoy = datetime.now()

        # Calcular edad
        edad = hoy.year - fecha_nac_obj.year

        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
            edad -= 1

        return edad

    except (ValueError, AttributeError):
        return None


def categorizar_por_edad(edad: int) -> str:
    """
    Categoriza a un paciente por rango de edad.

    Categorías:
    - "niño": 0-17 años
    - "adulto": 18-64 años
    - "mayor": 65+ años

    Args:
        edad: Edad del paciente

    Returns:
        Categoría de edad

    Examples:
        >>> categorizar_por_edad(10)
        'niño'
        >>> categorizar_por_edad(45)
        'adulto'
        >>> categorizar_por_edad(70)
        'mayor'
    """
    if edad < 18:
        return "niño"
    elif edad < 65:
        return "adulto"
    else:
        return "mayor"


def categorizar_nivel_riesgo(registro: dict[str, Any]) -> str:
    """
    Categoriza el nivel de riesgo de un paciente.

    Criterios:
    - ALTO: Edad 65+ Y (Diabetes O Hipertensión)
    - MEDIO: Edad 40+ Y (Diabetes O Hipertensión) O Edad 65+ sin condiciones críticas
    - BAJO: Resto

    Args:
        registro: Registro del paciente con campos edad y diagnostico

    Returns:
        Nivel de riesgo: "bajo", "medio", "alto"

    Examples:
        >>> registro = {"edad": 70, "diagnostico": "Diabetes"}
        >>> categorizar_nivel_riesgo(registro)
        'alto'

        >>> registro = {"edad": 25, "diagnostico": "Chequeo general"}
        >>> categorizar_nivel_riesgo(registro)
        'bajo'
    """
    edad = registro.get("edad", 0)
    diagnostico = registro.get("diagnostico", "").lower()

    # Condiciones críticas
    condiciones_criticas = ["diabetes", "hipertensión", "hipertension"]
    tiene_condicion_critica = any(
        condicion in diagnostico for condicion in condiciones_criticas
    )

    # Evaluar riesgo
    if edad >= 65 and tiene_condicion_critica:
        return "alto"
    elif (edad >= 40 and tiene_condicion_critica) or (edad >= 65):
        return "medio"
    else:
        return "bajo"


def enriquecer_registro(registro: dict[str, Any]) -> dict[str, Any]:
    """
    Enriquece un registro con campos calculados.

    Campos agregados:
    - categoria_edad: Categoría por edad
    - nivel_riesgo: Nivel de riesgo médico
    - fecha_procesamiento: Timestamp de procesamiento

    Args:
        registro: Registro original del paciente

    Returns:
        Registro enriquecido con campos adicionales

    Examples:
        >>> registro = {
        ...     "paciente_id": "P001",
        ...     "nombre": "Juan Pérez",
        ...     "edad": 45,
        ...     "diagnostico": "Diabetes"
        ... }
        >>> enriquecido = enriquecer_registro(registro)
        >>> "categoria_edad" in enriquecido
        True
        >>> "nivel_riesgo" in enriquecido
        True
        >>> enriquecido["categoria_edad"]
        'adulto'
    """
    # Copiar registro original para no modificarlo
    enriquecido = registro.copy()

    # Agregar categoría de edad
    if "edad" in registro:
        enriquecido["categoria_edad"] = categorizar_por_edad(registro["edad"])

    # Agregar nivel de riesgo
    enriquecido["nivel_riesgo"] = categorizar_nivel_riesgo(registro)

    # Agregar timestamp de procesamiento
    enriquecido["fecha_procesamiento"] = datetime.utcnow().isoformat() + "Z"

    return enriquecido
