/**
 * Storage Manager - Data Engineer: The Game
 *
 * Handles localStorage operations with backwards compatibility
 * for existing save games and migration to new format.
 *
 * Save Format v2:
 * - 'dataEngineerGame' (JSON): Main game state
 * - 'gameConfig' (JSON): Settings (sounds, animations, volume)
 *
 * Legacy Format (v1):
 * - Individual keys: playerName, level, xp, totalXP, missionsCompleted
 */

const StorageManager = (function() {
    'use strict';

    // Storage keys
    const KEYS = {
        GAME_STATE: 'dataEngineerGame',
        CONFIG: 'gameConfig',
        // Legacy keys (v1)
        LEGACY: {
            PLAYER_NAME: 'playerName',
            LEVEL: 'level',
            XP: 'xp',
            TOTAL_XP: 'totalXP',
            MISSIONS_COMPLETED: 'missionsCompleted'
        }
    };

    // Default game state
    const DEFAULT_GAME_STATE = {
        version: 2,
        playerName: '',
        level: 1,
        xp: 0,
        totalXP: 0,
        currentModule: 1,
        missionsCompleted: [],
        moduleProgress: {},
        achievements: [],
        statistics: {
            totalPlayTime: 0,
            missionsAttempted: 0,
            hintsUsed: 0
        },
        lastPlayed: null
    };

    // Default config
    const DEFAULT_CONFIG = {
        soundsEnabled: true,
        animationsEnabled: true,
        volume: 0.5
    };

    /**
     * Check if legacy save exists
     * @returns {boolean}
     */
    function hasLegacySave() {
        return localStorage.getItem(KEYS.LEGACY.PLAYER_NAME) !== null;
    }

    /**
     * Check if new format save exists
     * @returns {boolean}
     */
    function hasSave() {
        return localStorage.getItem(KEYS.GAME_STATE) !== null || hasLegacySave();
    }

    /**
     * Migrate legacy save to new format
     * @returns {Object} Migrated game state
     */
    function migrateLegacySave() {
        console.log('[StorageManager] Migrating legacy save to v2 format...');

        const legacyState = {
            version: 2,
            playerName: localStorage.getItem(KEYS.LEGACY.PLAYER_NAME) || '',
            level: parseInt(localStorage.getItem(KEYS.LEGACY.LEVEL)) || 1,
            xp: parseInt(localStorage.getItem(KEYS.LEGACY.XP)) || 0,
            totalXP: parseInt(localStorage.getItem(KEYS.LEGACY.TOTAL_XP)) || 0,
            currentModule: 1,
            missionsCompleted: JSON.parse(localStorage.getItem(KEYS.LEGACY.MISSIONS_COMPLETED) || '[]'),
            moduleProgress: {},
            achievements: [],
            statistics: {
                totalPlayTime: 0,
                missionsAttempted: 0,
                hintsUsed: 0
            },
            lastPlayed: new Date().toISOString()
        };

        // Calculate module progress from completed missions
        legacyState.moduleProgress = calculateModuleProgress(legacyState.missionsCompleted);

        // Save in new format
        saveGameState(legacyState);

        // Clean up legacy keys (optional - keep for safety)
        // clearLegacyKeys();

        console.log('[StorageManager] Migration complete:', legacyState);
        return legacyState;
    }

    /**
     * Calculate module progress from completed missions
     * @param {Array} completedMissions - Array of mission IDs
     * @returns {Object} Module progress object
     */
    function calculateModuleProgress(completedMissions) {
        const progress = {};

        completedMissions.forEach(missionId => {
            // Extract module number from mission ID
            // Format: 'mission_X_Y' or 'mission_Xa' or 'sql_1' etc.
            let moduleNum = 1; // Default to module 1

            if (missionId.startsWith('mission_1') || missionId.startsWith('mission_2') ||
                missionId.startsWith('mission_3') || missionId.startsWith('mission_4') ||
                missionId.startsWith('mission_5')) {
                moduleNum = 1; // Statistics missions
            } else if (missionId.startsWith('sql_')) {
                moduleNum = 2;
            } else if (missionId.startsWith('etl_')) {
                moduleNum = 3;
            } else if (missionId.startsWith('api_')) {
                moduleNum = 4;
            } else if (missionId.startsWith('db_')) {
                moduleNum = 5;
            } else if (missionId.startsWith('airflow_')) {
                moduleNum = 6;
            } else if (missionId.startsWith('cloud_')) {
                moduleNum = 7;
            } else if (missionId.startsWith('dwh_')) {
                moduleNum = 8;
            } else if (missionId.startsWith('spark_')) {
                moduleNum = 9;
            } else if (missionId.startsWith('ml_')) {
                moduleNum = 10;
            }

            if (!progress[moduleNum]) {
                progress[moduleNum] = {
                    completed: [],
                    unlocked: true
                };
            }
            progress[moduleNum].completed.push(missionId);
        });

        return progress;
    }

    /**
     * Load game state from storage
     * @returns {Object} Game state object
     */
    function loadGameState() {
        // Check for new format first
        const savedState = localStorage.getItem(KEYS.GAME_STATE);

        if (savedState) {
            try {
                const state = JSON.parse(savedState);
                console.log('[StorageManager] Loaded game state v' + (state.version || 1));
                return { ...DEFAULT_GAME_STATE, ...state };
            } catch (e) {
                console.error('[StorageManager] Error parsing saved state:', e);
                return { ...DEFAULT_GAME_STATE };
            }
        }

        // Check for legacy save
        if (hasLegacySave()) {
            return migrateLegacySave();
        }

        // No save found
        console.log('[StorageManager] No save found, returning default state');
        return { ...DEFAULT_GAME_STATE };
    }

    /**
     * Save game state to storage
     * @param {Object} state - Game state to save
     */
    function saveGameState(state) {
        state.lastPlayed = new Date().toISOString();

        try {
            localStorage.setItem(KEYS.GAME_STATE, JSON.stringify(state));

            // Also maintain legacy keys for backwards compatibility
            localStorage.setItem(KEYS.LEGACY.PLAYER_NAME, state.playerName);
            localStorage.setItem(KEYS.LEGACY.LEVEL, state.level);
            localStorage.setItem(KEYS.LEGACY.XP, state.xp);
            localStorage.setItem(KEYS.LEGACY.TOTAL_XP, state.totalXP);
            localStorage.setItem(KEYS.LEGACY.MISSIONS_COMPLETED, JSON.stringify(state.missionsCompleted));

            console.log('[StorageManager] Game saved');
        } catch (e) {
            console.error('[StorageManager] Error saving game:', e);
        }
    }

    /**
     * Load configuration from storage
     * @returns {Object} Config object
     */
    function loadConfig() {
        const savedConfig = localStorage.getItem(KEYS.CONFIG);

        if (savedConfig) {
            try {
                return { ...DEFAULT_CONFIG, ...JSON.parse(savedConfig) };
            } catch (e) {
                console.error('[StorageManager] Error parsing config:', e);
            }
        }

        return { ...DEFAULT_CONFIG };
    }

    /**
     * Save configuration to storage
     * @param {Object} config - Config object to save
     */
    function saveConfig(config) {
        try {
            localStorage.setItem(KEYS.CONFIG, JSON.stringify(config));
            console.log('[StorageManager] Config saved');
        } catch (e) {
            console.error('[StorageManager] Error saving config:', e);
        }
    }

    /**
     * Clear all game data (reset)
     */
    function clearAllData() {
        localStorage.removeItem(KEYS.GAME_STATE);
        localStorage.removeItem(KEYS.CONFIG);

        // Clear legacy keys
        Object.values(KEYS.LEGACY).forEach(key => {
            localStorage.removeItem(key);
        });

        console.log('[StorageManager] All game data cleared');
    }

    /**
     * Export save data for backup
     * @returns {string} JSON string of save data
     */
    function exportSave() {
        const data = {
            gameState: loadGameState(),
            config: loadConfig(),
            exportDate: new Date().toISOString()
        };
        return JSON.stringify(data, null, 2);
    }

    /**
     * Import save data from backup
     * @param {string} jsonString - JSON string of save data
     * @returns {boolean} Success status
     */
    function importSave(jsonString) {
        try {
            const data = JSON.parse(jsonString);

            if (data.gameState) {
                saveGameState(data.gameState);
            }
            if (data.config) {
                saveConfig(data.config);
            }

            console.log('[StorageManager] Save imported successfully');
            return true;
        } catch (e) {
            console.error('[StorageManager] Error importing save:', e);
            return false;
        }
    }

    /**
     * Get player name (quick access)
     * @returns {string} Player name or empty string
     */
    function getPlayerName() {
        return localStorage.getItem(KEYS.LEGACY.PLAYER_NAME) || '';
    }

    // Public API
    return {
        hasSave,
        hasLegacySave,
        loadGameState,
        saveGameState,
        loadConfig,
        saveConfig,
        clearAllData,
        exportSave,
        importSave,
        getPlayerName,
        DEFAULT_GAME_STATE,
        DEFAULT_CONFIG
    };
})();

// Export for ES modules (if supported)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StorageManager;
}
