from functools import wraps
<<<<<<< HEAD
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] != 'admin':
                return jsonify({'error': 'Admins only'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
=======
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from werkzeug.exceptions import Forbidden

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get('role') == 'admin':
            raise Forbidden("Admin privileges required")
        return f(*args, **kwargs)
    return decorated_function
>>>>>>> bacdcd01b87596db6e2cf86eb3870a00b42cd9cf
