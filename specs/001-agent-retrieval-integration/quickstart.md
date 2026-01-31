# Quickstart Guide: RAG Agent Retrieval Integration

**Feature**: RAG Agent Retrieval Integration
**Date**: 2026-01-23
**Branch**: 001-agent-retrieval-integration

## Overview

Quick start guide for implementing and using the RAG agent that integrates retrieval functionality directly. The agent accepts user queries, embeds them using Cohere, retrieves top-k vectors from Qdrant, ranks results, and generates grounded answers using only retrieved book context and optional user-selected text.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to OpenAI API (get API key from [OpenAI Dashboard](https://platform.openai.com/api-keys))
- Access to Cohere API (get API key from [Cohere Dashboard](https://dashboard.cohere.ai))
- Access to Qdrant Cloud (URL and API key from your Qdrant setup)
- Pre-existing vector collection with embedded book content (from Spec-1)

## Installation

1. Install required dependencies:
   ```bash
   pip install openai cohere qdrant-client python-dotenv pydantic pytest
   ```

2. Create a `.env` file in your project root with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   COLLECTION_NAME=your_collection_name_from_spec_1
   ```

## Basic Usage

### 1. Import and initialize the agent system:

```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()
```

### 2. Process a basic query:

```python
# Process a query with the agent
response = agent.process_query("your natural language query here")
print(f"Response: {response.response_text}")
print(f"Sources: {response.sources_cited}")
```

### 3. Process query with user-provided context:

```python
# Process a query with additional user context
response = agent.process_query(
    query="your question about the provided text",
    user_context="Additional text provided by the user for focused analysis"
)
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for agent functionality
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `COLLECTION_NAME`: Name of the vector collection to search

### Runtime Parameters
- `top_k`: Number of results to retrieve (default: 5, max: 20)
- `threshold`: Minimum similarity score (default: 0.0)
- `timeout`: Request timeout in seconds (default: 30)

## Testing

### Run the basic tests:

```bash
# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_agent.py
pytest tests/test_integration.py
```

### Example test for agent functionality:

```python
import pytest
from agent import RAGAgent

def test_basic_query_processing():
    agent = RAGAgent()
    response = agent.process_query("What are the key principles of AI safety?")

    assert response.response_text is not None
    assert len(response.response_text) > 0
    assert len(response.sources_cited) > 0
    assert response.grounding_confidence >= 0.0
    assert response.grounding_confidence <= 1.0

def test_user_context_integration():
    user_context = "Artificial Intelligence safety is crucial for preventing harmful behaviors."
    agent = RAGAgent()
    response = agent.process_query(
        query="Why is AI safety important?",
        user_context=user_context
    )

    assert response.response_text is not None
    assert user_context in response.sources_cited or response.retrieval_used
```

## Example Implementation

```python
import os
from agent import RAGAgent

def main():
    # Initialize agent
    agent = RAGAgent()

    # Example query
    query = "What are the key principles of AI safety?"
    response = agent.process_query(query, top_k=3)

    print(f"Query: {query}")
    print(f"Response: {response.response_text}")
    print(f"Sources cited: {len(response.sources_cited)}")
    for i, source in enumerate(response.sources_cited, 1):
        print(f"  {i}. {source}")
    print(f"Grounding confidence: {response.grounding_confidence:.2f}")

if __name__ == "__main__":
    main()
```

## Troubleshooting

1. **Connection Issues**: Verify that QDRANT_URL, QDRANT_API_KEY, OPENAI_API_KEY, and COHERE_API_KEY are correct
2. **API Key Issues**: Check that all API keys are valid and have sufficient quota
3. **Collection Not Found**: Ensure the collection from Spec-1 exists and is properly named
4. **Empty Results**: Try lowering the threshold or checking if embeddings were properly stored
5. **Agent Initialization**: Ensure the OpenAI Assistant was created successfully

## Next Steps

1. Integrate the agent into your application
2. Customize the agent's system prompt for your specific domain
3. Monitor agent performance and retrieval effectiveness
4. Implement additional logging for production environments
5. Add caching for frequently requested queries