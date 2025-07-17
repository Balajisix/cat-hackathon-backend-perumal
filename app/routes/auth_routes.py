from flask import Blueprint, jsonify, request
from ..services.auth_service import register_user, login_user, logout_user, create_worker
from flask import session
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

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
    
@admin_bp.route('/create-worker', methods=['POST'])
def add_worker():
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    try:
        result = create_worker(data)
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@auth_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"message": "Authenticated user", "user_id": user_id}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():  
    try:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400