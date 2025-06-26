from functools import wraps
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