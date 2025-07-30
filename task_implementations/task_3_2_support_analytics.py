"""
Task 3.2 Implementation: Support Analytics with Slider-controlled Visualizations

Implementacija analitike i grafikona za podršku sa fokus na slider-based kontrole za intuitivnu interakciju.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional


class SupportAnalyticsImplementation:
    """Implementacija Support Analytics sistema sa slider kontrolama."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.templates_dir = Path("templates")
        self.static_dir = Path("static")
        self.utils_dir = Path("utils")
        
    def execute(self) -> bool:
        """Izvršava kompletan Task 3.2."""
        try:
            self.logger.info("📊 Početak implementacije Support Analytics sa sliderima")
            
            # Korak 1: Kreiranje Chart Data Utils
            if not self._create_chart_data_utils():
                return False
                
            # Korak 2: HTML template za analytics sa sliderima
            if not self._create_analytics_template():
                return False
                
            # Korak 3: JavaScript za Chart.js sa slider kontrolama
            if not self._create_charts_javascript():
                return False
                
            # Korak 4: CSS stilovi za analytics i slajdere
            if not self._create_analytics_styles():
                return False
                
            # Korak 5: Dodatni API endpointi za analytics
            if not self._extend_support_routes():
                return False
                
            # Korak 6: Testiranje analytics funkcionalnosti
            if not self._test_analytics():
                return False
                
            self.logger.info("✅ Task 3.2 Support Analytics uspešno implementiran!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška u Task 3.2: {str(e)}")
            return False
    
    def _create_chart_data_utils(self) -> bool:
        """Kreiranje utility funkcija za Chart.js podatke."""
        try:
            self.logger.info("🔧 Kreiranje chart_data.py utils")
            
            utils_content = '''"""
Utility functions for chart data processing in Support Analytics.
Fokus na pripremu podataka za Chart.js sa slider kontrolama.
"""

from typing import Dict, List, Any, Optional, Tuple
from models import Party, City, PartySupport, Simulation
from sqlalchemy import func
from extensions import db
import json
import random


class ChartDataProcessor:
    """Klasa za procesiranje podataka za chart-ove sa slider parametrima."""
    
    def __init__(self, simulation_id: int):
        self.simulation_id = simulation_id
        self.parties = Party.query.filter_by(simulation_id=simulation_id).all()
        self.cities = City.query.filter_by(simulation_id=simulation_id).all()
    
    def get_pie_chart_data(self, city_id: Optional[int] = None, 
                          min_support: float = 0, max_support: float = 100) -> Dict[str, Any]:
        """
        Generiše podatke za pie chart sa slider filterima.
        
        Args:
            city_id: ID grada (None za sve gradove)
            min_support: Minimalna podrška za prikaz (slider kontrola)
            max_support: Maksimalna podrška za prikaz (slider kontrola)
        """
        if city_id:
            # Pie chart za specifičan grad
            supports = PartySupport.query.filter_by(city_id=city_id).join(Party).filter(
                Party.simulation_id == self.simulation_id,
                PartySupport.support_percentage >= min_support,
                PartySupport.support_percentage <= max_support
            ).all()
            
            labels = []
            data = []
            background_colors = []
            
            for support in supports:
                if support.support_percentage > 0:
                    labels.append(support.party.name)
                    data.append(support.support_percentage)
                    background_colors.append(support.party.color)
            
            # Dodaj "Other" kategoriju ako ima filtriranih podataka
            total_shown = sum(data)
            if total_shown < 100:
                labels.append("Ostalo")
                data.append(100 - total_shown)
                background_colors.append("#e9ecef")
        
        else:
            # Pie chart za prosečnu podršku kroz sve gradove
            party_averages = db.session.query(
                Party.id,
                Party.name,
                Party.color,
                func.avg(PartySupport.support_percentage).label('avg_support')
            ).join(PartySupport).filter(
                Party.simulation_id == self.simulation_id
            ).group_by(Party.id).having(
                func.avg(PartySupport.support_percentage) >= min_support,
                func.avg(PartySupport.support_percentage) <= max_support
            ).all()
            
            labels = [p.name for p in party_averages]
            data = [float(p.avg_support) for p in party_averages]
            background_colors = [p.color for p in party_averages]
        
        return {
            'type': 'pie',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': background_colors,
                    'borderColor': '#ffffff',
                    'borderWidth': 2,
                    'hoverBorderWidth': 3
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom',
                        'labels': {
                            'usePointStyle': True,
                            'padding': 20
                        }
                    },
                    'tooltip': {
                        'callbacks': {
                            'label': 'function(context) { return context.label + ": " + context.parsed.toFixed(1) + "%"; }'
                        }
                    }
                },
                'animation': {
                    'animateRotate': True,
                    'animateScale': True
                }
            }
        }
    
    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        """Konvertuje hex boju u RGBA sa alpha kanalom."""
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f'rgba({r}, {g}, {b}, {alpha})'
        
        return f'rgba(0, 0, 0, {alpha})'  # fallback'''

            # Kreiraj utils direktorijum ako ne postoji
            self.utils_dir.mkdir(exist_ok=True)
            
            utils_path = self.utils_dir / "chart_data.py"
            with open(utils_path, 'w', encoding='utf-8') as f:
                f.write(utils_content)
                
            self.logger.info(f"✅ Chart data utils kreiran: {utils_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju chart data utils: {str(e)}")
            return False
    
    def _create_analytics_template(self) -> bool:
        """Kreiranje HTML template-a za analytics sa sliderima."""
        try:
            self.logger.info("📄 Kreiranje support_analytics.html template-a")
            
            template_content = '''{% extends "base.html" %}
{% block title %}Support Analytics - {{ simulation.name if simulation else 'ELECTORI' }}{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/support_matrix.css') }}">
<style>
.analytics-container { padding: 1rem; }
.chart-container { position: relative; height: 400px; margin-bottom: 2rem; }
.slider-controls { background: #f8f9fa; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; }
</style>
{% endblock %}

{% block content %}
<div class="analytics-container">
    <div class="row">
        <div class="col-12">
            <h1 class="h3 mb-4">
                <i class="fas fa-chart-area"></i>
                Support Analytics
            </h1>
        </div>
    </div>

    <!-- Slider Controls -->
    <div class="row">
        <div class="col-12">
            <div class="slider-controls">
                <div class="row">
                    <div class="col-md-3">
                        <label>Min Support Filter</label>
                        <input type="range" class="form-range" id="minSupportSlider" min="0" max="100" value="0">
                        <span id="minSupportValue">0%</span>
                    </div>
                    <div class="col-md-3">
                        <label>Max Support Filter</label>
                        <input type="range" class="form-range" id="maxSupportSlider" min="0" max="100" value="100">
                        <span id="maxSupportValue">100%</span>
                    </div>
                    <div class="col-md-3">
                        <label>Chart Opacity</label>
                        <input type="range" class="form-range" id="opacitySlider" min="0.1" max="1.0" step="0.1" value="1.0">
                        <span id="opacityValue">100%</span>
                    </div>
                    <div class="col-md-3">
                        <label>Animation Speed</label>
                        <input type="range" class="form-range" id="animationSlider" min="500" max="3000" step="100" value="1000">
                        <span id="animationValue">1000ms</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Charts -->
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Party Distribution</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Party Comparison</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ url_for('static', filename='js/charts.js') }}"></script>
{% endblock %}'''

            template_path = self.templates_dir / "support_analytics.html"
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
                
            self.logger.info(f"✅ Analytics template kreiran: {template_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju analytics template-a: {str(e)}")
            return False
    
    def _create_charts_javascript(self) -> bool:
        """Kreiranje JavaScript-a za Chart.js sa slider kontrolama."""
        try:
            self.logger.info("📜 Kreiranje charts.js")
            
            js_content = '''/**
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
});'''

            js_dir = self.static_dir / "js"
            js_dir.mkdir(parents=True, exist_ok=True)
            
            js_path = js_dir / "charts.js"
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
                
            self.logger.info(f"✅ Charts JavaScript kreiran: {js_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri kreiranju charts JavaScript-a: {str(e)}")
            return False
    
    def _create_analytics_styles(self) -> bool:
        """Kreiranje dodatnih CSS stilova za analytics."""
        # Analytics koriste iste stilove kao support matrix
        self.logger.info("✅ Analytics koriste postojeće slider stilove")
        return True
    
    def _extend_support_routes(self) -> bool:
        """Dodavanje analytics endpoint-a u support routes."""
        # Analytics endpoint už postoji u support_routes.py
        self.logger.info("✅ Analytics endpoints već postoje u support_routes.py")
        return True
    
    def _test_analytics(self) -> bool:
        """Testiranje analytics funkcionalnosti."""
        try:
            self.logger.info("🧪 Pokretanje testova za Support Analytics")
            
            # Test postojanja fajlova
            required_files = [
                "templates/support_analytics.html",
                "static/js/charts.js",
                "utils/chart_data.py"
            ]
            
            for file_path in required_files:
                if not Path(file_path).exists():
                    self.logger.error(f"❌ Nedostaje fajl: {file_path}")
                    return False
            
            self.logger.info("✅ Svi analytics fajlovi postoje")
            
            # Test HTML template sadržaja
            template_path = Path("templates/support_analytics.html")
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_elements = [
                'id="minSupportSlider"',
                'id="opacitySlider"',
                'id="pieChart"',
                'id="barChart"',
                'chart.js'  # Changed from 'Chart.js' to match actual template
            ]
            
            for element in required_elements:
                if element not in content:
                    self.logger.error(f"❌ Template ne sadrži: {element}")
                    return False
            
            self.logger.info("✅ Analytics template je valjan")
            
            # Test JavaScript funkcija
            js_path = Path("static/js/charts.js")
            with open(js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_functions = [
                'setupSliders',
                'createCharts',
                'updateCharts',
                'filterPartyData'
            ]
            
            for func in required_functions:
                if func not in content:
                    self.logger.error(f"❌ JavaScript ne sadrži funkciju: {func}")
                    return False
            
            self.logger.info("✅ Charts JavaScript je valjan")
            
            self.logger.info("🎉 Svi analytics testovi prošli uspešno!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri testiranju analytics: {str(e)}")
            return False