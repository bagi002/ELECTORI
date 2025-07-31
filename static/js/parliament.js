/**
 * Parliament JavaScript
 * Handles parliament composition, laws, and coalition management
 */

class ParliamentManager {
    constructor() {
        this.composition = null;
        this.laws = [];
        this.charts = {};
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadParliamentComposition();
        this.loadLaws();
        this.setupCharts();
    }
    
    bindEvents() {
        // Generate parliament
        document.getElementById('generate-parliament-btn')?.addEventListener('click', () => {
            this.showGenerateParliamentModal();
        });
        
        document.getElementById('create-first-parliament-btn')?.addEventListener('click', () => {
            this.showGenerateParliamentModal();
        });
        
        document.getElementById('confirm-generate-parliament')?.addEventListener('click', () => {
            this.generateParliament();
        });
        
        // Create law
        document.getElementById('create-law-btn')?.addEventListener('click', () => {
            this.showCreateLawModal();
        });
        
        document.getElementById('createLawForm')?.addEventListener('submit', (e) => {
            this.handleCreateLaw(e);
        });
        
        // Refresh
        document.getElementById('refresh-parliament-btn')?.addEventListener('click', () => {
            this.refresh();
        });
        
        // Law status filter
        document.getElementById('law-status-filter')?.addEventListener('change', (e) => {
            this.filterLaws(e.target.value);
        });
    }
    
    async loadParliamentComposition() {
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/parliament/composition');
            if (!response.ok) {
                throw new Error('Greška pri učitavanju kompozicije parlamenta');
            }
            
            const data = await response.json();
            this.composition = data;
            this.renderComposition();
            this.renderStatistics();
            this.renderHemicycle();
            
        } catch (error) {
            console.error('Error loading parliament composition:', error);
            this.showEmptyState();
        } finally {
            this.showLoading(false);
        }
    }
    
    renderComposition() {
        if (!this.composition || Object.keys(this.composition.composition).length === 0) {
            this.showEmptyState();
            return;
        }
        
        this.hideEmptyState();
        this.updateCompositionChart();
        this.updateCompositionTable();
    }
    
    updateCompositionChart() {
        const ctx = document.getElementById('composition-chart').getContext('2d');
        
        const parties = Object.values(this.composition.composition);
        const labels = parties.map(p => p.party.name);
        const data = parties.map(p => p.seat_count);
        const colors = parties.map(p => p.party.color);
        
        if (this.charts.composition) {
            this.charts.composition.destroy();
        }
        
        this.charts.composition = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} poslanika (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '50%'
            }
        });
    }
    
    updateCompositionTable() {
        const tbody = document.querySelector('#composition-table tbody');
        tbody.innerHTML = '';
        
        const parties = Object.values(this.composition.composition);
        const totalSeats = this.composition.statistics.total_seats;
        const majorityThreshold = this.composition.statistics.majority_threshold;
        
        parties.forEach(partyData => {
            const row = document.createElement('tr');
            
            // Determine party status
            let status = 'minor';
            let statusLabel = 'Manja partija';
            
            if (partyData.seat_count >= majorityThreshold) {
                status = 'majority';
                statusLabel = 'Većinska';
            } else if (partyData.seat_count >= totalSeats * 0.1) {
                status = 'opposition';
                statusLabel = 'Opozicija';
            }
            
            row.innerHTML = `
                <td>
                    <div class="party-name">
                        <div class="party-color-indicator" style="background-color: ${partyData.party.color}"></div>
                        ${partyData.party.name}
                    </div>
                </td>
                <td class="seat-count">${partyData.seat_count}</td>
                <td class="percentage">${partyData.percentage.toFixed(1)}%</td>
                <td>
                    <span class="party-status status-${status}">${statusLabel}</span>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    renderStatistics() {
        if (!this.composition) return;
        
        const stats = this.composition.statistics;
        
        document.getElementById('total-mps').textContent = stats.total_seats;
        document.getElementById('total-seats').textContent = stats.total_seats;
        document.getElementById('majority-threshold').textContent = stats.majority_threshold;
    }
    
    async renderHemicycle() {
        try {
            const response = await fetch('/api/parliament/hemicycle-data');
            if (!response.ok) return;
            
            const data = await response.json();
            this.createHemicycleVisualization(data);
            
        } catch (error) {
            console.error('Error loading hemicycle data:', error);
        }
    }
    
    createHemicycleVisualization(data) {
        const container = document.getElementById('parliament-hemicycle');
        const legend = document.getElementById('hemicycle-legend');
        
        container.innerHTML = '';
        legend.innerHTML = '';
        
        // Create seats
        data.seats.forEach(seat => {
            const seatElement = document.createElement('div');
            seatElement.className = 'parliament-seat';
            seatElement.style.backgroundColor = seat.party_color;
            seatElement.style.left = `${seat.x}%`;
            seatElement.style.top = `${seat.y}%`;
            seatElement.title = `${seat.name} (${seat.party_name})`;
            
            container.appendChild(seatElement);
        });
        
        // Create legend
        const partyBlocks = Object.values(data.party_blocks);
        partyBlocks.forEach(block => {
            const legendItem = document.createElement('div');
            legendItem.className = 'legend-item';
            legendItem.innerHTML = `
                <div class="legend-color" style="background-color: ${block.party_color}"></div>
                <span>${block.party_name} (${block.seats})</span>
            `;
            legend.appendChild(legendItem);
        });
    }
    
    async loadLaws() {
        try {
            const response = await fetch('/api/parliament/laws');
            if (!response.ok) return;
            
            const data = await response.json();
            this.laws = data.laws;
            this.renderLaws();
            
            // Update statistics
            const activeLaws = this.laws.filter(law => law.status !== 'rejected').length;
            document.getElementById('active-laws').textContent = activeLaws;
            
        } catch (error) {
            console.error('Error loading laws:', error);
        }
    }
    
    renderLaws() {
        const container = document.getElementById('laws-grid');
        
        if (this.laws.length === 0) {
            container.innerHTML = '<p class="text-muted">Nema predloženih zakona</p>';
            return;
        }
        
        container.innerHTML = this.laws.map(law => this.createLawCard(law)).join('');
    }
    
    createLawCard(law) {
        const statusClass = `status-${law.status}`;
        const statusLabel = this.getStatusLabel(law.status);
        
        return `
            <div class="law-card" onclick="parliamentManager.viewLawDetails(${law.id})">
                <div class="law-title">${law.title}</div>
                <div class="law-meta">
                    <span>Predlagač: ${law.proposer_party?.name || 'N/A'}</span>
                    <span class="law-status ${statusClass}">${statusLabel}</span>
                </div>
                <div class="law-meta">
                    <span>Datum: ${this.formatDate(law.proposed_date)}</span>
                    <span>Glasovi: ${law.vote_counts.for}/${law.vote_counts.against}/${law.vote_counts.abstain}</span>
                </div>
            </div>
        `;
    }
    
    getStatusLabel(status) {
        const labels = {
            'proposed': 'Predložen',
            'voting': 'Na glasanju',
            'passed': 'Usvojen',
            'rejected': 'Odbačen'
        };
        return labels[status] || status;
    }
    
    filterLaws(status) {
        const filteredLaws = status ? this.laws.filter(law => law.status === status) : this.laws;
        const container = document.getElementById('laws-grid');
        
        if (filteredLaws.length === 0) {
            container.innerHTML = '<p class="text-muted">Nema zakona sa izabranim statusom</p>';
            return;
        }
        
        container.innerHTML = filteredLaws.map(law => this.createLawCard(law)).join('');
    }
    
    async showGenerateParliamentModal() {
        // Load available parliamentary elections
        try {
            const response = await fetch('/api/elections/');
            if (response.ok) {
                const data = await response.json();
                const parliamentaryElections = data.elections.filter(e => e.type === 'parliamentary');
                
                const select = document.getElementById('election-select');
                select.innerHTML = '<option value="">Izaberite izbore...</option>';
                
                parliamentaryElections.forEach(election => {
                    const option = document.createElement('option');
                    option.value = election.id;
                    option.textContent = `${election.name} (${this.formatDate(election.election_date)})`;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading elections:', error);
        }
        
        const modal = new bootstrap.Modal(document.getElementById('generateParliamentModal'));
        modal.show();
    }
    
    async generateParliament() {
        try {
            const electionId = document.getElementById('election-select').value;
            if (!electionId) {
                this.showError('Molimo izaberite izbore');
                return;
            }
            
            const response = await fetch(`/api/parliament/generate-from-election/${electionId}`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Greška pri generiranju parlamenta');
            }
            
            const result = await response.json();
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('generateParliamentModal')).hide();
            
            // Refresh data
            await this.loadParliamentComposition();
            
            this.showSuccess(`Parlament je uspešno generiran sa ${result.mps_created} poslanika`);
            
        } catch (error) {
            console.error('Error generating parliament:', error);
            this.showError(error.message);
        }
    }
    
    async showCreateLawModal() {
        // Load parties for proposer selection
        try {
            const response = await fetch('/api/parties/');
            if (response.ok) {
                const data = await response.json();
                
                const select = document.getElementById('proposerParty');
                select.innerHTML = '<option value="">Izaberite partiju...</option>';
                
                data.parties.forEach(party => {
                    const option = document.createElement('option');
                    option.value = party.id;
                    option.textContent = party.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading parties:', error);
        }
        
        // Set default date to today
        document.getElementById('proposedDate').value = new Date().toISOString().split('T')[0];
        
        const modal = new bootstrap.Modal(document.getElementById('createLawModal'));
        modal.show();
    }
    
    async handleCreateLaw(e) {
        e.preventDefault();
        
        try {
            const formData = new FormData(e.target);
            const data = {
                title: formData.get('title'),
                description: formData.get('description'),
                proposer_party_id: parseInt(formData.get('proposer_party_id')),
                proposed_date: formData.get('proposed_date'),
                parliament_type: 'national'
            };
            
            const response = await fetch('/api/parliament/laws', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Greška pri kreiranju zakona');
            }
            
            const law = await response.json();
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('createLawModal')).hide();
            
            // Reset form
            e.target.reset();
            
            // Refresh laws
            await this.loadLaws();
            
            this.showSuccess('Zakon je uspešno predložen');
            
        } catch (error) {
            console.error('Error creating law:', error);
            this.showError(error.message);
        }
    }
    
    viewLawDetails(lawId) {
        // Placeholder for law details modal
        console.log('View law details:', lawId);
    }
    
    async refresh() {
        await this.loadParliamentComposition();
        await this.loadLaws();
    }
    
    setupCharts() {
        if (typeof Chart !== 'undefined') {
            Chart.defaults.font.family = 'Inter, system-ui, sans-serif';
            Chart.defaults.color = '#4a5568';
        }
    }
    
    showLoading(show) {
        const container = document.getElementById('loading-container');
        const overview = document.querySelector('.parliament-overview');
        const statistics = document.querySelector('.parliament-statistics');
        
        if (show) {
            container.style.display = 'flex';
            if (overview) overview.style.display = 'none';
            if (statistics) statistics.style.display = 'none';
        } else {
            container.style.display = 'none';
            if (overview) overview.style.display = 'block';
            if (statistics) statistics.style.display = 'block';
        }
    }
    
    showEmptyState() {
        document.getElementById('empty-state').style.display = 'block';
        document.querySelector('.parliament-overview').style.display = 'none';
        document.querySelector('.parliament-statistics').style.display = 'none';
    }
    
    hideEmptyState() {
        document.getElementById('empty-state').style.display = 'none';
        document.querySelector('.parliament-overview').style.display = 'block';
        document.querySelector('.parliament-statistics').style.display = 'block';
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('sr-RS', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    showSuccess(message) {
        // Create success toast or alert
        console.log('Success:', message);
        alert(`Uspeh: ${message}`);
    }
    
    showError(message) {
        // Create error toast or alert
        console.error('Error:', message);
        alert(`Greška: ${message}`);
    }
}

// Initialize when DOM is loaded
let parliamentManager;
document.addEventListener('DOMContentLoaded', () => {
    parliamentManager = new ParliamentManager();
});