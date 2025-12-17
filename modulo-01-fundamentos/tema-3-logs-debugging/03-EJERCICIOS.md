# Ejercicios Prácticos: Sistema de Logs y Debugging

## 📚 Instrucciones Generales

> **Importante**: Intenta resolver cada ejercicio por tu cuenta antes de ver la solución. El aprendizaje real viene de intentar, equivocarse y corregir.

**Cómo usar este documento:**
1. Lee el contexto y entiende el problema
2. Intenta escribir el código sin mirar la solución
3. Ejecuta tu código y verifica que funciona
4. Compara tu solución con la proporcionada
5. Marca el ejercicio como completado en la tabla al final

**Tiempo estimado:** 2-3 horas (todos los ejercicios)

---

## 🟢 Ejercicios Básicos (1-6)

### Ejercicio 1: Configuración Básica de Logging
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 10 minutos

**Contexto**:
Trabajas en **DataFlow Industries** y necesitas crear un script simple que procese una lista de números y calcule su promedio. Tu jefa María quiere que uses logging en lugar de `print()`.

**Tu tarea**:
1. Configura logging con nivel INFO
2. Registra el inicio del proceso
3. Registra cuántos números se van a procesar
4. Registra el resultado final
5. Registra el fin del proceso

**Código inicial**:
```python
def calcular_promedio(numeros):
    # TODO: Añadir logging aquí
    total = sum(numeros)
    promedio = total / len(numeros)
    return promedio

# Ejecutar
numeros = [10, 20, 30, 40, 50]
resultado = calcular_promedio(numeros)
```

**Ayuda**: Usa `logging.basicConfig()` al inicio y `logging.info()` para los mensajes.

---

### Ejercicio 2: Niveles de Log Apropiados
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 10 minutos

**Contexto**:
**RestaurantData Co.** tiene una función que valida precios de productos. Necesitas añadir logging con los niveles apropiados.

**Tu tarea**:
Añade logging usando el nivel correcto para cada situación:
- Inicio de validación → INFO
- Precio válido → DEBUG
- Precio negativo → ERROR
- Precio muy alto (>1000€) → WARNING

**Código inicial**:
```python
def validar_precio(producto, precio):
    # TODO: Añadir logging con niveles apropiados

    if precio < 0:
        return False, "Precio negativo"

    if precio > 1000:
        return True, "Precio válido pero muy alto"

    return True, "Precio válido"

# Probar con diferentes valores
validar_precio("Hamburguesa", 12.50)
validar_precio("Menú especial", -5.00)
validar_precio("Catering evento", 1500.00)
```

**Ayuda**: Recuerda que DEBUG es para detalles, INFO para flujo normal, WARNING para cosas inesperadas pero no errores, y ERROR para fallos.

---

### Ejercicio 3: Logging en Archivo
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 12 minutos

**Contexto**:
**CloudAPI Systems** necesita que los logs de su script de monitoreo se guarden en un archivo llamado `monitoreo.log` en lugar de mostrarse solo en consola.

**Tu tarea**:
1. Configura logging para escribir en archivo `monitoreo.log`
2. Usa formato: `%(asctime)s - %(levelname)s - %(message)s`
3. Registra el estado de 3 servidores (online/offline)

**Código inicial**:
```python
import logging

# TODO: Configurar logging para escribir en archivo

def verificar_servidor(nombre, estado):
    # TODO: Registrar el estado del servidor
    pass

# Verificar servidores
verificar_servidor("Servidor-1", "online")
verificar_servidor("Servidor-2", "offline")
verificar_servidor("Servidor-3", "online")
```

**Ayuda**: Usa el parámetro `filename` en `basicConfig()`.

---

### Ejercicio 4: Try-Except con Logging
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 15 minutos

**Contexto**:
**FinTech Analytics** tiene una función que divide dos números. A veces recibe datos inválidos y falla. Necesitas añadir manejo de errores con logging.

**Tu tarea**:
1. Añade try-except para capturar errores
2. Registra errores con `logging.error()`
3. Registra el tipo de error que ocurrió
4. La función debe retornar `None` si hay error

**Código inicial**:
```python
def dividir(a, b):
    # TODO: Añadir try-except y logging
    resultado = a / b
    return resultado

# Probar con diferentes valores
print(dividir(10, 2))      # Debe funcionar
print(dividir(10, 0))      # Error: división por cero
print(dividir("10", 2))    # Error: tipo incorrecto
```

**Ayuda**: Captura `ZeroDivisionError` y `TypeError` por separado.

---

### Ejercicio 5: Logging de Progreso
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 15 minutos

**Contexto**:
**LogisticFlow** procesa 1000 paquetes. Quieren ver el progreso cada 100 paquetes procesados.

**Tu tarea**:
1. Procesa una lista de 1000 números (simula paquetes)
2. Registra progreso cada 100 iteraciones
3. Registra el total al final

**Código inicial**:
```python
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def procesar_paquetes(cantidad):
    # TODO: Procesar y registrar progreso cada 100
    for i in range(1, cantidad + 1):
        # Simular procesamiento
        pass

    # TODO: Registrar total procesado

procesar_paquetes(1000)
```

**Ayuda**: Usa `if i % 100 == 0:` para detectar cada 100 iteraciones.

---

### Ejercicio 6: Formato Personalizado
**Dificultad**: ⭐ Fácil
**Tiempo estimado**: 12 minutos

**Contexto**:
**DataFlow Industries** quiere logs con formato específico que incluya: fecha, hora, nivel, nombre del archivo y mensaje.

**Tu tarea**:
Configura logging con el formato: `YYYY-MM-DD HH:MM:SS - NIVEL - [archivo.py] - Mensaje`

**Código inicial**:
```python
import logging

# TODO: Configurar con formato personalizado

logging.info("Iniciando proceso ETL")
logging.warning("Memoria al 85%")
logging.error("Error al conectar a base de datos")
```

**Ayuda**: Usa `%(asctime)s`, `%(levelname)s`, `%(filename)s` y `%(message)s` en el formato.

---

## 🟡 Ejercicios Intermedios (7-11)

### Ejercicio 7: Múltiples Handlers
**Dificultad**: ⭐⭐ Intermedio
**Tiempo estimado**: 20 minutos

**Contexto**:
**CloudAPI Systems** necesita logs tanto en consola (para desarrollo) como en archivo (para auditoría). Los logs de consola deben ser solo INFO y superiores, mientras que el archivo debe capturar TODO (DEBUG incluido).

**Tu tarea**:
1. Crea un logger con nombre `cloudapi`
2. Añade un handler de consola (nivel INFO)
3. Añade un handler de archivo (nivel DEBUG)
4. Ambos con el mismo formato
5. Prueba con mensajes de diferentes niveles

**Código inicial**:
```python
import logging

# TODO: Crear logger y configurar handlers

logger = logging.getLogger('cloudapi')

# Probar con diferentes niveles
logger.debug("Detalles de configuración: puerto=8080")
logger.info("Servidor iniciado")
logger.warning("Conexión lenta detectada")
logger.error("Error al procesar request")
```

**Ayuda**: Usa `StreamHandler()` para consola y `FileHandler()` para archivo.

---

### Ejercicio 8: Rotación de Archivos por Tamaño
**Dificultad**: ⭐⭐ Intermedio
**Tiempo estimado**: 25 minutos

**Contexto**:
**RestaurantData Co.** genera muchos logs. Necesitan rotación automática cuando el archivo alcance 1 MB, manteniendo 3 backups.

**Tu tarea**:
1. Configura `RotatingFileHandler`
2. Tamaño máximo: 1 MB (1024 * 1024 bytes)
3. Mantener 3 archivos de backup
4. Simula generación de logs (escribe 1000 mensajes)

**Código inicial**:
```python
import logging
from logging.handlers import RotatingFileHandler

# TODO: Configurar RotatingFileHandler

logger = logging.getLogger('restaurant_logs')

# Simular generación de muchos logs
for i in range(1000):
    logger.info(f"Procesando pedido #{i}: Cliente X, Total: {i * 10}€")
```

**Ayuda**: `RotatingFileHandler(filename, maxBytes, backupCount)`.

---

### Ejercicio 9: Debugging de Datos Inválidos
**Dificultad**: ⭐⭐ Intermedio
**Tiempo estimado**: 30 minutos

**Contexto**:
**FinTech Analytics** procesa transacciones pero algunas tienen datos inválidos. Necesitas identificar cuáles fallan y por qué, sin detener todo el proceso.

**Datos**:
```python
transacciones = [
    {'id': 1, 'monto': 100.50, 'tipo': 'compra'},
    {'id': 2, 'monto': -50.00, 'tipo': 'compra'},      # Error: monto negativo
    {'id': 3, 'monto': 'N/A', 'tipo': 'compra'},       # Error: monto no numérico
    {'id': 4, 'monto': 200.00, 'tipo': 'compra'},
    {'id': 5, 'monto': 75.30, 'tipo': 'devolucion'},
    {'id': 6, 'monto': 150.00, 'tipo': 'invalido'},    # Error: tipo desconocido
]
```

**Tu tarea**:
1. Procesa todas las transacciones
2. Registra cada error con el ID de la transacción
3. Continúa procesando aunque haya errores
4. Al final, muestra resumen: exitosas, fallidas, tipos de error

**Ayuda**: Usa try-except dentro del bucle, no fuera.

---

### Ejercicio 10: Logger Reutilizable
**Dificultad**: ⭐⭐ Intermedio
**Tiempo estimado**: 30 minutos

**Contexto**:
**LogisticFlow** tiene múltiples scripts que necesitan logging consistente. Crea una función que configure un logger estándar que puedan usar todos.

**Tu tarea**:
Crea una función `crear_logger(nombre, nivel, archivo)` que:
1. Cree un logger con el nombre dado
2. Configure nivel de log
3. Añada handler de archivo
4. Añada handler de consola
5. Use formato estándar de la empresa

**Código inicial**:
```python
import logging

def crear_logger(nombre, nivel=logging.INFO, archivo=None):
    # TODO: Implementar función
    pass

# Usar el logger
logger1 = crear_logger('entregas', logging.DEBUG, 'entregas.log')
logger1.info("Procesando entrega #123")

logger2 = crear_logger('inventario', logging.WARNING, 'inventario.log')
logger2.warning("Stock bajo: Producto XYZ")
```

**Ayuda**: Verifica que el logger no tenga handlers ya añadidos antes de añadir nuevos.

---

### Ejercicio 11: Logging con Request ID
**Dificultad**: ⭐⭐ Intermedio
**Tiempo estimado**: 25 minutos

**Contexto**:
**CloudAPI Systems** procesa múltiples requests simultáneamente. Necesitan identificar qué logs pertenecen a cada request usando un ID único.

**Tu tarea**:
1. Procesa una lista de requests
2. Cada log debe incluir `[Request {id}]` al inicio
3. Registra inicio, procesamiento y fin de cada request
4. Simula un error aleatorio en algunos requests

**Código inicial**:
```python
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def procesar_request(request_id, endpoint):
    # TODO: Añadir logging con request_id
    # TODO: Simular procesamiento
    # TODO: Simular error aleatorio (10% probabilidad)
    pass

# Procesar varios requests
requests = [
    (1, '/api/ventas'),
    (2, '/api/clientes'),
    (3, '/api/productos'),
    (4, '/api/ventas'),
    (5, '/api/reportes'),
]

for req_id, endpoint in requests:
    procesar_request(req_id, endpoint)
```

**Ayuda**: Usa f-strings para incluir el request_id en cada mensaje.

---

## 🔴 Ejercicios Avanzados (12-14)

### Ejercicio 12: Sistema de Logging Enterprise
**Dificultad**: ⭐⭐⭐ Avanzado
**Tiempo estimado**: 45 minutos

**Contexto**:
**DataFlow Industries** necesita un sistema de logging completo para producción con:
- Rotación diaria de archivos
- Archivo separado para errores
- Configuración por variable de entorno
- Retención de 30 días para logs normales, 90 para errores

**Tu tarea**:
Crea una clase `LoggerEmpresa` que:
1. Configure rotación diaria con `TimedRotatingFileHandler`
2. Cree archivo separado para errores (ERROR y CRITICAL)
3. Lea nivel de log de variable de entorno `LOG_LEVEL`
4. Incluya nombre del servicio en cada log
5. Formato: `YYYY-MM-DD HH:MM:SS - SERVICIO - NIVEL - Mensaje`

**Código inicial**:
```python
import logging
from logging.handlers import TimedRotatingFileHandler
import os

class LoggerEmpresa:
    def __init__(self, nombre_servicio):
        # TODO: Implementar configuración completa
        pass

    def get_logger(self):
        # TODO: Retornar logger configurado
        pass

# Usar el logger
logger = LoggerEmpresa('pipeline_etl').get_logger()
logger.info("Pipeline iniciado")
logger.error("Error al conectar a base de datos")
```

**Ayuda**: Usa `when='midnight'` para rotación diaria y `suffix='%Y-%m-%d'` para el formato de fecha.

---

### Ejercicio 13: Debugging de Pipeline Complejo
**Dificultad**: ⭐⭐⭐ Avanzado
**Tiempo estimado**: 50 minutos

**Contexto**:
**RestaurantData Co.** tiene un pipeline ETL complejo que a veces falla. Necesitas implementar logging detallado para identificar problemas.

**Pipeline**:
1. Extraer datos de archivo CSV
2. Validar campos obligatorios
3. Transformar datos (calcular totales)
4. Detectar outliers
5. Guardar en archivo de salida

**Tu tarea**:
Implementa el pipeline completo con:
1. Logging de cada fase
2. Contadores de registros procesados/fallidos
3. Logging de outliers detectados
4. Resumen final con métricas
5. Decisión automática: si >5% errores, alerta crítica

**Datos de prueba**:
```python
datos_csv = [
    {'id': 1, 'producto': 'Hamburguesa', 'precio': 12.50, 'cantidad': 2},
    {'id': 2, 'producto': 'Pizza', 'precio': 15.00, 'cantidad': 1},
    {'id': 3, 'producto': '', 'precio': 10.00, 'cantidad': 3},           # Error: producto vacío
    {'id': 4, 'producto': 'Ensalada', 'precio': -5.00, 'cantidad': 1},   # Error: precio negativo
    {'id': 5, 'producto': 'Pasta', 'precio': 18.00, 'cantidad': 2},
    {'id': 6, 'producto': 'Catering', 'precio': 5000.00, 'cantidad': 1}, # Outlier
    {'id': 7, 'producto': 'Bebida', 'precio': 3.50, 'cantidad': 5},
]
```

**Ayuda**: Usa un diccionario para contar tipos de errores.

---

### Ejercicio 14: Logging con Métricas de Performance
**Dificultad**: ⭐⭐⭐ Avanzado
**Tiempo estimado**: 40 minutos

**Contexto**:
**CloudAPI Systems** necesita monitorear el performance de su API. Quieren registrar tiempo de respuesta de cada endpoint y alertar si es muy lento.

**Tu tarea**:
Implementa un sistema que:
1. Mida tiempo de ejecución de cada función
2. Registre tiempo de respuesta en logs
3. Alerte (WARNING) si tiempo > 1 segundo
4. Alerte (ERROR) si tiempo > 3 segundos
5. Al final, muestre estadísticas: promedio, mínimo, máximo

**Código inicial**:
```python
import logging
import time
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def medir_performance(func):
    """Decorador para medir tiempo de ejecución."""
    # TODO: Implementar decorador que mida tiempo y registre logs
    pass

@medir_performance
def consultar_ventas():
    time.sleep(random.uniform(0.1, 2.0))  # Simular trabajo
    return {"ventas": 1500}

@medir_performance
def consultar_clientes():
    time.sleep(random.uniform(0.5, 3.5))  # Simular trabajo
    return {"clientes": 250}

# Ejecutar múltiples veces
for i in range(10):
    consultar_ventas()
    consultar_clientes()
```

**Ayuda**: Usa `time.time()` antes y después de ejecutar la función. Guarda los tiempos en una lista para calcular estadísticas.

---

## ✅ Soluciones

### Solución Ejercicio 1: Configuración Básica

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calcular_promedio(numeros):
    logging.info("Iniciando cálculo de promedio")
    logging.info(f"Cantidad de números a procesar: {len(numeros)}")

    total = sum(numeros)
    promedio = total / len(numeros)

    logging.info(f"Promedio calculado: {promedio:.2f}")
    logging.info("Proceso completado")

    return promedio

# Ejecutar
numeros = [10, 20, 30, 40, 50]
resultado = calcular_promedio(numeros)
```

**Explicación**:
- `basicConfig()` se llama una sola vez al inicio
- Usamos `logging.info()` para el flujo normal del programa
- Incluimos información útil: cantidad de números y resultado
- Formato con timestamp para saber cuándo ocurrió cada evento

**Resultado esperado**:
```
2025-10-18 15:30:45 - INFO - Iniciando cálculo de promedio
2025-10-18 15:30:45 - INFO - Cantidad de números a procesar: 5
2025-10-18 15:30:45 - INFO - Promedio calculado: 30.00
2025-10-18 15:30:45 - INFO - Proceso completado
```

---

### Solución Ejercicio 2: Niveles de Log Apropiados

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Capturar todos los niveles
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validar_precio(producto, precio):
    logging.info(f"Validando precio de '{producto}'")

    if precio < 0:
        logging.error(f"Precio negativo para '{producto}': {precio}€")
        return False, "Precio negativo"

    if precio > 1000:
        logging.warning(
            f"Precio muy alto para '{producto}': {precio}€ "
            f"(umbral: 1000€)"
        )
        return True, "Precio válido pero muy alto"

    logging.debug(f"Precio válido para '{producto}': {precio}€")
    return True, "Precio válido"

# Probar con diferentes valores
validar_precio("Hamburguesa", 12.50)
validar_precio("Menú especial", -5.00)
validar_precio("Catering evento", 1500.00)
```

**Explicación**:
- **INFO**: Inicio de validación (flujo normal)
- **DEBUG**: Precio válido (detalle que no siempre necesitas ver)
- **WARNING**: Precio muy alto (sospechoso pero no error)
- **ERROR**: Precio negativo (dato inválido)

**Resultado esperado**:
```
2025-10-18 15:35:10 - INFO - Validando precio de 'Hamburguesa'
2025-10-18 15:35:10 - DEBUG - Precio válido para 'Hamburguesa': 12.5€
2025-10-18 15:35:10 - INFO - Validando precio de 'Menú especial'
2025-10-18 15:35:10 - ERROR - Precio negativo para 'Menú especial': -5.0€
2025-10-18 15:35:10 - INFO - Validando precio de 'Catering evento'
2025-10-18 15:35:10 - WARNING - Precio muy alto para 'Catering evento': 1500.0€ (umbral: 1000€)
```

---

### Solución Ejercicio 3: Logging en Archivo

```python
import logging

# Configurar logging para escribir en archivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='monitoreo.log',
    filemode='a'  # 'a' = append, 'w' = overwrite
)

def verificar_servidor(nombre, estado):
    if estado == "online":
        logging.info(f"Servidor '{nombre}' está ONLINE")
    else:
        logging.error(f"Servidor '{nombre}' está OFFLINE")

# Verificar servidores
verificar_servidor("Servidor-1", "online")
verificar_servidor("Servidor-2", "offline")
verificar_servidor("Servidor-3", "online")

print("Logs guardados en 'monitoreo.log'")
```

**Explicación**:
- `filename='monitoreo.log'` guarda logs en archivo
- `filemode='a'` añade al archivo existente (no sobrescribe)
- Los logs NO aparecen en consola, solo en archivo
- Usamos ERROR para servidores offline (problema que requiere atención)

**Contenido de `monitoreo.log`**:
```
2025-10-18 15:40:20 - INFO - Servidor 'Servidor-1' está ONLINE
2025-10-18 15:40:20 - ERROR - Servidor 'Servidor-2' está OFFLINE
2025-10-18 15:40:20 - INFO - Servidor 'Servidor-3' está ONLINE
```

---

### Solución Ejercicio 4: Try-Except con Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

def dividir(a, b):
    try:
        resultado = a / b
        logging.info(f"División exitosa: {a} / {b} = {resultado}")
        return resultado

    except ZeroDivisionError:
        logging.error(f"Error: División por cero ({a} / {b})")
        return None

    except TypeError as e:
        logging.error(f"Error de tipo: {e} (a={a}, b={b})")
        return None

    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return None

# Probar con diferentes valores
print(dividir(10, 2))      # Debe funcionar
print(dividir(10, 0))      # Error: división por cero
print(dividir("10", 2))    # Error: tipo incorrecto
```

**Explicación**:
- Capturamos errores específicos primero (`ZeroDivisionError`, `TypeError`)
- Luego capturamos cualquier otro error con `Exception`
- Registramos información útil: qué valores causaron el error
- Retornamos `None` para indicar fallo (consistente)

**Resultado esperado**:
```
INFO - División exitosa: 10 / 2 = 5.0
5.0
ERROR - Error: División por cero (10 / 0)
None
ERROR - Error de tipo: unsupported operand type(s) for /: 'str' and 'int' (a=10, b=2)
None
```

---

### Solución Ejercicio 5: Logging de Progreso

```python
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def procesar_paquetes(cantidad):
    logging.info(f"Iniciando procesamiento de {cantidad} paquetes")

    for i in range(1, cantidad + 1):
        # Simular procesamiento
        pass

        # Registrar progreso cada 100
        if i % 100 == 0:
            logging.info(f"Progreso: {i}/{cantidad} paquetes procesados")

    logging.info(f"Procesamiento completado: {cantidad} paquetes")

procesar_paquetes(1000)
```

**Explicación**:
- `i % 100 == 0` detecta múltiplos de 100
- Mostramos progreso relativo: `{i}/{cantidad}`
- Mensaje final confirma completitud

**Resultado esperado**:
```
Iniciando procesamiento de 1000 paquetes
Progreso: 100/1000 paquetes procesados
Progreso: 200/1000 paquetes procesados
Progreso: 300/1000 paquetes procesados
...
Progreso: 1000/1000 paquetes procesados
Procesamiento completado: 1000 paquetes
```

---

### Solución Ejercicio 6: Formato Personalizado

```python
import logging

# Configurar con formato personalizado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Iniciando proceso ETL")
logging.warning("Memoria al 85%")
logging.error("Error al conectar a base de datos")
```

**Explicación**:
- `%(asctime)s`: Fecha y hora
- `%(levelname)s`: Nivel del log
- `%(filename)s`: Nombre del archivo que generó el log
- `%(message)s`: El mensaje
- `datefmt`: Formato específico de fecha

**Resultado esperado**:
```
2025-10-18 15:45:30 - INFO - [ejercicio6.py] - Iniciando proceso ETL
2025-10-18 15:45:30 - WARNING - [ejercicio6.py] - Memoria al 85%
2025-10-18 15:45:30 - ERROR - [ejercicio6.py] - Error al conectar a base de datos
```

---

### Solución Ejercicio 7: Múltiples Handlers

```python
import logging

# Crear logger
logger = logging.getLogger('cloudapi')
logger.setLevel(logging.DEBUG)  # Captura TODO

# Formato común
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler 1: Consola (solo INFO y superior)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Handler 2: Archivo (TODO, incluido DEBUG)
file_handler = logging.FileHandler('cloudapi.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Añadir handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Probar con diferentes niveles
logger.debug("Detalles de configuración: puerto=8080")
logger.info("Servidor iniciado")
logger.warning("Conexión lenta detectada")
logger.error("Error al procesar request")
```

**Explicación**:
- Creamos un logger con nombre específico
- Dos handlers: uno para consola, otro para archivo
- Niveles diferentes: INFO en consola, DEBUG en archivo
- Mismo formato para ambos

**En consola (solo INFO y superior)**:
```
2025-10-18 15:50:10 - INFO - Servidor iniciado
2025-10-18 15:50:10 - WARNING - Conexión lenta detectada
2025-10-18 15:50:10 - ERROR - Error al procesar request
```

**En archivo `cloudapi.log` (TODO)**:
```
2025-10-18 15:50:10 - DEBUG - Detalles de configuración: puerto=8080
2025-10-18 15:50:10 - INFO - Servidor iniciado
2025-10-18 15:50:10 - WARNING - Conexión lenta detectada
2025-10-18 15:50:10 - ERROR - Error al procesar request
```

---

### Solución Ejercicio 8: Rotación de Archivos por Tamaño

```python
import logging
from logging.handlers import RotatingFileHandler

# Crear logger
logger = logging.getLogger('restaurant_logs')
logger.setLevel(logging.INFO)

# Configurar RotatingFileHandler
handler = RotatingFileHandler(
    filename='restaurant.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=3,  # Mantener 3 backups
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Simular generación de muchos logs
for i in range(1000):
    logger.info(f"Procesando pedido #{i}: Cliente X, Total: {i * 10}€")

print("Logs generados. Verifica los archivos:")
print("- restaurant.log (actual)")
print("- restaurant.log.1 (backup 1)")
print("- restaurant.log.2 (backup 2)")
print("- restaurant.log.3 (backup 3)")
```

**Explicación**:
- `maxBytes=1024*1024`: Cuando el archivo alcance 1MB, rotará
- `backupCount=3`: Mantiene 3 archivos antiguos
- Rotación automática: `file.log` → `file.log.1` → `file.log.2` → `file.log.3`

**Estructura de archivos resultante**:
```
restaurant.log      ← Archivo actual (más reciente)
restaurant.log.1    ← Backup 1
restaurant.log.2    ← Backup 2
restaurant.log.3    ← Backup 3 (más antiguo)
```

---

### Solución Ejercicio 9: Debugging de Datos Inválidos

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

transacciones = [
    {'id': 1, 'monto': 100.50, 'tipo': 'compra'},
    {'id': 2, 'monto': -50.00, 'tipo': 'compra'},
    {'id': 3, 'monto': 'N/A', 'tipo': 'compra'},
    {'id': 4, 'monto': 200.00, 'tipo': 'compra'},
    {'id': 5, 'monto': 75.30, 'tipo': 'devolucion'},
    {'id': 6, 'monto': 150.00, 'tipo': 'invalido'},
]

def procesar_transacciones(transacciones):
    logging.info(f"Iniciando procesamiento de {len(transacciones)} transacciones")

    exitosas = 0
    fallidas = 0
    tipos_error = {}

    for tx in transacciones:
        tx_id = tx['id']

        try:
            # Validar monto
            monto = float(tx['monto'])
            if monto < 0:
                raise ValueError(f"Monto negativo: {monto}")

            # Validar tipo
            tipos_validos = ['compra', 'devolucion']
            if tx['tipo'] not in tipos_validos:
                raise ValueError(f"Tipo inválido: {tx['tipo']}")

            # Procesar transacción
            logging.info(f"Transacción {tx_id}: {tx['tipo']} de {monto}€")
            exitosas += 1

        except ValueError as e:
            fallidas += 1
            error_tipo = str(e).split(':')[0]
            tipos_error[error_tipo] = tipos_error.get(error_tipo, 0) + 1
            logging.error(f"Transacción {tx_id}: {e}")
            logging.debug(f"Transacción {tx_id}: Datos completos: {tx}")
            continue

        except Exception as e:
            fallidas += 1
            tipos_error['Otro'] = tipos_error.get('Otro', 0) + 1
            logging.error(f"Transacción {tx_id}: Error inesperado - {e}")
            continue

    # Resumen final
    logging.info("=== Resumen del Procesamiento ===")
    logging.info(f"Total: {len(transacciones)}")
    logging.info(f"Exitosas: {exitosas}")
    logging.info(f"Fallidas: {fallidas}")

    if tipos_error:
        logging.info("Errores por tipo:")
        for tipo, cantidad in tipos_error.items():
            logging.info(f"  - {tipo}: {cantidad}")

    tasa_error = fallidas / len(transacciones)
    if tasa_error > 0.05:
        logging.critical(
            f"Tasa de error alta: {tasa_error:.1%}. Revisar calidad de datos."
        )

procesar_transacciones(transacciones)
```

**Explicación**:
- Try-except DENTRO del bucle para no detener todo
- Contadores de exitosas/fallidas
- Diccionario para contar tipos de error
- Resumen completo al final
- Alerta crítica si >5% errores

**Resultado esperado**:
```
2025-10-18 16:00:10 - INFO - Iniciando procesamiento de 6 transacciones
2025-10-18 16:00:10 - INFO - Transacción 1: compra de 100.5€
2025-10-18 16:00:10 - ERROR - Transacción 2: Monto negativo: -50.0
2025-10-18 16:00:10 - ERROR - Transacción 3: could not convert string to float: 'N/A'
2025-10-18 16:00:10 - INFO - Transacción 4: compra de 200.0€
2025-10-18 16:00:10 - INFO - Transacción 5: devolucion de 75.3€
2025-10-18 16:00:10 - ERROR - Transacción 6: Tipo inválido: invalido
2025-10-18 16:00:10 - INFO - === Resumen del Procesamiento ===
2025-10-18 16:00:10 - INFO - Total: 6
2025-10-18 16:00:10 - INFO - Exitosas: 3
2025-10-18 16:00:10 - INFO - Fallidas: 3
2025-10-18 16:00:10 - INFO - Errores por tipo:
2025-10-18 16:00:10 - INFO -   - Monto negativo: 1
2025-10-18 16:00:10 - INFO -   - Otro: 1
2025-10-18 16:00:10 - INFO -   - Tipo inválido: 1
2025-10-18 16:00:10 - CRITICAL - Tasa de error alta: 50.0%. Revisar calidad de datos.
```

---

### Solución Ejercicio 10: Logger Reutilizable

```python
import logging

def crear_logger(nombre, nivel=logging.INFO, archivo=None):
    """
    Crea un logger configurado con handlers estándar.

    Args:
        nombre: Nombre del logger
        nivel: Nivel de logging (default: INFO)
        archivo: Ruta del archivo de log (opcional)

    Returns:
        Logger configurado
    """
    # Crear logger
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Formato estándar de la empresa
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(nivel)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler de archivo (si se especifica)
    if archivo:
        file_handler = logging.FileHandler(archivo, encoding='utf-8')
        file_handler.setLevel(nivel)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Usar el logger
logger1 = crear_logger('entregas', logging.DEBUG, 'entregas.log')
logger1.info("Procesando entrega #123")
logger1.debug("Detalles de la entrega: destino=Madrid")

logger2 = crear_logger('inventario', logging.WARNING, 'inventario.log')
logger2.warning("Stock bajo: Producto XYZ")
logger2.info("Este mensaje NO aparece (nivel WARNING)")
```

**Explicación**:
- Función reutilizable para crear loggers consistentes
- Verifica handlers existentes para evitar duplicación
- Formato estándar de la empresa
- Archivo opcional
- Nivel configurable

---

### Solución Ejercicio 11: Logging con Request ID

```python
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def procesar_request(request_id, endpoint):
    logging.info(f"[Request {request_id}] Iniciando procesamiento de {endpoint}")

    inicio = time.time()

    try:
        # Simular procesamiento
        time.sleep(random.uniform(0.1, 0.5))

        # Simular error aleatorio (10% probabilidad)
        if random.random() < 0.1:
            raise Exception("Error de conexión con base de datos")

        tiempo = time.time() - inicio
        logging.info(f"[Request {request_id}] Completado en {tiempo:.3f}s")
        return {'status': 'success', 'tiempo': tiempo}

    except Exception as e:
        tiempo = time.time() - inicio
        logging.error(f"[Request {request_id}] Error: {e}")
        logging.info(f"[Request {request_id}] Fallido después de {tiempo:.3f}s")
        return {'status': 'error', 'error': str(e)}

# Procesar varios requests
requests = [
    (1, '/api/ventas'),
    (2, '/api/clientes'),
    (3, '/api/productos'),
    (4, '/api/ventas'),
    (5, '/api/reportes'),
]

for req_id, endpoint in requests:
    procesar_request(req_id, endpoint)
    time.sleep(0.1)
```

**Explicación**:
- `[Request {id}]` al inicio de cada mensaje
- Permite filtrar logs por request específico
- Útil cuando hay múltiples requests simultáneos
- Incluye tiempo de respuesta

**Resultado esperado**:
```
2025-10-18 16:10:15 - [Request 1] Iniciando procesamiento de /api/ventas
2025-10-18 16:10:15 - [Request 1] Completado en 0.234s
2025-10-18 16:10:15 - [Request 2] Iniciando procesamiento de /api/clientes
2025-10-18 16:10:16 - [Request 2] Completado en 0.412s
2025-10-18 16:10:16 - [Request 3] Iniciando procesamiento de /api/productos
2025-10-18 16:10:16 - [Request 3] Error: Error de conexión con base de datos
2025-10-18 16:10:16 - [Request 3] Fallido después de 0.156s
...
```

---

### Solución Ejercicio 12: Sistema de Logging Enterprise

```python
import logging
from logging.handlers import TimedRotatingFileHandler
import os

class LoggerEmpresa:
    """
    Sistema de logging enterprise con rotación diaria y archivo separado de errores.
    """

    def __init__(self, nombre_servicio):
        self.nombre_servicio = nombre_servicio
        self.logger = logging.getLogger(nombre_servicio)

        # Leer nivel de variable de entorno
        nivel_str = os.getenv('LOG_LEVEL', 'INFO')
        nivel = getattr(logging, nivel_str.upper(), logging.INFO)
        self.logger.setLevel(nivel)

        # Evitar duplicación
        if not self.logger.handlers:
            self._configurar_handlers()

    def _configurar_handlers(self):
        """Configura handlers con rotación diaria."""

        # Formato estándar
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)

        # Handler 1: Archivo principal con rotación diaria
        file_handler = TimedRotatingFileHandler(
            filename=f'logs/{self.nombre_servicio}.log',
            when='midnight',
            interval=1,
            backupCount=30,  # 30 días
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        file_handler.suffix = '%Y-%m-%d'  # Formato de fecha
        self.logger.addHandler(file_handler)

        # Handler 2: Archivo separado para errores
        error_handler = TimedRotatingFileHandler(
            filename=f'logs/{self.nombre_servicio}_errors.log',
            when='midnight',
            interval=1,
            backupCount=90,  # 90 días
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.suffix = '%Y-%m-%d'
        self.logger.addHandler(error_handler)

        # Handler 3: Consola (opcional, solo en desarrollo)
        if os.getenv('ENTORNO') == 'desarrollo':
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """Retorna el logger configurado."""
        return self.logger

# Usar el logger
logger = LoggerEmpresa('pipeline_etl').get_logger()
logger.info("Pipeline iniciado")
logger.debug("Configuración cargada: DB=localhost")
logger.warning("Conexión lenta detectada")
logger.error("Error al conectar a base de datos")
logger.critical("Sistema fuera de servicio")

print("\nLogs generados en:")
print("- logs/pipeline_etl.log (todos los logs)")
print("- logs/pipeline_etl_errors.log (solo errores)")
```

**Explicación**:
- Clase reutilizable para todos los servicios
- Rotación diaria a medianoche
- Archivo separado para errores (retención más larga)
- Lee nivel de variable de entorno `LOG_LEVEL`
- Incluye nombre del servicio en cada log
- Consola solo en desarrollo

**Estructura de archivos después de varios días**:
```
logs/
├── pipeline_etl.log                    ← Logs de hoy
├── pipeline_etl.log.2025-10-17         ← Logs de ayer
├── pipeline_etl.log.2025-10-16         ← Logs de anteayer
├── ...
├── pipeline_etl_errors.log             ← Errores de hoy
├── pipeline_etl_errors.log.2025-10-17  ← Errores de ayer
└── ...
```

---

### Solución Ejercicio 13: Debugging de Pipeline Complejo

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

datos_csv = [
    {'id': 1, 'producto': 'Hamburguesa', 'precio': 12.50, 'cantidad': 2},
    {'id': 2, 'producto': 'Pizza', 'precio': 15.00, 'cantidad': 1},
    {'id': 3, 'producto': '', 'precio': 10.00, 'cantidad': 3},
    {'id': 4, 'producto': 'Ensalada', 'precio': -5.00, 'cantidad': 1},
    {'id': 5, 'producto': 'Pasta', 'precio': 18.00, 'cantidad': 2},
    {'id': 6, 'producto': 'Catering', 'precio': 5000.00, 'cantidad': 1},
    {'id': 7, 'producto': 'Bebida', 'precio': 3.50, 'cantidad': 5},
]

def pipeline_etl(datos):
    logging.info("=== Iniciando Pipeline ETL ===")
    logging.info(f"Total de registros a procesar: {len(datos)}")

    # Contadores
    procesados = 0
    fallidos = 0
    tipos_error = {}
    outliers = []
    datos_validos = []

    # Fase 1: Extracción (ya tenemos los datos)
    logging.info("Fase 1: Extracción - Completada")

    # Fase 2: Validación y Transformación
    logging.info("Fase 2: Validación y Transformación")

    for registro in datos:
        reg_id = registro['id']

        try:
            # Validar campos obligatorios
            if not registro['producto']:
                raise ValueError("Producto vacío")

            precio = float(registro['precio'])
            cantidad = int(registro['cantidad'])

            # Validar valores
            if precio < 0:
                raise ValueError(f"Precio negativo: {precio}")
            if cantidad <= 0:
                raise ValueError(f"Cantidad inválida: {cantidad}")

            # Calcular total
            total = precio * cantidad
            registro['total'] = total

            # Detectar outliers (total > 1000€)
            if total > 1000:
                outliers.append(registro)
                logging.warning(
                    f"Registro {reg_id}: Outlier detectado - "
                    f"Total: {total:.2f}€ (Producto: {registro['producto']})"
                )

            datos_validos.append(registro)
            procesados += 1

        except ValueError as e:
            fallidos += 1
            error_tipo = str(e).split(':')[0]
            tipos_error[error_tipo] = tipos_error.get(error_tipo, 0) + 1
            logging.error(f"Registro {reg_id}: {e}")
            logging.debug(f"Registro {reg_id}: Datos: {registro}")
            continue

        except Exception as e:
            fallidos += 1
            tipos_error['Otro'] = tipos_error.get('Otro', 0) + 1
            logging.error(f"Registro {reg_id}: Error inesperado - {e}")
            continue

    logging.info(f"Validación completada: {procesados} válidos, {fallidos} inválidos")

    # Fase 3: Carga (simular guardado)
    logging.info("Fase 3: Carga a archivo de salida")
    logging.info(f"Guardando {len(datos_validos)} registros válidos")

    # Resumen final
    logging.info("=== Resumen del Pipeline ===")
    logging.info(f"Total procesados: {len(datos)}")
    logging.info(f"Exitosos: {procesados}")
    logging.info(f"Fallidos: {fallidos}")
    logging.info(f"Outliers detectados: {len(outliers)}")

    if tipos_error:
        logging.info("Errores por tipo:")
        for tipo, cantidad in tipos_error.items():
            logging.info(f"  - {tipo}: {cantidad}")

    # Decisión automática
    tasa_error = fallidos / len(datos)
    logging.info(f"Tasa de error: {tasa_error:.1%}")

    if tasa_error > 0.05:
        logging.critical(
            f"ALERTA: Tasa de error ({tasa_error:.1%}) supera el umbral (5%). "
            f"Revisar calidad de datos urgentemente."
        )
    else:
        logging.info("Pipeline completado exitosamente")

    return {
        'procesados': procesados,
        'fallidos': fallidos,
        'outliers': len(outliers),
        'tasa_error': tasa_error
    }

# Ejecutar pipeline
resultado = pipeline_etl(datos_csv)
print(f"\nResultado: {resultado}")
```

**Explicación**:
- Pipeline completo con 3 fases (Extracción, Transformación, Carga)
- Logging detallado de cada fase
- Contadores de métricas importantes
- Detección de outliers sin fallar
- Resumen completo al final
- Decisión automática basada en tasa de error

---

### Solución Ejercicio 14: Logging con Métricas de Performance

```python
import logging
import time
import random
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Almacenar métricas
metricas = {}

def medir_performance(func):
    """Decorador para medir tiempo de ejecución."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        nombre_func = func.__name__

        # Inicializar lista de tiempos si no existe
        if nombre_func not in metricas:
            metricas[nombre_func] = []

        # Medir tiempo
        inicio = time.time()
        resultado = func(*args, **kwargs)
        tiempo = time.time() - inicio

        # Guardar métrica
        metricas[nombre_func].append(tiempo)

        # Logging según tiempo
        if tiempo > 3.0:
            logging.error(
                f"{nombre_func}() - Tiempo CRÍTICO: {tiempo:.3f}s (>3s)"
            )
        elif tiempo > 1.0:
            logging.warning(
                f"{nombre_func}() - Tiempo LENTO: {tiempo:.3f}s (>1s)"
            )
        else:
            logging.info(
                f"{nombre_func}() - Tiempo OK: {tiempo:.3f}s"
            )

        return resultado

    return wrapper

@medir_performance
def consultar_ventas():
    time.sleep(random.uniform(0.1, 2.0))
    return {"ventas": 1500}

@medir_performance
def consultar_clientes():
    time.sleep(random.uniform(0.5, 3.5))
    return {"clientes": 250}

def mostrar_estadisticas():
    """Muestra estadísticas de performance."""
    logging.info("=== Estadísticas de Performance ===")

    for func_name, tiempos in metricas.items():
        promedio = sum(tiempos) / len(tiempos)
        minimo = min(tiempos)
        maximo = max(tiempos)

        logging.info(f"\n{func_name}():")
        logging.info(f"  - Llamadas: {len(tiempos)}")
        logging.info(f"  - Promedio: {promedio:.3f}s")
        logging.info(f"  - Mínimo: {minimo:.3f}s")
        logging.info(f"  - Máximo: {maximo:.3f}s")

# Ejecutar múltiples veces
logging.info("Iniciando monitoreo de performance...")

for i in range(10):
    logging.info(f"\n--- Iteración {i+1}/10 ---")
    consultar_ventas()
    consultar_clientes()

# Mostrar estadísticas finales
mostrar_estadisticas()
```

**Explicación**:
- Decorador que mide tiempo automáticamente
- Almacena tiempos en diccionario global
- Logging con niveles según tiempo:
  - OK: < 1s (INFO)
  - Lento: 1-3s (WARNING)
  - Crítico: > 3s (ERROR)
- Estadísticas al final: promedio, mínimo, máximo

---

## 📊 Tabla de Autoevaluación

Marca los ejercicios que has completado:

| Ejercicio | Dificultad | Completado | Correcto | Notas |
|-----------|------------|------------|----------|-------|
| 1 - Configuración Básica | ⭐ | [ ] | [ ] | |
| 2 - Niveles Apropiados | ⭐ | [ ] | [ ] | |
| 3 - Logging en Archivo | ⭐ | [ ] | [ ] | |
| 4 - Try-Except con Logging | ⭐ | [ ] | [ ] | |
| 5 - Logging de Progreso | ⭐ | [ ] | [ ] | |
| 6 - Formato Personalizado | ⭐ | [ ] | [ ] | |
| 7 - Múltiples Handlers | ⭐⭐ | [ ] | [ ] | |
| 8 - Rotación por Tamaño | ⭐⭐ | [ ] | [ ] | |
| 9 - Debugging de Datos | ⭐⭐ | [ ] | [ ] | |
| 10 - Logger Reutilizable | ⭐⭐ | [ ] | [ ] | |
| 11 - Logging con Request ID | ⭐⭐ | [ ] | [ ] | |
| 12 - Sistema Enterprise | ⭐⭐⭐ | [ ] | [ ] | |
| 13 - Pipeline Complejo | ⭐⭐⭐ | [ ] | [ ] | |
| 14 - Métricas de Performance | ⭐⭐⭐ | [ ] | [ ] | |

---

## 🎯 Resumen de Conceptos Practicados

### Conceptos Básicos
- ✅ Configuración de logging con `basicConfig()`
- ✅ Uso de niveles apropiados (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ✅ Logging en archivo vs consola
- ✅ Manejo de errores con try-except y logging
- ✅ Logging de progreso en bucles
- ✅ Formato personalizado de mensajes

### Conceptos Intermedios
- ✅ Múltiples handlers (consola + archivo)
- ✅ Rotación de archivos por tamaño (`RotatingFileHandler`)
- ✅ Debugging sistemático de datos problemáticos
- ✅ Creación de loggers reutilizables
- ✅ Trazabilidad con IDs únicos

### Conceptos Avanzados
- ✅ Sistema de logging enterprise
- ✅ Rotación por tiempo (`TimedRotatingFileHandler`)
- ✅ Archivo separado para errores
- ✅ Configuración por variables de entorno
- ✅ Pipeline ETL completo con logging
- ✅ Métricas de performance con decoradores

---

## 📚 Próximo Paso

¡Felicidades por completar los ejercicios! Ahora estás listo para:

1. ✅ Construir el **proyecto práctico** → `04-proyecto-practico/`
2. ✅ Aplicar logging en tus propios proyectos
3. ✅ Continuar con el **Tema 4** del Módulo 1

**Recuerda**: El logging es una habilidad que usarás TODOS los días como Data Engineer. ¡Practica hasta que se vuelva natural!

---

**Última actualización:** 2025-10-18
**Tiempo total estimado:** 2-3 horas
**Autor:** Equipo Pedagógico del Master en Ingeniería de Datos
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
