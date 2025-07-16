from ..extensions import bcrypt

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(plain, hashed):
    return bcrypt.check_password_hash(hashed, plain)
