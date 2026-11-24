from abc import ABC, abstractmethod
from typing import List, Optional
from .models import User, Post

class IUserRepository(ABC):
    @abstractmethod
    def create(self, username: str, email: str, password_hash: str, role: str) -> User: pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> User: pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> User: pass # Доп. метод для уникального поля
    
    @abstractmethod
    def list(self, limit: int, offset: int) -> List[User]: pass
    
    @abstractmethod
    def update(self, user_id: str, username: str, email: str) -> User: pass
    
    @abstractmethod
    def delete(self, user_id: str) -> None: pass

class IPostRepository(ABC):
    @abstractmethod
    def create(self, author_id: str, title: str, content: str, status: str) -> Post: pass
    
    @abstractmethod
    def get_by_id(self, post_id: str) -> Post: pass
    
    @abstractmethod
    def list(self, limit: int, offset: int) -> List[Post]: pass
    
    @abstractmethod
    def delete(self, post_id: str) -> None: pass