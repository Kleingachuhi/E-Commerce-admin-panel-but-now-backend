from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import Product, ProductItem, ProductCategory
from server.extensions import db
from server.utils.validators import validate_product_input
from server.services.product_service import log_product_action
from server.utils.decorators import admin_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'base_price': p.base_price,
        'category': p.category.name if p.category else None,
        'items': [{
            'id': i.id,
            'sku': i.sku,
            'size': i.size,
            'color': i.color,
            'price': p.base_price + i.price_adjustment,
            'stock': i.stock_quantity,
            'image_url': i.image_url
        } for i in p.items]
    } for p in products]), 200

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'base_price': product.base_price,
        'category': product.category.name if product.category else None,
        'items': [{
            'id': i.id,
            'sku': i.sku,
            'size': i.size,
            'color': i.color,
            'price': product.base_price + i.price_adjustment,
            'stock': i.stock_quantity,
            'image_url': i.image_url
        } for i in product.items]
    }), 200

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    errors = validate_product_input(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Create product
    product = Product(
        name=data['name'],
        description=data.get('description'),
        base_price=data['base_price'],
        user_id=current_user['id'],
        category_id=data.get('category_id')
    )
    
    db.session.add(product)
    db.session.commit()
    
    # Create product items if provided
    if 'items' in data:
        for item_data in data['items']:
            item = ProductItem(
                sku=item_data['sku'],
                size=item_data.get('size'),
                color=item_data.get('color'),
                price_adjustment=item_data.get('price_adjustment', 0),
                stock_quantity=item_data.get('stock_quantity', 0),
                image_url=item_data.get('image_url'),
                product_id=product.id
            )
            db.session.add(item)
        db.session.commit()
    
    # Log action
    log_product_action(current_user['id'], 'create', 'products', product.id, None, product.to_dict())
    
    return jsonify({'message': 'Product created successfully', 'id': product.id}), 201

@products_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    data = request.get_json()
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(id)
    
    old_values = {
        'name': product.name,
        'description': product.description,
        'base_price': product.base_price,
        'category_id': product.category_id
    }
    
    errors = validate_product_input(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Update product
    product.name = data['name']
    product.description = data.get('description', product.description)
    product.base_price = data['base_price']
    product.category_id = data.get('category_id', product.category_id)
    
    db.session.commit()
    
    # Log action
    log_product_action(current_user['id'], 'update', 'products', product.id, old_values, product.to_dict())
    
    return jsonify({'message': 'Product updated successfully'}), 200

@products_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_product(id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(id)
    
    old_values = product.to_dict()
    
    db.session.delete(product)
    db.session.commit()
    
    # Log action
    log_product_action(current_user['id'], 'delete', 'products', id, old_values, None)
    
    return jsonify({'message': 'Product deleted successfully'}), 200

