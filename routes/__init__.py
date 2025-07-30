# Routes package for ELECTORI application
from .simulation_routes import bp as simulation_bp
from .city_routes import bp as city_bp
from .party_routes import bp as party_bp

__all__ = [
    'simulation_bp',
    'city_bp', 
    'party_bp'
]
