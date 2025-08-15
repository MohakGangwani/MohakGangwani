import os
import logging
import json
from datetime import datetime
from typing import Dict, Any
from functools import wraps
import yaml
from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
from config import Config
from utils import validate_contact_form_data, sanitize_input

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize cache
cache = Cache()

# Content cache
_content_cache = {}
_cache_timestamp = 0

def log_request_info(func):
    """Decorator to log request information."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
        return func(*args, **kwargs)
    return wrapper

def log_error(error, context=""):
    """Log errors with structured information."""
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'request_path': request.path if request else 'N/A',
        'request_method': request.method if request else 'N/A',
        'remote_addr': request.remote_addr if request else 'N/A',
        'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
        'context': context
    }
    logger.error(f"Error occurred: {json.dumps(error_data, indent=2)}")

@cache.memoize(timeout=300)  # Cache for 5 minutes
def load_content() -> Dict[str, Any]:
    """Load content from YAML file with Redis caching."""
    global _content_cache, _cache_timestamp
    
    try:
        # Check if cache is still valid (5 minutes)
        current_time = os.path.getmtime(Config.CONTENT_FILE)
        if _content_cache and current_time <= _cache_timestamp:
            return _content_cache
        
        with open(Config.CONTENT_FILE, 'r', encoding='utf-8') as file:
            _content_cache = yaml.safe_load(file)
            _cache_timestamp = current_time
            logger.info("Content loaded and cached successfully")
            return _content_cache
    except FileNotFoundError:
        logger.error(f"{Config.CONTENT_FILE} file not found")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing {Config.CONTENT_FILE}: {e}")
        return {}
    except Exception as e:
        log_error(e, "load_content")
        return {}

def create_app() -> Flask:
    """Application factory pattern."""
    
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    
    # Configure Flask-Mail
    app.config.update(Config.get_email_config())
    
    # Configure Flask-Caching
    app.config['CACHE_TYPE'] = Config.CACHE_TYPE
    app.config['CACHE_REDIS_URL'] = Config.REDIS_URL if Config.REDIS_ENABLED else None
    app.config['CACHE_DEFAULT_TIMEOUT'] = Config.CACHE_DEFAULT_TIMEOUT
    app.config['CACHE_KEY_PREFIX'] = Config.CACHE_KEY_PREFIX
    
    # Initialize extensions
    mail = Mail(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[Config.RATE_LIMIT_DEFAULT]
    )
    cache.init_app(app)
    
    def get_navbar_state(active_page: str) -> Dict[str, str]:
        """Generate navbar state for the given active page."""
        pages = ['index', 'resume', 'services', 'projects', 'contact']
        return {page: 'active' if page == active_page else 'inactive' for page in pages}
    
    @app.errorhandler(404)
    def not_found_error(error):
        log_error(error, "404 error")
        return render_template('404.html', title="Page Not Found", navbar=get_navbar_state('index'), content=load_content()), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        log_error(error, "500 error")
        return render_template('500.html', title="Server Error", navbar=get_navbar_state('index'), content=load_content()), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        log_error(e, "Unhandled exception")
        if isinstance(e, HTTPException):
            return e
        return render_template('500.html', title="Server Error", navbar=get_navbar_state('index'), content=load_content()), 500
    
    @app.errorhandler(413)
    def too_large(error):
        log_error(error, "File too large")
        return jsonify({'error': 'File too large'}), 413
    
    @app.errorhandler(429)
    def too_many_requests(error):
        log_error(error, "Rate limit exceeded")
        return jsonify({'error': 'Too many requests. Please try again later.'}), 429
    
    @app.route('/')
    @app.route('/index')
    @log_request_info
    @cache.cached(timeout=300)
    def home():
        """Home page route."""
        try:
            return render_template(
                'index.html', 
                title="Home", 
                content=load_content(), 
                navbar=get_navbar_state('index')
            )
        except Exception as e:
            log_error(e, "home route")
            abort(500)
    
    @app.route('/resume')
    @log_request_info
    @cache.cached(timeout=300)
    def resume():
        """Resume page route."""
        try:
            return render_template(
                'resume.html', 
                title="Resume", 
                content=load_content(), 
                navbar=get_navbar_state('resume')
            )
        except Exception as e:
            log_error(e, "resume route")
            abort(500)
    
    @app.route('/projects')
    @log_request_info
    @cache.cached(timeout=300)
    def projects():
        """Projects page route."""
        try:
            return render_template(
                'projects.html', 
                title="Projects", 
                content=load_content(), 
                navbar=get_navbar_state('projects')
            )
        except Exception as e:
            log_error(e, "projects route")
            abort(500)
    
    @app.route('/services')
    @log_request_info
    @cache.cached(timeout=300)
    def services():
        """Services page route."""
        try:
            return render_template(
                'services.html', 
                title="Services", 
                content=load_content(), 
                navbar=get_navbar_state('services')
            )
        except Exception as e:
            log_error(e, "services route")
            abort(500)
    
    @app.route('/contact', methods=['GET', 'POST'])
    @limiter.limit(Config.RATE_LIMIT_CONTACT)
    @log_request_info
    def contact():
        """Contact page route with rate limiting."""
        try:
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
                    logger.warning(f"Contact form validation failed: {error_message}")
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
                    log_error(e, "email sending")
                    flash('Failed to send the message. Please try again later.', 'danger')
                
                return redirect(url_for('contact'))
            
            return render_template(
                'contact.html', 
                title="Contact", 
                content=content, 
                navbar=navbar
            )
        except Exception as e:
            log_error(e, "contact route")
            abort(500)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        try:
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'cache_status': 'redis' if Config.REDIS_ENABLED else 'simple',
                'email_configured': Config.validate_email_config()
            })
        except Exception as e:
            log_error(e, "health check")
            return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.FLASK_ENV == 'development')