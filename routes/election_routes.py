"""Election routes for ELECTORI application."""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime, date
from models.election import Election, Candidacy, CandidacyMembership, ElectionResult, ElectionType, ElectionStatus, CandidacyType
from models.simulation import Simulation
from models.party import Party
from models.city import City
from utils.validators import validate_required_fields
from utils.helpers import get_active_simulation, format_api_response
from extensions import db

bp = Blueprint('elections', __name__, url_prefix='/api/elections')


@bp.route('/', methods=['GET'])
def get_elections():
    """Get all elections for the active simulation."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        elections = Election.get_by_simulation(simulation.id)
        return jsonify({
            'elections': [election.to_dict() for election in elections],
            'total': len(elections)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
def create_election():
    """Create a new election."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'type', 'election_date']
        if not validate_required_fields(data, required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse election type
        try:
            election_type = ElectionType(data['type'])
        except ValueError:
            return jsonify({'error': 'Invalid election type'}), 400
        
        # Parse election date
        try:
            election_date = datetime.strptime(data['election_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate census threshold for parliamentary and municipal elections
        census_threshold = data.get('census_threshold', 0.0)
        if election_type in [ElectionType.PARLIAMENTARY, ElectionType.MUNICIPAL]:
            if not (0 <= census_threshold <= 50):
                return jsonify({'error': 'Census threshold must be between 0 and 50'}), 400
        
        # Create election
        election = Election.create(
            simulation_id=simulation.id,
            name=data['name'],
            election_type=election_type,
            election_date=election_date,
            census_threshold=census_threshold,
            round_number=data.get('round_number', 1)
        )
        
        return jsonify(election.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>', methods=['GET'])
def get_election(election_id):
    """Get a specific election."""
    try:
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        # Get candidacies with their party memberships
        candidacies_data = []
        for candidacy in election.candidacies:
            candidacy_dict = candidacy.to_dict()
            candidacy_dict['parties'] = []
            for membership in candidacy.memberships:
                party = Party.get_by_id(membership.party_id)
                if party:
                    candidacy_dict['parties'].append({
                        'id': party.id,
                        'name': party.name,
                        'color': party.color,
                        'is_lead_party': membership.is_lead_party
                    })
            candidacies_data.append(candidacy_dict)
        
        election_dict = election.to_dict()
        election_dict['candidacies'] = candidacies_data
        
        return jsonify(election_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>', methods=['PUT'])
def update_election(election_id):
    """Update an election."""
    try:
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        data = request.get_json()
        
        # Parse and validate data
        update_data = {}
        
        if 'name' in data:
            update_data['name'] = data['name']
        
        if 'type' in data:
            try:
                update_data['type'] = ElectionType(data['type'])
            except ValueError:
                return jsonify({'error': 'Invalid election type'}), 400
        
        if 'election_date' in data:
            try:
                update_data['election_date'] = datetime.strptime(data['election_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if 'status' in data:
            try:
                update_data['status'] = ElectionStatus(data['status'])
            except ValueError:
                return jsonify({'error': 'Invalid election status'}), 400
        
        if 'census_threshold' in data:
            census_threshold = data['census_threshold']
            if not (0 <= census_threshold <= 50):
                return jsonify({'error': 'Census threshold must be between 0 and 50'}), 400
            update_data['census_threshold'] = census_threshold
        
        if 'round_number' in data:
            round_number = data['round_number']
            if round_number not in (1, 2):
                return jsonify({'error': 'Round number must be 1 or 2'}), 400
            update_data['round_number'] = round_number
        
        # Update election
        election.update(**update_data)
        
        return jsonify(election.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    """Delete an election."""
    try:
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        election.delete()
        return jsonify({'message': 'Election deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>/candidacies', methods=['GET'])
def get_candidacies(election_id):
    """Get all candidacies for an election."""
    try:
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        candidacies = Candidacy.get_by_election(election_id)
        candidacies_data = []
        
        for candidacy in candidacies:
            candidacy_dict = candidacy.to_dict()
            candidacy_dict['parties'] = []
            for membership in candidacy.memberships:
                party = Party.get_by_id(membership.party_id)
                if party:
                    candidacy_dict['parties'].append({
                        'id': party.id,
                        'name': party.name,
                        'color': party.color,
                        'is_lead_party': membership.is_lead_party
                    })
            candidacies_data.append(candidacy_dict)
        
        return jsonify({
            'candidacies': candidacies_data,
            'total': len(candidacies_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>/candidacies', methods=['POST'])
def create_candidacy(election_id):
    """Create a new candidacy for an election."""
    try:
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'type', 'party_ids']
        if not validate_required_fields(data, required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse candidacy type
        try:
            candidacy_type = CandidacyType(data['type'])
        except ValueError:
            return jsonify({'error': 'Invalid candidacy type'}), 400
        
        # Validate party IDs
        party_ids = data['party_ids']
        if not isinstance(party_ids, list) or len(party_ids) == 0:
            return jsonify({'error': 'At least one party must be specified'}), 400
        
        # For single party candidacies, only one party allowed
        if candidacy_type == CandidacyType.PARTY and len(party_ids) > 1:
            return jsonify({'error': 'Single party candidacy can only have one party'}), 400
        
        # Check if all parties exist
        simulation = get_active_simulation()
        parties = []
        for party_id in party_ids:
            party = Party.get_by_id(party_id)
            if not party or party.simulation_id != simulation.id:
                return jsonify({'error': f'Party with ID {party_id} not found'}), 400
            parties.append(party)
        
        # Create candidacy
        candidacy = Candidacy.create(
            election_id=election_id,
            name=data['name'],
            candidacy_type=candidacy_type,
            city_id=data.get('city_id')
        )
        
        # Create party memberships
        lead_party_id = data.get('lead_party_id', party_ids[0])
        for i, party_id in enumerate(party_ids):
            is_lead = (party_id == lead_party_id)
            CandidacyMembership.create(
                candidacy_id=candidacy.id,
                party_id=party_id,
                is_lead_party=is_lead
            )
        
        # Return candidacy with party information
        candidacy_dict = candidacy.to_dict()
        candidacy_dict['parties'] = []
        for membership in candidacy.memberships:
            party = Party.get_by_id(membership.party_id)
            if party:
                candidacy_dict['parties'].append({
                    'id': party.id,
                    'name': party.name,
                    'color': party.color,
                    'is_lead_party': membership.is_lead_party
                })
        
        return jsonify(candidacy_dict), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:election_id>/candidacies/<int:candidacy_id>', methods=['DELETE'])
def delete_candidacy(election_id, candidacy_id):
    """Delete a candidacy."""
    try:
        candidacy = Candidacy.get_by_id(candidacy_id)
        if not candidacy or candidacy.election_id != election_id:
            return jsonify({'error': 'Candidacy not found'}), 404
        
        candidacy.delete()
        return jsonify({'message': 'Candidacy deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/types', methods=['GET'])
def get_election_types():
    """Get all available election types."""
    return jsonify({
        'types': [{'value': t.value, 'label': t.value.title()} for t in ElectionType]
    })


@bp.route('/statuses', methods=['GET'])
def get_election_statuses():
    """Get all available election statuses."""
    return jsonify({
        'statuses': [{'value': s.value, 'label': s.value.title()} for s in ElectionStatus]
    })


@bp.route('/<int:election_id>/available-parties', methods=['GET'])
def get_available_parties(election_id):
    """Get parties available for candidacy in an election."""
    try:
        simulation = get_active_simulation()
        if not simulation:
            return jsonify({'error': 'No active simulation'}), 400
        
        # Get all parties in simulation
        parties = Party.get_by_simulation(simulation.id)
        
        # Get parties already in candidacies for this election
        election = Election.get_by_id(election_id)
        if not election:
            return jsonify({'error': 'Election not found'}), 404
        
        used_party_ids = set()
        for candidacy in election.candidacies:
            for membership in candidacy.memberships:
                used_party_ids.add(membership.party_id)
        
        # Filter out already used parties
        available_parties = [
            party.to_dict() for party in parties 
            if party.id not in used_party_ids
        ]
        
        return jsonify({
            'parties': available_parties,
            'total': len(available_parties)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500