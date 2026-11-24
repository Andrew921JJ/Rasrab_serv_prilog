from app.infrastructure.repositories_pg import PgPostRepository
from app.domain.errors import ErrNotFound, ErrConflict, ErrInvalidInput
from app.api.dto import CommentDTO

class CommentService:
    def __init__(self, post_repo: PgPostRepository):
        self.post_repo = post_repo

    def create_comment(self, post_id: str, user_id: str, content: str) -> CommentDTO:
        post = self.post_repo.get_by_id(post_id)
        
        if post.status == 'archived':
            raise ErrConflict("Нельзя комментировать архивные посты")
        
        if len(content) < 2:
            raise ErrInvalidInput("Комментарий слишком короткий")

        comment_id = self.post_repo.create_comment_safe(post_id, user_id, content)
        
        return CommentDTO(
            id=comment_id, 
            post_id=post_id, 
            user_id=user_id, 
            content=content, 
            created_at=None
        )