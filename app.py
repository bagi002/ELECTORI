import os
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from models import simulation, city, party, election, parliament
    
    # Register blueprints
    from routes import simulation_routes, city_routes, party_routes
    app.register_blueprint(simulation_routes.bp)
    app.register_blueprint(city_routes.bp)
    app.register_blueprint(party_routes.bp)
    
    # Main routes
    @app.route('/')
    def index():
        """Main application page."""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard page."""
        # Check if there's an active simulation in session
        active_simulation_id = session.get('active_simulation_id')
        return render_template('dashboard.html', 
                             active_simulation_id=active_simulation_id)
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'app': app.config['APP_NAME'],
            'version': app.config['APP_VERSION']
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith('/api'):
            return jsonify({'error': 'Bad request'}), 400
        return render_template('errors/400.html'), 400
    
    # CLI commands
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized.')
    
    @app.cli.command()
    def seed_db():
        """Seed the database with sample data."""
        from seed_data import seed_database
        seed_database()
        print('Database seeded with sample data.')
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
