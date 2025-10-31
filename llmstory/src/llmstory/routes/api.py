"""
API routes for LLM Story application.
Handles all API endpoints for data exchange using dependency injection.
"""
from flask import Blueprint, jsonify, request
from flask_injector import inject
from ..services import StoryService, ContactService, HealthService

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health')
@inject
def health_check(health_service: HealthService):
    """Health check endpoint with dependency injection"""
    return jsonify(health_service.get_health_status())

@api_bp.route('/health/simple')
@inject
def simple_health_check(health_service: HealthService):
    """Simple health check endpoint"""
    return jsonify(health_service.get_simple_health())

@api_bp.route('/health/readiness')
@inject
def readiness_check(health_service: HealthService):
    """Readiness check endpoint"""
    return jsonify(health_service.get_readiness_status())

@api_bp.route('/health/liveness')
@inject
def liveness_check(health_service: HealthService):
    """Liveness check endpoint"""
    return jsonify(health_service.get_liveness_status())

@api_bp.route('/version')
def version():
    """API version information"""
    return jsonify({
        'version': '1.0.0',
        'api_name': 'LLM Story API',
        'description': 'API for LLM Story application with dependency injection',
        'features': ['dependency_injection', 'service_layer', 'health_monitoring']
    })

@api_bp.route('/contact', methods=['POST'])
@inject
def submit_contact(contact_service: ContactService):
    """Handle contact form submissions using dependency injection"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract and validate data using the service
        result = contact_service.submit_contact(
            name=data.get('name', ''),
            email=data.get('email', ''),
            subject=data.get('subject', ''),
            message=data.get('message', '')
        )
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/contact', methods=['GET'])
@inject
def get_contacts(contact_service: ContactService):
    """Get all contact submissions (admin endpoint)"""
    try:
        contacts = contact_service.get_all_contacts()
        unread_count = contact_service.get_unread_contacts_count()
        
        return jsonify({
            'contacts': contacts,
            'total': len(contacts),
            'unread_count': unread_count
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/contact/<int:contact_id>/read', methods=['PATCH'])
@inject
def mark_contact_read(contact_id: int, contact_service: ContactService):
    """Mark a contact as read"""
    try:
        success = contact_service.mark_contact_as_read(contact_id)
        if success:
            return jsonify({'message': 'Contact marked as read'})
        else:
            return jsonify({'error': 'Contact not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
@api_bp.route('/stories', methods=['GET'])
@inject
def get_stories(story_service: StoryService):
    """Get list of stories using dependency injection"""
    try:
        # Get query parameters
        search = request.args.get('search')
        
        if search:
            stories = story_service.search_stories(search)
        else:
            stories = story_service.get_all_stories()
        
        return jsonify({
            'stories': stories,
            'total': len(stories),
            'total_all_stories': story_service.get_stories_count()
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/stories', methods=['POST'])
@inject
def create_story(story_service: StoryService):
    """Create a new story using dependency injection"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        if not data.get('title') or not data.get('content'):
            return jsonify({
                'error': 'Missing required fields: title and content'
            }), 400
        
        # Create story using service
        story = story_service.create_story(
            title=data['title'],
            content=data['content'],
            summary=data.get('summary', '')
        )
        
        return jsonify({
            'success': True,
            'story': story,
            'message': 'Story created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/stories/<int:story_id>', methods=['GET'])
@inject
def get_story(story_id: int, story_service: StoryService):
    """Get a specific story by ID using dependency injection"""
    try:
        story = story_service.get_story_by_id(story_id)
        if story:
            return jsonify({'story': story})
        else:
            return jsonify({'error': 'Story not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/stories/<int:story_id>', methods=['PUT'])
@inject
def update_story(story_id: int, story_service: StoryService):
    """Update a story using dependency injection"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Update story using service
        updated_story = story_service.update_story(story_id, **data)
        
        if updated_story:
            return jsonify({
                'success': True,
                'story': updated_story,
                'message': 'Story updated successfully'
            })
        else:
            return jsonify({'error': 'Story not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/stories/<int:story_id>', methods=['DELETE'])
@inject
def delete_story(story_id: int, story_service: StoryService):
    """Delete a story using dependency injection"""
    try:
        success = story_service.delete_story(story_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Story deleted successfully'
            })
        else:
            return jsonify({'error': 'Story not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api_bp.route('/stats')
@inject
def get_stats(story_service: StoryService, contact_service: ContactService):
    """Get application statistics using dependency injection"""
    try:
        return jsonify({
            'stories': {
                'total': story_service.get_stories_count(),
                'published': len([s for s in story_service.get_all_stories() if s['status'] == 'published']),
                'drafts': len([s for s in story_service.get_all_stories() if s['status'] == 'draft'])
            },
            'contacts': {
                'total': len(contact_service.get_all_contacts()),
                'unread': contact_service.get_unread_contacts_count()
            }
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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
            '/api/contact',
            '/api/stories',
            '/api/stats'
        ]
    }), 404