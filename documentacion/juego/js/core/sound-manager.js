/**
 * Sound Manager - Data Engineer: The Game
 *
 * Handles all audio using Web Audio API.
 * Generates sounds programmatically (no external files needed).
 */

const SoundManager = (function() {
    'use strict';

    // Audio Context (created on first user interaction)
    let audioContext = null;

    // Configuration
    let config = {
        enabled: true,
        volume: 0.5
    };

    // Sound definitions
    const SOUNDS = {
        click: {
            notes: [{ freq: 800, duration: 0.05, volume: 0.3 }]
        },
        correct: {
            // Ascending chord (C5, E5, G5)
            notes: [
                { freq: 523.25, duration: 0.1, volume: 1, delay: 0 },
                { freq: 659.25, duration: 0.1, volume: 1, delay: 0.1 },
                { freq: 783.99, duration: 0.2, volume: 1, delay: 0.2 }
            ]
        },
        incorrect: {
            // Descending beep
            notes: [
                { freq: 400, duration: 0.1, volume: 1, delay: 0 },
                { freq: 300, duration: 0.15, volume: 1, delay: 0.1 }
            ]
        },
        levelup: {
            // Fanfare (5 notes)
            notes: [
                { freq: 523.25, duration: 0.1, volume: 1, delay: 0 },
                { freq: 659.25, duration: 0.1, volume: 1, delay: 0.1 },
                { freq: 783.99, duration: 0.1, volume: 1, delay: 0.2 },
                { freq: 1046.50, duration: 0.1, volume: 1, delay: 0.3 },
                { freq: 1318.51, duration: 0.3, volume: 1, delay: 0.4 }
            ]
        },
        xp: {
            notes: [{ freq: 1200, duration: 0.1, volume: 0.5 }]
        },
        unlock: {
            // Module unlock sound
            notes: [
                { freq: 392.00, duration: 0.15, volume: 1, delay: 0 },    // G4
                { freq: 523.25, duration: 0.15, volume: 1, delay: 0.15 }, // C5
                { freq: 659.25, duration: 0.15, volume: 1, delay: 0.3 },  // E5
                { freq: 783.99, duration: 0.3, volume: 1, delay: 0.45 }   // G5
            ]
        },
        hint: {
            notes: [
                { freq: 600, duration: 0.1, volume: 0.4, delay: 0 },
                { freq: 800, duration: 0.1, volume: 0.4, delay: 0.1 }
            ]
        },
        transition: {
            notes: [{ freq: 500, duration: 0.08, volume: 0.2 }]
        }
    };

    /**
     * Initialize Audio Context (must be called after user interaction)
     * @returns {AudioContext}
     */
    function initAudioContext() {
        if (!audioContext) {
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                console.log('[SoundManager] AudioContext initialized');
            } catch (e) {
                console.error('[SoundManager] Failed to create AudioContext:', e);
            }
        }

        // Resume if suspended (browser autoplay policy)
        if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume();
        }

        return audioContext;
    }

    /**
     * Play a single note
     * @param {number} frequency - Frequency in Hz
     * @param {number} duration - Duration in seconds
     * @param {number} vol - Volume multiplier (0-1)
     * @param {number} delay - Delay before playing in seconds
     */
    function playNote(frequency, duration, vol = 1, delay = 0) {
        const ctx = initAudioContext();
        if (!ctx || !config.enabled) return;

        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';

        const actualVolume = config.volume * vol;
        const startTime = ctx.currentTime + delay;
        const endTime = startTime + duration;

        // Envelope for smooth sound
        gainNode.gain.setValueAtTime(0, startTime);
        gainNode.gain.linearRampToValueAtTime(actualVolume, startTime + 0.01);
        gainNode.gain.linearRampToValueAtTime(actualVolume * 0.7, endTime - 0.05);
        gainNode.gain.linearRampToValueAtTime(0, endTime);

        oscillator.start(startTime);
        oscillator.stop(endTime);
    }

    /**
     * Play a predefined sound
     * @param {string} soundName - Name of the sound to play
     */
    function play(soundName) {
        if (!config.enabled) return;

        const sound = SOUNDS[soundName];
        if (!sound) {
            console.warn('[SoundManager] Unknown sound:', soundName);
            return;
        }

        sound.notes.forEach(note => {
            playNote(note.freq, note.duration, note.volume, note.delay || 0);
        });
    }

    /**
     * Enable or disable sounds
     * @param {boolean} enabled
     */
    function setEnabled(enabled) {
        config.enabled = enabled;
        console.log('[SoundManager] Sounds', enabled ? 'enabled' : 'disabled');
    }

    /**
     * Set volume
     * @param {number} volume - Volume level (0-1)
     */
    function setVolume(volume) {
        config.volume = Math.max(0, Math.min(1, volume));
        console.log('[SoundManager] Volume set to', config.volume);
    }

    /**
     * Get current volume
     * @returns {number}
     */
    function getVolume() {
        return config.volume;
    }

    /**
     * Check if sounds are enabled
     * @returns {boolean}
     */
    function isEnabled() {
        return config.enabled;
    }

    /**
     * Load configuration
     * @param {Object} cfg - Config object with enabled and volume
     */
    function loadConfig(cfg) {
        if (cfg.soundsEnabled !== undefined) {
            config.enabled = cfg.soundsEnabled;
        }
        if (cfg.volume !== undefined) {
            config.volume = cfg.volume;
        }
    }

    /**
     * Play a custom frequency sequence
     * @param {Array} notes - Array of {freq, duration, volume, delay}
     */
    function playSequence(notes) {
        if (!config.enabled) return;

        notes.forEach(note => {
            playNote(note.freq, note.duration, note.volume || 1, note.delay || 0);
        });
    }

    /**
     * Test sound system (useful for settings)
     */
    function test() {
        play('xp');
    }

    // Public API
    return {
        init: initAudioContext,
        play,
        playNote,
        playSequence,
        setEnabled,
        setVolume,
        getVolume,
        isEnabled,
        loadConfig,
        test,
        SOUNDS
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SoundManager;
}
