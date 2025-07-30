"""Simulation model for ELECTORI application."""
from datetime import datetime
import enum

# Get db instance - will be set by Flask app
from app import db


class SimulationStatus(enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class Simulation(db.Model):
    """Simulation model - represents a political simulation session."""
    
    __tablename__ = 'simulations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_played = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(SimulationStatus), nullable=False, default=SimulationStatus.ACTIVE)
    
    # Relationships
    cities = db.relationship('City', backref='simulation', lazy=True, cascade='all, delete-orphan')
    parties = db.relationship('Party', backref='simulation', lazy=True, cascade='all, delete-orphan')
    elections = db.relationship('Election', backref='simulation', lazy=True, cascade='all, delete-orphan')
    mps = db.relationship('MP', backref='simulation', lazy=True, cascade='all, delete-orphan')
    coalitions = db.relationship('ParliamentCoalition', backref='simulation', lazy=True, cascade='all, delete-orphan')
    laws = db.relationship('Law', backref='simulation', lazy=True, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_simulation_name'),
    )
    
    def __repr__(self):
        return f'<Simulation {self.name}: {self.country_name}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'country_name': self.country_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_played': self.last_played.isoformat() if self.last_played else None,
            'status': self.status.value if self.status else None
        }
    
    # CRUD operations
    @classmethod
    def create(cls, name, country_name):
        """Create a new simulation."""
        simulation = cls(name=name, country_name=country_name)
        db.session.add(simulation)
        db.session.commit()
        return simulation
    
    @classmethod
    def get_by_id(cls, simulation_id):
        """Get simulation by ID."""
        return cls.query.get(simulation_id)
    
    @classmethod
    def get_all(cls):
        """Get all simulations."""
        return cls.query.all()
    
    def update(self, **kwargs):
        """Update simulation attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_played = datetime.utcnow()
        db.session.commit()
    
    def delete(self):
        """Delete the simulation."""
        db.session.delete(self)
        db.session.commit()