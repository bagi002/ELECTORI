/**
 * ELECTORI UI Framework - Modern JavaScript components
 * Replaces Bootstrap with enhanced functionality
 */

class ElectoriUI {
    constructor() {
        this.modals = new Map();
        this.alerts = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
    }

    setupEventListeners() {
        // Modal backdrop clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideModal(e.target);
            }
        });

        // Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal.show');
                if (activeModal) {
                    this.hideModal(activeModal);
                }
            }
        });

        // Alert close buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.alert-close')) {
                const alert = e.target.closest('.alert');
                if (alert) {
                    this.closeAlert(alert);
                }
            }
        });
    }

    initializeComponents() {
        // Initialize any existing modals
        document.querySelectorAll('.modal').forEach(modal => {
            this.registerModal(modal);
        });
    }

    // Modal System
    registerModal(modalElement) {
        const id = modalElement.id || `modal-${Date.now()}`;
        modalElement.id = id;
        this.modals.set(id, modalElement);
        return id;
    }

    showModal(modalId) {
        const modal = typeof modalId === 'string' ? 
            this.modals.get(modalId) || document.getElementById(modalId) :
            modalId;
        
        if (!modal) return false;

        // Add modal to registry if not exists
        if (!modal.id || !this.modals.has(modal.id)) {
            this.registerModal(modal);
        }

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Focus trap
        this.trapFocus(modal);
        
        // Trigger event
        this.triggerEvent(modal, 'modal:show');
        
        return true;
    }

    hideModal(modalId) {
        const modal = typeof modalId === 'string' ? 
            this.modals.get(modalId) || document.getElementById(modalId) :
            modalId;
        
        if (!modal) return false;

        modal.classList.remove('show');
        document.body.style.overflow = '';
        
        // Trigger event
        this.triggerEvent(modal, 'modal:hide');
        
        return true;
    }

    createModal(options = {}) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    ${options.header ? `
                        <div class="modal-header">
                            <h5 class="modal-title">${options.title || 'Modal'}</h5>
                            <button type="button" class="btn btn-sm btn-outline modal-close" data-dismiss="modal">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>
                        </div>
                    ` : ''}
                    <div class="modal-body">
                        ${options.body || ''}
                    </div>
                    ${options.footer ? `
                        <div class="modal-footer">
                            ${options.footer}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Setup close button
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hideModal(modal));
        }

        const modalId = this.registerModal(modal);
        return modalId;
    }

    // Alert System
    showAlert(message, type = 'info', duration = 5000) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.innerHTML = `
            <div class="alert-content">
                <div class="alert-icon">
                    ${this.getAlertIcon(type)}
                </div>
                <div class="alert-message">${message}</div>
            </div>
            <button type="button" class="alert-close btn btn-sm">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        `;

        // Position alerts
        let alertContainer = document.querySelector('.alert-container');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.className = 'alert-container';
            alertContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1100;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(alertContainer);
        }

        alert.style.pointerEvents = 'auto';
        alertContainer.appendChild(alert);
        this.alerts.push(alert);

        // Auto close
        if (duration > 0) {
            setTimeout(() => this.closeAlert(alert), duration);
        }

        return alert;
    }

    closeAlert(alert) {
        if (!alert.parentNode) return;
        
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
            const index = this.alerts.indexOf(alert);
            if (index > -1) {
                this.alerts.splice(index, 1);
            }
        }, 300);
    }

    getAlertIcon(type) {
        const icons = {
            success: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20,6 9,17 4,12"></polyline></svg>',
            danger: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
            warning: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            info: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        };
        return icons[type] || icons.info;
    }

    // Progress Bar System
    updateProgress(element, percentage, animated = true) {
        const progressBar = typeof element === 'string' ? 
            document.querySelector(element) : element;
        
        if (!progressBar) return;

        progressBar.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
        
        if (animated) {
            progressBar.classList.add('animated');
        }
        
        // Update text if exists
        const text = progressBar.querySelector('.progress-text');
        if (text) {
            text.textContent = `${Math.round(percentage)}%`;
        }
    }

    // Form Validation
    validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        const errors = [];

        inputs.forEach(input => {
            this.clearFieldError(input);
            
            if (!input.value.trim()) {
                this.showFieldError(input, 'This field is required');
                isValid = false;
                errors.push(input);
            } else if (input.type === 'email' && !this.isValidEmail(input.value)) {
                this.showFieldError(input, 'Please enter a valid email address');
                isValid = false;
                errors.push(input);
            }
        });

        return { isValid, errors };
    }

    showFieldError(input, message) {
        input.classList.add('error');
        
        let errorElement = input.parentNode.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            errorElement.style.cssText = `
                color: var(--danger-500);
                font-size: 0.75rem;
                margin-top: 0.25rem;
            `;
            input.parentNode.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
    }

    clearFieldError(input) {
        input.classList.remove('error');
        const errorElement = input.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Utility Functions
    trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleTabKey = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        };

        element.addEventListener('keydown', handleTabKey);
        firstElement.focus();
    }

    triggerEvent(element, eventName, detail = null) {
        const event = new CustomEvent(eventName, {
            detail,
            bubbles: true,
            cancelable: true
        });
        element.dispatchEvent(event);
    }

    // Animation helpers
    animate(element, animation, duration = 300) {
        return new Promise(resolve => {
            element.style.animation = `${animation} ${duration}ms ease-in-out`;
            
            setTimeout(() => {
                element.style.animation = '';
                resolve();
            }, duration);
        });
    }

    // Loading states
    setLoading(button, loading = true) {
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.innerHTML = `
                <svg class="loading-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                Loading...
            `;
            
            // Add spinner animation
            const spinner = button.querySelector('.loading-spinner');
            if (spinner) {
                spinner.style.animation = 'spin 1s linear infinite';
            }
        } else {
            button.disabled = false;
            button.textContent = button.dataset.originalText || 'Submit';
        }
    }

    // Responsive utilities
    isMobile() {
        return window.innerWidth <= 768;
    }

    isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    }

    isDesktop() {
        return window.innerWidth > 1024;
    }
}

// Chart.js replacement for basic charts
class ElectoriChart {
    constructor(canvas, config) {
        this.canvas = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
        this.ctx = this.canvas.getContext('2d');
        this.config = config;
        this.data = config.data || {};
        this.options = config.options || {};
        
        this.render();
    }

    render() {
        const { width, height } = this.canvas;
        this.ctx.clearRect(0, 0, width, height);
        
        switch (this.config.type) {
            case 'doughnut':
                this.renderDoughnut();
                break;
            case 'bar':
                this.renderBar();
                break;
            case 'line':
                this.renderLine();
                break;
            default:
                console.warn('Chart type not supported:', this.config.type);
        }
    }

    renderDoughnut() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;
        const innerRadius = radius * 0.6; // Doughnut hole
        
        const dataset = this.data.datasets[0];
        const data = dataset.data;
        const backgroundColor = dataset.backgroundColor;
        const total = data.reduce((sum, value) => sum + value, 0);
        
        let currentAngle = -Math.PI / 2; // Start from top
        
        data.forEach((value, index) => {
            const sliceAngle = (value / total) * 2 * Math.PI;
            
            // Draw slice
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            this.ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true);
            this.ctx.closePath();
            
            this.ctx.fillStyle = backgroundColor[index] || `hsl(${index * 60}, 70%, 50%)`;
            this.ctx.fill();
            
            currentAngle += sliceAngle;
        });
        
        // Draw legend if requested
        if (this.options.plugins?.legend?.position) {
            this.drawLegend();
        }
    }

    renderBar() {
        const padding = 40;
        const chartWidth = this.canvas.width - (padding * 2);
        const chartHeight = this.canvas.height - (padding * 2);
        
        const dataset = this.data.datasets[0];
        const data = dataset.data;
        const labels = this.data.labels;
        const maxValue = Math.max(...data);
        
        const barWidth = chartWidth / data.length * 0.8;
        const barSpacing = chartWidth / data.length * 0.2;
        
        data.forEach((value, index) => {
            const barHeight = (value / maxValue) * chartHeight;
            const x = padding + (index * (barWidth + barSpacing));
            const y = this.canvas.height - padding - barHeight;
            
            this.ctx.fillStyle = dataset.backgroundColor || '#3b82f6';
            this.ctx.fillRect(x, y, barWidth, barHeight);
            
            // Draw labels
            this.ctx.fillStyle = '#374151';
            this.ctx.font = '12px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(labels[index], x + barWidth/2, this.canvas.height - 10);
        });
    }

    drawLegend() {
        // Simple legend implementation
        const legendY = this.canvas.height - 30;
        let legendX = 10;
        
        this.data.labels.forEach((label, index) => {
            const color = this.data.datasets[0].backgroundColor[index];
            
            // Color box
            this.ctx.fillStyle = color;
            this.ctx.fillRect(legendX, legendY, 12, 12);
            
            // Label text
            this.ctx.fillStyle = '#374151';
            this.ctx.font = '11px sans-serif';
            this.ctx.fillText(label, legendX + 16, legendY + 9);
            
            legendX += this.ctx.measureText(label).width + 30;
        });
    }

    update() {
        this.render();
    }

    destroy() {
        // Cleanup if needed
    }
}

// Global initialization
let electoriUI;
let Chart; // Chart.js compatible

document.addEventListener('DOMContentLoaded', () => {
    electoriUI = new ElectoriUI();
    
    // Make Chart available globally for compatibility
    window.Chart = ElectoriChart;
    Chart = ElectoriChart;
    Chart.defaults = {
        font: { family: 'sans-serif' },
        color: '#374151'
    };
    
    // Bootstrap compatibility layer
    window.bootstrap = {
        Modal: {
            getInstance: (element) => ({
                show: () => electoriUI.showModal(element),
                hide: () => electoriUI.hideModal(element)
            })
        }
    };
    
    // Add CSS for spinner animation
    if (!document.querySelector('#electori-ui-styles')) {
        const style = document.createElement('style');
        style.id = 'electori-ui-styles';
        style.textContent = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .alert-container .alert {
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }
            
            .alert-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .form-control.error {
                border-color: var(--danger-500);
                box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
            }
        `;
        document.head.appendChild(style);
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ElectoriUI, ElectoriChart };
}