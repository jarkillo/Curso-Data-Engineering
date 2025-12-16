/**
 * Module 7: Cloud (AWS) - Data Engineer: The Game
 *
 * Missions covering cloud fundamentals:
 * - S3: Object storage basics
 * - IAM: Permissions and roles
 * - Lambda: Serverless computing
 * - Glue: ETL service
 * - Cost optimization
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE CLOUD DATA FOR MISSIONS
    // ==========================================

    // S3 bucket structure
    const S3_DATA = {
        buckets: [
            {
                name: 'dataflow-raw-data',
                region: 'us-east-1',
                objects: [
                    { key: 'sales/2024/01/transactions.parquet', size: '2.5 GB', storageClass: 'STANDARD' },
                    { key: 'sales/2024/01/customers.csv', size: '150 MB', storageClass: 'STANDARD' },
                    { key: 'logs/2024/01/app.log', size: '500 MB', storageClass: 'STANDARD' },
                    { key: 'archive/2023/annual_report.pdf', size: '25 MB', storageClass: 'GLACIER' }
                ],
                totalSize: '3.175 GB'
            },
            {
                name: 'dataflow-processed',
                region: 'us-east-1',
                objects: [
                    { key: 'warehouse/dim_customers.parquet', size: '800 MB', storageClass: 'STANDARD' },
                    { key: 'warehouse/fact_sales.parquet', size: '5 GB', storageClass: 'STANDARD' }
                ],
                totalSize: '5.8 GB'
            }
        ],
        storageCosts: {
            STANDARD: 0.023,      // per GB/month
            STANDARD_IA: 0.0125,  // Infrequent Access
            GLACIER: 0.004,       // Archive
            DEEP_ARCHIVE: 0.00099 // Long-term archive
        }
    };

    // IAM policies example
    const IAM_DATA = {
        policies: [
            {
                name: 'DataEngineerPolicy',
                description: 'Acceso para Data Engineers',
                permissions: [
                    { service: 'S3', actions: ['GetObject', 'PutObject', 'ListBucket'], resources: ['arn:aws:s3:::dataflow-*'] },
                    { service: 'Glue', actions: ['StartJobRun', 'GetJobRun'], resources: ['*'] },
                    { service: 'Athena', actions: ['StartQueryExecution', 'GetQueryResults'], resources: ['*'] }
                ]
            },
            {
                name: 'DataAnalystPolicy',
                description: 'Acceso solo lectura para Analysts',
                permissions: [
                    { service: 'S3', actions: ['GetObject', 'ListBucket'], resources: ['arn:aws:s3:::dataflow-processed/*'] },
                    { service: 'Athena', actions: ['StartQueryExecution', 'GetQueryResults'], resources: ['*'] }
                ]
            }
        ],
        roles: [
            { name: 'GlueServiceRole', trustPolicy: 'glue.amazonaws.com', policies: ['AWSGlueServiceRole', 'S3FullAccess'] },
            { name: 'LambdaExecutionRole', trustPolicy: 'lambda.amazonaws.com', policies: ['AWSLambdaBasicExecutionRole', 'S3ReadOnly'] }
        ]
    };

    // Lambda function example
    const LAMBDA_DATA = {
        functions: [
            {
                name: 'process-new-files',
                runtime: 'python3.11',
                memory: 512,
                timeout: 300,
                trigger: 'S3 Event (ObjectCreated)',
                avgDuration: 45000, // ms
                monthlyInvocations: 10000
            }
        ],
        pricing: {
            requestCost: 0.20,        // per 1M requests
            durationCost: 0.0000166667 // per GB-second
        }
    };

    // Glue job example
    const GLUE_DATA = {
        jobs: [
            {
                name: 'etl-ventas-diario',
                type: 'Spark',
                workerType: 'G.1X',
                numberOfWorkers: 10,
                avgRuntime: 15, // minutes
                dpuHours: 2.5
            }
        ],
        pricing: {
            dpuHourCost: 0.44 // per DPU-hour
        }
    };

    // Monthly costs breakdown
    const COST_DATA = {
        current: {
            s3Storage: 250,
            s3Requests: 45,
            lambda: 35,
            glue: 400,
            athena: 25,
            dataTransfer: 150,
            total: 905
        },
        optimized: {
            s3Storage: 125,  // Using lifecycle policies
            s3Requests: 45,
            lambda: 35,
            glue: 280,       // Right-sized workers
            athena: 15,      // Partitioned queries
            dataTransfer: 75, // Same region
            total: 575
        }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'cloud_1',
            title: 'Misión 1: Amazon S3 Básico',
            description: `
                <p><strong>Cliente: CloudMaster Solutions</strong></p>
                <p>Amazon S3 es el servicio de almacenamiento de objetos más usado en la nube.</p>
                <p>Analiza la estructura de estos buckets:</p>
                <div class="s3-structure">
                    <pre>${JSON.stringify(S3_DATA.buckets, null, 2)}</pre>
                </div>
                <p><strong>¿Cuántos objetos en total hay en ambos buckets?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Cuenta los elementos en los arrays "objects" de cada bucket.
                </div>
            `,
            type: 'numeric',
            xp: 150,
            data: S3_DATA.buckets,
            validate: function(answer, data) {
                const total = data.reduce((sum, bucket) => sum + bucket.objects.length, 0);
                return Math.abs(answer - total) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.reduce((sum, bucket) => sum + bucket.objects.length, 0); // 6
            }
        },
        {
            id: 'cloud_2',
            title: 'Misión 2: IAM - Permisos y Roles',
            description: `
                <p><strong>Cliente: CloudMaster Solutions</strong></p>
                <p>Un nuevo Data Analyst necesita acceso al data warehouse.</p>
                <p>Requisitos:</p>
                <ul>
                    <li>✓ Puede LEER datos procesados en S3</li>
                    <li>✓ Puede ejecutar queries en Athena</li>
                    <li>✗ NO puede escribir en S3</li>
                    <li>✗ NO puede ejecutar jobs de Glue</li>
                </ul>
                <p><strong>¿Qué política le asignarías?</strong></p>
            `,
            type: 'choice',
            xp: 150,
            choices: [
                {
                    id: 'engineer',
                    label: 'DataEngineerPolicy',
                    description: 'Acceso completo a S3, Glue y Athena'
                },
                {
                    id: 'analyst',
                    label: 'DataAnalystPolicy',
                    description: 'Solo lectura de S3 processed y Athena'
                },
                {
                    id: 'admin',
                    label: 'AdministratorAccess',
                    description: 'Acceso total a todos los servicios'
                },
                {
                    id: 's3full',
                    label: 'AmazonS3FullAccess',
                    description: 'Acceso completo a S3'
                }
            ],
            validate: function(answer) {
                return answer === 'analyst';
            },
            correctAnswer: 'analyst',
            explanation: `
                <p><strong>DataAnalystPolicy</strong> es correcta porque:</p>
                <ul>
                    <li>Sigue el principio de <strong>menor privilegio</strong></li>
                    <li>Solo permite GET (lectura) en S3, no PUT (escritura)</li>
                    <li>Limita acceso solo al bucket processed</li>
                    <li>Permite Athena para queries pero no Glue para ETL</li>
                </ul>
                <p><strong>Nunca dar más permisos de los necesarios.</strong></p>
            `
        },
        {
            id: 'cloud_3',
            title: 'Misión 3: AWS Lambda',
            description: `
                <p><strong>Cliente: CloudMaster Solutions</strong></p>
                <p>Tienes una función Lambda que procesa archivos nuevos en S3:</p>
                <div class="lambda-config">
                    <ul>
                        <li><strong>Memoria:</strong> 512 MB</li>
                        <li><strong>Duración promedio:</strong> 45 segundos</li>
                        <li><strong>Invocaciones/mes:</strong> 10,000</li>
                    </ul>
                </div>
                <p>Costos Lambda:</p>
                <ul>
                    <li>Requests: $0.20 por millón</li>
                    <li>Duración: $0.0000166667 por GB-segundo</li>
                </ul>
                <p><strong>¿Cuál es el costo mensual aproximado de esta función? (en USD)</strong></p>
                <div class="mission-hint">
                    <strong>💡 Fórmula:</strong><br>
                    Costo = (Requests × $0.20/1M) + (GB-segundos × $0.0000166667)<br>
                    GB-segundos = (Memoria_GB × Duración_seg × Invocaciones)
                </div>
            `,
            type: 'numeric',
            xp: 200,
            data: LAMBDA_DATA,
            validate: function(answer, data) {
                // 10000 requests = $0.002
                // GB-seconds = 0.5 GB × 45 sec × 10000 = 225000 GB-sec
                // Duration cost = 225000 × $0.0000166667 = $3.75
                // Total = ~$3.75
                const correctAnswer = 3.75;
                return Math.abs(answer - correctAnswer) < 0.5;
            },
            getCorrectAnswer: function() {
                return 3.75;
            }
        },
        {
            id: 'cloud_4',
            title: 'Misión 4: AWS Glue ETL',
            description: `
                <p><strong>Cliente: CloudMaster Solutions</strong></p>
                <p>AWS Glue es un servicio de ETL serverless. Analiza este job:</p>
                <div class="glue-job">
                    <ul>
                        <li><strong>Tipo:</strong> Spark</li>
                        <li><strong>Workers:</strong> 10 (G.1X)</li>
                        <li><strong>Runtime promedio:</strong> 15 minutos</li>
                        <li><strong>Ejecuciones/día:</strong> 4</li>
                    </ul>
                    <p><strong>Costo:</strong> $0.44 por DPU-hora</p>
                    <p><strong>Nota:</strong> G.1X = 1 DPU por worker</p>
                </div>
                <p><strong>¿Cuál es el costo diario de este job Glue? (en USD)</strong></p>
                <div class="mission-hint">
                    <strong>💡 Fórmula:</strong><br>
                    DPU-horas = Workers × (Runtime_min/60) × Ejecuciones<br>
                    Costo = DPU-horas × $0.44
                </div>
            `,
            type: 'numeric',
            xp: 200,
            data: GLUE_DATA,
            validate: function(answer, data) {
                // DPU-hours = 10 workers × (15/60 hours) × 4 runs = 10 DPU-hours
                // Cost = 10 × $0.44 = $4.40
                const correctAnswer = 4.40;
                return Math.abs(answer - correctAnswer) < 0.3;
            },
            getCorrectAnswer: function() {
                return 4.40;
            }
        },
        {
            id: 'cloud_5',
            title: 'Misión 5: Optimización de Costos',
            description: `
                <p><strong>Cliente: CloudMaster Solutions</strong></p>
                <p>El CTO quiere reducir la factura de AWS. Estos son los costos actuales:</p>
                <div class="cost-breakdown">
                    <table class="cost-table">
                        <tr><th>Servicio</th><th>Actual</th><th>Optimizado</th></tr>
                        <tr><td>S3 Storage</td><td>$250</td><td>$125</td></tr>
                        <tr><td>S3 Requests</td><td>$45</td><td>$45</td></tr>
                        <tr><td>Lambda</td><td>$35</td><td>$35</td></tr>
                        <tr><td>Glue</td><td>$400</td><td>$280</td></tr>
                        <tr><td>Athena</td><td>$25</td><td>$15</td></tr>
                        <tr><td>Data Transfer</td><td>$150</td><td>$75</td></tr>
                        <tr class="total"><td><strong>Total</strong></td><td><strong>$905</strong></td><td><strong>$575</strong></td></tr>
                    </table>
                </div>
                <p><strong>¿Qué porcentaje de ahorro representa la optimización?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Fórmula:</strong> Ahorro % = ((Actual - Optimizado) / Actual) × 100
                </div>
            `,
            type: 'numeric',
            xp: 225,
            data: COST_DATA,
            validate: function(answer, data) {
                // Savings = (905 - 575) / 905 × 100 = 36.46%
                const correctAnswer = 36.46;
                return Math.abs(answer - correctAnswer) < 1;
            },
            getCorrectAnswer: function() {
                return 36.46;
            },
            explanation: `
                <p><strong>Estrategias de optimización aplicadas:</strong></p>
                <ul>
                    <li><strong>S3:</strong> Lifecycle policies para mover datos antiguos a Glacier</li>
                    <li><strong>Glue:</strong> Right-sizing de workers, Auto Scaling</li>
                    <li><strong>Athena:</strong> Particionado de tablas, formato columnar (Parquet)</li>
                    <li><strong>Transfer:</strong> Mantener datos en la misma región</li>
                </ul>
            `
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 7: Cloud (AWS)',
            scenes: [
                {
                    id: 1,
                    content: `
                        El Data Engineering moderno vive en la <strong>nube</strong>.
                        Escalabilidad infinita, pago por uso, servicios gestionados.
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
                        "AWS es el líder del mercado cloud. Como Data Engineer,
                        usarás S3, Glue, Lambda, Athena y muchos más servicios a diario."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Nuevo cliente: <strong>CloudMaster Solutions</strong>.
                        Están migrando su infraestructura on-premise a AWS."
                    `,
                    tutorial: {
                        title: 'Servicios AWS para Data Engineering',
                        content: `
                            <ul>
                                <li><strong>S3</strong>: Almacenamiento de objetos (Data Lake)</li>
                                <li><strong>Glue</strong>: ETL serverless</li>
                                <li><strong>Lambda</strong>: Funciones serverless</li>
                                <li><strong>Athena</strong>: Queries SQL sobre S3</li>
                                <li><strong>Redshift</strong>: Data Warehouse</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás a usar estos servicios y a optimizar costos.
                        En la nube, cada centavo cuenta."
                    `,
                    tutorial: {
                        title: 'Principio de Menor Privilegio',
                        content: `
                            <p>En IAM, siempre dar los <strong>mínimos permisos necesarios</strong>:</p>
                            <ul>
                                <li>No usar AdministratorAccess</li>
                                <li>Políticas específicas por rol</li>
                                <li>Recursos limitados (ARNs específicos)</li>
                                <li>Revisar permisos regularmente</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'CloudMaster Solutions'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Calculate S3 storage cost
     * @param {number} sizeGB - Size in GB
     * @param {string} storageClass - Storage class
     * @returns {number} Monthly cost in USD
     */
    function calculateS3Cost(sizeGB, storageClass = 'STANDARD') {
        const cost = S3_DATA.storageCosts[storageClass] || S3_DATA.storageCosts.STANDARD;
        return sizeGB * cost;
    }

    /**
     * Calculate Lambda cost
     * @param {number} invocations - Number of invocations
     * @param {number} memoryMB - Memory in MB
     * @param {number} durationMs - Duration in milliseconds
     * @returns {number} Cost in USD
     */
    function calculateLambdaCost(invocations, memoryMB, durationMs) {
        const requestCost = (invocations / 1000000) * LAMBDA_DATA.pricing.requestCost;
        const gbSeconds = (memoryMB / 1024) * (durationMs / 1000) * invocations;
        const durationCost = gbSeconds * LAMBDA_DATA.pricing.durationCost;
        return requestCost + durationCost;
    }

    /**
     * Calculate Glue job cost
     * @param {number} workers - Number of workers
     * @param {number} runtimeMinutes - Runtime in minutes
     * @param {number} runs - Number of runs
     * @returns {number} Cost in USD
     */
    function calculateGlueCost(workers, runtimeMinutes, runs = 1) {
        const dpuHours = workers * (runtimeMinutes / 60) * runs;
        return dpuHours * GLUE_DATA.pricing.dpuHourCost;
    }

    /**
     * Suggest cost optimizations
     * @param {Object} currentCosts
     * @returns {Array} Optimization suggestions
     */
    function suggestOptimizations(currentCosts) {
        const suggestions = [];

        if (currentCosts.s3Storage > 100) {
            suggestions.push({
                service: 'S3',
                suggestion: 'Implementar lifecycle policies para mover datos a Glacier',
                potentialSavings: '50%'
            });
        }

        if (currentCosts.glue > 200) {
            suggestions.push({
                service: 'Glue',
                suggestion: 'Right-size workers y habilitar auto-scaling',
                potentialSavings: '30%'
            });
        }

        if (currentCosts.dataTransfer > 100) {
            suggestions.push({
                service: 'Data Transfer',
                suggestion: 'Mantener datos y compute en la misma región',
                potentialSavings: '50%'
            });
        }

        return suggestions;
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(7, {
            missions: MISSIONS,
            story: STORY,
            data: {
                s3: S3_DATA,
                iam: IAM_DATA,
                lambda: LAMBDA_DATA,
                glue: GLUE_DATA,
                costs: COST_DATA
            },
            helpers: {
                calculateS3Cost,
                calculateLambdaCost,
                calculateGlueCost,
                suggestOptimizations
            }
        });
        console.log('[Module7] Cloud module registered');
    }

    // Expose globally for backwards compatibility
    window.Module7 = {
        MISSIONS,
        STORY,
        S3_DATA,
        IAM_DATA,
        LAMBDA_DATA,
        GLUE_DATA,
        COST_DATA,
        calculateS3Cost,
        calculateLambdaCost,
        calculateGlueCost,
        suggestOptimizations
    };

})();
