from sqlalchemy.orm import Session
from models.chatlog import ChatLog
from datetime import datetime
import time

def log_chat_interaction(
    db: Session,
    user_id: str,
    question: str,
    response: str,
    sources: list = None,
    context_used: dict = None,
    language: str = "en",
    selected_text: str = None,
    response_time_ms: int = None,
    session_id: str = None
):
    """
    Log chat interaction to database
    """
    chat_log = ChatLog(
        user_id=user_id,
        question=question,
        response=response,
        sources=sources,
        context_used=context_used,
        language=language,
        selected_text=selected_text,
        response_time_ms=response_time_ms,
        session_id=session_id
    )

    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)

    return chat_log