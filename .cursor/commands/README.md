# Comandos Personalizados de Cursor

Este directorio contiene comandos personalizados para facilitar la gestión y mantenimiento del proyecto.

## 📋 Revisar Arquitectura

### Descripción
Comando que analiza la estructura del proyecto y detecta problemas de organización como:
- Archivos de documentación en la raíz que deberían estar en `documentacion/`
- Scripts mal ubicados que deberían estar en `scripts/`
- Archivos temporales que deberían limpiarse
- Archivos no clasificados que necesitan revisión

### Uso

#### Desde la línea de comandos:
```bash
node .cursor/commands/revisar-arquitectura.mjs
```

#### Desde Cursor:
1. Abrir el Command Palette (Ctrl+Shift+P)
2. Buscar "Revisar Arquitectura"
3. Ejecutar el comando

#### Atajo de teclado:
```
Ctrl+Alt+A
```

### Qué detecta

#### 🔴 Problemas críticos:
- Archivos `.md` relacionados con documentación en la raíz
- Scripts (`.sh`, `.ps1`, `.bat`) en la raíz
- Archivos de tickets de Jira (`*_JAR-*.md`) fuera de documentación
- Reportes (`REPORTE_*.md`) fuera de documentación

#### ⚠️ Advertencias:
- Archivos temporales (`game_save.json`, `claude.md`, etc.)
- Archivos no clasificados que podrían necesitar ubicación específica

#### 💡 Sugerencias:
- Comandos específicos para reorganizar archivos
- Recomendaciones de estructura de carpetas
- Mejoras de .gitignore y .cursorignore

### Estructura recomendada

El comando sugiere la siguiente estructura:

```
proyecto/
├── README.md
├── requirements.txt
├── docker-compose.yml
│
├── documentacion/
│   ├── jira/              # Tickets
│   ├── reportes/          # Reportes de calidad
│   └── guias/             # Guías
│
├── src/                   # Código fuente
├── tests/                 # Tests
├── scripts/               # Scripts de setup
├── airflow/               # Configuración Airflow
└── data/                  # Datos (si aplica)
```

### Principios de organización

1. **Raíz limpia**: Solo archivos esenciales de configuración
2. **Documentación agrupada**: Fácil de encontrar y mantener
3. **Código separado**: `src/` para código, `tests/` para pruebas
4. **Scripts organizados**: Herramientas en un solo lugar
5. **Sin archivos temporales**: Mantener limpio el repositorio

### Cuándo usar este comando

- **Antes de hacer commits**: Verificar que no se están agregando archivos en lugares incorrectos
- **Durante code reviews**: Validar que la estructura es correcta
- **Al recibir cambios de otros**: Revisar si mantienen la organización
- **Periódicamente**: Como parte del mantenimiento del proyecto

### Personalización

Para personalizar qué archivos se consideran en cada categoría, editar el objeto `ESTRUCTURA_ESPERADA` en el archivo `revisar-arquitectura.mjs`:

```javascript
const ESTRUCTURA_ESPERADA = {
  raiz: {
    permitidos: [...],
    carpetas_obligatorias: [...]
  },
  documentacion: {
    patrones: [...]
  },
  // ...
};
```

### Salida del comando

El comando genera un reporte con:
- Lista de problemas críticos (en rojo)
- Lista de advertencias (en amarillo)
- Sugerencias de mejora con comandos específicos (en azul)
- Resumen numérico de problemas encontrados
- Estructura recomendada del proyecto

### Integración con CI/CD

Este comando puede integrarse en pipelines de CI/CD para validar la estructura antes de mergear:

```yaml
# .github/workflows/validate-structure.yml
name: Validar Estructura
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Revisar Arquitectura
        run: node .cursor/commands/revisar-arquitectura.mjs
```

## 🔄 Aplicar Reorganización

### Descripción
Comando que aplica automáticamente la reorganización sugerida por el revisor de arquitectura. Mueve archivos a sus ubicaciones correctas y crea las subcarpetas necesarias.

### Uso

#### Modo Dry-Run (recomendado primero):
```bash
node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
```

#### Aplicar reorganización:
```bash
node .cursor/commands/aplicar-reorganizacion.mjs
```

#### Ver ayuda:
```bash
node .cursor/commands/aplicar-reorganizacion.mjs --help
```

### Qué hace

1. **Analiza** archivos en la raíz
2. **Clasifica** según reglas de arquitectura
3. **Crea** directorios necesarios
4. **Mueve** archivos a ubicaciones correctas
5. **Reporta** resumen de operaciones

### Categorías y destinos

#### 📚 Documentación → `documentacion/`
Con subcarpetas organizadas:
- **jira/**: Tickets (`*_JAR-*.md`, `CHECKLIST_JAR-*.md`)
- **reportes/**: Reportes (`REPORTE_*.md`, `REVISION_*.md`)
- **guias/**: Guías (`GUIA_*.md`, `ENV_EXAMPLE.md`)
- **pull_requests/**: PRs (`PR_*.md`, `COMMIT_MESSAGE_*.md`)

#### 🚀 Scripts → `scripts/`
- Todos los scripts de shell (`.sh`, `.ps1`, `.bat`)

#### 🎮 Juego → `documentacion/juego/`
- `README_JUEGO*.md`
- `game.html`
- `data_engineer_game.py`
- `EMPRESAS_FICTICIAS.md`

### Archivos que NO se mueven

Estos archivos se mantienen en la raíz:
- `README.md`
- `requirements.txt`
- `docker-compose.yml`
- `.gitignore`, `.cursorignore`
- `ORDEN_DE_IMPLEMENTACION.md`
- `game_save.json` (guardado del juego)

### Flujo recomendado

1. **Revisar** qué hay mal:
   ```bash
   node .cursor/commands/revisar-arquitectura.mjs
   ```

2. **Simular** reorganización:
   ```bash
   node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
   ```

3. **Aplicar** si todo se ve bien:
   ```bash
   node .cursor/commands/aplicar-reorganizacion.mjs
   ```

4. **Verificar** que quedó bien:
   ```bash
   node .cursor/commands/revisar-arquitectura.mjs
   ```

5. **Commit** los cambios:
   ```bash
   git add -A
   git commit -m "refactor: reorganizar estructura del proyecto"
   ```

### Seguridad

- **Modo Dry-Run**: Siempre úsalo primero para ver qué se movería
- **Sin confirmación**: El comando mueve archivos directamente (por eso el dry-run es importante)
- **Respaldo**: Considera hacer backup o commit antes de ejecutar
- **Rollback**: Si algo sale mal, puedes revertir con git

### Ejemplo de salida

```
================================================================================
🔄 REORGANIZADOR DE ARQUITECTURA DEL PROYECTO
   [MODO DRY-RUN - No se moverán archivos realmente]
================================================================================

📋 PLAN DE REORGANIZACIÓN:

DOCUMENTACION (10 archivos):
  • CHECKLIST_JAR-200.md → documentacion/jira/
  • REPORTE_CALIDAD_JAR-200.md → documentacion/reportes/
  • GUIA_INSTALACION.md → documentacion/guias/
  ...

📁 Creando directorios necesarios...
  [DRY-RUN] Crearía directorio: documentacion/jira
  [DRY-RUN] Crearía directorio: documentacion/reportes

🚚 Moviendo archivos...
  [DRY-RUN] CHECKLIST_JAR-200.md → documentacion/jira/CHECKLIST_JAR-200.md
  ...

📊 RESUMEN DE REORGANIZACIÓN
  Archivos movidos exitosamente: 15
  Errores: 0

💡 Esto fue una simulación. Para aplicar los cambios, ejecuta sin --dry-run
```

## Crear nuevos comandos

Para crear un nuevo comando:

1. Crear el archivo `.mjs` o `.js` con la lógica del comando
2. Crear el archivo `.json` con los metadatos:
   ```json
   {
     "name": "Nombre del Comando",
     "description": "Descripción breve",
     "command": "node .cursor/commands/mi-comando.mjs",
     "icon": "🔧",
     "category": "development",
     "tags": ["tag1", "tag2"]
   }
   ```
3. Documentar el comando en este README
4. Asegurarse de que el comando sea ejecutable y no tenga dependencias externas

## Mantenimiento

- Revisar y actualizar los comandos regularmente
- Añadir tests si el comando crece en complejidad
- Mantener la documentación actualizada
- Seguir los principios de código limpio del proyecto

