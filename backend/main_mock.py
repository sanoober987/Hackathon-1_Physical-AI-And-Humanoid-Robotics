from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Physical AI & Humanoid Robotics API...")
    yield
    # Shutdown
    print("Shutting down Physical AI & Humanoid Robotics API...")

app = FastAPI(
    title="Physical AI & Humanoid Robotics API",
    description="Backend API for the Physical AI & Humanoid Robotics textbook project",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple chat request/response models
class ChatRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    language: str = "en"

class SelectedTextChatRequest(BaseModel):
    question: str
    selected_text: str
    user_id: Optional[str] = None
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    context_used: Optional[Dict[str, Any]] = None

# Mock services to avoid heavy dependencies during testing
class MockRAGService:
    async def process_query(self, query: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        # Mock response based on query
        if "physical ai" in query.lower():
            response = "Physical AI represents a paradigm shift in artificial intelligence, moving beyond traditional digital computation to embrace the challenges and opportunities of intelligent systems operating in the physical world. Unlike conventional AI that processes abstract symbols and data, Physical AI integrates perception, reasoning, and action within real-world environments."
        else:
            response = f"This is a mock response to your query: '{query}'. In the full implementation, this would be answered using RAG (Retrieval-Augmented Generation) with semantic search against the Physical AI & Humanoid Robotics textbook content."

        return {
            "response": response,
            "sources": [{"title": "Mock Source", "chapter": "Mock Chapter", "section": "Mock Section", "content_preview": "This is simulated content from the textbook..."}],
            "context_used": {"query": query, "retrieved_docs_count": 1, "user_profile_used": user_profile is not None}
        }

    async def process_selected_text_query(self, query: str, selected_text: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        response = f"Based on the selected text '{selected_text[:50]}...' and your question '{query}', here is a relevant answer. In the full implementation, this would use RAG to provide contextual responses."

        return {
            "response": response,
            "sources": [{"title": "Selected Text Context", "chapter": "Relevant Chapter", "section": "Relevant Section", "content_preview": selected_text[:100] + "..."}],
            "context_used": {"query": query, "selected_text": selected_text, "retrieved_docs_count": 1, "user_profile_used": user_profile is not None}
        }

# Initialize mock service
rag_service = MockRAGService()

# Mock user profile service
class MockUserProfileService:
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "level": "intermediate",
            "interests": ["robotics", "AI"],
            "preferences": [],
            "learning_history": [],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }

user_profile_service = MockUserProfileService()

# Mock translation service
class MockTranslationService:
    def translate_text(self, text: str, target_lang: str = "ur", source_lang: str = "en") -> str:
        if target_lang == "ur":
            return f"[URDU TRANSLATION MOCK: {text[:30]}...]"
        return text

translation_service = MockTranslationService()

# Mock rate limiter
class MockRateLimiter:
    def is_allowed(self, user_id: str, max_requests: int = None) -> bool:
        return True  # Allow all requests in mock version

    def get_remaining_requests(self, user_id: str, max_requests: int = None) -> int:
        return 100

rate_limiter = MockRateLimiter()
global_rate_limiter = MockRateLimiter()

# Mock chat logger
def mock_log_chat_interaction(db, user_id, question, response, sources=None, context_used=None, language="en", selected_text=None, response_time_ms=None, session_id=None):
    print(f"Mock logging: {user_id} asked '{question[:30]}...' in {language}")

# Import database dependencies conditionally to avoid issues
try:
    from sqlalchemy.orm import Session
    def get_db():
        # Mock database dependency
        yield None
    HAS_DATABASE = True
except ImportError:
    def get_db():
        yield None
    HAS_DATABASE = False

# Chat endpoints
@app.post("/api/v1/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db) if HAS_DATABASE else None):
    """Main chat endpoint for normal QA from the whole book"""
    try:
        # Get user profile if user_id provided
        user_profile = None
        if request.user_id:
            user_profile = user_profile_service.get_user_profile(request.user_id)

        # Process the query using mock RAG
        response_data = await rag_service.process_query(
            query=request.question,
            user_id=request.user_id,
            user_profile=user_profile
        )

        # Mock translation if needed
        original_response = response_data['response']
        if request.language != "en":
            response_data['response'] = translation_service.translate_text(
                response_data['response'],
                target_lang=request.language
            )

        # Mock logging
        mock_log_chat_interaction(
            db=db,
            user_id=request.user_id,
            question=request.question,
            response=original_response if request.language == "en" else response_data['response'],
            sources=response_data.get('sources', []),
            context_used=response_data.get('context_used', {}),
            language=request.language
        )

        return ChatResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@app.post("/api/v1/chat/selected", response_model=ChatResponse)
async def chat_selected_text(request: SelectedTextChatRequest, db: Session = Depends(get_db) if HAS_DATABASE else None):
    """Chat endpoint for selected-text QA (user highlights text and asks a question)"""
    try:
        # Get user profile if user_id provided
        user_profile = None
        if request.user_id:
            user_profile = user_profile_service.get_user_profile(request.user_id)

        # Process the query using mock RAG with selected text context
        response_data = await rag_service.process_selected_text_query(
            query=request.question,
            selected_text=request.selected_text,
            user_id=request.user_id,
            user_profile=user_profile
        )

        # Mock translation if needed
        original_response = response_data['response']
        if request.language != "en":
            response_data['response'] = translation_service.translate_text(
                response_data['response'],
                target_lang=request.language
            )

        # Mock logging
        mock_log_chat_interaction(
            db=db,
            user_id=request.user_id,
            question=request.question,
            response=original_response if request.language == "en" else response_data['response'],
            sources=response_data.get('sources', []),
            context_used=response_data.get('context_used', {}),
            language=request.language,
            selected_text=request.selected_text
        )

        return ChatResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")

@app.get("/api/v1/chat/capabilities")
async def get_chat_capabilities():
    """Get the capabilities of the chatbot"""
    return {
        "capabilities": [
            "Normal QA from the whole book",
            "Selected-text QA (user highlights text and asks a question)",
            "Personalized answers based on user profile",
            "Urdu translation support",
            "Context-aware responses using RAG",
            "Source citations from book sections"
        ],
        "supported_languages": ["en", "ur"],
        "rag_enabled": True,
        "knowledge_base_size": "Comprehensive textbook content",
        "status": "Operational (Mock Implementation)"
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to Physical AI & Humanoid Robotics API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Physical AI & Humanoid Robotics API", "dependencies": "mocked for testing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)