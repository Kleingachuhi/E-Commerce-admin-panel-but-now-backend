from server.extensions import db

class ProductItem(db.Model):
    tablename = 'product_items'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    price_adjustment = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'size': self.size,
            'color': self.color,
            'price_adjustment': self.price_adjustment,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url,
            'product_id': self.product_id
        }

    def repr(self):
        return f'<ProductItem {self.sku}>'