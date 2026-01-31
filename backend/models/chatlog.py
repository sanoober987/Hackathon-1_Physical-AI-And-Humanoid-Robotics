from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True, index=True)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)  # Store as JSON array
    context_used = Column(JSON, nullable=True)  # Store as JSON object
    language = Column(String, default="en")  # en, ur, etc.
    selected_text = Column(Text, nullable=True)  # If this was a selected text query
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    response_time_ms = Column(Integer, nullable=True)  # How long the response took
    session_id = Column(String, nullable=True, index=True)  # To group related chats

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question": self.question,
            "response": self.response,
            "sources": self.sources,
            "context_used": self.context_used,
            "language": self.language,
            "selected_text": self.selected_text,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "response_time_ms": self.response_time_ms,
            "session_id": self.session_id
        }