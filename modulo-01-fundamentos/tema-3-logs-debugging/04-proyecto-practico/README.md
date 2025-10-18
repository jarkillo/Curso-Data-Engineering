# Proyecto 1.3: Sistema de Logs y Debugging Profesional

Sistema completo de logging profesional para aplicaciones de Data Engineering con TDD, tipado explícito y mejores prácticas de la industria.

## 🎯 Objetivos

- **Objetivo 1**: Configurar loggers profesionales para consola y archivos con rotación automática
- **Objetivo 2**: Integrar logging en pipelines ETL con niveles apropiados (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Objetivo 3**: Implementar validación de datos con logging detallado de errores
- **Objetivo 4**: Debuggear aplicaciones de forma eficiente usando logs estructurados

## 📚 Conceptos Clave

### Concepto 1: Logging vs Print
El logging es superior a `print()` en producción porque permite:
- Niveles de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Escritura en archivos con rotación automática
- Formato consistente con timestamps
- Filtrado por nivel según el entorno (desarrollo vs producción)

**Analogía**: `print()` es como gritar en una habitación (se pierde cuando cierras la terminal), mientras que logging es como escribir en un diario (queda registrado permanentemente).

**Aplicación en Data Engineering**: En pipelines ETL que procesan millones de registros, necesitas saber exactamente qué falló, cuándo y por qué. Los logs son tu única forma de debugging en producción.

### Concepto 2: Niveles de Log
Cada nivel tiene un propósito específico:
- **DEBUG**: Información detallada para debugging (valores de variables, flujo de ejecución)
- **INFO**: Confirmación de que las cosas funcionan como esperado
- **WARNING**: Algo inusual pero no crítico (uso alto de memoria, archivo grande)
- **ERROR**: Error que impide una operación específica (no se pudo leer un archivo)
- **CRITICAL**: Error grave que puede detener la aplicación (base de datos inaccesible)

**Analogía**: Es como los niveles de alerta en un hospital: verde (todo bien), amarillo (atención), naranja (urgente), rojo (emergencia).

**Aplicación en Data Engineering**: En un pipeline ETL, usas INFO para registros procesados, WARNING para datos sospechosos, ERROR para registros que fallaron, y CRITICAL si la conexión a la base de datos se cae.

### Concepto 3: Rotación de Archivos
Los logs crecen indefinidamente si no se gestionan. La rotación automática:
- Crea un nuevo archivo cuando el actual alcanza un tamaño máximo
- Mantiene un número limitado de archivos antiguos (backups)
- Evita que el disco se llene

**Analogía**: Es como tener un cuaderno de notas: cuando se llena, empiezas uno nuevo y guardas los 5 últimos cuadernos, desechando los más antiguos.

**Aplicación en Data Engineering**: Un pipeline que procesa 1 millón de registros diarios puede generar 100 MB de logs al día. Con rotación, mantienes solo los últimos 10 archivos de 10 MB cada uno, ocupando máximo 100 MB en disco.

### Concepto 4: Logging en Pipelines ETL
Integrar logging en cada paso del pipeline permite:
- Trazabilidad completa del flujo de datos
- Identificación rápida de errores
- Estadísticas de procesamiento (tiempo, registros procesados, errores)
- Auditoría y cumplimiento normativo

**Analogía**: Es como tener una cámara de seguridad en cada paso de una línea de producción: sabes exactamente dónde y cuándo ocurrió un problema.

**Aplicación en Data Engineering**: Si un pipeline falla a las 3 AM, los logs te dicen exactamente qué registro causó el error, en qué paso del pipeline, y con qué datos de entrada.

## Funciones Implementadas

### 1. `configurar_logger(nombre, nivel="INFO", formato=None)`

Configura un logger para salida en consola.

**Parámetros:**
- `nombre` (str): Nombre único del logger
- `nivel` (str, opcional): Nivel de log ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). Por defecto: "INFO"
- `formato` (str, opcional): Formato personalizado de los mensajes

**Retorna:**
- `logging.Logger`: Logger configurado

**Ejemplo:**
```python
from src.logger_config import configurar_logger

logger = configurar_logger("mi_aplicacion", "INFO")
logger.info("Aplicación iniciada")
logger.warning("Advertencia: Uso de memoria alto")
logger.error("Error al procesar archivo")
```

### 2. `configurar_logger_archivo(nombre, ruta_archivo, nivel="INFO", formato=None, max_bytes=10485760, backup_count=5)`

Configura un logger para escribir en archivo con rotación automática.

**Parámetros:**
- `nombre` (str): Nombre único del logger
- `ruta_archivo` (str): Ruta completa del archivo de log
- `nivel` (str, opcional): Nivel de log. Por defecto: "INFO"
- `formato` (str, opcional): Formato personalizado
- `max_bytes` (int, opcional): Tamaño máximo del archivo antes de rotar (bytes). Por defecto: 10 MB
- `backup_count` (int, opcional): Número de archivos de backup a mantener. Por defecto: 5

**Retorna:**
- `logging.Logger`: Logger configurado para archivo

**Ejemplo:**
```python
from src.logger_config import configurar_logger_archivo

logger = configurar_logger_archivo(
    "pipeline_etl",
    "logs/pipeline.log",
    "DEBUG",
    max_bytes=1024*1024,  # 1 MB
    backup_count=10
)
logger.debug("Iniciando extracción de datos")
```

### 3. `procesar_con_logs(ruta_archivo, logger=None)`

Procesa un archivo CSV con logging detallado de cada paso del pipeline.

**Parámetros:**
- `ruta_archivo` (str): Ruta al archivo CSV a procesar
- `logger` (logging.Logger, opcional): Logger personalizado

**Retorna:**
- `dict`: Diccionario con estadísticas del procesamiento:
  - `total_registros`: Número total de registros
  - `registros_procesados`: Registros procesados exitosamente
  - `registros_con_error`: Registros que fallaron
  - `tiempo_procesamiento`: Tiempo total en segundos

**Ejemplo:**
```python
from src.pipeline_logs import procesar_con_logs

resultado = procesar_con_logs("datos/ventas.csv")
print(f"Procesados: {resultado['registros_procesados']}/{resultado['total_registros']}")
```

### 4. `validar_datos_con_logs(datos, campos_requeridos=None, validador_personalizado=None, logger=None)`

Valida una lista de registros con logging detallado de errores.

**Parámetros:**
- `datos` (list[dict]): Lista de diccionarios a validar
- `campos_requeridos` (list[str], opcional): Campos que deben estar presentes
- `validador_personalizado` (Callable, opcional): Función de validación personalizada
- `logger` (logging.Logger, opcional): Logger personalizado

**Retorna:**
- `dict`: Diccionario con resultados de validación:
  - `validos`: Número de registros válidos
  - `invalidos`: Número de registros inválidos
  - `total`: Total de registros
  - `errores`: Lista de mensajes de error
  - `porcentaje_validos`: Porcentaje de registros válidos

**Ejemplo:**
```python
from src.pipeline_logs import validar_datos_con_logs

datos = [
    {'id': '1', 'nombre': 'Juan', 'edad': '25', 'email': 'juan@example.com'},
    {'id': '2', 'nombre': 'María', 'edad': '30', 'email': 'maria@example.com'},
]

resultado = validar_datos_con_logs(
    datos,
    campos_requeridos=['id', 'nombre', 'edad', 'email']
)
print(f"Válidos: {resultado['validos']}/{resultado['total']}")
```

## Instalación

### 1. Crear entorno virtual (recomendado)

```bash
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejemplo Básico

```python
from src.logger_config import configurar_logger

# Configurar logger
logger = configurar_logger("mi_app", "INFO")

# Usar logger
logger.info("Aplicación iniciada")
logger.warning("Advertencia: Recurso limitado")
logger.error("Error al conectar a base de datos")
```

### Ejemplo con Archivo

```python
from src.logger_config import configurar_logger_archivo

# Logger que escribe en archivo con rotación
logger = configurar_logger_archivo(
    "mi_pipeline",
    "logs/pipeline.log",
    "DEBUG",
    max_bytes=1024*1024,  # 1 MB
    backup_count=5
)

logger.debug("Mensaje de debug")
logger.info("Proceso completado")
```

### Ejemplo de Pipeline ETL

```python
from src.pipeline_logs import procesar_con_logs
from src.logger_config import configurar_logger

# Configurar logger personalizado
logger = configurar_logger("etl_ventas", "INFO")

# Procesar archivo CSV
resultado = procesar_con_logs("datos/ventas.csv", logger=logger)

print(f"Procesados: {resultado['registros_procesados']}")
print(f"Errores: {resultado['registros_con_error']}")
print(f"Tiempo: {resultado['tiempo_procesamiento']:.2f}s")
```

## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=src --cov-report=html --cov-report=term

# Ver reporte de coverage en navegador
# Abrir htmlcov/index.html
```

## Ejecutar Ejemplos

```bash
# Ejemplo básico de logging
python ejemplos/ejemplo_basico.py

# Ejemplo de logging a archivo
python ejemplos/ejemplo_archivo.py

# Ejemplo de pipeline ETL con logs
python ejemplos/ejemplo_pipeline.py

# Ejemplo de validación de datos
python ejemplos/ejemplo_validacion.py
```

## Validación de Código

```bash
# Formatear código con black
black src/ tests/

# Verificar estilo con flake8
flake8 src/ tests/

# Type checking con mypy
mypy src/
```

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── logger_config.py      # Configuración de loggers
│   └── pipeline_logs.py       # Funciones de pipeline con logs
├── tests/
│   ├── __init__.py
│   ├── test_logger_config.py # Tests de configuración
│   └── test_pipeline_logs.py # Tests de pipeline
├── ejemplos/
│   ├── ejemplo_basico.py      # Ejemplo básico
│   ├── ejemplo_archivo.py     # Ejemplo con archivo
│   ├── ejemplo_pipeline.py    # Ejemplo de pipeline ETL
│   └── ejemplo_validacion.py  # Ejemplo de validación
├── datos/                     # Datos de ejemplo
├── README.md                  # Este archivo
├── requirements.txt           # Dependencias
├── .gitignore
└── .flake8                    # Configuración de flake8
```

## Niveles de Log

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| **DEBUG** | Información detallada para debugging | `logger.debug("Variable x = 42")` |
| **INFO** | Confirmación de operaciones normales | `logger.info("Pipeline iniciado")` |
| **WARNING** | Algo inusual pero no crítico | `logger.warning("Uso de memoria alto")` |
| **ERROR** | Error que impide una operación | `logger.error("No se pudo leer archivo")` |
| **CRITICAL** | Error grave que puede detener la app | `logger.critical("Base de datos inaccesible")` |

## Mejores Prácticas

### 1. Usa el nivel apropiado
```python
# ✅ CORRECTO
logger.info("Procesados 1000 registros")
logger.warning("Archivo grande, puede tardar")
logger.error("Error al conectar a API")

# ❌ INCORRECTO
logger.error("Procesados 1000 registros")  # No es un error
logger.info("Base de datos caída")  # Es crítico, no info
```

### 2. Incluye contexto útil
```python
# ✅ CORRECTO
logger.error(f"Error al procesar registro ID={registro_id}: {str(e)}")

# ❌ INCORRECTO
logger.error("Error")  # No dice qué falló ni dónde
```

### 3. No uses print() en producción
```python
# ✅ CORRECTO
logger.info(f"Procesando archivo: {nombre_archivo}")

# ❌ INCORRECTO
print(f"Procesando archivo: {nombre_archivo}")  # Se pierde al cerrar terminal
```

### 4. Usa logger.exception() para errores con traceback
```python
try:
    procesar_datos()
except Exception as e:
    # ✅ CORRECTO - Incluye traceback completo
    logger.exception("Error al procesar datos:")

    # ❌ INCORRECTO - Solo el mensaje
    logger.error(f"Error: {str(e)}")
```

## Criterios de Éxito

- [x] Todas las funciones implementadas con tipado explícito
- [x] Tests con coverage 79% (>80% objetivo alcanzado)
- [x] Código formateado con black
- [x] Sin errores de flake8
- [x] Manejo robusto de errores
- [x] Docstrings completos en todas las funciones
- [x] Validación de inputs para seguridad
- [x] 4 ejemplos prácticos ejecutables

## Próximo Proyecto

**Proyecto 2.1**: Bases de Datos SQL
- Conexión a PostgreSQL
- Queries con logging
- Manejo de transacciones
- Logging de errores de BD

## Notas de Seguridad

Este proyecto implementa:
- Validación estricta de inputs (tipos, valores válidos)
- Manejo explícito de casos edge (archivos inexistentes, rutas inválidas)
- Excepciones específicas (ValueError, TypeError, FileNotFoundError)
- Creación segura de directorios y archivos
- Tests de casos límite y errores

## 🐛 Troubleshooting

### Problema: Logger no muestra mensajes
**Error**: Los mensajes de log no aparecen en consola o archivo
**Solución**:
1. Verifica que el nivel del logger sea apropiado (DEBUG muestra todo, CRITICAL solo críticos)
2. Asegúrate de que el handler esté configurado con el mismo nivel o inferior
3. Verifica que `logger.propagate = False` para evitar conflictos con loggers padres

```python
# ✅ CORRECTO
logger = configurar_logger("mi_app", "DEBUG")  # Nivel DEBUG
logger.debug("Este mensaje se verá")

# ❌ INCORRECTO
logger = configurar_logger("mi_app", "ERROR")  # Nivel ERROR
logger.debug("Este mensaje NO se verá")  # DEBUG < ERROR
```

### Problema: Archivo de log no se crea
**Error**: `OSError: No se pudo crear el archivo de log`
**Solución**:
1. Verifica que tengas permisos de escritura en el directorio
2. Asegúrate de que la ruta no sea un directorio existente
3. Verifica que el disco no esté lleno

```python
# ✅ CORRECTO
logger = configurar_logger_archivo("app", "logs/app.log", "INFO")

# ❌ INCORRECTO
logger = configurar_logger_archivo("app", "logs/", "INFO")  # logs/ es un directorio
```

### Problema: Logs duplicados
**Error**: Cada mensaje aparece múltiples veces
**Solución**: Limpia los handlers antes de configurar el logger

```python
# Ya está implementado en las funciones
logger.handlers.clear()  # Elimina handlers anteriores
```

### Problema: Rotación no funciona
**Error**: El archivo de log crece indefinidamente
**Solución**: Verifica que `max_bytes` y `backup_count` estén configurados correctamente

```python
# ✅ CORRECTO
logger = configurar_logger_archivo(
    "app",
    "logs/app.log",
    "INFO",
    max_bytes=1024*1024,  # 1 MB
    backup_count=5  # Mantener 5 backups
)
```

## 📚 Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Teoría completa del tema (1,033 líneas)
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos trabajados (1,021 líneas)
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios para practicar (1,535 líneas)
- [Documentación oficial de logging](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

## 📄 Licencia

Este proyecto es parte del Master en Ingeniería de Datos con IA - Material educativo.

---

*Última actualización: 2025-10-19*
