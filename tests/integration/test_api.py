import pytest
from unittest.mock import MagicMock
from app import create_app
from pydantic import ValidationError

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Мокаем репозиторий, чтобы не лезть в БД
    app.config['POST_REPO'] = MagicMock()
    with app.test_client() as client:
        yield client

def test_validation_error(client):
    # B8: Ошибка валидации (пустой title)
    response = client.post('/api/posts/', json={
        "title": "", # Слишком короткий
        "content": "Valid content here",
        "author_id": "123e4567-e89b-12d3-a456-426614174000"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in data["error"]

def test_not_found(client):
    # B8: 404
    from app.domain.errors import ErrNotFound
    client.application.config['POST_REPO'].get_by_id.side_effect = ErrNotFound("Пост не найден")
    
    response = client.get('/api/posts/123e4567-e89b-12d3-a456-426614174000')
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"

def test_internal_server_error(client):
    # B8: 500 без раскрытия подробностей
    client.application.config['POST_REPO'].get_by_id.side_effect = Exception("Секретная информация")
    
    response = client.get('/api/posts/123e4567-e89b-12d3-a456-426614174000')
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "Секретная информация" not in data["error"]["message"] # Не раскрываем!

def test_unknown_field(client):
    # B4: Неизвестное поле в JSON
    response = client.post('/api/posts/', json={
        "title": "Valid Title",
        "content": "Valid content here",
        "author_id": "123e4567-e89b-12d3-a456-426614174000",
        "hacker_field": "attack" # Лишнее поле
    })
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"