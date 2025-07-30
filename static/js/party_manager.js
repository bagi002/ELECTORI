/**
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
});