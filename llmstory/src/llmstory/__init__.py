import os
from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector
from .routes import website_bp, api_bp
from .di_config import ServiceModule, RepositoryModule, ConfigModule
from .services import ConfigService

def create_app():
    """Application factory function with dependency injection and configuration"""
    # Create injector first to get config service
    injector = Injector([
        ServiceModule,
        RepositoryModule,
        ConfigModule
    ])
    
    # Get configuration service
    config_service = injector.get(ConfigService)
    
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create Flask app with custom template and static folders
    app = Flask(__name__, 
               template_folder=os.path.join(current_dir, 'templates'),
               static_folder=os.path.join(current_dir, 'static'))
    
    # Configure the app using config service
    app.config.update(config_service.get_flask_config())
    
    # Additional Flask configuration
    app.config['CONFIG_SERVICE'] = config_service
    
    # Register blueprints
    app.register_blueprint(website_bp)
    app.register_blueprint(api_bp)
    
    # Configure Flask-Injector
    FlaskInjector(app=app, injector=injector)
    
    print("✅ Dependency injection configured successfully!")
    print(f"📦 Available services: ConfigService")
    print(f"🌍 Environment: {config_service.environment}")
    print(f"🐛 Debug mode: {config_service.debug}")
    
    return app

# Create the app instance
app = create_app()

def main() -> None:
    """Main function that starts the Flask application with configuration."""
    config_service = app.config['CONFIG_SERVICE']
    
    print("🚀 Starting LLM Story Flask application...")
    print(f"🌍 Environment: {config_service.environment}")
    print(f"🔧 Host: {config_service.flask_host}:{config_service.flask_port}")
    print(f"🐛 Debug: {config_service.debug}")
    
    app.run(
        debug=config_service.debug,
        host=config_service.flask_host,
        port=config_service.flask_port
    )
