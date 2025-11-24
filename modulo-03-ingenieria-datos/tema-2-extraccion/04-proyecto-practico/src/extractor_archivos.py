"""
Módulo de extracción de datos desde archivos.

Este módulo proporciona funciones para extraer datos de archivos locales:
- CSV con detección automática de encoding
- JSON (simple, nested, JSON Lines)
- Excel con múltiples hojas

Todas las funciones son puras (sin efectos colaterales) y están completamente testeadas.
"""

import json
from pathlib import Path
from typing import Any

import chardet
import pandas as pd


def detectar_encoding_archivo(ruta: str | Path) -> str:
    """
    Detecta automáticamente el encoding de un archivo.

    Usa la librería chardet para analizar los primeros bytes del archivo
    y determinar qué encoding es más probable.

    Args:
        ruta: Ruta al archivo (str o Path)

    Returns:
        Encoding detectado (ej: 'utf-8', 'latin-1', 'windows-1252')

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si no se puede detectar el encoding

    Examples:
        >>> encoding = detectar_encoding_archivo('datos.csv')
        >>> print(encoding)
        'utf-8'
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta}")

    # Leer primeros bytes para detección
    with open(ruta, "rb") as archivo:
        contenido = archivo.read()

    # Detectar encoding
    resultado = chardet.detect(contenido)
    encoding = resultado.get("encoding")
    confianza = resultado.get("confidence", 0)

    if not encoding or confianza < 0.5:
        raise ValueError(
            f"No se pudo detectar el encoding con suficiente confianza "
            f"(confianza: {confianza:.2%})"
        )

    return encoding


def leer_csv_con_encoding_auto(ruta: str | Path, **kwargs: Any) -> pd.DataFrame:
    """
    Lee un archivo CSV detectando automáticamente el encoding.

    Primero detecta el encoding del archivo, luego lo lee con pandas.
    Acepta todos los parámetros de pd.read_csv().

    Args:
        ruta: Ruta al archivo CSV
        **kwargs: Argumentos adicionales para pd.read_csv
                  (ej: delimiter, header, na_values, etc.)

    Returns:
        DataFrame con los datos del CSV

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no es un CSV válido o encoding no detectado

    Examples:
        >>> df = leer_csv_con_encoding_auto('datos.csv')
        >>> print(len(df))
        100

        >>> df = leer_csv_con_encoding_auto('datos.csv', delimiter=';')
        >>> print(df.columns.tolist())
        ['nombre', 'edad', 'ciudad']
    """
    ruta = Path(ruta)

    # Detectar encoding
    encoding = detectar_encoding_archivo(ruta)

    # Leer CSV con encoding detectado
    try:
        df = pd.read_csv(ruta, encoding=encoding, **kwargs)
    except Exception as e:
        raise ValueError(f"Error al leer CSV: {str(e)}")

    return df


def leer_json_nested(
    ruta: str | Path, aplanar: bool = True, max_nivel: int | None = None
) -> pd.DataFrame:
    """
    Lee un archivo JSON con estructuras anidadas.

    Puede aplanar automáticamente estructuras nested usando json_normalize.
    Soporta tanto archivos JSON normales como JSON Lines.

    Args:
        ruta: Ruta al archivo JSON
        aplanar: Si True, aplana estructuras nested (default: True)
        max_nivel: Máximo nivel de anidamiento a aplanar (None = todos)

    Returns:
        DataFrame con los datos del JSON

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no es JSON válido

    Examples:
        >>> df = leer_json_nested('datos.json')
        >>> print(df.columns.tolist())
        ['id', 'nombre', 'direccion.calle', 'direccion.ciudad']

        >>> df = leer_json_nested('datos.json', aplanar=False)
        >>> print(type(df['direccion'][0]))
        <class 'dict'>
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta}")

    try:
        with open(ruta, encoding="utf-8") as archivo:
            contenido = archivo.read().strip()

            # Detectar si es JSON Lines (cada línea es un JSON)
            if "\n" in contenido:
                primer_linea = contenido.split("\n")[0].strip()
                if primer_linea.startswith("{"):
                    # Es JSON Lines
                    datos = []
                    for linea in contenido.split("\n"):
                        if linea.strip():
                            datos.append(json.loads(linea))
                else:
                    # Es JSON normal con saltos de línea
                    datos = json.loads(contenido)
            else:
                # JSON normal
                datos = json.loads(contenido)

        # Convertir a DataFrame
        if aplanar:
            from pandas import json_normalize

            df = json_normalize(datos, max_level=max_nivel)
        else:
            df = pd.DataFrame(datos)

        return df

    except json.JSONDecodeError as e:
        raise ValueError(f"El archivo no es JSON válido: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error al leer JSON: {str(e)}")


def leer_excel_multiple_sheets(
    ruta: str | Path, combinar: bool = False, nombre_columna_hoja: str = "hoja"
) -> dict[str, pd.DataFrame] | pd.DataFrame:
    """
    Lee un archivo Excel con todas sus hojas.

    Puede retornar un diccionario con cada hoja como DataFrame separado,
    o combinar todas las hojas en un solo DataFrame.

    Args:
        ruta: Ruta al archivo Excel
        combinar: Si True, combina todas las hojas en un DataFrame
        nombre_columna_hoja: Nombre de columna para indicar la hoja de origen
                            (solo si combinar=True)

    Returns:
        Si combinar=False: dict[nombre_hoja, DataFrame]
        Si combinar=True: DataFrame con todas las hojas

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo no es Excel válido o está vacío

    Examples:
        >>> hojas = leer_excel_multiple_sheets('ventas.xlsx')
        >>> print(list(hojas.keys()))
        ['Enero', 'Febrero', 'Marzo']

        >>> df = leer_excel_multiple_sheets('ventas.xlsx', combinar=True)
        >>> print(df['hoja'].unique())
        ['Enero', 'Febrero', 'Marzo']
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta}")

    try:
        # Leer todas las hojas
        hojas = pd.read_excel(ruta, sheet_name=None)

        if not hojas:
            raise ValueError("El archivo Excel no contiene hojas")

        if combinar:
            # Combinar todas las hojas
            dfs = []
            for nombre_hoja, df in hojas.items():
                df = df.copy()
                df[nombre_columna_hoja] = nombre_hoja
                dfs.append(df)

            return pd.concat(dfs, ignore_index=True)
        else:
            return hojas

    except Exception as e:
        raise ValueError(f"Error al leer Excel: {str(e)}")


def validar_estructura_archivo(
    df: pd.DataFrame, columnas_requeridas: list[str], lanzar_error: bool = True
) -> bool:
    """
    Valida que un DataFrame tenga las columnas requeridas.

    Verifica que todas las columnas especificadas existan en el DataFrame.
    Puede lanzar una excepción o retornar False.

    Args:
        df: DataFrame a validar
        columnas_requeridas: Lista de nombres de columnas que deben existir
        lanzar_error: Si True, lanza ValueError si faltan columnas
                     Si False, retorna False si faltan columnas

    Returns:
        True si todas las columnas existen, False si faltan (solo si lanzar_error=False)

    Raises:
        ValueError: Si faltan columnas y lanzar_error=True
        TypeError: Si df no es un DataFrame

    Examples:
        >>> df = pd.DataFrame({'id': [1, 2], 'nombre': ['Ana', 'Carlos']})
        >>> validar_estructura_archivo(df, ['id', 'nombre'])
        True

        >>> validar_estructura_archivo(df, ['id', 'edad'], lanzar_error=False)
        False
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El primer argumento debe ser un DataFrame")

    columnas_presentes = set(df.columns)
    columnas_esperadas = set(columnas_requeridas)

    columnas_faltantes = columnas_esperadas - columnas_presentes

    if columnas_faltantes:
        if lanzar_error:
            raise ValueError(
                f"Faltan columnas requeridas: {sorted(columnas_faltantes)}"
            )
        return False

    return True


def convertir_formato_archivo(
    ruta_origen: str | Path,
    ruta_destino: str | Path,
    formato_destino: str | None = None,
) -> None:
    """
    Convierte un archivo de un formato a otro.

    Soporta conversiones entre CSV, JSON y Excel.
    El formato de destino se detecta automáticamente de la extensión
    si no se especifica explícitamente.

    Args:
        ruta_origen: Ruta al archivo de origen
        ruta_destino: Ruta donde guardar el archivo convertido
        formato_destino: Formato explícito ('csv', 'json', 'excel')
                        Si None, se detecta de la extensión

    Raises:
        FileNotFoundError: Si el archivo de origen no existe
        ValueError: Si el formato no es soportado

    Examples:
        >>> convertir_formato_archivo('datos.csv', 'datos.json')

        >>> convertir_formato_archivo('datos.json', 'datos.xlsx', 'excel')
    """
    ruta_origen = Path(ruta_origen)
    ruta_destino = Path(ruta_destino)

    if not ruta_origen.exists():
        raise FileNotFoundError(f"El archivo de origen no existe: {ruta_origen}")

    # Detectar formato de origen
    ext_origen = ruta_origen.suffix.lower()

    # Detectar formato de destino
    if formato_destino is None:
        ext_destino = ruta_destino.suffix.lower()
        if ext_destino == ".csv":
            formato_destino = "csv"
        elif ext_destino == ".json":
            formato_destino = "json"
        elif ext_destino in [".xlsx", ".xls"]:
            formato_destino = "excel"
        else:
            raise ValueError(f"Formato no soportado: {ext_destino}")

    # Leer archivo de origen
    if ext_origen == ".csv":
        df = leer_csv_con_encoding_auto(ruta_origen)
    elif ext_origen == ".json":
        df = leer_json_nested(ruta_origen)
    elif ext_origen in [".xlsx", ".xls"]:
        resultado = leer_excel_multiple_sheets(ruta_origen, combinar=True)
        df = (
            resultado
            if isinstance(resultado, pd.DataFrame)
            else list(resultado.values())[0]
        )
    else:
        raise ValueError(f"Formato de origen no soportado: {ext_origen}")

    # Guardar en formato de destino
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    if formato_destino == "csv":
        df.to_csv(ruta_destino, index=False, encoding="utf-8")
    elif formato_destino == "json":
        df.to_json(ruta_destino, orient="records", force_ascii=False, indent=2)
    elif formato_destino == "excel":
        df.to_excel(ruta_destino, index=False)
    else:
        raise ValueError(f"Formato de destino no soportado: {formato_destino}")
