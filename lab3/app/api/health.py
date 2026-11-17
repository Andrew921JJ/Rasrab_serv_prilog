from flask import Blueprint, jsonify
from app.services.health_service import HealthService

# Создаем Blueprint для группы эндпоинтов здоровья
health_bp = Blueprint('health', __name__)

@health_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    GET /api/v1/health
    Возвращает 200 OK и информацию о сервисе.
    """
    data = HealthService.get_health_status()
    return jsonify(data), 200
