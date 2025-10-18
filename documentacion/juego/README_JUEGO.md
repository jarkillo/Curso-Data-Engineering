# 🎮 DATA ENGINEER: THE GAME

## Un simulador adictivo donde aprendes Data Engineering jugando

---

## 🚀 ¿Qué es esto?

**Data Engineer: The Game** es un juego interactivo de simulación donde:

- 🎯 Completas **misiones** reales de Data Engineering
- 📈 Ganas **XP** y subes de **nivel** (de Trainee a Data Architect)
- 🏆 Desbloqueas **logros** y **tecnologías**
- 💾 Tu **progreso se guarda automáticamente**
- 📚 **Aprendes** conceptos reales mientras te diviertes

Es como un juego de simulación empresarial, pero aprenderás **Data Engineering de verdad**.

---

## 🎬 Cómo Empezar

### 1. Requisitos

```bash
Python 3.8 o superior (ya lo tienes instalado)
```

### 2. Ejecutar el Juego

```bash
# En la carpeta del proyecto
python data_engineer_game.py
```

### 3. Primera Vez

La primera vez que juegues:
1. Te pedirá tu nombre
2. Comenzarás como **Trainee** (nivel 1)
3. Verás la historia introductoria
4. Recibirás tu primera misión

### 4. Partidas Posteriores

Tu progreso se guarda en `game_save.json`. La próxima vez que juegues:
- Cargarás automáticamente tu partida guardada
- Continuarás donde lo dejaste
- Todas tus stats, XP y logros se mantienen

---

## 🎮 Cómo Jugar

### Interfaz Principal

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      DATA ENGINEER: THE GAME                             ║
╚══════════════════════════════════════════════════════════════════════════╝

👤 Juan | 💼 Junior Data Engineer | Nivel 5
XP: [████████████████░░░░░░░░] 450/700
──────────────────────────────────────────────────────────────────────────

🎮 MENÚ PRINCIPAL

  1. 🚀 Continuar Aventura (Módulo 1, Tema 1)
  2. 📊 Ver Dashboard y Estadísticas
  3. 🏆 Ver Logros
  4. 📚 Biblioteca de Aprendizaje
  5. ⚙️  Configuración
  6. 💾 Guardar y Salir
```

### Sistema de Progresión

#### Niveles
- Empiezas en **Nivel 1**
- Cada misión completada te da **XP**
- Al acumular suficiente XP, **subes de nivel**
- Cada nivel requiere más XP que el anterior

#### Rangos Profesionales

| Nivel | Rango | Emoji |
|-------|-------|-------|
| 1-2 | Trainee | 🎓 |
| 3-6 | Junior Data Engineer | 💼 |
| 7-11 | Data Engineer | 🔧 |
| 12-16 | Senior Data Engineer | ⭐ |
| 17-19 | Lead Data Engineer | 👑 |
| 20+ | Data Architect | 🏆 |

Cuando alcanzas el nivel de un nuevo rango, recibes una **PROMOCIÓN** especial.

#### Logros

Desbloquea logros especiales:
- 🏅 **Detective de Datos**: Detecta tu primer outlier
- 🧪 **Test Master**: Pasa 100 tests
- 📝 **Code Warrior**: Escribe 1,000 líneas de código
- ⚡ **Speed Runner**: Completa 10 misiones en una sesión
- Y muchos más...

Cada logro te da **+50 XP bonus**.

---

## 📖 La Historia

Trabajas para **DataFlow Industries**, una consultora de Data Engineering.

Tu jefa, **María**, te asigna a diferentes clientes en cada módulo:

### Módulo 1: RestaurantData Co.
- Cliente: Red de restaurantes
- Desafío: Análisis de ventas y estadísticas básicas
- Aprenderás: Python, estadística descriptiva, fundamentos

### Módulos Futuros
- CloudAPI Systems (APIs y pipelines)
- LogisticFlow (transformación de datos)
- FinTech Analytics (bases de datos y SQL)
- Y más...

---

## 🎯 Misiones

Las misiones son **ejercicios prácticos** con contexto real:

### Ejemplo de Misión:

```
📋 NUEVA MISIÓN

Calcular la Media de Ventas
Dificultad: Fácil | Recompensa: +100 XP

María te pasa los datos de ventas de la última semana:
    Ventas: [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]

Tu tarea: Calcular la venta promedio (media) para saber si cumplimos 
nuestro objetivo de 170€ por día.

RECORDATORIO: Media = Suma de valores / Cantidad de valores

──────────────────────────────────────────────────────────────────────────

📝 EJERCICIO:
Calcula la media de: [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40]

Objetivo: > 170€

Tu respuesta (en €): _
```

### Tipos de Misiones

- **Fácil** 🟢: Introductorias, conceptos básicos (+50-100 XP)
- **Medio** 🟡: Aplicación práctica, casos reales (+100-200 XP)
- **Difícil** 🔴: Desafíos complejos, múltiples pasos (+200-500 XP)

---

## 📊 Dashboard y Stats

Accede a tu dashboard (opción 2 del menú) para ver:

```
📊 TUS ESTADÍSTICAS

💻 CÓDIGO:
   Líneas escritas:        1,247
   Tests pasados:          42
   Bugs corregidos:        8

📚 PROGRESO:
   Proyectos completados:  3
   Ejercicios resueltos:   18
   Horas de estudio:       12

⭐ EXPERIENCIA:
   XP Total ganado:        2,450
   Logros desbloqueados:   5

🎯 PRÓXIMA PROMOCIÓN:
   ⭐ Senior Data Engineer
   Faltan 3 niveles

🔧 TECNOLOGÍAS DESBLOQUEADAS:
   Python | Git | Pandas | SQL | Docker | Airflow
```

---

## 💡 Tips para Jugar

### 1. Lee con Atención
Cada misión tiene **recordatorios** y **pistas**. Léelos antes de responder.

### 2. Usa la Biblioteca
Si no recuerdas un concepto, ve a:
- **Opción 4: Biblioteca de Aprendizaje**
- Allí puedes repasar teoría, ejemplos y fórmulas

### 3. No te Frustres
- Tienes **3 intentos** por misión
- Si fallas, puedes reintentar más tarde
- El objetivo es **aprender**, no solo ganar XP

### 4. Sigue la Historia
- El juego tiene una **narrativa progresiva**
- Cada módulo te presenta un nuevo cliente/desafío
- Es como trabajar en una consultora real

### 5. Sesiones Cortas
- Puedes jugar **5-10 minutos** y guardar
- Tu progreso se guarda automáticamente
- Perfecto para aprender en ratos libres

---

## 🎨 Características Técnicas

### Guardado Automático
Tu progreso se guarda en `game_save.json`:
```json
{
  "player_name": "Juan",
  "level": 5,
  "xp": 450,
  "current_module": 1,
  "completed_missions": ["m1t1_mission_01", "m1t1_mission_02"],
  "stats": { ... }
}
```

**NUNCA** edites este archivo manualmente o perderás tu progreso.

### Multiplataforma
- ✅ Windows
- ✅ Linux
- ✅ macOS

Funciona en cualquier sistema con Python 3.8+.

---

## 🐛 Solución de Problemas

### El juego no inicia
```bash
# Verifica tu versión de Python
python --version

# Debe ser >= 3.8
```

### Perdí mi progreso
Si borraste `game_save.json`, tu progreso se perdió. El juego creará una nueva partida.

**Consejo:** Haz backup de `game_save.json` regularmente.

### Los colores no se ven bien
En Windows antiguo, los colores ANSI pueden no funcionar. El juego funciona igual, solo sin colores.

---

## 🎯 Roadmap del Juego

### ✅ Implementado (v1.0)
- Sistema de niveles y XP
- Rangos profesionales
- Misiones del Módulo 1, Tema 1 (Estadística)
- Dashboard de stats
- Sistema de logros
- Guardado automático

### 🚧 Próximamente (v1.1)
- Más misiones del Módulo 1
- Sistema de badges visuales
- Ranking online (opcional)
- Modo challenge (contra reloj)
- Easter eggs

### 🔮 Futuro (v2.0)
- Todos los 10 módulos del Master
- Modo multijugador (competir con amigos)
- Certificados al completar módulos
- Integración con GitHub (subir tu código real)

---

## 🤝 Contribuir

Si encuentras bugs o tienes ideas:
1. Documenta el problema
2. Sugiere mejoras
3. Crea nuevas misiones

---

## 📜 Licencia

Este juego es parte del **Master en Ingeniería de Datos con IA**.  
Úsalo libremente para aprender y divertirte.

---

## 🎮 ¡A Jugar!

```bash
python data_engineer_game.py
```

**¡Que disfrutes aprendiendo Data Engineering! 🚀**

---

**Versión:** 1.0  
**Última actualización:** 2025-10-18  
**Creado con:** ❤️ y Python

