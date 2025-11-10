"""
Generador de Dimensión de Cliente (DimCliente) con SCD Type 2.

Este módulo genera un catálogo de clientes sintéticos con campos SCD Type 2
para rastreo histórico de cambios.

Funciones:
    generar_dim_cliente: Genera catálogo de clientes con SCD Type 2
"""

import random
from datetime import date, timedelta

import pandas as pd
from faker import Faker


def generar_dim_cliente(num_clientes: int) -> pd.DataFrame:
    """
    Genera catálogo de clientes sintéticos con campos SCD Type 2.

    Args:
        num_clientes: Cantidad de clientes a generar

    Returns:
        DataFrame con DimCliente con columnas:
            - cliente_id (int): ID único del cliente
            - nombre (str): Nombre completo
            - email (str): Email único
            - telefono (str): Número telefónico
            - direccion (str): Dirección completa
            - ciudad (str): Ciudad
            - estado (str): Estado/Provincia
            - codigo_postal (str): Código postal (5 dígitos)
            - fecha_registro (date): Fecha de registro del cliente
            - segmento (str): Segmento del cliente (Premium, Regular, Nuevo)
            - fecha_inicio (date): Fecha inicio validez SCD Type 2
            - fecha_fin (date|None): Fecha fin validez SCD Type 2 (None si actual)
            - version (int): Versión del registro (1 para inicial)
            - es_actual (bool): True si es versión actual

    Raises:
        ValueError: Si num_clientes <= 0

    Examples:
        >>> clientes = generar_dim_cliente(100)
        >>> print(clientes.shape)
        (100, 14)

        >>> print(clientes['version'].unique())
        [1]

        >>> print(clientes['es_actual'].all())
        True
    """
    if num_clientes <= 0:
        raise ValueError(f"num_clientes debe ser mayor que 0. Recibido: {num_clientes}")

    fake = Faker("es_MX")
    Faker.seed(42)  # Para reproducibilidad

    clientes = []

    # Estados de México
    estados = [
        "CDMX",
        "Jalisco",
        "Nuevo León",
        "Puebla",
        "Guanajuato",
        "Veracruz",
        "Yucatán",
        "Querétaro",
        "Estado de México",
    ]

    # Ciudades por estado (simplificado)
    ciudades_por_estado = {
        "CDMX": ["Ciudad de México", "Coyoacán", "Polanco"],
        "Jalisco": ["Guadalajara", "Zapopan", "Tlaquepaque"],
        "Nuevo León": ["Monterrey", "San Pedro", "Apodaca"],
        "Puebla": ["Puebla", "Cholula"],
        "Guanajuato": ["León", "Guanajuato", "Celaya"],
        "Veracruz": ["Veracruz", "Xalapa"],
        "Yucatán": ["Mérida", "Valladolid"],
        "Querétaro": ["Querétaro", "San Juan del Río"],
        "Estado de México": ["Toluca", "Naucalpan", "Ecatepec"],
    }

    # Segmentos de clientes
    segmentos = ["Premium", "Regular", "Nuevo"]

    # Fecha de hoy para SCD Type 2
    fecha_hoy = date.today()

    cliente_id = 1

    for _ in range(num_clientes):
        # Generar datos del cliente
        nombre = fake.name()
        email = fake.email()
        telefono = fake.phone_number()
        direccion = fake.street_address()

        # Seleccionar estado y ciudad coherente
        estado = random.choice(estados)
        ciudad = random.choice(ciudades_por_estado[estado])

        # Código postal de 5 dígitos
        codigo_postal = f"{random.randint(10000, 99999)}"

        # Fecha de registro (entre 1 y 3 años atrás)
        dias_atras = random.randint(365, 1095)
        fecha_registro = fecha_hoy - timedelta(days=dias_atras)

        # Segmento del cliente
        segmento = random.choice(segmentos)

        # Campos SCD Type 2 (versión inicial)
        fecha_inicio = fecha_registro  # Inicia el día que se registró
        fecha_fin = None  # Registro actual, no tiene fecha fin
        version = 1  # Primera versión
        es_actual = True  # Es la versión actual

        clientes.append(
            {
                "cliente_id": cliente_id,
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "direccion": direccion,
                "ciudad": ciudad,
                "estado": estado,
                "codigo_postal": codigo_postal,
                "fecha_registro": fecha_registro,
                "segmento": segmento,
                # SCD Type 2 fields
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "version": version,
                "es_actual": es_actual,
            }
        )

        cliente_id += 1

    return pd.DataFrame(clientes)
