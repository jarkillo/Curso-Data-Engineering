# Ejercicios Prácticos: Feature Engineering

Estos ejercicios están diseñados para que practiques las técnicas de feature engineering vistas en la teoría y ejemplos. Cada ejercicio incluye contexto empresarial, datos, y una solución completa al final.

---

## Ejercicios Básicos

### Ejercicio 1: Label Encoding Ordenado

**Dificultad**: ⭐ Fácil

**Contexto**:
**LogisticFlow** tiene datos de envíos con una columna de prioridad que necesita convertirse en números para un modelo de predicción de tiempos.

**Datos**:
```python
import pandas as pd

envios = pd.DataFrame({
    'envio_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'prioridad': ['baja', 'alta', 'urgente', 'media', 'baja', 'urgente', 'media', 'alta'],
    'peso_kg': [2.5, 5.0, 1.2, 8.0, 3.5, 0.8, 6.0, 4.0]
})
```

**Pregunta**:
Convierte la columna `prioridad` a valores numéricos manteniendo el orden lógico: baja < media < alta < urgente.

**Pista**:
Usa un diccionario para mapear las categorías a números.

---

### Ejercicio 2: One-Hot Encoding

**Dificultad**: ⭐ Fácil

**Contexto**:
**RestaurantData Co.** necesita preparar datos de pedidos para un modelo de predicción de satisfacción.

**Datos**:
```python
pedidos = pd.DataFrame({
    'pedido_id': [1, 2, 3, 4, 5],
    'tipo_comida': ['pizza', 'sushi', 'hamburguesa', 'pizza', 'sushi'],
    'metodo_pago': ['efectivo', 'tarjeta', 'tarjeta', 'efectivo', 'app'],
    'monto': [25.50, 42.00, 18.00, 30.00, 38.00]
})
```

**Pregunta**:
Aplica One-Hot Encoding a `tipo_comida` y `metodo_pago`. ¿Cuántas columnas tendrá el dataset final?

**Pista**:
Usa `pd.get_dummies()` o `sklearn.preprocessing.OneHotEncoder`.

---

### Ejercicio 3: StandardScaler vs MinMaxScaler

**Dificultad**: ⭐ Fácil

**Contexto**:
**CloudAPI Systems** tiene métricas de rendimiento con escalas muy diferentes.

**Datos**:
```python
metricas = pd.DataFrame({
    'api_id': ['api_1', 'api_2', 'api_3', 'api_4', 'api_5'],
    'latencia_ms': [50, 120, 80, 200, 95],
    'requests_hora': [10000, 5000, 8000, 2000, 7000],
    'errores_porcentaje': [0.1, 0.5, 0.2, 1.2, 0.3]
})
```

**Pregunta**:
1. Aplica StandardScaler a las columnas numéricas
2. Aplica MinMaxScaler a las mismas columnas
3. ¿Cuál usarías si vas a entrenar una red neuronal? ¿Por qué?

**Pista**:
Recuerda: StandardScaler produce valores con media=0, std=1. MinMaxScaler produce valores en [0, 1].

---

## Ejercicios Intermedios

### Ejercicio 4: Imputación Estratégica

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**FinTech Analytics** tiene datos de clientes con valores faltantes que necesitan tratamiento diferenciado.

**Datos**:
```python
import numpy as np

clientes = pd.DataFrame({
    'cliente_id': range(1, 11),
    'edad': [25, np.nan, 35, 42, np.nan, 55, 28, np.nan, 48, 33],
    'ingresos': [30000, 45000, np.nan, 65000, 38000, np.nan, 42000, 55000, np.nan, 40000],
    'score_credito': [650, 720, 680, np.nan, 700, 750, np.nan, 690, 710, np.nan],
    'segmento': ['A', 'B', np.nan, 'A', 'B', 'A', np.nan, 'B', 'A', 'B']
})
```

**Pregunta**:
1. Imputa `edad` con la mediana
2. Imputa `ingresos` con la media
3. Imputa `score_credito` con la mediana
4. Imputa `segmento` con la moda
5. Crea columnas indicadoras de missing para cada variable

**Pista**:
Usa `SimpleImputer` de sklearn con diferentes estrategias.

---

### Ejercicio 5: Feature Engineering Temporal Completo

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RestaurantData Co.** quiere extraer todas las features posibles de las fechas de reserva.

**Datos**:
```python
reservas = pd.DataFrame({
    'reserva_id': range(1, 9),
    'fecha_hora': [
        '2024-02-14 19:30:00',  # San Valentín
        '2024-03-15 13:00:00',  # Viernes
        '2024-03-16 21:00:00',  # Sábado noche
        '2024-03-17 14:00:00',  # Domingo almuerzo
        '2024-12-24 20:30:00',  # Nochebuena
        '2024-12-31 22:00:00',  # Nochevieja
        '2024-01-01 13:30:00',  # Año Nuevo
        '2024-04-01 12:00:00',  # Lunes normal
    ],
    'num_personas': [2, 4, 6, 5, 8, 10, 4, 3]
})
reservas['fecha_hora'] = pd.to_datetime(reservas['fecha_hora'])
```

**Pregunta**:
Extrae las siguientes features:
1. Hora, día de semana, mes
2. Es fin de semana (bool)
3. Es almuerzo (12-15h) o cena (19-23h)
4. Es fecha especial (San Valentín, Nochebuena, Nochevieja, Año Nuevo)
5. Encoding cíclico de la hora (seno y coseno)

**Pista**:
Usa `.dt` accessor de pandas y define funciones auxiliares para fechas especiales.

---

### Ejercicio 6: Detección y Tratamiento de Outliers

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**LogisticFlow** tiene datos de tiempos de entrega donde algunos valores parecen erróneos.

**Datos**:
```python
entregas = pd.DataFrame({
    'entrega_id': range(1, 16),
    'tiempo_horas': [24, 48, 36, 72, 500, 42, 30, 55, 1000, 38,
                    45, 60, 28, 800, 52],
    'distancia_km': [100, 200, 150, 300, 180, 160, 120, 220, 250, 140,
                    170, 240, 110, 190, 200]
})
```

**Pregunta**:
1. Detecta outliers en `tiempo_horas` usando el método IQR
2. Detecta outliers usando Z-score (|z| > 3)
3. Aplica "capping" para limitar los outliers al percentil 95
4. ¿Cuántos outliers encontraste con cada método?

**Pista**:
IQR = Q3 - Q1, outliers son valores < Q1 - 1.5*IQR o > Q3 + 1.5*IQR

---

## Ejercicios Avanzados

### Ejercicio 7: Target Encoding con Validación

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**FinTech Analytics** tiene una variable categórica de alta cardinalidad (muchas categorías) que necesita encoding especial.

**Datos**:
```python
transacciones = pd.DataFrame({
    'transaccion_id': range(1, 21),
    'codigo_comercio': ['A001', 'B002', 'A001', 'C003', 'B002',
                        'A001', 'D004', 'B002', 'C003', 'A001',
                        'E005', 'A001', 'B002', 'C003', 'D004',
                        'A001', 'F006', 'B002', 'A001', 'C003'],
    'monto': [100, 250, 80, 500, 200, 120, 350, 180, 450, 90,
              600, 110, 220, 480, 380, 95, 700, 190, 105, 520],
    'es_fraude': [0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
})
```

**Pregunta**:
1. Calcula el target encoding para `codigo_comercio` (media de `es_fraude` por código)
2. ¿Por qué es peligroso hacer esto directamente? (pista: data leakage)
3. Implementa una versión con "smoothing" que mezcle la media global con la media del grupo

**Fórmula de smoothing**:
```
encoded = (count * mean_grupo + m * mean_global) / (count + m)
```
donde `m` es un parámetro de suavizado (ej: m=10)

**Pista**:
El smoothing ayuda cuando hay pocas observaciones en un grupo.

---

### Ejercicio 8: Pipeline de Features para Producción

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**CloudAPI Systems** necesita un pipeline de transformación que pueda usarse tanto en entrenamiento como en producción.

**Datos**:
```python
import numpy as np

logs_api = pd.DataFrame({
    'request_id': range(1, 51),
    'endpoint': np.random.choice(['/users', '/orders', '/products', '/auth'], 50),
    'metodo': np.random.choice(['GET', 'POST', 'PUT', 'DELETE'], 50),
    'latencia_ms': np.random.exponential(100, 50).round(2),
    'tamaño_response_kb': np.random.exponential(50, 50).round(2),
    'hora': np.random.randint(0, 24, 50),
    'codigo_status': np.random.choice([200, 201, 400, 404, 500, None], 50),
    'es_error': np.random.choice([0, 0, 0, 0, 1], 50)
})
```

**Pregunta**:
Crea un `ColumnTransformer` con los siguientes pipelines:
1. **Numéricas** (`latencia_ms`, `tamaño_response_kb`): Imputar con mediana → StandardScaler
2. **Categóricas** (`endpoint`, `metodo`): Imputar con 'UNKNOWN' → OneHotEncoder
3. **Cíclicas** (`hora`): Imputar con mediana → Encoding seno/coseno
4. **Status** (`codigo_status`): Imputar con 200 → OneHotEncoder

Además:
- Guarda el pipeline con joblib
- Demuestra cómo usarlo en "producción" con nuevos datos

**Pista**:
Usa `sklearn.compose.ColumnTransformer` y define transformadores para cada tipo.

---

### Ejercicio 9: Feature Engineering para Detección de Fraude

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**FinTech Analytics** necesita crear features especializadas para detectar transacciones fraudulentas.

**Datos**:
```python
# Historial de transacciones de un cliente
transacciones_cliente = pd.DataFrame({
    'transaccion_id': range(1, 16),
    'cliente_id': [1]*15,
    'fecha_hora': pd.date_range('2024-01-01 08:00', periods=15, freq='3H'),
    'monto': [50, 45, 200, 55, 48, 1500, 52, 47, 5000, 53,
              49, 51, 46, 3000, 50],
    'pais': ['ES', 'ES', 'ES', 'ES', 'ES', 'BR', 'ES', 'ES', 'RU', 'ES',
             'ES', 'ES', 'ES', 'CN', 'ES'],
    'tipo_comercio': ['retail', 'retail', 'online', 'retail', 'retail',
                      'online', 'retail', 'retail', 'online', 'retail',
                      'retail', 'retail', 'retail', 'online', 'retail']
})
```

**Pregunta**:
Crea las siguientes features de comportamiento:
1. `monto_vs_promedio_historico`: ratio del monto actual vs promedio de transacciones anteriores
2. `tiempo_desde_ultima_transaccion_horas`: tiempo desde la transacción anterior
3. `cambio_pais`: 1 si el país es diferente al de la transacción anterior, 0 si no
4. `transacciones_ultimas_24h`: conteo de transacciones en las últimas 24 horas
5. `monto_acumulado_24h`: suma de montos en las últimas 24 horas

**Pista**:
Usa `.shift()` para comparar con transacciones anteriores y `.rolling()` para ventanas temporales.

---

### Ejercicio 10: Validación de Feature Engineering

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
Antes de poner un pipeline de features en producción, necesitas validar que funciona correctamente.

**Datos**:
```python
# Dataset de entrenamiento
train_data = pd.DataFrame({
    'edad': [25, 30, 35, 40, 45, 50, 55, 60],
    'salario': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla', 'Barcelona', 'Madrid', 'Valencia'],
    'target': [0, 0, 1, 1, 1, 1, 1, 1]
})

# Nuevos datos de producción (pueden tener valores no vistos)
prod_data = pd.DataFrame({
    'edad': [28, 52],
    'salario': [35000, 85000],
    'ciudad': ['Madrid', 'Bilbao'],  # ¡Bilbao no estaba en train!
})
```

**Pregunta**:
1. Crea un pipeline que procese `train_data`
2. Aplica el mismo pipeline a `prod_data`
3. ¿Qué problema surge con la ciudad 'Bilbao'? ¿Cómo lo resuelves?
4. Escribe una función de validación que verifique:
   - No hay valores NaN en la salida
   - El número de features es consistente
   - Los rangos de valores son razonables

**Pista**:
Usa `handle_unknown='ignore'` en OneHotEncoder para manejar categorías nuevas.

---

## Soluciones

### Solución Ejercicio 1

```python
import pandas as pd

envios = pd.DataFrame({
    'envio_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'prioridad': ['baja', 'alta', 'urgente', 'media', 'baja', 'urgente', 'media', 'alta'],
    'peso_kg': [2.5, 5.0, 1.2, 8.0, 3.5, 0.8, 6.0, 4.0]
})

# Definir el orden lógico
orden_prioridad = {
    'baja': 0,
    'media': 1,
    'alta': 2,
    'urgente': 3
}

# Aplicar el mapeo
envios['prioridad_encoded'] = envios['prioridad'].map(orden_prioridad)

print(envios)
#    envio_id prioridad  peso_kg  prioridad_encoded
# 0         1      baja      2.5                  0
# 1         2      alta      5.0                  2
# 2         3   urgente      1.2                  3
# 3         4     media      8.0                  1
# ...

print("\nVerificación del orden:")
print("  baja (0) < media (1) < alta (2) < urgente (3)")
```

---

### Solución Ejercicio 2

```python
import pandas as pd

pedidos = pd.DataFrame({
    'pedido_id': [1, 2, 3, 4, 5],
    'tipo_comida': ['pizza', 'sushi', 'hamburguesa', 'pizza', 'sushi'],
    'metodo_pago': ['efectivo', 'tarjeta', 'tarjeta', 'efectivo', 'app'],
    'monto': [25.50, 42.00, 18.00, 30.00, 38.00]
})

# Aplicar One-Hot Encoding
pedidos_encoded = pd.get_dummies(
    pedidos,
    columns=['tipo_comida', 'metodo_pago'],
    prefix=['comida', 'pago']
)

print(pedidos_encoded)
print(f"\nColumnas originales: {len(pedidos.columns)}")
print(f"Columnas finales: {len(pedidos_encoded.columns)}")

# Respuesta:
# - tipo_comida tiene 3 categorías → 3 columnas
# - metodo_pago tiene 3 categorías → 3 columnas
# - Total: 2 (pedido_id, monto) + 3 + 3 = 8 columnas
```

---

### Solución Ejercicio 3

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

metricas = pd.DataFrame({
    'api_id': ['api_1', 'api_2', 'api_3', 'api_4', 'api_5'],
    'latencia_ms': [50, 120, 80, 200, 95],
    'requests_hora': [10000, 5000, 8000, 2000, 7000],
    'errores_porcentaje': [0.1, 0.5, 0.2, 1.2, 0.3]
})

numeric_cols = ['latencia_ms', 'requests_hora', 'errores_porcentaje']
datos = metricas[numeric_cols]

# StandardScaler
scaler_std = StandardScaler()
datos_std = pd.DataFrame(
    scaler_std.fit_transform(datos),
    columns=numeric_cols
)
print("=== StandardScaler ===")
print(datos_std.round(2))
print(f"Media: {datos_std.mean().round(4).tolist()}")
print(f"Std: {datos_std.std().round(4).tolist()}")

# MinMaxScaler
scaler_mm = MinMaxScaler()
datos_mm = pd.DataFrame(
    scaler_mm.fit_transform(datos),
    columns=numeric_cols
)
print("\n=== MinMaxScaler ===")
print(datos_mm.round(2))
print(f"Min: {datos_mm.min().tolist()}")
print(f"Max: {datos_mm.max().tolist()}")

print("\n=== Recomendación ===")
print("Para redes neuronales: MinMaxScaler")
print("Razón: Las funciones de activación (sigmoid, tanh) funcionan")
print("mejor con valores en rangos acotados [0,1] o [-1,1]")
```

---

### Solución Ejercicio 4

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

clientes = pd.DataFrame({
    'cliente_id': range(1, 11),
    'edad': [25, np.nan, 35, 42, np.nan, 55, 28, np.nan, 48, 33],
    'ingresos': [30000, 45000, np.nan, 65000, 38000, np.nan, 42000, 55000, np.nan, 40000],
    'score_credito': [650, 720, 680, np.nan, 700, 750, np.nan, 690, 710, np.nan],
    'segmento': ['A', 'B', np.nan, 'A', 'B', 'A', np.nan, 'B', 'A', 'B']
})

# Crear copia para trabajar
df = clientes.copy()

# 1. Indicadores de missing (antes de imputar)
for col in ['edad', 'ingresos', 'score_credito', 'segmento']:
    df[f'{col}_missing'] = df[col].isnull().astype(int)

# 2. Imputar edad con mediana
imputer_mediana = SimpleImputer(strategy='median')
df['edad'] = imputer_mediana.fit_transform(df[['edad']])

# 3. Imputar ingresos con media
imputer_media = SimpleImputer(strategy='mean')
df['ingresos'] = imputer_media.fit_transform(df[['ingresos']])

# 4. Imputar score_credito con mediana
df['score_credito'] = imputer_mediana.fit_transform(df[['score_credito']])

# 5. Imputar segmento con moda
imputer_moda = SimpleImputer(strategy='most_frequent')
df['segmento'] = imputer_moda.fit_transform(df[['segmento']]).ravel()

print("=== Dataset Imputado ===")
print(df)
print(f"\nMissing values restantes: {df.isnull().sum().sum()}")
```

---

### Solución Ejercicio 5

```python
import pandas as pd
import numpy as np

reservas = pd.DataFrame({
    'reserva_id': range(1, 9),
    'fecha_hora': pd.to_datetime([
        '2024-02-14 19:30:00', '2024-03-15 13:00:00',
        '2024-03-16 21:00:00', '2024-03-17 14:00:00',
        '2024-12-24 20:30:00', '2024-12-31 22:00:00',
        '2024-01-01 13:30:00', '2024-04-01 12:00:00',
    ]),
    'num_personas': [2, 4, 6, 5, 8, 10, 4, 3]
})

# 1. Features básicas
reservas['hora'] = reservas['fecha_hora'].dt.hour
reservas['dia_semana'] = reservas['fecha_hora'].dt.dayofweek
reservas['mes'] = reservas['fecha_hora'].dt.month

# 2. Es fin de semana
reservas['es_fin_de_semana'] = (reservas['dia_semana'] >= 5).astype(int)

# 3. Almuerzo o cena
reservas['es_almuerzo'] = ((reservas['hora'] >= 12) & (reservas['hora'] <= 15)).astype(int)
reservas['es_cena'] = ((reservas['hora'] >= 19) & (reservas['hora'] <= 23)).astype(int)

# 4. Fechas especiales
fechas_especiales = {
    (2, 14): 'san_valentin',
    (12, 24): 'nochebuena',
    (12, 31): 'nochevieja',
    (1, 1): 'año_nuevo'
}

def identificar_fecha_especial(fecha):
    key = (fecha.month, fecha.day)
    return 1 if key in fechas_especiales else 0

reservas['es_fecha_especial'] = reservas['fecha_hora'].apply(identificar_fecha_especial)

# 5. Encoding cíclico de hora
reservas['hora_sin'] = np.sin(2 * np.pi * reservas['hora'] / 24)
reservas['hora_cos'] = np.cos(2 * np.pi * reservas['hora'] / 24)

print("=== Features Temporales Extraídas ===")
print(reservas.round(2))
```

---

### Solución Ejercicio 6

```python
import pandas as pd
import numpy as np
from scipy import stats

entregas = pd.DataFrame({
    'entrega_id': range(1, 16),
    'tiempo_horas': [24, 48, 36, 72, 500, 42, 30, 55, 1000, 38,
                    45, 60, 28, 800, 52],
    'distancia_km': [100, 200, 150, 300, 180, 160, 120, 220, 250, 140,
                    170, 240, 110, 190, 200]
})

# 1. Detección con IQR
Q1 = entregas['tiempo_horas'].quantile(0.25)
Q3 = entregas['tiempo_horas'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers_iqr = entregas[
    (entregas['tiempo_horas'] < limite_inferior) |
    (entregas['tiempo_horas'] > limite_superior)
]
print(f"=== Método IQR ===")
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
print(f"Límites: [{limite_inferior:.0f}, {limite_superior:.0f}]")
print(f"Outliers encontrados: {len(outliers_iqr)}")
print(outliers_iqr[['entrega_id', 'tiempo_horas']])

# 2. Detección con Z-score
z_scores = np.abs(stats.zscore(entregas['tiempo_horas']))
outliers_zscore = entregas[z_scores > 3]
print(f"\n=== Método Z-score (|z| > 3) ===")
print(f"Outliers encontrados: {len(outliers_zscore)}")
print(outliers_zscore[['entrega_id', 'tiempo_horas']])

# 3. Capping al percentil 95
p95 = entregas['tiempo_horas'].quantile(0.95)
entregas['tiempo_horas_capped'] = entregas['tiempo_horas'].clip(upper=p95)

print(f"\n=== Capping al percentil 95 ({p95:.0f} horas) ===")
print(entregas[['entrega_id', 'tiempo_horas', 'tiempo_horas_capped']])
```

---

### Solución Ejercicio 7

```python
import pandas as pd
import numpy as np

transacciones = pd.DataFrame({
    'transaccion_id': range(1, 21),
    'codigo_comercio': ['A001', 'B002', 'A001', 'C003', 'B002',
                        'A001', 'D004', 'B002', 'C003', 'A001',
                        'E005', 'A001', 'B002', 'C003', 'D004',
                        'A001', 'F006', 'B002', 'A001', 'C003'],
    'monto': [100, 250, 80, 500, 200, 120, 350, 180, 450, 90,
              600, 110, 220, 480, 380, 95, 700, 190, 105, 520],
    'es_fraude': [0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
})

# 1. Target encoding simple (PELIGROSO - solo para demostración)
target_means = transacciones.groupby('codigo_comercio')['es_fraude'].mean()
transacciones['target_encoded_simple'] = transacciones['codigo_comercio'].map(target_means)

print("=== Target Encoding Simple ===")
print(target_means)

# 2. Por qué es peligroso: DATA LEAKAGE
print("\n=== ¿Por qué es peligroso? ===")
print("El encoding usa información del target (es_fraude) que no")
print("tendríamos en producción. El modelo 'hace trampa' aprendiendo")
print("la respuesta directamente del encoding.")

# 3. Target encoding con smoothing
m = 10  # Parámetro de suavizado
mean_global = transacciones['es_fraude'].mean()

def smooth_target_encoding(group):
    count = len(group)
    mean_grupo = group['es_fraude'].mean()
    return (count * mean_grupo + m * mean_global) / (count + m)

target_means_smoothed = transacciones.groupby('codigo_comercio').apply(smooth_target_encoding)
transacciones['target_encoded_smoothed'] = transacciones['codigo_comercio'].map(target_means_smoothed)

print(f"\n=== Target Encoding con Smoothing (m={m}) ===")
print(f"Media global: {mean_global:.3f}")
comparison = pd.DataFrame({
    'simple': target_means,
    'smoothed': target_means_smoothed
})
print(comparison.round(3))
print("\nNota: Códigos con pocas observaciones (E005, F006) se acercan")
print("más a la media global con smoothing.")
```

---

### Solución Ejercicio 8

```python
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib

# Datos
np.random.seed(42)
logs_api = pd.DataFrame({
    'request_id': range(1, 51),
    'endpoint': np.random.choice(['/users', '/orders', '/products', '/auth'], 50),
    'metodo': np.random.choice(['GET', 'POST', 'PUT', 'DELETE'], 50),
    'latencia_ms': np.random.exponential(100, 50).round(2),
    'tamaño_response_kb': np.random.exponential(50, 50).round(2),
    'hora': np.random.randint(0, 24, 50),
    'codigo_status': np.random.choice([200, 201, 400, 404, 500, None], 50),
    'es_error': np.random.choice([0, 0, 0, 0, 1], 50)
})

# Transformador cíclico personalizado
class CyclicEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, max_val=24):
        self.max_val = max_val

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.array(X).flatten()
        angulo = 2 * np.pi * X / self.max_val
        return np.column_stack([np.sin(angulo), np.cos(angulo)])

# Definir pipelines
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='UNKNOWN')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

cyclic_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('cyclic', CyclicEncoder(max_val=24))
])

status_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=200)),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combinar en ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, ['latencia_ms', 'tamaño_response_kb']),
    ('cat', categorical_pipeline, ['endpoint', 'metodo']),
    ('cyclic', cyclic_pipeline, ['hora']),
    ('status', status_pipeline, ['codigo_status'])
])

# Separar features y target
X = logs_api.drop(['request_id', 'es_error'], axis=1)
y = logs_api['es_error']

# Entrenar el pipeline
X_transformed = preprocessor.fit_transform(X)
print(f"Shape original: {X.shape}")
print(f"Shape transformado: {X_transformed.shape}")

# Guardar para producción
joblib.dump(preprocessor, 'api_feature_pipeline.pkl')

# Simular uso en producción
print("\n=== Uso en Producción ===")
nuevo_request = pd.DataFrame({
    'endpoint': ['/users'],
    'metodo': ['GET'],
    'latencia_ms': [150.0],
    'tamaño_response_kb': [25.0],
    'hora': [14],
    'codigo_status': [200]
})

# Cargar y usar
preprocessor_prod = joblib.load('api_feature_pipeline.pkl')
X_nuevo = preprocessor_prod.transform(nuevo_request)
print(f"Nuevo request transformado: shape {X_nuevo.shape}")
```

---

### Solución Ejercicio 9

```python
import pandas as pd
import numpy as np

transacciones_cliente = pd.DataFrame({
    'transaccion_id': range(1, 16),
    'cliente_id': [1]*15,
    'fecha_hora': pd.date_range('2024-01-01 08:00', periods=15, freq='3H'),
    'monto': [50, 45, 200, 55, 48, 1500, 52, 47, 5000, 53,
              49, 51, 46, 3000, 50],
    'pais': ['ES', 'ES', 'ES', 'ES', 'ES', 'BR', 'ES', 'ES', 'RU', 'ES',
             'ES', 'ES', 'ES', 'CN', 'ES'],
    'tipo_comercio': ['retail', 'retail', 'online', 'retail', 'retail',
                      'online', 'retail', 'retail', 'online', 'retail',
                      'retail', 'retail', 'retail', 'online', 'retail']
})

df = transacciones_cliente.copy()

# 1. Monto vs promedio histórico
df['promedio_anterior'] = df['monto'].expanding().mean().shift(1)
df['monto_vs_promedio'] = df['monto'] / df['promedio_anterior']

# 2. Tiempo desde última transacción
df['tiempo_desde_anterior'] = df['fecha_hora'].diff().dt.total_seconds() / 3600

# 3. Cambio de país
df['pais_anterior'] = df['pais'].shift(1)
df['cambio_pais'] = (df['pais'] != df['pais_anterior']).astype(int)

# 4. Transacciones últimas 24h (usando rolling con ventana de tiempo)
df = df.set_index('fecha_hora')
df['transacciones_24h'] = df['monto'].rolling('24H').count()
df = df.reset_index()

# 5. Monto acumulado últimas 24h
df = df.set_index('fecha_hora')
df['monto_acumulado_24h'] = df['monto'].rolling('24H').sum()
df = df.reset_index()

print("=== Features de Comportamiento para Detección de Fraude ===")
features_fraude = ['transaccion_id', 'monto', 'pais', 'monto_vs_promedio',
                   'tiempo_desde_anterior', 'cambio_pais', 'transacciones_24h',
                   'monto_acumulado_24h']
print(df[features_fraude].round(2))

print("\n=== Observaciones ===")
print("- Transacción 6 (BR, 1500): monto_vs_promedio muy alto + cambio de país")
print("- Transacción 9 (RU, 5000): monto extremo + cambio de país")
print("- Transacción 14 (CN, 3000): monto alto + cambio de país")
print("Estas serían candidatas a fraude.")
```

---

### Solución Ejercicio 10

```python
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Datos de entrenamiento
train_data = pd.DataFrame({
    'edad': [25, 30, 35, 40, 45, 50, 55, 60],
    'salario': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Madrid', 'Sevilla', 'Barcelona', 'Madrid', 'Valencia'],
    'target': [0, 0, 1, 1, 1, 1, 1, 1]
})

# Datos de producción (con categoría nueva)
prod_data = pd.DataFrame({
    'edad': [28, 52],
    'salario': [35000, 85000],
    'ciudad': ['Madrid', 'Bilbao'],  # Bilbao es nueva
})

# 1. Crear pipeline
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='UNKNOWN')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))  # ¡IMPORTANTE!
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, ['edad', 'salario']),
    ('cat', categorical_pipeline, ['ciudad'])
])

# 2. Entrenar con train_data
X_train = train_data.drop('target', axis=1)
X_train_transformed = preprocessor.fit_transform(X_train)

print("=== Entrenamiento ===")
print(f"Shape: {X_train_transformed.shape}")
print(f"Categorías aprendidas: {preprocessor.named_transformers_['cat'].named_steps['onehot'].categories_}")

# 3. Aplicar a prod_data
X_prod_transformed = preprocessor.transform(prod_data)

print("\n=== Producción ===")
print(f"Shape: {X_prod_transformed.shape}")
print("Nota: Bilbao se maneja correctamente con handle_unknown='ignore'")
print("      (todas las columnas de ciudad serán 0 para Bilbao)")

# 4. Función de validación
def validar_features(X_transformed, expected_shape, name="datos"):
    """Valida que las features transformadas sean correctas."""
    errores = []

    # Check NaN
    if np.isnan(X_transformed).any():
        errores.append(f"Hay valores NaN en {name}")

    # Check shape
    if X_transformed.shape[1] != expected_shape:
        errores.append(f"Shape incorrecto: esperado {expected_shape}, obtenido {X_transformed.shape[1]}")

    # Check rangos razonables
    if np.abs(X_transformed).max() > 100:
        errores.append(f"Valores muy extremos detectados (max: {np.abs(X_transformed).max():.2f})")

    if errores:
        print(f"❌ Validación fallida para {name}:")
        for e in errores:
            print(f"   - {e}")
        return False
    else:
        print(f"✅ Validación exitosa para {name}")
        return True

# Ejecutar validación
print("\n=== Validación ===")
expected_features = X_train_transformed.shape[1]
validar_features(X_train_transformed, expected_features, "entrenamiento")
validar_features(X_prod_transformed, expected_features, "producción")
```

---

## Próximo Paso

Has completado los ejercicios de Feature Engineering. Ahora es momento de aplicar todo en un proyecto práctico completo.

[Continuar a 04-proyecto-practico →](04-proyecto-practico/)
