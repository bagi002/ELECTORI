"""Election models for ELECTORI application."""
from sqlalchemy.orm import validates
from datetime import datetime, date
import enum
from extensions import db


class ElectionType(enum.Enum):
    PARLIAMENTARY = "parliamentary"
    MUNICIPAL = "municipal"
    PRESIDENTIAL = "presidential"


class ElectionStatus(enum.Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class CandidacyType(enum.Enum):
    PARTY = "party"
    COALITION = "coalition"


class Election(db.Model):
    """Election model - represents an election event."""
    
    __tablename__ = 'elections'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(ElectionType), nullable=False)
    election_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(ElectionStatus), nullable=False, default=ElectionStatus.SCHEDULED)
    census_threshold = db.Column(db.Float, nullable=True, default=0.0)  # For parliamentary and municipal
    round_number = db.Column(db.Integer, nullable=False, default=1)  # For presidential (1 or 2)
    
    # Relationships
    candidacies = db.relationship('Candidacy', backref='election', lazy=True, cascade='all, delete-orphan')
    election_results = db.relationship('ElectionResult', backref='election', lazy=True, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('census_threshold >= 0 AND census_threshold <= 50', name='check_census_threshold_range'),
        db.CheckConstraint('round_number IN (1, 2)', name='check_round_number'),
    )
    
    @validates('census_threshold')
    def validate_census_threshold(self, key, census_threshold):
        """Validate census threshold is between 0 and 50."""
        if census_threshold is not None and (census_threshold < 0 or census_threshold > 50):
            raise ValueError("Census threshold must be between 0 and 50")
        return census_threshold
    
    @validates('round_number')
    def validate_round_number(self, key, round_number):
        """Validate round number is 1 or 2."""
        if round_number not in (1, 2):
            raise ValueError("Round number must be 1 or 2")
        return round_number
    
    def __repr__(self):
        return f'<Election {self.name}: {self.type.value} on {self.election_date}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'name': self.name,
            'type': self.type.value if self.type else None,
            'election_date': self.election_date.isoformat() if self.election_date else None,
            'status': self.status.value if self.status else None,
            'census_threshold': self.census_threshold,
            'round_number': self.round_number
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, name, election_type, election_date, census_threshold=None, round_number=1):
        """Create a new election."""
        election = cls(
            simulation_id=simulation_id,
            name=name,
            type=election_type,
            election_date=election_date,
            census_threshold=census_threshold,
            round_number=round_number
        )
        db.session.add(election)
        db.session.commit()
        return election
    
    @classmethod
    def get_by_id(cls, election_id):
        """Get election by ID."""
        return cls.query.get(election_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id):
        """Get all elections for a simulation."""
        return cls.query.filter_by(simulation_id=simulation_id).all()
    
    def update(self, **kwargs):
        """Update election attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the election."""
        db.session.delete(self)
        db.session.commit()


class Candidacy(db.Model):
    """Candidacy model - represents a candidacy (party or coalition) in an election."""
    
    __tablename__ = 'candidacies'
    
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(CandidacyType), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)  # For municipal elections
    
    # Relationships
    memberships = db.relationship('CandidacyMembership', backref='candidacy', lazy=True, cascade='all, delete-orphan')
    election_results = db.relationship('ElectionResult', backref='candidacy', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Candidacy {self.name}: {self.type.value}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'election_id': self.election_id,
            'name': self.name,
            'type': self.type.value if self.type else None,
            'city_id': self.city_id
        }
    
    # CRUD operations
    @classmethod
    def create(cls, election_id, name, candidacy_type, city_id=None):
        """Create a new candidacy."""
        candidacy = cls(
            election_id=election_id,
            name=name,
            type=candidacy_type,
            city_id=city_id
        )
        db.session.add(candidacy)
        db.session.commit()
        return candidacy
    
    @classmethod
    def get_by_id(cls, candidacy_id):
        """Get candidacy by ID."""
        return cls.query.get(candidacy_id)
    
    @classmethod
    def get_by_election(cls, election_id):
        """Get all candidacies for an election."""
        return cls.query.filter_by(election_id=election_id).all()
    
    def update(self, **kwargs):
        """Update candidacy attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the candidacy."""
        db.session.delete(self)
        db.session.commit()


class CandidacyMembership(db.Model):
    """CandidacyMembership model - represents party membership in a candidacy."""
    
    __tablename__ = 'candidacy_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    candidacy_id = db.Column(db.Integer, db.ForeignKey('candidacies.id'), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    is_lead_party = db.Column(db.Boolean, nullable=False, default=False)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('candidacy_id', 'party_id', name='uq_candidacy_party_membership'),
    )
    
    def __repr__(self):
        lead_status = "Lead" if self.is_lead_party else "Member"
        return f'<CandidacyMembership {self.party.name} in {self.candidacy.name}: {lead_status}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'candidacy_id': self.candidacy_id,
            'party_id': self.party_id,
            'is_lead_party': self.is_lead_party
        }
    
    # CRUD operations
    @classmethod
    def create(cls, candidacy_id, party_id, is_lead_party=False):
        """Create a new candidacy membership."""
        membership = cls(
            candidacy_id=candidacy_id,
            party_id=party_id,
            is_lead_party=is_lead_party
        )
        db.session.add(membership)
        db.session.commit()
        return membership
    
    @classmethod
    def get_by_id(cls, membership_id):
        """Get candidacy membership by ID."""
        return cls.query.get(membership_id)
    
    @classmethod
    def get_by_candidacy(cls, candidacy_id):
        """Get all memberships for a candidacy."""
        return cls.query.filter_by(candidacy_id=candidacy_id).all()
    
    def update(self, **kwargs):
        """Update membership attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the candidacy membership."""
        db.session.delete(self)
        db.session.commit()


class ElectionResult(db.Model):
    """ElectionResult model - represents election results for a candidacy in a city."""
    
    __tablename__ = 'election_results'
    
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    candidacy_id = db.Column(db.Integer, db.ForeignKey('candidacies.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)  # Nullable for national results
    votes_count = db.Column(db.Integer, nullable=False, default=0)
    vote_percentage = db.Column(db.Float, nullable=False, default=0.0)
    seats_won = db.Column(db.Integer, nullable=True, default=0)  # For parliamentary elections
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('election_id', 'candidacy_id', 'city_id', name='uq_election_result_per_city'),
        db.CheckConstraint('votes_count >= 0', name='check_votes_count_positive'),
        db.CheckConstraint('vote_percentage >= 0 AND vote_percentage <= 100', name='check_vote_percentage_range'),
        db.CheckConstraint('seats_won >= 0', name='check_seats_won_positive'),
    )
    
    @validates('votes_count')
    def validate_votes_count(self, key, votes_count):
        """Validate votes count is non-negative."""
        if votes_count < 0:
            raise ValueError("Votes count must be non-negative")
        return votes_count
    
    @validates('vote_percentage')
    def validate_vote_percentage(self, key, vote_percentage):
        """Validate vote percentage is between 0 and 100."""
        if vote_percentage < 0 or vote_percentage > 100:
            raise ValueError("Vote percentage must be between 0 and 100")
        return vote_percentage
    
    @validates('seats_won')
    def validate_seats_won(self, key, seats_won):
        """Validate seats won is non-negative."""
        if seats_won is not None and seats_won < 0:
            raise ValueError("Seats won must be non-negative")
        return seats_won
    
    def __repr__(self):
        return f'<ElectionResult {self.candidacy.name}: {self.vote_percentage}% ({self.votes_count} votes)>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'election_id': self.election_id,
            'candidacy_id': self.candidacy_id,
            'city_id': self.city_id,
            'votes_count': self.votes_count,
            'vote_percentage': self.vote_percentage,
            'seats_won': self.seats_won
        }
    
    # CRUD operations
    @classmethod
    def create(cls, election_id, candidacy_id, votes_count, vote_percentage, city_id=None, seats_won=None):
        """Create a new election result."""
        result = cls(
            election_id=election_id,
            candidacy_id=candidacy_id,
            city_id=city_id,
            votes_count=votes_count,
            vote_percentage=vote_percentage,
            seats_won=seats_won
        )
        db.session.add(result)
        db.session.commit()
        return result
    
    @classmethod
    def get_by_id(cls, result_id):
        """Get election result by ID."""
        return cls.query.get(result_id)
    
    @classmethod
    def get_by_election(cls, election_id):
        """Get all results for an election."""
        return cls.query.filter_by(election_id=election_id).all()
    
    @classmethod
    def get_by_city(cls, city_id, election_id):
        """Get all results for a city in an election."""
        return cls.query.filter_by(city_id=city_id, election_id=election_id).all()
    
    def update(self, **kwargs):
        """Update election result attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the election result."""
        db.session.delete(self)
        db.session.commit()