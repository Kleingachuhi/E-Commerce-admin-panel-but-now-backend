from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import User, AuditLog
from server.extensions import db
from server.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'is_active': u.is_active
    } for u in users]), 200

@admin_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    
    if 'role' in data and data['role'] in ['user', 'admin']:
        user.role = data['role']
    
    if 'is_active' in data and isinstance(data['is_active'], bool):
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'}), 200

@admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@admin_required()
def get_audit_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'logs': [{
            'id': log.id,
            'action': log.action,
            'table_name': log.table_name,
            'record_id': log.record_id,
            'user_id': log.user_id,
            'username': log.user.username if log.user else None,
            'old_values': log.old_values,
            'new_values': log.new_values,
            'ip_address': log.ip_address,
            'created_at': log.created_at.isoformat()
        } for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': logs.page
    }), 200