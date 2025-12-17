# Tema 2: Procesamiento de Archivos CSV

## 📚 ¿Qué Aprenderás en Este Tema?

Al finalizar este tema serás capaz de:
- ✅ Entender qué es un archivo CSV y por qué es el formato más usado en Data Engineering
- ✅ Leer y escribir archivos CSV con Python de forma robusta
- ✅ Manejar problemas comunes: encoding, delimitadores, comillas, archivos vacíos
- ✅ Validar datos antes de procesarlos
- ✅ Transformar datos CSV de forma segura y eficiente
- ✅ Aplicar buenas prácticas en producción

**Duración estimada:** 1-2 semanas
**Nivel:** Principiante (requiere conocimientos básicos de Python)

---

## 🎯 ¿Por Qué CSV en Data Engineering?

### El Formato Universal de Datos

Imagina que trabajas en **DataFlow Industries** (tu empresa de Data Engineering) y tu primer cliente es **RestaurantData Co.**, una cadena de restaurantes.

Ellos te envían sus datos de ventas diarias. ¿En qué formato crees que vienen?

**¡CSV!** (Comma-Separated Values)

### ¿Por qué CSV es tan popular?

1. **Universal**: Cualquier sistema puede leerlo (Excel, Python, R, bases de datos, etc.)
2. **Simple**: Es solo texto plano, fácil de entender
3. **Ligero**: Ocupa poco espacio comparado con otros formatos
4. **Compatible**: Funciona en cualquier sistema operativo (Windows, Linux, Mac)

### Ejemplo Real: Tu Primer Día

Te llega este email:

```
De: cliente@restaurantdata.co
Para: tu@dataflow.com
Asunto: Datos de ventas - Octubre 2025

Hola,

Adjunto el archivo ventas_octubre.csv con nuestras ventas del mes.
¿Puedes analizarlo?

Gracias
```

Abres el archivo y ves esto:

```csv
fecha,local,producto,cantidad,precio_unitario,total
2025-10-01,Madrid Centro,Pizza Margarita,3,12.50,37.50
2025-10-01,Madrid Centro,Coca-Cola,3,2.50,7.50
2025-10-01,Barcelona Norte,Pasta Carbonara,2,14.00,28.00
```

**Pregunta**: ¿Cómo procesas esto con Python? ¿Qué problemas pueden surgir?

**Respuesta**: ¡Eso es exactamente lo que aprenderás en este tema!

---

## 📊 Parte 1: ¿Qué es un Archivo CSV?

### 1.1 Definición Simple

Un **archivo CSV** (Comma-Separated Values) es un archivo de texto plano donde:
- Cada **línea** es una **fila** de datos
- Los **valores** de cada fila están separados por **comas** (u otro delimitador)
- La **primera línea** suele contener los **nombres de las columnas** (headers)

### 1.2 Analogía: La Tabla de Excel

Piensa en una tabla de Excel:

| Nombre | Edad | Ciudad |
|--------|------|--------|
| Ana    | 25   | Madrid |
| Luis   | 30   | Barcelona |
| María  | 28   | Valencia |

En formato CSV, esto se ve así:

```csv
Nombre,Edad,Ciudad
Ana,25,Madrid
Luis,30,Barcelona
María,28,Valencia
```

**¿Ves el patrón?**
- Primera línea: `Nombre,Edad,Ciudad` → Headers (nombres de columnas)
- Segunda línea: `Ana,25,Madrid` → Primera fila de datos
- Tercera línea: `Luis,30,Barcelona` → Segunda fila de datos
- Y así sucesivamente...

### 1.3 Estructura de un CSV

```
header1,header2,header3
valor1,valor2,valor3
valor4,valor5,valor6
```

**Componentes**:
1. **Headers** (opcional pero recomendado): Primera fila con nombres de columnas
2. **Filas de datos**: Cada línea es un registro
3. **Delimitador**: Carácter que separa valores (usualmente `,`)
4. **Saltos de línea**: Separan filas (usualmente `\n` o `\r\n`)

### 1.4 Ejemplo Paso a Paso

Vamos a crear un CSV desde cero para entenderlo mejor.

**Paso 1**: Decide qué datos quieres guardar

```
Quiero guardar información de productos:
- Nombre del producto
- Precio
- Stock disponible
```

**Paso 2**: Crea los headers

```csv
producto,precio,stock
```

**Paso 3**: Añade los datos

```csv
producto,precio,stock
Laptop,899.99,15
Mouse,19.99,50
Teclado,49.99,30
```

**¡Listo!** Ya tienes un archivo CSV válido.

---

## 📝 Parte 2: Delimitadores y Formatos

### 2.1 ¿Qué es un Delimitador?

El **delimitador** es el carácter que separa los valores en cada fila.

**Analogía**: Imagina que estás leyendo una lista de compras:

```
Manzanas, Peras, Naranjas, Plátanos
```

La **coma** (`,`) es el delimitador que te dice dónde termina un producto y empieza otro.

### 2.2 Delimitadores Comunes

| Delimitador | Nombre | Ejemplo | Cuándo Usarlo |
|-------------|--------|---------|---------------|
| `,` | Coma | `Ana,25,Madrid` | Estándar internacional |
| `;` | Punto y coma | `Ana;25;Madrid` | Europa (Excel español) |
| `\t` | Tabulador (Tab) | `Ana    25    Madrid` | TSV (Tab-Separated Values) |
| `|` | Pipe | `Ana|25|Madrid` | Cuando los datos tienen comas |

### 2.3 Problema: ¿Qué pasa si los datos tienen comas?

Imagina este CSV:

```csv
nombre,ciudad,descripcion
Ana,Madrid,Le gusta la pizza, la pasta y el helado
```

**¿Cuántas columnas tiene?**
- Esperamos: 3 columnas (nombre, ciudad, descripcion)
- Realidad: ¡5 columnas! (porque hay comas en la descripción)

**Solución 1**: Usar comillas

```csv
nombre,ciudad,descripcion
Ana,Madrid,"Le gusta la pizza, la pasta y el helado"
```

Ahora Python sabe que todo lo que está entre comillas es un solo valor.

**Solución 2**: Cambiar el delimitador

```csv
nombre;ciudad;descripcion
Ana;Madrid;Le gusta la pizza, la pasta y el helado
```

Usamos `;` en lugar de `,` para evitar confusiones.

### 2.4 Ejemplo Real: CSV Europeo vs Americano

**CSV Americano** (delimitador: `,`):
```csv
producto,precio,stock
Laptop,899.99,15
```

**CSV Europeo** (delimitador: `;`, decimales con `,`):
```csv
producto;precio;stock
Laptop;899,99;15
```

**¿Por qué la diferencia?**
- En Europa se usa `,` para decimales (899,99€)
- Por eso Excel europeo usa `;` como delimitador

**En Data Engineering**: Debes estar preparado para ambos formatos.

---

## 🔤 Parte 3: Encoding (Codificación de Caracteres)

### 3.1 ¿Qué es el Encoding?

El **encoding** (codificación) es cómo se representan los caracteres en el archivo.

**Analogía**: Imagina que el encoding es el "idioma" en el que está escrito el archivo.

- **UTF-8**: El "esperanto" de los encodings (universal, recomendado)
- **Latin-1 (ISO-8859-1)**: Común en Europa occidental
- **Windows-1252**: Usado por Excel en Windows
- **ASCII**: Solo caracteres básicos (sin tildes, sin ñ)

### 3.2 Problema: Caracteres Especiales

Tienes este CSV:

```csv
nombre,ciudad
José,Málaga
María,León
```

Si lo abres con el encoding incorrecto, verás:

```
JosÃ©,MÃ¡laga
MarÃ­a,LeÃ³n
```

**¿Por qué?** Porque el archivo está en UTF-8 pero lo abriste como Latin-1 (o viceversa).

### 3.3 Encodings Comunes en Data Engineering

| Encoding | Uso | Caracteres Soportados | Recomendación |
|----------|-----|----------------------|---------------|
| **UTF-8** | Universal | Todos (emojis incluidos 🎉) | ✅ Usa siempre que puedas |
| Latin-1 | Europa occidental | Tildes, ñ, ç | ⚠️ Solo si es necesario |
| ASCII | Sistemas antiguos | Solo a-z, A-Z, 0-9 | ❌ Evitar (muy limitado) |
| Windows-1252 | Excel Windows | Similar a Latin-1 | ⚠️ Común en archivos de Excel |

### 3.4 Ejemplo Práctico

```python
# ❌ MAL: Asume encoding por defecto
with open('datos.csv', 'r') as archivo:
    contenido = archivo.read()  # Puede fallar con tildes

# ✅ BIEN: Especifica encoding explícitamente
with open('datos.csv', 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()  # Funciona con tildes, ñ, etc.
```

**Regla de oro**: Siempre especifica `encoding='utf-8'` al abrir archivos.

---

## 🛡️ Parte 4: Manejo de Errores Comunes

### 4.1 Archivo Vacío

**Problema**: El archivo existe pero está vacío (0 bytes).

```python
# ❌ Esto puede fallar
import csv
with open('datos.csv', 'r') as archivo:
    lector = csv.reader(archivo)
    headers = next(lector)  # Error si el archivo está vacío
```

**Solución**: Validar antes de procesar

```python
# ✅ Validación robusta
import os

if not os.path.exists('datos.csv'):
    raise FileNotFoundError("El archivo no existe")

if os.path.getsize('datos.csv') == 0:
    raise ValueError("El archivo está vacío")

# Ahora sí, procesar...
```

### 4.2 Delimitador Incorrecto

**Problema**: Intentas leer un CSV con `;` pero usas `,` como delimitador.

```csv
nombre;edad;ciudad
Ana;25;Madrid
```

```python
# ❌ Usa delimitador incorrecto
import csv
with open('datos.csv', 'r') as archivo:
    lector = csv.reader(archivo, delimiter=',')  # ¡Mal!
    for fila in lector:
        print(fila)  # ['nombre;edad;ciudad'] ← Todo en una sola columna
```

**Solución**: Detectar el delimitador automáticamente

```python
# ✅ Detecta el delimitador
import csv

with open('datos.csv', 'r') as archivo:
    muestra = archivo.read(1024)  # Lee los primeros 1024 caracteres
    archivo.seek(0)  # Vuelve al inicio

    sniffer = csv.Sniffer()
    delimitador = sniffer.sniff(muestra).delimiter

    lector = csv.reader(archivo, delimiter=delimitador)
    for fila in lector:
        print(fila)  # ['Ana', '25', 'Madrid'] ← ¡Correcto!
```

### 4.3 Filas con Diferente Número de Columnas

**Problema**: Algunas filas tienen más o menos columnas que otras.

```csv
nombre,edad,ciudad
Ana,25,Madrid
Luis,30  ← Falta la ciudad
María,28,Valencia,España  ← Columna extra
```

**Solución**: Validar y manejar inconsistencias

```python
# ✅ Validación de columnas
import csv

with open('datos.csv', 'r') as archivo:
    lector = csv.reader(archivo)
    headers = next(lector)
    num_columnas_esperadas = len(headers)

    for num_fila, fila in enumerate(lector, start=2):
        if len(fila) != num_columnas_esperadas:
            print(f"⚠️ Fila {num_fila}: Esperaba {num_columnas_esperadas} columnas, encontré {len(fila)}")
            # Decidir: ¿Saltar fila? ¿Rellenar con None? ¿Lanzar error?
```

### 4.4 Valores Nulos o Vacíos

**Problema**: Algunos valores están vacíos.

```csv
nombre,edad,ciudad
Ana,25,Madrid
Luis,,Barcelona  ← Edad vacía
María,28,  ← Ciudad vacía
```

**Solución**: Decidir cómo manejar valores vacíos

```python
# ✅ Manejo de valores vacíos
import csv

with open('datos.csv', 'r') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        # Opción 1: Reemplazar vacíos con None
        edad = fila['edad'] if fila['edad'] else None

        # Opción 2: Reemplazar vacíos con valor por defecto
        ciudad = fila['ciudad'] if fila['ciudad'] else 'Desconocida'

        print(f"{fila['nombre']}: {edad} años, {ciudad}")
```

---

## 📖 Parte 5: Lectura de CSV con Python

### 5.1 Método 1: Módulo `csv` (Estándar)

El módulo `csv` viene incluido con Python (no necesitas instalarlo).

**Lectura básica**:

```python
import csv

# Abrir y leer CSV
with open('datos.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.reader(archivo)

    # Leer headers
    headers = next(lector)
    print(f"Columnas: {headers}")

    # Leer filas
    for fila in lector:
        print(fila)  # fila es una lista: ['Ana', '25', 'Madrid']
```

**Lectura con DictReader** (más conveniente):

```python
import csv

with open('datos.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        print(fila)  # fila es un diccionario: {'nombre': 'Ana', 'edad': '25', 'ciudad': 'Madrid'}
        print(f"{fila['nombre']} tiene {fila['edad']} años")
```

**Ventajas de DictReader**:
- Acceso por nombre de columna (más legible)
- No necesitas recordar el índice de cada columna
- Código más mantenible

### 5.2 Método 2: Pandas (Para Análisis de Datos)

Si vas a hacer análisis de datos, usa `pandas` (necesitas instalarlo: `pip install pandas`).

```python
import pandas as pd

# Leer CSV
df = pd.read_csv('datos.csv', encoding='utf-8')

# Ver primeras filas
print(df.head())

# Acceder a columnas
print(df['nombre'])

# Filtrar datos
mayores_25 = df[df['edad'] > 25]
```

**Cuándo usar cada uno**:
- **`csv`**: Para procesamiento simple, archivos grandes, bajo uso de memoria
- **`pandas`**: Para análisis, transformaciones complejas, estadísticas

---

## ✍️ Parte 6: Escritura de CSV con Python

### 6.1 Escritura Básica

```python
import csv

# Datos a escribir
datos = [
    ['nombre', 'edad', 'ciudad'],  # Headers
    ['Ana', 25, 'Madrid'],
    ['Luis', 30, 'Barcelona'],
    ['María', 28, 'Valencia']
]

# Escribir CSV
with open('salida.csv', 'w', encoding='utf-8', newline='') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerows(datos)  # Escribe todas las filas de una vez
```

**Nota**: `newline=''` es importante en Windows para evitar líneas en blanco extra.

### 6.2 Escritura con DictWriter

```python
import csv

# Datos como diccionarios
datos = [
    {'nombre': 'Ana', 'edad': 25, 'ciudad': 'Madrid'},
    {'nombre': 'Luis', 'edad': 30, 'ciudad': 'Barcelona'},
    {'nombre': 'María', 'edad': 28, 'ciudad': 'Valencia'}
]

# Escribir CSV
with open('salida.csv', 'w', encoding='utf-8', newline='') as archivo:
    headers = ['nombre', 'edad', 'ciudad']
    escritor = csv.DictWriter(archivo, fieldnames=headers)

    escritor.writeheader()  # Escribe los headers
    escritor.writerows(datos)  # Escribe las filas
```

### 6.3 Escritura con Pandas

```python
import pandas as pd

# Crear DataFrame
df = pd.DataFrame({
    'nombre': ['Ana', 'Luis', 'María'],
    'edad': [25, 30, 28],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia']
})

# Escribir CSV
df.to_csv('salida.csv', index=False, encoding='utf-8')
```

**Nota**: `index=False` evita que se escriba la columna de índice.

---

## 🔍 Parte 7: Validación de Datos CSV

### 7.1 ¿Por Qué Validar?

En Data Engineering, **nunca confíes en los datos de entrada**. Siempre pueden venir:
- Archivos corruptos
- Datos faltantes
- Formatos incorrectos
- Valores fuera de rango

**Regla de oro**: Validar antes de procesar.

### 7.2 Validaciones Comunes

#### 1. Validar que el archivo existe y no está vacío

```python
import os

def validar_archivo_csv(ruta_archivo: str) -> None:
    """
    Valida que el archivo CSV existe y no está vacío.

    Args:
        ruta_archivo: Ruta al archivo CSV

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    if os.path.getsize(ruta_archivo) == 0:
        raise ValueError(f"El archivo está vacío: {ruta_archivo}")
```

#### 2. Validar headers esperados

```python
import csv

def validar_headers(ruta_archivo: str, headers_esperados: list) -> None:
    """
    Valida que el CSV tiene los headers esperados.

    Args:
        ruta_archivo: Ruta al archivo CSV
        headers_esperados: Lista de headers que debe tener el archivo

    Raises:
        ValueError: Si los headers no coinciden
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        headers = next(lector)

        if headers != headers_esperados:
            raise ValueError(
                f"Headers incorrectos.\n"
                f"Esperados: {headers_esperados}\n"
                f"Encontrados: {headers}"
            )
```

#### 3. Validar tipos de datos

```python
def validar_fila(fila: dict, validaciones: dict) -> list:
    """
    Valida que los valores de una fila cumplen con los tipos esperados.

    Args:
        fila: Diccionario con los datos de la fila
        validaciones: Diccionario {columna: tipo_esperado}

    Returns:
        Lista de errores encontrados (vacía si todo está bien)
    """
    errores = []

    for columna, tipo_esperado in validaciones.items():
        valor = fila.get(columna, '')

        if not valor:  # Valor vacío
            errores.append(f"Columna '{columna}' está vacía")
            continue

        try:
            if tipo_esperado == int:
                int(valor)
            elif tipo_esperado == float:
                float(valor)
            # Añadir más validaciones según necesites
        except ValueError:
            errores.append(f"Columna '{columna}': esperaba {tipo_esperado.__name__}, encontré '{valor}'")

    return errores
```

### 7.3 Ejemplo Completo de Validación

```python
import csv
import os

def procesar_csv_con_validacion(ruta_archivo: str) -> list:
    """
    Procesa un CSV con validaciones completas.

    Args:
        ruta_archivo: Ruta al archivo CSV

    Returns:
        Lista de diccionarios con los datos válidos

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si hay errores de validación críticos
    """
    # 1. Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

    if os.path.getsize(ruta_archivo) == 0:
        raise ValueError("El archivo está vacío")

    # 2. Leer y validar
    datos_validos = []
    errores = []

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        # 3. Validar headers
        headers_esperados = ['nombre', 'edad', 'ciudad']
        if lector.fieldnames != headers_esperados:
            raise ValueError(f"Headers incorrectos: {lector.fieldnames}")

        # 4. Validar cada fila
        for num_fila, fila in enumerate(lector, start=2):
            # Validar edad es un número
            try:
                edad = int(fila['edad'])
                if edad < 0 or edad > 120:
                    errores.append(f"Fila {num_fila}: Edad fuera de rango: {edad}")
                    continue
            except ValueError:
                errores.append(f"Fila {num_fila}: Edad no es un número: {fila['edad']}")
                continue

            # Validar nombre no vacío
            if not fila['nombre'].strip():
                errores.append(f"Fila {num_fila}: Nombre vacío")
                continue

            # Si pasa todas las validaciones, añadir a datos válidos
            datos_validos.append(fila)

    # 5. Reportar errores
    if errores:
        print(f"⚠️ Se encontraron {len(errores)} errores:")
        for error in errores[:10]:  # Mostrar solo los primeros 10
            print(f"  - {error}")

    print(f"✅ {len(datos_validos)} filas válidas procesadas")

    return datos_validos
```

---

## 🔄 Parte 8: Transformación de Datos CSV

### 8.1 Transformaciones Comunes

#### 1. Filtrar filas

```python
import csv

def filtrar_por_ciudad(archivo_entrada: str, archivo_salida: str, ciudad: str) -> None:
    """
    Filtra un CSV y guarda solo las filas de una ciudad específica.
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
            lector = csv.DictReader(entrada)
            escritor = csv.DictWriter(salida, fieldnames=lector.fieldnames)

            escritor.writeheader()

            for fila in lector:
                if fila['ciudad'] == ciudad:
                    escritor.writerow(fila)
```

#### 2. Añadir columnas calculadas

```python
import csv

def añadir_columna_calculada(archivo_entrada: str, archivo_salida: str) -> None:
    """
    Añade una columna 'mayor_edad' basada en la edad.
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
            lector = csv.DictReader(entrada)

            # Añadir nueva columna a los headers
            fieldnames = lector.fieldnames + ['mayor_edad']
            escritor = csv.DictWriter(salida, fieldnames=fieldnames)

            escritor.writeheader()

            for fila in lector:
                edad = int(fila['edad'])
                fila['mayor_edad'] = 'Sí' if edad >= 18 else 'No'
                escritor.writerow(fila)
```

#### 3. Agrupar y agregar

```python
import csv
from collections import defaultdict

def agrupar_por_ciudad(archivo_entrada: str) -> dict:
    """
    Agrupa personas por ciudad y cuenta cuántas hay en cada una.

    Returns:
        Diccionario {ciudad: cantidad}
    """
    conteo = defaultdict(int)

    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            ciudad = fila['ciudad']
            conteo[ciudad] += 1

    return dict(conteo)
```

---

## 🎯 Parte 9: Buenas Prácticas en Producción

### 9.1 Siempre Usa Context Managers (`with`)

```python
# ❌ MAL: Puedes olvidar cerrar el archivo
archivo = open('datos.csv', 'r')
datos = archivo.read()
archivo.close()  # ¿Y si hay un error antes de esto?

# ✅ BIEN: El archivo se cierra automáticamente
with open('datos.csv', 'r', encoding='utf-8') as archivo:
    datos = archivo.read()
# Aquí el archivo ya está cerrado, incluso si hubo un error
```

### 9.2 Especifica Siempre el Encoding

```python
# ❌ MAL: Encoding por defecto (puede variar según el sistema)
with open('datos.csv', 'r') as archivo:
    datos = archivo.read()

# ✅ BIEN: Encoding explícito
with open('datos.csv', 'r', encoding='utf-8') as archivo:
    datos = archivo.read()
```

### 9.3 Valida Antes de Procesar

```python
# ❌ MAL: Confiar ciegamente en los datos
import csv
with open('datos.csv', 'r') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        edad = int(fila['edad'])  # ¿Y si no es un número?

# ✅ BIEN: Validar y manejar errores
import csv
with open('datos.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for num_fila, fila in enumerate(lector, start=2):
        try:
            edad = int(fila['edad'])
        except ValueError:
            print(f"⚠️ Fila {num_fila}: Edad inválida '{fila['edad']}'")
            continue
```

### 9.4 Maneja Archivos Grandes con Generadores

```python
# ❌ MAL: Cargar todo en memoria (puede fallar con archivos grandes)
import csv
with open('datos_grandes.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    todas_las_filas = list(lector)  # Carga todo en memoria
    for fila in todas_las_filas:
        procesar(fila)

# ✅ BIEN: Procesar línea por línea (memoria constante)
import csv
with open('datos_grandes.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:  # Procesa una fila a la vez
        procesar(fila)
```

### 9.5 Usa `newline=''` al Escribir en Windows

```python
# ❌ MAL: Puede generar líneas en blanco extra en Windows
with open('salida.csv', 'w', encoding='utf-8') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(['a', 'b', 'c'])

# ✅ BIEN: newline='' evita líneas en blanco
with open('salida.csv', 'w', encoding='utf-8', newline='') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(['a', 'b', 'c'])
```

### 9.6 Logging en Lugar de Print

```python
# ❌ MAL: Usar print para debugging
print("Procesando archivo...")
print(f"Encontradas {len(filas)} filas")

# ✅ BIEN: Usar logging (más profesional)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Procesando archivo...")
logger.info(f"Encontradas {len(filas)} filas")
```

---

## 📊 Parte 10: CSV vs Otros Formatos

### 10.1 Comparación

| Característica | CSV | JSON | Parquet | Excel |
|----------------|-----|------|---------|-------|
| **Tamaño** | Pequeño | Mediano | Muy pequeño | Grande |
| **Velocidad lectura** | Rápida | Media | Muy rápida | Lenta |
| **Estructura** | Tabular | Anidada | Tabular | Tabular |
| **Tipos de datos** | No (todo es texto) | Sí | Sí | Sí |
| **Compresión** | No nativa | No nativa | Sí | Sí |
| **Legibilidad humana** | ✅ Sí | ✅ Sí | ❌ No (binario) | ✅ Sí |
| **Universal** | ✅ Sí | ✅ Sí | ⚠️ Requiere librerías | ✅ Sí |

### 10.2 Cuándo Usar CSV

**✅ Usa CSV cuando**:
- Necesitas intercambiar datos entre sistemas diferentes
- Los datos son tabulares (filas y columnas)
- Quieres que sea legible por humanos
- No necesitas tipos de datos complejos
- El tamaño del archivo es manejable (< 1 GB)

**❌ No uses CSV cuando**:
- Los datos tienen estructura anidada (usa JSON)
- Necesitas máxima eficiencia (usa Parquet)
- Trabajas con archivos muy grandes (> 1 GB, usa Parquet)
- Necesitas preservar tipos de datos exactos (usa Parquet o base de datos)

---

## 🎓 Parte 11: Casos de Uso en Data Engineering

### 11.1 ETL: Extract, Transform, Load

**Caso**: Extraer datos de un sistema, transformarlos y cargarlos en otro.

```python
import csv

def etl_ventas(archivo_entrada: str, archivo_salida: str) -> None:
    """
    ETL simple: Extrae ventas, calcula totales, carga resultado.
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as entrada:
        with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
            lector = csv.DictReader(entrada)

            # Transform: Añadir columna calculada
            fieldnames = lector.fieldnames + ['total']
            escritor = csv.DictWriter(salida, fieldnames=fieldnames)
            escritor.writeheader()

            for fila in lector:
                # Extract
                cantidad = int(fila['cantidad'])
                precio = float(fila['precio_unitario'])

                # Transform
                fila['total'] = cantidad * precio

                # Load
                escritor.writerow(fila)
```

### 11.2 Data Quality: Validación de Datos

**Caso**: Validar que los datos cumplen con reglas de negocio.

```python
import csv

def validar_calidad_datos(archivo: str) -> dict:
    """
    Valida la calidad de los datos y retorna métricas.

    Returns:
        Diccionario con métricas de calidad
    """
    metricas = {
        'total_filas': 0,
        'filas_validas': 0,
        'filas_invalidas': 0,
        'errores': []
    }

    with open(archivo, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)

        for num_fila, fila in enumerate(lector, start=2):
            metricas['total_filas'] += 1

            # Validar reglas de negocio
            errores_fila = []

            # Regla 1: Precio debe ser positivo
            try:
                precio = float(fila['precio'])
                if precio <= 0:
                    errores_fila.append(f"Precio no positivo: {precio}")
            except ValueError:
                errores_fila.append(f"Precio inválido: {fila['precio']}")

            # Regla 2: Cantidad debe ser entero positivo
            try:
                cantidad = int(fila['cantidad'])
                if cantidad <= 0:
                    errores_fila.append(f"Cantidad no positiva: {cantidad}")
            except ValueError:
                errores_fila.append(f"Cantidad inválida: {fila['cantidad']}")

            # Actualizar métricas
            if errores_fila:
                metricas['filas_invalidas'] += 1
                metricas['errores'].append({
                    'fila': num_fila,
                    'errores': errores_fila
                })
            else:
                metricas['filas_validas'] += 1

    return metricas
```

### 11.3 Data Integration: Combinar Múltiples Fuentes

**Caso**: Combinar datos de ventas de múltiples locales.

```python
import csv
import os

def consolidar_ventas(carpeta_entrada: str, archivo_salida: str) -> None:
    """
    Consolida múltiples CSVs de ventas en uno solo.
    """
    with open(archivo_salida, 'w', encoding='utf-8', newline='') as salida:
        escritor = None

        for archivo in os.listdir(carpeta_entrada):
            if not archivo.endswith('.csv'):
                continue

            ruta_archivo = os.path.join(carpeta_entrada, archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as entrada:
                lector = csv.DictReader(entrada)

                # Inicializar escritor con los headers del primer archivo
                if escritor is None:
                    escritor = csv.DictWriter(salida, fieldnames=lector.fieldnames)
                    escritor.writeheader()

                # Escribir todas las filas
                for fila in lector:
                    escritor.writerow(fila)
```

---

## ✅ Checklist de Aprendizaje

Marca cada punto cuando lo hayas entendido:

### Conceptos Básicos
- [ ] Entiendo qué es un archivo CSV y su estructura
- [ ] Sé qué es un delimitador y cuáles son los más comunes
- [ ] Entiendo qué es el encoding y por qué es importante
- [ ] Puedo explicar la diferencia entre CSV europeo y americano

### Lectura de CSV
- [ ] Sé usar el módulo `csv` de Python
- [ ] Entiendo la diferencia entre `csv.reader` y `csv.DictReader`
- [ ] Sé cuándo usar `csv` vs `pandas`
- [ ] Siempre especifico `encoding='utf-8'` al abrir archivos

### Escritura de CSV
- [ ] Sé escribir CSV con `csv.writer`
- [ ] Sé escribir CSV con `csv.DictWriter`
- [ ] Uso `newline=''` en Windows para evitar líneas en blanco

### Manejo de Errores
- [ ] Valido que el archivo existe antes de abrirlo
- [ ] Valido que el archivo no está vacío
- [ ] Manejo archivos con delimitadores incorrectos
- [ ] Manejo filas con diferente número de columnas
- [ ] Manejo valores nulos o vacíos

### Validación de Datos
- [ ] Valido los headers esperados
- [ ] Valido los tipos de datos de cada columna
- [ ] Implemento reglas de negocio en mis validaciones
- [ ] Reporto errores de forma clara

### Transformación
- [ ] Sé filtrar filas de un CSV
- [ ] Sé añadir columnas calculadas
- [ ] Sé agrupar y agregar datos
- [ ] Sé combinar múltiples CSVs

### Buenas Prácticas
- [ ] Siempre uso context managers (`with`)
- [ ] Siempre especifico el encoding
- [ ] Valido antes de procesar
- [ ] Manejo archivos grandes con generadores
- [ ] Uso logging en lugar de print

### Aplicaciones
- [ ] Entiendo cómo usar CSV en ETL
- [ ] Sé implementar validaciones de calidad de datos
- [ ] Sé integrar datos de múltiples fuentes
- [ ] Entiendo cuándo usar CSV vs otros formatos

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Python csv module](https://docs.python.org/3/library/csv.html)
- [Pandas read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [RFC 4180 - CSV Format](https://tools.ietf.org/html/rfc4180)

### Artículos Recomendados
- [CSV Best Practices](https://www.oreilly.com/library/view/bad-data-handbook/9781449324957/)
- [Character Encoding for Beginners](https://www.w3.org/International/questions/qa-what-is-encoding)

### Herramientas Útiles
- [csvkit](https://csvkit.readthedocs.io/) - Herramientas de línea de comandos para CSV
- [CSVLint](https://csvlint.io/) - Validador online de CSV

### Próximos Pasos
- **02-EJEMPLOS.md**: Ejemplos trabajados paso a paso
- **03-EJERCICIOS.md**: Ejercicios prácticos con soluciones
- **04-proyecto-practico/**: Implementa un procesador CSV robusto

---

**¡Felicidades!** Has completado la teoría del Tema 2. Ahora es momento de practicar con ejemplos reales.

---

*Última actualización: 2025-10-19*
---

## 🧭 Navegación

⬅️ **Anterior**: [Python y Estadística - Proyecto Práctico](../tema-1-python-estadistica/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
