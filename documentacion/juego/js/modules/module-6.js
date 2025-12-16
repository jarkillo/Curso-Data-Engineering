/**
 * Module 6: Airflow - Data Engineer: The Game
 *
 * Missions covering Airflow fundamentals:
 * - DAG basics and structure
 * - Operators (Python, Bash, SQL)
 * - Scheduling with cron expressions
 * - XComs for task communication
 * - Error handling and retries
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE DAG DATA FOR AIRFLOW MISSIONS
    // ==========================================

    // Example DAG structures
    const DAG_DATA = {
        // Simple ETL DAG
        etl_dag: {
            dag_id: 'etl_ventas_diario',
            schedule: '0 6 * * *',
            description: 'ETL diario de ventas',
            tasks: [
                { id: 'extract_csv', operator: 'PythonOperator', upstream: [] },
                { id: 'validate_data', operator: 'PythonOperator', upstream: ['extract_csv'] },
                { id: 'transform_data', operator: 'PythonOperator', upstream: ['validate_data'] },
                { id: 'load_warehouse', operator: 'PostgresOperator', upstream: ['transform_data'] },
                { id: 'send_notification', operator: 'EmailOperator', upstream: ['load_warehouse'] }
            ]
        },

        // Complex DAG with branches
        complex_dag: {
            dag_id: 'proceso_datos_cliente',
            schedule: '0 8 * * 1-5',
            tasks: [
                { id: 'start', operator: 'DummyOperator', upstream: [] },
                { id: 'check_source', operator: 'BranchPythonOperator', upstream: ['start'] },
                { id: 'process_api', operator: 'PythonOperator', upstream: ['check_source'] },
                { id: 'process_file', operator: 'PythonOperator', upstream: ['check_source'] },
                { id: 'merge_data', operator: 'PythonOperator', upstream: ['process_api', 'process_file'] },
                { id: 'quality_check', operator: 'PythonOperator', upstream: ['merge_data'] },
                { id: 'end', operator: 'DummyOperator', upstream: ['quality_check'] }
            ]
        },

        // Failing DAG example
        failing_dag: {
            dag_id: 'dag_con_errores',
            tasks: [
                { id: 'task_a', status: 'success', retries: 0 },
                { id: 'task_b', status: 'success', retries: 1 },
                { id: 'task_c', status: 'failed', retries: 3, error: 'ConnectionError: Database unavailable' },
                { id: 'task_d', status: 'upstream_failed', retries: 0 }
            ]
        }
    };

    // Cron expressions reference
    const CRON_EXPRESSIONS = {
        '0 0 * * *': 'Cada día a medianoche',
        '0 6 * * *': 'Cada día a las 6:00 AM',
        '*/15 * * * *': 'Cada 15 minutos',
        '0 8 * * 1-5': 'Lunes a viernes a las 8:00 AM',
        '0 0 1 * *': 'Primer día de cada mes a medianoche',
        '0 12 * * 0': 'Cada domingo a las 12:00 PM'
    };

    // Operator types
    const OPERATORS = {
        PythonOperator: {
            name: 'PythonOperator',
            description: 'Ejecuta una función Python',
            example: `
PythonOperator(
    task_id='process_data',
    python_callable=my_function,
    op_kwargs={'param': 'value'}
)`
        },
        BashOperator: {
            name: 'BashOperator',
            description: 'Ejecuta un comando bash',
            example: `
BashOperator(
    task_id='run_script',
    bash_command='python /scripts/process.py'
)`
        },
        PostgresOperator: {
            name: 'PostgresOperator',
            description: 'Ejecuta SQL en PostgreSQL',
            example: `
PostgresOperator(
    task_id='load_data',
    postgres_conn_id='my_postgres',
    sql='INSERT INTO table SELECT * FROM staging;'
)`
        },
        EmailOperator: {
            name: 'EmailOperator',
            description: 'Envía un email',
            example: `
EmailOperator(
    task_id='send_alert',
    to='team@company.com',
    subject='Pipeline completado'
)`
        },
        BranchPythonOperator: {
            name: 'BranchPythonOperator',
            description: 'Decide qué rama ejecutar',
            example: `
BranchPythonOperator(
    task_id='check_condition',
    python_callable=decide_branch
)`
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'airflow_1',
            title: 'Misión 1: Tu Primer DAG',
            description: `
                <p><strong>Cliente: AirPipeline Corp</strong></p>
                <p>Apache Airflow organiza los pipelines como <strong>DAGs</strong> (Directed Acyclic Graphs).</p>
                <p>Analiza este DAG de ETL diario:</p>
                <div class="dag-preview">
                    <pre>${JSON.stringify(DAG_DATA.etl_dag, null, 2)}</pre>
                </div>
                <p><strong>¿Cuántas tareas (tasks) tiene este DAG?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Cuenta los elementos en el array "tasks".
                </div>
            `,
            type: 'numeric',
            xp: 150,
            data: DAG_DATA.etl_dag,
            validate: function(answer, data) {
                return Math.abs(answer - data.tasks.length) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.tasks.length; // 5
            }
        },
        {
            id: 'airflow_2',
            title: 'Misión 2: Operadores',
            description: `
                <p><strong>Cliente: AirPipeline Corp</strong></p>
                <p>Airflow usa <strong>Operadores</strong> para definir qué hace cada tarea.</p>
                <p>Necesitas ejecutar un script de Python que procesa datos de ventas.</p>
                <p><strong>¿Qué operador usarías?</strong></p>
            `,
            type: 'choice',
            xp: 150,
            choices: [
                {
                    id: 'python',
                    label: 'PythonOperator',
                    description: 'Ejecuta una función Python directamente'
                },
                {
                    id: 'bash',
                    label: 'BashOperator',
                    description: 'Ejecuta un comando en terminal'
                },
                {
                    id: 'postgres',
                    label: 'PostgresOperator',
                    description: 'Ejecuta queries SQL en PostgreSQL'
                },
                {
                    id: 'email',
                    label: 'EmailOperator',
                    description: 'Envía notificaciones por email'
                }
            ],
            validate: function(answer) {
                return answer === 'python';
            },
            correctAnswer: 'python',
            explanation: `
                <p><strong>PythonOperator</strong> es la mejor opción porque:</p>
                <ul>
                    <li>Ejecuta funciones Python directamente</li>
                    <li>Permite pasar argumentos con <code>op_kwargs</code></li>
                    <li>Integra naturalmente con el código Python existente</li>
                    <li>Facilita el debugging y testing</li>
                </ul>
            `
        },
        {
            id: 'airflow_3',
            title: 'Misión 3: Scheduling con Cron',
            description: `
                <p><strong>Cliente: AirPipeline Corp</strong></p>
                <p>Airflow usa expresiones <strong>cron</strong> para programar DAGs.</p>
                <p>El cliente necesita un pipeline que se ejecute:</p>
                <div class="requirement-box">
                    <ul>
                        <li>De Lunes a Viernes</li>
                        <li>A las 8:00 AM</li>
                    </ul>
                </div>
                <p><strong>¿Cuál es la expresión cron correcta?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Formato cron:</strong> minuto hora día_mes mes día_semana<br>
                    <code>0 8 * * 1-5</code> = minuto 0, hora 8, cualquier día, cualquier mes, lun-vie
                </div>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'a',
                    label: '0 8 * * 1-5',
                    description: 'Minuto 0, hora 8, lunes a viernes'
                },
                {
                    id: 'b',
                    label: '8 0 * * 1-5',
                    description: 'Minuto 8, hora 0, lunes a viernes'
                },
                {
                    id: 'c',
                    label: '0 8 * * *',
                    description: 'Todos los días a las 8:00'
                },
                {
                    id: 'd',
                    label: '* 8 * * 1-5',
                    description: 'Cada minuto de las 8:00, lunes a viernes'
                }
            ],
            validate: function(answer) {
                return answer === 'a';
            },
            correctAnswer: 'a',
            explanation: `
                <p><strong>0 8 * * 1-5</strong> es correcto:</p>
                <ul>
                    <li><strong>0</strong> - Minuto 0</li>
                    <li><strong>8</strong> - Hora 8 (8:00 AM)</li>
                    <li><strong>*</strong> - Cualquier día del mes</li>
                    <li><strong>*</strong> - Cualquier mes</li>
                    <li><strong>1-5</strong> - Lunes (1) a Viernes (5)</li>
                </ul>
            `
        },
        {
            id: 'airflow_4',
            title: 'Misión 4: XComs',
            description: `
                <p><strong>Cliente: AirPipeline Corp</strong></p>
                <p>Los <strong>XComs</strong> (Cross-Communications) permiten que las tareas compartan datos.</p>
                <div class="code-example">
                    <pre>
# Task 1: Extrae y retorna datos
def extract_data(**context):
    data = fetch_from_api()
    return data  # Automáticamente push a XCom

# Task 2: Recibe datos de Task 1
def transform_data(**context):
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='extract_task')
    # Procesa data...
                    </pre>
                </div>
                <p><strong>¿Cuál es el límite recomendado de datos en XCom?</strong></p>
            `,
            type: 'choice',
            xp: 200,
            choices: [
                {
                    id: 'a',
                    label: 'Sin límite',
                    description: 'XCom puede almacenar cualquier cantidad de datos'
                },
                {
                    id: 'b',
                    label: '48 KB (metadata pequeña)',
                    description: 'Solo IDs, rutas de archivos, pequeños resultados'
                },
                {
                    id: 'c',
                    label: '10 MB',
                    description: 'Suficiente para datasets medianos'
                },
                {
                    id: 'd',
                    label: '1 GB',
                    description: 'Para grandes volúmenes de datos'
                }
            ],
            validate: function(answer) {
                return answer === 'b';
            },
            correctAnswer: 'b',
            explanation: `
                <p><strong>48 KB</strong> es el límite recomendado porque:</p>
                <ul>
                    <li>XComs se almacenan en la base de metadatos de Airflow</li>
                    <li>Datos grandes ralentizan el sistema</li>
                    <li><strong>Mejor práctica:</strong> Pasar rutas de archivos (S3, GCS) en lugar de datos</li>
                    <li>Para datos grandes, usa almacenamiento externo</li>
                </ul>
            `
        },
        {
            id: 'airflow_5',
            title: 'Misión 5: Manejo de Errores',
            description: `
                <p><strong>Cliente: AirPipeline Corp</strong></p>
                <p>Tu DAG falló. Analiza el estado de las tareas:</p>
                <div class="dag-status">
                    <table class="status-table">
                        <tr><th>Task</th><th>Estado</th><th>Reintentos</th></tr>
                        <tr><td>task_a</td><td class="success">✓ success</td><td>0</td></tr>
                        <tr><td>task_b</td><td class="success">✓ success</td><td>1</td></tr>
                        <tr><td>task_c</td><td class="failed">✗ failed</td><td>3 (max)</td></tr>
                        <tr><td>task_d</td><td class="upstream">⬆ upstream_failed</td><td>0</td></tr>
                    </table>
                    <p class="error-msg">Error en task_c: ConnectionError: Database unavailable</p>
                </div>
                <p><strong>¿Cuál es la mejor estrategia para solucionar esto?</strong></p>
            `,
            type: 'choice',
            xp: 200,
            choices: [
                {
                    id: 'a',
                    label: 'Reiniciar todo el DAG desde el inicio',
                    description: 'Ejecutar todas las tareas de nuevo'
                },
                {
                    id: 'b',
                    label: 'Arreglar el problema y hacer "Clear" solo de task_c',
                    description: 'Corregir conexión DB y re-ejecutar task_c y dependientes'
                },
                {
                    id: 'c',
                    label: 'Aumentar retries a 10 y esperar',
                    description: 'Más reintentos resolverán el problema'
                },
                {
                    id: 'd',
                    label: 'Ignorar y continuar con el siguiente DAG run',
                    description: 'Perder este batch de datos'
                }
            ],
            validate: function(answer) {
                return answer === 'b';
            },
            correctAnswer: 'b',
            explanation: `
                <p><strong>"Clear" de task_c</strong> es la mejor opción porque:</p>
                <ul>
                    <li>No re-ejecuta tareas ya completadas (task_a, task_b)</li>
                    <li>Al hacer Clear, task_c y task_d se marcan para re-ejecución</li>
                    <li>Primero hay que resolver el problema de conexión a DB</li>
                    <li>Es eficiente y mantiene el estado del DAG</li>
                </ul>
                <p><strong>Comando:</strong> <code>airflow tasks clear dag_id -t task_c</code></p>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 6: Apache Airflow',
            scenes: [
                {
                    id: 1,
                    content: `
                        Los pipelines manuales no escalan. Necesitas <strong>orquestación</strong>:
                        programar, monitorear y manejar dependencias automáticamente.
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
                        "Apache Airflow es el estándar de la industria para orquestación de datos.
                        Lo usan Airbnb, Spotify, Twitter, y miles de empresas más."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Nuevo cliente: <strong>AirPipeline Corp</strong>.
                        Tienen 50 pipelines manuales que necesitan automatizar."
                    `,
                    tutorial: {
                        title: '¿Qué es Apache Airflow?',
                        content: `
                            <ul>
                                <li><strong>Orquestador</strong> de workflows de datos</li>
                                <li>Pipelines como <strong>código Python</strong></li>
                                <li><strong>DAGs</strong>: Grafos dirigidos acíclicos</li>
                                <li>UI web para monitoreo</li>
                                <li>Scheduling, retries, alertas</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás a crear DAGs, usar operadores,
                        programar ejecuciones y manejar errores."
                    `,
                    tutorial: {
                        title: 'Conceptos Clave',
                        content: `
                            <ul>
                                <li><strong>DAG</strong>: Define el flujo completo</li>
                                <li><strong>Task</strong>: Una unidad de trabajo</li>
                                <li><strong>Operator</strong>: Tipo de tarea</li>
                                <li><strong>Schedule</strong>: Cuándo ejecutar</li>
                                <li><strong>XCom</strong>: Comunicación entre tasks</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'AirPipeline Corp'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Parse cron expression to human readable
     * @param {string} cron
     * @returns {string}
     */
    function parseCronExpression(cron) {
        return CRON_EXPRESSIONS[cron] || 'Expresión personalizada';
    }

    /**
     * Get operator info
     * @param {string} operatorName
     * @returns {Object}
     */
    function getOperatorInfo(operatorName) {
        return OPERATORS[operatorName] || null;
    }

    /**
     * Calculate DAG dependencies
     * @param {Object} dag
     * @returns {Object} Dependency map
     */
    function calculateDependencies(dag) {
        const deps = {};
        dag.tasks.forEach(task => {
            deps[task.id] = {
                upstream: task.upstream || [],
                downstream: []
            };
        });

        // Calculate downstream
        dag.tasks.forEach(task => {
            (task.upstream || []).forEach(upstreamId => {
                if (deps[upstreamId]) {
                    deps[upstreamId].downstream.push(task.id);
                }
            });
        });

        return deps;
    }

    /**
     * Find critical path in DAG
     * @param {Object} dag
     * @returns {Array} Critical path task IDs
     */
    function findCriticalPath(dag) {
        const deps = calculateDependencies(dag);
        const visited = new Set();
        const path = [];

        // Find start task (no upstream)
        let current = dag.tasks.find(t => !t.upstream || t.upstream.length === 0);

        while (current && !visited.has(current.id)) {
            visited.add(current.id);
            path.push(current.id);

            // Find next task with most downstream
            const downstream = deps[current.id].downstream;
            if (downstream.length > 0) {
                current = dag.tasks.find(t => t.id === downstream[0]);
            } else {
                current = null;
            }
        }

        return path;
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(6, {
            missions: MISSIONS,
            story: STORY,
            data: DAG_DATA,
            cronExpressions: CRON_EXPRESSIONS,
            operators: OPERATORS,
            helpers: {
                parseCronExpression,
                getOperatorInfo,
                calculateDependencies,
                findCriticalPath
            }
        });
        console.log('[Module6] Airflow module registered');
    }

    // Expose globally for backwards compatibility
    window.Module6 = {
        MISSIONS,
        STORY,
        DAG_DATA,
        CRON_EXPRESSIONS,
        OPERATORS,
        parseCronExpression,
        getOperatorInfo,
        calculateDependencies,
        findCriticalPath
    };

})();
