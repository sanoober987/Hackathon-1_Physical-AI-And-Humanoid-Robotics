# Quickstart Guide: RAG Pipeline Retrieval and Validation System

**Feature**: RAG Pipeline – Retrieval and Validation System
**Date**: 2026-01-23
**Branch**: 003-rag-pipeline

## Overview

Quick start guide for implementing and using the RAG retrieval system that connects to Qdrant vector storage and uses Cohere for query embeddings.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Cohere API (get API key from [Cohere Dashboard](https://dashboard.cohere.ai))
- Access to Qdrant Cloud (URL and API key from your Qdrant setup)

## Installation

1. Install required dependencies:
   ```bash
   pip install cohere qdrant-client python-dotenv pydantic
   ```

2. Create a `.env` file in your project root with the following:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   COLLECTION_NAME=your_collection_name_from_spec_1
   ```

## Basic Usage

### 1. Import and initialize the retrieval system:

```python
from retrieve import RAGRetriever

# Initialize the retriever
retriever = RAGRetriever()
```

### 2. Perform a basic retrieval:

```python
# Perform a retrieval with default settings
results = retriever.retrieve("your natural language query here", top_k=5)
print(f"Found {len(results)} relevant chunks:")
for result in results:
    print(f"- Score: {result.score}")
    print(f"  Content: {result.content[:100]}...")
    print(f"  Source: {result.metadata['url']}")
```

### 3. Advanced retrieval with custom parameters:

```python
# Retrieve with custom parameters
results = retriever.retrieve(
    query="your query",
    top_k=10,  # Get 10 results instead of default 5
    threshold=0.3  # Only return results with similarity >= 0.3
)
```

## Validation

### Run the built-in validation routine:

```python
from retrieve import validate_retrieval_system

# Run validation with test queries
validation_results = validate_retrieval_system()

# Print validation summary
for result in validation_results:
    print(f"Test '{result.test_name}': {'PASSED' if result.passed else 'FAILED'}")
    if not result.passed:
        print(f"  Details: {result.details}")
```

## Configuration

### Environment Variables
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `COLLECTION_NAME`: Name of the vector collection to search

### Runtime Parameters
- `top_k`: Number of results to return (default: 5, max: 100)
- `threshold`: Minimum similarity score (default: 0.0)
- `timeout`: Request timeout in seconds (default: 30)

## Error Handling

The retrieval system handles the following errors gracefully:

- **Missing Collection**: If the Qdrant collection doesn't exist
- **API Failures**: If Cohere or Qdrant APIs are unavailable
- **Empty Results**: If no relevant chunks are found
- **Invalid Queries**: If queries are malformed or empty

## Example Implementation

```python
import os
from retrieve import RAGRetriever

def main():
    # Initialize retriever
    retriever = RAGRetriever()
    
    # Example query
    query = "What are the key principles of AI safety?"
    results = retriever.retrieve(query, top_k=3)
    
    print(f"Query: {query}")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. [{result.score:.3f}] {result.content[:150]}...")
        print(f"   Source: {result.metadata.get('url', 'Unknown')}")
        print()

if __name__ == "__main__":
    main()
```

## Troubleshooting

1. **Connection Issues**: Verify that QDRANT_URL and QDRANT_API_KEY are correct
2. **API Key Issues**: Check that COHERE_API_KEY is valid and has sufficient quota
3. **Collection Not Found**: Ensure the collection from Spec-1 exists and is properly named
4. **Empty Results**: Try lowering the threshold or checking if embeddings were properly stored

## Next Steps

1. Integrate the retrieval system into your application
2. Customize the validation routine with your specific test queries
3. Monitor retrieval performance and adjust parameters as needed
4. Implement caching for frequently requested queries
