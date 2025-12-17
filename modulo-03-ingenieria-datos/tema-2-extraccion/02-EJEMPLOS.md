# Ejemplos Prácticos: Extracción de Datos

Este documento presenta 5 ejemplos trabajados paso a paso que demuestran técnicas de extracción de datos en contextos empresariales reales.

**Empresa ficticia**: **DataFlow Inc.** - Una consultora de Data Engineering que ayuda a sus clientes a extraer y procesar datos de múltiples fuentes.

---

## Ejemplo 1: CSV con Encoding Problemático - Nivel: Básico

### Contexto

DataFlow Inc. recibe un archivo CSV de un cliente europeo (Francia) que contiene información de empleados. El archivo fue exportado desde un sistema antiguo y tiene caracteres especiales (acentos, eñes, cedillas).

Al intentar abrirlo con el encoding por defecto (UTF-8), aparecen caracteres raros o errores de lectura.

### Problema

```python
# ❌ Esto fallará con UnicodeDecodeError o mostrará caracteres raros
import pandas as pd

df = pd.read_csv('empleados_francia.csv')  # Error o caracteres �
```

### Datos de ejemplo

Creemos primero el archivo problemático:

```python
# Crear un CSV con encoding Latin-1 (ISO-8859-1)
datos = """nombre,apellido,ciudad,salario
François,Müller,París,45000
José,García,León,38000
Søren,Andersen,København,52000
Hélène,Dubois,Marseille,41000
"""

# Guardar con encoding Latin-1 (común en sistemas europeos antiguos)
with open('empleados_francia.csv', 'w', encoding='latin-1') as f:
    f.write(datos)

print("✅ Archivo CSV con encoding Latin-1 creado")
```

### Paso 1: Detectar el encoding automáticamente

```python
import chardet

def detectar_encoding(ruta_archivo):
    """Detecta el encoding de un archivo automáticamente"""
    with open(ruta_archivo, 'rb') as archivo:
        contenido = archivo.read()
        resultado = chardet.detect(contenido)

    encoding = resultado['encoding']
    confianza = resultado['confidence']

    print(f"Encoding detectado: {encoding}")
    print(f"Confianza: {confianza * 100:.1f}%")

    return encoding

# Detectar el encoding
encoding_detectado = detectar_encoding('empleados_francia.csv')
```

**Salida esperada**:
```
Encoding detectado: ISO-8859-1
Confianza: 73.0%
```

### Paso 2: Leer el CSV con el encoding correcto

```python
import pandas as pd

# Leer con el encoding detectado
df = pd.read_csv('empleados_francia.csv', encoding=encoding_detectado)

print("\n✅ Datos leídos correctamente:")
print(df)
```

**Salida esperada**:
```
      nombre apellido       ciudad  salario
0   François   Müller        París    45000
1       José  García         León    38000
2      Søren Andersen   København    52000
3     Hélène   Dubois    Marseille    41000
```

### Paso 3: Función reutilizable

```python
def leer_csv_con_encoding_automatico(ruta_archivo, **kwargs):
    """
    Lee un CSV detectando automáticamente el encoding.

    Args:
        ruta_archivo (str): Ruta al archivo CSV
        **kwargs: Argumentos adicionales para pd.read_csv

    Returns:
        pd.DataFrame: Datos del CSV
    """
    # Detectar encoding
    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()
        encoding = chardet.detect(contenido)['encoding']

    # Leer CSV con el encoding detectado
    df = pd.read_csv(ruta_archivo, encoding=encoding, **kwargs)

    return df

# Usar la función
df = leer_csv_con_encoding_automatico(
    'empleados_francia.csv',
    delimiter=',',
    na_values=['', 'NULL']
)

print("\n✅ Función reutilizable funcionando correctamente")
```

### Interpretación

**En el mundo real**:
- El 90% de los problemas con CSV vienen del encoding incorrecto
- `chardet` es tu mejor amigo para detectar encodings automáticamente
- Encodings comunes: UTF-8 (moderno), Latin-1 (Europa), Windows-1252 (Windows antiguo)
- Siempre valida los datos después de leer (verificar que los acentos se ven bien)

**Decisión de negocio**:
- **Estandariza todo a UTF-8**: Convierte todos los CSV a UTF-8 al ingresarlos a tu sistema
- **Documenta el encoding**: Si guardas archivos, documenta qué encoding usaste

---

## Ejemplo 2: JSON Nested con Múltiples Niveles - Nivel: Intermedio

### Contexto

DataFlow Inc. consume una API de un e-commerce que devuelve información de pedidos. El JSON tiene una estructura anidada compleja: cada pedido contiene productos, cada producto tiene detalles, y el cliente tiene dirección anidada.

### Datos de ejemplo

```python
import json

# JSON con estructura nested compleja
pedido_json = {
    "pedido_id": "ORD-2025-001",
    "fecha": "2025-01-15",
    "estado": "entregado",
    "cliente": {
        "id": "CLI-789",
        "nombre": "Ana Martínez",
        "email": "ana@ejemplo.com",
        "direccion": {
            "calle": "Gran Vía 28",
            "ciudad": "Madrid",
            "codigo_postal": "28013",
            "pais": "España"
        }
    },
    "productos": [
        {
            "producto_id": "PROD-101",
            "nombre": "Laptop Dell XPS",
            "cantidad": 1,
            "precio_unitario": 1299.99,
            "descuento": {
                "tipo": "porcentaje",
                "valor": 10
            }
        },
        {
            "producto_id": "PROD-205",
            "nombre": "Mouse Logitech",
            "cantidad": 2,
            "precio_unitario": 29.99,
            "descuento": {
                "tipo": "fijo",
                "valor": 5
            }
        }
    ],
    "totales": {
        "subtotal": 1359.97,
        "descuentos": 135.00,
        "impuestos": 244.79,
        "total": 1469.76
    },
    "metadatos": {
        "canal": "web",
        "dispositivo": "mobile",
        "campana": "cyber_monday"
    }
}

# Guardar como JSON
with open('pedido_complejo.json', 'w', encoding='utf-8') as f:
    json.dump(pedido_json, f, indent=2, ensure_ascii=False)

print("✅ JSON nested creado")
```

### Paso 1: Leer y explorar la estructura

```python
import json

# Leer JSON
with open('pedido_complejo.json', 'r', encoding='utf-8') as f:
    pedido = json.load(f)

# Explorar estructura
print("Claves principales:", list(pedido.keys()))
print("\nCliente:", pedido['cliente']['nombre'])
print("Ciudad:", pedido['cliente']['direccion']['ciudad'])
print("\nNúmero de productos:", len(pedido['productos']))
```

**Salida**:
```
Claves principales: ['pedido_id', 'fecha', 'estado', 'cliente', 'productos', 'totales', 'metadatos']

Cliente: Ana Martínez
Ciudad: Madrid

Número de productos: 2
```

### Paso 2: Aplanar (flatten) el JSON con pandas

```python
import pandas as pd
from pandas import json_normalize

# Normalizar la estructura nested
df_pedido = json_normalize(pedido)

print("\n✅ Estructura aplanada:")
print(df_pedido.columns.tolist())
```

**Salida** (columnas aplanadas):
```
['pedido_id', 'fecha', 'estado',
 'cliente.id', 'cliente.nombre', 'cliente.email',
 'cliente.direccion.calle', 'cliente.direccion.ciudad',
 'cliente.direccion.codigo_postal', 'cliente.direccion.pais',
 'totales.subtotal', 'totales.descuentos', 'totales.impuestos', 'totales.total',
 'metadatos.canal', 'metadatos.dispositivo', 'metadatos.campana']
```

### Paso 3: Extraer productos en tabla separada

```python
# Los productos son una lista, necesitan tabla separada
df_productos = json_normalize(
    pedido,
    record_path=['productos'],  # Ruta a la lista
    meta=['pedido_id', 'fecha'],  # Campos del nivel superior a incluir
    record_prefix='producto_'
)

print("\n✅ Tabla de productos:")
print(df_productos)
```

**Salida**:
```
   producto_producto_id        producto_nombre  producto_cantidad  ...
0           PROD-101      Laptop Dell XPS                 1      ...
1           PROD-205      Mouse Logitech                  2      ...
```

### Paso 4: Calcular precio total con descuento

```python
def calcular_precio_con_descuento(row):
    """Calcula el precio final aplicando descuento"""
    precio = row['producto_precio_unitario']
    cantidad = row['producto_cantidad']
    descuento_tipo = row['producto_descuento.tipo']
    descuento_valor = row['producto_descuento.valor']

    if descuento_tipo == 'porcentaje':
        precio_con_descuento = precio * (1 - descuento_valor / 100)
    else:  # descuento fijo
        precio_con_descuento = precio - descuento_valor

    return precio_con_descuento * cantidad

df_productos['total'] = df_productos.apply(calcular_precio_con_descuento, axis=1)

print("\n✅ Productos con totales calculados:")
print(df_productos[['producto_nombre', 'producto_cantidad', 'producto_precio_unitario', 'total']])
```

**Salida**:
```
         producto_nombre  producto_cantidad  producto_precio_unitario     total
0       Laptop Dell XPS                  1                 1299.99  1169.99
1       Mouse Logitech                   2                   29.99    49.98
```

### Paso 5: Función reutilizable para JSON nested

```python
def procesar_pedido_nested(ruta_json):
    """
    Procesa un JSON nested de pedido y devuelve 2 DataFrames.

    Returns:
        tuple: (df_pedido, df_productos)
    """
    # Leer JSON
    with open(ruta_json, 'r', encoding='utf-8') as f:
        pedido = json.load(f)

    # Aplanar datos del pedido (sin productos)
    pedido_sin_productos = {k: v for k, v in pedido.items() if k != 'productos'}
    df_pedido = json_normalize(pedido_sin_productos)

    # Extraer productos
    df_productos = json_normalize(
        pedido,
        record_path=['productos'],
        meta=['pedido_id'],
        record_prefix='producto_'
    )

    return df_pedido, df_productos

# Usar la función
df_pedido, df_productos = procesar_pedido_nested('pedido_complejo.json')

print("\n✅ Función reutilizable lista")
print(f"Pedido: {df_pedido.shape[0]} registro")
print(f"Productos: {df_productos.shape[0]} registros")
```

### Interpretación

**En el mundo real**:
- Las APIs modernas devuelven JSON nested para representar relaciones
- `json_normalize()` es la herramienta principal para aplanar estructuras
- A menudo necesitarás múltiples tablas (pedidos, productos, clientes) → modelo relacional
- Documenta la estructura JSON que esperas recibir

**Decisión de negocio**:
- **Normaliza los datos**: Separa en tablas relacionadas (pedidos, productos)
- **Valida la estructura**: Verifica que los campos obligatorios existen
- **Maneja cambios en la API**: La estructura puede cambiar, usa try/except

---

## Ejemplo 3: API Paginada con Reintentos Automáticos - Nivel: Intermedio

### Contexto

DataFlow Inc. consume una API de análisis de redes sociales que devuelve tweets. La API está paginada (100 tweets por petición) y a veces falla temporalmente (errores 5xx). Necesitamos extraer 500 tweets con manejo robusto de errores.

### Simulación de API (para testing)

```python
from flask import Flask, jsonify, request
import random
import time

# Esta sección es solo para demostración
# En la realidad, consumirías una API externa

app = Flask(__name__)

@app.route('/api/tweets')
def get_tweets():
    """Simula API paginada con fallas aleatorias"""

    # Simular fallas aleatorias (20% de probabilidad)
    if random.random() < 0.2:
        return jsonify({"error": "Internal Server Error"}), 500

    # Parámetros de paginación
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))

    # Generar tweets ficticios
    tweets = [
        {
            "id": 1000 + offset + i,
            "texto": f"Este es el tweet número {1000 + offset + i}",
            "usuario": f"usuario_{(offset + i) % 50}",
            "likes": random.randint(0, 1000),
            "retweets": random.randint(0, 500),
            "fecha": "2025-01-15"
        }
        for i in range(limit)
    ]

    return jsonify({
        "data": tweets,
        "pagination": {
            "offset": offset,
            "limit": limit,
            "total": 500
        }
    })

# Para ejecutar: python api_simulada.py
# (No ejecutes esto en el ejemplo, es solo para entender)
```

### Paso 1: Función de petición con reintentos

```python
import requests
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hacer_peticion_con_reintentos(url, params=None, max_reintentos=3):
    """
    Hace petición HTTP con reintentos y backoff exponencial.

    Args:
        url (str): URL de la API
        params (dict): Parámetros de la petición
        max_reintentos (int): Número máximo de reintentos

    Returns:
        dict: Respuesta JSON de la API

    Raises:
        Exception: Si falla después de todos los reintentos
    """
    for intento in range(max_reintentos):
        try:
            logger.info(f"Intento {intento + 1} de {max_reintentos}")

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            # Si es exitoso (200-299), devolver
            if 200 <= response.status_code < 300:
                logger.info(f"✅ Petición exitosa: {response.status_code}")
                return response.json()

            # Si es error del cliente (400-499), no reintentar
            if 400 <= response.status_code < 500:
                logger.error(f"❌ Error del cliente: {response.status_code}")
                raise ValueError(f"Error {response.status_code}: {response.text}")

            # Si es error del servidor (500-599), reintentar
            logger.warning(f"⚠️ Error del servidor: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.warning(f"⚠️ Timeout en intento {intento + 1}")

        except requests.exceptions.ConnectionError:
            logger.warning(f"⚠️ Error de conexión en intento {intento + 1}")

        # Backoff exponencial: 1s, 2s, 4s
        if intento < max_reintentos - 1:
            tiempo_espera = 2 ** intento
            logger.info(f"⏳ Esperando {tiempo_espera}s antes del siguiente intento")
            time.sleep(tiempo_espera)

    raise Exception(f"❌ Petición falló después de {max_reintentos} intentos")

# Probar la función (con JSONPlaceholder - API de prueba real)
url_prueba = "https://jsonplaceholder.typicode.com/posts"
resultado = hacer_peticion_con_reintentos(url_prueba, params={"_limit": 5})

print(f"\n✅ Se obtuvieron {len(resultado)} posts de prueba")
```

### Paso 2: Paginación completa

```python
def extraer_todos_los_datos_paginados(url_base, limit_por_pagina=100):
    """
    Extrae todos los datos de una API paginada con reintentos.

    Args:
        url_base (str): URL base de la API
        limit_por_pagina (int): Registros por página

    Returns:
        list: Todos los datos extraídos
    """
    todos_los_datos = []
    offset = 0

    logger.info(f"🚀 Iniciando extracción paginada desde {url_base}")

    while True:
        # Preparar parámetros de paginación
        params = {
            'offset': offset,
            'limit': limit_por_pagina
        }

        # Hacer petición con reintentos
        try:
            respuesta = hacer_peticion_con_reintentos(
                url_base,
                params=params,
                max_reintentos=3
            )

            # Extraer datos
            # (La estructura varía según la API, ajustar según necesidad)
            if isinstance(respuesta, list):
                datos_pagina = respuesta
            elif isinstance(respuesta, dict) and 'data' in respuesta:
                datos_pagina = respuesta['data']
            else:
                datos_pagina = []

            # Si no hay datos, terminar
            if not datos_pagina or len(datos_pagina) == 0:
                logger.info("✅ No hay más datos, paginación completa")
                break

            # Agregar a la lista total
            todos_los_datos.extend(datos_pagina)
            logger.info(f"📦 Extraídos {len(datos_pagina)} registros (total: {len(todos_los_datos)})")

            # Avanzar a la siguiente página
            offset += limit_por_pagina

            # Rate limiting: esperar 1 segundo entre peticiones
            time.sleep(1)

        except Exception as e:
            logger.error(f"❌ Error fatal en offset {offset}: {str(e)}")
            break

    logger.info(f"🎉 Extracción completada: {len(todos_los_datos)} registros totales")
    return todos_los_datos

# Ejemplo con JSONPlaceholder (API pública)
datos = extraer_todos_los_datos_paginados(
    'https://jsonplaceholder.typicode.com/posts',
    limit_por_pagina=10
)

print(f"\n✅ Total extraído: {len(datos)} posts")
```

**Salida esperada**:
```
INFO:__main__:🚀 Iniciando extracción paginada desde https://jsonplaceholder.typicode.com/posts
INFO:__main__:Intento 1 de 3
INFO:__main__:✅ Petición exitosa: 200
INFO:__main__:📦 Extraídos 10 registros (total: 10)
...
INFO:__main__:🎉 Extracción completada: 100 registros totales

✅ Total extraído: 100 posts
```

### Paso 3: Guardar los datos extraídos

```python
import pandas as pd
from datetime import datetime

# Convertir a DataFrame
df = pd.DataFrame(datos)

# Agregar metadatos de extracción
df['fecha_extraccion'] = datetime.now()

# Guardar en múltiples formatos
df.to_csv('tweets_extraidos.csv', index=False, encoding='utf-8')
df.to_json('tweets_extraidos.json', orient='records', lines=True)  # JSON Lines

print(f"\n✅ Datos guardados:")
print(f"   - tweets_extraidos.csv")
print(f"   - tweets_extraidos.json")
print(f"\nPrimeras filas:")
print(df.head())
```

### Interpretación

**En el mundo real**:
- Las APIs fallan temporalmente (mantenimiento, sobrecarga, problemas de red)
- Los reintentos con backoff exponencial son esenciales
- **Backoff exponencial**: Esperar 1s, 2s, 4s, 8s... entre reintentos (no saturar más)
- Rate limiting: 1-2 segundos entre peticiones normales
- Logging: Fundamental para debuggear problemas en producción

**Decisiones de negocio**:
- **Máximo de reintentos**: 3 es razonable (más de 5 puede indicar un problema mayor)
- **Guardar progreso**: Si extraes millones de registros, guarda checkpoints cada N páginas
- **Alertas**: Si la API falla > 50% del tiempo, alertar al equipo

---

## Ejemplo 4: Scraping Básico con Beautiful Soup - Nivel: Básico

### Contexto

DataFlow Inc. necesita extraer información de productos de un catálogo web que no tiene API. El cliente quiere saber precios y disponibilidad de productos tecnológicos.

**Importante**: Este ejemplo usa un HTML de prueba local. En producción, SIEMPRE verifica `robots.txt` y términos de servicio antes de scrapear.

### Paso 1: Crear página HTML de prueba

```python
html_prueba = """
<!DOCTYPE html>
<html>
<head>
    <title>Catálogo de Productos</title>
</head>
<body>
    <h1>Productos Tecnológicos</h1>

    <div class="producto" id="prod-1">
        <h2 class="nombre">Laptop Dell XPS 15</h2>
        <p class="descripcion">Laptop profesional con pantalla 4K</p>
        <span class="precio">1299.99€</span>
        <span class="disponibilidad">En stock</span>
        <a href="/productos/dell-xps-15" class="link">Ver detalles</a>
    </div>

    <div class="producto" id="prod-2">
        <h2 class="nombre">iPhone 15 Pro</h2>
        <p class="descripcion">Smartphone premium con chip A17</p>
        <span class="precio">1199.00€</span>
        <span class="disponibilidad">Agotado</span>
        <a href="/productos/iphone-15-pro" class="link">Ver detalles</a>
    </div>

    <div class="producto" id="prod-3">
        <h2 class="nombre">Monitor LG UltraWide</h2>
        <p class="descripcion">Monitor 34" curvo para productividad</p>
        <span class="precio">599.99€</span>
        <span class="disponibilidad">En stock</span>
        <a href="/productos/lg-ultrawide" class="link">Ver detalles</a>
    </div>

    <table class="especificaciones">
        <tr>
            <th>Categoría</th>
            <th>Productos</th>
            <th>Precio Promedio</th>
        </tr>
        <tr>
            <td>Laptops</td>
            <td>15</td>
            <td>899€</td>
        </tr>
        <tr>
            <td>Smartphones</td>
            <td>23</td>
            <td>649€</td>
        </tr>
    </table>
</body>
</html>
"""

# Guardar HTML de prueba
with open('catalogo_prueba.html', 'w', encoding='utf-8') as f:
    f.write(html_prueba)

print("✅ HTML de prueba creado")
```

### Paso 2: Parsear HTML con Beautiful Soup

```python
from bs4 import BeautifulSoup

# Leer HTML
with open('catalogo_prueba.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Parsear con Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Verificar que cargó correctamente
titulo = soup.find('h1').text
print(f"\n📄 Título de la página: {titulo}")
```

**Salida**:
```
📄 Título de la página: Productos Tecnológicos
```

### Paso 3: Extraer productos

```python
# Buscar todos los productos
productos_html = soup.find_all('div', class_='producto')

print(f"\n🔍 Se encontraron {len(productos_html)} productos")

productos_extraidos = []

for producto in productos_html:
    # Extraer información de cada producto
    nombre = producto.find('h2', class_='nombre').text.strip()
    descripcion = producto.find('p', class_='descripcion').text.strip()
    precio_texto = producto.find('span', class_='precio').text.strip()
    disponibilidad = producto.find('span', class_='disponibilidad').text.strip()
    link = producto.find('a', class_='link')['href']

    # Limpiar precio (quitar € y convertir a float)
    precio = float(precio_texto.replace('€', '').replace(',', '.'))

    # Crear diccionario
    producto_dict = {
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': precio,
        'disponibilidad': disponibilidad,
        'link': link
    }

    productos_extraidos.append(producto_dict)

    print(f"\n  ✅ {nombre}")
    print(f"     Precio: {precio}€")
    print(f"     Stock: {disponibilidad}")
```

**Salida**:
```
🔍 Se encontraron 3 productos

  ✅ Laptop Dell XPS 15
     Precio: 1299.99€
     Stock: En stock

  ✅ iPhone 15 Pro
     Precio: 1199.0€
     Stock: Agotado

  ✅ Monitor LG UltraWide
     Precio: 599.99€
     Stock: En stock
```

### Paso 4: Extraer tabla de especificaciones

```python
import pandas as pd

# Buscar tabla
tabla = soup.find('table', class_='especificaciones')

# Extraer con pandas (método fácil)
df_tabla = pd.read_html(str(tabla))[0]

print("\n📊 Tabla de especificaciones:")
print(df_tabla)
```

**Salida**:
```
📊 Tabla de especificaciones:
    Categoría  Productos Precio Promedio
0     Laptops         15             899€
1  Smartphones         23             649€
```

### Paso 5: Guardar datos scrapeados

```python
import pandas as pd
from datetime import datetime

# Convertir a DataFrame
df_productos = pd.DataFrame(productos_extraidos)

# Agregar metadatos
df_productos['fecha_scraping'] = datetime.now()
df_productos['fuente'] = 'catalogo_prueba.html'

# Filtrar solo productos disponibles
df_disponibles = df_productos[df_productos['disponibilidad'] == 'En stock']

print(f"\n✅ Productos disponibles: {len(df_disponibles)}")
print(df_disponibles[['nombre', 'precio']])

# Guardar
df_productos.to_csv('productos_scrapeados.csv', index=False)
print("\n💾 Datos guardados en productos_scrapeados.csv")
```

### Paso 6: Función reutilizable

```python
def scrapear_catalogo(ruta_html_o_url):
    """
    Scrapea productos de un catálogo HTML.

    Args:
        ruta_html_o_url (str): Ruta local o URL

    Returns:
        pd.DataFrame: Productos extraídos
    """
    from bs4 import BeautifulSoup
    import requests

    # Si es URL, hacer petición
    if ruta_html_o_url.startswith('http'):
        headers = {
            'User-Agent': 'DataFlowBot/1.0 (contacto@dataflow.com)'
        }
        response = requests.get(ruta_html_o_url, headers=headers)
        html = response.text
    else:
        # Si es archivo local
        with open(ruta_html_o_url, 'r', encoding='utf-8') as f:
            html = f.read()

    # Parsear
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer productos
    productos = []
    for producto in soup.find_all('div', class_='producto'):
        productos.append({
            'nombre': producto.find('h2', class_='nombre').text.strip(),
            'precio': float(producto.find('span', class_='precio').text.strip().replace('€', '').replace(',', '.')),
            'disponibilidad': producto.find('span', class_='disponibilidad').text.strip()
        })

    return pd.DataFrame(productos)

# Usar la función
df = scrapear_catalogo('catalogo_prueba.html')
print("\n✅ Función reutilizable lista")
print(f"Productos extraídos: {len(df)}")
```

### Interpretación

**En el mundo real**:
- **Siempre verifica `robots.txt`** antes de scrapear
- **User-Agent identificable**: No te hagas pasar por un navegador
- **Rate limiting**: 1-2 segundos entre peticiones mínimo
- **Estructura puede cambiar**: El HTML puede cambiar en cualquier momento, tu script se rompe
- **APIs son mejores**: Si existe una API, úsala en lugar de scraping

**Decisiones de negocio**:
- **Monitorear cambios**: Alerta si la estructura HTML cambia
- **Scraping periódico**: No scrapees en tiempo real, hazlo 1-2 veces al día
- **Contactar al dueño**: Si scrapeas mucho, contacta y pide una API o permiso

---

## Ejemplo 5: Extracción Multi-Fuente (CSV + API + Web) - Nivel: Avanzado

### Contexto

DataFlow Inc. trabaja en un proyecto de análisis de competencia para un cliente de e-commerce. Necesitan combinar datos de 3 fuentes:

1. **CSV local**: Lista de productos del cliente
2. **API externa**: Precios de competidores
3. **Web scraping**: Reviews de productos

### Paso 1: Preparar datos de ejemplo

```python
import pandas as pd
import json

# 1. CSV de productos del cliente
productos_cliente = """sku,nombre,categoria,precio_cliente
PROD-001,Laptop Gaming ASUS,Laptops,1499.99
PROD-002,Mouse Logitech MX,Accesorios,79.99
PROD-003,Teclado Mecánico,Accesorios,149.99
"""

with open('productos_cliente.csv', 'w', encoding='utf-8') as f:
    f.write(productos_cliente)

print("✅ CSV de productos del cliente creado")

# 2. Simular API de precios de competencia (en realidad usaremos un JSON local)
precios_competencia = {
    "PROD-001": {"competidor": "CompetidorA", "precio": 1399.99},
    "PROD-002": {"competidor": "CompetidorB", "precio": 69.99},
    "PROD-003": {"competidor": "CompetidorA", "precio": 139.99}
}

with open('precios_api.json', 'w', encoding='utf-8') as f:
    json.dump(precios_competencia, f, indent=2)

print("✅ JSON de precios de competencia creado")

# 3. HTML con reviews (simulado)
html_reviews = """
<!DOCTYPE html>
<html>
<body>
    <div class="review" data-sku="PROD-001">
        <span class="rating">4.5</span>
        <span class="num-reviews">128</span>
    </div>
    <div class="review" data-sku="PROD-002">
        <span class="rating">4.8</span>
        <span class="num-reviews">342</span>
    </div>
    <div class="review" data-sku="PROD-003">
        <span class="rating">4.2</span>
        <span class="num-reviews">89</span>
    </div>
</body>
</html>
"""

with open('reviews.html', 'w', encoding='utf-8') as f:
    f.write(html_reviews)

print("✅ HTML de reviews creado")
```

### Paso 2: Extraer de cada fuente

```python
import pandas as pd
import json
from bs4 import BeautifulSoup

# FUENTE 1: CSV
df_productos = pd.read_csv('productos_cliente.csv')
print(f"\n1️⃣ CSV cargado: {len(df_productos)} productos")

# FUENTE 2: API (simulada con JSON)
with open('precios_api.json', 'r') as f:
    precios_api = json.load(f)

# Convertir a DataFrame
df_precios = pd.DataFrame([
    {'sku': sku, 'precio_competencia': info['precio'], 'competidor': info['competidor']}
    for sku, info in precios_api.items()
])
print(f"2️⃣ API consumida: {len(df_precios)} precios")

# FUENTE 3: Web scraping
with open('reviews.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

reviews_data = []
for review_div in soup.find_all('div', class_='review'):
    reviews_data.append({
        'sku': review_div['data-sku'],
        'rating': float(review_div.find('span', class_='rating').text),
        'num_reviews': int(review_div.find('span', class_='num-reviews').text)
    })

df_reviews = pd.DataFrame(reviews_data)
print(f"3️⃣ Scraping completado: {len(df_reviews)} reviews")
```

**Salida**:
```
1️⃣ CSV cargado: 3 productos
2️⃣ API consumida: 3 precios
3️⃣ Scraping completado: 3 reviews
```

### Paso 3: Consolidar todas las fuentes

```python
# Combinar todas las fuentes usando SKU como clave
df_consolidado = df_productos.copy()

# Merge con precios de competencia
df_consolidado = df_consolidado.merge(
    df_precios,
    on='sku',
    how='left'
)

# Merge con reviews
df_consolidado = df_consolidado.merge(
    df_reviews,
    on='sku',
    how='left'
)

print("\n📊 Datos consolidados:")
print(df_consolidado)
```

**Salida**:
```
📊 Datos consolidados:
        sku                  nombre   categoria  precio_cliente  precio_competencia    competidor  rating  num_reviews
0  PROD-001     Laptop Gaming ASUS     Laptops         1499.99             1399.99  CompetidorA    4.5          128
1  PROD-002      Mouse Logitech MX  Accesorios           79.99               69.99  CompetidorB    4.8          342
2  PROD-003      Teclado Mecánico  Accesorios          149.99              139.99  CompetidorA    4.2           89
```

### Paso 4: Calcular KPIs y análisis

```python
# Calcular diferencia de precio
df_consolidado['diferencia_precio'] = df_consolidado['precio_cliente'] - df_consolidado['precio_competencia']
df_consolidado['diferencia_porcentual'] = (df_consolidado['diferencia_precio'] / df_consolidado['precio_competencia'] * 100).round(2)

# Clasificar competitividad
def clasificar_competitividad(row):
    if row['diferencia_porcentual'] < -5:
        return 'Muy competitivo'
    elif row['diferencia_porcentual'] < 5:
        return 'Competitivo'
    else:
        return 'Caro'

df_consolidado['competitividad'] = df_consolidado.apply(clasificar_competitividad, axis=1)

# Agregar score combinado (precio + rating)
df_consolidado['score'] = (
    df_consolidado['rating'] / 5 * 50 +  # Rating pesa 50%
    (100 - df_consolidado['diferencia_porcentual'].abs()) / 100 * 50  # Competitividad pesa 50%
).round(2)

print("\n📈 Análisis completo:")
print(df_consolidado[['nombre', 'diferencia_porcentual', 'rating', 'competitividad', 'score']])
```

**Salida**:
```
📈 Análisis completo:
                  nombre  diferencia_porcentual  rating  competitividad  score
0    Laptop Gaming ASUS                   7.14     4.5            Caro  41.43
1     Mouse Logitech MX                  14.29     4.8            Caro  40.71
2     Teclado Mecánico                   7.14     4.2  Competitivo  41.43
```

### Paso 5: Generar reporte final

```python
from datetime import datetime

# Agregar metadatos
df_consolidado['fecha_analisis'] = datetime.now()
df_consolidado['fuentes'] = 'CSV + API + Scraping'

# Guardar reporte
df_consolidado.to_csv('reporte_competencia.csv', index=False)
df_consolidado.to_excel('reporte_competencia.xlsx', index=False)

print("\n✅ Reporte generado:")
print("   - reporte_competencia.csv")
print("   - reporte_competencia.xlsx")

# Resumen ejecutivo
print("\n📊 RESUMEN EJECUTIVO:")
print(f"Total de productos analizados: {len(df_consolidado)}")
print(f"Productos competitivos: {(df_consolidado['competitividad'] == 'Competitivo').sum()}")
print(f"Productos caros: {(df_consolidado['competitividad'] == 'Caro').sum()}")
print(f"Rating promedio: {df_consolidado['rating'].mean():.2f}")
print(f"Diferencia de precio promedio: {df_consolidado['diferencia_porcentual'].mean():.2f}%")
```

**Salida**:
```
✅ Reporte generado:
   - reporte_competencia.csv
   - reporte_competencia.xlsx

📊 RESUMEN EJECUTIVO:
Total de productos analizados: 3
Productos competitivos: 1
Productos caros: 2
Rating promedio: 4.50
Diferencia de precio promedio: 9.52%
```

### Interpretación

**En el mundo real**:
- Combinar múltiples fuentes es MUY común en Data Engineering
- Cada fuente tiene su propia frecuencia de actualización (CSV diario, API cada hora, scraping semanal)
- La clave (SKU, ID, etc.) debe ser consistente entre fuentes
- Los datos pueden no coincidir perfectamente (usar `how='left'` o `how='outer'` según necesidad)

**Decisiones de negocio**:
- **Priorizar fuentes**: Si hay conflicto, ¿qué fuente es la verdad?
- **Alertas**: Si la diferencia de precio es > 20%, alertar al equipo de pricing
- **Automatización**: Este pipeline debería ejecutarse automáticamente (Airflow, cron)
- **Calidad de datos**: Validar que todas las fuentes se actualizaron correctamente

---

## Resumen de los 5 Ejemplos

| Ejemplo | Nivel | Fuente | Concepto clave |
|---------|-------|--------|----------------|
| 1 | Básico | CSV | Encoding automático |
| 2 | Intermedio | JSON | Aplanar estructuras nested |
| 3 | Intermedio | API | Paginación + reintentos |
| 4 | Básico | Web | Scraping ético con Beautiful Soup |
| 5 | Avanzado | Multi-fuente | Consolidación de datos |

**Próximo paso**: `03-EJERCICIOS.md` donde pondrás en práctica estos conceptos con 15 ejercicios.

---

**¡Excelente trabajo!** Ya dominas los patrones fundamentales de extracción de datos. Ahora es tu turno de practicar.
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
