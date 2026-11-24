import psycopg
from psycopg.rows import dict_row
from typing import List, Optional
import uuid

from app.domain.models import User, Post, Comment
from app.domain.repositories import IUserRepository, IPostRepository
from app.domain.errors import ErrNotFound, ErrAlreadyExists, ErrConflict, ErrInvalidInput

class PgUserRepository(IUserRepository):
    def __init__(self, pool):
        self.pool = pool

    # <--- ВАЖНО: Отступ выровнен с __init__ (4 пробела)
    def create(self, username: str, email: str, password_hash: str, role: str) -> User:
        user_id = str(uuid.uuid4())
        query = """
            INSERT INTO users (id, username, email, password_hash, role, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id, username, email, password_hash, role, created_at
        """
        try:
            with self.pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query, (user_id, username, email, password_hash, role))
                    row = cur.fetchone()
                    return User(**row)
        except psycopg.errors.UniqueViolation:
            raise ErrAlreadyExists(f"Пользователь с email {email} уже существует")
    def get_by_id(self, user_id: str) -> User:
        query = "SELECT id, username, email, password_hash, role, created_at FROM users WHERE id = %s"
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (user_id,))
                row = cur.fetchone()
                if not row:
                    raise ErrNotFound(f"Пользователь с ID {user_id} не найден")
                return User(**row)

    def get_by_email(self, email: str) -> User:
        query = "SELECT id, username, email, password_hash, role, created_at FROM users WHERE email = %s"
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (email,))
                row = cur.fetchone()
                if not row:
                    raise ErrNotFound("Пользователь не найден")
                return User(**row)

    def list(self, limit: int, offset: int) -> List[User]:
        query = "SELECT id, username, email, password_hash, role, created_at FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s"
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (limit, offset))
                return [User(**row) for row in cur.fetchall()]

    def update(self, user_id: str, username: str, email: str) -> User:
        query = """
            UPDATE users 
            SET username = %s, email = %s 
            WHERE id = %s 
            RETURNING id, username, email, password_hash, role, created_at
        """
        try:
            with self.pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query, (username, email, user_id))
                    if cur.rowcount == 0:
                        raise ErrNotFound(f"Пользователь {user_id} не найден")
                    row = cur.fetchone()
                    return User(**row)
        except psycopg.errors.UniqueViolation:
             raise ErrConflict("Email уже занят другим пользователем")

    def delete(self, user_id: str) -> None:
        query = "DELETE FROM users WHERE id = %s"
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                if cur.rowcount == 0:
                    raise ErrNotFound(f"Пользователь {user_id} не найден")


# ==========================================
# РЕАЛИЗАЦИЯ ДЛЯ ПОСТОВ
# ==========================================
class PgPostRepository(IPostRepository):
    def __init__(self, pool):
        self.pool = pool

    def create(self, author_id: str, title: str, content: str, status: str = 'draft') -> Post:
        post_id = str(uuid.uuid4()) # <--- ДОБАВЛЕНА генерация ID для поста
        query = """
            INSERT INTO posts (id, author_id, title, content, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, author_id, title, content, status, created_at
        """
        try:
            with self.pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query, (post_id, author_id, title, content, status))
                    row = cur.fetchone()
                    return Post(**row)
        except psycopg.errors.ForeignKeyViolation:
            raise ErrInvalidInput(f"Автор с ID {author_id} не существует")
        except psycopg.errors.UniqueViolation:
            raise ErrAlreadyExists(f"Пост с таким названием/слоганом уже существует")

    def get_by_id(self, post_id: str) -> Post:
        query = "SELECT id, author_id, title, content, status, created_at FROM posts WHERE id = %s"
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (post_id,))
                row = cur.fetchone()
                if not row:
                    raise ErrNotFound(f"Пост с ID {post_id} не найден")
                return Post(**row)

    def list(self, limit: int, offset: int) -> List[Post]:
        query = """
            SELECT id, author_id, title, content, status, created_at 
            FROM posts 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, (limit, offset))
                return [Post(**row) for row in cur.fetchall()]

    def delete(self, post_id: str) -> None:
        query = "DELETE FROM posts WHERE id = %s"
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (post_id,))
                if cur.rowcount == 0:
                    raise ErrNotFound(f"Пост {post_id} не найден")

    # ==========================================
    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
    # ==========================================
    def create_comment_safe(self, post_id: str, user_id: str, content: str) -> str:
        comment_id = str(uuid.uuid4()) # <--- ДОБАВЛЕНА генерация ID для комментария
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM posts WHERE id = %s FOR UPDATE", (post_id,))
                if cur.fetchone() is None:
                    raise ErrNotFound("Пост не найден или был удален")
                
                cur.execute(
                    "INSERT INTO comments (id, post_id, user_id, content) VALUES (%s, %s, %s, %s) RETURNING id",
                    (comment_id, post_id, user_id, content)
                )
                return comment_id