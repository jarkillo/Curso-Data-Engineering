/**
 * Story Manager - Data Engineer: The Game
 *
 * Handles module introduction stories with dynamic scene rendering.
 * Supports characters, tutorials, and narrative progression.
 */

const StoryManager = (function() {
    'use strict';

    // Current story state
    let currentStory = null;
    let currentSceneIndex = 0;
    let onCompleteCallback = null;

    /**
     * Show a module's introduction story
     * @param {Object} storyData - Story data from module
     * @param {Function} onComplete - Callback when story finishes
     */
    function showStory(storyData, onComplete) {
        if (!storyData || !storyData.scenes || storyData.scenes.length === 0) {
            // No story, call completion immediately
            if (onComplete) onComplete();
            return;
        }

        currentStory = storyData;
        currentSceneIndex = 0;
        onCompleteCallback = onComplete;

        // Get or create story container
        const container = getStoryContainer();
        if (!container) {
            console.error('[StoryManager] No story container found');
            if (onComplete) onComplete();
            return;
        }

        // Show the story screen
        UIManager.showScreen('dynamicStoryScreen');

        // Render first scene
        renderScene(currentSceneIndex);

        // Play transition sound
        if (typeof SoundManager !== 'undefined') {
            SoundManager.play('transition');
        }
    }

    /**
     * Get or create the dynamic story container
     * @returns {HTMLElement}
     */
    function getStoryContainer() {
        let container = document.getElementById('dynamicStoryScreen');

        if (!container) {
            // Create container if it doesn't exist
            container = document.createElement('div');
            container.id = 'dynamicStoryScreen';
            container.className = 'screen';
            container.style.display = 'none';
            container.innerHTML = `
                <div class="story-container">
                    <div class="story-header">
                        <h2 id="storyTitle"></h2>
                        <span class="story-progress" id="storyProgress"></span>
                    </div>
                    <div class="story-content" id="dynamicStoryContent"></div>
                    <div class="story-actions">
                        <button class="story-btn secondary" id="storyBackBtn" onclick="StoryManager.previousScene()">
                            ← Anterior
                        </button>
                        <button class="story-btn primary" id="storyNextBtn" onclick="StoryManager.nextScene()">
                            Continuar →
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(container);
        }

        return container;
    }

    /**
     * Render a specific scene
     * @param {number} index - Scene index
     */
    function renderScene(index) {
        if (!currentStory || index < 0 || index >= currentStory.scenes.length) {
            return;
        }

        const scene = currentStory.scenes[index];
        const contentEl = document.getElementById('dynamicStoryContent');
        const titleEl = document.getElementById('storyTitle');
        const progressEl = document.getElementById('storyProgress');
        const backBtn = document.getElementById('storyBackBtn');
        const nextBtn = document.getElementById('storyNextBtn');

        if (!contentEl) return;

        // Update title
        if (titleEl) {
            titleEl.textContent = currentStory.title || 'Tu Historia Continúa...';
        }

        // Update progress
        if (progressEl) {
            progressEl.textContent = `${index + 1} / ${currentStory.scenes.length}`;
        }

        // Build scene HTML
        let html = '<div class="story-scene-content animate-fade-in">';

        // Character dialogue
        if (scene.character) {
            html += `
                <div class="story-character">
                    <div class="character-avatar">${scene.character.avatar || '👤'}</div>
                    <div class="character-info">
                        <div class="character-name">${scene.character.name}</div>
                        <div class="character-role">${scene.character.role || ''}</div>
                    </div>
                </div>
            `;
        }

        // Scene content
        html += `<div class="story-text">${scene.content}</div>`;

        // Tutorial box if present
        if (scene.tutorial) {
            html += `
                <div class="story-tutorial">
                    <div class="tutorial-title">📖 ${scene.tutorial.title}</div>
                    <div class="tutorial-content">${scene.tutorial.content}</div>
                </div>
            `;
        }

        html += '</div>';
        contentEl.innerHTML = html;

        // Update navigation buttons
        if (backBtn) {
            backBtn.style.visibility = index > 0 ? 'visible' : 'hidden';
        }

        if (nextBtn) {
            const isLast = index === currentStory.scenes.length - 1;
            nextBtn.textContent = isLast ? '¡Comenzar! 🚀' : 'Continuar →';
        }

        // Play sound
        if (typeof SoundManager !== 'undefined') {
            SoundManager.play('click');
        }
    }

    /**
     * Go to next scene or complete story
     */
    function nextScene() {
        if (!currentStory) return;

        if (currentSceneIndex < currentStory.scenes.length - 1) {
            currentSceneIndex++;
            renderScene(currentSceneIndex);
        } else {
            // Story complete
            completeStory();
        }
    }

    /**
     * Go to previous scene
     */
    function previousScene() {
        if (!currentStory || currentSceneIndex <= 0) return;

        currentSceneIndex--;
        renderScene(currentSceneIndex);
    }

    /**
     * Complete the current story
     */
    function completeStory() {
        const callback = onCompleteCallback;

        // Reset state
        currentStory = null;
        currentSceneIndex = 0;
        onCompleteCallback = null;

        // Play completion sound
        if (typeof SoundManager !== 'undefined') {
            SoundManager.play('correct');
        }

        // Execute callback
        if (callback) {
            callback();
        }
    }

    /**
     * Skip the current story
     */
    function skipStory() {
        completeStory();
    }

    /**
     * Check if a story is currently playing
     * @returns {boolean}
     */
    function isPlaying() {
        return currentStory !== null;
    }

    /**
     * Get current scene index
     * @returns {number}
     */
    function getCurrentSceneIndex() {
        return currentSceneIndex;
    }

    /**
     * Get total scenes in current story
     * @returns {number}
     */
    function getTotalScenes() {
        return currentStory ? currentStory.scenes.length : 0;
    }

    // Public API
    return {
        showStory,
        nextScene,
        previousScene,
        skipStory,
        isPlaying,
        getCurrentSceneIndex,
        getTotalScenes
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StoryManager;
}
