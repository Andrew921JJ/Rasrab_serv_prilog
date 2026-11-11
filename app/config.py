import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERVICE_NAME = os.getenv("SERVICE_NAME", "ChatService")
    SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_ENV") == "development"

    # Настройки MySQL (Драйвер PyMySQL)
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "chat_db")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Пул соединений с повторными попытками (Пункт 4)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 280, # MySQL обрывает соединения через 8 часов (28800 сек)
        "pool_pre_ping": True, # Проверка соединения перед использованием
    }