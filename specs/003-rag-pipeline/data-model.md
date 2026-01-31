# Data Model: RAG Pipeline Retrieval and Validation System

**Feature**: RAG Pipeline – Retrieval and Validation System
**Date**: 2026-01-23
**Branch**: 003-rag-pipeline

## Overview

Data model for the RAG retrieval system, defining the structure of query inputs, search results, and validation data.

## Core Entities

### QueryInput
Represents a natural language query submitted for retrieval

- **query_text** (str): The natural language query text
- **top_k** (int, optional): Number of results to return (default: 5)
- **filters** (dict, optional): Additional filters for search (default: {})
- **threshold** (float, optional): Minimum similarity threshold (default: 0.0)

### SearchResult
Represents a single result from the vector similarity search

- **content** (str): The text content of the retrieved chunk
- **score** (float): Similarity score between query and result
- **metadata** (dict): Additional metadata about the source
  - **url** (str): Source URL of the content
  - **title** (str): Title of the source document
  - **section** (str): Section where the content appears
  - **chunk_index** (int): Index of the chunk in the original document

### RetrievalResult
Represents the complete result of a retrieval operation

- **query_embedding** (list[float]): The embedding vector of the query
- **results** (list[SearchResult]): List of search results ordered by relevance
- **execution_time** (float): Time taken to execute the retrieval in seconds
- **retrieval_stats** (dict): Statistics about the retrieval
  - **total_candidates** (int): Total number of candidates considered
  - **search_threshold** (float): Threshold used for filtering results

### ValidationError
Represents an error encountered during validation

- **test_query** (str): The query that caused the error
- **expected_result** (any): Expected result for the test
- **actual_result** (any): Actual result received
- **error_message** (str): Description of the validation error
- **timestamp** (datetime): When the error occurred

### ValidationResult
Represents the result of a validation operation

- **test_name** (str): Name of the test performed
- **passed** (bool): Whether the test passed
- **details** (str): Additional details about the test result
- **accuracy_score** (float, optional): Accuracy metric if applicable
- **timestamp** (datetime): When the test was run

## Relationships

```
QueryInput --(generates)--> QueryEmbedding
QueryEmbedding --(performs similarity search in)--> VectorDB
VectorDB --(returns)--> SearchResult[0..*]
SearchResult[0..*] --(composes)--> RetrievalResult
TestQuery --(validates)--> RetrievalResult
TestQuery --(produces)--> ValidationResult
ValidationResult --(may contain)--> ValidationError[0..*]
```

## Validation Rules

### QueryInput Validation
- query_text must not be empty
- top_k must be between 1 and 100
- threshold must be between 0.0 and 1.0

### SearchResult Validation
- content must not be empty
- score must be between 0.0 and 1.0
- metadata must contain required fields: url, title, section

### RetrievalResult Validation
- results list must not exceed top_k specified in original query
- execution_time must be positive

## State Transitions

### Retrieval Process
1. **QUERY_RECEIVED**: QueryInput is validated
2. **EMBEDDING_GENERATED**: Query embedding is created
3. **SEARCH_PERFORMED**: Vector similarity search is executed
4. **RESULTS_FORMATTED**: Results are prepared with metadata
5. **RETRIEVAL_COMPLETE**: Final RetrievalResult is returned

### Validation Process
1. **VALIDATION_STARTED**: Validation routine begins
2. **TEST_EXECUTED**: Individual test is run
3. **RESULT_COMPARED**: Expected vs actual results compared
4. **VALIDATION_COMPLETE**: ValidationResult is produced

## Constraints

- All string fields have maximum length of 10,000 characters unless otherwise specified
- Numeric values must be within appropriate ranges as defined in validation rules
- Metadata fields are nullable but strongly recommended for proper attribution
- Timestamps are in ISO 8601 format
