from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import asyncio
from datetime import datetime

load_dotenv()

class UserProfile(BaseModel):
    user_id: str
    level: str = "intermediate"  # beginner, intermediate, advanced
    interests: List[str] = []
    preferences: List[str] = []
    learning_history: List[Dict[str, Any]] = []
    created_at: datetime = None
    updated_at: datetime = None

class UserProfileService:
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll simulate with a simple in-memory store
        self.user_profiles = {}

        # Database connection details for Neon Postgres
        self.db_url = os.getenv("NEON_DB_URL")

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user profile from database
        """
        # In a real implementation, this would query the database
        # For now, return a default profile or mock data

        # Check if profile exists in memory
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]

        # Create a default profile if it doesn't exist
        default_profile = {
            "user_id": user_id,
            "level": "intermediate",
            "interests": [],
            "preferences": [],
            "learning_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # Store in memory
        self.user_profiles[user_id] = default_profile
        return default_profile

    def create_or_update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update user profile in database
        """
        # Get existing profile or create new one
        existing_profile = self.get_user_profile(user_id)

        # Update with new data
        for key, value in profile_data.items():
            if key in existing_profile and key != "user_id":
                existing_profile[key] = value

        existing_profile["updated_at"] = datetime.now().isoformat()

        # Store updated profile
        self.user_profiles[user_id] = existing_profile

        return existing_profile

    def add_learning_history(self, user_id: str, topic: str, interaction_type: str = "query") -> Dict[str, Any]:
        """
        Add learning history entry for user
        """
        profile = self.get_user_profile(user_id)

        history_entry = {
            "topic": topic,
            "interaction_type": interaction_type,
            "timestamp": datetime.now().isoformat()
        }

        profile["learning_history"].append(history_entry)

        # Keep only last 50 history entries
        if len(profile["learning_history"]) > 50:
            profile["learning_history"] = profile["learning_history"][-50:]

        self.user_profiles[user_id] = profile
        return profile

    def get_personalized_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get personalized context for user based on profile
        """
        profile = self.get_user_profile(user_id)

        context = {
            "level": profile.get("level", "intermediate"),
            "interests": profile.get("interests", []),
            "recent_topics": [entry["topic"] for entry in profile.get("learning_history", [])[-5:]],
            "preferred_format": "detailed" if profile.get("level") == "advanced" else "balanced"
        }

        return context

    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user preferences asynchronously
        """
        profile = self.get_user_profile(user_id)

        # Update preferences
        if "interests" in preferences:
            profile["interests"] = list(set(profile.get("interests", []) + preferences["interests"]))

        if "level" in preferences:
            profile["level"] = preferences["level"]

        if "preferences" in preferences:
            profile["preferences"] = preferences["preferences"]

        profile["updated_at"] = datetime.now().isoformat()

        self.user_profiles[user_id] = profile
        return profile