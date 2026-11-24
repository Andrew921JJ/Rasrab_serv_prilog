from flask import Flask, jsonify
from flask_migrate import Migrate
from .config import Config
from .db import init_db_with_retries, db
import atexit # <--- Добавлен импорт

migrate = Migrate()

def register_error_handlers(app):
    from .domain.errors import ErrNotFound, ErrAlreadyExists, ErrConflict, ErrInvalidInput
    
    @app.errorhandler(ErrNotFound)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(ErrAlreadyExists)
    def handle_already_exists(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(ErrConflict)
    def handle_conflict(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(ErrInvalidInput)
    def handle_invalid_input(e):
        return jsonify({"error": str(e)}), 422


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db_with_retries(app)
    migrate.init_app(app, db)

    from . import models

    # ==========================================
    # ИНИЦИАЛИЗАЦИЯ РЕПОЗИТОРИЕВ (ЛР №6)
    # ==========================================
    from .infrastructure.repositories_pg import PgUserRepository, PgPostRepository
    from psycopg_pool import ConnectionPool
    import os
    
    conninfo = f"host={os.getenv('DB_HOST', 'db')} port={os.getenv('DB_PORT', 5432)} " \
               f"user={os.getenv('DB_USER', 'app')} password={os.getenv('DB_PASSWORD', 'supersecret')} " \
               f"dbname={os.getenv('DB_NAME', 'appdb')}"
    
    # Открываем пул
    pool = ConnectionPool(conninfo=conninfo, min_size=1, max_size=10)
    pool.open()

    # Сохраняем пул в конфиге, чтобы его можно было закрыть
    app.config['DB_POOL'] = pool

    # Регистрируем закрытие пула при остановке приложения (чтобы убрать RuntimeError из логов)
    @atexit.register
    def close_db_pool():
        if not pool.closed:
            pool.close()

    # Сохраняем репозитории
    app.config['USER_REPO'] = PgUserRepository(pool)
    app.config['POST_REPO'] = PgPostRepository(pool)

    # ==========================================
    # РЕГИСТРАЦИЯ BLUEPRINTS
    # ==========================================
    from .api.health import health_bp
    from .api.auth import auth_bp
    from .api.users import users_bp
    from .api.rooms import rooms_bp
    from .api.posts import posts_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(posts_bp, url_prefix='/api/posts')

    # ==========================================
    # РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ОШИБОК
    # ==========================================
    register_error_handlers(app)

    return app