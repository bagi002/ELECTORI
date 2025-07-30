"""
Test API endpoints for ELECTORI application.
Tests the CRUD operations for simulations, cities, and parties.
"""

import pytest
import json
from datetime import datetime, date
from app import create_app, db
from models.simulation import Simulation, SimulationStatus
from models.city import City
from models.party import Party, PartyIdeology


@pytest.fixture
def app():
    """Create test app."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_simulation(app):
    """Create a sample simulation for testing."""
    with app.app_context():
        simulation = Simulation(
            name="Test Simulation",
            country_name="Test Country"
        )
        db.session.add(simulation)
        db.session.commit()
        simulation_id = simulation.id
        db.session.expunge(simulation)  # Remove from session
        return simulation_id


@pytest.fixture
def sample_city(app, sample_simulation):
    """Create a sample city for testing."""
    with app.app_context():
        city = City(
            simulation_id=sample_simulation,
            name="Test City",
            population=100000
        )
        db.session.add(city)
        db.session.commit()
        city_id = city.id
        db.session.expunge(city)  # Remove from session
        return city_id


@pytest.fixture
def sample_party(app, sample_simulation):
    """Create a sample party for testing."""
    with app.app_context():
        party = Party(
            simulation_id=sample_simulation,
            name="Test Party",
            color="#FF0000",
            ideology=PartyIdeology.CENTER,
            leader_name="Test Leader"
        )
        db.session.add(party)
        db.session.commit()
        party_id = party.id
        db.session.expunge(party)  # Remove from session
        return party_id


class TestSimulationAPI:
    """Test simulation API endpoints."""
    
    def test_get_simulations_empty(self, client):
        """Test getting simulations when none exist."""
        response = client.get('/api/simulations')
        assert response.status_code == 200
        assert response.json == []
    
    def test_get_simulations_with_data(self, client, sample_simulation):
        """Test getting simulations with data."""
        response = client.get('/api/simulations')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test Simulation'
    
    def test_get_simulation_by_id(self, client, sample_simulation):
        """Test getting specific simulation by ID."""
        response = client.get(f'/api/simulations/{sample_simulation}')
        assert response.status_code == 200
        assert response.json['name'] == 'Test Simulation'
        assert response.json['country_name'] == 'Test Country'
    
    def test_get_simulation_not_found(self, client):
        """Test getting non-existent simulation."""
        response = client.get('/api/simulations/999')
        assert response.status_code == 404
        assert 'nije pronađena' in response.json['error']
    
    def test_create_simulation(self, client):
        """Test creating new simulation."""
        data = {
            'name': 'New Simulation',
            'country_name': 'New Country'
        }
        response = client.post('/api/simulations', 
                              data=json.dumps(data), 
                              content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'New Simulation'
        assert response.json['country_name'] == 'New Country'
    
    def test_create_simulation_validation_error(self, client):
        """Test creating simulation with validation errors."""
        data = {'name': ''}  # Missing country_name and empty name
        response = client.post('/api/simulations', 
                              data=json.dumps(data), 
                              content_type='application/json')
        assert response.status_code == 400
        assert 'Validacijska greška' in response.json['error']
    
    def test_create_simulation_duplicate_name(self, client, sample_simulation):
        """Test creating simulation with duplicate name."""
        data = {
            'name': 'Test Simulation',  # Same as existing
            'country_name': 'Different Country'
        }
        response = client.post('/api/simulations', 
                              data=json.dumps(data), 
                              content_type='application/json')
        assert response.status_code == 400
        assert 'već postoji' in response.json['error']
    
    def test_update_simulation(self, client, sample_simulation):
        """Test updating simulation."""
        data = {
            'name': 'Updated Simulation',
            'country_name': 'Updated Country'
        }
        response = client.put(f'/api/simulations/{sample_simulation}',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Simulation'
    
    def test_delete_simulation(self, client, sample_simulation):
        """Test deleting simulation."""
        response = client.delete(f'/api/simulations/{sample_simulation}')
        assert response.status_code == 200
        assert 'uspešno obrisana' in response.json['message']
        
        # Verify deletion
        response = client.get(f'/api/simulations/{sample_simulation}')
        assert response.status_code == 404
    
    def test_activate_simulation(self, client, sample_simulation):
        """Test activating simulation."""
        response = client.post(f'/api/simulations/{sample_simulation}/activate')
        assert response.status_code == 200
        assert 'aktivirana' in response.json['message']
        
        # Verify active simulation
        response = client.get('/api/simulations/active')
        assert response.status_code == 200
        assert response.json['id'] == sample_simulation
    
    def test_get_active_simulation_none(self, client):
        """Test getting active simulation when none is set."""
        response = client.get('/api/simulations/active')
        assert response.status_code == 404
        assert 'Nema aktivne simulacije' in response.json['message']


class TestCityAPI:
    """Test city API endpoints."""
    
    def test_get_cities_no_active_simulation(self, client):
        """Test getting cities without active simulation."""
        response = client.get('/api/cities')
        assert response.status_code == 400
        assert 'Nema aktivne simulacije' in response.json['error']
    
    def test_get_cities_with_active_simulation(self, client, sample_simulation, sample_city):
        """Test getting cities with active simulation."""
        # Set active simulation
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get('/api/cities')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test City'
    
    def test_get_city_by_id(self, client, sample_simulation, sample_city):
        """Test getting specific city."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get(f'/api/cities/{sample_city}')
        assert response.status_code == 200
        assert response.json['name'] == 'Test City'
        assert response.json['population'] == 100000
    
    def test_create_city(self, client, sample_simulation):
        """Test creating new city."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {
            'name': 'New City',
            'population': 50000,
            'coordinates_x': 10.5,
            'coordinates_y': 20.3
        }
        response = client.post('/api/cities',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'New City'
        assert response.json['population'] == 50000
    
    def test_create_city_validation_error(self, client, sample_simulation):
        """Test creating city with validation error."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {'population': 50}  # Too small, missing name
        response = client.post('/api/cities',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 400
        assert 'Validacijska greška' in response.json['error']
    
    def test_update_city(self, client, sample_simulation, sample_city):
        """Test updating city."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {
            'name': 'Updated City',
            'population': 150000
        }
        response = client.put(f'/api/cities/{sample_city}',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'Updated City'
        assert response.json['population'] == 150000
    
    def test_delete_city(self, client, sample_simulation, sample_city):
        """Test deleting city."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.delete(f'/api/cities/{sample_city}')
        assert response.status_code == 200
        assert 'uspešno obrisan' in response.json['message']
    
    def test_get_city_stats(self, client, sample_simulation, sample_city):
        """Test getting city statistics."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get(f'/api/cities/{sample_city}/stats')
        assert response.status_code == 200
        assert 'total_party_support' in response.json
        assert 'party_supports' in response.json
    
    def test_search_cities(self, client, sample_simulation, sample_city):
        """Test searching cities."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get('/api/cities/search?q=Test')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test City'


class TestPartyAPI:
    """Test party API endpoints."""
    
    def test_get_parties_no_active_simulation(self, client):
        """Test getting parties without active simulation."""
        response = client.get('/api/parties')
        assert response.status_code == 400
        assert 'Nema aktivne simulacije' in response.json['error']
    
    def test_get_parties_with_active_simulation(self, client, sample_simulation, sample_party):
        """Test getting parties with active simulation."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get('/api/parties')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test Party'
    
    def test_get_party_by_id(self, client, sample_simulation, sample_party):
        """Test getting specific party."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get(f'/api/parties/{sample_party}')
        assert response.status_code == 200
        assert response.json['name'] == 'Test Party'
        assert response.json['color'] == '#FF0000'
    
    def test_create_party(self, client, sample_simulation):
        """Test creating new party."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {
            'name': 'New Party',
            'color': '#00FF00',
            'ideology': 'levi',
            'leader_name': 'New Leader',
            'description': 'Test party description'
        }
        response = client.post('/api/parties',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'New Party'
        assert response.json['color'] == '#00FF00'
    
    def test_create_party_validation_error(self, client, sample_simulation):
        """Test creating party with validation error."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {'name': ''}  # Empty name, missing color
        response = client.post('/api/parties',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 400
        assert 'Validacijska greška' in response.json['error']
    
    def test_update_party(self, client, sample_simulation, sample_party):
        """Test updating party."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {
            'name': 'Updated Party',
            'color': '#0000FF',
            'leader_name': 'Updated Leader'
        }
        response = client.put(f'/api/parties/{sample_party}',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Party'
        assert response.json['color'] == '#0000FF'
    
    def test_delete_party(self, client, sample_simulation, sample_party):
        """Test deleting party."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.delete(f'/api/parties/{sample_party}')
        assert response.status_code == 200
        assert 'uspešno obrisana' in response.json['message']
    
    def test_get_party_support(self, client, sample_simulation, sample_party):
        """Test getting party support."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get(f'/api/parties/{sample_party}/support')
        assert response.status_code == 200
        assert 'party' in response.json
        assert 'support_data' in response.json
        assert 'average_support' in response.json
    
    def test_search_parties(self, client, sample_simulation, sample_party):
        """Test searching parties."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.get('/api/parties/search?q=Test')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test Party'
    
    def test_get_ideologies(self, client):
        """Test getting available ideologies."""
        response = client.get('/api/parties/ideologies')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert 'centar' in response.json


class TestAPIErrorHandling:
    """Test API error handling."""
    
    def test_invalid_json(self, client, sample_simulation):
        """Test handling invalid JSON."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        response = client.post('/api/cities',
                              data='invalid json',
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_missing_content_type(self, client, sample_simulation):
        """Test handling missing content type."""
        with client.session_transaction() as sess:
            sess['active_simulation_id'] = sample_simulation
        
        data = {'name': 'Test', 'population': 1000}
        response = client.post('/api/cities',
                              data=json.dumps(data))
        # Without content-type header, Flask may not parse JSON correctly
        assert response.status_code in [400, 500]  # Allow both error types
    
    def test_health_endpoints(self, client):
        """Test health check endpoints."""
        endpoints = [
            '/api/simulations/health',
            '/api/cities/health',
            '/api/parties/health'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            assert response.json['status'] == 'ok'


class TestWorkflowIntegration:
    """Test API workflow integration."""
    
    def test_complete_workflow(self, client):
        """Test complete workflow: create simulation, create city and party."""
        # Create simulation
        sim_data = {
            'name': 'Workflow Test',
            'country_name': 'Test Country'
        }
        response = client.post('/api/simulations',
                              data=json.dumps(sim_data),
                              content_type='application/json')
        assert response.status_code == 201
        simulation_id = response.json['id']
        
        # Activate simulation
        response = client.post(f'/api/simulations/{simulation_id}/activate')
        assert response.status_code == 200
        
        # Create city
        city_data = {
            'name': 'Workflow City',
            'population': 75000
        }
        response = client.post('/api/cities',
                              data=json.dumps(city_data),
                              content_type='application/json')
        assert response.status_code == 201
        city_id = response.json['id']
        
        # Create party
        party_data = {
            'name': 'Workflow Party',
            'color': '#FF00FF',
            'ideology': 'desni'
        }
        response = client.post('/api/parties',
                              data=json.dumps(party_data),
                              content_type='application/json')
        assert response.status_code == 201
        party_id = response.json['id']
        
        # Verify all created correctly
        response = client.get('/api/simulations/active')
        assert response.status_code == 200
        assert response.json['name'] == 'Workflow Test'
        
        response = client.get('/api/cities')
        assert response.status_code == 200
        assert len(response.json) == 1
        
        response = client.get('/api/parties')
        assert response.status_code == 200
        assert len(response.json) == 1