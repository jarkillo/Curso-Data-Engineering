/**
 * SQL Editor Tool - Data Engineer: The Game
 *
 * Interactive SQL editor with syntax highlighting and
 * query execution using sql.js (SQLite in browser).
 */

const SQLEditor = (function() {
    'use strict';

    // SQL.js database instance
    let db = null;
    let isLoaded = false;
    let loadPromise = null;

    // Editor state
    let currentQuery = '';
    let queryHistory = [];
    let historyIndex = -1;

    // SQL keywords for highlighting
    const SQL_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'LIKE',
        'ORDER', 'BY', 'ASC', 'DESC', 'LIMIT', 'OFFSET',
        'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER', 'ON',
        'GROUP', 'HAVING', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX',
        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
        'CREATE', 'TABLE', 'DROP', 'ALTER', 'INDEX',
        'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'UNIQUE',
        'NULL', 'NOT NULL', 'DEFAULT', 'AS', 'DISTINCT',
        'UNION', 'ALL', 'EXCEPT', 'INTERSECT',
        'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
        'BETWEEN', 'EXISTS', 'IS'
    ];

    /**
     * Load sql.js library dynamically
     * @returns {Promise}
     */
    function loadSqlJs() {
        if (isLoaded) {
            return Promise.resolve();
        }

        if (loadPromise) {
            return loadPromise;
        }

        loadPromise = new Promise((resolve, reject) => {
            // Check if already loaded
            if (typeof initSqlJs !== 'undefined') {
                initSqlJs({
                    locateFile: file => `https://sql.js.org/dist/${file}`
                }).then(SQL => {
                    db = new SQL.Database();
                    isLoaded = true;
                    console.log('[SQLEditor] sql.js loaded successfully');
                    resolve();
                }).catch(reject);
                return;
            }

            // Load script
            const script = document.createElement('script');
            script.src = 'https://sql.js.org/dist/sql-wasm.js';
            script.onload = () => {
                initSqlJs({
                    locateFile: file => `https://sql.js.org/dist/${file}`
                }).then(SQL => {
                    db = new SQL.Database();
                    isLoaded = true;
                    console.log('[SQLEditor] sql.js loaded successfully');
                    resolve();
                }).catch(reject);
            };
            script.onerror = () => reject(new Error('Failed to load sql.js'));
            document.head.appendChild(script);
        });

        return loadPromise;
    }

    /**
     * Initialize the SQL editor UI
     * @param {string} containerId - Container element ID
     * @param {Object} options - Editor options
     */
    function init(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('[SQLEditor] Container not found:', containerId);
            return;
        }

        const defaultOptions = {
            placeholder: 'SELECT * FROM tabla;',
            height: '150px',
            showHistory: true,
            showHelp: true
        };

        const opts = { ...defaultOptions, ...options };

        container.innerHTML = `
            <div class="sql-editor-container">
                <div class="sql-editor-header">
                    <span class="sql-editor-title">🗃️ Editor SQL</span>
                    <div class="sql-editor-actions">
                        ${opts.showHistory ? '<button class="sql-btn small" onclick="SQLEditor.showHistory()" title="Historial">📜</button>' : ''}
                        ${opts.showHelp ? '<button class="sql-btn small" onclick="SQLEditor.showHelp()" title="Ayuda">❓</button>' : ''}
                        <button class="sql-btn small" onclick="SQLEditor.clearEditor()" title="Limpiar">🗑️</button>
                    </div>
                </div>
                <div class="sql-editor-wrapper">
                    <div class="sql-line-numbers" id="sqlLineNumbers">1</div>
                    <textarea
                        id="sqlInput"
                        class="sql-input"
                        placeholder="${opts.placeholder}"
                        style="height: ${opts.height}"
                        spellcheck="false"
                    ></textarea>
                </div>
                <div class="sql-editor-toolbar">
                    <button class="sql-btn primary" onclick="SQLEditor.executeQuery()">
                        ▶️ Ejecutar (Ctrl+Enter)
                    </button>
                    <span class="sql-status" id="sqlStatus">Listo</span>
                </div>
                <div class="sql-results-container" id="sqlResults" style="display: none;">
                    <div class="sql-results-header">
                        <span>📊 Resultados</span>
                        <span class="sql-results-count" id="sqlResultsCount"></span>
                    </div>
                    <div class="sql-results-table" id="sqlResultsTable"></div>
                </div>
                <div class="sql-error-container" id="sqlError" style="display: none;"></div>
            </div>
        `;

        // Setup event listeners
        const input = document.getElementById('sqlInput');
        if (input) {
            input.addEventListener('input', handleInput);
            input.addEventListener('keydown', handleKeyDown);
            input.addEventListener('scroll', syncScroll);
        }

        // Load sql.js in background
        loadSqlJs().catch(err => {
            console.error('[SQLEditor] Failed to load sql.js:', err);
            setStatus('Error cargando SQL engine', 'error');
        });
    }

    /**
     * Handle input changes
     * @param {Event} e
     */
    function handleInput(e) {
        currentQuery = e.target.value;
        updateLineNumbers();
    }

    /**
     * Handle keyboard shortcuts
     * @param {KeyboardEvent} e
     */
    function handleKeyDown(e) {
        // Ctrl+Enter to execute
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            executeQuery();
            return;
        }

        // Tab for indentation
        if (e.key === 'Tab') {
            e.preventDefault();
            const input = e.target;
            const start = input.selectionStart;
            const end = input.selectionEnd;
            input.value = input.value.substring(0, start) + '    ' + input.value.substring(end);
            input.selectionStart = input.selectionEnd = start + 4;
            handleInput({ target: input });
        }

        // Up/Down for history
        if (e.ctrlKey && e.key === 'ArrowUp') {
            e.preventDefault();
            navigateHistory(-1);
        }
        if (e.ctrlKey && e.key === 'ArrowDown') {
            e.preventDefault();
            navigateHistory(1);
        }
    }

    /**
     * Sync scroll between textarea and line numbers
     */
    function syncScroll() {
        const input = document.getElementById('sqlInput');
        const lineNumbers = document.getElementById('sqlLineNumbers');
        if (input && lineNumbers) {
            lineNumbers.scrollTop = input.scrollTop;
        }
    }

    /**
     * Update line numbers
     */
    function updateLineNumbers() {
        const input = document.getElementById('sqlInput');
        const lineNumbers = document.getElementById('sqlLineNumbers');
        if (!input || !lineNumbers) return;

        const lines = input.value.split('\n').length;
        lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('<br>');
    }

    /**
     * Execute the current SQL query
     * @param {string} query - Optional query override
     * @returns {Object} Query result
     */
    function executeQuery(query = null) {
        const sql = query || document.getElementById('sqlInput')?.value?.trim();

        if (!sql) {
            setStatus('Escribe una consulta SQL', 'warning');
            return null;
        }

        if (!isLoaded || !db) {
            setStatus('SQL engine no cargado', 'error');
            return null;
        }

        setStatus('Ejecutando...', 'loading');
        hideResults();
        hideError();

        try {
            const results = db.exec(sql);

            // Add to history
            if (!queryHistory.includes(sql)) {
                queryHistory.unshift(sql);
                if (queryHistory.length > 50) {
                    queryHistory.pop();
                }
                historyIndex = -1;
            }

            if (results.length === 0) {
                // Query executed but no results (INSERT, UPDATE, etc.)
                const changes = db.getRowsModified();
                setStatus(`Ejecutado correctamente. ${changes} filas afectadas.`, 'success');
                showResults([], []);
                return { success: true, changes };
            }

            const result = results[0];
            const columns = result.columns;
            const rows = result.values;

            setStatus(`${rows.length} resultado(s) en ${columns.length} columna(s)`, 'success');
            showResults(columns, rows);

            return { success: true, columns, rows };

        } catch (error) {
            setStatus('Error en la consulta', 'error');
            showError(error.message);
            return { success: false, error: error.message };
        }
    }

    /**
     * Show query results
     * @param {Array} columns - Column names
     * @param {Array} rows - Row data
     */
    function showResults(columns, rows) {
        const container = document.getElementById('sqlResults');
        const table = document.getElementById('sqlResultsTable');
        const count = document.getElementById('sqlResultsCount');

        if (!container || !table) return;

        if (columns.length === 0) {
            table.innerHTML = '<div class="sql-no-results">Consulta ejecutada sin resultados</div>';
            container.style.display = 'block';
            return;
        }

        let html = '<table class="sql-table">';

        // Header
        html += '<thead><tr>';
        columns.forEach(col => {
            html += `<th>${escapeHtml(col)}</th>`;
        });
        html += '</tr></thead>';

        // Body
        html += '<tbody>';
        rows.forEach(row => {
            html += '<tr>';
            row.forEach(cell => {
                const value = cell === null ? '<span class="sql-null">NULL</span>' : escapeHtml(String(cell));
                html += `<td>${value}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table>';

        table.innerHTML = html;
        if (count) count.textContent = `(${rows.length} filas)`;
        container.style.display = 'block';
    }

    /**
     * Hide results container
     */
    function hideResults() {
        const container = document.getElementById('sqlResults');
        if (container) container.style.display = 'none';
    }

    /**
     * Show error message
     * @param {string} message
     */
    function showError(message) {
        const container = document.getElementById('sqlError');
        if (container) {
            container.innerHTML = `<span class="sql-error-icon">❌</span> ${escapeHtml(message)}`;
            container.style.display = 'block';
        }
    }

    /**
     * Hide error container
     */
    function hideError() {
        const container = document.getElementById('sqlError');
        if (container) container.style.display = 'none';
    }

    /**
     * Set status message
     * @param {string} message
     * @param {string} type - 'success', 'error', 'warning', 'loading'
     */
    function setStatus(message, type = 'info') {
        const status = document.getElementById('sqlStatus');
        if (status) {
            status.textContent = message;
            status.className = `sql-status sql-status-${type}`;
        }
    }

    /**
     * Clear the editor
     */
    function clearEditor() {
        const input = document.getElementById('sqlInput');
        if (input) {
            input.value = '';
            currentQuery = '';
            updateLineNumbers();
        }
        hideResults();
        hideError();
        setStatus('Listo');
    }

    /**
     * Navigate query history
     * @param {number} direction - -1 for older, 1 for newer
     */
    function navigateHistory(direction) {
        if (queryHistory.length === 0) return;

        historyIndex += direction;
        historyIndex = Math.max(-1, Math.min(historyIndex, queryHistory.length - 1));

        const input = document.getElementById('sqlInput');
        if (input) {
            if (historyIndex === -1) {
                input.value = currentQuery;
            } else {
                input.value = queryHistory[historyIndex];
            }
            updateLineNumbers();
        }
    }

    /**
     * Show query history modal
     */
    function showHistory() {
        if (queryHistory.length === 0) {
            alert('No hay historial de consultas');
            return;
        }

        const historyHtml = queryHistory
            .map((q, i) => `<div class="history-item" onclick="SQLEditor.loadFromHistory(${i})">${escapeHtml(q.substring(0, 100))}${q.length > 100 ? '...' : ''}</div>`)
            .join('');

        // Simple alert for now, can be replaced with modal
        console.log('Query history:', queryHistory);
        alert('Historial (ver consola):\n' + queryHistory.slice(0, 5).join('\n---\n'));
    }

    /**
     * Load query from history
     * @param {number} index
     */
    function loadFromHistory(index) {
        if (queryHistory[index]) {
            const input = document.getElementById('sqlInput');
            if (input) {
                input.value = queryHistory[index];
                updateLineNumbers();
            }
        }
    }

    /**
     * Show SQL help
     */
    function showHelp() {
        alert(`SQL Editor - Ayuda

Atajos de teclado:
• Ctrl+Enter: Ejecutar consulta
• Ctrl+↑/↓: Navegar historial
• Tab: Insertar espacios

Comandos SQL soportados:
• SELECT, INSERT, UPDATE, DELETE
• CREATE TABLE, DROP TABLE
• JOIN, GROUP BY, ORDER BY
• Funciones: COUNT, SUM, AVG, MIN, MAX

Ejemplo:
SELECT * FROM usuarios WHERE edad > 18;`);
    }

    /**
     * Create a table in the database
     * @param {string} tableName
     * @param {Array} columns - Array of column definitions
     * @param {Array} data - Optional initial data
     */
    function createTable(tableName, columns, data = []) {
        if (!isLoaded || !db) {
            console.error('[SQLEditor] Database not loaded');
            return false;
        }

        try {
            // Drop existing table
            db.run(`DROP TABLE IF EXISTS ${tableName}`);

            // Create table
            const columnDefs = columns.map(col => {
                if (typeof col === 'string') {
                    return `${col} TEXT`;
                }
                return `${col.name} ${col.type || 'TEXT'}${col.primary ? ' PRIMARY KEY' : ''}`;
            }).join(', ');

            db.run(`CREATE TABLE ${tableName} (${columnDefs})`);

            // Insert data
            if (data.length > 0) {
                const colNames = columns.map(c => typeof c === 'string' ? c : c.name);
                const placeholders = colNames.map(() => '?').join(', ');
                const stmt = db.prepare(`INSERT INTO ${tableName} (${colNames.join(', ')}) VALUES (${placeholders})`);

                data.forEach(row => {
                    const values = Array.isArray(row) ? row : colNames.map(c => row[c]);
                    stmt.run(values);
                });

                stmt.free();
            }

            console.log(`[SQLEditor] Table ${tableName} created with ${data.length} rows`);
            return true;

        } catch (error) {
            console.error('[SQLEditor] Error creating table:', error);
            return false;
        }
    }

    /**
     * Get the current query text
     * @returns {string}
     */
    function getQuery() {
        return document.getElementById('sqlInput')?.value || '';
    }

    /**
     * Set the query text
     * @param {string} query
     */
    function setQuery(query) {
        const input = document.getElementById('sqlInput');
        if (input) {
            input.value = query;
            updateLineNumbers();
        }
    }

    /**
     * Check if database is ready
     * @returns {boolean}
     */
    function isReady() {
        return isLoaded && db !== null;
    }

    /**
     * Escape HTML special characters
     * @param {string} text
     * @returns {string}
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Public API
    return {
        init,
        loadSqlJs,
        executeQuery,
        createTable,
        clearEditor,
        showHistory,
        loadFromHistory,
        showHelp,
        getQuery,
        setQuery,
        isReady,
        navigateHistory
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SQLEditor;
}
