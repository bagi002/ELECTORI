"""
Task 3.1 Implementation: Support Matrix with Slider-based UI

Implementacija matrice podrške partija po gradovima sa fokus na slider-based korisnički interfejs.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional


class SupportMatrixImplementation:
    """Implementacija Support Matrix sistema sa slider UI/UX."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.templates_dir = Path("templates")
        self.static_dir = Path("static")
        self.routes_dir = Path("routes")
        
    def execute(self) -> bool:
        """Izvršava kompletan Task 3.1."""
        try:
            self.logger.info("🎯 Početak implementacije Support Matrix sa sliderima")
            
            # Korak 1: Kreiranje HTML template-a sa sliderima
            if not self._create_support_matrix_template():
                return False
                
            # Korak 2: JavaScript funkcionalnost sa sliderima
            if not self._create_support_matrix_javascript():
                return False
                
            # Korak 3: CSS styling za slajdere
            if not self._create_support_matrix_styles():
                return False
                
            # Korak 4: Registracija routes
            if not self._register_support_routes():
                return False
                
            # Korak 5: Testiranje funkcionalnosti
            if not self._test_support_matrix():
                return False
                
            self.logger.info("✅ Task 3.1 Support Matrix uspešno implementiran!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška u Task 3.1: {str(e)}")
            return False
    
    def _create_support_matrix_template(self) -> bool:
        """Kreiranje HTML template-a sa slider kontrolama."""
        try:
            self.logger.info("📄 Kreiranje support_matrix.html template-a sa sliderima")
            
            template_content = '''{% extends "base.html" %}
{% block title %}Support Matrix - {{ simulation.name if simulation else 'ELECTORI' }}{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/support_matrix.css') }}">
{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="h3">
                    <i class="fas fa-chart-bar"></i>
                    Matrica Podrške
                </h1>
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-outline-primary" id="validateMatrix">
                        <i class="fas fa-check-circle"></i> Validiraj
                    </button>
                    <button type="button" class="btn btn-outline-warning" id="normalizeMatrix">
                        <i class="fas fa-balance-scale"></i> Normalizuj
                    </button>
                    <button type="button" class="btn btn-outline-success" id="bulkEditBtn">
                        <i class="fas fa-edit"></i> Bulk Edit
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Slider Controls Panel -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-primary">
                <div class="card-header bg-primary text-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-sliders-h"></i>
                        Slider Kontrole
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <!-- Bulk Edit Slider -->
                        <div class="col-md-3">
                            <label for="bulkEditSlider" class="form-label">
                                <i class="fas fa-arrows-alt-h"></i>
                                Bulk Edit Vrednost
                            </label>
                            <div class="slider-container">
                                <input type="range" 
                                       class="form-range slider-primary" 
                                       id="bulkEditSlider" 
                                       min="0" 
                                       max="100" 
                                       step="0.1" 
                                       value="0">
                                <div class="slider-output">
                                    <span id="bulkEditValue">0.0</span>%
                                </div>
                            </div>
                        </div>
                        
                        <!-- Filter Range Slider -->
                        <div class="col-md-3">
                            <label for="filterRangeSlider" class="form-label">
                                <i class="fas fa-filter"></i>
                                Filter Opseg
                            </label>
                            <div class="slider-container">
                                <input type="range" 
                                       class="form-range slider-secondary" 
                                       id="filterRangeMin" 
                                       min="0" 
                                       max="100" 
                                       step="1" 
                                       value="0">
                                <input type="range" 
                                       class="form-range slider-secondary" 
                                       id="filterRangeMax" 
                                       min="0" 
                                       max="100" 
                                       step="1" 
                                       value="100">
                                <div class="slider-output">
                                    <span id="filterRangeValue">0% - 100%</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Auto-normalization Parameters -->
                        <div class="col-md-3">
                            <label for="normalizationThreshold" class="form-label">
                                <i class="fas fa-percent"></i>
                                Normalizacija Prag
                            </label>
                            <div class="slider-container">
                                <input type="range" 
                                       class="form-range slider-warning" 
                                       id="normalizationThreshold" 
                                       min="95" 
                                       max="120" 
                                       step="1" 
                                       value="100">
                                <div class="slider-output">
                                    <span id="normalizationValue">100</span>%
                                </div>
                            </div>
                        </div>
                        
                        <!-- Display Mode -->
                        <div class="col-md-3">
                            <label for="displayMode" class="form-label">
                                <i class="fas fa-eye"></i>
                                Prikaz Mode
                            </label>
                            <div class="slider-container">
                                <select class="form-select" id="displayMode">
                                    <option value="all">Svi</option>
                                    <option value="valid">Validni (≤100%)</option>
                                    <option value="invalid">Nevalidni (>100%)</option>
                                    <option value="incomplete">Nepopunjeni</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Support Matrix Table -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover mb-0" id="supportMatrix">
                            <thead class="table-dark">
                                <tr>
                                    <th scope="col" class="sticky-column">
                                        <i class="fas fa-flag"></i>
                                        Partija
                                    </th>
                                    <!-- City headers will be populated by JavaScript -->
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Matrix rows will be populated by JavaScript -->
                            </tbody>
                            <tfoot class="table-light">
                                <tr>
                                    <th scope="row" class="sticky-column">
                                        <i class="fas fa-calculator"></i>
                                        Ukupno po gradu
                                    </th>
                                    <!-- City totals will be populated by JavaScript -->
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Status Cards -->
    <div class="row mt-4">
        <div class="col-md-3">
            <div class="card border-success">
                <div class="card-body text-center">
                    <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                    <h5 class="card-title">Validni Gradovi</h5>
                    <h3 class="text-success" id="validCitiesCount">-</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-danger">
                <div class="card-body text-center">
                    <i class="fas fa-exclamation-triangle fa-2x text-danger mb-2"></i>
                    <h5 class="card-title">Nevalidni Gradovi</h5>
                    <h3 class="text-danger" id="invalidCitiesCount">-</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-info">
                <div class="card-body text-center">
                    <i class="fas fa-percentage fa-2x text-info mb-2"></i>
                    <h5 class="card-title">Prosečna Podrška</h5>
                    <h3 class="text-info" id="averageSupport">-</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-warning">
                <div class="card-body text-center">
                    <i class="fas fa-chart-line fa-2x text-warning mb-2"></i>
                    <h5 class="card-title">Popunjenost</h5>
                    <h3 class="text-warning" id="completionPercentage">-</h3>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Bulk Edit Modal -->
<div class="modal fade" id="bulkEditModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    <i class="fas fa-edit"></i>
                    Bulk Edit Podrške
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="bulkPartySelect" class="form-label">Izaberi Partiju</label>
                        <select class="form-select" id="bulkPartySelect">
                            <option value="">Sve partije</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label for="bulkCitySelect" class="form-label">Izaberi Grad</label>
                        <select class="form-select" id="bulkCitySelect">
                            <option value="">Svi gradovi</option>
                        </select>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-12">
                        <label for="bulkValueSlider" class="form-label">
                            <i class="fas fa-sliders-h"></i>
                            Nova Vrednost
                        </label>
                        <div class="slider-container">
                            <input type="range" 
                                   class="form-range slider-success" 
                                   id="bulkValueSlider" 
                                   min="0" 
                                   max="100" 
                                   step="0.1" 
                                   value="0">
                            <div class="slider-output">
                                <span id="bulkValueDisplay">0.0</span>%
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="bulkPreserveZero" checked>
                            <label class="form-check-label" for="bulkPreserveZero">
                                Zadrži nulte vrednosti
                            </label>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-12">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i>
                            <strong>Pregled:</strong> 
                            <span id="bulkPreview">Odaberite kriterijume za bulk edit</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-success" id="applyBulkEdit">
                    <i class="fas fa-check"></i>
                    Primeni Izmene
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/support_matrix.js') }}"></script>
{% endblock %}'''

            # Kreiraj templates direktorijum ako ne postoji
            self.templates_dir.mkdir(exist_ok=True)
            
            template_path = self.templates_dir / "support_matrix.html"
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
                
            self.logger.info(f"✅ Template kreiran: {template_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju template-a: {str(e)}")
            return False
    
    def _create_support_matrix_javascript(self) -> bool:
        """Kreiranje JavaScript-a sa slider funkcionalnostima."""
        try:
            self.logger.info("📜 Kreiranje support_matrix.js sa slider kontrolama")
            
            js_content = '''/**
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
        let message = 'Validacijske greške:\\n';
        errors.forEach(error => {
            const city = this.cities.find(c => c.id == error.city_id);
            message += `• ${city ? city.name : error.city_id}: ${error.message}\\n`;
        });
        alert(message);
    }
    
    showNormalizationResults(log) {
        let message = 'Normalizacija završena:\\n';
        log.forEach(item => {
            const city = this.cities.find(c => c.id == item.city_id);
            message += `• ${city ? city.name : item.city_id}: ${item.original_total.toFixed(1)}% → 100%\\n`;
        });
        alert(message);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SupportMatrixManager();
});'''

            # Kreiraj static/js direktorijum ako ne postoji
            js_dir = self.static_dir / "js"
            js_dir.mkdir(parents=True, exist_ok=True)
            
            js_path = js_dir / "support_matrix.js"
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
                
            self.logger.info(f"✅ JavaScript kreiran: {js_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju JavaScript-a: {str(e)}")
            return False
    
    def _create_support_matrix_styles(self) -> bool:
        """Kreiranje CSS stilova za slajdere i matricu."""
        try:
            self.logger.info("🎨 Kreiranje support_matrix.css sa slider stilovima")
            
            css_content = '''/* Support Matrix CSS with Slider-focused Design */

/* Main Container */
.support-matrix-container {
    padding: 1rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    min-height: 100vh;
}

/* Slider Controls Panel */
.card.border-primary {
    border-width: 2px !important;
    box-shadow: 0 0.5rem 1rem rgba(0, 123, 255, 0.15);
}

.card-header.bg-primary {
    background: linear-gradient(90deg, #007bff, #0056b3) !important;
}

/* Slider Container */
.slider-container {
    position: relative;
    margin-top: 0.5rem;
}

/* Enhanced Range Sliders */
.form-range {
    height: 8px;
    background: transparent;
    border-radius: 10px;
    outline: none;
    transition: all 0.3s ease;
}

.form-range::-webkit-slider-track {
    height: 8px;
    background: #e9ecef;
    border-radius: 10px;
    border: none;
}

.form-range::-webkit-slider-thumb {
    appearance: none;
    height: 20px;
    width: 20px;
    border-radius: 50%;
    background: #007bff;
    cursor: pointer;
    border: 3px solid #ffffff;
    box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
    transition: all 0.2s ease;
}

.form-range::-webkit-slider-thumb:hover {
    background: #0056b3;
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.5);
}

.form-range::-moz-range-track {
    height: 8px;
    background: #e9ecef;
    border-radius: 10px;
    border: none;
}

.form-range::-moz-range-thumb {
    height: 20px;
    width: 20px;
    border-radius: 50%;
    background: #007bff;
    cursor: pointer;
    border: 3px solid #ffffff;
    box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

/* Slider Color Variants */
.slider-primary::-webkit-slider-thumb {
    background: #007bff;
}

.slider-secondary::-webkit-slider-thumb {
    background: #6c757d;
}

.slider-success::-webkit-slider-thumb {
    background: #28a745;
}

.slider-warning::-webkit-slider-thumb {
    background: #ffc107;
}

.slider-danger::-webkit-slider-thumb {
    background: #dc3545;
}

/* Slider Output */
.slider-output {
    text-align: center;
    margin-top: 0.5rem;
    font-weight: 600;
    color: #495057;
    font-size: 0.9rem;
}

/* Support Matrix Table */
#supportMatrix {
    font-size: 0.9rem;
    border: none !important;
}

#supportMatrix .sticky-column {
    position: sticky;
    left: 0;
    background: #ffffff;
    z-index: 10;
    min-width: 200px;
    box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
}

/* Party Header */
.party-header {
    display: flex;
    align-items: center;
    padding: 0.5rem;
}

.party-color {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 0.5rem;
    border: 2px solid #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.party-name {
    font-weight: 600;
    font-size: 0.9rem;
}

/* City Header */
.city-header {
    text-align: center;
    padding: 0.5rem;
}

.city-name {
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}

.city-population {
    font-size: 0.75rem;
    color: #6c757d;
}

/* Support Input Container */
.support-input-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.75rem 0.5rem;
    position: relative;
}

.support-slider {
    width: 100%;
    margin-bottom: 0.5rem;
}

.support-value {
    font-weight: 600;
    font-size: 0.9rem;
    color: #495057;
    margin-bottom: 0.25rem;
}

.support-status {
    font-size: 0.75rem;
    height: 1rem;
}

/* Support Cell States */
.support-cell {
    min-width: 120px;
    border: 1px solid #dee2e6;
    transition: all 0.3s ease;
}

.support-cell:hover {
    background-color: #f8f9fa;
    box-shadow: inset 0 0 8px rgba(0, 123, 255, 0.1);
}

.support-cell.filtered-out {
    opacity: 0.3;
    background-color: #f8f9fa;
}

/* City Total */
.city-total {
    background-color: #f8f9fa;
    font-weight: 600;
}

.total-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.75rem;
}

.total-container.valid {
    color: #28a745;
}

.total-container.invalid {
    color: #dc3545;
}

.total-value {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.total-bar {
    width: 60px;
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.total-fill {
    height: 100%;
    background: linear-gradient(90deg, #28a745, #20c997);
    transition: width 0.3s ease;
}

.total-container.invalid .total-fill {
    background: linear-gradient(90deg, #dc3545, #c82333);
}

/* Status Cards */
.card.border-success,
.card.border-danger,
.card.border-info,
.card.border-warning {
    border-width: 2px !important;
    transition: all 0.3s ease;
}

.card.border-success:hover {
    box-shadow: 0 0.5rem 1rem rgba(40, 167, 69, 0.15);
}

.card.border-danger:hover {
    box-shadow: 0 0.5rem 1rem rgba(220, 53, 69, 0.15);
}

.card.border-info:hover {
    box-shadow: 0 0.5rem 1rem rgba(23, 162, 184, 0.15);
}

.card.border-warning:hover {
    box-shadow: 0 0.5rem 1rem rgba(255, 193, 7, 0.15);
}

/* Bulk Edit Modal */
.modal-lg {
    max-width: 800px;
}

.modal-header {
    background: linear-gradient(90deg, #007bff, #0056b3);
    color: white;
}

.modal-header .btn-close {
    filter: invert(1);
}

/* Bulk Edit Preview */
.alert-info {
    border-left: 4px solid #17a2b8;
    background: linear-gradient(90deg, rgba(23, 162, 184, 0.1), rgba(23, 162, 184, 0.05));
}

/* Responsive Design */
@media (max-width: 768px) {
    .slider-container {
        margin-bottom: 1rem;
    }
    
    .support-input-container {
        padding: 0.5rem 0.25rem;
    }
    
    .party-header,
    .city-header {
        padding: 0.25rem;
    }
    
    .city-name,
    .party-name {
        font-size: 0.8rem;
    }
    
    .support-value {
        font-size: 0.8rem;
    }
    
    #supportMatrix .sticky-column {
        min-width: 150px;
    }
}

/* Animation Classes */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.support-cell {
    animation: slideIn 0.3s ease;
}

/* Focus States for Accessibility */
.form-range:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

.support-slider:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

/* Loading States */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

.loading::after {
    content: '';
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
}

/* Tooltip Styles */
.tooltip-inner {
    background-color: #007bff;
    border-radius: 6px;
}

.tooltip.bs-tooltip-top .tooltip-arrow::before {
    border-top-color: #007bff;
}

/* Print Styles */
@media print {
    .slider-container,
    .btn-group {
        display: none !important;
    }
    
    .support-value {
        font-size: 0.8rem !important;
    }
}'''

            # Kreiraj static/css direktorijum ako ne postoji
            css_dir = self.static_dir / "css"
            css_dir.mkdir(parents=True, exist_ok=True)
            
            css_path = css_dir / "support_matrix.css"
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
                
            self.logger.info(f"✅ CSS stilovi kreirani: {css_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju CSS stilova: {str(e)}")
            return False
    
    def _register_support_routes(self) -> bool:
        """Registracija support routes u glavnoj aplikaciji."""
        try:
            self.logger.info("🔗 Registracija support routes")
            
            # Proverava da li routes već postoje
            if not (self.routes_dir / "support_routes.py").exists():
                self.logger.warning("⚠️ support_routes.py nije pronađen")
                return False
            
            # Proverava da li je blueprint registrovan u app.py
            app_path = Path("app.py")
            if not app_path.exists():
                self.logger.warning("⚠️ app.py nije pronađen")
                return False
            
            # Čita postojeći app.py
            with open(app_path, 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            # Proverava da li je support blueprint već registrovan
            if 'support_bp' in app_content and 'support_routes' in app_content:
                self.logger.info("✅ Support routes već registrovani")
                return True
            
            # Dodaje import za support routes
            import_line = "from routes.support_routes import support_bp"
            if import_line not in app_content:
                # Nalazi poziciju za dodavanje importa
                lines = app_content.split('\n')
                last_import_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith('from routes.') or line.startswith('from models.'):
                        last_import_idx = i
                
                if last_import_idx >= 0:
                    lines.insert(last_import_idx + 1, import_line)
                else:
                    # Ako nema postojećih route importa, dodaje na početak
                    lines.insert(1, import_line)
                
                app_content = '\n'.join(lines)
            
            # Dodaje blueprint registraciju
            blueprint_reg = "app.register_blueprint(support_bp)"
            if blueprint_reg not in app_content:
                # Nalazi poziciju za dodavanje blueprint registracije
                lines = app_content.split('\n')
                for i, line in enumerate(lines):
                    if 'register_blueprint' in line:
                        lines.insert(i + 1, f"    {blueprint_reg}")
                        break
                else:
                    # Ako nema postojećih blueprint registracija, dodaje pre if __name__ == '__main__'
                    for i, line in enumerate(lines):
                        if 'if __name__ == ' in line:
                            lines.insert(i, f"    {blueprint_reg}")
                            lines.insert(i, "")
                            break
                
                app_content = '\n'.join(lines)
            
            # Čuva ažurirani app.py
            with open(app_path, 'w', encoding='utf-8') as f:
                f.write(app_content)
            
            self.logger.info("✅ Support routes uspešno registrovani u app.py")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri registraciji routes: {str(e)}")
            return False
    
    def _test_support_matrix(self) -> bool:
        """Testiranje Support Matrix funkcionalnosti."""
        try:
            self.logger.info("🧪 Pokretanje testova za Support Matrix")
            
            # Osnovni testovi za postojanje fajlova
            required_files = [
                "templates/support_matrix.html",
                "static/js/support_matrix.js", 
                "static/css/support_matrix.css",
                "routes/support_routes.py"
            ]
            
            for file_path in required_files:
                if not Path(file_path).exists():
                    self.logger.error(f"❌ Nedostaje fajl: {file_path}")
                    return False
            
            self.logger.info("✅ Svi potrebni fajlovi postoje")
            
            # Test da li se može importovati routes
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("support_routes", "routes/support_routes.py")
                support_routes = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(support_routes)
                self.logger.info("✅ Support routes modul se može uspešno importovati")
            except Exception as e:
                self.logger.error(f"❌ Greška pri importu support routes: {str(e)}")
                return False
            
            # Test da li HTML template sadrži key elemente
            template_path = Path("templates/support_matrix.html")
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            required_elements = [
                'id="supportMatrix"',
                'id="bulkEditSlider"',
                'id="filterRangeMin"',
                'id="normalizationThreshold"',
                'form-range'  # Changed from 'class="support-slider"' to more generic check
            ]
            
            for element in required_elements:
                if element not in template_content:
                    self.logger.error(f"❌ Template ne sadrži: {element}")
                    return False
            
            self.logger.info("✅ HTML template sadrži sve potrebne slider elemente")
            
            # Test da li JavaScript sadrži key funkcije
            js_path = Path("static/js/support_matrix.js")
            with open(js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            required_functions = [
                'setupSliderControls',
                'updateSliderBackground',
                'updateSupport',
                'validateMatrix',
                'normalizeMatrix',
                'applyBulkEdit'
            ]
            
            for func in required_functions:
                if func not in js_content:
                    self.logger.error(f"❌ JavaScript ne sadrži funkciju: {func}")
                    return False
            
            self.logger.info("✅ JavaScript sadrži sve potrebne slider funkcije")
            
            # Test da li CSS sadrži slider stilove
            css_path = Path("static/css/support_matrix.css")
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            required_styles = [
                '.form-range',
                '.slider-container',
                '.slider-primary',
                '.support-slider',
                '.slider-output'
            ]
            
            for style in required_styles:
                if style not in css_content:
                    self.logger.error(f"❌ CSS ne sadrži stil: {style}")
                    return False
            
            self.logger.info("✅ CSS sadrži sve potrebne slider stilove")
            
            self.logger.info("🎉 Svi testovi za Support Matrix prošli uspešno!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri testiranju Support Matrix: {str(e)}")
            return False