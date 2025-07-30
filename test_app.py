#!/usr/bin/env python3
"""
Simple test script to verify the Flask application works correctly.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, load_content
from config import Config
from utils import validate_contact_form_data, sanitize_input, validate_email_address

class TestApp(unittest.TestCase):
    """Test cases for the Flask application."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_home_page(self):
        """Test that home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_resume_page(self):
        """Test that resume page loads correctly."""
        response = self.client.get('/resume')
        self.assertEqual(response.status_code, 200)
    
    def test_projects_page(self):
        """Test that projects page loads correctly."""
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page(self):
        """Test that contact page loads correctly."""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
    
    def test_404_page(self):
        """Test that 404 page works correctly."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        # Test normal input
        self.assertEqual(sanitize_input("Hello World"), "Hello World")
        
        # Test XSS attempt
        self.assertEqual(sanitize_input("<script>alert('xss')</script>"), "scriptalert('xss')/script")
        
        # Test empty input
        self.assertEqual(sanitize_input(""), "")
        self.assertEqual(sanitize_input(None), "")
    
    def test_email_validation(self):
        """Test email validation."""
        # Valid emails
        self.assertTrue(validate_email_address("test@example.com")[0])
        self.assertTrue(validate_email_address("user.name@domain.co.uk")[0])
        
        # Invalid emails
        self.assertFalse(validate_email_address("invalid-email")[0])
        self.assertFalse(validate_email_address("@example.com")[0])
        self.assertFalse(validate_email_address("test@")[0])
    
    def test_contact_form_validation(self):
        """Test contact form validation."""
        # Valid form data
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message with more than 10 characters.'
        }
        is_valid, error = validate_contact_form_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
        
        # Invalid form data - missing fields
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            # Missing subject and message
        }
        is_valid, error = validate_contact_form_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("required", error)
        
        # Invalid form data - short message
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Short'
        }
        is_valid, error = validate_contact_form_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("10 characters", error)
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test email config validation
        with patch.object(Config, 'MAIL_USERNAME', 'test@example.com'):
            with patch.object(Config, 'MAIL_PASSWORD', 'password'):
                with patch.object(Config, 'MAIL_DEFAULT_SENDER', 'test@example.com'):
                    self.assertTrue(Config.validate_email_config())
        
        # Test incomplete email config
        with patch.object(Config, 'MAIL_USERNAME', None):
            self.assertFalse(Config.validate_email_config())
    
    def test_load_content(self):
        """Test content loading."""
        content = load_content()
        # Should return a dictionary (even if empty)
        self.assertIsInstance(content, dict)

if __name__ == '__main__':
    print("Running tests...")
    unittest.main(verbosity=2) 