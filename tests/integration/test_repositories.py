import pytest
import psycopg_pool
from datetime import datetime
from uuid import uuid4

from app.infrastructure.repositories_pg import PgUserRepository
from app.domain.errors import ErrNotFound, ErrAlreadyExists

@pytest.fixture(scope="module")
def pool():
    # Подключаемся к БД
    pool = psycopg_pool.ConnectionPool("host=db port=5432 user=app password=supersecret dbname=appdb")
    pool.open()
    yield pool
    pool.close()

@pytest.fixture
def repo(pool):
    # Очистка перед каждым тестом
    with pool.connection() as conn:
        conn.execute("TRUNCATE TABLE users CASCADE;")
    return PgUserRepository(pool)

def test_create_and_get(repo):
    # Сценарий 1: Создание и чтение (ID и created_at заполняются СУБД)
    email = f"test_{uuid4()}@test.com"
    user = repo.create(username="testuser", email=email, password_hash="hash", role="user")
    
    assert user.id is not None # СУБД сгенерировала UUID
    assert user.created_at is not None # СУБД поставила TIMESTAMP
    
    found = repo.get_by_id(user.id)
    assert found.email == email

def test_get_non_existent(repo):
    # Сценарий 2: Чтение несуществующей записи
    with pytest.raises(ErrNotFound):
        repo.get_by_id(str(uuid4()))

def test_create_duplicate(repo):
    # Сценарий 3: Повторное создание с тем же уникальным значением
    email = f"dup_{uuid4()}@test.com"
    repo.create(username="user1", email=email, password_hash="hash", role="user")
    
    with pytest.raises(ErrAlreadyExists):
        repo.create(username="user2", email=email, password_hash="hash", role="user")

def test_list_pagination(repo):
    # Сценарий 4: Постраничная выборка
    for i in range(15):
        repo.create(username=f"user{i}", email=f"user{i}@test.com", password_hash="hash", role="user")
    
    page1 = repo.list(limit=10, offset=0)
    page2 = repo.list(limit=10, offset=10)
    
    assert len(page1) == 10
    assert len(page2) == 5 # Остаток

def test_delete(repo):
    # Сценарий 5: Удаление и последующее чтение
    user = repo.create(username="todelete", email="del@test.com", password_hash="hash", role="user")
    repo.delete(user.id)
    
    with pytest.raises(ErrNotFound):
        repo.get_by_id(user.id)

def test_sql_injection(repo):
    # Сценарий 6: SQL-инъекция в GetByEmail
    # Пытаемся передать строку, которая "ломает" запрос
    malicious_email = "' OR '1'='1"
    
    # Если запрос параметризован (%s), база воспримет это как строку и ничего не найдет
    with pytest.raises(ErrNotFound):
        repo.get_by_email(malicious_email)