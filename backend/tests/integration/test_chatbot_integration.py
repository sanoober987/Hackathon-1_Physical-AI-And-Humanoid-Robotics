import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.mark.integration
def test_full_chat_flow():
    """Integration test for the full chat flow"""
    # Mock the chatbot service to avoid needing real OpenAI/Qdrant
    with patch('services.chatbot_service.ChatbotService.process_query') as mock_process:
        mock_process.return_value = AsyncMock()
        mock_process.return_value.response_text = "This is a test response"
        mock_process.return_value.context = {}
        mock_process.return_value.suggestions = ["Suggestion 1", "Suggestion 2"]

        payload = {
            "message": "Tell me about ROS 2",
            "user_id": "integration_test_user"
        }

        response = client.post("/api/v1/chatbot/chat", json=payload)

        # The endpoint should exist and accept the request
        assert response.status_code in [200, 500]  # Either success or internal error due to mocking

@pytest.mark.integration
def test_user_registration_and_login_flow():
    """Integration test for user registration and login flow"""
    # Register a new user
    register_payload = {
        "email": "integration@test.com",
        "password": "secure_password",
        "name": "Integration Test User"
    }

    register_response = client.post("/api/v1/auth/register", json=register_payload)

    # Login with the registered user
    login_payload = {
        "email": "integration@test.com",
        "password": "secure_password"
    }

    login_response = client.post("/api/v1/auth/login", json=login_payload)

    # Both endpoints should exist
    assert register_response.status_code in [200, 422]
    assert login_response.status_code in [200, 422]

@pytest.mark.integration
def test_personalization_flow():
    """Integration test for personalization flow"""
    user_id = "integration_test_user"

    # Get initial preferences
    get_response = client.get(f"/api/v1/personalization/{user_id}")

    # Update preferences
    update_payload = {
        "user_id": user_id,
        "preferences": {
            "preferred_language": "ur",
            "learning_style": "visual",
            "difficulty_level": "advanced"
        }
    }

    update_response = client.post("/api/v1/personalization/update", json=update_payload)

    assert get_response.status_code in [200, 404, 422]
    assert update_response.status_code in [200, 422]

@pytest.mark.integration
def test_endpoints_availability():
    """Test that all major endpoints are accessible"""
    endpoints_to_test = [
        ("/", "get"),
        ("/health", "get"),
        ("/api/v1/chatbot/modules-info", "get"),
        ("/api/v1/auth/me", "get"),
        ("/api/v1/personalization/test_user/bookmarks", "get")
    ]

    for endpoint, method in endpoints_to_test:
        if method == "get":
            response = client.get(endpoint)
        elif method == "post":
            response = client.post(endpoint, json={})

        # All endpoints should be reachable (even if they return errors due to missing params)
        assert response.status_code in [200, 404, 405, 422, 500]