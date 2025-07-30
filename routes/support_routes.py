"""Support routes for ELECTORI application."""
from flask import Blueprint, jsonify, request, session
from sqlalchemy import func
from models import PartySupport, Party, City, Simulation
from extensions import db
import logging

logger = logging.getLogger(__name__)

support_bp = Blueprint('support', __name__, url_prefix='/api/support')


@support_bp.route('/matrix', methods=['GET'])
def get_support_matrix():
    """Get support matrix for all parties and cities in active simulation."""
    try:
        # Get active simulation
        active_sim_id = session.get('active_simulation_id')
        if not active_sim_id:
            return jsonify({'error': 'No active simulation selected'}), 400
        
        # Get all parties and cities for the simulation
        parties = Party.query.filter_by(simulation_id=active_sim_id).all()
        cities = City.query.filter_by(simulation_id=active_sim_id).all()
        
        # Build matrix data
        matrix_data = {
            'simulation_id': active_sim_id,
            'parties': [p.to_dict() for p in parties],
            'cities': [c.to_dict() for c in cities],
            'support_matrix': {}
        }
        
        # Get all support data
        supports = PartySupport.query.join(Party).filter(
            Party.simulation_id == active_sim_id
        ).all()
        
        # Organize support data by party and city
        for support in supports:
            party_id = str(support.party_id)
            city_id = str(support.city_id)
            
            if party_id not in matrix_data['support_matrix']:
                matrix_data['support_matrix'][party_id] = {}
            
            matrix_data['support_matrix'][party_id][city_id] = {
                'support_percentage': support.support_percentage,
                'last_updated': support.last_updated.isoformat() if support.last_updated else None,
                'support_id': support.id
            }
        
        # Fill in missing entries with 0%
        for party in parties:
            party_id = str(party.id)
            if party_id not in matrix_data['support_matrix']:
                matrix_data['support_matrix'][party_id] = {}
            
            for city in cities:
                city_id = str(city.id)
                if city_id not in matrix_data['support_matrix'][party_id]:
                    matrix_data['support_matrix'][party_id][city_id] = {
                        'support_percentage': 0.0,
                        'last_updated': None,
                        'support_id': None
                    }
        
        return jsonify(matrix_data)
        
    except Exception as e:
        logger.error(f"Error getting support matrix: {str(e)}")
        return jsonify({'error': 'Failed to retrieve support matrix'}), 500


@support_bp.route('/matrix/validate', methods=['POST'])
def validate_support_matrix():
    """Validate support matrix to ensure city totals don't exceed 100%."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        support_matrix = data.get('support_matrix', {})
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'city_totals': {}
        }
        
        # Calculate totals by city
        cities_totals = {}
        for party_id, cities_data in support_matrix.items():
            for city_id, support_data in cities_data.items():
                support_percentage = support_data.get('support_percentage', 0)
                if city_id not in cities_totals:
                    cities_totals[city_id] = 0
                cities_totals[city_id] += support_percentage
        
        # Validate each city total
        for city_id, total in cities_totals.items():
            validation_result['city_totals'][city_id] = total
            
            if total > 100:
                validation_result['valid'] = False
                validation_result['errors'].append({
                    'city_id': city_id,
                    'message': f'Total support exceeds 100% ({total:.1f}%)',
                    'total': total
                })
            elif total > 95:
                validation_result['warnings'].append({
                    'city_id': city_id,
                    'message': f'Total support is very high ({total:.1f}%)',
                    'total': total
                })
        
        return jsonify(validation_result)
        
    except Exception as e:
        logger.error(f"Error validating support matrix: {str(e)}")
        return jsonify({'error': 'Failed to validate support matrix'}), 500


@support_bp.route('/matrix/normalize', methods=['POST'])
def normalize_support_matrix():
    """Auto-normalize support matrix for cities exceeding 100%."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        support_matrix = data.get('support_matrix', {})
        normalization_options = data.get('options', {})
        
        # Options for normalization
        preserve_zero = normalization_options.get('preserve_zero', True)
        min_support = normalization_options.get('min_support', 0.1)
        
        normalized_matrix = {}
        normalization_log = []
        
        # Calculate city totals first
        cities_totals = {}
        for party_id, cities_data in support_matrix.items():
            for city_id, support_data in cities_data.items():
                support_percentage = support_data.get('support_percentage', 0)
                if city_id not in cities_totals:
                    cities_totals[city_id] = 0
                cities_totals[city_id] += support_percentage
        
        # Normalize cities that exceed 100%
        for city_id, total in cities_totals.items():
            if total > 100:
                # Calculate normalization factor
                normalization_factor = 100.0 / total
                
                normalization_log.append({
                    'city_id': city_id,
                    'original_total': total,
                    'normalization_factor': normalization_factor,
                    'normalized_total': 100.0
                })
                
                # Apply normalization to all parties for this city
                for party_id, cities_data in support_matrix.items():
                    if party_id not in normalized_matrix:
                        normalized_matrix[party_id] = {}
                    
                    if city_id in cities_data:
                        original_support = cities_data[city_id].get('support_percentage', 0)
                        
                        if preserve_zero and original_support == 0:
                            normalized_support = 0
                        else:
                            normalized_support = original_support * normalization_factor
                            if normalized_support < min_support and original_support > 0:
                                normalized_support = min_support
                        
                        normalized_matrix[party_id][city_id] = {
                            **cities_data[city_id],
                            'support_percentage': round(normalized_support, 2),
                            'original_support': original_support,
                            'normalized': True
                        }
                    else:
                        normalized_matrix[party_id][city_id] = {
                            'support_percentage': 0,
                            'original_support': 0,
                            'normalized': False
                        }
            else:
                # City doesn't need normalization, copy as-is
                for party_id, cities_data in support_matrix.items():
                    if party_id not in normalized_matrix:
                        normalized_matrix[party_id] = {}
                    
                    if city_id in cities_data:
                        normalized_matrix[party_id][city_id] = {
                            **cities_data[city_id],
                            'normalized': False
                        }
                    else:
                        normalized_matrix[party_id][city_id] = {
                            'support_percentage': 0,
                            'normalized': False
                        }
        
        return jsonify({
            'normalized_matrix': normalized_matrix,
            'normalization_log': normalization_log,
            'options_used': normalization_options
        })
        
    except Exception as e:
        logger.error(f"Error normalizing support matrix: {str(e)}")
        return jsonify({'error': 'Failed to normalize support matrix'}), 500


@support_bp.route('/update', methods=['POST'])
def update_support():
    """Update party support for a specific party-city combination."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['party_id', 'city_id', 'support_percentage']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        party_id = data['party_id']
        city_id = data['city_id']
        support_percentage = data['support_percentage']
        
        # Validate support percentage
        if not (0 <= support_percentage <= 100):
            return jsonify({'error': 'Support percentage must be between 0 and 100'}), 400
        
        # Check if party and city exist and belong to active simulation
        active_sim_id = session.get('active_simulation_id')
        if not active_sim_id:
            return jsonify({'error': 'No active simulation selected'}), 400
        
        party = Party.query.filter_by(id=party_id, simulation_id=active_sim_id).first()
        if not party:
            return jsonify({'error': 'Party not found in active simulation'}), 404
        
        city = City.query.filter_by(id=city_id, simulation_id=active_sim_id).first()
        if not city:
            return jsonify({'error': 'City not found in active simulation'}), 404
        
        # Find existing support record or create new one
        support = PartySupport.query.filter_by(party_id=party_id, city_id=city_id).first()
        
        if support:
            # Update existing support
            old_percentage = support.support_percentage
            support.update(support_percentage)
            action = 'updated'
        else:
            # Create new support record
            support = PartySupport.create(party_id, city_id, support_percentage)
            old_percentage = 0
            action = 'created'
        
        # Calculate new city total
        city_total = db.session.query(func.sum(PartySupport.support_percentage)).filter_by(city_id=city_id).scalar() or 0
        
        return jsonify({
            'success': True,
            'action': action,
            'support': support.to_dict(),
            'old_percentage': old_percentage,
            'new_percentage': support_percentage,
            'city_total': float(city_total),
            'city_total_valid': city_total <= 100
        })
        
    except Exception as e:
        logger.error(f"Error updating support: {str(e)}")
        return jsonify({'error': 'Failed to update support'}), 500


@support_bp.route('/bulk-update', methods=['POST'])
def bulk_update_support():
    """Bulk update multiple support values."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        updates = data.get('updates', [])
        if not updates:
            return jsonify({'error': 'No updates provided'}), 400
        
        active_sim_id = session.get('active_simulation_id')
        if not active_sim_id:
            return jsonify({'error': 'No active simulation selected'}), 400
        
        results = []
        errors = []
        
        # Process each update
        for update in updates:
            try:
                party_id = update.get('party_id')
                city_id = update.get('city_id')
                support_percentage = update.get('support_percentage')
                
                # Validate required fields
                if not all([party_id is not None, city_id is not None, support_percentage is not None]):
                    errors.append({
                        'update': update,
                        'error': 'Missing required fields'
                    })
                    continue
                
                # Validate support percentage
                if not (0 <= support_percentage <= 100):
                    errors.append({
                        'update': update,
                        'error': 'Support percentage must be between 0 and 100'
                    })
                    continue
                
                # Check if party and city exist
                party = Party.query.filter_by(id=party_id, simulation_id=active_sim_id).first()
                city = City.query.filter_by(id=city_id, simulation_id=active_sim_id).first()
                
                if not party or not city:
                    errors.append({
                        'update': update,
                        'error': 'Party or city not found'
                    })
                    continue
                
                # Update or create support
                support = PartySupport.query.filter_by(party_id=party_id, city_id=city_id).first()
                
                if support:
                    old_percentage = support.support_percentage
                    support.update(support_percentage)
                    action = 'updated'
                else:
                    support = PartySupport.create(party_id, city_id, support_percentage)
                    old_percentage = 0
                    action = 'created'
                
                results.append({
                    'party_id': party_id,
                    'city_id': city_id,
                    'action': action,
                    'old_percentage': old_percentage,
                    'new_percentage': support_percentage
                })
                
            except Exception as e:
                errors.append({
                    'update': update,
                    'error': str(e)
                })
        
        return jsonify({
            'success': len(errors) == 0,
            'results': results,
            'errors': errors,
            'total_updates': len(updates),
            'successful_updates': len(results),
            'failed_updates': len(errors)
        })
        
    except Exception as e:
        logger.error(f"Error bulk updating support: {str(e)}")
        return jsonify({'error': 'Failed to bulk update support'}), 500


@support_bp.route('/city/<int:city_id>/total', methods=['GET'])
def get_city_support_total(city_id):
    """Get total support percentage for a specific city."""
    try:
        active_sim_id = session.get('active_simulation_id')
        if not active_sim_id:
            return jsonify({'error': 'No active simulation selected'}), 400
        
        # Verify city exists in active simulation
        city = City.query.filter_by(id=city_id, simulation_id=active_sim_id).first()
        if not city:
            return jsonify({'error': 'City not found in active simulation'}), 404
        
        # Calculate total support
        total_support = db.session.query(func.sum(PartySupport.support_percentage)).filter_by(city_id=city_id).scalar() or 0
        
        # Get individual party supports
        supports = PartySupport.query.filter_by(city_id=city_id).join(Party).filter(
            Party.simulation_id == active_sim_id
        ).all()
        
        party_supports = [
            {
                'party_id': s.party_id,
                'party_name': s.party.name,
                'support_percentage': s.support_percentage,
                'last_updated': s.last_updated.isoformat() if s.last_updated else None
            }
            for s in supports
        ]
        
        return jsonify({
            'city_id': city_id,
            'city_name': city.name,
            'total_support': float(total_support),
            'is_valid': total_support <= 100,
            'remaining_support': max(0, 100 - total_support),
            'party_supports': party_supports
        })
        
    except Exception as e:
        logger.error(f"Error getting city support total: {str(e)}")
        return jsonify({'error': 'Failed to get city support total'}), 500


@support_bp.route('/analytics/summary', methods=['GET'])
def get_support_analytics_summary():
    """Get summary analytics for support data."""
    try:
        active_sim_id = session.get('active_simulation_id')
        if not active_sim_id:
            return jsonify({'error': 'No active simulation selected'}), 400
        
        # Get basic counts
        parties_count = Party.query.filter_by(simulation_id=active_sim_id).count()
        cities_count = City.query.filter_by(simulation_id=active_sim_id).count()
        supports_count = PartySupport.query.join(Party).filter(Party.simulation_id == active_sim_id).count()
        
        # Get party totals
        party_totals = db.session.query(
            Party.id,
            Party.name,
            Party.color,
            func.sum(PartySupport.support_percentage).label('total_support'),
            func.count(PartySupport.id).label('cities_count')
        ).join(PartySupport, Party.id == PartySupport.party_id, isouter=True).filter(
            Party.simulation_id == active_sim_id
        ).group_by(Party.id).all()
        
        # Get city totals
        city_totals = db.session.query(
            City.id,
            City.name,
            City.population,
            func.sum(PartySupport.support_percentage).label('total_support'),
            func.count(PartySupport.id).label('parties_count')
        ).join(PartySupport, City.id == PartySupport.city_id, isouter=True).filter(
            City.simulation_id == active_sim_id
        ).group_by(City.id).all()
        
        # Calculate statistics
        valid_cities = sum(1 for city in city_totals if (city.total_support or 0) <= 100)
        invalid_cities = cities_count - valid_cities
        
        return jsonify({
            'summary': {
                'parties_count': parties_count,
                'cities_count': cities_count,
                'supports_count': supports_count,
                'valid_cities': valid_cities,
                'invalid_cities': invalid_cities,
                'completion_percentage': (supports_count / (parties_count * cities_count) * 100) if parties_count * cities_count > 0 else 0
            },
            'party_analytics': [
                {
                    'party_id': p.id,
                    'party_name': p.name,
                    'party_color': p.color,
                    'total_support': float(p.total_support or 0),
                    'cities_with_support': p.cities_count or 0,
                    'average_support': float((p.total_support or 0) / max(1, p.cities_count or 1))
                }
                for p in party_totals
            ],
            'city_analytics': [
                {
                    'city_id': c.id,
                    'city_name': c.name,
                    'city_population': c.population,
                    'total_support': float(c.total_support or 0),
                    'parties_with_support': c.parties_count or 0,
                    'is_valid': (c.total_support or 0) <= 100,
                    'remaining_support': max(0, 100 - (c.total_support or 0))
                }
                for c in city_totals
            ]
        })
        
    except Exception as e:
        logger.error(f"Error getting support analytics summary: {str(e)}")
        return jsonify({'error': 'Failed to get support analytics summary'}), 500