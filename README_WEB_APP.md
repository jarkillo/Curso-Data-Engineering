# 🌐 Web App - Master en Data Engineering

Aplicación web completa que integra el contenido del curso con un sistema de juego educativo.

## 🎯 Características

- **📚 Visor de Contenidos**: Navegación intuitiva por módulos, temas y contenidos
- **🎮 Sistema de Juego**: Gamificación con niveles, XP, misiones y logros
- **📊 Dashboard de Progreso**: Tracking visual de tu avance en el curso
- **🎨 UI Moderna**: Interfaz responsive con React + Tailwind CSS
- **⚡ API Rápida**: Backend con FastAPI y documentación automática

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

```bash
# Iniciar todo (backend + frontend)
docker-compose -f docker-compose.web.yml up

# Acceder a la aplicación
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Opción 2: Desarrollo Local

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\Activate.ps1  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Iniciar servidor
uvicorn app.main:app --reload

# API disponible en: http://localhost:8000
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# App disponible en: http://localhost:5173
```

## 📁 Estructura del Proyecto

```
.
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/routes/        # Endpoints API
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   └── main.py            # Entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── pages/             # Páginas
│   │   ├── services/          # Cliente API
│   │   ├── store/             # Zustand stores
│   │   └── types/             # TypeScript types
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.web.yml     # Docker Compose config
```

## 🔌 API Endpoints

### Contenidos

- `GET /api/v1/modules` - Listar todos los módulos
- `GET /api/v1/modules/{id}` - Obtener módulo específico
- `GET /api/v1/content/{module_id}/{topic_id}/{section}` - Obtener contenido

### Juego

- `GET /api/v1/game/state` - Estado del juego del usuario
- `GET /api/v1/game/missions` - Misiones disponibles
- `GET /api/v1/game/achievements` - Logros
- `POST /api/v1/game/mission/{id}/complete` - Completar misión
- `POST /api/v1/game/xp` - Añadir XP

### Progreso

- `GET /api/v1/progress` - Progreso general del usuario

**Documentación completa:** http://localhost:8000/api/docs

## 🎮 Características del Juego

### Sistema de Niveles

- **Niveles**: 1-20+
- **XP por nivel**: Progresivo (100, 250, 450, 700...)
- **Rangos**:
  - 🎓 Trainee (Nivel 0-2)
  - 💼 Junior Data Engineer (Nivel 3-6)
  - 🔧 Data Engineer (Nivel 7-11)
  - ⭐ Senior Data Engineer (Nivel 12-16)
  - 👑 Lead Data Engineer (Nivel 17-19)
  - 🏆 Data Architect (Nivel 20+)

### Misiones

Vinculadas a los temas del curso. Al completar un tema, puedes completar su misión correspondiente y ganar XP.

### Logros

Desbloquea logros especiales al alcanzar hitos:
- 🎯 Primera Misión
- 💼 Nivel 5 alcanzado
- 📚 Módulo completado
- Y más...

### Estadísticas

Tracking de:
- Líneas de código escritas
- Tests pasados
- Bugs corregidos
- Proyectos completados
- Horas de estudio
- Ejercicios resueltos

## 🛠️ Tecnologías

### Backend

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos (PostgreSQL en producción)
- **Python 3.13+**

### Frontend

- **React 18** - Library UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool ultra rápido
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Navegación
- **React Query** - Data fetching
- **Zustand** - State management
- **React Markdown** - Renderizado markdown
- **Syntax Highlighter** - Highlighting de código

## 📊 Base de Datos

### Modelos

- **GameState**: Estado del juego del usuario (nivel, XP, misiones, logros)
- **UserProgress**: Progreso en el curso (temas completados, tiempo)
- **User**: Información del usuario (futuro, para autenticación)

## 🔄 Flujo de Usuario

1. **Inicio**: Dashboard con resumen de progreso y juego
2. **Módulos**: Lista de módulos con estado (completado/en progreso/bloqueado)
3. **Temas**: Dentro de cada módulo, lista de temas
4. **Contenido**: Visor markdown con pestañas (Teoría/Ejemplos/Ejercicios/Proyecto)
5. **Juego**: Dashboard del juego con misiones, logros y stats

## 🎨 Capturas de Pantalla

### Dashboard Principal

```
╔════════════════════════════════════════════════╗
║  📚 CURSO              │  🎮 JUEGO              ║
║  40% Completado        │  Nivel 5 - Junior DE   ║
║  ████████░░░░░░░░      │  450/700 XP            ║
║  [Continuar →]         │  [Jugar →]             ║
╚════════════════════════════════════════════════╝
```

### Visor de Contenido

- Markdown renderizado con syntax highlighting
- Navegación por pestañas (Teoría, Ejemplos, Ejercicios, Proyecto)
- Código copiable con un click

### Dashboard del Juego

- Barra de XP animada
- Lista de misiones con recompensas
- Grid de logros
- Estadísticas del jugador

## 🚧 Desarrollo

### Scripts Útiles

#### Backend

```bash
# Formatear código
black app/ tests/

# Linting
flake8 app/ tests/

# Tests
pytest --cov=app tests/

# Crear migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head
```

#### Frontend

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview build
npm run preview

# Linting
npm run lint
```

## 📝 Variables de Entorno

### Backend (.env)

```env
APP_NAME="Master Data Engineering API"
DEBUG=true
DATABASE_URL="sqlite:///./data_engineering.db"
SECRET_KEY="your-secret-key"
CORS_ORIGINS=["http://localhost:5173"]
CONTENT_BASE_PATH="../"
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🐛 Troubleshooting

### Backend no inicia

- Verificar que Python 3.13+ está instalado
- Verificar que las dependencias están instaladas: `pip install -r requirements.txt`
- Verificar que el archivo .env existe

### Frontend no compila

- Verificar que Node.js 18+ está instalado
- Borrar node_modules y reinstalar: `rm -rf node_modules && npm install`
- Limpiar cache de Vite: `rm -rf .vite`

### API no responde

- Verificar que el backend está corriendo en http://localhost:8000
- Verificar CORS en backend/app/config.py
- Verificar logs del backend

## 📈 Próximas Funcionalidades

### Fase 2: Sistema de Autenticación

- [ ] Login/Registro de usuarios
- [ ] JWT tokens
- [ ] Progreso por usuario
- [ ] Perfil de usuario

### Fase 3: Mejoras UX

- [ ] Búsqueda de contenidos
- [ ] Modo oscuro
- [ ] Responsive mobile
- [ ] Notificaciones toast

### Fase 4: Sistema Free/Pro

- [ ] Tiers de usuarios
- [ ] Contenido premium
- [ ] Certificados
- [ ] Analytics

## 🤝 Contribuir

Este es un proyecto educativo. Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es material educativo de código abierto.

---

**Última actualización:** 2025-11-03
**Versión:** 1.0.0 (MVP)

**¡Bienvenido al Master en Data Engineering! 🚀📊**
