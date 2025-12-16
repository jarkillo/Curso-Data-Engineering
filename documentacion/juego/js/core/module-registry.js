/**
 * Module Registry - Data Engineer: The Game
 *
 * Central registry for game modules (chapters) and their missions.
 * Handles module loading, progression, and mission management.
 */

const ModuleRegistry = (function() {
    'use strict';

    // Registered modules
    const modules = new Map();

    // Module metadata
    const MODULE_INFO = {
        1: {
            id: 1,
            name: 'Estadistica',
            displayName: 'Estadistica',
            icon: '📊',
            color: '#667eea',
            description: 'Aprende los fundamentos de estadistica descriptiva',
            requiredLevel: 1,
            totalMissions: 7,
            company: 'DataFlow Industries'
        },
        2: {
            id: 2,
            name: 'SQL',
            displayName: 'SQL',
            icon: '🗃️',
            color: '#00d2ff',
            description: 'Domina el lenguaje de consulta de bases de datos',
            requiredLevel: 2,
            totalMissions: 5,
            company: 'QueryMasters Inc.'
        },
        3: {
            id: 3,
            name: 'ETL',
            displayName: 'ETL',
            icon: '🔄',
            color: '#6bcf7f',
            description: 'Extract, Transform, Load - El corazon del Data Engineering',
            requiredLevel: 3,
            totalMissions: 5,
            company: 'DataFlow Industries'
        },
        4: {
            id: 4,
            name: 'APIs',
            displayName: 'APIs',
            icon: '🌐',
            color: '#ff8b94',
            description: 'Conecta con el mundo a traves de APIs REST',
            requiredLevel: 4,
            totalMissions: 5,
            company: 'CloudAPI Systems'
        },
        5: {
            id: 5,
            name: 'Databases',
            displayName: 'Bases de Datos',
            icon: '💾',
            color: '#ffd93d',
            description: 'Diseno y optimizacion de bases de datos',
            requiredLevel: 5,
            totalMissions: 5,
            company: 'DataVault Corp'
        },
        6: {
            id: 6,
            name: 'Airflow',
            displayName: 'Apache Airflow',
            icon: '🌪️',
            color: '#4ecdc4',
            description: 'Orquestacion de pipelines de datos',
            requiredLevel: 6,
            totalMissions: 5,
            company: 'LogisticFlow'
        },
        7: {
            id: 7,
            name: 'Cloud',
            displayName: 'Cloud (AWS)',
            icon: '☁️',
            color: '#ff9500',
            description: 'Data Engineering en la nube',
            requiredLevel: 7,
            totalMissions: 5,
            company: 'CloudScale Solutions'
        },
        8: {
            id: 8,
            name: 'DataWarehouse',
            displayName: 'Data Warehousing',
            icon: '🏛️',
            color: '#a8e6cf',
            description: 'Modelado dimensional y analytics',
            requiredLevel: 8,
            totalMissions: 5,
            company: 'AnalyticsHub'
        },
        9: {
            id: 9,
            name: 'Spark',
            displayName: 'Apache Spark',
            icon: '⚡',
            color: '#ff6b6b',
            description: 'Procesamiento de Big Data',
            requiredLevel: 9,
            totalMissions: 5,
            company: 'BigData Corp'
        },
        10: {
            id: 10,
            name: 'MLOps',
            displayName: 'ML / MLOps',
            icon: '🤖',
            color: '#c7ceea',
            description: 'Machine Learning en produccion',
            requiredLevel: 10,
            totalMissions: 5,
            company: 'FinTech Analytics'
        }
    };

    /**
     * Register a module with its missions
     * @param {number} moduleId - Module number (1-10)
     * @param {Object} moduleData - Module data including missions array
     */
    function register(moduleId, moduleData) {
        if (!MODULE_INFO[moduleId]) {
            console.error('[ModuleRegistry] Invalid module ID:', moduleId);
            return;
        }

        modules.set(moduleId, {
            ...MODULE_INFO[moduleId],
            ...moduleData,
            loaded: true
        });

        console.log(`[ModuleRegistry] Module ${moduleId} registered with ${moduleData.missions?.length || 0} missions`);
    }

    /**
     * Get module by ID
     * @param {number} moduleId
     * @returns {Object|null}
     */
    function getModule(moduleId) {
        return modules.get(moduleId) || null;
    }

    /**
     * Get module info (metadata only)
     * @param {number} moduleId
     * @returns {Object|null}
     */
    function getModuleInfo(moduleId) {
        return MODULE_INFO[moduleId] || null;
    }

    /**
     * Get all registered modules
     * @returns {Array}
     */
    function getAllModules() {
        return Array.from(modules.values());
    }

    /**
     * Get all module IDs
     * @returns {Array}
     */
    function getAllModuleIds() {
        return Object.keys(MODULE_INFO).map(Number);
    }

    /**
     * Check if module is loaded
     * @param {number} moduleId
     * @returns {boolean}
     */
    function isModuleLoaded(moduleId) {
        return modules.has(moduleId);
    }

    /**
     * Get mission by ID
     * @param {string} missionId - Full mission ID (e.g., 'mission_1_1', 'sql_1')
     * @returns {Object|null}
     */
    function getMission(missionId) {
        for (const module of modules.values()) {
            if (module.missions) {
                const mission = module.missions.find(m => m.id === missionId);
                if (mission) {
                    return { ...mission, moduleId: module.id };
                }
            }
        }
        return null;
    }

    /**
     * Get missions for a module
     * @param {number} moduleId
     * @returns {Array}
     */
    function getModuleMissions(moduleId) {
        const module = modules.get(moduleId);
        return module?.missions || [];
    }

    /**
     * Get next mission in sequence
     * @param {string} currentMissionId
     * @returns {Object|null} Next mission or null if none
     */
    function getNextMission(currentMissionId) {
        const currentMission = getMission(currentMissionId);
        if (!currentMission) return null;

        const missions = getModuleMissions(currentMission.moduleId);
        const currentIndex = missions.findIndex(m => m.id === currentMissionId);

        // Try next mission in same module
        if (currentIndex < missions.length - 1) {
            return missions[currentIndex + 1];
        }

        // Try first mission of next module
        const nextModuleId = currentMission.moduleId + 1;
        if (nextModuleId <= 10) {
            const nextMissions = getModuleMissions(nextModuleId);
            if (nextMissions.length > 0) {
                return nextMissions[0];
            }
        }

        return null;
    }

    /**
     * Check if module is unlocked based on player progress
     * @param {number} moduleId
     * @param {Object} gameState - Player's game state
     * @returns {boolean}
     */
    function isModuleUnlocked(moduleId, gameState) {
        // Module 1 is always unlocked
        if (moduleId === 1) return true;

        // Check level requirement
        if (gameState.level < MODULE_INFO[moduleId]?.requiredLevel) {
            return false;
        }

        // Check if previous module is 80% complete
        const prevModuleId = moduleId - 1;
        const prevModule = modules.get(prevModuleId);
        if (!prevModule) return false;

        const prevProgress = getModuleProgress(prevModuleId, gameState);
        return prevProgress >= 0.8;
    }

    /**
     * Calculate module progress (0-1)
     * @param {number} moduleId
     * @param {Object} gameState
     * @returns {number}
     */
    function getModuleProgress(moduleId, gameState) {
        const module = modules.get(moduleId);
        if (!module || !module.missions) return 0;

        const completed = module.missions.filter(m =>
            gameState.missionsCompleted.includes(m.id)
        ).length;

        return completed / module.missions.length;
    }

    /**
     * Get total missions count
     * @returns {number}
     */
    function getTotalMissionsCount() {
        let total = 0;
        for (const module of modules.values()) {
            total += module.missions?.length || 0;
        }
        return total;
    }

    /**
     * Get completed missions count for a module
     * @param {number} moduleId
     * @param {Object} gameState
     * @returns {number}
     */
    function getCompletedMissionsCount(moduleId, gameState) {
        const module = modules.get(moduleId);
        if (!module || !module.missions) return 0;

        return module.missions.filter(m =>
            gameState.missionsCompleted.includes(m.id)
        ).length;
    }

    /**
     * Load a module script dynamically
     * @param {number} moduleId
     * @returns {Promise}
     */
    function loadModuleScript(moduleId) {
        return new Promise((resolve, reject) => {
            if (isModuleLoaded(moduleId)) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = `js/modules/module-${moduleId}.js`;
            script.onload = () => {
                console.log(`[ModuleRegistry] Module ${moduleId} script loaded`);
                resolve();
            };
            script.onerror = () => {
                reject(new Error(`Failed to load module ${moduleId}`));
            };
            document.head.appendChild(script);
        });
    }

    /**
     * Get story introduction for module
     * @param {number} moduleId
     * @returns {Object|null}
     */
    function getModuleStory(moduleId) {
        const module = modules.get(moduleId);
        return module?.story || null;
    }

    // Public API
    return {
        register,
        getModule,
        getModuleInfo,
        getAllModules,
        getAllModuleIds,
        isModuleLoaded,
        getMission,
        getModuleMissions,
        getNextMission,
        isModuleUnlocked,
        getModuleProgress,
        getTotalMissionsCount,
        getCompletedMissionsCount,
        loadModuleScript,
        getModuleStory,
        MODULE_INFO
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModuleRegistry;
}
