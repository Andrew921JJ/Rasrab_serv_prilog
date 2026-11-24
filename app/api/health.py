from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import db
from ..config import config

# Объявляем Blueprint с именем 'health_bp'
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    try:
        # Проверяем подключение к БД через SQLAlchemy
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "status": "ok", 
            "db": "up", 
            "service": config.SERVICE_NAME
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error", 
            "db": "down"
        }), 503