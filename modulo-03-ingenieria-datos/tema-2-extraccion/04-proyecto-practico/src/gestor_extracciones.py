"""
Módulo gestor de extracciones multi-fuente.

Orquesta extracciones de múltiples fuentes (archivos, APIs, web)
y genera reportes consolidados.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from .extractor_apis import extraer_api_completa
from .extractor_archivos import (
    leer_csv_con_encoding_auto,
    leer_excel_multiple_sheets,
    leer_json_nested,
)
from .extractor_web import extraer_html, extraer_tabla_html, parsear_con_beautifulsoup
from .validadores import validar_no_vacio

logger = logging.getLogger(__name__)


def extraer_desde_fuente(
    tipo_fuente: Literal["csv", "json", "excel", "api", "web"],
    configuracion: dict[str, Any],
) -> pd.DataFrame:
    """
    Extrae datos de una fuente específica.

    Args:
        tipo_fuente: Tipo de fuente ('csv', 'json', 'excel', 'api', 'web')
        configuracion: Dict con configuración específica de la fuente

    Returns:
        DataFrame con los datos extraídos

    Raises:
        ValueError: Si el tipo de fuente no es válido

    Examples:
        >>> df = extraer_desde_fuente('csv', {'ruta': 'datos.csv'})
    """
    logger.info(f"Extrayendo desde fuente: {tipo_fuente}")

    if tipo_fuente == "csv":
        ruta = configuracion.get("ruta")
        if not ruta:
            raise ValueError("Configuración CSV requiere 'ruta'")
        return leer_csv_con_encoding_auto(ruta, **configuracion.get("kwargs", {}))

    elif tipo_fuente == "json":
        ruta = configuracion.get("ruta")
        if not ruta:
            raise ValueError("Configuración JSON requiere 'ruta'")
        return leer_json_nested(ruta, **configuracion.get("kwargs", {}))

    elif tipo_fuente == "excel":
        ruta = configuracion.get("ruta")
        combinar = configuracion.get("combinar", True)
        if not ruta:
            raise ValueError("Configuración Excel requiere 'ruta'")
        resultado = leer_excel_multiple_sheets(ruta, combinar=combinar)
        return (
            resultado
            if isinstance(resultado, pd.DataFrame)
            else pd.concat(resultado.values())
        )

    elif tipo_fuente == "api":
        url = configuracion.get("url")
        if not url:
            raise ValueError("Configuración API requiere 'url'")
        datos = extraer_api_completa(url, **configuracion.get("kwargs", {}))
        return pd.DataFrame(datos)

    elif tipo_fuente == "web":
        url = configuracion.get("url")
        if not url:
            raise ValueError("Configuración Web requiere 'url'")
        html = extraer_html(url, **configuracion.get("kwargs", {}))
        soup = parsear_con_beautifulsoup(html)
        datos = extraer_tabla_html(soup, configuracion.get("selector"))
        return pd.DataFrame(datos)

    else:
        raise ValueError(f"Tipo de fuente no soportado: {tipo_fuente}")


def orquestar_extraccion_multiple(
    fuentes: list[dict[str, Any]], combinar: bool = False
) -> dict[str, pd.DataFrame] | pd.DataFrame:
    """
    Orquesta extracción desde múltiples fuentes.

    Args:
        fuentes: Lista de dicts con tipo y configuración de cada fuente
        combinar: Si True, combina todos los DataFrames en uno

    Returns:
        Dict con DataFrames por fuente o DataFrame combinado

    Examples:
        >>> fuentes = [
        ...     {'tipo': 'csv', 'nombre': 'ventas', 'config': {'ruta': 'ventas.csv'}},
        ...     {'tipo': 'api', 'nombre': 'usuarios', 'config': {'url': 'https://...'}}
        ... ]
        >>> resultados = orquestar_extraccion_multiple(fuentes)
    """
    resultados = {}

    for fuente in fuentes:
        nombre = fuente.get("nombre", f"fuente_{len(resultados)}")
        tipo = fuente.get("tipo")
        config = fuente.get("config", {})

        try:
            df = extraer_desde_fuente(tipo, config)
            resultados[nombre] = df
            logger.info(f"✓ Fuente '{nombre}' extraída: {len(df)} filas")
        except Exception as e:
            logger.error(f"✗ Error en fuente '{nombre}': {str(e)}")
            resultados[nombre] = pd.DataFrame()  # DataFrame vacío en caso de error

    if combinar:
        # Combinar todos los DataFrames
        dfs = [df for df in resultados.values() if not df.empty]
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()

    return resultados


def generar_reporte_extraccion(
    resultados: dict[str, pd.DataFrame], validaciones: dict[str, dict] | None = None
) -> dict[str, Any]:
    """
    Genera reporte consolidado de extracción.

    Args:
        resultados: Dict con DataFrames extraídos por fuente
        validaciones: Dict opcional con resultados de validaciones

    Returns:
        Reporte completo con estadísticas
    """
    reporte = {
        "timestamp": datetime.now().isoformat(),
        "num_fuentes": len(resultados),
        "fuentes": {},
        "totales": {"filas": 0, "columnas_unicas": set()},
    }

    for nombre, df in resultados.items():
        info_fuente = {
            "filas": len(df),
            "columnas": len(df.columns),
            "nombres_columnas": list(df.columns),
            "memoria_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "vacio": df.empty,
        }

        reporte["fuentes"][nombre] = info_fuente
        reporte["totales"]["filas"] += len(df)
        reporte["totales"]["columnas_unicas"].update(df.columns)

    reporte["totales"]["columnas_unicas"] = list(reporte["totales"]["columnas_unicas"])

    if validaciones:
        reporte["validaciones"] = validaciones

    return reporte


def guardar_resultados(
    resultados: dict[str, pd.DataFrame],
    directorio_salida: str | Path,
    formato: Literal["csv", "json", "excel"] = "csv",
) -> list[Path]:
    """
    Guarda los resultados de extracción en archivos.

    Args:
        resultados: Dict con DataFrames por fuente
        directorio_salida: Directorio donde guardar
        formato: Formato de salida ('csv', 'json', 'excel')

    Returns:
        Lista de rutas de archivos guardados
    """
    directorio = Path(directorio_salida)
    directorio.mkdir(parents=True, exist_ok=True)

    archivos_guardados = []

    for nombre, df in resultados.items():
        if df.empty:
            logger.warning(f"Saltando fuente '{nombre}' (vacía)")
            continue

        if formato == "csv":
            ruta = directorio / f"{nombre}.csv"
            df.to_csv(ruta, index=False, encoding="utf-8")
        elif formato == "json":
            ruta = directorio / f"{nombre}.json"
            df.to_json(ruta, orient="records", force_ascii=False, indent=2)
        elif formato == "excel":
            ruta = directorio / f"{nombre}.xlsx"
            df.to_excel(ruta, index=False)
        else:
            raise ValueError(f"Formato no soportado: {formato}")

        archivos_guardados.append(ruta)
        logger.info(f"Guardado: {ruta}")

    return archivos_guardados


def pipeline_completo(
    fuentes: list[dict[str, Any]],
    directorio_salida: str | Path | None = None,
    validar: bool = True,
    formato_salida: Literal["csv", "json", "excel"] = "csv",
) -> dict[str, Any]:
    """
    Pipeline completo de extracción, validación y almacenamiento.

    Args:
        fuentes: Lista de fuentes a extraer
        directorio_salida: Donde guardar (None = no guardar)
        validar: Si True, ejecuta validaciones
        formato_salida: Formato para guardar

    Returns:
        Dict con reporte completo del pipeline
    """
    logger.info(f"Iniciando pipeline con {len(fuentes)} fuentes")

    # 1. Extracción
    resultados = orquestar_extraccion_multiple(fuentes, combinar=False)

    # 2. Validación (opcional)
    validaciones = {}
    if validar:
        for nombre, df in resultados.items():
            validaciones[nombre] = {
                "vacio": validar_no_vacio(df),
                # Agregar más validaciones según necesidad
            }

    # 3. Generar reporte
    reporte = generar_reporte_extraccion(resultados, validaciones if validar else None)

    # 4. Guardar (opcional)
    if directorio_salida:
        archivos = guardar_resultados(resultados, directorio_salida, formato_salida)
        reporte["archivos_guardados"] = [str(f) for f in archivos]

    logger.info("Pipeline completado exitosamente")
    return reporte
