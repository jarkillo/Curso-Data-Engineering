# Ejercicios Prácticos: Procesamiento de Archivos CSV

Este documento contiene **15 ejercicios** diseñados para que practiques todo lo aprendido sobre procesamiento de archivos CSV.

> **📝 Instrucciones**: Intenta resolver cada ejercicio por tu cuenta antes de ver la solución. Usa las funciones del módulo `csv` de Python y aplica las buenas prácticas que has aprendido.

**Distribución**:
- ⭐ **Ejercicios Básicos** (1-6): Lectura y escritura simple
- ⭐⭐ **Ejercicios Intermedios** (7-11): Validación y transformación
- ⭐⭐⭐ **Ejercicios Avanzados** (12-15): Pipelines complejos

**Duración estimada**: 3-4 horas

---

## 📋 Índice de Ejercicios

### Básicos
1. Leer y mostrar un CSV
2. Contar filas de un CSV
3. Filtrar por columna
4. Crear CSV desde listas
5. Calcular totales
6. Detectar delimitador automáticamente

### Intermedios
7. Validar headers
8. Limpiar valores vacíos
9. Convertir tipos de datos
10. Añadir columna calculada
11. Combinar dos CSVs

### Avanzados
12. Validación completa con reporte
13. Transformación con múltiples reglas
14. Pipeline ETL simplificado
15. Procesamiento de archivo grande (streaming)

---

## Ejercicios Básicos

### Ejercicio 1: Leer y Mostrar un CSV

**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas para **RestaurantData Co.** y te envían un archivo con los productos del menú.

**Datos**:
Crea un archivo `menu.csv` con este contenido:
```csv
producto,categoria,precio
Pizza Margarita,Pizzas,12.50
Pasta Carbonara,Pastas,14.00
Ensalada César,Ensaladas,9.50
Coca-Cola,Bebidas,2.50
Tiramisu,Postres,6.00
```

**Tu tarea**:
1. Leer el archivo usando `csv.DictReader`
2. Mostrar cada producto con su precio en formato: `"Pizza Margarita: 12.50€"`

**Ayuda**:
- Usa `with open()` para abrir el archivo
- Recuerda especificar `encoding='utf-8'`
- Itera sobre el lector con un `for`

---

### Ejercicio 2: Contar Filas de un CSV

**Dificultad**: ⭐ Fácil

**Contexto**:
Necesitas saber cuántos productos tiene el menú (sin contar el header).

**Datos**:
Usa el mismo archivo `menu.csv` del ejercicio anterior.

**Tu tarea**:
1. Leer el archivo
2. Contar cuántas filas de datos tiene (sin contar el header)
3. Mostrar: `"El menú tiene X productos"`

**Ayuda**:
- Puedes usar `enumerate()` para contar
- O simplemente incrementar un contador en el bucle

---

### Ejercicio 3: Filtrar por Columna

**Dificultad**: ⭐ Fácil

**Contexto**:
El gerente quiere ver solo las **Pizzas** del menú.

**Datos**:
Usa el archivo `menu.csv`.

**Tu tarea**:
1. Leer el archivo
2. Filtrar solo los productos de categoría "Pizzas"
3. Mostrar cada pizza encontrada

**Ayuda**:
- Usa una condición `if` dentro del bucle
- Compara `fila['categoria'] == 'Pizzas'`

---

### Ejercicio 4: Crear CSV desde Listas

**Dificultad**: ⭐ Fácil

**Contexto**:
Tienes datos de empleados en listas de Python y necesitas guardarlos en un CSV.

**Datos**:
```python
empleados = [
    ['Ana García', 'Gerente', 45000],
    ['Luis Pérez', 'Cocinero', 28000],
    ['María López', 'Camarera', 22000]
]
```

**Tu tarea**:
1. Crear un archivo `empleados.csv`
2. Escribir los headers: `nombre,puesto,salario`
3. Escribir las filas de datos
4. Verificar que el archivo se creó correctamente

**Ayuda**:
- Usa `csv.writer()`
- Escribe los headers primero con `writerow()`
- Luego escribe todas las filas con `writerows()`

---

### Ejercicio 5: Calcular Totales

**Dificultad**: ⭐ Fácil

**Contexto**:
Necesitas calcular el precio total del menú (suma de todos los precios).

**Datos**:
Usa el archivo `menu.csv`.

**Tu tarea**:
1. Leer el archivo
2. Sumar todos los precios
3. Mostrar: `"Precio total del menú: XX.XX€"`

**Ayuda**:
- Convierte el precio a `float` antes de sumar
- Usa `round()` para redondear a 2 decimales

---

### Ejercicio 6: Detectar Delimitador Automáticamente

**Dificultad**: ⭐ Fácil

**Contexto**:
Te envían un archivo pero no sabes si usa `,` o `;` como delimitador.

**Datos**:
Crea un archivo `datos_europeos.csv` con este contenido:
```csv
nombre;edad;ciudad
Ana;25;Madrid
Luis;30;Barcelona
```

**Tu tarea**:
1. Usar `csv.Sniffer()` para detectar el delimitador automáticamente
2. Leer el archivo con el delimitador detectado
3. Mostrar: `"Delimitador detectado: ;"`
4. Mostrar las filas leídas

**Ayuda**:
- Lee una muestra del archivo con `archivo.read(1024)`
- Usa `sniffer.sniff(muestra).delimiter`
- Recuerda hacer `archivo.seek(0)` para volver al inicio

---

## Ejercicios Intermedios

### Ejercicio 7: Validar Headers

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Recibes archivos CSV de diferentes proveedores y necesitas validar que tengan las columnas correctas.

**Datos**:
Crea dos archivos:

`ventas_correcto.csv`:
```csv
fecha,producto,cantidad,precio
2025-10-01,Laptop,2,899.99
```

`ventas_incorrecto.csv`:
```csv
date,item,qty,price
2025-10-01,Laptop,2,899.99
```

**Tu tarea**:
1. Crear una función `validar_headers(archivo, headers_esperados)`
2. La función debe retornar `True` si los headers coinciden, `False` si no
3. Probar con ambos archivos
4. Mostrar un mensaje claro en cada caso

**Ayuda**:
- Lee solo la primera línea (headers) con `next(lector)`
- Compara con los headers esperados: `['fecha', 'producto', 'cantidad', 'precio']`

---

### Ejercicio 8: Limpiar Valores Vacíos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**CloudAPI Systems** te envía datos con valores vacíos que necesitas limpiar.

**Datos**:
Crea `api_logs.csv`:
```csv
timestamp,endpoint,response_time
2025-10-19 10:00:00,/api/users,45
2025-10-19 10:01:00,,123
2025-10-19 10:02:00,/api/products,
2025-10-19 10:03:00,/api/users,78
```

**Tu tarea**:
1. Leer el archivo
2. Reemplazar valores vacíos:
   - `endpoint` vacío → `"DESCONOCIDO"`
   - `response_time` vacío → `0`
3. Guardar el archivo limpio en `api_logs_limpio.csv`
4. Mostrar cuántos valores vacíos se encontraron

**Ayuda**:
- Usa `if not fila['columna'].strip():` para detectar vacíos
- Reemplaza antes de escribir la nueva fila

---

### Ejercicio 9: Convertir Tipos de Datos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Necesitas convertir los datos de strings a sus tipos correctos y detectar errores.

**Datos**:
Crea `productos.csv`:
```csv
nombre,precio,stock
Laptop,899.99,15
Mouse,19.99,abc
Teclado,xyz,30
Monitor,299.99,8
```

**Tu tarea**:
1. Leer el archivo
2. Intentar convertir:
   - `precio` a `float`
   - `stock` a `int`
3. Si hay error de conversión, mostrar un mensaje y saltar esa fila
4. Guardar solo las filas válidas en `productos_validos.csv`
5. Mostrar un resumen: `"X filas válidas, Y filas inválidas"`

**Ayuda**:
- Usa `try/except ValueError` para capturar errores de conversión
- Lleva un contador de filas válidas e inválidas

---

### Ejercicio 10: Añadir Columna Calculada

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RestaurantData Co.** quiere añadir una columna con el IVA (21%) a sus productos.

**Datos**:
Usa el archivo `menu.csv` del ejercicio 1.

**Tu tarea**:
1. Leer `menu.csv`
2. Calcular el precio con IVA (precio * 1.21)
3. Añadir una columna `precio_con_iva`
4. Guardar en `menu_con_iva.csv`
5. Redondear a 2 decimales

**Ayuda**:
- Añade `'precio_con_iva'` a los fieldnames
- Calcula: `precio_con_iva = float(fila['precio']) * 1.21`
- Usa `round(precio_con_iva, 2)`

---

### Ejercicio 11: Combinar Dos CSVs

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Tienes dos archivos: uno con productos y otro con stock. Necesitas combinarlos.

**Datos**:

`productos.csv`:
```csv
id,nombre,precio
1,Laptop,899.99
2,Mouse,19.99
3,Teclado,49.99
```

`stock.csv`:
```csv
id,cantidad
1,15
2,50
3,30
```

**Tu tarea**:
1. Leer ambos archivos
2. Combinarlos por `id`
3. Crear `productos_completo.csv` con: `id,nombre,precio,cantidad`
4. Manejar el caso donde un `id` no existe en ambos archivos

**Ayuda**:
- Primero lee `stock.csv` y guarda en un diccionario: `{id: cantidad}`
- Luego lee `productos.csv` y busca la cantidad correspondiente
- Si no existe, usa `0` como cantidad

---

## Ejercicios Avanzados

### Ejercicio 12: Validación Completa con Reporte

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Eres el Data Engineer de **DataFlow Industries**. Necesitas crear un validador robusto que genere un reporte detallado.

**Datos**:
Crea `ventas_con_errores.csv`:
```csv
fecha,producto,cantidad,precio
2025-10-01,Laptop,2,899.99
2025-10-02,Mouse,-5,19.99
2025-10-03,,3,49.99
2025-10-04,Teclado,abc,29.99
2025-10-05,Monitor,1,0
2025-10-06,Webcam,2,59.99
```

**Tu tarea**:
1. Crear una función `validar_ventas(archivo_entrada, archivo_reporte)`
2. Validar:
   - `fecha` no vacía
   - `producto` no vacío
   - `cantidad` es entero positivo
   - `precio` es float positivo
3. Generar un reporte en `reporte_validacion.txt` con:
   - Total de filas procesadas
   - Filas válidas e inválidas (con porcentajes)
   - Lista detallada de errores por fila
4. Guardar filas válidas en `ventas_validas.csv`

**Ayuda**:
- Crea una lista de errores por cada fila
- Usa un diccionario para acumular métricas
- Escribe el reporte con formato claro

**Formato esperado del reporte**:
```
REPORTE DE VALIDACIÓN
=====================
Total de filas: 6
Filas válidas: 2 (33.3%)
Filas inválidas: 4 (66.7%)

ERRORES DETALLADOS:
- Fila 3: cantidad negativa (-5)
- Fila 4: producto vacío
- Fila 5: cantidad no es un número ('abc')
- Fila 6: precio cero o negativo (0)
```

---

### Ejercicio 13: Transformación con Múltiples Reglas

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**LogisticFlow** necesita transformar sus datos de envíos aplicando múltiples reglas de negocio.

**Datos**:
Crea `envios_raw.csv`:
```csv
id,origen,destino,peso_kg,distancia_km
E001,Madrid,Barcelona,5.5,620
E002,Barcelona,Valencia,12.0,350
E003,Madrid,Sevilla,3.2,530
E004,Valencia,Madrid,8.7,350
E005,Sevilla,Barcelona,25.5,1000
```

**Tu tarea**:
1. Leer el archivo
2. Aplicar transformaciones:
   - Calcular `costo_base` = distancia_km * 0.50€
   - Calcular `costo_peso`:
     - 0-5 kg: +0€
     - 5-10 kg: +5€
     - 10-20 kg: +10€
     - >20 kg: +20€
   - Calcular `costo_total` = costo_base + costo_peso
   - Clasificar `urgencia`:
     - distancia < 400 km: "LOCAL"
     - 400-700 km: "REGIONAL"
     - >700 km: "NACIONAL"
3. Guardar en `envios_procesados.csv` con todas las columnas nuevas
4. Calcular y mostrar:
   - Costo promedio por envío
   - Distribución por urgencia (cuántos de cada tipo)

**Ayuda**:
- Crea funciones separadas para cada cálculo
- Usa condicionales para las clasificaciones
- Acumula estadísticas mientras procesas

---

### Ejercicio 14: Pipeline ETL Simplificado

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Necesitas crear un pipeline ETL que procese datos de múltiples fuentes, los valide, transforme y consolide.

**Datos**:

`ventas_local_a.csv`:
```csv
fecha,producto,cantidad,precio
2025-10-01,Laptop,2,899.99
2025-10-02,Mouse,5,19.99
```

`ventas_local_b.csv`:
```csv
fecha,producto,cantidad,precio
2025-10-01,Teclado,3,49.99
2025-10-02,Monitor,1,299.99
```

**Tu tarea**:
1. Crear una clase `PipelineVentas` con métodos:
   - `extract(archivos)`: Lee múltiples CSVs
   - `transform()`: Calcula total = cantidad * precio
   - `validate()`: Valida datos (cantidad > 0, precio > 0)
   - `load(archivo_salida)`: Guarda datos consolidados
2. El pipeline debe:
   - Añadir columna `local` (A o B según el archivo)
   - Añadir columna `total`
   - Rechazar filas inválidas
   - Generar logs con `print()` en cada fase
3. Guardar resultado en `ventas_consolidadas.csv`

**Ayuda**:
- Usa `__init__` para inicializar listas de datos
- Guarda datos válidos e inválidos en atributos separados
- Usa métodos para organizar el código

**Estructura esperada**:
```python
class PipelineVentas:
    def __init__(self):
        self.datos_raw = []
        self.datos_validos = []
        self.datos_invalidos = []

    def extract(self, archivos):
        # Tu código aquí
        pass

    def validate(self):
        # Tu código aquí
        pass

    def transform(self):
        # Tu código aquí
        pass

    def load(self, archivo_salida):
        # Tu código aquí
        pass

    def run(self, archivos, archivo_salida):
        self.extract(archivos)
        self.validate()
        self.transform()
        self.load(archivo_salida)
```

---

### Ejercicio 15: Procesamiento de Archivo Grande (Streaming)

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**CloudAPI Systems** te envía un archivo CSV con **millones de registros** de logs. No puedes cargarlo todo en memoria.

**Datos**:
Primero, crea un archivo grande de prueba:

```python
import csv
import random
from datetime import datetime, timedelta

# Generar archivo de prueba con 100,000 filas
with open('logs_grande.csv', 'w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['timestamp', 'endpoint', 'response_time_ms', 'status_code'])

    fecha_base = datetime(2025, 10, 1)
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/payments']

    for i in range(100000):
        timestamp = fecha_base + timedelta(seconds=i)
        endpoint = random.choice(endpoints)
        response_time = random.randint(10, 500)
        status_code = random.choice([200, 200, 200, 200, 404, 500])  # 80% success

        escritor.writerow([
            timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            endpoint,
            response_time,
            status_code
        ])

print("✅ Archivo generado: logs_grande.csv (100,000 filas)")
```

**Tu tarea**:
1. Procesar el archivo **sin cargar todo en memoria** (streaming)
2. Calcular estadísticas:
   - Total de requests
   - Tiempo de respuesta promedio
   - Distribución de status codes (200, 404, 500)
   - Endpoint más lento (mayor tiempo promedio)
3. Generar un archivo `estadisticas_logs.csv` con:
   - Una fila por endpoint
   - Columnas: `endpoint, total_requests, tiempo_promedio, errores`
4. Mostrar el uso de memoria (debe ser bajo y constante)

**Ayuda**:
- **NO uses** `list(lector)` ni cargues todas las filas en una lista
- Procesa línea por línea en el bucle
- Usa diccionarios para acumular estadísticas
- Usa `collections.defaultdict` para simplificar

**Restricción**: Tu solución debe usar **menos de 50 MB de RAM** independientemente del tamaño del archivo.

**Pista para medir memoria**:
```python
import tracemalloc

tracemalloc.start()

# Tu código aquí

current, peak = tracemalloc.get_traced_memory()
print(f"Memoria usada: {current / 1024 / 1024:.2f} MB")
print(f"Pico de memoria: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

---

## Soluciones

### Solución Ejercicio 1

```python
import csv

# Leer y mostrar el CSV
with open('menu.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    print("MENÚ DE RESTAURANTDATA CO.")
    print("-" * 40)

    for fila in lector:
        producto = fila['producto']
        precio = fila['precio']
        print(f"{producto}: {precio}€")
```

**Salida esperada**:
```
MENÚ DE RESTAURANTDATA CO.
----------------------------------------
Pizza Margarita: 12.50€
Pasta Carbonara: 14.00€
Ensalada César: 9.50€
Coca-Cola: 2.50€
Tiramisu: 6.00€
```

---

### Solución Ejercicio 2

```python
import csv

# Contar filas
with open('menu.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    contador = 0
    for fila in lector:
        contador += 1

    print(f"El menú tiene {contador} productos")
```

**Salida esperada**:
```
El menú tiene 5 productos
```

**Alternativa más Pythonica**:
```python
import csv

with open('menu.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    filas = list(lector)
    print(f"El menú tiene {len(filas)} productos")
```

---

### Solución Ejercicio 3

```python
import csv

# Filtrar por categoría
with open('menu.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    print("PIZZAS DEL MENÚ:")
    print("-" * 40)

    for fila in lector:
        if fila['categoria'] == 'Pizzas':
            print(f"- {fila['producto']}: {fila['precio']}€")
```

**Salida esperada**:
```
PIZZAS DEL MENÚ:
----------------------------------------
- Pizza Margarita: 12.50€
```

---

### Solución Ejercicio 4

```python
import csv

# Datos
empleados = [
    ['Ana García', 'Gerente', 45000],
    ['Luis Pérez', 'Cocinero', 28000],
    ['María López', 'Camarera', 22000]
]

# Escribir CSV
with open('empleados.csv', 'w', encoding='utf-8', newline='') as archivo:
    escritor = csv.writer(archivo)

    # Escribir headers
    escritor.writerow(['nombre', 'puesto', 'salario'])

    # Escribir datos
    escritor.writerows(empleados)

print("✅ Archivo 'empleados.csv' creado correctamente")

# Verificar leyendo el archivo
print("\nContenido del archivo:")
with open('empleados.csv', 'r', encoding='utf-8') as archivo:
    print(archivo.read())
```

---

### Solución Ejercicio 5

```python
import csv

# Calcular total
total = 0.0

with open('menu.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        precio = float(fila['precio'])
        total += precio

print(f"Precio total del menú: {total:.2f}€")
```

**Salida esperada**:
```
Precio total del menú: 44.50€
```

---

### Solución Ejercicio 6

```python
import csv

# Detectar delimitador
with open('datos_europeos.csv', 'r', encoding='utf-8') as archivo:
    # Leer muestra
    muestra = archivo.read(1024)
    archivo.seek(0)  # Volver al inicio

    # Detectar delimitador
    sniffer = csv.Sniffer()
    delimitador = sniffer.sniff(muestra).delimiter

    print(f"Delimitador detectado: '{delimitador}'")
    print()

    # Leer con el delimitador correcto
    lector = csv.DictReader(archivo, delimiter=delimitador)

    print("Datos leídos:")
    for fila in lector:
        print(fila)
```

**Salida esperada**:
```
Delimitador detectado: ';'

Datos leídos:
{'nombre': 'Ana', 'edad': '25', 'ciudad': 'Madrid'}
{'nombre': 'Luis', 'edad': '30', 'ciudad': 'Barcelona'}
```

---

### Solución Ejercicio 7

```python
import csv

def validar_headers(archivo: str, headers_esperados: list) -> bool:
    """
    Valida que un CSV tiene los headers esperados.

    Args:
        archivo: Ruta al archivo CSV
        headers_esperados: Lista de headers esperados

    Returns:
        True si los headers coinciden, False si no
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        headers = next(lector)

        if headers == headers_esperados:
            return True
        else:
            print(f"❌ Headers incorrectos en {archivo}")
            print(f"   Esperados: {headers_esperados}")
            print(f"   Encontrados: {headers}")
            return False

# Probar
headers_esperados = ['fecha', 'producto', 'cantidad', 'precio']

print("Validando archivos...")
print()

if validar_headers('ventas_correcto.csv', headers_esperados):
    print("✅ ventas_correcto.csv: Headers correctos")

print()

if validar_headers('ventas_incorrecto.csv', headers_esperados):
    print("✅ ventas_incorrecto.csv: Headers correctos")
```

---

### Solución Ejercicio 8

```python
import csv

# Limpiar valores vacíos
valores_vacios = 0

with open('api_logs.csv', 'r', encoding='utf-8') as entrada:
    with open('api_logs_limpio.csv', 'w', encoding='utf-8', newline='') as salida:
        lector = csv.DictReader(entrada)
        escritor = csv.DictWriter(salida, fieldnames=lector.fieldnames)

        escritor.writeheader()

        for fila in lector:
            # Limpiar endpoint vacío
            if not fila['endpoint'].strip():
                fila['endpoint'] = 'DESCONOCIDO'
                valores_vacios += 1

            # Limpiar response_time vacío
            if not fila['response_time'].strip():
                fila['response_time'] = '0'
                valores_vacios += 1

            escritor.writerow(fila)

print(f"✅ Archivo limpiado")
print(f"   Valores vacíos encontrados y reemplazados: {valores_vacios}")
```

---

### Solución Ejercicio 9

```python
import csv

filas_validas = 0
filas_invalidas = 0

with open('productos.csv', 'r', encoding='utf-8') as entrada:
    with open('productos_validos.csv', 'w', encoding='utf-8', newline='') as salida:
        lector = csv.DictReader(entrada)
        escritor = csv.DictWriter(salida, fieldnames=lector.fieldnames)

        escritor.writeheader()

        for num_fila, fila in enumerate(lector, start=2):
            try:
                # Intentar convertir
                precio = float(fila['precio'])
                stock = int(fila['stock'])

                # Si llegamos aquí, la conversión fue exitosa
                escritor.writerow(fila)
                filas_validas += 1

            except ValueError as e:
                print(f"⚠️ Fila {num_fila}: Error de conversión - {e}")
                filas_invalidas += 1

print()
print(f"📊 Resumen:")
print(f"   Filas válidas: {filas_validas}")
print(f"   Filas inválidas: {filas_invalidas}")
```

---

### Solución Ejercicio 10

```python
import csv

with open('menu.csv', 'r', encoding='utf-8') as entrada:
    with open('menu_con_iva.csv', 'w', encoding='utf-8', newline='') as salida:
        lector = csv.DictReader(entrada)

        # Añadir nueva columna a los fieldnames
        fieldnames = list(lector.fieldnames) + ['precio_con_iva']
        escritor = csv.DictWriter(salida, fieldnames=fieldnames)

        escritor.writeheader()

        for fila in lector:
            # Calcular precio con IVA
            precio = float(fila['precio'])
            precio_con_iva = round(precio * 1.21, 2)
            fila['precio_con_iva'] = precio_con_iva

            escritor.writerow(fila)

print("✅ Archivo 'menu_con_iva.csv' creado con éxito")
```

---

### Solución Ejercicio 11

```python
import csv

# Paso 1: Leer stock en un diccionario
stock_dict = {}
with open('stock.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        id_producto = fila['id']
        cantidad = int(fila['cantidad'])
        stock_dict[id_producto] = cantidad

# Paso 2: Leer productos y combinar con stock
with open('productos.csv', 'r', encoding='utf-8') as entrada:
    with open('productos_completo.csv', 'w', encoding='utf-8', newline='') as salida:
        lector = csv.DictReader(entrada)

        fieldnames = ['id', 'nombre', 'precio', 'cantidad']
        escritor = csv.DictWriter(salida, fieldnames=fieldnames)

        escritor.writeheader()

        for fila in lector:
            id_producto = fila['id']

            # Buscar cantidad en el diccionario
            cantidad = stock_dict.get(id_producto, 0)  # 0 si no existe

            escritor.writerow({
                'id': id_producto,
                'nombre': fila['nombre'],
                'precio': fila['precio'],
                'cantidad': cantidad
            })

print("✅ Archivos combinados en 'productos_completo.csv'")
```

---

### Solución Ejercicio 12

```python
import csv

def validar_ventas(archivo_entrada: str, archivo_reporte: str) -> None:
    """
    Valida un archivo de ventas y genera un reporte detallado.
    """
    metricas = {
        'total': 0,
        'validas': 0,
        'invalidas': 0,
        'errores': []
    }

    filas_validas = []

    # Leer y validar
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        lector = csv.DictReader(entrada)

        for num_fila, fila in enumerate(lector, start=2):
            metricas['total'] += 1
            errores_fila = []

            # Validar fecha
            if not fila['fecha'].strip():
                errores_fila.append("fecha vacía")

            # Validar producto
            if not fila['producto'].strip():
                errores_fila.append("producto vacío")

            # Validar cantidad
            try:
                cantidad = int(fila['cantidad'])
                if cantidad <= 0:
                    errores_fila.append(f"cantidad negativa ({cantidad})")
            except ValueError:
                errores_fila.append(f"cantidad no es un número ('{fila['cantidad']}')")

            # Validar precio
            try:
                precio = float(fila['precio'])
                if precio <= 0:
                    errores_fila.append(f"precio cero o negativo ({precio})")
            except ValueError:
                errores_fila.append(f"precio no es un número ('{fila['precio']}')")

            # Clasificar fila
            if errores_fila:
                metricas['invalidas'] += 1
                metricas['errores'].append(f"Fila {num_fila}: {', '.join(errores_fila)}")
            else:
                metricas['validas'] += 1
                filas_validas.append(fila)

    # Guardar filas válidas
    if filas_validas:
        with open('ventas_validas.csv', 'w', encoding='utf-8', newline='') as salida:
            escritor = csv.DictWriter(salida, fieldnames=['fecha', 'producto', 'cantidad', 'precio'])
            escritor.writeheader()
            escritor.writerows(filas_validas)

    # Generar reporte
    porcentaje_validas = (metricas['validas'] / metricas['total'] * 100) if metricas['total'] > 0 else 0
    porcentaje_invalidas = 100 - porcentaje_validas

    reporte = f"""REPORTE DE VALIDACIÓN
=====================
Total de filas: {metricas['total']}
Filas válidas: {metricas['validas']} ({porcentaje_validas:.1f}%)
Filas inválidas: {metricas['invalidas']} ({porcentaje_invalidas:.1f}%)

ERRORES DETALLADOS:
"""

    if metricas['errores']:
        for error in metricas['errores']:
            reporte += f"- {error}\n"
    else:
        reporte += "✅ No se encontraron errores\n"

    # Guardar reporte
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)

    print(reporte)
    print(f"✅ Reporte guardado en: {archivo_reporte}")

# Ejecutar
validar_ventas('ventas_con_errores.csv', 'reporte_validacion.txt')
```

---

### Solución Ejercicio 13

```python
import csv
from collections import Counter

def calcular_costo_peso(peso_kg: float) -> float:
    """Calcula el costo adicional por peso."""
    if peso_kg <= 5:
        return 0.0
    elif peso_kg <= 10:
        return 5.0
    elif peso_kg <= 20:
        return 10.0
    else:
        return 20.0

def clasificar_urgencia(distancia_km: float) -> str:
    """Clasifica la urgencia según la distancia."""
    if distancia_km < 400:
        return "LOCAL"
    elif distancia_km <= 700:
        return "REGIONAL"
    else:
        return "NACIONAL"

# Procesar envíos
costos_totales = []
urgencias = []

with open('envios_raw.csv', 'r', encoding='utf-8') as entrada:
    with open('envios_procesados.csv', 'w', encoding='utf-8', newline='') as salida:
        lector = csv.DictReader(entrada)

        fieldnames = list(lector.fieldnames) + ['costo_base', 'costo_peso', 'costo_total', 'urgencia']
        escritor = csv.DictWriter(salida, fieldnames=fieldnames)

        escritor.writeheader()

        for fila in lector:
            peso = float(fila['peso_kg'])
            distancia = float(fila['distancia_km'])

            # Calcular costos
            costo_base = distancia * 0.50
            costo_peso = calcular_costo_peso(peso)
            costo_total = costo_base + costo_peso

            # Clasificar urgencia
            urgencia = clasificar_urgencia(distancia)

            # Añadir columnas calculadas
            fila['costo_base'] = round(costo_base, 2)
            fila['costo_peso'] = costo_peso
            fila['costo_total'] = round(costo_total, 2)
            fila['urgencia'] = urgencia

            # Acumular para estadísticas
            costos_totales.append(costo_total)
            urgencias.append(urgencia)

            escritor.writerow(fila)

# Mostrar estadísticas
costo_promedio = sum(costos_totales) / len(costos_totales)
conteo_urgencias = Counter(urgencias)

print("✅ Envíos procesados")
print()
print(f"📊 Estadísticas:")
print(f"   Costo promedio por envío: {costo_promedio:.2f}€")
print()
print("   Distribución por urgencia:")
for urgencia, cantidad in conteo_urgencias.items():
    porcentaje = (cantidad / len(urgencias)) * 100
    print(f"   - {urgencia}: {cantidad} ({porcentaje:.1f}%)")
```

---

### Solución Ejercicio 14

```python
import csv

class PipelineVentas:
    """Pipeline ETL para procesar ventas de múltiples locales."""

    def __init__(self):
        self.datos_raw = []
        self.datos_validos = []
        self.datos_invalidos = []

    def extract(self, archivos: dict) -> None:
        """
        Extrae datos de múltiples archivos CSV.

        Args:
            archivos: Diccionario {nombre_local: ruta_archivo}
        """
        print("=== FASE 1: EXTRACT ===")

        for nombre_local, ruta_archivo in archivos.items():
            print(f"Leyendo: {ruta_archivo}")

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)

                for fila in lector:
                    fila['local'] = nombre_local
                    self.datos_raw.append(fila)

        print(f"Total de filas extraídas: {len(self.datos_raw)}")
        print()

    def validate(self) -> None:
        """Valida los datos extraídos."""
        print("=== FASE 2: VALIDATE ===")

        for fila in self.datos_raw:
            try:
                cantidad = int(fila['cantidad'])
                precio = float(fila['precio'])

                if cantidad > 0 and precio > 0:
                    self.datos_validos.append(fila)
                else:
                    self.datos_invalidos.append(fila)
                    print(f"⚠️ Fila inválida: cantidad={cantidad}, precio={precio}")

            except ValueError:
                self.datos_invalidos.append(fila)
                print(f"⚠️ Fila inválida: error de conversión")

        print(f"Filas válidas: {len(self.datos_validos)}")
        print(f"Filas inválidas: {len(self.datos_invalidos)}")
        print()

    def transform(self) -> None:
        """Transforma los datos válidos."""
        print("=== FASE 3: TRANSFORM ===")

        for fila in self.datos_validos:
            cantidad = int(fila['cantidad'])
            precio = float(fila['precio'])
            fila['total'] = round(cantidad * precio, 2)

        print(f"Filas transformadas: {len(self.datos_validos)}")
        print()

    def load(self, archivo_salida: str) -> None:
        """Carga los datos en el archivo de salida."""
        print("=== FASE 4: LOAD ===")

        with open(archivo_salida, 'w', encoding='utf-8', newline='') as archivo:
            fieldnames = ['local', 'fecha', 'producto', 'cantidad', 'precio', 'total']
            escritor = csv.DictWriter(archivo, fieldnames=fieldnames)

            escritor.writeheader()
            escritor.writerows(self.datos_validos)

        print(f"✅ Datos guardados en: {archivo_salida}")
        print()

    def run(self, archivos: dict, archivo_salida: str) -> None:
        """Ejecuta el pipeline completo."""
        self.extract(archivos)
        self.validate()
        self.transform()
        self.load(archivo_salida)
        print("✅ Pipeline completado exitosamente")

# Ejecutar pipeline
pipeline = PipelineVentas()
archivos = {
    'A': 'ventas_local_a.csv',
    'B': 'ventas_local_b.csv'
}
pipeline.run(archivos, 'ventas_consolidadas.csv')
```

---

### Solución Ejercicio 15

```python
import csv
import tracemalloc
from collections import defaultdict

def procesar_logs_streaming(archivo_entrada: str, archivo_salida: str) -> None:
    """
    Procesa un archivo CSV grande usando streaming (sin cargar todo en memoria).

    Args:
        archivo_entrada: CSV con logs
        archivo_salida: CSV con estadísticas por endpoint
    """
    # Iniciar medición de memoria
    tracemalloc.start()

    # Diccionarios para acumular estadísticas (memoria constante)
    stats = defaultdict(lambda: {
        'total_requests': 0,
        'suma_tiempos': 0,
        'errores': 0
    })

    total_requests = 0

    # Procesar línea por línea (streaming)
    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            total_requests += 1

            endpoint = fila['endpoint']
            response_time = int(fila['response_time_ms'])
            status_code = int(fila['status_code'])

            # Acumular estadísticas
            stats[endpoint]['total_requests'] += 1
            stats[endpoint]['suma_tiempos'] += response_time

            if status_code >= 400:
                stats[endpoint]['errores'] += 1

    # Calcular promedios
    for endpoint, datos in stats.items():
        datos['tiempo_promedio'] = round(datos['suma_tiempos'] / datos['total_requests'], 2)
        del datos['suma_tiempos']  # Ya no lo necesitamos

    # Guardar estadísticas
    with open(archivo_salida, 'w', encoding='utf-8', newline='') as archivo:
        fieldnames = ['endpoint', 'total_requests', 'tiempo_promedio', 'errores']
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)

        escritor.writeheader()

        for endpoint, datos in sorted(stats.items()):
            escritor.writerow({
                'endpoint': endpoint,
                'total_requests': datos['total_requests'],
                'tiempo_promedio': datos['tiempo_promedio'],
                'errores': datos['errores']
            })

    # Medir memoria
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Mostrar resultados
    print("✅ Procesamiento completado")
    print()
    print(f"📊 Estadísticas:")
    print(f"   Total de requests procesados: {total_requests:,}")
    print(f"   Endpoints únicos: {len(stats)}")
    print()
    print(f"💾 Uso de memoria:")
    print(f"   Memoria actual: {current / 1024 / 1024:.2f} MB")
    print(f"   Pico de memoria: {peak / 1024 / 1024:.2f} MB")
    print()

    if peak / 1024 / 1024 < 50:
        print("✅ Uso de memoria eficiente (< 50 MB)")
    else:
        print("⚠️ Uso de memoria alto (> 50 MB)")

# Ejecutar
procesar_logs_streaming('logs_grande.csv', 'estadisticas_logs.csv')
```

**Salida esperada**:
```
✅ Procesamiento completado

📊 Estadísticas:
   Total de requests procesados: 100,000
   Endpoints únicos: 4

💾 Uso de memoria:
   Memoria actual: 2.45 MB
   Pico de memoria: 3.12 MB

✅ Uso de memoria eficiente (< 50 MB)
```

---

## 📊 Tabla de Autoevaluación

Marca cada ejercicio que completes:

| Ejercicio | Completado | Correcto | Notas |
|-----------|------------|----------|-------|
| 1. Leer y mostrar CSV | [ ] | [ ] | |
| 2. Contar filas | [ ] | [ ] | |
| 3. Filtrar por columna | [ ] | [ ] | |
| 4. Crear CSV desde listas | [ ] | [ ] | |
| 5. Calcular totales | [ ] | [ ] | |
| 6. Detectar delimitador | [ ] | [ ] | |
| 7. Validar headers | [ ] | [ ] | |
| 8. Limpiar valores vacíos | [ ] | [ ] | |
| 9. Convertir tipos de datos | [ ] | [ ] | |
| 10. Añadir columna calculada | [ ] | [ ] | |
| 11. Combinar dos CSVs | [ ] | [ ] | |
| 12. Validación con reporte | [ ] | [ ] | |
| 13. Transformación múltiple | [ ] | [ ] | |
| 14. Pipeline ETL | [ ] | [ ] | |
| 15. Procesamiento streaming | [ ] | [ ] | |

---

## 🎓 Criterios de Éxito

Has completado exitosamente este tema si:

- ✅ Resolviste al menos **10 de 15 ejercicios** (67%)
- ✅ Completaste **todos los ejercicios básicos** (1-6)
- ✅ Completaste **al menos 3 ejercicios intermedios** (7-11)
- ✅ Completaste **al menos 1 ejercicio avanzado** (12-15)
- ✅ Tu código sigue las buenas prácticas aprendidas
- ✅ Entiendes por qué cada solución funciona

---

## 📚 Próximos Pasos

Una vez completados los ejercicios:

1. **Implementa el proyecto práctico**: Ve a `04-proyecto-practico/` y crea un procesador CSV robusto con TDD
2. **Aplica lo aprendido**: Usa CSV en tus propios proyectos
3. **Continúa con el Tema 3**: Sistema de Logs y Debugging

---

**¡Felicidades por completar los ejercicios!** 🎉

---

*Última actualización: 2025-10-19*
