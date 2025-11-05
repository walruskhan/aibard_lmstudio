import os
from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO
from .routes import website_bp, api_bp

socketio = SocketIO()

def create_app():
    """Application factory function with configuration"""

    # Load environment variables from .env file
    load_dotenv()
    
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create Flask app with custom template and static folders
    app = Flask(__name__, 
               template_folder=os.path.join(current_dir, 'templates'),
               static_folder=os.path.join(current_dir, 'static'))

    
    # Load all environment variables into Flask's config
    for key, value in os.environ.items():
        # Convert string booleans to actual booleans
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        # Convert numeric strings to integers where appropriate
        elif value.isdigit():
            value = int(value)
        app.config[key] = value

    app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')


    # # Add debugger attachment in development
    # if app.config.get('FLASK_DEBUG'):
    #     try:
    #         import debugpy
    #         debugpy.listen(5678)
    #         print("Debugger listening on port 5678")
    #     except ImportError:
    #         pass  # debugpy not installed
        
    # Register blueprints
    app.register_blueprint(website_bp)
    app.register_blueprint(api_bp)

    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')

    
    
    return app

# Create the app instance
app = create_app()

def main() -> None:
    """Main function that starts the Flask application with configuration."""    
    print("🚀 Starting LLM Story Flask application...")
    print(f"🌍 Environment: {app.config.get('ENVIRONMENT', 'development')}")
    print(f"🔧 Host: {app.config.get('FLASK_HOST', '0.0.0.0')}:{app.config.get('FLASK_PORT', 5000)}")
    print(f"🐛 Debug: {app.config.get('DEBUG', True)}")

    app.run(
        debug=app.config.get('DEBUG', True),
        host=app.config.get('FLASK_HOST', '0.0.0.0'),
        port=app.config.get('FLASK_PORT', 5000)
    )
