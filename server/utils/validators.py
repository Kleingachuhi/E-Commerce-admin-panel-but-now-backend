import re
from flask import request
from werkzeug.exceptions import BadRequest

def validate_user_input(input_data, required_fields=None):
    """
    Comprehensive input validation for user data
    Args:
        input_data (dict): The user input to validate
        required_fields (list): List of required field names
    Returns:
        dict: Validated and cleaned data
    Raises:
        BadRequest: If validation fails with detailed error messages
    """
    errors = {}
    
    # 1. Check input type
    if not isinstance(input_data, dict):
        raise BadRequest("Input must be a JSON object")

    # 2. Check required fields
    if required_fields:
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            errors['missing_fields'] = missing_fields

    # 3. Field-specific validations
    if 'username' in input_data:
        username = input_data['username']
        if not isinstance(username, str):
            errors['username'] = "Must be a string"
        elif len(username) < 3:
            errors['username'] = "Must be at least 3 characters"
        elif not username.isalnum():
            errors['username'] = "Must contain only letters and numbers"

    if 'email' in input_data:
        email = input_data['email']
        if not isinstance(email, str):
            errors['email'] = "Must be a string"
        elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            errors['email'] = "Invalid email format"

    if 'password' in input_data:
        password = input_data['password']
        if not isinstance(password, str):
            errors['password'] = "Must be a string"
        elif len(password) < 8:
            errors['password'] = "Must be at least 8 characters"
        elif not any(char.isdigit() for char in password):
            errors['password'] = "Must contain at least one number"

    if 'role' in input_data and input_data['role'] not in ['admin', 'user']:
        errors['role'] = "Must be either 'admin' or 'user'"

    # 4. Raise errors if any
    if errors:
        raise BadRequest({
            "error": "Validation failed",
            "details": errors
        })

    # 5. Clean and return data
    cleaned_data = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in input_data.items()
    }

    return cleaned_data

def validate_email(email):
    """Validate email format"""
    if not isinstance(email, str):
        raise BadRequest("Email must be a string")
    
    email = email.strip().lower()
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise BadRequest("Invalid email address format")
    
    return email

def validate_password(password):
    """Validate password requirements"""
    if not isinstance(password, str):
        raise BadRequest("Password must be a string")
    
    if len(password) < 8:
        raise BadRequest("Password must be at least 8 characters")
    
    if not any(char.isdigit() for char in password):
        raise BadRequest("Password must contain at least one number")
    
    if not any(char.isupper() for char in password):
        raise BadRequest("Password must contain at least one uppercase letter")
    
    return password