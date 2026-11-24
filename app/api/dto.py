from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PostDTO:
    id: str
    title: str
    content: str
    status: str
    created_at: datetime

@dataclass
class CommentDTO:
    id: str
    post_id: str
    user_id: str
    content: str
    created_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }