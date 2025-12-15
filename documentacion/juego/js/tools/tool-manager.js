/**
 * Tool Manager - Data Engineer: The Game
 *
 * Manages loading, initialization, and switching between
 * different tools used in game missions.
 */

const ToolManager = (function() {
    'use strict';

    // Registered tools
    const tools = new Map();

    // Tool configurations
    const TOOL_CONFIG = {
        calculator: {
            name: 'Calculadora',
            icon: '🧮',
            script: null, // Built-in
            global: 'Calculator',
            modules: [1] // Used in Module 1
        },
        sqlEditor: {
            name: 'Editor SQL',
            icon: '🗃️',
            script: 'js/tools/sql-editor.js',
            global: 'SQLEditor',
            modules: [2, 5] // SQL and Databases modules
        },
        jsonViewer: {
            name: 'Visor JSON',
            icon: '🔍',
            script: 'js/tools/json-viewer.js',
            global: 'JSONViewer',
            modules: [4] // APIs module
        },
        dagVisualizer: {
            name: 'Visualizador DAG',
            icon: '🔄',
            script: 'js/tools/dag-visualizer.js',
            global: 'DAGVisualizer',
            modules: [6] // Airflow module
        },
        codeEditor: {
            name: 'Editor de Código',
            icon: '📝',
            script: 'js/tools/code-editor.js',
            global: 'CodeEditor',
            modules: [3, 7, 8, 9, 10] // ETL, Cloud, DWH, Spark, ML
        }
    };

    // Active tool
    let activeTool = null;
    let activeContainer = null;

    /**
     * Initialize the tool manager
     */
    function init() {
        console.log('[ToolManager] Initializing...');

        // Register built-in tools
        Object.entries(TOOL_CONFIG).forEach(([id, config]) => {
            if (!config.script) {
                // Built-in tool, register immediately
                tools.set(id, {
                    ...config,
                    loaded: true
                });
            } else {
                tools.set(id, {
                    ...config,
                    loaded: false
                });
            }
        });

        console.log('[ToolManager] Initialized with', tools.size, 'tools');
    }

    /**
     * Load a tool script dynamically
     * @param {string} toolId
     * @returns {Promise}
     */
    function loadTool(toolId) {
        return new Promise((resolve, reject) => {
            const tool = tools.get(toolId);

            if (!tool) {
                reject(new Error(`Tool not found: ${toolId}`));
                return;
            }

            if (tool.loaded) {
                resolve(tool);
                return;
            }

            if (!tool.script) {
                tool.loaded = true;
                resolve(tool);
                return;
            }

            // Check if global already exists
            if (window[tool.global]) {
                tool.loaded = true;
                resolve(tool);
                return;
            }

            // Load script
            const script = document.createElement('script');
            script.src = tool.script;
            script.onload = () => {
                tool.loaded = true;
                console.log(`[ToolManager] Tool loaded: ${toolId}`);
                resolve(tool);
            };
            script.onerror = () => {
                reject(new Error(`Failed to load tool: ${toolId}`));
            };
            document.head.appendChild(script);
        });
    }

    /**
     * Get tools for a specific module
     * @param {number} moduleId
     * @returns {Array} Array of tool IDs
     */
    function getToolsForModule(moduleId) {
        const moduleTools = [];

        tools.forEach((tool, id) => {
            if (tool.modules.includes(moduleId)) {
                moduleTools.push(id);
            }
        });

        return moduleTools;
    }

    /**
     * Initialize a tool in a container
     * @param {string} toolId
     * @param {string} containerId
     * @param {Object} options
     * @returns {Promise}
     */
    async function initTool(toolId, containerId, options = {}) {
        try {
            await loadTool(toolId);

            const tool = tools.get(toolId);
            if (!tool) {
                throw new Error(`Tool not found: ${toolId}`);
            }

            const toolInstance = window[tool.global];
            if (!toolInstance) {
                throw new Error(`Tool global not found: ${tool.global}`);
            }

            if (typeof toolInstance.init === 'function') {
                toolInstance.init(containerId, options);
            }

            activeTool = toolId;
            activeContainer = containerId;

            console.log(`[ToolManager] Tool initialized: ${toolId} in ${containerId}`);
            return toolInstance;

        } catch (error) {
            console.error('[ToolManager] Error initializing tool:', error);
            throw error;
        }
    }

    /**
     * Create a tool panel with tabs for multiple tools
     * @param {string} containerId
     * @param {Array} toolIds - Array of tool IDs to show
     * @param {Object} options
     */
    async function createToolPanel(containerId, toolIds, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('[ToolManager] Container not found:', containerId);
            return;
        }

        // Load all required tools
        await Promise.all(toolIds.map(id => loadTool(id)));

        // Create tabs HTML
        let tabsHtml = '<div class="tool-tabs">';
        toolIds.forEach((id, index) => {
            const tool = tools.get(id);
            if (tool) {
                tabsHtml += `
                    <button class="tool-tab ${index === 0 ? 'active' : ''}"
                            data-tool="${id}"
                            onclick="ToolManager.switchTool('${containerId}', '${id}')">
                        ${tool.icon} ${tool.name}
                    </button>
                `;
            }
        });
        tabsHtml += '</div>';

        // Create content containers
        let contentHtml = '<div class="tool-contents">';
        toolIds.forEach((id, index) => {
            contentHtml += `
                <div class="tool-content ${index === 0 ? 'active' : ''}"
                     id="${containerId}_${id}"
                     data-tool="${id}">
                </div>
            `;
        });
        contentHtml += '</div>';

        container.innerHTML = tabsHtml + contentHtml;

        // Initialize first tool
        if (toolIds.length > 0) {
            await initTool(toolIds[0], `${containerId}_${toolIds[0]}`, options[toolIds[0]] || {});
        }
    }

    /**
     * Switch to a different tool in a panel
     * @param {string} panelId
     * @param {string} toolId
     */
    async function switchTool(panelId, toolId) {
        const panel = document.getElementById(panelId);
        if (!panel) return;

        // Update tabs
        panel.querySelectorAll('.tool-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tool === toolId);
        });

        // Update content
        panel.querySelectorAll('.tool-content').forEach(content => {
            content.classList.toggle('active', content.dataset.tool === toolId);
        });

        // Initialize tool if not already
        const contentId = `${panelId}_${toolId}`;
        const content = document.getElementById(contentId);
        if (content && content.innerHTML.trim() === '') {
            await initTool(toolId, contentId);
        }

        activeTool = toolId;

        // Play sound
        if (typeof SoundManager !== 'undefined') {
            SoundManager.play('click');
        }
    }

    /**
     * Get tool instance by ID
     * @param {string} toolId
     * @returns {Object|null}
     */
    function getTool(toolId) {
        const tool = tools.get(toolId);
        if (tool && tool.loaded) {
            return window[tool.global] || null;
        }
        return null;
    }

    /**
     * Get all registered tools
     * @returns {Map}
     */
    function getAllTools() {
        return tools;
    }

    /**
     * Get active tool ID
     * @returns {string|null}
     */
    function getActiveTool() {
        return activeTool;
    }

    /**
     * Check if a tool is loaded
     * @param {string} toolId
     * @returns {boolean}
     */
    function isToolLoaded(toolId) {
        const tool = tools.get(toolId);
        return tool ? tool.loaded : false;
    }

    // Public API
    return {
        init,
        loadTool,
        getToolsForModule,
        initTool,
        createToolPanel,
        switchTool,
        getTool,
        getAllTools,
        getActiveTool,
        isToolLoaded,
        TOOL_CONFIG
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ToolManager;
}
