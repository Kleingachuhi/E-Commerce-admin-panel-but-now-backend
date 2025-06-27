from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest
from server.models.user import User
from server.extensions import db, bcrypt
from server.utils.validators import validate_user_input, validate_email, validate_password
from server.services.auth_service import log_auth_action

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({
                "error": "Invalid content type",
                "message": "Content-Type must be application/json"
            }), 415

        try:
            data = validate_user_input(
                request.get_json(),
                required_fields=['username', 'email', 'password']
            )
        except BadRequest as e:
            return jsonify(e.description), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                "error": "Registration failed",
                "details": {"username": "Username already exists"}
            }), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                "error": "Registration failed", 
                "details": {"email": "Email already exists"}
            }), 400

        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        log_auth_action(
            user_id=user.id,
            action='register',
            ip_address=request.remote_addr,
            table_name='users',
            record_id=user.id,
            new_values={
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        )

        access_token = create_access_token(identity={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })

        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            },
            'access_token': access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        if not request.is_json:
            return jsonify({
                "error": "Invalid content type",
                "message": "Content-Type must be application/json"
            }), 415

        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "error": "Missing credentials",
                "message": "Username and password are required"
            }), 400

        user = User.query.filter_by(username=data['username']).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            return jsonify({
                "error": "Invalid credentials",
                "message": "Invalid username or password"
            }), 401

        if not user.is_active:
            return jsonify({
                "error": "Account disabled",
                "message": "This account has been deactivated"
            }), 403

        access_token = create_access_token(identity={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        })

        log_auth_action(
            user_id=user.id,
            action='login',
            ip_address=request.remote_addr,
            table_name='users',
            record_id=user.id
        )

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Login failed",
            "message": str(e)
        }), 500

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        'message': 'Protected endpoint accessed successfully',
        'user': current_user
    }), 200


@auth_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        identity = get_jwt_identity()
        user_id = identity['id'] 

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch user data",
            "message": str(e)
        }), 500
