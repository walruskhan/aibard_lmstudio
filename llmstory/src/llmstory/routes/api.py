"""
API routes for LLM Story application.
Handles all API endpoints for data exchange.
"""
from flask import Blueprint, jsonify, request
import json
from datetime import datetime

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'LLM Story API'
    })

@api_bp.route('/version')
def version():
    """API version information"""
    return jsonify({
        'version': '1.0.0',
        'api_name': 'LLM Story API',
        'description': 'API for LLM Story application'
    })

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Basic email validation
        email = data['email']
        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({
                'error': 'Invalid email format'
            }), 400
        
        # In a real application, you would save this to a database
        # For now, we'll just log it and return success
        contact_data = {
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Log the contact submission (in production, save to database)
        print(f"Contact form submission: {json.dumps(contact_data, indent=2)}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'submission_id': f"contact_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@api_bp.route('/stories', methods=['GET'])
def get_stories():
    """Get list of stories (placeholder endpoint)"""
    # This is a placeholder - in a real app, you'd fetch from a database
    stories = [
        {
            'id': 1,
            'title': 'The AI Assistant',
            'summary': 'A story about an AI that learns to be helpful',
            'created_at': '2025-10-30T10:00:00Z',
            'status': 'published'
        },
        {
            'id': 2,
            'title': 'Code Generation Magic',
            'summary': 'How AI helps developers write better code',
            'created_at': '2025-10-30T11:00:00Z',
            'status': 'draft'
        }
    ]
    
    return jsonify({
        'stories': stories,
        'total': len(stories)
    })

@api_bp.route('/stories', methods=['POST'])
def create_story():
    """Create a new story (placeholder endpoint)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'title' not in data or 'content' not in data:
            return jsonify({
                'error': 'Missing required fields: title and content'
            }), 400
        
        # In a real application, you would save this to a database
        story = {
            'id': 3,  # This would be auto-generated
            'title': data['title'],
            'content': data['content'],
            'summary': data.get('summary', ''),
            'created_at': datetime.now().isoformat(),
            'status': 'draft'
        }
        
        return jsonify({
            'success': True,
            'story': story,
            'message': 'Story created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@api_bp.route('/stories/<int:story_id>', methods=['GET'])
def get_story(story_id):
    """Get a specific story by ID (placeholder endpoint)"""
    # This is a placeholder - in a real app, you'd fetch from a database
    if story_id == 1:
        story = {
            'id': 1,
            'title': 'The AI Assistant',
            'content': 'Once upon a time, there was an AI assistant that wanted to help everyone...',
            'summary': 'A story about an AI that learns to be helpful',
            'created_at': '2025-10-30T10:00:00Z',
            'status': 'published'
        }
        return jsonify({'story': story})
    else:
        return jsonify({'error': 'Story not found'}), 404

@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors for API routes"""
    return jsonify({
        'error': 'API endpoint not found',
        'available_endpoints': [
            '/api/health',
            '/api/version',
            '/api/contact',
            '/api/stories'
        ]
    }), 404