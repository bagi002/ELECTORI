/**
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
});