/**
 * Support Matrix JavaScript with Slider-based UI/UX
 * Fokus na intuitivnu interakciju kroz slajdere za sve kontrole
 */

class SupportMatrixManager {
    constructor() {
        this.supportData = {};
        this.parties = [];
        this.cities = [];
        this.validationResults = {};
        this.sliderInstances = new Map();
        
        this.init();
    }
    
    async init() {
        console.log('🎯 Inicijalizacija Support Matrix Manager-a sa sliderima');
        
        // Postavke za slajdere
        this.setupSliderControls();
        
        // Event listeneri
        this.setupEventListeners();
        
        // Učitaj podatke
        await this.loadSupportMatrix();
        
        // Renderuj matricu
        this.renderMatrix();
        
        // Ažuriraj statistike
        this.updateStatistics();
    }
    
    setupSliderControls() {
        // Bulk Edit Slider
        const bulkEditSlider = document.getElementById('bulkEditSlider');
        const bulkEditValue = document.getElementById('bulkEditValue');
        
        if (bulkEditSlider) {
            bulkEditSlider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                bulkEditValue.textContent = value.toFixed(1);
                this.updateSliderBackground(bulkEditSlider, value);
            });
        }
        
        // Filter Range Sliders
        const filterRangeMin = document.getElementById('filterRangeMin');
        const filterRangeMax = document.getElementById('filterRangeMax');
        const filterRangeValue = document.getElementById('filterRangeValue');
        
        if (filterRangeMin && filterRangeMax) {
            const updateFilterRange = () => {
                const min = parseInt(filterRangeMin.value);
                const max = parseInt(filterRangeMax.value);
                
                // Osiguraj da min nije veći od max
                if (min > max) {
                    filterRangeMin.value = max;
                }
                if (max < min) {
                    filterRangeMax.value = min;
                }
                
                const finalMin = parseInt(filterRangeMin.value);
                const finalMax = parseInt(filterRangeMax.value);
                
                filterRangeValue.textContent = `${finalMin}% - ${finalMax}%`;
                this.applyFilter(finalMin, finalMax);
                
                this.updateSliderBackground(filterRangeMin, finalMin);
                this.updateSliderBackground(filterRangeMax, finalMax);
            };
            
            filterRangeMin.addEventListener('input', updateFilterRange);
            filterRangeMax.addEventListener('input', updateFilterRange);
        }
        
        // Normalization Threshold Slider
        const normalizationThreshold = document.getElementById('normalizationThreshold');
        const normalizationValue = document.getElementById('normalizationValue');
        
        if (normalizationThreshold) {
            normalizationThreshold.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                normalizationValue.textContent = value;
                this.updateSliderBackground(normalizationThreshold, value, 95, 120);
            });
        }
        
        // Bulk Edit Modal Slider
        const bulkValueSlider = document.getElementById('bulkValueSlider');
        const bulkValueDisplay = document.getElementById('bulkValueDisplay');
        
        if (bulkValueSlider) {
            bulkValueSlider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                bulkValueDisplay.textContent = value.toFixed(1);
                this.updateSliderBackground(bulkValueSlider, value);
                this.updateBulkPreview();
            });
        }
    }
    
    updateSliderBackground(slider, value, min = 0, max = 100) {
        const percentage = ((value - min) / (max - min)) * 100;
        slider.style.background = `linear-gradient(to right, var(--bs-primary) 0%, var(--bs-primary) ${percentage}%, #e9ecef ${percentage}%, #e9ecef 100%)`;
    }
    
    setupEventListeners() {
        // Validate Matrix button
        document.getElementById('validateMatrix')?.addEventListener('click', () => {
            this.validateMatrix();
        });
        
        // Normalize Matrix button
        document.getElementById('normalizeMatrix')?.addEventListener('click', () => {
            this.normalizeMatrix();
        });
        
        // Bulk Edit button
        document.getElementById('bulkEditBtn')?.addEventListener('click', () => {
            this.openBulkEditModal();
        });
        
        // Apply Bulk Edit button
        document.getElementById('applyBulkEdit')?.addEventListener('click', () => {
            this.applyBulkEdit();
        });
        
        // Display Mode select
        document.getElementById('displayMode')?.addEventListener('change', (e) => {
            this.applyDisplayMode(e.target.value);
        });
    }
    
    async loadSupportMatrix() {
        try {
            const response = await fetch('/api/support/matrix');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.supportData = data.support_matrix || {};
            this.parties = data.parties || [];
            this.cities = data.cities || [];
            
            console.log('📊 Support matrix data loaded:', data);
            
        } catch (error) {
            console.error('❌ Error loading support matrix:', error);
            this.showError('Greška pri učitavanju matrice podrške');
        }
    }
    
    renderMatrix() {
        const table = document.getElementById('supportMatrix');
        if (!table) return;
        
        const thead = table.querySelector('thead tr');
        const tbody = table.querySelector('tbody');
        const tfoot = table.querySelector('tfoot tr');
        
        // Clear existing content (except first column header)
        thead.innerHTML = '<th scope="col" class="sticky-column"><i class="fas fa-flag"></i> Partija</th>';
        tbody.innerHTML = '';
        tfoot.innerHTML = '<th scope="row" class="sticky-column"><i class="fas fa-calculator"></i> Ukupno po gradu</th>';
        
        // Add city headers
        this.cities.forEach(city => {
            const th = document.createElement('th');
            th.scope = 'col';
            th.innerHTML = `
                <div class="city-header">
                    <div class="city-name">${city.name}</div>
                    <div class="city-population">${city.population.toLocaleString()}</div>
                </div>
            `;
            thead.appendChild(th);
        });
        
        // Add party rows
        this.parties.forEach(party => {
            const tr = document.createElement('tr');
            tr.dataset.partyId = party.id;
            
            // Party name cell
            const partyCell = document.createElement('th');
            partyCell.scope = 'row';
            partyCell.className = 'sticky-column';
            partyCell.innerHTML = `
                <div class="party-header">
                    <div class="party-color" style="background-color: ${party.color}"></div>
                    <div class="party-name">${party.name}</div>
                </div>
            `;
            tr.appendChild(partyCell);
            
            // Support cells with sliders
            this.cities.forEach(city => {
                const td = document.createElement('td');
                td.className = 'support-cell';
                td.dataset.partyId = party.id;
                td.dataset.cityId = city.id;
                
                const supportData = this.supportData[party.id]?.[city.id] || { support_percentage: 0 };
                const supportValue = supportData.support_percentage || 0;
                
                td.innerHTML = `
                    <div class="support-input-container">
                        <input type="range" 
                               class="form-range support-slider" 
                               min="0" 
                               max="100" 
                               step="0.1" 
                               value="${supportValue}"
                               data-party-id="${party.id}"
                               data-city-id="${city.id}">
                        <div class="support-value">${supportValue.toFixed(1)}%</div>
                        <div class="support-status"></div>
                    </div>
                `;
                
                tr.appendChild(td);
                
                // Dodaj event listener za slider
                const slider = td.querySelector('.support-slider');
                const valueDisplay = td.querySelector('.support-value');
                
                slider.addEventListener('input', (e) => {
                    const newValue = parseFloat(e.target.value);
                    valueDisplay.textContent = `${newValue.toFixed(1)}%`;
                    this.updateSliderBackground(slider, newValue);
                    
                    // Debounced update
                    clearTimeout(slider.updateTimeout);
                    slider.updateTimeout = setTimeout(() => {
                        this.updateSupport(party.id, city.id, newValue);
                    }, 300);
                });
                
                // Initial slider background
                this.updateSliderBackground(slider, supportValue);
            });
            
            tbody.appendChild(tr);
        });
        
        // Add city totals row
        this.cities.forEach(city => {
            const td = document.createElement('td');
            td.className = 'city-total';
            td.dataset.cityId = city.id;
            
            const total = this.calculateCityTotal(city.id);
            const isValid = total <= 100;
            
            td.innerHTML = `
                <div class="total-container ${isValid ? 'valid' : 'invalid'}">
                    <div class="total-value">${total.toFixed(1)}%</div>
                    <div class="total-bar">
                        <div class="total-fill" style="width: ${Math.min(total, 100)}%"></div>
                    </div>
                    <div class="total-status">
                        <i class="fas ${isValid ? 'fa-check' : 'fa-exclamation-triangle'}"></i>
                    </div>
                </div>
            `;
            
            tfoot.appendChild(td);
        });
    }
    
    calculateCityTotal(cityId) {
        let total = 0;
        this.parties.forEach(party => {
            const support = this.supportData[party.id]?.[cityId]?.support_percentage || 0;
            total += support;
        });
        return total;
    }
    
    async updateSupport(partyId, cityId, supportPercentage) {
        try {
            const response = await fetch('/api/support/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    party_id: partyId,
                    city_id: cityId,
                    support_percentage: supportPercentage
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Update local data
            if (!this.supportData[partyId]) {
                this.supportData[partyId] = {};
            }
            this.supportData[partyId][cityId] = {
                support_percentage: supportPercentage,
                last_updated: new Date().toISOString()
            };
            
            // Update city total
            this.updateCityTotal(cityId);
            
            // Update statistics
            this.updateStatistics();
            
            // Visual feedback
            this.showSuccessToast(`Podrška ažurirana: ${supportPercentage.toFixed(1)}%`);
            
        } catch (error) {
            console.error('❌ Error updating support:', error);
            this.showError('Greška pri ažuriranju podrške');
        }
    }
    
    updateCityTotal(cityId) {
        const totalCell = document.querySelector(`[data-city-id="${cityId}"].city-total`);
        if (!totalCell) return;
        
        const total = this.calculateCityTotal(cityId);
        const isValid = total <= 100;
        
        const totalContainer = totalCell.querySelector('.total-container');
        totalContainer.className = `total-container ${isValid ? 'valid' : 'invalid'}`;
        
        totalCell.querySelector('.total-value').textContent = `${total.toFixed(1)}%`;
        totalCell.querySelector('.total-fill').style.width = `${Math.min(total, 100)}%`;
        
        const statusIcon = totalCell.querySelector('.total-status i');
        statusIcon.className = `fas ${isValid ? 'fa-check' : 'fa-exclamation-triangle'}`;
    }
    
    async validateMatrix() {
        try {
            const response = await fetch('/api/support/matrix/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    support_matrix: this.supportData
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const validation = await response.json();
            this.validationResults = validation;
            
            if (validation.valid) {
                this.showSuccessToast('Matrica je validna! ✅');
            } else {
                this.showValidationErrors(validation.errors);
            }
            
        } catch (error) {
            console.error('❌ Error validating matrix:', error);
            this.showError('Greška pri validaciji matrice');
        }
    }
    
    async normalizeMatrix() {
        const threshold = parseInt(document.getElementById('normalizationThreshold').value);
        
        try {
            const response = await fetch('/api/support/matrix/normalize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    support_matrix: this.supportData,
                    options: {
                        preserve_zero: true,
                        min_support: 0.1,
                        threshold: threshold
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Update support data
            this.supportData = result.normalized_matrix;
            
            // Re-render matrix
            this.renderMatrix();
            
            // Show normalization log
            this.showNormalizationResults(result.normalization_log);
            
        } catch (error) {
            console.error('❌ Error normalizing matrix:', error);
            this.showError('Greška pri normalizaciji matrice');
        }
    }
    
    openBulkEditModal() {
        // Populate dropdowns
        const partySelect = document.getElementById('bulkPartySelect');
        const citySelect = document.getElementById('bulkCitySelect');
        
        if (partySelect) {
            partySelect.innerHTML = '<option value="">Sve partije</option>';
            this.parties.forEach(party => {
                partySelect.innerHTML += `<option value="${party.id}">${party.name}</option>`;
            });
        }
        
        if (citySelect) {
            citySelect.innerHTML = '<option value="">Svi gradovi</option>';
            this.cities.forEach(city => {
                citySelect.innerHTML += `<option value="${city.id}">${city.name}</option>`;
            });
        }
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('bulkEditModal'));
        modal.show();
    }
    
    updateBulkPreview() {
        const partyId = document.getElementById('bulkPartySelect').value;
        const cityId = document.getElementById('bulkCitySelect').value;
        const value = parseFloat(document.getElementById('bulkValueSlider').value);
        const preserveZero = document.getElementById('bulkPreserveZero').checked;
        
        let preview = '';
        let affectedCount = 0;
        
        if (partyId && cityId) {
            preview = `Jedna ćelija: ${value.toFixed(1)}%`;
            affectedCount = 1;
        } else if (partyId) {
            const party = this.parties.find(p => p.id == partyId);
            preview = `Svi gradovi za partiju "${party.name}": ${value.toFixed(1)}%`;
            affectedCount = this.cities.length;
        } else if (cityId) {
            const city = this.cities.find(c => c.id == cityId);
            preview = `Sve partije za grad "${city.name}": ${value.toFixed(1)}%`;
            affectedCount = this.parties.length;
        } else {
            preview = `Sve ćelije: ${value.toFixed(1)}%`;
            affectedCount = this.parties.length * this.cities.length;
        }
        
        if (preserveZero) {
            preview += ' (zadržavaju se nulte vrednosti)';
        }
        
        document.getElementById('bulkPreview').innerHTML = `${preview}<br><small>Uticaće na ${affectedCount} ćelija</small>`;
    }
    
    async applyBulkEdit() {
        const partyId = document.getElementById('bulkPartySelect').value;
        const cityId = document.getElementById('bulkCitySelect').value;
        const value = parseFloat(document.getElementById('bulkValueSlider').value);
        const preserveZero = document.getElementById('bulkPreserveZero').checked;
        
        const updates = [];
        
        // Generate updates based on selection
        if (partyId && cityId) {
            updates.push({ party_id: partyId, city_id: cityId, support_percentage: value });
        } else if (partyId) {
            this.cities.forEach(city => {
                const currentValue = this.supportData[partyId]?.[city.id]?.support_percentage || 0;
                if (!preserveZero || currentValue > 0) {
                    updates.push({ party_id: partyId, city_id: city.id, support_percentage: value });
                }
            });
        } else if (cityId) {
            this.parties.forEach(party => {
                const currentValue = this.supportData[party.id]?.[cityId]?.support_percentage || 0;
                if (!preserveZero || currentValue > 0) {
                    updates.push({ party_id: party.id, city_id: cityId, support_percentage: value });
                }
            });
        } else {
            this.parties.forEach(party => {
                this.cities.forEach(city => {
                    const currentValue = this.supportData[party.id]?.[city.id]?.support_percentage || 0;
                    if (!preserveZero || currentValue > 0) {
                        updates.push({ party_id: party.id, city_id: city.id, support_percentage: value });
                    }
                });
            });
        }
        
        try {
            const response = await fetch('/api/support/bulk-update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ updates })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Reload matrix data
            await this.loadSupportMatrix();
            this.renderMatrix();
            this.updateStatistics();
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('bulkEditModal'));
            modal.hide();
            
            this.showSuccessToast(`Bulk edit završen: ${result.successful_updates} ažuriranja`);
            
        } catch (error) {
            console.error('❌ Error in bulk edit:', error);
            this.showError('Greška pri bulk edit operaciji');
        }
    }
    
    applyFilter(min, max) {
        const cells = document.querySelectorAll('.support-cell');
        cells.forEach(cell => {
            const slider = cell.querySelector('.support-slider');
            const value = parseFloat(slider.value);
            
            if (value >= min && value <= max) {
                cell.style.display = '';
                cell.classList.remove('filtered-out');
            } else {
                cell.classList.add('filtered-out');
            }
        });
    }
    
    applyDisplayMode(mode) {
        const rows = document.querySelectorAll('#supportMatrix tbody tr');
        
        rows.forEach(row => {
            const cityTotals = [];
            row.querySelectorAll('.support-cell').forEach(cell => {
                const cityId = cell.dataset.cityId;
                const total = this.calculateCityTotal(cityId);
                cityTotals.push(total);
            });
            
            let shouldShow = true;
            
            switch (mode) {
                case 'valid':
                    shouldShow = cityTotals.every(total => total <= 100);
                    break;
                case 'invalid':
                    shouldShow = cityTotals.some(total => total > 100);
                    break;
                case 'incomplete':
                    shouldShow = cityTotals.some(total => total < 90);
                    break;
            }
            
            row.style.display = shouldShow ? '' : 'none';
        });
    }
    
    updateStatistics() {
        // Calculate statistics
        let validCities = 0;
        let invalidCities = 0;
        let totalSupport = 0;
        let filledCells = 0;
        let totalCells = this.parties.length * this.cities.length;
        
        this.cities.forEach(city => {
            const total = this.calculateCityTotal(city.id);
            if (total <= 100) {
                validCities++;
            } else {
                invalidCities++;
            }
            totalSupport += total;
        });
        
        // Count filled cells
        this.parties.forEach(party => {
            this.cities.forEach(city => {
                const support = this.supportData[party.id]?.[city.id]?.support_percentage || 0;
                if (support > 0) filledCells++;
            });
        });
        
        // Update UI
        document.getElementById('validCitiesCount').textContent = validCities;
        document.getElementById('invalidCitiesCount').textContent = invalidCities;
        document.getElementById('averageSupport').textContent = `${(totalSupport / this.cities.length).toFixed(1)}%`;
        document.getElementById('completionPercentage').textContent = `${((filledCells / totalCells) * 100).toFixed(1)}%`;
    }
    
    showSuccessToast(message) {
        // Create and show toast notification
        console.log('✅ Success:', message);
        // Implementation for toast notifications can be added here
    }
    
    showError(message) {
        console.error('❌ Error:', message);
        alert(message); // Simple fallback, can be replaced with better UI
    }
    
    showValidationErrors(errors) {
        let message = 'Validacijske greške:\n';
        errors.forEach(error => {
            const city = this.cities.find(c => c.id == error.city_id);
            message += `• ${city ? city.name : error.city_id}: ${error.message}\n`;
        });
        alert(message);
    }
    
    showNormalizationResults(log) {
        let message = 'Normalizacija završena:\n';
        log.forEach(item => {
            const city = this.cities.find(c => c.id == item.city_id);
            message += `• ${city ? city.name : item.city_id}: ${item.original_total.toFixed(1)}% → 100%\n`;
        });
        alert(message);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SupportMatrixManager();
});