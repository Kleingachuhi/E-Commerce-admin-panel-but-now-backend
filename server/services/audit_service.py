from server.models.audit_log import AuditLog
from server.extensions import db

def validate_product_input(data):
    errors = {}
    if not data.get('name'):
        errors['name'] = 'Product name is required'
    if data.get('base_price') is None or float(data.get('base_price', 0)) <= 0:
        errors['base_price'] = 'Base price must be greater than 0'
    return errors

def validate_category_input(data):
    errors = {}
    if not data.get('name'):
        errors['name'] = 'Category name is required'
    return errors