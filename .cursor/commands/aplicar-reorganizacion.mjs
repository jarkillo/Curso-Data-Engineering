#!/usr/bin/env node

/**
 * Comando para aplicar automáticamente la reorganización sugerida
 * Mueve archivos a sus ubicaciones correctas según las reglas de arquitectura
 *
 * IMPORTANTE: Ejecutar primero revisar-arquitectura.mjs para ver qué se va a mover
 */

import { readdir, stat, rename, mkdir, access } from 'fs/promises';
import { join } from 'path';
import { constants } from 'fs';

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

// Configuración de la reorganización
const REORGANIZACION = {
    documentacion: {
        destino: 'documentacion',
        patrones: [
            'CHANGELOG.md',
            'GUIA_*.md',
            'PROGRAMA_*.md',
            'PROYECTOS_*.md',
            'RECURSOS.md',
            'RESUMEN_*.md',
            'ENV_EXAMPLE.md',
            '*_JAR-*.md',
            'REPORTE_*.md',
            'CHECKLIST_*.md',
            'INSTRUCCIONES_*.md',
            'PR_*.md',
            'COMMIT_MESSAGE_*.md',
            'REVISION_*.md',
            '*.pdf'
        ],
        subcarpetas: {
            jira: ['*_JAR-*.md', 'CHECKLIST_JAR-*.md'],
            reportes: ['REPORTE_*.md', 'REVISION_*.md'],
            guias: ['GUIA_*.md', 'ENV_EXAMPLE.md'],
            pull_requests: ['PR_*.md', 'COMMIT_MESSAGE_*.md', 'INSTRUCCIONES_PR_*.md']
        }
    },
    scripts: {
        destino: 'scripts',
        patrones: ['*.sh', '*.ps1', '*.bat']
    },
    juego: {
        destino: 'documentacion/juego',
        patrones: [
            'README_JUEGO*.md',
            'RESUMEN_JUEGO.md',
            'game.html',
            'data_engineer_game.py',
            'EMPRESAS_FICTICIAS.md'
        ]
    }
};

// Archivos que NO deben moverse (permitidos en raíz)
const RAIZ_PERMITIDOS = [
    'README.md',
    'requirements.txt',
    'docker-compose.yml',
    '.gitignore',
    '.cursorignore',
    '.env',
    'pyproject.toml',
    'setup.py',
    'LICENSE',
    '.coverage',
    'game_save.json',  // Archivo de guardado del juego, se mantiene en raíz
    'ORDEN_DE_IMPLEMENTACION.md'  // Documento importante de gestión
];

class ReorganizadorArquitectura {
    constructor(dryRun = false) {
        this.dryRun = dryRun;
        this.movimientos = [];
        this.errores = [];
        this.directoriosCreados = new Set();
    }

    log(mensaje, color = '') {
        console.log(`${color}${mensaje}${COLORES.reset}`);
    }

    coincidePatron(archivo, patron) {
        const regex = new RegExp('^' + patron.replace(/\*/g, '.*') + '$');
        return regex.test(archivo);
    }

    async directorioExiste(ruta) {
        try {
            await access(ruta, constants.F_OK);
            return true;
        } catch {
            return false;
        }
    }

    async crearDirectorio(ruta) {
        if (this.directoriosCreados.has(ruta)) {
            return;
        }

        if (await this.directorioExiste(ruta)) {
            this.directoriosCreados.add(ruta);
            return;
        }

        if (this.dryRun) {
            this.log(`  [DRY-RUN] Crearía directorio: ${ruta}`, COLORES.cyan);
        } else {
            await mkdir(ruta, { recursive: true });
            this.log(`  ✅ Directorio creado: ${ruta}`, COLORES.verde);
        }

        this.directoriosCreados.add(ruta);
    }

    determinarSubcarpeta(archivo, categoria) {
        if (categoria !== 'documentacion') {
            return null;
        }

        const subcarpetas = REORGANIZACION.documentacion.subcarpetas;

        for (const [subcarpeta, patrones] of Object.entries(subcarpetas)) {
            for (const patron of patrones) {
                if (this.coincidePatron(archivo, patron)) {
                    return subcarpeta;
                }
            }
        }

        return null;
    }

    clasificarArchivo(archivo) {
        // Si está permitido en raíz, no mover
        if (RAIZ_PERMITIDOS.includes(archivo)) {
            return null;
        }

        // Verificar cada categoría
        for (const [categoria, config] of Object.entries(REORGANIZACION)) {
            for (const patron of config.patrones) {
                if (this.coincidePatron(archivo, patron)) {
                    return categoria;
                }
            }
        }

        return null;
    }

    async obtenerArchivosRaiz() {
        const items = await readdir('.');
        const archivos = [];

        for (const item of items) {
            try {
                const stats = await stat(item);
                if (stats.isFile() && !item.startsWith('.')) {
                    archivos.push(item);
                }
            } catch (error) {
                // Ignorar archivos que no se pueden leer
            }
        }

        return archivos;
    }

    async moverArchivo(archivo, destino) {
        try {
            if (this.dryRun) {
                this.log(`  [DRY-RUN] ${archivo} → ${destino}`, COLORES.cyan);
            } else {
                await rename(archivo, destino);
                this.log(`  ✅ ${archivo} → ${destino}`, COLORES.verde);
            }

            this.movimientos.push({ archivo, destino, exito: true });
        } catch (error) {
            this.log(`  ❌ Error al mover ${archivo}: ${error.message}`, COLORES.rojo);
            this.errores.push({ archivo, error: error.message });
            this.movimientos.push({ archivo, destino, exito: false, error: error.message });
        }
    }

    async reorganizar() {
        this.log('\n' + '='.repeat(80), COLORES.bold + COLORES.magenta);
        this.log('🔄 REORGANIZADOR DE ARQUITECTURA DEL PROYECTO', COLORES.bold + COLORES.magenta);
        if (this.dryRun) {
            this.log('   [MODO DRY-RUN - No se moverán archivos realmente]', COLORES.amarillo);
        }
        this.log('='.repeat(80) + '\n', COLORES.bold + COLORES.magenta);

        // Obtener archivos en raíz
        const archivos = await this.obtenerArchivosRaiz();

        // Agrupar por categoría
        const archivosPorCategoria = {};

        for (const archivo of archivos) {
            const categoria = this.clasificarArchivo(archivo);
            if (categoria) {
                if (!archivosPorCategoria[categoria]) {
                    archivosPorCategoria[categoria] = [];
                }
                archivosPorCategoria[categoria].push(archivo);
            }
        }

        // Si no hay nada que mover
        if (Object.keys(archivosPorCategoria).length === 0) {
            this.log('✅ No hay archivos que necesiten reorganizarse', COLORES.verde);
            this.log('\nLa arquitectura del proyecto ya está limpia y organizada.\n', COLORES.verde);
            return;
        }

        // Mostrar plan de reorganización
        this.log('📋 PLAN DE REORGANIZACIÓN:\n', COLORES.bold + COLORES.azul);

        for (const [categoria, archivosCategoria] of Object.entries(archivosPorCategoria)) {
            const config = REORGANIZACION[categoria];
            this.log(`${categoria.toUpperCase()} (${archivosCategoria.length} archivos):`, COLORES.amarillo);

            for (const archivo of archivosCategoria) {
                const subcarpeta = this.determinarSubcarpeta(archivo, categoria);
                const destino = subcarpeta
                    ? join(config.destino, subcarpeta)
                    : config.destino;
                this.log(`  • ${archivo} → ${destino}/`, COLORES.cyan);
            }
            this.log('');
        }

        // Confirmar si no es dry-run
        if (!this.dryRun) {
            this.log('⚠️  ADVERTENCIA: Esta operación moverá archivos.', COLORES.bold + COLORES.amarillo);
            this.log('Si quieres ver qué se movería sin hacerlo, ejecuta con --dry-run\n', COLORES.amarillo);
        }

        // Crear directorios necesarios
        this.log('📁 Creando directorios necesarios...\n', COLORES.bold + COLORES.azul);

        const directoriosNecesarios = new Set();
        for (const [categoria, archivosCategoria] of Object.entries(archivosPorCategoria)) {
            const config = REORGANIZACION[categoria];
            directoriosNecesarios.add(config.destino);

            for (const archivo of archivosCategoria) {
                const subcarpeta = this.determinarSubcarpeta(archivo, categoria);
                if (subcarpeta) {
                    directoriosNecesarios.add(join(config.destino, subcarpeta));
                }
            }
        }

        for (const dir of directoriosNecesarios) {
            await this.crearDirectorio(dir);
        }

        // Mover archivos
        this.log('\n🚚 Moviendo archivos...\n', COLORES.bold + COLORES.azul);

        for (const [categoria, archivosCategoria] of Object.entries(archivosPorCategoria)) {
            const config = REORGANIZACION[categoria];

            for (const archivo of archivosCategoria) {
                const subcarpeta = this.determinarSubcarpeta(archivo, categoria);
                const destinoDir = subcarpeta
                    ? join(config.destino, subcarpeta)
                    : config.destino;
                const destinoCompleto = join(destinoDir, archivo);

                await this.moverArchivo(archivo, destinoCompleto);
            }
        }

        // Resumen
        this.mostrarResumen();
    }

    mostrarResumen() {
        this.log('\n' + '='.repeat(80), COLORES.bold + COLORES.magenta);
        this.log('📊 RESUMEN DE REORGANIZACIÓN', COLORES.bold + COLORES.magenta);
        this.log('='.repeat(80), COLORES.bold + COLORES.magenta);

        const exitosos = this.movimientos.filter(m => m.exito).length;
        const fallidos = this.errores.length;

        this.log(`\n  Archivos movidos exitosamente: ${exitosos}`,
            exitosos > 0 ? COLORES.verde : COLORES.amarillo);
        this.log(`  Errores: ${fallidos}`,
            fallidos > 0 ? COLORES.rojo : COLORES.verde);

        if (fallidos > 0) {
            this.log('\n❌ Errores encontrados:', COLORES.rojo);
            for (const error of this.errores) {
                this.log(`  • ${error.archivo}: ${error.error}`, COLORES.rojo);
            }
        }

        if (this.dryRun) {
            this.log('\n💡 Esto fue una simulación. Para aplicar los cambios, ejecuta sin --dry-run',
                COLORES.bold + COLORES.cyan);
        } else if (exitosos > 0) {
            this.log('\n✅ Reorganización completada con éxito!', COLORES.bold + COLORES.verde);
            this.log('\n💡 Sugerencias:', COLORES.azul);
            this.log('  1. Verifica que los archivos se movieron correctamente', COLORES.cyan);
            this.log('  2. Actualiza cualquier referencia a estos archivos en tu código', COLORES.cyan);
            this.log('  3. Ejecuta "node .cursor/commands/revisar-arquitectura.mjs" para verificar', COLORES.cyan);
            this.log('  4. Haz commit de los cambios si todo está bien', COLORES.cyan);
        }

        this.log('');
    }
}

// Procesar argumentos de línea de comandos
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run') || args.includes('-d');

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
${COLORES.bold}${COLORES.cyan}REORGANIZADOR DE ARQUITECTURA${COLORES.reset}

Mueve automáticamente archivos a sus ubicaciones correctas según las reglas de arquitectura.

${COLORES.bold}Uso:${COLORES.reset}
  node .cursor/commands/aplicar-reorganizacion.mjs [opciones]

${COLORES.bold}Opciones:${COLORES.reset}
  --dry-run, -d    Simula la reorganización sin mover archivos
  --help, -h       Muestra esta ayuda

${COLORES.bold}Ejemplos:${COLORES.reset}
  # Ver qué se movería (simulación)
  node .cursor/commands/aplicar-reorganizacion.mjs --dry-run

  # Aplicar la reorganización
  node .cursor/commands/aplicar-reorganizacion.mjs

${COLORES.bold}Recomendación:${COLORES.reset}
  Ejecuta primero con --dry-run para ver qué cambios se aplicarían.
`);
    process.exit(0);
}

// Ejecutar reorganización
const reorganizador = new ReorganizadorArquitectura(dryRun);
reorganizador.reorganizar().catch(error => {
    console.error(`${COLORES.rojo}Error fatal: ${error.message}${COLORES.reset}`);
    process.exit(1);
});

