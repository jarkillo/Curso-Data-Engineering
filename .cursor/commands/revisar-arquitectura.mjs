#!/usr/bin/env node

/**
 * Comando para revisar la arquitectura del proyecto
 * Detecta archivos mal ubicados, estructura desorganizada y sugiere mejoras
 */

import { readdir, stat } from 'fs/promises';
import { join } from 'path';

// Configuración de la estructura esperada
const ESTRUCTURA_ESPERADA = {
    raiz: {
        permitidos: [
            'README.md',
            'requirements.txt',
            'docker-compose.yml',
            '.gitignore',
            '.env',
            'pyproject.toml',
            'setup.py',
            'LICENSE'
        ],
        carpetas_obligatorias: [
            'documentacion',
            'src',
            'tests',
            'scripts'
        ]
    },
    documentacion: {
        descripcion: 'Toda la documentación del proyecto',
        patrones: [
            'CHANGELOG.md',
            'GUIA_*.md',
            'PROGRAMA_*.md',
            'PROYECTOS_*.md',
            'RECURSOS.md',
            'RESUMEN_*.md',
            'ENV_EXAMPLE.md',
            '*_JAR-*.md',  // Tickets de Jira
            'REPORTE_*.md',
            'CHECKLIST_*.md',
            'INSTRUCCIONES_*.md',
            'PR_*.md',
            'COMMIT_MESSAGE_*.md',
            '*.pdf'
        ]
    },
    scripts: {
        descripcion: 'Scripts de automatización y setup',
        patrones: ['*.sh', '*.ps1', '*.bat']
    },
    temporal: {
        descripcion: 'Archivos que deberían eliminarse o moverse',
        patrones: [
            'claude.md',
            'game_save.json',
            'game.html',
            '*_JUEGO*.md'
        ]
    }
};

const COLORES = {
    reset: '\x1b[0m',
    rojo: '\x1b[31m',
    verde: '\x1b[32m',
    amarillo: '\x1b[33m',
    azul: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    bold: '\x1b[1m'
};

class RevisorArquitectura {
    constructor() {
        this.problemas = [];
        this.advertencias = [];
        this.sugerencias = [];
        this.archivos_raiz = [];
    }

    log(mensaje, color = '') {
        console.log(`${color}${mensaje}${COLORES.reset}`);
    }

    async obtenerArchivosRaiz() {
        try {
            const items = await readdir('.');
            const archivos = [];

            for (const item of items) {
                const stats = await stat(item);
                if (stats.isFile()) {
                    archivos.push(item);
                }
            }

            return archivos;
        } catch (error) {
            this.problemas.push(`Error al leer directorio raíz: ${error.message}`);
            return [];
        }
    }

    coincidePatron(archivo, patron) {
        const regex = new RegExp('^' + patron.replace(/\*/g, '.*') + '$');
        return regex.test(archivo);
    }

    clasificarArchivo(archivo) {
        // Verificar si está permitido en raíz
        if (ESTRUCTURA_ESPERADA.raiz.permitidos.includes(archivo)) {
            return 'permitido';
        }

        // Verificar si debería estar en documentacion
        for (const patron of ESTRUCTURA_ESPERADA.documentacion.patrones) {
            if (this.coincidePatron(archivo, patron)) {
                return 'documentacion';
            }
        }

        // Verificar si es temporal
        for (const patron of ESTRUCTURA_ESPERADA.temporal.patrones) {
            if (this.coincidePatron(archivo, patron)) {
                return 'temporal';
            }
        }

        // Verificar si es script
        for (const patron of ESTRUCTURA_ESPERADA.scripts.patrones) {
            if (this.coincidePatron(archivo, patron)) {
                return 'scripts';
            }
        }

        return 'desconocido';
    }

    async analizar() {
        this.log('\n' + '='.repeat(80), COLORES.bold + COLORES.cyan);
        this.log('📋 REVISOR DE ARQUITECTURA DEL PROYECTO', COLORES.bold + COLORES.cyan);
        this.log('='.repeat(80) + '\n', COLORES.bold + COLORES.cyan);

        // Obtener archivos en raíz
        this.archivos_raiz = await this.obtenerArchivosRaiz();

        // Clasificar archivos
        const clasificacion = {
            permitido: [],
            documentacion: [],
            scripts: [],
            temporal: [],
            desconocido: []
        };

        for (const archivo of this.archivos_raiz) {
            const tipo = this.clasificarArchivo(archivo);
            clasificacion[tipo].push(archivo);
        }

        // Reportar problemas
        this.reportarProblemas(clasificacion);
        this.reportarAdvertencias(clasificacion);
        this.generarSugerencias(clasificacion);
        this.mostrarResumen();
        this.mostrarEstructuraRecomendada();
    }

    reportarProblemas(clasificacion) {
        if (clasificacion.documentacion.length > 0) {
            this.log('\n🔴 PROBLEMAS CRÍTICOS:', COLORES.bold + COLORES.rojo);
            this.log('─'.repeat(80), COLORES.rojo);
            this.log('\nArchivos de documentación en raíz que deberían estar en documentacion/:\n', COLORES.rojo);

            clasificacion.documentacion.forEach(archivo => {
                this.log(`  • ${archivo}`, COLORES.rojo);
                this.problemas.push(`${archivo} debería estar en documentacion/`);
            });
        }

        if (clasificacion.scripts.length > 0) {
            if (this.problemas.length === 0) {
                this.log('\n🔴 PROBLEMAS CRÍTICOS:', COLORES.bold + COLORES.rojo);
                this.log('─'.repeat(80), COLORES.rojo);
            }
            this.log('\nScripts en raíz que deberían estar en scripts/:\n', COLORES.rojo);

            clasificacion.scripts.forEach(archivo => {
                this.log(`  • ${archivo}`, COLORES.rojo);
                this.problemas.push(`${archivo} debería estar en scripts/`);
            });
        }
    }

    reportarAdvertencias(clasificacion) {
        if (clasificacion.temporal.length > 0) {
            this.log('\n⚠️  ADVERTENCIAS:', COLORES.bold + COLORES.amarillo);
            this.log('─'.repeat(80), COLORES.amarillo);
            this.log('\nArchivos temporales o de desarrollo que deberían revisarse:\n', COLORES.amarillo);

            clasificacion.temporal.forEach(archivo => {
                this.log(`  • ${archivo} - Considerar eliminar o mover`, COLORES.amarillo);
                this.advertencias.push(`${archivo} parece ser temporal`);
            });
        }

        if (clasificacion.desconocido.length > 0) {
            if (this.advertencias.length === 0) {
                this.log('\n⚠️  ADVERTENCIAS:', COLORES.bold + COLORES.amarillo);
                this.log('─'.repeat(80), COLORES.amarillo);
            }
            this.log('\nArchivos no clasificados (revisar si pertenecen en raíz):\n', COLORES.amarillo);

            clasificacion.desconocido.forEach(archivo => {
                this.log(`  • ${archivo}`, COLORES.amarillo);
                this.advertencias.push(`${archivo} no está clasificado`);
            });
        }
    }

    generarSugerencias(clasificacion) {
        this.log('\n💡 SUGERENCIAS DE MEJORA:', COLORES.bold + COLORES.azul);
        this.log('─'.repeat(80), COLORES.azul);

        if (clasificacion.documentacion.length > 0) {
            this.log('\n1. Mover archivos de documentación:', COLORES.azul);
            clasificacion.documentacion.forEach(archivo => {
                this.log(`   mv "${archivo}" documentacion/`, COLORES.cyan);
            });
            this.sugerencias.push('Organizar documentación en carpeta dedicada');
        }

        if (clasificacion.scripts.length > 0) {
            this.log('\n2. Mover scripts a su carpeta:', COLORES.azul);
            clasificacion.scripts.forEach(archivo => {
                this.log(`   mv "${archivo}" scripts/`, COLORES.cyan);
            });
            this.sugerencias.push('Organizar scripts en carpeta dedicada');
        }

        if (clasificacion.temporal.length > 0) {
            this.log('\n3. Limpiar archivos temporales:', COLORES.azul);
            clasificacion.temporal.forEach(archivo => {
                this.log(`   # Revisar si es necesario: ${archivo}`, COLORES.cyan);
            });
            this.sugerencias.push('Limpiar archivos temporales no necesarios');
        }

        // Sugerencias adicionales
        this.log('\n4. Sugerencias adicionales de arquitectura:', COLORES.azul);
        this.log('   • Crear .cursorignore para excluir archivos temporales', COLORES.cyan);
        this.log('   • Actualizar .gitignore con archivos de trabajo temporal', COLORES.cyan);
        this.log('   • Considerar crear documentacion/jira/ para tickets', COLORES.cyan);
        this.log('   • Crear documentacion/reportes/ para reportes de calidad', COLORES.cyan);
    }

    mostrarResumen() {
        this.log('\n📊 RESUMEN:', COLORES.bold + COLORES.magenta);
        this.log('─'.repeat(80), COLORES.magenta);

        const total_problemas = this.problemas.length;
        const total_advertencias = this.advertencias.length;
        const total_sugerencias = this.sugerencias.length;

        this.log(`\n  Problemas críticos: ${total_problemas}`,
            total_problemas > 0 ? COLORES.rojo : COLORES.verde);
        this.log(`  Advertencias: ${total_advertencias}`,
            total_advertencias > 0 ? COLORES.amarillo : COLORES.verde);
        this.log(`  Sugerencias: ${total_sugerencias}`, COLORES.azul);

        if (total_problemas === 0 && total_advertencias === 0) {
            this.log('\n✅ ¡La arquitectura del proyecto está limpia!', COLORES.bold + COLORES.verde);
        } else {
            this.log('\n⚡ Se recomienda atender los problemas identificados', COLORES.bold + COLORES.amarillo);
        }
    }

    mostrarEstructuraRecomendada() {
        this.log('\n📁 ESTRUCTURA RECOMENDADA:', COLORES.bold + COLORES.verde);
        this.log('─'.repeat(80), COLORES.verde);
        this.log(`
proyecto/
├── README.md                    # Documentación principal
├── requirements.txt             # Dependencias Python
├── docker-compose.yml          # Configuración Docker
├── .gitignore                  # Archivos ignorados por git
├── .cursorignore              # Archivos ignorados por Cursor
│
├── documentacion/              # 📚 Toda la documentación
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── jira/                   # Tickets y tareas
│   │   ├── JAR-200.md
│   │   └── ...
│   ├── reportes/              # Reportes de calidad
│   │   ├── REPORTE_CALIDAD.md
│   │   └── ...
│   └── guias/                 # Guías y tutoriales
│       ├── GUIA_INSTALACION.md
│       └── ...
│
├── src/                       # 🔧 Código fuente
│   └── ...
│
├── tests/                     # ✅ Tests
│   └── ...
│
├── scripts/                   # 🚀 Scripts de automatización
│   ├── setup_windows.ps1
│   ├── setup_linux.sh
│   └── ...
│
├── airflow/                   # Configuración Airflow
│   ├── dags/
│   ├── logs/
│   └── plugins/
│
└── data/                      # 💾 Datos (si aplica)
    ├── raw/
    ├── processed/
    └── ...
`, COLORES.verde);

        this.log('\n💡 Principios de organización:', COLORES.bold + COLORES.cyan);
        this.log('  1. Raíz limpia: solo archivos esenciales de configuración', COLORES.cyan);
        this.log('  2. Documentación agrupada: fácil de encontrar y mantener', COLORES.cyan);
        this.log('  3. Código separado: src/ para código, tests/ para pruebas', COLORES.cyan);
        this.log('  4. Scripts organizados: herramientas en un solo lugar', COLORES.cyan);
        this.log('  5. Sin archivos temporales: mantener limpio el repositorio', COLORES.cyan);
    }
}

// Ejecutar el revisor
const revisor = new RevisorArquitectura();
revisor.analizar().catch(error => {
    console.error(`${COLORES.rojo}Error fatal: ${error.message}${COLORES.reset}`);
    process.exit(1);
});

