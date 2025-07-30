/**
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
});