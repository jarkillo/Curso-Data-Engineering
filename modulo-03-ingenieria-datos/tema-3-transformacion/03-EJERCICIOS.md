# Ejercicios Prácticos: Transformación con Pandas

**Objetivo**: Practicar las técnicas de transformación de datos con Pandas en ejercicios progresivos.

**Instrucciones**:
- Intenta resolver cada ejercicio sin mirar la solución
- Prueba tu código con diferentes casos
- Compara tu solución con la proporcionada
- Los ejercicios están ordenados por dificultad (⭐ fácil → ⭐⭐⭐ difícil)

---

## 📋 Índice de Ejercicios

### Básicos (⭐)
1. [Filtrado Básico](#ejercicio-1-filtrado-básico-)
2. [Cálculo de Columnas Derivadas](#ejercicio-2-cálculo-de-columnas-derivadas-)
3. [Manejo de Valores Nulos](#ejercicio-3-manejo-de-valores-nulos-)
4. [Normalización de Texto](#ejercicio-4-normalización-de-texto-)
5. [Agrupación Simple](#ejercicio-5-agrupación-simple-)

### Intermedios (⭐⭐)
6. [Transformación con Apply](#ejercicio-6-transformación-con-apply-)
7. [Merge de DataFrames](#ejercicio-7-merge-de-dataframes-)
8. [GroupBy con Múltiples Agregaciones](#ejercicio-8-groupby-con-múltiples-agregaciones-)
9. [Pivot Table](#ejercicio-9-pivot-table-)
10. [Detección de Duplicados Complejos](#ejercicio-10-detección-de-duplicados-complejos-)

### Avanzados (⭐⭐⭐)
11. [Pipeline de Limpieza Completo](#ejercicio-11-pipeline-de-limpieza-completo-)
12. [Cálculo de Métricas Rolling](#ejercicio-12-cálculo-de-métricas-rolling-)
13. [Transformación Condicional Compleja](#ejercicio-13-transformación-condicional-compleja-)
14. [Merge Múltiple con Validación](#ejercicio-14-merge-múltiple-con-validación-)
15. [Optimización de Performance](#ejercicio-15-optimización-de-performance-)

---

## Ejercicio 1: Filtrado Básico ⭐

### Enunciado

Dada una tabla de productos, filtra aquellos que:
- Tengan un precio mayor a 100
- Pertenezcan a la categoría "Electrónica" o "Computadoras"
- Tengan stock disponible (> 0)

### Datos de Entrada

```python
import pandas as pd

productos = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'nombre': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Tablet', 'Cable', 'Impresora', 'Router'],
    'precio': [850, 25, 75, 320, 450, 10, 280, 95],
    'categoria': ['Computadoras', 'Accesorios', 'Accesorios', 'Electrónica',
                  'Computadoras', 'Accesorios', 'Electrónica', 'Redes'],
    'stock': [15, 120, 45, 0, 8, 200, 12, 0]
})
```

### Solución

```python
def filtrar_productos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra productos según criterios específicos.

    Args:
        df: DataFrame con datos de productos

    Returns:
        DataFrame filtrado
    """
    # Aplicar filtros combinados
    productos_filtrados = df[
        (df['precio'] > 100) &
        (df['categoria'].isin(['Electrónica', 'Computadoras'])) &
        (df['stock'] > 0)
    ]

    return productos_filtrados


# Prueba
resultado = filtrar_productos(productos)
print(resultado)

# Output esperado:
#    id   nombre  precio      categoria  stock
# 0   1   Laptop     850  Computadoras     15
# 3   4  Monitor     320   Electrónica      0  (No debería aparecer, stock=0)
# 4   5   Tablet     450  Computadoras      8
# 6   7 Impresora   280   Electrónica     12
```

### Validación

```python
assert len(resultado) == 3, "Deberían ser 3 productos"
assert all(resultado['precio'] > 100), "Todos los precios deben ser > 100"
assert all(resultado['stock'] > 0), "Todos deben tener stock"
print("✅ Ejercicio 1 correcto")
```

---

## Ejercicio 2: Cálculo de Columnas Derivadas ⭐

### Enunciado

Dada una tabla de ventas, calcula:
- `subtotal`: cantidad × precio_unitario
- `descuento_monto`: subtotal × (descuento_pct / 100)
- `total`: subtotal - descuento_monto
- `iva`: total × 0.21
- `total_con_iva`: total + iva

### Datos de Entrada

```python
ventas = pd.DataFrame({
    'venta_id': [1, 2, 3, 4, 5],
    'cantidad': [2, 1, 5, 3, 4],
    'precio_unitario': [100, 50, 25, 75, 120],
    'descuento_pct': [10, 0, 15, 5, 20]
})
```

### Solución

```python
def calcular_columnas_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula columnas derivadas de ventas.

    Args:
        df: DataFrame con ventas

    Returns:
        DataFrame con columnas calculadas
    """
    df_result = df.copy()

    # Cálculos en secuencia
    df_result['subtotal'] = df_result['cantidad'] * df_result['precio_unitario']
    df_result['descuento_monto'] = df_result['subtotal'] * (df_result['descuento_pct'] / 100)
    df_result['total'] = df_result['subtotal'] - df_result['descuento_monto']
    df_result['iva'] = df_result['total'] * 0.21
    df_result['total_con_iva'] = df_result['total'] + df_result['iva']

    # Redondear a 2 decimales
    columnas_redondear = ['subtotal', 'descuento_monto', 'total', 'iva', 'total_con_iva']
    df_result[columnas_redondear] = df_result[columnas_redondear].round(2)

    return df_result


# Prueba
resultado = calcular_columnas_ventas(ventas)
print(resultado[['venta_id', 'cantidad', 'precio_unitario', 'total', 'total_con_iva']])

# Output esperado:
#    venta_id  cantidad  precio_unitario   total  total_con_iva
# 0         1         2              100  180.00         217.80
# 1         2         1               50   50.00          60.50
# 2         3         5               25  106.25         128.56
# 3         4         3               75  213.75         258.64
# 4         5         4              120  384.00         464.64
```

### Validación

```python
assert 'total_con_iva' in resultado.columns, "Debe tener columna total_con_iva"
assert resultado['total_con_iva'].iloc[0] == 217.80, "Cálculo incorrecto"
print("✅ Ejercicio 2 correcto")
```

---

## Ejercicio 3: Manejo de Valores Nulos ⭐

### Enunciado

Limpia un DataFrame con valores nulos siguiendo estas reglas:
- Elimina filas donde `id` sea nulo
- Rellena `nombre` nulo con "Desconocido"
- Rellena `edad` nulo con la mediana
- Rellena `ciudad` nulo con "No Especificada"
- Elimina la columna `comentarios` si tiene más del 50% de nulos

### Datos de Entrada

```python
import numpy as np

clientes = pd.DataFrame({
    'id': [1, 2, None, 4, 5, 6],
    'nombre': ['Ana', None, 'Carlos', 'Diana', 'Eduardo', None],
    'edad': [25, 34, 28, None, 45, 31],
    'ciudad': ['Madrid', 'Barcelona', None, 'Valencia', None, 'Sevilla'],
    'comentarios': [None, None, None, 'VIP', None, None]
})
```

### Solución

```python
def limpiar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia valores nulos según reglas específicas.

    Args:
        df: DataFrame con valores nulos

    Returns:
        DataFrame limpio
    """
    df_clean = df.copy()

    # 1. Eliminar filas sin ID
    df_clean = df_clean.dropna(subset=['id'])

    # 2. Rellenar nombre
    df_clean['nombre'] = df_clean['nombre'].fillna('Desconocido')

    # 3. Rellenar edad con mediana
    edad_mediana = df_clean['edad'].median()
    df_clean['edad'] = df_clean['edad'].fillna(edad_mediana)

    # 4. Rellenar ciudad
    df_clean['ciudad'] = df_clean['ciudad'].fillna('No Especificada')

    # 5. Eliminar columnas con >50% nulos
    umbral = len(df_clean) * 0.5
    df_clean = df_clean.dropna(axis=1, thresh=umbral)

    return df_clean


# Prueba
resultado = limpiar_nulos(clientes)
print(resultado)
print(f"\nColumnas finales: {list(resultado.columns)}")

# Output esperado: 5 filas, sin columna 'comentarios'
```

### Validación

```python
assert len(resultado) == 5, "Deberían ser 5 filas (1 eliminada)"
assert resultado['id'].isnull().sum() == 0, "No debe haber IDs nulos"
assert 'comentarios' not in resultado.columns, "Columna comentarios debe eliminarse"
print("✅ Ejercicio 3 correcto")
```

---

## Ejercicio 4: Normalización de Texto ⭐

### Enunciado

Normaliza los datos de texto en un DataFrame:
- Convierte nombres a formato Title Case (Primera Letra Mayúscula)
- Convierte emails a minúsculas
- Elimina espacios al inicio y final
- Estandariza códigos de país a mayúsculas

### Datos de Entrada

```python
usuarios = pd.DataFrame({
    'nombre': ['  juan perez  ', 'MARIA LOPEZ', 'ana García', '  Carlos Ruiz'],
    'email': ['JUAN@EMAIL.COM', '  maria@email.com', 'Ana@EMAIL.com  ', 'carlos@email.com'],
    'pais': ['es', 'ES', 'Fr', '  uk  ']
})
```

### Solución

```python
def normalizar_texto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza campos de texto.

    Args:
        df: DataFrame con texto sin normalizar

    Returns:
        DataFrame con texto normalizado
    """
    df_norm = df.copy()

    # Nombres: Title Case y trim
    df_norm['nombre'] = df_norm['nombre'].str.strip().str.title()

    # Emails: minúsculas y trim
    df_norm['email'] = df_norm['email'].str.strip().str.lower()

    # País: mayúsculas y trim
    df_norm['pais'] = df_norm['pais'].str.strip().str.upper()

    return df_norm


# Prueba
resultado = normalizar_texto(usuarios)
print(resultado)

# Output esperado:
#          nombre              email pais
# 0   Juan Perez   juan@email.com   ES
# 1  Maria Lopez  maria@email.com   ES
# 2   Ana García    ana@email.com   FR
# 3  Carlos Ruiz carlos@email.com   UK
```

### Validación

```python
assert resultado['nombre'].iloc[0] == 'Juan Perez', "Formato de nombre incorrecto"
assert resultado['email'].iloc[0] == 'juan@email.com', "Email debe estar en minúsculas"
assert resultado['pais'].iloc[0] == 'ES', "País debe estar en mayúsculas"
print("✅ Ejercicio 4 correcto")
```

---

## Ejercicio 5: Agrupación Simple ⭐

### Enunciado

Agrupa las ventas por categoría y calcula:
- Total de ventas (suma)
- Número de transacciones (count)
- Ticket promedio (mean)
- Venta máxima (max)

Ordena el resultado por total de ventas descendente.

### Datos de Entrada

```python
ventas = pd.DataFrame({
    'categoria': ['Electrónica', 'Ropa', 'Electrónica', 'Alimentos',
                  'Ropa', 'Electrónica', 'Alimentos', 'Ropa'],
    'monto': [1200, 85, 450, 35, 120, 890, 28, 95]
})
```

### Solución

```python
def agrupar_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa ventas por categoría con múltiples métricas.

    Args:
        df: DataFrame con ventas

    Returns:
        DataFrame agregado
    """
    resultado = df.groupby('categoria').agg(
        total_ventas=('monto', 'sum'),
        num_transacciones=('monto', 'count'),
        ticket_promedio=('monto', 'mean'),
        venta_maxima=('monto', 'max')
    ).round(2)

    # Ordenar por total ventas
    resultado = resultado.sort_values('total_ventas', ascending=False)

    return resultado.reset_index()


# Prueba
resultado = agrupar_por_categoria(ventas)
print(resultado)

# Output esperado:
#        categoria  total_ventas  num_transacciones  ticket_promedio  venta_maxima
# 0  Electrónica        2540.0                  3           846.67        1200.0
# 1         Ropa         300.0                  3           100.00         120.0
# 2    Alimentos          63.0                  2            31.50          35.0
```

### Validación

```python
assert resultado['categoria'].iloc[0] == 'Electrónica', "Primera categoría debe ser Electrónica"
assert resultado['total_ventas'].iloc[0] == 2540.0, "Total ventas incorrecto"
print("✅ Ejercicio 5 correcto")
```

---

## Ejercicio 6: Transformación con Apply ⭐⭐

### Enunciado

Crea funciones para categorizar clientes basándose en múltiples factores:
- Calcula `categoria_edad`: 'Joven' (<30), 'Adulto' (30-50), 'Senior' (>50)
- Calcula `nivel_gasto`: 'Bajo' (<500), 'Medio' (500-2000), 'Alto' (>2000)
- Calcula `puntuacion_fidelidad` basado en años como cliente y gasto total

### Datos de Entrada

```python
clientes = pd.DataFrame({
    'cliente_id': [1, 2, 3, 4, 5],
    'edad': [25, 35, 52, 28, 45],
    'gasto_total': [350, 1500, 5000, 800, 400],
    'años_cliente': [1, 3, 10, 2, 5]
})
```

### Solución

```python
def categorizar_edad(edad: int) -> str:
    """Categoriza edad."""
    if edad < 30:
        return 'Joven'
    elif edad <= 50:
        return 'Adulto'
    else:
        return 'Senior'


def categorizar_gasto(gasto: float) -> str:
    """Categoriza nivel de gasto."""
    if gasto < 500:
        return 'Bajo'
    elif gasto <= 2000:
        return 'Medio'
    else:
        return 'Alto'


def calcular_puntuacion_fidelidad(row: pd.Series) -> float:
    """
    Calcula puntuación de fidelidad.
    Fórmula: (años_cliente * 10) + (gasto_total / 100)
    """
    return (row['años_cliente'] * 10) + (row['gasto_total'] / 100)


def enriquecer_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece datos de clientes con categorías y métricas.

    Args:
        df: DataFrame con datos de clientes

    Returns:
        DataFrame enriquecido
    """
    df_enriquecido = df.copy()

    # Aplicar categorizaciones
    df_enriquecido['categoria_edad'] = df_enriquecido['edad'].apply(categorizar_edad)
    df_enriquecido['nivel_gasto'] = df_enriquecido['gasto_total'].apply(categorizar_gasto)
    df_enriquecido['puntuacion_fidelidad'] = df_enriquecido.apply(
        calcular_puntuacion_fidelidad,
        axis=1
    ).round(2)

    return df_enriquecido


# Prueba
resultado = enriquecer_clientes(clientes)
print(resultado)

# Output esperado:
#    cliente_id  edad  gasto_total  años_cliente categoria_edad nivel_gasto  puntuacion_fidelidad
# 0           1    25          350             1         Joven        Bajo                 13.50
# 1           2    35         1500             3        Adulto       Medio                 45.00
# 2           3    52         5000            10        Senior        Alto                150.00
# 3           4    28          800             2         Joven       Medio                 28.00
# 4           5    45          400             5        Adulto        Bajo                 54.00
```

### Validación

```python
assert 'categoria_edad' in resultado.columns, "Falta columna categoria_edad"
assert resultado['categoria_edad'].iloc[0] == 'Joven', "Categoría edad incorrecta"
assert resultado['puntuacion_fidelidad'].iloc[2] == 150.0, "Puntuación incorrecta"
print("✅ Ejercicio 6 correcto")
```

---

## Ejercicio 7: Merge de DataFrames ⭐⭐

### Enunciado

Tienes dos DataFrames: `pedidos` y `productos`. Realiza un merge para obtener:
- Todos los pedidos con información del producto
- Calcula el `total` (cantidad × precio)
- Identifica pedidos de productos que ya no existen (marca con flag `producto_existe`)

### Datos de Entrada

```python
pedidos = pd.DataFrame({
    'pedido_id': [1, 2, 3, 4, 5],
    'producto_id': [101, 102, 103, 104, 102],
    'cantidad': [2, 1, 5, 3, 2]
})

productos = pd.DataFrame({
    'producto_id': [101, 102, 103],
    'nombre': ['Laptop', 'Mouse', 'Teclado'],
    'precio': [850, 25, 75]
})
```

### Solución

```python
def unir_pedidos_productos(
    pedidos: pd.DataFrame,
    productos: pd.DataFrame
) -> pd.DataFrame:
    """
    Une pedidos con productos y calcula totales.

    Args:
        pedidos: DataFrame de pedidos
        productos: DataFrame de productos

    Returns:
        DataFrame unificado con cálculos
    """
    # LEFT JOIN para mantener todos los pedidos
    df_merged = pd.merge(
        pedidos,
        productos,
        on='producto_id',
        how='left',
        indicator=True  # Agrega columna _merge para validar
    )

    # Crear flag de existencia
    df_merged['producto_existe'] = df_merged['_merge'] == 'both'

    # Calcular total (manejar productos inexistentes)
    df_merged['total'] = df_merged['cantidad'] * df_merged['precio']
    df_merged['total'] = df_merged['total'].fillna(0)

    # Rellenar nombres de productos inexistentes
    df_merged['nombre'] = df_merged['nombre'].fillna('PRODUCTO INEXISTENTE')
    df_merged['precio'] = df_merged['precio'].fillna(0)

    # Limpiar columna auxiliar
    df_merged = df_merged.drop('_merge', axis=1)

    return df_merged


# Prueba
resultado = unir_pedidos_productos(pedidos, productos)
print(resultado)

# Output esperado:
#    pedido_id  producto_id  cantidad             nombre  precio   total  producto_existe
# 0          1          101         2             Laptop   850.0  1700.0             True
# 1          2          102         1              Mouse    25.0    25.0             True
# 2          3          103         5            Teclado    75.0   375.0             True
# 3          4          104         3  PRODUCTO INEXISTENTE  0.0     0.0            False
# 4          5          102         2              Mouse    25.0    50.0             True
```

### Validación

```python
assert len(resultado) == 5, "Deben ser 5 pedidos"
assert resultado['producto_existe'].sum() == 4, "4 productos deben existir"
assert resultado['total'].iloc[3] == 0, "Producto inexistente debe tener total 0"
print("✅ Ejercicio 7 correcto")
```

---

## Ejercicio 8: GroupBy con Múltiples Agregaciones ⭐⭐

### Enunciado

Agrupa las ventas por `vendedor` y `categoria`, calculando:
- Número de ventas
- Total de ingresos
- Ticket promedio
- Desviación estándar de ventas

Luego, encuentra el top vendedor por cada categoría.

### Datos de Entrada

```python
ventas = pd.DataFrame({
    'vendedor': ['Ana', 'Carlos', 'Ana', 'Maria', 'Carlos', 'Ana', 'Maria', 'Carlos'],
    'categoria': ['Electrónica', 'Electrónica', 'Ropa', 'Electrónica',
                  'Ropa', 'Electrónica', 'Ropa', 'Ropa'],
    'monto': [1200, 850, 120, 950, 85, 1100, 145, 95]
})
```

### Solución

```python
def analizar_ventas_vendedor_categoria(df: pd.DataFrame) -> tuple:
    """
    Analiza ventas por vendedor y categoría.

    Args:
        df: DataFrame con ventas

    Returns:
        Tupla con (agregado_completo, top_por_categoria)
    """
    # Agregación completa
    agregado = df.groupby(['vendedor', 'categoria']).agg(
        num_ventas=('monto', 'count'),
        total_ingresos=('monto', 'sum'),
        ticket_promedio=('monto', 'mean'),
        std_ventas=('monto', 'std')
    ).round(2).reset_index()

    # Top vendedor por categoría
    top_por_categoria = agregado.loc[
        agregado.groupby('categoria')['total_ingresos'].idxmax()
    ]

    return agregado, top_por_categoria


# Prueba
agregado, top_vendedores = analizar_ventas_vendedor_categoria(ventas)

print("AGREGADO COMPLETO:")
print(agregado)

print("\nTOP VENDEDOR POR CATEGORÍA:")
print(top_vendedores)

# Output esperado top:
#   vendedor     categoria  num_ventas  total_ingresos  ticket_promedio  std_ventas
# 0      Ana  Electrónica           2          2300.0          1150.00       70.71
# 3    Maria          Ropa           2           145.0            72.50       14.14
```

### Validación

```python
assert len(top_vendedores) == 2, "Debe haber 2 categorías"
assert 'Ana' in top_vendedores['vendedor'].values, "Ana debe ser top en Electrónica"
print("✅ Ejercicio 8 correcto")
```

---

## Ejercicio 9: Pivot Table ⭐⭐

### Enunciado

Crea una tabla dinámica que muestre las ventas mensuales por producto.
- Filas: productos
- Columnas: meses
- Valores: suma de ventas
- Agrega una columna `TOTAL` con la suma por producto

### Datos de Entrada

```python
ventas = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Laptop', 'Teclado', 'Mouse', 'Laptop', 'Teclado', 'Mouse'],
    'mes': ['Enero', 'Enero', 'Febrero', 'Enero', 'Febrero', 'Marzo', 'Febrero', 'Marzo'],
    'ventas': [1200, 50, 1150, 75, 60, 1300, 80, 55]
})
```

### Solución

```python
def crear_pivot_ventas_mensuales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea tabla dinámica de ventas mensuales.

    Args:
        df: DataFrame con ventas

    Returns:
        DataFrame pivotado con totales
    """
    # Crear pivot table
    pivot = pd.pivot_table(
        df,
        values='ventas',
        index='producto',
        columns='mes',
        aggfunc='sum',
        fill_value=0
    )

    # Agregar columna de total
    pivot['TOTAL'] = pivot.sum(axis=1)

    # Agregar fila de total
    pivot.loc['TOTAL'] = pivot.sum()

    return pivot


# Prueba
resultado = crear_pivot_ventas_mensuales(ventas)
print(resultado)

# Output esperado:
# mes         Enero  Febrero  Marzo   TOTAL
# producto
# Laptop       1200     1150   1300  3650.0
# Mouse          50       60     55   165.0
# Teclado        75       80      0   155.0
# TOTAL        1325     1290   1355  3970.0
```

### Validación

```python
assert 'TOTAL' in resultado.columns, "Debe tener columna TOTAL"
assert 'TOTAL' in resultado.index, "Debe tener fila TOTAL"
assert resultado.loc['Laptop', 'TOTAL'] == 3650.0, "Total de Laptop incorrecto"
print("✅ Ejercicio 9 correcto")
```

---

## Ejercicio 10: Detección de Duplicados Complejos ⭐⭐

### Enunciado

Detecta y elimina duplicados "lógicos" en una tabla de transacciones donde se consideran duplicados si tienen:
- Mismo `cliente_id`
- Mismo `producto_id`
- Misma `fecha`
- Diferencia de `monto` menor al 1%

Mantén el registro con el `monto` más alto.

### Datos de Entrada

```python
transacciones = pd.DataFrame({
    'trans_id': [1, 2, 3, 4, 5, 6],
    'cliente_id': [101, 101, 102, 101, 103, 102],
    'producto_id': [201, 201, 202, 203, 201, 202],
    'fecha': ['2024-01-15', '2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-16'],
    'monto': [100.0, 100.5, 50.0, 75.0, 200.0, 50.2]
})
```

### Solución

```python
def eliminar_duplicados_logicos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina duplicados lógicos basados en reglas de negocio.

    Args:
        df: DataFrame con transacciones

    Returns:
        DataFrame sin duplicados lógicos
    """
    df_sorted = df.copy()

    # Convertir fecha a datetime
    df_sorted['fecha'] = pd.to_datetime(df_sorted['fecha'])

    # Ordenar por monto descendente para mantener el más alto
    df_sorted = df_sorted.sort_values('monto', ascending=False)

    # Identificar grupos potencialmente duplicados
    columnas_agrupacion = ['cliente_id', 'producto_id', 'fecha']

    # Función para verificar si son duplicados lógicos
    def son_duplicados_logicos(grupo):
        if len(grupo) == 1:
            return grupo

        # Tomar el primero (mayor monto) como referencia
        referencia = grupo.iloc[0]
        filas_mantener = [True]  # Mantener la referencia

        # Comparar el resto con la referencia
        for idx in range(1, len(grupo)):
            fila_actual = grupo.iloc[idx]
            diferencia_pct = abs(fila_actual['monto'] - referencia['monto']) / referencia['monto'] * 100

            # Si la diferencia es < 1%, es duplicado
            if diferencia_pct < 1:
                filas_mantener.append(False)
            else:
                filas_mantener.append(True)

        return grupo[filas_mantener]

    # Aplicar la lógica por grupo
    df_sin_duplicados = df_sorted.groupby(columnas_agrupacion, group_keys=False).apply(
        son_duplicados_logicos
    ).reset_index(drop=True)

    # Ordenar por trans_id original
    df_sin_duplicados = df_sin_duplicados.sort_values('trans_id').reset_index(drop=True)

    return df_sin_duplicados


# Prueba
resultado = eliminar_duplicados_logicos(transacciones)
print("TRANSACCIONES ORIGINALES:")
print(transacciones)
print(f"\nTRANSACCIONES SIN DUPLICADOS LÓGICOS:")
print(resultado)
print(f"\nEliminadas: {len(transacciones) - len(resultado)} transacciones")

# Output esperado: trans_id 1 eliminado (duplicado lógico de 2)
# trans_id 6 mantenido (diferencia > 1% con trans 3)
```

### Validación

```python
assert len(resultado) == 5, "Debe eliminar 1 transacción"
assert 1 not in resultado['trans_id'].values, "trans_id 1 debe eliminarse"
assert 2 in resultado['trans_id'].values, "trans_id 2 debe mantenerse"
print("✅ Ejercicio 10 correcto")
```

---

## Ejercicio 11: Pipeline de Limpieza Completo ⭐⭐⭐

### Enunciado

Implementa un pipeline de limpieza completo que:
1. Elimine duplicados completos
2. Maneje valores nulos estratégicamente
3. Valide y convierta tipos de datos
4. Normalice texto
5. Valide rangos de valores (precio > 0, edad entre 18-100)
6. Cree un reporte de la limpieza

### Datos de Entrada

```python
datos_raw = pd.DataFrame({
    'id': [1, 2, 2, 3, 4, None, 6, 7],
    'nombre': ['  Juan  ', 'MARIA', 'MARIA', 'Ana', None, 'Pedro', 'Laura', 'Carlos'],
    'edad': ['25', '150', '150', '28', '45', '30', 'invalid', '35'],
    'email': ['juan@test.com', 'MARIA@test.COM', 'MARIA@test.COM',
              'ana@test.com', 'pedro@test', None, 'laura@test.com', 'carlos@test.com'],
    'precio': [100, -50, -50, 250, 300, 450, 75, None]
})
```

### Solución

```python
from typing import Dict

def pipeline_limpieza_completo(df: pd.DataFrame) -> tuple:
    """
    Pipeline completo de limpieza de datos.

    Args:
        df: DataFrame crudo

    Returns:
        Tupla (DataFrame limpio, reporte de limpieza)
    """
    reporte = {
        'filas_iniciales': len(df),
        'columnas_iniciales': len(df.columns)
    }

    df_clean = df.copy()

    # 1. Eliminar duplicados completos
    duplicados = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    reporte['duplicados_eliminados'] = duplicados

    # 2. Eliminar filas sin ID
    sin_id = df_clean['id'].isnull().sum()
    df_clean = df_clean.dropna(subset=['id'])
    reporte['filas_sin_id'] = sin_id

    # 3. Manejar valores nulos
    df_clean['nombre'] = df_clean['nombre'].fillna('Desconocido')
    df_clean['email'] = df_clean['email'].fillna('sin_email@ejemplo.com')

    # 4. Normalizar texto
    df_clean['nombre'] = df_clean['nombre'].str.strip().str.title()
    df_clean['email'] = df_clean['email'].str.lower().str.strip()

    # 5. Validar y convertir tipos
    # Edad: convertir a numérico
    df_clean['edad'] = pd.to_numeric(df_clean['edad'], errors='coerce')

    # Validar rango de edad
    edad_invalidas = ((df_clean['edad'] < 18) | (df_clean['edad'] > 100)).sum()
    df_clean.loc[(df_clean['edad'] < 18) | (df_clean['edad'] > 100), 'edad'] = None

    # Rellenar edades inválidas con mediana
    edad_mediana = df_clean['edad'].median()
    df_clean['edad'] = df_clean['edad'].fillna(edad_mediana).astype(int)
    reporte['edades_corregidas'] = edad_invalidas

    # Precio: validar que sea positivo
    df_clean['precio'] = pd.to_numeric(df_clean['precio'], errors='coerce')
    precios_negativos = (df_clean['precio'] < 0).sum()
    df_clean.loc[df_clean['precio'] < 0, 'precio'] = None
    df_clean['precio'] = df_clean['precio'].fillna(df_clean['precio'].median())
    reporte['precios_corregidos'] = precios_negativos

    # 6. Validar emails (debe tener @ y .)
    def es_email_valido(email: str) -> bool:
        return '@' in email and '.' in email.split('@')[1]

    df_clean['email_valido'] = df_clean['email'].apply(es_email_valido)
    reporte['emails_invalidos'] = (~df_clean['email_valido']).sum()

    # 7. Convertir ID a entero
    df_clean['id'] = df_clean['id'].astype(int)

    # Estadísticas finales
    reporte['filas_finales'] = len(df_clean)
    reporte['columnas_finales'] = len(df_clean.columns)
    reporte['tasa_retencion'] = (reporte['filas_finales'] / reporte['filas_iniciales']) * 100

    return df_clean, reporte


# Prueba
df_limpio, reporte = pipeline_limpieza_completo(datos_raw)

print("DATOS LIMPIOS:")
print(df_limpio)

print("\nREPORTE DE LIMPIEZA:")
for clave, valor in reporte.items():
    if isinstance(valor, float):
        print(f"  {clave}: {valor:.2f}")
    else:
        print(f"  {clave}: {valor}")
```

### Validación

```python
assert len(df_limpio) == 6, "Deben quedar 6 filas"
assert df_limpio['edad'].min() >= 18, "Todas las edades deben ser >= 18"
assert df_limpio['precio'].min() > 0, "Todos los precios deben ser positivos"
assert reporte['duplicados_eliminados'] == 1, "Debe eliminar 1 duplicado"
print("✅ Ejercicio 11 correcto")
```

---

## Ejercicio 12: Cálculo de Métricas Rolling ⭐⭐⭐

### Enunciado

Calcula métricas móviles (rolling) para una serie temporal de ventas:
- Media móvil de 7 días
- Media móvil de 30 días
- Desviación estándar móvil de 7 días
- Crecimiento porcentual respecto al día anterior

### Datos de Entrada

```python
import numpy as np

np.random.seed(42)
fechas = pd.date_range('2024-01-01', periods=60, freq='D')
ventas_diarias = pd.DataFrame({
    'fecha': fechas,
    'ventas': np.random.randint(100, 1000, 60) + np.sin(np.arange(60) * 0.5) * 200
})
```

### Solución

```python
def calcular_metricas_rolling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas rolling para serie temporal.

    Args:
        df: DataFrame con fecha y ventas

    Returns:
        DataFrame con métricas rolling
    """
    df_metricas = df.copy()

    # Asegurar que fecha sea índice
    df_metricas = df_metricas.set_index('fecha')

    # Media móvil 7 días
    df_metricas['ma_7'] = df_metricas['ventas'].rolling(window=7).mean().round(2)

    # Media móvil 30 días
    df_metricas['ma_30'] = df_metricas['ventas'].rolling(window=30).mean().round(2)

    # Desviación estándar móvil 7 días
    df_metricas['std_7'] = df_metricas['ventas'].rolling(window=7).std().round(2)

    # Crecimiento porcentual día anterior
    df_metricas['crecimiento_pct'] = df_metricas['ventas'].pct_change() * 100
    df_metricas['crecimiento_pct'] = df_metricas['crecimiento_pct'].round(2)

    # Indicador: ventas por encima de MA7
    df_metricas['por_encima_ma7'] = df_metricas['ventas'] > df_metricas['ma_7']

    # Máximo móvil 7 días
    df_metricas['max_7'] = df_metricas['ventas'].rolling(window=7).max()

    # Mínimo móvil 7 días
    df_metricas['min_7'] = df_metricas['ventas'].rolling(window=7).min()

    return df_metricas.reset_index()


# Prueba
resultado = calcular_metricas_rolling(ventas_diarias)

print("MÉTRICAS ROLLING (últimos 10 días):")
columnas_mostrar = ['fecha', 'ventas', 'ma_7', 'ma_30', 'std_7', 'crecimiento_pct']
print(resultado[columnas_mostrar].tail(10))
```

### Validación

```python
assert 'ma_7' in resultado.columns, "Falta media móvil 7 días"
assert resultado['ma_7'].notna().sum() == len(resultado) - 6, "MA7 debe tener 6 NaN iniciales"
assert 'crecimiento_pct' in resultado.columns, "Falta crecimiento porcentual"
print("✅ Ejercicio 12 correcto")
```

---

## Ejercicio 13: Transformación Condicional Compleja ⭐⭐⭐

### Enunciado

Implementa una función que calcule el precio final de productos basándose en reglas complejas:
- Descuento base según categoría: Electrónica (10%), Ropa (15%), Otros (5%)
- Descuento adicional si stock > 100: +5%
- Descuento adicional si es temporada (True): +10%
- Si el precio final < costo, ajustar a costo + 10%
- Calcular margen de beneficio porcentual

### Datos de Entrada

```python
productos = pd.DataFrame({
    'producto_id': [1, 2, 3, 4, 5, 6],
    'nombre': ['Laptop', 'Camisa', 'Mouse', 'Pantalón', 'Monitor', 'Zapatos'],
    'categoria': ['Electrónica', 'Ropa', 'Electrónica', 'Ropa', 'Electrónica', 'Ropa'],
    'precio_base': [1000, 50, 25, 80, 350, 120],
    'costo': [700, 20, 10, 30, 200, 50],
    'stock': [50, 150, 200, 80, 120, 90],
    'temporada': [False, True, True, True, False, True]
})
```

### Solución

```python
def calcular_precio_final_complejo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula precio final con múltiples reglas de descuento.

    Args:
        df: DataFrame con productos

    Returns:
        DataFrame con precios calculados
    """
    df_precios = df.copy()

    # 1. Descuento base según categoría
    descuento_categoria = {
        'Electrónica': 0.10,
        'Ropa': 0.15,
        'Otros': 0.05
    }

    df_precios['descuento_base'] = df_precios['categoria'].map(
        descuento_categoria
    ).fillna(0.05)

    # 2. Descuento adicional por stock alto
    df_precios['descuento_stock'] = (df_precios['stock'] > 100).astype(int) * 0.05

    # 3. Descuento por temporada
    df_precios['descuento_temporada'] = df_precios['temporada'].astype(int) * 0.10

    # 4. Calcular descuento total
    df_precios['descuento_total'] = (
        df_precios['descuento_base'] +
        df_precios['descuento_stock'] +
        df_precios['descuento_temporada']
    )

    # 5. Aplicar descuento
    df_precios['precio_con_descuento'] = (
        df_precios['precio_base'] * (1 - df_precios['descuento_total'])
    )

    # 6. Validar que no sea menor que costo + 10%
    precio_minimo = df_precios['costo'] * 1.10
    df_precios['precio_final'] = df_precios[['precio_con_descuento', precio_minimo]].max(axis=1)

    # 7. Marcar si se ajustó el precio
    df_precios['precio_ajustado'] = (
        df_precios['precio_final'] > df_precios['precio_con_descuento']
    )

    # 8. Calcular margen de beneficio
    df_precios['margen_pct'] = (
        (df_precios['precio_final'] - df_precios['costo']) / df_precios['precio_final'] * 100
    ).round(2)

    # 9. Calcular ahorro para el cliente
    df_precios['ahorro'] = df_precios['precio_base'] - df_precios['precio_final']
    df_precios['ahorro_pct'] = (
        df_precios['ahorro'] / df_precios['precio_base'] * 100
    ).round(2)

    # Redondear precios
    df_precios['precio_final'] = df_precios['precio_final'].round(2)

    return df_precios


# Prueba
resultado = calcular_precio_final_complejo(productos)

columnas_mostrar = [
    'nombre', 'categoria', 'precio_base', 'descuento_total',
    'precio_final', 'margen_pct', 'precio_ajustado'
]
print(resultado[columnas_mostrar])
```

### Validación

```python
assert all(resultado['precio_final'] >= resultado['costo'] * 1.10), "Precio no debe ser menor a costo + 10%"
assert all(resultado['margen_pct'] >= 10), "Margen debe ser al menos 10%"
assert 'ahorro_pct' in resultado.columns, "Falta columna de ahorro porcentual"
print("✅ Ejercicio 13 correcto")
```

---

## Ejercicio 14: Merge Múltiple con Validación ⭐⭐⭐

### Enunciado

Realiza un merge de 4 tablas (pedidos, clientes, productos, envíos) con validaciones:
1. Verifica que no se dupliquen filas inesperadamente
2. Identifica pedidos sin cliente, producto o envío
3. Calcula métricas agregadas
4. Genera reporte de calidad del merge

### Datos de Entrada

```python
pedidos = pd.DataFrame({
    'pedido_id': [1, 2, 3, 4, 5],
    'cliente_id': [101, 102, 103, 999, 101],  # 999 no existe
    'producto_id': [201, 202, 203, 201, 888],  # 888 no existe
    'cantidad': [2, 1, 3, 5, 2]
})

clientes = pd.DataFrame({
    'cliente_id': [101, 102, 103],
    'nombre': ['Ana', 'Carlos', 'María'],
    'segmento': ['Premium', 'Standard', 'Premium']
})

productos = pd.DataFrame({
    'producto_id': [201, 202, 203],
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'precio': [1000, 25, 75]
})

envios = pd.DataFrame({
    'pedido_id': [1, 2, 3],  # Pedidos 4 y 5 sin envío
    'fecha_envio': ['2024-01-15', '2024-01-16', '2024-01-17'],
    'estado': ['Entregado', 'En tránsito', 'Entregado']
})
```

### Solución

```python
def merge_multiple_con_validacion(
    pedidos: pd.DataFrame,
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    envios: pd.DataFrame
) -> tuple:
    """
    Merge múltiple con validaciones exhaustivas.

    Args:
        pedidos, clientes, productos, envios: DataFrames a unir

    Returns:
        Tupla (DataFrame unificado, reporte de calidad)
    """
    reporte = {}

    # Registros iniciales
    reporte['pedidos_iniciales'] = len(pedidos)

    # MERGE 1: Pedidos + Clientes
    df = pd.merge(
        pedidos,
        clientes,
        on='cliente_id',
        how='left',
        indicator='_merge_cliente'
    )

    pedidos_sin_cliente = (df['_merge_cliente'] == 'left_only').sum()
    reporte['pedidos_sin_cliente'] = pedidos_sin_cliente

    # MERGE 2: + Productos
    df = pd.merge(
        df,
        productos,
        on='producto_id',
        how='left',
        indicator='_merge_producto'
    )

    pedidos_sin_producto = (df['_merge_producto'] == 'left_only').sum()
    reporte['pedidos_sin_producto'] = pedidos_sin_producto

    # MERGE 3: + Envíos
    df = pd.merge(
        df,
        envios,
        on='pedido_id',
        how='left',
        indicator='_merge_envio'
    )

    pedidos_sin_envio = (df['_merge_envio'] == 'left_only').sum()
    reporte['pedidos_sin_envio'] = pedidos_sin_envio

    # VALIDACIONES
    # 1. Verificar duplicados
    duplicados = df.duplicated(subset=['pedido_id']).sum()
    reporte['pedidos_duplicados'] = duplicados

    if duplicados > 0:
        raise ValueError(f"¡ADVERTENCIA! {duplicados} pedidos duplicados después del merge")

    # 2. Calcular total
    df['total'] = df['cantidad'] * df['precio']

    # 3. Crear flags de problemas
    df['tiene_cliente'] = df['_merge_cliente'] == 'both'
    df['tiene_producto'] = df['_merge_producto'] == 'both'
    df['tiene_envio'] = df['_merge_envio'] == 'both'
    df['pedido_completo'] = df['tiene_cliente'] & df['tiene_producto']

    # 4. Métricas de calidad
    reporte['pedidos_finales'] = len(df)
    reporte['pedidos_completos'] = df['pedido_completo'].sum()
    reporte['pedidos_con_problemas'] = len(df) - df['pedido_completo'].sum()
    reporte['tasa_completitud'] = (df['pedido_completo'].sum() / len(df)) * 100

    # 5. Métricas de negocio (solo pedidos válidos)
    df_validos = df[df['pedido_completo']]
    if len(df_validos) > 0:
        reporte['revenue_total'] = df_validos['total'].sum()
        reporte['ticket_promedio'] = df_validos['total'].mean()
        reporte['pedidos_entregados'] = (df_validos['estado'] == 'Entregado').sum()
    else:
        reporte['revenue_total'] = 0
        reporte['ticket_promedio'] = 0
        reporte['pedidos_entregados'] = 0

    # Limpiar columnas auxiliares
    df = df.drop(['_merge_cliente', '_merge_producto', '_merge_envio'], axis=1)

    return df, reporte


# Prueba
df_unificado, reporte_calidad = merge_multiple_con_validacion(
    pedidos, clientes, productos, envios
)

print("DATASET UNIFICADO:")
columnas_mostrar = [
    'pedido_id', 'nombre', 'producto', 'cantidad', 'total',
    'tiene_cliente', 'tiene_producto', 'tiene_envio', 'pedido_completo'
]
print(df_unificado[columnas_mostrar])

print("\nREPORTE DE CALIDAD DEL MERGE:")
for clave, valor in reporte_calidad.items():
    if isinstance(valor, float):
        print(f"  {clave}: {valor:.2f}")
    else:
        print(f"  {clave}: {valor}")

# Identificar problemas
print("\nPEDIDOS CON PROBLEMAS:")
problemas = df_unificado[~df_unificado['pedido_completo']]
if len(problemas) > 0:
    print(problemas[['pedido_id', 'cliente_id', 'producto_id', 'tiene_cliente', 'tiene_producto']])
else:
    print("  No hay pedidos con problemas")
```

### Validación

```python
assert reporte_calidad['pedidos_sin_cliente'] == 1, "Debe haber 1 pedido sin cliente"
assert reporte_calidad['pedidos_sin_producto'] == 1, "Debe haber 1 pedido sin producto"
assert reporte_calidad['pedidos_sin_envio'] == 2, "Deben haber 2 pedidos sin envío"
assert reporte_calidad['pedidos_duplicados'] == 0, "No debe haber duplicados"
print("✅ Ejercicio 14 correcto")
```

---

## Ejercicio 15: Optimización de Performance ⭐⭐⭐

### Enunciado

Tienes un DataFrame grande y necesitas optimizar su procesamiento. Implementa:
1. Optimización de tipos de datos
2. Uso de operaciones vectorizadas en lugar de apply
3. Procesamiento en chunks
4. Comparación de tiempos de ejecución

### Datos de Entrada

```python
import numpy as np
import time

np.random.seed(42)
n = 100000

df_grande = pd.DataFrame({
    'id': range(1, n + 1),
    'categoria': np.random.choice(['A', 'B', 'C', 'D'], n),
    'valor1': np.random.randint(1, 1000, n),
    'valor2': np.random.randint(1, 1000, n),
    'texto': [f'TEXTO_{i}' for i in range(n)]
})
```

### Solución

```python
def version_lenta(df: pd.DataFrame) -> pd.DataFrame:
    """Versión NO optimizada (para comparación)."""
    df_result = df.copy()

    # Usar apply (lento)
    df_result['suma'] = df_result.apply(lambda row: row['valor1'] + row['valor2'], axis=1)
    df_result['producto'] = df_result.apply(lambda row: row['valor1'] * row['valor2'], axis=1)
    df_result['ratio'] = df_result.apply(
        lambda row: row['valor1'] / row['valor2'] if row['valor2'] != 0 else 0,
        axis=1
    )

    return df_result


def version_optimizada(df: pd.DataFrame) -> pd.DataFrame:
    """Versión optimizada con vectorización."""
    df_result = df.copy()

    # Operaciones vectorizadas (rápido)
    df_result['suma'] = df_result['valor1'] + df_result['valor2']
    df_result['producto'] = df_result['valor1'] * df_result['valor2']
    df_result['ratio'] = df_result['valor1'] / df_result['valor2'].replace(0, 1)

    return df_result


def optimizar_tipos_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Optimiza los tipos de datos para reducir memoria."""
    df_optimizado = df.copy()

    # Optimizar enteros
    df_optimizado['id'] = df_optimizado['id'].astype('int32')
    df_optimizado['valor1'] = df_optimizado['valor1'].astype('int16')
    df_optimizado['valor2'] = df_optimizado['valor2'].astype('int16')

    # Optimizar strings repetidos con category
    df_optimizado['categoria'] = df_optimizado['categoria'].astype('category')

    return df_optimizado


def procesar_en_chunks(df: pd.DataFrame, chunk_size: int = 10000) -> pd.DataFrame:
    """Procesa DataFrame grande en chunks."""
    chunks_procesados = []

    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end].copy()

        # Procesar chunk
        chunk['suma'] = chunk['valor1'] + chunk['valor2']
        chunk['producto'] = chunk['valor1'] * chunk['valor2']

        chunks_procesados.append(chunk)

    return pd.concat(chunks_procesados, ignore_index=True)


def comparar_performance(df: pd.DataFrame) -> dict:
    """Compara diferentes enfoques de optimización."""
    resultados = {}

    # Tamaño original
    memoria_original = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    resultados['memoria_original_mb'] = round(memoria_original, 2)

    # Optimizar tipos
    df_optimizado = optimizar_tipos_datos(df)
    memoria_optimizada = df_optimizado.memory_usage(deep=True).sum() / 1024 / 1024
    resultados['memoria_optimizada_mb'] = round(memoria_optimizada, 2)
    resultados['ahorro_memoria_pct'] = round(
        ((memoria_original - memoria_optimizada) / memoria_original) * 100, 2
    )

    # Medir tiempo versión lenta (solo con subset)
    df_sample = df.head(1000)
    inicio = time.time()
    _ = version_lenta(df_sample)
    tiempo_lento = time.time() - inicio
    resultados['tiempo_lento_1k_filas'] = round(tiempo_lento, 4)

    # Medir tiempo versión optimizada
    inicio = time.time()
    _ = version_optimizada(df_sample)
    tiempo_rapido = time.time() - inicio
    resultados['tiempo_rapido_1k_filas'] = round(tiempo_rapido, 4)

    # Mejora de velocidad
    resultados['mejora_velocidad_x'] = round(tiempo_lento / tiempo_rapido, 2)

    # Procesar en chunks todo el dataset
    inicio = time.time()
    _ = procesar_en_chunks(df_optimizado, chunk_size=10000)
    tiempo_chunks = time.time() - inicio
    resultados['tiempo_chunks_total'] = round(tiempo_chunks, 4)

    return resultados


# Prueba
print("Comparando enfoques de optimización...")
print("(Esto puede tomar unos segundos...)\n")

resultados = comparar_performance(df_grande)

print("RESULTADOS DE OPTIMIZACIÓN:")
print("=" * 60)
for clave, valor in resultados.items():
    print(f"  {clave}: {valor}")

print("\n📊 CONCLUSIONES:")
print(f"  - Ahorro de memoria: {resultados['ahorro_memoria_pct']}%")
print(f"  - Vectorización es {resultados['mejora_velocidad_x']}x más rápida")
print(f"  - Procesamiento de 100k filas en chunks: {resultados['tiempo_chunks_total']}s")
```

### Validación

```python
assert resultados['ahorro_memoria_pct'] > 0, "Debe haber ahorro de memoria"
assert resultados['mejora_velocidad_x'] > 1, "Vectorización debe ser más rápida"
print("✅ Ejercicio 15 correcto")
```

---

## 📝 Resumen y Siguientes Pasos

¡Felicidades! Has completado 15 ejercicios de transformación con Pandas que cubren:

### Habilidades Adquiridas ✅

- ⭐ **Básico**: Filtrado, cálculos, nulos, texto, groupby
- ⭐⭐ **Intermedio**: Apply, merges, pivots, duplicados complejos
- ⭐⭐⭐ **Avanzado**: Pipelines, rolling, optimización, validaciones

### Próximos Pasos

1. **Revisa tus soluciones**: Compáralas con las proporcionadas
2. **Experimenta**: Modifica los ejercicios con tus propios datos
3. **Proyecto práctico**: Aplica lo aprendido en `04-proyecto-practico/`
4. **Optimiza**: Intenta mejorar el rendimiento de tus soluciones

### Recursos Adicionales

- Documentación oficial de Pandas: https://pandas.pydata.org/docs/
- Pandas Cheat Sheet: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
- Practice Problems: Kaggle, LeetCode, HackerRank

---

**Tiempo estimado de práctica**: 4-6 horas
**Última actualización**: 2025-10-30
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
