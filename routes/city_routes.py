# City routes - CRUD operations for cities
from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.city import City
from models.simulation import Simulation
from utils.validators import validate_city_data

bp = Blueprint('cities', __name__, url_prefix='/api/cities')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'cities'}

def get_active_simulation_id():
    """Helper function to get active simulation ID"""
    simulation_id = session.get('active_simulation_id')
    if not simulation_id:
        return None
    return simulation_id

@bp.route('', methods=['GET'])
def get_cities():
    """Get all cities for active simulation"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        cities = City.query.filter_by(simulation_id=simulation_id).all()
        return jsonify([city.to_dict() for city in cities])
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju gradova', 'details': str(e)}), 500

@bp.route('/<int:city_id>', methods=['GET'])
def get_city(city_id):
    """Get specific city by ID"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        city = City.get_by_id(city_id)
        if not city or city.simulation_id != simulation_id:
            return jsonify({'error': 'Grad nije pronađen'}), 404
        return jsonify(city.to_dict())
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju grada', 'details': str(e)}), 500

@bp.route('', methods=['POST'])
def create_city():
    """Create new city in active simulation"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        # Verify simulation exists
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulacija nije pronađena'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nedostaju podaci'}), 400
            
        # Validate input data
        errors = validate_city_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Create new city
        city = City(
            simulation_id=simulation_id,
            name=data['name'],
            population=data['population'],
            coordinates_x=data.get('coordinates_x'),
            coordinates_y=data.get('coordinates_y')
        )
        
        db.session.add(city)
        db.session.commit()
        
        return jsonify(city.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Grad sa tim imenom već postoji u ovoj simulaciji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri kreiranju grada', 'details': str(e)}), 500

@bp.route('/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    """Update existing city"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        city = City.get_by_id(city_id)
        if not city or city.simulation_id != simulation_id:
            return jsonify({'error': 'Grad nije pronađen'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nedostaju podaci'}), 400
            
        # Validate input data
        errors = validate_city_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Update city
        city.update(**data)
        db.session.commit()
        
        return jsonify(city.to_dict())
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Grad sa tim imenom već postoji u ovoj simulaciji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri ažuriranju grada', 'details': str(e)}), 500

@bp.route('/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete city"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        city = City.get_by_id(city_id)
        if not city or city.simulation_id != simulation_id:
            return jsonify({'error': 'Grad nije pronađen'}), 404
            
        # Check if city has dependencies (party support, elections, etc.)
        if city.party_supports:
            return jsonify({'error': 'Grad se ne može obrisati jer ima povezane podatke o podršci partija'}), 400
            
        city.delete()
        db.session.commit()
        
        return jsonify({'message': 'Grad je uspešno obrisan'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri brisanju grada', 'details': str(e)}), 500

@bp.route('/<int:city_id>/stats', methods=['GET'])
def get_city_stats(city_id):
    """Get city statistics including party support"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        city = City.get_by_id(city_id)
        if not city or city.simulation_id != simulation_id:
            return jsonify({'error': 'Grad nije pronađen'}), 404
            
        city_dict = city.to_dict()
        city_dict['total_party_support'] = city.get_total_support()
        city_dict['party_supports'] = [support.to_dict() for support in city.party_supports]
        
        return jsonify(city_dict)
        
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju statistika grada', 'details': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_cities():
    """Search cities by name"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Potreban je upit za pretragu'}), 400
            
        cities = City.query.filter(
            City.simulation_id == simulation_id,
            City.name.ilike(f'%{query}%')
        ).all()
        
        return jsonify([city.to_dict() for city in cities])
        
    except Exception as e:
        return jsonify({'error': 'Greška pri pretragama gradova', 'details': str(e)}), 500
