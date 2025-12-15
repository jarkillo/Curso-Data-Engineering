/**
 * Module 1: Statistics - Data Engineer: The Game
 *
 * Missions covering basic statistics concepts:
 * - Mean (average)
 * - Median
 * - Mode
 * - Variance and Standard Deviation
 */

(function() {
    'use strict';

    // ==========================================
    // MISSION DATA
    // ==========================================

    // Mission 1: Mean calculation
    const MISSION_1_DATA = {
        ventas: [145.30, 132.50, 189.75, 156.20, 198.50, 234.80, 175.40],
        dias: ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
        objetivo: 170,
        xp: 100
    };

    // Mission 2A: Outliers (evident)
    const MISSION_2A_DATA = {
        ventas: [50, 60, 55, 58, 500, 52, 57],
        dias: ['Suc 1', 'Suc 2', 'Suc 3', 'Suc 4', 'Suc 5', 'Suc 6', 'Suc 7'],
        xp: 75
    };

    // Mission 2B: Outliers (subtle)
    const MISSION_2B_DATA = {
        ventas: [120, 135, 128, 200, 125, 132, 210, 130, 122],
        dias: ['Suc 1', 'Suc 2', 'Suc 3', 'Suc 4', 'Suc 5', 'Suc 6', 'Suc 7', 'Suc 8', 'Suc 9'],
        xp: 125
    };

    // Mission 3A: Mode (simple)
    const MISSION_3A_DATA = {
        ventas: [
            { producto: 'Camiseta Azul', talla: 'M', cantidad: 45 },
            { producto: 'Camiseta Azul', talla: 'L', cantidad: 32 },
            { producto: 'Camiseta Azul', talla: 'S', cantidad: 28 },
            { producto: 'Camiseta Azul', talla: 'XL', cantidad: 15 },
            { producto: 'Camiseta Azul', talla: 'M', cantidad: 38 }
        ],
        xp: 100
    };

    // Mission 3B: Mode (bimodal)
    const MISSION_3B_DATA = {
        ventas: [
            { tienda: 'Tienda 1', talla_mas_vendida: 'M', unidades: 45 },
            { tienda: 'Tienda 2', talla_mas_vendida: 'L', unidades: 43 },
            { tienda: 'Tienda 3', talla_mas_vendida: 'M', unidades: 41 },
            { tienda: 'Tienda 4', talla_mas_vendida: 'L', unidades: 42 },
            { tienda: 'Tienda 5', talla_mas_vendida: 'M', unidades: 38 },
            { tienda: 'Tienda 6', talla_mas_vendida: 'L', unidades: 44 },
            { tienda: 'Tienda 7', talla_mas_vendida: 'S', unidades: 25 }
        ],
        xp: 175  // 150 + 25 bonus
    };

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Calculate median of an array
     * @param {Array} datos - Array of numbers
     * @returns {number}
     */
    function calcularMediana(datos) {
        const ordenados = [...datos].sort((a, b) => a - b);
        const n = ordenados.length;

        if (n % 2 === 0) {
            return (ordenados[n / 2 - 1] + ordenados[n / 2]) / 2;
        } else {
            return ordenados[Math.floor(n / 2)];
        }
    }

    /**
     * Detect outliers using IQR method
     * @param {Array} datos - Array of numbers
     * @returns {Array} Indices of outliers
     */
    function detectarOutliersIQR(datos) {
        const ordenados = [...datos].sort((a, b) => a - b);
        const n = ordenados.length;

        const q1Index = Math.floor(n * 0.25);
        const q3Index = Math.floor(n * 0.75);
        const q1 = ordenados[q1Index];
        const q3 = ordenados[q3Index];
        const iqr = q3 - q1;

        const limiteInferior = q1 - 1.5 * iqr;
        const limiteSuperior = q3 + 1.5 * iqr;

        return datos.map((valor, index) =>
            valor < limiteInferior || valor > limiteSuperior ? index : null
        ).filter(index => index !== null);
    }

    /**
     * Calculate mode of an array
     * @param {Array} datos - Array of values
     * @returns {Object} Mode info
     */
    function calcularModa(datos) {
        const frequencies = {};
        datos.forEach(valor => {
            frequencies[valor] = (frequencies[valor] || 0) + 1;
        });

        const maxFreq = Math.max(...Object.values(frequencies));
        const modas = Object.entries(frequencies)
            .filter(([_, freq]) => freq === maxFreq)
            .map(([valor, _]) => valor);

        return {
            modas: modas,
            frequencies: frequencies,
            maxFrequency: maxFreq,
            esBimodal: modas.length === 2,
            esMultimodal: modas.length > 2,
            esUnimodal: modas.length === 1
        };
    }

    // ==========================================
    // MISSION DEFINITIONS
    // ==========================================

    const MISSIONS = [
        {
            id: 'mission_1_1',
            title: 'Mision 1: Calcular la Media',
            description: `
                <p><strong>Cliente: RestaurantData Co.</strong></p>
                <p>Calcula el <strong>promedio (media)</strong> de ventas de la semana.</p>
                <p>Objetivo del cliente: 170 EUR/dia</p>
            `,
            type: 'numeric',
            xp: 100,
            data: MISSION_1_DATA,
            validate: function(answer, data) {
                const sum = data.ventas.reduce((a, b) => a + b, 0);
                const correct = sum / data.ventas.length;
                return Math.abs(answer - correct) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return data.ventas.reduce((a, b) => a + b, 0) / data.ventas.length;
            }
        },
        {
            id: 'mission_2a',
            title: 'Mision 2A: Detectar Outliers Evidentes',
            description: `
                <p><strong>Cliente: RestaurantData Co.</strong></p>
                <p>Calcula la <strong>mediana</strong> de las ventas de 7 sucursales.</p>
                <p style="color: #ff4757;">Una sucursal tiene un error evidente (marcada en rojo).</p>
            `,
            type: 'numeric',
            xp: 75,
            data: MISSION_2A_DATA,
            validate: function(answer, data) {
                const correct = calcularMediana(data.ventas);
                return Math.abs(answer - correct) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return calcularMediana(data.ventas);
            }
        },
        {
            id: 'mission_2b',
            title: 'Mision 2B: Outliers Sutiles (Avanzado)',
            description: `
                <p><strong>Cliente: RestaurantData Co. (Zona Premium)</strong></p>
                <p>Calcula la <strong>mediana</strong> de las ventas de 9 sucursales.</p>
                <p style="color: #ff4757;">Los outliers son mas sutiles. Detectados con IQR.</p>
            `,
            type: 'numeric',
            xp: 125,
            data: MISSION_2B_DATA,
            validate: function(answer, data) {
                const correct = calcularMediana(data.ventas);
                return Math.abs(answer - correct) < 0.5;
            },
            getCorrectAnswer: function(data) {
                return calcularMediana(data.ventas);
            }
        },
        {
            id: 'mission_3a',
            title: 'Mision 3A: Identificar la Talla Mas Vendida',
            description: `
                <p><strong>Cliente: TrendyShop Analytics</strong></p>
                <p>Analiza las ventas e identifica la <strong>talla MAS VENDIDA</strong>.</p>
                <p style="opacity: 0.8;">Pista: Cuenta la frecuencia, no sumes unidades.</p>
            `,
            type: 'text',
            xp: 100,
            data: MISSION_3A_DATA,
            validate: function(answer, data) {
                const normalized = answer.trim().toUpperCase();
                return ['M', 'MEDIANA', 'MEDIUM'].includes(normalized);
            }
        },
        {
            id: 'mission_3b',
            title: 'Mision 3B: Distribucion Bimodal (Avanzado)',
            description: `
                <p><strong>Cliente: TrendyShop Analytics (Zona Premium)</strong></p>
                <p>Identifica la(s) <strong>talla(s) MAS FRECUENTE(s)</strong>.</p>
                <p>Si hay DOS modas, reporta ambas separadas por coma (ej: "M,L").</p>
            `,
            type: 'text',
            xp: 175,
            data: MISSION_3B_DATA,
            validate: function(answer, data) {
                const normalized = answer
                    .toUpperCase()
                    .replace(/\s+/g, '')
                    .replace(/Y/g, ',')
                    .split(',')
                    .filter(x => x.length > 0)
                    .sort()
                    .join(',');
                return ['L,M', 'M,L'].includes(normalized);
            }
        },
        {
            id: 'mission_5a',
            title: 'Mision 5A: Varianza - Comparar Consistencia',
            description: `
                <p><strong>Cliente: LogisticFlow</strong></p>
                <p>Compara la consistencia de dos proveedores usando varianza.</p>
            `,
            type: 'choice',
            xp: 150,
            data: {
                proveedorA: [48, 52, 49, 51, 50, 48, 52, 50, 49, 51],
                proveedorB: [35, 60, 45, 55, 40, 65, 42, 58, 38, 62]
            }
        },
        {
            id: 'mission_5b',
            title: 'Mision 5B: Desviacion Estandar',
            description: `
                <p><strong>Cliente: LogisticFlow</strong></p>
                <p>Calcula la desviacion estandar para evaluar riesgo.</p>
            `,
            type: 'numeric',
            xp: 200,
            data: {}
        }
    ];

    // ==========================================
    // STORY CONTENT
    // ==========================================

    const STORY = {
        intro: {
            title: 'Tu Historia Comienza...',
            scenes: [
                {
                    id: 1,
                    content: `
                        Has estado buscando trabajo como Data Engineer durante meses.
                        Finalmente recibiste un email de <strong>DataFlow Industries</strong>.
                        Hoy es tu <strong>primer dia</strong>.
                    `
                },
                {
                    id: 2,
                    character: {
                        name: 'Maria Gonzalez',
                        role: 'Lead Data Engineer | Tu Mentora',
                        avatar: '👩‍💼'
                    },
                    content: `
                        "Hola! Bienvenido/a al equipo. Soy Maria, sere tu mentora.
                        Todos empezamos desde cero. Te voy a ensenar todo, paso a paso."
                    `
                },
                {
                    id: 3,
                    content: `
                        "Tenemos un nuevo cliente: <strong>RestaurantData Co.</strong>
                        Necesitan analizar sus datos de ventas. Aqui es donde entramos nosotros."
                    `,
                    tutorial: {
                        title: 'Que hace un Data Engineer?',
                        content: `
                            <ul>
                                <li>Recopilar datos de diferentes fuentes</li>
                                <li>Transformar datos en informacion util</li>
                                <li>Analizar patrones y tendencias</li>
                                <li>Asegurar la calidad de los datos</li>
                            </ul>
                        `
                    }
                },
                {
                    id: 4,
                    content: `
                        "Para empezar, te voy a ensenar la <strong>MEDIA</strong> (promedio).
                        RestaurantData Co. quiere saber si cumplen su objetivo de 170 EUR/dia."
                    `,
                    tutorial: {
                        title: 'Que es la Media?',
                        content: `
                            La <strong>media</strong> es el valor promedio de un conjunto de datos.
                            <br><br>
                            <strong>Formula:</strong> Media = Suma de todos los valores / Cantidad de valores
                        `
                    }
                }
            ]
        },
        company: 'DataFlow Industries'
    };

    // ==========================================
    // MODULE REGISTRATION
    // ==========================================

    // Register with ModuleRegistry if available
    if (typeof ModuleRegistry !== 'undefined') {
        ModuleRegistry.register(1, {
            missions: MISSIONS,
            story: STORY,
            helpers: {
                calcularMediana,
                detectarOutliersIQR,
                calcularModa
            },
            data: {
                MISSION_1_DATA,
                MISSION_2A_DATA,
                MISSION_2B_DATA,
                MISSION_3A_DATA,
                MISSION_3B_DATA
            }
        });
        console.log('[Module1] Statistics module registered');
    }

    // Expose globally for backwards compatibility
    window.Module1 = {
        MISSIONS,
        STORY,
        calcularMediana,
        detectarOutliersIQR,
        calcularModa,
        MISSION_1_DATA,
        MISSION_2A_DATA,
        MISSION_2B_DATA,
        MISSION_3A_DATA,
        MISSION_3B_DATA
    };

})();
