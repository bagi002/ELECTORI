import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from config import config
from extensions import db, migrate


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
    # This must be done after db.init_app()
    from models import simulation, city, party, election, parliament
    
    # Register blueprints
    from routes import simulation_routes, city_routes, party_routes
    from routes.support_routes import support_bp
    from routes.election_routes import bp as election_bp
    app.register_blueprint(simulation_routes.bp)
    app.register_blueprint(city_routes.bp)
    app.register_blueprint(party_routes.bp)
    app.register_blueprint(support_bp)
    app.register_blueprint(election_bp)
    
    # Main routes
    @app.route('/')
    def index():
        """Main application page - redirect to most functional page."""
        # Check if there's an active simulation in session
        active_simulation_id = session.get('active_simulation_id')
        
        if active_simulation_id:
            # If there's an active simulation, go to dashboard
            return redirect(url_for('dashboard'))
        else:
            # If no active simulation, go to simulation manager to select/create one
            return redirect(url_for('simulation_manager'))
    
    @app.route('/welcome')
    def welcome():
        """Welcome page for new users."""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard page."""
        # Check if there's an active simulation in session
        active_simulation_id = session.get('active_simulation_id')
        
        # If no active simulation, redirect to simulation manager
        if not active_simulation_id:
            return redirect(url_for('simulation_manager'))
            
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
    
    @app.before_request
    def validate_json():
        """Validate JSON in requests."""
        if request.path.startswith('/api') and request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type and 'application/json' in request.content_type:
                try:
                    if request.content_length and request.content_length > 0:
                        request.get_json(force=True)
                except Exception:
                    return jsonify({'error': 'Invalid JSON'}), 400
    
    @app.context_processor
    def inject_ui_state():
        """Inject UI state into all templates."""
        try:
            from utils.ui_state_manager import get_ui_context
            return get_ui_context()
        except Exception as e:
            # Fallback if UI state manager fails
            return {
                'ui_state': {
                    'navigation': {
                        'dashboard': True,
                        'simulations': True,
                        'cities': True,
                        'parties': True,
                        'elections': False,
                        'parliament': False
                    },
                    'active_simulation_id': session.get('active_simulation_id'),
                    'show_simulation_list': True,
                    'has_active_simulation': bool(session.get('active_simulation_id'))
                }
            }
    
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
    
    # Task 2 Frontend Routes
    @app.route("/simulation-manager")
    def simulation_manager():
        """Simulation manager page."""
        return render_template("simulation_manager.html")
    
    @app.route("/city-manager")
    def city_manager():
        """City manager page."""
        return render_template("city_manager.html")
    
    @app.route("/party-manager")
    def party_manager():
        """Party manager page."""
        return render_template("party_manager.html")
    
    @app.route("/party-profile")
    def party_profile():
        """Party profile page."""
        return render_template("party_profile.html")
    
    # Task 4 Election System Routes
    @app.route("/election-manager")
    def election_manager():
        """Election manager page."""
        return render_template("election_manager.html")
    
    # Task 3 Support System Routes
    @app.route("/support-matrix")
    def support_matrix():
        """Support matrix page with slider controls."""
        return render_template("support_matrix.html")
    
    @app.route("/support-analytics")
    def support_analytics():
        """Support analytics page with slider-controlled charts."""
        return render_template("support_analytics.html")
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
