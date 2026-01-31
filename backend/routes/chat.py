from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, AsyncGenerator
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Try to use the full RAG service, fall back to mock version for testing
try:
    from services.rag_service import RAGService
except ImportError as e:
    print(f"Full RAG service not available: {e}")
    print("Using mock RAG service for testing...")
    from services.mock_rag_service import MockRAGService as RAGService

from services.user_profile import UserProfileService
from services.translation_service import TranslationService
from utils.rate_limiter import RateLimiter, GlobalRateLimiter
from utils.chat_logger import log_chat_interaction
from models.chatlog import ChatLog
from sqlalchemy.orm import Session
from utils.database import get_db
import time
import json
import asyncio

router = APIRouter()

# Initialize services
rag_service = RAGService()
user_profile_service = UserProfileService()
translation_service = TranslationService()
rate_limiter = RateLimiter()
global_rate_limiter = GlobalRateLimiter()

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

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint for normal QA from the whole book
    """
    start_time = time.time()

    # Check rate limits
    if not global_rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Global rate limit exceeded. Please try again later.")

    if request.user_id and not rate_limiter.is_allowed(request.user_id):
        remaining = rate_limiter.get_remaining_requests(request.user_id)
        reset_time = rate_limiter.get_reset_time(request.user_id)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. {remaining} requests remaining. Reset in {(reset_time - time.time()) / 60:.1f} minutes."
        )

    try:
        # Get user profile if user_id provided
        user_profile = None
        if request.user_id:
            user_profile = user_profile_service.get_user_profile(request.user_id)

        # Process the query using RAG
        response_data = await rag_service.process_query(
            query=request.question,
            user_id=request.user_id,
            user_profile=user_profile
        )

        # Translate response if needed
        original_response = response_data['response']
        if request.language != "en":
            translated_response = translation_service.translate_text(
                response_data['response'],
                target_lang=request.language
            )
            response_data['response'] = translated_response

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Log the interaction
        log_chat_interaction(
            db=db,
            user_id=request.user_id,
            question=request.question,
            response=original_response if request.language == "en" else response_data['response'],
            sources=response_data.get('sources', []),
            context_used=response_data.get('context_used', {}),
            language=request.language,
            response_time_ms=response_time_ms
        )

        return ChatResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@router.post("/selected", response_model=ChatResponse)
async def chat_selected_text(request: SelectedTextChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint for selected-text QA (user highlights text and asks a question)
    """
    start_time = time.time()

    # Check rate limits
    if not global_rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Global rate limit exceeded. Please try again later.")

    if request.user_id and not rate_limiter.is_allowed(request.user_id):
        remaining = rate_limiter.get_remaining_requests(request.user_id)
        reset_time = rate_limiter.get_reset_time(request.user_id)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. {remaining} requests remaining. Reset in {(reset_time - time.time()) / 60:.1f} minutes."
        )

    try:
        # Get user profile if user_id provided
        user_profile = None
        if request.user_id:
            user_profile = user_profile_service.get_user_profile(request.user_id)

        # Process the query using RAG with selected text context
        response_data = await rag_service.process_selected_text_query(
            query=request.question,
            selected_text=request.selected_text,
            user_id=request.user_id,
            user_profile=user_profile
        )

        # Translate response if needed
        original_response = response_data['response']
        if request.language != "en":
            translated_response = translation_service.translate_text(
                response_data['response'],
                target_lang=request.language
            )
            response_data['response'] = translated_response

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Log the interaction
        log_chat_interaction(
            db=db,
            user_id=request.user_id,
            question=request.question,
            response=original_response if request.language == "en" else response_data['response'],
            sources=response_data.get('sources', []),
            context_used=response_data.get('context_used', {}),
            language=request.language,
            selected_text=request.selected_text,
            response_time_ms=response_time_ms
        )

        return ChatResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")

@router.get("/capabilities")
async def get_chat_capabilities():
    """
    Get the capabilities of the chatbot
    """
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
        "knowledge_base_size": "Comprehensive textbook content"
    }

async def stream_response_generator(request: ChatRequest, db: Session):
    """
    Generator function that yields streaming responses
    """
    start_time = time.time()

    # Check rate limits
    if not global_rate_limiter.is_allowed():
        yield f"data: {json.dumps({'type': 'error', 'message': 'Global rate limit exceeded. Please try again later.'})}\n\n"
        return

    if request.user_id and not rate_limiter.is_allowed(request.user_id):
        remaining = rate_limiter.get_remaining_requests(request.user_id)
        reset_time = rate_limiter.get_reset_time(request.user_id)
        yield f"data: {json.dumps({'type': 'error', 'message': f'Rate limit exceeded. {remaining} requests remaining. Reset in {(reset_time - time.time()) / 60:.1f} minutes.'})}\n\n"
        return

    try:
        # Get user profile if user_id provided
        user_profile = None
        if request.user_id:
            user_profile = user_profile_service.get_user_profile(request.user_id)

        # Process the query using RAG with streaming support
        # We'll simulate token streaming by breaking the response into chunks
        response_data = await rag_service.process_query(
            query=request.question,
            user_id=request.user_id,
            user_profile=user_profile
        )

        # Get the response text
        original_response = response_data['response']

        # Translate response if needed
        if request.language != "en":
            translated_response = translation_service.translate_text(
                response_data['response'],
                target_lang=request.language
            )
            response_data['response'] = translated_response
        else:
            translated_response = original_response

        # Stream the response as individual tokens/words
        response_text = response_data['response']

        # Send sources first
        if 'sources' in response_data and response_data['sources']:
            yield f"data: {json.dumps({'type': 'sources', 'sources': response_data['sources']})}\n\n"

        # Stream the response text character by character or word by word
        # For better UX, we'll stream by sentences/paragraphs
        import re
        sentences = re.split(r'[.!?]+', response_text)

        full_response_buffer = ""
        for i, sentence in enumerate(sentences):
            if sentence.strip():  # Skip empty sentences
                sentence = sentence.strip()
                # Add punctuation back if it was removed
                if i < len(sentences) - 1:  # Not the last sentence
                    sentence += "."

                full_response_buffer += sentence
                if i > 0:  # Add space between sentences
                    full_response_buffer += " "

                # Yield the token
                yield f"data: {json.dumps({'type': 'token', 'token': sentence + (' ' if i < len(sentences) - 1 else '')})}\n\n"

                # Small delay to simulate real streaming
                await asyncio.sleep(0.02)

        # Send done signal
        response_time_ms = int((time.time() - start_time) * 1000)

        # Log the interaction
        log_chat_interaction(
            db=db,
            user_id=request.user_id,
            question=request.question,
            response=original_response if request.language == "en" else response_data['response'],
            sources=response_data.get('sources', []),
            context_used=response_data.get('context_used', {}),
            language=request.language,
            response_time_ms=response_time_ms
        )

        yield f"data: {json.dumps({'type': 'done', 'response_time': response_time_ms})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': f'Error processing chat message: {str(e)}'})}\n\n"


@router.post("/stream", response_class=StreamingResponse)
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Streaming chat endpoint that sends responses token by token
    """
    return StreamingResponse(
        stream_response_generator(request, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.on_event("startup")
async def startup_event():
    """
    Initialize the RAG service on startup
    """
    await rag_service.initialize()