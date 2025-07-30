"""
Unit tests for ELECTORI models.

This module contains comprehensive unit tests for all models including:
- Model creation and validation
- CRUD operations
- Relationships
- Constraints and validations
- Business logic
"""

import pytest
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from models import (
    Simulation, City, Party, PartySupport, Election, Candidacy, 
    CandidacyMembership, ElectionResult, MP, ParliamentCoalition, Law, Vote
)
from models.simulation import SimulationStatus
from models.party import PartyIdeology
from models.election import ElectionType, ElectionStatus, CandidacyType
from models.parliament import ParliamentType, LawStatus, VoteType


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


class TestSimulation:
    """Test cases for Simulation model."""
    
    def test_create_simulation(self, app):
        """Test creating a new simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Sim", "Test Nation")
            
            assert simulation.id is not None
            assert simulation.name == "Test Sim"
            assert simulation.country_name == "Test Nation"
            assert simulation.status == SimulationStatus.ACTIVE
            assert simulation.created_at is not None
            assert simulation.last_played is None
    
    def test_simulation_unique_name(self, app):
        """Test that simulation names must be unique."""
        with app.app_context():
            Simulation.create("Unique Name", "Country1")
            
            with pytest.raises(IntegrityError):
                Simulation.create("Unique Name", "Country2")
    
    def test_simulation_to_dict(self, app):
        """Test simulation serialization to dictionary."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            data = simulation.to_dict()
            
            assert data['id'] == simulation.id
            assert data['name'] == simulation.name
            assert data['country_name'] == simulation.country_name
            assert data['status'] == simulation.status.value
    
    def test_simulation_update(self, app):
        """Test updating simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            simulation.update(status=SimulationStatus.PAUSED)
            
            assert simulation.status == SimulationStatus.PAUSED
            assert simulation.last_played is not None
    
    def test_simulation_delete(self, app):
        """Test deleting simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            sim_id = simulation.id
            simulation.delete()
            
            assert Simulation.get_by_id(sim_id) is None


class TestCity:
    """Test cases for City model."""
    
    def test_create_city(self, app):
        """Test creating a new city."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "New City", 250000)
            
            assert city.id is not None
            assert city.name == "New City"
            assert city.population == 250000
            assert city.simulation_id == simulation.id
    
    def test_city_population_validation(self, app):
        """Test city population validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Test minimum population
            with pytest.raises(ValueError):
                City.create(simulation.id, "Too Small", 50)
            
            # Test maximum population
            with pytest.raises(ValueError):
                City.create(simulation.id, "Too Big", 20000000)
    
    def test_city_unique_name_per_simulation(self, app):
        """Test that city names must be unique within a simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            City.create(simulation.id, "City Name", 100000)
            
            with pytest.raises(IntegrityError):
                City.create(simulation.id, "City Name", 200000)
    
    def test_city_coordinates(self, app):
        """Test city with coordinates."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Located City", 300000, 44.8, 20.4)
            
            assert city.coordinates_x == 44.8
            assert city.coordinates_y == 20.4
    
    def test_city_get_total_support(self, app):
        """Test getting total party support in city."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000, 45.0, 20.0)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            PartySupport.create(party.id, city.id, 35.0)
            
            total_support = city.get_total_support()
            assert total_support == 35.0


class TestParty:
    """Test cases for Party model."""
    
    def test_create_party(self, app):
        """Test creating a new party."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id,
                "New Party",
                "#00FF00",
                PartyIdeology.LEFT,
                "Party Leader",
                description="A test party"
            )
            
            assert party.id is not None
            assert party.name == "New Party"
            assert party.color == "#00FF00"
            assert party.ideology == PartyIdeology.LEFT
            assert party.leader_name == "Party Leader"
            assert party.description == "A test party"
    
    def test_party_color_validation(self, app):
        """Test party color validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Valid hex color
            party = Party.create(
                simulation.id, "Valid Color", "#123ABC", 
                PartyIdeology.CENTER, "Leader"
            )
            assert party.color == "#123ABC"
            
            # Invalid color format
            with pytest.raises(ValueError):
                Party.create(
                    simulation.id, "Invalid Color", "red", 
                    PartyIdeology.CENTER, "Leader"
                )
    
    def test_party_description_length(self, app):
        """Test party description length validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            long_description = "x" * 501
            
            with pytest.raises(ValueError):
                Party.create(
                    simulation.id, "Long Desc", "#FF0000", 
                    PartyIdeology.CENTER, "Leader", description=long_description
                )
    
    def test_party_unique_name_per_simulation(self, app):
        """Test that party names must be unique within a simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            Party.create(
                simulation.id, "Unique Party", "#FF0000", 
                PartyIdeology.CENTER, "Leader1"
            )
            
            with pytest.raises(IntegrityError):
                Party.create(
                    simulation.id, "Unique Party", "#00FF00", 
                    PartyIdeology.LEFT, "Leader2"
                )


class TestPartySupport:
    """Test cases for PartySupport model."""
    
    def test_create_party_support(self, app):
        """Test creating party support."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            support = PartySupport.create(party.id, city.id, 42.5)
            
            assert support.id is not None
            assert support.party_id == party.id
            assert support.city_id == city.id
            assert support.support_percentage == 42.5
            assert support.last_updated is not None
    
    def test_party_support_percentage_validation(self, app):
        """Test party support percentage validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            
            # Test negative percentage
            with pytest.raises(ValueError):
                PartySupport.create(party.id, city.id, -5.0)
            
            # Test percentage over 100
            with pytest.raises(ValueError):
                PartySupport.create(party.id, city.id, 105.0)
    
    def test_party_support_unique_per_city(self, app):
        """Test that party support is unique per city."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            PartySupport.create(party.id, city.id, 30.0)
            
            with pytest.raises(IntegrityError):
                PartySupport.create(party.id, city.id, 40.0)
    
    def test_party_support_update(self, app):
        """Test updating party support."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            support = PartySupport.create(party.id, city.id, 30.0)
            original_time = support.last_updated
            
            support.update(45.0)
            
            assert support.support_percentage == 45.0
            assert support.last_updated > original_time


class TestElection:
    """Test cases for Election model."""
    
    def test_create_election(self, app):
        """Test creating an election."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            election = Election.create(
                simulation.id,
                "Test Election",
                ElectionType.PARLIAMENTARY,
                date(2025, 6, 15),
                census_threshold=5.0
            )
            
            assert election.id is not None
            assert election.name == "Test Election"
            assert election.type == ElectionType.PARLIAMENTARY
            assert election.election_date == date(2025, 6, 15)
            assert election.census_threshold == 5.0
            assert election.status == ElectionStatus.SCHEDULED
    
    def test_election_census_threshold_validation(self, app):
        """Test election census threshold validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Valid threshold
            election = Election.create(
                simulation.id, "Valid", ElectionType.PARLIAMENTARY,
                date(2025, 6, 15), census_threshold=3.0
            )
            assert election.census_threshold == 3.0
            
            # Invalid threshold (too high)
            with pytest.raises(ValueError):
                Election.create(
                    simulation.id, "Invalid", ElectionType.PARLIAMENTARY,
                    date(2025, 6, 15), census_threshold=60.0
                )
    
    def test_election_round_number_validation(self, app):
        """Test election round number validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Valid round number
            election = Election.create(
                simulation.id, "Valid", ElectionType.PRESIDENTIAL,
                date(2025, 6, 15), round_number=2
            )
            assert election.round_number == 2
            
            # Invalid round number
            with pytest.raises(ValueError):
                Election.create(
                    simulation.id, "Invalid", ElectionType.PRESIDENTIAL,
                    date(2025, 6, 15), round_number=3
                )


class TestMP:
    """Test cases for MP model."""
    
    def test_create_mp(self, app):
        """Test creating an MP."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            city = City.create(simulation.id, "Test City", 500000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            mp = MP.create(
                simulation.id,
                party.id,
                "Test MP",
                ParliamentType.NATIONAL,
                date(2024, 6, 15),
                city_id=city.id
            )
            
            assert mp.id is not None
            assert mp.name == "Test MP"
            assert mp.party_id == party.id
            assert mp.city_id == city.id
            assert mp.parliament_type == ParliamentType.NATIONAL
            assert mp.active is True
    
    def test_mp_get_by_simulation(self, app):
        """Test getting MPs by simulation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            mp1 = MP.create(
                simulation.id, party.id, "MP1", 
                ParliamentType.NATIONAL, date(2024, 6, 15)
            )
            mp2 = MP.create(
                simulation.id, party.id, "MP2", 
                ParliamentType.MUNICIPAL, date(2024, 6, 15)
            )
            
            all_mps = MP.get_by_simulation(simulation.id)
            national_mps = MP.get_by_simulation(simulation.id, ParliamentType.NATIONAL)
            
            assert len(all_mps) == 2
            assert len(national_mps) == 1
            assert national_mps[0].name == "MP1"


class TestLaw:
    """Test cases for Law model."""
    
    def test_create_law(self, app):
        """Test creating a law."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            law = Law.create(
                simulation.id,
                "Test Law",
                party.id,
                ParliamentType.NATIONAL,
                date(2024, 8, 1),
                description="A test law"
            )
            
            assert law.id is not None
            assert law.title == "Test Law"
            assert law.proposer_party_id == party.id
            assert law.parliament_type == ParliamentType.NATIONAL
            assert law.status == LawStatus.PROPOSED
    
    def test_law_title_validation(self, app):
        """Test law title length validation."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            long_title = "x" * 201
            
            with pytest.raises(ValueError):
                Law.create(
                    simulation.id, long_title, party.id,
                    ParliamentType.NATIONAL, date(2024, 8, 1)
                )
    
    def test_law_get_vote_counts(self, app):
        """Test getting vote counts for a law."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            law = Law.create(
                simulation.id, "Vote Test Law", party.id,
                ParliamentType.NATIONAL, date(2024, 8, 1)
            )
            
            # Create MPs and votes
            mp1 = MP.create(simulation.id, party.id, "MP1", ParliamentType.NATIONAL, date(2024, 6, 15))
            mp2 = MP.create(simulation.id, party.id, "MP2", ParliamentType.NATIONAL, date(2024, 6, 15))
            mp3 = MP.create(simulation.id, party.id, "MP3", ParliamentType.NATIONAL, date(2024, 6, 15))
            
            Vote.create(law.id, mp1.id, VoteType.FOR)
            Vote.create(law.id, mp2.id, VoteType.FOR)
            Vote.create(law.id, mp3.id, VoteType.AGAINST)
            
            vote_counts = law.get_vote_counts()
            
            assert vote_counts['for'] == 2
            assert vote_counts['against'] == 1
            assert vote_counts['abstain'] == 0
            assert vote_counts['total'] == 3


class TestVote:
    """Test cases for Vote model."""
    
    def test_create_vote(self, app):
        """Test creating a vote."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            law = Law.create(
                simulation.id, "Test Law", party.id,
                ParliamentType.NATIONAL, date(2024, 8, 1)
            )
            mp = MP.create(
                simulation.id, party.id, "Test MP",
                ParliamentType.NATIONAL, date(2024, 6, 15)
            )
            
            vote = Vote.create(law.id, mp.id, VoteType.FOR)
            
            assert vote.id is not None
            assert vote.law_id == law.id
            assert vote.mp_id == mp.id
            assert vote.vote_type == VoteType.FOR
            assert vote.vote_date is not None
    
    def test_vote_unique_per_law_per_mp(self, app):
        """Test that MP can only vote once per law."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            party = Party.create(
                simulation.id, "Test Party", "#FF0000", 
                PartyIdeology.CENTER, "Test Leader"
            )
            law = Law.create(
                simulation.id, "Test Law", party.id,
                ParliamentType.NATIONAL, date(2024, 8, 1)
            )
            mp = MP.create(
                simulation.id, party.id, "Test MP",
                ParliamentType.NATIONAL, date(2024, 6, 15)
            )
            
            Vote.create(law.id, mp.id, VoteType.FOR)
            
            with pytest.raises(IntegrityError):
                Vote.create(law.id, mp.id, VoteType.AGAINST)


class TestRelationships:
    """Test model relationships."""
    
    def test_simulation_relationships(self, app):
        """Test simulation relationships with other models."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Create related objects
            city = City.create(simulation.id, "Test City", 100000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000",
                PartyIdeology.CENTER, "Leader"
            )
            
            # Test relationships
            assert len(simulation.cities) == 1
            assert simulation.cities[0].name == "Test City"
            assert len(simulation.parties) == 1
            assert simulation.parties[0].name == "Test Party"
    
    def test_cascade_delete(self, app):
        """Test cascade delete when simulation is deleted."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Create related objects
            city = City.create(simulation.id, "Test City", 100000)
            party = Party.create(
                simulation.id, "Test Party", "#FF0000",
                PartyIdeology.CENTER, "Leader"
            )
            support = PartySupport.create(party.id, city.id, 50.0)
            
            city_id = city.id
            party_id = party.id
            support_id = support.id
            
            # Delete simulation
            simulation.delete()
            
            # Check that related objects are deleted
            assert City.get_by_id(city_id) is None
            assert Party.get_by_id(party_id) is None
            assert PartySupport.get_by_id(support_id) is None


class TestCRUDOperations:
    """Test CRUD operations for all models."""
    
    def test_simulation_crud(self, app):
        """Test complete CRUD operations for Simulation."""
        with app.app_context():
            # Create
            simulation = Simulation.create("CRUD Test", "CRUD Country")
            assert simulation.id is not None
            
            # Read
            found_sim = Simulation.get_by_id(simulation.id)
            assert found_sim.name == "CRUD Test"
            
            all_sims = Simulation.get_all()
            assert len(all_sims) >= 1
            
            # Update
            simulation.update(country_name="Updated Country")
            assert simulation.country_name == "Updated Country"
            
            # Delete
            sim_id = simulation.id
            simulation.delete()
            assert Simulation.get_by_id(sim_id) is None
    
    def test_city_crud(self, app):
        """Test complete CRUD operations for City."""
        with app.app_context():
            simulation = Simulation.create("Test Simulation", "Test Country")
            
            # Create
            city = City.create(simulation.id, "CRUD City", 300000)
            assert city.id is not None
            
            # Read
            found_city = City.get_by_id(city.id)
            assert found_city.name == "CRUD City"
            
            cities_by_sim = City.get_by_simulation(simulation.id)
            assert len(cities_by_sim) >= 1
            
            # Update
            city.update(population=400000)
            assert city.population == 400000
            
            # Delete
            city_id = city.id
            city.delete()
            assert City.get_by_id(city_id) is None


if __name__ == '__main__':
    pytest.main([__file__])