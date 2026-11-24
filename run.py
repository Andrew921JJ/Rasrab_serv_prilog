import os
from app import create_app

# Создаем приложение с помощью фабрики
app = create_app()

if __name__ == '__main__':
    # Запускаем встроенный сервер Flask для разработки
    # (В Docker с Gunicorn эта часть кода не выполняется)
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)