# Data Model: FastAPI RAG Agent Integration

**Feature**: RAG System – Backend and Frontend Integration
**Date**: 2026-01-24
**Status**: Draft

## Overview
This document defines the data structures and schemas for the RAG system API, based on the key entities identified in the feature specification.

## Query Request Model

### Schema Definition
```python
from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    """
    Request model for RAG query endpoint
    """
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "query": "What are the main concepts discussed in this document?",
                "selected_text": "Optional context from user selection...",
                "session_id": "unique-session-identifier"
            }
        }
```

### Field Definitions
- `query`: (Required) The user's question or query text
  - Type: String
  - Constraints: Min length 1, Max length 1000 characters
  - Validation: Non-empty, sanitized input

- `selected_text`: (Optional) Additional context provided by user selection
  - Type: String or null
  - Constraints: Max length 5000 characters
  - Validation: Sanitized input if provided

- `session_id`: (Optional) Session identifier for future extensibility
  - Type: String or null
  - Constraints: UUID format if provided
  - Validation: Proper UUID format if present

## Response Model

### Schema Definition
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SourceMetadata(BaseModel):
    """
    Metadata for a source document used in the response
    """
    title: str
    url: str
    excerpt: str
    confidence: float
    page_number: Optional[int] = None

class QueryResponse(BaseModel):
    """
    Response model for RAG query endpoint
    """
    answer: str
    sources: List[SourceMetadata]
    confidence: float
    processing_time_ms: int
    timestamp: datetime

    class Config:
        schema_extra = {
            "example": {
                "answer": "The main concepts include distributed systems, consensus algorithms, and fault tolerance...",
                "sources": [
                    {
                        "title": "Distributed Systems Fundamentals",
                        "url": "/docs/distributed-systems/introduction",
                        "excerpt": "Distributed systems consist of multiple components...",
                        "confidence": 0.95,
                        "page_number": 12
                    }
                ],
                "confidence": 0.87,
                "processing_time_ms": 1250,
                "timestamp": "2026-01-24T10:30:00Z"
            }
        }
```

### Field Definitions
- `answer`: (Required) The generated answer based on retrieved documents
  - Type: String
  - Constraints: Non-empty response

- `sources`: (Required) Array of source documents used to generate the answer
  - Type: Array of SourceMetadata objects
  - Constraints: Minimum 0 items, maximum 10 items

- `confidence`: (Required) Overall confidence score for the response
  - Type: Float
  - Range: 0.0 to 1.0
  - Validation: Between 0 and 1

- `processing_time_ms`: (Required) Time taken to process the request
  - Type: Integer
  - Unit: Milliseconds

- `timestamp`: (Required) When the response was generated
  - Type: ISO 8601 datetime string

## Error Response Model

### Schema Definition
```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    Standard error response model
    """
    error: str
    error_code: str
    details: Optional[dict] = None
```

### Field Definitions
- `error`: (Required) Human-readable error message
- `error_code`: (Required) Machine-readable error code
- `details`: (Optional) Additional error details

## Validation Rules

### Input Validation
1. Query length: 1-1000 characters
2. Selected text length: 0-5000 characters
3. Input sanitization: Prevent injection attacks
4. Session ID format: Valid UUID if provided

### Business Logic Validation
1. Query relevance: Must be related to available documents
2. Source quality: Only return high-confidence sources
3. Response coherence: Ensure answer relates to query

## State Transitions

### Request Lifecycle
```
Incoming Request → Validation → Processing → Response Formatting → Response Sent
```

### Error Handling States
```
Valid Request → Agent Processing → [Success → Response] OR [Failure → Error Response]
```

## Relationships

### QueryRequest ↔ Agent
- QueryRequest provides input parameters to the RAG agent
- Agent processes the query and returns structured results

### Agent ↔ Response
- Agent output is transformed into the QueryResponse format
- Source metadata is preserved and formatted according to the schema

## Performance Considerations

### Size Limits
- Query: Max 1000 characters (prevent overly large requests)
- Selected text: Max 5000 characters (limit context length)
- Sources array: Max 10 items (prevent overly verbose responses)

### Validation Efficiency
- Use Pydantic's built-in validation for performance
- Apply constraints early to prevent unnecessary processing