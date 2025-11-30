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


def generar_dim_cliente_con_historial(
    num_clientes: int, porcentaje_con_historial: int = 30
) -> pd.DataFrame:
    """
    Genera catalogo de clientes con historial SCD Type 2 real.

    A diferencia de generar_dim_cliente, esta funcion genera clientes donde
    un porcentaje de ellos tiene multiples versiones (cambios historicos),
    simulando cambios reales de direccion, ciudad, estado o segmento.

    Args:
        num_clientes: Cantidad de clientes unicos a generar
        porcentaje_con_historial: Porcentaje de clientes con historial (0-100)

    Returns:
        DataFrame con DimCliente incluyendo versiones historicas

    Raises:
        ValueError: Si num_clientes <= 0
        ValueError: Si porcentaje_con_historial no esta entre 0 y 100

    Examples:
        >>> clientes = generar_dim_cliente_con_historial(100, porcentaje_con_historial=30)
        >>> print(clientes["cliente_id"].nunique())
        100

        >>> # Habra mas de 100 registros debido al historial
        >>> print(len(clientes) > 100)
        True
    """
    if num_clientes <= 0:
        raise ValueError(f"num_clientes debe ser mayor que 0. Recibido: {num_clientes}")

    if not 0 <= porcentaje_con_historial <= 100:
        raise ValueError(
            f"porcentaje_con_historial debe estar entre 0 y 100. "
            f"Recibido: {porcentaje_con_historial}"
        )

    # Generar clientes base (version 1)
    clientes_base = generar_dim_cliente(num_clientes)

    # Si no hay historial, retornar directamente
    if porcentaje_con_historial == 0:
        return clientes_base

    # Determinar cuantos clientes tendran historial
    num_con_historial = int(num_clientes * porcentaje_con_historial / 100)

    # Seleccionar clientes que tendran historial (aleatoriamente)
    random.seed(42)  # Reproducibilidad
    indices_con_historial = random.sample(range(num_clientes), num_con_historial)

    # Estados y ciudades para generar cambios
    estados = [
        "CDMX",
        "Jalisco",
        "Nuevo Leon",
        "Puebla",
        "Guanajuato",
        "Veracruz",
        "Yucatan",
        "Queretaro",
        "Estado de Mexico",
    ]

    ciudades_por_estado = {
        "CDMX": ["Ciudad de Mexico", "Coyoacan", "Polanco"],
        "Jalisco": ["Guadalajara", "Zapopan", "Tlaquepaque"],
        "Nuevo Leon": ["Monterrey", "San Pedro", "Apodaca"],
        "Puebla": ["Puebla", "Cholula"],
        "Guanajuato": ["Leon", "Guanajuato", "Celaya"],
        "Veracruz": ["Veracruz", "Xalapa"],
        "Yucatan": ["Merida", "Valladolid"],
        "Queretaro": ["Queretaro", "San Juan del Rio"],
        "Estado de Mexico": ["Toluca", "Naucalpan", "Ecatepec"],
    }

    segmentos = ["Premium", "Regular", "Nuevo"]

    fake = Faker("es_MX")
    Faker.seed(43)  # Semilla diferente para variacion

    registros_finales = []
    fecha_hoy = date.today()

    for idx, row in clientes_base.iterrows():
        cliente_dict = row.to_dict()

        if idx in indices_con_historial:
            # Este cliente tendra historial
            num_versiones_extra = random.randint(1, 3)

            fecha_registro = cliente_dict["fecha_registro"]
            dias_desde_registro = (fecha_hoy - fecha_registro).days

            if dias_desde_registro <= num_versiones_extra:
                num_versiones_extra = max(1, dias_desde_registro - 1)

            intervalo = dias_desde_registro // (num_versiones_extra + 1)
            fechas_cambio = []
            for i in range(1, num_versiones_extra + 1):
                dias = intervalo * i + random.randint(0, max(1, intervalo // 2))
                fecha_cambio = fecha_registro + timedelta(
                    days=min(dias, dias_desde_registro - 1)
                )
                fechas_cambio.append(fecha_cambio)

            fechas_cambio.sort()

            version_actual = cliente_dict.copy()
            version_num = 1

            for fecha_cambio in fechas_cambio:
                version_cerrada = version_actual.copy()
                version_cerrada["fecha_fin"] = fecha_cambio
                version_cerrada["es_actual"] = False
                version_cerrada["version"] = version_num
                registros_finales.append(version_cerrada)

                version_num += 1
                version_actual = version_actual.copy()
                version_actual["version"] = version_num
                version_actual["fecha_inicio"] = fecha_cambio
                version_actual["fecha_fin"] = None
                version_actual["es_actual"] = True

                tipo_cambio = random.choice(["direccion", "ubicacion", "segmento"])

                if tipo_cambio == "direccion":
                    version_actual["direccion"] = fake.street_address()
                    version_actual["codigo_postal"] = f"{random.randint(10000, 99999)}"
                elif tipo_cambio == "ubicacion":
                    nuevo_estado = random.choice(
                        [e for e in estados if e != version_actual["estado"]]
                    )
                    version_actual["estado"] = nuevo_estado
                    version_actual["ciudad"] = random.choice(
                        ciudades_por_estado[nuevo_estado]
                    )
                    version_actual["direccion"] = fake.street_address()
                    version_actual["codigo_postal"] = f"{random.randint(10000, 99999)}"
                else:
                    version_actual["segmento"] = random.choice(
                        [s for s in segmentos if s != version_actual["segmento"]]
                    )

            registros_finales.append(version_actual)
        else:
            registros_finales.append(cliente_dict)

    return pd.DataFrame(registros_finales)
