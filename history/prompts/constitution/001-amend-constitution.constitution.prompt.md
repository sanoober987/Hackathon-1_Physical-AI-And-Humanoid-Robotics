---
id: 001
title: Amend Constitution
stage: constitution
date: 2026-01-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Code User
command: /sp.constitution
labels: [constitution,ai-book,rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: AI-Authored Book with Embedded RAG Chatbot

Overview:
Create an AI-written technical book using Claude Code and Spec-Kit Plus, built with Docusaurus and deployed to GitHub Pages. Embed a RAG chatbot that answers questions about the book and user-selected text using OpenAI Agents/ChatKit, FastAPI, Neon Postgres, and Qdrant Cloud.

Core Principles:
- Spec-first workflow (Spec-Kit Plus)
- Accuracy and clarity
- Reproducible builds and deployment
- Secure, modular architecture
- Low-latency retrieval

Authoring Standards:
- Content generated via Claude Code.
- Docusaurus Markdown with frontmatter.
- Each chapter: overview, concepts, examples, summary.
- No hallucinations outside verified context.

Platform Standards:
- Framework: Docusaurus
- Deploy: GitHub Pages
- SEO-friendly structure and navigation.

RAG Standards:
- FastAPI backend.
- Qdrant for vectors, Neon for metadata.
- Answer from full book or selected text only.
- Source-aware, context-bounded responses.

Security & Performa

## Response snapshot

Updated the project constitution file at .specify/memory/constitution.md with the specific principles and requirements for the AI-authored book with embedded RAG chatbot project. The constitution now includes:

- Core Principles: Spec-first workflow, Accuracy and Clarity, Reproducible Builds and Deployment, Secure, Modular Architecture, Low-latency Retrieval, and Docusaurus and GitHub Pages Deployment
- Technology Stack Requirements: Including Docusaurus, FastAPI, Neon Postgres, Qdrant Cloud, and GitHub Pages
- Development Workflow: Covering content generation via Claude Code, Docusaurus Markdown standards, and RAG response guidelines
- Governance: Updated with compliance rules for authoring standards, testing, and documentation

Also added a sync impact report to document the changes made and verified that all placeholder tokens were properly replaced.

## Outcome

- ✅ Impact: Updated constitution file with project-specific principles and requirements
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with all required principles
- 🔁 Next prompts: Ready to proceed with spec creation using /sp.specify
- 🧠 Reflection: The constitution now properly reflects the project requirements and can guide future development decisions.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All placeholder tokens replaced successfully
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Proceed with spec creation