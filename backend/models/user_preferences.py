from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class UserPreferences(BaseModel):
    user_id: str
    preferred_language: str = "en"
    learning_style: str = "visual"  # visual, auditory, reading/writing, kinesthetic
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced
    modules_completed: List[str] = []
    bookmarks: List[Dict[str, Any]] = []
    personalization_enabled: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True