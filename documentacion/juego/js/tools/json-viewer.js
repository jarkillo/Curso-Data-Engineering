/**
 * JSON Viewer Tool - Data Engineer: The Game
 *
 * Interactive JSON viewer with syntax highlighting,
 * collapsible nodes, and search functionality.
 */

const JSONViewer = (function() {
    'use strict';

    // Current JSON data
    let currentData = null;
    let expandedPaths = new Set();

    /**
     * Initialize the JSON viewer
     * @param {string} containerId - Container element ID
     * @param {Object} options - Viewer options
     */
    function init(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('[JSONViewer] Container not found:', containerId);
            return;
        }

        const defaultOptions = {
            showToolbar: true,
            showLineNumbers: true,
            initialExpanded: 2, // Levels to expand initially
            theme: 'dark'
        };

        const opts = { ...defaultOptions, ...options };

        container.innerHTML = `
            <div class="json-viewer-container" data-theme="${opts.theme}">
                ${opts.showToolbar ? `
                <div class="json-viewer-toolbar">
                    <span class="json-viewer-title">🔍 JSON Viewer</span>
                    <div class="json-viewer-actions">
                        <button class="json-btn small" onclick="JSONViewer.expandAll()" title="Expandir todo">➕</button>
                        <button class="json-btn small" onclick="JSONViewer.collapseAll()" title="Colapsar todo">➖</button>
                        <button class="json-btn small" onclick="JSONViewer.copyToClipboard()" title="Copiar">📋</button>
                        <input type="text" class="json-search" id="jsonSearch" placeholder="Buscar..." oninput="JSONViewer.search(this.value)">
                    </div>
                </div>
                ` : ''}
                <div class="json-viewer-content" id="jsonContent">
                    <div class="json-placeholder">Carga un JSON para visualizar</div>
                </div>
                <div class="json-viewer-footer" id="jsonFooter" style="display: none;">
                    <span id="jsonStats"></span>
                </div>
            </div>
        `;
    }

    /**
     * Load and display JSON data
     * @param {Object|string} data - JSON object or string
     * @param {number} expandLevels - Number of levels to expand initially
     */
    function load(data, expandLevels = 2) {
        try {
            // Parse if string
            if (typeof data === 'string') {
                data = JSON.parse(data);
            }

            currentData = data;
            expandedPaths.clear();

            // Pre-expand initial levels
            preExpandLevels(data, '', expandLevels);

            render();
            updateStats();

        } catch (error) {
            showError(`Error parsing JSON: ${error.message}`);
        }
    }

    /**
     * Pre-expand paths up to a certain level
     * @param {*} data
     * @param {string} path
     * @param {number} levels
     */
    function preExpandLevels(data, path, levels) {
        if (levels <= 0) return;

        if (Array.isArray(data)) {
            expandedPaths.add(path || 'root');
            data.forEach((item, index) => {
                preExpandLevels(item, path ? `${path}[${index}]` : `[${index}]`, levels - 1);
            });
        } else if (data !== null && typeof data === 'object') {
            expandedPaths.add(path || 'root');
            Object.keys(data).forEach(key => {
                preExpandLevels(data[key], path ? `${path}.${key}` : key, levels - 1);
            });
        }
    }

    /**
     * Render the JSON viewer
     */
    function render() {
        const content = document.getElementById('jsonContent');
        if (!content || currentData === null) return;

        content.innerHTML = renderValue(currentData, '', 'root');
    }

    /**
     * Render a JSON value recursively
     * @param {*} value
     * @param {string} path
     * @param {string} key
     * @returns {string} HTML
     */
    function renderValue(value, path, key = null) {
        const currentPath = path || 'root';
        const isExpanded = expandedPaths.has(currentPath);

        if (Array.isArray(value)) {
            return renderArray(value, currentPath, key, isExpanded);
        } else if (value !== null && typeof value === 'object') {
            return renderObject(value, currentPath, key, isExpanded);
        } else {
            return renderPrimitive(value, key);
        }
    }

    /**
     * Render an array
     */
    function renderArray(arr, path, key, isExpanded) {
        const isEmpty = arr.length === 0;
        const toggleIcon = isEmpty ? '' : `<span class="json-toggle" onclick="JSONViewer.toggle('${path}')">${isExpanded ? '▼' : '▶'}</span>`;
        const keyHtml = key !== null ? `<span class="json-key">"${escapeHtml(key)}"</span><span class="json-colon">: </span>` : '';

        let html = `<div class="json-line json-array">`;
        html += toggleIcon;
        html += keyHtml;
        html += `<span class="json-bracket">[</span>`;

        if (isEmpty) {
            html += `<span class="json-bracket">]</span>`;
        } else if (!isExpanded) {
            html += `<span class="json-collapsed" onclick="JSONViewer.toggle('${path}')">${arr.length} items</span>`;
            html += `<span class="json-bracket">]</span>`;
        } else {
            html += `</div><div class="json-children">`;
            arr.forEach((item, index) => {
                const itemPath = `${path}[${index}]`;
                html += `<div class="json-item">`;
                html += `<span class="json-index">${index}: </span>`;
                html += renderValue(item, itemPath, null);
                if (index < arr.length - 1) {
                    html += `<span class="json-comma">,</span>`;
                }
                html += `</div>`;
            });
            html += `</div><div class="json-line"><span class="json-bracket">]</span>`;
        }

        html += `</div>`;
        return html;
    }

    /**
     * Render an object
     */
    function renderObject(obj, path, key, isExpanded) {
        const keys = Object.keys(obj);
        const isEmpty = keys.length === 0;
        const toggleIcon = isEmpty ? '' : `<span class="json-toggle" onclick="JSONViewer.toggle('${path}')">${isExpanded ? '▼' : '▶'}</span>`;
        const keyHtml = key !== null ? `<span class="json-key">"${escapeHtml(key)}"</span><span class="json-colon">: </span>` : '';

        let html = `<div class="json-line json-object">`;
        html += toggleIcon;
        html += keyHtml;
        html += `<span class="json-bracket">{</span>`;

        if (isEmpty) {
            html += `<span class="json-bracket">}</span>`;
        } else if (!isExpanded) {
            html += `<span class="json-collapsed" onclick="JSONViewer.toggle('${path}')">${keys.length} properties</span>`;
            html += `<span class="json-bracket">}</span>`;
        } else {
            html += `</div><div class="json-children">`;
            keys.forEach((k, index) => {
                const itemPath = path ? `${path}.${k}` : k;
                html += `<div class="json-item">`;
                html += renderValue(obj[k], itemPath, k);
                if (index < keys.length - 1) {
                    html += `<span class="json-comma">,</span>`;
                }
                html += `</div>`;
            });
            html += `</div><div class="json-line"><span class="json-bracket">}</span>`;
        }

        html += `</div>`;
        return html;
    }

    /**
     * Render a primitive value
     */
    function renderPrimitive(value, key) {
        const keyHtml = key !== null ? `<span class="json-key">"${escapeHtml(key)}"</span><span class="json-colon">: </span>` : '';

        let valueHtml;
        if (typeof value === 'string') {
            valueHtml = `<span class="json-string">"${escapeHtml(value)}"</span>`;
        } else if (typeof value === 'number') {
            valueHtml = `<span class="json-number">${value}</span>`;
        } else if (typeof value === 'boolean') {
            valueHtml = `<span class="json-boolean">${value}</span>`;
        } else if (value === null) {
            valueHtml = `<span class="json-null">null</span>`;
        } else {
            valueHtml = `<span class="json-unknown">${escapeHtml(String(value))}</span>`;
        }

        return `<span class="json-primitive">${keyHtml}${valueHtml}</span>`;
    }

    /**
     * Toggle expand/collapse of a path
     * @param {string} path
     */
    function toggle(path) {
        if (expandedPaths.has(path)) {
            expandedPaths.delete(path);
        } else {
            expandedPaths.add(path);
        }
        render();
    }

    /**
     * Expand all nodes
     */
    function expandAll() {
        expandAllPaths(currentData, '');
        render();
    }

    /**
     * Recursively expand all paths
     */
    function expandAllPaths(data, path) {
        const currentPath = path || 'root';

        if (Array.isArray(data)) {
            expandedPaths.add(currentPath);
            data.forEach((item, index) => {
                expandAllPaths(item, `${currentPath}[${index}]`);
            });
        } else if (data !== null && typeof data === 'object') {
            expandedPaths.add(currentPath);
            Object.keys(data).forEach(key => {
                expandAllPaths(data[key], currentPath === 'root' ? key : `${currentPath}.${key}`);
            });
        }
    }

    /**
     * Collapse all nodes
     */
    function collapseAll() {
        expandedPaths.clear();
        expandedPaths.add('root'); // Keep root expanded
        render();
    }

    /**
     * Search within JSON
     * @param {string} query
     */
    function search(query) {
        if (!query) {
            render();
            return;
        }

        query = query.toLowerCase();
        const content = document.getElementById('jsonContent');
        if (!content) return;

        // Highlight matching text
        const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT);
        const matches = [];

        while (walker.nextNode()) {
            const node = walker.currentNode;
            if (node.textContent.toLowerCase().includes(query)) {
                matches.push(node);
            }
        }

        // Remove existing highlights (safe: use textNode instead of outerHTML to prevent XSS)
        content.querySelectorAll('.json-highlight').forEach(el => {
            const textNode = document.createTextNode(el.textContent);
            el.parentNode.replaceChild(textNode, el);
        });

        // Add new highlights (escape HTML to prevent XSS)
        matches.forEach(node => {
            const text = node.textContent;
            // Escape HTML entities before creating highlight spans
            const escapedText = text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
            const escapedQuery = escapeRegex(query)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
            const regex = new RegExp(`(${escapedQuery})`, 'gi');
            const newHtml = escapedText.replace(regex, '<span class="json-highlight">$1</span>');

            const span = document.createElement('span');
            span.innerHTML = newHtml;
            node.parentNode.replaceChild(span, node);
        });
    }

    /**
     * Copy JSON to clipboard
     */
    function copyToClipboard() {
        if (!currentData) {
            alert('No hay JSON para copiar');
            return;
        }

        const text = JSON.stringify(currentData, null, 2);

        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('JSON copiado al portapapeles');
            });
        } else {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            showNotification('JSON copiado al portapapeles');
        }
    }

    /**
     * Update statistics
     */
    function updateStats() {
        const footer = document.getElementById('jsonFooter');
        const stats = document.getElementById('jsonStats');
        if (!footer || !stats || !currentData) return;

        const counts = countElements(currentData);
        stats.textContent = `${counts.objects} objetos, ${counts.arrays} arrays, ${counts.primitives} valores`;
        footer.style.display = 'block';
    }

    /**
     * Count JSON elements
     */
    function countElements(data) {
        let objects = 0, arrays = 0, primitives = 0;

        function count(value) {
            if (Array.isArray(value)) {
                arrays++;
                value.forEach(count);
            } else if (value !== null && typeof value === 'object') {
                objects++;
                Object.values(value).forEach(count);
            } else {
                primitives++;
            }
        }

        count(data);
        return { objects, arrays, primitives };
    }

    /**
     * Show error message
     */
    function showError(message) {
        const content = document.getElementById('jsonContent');
        if (content) {
            content.innerHTML = `<div class="json-error">❌ ${escapeHtml(message)}</div>`;
        }
    }

    /**
     * Show notification
     */
    function showNotification(message) {
        // Simple notification - could be enhanced
        const notification = document.createElement('div');
        notification.className = 'json-notification';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }

    /**
     * Get current JSON data
     * @returns {Object}
     */
    function getData() {
        return currentData;
    }

    /**
     * Clear the viewer
     */
    function clear() {
        currentData = null;
        expandedPaths.clear();
        const content = document.getElementById('jsonContent');
        if (content) {
            content.innerHTML = '<div class="json-placeholder">Carga un JSON para visualizar</div>';
        }
        const footer = document.getElementById('jsonFooter');
        if (footer) footer.style.display = 'none';
    }

    /**
     * Escape HTML special characters
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Escape regex special characters
     */
    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Public API
    return {
        init,
        load,
        toggle,
        expandAll,
        collapseAll,
        search,
        copyToClipboard,
        getData,
        clear
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JSONViewer;
}
