"""Party models for ELECTORI application."""
from sqlalchemy.orm import validates
from datetime import datetime, date
import enum
import re
from app import db


class PartyIdeology(enum.Enum):
    LEFT = "levi"
    CENTER_LEFT = "centar-levi"
    CENTER = "centar"
    CENTER_RIGHT = "centar-desni"
    RIGHT = "desni"


class Party(db.Model):
    """Party model - represents a political party in a simulation."""
    
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=False)  # Hex color format #RRGGBB
    ideology = db.Column(db.Enum(PartyIdeology), nullable=False)
    leader_name = db.Column(db.String(50), nullable=False)
    founded_date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.Text(500), nullable=True)
    
    # Relationships
    party_supports = db.relationship('PartySupport', backref='party', lazy=True, cascade='all, delete-orphan')
    candidacy_memberships = db.relationship('CandidacyMembership', backref='party', lazy=True)
    mps = db.relationship('MP', backref='party', lazy=True)
    proposed_laws = db.relationship('Law', backref='proposer_party', lazy=True)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('simulation_id', 'name', name='uq_party_name_per_simulation'),
    )
    
    @validates('color')
    def validate_color(self, key, color):
        """Validate color is in hex format."""
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            raise ValueError("Color must be in hex format (#RRGGBB)")
        return color
    
    @validates('description')
    def validate_description(self, key, description):
        """Validate description length."""
        if description and len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")
        return description
    
    def __repr__(self):
        return f'<Party {self.name}: {self.ideology.value}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'name': self.name,
            'color': self.color,
            'ideology': self.ideology.value if self.ideology else None,
            'leader_name': self.leader_name,
            'founded_date': self.founded_date.isoformat() if self.founded_date else None,
            'description': self.description
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, name, color, ideology, leader_name, founded_date=None, description=None):
        """Create a new party."""
        party = cls(
            simulation_id=simulation_id,
            name=name,
            color=color,
            ideology=ideology,
            leader_name=leader_name,
            founded_date=founded_date or date.today(),
            description=description
        )
        db.session.add(party)
        db.session.commit()
        return party
    
    @classmethod
    def get_by_id(cls, party_id):
        """Get party by ID."""
        return cls.query.get(party_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id):
        """Get all parties for a simulation."""
        return cls.query.filter_by(simulation_id=simulation_id).all()
    
    def update(self, **kwargs):
        """Update party attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the party."""
        db.session.delete(self)
        db.session.commit()
    
    def get_support_in_city(self, city_id):
        """Get party support percentage in a specific city."""
        support = PartySupport.query.filter_by(party_id=self.id, city_id=city_id).first()
        return support.support_percentage if support else 0.0


class PartySupport(db.Model):
    """PartySupport model - represents party support percentage in a city."""
    
    __tablename__ = 'party_supports'
    
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    support_percentage = db.Column(db.Float, nullable=False, default=0.0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('party_id', 'city_id', name='uq_party_support_per_city'),
        db.CheckConstraint('support_percentage >= 0 AND support_percentage <= 100', name='check_support_percentage_range'),
    )
    
    @validates('support_percentage')
    def validate_support_percentage(self, key, support_percentage):
        """Validate support percentage is between 0 and 100."""
        if support_percentage < 0 or support_percentage > 100:
            raise ValueError("Support percentage must be between 0 and 100")
        return support_percentage
    
    def __repr__(self):
        return f'<PartySupport {self.party.name} in {self.city.name}: {self.support_percentage}%>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'party_id': self.party_id,
            'city_id': self.city_id,
            'support_percentage': self.support_percentage,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    # CRUD operations
    @classmethod
    def create(cls, party_id, city_id, support_percentage):
        """Create a new party support record."""
        support = cls(
            party_id=party_id,
            city_id=city_id,
            support_percentage=support_percentage
        )
        db.session.add(support)
        db.session.commit()
        return support
    
    @classmethod
    def get_by_id(cls, support_id):
        """Get party support by ID."""
        return cls.query.get(support_id)
    
    @classmethod
    def get_by_city(cls, city_id):
        """Get all party supports for a city."""
        return cls.query.filter_by(city_id=city_id).all()
    
    @classmethod
    def get_by_party(cls, party_id):
        """Get all party supports for a party."""
        return cls.query.filter_by(party_id=party_id).all()
    
    def update(self, support_percentage):
        """Update support percentage."""
        self.support_percentage = support_percentage
        self.last_updated = datetime.utcnow()
        db.session.commit()
    
    def delete(self):
        """Delete the party support record."""
        db.session.delete(self)
        db.session.commit()