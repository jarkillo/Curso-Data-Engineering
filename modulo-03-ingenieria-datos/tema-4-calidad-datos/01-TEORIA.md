# Tema 4: Calidad de Datos

**Duración estimada**: 1-2 semanas
**Nivel**: Intermedio-Avanzado
**Prerrequisitos**: Python básico, Pandas (Tema 3), conceptos de ETL

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. **Entender las dimensiones de calidad** de datos (completeness, accuracy, consistency, timeliness)
2. **Validar esquemas de datos** usando Pandera y Great Expectations
3. **Detectar duplicados** exactos y similares con fuzzy matching
4. **Identificar y tratar outliers** usando métodos estadísticos (IQR, Z-score)
5. **Realizar data profiling** para analizar la calidad de datasets
6. **Implementar monitoreo continuo** de calidad en pipelines ETL
7. **Construir frameworks de calidad** reutilizables y mantenibles

---

## 📚 Tabla de Contenidos

1. [Introducción a Calidad de Datos](#1-introducción-a-calidad-de-datos)
2. [Dimensiones de Calidad](#2-dimensiones-de-calidad)
3. [Validación de Esquemas](#3-validación-de-esquemas)
4. [Detección de Duplicados](#4-detección-de-duplicados)
5. [Manejo de Outliers](#5-manejo-de-outliers)
6. [Data Profiling](#6-data-profiling)
7. [Monitoreo Continuo de Calidad](#7-monitoreo-continuo-de-calidad)
8. [Frameworks de Calidad](#8-frameworks-de-calidad)
9. [Errores Comunes](#9-errores-comunes)
10. [Buenas Prácticas](#10-buenas-prácticas)

---

## 1. Introducción a Calidad de Datos

### ¿Qué es Calidad de Datos?

La **calidad de datos** se refiere al grado en que los datos cumplen con los requisitos y expectativas para su uso previsto. En Data Engineering, la calidad de datos es crítica porque:

- **Decisiones de negocio** se basan en datos de calidad
- **Modelos de ML** solo son tan buenos como los datos que los entrenan
- **Reportes y análisis** incorrectos pueden llevar a conclusiones erróneas
- **Costos operativos** aumentan cuando hay que corregir datos malos

### Impacto de Datos de Mala Calidad

**Consecuencias**:
- **Pérdida de confianza**: Los usuarios no confían en los datos
- **Costos financieros**: Decisiones incorrectas basadas en datos malos
- **Tiempo perdido**: Corregir datos consume recursos valiosos
- **Riesgo legal**: Reportes incorrectos pueden tener implicaciones legales
- **Reputación**: Clientes reciben información incorrecta

**Ejemplos reales**:
- Base de datos de clientes con duplicados → envío múltiple de correos
- Precios negativos en ventas → reportes financieros incorrectos
- Fechas futuras en registros históricos → análisis de tendencias erróneo
- Valores nulos en campos críticos → pipelines que fallan

### Calidad en el Ciclo de Vida de los Datos

La calidad debe verificarse en todas las fases:

1. **Extracción**: Validar datos en origen
2. **Transformación**: Verificar reglas de negocio
3. **Carga**: Confirmar integridad antes de insertar
4. **Almacenamiento**: Monitorear cambios y degradación
5. **Consumo**: Alertar a usuarios sobre problemas conocidos

---

## 2. Dimensiones de Calidad

### 2.1 Completeness (Completitud)

**Definición**: Grado en que los datos obligatorios están presentes.

**Métricas**:
- Porcentaje de valores nulos por columna
- Porcentaje de registros completos
- Campos requeridos vs opcionales

**Ejemplo**:
```python
import pandas as pd

def evaluar_completitud(df: pd.DataFrame) -> dict:
    """Evalúa completitud del DataFrame."""
    total_registros = len(df)

    completitud = {}
    for columna in df.columns:
        valores_no_nulos = df[columna].notna().sum()
        porcentaje = (valores_no_nulos / total_registros) * 100
        completitud[columna] = round(porcentaje, 2)

    return completitud
```

**Reglas**:
- Identificar campos obligatorios vs opcionales
- Definir umbrales aceptables (ej: email 100%, teléfono 80%)
- Establecer valores por defecto cuando sea apropiado

### 2.2 Accuracy (Precisión)

**Definición**: Grado en que los datos representan correctamente la realidad.

**Validaciones**:
- Formatos correctos (emails, teléfonos, fechas)
- Rangos válidos (edad 0-120, precios > 0)
- Coherencia con fuentes externas (códigos postales, países)

**Ejemplo**:
```python
import re

def validar_email(email: str) -> bool:
    """Valida formato de email."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

def validar_rango_edad(edad: int) -> bool:
    """Valida que edad esté en rango realista."""
    return 0 <= edad <= 120
```

**Estrategias**:
- Validación en tiempo de entrada
- Comparación con fuentes de referencia
- Verificación cruzada entre campos relacionados

### 2.3 Consistency (Consistencia)

**Definición**: Grado en que los datos son uniformes entre diferentes fuentes y en el tiempo.

**Problemas comunes**:
- Formatos diferentes para el mismo dato
- Representaciones múltiples del mismo concepto
- Inconsistencias entre sistemas relacionados

**Ejemplo**:
```python
def normalizar_genero(genero: str) -> str:
    """Normaliza valores de género a formato estándar."""
    mapeo = {
        'M': 'Masculino',
        'F': 'Femenino',
        'H': 'Masculino',
        'M': 'Femenino',
        'MALE': 'Masculino',
        'FEMALE': 'Femenino',
    }
    return mapeo.get(genero.upper(), 'Desconocido')
```

### 2.4 Timeliness (Actualidad)

**Definición**: Grado en que los datos están actualizados para su uso previsto.

**Consideraciones**:
- Frecuencia de actualización requerida
- Latencia aceptable desde el evento hasta la disponibilidad
- Identificación de datos obsoletos

**Ejemplo**:
```python
from datetime import datetime, timedelta

def datos_obsoletos(fecha_actualizacion: datetime,
                   max_dias: int = 30) -> bool:
    """Verifica si datos están obsoletos."""
    dias_transcurridos = (datetime.now() - fecha_actualizacion).days
    return dias_transcurridos > max_dias
```

### 2.5 Otras Dimensiones

**Validity (Validez)**: Datos cumplen con reglas de negocio
**Uniqueness (Unicidad)**: No hay duplicados
**Integrity (Integridad)**: Relaciones entre datos son correctas

---

## 3. Validación de Esquemas

### 3.1 ¿Por qué Validar Esquemas?

La validación de esquemas asegura que:
- Los datos tienen los tipos correctos
- Los valores están en rangos válidos
- Se cumplen las reglas de negocio
- La estructura es consistente

### 3.2 Validación con Pandera

**Pandera** es una librería de Python para validación de DataFrames con esquemas declarativos.

**Instalación**:
```bash
pip install pandera
```

**Ejemplo básico**:
```python
import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema

# Definir esquema
esquema_ventas = DataFrameSchema({
    "producto_id": Column(int, pa.Check.greater_than(0)),
    "cantidad": Column(int, pa.Check.between(1, 1000)),
    "precio": Column(float, pa.Check.greater_than(0)),
    "fecha": Column(pd.DatetimeTZDtype(tz="UTC")),
    "region": Column(str, pa.Check.isin(["Norte", "Sur", "Este", "Oeste"])),
})

# Validar DataFrame
try:
    df_validado = esquema_ventas.validate(df)
    print("✓ Datos válidos")
except pa.errors.SchemaError as e:
    print(f"✗ Error de validación: {e}")
```

**Validaciones avanzadas**:
```python
# Validación personalizada
def email_valido(email: str) -> bool:
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

esquema_clientes = DataFrameSchema({
    "email": Column(str, pa.Check(email_valido)),
    "edad": Column(int, pa.Check.between(18, 100)),
    "saldo": Column(float, pa.Check.greater_than_or_equal_to(0)),
})
```

### 3.3 Validación con Great Expectations

**Great Expectations** es un framework completo para validación y documentación de datos.

**Instalación**:
```bash
pip install great-expectations
```

**Ejemplo básico**:
```python
import great_expectations as gx

# Crear contexto
context = gx.get_context()

# Crear expectativa
df.expect_column_values_to_be_between(
    column="precio",
    min_value=0,
    max_value=10000
)

df.expect_column_values_to_not_be_null(
    column="cliente_id"
)

df.expect_column_values_to_be_in_set(
    column="estado",
    value_set=["Activo", "Inactivo", "Suspendido"]
)
```

**Ventajas de Great Expectations**:
- Documentación automática de expectativas
- Reportes visuales de validaciones
- Integración con pipelines de datos
- Versionado de expectativas

### 3.4 Validación Manual con Pandas

Para validaciones simples, puedes usar Pandas directamente:

```python
def validar_datos_ventas(df: pd.DataFrame) -> tuple[bool, list]:
    """
    Valida DataFrame de ventas.

    Returns:
        Tupla (es_valido, lista_errores)
    """
    errores = []

    # Verificar columnas requeridas
    columnas_requeridas = ['producto_id', 'cantidad', 'precio', 'fecha']
    for col in columnas_requeridas:
        if col not in df.columns:
            errores.append(f"Falta columna requerida: {col}")

    # Verificar tipos
    if not pd.api.types.is_integer_dtype(df['cantidad']):
        errores.append("Columna 'cantidad' debe ser entero")

    # Verificar rangos
    if (df['precio'] < 0).any():
        errores.append("Encontrados precios negativos")

    # Verificar nulos en campos críticos
    if df['producto_id'].isnull().any():
        errores.append("Producto_id no puede ser nulo")

    return len(errores) == 0, errores
```

---

## 4. Detección de Duplicados

### 4.1 Duplicados Exactos

Los duplicados exactos son registros idénticos en todas o algunas columnas clave.

**Detección con Pandas**:
```python
# Verificar duplicados completos
duplicados_completos = df.duplicated()
print(f"Duplicados completos: {duplicados_completos.sum()}")

# Verificar duplicados por columnas específicas
duplicados_id = df.duplicated(subset=['cliente_id'], keep=False)
print(f"Clientes duplicados: {duplicados_id.sum()}")

# Ver registros duplicados
df_duplicados = df[duplicados_id]
```

**Estrategias de eliminación**:
```python
# Mantener primera ocurrencia
df_sin_dup = df.drop_duplicates(subset=['cliente_id'], keep='first')

# Mantener última ocurrencia
df_sin_dup = df.drop_duplicates(subset=['cliente_id'], keep='last')

# Eliminar todas las ocurrencias
df_sin_dup = df.drop_duplicates(subset=['cliente_id'], keep=False)
```

### 4.2 Duplicados Fuzzy (Similares)

Los duplicados fuzzy son registros similares pero no idénticos (ej: "Juan Perez" vs "Juan Pérez").

**RapidFuzz** es una librería rápida para fuzzy matching:

```bash
pip install rapidfuzz
```

**Ejemplo básico**:
```python
from rapidfuzz import fuzz, process

def encontrar_duplicados_fuzzy(nombres: list, umbral: int = 85) -> list:
    """
    Encuentra nombres similares usando fuzzy matching.

    Args:
        nombres: Lista de nombres a comparar
        umbral: Score mínimo para considerar match (0-100)

    Returns:
        Lista de tuplas (nombre1, nombre2, score)
    """
    duplicados = []

    for i, nombre1 in enumerate(nombres):
        for nombre2 in nombres[i+1:]:
            score = fuzz.ratio(nombre1, nombre2)
            if score >= umbral:
                duplicados.append((nombre1, nombre2, score))

    return duplicados

# Uso
nombres = ["Juan Perez", "Juan Pérez", "Maria Lopez", "María López"]
duplicados = encontrar_duplicados_fuzzy(nombres)
for n1, n2, score in duplicados:
    print(f"{n1} ↔ {n2}: {score}%")
```

**Métodos de comparación**:
```python
from rapidfuzz import fuzz

texto1 = "Juan Perez Martinez"
texto2 = "Juan Pérez Martínez"

# Ratio simple
score1 = fuzz.ratio(texto1, texto2)

# Partial ratio (subcadenas)
score2 = fuzz.partial_ratio(texto1, texto2)

# Token sort (ignora orden)
score3 = fuzz.token_sort_ratio(texto1, texto2)

# Token set (ignora duplicados)
score4 = fuzz.token_set_ratio(texto1, texto2)

print(f"Ratio: {score1}, Partial: {score2}, Sort: {score3}, Set: {score4}")
```

**Detección en DataFrames**:
```python
def detectar_duplicados_fuzzy_df(df: pd.DataFrame,
                                  columna: str,
                                  umbral: int = 85) -> pd.DataFrame:
    """Detecta duplicados fuzzy en una columna del DataFrame."""
    from rapidfuzz import fuzz

    valores = df[columna].dropna().unique().tolist()
    duplicados = []

    for i, val1 in enumerate(valores):
        for val2 in valores[i+1:]:
            score = fuzz.ratio(str(val1), str(val2))
            if score >= umbral:
                duplicados.append({
                    'valor1': val1,
                    'valor2': val2,
                    'score': score
                })

    return pd.DataFrame(duplicados)
```

---

## 5. Manejo de Outliers

### 5.1 ¿Qué son los Outliers?

**Outliers** (valores atípicos) son observaciones que se desvían significativamente del resto de los datos.

**Pueden ser**:
- **Errores**: Datos ingresados incorrectamente (edad 999, precio -100)
- **Válidos**: Eventos reales pero inusuales (venta de 1M de unidades)

### 5.2 Método IQR (Rango Intercuartílico)

El método IQR usa cuartiles para identificar outliers.

**Fórmula**:
- Q1 = Percentil 25
- Q3 = Percentil 75
- IQR = Q3 - Q1
- Límite inferior = Q1 - 1.5 * IQR
- Límite superior = Q3 + 1.5 * IQR

**Implementación**:
```python
def detectar_outliers_iqr(df: pd.DataFrame, columna: str) -> pd.Series:
    """
    Detecta outliers usando método IQR.

    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a analizar

    Returns:
        Serie booleana indicando outliers
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outliers = (df[columna] < limite_inferior) | (df[columna] > limite_superior)

    return outliers

# Uso
outliers_precio = detectar_outliers_iqr(df, 'precio')
print(f"Outliers encontrados: {outliers_precio.sum()}")
print(f"Porcentaje: {(outliers_precio.sum() / len(df)) * 100:.2f}%")
```

### 5.3 Método Z-Score

El Z-score mide cuántas desviaciones estándar está un valor de la media.

**Fórmula**:
\[ Z = \frac{X - \mu}{\sigma} \]

Donde:
- X = valor observado
- μ = media
- σ = desviación estándar

**Implementación**:
```python
import numpy as np

def detectar_outliers_zscore(df: pd.DataFrame,
                              columna: str,
                              umbral: float = 3.0) -> pd.Series:
    """
    Detecta outliers usando Z-score.

    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a analizar
        umbral: Número de desviaciones estándar (típicamente 3)

    Returns:
        Serie booleana indicando outliers
    """
    media = df[columna].mean()
    std = df[columna].std()

    z_scores = np.abs((df[columna] - media) / std)
    outliers = z_scores > umbral

    return outliers

# Uso
outliers_zscore = detectar_outliers_zscore(df, 'precio', umbral=3)
print(f"Outliers (Z-score > 3): {outliers_zscore.sum()}")
```

### 5.4 Isolation Forest

**Isolation Forest** es un algoritmo de ML para detectar anomalías.

```bash
pip install scikit-learn
```

```python
from sklearn.ensemble import IsolationForest

def detectar_outliers_isolation_forest(df: pd.DataFrame,
                                        columnas: list,
                                        contamination: float = 0.1) -> pd.Series:
    """
    Detecta outliers usando Isolation Forest.

    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a analizar
        contamination: Proporción esperada de outliers (0.0-0.5)

    Returns:
        Serie booleana indicando outliers
    """
    # Preparar datos
    X = df[columnas].dropna()

    # Entrenar modelo
    clf = IsolationForest(contamination=contamination, random_state=42)
    predicciones = clf.fit_predict(X)

    # -1 indica outlier, 1 indica normal
    outliers = predicciones == -1

    return pd.Series(outliers, index=X.index)
```

### 5.5 Tratamiento de Outliers

**Opciones**:

1. **Eliminar**: Remover registros con outliers
```python
df_sin_outliers = df[~outliers]
```

2. **Imputar**: Reemplazar con media/mediana
```python
df.loc[outliers, 'precio'] = df['precio'].median()
```

3. **Capping**: Limitar a percentiles
```python
p95 = df['precio'].quantile(0.95)
p05 = df['precio'].quantile(0.05)
df['precio'] = df['precio'].clip(lower=p05, upper=p95)
```

4. **Transformar**: Aplicar log/sqrt para reducir impacto
```python
df['precio_log'] = np.log1p(df['precio'])
```

---

## 6. Data Profiling

### 6.1 ¿Qué es Data Profiling?

**Data profiling** es el análisis sistemático de datos para entender su estructura, contenido y calidad.

**Objetivos**:
- Comprender la distribución de valores
- Identificar patrones y anomalías
- Evaluar calidad general
- Documentar características de los datos

### 6.2 Profiling Básico con Pandas

```python
def perfil_basico(df: pd.DataFrame) -> dict:
    """Genera perfil básico del DataFrame."""
    perfil = {
        'num_registros': len(df),
        'num_columnas': len(df.columns),
        'memoria_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'columnas': {}
    }

    for col in df.columns:
        perfil['columnas'][col] = {
            'tipo': str(df[col].dtype),
            'nulos': int(df[col].isnull().sum()),
            'porcentaje_nulos': round(df[col].isnull().mean() * 100, 2),
            'unicos': int(df[col].nunique()),
            'duplicados': int(df[col].duplicated().sum()),
        }

        # Estadísticas numéricas
        if pd.api.types.is_numeric_dtype(df[col]):
            perfil['columnas'][col].update({
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'media': float(df[col].mean()),
                'mediana': float(df[col].median()),
                'std': float(df[col].std()),
            })

    return perfil
```

### 6.3 ydata-profiling (pandas-profiling)

**ydata-profiling** genera reportes HTML completos automáticamente.

```bash
pip install ydata-profiling
```

**Uso básico**:
```python
from ydata_profiling import ProfileReport

# Generar reporte
profile = ProfileReport(df, title="Reporte de Calidad - Ventas")

# Guardar como HTML
profile.to_file("reporte_ventas.html")

# Ver en Jupyter
profile.to_widgets()
```

**Configuración avanzada**:
```python
profile = ProfileReport(
    df,
    title="Reporte Personalizado",
    minimal=False,  # False = reporte completo
    explorative=True,  # Análisis más profundo
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": False},
    },
    missing_diagrams={
        "bar": True,
        "matrix": True,
        "heatmap": True,
    },
)
```

**Información incluida**:
- Resumen general del dataset
- Estadísticas por variable
- Distribuciones y histogramas
- Correlaciones entre variables
- Valores faltantes
- Duplicados
- Alertas de calidad

### 6.4 Análisis de Correlaciones

```python
def analizar_correlaciones(df: pd.DataFrame,
                          umbral: float = 0.7) -> pd.DataFrame:
    """
    Identifica variables altamente correlacionadas.

    Args:
        df: DataFrame con datos numéricos
        umbral: Correlación mínima para reportar

    Returns:
        DataFrame con pares de variables correlacionadas
    """
    # Calcular matriz de correlación
    correlaciones = df.select_dtypes(include=[np.number]).corr()

    # Encontrar pares con correlación alta
    pares_alta_corr = []

    for i in range(len(correlaciones.columns)):
        for j in range(i+1, len(correlaciones.columns)):
            col1 = correlaciones.columns[i]
            col2 = correlaciones.columns[j]
            valor = correlaciones.iloc[i, j]

            if abs(valor) >= umbral:
                pares_alta_corr.append({
                    'variable1': col1,
                    'variable2': col2,
                    'correlacion': round(valor, 3)
                })

    return pd.DataFrame(pares_alta_corr)
```

---

## 7. Monitoreo Continuo de Calidad

### 7.1 ¿Por qué Monitorear?

Los datos no son estáticos; su calidad puede degradarse con el tiempo:
- Cambios en sistemas fuente
- Nuevas reglas de negocio
- Errores en pipelines
- Datos obsoletos

### 7.2 Métricas a Monitorear

```python
from datetime import datetime

def metricas_calidad(df: pd.DataFrame) -> dict:
    """Calcula métricas clave de calidad."""
    total_registros = len(df)
    total_celdas = total_registros * len(df.columns)

    metricas = {
        'timestamp': datetime.now().isoformat(),
        'total_registros': total_registros,
        'total_columnas': len(df.columns),

        # Completitud
        'celdas_vacias': int(df.isnull().sum().sum()),
        'porcentaje_completitud': round((1 - df.isnull().sum().sum() / total_celdas) * 100, 2),

        # Duplicados
        'registros_duplicados': int(df.duplicated().sum()),
        'porcentaje_duplicados': round((df.duplicated().sum() / total_registros) * 100, 2),

        # Por columna
        'columnas_con_nulos': int((df.isnull().sum() > 0).sum()),
        'columnas_100_completas': int((df.isnull().sum() == 0).sum()),
    }

    return metricas
```

### 7.3 Alertas Automáticas

```python
def verificar_alertas(metricas: dict,
                     umbrales: dict) -> list:
    """
    Verifica si métricas exceden umbrales y genera alertas.

    Args:
        metricas: Dict con métricas calculadas
        umbrales: Dict con umbrales máximos permitidos

    Returns:
        Lista de alertas generadas
    """
    alertas = []

    if metricas['porcentaje_completitud'] < umbrales.get('completitud_minima', 95):
        alertas.append({
            'nivel': 'WARNING',
            'mensaje': f"Completitud baja: {metricas['porcentaje_completitud']}%"
        })

    if metricas['porcentaje_duplicados'] > umbrales.get('duplicados_maximos', 1):
        alertas.append({
            'nivel': 'ERROR',
            'mensaje': f"Demasiados duplicados: {metricas['porcentaje_duplicados']}%"
        })

    return alertas
```

### 7.4 Registro de Calidad

```python
import json
from pathlib import Path

def registrar_calidad(metricas: dict, archivo_log: str = "calidad_log.jsonl"):
    """Registra métricas de calidad en archivo JSONL."""
    ruta = Path(archivo_log)

    with open(ruta, 'a', encoding='utf-8') as f:
        f.write(json.dumps(metricas, ensure_ascii=False) + '\n')
```

---

## 8. Frameworks de Calidad

### 8.1 Arquitectura de un Framework

Un framework de calidad reutilizable debe tener:

1. **Módulo de validación**: Esquemas y reglas
2. **Módulo de detección**: Duplicados y outliers
3. **Módulo de profiling**: Análisis y reportes
4. **Módulo de monitoreo**: Métricas y alertas
5. **Módulo de corrección**: Limpieza automática

### 8.2 Estructura Recomendada

```
calidad_framework/
├── src/
│   ├── validador_esquema.py    # Validaciones
│   ├── detector_duplicados.py   # Duplicados
│   ├── detector_outliers.py     # Outliers
│   ├── profiler.py              # Profiling
│   └── monitor.py               # Monitoreo
├── tests/                       # Tests unitarios
├── configuracion/
│   ├── esquemas.yaml           # Definición de esquemas
│   └── umbrales.yaml           # Umbrales de calidad
└── reportes/                   # Reportes generados
```

### 8.3 Pipeline de Calidad

```python
def pipeline_calidad(df: pd.DataFrame,
                    config: dict) -> tuple[pd.DataFrame, dict]:
    """
    Pipeline completo de calidad de datos.

    Args:
        df: DataFrame a procesar
        config: Configuración de validaciones

    Returns:
        Tupla (DataFrame limpio, reporte de calidad)
    """
    reporte = {'pasos': []}

    # 1. Validar esquema
    es_valido, errores = validar_esquema(df, config['esquema'])
    reporte['pasos'].append({
        'paso': 'validacion_esquema',
        'valido': es_valido,
        'errores': errores
    })

    if not es_valido:
        raise ValueError(f"Esquema inválido: {errores}")

    # 2. Detectar y eliminar duplicados
    duplicados = detectar_duplicados_exactos(df, config['columnas_clave'])
    df_limpio = df.drop_duplicates(subset=config['columnas_clave'])
    reporte['pasos'].append({
        'paso': 'eliminacion_duplicados',
        'duplicados_encontrados': duplicados.sum(),
        'registros_eliminados': len(df) - len(df_limpio)
    })

    # 3. Detectar y tratar outliers
    for col in config['columnas_numericas']:
        outliers = detectar_outliers_iqr(df_limpio, col)
        df_limpio = df_limpio[~outliers]
        reporte['pasos'].append({
            'paso': f'outliers_{col}',
            'outliers_encontrados': outliers.sum()
        })

    # 4. Generar perfil
    perfil = perfil_basico(df_limpio)
    reporte['perfil_final'] = perfil

    return df_limpio, reporte
```

---

## 9. Errores Comunes

### Error 1: No Validar en Todas las Etapas

**Problema**: Solo validar al final del pipeline.

**Solución**: Validar después de cada transformación importante.

```python
# ❌ MAL
df = extraer_datos()
df = transformar_datos(df)
df = limpiar_datos(df)
validar(df)  # Solo al final

# ✅ BIEN
df = extraer_datos()
validar_extraccion(df)

df = transformar_datos(df)
validar_transformacion(df)

df = limpiar_datos(df)
validar_limpieza(df)
```

### Error 2: Eliminar Datos sin Analizar

**Problema**: Eliminar outliers o duplicados automáticamente sin investigar.

**Solución**: Siempre revisar y documentar qué se elimina y por qué.

```python
# ❌ MAL
df = df.drop_duplicates()  # Elimina sin revisar

# ✅ BIEN
duplicados = df[df.duplicated(keep=False)]
print(f"Se encontraron {len(duplicados)} duplicados")
print(duplicados.head())
# Decisión informada de cómo manejarlos
```

### Error 3: Asumir Datos Estáticos

**Problema**: Validar una vez y asumir que siempre será así.

**Solución**: Implementar monitoreo continuo.

### Error 4: Validaciones Demasiado Estrictas

**Problema**: Reglas tan estrictas que rechazan datos válidos.

**Solución**: Balancear precisión y recall; permitir excepciones documentadas.

### Error 5: No Documentar Reglas de Calidad

**Problema**: Reglas de validación no documentadas o en el código.

**Solución**: Documentar todas las reglas en archivos de configuración.

```yaml
# esquemas.yaml
ventas:
  columnas_requeridas:
    - producto_id
    - cantidad
    - precio
  rangos:
    cantidad:
      min: 1
      max: 1000
    precio:
      min: 0
      max: 100000
  valores_permitidos:
    region:
      - Norte
      - Sur
      - Este
      - Oeste
```

---

## 10. Buenas Prácticas

### 1. Definir Reglas de Calidad con el Negocio

Las reglas de calidad deben venir del negocio, no solo de TI:
- ¿Qué campos son obligatorios?
- ¿Qué rangos son válidos?
- ¿Qué nivel de duplicados es aceptable?

### 2. Fallar Rápido y Claro

```python
def validar_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """Valida datos de ventas con mensajes claros."""
    if df.empty:
        raise ValueError("DataFrame de ventas está vacío")

    if 'precio' not in df.columns:
        raise ValueError("Falta columna requerida: 'precio'")

    precios_invalidos = (df['precio'] < 0).sum()
    if precios_invalidos > 0:
        raise ValueError(
            f"Encontrados {precios_invalidos} precios negativos. "
            f"Todos los precios deben ser >= 0"
        )

    return df
```

### 3. Usar Type Hints

```python
from typing import List, Dict, Tuple
import pandas as pd

def validar_esquema(df: pd.DataFrame,
                   esquema: Dict[str, type]) -> Tuple[bool, List[str]]:
    """
    Valida tipos de columnas contra esquema.

    Args:
        df: DataFrame a validar
        esquema: Dict con nombre_columna: tipo_esperado

    Returns:
        Tupla (es_valido, lista_errores)
    """
    pass
```

### 4. Testear las Validaciones

```python
def test_detectar_outliers_iqr():
    """Test de detección de outliers."""
    # Datos con outlier conocido
    df = pd.DataFrame({'valores': [1, 2, 3, 4, 5, 100]})

    outliers = detectar_outliers_iqr(df, 'valores')

    # Verificar que detecta el outlier
    assert outliers.sum() == 1
    assert outliers.iloc[-1] == True  # El 100 es outlier
```

### 5. Generar Reportes Visuales

```python
import matplotlib.pyplot as plt

def visualizar_calidad(df: pd.DataFrame, output_path: str):
    """Genera reporte visual de calidad."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Completitud por columna
    completitud = (1 - df.isnull().mean()) * 100
    completitud.plot(kind='barh', ax=axes[0, 0])
    axes[0, 0].set_title('Completitud por Columna (%)')

    # Distribución de nulos
    nulos = df.isnull().sum()
    nulos[nulos > 0].plot(kind='bar', ax=axes[0, 1])
    axes[0, 1].set_title('Valores Nulos por Columna')

    # Valores únicos
    unicos = df.nunique()
    unicos.plot(kind='bar', ax=axes[1, 0])
    axes[1, 0].set_title('Valores Únicos por Columna')

    # Duplicados
    duplicados = df.duplicated(subset=df.columns, keep=False).sum()
    axes[1, 1].pie([duplicados, len(df) - duplicados],
                   labels=['Duplicados', 'Únicos'],
                   autopct='%1.1f%%')
    axes[1, 1].set_title('Duplicados vs Únicos')

    plt.tight_layout()
    plt.savefig(output_path)
```

### 6. Versionado de Esquemas

```python
# esquemas/ventas_v1.py
ESQUEMA_VENTAS_V1 = {
    'version': '1.0',
    'fecha': '2024-01-01',
    'columnas': {
        'producto_id': int,
        'cantidad': int,
        'precio': float,
    }
}

# esquemas/ventas_v2.py
ESQUEMA_VENTAS_V2 = {
    'version': '2.0',
    'fecha': '2024-06-01',
    'cambios': 'Añadida columna region',
    'columnas': {
        'producto_id': int,
        'cantidad': int,
        'precio': float,
        'region': str,  # Nueva
    }
}
```

### 7. Logging de Calidad

```python
import logging

logger = logging.getLogger(__name__)

def validar_con_logs(df: pd.DataFrame) -> pd.DataFrame:
    """Valida datos con logging detallado."""
    logger.info(f"Iniciando validación de {len(df)} registros")

    nulos_antes = df.isnull().sum().sum()
    logger.info(f"Valores nulos encontrados: {nulos_antes}")

    duplicados = df.duplicated().sum()
    logger.warning(f"Duplicados encontrados: {duplicados}")

    if duplicados > len(df) * 0.05:
        logger.error(f"Duplicados exceden umbral del 5%")
        raise ValueError("Demasiados duplicados")

    logger.info("Validación completada exitosamente")
    return df
```

### 8. Configuración Externalizada

```python
import yaml
from pathlib import Path

def cargar_configuracion_calidad(archivo: str) -> dict:
    """Carga configuración de calidad desde YAML."""
    ruta = Path(archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra {archivo}")

    with open(ruta, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config
```

### 9. Documentación Clara

```python
def detectar_duplicados_fuzzy(df: pd.DataFrame,
                              columna: str,
                              umbral: int = 85) -> pd.DataFrame:
    """
    Detecta registros con valores similares usando fuzzy matching.

    Args:
        df: DataFrame a analizar
        columna: Nombre de la columna para comparar
        umbral: Score mínimo para considerar match (0-100).
               85 es un buen balance entre precisión y recall.

    Returns:
        DataFrame con columnas:
        - valor1: Primer valor del par
        - valor2: Segundo valor del par
        - score: Similitud entre 0-100

    Raises:
        ValueError: Si la columna no existe o está vacía

    Example:
        >>> df = pd.DataFrame({'nombre': ['Juan', 'Juán', 'Pedro']})
        >>> duplicados = detectar_duplicados_fuzzy(df, 'nombre', 90)
        >>> print(duplicados)
           valor1 valor2  score
        0    Juan   Juán     96
    """
    pass
```

### 10. Calidad como Código

Trata las reglas de calidad como código:
- Control de versiones (Git)
- Revisión por pares (Pull Requests)
- Tests automatizados (CI/CD)
- Documentación (README, docstrings)

---

## 📝 Resumen

La **calidad de datos** es fundamental en Data Engineering:

1. **4 Dimensiones clave**: Completitud, precisión, consistencia, actualidad
2. **Validación de esquemas**: Pandera y Great Expectations
3. **Duplicados**: Exactos con Pandas, fuzzy con RapidFuzz
4. **Outliers**: IQR, Z-score, Isolation Forest
5. **Profiling**: Análisis con ydata-profiling
6. **Monitoreo**: Métricas continuas y alertas
7. **Frameworks**: Arquitectura modular y reutilizable

**Recuerda**:
- Validar en cada etapa del pipeline
- Documentar todas las reglas de calidad
- Generar reportes visuales comprensibles
- Monitorear continuamente
- Fallar rápido con mensajes claros

---

## 📚 Recursos Adicionales

### Librerías

- **Pandera**: https://pandera.readthedocs.io/
- **Great Expectations**: https://greatexpectations.io/
- **RapidFuzz**: https://github.com/maxbachmann/RapidFuzz
- **ydata-profiling**: https://github.com/ydataai/ydata-profiling

### Lecturas

- "Data Quality: The Accuracy Dimension" - Jack E. Olson
- "Bad Data Handbook" - Q. Ethan McCallum
- "Data Quality Fundamentals" - Barr Moses

### Herramientas

- **Soda**: Framework de calidad para data engineers
- **Deequ**: Librería de AWS para calidad de datos
- **Tensorflow Data Validation**: Para validación en ML

---

**Próximo tema**: Tema 5 - Carga de Datos (Load)

*Última actualización: 2025-10-30*
