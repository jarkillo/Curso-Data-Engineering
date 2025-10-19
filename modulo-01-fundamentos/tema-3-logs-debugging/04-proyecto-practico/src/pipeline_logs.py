"""
Módulo de pipeline con logging integrado.

Este módulo proporciona funciones para procesar datos con logging
profesional integrado en cada paso del pipeline.
"""

import csv
import logging
import time
from pathlib import Path
from typing import Any, Callable, Optional


def procesar_con_logs(
    ruta_archivo: str, logger: Optional[logging.Logger] = None
) -> dict[str, Any]:
    """
    Procesa un archivo CSV con logging detallado de cada paso.

    Esta función implementa un pipeline ETL básico que:
    1. Lee un archivo CSV
    2. Valida y procesa cada registro
    3. Genera estadísticas del procesamiento
    4. Loggea cada paso con nivel apropiado

    Args:
        ruta_archivo: Ruta al archivo CSV a procesar
        logger: Logger personalizado (opcional). Si no se proporciona,
               usa logger por defecto

    Returns:
        Diccionario con estadísticas del procesamiento:
        - total_registros: Número total de registros en el archivo
        - registros_procesados: Registros procesados exitosamente
        - registros_con_error: Registros que fallaron
        - tiempo_procesamiento: Tiempo total en segundos

    Raises:
        TypeError: Si ruta_archivo no es string
        ValueError: Si ruta_archivo está vacía
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> resultado = procesar_con_logs("ventas.csv")
        >>> print(f"Procesados: {resultado['registros_procesados']}")
        Procesados: 150

        >>> # Con logger personalizado
        >>> mi_logger = logging.getLogger("mi_pipeline")
        >>> resultado = procesar_con_logs("datos.csv", logger=mi_logger)
    """
    # Validación de inputs
    if not isinstance(ruta_archivo, str):
        raise TypeError("La ruta del archivo debe ser un string")

    if not ruta_archivo or ruta_archivo.strip() == "":
        raise ValueError("La ruta del archivo no puede estar vacía")

    # Configurar logger
    if logger is None:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(handler)

    # Inicializar estadísticas
    stats = {
        "total_registros": 0,
        "registros_procesados": 0,
        "registros_con_error": 0,
        "tiempo_procesamiento": 0.0,
    }

    tiempo_inicio = time.time()

    logger.info("=" * 60)
    logger.info("Iniciando procesamiento de archivo CSV")
    logger.info(f"Archivo: {ruta_archivo}")
    logger.info("=" * 60)

    # Verificar que el archivo existe
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        logger.error(f"Archivo no encontrado: {ruta_archivo}")
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    if not ruta.is_file():
        logger.error(f"La ruta no es un archivo: {ruta_archivo}")
        raise ValueError(f"La ruta no es un archivo: {ruta_archivo}")

    try:
        # Paso 1: Leer archivo CSV
        logger.info("Paso 1: Leyendo archivo CSV...")

        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Validar que tiene headers
            if reader.fieldnames is None:
                logger.error("El archivo CSV no tiene headers")
                raise ValueError("El archivo CSV no tiene headers")

            logger.debug(f"Campos detectados: {', '.join(reader.fieldnames)}")

            # Procesar cada registro
            registros = list(reader)
            stats["total_registros"] = len(registros)

            if stats["total_registros"] == 0:
                logger.warning("El archivo CSV está vacío (solo contiene headers)")
            else:
                logger.info(
                    f"Total de registros a procesar: {stats['total_registros']}"
                )

        # Paso 2: Procesar registros
        if stats["total_registros"] > 0:
            logger.info("Paso 2: Procesando registros...")

            for idx, registro in enumerate(registros, start=1):
                try:
                    # Validar registro (ejemplo básico)
                    if not registro:
                        logger.warning(f"Registro {idx}: Vacío, se omite")
                        stats["registros_con_error"] += 1
                        continue

                    # Procesar registro (aquí iría la lógica real)
                    # Por ahora solo validamos que tenga datos
                    if all(valor == "" for valor in registro.values()):
                        logger.warning(f"Registro {idx}: Todos los campos vacíos")
                        stats["registros_con_error"] += 1
                        continue

                    # Validar campos numéricos si existen
                    for campo, valor in registro.items():
                        if campo.lower() in ["precio", "cantidad", "monto", "edad"]:
                            if valor and valor.strip():
                                try:
                                    float(valor)
                                except ValueError:
                                    logger.warning(
                                        f"Registro {idx}: Campo '{campo}' tiene valor "
                                        f"no numérico: '{valor}'"
                                    )
                                    stats["registros_con_error"] += 1
                                    break
                    else:
                        # Si no hubo break, el registro es válido
                        stats["registros_procesados"] += 1
                        logger.debug(f"Registro {idx}: Procesado exitosamente")

                except Exception as e:
                    logger.error(f"Registro {idx}: Error al procesar - {str(e)}")
                    stats["registros_con_error"] += 1

            logger.info(
                f"Procesados {stats['registros_procesados']} registros exitosamente"
            )

            if stats["registros_con_error"] > 0:
                logger.warning(
                    f"Se encontraron {stats['registros_con_error']} registros "
                    f"con errores"
                )

        # Calcular tiempo de procesamiento
        tiempo_fin = time.time()
        stats["tiempo_procesamiento"] = tiempo_fin - tiempo_inicio

        logger.info("=" * 60)
        logger.info("Procesamiento completado exitosamente")
        logger.info(
            f"Tiempo total: {stats['tiempo_procesamiento']:.2f} segundos"
        )
        logger.info(
            f"Registros procesados: {stats['registros_procesados']}/"
            f"{stats['total_registros']}"
        )
        logger.info("=" * 60)

        return stats

    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error crítico durante el procesamiento: {str(e)}")
        logger.exception("Detalles del error:")
        raise


def validar_datos_con_logs(
    datos: list[dict[str, Any]],
    campos_requeridos: Optional[list[str]] = None,
    validador_personalizado: Optional[Callable[[dict], bool]] = None,
    logger: Optional[logging.Logger] = None,
) -> dict[str, Any]:
    """
    Valida una lista de registros con logging detallado.

    Esta función valida datos según reglas predefinidas y personalizadas,
    loggeando cada problema encontrado para facilitar debugging.

    Args:
        datos: Lista de diccionarios a validar
        campos_requeridos: Lista de campos que deben estar presentes
        validador_personalizado: Función que recibe un registro y
                                 retorna True si es válido, False si no
        logger: Logger personalizado (opcional)

    Returns:
        Diccionario con resultados de validación:
        - validos: Número de registros válidos
        - invalidos: Número de registros inválidos
        - total: Total de registros
        - errores: Lista de mensajes de error
        - porcentaje_validos: Porcentaje de registros válidos

    Raises:
        TypeError: Si datos no es una lista

    Examples:
        >>> datos = [
        ...     {'id': '1', 'nombre': 'Juan', 'edad': '25'},
        ...     {'id': '2', 'nombre': 'María', 'edad': '30'},
        ... ]
        >>> resultado = validar_datos_con_logs(
        ...     datos, campos_requeridos=['id', 'nombre']
        ... )
        >>> print(f"Válidos: {resultado['validos']}/{resultado['total']}")
        Válidos: 2/2

        >>> # Con validador personalizado
        >>> def validar_edad(registro):
        ...     return int(registro.get('edad', 0)) >= 18
        >>> resultado = validar_datos_con_logs(
        ...     datos, validador_personalizado=validar_edad
        ... )
    """
    # Validación de inputs
    if not isinstance(datos, list):
        raise TypeError("Los datos deben ser una lista")

    # Configurar logger
    if logger is None:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(handler)

    # Inicializar resultados
    resultado = {
        "validos": 0,
        "invalidos": 0,
        "total": len(datos),
        "errores": [],
        "porcentaje_validos": 0.0,
    }

    logger.info("=" * 60)
    logger.info("Iniciando validación de datos")
    logger.info(f"Total de registros a validar: {resultado['total']}")
    logger.info("=" * 60)

    if resultado["total"] == 0:
        logger.warning("La lista de datos está vacía")
        return resultado

    # Validar cada registro
    for idx, registro in enumerate(datos, start=1):
        es_valido = True
        errores_registro = []

        try:
            # Validación 1: Campos requeridos
            if campos_requeridos:
                for campo in campos_requeridos:
                    if campo not in registro:
                        es_valido = False
                        error_msg = f"Registro {idx}: Falta campo requerido '{campo}'"
                        errores_registro.append(error_msg)
                        logger.warning(error_msg)
                    elif not registro[campo] or str(registro[campo]).strip() == "":
                        es_valido = False
                        error_msg = (
                            f"Registro {idx}: Campo requerido '{campo}' está vacío"
                        )
                        errores_registro.append(error_msg)
                        logger.warning(error_msg)

            # Validación 2: Campos comunes (nombre, email, edad)
            if "nombre" in registro:
                nombre = str(registro["nombre"]).strip()
                if not nombre:
                    es_valido = False
                    error_msg = f"Registro {idx}: Campo 'nombre' está vacío"
                    errores_registro.append(error_msg)
                    logger.warning(error_msg)

            if "email" in registro:
                email = str(registro["email"]).strip()
                if email and "@" not in email:
                    es_valido = False
                    error_msg = f"Registro {idx}: Email inválido '{email}'"
                    errores_registro.append(error_msg)
                    logger.warning(error_msg)

            if "edad" in registro:
                try:
                    edad = int(registro["edad"])
                    if edad < 0:
                        es_valido = False
                        error_msg = f"Registro {idx}: Edad negativa '{edad}'"
                        errores_registro.append(error_msg)
                        logger.warning(error_msg)
                except (ValueError, TypeError):
                    es_valido = False
                    error_msg = f"Registro {idx}: Edad no es un número válido"
                    errores_registro.append(error_msg)
                    logger.warning(error_msg)

            # Validación 3: Validador personalizado
            if validador_personalizado and es_valido:
                try:
                    if not validador_personalizado(registro):
                        es_valido = False
                        error_msg = f"Registro {idx}: No pasó validación personalizada"
                        errores_registro.append(error_msg)
                        logger.warning(error_msg)
                except Exception as e:
                    es_valido = False
                    error_msg = (
                        f"Registro {idx}: Error en validador personalizado - {str(e)}"
                    )
                    errores_registro.append(error_msg)
                    logger.error(error_msg)

            # Actualizar contadores
            if es_valido:
                resultado["validos"] += 1
                logger.debug(f"Registro {idx}: Válido")
            else:
                resultado["invalidos"] += 1
                resultado["errores"].extend(errores_registro)

        except Exception as e:
            resultado["invalidos"] += 1
            error_msg = f"Registro {idx}: Error inesperado - {str(e)}"
            resultado["errores"].append(error_msg)
            logger.error(error_msg)

    # Calcular porcentaje
    if resultado["total"] > 0:
        resultado["porcentaje_validos"] = (
            resultado["validos"] / resultado["total"]
        ) * 100
    else:
        resultado["porcentaje_validos"] = 0.0

    # Log final
    logger.info("=" * 60)
    logger.info("Validación completada")
    logger.info(
        f"Registros válidos: {resultado['validos']}/{resultado['total']} "
        f"({resultado['porcentaje_validos']:.1f}%)"
    )
    logger.info(f"Registros inválidos: {resultado['invalidos']}")
    logger.info("=" * 60)

    if resultado["invalidos"] > 0:
        logger.warning(f"Se encontraron {resultado['invalidos']} registros inválidos")

    return resultado
