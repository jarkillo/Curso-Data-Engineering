# Configuración de Cursor para el Proyecto

Este directorio contiene configuración personalizada y comandos especiales para Cursor AI.

## 📁 Estructura

```
.cursor/
├── commands/              # Comandos personalizados
│   ├── revisar-arquitectura.mjs
│   ├── aplicar-reorganizacion.mjs
│   └── README.md
└── README.md             # Este archivo
```

## 🎯 Propósito

La carpeta `.cursor/` almacena herramientas y configuraciones específicas para mejorar el flujo de trabajo con Cursor AI:

### 1. **Comandos Personalizados** (`commands/`)

Herramientas ejecutables que ayudan a mantener la calidad y estructura del proyecto:

- **`revisar-arquitectura.mjs`**: Analiza la estructura del proyecto e identifica problemas de organización
- **`aplicar-reorganizacion.mjs`**: Aplica automáticamente las correcciones sugeridas

Ver detalles en [commands/README.md](commands/README.md)

### 2. **Configuraciones Futuras**

Esta carpeta puede expandirse con:
- Templates de código
- Snippets personalizados
- Reglas de linting específicas del proyecto
- Scripts de generación de código
- Hooks pre-commit personalizados

## 🚀 Uso Rápido

### Revisar estructura del proyecto
```bash
node .cursor/commands/revisar-arquitectura.mjs
```

### Reorganizar archivos (simulación)
```bash
node .cursor/commands/aplicar-reorganizacion.mjs --dry-run
```

### Reorganizar archivos (real)
```bash
node .cursor/commands/aplicar-reorganizacion.mjs
```

## 📋 Buenas Prácticas

### Para Agentes IA

1. **Antes de crear archivos**: Verificar con `revisar-arquitectura` dónde deben ir
2. **Documentación**: Siempre en `documentacion/` con subcarpetas adecuadas
3. **Scripts**: Siempre en `scripts/`
4. **Código fuente**: Siempre en `src/` o carpetas de módulos
5. **Tests**: Siempre en `tests/`
6. **Archivos temporales**: Evitar dejarlos en la raíz

### Archivos Permitidos en Raíz

Solo estos archivos deben estar en la raíz del proyecto:
- `README.md` - Documentación principal
- `requirements.txt` - Dependencias Python
- `docker-compose.yml` - Configuración Docker
- `.gitignore` - Archivos ignorados por Git
- `.cursorignore` - Archivos ignorados por Cursor
- `ORDEN_DE_IMPLEMENTACION.md` - Gestión del proyecto
- `game_save.json` - Guardado del juego (temporal)

### Estructura de Documentación

```
documentacion/
├── jira/                 # Tickets de Jira (JAR-*)
├── reportes/            # Reportes de calidad y revisiones
├── guias/               # Guías de instalación y uso
├── pull_requests/       # Documentación de PRs
└── juego/              # Archivos del juego educativo
```

## 🔧 Mantenimiento

### Actualizar Reglas de Arquitectura

Para modificar qué archivos van dónde, editar los archivos en `commands/`:
- `revisar-arquitectura.mjs`: Actualizar `ESTRUCTURA_ESPERADA`
- `aplicar-reorganizacion.mjs`: Actualizar `REORGANIZACION`

### Añadir Nuevos Comandos

1. Crear el archivo `.mjs` con el código
2. Crear el archivo `.json` con metadatos (opcional)
3. Documentar en `commands/README.md`
4. Actualizar este README con el nuevo comando

## 📚 Documentación Relacionada

- [Comandos Personalizados](commands/README.md)
- [Guía de Instalación](../documentacion/GUIA_INSTALACION.md)
- [CHANGELOG](../documentacion/CHANGELOG.md)
- [README Principal](../README.md)

## 🤝 Contribuir

Al agregar nuevas herramientas a `.cursor/`:

1. **Mantener consistencia**: Seguir el estilo de los comandos existentes
2. **Documentar bien**: Cada comando debe tener su sección en el README
3. **Agregar ejemplos**: Los usuarios deben poder usar los comandos sin leer código
4. **Actualizar CHANGELOG**: Documentar cambios significativos

## 🔍 Control de Versiones

Esta carpeta **SÍ** debe estar en Git porque contiene herramientas útiles para todos los colaboradores.

Los archivos que **NO** deben estar en Git:
- Configuraciones personales de Cursor
- Archivos de cache
- Archivos temporales generados por comandos

## 💡 Tips para Agentes IA

Si eres un agente IA trabajando en este proyecto:

1. **Ejecuta `revisar-arquitectura`** antes de crear múltiples archivos
2. **Usa `aplicar-reorganizacion --dry-run`** para ver cambios antes de aplicarlos
3. **Respeta la estructura**: No dejes archivos en la raíz sin justificación
4. **Documenta cambios**: Actualiza el CHANGELOG cuando creas nuevos comandos
5. **Pregunta al usuario**: Si no estás seguro dónde va un archivo, consulta

## 📞 Soporte

Para preguntas sobre los comandos de Cursor:
1. Lee este README y el de `commands/`
2. Ejecuta los comandos con `--help`
3. Revisa el código fuente (está bien comentado)
4. Consulta el CHANGELOG para cambios recientes

---

**Última actualización**: 2025-10-18
**Versión**: 1.0.0
**Mantenedor**: Equipo del Master en Ingeniería de Datos

