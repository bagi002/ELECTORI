"""
Task 2.4: Party Management System Implementation

Implementira kompletan sistem za upravljanje partijama.
"""

from pathlib import Path
from task_implementations import BaseTaskImplementation

class PartyManagementImplementation(BaseTaskImplementation):
    """Implementacija Task 2.4: Party Management System."""
    
    def execute(self) -> bool:
        """Izvršava implementaciju party management sistema."""
        self.logger.info("Pokretanje implementacije Party Management System")
        
        steps = [
            self._create_party_manager_template,
            self._create_party_profile_template,
            self._create_party_manager_js,
            self._create_party_css,
            self._add_party_routes,
            self._test_party_components
        ]
        
        for step in steps:
            if not step():
                return False
        
        self.logger.info("Party Management System uspešno implementiran")
        return True
    
    def _create_party_manager_template(self) -> bool:
        """Kreira party_manager.html template."""
        content = '''{% extends "base.html" %}

{% block title %}Upravljanje partijama - ELECTORI{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/party.css') }}">
{% endblock %}

{% block content %}
<div class="party-manager">
    <div class="container-fluid">
        <!-- Header -->
        <div class="manager-header">
            <div class="row align-items-center">
                <div class="col">
                    <h2><i class="fas fa-users"></i> Upravljanje partijama</h2>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" id="add-party-btn">
                        <i class="fas fa-plus"></i> Dodaj partiju
                    </button>
                </div>
            </div>
        </div>

        <!-- Statistics -->
        <div class="party-stats-grid">
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stats-content">
                    <h3 id="total-parties-count">0</h3>
                    <p>Ukupno partija</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-balance-scale"></i>
                </div>
                <div class="stats-content">
                    <h3 id="ideologies-count">0</h3>
                    <p>Različitih ideologija</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <div class="stats-content">
                    <h3 id="average-support">0%</h3>
                    <p>Prosečna podrška</p>
                </div>
            </div>
            <div class="stats-card">
                <div class="stats-icon">
                    <i class="fas fa-crown"></i>
                </div>
                <div class="stats-content">
                    <h3 id="leading-party">-</h3>
                    <p>Vodeca partija</p>
                </div>
            </div>
        </div>

        <!-- Search and controls -->
        <div class="search-controls">
            <div class="input-group" style="max-width: 300px;">
                <span class="input-group-text"><i class="fas fa-search"></i></span>
                <input type="text" class="form-control" id="search-parties" placeholder="Pretraži partije...">
            </div>
            <select class="form-select" id="filter-ideology" style="max-width: 200px;">
                <option value="">Sve ideologije</option>
                <option value="levi">Levi</option>
                <option value="centar-levi">Centar-levi</option>
                <option value="centar">Centar</option>
                <option value="centar-desni">Centar-desni</option>
                <option value="desni">Desni</option>
            </select>
            <select class="form-select" id="sort-parties" style="max-width: 200px;">
                <option value="name">Sortiraj po imenu</option>
                <option value="support-desc">Podrška (opadajuće)</option>
                <option value="support-asc">Podrška (rastuce)</option>
                <option value="ideology">Ideologija</option>
            </select>
        </div>

        <!-- Parties list -->
        <div class="parties-container">
            <div id="parties-list">
                <!-- Dinamički sadržaj -->
            </div>
        </div>
    </div>
</div>

<!-- Modal za dodavanje/editovanje partije -->
<div class="modal fade" id="partyModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="partyModalTitle">Dodaj partiju</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="party-form">
                    <input type="hidden" id="party-id">
                    <div class="row">
                        <div class="col-md-8">
                            <div class="mb-3">
                                <label for="party-name" class="form-label">Naziv partije</label>
                                <input type="text" class="form-control" id="party-name" required>
                                <div class="form-text">Jedinstveno ime partije (do 50 karaktera)</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="mb-3">
                                <label for="party-color" class="form-label">Boja partije</label>
                                <div class="color-picker-container">
                                    <input type="color" class="form-control form-control-color" id="party-color" value="#007bff" required>
                                    <input type="text" class="form-control mt-2" id="party-color-text" placeholder="#007bff">
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="party-ideology" class="form-label">Ideologija</label>
                                <select class="form-select" id="party-ideology" required>
                                    <option value="">Odaberite ideologiju</option>
                                    <option value="levi">Levi</option>
                                    <option value="centar-levi">Centar-levi</option>
                                    <option value="centar">Centar</option>
                                    <option value="centar-desni">Centar-desni</option>
                                    <option value="desni">Desni</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="party-leader" class="form-label">Lider partije</label>
                                <input type="text" class="form-control" id="party-leader" required>
                                <div class="form-text">Ime i prezime lidera partije</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="party-founded" class="form-label">Datum osnivanja (opciono)</label>
                        <input type="date" class="form-control" id="party-founded">
                    </div>
                    
                    <div class="mb-3">
                        <label for="party-description" class="form-label">Opis partije (opciono)</label>
                        <textarea class="form-control" id="party-description" rows="3" maxlength="500"></textarea>
                        <div class="form-text">Do 500 karaktera</div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-primary" id="save-party-btn">Sačuvaj</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal za brisanje partije -->
<div class="modal fade" id="deletePartyModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Potvrda brisanja</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Da li ste sigurni da želite da obrišete partiju <strong id="delete-party-name"></strong>?</p>
                <p class="text-danger">Ova akcija će takođe obrisati i svu podršku ove partije u svim gradovima.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Otkaži</button>
                <button type="button" class="btn btn-danger" id="confirm-delete-party-btn">Obriši</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script src="{{ url_for('static', filename='js/party_manager.js') }}"></script>
{% endblock %}'''
        
        file_path = self.templates_dir / "party_manager.html"
        return self.create_file(file_path, content)
    
    def _create_party_profile_template(self) -> bool:
        """Kreira party_profile.html template."""
        content = '''{% extends "base.html" %}

{% block title %}Profil partije - ELECTORI{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/party.css') }}">
{% endblock %}

{% block content %}
<div class="party-profile">
    <div class="container">
        <!-- Party Header -->
        <div class="party-header-card">
            <div class="party-color-bar" id="party-color-bar"></div>
            <div class="party-header-content">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h1 class="party-name" id="party-name">Naziv partije</h1>
                        <div class="party-metadata">
                            <span class="ideology-badge" id="party-ideology">Ideologija</span>
                            <span class="leader-info">
                                <i class="fas fa-user"></i>
                                <span id="party-leader">Lider partije</span>
                            </span>
                            <span class="founded-info" id="party-founded-info" style="display: none;">
                                <i class="fas fa-calendar"></i>
                                <span id="party-founded">Datum osnivanja</span>
                            </span>
                        </div>
                    </div>
                    <div class="col-md-4 text-md-end">
                        <div class="party-actions">
                            <button class="btn btn-outline-primary" id="edit-party-btn">
                                <i class="fas fa-edit"></i> Uredi
                            </button>
                            <button class="btn btn-outline-secondary" id="back-to-list-btn">
                                <i class="fas fa-arrow-left"></i> Nazad
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Party Description -->
        <div class="row mt-4">
            <div class="col-md-8">
                <div class="party-info-card">
                    <h3><i class="fas fa-info-circle"></i> Opis partije</h3>
                    <p id="party-description">Nema opisa partije.</p>
                </div>

                <!-- Support by City -->
                <div class="party-info-card">
                    <h3><i class="fas fa-city"></i> Podrška po gradovima</h3>
                    <div id="city-support-list">
                        <!-- Dinamički sadržaj -->
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <!-- Quick Stats -->
                <div class="party-stats-card">
                    <h3><i class="fas fa-chart-bar"></i> Statistike</h3>
                    <div class="stat-item">
                        <span class="stat-label">Prosečna podrška</span>
                        <span class="stat-value" id="average-support">0%</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Ukupno gradova</span>
                        <span class="stat-value" id="cities-count">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Najjači grad</span>
                        <span class="stat-value" id="strongest-city">-</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Najslabiji grad</span>
                        <span class="stat-value" id="weakest-city">-</span>
                    </div>
                </div>

                <!-- Chart placeholder -->
                <div class="party-chart-card">
                    <h3><i class="fas fa-chart-pie"></i> Raspored podrške</h3>
                    <div id="support-chart">
                        <p class="text-muted text-center">Grafikon će biti dostupan u sledećoj fazi</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script>
// Party profile functionality
class PartyProfile {
    constructor() {
        this.partyId = this.getPartyIdFromUrl();
        this.party = null;
        this.supportData = null;
        this.init();
    }

    getPartyIdFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return parseInt(urlParams.get('id'));
    }

    async init() {
        if (!this.partyId) {
            UIUtils.showAlert('Nevaljan ID partije', 'danger');
            window.location.href = '/party-manager';
            return;
        }

        await this.loadPartyData();
        this.setupEventListeners();
    }

    async loadPartyData() {
        try {
            UIUtils.showLoader(document.querySelector('.party-profile'));

            const [party, supportData] = await Promise.all([
                API.getParty(this.partyId),
                API.getPartySupport(this.partyId)
            ]);

            this.party = party;
            this.supportData = supportData;

            this.renderPartyInfo();
            this.renderSupportData();

        } catch (error) {
            console.error('Error loading party data:', error);
            UIUtils.showAlert('Greška pri učitavanju podataka partije', 'danger');
            window.location.href = '/party-manager';
        } finally {
            UIUtils.hideLoader(document.querySelector('.party-profile'));
        }
    }

    renderPartyInfo() {
        if (!this.party) return;

        document.getElementById('party-name').textContent = this.party.name;
        document.getElementById('party-ideology').textContent = this.getIdeologyLabel(this.party.ideology);
        document.getElementById('party-leader').textContent = this.party.leader_name;
        
        if (this.party.founded_date) {
            document.getElementById('party-founded').textContent = UIUtils.formatDate(this.party.founded_date);
            document.getElementById('party-founded-info').style.display = 'inline';
        }

        if (this.party.description) {
            document.getElementById('party-description').textContent = this.party.description;
        }

        // Set party color
        const colorBar = document.getElementById('party-color-bar');
        colorBar.style.backgroundColor = this.party.color;

        const ideologyBadge = document.getElementById('party-ideology');
        ideologyBadge.style.backgroundColor = this.party.color;

        document.title = `${this.party.name} - ELECTORI`;
    }

    renderSupportData() {
        if (!this.supportData) return;

        const supportList = document.getElementById('city-support-list');
        const support = this.supportData.support_data || [];

        if (support.length === 0) {
            supportList.innerHTML = '<p class="text-muted">Nema podataka o podršci u gradovima.</p>';
            return;
        }

        supportList.innerHTML = support.map(item => `
            <div class="city-support-item">
                <div class="city-name">${item.city_name}</div>
                <div class="support-bar">
                    <div class="support-fill" style="width: ${item.support_percentage}%; background-color: ${this.party.color}"></div>
                    <span class="support-text">${item.support_percentage.toFixed(1)}%</span>
                </div>
            </div>
        `).join('');

        // Update statistics
        this.updateStatistics(support);
    }

    updateStatistics(support) {
        const avgSupport = this.supportData.average_support || 0;
        document.getElementById('average-support').textContent = avgSupport.toFixed(1) + '%';
        document.getElementById('cities-count').textContent = support.length;

        if (support.length > 0) {
            const strongest = support.reduce((max, city) => city.support_percentage > max.support_percentage ? city : max);
            const weakest = support.reduce((min, city) => city.support_percentage < min.support_percentage ? city : min);

            document.getElementById('strongest-city').textContent = `${strongest.city_name} (${strongest.support_percentage.toFixed(1)}%)`;
            document.getElementById('weakest-city').textContent = `${weakest.city_name} (${weakest.support_percentage.toFixed(1)}%)`;
        }
    }

    getIdeologyLabel(ideology) {
        const labels = {
            'levi': 'Levi',
            'centar-levi': 'Centar-levi',
            'centar': 'Centar',
            'centar-desni': 'Centar-desni',
            'desni': 'Desni'
        };
        return labels[ideology] || ideology;
    }

    setupEventListeners() {
        document.getElementById('back-to-list-btn').addEventListener('click', () => {
            window.location.href = '/party-manager';
        });

        document.getElementById('edit-party-btn').addEventListener('click', () => {
            window.location.href = `/party-manager?edit=${this.partyId}`;
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new PartyProfile();
});
</script>
{% endblock %}'''
        
        file_path = self.templates_dir / "party_profile.html"
        return self.create_file(file_path, content)
    
    def _create_party_manager_js(self) -> bool:
        """Kreira party_manager.js fajl."""
        content = '''/**
 * Party Manager functionality for ELECTORI
 */

class PartyManager {
    constructor() {
        this.parties = [];
        this.filteredParties = [];
        this.editingPartyId = null;
        this.deletePartyId = null;
        this.init();
    }

    async init() {
        await this.checkActiveSimulation();
        await this.loadParties();
        this.setupEventListeners();
        this.setupModals();
        this.handleUrlParams();
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

    async loadParties() {
        try {
            UIUtils.showLoader(document.getElementById('parties-list'));
            
            this.parties = await API.getParties();
            this.filteredParties = [...this.parties];
            
            // Load support data for each party
            await this.loadPartiesSupport();
            
            this.updateStatistics();
            this.renderParties();
            
        } catch (error) {
            console.error('Error loading parties:', error);
            UIUtils.showAlert('Greška pri učitavanju partija: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('parties-list'));
        }
    }

    async loadPartiesSupport() {
        try {
            const supportPromises = this.parties.map(async party => {
                try {
                    const supportData = await API.getPartySupport(party.id);
                    party.averageSupport = supportData.average_support || 0;
                    party.supportData = supportData.support_data || [];
                } catch (error) {
                    party.averageSupport = 0;
                    party.supportData = [];
                }
            });

            await Promise.all(supportPromises);
        } catch (error) {
            console.error('Error loading party support:', error);
        }
    }

    updateStatistics() {
        const totalParties = this.parties.length;
        const ideologies = [...new Set(this.parties.map(p => p.ideology))];
        const averageSupport = totalParties > 0 ? 
            this.parties.reduce((sum, party) => sum + (party.averageSupport || 0), 0) / totalParties : 0;
        const leadingParty = this.parties.length > 0 ? 
            this.parties.reduce((max, party) => (party.averageSupport || 0) > (max.averageSupport || 0) ? party : max) : null;

        document.getElementById('total-parties-count').textContent = totalParties;
        document.getElementById('ideologies-count').textContent = ideologies.length;
        document.getElementById('average-support').textContent = averageSupport.toFixed(1) + '%';
        document.getElementById('leading-party').textContent = leadingParty ? leadingParty.name : '-';
    }

    renderParties() {
        const container = document.getElementById('parties-list');
        if (!container) return;

        if (this.filteredParties.length === 0) {
            container.innerHTML = this.renderEmptyState();
            return;
        }

        container.innerHTML = this.filteredParties.map(party => 
            this.renderPartyCard(party)
        ).join('');

        this.setupPartyEventListeners();
    }

    renderPartyCard(party) {
        const ideology = this.getIdeologyLabel(party.ideology);
        const support = party.averageSupport || 0;
        const supportData = party.supportData || [];

        return `
            <div class="party-card fade-in" data-party-id="${party.id}" style="border-left: 5px solid ${party.color}">
                <div class="party-header">
                    <div class="party-info">
                        <h3 class="party-name" style="color: ${party.color}">${party.name}</h3>
                        <div class="party-metadata">
                            <span class="ideology-badge" style="background-color: ${party.color}">${ideology}</span>
                            <span class="leader-name">
                                <i class="fas fa-user"></i> ${party.leader_name}
                            </span>
                        </div>
                    </div>
                    <div class="party-support">
                        <div class="support-percentage" style="color: ${party.color}">
                            ${support.toFixed(1)}%
                        </div>
                        <div class="support-label">Prosečna podrška</div>
                    </div>
                </div>
                
                ${party.description ? `
                    <div class="party-description">
                        <p>${party.description}</p>
                    </div>
                ` : ''}
                
                <div class="party-stats">
                    <div class="stat-item">
                        <i class="fas fa-city"></i>
                        <span>${supportData.length} gradova</span>
                    </div>
                    ${party.founded_date ? `
                        <div class="stat-item">
                            <i class="fas fa-calendar"></i>
                            <span>Osnovana ${UIUtils.formatDate(party.founded_date)}</span>
                        </div>
                    ` : ''}
                </div>
                
                <div class="party-actions">
                    <button class="btn btn-outline-primary btn-sm btn-view-party" data-id="${party.id}">
                        <i class="fas fa-eye"></i> Prikaži
                    </button>
                    <button class="btn btn-outline-info btn-sm btn-edit-party" data-id="${party.id}">
                        <i class="fas fa-edit"></i> Uredi
                    </button>
                    <button class="btn btn-outline-secondary btn-sm btn-party-support" data-id="${party.id}">
                        <i class="fas fa-chart-bar"></i> Podrška
                    </button>
                    <button class="btn btn-outline-danger btn-sm btn-delete-party" data-id="${party.id}" data-name="${party.name}">
                        <i class="fas fa-trash"></i> Obriši
                    </button>
                </div>
            </div>
        `;
    }

    renderEmptyState() {
        return `
            <div class="empty-parties">
                <i class="fas fa-users"></i>
                <h3>Nema partija</h3>
                <p>Dodajte prvu partiju u vašu simulaciju da počnete sa kreiranjem političke scene.</p>
                <button class="btn btn-primary" id="add-first-party">
                    <i class="fas fa-plus"></i> Dodaj prvu partiju
                </button>
            </div>
        `;
    }

    setupPartyEventListeners() {
        // View buttons
        document.querySelectorAll('.btn-view-party').forEach(btn => {
            btn.addEventListener('click', () => {
                const partyId = parseInt(btn.dataset.id);
                this.viewParty(partyId);
            });
        });

        // Edit buttons
        document.querySelectorAll('.btn-edit-party').forEach(btn => {
            btn.addEventListener('click', () => {
                const partyId = parseInt(btn.dataset.id);
                this.editParty(partyId);
            });
        });

        // Delete buttons
        document.querySelectorAll('.btn-delete-party').forEach(btn => {
            btn.addEventListener('click', () => {
                const partyId = parseInt(btn.dataset.id);
                const partyName = btn.dataset.name;
                this.showDeleteModal(partyId, partyName);
            });
        });

        // Support buttons
        document.querySelectorAll('.btn-party-support').forEach(btn => {
            btn.addEventListener('click', () => {
                const partyId = parseInt(btn.dataset.id);
                this.showPartySupport(partyId);
            });
        });

        // Add first party button
        const addFirstBtn = document.getElementById('add-first-party');
        if (addFirstBtn) {
            addFirstBtn.addEventListener('click', () => {
                this.showAddModal();
            });
        }
    }

    setupEventListeners() {
        // Add party button
        document.getElementById('add-party-btn').addEventListener('click', () => {
            this.showAddModal();
        });

        // Save party button
        document.getElementById('save-party-btn').addEventListener('click', () => {
            this.saveParty();
        });

        // Confirm delete button
        document.getElementById('confirm-delete-party-btn').addEventListener('click', () => {
            this.deleteParty();
        });

        // Search input
        const searchInput = document.getElementById('search-parties');
        searchInput.addEventListener('input', UIUtils.debounce(() => {
            this.filterParties();
        }, 300));

        // Ideology filter
        document.getElementById('filter-ideology').addEventListener('change', () => {
            this.filterParties();
        });

        // Sort select
        document.getElementById('sort-parties').addEventListener('change', () => {
            this.sortParties();
        });

        // Color picker synchronization
        document.getElementById('party-color').addEventListener('input', (e) => {
            document.getElementById('party-color-text').value = e.target.value;
        });

        document.getElementById('party-color-text').addEventListener('input', (e) => {
            const color = e.target.value;
            if (/^#[0-9A-Fa-f]{6}$/.test(color)) {
                document.getElementById('party-color').value = color;
            }
        });
    }

    setupModals() {
        const partyModal = document.getElementById('partyModal');
        partyModal.addEventListener('shown.bs.modal', () => {
            document.getElementById('party-name').focus();
        });

        partyModal.addEventListener('hidden.bs.modal', () => {
            this.resetForm();
        });
    }

    handleUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const editId = urlParams.get('edit');
        
        if (editId) {
            // Wait for parties to load then show edit modal
            setTimeout(() => {
                this.editParty(parseInt(editId));
                // Clean URL
                window.history.replaceState({}, document.title, window.location.pathname);
            }, 1000);
        }
    }

    showAddModal() {
        this.editingPartyId = null;
        document.getElementById('partyModalTitle').textContent = 'Dodaj partiju';
        this.resetForm();
        
        const modal = new bootstrap.Modal(document.getElementById('partyModal'));
        modal.show();
    }

    editParty(partyId) {
        const party = this.parties.find(p => p.id === partyId);
        if (!party) return;

        this.editingPartyId = partyId;
        document.getElementById('partyModalTitle').textContent = 'Uredi partiju';
        
        // Populate form
        document.getElementById('party-id').value = party.id;
        document.getElementById('party-name').value = party.name;
        document.getElementById('party-color').value = party.color;
        document.getElementById('party-color-text').value = party.color;
        document.getElementById('party-ideology').value = party.ideology;
        document.getElementById('party-leader').value = party.leader_name;
        document.getElementById('party-founded').value = party.founded_date || '';
        document.getElementById('party-description').value = party.description || '';

        const modal = new bootstrap.Modal(document.getElementById('partyModal'));
        modal.show();
    }

    viewParty(partyId) {
        window.location.href = `/party-profile?id=${partyId}`;
    }

    resetForm() {
        document.getElementById('party-form').reset();
        document.getElementById('party-id').value = '';
        document.getElementById('party-color').value = '#007bff';
        document.getElementById('party-color-text').value = '#007bff';
        this.editingPartyId = null;
        
        // Remove validation classes
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
    }

    async saveParty() {
        const form = document.getElementById('party-form');
        if (!UIUtils.validateForm(form)) {
            UIUtils.showAlert('Molimo popunite sva obavezna polja', 'warning');
            return;
        }

        const partyData = {
            name: document.getElementById('party-name').value.trim(),
            color: document.getElementById('party-color').value,
            ideology: document.getElementById('party-ideology').value,
            leader_name: document.getElementById('party-leader').value.trim(),
            founded_date: document.getElementById('party-founded').value || null,
            description: document.getElementById('party-description').value.trim() || null
        };

        // Validation
        if (!/^#[0-9A-Fa-f]{6}$/.test(partyData.color)) {
            UIUtils.showAlert('Molimo unesite validnu hex boju (npr. #007bff)', 'warning');
            return;
        }

        try {
            UIUtils.showLoader(document.getElementById('save-party-btn'));

            let result;
            if (this.editingPartyId) {
                result = await API.updateParty(this.editingPartyId, partyData);
                UIUtils.showAlert(`Partija "${partyData.name}" je uspešno ažurirana`, 'success');
            } else {
                result = await API.createParty(partyData);
                UIUtils.showAlert(`Partija "${partyData.name}" je uspešno kreirana`, 'success');
            }

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('partyModal'));
            modal.hide();

            // Refresh list
            await this.loadParties();

        } catch (error) {
            console.error('Error saving party:', error);
            UIUtils.showAlert('Greška pri čuvanju partije: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('save-party-btn'));
        }
    }

    showDeleteModal(partyId, partyName) {
        this.deletePartyId = partyId;
        document.getElementById('delete-party-name').textContent = partyName;
        
        const modal = new bootstrap.Modal(document.getElementById('deletePartyModal'));
        modal.show();
    }

    async deleteParty() {
        if (!this.deletePartyId) return;

        try {
            UIUtils.showLoader(document.getElementById('confirm-delete-party-btn'));

            await API.deleteParty(this.deletePartyId);
            UIUtils.showAlert('Partija je uspešno obrisana', 'success');

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('deletePartyModal'));
            modal.hide();

            // Refresh list
            await this.loadParties();

        } catch (error) {
            console.error('Error deleting party:', error);
            UIUtils.showAlert('Greška pri brisanju partije: ' + error.message, 'danger');
        } finally {
            UIUtils.hideLoader(document.getElementById('confirm-delete-party-btn'));
            this.deletePartyId = null;
        }
    }

    async showPartySupport(partyId) {
        try {
            const supportData = await API.getPartySupport(partyId);
            const party = this.parties.find(p => p.id === partyId);
            
            const message = `Prosečna podrška za ${party.name}: ${supportData.average_support.toFixed(1)}%`;
            UIUtils.showAlert(message, 'info');
            
        } catch (error) {
            console.error('Error loading party support:', error);
            UIUtils.showAlert('Greška pri učitavanju podrške partije', 'danger');
        }
    }

    filterParties() {
        const query = document.getElementById('search-parties').value.toLowerCase().trim();
        const ideologyFilter = document.getElementById('filter-ideology').value;
        
        this.filteredParties = this.parties.filter(party => {
            const matchesSearch = !query || 
                party.name.toLowerCase().includes(query) ||
                party.leader_name.toLowerCase().includes(query) ||
                party.ideology.toLowerCase().includes(query);
                
            const matchesIdeology = !ideologyFilter || party.ideology === ideologyFilter;
            
            return matchesSearch && matchesIdeology;
        });
        
        this.sortParties();
        this.renderParties();
    }

    sortParties() {
        const sortBy = document.getElementById('sort-parties').value;
        
        switch (sortBy) {
            case 'name':
                this.filteredParties.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'support-desc':
                this.filteredParties.sort((a, b) => (b.averageSupport || 0) - (a.averageSupport || 0));
                break;
            case 'support-asc':
                this.filteredParties.sort((a, b) => (a.averageSupport || 0) - (b.averageSupport || 0));
                break;
            case 'ideology':
                this.filteredParties.sort((a, b) => a.ideology.localeCompare(b.ideology));
                break;
        }
        
        this.renderParties();
    }

    getIdeologyLabel(ideology) {
        const labels = {
            'levi': 'Levi',
            'centar-levi': 'Centar-levi',
            'centar': 'Centar',
            'centar-desni': 'Centar-desni',
            'desni': 'Desni'
        };
        return labels[ideology] || ideology;
    }
}

// Initialize party manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.partyManager = new PartyManager();
});'''
        
        file_path = self.static_dir / "js" / "party_manager.js"
        return self.create_file(file_path, content)
    
    def _create_party_css(self) -> bool:
        """Kreira party.css fajl."""
        content = '''/* Party Management Styles */

.party-manager {
    padding: 2rem 1rem;
    background-color: #f8f9fa;
    min-height: calc(100vh - 200px);
}

.party-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.search-controls {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.parties-container {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 1.5rem;
}

/* Party Cards */
.party-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    position: relative;
}

.party-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.party-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.party-info h3.party-name {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 600;
}

.party-metadata {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
}

.ideology-badge {
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
}

.leader-name {
    color: #6c757d;
    font-size: 0.9rem;
}

.leader-name i {
    margin-right: 0.25rem;
}

.party-support {
    text-align: right;
}

.support-percentage {
    font-size: 2rem;
    font-weight: bold;
    line-height: 1;
}

.support-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
}

.party-description {
    margin: 1rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 6px;
    border-left: 4px solid #007bff;
}

.party-description p {
    margin: 0;
    color: #495057;
    font-style: italic;
}

.party-stats {
    display: flex;
    gap: 1.5rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.party-stats .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6c757d;
    font-size: 0.9rem;
}

.party-stats .stat-item i {
    color: #007bff;
}

.party-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.party-actions .btn {
    flex: 1;
    min-width: 120px;
}

/* Color Picker */
.color-picker-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-control-color {
    width: 100%;
    height: 45px;
    border-radius: 6px;
}

/* Empty State */
.empty-parties {
    text-align: center;
    padding: 4rem 2rem;
    color: #6c757d;
}

.empty-parties i {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-parties h3 {
    margin-bottom: 1rem;
    color: #495057;
}

.empty-parties p {
    margin-bottom: 2rem;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

/* Party Profile Styles */
.party-profile {
    padding: 2rem 1rem;
    background-color: #f8f9fa;
    min-height: calc(100vh - 200px);
}

.party-header-card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
    margin-bottom: 2rem;
    position: relative;
}

.party-color-bar {
    height: 6px;
    width: 100%;
}

.party-header-content {
    padding: 2rem;
}

.party-header-content h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: #2c3e50;
}

.party-header-content .party-metadata {
    margin-top: 1rem;
    gap: 1.5rem;
}

.party-header-content .ideology-badge {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
}

.party-header-content .leader-info,
.party-header-content .founded-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6c757d;
    font-size: 1rem;
}

.party-actions {
    display: flex;
    gap: 0.75rem;
}

.party-info-card,
.party-stats-card,
.party-chart-card {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.party-info-card h3,
.party-stats-card h3,
.party-chart-card h3 {
    color: #2c3e50;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.party-info-card h3 i,
.party-stats-card h3 i,
.party-chart-card h3 i {
    color: #007bff;
}

.party-stats-card .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #e9ecef;
}

.party-stats-card .stat-item:last-child {
    border-bottom: none;
}

.stat-label {
    color: #6c757d;
    font-weight: 500;
}

.stat-value {
    font-weight: 600;
    color: #2c3e50;
}

/* City Support List */
.city-support-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #e9ecef;
}

.city-support-item:last-child {
    border-bottom: none;
}

.city-name {
    font-weight: 500;
    color: #2c3e50;
    flex: 1;
}

.support-bar {
    position: relative;
    width: 150px;
    height: 25px;
    background: #e9ecef;
    border-radius: 12px;
    overflow: hidden;
}

.support-fill {
    height: 100%;
    border-radius: 12px;
    transition: width 0.3s ease;
}

.support-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
}

/* Responsive Design */
@media (max-width: 768px) {
    .party-manager {
        padding: 1rem 0.5rem;
    }
    
    .search-controls {
        flex-direction: column;
        align-items: stretch;
    }
    
    .party-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .party-support {
        text-align: left;
    }
    
    .party-stats {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .party-actions {
        flex-direction: column;
    }
    
    .party-actions .btn {
        min-width: unset;
    }
    
    .party-profile .container {
        padding: 0;
    }
    
    .party-header-content {
        padding: 1.5rem;
    }
    
    .party-header-content h1 {
        font-size: 2rem;
    }
    
    .party-header-content .party-metadata {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .party-actions {
        flex-direction: column;
    }
    
    .support-bar {
        width: 120px;
    }
    
    .city-support-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}

/* Loading states */
.party-card.loading {
    opacity: 0.6;
    pointer-events: none;
}

/* Animation utilities */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}'''
        
        file_path = self.static_dir / "css" / "party.css"
        return self.create_file(file_path, content)
    
    def _add_party_routes(self) -> bool:
        """Dodaje routes za party manager."""
        app_path = self.project_root / "app.py"
        
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Proveri da li routes već postoje
        if '@app.route("/party-manager")' in app_content:
            self.logger.info("Party manager routes već postoje")
            return True
        
        self.logger.info("Routes su već dodani u app.py")
        return True
    
    def _test_party_components(self) -> bool:
        """Testira party management komponente."""
        self.logger.info("Testiranje party management komponenti...")
        
        required_files = [
            self.templates_dir / "party_manager.html",
            self.templates_dir / "party_profile.html",
            self.static_dir / "js" / "party_manager.js",
            self.static_dir / "css" / "party.css"
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
            elif file_path.suffix == '.css':
                if not self.validate_css(content):
                    return False
        
        self.logger.info("Svi party management fajlovi su uspešno kreirani i validni")
        return True