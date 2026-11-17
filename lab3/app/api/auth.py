from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    # Логика входа...
    return jsonify({"message": "Login successful", "token": "fake-jwt-token"}), 200

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    # Логика регистрации...
    return jsonify({"message": "User created"}), 201
