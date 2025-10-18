# 🤖 GUÍA PARA AGENTES IA - WORKFLOW GIT

## 🌳 ESTRUCTURA DE RAMAS

```
main (protegida) ← PRODUCCIÓN - NUNCA TOCAR DIRECTAMENTE
  ↑
  PR (con aprobación)
  ↑
dev ← DESARROLLO - Rama base para trabajo diario
  ↑
  PR (sin aprobación necesaria)
  ↑
feature/nombre ← TRABAJO INDIVIDUAL - Cada tarea nueva
```

---

## ⛔ REGLA DE ORO

### **NUNCA, JAMÁS, BAJO NINGUNA CIRCUNSTANCIA TOCAR MAIN DIRECTAMENTE**

```bash
# ❌ PROHIBIDO ABSOLUTAMENTE
git checkout main
git commit -m "..."
git push origin main

# ✅ CORRECTO - SIEMPRE USAR RAMAS
git checkout dev
git checkout -b feature/mi-tarea
git commit -m "..."
git push origin feature/mi-tarea
```

---

## 📋 WORKFLOW DIARIO (PASO A PASO)

### 1️⃣ Empezar Nueva Tarea

```bash
# Asegurarse de estar en dev actualizado
git checkout dev
git pull origin dev

# Crear rama de feature desde dev
git checkout -b feature/descripcion-clara

# Ejemplos de nombres de rama:
# feature/add-login-endpoint
# feature/JAR-201-user-authentication
# fix/correct-csv-parsing
# docs/update-readme-installation
```

### 2️⃣ Trabajar en la Tarea

```bash
# Hacer cambios en archivos
# ...

# Ver qué cambió
git status
git diff

# Añadir cambios
git add .
# o específicamente
git add archivo1.py archivo2.md

# Commit con mensaje descriptivo
git commit -m "tipo: descripción clara"
```

### 3️⃣ Subir Cambios

```bash
# Push de la rama feature
git push origin feature/descripcion-clara

# Si es el primer push de la rama
git push -u origin feature/descripcion-clara
```

### 4️⃣ Crear Pull Request

```bash
# PR hacia dev (trabajo diario)
gh pr create --base dev --title "Título descriptivo" --body "Descripción detallada"

# PR hacia main (release/producción) - SOLO DESDE DEV
gh pr create --base main --title "Release vX.X.X" --body "Cambios en esta versión"
```

### 5️⃣ Después del Merge

```bash
# Actualizar dev local
git checkout dev
git pull origin dev

# Eliminar rama local mergeada
git branch -d feature/descripcion-clara

# Limpiar referencias remotas
git fetch --prune
```

---

## 🎯 TIPOS DE COMMIT

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Cuándo usar | Ejemplo |
|------|-------------|---------|
| `feat:` | Nueva funcionalidad | `feat: add user login endpoint` |
| `fix:` | Corrección de bug | `fix: correct CSV parsing error` |
| `docs:` | Solo documentación | `docs: update installation guide` |
| `refactor:` | Refactorización | `refactor: simplify authentication logic` |
| `test:` | Añadir/modificar tests | `test: add unit tests for parser` |
| `chore:` | Mantenimiento | `chore: update dependencies` |
| `style:` | Formateo | `style: apply black formatting` |
| `perf:` | Mejora rendimiento | `perf: optimize database queries` |

**Formato completo:**
```
tipo(scope): descripción breve

Descripción más detallada si es necesario.

Fixes #123
```

---

## 🔀 FLUJOS ESPECÍFICOS

### Feature Normal (Día a día)

```bash
dev (actualizado)
  ↓
feature/mi-tarea (crear)
  ↓
commits + tests
  ↓
push origin feature/mi-tarea
  ↓
PR → dev (sin aprobación necesaria)
  ↓
merge automático o manual
  ↓
delete feature/mi-tarea
```

### Release a Producción (Main)

```bash
dev (con todas las features listas)
  ↓
asegurar todos los tests pasan
  ↓
actualizar CHANGELOG.md
  ↓
PR → main (REQUIERE APROBACIÓN)
  ↓
esperar code review
  ↓
merge después de aprobación
  ↓
main se actualiza automáticamente
```

### Hotfix Urgente (Bug en Producción)

```bash
main (actualizado)
  ↓
hotfix/descripcion-bug (crear desde main)
  ↓
fix + tests
  ↓
push origin hotfix/descripcion-bug
  ↓
PR → main (REQUIERE APROBACIÓN)
  ↓
PR → dev (mantener sincronizado)
  ↓
merge en ambas ramas
```

---

## 📊 PROTECCIONES CONFIGURADAS

### Main (Producción)
- ✅ Requiere Pull Request obligatorio
- ✅ Requiere 1 aprobación mínima
- ✅ Enforce admins = true (ni admins pueden push directo)
- ✅ No force pushes
- ✅ No deletions
- ✅ Dismiss stale reviews

### Dev (Desarrollo)
- ✅ Branch existe y es la base para trabajo
- ℹ️ No requiere aprobaciones (más ágil)
- ℹ️ Pero aún así usar PRs para trazabilidad

---

## ✅ CHECKLIST ANTES DE CADA ACCIÓN

Antes de hacer cualquier cambio:

- [ ] ¿Estoy en una rama de feature? (NO en main, NO en dev directamente)
- [ ] ¿Mi rama tiene un nombre descriptivo?
- [ ] ¿He actualizado dev antes de crear mi rama?
- [ ] ¿Mis commits siguen Conventional Commits?
- [ ] ¿He ejecutado tests si aplica?
- [ ] ¿He actualizado documentación relevante?
- [ ] ¿He creado PR en lugar de merge directo?

---

## 🚫 ERRORES COMUNES Y CÓMO EVITARLOS

### Error 1: Push Directo a Main
```bash
# ❌ MAL
git checkout main
git push origin main

# ✅ BIEN
git checkout dev
git checkout -b feature/mi-tarea
git push origin feature/mi-tarea
gh pr create --base dev
```

### Error 2: Trabajar Directamente en Dev
```bash
# ❌ MAL (menos grave pero no ideal)
git checkout dev
git commit -m "..."
git push origin dev

# ✅ BIEN
git checkout dev
git checkout -b feature/mi-tarea
git commit -m "..."
git push origin feature/mi-tarea
gh pr create --base dev
```

### Error 3: No Actualizar Dev Antes de Crear Feature
```bash
# ❌ MAL
git checkout -b feature/mi-tarea  # desde dev desactualizado

# ✅ BIEN
git checkout dev
git pull origin dev
git checkout -b feature/mi-tarea
```

### Error 4: Nombre de Rama Poco Descriptivo
```bash
# ❌ MAL
git checkout -b temp
git checkout -b fix
git checkout -b asdf

# ✅ BIEN
git checkout -b feature/add-user-authentication
git checkout -b fix/csv-parsing-error
git checkout -b docs/update-installation-guide
```

---

## 🔧 COMANDOS ÚTILES

### Ver Estado Actual
```bash
git status                          # Qué cambió
git branch -a                       # Todas las ramas (local + remoto)
git log --oneline -10              # Últimos 10 commits
git diff                           # Diferencias no staged
git diff --staged                  # Diferencias staged
```

### Sincronización
```bash
git fetch origin                   # Obtener cambios sin aplicar
git pull origin dev                # Traer y aplicar cambios de dev
git fetch --prune                  # Limpiar referencias remotas eliminadas
```

### Limpieza
```bash
git branch -d nombre-rama          # Eliminar rama local mergeada
git branch -D nombre-rama          # Forzar eliminación (cuidado)
git stash                          # Guardar cambios temporalmente
git stash pop                      # Recuperar cambios guardados
```

### Deshacer Cambios (Cuidado)
```bash
git restore archivo.py             # Descartar cambios no staged
git restore --staged archivo.py   # Unstage archivo
git reset --soft HEAD~1            # Deshacer último commit (mantener cambios)
git reset --hard HEAD~1            # Deshacer último commit (PELIGRO: perder cambios)
```

---

## 📞 ¿QUÉ HACER SI...?

### ...Hice Commit en la Rama Incorrecta?
```bash
# Si aún no hiciste push
git stash                          # Guardar cambios
git checkout rama-correcta
git stash pop                      # Aplicar cambios
```

### ...Olvidé Actualizar Dev Antes de Crear Feature?
```bash
git checkout dev
git pull origin dev
git checkout feature/mi-rama
git merge dev                      # Traer cambios de dev
```

### ...Necesito Cambios de Otra Rama?
```bash
git checkout mi-rama
git merge otra-rama                # Traer cambios
# o
git cherry-pick <commit-hash>      # Traer commit específico
```

### ...Hay Conflictos en el Merge?
```bash
# Git marcará los conflictos en archivos
# Editar archivos y resolver conflictos manualmente
git add archivo-resuelto.py
git commit -m "merge: resolver conflictos"
```

---

## 🎓 RECURSOS

- [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

---

## 📝 RESUMEN RÁPIDO

```bash
# INICIO DEL DÍA
git checkout dev && git pull origin dev

# NUEVA TAREA
git checkout -b feature/descripcion

# TRABAJO
git add . && git commit -m "feat: descripción"

# SUBIR
git push origin feature/descripcion

# PR
gh pr create --base dev --title "..." --body "..."

# FIN (después del merge)
git checkout dev && git pull origin dev
git branch -d feature/descripcion
git fetch --prune
```

---

**Última actualización:** 2025-10-18  
**Versión:** 1.0.0  
**Autor:** Sistema  
**Razón:** Establecer workflow claro después de error de push directo a main

