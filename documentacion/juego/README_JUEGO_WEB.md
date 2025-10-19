# 🎮 DATA ENGINEER: THE GAME - Versión Web

## ¡Ahora sí! Versión moderna e interactiva

---

## 🚀 Cómo Jugar

### Opción 1: Abrir directamente
```
1. Haz doble click en game.html
2. Se abrirá en tu navegador
3. ¡A jugar!
```

### Opción 2: Servidor local (recomendado)
```bash
# Con Python
python -m http.server 8000

# Abre en el navegador
http://localhost:8000/game.html
```

---

## ✨ Características

### 🎨 Interfaz Visual Moderna
- **Diseño glassmorphism** (cristal esmerilado)
- **Gradientes animados**
- **Responsive** (funciona en móvil)
- **Animaciones suaves**

### 🧮 Calculadora Integrada
- **Calculadora funcional** dentro del juego
- **Botón "Copiar"** para pasar el resultado directamente
- **No necesitas calculadora física** 😄

### 📊 Visualizaciones
- **Gráfico de barras** interactivo
- **Datos clickeables** con efectos hover
- **Colores que ayudan** a entender los datos

### 📈 Ayuda Estadística
- **Panel de ayuda** con valores calculados
- **Fórmulas visuales**
- **Pistas contextuales**

### 💾 Guardado Automático
- Tu progreso se guarda en **localStorage**
- **No se pierde** al cerrar el navegador
- Continúas donde lo dejaste

---

## 🎯 Lo Que Tiene Ahora

### Misión 1: Análisis de Ventas ✅
- ✅ **Visualización de datos** (ventas de la semana)
- ✅ **Gráfico de barras** interactivo
- ✅ **Calculadora integrada** para hacer cálculos
- ✅ **Panel de ayuda** con fórmulas y pistas
- ✅ **Sistema de XP** y niveles
- ✅ **Feedback visual** (correcto/incorrecto)

### Misión 2A: Mediana con Outliers Evidentes ✅
- ✅ **Tutorial integrado** sobre mediana y outliers
- ✅ **Outliers destacados en rojo** (visualización clara)
- ✅ **Dataset con outlier evidente** (500€ vs ~55€)
- ✅ **Comparación media vs mediana** en el feedback
- ✅ **Narrativa continuada** con RestaurantData Co.
- ✅ **+75 XP** al completar

### Misión 2B: Mediana con Outliers Sutiles ✅
- ✅ **Detección automática con regla IQR** (Interquartile Range)
- ✅ **Dataset más complejo** (9 sucursales, zona premium)
- ✅ **Outliers sutiles** marcados en rojo
- ✅ **Análisis de decisiones de negocio** en el feedback
- ✅ **Tutorial de regla IQR** integrado
- ✅ **+125 XP** al completar

### Misión 3A: Moda Simple ✅
- ✅ **Primera misión con datos categóricos** (tallas, no números)
- ✅ **Tutorial integrado** sobre la moda
- ✅ **Visualización con destaque dorado** para la moda
- ✅ **Empresa ficticia**: TrendyShop Analytics
- ✅ **Diferencia entre frecuencia y suma** clarificada
- ✅ **+100 XP** al completar

### Misión 3B: Distribución Bimodal ✅
- ✅ **Concepto avanzado**: Distribución bimodal
- ✅ **Validación flexible** (acepta "M,L" o "L,M" o "M y L")
- ✅ **Tabla de frecuencias** con destaque de modas
- ✅ **Feedback pedagógico** sobre bimodalidad
- ✅ **+150 XP + 25 XP bonus** al completar

### Misión 4A: Percentil 50 (Mediana) ✅
- ✅ **Tutorial integrado** sobre percentiles y cuartiles
- ✅ **Conexión explícita** con Misión 2 (P50 = mediana)
- ✅ **Visualización de línea temporal** con Q2 marcado en dorado
- ✅ **Zonas coloreadas** (50% más rápidos vs 50% más lentos)
- ✅ **Empresa ficticia**: PerformanceAPI Analytics (monitoreo de APIs)
- ✅ **Contexto empresarial**: Establecer SLAs realistas
- ✅ **+100 XP + 20 XP bonus** al completar

### Misión 4B: Cuartiles Completos (Q1, Q2, Q3) ✅
- ✅ **Visualización de boxplot** interactivo con zonas coloreadas
- ✅ **Detección de outliers** con regla IQR
- ✅ **Cuartiles visuales**: Q1 (verde), Q2 (amarillo), Q3 (naranja), Q4 (rojo)
- ✅ **Conexión con IQR** de Misión 2B
- ✅ **Decisiones de SLA** por niveles (Premium, Estándar, Básico)
- ✅ **Nota sobre métodos de cálculo** (simplificado vs numpy/pandas)
- ✅ **+150 XP + 50 XP bonus** al completar

### Sistema de Progresión ✅
- ✅ **Desbloqueo progresivo**: Misión 1 → 2A → 2B → 3A → 3B → 4A → 4B
- ✅ **Guardado automático** en localStorage
- ✅ **Botón "Continuar"** lleva a la siguiente misión
- ✅ **Total: 895 XP** disponibles (100 + 75 + 125 + 100 + 175 + 120 + 200)

---

## 🎮 Cómo Funciona

### 1. Inicio del Juego
```
La primera vez te pregunta tu nombre
Se guarda en localStorage
Siempre aparecerá tu nombre
```

### 2. La Misión
```
María te da contexto empresarial
Ves los datos de ventas visualmente
Tienes un gráfico de barras
Tu objetivo: calcular la media
```

### 3. Herramientas
```
🧮 CALCULADORA
   - Haz clic en los botones O
   - Escribe directamente con el teclado:
     • Números: 0-9
     • Operadores: + - * /
     • Punto decimal: . o ,
     • Calcular: Enter o =
     • Borrar: Escape o Delete
     • Borrar último: Backspace
   - Copia el resultado al campo de respuesta

📊 AYUDA
   - Cantidad de datos
   - Suma total
   - Mín/Máx
   - Fórmula visual
```

### 4. Respuesta
```
Ingresas tu respuesta
Presionas "ENVIAR"
Feedback inmediato
Si aciertas: +100 XP
```

### 5. Progreso
```
XP se acumula
Barra visual de progreso
Subes de nivel
Desblocas más misiones
```

---

## 🎨 Capturas (conceptuales)

### Header
```
╔══════════════════════════════════════════════════╗
║          DATA ENGINEER: THE GAME                 ║
╠══════════════════════════════════════════════════╣
║  👤 Juan  |  🎓 Trainee  |  ⭐ Nivel 1          ║
║  XP: [████████░░░░░░░░] 50 / 100 XP             ║
╚══════════════════════════════════════════════════╝
```

### Misión + Herramientas
```
┌────────────────────────────────┬──────────────────┐
│  📋 Misión 1: Ventas          │  🧮 Calculadora  │
│                                │                  │
│  Datos: [145.30€] [132.50€]   │   [7] [8] [9] [/]│
│                                │   [4] [5] [6] [×]│
│  📊 Gráfico de Barras         │   [1] [2] [3] [-]│
│  ▂▃█▅▇█▆                      │   [0] [.] [C] [+]│
│                                │   [  =  ] [Copiar]│
│  ✍️ Tu Respuesta:             │                  │
│  [    176.06     ]            │  📊 Ayuda        │
│  [🚀 ENVIAR]                  │  Suma: 1232.45€  │
│                                │  Cantidad: 7     │
│  💡 Recuerda:                 │  Media = ? / 7   │
│  Media = Suma / Cantidad       │                  │
└────────────────────────────────┴──────────────────┘
```

---

## 💡 Por Qué Es Mejor Que la Versión Terminal

### ❌ Versión Terminal (Antigua)
```
- Texto plano y aburrido
- Necesitas calculadora física
- Sin visualizaciones
- No es intuitivo
- Parece de 1990
```

### ✅ Versión Web (Nueva)
```
✨ Interfaz visual bonita
🧮 Calculadora integrada
📊 Gráficos interactivos
🎨 Colores y animaciones
📱 Funciona en móvil
💾 Guardado automático
🎯 Más intuitivo
🚀 Moderno y atractivo
```

---

## 🛠️ Tecnologías Usadas

- **HTML5**: Estructura
- **CSS3**: Estilos modernos (glassmorphism, gradientes)
- **JavaScript vanilla**: Lógica del juego
- **localStorage**: Guardado de progreso
- **Responsive design**: Funciona en cualquier pantalla

**Sin dependencias externas** → Funciona offline

---

## 🚀 Roadmap Versión Web

### ✅ Implementado (v1.3)
- Misión 1 completa (Media)
- Misión 2A completa (Mediana con outliers evidentes)
- Misión 2B completa (Mediana con outliers sutiles)
- Misión 3A completa (Moda simple)
- Misión 3B completa (Distribución bimodal)
- Misión 4A completa (Percentil 50 - Mediana)
- Misión 4B completa (Cuartiles Q1, Q2, Q3)
- Calculadora funcional
- Sistema de XP y progresión
- Visualizaciones avanzadas:
  - Outliers y modas destacados
  - Línea temporal con Q2
  - Boxplot interactivo con cuartiles
- Guardado automático
- Sistema de desbloqueo progresivo
- Tabla de frecuencias interactiva

### 🚧 Próximo (v1.4)
- [ ] Misión 5: Varianza y desviación estándar
- [ ] Misión 6: Correlación y regresión lineal
- [ ] Dashboard completo de stats
- [ ] Sistema de logros con badges visuales
- [ ] Animaciones de level up más épicas
- [ ] Sonidos y efectos

### 🔮 Futuro (v2.0)
- [ ] Todos los módulos del Master
- [ ] Editor de código integrado (Monaco Editor)
- [ ] Terminal web para ejecutar Python
- [ ] Multiplayer (competir con amigos)
- [ ] Leaderboard online
- [ ] Certificados descargables

---

## 🎯 Comparación: Terminal vs Web

| Característica     | Terminal     | Web                 |
| ------------------ | ------------ | ------------------- |
| **Visual**         | ❌ Solo texto | ✅ Gráficos, colores |
| **Calculadora**    | ❌ Externa    | ✅ Integrada         |
| **Interactividad** | ❌ Baja       | ✅ Alta              |
| **Gráficos**       | ❌ No         | ✅ Sí                |
| **Móvil**          | ❌ No         | ✅ Sí                |
| **Moderno**        | ❌ Años 90    | ✅ 2025              |
| **Diversión**      | ⭐⭐           | ⭐⭐⭐⭐⭐               |

---

## 🐛 Troubleshooting

### El juego no se ve bien
```
- Usa Chrome, Firefox o Edge moderno
- Actualiza tu navegador
- Verifica que JavaScript esté habilitado
```

### No se guarda el progreso
```
- Verifica que las cookies/localStorage estén permitidos
- No uses modo incógnito
- Abre siempre desde la misma URL
```

### La calculadora no funciona
```
- Verifica que JavaScript esté habilitado
- Refresca la página (F5)
- Abre la consola (F12) para ver errores
```

---

## 📱 Compatibilidad

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ Móviles (iOS/Android)

---

## 🎮 Tips para Jugar

### 1. Usa la Calculadora
```
No necesitas calculadora física
Suma todos los valores
Divide por 7
Presiona "Copiar" para pasar el resultado
```

### 2. Observa el Gráfico
```
El gráfico te ayuda a visualizar
Identifica valores altos y bajos
Hover para ver detalles
```

### 3. Usa el Panel de Ayuda
```
Te da la suma total
Te muestra la fórmula
Son pistas sin dar la respuesta
```

### 4. No Te Frustres
```
Puedes intentar las veces que quieras
Usa las herramientas disponibles
Lee las pistas
```

---

## ✅ Mejoras Implementadas (2025-10-19)

### Pedagógicas
- ✅ **Comentarios explicativos** sobre cálculo de percentiles (método simplificado)
- ✅ **Aclaración de métodos** de detección de outliers (2A vs 2B)
- ✅ **Clarificación conceptual**: Mediana incluye outliers (no los excluye)
- ✅ **Nota de tolerancia**: ±0.5€ visible en panel de ayuda

### Accesibilidad
- ✅ **Etiquetas ARIA**: role="alert", aria-live, aria-label en elementos clave
- ✅ **Navegación por teclado**: Estilos :focus y :focus-visible
- ✅ **Feedback visual**: Outline dorado (#ffd700) al navegar con Tab
- ✅ **Screen readers**: Soporte mejorado con aria-atomic y aria-describedby

### Calidad
- ✅ **Revisión pedagógica**: 9.2/10 (Psicólogo Educativo)
- ✅ **Revisión UX/UI**: 9.0/10 (Especialista UX/UI)
- ✅ **Reportes completos**: `REVISION_PEDAGOGICA_MISION_2.md` y `REVISION_UX_UI_GAME.md`

---

## 🎨 Próximas Mejoras Visuales

### Animaciones
- [ ] Confetti al completar misión
- [ ] Partículas de XP flotantes
- [ ] Transiciones más suaves
- [ ] Loading spinners

### UX
- [ ] Tooltips explicativos personalizados
- [ ] Indicador de carga entre misiones
- [ ] Modo oscuro/claro (toggle)
- [ ] Mini-map de progreso

### Gamificación
- [ ] Racha de días (streaks)
- [ ] Desafíos diarios
- [ ] Modo competitivo
- [ ] Rankings

---

## 🤝 Feedback

Si tienes ideas o sugerencias:
1. ¿Qué te gustaría ver?
2. ¿Qué mejorarías?
3. ¿Qué otras herramientas necesitas?

---

## 🎉 ¡A Jugar!

```bash
# Abre game.html en tu navegador
# O ejecuta:
python -m http.server 8000

# Y abre:
# http://localhost:8000/game.html
```

**¡Diviértete aprendiendo Data Engineering! 🚀**

---

**Versión:** 1.3 Web (con Misión 4: Percentiles y Cuartiles)
**Última actualización:** 2025-10-19
**Creado con:** ❤️, HTML, CSS y JavaScript
