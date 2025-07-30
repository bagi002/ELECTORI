/**
 * API modul za komunikaciju sa ELECTORI backend-om
 */

class ElectoriAPI {
    constructor() {
        this.baseUrl = '';
        this.defaultHeaders = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * Generička metoda za API pozive
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}/api${endpoint}`;
        const config = {
            headers: this.defaultHeaders,
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Simulacije
    async getSimulations() {
        return this.request('/simulations');
    }

    async getSimulation(id) {
        return this.request(`/simulations/${id}`);
    }

    async createSimulation(data) {
        return this.request('/simulations', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateSimulation(id, data) {
        return this.request(`/simulations/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteSimulation(id) {
        return this.request(`/simulations/${id}`, {
            method: 'DELETE'
        });
    }

    async activateSimulation(id) {
        return this.request(`/simulations/${id}/activate`, {
            method: 'POST'
        });
    }

    async getActiveSimulation() {
        return this.request('/simulations/active');
    }

    // Gradovi
    async getCities() {
        return this.request('/cities');
    }

    async getCity(id) {
        return this.request(`/cities/${id}`);
    }

    async createCity(data) {
        return this.request('/cities', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateCity(id, data) {
        return this.request(`/cities/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteCity(id) {
        return this.request(`/cities/${id}`, {
            method: 'DELETE'
        });
    }

    async getCityStats(id) {
        return this.request(`/cities/${id}/stats`);
    }

    async searchCities(query) {
        return this.request(`/cities/search?q=${encodeURIComponent(query)}`);
    }

    // Partije
    async getParties() {
        return this.request('/parties');
    }

    async getParty(id) {
        return this.request(`/parties/${id}`);
    }

    async createParty(data) {
        return this.request('/parties', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateParty(id, data) {
        return this.request(`/parties/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteParty(id) {
        return this.request(`/parties/${id}`, {
            method: 'DELETE'
        });
    }

    async getPartySupport(id) {
        return this.request(`/parties/${id}/support`);
    }

    async searchParties(query) {
        return this.request(`/parties/search?q=${encodeURIComponent(query)}`);
    }

    async getIdeologies() {
        return this.request('/parties/ideologies');
    }

    // Utility metode
    async healthCheck(module = '') {
        const endpoint = module ? `/${module}/health` : '/health';
        return this.request(endpoint);
    }
}

// Kreiranje globalne instance
window.API = new ElectoriAPI();

/**
 * Utility funkcije za rad sa API-jem
 */
class UIUtils {
    static showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        const alertId = 'alert-' + Date.now();
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" id="${alertId}" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        alertContainer.insertAdjacentHTML('beforeend', alertHtml);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    static showLoader(element) {
        if (element) {
            element.classList.add('loading');
        }
    }

    static hideLoader(element) {
        if (element) {
            element.classList.remove('loading');
        }
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('sr-RS', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static formatNumber(number) {
        return new Intl.NumberFormat('sr-RS').format(number);
    }

    static validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return isValid;
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Globalni export utility funkcija
window.UIUtils = UIUtils;