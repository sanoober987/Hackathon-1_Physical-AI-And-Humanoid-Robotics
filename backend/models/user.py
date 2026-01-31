from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticModel
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    personalization_settings = relationship("PersonalizationSetting", back_populates="user")

# Pydantic models for API
class UserBase(PydanticModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
