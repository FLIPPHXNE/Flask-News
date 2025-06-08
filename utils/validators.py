import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_user_data(data, is_update=False):
    errors = {}

    if not is_update or 'first_name' in data:
        if not data.get('first_name') or len(data['first_name']) > 50:
            errors['first_name'] = 'Invalid first name (1-50 characters)'

    if not is_update or 'last_name' in data:
        if not data.get('last_name') or len(data['last_name']) > 50:
            errors['last_name'] = 'Invalid last name (1-50 characters)'

    if not is_update or 'email' in data:
        email = data.get('email', '')
        if not email or not validate_email(email):
            errors['email'] = 'Invalid email format'

    if not is_update or 'password' in data:
        password = data.get('password', '')
        if not password or len(password) < 6:
            errors['password'] = 'Password too short (min 6 characters)'

    return errors