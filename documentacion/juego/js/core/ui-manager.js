/**
 * UI Manager - Data Engineer: The Game
 *
 * Handles all DOM manipulations, screen transitions,
 * and visual feedback (animations, confetti, etc.)
 */

const UIManager = (function() {
    'use strict';

    // Configuration
    let config = {
        animationsEnabled: true
    };

    // Screen references
    const SCREENS = {
        START: 'startScreen',
        STORY: 'storyScreen',
        GAME: 'gameScreen',
        MODULE_SELECT: 'moduleSelectScreen'
    };

    // Current active screen
    let currentScreen = SCREENS.START;

    /**
     * Show a specific screen, hide others
     * @param {string} screenId - ID of screen to show
     */
    function showScreen(screenId) {
        Object.values(SCREENS).forEach(id => {
            const screen = document.getElementById(id);
            if (screen) {
                screen.style.display = id === screenId ? 'block' : 'none';
            }
        });

        currentScreen = screenId;
        console.log('[UIManager] Showing screen:', screenId);

        // Special handling for different screens
        if (screenId === SCREENS.START) {
            document.getElementById(SCREENS.START).style.display = 'flex';
        }
    }

    /**
     * Get current active screen
     * @returns {string}
     */
    function getCurrentScreen() {
        return currentScreen;
    }

    /**
     * Show modal by ID
     * @param {string} modalId
     */
    function showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            modal.style.display = 'flex';

            // Focus first input if exists
            const firstInput = modal.querySelector('input');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    /**
     * Hide modal by ID
     * @param {string} modalId
     */
    function hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }
    }

    /**
     * Show story scene by number
     * @param {number} sceneNum
     */
    function showScene(sceneNum) {
        document.querySelectorAll('.story-scene').forEach(scene => {
            scene.classList.remove('active');
        });

        const scene = document.getElementById('scene' + sceneNum);
        if (scene) {
            scene.classList.add('active');
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    /**
     * Update player stats display
     * @param {Object} stats - { name, level, xp, totalXP }
     */
    function updatePlayerStats(stats) {
        if (stats.name !== undefined) {
            const nameEl = document.getElementById('playerName');
            if (nameEl) nameEl.textContent = stats.name;
        }

        if (stats.level !== undefined) {
            const levelEl = document.getElementById('playerLevel');
            if (levelEl) levelEl.textContent = stats.level;
        }

        // Update all player name placeholders in story
        if (stats.name) {
            document.querySelectorAll('[id^="playerNameStory"]').forEach(el => {
                el.textContent = stats.name;
            });
        }
    }

    /**
     * Update XP bar display
     * @param {number} currentXP - Current XP in level
     * @param {number} xpNeeded - XP needed for next level
     */
    function updateXPBar(currentXP, xpNeeded) {
        const xpBar = document.getElementById('xpBar');
        if (!xpBar) return;

        const percentage = Math.min((currentXP / xpNeeded) * 100, 100);
        xpBar.style.width = percentage + '%';
        xpBar.textContent = `${currentXP}/${xpNeeded} XP`;
    }

    /**
     * Show feedback message
     * @param {string} message - HTML content
     * @param {string} type - 'success' or 'error'
     */
    function showFeedback(message, type = 'success') {
        const feedback = document.getElementById('feedback');
        if (!feedback) return;

        feedback.className = 'feedback ' + type;
        feedback.innerHTML = message;
        feedback.style.display = 'block';

        // Scroll to feedback
        feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Hide feedback message
     */
    function hideFeedback() {
        const feedback = document.getElementById('feedback');
        if (feedback) {
            feedback.style.display = 'none';
        }
    }

    /**
     * Show confetti animation
     */
    function showConfetti() {
        if (!config.animationsEnabled) return;

        for (let i = 0; i < 50; i++) {
            setTimeout(() => createConfettiParticle(), i * 20);
        }
    }

    /**
     * Create a single confetti particle
     */
    function createConfettiParticle() {
        const particle = document.createElement('div');
        particle.className = 'confetti-particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.backgroundColor = getRandomColor();
        document.body.appendChild(particle);

        // Use anime.js if available, otherwise CSS fallback
        if (typeof anime !== 'undefined') {
            anime({
                targets: particle,
                translateY: [0, window.innerHeight + 50],
                translateX: [0, (Math.random() - 0.5) * 200],
                rotate: Math.random() * 720,
                opacity: [1, 0],
                duration: 2000 + Math.random() * 1000,
                easing: 'easeInQuad',
                complete: () => particle.remove()
            });
        } else {
            particle.style.animation = 'confetti-fall 2s ease-in forwards';
            setTimeout(() => particle.remove(), 2000);
        }
    }

    /**
     * Get random confetti color
     * @returns {string}
     */
    function getRandomColor() {
        const colors = [
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#ffd93d',
            '#6bcf7f', '#a8e6cf', '#ff8b94', '#c7ceea'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    /**
     * Show floating XP animation
     * @param {number} amount - XP amount
     * @param {Element} anchorElement - Element to anchor animation to
     */
    function showFloatingXP(amount, anchorElement = null) {
        if (!config.animationsEnabled) return;

        const xpText = document.createElement('div');
        xpText.className = 'floating-xp';
        xpText.textContent = `+${amount} XP`;

        // Position near submit button or provided element
        const anchor = anchorElement || document.getElementById('submitBtn');
        if (anchor) {
            const rect = anchor.getBoundingClientRect();
            xpText.style.left = rect.left + rect.width / 2 + 'px';
            xpText.style.top = rect.top + 'px';
        } else {
            xpText.style.left = '50%';
            xpText.style.top = '50%';
        }

        document.body.appendChild(xpText);

        if (typeof anime !== 'undefined') {
            anime({
                targets: xpText,
                translateY: -100,
                opacity: [1, 0],
                scale: [1, 1.5],
                duration: 1500,
                easing: 'easeOutQuad',
                complete: () => xpText.remove()
            });
        } else {
            xpText.style.animation = 'float-up-xp 1.5s ease-out forwards';
            setTimeout(() => xpText.remove(), 1500);
        }
    }

    /**
     * Animate level up
     */
    function animateLevelUp() {
        if (!config.animationsEnabled) return;

        const levelElement = document.getElementById('playerLevel');
        if (!levelElement) return;

        if (typeof anime !== 'undefined') {
            anime({
                targets: levelElement,
                scale: [1, 1.3, 1],
                rotate: [0, 360],
                duration: 1000,
                easing: 'easeInOutQuad'
            });
        } else {
            levelElement.classList.add('level-up-animation');
            setTimeout(() => levelElement.classList.remove('level-up-animation'), 1000);
        }
    }

    /**
     * Pulse XP bar animation
     */
    function pulseXPBar() {
        if (!config.animationsEnabled) return;

        const xpBar = document.getElementById('xpBar');
        if (!xpBar) return;

        if (typeof anime !== 'undefined') {
            anime({
                targets: xpBar,
                scaleY: [1, 1.1, 1],
                duration: 300,
                easing: 'easeInOutQuad'
            });
        } else {
            xpBar.classList.add('xp-bar-pulse');
            setTimeout(() => xpBar.classList.remove('xp-bar-pulse'), 300);
        }
    }

    /**
     * Enable or disable animations
     * @param {boolean} enabled
     */
    function setAnimationsEnabled(enabled) {
        config.animationsEnabled = enabled;
        console.log('[UIManager] Animations', enabled ? 'enabled' : 'disabled');
    }

    /**
     * Check if animations are enabled
     * @returns {boolean}
     */
    function isAnimationsEnabled() {
        return config.animationsEnabled;
    }

    /**
     * Load configuration
     * @param {Object} cfg
     */
    function loadConfig(cfg) {
        if (cfg.animationsEnabled !== undefined) {
            config.animationsEnabled = cfg.animationsEnabled;
        }
    }

    /**
     * Set element visibility
     * @param {string} elementId
     * @param {boolean} visible
     */
    function setVisible(elementId, visible) {
        const el = document.getElementById(elementId);
        if (el) {
            el.style.display = visible ? '' : 'none';
        }
    }

    /**
     * Set element enabled/disabled state
     * @param {string} elementId
     * @param {boolean} enabled
     */
    function setEnabled(elementId, enabled) {
        const el = document.getElementById(elementId);
        if (el) {
            el.disabled = !enabled;
        }
    }

    /**
     * Update mission panel content
     * @param {Object} mission - Mission data
     */
    function updateMissionPanel(mission) {
        const titleEl = document.getElementById('missionTitle');
        const descEl = document.getElementById('missionDescription');

        if (titleEl && mission.title) {
            titleEl.textContent = mission.title;
        }
        if (descEl && mission.description) {
            descEl.innerHTML = mission.description;
        }
    }

    /**
     * Clear answer input
     */
    function clearAnswerInput() {
        const input = document.getElementById('answerInput');
        if (input) {
            input.value = '';
        }
    }

    // Public API
    return {
        SCREENS,
        showScreen,
        getCurrentScreen,
        showModal,
        hideModal,
        showScene,
        updatePlayerStats,
        updateXPBar,
        showFeedback,
        hideFeedback,
        showConfetti,
        showFloatingXP,
        animateLevelUp,
        pulseXPBar,
        setAnimationsEnabled,
        isAnimationsEnabled,
        loadConfig,
        setVisible,
        setEnabled,
        updateMissionPanel,
        clearAnswerInput
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIManager;
}
