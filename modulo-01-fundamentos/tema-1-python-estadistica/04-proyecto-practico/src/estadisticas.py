"""
Módulo de estadísticas básicas.

Este módulo proporciona funciones para calcular estadísticas descriptivas
de conjuntos de datos numéricos.

Todas las funciones siguen estos principios:
- Tipado explícito para claridad y detección de errores
- Validación exhaustiva de inputs para seguridad
- Funciones puras sin efectos secundarios
- Docstrings completos con ejemplos
- Manejo explícito de errores con excepciones específicas

Autor: Master en Ingeniería de Datos con IA
Fecha: 2025
"""

from typing import List, Union, Dict
from collections import Counter
import math


def calcular_media(datos: List[Union[int, float]]) -> float:
    """
    Calcula la media aritmética (promedio) de una lista de números.

    La media aritmética es la suma de todos los valores dividida por
    la cantidad de valores. Es una medida de tendencia central que
    representa el valor "promedio" del conjunto de datos.

    Fórmula: media = (suma de todos los valores) / (cantidad de valores)

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números (enteros o decimales) de la cual calcular la media.
        No puede estar vacía.

    Retorna
    -------
    float
        La media aritmética de los datos.

    Lanza
    -----
    TypeError
        Si datos no es una lista o contiene elementos no numéricos.
    ValueError
        Si la lista está vacía.

    Ejemplos
    --------
    >>> calcular_media([1, 2, 3, 4, 5])
    3.0

    >>> calcular_media([10.5, 20.5, 30.5])
    20.5

    >>> calcular_media([-5, 0, 5])
    0.0

    Ejemplo real - Ventas diarias de un restaurante:
    >>> ventas_diarias = [150.50, 180.75, 200.00, 165.25]
    >>> calcular_media(ventas_diarias)
    174.125

    Notas de Seguridad
    ------------------
    - Valida que el input sea una lista
    - Valida que todos los elementos sean números
    - Valida que la lista no esté vacía
    - No modifica la lista original (función pura)
    """
    # Validación 1: Verificar que sea una lista
    if not isinstance(datos, list):
        raise TypeError(
            "Los datos deben ser una lista. " f"Se recibió: {type(datos).__name__}"
        )

    # Validación 2: Verificar que la lista no esté vacía
    if len(datos) == 0:
        raise ValueError(
            "La lista de datos no puede estar vacía. "
            "Se necesita al menos un valor para calcular la media."
        )

    # Validación 3: Verificar que todos los elementos sean números
    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"El elemento en la posición {i} es de tipo "
                f"{type(valor).__name__}: {valor}"
            )
        # Validación adicional: None se considera como bool en algunos contextos
        if valor is None:
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"Se encontró None en la posición {i}"
            )

    # Cálculo de la media
    suma_total = sum(datos)
    cantidad = len(datos)
    media = suma_total / cantidad

    return float(media)


def calcular_mediana(datos: List[Union[int, float]]) -> float:
    """
    Calcula la mediana de una lista de números.

    La mediana es el valor que separa la mitad superior de la mitad inferior
    de un conjunto de datos ordenado. Es más robusta que la media ante valores
    extremos (outliers).

    - Si la cantidad de elementos es impar: la mediana es el valor central
    - Si la cantidad de elementos es par: la mediana es el promedio de los
      dos valores centrales

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números de la cual calcular la mediana.
        No puede estar vacía.

    Retorna
    -------
    float
        La mediana de los datos.

    Lanza
    -----
    TypeError
        Si datos no es una lista o contiene elementos no numéricos.
    ValueError
        Si la lista está vacía.

    Ejemplos
    --------
    >>> calcular_mediana([1, 2, 3, 4, 5])
    3.0

    >>> calcular_mediana([1, 2, 3, 4])
    2.5

    >>> calcular_mediana([5, 1, 3, 2, 4])  # Lista desordenada
    3.0

    Ejemplo real - Tiempos de respuesta de API (ms):
    La mediana es mejor que la media para tiempos de respuesta
    porque no se ve afectada por outliers.

    >>> tiempos = [10, 12, 15, 18, 20, 25, 500]  # 500ms es un outlier
    >>> calcular_mediana(tiempos)
    18.0

    >>> calcular_media(tiempos)  # La media se ve muy afectada
    85.71...

    Notas de Seguridad
    ------------------
    - Valida que el input sea una lista
    - Valida que todos los elementos sean números
    - Valida que la lista no esté vacía
    - No modifica la lista original (crea una copia para ordenar)
    """
    # Validación 1: Verificar que sea una lista
    if not isinstance(datos, list):
        raise TypeError(
            "Los datos deben ser una lista. " f"Se recibió: {type(datos).__name__}"
        )

    # Validación 2: Verificar que la lista no esté vacía
    if len(datos) == 0:
        raise ValueError(
            "La lista de datos no puede estar vacía. "
            "Se necesita al menos un valor para calcular la mediana."
        )

    # Validación 3: Verificar que todos los elementos sean números
    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"El elemento en la posición {i} es de tipo "
                f"{type(valor).__name__}: {valor}"
            )
        if valor is None:
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"Se encontró None en la posición {i}"
            )

    # Ordenar la lista (hacer una copia para no modificar la original)
    datos_ordenados = sorted(datos)
    cantidad = len(datos_ordenados)

    # Calcular la mediana
    if cantidad % 2 == 1:
        # Cantidad impar: tomar el elemento del medio
        indice_medio = cantidad // 2
        mediana = datos_ordenados[indice_medio]
    else:
        # Cantidad par: promediar los dos elementos del medio
        indice_medio_superior = cantidad // 2
        indice_medio_inferior = indice_medio_superior - 1
        mediana = (
            datos_ordenados[indice_medio_inferior]
            + datos_ordenados[indice_medio_superior]
        ) / 2

    return float(mediana)


def calcular_moda(datos: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Calcula la moda (valor o valores más frecuentes) de una lista de números.

    La moda es el valor que aparece con mayor frecuencia en un conjunto de datos.
    Puede haber una moda (unimodal), varias modas (bimodal, multimodal) o ninguna
    moda dominante (cuando todos los valores aparecen la misma cantidad de veces).

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números de la cual calcular la moda.
        No puede estar vacía.

    Retorna
    -------
    List[Union[int, float]]
        Lista con el valor o valores que aparecen más frecuentemente.
        Si todos los valores aparecen la misma cantidad de veces, devuelve todos.

    Lanza
    -----
    TypeError
        Si datos no es una lista o contiene elementos no numéricos.
    ValueError
        Si la lista está vacía.

    Ejemplos
    --------
    >>> calcular_moda([1, 2, 2, 2, 3, 4])
    [2]

    >>> calcular_moda([1, 1, 2, 2, 3])  # Bimodal
    [1, 2]

    >>> calcular_moda([1, 2, 3, 4])  # Todos únicos
    [1, 2, 3, 4]

    Ejemplo real - Productos más vendidos en Yurest:
    >>> ids_productos = [101, 102, 101, 103, 101, 102, 104]
    >>> calcular_moda(ids_productos)
    [101]

    Notas
    -----
    - Devuelve siempre una lista, incluso si hay una sola moda
    - Preserva el tipo original (int o float)
    """
    # Validaciones (igual que las otras funciones)
    if not isinstance(datos, list):
        raise TypeError(
            "Los datos deben ser una lista. " f"Se recibió: {type(datos).__name__}"
        )

    if len(datos) == 0:
        raise ValueError(
            "La lista de datos no puede estar vacía. "
            "Se necesita al menos un valor para calcular la moda."
        )

    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"El elemento en la posición {i} es de tipo "
                f"{type(valor).__name__}: {valor}"
            )
        if valor is None:
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"Se encontró None en la posición {i}"
            )

    # Contar frecuencias
    contador = Counter(datos)
    max_frecuencia = max(contador.values())

    # Encontrar todos los valores con la frecuencia máxima
    modas = [
        valor for valor, frecuencia in contador.items() if frecuencia == max_frecuencia
    ]

    # Ordenar para consistencia en los resultados
    modas_ordenadas = sorted(modas)

    return modas_ordenadas


def calcular_varianza(datos: List[Union[int, float]]) -> float:
    """
    Calcula la varianza poblacional de una lista de números.

    La varianza mide qué tan dispersos están los datos respecto a la media.
    Es el promedio de las diferencias al cuadrado entre cada valor y la media.

    Fórmula: varianza = Σ(xi - media)² / N

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números de la cual calcular la varianza.
        No puede estar vacía.

    Retorna
    -------
    float
        La varianza poblacional de los datos.

    Lanza
    -----
    TypeError
        Si datos no es una lista o contiene elementos no numéricos.
    ValueError
        Si la lista está vacía.

    Ejemplos
    --------
    >>> calcular_varianza([2, 4, 4, 4, 5, 5, 7, 9])
    4.0

    >>> calcular_varianza([5, 5, 5, 5])  # Sin variación
    0.0

    Notas
    -----
    - Se calcula la varianza poblacional (divisor N)
    - Para varianza muestral, se usaría (N-1) como divisor
    - La varianza está en unidades al cuadrado
    """
    # Validaciones (reutilizando la lógica)
    if not isinstance(datos, list):
        raise TypeError(
            "Los datos deben ser una lista. " f"Se recibió: {type(datos).__name__}"
        )

    if len(datos) == 0:
        raise ValueError("La lista de datos no puede estar vacía.")

    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"El elemento en la posición {i} es de tipo {type(valor).__name__}"
            )
        if valor is None:
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"Se encontró None en la posición {i}"
            )

    # Calcular la media
    media = calcular_media(datos)

    # Calcular suma de diferencias al cuadrado
    suma_diferencias_cuadrado = sum((x - media) ** 2 for x in datos)

    # Varianza poblacional
    varianza = suma_diferencias_cuadrado / len(datos)

    return float(varianza)


def calcular_desviacion_estandar(datos: List[Union[int, float]]) -> float:
    """
    Calcula la desviación estándar de una lista de números.

    La desviación estándar es la raíz cuadrada de la varianza.
    Mide la dispersión de los datos en las mismas unidades que los datos originales,
    lo que la hace más interpretable que la varianza.

    Fórmula: desviación_estándar = √(varianza)

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números de la cual calcular la desviación estándar.
        No puede estar vacía.

    Retorna
    -------
    float
        La desviación estándar de los datos.

    Lanza
    -----
    TypeError
        Si datos no es una lista o contiene elementos no numéricos.
    ValueError
        Si la lista está vacía.

    Ejemplos
    --------
    >>> calcular_desviacion_estandar([2, 4, 4, 4, 5, 5, 7, 9])
    2.0

    >>> calcular_desviacion_estandar([5, 5, 5, 5])  # Sin variación
    0.0

    Ejemplo real - Volatilidad de ventas:
    >>> ventas_estables = [100, 102, 98, 101, 99]
    >>> ventas_volatiles = [50, 150, 75, 125, 100]
    >>> calcular_desviacion_estandar(ventas_estables)  # Baja desviación
    1.41...
    >>> calcular_desviacion_estandar(ventas_volatiles)  # Alta desviación
    35.35...

    Notas
    -----
    - Está en las mismas unidades que los datos originales
    - Más fácil de interpretar que la varianza
    - Útil para medir volatilidad, riesgo, consistencia
    """
    # Calcular varianza (que ya hace todas las validaciones)
    varianza = calcular_varianza(datos)

    # Desviación estándar es la raíz cuadrada de la varianza
    desviacion = math.sqrt(varianza)

    return float(desviacion)


def calcular_percentiles(
    datos: List[Union[int, float]], percentiles: List[int]
) -> Dict[int, float]:
    """
    Calcula percentiles específicos de una lista de números.

    Los percentiles dividen un conjunto de datos ordenado en 100 partes iguales.
    El percentil P indica que el P% de los datos son menores o iguales a ese valor.

    Percentiles comunes:
    - P25 (Q1): Primer cuartil, 25% de los datos están por debajo
    - P50 (Q2): Mediana, 50% de los datos están por debajo
    - P75 (Q3): Tercer cuartil, 75% de los datos están por debajo
    - P95: 95% de los datos están por debajo (común para SLAs)

    Parámetros
    ----------
    datos : List[Union[int, float]]
        Lista de números de la cual calcular los percentiles.
        No puede estar vacía.
    percentiles : List[int]
        Lista de percentiles a calcular (valores entre 0 y 100).

    Retorna
    -------
    Dict[int, float]
        Diccionario donde las claves son los percentiles solicitados
        y los valores son los valores correspondientes en los datos.

    Lanza
    -----
    TypeError
        Si datos o percentiles no son listas, o contienen tipos incorrectos.
    ValueError
        Si la lista de datos está vacía o los percentiles están fuera de rango [0, 100].

    Ejemplos
    --------
    >>> datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> calcular_percentiles(datos, [25, 50, 75])
    {25: 3.25, 50: 5.5, 75: 7.75}

    Ejemplo real - SLA de tiempos de respuesta:
    En Agora/Yurest, queremos que el 95% de las peticiones respondan
    en menos de 100ms.

    >>> tiempos_ms = [10, 12, 15, 18, 20, 22, 25, 30, 35, 200]
    >>> resultado = calcular_percentiles(tiempos_ms, [50, 95, 99])
    >>> resultado[95]  # P95 debe ser < 100ms para cumplir SLA
    47.5

    Notas
    -----
    - Usa interpolación lineal para valores intermedios
    - Los datos se ordenan internamente sin modificar la lista original
    """
    # Validación de datos
    if not isinstance(datos, list):
        raise TypeError(
            "Los datos deben ser una lista. " f"Se recibió: {type(datos).__name__}"
        )

    if len(datos) == 0:
        raise ValueError("La lista de datos no puede estar vacía.")

    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"El elemento en la posición {i} es de tipo {type(valor).__name__}"
            )
        if valor is None:
            raise TypeError(
                f"Todos los elementos deben ser números. "
                f"Se encontró None en la posición {i}"
            )

    # Validación de percentiles
    if not isinstance(percentiles, list):
        raise TypeError(
            "Los percentiles deben ser una lista. "
            f"Se recibió: {type(percentiles).__name__}"
        )

    for i, p in enumerate(percentiles):
        if not isinstance(p, int):
            raise TypeError(
                f"Todos los percentiles deben ser enteros. "
                f"El percentil en la posición {i} es de tipo {type(p).__name__}"
            )
        if not 0 <= p <= 100:
            raise ValueError(
                f"Los percentiles deben estar entre 0 y 100. " f"Se recibió: {p}"
            )

    # Ordenar datos (sin modificar original)
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)

    resultados = {}

    for p in percentiles:
        # Calcular la posición del percentil
        # Usamos interpolación lineal (método más común)
        if p == 0:
            resultados[p] = float(datos_ordenados[0])
        elif p == 100:
            resultados[p] = float(datos_ordenados[-1])
        else:
            # Fórmula: posición = (percentil / 100) * (n - 1)
            posicion = (p / 100) * (n - 1)
            indice_inferior = int(posicion)
            indice_superior = indice_inferior + 1

            if indice_superior >= n:
                resultados[p] = float(datos_ordenados[-1])
            else:
                # Interpolación lineal
                fraccion = posicion - indice_inferior
                valor_inferior = datos_ordenados[indice_inferior]
                valor_superior = datos_ordenados[indice_superior]
                valor_percentil = valor_inferior + fraccion * (
                    valor_superior - valor_inferior
                )
                resultados[p] = float(valor_percentil)

    return resultados
