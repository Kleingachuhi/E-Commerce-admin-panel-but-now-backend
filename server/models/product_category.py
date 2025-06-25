from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import ProductCategory
from server.extensions import db
from server.utils.validators import validate_category_input
from server.services.audit_service import log_action

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = ProductCategory.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'product_count': len(c.products)
    } for c in categories]), 200

@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = ProductCategory.query.get_or_404(id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'products': [{
            'id': p.id,
            'name': p.name,
            'base_price': p.base_price
        } for p in category.products]
    }), 200

@categories_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required()
def create_category():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    errors = validate_category_input(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    category = ProductCategory(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(category)
    db.session.commit()
    
    # Log action
    log_action(current_user['id'], 'create', 'product_categories', category.id, None, {
        'name': category.name,
        'description': category.description
    })
    
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

@categories_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required()
def update_category(id):
    data = request.get_json()
    current_user = get_jwt_identity()
    category = ProductCategory.query.get_or_404(id)
    
    old_values = {
        'name': category.name,
        'description': category.description
    }
    
    errors = validate_category_input(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    category.name = data['name']
    category.description = data.get('description', category.description)
    
    db.session.commit()
    
    # Log action
    log_action(current_user['id'], 'update', 'product_categories', category.id, old_values, {
        'name': category.name,
        'description': category.description
    })
    
    return jsonify({'message': 'Category updated successfully'}), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_category(id):
    current_user = get_jwt_identity()
    category = ProductCategory.query.get_or_404(id)
    
    old_values = {
        'name': category.name,
        'description': category.description
    }
    
    db.session.delete(category)
    db.session.commit()
    
    log_action(current_user['id'], 'delete', 'product_categories', id, old_values, None)
    
    return jsonify({'message': 'Category deleted successfully'}), 200