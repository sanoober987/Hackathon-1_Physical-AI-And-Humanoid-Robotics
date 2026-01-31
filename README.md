# Physical AI & Humanoid Robotics Textbook Assistant

A comprehensive AI assistant for the Physical AI & Humanoid Robotics textbook with full English/Urdu support, RAG capabilities, and chat history.

## 🌟 Features

### 📚 Bilingual Support
- Complete textbook content in both English and Urdu
- Automatic language detection based on URL
- Native language responses

### 🔍 RAG (Retrieval Augmented Generation)
- Processes both English and Urdu documents
- Creates semantic embeddings for accurate retrieval
- Prevents hallucinations with source citations
- Context-aware responses

### 💬 Smart Chat Interface
- Modern glassmorphism UI design
- Real-time conversation history
- Persistent storage across sessions
- Professional, responsive interface

### 📖 Complete Textbook Access
- Full course content indexed and searchable
- Chapter-wise organization preserved
- Technical concepts explained clearly

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework
- **Sentence Transformers**: Multilingual embeddings
- **SQLite**: Lightweight database for history
- **Pydantic**: Data validation

### Frontend
- **Docusaurus**: Static site generator
- **React**: Component-based UI
- **CSS Modules**: Scoped styling
- **i18n**: Internationalization support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd PhysicalAI_Book
```

2. **Start the backend**
```bash
cd PhysicalAI_Book
python start_backend.py
```

3. **In a new terminal, start the frontend**
```bash
cd PhysicalAI_Book/frontend
npm install
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:3000/assistant
- Backend API: http://localhost:8000

## 🌐 Language Support

### English Interface
- URL: `http://localhost:3000/assistant`
- Responses in English
- English textbook content

### Urdu Interface
- URL: `http://localhost:3000/ur/assistant`
- Responses in Urdu
- Urdu textbook content

## 🤖 Using the Assistant

1. Navigate to the assistant page
2. Type your question about Physical AI, robotics, or humanoid systems
3. Receive contextual answers from the textbook
4. View source citations for fact-checking
5. Continue conversations with context preservation

## 🏗️ Project Structure

```
PhysicalAI_Book/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main application
│   ├── rag/                # RAG pipeline
│   ├── models/             # Data models
│   └── requirements.txt    # Dependencies
├── frontend/               # Docusaurus frontend
│   ├── docs/               # English textbook
│   ├── docs-ur/            # Urdu textbook
│   ├── src/                # React components
│   └── docusaurus.config.js
├── vector_store.pkl        # Embedded knowledge base
└── chat_history.db         # Conversation history
```

## 📊 API Endpoints

### Chat
- `POST /api/v1/chat/` - Get AI responses with RAG

### History
- `GET /api/v1/history/` - Retrieve conversation history
- `DELETE /api/v1/history/` - Delete history

### Status
- `GET /api/v1/status/` - System health check

## 🧪 Testing

The system includes comprehensive testing for:
- Document loading and translation
- Embedding accuracy
- API functionality
- UI responsiveness
- Internationalization

## 📈 Performance

- Fast response times with optimized embeddings
- Efficient vector search
- Caching mechanisms
- Scalable architecture

## 🌍 Impact

This assistant makes advanced robotics education accessible in both English and Urdu, supporting diverse learners in the field of Physical AI and Humanoid Robotics.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines for details on our code of conduct and development process.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the repository or contact the development team.
