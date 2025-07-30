# City routes placeholder
from flask import Blueprint

bp = Blueprint('cities', __name__, url_prefix='/api/cities')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'cities'}
