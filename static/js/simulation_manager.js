/**
 * Simulation Manager functionality for ELECTORI
 */

class SimulationManager {
    constructor() {
        this.activeSimulation = null;
        this.simulations = [];
        this.deleteSimulationId = null;
        this.init();
    }

    async init() {
        await this.loadSimulations();
        this.setupEventListeners();
        this.setupModals();
    }

    async loadSimulations() {
        try {
            UIUtils.showLoader(document.querySelector('.simulations-grid'));
            
            const [simulations, activeSimulation] = await Promise.all([
                API.getSimulations(),
                API.getActiveSimulation().catch(() => null)
            ]);

            this.simulations = simulations;
            this.activeSimulation = activeSimulation;
            
            this.renderSimulations();
            
        } catch (error) {
            console.error('Error loading simulations:', error);
            UIUtils.showAlert('Greška pri učitavanju simulacija', 'danger');
        } finally {
            UIUtils.hideLoader(document.querySelector('.simulations-grid'));
        }
    }

    renderSimulations() {
        const grid = document.getElementById('simulations-grid');
        if (!grid) return;

        if (this.simulations.length === 0) {
            grid.innerHTML = this.renderEmptyState();
            return;
        }

        grid.innerHTML = this.simulations.map(simulation => 
            this.renderSimulationCard(simulation)
        ).join('');

        // Add event listeners to cards
        this.setupCardEventListeners();
    }

    renderSimulationCard(simulation) {
        const isActive = this.activeSimulation && this.activeSimulation.id === simulation.id;
        const statusClass = simulation.status || 'active';
        
        return `
            <div class="simulation-card ${isActive ? 'active' : ''} fade-in-up" data-simulation-id="${simulation.id}">
                <div class="simulation-header">
                    <div class="simulation-info">
                        <h3>${simulation.name}</h3>
                        <div class="country-name">${simulation.country_name}</div>
                    </div>
                    <span class="simulation-status ${statusClass}">${this.getStatusLabel(statusClass)}</span>
                </div>
                
                <div class="simulation-stats">
                    <div class="stat-item">
                        <span class="number">${simulation.cities_count || 0}</span>
                        <span class="label">Gradovi</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">${simulation.parties_count || 0}</span>
                        <span class="label">Partije</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">${simulation.elections_count || 0}</span>
                        <span class="label">Izbori</span>
                    </div>
                </div>
                
                <div class="simulation-meta">
                    <span>Kreirana: ${UIUtils.formatDate(simulation.created_at)}</span>
                    ${simulation.last_played ? `<span>Poslednja igra: ${UIUtils.formatDate(simulation.last_played)}</span>` : ''}
                </div>
                
                <div class="simulation-actions">
                    ${!isActive ? `<button class="btn btn-primary btn-activate" data-id="${simulation.id}">
                        <i class="fas fa-play"></i> Aktiviraj
                    </button>` : `<button class="btn btn-success" disabled>
                        <i class="fas fa-check"></i> Aktivna
                    </button>`}
                    <button class="btn btn-outline-secondary btn-export" data-id="${simulation.id}">
                        <i class="fas fa-download"></i> Izvezi
                    </button>
                    <button class="btn btn-outline-danger btn-delete" data-id="${simulation.id}" data-name="${simulation.name}">
                        <i class="fas fa-trash"></i> Obriši
                    </button>
                </div>
            </div>
        `;
    }

    renderEmptyState() {
        return `
            <div class="empty-state">
                <i class="fas fa-globe"></i>
                <h3>Nema simulacija</h3>
                <p>Kreirajte novu simulaciju da počnete sa upravljanjem političkim sistemom vaše fiktivne države.</p>
                <button class="btn btn-primary btn-lg" id="create-first-simulation">
                    <i class="fas fa-plus"></i> Kreiraj prvu simulaciju
                </button>
            </div>
        `;
    }

    getStatusLabel(status) {
        const labels = {
            'active': 'Aktivna',
            'paused': 'Pauzirana',
            'completed': 'Završena'
        };
        return labels[status] || 'Aktivna';
    }

    setupCardEventListeners() {
        // Activate buttons
        document.querySelectorAll('.btn-activate').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const simulationId = btn.dataset.id;
                this.activateSimulation(simulationId);
            });
        });

        // Export buttons
        document.querySelectorAll('.btn-export').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const simulationId = btn.dataset.id;
                this.exportSimulation(simulationId);
            });
        });

        // Delete buttons
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const simulationId = btn.dataset.id;
                const simulationName = btn.dataset.name;
                this.showDeleteModal(simulationId, simulationName);
            });
        });

        // Card click for details
        document.querySelectorAll('.simulation-card').forEach(card => {
            card.addEventListener('click', () => {
                const simulationId = card.dataset.simulationId;
                this.showSimulationDetails(simulationId);
            });
        });

        // Empty state button
        const firstSimBtn = document.getElementById('create-first-simulation');
        if (firstSimBtn) {
            firstSimBtn.addEventListener('click', () => {
                this.showCreateModal();
            });
        }
    }

    setupEventListeners() {
        // Create simulation button
        const createBtn = document.getElementById('create-simulation-btn');
        if (createBtn) {
            createBtn.addEventListener('click', () => {
                this.showCreateModal();
            });
        }

        // Import button
        const importBtn = document.getElementById('import-simulation-btn');
        if (importBtn) {
            importBtn.addEventListener('click', () => {
                this.showImportDialog();
            });
        }

        // Save simulation button
        const saveBtn = document.getElementById('save-simulation-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                this.createSimulation();
            });
        }

        // Confirm delete button
        const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', () => {
                this.deleteSimulation();
            });
        }

        // Import file input
        const importInput = document.getElementById('import-file-input');
        if (importInput) {
            importInput.addEventListener('change', (e) => {
                this.handleImportFile(e.target.files[0]);
            });
        }
    }

    setupModals() {
        // Reset form when modal is shown
        const createModal = document.getElementById('createSimulationModal');
        if (createModal) {
            createModal.addEventListener('shown.bs.modal', () => {
                document.getElementById('create-simulation-form').reset();
                document.getElementById('simulation-name').focus();
            });
        }
    }

    showCreateModal() {
        const modal = new bootstrap.Modal(document.getElementById('createSimulationModal'));
        modal.show();
    }

    async createSimulation() {
        const form = document.getElementById('create-simulation-form');
        if (!UIUtils.validateForm(form)) {
            UIUtils.showAlert('Molimo popunite sva obavezna polja', 'warning');
            return;
        }

        const name = document.getElementById('simulation-name').value.trim();
        const countryName = document.getElementById('country-name').value.trim();

        try {
            UIUtils.showLoader(document.getElementById('save-simulation-btn'));

            const simulation = await API.createSimulation({
                name: name,
                country_name: countryName
            });

            UIUtils.showAlert(`Simulacija "${name}" je uspešno kreirana`, 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('createSimulationModal'));
            modal.hide();

            // Refresh list
            await this.loadSimulations();

        } catch (error) {
            console.error('Error creating simulation:', error);
            UIUtils.showAlert('Greška pri kreiranju simulacije: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('save-simulation-btn'));
        }
    }

    async activateSimulation(simulationId) {
        try {
            const card = document.querySelector(`[data-simulation-id="${simulationId}"]`);
            UIUtils.showLoader(card);

            await API.activateSimulation(simulationId);
            
            UIUtils.showAlert('Simulacija je uspešno aktivirana', 'success');
            
            // Redirect to dashboard after successful activation
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000); // Wait 1 second to show the success message

        } catch (error) {
            console.error('Error activating simulation:', error);
            UIUtils.showAlert('Greška pri aktivaciji simulacije: ' + error.message, 'danger');
        }
    }

    showDeleteModal(simulationId, simulationName) {
        this.deleteSimulationId = simulationId;
        
        document.getElementById('delete-simulation-name').textContent = simulationName;
        
        const modal = new bootstrap.Modal(document.getElementById('deleteSimulationModal'));
        modal.show();
    }

    async deleteSimulation() {
        if (!this.deleteSimulationId) return;

        try {
            UIUtils.showLoader(document.getElementById('confirm-delete-btn'));

            await API.deleteSimulation(this.deleteSimulationId);
            
            UIUtils.showAlert('Simulacija je uspešno obrisana', 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteSimulationModal'));
            modal.hide();

            // Refresh list
            await this.loadSimulations();

        } catch (error) {
            console.error('Error deleting simulation:', error);
            UIUtils.showAlert('Greška pri brisanju simulacije: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('confirm-delete-btn'));
            this.deleteSimulationId = null;
        }
    }

    showImportDialog() {
        document.getElementById('import-file-input').click();
    }

    async handleImportFile(file) {
        if (!file) return;

        if (file.type !== 'application/json') {
            UIUtils.showAlert('Molimo odaberite JSON fajl', 'warning');
            return;
        }

        try {
            const content = await file.text();
            const data = JSON.parse(content);
            
            // TODO: Implement import validation and processing
            UIUtils.showAlert('Import funkcionalnost će biti dostupna u sledećoj fazi', 'info');
            
        } catch (error) {
            console.error('Error importing file:', error);
            UIUtils.showAlert('Greška pri čitanju fajla: ' + error.message, 'danger');
        }
    }

    async exportSimulation(simulationId) {
        try {
            // TODO: Implement export functionality
            UIUtils.showAlert('Export funkcionalnost će biti dostupna u sledećoj fazi', 'info');
            
        } catch (error) {
            console.error('Error exporting simulation:', error);
            UIUtils.showAlert('Greška pri eksportu simulacije: ' + error.message, 'danger');
        }
    }

    showSimulationDetails(simulationId) {
        // TODO: Implement simulation details view
        console.log('Show details for simulation:', simulationId);
    }
}

// Initialize simulation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.simulationManager = new SimulationManager();
});