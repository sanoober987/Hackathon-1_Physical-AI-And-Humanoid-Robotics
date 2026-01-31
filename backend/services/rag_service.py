from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from .qdrant_client import QdrantVectorStore
from .embedder import Embedder
from .user_profile import UserProfileService
import asyncio

load_dotenv()

class RAGResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    context_used: Optional[Dict[str, Any]] = None

class RAGService:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize vector store
        self.vector_store = QdrantVectorStore()

        # Initialize embedder
        self.embedder = Embedder()

        # Initialize user profile service
        self.user_profile_service = UserProfileService()

    async def initialize(self):
        """
        Initialize the RAG service
        """
        await self.vector_store.initialize()
        print("RAG Service initialized successfully")

    async def process_query(self, query: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """
        Process a user query using RAG (Retrieval Augmented Generation)
        """
        # Retrieve relevant documents from knowledge base
        retrieved_docs = await self.vector_store.search_similar(query, limit=5)

        # Enhance context with user profile if available
        enhanced_context = self._enhance_context_with_user_profile(retrieved_docs, user_profile)

        # Generate response using LLM with retrieved context
        response_text = await self._generate_response(query, enhanced_context, user_profile)

        # Prepare sources for citation
        sources = self._prepare_sources(retrieved_docs)

        # Update user learning history if user_id provided
        if user_id:
            await self.user_profile_service.add_learning_history(user_id, query, "normal_query")

        return {
            "response": response_text,
            "sources": sources,
            "context_used": {
                "query": query,
                "retrieved_docs_count": len(retrieved_docs),
                "user_profile_used": user_profile is not None
            }
        }

    async def process_selected_text_query(self, query: str, selected_text: str, user_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """
        Process a query with selected text context using RAG
        """
        # First search for context around the selected text
        text_context_docs = await self.vector_store.search_similar(selected_text, limit=3)

        # Then search for broader context related to the query
        query_context_docs = await self.vector_store.search_similar(query, limit=3)

        # Combine contexts
        all_docs = text_context_docs + query_context_docs

        # Deduplicate by ID
        seen_ids = set()
        combined_docs = []
        for doc in all_docs:
            if doc['id'] not in seen_ids:
                combined_docs.append(doc)
                seen_ids.add(doc['id'])

        # Limit to top 5 unique documents
        combined_docs = combined_docs[:5]

        # Enhance context with user profile if available
        enhanced_context = self._enhance_context_with_user_profile(combined_docs, user_profile, selected_text)

        # Generate response using LLM with selected text and retrieved context
        response_text = await self._generate_response_with_selected_text(query, selected_text, enhanced_context, user_profile)

        # Prepare sources for citation
        sources = self._prepare_sources(combined_docs)

        # Update user learning history if user_id provided
        if user_id:
            await self.user_profile_service.add_learning_history(user_id, f"Selected text query: {query}", "selected_text_query")

        return {
            "response": response_text,
            "sources": sources,
            "context_used": {
                "query": query,
                "selected_text": selected_text,
                "retrieved_docs_count": len(combined_docs),
                "user_profile_used": user_profile is not None
            }
        }

    def _enhance_context_with_user_profile(self, docs: List[Dict], user_profile: Dict = None, selected_text: str = None) -> str:
        """
        Enhance the context with user profile information
        """
        context_parts = []

        # Add selected text if provided
        if selected_text:
            context_parts.append(f"USER SELECTED TEXT: {selected_text}")

        # Add user profile context if available
        if user_profile:
            profile_context = f"USER CONTEXT: "
            if user_profile.get('level'):
                profile_context += f"Academic level: {user_profile['level']}. "
            if user_profile.get('interests'):
                profile_context += f"Interests: {', '.join(user_profile['interests'])}. "
            if user_profile.get('preferences'):
                profile_context += f"Preferences: {', '.join(user_profile['preferences'])}. "
            context_parts.append(profile_context)

        # Add document content
        for doc in docs:
            doc_context = f"SECTION: {doc.get('title', 'Unknown')} - {doc.get('section', 'Unknown')}\n"
            doc_context += f"CHAPTER: {doc.get('chapter', 'Unknown')}\n"
            doc_context += f"CONTENT: {doc.get('content', '')}"
            context_parts.append(doc_context)

        return "\n\n".join(context_parts)

    async def _generate_response(self, query: str, context: str, user_profile: Dict = None) -> str:
        """
        Generate a response using OpenAI based on retrieved documents and user context
        """
        # Create prompt for OpenAI
        prompt = self._build_prompt(query, context, user_profile)

        # Call OpenAI API
        try:
            response = await self.openai_client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": self._get_system_prompt(user_profile)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
                stream=False
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"I'm sorry, I encountered an error processing your query: {str(e)}. Please try again."

    async def _generate_response_with_selected_text(self, query: str, selected_text: str, context: str, user_profile: Dict = None) -> str:
        """
        Generate a response considering the selected text context
        """
        # Create prompt for OpenAI with selected text emphasis
        prompt = self._build_selected_text_prompt(query, selected_text, context, user_profile)

        # Call OpenAI API
        try:
            response = await self.openai_client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": self._get_system_prompt_for_selected_text(user_profile)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
                stream=False
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"I'm sorry, I encountered an error processing your query: {str(e)}. Please try again."

    def _build_prompt(self, query: str, context: str, user_profile: Dict = None) -> str:
        """
        Build the prompt for normal queries
        """
        return f"""You are an expert assistant for the Physical AI & Humanoid Robotics textbook. Answer the user's question based on the provided context from the textbook.

Guidelines:
- Always be factual and refer to the textbook content when possible
- If the context doesn't contain enough information to answer the question, say so and suggest related topics
- Provide clear explanations suitable for the user's academic level
- Include relevant citations to textbook sections when possible

Context from textbook:
{context}

Question: {query}

Answer (include sources/references to textbook sections):"""

    def _build_selected_text_prompt(self, query: str, selected_text: str, context: str, user_profile: Dict = None) -> str:
        """
        Build the prompt for selected text queries
        """
        return f"""You are an expert assistant for the Physical AI & Humanoid Robotics textbook. The user has highlighted specific text and is asking a question about it.

Highlighted text: "{selected_text}"

Based on this highlighted text and the additional context from the textbook, answer the user's question.

Guidelines:
- Address the highlighted text directly in your response
- Connect the highlighted text to the user's question
- Use the additional context to provide comprehensive answers
- Always be factual and refer to the textbook content when possible
- If the context doesn't contain enough information to answer the question, say so and suggest related topics
- Provide clear explanations suitable for the user's academic level

Additional context from textbook:
{context}

Question: {query}

Answer (include sources/references to textbook sections):"""

    def _get_system_prompt(self, user_profile: Dict = None) -> str:
        """
        Get the system prompt based on user profile
        """
        base_prompt = "You are an expert assistant for the Physical AI & Humanoid Robotics textbook. Provide accurate, helpful answers to student questions based on the textbook content. Be factual, clear, and educational. Include citations to specific textbook sections when possible. If the provided context doesn't contain sufficient information, acknowledge this and suggest related topics the user might explore."

        if user_profile:
            level = user_profile.get('level', 'intermediate')
            if level == 'beginner':
                base_prompt += " Explain concepts in simple terms suitable for beginners."
            elif level == 'advanced':
                base_prompt += " Provide detailed, technical explanations suitable for advanced students."

        return base_prompt

    def _get_system_prompt_for_selected_text(self, user_profile: Dict = None) -> str:
        """
        Get the system prompt for selected text queries
        """
        base_prompt = "You are an expert assistant for the Physical AI & Humanoid Robotics textbook. The user has highlighted specific text and is asking a question about it. Address the highlighted text directly in your response and connect it to the user's question. Provide accurate, helpful answers based on the textbook content. Be factual, clear, and educational. Include citations to specific textbook sections when possible."

        if user_profile:
            level = user_profile.get('level', 'intermediate')
            if level == 'beginner':
                base_prompt += " Explain concepts in simple terms suitable for beginners."
            elif level == 'advanced':
                base_prompt += " Provide detailed, technical explanations suitable for advanced students."

        return base_prompt

    def _prepare_sources(self, docs: List[Dict]) -> List[Dict[str, Any]]:
        """
        Prepare sources for citation
        """
        sources = []
        for doc in docs:
            source = {
                "id": doc.get('id'),
                "title": doc.get('title', 'Unknown'),
                "chapter": doc.get('chapter', 'Unknown'),
                "section": doc.get('section', 'Unknown'),
                "relevance_score": doc.get('score', 0.0),
                "content_preview": doc.get('content', '')[:200] + "..." if len(doc.get('content', '')) > 200 else doc.get('content', '')
            }
            sources.append(source)

        return sources