"""
Chat history manager for storing and retrieving conversation history
Supports SQLite storage for persistence
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from .chat_models import HistoryEntry, ChatResponse
import os

class HistoryManager:
    def __init__(self, db_path: str = "PhysicalAI_Book/chat_history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Initialize the database and create tables if they don't exist
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT,
                question TEXT NOT NULL,
                response TEXT NOT NULL,
                sources TEXT,  -- JSON string of sources
                language TEXT DEFAULT 'en',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON chat_history(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON chat_history(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_history(timestamp)')

        conn.commit()
        conn.close()

    def save_chat(self, user_id: str, question: str, response: str, sources: List[Dict[str, Any]], language: str, session_id: Optional[str] = None):
        """
        Save a chat interaction to history
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        sources_json = json.dumps(sources) if sources else "[]"

        cursor.execute('''
            INSERT INTO chat_history (user_id, session_id, question, response, sources, language, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, session_id, question, response, sources_json, language, datetime.utcnow()))

        conn.commit()
        conn.close()

    def get_history(self, user_id: str, limit: int = 10, offset: int = 0) -> List[HistoryEntry]:
        """
        Retrieve chat history for a user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT user_id, question, response, language, timestamp
            FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            entry = HistoryEntry(
                user_id=row[0],
                question=row[1],
                response=row[2],
                language=row[3],
                timestamp=datetime.fromisoformat(row[4]) if isinstance(row[4], str) else row[4]
            )
            history.append(entry)

        return history

    def get_total_history_count(self, user_id: str) -> int:
        """
        Get the total number of chat entries for a user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM chat_history WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]

        conn.close()
        return count

    def delete_history(self, user_id: str, history_id: Optional[str] = None):
        """
        Delete chat history for a user
        If history_id is provided, delete specific entry; otherwise delete all for user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if history_id:
            cursor.execute('DELETE FROM chat_history WHERE user_id = ? AND id = ?', (user_id, history_id))
        else:
            cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))

        conn.commit()
        conn.close()

    def get_recent_conversations(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversations for context
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT question, response, language, timestamp
            FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        conversations = []
        for row in rows:
            conv = {
                'question': row[0],
                'response': row[1],
                'language': row[2],
                'timestamp': row[3]
            }
            conversations.append(conv)

        return conversations

# Example usage
if __name__ == "__main__":
    history_manager = HistoryManager()

    # Test saving a chat
    history_manager.save_chat(
        user_id="test_user_123",
        question="What is Physical AI?",
        response="Physical AI refers to AI systems that interact with the physical world...",
        sources=[{"title": "Introduction", "path": "docs/intro.md"}],
        language="en"
    )

    # Test retrieving history
    history = history_manager.get_history(user_id="test_user_123")
    print(f"Retrieved {len(history)} history entries")

    # Test getting total count
    total = history_manager.get_total_history_count(user_id="test_user_123")
    print(f"Total history count: {total}")