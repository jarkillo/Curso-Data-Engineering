/**
 * Module 9: Apache Spark - Data Engineer: The Game
 *
 * Missions covering Spark fundamentals:
 * - DataFrames and basic operations
 * - Transformations (map, filter, groupBy)
 * - Joins (broadcast, shuffle)
 * - Optimization (partitioning, caching)
 * - Structured Streaming basics
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE SPARK DATA FOR MISSIONS
    // ==========================================

    // DataFrame example
    const DATAFRAME_DATA = {
        ventas: [
            { id: 1, producto: 'Laptop', cantidad: 5, precio: 1200.00, fecha: '2024-01-15' },
            { id: 2, producto: 'Mouse', cantidad: 50, precio: 25.00, fecha: '2024-01-15' },
            { id: 3, producto: 'Teclado', cantidad: 30, precio: 75.00, fecha: '2024-01-16' },
            { id: 4, producto: 'Monitor', cantidad: 10, precio: 350.00, fecha: '2024-01-16' },
            { id: 5, producto: 'Laptop', cantidad: 3, precio: 1200.00, fecha: '2024-01-17' }
        ],
        schema: {
            columns: ['id', 'producto', 'cantidad', 'precio', 'fecha'],
            types: ['INT', 'STRING', 'INT', 'DOUBLE', 'DATE']
        }
    };

    // Transformation examples
    const TRANSFORMATION_DATA = {
        operations: [
            {
                name: 'filter',
                description: 'Filtra filas que cumplen condición',
                example: 'df.filter(col("cantidad") > 10)',
                type: 'narrow'
            },
            {
                name: 'select',
                description: 'Selecciona columnas específicas',
                example: 'df.select("producto", "cantidad")',
                type: 'narrow'
            },
            {
                name: 'groupBy',
                description: 'Agrupa por columna(s)',
                example: 'df.groupBy("producto").sum("cantidad")',
                type: 'wide'
            },
            {
                name: 'orderBy',
                description: 'Ordena por columna(s)',
                example: 'df.orderBy(col("precio").desc())',
                type: 'wide'
            }
        ],
        narrowVsWide: {
            narrow: {
                description: 'No requiere shuffle de datos entre particiones',
                examples: ['filter', 'select', 'map', 'flatMap'],
                performance: 'Rápido'
            },
            wide: {
                description: 'Requiere shuffle (redistribución de datos)',
                examples: ['groupBy', 'orderBy', 'join', 'distinct'],
                performance: 'Costoso'
            }
        }
    };

    // Join examples
    const JOIN_DATA = {
        ventas: {
            name: 'ventas_df',
            rows: 10000000,
            columns: ['venta_id', 'producto_id', 'cantidad', 'total']
        },
        productos: {
            name: 'productos_df',
            rows: 5000,
            columns: ['producto_id', 'nombre', 'categoria', 'precio']
        },
        joinTypes: [
            {
                type: 'Shuffle Join',
                description: 'Ambos DataFrames se redistribuyen por la key',
                useCase: 'Cuando ambos son grandes',
                cost: 'Alto (shuffle de ambos lados)'
            },
            {
                type: 'Broadcast Join',
                description: 'El DF pequeño se envía a todos los workers',
                useCase: 'Cuando uno es pequeño (< 10MB por defecto)',
                cost: 'Bajo (sin shuffle del DF grande)'
            },
            {
                type: 'Sort-Merge Join',
                description: 'Ambos se ordenan y luego se mergean',
                useCase: 'Cuando ambos son grandes y ordenados',
                cost: 'Medio'
            }
        ]
    };

    // Optimization data
    const OPTIMIZATION_DATA = {
        partitioning: {
            before: {
                partitions: 200,
                dataSize: '10 GB',
                partitionSize: '50 MB cada una',
                problem: 'Muchas particiones pequeñas = overhead'
            },
            after: {
                partitions: 50,
                dataSize: '10 GB',
                partitionSize: '200 MB cada una',
                benefit: 'Menos overhead, mejor paralelismo'
            },
            rule: 'Particiones de 100-200 MB idealmente'
        },
        caching: {
            levels: [
                { name: 'MEMORY_ONLY', description: 'Solo RAM, se recalcula si no cabe' },
                { name: 'MEMORY_AND_DISK', description: 'RAM primero, disco si no cabe' },
                { name: 'DISK_ONLY', description: 'Solo disco' },
                { name: 'MEMORY_ONLY_SER', description: 'RAM serializado (menos espacio, más CPU)' }
            ],
            scenario: {
                withoutCache: {
                    query1Time: 120, // seconds
                    query2Time: 120,
                    query3Time: 120,
                    totalTime: 360
                },
                withCache: {
                    query1Time: 120, // First query still slow
                    query2Time: 5,   // Cached!
                    query3Time: 5,
                    totalTime: 130
                }
            }
        }
    };

    // Streaming data
    const STREAMING_DATA = {
        example: {
            source: 'Kafka topic: user_events',
            eventsPerSecond: 10000,
            schema: ['user_id', 'event_type', 'timestamp', 'properties']
        },
        triggerModes: [
            {
                mode: 'ProcessingTime("10 seconds")',
                description: 'Micro-batch cada 10 segundos'
            },
            {
                mode: 'Continuous("1 second")',
                description: 'Procesamiento continuo con checkpoint cada 1s'
            },
            {
                mode: 'Once()',
                description: 'Procesa todo lo disponible y termina'
            }
        ],
        watermark: {
            description: 'Maneja datos que llegan tarde (late data)',
            example: 'withWatermark("timestamp", "10 minutes")',
            behavior: 'Acepta eventos hasta 10 min después de su timestamp'
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'spark_1',
            title: 'Misión 1: DataFrames Básicos',
            description: `
                <p><strong>Cliente: SparkMaster Inc</strong></p>
                <p>Los <strong>DataFrames</strong> de Spark son colecciones distribuidas con schema.</p>
                <p>Tienes este DataFrame de ventas:</p>
                <div class="dataframe-preview">
                    <table>
                        <tr><th>id</th><th>producto</th><th>cantidad</th><th>precio</th><th>fecha</th></tr>
                        ${DATAFRAME_DATA.ventas.map(r => `
                            <tr><td>${r.id}</td><td>${r.producto}</td><td>${r.cantidad}</td><td>$${r.precio}</td><td>${r.fecha}</td></tr>
                        `).join('')}
                    </table>
                </div>
                <p><strong>¿Cuál es el total de unidades vendidas de "Laptop"?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Filtra por producto="Laptop" y suma las cantidades.
                </div>
            `,
            type: 'numeric',
            xp: 175,
            data: DATAFRAME_DATA,
            validate: function(answer, data) {
                const total = data.ventas
                    .filter(v => v.producto === 'Laptop')
                    .reduce((sum, v) => sum + v.cantidad, 0);
                return Math.abs(answer - total) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.ventas
                    .filter(v => v.producto === 'Laptop')
                    .reduce((sum, v) => sum + v.cantidad, 0); // 8
            }
        },
        {
            id: 'spark_2',
            title: 'Misión 2: Transformaciones',
            description: `
                <p><strong>Cliente: SparkMaster Inc</strong></p>
                <p>Spark divide las transformaciones en <strong>Narrow</strong> y <strong>Wide</strong>.</p>
                <div class="transformation-types">
                    <div class="narrow">
                        <h4>Narrow (Sin shuffle)</h4>
                        <p>Cada partición de salida depende de una partición de entrada</p>
                        <p>Ejemplos: filter, select, map</p>
                    </div>
                    <div class="wide">
                        <h4>Wide (Con shuffle)</h4>
                        <p>Cada partición de salida puede depender de múltiples de entrada</p>
                        <p>Ejemplos: groupBy, orderBy, join</p>
                    </div>
                </div>
                <p><strong>¿Qué tipo de transformación es <code>groupBy().sum()</code>?</strong></p>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'narrow',
                    label: 'Narrow Transformation',
                    description: 'No requiere shuffle de datos'
                },
                {
                    id: 'wide',
                    label: 'Wide Transformation',
                    description: 'Requiere shuffle de datos entre particiones'
                },
                {
                    id: 'action',
                    label: 'Action (no transformation)',
                    description: 'Es una acción, no una transformación'
                },
                {
                    id: 'lazy',
                    label: 'Lazy Transformation',
                    description: 'Transformación perezosa'
                }
            ],
            validate: function(answer) {
                return answer === 'wide';
            },
            correctAnswer: 'wide',
            explanation: `
                <p><strong>Wide Transformation</strong> porque:</p>
                <ul>
                    <li><code>groupBy</code> necesita agrupar datos por key</li>
                    <li>Los datos con la misma key pueden estar en diferentes particiones</li>
                    <li>Spark debe hacer <strong>shuffle</strong> para juntar los datos</li>
                    <li>El shuffle es la operación más costosa en Spark</li>
                </ul>
            `
        },
        {
            id: 'spark_3',
            title: 'Misión 3: Broadcast Join',
            description: `
                <p><strong>Cliente: SparkMaster Inc</strong></p>
                <p>Tienes dos DataFrames para hacer JOIN:</p>
                <div class="join-scenario">
                    <div class="df-large">
                        <h4>ventas_df</h4>
                        <p><strong>10 millones</strong> de filas</p>
                        <p>Columnas: venta_id, producto_id, cantidad</p>
                    </div>
                    <div class="df-small">
                        <h4>productos_df</h4>
                        <p><strong>5,000</strong> filas (~500 KB)</p>
                        <p>Columnas: producto_id, nombre, categoria</p>
                    </div>
                </div>
                <p><strong>¿Qué tipo de JOIN debería usar Spark automáticamente?</strong></p>
            `,
            type: 'choice',
            xp: 200,
            choices: [
                {
                    id: 'shuffle',
                    label: 'Shuffle Join',
                    description: 'Redistribuye ambos DataFrames por la key'
                },
                {
                    id: 'broadcast',
                    label: 'Broadcast Join',
                    description: 'Envía el DF pequeño a todos los workers'
                },
                {
                    id: 'sortmerge',
                    label: 'Sort-Merge Join',
                    description: 'Ordena ambos y luego mergea'
                },
                {
                    id: 'nested',
                    label: 'Nested Loop Join',
                    description: 'Compara cada fila con todas las otras'
                }
            ],
            validate: function(answer) {
                return answer === 'broadcast';
            },
            correctAnswer: 'broadcast',
            explanation: `
                <p><strong>Broadcast Join</strong> es óptimo aquí porque:</p>
                <ul>
                    <li>productos_df es pequeño (~500 KB << 10 MB threshold)</li>
                    <li>Se envía a todos los workers una sola vez</li>
                    <li>ventas_df no se mueve (sin shuffle)</li>
                    <li><strong>Mucho más rápido</strong> que shuffle join</li>
                </ul>
                <p>Puedes forzarlo: <code>broadcast(productos_df)</code></p>
            `
        },
        {
            id: 'spark_4',
            title: 'Misión 4: Caching y Particiones',
            description: `
                <p><strong>Cliente: SparkMaster Inc</strong></p>
                <p>Ejecutas 3 queries sobre el mismo DataFrame (sin cache):</p>
                <div class="cache-scenario">
                    <table>
                        <tr><th>Query</th><th>Sin Cache</th><th>Con Cache</th></tr>
                        <tr><td>Query 1</td><td>120 seg</td><td>120 seg</td></tr>
                        <tr><td>Query 2</td><td>120 seg</td><td>5 seg</td></tr>
                        <tr><td>Query 3</td><td>120 seg</td><td>5 seg</td></tr>
                        <tr class="total"><td><strong>Total</strong></td><td><strong>360 seg</strong></td><td><strong>130 seg</strong></td></tr>
                    </table>
                </div>
                <p><strong>¿Cuántos segundos ahorra el caching en este escenario?</strong></p>
            `,
            type: 'numeric',
            xp: 225,
            data: OPTIMIZATION_DATA.caching,
            validate: function(answer, data) {
                const savings = data.scenario.withoutCache.totalTime - data.scenario.withCache.totalTime;
                return Math.abs(answer - savings) < 5;
            },
            getCorrectAnswer: function(data) {
                return data.scenario.withoutCache.totalTime - data.scenario.withCache.totalTime; // 230
            }
        },
        {
            id: 'spark_5',
            title: 'Misión 5: Structured Streaming',
            description: `
                <p><strong>Cliente: SparkMaster Inc</strong></p>
                <p>Tienes un stream de Kafka con 10,000 eventos/segundo.</p>
                <p>Algunos eventos llegan tarde (hasta 15 minutos de delay).</p>
                <div class="streaming-config">
                    <pre>
df = spark.readStream.format("kafka")
    .option("subscribe", "user_events")
    .load()

# ¿Qué watermark configurarías?
df.withWatermark("timestamp", "???")
    .groupBy(window("timestamp", "5 minutes"), "event_type")
    .count()
                    </pre>
                </div>
                <p><strong>¿Qué valor de watermark usarías para no perder datos tardíos?</strong></p>
            `,
            type: 'choice',
            xp: 250,
            choices: [
                {
                    id: 'a',
                    label: '5 minutes',
                    description: 'Acepta eventos hasta 5 min tarde'
                },
                {
                    id: 'b',
                    label: '15 minutes',
                    description: 'Acepta eventos hasta 15 min tarde'
                },
                {
                    id: 'c',
                    label: '1 hour',
                    description: 'Acepta eventos hasta 1 hora tarde'
                },
                {
                    id: 'd',
                    label: '0 minutes',
                    description: 'No acepta eventos tardíos'
                }
            ],
            validate: function(answer) {
                return answer === 'b';
            },
            correctAnswer: 'b',
            explanation: `
                <p><strong>15 minutes</strong> es correcto porque:</p>
                <ul>
                    <li>El enunciado dice que eventos llegan hasta 15 min tarde</li>
                    <li>El watermark debe ser >= al máximo delay esperado</li>
                    <li>Más grande = más memoria (guarda más estado)</li>
                    <li>Más pequeño = pierde datos tardíos</li>
                </ul>
                <p><strong>Trade-off:</strong> Latencia vs Completitud</p>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 9: Apache Spark',
            scenes: [
                {
                    id: 1,
                    content: `
                        Cuando los datos no caben en una máquina, necesitas
                        <strong>procesamiento distribuido</strong>. Apache Spark es el líder.
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
                        "Spark puede procesar petabytes de datos.
                        Es 100x más rápido que MapReduce tradicional."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Nuevo cliente: <strong>SparkMaster Inc</strong>.
                        Procesan 50 TB de datos diarios y necesitan optimizar."
                    `,
                    tutorial: {
                        title: 'Conceptos Clave Spark',
                        content: `
                            <ul>
                                <li><strong>DataFrame</strong>: Tabla distribuida con schema</li>
                                <li><strong>Transformation</strong>: Operación lazy (map, filter)</li>
                                <li><strong>Action</strong>: Ejecuta el plan (collect, count)</li>
                                <li><strong>Partition</strong>: Chunk de datos en un worker</li>
                                <li><strong>Shuffle</strong>: Redistribución de datos (costoso)</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás DataFrames, transformaciones, JOINs optimizados,
                        caching y Structured Streaming."
                    `,
                    tutorial: {
                        title: 'Lazy Evaluation',
                        content: `
                            <p>Spark NO ejecuta transformaciones inmediatamente:</p>
                            <pre>
# Esto NO ejecuta nada aún
df2 = df.filter(...)
df3 = df2.groupBy(...)

# AHORA ejecuta todo el plan
df3.count()  # Action!
                            </pre>
                            <p>Permite optimizar el plan completo antes de ejecutar.</p>
                        `
                    }
                }
            ]
        },
        company: 'SparkMaster Inc'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Simulate DataFrame operations
     * @param {Array} data
     * @param {string} operation
     * @param {Object} params
     * @returns {Array}
     */
    function simulateDataFrameOp(data, operation, params) {
        switch (operation) {
            case 'filter':
                return data.filter(row => {
                    const value = row[params.column];
                    switch (params.operator) {
                        case '>': return value > params.value;
                        case '<': return value < params.value;
                        case '=': return value === params.value;
                        default: return true;
                    }
                });
            case 'select':
                return data.map(row => {
                    const newRow = {};
                    params.columns.forEach(col => {
                        newRow[col] = row[col];
                    });
                    return newRow;
                });
            case 'groupBy':
                const groups = {};
                data.forEach(row => {
                    const key = row[params.column];
                    if (!groups[key]) {
                        groups[key] = [];
                    }
                    groups[key].push(row);
                });
                return groups;
            default:
                return data;
        }
    }

    /**
     * Calculate partition recommendation
     * @param {number} dataSizeGB
     * @param {number} targetPartitionMB
     * @returns {number}
     */
    function calculateOptimalPartitions(dataSizeGB, targetPartitionMB = 128) {
        const dataSizeMB = dataSizeGB * 1024;
        return Math.ceil(dataSizeMB / targetPartitionMB);
    }

    /**
     * Estimate join type based on DataFrame sizes
     * @param {number} leftRows
     * @param {number} rightRows
     * @param {number} broadcastThresholdMB
     * @returns {string}
     */
    function estimateJoinType(leftRows, rightRows, broadcastThresholdMB = 10) {
        const estimatedSizeMB = Math.min(leftRows, rightRows) * 0.0001; // Rough estimate

        if (estimatedSizeMB < broadcastThresholdMB) {
            return 'Broadcast Join';
        }
        return 'Shuffle Join';
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(9, {
            missions: MISSIONS,
            story: STORY,
            data: {
                dataframe: DATAFRAME_DATA,
                transformation: TRANSFORMATION_DATA,
                join: JOIN_DATA,
                optimization: OPTIMIZATION_DATA,
                streaming: STREAMING_DATA
            },
            helpers: {
                simulateDataFrameOp,
                calculateOptimalPartitions,
                estimateJoinType
            }
        });
        console.log('[Module9] Spark module registered');
    }

    // Expose globally for backwards compatibility
    window.Module9 = {
        MISSIONS,
        STORY,
        DATAFRAME_DATA,
        TRANSFORMATION_DATA,
        JOIN_DATA,
        OPTIMIZATION_DATA,
        STREAMING_DATA,
        simulateDataFrameOp,
        calculateOptimalPartitions,
        estimateJoinType
    };

})();
