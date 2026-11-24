import pytest
from unittest.mock import MagicMock
from app.services.post_service import PostService
from app.domain.models import Post
from app.domain.errors import ErrInvalidInput

def test_create_post_short_title():
    # Arrange: Создаем заглушку репозитория
    mock_repo = MagicMock()
    service = PostService(mock_repo)
    
    # Act & Assert: Проверяем нарушение бизнес-правила (заголовок < 3 символов)
    with pytest.raises(ErrInvalidInput):
        service.create_post(author_id="user-1", title="A", content="Text")
    
    # Проверяем, что репозиторий не вызывался (бизнес-правило сработало до БД)
    mock_repo.create.assert_not_called()

def test_create_post_success():
    # Arrange
    mock_repo = MagicMock()
    # Имитируем успешный ответ от БД
    mock_repo.create.return_value = Post(
        id="post-1", author_id="user-1", title="Valid Title", 
        content="Text", status="draft", created_at=None
    )
    service = PostService(mock_repo)
    
    # Act
    dto = service.create_post(author_id="user-1", title="Valid Title", content="Text")
    
    # Assert
    assert dto.title == "Valid Title"
    assert dto.id == "post-1"
    mock_repo.create.assert_called_once_with("user-1", "Valid Title", "Text")