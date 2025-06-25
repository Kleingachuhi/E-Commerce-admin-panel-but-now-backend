from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kw):
            verify_jwt_in_request()
            if get_jwt().get('role') != 'admin':
                return jsonify({'error':'Admins only'}),403
            return fn(*args, **kw)
        return decorator
    return wrapper