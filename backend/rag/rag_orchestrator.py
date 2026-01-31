"""
RAG Orchestrator for Physical AI textbook
Manages the entire RAG pipeline: loading, indexing, and retrieval
"""
import logging
from typing import List, Dict, Optional
from .document_loader import DocumentLoader
from .embedding_engine import VectorStore
import os

logger = logging.getLogger(__name__)

class RAGOrchestrator:
    def __init__(self, docs_path: str = "PhysicalAI_Book/frontend/docs",
                 docs_ur_path: str = "PhysicalAI_Book/frontend/docs-ur",
                 vector_store_path: str = "PhysicalAI_Book/vector_store.pkl"):
        """
        Initialize the RAG orchestrator
        """
        self.document_loader = DocumentLoader(docs_path, docs_ur_path)
        self.vector_store = VectorStore(vector_store_path)
        self.is_initialized = False

    def initialize_index(self, rebuild: bool = False):
        """
        Initialize or rebuild the document index
        """
        if not rebuild and self.vector_store.get_embedding_count() > 0:
            logger.info("Vector store already exists, skipping initialization")
            self.is_initialized = True
            return

        logger.info("Initializing RAG index...")

        # Load and chunk English documents
        logger.info("Loading English documents...")
        en_chunks = self.document_loader.load_and_chunk_documents("en")
        logger.info(f"Loaded {len(en_chunks)} English document chunks")

        # Load and chunk Urdu documents
        logger.info("Loading Urdu documents...")
        ur_chunks = self.document_loader.load_and_chunk_documents("ur")
        logger.info(f"Loaded {len(ur_chunks)} Urdu document chunks")

        # Combine all chunks
        all_chunks = en_chunks + ur_chunks

        # Add documents to vector store
        logger.info("Adding documents to vector store...")
        self.vector_store.add_documents_batch(all_chunks)

        # Save the vector store
        self.vector_store.save()

        logger.info(f"RAG index initialized with {len(all_chunks)} document chunks")
        self.is_initialized = True

    def query(self, question: str, language: str = "en", top_k: int = 3) -> Dict:
        """
        Query the RAG system
        """
        if not self.is_initialized:
            raise ValueError("RAG system not initialized. Call initialize_index() first.")

        # Search for relevant documents
        search_results = self.vector_store.search(
            query=question,
            language=language,
            top_k=top_k
        )

        # Prepare response
        response = {
            "question": question,
            "language": language,
            "retrieved_documents": search_results,
            "answer": self._generate_answer(question, search_results, language)
        }

        logger.info(f"Query processed: '{question}' in language {language}")
        return response

    def _generate_answer(self, question: str, retrieved_docs: List[Dict], language: str = "en") -> str:
        """
        Generate an answer based on retrieved documents
        """
        if not retrieved_docs:
            if language == "ur":
                return "معذرت، میں آپ کے سوال کا جواب دینے کے لیے متعلقہ دستاویزات نہیں تلاش کر سکا۔"
            else:
                return "Sorry, I couldn't find relevant documents to answer your question."

        # Concatenate relevant content
        context_parts = []
        for doc in retrieved_docs:
            content = doc['content'][:500]  # Limit content length
            context_parts.append(content)

        context = "\n\n".join(context_parts)

        # Generate response based on language
        if language == "ur":
            answer = f"آپ کے سوال کے مطابق، مندرجہ ذیل معلومات متعلقہ دستاویزات سے حاصل کی گئی ہے:\n\n{context[:1000]}..."
        else:
            answer = f"Based on the relevant documents, here's the information:\n\n{context[:1000]}..."

        return answer

    def get_document_count(self, language: str = None) -> int:
        """
        Get the number of indexed documents
        """
        return self.vector_store.get_embedding_count(language)

# Example usage and testing
if __name__ == "__main__":
    # Initialize RAG orchestrator
    rag = RAGOrchestrator()

    # Initialize the index (this will load and embed all documents)
    rag.initialize_index()

    # Test queries in English
    print("Testing English query:")
    result_en = rag.query("What is Physical AI?", language="en")
    print(f"Question: {result_en['question']}")
    print(f"Answer: {result_en['answer']}")
    print(f"Retrieved {len(result_en['retrieved_documents'])} documents\n")

    # Test queries in Urdu
    print("Testing Urdu query:")
    result_ur = rag.query("فزکل AI کیا ہے؟", language="ur")
    print(f"Question: {result_ur['question']}")
    print(f"Answer: {result_ur['answer']}")
    print(f"Retrieved {len(result_ur['retrieved_documents'])} documents")