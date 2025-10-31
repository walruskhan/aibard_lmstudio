"""
API routes for LLM Story application.
Handles all API endpoints for data exchange using dependency injection.
"""
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..services import ConfigService

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/config')
@inject
def get_public_config(config_service: ConfigService):
    """Get public configuration information"""
    return jsonify({
        'environment': config_service.environment,
        'api': {
            'version': config_service.api.version,
            'title': config_service.api.title,
            'description': config_service.api.description
        },
        'features': {
            'story_analytics': config_service.features.enable_story_analytics,
            'api_docs': config_service.features.enable_api_docs,
            'health_detailed': config_service.features.enable_health_detailed,
            'contact_email': config_service.features.enable_contact_email
        },
        'cors_origins': config_service.security.cors_origins,
        'rate_limit_per_minute': config_service.security.rate_limit_per_minute
    })

@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors for API routes"""
    return jsonify({
        'error': 'API endpoint not found',
        'available_endpoints': [
            '/api/health',
            '/api/health/simple',
            '/api/health/readiness', 
            '/api/health/liveness',
            '/api/version',
            '/api/config',
            '/api/contact',
            '/api/stories',
            '/api/stats'
        ]
    }), 404