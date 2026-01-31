from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from models.personalization import PersonalizationSettingCreate, PersonalizationSettingResponse
from models.user import UserResponse
from utils.database import get_db
from routes.auth import oauth2_scheme, get_current_user

router = APIRouter()

# Request models for the frontend API calls
class PreferencesRequest(BaseModel):
    user_id: str
    preferences: Dict[str, Any]

class LanguagePreferencesRequest(BaseModel):
    user_id: str
    language: str
    timestamp: str

class SuccessResponse(BaseModel):
    success: bool
    message: str

@router.post("/preferences", response_model=SuccessResponse)
async def save_preferences(request: PreferencesRequest):
    """
    Save user preferences from the frontend
    """
    # In a real implementation, this would save to database
    # For now, just return success
    print(f"Saving preferences for user {request.user_id}: {request.preferences}")

    return SuccessResponse(
        success=True,
        message="Preferences saved successfully"
    )

@router.post("/language-preferences", response_model=SuccessResponse)
async def save_language_preferences(request: LanguagePreferencesRequest):
    """
    Save language preferences from the frontend
    """
    # In a real implementation, this would save to database
    # For now, just return success
    print(f"Saving language preferences for user {request.user_id}: {request.language}")

    return SuccessResponse(
        success=True,
        message="Language preferences saved successfully"
    )

@router.get("/", response_model=List[PersonalizationSettingResponse])
async def get_personalization_settings(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all personalization settings for the current user
    """
    from models.personalization import PersonalizationSetting

    settings = db.query(PersonalizationSetting).filter(
        PersonalizationSetting.user_id == current_user.id
    ).all()

    return settings

@router.post("/", response_model=PersonalizationSettingResponse)
async def create_personalization_setting(
    setting: PersonalizationSettingCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new personalization setting for the current user
    """
    from models.personalization import PersonalizationSetting

    db_setting = PersonalizationSetting(
        user_id=current_user.id,
        setting_name=setting.setting_name,
        setting_value=setting.setting_value
    )

    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)

    return db_setting

@router.put("/{setting_id}", response_model=PersonalizationSettingResponse)
async def update_personalization_setting(
    setting_id: int,
    setting: PersonalizationSettingCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing personalization setting
    """
    from models.personalization import PersonalizationSetting

    db_setting = db.query(PersonalizationSetting).filter(
        PersonalizationSetting.id == setting_id,
        PersonalizationSetting.user_id == current_user.id
    ).first()

    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db_setting.setting_name = setting.setting_name
    db_setting.setting_value = setting.setting_value

    db.commit()
    db.refresh(db_setting)

    return db_setting

@router.delete("/{setting_id}")
async def delete_personalization_setting(
    setting_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a personalization setting
    """
    from models.personalization import PersonalizationSetting

    db_setting = db.query(PersonalizationSetting).filter(
        PersonalizationSetting.id == setting_id,
        PersonalizationSetting.user_id == current_user.id
    ).first()

    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db.delete(db_setting)
    db.commit()

    return {"message": "Setting deleted successfully"}
