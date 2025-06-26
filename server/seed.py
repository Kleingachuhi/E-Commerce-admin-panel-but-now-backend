from server.app import create_app
from server.extensions import db
from server.models.user import User
from server.models.products import Product
from server.models.product_item import ProductItem
from server.models.product_category import ProductCategory
from server.models.audit_log import AuditLog
import sys

app = create_app()

def seed_database():
    with app.app_context():
        try:
            print("Starting database seeding...")
            db.drop_all()
            db.create_all()

            # Admin user
            admin = User(username='admin', email='admin@example.com', role='admin', is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)

            # Regular user
            user = User(username='user', email='user@example.com', role='user', is_active=True)
            user.set_password('user123')
            db.session.add(user)

            # Categories
            electronics = ProductCategory(name='Electronics', description='Electronic devices')
            clothing = ProductCategory(name='Clothing', description='Apparel and accessories')
            db.session.add_all([electronics, clothing])
            db.session.flush()

            # Products
            laptop = Product(name='Laptop', description='High performance laptop', base_price=999.99, user_id=1, category_id=1)
            tshirt = Product(name='T-Shirt', description='Cotton t-shirt', base_price=19.99, user_id=2, category_id=2)
            db.session.add_all([laptop, tshirt])
            db.session.flush()

            # Product items
            laptop_item = ProductItem(sku='LP001', size='15-inch', color='Silver', price_adjustment=0, stock_quantity=50, product_id=1)
            tshirt_item = ProductItem(sku='TS001', size='M', color='Black', price_adjustment=0, stock_quantity=100, product_id=2)
            db.session.add_all([laptop_item, tshirt_item])

            db.session.commit()
            print("Database seeded successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f" Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    seed_database()