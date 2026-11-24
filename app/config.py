import os
import sys

class Config:
    def __init__(self):
        # Обязательные переменные
        self.DB_HOST = self._require("DB_HOST")
        self.DB_PORT = self._require("DB_PORT")
        self.DB_USER = self._require("DB_USER")
        self.DB_PASSWORD = self._require("DB_PASSWORD")
        self.DB_NAME = self._require("DB_NAME")
        
        # Необязательные (со значениями по умолчанию)
        self.DB_MAX_CONNS = int(os.getenv("DB_MAX_CONNS", "10"))
        self.DB_CONN_RETRIES = int(os.getenv("DB_CONN_RETRIES", "10"))
        self.DB_CONN_RETRY_DELAY = float(os.getenv("DB_CONN_RETRY_DELAY", "2"))
        
        # Для Flask
        self.SERVICE_NAME = os.getenv("SERVICE_NAME", "ChatService")
        self.SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

    @staticmethod
    def _require(name: str) -> str:
        value = os.getenv(name)
        if value is None or value.strip() == "":
            print(f"[CONFIG ERROR] Обязательная переменная окружения '{name}' не задана.", file=sys.stderr)
            sys.exit(1) # Прекращаем запуск
        return value

config = Config()