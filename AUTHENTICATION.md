# 🔐 Sistema de Autenticación - Master Data Engineering

**Versión:** 2.0 (Fase 2 completada)
**Fecha:** 2025-11-03

---

## 🎯 Descripción

Sistema completo de autenticación JWT que protege todas las rutas de la aplicación y permite a cada usuario tener su propio progreso y estado de juego aislado.

---

## ✨ Características

### Backend
- ✅ Registro de usuarios con validación
- ✅ Login con email y contraseña
- ✅ Tokens JWT seguros
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Middleware de autenticación
- ✅ Rutas protegidas
- ✅ Sistema de tiers (Free/Pro)
- ✅ Relación User ↔ GameState (one-to-one)

### Frontend
- ✅ Páginas de Login y Registro
- ✅ AuthContext global
- ✅ Rutas protegidas con ProtectedRoute
- ✅ Token almacenado en localStorage
- ✅ Interceptors automáticos para añadir token
- ✅ Logout funcional
- ✅ Redirect automático a /login si no autenticado

---

## 🔌 API Endpoints

### Autenticación

#### Registrar Usuario
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "usuario@email.com",
  "username": "usuario123",
  "password": "contraseña123",
  "full_name": "Nombre Completo" // Opcional
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "email": "usuario@email.com",
  "username": "usuario123",
  "full_name": "Nombre Completo",
  "is_active": true,
  "is_verified": false,
  "tier": "free",
  "created_at": "2025-11-03T10:00:00Z",
  "last_login": null
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "usuario@email.com",
  "password": "contraseña123"
}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Obtener Usuario Actual
```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@email.com",
  "username": "usuario123",
  "full_name": "Nombre Completo",
  "is_active": true,
  "is_verified": false,
  "tier": "free",
  "created_at": "2025-11-03T10:00:00Z",
  "last_login": "2025-11-03T10:05:00Z"
}
```

#### Refrescar Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer {token}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 🔒 Rutas Protegidas

Todas las siguientes rutas **requieren autenticación** (token JWT en header):

### Contenido
- `GET /api/v1/modules`
- `GET /api/v1/modules/{id}`
- `GET /api/v1/content/{module_id}/{topic_id}/{section}`

### Juego
- `GET /api/v1/game/state`
- `GET /api/v1/game/missions`
- `GET /api/v1/game/achievements`
- `POST /api/v1/game/mission/{id}/complete`
- `POST /api/v1/game/xp`

### Progreso
- `GET /api/v1/progress`

---

## 💻 Uso en el Frontend

### Registro de Usuario

```tsx
import { useAuth } from '@/context/AuthContext'

function RegisterForm() {
  const { register } = useAuth()

  const handleSubmit = async (e) => {
    await register({
      email: 'user@email.com',
      username: 'username',
      password: 'password123',
      full_name: 'Full Name'
    })
    // Usuario registrado y logeado automáticamente
    // Redirige a /
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Login

```tsx
import { useAuth } from '@/context/AuthContext'

function LoginForm() {
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    await login({
      email: 'user@email.com',
      password: 'password123'
    })
    // Usuario logeado, token guardado en localStorage
    // Redirige a /
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Obtener Usuario Actual

```tsx
import { useAuth } from '@/context/AuthContext'

function UserProfile() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) return <div>No autenticado</div>

  return (
    <div>
      <p>Email: {user.email}</p>
      <p>Username: {user.username}</p>
      <p>Tier: {user.tier}</p>
    </div>
  )
}
```

### Logout

```tsx
import { useAuth } from '@/context/AuthContext'

function LogoutButton() {
  const { logout } = useAuth()

  return (
    <button onClick={logout}>
      Cerrar Sesión
    </button>
  )
}
```

### Proteger Rutas

```tsx
import ProtectedRoute from '@/components/common/ProtectedRoute'

// En App.tsx
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <DashboardPage />
    </ProtectedRoute>
  }
/>
```

---

## 🔐 Seguridad

### Backend

1. **Contraseñas hasheadas** con bcrypt (12 rounds)
   - Nunca se almacenan contraseñas en texto plano
   - Hash verificado en cada login

2. **JWT Tokens**
   - Firmados con HS256
   - Incluyen user_id y email
   - Expiración configurable (default: 30 minutos)
   - Secret key debe cambiarse en producción

3. **Validación de inputs**
   - Email válido requerido
   - Username: 3-50 caracteres
   - Password: mínimo 6 caracteres
   - Verificación de emails/usernames duplicados

4. **SQL Injection Prevention**
   - Uso de SQLAlchemy ORM
   - Queries parametrizadas

5. **CORS configurado**
   - Solo permite orígenes específicos
   - Credenciales habilitadas

### Frontend

1. **Token Storage**
   - Almacenado en localStorage
   - Enviado automáticamente en cada request (via interceptor)
   - Eliminado al hacer logout

2. **Interceptors**
   - Añade token a todas las peticiones
   - Redirect automático a /login en 401

3. **Route Guards**
   - Componente `ProtectedRoute`
   - Verifica autenticación antes de renderizar
   - Loading state mientras verifica

---

## 🗄️ Modelo de Datos

### User

```python
class User:
    id: int                    # Primary key
    email: str                 # Unique, required
    username: str              # Unique, required
    password_hash: str         # Bcrypt hash
    full_name: str | None      # Optional
    is_active: bool            # Default: True
    is_verified: bool          # Default: False
    tier: str                  # 'free' | 'pro'
    created_at: datetime
    last_login: datetime | None
```

### GameState (relación con User)

```python
class GameState:
    id: int
    user_id: int              # Foreign key → users.id (unique)
    # ... resto de campos del juego
```

**Relación:** One-to-One (un usuario tiene un único estado de juego)

---

## 🧪 Testing

### Probar Registro

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@email.com",
    "username": "testuser",
    "password": "test123"
  }'
```

### Probar Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@email.com",
    "password": "test123"
  }'

# Guarda el access_token de la respuesta
```

### Probar Ruta Protegida

```bash
# Usar el token del login anterior
curl -X GET http://localhost:8000/api/v1/game/state \
  -H "Authorization: Bearer {TU_TOKEN_AQUI}"
```

---

## ⚙️ Configuración

### Variables de Entorno (Backend)

```env
# Security
SECRET_KEY="your-secret-key-here-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

**⚠️ IMPORTANTE:** Cambia el `SECRET_KEY` en producción:

```python
# Generar secret key segura:
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🚀 Flujo Completo

### Primera Vez (Registro)

1. Usuario va a `/register`
2. Completa formulario de registro
3. Frontend → `POST /api/v1/auth/register`
4. Backend crea usuario con contraseña hasheada
5. Frontend automáticamente hace login
6. Frontend → `POST /api/v1/auth/login`
7. Backend devuelve JWT token
8. Token guardado en localStorage
9. Redirect a `/` (HomePage)
10. Todas las peticiones incluyen token automáticamente

### Login Posterior

1. Usuario va a `/login`
2. Ingresa email y contraseña
3. Frontend → `POST /api/v1/auth/login`
4. Backend valida y devuelve JWT token
5. Token guardado en localStorage
6. Redirect a `/`

### Sesión Activa

1. Al cargar la app, AuthContext busca token en localStorage
2. Si existe token → fetch user info desde `/api/v1/auth/me`
3. Si token válido → usuario autenticado
4. Si token inválido → eliminado de localStorage
5. Todas las rutas protegidas accesibles
6. Interceptor añade token a cada request

### Logout

1. Usuario click en botón logout
2. Token eliminado de localStorage
3. Estado de user limpiado
4. Redirect a `/login`

---

## 🐛 Troubleshooting

### "Invalid authentication credentials"
- Token expirado → hacer login nuevamente
- Token inválido → verificar que el SECRET_KEY sea correcto

### "Email already registered"
- El email ya existe en la base de datos
- Usar otro email o hacer login

### "Username already taken"
- El username ya existe
- Elegir otro username

### 401 en todas las requests
- Token no se está enviando correctamente
- Verificar que el interceptor esté configurado
- Verificar que el token esté en localStorage

### CORS errors
- Verificar que el origen del frontend esté en `CORS_ORIGINS`
- Por defecto: `["http://localhost:5173", "http://localhost:3000"]`

---

## 📊 Diferencias con MVP (Fase 1)

| Aspecto | Fase 1 (MVP) | Fase 2 (Auth) |
|---------|--------------|---------------|
| **Usuarios** | Un solo usuario global | Múltiples usuarios con cuentas |
| **Autenticación** | No requerida | JWT requerido en todas las rutas |
| **GameState** | Compartido | Aislado por usuario |
| **Seguridad** | Sin protección | Contraseñas hasheadas, tokens seguros |
| **Rutas** | Todas públicas | Protegidas con middleware |
| **Frontend** | Sin login | Login/Register obligatorio |

---

## 🔜 Próximos Pasos (Fase 3)

- [ ] Sistema de roles (admin, user)
- [ ] Verificación de email
- [ ] Reset de contraseña
- [ ] OAuth (Google, GitHub)
- [ ] Rate limiting por usuario
- [ ] Logs de actividad por usuario
- [ ] Sesiones múltiples por usuario
- [ ] Blacklist de tokens

---

## 📝 Notas de Desarrollo

### Crear nuevo usuario manualmente

```python
from app.models.user import User
from app.utils.password import hash_password
from app.database import SessionLocal

db = SessionLocal()
user = User(
    email="admin@example.com",
    username="admin",
    password_hash=hash_password("admin123"),
    tier="pro",
    is_verified=True
)
db.add(user)
db.commit()
```

### Verificar token JWT

```python
from app.utils.jwt import verify_token

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = verify_token(token)
print(payload)  # {'sub': '1', 'email': 'user@example.com', 'exp': ...}
```

---

**Última actualización:** 2025-11-03
**Versión:** 2.0 (Fase 2 completada)

**Sistema de autenticación completo y funcional! 🎉🔐**
