# Módulo 9: Apache Spark y Big Data

**Objetivo**: Dominar Apache Spark para procesamiento distribuido de grandes volúmenes de datos, incluyendo batch processing, SQL analytics y streaming en tiempo real.

---

## 📋 Contenido del Módulo

| Tema | Estado | Descripción |
|------|--------|-------------|
| **Tema 1**: Introducción a Spark | 🚧 En desarrollo | RDDs, DataFrames, transformaciones, acciones |
| **Tema 2**: Spark SQL y Optimización | 📋 Planificado | Catalyst, particionamiento, caching |
| **Tema 3**: Spark Streaming | 📋 Planificado | Structured Streaming, Kafka, windowing |

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

### Tema 1: Introducción a Spark
- ✅ Entender la arquitectura distribuida de Spark
- ✅ Trabajar con RDDs, DataFrames y Datasets
- ✅ Aplicar transformaciones y acciones
- ✅ Comprender lazy evaluation y DAG
- ✅ Ejecutar jobs en modo local y cluster

### Tema 2: Spark SQL y Optimización
- ⬜ Escribir queries SQL sobre DataFrames
- ⬜ Entender el Catalyst Optimizer
- ⬜ Aplicar particionamiento efectivo
- ⬜ Usar caching y persistencia
- ⬜ Optimizar joins y shuffles

### Tema 3: Spark Streaming
- ⬜ Implementar Structured Streaming
- ⬜ Trabajar con ventanas de tiempo (windowing)
- ⬜ Integrar Kafka con Spark
- ⬜ Manejar late data y watermarks

---

## 🏗️ Requisitos Previos

- **Módulos completados**:
  - Módulo 1: Fundamentos de Python
  - Módulo 3: Ingeniería de Datos Core (ETL/Pandas)
  - Módulo 8: Data Warehousing (recomendado)

- **Conocimientos**:
  - Python intermedio
  - SQL básico
  - Conceptos de ETL

- **Software**:
  - Docker Desktop
  - Python 3.11+
  - Java 11+ (para Spark)

---

## 🚀 Instalación

### Opción 1: Docker (Recomendado)

```bash
# Usar imagen oficial de Spark
docker run -it --rm \
  -p 4040:4040 \
  -v $(pwd):/app \
  apache/spark:3.5.0-python3 \
  /opt/spark/bin/pyspark

# O usar Jupyter con PySpark
docker run -it --rm \
  -p 8888:8888 \
  -p 4040:4040 \
  -v $(pwd):/home/jovyan/work \
  jupyter/pyspark-notebook
```

### Opción 2: Instalación Local

```bash
# Instalar Java 11
# Windows: descargar de adoptium.net
# Mac: brew install openjdk@11
# Linux: sudo apt install openjdk-11-jdk

# Instalar PySpark
pip install pyspark==3.5.0

# Verificar instalación
pyspark --version
```

---

## 📊 Arquitectura de Spark

```
                    ┌─────────────────────────────────────┐
                    │           Driver Program            │
                    │  (SparkContext / SparkSession)      │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │         Cluster Manager             │
                    │   (Standalone / YARN / Kubernetes)  │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
┌─────────▼─────────┐     ┌───────────▼───────────┐   ┌───────────▼───────────┐
│    Worker Node    │     │     Worker Node       │   │     Worker Node       │
│   ┌───────────┐   │     │   ┌───────────┐       │   │   ┌───────────┐       │
│   │ Executor  │   │     │   │ Executor  │       │   │   │ Executor  │       │
│   │  ┌─────┐  │   │     │   │  ┌─────┐  │       │   │   │  ┌─────┐  │       │
│   │  │Task │  │   │     │   │  │Task │  │       │   │   │  │Task │  │       │
│   │  └─────┘  │   │     │   │  └─────┘  │       │   │   │  └─────┘  │       │
│   └───────────┘   │     │   └───────────┘       │   │   └───────────┘       │
└───────────────────┘     └───────────────────────┘   └───────────────────────┘
```

---

## 📚 Recursos Adicionales

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Learning Spark, 2nd Edition](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050049/)
- [Spark: The Definitive Guide](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/)

---

## 📝 Changelog

### v0.1.0 (En desarrollo)
- 🚧 Tema 1: Introducción a Spark
- 📋 Tema 2: Planificado
- 📋 Tema 3: Planificado

---

**Siguiente paso**: [Tema 1: Introducción a Spark](tema-1-introduccion/)
