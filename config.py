import os
from typing import Optional

class Config:
    """Configuration class for the application."""
    
    # Flask Configuration
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV: str = os.environ.get('FLASK_ENV', 'production')
    
    # Email Configuration
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT: int = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS: bool = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME: Optional[str] = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD: Optional[str] = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: Optional[str] = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "200 per day, 50 per hour"
    RATE_LIMIT_CONTACT: str = "5 per minute"
    
    # Content File
    CONTENT_FILE: str = 'params.yaml'
    
    @classmethod
    def validate_email_config(cls) -> bool:
        """Validate that email configuration is complete."""
        required_fields = ['MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_DEFAULT_SENDER']
        return all(getattr(cls, field) for field in required_fields)
    
    @classmethod
    def get_email_config(cls) -> dict:
        """Get email configuration as dictionary."""
        return {
            'MAIL_SERVER': cls.MAIL_SERVER,
            'MAIL_PORT': cls.MAIL_PORT,
            'MAIL_USE_TLS': cls.MAIL_USE_TLS,
            'MAIL_USERNAME': cls.MAIL_USERNAME,
            'MAIL_PASSWORD': cls.MAIL_PASSWORD,
            'MAIL_DEFAULT_SENDER': cls.MAIL_DEFAULT_SENDER,
        } 