"""
Routes package initialization.
Exports blueprints for easy import.
"""
from .website import website_bp
from .api import api_bp

__all__ = ['website_bp', 'api_bp']