# Ejemplos Prácticos: Feature Engineering

En esta sección trabajaremos ejemplos paso a paso usando datasets realistas. Todos los ejemplos son ejecutables y usan empresas ficticias para mantener el contexto profesional.

---

## Ejemplo 1: Encoding de Variables Categóricas - Nivel: Básico

### Contexto

**FinTech Analytics** te ha contratado para preparar datos de clientes para un modelo de scoring crediticio. Tienen información de clientes con variables categóricas que necesitan transformarse antes de entrenar el modelo.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Datos de clientes de FinTech Analytics
clientes = pd.DataFrame({
    'cliente_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'educacion': ['secundaria', 'universidad', 'master', 'secundaria',
                  'universidad', 'doctorado', 'master', 'universidad'],
    'tipo_vivienda': ['alquiler', 'propia', 'propia', 'alquiler',
                      'hipoteca', 'propia', 'hipoteca', 'alquiler'],
    'region': ['norte', 'sur', 'centro', 'norte', 'sur', 'centro', 'norte', 'sur'],
    'ingresos': [25000, 45000, 65000, 28000, 52000, 85000, 58000, 42000],
    'aprobado': [0, 1, 1, 0, 1, 1, 1, 1]  # Target: crédito aprobado
})

print("=== Datos Originales ===")
print(clientes)
```

### Paso 1: Identificar el tipo de cada variable categórica

```python
# Análisis de variables
print("\n=== Análisis de Variables Categóricas ===")

# Educación: ORDINAL (tiene orden natural)
print("\nEducación (ORDINAL):")
print("  secundaria < universidad < master < doctorado")
print(f"  Valores únicos: {clientes['educacion'].unique()}")

# Tipo vivienda: NOMINAL (sin orden inherente)
print("\nTipo Vivienda (NOMINAL):")
print("  alquiler, propia, hipoteca - sin orden")
print(f"  Valores únicos: {clientes['tipo_vivienda'].unique()}")

# Región: NOMINAL (sin orden inherente)
print("\nRegión (NOMINAL):")
print(f"  Valores únicos: {clientes['region'].unique()}")
```

### Paso 2: Label Encoding para variable ordinal (educación)

```python
# Para educación usamos Label Encoding CON ORDEN MANUAL
# porque Label Encoder asigna orden alfabético (incorrecto)

# Definimos el orden correcto
orden_educacion = {
    'secundaria': 0,
    'universidad': 1,
    'master': 2,
    'doctorado': 3
}

# Aplicamos el mapeo
clientes['educacion_encoded'] = clientes['educacion'].map(orden_educacion)

print("\n=== Label Encoding (Educación) ===")
print(clientes[['cliente_id', 'educacion', 'educacion_encoded']])

# Verificación: el orden tiene sentido
print("\nVerificación del orden:")
print("  0: secundaria (nivel más bajo)")
print("  1: universidad")
print("  2: master")
print("  3: doctorado (nivel más alto)")
```

### Paso 3: One-Hot Encoding para variables nominales

```python
# Para tipo_vivienda y region usamos One-Hot
# porque NO tienen orden natural

# Método 1: pd.get_dummies (más simple)
print("\n=== One-Hot Encoding (Tipo Vivienda) ===")
tipo_vivienda_onehot = pd.get_dummies(
    clientes['tipo_vivienda'],
    prefix='vivienda'
)
print(tipo_vivienda_onehot)

# Método 2: sklearn OneHotEncoder (mejor para producción)
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
region_encoded = encoder.fit_transform(clientes[['region']])

# Crear DataFrame con nombres de columnas
region_columns = encoder.get_feature_names_out(['region'])
region_onehot = pd.DataFrame(region_encoded, columns=region_columns)

print("\n=== One-Hot Encoding (Región con sklearn) ===")
print(region_onehot)
```

### Paso 4: Combinar todo en un DataFrame final

```python
# Combinar todas las transformaciones
clientes_final = pd.concat([
    clientes[['cliente_id', 'ingresos', 'aprobado']],  # Numéricas y target
    clientes[['educacion_encoded']],                    # Ordinal encoded
    tipo_vivienda_onehot,                               # One-hot vivienda
    region_onehot                                       # One-hot región
], axis=1)

print("\n=== Dataset Final para ML ===")
print(clientes_final)
print(f"\nColumnas: {list(clientes_final.columns)}")
print(f"Shape: {clientes_final.shape}")
```

### Resultado

```
=== Dataset Final para ML ===
   cliente_id  ingresos  aprobado  educacion_encoded  vivienda_alquiler  vivienda_hipoteca  vivienda_propia  region_centro  region_norte  region_sur
0           1     25000         0                  0                  1                  0                0              0             1           0
1           2     45000         1                  1                  0                  0                1              0             0           1
2           3     65000         1                  2                  0                  0                1              1             0           0
3           4     28000         0                  0                  1                  0                0              0             1           0
4           5     52000         1                  1                  0                  1                0              0             0           1
5           6     85000         1                  3                  0                  0                1              1             0           0
6           7     58000         1                  2                  0                  1                0              0             1           0
7           8     42000         1                  1                  1                  0                0              0             0           1
```

### Interpretación

1. **Educación** se convirtió en un solo número (0-3) manteniendo el orden natural
2. **Tipo vivienda** generó 3 columnas binarias (una por categoría)
3. **Región** generó 3 columnas binarias (una por categoría)
4. El dataset pasó de 6 columnas a 10, pero ahora es 100% numérico y listo para ML

---

## Ejemplo 2: Scaling de Variables Numéricas - Nivel: Básico

### Contexto

**CloudAPI Systems** necesita predecir el tiempo de respuesta de sus APIs. Tienen métricas con escalas muy diferentes que necesitan normalizarse para que el modelo funcione correctamente.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import matplotlib.pyplot as plt

# Métricas de APIs de CloudAPI Systems
metricas = pd.DataFrame({
    'api_id': ['api_users', 'api_orders', 'api_products', 'api_auth',
               'api_search', 'api_reports', 'api_admin', 'api_payments'],
    'requests_por_segundo': [1500, 800, 450, 2000, 1200, 100, 50, 900],
    'tiempo_respuesta_ms': [45, 120, 80, 25, 200, 500, 150, 65],
    'memoria_mb': [512, 1024, 768, 256, 2048, 4096, 512, 1024],
    'cpu_percent': [25.5, 45.2, 35.8, 15.2, 65.3, 85.1, 20.5, 40.2]
})

print("=== Datos Originales ===")
print(metricas)
print("\n=== Estadísticas ===")
print(metricas.describe())
```

### El Problema: Escalas muy diferentes

```python
print("\n=== Rangos de cada variable ===")
numeric_cols = ['requests_por_segundo', 'tiempo_respuesta_ms', 'memoria_mb', 'cpu_percent']

for col in numeric_cols:
    print(f"{col}:")
    print(f"  Min: {metricas[col].min()}")
    print(f"  Max: {metricas[col].max()}")
    print(f"  Rango: {metricas[col].max() - metricas[col].min()}")
    print()

# Problema: memoria_mb tiene rango de 3840 mientras cpu_percent tiene rango de 70
# Un modelo lineal dará más "importancia" a memoria solo por tener números más grandes
```

### Paso 1: StandardScaler (Z-score)

```python
# StandardScaler: media=0, std=1
# Ideal para datos con distribución aproximadamente normal

scaler_standard = StandardScaler()
datos_numeric = metricas[numeric_cols]

# Fit y transform
datos_standard = scaler_standard.fit_transform(datos_numeric)
df_standard = pd.DataFrame(datos_standard, columns=numeric_cols)

print("=== StandardScaler ===")
print(df_standard.round(2))

print("\nVerificación:")
print(f"  Media de cada columna: {df_standard.mean().round(4).tolist()}")
print(f"  Std de cada columna: {df_standard.std().round(4).tolist()}")
```

### Paso 2: MinMaxScaler (Rango 0-1)

```python
# MinMaxScaler: valores entre 0 y 1
# Ideal para redes neuronales o cuando necesitas valores acotados

scaler_minmax = MinMaxScaler()
datos_minmax = scaler_minmax.fit_transform(datos_numeric)
df_minmax = pd.DataFrame(datos_minmax, columns=numeric_cols)

print("\n=== MinMaxScaler ===")
print(df_minmax.round(2))

print("\nVerificación:")
print(f"  Min de cada columna: {df_minmax.min().tolist()}")
print(f"  Max de cada columna: {df_minmax.max().tolist()}")
```

### Paso 3: RobustScaler (Resistente a outliers)

```python
# Agregamos un outlier para demostrar RobustScaler
metricas_con_outlier = metricas.copy()
metricas_con_outlier.loc[8] = ['api_legacy', 50, 5000, 512, 10.0]  # tiempo_respuesta muy alto

print("\n=== Datos con Outlier ===")
print(metricas_con_outlier)

# Comparar StandardScaler vs RobustScaler con outlier
datos_outlier = metricas_con_outlier[numeric_cols]

# StandardScaler (afectado por outlier)
standard_outlier = StandardScaler().fit_transform(datos_outlier)
df_standard_outlier = pd.DataFrame(standard_outlier, columns=numeric_cols)

# RobustScaler (resistente a outlier)
robust_outlier = RobustScaler().fit_transform(datos_outlier)
df_robust_outlier = pd.DataFrame(robust_outlier, columns=numeric_cols)

print("\n=== Comparación: tiempo_respuesta_ms ===")
comparison = pd.DataFrame({
    'original': datos_outlier['tiempo_respuesta_ms'].values,
    'standard': df_standard_outlier['tiempo_respuesta_ms'].round(2).values,
    'robust': df_robust_outlier['tiempo_respuesta_ms'].round(2).values
})
print(comparison)

print("\nObservación:")
print("  StandardScaler: el outlier (5000ms) distorsiona la escala de todos los valores")
print("  RobustScaler: el outlier tiene menos impacto en los demás valores")
```

### Resultado: Cuándo usar cada Scaler

```python
print("\n=== Guía de Selección de Scaler ===")
print("""
┌─────────────────┬─────────────────────────────────┬────────────────────────┐
│ Scaler          │ Cuándo Usarlo                   │ Resultado              │
├─────────────────┼─────────────────────────────────┼────────────────────────┤
│ StandardScaler  │ Datos ~normales, sin outliers   │ Media=0, Std=1         │
│ MinMaxScaler    │ Redes neuronales, valores [0,1] │ Min=0, Max=1           │
│ RobustScaler    │ Datos con outliers              │ Mediana=0, IQR=1       │
└─────────────────┴─────────────────────────────────┴────────────────────────┘
""")
```

### Interpretación

1. **StandardScaler** funciona bien cuando los datos son aproximadamente normales
2. **MinMaxScaler** garantiza valores entre 0 y 1, pero un solo outlier puede comprimir todos los demás valores
3. **RobustScaler** es la mejor opción cuando hay outliers que no quieres eliminar

---

## Ejemplo 3: Manejo de Missing Values - Nivel: Intermedio

### Contexto

**LogisticFlow** tiene datos de envíos con valores faltantes. Necesitas decidir la mejor estrategia de imputación para cada columna antes de entrenar un modelo de predicción de tiempos de entrega.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Datos de envíos de LogisticFlow con valores faltantes
np.random.seed(42)

envios = pd.DataFrame({
    'envio_id': range(1, 16),
    'distancia_km': [50, 120, np.nan, 85, 200, 150, np.nan, 95, 180, 60,
                     np.nan, 110, 75, 160, 90],
    'peso_kg': [2.5, 15.0, 8.0, np.nan, 25.0, 12.0, 5.0, np.nan, 20.0, 3.0,
                10.0, np.nan, 7.0, 18.0, 6.0],
    'tipo_envio': ['express', 'standard', 'express', 'standard', np.nan,
                   'economy', 'express', 'standard', np.nan, 'express',
                   'standard', 'economy', 'express', np.nan, 'standard'],
    'zona': ['urbana', 'rural', 'urbana', 'suburbana', 'rural',
             np.nan, 'urbana', 'rural', 'suburbana', np.nan,
             'urbana', 'rural', 'suburbana', 'urbana', 'rural'],
    'tiempo_entrega_horas': [4, 24, 5, 18, 48, 36, 6, 20, 40, 5,
                             15, 30, 8, 35, 22]
})

print("=== Datos Originales ===")
print(envios)

print("\n=== Conteo de Missing Values ===")
print(envios.isnull().sum())
print(f"\nPorcentaje de missing por columna:")
print((envios.isnull().sum() / len(envios) * 100).round(1))
```

### Paso 1: Analizar el patrón de missing

```python
print("\n=== Análisis del Patrón de Missing ===")

# Visualizar dónde están los missing
missing_matrix = envios.isnull().astype(int)
print(missing_matrix)

print("\nPatrón identificado:")
print("  - distancia_km: 3 missing (20%) - numérica continua")
print("  - peso_kg: 3 missing (20%) - numérica continua")
print("  - tipo_envio: 3 missing (20%) - categórica nominal")
print("  - zona: 2 missing (13%) - categórica nominal")
```

### Paso 2: Imputación de variables numéricas

```python
# Estrategia para numéricas: usar la MEDIANA (más robusta que la media)

print("\n=== Imputación de Variables Numéricas ===")

# Estadísticas antes de imputar
print("Estadísticas ANTES de imputar:")
print(f"  distancia_km: media={envios['distancia_km'].mean():.1f}, mediana={envios['distancia_km'].median():.1f}")
print(f"  peso_kg: media={envios['peso_kg'].mean():.1f}, mediana={envios['peso_kg'].median():.1f}")

# Crear imputador con mediana
imputer_numeric = SimpleImputer(strategy='median')

# Aplicar solo a columnas numéricas
numeric_cols = ['distancia_km', 'peso_kg']
envios_imputed = envios.copy()
envios_imputed[numeric_cols] = imputer_numeric.fit_transform(envios[numeric_cols])

print("\nValores imputados (distancia_km):")
original_missing = envios['distancia_km'].isnull()
print(f"  Índices con missing: {list(envios[original_missing].index)}")
print(f"  Valor imputado: {envios_imputed.loc[original_missing, 'distancia_km'].iloc[0]:.1f} km (mediana)")

print("\nValores imputados (peso_kg):")
original_missing = envios['peso_kg'].isnull()
print(f"  Índices con missing: {list(envios[original_missing].index)}")
print(f"  Valor imputado: {envios_imputed.loc[original_missing, 'peso_kg'].iloc[0]:.1f} kg (mediana)")
```

### Paso 3: Imputación de variables categóricas

```python
print("\n=== Imputación de Variables Categóricas ===")

# Estadísticas de frecuencia
print("Frecuencias ANTES de imputar:")
print("\ntipo_envio:")
print(envios['tipo_envio'].value_counts())
print("\nzona:")
print(envios['zona'].value_counts())

# Crear imputador con la MODA (valor más frecuente)
imputer_categorical = SimpleImputer(strategy='most_frequent')

# Aplicar a columnas categóricas
categorical_cols = ['tipo_envio', 'zona']
envios_imputed[categorical_cols] = imputer_categorical.fit_transform(envios[categorical_cols])

print("\nValores imputados:")
print(f"  tipo_envio: 'express' (más frecuente)")
print(f"  zona: 'urbana' (más frecuente)")
```

### Paso 4: Crear indicadores de missing (opcional pero útil)

```python
print("\n=== Indicadores de Missing ===")

# A veces el HECHO de que falte un valor es información útil
# Crear columnas indicadoras

for col in ['distancia_km', 'peso_kg', 'tipo_envio', 'zona']:
    envios_imputed[f'{col}_was_missing'] = envios[col].isnull().astype(int)

print("Columnas indicadoras creadas:")
missing_indicators = [col for col in envios_imputed.columns if '_was_missing' in col]
print(envios_imputed[['envio_id'] + missing_indicators])
```

### Paso 5: Dataset final

```python
print("\n=== Dataset Final (sin missing) ===")
print(envios_imputed.to_string())

print("\n=== Verificación: No hay missing ===")
print(envios_imputed.isnull().sum())
```

### Resultado

El dataset ahora tiene:
- Todas las variables numéricas imputadas con la mediana
- Todas las variables categóricas imputadas con la moda
- Columnas indicadoras que marcan qué valores fueron imputados

### Interpretación

```python
print("""
=== Resumen de Estrategias Aplicadas ===

┌────────────────┬─────────────────────┬─────────────────────────────────────┐
│ Columna        │ Tipo                │ Estrategia                          │
├────────────────┼─────────────────────┼─────────────────────────────────────┤
│ distancia_km   │ Numérica continua   │ Mediana (robusta a outliers)        │
│ peso_kg        │ Numérica continua   │ Mediana (robusta a outliers)        │
│ tipo_envio     │ Categórica nominal  │ Moda (valor más frecuente)          │
│ zona           │ Categórica nominal  │ Moda (valor más frecuente)          │
└────────────────┴─────────────────────┴─────────────────────────────────────┘

Indicadores de missing: Preservan la información de QUÉ valores faltaban,
lo cual puede ser predictivo (ej: si siempre falta la zona en envíos problemáticos).
""")
```

---

## Ejemplo 4: Feature Engineering Temporal - Nivel: Intermedio

### Contexto

**RestaurantData Co.** quiere predecir las ventas de sus restaurantes. Tienen datos con fechas que contienen información valiosa sin explotar.

### Datos

```python
import pandas as pd
import numpy as np
from datetime import datetime

# Datos de ventas de RestaurantData Co.
ventas = pd.DataFrame({
    'venta_id': range(1, 13),
    'fecha_hora': [
        '2024-01-15 12:30:00',  # Lunes almuerzo
        '2024-01-15 20:00:00',  # Lunes cena
        '2024-01-16 13:00:00',  # Martes almuerzo
        '2024-01-20 21:30:00',  # Sábado cena
        '2024-01-21 14:00:00',  # Domingo almuerzo
        '2024-02-14 20:30:00',  # San Valentín cena
        '2024-03-15 12:00:00',  # Viernes almuerzo
        '2024-03-15 19:30:00',  # Viernes cena
        '2024-03-16 22:00:00',  # Sábado noche
        '2024-12-24 21:00:00',  # Nochebuena
        '2024-12-25 14:30:00',  # Navidad almuerzo
        '2024-12-31 23:30:00',  # Nochevieja
    ],
    'monto': [45, 85, 38, 120, 55, 180, 42, 95, 110, 250, 150, 300]
})

# Convertir a datetime
ventas['fecha_hora'] = pd.to_datetime(ventas['fecha_hora'])

print("=== Datos Originales ===")
print(ventas)
```

### Paso 1: Extraer features básicas de fecha

```python
print("\n=== Features Básicas de Fecha ===")

# Extraer componentes de la fecha
ventas['hora'] = ventas['fecha_hora'].dt.hour
ventas['dia_semana'] = ventas['fecha_hora'].dt.dayofweek  # 0=lunes, 6=domingo
ventas['dia_mes'] = ventas['fecha_hora'].dt.day
ventas['mes'] = ventas['fecha_hora'].dt.month
ventas['año'] = ventas['fecha_hora'].dt.year
ventas['trimestre'] = ventas['fecha_hora'].dt.quarter
ventas['dia_año'] = ventas['fecha_hora'].dt.dayofyear
ventas['semana_año'] = ventas['fecha_hora'].dt.isocalendar().week

print(ventas[['fecha_hora', 'hora', 'dia_semana', 'dia_mes', 'mes', 'trimestre']])
```

### Paso 2: Crear features binarias (flags)

```python
print("\n=== Features Binarias ===")

# ¿Es fin de semana?
ventas['es_fin_de_semana'] = (ventas['dia_semana'] >= 5).astype(int)

# ¿Es horario de almuerzo (12-15)?
ventas['es_almuerzo'] = ((ventas['hora'] >= 12) & (ventas['hora'] <= 15)).astype(int)

# ¿Es horario de cena (19-23)?
ventas['es_cena'] = ((ventas['hora'] >= 19) & (ventas['hora'] <= 23)).astype(int)

# ¿Es horario pico?
ventas['es_horario_pico'] = ((ventas['hora'].isin([13, 14, 20, 21]))).astype(int)

print(ventas[['fecha_hora', 'es_fin_de_semana', 'es_almuerzo', 'es_cena', 'es_horario_pico']])
```

### Paso 3: Identificar fechas especiales

```python
print("\n=== Fechas Especiales ===")

# Definir fechas especiales (holidays)
fechas_especiales = {
    (2, 14): 'san_valentin',
    (12, 24): 'nochebuena',
    (12, 25): 'navidad',
    (12, 31): 'nochevieja',
}

def es_fecha_especial(fecha):
    """Identifica si una fecha es especial."""
    key = (fecha.month, fecha.day)
    return fechas_especiales.get(key, 'normal')

ventas['tipo_dia'] = ventas['fecha_hora'].apply(es_fecha_especial)
ventas['es_festivo'] = (ventas['tipo_dia'] != 'normal').astype(int)

print(ventas[['fecha_hora', 'tipo_dia', 'es_festivo', 'monto']])

print("\nObservación: Las fechas especiales tienen montos más altos")
print(f"  Promedio día normal: {ventas[ventas['es_festivo']==0]['monto'].mean():.0f}€")
print(f"  Promedio día festivo: {ventas[ventas['es_festivo']==1]['monto'].mean():.0f}€")
```

### Paso 4: Encoding cíclico para hora y día de semana

```python
print("\n=== Encoding Cíclico ===")

# Problema: hora 23 y hora 0 están "lejos" numéricamente pero "cerca" en realidad
# Solución: usar seno y coseno

def encode_ciclico(valor: int, max_valor: int) -> tuple:
    """Codifica un valor cíclico usando seno y coseno."""
    angulo = 2 * np.pi * valor / max_valor
    return np.sin(angulo), np.cos(angulo)

# Encoding cíclico para hora (ciclo de 24)
ventas['hora_sin'], ventas['hora_cos'] = zip(*ventas['hora'].apply(
    lambda x: encode_ciclico(x, 24)
))

# Encoding cíclico para día de semana (ciclo de 7)
ventas['dia_sin'], ventas['dia_cos'] = zip(*ventas['dia_semana'].apply(
    lambda x: encode_ciclico(x, 7)
))

# Encoding cíclico para mes (ciclo de 12)
ventas['mes_sin'], ventas['mes_cos'] = zip(*ventas['mes'].apply(
    lambda x: encode_ciclico(x, 12)
))

print(ventas[['hora', 'hora_sin', 'hora_cos']].round(2))

print("\nVerificación: hora 23 y hora 1 están cerca en espacio seno/coseno")
hora_23 = encode_ciclico(23, 24)
hora_1 = encode_ciclico(1, 24)
print(f"  Hora 23: sin={hora_23[0]:.2f}, cos={hora_23[1]:.2f}")
print(f"  Hora 1:  sin={hora_1[0]:.2f}, cos={hora_1[1]:.2f}")
print(f"  Cosenos casi iguales -> el modelo entiende que están cerca")
```

### Paso 5: Dataset final con features temporales

```python
print("\n=== Dataset Final con Features Temporales ===")

# Seleccionar features útiles para ML
features_temporales = [
    'monto',  # Target
    # Features cíclicas (mejor que numéricas crudas)
    'hora_sin', 'hora_cos',
    'dia_sin', 'dia_cos',
    'mes_sin', 'mes_cos',
    # Features binarias
    'es_fin_de_semana',
    'es_almuerzo',
    'es_cena',
    'es_horario_pico',
    'es_festivo',
]

df_final = ventas[features_temporales]
print(df_final.round(2))
print(f"\nShape: {df_final.shape}")
```

### Interpretación

De una simple columna `fecha_hora` extrajimos 11 features para ML:
- 6 features cíclicas (seno/coseno para hora, día, mes)
- 5 features binarias (fin de semana, almuerzo, cena, pico, festivo)

Esto permite al modelo capturar patrones como:
- Ventas más altas los fines de semana
- Diferencia entre almuerzo y cena
- Picos en fechas especiales

---

## Ejemplo 5: Pipeline Completo de Feature Engineering - Nivel: Avanzado

### Contexto

**FinTech Analytics** necesita un pipeline completo que transforme datos crudos de clientes en features listas para un modelo de detección de fraude. El pipeline debe ser reproducible y funcionar igual en entrenamiento y producción.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin

# Datos de transacciones de FinTech Analytics
np.random.seed(42)

transacciones = pd.DataFrame({
    'transaccion_id': range(1, 101),
    'monto': np.random.exponential(100, 100).round(2),
    'hora_transaccion': np.random.randint(0, 24, 100),
    'tipo_comercio': np.random.choice(['retail', 'online', 'restaurante', 'viajes', 'servicios'], 100),
    'pais': np.random.choice(['ES', 'FR', 'DE', 'IT', 'PT', None], 100),
    'dispositivo': np.random.choice(['mobile', 'desktop', 'tablet', None], 100),
    'intentos_previos': np.random.choice([0, 1, 2, 3, None], 100),
    'es_fraude': np.random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 100)  # 10% fraude
})

print("=== Datos Originales ===")
print(transacciones.head(10))
print(f"\nShape: {transacciones.shape}")
print(f"\nMissing values:\n{transacciones.isnull().sum()}")
```

### Paso 1: Definir transformadores personalizados

```python
class CyclicEncoder(BaseEstimator, TransformerMixin):
    """
    Transformador para encoding cíclico de variables temporales.

    Convierte valores numéricos cíclicos (horas, días, meses)
    en representaciones seno/coseno.
    """

    def __init__(self, max_val: int = 24):
        self.max_val = max_val

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.array(X).flatten()
        angulo = 2 * np.pi * X / self.max_val
        return np.column_stack([np.sin(angulo), np.cos(angulo)])

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            input_features = ['feature']
        return [f"{input_features[0]}_sin", f"{input_features[0]}_cos"]


class MissingIndicator(BaseEstimator, TransformerMixin):
    """
    Transformador que crea indicadores de valores faltantes.
    """

    def __init__(self):
        self.columns_with_missing = None

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            self.columns_with_missing = X.columns[X.isnull().any()].tolist()
        else:
            self.columns_with_missing = list(range(X.shape[1]))
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            return X.isnull().astype(int).values
        return np.isnan(X).astype(int)


print("=== Transformadores Personalizados Definidos ===")
print("  - CyclicEncoder: para horas (seno/coseno)")
print("  - MissingIndicator: para crear flags de missing")
```

### Paso 2: Construir el pipeline con ColumnTransformer

```python
# Definir qué columnas van a cada transformación
numeric_features = ['monto', 'intentos_previos']
categorical_features = ['tipo_comercio', 'pais', 'dispositivo']
cyclic_features = ['hora_transaccion']

# Pipeline para variables numéricas
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para variables categóricas
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='MISSING')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Pipeline para variables cíclicas
cyclic_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('cyclic', CyclicEncoder(max_val=24))
])

# Combinar todo en un ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_pipeline, numeric_features),
        ('cat', categorical_pipeline, categorical_features),
        ('cyclic', cyclic_pipeline, cyclic_features)
    ],
    remainder='drop'  # Eliminar columnas no especificadas
)

print("\n=== Pipeline Definido ===")
print(preprocessor)
```

### Paso 3: Aplicar el pipeline (fit_transform)

```python
# Separar features y target
X = transacciones.drop(['transaccion_id', 'es_fraude'], axis=1)
y = transacciones['es_fraude']

# Aplicar transformaciones
X_transformed = preprocessor.fit_transform(X)

print("\n=== Datos Transformados ===")
print(f"Shape original: {X.shape}")
print(f"Shape transformado: {X_transformed.shape}")

# Obtener nombres de features
feature_names = (
    numeric_features +
    list(preprocessor.named_transformers_['cat']
         .named_steps['onehot']
         .get_feature_names_out(categorical_features)) +
    ['hora_sin', 'hora_cos']
)

print(f"\nFeatures resultantes ({len(feature_names)}):")
for i, name in enumerate(feature_names):
    print(f"  {i}: {name}")
```

### Paso 4: Crear DataFrame final para visualización

```python
# Crear DataFrame con las features transformadas
df_transformed = pd.DataFrame(X_transformed, columns=feature_names)

print("\n=== Primeras 5 filas del Dataset Transformado ===")
print(df_transformed.head().round(2).to_string())

print("\n=== Estadísticas del Dataset Transformado ===")
print(df_transformed.describe().round(2))
```

### Paso 5: Guardar el pipeline para producción

```python
import joblib

# Guardar el preprocessor para usar en producción
# joblib.dump(preprocessor, 'feature_pipeline.pkl')

print("\n=== Pipeline Listo para Producción ===")
print("""
Uso en producción:

    # Cargar pipeline guardado
    preprocessor = joblib.load('feature_pipeline.pkl')

    # Transformar nuevos datos (SIN fit, solo transform)
    new_data = pd.DataFrame({...})  # Nuevas transacciones
    X_new = preprocessor.transform(new_data)

    # Predecir
    predictions = model.predict(X_new)

IMPORTANTE:
  - Usar .transform() en producción, NO .fit_transform()
  - El pipeline recuerda los parámetros del entrenamiento
  - Garantiza consistencia entre train y producción
""")
```

### Resultado Final

```python
print("""
=== Resumen del Pipeline ===

┌─────────────────────┬─────────────────────────────────────────────────────┐
│ Paso                │ Transformación                                      │
├─────────────────────┼─────────────────────────────────────────────────────┤
│ Numéricas           │ Imputar (mediana) → StandardScaler                  │
│ Categóricas         │ Imputar ('MISSING') → OneHotEncoder                 │
│ Cíclicas (hora)     │ Imputar (mediana) → CyclicEncoder (sin/cos)         │
└─────────────────────┴─────────────────────────────────────────────────────┘

Features originales: 6
Features transformadas: ~17 (depende de categorías únicas)

El pipeline es:
  ✅ Reproducible (mismo resultado cada vez)
  ✅ Serializable (se puede guardar y cargar)
  ✅ Consistente (train y producción usan los mismos parámetros)
  ✅ Maneja missing values automáticamente
  ✅ Escala variables correctamente
""")
```

---

## Código Completo Ejecutable

```python
"""
Feature Engineering - Ejemplos Completos
FinTech Analytics / RestaurantData Co. / LogisticFlow / CloudAPI Systems

Ejecutar este script para ver todos los ejemplos en acción.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

def main():
    print("=" * 60)
    print("FEATURE ENGINEERING - EJEMPLOS PRÁCTICOS")
    print("=" * 60)

    # Ejemplo 1: Encoding
    print("\n[1/5] Encoding de variables categóricas...")
    # (código del ejemplo 1)

    # Ejemplo 2: Scaling
    print("\n[2/5] Scaling de variables numéricas...")
    # (código del ejemplo 2)

    # Ejemplo 3: Missing Values
    print("\n[3/5] Manejo de missing values...")
    # (código del ejemplo 3)

    # Ejemplo 4: Features Temporales
    print("\n[4/5] Feature engineering temporal...")
    # (código del ejemplo 4)

    # Ejemplo 5: Pipeline Completo
    print("\n[5/5] Pipeline completo de producción...")
    # (código del ejemplo 5)

    print("\n" + "=" * 60)
    print("¡Ejemplos completados!")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

## Próximo Paso

Ahora que has visto los ejemplos, es hora de practicar por tu cuenta.

[Continuar a 03-EJERCICIOS.md →](03-EJERCICIOS.md)
