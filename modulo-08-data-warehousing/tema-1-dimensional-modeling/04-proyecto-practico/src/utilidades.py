"""
Módulo de utilidades y funciones helper para Data Warehouse.

Provee funciones de apoyo para:
- Logging y registro de eventos
- Formateo de números y salida
- Validación de archivos y directorios
- Medición de tiempos de ejecución
"""

import logging
import time
from contextlib import contextmanager
from pathlib import Path


def configurar_logging(
    nivel: str = "INFO", formato: str | None = None
) -> logging.Logger:
    """
    Configura el sistema de logging para la aplicación.

    Args:
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        formato: Formato personalizado para los mensajes (opcional)

    Returns:
        Logger configurado

    Examples:
        >>> logger = configurar_logging(nivel="INFO")
        >>> logger.info("Iniciando proceso")
        >>> logger = configurar_logging(nivel="DEBUG")
        >>> logger.debug("Mensaje de debug")
    """
    # Configurar formato por defecto si no se especifica
    if formato is None:
        formato = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Crear logger
    logger = logging.getLogger("data_warehouse")

    # Configurar nivel
    nivel_logging = getattr(logging, nivel.upper())
    logger.setLevel(nivel_logging)

    # Limpiar handlers existentes para evitar duplicados
    logger.handlers.clear()

    # Crear y configurar handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(nivel_logging)

    # Crear formatter y añadirlo al handler
    formatter = logging.Formatter(formato)
    console_handler.setFormatter(formatter)

    # Añadir handler al logger
    logger.addHandler(console_handler)

    return logger


def formatear_numero(numero: int | float, decimales: int = 0) -> str:
    """
    Formatea un número con separadores de miles y decimales.

    Args:
        numero: Número a formatear (int o float)
        decimales: Cantidad de decimales a mostrar (default: 0)

    Returns:
        String con número formateado

    Examples:
        >>> formatear_numero(1234567)
        '1,234,567'
        >>> formatear_numero(1234.5678, decimales=2)
        '1,234.57'
        >>> formatear_numero(1234.5678, decimales=0)
        '1,235'
    """
    if decimales == 0:
        # Para enteros, usar formato con comas
        return f"{int(round(numero)):,}"
    else:
        # Para floats, usar formato con decimales
        return f"{numero:,.{decimales}f}"


def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
    """
    Formatea un valor decimal como porcentaje.

    Args:
        valor: Valor decimal (ej: 0.1234 para 12.34%)
        decimales: Cantidad de decimales a mostrar (default: 2)

    Returns:
        String con porcentaje formateado

    Examples:
        >>> formatear_porcentaje(0.1234, decimales=2)
        '12.34%'
        >>> formatear_porcentaje(0.1234, decimales=0)
        '12%'
        >>> formatear_porcentaje(1.0, decimales=1)
        '100.0%'
    """
    porcentaje = valor * 100
    return f"{porcentaje:.{decimales}f}%"


def imprimir_tabla(
    datos: list[dict], headers: list[str], titulo: str | None = None
) -> None:
    """
    Imprime datos en formato tabla para la consola.

    Args:
        datos: Lista de diccionarios con los datos
        headers: Lista de claves a mostrar como columnas
        titulo: Título opcional para la tabla

    Examples:
        >>> datos = [
        ...     {"nombre": "Juan", "edad": 30, "ciudad": "CDMX"},
        ...     {"nombre": "María", "edad": 25, "ciudad": "GDL"}
        ... ]
        >>> imprimir_tabla(datos, headers=["nombre", "edad", "ciudad"])
        >>> imprimir_tabla(datos, headers=["nombre", "edad"], titulo="Usuarios")
    """
    if not datos:
        print("No hay datos para mostrar")
        return

    # Calcular anchos de columna
    anchos = {}
    for header in headers:
        # Ancho mínimo es el tamaño del header
        ancho_header = len(str(header))
        # Buscar el valor más largo en los datos
        ancho_datos = max((len(str(fila.get(header, ""))) for fila in datos), default=0)
        anchos[header] = max(ancho_header, ancho_datos) + 2

    # Imprimir título si existe
    if titulo:
        ancho_total = sum(anchos.values()) + len(headers) + 1
        print("\n" + "=" * ancho_total)
        print(f" {titulo}")
        print("=" * ancho_total)

    # Imprimir separador superior
    print("\n" + "-" * (sum(anchos.values()) + len(headers) + 1))

    # Imprimir headers
    header_str = "|"
    for header in headers:
        header_str += f" {str(header).ljust(anchos[header])}|"
    print(header_str)

    # Imprimir separador headers-datos
    print("-" * (sum(anchos.values()) + len(headers) + 1))

    # Imprimir filas
    for fila in datos:
        fila_str = "|"
        for header in headers:
            valor = str(fila.get(header, ""))
            fila_str += f" {valor.ljust(anchos[header])}|"
        print(fila_str)

    # Imprimir separador inferior
    print("-" * (sum(anchos.values()) + len(headers) + 1) + "\n")


def validar_archivo_existe(ruta: str) -> bool:
    """
    Valida que un archivo exista en el sistema.

    Args:
        ruta: Ruta al archivo a validar

    Returns:
        True si el archivo existe

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> validar_archivo_existe("datos.csv")  # Si existe
        True
        >>> validar_archivo_existe("inexistente.csv")  # Lanza FileNotFoundError
        Traceback (most recent call last):
        ...
        FileNotFoundError: Archivo no encontrado: inexistente.csv
    """
    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    if not archivo.is_file():
        raise ValueError(f"La ruta no es un archivo: {ruta}")

    return True


def crear_directorio_si_no_existe(ruta: str) -> None:
    """
    Crea un directorio si no existe (similar a mkdir -p).

    Args:
        ruta: Ruta del directorio a crear

    Examples:
        >>> crear_directorio_si_no_existe("output/datos")
        >>> # Crea 'output' y 'datos' si no existen
    """
    directorio = Path(ruta)
    directorio.mkdir(parents=True, exist_ok=True)


@contextmanager
def medir_tiempo(descripcion: str):
    """
    Context manager para medir tiempo de ejecución de bloques de código.

    Args:
        descripcion: Descripción de la operación a medir

    Yields:
        None

    Examples:
        >>> with medir_tiempo("Carga de datos"):
        ...     # operación costosa
        ...     time.sleep(1)
        Carga de datos: Completado en 1.00 segundos
    """
    inicio = time.time()
    try:
        yield
    finally:
        fin = time.time()
        duracion = fin - inicio

        if duracion < 1:
            print(f"{descripcion}: Completado en {duracion*1000:.2f} ms")
        else:
            print(f"{descripcion}: Completado en {duracion:.2f} segundos")
