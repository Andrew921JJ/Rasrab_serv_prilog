import time
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from .config import config

logger = logging.getLogger(__name__)

# Создаем объект SQLAlchemy (его будет использовать Flask-Migrate)
db = SQLAlchemy()

def init_db_with_retries(app):
    """
    Инициализирует подключение к PostgreSQL с повторными попытками при старте.
    """
    # Формируем строку подключения для PostgreSQL (используем драйвер psycopg 3)
    db_uri = (
        f"postgresql+psycopg://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Настройки пула соединений (ограниченный размер)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': config.DB_MAX_CONNS,
        'max_overflow': 2,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }

    # Инициализируем SQLAlchemy с приложением
    db.init_app(app)

    # Делаем повторные попытки подключения при старте
    retries = config.DB_CONN_RETRIES
    delay = config.DB_CONN_RETRY_DELAY
    
    for attempt in range(1, retries + 1):
        try:
            # Пытаемся выполнить простой запрос, чтобы проверить соединение
            with app.app_context():
                db.session.execute(text("SELECT 1"))
                db.session.commit()
            logger.info(f"Подключение к БД установлено (попытка {attempt}).")
            return
        except OperationalError as e:
            logger.warning(
                f"Попытка {attempt}/{retries} не удалась: {e}. "
                f"Повтор через {delay} сек."
            )
            if attempt == retries:
                raise RuntimeError(f"Не удалось подключиться к БД после {retries} попыток.") from e
            time.sleep(delay)