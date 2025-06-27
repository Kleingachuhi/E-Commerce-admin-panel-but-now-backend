from server.models import Product, ProductItem
from server.extensions import db

def create_product_with_items(product_data, items_data, user_id):
    product = Product(
        name=product_data['name'],
        description=product_data.get('description', ''),
        base_price=product_data['base_price'],
        user_id=user_id,
        category_id=product_data.get('category_id')
    )
    
    db.session.add(product)
    db.session.flush()  # To get the product ID
    
    for item_data in items_data:
        item = ProductItem(
            sku=item_data['sku'],
            size=item_data.get('size'),
            color=item_data.get('color'),
            price_adjustment=item_data.get('price_adjustment', 0.0),
            stock_quantity=item_data.get('stock_quantity', 0),
            image_url=item_data.get('image_url'),
            product_id=product.id
        )
        db.session.add(item)
    
    db.session.commit()
    return product