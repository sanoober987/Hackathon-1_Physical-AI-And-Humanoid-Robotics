from typing import Dict, List, Any
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from .vector_db_service import VectorDBService

load_dotenv()

class ChatResponse(BaseModel):
    response_text: str
    context: Dict[str, Any] = {}
    suggestions: List[str] = []

class ChatbotService:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize vector database service
        self.vector_db = VectorDBService()

    async def process_query(self, query: str, user_id: str = None, context: Dict = {}) -> ChatResponse:
        """
        Process a user query using RAG (Retrieval Augmented Generation)
        """
        # Retrieve relevant documents from knowledge base
        retrieved_docs = self.vector_db.search_similar(query, limit=5)

        # Generate response using OpenAI with retrieved context
        response_text = await self._generate_response(query, retrieved_docs, context)

        # Generate follow-up suggestions
        suggestions = await self._generate_suggestions(query)

        return ChatResponse(
            response_text=response_text,
            context=context,
            suggestions=suggestions
        )

    async def _generate_response(self, query: str, documents: List[Dict], context: Dict) -> str:
        """
        Generate a response using OpenAI based on retrieved documents
        """
        # Combine documents into context
        context_str = "\n\n".join([f"Section: {doc['section']}\nContent: {doc['content']}" for doc in documents])

        # Create prompt for OpenAI
        prompt = f"""
        You are an expert assistant for the Physical AI & Humanoid Robotics textbook.
        Answer the user's question based on the provided context from the textbook.

        If the context doesn't contain enough information to answer the question, say so and suggest related topics.
        Always be factual and refer to the textbook content when possible.

        Context from textbook:
        {context_str}

        Question: {query}

        Answer:
        """

        # Call OpenAI API
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert assistant for the Physical AI & Humanoid Robotics textbook. Provide accurate, helpful answers to student questions based on the textbook content. Be factual, clear, and educational. If the provided context doesn't contain sufficient information, acknowledge this and suggest related topics the user might explore."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"I'm sorry, I encountered an error processing your query: {str(e)}. Please try again."

    async def _generate_suggestions(self, query: str) -> List[str]:
        """
        Generate follow-up question suggestions
        """
        # In a real implementation, this would analyze the query and suggest related topics
        # For now, return suggestions based on detected topics
        suggestions_map = {
            "ros": [
                "What are the differences between ROS and ROS 2?",
                "How do I create a ROS 2 package?",
                "What are ROS 2 Quality of Service policies?"
            ],
            "digital twin": [
                "How do digital twins improve robot development?",
                "What are the components of a digital twin system?",
                "How is digital twin used in manufacturing robotics?"
            ],
            "nvidia isaac": [
                "What is Isaac Sim?",
                "How do I use Isaac ROS?",
                "What are the benefits of GPU acceleration in robotics?"
            ],
            "vision language action": [
                "How do VLA models work?",
                "What are the applications of VLA in robotics?",
                "How is multimodal learning different from traditional AI?"
            ],
            "humanoid": [
                "What are the challenges in humanoid robotics?",
                "How do humanoid robots maintain balance?",
                "What are the applications of humanoid robots?"
            ],
            "physical ai": [
                "What makes Physical AI different from traditional AI?",
                "What are the core challenges in Physical AI?",
                "How is Physical AI applied in robotics?"
            ]
        }

        # Find matching suggestions based on query
        query_lower = query.lower()
        for key, suggestions in suggestions_map.items():
            if key in query_lower:
                return suggestions[:3]  # Return first 3 suggestions

        # Default suggestions
        return [
            "Can you explain this concept in more detail?",
            "What are some practical applications of this?",
            "Are there any exercises to practice this concept?"
        ]

    def query_knowledge_base(self, query: str) -> List[Dict]:
        """
        Directly query the knowledge base for relevant information
        """
        return self.vector_db.search_similar(query, limit=5)

    def get_modules_info(self) -> Dict:
        """
        Get information about all modules in the textbook
        """
        chapters = self.vector_db.get_all_chapters()

        return {
            "modules": [
                {
                    "id": i+1,
                    "title": chapter,
                    "description": f"Chapter covering {chapter}",
                    "topics": ["General concepts", "Applications", "Examples"]
                }
                for i, chapter in enumerate(chapters)
            ]
        }