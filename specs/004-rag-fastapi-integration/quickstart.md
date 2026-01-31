# Quickstart Guide: FastAPI RAG Agent Integration

**Feature**: RAG System – Backend and Frontend Integration
**Date**: 2026-01-24
**Status**: Draft

## Overview
This guide provides a quick introduction to setting up and running the RAG system API server for development and testing.

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Access to the existing agent implementation (`agent.py`)
- Vector store (Qdrant) connection details (for production)

## Installation

### 1. Clone or Navigate to Project Directory
```bash
cd C:\Users\Z.H\Desktop\Hackathon_1_2025
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-multipart pydantic python-dotenv
pip install qdrant-client  # For vector store integration
```

## Running the Server

### 1. Basic Startup
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. With Environment Variables
```bash
# Create .env file with configuration
cat > .env << EOF
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
VECTOR_STORE_URL=http://localhost:6333
TIMEOUT_SECONDS=30
EOF

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Query Example
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic of this documentation?",
    "selected_text": "Optional context from user selection",
    "session_id": "test-session-123"
  }'
```

## Configuration Options

### Environment Variables
- `DEBUG`: Enable/disable debug mode (default: false)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS
- `TIMEOUT_SECONDS`: Request timeout in seconds (default: 30)
- `LOG_LEVEL`: Logging level (default: info)

### Example Production Configuration
```bash
DEBUG=false
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://your-docusaurus-site.com
TIMEOUT_SECONDS=10
LOG_LEVEL=warning
```

## API Endpoints

### Query Endpoint
- **Method**: POST
- **Path**: `/query`
- **Description**: Process user queries through the RAG system
- **Response**: JSON with answer, sources, and metadata

### Health Endpoint
- **Method**: GET
- **Path**: `/health`
- **Description**: Check API health status
- **Response**: JSON with health status

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure `agent.py` is in the project root
   - Check that all dependencies are installed

2. **CORS Errors**
   - Verify `ALLOWED_ORIGINS` includes your frontend domain
   - Check that frontend is sending correct Origin header

3. **Timeout Errors**
   - Increase `TIMEOUT_SECONDS` if processing is slow
   - Check vector store connectivity

4. **Connection Issues**
   - Verify vector store (Qdrant) is running
   - Check network connectivity to external services

## Next Steps

1. Integrate with your Docusaurus frontend
2. Configure production environment variables
3. Set up monitoring and logging
4. Implement rate limiting for production use