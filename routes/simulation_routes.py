# Simulation routes placeholder
from flask import Blueprint

bp = Blueprint('simulations', __name__, url_prefix='/api/simulations')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'simulations'}
