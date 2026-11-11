import os



PROJECT_STRUCTURE = {
    # Корневые файлы
    "requirements.txt": """Flask==3.0.0
python-dotenv==1.0.0
""",
    ".env": """FLASK_APP=run.py
FLASK_ENV=development
PORT=5000
SERVICE_NAME=ChatService
SERVICE_VERSION=1.0.0
""",
    "run.py": """from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    # Запуск сервера
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
""",

    # Пакет app
    "app/__init__.py": """from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Регистрация Blueprints (маршрутов)
    from app.api.health import health_bp
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.rooms import rooms_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)

    return app
""",
    "app/config.py": """import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

class Config:
    \"\"\"Базовый класс конфигурации\"\"\"
    SERVICE_NAME = os.getenv("SERVICE_NAME", "DefaultService")
    SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_ENV") == "development"
""",

    # Пакет app/api
    "app/api/__init__.py": "",
    "app/api/health.py": """from flask import Blueprint, jsonify
from app.services.health_service import HealthService

# Создаем Blueprint для группы эндпоинтов здоровья
health_bp = Blueprint('health', __name__)

@health_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    \"\"\"
    GET /api/v1/health
    Возвращает 200 OK и информацию о сервисе.
    \"\"\"
    data = HealthService.get_health_status()
    return jsonify(data), 200
""",
    "app/api/auth.py": """from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    # Логика входа...
    return jsonify({"message": "Login successful", "token": "fake-jwt-token"}), 200

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    # Логика регистрации...
    return jsonify({"message": "User created"}), 201
""",
    "app/api/users.py": """from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/me', methods=['GET'])
def get_me():
    return jsonify({"id": 1, "username": "testuser"}), 200
""",
    "app/api/rooms.py": """from flask import Blueprint, jsonify

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
    # Логика удаления
    return '', 204
""",

    # Пакет app/services
    "app/services/__init__.py": "",
    "app/services/health_service.py": """import time
from app.config import Config

# Запоминаем время старта приложения
START_TIME = time.time()

class HealthService:
    @staticmethod
    def get_health_status():
        \"\"\"
        Формирует базовую информацию о сервисе.
        \"\"\"
        uptime_seconds = time.time() - START_TIME
        
        return {
            "status": "200 OK",
            "service": {
                "name": Config.SERVICE_NAME,
                "version": Config.SERVICE_VERSION,
                "uptime": f"{uptime_seconds:.2f} seconds"
            }
        }
"""
}

def create_project_structure(base_dir="."):
    """
    Создает структуру папок и файлов на основе словаря PROJECT_STRUCTURE.
    """
    print(f"Создание структуры проекта в: {os.path.abspath(base_dir)}")
    
    for path, content in PROJECT_STRUCTURE.items():
        full_path = os.path.join(base_dir, path)
        
        # Если content is None, это просто папка (не используется в текущем словаре, но полезно)
        if content is None:
            os.makedirs(full_path, exist_ok=True)
            print(f"[DIR]  {full_path}")
            continue

        # Создаем директорию, если её нет
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"[DIR]  {directory}")

        # Создаем файл и записываем контент
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[FILE] {full_path}")
        except Exception as e:
            print(f"[ERR]  Не удалось создать файл {full_path}: {e}")

    print("\nГотово! Структура проекта успешно создана.")
    print("Не забудьте установить зависимости: pip install -r requirements.txt")

if __name__ == "__main__":
    create_project_structure()