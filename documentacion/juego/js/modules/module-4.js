/**
 * Module 4: APIs - Data Engineer: The Game
 *
 * Missions covering API fundamentals:
 * - REST basics and HTTP methods
 * - Query parameters and filtering
 * - Pagination strategies
 * - Error handling and status codes
 * - Rate limiting and caching
 */

(function() {
    'use strict';

    // ==========================================
    // SIMULATED API DATA
    // ==========================================

    // Simulated API responses
    const API_DATA = {
        // Products endpoint
        products: {
            data: [
                { id: 1, name: 'Laptop Pro', category: 'electronics', price: 1299.99, stock: 50 },
                { id: 2, name: 'Wireless Mouse', category: 'electronics', price: 29.99, stock: 200 },
                { id: 3, name: 'Office Chair', category: 'furniture', price: 249.99, stock: 30 },
                { id: 4, name: 'Standing Desk', category: 'furniture', price: 499.99, stock: 15 },
                { id: 5, name: 'Monitor 27"', category: 'electronics', price: 399.99, stock: 75 },
                { id: 6, name: 'Keyboard RGB', category: 'electronics', price: 89.99, stock: 150 },
                { id: 7, name: 'Webcam HD', category: 'electronics', price: 79.99, stock: 100 },
                { id: 8, name: 'Desk Lamp', category: 'furniture', price: 45.99, stock: 80 },
                { id: 9, name: 'USB Hub', category: 'electronics', price: 24.99, stock: 300 },
                { id: 10, name: 'Cable Manager', category: 'accessories', price: 15.99, stock: 500 }
            ],
            pagination: {
                total: 10,
                per_page: 3,
                current_page: 1,
                total_pages: 4
            }
        },

        // Users endpoint
        users: {
            data: [
                { id: 1, username: 'admin', role: 'admin', active: true },
                { id: 2, username: 'analyst1', role: 'analyst', active: true },
                { id: 3, username: 'dev_user', role: 'developer', active: true },
                { id: 4, username: 'viewer', role: 'viewer', active: false },
                { id: 5, username: 'manager1', role: 'manager', active: true }
            ]
        },

        // Rate limit info
        rateLimits: {
            requests_per_minute: 60,
            requests_remaining: 45,
            reset_time: '2024-01-20T12:00:00Z'
        }
    };

    // HTTP Status codes reference
    const HTTP_STATUS = {
        200: { name: 'OK', description: 'Solicitud exitosa' },
        201: { name: 'Created', description: 'Recurso creado' },
        400: { name: 'Bad Request', description: 'Error en la solicitud del cliente' },
        401: { name: 'Unauthorized', description: 'Autenticación requerida' },
        403: { name: 'Forbidden', description: 'Acceso denegado' },
        404: { name: 'Not Found', description: 'Recurso no encontrado' },
        429: { name: 'Too Many Requests', description: 'Límite de solicitudes excedido' },
        500: { name: 'Internal Server Error', description: 'Error del servidor' },
        503: { name: 'Service Unavailable', description: 'Servicio no disponible' }
    };

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'api_1',
            title: 'Misión 1: Tu Primera API',
            description: `
                <p><strong>Cliente: CloudAPI Systems</strong></p>
                <p>Vamos a conectarnos a una API REST. Analiza esta respuesta JSON:</p>
                <div class="api-response">
                    <div class="api-endpoint">GET /api/v1/products</div>
                    <pre>${JSON.stringify(API_DATA.products.data.slice(0, 3), null, 2)}</pre>
                </div>
                <p><strong>¿Cuántos productos tiene categoría "electronics"?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Filtra por el campo "category" en todo el dataset (10 productos).
                </div>
            `,
            type: 'numeric',
            xp: 100,
            data: API_DATA.products.data,
            validate: function(answer, data) {
                const count = data.filter(p => p.category === 'electronics').length;
                return Math.abs(answer - count) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.filter(p => p.category === 'electronics').length; // 6
            }
        },
        {
            id: 'api_2',
            title: 'Misión 2: Query Parameters',
            description: `
                <p><strong>Cliente: CloudAPI Systems</strong></p>
                <p>Las APIs permiten filtrar datos usando query parameters en la URL.</p>
                <p>¿Cuál es la URL correcta para obtener productos de categoría "furniture" con precio menor a 300?</p>
                <div class="api-example">
                    <strong>Formato:</strong> /api/products?param1=valor1&param2=valor2
                </div>
            `,
            type: 'choice',
            xp: 100,
            choices: [
                {
                    id: 'a',
                    label: '/api/products/furniture/300',
                    description: 'Usando path parameters'
                },
                {
                    id: 'b',
                    label: '/api/products?category=furniture&max_price=300',
                    description: 'Usando query parameters'
                },
                {
                    id: 'c',
                    label: '/api/products?filter=category:furniture,price<300',
                    description: 'Usando filtro combinado'
                },
                {
                    id: 'd',
                    label: '/api/products?category=furniture&price=300',
                    description: 'Sin operador de comparación'
                }
            ],
            validate: function(answer) {
                return answer === 'b';
            },
            correctAnswer: 'b',
            explanation: `
                <p>La opción B es correcta porque:</p>
                <ul>
                    <li>Usa <strong>query parameters</strong> (después del ?)</li>
                    <li>Separa parámetros con <strong>&</strong></li>
                    <li>Usa nombres descriptivos (category, max_price)</li>
                </ul>
            `
        },
        {
            id: 'api_3',
            title: 'Misión 3: Paginación',
            description: `
                <p><strong>Cliente: CloudAPI Systems</strong></p>
                <p>La API devuelve datos paginados. Analiza esta respuesta:</p>
                <div class="api-response">
                    <pre>${JSON.stringify({
                        data: '[ ... 3 productos ... ]',
                        pagination: API_DATA.products.pagination
                    }, null, 2)}</pre>
                </div>
                <p><strong>¿Cuántas solicitudes necesitas para obtener TODOS los productos?</strong></p>
            `,
            type: 'numeric',
            xp: 150,
            data: API_DATA.products.pagination,
            validate: function(answer, data) {
                return Math.abs(answer - data.total_pages) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.total_pages; // 4
            }
        },
        {
            id: 'api_4',
            title: 'Misión 4: Códigos de Estado HTTP',
            description: `
                <p><strong>Cliente: CloudAPI Systems</strong></p>
                <p>Tu pipeline recibe este error de la API:</p>
                <div class="api-error">
                    <code>HTTP 429 - Too Many Requests</code>
                    <p>Headers: X-RateLimit-Reset: 60 seconds</p>
                </div>
                <p><strong>¿Cuál es la mejor estrategia para manejar este error?</strong></p>
            `,
            type: 'choice',
            xp: 175,
            choices: [
                {
                    id: 'a',
                    label: 'Reintentar inmediatamente',
                    description: 'Hacer la solicitud de nuevo al instante'
                },
                {
                    id: 'b',
                    label: 'Esperar y reintentar (Exponential Backoff)',
                    description: 'Esperar el tiempo indicado, luego reintentar'
                },
                {
                    id: 'c',
                    label: 'Reportar error y detener',
                    description: 'Fallar el pipeline y notificar'
                },
                {
                    id: 'd',
                    label: 'Ignorar y continuar',
                    description: 'Saltar este dato y seguir con el siguiente'
                }
            ],
            validate: function(answer) {
                return answer === 'b';
            },
            correctAnswer: 'b',
            explanation: `
                <p><strong>Exponential Backoff</strong> es la mejor práctica porque:</p>
                <ul>
                    <li>Respeta los límites de la API (el header indica 60 segundos)</li>
                    <li>Permite recuperación automática</li>
                    <li>Evita sobrecargar el servidor</li>
                    <li>Es la estrategia estándar para errores 429</li>
                </ul>
            `
        },
        {
            id: 'api_5',
            title: 'Misión 5: Rate Limiting y Caching',
            description: `
                <p><strong>Cliente: CloudAPI Systems</strong></p>
                <p>Tu pipeline necesita hacer 1000 llamadas a una API con estos límites:</p>
                <div class="api-limits">
                    <ul>
                        <li>Rate Limit: <strong>60 requests/minuto</strong></li>
                        <li>Datos cambian cada <strong>24 horas</strong></li>
                    </ul>
                </div>
                <p><strong>¿Cuántos minutos tardará completar las 1000 llamadas sin cache?</strong></p>
                <div class="mission-hint">
                    <strong>💡 Pista:</strong> Redondea hacia arriba (necesitas minutos completos)
                </div>
            `,
            type: 'numeric',
            xp: 200,
            data: { requests: 1000, rate_limit: 60 },
            validate: function(answer, data) {
                // 1000 / 60 = 16.67, rounded up = 17 minutes
                const correct = Math.ceil(data.requests / data.rate_limit);
                return Math.abs(answer - correct) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return Math.ceil(data.requests / data.rate_limit); // 17
            },
            bonusQuestion: {
                text: '¿Cuántas llamadas ahorrarías con cache de 24h si ejecutas el pipeline 4 veces al día?',
                answer: 3000 // (4-1) * 1000
            }
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Módulo 4: APIs',
            scenes: [
                {
                    id: 1,
                    content: `
                        Los datos no siempre vienen de archivos. En el mundo moderno,
                        la mayoría vienen de <strong>APIs</strong>.
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
                        "Las APIs son la forma en que los sistemas se comunican entre sí.
                        Como Data Engineer, consumirás APIs constantemente."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Tenemos un nuevo cliente: <strong>CloudAPI Systems</strong>.
                        Necesitan ayuda para integrar datos de múltiples APIs."
                    `,
                    tutorial: {
                        title: '¿Qué es una API REST?',
                        content: `
                            <ul>
                                <li><strong>API</strong>: Application Programming Interface</li>
                                <li><strong>REST</strong>: Arquitectura basada en HTTP</li>
                                <li>Usa métodos: GET, POST, PUT, DELETE</li>
                                <li>Devuelve datos en JSON o XML</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Aprenderás a consumir APIs, manejar errores,
                        y trabajar con rate limits y paginación."
                    `,
                    tutorial: {
                        title: 'Métodos HTTP',
                        content: `
                            <ul>
                                <li><strong>GET</strong>: Obtener datos</li>
                                <li><strong>POST</strong>: Crear nuevos datos</li>
                                <li><strong>PUT</strong>: Actualizar datos existentes</li>
                                <li><strong>DELETE</strong>: Eliminar datos</li>
                            </ul>
                        `
                    }
                }
            ]
        },
        company: 'CloudAPI Systems'
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Simulate an API call
     * @param {string} endpoint
     * @param {Object} params
     * @returns {Object} Simulated response
     */
    function simulateAPICall(endpoint, params = {}) {
        // Simulate latency
        const latency = Math.random() * 500 + 100;

        // Check rate limit
        if (Math.random() < 0.1) {
            return {
                status: 429,
                error: 'Too Many Requests',
                headers: {
                    'X-RateLimit-Remaining': 0,
                    'X-RateLimit-Reset': 60
                }
            };
        }

        // Return data based on endpoint
        switch (endpoint) {
            case '/api/products':
                let products = [...API_DATA.products.data];

                // Apply filters
                if (params.category) {
                    products = products.filter(p => p.category === params.category);
                }
                if (params.max_price) {
                    products = products.filter(p => p.price <= params.max_price);
                }

                // Apply pagination
                const page = params.page || 1;
                const perPage = params.per_page || 3;
                const start = (page - 1) * perPage;
                const paginatedProducts = products.slice(start, start + perPage);

                return {
                    status: 200,
                    data: paginatedProducts,
                    pagination: {
                        total: products.length,
                        per_page: perPage,
                        current_page: page,
                        total_pages: Math.ceil(products.length / perPage)
                    },
                    latency
                };

            case '/api/users':
                return {
                    status: 200,
                    data: API_DATA.users.data,
                    latency
                };

            default:
                return {
                    status: 404,
                    error: 'Not Found'
                };
        }
    }

    /**
     * Get HTTP status info
     * @param {number} code
     * @returns {Object}
     */
    function getHTTPStatus(code) {
        return HTTP_STATUS[code] || { name: 'Unknown', description: 'Código desconocido' };
    }

    /**
     * Calculate rate limit timing
     * @param {number} totalRequests
     * @param {number} rateLimit
     * @returns {Object}
     */
    function calculateRateLimitTiming(totalRequests, rateLimit) {
        const minutesNeeded = Math.ceil(totalRequests / rateLimit);
        const secondsNeeded = minutesNeeded * 60;

        return {
            minutes: minutesNeeded,
            seconds: secondsNeeded,
            formatted: `${minutesNeeded} minutos (${secondsNeeded} segundos)`
        };
    }

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(4, {
            missions: MISSIONS,
            story: STORY,
            data: API_DATA,
            httpStatus: HTTP_STATUS,
            helpers: {
                simulateAPICall,
                getHTTPStatus,
                calculateRateLimitTiming
            }
        });
        console.log('[Module4] APIs module registered');
    }

    // Expose globally for backwards compatibility
    window.Module4 = {
        MISSIONS,
        STORY,
        API_DATA,
        HTTP_STATUS,
        simulateAPICall,
        getHTTPStatus,
        calculateRateLimitTiming
    };

})();
