from flask import Blueprint, jsonify, request
from ..services.auth_service import register_user, login_user, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        user = register_user(data)
        return jsonify({"message": "User registered successfully", "user": user}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():   
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        user = login_user(data)
        return jsonify({"message": "Login successful", "user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@auth_bp.route('/logout', methods=['POST'])
def logout():  
    try:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400