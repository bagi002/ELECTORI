# Validation utilities for ELECTORI application

def validate_simulation_data(data):
    """Validate simulation creation data"""
    errors = []
    
    if not data.get('name'):
        errors.append('Ime simulacije je obavezno')
    
    if not data.get('country_name'):
        errors.append('Ime države je obavezno')
        
    return errors

def validate_city_data(data):
    """Validate city data"""
    errors = []
    
    if not data.get('name'):
        errors.append('Ime grada je obavezno')
        
    population = data.get('population')
    if not population or population < 100:
        errors.append('Broj stanovnika mora biti veći od 100')
        
    return errors

def validate_party_data(data):
    """Validate party data"""
    errors = []
    
    if not data.get('name'):
        errors.append('Ime partije je obavezno')
        
    if not data.get('color'):
        errors.append('Boja partije je obavezna')
        
    return errors
