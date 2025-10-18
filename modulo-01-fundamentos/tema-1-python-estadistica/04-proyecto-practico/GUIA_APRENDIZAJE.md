# Guía de Aprendizaje: Calculadora de Estadísticas Básicas

## 📘 Para Quién es Esta Guía

Esta guía está diseñada para personas que están comenzando en programación y data engineering. **No necesitas conocimientos previos de estadística o Python avanzado**. Te explicaremos todo desde cero.

---

## 🎯 ¿Por Qué Empezamos con Estadísticas?

### Conexión con Data Engineering

Como Data Engineer, tu trabajo principal es **mover, transformar y garantizar la calidad de los datos**. Las estadísticas son fundamentales porque:

1. **Validación de Datos**: ¿Los datos tienen sentido? ¿Hay valores anómalos?
2. **Monitoreo de Calidad**: ¿Cuántos valores nulos hay? ¿Ha cambiado la distribución?
3. **Métricas de Negocio**: Calcular KPIs, promedios, tendencias
4. **Detección de Anomalías**: Identificar problemas en los datos

### Ejemplo Real: Yurest (Sistema de Ventas)

Imagina que trabajas con Yurest, un sistema de ventas de restaurantes. Cada día necesitas:

```python
# Datos reales del día
ventas_dia = [45.50, 78.20, 125.00, 34.80, 89.50, 156.70, 67.30]

# Preguntas que debes responder:
# 1. ¿Cuál fue la venta promedio? → Media
# 2. ¿Cuál fue la venta típica? → Mediana
# 3. ¿Qué monto se repitió más? → Moda
# 4. ¿Las ventas fueron estables o muy variables? → Desviación estándar
# 5. ¿El 90% de las ventas fueron menores a cuánto? → Percentil 90
```

**Esto es exactamente lo que hace nuestro proyecto.**

---

## 📚 Conceptos Estadísticos Explicados (Sin Matemáticas Complicadas)

### 1. Media (Promedio)

**¿Qué es?**  
Es la suma de todos los valores dividida por cuántos valores hay.

**¿Para qué sirve?**  
Te da una idea general del valor "típico" o "central".

**Ejemplo cotidiano:**
```
Ventas de la semana: 100€, 150€, 200€, 120€, 180€

Media = (100 + 150 + 200 + 120 + 180) / 5 = 150€

Interpretación: "En promedio, vendemos 150€ al día"
```

**Problema:**  
La media se ve MUY afectada por valores extremos (outliers).

```
Ventas normales: 100€, 110€, 105€, 115€
Día especial con evento: 1000€

Media = (100 + 110 + 105 + 115 + 1000) / 5 = 286€

¿Es 286€ representativo de un día normal? ¡NO!
```

### 2. Mediana

**¿Qué es?**  
El valor que está justo en el medio cuando ordenas todos los datos.

**¿Para qué sirve?**  
Es más robusta que la media. Los valores extremos no la afectan tanto.

**Ejemplo:**
```
Ventas ordenadas: 100€, 105€, 110€, 115€, 1000€
                            ↑
                        Mediana = 110€
```

**¿Cuándo usarla?**  
- Tiempos de respuesta de una API (algunos requests pueden ser muy lentos)
- Salarios (pocos CEOs con salarios altísimos no deben afectar el "salario típico")
- Datos con outliers

**Ejemplo real Agora:**
```python
# Tiempos de respuesta de API en milisegundos
tiempos = [10, 12, 15, 18, 20, 25, 500]  # 500ms es un outlier

media = 85.7ms    # ¡Muy afectada por el 500!
mediana = 18ms    # Representa mejor el tiempo "típico"

# Para SLAs (Service Level Agreements), la mediana es más útil
```

### 3. Moda

**¿Qué es?**  
El valor que más se repite.

**¿Para qué sirve?**  
Identificar qué es lo más común o frecuente.

**Ejemplo Yurest:**
```python
# IDs de productos vendidos hoy
productos_vendidos = [
    101,  # Hamburguesa
    102,  # Pizza
    101,  # Hamburguesa
    103,  # Ensalada
    101,  # Hamburguesa
    102,  # Pizza
    104   # Pasta
]

Moda = 101 (Hamburguesa) → Es el producto más vendido
```

**Casos especiales:**
- **Unimodal**: Una sola moda (lo más común)
- **Bimodal**: Dos modas (dos cosas igualmente comunes)
- **Multimodal**: Varias modas

### 4. Varianza y Desviación Estándar

**¿Qué miden?**  
Qué tan dispersos o "esparcidos" están los datos respecto al promedio.

**Analogía simple:**
Imagina dos restaurantes:

```
Restaurante A: ventas diarias = [98€, 100€, 102€, 99€, 101€]
→ Muy estable, predecible

Restaurante B: ventas diarias = [50€, 150€, 75€, 200€, 25€]
→ Muy variable, impredecible
```

**La desviación estándar te dice:**
- Baja desviación = Datos estables, predecibles, consistentes
- Alta desviación = Datos variables, impredecibles, volátiles

**Ejemplo real:**
```python
# Ventas estables
ventas_a = [98, 100, 102, 99, 101]
desviacion_a = 1.4€  # Muy baja → Negocio estable

# Ventas volátiles
ventas_b = [50, 150, 75, 200, 25]
desviacion_b = 64.8€  # Muy alta → Negocio impredecible
```

### 5. Percentiles

**¿Qué son?**  
Dividen tus datos ordenados en 100 partes iguales.

**Percentiles comunes:**
- **Percentil 25 (Q1)**: 25% de los datos están por debajo
- **Percentil 50 (Q2)**: Es la mediana
- **Percentil 75 (Q3)**: 75% de los datos están por debajo
- **Percentil 95**: 95% de los datos están por debajo (muy usado en SLAs)

**Ejemplo SLA de Agora:**
```python
# Queremos que el 95% de las peticiones respondan en < 100ms

tiempos_respuesta = [10, 12, 15, 18, 20, 22, 25, 30, 35, 200]

P50 = 21ms   # Mediana - tiempo típico
P95 = 47ms   # El 95% responde en < 47ms → ¡Cumplimos el SLA!
P99 = 112ms  # El 99% responde en < 112ms
```

**¿Por qué P95 y no la media?**  
Porque el P95 ignora los outliers extremos pero te dice el tiempo "máximo razonable".

---

## 🧪 ¿Qué es TDD (Test-Driven Development)?

### El Problema Tradicional

Normalmente programamos así:
1. Escribo la función
2. Pruebo manualmente si funciona
3. "Parece que funciona" ✓
4. **Meses después**: Bug en producción 💥

### La Solución: TDD

TDD es escribir **los tests ANTES del código**:

```
1. Escribo el test (que va a fallar porque la función no existe)
   ↓
2. Escribo la función MÁS SIMPLE que haga pasar el test
   ↓
3. Refactorizo (mejoro el código manteniendo los tests verdes)
   ↓
4. Repito para la siguiente funcionalidad
```

### Ejemplo Real: Calculando la Media

**Paso 1: Escribir el test primero**

```python
# tests/test_estadisticas.py

def test_media_lista_simple():
    """Test: ¿la media de [1,2,3,4,5] es 3?"""
    datos = [1.0, 2.0, 3.0, 4.0, 5.0]
    resultado = calcular_media(datos)
    assert resultado == 3.0
```

**Ejecutamos:** `pytest` → ❌ FALLA (la función no existe aún)

**Paso 2: Implementar lo mínimo**

```python
# src/estadisticas.py

def calcular_media(datos):
    """Calcula la media."""
    return sum(datos) / len(datos)
```

**Ejecutamos:** `pytest` → ✅ PASA

**Paso 3: Escribir más tests (casos edge)**

```python
def test_media_lista_vacia_lanza_error():
    """¿Qué pasa si la lista está vacía?"""
    with pytest.raises(ValueError):
        calcular_media([])
```

**Ejecutamos:** `pytest` → ❌ FALLA (no validamos listas vacías)

**Paso 4: Mejorar la implementación**

```python
def calcular_media(datos):
    """Calcula la media."""
    if len(datos) == 0:
        raise ValueError("La lista no puede estar vacía")
    return sum(datos) / len(datos)
```

**Ejecutamos:** `pytest` → ✅ TODOS PASAN

### Beneficios de TDD

1. **Seguridad**: Sabes que tu código funciona ANTES de publicarlo
2. **Documentación viva**: Los tests muestran cómo usar las funciones
3. **Refactoring seguro**: Puedes mejorar el código sin miedo a romperlo
4. **Menos bugs**: Los problemas se detectan inmediatamente

---

## 🔍 Recorrido por el Código (Línea por Línea)

### Función: `calcular_media()`

Vamos a analizar el código paso a paso:

```python
def calcular_media(datos: List[Union[int, float]]) -> float:
```

**¿Qué significa esto?**
- `def calcular_media`: Definimos una función llamada calcular_media
- `datos: List[Union[int, float]]`: El parámetro `datos` debe ser una lista de enteros o flotantes
- `-> float`: La función devuelve un número decimal (float)

**¿Por qué tipado explícito?**
- Ayuda a entender qué espera la función
- El editor puede avisarte de errores
- Mejor documentación

```python
    if not isinstance(datos, list):
        raise TypeError("Los datos deben ser una lista.")
```

**¿Qué hace?**
- Verifica que `datos` sea realmente una lista
- Si alguien pasa un string o un número, lanza error
- **Seguridad**: Validamos inputs desde el inicio

**Ejemplo de lo que previene:**
```python
calcular_media("12345")  # ❌ TypeError claro
calcular_media(42)       # ❌ TypeError claro
```

```python
    if len(datos) == 0:
        raise ValueError("La lista no puede estar vacía.")
```

**¿Por qué?**
- No puedes calcular la media de 0 números (división por cero)
- **Mejor**: Lanzar error claro que crash misterioso

```python
    for i, valor in enumerate(datos):
        if not isinstance(valor, (int, float)):
            raise TypeError(f"El elemento en posición {i} no es un número")
```

**¿Qué hace?**
- Revisa CADA elemento de la lista
- Si encuentra algo que no sea número, lanza error CON CONTEXTO

**Ejemplo:**
```python
calcular_media([1, 2, "tres", 4])
# TypeError: El elemento en posición 2 es de tipo str: tres
#           ↑ Te dice EXACTAMENTE qué está mal
```

```python
    suma_total = sum(datos)
    cantidad = len(datos)
    media = suma_total / cantidad
    return float(media)
```

**El cálculo real:**
- Suma todos los valores
- Cuenta cuántos son
- Divide suma / cantidad
- Devuelve el resultado

### ¿Por Qué Tanto Código de Validación?

**Código sin validación:**
```python
def calcular_media(datos):
    return sum(datos) / len(datos)
```
- 2 líneas
- ❌ Crash si lista vacía
- ❌ Crash si tiene strings
- ❌ Mensajes de error confusos

**Código CON validación:**
```python
def calcular_media(datos):
    # 20 líneas de validación
    # ...
    return sum(datos) / len(datos)
```
- 30 líneas
- ✅ Errores claros y útiles
- ✅ Previene crashes
- ✅ Fácil de debuggear
- ✅ Producción-ready

**En Data Engineering**: Los datos SIEMPRE son sucios. La validación es CRÍTICA.

---

## 🎮 Ejercicios Prácticos

### Ejercicio 1: Usar las Funciones

```python
# Copia este código en un archivo test.py

from src.estadisticas import (
    calcular_media,
    calcular_mediana,
    calcular_desviacion_estandar
)

# Caso: Análisis de ventas de tu tienda
ventas_semana = [120.50, 135.75, 98.30, 145.00, 132.80, 110.25, 155.60]

# 1. Calcula la venta promedio
promedio = calcular_media(ventas_semana)
print(f"Venta promedio: {promedio:.2f}€")

# 2. Calcula la venta mediana
mediana = calcular_mediana(ventas_semana)
print(f"Venta mediana: {mediana:.2f}€")

# 3. Calcula la desviación estándar
desviacion = calcular_desviacion_estandar(ventas_semana)
print(f"Desviación: {desviacion:.2f}€")

# Pregunta: ¿Las ventas son estables o variables?
if desviacion < 20:
    print("✓ Ventas estables")
else:
    print("⚠ Ventas muy variables")
```

### Ejercicio 2: Detectar Outliers

```python
from src.estadisticas import calcular_media, calcular_desviacion_estandar

# Tiempos de respuesta de tu API
tiempos = [12, 15, 13, 18, 14, 250, 16, 15]  # 250ms es un outlier

media = calcular_media(tiempos)
desviacion = calcular_desviacion_estandar(tiempos)

# Detectar outliers (valores > 2 desviaciones de la media)
outliers = [t for t in tiempos if abs(t - media) > 2 * desviacion]

print(f"Media: {media:.1f}ms")
print(f"Outliers detectados: {outliers}")
```

### Ejercicio 3: Escribir Tu Propio Test

```python
# Escribe un test para verificar que la media de [10, 20, 30] es 20

def test_mi_primer_test():
    datos = [10, 20, 30]
    resultado = calcular_media(datos)
    assert resultado == 20.0, "La media de 10,20,30 debe ser 20"

# Ejecuta: pytest -v
```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Instalar Dependencias

```bash
# Navegar al proyecto
cd modulo-01-fundamentos/proyecto-1-estadisticas

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ver coverage
pytest --cov=src --cov-report=html tests/

# Abrir reporte HTML
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

### 3. Usar las Funciones en Python

```python
# Abrir Python interactivo
python

# Importar funciones
from src.estadisticas import *

# Probar
datos = [1, 2, 3, 4, 5]
print(calcular_media(datos))
print(calcular_mediana(datos))
```

### 4. Formatear y Validar Código

```bash
# Formatear con black
black src/ tests/

# Validar estilo con flake8
flake8 src/ tests/ --max-line-length=100

# Type checking con mypy
mypy src/
```

---

## 📖 Recursos Adicionales

### Para Aprender Más Estadística

1. **Khan Academy** - Statistics and Probability (gratis, en español)
2. **StatQuest (YouTube)** - Explicaciones visuales excelentes
3. **Libro**: "Estadística para Dummies" - Deborah Rumsey

### Para Aprender Más Python

1. **Python.org Tutorial** - Oficial y completo
2. **Real Python** - Tutoriales prácticos
3. **Libro**: "Python Crash Course" - Eric Matthes

### Para Aprender Más Testing

1. **pytest Documentation** - Documentación oficial
2. **Test-Driven Development with Python** - Harry Percival
3. **YouTube**: "TDD en Python" - Muchos tutoriales

---

## ❓ Preguntas Frecuentes

### ¿Por qué no usar librerías como NumPy o SciPy?

**Respuesta**: En este proyecto queremos **entender los fundamentos**. NumPy es excelente, pero primero debes saber qué está haciendo por debajo. En proyectos futuros sí usaremos NumPy.

### ¿Por qué tantas validaciones? ¿No es código extra?

**Respuesta**: En **producción**, los datos son sucios. Una función sin validación puede:
- Crashear tu sistema
- Dar resultados incorrectos silenciosamente
- Ser muy difícil de debuggear

Las validaciones son una **inversión**: más código ahora = menos problemas después.

### ¿Es normal que los tests tengan MÁS líneas que el código?

**Respuesta**: ¡Sí! Es completamente normal. Los tests cubren:
- Casos normales
- Casos edge (límites)
- Casos de error
- Diferentes tipos de datos

Un buen test suite suele tener 2-3x más líneas que el código de producción.

### ¿Debo memorizar todas las fórmulas?

**Respuesta**: NO. Lo importante es:
1. Entender **qué** hace cada estadística
2. Saber **cuándo** usarla
3. Poder **interpretar** los resultados

Las fórmulas están en la documentación. El criterio no.

---

## ✅ Checklist de Aprendizaje

Marca lo que has aprendido:

### Conceptos Estadísticos
- [ ] Entiendo qué es la media y cuándo usarla
- [ ] Entiendo por qué la mediana es mejor para outliers
- [ ] Puedo explicar qué es la moda con mis propias palabras
- [ ] Entiendo qué mide la desviación estándar
- [ ] Sé para qué sirven los percentiles

### Python
- [ ] Entiendo qué es el tipado explícito
- [ ] Sé por qué validar inputs es importante
- [ ] Puedo escribir funciones con docstrings
- [ ] Entiendo cómo manejar excepciones

### Testing
- [ ] Entiendo el flujo de TDD (test → código → refactor)
- [ ] Puedo escribir un test básico con pytest
- [ ] Entiendo qué es el coverage
- [ ] Sé por qué los tests son importantes

### Data Engineering
- [ ] Veo la conexión entre estadísticas y datos
- [ ] Entiendo casos de uso reales (Yurest, Agora)
- [ ] Puedo explicar por qué esto es relevante para mi carrera

---

## 🎯 Próximo Paso

Una vez que te sientas cómodo con este proyecto, continuarás con:

**Proyecto 1.2: Procesador de Archivos CSV**

Donde aprenderás:
- Leer archivos reales
- Validar esquemas de datos
- Transformar datos
- Logging profesional
- Manejo de errores en archivos

---

**¿Tienes dudas?** Revisa la documentación, ejecuta los ejemplos, experimenta con el código. La mejor forma de aprender es **haciendo**.

**¡Buen viaje en tu camino a Data Engineer! 🚀**

