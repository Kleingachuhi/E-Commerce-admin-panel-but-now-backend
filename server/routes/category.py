from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import ProductCategory
from server.extensions import db
from server.utils.decorators import admin_required

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = ProductCategory.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@category_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    category = ProductCategory(name=data['name'], description=data.get('description', ''))
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    category = ProductCategory.query.get_or_404(category_id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    db.session.commit()
    return jsonify(category.to_dict()), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    category = ProductCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'}), 200