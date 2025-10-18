# 📋 Guía de Comandos de Arquitectura

## ¿Qué problema resuelven estos comandos?

Con agentes de IA trabajando en el proyecto, es común que se generen muchos archivos de documentación en la raíz del proyecto, perdiendo la estructura organizada. Estos comandos te ayudan a:

1. ✅ **Detectar** archivos mal ubicados
2. ✅ **Reorganizar** automáticamente la estructura
3. ✅ **Mantener** una arquitectura limpia y fácil de navegar

## 🚀 Uso Rápido

### Paso 1: Revisar qué está mal

```bash
node .cursor/commands/revisar-arquitectura.mjs
```

Este comando te mostrará:
- 🔴 **Problemas críticos**: Archivos que definitivamente están mal ubicados
- ⚠️ **Advertencias**: Archivos que deberías revisar
- 💡 **Sugerencias**: Comandos para reorganizar

### Paso 2: Ver qué se movería (simulación)

```bash
node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
```

Esto muestra exactamente qué archivos se moverían y adónde, **sin mover nada realmente**.

### Paso 3: Aplicar la reorganización

```bash
node .cursor/commands/aplicar-reorganizacion.mjs
```

Este comando **mueve los archivos** a sus ubicaciones correctas.

### Paso 4: Verificar que quedó bien

```bash
node .cursor/commands/revisar-arquitectura.mjs
```

Si todo está bien, deberías ver: ✅ **¡La arquitectura del proyecto está limpia!**

## 📁 Estructura Recomendada

```
proyecto/
├── README.md                    # 📖 Documentación principal
├── requirements.txt             # 📦 Dependencias Python
├── docker-compose.yml          # 🐳 Configuración Docker
│
├── documentacion/              # 📚 TODA LA DOCUMENTACIÓN
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── jira/                   # Tickets de Jira (JAR-200, etc.)
│   ├── reportes/              # Reportes de calidad
│   ├── guias/                 # Guías de instalación
│   ├── pull_requests/         # Documentación de PRs
│   └── juego/                 # Archivos del juego educativo
│
├── src/                       # 🔧 Código fuente
├── tests/                     # ✅ Tests
├── scripts/                   # 🚀 Scripts de automatización
├── airflow/                   # Configuración Airflow
└── data/                      # 💾 Datos (si aplica)
```

## 🎯 Principios de Organización

1. **Raíz limpia**: Solo archivos esenciales de configuración
2. **Documentación agrupada**: Fácil de encontrar y mantener
3. **Código separado**: `src/` para código, `tests/` para pruebas
4. **Scripts organizados**: Herramientas en un solo lugar
5. **Sin archivos temporales**: Mantener limpio el repositorio

## 📋 Qué detectan los comandos

### ✅ Archivos permitidos en raíz
- `README.md`
- `requirements.txt`
- `docker-compose.yml`
- `.gitignore`, `.cursorignore`
- `ORDEN_DE_IMPLEMENTACION.md`
- `game_save.json` (guardado del juego)

### 📚 Documentación → `documentacion/`
- `CHANGELOG.md`
- `GUIA_*.md`
- `REPORTE_*.md`
- `*_JAR-*.md` (tickets de Jira)
- `CHECKLIST_*.md`
- `INSTRUCCIONES_*.md`
- `PR_*.md`
- `*.pdf`

**Con subcarpetas:**
- `jira/` → Tickets (`JAR-200.md`, etc.)
- `reportes/` → Reportes de calidad
- `guias/` → Guías de instalación
- `pull_requests/` → Documentación de PRs

### 🚀 Scripts → `scripts/`
- `*.sh` (Linux/Mac)
- `*.ps1` (PowerShell)
- `*.bat` (Windows)

### 🎮 Juego → `documentacion/juego/`
- `README_JUEGO*.md`
- `game.html`
- `data_engineer_game.py`
- `EMPRESAS_FICTICIAS.md`

## 💡 Casos de Uso

### Para desarrolladores

```bash
# Antes de hacer commit, verificar estructura
node .cursor/commands/revisar-arquitectura.mjs

# Si hay problemas, reorganizar
node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
node .cursor/commands/aplicar-reorganizacion.mjs

# Commit los cambios
git add -A
git commit -m "refactor: reorganizar estructura del proyecto"
```

### Para agentes IA

Antes de crear múltiples archivos de documentación:

```bash
# Verificar dónde deben ir los archivos
node .cursor/commands/revisar-arquitectura.mjs

# Crear archivos en la ubicación correcta desde el inicio
```

### Durante code review

```bash
# Verificar que el PR mantiene la estructura
node .cursor/commands/revisar-arquitectura.mjs

# Si no, sugerir reorganización antes de mergear
```

## ⚙️ Opciones de los Comandos

### revisar-arquitectura.mjs
```bash
node .cursor/commands/revisar-arquitectura.mjs
```
No tiene opciones, simplemente analiza y reporta.

### aplicar-reorganizacion.mjs
```bash
# Ver ayuda
node .cursor/commands/aplicar-reorganizacion.mjs --help

# Simulación (no mueve archivos)
node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
node .cursor/commands/aplicar-reorganizacion.mjs -d

# Aplicar cambios reales
node .cursor/commands/aplicar-reorganizacion.mjs
```

## 🔐 Seguridad y Reversión

### Antes de reorganizar
1. ✅ Haz commit de cambios actuales
2. ✅ Usa `--dry-run` primero
3. ✅ Verifica que los destinos son correctos

### Si algo sale mal
```bash
# Revertir cambios con git
git checkout .

# O revertir el último commit
git reset --hard HEAD~1
```

## 📝 Ejemplos Reales

### Ejemplo 1: Proyecto nuevo con agentes
```bash
# Después de que los agentes crean varios archivos
$ node .cursor/commands/revisar-arquitectura.mjs

🔴 PROBLEMAS CRÍTICOS:
  • REPORTE_CALIDAD_JAR-200.md → debería estar en documentacion/
  • CHECKLIST_JAR-200.md → debería estar en documentacion/

⚠️ ADVERTENCIAS:
  • claude.md → archivo temporal

# Simular reorganización
$ node .cursor/commands/aplicar-reorganizacion.mjs --dry-run

📋 PLAN DE REORGANIZACIÓN:
DOCUMENTACION (8 archivos):
  • REPORTE_CALIDAD_JAR-200.md → documentacion/jira/
  • CHECKLIST_JAR-200.md → documentacion/jira/
  ...

# Aplicar
$ node .cursor/commands/aplicar-reorganizacion.mjs

✅ Reorganización completada con éxito!

# Verificar
$ node .cursor/commands/revisar-arquitectura.mjs

✅ ¡La arquitectura del proyecto está limpia!
```

### Ejemplo 2: Mantenimiento periódico
```bash
# Revisar cada semana
node .cursor/commands/revisar-arquitectura.mjs

# Si aparecen problemas, corregir
node .cursor/commands/aplicar-reorganizacion.mjs
```

## 🔄 Integración con Git Hooks

Puedes añadir esto a tu `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Verificar arquitectura antes de commit
node .cursor/commands/revisar-arquitectura.mjs

# Si hay errores, sugerir reorganización
if [ $? -ne 0 ]; then
  echo "⚠️  Hay problemas de arquitectura."
  echo "Ejecuta: node .cursor/commands/aplicar-reorganizacion.mjs"
  exit 1
fi
```

## 🚨 Troubleshooting

### "Cannot find module"
```bash
# Asegúrate de estar en la raíz del proyecto
cd "E:\Curso Data Engineering"
node .cursor/commands/revisar-arquitectura.mjs
```

### "Permission denied"
```bash
# En Linux/Mac, dar permisos de ejecución
chmod +x .cursor/commands/*.mjs
```

### Archivos no detectados
Verifica que el patrón esté en la configuración:
- Edita `revisar-arquitectura.mjs` → `ESTRUCTURA_ESPERADA`
- Edita `aplicar-reorganizacion.mjs` → `REORGANIZACION`

## 📚 Más Información

- [Documentación completa de comandos](.cursor/commands/README.md)
- [Configuración de Cursor](.cursor/README.md)
- [CHANGELOG](documentacion/CHANGELOG.md)

## 🎓 Tips y Mejores Prácticas

### Para equipos
1. Ejecutar `revisar-arquitectura` semanalmente
2. Incluir en el checklist de PR
3. Documentar excepciones si las hay

### Para proyectos nuevos
1. Configurar estructura desde el inicio
2. Entrenar a agentes IA sobre la estructura
3. Revisar después de cada sesión de IA

### Para proyectos grandes
1. Personalizar patrones en los comandos
2. Crear subcarpetas adicionales si es necesario
3. Documentar la estructura en el README

## ✅ Checklist de Uso

- [ ] He leído esta guía
- [ ] He ejecutado `revisar-arquitectura` para ver el estado actual
- [ ] He probado `aplicar-reorganizacion --dry-run` para simular
- [ ] He aplicado la reorganización con `aplicar-reorganizacion`
- [ ] He verificado que todo quedó bien con `revisar-arquitectura`
- [ ] He hecho commit de los cambios

---

**¿Dudas o problemas?** Revisa [.cursor/commands/README.md](.cursor/commands/README.md) o consulta el código fuente de los comandos (están bien documentados).

