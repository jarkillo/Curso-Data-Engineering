/**
 * Module 10: ML/MLOps - Data Engineer: The Game
 *
 * Missions covering ML Engineering fundamentals:
 * - Feature Engineering
 * - Model Training (train/test split)
 * - Model Deployment (API serving)
 * - Model Monitoring (drift detection)
 * - MLOps Pipeline (end-to-end)
 */

(function() {
    'use strict';

    // ==========================================
    // SAMPLE ML DATA FOR MISSIONS
    // ==========================================

    // Feature Engineering data
    const FEATURE_DATA = {
        rawData: [
            { user_id: 1, purchase_date: '2024-01-15', amount: 150.00, category: 'Electronics' },
            { user_id: 1, purchase_date: '2024-01-20', amount: 50.00, category: 'Books' },
            { user_id: 1, purchase_date: '2024-02-01', amount: 200.00, category: 'Electronics' },
            { user_id: 2, purchase_date: '2024-01-10', amount: 75.00, category: 'Clothing' },
            { user_id: 2, purchase_date: '2024-01-25', amount: 300.00, category: 'Electronics' }
        ],
        engineeredFeatures: {
            user_1: {
                total_purchases: 3,
                avg_amount: 133.33,
                days_since_first: 17,
                favorite_category: 'Electronics',
                purchase_frequency: 0.18 // purchases per day
            },
            user_2: {
                total_purchases: 2,
                avg_amount: 187.50,
                days_since_first: 15,
                favorite_category: 'Electronics',
                purchase_frequency: 0.13
            }
        },
        featureTypes: [
            { name: 'Numerical', examples: ['total_purchases', 'avg_amount'], encoding: 'None/Scaling' },
            { name: 'Categorical', examples: ['favorite_category'], encoding: 'One-Hot/Label' },
            { name: 'Temporal', examples: ['days_since_first'], encoding: 'Extract components' },
            { name: 'Text', examples: ['product_description'], encoding: 'TF-IDF/Embeddings' }
        ]
    };

    // Train/Test Split data
    const TRAINING_DATA = {
        dataset: {
            totalSamples: 10000,
            features: 25,
            target: 'will_churn'
        },
        splits: {
            trainSize: 0.7,
            validationSize: 0.15,
            testSize: 0.15
        },
        stratification: {
            className: 'will_churn',
            distribution: { 0: 0.85, 1: 0.15 }, // Imbalanced!
            importance: 'Mantener proporción de clases en cada split'
        },
        crossValidation: {
            folds: 5,
            description: 'K-Fold para evaluar varianza del modelo'
        }
    };

    // Model Deployment data
    const DEPLOYMENT_DATA = {
        modelInfo: {
            name: 'churn_predictor_v2',
            framework: 'scikit-learn',
            size: '45 MB',
            avgLatency: 15, // ms
            throughput: 1000 // requests/sec
        },
        deploymentOptions: [
            {
                name: 'REST API (Flask/FastAPI)',
                pros: ['Simple', 'Flexible', 'Bien documentado'],
                cons: ['Escalar manualmente', 'Gestionar infraestructura'],
                useCase: 'Aplicaciones web, microservicios'
            },
            {
                name: 'Serverless (AWS Lambda)',
                pros: ['Auto-scaling', 'Pay per use', 'Sin servers'],
                cons: ['Cold starts', 'Límites de memoria', 'Vendor lock-in'],
                useCase: 'Cargas variables, bajo volumen'
            },
            {
                name: 'Container (Docker + K8s)',
                pros: ['Portabilidad', 'Scaling controlado', 'CI/CD fácil'],
                cons: ['Complejidad', 'Requiere orquestación'],
                useCase: 'Producción enterprise, alto volumen'
            },
            {
                name: 'Managed (SageMaker/Vertex AI)',
                pros: ['Todo integrado', 'Monitoring incluido', 'Auto-scaling'],
                cons: ['Costo', 'Vendor lock-in'],
                useCase: 'Equipos pequeños, rápido a producción'
            }
        ],
        apiExample: `
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("model.pkl")

class PredictionInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(input: PredictionInput):
    prediction = model.predict([input.features])
    return {"prediction": int(prediction[0])}`
    };

    // Model Monitoring data
    const MONITORING_DATA = {
        driftTypes: [
            {
                name: 'Data Drift',
                description: 'Cambio en la distribución de features de entrada',
                example: 'avg_amount cambió de $100 a $150',
                detection: 'KS test, PSI, distribución comparison'
            },
            {
                name: 'Concept Drift',
                description: 'Cambio en la relación feature-target',
                example: 'El comportamiento de churn cambió post-pandemia',
                detection: 'Monitorear métricas de modelo en producción'
            },
            {
                name: 'Label Drift',
                description: 'Cambio en la distribución del target',
                example: 'Churn rate pasó de 15% a 25%',
                detection: 'Tracking de distribución de predicciones'
            }
        ],
        metrics: {
            training: { accuracy: 0.92, precision: 0.85, recall: 0.78, f1: 0.81 },
            week1: { accuracy: 0.91, precision: 0.84, recall: 0.77, f1: 0.80 },
            week2: { accuracy: 0.89, precision: 0.82, recall: 0.75, f1: 0.78 },
            week3: { accuracy: 0.85, precision: 0.78, recall: 0.70, f1: 0.74 },
            week4: { accuracy: 0.80, precision: 0.72, recall: 0.65, f1: 0.68 }
        },
        alerts: [
            { type: 'Warning', threshold: 'Accuracy < 0.88', action: 'Investigar drift' },
            { type: 'Critical', threshold: 'Accuracy < 0.82', action: 'Reentrenar modelo' }
        ]
    };

    // MLOps Pipeline data
    const MLOPS_DATA = {
        stages: [
            { name: 'Data Ingestion', tools: ['Airflow', 'Prefect'], output: 'Raw data in S3' },
            { name: 'Data Validation', tools: ['Great Expectations', 'TFDV'], output: 'Validated data' },
            { name: 'Feature Engineering', tools: ['Feast', 'dbt'], output: 'Feature store' },
            { name: 'Model Training', tools: ['MLflow', 'Kubeflow'], output: 'Trained model' },
            { name: 'Model Validation', tools: ['MLflow', 'Custom'], output: 'Approved model' },
            { name: 'Model Registry', tools: ['MLflow', 'SageMaker'], output: 'Versioned model' },
            { name: 'Deployment', tools: ['SageMaker', 'Seldon'], output: 'Live endpoint' },
            { name: 'Monitoring', tools: ['Evidently', 'Prometheus'], output: 'Alerts/Dashboard' }
        ],
        maturityLevels: [
            { level: 0, name: 'No MLOps', description: 'Manual, notebooks, no versioning' },
            { level: 1, name: 'DevOps pero no MLOps', description: 'CI/CD pero modelos manuales' },
            { level: 2, name: 'MLOps Automatizado', description: 'Training automatizado, CD de modelos' },
            { level: 3, name: 'MLOps Full', description: 'Retraining automático basado en drift' }
        ]
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'ml_1',
            title: 'Misión 1: Feature Engineering',
            description: `
                <p><strong>Cliente: PredictiveAI Labs</strong></p>
                <p>Los modelos de ML solo son tan buenos como sus <strong>features</strong>.</p>
                <p>Tienes datos de compras de usuarios:</p>
                <div class="data-preview">
                    <table>
                        <tr><th>user_id</th><th>purchase_date</th><th>amount</th><th>category</th></tr>
                        ${FEATURE_DATA.rawData.slice(0, 3).map(r => `
                            <tr><td>${r.user_id}</td><td>${r.purchase_date}</td><td>$${r.amount}</td><td>${r.category}</td></tr>
                        `).join('')}
                    </table>
                </div>
                <p>Para el user_id=1 calculaste: total_purchases=3, avg_amount=$133.33</p>
                <p><strong>¿Cuántos features nuevos creaste a partir de los datos originales?</strong></p>
                <p>Features originales: user_id, purchase_date, amount, category (4)</p>
                <p>Features engineered: total_purchases, avg_amount, days_since_first, favorite_category, purchase_frequency</p>
            `,
            type: 'numeric',
            xp: 175,
            data: FEATURE_DATA,
            validate: function(answer) {
                // 5 engineered features
                return Math.abs(answer - 5) < 0.5;
            },
            getCorrectAnswer: function() {
                return 5;
            }
        },
        {
            id: 'ml_2',
            title: 'Misión 2: Train/Test Split',
            description: `
                <p><strong>Cliente: PredictiveAI Labs</strong></p>
                <p>Tienes un dataset de 10,000 muestras para predecir churn.</p>
                <p>El dataset está <strong>desbalanceado</strong>: 85% no-churn, 15% churn.</p>
                <p>Quieres dividir: 70% train, 15% validation, 15% test.</p>
                <p><strong>¿Qué técnica debes usar para mantener la proporción de clases?</strong></p>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'random',
                    label: 'Random Split',
                    description: 'Dividir aleatoriamente sin consideraciones'
                },
                {
                    id: 'stratified',
                    label: 'Stratified Split',
                    description: 'Mantener proporción de clases en cada split'
                },
                {
                    id: 'timebased',
                    label: 'Time-based Split',
                    description: 'Dividir por fecha'
                },
                {
                    id: 'groupbased',
                    label: 'Group-based Split',
                    description: 'Dividir por grupos de usuarios'
                }
            ],
            validate: function(answer) {
                return answer === 'stratified';
            },
            correctAnswer: 'stratified',
            explanation: `
                <p><strong>Stratified Split</strong> es esencial porque:</p>
                <ul>
                    <li>Mantiene 85/15 en train, validation Y test</li>
                    <li>Con random split, test podría tener 90/10 o 80/20</li>
                    <li>Evaluación sería inconsistente</li>
                    <li>En sklearn: <code>train_test_split(stratify=y)</code></li>
                </ul>
            `
        },
        {
            id: 'ml_3',
            title: 'Misión 3: Model Deployment',
            description: `
                <p><strong>Cliente: PredictiveAI Labs</strong></p>
                <p>Tu modelo de churn está listo para producción:</p>
                <ul>
                    <li>Tamaño: 45 MB</li>
                    <li>Latencia requerida: < 50ms</li>
                    <li>Tráfico esperado: 100-10,000 requests/segundo (variable)</li>
                    <li>Equipo pequeño, sin DevOps dedicado</li>
                </ul>
                <p><strong>¿Qué opción de deployment es más adecuada?</strong></p>
            `,
            type: 'choice',
            xp: 200,
            choices: [
                {
                    id: 'flask',
                    label: 'REST API (Flask en EC2)',
                    description: 'API tradicional en servidor'
                },
                {
                    id: 'lambda',
                    label: 'AWS Lambda',
                    description: 'Serverless, auto-scaling'
                },
                {
                    id: 'k8s',
                    label: 'Kubernetes',
                    description: 'Containers orquestados'
                },
                {
                    id: 'managed',
                    label: 'SageMaker Endpoint',
                    description: 'Servicio gestionado de AWS'
                }
            ],
            validate: function(answer) {
                return answer === 'managed';
            },
            correctAnswer: 'managed',
            explanation: `
                <p><strong>SageMaker Endpoint</strong> es ideal porque:</p>
                <ul>
                    <li><strong>Auto-scaling:</strong> Maneja 100-10K req/s automáticamente</li>
                    <li><strong>Equipo pequeño:</strong> Sin gestión de infraestructura</li>
                    <li><strong>Latencia:</strong> Optimizado para ML inference</li>
                    <li><strong>Monitoring:</strong> CloudWatch integrado</li>
                </ul>
                <p>Lambda tendría cold starts y límites de memoria.</p>
            `
        },
        {
            id: 'ml_4',
            title: 'Misión 4: Model Monitoring',
            description: `
                <p><strong>Cliente: PredictiveAI Labs</strong></p>
                <p>Tu modelo en producción muestra esta degradación:</p>
                <div class="metrics-table">
                    <table>
                        <tr><th>Semana</th><th>Accuracy</th><th>F1</th></tr>
                        <tr><td>Training</td><td>0.92</td><td>0.81</td></tr>
                        <tr><td>Semana 1</td><td>0.91</td><td>0.80</td></tr>
                        <tr><td>Semana 2</td><td>0.89</td><td>0.78</td></tr>
                        <tr class="warning"><td>Semana 3</td><td>0.85</td><td>0.74</td></tr>
                        <tr class="critical"><td>Semana 4</td><td>0.80</td><td>0.68</td></tr>
                    </table>
                </div>
                <p>Alertas configuradas: Warning < 0.88, Critical < 0.82</p>
                <p><strong>¿En qué semana debería dispararse la alerta Critical?</strong></p>
            `,
            type: 'numeric',
            xp: 225,
            data: MONITORING_DATA,
            validate: function(answer) {
                // Semana 4: accuracy 0.80 < 0.82 (critical threshold)
                return Math.abs(answer - 4) < 0.5;
            },
            getCorrectAnswer: function() {
                return 4;
            }
        },
        {
            id: 'ml_5',
            title: 'Misión 5: MLOps Pipeline',
            description: `
                <p><strong>Cliente: PredictiveAI Labs</strong></p>
                <p>El cliente quiere implementar MLOps completo.</p>
                <p>Actualmente están en <strong>Nivel 0</strong>: todo manual, notebooks, sin versioning.</p>
                <div class="mlops-levels">
                    <table>
                        <tr><th>Nivel</th><th>Descripción</th></tr>
                        <tr><td>0</td><td>Manual, notebooks</td></tr>
                        <tr><td>1</td><td>CI/CD pero modelos manuales</td></tr>
                        <tr><td>2</td><td>Training automatizado</td></tr>
                        <tr><td>3</td><td>Retraining automático por drift</td></tr>
                    </table>
                </div>
                <p><strong>¿Cuántas etapas tiene un pipeline MLOps completo?</strong></p>
                <p>Etapas: Ingestion → Validation → Feature Eng → Training → Model Validation → Registry → Deployment → Monitoring</p>
            `,
            type: 'numeric',
            xp: 250,
            data: MLOPS_DATA,
            validate: function(answer, data) {
                return Math.abs(answer - data.stages.length) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.stages.length; // 8
            }
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 10: ML/MLOps',
            scenes: [
                {
                    id: 1,
                    content: `
                        El Data Engineering moderno incluye <strong>Machine Learning en producción</strong>.
                        No basta con entrenar un modelo: hay que desplegarlo, monitorearlo y mantenerlo.
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
                        "El 87% de los proyectos de ML nunca llegan a producción.
                        MLOps es la disciplina que cierra esa brecha."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Último cliente: <strong>PredictiveAI Labs</strong>.
                        Quieren pasar de notebooks a producción enterprise."
                    `,
                    tutorial: {
                        title: 'ML Engineering vs Data Science',
                        content: `
                            <ul>
                                <li><strong>Data Scientist</strong>: Entrena modelos en notebooks</li>
                                <li><strong>ML Engineer</strong>: Lleva modelos a producción</li>
                                <li><strong>Data Engineer</strong>: Proporciona datos limpios y pipelines</li>
                                <li><strong>MLOps</strong>: Automatiza todo el ciclo de vida</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Este es el módulo final. Aprenderás feature engineering,
                        deployment, monitoring y pipelines MLOps completos."
                    `,
                    tutorial: {
                        title: 'El Ciclo MLOps',
                        content: `
                            <p>MLOps = ML + DevOps + Data Engineering</p>
                            <pre>
Data → Features → Train → Deploy → Monitor
  ↑                                    |
  └────── Retraining automático ←──────┘
                            </pre>
                            <p>El objetivo: modelos que mejoran continuamente.</p>
                        `
                    }
                }
            ]
        },
        company: 'PredictiveAI Labs'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Calculate feature statistics
     * @param {Array} data
     * @param {string} column
     * @returns {Object}
     */
    function calculateFeatureStats(data, column) {
        const values = data.map(row => row[column]).filter(v => typeof v === 'number');
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const sorted = [...values].sort((a, b) => a - b);
        const median = sorted[Math.floor(sorted.length / 2)];
        const min = Math.min(...values);
        const max = Math.max(...values);

        return { mean, median, min, max, count: values.length };
    }

    /**
     * Detect data drift using simple threshold
     * @param {Object} baseline - Baseline statistics
     * @param {Object} current - Current statistics
     * @param {number} threshold - Drift threshold (default 0.2 = 20%)
     * @returns {Object}
     */
    function detectDrift(baseline, current, threshold = 0.2) {
        const meanDrift = Math.abs(current.mean - baseline.mean) / baseline.mean;
        const hasDrift = meanDrift > threshold;

        return {
            meanDrift: (meanDrift * 100).toFixed(2) + '%',
            hasDrift,
            recommendation: hasDrift ? 'Investigar y posiblemente reentrenar' : 'OK'
        };
    }

    /**
     * Calculate model performance degradation
     * @param {Object} metrics - Weekly metrics
     * @returns {Object}
     */
    function calculateDegradation(metrics) {
        const baseline = metrics.training.accuracy;
        const current = metrics.week4.accuracy;
        const degradation = ((baseline - current) / baseline * 100).toFixed(2);

        return {
            baseline,
            current,
            degradation: degradation + '%',
            weeks: 4,
            trend: 'Decreasing'
        };
    }

    /**
     * Recommend MLOps maturity next step
     * @param {number} currentLevel
     * @returns {Object}
     */
    function recommendNextStep(currentLevel) {
        const recommendations = {
            0: {
                nextLevel: 1,
                actions: ['Implementar version control', 'Crear CI/CD básico', 'Documentar modelos']
            },
            1: {
                nextLevel: 2,
                actions: ['Automatizar training pipeline', 'Implementar model registry', 'Añadir data validation']
            },
            2: {
                nextLevel: 3,
                actions: ['Implementar monitoring de drift', 'Automatizar retraining', 'A/B testing de modelos']
            },
            3: {
                nextLevel: 'Máximo',
                actions: ['Optimizar continuamente', 'Expandir a más casos de uso']
            }
        };

        return recommendations[currentLevel] || recommendations[0];
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(10, {
            missions: MISSIONS,
            story: STORY,
            data: {
                features: FEATURE_DATA,
                training: TRAINING_DATA,
                deployment: DEPLOYMENT_DATA,
                monitoring: MONITORING_DATA,
                mlops: MLOPS_DATA
            },
            helpers: {
                calculateFeatureStats,
                detectDrift,
                calculateDegradation,
                recommendNextStep
            }
        });
        console.log('[Module10] ML/MLOps module registered');
    }

    // Expose globally for backwards compatibility
    window.Module10 = {
        MISSIONS,
        STORY,
        FEATURE_DATA,
        TRAINING_DATA,
        DEPLOYMENT_DATA,
        MONITORING_DATA,
        MLOPS_DATA,
        calculateFeatureStats,
        detectDrift,
        calculateDegradation,
        recommendNextStep
    };

})();
