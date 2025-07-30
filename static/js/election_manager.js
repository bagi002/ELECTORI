/**
 * Election Manager JavaScript
 * Handles UI interactions for election management
 */

class ElectionManager {
    constructor() {
        this.elections = [];
        this.currentElection = null;
        this.availableParties = [];
        this.selectedParties = [];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadElections();
        this.setupFormValidation();
        this.initializeTooltips();
    }
    
    bindEvents() {
        // Create election buttons
        document.getElementById('create-election-btn')?.addEventListener('click', () => {
            this.showCreateElectionModal();
        });
        
        document.getElementById('create-first-election-btn')?.addEventListener('click', () => {
            this.showCreateElectionModal();
        });
        
        // Refresh button
        document.getElementById('refresh-elections-btn')?.addEventListener('click', () => {
            this.loadElections();
        });
        
        // Form submissions
        document.getElementById('createElectionForm')?.addEventListener('submit', (e) => {
            this.handleCreateElection(e);
        });
        
        document.getElementById('candidacyForm')?.addEventListener('submit', (e) => {
            this.handleCreateCandidacy(e);
        });
        
        // Election type change
        document.getElementById('electionType')?.addEventListener('change', (e) => {
            this.handleElectionTypeChange(e.target.value);
        });
        
        // Candidacy type change
        document.getElementById('candidacyType')?.addEventListener('change', (e) => {
            this.handleCandidacyTypeChange(e.target.value);
        });
        
        // Delete confirmation
        document.getElementById('confirm-delete-election')?.addEventListener('click', () => {
            this.confirmDeleteElection();
        });
        
        // Manage candidacies button
        document.getElementById('manage-candidacies-btn')?.addEventListener('click', () => {
            this.showCandidacyModal();
        });
    }
    
    setupFormValidation() {
        // Custom validation for forms
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }
    
    initializeTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    async loadElections() {
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/elections/');
            if (!response.ok) {
                throw new Error('Greška pri učitavanju izbora');
            }
            
            const data = await response.json();
            this.elections = data.elections || [];
            this.renderElections();
            
        } catch (error) {
            console.error('Error loading elections:', error);
            this.showToast('Greška', 'Nije moguće učitati izbore', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    renderElections() {
        const container = document.getElementById('elections-grid');
        const emptyState = document.getElementById('empty-state');
        
        if (!this.elections || this.elections.length === 0) {
            container.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }
        
        container.style.display = 'grid';
        emptyState.style.display = 'none';
        
        container.innerHTML = this.elections.map(election => this.createElectionCard(election)).join('');
        
        // Add event listeners to action buttons
        this.bindElectionActions();
    }
    
    createElectionCard(election) {
        const typeClass = `election-type-${election.type}`;
        const statusClass = `status-${election.status}`;
        const typeLabel = this.getElectionTypeLabel(election.type);
        const statusLabel = this.getElectionStatusLabel(election.status);
        const formattedDate = this.formatDate(election.election_date);
        
        return `
            <div class="election-card fade-in" data-election-id="${election.id}">
                <div class="election-card-header">
                    <h3 class="election-title">
                        ${this.getElectionIcon(election.type)}
                        ${election.name}
                    </h3>
                    <span class="election-type-badge ${typeClass}">${typeLabel}</span>
                </div>
                <div class="election-card-body">
                    <div class="election-meta">
                        <div class="meta-item">
                            <span class="meta-label">Datum</span>
                            <span class="meta-value">
                                <i class="fas fa-calendar"></i>
                                ${formattedDate}
                            </span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Status</span>
                            <span class="meta-value">
                                <span class="status-indicator ${statusClass}">${statusLabel}</span>
                            </span>
                        </div>
                        ${election.type !== 'presidential' ? `
                        <div class="meta-item">
                            <span class="meta-label">Cenzus</span>
                            <span class="meta-value">
                                <i class="fas fa-percentage"></i>
                                ${election.census_threshold || 0}%
                            </span>
                        </div>
                        ` : `
                        <div class="meta-item">
                            <span class="meta-label">Krug</span>
                            <span class="meta-value">
                                <i class="fas fa-circle-notch"></i>
                                ${election.round_number}. krug
                            </span>
                        </div>
                        `}
                    </div>
                    
                    <div class="candidacies-count">
                        <div class="candidacies-label">Kandidature</div>
                        <div class="candidacies-value" id="candidacies-count-${election.id}">
                            <i class="fas fa-users"></i>
                            Učitavanje...
                        </div>
                    </div>
                    
                    <div class="election-actions">
                        <button class="btn btn-outline-primary btn-sm" onclick="electionManager.viewElectionDetails(${election.id})">
                            <i class="fas fa-eye"></i>
                            Detalji
                        </button>
                        <button class="btn btn-outline-success btn-sm" onclick="electionManager.manageCandidacies(${election.id})">
                            <i class="fas fa-users"></i>
                            Kandidature
                        </button>
                        ${election.status === 'scheduled' ? `
                        <button class="btn btn-outline-warning btn-sm" onclick="electionManager.editElection(${election.id})">
                            <i class="fas fa-edit"></i>
                            Uredi
                        </button>
                        ` : ''}
                        <button class="btn btn-outline-danger btn-sm" onclick="electionManager.deleteElection(${election.id}, '${election.name}')">
                            <i class="fas fa-trash"></i>
                            Obriši
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    async loadCandidaciesCount(electionId) {
        try {
            const response = await fetch(`/api/elections/${electionId}/candidacies`);
            if (response.ok) {
                const data = await response.json();
                const countElement = document.getElementById(`candidacies-count-${electionId}`);
                if (countElement) {
                    countElement.innerHTML = `
                        <i class="fas fa-users"></i>
                        ${data.total} kandidatura
                    `;
                }
            }
        } catch (error) {
            console.error('Error loading candidacies count:', error);
        }
    }
    
    bindElectionActions() {
        // Load candidacies count for each election
        this.elections.forEach(election => {
            this.loadCandidaciesCount(election.id);
        });
    }
    
    showCreateElectionModal() {
        // Reset form
        document.getElementById('createElectionForm').reset();
        document.getElementById('createElectionForm').classList.remove('was-validated');
        
        // Set default date to tomorrow
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        document.getElementById('electionDate').value = tomorrow.toISOString().split('T')[0];
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('createElectionModal'));
        modal.show();
    }
    
    handleElectionTypeChange(type) {
        const censusGroup = document.getElementById('censusThresholdGroup');
        const roundGroup = document.getElementById('roundNumberGroup');
        
        if (type === 'presidential') {
            censusGroup.style.display = 'none';
            roundGroup.style.display = 'block';
            document.getElementById('censusThreshold').value = 0;
        } else {
            censusGroup.style.display = 'block';
            roundGroup.style.display = 'none';
            document.getElementById('roundNumber').value = 1;
        }
    }
    
    async handleCreateElection(e) {
        e.preventDefault();
        
        const form = e.target;
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }
        
        try {
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                type: formData.get('type'),
                election_date: formData.get('election_date'),
                census_threshold: parseFloat(formData.get('census_threshold') || 0),
                round_number: parseInt(formData.get('round_number') || 1)
            };
            
            const response = await fetch('/api/elections/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Greška pri kreiranju izbora');
            }
            
            const election = await response.json();
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('createElectionModal')).hide();
            
            // Refresh elections list
            await this.loadElections();
            
            this.showToast('Uspeh', 'Izbori su uspešno kreirani', 'success');
            
        } catch (error) {
            console.error('Error creating election:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    async viewElectionDetails(electionId) {
        try {
            const response = await fetch(`/api/elections/${electionId}`);
            if (!response.ok) {
                throw new Error('Greška pri učitavanju detalja izbora');
            }
            
            const election = await response.json();
            this.currentElection = election;
            
            const content = this.createElectionDetailsContent(election);
            document.getElementById('electionDetailsContent').innerHTML = content;
            
            const modal = new bootstrap.Modal(document.getElementById('electionDetailsModal'));
            modal.show();
            
        } catch (error) {
            console.error('Error loading election details:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    createElectionDetailsContent(election) {
        const typeLabel = this.getElectionTypeLabel(election.type);
        const statusLabel = this.getElectionStatusLabel(election.status);
        const formattedDate = this.formatDate(election.election_date);
        
        return `
            <div class="election-details">
                <div class="row">
                    <div class="col-md-6">
                        <h6>Osnovne informacije</h6>
                        <table class="table table-borderless">
                            <tr>
                                <td><strong>Naziv:</strong></td>
                                <td>${election.name}</td>
                            </tr>
                            <tr>
                                <td><strong>Tip:</strong></td>
                                <td>${typeLabel}</td>
                            </tr>
                            <tr>
                                <td><strong>Datum:</strong></td>
                                <td>${formattedDate}</td>
                            </tr>
                            <tr>
                                <td><strong>Status:</strong></td>
                                <td><span class="status-indicator status-${election.status}">${statusLabel}</span></td>
                            </tr>
                            ${election.type !== 'presidential' ? `
                            <tr>
                                <td><strong>Cenzus:</strong></td>
                                <td>${election.census_threshold || 0}%</td>
                            </tr>
                            ` : `
                            <tr>
                                <td><strong>Krug:</strong></td>
                                <td>${election.round_number}. krug</td>
                            </tr>
                            `}
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6>Kandidature</h6>
                        <div class="candidacies-details">
                            ${election.candidacies && election.candidacies.length > 0 ? 
                                election.candidacies.map(candidacy => `
                                    <div class="candidacy-item">
                                        <div class="candidacy-info">
                                            <h6>${candidacy.name}</h6>
                                            <div class="candidacy-parties">
                                                ${candidacy.parties.map(party => `
                                                    <span class="party-chip ${party.is_lead_party ? 'lead-party-indicator' : ''}" 
                                                          style="background-color: ${party.color}">
                                                        ${party.name}${party.is_lead_party ? ' (vodeća)' : ''}
                                                    </span>
                                                `).join('')}
                                            </div>
                                        </div>
                                    </div>
                                `).join('')
                                : '<p class="text-muted">Nema kandidatura</p>'
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    async manageCandidacies(electionId) {
        this.currentElection = { id: electionId };
        await this.loadAvailableParties(electionId);
        await this.loadCandidacies(electionId);
        
        const modal = new bootstrap.Modal(document.getElementById('candidacyModal'));
        modal.show();
    }
    
    showCandidacyModal() {
        if (!this.currentElection) return;
        
        this.manageCandidacies(this.currentElection.id);
    }
    
    async loadAvailableParties(electionId) {
        try {
            const response = await fetch(`/api/elections/${electionId}/available-parties`);
            if (!response.ok) {
                throw new Error('Greška pri učitavanju partija');
            }
            
            const data = await response.json();
            this.availableParties = data.parties || [];
            this.renderAvailableParties();
            
        } catch (error) {
            console.error('Error loading available parties:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    renderAvailableParties() {
        const container = document.getElementById('available-parties-container');
        
        if (this.availableParties.length === 0) {
            container.innerHTML = '<p class="text-muted">Sve partije su već u kandidaturama</p>';
            return;
        }
        
        container.innerHTML = this.availableParties.map(party => `
            <div class="party-selection">
                <label class="party-checkbox">
                    <input type="checkbox" value="${party.id}" onchange="electionManager.togglePartySelection(${party.id})">
                    <div class="party-color-indicator" style="background-color: ${party.color}"></div>
                    <div class="party-info">
                        <div class="party-name">${party.name}</div>
                        <div class="party-ideology">${party.ideology}</div>
                    </div>
                </label>
            </div>
        `).join('');
    }
    
    togglePartySelection(partyId) {
        const checkbox = document.querySelector(`input[value="${partyId}"]`);
        const party = this.availableParties.find(p => p.id === partyId);
        
        if (checkbox.checked) {
            this.selectedParties.push(party);
        } else {
            this.selectedParties = this.selectedParties.filter(p => p.id !== partyId);
        }
        
        this.updateLeadPartyOptions();
        this.updateCandidacyName();
    }
    
    updateLeadPartyOptions() {
        const select = document.getElementById('leadParty');
        const group = document.getElementById('leadPartyGroup');
        
        if (this.selectedParties.length > 1) {
            group.style.display = 'block';
            select.innerHTML = '<option value="">Izaberite vodeću partiju...</option>' +
                this.selectedParties.map(party => `<option value="${party.id}">${party.name}</option>`).join('');
        } else {
            group.style.display = 'none';
            select.innerHTML = '';
        }
    }
    
    updateCandidacyName() {
        const nameInput = document.getElementById('candidacyName');
        const typeSelect = document.getElementById('candidacyType');
        
        if (this.selectedParties.length === 1 && typeSelect.value === 'party') {
            nameInput.value = this.selectedParties[0].name;
        } else if (this.selectedParties.length > 1 && typeSelect.value === 'coalition') {
            nameInput.value = this.selectedParties.map(p => p.name).join(' - ');
        }
    }
    
    handleCandidacyTypeChange(type) {
        const leadPartyGroup = document.getElementById('leadPartyGroup');
        
        // Reset selections
        this.selectedParties = [];
        document.querySelectorAll('#available-parties-container input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });
        
        this.updateLeadPartyOptions();
        document.getElementById('candidacyName').value = '';
        
        if (type === 'coalition') {
            // Coalition can have multiple parties
            leadPartyGroup.style.display = 'none';
        } else {
            // Single party candidacy
            leadPartyGroup.style.display = 'none';
        }
    }
    
    async loadCandidacies(electionId) {
        try {
            const response = await fetch(`/api/elections/${electionId}/candidacies`);
            if (!response.ok) {
                throw new Error('Greška pri učitavanju kandidatura');
            }
            
            const data = await response.json();
            this.renderCandidacies(data.candidacies || []);
            
        } catch (error) {
            console.error('Error loading candidacies:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    renderCandidacies(candidacies) {
        const container = document.getElementById('candidacies-list');
        
        if (candidacies.length === 0) {
            container.innerHTML = '<p class="text-muted">Nema kandidatura</p>';
            return;
        }
        
        container.innerHTML = candidacies.map(candidacy => `
            <div class="candidacy-item">
                <div class="candidacy-info">
                    <h6>${candidacy.name}</h6>
                    <div class="candidacy-parties">
                        ${candidacy.parties.map(party => `
                            <span class="party-chip ${party.is_lead_party ? 'lead-party-indicator' : ''}" 
                                  style="background-color: ${party.color}">
                                ${party.name}${party.is_lead_party ? ' (vodeća)' : ''}
                            </span>
                        `).join('')}
                    </div>
                </div>
                <button class="btn btn-outline-danger btn-sm" onclick="electionManager.deleteCandidacy(${candidacy.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    }
    
    async handleCreateCandidacy(e) {
        e.preventDefault();
        
        const form = e.target;
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }
        
        if (this.selectedParties.length === 0) {
            this.showToast('Greška', 'Molimo izaberite bar jednu partiju', 'error');
            return;
        }
        
        try {
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                type: formData.get('type'),
                party_ids: this.selectedParties.map(p => p.id),
                lead_party_id: formData.get('lead_party_id') || this.selectedParties[0].id
            };
            
            const response = await fetch(`/api/elections/${this.currentElection.id}/candidacies`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Greška pri kreiranju kandidature');
            }
            
            // Reset form
            form.reset();
            form.classList.remove('was-validated');
            this.selectedParties = [];
            
            // Reload data
            await this.loadAvailableParties(this.currentElection.id);
            await this.loadCandidacies(this.currentElection.id);
            await this.loadElections(); // Refresh main list
            
            this.showToast('Uspeh', 'Kandidatura je uspešno kreirana', 'success');
            
        } catch (error) {
            console.error('Error creating candidacy:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    async deleteCandidacy(candidacyId) {
        if (!confirm('Da li ste sigurni da želite da obrišete ovu kandidaturu?')) {
            return;
        }
        
        try {
            const response = await fetch(`/api/elections/${this.currentElection.id}/candidacies/${candidacyId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Greška pri brisanju kandidature');
            }
            
            // Reload data
            await this.loadAvailableParties(this.currentElection.id);
            await this.loadCandidacies(this.currentElection.id);
            await this.loadElections(); // Refresh main list
            
            this.showToast('Uspeh', 'Kandidatura je uspešno obrisana', 'success');
            
        } catch (error) {
            console.error('Error deleting candidacy:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    deleteElection(electionId, electionName) {
        this.currentElection = { id: electionId, name: electionName };
        document.getElementById('delete-election-name').textContent = electionName;
        
        const modal = new bootstrap.Modal(document.getElementById('deleteElectionModal'));
        modal.show();
    }
    
    async confirmDeleteElection() {
        try {
            const response = await fetch(`/api/elections/${this.currentElection.id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Greška pri brisanju izbora');
            }
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('deleteElectionModal')).hide();
            
            // Refresh elections list
            await this.loadElections();
            
            this.showToast('Uspeh', 'Izbori su uspešno obrisani', 'success');
            
        } catch (error) {
            console.error('Error deleting election:', error);
            this.showToast('Greška', error.message, 'error');
        }
    }
    
    // Utility methods
    getElectionTypeLabel(type) {
        const labels = {
            'parliamentary': 'Parlamentarni',
            'municipal': 'Opštinski',
            'presidential': 'Predsednički'
        };
        return labels[type] || type;
    }
    
    getElectionStatusLabel(status) {
        const labels = {
            'scheduled': 'Zakazan',
            'ongoing': 'U toku',
            'completed': 'Završen'
        };
        return labels[status] || status;
    }
    
    getElectionIcon(type) {
        const icons = {
            'parliamentary': '<i class="fas fa-university"></i>',
            'municipal': '<i class="fas fa-city"></i>',
            'presidential': '<i class="fas fa-crown"></i>'
        };
        return icons[type] || '<i class="fas fa-vote-yea"></i>';
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('sr-RS', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    showLoading(show) {
        const loadingContainer = document.getElementById('loading-container');
        const electionsContainer = document.getElementById('elections-grid');
        const emptyState = document.getElementById('empty-state');
        
        if (show) {
            loadingContainer.style.display = 'flex';
            electionsContainer.style.display = 'none';
            emptyState.style.display = 'none';
        } else {
            loadingContainer.style.display = 'none';
        }
    }
    
    showToast(title, message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        const toastId = 'toast-' + Date.now();
        
        const bgClass = {
            'success': 'bg-success',
            'error': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        }[type] || 'bg-info';
        
        const icon = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        }[type] || 'fas fa-info-circle';
        
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header ${bgClass} text-white">
                    <i class="${icon} me-2"></i>
                    <strong class="me-auto">${title}</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: type === 'error' ? 8000 : 5000
        });
        
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Initialize when DOM is loaded
let electionManager;
document.addEventListener('DOMContentLoaded', () => {
    electionManager = new ElectionManager();
});