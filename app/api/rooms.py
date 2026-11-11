from flask import Blueprint, jsonify

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/api/v1/rooms', methods=['GET'])
def get_rooms():
    return jsonify([{"id": 1, "name": "General"}]), 200

@rooms_bp.route('/api/v1/rooms', methods=['POST'])
def create_room():
    return jsonify({"id": 2, "name": "New Room"}), 201

@rooms_bp.route('/api/v1/rooms/<int:room_id>/messages', methods=['GET'])
def get_messages(room_id):
    return jsonify([{"id": 101, "text": "Hello", "room_id": room_id}]), 200

@rooms_bp.route('/api/v1/rooms/<int:room_id>/messages', methods=['POST'])
def send_message(room_id):
    return jsonify({"id": 102, "text": "New message", "room_id": room_id}), 201

@rooms_bp.route('/api/v1/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    
    return '', 204
