import time
from app.config import Config

# Запоминаем время старта приложения
START_TIME = time.time()

class HealthService:
    @staticmethod
    def get_health_status():
        """
        Формирует базовую информацию о сервисе.
        """
        uptime_seconds = time.time() - START_TIME
        
        return {
            "status": "200 OK",
            "service": {
                "name": Config.SERVICE_NAME,
                "version": Config.SERVICE_VERSION,
                "uptime": f"{uptime_seconds:.2f} seconds"
            }
        }
