"""
Website routes for LLM Story application.
Handles all frontend/website related routes.
"""
from flask import Blueprint, render_template

# Create a blueprint for website routes
website_bp = Blueprint('website', __name__)

@website_bp.route('/')
def home():
    """Home page route using template"""
    return render_template('index.html')

@website_bp.route('/about')
def about():
    """About page route using template"""
    return render_template('about.html')

@website_bp.route('/contact')
def contact():
    """Contact page route using template"""
    return render_template('contact.html')

@website_bp.route('/docs')
def docs():
    """Documentation page"""
    return render_template('docs.html')

@website_bp.route('/portfolio')
def portfolio():
    """Portfolio/Projects page"""
    return render_template('portfolio.html')