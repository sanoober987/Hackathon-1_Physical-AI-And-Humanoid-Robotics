"""
Mock RAG service for testing without any dependencies
"""
import os
import json
from typing import Dict, List, Any
from pydantic import BaseModel

class RAGResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    context_used: Dict[str, Any] = {}

class MockRAGService:
    def __init__(self):
        print("Mock RAG Service initialized (no dependencies)")
        # Load some sample responses for testing
        self.sample_responses = {
            "hello": "Hello! I'm your Physical AI & Humanoid Robotics Assistant. How can I help you today?",
            "physical ai": "Physical AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators. It combines machine learning with robotics to create systems that can perceive, reason, and act in physical environments.",
            "robotics": "Robotics is an interdisciplinary field that integrates computer science, electrical engineering, and mechanical engineering. It deals with the design, construction, operation, and use of robots.",
            "humanoid": "Humanoid robots are robots designed to look and act like humans. They typically have a head, torso, two arms, and two legs, and are designed to interact with human tools and environments.",
            "textbook": "This is the Physical AI & Humanoid Robotics textbook. It covers topics like embodied intelligence, sensorimotor learning, balance control, and humanoid robotics systems.",
            "balance": "Humanoid robots maintain balance using a combination of sensors like gyroscopes and accelerometers, along with control algorithms that continuously adjust the robot's center of gravity.",
            "embodied intelligence": "Embodied intelligence is the idea that intelligence emerges from the interaction between an agent and its environment, rather than being purely computational."
        }

    async def initialize(self):
        """Initialize the service"""
        print("Mock RAG Service initialized successfully")

    async def process_query(self, query: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """Process a query using simple lookup"""
        query_lower = query.lower()

        # Look for matching keywords in sample responses
        response_text = "I'm sorry, I don't have specific information about that topic in my mock service. Please try asking about physical AI, robotics, or humanoid systems."

        for keyword, response in self.sample_responses.items():
            if keyword in query_lower:
                response_text = response
                break

        # Add generic sources
        sources = [
            {
                "id": "mock-source-1",
                "title": "Physical AI Textbook",
                "chapter": "General Concepts",
                "section": "Introduction",
                "relevance_score": 0.8,
                "content_preview": "Sample content about Physical AI concepts"
            },
            {
                "id": "mock-source-2",
                "title": "Robotics Fundamentals",
                "chapter": "Chapter 2",
                "section": "Basic Principles",
                "relevance_score": 0.7,
                "content_preview": "Information about robotic systems and components"
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
        response_text = f"Based on the selected text '{selected_text}' and your question '{query}', I can provide information about Physical AI concepts. The mock service simulates how the real RAG system would process your query."

        sources = [
            {
                "id": "selected-text-source",
                "title": "Selected Text Context",
                "chapter": "User Selection",
                "section": "Custom Query",
                "relevance_score": 0.9,
                "content_preview": selected_text[:200] + "..."
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