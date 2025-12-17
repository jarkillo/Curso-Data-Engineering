# Ejemplos Prácticos: Transformación con Pandas

**Objetivo**: Aplicar los conceptos de transformación con Pandas en casos reales de Data Engineering.

---

## 📋 Índice de Ejemplos

1. [Limpieza de Datos (nulls, duplicados, tipos)](#ejemplo-1-limpieza-de-datos)
2. [Transformación con Apply y Lambda](#ejemplo-2-transformación-con-apply-y-lambda)
3. [GroupBy y Agregaciones Complejas](#ejemplo-3-groupby-y-agregaciones-complejas)
4. [Merge de Múltiples DataFrames](#ejemplo-4-merge-de-múltiples-dataframes)
5. [Pipeline Completo de Transformación](#ejemplo-5-pipeline-completo-de-transformación)

---

## Ejemplo 1: Limpieza de Datos

### 📖 Contexto

Recibimos datos de clientes de un sistema CRM con problemas de calidad: valores nulos, duplicados, tipos incorrectos y formato inconsistente.

### 🎯 Objetivo

Limpiar los datos para que sean utilizables en análisis y reportes.

### 💻 Código

```python
import pandas as pd
import numpy as np
from typing import Dict, List

def cargar_datos_clientes() -> pd.DataFrame:
    """Simula carga de datos de clientes con problemas de calidad."""
    datos = {
        'cliente_id': [1, 2, 2, 3, 4, 5, 6, None, 8],
        'nombre': ['Juan Pérez', 'MARIA LOPEZ', 'Maria Lopez', 'Ana García',
                   None, 'Pedro Ruiz', 'Laura Martín', 'Carlos Vega', '  Sofia Torres  '],
        'email': ['juan@email.com', 'MARIA@EMAIL.COM', 'maria@email.com',
                  'ana@email.com', 'pedro@invalido', None, 'laura@email.com',
                  'carlos@email.com', 'sofia@email.com'],
        'edad': ['25', '34', '34', '28', '45', 'treinta', '31', '29', '22'],
        'ciudad': ['Madrid', 'madrid', 'Madrid', 'Barcelona', 'Valencia',
                   'Sevilla', None, 'Bilbao', 'Málaga'],
        'fecha_registro': ['2024-01-15', '2024-02-20', '2024-02-20', '2024-03-10',
                          '15/04/2024', '2024-05-22', '2024-06-01', None, '2024-07-18']
    }

    return pd.DataFrame(datos)


def limpiar_datos_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia datos de clientes con validaciones y transformaciones.

    Args:
        df: DataFrame con datos crudos de clientes

    Returns:
        DataFrame limpio y validado
    """
    if df.empty:
        raise ValueError("DataFrame vacío")

    df_limpio = df.copy()

    # 1. MANEJAR DUPLICADOS
    print(f"Filas originales: {len(df_limpio)}")
    print(f"Duplicados encontrados: {df_limpio.duplicated(subset=['cliente_id']).sum()}")

    # Eliminar duplicados basados en cliente_id (mantener el primero)
    df_limpio = df_limpio.drop_duplicates(subset=['cliente_id'], keep='first')
    print(f"Filas después de eliminar duplicados: {len(df_limpio)}")

    # 2. MANEJAR VALORES NULOS
    print(f"\nValores nulos por columna:")
    print(df_limpio.isnull().sum())

    # Eliminar filas sin cliente_id (es clave primaria)
    df_limpio = df_limpio.dropna(subset=['cliente_id'])

    # Rellenar nombres nulos con 'Desconocido'
    df_limpio['nombre'] = df_limpio['nombre'].fillna('Desconocido')

    # Rellenar emails nulos con formato especial
    df_limpio['email'] = df_limpio['email'].fillna('sin_email@desconocido.com')

    # Rellenar ciudades nulas con 'No Especificada'
    df_limpio['ciudad'] = df_limpio['ciudad'].fillna('No Especificada')

    # 3. NORMALIZAR TEXTO
    # Nombres: capitalizar correctamente
    df_limpio['nombre'] = df_limpio['nombre'].str.strip().str.title()

    # Emails: convertir a minúsculas
    df_limpio['email'] = df_limpio['email'].str.lower().str.strip()

    # Ciudades: capitalizar
    df_limpio['ciudad'] = df_limpio['ciudad'].str.strip().str.title()

    # 4. VALIDAR Y CONVERTIR TIPOS DE DATOS
    # Edad: convertir a numérico (valores no numéricos se convierten en NaN)
    df_limpio['edad'] = pd.to_numeric(df_limpio['edad'], errors='coerce')

    # Rellenar edades inválidas con la mediana
    edad_mediana = df_limpio['edad'].median()
    df_limpio['edad'] = df_limpio['edad'].fillna(edad_mediana)

    # Convertir edad a entero
    df_limpio['edad'] = df_limpio['edad'].astype(int)

    # 5. VALIDAR Y ESTANDARIZAR FECHAS
    # Intentar parsear fechas con múltiples formatos
    df_limpio['fecha_registro'] = pd.to_datetime(
        df_limpio['fecha_registro'],
        format='mixed',
        errors='coerce'
    )

    # Rellenar fechas nulas con fecha actual
    df_limpio['fecha_registro'] = df_limpio['fecha_registro'].fillna(pd.Timestamp.now())

    # 6. VALIDACIONES DE NEGOCIO
    # Validar formato de email básico
    def es_email_valido(email: str) -> bool:
        return '@' in email and '.' in email.split('@')[1]

    df_limpio['email_valido'] = df_limpio['email'].apply(es_email_valido)

    # Validar rango de edad
    df_limpio['edad_valida'] = (df_limpio['edad'] >= 18) & (df_limpio['edad'] <= 120)

    # 7. CREAR CLIENTE_ID ENTERO
    df_limpio['cliente_id'] = df_limpio['cliente_id'].astype(int)

    # 8. RESETEAR ÍNDICE
    df_limpio = df_limpio.reset_index(drop=True)

    return df_limpio


def generar_reporte_limpieza(df_original: pd.DataFrame, df_limpio: pd.DataFrame) -> Dict:
    """Genera reporte de la limpieza realizada."""
    reporte = {
        'filas_originales': len(df_original),
        'filas_finales': len(df_limpio),
        'filas_eliminadas': len(df_original) - len(df_limpio),
        'nulos_originales': df_original.isnull().sum().sum(),
        'nulos_finales': df_limpio.isnull().sum().sum(),
        'duplicados_eliminados': df_original.duplicated().sum(),
        'emails_invalidos': (~df_limpio['email_valido']).sum(),
        'edades_invalidas': (~df_limpio['edad_valida']).sum()
    }

    return reporte


# EJECUCIÓN
if __name__ == '__main__':
    # Cargar datos
    df_raw = cargar_datos_clientes()

    print("=" * 60)
    print("DATOS ORIGINALES")
    print("=" * 60)
    print(df_raw)
    print(f"\nTipos de datos:")
    print(df_raw.dtypes)

    # Limpiar datos
    print("\n" + "=" * 60)
    print("PROCESO DE LIMPIEZA")
    print("=" * 60)
    df_clean = limpiar_datos_clientes(df_raw)

    # Mostrar resultado
    print("\n" + "=" * 60)
    print("DATOS LIMPIOS")
    print("=" * 60)
    print(df_clean)
    print(f"\nTipos de datos:")
    print(df_clean.dtypes)

    # Generar reporte
    print("\n" + "=" * 60)
    print("REPORTE DE LIMPIEZA")
    print("=" * 60)
    reporte = generar_reporte_limpieza(df_raw, df_clean)
    for clave, valor in reporte.items():
        print(f"{clave}: {valor}")
```

### 📊 Output Esperado

```
============================================================
DATOS ORIGINALES
============================================================
   cliente_id            nombre              email edad     ciudad fecha_registro
0         1.0       Juan Pérez    juan@email.com   25     Madrid     2024-01-15
1         2.0      MARIA LOPEZ  MARIA@EMAIL.COM   34     madrid     2024-02-20
2         2.0      Maria Lopez   maria@email.com   34     Madrid     2024-02-20
3         3.0       Ana García     ana@email.com   28  Barcelona     2024-03-10
4         4.0              None   pedro@invalido   45   Valencia     15/04/2024
5         5.0       Pedro Ruiz             None treinta   Sevilla     2024-05-22
6         6.0     Laura Martín   laura@email.com   31       None     2024-06-01
7         NaN      Carlos Vega  carlos@email.com   29     Bilbao           None
8         8.0   Sofia Torres    sofia@email.com   22     Málaga     2024-07-18

============================================================
PROCESO DE LIMPIEZA
============================================================
Filas originales: 9
Duplicados encontrados: 1
Filas después de eliminar duplicados: 8
...

============================================================
REPORTE DE LIMPIEZA
============================================================
filas_originales: 9
filas_finales: 7
filas_eliminadas: 2
nulos_originales: 7
nulos_finales: 0
duplicados_eliminados: 1
emails_invalidos: 2
edades_invalidas: 0
```

### 🎓 Conceptos Clave

- ✅ Identificación y eliminación de duplicados
- ✅ Manejo estratégico de valores nulos
- ✅ Normalización de texto (mayúsculas, espacios)
- ✅ Conversión y validación de tipos de datos
- ✅ Parseo de fechas con múltiples formatos
- ✅ Validaciones de negocio personalizadas

---

## Ejemplo 2: Transformación con Apply y Lambda

### 📖 Contexto

Tenemos datos de transacciones bancarias que necesitan ser enriquecidos y categorizados para análisis de fraude.

### 🎯 Objetivo

Aplicar transformaciones complejas usando `apply()` y funciones lambda para extraer información y detectar patrones.

### 💻 Código

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict

def cargar_transacciones() -> pd.DataFrame:
    """Simula carga de transacciones bancarias."""
    np.random.seed(42)

    datos = {
        'transaccion_id': range(1, 21),
        'cliente_id': np.random.randint(100, 110, 20),
        'monto': np.random.uniform(10, 5000, 20).round(2),
        'comercio': [
            'Amazon - Electrónica', 'Mercadona - Supermercado', 'Shell - Gasolina',
            'Zara - Ropa', 'Amazon - Libros', 'Booking.com - Hotel',
            'Netflix - Streaming', 'Uber - Transporte', 'McDonald\'s - Comida',
            'Apple Store - Tecnología', 'Carrefour - Supermercado', 'Repsol - Gasolina',
            'H&M - Ropa', 'Spotify - Música', 'Cabify - Transporte',
            'KFC - Comida', 'Steam - Videojuegos', 'Decathlon - Deportes',
            'IKEA - Muebles', 'Booking.com - Vuelo'
        ],
        'pais': ['ES', 'ES', 'ES', 'ES', 'US', 'FR', 'US', 'ES', 'ES', 'US',
                 'ES', 'ES', 'ES', 'US', 'ES', 'ES', 'US', 'ES', 'ES', 'UK'],
        'hora': [f"{h:02d}:{m:02d}" for h, m in zip(
            np.random.randint(0, 24, 20),
            np.random.randint(0, 60, 20)
        )]
    }

    fechas_base = pd.date_range('2024-01-01', periods=20, freq='D')
    datos['fecha'] = fechas_base

    return pd.DataFrame(datos)


def extraer_categoria_comercio(comercio: str) -> str:
    """Extrae la categoría del nombre del comercio."""
    if ' - ' in comercio:
        return comercio.split(' - ')[1]
    return 'Otros'


def extraer_nombre_comercio(comercio: str) -> str:
    """Extrae el nombre del comercio."""
    if ' - ' in comercio:
        return comercio.split(' - ')[0]
    return comercio


def clasificar_monto(monto: float) -> str:
    """Clasifica el monto de la transacción."""
    if monto < 50:
        return 'Bajo'
    elif monto < 200:
        return 'Medio'
    elif monto < 1000:
        return 'Alto'
    else:
        return 'Muy Alto'


def calcular_riesgo_fraude(row: pd.Series) -> str:
    """Calcula nivel de riesgo de fraude basado en múltiples factores."""
    riesgo_puntos = 0

    # Factor 1: Monto alto
    if row['monto'] > 2000:
        riesgo_puntos += 3
    elif row['monto'] > 1000:
        riesgo_puntos += 2

    # Factor 2: País extranjero
    if row['pais'] != 'ES':
        riesgo_puntos += 2

    # Factor 3: Hora inusual (madrugada)
    hora = int(row['hora'].split(':')[0])
    if hora >= 0 and hora < 6:
        riesgo_puntos += 1

    # Factor 4: Categorías de alto riesgo
    categorias_riesgo = ['Tecnología', 'Electrónica', 'Videojuegos']
    if row['categoria'] in categorias_riesgo and row['monto'] > 500:
        riesgo_puntos += 2

    # Clasificación final
    if riesgo_puntos >= 5:
        return 'Alto'
    elif riesgo_puntos >= 3:
        return 'Medio'
    return 'Bajo'


def es_transaccion_internacional(pais: str) -> bool:
    """Verifica si es transacción internacional."""
    return pais != 'ES'


def enriquecer_transacciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece datos de transacciones con información adicional.

    Args:
        df: DataFrame con transacciones originales

    Returns:
        DataFrame enriquecido con nuevas columnas calculadas
    """
    df_enriquecido = df.copy()

    # 1. EXTRAER INFORMACIÓN CON APPLY
    print("Extrayendo información del comercio...")
    df_enriquecido['nombre_comercio'] = df_enriquecido['comercio'].apply(extraer_nombre_comercio)
    df_enriquecido['categoria'] = df_enriquecido['comercio'].apply(extraer_categoria_comercio)

    # 2. CLASIFICACIONES CON LAMBDA
    print("Clasificando transacciones...")
    df_enriquecido['rango_monto'] = df_enriquecido['monto'].apply(lambda x: clasificar_monto(x))

    # 3. TRANSFORMACIONES SIMPLES CON LAMBDA
    df_enriquecido['es_internacional'] = df_enriquecido['pais'].apply(
        lambda x: es_transaccion_internacional(x)
    )

    # Convertir booleano a texto legible
    df_enriquecido['tipo_transaccion'] = df_enriquecido['es_internacional'].apply(
        lambda x: 'Internacional' if x else 'Nacional'
    )

    # 4. CÁLCULOS COMPLEJOS CON APPLY Y AXIS=1
    print("Calculando riesgo de fraude...")
    df_enriquecido['riesgo_fraude'] = df_enriquecido.apply(calcular_riesgo_fraude, axis=1)

    # 5. TRANSFORMACIONES DE FECHA/HORA
    df_enriquecido['dia_semana'] = df_enriquecido['fecha'].dt.day_name()
    df_enriquecido['es_fin_semana'] = df_enriquecido['fecha'].dt.dayofweek >= 5

    # 6. FORMATEO CON LAMBDA
    df_enriquecido['monto_formateado'] = df_enriquecido['monto'].apply(
        lambda x: f"€{x:,.2f}"
    )

    # 7. CÁLCULOS POR CLIENTE CON TRANSFORM
    df_enriquecido['gasto_promedio_cliente'] = df_enriquecido.groupby('cliente_id')['monto'].transform('mean')
    df_enriquecido['desviacion_gasto'] = df_enriquecido['monto'] - df_enriquecido['gasto_promedio_cliente']

    # 8. INDICADOR DE GASTO ATÍPICO
    df_enriquecido['gasto_atipico'] = df_enriquecido.apply(
        lambda row: abs(row['desviacion_gasto']) > (row['gasto_promedio_cliente'] * 0.5),
        axis=1
    )

    return df_enriquecido


def generar_resumen_enriquecimiento(df_original: pd.DataFrame, df_enriquecido: pd.DataFrame) -> None:
    """Muestra resumen del enriquecimiento realizado."""
    print("\n" + "=" * 80)
    print("RESUMEN DE ENRIQUECIMIENTO")
    print("=" * 80)

    columnas_nuevas = set(df_enriquecido.columns) - set(df_original.columns)
    print(f"Columnas originales: {len(df_original.columns)}")
    print(f"Columnas finales: {len(df_enriquecido.columns)}")
    print(f"Columnas añadidas: {len(columnas_nuevas)}")
    print(f"\nNuevas columnas: {', '.join(sorted(columnas_nuevas))}")

    print(f"\n📊 Distribución de Riesgo de Fraude:")
    print(df_enriquecido['riesgo_fraude'].value_counts())

    print(f"\n📊 Transacciones por Tipo:")
    print(df_enriquecido['tipo_transaccion'].value_counts())

    print(f"\n📊 Transacciones con Gasto Atípico:")
    print(f"Atípicas: {df_enriquecido['gasto_atipico'].sum()}")
    print(f"Normales: {(~df_enriquecido['gasto_atipico']).sum()}")


# EJECUCIÓN
if __name__ == '__main__':
    # Cargar transacciones
    df_transacciones = cargar_transacciones()

    print("=" * 80)
    print("TRANSACCIONES ORIGINALES")
    print("=" * 80)
    print(df_transacciones.head(10))

    # Enriquecer
    print("\n" + "=" * 80)
    print("ENRIQUECIENDO TRANSACCIONES")
    print("=" * 80)
    df_enriquecido = enriquecer_transacciones(df_transacciones)

    # Mostrar resultado
    print("\n" + "=" * 80)
    print("TRANSACCIONES ENRIQUECIDAS")
    print("=" * 80)
    columnas_mostrar = [
        'transaccion_id', 'nombre_comercio', 'categoria', 'monto_formateado',
        'rango_monto', 'tipo_transaccion', 'riesgo_fraude', 'gasto_atipico'
    ]
    print(df_enriquecido[columnas_mostrar].head(10))

    # Resumen
    generar_resumen_enriquecimiento(df_transacciones, df_enriquecido)

    # Casos de alto riesgo
    print("\n" + "=" * 80)
    print("⚠️  TRANSACCIONES DE ALTO RIESGO")
    print("=" * 80)
    alto_riesgo = df_enriquecido[df_enriquecido['riesgo_fraude'] == 'Alto']
    if len(alto_riesgo) > 0:
        print(alto_riesgo[columnas_mostrar])
    else:
        print("No se encontraron transacciones de alto riesgo")
```

### 🎓 Conceptos Clave

- ✅ Uso de `apply()` con funciones personalizadas
- ✅ Funciones lambda para transformaciones rápidas
- ✅ `apply()` con `axis=1` para procesar filas completas
- ✅ `transform()` para mantener dimensionalidad
- ✅ Combinación de múltiples factores en cálculos complejos
- ✅ Extracción y formateo de información

---

## Ejemplo 3: GroupBy y Agregaciones Complejas

### 📖 Contexto

Tenemos datos de ventas de una cadena de tiendas y necesitamos generar reportes analíticos con métricas agregadas.

### 🎯 Objetivo

Dominar GroupBy para crear análisis multidimensionales con agregaciones personalizadas.

### 💻 Código

```python
import pandas as pd
import numpy as np
from typing import Dict, Tuple

def cargar_ventas_tiendas() -> pd.DataFrame:
    """Simula datos de ventas de múltiples tiendas."""
    np.random.seed(42)

    tiendas = ['Madrid Centro', 'Barcelona Diagonal', 'Valencia Puerto',
               'Sevilla Nervión', 'Bilbao Casco']
    productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Impresora',
                 'Webcam', 'Auriculares', 'Tablet']
    vendedores = ['Ana', 'Carlos', 'María', 'Pedro', 'Laura']

    n_ventas = 200

    datos = {
        'venta_id': range(1, n_ventas + 1),
        'tienda': np.random.choice(tiendas, n_ventas),
        'producto': np.random.choice(productos, n_ventas),
        'vendedor': np.random.choice(vendedores, n_ventas),
        'cantidad': np.random.randint(1, 10, n_ventas),
        'precio_unitario': np.random.choice([25, 75, 150, 350, 450, 85, 120, 520], n_ventas),
        'descuento_pct': np.random.choice([0, 5, 10, 15, 20], n_ventas),
        'mes': np.random.choice(['Enero', 'Febrero', 'Marzo', 'Abril'], n_ventas),
        'categoria': np.random.choice(['Entrada', 'Media', 'Alta'], n_ventas)
    }

    df = pd.DataFrame(datos)

    # Calcular campos derivados
    df['subtotal'] = df['cantidad'] * df['precio_unitario']
    df['descuento'] = df['subtotal'] * (df['descuento_pct'] / 100)
    df['total'] = df['subtotal'] - df['descuento']

    return df


def analizar_ventas_por_tienda(df: pd.DataFrame) -> pd.DataFrame:
    """Genera análisis agregado por tienda."""
    analisis = df.groupby('tienda').agg(
        num_ventas=('venta_id', 'count'),
        total_vendido=('total', 'sum'),
        ticket_promedio=('total', 'mean'),
        ticket_maximo=('total', 'max'),
        ticket_minimo=('total', 'min'),
        productos_vendidos=('cantidad', 'sum'),
        descuento_promedio=('descuento_pct', 'mean')
    ).round(2)

    # Calcular ventas per cápita (asumiendo ventas = transacciones)
    analisis['venta_promedio_ticket'] = (analisis['total_vendido'] / analisis['num_ventas']).round(2)

    # Ordenar por total vendido
    analisis = analisis.sort_values('total_vendido', ascending=False)

    return analisis.reset_index()


def analizar_ventas_multidimensional(df: pd.DataFrame) -> pd.DataFrame:
    """Análisis por tienda y producto."""
    analisis = df.groupby(['tienda', 'producto']).agg(
        unidades_vendidas=('cantidad', 'sum'),
        ingresos_totales=('total', 'sum'),
        num_transacciones=('venta_id', 'count')
    ).round(2)

    return analisis.reset_index()


def top_productos_por_tienda(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Encuentra los N productos más vendidos por tienda."""
    # Agrupar y ordenar
    ventas_producto = df.groupby(['tienda', 'producto']).agg(
        ingresos=('total', 'sum')
    ).reset_index()

    # Top N por tienda
    top_por_tienda = ventas_producto.groupby('tienda').apply(
        lambda x: x.nlargest(top_n, 'ingresos')
    ).reset_index(drop=True)

    return top_por_tienda


def analisis_vendedores(df: pd.DataFrame) -> pd.DataFrame:
    """Análisis de performance de vendedores."""
    analisis = df.groupby('vendedor').agg(
        num_ventas=('venta_id', 'count'),
        total_ingresos=('total', 'sum'),
        ticket_promedio=('total', 'mean'),
        mejor_venta=('total', 'max'),
        productos_vendidos=('cantidad', 'sum')
    ).round(2)

    # Calcular productividad (ingresos por venta)
    analisis['productividad'] = (analisis['total_ingresos'] / analisis['num_ventas']).round(2)

    # Ranking
    analisis['ranking'] = analisis['total_ingresos'].rank(ascending=False, method='dense').astype(int)

    return analisis.sort_values('ranking').reset_index()


def funcion_agregacion_personalizada(serie: pd.Series) -> float:
    """Calcula el coeficiente de variación (medida de dispersión)."""
    if len(serie) == 0 or serie.std() == 0:
        return 0.0
    return (serie.std() / serie.mean()) * 100


def analisis_avanzado_con_agregaciones_custom(df: pd.DataFrame) -> pd.DataFrame:
    """Usa agregaciones personalizadas."""
    analisis = df.groupby('tienda').agg(
        total_ventas=('total', 'sum'),
        promedio_ventas=('total', 'mean'),
        mediana_ventas=('total', 'median'),
        std_ventas=('total', 'std'),
        coef_variacion=('total', funcion_agregacion_personalizada),
        rango_precios=('total', lambda x: x.max() - x.min()),
        percentil_90=('total', lambda x: x.quantile(0.9))
    ).round(2)

    return analisis.reset_index()


def comparacion_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """Comparación de ventas entre meses."""
    comparacion = df.groupby(['mes', 'tienda']).agg(
        total_vendido=('total', 'sum')
    ).round(2)

    # Pivot para tener meses en columnas
    pivot = comparacion.reset_index().pivot(
        index='tienda',
        columns='mes',
        values='total_vendido'
    ).fillna(0)

    # Calcular total por tienda
    pivot['TOTAL'] = pivot.sum(axis=1)

    return pivot


def analizar_descuentos_impacto(df: pd.DataFrame) -> pd.DataFrame:
    """Analiza el impacto de los descuentos."""
    analisis = df.groupby('descuento_pct').agg(
        num_ventas=('venta_id', 'count'),
        ingresos_brutos=('subtotal', 'sum'),
        ingresos_netos=('total', 'sum'),
        descuento_aplicado=('descuento', 'sum'),
        ticket_promedio=('total', 'mean')
    ).round(2)

    # Calcular porcentaje de ingresos perdidos
    analisis['pct_ingreso_perdido'] = (
        (analisis['descuento_aplicado'] / analisis['ingresos_brutos']) * 100
    ).round(2)

    return analisis.reset_index()


# EJECUCIÓN
if __name__ == '__main__':
    # Cargar datos
    df_ventas = cargar_ventas_tiendas()

    print("=" * 90)
    print("DATOS DE VENTAS")
    print("=" * 90)
    print(df_ventas.head(10))
    print(f"\nTotal de ventas: {len(df_ventas)}")

    # Análisis 1: Por tienda
    print("\n" + "=" * 90)
    print("📊 ANÁLISIS POR TIENDA")
    print("=" * 90)
    analisis_tienda = analizar_ventas_por_tienda(df_ventas)
    print(analisis_tienda)

    # Análisis 2: Top productos por tienda
    print("\n" + "=" * 90)
    print("🏆 TOP 3 PRODUCTOS POR TIENDA")
    print("=" * 90)
    top_productos = top_productos_por_tienda(df_ventas, top_n=3)
    for tienda in top_productos['tienda'].unique():
        print(f"\n{tienda}:")
        datos_tienda = top_productos[top_productos['tienda'] == tienda]
        for idx, row in datos_tienda.iterrows():
            print(f"  {row['producto']}: €{row['ingresos']:,.2f}")

    # Análisis 3: Performance de vendedores
    print("\n" + "=" * 90)
    print("👥 PERFORMANCE DE VENDEDORES")
    print("=" * 90)
    performance = analisis_vendedores(df_ventas)
    print(performance)

    # Análisis 4: Agregaciones personalizadas
    print("\n" + "=" * 90)
    print("📈 ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 90)
    stats_avanzado = analisis_avanzado_con_agregaciones_custom(df_ventas)
    print(stats_avanzado)

    # Análisis 5: Comparación mensual
    print("\n" + "=" * 90)
    print("📅 COMPARACIÓN MENSUAL POR TIENDA")
    print("=" * 90)
    comp_mensual = comparacion_mensual(df_ventas)
    print(comp_mensual)

    # Análisis 6: Impacto de descuentos
    print("\n" + "=" * 90)
    print("💰 IMPACTO DE DESCUENTOS")
    print("=" * 90)
    impacto_desc = analizar_descuentos_impacto(df_ventas)
    print(impacto_desc)
```

### 🎓 Conceptos Clave

- ✅ GroupBy con múltiples agregaciones
- ✅ Agregaciones personalizadas con funciones lambda
- ✅ GroupBy multinivel (múltiples columnas)
- ✅ Top N por grupo
- ✅ Pivot tables para análisis matricial
- ✅ Cálculo de métricas de negocio complejas

---

## Ejemplo 4: Merge de Múltiples DataFrames

### 📖 Contexto

Sistema de e-commerce con datos distribuidos en múltiples tablas: pedidos, clientes, productos y envíos.

### 🎯 Objetivo

Combinar múltiples DataFrames para crear un dataset unificado para análisis.

### 💻 Código

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def crear_datos_ecommerce() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Crea datasets simulados de un e-commerce."""
    np.random.seed(42)

    # CLIENTES
    clientes = pd.DataFrame({
        'cliente_id': range(1, 21),
        'nombre': [f'Cliente {i}' for i in range(1, 21)],
        'email': [f'cliente{i}@email.com' for i in range(1, 21)],
        'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 20),
        'segmento': np.random.choice(['Premium', 'Standard', 'Básico'], 20),
        'fecha_registro': pd.date_range('2023-01-01', periods=20, freq='15D')
    })

    # PRODUCTOS
    productos = pd.DataFrame({
        'producto_id': range(101, 116),
        'nombre_producto': [
            'Laptop Pro', 'Mouse Inalámbrico', 'Teclado Mecánico', 'Monitor 27"',
            'Auriculares Bluetooth', 'Webcam HD', 'Tablet 10"', 'Disco SSD 1TB',
            'Hub USB-C', 'Cable HDMI', 'Mousepad Gaming', 'Silla Ergonómica',
            'Lámpara LED', 'Soporte Monitor', 'Micrófono USB'
        ],
        'categoria': [
            'Computadoras', 'Accesorios', 'Accesorios', 'Monitores', 'Audio',
            'Video', 'Tablets', 'Almacenamiento', 'Accesorios', 'Cables',
            'Accesorios', 'Muebles', 'Iluminación', 'Muebles', 'Audio'
        ],
        'precio': [1200, 25, 89, 350, 75, 65, 299, 120, 35, 15, 20, 180, 45, 50, 95],
        'stock': np.random.randint(0, 100, 15),
        'proveedor': np.random.choice(['Proveedor A', 'Proveedor B', 'Proveedor C'], 15)
    })

    # PEDIDOS
    n_pedidos = 50
    pedidos = pd.DataFrame({
        'pedido_id': range(1000, 1000 + n_pedidos),
        'cliente_id': np.random.choice(clientes['cliente_id'], n_pedidos),
        'producto_id': np.random.choice(productos['producto_id'], n_pedidos),
        'cantidad': np.random.randint(1, 5, n_pedidos),
        'fecha_pedido': pd.date_range('2024-01-01', periods=n_pedidos, freq='D')[:n_pedidos],
        'estado': np.random.choice(['Completado', 'En proceso', 'Cancelado'], n_pedidos, p=[0.7, 0.2, 0.1])
    })

    # ENVÍOS (algunos pedidos no tienen envío aún)
    pedidos_con_envio = pedidos[pedidos['estado'] != 'Cancelado'].sample(frac=0.8)
    envios = pd.DataFrame({
        'envio_id': range(2000, 2000 + len(pedidos_con_envio)),
        'pedido_id': pedidos_con_envio['pedido_id'].values,
        'fecha_envio': pedidos_con_envio['fecha_pedido'] + pd.Timedelta(days=1),
        'fecha_entrega': pedidos_con_envio['fecha_pedido'] + pd.Timedelta(days=3),
        'transportista': np.random.choice(['DHL', 'UPS', 'Correos', 'SEUR'], len(pedidos_con_envio)),
        'costo_envio': np.random.choice([0, 3.99, 5.99, 8.99], len(pedidos_con_envio))
    })

    return clientes, productos, pedidos, envios


def crear_dataset_unificado(
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    pedidos: pd.DataFrame,
    envios: pd.DataFrame
) -> pd.DataFrame:
    """
    Une múltiples DataFrames en un dataset unificado.

    Args:
        clientes: DataFrame de clientes
        productos: DataFrame de productos
        pedidos: DataFrame de pedidos
        envios: DataFrame de envíos

    Returns:
        DataFrame unificado con toda la información
    """
    print("Iniciando proceso de unificación...")

    # PASO 1: Merge de pedidos con clientes (LEFT JOIN)
    # Queremos mantener todos los pedidos, incluso si falta info del cliente
    print("\n1. Uniendo pedidos con clientes...")
    df = pd.merge(
        pedidos,
        clientes,
        on='cliente_id',
        how='left',
        suffixes=('_pedido', '_cliente')
    )
    print(f"   Filas después del merge: {len(df)}")

    # PASO 2: Merge con productos (INNER JOIN)
    # Solo queremos pedidos de productos que existen
    print("\n2. Uniendo con productos...")
    df = pd.merge(
        df,
        productos,
        on='producto_id',
        how='inner',
        suffixes=('', '_producto')
    )
    print(f"   Filas después del merge: {len(df)}")

    # PASO 3: Merge con envíos (LEFT JOIN)
    # Algunos pedidos pueden no tener envío aún
    print("\n3. Uniendo con envíos...")
    df = pd.merge(
        df,
        envios,
        on='pedido_id',
        how='left'
    )
    print(f"   Filas después del merge: {len(df)}")

    # PASO 4: Calcular campos derivados
    print("\n4. Calculando campos derivados...")
    df['subtotal'] = df['cantidad'] * df['precio']
    df['total_con_envio'] = df['subtotal'] + df['costo_envio'].fillna(0)

    # Calcular días hasta entrega
    df['dias_entrega'] = (df['fecha_entrega'] - df['fecha_pedido']).dt.days

    # Indicador de envío pendiente
    df['envio_pendiente'] = df['envio_id'].isnull()

    # Margen de cliente (Premium paga más)
    margen_dict = {'Premium': 1.2, 'Standard': 1.0, 'Básico': 0.9}
    df['factor_segmento'] = df['segmento'].map(margen_dict)
    df['valor_cliente'] = df['subtotal'] * df['factor_segmento']

    return df


def validar_merge(df: pd.DataFrame) -> Dict:
    """Valida la calidad del merge realizado."""
    validaciones = {
        'total_filas': len(df),
        'clientes_unicos': df['cliente_id'].nunique(),
        'productos_unicos': df['producto_id'].nunique(),
        'pedidos_sin_envio': df['envio_pendiente'].sum(),
        'pedidos_con_envio': (~df['envio_pendiente']).sum(),
        'valores_nulos_criticos': df[['cliente_id', 'producto_id', 'pedido_id']].isnull().sum().sum(),
        'revenue_total': df['total_con_envio'].sum(),
        'ticket_promedio': df['total_con_envio'].mean()
    }

    return validaciones


def analizar_dataset_unificado(df: pd.DataFrame) -> None:
    """Genera análisis del dataset unificado."""
    print("\n" + "=" * 90)
    print("📊 ANÁLISIS DEL DATASET UNIFICADO")
    print("=" * 90)

    # Top clientes
    print("\n🏆 TOP 5 CLIENTES POR INGRESOS:")
    top_clientes = df.groupby(['cliente_id', 'nombre', 'segmento']).agg(
        total_gastado=('total_con_envio', 'sum'),
        num_pedidos=('pedido_id', 'count')
    ).sort_values('total_gastado', ascending=False).head(5).reset_index()
    print(top_clientes)

    # Productos más vendidos
    print("\n🏆 TOP 5 PRODUCTOS POR VENTAS:")
    top_productos = df.groupby(['producto_id', 'nombre_producto', 'categoria']).agg(
        unidades_vendidas=('cantidad', 'sum'),
        ingresos=('subtotal', 'sum')
    ).sort_values('ingresos', ascending=False).head(5).reset_index()
    print(top_productos)

    # Análisis por segmento
    print("\n📈 ANÁLISIS POR SEGMENTO DE CLIENTE:")
    por_segmento = df.groupby('segmento').agg(
        num_clientes=('cliente_id', 'nunique'),
        num_pedidos=('pedido_id', 'count'),
        total_ingresos=('valor_cliente', 'sum'),
        ticket_promedio=('valor_cliente', 'mean')
    ).round(2)
    print(por_segmento)

    # Análisis de envíos
    print("\n📦 ANÁLISIS DE ENVÍOS:")
    por_transportista = df[~df['envio_pendiente']].groupby('transportista').agg(
        num_envios=('envio_id', 'count'),
        dias_promedio_entrega=('dias_entrega', 'mean'),
        costo_promedio=('costo_envio', 'mean')
    ).round(2)
    print(por_transportista)


def detectar_problemas_merge(df: pd.DataFrame) -> None:
    """Detecta problemas comunes en merges."""
    print("\n" + "=" * 90)
    print("🔍 DETECCIÓN DE PROBLEMAS EN EL MERGE")
    print("=" * 90)

    # Duplicados
    duplicados = df.duplicated(subset=['pedido_id']).sum()
    print(f"\n⚠️  Pedidos duplicados: {duplicados}")

    # Valores nulos inesperados
    print(f"\n⚠️  Valores nulos por columna:")
    nulos = df.isnull().sum()
    nulos_importantes = nulos[nulos > 0]
    if len(nulos_importantes) > 0:
        print(nulos_importantes)
    else:
        print("   No hay valores nulos")

    # Pedidos sin cliente (no debería pasar)
    pedidos_sin_cliente = df['cliente_id'].isnull().sum()
    if pedidos_sin_cliente > 0:
        print(f"\n❌ ERROR: {pedidos_sin_cliente} pedidos sin cliente asociado")
    else:
        print(f"\n✅ Todos los pedidos tienen cliente asociado")


# EJECUCIÓN
if __name__ == '__main__':
    # Crear datos
    print("=" * 90)
    print("CREANDO DATOS DE E-COMMERCE")
    print("=" * 90)
    clientes, productos, pedidos, envios = crear_datos_ecommerce()

    print(f"\n📊 Tablas creadas:")
    print(f"   - Clientes: {len(clientes)} registros")
    print(f"   - Productos: {len(productos)} registros")
    print(f"   - Pedidos: {len(pedidos)} registros")
    print(f"   - Envíos: {len(envios)} registros")

    # Unificar
    print("\n" + "=" * 90)
    print("UNIFICANDO DATASETS")
    print("=" * 90)
    df_unificado = crear_dataset_unificado(clientes, productos, pedidos, envios)

    # Validar
    print("\n" + "=" * 90)
    print("VALIDACIÓN DEL MERGE")
    print("=" * 90)
    validaciones = validar_merge(df_unificado)
    for clave, valor in validaciones.items():
        print(f"   {clave}: {valor}")

    # Mostrar muestra
    print("\n" + "=" * 90)
    print("MUESTRA DEL DATASET UNIFICADO")
    print("=" * 90)
    columnas_mostrar = [
        'pedido_id', 'nombre', 'nombre_producto', 'cantidad',
        'subtotal', 'costo_envio', 'total_con_envio', 'estado'
    ]
    print(df_unificado[columnas_mostrar].head(10))

    # Análisis
    analizar_dataset_unificado(df_unificado)

    # Detectar problemas
    detectar_problemas_merge(df_unificado)
```

### 🎓 Conceptos Clave

- ✅ Merges secuenciales de múltiples tablas
- ✅ Diferentes tipos de joins (LEFT, INNER)
- ✅ Uso de suffixes para columnas duplicadas
- ✅ Validación post-merge
- ✅ Cálculo de métricas derivadas
- ✅ Detección de problemas en merges

---

## Ejemplo 5: Pipeline Completo de Transformación

### 📖 Contexto

Crear un pipeline ETL completo que tome datos crudos, los limpie, transforme, enriquezca y genere reportes.

### 🎯 Objetivo

Implementar un pipeline profesional de transformación siguiendo buenas prácticas de Data Engineering.

### 💻 Código

```python
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PipelineTransformacion:
    """Pipeline completo de transformación de datos de ventas."""

    def __init__(self):
        self.df_raw = None
        self.df_clean = None
        self.df_enriquecido = None
        self.df_agregado = None
        self.metricas = {}

    def extraer(self, path: str = None) -> pd.DataFrame:
        """
        Fase de Extracción: Carga datos crudos.

        Args:
            path: Ruta al archivo (None para datos simulados)

        Returns:
            DataFrame con datos crudos
        """
        logger.info("=" * 70)
        logger.info("FASE 1: EXTRACCIÓN")
        logger.info("=" * 70)

        if path:
            logger.info(f"Cargando datos desde: {path}")
            self.df_raw = pd.read_csv(path)
        else:
            logger.info("Generando datos simulados...")
            self.df_raw = self._generar_datos_simulados()

        logger.info(f"✅ Datos extraídos: {len(self.df_raw)} filas, {len(self.df_raw.columns)} columnas")
        self.metricas['filas_extraidas'] = len(self.df_raw)

        return self.df_raw

    def _generar_datos_simulados(self) -> pd.DataFrame:
        """Genera datos simulados para demostración."""
        np.random.seed(42)
        n = 100

        datos = {
            'id_venta': range(1, n + 1),
            'fecha': pd.date_range('2024-01-01', periods=n, freq='D')[:n],
            'cliente': [f'CLI{i:04d}' for i in np.random.randint(1, 30, n)],
            'producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Impresora'], n),
            'cantidad': np.random.randint(1, 10, n),
            'precio': np.random.choice([25, 75, 150, 350, 450], n),
            'descuento': np.random.choice([0, 5, 10, 15, 20], n),
            'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n),
            'canal': np.random.choice(['Online', 'Tienda', 'Teléfono'], n),
            'vendedor': np.random.choice(['Ana', 'Carlos', 'María', 'Pedro'], n)
        }

        # Introducir problemas de calidad
        df = pd.DataFrame(datos)
        df.loc[np.random.choice(df.index, 5), 'cliente'] = None
        df.loc[np.random.choice(df.index, 3), 'precio'] = None
        df = pd.concat([df, df.iloc[:2]], ignore_index=True)  # Duplicados

        return df

    def limpiar(self) -> pd.DataFrame:
        """
        Fase de Limpieza: Elimina duplicados, maneja nulos, valida tipos.

        Returns:
            DataFrame limpio
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 2: LIMPIEZA")
        logger.info("=" * 70)

        if self.df_raw is None:
            raise ValueError("Debe ejecutar extraer() primero")

        df = self.df_raw.copy()
        filas_iniciales = len(df)

        # 1. Eliminar duplicados
        duplicados_antes = df.duplicated().sum()
        df = df.drop_duplicates()
        logger.info(f"✅ Duplicados eliminados: {duplicados_antes}")

        # 2. Manejar valores nulos
        nulos_antes = df.isnull().sum().sum()
        df = df.dropna(subset=['id_venta', 'producto'])
        df['cliente'] = df['cliente'].fillna('CLI_DESCONOCIDO')
        df['precio'] = df['precio'].fillna(df['precio'].median())
        logger.info(f"✅ Valores nulos manejados: {nulos_antes}")

        # 3. Validar tipos de datos
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df['cantidad'] = df['cantidad'].astype(int)
        df['precio'] = df['precio'].astype(float)
        df['descuento'] = df['descuento'].astype(int)
        logger.info("✅ Tipos de datos validados")

        # 4. Normalizar texto
        df['region'] = df['region'].str.title().str.strip()
        df['canal'] = df['canal'].str.title().str.strip()
        df['producto'] = df['producto'].str.title().str.strip()
        logger.info("✅ Texto normalizado")

        self.df_clean = df
        self.metricas['filas_eliminadas'] = filas_iniciales - len(df)
        self.metricas['filas_limpias'] = len(df)

        logger.info(f"✅ Limpieza completada: {len(df)} filas ({self.metricas['filas_eliminadas']} eliminadas)")

        return self.df_clean

    def transformar(self) -> pd.DataFrame:
        """
        Fase de Transformación: Calcula campos derivados y enriquece.

        Returns:
            DataFrame transformado
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 3: TRANSFORMACIÓN")
        logger.info("=" * 70)

        if self.df_clean is None:
            raise ValueError("Debe ejecutar limpiar() primero")

        df = self.df_clean.copy()

        # 1. Cálculos financieros
        df['subtotal'] = df['cantidad'] * df['precio']
        df['descuento_monto'] = df['subtotal'] * (df['descuento'] / 100)
        df['total'] = df['subtotal'] - df['descuento_monto']
        logger.info("✅ Cálculos financieros completados")

        # 2. Extraer información temporal
        df['año'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['trimestre'] = df['fecha'].dt.quarter
        df['dia_semana'] = df['fecha'].dt.day_name()
        df['es_fin_semana'] = df['fecha'].dt.dayofweek >= 5
        logger.info("✅ Información temporal extraída")

        # 3. Categorizar ventas
        df['categoria_venta'] = pd.cut(
            df['total'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Pequeña', 'Mediana', 'Grande', 'Muy Grande']
        )
        logger.info("✅ Ventas categorizadas")

        # 4. Métricas por cliente (con transform)
        df['total_cliente'] = df.groupby('cliente')['total'].transform('sum')
        df['num_compras_cliente'] = df.groupby('cliente')['id_venta'].transform('count')
        df['ticket_promedio_cliente'] = df['total_cliente'] / df['num_compras_cliente']
        logger.info("✅ Métricas por cliente calculadas")

        # 5. Ranking de productos
        df['ranking_producto'] = df.groupby('producto')['total'].rank(
            method='dense',
            ascending=False
        )
        logger.info("✅ Rankings calculados")

        # 6. Indicadores de negocio
        df['venta_alta_valor'] = df['total'] > df['total'].quantile(0.75)
        df['cliente_recurrente'] = df['num_compras_cliente'] > 1
        df['con_descuento'] = df['descuento'] > 0
        logger.info("✅ Indicadores de negocio creados")

        self.df_enriquecido = df
        self.metricas['columnas_añadidas'] = len(df.columns) - len(self.df_clean.columns)

        logger.info(f"✅ Transformación completada: {self.metricas['columnas_añadidas']} columnas añadidas")

        return self.df_enriquecido

    def agregar(self) -> Dict[str, pd.DataFrame]:
        """
        Fase de Agregación: Genera vistas agregadas para análisis.

        Returns:
            Diccionario con múltiples vistas agregadas
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 4: AGREGACIÓN")
        logger.info("=" * 70)

        if self.df_enriquecido is None:
            raise ValueError("Debe ejecutar transformar() primero")

        df = self.df_enriquecido
        agregaciones = {}

        # 1. Resumen por producto
        agregaciones['por_producto'] = df.groupby('producto').agg(
            unidades_vendidas=('cantidad', 'sum'),
            ingresos_totales=('total', 'sum'),
            num_ventas=('id_venta', 'count'),
            ticket_promedio=('total', 'mean'),
            precio_promedio=('precio', 'mean')
        ).round(2).sort_values('ingresos_totales', ascending=False)
        logger.info("✅ Agregación por producto completada")

        # 2. Resumen por región
        agregaciones['por_region'] = df.groupby('region').agg(
            total_ventas=('total', 'sum'),
            num_transacciones=('id_venta', 'count'),
            clientes_unicos=('cliente', 'nunique'),
            ticket_promedio=('total', 'mean')
        ).round(2).sort_values('total_ventas', ascending=False)
        logger.info("✅ Agregación por región completada")

        # 3. Resumen por canal
        agregaciones['por_canal'] = df.groupby('canal').agg(
            ingresos=('total', 'sum'),
            num_ventas=('id_venta', 'count'),
            productos_vendidos=('cantidad', 'sum')
        ).round(2)
        logger.info("✅ Agregación por canal completada")

        # 4. Resumen temporal
        agregaciones['por_mes'] = df.groupby(['año', 'mes']).agg(
            ingresos=('total', 'sum'),
            ventas=('id_venta', 'count')
        ).round(2)
        logger.info("✅ Agregación temporal completada")

        # 5. Top clientes
        agregaciones['top_clientes'] = df.groupby('cliente').agg(
            total_gastado=('total', 'sum'),
            num_compras=('id_venta', 'count'),
            ticket_promedio=('total', 'mean')
        ).round(2).sort_values('total_gastado', ascending=False).head(10)
        logger.info("✅ Top clientes identificados")

        self.df_agregado = agregaciones
        self.metricas['num_vistas_agregadas'] = len(agregaciones)

        logger.info(f"✅ Agregación completada: {len(agregaciones)} vistas creadas")

        return agregaciones

    def generar_reporte(self) -> Dict:
        """
        Genera reporte final con métricas y resultados.

        Returns:
            Diccionario con métricas del pipeline
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 5: REPORTE FINAL")
        logger.info("=" * 70)

        if self.df_enriquecido is None:
            raise ValueError("Pipeline incompleto")

        reporte = {
            **self.metricas,
            'revenue_total': self.df_enriquecido['total'].sum(),
            'ticket_promedio': self.df_enriquecido['total'].mean(),
            'clientes_unicos': self.df_enriquecido['cliente'].nunique(),
            'productos_unicos': self.df_enriquecido['producto'].nunique(),
            'ventas_con_descuento': (self.df_enriquecido['descuento'] > 0).sum(),
            'porcentaje_descuento': ((self.df_enriquecido['descuento'] > 0).sum() / len(self.df_enriquecido) * 100)
        }

        logger.info("📊 MÉTRICAS PRINCIPALES:")
        for clave, valor in reporte.items():
            if isinstance(valor, float):
                logger.info(f"   {clave}: {valor:,.2f}")
            else:
                logger.info(f"   {clave}: {valor}")

        return reporte

    def ejecutar_pipeline_completo(self, path: str = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Ejecuta el pipeline completo de principio a fin.

        Args:
            path: Ruta opcional al archivo de datos

        Returns:
            Tupla con (DataFrame final, reporte de métricas)
        """
        logger.info("🚀 INICIANDO PIPELINE DE TRANSFORMACIÓN")
        inicio = datetime.now()

        try:
            self.extraer(path)
            self.limpiar()
            self.transformar()
            self.agregar()
            reporte = self.generar_reporte()

            duracion = (datetime.now() - inicio).total_seconds()
            reporte['duracion_segundos'] = duracion

            logger.info(f"\n✅ PIPELINE COMPLETADO EXITOSAMENTE EN {duracion:.2f} SEGUNDOS")

            return self.df_enriquecido, reporte

        except Exception as e:
            logger.error(f"❌ ERROR EN EL PIPELINE: {str(e)}")
            raise


# EJECUCIÓN
if __name__ == '__main__':
    # Crear instancia del pipeline
    pipeline = PipelineTransformacion()

    # Ejecutar pipeline completo
    df_final, reporte = pipeline.ejecutar_pipeline_completo()

    # Mostrar resultados
    print("\n" + "=" * 90)
    print("DATASET FINAL (Muestra)")
    print("=" * 90)
    columnas_importantes = [
        'id_venta', 'fecha', 'cliente', 'producto', 'cantidad',
        'total', 'categoria_venta', 'es_fin_semana'
    ]
    print(df_final[columnas_importantes].head(10))

    # Mostrar agregaciones
    print("\n" + "=" * 90)
    print("RESUMEN POR PRODUCTO")
    print("=" * 90)
    print(pipeline.df_agregado['por_producto'].head())

    print("\n" + "=" * 90)
    print("TOP 10 CLIENTES")
    print("=" * 90)
    print(pipeline.df_agregado['top_clientes'])
```

### 🎓 Conceptos Clave

- ✅ Arquitectura de pipeline ETL completo
- ✅ Separación de responsabilidades (extraer, limpiar, transformar, agregar)
- ✅ Logging profesional para monitoreo
- ✅ Manejo de errores robusto
- ✅ Generación de métricas y reportes
- ✅ Código reutilizable y mantenible

---

## 📝 Resumen de Ejemplos

Has visto 5 ejemplos progresivos que cubren:

1. **Limpieza de datos**: Manejo de nulos, duplicados y normalización
2. **Apply y Lambda**: Transformaciones complejas y personalizadas
3. **GroupBy avanzado**: Agregaciones multidimensionales
4. **Merges múltiples**: Combinación de datasets relacionados
5. **Pipeline completo**: Arquitectura ETL profesional

### Próximos Pasos

1. Ejecuta cada ejemplo y experimenta con los datos
2. Modifica los ejemplos para probar diferentes escenarios
3. Practica con los ejercicios en `03-EJERCICIOS.md`
4. Construye tu proyecto práctico en `04-proyecto-practico/`

---

**Tiempo estimado**: 60-90 minutos
**Última actualización**: 2025-10-30
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
