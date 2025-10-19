# 📚 Revisión Pedagógica: Misión 2 - Mediana y Outliers

**Fecha**: 2025-10-19
**Revisor**: Psicólogo Educativo (Equipo Teaching)
**Archivo revisado**: `documentacion/juego/game.html` (Misión 2A y 2B)
**Objetivo**: Validar que la Misión 2 enseña correctamente los conceptos de **mediana** y **outliers**

---

## ✅ Fortalezas Pedagógicas

### 1. Progresión Lógica Excelente
- ✅ **Secuencia natural**: Tutorial → Misión Básica (2A) → Misión Compleja (2B)
- ✅ **Construcción sobre conocimiento previo**: Asume que el jugador ya completó la Misión 1 (media)
- ✅ **Comparación explícita**: Contrasta media vs mediana para mostrar ventajas

### 2. Contexto Narrativo Significativo
- ✅ **Continuidad**: Usa el mismo cliente (RestaurantData Co.) de la Misión 1
- ✅ **Problema real**: Errores en sistemas de ventas son situaciones empresariales auténticas
- ✅ **Motivación clara**: El jugador entiende POR QUÉ necesita aprender mediana (outliers distorsionan la media)

### 3. Explicación Clara de Conceptos

#### Mediana (Escena 5)
```
✅ Definición simple: "valor del medio cuando ordenas los datos"
✅ Pasos concretos: Ordenar → Cantidad impar/par → Tomar centro
✅ Ejemplo trabajado: [50, 55, 52, 58, 500, 60, 57] → Mediana = 57€
✅ Comparación: Media = 118.86€ vs Mediana = 57€
✅ Ventaja explicada: "NO se ve afectada por outliers"
```

#### Outliers (Escena 5)
```
✅ Definición simple: "valores muy diferentes al resto"
✅ Tipos explicados: Errores vs Casos especiales
✅ Problema identificado: "distorsionan la media"
✅ Visualización: Destacados en rojo en gráficos
```

#### Regla IQR (Escena 7)
```
✅ Contexto: "outliers no tan obvios"
✅ Método estructurado: 4 pasos claros
✅ Fórmula explicada: [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
✅ Aplicación práctica: "método estadístico profesional"
```

### 4. Feedback Pedagógico de Calidad

#### Respuesta Correcta (Misión 2A)
```javascript
✅ Celebración personalizada: "¡EXCELENTE, ${playerName}!"
✅ Datos concretos: Mediana = 57€, Media = 118.86€
✅ Interpretación: "¿Ves la diferencia?"
✅ Contexto narrativo: María explica la decisión de negocio
✅ Recompensa clara: +75 XP
✅ Progresión: Botón para continuar a Misión 2B
```

#### Respuesta Incorrecta (Misión 2A)
```javascript
✅ Tono constructivo: "Recuerda que..."
✅ Hint específico: "Ordena los valores primero: 50, 52, 55, 57, 58, 60, 500"
✅ Pregunta guiada: "¿Cuál es el valor del centro?"
✅ No da la respuesta directa (permite aprender)
```

### 5. Implementación Técnica Correcta

#### Función `calcularMediana()`
```javascript
✅ Ordena correctamente: [...datos].sort((a, b) => a - b)
✅ Maneja cantidad par: promedio de los dos del centro
✅ Maneja cantidad impar: valor del centro
✅ Usa Math.floor() correctamente para índices
```

#### Función `detectarOutliersIQR()`
```javascript
✅ Calcula Q1 y Q3 correctamente (percentiles 25 y 75)
✅ Calcula IQR: Q3 - Q1
✅ Aplica regla estándar: 1.5 × IQR
✅ Retorna índices de outliers (útil para visualización)
```

### 6. Datasets Pedagógicamente Diseñados

#### Misión 2A (Básica)
```javascript
mision2A_ventas = [50, 60, 55, 58, 500, 52, 57]
✅ Outlier evidente: 500€ (10x el valor típico)
✅ Fácil de identificar visualmente
✅ Cantidad impar (7 valores) → Mediana clara (57€)
✅ Contraste dramático: Media = 118.86€ vs Mediana = 57€
```

#### Misión 2B (Compleja)
```javascript
mision2B_ventas = [120, 135, 128, 200, 125, 132, 210, 130, 122]
✅ Outliers sutiles: 200€ y 210€ (no tan obvios)
✅ Requiere método IQR para detectar
✅ Cantidad impar (9 valores) → Mediana = 130€
✅ Dataset más grande (9 vs 7) → Mayor complejidad
```

### 7. Visualización Efectiva
- ✅ **Outliers en rojo**: Identificación visual inmediata
- ✅ **Valores normales en azul/morado**: Contraste claro
- ✅ **Detección automática**: El jugador ve los outliers antes de calcular
- ✅ **Gráfico de barras**: Facilita comparación de magnitudes

### 8. Gamificación Saludable
- ✅ **XP progresivo**: 75 XP (básica) → 125 XP (compleja)
- ✅ **Desbloqueo lógico**: 2B solo después de completar 2A
- ✅ **Recompensa por aprendizaje**: XP por respuesta correcta, no por intentos
- ✅ **Sin penalización**: Intentos ilimitados sin perder XP

---

## ⚠️ Áreas de Mejora

### Problema 1: Cálculo de Percentiles en `detectarOutliersIQR()`
**Ubicación**: Líneas 1465-1484 (función `detectarOutliersIQR`)

**Problema**:
```javascript
const q1Index = Math.floor(n * 0.25);
const q3Index = Math.floor(n * 0.75);
const q1 = ordenados[q1Index];
const q3 = ordenados[q3Index];
```

El cálculo de percentiles usando índices directos (`n * 0.25`) es una **aproximación simplificada**. Para el dataset de Misión 2B:

```javascript
mision2B_ventas = [120, 135, 128, 200, 125, 132, 210, 130, 122]
Ordenados: [120, 122, 125, 128, 130, 132, 135, 200, 210]
n = 9

q1Index = Math.floor(9 * 0.25) = Math.floor(2.25) = 2
q3Index = Math.floor(9 * 0.75) = Math.floor(6.75) = 6

Q1 = ordenados[2] = 125
Q3 = ordenados[6] = 135
IQR = 135 - 125 = 10

Límite inferior = 125 - 1.5 × 10 = 110
Límite superior = 135 + 1.5 × 10 = 150

Outliers: 200 (índice 7) y 210 (índice 8) ✅
```

**Impacto**:
- Para este dataset específico, **funciona correctamente** y detecta los outliers esperados (200€ y 210€)
- Sin embargo, el método es **pedagógicamente incompleto** porque:
  - No explica que hay múltiples métodos para calcular percentiles
  - Puede dar resultados diferentes a calculadoras estadísticas profesionales
  - No menciona la interpolación entre valores

**Sugerencia**:
Añadir un comentario en el código explicando la simplificación:

```javascript
// Detectar outliers usando regla IQR (Interquartile Range)
// NOTA: Este método usa una aproximación simplificada de percentiles
// (método de índice directo). Para datasets pequeños es suficiente.
function detectarOutliersIQR(datos) {
    const ordenados = [...datos].sort((a, b) => a - b);
    const n = ordenados.length;

    // Calcular Q1 (percentil 25) y Q3 (percentil 75)
    // Método simplificado: índice = floor(n × percentil)
    const q1Index = Math.floor(n * 0.25);
    const q3Index = Math.floor(n * 0.75);
    const q1 = ordenados[q1Index];
    const q3 = ordenados[q3Index];
    const iqr = q3 - q1;

    // Límites para outliers (regla estándar: 1.5 × IQR)
    const limiteInferior = q1 - 1.5 * iqr;
    const limiteSuperior = q3 + 1.5 * iqr;

    // Retornar índices de outliers en el array original
    return datos.map((valor, index) =>
        valor < limiteInferior || valor > limiteSuperior ? index : null
    ).filter(index => index !== null);
}
```

**Prioridad**: 🟡 Media (funciona correctamente, pero podría ser más educativo)

---

### Problema 2: Detección de Outliers en Misión 2A (Método Inconsistente)
**Ubicación**: Líneas 1890-1891 (función `startMission2A`)

**Problema**:
```javascript
const mediana = calcularMediana(mision2A_ventas);
const outliers = mision2A_ventas.map((v, i) => v > mediana * 5 ? i : null).filter(i => i !== null);
```

La Misión 2A usa un método **ad-hoc** (valor > 5× mediana) en lugar de la regla IQR.

**Impacto**:
- ✅ **Funciona para este dataset**: 500€ > 57€ × 5 (285€) → Detecta el outlier
- ⚠️ **Inconsistencia pedagógica**: La Escena 7 enseña la regla IQR, pero la Misión 2A usa otro método
- ⚠️ **Confusión potencial**: Un estudiante avanzado podría notar la discrepancia

**Justificación del diseño actual**:
- La Misión 2A es **básica** y el outlier es **evidente** (500€ vs ~55€)
- Usar IQR aquí sería **excesivo** para el nivel de dificultad
- El método "5× mediana" es **intuitivo** y **suficiente** para outliers evidentes

**Sugerencia**:
Añadir una explicación en la Escena 6 (introducción a Misión 2A) que mencione que hay diferentes métodos:

```html
<div class="tutorial-box">
    <div class="tutorial-title">💡 Recuerda</div>
    <div class="tutorial-content">
        <strong>Mediana:</strong> Ordena los datos y toma el valor del medio.
        <br><br>
        Los valores <strong style="color: #ff4757;">rojos</strong> en el gráfico son outliers detectados
        automáticamente. En esta misión, el outlier es <strong>muy evidente</strong>
        (mucho mayor que el resto).
        <br><br>
        <em>En la próxima misión aprenderás un método más sofisticado para detectar outliers sutiles.</em>
        <br><br>
        Usa la <strong>calculadora</strong> y el <strong>panel de ayuda</strong> para resolver.
    </div>
</div>
```

**Prioridad**: 🟢 Baja (el diseño actual es pedagógicamente válido para una progresión básica → avanzada)

---

### Problema 3: Falta de Explicación sobre "Ignorar Outliers"
**Ubicación**: Escena 7 (Tutorial Misión 2B)

**Problema**:
La Escena 7 menciona:
> "Tu tarea: calcula la mediana de TODAS las ventas (incluyendo outliers)"

Pero luego en el feedback de Misión 2B dice:
> "Decisión de negocio: Investigar sucursales 4, 7 antes de tomar decisiones basadas en la media."

**Impacto**:
- ⚠️ **Ambigüedad**: No queda claro si la mediana se calcula CON o SIN outliers
- ⚠️ **Confusión conceptual**: La mediana es robusta a outliers, pero ¿debemos excluirlos o no?

**Clarificación técnica**:
En estadística, la **mediana se calcula con todos los valores** (incluyendo outliers). Su ventaja es que **no se ve afectada** por ellos, no que los excluya.

**Sugerencia**:
Aclarar en la Escena 7:

```html
<div class="tutorial-box">
    <div class="tutorial-title">🎯 Tu Tarea</div>
    <div class="tutorial-content">
        Calcula la <strong>mediana</strong> de TODAS las ventas (incluyendo outliers).
        <br><br>
        <strong>Importante:</strong> La mediana NO excluye outliers, simplemente
        <strong style="color: #32cd32;">no se ve afectada</strong> por ellos.
        <br><br>
        Después de calcularla, verás cómo la mediana te da una visión clara
        de la venta típica, mientras que la media está distorsionada.
    </div>
</div>
```

**Prioridad**: 🟡 Media (puede causar confusión conceptual)

---

### Problema 4: Tolerancia de Respuesta (±0.5) No Explicada
**Ubicación**: Líneas 1719 y 1764 (funciones `checkAnswerMission2A` y `checkAnswerMission2B`)

**Problema**:
```javascript
if (Math.abs(answer - correctAnswer) < 0.5) {
    // Correct!
}
```

La tolerancia de ±0.5 **no se menciona** en ninguna parte del juego.

**Impacto**:
- ⚠️ **Confusión potencial**: Si un jugador calcula 57.3€ y la respuesta correcta es 57€, será aceptada, pero no sabrá por qué
- ⚠️ **Falta de transparencia**: Las reglas del juego deben ser claras

**Sugerencia**:
Añadir una nota en el panel de ayuda o en las instrucciones:

```html
<div class="stats-helper">
    <div class="stats-title">📊 Panel de Ayuda</div>
    <div class="stats-content">
        <p><strong>Cálculo de Mediana:</strong></p>
        <ol>
            <li>Ordena los valores de menor a mayor</li>
            <li>Si hay cantidad impar: toma el valor del centro</li>
            <li>Si hay cantidad par: promedia los dos del centro</li>
        </ol>
        <p style="margin-top: 10px;"><strong>Nota:</strong> Se acepta una tolerancia de ±0.5€
        para compensar redondeos.</p>
    </div>
</div>
```

**Prioridad**: 🟢 Baja (no afecta el aprendizaje, pero mejora la transparencia)

---

### Problema 5: Falta de Explicación sobre Cantidad Par vs Impar
**Ubicación**: Misión 2B (9 valores, cantidad impar)

**Problema**:
Ambas misiones usan **cantidad impar** de valores:
- Misión 2A: 7 valores → Mediana = valor #4
- Misión 2B: 9 valores → Mediana = valor #5

**Impacto**:
- ⚠️ **Falta de práctica**: El jugador nunca calcula mediana con cantidad **par** de valores
- ⚠️ **Concepto incompleto**: La Escena 5 explica el caso par, pero no hay ejercicio práctico

**Sugerencia**:
Considerar añadir una **Misión 2C** (opcional, bonus) con cantidad par de valores:

```javascript
// Misión 2C (Bonus): Cantidad par de valores
const mision2C_ventas = [45, 50, 52, 55, 58, 60, 62, 65];
// Ordenados: [45, 50, 52, 55, 58, 60, 62, 65]
// Mediana = (55 + 58) / 2 = 56.5€
```

O modificar Misión 2B para tener 10 valores en lugar de 9.

**Prioridad**: 🟡 Media (el concepto está explicado, pero falta práctica)

---

## 🎯 Recomendaciones Generales

### 1. Añadir Comentarios Explicativos en el Código
Para que el juego también sea educativo para quien lea el código fuente:

```javascript
// Calcular mediana de un array de números
// La mediana es el valor del medio cuando los datos están ordenados
// Ventaja: NO se ve afectada por outliers (a diferencia de la media)
function calcularMediana(datos) {
    // Crear copia y ordenar de menor a mayor
    const ordenados = [...datos].sort((a, b) => a - b);
    const n = ordenados.length;

    if (n % 2 === 0) {
        // Cantidad PAR: promedio de los dos valores del centro
        // Ejemplo: [1, 2, 3, 4] → Mediana = (2 + 3) / 2 = 2.5
        return (ordenados[n / 2 - 1] + ordenados[n / 2]) / 2;
    } else {
        // Cantidad IMPAR: valor del centro
        // Ejemplo: [1, 2, 3, 4, 5] → Mediana = 3
        return ordenados[Math.floor(n / 2)];
    }
}
```

### 2. Añadir Sección de "Conceptos Aprendidos" al Completar Misión 2B
Al finalizar la Misión 2B, mostrar un resumen:

```html
<div class="tutorial-box" style="background: linear-gradient(135deg, #32cd32 0%, #228b22 100%);">
    <div class="tutorial-title">🎓 Conceptos Dominados</div>
    <div class="tutorial-content">
        ✅ <strong>Mediana:</strong> Valor del medio (robusto a outliers)<br>
        ✅ <strong>Outliers:</strong> Valores atípicos que distorsionan la media<br>
        ✅ <strong>Regla IQR:</strong> Método estadístico para detectar outliers<br>
        ✅ <strong>Media vs Mediana:</strong> Cuándo usar cada una<br>
        ✅ <strong>Decisiones de negocio:</strong> Investigar outliers antes de actuar<br>
        <br>
        <em>¡Estás listo para análisis estadísticos más avanzados!</em>
    </div>
</div>
```

### 3. Añadir Enlace a Documentación Teórica
En el panel de ayuda, añadir un enlace a la teoría:

```html
<p style="margin-top: 15px;">
    📚 <strong>¿Quieres profundizar?</strong><br>
    Lee la teoría completa en:
    <a href="../modulo-01-fundamentos/tema-1-python-estadistica/01-TEORIA.md"
       target="_blank" style="color: #ffd700;">
        01-TEORIA.md
    </a>
</p>
```

### 4. Considerar Añadir Modo "Explicación Paso a Paso"
Un botón que muestre cómo se calcula la mediana paso a paso:

```javascript
function mostrarPasoAPaso() {
    const datos = gameState.currentMissionData;
    const ordenados = [...datos].sort((a, b) => a - b);
    const n = ordenados.length;
    const mediana = calcularMediana(datos);

    alert(`
📊 CÁLCULO PASO A PASO DE LA MEDIANA

1️⃣ Datos originales:
   ${datos.join(', ')}

2️⃣ Ordenar de menor a mayor:
   ${ordenados.join(', ')}

3️⃣ Cantidad de valores: ${n} (impar/par)

4️⃣ Valor del centro:
   Posición ${Math.floor(n/2) + 1} → ${mediana}€

✅ Mediana = ${mediana}€
    `);
}
```

---

## 📊 Checklist de Validación Pedagógica

### ✅ Progresión Pedagógica
- [x] ¿El contenido asume conocimientos que el estudiante aún no tiene? **NO** (asume solo Misión 1)
- [x] ¿Hay un "salto" conceptual brusco? **NO** (progresión suave: tutorial → básico → complejo)
- [x] ¿Los ejemplos van de simple a complejo? **SÍ** (2A evidente → 2B sutil)
- [x] ¿Se explican los prerrequisitos necesarios? **SÍ** (Escenas 5, 6, 7)

### ✅ Claridad y Comprensión
- [x] ¿Un estudiante sin experiencia puede entender esto? **SÍ** (explicaciones simples, analogías)
- [x] ¿Las analogías son efectivas? **SÍ** ("valor del medio", "error en el sistema")
- [x] ¿La jerga técnica está explicada? **SÍ** (outliers, IQR, percentiles)
- [x] ¿Los ejemplos son relevantes y realistas? **SÍ** (ventas de restaurantes)

### ✅ Motivación
- [x] ¿El contenido explica POR QUÉ es importante aprender esto? **SÍ** (outliers distorsionan la media)
- [x] ¿Hay ejemplos del mundo real que generen interés? **SÍ** (errores en sistemas de ventas)
- [x] ¿Se celebran los logros del estudiante? **SÍ** (feedback positivo, XP)
- [x] ¿Los errores se tratan como oportunidades de aprendizaje? **SÍ** (hints constructivos)

### ✅ Carga Cognitiva
- [x] ¿Se presenta demasiada información a la vez? **NO** (progresión gradual)
- [x] ¿Los párrafos son demasiado largos? **NO** (texto conciso, bien estructurado)
- [x] ¿Hay suficientes ejemplos visuales o mentales? **SÍ** (gráficos, outliers en rojo)
- [x] ¿El estudiante tiene oportunidades de practicar antes de seguir? **SÍ** (2A antes de 2B)

### ✅ Gamificación
- [x] ¿Las mecánicas de XP son justas y motivadoras? **SÍ** (75 XP básica, 125 XP compleja)
- [x] ¿El juego enseña o solo entretiene? **ENSEÑA** (conceptos estadísticos correctos)
- [x] ¿Hay riesgo de adicción o comportamiento compulsivo? **NO** (progresión lineal, sin presión)
- [x] ¿El feedback es inmediato y constructivo? **SÍ** (respuesta instantánea con explicación)
- [x] ¿Las misiones tienen contexto narrativo significativo? **SÍ** (RestaurantData Co., María)

---

## 🎯 Veredicto Final

### ✅ APROBADO CON RECOMENDACIONES

La **Misión 2** del juego web enseña correctamente los conceptos de **mediana** y **outliers** con una calidad pedagógica **excelente**.

**Puntos fuertes**:
- Progresión lógica y natural
- Explicaciones claras y accesibles
- Implementación técnica correcta
- Datasets pedagógicamente diseñados
- Feedback constructivo y motivador
- Visualización efectiva (outliers en rojo)
- Gamificación saludable

**Áreas de mejora identificadas** (opcionales, no bloquean la aprobación):
1. 🟡 Añadir comentarios sobre el método de cálculo de percentiles
2. 🟢 Explicar la inconsistencia de métodos de detección (2A vs 2B)
3. 🟡 Aclarar que la mediana incluye outliers (no los excluye)
4. 🟢 Mencionar la tolerancia de ±0.5 en las instrucciones
5. 🟡 Considerar añadir práctica con cantidad par de valores

**Recomendación**: ✅ **Implementar en producción**. Las mejoras sugeridas pueden aplicarse en futuras iteraciones sin afectar la calidad educativa actual.

---

## 📝 Próximos Pasos Sugeridos

1. **Corto plazo** (opcional):
   - Añadir comentarios explicativos en el código JavaScript
   - Aclarar en Escena 7 que la mediana incluye outliers
   - Mencionar tolerancia de ±0.5 en panel de ayuda

2. **Mediano plazo** (futuras misiones):
   - Misión 2C (bonus) con cantidad par de valores
   - Modo "Explicación paso a paso" para cálculos
   - Sección "Conceptos Dominados" al finalizar

3. **Largo plazo** (mejora continua):
   - Enlace a documentación teórica desde el juego
   - Tests A/B para medir efectividad pedagógica
   - Feedback de estudiantes reales

---

**Firma**: Psicólogo Educativo - Equipo Teaching
**Fecha**: 2025-10-19
**Estado**: ✅ Aprobado para producción
