from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..services.chatbot_service import ChatbotService

router = APIRouter()

# Initialize the chatbot service
chatbot_service = ChatbotService()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    context: Optional[Dict[str, Any]] = {}
    suggestions: List[str] = []

class KnowledgeQueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class KnowledgeQueryResponse(BaseModel):
    results: List[Dict[str, Any]]

@router.post("/message")
async def chat_message(request: ChatRequest):
    """
    Handle chat messages for the Physical AI & Humanoid Robotics textbook using RAG
    """
    try:
        # Process the query using the RAG system
        response = await chatbot_service.process_query(
            query=request.message,
            user_id=request.user_id,
            context=request.context
        )

        return ChatResponse(
            response=response.response_text,
            context=response.context,
            suggestions=response.suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@router.post("/query-knowledge")
async def query_knowledge(request: KnowledgeQueryRequest):
    """
    Query the knowledge base directly for relevant information
    """
    try:
        # Query the knowledge base
        results = chatbot_service.query_knowledge_base(request.query)

        return KnowledgeQueryResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying knowledge base: {str(e)}")

@router.get("/modules")
async def get_modules():
    """
    Get information about all textbook modules/chapters
    """
    try:
        modules_info = chatbot_service.get_modules_info()
        return modules_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving modules: {str(e)}")

@router.get("/capabilities")
async def get_chat_capabilities():
    """
    Get the capabilities of the chatbot
    """
    return {
        "capabilities": [
            "Answer questions about Physical AI",
            "Explain robotics concepts",
            "Provide examples of humanoid systems",
            "Discuss ethical considerations",
            "Reference textbook chapters",
            "Provide context-aware responses using RAG",
            "Generate follow-up suggestions"
        ],
        "supported_topics": [
            "kinematics",
            "control systems",
            "sensors and perception",
            "motion planning",
            "human-robot interaction",
            "ethics in robotics",
            "ROS2 fundamentals",
            "Digital twin technology",
            "NVIDIA Isaac platform",
            "Vision-Language-Action models"
        ],
        "rag_enabled": True,
        "knowledge_base_size": "Comprehensive textbook content"
    }
