# Physical AI Assistant Setup Guide

## Overview
This guide will help you set up the complete Physical AI Assistant with English/Urdu support, RAG functionality, and chat history.

## Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm/yarn

## Backend Setup (FastAPI)

### 1. Install Backend Dependencies
```bash
cd PhysicalAI_Book/backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd PhysicalAI_Book
python start_backend.py
```

The backend will be available at `http://localhost:8000`

### 3. Backend Endpoints
- `GET /` - Health check
- `POST /api/v1/chat/` - Chat with RAG
- `GET /api/v1/history/` - Get chat history
- `DELETE /api/v1/history/` - Delete chat history
- `GET /api/v1/status/` - System status

## Frontend Setup (Docusaurus)

### 1. Install Frontend Dependencies
```bash
cd PhysicalAI_Book/frontend
npm install
```

### 2. Start the Frontend Development Server
```bash
cd PhysicalAI_Book/frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Features

### 1. English/Urdu Support
- The system automatically detects language from the URL
- `/assistant` - English interface
- `/ur/assistant` - Urdu interface
- AI responses match the selected language

### 2. RAG (Retrieval Augmented Generation)
- Loads both English and Urdu textbooks
- Creates vector embeddings for documents
- Retrieves relevant information for queries
- Prevents hallucination by citing sources

### 3. Chat History
- Stores conversations in SQLite database
- Persists across browser sessions
- Maintains conversation context

### 4. Modern UI
- Glassmorphism design
- Responsive layout
- Smooth animations
- Professional appearance

## Project Structure
```
PhysicalAI_Book/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── main.py               # Application runner
│   ├── rag/                  # RAG pipeline
│   │   ├── document_loader.py
│   │   ├── embedding_engine.py
│   │   └── rag_orchestrator.py
│   ├── models/               # Data models
│   │   ├── chat_models.py
│   │   └── history_manager.py
│   └── requirements.txt
├── frontend/
│   ├── docs/                 # English documentation
│   ├── docs-ur/              # Urdu documentation
│   ├── src/
│   │   ├── components/       # React components
│   │   │   └── ChatWidget.jsx
│   │   ├── pages/            # Pages
│   │   │   └── assistant.jsx
│   │   └── theme/            # Docusaurus theme
│   │       └── Root.js
│   └── docusaurus.config.js
├── vector_store.pkl          # Vector store (generated)
└── chat_history.db           # Chat history (generated)
```

## API Documentation

### Chat Endpoint
**POST** `/api/v1/chat/`

Request Body:
```json
{
  "question": "What is Physical AI?",
  "user_id": "user_12345",
  "language": "en"
}
```

Response:
```json
{
  "response": "Physical AI refers to AI systems that interact with the physical world...",
  "sources": [
    {
      "title": "Introduction",
      "path": "docs/intro.md",
      "section": "Physical AI combines artificial intelligence...",
      "confidence": 0.95
    }
  ],
  "language": "en",
  "timestamp": "2023-12-07T10:30:00Z"
}
```

### History Endpoint
**GET** `/api/v1/history/?user_id=user_12345&limit=10&offset=0`

Response:
```json
{
  "history": [
    {
      "user_id": "user_12345",
      "question": "What is Physical AI?",
      "response": "Physical AI refers to AI systems...",
      "language": "en",
      "timestamp": "2023-12-07T10:30:00Z"
    }
  ],
  "total": 1
}
```

## Troubleshooting

### Common Issues
1. **Backend won't start**: Make sure all dependencies are installed
2. **Frontend can't connect to backend**: Check that backend is running on port 8000
3. **Slow responses**: Initial setup may take time to load and index documents
4. **Translation issues**: Verify docs-ur directory contains translated files

### Development Tips
- The RAG system initializes on first run, which may take a few minutes
- Vector store is persisted in `vector_store.pkl`
- Chat history is stored in `chat_history.db`
- Both English and Urdu documents are processed during initialization

## Production Deployment

For production deployment:
1. Use a production WSGI server like Gunicorn instead of uvicorn's dev server
2. Configure proper CORS settings for your domain
3. Set up a proper database instead of SQLite for scalability
4. Add authentication for user sessions
5. Implement rate limiting for API endpoints