"""
Simple RAG service for testing without heavy dependencies
"""
import os
import json
from typing import Dict, List, Any
from pydantic import BaseModel

class RAGResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    context_used: Dict[str, Any] = {}

class SimpleRAGService:
    def __init__(self):
        print("Simple RAG Service initialized (no heavy dependencies)")
        # Load some sample responses for testing
        self.sample_responses = {
            "hello": "Hello! I'm your Physical AI & Humanoid Robotics Assistant. How can I help you today?",
            "physical ai": "Physical AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators. It combines machine learning with robotics to create systems that can perceive, reason, and act in physical environments.",
            "robotics": "Robotics is an interdisciplinary field that integrates computer science, electrical engineering, and mechanical engineering. It deals with the design, construction, operation, and use of robots.",
            "humanoid": "Humanoid robots are robots designed to look and act like humans. They typically have a head, torso, two arms, and two legs, and are designed to interact with human tools and environments.",
            "textbook": "This is the Physical AI & Humanoid Robotics textbook. It covers topics like embodied intelligence, sensorimotor learning, balance control, and humanoid robotics systems."
        }

    async def initialize(self):
        """Initialize the service"""
        print("Simple RAG Service initialized successfully")

    async def process_query(self, query: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """Process a query using simple lookup"""
        query_lower = query.lower()

        # Look for matching keywords in sample responses
        response_text = "I'm sorry, I don't have specific information about that topic in my simple test mode. Please try asking about physical AI, robotics, or humanoid systems."

        for keyword, response in self.sample_responses.items():
            if keyword in query_lower:
                response_text = response
                break

        # Add generic sources
        sources = [
            {
                "id": "sample-source",
                "title": "Physical AI Textbook",
                "chapter": "General",
                "section": "Introduction",
                "relevance_score": 0.8,
                "content_preview": "Sample content about Physical AI concepts"
            }
        ]

        return {
            "response": response_text,
            "sources": sources,
            "context_used": {
                "query": query,
                "retrieved_docs_count": len(sources),
                "user_profile_used": user_profile is not None
            }
        }

    async def process_selected_text_query(self, query: str, selected_text: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """Process a query with selected text context"""
        response_text = f"Based on the selected text '{selected_text}' and your question '{query}', this is a simulated response from the simple RAG service."

        sources = [
            {
                "id": "selected-text-source",
                "title": "Selected Text Context",
                "chapter": "User Selection",
                "section": "Custom",
                "relevance_score": 0.9,
                "content_preview": selected_text[:200]
            }
        ]

        return {
            "response": response_text,
            "sources": sources,
            "context_used": {
                "query": query,
                "selected_text": selected_text,
                "retrieved_docs_count": len(sources),
                "user_profile_used": user_profile is not None
            }
        }