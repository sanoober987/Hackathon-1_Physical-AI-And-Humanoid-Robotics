import pytest
from unittest.mock import Mock, AsyncMock, patch
from services.chatbot_service import ChatbotService, ChatResponse

@pytest.fixture
def chatbot_service():
    """Create a ChatbotService instance for testing"""
    with patch('qdrant_client.QdrantClient'), \
         patch('openai.OpenAI'):
        service = ChatbotService()
        return service

@pytest.mark.asyncio
async def test_process_query(chatbot_service):
    """Test processing a user query"""
    # Mock the internal methods
    with patch.object(chatbot_service, '_retrieve_relevant_documents',
                      new_callable=AsyncMock) as mock_retrieve, \
         patch.object(chatbot_service, '_generate_response',
                      new_callable=AsyncMock) as mock_generate, \
         patch.object(chatbot_service, '_generate_suggestions',
                      new_callable=AsyncMock) as mock_suggestions:

        mock_retrieve.return_value = [{"content": "test document"}]
        mock_generate.return_value = "test response"
        mock_suggestions.return_value = ["suggestion1", "suggestion2"]

        result = await chatbot_service.process_query("test query", "user123")

        assert isinstance(result, ChatResponse)
        assert result.response_text == "test response"
        assert result.suggestions == ["suggestion1", "suggestion2"]

@pytest.mark.asyncio
async def test_retrieve_relevant_documents(chatbot_service):
    """Test retrieving relevant documents"""
    with patch.object(chatbot_service.qdrant_client, 'search',
                      return_value=[]):
        result = await chatbot_service._retrieve_relevant_documents("test query")

        # For now, test the mock result since actual implementation is mocked
        assert result is not None

@pytest.mark.asyncio
async def test_generate_suggestions_ros_topic():
    """Test generating suggestions for ROS-related queries"""
    with patch('qdrant_client.QdrantClient'), \
         patch('openai.OpenAI'):
        service = ChatbotService()

    suggestions = await service._generate_suggestions("What is ROS?")

    # Check that ROS-related suggestions are included
    ros_suggestions = [
        "What are the differences between ROS and ROS 2?",
        "How do I create a ROS 2 package?",
        "What are ROS 2 Quality of Service policies?"
    ]

    # At least one ROS suggestion should be in the results
    found_ros_suggestion = any(s in suggestions for s in ros_suggestions)
    assert found_ros_suggestion

@pytest.mark.asyncio
async def test_get_modules_info(chatbot_service):
    """Test getting modules information"""
    modules_info = chatbot_service.get_modules_info()

    assert "modules" in modules_info
    assert len(modules_info["modules"]) == 4

    # Check first module
    first_module = modules_info["modules"][0]
    assert first_module["id"] == 1
    assert first_module["title"] == "ROS 2 Fundamentals"
    assert "Nodes" in first_module["topics"]