"""Parliament routes for ELECTORI application."""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime, date
import math
from models.parliament import MP, ParliamentCoalition, Law, Vote, ParliamentType, LawStatus, VoteType
from models.simulation import Simulation
from models.party import Party
from models.city import City
from models.election import ElectionResult
from utils.validators import validate_required_fields
from utils.helpers import get_active_simulation, format_api_response
from extensions import db

bp = Blueprint('parliament', __name__, url_prefix='/api/parliament')


@bp.route('/composition', methods=['GET'])
def get_parliament_composition():
    """Get current parliament composition."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        parliament_type = request.args.get('type', 'national')
        city_id = request.args.get('city_id', type=int)
        
        try:
            parliament_type_enum = ParliamentType(parliament_type)
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        # Get MPs
        mps = MP.get_by_simulation(
            simulation.id, 
            parliament_type=parliament_type_enum,
            active_only=True
        )
        
        # Group by party
        composition = {}
        total_seats = 0
        
        for mp in mps:
            party = Party.get_by_id(mp.party_id)
            if party:
                if party.id not in composition:
                    composition[party.id] = {
                        'party': party.to_dict(),
                        'mps': [],
                        'seat_count': 0
                    }
                
                composition[party.id]['mps'].append(mp.to_dict())
                composition[party.id]['seat_count'] += 1
                total_seats += 1
        
        # Calculate percentages
        for party_data in composition.values():
            party_data['percentage'] = (party_data['seat_count'] / total_seats * 100) if total_seats > 0 else 0
        
        # Sort by seat count
        sorted_composition = dict(sorted(
            composition.items(), 
            key=lambda x: x[1]['seat_count'], 
            reverse=True
        ))
        
        return jsonify({
            'composition': sorted_composition,
            'statistics': {
                'total_seats': total_seats,
                'total_parties': len(composition),
                'parliament_type': parliament_type,
                'city_id': city_id,
                'majority_threshold': total_seats // 2 + 1,
                'qualified_majority_threshold': int(total_seats * 2/3)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/mps', methods=['GET'])
def get_mps():
    """Get MPs list with filtering options."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        # Get filters
        parliament_type = request.args.get('type', 'national')
        party_id = request.args.get('party_id', type=int)
        city_id = request.args.get('city_id', type=int)
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        try:
            parliament_type_enum = ParliamentType(parliament_type)
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        # Build query
        query = MP.query.filter_by(
            simulation_id=simulation.id,
            parliament_type=parliament_type_enum
        )
        
        if party_id:
            query = query.filter_by(party_id=party_id)
        
        if city_id:
            query = query.filter_by(city_id=city_id)
        
        if active_only:
            query = query.filter_by(active=True)
        
        mps = query.all()
        
        # Enrich with party and city information
        mps_data = []
        for mp in mps:
            mp_dict = mp.to_dict()
            
            # Add party info
            party = Party.get_by_id(mp.party_id)
            if party:
                mp_dict['party'] = party.to_dict()
            
            # Add city info
            if mp.city_id:
                city = City.get_by_id(mp.city_id)
                if city:
                    mp_dict['city'] = city.to_dict()
            
            mps_data.append(mp_dict)
        
        return jsonify({
            'mps': mps_data,
            'total': len(mps_data),
            'filters': {
                'parliament_type': parliament_type,
                'party_id': party_id,
                'city_id': city_id,
                'active_only': active_only
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/coalitions', methods=['GET'])
def get_coalitions():
    """Get parliament coalitions."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        parliament_type = request.args.get('type', 'national')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        try:
            parliament_type_enum = ParliamentType(parliament_type)
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        coalitions = ParliamentCoalition.get_by_simulation(
            simulation.id,
            parliament_type=parliament_type_enum,
            active_only=active_only
        )
        
        return jsonify({
            'coalitions': [coalition.to_dict() for coalition in coalitions],
            'total': len(coalitions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/coalitions', methods=['POST'])
def create_coalition():
    """Create a new parliament coalition."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'parliament_type', 'formed_date']
        if not validate_required_fields(data, required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse parliament type
        try:
            parliament_type = ParliamentType(data['parliament_type'])
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        # Parse date
        try:
            formed_date = datetime.strptime(data['formed_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create coalition
        coalition = ParliamentCoalition.create(
            simulation_id=simulation.id,
            name=data['name'],
            parliament_type=parliament_type,
            formed_date=formed_date,
            city_id=data.get('city_id'),
            active=data.get('active', True)
        )
        
        return jsonify(coalition.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/laws', methods=['GET'])
def get_laws():
    """Get laws with filtering options."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        parliament_type = request.args.get('type', 'national')
        status = request.args.get('status')
        
        try:
            parliament_type_enum = ParliamentType(parliament_type)
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        status_enum = None
        if status:
            try:
                status_enum = LawStatus(status)
            except ValueError:
                return jsonify({'error': 'Invalid law status'}), 400
        
        laws = Law.get_by_simulation(
            simulation.id,
            parliament_type=parliament_type_enum,
            status=status_enum
        )
        
        # Enrich with proposer party and vote counts
        laws_data = []
        for law in laws:
            law_dict = law.to_dict()
            
            # Add proposer party info
            proposer = Party.get_by_id(law.proposer_party_id)
            if proposer:
                law_dict['proposer_party'] = proposer.to_dict()
            
            # Add vote counts
            law_dict['vote_counts'] = law.get_vote_counts()
            
            laws_data.append(law_dict)
        
        return jsonify({
            'laws': laws_data,
            'total': len(laws_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/laws', methods=['POST'])
def create_law():
    """Create a new law proposal."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'proposer_party_id', 'parliament_type', 'proposed_date']
        if not validate_required_fields(data, required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse parliament type
        try:
            parliament_type = ParliamentType(data['parliament_type'])
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        # Parse date
        try:
            proposed_date = datetime.strptime(data['proposed_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate proposer party
        proposer = Party.get_by_id(data['proposer_party_id'])
        if not proposer or proposer.simulation_id != simulation.id:
            return jsonify({'error': 'Invalid proposer party'}), 400
        
        # Create law
        law = Law.create(
            simulation_id=simulation.id,
            title=data['title'],
            proposer_party_id=data['proposer_party_id'],
            parliament_type=parliament_type,
            proposed_date=proposed_date,
            description=data.get('description'),
            city_id=data.get('city_id')
        )
        
        return jsonify(law.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/hemicycle-data', methods=['GET'])
def get_hemicycle_data():
    """Get data for hemicycle visualization."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        parliament_type = request.args.get('type', 'national')
        
        try:
            parliament_type_enum = ParliamentType(parliament_type)
        except ValueError:
            return jsonify({'error': 'Invalid parliament type'}), 400
        
        # Get MPs grouped by party
        mps = MP.get_by_simulation(
            simulation.id,
            parliament_type=parliament_type_enum,
            active_only=True
        )
        
        # Group by party and prepare hemicycle data
        party_blocks = {}
        total_seats = 0
        
        for mp in mps:
            party = Party.get_by_id(mp.party_id)
            if party:
                if party.id not in party_blocks:
                    party_blocks[party.id] = {
                        'party_name': party.name,
                        'party_color': party.color,
                        'seats': 0,
                        'mps': []
                    }
                
                party_blocks[party.id]['seats'] += 1
                party_blocks[party.id]['mps'].append({
                    'id': mp.id,
                    'name': mp.name
                })
                total_seats += 1
        
        # Sort parties by seat count (largest to smallest)
        sorted_blocks = dict(sorted(
            party_blocks.items(),
            key=lambda x: x[1]['seats'],
            reverse=True
        ))
        
        # Generate seat positions for hemicycle
        seats = []
        seat_index = 0
        
        for party_id, block in sorted_blocks.items():
            for mp in block['mps']:
                # Calculate position in hemicycle
                angle = (seat_index / total_seats) * 180  # Half circle
                row = int(seat_index / 50) + 1  # Multiple rows
                radius = 40 + (row * 12)
                
                x = 50 + (radius * math.cos(math.radians(angle)))
                y = 90 - (radius * math.sin(math.radians(angle)))
                
                seats.append({
                    'id': mp['id'],
                    'name': mp['name'],
                    'party_name': block['party_name'],
                    'party_color': block['party_color'],
                    'x': x,
                    'y': y,
                    'seat_number': seat_index + 1
                })
                
                seat_index += 1
        
        return jsonify({
            'seats': seats,
            'party_blocks': sorted_blocks,
            'statistics': {
                'total_seats': total_seats,
                'total_parties': len(party_blocks),
                'parliament_type': parliament_type
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/generate-from-election/<int:election_id>', methods=['POST'])
def generate_parliament_from_election(election_id):
    """Generate parliament composition from election results."""
    try:
        from models.election import Election, ElectionResult
        
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        if election.type != 'parliamentary':
            return jsonify({'error': 'Only parliamentary elections can generate parliament'}), 400
        
        # Get national election results
        results = ElectionResult.query.filter_by(
            election_id=election_id,
            city_id=None  # National results
        ).all()
        
        if not results:
            return jsonify({'error': 'No election results found'}), 404
        
        # Clear existing MPs for this simulation
        MP.query.filter_by(
            simulation_id=election.simulation_id,
            parliament_type=ParliamentType.NATIONAL
        ).delete()
        
        # Generate MPs based on seat allocation
        mp_count = 0
        for result in results:
            if result.seats_won and result.seats_won > 0:
                candidacy = result.candidacy
                
                # Get parties from candidacy
                for membership in candidacy.memberships:
                    party = Party.get_by_id(membership.party_id)
                    if party:
                        # Calculate seats for this party based on lead status
                        party_seats = result.seats_won if membership.is_lead_party else max(1, result.seats_won // 3)
                        
                        # Generate MPs
                        for i in range(party_seats):
                            mp_name = f"{party.leader_name} {i+1}" if i > 0 else party.leader_name
                            
                            MP.create(
                                simulation_id=election.simulation_id,
                                party_id=party.id,
                                name=mp_name,
                                parliament_type=ParliamentType.NATIONAL,
                                elected_date=election.election_date
                            )
                            mp_count += 1
        
        return jsonify({
            'message': f'Parliament generated with {mp_count} MPs',
            'mps_created': mp_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500