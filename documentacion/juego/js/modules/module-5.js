/**
 * Module 5: Databases - Data Engineer: The Game
 *
 * Missions covering database fundamentals:
 * - Schema design and relationships
 * - Normalization (1NF, 2NF, 3NF)
 * - Indexes and performance
 * - Transactions and ACID
 * - NoSQL vs SQL
 */

(function() {
    'use strict';

    // ==========================================
    // DATABASE DESIGN DATA
    // ==========================================

    // Example schemas for missions
    const SCHEMAS = {
        // Denormalized (bad) design
        denormalized: {
            orders: [
                { order_id: 1, customer_name: 'Ana García', customer_email: 'ana@email.com', customer_city: 'Madrid', product_name: 'Laptop', product_price: 1200, quantity: 1 },
                { order_id: 2, customer_name: 'Ana García', customer_email: 'ana@email.com', customer_city: 'Madrid', product_name: 'Mouse', product_price: 25, quantity: 2 },
                { order_id: 3, customer_name: 'Carlos López', customer_email: 'carlos@email.com', customer_city: 'Barcelona', product_name: 'Laptop', product_price: 1200, quantity: 1 },
                { order_id: 4, customer_name: 'Ana García', customer_email: 'ana_new@email.com', customer_city: 'Madrid', product_name: 'Keyboard', product_price: 80, quantity: 1 }
            ]
        },

        // Normalized (good) design
        normalized: {
            customers: [
                { customer_id: 1, name: 'Ana García', email: 'ana@email.com', city: 'Madrid' },
                { customer_id: 2, name: 'Carlos López', email: 'carlos@email.com', city: 'Barcelona' }
            ],
            products: [
                { product_id: 1, name: 'Laptop', price: 1200 },
                { product_id: 2, name: 'Mouse', price: 25 },
                { product_id: 3, name: 'Keyboard', price: 80 }
            ],
            orders: [
                { order_id: 1, customer_id: 1, product_id: 1, quantity: 1 },
                { order_id: 2, customer_id: 1, product_id: 2, quantity: 2 },
                { order_id: 3, customer_id: 2, product_id: 1, quantity: 1 },
                { order_id: 4, customer_id: 1, product_id: 3, quantity: 1 }
            ]
        }
    };

    // Index scenarios
    const INDEX_SCENARIOS = {
        table: 'ventas',
        rows: 10000000, // 10 million rows
        queries: [
            { type: 'SELECT', where: 'fecha', frequency: 'Alta (100/min)' },
            { type: 'SELECT', where: 'cliente_id', frequency: 'Alta (80/min)' },
            { type: 'SELECT', where: 'producto_id, fecha', frequency: 'Media (20/min)' },
            { type: 'INSERT', frequency: 'Baja (5/min)' }
        ],
        currentIndexes: ['PRIMARY KEY (id)'],
        suggestedIndexes: ['fecha', 'cliente_id', '(producto_id, fecha)']
    };

    // ACID scenarios
    const ACID_SCENARIOS = {
        transfer: {
            description: 'Transferencia bancaria de 1000€ de cuenta A a cuenta B',
            steps: [
                'BEGIN TRANSACTION',
                'UPDATE cuentas SET saldo = saldo - 1000 WHERE id = A',
                'UPDATE cuentas SET saldo = saldo + 1000 WHERE id = B',
                'COMMIT'
            ],
            failure_point: 'Después del paso 2, antes del paso 3'
        }
    };

    // NoSQL vs SQL comparison
    const NOSQL_COMPARISON = {
        useCases: [
            { scenario: 'Sistema bancario con transacciones', best: 'SQL', reason: 'ACID crítico' },
            { scenario: 'Catálogo de productos con atributos variables', best: 'NoSQL', reason: 'Schema flexible' },
            { scenario: 'Logs de aplicación en tiempo real', best: 'NoSQL', reason: 'Alto volumen de escritura' },
            { scenario: 'Reportes financieros con JOINs complejos', best: 'SQL', reason: 'Queries relacionales' },
            { scenario: 'Sesiones de usuario en web app', best: 'NoSQL', reason: 'Key-value rápido' }
        ]
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'db_1',
            title: 'Misión 1: Diseño de Esquema',
            description: `
                <p><strong>Cliente: DataVault Corp</strong></p>
                <p>Analiza esta tabla denormalizada:</p>
                <div class="schema-view">
                    <table class="mini-table">
                        <tr><th>order_id</th><th>customer_name</th><th>customer_email</th><th>product_name</th><th>quantity</th></tr>
                        <tr><td>1</td><td>Ana García</td><td>ana@email.com</td><td>Laptop</td><td>1</td></tr>
                        <tr><td>2</td><td>Ana García</td><td>ana@email.com</td><td>Mouse</td><td>2</td></tr>
                        <tr><td>3</td><td>Carlos López</td><td>carlos@email.com</td><td>Laptop</td><td>1</td></tr>
                    </table>
                </div>
                <p><strong>¿Cuántas tablas necesitas para normalizar correctamente este diseño?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Identifica las entidades: clientes, productos, pedidos...
                </div>
            `,
            type: 'numeric',
            xp: 150,
            data: SCHEMAS.denormalized,
            validate: function(answer) {
                // 3 tables: customers, products, orders
                return Math.abs(answer - 3) < 0.5;
            },
            getCorrectAnswer: function() {
                return 3;
            }
        },
        {
            id: 'db_2',
            title: 'Misión 2: Normalización',
            description: `
                <p><strong>Cliente: DataVault Corp</strong></p>
                <p>En la tabla anterior, Ana García aparece con dos emails diferentes:</p>
                <ul>
                    <li>Pedido 1-2: ana@email.com</li>
                    <li>Pedido 4: ana_new@email.com</li>
                </ul>
                <p><strong>¿Qué problema de normalización representa esto?</strong></p>
            `,
            type: 'choice',
            xp: 150,
            choices: [
                {
                    id: 'redundancy',
                    label: 'Redundancia de datos',
                    description: 'Datos duplicados en múltiples filas'
                },
                {
                    id: 'anomaly',
                    label: 'Anomalía de actualización',
                    description: 'Inconsistencia al modificar datos'
                },
                {
                    id: 'dependency',
                    label: 'Dependencia transitiva',
                    description: 'Columnas que dependen de otras no-clave'
                },
                {
                    id: 'null',
                    label: 'Valores nulos',
                    description: 'Campos vacíos innecesarios'
                }
            ],
            validate: function(answer) {
                return answer === 'anomaly';
            },
            correctAnswer: 'anomaly',
            explanation: `
                <p><strong>Anomalía de actualización:</strong></p>
                <p>Cuando Ana cambió su email, solo se actualizó en algunos registros,
                creando inconsistencia. En un esquema normalizado, el email estaría
                en una sola fila de la tabla "clientes".</p>
            `
        },
        {
            id: 'db_3',
            title: 'Misión 3: Índices y Performance',
            description: `
                <p><strong>Cliente: DataVault Corp</strong></p>
                <p>Tienes una tabla "ventas" con <strong>10 millones</strong> de registros.</p>
                <p>Esta query tarda 45 segundos:</p>
                <div class="code-block">
                    <code>SELECT * FROM ventas WHERE fecha = '2024-01-15';</code>
                </div>
                <p><strong>¿Qué acción mejoraría más el rendimiento?</strong></p>
            `,
            type: 'choice',
            xp: 175,
            data: INDEX_SCENARIOS,
            choices: [
                {
                    id: 'more_ram',
                    label: 'Añadir más RAM al servidor',
                    description: 'Incrementar memoria disponible'
                },
                {
                    id: 'index',
                    label: 'Crear índice en columna "fecha"',
                    description: 'CREATE INDEX idx_fecha ON ventas(fecha)'
                },
                {
                    id: 'partition',
                    label: 'Particionar la tabla',
                    description: 'Dividir en subtablas por rango'
                },
                {
                    id: 'cache',
                    label: 'Implementar cache',
                    description: 'Guardar resultados en memoria'
                }
            ],
            validate: function(answer) {
                return answer === 'index';
            },
            correctAnswer: 'index',
            explanation: `
                <p><strong>Crear un índice</strong> es la solución correcta porque:</p>
                <ul>
                    <li>Sin índice: escaneo completo de 10M de filas (Full Table Scan)</li>
                    <li>Con índice: búsqueda directa O(log n)</li>
                    <li>Mejora típica: de 45s a < 1 segundo</li>
                </ul>
                <p>Particionamiento y cache son buenas opciones secundarias.</p>
            `
        },
        {
            id: 'db_4',
            title: 'Misión 4: Transacciones ACID',
            description: `
                <p><strong>Cliente: DataVault Corp</strong></p>
                <p>Una transferencia bancaria ejecuta estos pasos:</p>
                <ol>
                    <li>BEGIN TRANSACTION</li>
                    <li>Restar 1000€ de cuenta A</li>
                    <li>Sumar 1000€ a cuenta B</li>
                    <li>COMMIT</li>
                </ol>
                <p>Si el sistema falla <strong>después del paso 2</strong> pero <strong>antes del paso 3</strong>,
                ¿qué propiedad ACID garantiza que no se pierda dinero?</p>
            `,
            type: 'choice',
            xp: 200,
            data: ACID_SCENARIOS.transfer,
            choices: [
                {
                    id: 'atomicity',
                    label: 'Atomicity (Atomicidad)',
                    description: 'Todo o nada - la transacción completa o se revierte'
                },
                {
                    id: 'consistency',
                    label: 'Consistency (Consistencia)',
                    description: 'Los datos cumplen todas las reglas'
                },
                {
                    id: 'isolation',
                    label: 'Isolation (Aislamiento)',
                    description: 'Transacciones no interfieren entre sí'
                },
                {
                    id: 'durability',
                    label: 'Durability (Durabilidad)',
                    description: 'Los cambios confirmados persisten'
                }
            ],
            validate: function(answer) {
                return answer === 'atomicity';
            },
            correctAnswer: 'atomicity',
            explanation: `
                <p><strong>Atomicidad</strong> garantiza que:</p>
                <ul>
                    <li>La transacción es "todo o nada"</li>
                    <li>Si falla antes del COMMIT, se hace ROLLBACK</li>
                    <li>Los 1000€ vuelven a la cuenta A automáticamente</li>
                    <li>No hay estado intermedio inconsistente</li>
                </ul>
            `
        },
        {
            id: 'db_5',
            title: 'Misión 5: SQL vs NoSQL',
            description: `
                <p><strong>Cliente: DataVault Corp</strong></p>
                <p>Un e-commerce necesita almacenar productos con atributos muy diferentes:</p>
                <ul>
                    <li><strong>Laptops:</strong> RAM, CPU, pantalla, peso...</li>
                    <li><strong>Camisetas:</strong> talla, color, material...</li>
                    <li><strong>Libros:</strong> autor, ISBN, páginas...</li>
                </ul>
                <p><strong>¿Qué tipo de base de datos es más adecuada?</strong></p>
            `,
            type: 'choice',
            xp: 200,
            data: NOSQL_COMPARISON,
            choices: [
                {
                    id: 'sql',
                    label: 'SQL Relacional (PostgreSQL)',
                    description: 'Tablas con esquema fijo'
                },
                {
                    id: 'document',
                    label: 'NoSQL Documental (MongoDB)',
                    description: 'Documentos JSON flexibles'
                },
                {
                    id: 'keyvalue',
                    label: 'NoSQL Key-Value (Redis)',
                    description: 'Pares clave-valor simples'
                },
                {
                    id: 'graph',
                    label: 'NoSQL Grafo (Neo4j)',
                    description: 'Nodos y relaciones'
                }
            ],
            validate: function(answer) {
                return answer === 'document';
            },
            correctAnswer: 'document',
            explanation: `
                <p><strong>NoSQL Documental</strong> es ideal porque:</p>
                <ul>
                    <li>Cada producto puede tener atributos diferentes</li>
                    <li>No necesitas modificar el esquema para nuevos tipos</li>
                    <li>JSON permite estructuras anidadas flexibles</li>
                </ul>
                <p>En SQL necesitarías: tabla por tipo de producto o columnas opcionales (ineficiente).</p>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 5: Bases de Datos',
            scenes: [
                {
                    id: 1,
                    content: `
                        Has aprendido a consultar bases de datos con SQL.
                        Ahora es momento de entender cómo <strong>diseñarlas</strong>.
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
                        "Un buen diseño de base de datos es la diferencia entre
                        un sistema que funciona y uno que colapsa bajo presión."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Nuestro cliente <strong>DataVault Corp</strong> necesita
                        rediseñar su base de datos. Está llena de problemas."
                    `,
                    tutorial: {
                        title: '¿Por qué importa el diseño?',
                        content: `
                            <ul>
                                <li><strong>Performance:</strong> Queries rápidas vs lentas</li>
                                <li><strong>Integridad:</strong> Datos consistentes</li>
                                <li><strong>Escalabilidad:</strong> Crecer sin problemas</li>
                                <li><strong>Mantenimiento:</strong> Fácil de actualizar</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás normalización, índices, transacciones,
                        y cuándo usar SQL vs NoSQL."
                    `,
                    tutorial: {
                        title: 'Conceptos Clave',
                        content: `
                            <ul>
                                <li><strong>Normalización:</strong> Eliminar redundancia</li>
                                <li><strong>Índices:</strong> Acelerar búsquedas</li>
                                <li><strong>ACID:</strong> Garantías de transacciones</li>
                                <li><strong>NoSQL:</strong> Alternativas para casos específicos</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'DataVault Corp'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Check if a schema is in a specific normal form
     */
    function checkNormalForm(schema, form) {
        // Simplified check - in real scenario would be more complex
        switch (form) {
            case '1NF':
                // All columns atomic
                return true;
            case '2NF':
                // 1NF + no partial dependencies
                return schema.tables && schema.tables.length >= 2;
            case '3NF':
                // 2NF + no transitive dependencies
                return schema.tables && schema.tables.length >= 3;
            default:
                return false;
        }
    }

    /**
     * Estimate query performance improvement with index
     */
    function estimateIndexImprovement(rowCount, selectivity) {
        // Without index: O(n) full scan
        const withoutIndex = rowCount;
        // With index: O(log n) + selectivity * n
        const withIndex = Math.log2(rowCount) + (selectivity * rowCount);
        return {
            withoutIndex,
            withIndex,
            improvement: Math.round((1 - withIndex / withoutIndex) * 100)
        };
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(5, {
            missions: MISSIONS,
            story: STORY,
            schemas: SCHEMAS,
            indexScenarios: INDEX_SCENARIOS,
            acidScenarios: ACID_SCENARIOS,
            nosqlComparison: NOSQL_COMPARISON,
            helpers: {
                checkNormalForm,
                estimateIndexImprovement
            }
        });
        console.log('[Module5] Databases module registered');
    }

    // Expose globally
    window.Module5 = {
        MISSIONS,
        STORY,
        SCHEMAS,
        INDEX_SCENARIOS,
        ACID_SCENARIOS,
        NOSQL_COMPARISON,
        checkNormalForm,
        estimateIndexImprovement
    };

})();
