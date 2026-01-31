from sqlalchemy import Column, String, Text, Integer
from pydantic import BaseModel as PydanticModel
from .base import BaseModel

class Chapter(BaseModel):
    __tablename__ = "chapters"
    
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    language = Column(String, default="en")  # For multilingual support

# Pydantic models for API
class ChapterBase(PydanticModel):
    title: str
    slug: str
    content: str
    language: str = "en"

class ChapterCreate(ChapterBase):
    pass

class ChapterResponse(ChapterBase):
    id: int

    class Config:
        from_attributes = True
