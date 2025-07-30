/**
 * Support Analytics Charts with Slider Controls
 */

class SupportAnalytics {
    constructor() {
        this.charts = {};
        this.currentData = {};
        this.sliderValues = {
            minSupport: 0,
            maxSupport: 100,
            opacity: 1.0,
            animationSpeed: 1000
        };
        
        this.init();
    }
    
    async init() {
        console.log('📊 Initializing Support Analytics');
        
        this.setupSliders();
        await this.loadData();
        this.createCharts();
    }
    
    setupSliders() {
        // Min Support Slider
        const minSupportSlider = document.getElementById('minSupportSlider');
        const minSupportValue = document.getElementById('minSupportValue');
        
        minSupportSlider?.addEventListener('input', (e) => {
            this.sliderValues.minSupport = parseFloat(e.target.value);
            minSupportValue.textContent = e.target.value + '%';
            this.updateCharts();
        });
        
        // Max Support Slider
        const maxSupportSlider = document.getElementById('maxSupportSlider');
        const maxSupportValue = document.getElementById('maxSupportValue');
        
        maxSupportSlider?.addEventListener('input', (e) => {
            this.sliderValues.maxSupport = parseFloat(e.target.value);
            maxSupportValue.textContent = e.target.value + '%';
            this.updateCharts();
        });
        
        // Opacity Slider
        const opacitySlider = document.getElementById('opacitySlider');
        const opacityValue = document.getElementById('opacityValue');
        
        opacitySlider?.addEventListener('input', (e) => {
            this.sliderValues.opacity = parseFloat(e.target.value);
            opacityValue.textContent = Math.round(e.target.value * 100) + '%';
            this.updateCharts();
        });
        
        // Animation Speed Slider
        const animationSlider = document.getElementById('animationSlider');
        const animationValue = document.getElementById('animationValue');
        
        animationSlider?.addEventListener('input', (e) => {
            this.sliderValues.animationSpeed = parseInt(e.target.value);
            animationValue.textContent = e.target.value + 'ms';
            this.updateChartAnimations();
        });
    }
    
    async loadData() {
        try {
            const response = await fetch('/api/support/analytics/summary');
            if (!response.ok) throw new Error('Failed to load analytics data');
            
            this.currentData = await response.json();
            console.log('📊 Analytics data loaded:', this.currentData);
        } catch (error) {
            console.error('❌ Error loading analytics data:', error);
        }
    }
    
    createCharts() {
        this.createPieChart();
        this.createBarChart();
    }
    
    createPieChart() {
        const ctx = document.getElementById('pieChart');
        if (!ctx) return;
        
        const filteredData = this.filterPartyData();
        
        this.charts.pie = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: filteredData.labels,
                datasets: [{
                    data: filteredData.data,
                    backgroundColor: filteredData.colors.map(color => 
                        this.hexToRgba(color, this.sliderValues.opacity)
                    ),
                    borderColor: filteredData.colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: this.sliderValues.animationSpeed
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    createBarChart() {
        const ctx = document.getElementById('barChart');
        if (!ctx) return;
        
        const filteredData = this.filterPartyData();
        
        this.charts.bar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: filteredData.labels,
                datasets: [{
                    label: 'Average Support',
                    data: filteredData.data,
                    backgroundColor: filteredData.colors.map(color => 
                        this.hexToRgba(color, this.sliderValues.opacity)
                    ),
                    borderColor: filteredData.colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: this.sliderValues.animationSpeed
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
    
    filterPartyData() {
        if (!this.currentData.party_analytics) {
            return { labels: [], data: [], colors: [] };
        }
        
        const filtered = this.currentData.party_analytics.filter(party => 
            party.average_support >= this.sliderValues.minSupport &&
            party.average_support <= this.sliderValues.maxSupport
        );
        
        return {
            labels: filtered.map(p => p.party_name),
            data: filtered.map(p => p.average_support),
            colors: filtered.map(p => p.party_color)
        };
    }
    
    updateCharts() {
        const filteredData = this.filterPartyData();
        
        // Update pie chart
        if (this.charts.pie) {
            this.charts.pie.data.labels = filteredData.labels;
            this.charts.pie.data.datasets[0].data = filteredData.data;
            this.charts.pie.data.datasets[0].backgroundColor = filteredData.colors.map(color => 
                this.hexToRgba(color, this.sliderValues.opacity)
            );
            this.charts.pie.update();
        }
        
        // Update bar chart
        if (this.charts.bar) {
            this.charts.bar.data.labels = filteredData.labels;
            this.charts.bar.data.datasets[0].data = filteredData.data;
            this.charts.bar.data.datasets[0].backgroundColor = filteredData.colors.map(color => 
                this.hexToRgba(color, this.sliderValues.opacity)
            );
            this.charts.bar.update();
        }
    }
    
    updateChartAnimations() {
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.options.animation) {
                chart.options.animation.duration = this.sliderValues.animationSpeed;
            }
        });
    }
    
    hexToRgba(hex, alpha) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SupportAnalytics();
});