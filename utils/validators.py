# Validation utilities for ELECTORI application

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present and non-empty"""
    if not data:
        return False
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    return True

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
