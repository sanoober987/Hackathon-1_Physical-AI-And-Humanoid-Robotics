import pytest
from datetime import datetime
from models.user import User, UserCreate, UserResponse
from models.user_preferences import UserPreferences

def test_user_creation():
    """Test creating a user model"""
    user = User(
        id="test_user_id",
        email="test@example.com",
        name="Test User",
        created_at=datetime.utcnow()
    )

    assert user.id == "test_user_id"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert isinstance(user.created_at, datetime)

def test_user_create_model():
    """Test UserCreate model validation"""
    user_create = UserCreate(
        email="newuser@example.com",
        name="New User",
        password="secure_password"
    )

    assert user_create.email == "newuser@example.com"
    assert user_create.name == "New User"
    assert user_create.password == "secure_password"

def test_user_response_model():
    """Test UserResponse model conversion"""
    user = User(
        id="test_user_id",
        email="test@example.com",
        name="Test User",
        created_at=datetime.utcnow()
    )

    user_response = UserResponse.from_orm(user)

    assert user_response.id == "test_user_id"
    assert user_response.email == "test@example.com"
    assert user_response.name == "Test User"

def test_user_preferences_default_values():
    """Test UserPreferences model with default values"""
    prefs = UserPreferences(user_id="test_user")

    assert prefs.user_id == "test_user"
    assert prefs.preferred_language == "en"
    assert prefs.learning_style == "visual"
    assert prefs.difficulty_level == "intermediate"
    assert prefs.modules_completed == []
    assert prefs.bookmarks == []
    assert prefs.personalization_enabled is True

def test_user_preferences_custom_values():
    """Test UserPreferences model with custom values"""
    custom_prefs = UserPreferences(
        user_id="test_user",
        preferred_language="ur",
        learning_style="auditory",
        difficulty_level="advanced",
        modules_completed=["1", "2"],
        bookmarks=[{"id": "1", "title": "Test"}],
        personalization_enabled=False
    )

    assert custom_prefs.preferred_language == "ur"
    assert custom_prefs.learning_style == "auditory"
    assert custom_prefs.difficulty_level == "advanced"
    assert custom_prefs.modules_completed == ["1", "2"]
    assert custom_prefs.bookmarks == [{"id": "1", "title": "Test"}]
    assert custom_prefs.personalization_enabled is False