"""
Generador de dimensión DimVendedor para Data Warehouse.

Este módulo genera datos sintéticos para la tabla de dimensión de vendedores
con estructura jerárquica (supervisores y gerentes regionales).
"""

import random

import pandas as pd

try:
    from faker import Faker

    FAKER_DISPONIBLE = True
except ImportError:
    FAKER_DISPONIBLE = False


def generar_dim_vendedor(num_vendedores: int) -> pd.DataFrame:
    """
    Genera datos sintéticos para la dimensión DimVendedor.

    Crea un DataFrame con información de vendedores incluyendo datos personales,
    región asignada, estructura jerárquica (supervisores) y comisión.

    Args:
        num_vendedores: Número de vendedores a generar (debe ser > 0)

    Returns:
        DataFrame con columnas:
        - vendedor_id (int): ID único del vendedor (PK)
        - nombre (str): Nombre completo
        - email (str): Correo electrónico corporativo
        - telefono (str): Teléfono de contacto
        - region (str): Región asignada (Norte/Sur/Centro/Este/Oeste)
        - comision_porcentaje (float): % de comisión sobre ventas (0-20)
        - supervisor_id (int): ID del supervisor (NULL para gerentes)
        - gerente_regional (str): Nombre del gerente regional

    Raises:
        ValueError: Si num_vendedores <= 0
        ImportError: Si Faker no está instalado (con mensaje instructivo)

    Examples:
        >>> df = generar_dim_vendedor(100)
        >>> df.shape
        (100, 8)
        >>> df['vendedor_id'].is_unique
        True
        >>> df['region'].unique()
        array(['Norte', 'Sur', 'Centro', 'Este', 'Oeste'], dtype=object)
    """
    # Validación de entrada
    if num_vendedores <= 0:
        raise ValueError("num_vendedores debe ser positivo")

    if not FAKER_DISPONIBLE:
        raise ImportError(
            "Faker no está instalado. "
            "Instalar con: pip install faker\n"
            "Este módulo requiere Faker para generar datos sintéticos realistas."
        )

    # Configurar generador de datos sintéticos
    fake = Faker(["es_MX", "es_ES"])
    random.seed(42)  # Para reproducibilidad en contexto educativo
    Faker.seed(42)

    # Regiones disponibles
    regiones = ["Norte", "Sur", "Centro", "Este", "Oeste"]

    # Determinar estructura jerárquica (20% gerentes, 80% vendedores con supervisor)
    num_gerentes = max(1, int(num_vendedores * 0.2))

    vendedores = []

    # FASE 1: Crear gerentes (sin supervisor)
    gerentes_ids = []
    gerentes_nombres = {}

    for i in range(1, num_gerentes + 1):
        nombre = fake.name()
        region = random.choice(regiones)

        vendedor = {
            "vendedor_id": i,
            "nombre": nombre,
            "email": generar_email_corporativo(nombre, region),
            "telefono": fake.phone_number(),
            "region": region,
            "comision_porcentaje": round(random.uniform(5.0, 10.0), 2),
            "supervisor_id": None,  # Gerentes no tienen supervisor
            "gerente_regional": nombre,  # Los gerentes son su propio gerente regional
        }

        vendedores.append(vendedor)
        gerentes_ids.append(i)
        gerentes_nombres[region] = nombre

    # FASE 2: Crear vendedores con supervisor
    for i in range(num_gerentes + 1, num_vendedores + 1):
        nombre = fake.name()
        region = random.choice(regiones)

        # Asignar supervisor aleatorio de los gerentes ya creados
        supervisor_id = random.choice(gerentes_ids)

        # Obtener gerente regional de la región asignada
        gerente_regional = gerentes_nombres.get(
            region, random.choice(list(gerentes_nombres.values()))
        )

        vendedor = {
            "vendedor_id": i,
            "nombre": nombre,
            "email": generar_email_corporativo(nombre, region),
            "telefono": fake.phone_number(),
            "region": region,
            "comision_porcentaje": round(random.uniform(2.0, 15.0), 2),
            "supervisor_id": supervisor_id,
            "gerente_regional": gerente_regional,
        }

        vendedores.append(vendedor)

    # Crear DataFrame
    df = pd.DataFrame(vendedores)

    # Asegurar tipos de datos correctos
    df["vendedor_id"] = df["vendedor_id"].astype(int)
    df["comision_porcentaje"] = df["comision_porcentaje"].astype(float)
    # supervisor_id puede tener NaN, pandas lo maneja como float

    return df


def generar_email_corporativo(nombre: str, region: str) -> str:
    """
    Genera email corporativo basado en nombre y región.

    Args:
        nombre: Nombre completo de la persona
        region: Región de la empresa

    Returns:
        Email en formato: nombre.apellido@ventasglobal.com

    Examples:
        >>> generar_email_corporativo("Juan Pérez", "Norte")
        'juan.perez@ventasglobal.com'
    """
    # Convertir a minúsculas y quitar acentos
    nombre_limpio = (
        nombre.lower()
        .replace(" ", ".")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )

    return f"{nombre_limpio}@ventasglobal.com"
