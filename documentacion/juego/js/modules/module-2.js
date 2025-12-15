/**
 * Module 2: SQL - Data Engineer: The Game
 *
 * Missions covering SQL fundamentals:
 * - SELECT queries
 * - WHERE filtering
 * - JOINs
 * - Aggregations (GROUP BY, HAVING)
 * - Query optimization
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE DATA FOR SQL MISSIONS
    // ==========================================

    // Tables for the SQL database
    const TABLES = {
        empleados: {
            columns: [
                { name: 'id', type: 'INTEGER PRIMARY KEY' },
                { name: 'nombre', type: 'TEXT' },
                { name: 'departamento_id', type: 'INTEGER' },
                { name: 'salario', type: 'REAL' },
                { name: 'fecha_contratacion', type: 'TEXT' }
            ],
            data: [
                [1, 'Ana García', 1, 45000, '2020-03-15'],
                [2, 'Carlos López', 2, 52000, '2019-07-01'],
                [3, 'María Rodríguez', 1, 48000, '2021-01-10'],
                [4, 'Juan Martínez', 3, 55000, '2018-11-20'],
                [5, 'Laura Sánchez', 2, 47000, '2022-02-28'],
                [6, 'Pedro Fernández', 1, 51000, '2020-08-05'],
                [7, 'Sofia Torres', 3, 62000, '2017-04-12'],
                [8, 'Diego Ruiz', 2, 44000, '2023-01-15'],
                [9, 'Elena Díaz', 1, 49000, '2021-06-20'],
                [10, 'Miguel Herrera', 3, 58000, '2019-09-30']
            ]
        },
        departamentos: {
            columns: [
                { name: 'id', type: 'INTEGER PRIMARY KEY' },
                { name: 'nombre', type: 'TEXT' },
                { name: 'presupuesto', type: 'REAL' }
            ],
            data: [
                [1, 'Ingeniería', 500000],
                [2, 'Marketing', 300000],
                [3, 'Ventas', 400000],
                [4, 'RRHH', 150000]
            ]
        },
        ventas: {
            columns: [
                { name: 'id', type: 'INTEGER PRIMARY KEY' },
                { name: 'empleado_id', type: 'INTEGER' },
                { name: 'producto', type: 'TEXT' },
                { name: 'cantidad', type: 'INTEGER' },
                { name: 'precio_unitario', type: 'REAL' },
                { name: 'fecha', type: 'TEXT' }
            ],
            data: [
                [1, 4, 'Software ERP', 2, 15000, '2024-01-15'],
                [2, 7, 'Licencia Cloud', 5, 3000, '2024-01-18'],
                [3, 10, 'Consultoría', 1, 25000, '2024-01-20'],
                [4, 4, 'Software CRM', 3, 8000, '2024-01-22'],
                [5, 7, 'Soporte Anual', 10, 2000, '2024-01-25'],
                [6, 10, 'Software ERP', 1, 15000, '2024-02-01'],
                [7, 4, 'Licencia Cloud', 8, 3000, '2024-02-05'],
                [8, 7, 'Consultoría', 2, 25000, '2024-02-10'],
                [9, 10, 'Software CRM', 4, 8000, '2024-02-15'],
                [10, 4, 'Soporte Anual', 15, 2000, '2024-02-20']
            ]
        },
        clientes: {
            columns: [
                { name: 'id', type: 'INTEGER PRIMARY KEY' },
                { name: 'empresa', type: 'TEXT' },
                { name: 'sector', type: 'TEXT' },
                { name: 'pais', type: 'TEXT' }
            ],
            data: [
                [1, 'TechCorp', 'Tecnología', 'España'],
                [2, 'BancoSeguro', 'Finanzas', 'México'],
                [3, 'RetailMax', 'Comercio', 'España'],
                [4, 'HealthPlus', 'Salud', 'Colombia'],
                [5, 'EduLearn', 'Educación', 'Argentina']
            ]
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'sql_1',
            title: 'Misión 1: Tu Primera Query',
            description: `
                <p><strong>Cliente: QueryMasters Inc.</strong></p>
                <p>El departamento de RRHH necesita ver la lista de todos los empleados.</p>
                <p>Escribe una query que muestre <strong>todos los campos</strong> de la tabla <code>empleados</code>.</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Usa SELECT * FROM para obtener todos los campos.
                </div>
            `,
            type: 'sql',
            xp: 100,
            tables: ['empleados'],
            validate: function(result, query) {
                // Check if query is a SELECT
                const normalizedQuery = query.toUpperCase().trim();
                if (!normalizedQuery.startsWith('SELECT')) {
                    return { success: false, message: 'Tu query debe empezar con SELECT' };
                }

                // Check if it returns all employees
                if (!result.success || !result.rows) {
                    return { success: false, message: 'La query no devolvió resultados' };
                }

                if (result.rows.length !== 10) {
                    return { success: false, message: `Esperábamos 10 empleados, obtuvimos ${result.rows.length}` };
                }

                // Check if all columns are present
                if (result.columns.length < 5) {
                    return { success: false, message: 'Faltan columnas. Usa SELECT * para obtener todas.' };
                }

                return { success: true };
            },
            solution: 'SELECT * FROM empleados;'
        },
        {
            id: 'sql_2',
            title: 'Misión 2: Filtrar con WHERE',
            description: `
                <p><strong>Cliente: QueryMasters Inc.</strong></p>
                <p>El CFO quiere ver solo los empleados con <strong>salario mayor a 50000</strong>.</p>
                <p>Escribe una query que filtre los empleados por salario.</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Usa WHERE para filtrar: WHERE columna > valor
                </div>
            `,
            type: 'sql',
            xp: 100,
            tables: ['empleados'],
            validate: function(result, query) {
                const normalizedQuery = query.toUpperCase();

                if (!normalizedQuery.includes('WHERE')) {
                    return { success: false, message: 'Debes usar la cláusula WHERE para filtrar' };
                }

                if (!normalizedQuery.includes('SALARIO')) {
                    return { success: false, message: 'Debes filtrar por la columna salario' };
                }

                if (!result.success || !result.rows) {
                    return { success: false, message: 'La query no devolvió resultados' };
                }

                // Should return 4 employees with salary > 50000
                if (result.rows.length !== 4) {
                    return { success: false, message: `Esperábamos 4 empleados con salario > 50000, obtuvimos ${result.rows.length}` };
                }

                return { success: true };
            },
            solution: 'SELECT * FROM empleados WHERE salario > 50000;'
        },
        {
            id: 'sql_3',
            title: 'Misión 3: Unir Tablas con JOIN',
            description: `
                <p><strong>Cliente: QueryMasters Inc.</strong></p>
                <p>Necesitamos un reporte que muestre el <strong>nombre del empleado</strong> junto con el <strong>nombre de su departamento</strong>.</p>
                <p>Une las tablas <code>empleados</code> y <code>departamentos</code>.</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Usa JOIN ... ON para conectar tablas por sus claves.
                </div>
            `,
            type: 'sql',
            xp: 150,
            tables: ['empleados', 'departamentos'],
            validate: function(result, query) {
                const normalizedQuery = query.toUpperCase();

                if (!normalizedQuery.includes('JOIN')) {
                    return { success: false, message: 'Debes usar JOIN para unir las tablas' };
                }

                if (!normalizedQuery.includes('ON')) {
                    return { success: false, message: 'Debes especificar la condición de unión con ON' };
                }

                if (!result.success || !result.rows) {
                    return { success: false, message: 'La query no devolvió resultados' };
                }

                // Should return 10 rows (all employees have departments)
                if (result.rows.length !== 10) {
                    return { success: false, message: `Esperábamos 10 resultados, obtuvimos ${result.rows.length}` };
                }

                // Check that department name is included
                const hasDepName = result.columns.some(col =>
                    col.toLowerCase().includes('departamento') ||
                    col.toLowerCase().includes('nombre')
                );

                if (result.columns.length < 2) {
                    return { success: false, message: 'Incluye al menos el nombre del empleado y del departamento' };
                }

                return { success: true };
            },
            solution: `SELECT e.nombre, d.nombre as departamento
FROM empleados e
JOIN departamentos d ON e.departamento_id = d.id;`
        },
        {
            id: 'sql_4',
            title: 'Misión 4: Agregaciones con GROUP BY',
            description: `
                <p><strong>Cliente: QueryMasters Inc.</strong></p>
                <p>El CEO quiere saber cuántos empleados hay en <strong>cada departamento</strong> y el <strong>salario promedio</strong>.</p>
                <p>Agrupa los datos y calcula las métricas.</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Usa GROUP BY con COUNT() y AVG()
                </div>
            `,
            type: 'sql',
            xp: 150,
            tables: ['empleados', 'departamentos'],
            validate: function(result, query) {
                const normalizedQuery = query.toUpperCase();

                if (!normalizedQuery.includes('GROUP BY')) {
                    return { success: false, message: 'Debes usar GROUP BY para agrupar' };
                }

                if (!normalizedQuery.includes('COUNT')) {
                    return { success: false, message: 'Usa COUNT() para contar empleados' };
                }

                if (!normalizedQuery.includes('AVG')) {
                    return { success: false, message: 'Usa AVG() para calcular el promedio' };
                }

                if (!result.success || !result.rows) {
                    return { success: false, message: 'La query no devolvió resultados' };
                }

                // Should return 3 departments (only ones with employees)
                if (result.rows.length !== 3) {
                    return { success: false, message: `Esperábamos 3 departamentos con empleados, obtuvimos ${result.rows.length}` };
                }

                return { success: true };
            },
            solution: `SELECT d.nombre as departamento,
       COUNT(e.id) as num_empleados,
       AVG(e.salario) as salario_promedio
FROM empleados e
JOIN departamentos d ON e.departamento_id = d.id
GROUP BY d.id, d.nombre;`
        },
        {
            id: 'sql_5',
            title: 'Misión 5: Query Avanzada',
            description: `
                <p><strong>Cliente: QueryMasters Inc.</strong></p>
                <p>Encuentra los departamentos donde el <strong>salario promedio supera los 50000</strong>.</p>
                <p>Muestra el nombre del departamento, número de empleados y salario promedio.</p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Usa HAVING para filtrar después de GROUP BY
                </div>
            `,
            type: 'sql',
            xp: 200,
            tables: ['empleados', 'departamentos'],
            validate: function(result, query) {
                const normalizedQuery = query.toUpperCase();

                if (!normalizedQuery.includes('GROUP BY')) {
                    return { success: false, message: 'Debes usar GROUP BY' };
                }

                if (!normalizedQuery.includes('HAVING')) {
                    return { success: false, message: 'Usa HAVING para filtrar grupos (WHERE es para filas individuales)' };
                }

                if (!normalizedQuery.includes('AVG')) {
                    return { success: false, message: 'Necesitas AVG() para calcular el promedio' };
                }

                if (!result.success || !result.rows) {
                    return { success: false, message: 'La query no devolvió resultados' };
                }

                // Should return 1 department (Ventas with avg ~58333)
                if (result.rows.length !== 1) {
                    return { success: false, message: `Esperábamos 1 departamento con salario promedio > 50000, obtuvimos ${result.rows.length}` };
                }

                return { success: true };
            },
            solution: `SELECT d.nombre as departamento,
       COUNT(e.id) as num_empleados,
       AVG(e.salario) as salario_promedio
FROM empleados e
JOIN departamentos d ON e.departamento_id = d.id
GROUP BY d.id, d.nombre
HAVING AVG(e.salario) > 50000;`
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 2: SQL',
            scenes: [
                {
                    id: 1,
                    content: `
                        Has completado tu primer mes en <strong>DataFlow Industries</strong>.
                        María está impresionada con tu progreso en estadística.
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
                        "¡Excelente trabajo con las estadísticas! Ahora es momento de aprender
                        la herramienta más importante de un Data Engineer: <strong>SQL</strong>."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Tenemos un nuevo cliente: <strong>QueryMasters Inc.</strong>
                        Necesitan organizar y consultar sus datos de empleados y ventas."
                    `,
                    tutorial: {
                        title: '¿Qué es SQL?',
                        content: `
                            <ul>
                                <li><strong>S</strong>tructured <strong>Q</strong>uery <strong>L</strong>anguage</li>
                                <li>Lenguaje para comunicarte con bases de datos</li>
                                <li>Permite consultar, insertar, actualizar y eliminar datos</li>
                                <li>Usado en el 90% de las empresas con datos</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Empezaremos con lo básico: <strong>SELECT</strong>.
                        Es la instrucción para LEER datos de una tabla."
                    `,
                    tutorial: {
                        title: 'Anatomía de una Query',
                        content: `
                            <code>SELECT columnas FROM tabla WHERE condición;</code>
                            <br><br>
                            <ul>
                                <li><strong>SELECT</strong>: Qué columnas quieres ver</li>
                                <li><strong>FROM</strong>: De qué tabla</li>
                                <li><strong>WHERE</strong>: Filtros (opcional)</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'QueryMasters Inc.'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Setup database tables for SQL missions
     * @param {Object} SQLEditor - Reference to SQL Editor tool
     */
    function setupDatabase(SQLEditor) {
        if (!SQLEditor || !SQLEditor.isReady()) {
            console.warn('[Module2] SQLEditor not ready');
            return false;
        }

        Object.entries(TABLES).forEach(([tableName, tableData]) => {
            SQLEditor.createTable(tableName, tableData.columns, tableData.data);
        });

        console.log('[Module2] Database tables created');
        return true;
    }

    /**
     * Get table schema for display
     * @param {string} tableName
     * @returns {Object}
     */
    function getTableSchema(tableName) {
        return TABLES[tableName] || null;
    }

    /**
     * Get all table names
     * @returns {Array}
     */
    function getTableNames() {
        return Object.keys(TABLES);
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(2, {
            missions: MISSIONS,
            story: STORY,
            tables: TABLES,
            helpers: {
                setupDatabase,
                getTableSchema,
                getTableNames
            }
        });
        console.log('[Module2] SQL module registered');
    }

    // Expose globally for backwards compatibility
    window.Module2 = {
        MISSIONS,
        STORY,
        TABLES,
        setupDatabase,
        getTableSchema,
        getTableNames
    };

})();
