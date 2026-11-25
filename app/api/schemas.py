from pydantic import BaseModel, Field, model_validator
from typing import Optional

# ==========================================
# СХЕМЫ ДЛЯ ПОСТОВ (B1)
# ==========================================
class PostCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=10)
    author_id: str = Field(..., pattern=r"^[0-9a-fA-F\-]{36}$")
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")

    model_config = {"extra": "forbid"} # B4: Запрет неизвестных полей

class PostUpdateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=10)
    
    model_config = {"extra": "forbid"}

# ==========================================
# СХЕМЫ ДЛЯ КОММЕНТАРИЕВ (B2 - проверка связи полей)
# ==========================================
class CommentCreateSchema(BaseModel):
    post_id: str = Field(..., pattern=r"^[0-9a-fA-F\-]{36}$")
    user_id: str = Field(..., pattern=r"^[0-9a-fA-F\-]{36}$")
    content: str = Field(..., min_length=2, max_length=1000)
    parent_id: Optional[str] = Field(None, pattern=r"^[0-9a-fA-F\-]{36}$")

    @model_validator(mode='after')
    def check_parent_and_content(self):
        # B2: Проверка связи двух полей
        if self.parent_id and len(self.content) < 5:
            raise ValueError("Ответ на комментарий должен быть не короче 5 символов")
        return self
    
    model_config = {"extra": "forbid"}