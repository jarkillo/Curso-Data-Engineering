# Feature Engineering: El Arte de Preparar Datos para Machine Learning

## Introducción

### ¿Por qué es tan importante el Feature Engineering?

Imagina que eres un chef preparando un plato gourmet. Podrías tener los mejores ingredientes del mundo, pero si no los preparas correctamente —si no los cortas bien, no los sazonas adecuadamente, o no los cocinas en el orden correcto— el resultado será mediocre.

**Feature Engineering es exactamente eso: el arte de preparar tus ingredientes (datos) para que el modelo de Machine Learning (el "horno") pueda producir el mejor resultado posible.**

En el mundo real del Data Engineering, esto es aún más crítico porque:

1. **Los datos crudos casi nunca están listos** para ser usados directamente
2. **El 80% del trabajo de ML** es preparación de datos (no entrenar modelos)
3. **Un buen feature engineering** puede hacer que un modelo simple supere a uno complejo
4. **La calidad de tus features** determina el techo de rendimiento de cualquier modelo

### Contexto en Data Engineering

Como Data Engineer, tu responsabilidad no es solo mover datos de A a B. Cada vez más, los equipos esperan que puedas:

- Crear pipelines de transformación de features **reproducibles y escalables**
- Diseñar sistemas que generen features **consistentes** entre entrenamiento y producción
- Implementar validaciones que detecten **data drift** y anomalías
- Versionar features junto con los datos y modelos

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tu Rol como Data Engineer                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Datos Crudos ──▶ [Feature Engineering] ──▶ Features Limpias  │
│                                                                 │
│   • Automatizar transformaciones                                │
│   • Garantizar reproducibilidad                                 │
│   • Escalar a producción                                        │
│   • Monitorear calidad                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conceptos Fundamentales

### Concepto 1: ¿Qué es una Feature?

Una **feature** (característica) es una propiedad medible de tus datos que el modelo usará para hacer predicciones.

**Analogía del mundo real**: Imagina que quieres predecir si lloverá mañana. Las features serían cosas como:
- Temperatura actual (numérica)
- Humedad (numérica)
- Dirección del viento (categórica)
- ¿Está nublado? (binaria)

Cada una de estas propiedades le da información al modelo para tomar su decisión.

**En Data Engineering**, trabajamos con features todo el tiempo sin llamarlas así:
- Columnas en una tabla SQL
- Campos en un JSON
- Atributos en un registro de log

La diferencia es que en ML necesitamos transformar estas columnas a **formatos que los algoritmos puedan entender**.

```python
# Datos crudos (no aptos para ML)
cliente = {
    "nombre": "María García",      # Texto - el modelo no puede usar esto directamente
    "fecha_registro": "2023-01-15", # Fecha - necesita transformación
    "ciudad": "Madrid",             # Categoría - necesita encoding
    "total_compras": 1500.50        # Numérico - ¡esto sí puede usarlo!
}

# Features transformadas (aptas para ML)
features = {
    "dias_como_cliente": 365,       # Transformación de fecha
    "ciudad_madrid": 1,             # One-hot encoding
    "ciudad_barcelona": 0,
    "total_compras": 1500.50,       # Ya era numérico
    "total_compras_normalizado": 0.75  # Escalado entre 0 y 1
}
```

### Concepto 2: Tipos de Features

Los modelos de ML trabajan con **números**. Por eso, necesitamos entender qué tipos de datos tenemos y cómo convertirlos.

#### 2.1 Features Numéricas

Son valores numéricos que pueden ser:

**Continuas**: Pueden tomar cualquier valor en un rango
- Temperatura: 23.5°C, 24.1°C, 24.15°C...
- Precio: 19.99€, 199.50€...
- Edad en días: 10950.5 días

**Discretas**: Solo toman valores enteros
- Número de compras: 0, 1, 2, 3...
- Cantidad de productos: 1, 2, 3...
- Año: 2020, 2021, 2022...

**Aplicación en Data Engineering**: Las features numéricas suelen requerir **scaling** (escalado) porque los modelos son sensibles a las magnitudes. Un salario de 50,000€ no debería "pesar" más que una edad de 30 años solo porque el número es más grande.

#### 2.2 Features Categóricas

Representan categorías o grupos:

**Nominales**: Sin orden inherente
- Color: rojo, azul, verde
- Ciudad: Madrid, Barcelona, Valencia
- Tipo de producto: electrónica, ropa, alimentación

**Ordinales**: Con orden significativo
- Educación: primaria < secundaria < universidad < máster
- Satisfacción: muy_malo < malo < neutral < bueno < muy_bueno
- Talla: XS < S < M < L < XL

**Aplicación en Data Engineering**: Estas features necesitan **encoding** (codificación) para convertirse en números que el modelo entienda.

#### 2.3 Features Temporales

Fechas y tiempos que esconden información valiosa:

```python
fecha = "2024-03-15 14:30:00"

# De una fecha podemos extraer MUCHAS features:
features_temporales = {
    "hora": 14,                    # Hora del día
    "dia_semana": 4,               # Viernes (0=lunes)
    "es_fin_de_semana": False,     # Binaria
    "mes": 3,                      # Marzo
    "trimestre": 1,                # Q1
    "dias_desde_inicio_año": 75,   # Día del año
    "es_festivo": False,           # Requiere calendario
}
```

**Aplicación en Data Engineering**: El procesamiento de fechas es donde el Data Engineer brilla. Saber extraer estas features puede ser la diferencia entre un modelo mediocre y uno excelente.

#### 2.4 Features de Texto

Texto libre que necesita procesamiento especial:

- Descripciones de productos
- Comentarios de usuarios
- Logs de sistema

**Aplicación en Data Engineering**: Este tema merece un módulo completo (NLP). Por ahora, lo mencionamos para que sepas que existe, pero no lo cubriremos en profundidad aquí.

---

### Concepto 3: Encoding de Variables Categóricas

**El problema**: Los modelos de ML no entienden "Madrid" o "Barcelona". Necesitan números.

**Analogía**: Es como traducir de un idioma a otro. El modelo "habla números" y tus datos "hablan texto". Necesitas un traductor (encoder).

#### 3.1 Label Encoding

Asigna un número único a cada categoría.

```python
# Original
ciudades = ["Madrid", "Barcelona", "Valencia", "Madrid", "Barcelona"]

# Label Encoding
# Madrid = 0, Barcelona = 1, Valencia = 2
ciudades_encoded = [0, 1, 2, 0, 1]
```

**Cuándo usarlo**:
- Variables ordinales (donde el orden importa)
- Algoritmos basados en árboles (Random Forest, XGBoost)

**Cuándo NO usarlo**:
- Variables nominales con modelos lineales (el modelo pensará que Valencia > Barcelona > Madrid)

#### 3.2 One-Hot Encoding

Crea una columna binaria (0/1) para cada categoría.

```python
# Original
ciudades = ["Madrid", "Barcelona", "Valencia"]

# One-Hot Encoding
#              Madrid  Barcelona  Valencia
# Madrid    →    1        0          0
# Barcelona →    0        1          0
# Valencia  →    0        0          1
```

**Cuándo usarlo**:
- Variables nominales (sin orden)
- Modelos lineales, redes neuronales
- Cuando tienes pocas categorías (< 10-15)

**Cuándo NO usarlo**:
- Muchas categorías (100 ciudades = 100 columnas nuevas)
- Puede causar "curse of dimensionality"

#### 3.3 Target Encoding (Mean Encoding)

Reemplaza cada categoría por la media del target para esa categoría.

```python
# Datos: predecir si un cliente comprará (1) o no (0)
# ciudad      compró
# Madrid        1
# Madrid        1
# Madrid        0
# Barcelona     0
# Barcelona     0

# Target Encoding
# Media de Madrid = (1+1+0)/3 = 0.67
# Media de Barcelona = (0+0)/2 = 0.0

# ciudad_encoded
# 0.67  (era Madrid)
# 0.67  (era Madrid)
# 0.67  (era Madrid)
# 0.0   (era Barcelona)
# 0.0   (era Barcelona)
```

**Cuándo usarlo**:
- Muchas categorías (alta cardinalidad)
- Cuando hay relación entre la categoría y el target

**Cuidado**:
- Riesgo de **data leakage** (filtración de información del target)
- Usar siempre con cross-validation

#### Comparación Rápida

| Método | Cardinalidad | Tipo Variable | Riesgo Leakage |
|--------|--------------|---------------|----------------|
| Label Encoding | Cualquiera | Ordinal | Bajo |
| One-Hot | Baja (<15) | Nominal | Bajo |
| Target Encoding | Alta (>15) | Cualquiera | **Alto** |

---

### Concepto 4: Scaling y Normalización

**El problema**: Las features numéricas tienen diferentes escalas.

```python
# Sin scaling
edad = 25           # Rango típico: 0-100
salario = 50000     # Rango típico: 20000-200000
```

Un modelo lineal pensará que el salario es "más importante" simplemente porque los números son más grandes. **Esto es incorrecto.**

**Analogía**: Imagina comparar la velocidad de un coche (200 km/h) con la de una persona (10 km/h). Si solo miras los números, el coche parece 20 veces "mejor". Pero si normalizas (coche al 100% de su capacidad vs persona al 100%), ambos están dando su máximo esfuerzo.

#### 4.1 StandardScaler (Z-score normalization)

Transforma los datos para que tengan media=0 y desviación estándar=1.

```
z = (x - media) / desviación_estándar
```

```python
# Original: [10, 20, 30, 40, 50]
# Media = 30, Std = 14.14
# Resultado: [-1.41, -0.71, 0, 0.71, 1.41]
```

**Cuándo usarlo**:
- Datos con distribución aproximadamente normal
- Modelos que asumen normalidad (regresión lineal, SVM)
- Redes neuronales

#### 4.2 MinMaxScaler

Escala los datos a un rango específico (generalmente 0-1).

```
x_scaled = (x - min) / (max - min)
```

```python
# Original: [10, 20, 30, 40, 50]
# Min = 10, Max = 50
# Resultado: [0, 0.25, 0.5, 0.75, 1.0]
```

**Cuándo usarlo**:
- Cuando necesitas valores acotados (0-1)
- Redes neuronales con activaciones sigmoides
- Algoritmos sensibles a la escala

**Cuidado**:
- Muy sensible a outliers (un valor extremo distorsiona todo)

#### 4.3 RobustScaler

Usa la mediana y el rango intercuartílico (IQR), resistente a outliers.

```
x_scaled = (x - mediana) / IQR
```

**Cuándo usarlo**:
- Datos con outliers que no quieres eliminar
- Cuando StandardScaler da resultados sesgados

#### Comparación de Scalers

| Scaler | Sensible a Outliers | Rango Resultado | Mejor Para |
|--------|---------------------|-----------------|------------|
| Standard | Sí | Sin límites | Datos normales |
| MinMax | **Muy** | [0, 1] | Redes neuronales |
| Robust | No | Sin límites | Datos con outliers |

---

### Concepto 5: Manejo de Missing Values (Valores Faltantes)

**El problema**: Los datos del mundo real siempre tienen huecos.

```python
# Datos reales de clientes
clientes = [
    {"edad": 25, "salario": 30000, "ciudad": "Madrid"},
    {"edad": None, "salario": 45000, "ciudad": "Barcelona"},  # Falta edad
    {"edad": 35, "salario": None, "ciudad": "Valencia"},      # Falta salario
    {"edad": 40, "salario": 55000, "ciudad": None},           # Falta ciudad
]
```

**Analogía**: Es como un cuestionario donde algunos encuestados dejaron preguntas en blanco. ¿Qué haces? ¿Los ignoras? ¿Inventas respuestas? ¿Usas la respuesta más común?

#### Estrategias de Imputación

**5.1 Eliminar filas (Listwise deletion)**
```python
# Eliminar cualquier fila con valores faltantes
# Resultado: Solo queda 1 fila de 4
```
- **Pros**: Simple, mantiene la integridad de los datos restantes
- **Contras**: Pierdes mucha información si hay muchos missing

**5.2 Imputación con la media/mediana**
```python
# Reemplazar valores faltantes con la media de la columna
edad_media = (25 + 35 + 40) / 3 = 33.33
# El None de edad se convierte en 33.33
```
- **Pros**: Simple, conserva el tamaño del dataset
- **Contras**: Reduce la varianza, puede introducir sesgo

**5.3 Imputación con la moda (para categóricas)**
```python
# Reemplazar con el valor más frecuente
# Si "Madrid" aparece más, el None de ciudad = "Madrid"
```

**5.4 Imputación por grupo**
```python
# Calcular la media por grupo (más sofisticado)
# Si la edad falta para alguien de Barcelona,
# usar la media de edad de los clientes de Barcelona
```

**5.5 Indicador de missing**
```python
# Crear una feature nueva que indique "faltaba este valor"
{"edad": 33.33, "edad_was_missing": 1, ...}
```
A veces el hecho de que falte un valor ES información útil.

#### Cuándo Usar Cada Estrategia

| Estrategia | % Missing | Tipo de Dato | Aleatorio |
|------------|-----------|--------------|-----------|
| Eliminar | <5% | Cualquiera | Sí |
| Media | 5-20% | Numérico | Sí |
| Mediana | 5-20% | Numérico con outliers | Sí |
| Moda | 5-20% | Categórico | Sí |
| Por grupo | >20% | Cualquiera | No |
| Indicador | Cualquier % | Cualquiera | No |

---

### Concepto 6: Manejo de Outliers

**El problema**: Valores extremos que pueden distorsionar tu modelo.

```python
salarios = [30000, 35000, 40000, 42000, 38000, 500000]  # ¿CEO infiltrado?
```

**Analogía**: Si calculas el salario promedio de una empresa y entra Jeff Bezos a trabajar, de repente el "promedio" no representa a nadie.

#### Detección de Outliers

**6.1 Método IQR (Rango Intercuartílico)**
```python
Q1 = percentil_25
Q3 = percentil_75
IQR = Q3 - Q1

# Outliers: valores fuera de [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
```

**6.2 Z-score**
```python
z = (x - media) / std

# Outliers: |z| > 3 (más de 3 desviaciones estándar)
```

#### Tratamiento de Outliers

**No siempre hay que eliminarlos.** A veces un outlier es información valiosa (fraude, error de sistema, cliente VIP).

| Acción | Cuándo Usarla |
|--------|---------------|
| **Eliminar** | Error obvio de datos |
| **Capping** | Reducir impacto sin eliminar |
| **Transformar** (log) | Datos con distribución sesgada |
| **Mantener** | El outlier es información real |

---

### Concepto 7: Feature Engineering Temporal

Las fechas son minas de oro de información.

**Analogía**: Si te digo "15 de marzo de 2024 a las 14:30", no es solo una fecha. Es:
- Viernes (día de más ventas en retail)
- Después de almuerzo (la gente compra diferente)
- Fin de Q1 (cierre fiscal para muchas empresas)
- Primavera en el hemisferio norte

```python
def extraer_features_temporales(fecha: datetime) -> dict:
    """
    Extrae múltiples features de una fecha.

    Args:
        fecha: Objeto datetime

    Returns:
        Diccionario con features temporales
    """
    return {
        # Cíclicas
        "hora": fecha.hour,
        "dia_semana": fecha.weekday(),
        "dia_mes": fecha.day,
        "mes": fecha.month,
        "trimestre": (fecha.month - 1) // 3 + 1,

        # Binarias
        "es_fin_de_semana": fecha.weekday() >= 5,
        "es_horario_laboral": 9 <= fecha.hour <= 18,

        # Derivadas
        "dia_del_año": fecha.timetuple().tm_yday,
        "semana_del_año": fecha.isocalendar()[1],
    }
```

#### Features Cíclicas

El problema: hora 23 y hora 0 están "cerca" en la realidad, pero para el modelo son muy diferentes (23 vs 0).

**Solución: Encoding Seno/Coseno**

```python
import numpy as np

def encode_ciclico(valor: int, max_valor: int) -> tuple[float, float]:
    """
    Codifica un valor cíclico usando seno y coseno.

    Args:
        valor: Valor a codificar (ej: hora 14)
        max_valor: Valor máximo del ciclo (ej: 24 para horas)

    Returns:
        Tupla (seno, coseno) que representa el valor
    """
    angulo = 2 * np.pi * valor / max_valor
    return np.sin(angulo), np.cos(angulo)

# Ejemplo: hora 23 y hora 1 están cerca en el espacio seno/coseno
hora_23 = encode_ciclico(23, 24)  # (−0.26, 0.97)
hora_1 = encode_ciclico(1, 24)    # (0.26, 0.97)
# ¡Cosenos casi iguales! El modelo entiende que están cerca
```

---

## Aplicaciones Prácticas en Data Engineering

### Caso de Uso 1: Pipeline de Features para E-commerce

```python
# Típico flujo en un e-commerce
def crear_features_cliente(df_transacciones: pd.DataFrame) -> pd.DataFrame:
    """
    Crea features de cliente desde transacciones.

    Este es el tipo de pipeline que crearás como Data Engineer.
    """
    return df_transacciones.groupby('cliente_id').agg({
        # Features de recency
        'fecha': lambda x: (datetime.now() - x.max()).days,  # Días desde última compra

        # Features de frecuencia
        'transaccion_id': 'count',  # Número de compras

        # Features monetarias
        'monto': ['sum', 'mean', 'std'],  # Total, promedio, variabilidad

        # Features de productos
        'categoria': lambda x: x.nunique(),  # Diversidad de categorías
    })
```

### Caso de Uso 2: Detección de Fraude

```python
# Features típicas para detectar fraude
features_fraude = {
    # Velocidad de transacciones
    "transacciones_ultima_hora": 5,
    "tiempo_desde_ultima_transaccion_minutos": 2,

    # Patrones geográficos
    "distancia_desde_ultima_transaccion_km": 500,
    "pais_diferente_al_habitual": True,

    # Patrones de comportamiento
    "monto_vs_promedio_historico": 3.5,  # 3.5 veces el promedio
    "categoria_nueva": True,
    "horario_inusual": True,
}
```

### Caso de Uso 3: Predicción de Churn

```python
# Features para predecir abandono de clientes
features_churn = {
    # Engagement
    "dias_desde_ultimo_login": 15,
    "sesiones_ultimo_mes": 3,
    "funciones_usadas_pct": 0.2,  # Solo usa 20% del producto

    # Tendencia
    "tendencia_uso_30d": -0.5,  # Bajando
    "tickets_soporte_ultimo_mes": 4,
    "nps_score": 3,  # Bajo

    # Financiero
    "meses_en_plan_actual": 11,  # Próximo a renovar
    "intentos_cancelacion": 1,
}
```

---

## Errores Comunes

### Error 1: Data Leakage (Filtración de Datos)

**Qué es**: Usar información que no tendrías en producción durante el entrenamiento.

```python
# ❌ INCORRECTO: Calculando el scaler con TODOS los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Incluye datos de test
X_train, X_test = train_test_split(X_scaled)

# ✅ CORRECTO: Calculando el scaler solo con datos de entrenamiento
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Solo fit en train
X_test_scaled = scaler.transform(X_test)         # Solo transform en test
```

**Por qué importa**: Tu modelo tendrá métricas increíbles en desarrollo pero fallará en producción.

### Error 2: No Guardar los Transformadores

```python
# ❌ INCORRECTO: Crear un nuevo scaler en producción
def predict_production(new_data):
    scaler = StandardScaler()  # ¡Nuevo scaler con diferentes parámetros!
    scaled = scaler.fit_transform(new_data)  # Escalado diferente
    return model.predict(scaled)

# ✅ CORRECTO: Guardar y reutilizar el mismo scaler
import joblib

# Durante entrenamiento
joblib.dump(scaler, 'scaler.pkl')

# En producción
scaler = joblib.load('scaler.pkl')
def predict_production(new_data):
    scaled = scaler.transform(new_data)  # Mismo escalado que en entrenamiento
    return model.predict(scaled)
```

### Error 3: Crear Features del Futuro

```python
# ❌ INCORRECTO: Predecir ventas de hoy usando ventas de mañana
features = {
    "ventas_mañana": 1500,  # ¡No tendrás este dato cuando predices!
}

# ✅ CORRECTO: Solo usar datos del pasado
features = {
    "ventas_ayer": 1200,
    "ventas_promedio_ultima_semana": 1100,
}
```

### Error 4: One-Hot Encoding con Alta Cardinalidad

```python
# ❌ INCORRECTO: One-hot con 10,000 códigos postales
# Resultado: 10,000 columnas nuevas

# ✅ CORRECTO: Agrupar o usar target encoding
# Opción 1: Agrupar por región
# Opción 2: Target encoding con validación cruzada
# Opción 3: Embedding (si usas deep learning)
```

---

## Checklist de Aprendizaje

Al terminar este tema, deberías poder:

- [ ] Explicar qué es una feature y por qué importa el feature engineering
- [ ] Identificar tipos de features (numéricas, categóricas, temporales)
- [ ] Elegir el encoding correcto para variables categóricas
- [ ] Decidir qué scaler usar según tus datos
- [ ] Implementar estrategias de imputación para missing values
- [ ] Detectar y tratar outliers apropiadamente
- [ ] Extraer features temporales de fechas
- [ ] Evitar data leakage en tus pipelines
- [ ] Diseñar pipelines de features reproducibles

---

## Resumen

| Concepto | Qué Hace | Cuándo Usarlo |
|----------|----------|---------------|
| **Label Encoding** | Asigna números a categorías | Variables ordinales |
| **One-Hot Encoding** | Crea columnas binarias | Nominales con baja cardinalidad |
| **Target Encoding** | Usa la media del target | Alta cardinalidad |
| **StandardScaler** | Media=0, Std=1 | Datos normales |
| **MinMaxScaler** | Escala a [0,1] | Redes neuronales |
| **RobustScaler** | Usa mediana/IQR | Datos con outliers |
| **Imputación Media** | Rellena con promedio | Missing aleatorios |
| **Encoding Cíclico** | Seno/Coseno | Horas, días, meses |

---

## Próximo Paso

En la siguiente sección veremos ejemplos prácticos de cada técnica con código ejecutable y datasets reales.

[Continuar a 02-EJEMPLOS.md →](02-EJEMPLOS.md)
