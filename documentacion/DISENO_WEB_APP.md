# 🌐 Diseño de Aplicación Web - Master Data Engineering

**Fecha:** 2025-11-03
**Versión:** 1.0
**Estado:** Propuesta de diseño

---

## 🎯 Objetivo

Crear una aplicación web completa que integre:
1. **Contenidos del curso** - Visualización navegable de teoría, ejemplos y ejercicios
2. **Juego educativo** - Versión web del juego actual de consola
3. **Sistema de progreso** - Tracking de avance del estudiante
4. **Preparación para freemium** - Arquitectura lista para usuarios Free/Pro

---

## 🏗️ Arquitectura Propuesta

### Stack Tecnológico

#### Backend
- **Framework:** FastAPI (Python 3.13+)
- **Base de datos:** SQLite → PostgreSQL (migración futura)
- **ORM:** SQLAlchemy
- **Autenticación:** JWT (preparado para sistema Free/Pro)
- **API:** RESTful con documentación automática (OpenAPI/Swagger)

#### Frontend
- **Framework:** React 18+ con TypeScript
- **UI Library:** Tailwind CSS + shadcn/ui
- **Routing:** React Router v6
- **State Management:** React Query + Zustand
- **Markdown:** react-markdown con syntax highlighting
- **Build:** Vite

#### Infraestructura
- **Desarrollo:** Docker Compose
- **Producción:** Preparado para deploy en Vercel/Netlify (frontend) + Railway/Render (backend)

---

## 📁 Estructura del Proyecto

```
Curso-Data-Engineering/
├── backend/                           # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point FastAPI
│   │   ├── config.py                 # Configuración
│   │   ├── database.py               # Conexión DB
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # Usuario
│   │   │   ├── progress.py          # Progreso del curso
│   │   │   └── game.py              # Estado del juego
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   └── game.py
│   │   ├── api/                      # Endpoints API
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── content.py       # Contenidos del curso
│   │   │   │   ├── game.py          # Sistema de juego
│   │   │   │   ├── progress.py      # Progreso del usuario
│   │   │   │   └── auth.py          # Autenticación
│   │   ├── services/                 # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── content_service.py   # Parsear markdown, etc.
│   │   │   ├── game_service.py      # Motor del juego
│   │   │   └── progress_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── markdown_parser.py    # Parser de .md
│   ├── tests/
│   ├── alembic/                      # Migraciones DB
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                          # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/               # Componentes React
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── content/
│   │   │   │   ├── ModuleCard.tsx
│   │   │   │   ├── TopicViewer.tsx
│   │   │   │   ├── MarkdownRenderer.tsx
│   │   │   │   ├── CodeBlock.tsx
│   │   │   │   └── ExerciseViewer.tsx
│   │   │   ├── game/
│   │   │   │   ├── GameDashboard.tsx
│   │   │   │   ├── MissionCard.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   ├── AchievementsList.tsx
│   │   │   │   └── StatsDisplay.tsx
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Card.tsx
│   │   │       └── Loading.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── ModulesPage.tsx
│   │   │   ├── TopicPage.tsx
│   │   │   ├── GamePage.tsx
│   │   │   ├── ProfilePage.tsx
│   │   │   └── NotFound.tsx
│   │   ├── hooks/
│   │   │   ├── useContent.ts
│   │   │   ├── useGame.ts
│   │   │   └── useProgress.ts
│   │   ├── services/
│   │   │   └── api.ts                # Cliente API
│   │   ├── store/
│   │   │   ├── gameStore.ts
│   │   │   └── userStore.ts
│   │   ├── types/
│   │   │   ├── content.ts
│   │   │   ├── game.ts
│   │   │   └── user.ts
│   │   ├── utils/
│   │   │   └── formatters.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.web.yml             # Docker para desarrollo web
└── README_WEB_APP.md                  # Documentación
```

---

## 🔌 API Endpoints

### Contenidos del Curso

```
GET    /api/v1/modules                    # Listar todos los módulos
GET    /api/v1/modules/{id}               # Obtener módulo específico
GET    /api/v1/modules/{id}/topics        # Temas de un módulo
GET    /api/v1/topics/{id}                # Obtener tema específico
GET    /api/v1/topics/{id}/content        # Contenido (teoría, ejemplos, ejercicios)
GET    /api/v1/search?q=query             # Buscar en contenidos
```

### Sistema de Juego

```
GET    /api/v1/game/state                 # Estado actual del juego del usuario
POST   /api/v1/game/mission/complete      # Completar misión
GET    /api/v1/game/missions              # Listar misiones disponibles
GET    /api/v1/game/achievements          # Logros del usuario
GET    /api/v1/game/leaderboard           # Tabla de líderes (futuro)
POST   /api/v1/game/xp                    # Añadir XP (después de ejercicio)
```

### Progreso del Usuario

```
GET    /api/v1/progress                   # Progreso general
GET    /api/v1/progress/module/{id}       # Progreso en módulo específico
POST   /api/v1/progress/topic/complete    # Marcar tema como completado
GET    /api/v1/progress/stats             # Estadísticas del usuario
```

### Autenticación (Preparado para Free/Pro)

```
POST   /api/v1/auth/register              # Registro
POST   /api/v1/auth/login                 # Login
POST   /api/v1/auth/refresh               # Refresh token
GET    /api/v1/auth/me                    # Usuario actual
```

---

## 🎮 Interfaz de Usuario

### 1. Página Principal (Home)

```
╔════════════════════════════════════════════════════════════════════╗
║  [Logo] MASTER DATA ENGINEERING          [🎮 Juego] [👤 Usuario]  ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  🚀 Bienvenido al Master en Data Engineering                       ║
║                                                                    ║
║  ┌──────────────────────┐  ┌──────────────────────┐              ║
║  │ 📚 CURSO             │  │ 🎮 JUEGO              │              ║
║  │                      │  │                       │              ║
║  │ 10 Módulos           │  │ Nivel: 5              │              ║
║  │ 40% Completado       │  │ Rango: Junior DE      │              ║
║  │                      │  │ XP: 450/700           │              ║
║  │ [Continuar →]        │  │ [Jugar →]             │              ║
║  └──────────────────────┘  └──────────────────────┘              ║
║                                                                    ║
║  📊 Tu Progreso                                                    ║
║  ████████████░░░░░░░░ 40%                                         ║
║                                                                    ║
║  🎯 Siguiente: Módulo 2 - Tema 2: SQL Intermedio                  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

### 2. Vista de Módulos

```
╔════════════════════════════════════════════════════════════════════╗
║  [← Volver] MÓDULO 2: BASES DE DATOS Y SQL          [🎮] [👤]     ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Sidebar:                    Main Content:                        ║
║  ┌──────────────┐           ┌──────────────────────────────────┐ ║
║  │ 📂 MÓDULOS   │           │ 📚 Temas del Módulo              │ ║
║  │              │           │                                  │ ║
║  │ ✅ Módulo 1  │           │ ┌─────────────────────────────┐  │ ║
║  │ ▶️ Módulo 2  │           │ │ ✅ Tema 1: SQL Básico       │  │ ║
║  │ 🔒 Módulo 3  │           │ │ 96% cobertura               │  │ ║
║  │ 🔒 Módulo 4  │           │ │ [Ver contenido →]           │  │ ║
║  │ ...          │           │ └─────────────────────────────┘  │ ║
║  │              │           │                                  │ ║
║  │ 🎮 Juego     │           │ ┌─────────────────────────────┐  │ ║
║  │ 👤 Perfil    │           │ │ ▶️ Tema 2: SQL Intermedio   │  │ ║
║  │ ⚙️ Config    │           │ │ En progreso                 │  │ ║
║  └──────────────┘           │ │ [Continuar →]               │  │ ║
║                             │ └─────────────────────────────┘  │ ║
║                             │                                  │ ║
║                             │ ┌─────────────────────────────┐  │ ║
║                             │ │ 🔒 Tema 3: Optimización SQL │  │ ║
║                             │ │ Bloqueado                   │  │ ║
║                             │ └─────────────────────────────┘  │ ║
║                             └──────────────────────────────────┘ ║
╚════════════════════════════════════════════════════════════════════╝
```

### 3. Vista de Contenido (Tema)

```
╔════════════════════════════════════════════════════════════════════╗
║  [← Volver] MÓDULO 2 > TEMA 1: SQL BÁSICO          [🎮] [👤]      ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  [📖 Teoría] [💡 Ejemplos] [✍️ Ejercicios] [🛠️ Proyecto]           ║
║  ─────────────────────────────────────────────────────────────     ║
║                                                                    ║
║  # 1. Introducción a SQL                                          ║
║                                                                    ║
║  SQL (Structured Query Language) es el lenguaje estándar...       ║
║                                                                    ║
║  ## 1.1 SELECT Básico                                             ║
║                                                                    ║
║  ```sql                                                            ║
║  SELECT * FROM users;                                             ║
║  ```                                                               ║
║                                                                    ║
║  [Progreso en este tema: ████████░░ 80%]                          ║
║                                                                    ║
║  [← Anterior]              [Siguiente →]                          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

### 4. Vista de Juego

```
╔════════════════════════════════════════════════════════════════════╗
║  DATA ENGINEER: THE GAME                            [👤 jarko]    ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  👤 jarko | 💼 Junior Data Engineer | Nivel 5                     ║
║  XP: [████████████████░░░░░░░░] 450/700                           ║
║  ──────────────────────────────────────────────────────────────   ║
║                                                                    ║
║  [🎮 Misiones] [🏆 Logros] [📊 Stats] [🔧 Tecnologías]             ║
║                                                                    ║
║  🚀 MISIONES DISPONIBLES                                           ║
║  ┌─────────────────────────────────────────────────────┐          ║
║  │ 🎯 Misión 1: Tu Primer Pipeline ETL                │          ║
║  │ Módulo 3 - Tema 1                                  │          ║
║  │ Recompensa: +100 XP                                │          ║
║  │ [Iniciar →]                                        │          ║
║  └─────────────────────────────────────────────────────┘          ║
║                                                                    ║
║  ┌─────────────────────────────────────────────────────┐          ║
║  │ 🔒 Misión 2: Web Scraping Avanzado                 │          ║
║  │ Completa Misión 1 para desbloquear                 │          ║
║  └─────────────────────────────────────────────────────┘          ║
║                                                                    ║
║  📊 TUS ESTADÍSTICAS                                               ║
║  • 📝 Líneas de código: 1,234                                      ║
║  • ✅ Tests pasados: 89                                            ║
║  • 🐛 Bugs corregidos: 12                                          ║
║  • 🎓 Proyectos completados: 4                                     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Flujo de Usuario

### Experiencia del Estudiante

1. **Primera visita:**
   - Landing page atractiva
   - Registro/Login (preparado para Free/Pro)
   - Tutorial interactivo

2. **Navegación del curso:**
   - Dashboard con progreso general
   - Lista de módulos con indicadores (✅ completado, ▶️ en progreso, 🔒 bloqueado)
   - Al hacer click en módulo → Ver temas
   - Al hacer click en tema → Ver contenido (Teoría/Ejemplos/Ejercicios/Proyecto)

3. **Lectura de contenido:**
   - Markdown renderizado con syntax highlighting
   - Navegación secuencial (Anterior/Siguiente)
   - Marcar secciones como leídas
   - Código copiable con un click

4. **Sistema de juego:**
   - Dashboard del juego accesible desde cualquier página
   - Completar misiones al terminar temas
   - Ganar XP automáticamente
   - Ver logros desbloqueados
   - Animaciones de level-up

5. **Progreso:**
   - Barra de progreso global
   - Progreso por módulo
   - Estadísticas detalladas
   - Historial de actividad

---

## 🎨 Diseño Visual

### Paleta de Colores

```css
/* Tema claro (default) */
--primary: #3B82F6      /* Azul */
--secondary: #10B981    /* Verde */
--accent: #F59E0B       /* Ámbar */
--background: #FFFFFF
--surface: #F3F4F6
--text: #111827

/* Tema oscuro (opcional) */
--primary-dark: #60A5FA
--secondary-dark: #34D399
--accent-dark: #FBBF24
--background-dark: #111827
--surface-dark: #1F2937
--text-dark: #F9FAFB
```

### Componentes UI

- Cards con sombras sutiles
- Botones con estados hover/active
- Progress bars animadas
- Badges para indicadores de estado
- Modals para misiones completadas
- Toasts para notificaciones

---

## 🔐 Sistema de Autenticación (Preparado para Free/Pro)

### Estructura

```python
# models/user.py
class User:
    id: int
    email: str
    username: str
    password_hash: str
    tier: str  # 'free' | 'pro'
    created_at: datetime
    last_login: datetime

    # Relaciones
    progress: UserProgress
    game_state: GameState
```

### Niveles de Acceso (Futuro)

- **Free:**
  - Acceso a Módulos 1-3
  - Límite de ejercicios por día
  - Sin certificados

- **Pro:**
  - Acceso completo a todos los módulos
  - Ejercicios ilimitados
  - Certificados al completar
  - Proyectos adicionales
  - Soporte prioritario

---

## 📊 Base de Datos

### Modelos Principales

#### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    tier VARCHAR DEFAULT 'free',
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

#### Game State
```sql
CREATE TABLE game_state (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0,
    total_xp_earned INTEGER DEFAULT 0,
    current_module INTEGER DEFAULT 1,
    current_tema INTEGER DEFAULT 1,
    stats JSONB,
    unlocked_technologies JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Progress
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    module_id INTEGER,
    topic_id INTEGER,
    section VARCHAR,  -- 'theory', 'examples', 'exercises', 'project'
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    time_spent_minutes INTEGER
);
```

#### Achievements
```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    achievement_key VARCHAR,
    unlocked_at TIMESTAMP
);
```

---

## 🚀 Plan de Implementación

### Fase 1: MVP (2-3 semanas) ✅ RECOMENDADO EMPEZAR AQUÍ

1. **Backend básico:**
   - FastAPI setup
   - Database con SQLite
   - Endpoints para contenidos (GET modules, topics)
   - Endpoint para estado del juego

2. **Frontend básico:**
   - React setup con Vite
   - Componentes de layout (Header, Sidebar)
   - Página de módulos
   - Visor de contenido markdown
   - Dashboard del juego (solo visualización)

3. **Integración:**
   - Conectar frontend con backend
   - Parsear archivos .md existentes
   - Mostrar progreso básico

### Fase 2: Juego Funcional (1-2 semanas)

1. Migrar lógica del juego Python a backend
2. Endpoints de juego funcionales
3. Sistema de misiones
4. Sistema de XP y logros
5. Animaciones de level-up

### Fase 3: Autenticación y Progreso (1 semana)

1. Sistema de login/registro
2. JWT tokens
3. Guardar progreso por usuario
4. Dashboard de usuario

### Fase 4: Mejoras UX (1 semana)

1. Búsqueda de contenidos
2. Modo oscuro
3. Responsive design
4. Optimizaciones de rendimiento

### Fase 5: Preparación Free/Pro (1 semana)

1. Sistema de tiers
2. Limitaciones para usuarios free
3. Página de upgrade
4. Analytics básicos

---

## 🧪 Testing

- **Backend:** pytest con cobertura >80%
- **Frontend:** Vitest + React Testing Library
- **E2E:** Playwright (opcional)
- **API:** Postman collections

---

## 📦 Deploy

### Desarrollo
```bash
docker-compose -f docker-compose.web.yml up
```

### Producción (Sugerencia)
- **Frontend:** Vercel/Netlify (gratis, auto-deploy)
- **Backend:** Railway/Render (gratis tier disponible)
- **DB:** Railway PostgreSQL (gratis tier)

---

## 🎯 Próximos Pasos

1. **Revisar este diseño** - ¿Te gusta la propuesta?
2. **Ajustar si necesario** - ¿Cambiarías algo?
3. **Empezar Fase 1 MVP** - Crear estructura básica
4. **Iteración rápida** - Ver resultado pronto y ajustar

---

## ❓ Preguntas para Decidir

1. **¿Prefieres empezar con el MVP minimalista o quieres toda la funcionalidad de una vez?**
2. **¿React está bien o prefieres otro framework (Vue, Svelte)?**
3. **¿Quieres autenticación desde el inicio o lo dejamos para después?**
4. **¿Tienes preferencias de diseño visual (ejemplos de webs que te gusten)?**

---

**¿Aprobamos este diseño y empezamos con la Fase 1?** 🚀
