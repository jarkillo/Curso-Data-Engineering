# Ejemplos Prácticos: Procesamiento de Archivos CSV

Este documento contiene **5 ejemplos trabajados paso a paso** que te ayudarán a dominar el procesamiento de archivos CSV en Python.

Cada ejemplo incluye:
- ✅ Contexto empresarial realista
- ✅ Datos concretos para trabajar
- ✅ Solución paso a paso explicada
- ✅ Código Python completo y ejecutable
- ✅ Interpretación de resultados

**Duración estimada:** 60-90 minutos

---

## 📋 Índice de Ejemplos

1. **[Básico]** Análisis de Ventas de RestaurantData Co.
2. **[Básico]** Consolidación de Datos de Múltiples Locales
3. **[Intermedio]** Validación y Limpieza de Datos con Errores
4. **[Intermedio]** Transformación y Enriquecimiento de Datos
5. **[Avanzado]** Pipeline ETL Completo con Manejo de Errores

---

## Ejemplo 1: Análisis de Ventas de RestaurantData Co.

### Nivel: ⭐ Básico

### Contexto

Trabajas para **DataFlow Industries** y tu primer cliente es **RestaurantData Co.**, una cadena de restaurantes.

Te envían un archivo CSV con las ventas del último mes y te piden:
1. Leer el archivo
2. Calcular el total de ventas
3. Identificar el producto más vendido
4. Guardar un resumen en un nuevo CSV

### Datos

Archivo: `ventas_octubre.csv`

```csv
fecha,producto,cantidad,precio_unitario
2025-10-01,Pizza Margarita,3,12.50
2025-10-01,Coca-Cola,5,2.50
2025-10-02,Pizza Margarita,2,12.50
2025-10-02,Pasta Carbonara,4,14.00
2025-10-03,Pizza Margarita,5,12.50
2025-10-03,Coca-Cola,8,2.50
2025-10-04,Pasta Carbonara,3,14.00
```

### Objetivo

Analizar las ventas y generar un resumen por producto.

---

### Solución Paso a Paso

#### Paso 1: Leer el archivo CSV

Primero, vamos a leer el archivo y ver qué contiene.

```python
import csv

# Leer el archivo
with open('ventas_octubre.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    print("Contenido del archivo:")
    print("-" * 60)

    for fila in lector:
        print(fila)
```

**Salida**:
```
Contenido del archivo:
------------------------------------------------------------
{'fecha': '2025-10-01', 'producto': 'Pizza Margarita', 'cantidad': '3', 'precio_unitario': '12.50'}
{'fecha': '2025-10-01', 'producto': 'Coca-Cola', 'cantidad': '5', 'precio_unitario': '2.50'}
...
```

**Observación**: Los valores son strings, necesitamos convertirlos a números.

---

#### Paso 2: Calcular el total por producto

Vamos a agrupar por producto y calcular:
- Total de unidades vendidas
- Total de ingresos

```python
import csv
from collections import defaultdict

# Diccionario para acumular datos por producto
ventas_por_producto = defaultdict(lambda: {'cantidad_total': 0, 'ingresos_totales': 0.0})

# Leer y procesar
with open('ventas_octubre.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        producto = fila['producto']
        cantidad = int(fila['cantidad'])
        precio = float(fila['precio_unitario'])

        # Calcular ingreso de esta venta
        ingreso = cantidad * precio

        # Acumular
        ventas_por_producto[producto]['cantidad_total'] += cantidad
        ventas_por_producto[producto]['ingresos_totales'] += ingreso

# Mostrar resultados
print("\nResumen de ventas por producto:")
print("-" * 60)

for producto, datos in ventas_por_producto.items():
    print(f"{producto}:")
    print(f"  - Unidades vendidas: {datos['cantidad_total']}")
    print(f"  - Ingresos totales: {datos['ingresos_totales']:.2f}€")
    print()
```

**Salida**:
```
Resumen de ventas por producto:
------------------------------------------------------------
Pizza Margarita:
  - Unidades vendidas: 10
  - Ingresos totales: 125.00€

Coca-Cola:
  - Unidades vendidas: 13
  - Ingresos totales: 32.50€

Pasta Carbonara:
  - Unidades vendidas: 7
  - Ingresos totales: 98.00€
```

---

#### Paso 3: Identificar el producto más vendido

```python
# Encontrar el producto más vendido (por cantidad)
producto_mas_vendido = max(
    ventas_por_producto.items(),
    key=lambda x: x[1]['cantidad_total']
)

print(f"🏆 Producto más vendido: {producto_mas_vendido[0]}")
print(f"   Unidades: {producto_mas_vendido[1]['cantidad_total']}")

# Encontrar el producto con más ingresos
producto_mas_ingresos = max(
    ventas_por_producto.items(),
    key=lambda x: x[1]['ingresos_totales']
)

print(f"\n💰 Producto con más ingresos: {producto_mas_ingresos[0]}")
print(f"   Ingresos: {producto_mas_ingresos[1]['ingresos_totales']:.2f}€")
```

**Salida**:
```
🏆 Producto más vendido: Coca-Cola
   Unidades: 13

💰 Producto con más ingresos: Pizza Margarita
   Ingresos: 125.00€
```

---

#### Paso 4: Guardar el resumen en un nuevo CSV

```python
import csv

# Preparar datos para escribir
datos_resumen = []
for producto, datos in ventas_por_producto.items():
    datos_resumen.append({
        'producto': producto,
        'cantidad_total': datos['cantidad_total'],
        'ingresos_totales': round(datos['ingresos_totales'], 2)
    })

# Ordenar por ingresos (mayor a menor)
datos_resumen.sort(key=lambda x: x['ingresos_totales'], reverse=True)

# Escribir CSV
with open('resumen_ventas.csv', 'w', encoding='utf-8', newline='') as archivo:
    fieldnames = ['producto', 'cantidad_total', 'ingresos_totales']
    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)

    escritor.writeheader()
    escritor.writerows(datos_resumen)

print("✅ Resumen guardado en 'resumen_ventas.csv'")
```

**Archivo generado**: `resumen_ventas.csv`

```csv
producto,cantidad_total,ingresos_totales
Pizza Margarita,10,125.0
Pasta Carbonara,7,98.0
Coca-Cola,13,32.5
```

---

### Código Completo

```python
import csv
from collections import defaultdict

def analizar_ventas(archivo_entrada: str, archivo_salida: str) -> dict:
    """
    Analiza ventas de un CSV y genera un resumen.

    Args:
        archivo_entrada: Ruta al CSV de ventas
        archivo_salida: Ruta donde guardar el resumen

    Returns:
        Diccionario con estadísticas de ventas
    """
    # Leer y procesar
    ventas_por_producto = defaultdict(lambda: {'cantidad_total': 0, 'ingresos_totales': 0.0})

    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            producto = fila['producto']
            cantidad = int(fila['cantidad'])
            precio = float(fila['precio_unitario'])
            ingreso = cantidad * precio

            ventas_por_producto[producto]['cantidad_total'] += cantidad
            ventas_por_producto[producto]['ingresos_totales'] += ingreso

    # Preparar resumen
    datos_resumen = []
    for producto, datos in ventas_por_producto.items():
        datos_resumen.append({
            'producto': producto,
            'cantidad_total': datos['cantidad_total'],
            'ingresos_totales': round(datos['ingresos_totales'], 2)
        })

    # Ordenar por ingresos
    datos_resumen.sort(key=lambda x: x['ingresos_totales'], reverse=True)

    # Guardar resumen
    with open(archivo_salida, 'w', encoding='utf-8', newline='') as archivo:
        fieldnames = ['producto', 'cantidad_total', 'ingresos_totales']
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        escritor.writeheader()
        escritor.writerows(datos_resumen)

    # Estadísticas
    producto_mas_vendido = max(ventas_por_producto.items(), key=lambda x: x[1]['cantidad_total'])
    producto_mas_ingresos = max(ventas_por_producto.items(), key=lambda x: x[1]['ingresos_totales'])

    return {
        'producto_mas_vendido': producto_mas_vendido[0],
        'producto_mas_ingresos': producto_mas_ingresos[0],
        'total_productos': len(ventas_por_producto)
    }

# Usar la función
estadisticas = analizar_ventas('ventas_octubre.csv', 'resumen_ventas.csv')
print(f"✅ Análisis completado:")
print(f"   - Producto más vendido: {estadisticas['producto_mas_vendido']}")
print(f"   - Producto con más ingresos: {estadisticas['producto_mas_ingresos']}")
print(f"   - Total de productos diferentes: {estadisticas['total_productos']}")
```

---

### Interpretación de Resultados

**Hallazgos clave**:
1. **Pizza Margarita** genera más ingresos (125€) aunque no es el más vendido en unidades
2. **Coca-Cola** es el más vendido (13 unidades) pero genera menos ingresos (32.50€)
3. Esto sugiere que la **estrategia de precios** es importante: productos de mayor precio generan más ingresos con menos ventas

**Decisiones de negocio**:
- Promocionar Pizza Margarita (alto margen)
- Considerar combos (Pizza + Coca-Cola)
- Analizar si Coca-Cola tiene suficiente margen

---

## Ejemplo 2: Consolidación de Datos de Múltiples Locales

### Nivel: ⭐ Básico

### Contexto

**RestaurantData Co.** tiene 3 locales: Madrid, Barcelona y Valencia.

Cada local envía su propio archivo CSV con las ventas del día. Tu tarea es:
1. Leer los 3 archivos
2. Consolidarlos en uno solo
3. Añadir una columna con el nombre del local
4. Calcular totales por local

### Datos

**Archivo**: `ventas_madrid.csv`
```csv
producto,cantidad,precio
Pizza,5,12.50
Pasta,3,14.00
```

**Archivo**: `ventas_barcelona.csv`
```csv
producto,cantidad,precio
Pizza,8,12.50
Ensalada,4,9.00
```

**Archivo**: `ventas_valencia.csv`
```csv
producto,cantidad,precio
Pasta,6,14.00
Pizza,3,12.50
```

---

### Solución Paso a Paso

#### Paso 1: Leer y consolidar los archivos

```python
import csv
import os

def consolidar_ventas(archivos: dict, archivo_salida: str) -> None:
    """
    Consolida múltiples CSVs de ventas en uno solo.

    Args:
        archivos: Diccionario {nombre_local: ruta_archivo}
        archivo_salida: Ruta del archivo consolidado
    """
    with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
        # Headers del archivo consolidado
        fieldnames = ['local', 'producto', 'cantidad', 'precio', 'total']
        escritor = csv.DictWriter(salida, fieldnames=fieldnames)
        escritor.writeheader()

        # Procesar cada archivo
        for nombre_local, ruta_archivo in archivos.items():
            with open(ruta_archivo, 'r', encoding='utf-8') as entrada:
                lector = csv.DictReader(entrada)

                for fila in lector:
                    # Calcular total
                    cantidad = int(fila['cantidad'])
                    precio = float(fila['precio'])
                    total = cantidad * precio

                    # Escribir fila con local añadido
                    escritor.writerow({
                        'local': nombre_local,
                        'producto': fila['producto'],
                        'cantidad': cantidad,
                        'precio': precio,
                        'total': round(total, 2)
                    })

# Consolidar
archivos = {
    'Madrid': 'ventas_madrid.csv',
    'Barcelona': 'ventas_barcelona.csv',
    'Valencia': 'ventas_valencia.csv'
}

consolidar_ventas(archivos, 'ventas_consolidadas.csv')
print("✅ Archivos consolidados en 'ventas_consolidadas.csv'")
```

**Archivo generado**: `ventas_consolidadas.csv`

```csv
local,producto,cantidad,precio,total
Madrid,Pizza,5,12.5,62.5
Madrid,Pasta,3,14.0,42.0
Barcelona,Pizza,8,12.5,100.0
Barcelona,Ensalada,4,9.0,36.0
Valencia,Pasta,6,14.0,84.0
Valencia,Pizza,3,12.5,37.5
```

---

#### Paso 2: Calcular totales por local

```python
import csv
from collections import defaultdict

def calcular_totales_por_local(archivo: str) -> dict:
    """
    Calcula el total de ventas por local.

    Args:
        archivo: Ruta al CSV consolidado

    Returns:
        Diccionario {local: total_ventas}
    """
    totales = defaultdict(float)

    with open(archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for fila in lector:
            local = fila['local']
            total = float(fila['total'])
            totales[local] += total

    return dict(totales)

# Calcular totales
totales = calcular_totales_por_local('ventas_consolidadas.csv')

print("\n📊 Totales por local:")
print("-" * 40)
for local, total in sorted(totales.items(), key=lambda x: x[1], reverse=True):
    print(f"{local:15} {total:>10.2f}€")

# Calcular total general
total_general = sum(totales.values())
print("-" * 40)
print(f"{'TOTAL GENERAL':15} {total_general:>10.2f}€")
```

**Salida**:
```
📊 Totales por local:
----------------------------------------
Barcelona          136.00€
Valencia           121.50€
Madrid             104.50€
----------------------------------------
TOTAL GENERAL      362.00€
```

---

### Interpretación de Resultados

**Hallazgos**:
1. **Barcelona** es el local con más ventas (136€)
2. **Madrid** tiene las ventas más bajas (104.50€)
3. La diferencia entre el mejor y el peor es de 31.50€ (30%)

**Decisiones de negocio**:
- Investigar por qué Barcelona vende más
- Aplicar estrategias de Barcelona en Madrid
- Considerar horarios, ubicación, promociones

---

## Ejemplo 3: Validación y Limpieza de Datos con Errores

### Nivel: ⭐⭐ Intermedio

### Contexto

**CloudAPI Systems** te envía un archivo CSV con tiempos de respuesta de su API, pero el archivo tiene **errores de calidad**:
- Valores faltantes
- Valores fuera de rango
- Formatos incorrectos

Tu tarea es:
1. Validar los datos
2. Identificar y reportar errores
3. Limpiar el archivo (eliminar filas inválidas)
4. Generar un reporte de calidad

### Datos

**Archivo**: `api_response_times.csv`

```csv
timestamp,endpoint,response_time_ms,status_code
2025-10-19 10:00:00,/api/users,45,200
2025-10-19 10:01:00,/api/products,123,200
2025-10-19 10:02:00,/api/users,,200
2025-10-19 10:03:00,/api/products,-50,200
2025-10-19 10:04:00,/api/users,5000,500
2025-10-19 10:05:00,/api/products,abc,200
2025-10-19 10:06:00,/api/users,78,200
2025-10-19 10:07:00,,95,200
```

**Problemas identificados**:
- Fila 3: `response_time_ms` vacío
- Fila 4: `response_time_ms` negativo (-50)
- Fila 6: `response_time_ms` no es un número ("abc")
- Fila 8: `endpoint` vacío

---

### Solución Paso a Paso

#### Paso 1: Definir reglas de validación

```python
def validar_fila(fila: dict, num_fila: int) -> list:
    """
    Valida una fila del CSV según reglas de negocio.

    Args:
        fila: Diccionario con los datos de la fila
        num_fila: Número de fila (para reportar errores)

    Returns:
        Lista de errores encontrados (vacía si todo está bien)
    """
    errores = []

    # Regla 1: timestamp no vacío
    if not fila['timestamp'].strip():
        errores.append(f"Fila {num_fila}: timestamp vacío")

    # Regla 2: endpoint no vacío
    if not fila['endpoint'].strip():
        errores.append(f"Fila {num_fila}: endpoint vacío")

    # Regla 3: response_time_ms debe ser un número positivo
    try:
        response_time = float(fila['response_time_ms'])
        if response_time < 0:
            errores.append(f"Fila {num_fila}: response_time_ms negativo ({response_time})")
        elif response_time > 10000:  # Más de 10 segundos es sospechoso
            errores.append(f"Fila {num_fila}: response_time_ms muy alto ({response_time}ms)")
    except ValueError:
        errores.append(f"Fila {num_fila}: response_time_ms no es un número ('{fila['response_time_ms']}')")

    # Regla 4: status_code debe ser un número entre 100 y 599
    try:
        status_code = int(fila['status_code'])
        if status_code < 100 or status_code > 599:
            errores.append(f"Fila {num_fila}: status_code fuera de rango ({status_code})")
    except ValueError:
        errores.append(f"Fila {num_fila}: status_code no es un número")

    return errores
```

---

#### Paso 2: Validar y limpiar el archivo

```python
import csv

def limpiar_csv(archivo_entrada: str, archivo_salida: str, archivo_errores: str) -> dict:
    """
    Valida, limpia y genera reporte de calidad de un CSV.

    Args:
        archivo_entrada: CSV original (con errores)
        archivo_salida: CSV limpio (solo filas válidas)
        archivo_errores: CSV con filas rechazadas

    Returns:
        Diccionario con métricas de calidad
    """
    metricas = {
        'total_filas': 0,
        'filas_validas': 0,
        'filas_invalidas': 0,
        'errores': []
    }

    filas_validas = []
    filas_invalidas = []

    # Leer y validar
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        lector = csv.DictReader(entrada)
        headers = lector.fieldnames

        for num_fila, fila in enumerate(lector, start=2):  # start=2 porque la fila 1 son headers
            metricas['total_filas'] += 1

            # Validar fila
            errores_fila = validar_fila(fila, num_fila)

            if errores_fila:
                metricas['filas_invalidas'] += 1
                metricas['errores'].extend(errores_fila)
                fila['errores'] = '; '.join([e.split(': ')[1] for e in errores_fila])
                filas_invalidas.append(fila)
            else:
                metricas['filas_validas'] += 1
                filas_validas.append(fila)

    # Escribir archivo limpio
    with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
        escritor = csv.DictWriter(salida, fieldnames=headers)
        escritor.writeheader()
        escritor.writerows(filas_validas)

    # Escribir archivo de errores
    with open(archivo_errores, 'w', encoding='utf-8', newline='') as errores:
        headers_errores = headers + ['errores']
        escritor = csv.DictWriter(errores, fieldnames=headers_errores)
        escritor.writeheader()
        escritor.writerows(filas_invalidas)

    return metricas

# Ejecutar limpieza
metricas = limpiar_csv(
    'api_response_times.csv',
    'api_response_times_limpio.csv',
    'api_response_times_errores.csv'
)

# Mostrar reporte
print("📊 REPORTE DE CALIDAD DE DATOS")
print("=" * 60)
print(f"Total de filas procesadas: {metricas['total_filas']}")
print(f"Filas válidas: {metricas['filas_validas']} ({metricas['filas_validas']/metricas['total_filas']*100:.1f}%)")
print(f"Filas inválidas: {metricas['filas_invalidas']} ({metricas['filas_invalidas']/metricas['total_filas']*100:.1f}%)")
print()
print("❌ Errores encontrados:")
for error in metricas['errores']:
    print(f"  - {error}")
```

**Salida**:
```
📊 REPORTE DE CALIDAD DE DATOS
============================================================
Total de filas procesadas: 8
Filas válidas: 4 (50.0%)
Filas inválidas: 4 (50.0%)

❌ Errores encontrados:
  - Fila 3: response_time_ms no es un número ('')
  - Fila 4: response_time_ms negativo (-50.0)
  - Fila 6: response_time_ms no es un número ('abc')
  - Fila 8: endpoint vacío
```

---

### Archivos Generados

**`api_response_times_limpio.csv`** (solo filas válidas):
```csv
timestamp,endpoint,response_time_ms,status_code
2025-10-19 10:00:00,/api/users,45,200
2025-10-19 10:01:00,/api/products,123,200
2025-10-19 10:04:00,/api/users,5000,500
2025-10-19 10:06:00,/api/users,78,200
```

**`api_response_times_errores.csv`** (filas rechazadas):
```csv
timestamp,endpoint,response_time_ms,status_code,errores
2025-10-19 10:02:00,/api/users,,200,response_time_ms no es un número ('')
2025-10-19 10:03:00,/api/products,-50,200,response_time_ms negativo (-50.0)
2025-10-19 10:05:00,/api/products,abc,200,response_time_ms no es un número ('abc')
2025-10-19 10:07:00,,95,200,endpoint vacío
```

---

### Interpretación de Resultados

**Calidad de datos**: 50% de las filas tienen errores (muy bajo, crítico)

**Acciones recomendadas**:
1. **Contactar al equipo de CloudAPI Systems**: Informar sobre los problemas de calidad
2. **Revisar el proceso de generación**: ¿Por qué hay valores vacíos y negativos?
3. **Implementar validaciones en origen**: Prevenir errores antes de enviar el CSV
4. **Automatizar este proceso**: Ejecutar validación en cada carga de datos

---

## Ejemplo 4: Transformación y Enriquecimiento de Datos

### Nivel: ⭐⭐ Intermedio

### Contexto

**LogisticFlow** te envía un CSV con envíos realizados. Necesitas:
1. Calcular el tiempo de entrega (diferencia entre fecha_envio y fecha_entrega)
2. Clasificar envíos por velocidad (Express, Normal, Lento)
3. Añadir una columna con el costo de envío basado en el peso
4. Generar un CSV enriquecido

### Datos

**Archivo**: `envios.csv`

```csv
id_envio,origen,destino,fecha_envio,fecha_entrega,peso_kg
ENV001,Madrid,Barcelona,2025-10-01,2025-10-02,5.5
ENV002,Barcelona,Valencia,2025-10-01,2025-10-04,12.0
ENV003,Madrid,Sevilla,2025-10-02,2025-10-03,3.2
ENV004,Valencia,Madrid,2025-10-02,2025-10-06,8.7
ENV005,Sevilla,Barcelona,2025-10-03,2025-10-04,15.3
```

### Reglas de Negocio

1. **Tiempo de entrega**:
   - Express: ≤ 1 día
   - Normal: 2-3 días
   - Lento: > 3 días

2. **Costo de envío**:
   - 0-5 kg: 10€
   - 5-10 kg: 15€
   - 10-20 kg: 25€
   - > 20 kg: 40€

---

### Solución Paso a Paso

#### Paso 1: Definir funciones de transformación

```python
from datetime import datetime

def calcular_dias_entrega(fecha_envio: str, fecha_entrega: str) -> int:
    """
    Calcula los días entre envío y entrega.

    Args:
        fecha_envio: Fecha en formato YYYY-MM-DD
        fecha_entrega: Fecha en formato YYYY-MM-DD

    Returns:
        Número de días de diferencia
    """
    formato = '%Y-%m-%d'
    envio = datetime.strptime(fecha_envio, formato)
    entrega = datetime.strptime(fecha_entrega, formato)
    diferencia = (entrega - envio).days
    return diferencia

def clasificar_velocidad(dias: int) -> str:
    """
    Clasifica la velocidad de entrega según los días.
    """
    if dias <= 1:
        return 'Express'
    elif dias <= 3:
        return 'Normal'
    else:
        return 'Lento'

def calcular_costo_envio(peso_kg: float) -> float:
    """
    Calcula el costo de envío según el peso.
    """
    if peso_kg <= 5:
        return 10.0
    elif peso_kg <= 10:
        return 15.0
    elif peso_kg <= 20:
        return 25.0
    else:
        return 40.0
```

---

#### Paso 2: Transformar y enriquecer el CSV

```python
import csv

def enriquecer_envios(archivo_entrada: str, archivo_salida: str) -> None:
    """
    Enriquece el CSV de envíos con datos calculados.

    Args:
        archivo_entrada: CSV original
        archivo_salida: CSV enriquecido
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
            lector = csv.DictReader(entrada)

            # Nuevos headers
            fieldnames = list(lector.fieldnames) + ['dias_entrega', 'velocidad', 'costo_envio']
            escritor = csv.DictWriter(salida, fieldnames=fieldnames)
            escritor.writeheader()

            # Procesar cada fila
            for fila in lector:
                # Calcular días de entrega
                dias = calcular_dias_entrega(fila['fecha_envio'], fila['fecha_entrega'])
                fila['dias_entrega'] = dias

                # Clasificar velocidad
                fila['velocidad'] = clasificar_velocidad(dias)

                # Calcular costo
                peso = float(fila['peso_kg'])
                fila['costo_envio'] = calcular_costo_envio(peso)

                # Escribir fila enriquecida
                escritor.writerow(fila)

# Enriquecer datos
enriquecer_envios('envios.csv', 'envios_enriquecidos.csv')
print("✅ Datos enriquecidos guardados en 'envios_enriquecidos.csv'")
```

**Archivo generado**: `envios_enriquecidos.csv`

```csv
id_envio,origen,destino,fecha_envio,fecha_entrega,peso_kg,dias_entrega,velocidad,costo_envio
ENV001,Madrid,Barcelona,2025-10-01,2025-10-02,5.5,1,Express,15.0
ENV002,Barcelona,Valencia,2025-10-01,2025-10-04,12.0,3,Normal,25.0
ENV003,Madrid,Sevilla,2025-10-02,2025-10-03,3.2,1,Express,10.0
ENV004,Valencia,Madrid,2025-10-02,2025-10-06,8.7,4,Lento,15.0
ENV005,Sevilla,Barcelona,2025-10-03,2025-10-04,15.3,1,Express,25.0
```

---

#### Paso 3: Generar estadísticas

```python
import csv
from collections import Counter

def generar_estadisticas(archivo: str) -> dict:
    """
    Genera estadísticas del archivo enriquecido.
    """
    velocidades = []
    costos = []

    with open(archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for fila in lector:
            velocidades.append(fila['velocidad'])
            costos.append(float(fila['costo_envio']))

    # Contar velocidades
    conteo_velocidades = Counter(velocidades)

    # Estadísticas de costos
    costo_promedio = sum(costos) / len(costos)
    costo_total = sum(costos)

    return {
        'velocidades': dict(conteo_velocidades),
        'costo_promedio': costo_promedio,
        'costo_total': costo_total,
        'total_envios': len(velocidades)
    }

# Generar estadísticas
stats = generar_estadisticas('envios_enriquecidos.csv')

print("\n📊 ESTADÍSTICAS DE ENVÍOS")
print("=" * 60)
print(f"Total de envíos: {stats['total_envios']}")
print()
print("Distribución por velocidad:")
for velocidad, cantidad in stats['velocidades'].items():
    porcentaje = (cantidad / stats['total_envios']) * 100
    print(f"  - {velocidad}: {cantidad} ({porcentaje:.1f}%)")
print()
print(f"Costo promedio por envío: {stats['costo_promedio']:.2f}€")
print(f"Costo total: {stats['costo_total']:.2f}€")
```

**Salida**:
```
📊 ESTADÍSTICAS DE ENVÍOS
============================================================
Total de envíos: 5

Distribución por velocidad:
  - Express: 3 (60.0%)
  - Normal: 1 (20.0%)
  - Lento: 1 (20.0%)

Costo promedio por envío: 18.00€
Costo total: 90.00€
```

---

### Interpretación de Resultados

**Hallazgos**:
1. **60% de los envíos son Express** (1 día o menos) - Excelente servicio
2. **20% son lentos** (más de 3 días) - Área de mejora
3. **Costo promedio: 18€** - Rentable si el margen es adecuado

**Decisiones de negocio**:
- Investigar el envío lento (ENV004: Valencia-Madrid, 4 días)
- Considerar promocionar el servicio Express (60% ya lo es)
- Optimizar rutas para reducir envíos lentos

---

## Ejemplo 5: Pipeline ETL Completo con Manejo de Errores

### Nivel: ⭐⭐⭐ Avanzado

### Contexto

Eres el Data Engineer principal de **DataFlow Industries**. Necesitas crear un **pipeline ETL completo** que:

1. **Extract**: Lee datos de ventas de múltiples fuentes (CSV con diferentes formatos)
2. **Transform**: Limpia, valida y transforma los datos
3. **Load**: Carga los datos en un CSV consolidado y genera reportes

El pipeline debe ser **robusto**: manejar errores, generar logs y crear reportes de calidad.

### Datos

**3 archivos de diferentes fuentes**:

**`fuente_a.csv`** (formato americano, delimitador `,`):
```csv
date,product,quantity,unit_price
2025-10-01,Laptop,2,899.99
2025-10-01,Mouse,5,19.99
2025-10-02,Keyboard,3,49.99
```

**`fuente_b.csv`** (formato europeo, delimitador `;`, decimales con `,`):
```csv
fecha;producto;cantidad;precio_unitario
2025-10-01;Monitor;1;299,99
2025-10-02;Webcam;4;79,99
```

**`fuente_c.csv`** (con errores de calidad):
```csv
date,product,quantity,unit_price
2025-10-01,Headphones,,59.99
2025-10-02,Speaker,-2,89.99
2025-10-03,Cable,10,abc
```

---

### Solución: Pipeline ETL Completo

```python
import csv
import os
import logging
from datetime import datetime
from typing import List, Dict, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipelineETL:
    """
    Pipeline ETL robusto para procesar múltiples fuentes de datos CSV.
    """

    def __init__(self):
        self.datos_validos = []
        self.datos_invalidos = []
        self.metricas = {
            'archivos_procesados': 0,
            'filas_totales': 0,
            'filas_validas': 0,
            'filas_invalidas': 0,
            'errores': []
        }

    def extract(self, archivos: List[Dict[str, str]]) -> None:
        """
        Extrae datos de múltiples archivos CSV.

        Args:
            archivos: Lista de diccionarios con configuración de cada archivo
                     [{'ruta': 'file.csv', 'delimitador': ',', 'encoding': 'utf-8'}]
        """
        logger.info("=== FASE 1: EXTRACT ===")

        for config in archivos:
            try:
                self._extract_file(config)
                self.metricas['archivos_procesados'] += 1
            except Exception as e:
                logger.error(f"Error al procesar {config['ruta']}: {e}")
                self.metricas['errores'].append(f"Archivo {config['ruta']}: {e}")

    def _extract_file(self, config: Dict[str, str]) -> None:
        """
        Extrae datos de un archivo CSV individual.
        """
        ruta = config['ruta']
        delimitador = config.get('delimitador', ',')
        encoding = config.get('encoding', 'utf-8')

        logger.info(f"Procesando: {ruta}")

        # Validar que el archivo existe
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

        # Validar que no está vacío
        if os.path.getsize(ruta) == 0:
            raise ValueError(f"Archivo vacío: {ruta}")

        # Leer archivo
        with open(ruta, 'r', encoding=encoding) as archivo:
            lector = csv.DictReader(archivo, delimiter=delimitador)

            for num_fila, fila in enumerate(lector, start=2):
                self.metricas['filas_totales'] += 1

                # Normalizar nombres de columnas (español/inglés)
                fila_normalizada = self._normalizar_fila(fila)

                # Validar y clasificar
                if self._validar_fila(fila_normalizada, ruta, num_fila):
                    self.datos_validos.append(fila_normalizada)
                    self.metricas['filas_validas'] += 1
                else:
                    self.datos_invalidos.append({
                        'archivo': ruta,
                        'fila': num_fila,
                        'datos': fila_normalizada
                    })
                    self.metricas['filas_invalidas'] += 1

    def _normalizar_fila(self, fila: Dict[str, str]) -> Dict[str, str]:
        """
        Normaliza los nombres de columnas y formatos de datos.
        """
        # Mapeo de nombres de columnas
        mapeo = {
            'date': 'fecha',
            'fecha': 'fecha',
            'product': 'producto',
            'producto': 'producto',
            'quantity': 'cantidad',
            'cantidad': 'cantidad',
            'unit_price': 'precio_unitario',
            'precio_unitario': 'precio_unitario'
        }

        fila_normalizada = {}
        for key, value in fila.items():
            nuevo_key = mapeo.get(key.lower(), key.lower())

            # Normalizar decimales (europeo → americano)
            if nuevo_key == 'precio_unitario' and ',' in value:
                value = value.replace(',', '.')

            fila_normalizada[nuevo_key] = value

        return fila_normalizada

    def _validar_fila(self, fila: Dict[str, str], archivo: str, num_fila: int) -> bool:
        """
        Valida que una fila cumple con las reglas de negocio.

        Returns:
            True si la fila es válida, False en caso contrario
        """
        errores = []

        # Validar campos requeridos
        campos_requeridos = ['fecha', 'producto', 'cantidad', 'precio_unitario']
        for campo in campos_requeridos:
            if not fila.get(campo, '').strip():
                errores.append(f"{campo} vacío")

        # Validar cantidad (debe ser entero positivo)
        try:
            cantidad = int(fila['cantidad'])
            if cantidad <= 0:
                errores.append(f"cantidad no positiva ({cantidad})")
        except (ValueError, KeyError):
            errores.append(f"cantidad inválida ('{fila.get('cantidad', '')}')")

        # Validar precio (debe ser float positivo)
        try:
            precio = float(fila['precio_unitario'])
            if precio <= 0:
                errores.append(f"precio no positivo ({precio})")
        except (ValueError, KeyError):
            errores.append(f"precio inválido ('{fila.get('precio_unitario', '')}')")

        # Registrar errores
        if errores:
            error_msg = f"{archivo} - Fila {num_fila}: {'; '.join(errores)}"
            logger.warning(error_msg)
            self.metricas['errores'].append(error_msg)
            return False

        return True

    def transform(self) -> None:
        """
        Transforma los datos válidos: calcula totales, añade timestamps, etc.
        """
        logger.info("=== FASE 2: TRANSFORM ===")

        for fila in self.datos_validos:
            # Calcular total
            cantidad = int(fila['cantidad'])
            precio = float(fila['precio_unitario'])
            fila['total'] = round(cantidad * precio, 2)

            # Añadir timestamp de procesamiento
            fila['procesado_en'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logger.info(f"Transformadas {len(self.datos_validos)} filas")

    def load(self, archivo_salida: str, archivo_errores: str, archivo_reporte: str) -> None:
        """
        Carga los datos transformados en archivos de salida.
        """
        logger.info("=== FASE 3: LOAD ===")

        # Guardar datos válidos
        self._guardar_datos_validos(archivo_salida)

        # Guardar datos inválidos
        self._guardar_datos_invalidos(archivo_errores)

        # Generar reporte
        self._generar_reporte(archivo_reporte)

    def _guardar_datos_validos(self, archivo: str) -> None:
        """
        Guarda los datos válidos en un CSV.
        """
        if not self.datos_validos:
            logger.warning("No hay datos válidos para guardar")
            return

        with open(archivo, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['fecha', 'producto', 'cantidad', 'precio_unitario', 'total', 'procesado_en']
            escritor = csv.DictWriter(f, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(self.datos_validos)

        logger.info(f"✅ Datos válidos guardados en: {archivo}")

    def _guardar_datos_invalidos(self, archivo: str) -> None:
        """
        Guarda los datos inválidos para revisión.
        """
        if not self.datos_invalidos:
            logger.info("No hay datos inválidos")
            return

        with open(archivo, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['archivo', 'fila', 'fecha', 'producto', 'cantidad', 'precio_unitario']
            escritor = csv.DictWriter(f, fieldnames=fieldnames)
            escritor.writeheader()

            for item in self.datos_invalidos:
                fila_salida = {
                    'archivo': item['archivo'],
                    'fila': item['fila'],
                    **item['datos']
                }
                escritor.writerow(fila_salida)

        logger.info(f"⚠️ Datos inválidos guardados en: {archivo}")

    def _generar_reporte(self, archivo: str) -> None:
        """
        Genera un reporte de calidad del pipeline.
        """
        porcentaje_validas = (self.metricas['filas_validas'] / self.metricas['filas_totales'] * 100) if self.metricas['filas_totales'] > 0 else 0

        reporte = f"""
REPORTE DE EJECUCIÓN DEL PIPELINE ETL
{'=' * 60}
Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MÉTRICAS GENERALES:
  - Archivos procesados: {self.metricas['archivos_procesados']}
  - Filas totales: {self.metricas['filas_totales']}
  - Filas válidas: {self.metricas['filas_validas']} ({porcentaje_validas:.1f}%)
  - Filas inválidas: {self.metricas['filas_invalidas']} ({100-porcentaje_validas:.1f}%)

ERRORES ENCONTRADOS:
"""

        if self.metricas['errores']:
            for error in self.metricas['errores']:
                reporte += f"  - {error}\n"
        else:
            reporte += "  ✅ No se encontraron errores\n"

        reporte += f"\n{'=' * 60}\n"

        # Guardar reporte
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(reporte)

        # También mostrar en consola
        print(reporte)
        logger.info(f"📊 Reporte guardado en: {archivo}")

# ===== EJECUTAR PIPELINE =====

def main():
    """
    Función principal que ejecuta el pipeline ETL.
    """
    logger.info("🚀 Iniciando Pipeline ETL")

    # Configuración de archivos de entrada
    archivos = [
        {'ruta': 'fuente_a.csv', 'delimitador': ',', 'encoding': 'utf-8'},
        {'ruta': 'fuente_b.csv', 'delimitador': ';', 'encoding': 'utf-8'},
        {'ruta': 'fuente_c.csv', 'delimitador': ',', 'encoding': 'utf-8'}
    ]

    # Crear y ejecutar pipeline
    pipeline = PipelineETL()

    try:
        # Extract
        pipeline.extract(archivos)

        # Transform
        pipeline.transform()

        # Load
        pipeline.load(
            archivo_salida='datos_consolidados.csv',
            archivo_errores='datos_rechazados.csv',
            archivo_reporte='reporte_pipeline.txt'
        )

        logger.info("✅ Pipeline completado exitosamente")

    except Exception as e:
        logger.error(f"❌ Error crítico en el pipeline: {e}")
        raise

if __name__ == '__main__':
    main()
```

---

### Salida del Pipeline

```
2025-10-19 14:30:00 - INFO - 🚀 Iniciando Pipeline ETL
2025-10-19 14:30:00 - INFO - === FASE 1: EXTRACT ===
2025-10-19 14:30:00 - INFO - Procesando: fuente_a.csv
2025-10-19 14:30:00 - INFO - Procesando: fuente_b.csv
2025-10-19 14:30:00 - INFO - Procesando: fuente_c.csv
2025-10-19 14:30:00 - WARNING - fuente_c.csv - Fila 2: cantidad vacío
2025-10-19 14:30:00 - WARNING - fuente_c.csv - Fila 3: cantidad no positiva (-2)
2025-10-19 14:30:00 - WARNING - fuente_c.csv - Fila 4: precio inválido ('abc')
2025-10-19 14:30:00 - INFO - === FASE 2: TRANSFORM ===
2025-10-19 14:30:00 - INFO - Transformadas 5 filas
2025-10-19 14:30:00 - INFO - === FASE 3: LOAD ===
2025-10-19 14:30:00 - INFO - ✅ Datos válidos guardados en: datos_consolidados.csv
2025-10-19 14:30:00 - INFO - ⚠️ Datos inválidos guardados en: datos_rechazados.csv
2025-10-19 14:30:00 - INFO - 📊 Reporte guardado en: reporte_pipeline.txt
2025-10-19 14:30:00 - INFO - ✅ Pipeline completado exitosamente
```

---

### Archivos Generados

**`datos_consolidados.csv`**:
```csv
fecha,producto,cantidad,precio_unitario,total,procesado_en
2025-10-01,Laptop,2,899.99,1799.98,2025-10-19 14:30:00
2025-10-01,Mouse,5,19.99,99.95,2025-10-19 14:30:00
2025-10-02,Keyboard,3,49.99,149.97,2025-10-19 14:30:00
2025-10-01,Monitor,1,299.99,299.99,2025-10-19 14:30:00
2025-10-02,Webcam,4,79.99,319.96,2025-10-19 14:30:00
```

**`datos_rechazados.csv`**:
```csv
archivo,fila,fecha,producto,cantidad,precio_unitario
fuente_c.csv,2,2025-10-01,Headphones,,59.99
fuente_c.csv,3,2025-10-02,Speaker,-2,89.99
fuente_c.csv,4,2025-10-03,Cable,10,abc
```

**`reporte_pipeline.txt`**:
```
REPORTE DE EJECUCIÓN DEL PIPELINE ETL
============================================================
Fecha de ejecución: 2025-10-19 14:30:00

MÉTRICAS GENERALES:
  - Archivos procesados: 3
  - Filas totales: 8
  - Filas válidas: 5 (62.5%)
  - Filas inválidas: 3 (37.5%)

ERRORES ENCONTRADOS:
  - fuente_c.csv - Fila 2: cantidad vacío
  - fuente_c.csv - Fila 3: cantidad no positiva (-2)
  - fuente_c.csv - Fila 4: precio inválido ('abc')

============================================================
```

---

### Interpretación de Resultados

**Calidad del Pipeline**:
- ✅ Procesó 3 archivos de diferentes formatos exitosamente
- ✅ Normalizó datos (español/inglés, decimales europeos/americanos)
- ✅ Validó y rechazó 3 filas con errores (37.5%)
- ✅ Generó logs detallados y reportes de calidad

**Decisiones de negocio**:
1. **Contactar al proveedor de fuente_c.csv**: 100% de sus datos tienen errores
2. **Automatizar este pipeline**: Ejecutar diariamente con cron/Airflow
3. **Monitorear la calidad**: Alertar si el porcentaje de errores supera el 10%

---

## 🎓 Resumen de Ejemplos

| Ejemplo                  | Nivel      | Conceptos Clave                          |
| ------------------------ | ---------- | ---------------------------------------- |
| 1. Análisis de Ventas    | Básico     | Lectura, agrupación, escritura           |
| 2. Consolidación         | Básico     | Múltiples archivos, añadir columnas      |
| 3. Validación y Limpieza | Intermedio | Validación de datos, manejo de errores   |
| 4. Transformación        | Intermedio | Cálculos, clasificación, enriquecimiento |
| 5. Pipeline ETL          | Avanzado   | ETL completo, logging, robustez          |

---

## 📚 Próximos Pasos

Ahora que has visto estos ejemplos trabajados:

1. **Practica**: Ve al archivo `03-EJERCICIOS.md` y resuelve los ejercicios
2. **Implementa**: Crea tu propio procesador CSV en el proyecto práctico
3. **Experimenta**: Modifica los ejemplos con tus propios datos

---

**¡Felicidades!** Has completado los ejemplos prácticos del Tema 2.

---

*Última actualización: 2025-10-19*
