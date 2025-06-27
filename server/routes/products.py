from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import Product, ProductItem
from server.extensions import db
from server.utils.decorators import admin_required
from server.services.auth_service import log_auth_action

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', type=str)
        
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        products = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'products': [p.to_dict() for p in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': products.page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404 if '404' in str(e) else 500

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        
        product = Product(
            name=data['name'],
            description=data.get('description'),
            base_price=float(data['base_price']),
            user_id=current_user['id'],
            category_id=data.get('category_id')
        )
        
        db.session.add(product)
        db.session.flush()  # Get the product ID before commit
        
        if 'items' in data:
            for item_data in data['items']:
                item = ProductItem(
                    sku=item_data['sku'],
                    size=item_data.get('size'),
                    color=item_data.get('color'),
                    price_adjustment=float(item_data.get('price_adjustment', 0)),
                    stock_quantity=int(item_data.get('stock_quantity', 0)),
                    product_id=product.id
                )
                db.session.add(item)
        
        db.session.commit()
        
        log_auth_action(
            current_user['id'],
            'product_created',
            request.remote_addr,
            table_name='products',
            record_id=product.id,
            new_values=data
        )
        
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        product = Product.query.get_or_404(product_id)
        
        old_values = {
            'name': product.name,
            'description': product.description,
            'base_price': product.base_price,
            'category_id': product.category_id
        }
        
        product.name = data['name']
        product.description = data.get('description', product.description)
        product.base_price = float(data['base_price'])
        product.category_id = data.get('category_id', product.category_id)
        
        db.session.commit()
        
        log_auth_action(
            current_user['id'],
            'product_updated',
            request.remote_addr,
            table_name='products',
            record_id=product.id,
            old_values=old_values,
            new_values=data
        )
        
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    try:
        current_user = get_jwt_identity()
        product = Product.query.get_or_404(product_id)
        
        product.is_active = False
        db.session.commit()
        
        log_auth_action(
            current_user['id'],
            'product_deleted',
            request.remote_addr,
            table_name='products',
            record_id=product.id
        )
        
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400