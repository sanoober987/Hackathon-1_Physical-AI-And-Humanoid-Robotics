<!--
Sync Impact Report:
Version change: N/A -> 1.0.0
Modified principles:
- Spec-first workflow (Spec-Kit Plus)
- Accuracy and Clarity
- Reproducible Builds and Deployment
- Secure, Modular Architecture
- Low-latency Retrieval
- Docusaurus and GitHub Pages Deployment

Added sections: Technology Stack Requirements, Development Workflow
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ reviewed - contains generic constitution check
- .specify/templates/spec-template.md ✅ reviewed - no direct constitution dependencies
- .specify/templates/tasks-template.md ✅ reviewed - no direct constitution dependencies
- .specify/templates/commands/*.md ✅ reviewed - no outdated references
Follow-up TODOs: None
-->
# AI-Authored Book with Embedded RAG Chatbot Constitution

## Core Principles

### Spec-first workflow (Spec-Kit Plus)
All development follows a specification-first approach using Spec-Kit Plus; Specifications must be complete and validated before implementation begins; Changes to specifications follow formal amendment procedures

### Accuracy and Clarity
All content and code must be accurate and clearly presented; No hallucinations outside verified context; Documentation and examples must be precise and testable

### Reproducible Builds and Deployment
All builds and deployments must be reproducible and deterministic; Deployment processes follow CI/CD pipelines; Artifacts are versioned and traceable

### Secure, Modular Architecture
System components are designed with security and modularity in mind; Clear separation of concerns between components; Security considerations are addressed at design phase

### Low-latency Retrieval
RAG system must deliver responses with minimal latency; Performance benchmarks are established and monitored; Optimization is prioritized for user experience

### Docusaurus and GitHub Pages Deployment
Documentation and books are built using Docusaurus framework and deployed to GitHub Pages; SEO-friendly structure and navigation are maintained; Static site generation enables fast loading

## Technology Stack Requirements

Framework: Docusaurus for documentation; Backend: FastAPI for RAG services; Database: Neon Postgres for metadata; Vector Store: Qdrant Cloud for embeddings; Deployment: GitHub Pages for static content

## Development Workflow

Content generated via Claude Code; Docusaurus Markdown with frontmatter; Each chapter includes overview, concepts, examples, and summary; RAG responses are source-aware and context-bounded

## Governance

All PRs/reviews must verify compliance with authoring standards; Code changes must include tests; Content changes must adhere to Docusaurus Markdown standards; RAG responses must cite sources from the book context

**Version**: 1.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19
