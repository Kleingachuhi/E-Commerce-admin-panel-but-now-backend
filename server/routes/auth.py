from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from server.models.user import User
from server.extensions import db
from server.utils.validators import validate_user_input
from server.services.auth_service import log_auth_action

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_user_input(data)
    if errors: return jsonify({'errors': errors}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username exists'}), 400
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user); db.session.commit()
    log_auth_action(user.id, 'register', request.remote_addr)
    return jsonify({'message':'Registered'}),201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}),401
    token = create_access_token(identity={'id':user.id,'role':user.role})
    log_auth_action(user.id, 'login', request.remote_addr)
    return jsonify({'access_token':token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current = get_jwt_identity()
    log_auth_action(current['id'], 'logout', request.remote_addr)
    return jsonify({'message':'Logged out'}), 200
