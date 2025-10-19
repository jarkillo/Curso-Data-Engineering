# 🎮 Diseño de Misión 3: Moda y Distribuciones Bimodales

**Issue**: JAR-181
**Fecha de diseño**: 2025-10-19
**Diseñador**: Game Design Team
**Estado**: ✅ Diseño Completo - Pendiente Implementación

---

## 📋 Resumen Ejecutivo

### Objetivo Pedagógico
Enseñar el concepto de **moda** (valor más frecuente) y **distribuciones bimodales** (dos modas) en el contexto de análisis de datos categóricos.

### Innovaciones
- ✅ Primera misión con datos **CATEGÓRICOS** (tallas, no números)
- ✅ Introduce concepto de **distribución bimodal**
- ✅ Validación flexible de respuestas múltiples
- ✅ Visualización de frecuencias con destaque dorado

### Métricas Clave
- **XP Total**: 275 XP (100 + 150 + 25 bonus)
- **Tiempo estimado**: 8-12 minutos
- **Complejidad**: Media-Alta
- **Tasa de éxito esperada**: >70% en 3A, >50% en 3B

---

## 1. Contexto y Narrativa

### Empresa Ficticia: TrendyShop Analytics

**Descripción**:
```
TrendyShop Analytics es una cadena de tiendas de ropa que vende camisetas
en diferentes tallas. Necesitan analizar qué tallas son las más demandadas
para optimizar su inventario y reducir costos de almacenamiento.
```

**Contexto empresarial**:
```
RestaurantData Co. está tan satisfecha con tu trabajo que te recomendaron
a TrendyShop Analytics. El CEO, Carlos Méndez, necesita saber:

"¿Cuáles son nuestros productos ESTRELLA?
¿En qué tallas deberíamos invertir más stock?"
```

### Personajes

**Jugador**: Data Engineer trainee con experiencia en media y mediana

**María González** (Mentora):
- Lead Data Engineer
- Te presenta el nuevo cliente
- Explica conceptos de moda y distribución bimodal

**Carlos Méndez** (CEO de TrendyShop):
- Necesita decisiones de inventario basadas en datos
- Quiere optimizar stock y reducir costos

---

## 2. Mecánica de la Misión

### Misión 3A: Moda Simple (Básica)

#### Dataset

```javascript
const mision3A_ventas = [
    { producto: 'Camiseta Azul', talla: 'M', cantidad: 45 },
    { producto: 'Camiseta Azul', talla: 'L', cantidad: 32 },
    { producto: 'Camiseta Azul', talla: 'S', cantidad: 28 },
    { producto: 'Camiseta Azul', talla: 'XL', cantidad: 15 },
    { producto: 'Camiseta Azul', talla: 'M', cantidad: 38 }  // M se repite
];

// Análisis:
// Tallas vendidas: M, L, S, XL, M
// Moda = M (aparece 2 veces)
// Total por talla:
//   M: 83 unidades (2 tiendas)
//   L: 32 unidades (1 tienda)
//   S: 28 unidades (1 tienda)
//   XL: 15 unidades (1 tienda)
```

#### Visualización

Gráfico de barras con frecuencias:
```
M:  ████████████ 83 unidades (2 tiendas) ⭐
L:  ████████ 32 unidades (1 tienda)
S:  ███████ 28 unidades (1 tienda)
XL: ████ 15 unidades (1 tienda)
```

#### Pregunta
"¿Cuál es la talla MÁS vendida?"

#### Respuesta Esperada
- "M" o "m" (case-insensitive)
- También acepta: "Mediana", "Medium", "m"

#### Recompensas
- Respuesta correcta primera vez: **+100 XP**
- Con 1 hint: +80 XP
- Con 2 hints: +60 XP
- Con 3 hints: +50 XP

---

### Misión 3B: Distribución Bimodal (Avanzada)

#### Dataset

```javascript
const mision3B_ventas = [
    { tienda: 'Tienda 1', talla_mas_vendida: 'M', unidades: 45 },
    { tienda: 'Tienda 2', talla_mas_vendida: 'L', unidades: 43 },
    { tienda: 'Tienda 3', talla_mas_vendida: 'M', unidades: 41 },
    { tienda: 'Tienda 4', talla_mas_vendida: 'L', unidades: 42 },
    { tienda: 'Tienda 5', talla_mas_vendida: 'M', unidades: 38 },
    { tienda: 'Tienda 6', talla_mas_vendida: 'L', unidades: 44 },
    { tienda: 'Tienda 7', talla_mas_vendida: 'S', unidades: 25 }
];

// Análisis de frecuencias:
// M: 3 tiendas (45, 41, 38) = 124 unidades totales
// L: 3 tiendas (43, 42, 44) = 129 unidades totales
// S: 1 tienda (25) = 25 unidades totales
//
// ¡DISTRIBUCIÓN BIMODAL! M y L aparecen 3 veces cada una
```

#### Visualización

Histograma de frecuencias:
```
Frecuencia por talla:
M: ███ 3 tiendas ⭐
L: ███ 3 tiendas ⭐ ← ¡Empate!
S: █ 1 tienda
```

Tabla de frecuencias:
```
┌───────┬────────────────────┬─────────────────┐
│ Talla │ Frecuencia         │ Total Unidades  │
├───────┼────────────────────┼─────────────────┤
│ M     │ ⭐ 3 tiendas       │ 124 unidades    │
│ L     │ ⭐ 3 tiendas       │ 129 unidades    │
│ S     │ 1 tienda           │ 25 unidades     │
└───────┴────────────────────┴─────────────────┘
```

#### Pregunta
"¿Cuál(es) es/son la(s) talla(s) más vendida(s)? (Separa con coma si hay más de una)"

#### Respuestas Aceptadas
- "M,L" o "L,M" (cualquier orden)
- "M, L" o "L, M" (con espacios)
- "m,l" o "l,m" (case-insensitive)
- "M y L" o "L y M" (con "y")

#### Recompensas
- Respuesta correcta primera vez: **+150 XP**
- Con 1 hint: +120 XP
- Con 2 hints: +100 XP
- Con 3 hints: +80 XP
- **BONUS** por identificar distribución bimodal: **+25 XP**

**Total posible**: 175 XP (150 + 25 bonus)

---

## 3. Sistema de XP y Progresión

### Tabla de Recompensas

| Misión    | Sin Hints  | 1 Hint     | 2 Hints    | 3 Hints    | Bonus   |
| --------- | ---------- | ---------- | ---------- | ---------- | ------- |
| 3A        | 100 XP     | 80 XP      | 60 XP      | 50 XP      | -       |
| 3B        | 150 XP     | 120 XP     | 100 XP     | 80 XP      | +25 XP  |
| **Total** | **275 XP** | **225 XP** | **185 XP** | **155 XP** | **+25** |

### Progresión de Nivel

Con 275 XP adicionales:
- Si el jugador tiene 300 XP (Misiones 1-2), llegará a **575 XP total**
- Nivel esperado: **Nivel 3-4** (dependiendo de la curva de XP)

---

## 4. Sistema de Hints

### Misión 3A - Hints Progresivos

```javascript
const hints3A = [
    {
        nivel: 1,
        texto: "💡 Cuenta cuántas veces aparece cada talla en la lista",
        costo: 10,
        pedagogia: "Guía hacia el concepto de frecuencia"
    },
    {
        nivel: 2,
        texto: "💡 La talla M aparece en 2 tiendas diferentes. ¿Hay alguna otra que aparezca más?",
        costo: 10,
        pedagogia: "Proporciona información específica sobre M"
    },
    {
        nivel: 3,
        texto: "💡 Suma las unidades por talla: M tiene más unidades totales que las demás",
        costo: 10,
        pedagogia: "Casi da la respuesta, pero requiere cálculo"
    }
];
```

### Misión 3B - Hints Progresivos

```javascript
const hints3B = [
    {
        nivel: 1,
        texto: "💡 Cuenta cuántas tiendas vendieron más cada talla (no las unidades, sino la frecuencia)",
        costo: 15,
        pedagogia: "Clarifica que se busca frecuencia, no suma"
    },
    {
        nivel: 2,
        texto: "💡 ¿Hay DOS tallas que aparecen el mismo número de veces? Eso es una distribución bimodal",
        costo: 15,
        pedagogia: "Introduce el concepto de bimodalidad"
    },
    {
        nivel: 3,
        texto: "💡 M aparece 3 veces, L aparece 3 veces, S aparece 1 vez. ¿Cuáles son las modas?",
        costo: 20,
        pedagogia: "Da las frecuencias exactas"
    }
];
```

### Estrategia de Hints

1. **Hint 1**: Guía general sobre el concepto
2. **Hint 2**: Información más específica
3. **Hint 3**: Casi da la respuesta (requiere último paso)

**Costo total de hints**: 30 XP (3A) + 50 XP (3B) = 80 XP

---

## 5. Visualizaciones

### Gráfico de Frecuencias (Misión 3A)

#### Código JavaScript

```javascript
function createFrequencyChart(data) {
    // Contar frecuencias
    const frequencies = {};
    data.forEach(item => {
        frequencies[item.talla] = (frequencies[item.talla] || 0) + item.cantidad;
    });

    // Encontrar máximo
    const maxFreq = Math.max(...Object.values(frequencies));

    // Crear barras
    const chartHTML = Object.entries(frequencies)
        .sort((a, b) => b[1] - a[1])  // Ordenar por frecuencia descendente
        .map(([talla, freq]) => {
            const percentage = (freq / maxFreq) * 100;
            const isModa = freq === maxFreq;

            return `
                <div class="bar-container">
                    <div class="bar ${isModa ? 'moda-highlight' : ''}"
                         style="height: ${percentage}%">
                        <span class="bar-value">${freq} unidades</span>
                    </div>
                    <span class="bar-label">${talla}</span>
                </div>
            `;
        }).join('');

    return chartHTML;
}
```

#### CSS para Destacar Moda

```css
.moda-highlight {
    background: linear-gradient(180deg, #ffd700 0%, #ff8c00 100%) !important;
    border: 2px solid #ffd700;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    animation: pulse-gold 2s infinite;
}

@keyframes pulse-gold {
    0%, 100% {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    50% {
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
    }
}
```

---

### Tabla de Frecuencias (Misión 3B)

#### HTML

```html
<div class="frequency-table">
    <h3>📊 Análisis de Frecuencias</h3>
    <table>
        <thead>
            <tr>
                <th>Talla</th>
                <th>Frecuencia (tiendas)</th>
                <th>Total Unidades</th>
            </tr>
        </thead>
        <tbody>
            <tr class="moda-row">
                <td>M</td>
                <td>⭐ 3 tiendas</td>
                <td>124 unidades</td>
            </tr>
            <tr class="moda-row">
                <td>L</td>
                <td>⭐ 3 tiendas</td>
                <td>129 unidades</td>
            </tr>
            <tr>
                <td>S</td>
                <td>1 tienda</td>
                <td>25 unidades</td>
            </tr>
        </tbody>
    </table>
</div>
```

#### CSS

```css
.frequency-table {
    background: rgba(0, 0, 0, 0.3);
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}

.frequency-table table {
    width: 100%;
    border-collapse: collapse;
}

.frequency-table th {
    background: rgba(255, 255, 255, 0.2);
    padding: 10px;
    text-align: left;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.frequency-table td {
    padding: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.moda-row {
    background: rgba(255, 215, 0, 0.2);
    border-left: 4px solid #ffd700;
}
```

---

## 6. Validación de Respuestas

### Función de Validación (Misión 3A)

```javascript
function checkAnswerMission3A(userAnswer) {
    // Normalizar respuesta
    const normalized = userAnswer.trim().toUpperCase();

    // Respuestas aceptadas
    const correctAnswers = ['M', 'MEDIANA', 'MEDIUM'];
    const isCorrect = correctAnswers.includes(normalized);

    if (isCorrect) {
        showFeedback('success', `
            ✅ ¡CORRECTO, ${gameState.playerName.toUpperCase()}!

            La moda es: M (talla Mediana)

            Análisis:
            - Talla M: 83 unidades (2 tiendas)
            - Talla L: 32 unidades (1 tienda)
            - Talla S: 28 unidades (1 tienda)
            - Talla XL: 15 unidades (1 tienda)

            La talla M es la MÁS FRECUENTE (aparece en más tiendas).

            Decisión de negocio:
            TrendyShop debe priorizar stock de talla M en sus próximos pedidos.

            María: "¡Perfecto! Ahora el CEO sabe en qué talla invertir más.
            Pero... ¿qué pasa cuando HAY DOS tallas igual de populares?
            Eso lo veremos en la siguiente misión."

            +100 XP ganados
        `);

        giveXP(100);

        if (!gameState.missionsCompleted.includes('mission_3a')) {
            gameState.missionsCompleted.push('mission_3a');
            saveGame();
        }

        document.getElementById('submitBtn').disabled = true;
    } else {
        // Analizar error común
        if (['L', 'S', 'XL'].includes(normalized)) {
            showFeedback('error', `
                ❌ Incorrecto.

                La talla ${normalized} no es la más frecuente.

                💡 Hint: Cuenta cuántas veces aparece CADA talla en la lista.
                La moda es la que aparece MÁS VECES.
            `);
        } else if (!isNaN(parseFloat(userAnswer))) {
            showFeedback('error', `
                ❌ Incorrecto.

                María: "Parece que estás intentando calcular la MEDIA de las unidades.
                Pero aquí no queremos el promedio, queremos la MODA."

                💡 Recuerda:
                - MEDIA = promedio de valores numéricos
                - MODA = valor que aparece MÁS VECES

                En este caso, no sumes las unidades. Solo cuenta:
                ¿Qué talla aparece en MÁS TIENDAS?
            `);
        } else {
            showFeedback('error', `
                ❌ Incorrecto.

                💡 Hint: La moda es el valor que aparece con MÁS FRECUENCIA.
                Revisa el gráfico y cuenta cuántas veces aparece cada talla.
            `);
        }
    }
}
```

### Función de Validación (Misión 3B)

```javascript
function checkAnswerMission3B(userAnswer) {
    // Normalizar respuesta
    const normalized = userAnswer
        .toUpperCase()
        .replace(/\s+/g, '')      // Eliminar espacios
        .replace(/Y/g, ',')       // Reemplazar "y" por coma
        .split(',')               // Separar por coma
        .filter(x => x.length > 0) // Eliminar vacíos
        .sort()                   // Ordenar alfabéticamente
        .join(',');

    // Respuestas correctas posibles
    const correctAnswers = ['L,M', 'M,L'];
    const isCorrect = correctAnswers.includes(normalized);

    if (isCorrect) {
        showFeedback('success', `
            ✅ ¡EXCELENTE! Has identificado la distribución BIMODAL.

            Análisis:
            - Talla M: 3 tiendas (124 unidades totales)
            - Talla L: 3 tiendas (129 unidades totales)

            Ambas tienen la MISMA FRECUENCIA (3 tiendas), por lo que
            ambas son MODAS.

            📊 Distribución Bimodal:
            Cuando DOS valores tienen la misma frecuencia máxima, tenemos
            una distribución bimodal. Esto indica:
            - Dos segmentos de clientes distintos
            - Dos productos igual de populares
            - Necesidad de stock balanceado

            Decisión de negocio:
            TrendyShop debe mantener stock EQUILIBRADO de tallas M y L,
            ya que ambas son igual de populares en diferentes tiendas.

            +150 XP ganados
            +25 XP BONUS por identificar distribución bimodal correctamente
        `);

        giveXP(150);
        giveXP(25); // Bonus

        if (!gameState.missionsCompleted.includes('mission_3b')) {
            gameState.missionsCompleted.push('mission_3b');
            saveGame();
        }

        document.getElementById('submitBtn').disabled = true;
    } else {
        // Analizar error común
        if (normalized === 'M' || normalized === 'L') {
            showFeedback('error', `
                ❌ Casi correcto, pero...

                Has identificado UNA de las modas, pero falta la otra.

                💡 Hint: Mira la tabla de frecuencias. ¿Hay OTRA talla
                que también aparezca 3 veces?

                Recuerda: Si dos valores tienen la misma frecuencia máxima,
                AMBOS son modas (distribución bimodal).

                Formato: Separa ambas tallas con coma (ej: "M,L" o "L,M")
            `);
        } else if (normalized.includes('S')) {
            showFeedback('error', `
                ❌ Incorrecto.

                La talla S solo aparece en 1 tienda, no es una moda.

                💡 Hint: Las modas son las tallas con MAYOR frecuencia.
                Busca las que aparecen MÁS VECES.
            `);
        } else {
            showFeedback('error', `
                ❌ Incorrecto.

                💡 Hint: No te fijes en las UNIDADES vendidas, sino en
                cuántas TIENDAS vendieron más cada talla.

                Cuenta: ¿Cuántas tiendas tienen M como talla más vendida?
                ¿Y cuántas tienen L?

                Si dos tallas tienen la misma frecuencia máxima, ambas son modas.
                Formato: "M,L" o "L,M"
            `);
        }
    }
}
```

---

## 7. Escenas de Tutorial

### Escena 8: Introducción a la Moda

```html
<div class="story-scene" id="scene8">
    <h2 style="font-size: 2rem; margin-bottom: 30px;">📊 Nueva Métrica: La Moda</h2>

    <div class="dialogue">
        <strong>María:</strong> "¡Excelente trabajo con media y mediana!
        Ahora te presento a un nuevo cliente..."
    </div>

    <div class="character">
        <div class="character-avatar">👔</div>
        <div class="character-info">
            <div class="character-name">Carlos Méndez</div>
            <div class="character-role">CEO - TrendyShop Analytics</div>
        </div>
    </div>

    <div class="dialogue">
        <strong>Carlos:</strong> "Vendemos camisetas en diferentes tallas.
        Necesito saber: ¿En qué tallas debo invertir más stock?"
        <br><br>
        <em>Muestra una hoja con datos de ventas</em>
        <br><br>
        "Tengo las ventas de la última semana, pero no sé cómo interpretarlas."
    </div>

    <div class="dialogue">
        <strong>María:</strong> "Mira estos datos, ${gameState.playerName}:"
        <br><br>
        <code style="background: rgba(0,0,0,0.3); padding: 10px; display: block; border-radius: 5px;">
        Tallas vendidas: S, M, L, M, S, M, L, M, XL, M, S, M
        </code>
        <br>
        "¿Puedes calcular la media o mediana de esto?"
        <br><br>
        <em>Pausa para reflexión</em>
        <br><br>
        "¡NO! Porque son CATEGORÍAS, no números. Aquí necesitamos la <strong style="color: #ffd700;">MODA</strong>."
    </div>

    <div class="tutorial-box">
        <div class="tutorial-title">💡 ¿Qué es la Moda?</div>
        <div class="tutorial-content">
            La <strong>moda</strong> es el valor que aparece con
            <strong>MÁS FRECUENCIA</strong> en un conjunto de datos.
            <br><br>
            <strong>Diferencia clave:</strong>
            <ul style="margin-top: 10px; margin-left: 20px;">
                <li>📊 <strong>Media</strong>: Promedio (solo para números)</li>
                <li>📍 <strong>Mediana</strong>: Valor del medio (solo para números)</li>
                <li>⭐ <strong>Moda</strong>: Más frecuente (¡funciona con categorías!)</li>
            </ul>
            <br>
            <strong>Ejemplo:</strong><br>
            Tallas vendidas: S, M, L, M, S, M<br>
            Moda = <strong>M</strong> (aparece 3 veces)
            <br><br>
            <strong>¿Para qué sirve?</strong>
            <ul style="margin-top: 10px; margin-left: 20px;">
                <li>Identificar productos más vendidos</li>
                <li>Encontrar tallas más demandadas</li>
                <li>Detectar patrones de comportamiento</li>
                <li>Decidir qué stock mantener</li>
            </ul>
        </div>
    </div>

    <div class="story-actions">
        <button class="story-btn" onclick="backToGame()">⬅️ Volver al Juego</button>
        <div style="display: flex; gap: 15px; align-items: center;">
            <div class="keyboard-hint">⌨️ <span class="key-indicator">Enter</span></div>
            <button class="story-btn primary" onclick="nextScene(9)">➡️ Continuar</button>
        </div>
    </div>
</div>
```

### Escena 9: Tutorial Distribución Bimodal

```html
<div class="story-scene" id="scene9">
    <h2 style="font-size: 2rem; margin-bottom: 30px;">📈 Distribución Bimodal</h2>

    <div class="dialogue">
        <strong>María:</strong> "Antes de empezar, déjame explicarte algo importante..."
        <br><br>
        "A veces, NO hay una sola moda. Puede haber DOS o más valores
        con la misma frecuencia máxima."
    </div>

    <div class="tutorial-box">
        <div class="tutorial-title">📊 Distribución Bimodal</div>
        <div class="tutorial-content">
            Cuando <strong>DOS valores</strong> tienen la misma frecuencia máxima,
            tenemos una <strong>distribución BIMODAL</strong>.
            <br><br>
            <strong>Ejemplo:</strong><br>
            Ventas: M, M, M, L, L, L, S<br>
            Modas = <strong>M y L</strong> (ambas aparecen 3 veces)
            <br><br>
            <strong>¿Qué significa en negocio?</strong>
            <ul style="margin-top: 10px; margin-left: 20px;">
                <li>✅ Dos segmentos de clientes distintos</li>
                <li>✅ Dos productos igual de populares</li>
                <li>✅ Necesidad de stock balanceado</li>
                <li>✅ No priorizar uno sobre el otro</li>
            </ul>
            <br>
            <strong style="color: #32cd32;">Importante:</strong>
            Si encuentras una distribución bimodal, debes reportar
            <strong>AMBAS modas</strong>, no solo una.
            <br><br>
            <strong>Ejemplo real:</strong><br>
            Si TrendyShop vende igual cantidad de tallas M y L, debe
            mantener stock equilibrado de ambas. Priorizar solo una
            causaría pérdida de ventas de la otra.
        </div>
    </div>

    <div class="dialogue">
        <strong>María:</strong> "En la primera parte de esta misión,
        trabajarás con una moda simple. En la segunda parte, te enfrentarás
        a una distribución bimodal. ¿Listo/a?"
    </div>

    <div class="story-actions">
        <button class="story-btn" onclick="nextScene(8)">⬅️ Atrás</button>
        <div style="display: flex; gap: 15px; align-items: center;">
            <div class="keyboard-hint">⌨️ <span class="key-indicator">Enter</span></div>
            <button class="story-btn primary" onclick="startMission3A()">🚀 ¡EMPEZAR MISIÓN 3A!</button>
        </div>
    </div>
</div>
```

---

## 8. Panel de Ayuda

### Ayuda Estadística (Misión 3A)

```javascript
function updateHelperMission3A() {
    // Calcular frecuencias
    const frequencies = {};
    mision3A_ventas.forEach(item => {
        frequencies[item.talla] = (frequencies[item.talla] || 0) + 1;
    });

    const totalUnits = {};
    mision3A_ventas.forEach(item => {
        totalUnits[item.talla] = (totalUnits[item.talla] || 0) + item.cantidad;
    });

    document.getElementById('helperTab').innerHTML = `
        <div class="stats-helper">
            <h3 style="margin-bottom: 15px;">📊 Ayuda Estadística</h3>

            <div class="helper-item">
                <div class="helper-label">Total de tiendas:</div>
                <div class="helper-value">${mision3A_ventas.length}</div>
            </div>

            <div class="helper-item">
                <div class="helper-label">Tallas diferentes:</div>
                <div class="helper-value">${Object.keys(frequencies).length}</div>
            </div>

            <div class="helper-item">
                <div class="helper-label">Frecuencias (tiendas):</div>
                <div style="margin-top: 10px;">
                    ${Object.entries(frequencies)
                        .sort((a, b) => b[1] - a[1])
                        .map(([talla, freq]) => `
                            <div style="margin-bottom: 5px;">
                                ${talla}: ${freq} ${freq > 1 ? 'tiendas' : 'tienda'}
                            </div>
                        `).join('')}
                </div>
            </div>

            <div class="helper-item">
                <div class="helper-label">Total unidades por talla:</div>
                <div style="margin-top: 10px;">
                    ${Object.entries(totalUnits)
                        .sort((a, b) => b[1] - a[1])
                        .map(([talla, units]) => `
                            <div style="margin-bottom: 5px;">
                                ${talla}: ${units} unidades
                            </div>
                        `).join('')}
                </div>
            </div>

            <div class="helper-item" style="background: rgba(255, 215, 0, 0.2); border: 2px solid #ffd700;">
                <div class="helper-label">💡 Recuerda:</div>
                <div style="margin-top: 10px; font-size: 0.95rem;">
                    La <strong>moda</strong> es el valor que aparece
                    <strong>MÁS VECES</strong>.
                    <br><br>
                    Busca la talla con mayor <strong>frecuencia</strong>
                    (no la que tiene más unidades totales).
                </div>
            </div>
        </div>
    `;
}
```

### Ayuda Estadística (Misión 3B)

```javascript
function updateHelperMission3B() {
    // Calcular frecuencias
    const frequencies = {};
    mision3B_ventas.forEach(item => {
        frequencies[item.talla_mas_vendida] = (frequencies[item.talla_mas_vendida] || 0) + 1;
    });

    const totalUnits = {};
    mision3B_ventas.forEach(item => {
        totalUnits[item.talla_mas_vendida] = (totalUnits[item.talla_mas_vendida] || 0) + item.unidades;
    });

    const maxFreq = Math.max(...Object.values(frequencies));

    document.getElementById('helperTab').innerHTML = `
        <div class="stats-helper">
            <h3 style="margin-bottom: 15px;">📊 Ayuda Estadística</h3>

            <div class="helper-item">
                <div class="helper-label">Total de tiendas:</div>
                <div class="helper-value">${mision3B_ventas.length}</div>
            </div>

            <div class="helper-item">
                <div class="helper-label">Tallas diferentes:</div>
                <div class="helper-value">${Object.keys(frequencies).length}</div>
            </div>

            <div class="helper-item">
                <div class="helper-label">Tabla de Frecuencias:</div>
                <table style="width: 100%; margin-top: 10px; border-collapse: collapse;">
                    <thead>
                        <tr style="background: rgba(255,255,255,0.1);">
                            <th style="padding: 5px; text-align: left;">Talla</th>
                            <th style="padding: 5px; text-align: center;">Frecuencia</th>
                            <th style="padding: 5px; text-align: right;">Unidades</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${Object.entries(frequencies)
                            .sort((a, b) => b[1] - a[1])
                            .map(([talla, freq]) => {
                                const isModa = freq === maxFreq;
                                const style = isModa ? 'background: rgba(255,215,0,0.2); border-left: 3px solid #ffd700;' : '';
                                return `
                                    <tr style="${style}">
                                        <td style="padding: 5px;">${isModa ? '⭐ ' : ''}${talla}</td>
                                        <td style="padding: 5px; text-align: center;">${freq} tiendas</td>
                                        <td style="padding: 5px; text-align: right;">${totalUnits[talla]} u.</td>
                                    </tr>
                                `;
                            }).join('')}
                    </tbody>
                </table>
            </div>

            <div class="helper-item" style="background: rgba(255, 215, 0, 0.2); border: 2px solid #ffd700;">
                <div class="helper-label">💡 Recuerda:</div>
                <div style="margin-top: 10px; font-size: 0.95rem;">
                    Si <strong>DOS tallas</strong> tienen la misma frecuencia máxima,
                    ambas son <strong>MODAS</strong> (distribución bimodal).
                    <br><br>
                    Formato de respuesta: "M,L" o "L,M"
                </div>
            </div>
        </div>
    `;
}
```

---

## 9. Implementación Técnica

### Función Auxiliar: Calcular Moda

```javascript
/**
 * Calcula la moda (valor más frecuente) de un array de datos
 * @param {Array} datos - Array de valores (pueden ser strings o números)
 * @returns {Object} - Objeto con modas, frecuencias y tipo de distribución
 */
function calcularModa(datos) {
    // Contar frecuencias
    const frequencies = {};
    datos.forEach(valor => {
        frequencies[valor] = (frequencies[valor] || 0) + 1;
    });

    // Encontrar frecuencia máxima
    const maxFreq = Math.max(...Object.values(frequencies));

    // Encontrar todos los valores con frecuencia máxima
    const modas = Object.entries(frequencies)
        .filter(([_, freq]) => freq === maxFreq)
        .map(([valor, _]) => valor);

    return {
        modas: modas,
        frequencies: frequencies,
        maxFrequency: maxFreq,
        esBimodal: modas.length === 2,
        esMultimodal: modas.length > 2,
        esUnimodal: modas.length === 1
    };
}
```

### Función: Iniciar Misión 3A

```javascript
function startMission3A() {
    // Ocultar pantallas
    document.getElementById('storyScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';

    // Configurar misión
    gameState.currentMissionType = 'mission_3a';
    gameState.currentMissionData = mision3A_ventas;

    // Actualizar UI
    document.querySelector('.mission-title').textContent =
        '📋 Misión 3A: Identificar la Talla Más Vendida';

    document.querySelector('.mission-description').innerHTML = `
        <p><strong>🏢 Cliente: TrendyShop Analytics</strong></p>
        <p style="margin-top: 10px;">
            Analiza las ventas de camisetas azules en diferentes tiendas.
        </p>
        <p style="margin-top: 10px;">
            <strong>Tu tarea:</strong> Identifica la <strong>talla MÁS VENDIDA</strong>
            (la que aparece en más tiendas).
        </p>
        <p style="margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
            💡 Pista: No sumes las unidades, cuenta la <strong>frecuencia</strong>
            (cuántas veces aparece cada talla).
        </p>
    `;

    // Actualizar hints
    document.querySelector('.hints').innerHTML = `
        <div class="hint-title">💡 Recuerda:</div>
        <p><strong>Moda</strong> = Valor que aparece MÁS VECES</p>
        <p style="margin-top: 10px;">
            No sumes las unidades, cuenta cuántas veces aparece cada talla.
        </p>
        <p style="margin-top: 10px; font-size: 0.9rem;">
            Usa el panel de <strong>📊 Ayuda</strong> para ver las frecuencias →
        </p>
    `;

    // Cargar visualizaciones
    loadFrequencyChartMission3A();
    updateHelperMission3A();

    // Limpiar inputs
    document.getElementById('answerInput').value = '';
    document.getElementById('answerInput').type = 'text';
    document.getElementById('answerInput').placeholder = 'Ingresa la talla (ej: M)';
    document.getElementById('feedback').innerHTML = '';
    document.getElementById('submitBtn').disabled = false;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    saveGame();
}
```

### Función: Iniciar Misión 3B

```javascript
function startMission3B() {
    // Ocultar pantallas
    document.getElementById('storyScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';

    // Configurar misión
    gameState.currentMissionType = 'mission_3b';
    gameState.currentMissionData = mision3B_ventas;

    // Actualizar UI
    document.querySelector('.mission-title').textContent =
        '📋 Misión 3B: Distribución Bimodal (Avanzado)';

    document.querySelector('.mission-description').innerHTML = `
        <p><strong>🏢 Cliente: TrendyShop Analytics (Zona Premium)</strong></p>
        <p style="margin-top: 10px;">
            Analiza las ventas de 7 tiendas en zona premium. Cada tienda reporta
            su talla más vendida.
        </p>
        <p style="margin-top: 10px;">
            <strong>Tu tarea:</strong> Identifica la(s) <strong>talla(s) MÁS FRECUENTE(s)</strong>.
        </p>
        <p style="margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
            ⚠️ <strong>Importante:</strong> Si hay DOS tallas con la misma frecuencia máxima,
            debes reportar AMBAS separadas por coma (ej: "M,L").
        </p>
    `;

    // Actualizar hints
    document.querySelector('.hints').innerHTML = `
        <div class="hint-title">💡 Recuerda:</div>
        <p><strong>Distribución Bimodal</strong> = DOS modas con igual frecuencia</p>
        <p style="margin-top: 10px;">
            Cuenta cuántas tiendas tienen cada talla como la más vendida.
        </p>
        <p style="margin-top: 10px; font-size: 0.9rem;">
            Si dos tallas aparecen el mismo número de veces, ambas son modas.
        </p>
    `;

    // Cargar visualizaciones
    loadFrequencyChartMission3B();
    updateHelperMission3B();

    // Limpiar inputs
    document.getElementById('answerInput').value = '';
    document.getElementById('answerInput').type = 'text';
    document.getElementById('answerInput').placeholder = 'Ingresa la(s) talla(s) (ej: M,L)';
    document.getElementById('feedback').innerHTML = '';
    document.getElementById('submitBtn').disabled = false;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    saveGame();
}
```

---

## 10. Criterios de Éxito

### Checklist de Implementación

#### Escenas de Tutorial
- [ ] Escena 8 (Introducción a la Moda) implementada
- [ ] Escena 9 (Tutorial Distribución Bimodal) implementada
- [ ] Navegación entre escenas funcional
- [ ] Keyboard navigation (Enter para avanzar)

#### Misión 3A
- [ ] Dataset `mision3A_ventas` definido
- [ ] Función `startMission3A()` implementada
- [ ] Gráfico de frecuencias con destaque de moda
- [ ] Validación de respuesta `checkAnswerMission3A()`
- [ ] 3 hints progresivos funcionales
- [ ] Feedback pedagógico claro
- [ ] Panel de ayuda con frecuencias

#### Misión 3B
- [ ] Dataset `mision3B_ventas` definido
- [ ] Función `startMission3B()` implementada
- [ ] Tabla de frecuencias con destaque de modas
- [ ] Validación de respuesta `checkAnswerMission3B()`
- [ ] Acepta múltiples formatos (M,L / L,M / M y L)
- [ ] 3 hints progresivos funcionales
- [ ] Feedback con análisis de distribución bimodal
- [ ] Bonus XP por identificar bimodalidad

#### Sistema General
- [ ] Función auxiliar `calcularModa()` implementada
- [ ] Guardado de progreso en localStorage
- [ ] Transición a Misión 4 al completar ambas
- [ ] Sistema de XP funcionando correctamente
- [ ] Accesibilidad (ARIA, teclado)

#### Testing
- [ ] Probar Misión 3A con respuesta correcta
- [ ] Probar Misión 3A con respuestas incorrectas
- [ ] Probar Misión 3B con ambas modas
- [ ] Probar Misión 3B con solo una moda (error)
- [ ] Probar diferentes formatos de respuesta
- [ ] Probar sistema de hints
- [ ] Probar en móvil (responsive)
- [ ] Probar navegación con teclado

#### Documentación
- [ ] README_JUEGO_WEB.md actualizado
- [ ] CHANGELOG.md actualizado
- [ ] Comentarios en código JavaScript
- [ ] Este documento de diseño archivado

---

### Métricas de Calidad

#### Tiempo de Juego
- **Objetivo**: 8-12 minutos para completar ambas misiones
- **Desglose**:
  - Tutorial (Escenas 8-9): 2-3 minutos
  - Misión 3A: 3-4 minutos
  - Misión 3B: 3-5 minutos

#### Tasa de Éxito
- **Misión 3A**: >70% sin hints
- **Misión 3B**: >50% sin hints (más difícil)
- **Con hints**: >90% en ambas

#### XP Disponible
- **Total**: 275 XP (100 + 150 + 25 bonus)
- **Promedio esperado**: 225 XP (con 1-2 hints)
- **Mínimo**: 155 XP (con todos los hints)

#### Cobertura de Conceptos
- ✅ Concepto de moda (valor más frecuente)
- ✅ Diferencia entre moda, media y mediana
- ✅ Aplicación a datos categóricos
- ✅ Distribución bimodal
- ✅ Toma de decisiones de negocio

---

## 11. Próximos Pasos

### Implementación (Frontend)

**Responsable**: @game-design [frontend]

**Tareas**:
1. Añadir datasets `mision3A_ventas` y `mision3B_ventas` en `game.html`
2. Implementar Escenas 8 y 9 en el HTML
3. Implementar funciones JavaScript:
   - `calcularModa()`
   - `startMission3A()`
   - `startMission3B()`
   - `checkAnswerMission3A()`
   - `checkAnswerMission3B()`
   - `updateHelperMission3A()`
   - `updateHelperMission3B()`
   - `loadFrequencyChartMission3A()`
   - `loadFrequencyChartMission3B()`
4. Añadir CSS para `.moda-highlight` y `.frequency-table`
5. Integrar con sistema de progresión existente
6. Testing manual completo

**Tiempo estimado**: 6-8 horas

---

### Revisión Pedagógica

**Responsable**: @teaching [pedagogo]

**Tareas**:
1. Revisar explicaciones de moda y distribución bimodal
2. Validar que los ejemplos son claros
3. Verificar progresión de dificultad (3A → 3B)
4. Revisar feedback pedagógico
5. Sugerir mejoras si es necesario

**Tiempo estimado**: 1-2 horas

---

### Revisión UX/UI

**Responsable**: @game-design [ux]

**Tareas**:
1. Revisar usabilidad de las visualizaciones
2. Verificar accesibilidad (ARIA, teclado)
3. Probar en diferentes dispositivos
4. Validar que el destaque de modas es claro
5. Sugerir mejoras visuales

**Tiempo estimado**: 1-2 horas

---

### Testing de Calidad

**Responsable**: @quality

**Tareas**:
1. Testing manual de todas las rutas
2. Probar diferentes formatos de respuesta
3. Verificar sistema de hints
4. Validar guardado de progreso
5. Probar en diferentes navegadores
6. Generar reporte de calidad

**Tiempo estimado**: 2-3 horas

---

### Documentación

**Responsable**: @documentation

**Tareas**:
1. Actualizar `README_JUEGO_WEB.md` con Misión 3
2. Actualizar `CHANGELOG.md` con cambios
3. Archivar este documento de diseño
4. Actualizar roadmap del juego

**Tiempo estimado**: 1 hora

---

## 12. Notas Adicionales

### Decisiones de Diseño

1. **¿Por qué dos sub-misiones?**
   - 3A introduce el concepto de moda de forma simple
   - 3B añade complejidad con distribución bimodal
   - Progresión pedagógica gradual

2. **¿Por qué datos categóricos?**
   - Demuestra que la moda funciona con categorías
   - Diferencia clara con media/mediana (solo números)
   - Aplicación real en análisis de productos

3. **¿Por qué validación flexible?**
   - Usuarios pueden escribir "M,L" o "L,M"
   - Reduce frustración por formato
   - Enfoque en concepto, no en sintaxis

4. **¿Por qué bonus XP en 3B?**
   - Recompensa identificación correcta de bimodalidad
   - Motiva a entender el concepto, no solo calcular
   - Diferencia entre "acertar" y "comprender"

### Riesgos y Mitigaciones

| Riesgo                               | Probabilidad | Impacto | Mitigación                                        |
| ------------------------------------ | ------------ | ------- | ------------------------------------------------- |
| Confusión entre frecuencia y suma    | Alta         | Medio   | Hints claros, panel de ayuda con ambos valores    |
| No entender distribución bimodal     | Media        | Alto    | Tutorial dedicado (Escena 9), ejemplos claros     |
| Frustración por formato de respuesta | Media        | Bajo    | Validación flexible, acepta múltiples formatos    |
| Dificultad excesiva en 3B            | Baja         | Medio   | 3 hints progresivos, tabla de frecuencias visible |

### Feedback de Usuarios (Anticipado)

**Posibles comentarios positivos**:
- "Finalmente entendí por qué la moda es útil"
- "La visualización con destaque dorado es muy clara"
- "Me gustó que aceptara diferentes formatos de respuesta"

**Posibles comentarios negativos**:
- "No entendí la diferencia entre frecuencia y suma al principio"
- "La Misión 3B es muy difícil"
- "¿Por qué no puedo usar solo números?"

**Respuestas preparadas**:
- Panel de ayuda muestra ambos valores (frecuencia y suma)
- 3 hints progresivos para 3B
- Tutorial explica que moda funciona con categorías

---

## 13. Referencias

### Archivos del Proyecto
- **Juego principal**: `documentacion/juego/game.html`
- **README del juego**: `documentacion/juego/README_JUEGO_WEB.md`
- **Empresas ficticias**: `documentacion/juego/EMPRESAS_FICTICIAS.md`
- **CHANGELOG**: `documentacion/CHANGELOG.md`

### Issues Relacionadas
- **JAR-180**: Misión 2 (Mediana) - ✅ Completada
- **JAR-181**: Misión 3 (Moda) - 🔄 Este diseño
- **JAR-182**: Misión 4 (Percentiles) - ⏳ Pendiente
- **JAR-183**: Misión 5 (Varianza) - ⏳ Pendiente

### Conceptos Pedagógicos
- **Moda**: Valor más frecuente
- **Distribución bimodal**: Dos modas con igual frecuencia
- **Distribución multimodal**: Más de dos modas
- **Frecuencia**: Número de veces que aparece un valor
- **Datos categóricos**: Categorías, no números (tallas, colores, etc.)

---

**Documento creado por**: Game Design Team
**Fecha**: 2025-10-19
**Versión**: 1.0
**Estado**: ✅ Diseño Completo - Listo para Implementación

---

## Aprobaciones

- [ ] **@game-design [diseñador]**: Diseño completo ✅
- [ ] **@teaching [pedagogo]**: Revisión pedagógica pendiente
- [ ] **@game-design [frontend]**: Implementación pendiente
- [ ] **@game-design [ux]**: Revisión UX pendiente
- [ ] **@quality**: Testing pendiente
- [ ] **@documentation**: Documentación pendiente
- [ ] **@project-management**: Cierre pendiente
