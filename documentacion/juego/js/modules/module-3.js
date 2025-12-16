/**
 * Module 3: ETL - Data Engineer: The Game
 *
 * Missions covering ETL fundamentals:
 * - Extract: Reading data from sources
 * - Transform: Cleaning and processing data
 * - Load: Writing data to destinations
 * - Data validation and quality
 * - Pipeline design
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE DATA FOR ETL MISSIONS
    // ==========================================

    // Raw CSV data (simulated)
    const RAW_DATA = {
        ventas_csv: [
            { id: '1', producto: 'Laptop Pro', cantidad: '5', precio: '1200.50', fecha: '2024-01-15' },
            { id: '2', producto: 'Monitor 27"', cantidad: '10', precio: '350.00', fecha: '2024-01-16' },
            { id: '3', producto: 'Teclado RGB', cantidad: '', precio: '85.99', fecha: '2024-01-16' },
            { id: '4', producto: 'Mouse Wireless', cantidad: '25', precio: 'ERROR', fecha: '2024-01-17' },
            { id: '5', producto: 'Laptop Pro', cantidad: '3', precio: '1200.50', fecha: '15/01/2024' },
            { id: '6', producto: 'Webcam HD', cantidad: '-2', precio: '120.00', fecha: '2024-01-18' },
            { id: '7', producto: 'Monitor 27"', cantidad: '8', precio: '350.00', fecha: '2024-01-18' },
            { id: '8', producto: 'Auriculares', cantidad: '15', precio: '75.50', fecha: null },
            { id: '9', producto: 'laptop pro', cantidad: '2', precio: '1200.50', fecha: '2024-01-19' },
            { id: '10', producto: 'SSD 1TB', cantidad: '20', precio: '89.99', fecha: '2024-01-20' }
        ],
        clientes_json: [
            { cliente_id: 'C001', nombre: 'Tech Solutions', email: 'contact@techsol.com', activo: true },
            { cliente_id: 'C002', nombre: 'Digital Corp', email: 'invalid-email', activo: true },
            { cliente_id: 'C003', nombre: '', email: 'info@dataflow.io', activo: false },
            { cliente_id: 'C004', nombre: 'Cloud Systems', email: 'sales@cloudsys.com', activo: true },
            { cliente_id: 'C005', nombre: 'AI Innovations', email: null, activo: true }
        ]
    };

    // Data quality rules
    const QUALITY_RULES = {
        ventas: {
            cantidad: { type: 'integer', min: 0, required: true },
            precio: { type: 'decimal', min: 0, required: true },
            fecha: { type: 'date', format: 'YYYY-MM-DD', required: true },
            producto: { type: 'string', required: true }
        },
        clientes: {
            nombre: { type: 'string', required: true, minLength: 1 },
            email: { type: 'email', required: true },
            activo: { type: 'boolean', required: true }
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'etl_1',
            title: 'Misión 1: Extraer Datos',
            description: `
                <p><strong>Cliente: DataFlow Industries</strong></p>
                <p>Tenemos un archivo CSV con datos de ventas. Antes de procesarlo, necesitamos entender su estructura.</p>
                <p>Analiza los datos y responde: <strong>¿Cuántas filas tiene el dataset?</strong></p>
                <div class="mission-data">
                    <pre>${JSON.stringify(RAW_DATA.ventas_csv.slice(0, 3), null, 2)}...</pre>
                    <p class="data-note">Mostrando 3 de N filas</p>
                </div>
            `,
            type: 'numeric',
            xp: 100,
            data: RAW_DATA.ventas_csv,
            validate: function(answer, data) {
                return Math.abs(answer - data.length) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.length; // 10
            }
        },
        {
            id: 'etl_2',
            title: 'Misión 2: Identificar Problemas',
            description: `
                <p><strong>Cliente: DataFlow Industries</strong></p>
                <p>Antes de transformar datos, debemos identificar problemas de calidad.</p>
                <p>Analiza el dataset de ventas y cuenta: <strong>¿Cuántas filas tienen al menos un problema?</strong></p>
                <div class="mission-hint">
                    <strong>Problemas a buscar:</strong>
                    <ul>
                        <li>Valores vacíos o null</li>
                        <li>Valores no numéricos donde debería haber números</li>
                        <li>Números negativos en cantidad</li>
                        <li>Formatos de fecha incorrectos</li>
                        <li>Inconsistencias en mayúsculas/minúsculas</li>
                    </ul>
                </div>
            `,
            type: 'numeric',
            xp: 150,
            data: RAW_DATA.ventas_csv,
            validate: function(answer, data) {
                // Problems: row 3 (empty cantidad), row 4 (ERROR precio),
                // row 5 (wrong date format), row 6 (negative cantidad),
                // row 8 (null fecha), row 9 (lowercase producto)
                const correctAnswer = 6;
                return Math.abs(answer - correctAnswer) < 0.5;
            },
            getCorrectAnswer: function() {
                return 6;
            }
        },
        {
            id: 'etl_3',
            title: 'Misión 3: Transformar Datos',
            description: `
                <p><strong>Cliente: DataFlow Industries</strong></p>
                <p>Después de limpiar los datos problemáticos, necesitamos transformarlos.</p>
                <p>Si eliminamos las filas con problemas y calculamos el <strong>total de ventas</strong> (cantidad × precio), ¿cuál es el resultado?</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Filas válidas: 1, 2, 7, 10
                </div>
            `,
            type: 'numeric',
            xp: 150,
            data: RAW_DATA.ventas_csv,
            validate: function(answer, data) {
                // Valid rows: 1, 2, 7, 10
                // Row 1: 5 * 1200.50 = 6002.50
                // Row 2: 10 * 350.00 = 3500.00
                // Row 7: 8 * 350.00 = 2800.00
                // Row 10: 20 * 89.99 = 1799.80
                // Total: 14102.30
                const correctAnswer = 14102.30;
                return Math.abs(answer - correctAnswer) < 1;
            },
            getCorrectAnswer: function() {
                return 14102.30;
            }
        },
        {
            id: 'etl_4',
            title: 'Misión 4: Estrategia de Carga',
            description: `
                <p><strong>Cliente: DataFlow Industries</strong></p>
                <p>El cliente tiene una tabla de destino con 1 millón de registros históricos.</p>
                <p>Cada día llegan ~1000 registros nuevos. ¿Qué estrategia de carga es más eficiente?</p>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'full',
                    label: 'Full Load',
                    description: 'Borrar todo y recargar los 1M + 1000 registros'
                },
                {
                    id: 'incremental',
                    label: 'Incremental Load',
                    description: 'Solo cargar los 1000 registros nuevos'
                },
                {
                    id: 'merge',
                    label: 'Merge/Upsert',
                    description: 'Insertar nuevos y actualizar existentes'
                }
            ],
            validate: function(answer) {
                return answer === 'incremental';
            },
            correctAnswer: 'incremental',
            explanation: `
                <p><strong>Incremental Load</strong> es la mejor opción porque:</p>
                <ul>
                    <li>Solo procesa 1000 registros en lugar de 1,001,000</li>
                    <li>Menor tiempo de ejecución</li>
                    <li>Menor uso de recursos</li>
                    <li>Menor riesgo de errores</li>
                </ul>
                <p>Full Load sería necesario solo si los datos históricos cambiaran.</p>
            `
        },
        {
            id: 'etl_5',
            title: 'Misión 5: Diseño de Pipeline',
            description: `
                <p><strong>Cliente: DataFlow Industries</strong></p>
                <p>Diseña un pipeline ETL ordenando los pasos correctamente.</p>
                <p>¿Cuál es el <strong>orden correcto</strong> de estos pasos?</p>
                <ol type="A">
                    <li>Cargar datos limpios a la tabla destino</li>
                    <li>Validar calidad de datos</li>
                    <li>Extraer datos del archivo CSV</li>
                    <li>Transformar y limpiar datos</li>
                    <li>Registrar métricas del proceso</li>
                </ol>
            `,
            type: 'text',
            xp: 200,
            validate: function(answer) {
                // Correct order: C, B, D, A, E (Extract, Validate, Transform, Load, Log)
                // Or: C, D, B, A, E (Extract, Transform, Validate, Load, Log)
                const normalized = answer.toUpperCase().replace(/[^A-E]/g, '');

                // Accept both valid orderings
                const validOrders = ['CBDAE', 'CDBAE', 'CBADE'];
                return validOrders.includes(normalized);
            },
            correctAnswer: 'C, B, D, A, E',
            explanation: `
                <p><strong>Orden correcto del pipeline:</strong></p>
                <ol>
                    <li><strong>C - Extraer:</strong> Primero obtenemos los datos</li>
                    <li><strong>B - Validar:</strong> Verificamos calidad inicial</li>
                    <li><strong>D - Transformar:</strong> Limpiamos y procesamos</li>
                    <li><strong>A - Cargar:</strong> Guardamos en destino</li>
                    <li><strong>E - Registrar:</strong> Documentamos el proceso</li>
                </ol>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 3: ETL',
            scenes: [
                {
                    id: 1,
                    content: `
                        Ya dominas estadística y SQL. Ahora viene lo que realmente define
                        a un Data Engineer: los <strong>pipelines ETL</strong>.
                    `
                },
                {
                    id: 2,
                    character: {
                        name: 'María González',
                        role: 'Lead Data Engineer | Tu Mentora',
                        avatar: '👩‍💼'
                    },
                    content: `
                        "ETL es el corazón del Data Engineering. Es el proceso de mover datos
                        de un lugar a otro, transformándolos en el camino."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Vamos a trabajar con datos reales de nuestro cliente interno.
                        Verás que los datos nunca vienen perfectos..."
                    `,
                    tutorial: {
                        title: '¿Qué es ETL?',
                        content: `
                            <ul>
                                <li><strong>E</strong>xtract: Obtener datos de la fuente</li>
                                <li><strong>T</strong>ransform: Limpiar y procesar</li>
                                <li><strong>L</strong>oad: Cargar al destino</li>
                            </ul>
                            <p>Es el proceso más importante en Data Engineering.</p>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "En este módulo aprenderás a identificar problemas de datos,
                        limpiarlos, y diseñar pipelines robustos."
                    `,
                    tutorial: {
                        title: 'Problemas Comunes de Datos',
                        content: `
                            <ul>
                                <li>Valores nulos o vacíos</li>
                                <li>Tipos de datos incorrectos</li>
                                <li>Formatos inconsistentes</li>
                                <li>Duplicados</li>
                                <li>Valores fuera de rango</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'DataFlow Industries'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Validate a single row against rules
     * @param {Object} row - Data row
     * @param {Object} rules - Validation rules
     * @returns {Array} Array of errors
     */
    function validateRow(row, rules) {
        const errors = [];

        Object.entries(rules).forEach(([field, rule]) => {
            const value = row[field];

            // Required check
            if (rule.required && (value === null || value === undefined || value === '')) {
                errors.push(`${field}: valor requerido`);
                return;
            }

            if (value === null || value === undefined || value === '') return;

            // Type checks
            switch (rule.type) {
                case 'integer':
                    if (!/^-?\d+$/.test(value)) {
                        errors.push(`${field}: debe ser entero`);
                    } else if (rule.min !== undefined && parseInt(value) < rule.min) {
                        errors.push(`${field}: debe ser >= ${rule.min}`);
                    }
                    break;

                case 'decimal':
                    if (!/^-?\d+\.?\d*$/.test(value)) {
                        errors.push(`${field}: debe ser decimal`);
                    } else if (rule.min !== undefined && parseFloat(value) < rule.min) {
                        errors.push(`${field}: debe ser >= ${rule.min}`);
                    }
                    break;

                case 'date':
                    if (rule.format === 'YYYY-MM-DD' && !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                        errors.push(`${field}: formato de fecha inválido`);
                    }
                    break;

                case 'email':
                    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                        errors.push(`${field}: email inválido`);
                    }
                    break;

                case 'string':
                    if (rule.minLength && value.length < rule.minLength) {
                        errors.push(`${field}: longitud mínima ${rule.minLength}`);
                    }
                    break;
            }
        });

        return errors;
    }

    /**
     * Count rows with data quality issues
     * @param {Array} data
     * @param {Object} rules
     * @returns {number}
     */
    function countProblematicRows(data, rules) {
        return data.filter(row => validateRow(row, rules).length > 0).length;
    }

    /**
     * Clean and transform data
     * @param {Array} data
     * @param {Object} rules
     * @returns {Array} Cleaned data
     */
    function cleanData(data, rules) {
        return data.filter(row => validateRow(row, rules).length === 0);
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(3, {
            missions: MISSIONS,
            story: STORY,
            data: RAW_DATA,
            rules: QUALITY_RULES,
            helpers: {
                validateRow,
                countProblematicRows,
                cleanData
            }
        });
        console.log('[Module3] ETL module registered');
    }

    // Expose globally for backwards compatibility
    window.Module3 = {
        MISSIONS,
        STORY,
        RAW_DATA,
        QUALITY_RULES,
        validateRow,
        countProblematicRows,
        cleanData
    };

})();
