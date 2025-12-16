/**
 * Module 8: Data Warehousing - Data Engineer: The Game
 *
 * Missions covering Data Warehouse fundamentals:
 * - Star Schema design
 * - Snowflake Schema normalization
 * - Slowly Changing Dimensions (SCD Type 2)
 * - Pre-aggregated tables
 * - OLAP vs OLTP patterns
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE DATA WAREHOUSE DATA FOR MISSIONS
    // ==========================================

    // Star Schema example
    const STAR_SCHEMA = {
        factTable: {
            name: 'fact_ventas',
            columns: [
                { name: 'venta_id', type: 'INT', isPK: true },
                { name: 'fecha_id', type: 'INT', isFK: true, references: 'dim_fecha' },
                { name: 'producto_id', type: 'INT', isFK: true, references: 'dim_producto' },
                { name: 'cliente_id', type: 'INT', isFK: true, references: 'dim_cliente' },
                { name: 'tienda_id', type: 'INT', isFK: true, references: 'dim_tienda' },
                { name: 'cantidad', type: 'INT', isMeasure: true },
                { name: 'precio_unitario', type: 'DECIMAL', isMeasure: true },
                { name: 'total_venta', type: 'DECIMAL', isMeasure: true },
                { name: 'descuento', type: 'DECIMAL', isMeasure: true }
            ],
            rows: 5000000
        },
        dimensions: [
            {
                name: 'dim_fecha',
                columns: ['fecha_id', 'fecha', 'dia', 'mes', 'trimestre', 'anio', 'dia_semana', 'es_feriado'],
                rows: 3650
            },
            {
                name: 'dim_producto',
                columns: ['producto_id', 'nombre', 'categoria', 'subcategoria', 'marca', 'precio_lista'],
                rows: 5000
            },
            {
                name: 'dim_cliente',
                columns: ['cliente_id', 'nombre', 'email', 'ciudad', 'pais', 'segmento'],
                rows: 100000
            },
            {
                name: 'dim_tienda',
                columns: ['tienda_id', 'nombre', 'direccion', 'ciudad', 'region', 'tipo'],
                rows: 500
            }
        ]
    };

    // Snowflake Schema (normalized dimensions)
    const SNOWFLAKE_SCHEMA = {
        factTable: STAR_SCHEMA.factTable,
        dimensions: [
            {
                name: 'dim_producto',
                columns: ['producto_id', 'nombre', 'precio_lista', 'subcategoria_id'],
                normalized: true,
                children: [
                    {
                        name: 'dim_subcategoria',
                        columns: ['subcategoria_id', 'nombre', 'categoria_id'],
                        children: [
                            {
                                name: 'dim_categoria',
                                columns: ['categoria_id', 'nombre', 'departamento']
                            }
                        ]
                    }
                ]
            },
            {
                name: 'dim_tienda',
                columns: ['tienda_id', 'nombre', 'direccion', 'ciudad_id'],
                normalized: true,
                children: [
                    {
                        name: 'dim_ciudad',
                        columns: ['ciudad_id', 'nombre', 'region_id'],
                        children: [
                            {
                                name: 'dim_region',
                                columns: ['region_id', 'nombre', 'pais']
                            }
                        ]
                    }
                ]
            }
        ]
    };

    // SCD Type 2 example
    const SCD_DATA = {
        tableName: 'dim_cliente_scd2',
        columns: [
            { name: 'sk_cliente', type: 'INT', description: 'Surrogate Key (auto-increment)' },
            { name: 'cliente_id', type: 'INT', description: 'Natural/Business Key' },
            { name: 'nombre', type: 'VARCHAR', description: 'Nombre del cliente' },
            { name: 'email', type: 'VARCHAR', description: 'Email actual' },
            { name: 'segmento', type: 'VARCHAR', description: 'Segmento de cliente (puede cambiar)' },
            { name: 'valid_from', type: 'DATE', description: 'Fecha inicio de validez' },
            { name: 'valid_to', type: 'DATE', description: 'Fecha fin de validez (9999-12-31 si actual)' },
            { name: 'is_current', type: 'BOOLEAN', description: 'True si es el registro actual' }
        ],
        sampleData: [
            { sk_cliente: 1, cliente_id: 100, nombre: 'Ana García', segmento: 'Bronze', valid_from: '2022-01-01', valid_to: '2023-06-15', is_current: false },
            { sk_cliente: 2, cliente_id: 100, nombre: 'Ana García', segmento: 'Silver', valid_from: '2023-06-16', valid_to: '2024-03-01', is_current: false },
            { sk_cliente: 3, cliente_id: 100, nombre: 'Ana García', segmento: 'Gold', valid_from: '2024-03-02', valid_to: '9999-12-31', is_current: true }
        ]
    };

    // Aggregation tables
    const AGGREGATION_DATA = {
        baseQuery: `
SELECT
    d.anio, d.mes,
    p.categoria,
    t.region,
    SUM(f.total_venta) as total_ventas,
    COUNT(*) as num_transacciones
FROM fact_ventas f
JOIN dim_fecha d ON f.fecha_id = d.fecha_id
JOIN dim_producto p ON f.producto_id = p.producto_id
JOIN dim_tienda t ON f.tienda_id = t.tienda_id
GROUP BY d.anio, d.mes, p.categoria, t.region`,
        baseQueryTime: '45 segundos',
        aggregatedTable: {
            name: 'agg_ventas_mensual_categoria_region',
            columns: ['anio', 'mes', 'categoria', 'region', 'total_ventas', 'num_transacciones'],
            rows: 2400, // 2 years × 12 months × 10 categories × 10 regions
            queryTime: '0.1 segundos'
        }
    };

    // OLAP vs OLTP comparison
    const OLAP_OLTP_DATA = {
        scenarios: [
            {
                id: 1,
                description: 'Procesar una venta en el punto de venta (POS)',
                correctAnswer: 'OLTP',
                explanation: 'Transacción individual, baja latencia requerida'
            },
            {
                id: 2,
                description: 'Generar reporte de ventas mensuales por región',
                correctAnswer: 'OLAP',
                explanation: 'Análisis agregado de grandes volúmenes de datos'
            },
            {
                id: 3,
                description: 'Actualizar el email de un cliente',
                correctAnswer: 'OLTP',
                explanation: 'Operación UPDATE simple en un registro'
            },
            {
                id: 4,
                description: 'Calcular tendencias de ventas de los últimos 5 años',
                correctAnswer: 'OLAP',
                explanation: 'Análisis histórico de grandes conjuntos de datos'
            }
        ],
        comparison: {
            OLTP: {
                purpose: 'Operaciones diarias',
                queries: 'Simples, pocos registros',
                optimization: 'Inserts/Updates rápidos',
                schema: 'Normalizado (3NF)',
                examples: ['ERP', 'CRM', 'E-commerce']
            },
            OLAP: {
                purpose: 'Análisis y reporting',
                queries: 'Complejas, millones de registros',
                optimization: 'Lectura rápida, agregaciones',
                schema: 'Desnormalizado (Star/Snowflake)',
                examples: ['Data Warehouse', 'BI Tools', 'Analytics']
            }
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'dwh_1',
            title: 'Misión 1: Star Schema',
            description: `
                <p><strong>Cliente: DataVault Analytics</strong></p>
                <p>El <strong>Star Schema</strong> es el patrón más común en Data Warehousing.</p>
                <p>Tiene una tabla de <strong>hechos (fact)</strong> central rodeada de <strong>dimensiones</strong>.</p>
                <div class="schema-preview">
                    <h4>Fact Table: ${STAR_SCHEMA.factTable.name}</h4>
                    <p>Columnas: ${STAR_SCHEMA.factTable.columns.map(c => c.name).join(', ')}</p>
                    <h4>Dimensiones:</h4>
                    <ul>
                        ${STAR_SCHEMA.dimensions.map(d => `<li>${d.name} (${d.rows.toLocaleString()} rows)</li>`).join('')}
                    </ul>
                </div>
                <p><strong>¿Cuántas dimensiones tiene este Star Schema?</strong></p>
            `,
            type: 'numeric',
            xp: 150,
            data: STAR_SCHEMA,
            validate: function(answer, data) {
                return Math.abs(answer - data.dimensions.length) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.dimensions.length; // 4
            }
        },
        {
            id: 'dwh_2',
            title: 'Misión 2: Snowflake Schema',
            description: `
                <p><strong>Cliente: DataVault Analytics</strong></p>
                <p>El <strong>Snowflake Schema</strong> normaliza las dimensiones en sub-tablas.</p>
                <div class="schema-comparison">
                    <div class="star">
                        <h4>Star Schema</h4>
                        <p>dim_producto: producto_id, nombre, <strong>categoria, subcategoria</strong>, marca</p>
                    </div>
                    <div class="snowflake">
                        <h4>Snowflake Schema</h4>
                        <p>dim_producto → dim_subcategoria → dim_categoria</p>
                    </div>
                </div>
                <p><strong>¿Cuál es la principal DESVENTAJA del Snowflake vs Star?</strong></p>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'a',
                    label: 'Requiere más JOINs en las queries',
                    description: 'Más tablas = más JOINs para obtener datos completos'
                },
                {
                    id: 'b',
                    label: 'Ocupa más espacio en disco',
                    description: 'La normalización aumenta el tamaño'
                },
                {
                    id: 'c',
                    label: 'Es más difícil de actualizar',
                    description: 'Los cambios son más complejos'
                },
                {
                    id: 'd',
                    label: 'No soporta agregaciones',
                    description: 'Las funciones SUM/AVG no funcionan'
                }
            ],
            validate: function(answer) {
                return answer === 'a';
            },
            correctAnswer: 'a',
            explanation: `
                <p><strong>Más JOINs</strong> es la principal desventaja:</p>
                <ul>
                    <li>Star: 1 JOIN para obtener categoría de producto</li>
                    <li>Snowflake: 3 JOINs (producto → subcategoria → categoria)</li>
                    <li>Más JOINs = queries más lentas</li>
                    <li>Pero Snowflake ahorra espacio (menos redundancia)</li>
                </ul>
                <p><strong>Trade-off:</strong> Velocidad (Star) vs Espacio (Snowflake)</p>
            `
        },
        {
            id: 'dwh_3',
            title: 'Misión 3: SCD Type 2',
            description: `
                <p><strong>Cliente: DataVault Analytics</strong></p>
                <p><strong>SCD Type 2</strong> (Slowly Changing Dimension) mantiene historial completo.</p>
                <p>Mira el historial de Ana García:</p>
                <div class="scd-table">
                    <table>
                        <tr><th>SK</th><th>ID</th><th>Nombre</th><th>Segmento</th><th>Valid From</th><th>Valid To</th><th>Current</th></tr>
                        ${SCD_DATA.sampleData.map(r => `
                            <tr>
                                <td>${r.sk_cliente}</td>
                                <td>${r.cliente_id}</td>
                                <td>${r.nombre}</td>
                                <td>${r.segmento}</td>
                                <td>${r.valid_from}</td>
                                <td>${r.valid_to}</td>
                                <td>${r.is_current}</td>
                            </tr>
                        `).join('')}
                    </table>
                </div>
                <p><strong>¿Cuántas veces ha cambiado de segmento Ana García?</strong></p>
            `,
            type: 'numeric',
            xp: 200,
            data: SCD_DATA,
            validate: function(answer, data) {
                // 3 registros = 2 cambios (Bronze→Silver, Silver→Gold)
                return Math.abs(answer - 2) < 0.5;
            },
            getCorrectAnswer: function() {
                return 2;
            }
        },
        {
            id: 'dwh_4',
            title: 'Misión 4: Tablas Agregadas',
            description: `
                <p><strong>Cliente: DataVault Analytics</strong></p>
                <p>Las <strong>tablas pre-agregadas</strong> mejoran el rendimiento dramáticamente.</p>
                <div class="performance-comparison">
                    <div class="before">
                        <h4>Sin Agregación</h4>
                        <p>Query sobre fact_ventas (5M rows)</p>
                        <p class="time bad">⏱️ ${AGGREGATION_DATA.baseQueryTime}</p>
                    </div>
                    <div class="after">
                        <h4>Con Tabla Agregada</h4>
                        <p>Query sobre agg_ventas_mensual (2,400 rows)</p>
                        <p class="time good">⏱️ ${AGGREGATION_DATA.aggregatedTable.queryTime}</p>
                    </div>
                </div>
                <p><strong>¿Cuántas veces más rápida es la query con agregación?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> 45 seg vs 0.1 seg. Divide el tiempo original entre el optimizado.
                </div>
            `,
            type: 'numeric',
            xp: 200,
            data: AGGREGATION_DATA,
            validate: function(answer) {
                // 45 / 0.1 = 450x más rápida
                return Math.abs(answer - 450) < 10;
            },
            getCorrectAnswer: function() {
                return 450;
            }
        },
        {
            id: 'dwh_5',
            title: 'Misión 5: OLAP vs OLTP',
            description: `
                <p><strong>Cliente: DataVault Analytics</strong></p>
                <p>El cliente quiere procesar una venta en tiempo real en su POS (punto de venta).</p>
                <p>Características del proceso:</p>
                <ul>
                    <li>Insertar 1 registro de venta</li>
                    <li>Actualizar inventario (1 registro)</li>
                    <li>Latencia máxima: 100ms</li>
                    <li>Miles de transacciones por hora</li>
                </ul>
                <p><strong>¿Qué tipo de sistema necesita?</strong></p>
            `,
            type: 'choice',
            xp: 225,
            choices: [
                {
                    id: 'oltp',
                    label: 'OLTP (Online Transaction Processing)',
                    description: 'Optimizado para transacciones individuales'
                },
                {
                    id: 'olap',
                    label: 'OLAP (Online Analytical Processing)',
                    description: 'Optimizado para análisis y reportes'
                },
                {
                    id: 'both',
                    label: 'Ambos en el mismo sistema',
                    description: 'Un solo sistema para todo'
                },
                {
                    id: 'nosql',
                    label: 'Base de datos NoSQL',
                    description: 'MongoDB o similar'
                }
            ],
            validate: function(answer) {
                return answer === 'oltp';
            },
            correctAnswer: 'oltp',
            explanation: `
                <p><strong>OLTP</strong> es correcto porque:</p>
                <ul>
                    <li><strong>Transacciones individuales:</strong> INSERT/UPDATE de pocos registros</li>
                    <li><strong>Baja latencia:</strong> < 100ms por operación</li>
                    <li><strong>Alta concurrencia:</strong> Miles de transacciones simultáneas</li>
                    <li><strong>Schema normalizado:</strong> Evita anomalías en updates</li>
                </ul>
                <p><strong>OLAP</strong> se usa para el Data Warehouse donde se analizan esas ventas después.</p>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 8: Data Warehousing',
            scenes: [
                {
                    id: 1,
                    content: `
                        Los datos operacionales no sirven para análisis.
                        Necesitas un <strong>Data Warehouse</strong>: optimizado para consultas analíticas.
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
                        "El Data Warehouse es donde los datos se convierten en insights.
                        Es el corazón de Business Intelligence."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Nuevo cliente: <strong>DataVault Analytics</strong>.
                        Necesitan diseñar su Data Warehouse desde cero."
                    `,
                    tutorial: {
                        title: 'Conceptos Clave DWH',
                        content: `
                            <ul>
                                <li><strong>Fact Table</strong>: Métricas del negocio (ventas, clicks)</li>
                                <li><strong>Dimension</strong>: Contexto (quién, qué, cuándo, dónde)</li>
                                <li><strong>Star Schema</strong>: Fact central + dimensiones</li>
                                <li><strong>Snowflake</strong>: Star con dims normalizadas</li>
                                <li><strong>SCD</strong>: Manejo de cambios históricos</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás a diseñar esquemas eficientes,
                        manejar historial con SCD, y optimizar queries con agregaciones."
                    `,
                    tutorial: {
                        title: 'OLTP vs OLAP',
                        content: `
                            <table class="comparison-table">
                                <tr><th></th><th>OLTP</th><th>OLAP</th></tr>
                                <tr><td>Propósito</td><td>Operaciones</td><td>Análisis</td></tr>
                                <tr><td>Queries</td><td>Simples</td><td>Complejas</td></tr>
                                <tr><td>Schema</td><td>Normalizado</td><td>Desnormalizado</td></tr>
                                <tr><td>Datos</td><td>Actuales</td><td>Históricos</td></tr>
                            </table>
                        `
                    }
                }
            ]
        },
        company: 'DataVault Analytics'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Count total tables in schema
     * @param {Object} schema
     * @returns {number}
     */
    function countTables(schema) {
        let count = 1; // Fact table
        count += schema.dimensions.length;
        return count;
    }

    /**
     * Calculate denormalization level
     * @param {Object} starSchema
     * @param {Object} snowflakeSchema
     * @returns {Object}
     */
    function compareDenormalization(starSchema, snowflakeSchema) {
        const starTables = countTables(starSchema);

        // Count snowflake tables recursively
        function countSnowflakeTables(dims) {
            let count = 0;
            dims.forEach(dim => {
                count++;
                if (dim.children) {
                    count += countSnowflakeTables(dim.children);
                }
            });
            return count;
        }

        const snowflakeTables = 1 + countSnowflakeTables(snowflakeSchema.dimensions);

        return {
            star: starTables,
            snowflake: snowflakeTables,
            additionalJoins: snowflakeTables - starTables
        };
    }

    /**
     * Calculate aggregation benefit
     * @param {number} baseTime - Base query time in seconds
     * @param {number} aggTime - Aggregated query time in seconds
     * @returns {Object}
     */
    function calculateAggregationBenefit(baseTime, aggTime) {
        return {
            speedup: baseTime / aggTime,
            percentImprovement: ((baseTime - aggTime) / baseTime * 100).toFixed(2)
        };
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(8, {
            missions: MISSIONS,
            story: STORY,
            data: {
                starSchema: STAR_SCHEMA,
                snowflakeSchema: SNOWFLAKE_SCHEMA,
                scdData: SCD_DATA,
                aggregationData: AGGREGATION_DATA,
                olapOltpData: OLAP_OLTP_DATA
            },
            helpers: {
                countTables,
                compareDenormalization,
                calculateAggregationBenefit
            }
        });
        console.log('[Module8] Data Warehousing module registered');
    }

    // Expose globally for backwards compatibility
    window.Module8 = {
        MISSIONS,
        STORY,
        STAR_SCHEMA,
        SNOWFLAKE_SCHEMA,
        SCD_DATA,
        AGGREGATION_DATA,
        OLAP_OLTP_DATA,
        countTables,
        compareDenormalization,
        calculateAggregationBenefit
    };

})();
