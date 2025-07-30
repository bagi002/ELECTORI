"""Parliament models for ELECTORI application."""
from sqlalchemy.orm import validates
from datetime import datetime, date
import enum
from app import db


class ParliamentType(enum.Enum):
    NATIONAL = "national"
    MUNICIPAL = "municipal"


class LawStatus(enum.Enum):
    PROPOSED = "proposed"
    VOTING = "voting"
    PASSED = "passed"
    REJECTED = "rejected"


class VoteType(enum.Enum):
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


class MP(db.Model):
    """MP model - represents a Member of Parliament."""
    
    __tablename__ = 'mps'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)  # Nullable for national MPs
    name = db.Column(db.String(50), nullable=False)
    parliament_type = db.Column(db.Enum(ParliamentType), nullable=False)
    elected_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    votes = db.relationship('Vote', backref='mp', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MP {self.name}: {self.party.name} ({self.parliament_type.value})>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'party_id': self.party_id,
            'city_id': self.city_id,
            'name': self.name,
            'parliament_type': self.parliament_type.value if self.parliament_type else None,
            'elected_date': self.elected_date.isoformat() if self.elected_date else None,
            'active': self.active
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, party_id, name, parliament_type, elected_date, city_id=None, active=True):
        """Create a new MP."""
        mp = cls(
            simulation_id=simulation_id,
            party_id=party_id,
            city_id=city_id,
            name=name,
            parliament_type=parliament_type,
            elected_date=elected_date,
            active=active
        )
        db.session.add(mp)
        db.session.commit()
        return mp
    
    @classmethod
    def get_by_id(cls, mp_id):
        """Get MP by ID."""
        return cls.query.get(mp_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id, parliament_type=None, active_only=True):
        """Get MPs for a simulation, optionally filtered by parliament type and active status."""
        query = cls.query.filter_by(simulation_id=simulation_id)
        if parliament_type:
            query = query.filter_by(parliament_type=parliament_type)
        if active_only:
            query = query.filter_by(active=True)
        return query.all()
    
    @classmethod
    def get_by_party(cls, party_id, active_only=True):
        """Get MPs for a party."""
        query = cls.query.filter_by(party_id=party_id)
        if active_only:
            query = query.filter_by(active=True)
        return query.all()
    
    def update(self, **kwargs):
        """Update MP attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the MP."""
        db.session.delete(self)
        db.session.commit()


class ParliamentCoalition(db.Model):
    """ParliamentCoalition model - represents a coalition in parliament."""
    
    __tablename__ = 'parliament_coalitions'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    parliament_type = db.Column(db.Enum(ParliamentType), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)  # For municipal coalitions
    formed_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f'<ParliamentCoalition {self.name}: {self.parliament_type.value}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'name': self.name,
            'parliament_type': self.parliament_type.value if self.parliament_type else None,
            'city_id': self.city_id,
            'formed_date': self.formed_date.isoformat() if self.formed_date else None,
            'active': self.active
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, name, parliament_type, formed_date, city_id=None, active=True):
        """Create a new parliament coalition."""
        coalition = cls(
            simulation_id=simulation_id,
            name=name,
            parliament_type=parliament_type,
            city_id=city_id,
            formed_date=formed_date,
            active=active
        )
        db.session.add(coalition)
        db.session.commit()
        return coalition
    
    @classmethod
    def get_by_id(cls, coalition_id):
        """Get coalition by ID."""
        return cls.query.get(coalition_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id, parliament_type=None, active_only=True):
        """Get coalitions for a simulation."""
        query = cls.query.filter_by(simulation_id=simulation_id)
        if parliament_type:
            query = query.filter_by(parliament_type=parliament_type)
        if active_only:
            query = query.filter_by(active=True)
        return query.all()
    
    def update(self, **kwargs):
        """Update coalition attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the coalition."""
        db.session.delete(self)
        db.session.commit()


class Law(db.Model):
    """Law model - represents a law proposal in parliament."""
    
    __tablename__ = 'laws'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    parliament_type = db.Column(db.Enum(ParliamentType), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)  # For municipal laws
    proposed_date = db.Column(db.Date, nullable=False)
    voting_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum(LawStatus), nullable=False, default=LawStatus.PROPOSED)
    proposer_party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='law', lazy=True, cascade='all, delete-orphan')
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate title length."""
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return title
    
    def __repr__(self):
        return f'<Law {self.title}: {self.status.value}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'title': self.title,
            'description': self.description,
            'parliament_type': self.parliament_type.value if self.parliament_type else None,
            'city_id': self.city_id,
            'proposed_date': self.proposed_date.isoformat() if self.proposed_date else None,
            'voting_date': self.voting_date.isoformat() if self.voting_date else None,
            'status': self.status.value if self.status else None,
            'proposer_party_id': self.proposer_party_id
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, title, proposer_party_id, parliament_type, proposed_date, description=None, city_id=None):
        """Create a new law."""
        law = cls(
            simulation_id=simulation_id,
            title=title,
            description=description,
            parliament_type=parliament_type,
            city_id=city_id,
            proposed_date=proposed_date,
            proposer_party_id=proposer_party_id
        )
        db.session.add(law)
        db.session.commit()
        return law
    
    @classmethod
    def get_by_id(cls, law_id):
        """Get law by ID."""
        return cls.query.get(law_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id, parliament_type=None, status=None):
        """Get laws for a simulation."""
        query = cls.query.filter_by(simulation_id=simulation_id)
        if parliament_type:
            query = query.filter_by(parliament_type=parliament_type)
        if status:
            query = query.filter_by(status=status)
        return query.all()
    
    def update(self, **kwargs):
        """Update law attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the law."""
        db.session.delete(self)
        db.session.commit()
    
    def get_vote_counts(self):
        """Get vote counts for this law."""
        votes_for = Vote.query.filter_by(law_id=self.id, vote_type=VoteType.FOR).count()
        votes_against = Vote.query.filter_by(law_id=self.id, vote_type=VoteType.AGAINST).count()
        votes_abstain = Vote.query.filter_by(law_id=self.id, vote_type=VoteType.ABSTAIN).count()
        
        return {
            'for': votes_for,
            'against': votes_against,
            'abstain': votes_abstain,
            'total': votes_for + votes_against + votes_abstain
        }


class Vote(db.Model):
    """Vote model - represents an MP's vote on a law."""
    
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    law_id = db.Column(db.Integer, db.ForeignKey('laws.id'), nullable=False)
    mp_id = db.Column(db.Integer, db.ForeignKey('mps.id'), nullable=False)
    vote_type = db.Column(db.Enum(VoteType), nullable=False)
    vote_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('law_id', 'mp_id', name='uq_mp_vote_per_law'),
    )
    
    def __repr__(self):
        return f'<Vote {self.mp.name} on {self.law.title}: {self.vote_type.value}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'law_id': self.law_id,
            'mp_id': self.mp_id,
            'vote_type': self.vote_type.value if self.vote_type else None,
            'vote_date': self.vote_date.isoformat() if self.vote_date else None
        }
    
    # CRUD operations
    @classmethod
    def create(cls, law_id, mp_id, vote_type, vote_date=None):
        """Create a new vote."""
        vote = cls(
            law_id=law_id,
            mp_id=mp_id,
            vote_type=vote_type,
            vote_date=vote_date or datetime.utcnow()
        )
        db.session.add(vote)
        db.session.commit()
        return vote
    
    @classmethod
    def get_by_id(cls, vote_id):
        """Get vote by ID."""
        return cls.query.get(vote_id)
    
    @classmethod
    def get_by_law(cls, law_id):
        """Get all votes for a law."""
        return cls.query.filter_by(law_id=law_id).all()
    
    @classmethod
    def get_by_mp(cls, mp_id):
        """Get all votes by an MP."""
        return cls.query.filter_by(mp_id=mp_id).all()
    
    def update(self, vote_type):
        """Update vote type."""
        self.vote_type = vote_type
        self.vote_date = datetime.utcnow()
        db.session.commit()
    
    def delete(self):
        """Delete the vote."""
        db.session.delete(self)
        db.session.commit()