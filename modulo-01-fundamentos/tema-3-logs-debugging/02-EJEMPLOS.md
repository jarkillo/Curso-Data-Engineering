# Ejemplos Prácticos: Sistema de Logs y Debugging

## 📚 Introducción

En este documento trabajaremos **4 ejemplos completos** de logging y debugging en contextos reales de Data Engineering.

Cada ejemplo incluye:
- ✅ Contexto empresarial realista
- ✅ Código completo paso a paso
- ✅ Explicación detallada de cada decisión
- ✅ Output real del programa
- ✅ Interpretación de resultados
- ✅ Mejores prácticas aplicadas

**Tiempo estimado:** 45-60 minutos

---

## Ejemplo 1: Logger Básico para Pipeline ETL - Nivel: Básico

### Contexto

Trabajas en **DataFlow Industries** y tu primer proyecto es crear un pipeline simple para **RestaurantData Co.** que:
1. Lee un archivo CSV con ventas diarias
2. Calcula el total de ventas
3. Guarda el resultado en un archivo de texto

Tu jefa María te dice: *"Necesito saber qué está pasando en cada paso del pipeline. Si algo falla, quiero saber exactamente dónde y por qué."*

### Objetivo

Implementar logging básico en un pipeline ETL simple.

---

### Paso 1: Código SIN Logging (Problemático)

```python
# pipeline_sin_logs.py
import csv

def procesar_ventas(archivo_csv):
    # Leer CSV
    with open(archivo_csv, 'r') as f:
        reader = csv.DictReader(f)
        ventas = [float(row['monto']) for row in reader]

    # Calcular total
    total = sum(ventas)

    # Guardar resultado
    with open('resultado.txt', 'w') as f:
        f.write(f"Total de ventas: {total}€")

    return total

# Ejecutar
resultado = procesar_ventas('ventas.csv')
print(f"Proceso completado: {resultado}€")
```

**Problemas:**
- ❌ Si falla, no sabes en qué paso
- ❌ No sabes cuántos registros se procesaron
- ❌ No hay registro de cuándo se ejecutó
- ❌ El `print()` desaparece cuando cierras la terminal

---

### Paso 2: Código CON Logging (Profesional)

```python
# pipeline_con_logs.py
import csv
import logging

# Configurar logging (una sola vez al inicio)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def procesar_ventas(archivo_csv):
    logging.info("=== Iniciando pipeline de ventas ===")
    logging.info(f"Archivo de entrada: {archivo_csv}")

    try:
        # Paso 1: Leer CSV
        logging.info("Paso 1: Leyendo archivo CSV...")
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ventas = [float(row['monto']) for row in reader]

        logging.info(f"Leídos {len(ventas)} registros del CSV")

        # Paso 2: Calcular total
        logging.info("Paso 2: Calculando total de ventas...")
        total = sum(ventas)
        logging.info(f"Total calculado: {total:.2f}€")

        # Paso 3: Guardar resultado
        logging.info("Paso 3: Guardando resultado en archivo...")
        with open('resultado.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total de ventas: {total:.2f}€")

        logging.info("Resultado guardado en 'resultado.txt'")
        logging.info("=== Pipeline completado exitosamente ===")

        return total

    except FileNotFoundError as e:
        logging.error(f"Archivo no encontrado: {e}")
        raise
    except KeyError as e:
        logging.error(f"Campo faltante en CSV: {e}")
        raise
    except ValueError as e:
        logging.error(f"Error al convertir monto a número: {e}")
        raise
    except Exception as e:
        logging.critical(f"Error inesperado: {e}")
        raise

# Ejecutar
if __name__ == "__main__":
    resultado = procesar_ventas('ventas.csv')
```

---

### Paso 3: Output del Programa

**Ejecución exitosa:**
```
2025-10-18 10:30:15 - INFO - === Iniciando pipeline de ventas ===
2025-10-18 10:30:15 - INFO - Archivo de entrada: ventas.csv
2025-10-18 10:30:15 - INFO - Paso 1: Leyendo archivo CSV...
2025-10-18 10:30:15 - INFO - Leídos 150 registros del CSV
2025-10-18 10:30:15 - INFO - Paso 2: Calculando total de ventas...
2025-10-18 10:30:15 - INFO - Total calculado: 12,450.75€
2025-10-18 10:30:15 - INFO - Paso 3: Guardando resultado en archivo...
2025-10-18 10:30:15 - INFO - Resultado guardado en 'resultado.txt'
2025-10-18 10:30:15 - INFO - === Pipeline completado exitosamente ===
```

**Ejecución con error (archivo no existe):**
```
2025-10-18 10:35:20 - INFO - === Iniciando pipeline de ventas ===
2025-10-18 10:35:20 - INFO - Archivo de entrada: ventas.csv
2025-10-18 10:35:20 - INFO - Paso 1: Leyendo archivo CSV...
2025-10-18 10:35:20 - ERROR - Archivo no encontrado: [Errno 2] No such file or directory: 'ventas.csv'
```

---

### Interpretación

**Ventajas del código con logging:**

1. **Trazabilidad completa**: Sabes exactamente qué pasó y cuándo
2. **Debugging fácil**: Si falla, sabes en qué paso (Paso 1, 2 o 3)
3. **Métricas útiles**: Sabes cuántos registros se procesaron
4. **Errores claros**: Los errores se registran con contexto
5. **Profesional**: Cualquier Data Engineer entendería este código

**Decisiones de diseño:**

- Usamos `INFO` para el flujo normal (no es debugging, es información útil)
- Usamos `ERROR` para errores recuperables
- Usamos `CRITICAL` para errores inesperados
- Incluimos el número de registros procesados (métrica importante)
- Formato claro con timestamp

---

## Ejemplo 2: Logging en Archivo con Rotación - Nivel: Intermedio

### Contexto

**CloudAPI Systems** tiene un servicio que procesa requests de API 24/7. Necesitan:
- Logs guardados en archivos (no solo en consola)
- Rotación automática cuando el archivo alcanza 5 MB
- Mantener los últimos 10 archivos de log
- Logs en consola para desarrollo, en archivo para producción

### Objetivo

Configurar un sistema de logging profesional con rotación de archivos.

---

### Paso 1: Estructura del Logger

```python
# api_service.py
import logging
from logging.handlers import RotatingFileHandler
import time

def configurar_logger():
    """
    Configura un logger con:
    - Handler de consola (para desarrollo)
    - Handler de archivo con rotación (para producción)
    """
    # Crear logger
    logger = logging.getLogger('cloudapi_service')
    logger.setLevel(logging.DEBUG)  # Captura TODO

    # Formato común para ambos handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler 1: Consola (solo INFO y superior)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler 2: Archivo con rotación (DEBUG y superior)
    file_handler = RotatingFileHandler(
        filename='cloudapi_service.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=10,  # Mantener 10 archivos
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Añadir handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Crear logger global
logger = configurar_logger()
```

---

### Paso 2: Usar el Logger en el Servicio

```python
def procesar_request(request_id, endpoint, params):
    """
    Procesa un request de API y registra toda la información relevante.
    """
    logger.info(f"[Request {request_id}] Iniciando procesamiento")
    logger.debug(f"[Request {request_id}] Endpoint: {endpoint}")
    logger.debug(f"[Request {request_id}] Parámetros: {params}")

    inicio = time.time()

    try:
        # Simular procesamiento
        if endpoint == '/api/ventas':
            resultado = procesar_ventas(params)
        elif endpoint == '/api/clientes':
            resultado = procesar_clientes(params)
        else:
            logger.warning(f"[Request {request_id}] Endpoint desconocido: {endpoint}")
            return {"error": "Endpoint no encontrado"}

        # Calcular tiempo de respuesta
        tiempo_respuesta = time.time() - inicio
        logger.info(f"[Request {request_id}] Completado en {tiempo_respuesta:.3f}s")

        # Alertar si es muy lento
        if tiempo_respuesta > 1.0:
            logger.warning(
                f"[Request {request_id}] Respuesta lenta: {tiempo_respuesta:.3f}s "
                f"(esperado < 1s)"
            )

        return resultado

    except ValueError as e:
        logger.error(f"[Request {request_id}] Parámetros inválidos: {e}")
        return {"error": "Parámetros inválidos"}

    except Exception as e:
        logger.exception(f"[Request {request_id}] Error inesperado")
        return {"error": "Error interno del servidor"}

def procesar_ventas(params):
    """Simula procesamiento de ventas."""
    logger.debug("Consultando base de datos de ventas...")
    time.sleep(0.5)  # Simular trabajo
    return {"ventas": 1500, "total": 45000.50}

def procesar_clientes(params):
    """Simula procesamiento de clientes."""
    logger.debug("Consultando base de datos de clientes...")
    time.sleep(0.3)  # Simular trabajo
    return {"clientes": 250, "activos": 180}
```

---

### Paso 3: Simular Tráfico de Requests

```python
def simular_trafico():
    """
    Simula múltiples requests para demostrar el logging.
    """
    logger.info("=== Servicio CloudAPI iniciado ===")
    logger.info("Configuración: Rotación 5MB, 10 backups")

    requests = [
        (1, '/api/ventas', {'fecha': '2025-10-18'}),
        (2, '/api/clientes', {'activos': True}),
        (3, '/api/productos', {}),  # Endpoint no existe
        (4, '/api/ventas', {'fecha': 'invalid'}),  # Error
        (5, '/api/clientes', {'activos': True}),
    ]

    for request_id, endpoint, params in requests:
        resultado = procesar_request(request_id, endpoint, params)
        logger.debug(f"[Request {request_id}] Resultado: {resultado}")
        time.sleep(0.1)  # Pequeña pausa entre requests

    logger.info("=== Servicio detenido ===")

if __name__ == "__main__":
    simular_trafico()
```

---

### Paso 4: Output del Programa

**En consola (solo INFO y superior):**
```
2025-10-18 11:15:30 - cloudapi_service - INFO - === Servicio CloudAPI iniciado ===
2025-10-18 11:15:30 - cloudapi_service - INFO - Configuración: Rotación 5MB, 10 backups
2025-10-18 11:15:30 - cloudapi_service - INFO - [Request 1] Iniciando procesamiento
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 1] Completado en 0.502s
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 2] Iniciando procesamiento
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 2] Completado en 0.301s
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 3] Iniciando procesamiento
2025-10-18 11:15:31 - cloudapi_service - WARNING - [Request 3] Endpoint desconocido: /api/productos
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 4] Iniciando procesamiento
2025-10-18 11:15:31 - cloudapi_service - ERROR - [Request 4] Parámetros inválidos: Fecha inválida
2025-10-18 11:15:32 - cloudapi_service - INFO - [Request 5] Iniciando procesamiento
2025-10-18 11:15:32 - cloudapi_service - INFO - [Request 5] Completado en 0.303s
2025-10-18 11:15:32 - cloudapi_service - INFO - === Servicio detenido ===
```

**En archivo `cloudapi_service.log` (incluye DEBUG):**
```
2025-10-18 11:15:30 - cloudapi_service - INFO - === Servicio CloudAPI iniciado ===
2025-10-18 11:15:30 - cloudapi_service - INFO - Configuración: Rotación 5MB, 10 backups
2025-10-18 11:15:30 - cloudapi_service - INFO - [Request 1] Iniciando procesamiento
2025-10-18 11:15:30 - cloudapi_service - DEBUG - [Request 1] Endpoint: /api/ventas
2025-10-18 11:15:30 - cloudapi_service - DEBUG - [Request 1] Parámetros: {'fecha': '2025-10-18'}
2025-10-18 11:15:30 - cloudapi_service - DEBUG - Consultando base de datos de ventas...
2025-10-18 11:15:31 - cloudapi_service - INFO - [Request 1] Completado en 0.502s
2025-10-18 11:15:31 - cloudapi_service - DEBUG - [Request 1] Resultado: {'ventas': 1500, 'total': 45000.5}
...
```

---

### Interpretación

**Ventajas de esta configuración:**

1. **Doble destino**: Consola para desarrollo, archivo para auditoría
2. **Niveles diferentes**: DEBUG en archivo (detalle completo), INFO en consola (menos ruido)
3. **Rotación automática**: No hay archivos gigantes
4. **Request ID**: Puedes rastrear un request específico en los logs
5. **Métricas de performance**: Tiempo de respuesta de cada request

**Decisiones de diseño:**

- `[Request {id}]` en cada log permite filtrar por request específico
- DEBUG incluye parámetros (útil para debugging, pero no en consola)
- WARNING para endpoints desconocidos (no es error fatal, pero debe investigarse)
- `logger.exception()` captura el stack trace completo

**Estructura de archivos después de rotación:**
```
cloudapi_service.log         ← Archivo actual
cloudapi_service.log.1       ← Backup 1 (más reciente)
cloudapi_service.log.2       ← Backup 2
...
cloudapi_service.log.10      ← Backup 10 (más antiguo)
```

---

## Ejemplo 3: Debugging de Pipeline con Datos Problemáticos - Nivel: Intermedio

### Contexto

**RestaurantData Co.** te reporta que su pipeline de procesamiento de ventas falla aleatoriamente. El pipeline procesa 10,000 registros diarios y a veces falla en el registro 3,456, otras veces en el 7,892.

Tu tarea: Usar logging para identificar qué registros causan problemas y por qué.

---

### Paso 1: Pipeline Original (Sin Debugging)

```python
# pipeline_original.py
import csv

def procesar_ventas_v1(archivo):
    with open(archivo, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            precio = float(row['precio'])
            cantidad = int(row['cantidad'])
            total = precio * cantidad
            # ... guardar en base de datos

    return "Completado"

# Este código falla pero no sabes dónde ni por qué
```

---

### Paso 2: Pipeline con Logging Estratégico

```python
# pipeline_con_debugging.py
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_debug.log'),
        logging.StreamHandler()
    ]
)

def procesar_ventas_v2(archivo):
    """
    Versión mejorada con logging detallado para debugging.
    """
    logger = logging.getLogger(__name__)

    logger.info(f"Iniciando procesamiento de {archivo}")

    registros_procesados = 0
    registros_con_error = 0
    errores_por_tipo = {}

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader, start=1):
                try:
                    # Log cada 1000 registros para seguimiento de progreso
                    if i % 1000 == 0:
                        logger.info(f"Progreso: {i} registros procesados")

                    # Validar y procesar
                    precio = float(row['precio'])
                    cantidad = int(row['cantidad'])

                    # Validaciones de negocio
                    if precio < 0:
                        raise ValueError(f"Precio negativo: {precio}")
                    if cantidad <= 0:
                        raise ValueError(f"Cantidad inválida: {cantidad}")

                    total = precio * cantidad

                    # Log de registros sospechosos (sin fallar)
                    if total > 10000:
                        logger.warning(
                            f"Registro {i}: Total muy alto ({total:.2f}€) - "
                            f"Precio: {precio}€, Cantidad: {cantidad}"
                        )

                    registros_procesados += 1

                except ValueError as e:
                    registros_con_error += 1
                    tipo_error = type(e).__name__
                    errores_por_tipo[tipo_error] = errores_por_tipo.get(tipo_error, 0) + 1

                    logger.error(
                        f"Registro {i}: Error de validación - {e}"
                    )
                    logger.debug(f"Registro {i}: Datos completos: {row}")

                    # Continuar con el siguiente registro (no fallar todo)
                    continue

                except Exception as e:
                    registros_con_error += 1
                    logger.exception(f"Registro {i}: Error inesperado")
                    logger.debug(f"Registro {i}: Datos completos: {row}")
                    continue

        # Resumen final
        logger.info("=== Resumen del Procesamiento ===")
        logger.info(f"Total de registros: {registros_procesados + registros_con_error}")
        logger.info(f"Procesados exitosamente: {registros_procesados}")
        logger.info(f"Con errores: {registros_con_error}")

        if errores_por_tipo:
            logger.info("Errores por tipo:")
            for tipo, cantidad in errores_por_tipo.items():
                logger.info(f"  - {tipo}: {cantidad}")

        # Decidir si el pipeline fue exitoso
        tasa_error = registros_con_error / (registros_procesados + registros_con_error)
        if tasa_error > 0.05:  # Más del 5% de errores
            logger.critical(
                f"Tasa de error muy alta: {tasa_error:.2%}. "
                f"Revisar calidad de datos."
            )

        return {
            'procesados': registros_procesados,
            'errores': registros_con_error,
            'tasa_error': tasa_error
        }

    except FileNotFoundError:
        logger.critical(f"Archivo no encontrado: {archivo}")
        raise
    except Exception as e:
        logger.exception("Error crítico en el pipeline")
        raise
```

---

### Paso 3: Datos de Prueba con Problemas

```python
# crear_datos_prueba.py
import csv

# Crear archivo CSV con datos problemáticos
datos = [
    {'id': 1, 'precio': '45.50', 'cantidad': '2'},      # OK
    {'id': 2, 'precio': '78.20', 'cantidad': '1'},      # OK
    {'id': 3, 'precio': 'N/A', 'cantidad': '3'},        # ERROR: precio no numérico
    {'id': 4, 'precio': '125.00', 'cantidad': '5'},     # OK
    {'id': 5, 'precio': '34.80', 'cantidad': '0'},      # ERROR: cantidad inválida
    {'id': 6, 'precio': '-10.00', 'cantidad': '2'},     # ERROR: precio negativo
    {'id': 7, 'precio': '5000.00', 'cantidad': '3'},    # WARNING: total muy alto
    {'id': 8, 'precio': '89.90', 'cantidad': '1'},      # OK
]

with open('ventas_test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'precio', 'cantidad'])
    writer.writeheader()
    writer.writerows(datos)

print("Archivo de prueba creado: ventas_test.csv")
```

---

### Paso 4: Ejecutar y Analizar Logs

```python
# ejecutar_pipeline.py
if __name__ == "__main__":
    resultado = procesar_ventas_v2('ventas_test.csv')
    print(f"\nResultado: {resultado}")
```

**Output:**
```
2025-10-18 14:20:10 - INFO - Iniciando procesamiento de ventas_test.csv
2025-10-18 14:20:10 - ERROR - Registro 3: Error de validación - could not convert string to float: 'N/A'
2025-10-18 14:20:10 - ERROR - Registro 5: Error de validación - Cantidad inválida: 0
2025-10-18 14:20:10 - ERROR - Registro 6: Error de validación - Precio negativo: -10.0
2025-10-18 14:20:10 - WARNING - Registro 7: Total muy alto (15000.00€) - Precio: 5000.0€, Cantidad: 3
2025-10-18 14:20:10 - INFO - === Resumen del Procesamiento ===
2025-10-18 14:20:10 - INFO - Total de registros: 8
2025-10-18 14:20:10 - INFO - Procesados exitosamente: 5
2025-10-18 14:20:10 - INFO - Con errores: 3
2025-10-18 14:20:10 - INFO - Errores por tipo:
2025-10-18 14:20:10 - INFO -   - ValueError: 3

Resultado: {'procesados': 5, 'errores': 3, 'tasa_error': 0.375}
```

---

### Interpretación

**Qué descubrimos con el logging:**

1. **Registro 3**: Campo 'precio' tiene valor 'N/A' (no numérico)
2. **Registro 5**: Cantidad es 0 (inválido para una venta)
3. **Registro 6**: Precio negativo (error de datos)
4. **Registro 7**: Venta de 15,000€ (sospechoso pero válido)

**Ventajas de este enfoque:**

- ✅ **No falla todo el pipeline**: Procesa lo que puede, registra lo que falla
- ✅ **Identificación exacta**: Sabes qué registro (número de línea) tiene problemas
- ✅ **Resumen útil**: Estadísticas de éxito/error al final
- ✅ **Alertas inteligentes**: WARNING para valores sospechosos pero válidos
- ✅ **Decisión automática**: Si >5% errores, alerta crítica

**Acciones a tomar:**

1. Contactar a RestaurantData Co. sobre calidad de datos
2. Implementar validación en la fuente (antes del pipeline)
3. Decidir si rechazar todo el lote o procesar lo válido

---

## Ejemplo 4: Logging en Producción con Rotación por Tiempo - Nivel: Avanzado

### Contexto

**LogisticFlow** tiene un servicio que corre 24/7 procesando entregas. Necesitan:
- Logs separados por día (un archivo por día)
- Mantener logs de los últimos 30 días
- Diferentes niveles de log según el entorno (dev/prod)
- Logs estructurados para análisis posterior

### Objetivo

Configurar un sistema de logging enterprise-grade con rotación por tiempo.

---

### Paso 1: Configuración Avanzada del Logger

```python
# logger_config.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

class LogisticFlowLogger:
    """
    Configuración centralizada de logging para LogisticFlow.
    """

    def __init__(self, nombre_servicio, nivel_log=None):
        self.nombre_servicio = nombre_servicio
        self.logger = logging.getLogger(nombre_servicio)

        # Determinar nivel según entorno
        entorno = os.getenv('ENTORNO', 'desarrollo')
        if nivel_log is None:
            nivel_log = self._obtener_nivel_por_entorno(entorno)

        self.logger.setLevel(nivel_log)

        # Evitar duplicación de handlers
        if not self.logger.handlers:
            self._configurar_handlers(entorno)

    def _obtener_nivel_por_entorno(self, entorno):
        """
        Niveles de log según entorno:
        - desarrollo: DEBUG (todo)
        - testing: INFO (flujo general)
        - produccion: WARNING (solo problemas)
        """
        niveles = {
            'desarrollo': logging.DEBUG,
            'testing': logging.INFO,
            'produccion': logging.WARNING
        }
        return niveles.get(entorno, logging.INFO)

    def _configurar_handlers(self, entorno):
        """Configura handlers según el entorno."""

        # Formato detallado para archivos
        formato_archivo = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Formato simple para consola
        formato_consola = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # Handler 1: Consola (siempre activo en desarrollo)
        if entorno == 'desarrollo':
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formato_consola)
            self.logger.addHandler(console_handler)

        # Handler 2: Archivo con rotación diaria
        file_handler = TimedRotatingFileHandler(
            filename=f'logs/{self.nombre_servicio}.log',
            when='midnight',  # Rotar a medianoche
            interval=1,  # Cada 1 día
            backupCount=30,  # Mantener 30 días
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato_archivo)
        file_handler.suffix = "%Y-%m-%d"  # Formato de fecha en nombre archivo
        self.logger.addHandler(file_handler)

        # Handler 3: Archivo separado para ERRORES críticos
        error_handler = TimedRotatingFileHandler(
            filename=f'logs/{self.nombre_servicio}_errors.log',
            when='midnight',
            interval=1,
            backupCount=90,  # Mantener errores 90 días
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formato_archivo)
        error_handler.suffix = "%Y-%m-%d"
        self.logger.addHandler(error_handler)

    def get_logger(self):
        """Retorna el logger configurado."""
        return self.logger
```

---

### Paso 2: Servicio de Procesamiento de Entregas

```python
# servicio_entregas.py
import time
from datetime import datetime
import random

# Crear directorio de logs si no existe
import os
os.makedirs('logs', exist_ok=True)

# Configurar logger
logger_config = LogisticFlowLogger('servicio_entregas')
logger = logger_config.get_logger()

class ServicioEntregas:
    """
    Servicio que procesa entregas en tiempo real.
    """

    def __init__(self):
        logger.info("=== Servicio de Entregas Iniciado ===")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info(f"Entorno: {os.getenv('ENTORNO', 'desarrollo')}")
        self.entregas_procesadas = 0
        self.entregas_fallidas = 0

    def procesar_entrega(self, entrega_id, destino, paquetes):
        """
        Procesa una entrega individual.
        """
        logger.info(f"[Entrega {entrega_id}] Iniciando procesamiento")
        logger.debug(f"[Entrega {entrega_id}] Destino: {destino}, Paquetes: {paquetes}")

        inicio = time.time()

        try:
            # Validar datos
            if not destino:
                raise ValueError("Destino no puede estar vacío")
            if paquetes <= 0:
                raise ValueError(f"Cantidad de paquetes inválida: {paquetes}")

            # Simular procesamiento
            tiempo_procesamiento = random.uniform(0.1, 0.5)
            time.sleep(tiempo_procesamiento)

            # Simular fallo aleatorio (5% de probabilidad)
            if random.random() < 0.05:
                raise Exception("Error de conexión con sistema de GPS")

            # Calcular ruta
            distancia_km = random.uniform(5, 50)
            tiempo_estimado_min = distancia_km * 2  # 2 min por km

            logger.info(
                f"[Entrega {entrega_id}] Ruta calculada: {distancia_km:.1f}km, "
                f"Tiempo estimado: {tiempo_estimado_min:.0f}min"
            )

            # Alertar si es muy lejos
            if distancia_km > 40:
                logger.warning(
                    f"[Entrega {entrega_id}] Distancia muy larga: {distancia_km:.1f}km"
                )

            tiempo_total = time.time() - inicio
            logger.info(
                f"[Entrega {entrega_id}] Procesada exitosamente en {tiempo_total:.3f}s"
            )

            self.entregas_procesadas += 1
            return {
                'entrega_id': entrega_id,
                'distancia_km': distancia_km,
                'tiempo_estimado_min': tiempo_estimado_min,
                'estado': 'procesada'
            }

        except ValueError as e:
            self.entregas_fallidas += 1
            logger.error(f"[Entrega {entrega_id}] Datos inválidos: {e}")
            return {'entrega_id': entrega_id, 'estado': 'error', 'motivo': str(e)}

        except Exception as e:
            self.entregas_fallidas += 1
            logger.exception(f"[Entrega {entrega_id}] Error crítico")
            return {'entrega_id': entrega_id, 'estado': 'error', 'motivo': 'Error interno'}

    def procesar_lote(self, entregas):
        """
        Procesa un lote de entregas.
        """
        logger.info(f"Procesando lote de {len(entregas)} entregas")

        resultados = []
        for entrega in entregas:
            resultado = self.procesar_entrega(
                entrega['id'],
                entrega['destino'],
                entrega['paquetes']
            )
            resultados.append(resultado)

        # Resumen del lote
        logger.info("=== Resumen del Lote ===")
        logger.info(f"Total: {len(entregas)}")
        logger.info(f"Exitosas: {self.entregas_procesadas}")
        logger.info(f"Fallidas: {self.entregas_fallidas}")

        tasa_exito = self.entregas_procesadas / len(entregas) if entregas else 0
        logger.info(f"Tasa de éxito: {tasa_exito:.1%}")

        if tasa_exito < 0.95:
            logger.critical(
                f"Tasa de éxito baja ({tasa_exito:.1%}). "
                f"Revisar sistema urgentemente."
            )

        return resultados

    def detener(self):
        """Detiene el servicio limpiamente."""
        logger.info("=== Servicio de Entregas Detenido ===")
        logger.info(f"Entregas procesadas: {self.entregas_procesadas}")
        logger.info(f"Entregas fallidas: {self.entregas_fallidas}")
```

---

### Paso 3: Simular Operación del Servicio

```python
# main.py
def main():
    # Simular diferentes entornos
    # os.environ['ENTORNO'] = 'produccion'  # Descomentar para prod

    servicio = ServicioEntregas()

    # Lote de entregas de prueba
    entregas = [
        {'id': 'E001', 'destino': 'Madrid Centro', 'paquetes': 3},
        {'id': 'E002', 'destino': 'Barcelona Norte', 'paquetes': 1},
        {'id': 'E003', 'destino': '', 'paquetes': 2},  # Error: destino vacío
        {'id': 'E004', 'destino': 'Valencia Sur', 'paquetes': 5},
        {'id': 'E005', 'destino': 'Sevilla Este', 'paquetes': 0},  # Error: paquetes inválidos
        {'id': 'E006', 'destino': 'Bilbao Oeste', 'paquetes': 2},
        {'id': 'E007', 'destino': 'Málaga Centro', 'paquetes': 4},
        {'id': 'E008', 'destino': 'Zaragoza Norte', 'paquetes': 1},
    ]

    resultados = servicio.procesar_lote(entregas)

    servicio.detener()

    return resultados

if __name__ == "__main__":
    main()
```

---

### Paso 4: Estructura de Archivos de Log Generados

Después de varios días de operación:

```
logs/
├── servicio_entregas.log                    ← Logs de hoy
├── servicio_entregas.log.2025-10-17         ← Logs de ayer
├── servicio_entregas.log.2025-10-16         ← Logs de anteayer
├── ...
├── servicio_entregas.log.2025-09-18         ← Logs de hace 30 días
├── servicio_entregas_errors.log             ← Errores de hoy
├── servicio_entregas_errors.log.2025-10-17  ← Errores de ayer
└── ...
```

---

### Interpretación

**Ventajas de esta configuración enterprise:**

1. **Rotación por tiempo**: Un archivo por día, fácil de encontrar logs de una fecha específica
2. **Retención configurable**: 30 días logs normales, 90 días errores (cumplimiento legal)
3. **Archivo separado de errores**: Fácil revisar solo problemas críticos
4. **Configuración por entorno**: Automáticamente ajusta nivel según dev/test/prod
5. **Información de contexto**: Incluye archivo y línea de código en logs de archivo
6. **Formato diferente**: Detallado en archivo, simple en consola

**Mejores prácticas aplicadas:**

- ✅ Logger centralizado (clase reutilizable)
- ✅ Configuración por variables de entorno
- ✅ Formato estructurado (fácil de parsear con herramientas)
- ✅ Separación de errores críticos
- ✅ Resumen de métricas al final del lote

**Uso en producción:**

```bash
# Desarrollo (logs detallados en consola)
python main.py

# Producción (solo warnings/errors, todo en archivo)
export ENTORNO=produccion
python main.py
```

---

## 📊 Resumen de Ejemplos

| Ejemplo | Nivel | Concepto Principal | Caso de Uso |
|---------|-------|-------------------|-------------|
| **1** | Básico | Logging básico vs print() | Pipeline ETL simple |
| **2** | Intermedio | Múltiples handlers + rotación por tamaño | Servicio API 24/7 |
| **3** | Intermedio | Debugging con logs estratégicos | Pipeline con datos problemáticos |
| **4** | Avanzado | Rotación por tiempo + configuración por entorno | Servicio enterprise en producción |

---

## 🎯 Patrones Comunes Aprendidos

### 1. Estructura de Logs en Pipelines ETL

```python
logger.info("=== Iniciando Pipeline ===")
logger.info("Fase 1: Extracción")
# ... código ...
logger.info("Fase 2: Transformación")
# ... código ...
logger.info("Fase 3: Carga")
# ... código ...
logger.info("=== Pipeline Completado ===")
```

### 2. Logging de Progreso en Bucles Grandes

```python
for i, item in enumerate(items, start=1):
    if i % 1000 == 0:  # Cada 1000
        logger.info(f"Progreso: {i}/{len(items)}")
```

### 3. Logging de Errores con Contexto

```python
try:
    operacion()
except Exception as e:
    logger.exception(f"Error en operacion() con parámetros: {params}")
```

### 4. Resumen de Métricas al Final

```python
logger.info("=== Resumen ===")
logger.info(f"Procesados: {exitosos}")
logger.info(f"Errores: {fallidos}")
logger.info(f"Tasa de éxito: {tasa:.1%}")
```

---

## 📚 Próximo Paso

Ahora que has visto ejemplos completos:

1. ✅ Practica con **ejercicios guiados** → `03-EJERCICIOS.md`
2. ✅ Construye el **proyecto práctico** → `04-proyecto-practico/`

**¡Estos patrones los usarás en todos tus proyectos de Data Engineering!**

---

**Última actualización:** 2025-10-18
**Duración de lectura:** 45-60 minutos
**Autor:** Equipo Pedagógico del Master en Ingeniería de Datos
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
