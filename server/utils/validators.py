import re
def validate_user_input(data):
    errors = {}
    if not data.get('username'): errors['username'] = 'Required'
    if not data.get('email') or not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
        errors['email'] = 'Invalid'
    pwd = data.get('password') or ''
    if len(pwd) < 8: errors['password']='Min 8 chars'
    return errors
