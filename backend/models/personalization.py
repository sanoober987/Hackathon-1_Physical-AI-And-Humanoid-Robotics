from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticModel
from .base import BaseModel

class PersonalizationSetting(BaseModel):
    __tablename__ = "personalization_settings"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    setting_name = Column(String)
    setting_value = Column(JSON)  # Store as JSON for flexibility
    
    # Relationship
    user = relationship("User", back_populates="personalization_settings")

# Pydantic models for API
class PersonalizationSettingBase(PydanticModel):
    setting_name: str
    setting_value: dict

class PersonalizationSettingCreate(PersonalizationSettingBase):
    pass

class PersonalizationSettingResponse(PersonalizationSettingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
