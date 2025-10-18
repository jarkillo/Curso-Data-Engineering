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

### Misión 1: Análisis de Ventas
- ✅ **Visualización de datos** (ventas de la semana)
- ✅ **Gráfico de barras** interactivo
- ✅ **Calculadora integrada** para hacer cálculos
- ✅ **Panel de ayuda** con fórmulas y pistas
- ✅ **Sistema de XP** y niveles
- ✅ **Feedback visual** (correcto/incorrecto)

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

### ✅ Implementado (v1.0)
- Misión 1 completa
- Calculadora funcional
- Sistema de XP
- Visualizaciones
- Guardado automático

### 🚧 Próximo (v1.1)
- [ ] Misión 2: Calcular mediana con outliers
- [ ] Misión 3: Identificar moda (productos más vendidos)
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

| Característica | Terminal | Web |
|---------------|----------|-----|
| **Visual** | ❌ Solo texto | ✅ Gráficos, colores |
| **Calculadora** | ❌ Externa | ✅ Integrada |
| **Interactividad** | ❌ Baja | ✅ Alta |
| **Gráficos** | ❌ No | ✅ Sí |
| **Móvil** | ❌ No | ✅ Sí |
| **Moderno** | ❌ Años 90 | ✅ 2025 |
| **Diversión** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

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

## 🎨 Próximas Mejoras Visuales

### Animaciones
- [ ] Confetti al completar misión
- [ ] Partículas de XP
- [ ] Transiciones más suaves
- [ ] Loading spinners

### UX
- [ ] Tutorial interactivo
- [ ] Tooltips explicativos
- [ ] Drag & drop para datos
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

**Versión:** 1.0 Web  
**Última actualización:** 2025-10-18  
**Creado con:** ❤️, HTML, CSS y JavaScript

