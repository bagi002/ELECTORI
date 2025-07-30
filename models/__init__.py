"""
Models package for ELECTORI application.

This package contains all the SQLAlchemy models for the application.
All models are properly initialized with the database instance from the Flask app.
"""

from .simulation import Simulation
from .city import City
from .party import Party, PartySupport
from .election import Election, Candidacy, CandidacyMembership, ElectionResult
from .parliament import MP, ParliamentCoalition, Law, Vote

__all__ = [
    'Simulation',
    'City',
    'Party',
    'PartySupport',
    'Election',
    'Candidacy',
    'CandidacyMembership',
    'ElectionResult',
    'MP',
    'ParliamentCoalition',
    'Law',
    'Vote'
]