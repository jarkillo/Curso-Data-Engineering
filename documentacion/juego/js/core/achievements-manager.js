/**
 * Achievements Manager - Data Engineer: The Game
 *
 * Handles achievement tracking, unlocking, and display.
 * Achievements provide extra motivation and recognize milestones.
 */

(function() {
    'use strict';

    // ==========================================
    // ACHIEVEMENT DEFINITIONS
    // ==========================================

    const ACHIEVEMENTS = {
        // Progression achievements
        first_mission: {
            id: 'first_mission',
            title: 'Primeros Pasos',
            description: 'Completa tu primera misión',
            icon: '🎯',
            xpBonus: 50,
            category: 'progression',
            secret: false
        },
        module_complete_1: {
            id: 'module_complete_1',
            title: 'Estadístico',
            description: 'Completa el Módulo 1: Estadística',
            icon: '📊',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_2: {
            id: 'module_complete_2',
            title: 'SQL Master',
            description: 'Completa el Módulo 2: SQL',
            icon: '🗄️',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_3: {
            id: 'module_complete_3',
            title: 'Pipeline Builder',
            description: 'Completa el Módulo 3: ETL',
            icon: '🔄',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_4: {
            id: 'module_complete_4',
            title: 'API Expert',
            description: 'Completa el Módulo 4: APIs',
            icon: '🌐',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_5: {
            id: 'module_complete_5',
            title: 'Database Architect',
            description: 'Completa el Módulo 5: Bases de Datos',
            icon: '💾',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_6: {
            id: 'module_complete_6',
            title: 'Orchestrator',
            description: 'Completa el Módulo 6: Airflow',
            icon: '🎼',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_7: {
            id: 'module_complete_7',
            title: 'Cloud Native',
            description: 'Completa el Módulo 7: Cloud',
            icon: '☁️',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_8: {
            id: 'module_complete_8',
            title: 'Warehouse Designer',
            description: 'Completa el Módulo 8: Data Warehousing',
            icon: '🏛️',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_9: {
            id: 'module_complete_9',
            title: 'Spark Champion',
            description: 'Completa el Módulo 9: Spark',
            icon: '⚡',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        module_complete_10: {
            id: 'module_complete_10',
            title: 'ML Engineer',
            description: 'Completa el Módulo 10: ML/MLOps',
            icon: '🤖',
            xpBonus: 200,
            category: 'progression',
            secret: false
        },
        all_modules: {
            id: 'all_modules',
            title: 'Data Engineer Completo',
            description: 'Completa los 10 módulos',
            icon: '🏆',
            xpBonus: 1000,
            category: 'progression',
            secret: false
        },

        // Performance achievements
        perfect_module: {
            id: 'perfect_module',
            title: 'Perfeccionista',
            description: 'Completa un módulo sin fallar ninguna misión',
            icon: '💎',
            xpBonus: 300,
            category: 'performance',
            secret: false
        },
        speed_demon: {
            id: 'speed_demon',
            title: 'Velocista',
            description: 'Completa 5 misiones en menos de 10 minutos',
            icon: '⚡',
            xpBonus: 150,
            category: 'performance',
            secret: false
        },
        streak_5: {
            id: 'streak_5',
            title: 'En Racha',
            description: 'Completa 5 misiones consecutivas correctamente',
            icon: '🔥',
            xpBonus: 100,
            category: 'performance',
            secret: false
        },
        streak_10: {
            id: 'streak_10',
            title: 'Imparable',
            description: 'Completa 10 misiones consecutivas correctamente',
            icon: '💪',
            xpBonus: 250,
            category: 'performance',
            secret: false
        },

        // Exploration achievements
        first_hint: {
            id: 'first_hint',
            title: 'Curioso',
            description: 'Usa una pista por primera vez',
            icon: '💡',
            xpBonus: 25,
            category: 'exploration',
            secret: false
        },
        no_hints_module: {
            id: 'no_hints_module',
            title: 'Autodidacta',
            description: 'Completa un módulo sin usar pistas',
            icon: '🧠',
            xpBonus: 200,
            category: 'exploration',
            secret: false
        },

        // XP milestones
        xp_1000: {
            id: 'xp_1000',
            title: 'Junior',
            description: 'Alcanza 1,000 XP',
            icon: '🌱',
            xpBonus: 100,
            category: 'milestone',
            secret: false
        },
        xp_5000: {
            id: 'xp_5000',
            title: 'Mid-Level',
            description: 'Alcanza 5,000 XP',
            icon: '🌿',
            xpBonus: 250,
            category: 'milestone',
            secret: false
        },
        xp_10000: {
            id: 'xp_10000',
            title: 'Senior',
            description: 'Alcanza 10,000 XP',
            icon: '🌳',
            xpBonus: 500,
            category: 'milestone',
            secret: false
        },

        // Secret achievements
        night_owl: {
            id: 'night_owl',
            title: 'Noctámbulo',
            description: 'Juega después de medianoche',
            icon: '🦉',
            xpBonus: 50,
            category: 'secret',
            secret: true
        },
        early_bird: {
            id: 'early_bird',
            title: 'Madrugador',
            description: 'Juega antes de las 6 AM',
            icon: '🐦',
            xpBonus: 50,
            category: 'secret',
            secret: true
        },
        comeback: {
            id: 'comeback',
            title: 'El Regreso',
            description: 'Vuelve después de 7 días sin jugar',
            icon: '🔙',
            xpBonus: 100,
            category: 'secret',
            secret: true
        }
    };

    // ==========================================
    // STATE MANAGEMENT
    // ==========================================

    let unlockedAchievements = [];
    let achievementQueue = []; // For showing notifications
    let currentStreak = 0;
    let sessionStartTime = Date.now();
    let missionsThisSession = 0;

    // ==========================================
    // CORE FUNCTIONS
    // ==========================================

    /**
     * Initialize achievements from storage
     */
    function init() {
        loadAchievements();
        checkTimeBasedAchievements();
        console.log('[Achievements] Initialized with', unlockedAchievements.length, 'unlocked');
    }

    /**
     * Load achievements from storage
     */
    function loadAchievements() {
        if (typeof StorageManager !== 'undefined') {
            const state = StorageManager.getGameState();
            unlockedAchievements = state.achievements || [];
            currentStreak = state.currentStreak || 0;
        } else {
            const saved = localStorage.getItem('dataEngineerGame');
            if (saved) {
                const state = JSON.parse(saved);
                unlockedAchievements = state.achievements || [];
                currentStreak = state.currentStreak || 0;
            }
        }
    }

    /**
     * Save achievements to storage
     */
    function saveAchievements() {
        if (typeof StorageManager !== 'undefined') {
            StorageManager.updateGameState({
                achievements: unlockedAchievements,
                currentStreak: currentStreak
            });
        } else {
            const saved = localStorage.getItem('dataEngineerGame');
            const state = saved ? JSON.parse(saved) : {};
            state.achievements = unlockedAchievements;
            state.currentStreak = currentStreak;
            localStorage.setItem('dataEngineerGame', JSON.stringify(state));
        }
    }

    /**
     * Check if achievement is unlocked
     * @param {string} achievementId
     * @returns {boolean}
     */
    function isUnlocked(achievementId) {
        return unlockedAchievements.includes(achievementId);
    }

    /**
     * Unlock an achievement
     * @param {string} achievementId
     * @returns {Object|null} Achievement data if newly unlocked
     */
    function unlock(achievementId) {
        if (isUnlocked(achievementId)) {
            return null;
        }

        const achievement = ACHIEVEMENTS[achievementId];
        if (!achievement) {
            console.warn('[Achievements] Unknown achievement:', achievementId);
            return null;
        }

        unlockedAchievements.push(achievementId);
        saveAchievements();

        // Add to notification queue
        achievementQueue.push(achievement);

        // Award bonus XP
        if (typeof GameEngine !== 'undefined' && achievement.xpBonus) {
            GameEngine.addXP(achievement.xpBonus);
        }

        console.log('[Achievements] Unlocked:', achievement.title);
        return achievement;
    }

    /**
     * Get next achievement notification from queue
     * @returns {Object|null}
     */
    function getNextNotification() {
        return achievementQueue.shift() || null;
    }

    /**
     * Check for time-based achievements
     */
    function checkTimeBasedAchievements() {
        const hour = new Date().getHours();

        if (hour >= 0 && hour < 5) {
            unlock('night_owl');
        }
        if (hour >= 4 && hour < 6) {
            unlock('early_bird');
        }

        // Check comeback achievement
        if (typeof StorageManager !== 'undefined') {
            const state = StorageManager.getGameState();
            const lastPlayed = state.lastPlayedTimestamp;
            if (lastPlayed) {
                const daysSince = (Date.now() - lastPlayed) / (1000 * 60 * 60 * 24);
                if (daysSince >= 7) {
                    unlock('comeback');
                }
            }
        }
    }

    // ==========================================
    // EVENT HANDLERS
    // ==========================================

    /**
     * Called when a mission is completed
     * @param {string} missionId
     * @param {boolean} correct
     * @param {boolean} usedHint
     */
    function onMissionComplete(missionId, correct, usedHint) {
        missionsThisSession++;

        // First mission
        if (missionsThisSession === 1 && correct) {
            unlock('first_mission');
        }

        // First hint
        if (usedHint) {
            unlock('first_hint');
        }

        // Streak tracking
        if (correct) {
            currentStreak++;
            if (currentStreak >= 5) {
                unlock('streak_5');
            }
            if (currentStreak >= 10) {
                unlock('streak_10');
            }
        } else {
            currentStreak = 0;
        }

        // Speed demon check
        const sessionMinutes = (Date.now() - sessionStartTime) / (1000 * 60);
        if (missionsThisSession >= 5 && sessionMinutes <= 10) {
            unlock('speed_demon');
        }

        saveAchievements();
    }

    /**
     * Called when a module is completed
     * @param {number} moduleId
     * @param {number} missionsCorrect
     * @param {number} totalMissions
     * @param {boolean} usedHints
     */
    function onModuleComplete(moduleId, missionsCorrect, totalMissions, usedHints) {
        // Module-specific achievement
        const moduleAchievement = `module_complete_${moduleId}`;
        unlock(moduleAchievement);

        // Perfect module
        if (missionsCorrect === totalMissions) {
            unlock('perfect_module');
        }

        // No hints module
        if (!usedHints) {
            unlock('no_hints_module');
        }

        // Check all modules complete
        let allComplete = true;
        for (let i = 1; i <= 10; i++) {
            if (!isUnlocked(`module_complete_${i}`)) {
                allComplete = false;
                break;
            }
        }
        if (allComplete) {
            unlock('all_modules');
        }
    }

    /**
     * Called when XP changes
     * @param {number} totalXP
     */
    function onXPChange(totalXP) {
        if (totalXP >= 1000) {
            unlock('xp_1000');
        }
        if (totalXP >= 5000) {
            unlock('xp_5000');
        }
        if (totalXP >= 10000) {
            unlock('xp_10000');
        }
    }

    // ==========================================
    // UI FUNCTIONS
    // ==========================================

    /**
     * Show achievement notification
     * @param {Object} achievement
     */
    function showNotification(achievement) {
        const container = document.createElement('div');
        container.className = 'achievement-notification';
        container.innerHTML = `
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-info">
                <div class="achievement-unlocked">Logro Desbloqueado!</div>
                <div class="achievement-title">${achievement.title}</div>
                <div class="achievement-desc">${achievement.description}</div>
                ${achievement.xpBonus ? `<div class="achievement-xp">+${achievement.xpBonus} XP</div>` : ''}
            </div>
        `;

        document.body.appendChild(container);

        // Animate in
        setTimeout(() => container.classList.add('show'), 100);

        // Remove after 4 seconds
        setTimeout(() => {
            container.classList.remove('show');
            setTimeout(() => container.remove(), 500);
        }, 4000);
    }

    /**
     * Process notification queue
     */
    function processNotificationQueue() {
        const achievement = getNextNotification();
        if (achievement) {
            showNotification(achievement);
            // Process next after delay
            setTimeout(processNotificationQueue, 4500);
        }
    }

    /**
     * Get all achievements for display
     * @returns {Array}
     */
    function getAllAchievements() {
        return Object.values(ACHIEVEMENTS).map(ach => ({
            ...ach,
            unlocked: isUnlocked(ach.id)
        }));
    }

    /**
     * Get achievements by category
     * @param {string} category
     * @returns {Array}
     */
    function getByCategory(category) {
        return getAllAchievements().filter(ach =>
            ach.category === category && (!ach.secret || ach.unlocked)
        );
    }

    /**
     * Get achievement stats
     * @returns {Object}
     */
    function getStats() {
        const all = Object.values(ACHIEVEMENTS);
        const unlocked = unlockedAchievements.length;
        const visible = all.filter(a => !a.secret || isUnlocked(a.id)).length;
        const totalXPBonus = unlockedAchievements.reduce((sum, id) => {
            const ach = ACHIEVEMENTS[id];
            return sum + (ach ? ach.xpBonus : 0);
        }, 0);

        return {
            unlocked,
            total: all.length,
            visible,
            percentage: Math.round((unlocked / all.length) * 100),
            totalXPBonus
        };
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    window.AchievementsManager = {
        init,
        isUnlocked,
        unlock,
        onMissionComplete,
        onModuleComplete,
        onXPChange,
        showNotification,
        processNotificationQueue,
        getAllAchievements,
        getByCategory,
        getStats,
        ACHIEVEMENTS
    };

    console.log('[AchievementsManager] Module loaded');

})();
