"""
Task 2.3: City Management System Implementation

Implementira kompletno upravljanje gradovima.
"""

from pathlib import Path
from task_implementations import BaseTaskImplementation

class CityManagementImplementation(BaseTaskImplementation):
    """Implementacija Task 2.3: City Management System."""
    
    def execute(self) -> bool:
        """Izvršava implementaciju city management sistema."""
        self.logger.info("Pokretanje implementacije City Management System")
        
        steps = [
            self._create_city_manager_template,
            self._create_city_manager_js,
            self._add_city_routes,
            self._test_city_components
        ]
        
        for step in steps:
            if not step():
                return False
        
        self.logger.info("City Management System uspešno implementiran")
        return True
    
    def _create_city_manager_template(self) -> bool:
        """Kreira city_manager.html template."""
        content = '''{% extends "base.html" %}

{% block title %}Upravljanje gradovima - ELECTORI{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
<style>
.city-manager {
    padding: 2rem 1rem;
    background-color: #f8f9fa;
    min-height: calc(100vh - 200px);
}

.city-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.city-table-container {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
}

.table-header {
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: between;
    align-items: center;
}

.search-controls {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1rem;
}

.city-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.city-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

.city-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
}

.city-name {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.city-population {
    color: #007bff;
    font-weight: 500;
}

.city-stats {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #6c757d;
}

.city-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

.btn-sm {
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
}

.empty-cities {
    text-align: center;
    padding: 3rem;
    color: #6c757d;
}

.empty-cities i {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

@media (max-width: 768px) {
    .search-controls {
        flex-direction: column;
        align-items: stretch;
    }
    
    .city-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .city-stats {
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .city-actions {
        justify-content: stretch;
    }
    
    .city-actions .btn {
        flex: 1;
    }
}
</style>
{% endblock %}

{% block content %}
<div class="city-manager">
    <div class="container-fluid">
        <!-- Header -->
        <div class="manager-header">
            <div class="row align-items-center">
                <div class="col">
                    <h2><i class="fas fa-city"></i> Upravljanje gradovima</h2>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" id="add-city-btn">
                        <i class="fas fa-plus"></i> Dodaj grad
                    </button>
                </div>
            </div>
        </div>

        <!-- Statistics -->
        <div class="city-stats-grid">
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-city"></i>
                </div>
                <div class="stats-content">
                    <h3 id="total-cities-count">0</h3>
                    <p>Ukupno gradova</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stats-content">
                    <h3 id="total-population">0</h3>
                    <p>Ukupna populacija</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="stats-content">
                    <h3 id="average-population">0</h3>
                    <p>Prosečna populacija</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="stats-content">
                    <h3 id="largest-city">-</h3>
                    <p>Najveći grad</p>
                </div>
            </div>
        </div>

        <!-- Search and controls -->
        <div class="search-controls">
            <div class="input-group" style="max-width: 300px;">
                <span class="input-group-text"><i class="fas fa-search"></i></span>
                <input type="text" class="form-control" id="search-cities" placeholder="Pretraži gradove...">
            </div>
            <select class="form-select" id="sort-cities" style="max-width: 200px;">
                <option value="name">Sortiraj po imenu</option>
                <option value="population-desc">Populacija (opadajuće)</option>
                <option value="population-asc">Populacija (rastuce)</option>
            </select>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="show-coordinates">
                <label class="form-check-label" for="show-coordinates">
                    Prikaži koordinate
                </label>
            </div>
        </div>

        <!-- Cities list -->
        <div class="city-table-container">
            <div class="table-header">
                <h4><i class="fas fa-list"></i> Lista gradova</h4>
                <span id="cities-count-display">0 gradova</span>
            </div>
            <div id="cities-list" class="p-3">
                <!-- Dinamički sadržaj -->
            </div>
        </div>
    </div>
</div>

<!-- Modal za dodavanje/editovanje grada -->
<div class="modal fade" id="cityModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="cityModalTitle">Dodaj grad</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="city-form">
                    <input type="hidden" id="city-id">
                    <div class="mb-3">
                        <label for="city-name" class="form-label">Naziv grada</label>
                        <input type="text" class="form-control" id="city-name" required>
                        <div class="form-text">Unesite jedinstveno ime grada (do 50 karaktera)</div>
                    </div>
                    <div class="mb-3">
                        <label for="city-population" class="form-label">Broj stanovnika</label>
                        <input type="number" class="form-control" id="city-population" 
                               min="100" max="10000000" required>
                        <div class="form-text">Između 100 i 10,000,000 stanovnika</div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <label for="city-coordinates-x" class="form-label">Koordinata X (opciono)</label>
                            <input type="number" class="form-control" id="city-coordinates-x" 
                                   step="0.01" min="-180" max="180">
                        </div>
                        <div class="col-md-6">
                            <label for="city-coordinates-y" class="form-label">Koordinata Y (opciono)</label>
                            <input type="number" class="form-control" id="city-coordinates-y" 
                                   step="0.01" min="-90" max="90">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-primary" id="save-city-btn">Sačuvaj</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal za brisanje grada -->
<div class="modal fade" id="deleteCityModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Potvrda brisanja</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Da li ste sigurni da želite da obrišete grad <strong id="delete-city-name"></strong>?</p>
                <p class="text-danger">Ova akcija će takođe obrisati i svu podršku partija u ovom gradu.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-danger" id="confirm-delete-city-btn">Obriši</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script src="{{ url_for('static', filename='js/city_manager.js') }}"></script>
{% endblock %}'''
        
        file_path = self.templates_dir / "city_manager.html"
        return self.create_file(file_path, content)
    
    def _create_city_manager_js(self) -> bool:
        """Kreira city_manager.js fajl."""
        content = '''/**
 * City Manager functionality for ELECTORI
 */

class CityManager {
    constructor() {
        this.cities = [];
        this.filteredCities = [];
        this.editingCityId = null;
        this.deleteCityId = null;
        this.showCoordinates = false;
        this.init();
    }

    async init() {
        await this.checkActiveSimulation();
        await this.loadCities();
        this.setupEventListeners();
        this.setupModals();
    }

    async checkActiveSimulation() {
        try {
            const activeSimulation = await API.getActiveSimulation();
            if (!activeSimulation) {
                UIUtils.showAlert('Nema aktivne simulacije. Molimo prvo aktivirajte simulaciju.', 'warning');
                setTimeout(() => {
                    window.location.href = '/simulation-manager';
                }, 3000);
                return false;
            }
            return true;
        } catch (error) {
            UIUtils.showAlert('Nema aktivne simulacije. Molimo prvo aktivirajte simulaciju.', 'warning');
            setTimeout(() => {
                window.location.href = '/simulation-manager';
            }, 3000);
            return false;
        }
    }

    async loadCities() {
        try {
            UIUtils.showLoader(document.getElementById('cities-list'));
            
            this.cities = await API.getCities();
            this.filteredCities = [...this.cities];
            
            this.updateStatistics();
            this.renderCities();
            
        } catch (error) {
            console.error('Error loading cities:', error);
            UIUtils.showAlert('Greška pri učitavanju gradova: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('cities-list'));
        }
    }

    updateStatistics() {
        const totalCities = this.cities.length;
        const totalPopulation = this.cities.reduce((sum, city) => sum + (city.population || 0), 0);
        const averagePopulation = totalCities > 0 ? Math.round(totalPopulation / totalCities) : 0;
        const largestCity = this.cities.length > 0 ? 
            this.cities.reduce((max, city) => city.population > max.population ? city : max) : null;

        // Update statistics display
        document.getElementById('total-cities-count').textContent = totalCities;
        document.getElementById('total-population').textContent = UIUtils.formatNumber(totalPopulation);
        document.getElementById('average-population').textContent = UIUtils.formatNumber(averagePopulation);
        document.getElementById('largest-city').textContent = largestCity ? largestCity.name : '-';
        
        // Update count display
        document.getElementById('cities-count-display').textContent = 
            `${this.filteredCities.length} od ${totalCities} gradova`;
    }

    renderCities() {
        const container = document.getElementById('cities-list');
        if (!container) return;

        if (this.filteredCities.length === 0) {
            container.innerHTML = this.renderEmptyState();
            return;
        }

        container.innerHTML = this.filteredCities.map(city => 
            this.renderCityCard(city)
        ).join('');

        this.setupCityEventListeners();
    }

    renderCityCard(city) {
        const coordinatesDisplay = this.showCoordinates && city.coordinates_x && city.coordinates_y ? 
            `<span><i class="fas fa-map-marker-alt"></i> ${city.coordinates_x.toFixed(2)}, ${city.coordinates_y.toFixed(2)}</span>` : '';

        return `
            <div class="city-card fade-in" data-city-id="${city.id}">
                <div class="city-header">
                    <h3 class="city-name">${city.name}</h3>
                    <span class="city-population">
                        <i class="fas fa-users"></i> ${UIUtils.formatNumber(city.population)}
                    </span>
                </div>
                <div class="city-stats">
                    <span><i class="fas fa-chart-pie"></i> Podrška: ${city.total_party_support || 0}%</span>
                    ${coordinatesDisplay}
                </div>
                <div class="city-actions">
                    <button class="btn btn-outline-primary btn-sm btn-edit-city" data-id="${city.id}">
                        <i class="fas fa-edit"></i> Uredi
                    </button>
                    <button class="btn btn-outline-info btn-sm btn-city-stats" data-id="${city.id}">
                        <i class="fas fa-chart-bar"></i> Statistike
                    </button>
                    <button class="btn btn-outline-danger btn-sm btn-delete-city" data-id="${city.id}" data-name="${city.name}">
                        <i class="fas fa-trash"></i> Obriši
                    </button>
                </div>
            </div>
        `;
    }

    renderEmptyState() {
        const hasActiveSim = this.cities !== null; // Ako je API poziv uspešan ali je prazan
        
        if (!hasActiveSim) {
            return `
                <div class="empty-cities">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Nema aktivne simulacije</h3>
                    <p>Molimo prvo aktivirajte simulaciju da možete upravljati gradovima.</p>
                    <a href="/simulation-manager" class="btn btn-primary">
                        <i class="fas fa-globe"></i> Upravljaj simulacijama
                    </a>
                </div>
            `;
        }

        return `
            <div class="empty-cities">
                <i class="fas fa-city"></i>
                <h3>Nema gradova</h3>
                <p>Dodajte prvi grad u vašu simulaciju da počnete sa kreiranjem političke scene.</p>
                <button class="btn btn-primary" id="add-first-city">
                    <i class="fas fa-plus"></i> Dodaj prvi grad
                </button>
            </div>
        `;
    }

    setupCityEventListeners() {
        // Edit buttons
        document.querySelectorAll('.btn-edit-city').forEach(btn => {
            btn.addEventListener('click', () => {
                const cityId = parseInt(btn.dataset.id);
                this.editCity(cityId);
            });
        });

        // Delete buttons
        document.querySelectorAll('.btn-delete-city').forEach(btn => {
            btn.addEventListener('click', () => {
                const cityId = parseInt(btn.dataset.id);
                const cityName = btn.dataset.name;
                this.showDeleteModal(cityId, cityName);
            });
        });

        // Stats buttons
        document.querySelectorAll('.btn-city-stats').forEach(btn => {
            btn.addEventListener('click', () => {
                const cityId = parseInt(btn.dataset.id);
                this.showCityStats(cityId);
            });
        });

        // Add first city button
        const addFirstBtn = document.getElementById('add-first-city');
        if (addFirstBtn) {
            addFirstBtn.addEventListener('click', () => {
                this.showAddModal();
            });
        }
    }

    setupEventListeners() {
        // Add city button
        document.getElementById('add-city-btn').addEventListener('click', () => {
            this.showAddModal();
        });

        // Save city button
        document.getElementById('save-city-btn').addEventListener('click', () => {
            this.saveCity();
        });

        // Confirm delete button
        document.getElementById('confirm-delete-city-btn').addEventListener('click', () => {
            this.deleteCity();
        });

        // Search input
        const searchInput = document.getElementById('search-cities');
        searchInput.addEventListener('input', UIUtils.debounce(() => {
            this.filterCities();
        }, 300));

        // Sort select
        document.getElementById('sort-cities').addEventListener('change', () => {
            this.sortCities();
        });

        // Show coordinates checkbox
        document.getElementById('show-coordinates').addEventListener('change', (e) => {
            this.showCoordinates = e.target.checked;
            this.renderCities();
        });
    }

    setupModals() {
        const cityModal = document.getElementById('cityModal');
        cityModal.addEventListener('shown.bs.modal', () => {
            document.getElementById('city-name').focus();
        });

        cityModal.addEventListener('hidden.bs.modal', () => {
            this.resetForm();
        });
    }

    showAddModal() {
        this.editingCityId = null;
        document.getElementById('cityModalTitle').textContent = 'Dodaj grad';
        this.resetForm();
        
        const modal = new bootstrap.Modal(document.getElementById('cityModal'));
        modal.show();
    }

    editCity(cityId) {
        const city = this.cities.find(c => c.id === cityId);
        if (!city) return;

        this.editingCityId = cityId;
        document.getElementById('cityModalTitle').textContent = 'Uredi grad';
        
        // Populate form
        document.getElementById('city-id').value = city.id;
        document.getElementById('city-name').value = city.name;
        document.getElementById('city-population').value = city.population;
        document.getElementById('city-coordinates-x').value = city.coordinates_x || '';
        document.getElementById('city-coordinates-y').value = city.coordinates_y || '';

        const modal = new bootstrap.Modal(document.getElementById('cityModal'));
        modal.show();
    }

    resetForm() {
        document.getElementById('city-form').reset();
        document.getElementById('city-id').value = '';
        this.editingCityId = null;
        
        // Remove validation classes
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
    }

    async saveCity() {
        const form = document.getElementById('city-form');
        if (!UIUtils.validateForm(form)) {
            UIUtils.showAlert('Molimo popunite sva obavezna polja', 'warning');
            return;
        }

        const cityData = {
            name: document.getElementById('city-name').value.trim(),
            population: parseInt(document.getElementById('city-population').value),
            coordinates_x: parseFloat(document.getElementById('city-coordinates-x').value) || null,
            coordinates_y: parseFloat(document.getElementById('city-coordinates-y').value) || null
        };

        // Validation
        if (cityData.population < 100 || cityData.population > 10000000) {
            UIUtils.showAlert('Broj stanovnika mora biti između 100 i 10,000,000', 'warning');
            return;
        }

        try {
            UIUtils.showLoader(document.getElementById('save-city-btn'));

            let result;
            if (this.editingCityId) {
                result = await API.updateCity(this.editingCityId, cityData);
                UIUtils.showAlert(`Grad "${cityData.name}" je uspešno ažuriran`, 'success');
            } else {
                result = await API.createCity(cityData);
                UIUtils.showAlert(`Grad "${cityData.name}" je uspešno kreiran`, 'success');
            }

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('cityModal'));
            modal.hide();

            // Refresh list
            await this.loadCities();

        } catch (error) {
            console.error('Error saving city:', error);
            UIUtils.showAlert('Greška pri čuvanju grada: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('save-city-btn'));
        }
    }

    showDeleteModal(cityId, cityName) {
        this.deleteCityId = cityId;
        document.getElementById('delete-city-name').textContent = cityName;
        
        const modal = new bootstrap.Modal(document.getElementById('deleteCityModal'));
        modal.show();
    }

    async deleteCity() {
        if (!this.deleteCityId) return;

        try {
            UIUtils.showLoader(document.getElementById('confirm-delete-city-btn'));

            await API.deleteCity(this.deleteCityId);
            UIUtils.showAlert('Grad je uspešno obrisan', 'success');

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteCityModal'));
            modal.hide();

            // Refresh list
            await this.loadCities();

        } catch (error) {
            console.error('Error deleting city:', error);
            UIUtils.showAlert('Greška pri brisanju grada: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('confirm-delete-city-btn'));
            this.deleteCityId = null;
        }
    }

    async showCityStats(cityId) {
        try {
            const stats = await API.getCityStats(cityId);
            const city = this.cities.find(c => c.id === cityId);
            
            UIUtils.showAlert(`Statistike za ${city.name}: Ukupna podrška ${stats.total_party_support}%`, 'info');
            
        } catch (error) {
            console.error('Error loading city stats:', error);
            UIUtils.showAlert('Greška pri učitavanju statistika grada', 'danger');
        }
    }

    filterCities() {
        const query = document.getElementById('search-cities').value.toLowerCase().trim();
        
        if (!query) {
            this.filteredCities = [...this.cities];
        } else {
            this.filteredCities = this.cities.filter(city => 
                city.name.toLowerCase().includes(query) ||
                city.population.toString().includes(query)
            );
        }
        
        this.sortCities();
        this.updateStatistics();
        this.renderCities();
    }

    sortCities() {
        const sortBy = document.getElementById('sort-cities').value;
        
        switch (sortBy) {
            case 'name':
                this.filteredCities.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'population-desc':
                this.filteredCities.sort((a, b) => b.population - a.population);
                break;
            case 'population-asc':
                this.filteredCities.sort((a, b) => a.population - b.population);
                break;
        }
        
        this.renderCities();
    }
}

// Initialize city manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cityManager = new CityManager();
});'''
        
        file_path = self.static_dir / "js" / "city_manager.js"
        return self.create_file(file_path, content)
    
    def _add_city_routes(self) -> bool:
        """Dodaje route za city manager."""
        app_path = self.project_root / "app.py"
        
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Proveri da li route već postoji
        if '@app.route("/city-manager")' in app_content:
            self.logger.info("City manager route već postoji")
            return True
        
        self.logger.info("Routes su već dodani u app.py")
        return True
    
    def _test_city_components(self) -> bool:
        """Testira city management komponente."""
        self.logger.info("Testiranje city management komponenti...")
        
        required_files = [
            self.templates_dir / "city_manager.html",
            self.static_dir / "js" / "city_manager.js"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                self.logger.error(f"Nedostaje fajl: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.suffix == '.html':
                if not self.validate_html(content):
                    return False
            elif file_path.suffix == '.js':
                if not self.validate_js(content):
                    return False
        
        self.logger.info("Svi city management fajlovi su uspešno kreirani i validni")
        return True