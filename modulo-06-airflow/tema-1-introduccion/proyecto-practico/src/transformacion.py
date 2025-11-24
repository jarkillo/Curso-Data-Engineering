"""
Módulo de transformación de datos

Funciones para calcular métricas de ventas.

Métricas calculadas:
- Total de ventas
- Ticket promedio
- Cantidad de ventas
- Top N productos más vendidos
"""

import pandas as pd


def calcular_ticket_promedio(df: pd.DataFrame) -> float:
    """
    Calcula el ticket promedio (promedio de la columna total).

    Args:
        df: DataFrame con columna "total"

    Returns:
        float: Ticket promedio

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({"total": [100.0, 200.0, 300.0]})
        >>> calcular_ticket_promedio(df)
        200.0
    """
    if df.empty or "total" not in df.columns:
        raise ValueError("El DataFrame está vacío o no tiene la columna 'total'")

    promedio = df["total"].mean()

    return float(promedio)


def obtener_top_productos(df: pd.DataFrame, n: int = 5) -> list[dict]:
    """
    Obtiene los N productos más vendidos ordenados por cantidad.

    Args:
        df: DataFrame con columnas "producto" y "cantidad"
        n: Número de productos a retornar (default: 5)

    Returns:
        list: Lista de dicts con formato [{"producto": str, "cantidad": int}, ...]

    Examples:
        >>> df = pd.DataFrame({"producto": ["A", "B"], "cantidad": [10, 20]})
        >>> obtener_top_productos(df, n=1)
        [{"producto": "B", "cantidad": 20}]
    """
    if df.empty:
        return []

    # Agrupar por producto y sumar cantidades
    df_agrupado = df.groupby("producto", as_index=False)["cantidad"].sum()

    # Ordenar por cantidad descendente
    df_ordenado = df_agrupado.sort_values("cantidad", ascending=False)

    # Tomar los top N
    top_n = df_ordenado.head(n)

    # Convertir a lista de dicts
    resultado = top_n.to_dict(orient="records")

    return resultado


def calcular_metricas_ventas(df: pd.DataFrame) -> dict:
    """
    Calcula todas las métricas de ventas.

    Args:
        df: DataFrame de ventas completo

    Returns:
        dict: Métricas con estructura:
            {
                "total_ventas": float,
                "ticket_promedio": float,
                "cantidad_ventas": int,
                "top_productos": list
            }

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({...})
        >>> metricas = calcular_metricas_ventas(df)
        >>> metricas["total_ventas"]
        1250.50
    """
    if df.empty:
        raise ValueError("El DataFrame está vacío. No se pueden calcular métricas.")

    # Calcular total de ventas
    total_ventas = float(df["total"].sum())

    # Calcular ticket promedio
    ticket_promedio = calcular_ticket_promedio(df)

    # Cantidad de ventas
    cantidad_ventas = len(df)

    # Top 5 productos
    top_productos = obtener_top_productos(df, n=5)

    # Construir dict de métricas
    metricas = {
        "total_ventas": total_ventas,
        "ticket_promedio": ticket_promedio,
        "cantidad_ventas": cantidad_ventas,
        "top_productos": top_productos,
    }

    print("📊 Métricas calculadas:")
    print(f"  - Total de ventas: ${total_ventas:,.2f}")
    print(f"  - Ticket promedio: ${ticket_promedio:,.2f}")
    print(f"  - Cantidad de ventas: {cantidad_ventas}")
    print(
        f"  - Top producto: {top_productos[0]['producto'] if top_productos else 'N/A'}"
    )

    return metricas
