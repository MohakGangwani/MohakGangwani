import re
from typing import Dict, Any, Tuple
from email_validator import validate_email, EmailNotValidError

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS attacks."""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def validate_email_address(email: str) -> Tuple[bool, str]:
    """Validate email address format."""
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)

def validate_contact_form_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate contact form data with enhanced security."""
    required_fields = ['name', 'email', 'subject', 'message']
    
    # Check required fields
    for field in required_fields:
        if not data.get(field) or not data[field].strip():
            return False, f"{field.title()} is required"
    
    # Sanitize inputs
    sanitized_data = {}
    for field in required_fields:
        sanitized_data[field] = sanitize_input(data[field])
        if not sanitized_data[field]:
            return False, f"{field.title()} cannot be empty"
    
    # Validate email
    is_valid_email, email_error = validate_email_address(sanitized_data['email'])
    if not is_valid_email:
        return False, f"Invalid email address: {email_error}"
    
    # Check message length
    if len(sanitized_data['message']) < 10:
        return False, "Message must be at least 10 characters long"
    
    if len(sanitized_data['message']) > 2000:
        return False, "Message must be less than 2000 characters"
    
    # Check name length
    if len(sanitized_data['name']) > 100:
        return False, "Name must be less than 100 characters"
    
    # Check subject length
    if len(sanitized_data['subject']) > 200:
        return False, "Subject must be less than 200 characters"
    
    return True, ""

def format_phone_number(phone: str) -> str:
    """Format phone number for display."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..." 