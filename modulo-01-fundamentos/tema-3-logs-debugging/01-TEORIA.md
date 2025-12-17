# Tema 3: Sistema de Logs y Debugging Profesional

## 📚 ¿Qué Aprenderás en Este Tema?

Al finalizar este tema serás capaz de:
- ✅ Entender qué son los logs y por qué son fundamentales en Data Engineering
- ✅ Usar el módulo `logging` de Python de forma profesional
- ✅ Configurar diferentes niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ✅ Crear logs que se escriben en archivos con rotación automática
- ✅ Debuggear código de forma eficiente
- ✅ Implementar logging en pipelines ETL reales
- ✅ Seguir mejores prácticas de logging en producción

**Duración estimada:** 1-2 semanas
**Nivel:** Principiante (no se requiere conocimiento previo)

---

## 🎯 ¿Por Qué Logs en Data Engineering?

### El Problema: Código que Falla en Producción

Imagina esta situación (basada en casos reales):

**Escenario:**
```python
# Tu pipeline ETL que procesa 1 millón de registros
def procesar_ventas():
    datos = extraer_de_api()
    datos_limpios = limpiar_datos(datos)
    cargar_a_base_datos(datos_limpios)
    print("✓ Proceso completado")
```

**A las 3 AM del domingo:**
```
📧 Email de alerta: "El pipeline falló"
```

**Tú (medio dormido):**
- ¿En qué paso falló? 🤔
- ¿Qué registro causó el error? 🤔
- ¿Cuántos registros se procesaron antes del fallo? 🤔
- ¿Fue un error de red, de datos, o de lógica? 🤔

**Sin logs:** No tienes respuestas. Debes ejecutar todo de nuevo y esperar que falle otra vez.

**Con logs:**
```
2025-10-18 03:15:23 - INFO - Iniciando extracción de API
2025-10-18 03:15:45 - INFO - Extraídos 1,000,000 registros
2025-10-18 03:16:12 - INFO - Iniciando limpieza de datos
2025-10-18 03:18:34 - INFO - Procesados 856,432 registros
2025-10-18 03:18:35 - ERROR - Error en registro ID=856433: campo 'precio' tiene valor 'N/A'
2025-10-18 03:18:35 - ERROR - Tipo de error: ValueError
2025-10-18 03:18:35 - INFO - Pipeline detenido. Registros procesados: 856,432/1,000,000
```

**Ahora sabes:**
- ✅ Falló en la limpieza de datos (no en extracción o carga)
- ✅ El registro problemático es el ID=856433
- ✅ El problema es un campo 'precio' con valor 'N/A'
- ✅ Se procesaron 856,432 registros exitosamente antes del error

**Puedes arreglarlo en 5 minutos** en lugar de 2 horas de debugging.

---

## 🔍 ¿Qué Son Los Logs?

### Definición Simple

Un **log** es un mensaje que tu programa escribe para contar qué está haciendo.

**Analogía: El Diario de un Barco**

Imagina un barco navegando. El capitán escribe en el diario de navegación:

```
08:00 - Zarpamos del puerto de Barcelona
10:30 - Velocidad: 15 nudos, Viento: 20 km/h NE
12:00 - Avistado banco de peces, desviación 5° norte
14:30 - ⚠️ Motor principal presenta vibración anormal
15:00 - Motor detenido para inspección
15:45 - Problema resuelto: filtro de combustible obstruido
16:00 - Motor reiniciado, velocidad normal
```

Si el barco se hunde, el diario cuenta **qué pasó y cuándo**.

Los logs de tu programa hacen lo mismo:
- Registran qué hace el programa
- Cuándo lo hace
- Si algo sale mal, qué falló

---

## 🚫 Print vs Logging: ¿Por Qué NO Usar `print()`?

### El Problema con `print()`

Muchos principiantes hacen esto:

```python
def procesar_archivo(archivo):
    print("Leyendo archivo...")
    datos = leer_csv(archivo)
    print(f"Leídos {len(datos)} registros")

    print("Validando datos...")
    datos_validos = validar(datos)
    print(f"Válidos: {len(datos_validos)}")

    print("Guardando en base de datos...")
    guardar(datos_validos)
    print("✓ Proceso completado")
```

**Problemas:**

1. **No se guarda en ningún lado**
   ```
   Los prints aparecen en la consola y desaparecen
   Si el programa se ejecuta en un servidor, no los ves
   ```

2. **No tiene niveles de importancia**
   ```
   ¿"Leyendo archivo..." es igual de importante que un ERROR?
   No puedes filtrar mensajes importantes
   ```

3. **No tiene timestamp**
   ```
   ¿Cuándo pasó cada cosa?
   No lo sabes
   ```

4. **No es profesional**
   ```
   En producción, nadie usa print()
   Es como usar una calculadora en lugar de Excel
   ```

### La Solución: Logging

```python
import logging

def procesar_archivo(archivo):
    logging.info("Leyendo archivo...")
    datos = leer_csv(archivo)
    logging.info(f"Leídos {len(datos)} registros")

    logging.info("Validando datos...")
    datos_validos = validar(datos)
    logging.info(f"Válidos: {len(datos_validos)}")

    logging.info("Guardando en base de datos...")
    guardar(datos_validos)
    logging.info("Proceso completado exitosamente")
```

**Ventajas:**
- ✅ Se guarda en archivos automáticamente
- ✅ Incluye timestamp
- ✅ Tiene niveles (INFO, WARNING, ERROR)
- ✅ Se puede configurar (activar/desactivar, cambiar formato)
- ✅ Es el estándar profesional

---

## 📊 Parte 1: Niveles de Log

Los logs tienen **5 niveles de importancia**, de menos a más grave:

### 1. DEBUG (Nivel 10)

**¿Qué es?**
Información muy detallada, útil solo para debugging.

**¿Cuándo usar?**
Cuando estás desarrollando o debuggeando un problema específico.

**Ejemplo:**
```python
logging.debug("Variable x tiene valor: 42")
logging.debug("Entrando en función calcular_media()")
logging.debug("Iteración 5 del bucle, valor actual: 123")
```

**En producción:** Normalmente DESACTIVADO (genera demasiado ruido).

---

### 2. INFO (Nivel 20)

**¿Qué es?**
Información general sobre el flujo del programa.

**¿Cuándo usar?**
Para confirmar que las cosas funcionan como se espera.

**Ejemplo:**
```python
logging.info("Iniciando extracción de datos de API")
logging.info("Procesados 1,000 registros")
logging.info("Pipeline completado exitosamente")
```

**En producción:** ACTIVADO. Es el nivel por defecto.

---

### 3. WARNING (Nivel 30)

**¿Qué es?**
Algo inesperado pasó, pero el programa puede continuar.

**¿Cuándo usar?**
Cuando algo no es ideal pero no es un error fatal.

**Ejemplo:**
```python
logging.warning("API respondió lento (2.5s), reintentando...")
logging.warning("Encontrados 5 registros duplicados, eliminando...")
logging.warning("Uso de memoria al 85%, considerar optimización")
```

**En producción:** ACTIVADO. Indica problemas potenciales.

---

### 4. ERROR (Nivel 40)

**¿Qué es?**
Algo falló, pero el programa puede continuar (quizás procesando otros datos).

**¿Cuándo usar?**
Cuando una operación específica falla pero no quieres detener todo el programa.

**Ejemplo:**
```python
logging.error("Error al procesar registro ID=12345: campo 'precio' vacío")
logging.error("No se pudo conectar a la base de datos, reintentando...")
logging.error("Archivo 'ventas.csv' no encontrado, saltando...")
```

**En producción:** ACTIVADO. Requiere atención.

---

### 5. CRITICAL (Nivel 50)

**¿Qué es?**
Error grave que impide que el programa continúe.

**¿Cuándo usar?**
Cuando el programa debe detenerse porque no puede continuar.

**Ejemplo:**
```python
logging.critical("No se pudo conectar a la base de datos después de 5 intentos")
logging.critical("Archivo de configuración crítico no encontrado")
logging.critical("Memoria insuficiente para continuar")
```

**En producción:** ACTIVADO. Alerta inmediata al equipo.

---

### Tabla Resumen de Niveles

| Nivel | Valor | Cuándo Usar | Ejemplo | En Producción |
|-------|-------|-------------|---------|---------------|
| **DEBUG** | 10 | Debugging detallado | "Variable x = 42" | ❌ Desactivado |
| **INFO** | 20 | Flujo normal | "Procesados 1000 registros" | ✅ Activado |
| **WARNING** | 30 | Algo inesperado | "API lenta, reintentando" | ✅ Activado |
| **ERROR** | 40 | Fallo recuperable | "Registro inválido, saltando" | ✅ Activado |
| **CRITICAL** | 50 | Fallo fatal | "No se puede continuar" | ✅ Activado |

---

## 🛠️ Parte 2: Configuración Básica de Logging

### 2.1 Configuración Mínima

```python
import logging

# Configuración básica (una sola vez al inicio del programa)
logging.basicConfig(level=logging.INFO)

# Ahora puedes usar logging en cualquier parte
logging.info("Este es un mensaje INFO")
logging.warning("Este es un WARNING")
logging.error("Este es un ERROR")
```

**Output:**
```
INFO:root:Este es un mensaje INFO
WARNING:root:Este es un WARNING
ERROR:root:Este es un ERROR
```

---

### 2.2 Configuración con Formato Personalizado

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Pipeline iniciado")
```

**Output:**
```
2025-10-18 14:30:45 - INFO - Pipeline iniciado
```

**Explicación del formato:**
- `%(asctime)s`: Fecha y hora
- `%(levelname)s`: Nivel (INFO, WARNING, etc.)
- `%(message)s`: Tu mensaje

---

### 2.3 Guardar Logs en Archivo

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pipeline.log',  # ← Guarda en archivo
    filemode='a'  # 'a' = append (añadir), 'w' = overwrite (sobrescribir)
)

logging.info("Este mensaje se guarda en pipeline.log")
```

**Resultado:** Se crea el archivo `pipeline.log`:
```
2025-10-18 14:30:45 - INFO - Este mensaje se guarda en pipeline.log
```

---

### 2.4 Logs en Consola Y Archivo (Ambos)

```python
import logging

# Crear logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Handler para archivo
file_handler = logging.FileHandler('pipeline.log')
file_handler.setLevel(logging.INFO)

# Formato
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Añadir handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Usar el logger
logger.info("Este mensaje aparece en consola Y en archivo")
```

---

## 🔄 Parte 3: Rotación de Archivos de Log

### 3.1 El Problema: Archivos de Log Gigantes

Imagina que tu pipeline se ejecuta cada hora, 24/7:

```
pipeline.log
Día 1: 10 MB
Día 2: 20 MB
Día 3: 30 MB
...
Día 30: 300 MB
Día 365: 3.6 GB  ← ¡Archivo enorme!
```

**Problemas:**
- Difícil de abrir (editores de texto se congelan)
- Ocupa mucho espacio en disco
- Difícil de buscar información específica

**Solución:** Rotación automática de archivos.

---

### 3.2 RotatingFileHandler: Rotación por Tamaño

```python
import logging
from logging.handlers import RotatingFileHandler

# Crear logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler con rotación por tamaño
handler = RotatingFileHandler(
    'pipeline.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5  # Mantener 5 archivos de backup
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Usar el logger
logger.info("Mensaje de log")
```

**¿Qué hace?**

Cuando `pipeline.log` alcanza 1 MB:
1. Renombra `pipeline.log` → `pipeline.log.1`
2. Renombra `pipeline.log.1` → `pipeline.log.2`
3. Renombra `pipeline.log.2` → `pipeline.log.3`
4. Renombra `pipeline.log.3` → `pipeline.log.4`
5. Renombra `pipeline.log.4` → `pipeline.log.5`
6. Elimina `pipeline.log.5` (el más antiguo)
7. Crea un nuevo `pipeline.log` vacío

**Resultado:**
```
pipeline.log      ← Archivo actual (más reciente)
pipeline.log.1    ← Backup 1
pipeline.log.2    ← Backup 2
pipeline.log.3    ← Backup 3
pipeline.log.4    ← Backup 4
pipeline.log.5    ← Backup 5 (más antiguo)
```

---

### 3.3 TimedRotatingFileHandler: Rotación por Tiempo

```python
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Rotar cada día a medianoche
handler = TimedRotatingFileHandler(
    'pipeline.log',
    when='midnight',  # Rotar a medianoche
    interval=1,  # Cada 1 día
    backupCount=30  # Mantener 30 días de logs
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Mensaje de log")
```

**Opciones de `when`:**
- `'S'`: Segundos
- `'M'`: Minutos
- `'H'`: Horas
- `'D'`: Días
- `'midnight'`: A medianoche
- `'W0'` - `'W6'`: Día de la semana (0=Lunes, 6=Domingo)

**Resultado:**
```
pipeline.log                    ← Logs de hoy
pipeline.log.2025-10-17         ← Logs de ayer
pipeline.log.2025-10-16         ← Logs de anteayer
...
pipeline.log.2025-09-18         ← Logs de hace 30 días
```

---

## 🐛 Parte 4: Debugging Profesional

### 4.1 ¿Qué es Debugging?

**Debugging** es el proceso de encontrar y corregir errores (bugs) en tu código.

**Analogía: Doctor Diagnosticando**

Imagina que vas al doctor:
- ❌ **Mal doctor:** "Tienes algo malo, toma esta pastilla"
- ✅ **Buen doctor:** "Vamos a hacer pruebas, medir tu temperatura, presión, análisis de sangre..."

Debugging es lo mismo:
- ❌ **Mal debugging:** Cambiar código al azar hasta que funcione
- ✅ **Buen debugging:** Investigar sistemáticamente qué está pasando

---

### 4.2 Técnicas de Debugging

#### Técnica 1: Logs Estratégicos

```python
def calcular_descuento(precio, porcentaje):
    logging.debug(f"Entrada: precio={precio}, porcentaje={porcentaje}")

    descuento = precio * (porcentaje / 100)
    logging.debug(f"Descuento calculado: {descuento}")

    precio_final = precio - descuento
    logging.debug(f"Precio final: {precio_final}")

    return precio_final
```

**Ventaja:** Ves el flujo de datos sin detener el programa.

---

#### Técnica 2: Try-Except con Logging

```python
def procesar_registro(registro):
    try:
        precio = float(registro['precio'])
        cantidad = int(registro['cantidad'])
        total = precio * cantidad
        return total
    except KeyError as e:
        logging.error(f"Campo faltante en registro: {e}")
        logging.error(f"Registro completo: {registro}")
        return None
    except ValueError as e:
        logging.error(f"Error de conversión: {e}")
        logging.error(f"Registro: {registro}")
        return None
```

**Ventaja:** Capturas el error Y registras información útil para debuggear.

---

#### Técnica 3: Logging de Excepciones Completas

```python
import logging

try:
    resultado = operacion_compleja()
except Exception as e:
    logging.exception("Error en operacion_compleja()")
    # logging.exception() registra el error Y el stack trace completo
```

**Output:**
```
ERROR - Error en operacion_compleja()
Traceback (most recent call last):
  File "pipeline.py", line 45, in operacion_compleja
    valor = 10 / 0
ZeroDivisionError: division by zero
```

---

### 4.3 Debugging en Pipelines ETL

**Caso Real: Pipeline que Procesa 1 Millón de Registros**

```python
def procesar_ventas(registros):
    logger.info(f"Iniciando procesamiento de {len(registros)} registros")

    procesados = 0
    errores = 0

    for i, registro in enumerate(registros):
        try:
            # Procesar registro
            resultado = procesar_registro(registro)
            procesados += 1

            # Log cada 10,000 registros (no cada uno, sería demasiado)
            if (i + 1) % 10000 == 0:
                logger.info(f"Progreso: {i+1}/{len(registros)} registros")

        except Exception as e:
            errores += 1
            logger.error(f"Error en registro {i}: {e}")
            logger.debug(f"Registro problemático: {registro}")

            # Si hay demasiados errores, detener
            if errores > 100:
                logger.critical(f"Demasiados errores ({errores}), deteniendo pipeline")
                break

    logger.info(f"Procesamiento completado: {procesados} exitosos, {errores} errores")
```

**Ventajas:**
- ✅ Sabes el progreso en tiempo real
- ✅ Registras errores sin detener todo el proceso
- ✅ Tienes información para debuggear después

---

## 📋 Parte 5: Mejores Prácticas de Logging

### 5.1 ¿Qué Loggear?

#### ✅ SÍ Loggear:

1. **Inicio y fin de procesos importantes**
   ```python
   logging.info("Iniciando extracción de datos")
   # ... código ...
   logging.info("Extracción completada: 10,000 registros")
   ```

2. **Progreso en operaciones largas**
   ```python
   logging.info(f"Procesados {i}/{total} registros")
   ```

3. **Errores y excepciones**
   ```python
   logging.error(f"Error al procesar registro {id}: {error}")
   ```

4. **Decisiones importantes del programa**
   ```python
   logging.warning("Cache no disponible, usando API directamente")
   ```

5. **Información de configuración al inicio**
   ```python
   logging.info(f"Conectando a base de datos: {DB_HOST}")
   logging.info(f"Nivel de log configurado: {LOG_LEVEL}")
   ```

#### ❌ NO Loggear:

1. **Información sensible**
   ```python
   # ❌ MAL
   logging.info(f"Password: {password}")
   logging.info(f"Token de API: {api_token}")

   # ✅ BIEN
   logging.info("Autenticación exitosa")
   ```

2. **Datos personales (GDPR)**
   ```python
   # ❌ MAL
   logging.info(f"Usuario: {email}, Tarjeta: {card_number}")

   # ✅ BIEN
   logging.info(f"Usuario: {hash(email)}, Pago procesado")
   ```

3. **Cada iteración de un bucle grande**
   ```python
   # ❌ MAL (genera millones de logs)
   for i in range(1000000):
       logging.info(f"Procesando registro {i}")

   # ✅ BIEN (log cada 10,000)
   for i in range(1000000):
       if i % 10000 == 0:
           logging.info(f"Progreso: {i}/1000000")
   ```

---

### 5.2 Formato de Mensajes

#### ✅ Buenos Mensajes:

```python
# Descriptivo y con contexto
logging.info("Extracción de API completada: 10,000 registros en 2.5s")

# Incluye IDs para rastrear
logging.error(f"Error al procesar pedido ID={pedido_id}: stock insuficiente")

# Incluye valores relevantes
logging.warning(f"API lenta: {tiempo_respuesta}s (esperado < 1s)")
```

#### ❌ Malos Mensajes:

```python
# Demasiado vago
logging.info("Proceso completado")  # ¿Qué proceso?

# Sin contexto
logging.error("Error")  # ¿Qué error? ¿Dónde?

# Demasiado técnico
logging.info("Exception in thread Thread-1")  # ¿Qué significa?
```

---

### 5.3 Niveles de Log en Diferentes Entornos

| Entorno | Nivel Recomendado | Razón |
|---------|-------------------|-------|
| **Desarrollo** | DEBUG | Quieres ver TODO para debuggear |
| **Testing** | INFO | Quieres ver el flujo general |
| **Staging** | INFO | Similar a producción pero con más detalle |
| **Producción** | WARNING | Solo lo importante (reduce ruido) |

**Configuración por entorno:**

```python
import os

# Leer nivel de log de variable de entorno
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

**Uso:**
```bash
# Desarrollo
export LOG_LEVEL=DEBUG
python pipeline.py

# Producción
export LOG_LEVEL=WARNING
python pipeline.py
```

---

## 🏢 Parte 6: Casos de Uso Reales

### Caso 1: Pipeline ETL en CloudAPI Systems

**Contexto:**
CloudAPI Systems necesita un pipeline que extraiga datos de su API, los transforme y los cargue en una base de datos.

**Código con Logging:**

```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logger
logger = logging.getLogger('pipeline_cloudapi')
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    'pipeline_cloudapi.log',
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def ejecutar_pipeline():
    logger.info("=== Iniciando Pipeline CloudAPI ===")

    try:
        # Extracción
        logger.info("Fase 1: Extracción de datos de API")
        datos = extraer_de_api()
        logger.info(f"Extraídos {len(datos)} registros de la API")

        # Transformación
        logger.info("Fase 2: Transformación de datos")
        datos_transformados = transformar_datos(datos)
        logger.info(f"Transformados {len(datos_transformados)} registros")

        # Carga
        logger.info("Fase 3: Carga a base de datos")
        registros_cargados = cargar_a_db(datos_transformados)
        logger.info(f"Cargados {registros_cargados} registros a la base de datos")

        logger.info("=== Pipeline completado exitosamente ===")

    except Exception as e:
        logger.critical(f"Pipeline falló: {e}")
        logger.exception("Stack trace completo:")
        raise
```

---

### Caso 2: Detección de Anomalías en RestaurantData Co.

**Contexto:**
RestaurantData Co. quiere detectar ventas anormalmente altas o bajas.

```python
def detectar_anomalias(ventas):
    logger.info(f"Analizando {len(ventas)} registros de ventas")

    media = calcular_media(ventas)
    desviacion = calcular_desviacion_estandar(ventas)

    logger.info(f"Media de ventas: {media:.2f}€")
    logger.info(f"Desviación estándar: {desviacion:.2f}€")

    umbral_superior = media + 2 * desviacion
    umbral_inferior = media - 2 * desviacion

    anomalias = 0
    for venta in ventas:
        if venta > umbral_superior:
            anomalias += 1
            logger.warning(f"Venta anormalmente ALTA: {venta}€ (umbral: {umbral_superior:.2f}€)")
        elif venta < umbral_inferior:
            anomalias += 1
            logger.warning(f"Venta anormalmente BAJA: {venta}€ (umbral: {umbral_inferior:.2f}€)")

    logger.info(f"Análisis completado: {anomalias} anomalías detectadas")
```

---

## ⚠️ Errores Comunes y Cómo Evitarlos

### Error 1: Configurar `basicConfig()` Múltiples Veces

```python
# ❌ MAL
import logging

def funcion_a():
    logging.basicConfig(level=logging.INFO)
    logging.info("Mensaje A")

def funcion_b():
    logging.basicConfig(level=logging.DEBUG)  # ← No hace nada!
    logging.debug("Mensaje B")  # ← No aparece
```

**Problema:** `basicConfig()` solo funciona la primera vez que se llama.

**Solución:** Configurar una sola vez al inicio del programa.

```python
# ✅ BIEN
import logging

# Al inicio del programa (una sola vez)
logging.basicConfig(level=logging.INFO)

def funcion_a():
    logging.info("Mensaje A")

def funcion_b():
    logging.debug("Mensaje B")
```

---

### Error 2: Loggear en Bucles Grandes

```python
# ❌ MAL (genera 1 millón de logs)
for i in range(1000000):
    logging.info(f"Procesando registro {i}")
```

**Solución:** Log cada N iteraciones.

```python
# ✅ BIEN
for i in range(1000000):
    if i % 10000 == 0:  # Cada 10,000
        logging.info(f"Progreso: {i}/1,000,000")
```

---

### Error 3: No Usar `logging.exception()` en Excepciones

```python
# ❌ MAL (pierdes el stack trace)
try:
    operacion()
except Exception as e:
    logging.error(f"Error: {e}")
```

**Solución:** Usar `logging.exception()`.

```python
# ✅ BIEN
try:
    operacion()
except Exception as e:
    logging.exception("Error en operacion()")
    # Registra el error Y el stack trace completo
```

---

### Error 4: Loggear Información Sensible

```python
# ❌ MAL
logging.info(f"Usuario {email} inició sesión con password {password}")
```

**Solución:** Nunca loggear passwords, tokens, datos personales.

```python
# ✅ BIEN
logging.info(f"Usuario {hash(email)} inició sesión exitosamente")
```

---

## ✅ Resumen del Tema

### Conceptos Clave

| Concepto | Qué es | Para qué sirve |
|----------|---------|----------------|
| **Log** | Mensaje que el programa escribe | Saber qué está pasando |
| **Niveles** | DEBUG, INFO, WARNING, ERROR, CRITICAL | Filtrar por importancia |
| **Handler** | Destino del log (consola, archivo) | Controlar dónde se guardan |
| **Formatter** | Formato del mensaje | Personalizar apariencia |
| **Rotación** | Dividir logs en múltiples archivos | Evitar archivos gigantes |

### Niveles de Log

| Nivel | Cuándo Usar | Ejemplo |
|-------|-------------|---------|
| DEBUG | Debugging detallado | "Variable x = 42" |
| INFO | Flujo normal | "Pipeline iniciado" |
| WARNING | Algo inesperado | "API lenta" |
| ERROR | Fallo recuperable | "Registro inválido" |
| CRITICAL | Fallo fatal | "No se puede continuar" |

### Mejores Prácticas

✅ **SÍ hacer:**
- Configurar logging al inicio del programa
- Usar niveles apropiados
- Incluir contexto en los mensajes
- Rotar archivos de log
- Usar `logging.exception()` en try-except

❌ **NO hacer:**
- Usar `print()` en lugar de logging
- Loggear información sensible
- Loggear en cada iteración de bucles grandes
- Configurar `basicConfig()` múltiples veces

---

## 🎯 Checklist de Aprendizaje

Antes de continuar a los ejemplos y ejercicios, verifica que entiendes:

- [ ] Puedo explicar por qué logging es mejor que `print()`
- [ ] Entiendo los 5 niveles de log y cuándo usar cada uno
- [ ] Sé configurar logging básico con `basicConfig()`
- [ ] Entiendo qué es un Handler y un Formatter
- [ ] Sé cómo rotar archivos de log por tamaño o tiempo
- [ ] Entiendo cómo usar logging para debugging
- [ ] Conozco las mejores prácticas de logging

---

## 📚 Próximo Paso

Ahora que entiendes la teoría, es momento de:

1. ✅ Ver **ejemplos trabajados** paso a paso → `02-EJEMPLOS.md`
2. ✅ Practicar con **ejercicios guiados** → `03-EJERCICIOS.md`
3. ✅ Construir el **proyecto práctico** → `04-proyecto-practico/`

**¡El logging es una habilidad esencial!** Todos los Data Engineers profesionales lo usan a diario.

---

## 📖 Recursos Adicionales

### Documentación Oficial
- [Logging HOWTO (Python Docs)](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

### Artículos Recomendados
- [The Hitchhiker's Guide to Python - Logging](https://docs.python-guide.org/writing/logging/)
- [Real Python - Logging in Python](https://realpython.com/python-logging/)

### Videos (si existen)
- Buscar "Python logging tutorial" en YouTube
- Buscar "Python logging best practices"

---

**Última actualización:** 2025-10-18
**Duración de lectura:** 35-50 minutos
**Autor:** Equipo Pedagógico del Master en Ingeniería de Datos
---

## 🧭 Navegación

⬅️ **Anterior**: [Procesamiento CSV - Proyecto Práctico](../tema-2-procesamiento-csv/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
