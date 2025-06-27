from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import User, AuditLog
from server.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active
    } for user in users]), 200

@admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@admin_required
def get_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify([log.to_dict() for log in logs]), 200

@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['PUT'])
@jwt_required()
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({
        'message': 'User status updated',
        'is_active': user.is_active
    }), 200