import os
from psycopg_pool import ConnectionPool
from app import create_app
from app.infrastructure.repositories_pg import PgUserRepository, PgPostRepository

# 1. Создаем пул соединений (из ЛР №5)
# В Docker DB_HOST=db, при локальном запуске — localhost
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecret")
DB_NAME = os.getenv("DB_NAME", "appdb")

conninfo = f"host={DB_HOST} port={DB_PORT} user={DB_USER} password={DB_PASSWORD} dbname={DB_NAME}"
pool = ConnectionPool(conninfo=conninfo, min_size=1, max_size=int(os.getenv("DB_MAX_CONNS", 10)))
pool.open()

# 2. Инициализируем репозитории
user_repo = PgUserRepository(pool)
post_repo = PgPostRepository(pool)

# 3. Создаем приложение
app = create_app()

# Делаем репозитории доступными внутри приложения (например, через app.config)
# Это позволит использовать их в Blueprint'ах (контроллерах)
app.config['USER_REPO'] = user_repo
app.config['POST_REPO'] = post_repo

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)