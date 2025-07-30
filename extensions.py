"""
Database instance for ELECTORI application.
This module provides the database instance to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create database instance
db = SQLAlchemy()
migrate = Migrate()