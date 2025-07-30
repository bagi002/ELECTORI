/**
 * ELECTORI - Main JavaScript File
 * Core functionality and utilities for the application
 */

// Global application namespace
window.ELECTORI = {
    // Configuration
    config: {
        apiBaseUrl: '/api',
        version: '1.0.0',
        debug: true
    },
    
    // State management
    state: {
        activeSimulationId: null,
        currentPage: null,
        user: null
    },
    
    // Event handlers
    events: {},
    
    // Utility functions
    utils: {},
    
    // API functions
    api: {},
    
    // UI functions
    ui: {}
};

// Utility functions
ELECTORI.utils = {
    /**
     * Format number with thousands separator
     */
    formatNumber: function(num) {
        if (num == null) return '0';
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    /**
     * Format percentage with specified decimal places
     */
    formatPercentage: function(num, decimals = 2) {
        if (num == null) return '0.00%';
        return parseFloat(num).toFixed(decimals) + '%';
    },
    
    /**
     * Format date in readable format
     */
    formatDate: function(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('sr-Latn-RS', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    /**
     * Debounce function calls
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * Generate random color for parties
     */
    generateRandomColor: function() {
        const colors = [
            '#e74c3c', '#3498db', '#2ecc71', '#f39c12', 
            '#9b59b6', '#1abc9c', '#34495e', '#e67e22',
            '#95a5a6', '#f1c40f', '#8e44ad', '#16a085'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    },
    
    /**
     * Validate email format
     */
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    /**
     * Generate unique ID
     */
    generateId: function() {
        return '_' + Math.random().toString(36).substr(2, 9);
    },
    
    /**
     * Deep clone object
     */
    deepClone: function(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => this.deepClone(item));
        if (typeof obj === 'object') {
            const copy = {};
            Object.keys(obj).forEach(key => {
                copy[key] = this.deepClone(obj[key]);
            });
            return copy;
        }
    }
};

// API functions
ELECTORI.api = {
    /**
     * Make HTTP request with error handling
     */
    request: async function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(ELECTORI.config.apiBaseUrl + url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API Request failed:', error);
            ELECTORI.ui.showAlert('Greška u komunikaciji sa serverom: ' + error.message, 'danger');
            throw error;
        }
    },
    
    /**
     * GET request
     */
    get: function(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        return this.request(fullUrl);
    },
    
    /**
     * POST request
     */
    post: function(url, data = {}) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * PUT request
     */
    put: function(url, data = {}) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * DELETE request
     */
    delete: function(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    }
};

// UI functions
ELECTORI.ui = {
    /**
     * Show alert message
     */
    showAlert: function(message, type = 'info', duration = 5000) {
        const alertContainer = document.getElementById('alert-container') || this.createAlertContainer();
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto-dismiss after duration
        if (duration > 0) {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, duration);
        }
        
        return alert;
    },
    
    /**
     * Create alert container if it doesn't exist
     */
    createAlertContainer: function() {
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1050;
            max-width: 400px;
        `;
        document.body.appendChild(container);
        return container;
    },
    
    /**
     * Show loading spinner
     */
    showLoading: function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (element) {
            element.disabled = true;
            const originalHTML = element.innerHTML;
            element.innerHTML = '<span class="spinner"></span> Učitavanje...';
            element.dataset.originalHtml = originalHTML;
        }
    },
    
    /**
     * Hide loading spinner
     */
    hideLoading: function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (element && element.dataset.originalHtml) {
            element.disabled = false;
            element.innerHTML = element.dataset.originalHtml;
            delete element.dataset.originalHtml;
        }
    },
    
    /**
     * Show confirmation dialog
     */
    confirm: function(message, title = 'Potvrda') {
        return new Promise((resolve) => {
            const result = window.confirm(`${title}\n\n${message}`);
            resolve(result);
        });
    },
    
    /**
     * Safely get or create Bootstrap modal
     */
    getModal: function(modalElement) {
        if (typeof modalElement === 'string') {
            modalElement = document.getElementById(modalElement) || document.querySelector(modalElement);
        }
        
        if (!modalElement) {
            console.error('Modal element not found');
            return null;
        }
        
        // Check if bootstrap is available
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            return bootstrap.Modal.getOrCreateInstance(modalElement);
        } else {
            // Fallback: manual modal control
            console.warn('Bootstrap not available, using fallback modal');
            return {
                show: function() {
                    modalElement.style.display = 'block';
                    modalElement.classList.add('show');
                    document.body.classList.add('modal-open');
                },
                hide: function() {
                    modalElement.style.display = 'none';
                    modalElement.classList.remove('show');
                    document.body.classList.remove('modal-open');
                }
            };
        }
    },
    
    /**
     * Create modal dialog
     */
    createModal: function(title, content, options = {}) {
        const modalId = 'modal-' + ELECTORI.utils.generateId();
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = modalId;
        modal.innerHTML = `
            <div class="modal-dialog ${options.size || ''}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        return modal;
    },
    
    /**
     * Update page title
     */
    setPageTitle: function(title) {
        document.title = `${title} - ELECTORI`;
    },
    
    /**
     * Format and display data in table
     */
    populateTable: function(tableId, data, columns) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const tbody = table.querySelector('tbody') || table;
        tbody.innerHTML = '';
        
        data.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(col => {
                const td = document.createElement('td');
                if (typeof col.render === 'function') {
                    td.innerHTML = col.render(row[col.key], row);
                } else {
                    td.textContent = row[col.key] || '';
                }
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
};

// Event management
ELECTORI.events = {
    listeners: {},
    
    /**
     * Add event listener
     */
    on: function(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    },
    
    /**
     * Remove event listener
     */
    off: function(event, callback) {
        if (!this.listeners[event]) return;
        const index = this.listeners[event].indexOf(callback);
        if (index > -1) {
            this.listeners[event].splice(index, 1);
        }
    },
    
    /**
     * Trigger event
     */
    trigger: function(event, data) {
        if (!this.listeners[event]) return;
        this.listeners[event].forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                console.error('Event callback error:', error);
            }
        });
    }
};

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('ELECTORI application initialized');
    
    // Set up global error handling
    window.addEventListener('error', function(event) {
        console.error('Global error:', event.error);
        if (ELECTORI.config.debug) {
            ELECTORI.ui.showAlert(
                'Dogodila se neočekivana greška. Molimo osvežite stranicu.',
                'danger'
            );
        }
    });
    
    // Set up unhandled promise rejection handling
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        if (ELECTORI.config.debug) {
            ELECTORI.ui.showAlert(
                'Dogodila se greška u aplikaciji. Molimo pokušajte ponovo.',
                'warning'
            );
        }
    });
    
    // Load active simulation from session storage
    const activeSimulationId = sessionStorage.getItem('activeSimulationId');
    if (activeSimulationId) {
        ELECTORI.state.activeSimulationId = parseInt(activeSimulationId);
    }
    
    // Set up navigation
    const navLinks = document.querySelectorAll('[data-page]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.dataset.page;
            ELECTORI.events.trigger('navigate', { page });
        });
    });
    
    // Trigger application ready event
    ELECTORI.events.trigger('app:ready');
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ELECTORI;
}
