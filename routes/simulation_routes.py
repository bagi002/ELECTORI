# Simulation routes - CRUD operations for simulations
from flask import Blueprint, request, jsonify, session, current_app
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.simulation import Simulation
from utils.validators import validate_simulation_data

bp = Blueprint('simulations', __name__, url_prefix='/api/simulations')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'simulations'}

@bp.route('', methods=['GET'])
def get_simulations():
    """Get all simulations"""
    try:
        simulations = Simulation.query.all()
        return jsonify([sim.to_dict() for sim in simulations])
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju simulacija', 'details': str(e)}), 500

@bp.route('/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get specific simulation by ID"""
    try:
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulacija nije pronađena'}), 404
        return jsonify(simulation.to_dict())
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju simulacije', 'details': str(e)}), 500

@bp.route('', methods=['POST'])
def create_simulation():
    """Create new simulation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nedostaju podaci'}), 400
            
        # Validate input data
        errors = validate_simulation_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Create new simulation
        simulation = Simulation(
            name=data['name'],
            country_name=data['country_name']
        )
        
        db.session.add(simulation)
        db.session.commit()
        
        # Set as active simulation in session
        session['active_simulation_id'] = simulation.id
        
        return jsonify(simulation.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Simulacija sa tim imenom već postoji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri kreiranju simulacije', 'details': str(e)}), 500

@bp.route('/<int:simulation_id>', methods=['PUT'])
def update_simulation(simulation_id):
    """Update existing simulation"""
    try:
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulacija nije pronađena'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nedostaju podaci'}), 400
            
        # Validate input data
        errors = validate_simulation_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Update simulation
        simulation.update(**data)
        db.session.commit()
        
        return jsonify(simulation.to_dict())
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Simulacija sa tim imenom već postoji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri ažuriranju simulacije', 'details': str(e)}), 500

@bp.route('/<int:simulation_id>', methods=['DELETE'])
def delete_simulation(simulation_id):
    """Delete simulation"""
    try:
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulacija nije pronađena'}), 404
            
        # Clear active simulation from session if it's being deleted
        if session.get('active_simulation_id') == simulation_id:
            session.pop('active_simulation_id', None)
            
        simulation.delete()
        db.session.commit()
        
        return jsonify({'message': 'Simulacija je uspešno obrisana'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri brisanju simulacije', 'details': str(e)}), 500

@bp.route('/<int:simulation_id>/activate', methods=['POST'])
def activate_simulation(simulation_id):
    """Set simulation as active in session"""
    try:
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulacija nije pronađena'}), 404
            
        # Update last_played timestamp
        simulation.update()  # No parameters - just updates last_played
        db.session.commit()
        
        # Set as active simulation
        session['active_simulation_id'] = simulation_id
        
        return jsonify({
            'message': 'Simulacija je aktivirana',
            'simulation': simulation.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri aktiviranju simulacije', 'details': str(e)}), 500

@bp.route('/active', methods=['GET'])
def get_active_simulation():
    """Get currently active simulation from session"""
    try:
        active_id = session.get('active_simulation_id')
        if not active_id:
            return jsonify({'message': 'Nema aktivne simulacije'}), 404
            
        simulation = Simulation.get_by_id(active_id)
        if not simulation:
            # Clean up invalid session data
            session.pop('active_simulation_id', None)
            return jsonify({'error': 'Aktivna simulacija nije pronađena'}), 404
            
        return jsonify(simulation.to_dict())
        
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju aktivne simulacije', 'details': str(e)}), 500
