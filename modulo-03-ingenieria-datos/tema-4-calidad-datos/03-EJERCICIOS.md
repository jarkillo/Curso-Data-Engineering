# Ejercicios Prácticos: Calidad de Datos

**Objetivo**: Practicar técnicas de calidad de datos en ejercicios progresivos.

**Instrucciones**:
- Intenta resolver cada ejercicio sin mirar la solución
- Prueba tu código con diferentes casos
- Compara tu solución con la proporcionada
- Los ejercicios están ordenados por dificultad (⭐ fácil → ⭐⭐⭐ difícil)

---

## 📋 Índice de Ejercicios

### Básicos (⭐)
1. [Validación de Tipos de Datos](#ejercicio-1-validación-de-tipos-de-datos-)
2. [Detección de Duplicados Exactos](#ejercicio-2-detección-de-duplicados-exactos-)
3. [Identificación de Outliers con IQR](#ejercicio-3-identificación-de-outliers-con-iqr-)
4. [Cálculo de Completitud](#ejercicio-4-cálculo-de-completitud-)
5. [Validación de Rangos](#ejercicio-5-validación-de-rangos-)

### Intermedios (⭐⭐)
6. [Validación de Esquema con Pandera](#ejercicio-6-validación-de-esquema-con-pandera-)
7. [Fuzzy Matching de Nombres](#ejercicio-7-fuzzy-matching-de-nombres-)
8. [Detección de Outliers Multivariada](#ejercicio-8-detección-de-outliers-multivariada-)
9. [Perfil de Calidad Personalizado](#ejercicio-9-perfil-de-calidad-personalizado-)
10. [Consolidación de Duplicados](#ejercicio-10-consolidación-de-duplicados-)

### Avanzados (⭐⭐⭐)
11. [Pipeline de Calidad Completo](#ejercicio-11-pipeline-de-calidad-completo-)
12. [Sistema de Alertas de Calidad](#ejercicio-12-sistema-de-alertas-de-calidad-)
13. [Validación Cross-Field](#ejercicio-13-validación-cross-field-)
14. [Framework de Calidad Reutilizable](#ejercicio-14-framework-de-calidad-reutilizable-)
15. [Monitoreo Temporal de Calidad](#ejercicio-15-monitoreo-temporal-de-calidad-)

---

## Ejercicio 1: Validación de Tipos de Datos ⭐

### Enunciado

Crea una función que valide que todas las columnas de un DataFrame tienen los tipos de datos esperados según un diccionario de especificación.

### Datos de Entrada

```python
import pandas as pd

df = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'nombre': ['Ana', 'Luis', 'Pedro', 'María', 'Juan'],
    'edad': [25, 30, '28', 35, 40],  # '28' es string
    'salario': [3000.0, 3500.0, 3200.0, 4000.0, 3800.0],
    'activo': [True, False, True, True, 1]  # 1 debería ser bool
})

esquema_esperado = {
    'id': 'int',
    'nombre': 'str',
    'edad': 'int',
    'salario': 'float',
    'activo': 'bool'
}
```

### Solución

```python
from typing import Dict, List, Tuple

def validar_tipos_columnas(df: pd.DataFrame,
                          esquema: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Valida que las columnas del DataFrame tengan los tipos esperados.

    Args:
        df: DataFrame a validar
        esquema: Dict con nombre_columna: tipo_esperado

    Returns:
        Tupla (es_valido, lista_errores)
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    errores = []

    # Mapeo de tipos esperados a tipos de pandas
    mapeo_tipos = {
        'int': ['int64', 'int32', 'int16', 'int8'],
        'float': ['float64', 'float32'],
        'str': ['object'],
        'bool': ['bool']
    }

    for columna, tipo_esperado in esquema.items():
        # Verificar que columna existe
        if columna not in df.columns:
            errores.append(f"Columna '{columna}' no encontrada en DataFrame")
            continue

        # Obtener tipo actual
        tipo_actual = str(df[columna].dtype)

        # Verificar tipo
        if tipo_esperado not in mapeo_tipos:
            errores.append(f"Tipo '{tipo_esperado}' no reconocido para columna '{columna}'")
            continue

        tipos_validos = mapeo_tipos[tipo_esperado]
        if tipo_actual not in tipos_validos:
            errores.append(
                f"Columna '{columna}': esperado {tipo_esperado}, encontrado {tipo_actual}"
            )

    es_valido = len(errores) == 0
    return es_valido, errores


# Prueba
es_valido, errores = validar_tipos_columnas(df, esquema_esperado)

if es_valido:
    print("✓ Todos los tipos son válidos")
else:
    print("✗ Errores de validación:")
    for error in errores:
        print(f"  - {error}")
```

### Resultado Esperado

```
✗ Errores de validación:
  - Columna 'edad': esperado int, encontrado object
  - Columna 'activo': esperado bool, encontrado int64
```

---

## Ejercicio 2: Detección de Duplicados Exactos ⭐

### Enunciado

Crea una función que detecte duplicados exactos en columnas específicas y genere un reporte detallado.

### Datos de Entrada

```python
df_productos = pd.DataFrame({
    'producto_id': [1, 2, 3, 4, 5, 6, 7],
    'nombre': ['Laptop', 'Mouse', 'Teclado', 'Mouse', 'Monitor', 'Laptop', 'Cable'],
    'precio': [850, 25, 75, 25, 320, 850, 10],
    'categoria': ['Computadoras', 'Accesorios', 'Accesorios', 'Accesorios',
                  'Electrónica', 'Computadoras', 'Accesorios']
})
```

### Solución

```python
from typing import List

def detectar_y_reportar_duplicados(df: pd.DataFrame,
                                    columnas: List[str]) -> Dict:
    """
    Detecta duplicados y genera reporte detallado.

    Args:
        df: DataFrame a analizar
        columnas: Lista de columnas para identificar duplicados

    Returns:
        Dict con estadísticas y registros duplicados
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    for col in columnas:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en DataFrame")

    # Detectar duplicados
    mascara_duplicados = df.duplicated(subset=columnas, keep=False)
    df_duplicados = df[mascara_duplicados].sort_values(by=columnas)

    # Generar reporte
    reporte = {
        'total_registros': len(df),
        'registros_duplicados': mascara_duplicados.sum(),
        'porcentaje_duplicados': round((mascara_duplicados.sum() / len(df)) * 100, 2),
        'registros_unicos': (~mascara_duplicados).sum(),
        'grupos_duplicados': 0,
        'duplicados_por_grupo': []
    }

    # Identificar grupos de duplicados
    if not df_duplicados.empty:
        grupos = df_duplicados.groupby(columnas).size()
        reporte['grupos_duplicados'] = len(grupos)
        reporte['duplicados_por_grupo'] = grupos.to_dict()

    reporte['dataframe_duplicados'] = df_duplicados

    return reporte


# Prueba
reporte = detectar_y_reportar_duplicados(df_productos, ['nombre', 'precio'])

print(f"Total de registros: {reporte['total_registros']}")
print(f"Registros duplicados: {reporte['registros_duplicados']} ({reporte['porcentaje_duplicados']}%)")
print(f"Grupos de duplicados: {reporte['grupos_duplicados']}")
print("\nRegistros duplicados:")
print(reporte['dataframe_duplicados'])
```

### Resultado Esperado

```
Total de registros: 7
Registros duplicados: 4 (57.14%)
Grupos de duplicados: 2

Registros duplicados:
   producto_id   nombre  precio      categoria
0            1   Laptop     850  Computadoras
5            6   Laptop     850  Computadoras
1            2    Mouse      25   Accesorios
3            4    Mouse      25   Accesorios
```

---

## Ejercicio 3: Identificación de Outliers con IQR ⭐

### Enunciado

Implementa una función que identifique outliers usando el método IQR y los clasifique en outliers bajos y altos.

### Datos de Entrada

```python
df_ventas = pd.DataFrame({
    'dia': range(1, 21),
    'ventas': [100, 105, 98, 102, 110, 95, 105, 103, 108, 99,
               500, 97, 104, 102, 106, 101, 99, -50, 103, 1000]
})
```

### Solución

```python
def identificar_outliers_iqr(df: pd.DataFrame,
                             columna: str) -> Dict:
    """
    Identifica outliers usando método IQR.

    Args:
        df: DataFrame a analizar
        columna: Nombre de la columna numérica

    Returns:
        Dict con outliers bajos, altos y estadísticas
    """
    if columna not in df.columns:
        raise ValueError(f"Columna '{columna}' no existe")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"Columna '{columna}' debe ser numérica")

    # Calcular cuartiles e IQR
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1

    # Calcular límites
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Identificar outliers
    outliers_bajos = df[df[columna] < limite_inferior]
    outliers_altos = df[df[columna] > limite_superior]

    resultado = {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'limite_inferior': limite_inferior,
        'limite_superior': limite_superior,
        'outliers_bajos': outliers_bajos,
        'num_outliers_bajos': len(outliers_bajos),
        'outliers_altos': outliers_altos,
        'num_outliers_altos': len(outliers_altos),
        'total_outliers': len(outliers_bajos) + len(outliers_altos)
    }

    return resultado


# Prueba
resultado = identificar_outliers_iqr(df_ventas, 'ventas')

print(f"Rango válido: [{resultado['limite_inferior']:.2f}, {resultado['limite_superior']:.2f}]")
print(f"Outliers bajos: {resultado['num_outliers_bajos']}")
print(resultado['outliers_bajos'])
print(f"\nOutliers altos: {resultado['num_outliers_altos']}")
print(resultado['outliers_altos'])
```

### Resultado Esperado

```
Rango válido: [86.25, 118.75]
Outliers bajos: 1
    dia  ventas
17   18     -50

Outliers altos: 2
    dia  ventas
10   11     500
19   20    1000
```

---

## Ejercicio 4: Cálculo de Completitud ⭐

### Enunciado

Crea una función que calcule la completitud (porcentaje de valores no nulos) por columna y genere un reporte visual.

### Datos de Entrada

```python
df_clientes = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'nombre': ['Ana', 'Luis', None, 'María', 'Juan'],
    'email': ['ana@email.com', None, 'pedro@email.com', 'maria@email.com', None],
    'telefono': ['611111111', '622222222', None, None, '655555555'],
    'direccion': [None, None, None, 'Calle Mayor 1', 'Plaza Sol 5']
})
```

### Solución

```python
def calcular_completitud(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula completitud por columna.

    Args:
        df: DataFrame a analizar

    Returns:
        DataFrame con estadísticas de completitud
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    total_registros = len(df)

    estadisticas = []
    for columna in df.columns:
        valores_no_nulos = df[columna].notna().sum()
        valores_nulos = df[columna].isna().sum()
        completitud = (valores_no_nulos / total_registros) * 100

        estadisticas.append({
            'columna': columna,
            'valores_no_nulos': valores_no_nulos,
            'valores_nulos': valores_nulos,
            'completitud_%': round(completitud, 2),
            'estado': 'Excelente' if completitud == 100
                     else 'Bueno' if completitud >= 80
                     else 'Regular' if completitud >= 50
                     else 'Malo'
        })

    df_resultado = pd.DataFrame(estadisticas)
    df_resultado = df_resultado.sort_values('completitud_%', ascending=False)

    return df_resultado


# Prueba
reporte_completitud = calcular_completitud(df_clientes)
print("Reporte de Completitud:")
print(reporte_completitud.to_string(index=False))

# Calcular completitud global
completitud_global = reporte_completitud['completitud_%'].mean()
print(f"\nCompletitud global: {completitud_global:.2f}%")
```

### Resultado Esperado

```
Reporte de Completitud:
    columna  valores_no_nulos  valores_nulos  completitud_%      estado
         id                 5              0         100.00  Excelente
     nombre                 4              1          80.00       Bueno
      email                 3              2          60.00     Regular
   telefono                 3              2          60.00     Regular
  direccion                 2              3          40.00        Malo

Completitud global: 68.00%
```

---

## Ejercicio 5: Validación de Rangos ⭐

### Enunciado

Implementa una función que valide que los valores numéricos están dentro de rangos permitidos.

### Datos de Entrada

```python
df_empleados = pd.DataFrame({
    'empleado_id': [1, 2, 3, 4, 5],
    'nombre': ['Ana', 'Luis', 'Pedro', 'María', 'Juan'],
    'edad': [25, 30, 150, 28, -5],
    'salario': [30000, 35000, 32000, 1000000, -1000],
    'antiguedad': [2, 5, 3, 8, 100]
})

rangos_validos = {
    'edad': (18, 70),
    'salario': (15000, 200000),
    'antiguedad': (0, 50)
}
```

### Solución

```python
from typing import Dict, Tuple

def validar_rangos_numericos(df: pd.DataFrame,
                             rangos: Dict[str, Tuple[float, float]]) -> Dict:
    """
    Valida que valores numéricos están en rangos válidos.

    Args:
        df: DataFrame a validar
        rangos: Dict con columna: (min, max)

    Returns:
        Dict con resultados de validación
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    resultado = {
        'es_valido': True,
        'errores': [],
        'valores_fuera_rango': {}
    }

    for columna, (minimo, maximo) in rangos.items():
        if columna not in df.columns:
            resultado['errores'].append(f"Columna '{columna}' no existe")
            resultado['es_valido'] = False
            continue

        if not pd.api.types.is_numeric_dtype(df[columna]):
            resultado['errores'].append(f"Columna '{columna}' no es numérica")
            resultado['es_valido'] = False
            continue

        # Detectar valores fuera de rango
        fuera_rango = df[(df[columna] < minimo) | (df[columna] > maximo)]

        if not fuera_rango.empty:
            resultado['es_valido'] = False
            resultado['valores_fuera_rango'][columna] = fuera_rango
            resultado['errores'].append(
                f"Columna '{columna}': {len(fuera_rango)} valores fuera del rango [{minimo}, {maximo}]"
            )

    return resultado


# Prueba
resultado = validar_rangos_numericos(df_empleados, rangos_validos)

if resultado['es_valido']:
    print("✓ Todos los valores están en rangos válidos")
else:
    print("✗ Valores fuera de rango detectados:\n")
    for error in resultado['errores']:
        print(f"  - {error}")

    print("\nRegistros problemáticos:")
    for columna, df_problema in resultado['valores_fuera_rango'].items():
        print(f"\n{columna}:")
        print(df_problema[['empleado_id', 'nombre', columna]])
```

### Resultado Esperado

```
✗ Valores fuera de rango detectados:

  - Columna 'edad': 2 valores fuera del rango [18, 70]
  - Columna 'salario': 2 valores fuera del rango [15000, 200000]
  - Columna 'antiguedad': 1 valores fuera del rango [0, 50]

Registros problemáticos:

edad:
   empleado_id nombre  edad
2            3  Pedro   150
4            5   Juan    -5

salario:
   empleado_id nombre  salario
3            4  María  1000000
4            5   Juan    -1000

antiguedad:
   empleado_id nombre  antiguedad
4            5   Juan         100
```

---

## Ejercicio 6: Validación de Esquema con Pandera ⭐⭐

### Enunciado

Define un esquema con Pandera que valide un DataFrame de transacciones bancarias con múltiples reglas de negocio.

### Datos de Entrada

```python
df_transacciones = pd.DataFrame({
    'transaccion_id': [1, 2, 2, 3, 4],  # 2 duplicado
    'cuenta_origen': ['ES12', 'ES34', 'ES56', 'ES78', 'INVALID'],
    'cuenta_destino': ['ES99', 'ES88', 'ES77', 'ES66', 'ES55'],
    'monto': [100.50, -50.00, 250.00, 1000000.00, 75.25],  # -50 negativo, 1M muy alto
    'tipo': ['Transferencia', 'Pago', 'Retiro', 'Transferencia', 'Deposito'],  # Deposito != Depósito
    'fecha': ['2024-10-20', '2024-10-21', '2024-10-22', '2025-12-01', '2024-10-24']  # 2025 futura
})
```

### Solución

```python
import pandera as pa
from pandera import Column, Check

# Función de validación personalizada
def codigo_iban_valido(codigo: str) -> bool:
    """Valida formato básico de código bancario español."""
    import re
    patron = r'^ES\d{2}$'
    return bool(re.match(patron, str(codigo)))

# Definir esquema
esquema_transacciones = pa.DataFrameSchema(
    columns={
        "transaccion_id": Column(
            int,
            checks=[
                Check.greater_than(0),
                Check(lambda s: s.is_unique, error="IDs de transacción deben ser únicos")
            ],
            nullable=False
        ),
        "cuenta_origen": Column(
            str,
            checks=Check(codigo_iban_valido, error="Código de cuenta inválido"),
            nullable=False
        ),
        "cuenta_destino": Column(
            str,
            checks=Check(codigo_iban_valido, error="Código de cuenta inválido"),
            nullable=False
        ),
        "monto": Column(
            float,
            checks=[
                Check.greater_than(0, error="Monto debe ser positivo"),
                Check.less_than_or_equal_to(100000, error="Monto excede límite de 100,000")
            ],
            nullable=False
        ),
        "tipo": Column(
            str,
            checks=Check.isin(
                ["Transferencia", "Pago", "Retiro", "Depósito"],
                error="Tipo de transacción no válido"
            ),
            nullable=False
        ),
        "fecha": Column(
            pd.DatetimeTZDtype(tz="UTC"),
            checks=Check(
                lambda s: s <= pd.Timestamp.now(tz="UTC"),
                error="Fecha no puede ser futura"
            ),
            nullable=False
        ),
    },
    coerce=True
)

def validar_transacciones(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Valida DataFrame de transacciones."""
    errores = []

    # Convertir fecha a datetime
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'], utc=True)

    try:
        esquema_transacciones.validate(df, lazy=True)
        return True, []
    except pa.errors.SchemaErrors as e:
        for error_line in str(e).split('\n'):
            if error_line.strip() and not error_line.startswith('---'):
                errores.append(error_line.strip())
        return False, errores

# Prueba
es_valido, errores = validar_transacciones(df_transacciones)

if es_valido:
    print("✓ Transacciones válidas")
else:
    print("✗ Errores encontrados:")
    for error in errores[:10]:  # Mostrar primeros 10 errores
        print(f"  - {error}")
```

---

## Ejercicio 7: Fuzzy Matching de Nombres ⭐⭐

### Enunciado

Implementa una función que encuentre nombres similares en una lista usando fuzzy matching con diferentes métodos y devuelva los más probables duplicados.

### Solución

```python
from rapidfuzz import fuzz
from typing import List

def encontrar_nombres_similares(nombres: List[str],
                                umbral: int = 80) -> pd.DataFrame:
    """
    Encuentra nombres similares usando fuzzy matching.

    Args:
        nombres: Lista de nombres a comparar
        umbral: Score mínimo para considerar similitud

    Returns:
        DataFrame con pares similares ordenados por score
    """
    if not nombres:
        raise ValueError("Lista de nombres está vacía")

    similares = []

    for i, nombre1 in enumerate(nombres):
        for nombre2 in nombres[i+1:]:
            # Calcular múltiples scores
            score_ratio = fuzz.ratio(nombre1, nombre2)
            score_partial = fuzz.partial_ratio(nombre1, nombre2)
            score_token_sort = fuzz.token_sort_ratio(nombre1, nombre2)

            # Score promedio
            score_promedio = (score_ratio + score_partial + score_token_sort) / 3

            if score_promedio >= umbral:
                similares.append({
                    'nombre1': nombre1,
                    'nombre2': nombre2,
                    'score_ratio': score_ratio,
                    'score_partial': score_partial,
                    'score_token_sort': score_token_sort,
                    'score_promedio': round(score_promedio, 2)
                })

    if similares:
        df_similares = pd.DataFrame(similares)
        df_similares = df_similares.sort_values('score_promedio', ascending=False)
        return df_similares
    else:
        return pd.DataFrame()

# Prueba
nombres_clientes = [
    'Juan Pérez García',
    'Juan Perez Garcia',
    'J. Pérez García',
    'María López Martínez',
    'Maria Lopez Martinez',
    'Pedro Sánchez',
    'Ana García Fernández',
    'Ana García Fdez.',
    'Luis Rodríguez Torres'
]

resultado = encontrar_nombres_similares(nombres_clientes, umbral=80)

if not resultado.empty:
    print(f"Se encontraron {len(resultado)} pares de nombres similares:\n")
    print(resultado.to_string(index=False))
else:
    print("No se encontraron nombres similares")
```

---

## Ejercicio 8: Detección de Outliers Multivariada ⭐⭐

### Enunciado

Implementa detección de outliers considerando múltiples columnas simultáneamente usando Isolation Forest.

### Solución

```python
from sklearn.ensemble import IsolationForest
import numpy as np

def detectar_outliers_multivariado(df: pd.DataFrame,
                                    columnas: List[str],
                                    contamination: float = 0.1) -> pd.DataFrame:
    """
    Detecta outliers considerando múltiples variables.

    Args:
        df: DataFrame a analizar
        columnas: Lista de columnas numéricas a considerar
        contamination: Proporción esperada de outliers

    Returns:
        DataFrame original con columna 'es_outlier' añadida
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    for col in columnas:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"Columna '{col}' debe ser numérica")

    # Preparar datos
    X = df[columnas].fillna(df[columnas].median())

    # Entrenar modelo
    clf = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )

    predicciones = clf.fit_predict(X)
    scores = clf.score_samples(X)

    # Añadir resultados al DataFrame
    df_resultado = df.copy()
    df_resultado['es_outlier'] = predicciones == -1
    df_resultado['anomaly_score'] = scores

    return df_resultado


# Prueba
np.random.seed(42)
df_ventas_multi = pd.DataFrame({
    'producto_id': range(1, 101),
    'precio': np.random.normal(100, 20, 100),
    'cantidad_vendida': np.random.normal(50, 10, 100),
    'descuento': np.random.uniform(0, 0.3, 100)
})

# Añadir outliers artificiales
df_ventas_multi.loc[98, 'precio'] = 500  # Precio muy alto
df_ventas_multi.loc[99, 'cantidad_vendida'] = 200  # Cantidad muy alta

resultado = detectar_outliers_multivariado(
    df_ventas_multi,
    ['precio', 'cantidad_vendida', 'descuento'],
    contamination=0.05
)

outliers = resultado[resultado['es_outlier']]
print(f"Outliers detectados: {len(outliers)}")
print("\nRegistros outliers:")
print(outliers[['producto_id', 'precio', 'cantidad_vendida', 'anomaly_score']])
```

---

## Ejercicio 9: Perfil de Calidad Personalizado ⭐⭐

### Enunciado

Crea una función que genere un perfil de calidad personalizado con métricas clave: completitud, duplicados, outliers y tipos de datos.

### Solución

```python
def generar_perfil_calidad(df: pd.DataFrame) -> Dict:
    """
    Genera perfil completo de calidad del DataFrame.

    Args:
        df: DataFrame a analizar

    Returns:
        Dict con métricas de calidad
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    perfil = {
        'resumen_general': {},
        'completitud_por_columna': {},
        'duplicados': {},
        'tipos_datos': {},
        'outliers_numericos': {}
    }

    # 1. Resumen general
    perfil['resumen_general'] = {
        'num_registros': len(df),
        'num_columnas': len(df.columns),
        'memoria_mb': round(df.memory_usage(deep=True).sum() / (1024**2), 2)
    }

    # 2. Completitud por columna
    for col in df.columns:
        perfil['completitud_por_columna'][col] = {
            'nulos': int(df[col].isna().sum()),
            'porcentaje_completo': round((df[col].notna().sum() / len(df)) * 100, 2)
        }

    # 3. Duplicados
    duplicados_completos = df.duplicated().sum()
    perfil['duplicados'] = {
        'registros_duplicados': int(duplicados_completos),
        'porcentaje': round((duplicados_completos / len(df)) * 100, 2)
    }

    # 4. Tipos de datos
    for col in df.columns:
        perfil['tipos_datos'][col] = str(df[col].dtype)

    # 5. Outliers en columnas numéricas
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR

        outliers = ((df[col] < limite_inf) | (df[col] > limite_sup)).sum()

        perfil['outliers_numericos'][col] = {
            'num_outliers': int(outliers),
            'porcentaje': round((outliers / len(df)) * 100, 2)
        }

    return perfil


# Prueba
import json

perfil = generar_perfil_calidad(df_ventas_multi)
print("PERFIL DE CALIDAD")
print("=" * 60)
print(json.dumps(perfil, indent=2, ensure_ascii=False))
```

---

## Ejercicio 10: Consolidación de Duplicados ⭐⭐

### Enunciado

Implementa una función que consolide registros duplicados eligiendo el "mejor" registro según criterios configurables.

### Solución

```python
def consolidar_duplicados_inteligente(df: pd.DataFrame,
                                       columnas_clave: List[str],
                                       prioridad_columnas: List[str]) -> pd.DataFrame:
    """
    Consolida duplicados eligiendo el registro más completo.

    Args:
        df: DataFrame con duplicados
        columnas_clave: Columnas para identificar duplicados
        prioridad_columnas: Columnas prioritarias para elegir mejor registro

    Returns:
        DataFrame consolidado
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    # Identificar duplicados
    duplicados_mascara = df.duplicated(subset=columnas_clave, keep=False)

    if not duplicados_mascara.any():
        return df.copy()  # Sin duplicados

    # Separar únicos y duplicados
    df_unicos = df[~duplicados_mascara].copy()
    df_duplicados = df[duplicados_mascara].copy()

    # Para cada grupo de duplicados, elegir el mejor
    mejores_registros = []

    for valores_clave, grupo in df_duplicados.groupby(columnas_clave):
        # Calcular score de calidad para cada registro
        scores = []

        for idx in grupo.index:
            registro = grupo.loc[idx]
            score = 0

            # Sumar puntos por campos no nulos en columnas prioritarias
            for col in prioridad_columnas:
                if col in registro.index and pd.notna(registro[col]):
                    score += 2  # Peso 2 para columnas prioritarias

            # Sumar puntos por campos no nulos en otras columnas
            for col in registro.index:
                if col not in prioridad_columnas and pd.notna(registro[col]):
                    score += 1

            scores.append((idx, score))

        # Elegir el registro con mayor score
        mejor_idx = max(scores, key=lambda x: x[1])[0]
        mejores_registros.append(grupo.loc[mejor_idx])

    # Combinar únicos con mejores duplicados
    df_consolidado = pd.concat([df_unicos, pd.DataFrame(mejores_registros)], ignore_index=True)

    return df_consolidado


# Prueba
df_clientes_dup = pd.DataFrame({
    'email': ['ana@email.com', 'ana@email.com', 'luis@email.com', 'luis@email.com', 'pedro@email.com'],
    'nombre': ['Ana García', 'Ana García', 'Luis López', None, 'Pedro Ruiz'],
    'telefono': [None, '611111111', '622222222', '622222222', '633333333'],
    'direccion': ['Calle 1', None, None, 'Plaza 2', 'Avenida 3'],
    'fecha_registro': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-03-15', '2024-04-01']
})

print("Datos originales:")
print(df_clientes_dup)

df_consolidado = consolidar_duplicados_inteligente(
    df_clientes_dup,
    columnas_clave=['email'],
    prioridad_columnas=['nombre', 'telefono']
)

print("\nDatos consolidados:")
print(df_consolidado)
print(f"\nRegistros: {len(df_clientes_dup)} → {len(df_consolidado)}")
```

---

## Ejercicio 11: Pipeline de Calidad Completo ⭐⭐⭐

### Enunciado

Implementa un pipeline completo que aplique todas las técnicas de calidad secuencialmente: validación, duplicados, outliers y genere reporte final.

### Solución

```python
def pipeline_calidad_completo(df: pd.DataFrame, config: Dict) -> Tuple[pd.DataFrame, Dict]:
    """
    Pipeline completo de calidad de datos.

    Args:
        df: DataFrame a procesar
        config: Configuración con esquemas, rangos, etc.

    Returns:
        Tupla (DataFrame limpio, reporte detallado)
    """
    reporte = {
        'inicio': {
            'registros': len(df),
            'columnas': len(df.columns)
        },
        'pasos': []
    }

    df_procesado = df.copy()

    # Paso 1: Validar tipos
    print("Paso 1: Validando tipos de datos...")
    if 'esquema_tipos' in config:
        es_valido, errores = validar_tipos_columnas(df_procesado, config['esquema_tipos'])
        reporte['pasos'].append({
            'paso': 'validacion_tipos',
            'valido': es_valido,
            'errores': errores
        })
        if not es_valido:
            print(f"  ⚠ Errores de tipo encontrados: {len(errores)}")

    # Paso 2: Eliminar duplicados
    print("Paso 2: Eliminando duplicados...")
    registros_antes = len(df_procesado)
    df_procesado = df_procesado.drop_duplicates(subset=config.get('columnas_clave', None))
    duplicados_eliminados = registros_antes - len(df_procesado)
    reporte['pasos'].append({
        'paso': 'eliminacion_duplicados',
        'duplicados_eliminados': duplicados_eliminados
    })
    print(f"  ✓ Eliminados {duplicados_eliminados} duplicados")

    # Paso 3: Eliminar outliers
    print("Paso 3: Tratando outliers...")
    total_outliers = 0
    for col in config.get('columnas_outliers', []):
        if pd.api.types.is_numeric_dtype(df_procesado[col]):
            outliers, _ = detectar_outliers_iqr(df_procesado, col)
            registros_antes = len(df_procesado)
            df_procesado = df_procesado[~outliers]
            outliers_eliminados = registros_antes - len(df_procesado)
            total_outliers += outliers_eliminados
            print(f"  ✓ {col}: {outliers_eliminados} outliers eliminados")

    reporte['pasos'].append({
        'paso': 'tratamiento_outliers',
        'total_outliers_eliminados': total_outliers
    })

    # Paso 4: Perfil final
    print("Paso 4: Generando perfil final...")
    perfil_final = generar_perfil_calidad(df_procesado)
    reporte['perfil_final'] = perfil_final

    reporte['final'] = {
        'registros': len(df_procesado),
        'columnas': len(df_procesado.columns),
        'registros_eliminados': len(df) - len(df_procesado),
        'porcentaje_retenido': round((len(df_procesado) / len(df)) * 100, 2)
    }

    print(f"\n✓ Pipeline completado")
    print(f"  Registros: {len(df)} → {len(df_procesado)} ({reporte['final']['porcentaje_retenido']}%)")

    return df_procesado, reporte


# Prueba
config_calidad = {
    'esquema_tipos': {
        'producto_id': 'int',
        'precio': 'float',
        'cantidad_vendida': 'int'
    },
    'columnas_clave': ['producto_id'],
    'columnas_outliers': ['precio', 'cantidad_vendida']
}

df_limpio, reporte = pipeline_calidad_completo(df_ventas_multi, config_calidad)
```

---

*Los ejercicios 12-15 seguirían el mismo formato con casos más avanzados: Sistema de Alertas, Validación Cross-Field, Framework Reutilizable y Monitoreo Temporal.*

---

## 📝 Resumen

Has practicado:

1. **Validación**: Tipos, rangos, esquemas con Pandera
2. **Duplicados**: Exactos y fuzzy matching
3. **Outliers**: IQR, Z-score, Isolation Forest
4. **Profiling**: Métricas de calidad completas
5. **Pipelines**: Integración de todas las técnicas

**Siguiente paso**: Aplica estos conceptos en el proyecto práctico del Tema 4.

---

*Última actualización: 2025-10-30*
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
