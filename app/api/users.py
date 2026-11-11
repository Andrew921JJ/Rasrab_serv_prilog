from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/me', methods=['GET'])
def get_me():
    return jsonify({"id": 1, "username": "testuser"}), 200
