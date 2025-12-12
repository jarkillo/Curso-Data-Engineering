# Módulo 10: Machine Learning para Data Engineers

**Objetivo**: Dominar las técnicas de Machine Learning desde la perspectiva de Ingeniería de Datos: feature engineering, pipelines ML production-ready, y MLOps para despliegue y monitoreo de modelos.

---

## 📋 Contenido del Módulo

| Tema | Estado | Descripción |
|------|--------|-------------|
| **Tema 1**: Feature Engineering | 🚧 En desarrollo | Transformaciones, encoding, scaling, pipelines de features |
| **Tema 2**: Pipelines ML | 📋 Planificado | scikit-learn pipelines, validación cruzada, train/test split |
| **Tema 3**: MLOps y Productivización | 📋 Planificado | MLflow, deployment, monitoreo de modelos |

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

### Tema 1: Feature Engineering
- ✅ Diseñar transformaciones de datos para ML
- ✅ Aplicar encoding de variables categóricas (One-Hot, Label, Target)
- ✅ Implementar scaling y normalización (StandardScaler, MinMaxScaler)
- ✅ Crear pipelines de features reutilizables
- ✅ Manejar missing values y outliers

### Tema 2: Pipelines ML
- ⬜ Construir pipelines end-to-end con scikit-learn
- ⬜ Implementar train/test/validation split correctamente
- ⬜ Aplicar cross-validation para evaluación robusta
- ⬜ Serializar y versionar modelos
- ⬜ Crear pipelines reproducibles

### Tema 3: MLOps y Productivización
- ⬜ Usar MLflow para tracking de experimentos
- ⬜ Versionar modelos y datasets
- ⬜ Desplegar modelos como APIs
- ⬜ Implementar monitoreo de drift
- ⬜ Configurar CI/CD para ML

---

## 🏗️ Requisitos Previos

- **Módulos completados**:
  - Módulo 1: Fundamentos de Python
  - Módulo 3: Ingeniería de Datos Core (ETL/Pandas)
  - Módulo 5: Bases de Datos Avanzadas (recomendado)

- **Conocimientos**:
  - Python intermedio/avanzado
  - Pandas y NumPy
  - Conceptos básicos de estadística
  - SQL básico

- **Software**:
  - Python 3.11+
  - Docker Desktop (para MLflow)
  - Git

---

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias principales

```txt
# ML Core
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0

# MLOps
mlflow>=2.8.0
joblib>=1.3.0

# Visualización
matplotlib>=3.7.0
seaborn>=0.12.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Quality
black>=23.9.0
flake8>=6.1.0
mypy>=1.5.0
```

---

## 🔧 Enfoque: Ingeniería, no Algoritmos

Este módulo se centra en la **perspectiva del Data Engineer**, no del Data Scientist:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ML desde la perspectiva DE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Data Scientist              vs           Data Engineer            │
│   ─────────────                           ─────────────             │
│   • Qué modelo usar                       • Cómo mover datos        │
│   • Ajustar hiperparámetros               • Pipelines reproducibles │
│   • Interpretar resultados                • Escalabilidad           │
│   • Validar hipótesis                     • Monitoreo en producción │
│                                           • CI/CD para ML           │
│                                                                     │
│   Nosotros nos enfocamos en el lado derecho                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Lo que SÍ cubrimos:
- Feature engineering automatizado y reproducible
- Pipelines que escalan a producción
- Versionado de modelos y datos
- Deployment y monitoreo
- Testing de pipelines ML

### Lo que NO cubrimos en profundidad:
- Teoría matemática de algoritmos
- Selección avanzada de modelos
- Deep Learning
- Interpretabilidad avanzada

---

## 📊 Arquitectura de un Pipeline ML Production-Ready

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ML Pipeline Production-Ready                     │
└─────────────────────────────────────────────────────────────────────────┘

    Raw Data         Feature Store        Model Registry       Serving
       │                   │                    │                  │
       ▼                   ▼                    ▼                  ▼
┌─────────────┐    ┌─────────────┐      ┌─────────────┐    ┌─────────────┐
│  Ingestion  │───▶│  Feature    │─────▶│  Training   │───▶│  Inference  │
│             │    │  Engineering│      │  Pipeline   │    │  Service    │
└─────────────┘    └─────────────┘      └─────────────┘    └─────────────┘
       │                   │                    │                  │
       ▼                   ▼                    ▼                  ▼
┌─────────────┐    ┌─────────────┐      ┌─────────────┐    ┌─────────────┐
│  Validation │    │  Feature    │      │  Model      │    │  Monitoring │
│  & Quality  │    │  Versioning │      │  Versioning │    │  & Alerts   │
└─────────────┘    └─────────────┘      └─────────────┘    └─────────────┘
```

---

## 📚 Recursos Adicionales

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Feature Engineering for ML (Google)](https://developers.google.com/machine-learning/data-prep)
- [Designing Machine Learning Systems (Chip Huyen)](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)

---

## 📝 Changelog

### v0.1.0 (En desarrollo)
- 🚧 Tema 1: Feature Engineering
- 📋 Tema 2: Planificado
- 📋 Tema 3: Planificado

---

**Siguiente paso**: [Tema 1: Feature Engineering](tema-1-feature-engineering/)
