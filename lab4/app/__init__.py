from flask import Flask
from flask_migrate import Migrate
from .config import Config        # <--- Добавлена точка
from .db import init_db_with_retries, db  # <--- Добавлена точка

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Подключаем БД с ретраями
    init_db_with_retries(app)
    
    # Подключаем миграции
    migrate.init_app(app, db)

    # Импортируем модели, чтобы Alembic их "увидел"
    from . import models          # <--- Добавлена точка

    # Регистрация Blueprints (из папки api)
    from .api.health import health_bp
    from .api.auth import auth_bp
    from .api.users import users_bp
    from .api.rooms import rooms_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)

    return app