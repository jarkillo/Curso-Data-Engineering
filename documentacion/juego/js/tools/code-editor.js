/**
 * Code Editor Tool - Data Engineer: The Game
 *
 * Simple code editor with syntax highlighting for
 * Python, SQL, and other languages used in data engineering.
 */

const CodeEditor = (function() {
    'use strict';

    // Editor instances
    const editors = new Map();

    // Syntax highlighting patterns
    const SYNTAX = {
        python: {
            keywords: /\b(def|class|if|elif|else|for|while|try|except|finally|with|as|import|from|return|yield|raise|pass|break|continue|and|or|not|in|is|None|True|False|lambda|global|nonlocal|assert|async|await)\b/g,
            strings: /(["'])(?:(?=(\\?))\2.)*?\1/g,
            comments: /#.*/g,
            numbers: /\b\d+\.?\d*\b/g,
            functions: /\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()/g,
            decorators: /@[a-zA-Z_][a-zA-Z0-9_]*/g
        },
        sql: {
            keywords: /\b(SELECT|FROM|WHERE|AND|OR|NOT|IN|LIKE|ORDER|BY|ASC|DESC|LIMIT|JOIN|INNER|LEFT|RIGHT|OUTER|ON|GROUP|HAVING|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|DROP|ALTER|INDEX|PRIMARY|KEY|FOREIGN|REFERENCES|UNIQUE|NULL|DEFAULT|AS|DISTINCT|UNION|ALL|CASE|WHEN|THEN|ELSE|END|COUNT|SUM|AVG|MIN|MAX|BETWEEN|EXISTS|IS)\b/gi,
            strings: /(["'])(?:(?=(\\?))\2.)*?\1/g,
            comments: /--.*|\/\*[\s\S]*?\*\//g,
            numbers: /\b\d+\.?\d*\b/g
        },
        javascript: {
            keywords: /\b(const|let|var|function|class|if|else|for|while|do|switch|case|default|break|continue|return|throw|try|catch|finally|new|typeof|instanceof|in|of|async|await|import|export|from|extends|static|get|set|this|super|null|undefined|true|false)\b/g,
            strings: /(["'`])(?:(?=(\\?))\2.)*?\1/g,
            comments: /\/\/.*|\/\*[\s\S]*?\*\//g,
            numbers: /\b\d+\.?\d*\b/g,
            functions: /\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?=\()/g
        },
        yaml: {
            keys: /^[a-zA-Z_][a-zA-Z0-9_]*(?=:)/gm,
            strings: /(["'])(?:(?=(\\?))\2.)*?\1/g,
            comments: /#.*/g,
            numbers: /\b\d+\.?\d*\b/g,
            booleans: /\b(true|false|yes|no|on|off)\b/gi
        }
    };

    /**
     * Initialize a code editor
     * @param {string} containerId - Container element ID
     * @param {Object} options - Editor options
     * @returns {string} Editor ID
     */
    function init(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('[CodeEditor] Container not found:', containerId);
            return null;
        }

        const editorId = options.id || `editor_${Date.now()}`;
        const defaultOptions = {
            language: 'python',
            theme: 'dark',
            lineNumbers: true,
            height: '200px',
            placeholder: '# Escribe tu código aquí...',
            readOnly: false
        };

        const opts = { ...defaultOptions, ...options };

        container.innerHTML = `
            <div class="code-editor-container" data-theme="${opts.theme}" id="${editorId}_container">
                <div class="code-editor-header">
                    <span class="code-editor-title">📝 Editor de Código</span>
                    <div class="code-editor-actions">
                        <select class="code-lang-select" id="${editorId}_lang" onchange="CodeEditor.setLanguage('${editorId}', this.value)">
                            <option value="python" ${opts.language === 'python' ? 'selected' : ''}>Python</option>
                            <option value="sql" ${opts.language === 'sql' ? 'selected' : ''}>SQL</option>
                            <option value="javascript" ${opts.language === 'javascript' ? 'selected' : ''}>JavaScript</option>
                            <option value="yaml" ${opts.language === 'yaml' ? 'selected' : ''}>YAML</option>
                        </select>
                        <button class="code-btn small" onclick="CodeEditor.copy('${editorId}')" title="Copiar">📋</button>
                        <button class="code-btn small" onclick="CodeEditor.clear('${editorId}')" title="Limpiar">🗑️</button>
                    </div>
                </div>
                <div class="code-editor-wrapper">
                    ${opts.lineNumbers ? `<div class="code-line-numbers" id="${editorId}_lines">1</div>` : ''}
                    <div class="code-editor-scroll">
                        <pre class="code-highlight" id="${editorId}_highlight"></pre>
                        <textarea
                            id="${editorId}_input"
                            class="code-input"
                            placeholder="${opts.placeholder}"
                            style="height: ${opts.height}"
                            spellcheck="false"
                            ${opts.readOnly ? 'readonly' : ''}
                        ></textarea>
                    </div>
                </div>
            </div>
        `;

        // Store editor instance
        editors.set(editorId, {
            containerId,
            options: opts,
            language: opts.language
        });

        // Setup event listeners
        const input = document.getElementById(`${editorId}_input`);
        if (input) {
            input.addEventListener('input', () => handleInput(editorId));
            input.addEventListener('scroll', () => syncScroll(editorId));
            input.addEventListener('keydown', (e) => handleKeyDown(e, editorId));
        }

        return editorId;
    }

    /**
     * Handle input changes
     */
    function handleInput(editorId) {
        updateLineNumbers(editorId);
        updateHighlight(editorId);
    }

    /**
     * Handle keyboard shortcuts
     */
    function handleKeyDown(e, editorId) {
        const input = e.target;

        // Tab for indentation
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = input.selectionStart;
            const end = input.selectionEnd;
            const spaces = '    ';

            if (e.shiftKey) {
                // Unindent
                const lineStart = input.value.lastIndexOf('\n', start - 1) + 1;
                const lineContent = input.value.substring(lineStart, start);
                if (lineContent.startsWith(spaces)) {
                    input.value = input.value.substring(0, lineStart) +
                        input.value.substring(lineStart + spaces.length);
                    input.selectionStart = input.selectionEnd = start - spaces.length;
                }
            } else {
                // Indent
                input.value = input.value.substring(0, start) + spaces + input.value.substring(end);
                input.selectionStart = input.selectionEnd = start + spaces.length;
            }
            handleInput(editorId);
        }

        // Auto-close brackets
        const pairs = { '(': ')', '[': ']', '{': '}', '"': '"', "'": "'" };
        if (pairs[e.key]) {
            e.preventDefault();
            const start = input.selectionStart;
            const end = input.selectionEnd;
            const selected = input.value.substring(start, end);
            input.value = input.value.substring(0, start) + e.key + selected + pairs[e.key] + input.value.substring(end);
            input.selectionStart = input.selectionEnd = start + 1;
            handleInput(editorId);
        }

        // Enter with auto-indent
        if (e.key === 'Enter') {
            const start = input.selectionStart;
            const lineStart = input.value.lastIndexOf('\n', start - 1) + 1;
            const line = input.value.substring(lineStart, start);
            const indent = line.match(/^\s*/)[0];

            // Check if line ends with colon (Python) or opening brace
            const prevChar = input.value[start - 1];
            const extraIndent = (prevChar === ':' || prevChar === '{') ? '    ' : '';

            e.preventDefault();
            input.value = input.value.substring(0, start) + '\n' + indent + extraIndent + input.value.substring(start);
            input.selectionStart = input.selectionEnd = start + 1 + indent.length + extraIndent.length;
            handleInput(editorId);
        }
    }

    /**
     * Sync scroll between textarea and highlight
     */
    function syncScroll(editorId) {
        const input = document.getElementById(`${editorId}_input`);
        const highlight = document.getElementById(`${editorId}_highlight`);
        const lines = document.getElementById(`${editorId}_lines`);

        if (input && highlight) {
            highlight.scrollTop = input.scrollTop;
            highlight.scrollLeft = input.scrollLeft;
        }
        if (input && lines) {
            lines.scrollTop = input.scrollTop;
        }
    }

    /**
     * Update line numbers
     */
    function updateLineNumbers(editorId) {
        const input = document.getElementById(`${editorId}_input`);
        const lines = document.getElementById(`${editorId}_lines`);
        if (!input || !lines) return;

        const lineCount = input.value.split('\n').length;
        lines.innerHTML = Array.from({ length: lineCount }, (_, i) => i + 1).join('<br>');
    }

    /**
     * Update syntax highlighting
     */
    function updateHighlight(editorId) {
        const editor = editors.get(editorId);
        const input = document.getElementById(`${editorId}_input`);
        const highlight = document.getElementById(`${editorId}_highlight`);

        if (!editor || !input || !highlight) return;

        let code = escapeHtml(input.value);
        code = applySyntaxHighlight(code, editor.language);

        // Ensure trailing newline for proper alignment
        if (!code.endsWith('\n')) {
            code += '\n';
        }

        highlight.innerHTML = code;
    }

    /**
     * Apply syntax highlighting
     */
    function applySyntaxHighlight(code, language) {
        const syntax = SYNTAX[language];
        if (!syntax) return code;

        // Apply patterns in specific order
        // Comments first (to prevent highlighting inside comments)
        if (syntax.comments) {
            code = code.replace(syntax.comments, '<span class="code-comment">$&</span>');
        }

        // Strings
        if (syntax.strings) {
            code = code.replace(syntax.strings, '<span class="code-string">$&</span>');
        }

        // Decorators (Python)
        if (syntax.decorators) {
            code = code.replace(syntax.decorators, '<span class="code-decorator">$&</span>');
        }

        // Keywords
        if (syntax.keywords) {
            code = code.replace(syntax.keywords, '<span class="code-keyword">$&</span>');
        }

        // Functions
        if (syntax.functions) {
            code = code.replace(syntax.functions, '<span class="code-function">$1</span>');
        }

        // Numbers
        if (syntax.numbers) {
            code = code.replace(syntax.numbers, '<span class="code-number">$&</span>');
        }

        // YAML keys
        if (syntax.keys) {
            code = code.replace(syntax.keys, '<span class="code-key">$&</span>');
        }

        // Booleans
        if (syntax.booleans) {
            code = code.replace(syntax.booleans, '<span class="code-boolean">$&</span>');
        }

        return code;
    }

    /**
     * Set editor language
     */
    function setLanguage(editorId, language) {
        const editor = editors.get(editorId);
        if (editor) {
            editor.language = language;
            updateHighlight(editorId);
        }
    }

    /**
     * Get editor content
     */
    function getValue(editorId) {
        const input = document.getElementById(`${editorId}_input`);
        return input ? input.value : '';
    }

    /**
     * Set editor content
     */
    function setValue(editorId, value) {
        const input = document.getElementById(`${editorId}_input`);
        if (input) {
            input.value = value;
            handleInput(editorId);
        }
    }

    /**
     * Clear editor
     */
    function clear(editorId) {
        setValue(editorId, '');
    }

    /**
     * Copy content to clipboard
     */
    function copy(editorId) {
        const value = getValue(editorId);
        if (!value) {
            alert('No hay código para copiar');
            return;
        }

        if (navigator.clipboard) {
            navigator.clipboard.writeText(value).then(() => {
                showNotification('Código copiado');
            });
        } else {
            const textarea = document.createElement('textarea');
            textarea.value = value;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            showNotification('Código copiado');
        }
    }

    /**
     * Show notification
     */
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'code-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 2000);
    }

    /**
     * Escape HTML
     */
    function escapeHtml(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * Destroy editor
     */
    function destroy(editorId) {
        editors.delete(editorId);
        const container = document.getElementById(`${editorId}_container`);
        if (container) {
            container.remove();
        }
    }

    // Public API
    return {
        init,
        getValue,
        setValue,
        setLanguage,
        clear,
        copy,
        destroy
    };
})();

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CodeEditor;
}
