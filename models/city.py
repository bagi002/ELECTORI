"""City model for ELECTORI application."""
from sqlalchemy.orm import validates
from app import db


class City(db.Model):
    """City model - represents a city in a simulation."""
    
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    coordinates_x = db.Column(db.Float, nullable=True)
    coordinates_y = db.Column(db.Float, nullable=True)
    
    # Relationships
    party_supports = db.relationship('PartySupport', backref='city', lazy=True, cascade='all, delete-orphan')
    candidacies = db.relationship('Candidacy', backref='city', lazy=True)
    election_results = db.relationship('ElectionResult', backref='city', lazy=True)
    mps = db.relationship('MP', backref='city', lazy=True)
    coalitions = db.relationship('ParliamentCoalition', backref='city', lazy=True)
    laws = db.relationship('Law', backref='city', lazy=True)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('simulation_id', 'name', name='uq_city_name_per_simulation'),
        db.CheckConstraint('population >= 100 AND population <= 10000000', name='check_population_range'),
    )
    
    @validates('population')
    def validate_population(self, key, population):
        """Validate population is within acceptable range."""
        if population < 100 or population > 10000000:
            raise ValueError("Population must be between 100 and 10,000,000")
        return population
    
    def __repr__(self):
        return f'<City {self.name}: {self.population:,} people>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'simulation_id': self.simulation_id,
            'name': self.name,
            'population': self.population,
            'coordinates_x': self.coordinates_x,
            'coordinates_y': self.coordinates_y
        }
    
    # CRUD operations
    @classmethod
    def create(cls, simulation_id, name, population, coordinates_x=None, coordinates_y=None):
        """Create a new city."""
        city = cls(
            simulation_id=simulation_id,
            name=name,
            population=population,
            coordinates_x=coordinates_x,
            coordinates_y=coordinates_y
        )
        db.session.add(city)
        db.session.commit()
        return city
    
    @classmethod
    def get_by_id(cls, city_id):
        """Get city by ID."""
        return cls.query.get(city_id)
    
    @classmethod
    def get_by_simulation(cls, simulation_id):
        """Get all cities for a simulation."""
        return cls.query.filter_by(simulation_id=simulation_id).all()
    
    def update(self, **kwargs):
        """Update city attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the city."""
        db.session.delete(self)
        db.session.commit()
    
    def get_total_support(self):
        """Get total party support percentage in this city."""
        return sum(support.support_percentage for support in self.party_supports)