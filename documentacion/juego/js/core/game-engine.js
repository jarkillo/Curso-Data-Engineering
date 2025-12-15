/**
 * Game Engine - Data Engineer: The Game
 *
 * Main state machine that orchestrates all game systems.
 * Handles game flow, state transitions, and coordinates
 * between storage, UI, sound, and module systems.
 */

const GameEngine = (function() {
    'use strict';

    // Game state
    let state = null;
    let config = null;

    // Current context
    let currentMission = null;
    let currentModule = null;
    let currentScene = 1;

    // Calculator state (preserved for backwards compatibility)
    let calcState = {
        display: '0',
        firstOperand: null,
        operator: null,
        waitingForSecondOperand: false
    };

    // Game states enum
    const GAME_STATES = {
        MENU: 'menu',
        STORY: 'story',
        PLAYING: 'playing',
        MODULE_SELECT: 'module_select',
        PAUSED: 'paused'
    };

    let currentGameState = GAME_STATES.MENU;

    /**
     * Initialize the game engine
     */
    function init() {
        console.log('[GameEngine] Initializing...');

        // Load configuration
        config = StorageManager.loadConfig();

        // Apply config to subsystems
        SoundManager.loadConfig(config);
        UIManager.loadConfig(config);

        // Check for existing save
        if (StorageManager.hasSave()) {
            UIManager.setVisible('loadBtn', true);
        } else {
            UIManager.setVisible('loadBtn', false);
        }

        // Setup global event listeners
        setupEventListeners();

        console.log('[GameEngine] Initialization complete');
    }

    /**
     * Setup global event listeners
     */
    function setupEventListeners() {
        // Keyboard navigation
        document.addEventListener('keydown', handleKeyDown);

        // Volume slider (if exists)
        const volumeSlider = document.getElementById('volumeSlider');
        if (volumeSlider) {
            volumeSlider.addEventListener('input', function() {
                const value = parseInt(this.value) / 100;
                SoundManager.setVolume(value);
                const volumeValue = document.getElementById('volumeValue');
                if (volumeValue) {
                    volumeValue.textContent = this.value + '%';
                }
            });

            volumeSlider.addEventListener('change', function() {
                SoundManager.test();
            });
        }

        // Close modals with Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const configModal = document.getElementById('configModal');
                if (configModal && configModal.style.display === 'flex') {
                    closeConfigModal();
                }
            }
        });
    }

    /**
     * Handle keyboard events
     * @param {KeyboardEvent} event
     */
    function handleKeyDown(event) {
        // Don't interfere with inputs
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }

        // Story navigation with Enter
        if (event.key === 'Enter' && currentGameState === GAME_STATES.STORY) {
            event.preventDefault();
            advanceStory();
        }

        // Calculator keyboard support
        if (currentGameState === GAME_STATES.PLAYING) {
            const calcTab = document.getElementById('calculatorTab');
            if (calcTab && calcTab.classList.contains('active')) {
                handleCalculatorKey(event);
            }
        }
    }

    /**
     * Start a new game
     */
    function newGame() {
        SoundManager.play('click');
        UIManager.showModal('nameModal');
    }

    /**
     * Start story after name input
     */
    function startStory() {
        const nameInput = document.getElementById('playerNameInput');
        const name = nameInput ? nameInput.value.trim() : '';

        if (!name) {
            alert('Por favor ingresa tu nombre');
            return;
        }

        // Initialize new state
        state = { ...StorageManager.DEFAULT_GAME_STATE };
        state.playerName = name;

        // Update UI
        UIManager.hideModal('nameModal');
        UIManager.showScreen(UIManager.SCREENS.STORY);
        UIManager.updatePlayerStats({ name: name });

        // Set game state
        currentGameState = GAME_STATES.STORY;
        currentScene = 1;
        UIManager.showScene(1);

        SoundManager.play('transition');
    }

    /**
     * Load existing game
     */
    function loadGame() {
        SoundManager.play('click');

        // Load state
        state = StorageManager.loadGameState();

        if (!state.playerName) {
            // No valid save, start new game
            newGame();
            return;
        }

        // Update UI
        UIManager.updatePlayerStats({
            name: state.playerName,
            level: state.level
        });
        updateXPDisplay();

        // Determine where to continue
        if (state.missionsCompleted.length === 0) {
            // New player, show story
            currentGameState = GAME_STATES.STORY;
            UIManager.showScreen(UIManager.SCREENS.STORY);
            UIManager.showScene(1);
        } else {
            // Returning player, go to game/module select
            startMission();
        }
    }

    /**
     * Advance story to next scene
     */
    function advanceStory() {
        const sceneMapping = {
            1: 2, 2: 3, 3: 4,
            // Scene 4 starts mission
            5: 6,
            // Scene 6 starts mission 2A
            7: null, // Starts mission 2B
            8: 9,
            // Scene 9 starts mission 3A
        };

        const nextScene = sceneMapping[currentScene];

        if (nextScene === undefined) {
            // Special handling for mission start scenes
            if (currentScene === 4) {
                startMission();
            }
        } else if (nextScene !== null) {
            nextScene(nextScene);
        }
    }

    /**
     * Navigate to a specific story scene
     * @param {number} sceneNum
     */
    function goToScene(sceneNum) {
        currentScene = sceneNum;
        UIManager.showScene(sceneNum);
        SoundManager.play('transition');
    }

    /**
     * Start the game mission screen
     */
    function startMission() {
        // Hide other screens, show game
        UIManager.showScreen(UIManager.SCREENS.GAME);
        currentGameState = GAME_STATES.PLAYING;

        // Update stats display
        UIManager.updatePlayerStats({
            name: state.playerName,
            level: state.level
        });
        updateXPDisplay();

        // Load first uncompleted mission or last available
        loadCurrentMission();

        // Save game
        saveGame();

        SoundManager.play('transition');
    }

    /**
     * Load the current mission content
     */
    function loadCurrentMission() {
        // Determine which mission to load
        // Default to mission 1_1 if nothing completed
        const missionToLoad = state.currentMission || findNextMission() || 'mission_1_1';

        const mission = ModuleRegistry.getMission(missionToLoad);
        if (mission && mission.setup) {
            currentMission = mission;
            mission.setup(state);
        } else {
            // Fallback to legacy mission loading
            console.log('[GameEngine] Using legacy mission system for:', missionToLoad);
            loadLegacyMission(missionToLoad);
        }
    }

    /**
     * Find next uncompleted mission
     * @returns {string|null}
     */
    function findNextMission() {
        // Get all missions from all loaded modules
        const allModules = ModuleRegistry.getAllModules();

        for (const module of allModules) {
            if (!ModuleRegistry.isModuleUnlocked(module.id, state)) continue;

            const missions = ModuleRegistry.getModuleMissions(module.id);
            for (const mission of missions) {
                if (!state.missionsCompleted.includes(mission.id)) {
                    return mission.id;
                }
            }
        }

        return null;
    }

    /**
     * Load legacy mission (backwards compatibility)
     * @param {string} missionId
     */
    function loadLegacyMission(missionId) {
        state.currentMission = missionId;
        state.currentMissionType = missionId;

        // Trigger legacy mission loading if Module1 provides it
        if (typeof window.loadLegacyMissionData === 'function') {
            window.loadLegacyMissionData(missionId, state);
        }
    }

    /**
     * Start a specific mission by ID
     * @param {string} missionId
     */
    function startMissionById(missionId) {
        const mission = ModuleRegistry.getMission(missionId);

        if (mission) {
            state.currentMission = missionId;
            currentMission = mission;

            // Show game screen
            UIManager.showScreen(UIManager.SCREENS.GAME);
            currentGameState = GAME_STATES.PLAYING;

            // Update display
            UIManager.updatePlayerStats({
                name: state.playerName,
                level: state.level
            });
            updateXPDisplay();

            // Load mission content
            loadMissionContent(mission);

            SoundManager.play('transition');
        } else {
            console.error('[GameEngine] Mission not found:', missionId);
        }
    }

    /**
     * Load mission content into the UI
     * @param {Object} mission
     */
    function loadMissionContent(mission) {
        // Update title and description
        const titleEl = document.getElementById('missionTitle');
        const descEl = document.getElementById('missionDescription');

        if (titleEl) titleEl.textContent = mission.title;
        if (descEl) descEl.innerHTML = mission.description;

        // Load data visualization
        if (mission.data) {
            loadDataVisualization(mission);
        }

        // Clear previous answer
        UIManager.clearAnswerInput();
        UIManager.hideFeedback();
    }

    /**
     * Load data visualization for mission
     * @param {Object} mission
     */
    function loadDataVisualization(mission) {
        const dataItems = document.getElementById('dataItems');
        const barChart = document.getElementById('barChart');

        if (!mission.data) return;

        // Determine data type and render accordingly
        if (mission.data.ventas && Array.isArray(mission.data.ventas)) {
            if (typeof mission.data.ventas[0] === 'number') {
                // Numeric data (missions 1, 2A, 2B)
                renderNumericData(mission.data);
            } else {
                // Object data (missions 3A, 3B)
                renderCategoryData(mission.data);
            }
        }

        // Update helper panel
        updateHelperPanel(mission.data);
    }

    /**
     * Render numeric data visualization
     * @param {Object} data
     */
    function renderNumericData(data) {
        const dataItems = document.getElementById('dataItems');
        const barChart = document.getElementById('barChart');
        const dias = data.dias || data.ventas.map((_, i) => `Item ${i + 1}`);
        const values = data.ventas;

        // Data items
        if (dataItems) {
            dataItems.innerHTML = values.map((val, i) => `
                <div class="data-item">
                    <div class="item-label">${dias[i]}</div>
                    <div class="item-value">${val.toFixed ? val.toFixed(2) : val}€</div>
                </div>
            `).join('');
        }

        // Bar chart
        if (barChart) {
            const maxValue = Math.max(...values);
            const outliers = detectOutliers(values);

            barChart.innerHTML = values.map((val, i) => {
                const heightPercent = (val / maxValue) * 100;
                const isOutlier = outliers.includes(i);
                return `
                    <div class="bar-item">
                        <div class="bar" style="height: ${heightPercent}%; ${isOutlier ? 'background: linear-gradient(180deg, #ff4757 0%, #ff6b81 100%);' : ''}"></div>
                        <div class="bar-label">${dias[i]}</div>
                        <div class="bar-value">${val.toFixed ? val.toFixed(2) : val}€</div>
                    </div>
                `;
            }).join('');
        }
    }

    /**
     * Render category data visualization
     * @param {Object} data
     */
    function renderCategoryData(data) {
        const dataItems = document.getElementById('dataItems');
        const barChart = document.getElementById('barChart');
        const items = data.ventas;

        if (dataItems) {
            dataItems.innerHTML = items.map(item => {
                const label = item.producto || item.tienda || 'Item';
                const value = item.talla || item.talla_mas_vendida || '';
                const count = item.cantidad || item.unidades || '';
                return `
                    <div class="data-item">
                        <div class="item-label">${label}</div>
                        <div class="item-value">${value} (${count})</div>
                    </div>
                `;
            }).join('');
        }

        // For category data, show frequency chart
        if (barChart) {
            const frequencies = {};
            items.forEach(item => {
                const key = item.talla || item.talla_mas_vendida;
                frequencies[key] = (frequencies[key] || 0) + 1;
            });

            const maxFreq = Math.max(...Object.values(frequencies));
            barChart.innerHTML = Object.entries(frequencies).map(([key, freq]) => {
                const heightPercent = (freq / maxFreq) * 100;
                return `
                    <div class="bar-item">
                        <div class="bar" style="height: ${heightPercent}%;"></div>
                        <div class="bar-label">${key}</div>
                        <div class="bar-value">${freq}x</div>
                    </div>
                `;
            }).join('');
        }
    }

    /**
     * Detect outliers using IQR method
     * @param {Array} values
     * @returns {Array} indices of outliers
     */
    function detectOutliers(values) {
        const sorted = [...values].sort((a, b) => a - b);
        const n = sorted.length;
        const q1 = sorted[Math.floor(n * 0.25)];
        const q3 = sorted[Math.floor(n * 0.75)];
        const iqr = q3 - q1;
        const lower = q1 - 1.5 * iqr;
        const upper = q3 + 1.5 * iqr;

        return values.map((val, i) => (val < lower || val > upper) ? i : null).filter(i => i !== null);
    }

    /**
     * Update helper panel with mission data
     * @param {Object} data
     */
    function updateHelperPanel(data) {
        if (!data.ventas) return;

        const values = Array.isArray(data.ventas) && typeof data.ventas[0] === 'number'
            ? data.ventas
            : null;

        if (values) {
            const sum = values.reduce((a, b) => a + b, 0);
            const min = Math.min(...values);
            const max = Math.max(...values);

            const helperCount = document.getElementById('helperCount');
            const helperSum = document.getElementById('helperSum');
            const helperMin = document.getElementById('helperMin');
            const helperMax = document.getElementById('helperMax');
            const formulaSum = document.getElementById('formulaSum');
            const formulaCount = document.getElementById('formulaCount');

            if (helperCount) helperCount.textContent = values.length;
            if (helperSum) helperSum.textContent = sum.toFixed(2) + '€';
            if (helperMin) helperMin.textContent = min.toFixed(2) + '€';
            if (helperMax) helperMax.textContent = max.toFixed(2) + '€';
            if (formulaSum) formulaSum.textContent = sum.toFixed(2);
            if (formulaCount) formulaCount.textContent = values.length;
        }
    }

    /**
     * Check player's answer for current mission
     */
    function checkAnswer() {
        const answerInput = document.getElementById('answerInput');
        if (!answerInput) return;

        const answer = answerInput.value.trim();

        if (!answer) {
            UIManager.showFeedback('⚠️ Por favor ingresa una respuesta', 'error');
            return;
        }

        if (!currentMission) {
            console.error('[GameEngine] No current mission');
            return;
        }

        // Determine answer type
        let userAnswer;
        if (currentMission.type === 'numeric') {
            userAnswer = parseFloat(answer.replace(',', '.'));
            if (isNaN(userAnswer)) {
                UIManager.showFeedback('⚠️ Por favor ingresa un número válido', 'error');
                return;
            }
        } else {
            userAnswer = answer;
        }

        // Validate answer
        const isCorrect = currentMission.validate
            ? currentMission.validate(userAnswer, currentMission.data)
            : false;

        if (isCorrect) {
            handleCorrectAnswer();
        } else {
            handleIncorrectAnswer();
        }
    }

    /**
     * Handle correct answer
     */
    function handleCorrectAnswer() {
        const xpReward = currentMission.xp || 100;

        // Complete mission
        completeMission(currentMission.id, xpReward);

        // Show feedback
        let correctAnswer = '';
        if (currentMission.getCorrectAnswer) {
            const answer = currentMission.getCorrectAnswer(currentMission.data);
            correctAnswer = typeof answer === 'number' ? answer.toFixed(2) : answer;
        }

        UIManager.showFeedback(`
            ✅ <strong>¡CORRECTO!</strong><br><br>
            ${correctAnswer ? `Respuesta: ${correctAnswer}` : ''}<br><br>
            <strong>+${xpReward} XP</strong><br><br>
            <button class="submit-btn" onclick="GameEngine.nextMission()" style="margin-top: 10px;">
                ➡️ Siguiente Misión
            </button>
        `, 'success');

        // Disable submit button
        UIManager.setEnabled('submitBtn', false);
    }

    /**
     * Handle incorrect answer
     */
    function handleIncorrectAnswer() {
        SoundManager.play('incorrect');

        UIManager.showFeedback(`
            ❌ <strong>Incorrecto</strong><br><br>
            Revisa tu cálculo e inténtalo de nuevo.<br>
            Usa las herramientas de ayuda si lo necesitas.
        `, 'error');
    }

    /**
     * Save current game state
     */
    function saveGame() {
        if (state) {
            StorageManager.saveGameState(state);
        }
    }

    /**
     * Add XP to player
     * @param {number} amount
     */
    function addXP(amount) {
        state.xp += amount;
        state.totalXP += amount;

        // Check for level up
        const xpForNextLevel = state.level * 100;

        if (state.xp >= xpForNextLevel) {
            state.xp -= xpForNextLevel;
            state.level++;

            // Level up effects
            SoundManager.play('levelup');
            UIManager.animateLevelUp();

            // Update display
            UIManager.updatePlayerStats({ level: state.level });
        } else {
            SoundManager.play('xp');
        }

        // Update XP bar
        UIManager.pulseXPBar();
        updateXPDisplay();

        // Save
        saveGame();
    }

    /**
     * Update XP display
     */
    function updateXPDisplay() {
        const xpForNextLevel = state.level * 100;
        UIManager.updateXPBar(state.xp, xpForNextLevel);
    }

    /**
     * Complete a mission
     * @param {string} missionId
     * @param {number} xpReward
     */
    function completeMission(missionId, xpReward) {
        if (!state.missionsCompleted.includes(missionId)) {
            state.missionsCompleted.push(missionId);
        }

        // Add XP
        addXP(xpReward);

        // Visual effects
        UIManager.showConfetti();
        UIManager.showFloatingXP(xpReward);

        // Sound
        SoundManager.play('correct');

        // Save
        saveGame();
    }

    /**
     * Go to next mission
     */
    function nextMission() {
        // Clear feedback
        UIManager.hideFeedback();
        UIManager.clearAnswerInput();
        UIManager.setEnabled('submitBtn', true);

        // Find next mission
        const nextMissionId = findNextMission();

        if (nextMissionId) {
            state.currentMission = nextMissionId;
            loadCurrentMission();
        } else {
            // All missions complete
            showCompletionScreen();
        }
    }

    /**
     * Show game completion screen
     */
    function showCompletionScreen() {
        UIManager.showFeedback(`
            🎉 <strong>¡FELICIDADES!</strong><br><br>
            Has completado todas las misiones disponibles.<br>
            Total XP: ${state.totalXP}<br>
            Nivel alcanzado: ${state.level}<br><br>
            <em>Más misiones próximamente...</em>
        `, 'success');
    }

    /**
     * Show credits
     */
    function showCredits() {
        SoundManager.play('click');
        alert('🎮 DATA ENGINEER: THE GAME\n\nCreado para aprender Data Engineering\n\nVersión: 2.0 Modular\n2025');
    }

    // ==========================================
    // CALCULATOR FUNCTIONS
    // ==========================================

    function updateCalcDisplay() {
        const display = document.getElementById('calcDisplay');
        if (display) {
            display.textContent = calcState.display;
        }
    }

    function appendCalc(digit) {
        if (calcState.waitingForSecondOperand) {
            calcState.display = digit;
            calcState.waitingForSecondOperand = false;
        } else {
            calcState.display = calcState.display === '0' ? digit : calcState.display + digit;
        }
        updateCalcDisplay();
    }

    function inputDecimal() {
        if (calcState.waitingForSecondOperand) {
            calcState.display = '0.';
            calcState.waitingForSecondOperand = false;
            updateCalcDisplay();
            return;
        }

        if (!calcState.display.includes('.')) {
            calcState.display += '.';
        }
        updateCalcDisplay();
    }

    function inputOperator(nextOperator) {
        const inputValue = parseFloat(calcState.display);

        if (calcState.operator && calcState.waitingForSecondOperand) {
            calcState.operator = nextOperator;
            return;
        }

        if (calcState.firstOperand === null) {
            calcState.firstOperand = inputValue;
        } else if (calcState.operator) {
            const result = calculate(calcState.firstOperand, inputValue, calcState.operator);
            calcState.display = String(result);
            calcState.firstOperand = result;
        }

        calcState.waitingForSecondOperand = true;
        calcState.operator = nextOperator;
        updateCalcDisplay();
    }

    function calculate(first, second, operator) {
        switch (operator) {
            case '+': return first + second;
            case '-': return first - second;
            case '*': return first * second;
            case '/': return first / second;
            default: return second;
        }
    }

    function calculateCalc() {
        const inputValue = parseFloat(calcState.display);

        if (calcState.operator && calcState.firstOperand !== null) {
            const result = calculate(calcState.firstOperand, inputValue, calcState.operator);
            calcState.display = String(result);
            calcState.firstOperand = null;
            calcState.operator = null;
            calcState.waitingForSecondOperand = false;
            updateCalcDisplay();
        }
    }

    function clearCalc() {
        calcState.display = '0';
        calcState.firstOperand = null;
        calcState.operator = null;
        calcState.waitingForSecondOperand = false;
        updateCalcDisplay();
    }

    function copyToAnswer() {
        const result = parseFloat(calcState.display);
        const answerInput = document.getElementById('answerInput');
        if (answerInput) {
            answerInput.value = result.toFixed(2);
        }
    }

    function handleCalculatorKey(event) {
        const key = event.key;

        if (key >= '0' && key <= '9') {
            event.preventDefault();
            appendCalc(key);
        } else if (['+', '-', '*', '/'].includes(key)) {
            event.preventDefault();
            inputOperator(key);
        } else if (key === '.' || key === ',') {
            event.preventDefault();
            inputDecimal();
        } else if (key === 'Enter' || key === '=') {
            event.preventDefault();
            calculateCalc();
        } else if (key === 'Escape' || key === 'Delete') {
            event.preventDefault();
            clearCalc();
        } else if (key === 'Backspace') {
            event.preventDefault();
            if (calcState.display.length > 1) {
                calcState.display = calcState.display.slice(0, -1);
            } else {
                calcState.display = '0';
            }
            updateCalcDisplay();
        }
    }

    // ==========================================
    // CONFIG FUNCTIONS
    // ==========================================

    function openConfigModal() {
        SoundManager.play('click');

        const modal = document.getElementById('configModal');
        if (modal) {
            modal.style.display = 'flex';

            // Load current values
            const soundToggle = document.getElementById('soundToggle');
            const volumeSlider = document.getElementById('volumeSlider');
            const volumeValue = document.getElementById('volumeValue');
            const animationsToggle = document.getElementById('animationsToggle');

            if (soundToggle) soundToggle.checked = SoundManager.isEnabled();
            if (volumeSlider) volumeSlider.value = Math.round(SoundManager.getVolume() * 100);
            if (volumeValue) volumeValue.textContent = Math.round(SoundManager.getVolume() * 100) + '%';
            if (animationsToggle) animationsToggle.checked = UIManager.isAnimationsEnabled();
        }
    }

    function closeConfigModal() {
        SoundManager.play('click');
        UIManager.hideModal('configModal');
    }

    function toggleSounds() {
        const soundToggle = document.getElementById('soundToggle');
        const enabled = soundToggle ? soundToggle.checked : true;
        SoundManager.setEnabled(enabled);
        saveConfig();
        if (enabled) {
            SoundManager.test();
        }
    }

    function toggleAnimations() {
        const animationsToggle = document.getElementById('animationsToggle');
        const enabled = animationsToggle ? animationsToggle.checked : true;
        UIManager.setAnimationsEnabled(enabled);
        saveConfig();
    }

    function setVolume(value) {
        const volume = parseInt(value) / 100;
        SoundManager.setVolume(volume);
        const volumeValue = document.getElementById('volumeValue');
        if (volumeValue) {
            volumeValue.textContent = value + '%';
        }
        saveConfig();
    }

    function saveConfig() {
        const newConfig = {
            soundsEnabled: SoundManager.isEnabled(),
            volume: SoundManager.getVolume(),
            animationsEnabled: UIManager.isAnimationsEnabled()
        };
        StorageManager.saveConfig(newConfig);
    }

    function confirmReset() {
        UIManager.showModal('resetModal');
    }

    function resetProgress() {
        StorageManager.clearAllData();
        UIManager.hideModal('resetModal');
        UIManager.hideModal('configModal');
        UIManager.showScreen(UIManager.SCREENS.START);
        currentGameState = GAME_STATES.MENU;
        state = null;
        window.location.reload();
    }

    function backToStart() {
        UIManager.showScreen(UIManager.SCREENS.START);
        currentGameState = GAME_STATES.MENU;
    }

    // ==========================================
    // TOOL FUNCTIONS
    // ==========================================

    function switchTool(tool) {
        const tabs = document.querySelectorAll('.tool-tab');
        const contents = document.querySelectorAll('.tool-content');

        tabs.forEach(tab => tab.classList.remove('active'));
        contents.forEach(content => content.classList.remove('active'));

        if (tool === 'calculator') {
            if (tabs[0]) tabs[0].classList.add('active');
            const calcTab = document.getElementById('calculatorTab');
            if (calcTab) calcTab.classList.add('active');
        } else {
            if (tabs[1]) tabs[1].classList.add('active');
            const helperTab = document.getElementById('helperTab');
            if (helperTab) helperTab.classList.add('active');
        }
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    // Expose state getter
    function getState() {
        return state;
    }

    function setState(newState) {
        state = newState;
    }

    return {
        // Initialization
        init,

        // Game flow
        newGame,
        startStory,
        loadGame,
        startMission,
        startMissionById,
        nextMission,
        showCredits,
        backToStart,

        // Story navigation
        goToScene,
        advanceStory,

        // Missions
        checkAnswer,
        loadMissionContent,

        // Progress
        addXP,
        completeMission,
        saveGame,

        // State access
        getState,
        setState,

        // Calculator
        appendCalc,
        inputDecimal,
        inputOperator,
        calculateCalc,
        clearCalc,
        copyToAnswer,

        // Config
        openConfigModal,
        closeConfigModal,
        toggleSounds,
        toggleAnimations,
        setVolume,
        confirmReset,
        resetProgress,

        // Tools
        switchTool,

        // Constants
        GAME_STATES
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GameEngine;
}
