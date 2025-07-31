# Helper utilities for ELECTORI application
from flask import session, jsonify
from models.simulation import Simulation

def get_active_simulation():
    """Get the currently active simulation from session"""
    simulation_id = session.get('active_simulation_id')
    if not simulation_id:
        return None
    
    return Simulation.get_by_id(simulation_id)

def format_api_response(data, status_code=200):
    """Format API response consistently"""
    response = jsonify(data)
    response.status_code = status_code
    return response

def format_number(num):
    """Format number with thousands separator"""
    if num is None:
        return '0'
    return f"{num:,}"

def format_percentage(num, decimals=2):
    """Format percentage with specified decimal places"""
    if num is None:
        return '0.00%'
    return f"{num:.{decimals}f}%"

def generate_color():
    """Generate random color for parties"""
    colors = [
        '#e74c3c', '#3498db', '#2ecc71', '#f39c12', 
        '#9b59b6', '#1abc9c', '#34495e', '#e67e22',
        '#95a5a6', '#f1c40f', '#8e44ad', '#16a085'
    ]
    import random
    return random.choice(colors)
