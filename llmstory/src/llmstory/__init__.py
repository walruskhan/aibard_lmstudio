import os
from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector
from .routes import website_bp, api_bp
from .di_config import ServiceModule, RepositoryModule, ConfigModule

def create_app():
    """Application factory function with dependency injection"""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create Flask app with custom template and static folders
    app = Flask(__name__, 
               template_folder=os.path.join(current_dir, 'templates'),
               static_folder=os.path.join(current_dir, 'static'))
    
    # Configure the app
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DEBUG'] = True
    
    # Register blueprints
    app.register_blueprint(website_bp)
    app.register_blueprint(api_bp)
    
    # Set up dependency injection
    injector = Injector([
        ServiceModule,
        RepositoryModule,
        ConfigModule
    ])
    
    # Configure Flask-Injector
    FlaskInjector(app=app, injector=injector)
    
    print("✅ Dependency injection configured successfully!")
    print("📦 Available services: StoryService, ContactService, HealthService")
    
    return app

# Create the app instance
app = create_app()

def main() -> None:
    print("Starting LLM Story Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
