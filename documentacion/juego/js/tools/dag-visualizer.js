/**
 * DAG Visualizer Tool - Data Engineer: The Game
 *
 * Interactive DAG (Directed Acyclic Graph) visualizer
 * for Apache Airflow pipelines and data workflows.
 */

const DAGVisualizer = (function() {
    'use strict';

    // Current DAG data
    let currentDAG = null;
    let canvas = null;
    let ctx = null;

    // Layout configuration
    const CONFIG = {
        nodeWidth: 140,
        nodeHeight: 50,
        nodeRadius: 8,
        horizontalGap: 80,
        verticalGap: 60,
        padding: 40,
        arrowSize: 8,
        colors: {
            node: {
                default: '#3498db',
                success: '#27ae60',
                failed: '#e74c3c',
                running: '#f39c12',
                pending: '#95a5a6'
            },
            text: '#ffffff',
            border: 'rgba(255, 255, 255, 0.3)',
            arrow: '#7f8c8d',
            background: 'transparent'
        },
        fonts: {
            node: 'bold 12px Arial',
            operator: '10px Arial'
        }
    };

    // Node positions cache
    let nodePositions = new Map();
    let selectedNode = null;

    /**
     * Initialize the DAG visualizer
     * @param {string} containerId - Container element ID
     * @param {Object} options - Visualizer options
     */
    function init(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('[DAGVisualizer] Container not found:', containerId);
            return;
        }

        const opts = { ...CONFIG, ...options };

        container.innerHTML = `
            <div class="dag-visualizer-container">
                <div class="dag-toolbar">
                    <span class="dag-title">🔄 DAG Visualizer</span>
                    <div class="dag-actions">
                        <button class="dag-btn small" onclick="DAGVisualizer.zoomIn()" title="Zoom In">🔍+</button>
                        <button class="dag-btn small" onclick="DAGVisualizer.zoomOut()" title="Zoom Out">🔍-</button>
                        <button class="dag-btn small" onclick="DAGVisualizer.resetView()" title="Reset">↺</button>
                    </div>
                </div>
                <div class="dag-canvas-wrapper" id="dagCanvasWrapper">
                    <canvas id="dagCanvas"></canvas>
                </div>
                <div class="dag-legend">
                    <div class="dag-legend-item">
                        <span class="dag-legend-color" style="background: ${opts.colors.node.success}"></span>
                        <span>Completado</span>
                    </div>
                    <div class="dag-legend-item">
                        <span class="dag-legend-color" style="background: ${opts.colors.node.running}"></span>
                        <span>Ejecutando</span>
                    </div>
                    <div class="dag-legend-item">
                        <span class="dag-legend-color" style="background: ${opts.colors.node.failed}"></span>
                        <span>Fallido</span>
                    </div>
                    <div class="dag-legend-item">
                        <span class="dag-legend-color" style="background: ${opts.colors.node.pending}"></span>
                        <span>Pendiente</span>
                    </div>
                </div>
                <div class="dag-node-info" id="dagNodeInfo" style="display: none;"></div>
            </div>
        `;

        // Setup canvas
        canvas = document.getElementById('dagCanvas');
        ctx = canvas.getContext('2d');

        // Setup event listeners
        setupEventListeners();

        // Initial resize
        resizeCanvas();
    }

    /**
     * Setup event listeners
     */
    function setupEventListeners() {
        // Resize handler
        window.addEventListener('resize', resizeCanvas);

        // Click handler for nodes
        if (canvas) {
            canvas.addEventListener('click', handleCanvasClick);
            canvas.addEventListener('mousemove', handleCanvasHover);
        }
    }

    /**
     * Resize canvas to fit container
     */
    function resizeCanvas() {
        if (!canvas) return;

        const wrapper = document.getElementById('dagCanvasWrapper');
        if (!wrapper) return;

        canvas.width = wrapper.clientWidth;
        canvas.height = wrapper.clientHeight || 300;

        if (currentDAG) {
            render();
        }
    }

    /**
     * Load and display a DAG
     * @param {Object} dag - DAG definition
     */
    function load(dag) {
        currentDAG = dag;
        nodePositions.clear();
        selectedNode = null;

        // Calculate layout
        calculateLayout();

        // Render
        render();
    }

    /**
     * Calculate node positions using topological sort
     */
    function calculateLayout() {
        if (!currentDAG || !currentDAG.tasks) return;

        const tasks = currentDAG.tasks;
        const levels = new Map();
        const visited = new Set();

        // Find root nodes (no dependencies)
        const roots = tasks.filter(task =>
            !task.dependencies || task.dependencies.length === 0
        );

        // BFS to assign levels
        let queue = roots.map(t => ({ task: t, level: 0 }));

        while (queue.length > 0) {
            const { task, level } = queue.shift();

            if (visited.has(task.id)) continue;
            visited.add(task.id);

            // Update level (take max if multiple paths)
            const currentLevel = levels.get(task.id) || 0;
            levels.set(task.id, Math.max(currentLevel, level));

            // Find dependents
            const dependents = tasks.filter(t =>
                t.dependencies && t.dependencies.includes(task.id)
            );

            dependents.forEach(dep => {
                queue.push({ task: dep, level: level + 1 });
            });
        }

        // Group tasks by level
        const levelGroups = new Map();
        levels.forEach((level, taskId) => {
            if (!levelGroups.has(level)) {
                levelGroups.set(level, []);
            }
            levelGroups.get(level).push(taskId);
        });

        // Calculate positions
        const maxLevel = Math.max(...levelGroups.keys());
        const canvasWidth = canvas?.width || 800;
        const canvasHeight = canvas?.height || 400;

        levelGroups.forEach((taskIds, level) => {
            const x = CONFIG.padding + level * (CONFIG.nodeWidth + CONFIG.horizontalGap);
            const totalHeight = taskIds.length * (CONFIG.nodeHeight + CONFIG.verticalGap) - CONFIG.verticalGap;
            const startY = (canvasHeight - totalHeight) / 2;

            taskIds.forEach((taskId, index) => {
                const y = startY + index * (CONFIG.nodeHeight + CONFIG.verticalGap);
                nodePositions.set(taskId, { x, y });
            });
        });
    }

    /**
     * Render the DAG
     */
    function render() {
        if (!ctx || !canvas || !currentDAG) return;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw edges first (behind nodes)
        drawEdges();

        // Draw nodes
        drawNodes();
    }

    /**
     * Draw all edges (dependencies)
     */
    function drawEdges() {
        if (!currentDAG.tasks) return;

        ctx.strokeStyle = CONFIG.colors.arrow;
        ctx.lineWidth = 2;

        currentDAG.tasks.forEach(task => {
            if (!task.dependencies) return;

            const toPos = nodePositions.get(task.id);
            if (!toPos) return;

            task.dependencies.forEach(depId => {
                const fromPos = nodePositions.get(depId);
                if (!fromPos) return;

                drawArrow(
                    fromPos.x + CONFIG.nodeWidth,
                    fromPos.y + CONFIG.nodeHeight / 2,
                    toPos.x,
                    toPos.y + CONFIG.nodeHeight / 2
                );
            });
        });
    }

    /**
     * Draw an arrow between two points
     */
    function drawArrow(fromX, fromY, toX, toY) {
        const headLength = CONFIG.arrowSize;
        const dx = toX - fromX;
        const dy = toY - fromY;
        const angle = Math.atan2(dy, dx);

        // Draw line
        ctx.beginPath();
        ctx.moveTo(fromX, fromY);
        ctx.lineTo(toX - headLength * Math.cos(angle), toY - headLength * Math.sin(angle));
        ctx.stroke();

        // Draw arrowhead
        ctx.beginPath();
        ctx.moveTo(toX, toY);
        ctx.lineTo(
            toX - headLength * Math.cos(angle - Math.PI / 6),
            toY - headLength * Math.sin(angle - Math.PI / 6)
        );
        ctx.lineTo(
            toX - headLength * Math.cos(angle + Math.PI / 6),
            toY - headLength * Math.sin(angle + Math.PI / 6)
        );
        ctx.closePath();
        ctx.fillStyle = CONFIG.colors.arrow;
        ctx.fill();
    }

    /**
     * Draw all nodes
     */
    function drawNodes() {
        if (!currentDAG.tasks) return;

        currentDAG.tasks.forEach(task => {
            const pos = nodePositions.get(task.id);
            if (!pos) return;

            drawNode(task, pos.x, pos.y);
        });
    }

    /**
     * Draw a single node
     */
    function drawNode(task, x, y) {
        const isSelected = selectedNode === task.id;
        const status = task.status || 'default';
        const color = CONFIG.colors.node[status] || CONFIG.colors.node.default;

        // Draw shadow
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 2;

        // Draw node background
        ctx.fillStyle = color;
        ctx.beginPath();
        roundRect(ctx, x, y, CONFIG.nodeWidth, CONFIG.nodeHeight, CONFIG.nodeRadius);
        ctx.fill();

        // Remove shadow for border and text
        ctx.shadowColor = 'transparent';

        // Draw border
        if (isSelected) {
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
        } else {
            ctx.strokeStyle = CONFIG.colors.border;
            ctx.lineWidth = 1;
        }
        ctx.beginPath();
        roundRect(ctx, x, y, CONFIG.nodeWidth, CONFIG.nodeHeight, CONFIG.nodeRadius);
        ctx.stroke();

        // Draw task name
        ctx.fillStyle = CONFIG.colors.text;
        ctx.font = CONFIG.fonts.node;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const taskName = task.name || task.id;
        const truncatedName = taskName.length > 15 ? taskName.substring(0, 12) + '...' : taskName;
        ctx.fillText(truncatedName, x + CONFIG.nodeWidth / 2, y + CONFIG.nodeHeight / 2 - 8);

        // Draw operator type
        if (task.operator) {
            ctx.font = CONFIG.fonts.operator;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
            ctx.fillText(task.operator, x + CONFIG.nodeWidth / 2, y + CONFIG.nodeHeight / 2 + 10);
        }

        // Draw status icon
        const statusIcon = getStatusIcon(status);
        if (statusIcon) {
            ctx.font = '14px Arial';
            ctx.fillText(statusIcon, x + CONFIG.nodeWidth - 15, y + 15);
        }
    }

    /**
     * Draw rounded rectangle
     */
    function roundRect(ctx, x, y, width, height, radius) {
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        ctx.lineTo(x + radius, y + height);
        ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        ctx.lineTo(x, y + radius);
        ctx.quadraticCurveTo(x, y, x + radius, y);
    }

    /**
     * Get status icon
     */
    function getStatusIcon(status) {
        const icons = {
            success: '✓',
            failed: '✗',
            running: '⟳',
            pending: '○'
        };
        return icons[status] || '';
    }

    /**
     * Handle canvas click
     */
    function handleCanvasClick(e) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const clickedNode = findNodeAtPosition(x, y);

        if (clickedNode) {
            selectedNode = clickedNode.id;
            showNodeInfo(clickedNode);
        } else {
            selectedNode = null;
            hideNodeInfo();
        }

        render();
    }

    /**
     * Handle canvas hover
     */
    function handleCanvasHover(e) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const hoveredNode = findNodeAtPosition(x, y);
        canvas.style.cursor = hoveredNode ? 'pointer' : 'default';
    }

    /**
     * Find node at canvas position
     */
    function findNodeAtPosition(x, y) {
        if (!currentDAG || !currentDAG.tasks) return null;

        for (const task of currentDAG.tasks) {
            const pos = nodePositions.get(task.id);
            if (!pos) continue;

            if (x >= pos.x && x <= pos.x + CONFIG.nodeWidth &&
                y >= pos.y && y <= pos.y + CONFIG.nodeHeight) {
                return task;
            }
        }

        return null;
    }

    /**
     * Show node information panel
     */
    function showNodeInfo(task) {
        const info = document.getElementById('dagNodeInfo');
        if (!info) return;

        info.innerHTML = `
            <div class="dag-info-header">
                <strong>${task.name || task.id}</strong>
                <span class="dag-info-status dag-status-${task.status || 'default'}">${task.status || 'default'}</span>
            </div>
            <div class="dag-info-content">
                <div class="dag-info-row">
                    <span class="dag-info-label">ID:</span>
                    <span>${task.id}</span>
                </div>
                ${task.operator ? `
                <div class="dag-info-row">
                    <span class="dag-info-label">Operador:</span>
                    <span>${task.operator}</span>
                </div>
                ` : ''}
                ${task.dependencies && task.dependencies.length > 0 ? `
                <div class="dag-info-row">
                    <span class="dag-info-label">Dependencias:</span>
                    <span>${task.dependencies.join(', ')}</span>
                </div>
                ` : ''}
                ${task.description ? `
                <div class="dag-info-row">
                    <span class="dag-info-label">Descripción:</span>
                    <span>${task.description}</span>
                </div>
                ` : ''}
            </div>
        `;
        info.style.display = 'block';
    }

    /**
     * Hide node information panel
     */
    function hideNodeInfo() {
        const info = document.getElementById('dagNodeInfo');
        if (info) info.style.display = 'none';
    }

    /**
     * Update task status
     * @param {string} taskId
     * @param {string} status
     */
    function updateTaskStatus(taskId, status) {
        if (!currentDAG || !currentDAG.tasks) return;

        const task = currentDAG.tasks.find(t => t.id === taskId);
        if (task) {
            task.status = status;
            render();
        }
    }

    /**
     * Get current DAG
     * @returns {Object}
     */
    function getDAG() {
        return currentDAG;
    }

    /**
     * Zoom controls
     */
    let zoomLevel = 1;

    function zoomIn() {
        zoomLevel = Math.min(zoomLevel + 0.1, 2);
        applyZoom();
    }

    function zoomOut() {
        zoomLevel = Math.max(zoomLevel - 0.1, 0.5);
        applyZoom();
    }

    function resetView() {
        zoomLevel = 1;
        applyZoom();
    }

    function applyZoom() {
        if (canvas) {
            canvas.style.transform = `scale(${zoomLevel})`;
            canvas.style.transformOrigin = 'center center';
        }
    }

    /**
     * Clear the visualizer
     */
    function clear() {
        currentDAG = null;
        nodePositions.clear();
        selectedNode = null;
        if (ctx && canvas) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        hideNodeInfo();
    }

    // Public API
    return {
        init,
        load,
        updateTaskStatus,
        getDAG,
        clear,
        zoomIn,
        zoomOut,
        resetView
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DAGVisualizer;
}
