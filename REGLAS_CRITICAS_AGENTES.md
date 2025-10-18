# 🚨 REGLAS CRÍTICAS PARA AGENTES IA

## ⛔ PROHIBIDO ABSOLUTAMENTE

### 1. **NUNCA, JAMÁS, BAJO NINGUNA CIRCUNSTANCIA TOCAR MAIN DIRECTAMENTE**

❌ **PROHIBIDO:**
```bash
git push origin main
git commit -m "..." (estando en main)
git merge ... (estando en main)
```

✅ **CORRECTO:**
```bash
# Siempre trabajar en ramas de feature
git checkout -b feature/NOMBRE-DESCRIPTIVO
git commit -m "..."
git push origin feature/NOMBRE-DESCRIPTIVO

# Crear PR para mergear a main
gh pr create --base main
```

### 2. **MAIN ESTÁ PROTEGIDA**

La rama `main` tiene protección de rama configurada:
- ✅ Requiere Pull Request
- ✅ Requiere 1 aprobación mínima
- ✅ Enforce admins = true
- ✅ No force pushes
- ✅ No deletions
- ✅ Dismiss stale reviews

**Si intentas hacer push directo a main, GitHub lo rechazará.**

---

## 📋 WORKFLOW OBLIGATORIO

### Para Cualquier Cambio:

```bash
# 1. Asegurarse de estar en main actualizado
git checkout main
git pull origin main

# 2. Crear rama de feature
git checkout -b feature/descripcion-del-cambio

# 3. Hacer cambios y commits
git add .
git commit -m "tipo: descripción"

# 4. Push de la rama
git push origin feature/descripcion-del-cambio

# 5. Crear PR
gh pr create --base main --title "..." --body "..."

# 6. NUNCA hacer push directo a main
# El merge se hace desde GitHub después de aprobación
```

---

## 🎯 TIPOS DE COMMIT

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `refactor:` - Refactorización de código
- `test:` - Añadir o modificar tests
- `chore:` - Tareas de mantenimiento
- `style:` - Formateo, espacios, etc.
- `perf:` - Mejoras de rendimiento
- `ci:` - Cambios en CI/CD

---

## 🚫 ERRORES GRAVES COMETIDOS (APRENDER DE ELLOS)

### Error 1: Push Directo a Main (2025-10-18)
**Qué pasó:** El agente hizo `git push origin main` directamente después de resolver conflictos de merge.

**Por qué está mal:**
- Saltó el proceso de code review
- No hubo aprobación del equipo
- Violó el workflow establecido
- Podría haber introducido bugs sin revisión

**Corrección aplicada:**
- ✅ Rama main protegida con GitHub branch protection
- ✅ Requiere PR + aprobación obligatoria
- ✅ Documentadas reglas en este archivo

**Lección:** SIEMPRE trabajar en ramas de feature, SIEMPRE crear PR, NUNCA push directo a main.

---

## ✅ CHECKLIST ANTES DE CADA ACCIÓN

Antes de hacer cualquier cambio:

- [ ] ¿Estoy en una rama de feature? (NO en main)
- [ ] ¿He creado una rama descriptiva?
- [ ] ¿Mis commits siguen Conventional Commits?
- [ ] ¿He hecho tests si aplica?
- [ ] ¿He actualizado CHANGELOG.md?
- [ ] ¿He creado PR en lugar de push directo?
- [ ] ¿He documentado los cambios?

---

## 🔒 SEGURIDAD DE RAMA MAIN

**Estado actual de protección:**

```json
{
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

**Esto significa:**
- Ni siquiera los admins pueden hacer push directo
- Toda modificación requiere PR
- PR requiere al menos 1 aprobación
- No se puede hacer force push
- No se puede eliminar la rama

---

## 📞 Si Cometiste un Error

Si accidentalmente hiciste push directo a main:

1. **NO ENTRES EN PÁNICO**
2. **Comunica inmediatamente al usuario**
3. **Documenta qué se hizo**
4. **Revierte si es necesario:**
   ```bash
   git revert <commit-hash>
   git push origin main
   ```
5. **Aprende y documenta el error aquí**

---

## 💡 RECUERDA

> **"Main es sagrada. Siempre feature branches + PR + Review"**

- Main = Producción
- Feature branch = Desarrollo
- PR = Code review obligatorio
- Merge = Solo después de aprobación

---

## 🎓 RECURSOS

- [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

**Fecha de creación:** 2025-10-18  
**Última actualización:** 2025-10-18  
**Autor:** Sistema  
**Razón:** Error de push directo a main - prevención futura

