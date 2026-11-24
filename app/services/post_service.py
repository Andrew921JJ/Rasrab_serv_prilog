from app.infrastructure.repositories_pg import PgPostRepository
from app.domain.errors import ErrInvalidInput
from app.api.dto import PostDTO

class PostService:
    def __init__(self, post_repo: PgPostRepository):
        self.post_repo = post_repo

    def create_post(self, author_id: str, title: str, content: str) -> PostDTO:
        if not title or len(title) < 3:
            raise ErrInvalidInput("Заголовок должен быть не менее 3 символов")
        
        post = self.post_repo.create(author_id, title, content)
        return PostDTO(post.id, post.title, post.content, post.status, post.created_at)

    def get_post(self, post_id: str) -> PostDTO:
        post = self.post_repo.get_by_id(post_id)
        return PostDTO(post.id, post.title, post.content, post.status, post.created_at)

    def list_posts(self, limit: int, offset: int):
        posts = self.post_repo.list(limit, offset)
        return [PostDTO(p.id, p.title, p.content, p.status, p.created_at) for p in posts]

    def update_post(self, post_id: str, title: str, content: str) -> PostDTO:
        post = self.post_repo.update(post_id, title, content)
        return PostDTO(post.id, post.title, post.content, post.status, post.created_at)

    def delete_post(self, post_id: str):
        self.post_repo.delete(post_id)