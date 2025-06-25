def validate_category_input(data):
    errors = {}
    
    if not data.get('name'):
        errors['name'] = 'Category name is required'
    elif len(data['name']) < 2:
        errors['name'] = 'Category name must be at least 2 characters'
    
    return errors