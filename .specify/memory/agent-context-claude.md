# AI-Authored Book with Embedded RAG Chatbot Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-22

## Active Technologies

- Python 3.11
- FastAPI for backend services
- Cohere for embedding generation
- Qdrant for vector storage
- BeautifulSoup4 for HTML parsing
- Requests for HTTP operations
- Pydantic for data validation
- UV for package management
- pytest for testing

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   └── embedding.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── content_ingestion.py
│   │   ├── text_splitter.py
│   │   ├── embedding_generator.py
│   │   └── vector_store.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Commands

- `uv init` - Initialize a new Python project with UV
- `uv add [package]` - Add a dependency
- `uv run [command]` - Run a command in the project environment
- `uv sync` - Install all dependencies from uv.lock
- `python main.py` - Run the main application
- `pytest` - Run tests

## Code Style

- Use type hints for all function signatures
- Follow PEP 8 style guidelines
- Use Pydantic models for data validation
- Structure code in logical modules (models, services, api, utils)
- Write docstrings for public functions and classes
- Handle errors gracefully with appropriate logging

## Recent Changes

- Feature 1-embeddings-storage: Added backend structure for ingesting URLs, generating embeddings, and storing in Qdrant vector database
- Feature includes content extraction, text chunking, embedding generation, and vector storage services
- API contract defined for ingestion, processing, and search operations

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->