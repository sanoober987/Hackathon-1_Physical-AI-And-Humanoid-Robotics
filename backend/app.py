from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import logging

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import the routes module
from routes.chat import router as chat_router
from models.history_manager import HistoryManager
from rag.rag_orchestrator import RAGOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Physical AI Assistant API",
    description="API for Physical AI and Humanoid Robotics textbook assistant with RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat routes (this includes both the regular and streaming endpoints)
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

# Initialize services
rag_system = RAGOrchestrator()
rag_system.initialize_index()  # Initialize on startup
history_manager = HistoryManager()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Physical AI Assistant API is running"}

@app.get("/api/v1/history/")
async def get_history(user_id: str, limit: int = 10, offset: int = 0):
    """Get chat history for a user"""
    try:
        logger.info(f"Retrieving history for user {user_id}")

        history = history_manager.get_history(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        total = history_manager.get_total_history_count(user_id=user_id)

        return {
            "history": history,
            "total": total
        }

    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.get("/api/v1/status/")
async def get_status():
    """Get system status and statistics"""
    try:
        stats = {
            "status": "healthy",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "services": {
                "rag_system": {
                    "initialized": rag_system.is_initialized,
                    "document_count": rag_system.get_document_count(),
                    "languages": {
                        "english": rag_system.get_document_count("en"),
                        "urdu": rag_system.get_document_count("ur")
                    }
                },
                "history_manager": {
                    "db_available": True  # Basic check
                }
            }
        }

        return stats
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")