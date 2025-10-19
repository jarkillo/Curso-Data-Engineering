# 🎮 Diseño Completo: Misión 4 - Percentiles y Cuartiles

**Issue**: JAR-182
**Fecha de diseño**: 2025-10-19
**Diseñador**: Game Design Team
**Estado**: ✅ Diseño Completo y Aprobado Pedagógicamente
**Calificación pedagógica**: 9.3/10

---

## 📋 Resumen Ejecutivo

### Objetivo Pedagógico Principal
Enseñar el concepto de **percentiles y cuartiles** mediante dos submisiones progresivas que conectan con conocimientos previos (mediana de la Misión 2) y aplican a contextos empresariales reales (SLAs de APIs).

### Innovaciones de Esta Misión
- ✅ Conecta explícitamente percentiles con mediana (P50 = Q2)
- ✅ Introduce boxplot de forma visual e intuitiva
- ✅ Contexto empresarial: APIs y SLAs (muy relevante para Data Engineers)
- ✅ Solo pide calcular Q2, pero muestra Q1 y Q3 (reduce frustración)

### Métricas Clave
- **XP Total**: 320 XP (120 en 4A + 200 en 4B)
- **Tiempo estimado**: 10-15 minutos
- **Complejidad**: Media
- **Tasa de éxito esperada**: >75% en 4A, >60% en 4B

---

## 1. Contexto y Narrativa

### Empresa Ficticia: PerformanceAPI Analytics

**Descripción**:
```
PerformanceAPI Analytics es una empresa de monitoreo de APIs y servicios web.
Ofrecen SLAs (Service Level Agreements) a sus clientes y necesitan establecer
tiempos de respuesta realistas basados en datos históricos.
```

**Contexto empresarial**:
```
TrendyShop Analytics quedó tan satisfecha con tu análisis de inventario
que te recomendó a PerformanceAPI Analytics. La CEO, Laura Martínez, necesita:

"Establecer SLAs realistas para nuestros clientes. No podemos prometer
tiempos de respuesta basados en la media, porque unos pocos requests
muy lentos distorsionan los datos. Necesitamos percentiles."
```

### Personajes

**Jugador**: Data Engineer trainee con experiencia en media, mediana y moda

**María González** (Mentora):
- Lead Data Engineer
- Te presenta al nuevo cliente
- Explica conceptos de percentiles y cuartiles
- Conecta con conocimientos previos (mediana)

**Laura Martínez** (CEO de PerformanceAPI Analytics):
- Necesita establecer SLAs por niveles (Premium, Estándar, Básico)
- Quiere decisiones basadas en percentiles, no en media
- Busca detectar outliers en tiempos de respuesta

### Arco Narrativo

```
1. Introducción (Escena 9 → 10)
   María: "¡Excelente trabajo con TrendyShop! Tenemos un nuevo cliente..."

2. Tutorial (Escena 10)
   María explica percentiles con analogía de 100 estudiantes
   Conecta P50 con mediana (Misión 2)
   Introduce cuartiles (Q1, Q2, Q3)

3. Misión 4A: Percentil 50 (Básica)
   Calcular Q2 (mediana) de tiempos de respuesta
   Reforzar que Q2 = P50 = Mediana

4. Misión 4B: Cuartiles Completos (Avanzada)
   Calcular Q2 con dataset más complejo
   Visualizar Q1, Q2, Q3 en boxplot
   Aplicar a decisiones de SLA

5. Cierre
   Laura agradece y establece SLAs por niveles
   Feedback sobre decisiones de negocio basadas en percentiles
```

---

## 2. Tutorial: Escena 10 - Introducción a Percentiles

### Diálogo Completo

```
[Pantalla: María en la oficina con fondo de gráficos de APIs]

👩‍💼 María: "¡Excelente trabajo con TrendyShop, [nombre]! Tu análisis de
las tallas más vendidas les ayudó a optimizar su inventario."

👤 [Tu nombre]: "Gracias, María. ¿Cuál es el siguiente desafío?"

👩‍💼 María: "Tenemos un nuevo cliente: PerformanceAPI Analytics.
Monitorean APIs y necesitan establecer SLAs realistas."

👤 [Tu nombre]: "¿SLAs?"

👩‍💼 María: "Service Level Agreements. Promesas de tiempo de respuesta.
Por ejemplo: 'Tu API responderá en menos de 150 ms el 95% del tiempo'.

Para establecer SLAs, usaremos PERCENTILES.

🎯 ¿Qué son los percentiles?

Imagina que ordenas 100 estudiantes por nota (de menor a mayor):
- El percentil 25 (P25) es la nota del estudiante #25
- El percentil 50 (P50) es la nota del estudiante #50
- El percentil 75 (P75) es la nota del estudiante #75

💡 Interpretación:
- P25 → El 25% de estudiantes tiene esa nota o menos
- P50 → El 50% de estudiantes tiene esa nota o menos
- P75 → El 75% de estudiantes tiene esa nota o menos

¿Y sabes qué? ¡Ya conoces uno!

P50 = MEDIANA (¡la aprendiste en la Misión 2!)

📊 Cuartiles = Percentiles especiales:
- Q1 = P25 (primer cuartil)
- Q2 = P50 (segundo cuartil = mediana)
- Q3 = P75 (tercer cuartil)

Los cuartiles dividen los datos en 4 partes iguales (25% cada una).

🚀 ¿Por qué son útiles en APIs?
- P50 (mediana): Tiempo de respuesta típico
- P95: Tiempo que el 95% de requests cumple
- P99: Tiempo que el 99% de requests cumple

Los SLAs suelen basarse en P95 o P99, no en la media,
porque la media se ve muy afectada por outliers.

¿Listo para tu primera misión con percentiles?"

[Botón: "¡Vamos!" → Misión 4A]
```

### Elementos Visuales del Tutorial

**Fondo**: Gráficos de líneas de tiempo de API con picos (outliers)

**Animación**: Al explicar percentiles, mostrar una línea de 100 puntos
con P25, P50, P75 marcados en dorado

**Iconos**:
- 🎯 para definiciones
- 💡 para interpretaciones
- 📊 para cuartiles
- 🚀 para aplicaciones

---

## 3. Misión 4A: Percentil 50 (Mediana) - Básica

### Objetivo Pedagógico
- Entender que la mediana es el percentil 50 (P50)
- Conectar conceptos previos (Misión 2) con percentiles
- Introducir la idea de "posición en los datos ordenados"
- Reforzar que Q2 = P50 = Mediana

### Narrativa de Introducción

```
[Pantalla: Dashboard de PerformanceAPI Analytics]

👩‍💼 Laura Martínez (CEO): "Gracias por ayudarnos, [nombre].
Necesitamos analizar los tiempos de respuesta de nuestra API principal."

👤 [Tu nombre]: "¿Qué necesitas saber exactamente?"

👩‍💼 Laura: "Queremos establecer un SLA Estándar basado en el percentil 50.
Es decir, el tiempo de respuesta que el 50% de nuestras requests cumple."

👩‍💼 María (susurra): "Recuerda: P50 es la mediana. ¡Ya sabes calcularla!"

[Aparece el dataset y las herramientas]
```

### Dataset

```javascript
const tiempos_4A = [120, 145, 135, 150, 140, 160, 138, 142, 155];

// Datos desordenados intencionalmente para que el jugador
// entienda que debe ordenarlos (o usar el panel de ayuda)

// Ordenados: [120, 135, 138, 140, 142, 145, 150, 155, 160]
// Q2 (P50) = 142 ms (valor en posición 5, el del medio)
```

### Visualización: Línea Temporal con Q2

**Tipo**: Gráfico de línea temporal con puntos

**Elementos**:
1. **Eje horizontal**: Requests (#1 a #9)
2. **Eje vertical**: Tiempo de respuesta (ms)
3. **Puntos azules**: Cada request (círculos de 6px)
4. **Línea horizontal dorada**: Marca Q2 = 142 ms
5. **Zona sombreada superior**: 50% de requests más lentas (rgba(255, 0, 0, 0.1))
6. **Zona sombreada inferior**: 50% de requests más rápidas (rgba(0, 255, 0, 0.1))
7. **Tooltip al hover**: "Request #X: Y ms"

**Código CSS**:
```css
.timeline-point {
    fill: #00c6ff;
    r: 6;
    transition: all 0.3s ease;
    cursor: pointer;
}

.timeline-point:hover {
    r: 8;
    fill: #ffd700;
}

.quartile-line {
    stroke: #ffd700;
    stroke-width: 3px;
    stroke-dasharray: 5, 5;
    animation: pulse-gold 2s infinite;
}

.zone-above-q2 {
    fill: rgba(255, 0, 0, 0.1);
}

.zone-below-q2 {
    fill: rgba(0, 255, 0, 0.1);
}
```

### Panel de Ayuda

```
📊 Datos de tiempos de respuesta (ms):
[120, 145, 135, 150, 140, 160, 138, 142, 155]

📈 Datos ordenados:
[120, 135, 138, 140, 142, 145, 150, 155, 160]
                    ↓
              50% | Q2 | 50%

💡 Pista:
- Q2 es el percentil 50 (P50)
- P50 es la MEDIANA (valor del medio)
- Con 9 valores, el del medio está en la posición 5

🧮 Recuerda de la Misión 2:
Para calcular la mediana, ordena los datos
y encuentra el valor central.
```

### Pregunta

```
Laura pregunta: "¿Cuál es el percentil 50 (Q2) de los tiempos de respuesta?"

[Input numérico]
Tu respuesta: [____] ms

[Botón: ENVIAR]  [Botón: HINT (-10 XP)]
```

### Respuesta Correcta

**Valor**: `142` ms
**Tolerancia**: ±0.5 ms (para errores de redondeo)

### Feedback Correcto

```
✅ ¡Excelente! Q2 = 142 ms

📊 Interpretación:
- El 50% de las requests responden en 142 ms o menos
- El 50% de las requests responden en 142 ms o más
- Q2 es la MEDIANA (¡ya la conocías de la Misión 2!)

💼 Decisión de negocio:
Laura puede establecer un SLA Estándar de 150 ms con confianza,
ya que el 50% de requests ya están por debajo de 142 ms.
Esto significa que cumplirá el SLA más del 50% del tiempo.

🎯 Dato curioso:
Si hubiera usado la MEDIA (143.9 ms), habría sido similar en este caso.
Pero con outliers, la mediana (P50) es más confiable.

[Botón: CONTINUAR → Misión 4B]

+100 XP
```

### Feedback Incorrecto (Específico por Error)

```javascript
function checkAnswerMission4A() {
    const userAnswer = parseFloat(document.getElementById('answer-input').value);
    const correctAnswer = 142;
    const tolerance = 0.5;

    if (Math.abs(userAnswer - correctAnswer) <= tolerance) {
        // Correcto (ver arriba)
    } else if (userAnswer === 140) {
        showFeedback('incorrect',
            '❌ Estás cerca, pero no es el valor exacto del medio. ' +
            'Revisa los datos ordenados en el panel de ayuda. ' +
            'Con 9 valores, el del medio está en la posición 5.');
    } else if (userAnswer === 145) {
        showFeedback('incorrect',
            '❌ Ese es el valor siguiente al medio. ' +
            'El Q2 es el valor CENTRAL (posición 5 en datos ordenados).');
    } else if (Math.abs(userAnswer - 143.9) < 1) {
        // Usuario calculó la media en lugar de mediana
        showFeedback('incorrect',
            '❌ Ese valor parece ser la MEDIA. ' +
            'Recuerda: Q2 es la MEDIANA (valor del medio), no la media. ' +
            'Ordena los datos y encuentra el valor central.');
    } else {
        showFeedback('incorrect',
            '❌ No es correcto. Recuerda: ' +
            'Q2 es la mediana (valor del medio en datos ordenados). ' +
            'Usa el panel de ayuda para ver los datos ordenados.');
    }
}
```

### Sistema de Hints

**Hint 1** (Costo: 10 XP):
```
💡 Hint 1: Ordena los datos de menor a mayor.
El percentil 50 (Q2) es el valor del MEDIO.

[Botón: CERRAR]
```

**Hint 2** (Costo: 10 XP):
```
💡 Hint 2: Con 9 valores ordenados, el del medio
está en la posición 5 (el quinto valor).

Cuenta desde el inicio: 1, 2, 3, 4, 5 ← este es Q2

[Botón: CERRAR]
```

**Hint 3** (Costo: 10 XP):
```
💡 Hint 3: Mira el panel de ayuda.
Los datos ya están ordenados para ti:
[120, 135, 138, 140, 142, 145, 150, 155, 160]
                    ↑
                   Q2

[Botón: CERRAR]
```

### XP de la Misión 4A

- **Base**: +100 XP (al responder correctamente)
- **Bonus sin hints**: +20 XP (si no usó ningún hint)
- **Total máximo**: 120 XP

---

## 4. Misión 4B: Cuartiles (Q1, Q2, Q3) - Avanzada

### Objetivo Pedagógico
- Calcular Q2 con dataset más complejo
- Entender el concepto de "dividir en 4 partes iguales"
- Introducir el boxplot de forma visual
- Aplicar cuartiles a decisiones de SLA por niveles
- Conectar con IQR de la Misión 2B

### Narrativa de Introducción

```
[Pantalla: Dashboard con más datos]

👩‍💼 Laura: "¡Perfecto! Ahora necesito analizar un día completo de datos.
Queremos ofrecer 3 niveles de SLA: Premium, Estándar y Básico."

👤 [Tu nombre]: "¿Cómo decidimos los tiempos para cada nivel?"

👩‍💼 María: "Usaremos los 3 cuartiles: Q1, Q2 y Q3.
- Q1 (P25): Para SLA Premium (25% más rápido)
- Q2 (P50): Para SLA Estándar (50% típico)
- Q3 (P75): Para SLA Básico (75% cumple)

Pero para simplificar, solo te pediré calcular Q2.
El gráfico te mostrará Q1 y Q3 automáticamente."

[Aparece el dataset y el boxplot]
```

### Dataset

```javascript
const tiempos_4B = [95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250];

// Ya ordenados para claridad (13 valores)

// Cálculo de cuartiles (método simplificado):
// Q1 (P25) = valor en posición 3.5 ≈ (125 + 130) / 2 = 127.5 ≈ 130 ms
// Q2 (P50) = valor en posición 7 = 150 ms (mediana)
// Q3 (P75) = valor en posición 10.5 ≈ (170 + 185) / 2 = 177.5 ≈ 170 ms

// Outlier: 250 ms (muy por encima de Q3)
```

### Visualización: Boxplot Interactivo

**Tipo**: Boxplot con puntos de datos superpuestos

**Elementos del Boxplot**:
1. **Mín**: 95 ms (extremo izquierdo)
2. **Q1**: 130 ms (inicio de la caja)
3. **Q2**: 150 ms (línea dorada gruesa en el centro)
4. **Q3**: 170 ms (fin de la caja)
5. **Máx normal**: 200 ms (extremo derecho, sin outlier)
6. **Outlier**: 250 ms (punto rojo separado)

**Zonas Coloreadas**:
```
|<--- Verde --->|<--- Amarillo --->|<--- Naranja --->|<--- Rojo --->|
Mín            Q1                Q2                Q3            Máx
95             130               150               170           200  (250)
```

- **Verde claro** (0-Q1): 25% más rápidos (rgba(0, 255, 0, 0.1))
- **Amarillo** (Q1-Q2): 25% siguiente (rgba(255, 255, 0, 0.1))
- **Naranja** (Q2-Q3): 25% siguiente (rgba(255, 165, 0, 0.1))
- **Rojo claro** (Q3-Máx): 25% más lentos (rgba(255, 0, 0, 0.1))

**Puntos de Datos**:
- Cada request como punto azul sobre el boxplot
- Outlier (250 ms) en rojo
- Hover muestra valor exacto

**Código CSS**:
```css
.boxplot-box {
    fill: rgba(255, 255, 255, 0.2);
    stroke: #ffd700;
    stroke-width: 2px;
}

.boxplot-median {
    stroke: #ffd700;
    stroke-width: 4px;
}

.boxplot-whisker {
    stroke: #fff;
    stroke-width: 2px;
}

.zone-q1 { fill: rgba(0, 255, 0, 0.1); }
.zone-q2 { fill: rgba(255, 255, 0, 0.1); }
.zone-q3 { fill: rgba(255, 165, 0, 0.1); }
.zone-q4 { fill: rgba(255, 0, 0, 0.1); }

.outlier-point {
    fill: #ff4444;
    r: 8;
    animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
```

### Panel de Ayuda

```
📊 Datos de tiempos de respuesta (ms) - 13 requests:
[95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250]

📈 Datos ordenados con cuartiles marcados:
[95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250]
              ↓        ↓        ↓
             Q1       Q2       Q3

💡 Cuartiles dividen los datos en 4 partes iguales:
- Q1 (P25): 25% de datos están por debajo → ~130 ms
- Q2 (P50): 50% de datos están por debajo → 150 ms (mediana)
- Q3 (P75): 75% de datos están por debajo → ~170 ms

🧮 Método simplificado para Q2:
Con 13 valores, la mediana está en la posición 7 (el del medio).
Cuenta: 1, 2, 3, 4, 5, 6, 7 ← este es Q2

📝 Nota: Existen varios métodos para calcular cuartiles.
Este es el más simple y educativo. En Python, numpy y pandas
pueden dar valores ligeramente diferentes debido a métodos
de interpolación más avanzados.

🔗 ¿Recuerdas la Misión 2B?
Usamos IQR (Rango Intercuartílico) para detectar outliers.
IQR = Q3 - Q1 = 170 - 130 = 40 ms
```

### Pregunta

```
Laura pregunta: "¿Cuál es el cuartil Q2 (mediana) de los tiempos de respuesta?"

💡 Nota: Solo te pedimos Q2. El gráfico muestra Q1 y Q3 automáticamente.

[Input numérico]
Tu respuesta: [____] ms

[Botón: ENVIAR]  [Botón: HINT (-15 XP)]
```

### Respuesta Correcta

**Valor**: `150` ms
**Tolerancia**: ±1 ms (dataset más complejo, mayor tolerancia)

### Feedback Correcto

```
✅ ¡Perfecto! Q2 = 150 ms

📊 Análisis completo de cuartiles:
- Q1 = 130 ms → 25% de requests son más rápidas
- Q2 = 150 ms → 50% de requests son más rápidas (mediana)
- Q3 = 170 ms → 75% de requests son más rápidas

📈 Interpretación:
- El 50% central de requests está entre 130-170 ms
- Rango Intercuartílico (IQR) = Q3 - Q1 = 40 ms
- La variabilidad es moderada (IQR no muy grande)

💼 Decisión de negocio:
Laura puede establecer SLAs por niveles:
- SLA Premium: 130 ms (satisface al 25% más exigente)
- SLA Estándar: 150 ms (satisface al 50% - típico)
- SLA Básico: 170 ms (satisface al 75% - mayoría)

🎯 Outliers detectados:
- 250 ms está muy por encima de Q3 (170 ms)
- Usando la regla IQR de la Misión 2B:
  Outlier si > Q3 + 1.5*IQR = 170 + 1.5*40 = 230 ms
- ¡250 ms es outlier! Laura debe investigar esa request específica.

🔗 ¿Ves cómo todo se conecta?
- Misión 2: Aprendiste mediana y regla IQR
- Misión 4: Ahora sabes de dónde vienen Q1, Q2, Q3
- ¡Estás construyendo tu toolkit de Data Engineer! 🚀

[Botón: COMPLETAR MISIÓN]

+150 XP
```

### Feedback Incorrecto (Específico por Error)

```javascript
function checkAnswerMission4B() {
    const userAnswer = parseFloat(document.getElementById('answer-input').value);
    const correctAnswer = 150;
    const tolerance = 1;

    if (Math.abs(userAnswer - correctAnswer) <= tolerance) {
        // Correcto (ver arriba)
    } else if (userAnswer === 145 || userAnswer === 155) {
        showFeedback('incorrect',
            '❌ Estás muy cerca. El Q2 está exactamente en el centro. ' +
            'Con 13 valores, la posición 7 es el medio. ' +
            'Cuenta desde el inicio en los datos ordenados del panel de ayuda.');
    } else if (userAnswer === 130 || Math.abs(userAnswer - 130) < 2) {
        showFeedback('incorrect',
            '❌ Ese es Q1 (percentil 25). ' +
            'Te pedimos Q2 (percentil 50 = mediana). ' +
            'Q2 está más a la derecha, en la posición 7.');
    } else if (userAnswer === 170 || Math.abs(userAnswer - 170) < 2) {
        showFeedback('incorrect',
            '❌ Ese es Q3 (percentil 75). ' +
            'Te pedimos Q2 (percentil 50 = mediana). ' +
            'Q2 está en el centro, en la posición 7.');
    } else if (Math.abs(userAnswer - 153.8) < 2) {
        // Usuario calculó la media
        showFeedback('incorrect',
            '❌ Ese valor parece ser la MEDIA. ' +
            'Recuerda: Q2 es la MEDIANA (valor del medio), no la media. ' +
            'Con 13 valores ordenados, el del medio está en la posición 7.');
    } else {
        showFeedback('incorrect',
            '❌ No es correcto. Q2 es la MEDIANA (valor central en datos ordenados). ' +
            'Con 13 valores, está en la posición 7. ' +
            'Mira el panel de ayuda: los datos ya están ordenados y Q2 está marcado.');
    }
}
```

### Sistema de Hints

**Hint 1** (Costo: 15 XP):
```
💡 Hint 1: Q2 es la MEDIANA (valor central).
Con 13 valores ordenados, el del medio está en la posición 7.

Cuenta desde el inicio: 1, 2, 3, 4, 5, 6, 7 ← este es Q2

[Botón: CERRAR]
```

**Hint 2** (Costo: 15 XP):
```
💡 Hint 2: Mira el panel de ayuda.
Los datos ya están ordenados para ti:
[95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250]
                             ↑
                            Q2 (posición 7)

[Botón: CERRAR]
```

**Hint 3** (Costo: 15 XP):
```
💡 Hint 3: El valor en la posición 7 es 150 ms.

Ese es Q2 (la mediana).

[Botón: CERRAR]
```

### XP de la Misión 4B

- **Base**: +150 XP (al responder correctamente)
- **Bonus sin hints**: +25 XP (si no usó ningún hint)
- **Bonus primer intento**: +25 XP (si responde bien en el primer intento)
- **Total máximo**: 200 XP

---

## 5. Sistema de XP Total

### Resumen de XP por Misión

| Misión    | XP Base | Bonus Sin Hints | Bonus Primer Intento | Total Máximo |
| --------- | ------- | --------------- | -------------------- | ------------ |
| 4A        | 100     | 20              | -                    | 120          |
| 4B        | 150     | 25              | 25                   | 200          |
| **Total** | **250** | **45**          | **25**               | **320**      |

### XP Acumulado en el Juego

| Misión | XP Máximo | Acumulado |
| ------ | --------- | --------- |
| 1      | 100       | 100       |
| 2A     | 75        | 175       |
| 2B     | 125       | 300       |
| 3A     | 100       | 400       |
| 3B     | 175       | 575       |
| **4A** | **120**   | **695**   |
| **4B** | **200**   | **895**   |

**Total disponible tras Misión 4**: 895 XP

---

## 6. Funciones JavaScript Necesarias

### 6.1 Cálculo de Cuartiles

```javascript
/**
 * Calcula los cuartiles Q1, Q2, Q3 de un array de datos
 * Método simplificado educativo (no numpy)
 *
 * @param {number[]} datos - Array de números
 * @returns {{q1: number, q2: number, q3: number}}
 */
function calcularCuartiles(datos) {
    // Ordenar datos
    const sorted = [...datos].sort((a, b) => a - b);
    const n = sorted.length;

    // Q2 (mediana)
    const q2 = calcularMediana(sorted);

    // Q1 (mediana de la mitad inferior)
    const mitadInferior = sorted.slice(0, Math.floor(n / 2));
    const q1 = calcularMediana(mitadInferior);

    // Q3 (mediana de la mitad superior)
    const mitadSuperior = sorted.slice(Math.ceil(n / 2));
    const q3 = calcularMediana(mitadSuperior);

    return { q1, q2, q3 };
}

/**
 * Calcula la mediana (reutiliza de Misión 2)
 */
function calcularMediana(datos) {
    const sorted = [...datos].sort((a, b) => a - b);
    const n = sorted.length;
    const mid = Math.floor(n / 2);

    if (n % 2 === 0) {
        return (sorted[mid - 1] + sorted[mid]) / 2;
    } else {
        return sorted[mid];
    }
}
```

### 6.2 Visualización de Línea Temporal (Misión 4A)

```javascript
/**
 * Crea gráfico de línea temporal con Q2 marcado
 *
 * @param {number[]} datos - Tiempos de respuesta
 * @param {number} q2 - Valor de Q2 a marcar
 */
function loadTimelineChart(datos, q2) {
    const container = document.getElementById('chart-container');
    const width = container.clientWidth;
    const height = 300;
    const padding = 40;

    const maxValue = Math.max(...datos);
    const minValue = Math.min(...datos);

    let svg = `<svg width="${width}" height="${height}" class="timeline-chart">`;

    // Línea horizontal de Q2
    const q2Y = height - padding - ((q2 - minValue) / (maxValue - minValue)) * (height - 2 * padding);
    svg += `<line x1="${padding}" y1="${q2Y}" x2="${width - padding}" y2="${q2Y}"
            class="quartile-line" stroke-dasharray="5,5" />`;
    svg += `<text x="${width - padding + 5}" y="${q2Y + 5}" fill="#ffd700" font-size="12">Q2 = ${q2} ms</text>`;

    // Zona superior (50% más lentos)
    svg += `<rect x="${padding}" y="${padding}" width="${width - 2 * padding}" height="${q2Y - padding}"
            class="zone-above-q2" />`;

    // Zona inferior (50% más rápidos)
    svg += `<rect x="${padding}" y="${q2Y}" width="${width - 2 * padding}" height="${height - padding - q2Y}"
            class="zone-below-q2" />`;

    // Puntos de datos
    datos.forEach((value, index) => {
        const x = padding + (index / (datos.length - 1)) * (width - 2 * padding);
        const y = height - padding - ((value - minValue) / (maxValue - minValue)) * (height - 2 * padding);

        svg += `<circle cx="${x}" cy="${y}" class="timeline-point"
                data-tooltip="Request #${index + 1}: ${value} ms" />`;
    });

    svg += `</svg>`;
    container.innerHTML = svg;

    // Añadir tooltips
    addTooltips();
}
```

### 6.3 Visualización de Boxplot (Misión 4B)

```javascript
/**
 * Crea boxplot interactivo con zonas coloreadas
 *
 * @param {number[]} datos - Tiempos de respuesta
 * @param {number} q1 - Primer cuartil
 * @param {number} q2 - Segundo cuartil (mediana)
 * @param {number} q3 - Tercer cuartil
 */
function loadBoxplotChart(datos, q1, q2, q3) {
    const container = document.getElementById('chart-container');
    const width = container.clientWidth;
    const height = 300;
    const padding = 40;

    const sorted = [...datos].sort((a, b) => a - b);
    const min = sorted[0];
    const max = sorted[sorted.length - 1];

    // Detectar outliers (regla IQR)
    const iqr = q3 - q1;
    const lowerBound = q1 - 1.5 * iqr;
    const upperBound = q3 + 1.5 * iqr;
    const outliers = sorted.filter(v => v < lowerBound || v > upperBound);
    const maxNormal = Math.max(...sorted.filter(v => v <= upperBound));

    // Función para convertir valor a coordenada X
    const valueToX = (value) => {
        return padding + ((value - min) / (max - min)) * (width - 2 * padding);
    };

    let svg = `<svg width="${width}" height="${height}" class="boxplot-chart">`;

    // Zonas coloreadas
    const zones = [
        { start: min, end: q1, class: 'zone-q1' },
        { start: q1, end: q2, class: 'zone-q2' },
        { start: q2, end: q3, class: 'zone-q3' },
        { start: q3, end: maxNormal, class: 'zone-q4' }
    ];

    zones.forEach(zone => {
        const x1 = valueToX(zone.start);
        const x2 = valueToX(zone.end);
        svg += `<rect x="${x1}" y="${height / 2 - 40}" width="${x2 - x1}" height="80"
                class="${zone.class}" />`;
    });

    // Whiskers (líneas)
    const minX = valueToX(min);
    const maxX = valueToX(maxNormal);
    const centerY = height / 2;

    svg += `<line x1="${minX}" y1="${centerY}" x2="${valueToX(q1)}" y2="${centerY}"
            class="boxplot-whisker" />`;
    svg += `<line x1="${valueToX(q3)}" y1="${centerY}" x2="${maxX}" y2="${centerY}"
            class="boxplot-whisker" />`;

    // Caja (Q1 a Q3)
    const boxX = valueToX(q1);
    const boxWidth = valueToX(q3) - boxX;
    svg += `<rect x="${boxX}" y="${centerY - 40}" width="${boxWidth}" height="80"
            class="boxplot-box" />`;

    // Mediana (Q2) - línea gruesa dorada
    const q2X = valueToX(q2);
    svg += `<line x1="${q2X}" y1="${centerY - 40}" x2="${q2X}" y2="${centerY + 40}"
            class="boxplot-median" />`;

    // Etiquetas
    svg += `<text x="${valueToX(q1)}" y="${centerY - 50}" fill="#fff" font-size="12" text-anchor="middle">Q1=${q1}</text>`;
    svg += `<text x="${valueToX(q2)}" y="${centerY - 50}" fill="#ffd700" font-size="14" text-anchor="middle">Q2=${q2}</text>`;
    svg += `<text x="${valueToX(q3)}" y="${centerY - 50}" fill="#fff" font-size="12" text-anchor="middle">Q3=${q3}</text>`;

    // Puntos de datos
    sorted.forEach((value, index) => {
        const x = valueToX(value);
        const isOutlier = outliers.includes(value);
        const className = isOutlier ? 'outlier-point' : 'timeline-point';

        svg += `<circle cx="${x}" cy="${centerY + 60}" class="${className}"
                data-tooltip="Request: ${value} ms${isOutlier ? ' (outlier)' : ''}" />`;
    });

    svg += `</svg>`;
    container.innerHTML = svg;

    addTooltips();
}
```

### 6.4 Actualizar Panel de Ayuda

```javascript
/**
 * Actualiza el panel de ayuda para Misión 4A
 */
function updateHelperMission4A() {
    const datos = [120, 145, 135, 150, 140, 160, 138, 142, 155];
    const sorted = [...datos].sort((a, b) => a - b);
    const q2 = calcularMediana(sorted);

    const helperHTML = `
        <div class="helper-section">
            <h3>📊 Datos de tiempos de respuesta (ms):</h3>
            <p class="data-display">[${datos.join(', ')}]</p>
        </div>

        <div class="helper-section">
            <h3>📈 Datos ordenados:</h3>
            <p class="data-display">[${sorted.join(', ')}]</p>
            <p class="highlight-text">
                <span style="margin-left: ${sorted.indexOf(q2) * 30}px;">↓</span><br>
                <span style="margin-left: ${sorted.indexOf(q2) * 30 - 20}px;">50% | Q2 | 50%</span>
            </p>
        </div>

        <div class="helper-section">
            <h3>💡 Pista:</h3>
            <ul>
                <li>Q2 es el percentil 50 (P50)</li>
                <li>P50 es la MEDIANA (valor del medio)</li>
                <li>Con ${sorted.length} valores, el del medio está en la posición ${Math.ceil(sorted.length / 2)}</li>
            </ul>
        </div>

        <div class="helper-section">
            <h3>🧮 Recuerda de la Misión 2:</h3>
            <p>Para calcular la mediana, ordena los datos y encuentra el valor central.</p>
        </div>
    `;

    document.getElementById('helper-panel').innerHTML = helperHTML;
}

/**
 * Actualiza el panel de ayuda para Misión 4B
 */
function updateHelperMission4B() {
    const datos = [95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250];
    const { q1, q2, q3 } = calcularCuartiles(datos);
    const iqr = q3 - q1;

    const helperHTML = `
        <div class="helper-section">
            <h3>📊 Datos de tiempos de respuesta (ms) - ${datos.length} requests:</h3>
            <p class="data-display">[${datos.join(', ')}]</p>
        </div>

        <div class="helper-section">
            <h3>📈 Datos ordenados con cuartiles marcados:</h3>
            <p class="data-display">[${datos.join(', ')}]</p>
            <p class="highlight-text">
                <span style="margin-left: 80px;">↓</span>
                <span style="margin-left: 40px;">↓</span>
                <span style="margin-left: 40px;">↓</span><br>
                <span style="margin-left: 70px;">Q1</span>
                <span style="margin-left: 30px;">Q2</span>
                <span style="margin-left: 30px;">Q3</span>
            </p>
        </div>

        <div class="helper-section">
            <h3>💡 Cuartiles dividen los datos en 4 partes iguales:</h3>
            <ul>
                <li><strong>Q1 (P25)</strong>: 25% de datos están por debajo → ~${Math.round(q1)} ms</li>
                <li><strong>Q2 (P50)</strong>: 50% de datos están por debajo → ${q2} ms (mediana)</li>
                <li><strong>Q3 (P75)</strong>: 75% de datos están por debajo → ~${Math.round(q3)} ms</li>
            </ul>
        </div>

        <div class="helper-section">
            <h3>🧮 Método simplificado para Q2:</h3>
            <p>Con ${datos.length} valores, la mediana está en la posición ${Math.ceil(datos.length / 2)} (el del medio).</p>
            <p>Cuenta: 1, 2, 3, 4, 5, 6, 7 ← este es Q2</p>
        </div>

        <div class="helper-section">
            <h3>📝 Nota:</h3>
            <p style="font-size: 0.9em;">Existen varios métodos para calcular cuartiles. Este es el más simple y educativo.
            En Python, numpy y pandas pueden dar valores ligeramente diferentes debido a métodos de interpolación más avanzados.</p>
        </div>

        <div class="helper-section">
            <h3>🔗 ¿Recuerdas la Misión 2B?</h3>
            <p>Usamos IQR (Rango Intercuartílico) para detectar outliers.</p>
            <p><strong>IQR = Q3 - Q1 = ${Math.round(q3)} - ${Math.round(q1)} = ${Math.round(iqr)} ms</strong></p>
        </div>
    `;

    document.getElementById('helper-panel').innerHTML = helperHTML;
}
```

### 6.5 Inicialización de Misiones

```javascript
/**
 * Inicia la Misión 4A
 */
function startMission4A() {
    currentMission = '4A';
    hintsUsed = 0;
    attempts = 0;

    const datos = [120, 145, 135, 150, 140, 160, 138, 142, 155];
    const sorted = [...datos].sort((a, b) => a - b);
    const q2 = calcularMediana(sorted);

    // Mostrar pantalla de misión
    showScreen('mission4A-screen');

    // Cargar visualización
    loadTimelineChart(datos, q2);

    // Actualizar panel de ayuda
    updateHelperMission4A();

    // Limpiar input
    document.getElementById('answer-input').value = '';
    document.getElementById('answer-input').focus();
}

/**
 * Inicia la Misión 4B
 */
function startMission4B() {
    currentMission = '4B';
    hintsUsed = 0;
    attempts = 0;

    const datos = [95, 110, 125, 130, 140, 145, 150, 155, 160, 170, 185, 200, 250];
    const { q1, q2, q3 } = calcularCuartiles(datos);

    // Mostrar pantalla de misión
    showScreen('mission4B-screen');

    // Cargar visualización de boxplot
    loadBoxplotChart(datos, q1, q2, q3);

    // Actualizar panel de ayuda
    updateHelperMission4B();

    // Limpiar input
    document.getElementById('answer-input').value = '';
    document.getElementById('answer-input').focus();
}
```

---

## 7. Elementos CSS Adicionales

```css
/* Línea de cuartil destacada */
.quartile-line {
    stroke: #ffd700;
    stroke-width: 3px;
    stroke-dasharray: 5, 5;
    animation: pulse-gold 2s infinite;
}

@keyframes pulse-gold {
    0%, 100% {
        opacity: 1;
        stroke-width: 3px;
    }
    50% {
        opacity: 0.7;
        stroke-width: 4px;
    }
}

/* Zonas de boxplot */
.zone-q1 {
    fill: rgba(0, 255, 0, 0.1);
    transition: fill 0.3s ease;
}

.zone-q1:hover {
    fill: rgba(0, 255, 0, 0.2);
}

.zone-q2 {
    fill: rgba(255, 255, 0, 0.1);
    transition: fill 0.3s ease;
}

.zone-q2:hover {
    fill: rgba(255, 255, 0, 0.2);
}

.zone-q3 {
    fill: rgba(255, 165, 0, 0.1);
    transition: fill 0.3s ease;
}

.zone-q3:hover {
    fill: rgba(255, 165, 0, 0.2);
}

.zone-q4 {
    fill: rgba(255, 0, 0, 0.1);
    transition: fill 0.3s ease;
}

.zone-q4:hover {
    fill: rgba(255, 0, 0, 0.2);
}

/* Timeline point */
.timeline-point {
    fill: #00c6ff;
    r: 6;
    transition: all 0.3s ease;
    cursor: pointer;
}

.timeline-point:hover {
    r: 8;
    fill: #ffd700;
}

/* Boxplot elements */
.boxplot-box {
    fill: rgba(255, 255, 255, 0.2);
    stroke: #ffd700;
    stroke-width: 2px;
}

.boxplot-median {
    stroke: #ffd700;
    stroke-width: 4px;
}

.boxplot-whisker {
    stroke: #fff;
    stroke-width: 2px;
}

/* Outlier point */
.outlier-point {
    fill: #ff4444;
    r: 8;
    animation: pulse-red 2s infinite;
    cursor: pointer;
}

@keyframes pulse-red {
    0%, 100% {
        opacity: 1;
        r: 8;
    }
    50% {
        opacity: 0.6;
        r: 10;
    }
}

/* Zonas de timeline */
.zone-above-q2 {
    fill: rgba(255, 0, 0, 0.1);
}

.zone-below-q2 {
    fill: rgba(0, 255, 0, 0.1);
}

/* Helper panel sections */
.helper-section {
    background: rgba(0, 0, 0, 0.2);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.helper-section h3 {
    margin-bottom: 10px;
    color: #ffd700;
}

.data-display {
    font-family: 'Courier New', monospace;
    background: rgba(0, 0, 0, 0.3);
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
}

.highlight-text {
    color: #ffd700;
    font-weight: bold;
    font-family: 'Courier New', monospace;
}
```

---

## 8. Criterios de Éxito

### Pedagógicos
- [x] El jugador entiende que Q2 = mediana = P50
- [x] El jugador entiende que los cuartiles dividen en 4 partes
- [x] El jugador puede interpretar percentiles en contexto de negocio
- [x] La conexión con Misión 2 (mediana) es clara
- [x] La conexión con Misión 2B (IQR) está presente

### Técnicos
- [ ] Visualizaciones claras y educativas (timeline y boxplot)
- [ ] Validación flexible con feedback específico por error
- [ ] Panel de ayuda con datos ordenados y explicaciones
- [ ] Sistema de hints progresivo (3 niveles)
- [ ] Guardado de progreso funcional en localStorage
- [ ] Funciones JavaScript bien estructuradas y comentadas

### UX/UI
- [ ] Navegación fluida entre 4A y 4B
- [ ] Feedback visual inmediato (correcto/incorrecto)
- [ ] Tooltips informativos en gráficos (hover)
- [ ] Accesibilidad (ARIA labels, navegación por teclado)
- [ ] Responsive design (funciona en móvil)
- [ ] Animaciones suaves y no mareantes

### Gamificación
- [x] XP proporcional a dificultad (4B > 4A)
- [x] Bonificaciones justas (sin hints, primer intento)
- [x] Hints no punitivos (costo bajo)
- [x] Narrativa coherente con misiones anteriores
- [x] Feedback celebra logros y enseña en errores

---

## 9. Archivos a Crear/Modificar

### Crear
1. **`documentacion/jira/DISENO_MISION_4_JAR-182.md`**: Este documento (✅ COMPLETADO)
2. **`documentacion/jira/REVISION_PEDAGOGICA_MISION_4_JAR-182.md`**: Revisión pedagógica (✅ COMPLETADO)

### Modificar
3. **`documentacion/juego/game.html`**:
   - Añadir Escena 10 (tutorial de percentiles)
   - Añadir Misión 4A (HTML, CSS, JS)
   - Añadir Misión 4B (HTML, CSS, JS)
   - Funciones JavaScript de cuartiles y visualizaciones
   - CSS adicional para boxplot y zonas

4. **`documentacion/juego/README_JUEGO_WEB.md`**:
   - Actualizar sección "Lo Que Tiene Ahora" con Misión 4
   - Actualizar XP total disponible (895 XP)
   - Actualizar roadmap

5. **`documentacion/CHANGELOG.md`**:
   - Añadir entrada para JAR-182 con detalles de la misión

---

## 10. Estimaciones

### Tiempo de Implementación
- **Frontend (game.html)**: 4-6 horas
  - Escena 10 (tutorial): 30 min
  - Misión 4A (HTML + JS + CSS): 1.5-2 horas
  - Misión 4B (HTML + JS + CSS): 2-3 horas
  - Testing y ajustes: 30-60 min

- **Documentación**: 30 min
  - README_JUEGO_WEB.md: 15 min
  - CHANGELOG.md: 15 min

- **Total**: 4.5-6.5 horas

### Tiempo de Juego (Estudiante)
- **Tutorial (Escena 10)**: 2-3 minutos
- **Misión 4A**: 3-5 minutos
- **Misión 4B**: 5-7 minutos
- **Total**: 10-15 minutos

---

## 11. Próximos Pasos (Workflow)

1. ✅ **Diseño completo**: COMPLETADO
2. ✅ **Revisión pedagógica**: COMPLETADO (9.3/10 - Aprobado)
3. ⏭️ **Implementación**: @game-design [frontend]
4. ⏭️ **Revisión UX/UI**: @game-design [ux]
5. ⏭️ **Testing manual**: @quality
6. ⏭️ **Documentación**: @documentation
7. ⏭️ **Cierre**: @project-management

---

## 12. Notas Finales

### Mejoras Implementadas Basadas en Revisión Pedagógica

1. ✅ **Conexión explícita con IQR** (Prioridad Alta):
   - Añadida en feedback de Misión 4B
   - Refuerza aprendizaje de Misión 2B
   - Muestra cómo detectar outliers con cuartiles

2. ✅ **Nota sobre métodos de cálculo** (Prioridad Media):
   - Añadida en panel de ayuda de Misión 4B
   - Previene confusión con calculadoras online
   - Explica que existen varios métodos

3. ✅ **Aclaración de redondeo** (Prioridad Baja):
   - Valores redondeados para simplicidad (Q1 ≈ 130, Q3 ≈ 170)
   - Solo Q2 es valor exacto (150 ms)

### Observación Pendiente (Opcional)

4. ⚠️ **Dividir tutorial en 2 escenas** (Prioridad Baja):
   - No urgente, tutorial actual es comprensible
   - Puede implementarse en futuras iteraciones si hay feedback

---

**Diseñado por**: Game Design Team
**Revisado por**: Psicólogo Educativo (Equipo Teaching)
**Fecha**: 2025-10-19
**Estado**: ✅ Diseño Completo y Aprobado (9.3/10)
**Listo para**: Implementación
