"""
Database initialization and management script for ELECTORI.

This module provides functions to initialize the SQLite database
and set up all required tables for the application.
"""

import os
from app import create_app
from extensions import db


def init_database(app=None):
    """
    Initialize the database with all tables.
    
    Args:
        app: Flask application instance. If None, creates a new one.
    """
    if app is None:
        app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")


def drop_database(app=None):
    """
    Drop all database tables.
    
    Args:
        app: Flask application instance. If None, creates a new one.
    """
    if app is None:
        app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All database tables dropped!")


def reset_database(app=None):
    """
    Reset the database by dropping and recreating all tables.
    
    Args:
        app: Flask application instance. If None, creates a new one.
    """
    if app is None:
        app = create_app()
    
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("Database reset successfully!")


def get_database_info(app=None):
    """
    Get information about the database and tables.
    
    Args:
        app: Flask application instance. If None, creates a new one.
        
    Returns:
        dict: Database information
    """
    if app is None:
        app = create_app()
    
    with app.app_context():
        # Get database metadata
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        
        info = {
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
            'database_exists': os.path.exists('electori.db') if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI'] else True,
            'tables': table_names,
            'table_count': len(table_names)
        }
        
        # Get row counts for each table
        table_info = {}
        for table_name in table_names:
            try:
                result = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                table_info[table_name] = {'row_count': count}
            except Exception as e:
                table_info[table_name] = {'row_count': 'Error', 'error': str(e)}
        
        info['table_info'] = table_info
        return info


def check_database_health(app=None):
    """
    Check database health and connectivity.
    
    Args:
        app: Flask application instance. If None, creates a new one.
        
    Returns:
        dict: Health check results
    """
    if app is None:
        app = create_app()
    
    health_status = {
        'database_accessible': False,
        'tables_exist': False,
        'foreign_keys_enabled': False,
        'errors': []
    }
    
    try:
        with app.app_context():
            # Check if we can connect to the database
            db.session.execute(db.text("SELECT 1"))
            health_status['database_accessible'] = True
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            health_status['tables_exist'] = len(table_names) > 0
            health_status['table_count'] = len(table_names)
            
            # Check if foreign keys are enabled (for SQLite)
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
                result = db.session.execute(db.text("PRAGMA foreign_keys"))
                fk_enabled = result.scalar()
                health_status['foreign_keys_enabled'] = bool(fk_enabled)
            else:
                health_status['foreign_keys_enabled'] = True  # Assume enabled for other databases
            
    except Exception as e:
        health_status['errors'].append(str(e))
    
    return health_status


if __name__ == '__main__':
    """
    Command-line interface for database operations.
    
    Usage:
        python database.py init    - Initialize database
        python database.py reset   - Reset database (drop and recreate)
        python database.py info    - Show database information
        python database.py health  - Check database health
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python database.py [init|reset|info|health]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'reset':
        reset_database()
    elif command == 'info':
        info = get_database_info()
        print("Database Information:")
        print(f"  URI: {info['database_uri']}")
        print(f"  Database exists: {info['database_exists']}")
        print(f"  Tables: {info['table_count']}")
        for table_name, table_data in info['table_info'].items():
            print(f"    {table_name}: {table_data['row_count']} rows")
    elif command == 'health':
        health = check_database_health()
        print("Database Health Check:")
        print(f"  Database accessible: {health['database_accessible']}")
        print(f"  Tables exist: {health['tables_exist']}")
        if 'table_count' in health:
            print(f"  Table count: {health['table_count']}")
        print(f"  Foreign keys enabled: {health['foreign_keys_enabled']}")
        if health['errors']:
            print("  Errors:")
            for error in health['errors']:
                print(f"    - {error}")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python database.py [init|reset|info|health]")
        sys.exit(1)