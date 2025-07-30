"""
Seed data script for ELECTORI application.

This script provides sample data for testing all the models and their relationships.
"""

from datetime import datetime, date
from app import create_app, db
from models import (
    Simulation, City, Party, PartySupport, Election, Candidacy, 
    CandidacyMembership, ElectionResult, MP, ParliamentCoalition, Law, Vote
)
from models.simulation import SimulationStatus
from models.party import PartyIdeology
from models.election import ElectionType, ElectionStatus, CandidacyType
from models.parliament import ParliamentType, LawStatus, VoteType


def clear_all_data():
    """Clear all data from the database."""
    try:
        # Clear in reverse order of dependencies
        Vote.query.delete()
        Law.query.delete()
        ParliamentCoalition.query.delete()
        MP.query.delete()
        ElectionResult.query.delete()
        CandidacyMembership.query.delete()
        Candidacy.query.delete()
        Election.query.delete()
        PartySupport.query.delete()
        Party.query.delete()
        City.query.delete()
        Simulation.query.delete()
        
        db.session.commit()
        print("All existing data cleared.")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing data: {e}")


def create_sample_simulation():
    """Create a sample simulation with all related data."""
    print("Creating sample simulation...")
    
    # Create simulation
    simulation = Simulation.create(
        name="Srbija 2025",
        country_name="Republika Srbija"
    )
    print(f"Created simulation: {simulation.name}")
    
    # Create cities
    cities = [
        City.create(simulation.id, "Beograd", 1700000, 44.8125, 20.4612),
        City.create(simulation.id, "Novi Sad", 350000, 45.2671, 19.8335),
        City.create(simulation.id, "Niš", 260000, 43.3209, 21.8958),
        City.create(simulation.id, "Kragujevac", 180000, 44.0131, 20.9253),
        City.create(simulation.id, "Subotica", 105000, 46.1008, 19.6677)
    ]
    print(f"Created {len(cities)} cities")
    
    # Create parties
    parties = [
        Party.create(
            simulation.id, "Srpska napredna stranka", "#0066CC", 
            PartyIdeology.CENTER_RIGHT, "Aleksandar Vučić", 
            date(2008, 9, 21), "Centralno-desna stranka, naslednica Srpskog pokreta obnove"
        ),
        Party.create(
            simulation.id, "Demokratska stranka", "#FFD700", 
            PartyIdeology.CENTER, "Zoran Lutovac",
            date(1989, 2, 3), "Centralna demokratska stranka osnovana 1989."
        ),
        Party.create(
            simulation.id, "Socijalistička partija Srbije", "#FF0000", 
            PartyIdeology.LEFT, "Ivica Dačić",
            date(1990, 7, 27), "Socijalistička partija, naslednica SK Srbije"
        ),
        Party.create(
            simulation.id, "Ne davimo Beograd", "#00CC66", 
            PartyIdeology.LEFT, "Radomir Lazović",
            date(2014, 3, 15), "Ekološka i građanska organizacija"
        ),
        Party.create(
            simulation.id, "Srpska radikalna stranka", "#000080", 
            PartyIdeology.RIGHT, "Vojislav Šešelj",
            date(1991, 2, 23), "Nacionalna radikalna stranka"
        )
    ]
    print(f"Created {len(parties)} parties")
    
    # Create party support in cities
    support_data = [
        # Belgrade
        (parties[0].id, cities[0].id, 35.0),  # SNS
        (parties[1].id, cities[0].id, 25.0),  # DS
        (parties[2].id, cities[0].id, 15.0),  # SPS
        (parties[3].id, cities[0].id, 15.0),  # NDB
        (parties[4].id, cities[0].id, 10.0),  # SRS
        
        # Novi Sad
        (parties[0].id, cities[1].id, 40.0),  # SNS
        (parties[1].id, cities[1].id, 30.0),  # DS
        (parties[2].id, cities[1].id, 12.0),  # SPS
        (parties[3].id, cities[1].id, 10.0),  # NDB
        (parties[4].id, cities[1].id, 8.0),   # SRS
        
        # Niš
        (parties[0].id, cities[2].id, 45.0),  # SNS
        (parties[1].id, cities[2].id, 20.0),  # DS
        (parties[2].id, cities[2].id, 20.0),  # SPS
        (parties[3].id, cities[2].id, 8.0),   # NDB
        (parties[4].id, cities[2].id, 7.0),   # SRS
        
        # Kragujevac
        (parties[0].id, cities[3].id, 42.0),  # SNS
        (parties[1].id, cities[3].id, 22.0),  # DS
        (parties[2].id, cities[3].id, 18.0),  # SPS
        (parties[3].id, cities[3].id, 10.0),  # NDB
        (parties[4].id, cities[3].id, 8.0),   # SRS
        
        # Subotica
        (parties[0].id, cities[4].id, 38.0),  # SNS
        (parties[1].id, cities[4].id, 28.0),  # DS
        (parties[2].id, cities[4].id, 14.0),  # SPS
        (parties[3].id, cities[4].id, 12.0),  # NDB
        (parties[4].id, cities[4].id, 8.0),   # SRS
    ]
    
    supports = []
    for party_id, city_id, percentage in support_data:
        support = PartySupport.create(party_id, city_id, percentage)
        supports.append(support)
    print(f"Created {len(supports)} party support records")
    
    # Create an election
    election = Election.create(
        simulation.id,
        "Parlamentarni izbori 2025",
        ElectionType.PARLIAMENTARY,
        date(2025, 12, 15),
        census_threshold=3.0
    )
    print(f"Created election: {election.name}")
    
    # Create candidacies
    candidacies = []
    for party in parties:
        candidacy = Candidacy.create(
            election.id,
            party.name,
            CandidacyType.PARTY
        )
        candidacies.append(candidacy)
        
        # Create candidacy membership
        CandidacyMembership.create(candidacy.id, party.id, is_lead_party=True)
    
    print(f"Created {len(candidacies)} candidacies")
    
    # Create MPs (based on imaginary election results)
    mp_distribution = [
        (parties[0], 65),  # SNS
        (parties[1], 45),  # DS
        (parties[2], 25),  # SPS
        (parties[3], 15),  # NDB
        (parties[4], 0),   # SRS (below census)
    ]
    
    mps = []
    mp_counter = 1
    for party, seats in mp_distribution:
        for i in range(seats):
            mp = MP.create(
                simulation.id,
                party.id,
                f"Poslanik {mp_counter}",
                ParliamentType.NATIONAL,
                date(2024, 6, 15),
                city_id=cities[i % len(cities)].id  # Distribute across cities
            )
            mps.append(mp)
            mp_counter += 1
    
    print(f"Created {len(mps)} MPs")
    
    # Create a coalition
    coalition = ParliamentCoalition.create(
        simulation.id,
        "Koalicija za promene",
        ParliamentType.NATIONAL,
        date(2024, 7, 1)
    )
    print(f"Created coalition: {coalition.name}")
    
    # Create some laws
    laws = [
        Law.create(
            simulation.id,
            "Zakon o digitalnoj upravi",
            parties[0].id,
            ParliamentType.NATIONAL,
            date(2024, 8, 1),
            description="Zakon koji reguliše digitalizaciju javne uprave"
        ),
        Law.create(
            simulation.id,
            "Zakon o zaštiti životne sredine",
            parties[3].id,
            ParliamentType.NATIONAL,
            date(2024, 8, 15),
            description="Zakon za poboljšanje zaštite životne sredine"
        ),
        Law.create(
            simulation.id,
            "Budžet Beograda za 2025",
            parties[1].id,
            ParliamentType.MUNICIPAL,
            date(2024, 9, 1),
            city_id=cities[0].id,
            description="Budžet grada Beograda za 2025. godinu"
        )
    ]
    print(f"Created {len(laws)} laws")
    
    # Create some votes on the first law
    votes = []
    law = laws[0]
    law.status = LawStatus.VOTING
    law.voting_date = date(2024, 8, 10)
    
    # Vote by party affiliation (simplified)
    vote_count = 0
    for mp in mps[:20]:  # First 20 MPs vote
        if mp.party_id == parties[0].id:  # SNS votes FOR
            vote_type = VoteType.FOR
        elif mp.party_id == parties[3].id:  # NDB votes AGAINST
            vote_type = VoteType.AGAINST
        else:  # Others abstain
            vote_type = VoteType.ABSTAIN
            
        vote = Vote.create(law.id, mp.id, vote_type, datetime(2024, 8, 10, 14, 30))
        votes.append(vote)
        vote_count += 1
    
    print(f"Created {len(votes)} votes")
    
    return {
        'simulation': simulation,
        'cities': cities,
        'parties': parties,
        'supports': supports,
        'election': election,
        'candidacies': candidacies,
        'mps': mps,
        'coalition': coalition,
        'laws': laws,
        'votes': votes
    }


def create_minimal_test_data():
    """Create minimal test data for basic testing."""
    print("Creating minimal test data...")
    
    # Create a simple simulation
    simulation = Simulation.create("Test Simulacija", "Test Država")
    
    # Create one city
    city = City.create(simulation.id, "Test Grad", 500000)
    
    # Create one party
    party = Party.create(
        simulation.id, "Test Partija", "#FF0000", 
        PartyIdeology.CENTER, "Test Lider"
    )
    
    # Create party support
    support = PartySupport.create(party.id, city.id, 50.0)
    
    print("Minimal test data created successfully!")
    return {
        'simulation': simulation,
        'city': city,
        'party': party,
        'support': support
    }


def verify_data_integrity():
    """Verify the integrity of created data."""
    print("\nVerifying data integrity...")
    
    # Check simulations
    simulations = Simulation.get_all()
    print(f"✓ {len(simulations)} simulations created")
    
    # Check cities
    cities = City.query.all()
    print(f"✓ {len(cities)} cities created")
    
    # Check parties
    parties = Party.query.all()
    print(f"✓ {len(parties)} parties created")
    
    # Check party supports
    supports = PartySupport.query.all()
    print(f"✓ {len(supports)} party support records created")
    
    # Verify support totals per city
    for city in cities:
        total_support = city.get_total_support()
        print(f"  - {city.name}: {total_support}% total support")
        if abs(total_support - 100.0) > 0.1:
            print(f"    ⚠️  Warning: Support doesn't add up to 100%")
    
    # Check elections
    elections = Election.query.all()
    print(f"✓ {len(elections)} elections created")
    
    # Check MPs
    mps = MP.query.all()
    print(f"✓ {len(mps)} MPs created")
    
    # Check laws
    laws = Law.query.all()
    print(f"✓ {len(laws)} laws created")
    
    # Check votes
    votes = Vote.query.all()
    print(f"✓ {len(votes)} votes created")
    
    # Test some relationships
    if simulations:
        sim = simulations[0]
        print(f"✓ Simulation '{sim.name}' has {len(sim.cities)} cities")
        print(f"✓ Simulation '{sim.name}' has {len(sim.parties)} parties")
    
    print("Data integrity verification completed!")


def seed_database(full_data=True):
    """
    Main function to seed the database with sample data.
    
    Args:
        full_data (bool): If True, creates comprehensive sample data.
                         If False, creates minimal test data.
    """
    app = create_app()
    
    with app.app_context():
        print("Starting database seeding...")
        
        # Clear existing data
        clear_all_data()
        
        # Create sample data
        if full_data:
            data = create_sample_simulation()
        else:
            data = create_minimal_test_data()
        
        # Verify data integrity
        verify_data_integrity()
        
        print("\n✅ Database seeding completed successfully!")
        return data


if __name__ == '__main__':
    """
    Command-line interface for seeding the database.
    
    Usage:
        python seed_data.py           - Create full sample data
        python seed_data.py minimal   - Create minimal test data
    """
    import sys
    
    full_data = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'minimal':
        full_data = False
    
    seed_database(full_data=full_data)