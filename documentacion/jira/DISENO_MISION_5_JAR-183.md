# 🎮 Diseño de Misión 5: Varianza y Desviación Estándar

**Issue**: JAR-183
**Fecha de diseño**: 2025-10-20
**Diseñador**: Game Design Team
**Revisor pedagógico**: Teaching Team (Pedagogo)
**Estado**: ✅ Diseño Completo con Mejoras Pedagógicas - Listo para Implementación

---

## 📋 Resumen Ejecutivo

### Objetivo Pedagógico
Enseñar el concepto de **dispersión de datos** a través de la **varianza** y **desviación estándar**, y explicar la diferencia entre **varianza poblacional (÷N)** y **varianza muestral (÷N-1)**.

### Innovaciones
- ✅ Primera misión que enseña **medidas de dispersión** (no solo tendencia central)
- ✅ Visualización de **dispersión con gráfico de puntos**
- ✅ Introduce concepto de **varianza poblacional vs muestral**
- ✅ Visualización de **campana gaussiana** con área sombreada
- ✅ Explicación pedagógica de la **corrección de Bessel** (por qué N-1)

### Métricas Clave
- **XP Total**: 275 XP (100 + 150 + 25 bonus)
- **Tiempo estimado**: 10-15 minutos
- **Complejidad**: Media-Alta
- **Tasa de éxito esperada**: >70% en 5A, >60% en 5B

### Calificación Pedagógica
- **Revisión inicial**: 8.5/10
- **Con mejoras aplicadas**: 9.2/10 (esperado)
- **Veredicto**: APROBADO CON MEJORAS IMPLEMENTADAS

---

## 📚 Revisión Pedagógica Previa

### ✅ Fortalezas Identificadas
1. **Progresión lógica**: De media/mediana/moda (tendencia central) a varianza/desviación (dispersión)
2. **Dos submisiones**: 5A (básica) introduce dispersión, 5B (avanzada) profundiza en N vs N-1
3. **Concepto importante**: La diferencia entre varianza poblacional y muestral es fundamental en estadística
4. **Visualizaciones apropiadas**: Gráfico de puntos para dispersión, campana para distribución

### ⚠️ Mejoras Críticas Implementadas
1. **✅ CORREGIDO - Contexto pedagógico reforzado**: Escena 10 ahora explica claramente por qué dos datasets con misma media pueden ser diferentes
2. **✅ CORREGIDO - Pregunta de 5A simplificada**: Ahora pide calcular la desviación estándar de AMBAS máquinas (no preguntar cuál es "más confiable")
3. **✅ CORREGIDO - Misión 5B simplificada**: Primero calcula varianza muestral, luego el tutorial explica por qué N-1 (no pide explicación en la respuesta)
4. **✅ CORREGIDO - Tutorial robusto**: Escena 10 ahora tiene analogía clara y ejemplos visuales
5. **✅ CORREGIDO - Bonus XP rediseñado**: Bonus por completar 5B correctamente (no por explicar, que no es verificable)

---

## 1. Contexto y Narrativa

### Empresa Ficticia: QualityControl Systems

**Descripción**:
```
QualityControl Systems es una empresa de control de calidad industrial
que monitorea la producción de fábricas. Tienen dos máquinas que producen
piezas de precisión, y necesitan saber cuál es más CONFIABLE para
cumplir con los estándares de calidad.
```

**Contexto empresarial**:
```
María te presenta un nuevo cliente: QualityControl Systems.
La Gerente de Calidad, Laura Martínez, tiene un problema:

"Tenemos dos máquinas que producen piezas. Ambas tienen una producción
PROMEDIO de 50 unidades/hora, pero una parece más confiable que la otra.
¿Cómo podemos medir esa 'confiabilidad' con datos?"

María te explica: "Hasta ahora has usado media, mediana y moda para
entender la TENDENCIA CENTRAL de los datos. Pero eso no es suficiente.
Necesitas entender la DISPERSIÓN: ¿qué tan esparcidos están los datos?"
```

### Personajes

**Jugador**: Data Engineer trainee con experiencia en media, mediana y moda

**María González** (Mentora):
- Lead Data Engineer de DataFlow Industries
- Te presenta el concepto de dispersión
- Explica por qué la media no es suficiente
- Enseña varianza y desviación estándar

**Laura Martínez** (Gerente de Calidad en QualityControl Systems):
- Cliente que necesita medir confiabilidad de máquinas
- Quiere tomar decisiones basadas en datos
- Busca reducir defectos de producción

---

## 2. Progresión Pedagógica

### De Tendencia Central a Dispersión

**Misiones previas** (contexto del jugador):
- ✅ Misión 1: Aprendió a calcular la **media**
- ✅ Misión 2: Aprendió a calcular la **mediana** (y detectar outliers)
- ✅ Misión 3: Aprendió a calcular la **moda** (y distribuciones bimodales)

**Problema pedagógico**:
```
El jugador sabe calcular media, mediana y moda.
Pero... ¿qué pasa cuando dos datasets tienen la MISMA media
pero se comportan MUY diferente?

Ejemplo:
Dataset A: [49, 50, 51, 50, 50] → Media = 50
Dataset B: [30, 40, 50, 60, 70] → Media = 50

¿Son iguales? NO. Uno es estable, otro es variable.
```

**Solución pedagógica**:
```
Introducir el concepto de DISPERSIÓN:
- Varianza: Mide qué tan lejos están los datos de la media
- Desviación estándar: Varianza en unidades comprensibles
```

---

## 3. Escena 10: Tutorial - Introducción a la Dispersión

### Objetivo Pedagógico
Explicar **por qué la media no es suficiente** y qué mide la **dispersión**.

### Contenido de la Escena

**Pantalla 1: El Problema**
```
María: "¡Excelente trabajo con las misiones anteriores! Ya dominas
media, mediana y moda. Pero déjame mostrarte algo interesante..."

[Visualización de dos gráficos lado a lado]

Máquina A: [50, 51, 49, 50, 50, 51, 49]
Máquina B: [35, 55, 60, 40, 65, 45, 50]

María: "Ambas máquinas tienen una producción PROMEDIO de 50 unidades/hora.
¿Significa eso que son iguales?"
```

**Pantalla 2: La Dispersión**
```
María: "¡NO! Observa los gráficos:

Máquina A: ●●●●●●● (todos los puntos cerca de 50)
Máquina B: ●  ●   ●  ●   ● (puntos muy esparcidos)

La Máquina A es ESTABLE y PREDECIBLE.
La Máquina B es VARIABLE e IMPREDECIBLE.

Ambas tienen media = 50, pero se comportan MUY diferente.
¿Cómo medimos esa diferencia?"
```

**Pantalla 3: La Solución**
```
María: "Necesitamos medir la DISPERSIÓN de los datos.
La dispersión responde: ¿Qué tan ESPARCIDOS están los valores?

Herramientas:
1. VARIANZA: Mide la dispersión (en unidades²)
2. DESVIACIÓN ESTÁNDAR: Raíz cuadrada de la varianza (en unidades normales)

Analogía:
- Media = ¿Dónde está el CENTRO?
- Desviación = ¿Qué tan LEJOS del centro están los datos?
```

**Pantalla 4: Interpretación**
```
María: "Desviación estándar BAJA → Datos JUNTOS → Estable ✓
Desviación estándar ALTA → Datos DISPERSOS → Variable ⚠️

En control de calidad:
- Baja desviación = Producción CONFIABLE
- Alta desviación = Producción IMPREDECIBLE

¡Vamos a calcularlo!"

[Botón: "Iniciar Misión 5A"]
```

### Elementos Visuales
- Dos gráficos de puntos lado a lado (Máquina A vs B)
- Línea horizontal en y=50 (la media)
- Puntos de Máquina A agrupados cerca de la línea
- Puntos de Máquina B muy dispersos
- Animación sutil de "dispersión" (puntos que se alejan/acercan)

---

## 4. Misión 5A: Calcular Desviación Estándar (Básica)

### Concepto Pedagógico
Introducir la **desviación estándar** como medida de dispersión y mostrar que dos datasets con la misma media pueden tener diferente dispersión.

### Dataset

```javascript
const mision5A_maquinaA = [50, 51, 49, 50, 50, 51, 49];
const mision5A_maquinaB = [35, 55, 60, 40, 65, 45, 50];

// Análisis:
// Máquina A:
//   Media = 50.0
//   Desviación estándar ≈ 0.76 (MUY BAJA → Estable)
//
// Máquina B:
//   Media = 50.0
//   Desviación estándar ≈ 10.35 (MUY ALTA → Variable)
```

### Cálculo Manual (para referencia del diseñador)

**Máquina A**:
```
Datos: [50, 51, 49, 50, 50, 51, 49]
Media = (50+51+49+50+50+51+49)/7 = 350/7 = 50.0

Diferencias con la media:
50-50=0, 51-50=1, 49-50=-1, 50-50=0, 50-50=0, 51-50=1, 49-50=-1

Cuadrados de las diferencias:
0², 1², (-1)², 0², 0², 1², (-1)² = 0, 1, 1, 0, 0, 1, 1

Suma de cuadrados = 0+1+1+0+0+1+1 = 4
Varianza = 4/7 ≈ 0.571
Desviación estándar = √0.571 ≈ 0.76
```

**Máquina B**:
```
Datos: [35, 55, 60, 40, 65, 45, 50]
Media = (35+55+60+40+65+45+50)/7 = 350/7 = 50.0

Diferencias con la media:
35-50=-15, 55-50=5, 60-50=10, 40-50=-10, 65-50=15, 45-50=-5, 50-50=0

Cuadrados:
225, 25, 100, 100, 225, 25, 0

Suma = 700
Varianza = 700/7 = 100
Desviación estándar = √100 = 10.0
```

### Visualización

**Gráfico de Puntos con Dispersión**:
```
Máquina A (Estable):
60 |
55 |
50 | ● ● ● ● ● ● ●  ← Todos cerca de 50
45 |
40 |
   +------------------
     1 2 3 4 5 6 7 (horas)

Máquina B (Variable):
70 |       ●
65 |         ●
60 |     ●
55 |   ●
50 | ●           ●  ← Muy dispersos
45 |       ●
40 |   ●
35 | ●
   +------------------
     1 2 3 4 5 6 7 (horas)
```

**Elementos visuales**:
- Dos gráficos lado a lado
- Línea horizontal punteada en y=50 (la media)
- Puntos de Máquina A en verde (estable)
- Puntos de Máquina B en naranja (variable)
- Área sombreada de ±1 desviación estándar (opcional)

### Narrativa de la Misión

```
Laura (Gerente de Calidad): "Gracias por venir. Tengo dos máquinas
de producción. Ambas producen en promedio 50 unidades por hora, pero
sospecho que una es más confiable que la otra."

[Muestra datos de ambas máquinas]

Laura: "Necesito que calcules la DESVIACIÓN ESTÁNDAR de ambas máquinas.
Eso me dirá cuál tiene una producción más CONSISTENTE."

María (hint): "Recuerda: desviación estándar BAJA = producción ESTABLE.
Usa la calculadora para hacer los cálculos."
```

### Pregunta

**Texto**:
```
Calcula la desviación estándar de la Máquina A.
Redondea a 2 decimales.

Ejemplo: Si calculas 5.678, escribe 5.68
```

**Respuesta correcta**: `0.76` (tolerancia: ±0.1)

**Segunda pregunta** (después de responder la primera):
```
Ahora calcula la desviación estándar de la Máquina B.
Redondea a 2 decimales.
```

**Respuesta correcta**: `10.00` o `10.0` o `10` (tolerancia: ±0.5)

### Panel de Ayuda

**Contenido**:
```
📊 DATOS DE MÁQUINA A
Producción por hora: [50, 51, 49, 50, 50, 51, 49]
Cantidad de datos: 7
Media: 50.0 unidades/hora

💡 FÓRMULA
Desviación estándar = √(Σ(x - media)² / N)

📝 PASOS
1. Calcula la media (ya la tienes: 50.0)
2. Resta la media a cada valor
3. Eleva al cuadrado cada diferencia
4. Suma todos los cuadrados
5. Divide por la cantidad (N=7)
6. Saca la raíz cuadrada

🧮 USA LA CALCULADORA
Puedes usar la calculadora integrada para hacer los cálculos.
```

### Feedback Pedagógico

**Si responde correctamente (0.76 para A, 10.00 para B)**:
```
✅ ¡CORRECTO!

Máquina A: Desviación = 0.76 unidades/hora
→ Producción MUY ESTABLE (valores entre 49-51)

Máquina B: Desviación = 10.00 unidades/hora
→ Producción MUY VARIABLE (valores entre 35-65)

Interpretación:
La Máquina A es 13 veces MÁS CONFIABLE que la Máquina B
(10.00 / 0.76 ≈ 13).

Laura debería usar la Máquina A para producción crítica
y revisar/reparar la Máquina B.

+100 XP
```

**Si responde incorrectamente**:

*Error común 1: Confunde con la media*
```
❌ No es correcto.

Parece que calculaste la MEDIA (50.0), no la DESVIACIÓN ESTÁNDAR.

Recuerda:
- Media = promedio de los valores
- Desviación = qué tan lejos están del promedio

Hint: La desviación de la Máquina A es MENOR que 1.
```

*Error común 2: Olvida la raíz cuadrada*
```
❌ No es correcto.

Parece que calculaste la VARIANZA, pero olvidaste sacar la raíz cuadrada.

Recuerda:
Desviación estándar = √(Varianza)

Hint: Si tu resultado es mayor que 1, saca la raíz cuadrada.
```

*Error común 3: Valor muy alejado*
```
❌ No es correcto.

Tu respuesta está muy alejada del valor correcto.

Pasos:
1. Calcula las diferencias: (valor - media)
2. Eleva al cuadrado cada diferencia
3. Suma todos los cuadrados
4. Divide por 7 (cantidad de datos)
5. Saca la raíz cuadrada

Usa la calculadora integrada para evitar errores.
```

### Sistema de XP

- **Respuesta correcta (ambas máquinas)**: +100 XP
- **Usar hint**: -5 XP (mínimo 80 XP total)
- **Intentos ilimitados**: Sin penalización por reintentar

### Criterios de Éxito

- [ ] El jugador entiende que dos datasets con misma media pueden ser diferentes
- [ ] El jugador calcula correctamente la desviación estándar
- [ ] El jugador interpreta que desviación baja = estable, alta = variable
- [ ] El jugador completa la misión en menos de 5 minutos

---

## 5. Escena 11: Tutorial - Varianza Poblacional vs Muestral

### Objetivo Pedagógico
Explicar la diferencia entre **varianza poblacional (÷N)** y **varianza muestral (÷N-1)**, y por qué usamos N-1 (corrección de Bessel).

### Contenido de la Escena

**Pantalla 1: El Problema**
```
María: "¡Excelente! Ya sabes calcular la desviación estándar.
Pero hay un detalle importante que debes conocer..."

María: "Cuando calculas la varianza, ¿divides por N o por N-1?
Depende de si tienes la POBLACIÓN COMPLETA o solo una MUESTRA."
```

**Pantalla 2: Población vs Muestra**
```
María: "Imagina que quieres saber la altura promedio de TODOS
los estudiantes de una universidad (10,000 personas).

OPCIÓN A: Medir a los 10,000 → POBLACIÓN COMPLETA
OPCIÓN B: Medir a 100 → MUESTRA

En Data Engineering, casi siempre trabajas con MUESTRAS,
no con poblaciones completas."
```

**Pantalla 3: La Corrección de Bessel**
```
María: "Cuando tienes una MUESTRA, la varianza tiende a ser
MENOR que la varianza real de la población.

¿Por qué? Porque tu muestra probablemente no incluye los valores
más extremos de la población.

SOLUCIÓN: Dividir por (N-1) en lugar de N.
Esto se llama 'corrección de Bessel' y hace que la estimación
sea más precisa."
```

**Pantalla 4: Fórmulas**
```
María: "Dos fórmulas:

VARIANZA POBLACIONAL (tienes TODOS los datos):
Varianza = Σ(x - media)² / N

VARIANZA MUESTRAL (tienes una MUESTRA):
Varianza = Σ(x - media)² / (N-1)

Regla práctica:
- ¿Tienes TODOS los datos? → Usa N
- ¿Es una muestra? → Usa N-1

En la siguiente misión, trabajarás con una MUESTRA.
¡Usa N-1!"

[Botón: "Iniciar Misión 5B"]
```

### Elementos Visuales
- Ilustración de población (muchos puntos) vs muestra (pocos puntos seleccionados)
- Tabla comparativa de fórmulas (N vs N-1)
- Ejemplo numérico simple mostrando la diferencia

---

## 6. Misión 5B: Varianza Muestral (Avanzada)

### Concepto Pedagógico
Aplicar el concepto de **varianza muestral (÷N-1)** en un contexto realista y entender cuándo usar N vs N-1.

### Dataset

```javascript
const mision5B_muestra = [47, 50, 48, 51, 49];

// Análisis:
// Muestra de n=5 tiempos de respuesta (en milisegundos)
// Media = 49.0 ms
// Varianza POBLACIONAL (÷5) = 2.0
// Varianza MUESTRAL (÷4) = 2.5  ← RESPUESTA CORRECTA
// Desviación estándar muestral = √2.5 ≈ 1.58 ms
```

### Cálculo Manual (para referencia)

```
Datos: [47, 50, 48, 51, 49]
n = 5 (muestra)

Paso 1: Media
Media = (47+50+48+51+49)/5 = 245/5 = 49.0

Paso 2: Diferencias con la media
47-49 = -2
50-49 = 1
48-49 = -1
51-49 = 2
49-49 = 0

Paso 3: Cuadrados
(-2)² = 4
(1)² = 1
(-1)² = 1
(2)² = 4
(0)² = 0

Paso 4: Suma de cuadrados
4 + 1 + 1 + 4 + 0 = 10

Paso 5: Varianza MUESTRAL (÷N-1)
Varianza = 10 / (5-1) = 10 / 4 = 2.5  ← CORRECTO

(Si usara N: 10/5 = 2.0 ← INCORRECTO para muestra)
```

### Visualización

**Campana Gaussiana con Área Sombreada**:
```
        Distribución Normal

    |     ╱‾‾‾╲
    |    ╱     ╲
    |   ╱  ±1σ  ╲
    |  ╱█████████╲
    | ╱███████████╲
    |╱_____________╲___
      45  47  49  51  53
           ↑
         Media

█ = Área sombreada (68% de los datos)
σ = Desviación estándar
```

**Elementos visuales**:
- Campana gaussiana centrada en la media (49)
- Área sombreada de ±1 desviación estándar (verde claro)
- Puntos de la muestra marcados en el eje X
- Etiquetas: "Media = 49.0", "σ ≈ 1.58"

### Narrativa de la Misión

```
Laura: "Perfecto, ahora necesito tu ayuda con otro análisis.
Hemos tomado una MUESTRA de 5 mediciones de tiempo de respuesta
de nuestro sistema de calidad."

[Muestra datos: 47, 50, 48, 51, 49 milisegundos]

Laura: "Necesito que calcules la VARIANZA MUESTRAL de estos datos.
Recuerda: como es una MUESTRA, debes usar (N-1) en el denominador."

María (hint): "Recuerda la fórmula:
Varianza muestral = Σ(x - media)² / (N-1)

En este caso, N=5, así que divides por 4."
```

### Pregunta

**Texto**:
```
Calcula la VARIANZA MUESTRAL de los datos.
Recuerda: usa (N-1) en el denominador.

Datos: [47, 50, 48, 51, 49]
Redondea a 1 decimal.

Ejemplo: Si calculas 2.456, escribe 2.5
```

**Respuesta correcta**: `2.5` (tolerancia: ±0.2)

### Panel de Ayuda

**Contenido**:
```
📊 DATOS DE LA MUESTRA
Tiempos de respuesta (ms): [47, 50, 48, 51, 49]
Tamaño de la muestra: n = 5
Media: 49.0 ms

💡 FÓRMULA (MUESTRAL)
Varianza = Σ(x - media)² / (N-1)
           ↑
    Divide por (N-1), NO por N

📝 PASOS
1. Calcula la media (ya la tienes: 49.0)
2. Resta la media a cada valor
3. Eleva al cuadrado cada diferencia
4. Suma todos los cuadrados
5. Divide por (N-1) = 4  ← ¡Importante!

⚠️ NOTA
Si divides por N=5, obtendrás 2.0 (incorrecto).
Si divides por N-1=4, obtendrás 2.5 (correcto).
```

### Feedback Pedagógico

**Si responde correctamente (2.5)**:
```
✅ ¡EXCELENTE!

Varianza muestral = 2.5 ms²
Desviación estándar = √2.5 ≈ 1.58 ms

Interpretación:
Los tiempos de respuesta varían ±1.58 ms del promedio (49 ms).
Esto indica un sistema MUY ESTABLE (baja variabilidad).

¿Por qué N-1?
Al usar (N-1) en lugar de N, compensamos el hecho de que
una muestra tiende a subestimar la variabilidad real de
la población completa.

Esto se llama "corrección de Bessel" y es fundamental
en estadística inferencial.

+150 XP
+25 XP BONUS por usar correctamente N-1
```

**Si responde incorrectamente**:

*Error común 1: Usó N en lugar de N-1*
```
❌ No es correcto.

Parece que dividiste por N=5 en lugar de (N-1)=4.

Recuerda:
- Varianza POBLACIONAL → Divide por N
- Varianza MUESTRAL → Divide por (N-1)

Como estos datos son una MUESTRA, debes dividir por 4.

Hint: Tu respuesta debería ser mayor que 2.0
```

*Error común 2: Calculó la desviación en lugar de varianza*
```
❌ No es correcto.

Parece que calculaste la DESVIACIÓN ESTÁNDAR (√varianza),
pero la pregunta pide la VARIANZA.

Recuerda:
- Varianza = Σ(x - media)² / (N-1)
- Desviación = √(Varianza)

Hint: La varianza es mayor que la desviación.
```

*Error común 3: Error de cálculo*
```
❌ No es correcto.

Revisa tus cálculos paso a paso:

1. Media = 49.0 ✓
2. Diferencias: [-2, 1, -1, 2, 0]
3. Cuadrados: [4, 1, 1, 4, 0]
4. Suma: 10
5. Divide por (N-1) = 4

Resultado: 10/4 = 2.5

Usa la calculadora para evitar errores.
```

### Sistema de XP

- **Respuesta correcta**: +150 XP
- **Bonus por usar N-1 correctamente**: +25 XP
- **Total**: 175 XP
- **Usar hint**: -10 XP (mínimo 140 XP total)

### Criterios de Éxito

- [ ] El jugador entiende la diferencia entre varianza poblacional y muestral
- [ ] El jugador usa correctamente (N-1) en el denominador
- [ ] El jugador interpreta el resultado en contexto
- [ ] El jugador completa la misión en menos de 7 minutos

---

## 7. Sistema de Progresión y Desbloqueo

### Flujo de Misiones

```
Misión 3B (Moda Bimodal) → Completada
         ↓
    Escena 10 (Tutorial: Dispersión)
         ↓
    Misión 5A (Desviación Estándar)
         ↓
    Escena 11 (Tutorial: N vs N-1)
         ↓
    Misión 5B (Varianza Muestral)
         ↓
    [Siguiente: Misión 4 o Módulo 2]
```

### Desbloqueo

- **Escena 10**: Se desbloquea automáticamente al completar Misión 3B
- **Misión 5A**: Se desbloquea al terminar Escena 10
- **Escena 11**: Se desbloquea al completar Misión 5A
- **Misión 5B**: Se desbloquea al terminar Escena 11

### XP Acumulado

```
Antes de Misión 5:
- Misión 1: 100 XP
- Misión 2A: 75 XP
- Misión 2B: 125 XP
- Misión 3A: 100 XP
- Misión 3B: 175 XP
Total: 575 XP

Después de Misión 5:
- Misión 5A: +100 XP
- Misión 5B: +175 XP (150 + 25 bonus)
Total: 850 XP
```

---

## 8. Funciones JavaScript Necesarias

### Función: calcularDesviacionEstandar()

```javascript
/**
 * Calcula la desviación estándar de un array de números
 * @param {number[]} datos - Array de números
 * @param {boolean} muestral - Si es true, usa N-1 (muestral), si es false usa N (poblacional)
 * @returns {number} Desviación estándar
 */
function calcularDesviacionEstandar(datos, muestral = false) {
    if (datos.length === 0) return 0;

    // Calcular media
    const media = datos.reduce((sum, val) => sum + val, 0) / datos.length;

    // Calcular suma de diferencias al cuadrado
    const sumaCuadrados = datos.reduce((sum, val) => {
        const diferencia = val - media;
        return sum + (diferencia * diferencia);
    }, 0);

    // Calcular varianza (poblacional o muestral)
    const divisor = muestral ? (datos.length - 1) : datos.length;
    const varianza = sumaCuadrados / divisor;

    // Desviación estándar es la raíz cuadrada de la varianza
    return Math.sqrt(varianza);
}
```

### Función: calcularVarianza()

```javascript
/**
 * Calcula la varianza de un array de números
 * @param {number[]} datos - Array de números
 * @param {boolean} muestral - Si es true, usa N-1 (muestral), si es false usa N (poblacional)
 * @returns {number} Varianza
 */
function calcularVarianza(datos, muestral = false) {
    if (datos.length === 0) return 0;

    const media = datos.reduce((sum, val) => sum + val, 0) / datos.length;
    const sumaCuadrados = datos.reduce((sum, val) => {
        const diferencia = val - media;
        return sum + (diferencia * diferencia);
    }, 0);

    const divisor = muestral ? (datos.length - 1) : datos.length;
    return sumaCuadrados / divisor;
}
```

### Función: startMission5A()

```javascript
function startMission5A() {
    currentMission = '5A';

    // Datos de las máquinas
    const maquinaA = [50, 51, 49, 50, 50, 51, 49];
    const maquinaB = [35, 55, 60, 40, 65, 45, 50];

    // Calcular respuestas correctas
    const respuestaA = calcularDesviacionEstandar(maquinaA, false); // 0.76
    const respuestaB = calcularDesviacionEstandar(maquinaB, false); // 10.00

    // Mostrar pantalla de misión
    showScreen('mission5A-screen');

    // Cargar visualización
    loadScatterPlotMission5A(maquinaA, maquinaB);

    // Actualizar panel de ayuda
    updateHelperMission5A(maquinaA);
}
```

### Función: checkAnswerMission5A()

```javascript
function checkAnswerMission5A() {
    const userAnswer = parseFloat(document.getElementById('answer-5a').value);
    const currentQuestion = gameState.mission5A_question || 'A';

    if (currentQuestion === 'A') {
        const correctAnswer = 0.76;
        const tolerance = 0.1;

        if (Math.abs(userAnswer - correctAnswer) <= tolerance) {
            showFeedback('correct', '✅ ¡Correcto! Máquina A tiene desviación = 0.76 (muy estable).');
            gameState.mission5A_question = 'B';
            document.getElementById('question-5a').textContent =
                'Ahora calcula la desviación estándar de la Máquina B.';
            document.getElementById('answer-5a').value = '';
            updateHelperMission5A([35, 55, 60, 40, 65, 45, 50]); // Cambiar a datos de B
        } else {
            showFeedback('incorrect', detectErrorMission5A(userAnswer, correctAnswer));
        }
    } else if (currentQuestion === 'B') {
        const correctAnswer = 10.00;
        const tolerance = 0.5;

        if (Math.abs(userAnswer - correctAnswer) <= tolerance) {
            showFeedback('correct', `
                ✅ ¡EXCELENTE!

                Máquina A: Desviación = 0.76 → MUY ESTABLE ✓
                Máquina B: Desviación = 10.00 → MUY VARIABLE ⚠️

                La Máquina A es 13 veces más confiable que la B.

                +100 XP
            `);
            giveXP(100);
            gameState.completedMissions.push('5A');
            unlockScene(11); // Desbloquear tutorial de N vs N-1
        } else {
            showFeedback('incorrect', detectErrorMission5A(userAnswer, correctAnswer));
        }
    }
}
```

### Función: loadScatterPlotMission5A()

```javascript
function loadScatterPlotMission5A(maquinaA, maquinaB) {
    const container = document.getElementById('chart-mission5a');

    // Crear dos gráficos lado a lado
    const html = `
        <div class="scatter-plots">
            <div class="scatter-plot">
                <h4>Máquina A (Estable)</h4>
                <div class="plot-area">
                    ${maquinaA.map((val, idx) => `
                        <div class="scatter-point"
                             style="left: ${idx * 14}%; bottom: ${(val-35)/35*100}%"
                             data-value="${val}">
                            <span class="point-label">${val}</span>
                        </div>
                    `).join('')}
                    <div class="mean-line" style="bottom: ${(50-35)/35*100}%">
                        <span>Media = 50</span>
                    </div>
                </div>
            </div>

            <div class="scatter-plot">
                <h4>Máquina B (Variable)</h4>
                <div class="plot-area">
                    ${maquinaB.map((val, idx) => `
                        <div class="scatter-point orange"
                             style="left: ${idx * 14}%; bottom: ${(val-35)/35*100}%"
                             data-value="${val}">
                            <span class="point-label">${val}</span>
                        </div>
                    `).join('')}
                    <div class="mean-line" style="bottom: ${(50-35)/35*100}%">
                        <span>Media = 50</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
}
```

---

## 9. Estilos CSS Necesarios

### Gráfico de Dispersión

```css
.scatter-plots {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.scatter-plot {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 1.5rem;
}

.scatter-plot h4 {
    text-align: center;
    margin-bottom: 1rem;
    color: #fff;
}

.plot-area {
    position: relative;
    height: 300px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    border-left: 2px solid rgba(255, 255, 255, 0.3);
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.scatter-point {
    position: absolute;
    width: 12px;
    height: 12px;
    background: #00ff88;
    border-radius: 50%;
    transform: translate(-50%, 50%);
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}

.scatter-point.orange {
    background: #ff9500;
    box-shadow: 0 0 10px rgba(255, 149, 0, 0.5);
}

.scatter-point:hover {
    transform: translate(-50%, 50%) scale(1.5);
}

.scatter-point:hover .point-label {
    display: block;
}

.point-label {
    display: none;
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
    padding: 4px 8px;
    border-radius: 5px;
    font-size: 12px;
    white-space: nowrap;
}

.mean-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background: rgba(255, 255, 255, 0.5);
    border-top: 2px dashed rgba(255, 255, 255, 0.7);
}

.mean-line span {
    position: absolute;
    right: 10px;
    top: -20px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.8);
}
```

### Campana Gaussiana (Misión 5B)

```css
.gaussian-chart {
    position: relative;
    height: 300px;
    margin: 2rem 0;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 2rem;
}

.gaussian-curve {
    position: relative;
    height: 200px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
}

.gaussian-bar {
    width: 3%;
    background: linear-gradient(to top, #00ff88, transparent);
    margin: 0 1px;
    transition: all 0.3s ease;
}

.gaussian-bar.shaded {
    background: linear-gradient(to top, rgba(0, 255, 136, 0.5), transparent);
}

.gaussian-axis {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
    padding: 0 2rem;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
}

.gaussian-label {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.7);
    padding: 10px 20px;
    border-radius: 10px;
    color: #fff;
    font-size: 14px;
}
```

---

## 10. Criterios de Validación

### Misión 5A

| Aspecto                 | Criterio       | Validación                            |
| ----------------------- | -------------- | ------------------------------------- |
| **Respuesta Máquina A** | 0.76 ± 0.1     | `Math.abs(userAnswer - 0.76) <= 0.1`  |
| **Respuesta Máquina B** | 10.00 ± 0.5    | `Math.abs(userAnswer - 10.00) <= 0.5` |
| **Formato**             | Número decimal | `!isNaN(parseFloat(userAnswer))`      |
| **Redondeo**            | 2 decimales    | Aceptar 0.76, 0.8, .76                |

### Misión 5B

| Aspecto        | Criterio               | Validación                          |
| -------------- | ---------------------- | ----------------------------------- |
| **Respuesta**  | 2.5 ± 0.2              | `Math.abs(userAnswer - 2.5) <= 0.2` |
| **Formato**    | Número decimal         | `!isNaN(parseFloat(userAnswer))`    |
| **Redondeo**   | 1 decimal              | Aceptar 2.5, 2.50                   |
| **Uso de N-1** | Implícito en respuesta | Si responde 2.0, detectar error     |

---

## 11. Testing Manual - Checklist

### Escena 10 (Tutorial Dispersión)
- [ ] Se muestra correctamente después de Misión 3B
- [ ] Los gráficos de Máquina A y B se visualizan correctamente
- [ ] La explicación es clara y comprensible
- [ ] El botón "Iniciar Misión 5A" funciona
- [ ] Keyboard navigation funciona (Enter para avanzar)

### Misión 5A
- [ ] Los datos de ambas máquinas se muestran correctamente
- [ ] El gráfico de dispersión se renderiza bien
- [ ] La calculadora funciona para hacer cálculos
- [ ] El panel de ayuda muestra información útil
- [ ] La primera pregunta (Máquina A) valida correctamente
- [ ] Al responder correctamente, cambia a pregunta de Máquina B
- [ ] La segunda pregunta (Máquina B) valida correctamente
- [ ] El feedback es claro y pedagógico
- [ ] Se otorgan 100 XP al completar
- [ ] Se desbloquea Escena 11

### Escena 11 (Tutorial N vs N-1)
- [ ] Se muestra correctamente después de Misión 5A
- [ ] La explicación de población vs muestra es clara
- [ ] La tabla comparativa de fórmulas se ve bien
- [ ] El ejemplo numérico es comprensible
- [ ] El botón "Iniciar Misión 5B" funciona

### Misión 5B
- [ ] Los datos de la muestra se muestran correctamente
- [ ] La campana gaussiana se renderiza bien
- [ ] El panel de ayuda enfatiza usar N-1
- [ ] La validación detecta si usó N en lugar de N-1
- [ ] El feedback explica por qué N-1
- [ ] Se otorgan 150 XP + 25 XP bonus
- [ ] Se marca como completada en el progreso

### Casos de Error
- [ ] Error: Confunde media con desviación (5A)
- [ ] Error: Olvida raíz cuadrada (5A)
- [ ] Error: Usa N en lugar de N-1 (5B)
- [ ] Error: Calcula desviación en lugar de varianza (5B)
- [ ] Feedback específico para cada tipo de error

### Accesibilidad
- [ ] ARIA labels en elementos interactivos
- [ ] Navegación por teclado funciona
- [ ] Focus visible en inputs y botones
- [ ] Screen reader puede leer el contenido

### Responsive
- [ ] Funciona en desktop (1920x1080)
- [ ] Funciona en tablet (768x1024)
- [ ] Funciona en móvil (375x667)
- [ ] Los gráficos se adaptan al tamaño de pantalla

---

## 12. Archivos a Modificar

### documentacion/juego/game.html
**Secciones a añadir**:
1. Escena 10 (Tutorial Dispersión) - ~100 líneas
2. Misión 5A (Desviación Estándar) - ~200 líneas
3. Escena 11 (Tutorial N vs N-1) - ~100 líneas
4. Misión 5B (Varianza Muestral) - ~200 líneas
5. Funciones JavaScript - ~300 líneas
6. Estilos CSS - ~150 líneas

**Total estimado**: ~1,050 líneas nuevas

### documentacion/juego/README_JUEGO_WEB.md
**Secciones a actualizar**:
- Añadir Misión 5A y 5B en "Lo Que Tiene Ahora"
- Actualizar XP total disponible (575 → 850 XP)
- Actualizar roadmap (marcar Misión 5 como completada)

### documentacion/CHANGELOG.md
**Entrada a añadir**:
```markdown
- **JAR-183: Misión 5 del Juego - Varianza y Desviación Estándar** (2025-10-XX):
  - ✅ Misión 5A: Introducción a la dispersión
  - ✅ Misión 5B: Varianza poblacional vs muestral
  - ✅ Tutorial sobre corrección de Bessel (N vs N-1)
  - ✅ Visualizaciones: gráfico de dispersión y campana gaussiana
  - Total: +275 XP (850 XP disponibles en el juego)
```

---

## 13. Resumen de Mejoras Pedagógicas Aplicadas

### Cambios Respecto al Diseño Inicial

| Aspecto         | Diseño Inicial                        | Diseño Final (Mejorado)                            |
| --------------- | ------------------------------------- | -------------------------------------------------- |
| **Pregunta 5A** | "¿Cuál es más confiable?" (subjetivo) | "Calcula la desviación de AMBAS" (objetivo)        |
| **Escena 10**   | Tutorial básico                       | Tutorial robusto con analogías y ejemplos visuales |
| **Misión 5B**   | Calcular + explicar N-1               | Solo calcular, tutorial explica N-1                |
| **Bonus XP**    | Por explicar (no verificable)         | Por completar correctamente (verificable)          |
| **Feedback**    | Genérico                              | Específico por tipo de error común                 |

### Calificación Pedagógica Final

**Antes de mejoras**: 8.5/10
**Después de mejoras**: 9.2/10 (esperado)

**Justificación**:
- ✅ Progresión lógica sin saltos conceptuales
- ✅ Preguntas objetivas y verificables
- ✅ Tutoriales robustos con analogías claras
- ✅ Feedback pedagógico específico
- ✅ Visualizaciones que enseñan, no solo decoran

---

## 14. Próximos Pasos

### Workflow de Implementación

1. **✅ COMPLETADO**: Diseño de mecánica (este documento)
2. **✅ COMPLETADO**: Revisión pedagógica (Teaching Team)
3. **SIGUIENTE**: Implementación en `game.html` por @game-design [frontend]
4. **PENDIENTE**: Revisión UX/UI por @game-design [ux]
5. **PENDIENTE**: Testing manual por @quality
6. **PENDIENTE**: Actualizar README_JUEGO_WEB.md por @documentation
7. **PENDIENTE**: Actualizar CHANGELOG.md por @documentation
8. **PENDIENTE**: Marcar JAR-183 como Done en Linear por @project-management

### Estimación de Tiempo

- **Implementación frontend**: 4-5 horas
- **Revisión UX/UI**: 1 hora
- **Testing manual**: 1-2 horas
- **Documentación**: 30 minutos
- **Total**: 6-8 horas

---

## 15. Referencias y Recursos

### Archivos del Proyecto
- **Juego principal**: `documentacion/juego/game.html`
- **README del juego**: `documentacion/juego/README_JUEGO_WEB.md`
- **Empresas ficticias**: `documentacion/juego/EMPRESAS_FICTICIAS.md`
- **CHANGELOG**: `documentacion/CHANGELOG.md`

### Issues Relacionadas
- **JAR-180**: Misión 2 (Mediana) - ✅ Completada
- **JAR-181**: Misión 3 (Moda) - ✅ Completada
- **JAR-182**: Misión 4 (Percentiles) - ⏳ Pendiente
- **JAR-183**: Misión 5 (Varianza) - 🔄 Este diseño

### Conceptos Pedagógicos
- **Dispersión**: Qué tan esparcidos están los datos
- **Varianza**: Medida de dispersión (en unidades²)
- **Desviación estándar**: Raíz cuadrada de la varianza (en unidades normales)
- **Varianza poblacional**: Divide por N (tienes todos los datos)
- **Varianza muestral**: Divide por N-1 (tienes una muestra)
- **Corrección de Bessel**: Por qué usamos N-1 en muestras

### Material Teórico Disponible
- `modulo-01-fundamentos/tema-1-python-estadistica/01-TEORIA.md` (Parte 2: Medidas de Dispersión)
- `modulo-01-fundamentos/tema-1-python-estadistica/02-EJEMPLOS.md` (Ejemplo 1: Desviación estándar)
- `modulo-01-fundamentos/tema-1-python-estadistica/03-EJERCICIOS.md` (Ejercicios 6, 7, 10, 12)

### Funciones Python Implementadas
- `calcular_varianza(datos: List[Union[int, float]]) -> float`
- `calcular_desviacion_estandar(datos: List[Union[int, float]]) -> float`
- Tests: 51/51 pasando (100%)
- Cobertura: 89%

---

## Aprobaciones

### Diseño de Juego
- [x] **Diseñador de Juegos**: Diseño completo con narrativa, mecánicas y XP
- [x] **Fecha**: 2025-10-20

### Pedagogía
- [x] **Pedagogo**: Revisión pedagógica completada con mejoras aplicadas
- [x] **Calificación**: 9.2/10 (esperado)
- [x] **Veredicto**: APROBADO PARA IMPLEMENTACIÓN
- [x] **Fecha**: 2025-10-20

### Pendientes
- [ ] **Desarrollador Frontend**: Implementación en game.html
- [ ] **Especialista UX/UI**: Revisión de usabilidad
- [ ] **Quality Assurance**: Testing manual completo
- [ ] **Documentador**: Actualización de README y CHANGELOG
- [ ] **Project Manager**: Cierre de issue en Linear

---

**Documento creado por**: Game Design Team + Teaching Team
**Fecha**: 2025-10-20
**Versión**: 2.0 (con mejoras pedagógicas)
**Estado**: ✅ Diseño Completo - Aprobado para Implementación

---

## Notas Finales

Este diseño incorpora las mejoras sugeridas por el equipo pedagógico para asegurar que la Misión 5 enseñe efectivamente los conceptos de varianza y desviación estándar. Las preguntas son objetivas y verificables, los tutoriales son robustos, y el feedback es específico por tipo de error.

La misión sigue el patrón establecido por las misiones anteriores (2 submisiones con tutoriales integrados) y mantiene la calidad pedagógica esperada (>9.0/10).

**¡Listo para implementación! 🚀**
