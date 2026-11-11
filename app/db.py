import time
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()

def init_db_with_retries(app, retries=5, delay=3):
    """
    Инициализация БД с повторными попытками подключения.
    """
    db.init_app(app)
    
    with app.app_context():
        for attempt in range(retries):
            try:
                # Пробуем выполнить простой запрос, чтобы проверить соединение
                db.session.execute(db.text('SELECT 1'))
                logging.info("Успешное подключение к базе данных MySQL.")
                return
            except OperationalError as e:
                logging.warning(f"Попытка {attempt + 1}/{retries} не удалась: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    logging.error("Не удалось подключиться к БД после всех попыток.")
                    raise e