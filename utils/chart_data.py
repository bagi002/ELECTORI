"""
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
        
        return f'rgba(0, 0, 0, {alpha})'  # fallback