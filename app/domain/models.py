from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str = field(repr=False) # Скрываем из вывода (п.1)
    role: str
    created_at: datetime

@dataclass
class Post:
    id: str
    author_id: str
    title: str
    content: str
    status: str
    created_at: datetime

@dataclass
class Comment:
    id: str
    post_id: str
    user_id: str
    content: str
    parent_id: Optional[str] = None
    created_at: Optional[datetime] = None