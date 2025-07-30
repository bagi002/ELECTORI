"""
Task 2.1: Frontend Framework i Layout Implementation

Implementira osnovni frontend sa HTML templates, CSS styling i JavaScript modules.
"""

from pathlib import Path
from task_implementations import BaseTaskImplementation

class FrontendImplementation(BaseTaskImplementation):
    """Implementacija Task 2.1: Frontend Framework i Layout."""
    
    def execute(self) -> bool:
        """Izvršava implementaciju frontend framework-a."""
        self.logger.info("Pokretanje implementacije Frontend Framework i Layout")
        
        steps = [
            self._create_dashboard_template,
            self._create_simulation_manager_template,
            self._update_base_template,
            self._create_dashboard_css,
            self._create_api_js,
            self._create_dashboard_js,
            self._update_main_css,
            self._test_frontend_components
        ]
        
        for step in steps:
            if not step():
                return False
        
        self.logger.info("Frontend Framework i Layout uspešno implementiran")
        return True
    
    def _create_dashboard_template(self) -> bool:
        """Kreira dashboard.html template."""
        content = '''{% extends "base.html" %}

{% block title %}Dashboard - ELECTORI{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
{% endblock %}

{% block content %}
<div class="dashboard-container">
    <!-- Header sa statistikama -->
    <div class="dashboard-header">
        <div class="row">
            <div class="col-md-3">
                <div class="stats-card">
                    <div class="stats-icon">
                        <i class="fas fa-globe"></i>
                    </div>
                    <div class="stats-content">
                        <h3 id="active-simulation-name">Nema aktivne simulacije</h3>
                        <p>Aktivna simulacija</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <div class="stats-icon">
                        <i class="fas fa-city"></i>
                    </div>
                    <div class="stats-content">
                        <h3 id="total-cities">0</h3>
                        <p>Ukupno gradova</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <div class="stats-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="stats-content">
                        <h3 id="total-parties">0</h3>
                        <p>Ukupno partija</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <div class="stats-icon">
                        <i class="fas fa-vote-yea"></i>
                    </div>
                    <div class="stats-content">
                        <h3 id="total-elections">0</h3>
                        <p>Ukupno izbora</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Glavna sekcija dashboard-a -->
    <div class="dashboard-main">
        <div class="row">
            <!-- Aktivnost timeline -->
            <div class="col-md-8">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h4><i class="fas fa-clock"></i> Poslednje aktivnosti</h4>
                    </div>
                    <div class="card-body">
                        <div id="activity-timeline">
                            <div class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-info-circle"></i>
                                </div>
                                <div class="activity-content">
                                    <p>Dobrodošli u ELECTORI!</p>
                                    <small class="text-muted">Kreirajte novu simulaciju da počnete.</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Quick actions -->
            <div class="col-md-4">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h4><i class="fas fa-bolt"></i> Brze akcije</h4>
                    </div>
                    <div class="card-body">
                        <div class="quick-actions">
                            <a href="/simulation-manager" class="quick-action-btn" id="manage-simulations">
                                <i class="fas fa-cogs"></i>
                                <span>Upravljaj simulacijama</span>
                            </a>
                            <a href="/city-manager" class="quick-action-btn" id="manage-cities">
                                <i class="fas fa-city"></i>
                                <span>Upravljaj gradovima</span>
                            </a>
                            <a href="/party-manager" class="quick-action-btn" id="manage-parties">
                                <i class="fas fa-users"></i>
                                <span>Upravljaj partijama</span>
                            </a>
                            <button class="quick-action-btn" id="create-election">
                                <i class="fas fa-vote-yea"></i>
                                <span>Kreiraj izbore</span>
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Upozorenja -->
                <div class="dashboard-card">
                    <div class="card-header">
                        <h4><i class="fas fa-exclamation-triangle"></i> Upozorenja</h4>
                    </div>
                    <div class="card-body">
                        <div id="warnings-list">
                            <!-- Dinamički sadržaj -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
{% endblock %}'''
        
        file_path = self.templates_dir / "dashboard.html"
        return self.create_file(file_path, content)
    
    def _create_simulation_manager_template(self) -> bool:
        """Kreira simulation_manager.html template."""
        content = '''{% extends "base.html" %}

{% block title %}Upravljanje simulacijama - ELECTORI{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/simulation.css') }}">
{% endblock %}

{% block content %}
<div class="simulation-manager">
    <div class="container-fluid">
        <!-- Header sa dugmićima -->
        <div class="manager-header">
            <div class="row align-items-center">
                <div class="col">
                    <h2><i class="fas fa-globe"></i> Upravljanje simulacijama</h2>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" id="create-simulation-btn">
                        <i class="fas fa-plus"></i> Nova simulacija
                    </button>
                    <button class="btn btn-secondary" id="import-simulation-btn">
                        <i class="fas fa-upload"></i> Uvezi
                    </button>
                </div>
            </div>
        </div>

        <!-- Lista simulacija -->
        <div class="simulations-grid" id="simulations-grid">
            <!-- Dinamički sadržaj -->
        </div>
    </div>
</div>

<!-- Modal za kreiranje simulacije -->
<div class="modal fade" id="createSimulationModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Kreiranje nove simulacije</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="create-simulation-form">
                    <div class="mb-3">
                        <label for="simulation-name" class="form-label">Naziv simulacije</label>
                        <input type="text" class="form-control" id="simulation-name" required>
                    </div>
                    <div class="mb-3">
                        <label for="country-name" class="form-label">Naziv države</label>
                        <input type="text" class="form-control" id="country-name" required>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-primary" id="save-simulation-btn">Kreiraj</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal za brisanje simulacije -->
<div class="modal fade" id="deleteSimulationModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Potvrda brisanja</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Da li ste sigurni da želite da obrišete simulaciju <strong id="delete-simulation-name"></strong>?</p>
                <p class="text-danger">Ova akcija se ne može poništiti.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-danger" id="confirm-delete-btn">Obriši</button>
            </div>
        </div>
    </div>
</div>

<!-- Hidden file input za import -->
<input type="file" id="import-file-input" accept=".json" style="display: none;">
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script src="{{ url_for('static', filename='js/simulation_manager.js') }}"></script>
{% endblock %}'''
        
        file_path = self.templates_dir / "simulation_manager.html"
        return self.create_file(file_path, content)
    
    def _update_base_template(self) -> bool:
        """Ažurira base.html template sa navigacijom."""
        # Prvo pravi backup postojećeg fajla
        base_path = self.templates_dir / "base.html"
        if not self.backup_file(base_path):
            return False
        
        content = '''<!DOCTYPE html>
<html lang="sr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ELECTORI - Simulacija Političkih Izbora{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-vote-yea"></i>
                ELECTORI
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/dashboard">
                            <i class="fas fa-tachometer-alt"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/simulation-manager">
                            <i class="fas fa-globe"></i> Simulacije
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/city-manager">
                            <i class="fas fa-city"></i> Gradovi
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/party-manager">
                            <i class="fas fa-users"></i> Partije
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/elections">
                            <i class="fas fa-vote-yea"></i> Izbori
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/parliament">
                            <i class="fas fa-landmark"></i> Parlament
                        </a>
                    </li>
                </ul>
                
                <ul class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="activeSimulationDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-globe"></i>
                            <span id="active-simulation-display">Nema aktivne simulacije</span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/simulation-manager">Promeni simulaciju</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="#" id="export-simulation">Izvezi simulaciju</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Alert container -->
    <div id="alert-container" class="container-fluid mt-3">
        <!-- Dinamički alerts -->
    </div>

    <!-- Main content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer bg-dark text-light mt-5">
        <div class="container">
            <div class="row py-4">
                <div class="col-md-6">
                    <h5>ELECTORI</h5>
                    <p>Simulacija političkih izbora i parlamentarnog sistema.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>&copy; 2025 ELECTORI. Sva prava zadržana.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Main JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''
        
        return self.create_file(base_path, content)
    
    def _create_dashboard_css(self) -> bool:
        """Kreira dashboard.css fajl."""
        content = '''/* Dashboard styling */
.dashboard-container {
    padding: 2rem 1rem;
    background-color: #f8f9fa;
    min-height: calc(100vh - 200px);
}

.dashboard-header {
    margin-bottom: 2rem;
}

.stats-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.stats-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.stats-icon {
    font-size: 2.5rem;
    margin-right: 1rem;
    color: #007bff;
    min-width: 60px;
}

.stats-content h3 {
    margin: 0;
    font-size: 2rem;
    font-weight: bold;
    color: #2c3e50;
}

.stats-content p {
    margin: 0;
    color: #6c757d;
    font-size: 0.9rem;
}

.dashboard-card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    overflow: hidden;
}

.dashboard-card .card-header {
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
    padding: 1rem 1.5rem;
    border: none;
}

.dashboard-card .card-header h4 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
}

.dashboard-card .card-body {
    padding: 1.5rem;
}

/* Activity timeline */
.activity-timeline {
    max-height: 400px;
    overflow-y: auto;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    padding: 1rem 0;
    border-bottom: 1px solid #e9ecef;
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-icon {
    font-size: 1.2rem;
    color: #007bff;
    margin-right: 1rem;
    margin-top: 0.2rem;
}

.activity-content p {
    margin: 0;
    font-weight: 500;
}

.activity-content small {
    display: block;
    margin-top: 0.25rem;
}

/* Quick actions */
.quick-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.quick-action-btn {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    text-decoration: none;
    color: #495057;
    transition: all 0.3s ease;
    cursor: pointer;
}

.quick-action-btn:hover {
    background: #007bff;
    border-color: #007bff;
    color: white;
    text-decoration: none;
    transform: translateX(5px);
}

.quick-action-btn i {
    font-size: 1.25rem;
    margin-right: 0.75rem;
    min-width: 24px;
}

.quick-action-btn span {
    font-weight: 500;
}

/* Responsive design */
@media (max-width: 768px) {
    .dashboard-container {
        padding: 1rem 0.5rem;
    }
    
    .stats-card {
        flex-direction: column;
        text-align: center;
    }
    
    .stats-icon {
        margin-right: 0;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-main .col-md-8,
    .dashboard-main .col-md-4 {
        margin-bottom: 1rem;
    }
}

/* Loading states */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

.loading::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}'''
        
        file_path = self.static_dir / "css" / "dashboard.css"
        return self.create_file(file_path, content)
    
    def _create_api_js(self) -> bool:
        """Kreira api.js fajl za komunikaciju sa backend-om."""
        content = '''/**
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
window.UIUtils = UIUtils;'''
        
        file_path = self.static_dir / "js" / "api.js"
        return self.create_file(file_path, content)
    
    def _create_dashboard_js(self) -> bool:
        """Kreira dashboard.js fajl."""
        content = '''/**
 * Dashboard functionality for ELECTORI
 */

class Dashboard {
    constructor() {
        this.refreshInterval = null;
        this.init();
    }

    async init() {
        await this.loadDashboardData();
        this.setupEventListeners();
        this.startAutoRefresh();
    }

    async loadDashboardData() {
        try {
            await this.updateActiveSimulation();
            await this.updateStatistics();
            await this.updateActivityTimeline();
            await this.updateWarnings();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            UIUtils.showAlert('Greška pri učitavanju dashboard podataka', 'danger');
        }
    }

    async updateActiveSimulation() {
        try {
            const simulation = await API.getActiveSimulation();
            
            // Update navigation
            const navDisplay = document.getElementById('active-simulation-display');
            if (navDisplay) {
                navDisplay.textContent = simulation.name;
            }

            // Update dashboard
            const dashboardName = document.getElementById('active-simulation-name');
            if (dashboardName) {
                dashboardName.textContent = simulation.name;
            }

            return simulation;
        } catch (error) {
            // No active simulation
            const navDisplay = document.getElementById('active-simulation-display');
            if (navDisplay) {
                navDisplay.textContent = 'Nema aktivne simulacije';
            }

            const dashboardName = document.getElementById('active-simulation-name');
            if (dashboardName) {
                dashboardName.textContent = 'Nema aktivne simulacije';
            }

            return null;
        }
    }

    async updateStatistics() {
        try {
            const activeSimulation = await this.updateActiveSimulation();
            
            if (!activeSimulation) {
                this.setStatistic('total-cities', 0);
                this.setStatistic('total-parties', 0);
                this.setStatistic('total-elections', 0);
                return;
            }

            // Učitaj statistike
            const [cities, parties] = await Promise.all([
                API.getCities().catch(() => []),
                API.getParties().catch(() => [])
            ]);

            this.setStatistic('total-cities', cities.length);
            this.setStatistic('total-parties', parties.length);
            this.setStatistic('total-elections', 0); // TODO: Implementirati kada budu dostupni

        } catch (error) {
            console.error('Error updating statistics:', error);
        }
    }

    setStatistic(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = UIUtils.formatNumber(value);
        }
    }

    async updateActivityTimeline() {
        const timeline = document.getElementById('activity-timeline');
        if (!timeline) return;

        try {
            // Simuliramo aktivnost (u budućnosti može doći iz API-ja)
            const activities = await this.getRecentActivities();
            
            timeline.innerHTML = activities.map(activity => `
                <div class="activity-item">
                    <div class="activity-icon">
                        <i class="${activity.icon}"></i>
                    </div>
                    <div class="activity-content">
                        <p>${activity.message}</p>
                        <small class="text-muted">${UIUtils.formatDate(activity.timestamp)}</small>
                    </div>
                </div>
            `).join('');

        } catch (error) {
            console.error('Error updating activity timeline:', error);
        }
    }

    async getRecentActivities() {
        // Mock data - u budućnosti će doći iz API-ja
        return [
            {
                icon: 'fas fa-info-circle',
                message: 'Dobrodošli u ELECTORI!',
                timestamp: new Date().toISOString()
            }
        ];
    }

    async updateWarnings() {
        const warningsList = document.getElementById('warnings-list');
        if (!warningsList) return;

        try {
            const warnings = await this.getSystemWarnings();
            
            if (warnings.length === 0) {
                warningsList.innerHTML = '<p class="text-muted">Nema upozorenja</p>';
                return;
            }

            warningsList.innerHTML = warnings.map(warning => `
                <div class="alert alert-${warning.type} alert-sm" role="alert">
                    <i class="${warning.icon}"></i>
                    ${warning.message}
                </div>
            `).join('');

        } catch (error) {
            console.error('Error updating warnings:', error);
        }
    }

    async getSystemWarnings() {
        const warnings = [];

        try {
            const activeSimulation = await this.updateActiveSimulation();
            
            if (!activeSimulation) {
                warnings.push({
                    type: 'warning',
                    icon: 'fas fa-exclamation-triangle',
                    message: 'Nema aktivne simulacije. Kreirajte novu simulaciju da počnete.'
                });
                return warnings;
            }

            // Proveri da li ima gradova
            const cities = await API.getCities().catch(() => []);
            if (cities.length === 0) {
                warnings.push({
                    type: 'info',
                    icon: 'fas fa-city',
                    message: 'Dodajte gradove u simulaciju da možete kreirati partije i izbore.'
                });
            }

            // Proveri da li ima partija
            const parties = await API.getParties().catch(() => []);
            if (parties.length === 0) {
                warnings.push({
                    type: 'info',
                    icon: 'fas fa-users',
                    message: 'Dodajte partije u simulaciju da možete kreirati izbore.'
                });
            }

            // TODO: Dodati ostala upozorenja

        } catch (error) {
            console.error('Error getting system warnings:', error);
        }

        return warnings;
    }

    setupEventListeners() {
        // Quick action buttons
        const manageSimulations = document.getElementById('manage-simulations');
        const manageCities = document.getElementById('manage-cities');
        const manageParties = document.getElementById('manage-parties');
        const createElection = document.getElementById('create-election');

        if (manageSimulations) {
            manageSimulations.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = '/simulation-manager';
            });
        }

        if (manageCities) {
            manageCities.addEventListener('click', async (e) => {
                e.preventDefault();
                const activeSimulation = await this.updateActiveSimulation();
                if (!activeSimulation) {
                    UIUtils.showAlert('Prvo morate aktivirati simulaciju', 'warning');
                    return;
                }
                window.location.href = '/city-manager';
            });
        }

        if (manageParties) {
            manageParties.addEventListener('click', async (e) => {
                e.preventDefault();
                const activeSimulation = await this.updateActiveSimulation();
                if (!activeSimulation) {
                    UIUtils.showAlert('Prvo morate aktivirati simulaciju', 'warning');
                    return;
                }
                window.location.href = '/party-manager';
            });
        }

        if (createElection) {
            createElection.addEventListener('click', async (e) => {
                e.preventDefault();
                const activeSimulation = await this.updateActiveSimulation();
                if (!activeSimulation) {
                    UIUtils.showAlert('Prvo morate aktivirati simulaciju', 'warning');
                    return;
                }
                UIUtils.showAlert('Kreiranje izbora će biti dostupno u sledećoj fazi', 'info');
            });
        }

        // Export simulation
        const exportBtn = document.getElementById('export-simulation');
        if (exportBtn) {
            exportBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.exportActiveSimulation();
            });
        }
    }

    async exportActiveSimulation() {
        try {
            const simulation = await API.getActiveSimulation();
            if (!simulation) {
                UIUtils.showAlert('Nema aktivne simulacije za eksport', 'warning');
                return;
            }

            // TODO: Implementirati eksport funkcionalnost
            UIUtils.showAlert('Eksport funkcionalnost će biti dostupna u sledećoj fazi', 'info');

        } catch (error) {
            console.error('Error exporting simulation:', error);
            UIUtils.showAlert('Greška pri eksportu simulacije', 'danger');
        }
    }

    startAutoRefresh() {
        // Refresh dashboard every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 30000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});'''
        
        file_path = self.static_dir / "js" / "dashboard.js"
        return self.create_file(file_path, content)
    
    def _update_main_css(self) -> bool:
        """Ažurira main CSS fajl sa osnovnim styling-om."""
        # Prvo pravi backup
        css_path = self.static_dir / "css" / "style.css"
        if not self.backup_file(css_path):
            return False
        
        content = '''/* ELECTORI Custom Styles */

:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
    
    --font-family-sans-serif: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --border-radius: 0.375rem;
    --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --transition: all 0.15s ease-in-out;
}

/* Base styling */
body {
    font-family: var(--font-family-sans-serif);
    line-height: 1.6;
    color: #212529;
    background-color: #f8f9fa;
}

/* Navigation enhancements */
.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

.navbar-nav .nav-link {
    font-weight: 500;
    transition: var(--transition);
}

.navbar-nav .nav-link:hover {
    color: #fff !important;
}

/* Main content */
.main-content {
    min-height: calc(100vh - 160px);
    padding-top: 1rem;
}

/* Footer */
.footer {
    margin-top: auto;
}

/* Form enhancements */
.form-control:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn {
    border-radius: var(--border-radius);
    font-weight: 500;
    transition: var(--transition);
}

.btn:hover {
    transform: translateY(-1px);
}

/* Card styling */
.card {
    border: none;
    border-radius: 10px;
    box-shadow: var(--box-shadow);
    transition: var(--transition);
}

.card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* Alert styling */
.alert {
    border: none;
    border-radius: var(--border-radius);
}

/* Loading spinner */
.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}

/* Custom utilities */
.text-truncate-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.text-truncate-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Responsive utilities */
@media (max-width: 576px) {
    .main-content {
        padding-top: 0.5rem;
    }
    
    .container-fluid {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
}

/* Animation utilities */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.slide-up {
    animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #999;
}

/* Print styles */
@media print {
    .navbar,
    .footer,
    .btn,
    .alert {
        display: none !important;
    }
    
    .main-content {
        padding: 0;
    }
}'''
        
        return self.create_file(css_path, content)
    
    def _test_frontend_components(self) -> bool:
        """Testira kreirana frontend komponente."""
        self.logger.info("Testiranje frontend komponenti...")
        
        # Proveri da li su fajlovi kreirani
        required_files = [
            self.templates_dir / "dashboard.html",
            self.templates_dir / "simulation_manager.html",
            self.templates_dir / "base.html",
            self.static_dir / "css" / "dashboard.css",
            self.static_dir / "js" / "api.js",
            self.static_dir / "js" / "dashboard.js",
            self.static_dir / "css" / "style.css"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                self.logger.error(f"Nedostaje fajl: {file_path}")
                return False
            
            # Osnovne validacije sadržaja
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.suffix == '.html':
                if not self.validate_html(content):
                    return False
            elif file_path.suffix == '.css':
                if not self.validate_css(content):
                    return False
            elif file_path.suffix == '.js':
                if not self.validate_js(content):
                    return False
        
        self.logger.info("Svi frontend fajlovi su uspešno kreirani i validni")
        return True