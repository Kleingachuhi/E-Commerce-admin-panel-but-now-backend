from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from server.models import AuditLog, User
from server.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/audit-logs')
@jwt_required()
@admin_required()
def get_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify([{'action': l.action, 'table': l.table_name} for l in logs])

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])