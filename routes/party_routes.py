# Party routes - CRUD operations for parties
from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.party import Party, PartySupport, PartyIdeology
from models.simulation import Simulation
from models.city import City
from utils.validators import validate_party_data
from utils.helpers import generate_color

bp = Blueprint('parties', __name__, url_prefix='/api/parties')

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'module': 'parties'}

def get_active_simulation_id():
    """Helper function to get active simulation ID"""
    simulation_id = session.get('active_simulation_id')
    if not simulation_id:
        return None
    return simulation_id

def convert_ideology_string(ideology_str):
    """Convert ideology string to PartyIdeology enum."""
    ideology_map = {
        'levi': PartyIdeology.LEFT,
        'centar-levi': PartyIdeology.CENTER_LEFT,
        'centar': PartyIdeology.CENTER,
        'centar-desni': PartyIdeology.CENTER_RIGHT,
        'desni': PartyIdeology.RIGHT
    }
    return ideology_map.get(ideology_str, PartyIdeology.CENTER)

@bp.route('', methods=['GET'])
def get_parties():
    """Get all parties for active simulation"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        parties = Party.query.filter_by(simulation_id=simulation_id).all()
        return jsonify([party.to_dict() for party in parties])
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju partija', 'details': str(e)}), 500

@bp.route('/<int:party_id>', methods=['GET'])
def get_party(party_id):
    """Get specific party by ID"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        party = Party.get_by_id(party_id)
        if not party or party.simulation_id != simulation_id:
            return jsonify({'error': 'Partija nije pronađena'}), 404
        return jsonify(party.to_dict())
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju partije', 'details': str(e)}), 500

@bp.route('', methods=['POST'])
def create_party():
    """Create new party in active simulation"""
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
        errors = validate_party_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Generate color if not provided
        if not data.get('color'):
            data['color'] = generate_color()
            
        # Create new party
        party = Party(
            simulation_id=simulation_id,
            name=data['name'],
            color=data['color'],
            ideology=convert_ideology_string(data.get('ideology', 'centar')),
            leader_name=data.get('leader_name', ''),
            founded_date=data.get('founded_date'),
            description=data.get('description', '')
        )
        
        db.session.add(party)
        db.session.commit()
        
        return jsonify(party.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Partija sa tim imenom već postoji u ovoj simulaciji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri kreiranju partije', 'details': str(e)}), 500

@bp.route('/<int:party_id>', methods=['PUT'])
def update_party(party_id):
    """Update existing party"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        party = Party.get_by_id(party_id)
        if not party or party.simulation_id != simulation_id:
            return jsonify({'error': 'Partija nije pronađena'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nedostaju podaci'}), 400
            
        # Validate input data
        errors = validate_party_data(data)
        if errors:
            return jsonify({'error': 'Validacijska greška', 'details': errors}), 400
            
        # Convert ideology if provided
        if 'ideology' in data:
            data['ideology'] = convert_ideology_string(data['ideology'])
            
        # Update party
        party.update(**data)
        db.session.commit()
        
        return jsonify(party.to_dict())
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Partija sa tim imenom već postoji u ovoj simulaciji'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri ažuriranju partije', 'details': str(e)}), 500

@bp.route('/<int:party_id>', methods=['DELETE'])
def delete_party(party_id):
    """Delete party"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        party = Party.get_by_id(party_id)
        if not party or party.simulation_id != simulation_id:
            return jsonify({'error': 'Partija nije pronađena'}), 404
            
        # Check if party has dependencies (support data, candidacies, etc.)
        if party.party_supports or party.candidacy_memberships or party.mps:
            return jsonify({'error': 'Partija se ne može obrisati jer ima povezane podatke'}), 400
            
        party.delete()
        db.session.commit()
        
        return jsonify({'message': 'Partija je uspešno obrisana'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri brisanju partije', 'details': str(e)}), 500

@bp.route('/<int:party_id>/support', methods=['GET'])
def get_party_support(party_id):
    """Get party support across all cities"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        party = Party.get_by_id(party_id)
        if not party or party.simulation_id != simulation_id:
            return jsonify({'error': 'Partija nije pronađena'}), 404
            
        support_data = []
        for support in party.party_supports:
            support_data.append({
                'city_id': support.city_id,
                'city_name': support.city.name,
                'support_percentage': support.support_percentage,
                'last_updated': support.last_updated.isoformat() if support.last_updated else None
            })
            
        return jsonify({
            'party': party.to_dict(),
            'support_data': support_data,
            'average_support': party.get_average_support(),
            'total_support_entries': len(support_data)
        })
        
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju podrške partije', 'details': str(e)}), 500

@bp.route('/<int:party_id>/support/<int:city_id>', methods=['PUT'])
def update_party_support(party_id, city_id):
    """Update party support for specific city"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        party = Party.get_by_id(party_id)
        if not party or party.simulation_id != simulation_id:
            return jsonify({'error': 'Partija nije pronađena'}), 404
            
        city = City.get_by_id(city_id)
        if not city or city.simulation_id != simulation_id:
            return jsonify({'error': 'Grad nije pronađen'}), 404
            
        data = request.get_json()
        if not data or 'support_percentage' not in data:
            return jsonify({'error': 'Nedostaje procenat podrške'}), 400
            
        support_percentage = data['support_percentage']
        if not isinstance(support_percentage, (int, float)) or support_percentage < 0 or support_percentage > 100:
            return jsonify({'error': 'Procenat podrške mora biti između 0 i 100'}), 400
            
        # Find or create party support record
        party_support = PartySupport.query.filter_by(
            party_id=party_id,
            city_id=city_id
        ).first()
        
        if party_support:
            party_support.update(support_percentage)
        else:
            party_support = PartySupport(
                party_id=party_id,
                city_id=city_id,
                support_percentage=support_percentage
            )
            db.session.add(party_support)
            
        db.session.commit()
        
        return jsonify(party_support.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Greška pri ažuriranju podrške partije', 'details': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_parties():
    """Search parties by name"""
    try:
        simulation_id = get_active_simulation_id()
        if not simulation_id:
            return jsonify({'error': 'Nema aktivne simulacije'}), 400
            
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Potreban je upit za pretragu'}), 400
            
        parties = Party.query.filter(
            Party.simulation_id == simulation_id,
            Party.name.ilike(f'%{query}%')
        ).all()
        
        return jsonify([party.to_dict() for party in parties])
        
    except Exception as e:
        return jsonify({'error': 'Greška pri pretragi partija', 'details': str(e)}), 500

@bp.route('/ideologies', methods=['GET'])
def get_ideologies():
    """Get available party ideologies"""
    try:
        from models.party import PartyIdeology
        ideologies = [ideology.value for ideology in PartyIdeology]
        return jsonify(ideologies)
    except Exception as e:
        return jsonify({'error': 'Greška pri dohvaćanju ideologija', 'details': str(e)}), 500
