"""
Pydantic models for chat requests and responses
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    question: str
    user_id: str
    language: str = "en"  # Default to English
    history_id: Optional[str] = None  # For continuing conversations

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    language: str
    timestamp: datetime

class HistoryEntry(BaseModel):
    user_id: str
    question: str
    response: str
    language: str
    timestamp: datetime

class GetHistoryRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class GetHistoryResponse(BaseModel):
    history: List[HistoryEntry]
    total: int

class DeleteHistoryRequest(BaseModel):
    user_id: str
    history_id: Optional[str] = None  # If None, delete all history for user