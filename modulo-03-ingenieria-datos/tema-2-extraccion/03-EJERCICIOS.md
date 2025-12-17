# Ejercicios Prácticos: Extracción de Datos

> **Instrucciones**: Intenta resolver cada ejercicio por tu cuenta antes de ver las soluciones. Usa las funciones que creaste en el proyecto práctico si están disponibles.

**Contexto**: Eres un Data Engineer en **DataFlow Inc.** y tus clientes necesitan extraer datos de diferentes fuentes. Cada ejercicio simula un caso real que podrías encontrar en tu trabajo.

---

## 📊 Ejercicios Básicos (1-5)

### Ejercicio 1: Detección Automática de Encoding
**Dificultad**: ⭐ Fácil

**Contexto**:
Un cliente te envía un archivo CSV desde un sistema legacy español. No sabes qué encoding usa (podría ser UTF-8, Latin-1, o Windows-1252).

**Datos**:
```python
# Crear archivo con encoding desconocido
datos_espanol = "nombre,ciudad,descripción\nJosé,León,Ingeniero de software\nMaría,Málaga,Analista de datos\n"
with open('clientes_espanol.csv', 'w', encoding='latin-1') as f:
    f.write(datos_espanol)
```

**Tu tarea**:
1. Detecta automáticamente el encoding del archivo
2. Lee el archivo con el encoding correcto usando pandas
3. Imprime las 2 primeras filas
4. Verifica que los caracteres especiales (tildes) se ven correctamente

**Ayuda**: Usa la librería `chardet` para detectar el encoding.

---

### Ejercicio 2: Lectura de JSON Lines (JSONL)
**Dificultad**: ⭐ Fácil

**Contexto**:
Un cliente te proporciona logs de su aplicación en formato JSON Lines (cada línea es un JSON válido).

**Datos**:
```python
logs = """{"timestamp": "2025-01-01 10:00:00", "nivel": "INFO", "mensaje": "Usuario login exitoso", "usuario_id": 123}
{"timestamp": "2025-01-01 10:05:23", "nivel": "ERROR", "mensaje": "Fallo en conexión BD", "usuario_id": 456}
{"timestamp": "2025-01-01 10:10:45", "nivel": "WARNING", "mensaje": "Timeout en API externa", "usuario_id": 789}
{"timestamp": "2025-01-01 10:15:12", "nivel": "INFO", "mensaje": "Usuario logout", "usuario_id": 123}
"""

with open('logs.jsonl', 'w', encoding='utf-8') as f:
    f.write(logs)
```

**Tu tarea**:
1. Lee el archivo JSON Lines línea por línea
2. Convierte cada línea a un diccionario Python
3. Crea un DataFrame de pandas con todos los logs
4. Filtra solo los logs con nivel "ERROR"
5. Imprime cuántos logs de cada nivel existen

**Ayuda**: Usa `json.loads()` para cada línea.

---

### Ejercicio 3: Lectura de Múltiples Hojas de Excel
**Dificultad**: ⭐ Fácil

**Contexto**:
Un cliente te envía un archivo Excel con ventas de 3 meses en diferentes hojas.

**Datos**:
```python
import pandas as pd

# Crear Excel con 3 hojas
ventas_enero = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'ventas': [50, 200, 150]
})

ventas_febrero = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'ventas': [60, 210, 140]
})

ventas_marzo = pd.DataFrame({
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'ventas': [55, 195, 160]
})

with pd.ExcelWriter('ventas_trimestre.xlsx') as writer:
    ventas_enero.to_excel(writer, sheet_name='Enero', index=False)
    ventas_febrero.to_excel(writer, sheet_name='Febrero', index=False)
    ventas_marzo.to_excel(writer, sheet_name='Marzo', index=False)
```

**Tu tarea**:
1. Lee todas las hojas del Excel en un diccionario
2. Combina las 3 hojas en un solo DataFrame
3. Agrega una columna "mes" que indique de qué hoja vienen los datos
4. Calcula el total de ventas por producto (suma de los 3 meses)
5. Imprime el producto más vendido

**Ayuda**: Usa `pd.read_excel(sheet_name=None)` para leer todas las hojas.

---

### Ejercicio 4: Limpieza de CSV con Valores Nulos
**Dificultad**: ⭐ Fácil

**Contexto**:
Un cliente te envía un CSV con datos "sucios" que contiene varios tipos de valores nulos representados de diferentes formas.

**Datos**:
```python
datos_sucios = """nombre,edad,ciudad,salario
Ana,28,Madrid,45000
Carlos,,Barcelona,
Pedro,35,NULL,52000
,42,Valencia,N/A
Laura,29,,48000
"""

with open('datos_sucios.csv', 'w') as f:
    f.write(datos_sucios)
```

**Tu tarea**:
1. Lee el CSV especificando qué valores considerar como nulos: `['', 'NULL', 'N/A']`
2. Imprime cuántos valores nulos hay en cada columna
3. Elimina las filas donde falte el nombre (columna crítica)
4. Rellena los valores nulos de "ciudad" con "Desconocido"
5. Rellena los valores nulos de "edad" y "salario" con la media de esa columna

**Ayuda**: Usa `na_values` en `pd.read_csv()`.

---

### Ejercicio 5: Validación de Estructura de CSV
**Dificultad**: ⭐ Fácil

**Contexto**:
Recibes CSVs de múltiples proveedores y necesitas validar que tengan la estructura esperada antes de procesarlos.

**Datos**:
```python
# CSV válido
csv_valido = """id,nombre,precio,stock
1,Producto A,29.99,100
2,Producto B,49.99,50
"""

# CSV inválido (falta columna "stock")
csv_invalido = """id,nombre,precio
1,Producto A,29.99
2,Producto B,49.99
"""

with open('productos_valido.csv', 'w') as f:
    f.write(csv_valido)

with open('productos_invalido.csv', 'w') as f:
    f.write(csv_invalido)
```

**Tu tarea**:
1. Crea una función `validar_estructura_csv(archivo, columnas_requeridas)` que:
   - Lee el CSV
   - Verifica que todas las columnas requeridas existen
   - Retorna `True` si es válido, `False` si no
   - Imprime qué columnas faltan si es inválido
2. Prueba la función con ambos archivos
3. Define las columnas requeridas como: `['id', 'nombre', 'precio', 'stock']`

**Ayuda**: Usa `set()` para comparar columnas esperadas vs presentes.

---

## 🔧 Ejercicios Intermedios (6-10)

### Ejercicio 6: API con Autenticación Bearer Token
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Necesitas consumir una API que requiere autenticación con Bearer Token. El token debe ir en el header `Authorization: Bearer <token>`.

**Datos**:
```python
# Simularemos la API con JSONPlaceholder (API pública de prueba)
# En la realidad, tendrías un token real
API_URL = "https://jsonplaceholder.typicode.com/posts"
TOKEN = "fake_token_123456"  # En producción, esto vendría de variable de entorno
```

**Tu tarea**:
1. Crea una función `hacer_peticion_autenticada(url, token)` que:
   - Construye el header con `Authorization: Bearer {token}`
   - Hace una petición GET
   - Retorna los datos JSON si es exitosa (status 200)
   - Lanza una excepción si falla (status != 200)
2. Prueba la función con JSONPlaceholder (no valida el token, así que funcionará)
3. Extrae los primeros 5 posts
4. Convierte a DataFrame y muestra las columnas: id, title

**Ayuda**: El header debe ser: `{'Authorization': f'Bearer {token}'}`

---

### Ejercicio 7: Paginación Offset-Based
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Una API devuelve datos paginados usando `offset` y `limit`. Debes extraer TODOS los datos hasta que no haya más.

**Datos**:
```python
# Usaremos JSONPlaceholder que soporta paginación
API_BASE = "https://jsonplaceholder.typicode.com/posts"
# Parámetros: ?_start=0&_limit=10
```

**Tu tarea**:
1. Crea una función `extraer_datos_paginados(url_base, limit_por_pagina)` que:
   - Comience en offset=0
   - Haga peticiones incrementando el offset: 0, 10, 20, 30...
   - Agregue los datos de cada página a una lista
   - Termine cuando una página devuelva 0 resultados
   - Implemente un sleep de 0.5s entre peticiones (rate limiting)
2. Extrae todos los posts (hay ~100 en total)
3. Imprime cuántos posts se extrajeron en total

**Ayuda**: Los parámetros son `_start` (offset) y `_limit` (cantidad por página).

---

### Ejercicio 8: Manejo de Errores 429 (Rate Limit)
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Estás consumiendo una API que tiene rate limiting. Si haces muchas peticiones rápido, devuelve error 429. Debes implementar reintentos con backoff.

**Tu tarea**:
1. Crea una función `peticion_con_rate_limit_handling(url, max_reintentos=3)` que:
   - Intente hacer la petición
   - Si recibe status 429, espere 2 segundos y reintente
   - Si recibe status 500-599, espere exponencialmente (1s, 2s, 4s) y reintente
   - Si recibe status 200, devuelva los datos
   - Si recibe status 400-499 (excepto 429), lance una excepción inmediatamente
   - Si agota los reintentos, lance una excepción
2. Implementa logging para cada intento
3. Prueba con una URL válida

**Ayuda**: Usa `time.sleep()` para esperar entre reintentos.

---

### Ejercicio 9: Scraping de Tabla HTML
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Necesitas extraer datos de una tabla HTML que contiene información de empleados.

**Datos**:
```python
html_tabla = """
<!DOCTYPE html>
<html>
<body>
    <table id="empleados">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Departamento</th>
                <th>Salario</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>001</td>
                <td>Ana García</td>
                <td>IT</td>
                <td>€45,000</td>
            </tr>
            <tr>
                <td>002</td>
                <td>Carlos López</td>
                <td>Ventas</td>
                <td>€38,000</td>
            </tr>
            <tr>
                <td>003</td>
                <td>Laura Martín</td>
                <td>IT</td>
                <td>€52,000</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

with open('empleados_tabla.html', 'w', encoding='utf-8') as f:
    f.write(html_tabla)
```

**Tu tarea**:
1. Lee el HTML y parsealo con Beautiful Soup
2. Extrae la tabla con id="empleados"
3. Convierte la tabla a DataFrame usando `pd.read_html()` O manualmente
4. Limpia la columna "Salario" (quitar "€" y ",", convertir a int)
5. Calcula el salario promedio por departamento
6. Imprime el departamento con mayor salario promedio

**Ayuda**: `pd.read_html(str(tabla))` puede extraer tablas automáticamente.

---

### Ejercicio 10: Verificar robots.txt Antes de Scrapear
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Antes de scrapear cualquier sitio web, debes verificar su archivo `robots.txt` para ver qué está permitido.

**Tu tarea**:
1. Crea una función `verificar_scraping_permitido(url_base, user_agent='*')` que:
   - Construya la URL del robots.txt: `{url_base}/robots.txt`
   - Haga una petición GET al robots.txt
   - Parsee el contenido buscando reglas para el user_agent
   - Retorne `True` si el scraping está permitido, `False` si no
   - Maneje el caso donde no existe robots.txt (asumir permitido)
2. Prueba con URLs reales:
   - https://www.python.org (tiene robots.txt)
   - https://example.com (probablemente no tiene)
3. Imprime el contenido del robots.txt si existe

**Ayuda**: Si el status es 404, no existe robots.txt (asumir permitido).

---

## 🚀 Ejercicios Avanzados (11-15)

### Ejercicio 11: Pipeline de Extracción Multi-Fuente
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Debes construir un pipeline que extraiga datos de 3 fuentes diferentes y los consolide en un reporte único.

**Datos**:
```python
# Fuente 1: CSV de productos locales
productos_csv = """sku,nombre,precio
SKU001,Laptop,1200
SKU002,Mouse,25
SKU003,Teclado,80
"""

# Fuente 2: JSON de stock desde API
stock_json = {
    "SKU001": {"cantidad": 15, "almacen": "A"},
    "SKU002": {"cantidad": 150, "almacen": "B"},
    "SKU003": {"cantidad": 80, "almacen": "A"}
}

# Fuente 3: HTML con reviews
reviews_html = """
<html>
<body>
    <div class="producto" data-sku="SKU001">
        <span class="rating">4.5</span>
    </div>
    <div class="producto" data-sku="SKU002">
        <span class="rating">4.8</span>
    </div>
    <div class="producto" data-sku="SKU003">
        <span class="rating">4.2</span>
    </div>
</body>
</html>
"""

# Crear archivos
with open('productos.csv', 'w') as f:
    f.write(productos_csv)

import json
with open('stock.json', 'w') as f:
    json.dump(stock_json, f)

with open('reviews.html', 'w') as f:
    f.write(reviews_html)
```

**Tu tarea**:
1. Extrae datos de las 3 fuentes
2. Consolida todo en un solo DataFrame usando "sku" como clave
3. Calcula un "score" combinado: `(rating / 5) * precio * (cantidad / 100)`
4. Identifica el producto con mejor score
5. Guarda el reporte consolidado en CSV y Excel

**Ayuda**: Usa múltiples `.merge()` para consolidar.

---

### Ejercicio 12: Extracción Robusta con Logging
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Debes extraer datos de una API que puede fallar ocasionalmente. Necesitas logging completo para debugging.

**Tu tarea**:
1. Configura logging para que guarde en archivo "extraccion.log"
2. Crea una función `extraer_con_logging(url)` que:
   - Registre el inicio de la extracción (timestamp, URL)
   - Haga la petición con reintentos (máx 3)
   - Registre cada intento fallido (con el error)
   - Registre el éxito (cuántos datos se obtuvieron)
   - Registre la duración total
   - Retorne los datos o None si falla completamente
3. Prueba con JSONPlaceholder
4. Revisa el archivo de log generado

**Ayuda**: Usa `logging.basicConfig()` con `filename='extraccion.log'`.

---

### Ejercicio 13: Scraping con Manejo de Contenido Dinámico
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Intentas scrapear un sitio que carga datos con JavaScript. Beautiful Soup no puede ver ese contenido. Debes buscar la API oculta.

**Tu tarea**:
1. **Simula el problema**: Crea un HTML que solo muestre un loading inicial
2. **Inspecciona Network**: En un sitio real, abrirías DevTools → Network → XHR
3. **Encuentra la API**: Busca peticiones JSON que carguen los datos
4. **Consume la API**: En lugar de scrapear HTML, consume la API directamente
5. Documenta el proceso de investigación

**Ayuda práctica**:
```python
# Muchos sitios tienen APIs "ocultas" como:
# https://ejemplo.com/api/v1/productos.json
# En lugar de scrapear:
# https://ejemplo.com/productos

# Ejemplo real con JSONPlaceholder:
# HTML (no útil): https://jsonplaceholder.typicode.com
# API (útil): https://jsonplaceholder.typicode.com/posts
```

**Realiza**:
1. Accede a JSONPlaceholder HTML vs API
2. Compara qué datos obtienes de cada uno
3. Escribe una función que priorice API sobre scraping

---

### Ejercicio 14: Caché de Peticiones API
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Haces muchas peticiones a una API lenta. Para no repetir peticiones idénticas, implementa un sistema de caché.

**Tu tarea**:
1. Crea una función `extraer_con_cache(url, cache_file='cache.json', ttl_segundos=3600)` que:
   - Verifique si ya existe en caché
   - Si existe y no ha expirado (< TTL), retorne del caché
   - Si no existe o expiró, haga la petición
   - Guarde en caché con timestamp
   - Retorne los datos
2. Implementa el caché en archivo JSON
3. Prueba haciendo la misma petición 2 veces:
   - Primera vez: debe hacer petición real (lento)
   - Segunda vez: debe usar caché (instantáneo)
4. Imprime de dónde vinieron los datos (caché o API)

**Ayuda**: Estructura del caché:
```json
{
  "url": {
    "timestamp": 1234567890,
    "datos": {...}
  }
}
```

---

### Ejercicio 15: Pipeline Completo con Orquestación
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
Necesitas un pipeline completo que:
1. Extraiga datos de múltiples fuentes
2. Valide que los datos son correctos
3. Consolide todo
4. Guarde en múltiples formatos
5. Genere un reporte de ejecución
6. Maneje errores robustamente

**Tu tarea**:
Crea una función `ejecutar_pipeline_completo()` que:
1. **Extracción**:
   - Lee CSV de productos
   - Consume API de precios
   - Scrapea reviews de HTML
2. **Validación**:
   - Verifica que no hay valores nulos críticos
   - Verifica que los SKUs coinciden entre fuentes
   - Valida rangos de precios (> 0, < 100000)
3. **Consolidación**:
   - Merge de las 3 fuentes
   - Calcula KPIs (precio promedio, rating promedio)
4. **Guardado**:
   - CSV
   - JSON
   - Excel
5. **Reporte**:
   - Genera un reporte de ejecución con:
     - Timestamp de inicio y fin
     - Duración total
     - Cantidad de registros por fuente
     - Cantidad de errores (si hubo)
     - Archivos generados

**Ayuda**: Usa try/except en cada etapa y registra errores en una lista.

---

## 📊 Tabla de Autoevaluación

| Ejercicio | Nivel | Completado | Correcto | Tiempo (min) | Notas |
|-----------|-------|------------|----------|--------------|-------|
| 1 - Encoding | ⭐ | [ ] | [ ] | | |
| 2 - JSON Lines | ⭐ | [ ] | [ ] | | |
| 3 - Excel múltiple | ⭐ | [ ] | [ ] | | |
| 4 - CSV sucio | ⭐ | [ ] | [ ] | | |
| 5 - Validación | ⭐ | [ ] | [ ] | | |
| 6 - API Auth | ⭐⭐ | [ ] | [ ] | | |
| 7 - Paginación | ⭐⭐ | [ ] | [ ] | | |
| 8 - Rate Limit | ⭐⭐ | [ ] | [ ] | | |
| 9 - Scraping tabla | ⭐⭐ | [ ] | [ ] | | |
| 10 - robots.txt | ⭐⭐ | [ ] | [ ] | | |
| 11 - Multi-fuente | ⭐⭐⭐ | [ ] | [ ] | | |
| 12 - Logging | ⭐⭐⭐ | [ ] | [ ] | | |
| 13 - API oculta | ⭐⭐⭐ | [ ] | [ ] | | |
| 14 - Caché | ⭐⭐⭐ | [ ] | [ ] | | |
| 15 - Pipeline completo | ⭐⭐⭐ | [ ] | [ ] | | |

---

## 💡 Soluciones

### Solución Ejercicio 1: Detección Automática de Encoding

```python
import chardet
import pandas as pd

# Detectar encoding
def detectar_encoding(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        resultado = chardet.detect(f.read())
    return resultado['encoding']

# Aplicar
encoding = detectar_encoding('clientes_espanol.csv')
print(f"Encoding detectado: {encoding}")

# Leer con encoding correcto
df = pd.read_csv('clientes_espanol.csv', encoding=encoding)
print("\n✅ Datos leídos correctamente:")
print(df.head(2))

# Verificar caracteres especiales
assert 'José' in df['nombre'].values
assert 'Málaga' in df['ciudad'].values
print("\n✅ Caracteres especiales correctos")
```

**Resultado esperado**:
```
Encoding detectado: ISO-8859-1

✅ Datos leídos correctamente:
  nombre ciudad            descripción
0   José   León  Ingeniero de software
1  María Málaga      Analista de datos

✅ Caracteres especiales correctos
```

---

### Solución Ejercicio 2: Lectura de JSON Lines

```python
import json
import pandas as pd

# Leer JSON Lines
registros = []
with open('logs.jsonl', 'r', encoding='utf-8') as f:
    for linea in f:
        registro = json.loads(linea.strip())
        registros.append(registro)

# Convertir a DataFrame
df_logs = pd.DataFrame(registros)

# Filtrar errores
df_errores = df_logs[df_logs['nivel'] == 'ERROR']
print(f"✅ Logs con ERROR: {len(df_errores)}")

# Contar por nivel
conteo_niveles = df_logs['nivel'].value_counts()
print("\n📊 Logs por nivel:")
print(conteo_niveles)
```

**Resultado esperado**:
```
✅ Logs con ERROR: 1

📊 Logs por nivel:
INFO       2
ERROR      1
WARNING    1
```

---

### Solución Ejercicio 3: Múltiples Hojas de Excel

```python
import pandas as pd

# Leer todas las hojas
todas_las_hojas = pd.read_excel('ventas_trimestre.xlsx', sheet_name=None)

# Combinar con columna de mes
df_combinado = pd.DataFrame()
for mes, df in todas_las_hojas.items():
    df['mes'] = mes
    df_combinado = pd.concat([df_combinado, df], ignore_index=True)

print("✅ Datos combinados:")
print(df_combinado)

# Total por producto
total_por_producto = df_combinado.groupby('producto')['ventas'].sum()
print("\n📊 Total de ventas por producto:")
print(total_por_producto)

# Producto más vendido
producto_top = total_por_producto.idxmax()
print(f"\n🏆 Producto más vendido: {producto_top}")
```

**Resultado esperado**:
```
✅ Datos combinados:
  producto  ventas      mes
0   Laptop      50    Enero
1    Mouse     200    Enero
...

📊 Total de ventas por producto:
Laptop      165
Mouse       605
Teclado     450

🏆 Producto más vendido: Mouse
```

---

### Solución Ejercicio 4: Limpieza de CSV

```python
import pandas as pd

# Leer con valores nulos especificados
df = pd.read_csv('datos_sucios.csv', na_values=['', 'NULL', 'N/A'])

print("🔍 Valores nulos por columna:")
print(df.isnull().sum())

# Eliminar filas sin nombre
df = df.dropna(subset=['nombre'])

# Rellenar ciudad con "Desconocido"
df['ciudad'] = df['ciudad'].fillna('Desconocido')

# Rellenar edad y salario con la media
df['edad'] = df['edad'].fillna(df['edad'].mean())
df['salario'] = df['salario'].fillna(df['salario'].mean())

print("\n✅ Datos limpios:")
print(df)
```

---

### Solución Ejercicio 5: Validación de Estructura

```python
import pandas as pd

def validar_estructura_csv(archivo, columnas_requeridas):
    """Valida que un CSV tiene la estructura esperada"""
    df = pd.read_csv(archivo)
    columnas_presentes = set(df.columns)
    columnas_esperadas = set(columnas_requeridas)

    columnas_faltantes = columnas_esperadas - columnas_presentes

    if columnas_faltantes:
        print(f"❌ Columnas faltantes: {columnas_faltantes}")
        return False
    else:
        print("✅ Estructura válida")
        return True

# Probar
columnas_req = ['id', 'nombre', 'precio', 'stock']

print("Validando CSV válido:")
validar_estructura_csv('productos_valido.csv', columnas_req)

print("\nValidando CSV inválido:")
validar_estructura_csv('productos_invalido.csv', columnas_req)
```

**Resultado esperado**:
```
Validando CSV válido:
✅ Estructura válida

Validando CSV inválido:
❌ Columnas faltantes: {'stock'}
```

---

### Solución Ejercicio 6: API con Autenticación

```python
import requests
import pandas as pd

def hacer_peticion_autenticada(url, token):
    """Hace petición con autenticación Bearer"""
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Probar
url = "https://jsonplaceholder.typicode.com/posts"
token = "fake_token_123"

datos = hacer_peticion_autenticada(url, token)
df = pd.DataFrame(datos[:5])

print("✅ Datos extraídos:")
print(df[['id', 'title']])
```

---

### Solución Ejercicio 7: Paginación

```python
import requests
import time

def extraer_datos_paginados(url_base, limit_por_pagina=10):
    """Extrae todos los datos paginados"""
    todos_los_datos = []
    offset = 0

    while True:
        params = {
            '_start': offset,
            '_limit': limit_por_pagina
        }

        response = requests.get(url_base, params=params)
        datos = response.json()

        if not datos or len(datos) == 0:
            break

        todos_los_datos.extend(datos)
        print(f"📦 Extraídos {len(datos)} registros (total: {len(todos_los_datos)})")

        offset += limit_por_pagina
        time.sleep(0.5)  # Rate limiting

    return todos_los_datos

# Usar
url = "https://jsonplaceholder.typicode.com/posts"
datos = extraer_datos_paginados(url, limit_por_pagina=10)
print(f"\n✅ Total extraído: {len(datos)} posts")
```

---

### Solución Ejercicio 8: Rate Limit Handling

```python
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def peticion_con_rate_limit_handling(url, max_reintentos=3):
    """Maneja rate limits y errores con reintentos"""

    for intento in range(max_reintentos):
        try:
            logger.info(f"Intento {intento + 1}")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                logger.info("✅ Petición exitosa")
                return response.json()

            elif response.status_code == 429:
                logger.warning("⚠️ Rate limit excedido, esperando 2s")
                time.sleep(2)

            elif 500 <= response.status_code < 600:
                tiempo_espera = 2 ** intento
                logger.warning(f"⚠️ Error {response.status_code}, esperando {tiempo_espera}s")
                time.sleep(tiempo_espera)

            else:
                raise Exception(f"Error {response.status_code}")

        except requests.exceptions.Timeout:
            logger.warning("⚠️ Timeout")
            time.sleep(2 ** intento)

    raise Exception("❌ Agotados los reintentos")

# Probar
url = "https://jsonplaceholder.typicode.com/posts/1"
datos = peticion_con_rate_limit_handling(url)
print(f"\n✅ Datos obtenidos: {datos['title']}")
```

---

### Solución Ejercicio 9: Scraping de Tabla

```python
from bs4 import BeautifulSoup
import pandas as pd

# Leer HTML
with open('empleados_tabla.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Extraer tabla
tabla = soup.find('table', id='empleados')
df = pd.read_html(str(tabla))[0]

# Limpiar salario
df['Salario'] = df['Salario'].str.replace('€', '').str.replace(',', '').astype(int)

# Calcular promedio por departamento
promedio_dept = df.groupby('Departamento')['Salario'].mean()

print("📊 Salario promedio por departamento:")
print(promedio_dept)

print(f"\n🏆 Departamento con mayor salario: {promedio_dept.idxmax()}")
```

---

### Solución Ejercicio 10: Verificar robots.txt

```python
import requests

def verificar_scraping_permitido(url_base, user_agent='*'):
    """Verifica si el scraping está permitido según robots.txt"""
    robots_url = f"{url_base}/robots.txt"

    try:
        response = requests.get(robots_url, timeout=10)

        if response.status_code == 404:
            print("ℹ️ No existe robots.txt, asumiendo permitido")
            return True

        if response.status_code == 200:
            print(f"✅ robots.txt encontrado:\n{response.text[:500]}")

            # Parseo simple: buscar "Disallow: /"
            if "Disallow: /" in response.text:
                print("⚠️ Scraping podría estar restringido")
                return False
            else:
                print("✅ Scraping parece permitido")
                return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Probar
verificar_scraping_permitido("https://www.python.org")
```

---

### Solución Ejercicio 11: Pipeline Multi-Fuente

```python
import pandas as pd
import json
from bs4 import BeautifulSoup

# 1. Extraer de CSV
df_productos = pd.read_csv('productos.csv')

# 2. Extraer de JSON
with open('stock.json', 'r') as f:
    stock_data = json.load(f)
df_stock = pd.DataFrame([
    {'sku': k, 'cantidad': v['cantidad'], 'almacen': v['almacen']}
    for k, v in stock_data.items()
])

# 3. Extraer de HTML
with open('reviews.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

reviews = []
for div in soup.find_all('div', class_='producto'):
    reviews.append({
        'sku': div['data-sku'],
        'rating': float(div.find('span', class_='rating').text)
    })
df_reviews = pd.DataFrame(reviews)

# 4. Consolidar
df_consolidado = df_productos.merge(df_stock, on='sku').merge(df_reviews, on='sku')

# 5. Calcular score
df_consolidado['score'] = (df_consolidado['rating'] / 5) * df_consolidado['precio'] * (df_consolidado['cantidad'] / 100)

print("📊 Reporte consolidado:")
print(df_consolidado)

print(f"\n🏆 Producto con mejor score: {df_consolidado.loc[df_consolidado['score'].idxmax(), 'nombre']}")

# 6. Guardar
df_consolidado.to_csv('reporte_consolidado.csv', index=False)
df_consolidado.to_excel('reporte_consolidado.xlsx', index=False)
print("\n✅ Reporte guardado")
```

---

### Solución Ejercicio 12: Logging

```python
import requests
import logging
from datetime import datetime
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraccion.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def extraer_con_logging(url, max_reintentos=3):
    """Extrae datos con logging completo"""
    inicio = datetime.now()
    logger.info(f"🚀 Iniciando extracción: {url}")

    for intento in range(max_reintentos):
        try:
            logger.info(f"Intento {intento + 1}/{max_reintentos}")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                datos = response.json()
                duracion = (datetime.now() - inicio).total_seconds()
                logger.info(f"✅ Extracción exitosa: {len(datos)} registros en {duracion:.2f}s")
                return datos
            else:
                logger.warning(f"⚠️ Status {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")

        time.sleep(2 ** intento)

    logger.error(f"❌ Extracción falló después de {max_reintentos} intentos")
    return None

# Usar
datos = extraer_con_logging("https://jsonplaceholder.typicode.com/posts")
print(f"\n✅ Ver logs en extraccion.log")
```

---

### Solución Ejercicio 13: API Oculta

```python
import requests

def buscar_api_oculta(url_base):
    """Busca APIs comunes en sitios web"""
    posibles_apis = [
        f"{url_base}/api/v1/data.json",
        f"{url_base}/api/data.json",
        f"{url_base}/data.json",
        f"{url_base}/api/posts",
    ]

    for api_url in posibles_apis:
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API encontrada: {api_url}")
                return api_url
        except:
            continue

    print("❌ No se encontró API oculta")
    return None

# Ejemplo con JSONPlaceholder
url_base = "https://jsonplaceholder.typicode.com"
api_url = buscar_api_oculta(url_base)

if api_url:
    datos = requests.get(api_url).json()
    print(f"📦 Datos obtenidos: {len(datos)} registros")
```

---

### Solución Ejercicio 14: Caché

```python
import requests
import json
import time
from datetime import datetime

def extraer_con_cache(url, cache_file='cache.json', ttl_segundos=3600):
    """Extrae con sistema de caché"""

    # Leer caché existente
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except:
        cache = {}

    # Verificar si existe en caché y no expiró
    if url in cache:
        timestamp_cache = cache[url]['timestamp']
        edad = time.time() - timestamp_cache

        if edad < ttl_segundos:
            print(f"✅ Usando caché (edad: {edad:.0f}s)")
            return cache[url]['datos']
        else:
            print(f"⚠️ Caché expirado (edad: {edad:.0f}s)")

    # Hacer petición real
    print("🌐 Haciendo petición a API...")
    response = requests.get(url)
    datos = response.json()

    # Guardar en caché
    cache[url] = {
        'timestamp': time.time(),
        'datos': datos
    }

    with open(cache_file, 'w') as f:
        json.dump(cache, f)

    print("✅ Datos guardados en caché")
    return datos

# Probar
url = "https://jsonplaceholder.typicode.com/posts/1"

print("Primera petición:")
datos1 = extraer_con_cache(url, ttl_segundos=60)

time.sleep(2)

print("\nSegunda petición (debe usar caché):")
datos2 = extraer_con_cache(url, ttl_segundos=60)
```

---

### Solución Ejercicio 15: Pipeline Completo

```python
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime

def ejecutar_pipeline_completo():
    """Pipeline completo de extracción"""
    reporte = {
        'inicio': datetime.now(),
        'errores': [],
        'registros_por_fuente': {},
        'archivos_generados': []
    }

    try:
        # 1. EXTRACCIÓN
        print("1️⃣ Extracción...")
        df_productos = pd.read_csv('productos.csv')
        reporte['registros_por_fuente']['CSV'] = len(df_productos)

        with open('stock.json', 'r') as f:
            stock_data = json.load(f)
        reporte['registros_por_fuente']['API'] = len(stock_data)

        with open('reviews.html', 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        reviews = soup.find_all('div', class_='producto')
        reporte['registros_por_fuente']['HTML'] = len(reviews)

        # 2. VALIDACIÓN
        print("2️⃣ Validación...")
        if df_productos.isnull().any().any():
            reporte['errores'].append("CSV tiene valores nulos")

        # 3. CONSOLIDACIÓN
        print("3️⃣ Consolidación...")
        # (código de consolidación del ejercicio 11)

        # 4. GUARDADO
        print("4️⃣ Guardado...")
        archivos = ['reporte.csv', 'reporte.json', 'reporte.xlsx']
        reporte['archivos_generados'] = archivos

        # 5. REPORTE
        reporte['fin'] = datetime.now()
        reporte['duracion'] = (reporte['fin'] - reporte['inicio']).total_seconds()

        print("\n" + "="*50)
        print("📊 REPORTE DE EJECUCIÓN")
        print("="*50)
        print(f"Inicio: {reporte['inicio']}")
        print(f"Fin: {reporte['fin']}")
        print(f"Duración: {reporte['duracion']:.2f}s")
        print(f"\nRegistros por fuente:")
        for fuente, cantidad in reporte['registros_por_fuente'].items():
            print(f"  - {fuente}: {cantidad}")
        print(f"\nErrores: {len(reporte['errores'])}")
        print(f"Archivos generados: {len(reporte['archivos_generados'])}")

        return reporte

    except Exception as e:
        reporte['errores'].append(str(e))
        print(f"❌ Error fatal: {e}")
        return reporte

# Ejecutar
reporte = ejecutar_pipeline_completo()
```

---

## 🎯 Criterios de Éxito

Has completado exitosamente los ejercicios si:

- ✅ Resolviste al menos 12 de 15 ejercicios
- ✅ Los ejercicios básicos (1-5) te tomaron <30 min cada uno
- ✅ Los ejercicios intermedios (6-10) te tomaron <60 min cada uno
- ✅ Los ejercicios avanzados (11-15) te tomaron <90 min cada uno
- ✅ Tu código es limpio y reutilizable
- ✅ Implementaste manejo de errores en ejercicios avanzados
- ✅ Usaste logging en al menos 2 ejercicios

---

**¡Felicidades!** Has completado los ejercicios de extracción de datos. Estás listo para el **proyecto práctico TDD** donde construirás un sistema de extracción completo y profesional.

**Próximo paso**: `04-proyecto-practico/` - Sistema de extracción multi-fuente con arquitectura limpia y >85% de cobertura de tests.
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
