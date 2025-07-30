# Party routes placeholder
from flask import Blueprint

bp = Blueprint('parties', __name__, url_prefix='/api/parties')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'parties'}
