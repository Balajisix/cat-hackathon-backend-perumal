from ..models.user import User
from ..extensions import db
from ..utils.hashing import hash_password, check_password
from flask import session
from app.utils.password_generator import generate_password


generated_pw = generate_password()

def register_user(data):
    if not data.get('username') or not data.get('email') or not data.get('password') or not data.get('role'):
        raise ValueError("Missing required fields")
    
    hashed_password = hash_password(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=data['role']
    ) 
    db.session.add(new_user)
    db.session.commit()
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

def login_user(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        raise ValueError("Missing required fields")
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password):
        raise ValueError("Invalid email or password")
    session['user_id'] = user.id
    session['username'] = user.username
    session['email'] = user.email
    session['role'] = user.role     
    session['is_logged_in'] = True

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role  
    }
def create_worker(data):
    if not data.get('username') or not data.get('email'):
        raise ValueError("Missing required fields")

    if User.query.filter_by(email=data['email']).first():
        raise ValueError("User with this email already exists")

    raw_password = generate_password()
    hashed_password = hash_password(raw_password)

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role='worker'
    )

    db.session.add(new_user)
    db.session.commit()
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "generated_password": raw_password 
    }

def logout_user():
    session.clear() 
    return {"message": "User logged out successfully"}