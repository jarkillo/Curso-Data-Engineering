# Introducción a Apache Airflow

**Tiempo de lectura:** 35-40 minutos
**Nivel:** Principiante absoluto
**Prerequisitos:** Conocimientos básicos de Python (variables, funciones, if/else)

> **⚠️ IMPORTANTE - Prerequisito de Docker:**
> Este tema requiere **Docker y Docker Compose** instalados y funcionando en tu sistema.
> Airflow se ejecuta como un conjunto de servicios (webserver, scheduler, base de datos)
> que se gestionan fácilmente con Docker Compose.
>
> **Si aún no tienes Docker:**
> - **Windows/Mac**: Instala [Docker Desktop](https://www.docker.com/products/docker-desktop)
> - **Linux**: Sigue la [guía oficial de Docker](https://docs.docker.com/engine/install/)
>
> **Verifica tu instalación** ejecutando:
> ```bash
> docker --version
> docker-compose --version
> ```
>
> Si necesitas ayuda, consulta `documentacion/GUIA_INSTALACION.md` en este repositorio.

---

## 📋 Índice

1. [¿Qué es Apache Airflow y por qué existe?](#qué-es-apache-airflow-y-por-qué-existe)
2. [Conceptos Fundamentales](#conceptos-fundamentales)
3. [Instalación y Configuración con Docker](#instalación-y-configuración-con-docker)
4. [Tu Primer DAG: "Hola Mundo"](#tu-primer-dag-hola-mundo)
5. [Operators Básicos](#operators-básicos)
6. [Dependencias entre Tasks](#dependencias-entre-tasks)
7. [Schedule Intervals: Cuándo Ejecutar](#schedule-intervals-cuándo-ejecutar)
8. [Mejores Prácticas](#mejores-prácticas)
9. [Errores Comunes](#errores-comunes)
10. [Checklist de Aprendizaje](#checklist-de-aprendizaje)

---

## ¿Qué es Apache Airflow y por qué existe?

### El Problema Real

Imagina que trabajas en una empresa de e-commerce y cada mañana a las 6 AM necesitas:

1. **Descargar** las ventas del día anterior desde la base de datos
2. **Limpiar** los datos (eliminar duplicados, corregir errores)
3. **Calcular** métricas (total de ventas, productos más vendidos)
4. **Generar** un reporte en Excel
5. **Enviar** el reporte por email al equipo de marketing

¿Cómo lo harías?

**Opción 1: Manual** 😓
Todos los días a las 6 AM, ejecutar 5 scripts de Python uno por uno. ¿Qué pasa si uno falla? ¿Qué pasa si te vas de vacaciones? ¿Qué pasa si el paso 3 depende del paso 2?

**Opción 2: Cron jobs** 🤔
Usar cron (programador de tareas de Linux) para ejecutar cada script. Mejor, pero:
- ¿Cómo manejas dependencias? (El paso 3 debe esperar al paso 2)
- ¿Cómo ves si algo falló?
- ¿Cómo reintentas si algo sale mal?
- ¿Cómo lo monitoreas?

**Opción 3: Apache Airflow** ✨
Una herramienta diseñada específicamente para este problema.

---

### La Analogía del Director de Orquesta

Piensa en Airflow como el **director de una orquesta**:

- **Tú eres el compositor**: Defines qué instrumentos tocan, en qué orden y cuándo
- **Airflow es el director**: Se asegura de que cada músico (script) toque en el momento correcto
- **Los músicos son tus scripts de Python**: Cada uno hace una tarea específica
- **La partitura es el DAG**: El plan maestro que define todo

Si un músico comete un error, el director puede pedirle que repita esa parte (reintentos automáticos). Si un músico termina su solo, el director señala al siguiente (dependencias). Todo está coordinado y bajo control.

---

### ¿Por Qué Airflow en Data Engineering?

En Data Engineering, constantemente necesitas:

**Pipelines ETL (Extract, Transform, Load)**:
- Extraer datos de APIs, bases de datos, archivos
- Transformar esos datos (limpiar, agregar, calcular)
- Cargar resultados en un data warehouse

**Workflows complejos**:
- Entrenar modelos de Machine Learning cada semana
- Generar reportes diarios para diferentes equipos
- Sincronizar datos entre sistemas cada hora
- Hacer backups de bases de datos cada noche

**Problemas que Airflow resuelve**:
- ✅ **Orquestación**: Ejecutar tareas en el orden correcto
- ✅ **Programación**: Ejecutar automáticamente a horas específicas
- ✅ **Monitoreo**: Ver qué está ejecutándose y qué falló
- ✅ **Reintentos**: Intentar de nuevo si algo falla
- ✅ **Alertas**: Notificarte si algo sale mal
- ✅ **Paralelización**: Ejecutar tareas simultáneamente cuando es posible
- ✅ **Visualización**: Ver tu workflow como un gráfico

---

## Conceptos Fundamentales

Antes de escribir código, necesitas entender 6 conceptos clave. Vamos a explicar cada uno con analogías simples.

### 1. DAG (Directed Acyclic Graph)

**Definición técnica**: Un gráfico dirigido acíclico que representa un flujo de trabajo.

**Definición simple**: Una receta de cocina con pasos ordenados.

**Analogía: Hacer un Pastel** 🎂

```
Comprar ingredientes
    ↓
Mezclar harina, huevos, azúcar
    ↓
Hornear
    ↓
Decorar
```

**Características clave**:

1. **Directed (Dirigido)**: Las flechas tienen dirección. No puedes hornear antes de mezclar.
2. **Acyclic (Acíclico)**: No hay ciclos infinitos. No puedes decorar, luego hornear, luego decorar otra vez en el mismo pastel.
3. **Graph (Gráfico)**: Es un diagrama visual de pasos conectados.

**En Airflow**:
- Cada receta es un DAG
- Cada paso (comprar, mezclar, hornear) es una **Task**
- Las flechas son las **dependencias**

**Por qué "acíclico" importa**:
Imagina si pudieras hacer esto:
```
Hornear → Decorar → Hornear → Decorar → Hornear → ...
```
¡Nunca terminarías! Airflow no permite esto.

---

### 2. Task (Tarea)

**Definición**: Un solo paso ejecutable en tu workflow.

**Analogía**: Un solo paso de la receta de cocina.

**Ejemplos de Tasks en Data Engineering**:
- "Descargar archivo CSV de un servidor FTP"
- "Ejecutar una consulta SQL en PostgreSQL"
- "Entrenar un modelo de Machine Learning"
- "Enviar un email con el reporte generado"

**Características de una buena Task**:
1. **Hace una sola cosa**: "Descargar archivo" (no "descargar y procesar y enviar")
2. **Es idempotente**: Si la ejecutas 10 veces con los mismos datos, obtienes el mismo resultado
3. **Tiene entrada y salida claras**: Sabes qué recibe y qué produce

**Ejemplo visual**:
```
Task: "Calcular total de ventas"
Entrada: ventas.csv
Salida: total = 25000
```

---

### 3. Operator (Operador)

**Definición**: El tipo de tarea que quieres ejecutar.

**Analogía**: El tipo de herramienta de cocina que usas.

En la cocina:
- **Batidora**: Para mezclar ingredientes
- **Horno**: Para hornear
- **Cuchillo**: Para cortar
- **Sartén**: Para freír

En Airflow:
- **PythonOperator**: Ejecuta una función de Python
- **BashOperator**: Ejecuta un comando de shell (bash)
- **PostgresOperator**: Ejecuta una consulta SQL
- **EmailOperator**: Envía un email

**Ejemplo práctico**:

Si quieres ejecutar esta función Python:
```python
def calcular_ventas():
    return 1000 + 2000
```

Usas un **PythonOperator**:
```python
task_calcular = PythonOperator(
    task_id="calcular_ventas",
    python_callable=calcular_ventas
)
```

Si quieres ejecutar este comando shell:
```bash
ls -la
```

Usas un **BashOperator**:
```python
task_listar = BashOperator(
    task_id="listar_archivos",
    bash_command="ls -la"
)
```

---

### 4. Scheduler (Programador)

**Definición**: El componente de Airflow que decide cuándo ejecutar cada tarea.

**Analogía**: El reloj despertador de tu smartphone.

Imagina que tienes 20 alarmas configuradas:
- Lunes a viernes: 7 AM (ir al gym)
- Todos los días: 8 AM (desayunar)
- Cada domingo: 10 AM (lavar el coche)

Tu smartphone:
1. **Revisa constantemente** la hora
2. **Compara** con las alarmas configuradas
3. **Activa** la alarma cuando es el momento
4. **Te notifica** si algo no funciona

El **Scheduler de Airflow** hace exactamente lo mismo:
1. Revisa cada 5-10 segundos qué DAGs deben ejecutarse
2. Verifica si es el momento (según el `schedule_interval`)
3. Envía las tasks al Executor para que las ejecute
4. Registra todo en logs

**Sin Scheduler**:
Tendrías que ejecutar manualmente cada DAG con `python mi_dag.py` cada vez.

**Con Scheduler**:
Configuras `schedule="@daily"` y Airflow se encarga de ejecutarlo todos los días a medianoche.

---

### 5. Executor (Ejecutor)

**Definición**: El componente que ejecuta las tareas.

**Analogía**: Los chefs en una cocina.

En un restaurante:
- **Un solo chef** (SequentialExecutor): Cocina un plato a la vez. Lento pero simple.
- **Varios chefs** (LocalExecutor): Varios chefs en la misma cocina. Más rápido.
- **Muchos chefs en varias cocinas** (CeleryExecutor): Chefs distribuidos en diferentes ubicaciones. Muy rápido, para producción.

**Tipos de Executors**:

1. **SequentialExecutor** (1 tarea a la vez):
   - Solo para pruebas
   - No permite paralelización
   - No recomendado

2. **LocalExecutor** (varias tareas en paralelo, misma máquina):
   - Bueno para desarrollo
   - Usa el poder de tu computadora/servidor
   - El que usaremos en este curso

3. **CeleryExecutor** (varias tareas en varias máquinas):
   - Para producción a gran escala
   - Requiere Redis o RabbitMQ
   - Distribución real

4. **KubernetesExecutor** (tareas en contenedores Kubernetes):
   - Para producción cloud-native
   - Escalado dinámico

**Por ahora, usamos LocalExecutor**: Suficiente para aprender y para proyectos medianos.

---

### 6. Webserver (Servidor Web)

**Definición**: La interfaz visual de Airflow donde ves todo lo que pasa.

**Analogía**: El tablero de un coche.

En un coche:
- **Velocímetro**: Cuánto vas
- **Combustible**: Cuánto te queda
- **Temperatura**: Si el motor está caliente
- **Luces de advertencia**: Si algo va mal

En Airflow Web UI:
- **DAGs page**: Lista de todos tus workflows
- **Graph View**: Visualización gráfica del DAG
- **Tree View**: Historial de ejecuciones
- **Logs**: Detalles de qué pasó en cada task
- **Admin panel**: Configuración de variables, conexiones

**Acceso**: Normalmente en `http://localhost:8080`

**Qué puedes hacer**:
- ✅ Ver qué DAGs están ejecutándose
- ✅ Ejecutar un DAG manualmente (trigger)
- ✅ Ver logs de una task que falló
- ✅ Pausar/activar DAGs
- ✅ Ver métricas y estadísticas

---

## Instalación y Configuración con Docker

### ¿Por qué Docker?

Instalar Airflow "a pelo" es complejo porque requiere:
- PostgreSQL (base de datos para metadata)
- Redis (opcional, para cache)
- Configuración de usuario admin
- Múltiples variables de entorno
- Inicialización de base de datos

**Docker simplifica todo esto** en un solo comando.

---

### Prerequisitos

1. **Docker Desktop** instalado y ejecutándose
   - Windows/Mac: Descargar de [docker.com](https://www.docker.com)
   - Linux: `sudo apt install docker.io docker-compose`

2. **Git** instalado (para clonar el repositorio del curso)

3. **Editor de código** (VS Code recomendado)

---

### Paso 1: Verificar Docker

Abre tu terminal y ejecuta:

```bash
docker --version
docker-compose --version
```

Deberías ver algo como:
```
Docker version 24.0.5
docker-compose version 1.29.2
```

Si ves errores, instala Docker Desktop primero.

---

### Paso 2: Navegar a la Carpeta del Curso

```bash
cd "Curso Data Engineering"
```

---

### Paso 3: Verificar el Archivo docker-compose.yml

El archivo `docker-compose.yml` en la raíz del proyecto ya tiene Airflow configurado. Puedes verlo con:

```bash
cat docker-compose.yml | grep -A 20 "airflow"
```

**Servicios incluidos**:
- `postgres-airflow`: Base de datos para Airflow
- `airflow-init`: Inicializa la base de datos y crea el usuario admin
- `airflow-webserver`: Interfaz web en puerto 8080
- `airflow-scheduler`: Programador que ejecuta los DAGs

---

### Paso 4: Iniciar Airflow

Ejecuta:

```bash
docker-compose up -d postgres-airflow airflow-init airflow-webserver airflow-scheduler
```

**Explicación del comando**:
- `docker-compose`: Herramienta para manejar múltiples contenedores
- `up`: Iniciar servicios
- `-d`: Modo "detached" (en segundo plano)
- `postgres-airflow airflow-init airflow-webserver airflow-scheduler`: Los 4 servicios necesarios

**Tiempo**: Primera vez tarda 2-5 minutos (descarga imágenes de Docker)

**Progreso**:
```
[+] Running 4/4
 ✔ Container master-postgres-airflow     Started
 ✔ Container master-airflow-init         Started
 ✔ Container master-airflow-webserver    Started
 ✔ Container master-airflow-scheduler    Started
```

---

### Paso 5: Verificar que Todo Funciona

```bash
docker-compose ps
```

Deberías ver:
```
NAME                        STATUS              PORTS
master-postgres-airflow     Up                  5432/tcp
master-airflow-webserver    Up (healthy)        0.0.0.0:8080->8080/tcp
master-airflow-scheduler    Up
```

**Si ves "Up (healthy)"** → Todo bien ✅
**Si ves "Restarting" o "Unhealthy"** → Hay un problema ❌

---

### Paso 6: Acceder a la Interfaz Web

1. Abre tu navegador
2. Ve a: **http://localhost:8080**
3. Verás la pantalla de login de Airflow

**Credenciales**:
- **Usuario**: `admin`
- **Contraseña**: `Airflow2025!Admin`

(Estas credenciales están en el archivo `docker-compose.yml`)

---

### Tour de la Interfaz Web

Una vez dentro, verás:

**1. DAGs Page (Página principal)**:
```
┌─────────────────────────────────────┐
│ Airflow                             │
├─────────────────────────────────────┤
│ DAGs  Browse  Admin  Docs           │
├─────────────────────────────────────┤
│ Search DAGs: [___________] 🔍       │
├─────────────────────────────────────┤
│ DAG                  Runs   Status  │
│ example_bash_operator  5     On    │
│ example_python         3     Off   │
└─────────────────────────────────────┘
```

**2. DAG Detail (Al hacer clic en un DAG)**:
- **Graph View**: Visualización gráfica del workflow
- **Tree View**: Historial de ejecuciones
- **Code**: Ver el código Python del DAG
- **Logs**: Ver logs de cada task

**3. Admin Panel**:
- **Variables**: Configuración global (por ejemplo, API keys)
- **Connections**: Credenciales de bases de datos/APIs

---

### Comandos Útiles

**Ver logs de un servicio**:
```bash
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

**Detener Airflow**:
```bash
docker-compose stop
```

**Reiniciar Airflow**:
```bash
docker-compose restart airflow-webserver airflow-scheduler
```

**Detener y eliminar todo (⚠️ cuidado, borra datos)**:
```bash
docker-compose down -v
```

---

## Tu Primer DAG: "Hola Mundo"

Ahora que Airflow está corriendo, vamos a crear nuestro primer workflow.

### Objetivo

Crear un DAG que ejecute una función Python simple que imprima "¡Hola desde Airflow!".

---

### Paso 1: Crear el Archivo del DAG

Los DAGs van en la carpeta `airflow/dags/`. Crea un archivo llamado `hola_mundo.py`:

**Ubicación**: `airflow/dags/hola_mundo.py`

```python
# Importar librerías necesarias
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Definir la función que queremos ejecutar
def saludar():
    """
    Esta función simplemente imprime un saludo.
    En un caso real, aquí harías algo útil como
    procesar datos, hacer cálculos, etc.
    """
    print("¡Hola desde Airflow!")
    print("Este es mi primer DAG y funciona correctamente.")
    return "Saludo completado"

# Definir el DAG
with DAG(
    dag_id="hola_mundo",                    # Nombre único del DAG
    description="Mi primer DAG en Airflow",  # Descripción para la UI
    start_date=datetime(2025, 1, 1),        # Fecha de inicio (retroactiva)
    schedule="@daily",                       # Ejecutar una vez al día
    catchup=False,                           # No ejecutar fechas pasadas
    tags=["tutorial", "principiante"],      # Etiquetas para organizar
) as dag:

    # Crear la tarea
    task_saludar = PythonOperator(
        task_id="saludar",           # Nombre único de la tarea
        python_callable=saludar,     # La función a ejecutar
    )
```

---

### Explicación Línea por Línea

#### Imports

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
```

- `datetime`: Para definir fechas de inicio
- `DAG`: La clase principal para crear un workflow
- `PythonOperator`: El operador para ejecutar funciones Python

---

#### La Función Python

```python
def saludar():
    print("¡Hola desde Airflow!")
    return "Saludo completado"
```

**¿Qué puede ir aquí?**
- Procesar un archivo CSV
- Hacer una consulta a una base de datos
- Llamar a una API
- Entrenar un modelo de ML
- Cualquier código Python válido

**Buenas prácticas**:
1. La función debe ser **autocontenida** (no depender de variables globales)
2. Debe retornar algo (útil para debugging)
3. Debe manejar errores con try/except si es posible

---

#### El DAG

```python
with DAG(
    dag_id="hola_mundo",
    ...
) as dag:
    ...
```

**Parámetros clave**:

1. **dag_id** (obligatorio):
   - Nombre único del DAG
   - Solo letras, números, guiones bajos
   - Ejemplo: `"hola_mundo"`, `"etl_ventas_diario"`

2. **description**:
   - Descripción que aparece en la UI
   - Ayuda a recordar qué hace este DAG

3. **start_date** (obligatorio):
   - Fecha desde la cual este DAG puede ejecutarse
   - Usa `datetime(2025, 1, 1)` (año, mes, día)
   - Puede ser en el pasado (Airflow no ejecutará fechas pasadas si `catchup=False`)

4. **schedule**:
   - Cuándo ejecutar el DAG
   - Opciones:
     - `"@daily"`: Una vez al día a medianoche
     - `"@hourly"`: Una vez por hora
     - `"@weekly"`: Una vez por semana
     - `None`: Solo ejecución manual
     - Cron expression: `"0 8 * * *"` (a las 8 AM todos los días)

5. **catchup**:
   - `False`: No ejecutar fechas pasadas (recomendado)
   - `True`: Ejecutar todas las fechas desde `start_date` hasta ahora

6. **tags**:
   - Lista de etiquetas para organizar
   - Ejemplo: `["ventas", "producción"]`

---

#### La Tarea

```python
task_saludar = PythonOperator(
    task_id="saludar",
    python_callable=saludar,
)
```

**Parámetros clave**:

1. **task_id** (obligatorio):
   - Nombre único de la tarea dentro del DAG
   - Aparece en la UI

2. **python_callable**:
   - La función Python a ejecutar
   - **OJO**: Sin paréntesis (`saludar`, NO `saludar()`)

---

### Paso 2: Detectar el DAG en Airflow

Airflow revisa la carpeta `dags/` cada 30 segundos por defecto.

**Verificar en la terminal**:
```bash
docker-compose logs -f airflow-scheduler | grep "hola_mundo"
```

Deberías ver algo como:
```
[INFO] - Added DAG: hola_mundo
```

**Verificar en la UI**:
1. Ve a http://localhost:8080
2. En la lista de DAGs, busca "hola_mundo"
3. Si no aparece, espera 30-60 segundos y recarga la página

---

### Paso 3: Ejecutar el DAG Manualmente

1. En la lista de DAGs, encuentra "hola_mundo"
2. Haz clic en el **botón de play ▶️** a la derecha
3. Confirma "Trigger DAG"
4. Ve a la columna "Runs" → verás un círculo verde (éxito) o rojo (fallo)

---

### Paso 4: Ver los Logs

1. Haz clic en el nombre del DAG "hola_mundo"
2. Verás el **Graph View**: Un gráfico con la tarea "saludar"
3. Haz clic en el cuadro de la tarea "saludar"
4. Haz clic en "Logs"
5. Verás el output:
   ```
   [INFO] - ¡Hola desde Airflow!
   [INFO] - Este es mi primer DAG y funciona correctamente.
   ```

---

### Paso 5: Pausar/Activar el DAG

En la lista de DAGs:
- **Toggle a la izquierda del nombre**: Activar/Pausar
- **Verde** = Activo (se ejecutará según schedule)
- **Gris** = Pausado (solo ejecución manual)

---

## Operators Básicos

Ya usaste `PythonOperator`. Ahora veremos otros operators comunes.

### 1. PythonOperator (Ejecutar Función Python)

**Cuándo usarlo**: Cuando necesitas ejecutar código Python personalizado.

**Ejemplo**: Procesar un archivo, hacer cálculos, llamar a una API.

```python
def procesar_datos():
    import pandas as pd
    df = pd.read_csv("ventas.csv")
    total = df["precio"].sum()
    print(f"Total de ventas: {total}")
    return total

task_procesar = PythonOperator(
    task_id="procesar_datos",
    python_callable=procesar_datos
)
```

---

### 2. BashOperator (Ejecutar Comando Shell)

**Cuándo usarlo**: Cuando necesitas ejecutar comandos de sistema operativo.

**Ejemplo**: Listar archivos, mover archivos, comprimir archivos.

```python
from airflow.operators.bash import BashOperator

task_listar = BashOperator(
    task_id="listar_archivos",
    bash_command="ls -la /path/to/directory"
)

task_comprimir = BashOperator(
    task_id="comprimir_logs",
    bash_command="tar -czf logs.tar.gz /var/log/*.log"
)
```

---

### 3. DummyOperator (Placeholder sin Ejecución)

**Cuándo usarlo**: Para organizar visualmente tu DAG, especialmente en puntos de unión o inicio/fin.

**Ejemplo**: Punto de inicio antes de tareas paralelas, punto de fin después de convergencia.

```python
from airflow.operators.dummy import DummyOperator

inicio = DummyOperator(task_id="inicio")
fin = DummyOperator(task_id="fin")

# inicio >> [tarea1, tarea2, tarea3] >> fin
```

**Visualización**:
```
      inicio
     /  |  \
task1 task2 task3
     \  |  /
       fin
```

---

### Comparación Rápida

| Operator         | Usa Para                    | Ejemplo                             |
| ---------------- | --------------------------- | ----------------------------------- |
| PythonOperator   | Código Python personalizado | Procesar CSV, llamar API            |
| BashOperator     | Comandos shell              | ls, cp, tar, curl                   |
| DummyOperator    | Organización visual         | Puntos de inicio/fin, convergencias |
| PostgresOperator | Queries SQL en PostgreSQL   | INSERT, UPDATE, SELECT              |
| EmailOperator    | Enviar emails               | Notificaciones de éxito/fallo       |

---

## Dependencias entre Tasks

En un DAG real, las tareas tienen orden. "Primero descarga, luego procesa, luego envía reporte".

### Operador `>>`  (Downstream)

**Significado**: "Esta tarea debe ejecutarse DESPUÉS de la otra"

```python
A >> B  # B se ejecuta DESPUÉS de A
```

**Analogía**: "Hornear >> Decorar" (decorar después de hornear)

---

### Operador `<<` (Upstream)

**Significado**: "Esta tarea debe ejecutarse ANTES de la otra"

```python
B << A  # B se ejecuta DESPUÉS de A (igual que A >> B)
```

**Uso**: Es menos común, `>>` es más intuitivo.

---

### Dependencias Secuenciales

```python
descargar >> limpiar >> analizar >> reportar
```

**Visualización**:
```
descargar → limpiar → analizar → reportar
```

**Ejecución**:
1. Primero: `descargar`
2. Cuando termine: `limpiar`
3. Cuando termine: `analizar`
4. Cuando termine: `reportar`

---

### Dependencias Paralelas (Fan-out)

```python
descargar >> [procesar_ventas, procesar_inventario, procesar_clientes]
```

**Visualización**:
```
         descargar
            |
   ┌────────┼────────┐
   ↓        ↓        ↓
ventas  inventario  clientes
```

**Ejecución**:
1. Primero: `descargar`
2. Cuando termine: Las 3 tareas en paralelo (si el Executor lo permite)

---

### Convergencia (Fan-in)

```python
[procesar_ventas, procesar_inventario, procesar_clientes] >> generar_reporte
```

**Visualización**:
```
ventas  inventario  clientes
   ↓        ↓        ↓
   └────────┼────────┘
            |
      generar_reporte
```

**Ejecución**:
1. Las 3 tareas en paralelo
2. `generar_reporte` espera a que las 3 terminen
3. Solo cuando las 3 están completas: ejecuta `generar_reporte`

---

### Ejemplo Completo

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

def descargar():
    print("Descargando datos...")

def procesar_ventas():
    print("Procesando ventas...")

def procesar_inventario():
    print("Procesando inventario...")

def generar_reporte():
    print("Generando reporte final...")

with DAG(
    dag_id="pipeline_completo",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    inicio = DummyOperator(task_id="inicio")

    task_descargar = PythonOperator(
        task_id="descargar",
        python_callable=descargar
    )

    task_ventas = PythonOperator(
        task_id="procesar_ventas",
        python_callable=procesar_ventas
    )

    task_inventario = PythonOperator(
        task_id="procesar_inventario",
        python_callable=procesar_inventario
    )

    task_reporte = PythonOperator(
        task_id="generar_reporte",
        python_callable=generar_reporte
    )

    fin = DummyOperator(task_id="fin")

    # Definir dependencias
    inicio >> task_descargar >> [task_ventas, task_inventario] >> task_reporte >> fin
```

**Visualización en Airflow**:
```
        inicio
          |
      descargar
       /     \
   ventas  inventario
       \     /
       reporte
          |
         fin
```

---

## Schedule Intervals: Cuándo Ejecutar

El `schedule` define cuándo Airflow debe ejecutar automáticamente tu DAG.

### Opciones Comunes (Presets)

```python
schedule="@once"     # Una sola vez
schedule="@hourly"   # Cada hora (minuto 0)
schedule="@daily"    # Cada día a medianoche (00:00)
schedule="@weekly"   # Cada lunes a medianoche
schedule="@monthly"  # El día 1 de cada mes a medianoche
schedule="@yearly"   # El 1 de enero a medianoche
schedule=None        # Solo ejecución manual
```

---

### Cron Expressions (Avanzado)

**Formato**: `"minuto hora día_mes mes día_semana"`

**Ejemplos**:

```python
# Todos los días a las 8:30 AM
schedule="30 8 * * *"

# Cada lunes a las 3 PM
schedule="0 15 * * 1"

# Cada 15 minutos
schedule="*/15 * * * *"

# El día 1 y 15 de cada mes a las 6 AM
schedule="0 6 1,15 * *"
```

**Herramienta útil**: [crontab.guru](https://crontab.guru/) para generar cron expressions.

---

### El Parámetro `catchup`

**Problema**: Si configuras `start_date=datetime(2024, 1, 1)` y hoy es 2025-10-25, ¿Airflow ejecutará 300 días de historial?

**Solución**:
- `catchup=True`: Sí, ejecutará todas las fechas pasadas (útil para backfill)
- `catchup=False`: No, solo desde ahora (recomendado para la mayoría de casos)

**Ejemplo**:

```python
# Ejecutar solo desde hoy en adelante
with DAG(
    dag_id="reporte_diario",
    start_date=datetime(2024, 1, 1),  # Fecha en el pasado
    schedule="@daily",
    catchup=False,  # ← Importante
) as dag:
    ...
```

---

### Ejecución Manual

Si `schedule=None`, el DAG solo se ejecuta manualmente:
- Haces clic en el botón "Trigger DAG" en la UI
- O usas el CLI: `airflow dags trigger mi_dag`

**Útil para**:
- Pipelines on-demand
- Testing
- Procesos esporádicos

---

## Mejores Prácticas

### 1. Un DAG por Archivo

❌ **MAL**:
```
mi_script.py
├── dag1
├── dag2
└── dag3
```

✅ **BIEN**:
```
dags/
├── dag_ventas.py
├── dag_inventario.py
└── dag_reportes.py
```

**Por qué**: Más fácil de mantener, encontrar y debuggear.

---

### 2. Nombres Descriptivos

❌ **MAL**:
```python
dag_id="dag1"
task_id="t1"
```

✅ **BIEN**:
```python
dag_id="etl_ventas_diario"
task_id="descargar_ventas_api"
```

**Por qué**: En 6 meses no recordarás qué hace "dag1".

---

### 3. Usa `catchup=False` por Defecto

A menos que específicamente necesites ejecutar fechas pasadas.

```python
catchup=False  # ← Añade esto siempre
```

---

### 4. Docstrings en DAGs

```python
with DAG(
    dag_id="etl_ventas",
    description="Pipeline ETL para procesar ventas diarias desde la API",  # ← Esto
    ...
) as dag:
    ...
```

---

### 5. Tasks Idempotentes

**Idempotente**: Ejecutar la misma task 10 veces con los mismos inputs produce el mismo output.

❌ **NO idempotente**:
```python
def agregar_venta():
    # Siempre añade una fila, aunque ya exista
    ejecutar_sql("INSERT INTO ventas VALUES (1, 100)")
```

✅ **Idempotente**:
```python
def agregar_venta():
    # Primero elimina si existe, luego inserta
    ejecutar_sql("DELETE FROM ventas WHERE id = 1")
    ejecutar_sql("INSERT INTO ventas VALUES (1, 100)")
```

**Por qué**: Si Airflow reintenta una task, no quieres duplicados ni efectos secundarios.

---

### 6. Usar Tags para Organizar

```python
tags=["producción", "crítico", "ventas"]
```

Luego puedes filtrar en la UI por tags.

---

### 7. Variables de Entorno para Configuración

No hardcodees credenciales o paths:

❌ **MAL**:
```python
db_password = "MiPasswordSecreta123"
```

✅ **BIEN**:
```python
from airflow.models import Variable
db_password = Variable.get("db_password")
```

(Configurar Variables en Admin → Variables en la UI)

---

## Errores Comunes

### Error 1: DAG No Aparece en la UI

**Síntomas**: Creaste el archivo, pero no ves el DAG.

**Causas posibles**:
1. **Sintaxis error en Python**: Revisa logs del scheduler
   ```bash
   docker-compose logs airflow-scheduler | grep "ERROR"
   ```

2. **Archivo no está en `dags/`**: Debe estar en `airflow/dags/mi_dag.py`

3. **Airflow no ha refrescado**: Espera 30-60 segundos

**Solución**: Revisa logs y sintaxis.

---

### Error 2: Task Falla con "ModuleNotFoundError"

**Síntomas**: Task falla, error dice "No module named 'pandas'"

**Causa**: La librería no está instalada en el contenedor de Airflow.

**Solución**:
1. Añadir al `requirements.txt` del proyecto
2. Reconstruir el contenedor:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

---

### Error 3: "DAG Seems to be Missing"

**Síntomas**: DAG aparecía, ahora dice "missing".

**Causa**: Error de sintaxis introducido recientemente.

**Solución**: Revisa el archivo `.py` del DAG, probablemente hay un error.

---

### Error 4: Task en Estado "Running" Indefinidamente

**Síntomas**: Task ejecutándose durante horas sin terminar.

**Causas**:
1. **Loop infinito** en tu código Python
2. **Esperando input del usuario** (Airflow no puede interactuar)

**Solución**:
1. Ve a la UI → Logs de la task
2. Identifica dónde se atascó
3. Corrige el código

---

### Error 5: "Broken DAG" (DAG Roto)

**Síntomas**: Icono rojo en la lista de DAGs.

**Causa**: Error de sintaxis o importación.

**Solución**:
1. Haz clic en el DAG roto
2. Verás el mensaje de error específico
3. Corrige el error en el archivo `.py`

---

## Checklist de Aprendizaje

Al terminar este tema, deberías poder:

- [ ] **Explicar qué es Airflow** con tus propias palabras
- [ ] **Describir qué es un DAG** usando una analogía (receta de cocina)
- [ ] **Diferenciar entre Task, Operator, Scheduler y Executor**
- [ ] **Iniciar Airflow con Docker Compose** sin ayuda
- [ ] **Acceder a la UI de Airflow** en localhost:8080
- [ ] **Crear un DAG simple** con PythonOperator
- [ ] **Definir dependencias** usando `>>` entre tasks
- [ ] **Configurar un schedule** (por ejemplo, `@daily`)
- [ ] **Ejecutar un DAG manualmente** desde la UI
- [ ] **Ver los logs** de una task que se ejecutó
- [ ] **Identificar 3 operators básicos**: PythonOperator, BashOperator, DummyOperator
- [ ] **Explicar qué significa `catchup=False`**
- [ ] **Listar 3 mejores prácticas** de Airflow

---

## Recursos Adicionales

### Documentación Oficial

- **Airflow Docs**: https://airflow.apache.org/docs/
- **Concepts**: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html
- **Tutorial**: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html

### Videos Recomendados

- **Airflow in 5 Minutes** (YouTube): Búsqueda recomendada
- **Apache Airflow Tutorial** (freeCodeCamp): Curso completo gratuito

### Artículos Útiles

- **Best Practices**: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
- **Common Pitfalls**: Búsqueda en Google "Airflow common mistakes"

### Comunidad

- **Slack de Airflow**: https://apache-airflow.slack.com/
- **Stack Overflow**: Tag `apache-airflow`
- **GitHub Issues**: https://github.com/apache/airflow/issues

---

## Próximos Pasos

En el siguiente tema (Airflow Intermedio), aprenderás:

1. **TaskGroups**: Organizar DAGs complejos
2. **XComs**: Pasar datos entre tasks
3. **Branching**: Condicionales en workflows
4. **Sensors**: Esperar por condiciones externas
5. **Dynamic DAG Generation**: Generar tasks en loops

Pero antes, asegúrate de:
- ✅ Completar todos los ejercicios del Tema 1
- ✅ Tener Airflow corriendo en tu máquina
- ✅ Haber creado al menos 2-3 DAGs simples

---

**¡Felicitaciones por completar la introducción a Airflow!** 🎉

Ahora tienes las bases para orquestar workflows de Data Engineering. En los ejemplos y ejercicios prácticos, consolidarás estos conceptos con casos reales.

---

**Fecha de creación**: 2025-10-25
**Autor**: @teaching [pedagogo]
**Módulo**: 6 - Apache Airflow y Orquestación
**Tema**: 1 - Introducción a Airflow
---

## 🧭 Navegación

⬅️ **Anterior**: [Módulo 5: Bases de Datos Avanzadas: Modelado de Datos](../../modulo-05-bases-datos-avanzadas/tema-3-modelado-datos/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
