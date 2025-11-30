# Proyecto 1.1: Calculadora de Estadísticas Básicas

## Descripción

Este proyecto implementa funciones reutilizables para calcular estadísticas básicas, aplicando **Test-Driven Development (TDD)**, tipado explícito, y siguiendo las mejores prácticas de desarrollo en Python.

## Objetivo Pedagógico

Aprender a:
- Escribir código Python limpio y profesional
- Aplicar TDD (escribir tests antes que el código)
- Usar tipado explícito para mejor documentación y detección de errores
- Manejar errores de forma robusta
- Validar inputs para seguridad
- Crear funciones puras sin efectos secundarios

## Conceptos Estadísticos Implementados

### Media (Promedio)
La **media aritmética** es la suma de todos los valores dividida por la cantidad de valores. Es útil para conocer el valor "central" de un conjunto de datos.

**Ejemplo**: Las ventas de DataBite en 5 días fueron [100, 150, 200, 120, 180]. La media es 150 euros/día.

### Mediana
La **mediana** es el valor que está en el centro cuando ordenamos los datos. Es más robusta que la media ante valores extremos.

**Ejemplo**: Tiempos de respuesta de API en ms: [10, 12, 15, 18, 500]. La mediana es 15ms (la media sería muy afectada por el 500).

### Moda
La **moda** es el valor que más se repite en un conjunto de datos.

**Ejemplo**: Productos más vendidos: [A, B, A, C, A, B]. La moda es A (aparece 3 veces).

### Desviación Estándar y Varianza
Miden qué tan dispersos están los datos respecto a la media.
- **Varianza**: Promedio de las diferencias al cuadrado
- **Desviación estándar**: Raíz cuadrada de la varianza (en las mismas unidades que los datos)

**Ejemplo**: Si las ventas varían mucho día a día, tendrán alta desviación estándar.

### Percentiles
Los **percentiles** dividen los datos ordenados en 100 partes iguales.
- Percentil 25 (Q1): 25% de los datos están por debajo
- Percentil 50 (Q2): Es la mediana
- Percentil 75 (Q3): 75% de los datos están por debajo

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

```python
from src.estadisticas import (
    calcular_media,
    calcular_mediana,
    calcular_moda,
    calcular_desviacion_estandar,
    calcular_varianza,
    calcular_percentiles
)

# Ejemplo: Análisis de ventas diarias (en euros)
ventas_diarias = [100.0, 150.0, 200.0, 120.0, 180.0, 110.0, 190.0]

# Calcular estadísticas básicas
media = calcular_media(ventas_diarias)
print(f"Venta promedio: {media:.2f}€")  # 150.00€

mediana = calcular_mediana(ventas_diarias)
print(f"Venta mediana: {mediana:.2f}€")

# Calcular dispersión
desv = calcular_desviacion_estandar(ventas_diarias)
print(f"Desviación estándar: {desv:.2f}€")

# Calcular percentiles (cuartiles)
percentiles = calcular_percentiles(ventas_diarias, [25, 50, 75])
print(f"Q1 (25%): {percentiles[25]:.2f}€")
print(f"Q2 (50%): {percentiles[50]:.2f}€")
print(f"Q3 (75%): {percentiles[75]:.2f}€")
```

## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=src --cov-report=html

# Ver reporte de coverage
# Abrir htmlcov/index.html en el navegador
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
proyecto-1-estadisticas/
├── src/
│   └── estadisticas.py      # Implementación de funciones
├── tests/
│   └── test_estadisticas.py # Tests unitarios
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias
└── .gitignore               # Archivos a ignorar en Git
```

## Criterios de Éxito

- [x] Todas las funciones implementadas con tipado explícito
- [x] Tests con coverage >80%
- [x] Código formateado con black
- [x] Sin errores de flake8
- [x] Manejo robusto de errores (listas vacías, valores inválidos)
- [x] Docstrings completos en todas las funciones
- [x] Validación de inputs para seguridad

## Próximo Proyecto

**Proyecto 1.2**: Procesador de Archivos CSV
- Leer y validar archivos CSV
- Transformar datos
- Manejo avanzado de errores
- Logging profesional

## Notas de Seguridad

Este proyecto implementa:
- Validación estricta de inputs (tipos, valores válidos)
- Manejo explícito de casos edge (listas vacías, valores None)
- Excepciones específicas (ValueError, TypeError)
- Sin efectos secundarios (funciones puras)
- Tests de casos límite

## Licencia

Este proyecto es parte del Master en Ingeniería de Datos con IA - Material educativo.
