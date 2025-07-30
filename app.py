import os
import logging
from typing import Dict, Any
from functools import wraps
import yaml
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
from config import Config
from utils import validate_contact_form_data, sanitize_input

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Content cache
_content_cache = {}
_cache_timestamp = 0

def load_content() -> Dict[str, Any]:
    """Load content from YAML file with caching."""
    global _content_cache, _cache_timestamp
    
    try:
        # Check if cache is still valid (5 minutes)
        current_time = os.path.getmtime(Config.CONTENT_FILE)
        if _content_cache and current_time <= _cache_timestamp:
            return _content_cache
        
        with open(Config.CONTENT_FILE, 'r', encoding='utf-8') as file:
            _content_cache = yaml.safe_load(file)
            _cache_timestamp = current_time
            return _content_cache
    except FileNotFoundError:
        logger.error(f"{Config.CONTENT_FILE} file not found")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing {Config.CONTENT_FILE}: {e}")
        return {}

def create_app() -> Flask:
    """Application factory pattern."""
    
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    
    # Configure Flask-Mail
    app.config.update(Config.get_email_config())
    
    # Initialize extensions
    mail = Mail(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[Config.RATE_LIMIT_DEFAULT]
    )
    
    def get_navbar_state(active_page: str) -> Dict[str, str]:
        """Generate navbar state for the given active page."""
        pages = ['index', 'resume', 'services', 'projects', 'contact']
        return {page: 'active' if page == active_page else 'inactive' for page in pages}
    

    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', title="Page Not Found", navbar=get_navbar_state('index'), content=load_content()), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return render_template('500.html', title="Server Error", navbar=get_navbar_state('index'), content=load_content()), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {e}")
        if isinstance(e, HTTPException):
            return e
        return render_template('500.html', title="Server Error", navbar=get_navbar_state('index'), content=load_content()), 500
    
    @app.route('/')
    @app.route('/index')
    def home():
        """Home page route."""
        return render_template(
            'index.html', 
            title="Home", 
            content=load_content(), 
            navbar=get_navbar_state('index')
        )
    
    @app.route('/resume')
    def resume():
        """Resume page route."""
        return render_template(
            'resume.html', 
            title="Resume", 
            content=load_content(), 
            navbar=get_navbar_state('resume')
        )
    
    @app.route('/projects')
    def projects():
        """Projects page route."""
        return render_template(
            'projects.html', 
            title="Projects", 
            content=load_content(), 
            navbar=get_navbar_state('projects')
        )
    
    @app.route('/services')
    def services():
        """Services page route."""
        return render_template(
            'services.html', 
            title="Services", 
            content=load_content(), 
            navbar=get_navbar_state('services')
        )
    
    @app.route('/contact', methods=['GET', 'POST'])
    @limiter.limit(Config.RATE_LIMIT_CONTACT)
    def contact():
        """Contact page route with rate limiting."""
        navbar = get_navbar_state('contact')
        content = load_content()
        
        if request.method == 'POST':
            form_data = {
                'name': sanitize_input(request.form.get('name', '')),
                'email': sanitize_input(request.form.get('email', '')),
                'subject': sanitize_input(request.form.get('subject', '')),
                'message': sanitize_input(request.form.get('message', ''))
            }
            
            # Validate form data
            is_valid, error_message = validate_contact_form_data(form_data)
            
            if not is_valid:
                flash(error_message, 'danger')
                return render_template(
                    'contact.html', 
                    title="Contact", 
                    content=content, 
                    navbar=navbar,
                    form_data=form_data
                )
            
            # Check if email is configured
            if not Config.validate_email_config():
                logger.error("Email configuration is incomplete")
                flash('Contact form is not configured. Please try again later.', 'danger')
                return render_template(
                    'contact.html', 
                    title="Contact", 
                    content=content, 
                    navbar=navbar,
                    form_data=form_data
                )
            
            try:
                # Send email
                msg = Message(
                    subject=f"Contact Form: {form_data['subject']}",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[app.config['MAIL_DEFAULT_SENDER']]
                )
                msg.body = f"""New message from {form_data['name']} ({form_data['email']}):
                
Subject: {form_data['subject']}

Message:
{form_data['message']}"""
                
                mail.send(msg)
                logger.info(f"Contact form submitted successfully from {form_data['email']}")
                flash('Message sent successfully!', 'success')
                
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                flash('Failed to send the message. Please try again later.', 'danger')
            
            return redirect(url_for('contact'))
        
        return render_template(
            'contact.html', 
            title="Contact", 
            content=content, 
            navbar=navbar
        )
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.FLASK_ENV == 'development')