"""
Módulo de configuración para el pipeline ETL en AWS.

Este módulo centraliza la configuración del proyecto leyendo variables
de entorno desde un archivo .env.
"""

from pathlib import Path


def cargar_configuracion(ruta_env: str | None = None) -> dict[str, str]:
    """
    Carga la configuración desde variables de entorno.

    Lee el archivo .env y retorna un diccionario con todas las configuraciones
    necesarias para el pipeline AWS.

    Args:
        ruta_env: Ruta opcional al archivo .env. Si no se proporciona,
                  busca .env en el directorio raíz del proyecto.

    Returns:
        Diccionario con configuraciones cargadas:
        - aws_access_key_id: Access key de AWS
        - aws_secret_access_key: Secret key de AWS
        - aws_region: Región AWS (ej: us-east-1)
        - s3_bucket_raw: Nombre del bucket S3 para datos raw
        - s3_bucket_processed: Nombre del bucket S3 para datos procesados
        - lambda_function_name: Nombre de la función Lambda
        - glue_database: Nombre de la base de datos Glue
        - athena_output_location: Ubicación de resultados Athena

    Raises:
        FileNotFoundError: Si el archivo .env no existe
        ValueError: Si faltan variables de entorno requeridas

    Examples:
        >>> config = cargar_configuracion()
        >>> config['aws_region']
        'us-east-1'
        >>> config['s3_bucket_raw']
        'cloudapi-logs-raw'
    """
    # Determinar ruta del archivo .env
    if ruta_env is None:
        ruta_proyecto = obtener_ruta_proyecto()
        ruta_env_path = ruta_proyecto / ".env"
    else:
        ruta_env_path = Path(ruta_env)

    # Verificar que el archivo existe
    if not ruta_env_path.exists():
        raise FileNotFoundError(f"Archivo .env no encontrado en: {ruta_env_path}")

    # Leer y parsear el archivo .env
    config: dict[str, str] = {}
    with open(ruta_env_path, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            # Ignorar líneas vacías y comentarios
            if not linea or linea.startswith("#"):
                continue

            # Parsear línea KEY=VALUE
            if "=" in linea:
                key, value = linea.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Mapear nombres de variables de .env a nombres internos
                mapeo = {
                    "AWS_ACCESS_KEY_ID": "aws_access_key_id",
                    "AWS_SECRET_ACCESS_KEY": "aws_secret_access_key",
                    "AWS_DEFAULT_REGION": "aws_region",
                    "S3_BUCKET_RAW": "s3_bucket_raw",
                    "S3_BUCKET_PROCESSED": "s3_bucket_processed",
                    "LAMBDA_FUNCTION_NAME": "lambda_function_name",
                    "GLUE_DATABASE": "glue_database",
                    "ATHENA_OUTPUT_LOCATION": "athena_output_location",
                }

                if key in mapeo:
                    config[mapeo[key]] = value

    return config


def validar_configuracion(config: dict[str, str]) -> tuple[bool, list[str]]:
    """
    Valida que la configuración tenga todas las claves requeridas.

    Args:
        config: Diccionario con configuración

    Returns:
        Tupla (es_valida, errores):
        - es_valida: True si la configuración es válida
        - errores: Lista de mensajes de error (vacía si es válida)

    Examples:
        >>> config = {'aws_region': 'us-east-1'}
        >>> valida, errores = validar_configuracion(config)
        >>> valida
        False
        >>> 'aws_access_key_id' in errores[0]
        True
    """
    campos_requeridos = [
        "aws_access_key_id",
        "aws_secret_access_key",
        "aws_region",
        "s3_bucket_raw",
        "s3_bucket_processed",
    ]

    errores: list[str] = []

    # Verificar campos faltantes
    for campo in campos_requeridos:
        if campo not in config:
            errores.append(f"Campo requerido faltante: {campo}")
        elif not config[campo] or config[campo].strip() == "":
            errores.append(f"Campo requerido vacío: {campo}")

    # Validar formato de región AWS (básico)
    if "aws_region" in config and config["aws_region"]:
        region = config["aws_region"]
        # Regiones válidas típicamente tienen formato: us-east-1, eu-west-2, etc.
        if not ("-" in region and len(region) >= 9):
            errores.append(
                f"Región AWS tiene formato inválido: {region}. "
                f"Ejemplo válido: us-east-1"
            )

    es_valida = len(errores) == 0
    return es_valida, errores


def obtener_ruta_proyecto() -> Path:
    """
    Obtiene la ruta absoluta del directorio raíz del proyecto.

    Returns:
        Path object con la ruta del proyecto

    Examples:
        >>> ruta = obtener_ruta_proyecto()
        >>> ruta.name
        '04-proyecto-practico'
    """
    # Obtener la ruta del archivo actual (config.py)
    ruta_actual = Path(__file__).resolve()

    # Subir dos niveles: config.py -> src/ -> 04-proyecto-practico/
    ruta_proyecto = ruta_actual.parent.parent

    return ruta_proyecto


def obtener_ruta_datos(tipo: str = "raw") -> Path:
    """
    Obtiene la ruta al directorio de datos (raw o processed).

    Args:
        tipo: 'raw' o 'processed'

    Returns:
        Path object con la ruta al directorio de datos

    Raises:
        ValueError: Si tipo no es 'raw' ni 'processed'

    Examples:
        >>> ruta = obtener_ruta_datos("raw")
        >>> str(ruta).endswith("data/raw")
        True
    """
    # Normalizar tipo a lowercase
    tipo_lower = tipo.lower()

    if tipo_lower not in ["raw", "processed"]:
        raise ValueError(
            f"Tipo de datos inválido: '{tipo}'. Debe ser 'raw' o 'processed'"
        )

    ruta_proyecto = obtener_ruta_proyecto()
    ruta_datos = ruta_proyecto / "data" / tipo_lower

    return ruta_datos
