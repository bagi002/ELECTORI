/**
 * Election Day Simulation JavaScript
 * Handles real-time election simulation with animated results
 */

class ElectionSimulation {
    constructor() {
        this.electionId = null;
        this.election = null;
        this.simulationRunning = false;
        this.charts = {};
        this.results = null;
        
        this.init();
    }
    
    init() {
        this.electionId = this.getElectionIdFromUrl();
        this.bindEvents();
        this.loadElectionInfo();
        this.setupCharts();
    }
    
    getElectionIdFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('election_id');
    }
    
    bindEvents() {
        // Start simulation
        document.getElementById('start-simulation-btn')?.addEventListener('click', () => {
            this.showSimulationSettings();
        });
        
        // Simulation settings
        document.getElementById('start-simulation-confirm')?.addEventListener('click', () => {
            this.startSimulation();
        });
        
        // Back to manager
        document.getElementById('back-to-manager-btn')?.addEventListener('click', () => {
            window.location.href = '/election-manager';
        });
        
        // City selector
        document.getElementById('city-selector')?.addEventListener('change', (e) => {
            this.showCityResults(e.target.value);
        });
        
        // Export buttons
        document.getElementById('export-pdf-btn')?.addEventListener('click', () => {
            this.exportResults('pdf');
        });
        
        document.getElementById('export-excel-btn')?.addEventListener('click', () => {
            this.exportResults('excel');
        });
        
        document.getElementById('export-json-btn')?.addEventListener('click', () => {
            this.exportResults('json');
        });
        
        // Randomness factor slider
        const randomnessSlider = document.getElementById('randomness-factor');
        if (randomnessSlider) {
            randomnessSlider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                document.getElementById('randomness-value').textContent = `${Math.round(value * 100)}%`;
            });
        }
    }
    
    async loadElectionInfo() {
        try {
            if (!this.electionId) {
                this.showError('ID izbora nije pronađen u URL-u');
                return;
            }
            
            const response = await fetch(`/api/elections/${this.electionId}`);
            if (!response.ok) {
                throw new Error('Greška pri učitavanju informacija o izboru');
            }
            
            this.election = await response.json();
            this.displayElectionInfo();
            this.checkExistingResults();
            
        } catch (error) {
            console.error('Error loading election info:', error);
            this.showError(error.message);
        }
    }
    
    displayElectionInfo() {
        document.getElementById('election-name').textContent = this.election.name;
        document.getElementById('election-date').textContent = this.formatDate(this.election.election_date);
        document.getElementById('election-type').textContent = this.getElectionTypeLabel(this.election.type);
        
        // Show parliament settings for parliamentary elections
        if (this.election.type === 'parliamentary') {
            document.getElementById('parliament-settings').style.display = 'block';
            document.getElementById('parliament-card').style.display = 'block';
        }
        
        // Show runoff info for presidential elections
        if (this.election.type === 'presidential') {
            document.getElementById('runoff-card').style.display = 'block';
        }
    }
    
    async checkExistingResults() {
        try {
            const response = await fetch(`/api/elections/${this.electionId}/results`);
            if (response.ok) {
                const data = await response.json();
                if (data.has_results) {
                    this.results = data;
                    this.displayResults();
                    this.showResultsSection();
                }
            }
        } catch (error) {
            console.error('Error checking existing results:', error);
        }
    }
    
    showSimulationSettings() {
        electoriUI.showModal('simulationSettingsModal');
    }
    
    async startSimulation() {
        try {
            // Close settings modal
            electoriUI.hideModal('simulationSettingsModal');
            
            // Get settings
            const randomnessFactor = parseFloat(document.getElementById('randomness-factor').value);
            const totalSeats = parseInt(document.getElementById('total-seats-input').value);
            
            // Show simulation status
            this.showSimulationStatus();
            this.simulationRunning = true;
            
            // Start simulation steps
            await this.runSimulationSteps(randomnessFactor, totalSeats);
            
        } catch (error) {
            console.error('Error starting simulation:', error);
            electoriUI.showAlert(error.message, 'danger');
            this.simulationRunning = false;
        }
    }
    
    async runSimulationSteps(randomnessFactor, totalSeats) {
        const steps = [
            { message: 'Priprema simulacije...', progress: 10 },
            { message: 'Učitavanje podataka o podršci...', progress: 20 },
            { message: 'Kalkulisanje glasova po gradovima...', progress: 40 },
            { message: 'Primena faktora nasumičnosti...', progress: 60 },
            { message: 'Brojanje glasova...', progress: 80 },
            { message: 'Kalkulisanje konačnih rezultata...', progress: 90 },
            { message: 'Završetak simulacije...', progress: 100 }
        ];
        
        // Show simulation progress
        for (let i = 0; i < steps.length; i++) {
            await this.updateSimulationProgress(steps[i]);
            await this.delay(800 + Math.random() * 400); // Random delay for realism
        }
        
        // Run the actual simulation
        try {
            const simulationData = {
                randomness_factor: randomnessFactor
            };
            
            const response = await fetch(`/api/elections/${this.electionId}/simulate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(simulationData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Greška pri simulaciji');
            }
            
            this.results = await response.json();
            
            // Hide simulation status and show results
            await this.delay(1000);
            this.hideSimulationStatus();
            this.displayResults();
            this.showResultsSection();
            this.showWinnerAnnouncement();
            
        } catch (error) {
            throw error;
        } finally {
            this.simulationRunning = false;
        }
    }
    
    async updateSimulationProgress(step) {
        const progressBar = document.getElementById('simulation-progress');
        const progressText = document.getElementById('progress-text');
        const messagesContainer = document.getElementById('simulation-messages');
        
        // Update progress bar
        progressBar.style.width = `${step.progress}%`;
        progressText.textContent = step.message;
        
        // Add message
        const messageDiv = document.createElement('div');
        messageDiv.className = 'simulation-message';
        messageDiv.textContent = `${new Date().toLocaleTimeString()} - ${step.message}`;
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    showSimulationStatus() {
        document.getElementById('simulation-status').style.display = 'block';
        document.getElementById('simulation-status').classList.add('fade-in-up');
    }
    
    hideSimulationStatus() {
        document.getElementById('simulation-status').style.display = 'none';
    }
    
    displayResults() {
        if (!this.results) return;
        
        this.displayNationalResults();
        this.displayCityResults();
        this.displayStatistics();
        
        if (this.election.type === 'parliamentary') {
            this.displayParliamentComposition();
        }
        
        if (this.election.type === 'presidential' && this.results.runoff) {
            this.displayRunoffInfo();
        }
    }
    
    displayNationalResults() {
        const nationalResults = this.results.national;
        
        // Update turnout
        document.getElementById('national-turnout').textContent = 
            `${nationalResults.turnout_percentage?.toFixed(1) || 0}%`;
        
        // Update chart
        this.updateNationalChart(nationalResults);
        
        // Update table
        this.updateResultsTable(nationalResults);
    }
    
    updateNationalChart(results) {
        const ctx = document.getElementById('national-results-chart').getContext('2d');
        
        // Get candidacy data
        const candidacyData = this.prepareCandidacyData(results);
        
        if (this.charts.national) {
            this.charts.national.destroy();
        }
        
        this.charts.national = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: candidacyData.labels,
                datasets: [{
                    data: candidacyData.percentages,
                    backgroundColor: candidacyData.colors,
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
                                return `${label}: ${value.toFixed(1)}%`;
                            }
                        }
                    }
                },
                cutout: '50%'
            }
        });
    }
    
    updateResultsTable(results) {
        const tbody = document.querySelector('#national-results-table tbody');
        tbody.innerHTML = '';
        
        const candidacyData = this.prepareCandidacyData(results);
        
        candidacyData.entries.forEach((entry, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="party-name">
                        <div class="party-color" style="background-color: ${candidacyData.colors[index]}"></div>
                        ${entry.name}
                    </div>
                </td>
                <td class="vote-count">${this.formatNumber(entry.votes)}</td>
                <td class="vote-percentage">${entry.percentage.toFixed(1)}%</td>
                <td class="seats-column">
                    ${entry.seats !== undefined ? `<span class="seat-count">${entry.seats}</span>` : '-'}
                </td>
            `;
            tbody.appendChild(row);
        });
    }
    
    prepareCandidacyData(results) {
        const candidacyEntries = [];
        
        // Get candidacy information
        for (let candidacyId in results.percentages) {
            const candidacy = this.election.candidacies.find(c => c.id == candidacyId);
            if (candidacy) {
                candidacyEntries.push({
                    id: candidacyId,
                    name: candidacy.name,
                    percentage: results.percentages[candidacyId],
                    votes: results.votes[candidacyId],
                    seats: results.seats ? results.seats[candidacyId] : undefined,
                    color: this.getCandidacyColor(candidacy)
                });
            }
        }
        
        // Sort by percentage descending
        candidacyEntries.sort((a, b) => b.percentage - a.percentage);
        
        return {
            entries: candidacyEntries,
            labels: candidacyEntries.map(e => e.name),
            percentages: candidacyEntries.map(e => e.percentage),
            colors: candidacyEntries.map(e => e.color)
        };
    }
    
    getCandidacyColor(candidacy) {
        // Use lead party color or generate one
        if (candidacy.parties && candidacy.parties.length > 0) {
            const leadParty = candidacy.parties.find(p => p.is_lead_party) || candidacy.parties[0];
            return leadParty.color;
        }
        
        // Generate color based on candidacy ID
        const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22'];
        return colors[candidacy.id % colors.length];
    }
    
    displayCityResults() {
        if (!this.results.cities) return;
        
        // Populate city selector
        this.populateCitySelector();
        
        // Show all cities initially
        this.showAllCityResults();
    }
    
    populateCitySelector() {
        const selector = document.getElementById('city-selector');
        selector.innerHTML = '<option value="">Svi gradovi</option>';
        
        for (let cityId in this.results.cities) {
            const cityData = this.results.cities[cityId];
            const option = document.createElement('option');
            option.value = cityId;
            option.textContent = cityData.city_name;
            selector.appendChild(option);
        }
    }
    
    showAllCityResults() {
        const container = document.getElementById('city-results-grid');
        container.innerHTML = '';
        
        for (let cityId in this.results.cities) {
            const cityData = this.results.cities[cityId];
            const cityCard = this.createCityResultCard(cityData);
            container.appendChild(cityCard);
        }
    }
    
    showCityResults(cityId) {
        const container = document.getElementById('city-results-grid');
        
        if (!cityId) {
            this.showAllCityResults();
            return;
        }
        
        const cityData = this.results.cities[cityId];
        if (cityData) {
            container.innerHTML = '';
            const cityCard = this.createCityResultCard(cityData);
            container.appendChild(cityCard);
        }
    }
    
    createCityResultCard(cityData) {
        const card = document.createElement('div');
        card.className = 'city-result-card slide-in-left';
        
        // Find winner
        let winnerId = null;
        let maxPercentage = 0;
        for (let candidacyId in cityData.percentages) {
            if (cityData.percentages[candidacyId] > maxPercentage) {
                maxPercentage = cityData.percentages[candidacyId];
                winnerId = candidacyId;
            }
        }
        
        const winner = this.election.candidacies.find(c => c.id == winnerId);
        
        card.innerHTML = `
            <div class="city-name">${cityData.city_name}</div>
            <div class="city-turnout">
                Izlaznost: ${cityData.turnout?.toFixed(1) || 0}% 
                (${this.formatNumber(cityData.voters)} glasača)
            </div>
            <div class="city-winner">
                <span class="winner-badge">Pobednik</span>
                ${winner ? winner.name : 'N/A'} - ${maxPercentage.toFixed(1)}%
            </div>
        `;
        
        return card;
    }
    
    displayParliamentComposition() {
        if (!this.results.national.seats) return;
        
        // Load D'Hondt analysis
        this.loadDHondtAnalysis();
        
        // Create hemicycle visualization
        this.createHemicycleVisualization();
    }
    
    async loadDHondtAnalysis() {
        try {
            const response = await fetch(`/api/elections/${this.electionId}/dhondt-analysis`);
            if (response.ok) {
                const analysis = await response.json();
                this.displayCoalitionAnalysis(analysis);
            }
        } catch (error) {
            console.error('Error loading D\'Hondt analysis:', error);
        }
    }
    
    createHemicycleVisualization() {
        const container = document.getElementById('parliament-hemicycle');
        container.innerHTML = '';
        
        const seats = this.results.national.seats;
        const totalSeats = Object.values(seats).reduce((sum, count) => sum + count, 0);
        
        document.getElementById('total-seats').textContent = totalSeats;
        
        let seatIndex = 0;
        for (let candidacyId in seats) {
            const seatCount = seats[candidacyId];
            const candidacy = this.election.candidacies.find(c => c.id == candidacyId);
            const color = this.getCandidacyColor(candidacy);
            
            for (let i = 0; i < seatCount; i++) {
                const seat = document.createElement('div');
                seat.className = 'parliament-seat';
                seat.style.backgroundColor = color;
                seat.title = `${candidacy.name} - Mandat ${i + 1}`;
                
                // Position seat in hemicycle
                const angle = (seatIndex / totalSeats) * Math.PI;
                const radius = 80 + (Math.floor(seatIndex / 50) * 15); // Multiple rows
                const x = 50 + (radius * Math.cos(angle));
                const y = 90 - (radius * Math.sin(angle));
                
                seat.style.left = `${x}%`;
                seat.style.top = `${y}%`;
                
                container.appendChild(seat);
                seatIndex++;
            }
        }
    }
    
    async displayCoalitionAnalysis(analysis) {
        try {
            const response = await fetch(`/api/elections/${this.electionId}/coalitions`);
            if (response.ok) {
                const coalitions = await response.json();
                this.renderCoalitionOptions(coalitions);
            }
        } catch (error) {
            console.error('Error loading coalitions:', error);
        }
    }
    
    renderCoalitionOptions(coalitionData) {
        const container = document.getElementById('coalition-analysis');
        
        const html = `
            <h5>Moguce koalicije za većinu (${coalitionData.metadata.required_seats} mandata)</h5>
            <div class="coalition-options">
                ${coalitionData.coalitions.slice(0, 5).map(coalition => `
                    <div class="coalition-option">
                        <div class="coalition-info">
                            <strong>${coalition.total_seats} mandata</strong>
                            <div class="coalition-parties">
                                ${coalition.candidacies.map(c => `
                                    <span class="coalition-party">${c.name} (${c.seats})</span>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    displayRunoffInfo() {
        if (!this.results.runoff) return;
        
        const container = document.getElementById('runoff-content');
        
        if (this.results.runoff.needed) {
            const topCandidates = this.results.runoff.candidates.map(id => {
                const candidacy = this.election.candidacies.find(c => c.id == id);
                const percentage = this.results.national.percentages[id];
                return { candidacy, percentage };
            });
            
            container.innerHTML = `
                <div class="runoff-info">
                    <p>Nijedan kandidat nije osvojio više od 50% glasova. Potreban je drugi krug.</p>
                    <div class="runoff-candidates">
                        ${topCandidates.map(candidate => `
                            <div class="runoff-candidate">
                                <div class="candidate-percentage">${candidate.percentage.toFixed(1)}%</div>
                                <div class="candidate-name">${candidate.candidacy.name}</div>
                            </div>
                        `).join('')}
                    </div>
                    <p class="text-muted">Ovi kandidati prolaze u drugi krug glasanja.</p>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="runoff-info">
                    <p>Drugi krug nije potreban - pobednik je određen u prvom krugu.</p>
                </div>
            `;
        }
    }
    
    displayStatistics() {
        const metadata = this.results.metadata;
        
        document.getElementById('total-voters').textContent = this.formatNumber(metadata.total_voters);
        document.getElementById('total-votes').textContent = this.formatNumber(metadata.total_votes);
        document.getElementById('average-turnout').textContent = `${metadata.turnout_percentage?.toFixed(1) || 0}%`;
        
        // Calculate winner margin
        const percentages = Object.values(this.results.national.percentages);
        percentages.sort((a, b) => b - a);
        const margin = percentages.length > 1 ? percentages[0] - percentages[1] : percentages[0];
        document.getElementById('winner-margin').textContent = `${margin.toFixed(1)}%`;
    }
    
    showResultsSection() {
        document.getElementById('results-container').style.display = 'block';
        document.getElementById('statistics-section').style.display = 'block';
        document.getElementById('export-section').style.display = 'block';
        
        // Add animations
        document.getElementById('results-container').classList.add('fade-in-up');
        document.getElementById('statistics-section').classList.add('fade-in-up');
        document.getElementById('export-section').classList.add('fade-in-up');
    }
    
    showWinnerAnnouncement() {
        // Find overall winner
        const nationalResults = this.results.national;
        let winnerId = null;
        let maxPercentage = 0;
        
        for (let candidacyId in nationalResults.percentages) {
            if (nationalResults.percentages[candidacyId] > maxPercentage) {
                maxPercentage = nationalResults.percentages[candidacyId];
                winnerId = candidacyId;
            }
        }
        
        const winner = this.election.candidacies.find(c => c.id == winnerId);
        if (winner) {
            const winnerInfo = document.getElementById('winner-info');
            winnerInfo.innerHTML = `
                <h3>${winner.name}</h3>
                <p class="winner-percentage">${maxPercentage.toFixed(1)}% glasova</p>
                ${this.results.national.seats ? `<p>${this.results.national.seats[winnerId]} mandata</p>` : ''}
            `;
            
            setTimeout(() => electoriUI.showModal('winnerModal'), 1000);
        }
    }
    
    setupCharts() {
        Chart.defaults.font.family = 'Inter, system-ui, sans-serif';
        Chart.defaults.color = '#4a5568';
    }
    
    async exportResults(format) {
        try {
            let url = `/api/elections/${this.electionId}/export?format=${format}`;
            
            if (format === 'json') {
                // For JSON, just download the current results
                const blob = new Blob([JSON.stringify(this.results, null, 2)], 
                    { type: 'application/json' });
                this.downloadBlob(blob, `election_results_${this.electionId}.json`);
                return;
            }
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Greška pri eksportu');
            }
            
            const blob = await response.blob();
            const extension = format === 'pdf' ? 'pdf' : 'xlsx';
            this.downloadBlob(blob, `election_results_${this.electionId}.${extension}`);
            
        } catch (error) {
            console.error('Error exporting results:', error);
            this.showError(error.message);
        }
    }
    
    downloadBlob(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
    
    // Utility methods
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('sr-RS', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    getElectionTypeLabel(type) {
        const labels = {
            'parliamentary': 'Parlamentarni izbori',
            'municipal': 'Opštinski izbori',
            'presidential': 'Predsednički izbori'
        };
        return labels[type] || type;
    }
    
    formatNumber(num) {
        if (num === null || num === undefined) return '0';
        return new Intl.NumberFormat('sr-RS').format(num);
    }
    
    showError(message) {
        electoriUI.showAlert(`Greška: ${message}`, 'danger');
    }
}

// Initialize when DOM is loaded
let electionSimulation;
document.addEventListener('DOMContentLoaded', () => {
    electionSimulation = new ElectionSimulation();
});