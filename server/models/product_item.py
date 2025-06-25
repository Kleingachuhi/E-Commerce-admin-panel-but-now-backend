from server.extensions import db

class ProductItem(db.Model):
    __tablename__ = 'product_items'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    price_adjustment = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __repr__(self):
        return f'<ProductItem {self.sku}>'