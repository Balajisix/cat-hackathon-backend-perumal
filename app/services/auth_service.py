from ..models.user import User
from ..extensions import db
from ..utils.hashing import hash_password, check_password
from flask import session
def register_user(data):
    if not data.get('username') or not data.get('email') or not data.get('password'):
        raise ValueError("Missing required fields")
    
    hashed_password = hash_password(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    ) 
    db.session.add(new_user)
    db.session.commit()
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

def login_user(data):
    if not data.get('email') or not data.get('password'):
        raise ValueError("Missing required fields")
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password(data['password'], user.password):
        raise ValueError("Invalid email or password")
    
    # Set session info (since you're using session auth)
    session['user_id'] = user.id
    session['username'] = user.username
    session['email'] = user.email
    session['is_logged_in'] = True

    return {"id": user.id, "username": user.username, "email": user.email}


def logout_user():
    session.clear()  # Clears all session data
    return {"message": "User logged out successfully"}