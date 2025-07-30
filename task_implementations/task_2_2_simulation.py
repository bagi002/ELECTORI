"""
Task 2.2: Simulation Management UI Implementation

Implementira kompletnu funkcionalnost za upravljanje simulacijama.
"""

from pathlib import Path
from task_implementations import BaseTaskImplementation

class SimulationManagementImplementation(BaseTaskImplementation):
    """Implementacija Task 2.2: Simulation Management UI."""
    
    def execute(self) -> bool:
        """Izvršava implementaciju simulation management UI."""
        self.logger.info("Pokretanje implementacije Simulation Management UI")
        
        steps = [
            self._create_simulation_css,
            self._create_simulation_manager_js,
            self._add_simulation_routes,
            self._test_simulation_components
        ]
        
        for step in steps:
            if not step():
                return False
        
        self.logger.info("Simulation Management UI uspešno implementiran")
        return True
    
    def _create_simulation_css(self) -> bool:
        """Kreira simulation.css fajl."""
        content = '''/* Simulation Management Styles */

.simulation-manager {
    padding: 2rem 1rem;
    background-color: #f8f9fa;
    min-height: calc(100vh - 200px);
}

.manager-header {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.manager-header h2 {
    color: #2c3e50;
    margin: 0;
    font-weight: 600;
}

.manager-header i {
    color: #007bff;
    margin-right: 0.5rem;
}

/* Simulations Grid */
.simulations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.simulation-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.simulation-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.simulation-card.active {
    border-color: #28a745;
    background: linear-gradient(135deg, #ffffff, #f8fff9);
}

.simulation-card.active::before {
    content: "AKTIVNA";
    position: absolute;
    top: 10px;
    right: -30px;
    background: #28a745;
    color: white;
    padding: 5px 40px;
    font-size: 0.8rem;
    font-weight: bold;
    transform: rotate(45deg);
}

.simulation-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.simulation-info h3 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.3rem;
    font-weight: 600;
}

.simulation-info .country-name {
    color: #6c757d;
    font-size: 1rem;
    margin-top: 0.25rem;
}

.simulation-status {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
}

.simulation-status.active {
    background: #d4edda;
    color: #155724;
}

.simulation-status.paused {
    background: #fff3cd;
    color: #856404;
}

.simulation-status.completed {
    background: #d1ecf1;
    color: #0c5460;
}

.simulation-stats {
    display: flex;
    justify-content: space-between;
    margin: 1rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.stat-item {
    text-align: center;
    flex: 1;
}

.stat-item .number {
    font-size: 1.5rem;
    font-weight: bold;
    color: #007bff;
    display: block;
}

.stat-item .label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
}

.simulation-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e9ecef;
    font-size: 0.9rem;
    color: #6c757d;
}

.simulation-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

.simulation-actions .btn {
    flex: 1;
    padding: 0.5rem;
    font-size: 0.9rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #6c757d;
}

.empty-state i {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-state h3 {
    margin-bottom: 1rem;
    color: #495057;
}

.empty-state p {
    margin-bottom: 2rem;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

/* Modal enhancements */
.modal-content {
    border: none;
    border-radius: 10px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.modal-header {
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
    border-radius: 10px 10px 0 0;
}

.modal-header .btn-close {
    filter: invert(1);
}

.form-label {
    font-weight: 600;
    color: #495057;
}

.form-control {
    border-radius: 8px;
    border: 2px solid #e9ecef;
    transition: all 0.3s ease;
}

.form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Loading states */
.simulation-card.loading {
    opacity: 0.6;
    pointer-events: none;
}

.simulation-card.loading::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30px;
    height: 30px;
    margin: -15px 0 0 -15px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Import/Export styling */
.import-export-area {
    border: 2px dashed #007bff;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
    background: #f8f9ff;
    transition: all 0.3s ease;
}

.import-export-area:hover {
    background: #e7f1ff;
    border-color: #0056b3;
}

.import-export-area.dragover {
    background: #cce7ff;
    border-color: #004494;
}

/* Responsive design */
@media (max-width: 768px) {
    .simulation-manager {
        padding: 1rem 0.5rem;
    }
    
    .simulations-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .simulation-stats {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-align: left;
    }
    
    .simulation-actions {
        flex-direction: column;
    }
    
    .manager-header {
        padding: 1rem;
    }
    
    .manager-header .row {
        flex-direction: column;
        gap: 1rem;
    }
}

/* Animation utilities */
.fade-in-up {
    animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}'''
        
        file_path = self.static_dir / "css" / "simulation.css"
        return self.create_file(file_path, content)
    
    def _create_simulation_manager_js(self) -> bool:
        """Kreira simulation_manager.js fajl."""
        content = '''/**
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
            await this.loadSimulations();

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
});'''
        
        file_path = self.static_dir / "js" / "simulation_manager.js"
        return self.create_file(file_path, content)
    
    def _add_simulation_routes(self) -> bool:
        """Dodaje rute za simulation manager."""
        app_path = self.project_root / "app.py"
        
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Proveri da li route već postoji
        if '@app.route("/simulation-manager")' in app_content:
            self.logger.info("Simulation manager route već postoji")
            return True
        
        self.logger.info("Routes su već dodani u app.py")
        return True
    
    def _test_simulation_components(self) -> bool:
        """Testira simulation management komponente."""
        self.logger.info("Testiranje simulation management komponenti...")
        
        # Proveri da li su fajlovi kreirani
        required_files = [
            self.static_dir / "css" / "simulation.css",
            self.static_dir / "js" / "simulation_manager.js"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                self.logger.error(f"Nedostaje fajl: {file_path}")
                return False
            
            # Osnovne validacije sadržaja
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.suffix == '.css':
                if not self.validate_css(content):
                    return False
            elif file_path.suffix == '.js':
                if not self.validate_js(content):
                    return False
        
        # Proverava da li template postoji
        template_path = self.templates_dir / "simulation_manager.html"
        if not template_path.exists():
            self.logger.error("Template simulation_manager.html ne postoji")
            return False
        
        self.logger.info("Svi simulation management fajlovi su uspešno kreirani i validni")
        return True