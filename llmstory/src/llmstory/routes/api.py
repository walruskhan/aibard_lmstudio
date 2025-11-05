"""
API routes for LLM Story application.
Handles all API endpoints for data exchange.
"""
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Sequence
from flask import Blueprint, Response, json, jsonify, request, current_app
import humanize
import lmstudio as lms
import uuid
from flask import make_response
from ..session import get_or_create_session, get_session
import time

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@contextmanager
def valid_lm_client():
    config = current_app.config
    SERVER_API_HOST = config.get('LMSTUDIO_API_HOST', 'localhost:1234')

    is_connected = lms.Client.is_valid_api_host(SERVER_API_HOST)
    if not is_connected:
        raise ConnectionError("Could not connect to LMStudio API")

    with lms.Client(SERVER_API_HOST) as client:
        yield client
        

@api_bp.route("/models/", methods=['DELETE'])
def unload_model(model_key: str):
    data = request.get_json()
    model_key = data['model_key']

    with valid_lm_client() as client:
        llms = [(m, ModelInfo(m).key) for m in lms.list_loaded_models("llm")]
        model_to_unload = next((m for m, key in llms if model_key == key), None)
        if model_to_unload is None:
            return jsonify({"error": "Model not found"}), 404

        model_to_unload.unload()
        return jsonify({"message": f"Model {model_key} unloaded successfully"})

@api_bp.route("/models/", methods=['PUT'])
def load_model(model_key: str):
    data = request.get_json()
    model_key = data['model_key']

    with valid_lm_client() as client:
        model = lms.llm(model_key)
        if model is None:
            return jsonify({
                "key": model_key,
                "loaded": False,
                "reason": "Unknown model key"
            })
        
        return jsonify({
            "key": model_key,
            "loaded": True
        })
    
def require_session_key(inner):
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id') or request.args.get('session_id')
        if not session_id and session_id is not str:
            return jsonify({"error": "Session ID required"}), 401
        kwargs['session_id'] = session_id
        return inner(*args, **kwargs)
    return wrapper

@api_bp.route("/session/<string:session_id>/models", methods=['PUT'])
def use_model(session_id: str):
    session = get_or_create_session(session_id)

    data = request.get_json()
    model_key = data['model_key']

    session.model_key = model_key

    return jsonify({
        "session_id": session_id,
        "model_key": model_key
    })

@api_bp.route("/session/debug", methods=['POST'])
def create_session_debug():
    session_id = str(uuid.uuid4())
    response = make_response(jsonify({"session_id": session_id, "created": True}))
    response.set_cookie('session_id', session_id, httponly=True, secure=False)
    return response


@api_bp.route("/session/<string:session_id>/chat/stream", methods=['GET'])
def stream_chat(session_id: str):
    def generate_sse_message():
        try:
            # session = get_session(session_id)

            for i in range(1, 10):
                yield json.dumps({
                    "data": {
                        "event": "response",
                        "text": f"Message = {i}"
                    }
                })
                time.sleep(1)
        except:
            yield json.dumps({
                "data": {
                    "error": "SESSION_NOT_EXIST",
                    "message": f"Session {session_id} does not exist"
                }
            })
            return
    
    return Response(generate_sse_message(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST'
                    })


@dataclass
class ModelInfo:
    key: str
    id: str
    arch: str
    context_length: int
    display_name: str
    format: str
    num_params: str

    def __init__(self, model: Sequence[lms.LLM]) -> ModelInfo:
        info = model.get_info()
        config = model.get_load_config()

        self.key = model.identifier
        self.id = info.instance_reference
        self.arch = info.architecture
        self.context_length = info.context_length
        self.display_name = info.display_name
        self.format = info.format
        self.num_params = info.params_string

@api_bp.route('/status')
def get_status():
    try:
        with valid_lm_client() as client:
            loaded_models = [ModelInfo(m) for m in client.llm.list_loaded()]

            available_models = [{
                "key": m.model_key,
                "size_bytes": m.info.size_bytes,
                "size_friendly": humanize.naturalsize(m.info.size_bytes)
            } for m in client.llm.list_downloaded()]

            return jsonify({
                    "is_connected": True,
                    "loaded_models": loaded_models,
                    "available_models": available_models
            })
    except ConnectionError as e:
        return jsonify({
            "is_connected": False,
            "loaded_models": [],
            "available_models": []
        })
        

@api_bp.route('/config')
def get_public_config():
    """Get public configuration information"""
    config = current_app.config
    return jsonify({
        'environment': config.get('ENVIRONMENT', 'development'),
        'api': {
            'version': config.get('API_VERSION', '1.0.0'),
            'title': config.get('API_TITLE', 'LLM Story API'),
            'description': config.get('API_DESCRIPTION', 'API for LLM Story application')
        },
        'features': {
            'story_analytics': config.get('ENABLE_STORY_ANALYTICS', False),
            'api_docs': config.get('ENABLE_API_DOCS', False),
            'health_detailed': config.get('ENABLE_HEALTH_DETAILED', False),
            'contact_email': config.get('ENABLE_CONTACT_EMAIL', False)
        },
        'flask': {
            'host': config.get('FLASK_HOST', '0.0.0.0'),
            'port': config.get('FLASK_PORT', 5000),
            'debug': config.get('DEBUG', True)
        },
        'lmstudio': {
            'api_host': config.get('LMSTUDIO_API_HOST', 'localhost:1234')
        }
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