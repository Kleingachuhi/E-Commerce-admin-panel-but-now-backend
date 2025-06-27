from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from server.models import Product, ProductItem, ProductCategory
from server.extensions import db

products_bp = Blueprint('products', __name__)
@products_bp.route('', methods=['GET'])

@jwt_required()
def get_products():
    try:
        rows = db.session.query(Product, ProductItem, ProductCategory)\
            .outerjoin(ProductItem, Product.id == ProductItem.product_id)\
            .outerjoin(ProductCategory, Product.category_id == ProductCategory.id)\
            .all()

        products_dict = {}

        for product, item, category in rows:
            if product.id not in products_dict:
                products_dict[product.id] = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "base_price": float(product.base_price),
                    "is_active": product.is_active,
                    "created_at": product.created_at.isoformat() if product.created_at else None,
                    "updated_at": product.updated_at.isoformat() if product.updated_at else None,
                    "user_id": product.user_id,
                    "category_id": product.category_id,
                    "category": {
                        "id": category.id if category else None,
                        "name": category.name if category else "Uncategorized"
                    },
                    "items": []
                }

            if item:
                products_dict[product.id]["items"].append({
                    "id": item.id,
                    "sku": item.sku,
                    "size": item.size,
                    "color": item.color,
                    "price_adjustment": float(item.price_adjustment),
                    "stock_quantity": item.stock_quantity,
                    "image_url": item.image_url,
                    "product_id": item.product_id
                })

        products = list(products_dict.values())

        return jsonify({"products": products}), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch products", "message": str(e)}), 500
