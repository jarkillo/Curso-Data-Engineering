# Tema 1: Ejercicios Prácticos de Estadística Descriptiva

## 📖 Cómo Usar Esta Guía

Esta sección contiene **15 ejercicios prácticos** para que consolides tu aprendizaje de estadística descriptiva.

**Metodología recomendada:**
1. Lee el contexto y los datos de cada ejercicio
2. Intenta resolver el ejercicio por tu cuenta (usa papel, lápiz y calculadora)
3. Escribe tu código Python si te sientes cómodo
4. Verifica tu respuesta con las soluciones al final
5. Si te equivocaste, revisa dónde estuvo el error y aprende de él

**Importante:**
- ✅ No te saltes ejercicios. La dificultad es progresiva.
- ✅ Intenta resolverlos sin mirar las soluciones primero.
- ✅ Usa las funciones del proyecto práctico (`04-proyecto-practico/`) si quieres.
- ✅ Anota tus dudas y revisa la teoría (`01-TEORIA.md`) si es necesario.

---

## 📊 Nivel 1: Ejercicios Básicos

Estos ejercicios cubren los conceptos fundamentales: media, mediana y moda.

---

### Ejercicio 1: Calcular la Media de Ventas Diarias
**Dificultad:** ⭐ Fácil
**Conceptos:** Media aritmética

**Contexto:**
Trabajas como analista de datos en una cadena de tiendas de electrónica. Tu jefe te pide analizar las ventas de la última semana de una sucursal para evaluar su rendimiento.

**Datos:**
Las ventas diarias (en euros) de la semana fueron:
```
Lunes:    850€
Martes:   920€
Miércoles: 780€
Jueves:   1,050€
Viernes:  1,200€
Sábado:   1,400€
Domingo:  950€
```

**Tu tarea:**
1. Calcula la venta promedio (media) de la semana
2. Si el objetivo de la tienda es vender 1,000€ por día en promedio, ¿se cumplió el objetivo?

**Espacio para tu respuesta:**
```
Media = _______________

¿Se cumplió el objetivo? _______________
```

---

### Ejercicio 2: Calcular la Mediana de Salarios
**Dificultad:** ⭐ Fácil
**Conceptos:** Mediana

**Contexto:**
Eres el responsable de recursos humanos de una startup tecnológica. Necesitas reportar el salario "típico" de tu equipo de desarrollo para una auditoría interna.

**Datos:**
Los salarios mensuales (en euros) de los 9 desarrolladores son:
```
2,500€, 2,800€, 2,600€, 3,200€, 2,700€, 2,900€, 3,000€, 2,750€, 6,000€
```

**Tu tarea:**
1. Calcula la mediana de los salarios
2. Calcula también la media
3. ¿Cuál de las dos (media o mediana) representa mejor el salario "típico"? ¿Por qué?

**Espacio para tu respuesta:**
```
Mediana = _______________

Media = _______________

¿Cuál es mejor y por qué? _______________
```

---

### Ejercicio 3: Identificar la Moda en Ventas de Productos
**Dificultad:** ⭐ Fácil
**Conceptos:** Moda

**Contexto:**
Gestionas el inventario de una tienda online de ropa. Necesitas identificar qué tallas se venden más para optimizar el stock.

**Datos:**
Las tallas vendidas en el último mes fueron:
```
S, M, M, L, M, S, M, XL, M, L, M, S, M, L, M, XXL, M, L, M, S, M
```

**Tu tarea:**
1. Identifica la moda (talla más vendida)
2. ¿Cuántas veces se vendió esa talla?
3. ¿Qué porcentaje del total de ventas representa?

**Espacio para tu respuesta:**
```
Moda (talla más vendida) = _______________

Frecuencia = _______________

Porcentaje = _______________
```

---

### Ejercicio 4: Comparar Media vs Mediana
**Dificultad:** ⭐ Fácil
**Conceptos:** Media, mediana, detección de outliers

**Contexto:**
Trabajas en el departamento de calidad de una empresa de logística. Estás analizando los tiempos de entrega (en horas) de los últimos 10 pedidos.

**Datos:**
Tiempos de entrega (en horas):
```
24, 26, 25, 27, 23, 25, 26, 24, 120, 25
```

**Tu tarea:**
1. Calcula la media de los tiempos de entrega
2. Calcula la mediana
3. ¿Hay algún valor atípico (outlier)? ¿Cuál?
4. ¿Qué métrica (media o mediana) usarías para reportar el tiempo de entrega "típico"?

**Espacio para tu respuesta:**
```
Media = _______________

Mediana = _______________

Outlier = _______________

¿Qué métrica usar? _______________
```

---

### Ejercicio 5: Interpretar Medidas de Tendencia Central
**Dificultad:** ⭐ Fácil
**Conceptos:** Interpretación de media, mediana, moda

**Contexto:**
Eres analista de datos en una plataforma de streaming de música. Analizas cuántas canciones escuchan los usuarios por día.

**Datos:**
Canciones escuchadas por 11 usuarios en un día:
```
15, 18, 20, 22, 18, 25, 18, 30, 19, 21, 18
```

**Tu tarea:**
1. Calcula la media
2. Calcula la mediana
3. Calcula la moda
4. Interpreta: ¿Qué te dice cada métrica sobre el comportamiento de los usuarios?

**Espacio para tu respuesta:**
```
Media = _______________

Mediana = _______________

Moda = _______________

Interpretación:
_______________
```

---

## 📈 Nivel 2: Ejercicios Intermedios

Estos ejercicios añaden complejidad con varianza, desviación estándar y percentiles.

---

### Ejercicio 6: Calcular Varianza y Desviación Estándar
**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Varianza, desviación estándar

**Contexto:**
Trabajas en el departamento financiero de una empresa. Tu jefe quiere saber qué sucursal tiene ventas más estables para planificar inversiones.

**Datos:**
Ventas mensuales (en miles de euros) de dos sucursales durante 6 meses:

**Sucursal A:**
```
50, 52, 51, 53, 50, 54
```

**Sucursal B:**
```
40, 60, 45, 65, 38, 62
```

**Tu tarea:**
1. Calcula la media de cada sucursal
2. Calcula la desviación estándar de cada sucursal
3. ¿Qué sucursal es más estable? ¿Por qué?

**Espacio para tu respuesta:**
```
Sucursal A:
  Media = _______________
  Desviación estándar = _______________

Sucursal B:
  Media = _______________
  Desviación estándar = _______________

¿Cuál es más estable? _______________
```

---

### Ejercicio 7: Comparar Estabilidad de Procesos
**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Desviación estándar, coeficiente de variación

**Contexto:**
Eres ingeniero de calidad en una fábrica. Necesitas comparar la consistencia de dos máquinas que producen tornillos. La longitud debe ser exacta.

**Datos:**
Longitud de tornillos (en mm) producidos por cada máquina (muestra de 8 tornillos):

**Máquina 1:**
```
50.1, 50.3, 49.9, 50.2, 50.0, 50.1, 50.2, 49.8
```

**Máquina 2:**
```
50.5, 49.2, 51.0, 48.8, 50.3, 49.5, 51.2, 49.5
```

**Tu tarea:**
1. Calcula la media de cada máquina
2. Calcula la desviación estándar de cada máquina
3. ¿Qué máquina es más precisa (consistente)?
4. ¿Cuál recomendarías para producción?

**Espacio para tu respuesta:**
```
Máquina 1:
  Media = _______________
  Desviación = _______________

Máquina 2:
  Media = _______________
  Desviación = _______________

¿Cuál es más precisa? _______________
```

---

### Ejercicio 8: Calcular Percentiles
**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Percentiles (P25, P50, P75, P95)

**Contexto:**
Trabajas en el equipo de infraestructura de una aplicación web. Necesitas analizar los tiempos de respuesta de tu API para reportar métricas de rendimiento.

**Datos:**
Tiempos de respuesta (en milisegundos) de 20 peticiones:
```
12, 15, 18, 14, 16, 22, 19, 17, 21, 23,
25, 18, 20, 16, 19, 24, 28, 31, 35, 18
```

**Tu tarea:**
1. Ordena los datos de menor a mayor
2. Calcula el P50 (mediana)
3. Calcula el P95
4. Si tu SLA dice "el P95 debe ser < 40ms", ¿lo cumples?

**Espacio para tu respuesta:**
```
Datos ordenados:
_______________

P50 = _______________

P95 = _______________

¿Cumple el SLA? _______________
```

---

### Ejercicio 9: Análisis Estadístico Completo
**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Media, mediana, desviación estándar, interpretación

**Contexto:**
Eres analista de datos en una empresa de e-commerce. Tu jefe te pide un análisis completo del valor de los pedidos del último mes.

**Datos:**
Valor de 15 pedidos (en euros):
```
45, 52, 48, 55, 50, 47, 53, 49, 51, 46, 54, 48, 50, 52, 49
```

**Tu tarea:**
1. Calcula la media
2. Calcula la mediana
3. Calcula la desviación estándar
4. Interpreta: ¿Los pedidos son consistentes o muy variables?
5. ¿Cuál sería un rango "normal" de valores de pedido? (usa media ± desviación)

**Espacio para tu respuesta:**
```
Media = _______________

Mediana = _______________

Desviación estándar = _______________

¿Son consistentes? _______________

Rango normal: _______________
```

---

### Ejercicio 10: Detectar Outliers con Desviación Estándar
**Dificultad:** ⭐⭐ Intermedio
**Conceptos:** Outliers, desviación estándar, regla 68-95-99.7

**Contexto:**
Trabajas en el departamento de fraude de un banco. Analizas transacciones para detectar actividad sospechosa.

**Datos:**
Montos de transacciones (en euros) de un cliente en los últimos 10 días:
```
50, 45, 52, 48, 50, 47, 53, 49, 250, 51
```

**Tu tarea:**
1. Calcula la media
2. Calcula la desviación estándar
3. Identifica valores que estén a más de 2 desviaciones estándar de la media
4. ¿Hay transacciones sospechosas? ¿Cuáles?

**Espacio para tu respuesta:**
```
Media = _______________

Desviación estándar = _______________

Límite superior (media + 2*desv) = _______________

Transacciones sospechosas: _______________
```

---

## 🎯 Nivel 3: Ejercicios Avanzados

Estos ejercicios integran múltiples conceptos y requieren interpretación de resultados para tomar decisiones.

---

### Ejercicio 11: Cumplimiento de SLA con Percentiles
**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Percentiles, SLAs, interpretación

**Contexto:**
Eres el líder técnico de un equipo de desarrollo. Tu empresa tiene un SLA (Service Level Agreement) que establece:
- "El 95% de las peticiones a la API deben responder en menos de 100ms"
- "El 99% de las peticiones deben responder en menos de 200ms"

**Datos:**
Tiempos de respuesta (en ms) de 30 peticiones durante la última hora:
```
15, 18, 22, 25, 19, 23, 28, 31, 24, 27,
20, 26, 29, 33, 21, 25, 30, 35, 28, 32,
24, 27, 31, 36, 150, 29, 34, 38, 26, 30
```

**Tu tarea:**
1. Calcula el P95
2. Calcula el P99
3. ¿Se cumple el primer SLA (P95 < 100ms)?
4. ¿Se cumple el segundo SLA (P99 < 200ms)?
5. ¿Hay algún outlier que debas investigar?

**Espacio para tu respuesta:**
```
P95 = _______________

P99 = _______________

¿Cumple SLA 1? _______________

¿Cumple SLA 2? _______________

Outliers a investigar: _______________
```

---

### Ejercicio 12: Comparar Rendimiento de Dos Equipos
**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Media, desviación estándar, coeficiente de variación, comparación

**Contexto:**
Eres gerente de operaciones en un call center. Necesitas comparar el rendimiento de dos equipos de atención al cliente para decidir cuál será el equipo piloto de un nuevo proyecto.

**Datos:**
Número de llamadas atendidas por día durante 2 semanas (10 días laborables):

**Equipo A:**
```
45, 48, 47, 46, 49, 48, 47, 50, 46, 49
```

**Equipo B:**
```
40, 55, 38, 60, 42, 58, 39, 62, 41, 55
```

**Tu tarea:**
1. Calcula la media de cada equipo
2. Calcula la desviación estándar de cada equipo
3. Calcula el coeficiente de variación de cada equipo (desviación/media × 100)
4. ¿Qué equipo es más consistente?
5. ¿Qué equipo elegirías para el proyecto piloto? Justifica tu respuesta.

**Espacio para tu respuesta:**
```
Equipo A:
  Media = _______________
  Desviación = _______________
  Coef. Variación = _______________

Equipo B:
  Media = _______________
  Desviación = _______________
  Coef. Variación = _______________

¿Cuál es más consistente? _______________

¿Cuál elegirías? _______________
```

---

### Ejercicio 13: Decidir Qué Métrica Usar
**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Media vs mediana, outliers, toma de decisiones

**Contexto:**
Eres analista de precios en una plataforma de alquiler de apartamentos. Necesitas reportar el precio "típico" de alquiler en una zona para un informe de mercado.

**Datos:**
Precios de alquiler mensual (en euros) de 12 apartamentos en la zona:
```
650, 680, 700, 720, 690, 710, 675, 695, 705, 2,500, 685, 715
```

**Tu tarea:**
1. Calcula la media
2. Calcula la mediana
3. Identifica outliers
4. ¿Qué métrica (media o mediana) usarías para reportar el precio "típico"?
5. Justifica tu decisión desde el punto de vista de negocio

**Espacio para tu respuesta:**
```
Media = _______________

Mediana = _______________

Outliers = _______________

¿Qué métrica usar? _______________

Justificación:
_______________
```

---

### Ejercicio 14: Caso Integrador - Análisis de Ventas Mensuales
**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Todos los conceptos del tema

**Contexto:**
Eres el director de análisis de datos de una cadena de cafeterías. Necesitas presentar un informe ejecutivo sobre las ventas del último trimestre de una sucursal.

**Datos:**
Ventas diarias (en euros) durante 30 días:
```
850, 920, 880, 910, 950, 1200, 1150, 870, 890, 920,
940, 980, 1000, 1180, 1220, 900, 910, 930, 960, 990,
1020, 1190, 1210, 920, 940, 970, 1000, 1030, 1170, 1200
```

**Tu tarea:**
Realiza un análisis estadístico completo:
1. Calcula la media de ventas diarias
2. Calcula la mediana
3. Calcula la desviación estándar
4. Calcula el P25, P50 y P75
5. Identifica si hay outliers (valores > media + 2*desviación)
6. Interpreta: ¿Las ventas son estables o variables?
7. ¿Qué días de la semana venden más? (pista: los días 6, 7, 14, 15, 22, 23, 29, 30 son fines de semana)

**Espacio para tu respuesta:**
```
Media = _______________
Mediana = _______________
Desviación = _______________
P25 = _______________
P50 = _______________
P75 = _______________
Outliers = _______________

Interpretación:
_______________

Patrón de ventas:
_______________
```

---

### Ejercicio 15: Decisiones de Negocio Basadas en Estadísticas
**Dificultad:** ⭐⭐⭐ Avanzado
**Conceptos:** Interpretación, toma de decisiones, análisis de negocio

**Contexto:**
Eres el gerente de producto de una aplicación móvil. Tienes datos de cuánto tiempo pasan los usuarios en la app por sesión. Necesitas decidir si implementar una nueva funcionalidad que podría aumentar el engagement.

**Datos:**
Tiempo de sesión (en minutos) de 25 usuarios:
```
5, 8, 12, 6, 10, 15, 7, 9, 11, 14,
8, 10, 13, 6, 9, 12, 16, 7, 11, 10,
8, 14, 9, 12, 10
```

**Contexto adicional:**
- La nueva funcionalidad cuesta 50,000€ implementar
- Cada minuto adicional de uso genera 0.05€ de ingresos por publicidad
- Tienes 100,000 usuarios activos mensuales
- Cada usuario usa la app 20 veces al mes en promedio

**Tu tarea:**
1. Calcula la media actual de tiempo de sesión
2. Calcula la mediana y desviación estándar
3. Si la nueva funcionalidad aumenta el tiempo de sesión en un 20%, ¿cuál sería la nueva media?
4. Calcula el incremento de ingresos mensuales con ese aumento
5. ¿Cuántos meses tardarías en recuperar la inversión?
6. ¿Recomendarías implementar la funcionalidad? Justifica con datos.

**Espacio para tu respuesta:**
```
Media actual = _______________
Mediana = _______________
Desviación = _______________

Nueva media (+20%) = _______________

Ingresos actuales/mes = _______________
Nuevos ingresos/mes = _______________
Incremento/mes = _______________

Meses para recuperar inversión = _______________

¿Implementar? _______________

Justificación:
_______________
```

---

## ✅ Soluciones Detalladas

A continuación encontrarás las soluciones completas de todos los ejercicios. Intenta resolver cada ejercicio por tu cuenta antes de consultar las soluciones.

---

### Solución Ejercicio 1: Calcular la Media de Ventas Diarias

**Paso 1: Organizar los datos**
```python
ventas = [850, 920, 780, 1050, 1200, 1400, 950]
```

**Paso 2: Calcular la media**
```python
media = sum(ventas) / len(ventas)
print(f"Media: {media:.2f}€")
```

**Cálculo manual:**
```
Suma = 850 + 920 + 780 + 1050 + 1200 + 1400 + 950 = 7,150€
Cantidad de días = 7
Media = 7,150 / 7 = 1,021.43€
```

**Respuesta:**
- Media = **1,021.43€**
- ¿Se cumplió el objetivo? **SÍ**, porque 1,021.43€ > 1,000€

**Interpretación:**
La tienda superó su objetivo de ventas en 21.43€ por día en promedio. Esto indica un buen rendimiento semanal.

---

### Solución Ejercicio 2: Calcular la Mediana de Salarios

**Paso 1: Organizar y ordenar los datos**
```python
salarios = [2500, 2800, 2600, 3200, 2700, 2900, 3000, 2750, 6000]
salarios_ordenados = sorted(salarios)
print(salarios_ordenados)
# [2500, 2600, 2700, 2750, 2800, 2900, 3000, 3200, 6000]
```

**Paso 2: Calcular la mediana**
```python
n = len(salarios_ordenados)
mediana = salarios_ordenados[n // 2]  # Posición 4 (índice 4)
print(f"Mediana: {mediana}€")
```

**Paso 3: Calcular la media**
```python
media = sum(salarios) / len(salarios)
print(f"Media: {media:.2f}€")
```

**Cálculo manual:**
```
Salarios ordenados: 2500, 2600, 2700, 2750, 2800, 2900, 3000, 3200, 6000
Posición central (9 valores): posición 5 → 2,800€
Mediana = 2,800€

Media = (2500 + 2800 + 2600 + 3200 + 2700 + 2900 + 3000 + 2750 + 6000) / 9
Media = 28,450 / 9 = 3,161.11€
```

**Respuesta:**
- Mediana = **2,800€**
- Media = **3,161.11€**
- **La mediana es mejor** porque hay un outlier (6,000€) que distorsiona la media. La mediana representa mejor el salario típico del equipo.

**Interpretación:**
El salario de 6,000€ (probablemente un senior o líder técnico) eleva la media significativamente. Para reportar el salario "típico", la mediana de 2,800€ es más representativa de lo que gana la mayoría del equipo.

---

### Solución Ejercicio 3: Identificar la Moda en Ventas de Productos

**Paso 1: Contar frecuencias**
```python
from collections import Counter

tallas = ['S', 'M', 'M', 'L', 'M', 'S', 'M', 'XL', 'M', 'L',
          'M', 'S', 'M', 'L', 'M', 'XXL', 'M', 'L', 'M', 'S', 'M']

contador = Counter(tallas)
print(contador)
# Counter({'M': 11, 'L': 4, 'S': 4, 'XL': 1, 'XXL': 1})
```

**Paso 2: Identificar la moda**
```python
moda = contador.most_common(1)[0]
print(f"Moda: {moda[0]} (vendida {moda[1]} veces)")
```

**Paso 3: Calcular porcentaje**
```python
total = len(tallas)
porcentaje = (moda[1] / total) * 100
print(f"Porcentaje: {porcentaje:.1f}%")
```

**Respuesta:**
- Moda = **M (talla M)**
- Frecuencia = **11 veces**
- Porcentaje = **52.4%** (11/21 × 100)

**Interpretación:**
Más de la mitad de las ventas son de talla M. Deberías asegurar que siempre haya stock suficiente de esta talla. Las tallas XL y XXL se venden muy poco, considera reducir su inventario.

---

### Solución Ejercicio 4: Comparar Media vs Mediana

**Paso 1: Calcular la media**
```python
tiempos = [24, 26, 25, 27, 23, 25, 26, 24, 120, 25]

media = sum(tiempos) / len(tiempos)
print(f"Media: {media:.1f} horas")
```

**Paso 2: Calcular la mediana**
```python
tiempos_ordenados = sorted(tiempos)
# [23, 24, 24, 25, 25, 25, 26, 26, 27, 120]

n = len(tiempos_ordenados)
mediana = (tiempos_ordenados[n//2 - 1] + tiempos_ordenados[n//2]) / 2
print(f"Mediana: {mediana} horas")
```

**Cálculo manual:**
```
Media = (24 + 26 + 25 + 27 + 23 + 25 + 26 + 24 + 120 + 25) / 10
Media = 345 / 10 = 34.5 horas

Mediana (posiciones 5 y 6): (25 + 25) / 2 = 25 horas
```

**Respuesta:**
- Media = **34.5 horas**
- Mediana = **25 horas**
- Outlier = **120 horas** (probablemente un pedido con problemas)
- **Usar la mediana** porque representa mejor el tiempo típico de entrega

**Interpretación:**
El valor de 120 horas es claramente anormal (5 días de entrega vs 1 día típico). Este pedido debe investigarse. Para reportar el rendimiento del servicio, usa la mediana de 25 horas, que refleja la experiencia de la mayoría de los clientes.

---

### Solución Ejercicio 5: Interpretar Medidas de Tendencia Central

**Código completo:**
```python
from collections import Counter

canciones = [15, 18, 20, 22, 18, 25, 18, 30, 19, 21, 18]

# Media
media = sum(canciones) / len(canciones)

# Mediana
canciones_ordenadas = sorted(canciones)
mediana = canciones_ordenadas[len(canciones) // 2]

# Moda
contador = Counter(canciones)
moda = contador.most_common(1)[0][0]

print(f"Media: {media:.1f} canciones")
print(f"Mediana: {mediana} canciones")
print(f"Moda: {moda} canciones")
```

**Cálculo manual:**
```
Media = (15 + 18 + 20 + 22 + 18 + 25 + 18 + 30 + 19 + 21 + 18) / 11
Media = 224 / 11 = 20.4 canciones

Ordenados: 15, 18, 18, 18, 18, 19, 20, 21, 22, 25, 30
Mediana (posición 6): 19 canciones

Moda: 18 canciones (aparece 4 veces)
```

**Respuesta:**
- Media = **20.4 canciones**
- Mediana = **19 canciones**
- Moda = **18 canciones**

**Interpretación:**
- **Media (20.4)**: El usuario promedio escucha ~20 canciones al día
- **Mediana (19)**: La mitad de los usuarios escucha menos de 19 canciones
- **Moda (18)**: El comportamiento más común es escuchar 18 canciones
- **Conclusión**: La mayoría de usuarios tiene un comportamiento similar (18-19 canciones), pero hay algunos usuarios "power users" (25-30 canciones) que elevan ligeramente la media.

---

### Solución Ejercicio 6: Calcular Varianza y Desviación Estándar

**Código completo:**
```python
import math

sucursal_a = [50, 52, 51, 53, 50, 54]
sucursal_b = [40, 60, 45, 65, 38, 62]

def calcular_estadisticas(datos, nombre):
    media = sum(datos) / len(datos)

    # Varianza
    diferencias_cuadradas = [(x - media) ** 2 for x in datos]
    varianza = sum(diferencias_cuadradas) / len(datos)

    # Desviación estándar
    desviacion = math.sqrt(varianza)

    print(f"\n{nombre}:")
    print(f"  Media: {media:.2f}k€")
    print(f"  Desviación estándar: {desviacion:.2f}k€")

    return media, desviacion

media_a, desv_a = calcular_estadisticas(sucursal_a, "Sucursal A")
media_b, desv_b = calcular_estadisticas(sucursal_b, "Sucursal B")
```

**Cálculo manual Sucursal A:**
```
Media = (50 + 52 + 51 + 53 + 50 + 54) / 6 = 310 / 6 = 51.67k€

Diferencias al cuadrado:
(50 - 51.67)² = 2.79
(52 - 51.67)² = 0.11
(51 - 51.67)² = 0.45
(53 - 51.67)² = 1.77
(50 - 51.67)² = 2.79
(54 - 51.67)² = 5.43

Varianza = (2.79 + 0.11 + 0.45 + 1.77 + 2.79 + 5.43) / 6 = 13.34 / 6 = 2.22
Desviación = √2.22 = 1.49k€
```

**Cálculo manual Sucursal B:**
```
Media = (40 + 60 + 45 + 65 + 38 + 62) / 6 = 310 / 6 = 51.67k€

Diferencias al cuadrado:
(40 - 51.67)² = 136.19
(60 - 51.67)² = 69.39
(45 - 51.67)² = 44.49
(65 - 51.67)² = 177.69
(38 - 51.67)² = 186.85
(62 - 51.67)² = 106.69

Varianza = 721.30 / 6 = 120.22
Desviación = √120.22 = 10.96k€
```

**Respuesta:**
- **Sucursal A**: Media = 51.67k€, Desviación = 1.49k€
- **Sucursal B**: Media = 51.67k€, Desviación = 10.96k€
- **La Sucursal A es más estable** porque tiene una desviación mucho menor

**Interpretación:**
Ambas sucursales venden lo mismo en promedio (51.67k€), pero la Sucursal A es mucho más predecible. Sus ventas varían solo ±1.49k€, mientras que la Sucursal B varía ±10.96k€. Para planificar inversiones, la Sucursal A es más confiable.

---

### Solución Ejercicio 7: Comparar Estabilidad de Procesos

**Código completo:**
```python
import math

maquina_1 = [50.1, 50.3, 49.9, 50.2, 50.0, 50.1, 50.2, 49.8]
maquina_2 = [50.5, 49.2, 51.0, 48.8, 50.3, 49.5, 51.2, 49.5]

def analizar_maquina(datos, nombre):
    media = sum(datos) / len(datos)
    varianza = sum((x - media) ** 2 for x in datos) / len(datos)
    desviacion = math.sqrt(varianza)

    print(f"\n{nombre}:")
    print(f"  Media: {media:.2f}mm")
    print(f"  Desviación: {desviacion:.3f}mm")

    return media, desviacion

media_1, desv_1 = analizar_maquina(maquina_1, "Máquina 1")
media_2, desv_2 = analizar_maquina(maquina_2, "Máquina 2")

print(f"\n¿Cuál es más precisa? Máquina 1 (desviación {desv_1:.3f} < {desv_2:.3f})")
```

**Cálculo manual Máquina 1:**
```
Media = (50.1 + 50.3 + 49.9 + 50.2 + 50.0 + 50.1 + 50.2 + 49.8) / 8
Media = 400.6 / 8 = 50.075mm

Desviación ≈ 0.158mm
```

**Cálculo manual Máquina 2:**
```
Media = (50.5 + 49.2 + 51.0 + 48.8 + 50.3 + 49.5 + 51.2 + 49.5) / 8
Media = 400.0 / 8 = 50.0mm

Desviación ≈ 0.776mm
```

**Respuesta:**
- **Máquina 1**: Media = 50.08mm, Desviación = 0.158mm
- **Máquina 2**: Media = 50.00mm, Desviación = 0.776mm
- **La Máquina 1 es más precisa** (menor desviación)
- **Recomendación**: Usar Máquina 1 para producción

**Interpretación:**
Aunque la Máquina 2 tiene una media más cercana al objetivo (50.0mm), la Máquina 1 es mucho más consistente. En producción, la consistencia es más importante que estar exactamente en el objetivo, porque puedes calibrar la máquina pero no puedes eliminar la variabilidad.

---

### Solución Ejercicio 8: Calcular Percentiles

**Código completo:**
```python
tiempos = [12, 15, 18, 14, 16, 22, 19, 17, 21, 23,
           25, 18, 20, 16, 19, 24, 28, 31, 35, 18]

# Ordenar
tiempos_ordenados = sorted(tiempos)
print("Datos ordenados:")
print(tiempos_ordenados)

# P50 (mediana)
n = len(tiempos_ordenados)
p50 = tiempos_ordenados[n // 2]

# P95
posicion_p95 = int(0.95 * n)
p95 = tiempos_ordenados[posicion_p95 - 1]

print(f"\nP50 (mediana): {p50}ms")
print(f"P95: {p95}ms")
print(f"SLA (P95 < 40ms): {'✅ CUMPLE' if p95 < 40 else '❌ NO CUMPLE'}")
```

**Cálculo manual:**
```
Datos ordenados (20 valores):
[12, 14, 15, 16, 16, 17, 18, 18, 18, 19,
 19, 20, 21, 22, 23, 24, 25, 28, 31, 35]

P50 (posición 10): 19ms
P95 (posición 19): 31ms
```

**Respuesta:**
- Datos ordenados: [12, 14, 15, 16, 16, 17, 18, 18, 18, 19, 19, 20, 21, 22, 23, 24, 25, 28, 31, 35]
- P50 = **19ms**
- P95 = **31ms**
- **SÍ cumple el SLA** (31ms < 40ms)

**Interpretación:**
El 95% de las peticiones responden en menos de 31ms, lo cual está muy por debajo del objetivo de 40ms. Esto indica un buen rendimiento de la API con margen de seguridad de 9ms.

---

### Solución Ejercicio 9: Análisis Estadístico Completo

**Código completo:**
```python
import math

pedidos = [45, 52, 48, 55, 50, 47, 53, 49, 51, 46, 54, 48, 50, 52, 49]

# Media
media = sum(pedidos) / len(pedidos)

# Mediana
pedidos_ordenados = sorted(pedidos)
mediana = pedidos_ordenados[len(pedidos) // 2]

# Desviación estándar
varianza = sum((x - media) ** 2 for x in pedidos) / len(pedidos)
desviacion = math.sqrt(varianza)

# Rango normal
rango_min = media - desviacion
rango_max = media + desviacion

print(f"Media: {media:.2f}€")
print(f"Mediana: {mediana}€")
print(f"Desviación estándar: {desviacion:.2f}€")
print(f"Rango normal: {rango_min:.2f}€ - {rango_max:.2f}€")
```

**Cálculo manual:**
```
Media = (45 + 52 + 48 + 55 + 50 + 47 + 53 + 49 + 51 + 46 + 54 + 48 + 50 + 52 + 49) / 15
Media = 749 / 15 = 49.93€

Mediana (posición 8): 50€

Desviación ≈ 2.83€

Rango normal: 49.93 - 2.83 = 47.10€ hasta 49.93 + 2.83 = 52.76€
```

**Respuesta:**
- Media = **49.93€**
- Mediana = **50€**
- Desviación estándar = **2.83€**
- **Los pedidos son muy consistentes** (desviación baja)
- Rango normal: **47.10€ - 52.76€**

**Interpretación:**
Los pedidos son extremadamente consistentes. La desviación de solo 2.83€ indica que la mayoría de los pedidos están entre 47€ y 53€. Esto sugiere que tienes un segmento de clientes muy homogéneo o productos con precios similares.

---

### Solución Ejercicio 10: Detectar Outliers con Desviación Estándar

**Código completo:**
```python
import math

transacciones = [50, 45, 52, 48, 50, 47, 53, 49, 250, 51]

# Media y desviación
media = sum(transacciones) / len(transacciones)
desviacion = math.sqrt(sum((x - media) ** 2 for x in transacciones) / len(transacciones))

# Límite para outliers (2 desviaciones)
limite_superior = media + 2 * desviacion
limite_inferior = media - 2 * desviacion

# Identificar outliers
outliers = [x for x in transacciones if x > limite_superior or x < limite_inferior]

print(f"Media: {media:.2f}€")
print(f"Desviación estándar: {desviacion:.2f}€")
print(f"Límite superior: {limite_superior:.2f}€")
print(f"Límite inferior: {limite_inferior:.2f}€")
print(f"Transacciones sospechosas: {outliers}")
```

**Cálculo manual:**
```
Media = (50 + 45 + 52 + 48 + 50 + 47 + 53 + 49 + 250 + 51) / 10
Media = 695 / 10 = 69.5€

Desviación ≈ 60.21€

Límite superior = 69.5 + 2(60.21) = 189.92€
Límite inferior = 69.5 - 2(60.21) = -50.92€ (no aplica, no hay valores negativos)
```

**Respuesta:**
- Media = **69.5€**
- Desviación estándar = **60.21€**
- Límite superior = **189.92€**
- Transacciones sospechosas: **[250€]**

**Interpretación:**
La transacción de 250€ está claramente fuera del patrón normal del cliente (más de 2 desviaciones estándar por encima de la media). Esta transacción debe ser investigada por el departamento de fraude, ya que es aproximadamente 3.6 veces mayor que las transacciones habituales del cliente.

---

### Solución Ejercicio 11: Cumplimiento de SLA con Percentiles

**Código completo:**
```python
import math

tiempos = [15, 18, 22, 25, 19, 23, 28, 31, 24, 27,
           20, 26, 29, 33, 21, 25, 30, 35, 28, 32,
           24, 27, 31, 36, 150, 29, 34, 38, 26, 30]

# Ordenar
tiempos_ordenados = sorted(tiempos)
n = len(tiempos_ordenados)

# P95 (usando math.ceil para redondeo correcto)
pos_p95 = math.ceil(0.95 * n) - 1
p95 = tiempos_ordenados[pos_p95]

# P99
pos_p99 = math.ceil(0.99 * n) - 1
p99 = tiempos_ordenados[pos_p99]

# Identificar outliers
media = sum(tiempos) / len(tiempos)
outliers = [t for t in tiempos if t > 100]

print(f"P95: {p95}ms")
print(f"P99: {p99}ms")
print(f"SLA 1 (P95 < 100ms): {'✅ CUMPLE' if p95 < 100 else '❌ NO CUMPLE'}")
print(f"SLA 2 (P99 < 200ms): {'✅ CUMPLE' if p99 < 200 else '❌ NO CUMPLE'}")
print(f"Outliers a investigar: {outliers}")
```

**Cálculo manual:**
```
Ordenados (30 valores):
[15, 18, 19, 20, 21, 22, 23, 24, 24, 25,
 25, 26, 26, 27, 27, 28, 28, 29, 29, 30,
 30, 31, 31, 32, 33, 34, 35, 36, 38, 150]

P95 (ceil(0.95 * 30) = 29, índice 28): 38ms
P99 (ceil(0.99 * 30) = 30, índice 29): 150ms
```

**Respuesta:**
- P95 = **38ms**
- P99 = **150ms**
- **SÍ cumple SLA 1** (38ms < 100ms) ✅
- **SÍ cumple SLA 2** (150ms < 200ms) ✅
- Outliers a investigar: **[150ms]**

**Interpretación:**
La API cumple ambos SLAs con margen de seguridad. Sin embargo, hay una petición que tardó 150ms (el P99), que es significativamente más lenta que el resto (la mayoría < 40ms). Deberías investigar:
- ¿Qué endpoint fue?
- ¿Hubo un problema de base de datos?
- ¿Fue un cache miss?

Aunque cumples el SLA, esta petición lenta podría indicar un problema potencial.

---

### Solución Ejercicio 12: Comparar Rendimiento de Dos Equipos

**Código completo:**
```python
import math

equipo_a = [45, 48, 47, 46, 49, 48, 47, 50, 46, 49]
equipo_b = [40, 55, 38, 60, 42, 58, 39, 62, 41, 55]

def analizar_equipo(datos, nombre):
    media = sum(datos) / len(datos)
    desviacion = math.sqrt(sum((x - media) ** 2 for x in datos) / len(datos))
    coef_variacion = (desviacion / media) * 100

    print(f"\n{nombre}:")
    print(f"  Media: {media:.1f} llamadas/día")
    print(f"  Desviación: {desviacion:.2f}")
    print(f"  Coef. Variación: {coef_variacion:.2f}%")

    return media, desviacion, coef_variacion

media_a, desv_a, cv_a = analizar_equipo(equipo_a, "Equipo A")
media_b, desv_b, cv_b = analizar_equipo(equipo_b, "Equipo B")

print(f"\n¿Cuál es más consistente? Equipo A (CV: {cv_a:.2f}% < {cv_b:.2f}%)")
```

**Cálculo manual:**
```
Equipo A:
Media = 475 / 10 = 47.5 llamadas/día
Desviación ≈ 1.43
Coef. Variación = (1.43 / 47.5) × 100 = 3.01%

Equipo B:
Media = 490 / 10 = 49.0 llamadas/día
Desviación ≈ 9.17
Coef. Variación = (9.17 / 49.0) × 100 = 18.71%
```

**Respuesta:**
- **Equipo A**: Media = 47.5, Desviación = 1.43, CV = 3.01%
- **Equipo B**: Media = 49.0, Desviación = 9.17, CV = 18.71%
- **El Equipo A es mucho más consistente** (CV 6 veces menor)
- **Elegiría el Equipo A** para el proyecto piloto

**Justificación:**
Aunque el Equipo B atiende ligeramente más llamadas en promedio (49 vs 47.5), el Equipo A es extremadamente consistente (CV = 3%). Esto significa:
- Rendimiento predecible día a día
- Menos riesgo de días con bajo rendimiento
- Más confiable para un proyecto piloto donde necesitas resultados estables

El Equipo B es muy variable (algunos días 38 llamadas, otros 62), lo cual indica falta de consistencia en el proceso o el equipo.

---

### Solución Ejercicio 13: Decidir Qué Métrica Usar

**Código completo:**
```python
import math

precios = [650, 680, 700, 720, 690, 710, 675, 695, 705, 2500, 685, 715]

# Media
media = sum(precios) / len(precios)

# Mediana
precios_ordenados = sorted(precios)
n = len(precios_ordenados)
mediana = (precios_ordenados[n//2 - 1] + precios_ordenados[n//2]) / 2

# Identificar outliers
desviacion = math.sqrt(sum((x - media) ** 2 for x in precios) / len(precios))
outliers = [p for p in precios if abs(p - media) > 2 * desviacion]

print(f"Media: {media:.2f}€")
print(f"Mediana: {mediana:.2f}€")
print(f"Outliers: {outliers}")
print(f"\n¿Qué métrica usar? MEDIANA")
```

**Cálculo manual:**
```
Media = (650 + 680 + 700 + 720 + 690 + 710 + 675 + 695 + 705 + 2500 + 685 + 715) / 12
Media = 10,125 / 12 = 843.75€

Ordenados: 650, 675, 680, 685, 690, 695, 700, 705, 710, 715, 720, 2500
Mediana (posiciones 6 y 7): (695 + 700) / 2 = 697.5€

Outlier: 2,500€ (apartamento de lujo)
```

**Respuesta:**
- Media = **843.75€**
- Mediana = **697.5€**
- Outliers = **[2,500€]**
- **Usar la MEDIANA** (697.5€)

**Justificación desde el punto de vista de negocio:**
El apartamento de 2,500€ es claramente atípico (probablemente un ático de lujo o apartamento premium). Si reportas la media de 843.75€:
- **Problema**: Engañas a los clientes potenciales, que esperarán precios de ~840€ pero encontrarán que la mayoría cuesta ~700€
- **Consecuencia**: Clientes frustrados, pérdida de confianza

Si reportas la mediana de 697.5€:
- **Ventaja**: Representa el precio que realmente encontrará el 50% de los clientes
- **Honestidad**: Es más representativo del mercado real
- **Decisión correcta**: Para informes de mercado, siempre usa la mediana cuando hay outliers

---

### Solución Ejercicio 14: Caso Integrador - Análisis de Ventas Mensuales

**Código completo:**
```python
import math

ventas = [850, 920, 880, 910, 950, 1200, 1150, 870, 890, 920,
          940, 980, 1000, 1180, 1220, 900, 910, 930, 960, 990,
          1020, 1190, 1210, 920, 940, 970, 1000, 1030, 1170, 1200]

# Estadísticas básicas
media = sum(ventas) / len(ventas)
ventas_ordenadas = sorted(ventas)
mediana = (ventas_ordenadas[14] + ventas_ordenadas[15]) / 2
desviacion = math.sqrt(sum((x - media) ** 2 for x in ventas) / len(ventas))

# Percentiles
p25 = ventas_ordenadas[int(0.25 * len(ventas))]
p50 = mediana
p75 = ventas_ordenadas[int(0.75 * len(ventas))]

# Outliers
limite_superior = media + 2 * desviacion
outliers = [v for v in ventas if v > limite_superior]

# Análisis de fines de semana
ventas_finde = [ventas[i] for i in [5, 6, 13, 14, 21, 22, 28, 29]]
media_finde = sum(ventas_finde) / len(ventas_finde)
ventas_semana = [v for i, v in enumerate(ventas) if i not in [5, 6, 13, 14, 21, 22, 28, 29]]
media_semana = sum(ventas_semana) / len(ventas_semana)

print(f"Media: {media:.2f}€")
print(f"Mediana: {mediana:.2f}€")
print(f"Desviación: {desviacion:.2f}€")
print(f"P25: {p25}€")
print(f"P50: {p50:.2f}€")
print(f"P75: {p75}€")
print(f"Outliers: {outliers}")
print(f"\nMedia entre semana: {media_semana:.2f}€")
print(f"Media fin de semana: {media_finde:.2f}€")
```

**Respuesta:**
- Media = **1,006.67€**
- Mediana = **965€**
- Desviación = **118.50€**
- P25 = **920€**
- P50 = **965€**
- P75 = **1,150€**
- Outliers = **Ninguno** (todos los valores están dentro de 2 desviaciones)

**Interpretación:**
Las ventas son **moderadamente variables** (desviación de 118.50€ sobre una media de 1,006.67€, ~11.8% de variación). Esto es normal para una cafetería.

**Patrón de ventas:**
- **Entre semana**: ~930€/día en promedio
- **Fin de semana**: ~1,190€/día en promedio
- **Diferencia**: Los fines de semana venden ~28% más

**Conclusión para el informe ejecutivo:**
"La sucursal genera ventas promedio de 1,006.67€/día con un patrón claro: los fines de semana superan las 1,200€ mientras que entre semana rondan los 900-950€. Las ventas son estables y predecibles, sin valores atípicos. Recomendación: Reforzar personal los fines de semana."

---

### Solución Ejercicio 15: Decisiones de Negocio Basadas en Estadísticas

**Código completo:**
```python
import math

tiempos_sesion = [5, 8, 12, 6, 10, 15, 7, 9, 11, 14,
                  8, 10, 13, 6, 9, 12, 16, 7, 11, 10,
                  8, 14, 9, 12, 10]

# Estadísticas actuales
media_actual = sum(tiempos_sesion) / len(tiempos_sesion)
tiempos_ordenados = sorted(tiempos_sesion)
mediana = tiempos_ordenados[len(tiempos_ordenados) // 2]
desviacion = math.sqrt(sum((x - media_actual) ** 2 for x in tiempos_sesion) / len(tiempos_sesion))

# Nueva media con aumento del 20%
nueva_media = media_actual * 1.20

# Datos del negocio
usuarios_activos = 100000
sesiones_por_usuario_mes = 20
ingresos_por_minuto = 0.05
costo_funcionalidad = 50000

# Cálculos de ingresos
sesiones_totales_mes = usuarios_activos * sesiones_por_usuario_mes
ingresos_actuales_mes = sesiones_totales_mes * media_actual * ingresos_por_minuto
nuevos_ingresos_mes = sesiones_totales_mes * nueva_media * ingresos_por_minuto
incremento_mes = nuevos_ingresos_mes - ingresos_actuales_mes

# ROI
meses_recuperacion = costo_funcionalidad / incremento_mes

print(f"Media actual: {media_actual:.2f} minutos")
print(f"Mediana: {mediana} minutos")
print(f"Desviación: {desviacion:.2f} minutos")
print(f"\nNueva media (+20%): {nueva_media:.2f} minutos")
print(f"\nIngresos actuales/mes: {ingresos_actuales_mes:,.2f}€")
print(f"Nuevos ingresos/mes: {nuevos_ingresos_mes:,.2f}€")
print(f"Incremento/mes: {incremento_mes:,.2f}€")
print(f"\nMeses para recuperar inversión: {meses_recuperacion:.1f} meses")
print(f"\n¿Implementar? {'SÍ' if meses_recuperacion <= 12 else 'NO'}")
```

**Cálculo manual:**
```
Media actual = 250 / 25 = 10 minutos
Mediana = 10 minutos
Desviación ≈ 2.83 minutos

Nueva media (+20%) = 10 × 1.20 = 12 minutos

Sesiones totales/mes = 100,000 × 20 = 2,000,000 sesiones

Ingresos actuales/mes = 2,000,000 × 10 × 0.05 = 1,000,000€
Nuevos ingresos/mes = 2,000,000 × 12 × 0.05 = 1,200,000€
Incremento/mes = 200,000€

Meses para recuperar = 50,000 / 200,000 = 0.25 meses (~1 semana)
```

**Respuesta:**
- Media actual = **10 minutos**
- Mediana = **10 minutos**
- Desviación = **2.83 minutos**
- Nueva media (+20%) = **12 minutos**
- Ingresos actuales/mes = **1,000,000€**
- Nuevos ingresos/mes = **1,200,000€**
- Incremento/mes = **200,000€**
- Meses para recuperar inversión = **0.25 meses** (~1 semana)
- **¿Implementar? SÍ, DEFINITIVAMENTE**

**Justificación con datos:**
Esta es una decisión extremadamente favorable:
1. **ROI rapidísimo**: Recuperas la inversión en ~1 semana
2. **Incremento significativo**: +200,000€/mes de ingresos adicionales
3. **Bajo riesgo**: Incluso si el aumento fuera solo del 10% (no 20%), seguiría siendo rentable
4. **Beneficio anual**: 200,000€ × 12 = 2,400,000€ adicionales al año

**Recomendación final:**
**IMPLEMENTAR INMEDIATAMENTE**. Con un ROI de menos de 1 mes, esta es una de las mejores inversiones posibles. Incluso en el peor escenario (aumento del 5% en lugar de 20%), recuperarías la inversión en 5 meses.

---

## 📊 Tabla de Autoevaluación

Usa esta tabla para hacer seguimiento de tu progreso:

| Ejercicio | Nivel         | Completado | Correcto | Notas |
| --------- | ------------- | ---------- | -------- | ----- |
| 1         | ⭐ Básico      | [ ]        | [ ]      |       |
| 2         | ⭐ Básico      | [ ]        | [ ]      |       |
| 3         | ⭐ Básico      | [ ]        | [ ]      |       |
| 4         | ⭐ Básico      | [ ]        | [ ]      |       |
| 5         | ⭐ Básico      | [ ]        | [ ]      |       |
| 6         | ⭐⭐ Intermedio | [ ]        | [ ]      |       |
| 7         | ⭐⭐ Intermedio | [ ]        | [ ]      |       |
| 8         | ⭐⭐ Intermedio | [ ]        | [ ]      |       |
| 9         | ⭐⭐ Intermedio | [ ]        | [ ]      |       |
| 10        | ⭐⭐ Intermedio | [ ]        | [ ]      |       |
| 11        | ⭐⭐⭐ Avanzado  | [ ]        | [ ]      |       |
| 12        | ⭐⭐⭐ Avanzado  | [ ]        | [ ]      |       |
| 13        | ⭐⭐⭐ Avanzado  | [ ]        | [ ]      |       |
| 14        | ⭐⭐⭐ Avanzado  | [ ]        | [ ]      |       |
| 15        | ⭐⭐⭐ Avanzado  | [ ]        | [ ]      |       |

---

## 🎯 Próximos Pasos

Una vez que hayas completado estos ejercicios:

1. ✅ **Revisa tus errores**: Aprende de cada error
2. ✅ **Practica con el proyecto**: Usa las funciones de `04-proyecto-practico/`
3. ✅ **Continúa con el Tema 2**: Procesamiento de archivos CSV
4. ✅ **Aplica lo aprendido**: Busca datasets reales para practicar

**Recursos adicionales:**
- Vuelve a `01-TEORIA.md` si necesitas repasar conceptos
- Revisa `02-EJEMPLOS.md` para ver más casos resueltos
- Experimenta con el código del proyecto práctico

---

## 💡 Consejos para el Éxito

1. **No te frustres**: La estadística requiere práctica
2. **Usa calculadora**: No pierdas tiempo en cálculos manuales complejos
3. **Entiende el concepto**: Es más importante que memorizar fórmulas
4. **Practica regularmente**: 30 minutos al día es mejor que 3 horas una vez
5. **Aplica a casos reales**: Busca datos de tu trabajo o vida diaria

---

**¡Felicitaciones por completar los ejercicios de Estadística Descriptiva!** 🎉

Ahora tienes las habilidades fundamentales para analizar datos como un Data Engineer profesional.

---

**Última actualización:** 2025-10-19
**Duración estimada:** 3-4 horas (todos los ejercicios)
