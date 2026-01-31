"""
Embedding engine for Physical AI textbook content
Uses sentence transformers for multilingual support
"""
import numpy as np
from typing import List, Dict, Union
import logging
from sentence_transformers import SentenceTransformer
import pickle
import os
import hashlib

logger = logging.getLogger(__name__)

class EmbeddingEngine:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize the embedding engine with a multilingual model
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        logger.info(f"Initialized embedding model: {model_name}")

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode text(s) into embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        # Handle empty texts
        processed_texts = []
        for text in texts:
            if not text or text.isspace():
                processed_texts.append("empty")
            else:
                processed_texts.append(text)

        embeddings = self.model.encode(processed_texts)
        return embeddings

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        if vec1.ndim == 1:
            vec1 = vec1.reshape(1, -1)
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)

        dot_product = np.dot(vec1, vec2.T)
        norm_vec1 = np.linalg.norm(vec1, axis=1, keepdims=True)
        norm_vec2 = np.linalg.norm(vec2, axis=1, keepdims=True)
        similarity = dot_product / (norm_vec1 * norm_vec2)
        return float(similarity[0][0])

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        """
        sample_text = ["test"]
        embedding = self.encode(sample_text)
        return embedding.shape[1]

class VectorStore:
    def __init__(self, storage_path: str = "PhysicalAI_Book/vector_store.pkl"):
        """
        Initialize vector store with persistent storage
        """
        self.storage_path = storage_path
        self.embeddings = {}  # id -> embedding vector
        self.documents = {}   # id -> document metadata
        self.language_embeddings = {"en": {}, "ur": {}}  # separate stores by language
        self.embedding_engine = EmbeddingEngine()

        # Load existing data if available
        self.load()

    def add_document(self, doc_id: str, content: str, metadata: Dict, language: str = "en"):
        """
        Add a document to the vector store
        """
        try:
            # Generate embedding for the content
            embedding = self.embedding_engine.encode(content)[0]

            # Store embedding and document
            self.embeddings[doc_id] = embedding
            self.documents[doc_id] = {
                "content": content,
                "metadata": metadata
            }

            # Add to language-specific store
            if language not in self.language_embeddings:
                self.language_embeddings[language] = {}
            self.language_embeddings[language][doc_id] = embedding

            logger.info(f"Added document to vector store: {doc_id} (lang: {language})")
        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {str(e)}")

    def add_documents_batch(self, documents: List[Dict]):
        """
        Add multiple documents efficiently
        """
        contents = []
        doc_data = []

        for doc in documents:
            contents.append(doc.get('content', ''))
            doc_data.append({
                'id': doc['id'],
                'metadata': {
                    'title': doc.get('title', ''),
                    'path': doc.get('path', ''),
                    'language': doc.get('language', 'en'),
                    'source': doc.get('source', '')
                }
            })

        # Batch encode all contents
        embeddings = self.embedding_engine.encode(contents)

        # Add each document
        for i, doc_info in enumerate(doc_data):
            doc_id = doc_info['id']
            self.embeddings[doc_id] = embeddings[i]
            self.documents[doc_id] = {
                "content": contents[i],
                "metadata": doc_info['metadata']
            }

            lang = doc_info['metadata']['language']
            if lang not in self.language_embeddings:
                self.language_embeddings[lang] = {}
            self.language_embeddings[lang][doc_id] = embeddings[i]

        logger.info(f"Added {len(documents)} documents to vector store in batch")

    def search(self, query: str, language: str = "en", top_k: int = 5) -> List[Dict]:
        """
        Search for documents similar to the query in the specified language
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_engine.encode(query)[0]

            # Get embeddings for the specified language
            lang_embeddings = self.language_embeddings.get(language, {})
            if not lang_embeddings:
                logger.warning(f"No embeddings found for language: {language}")
                return []

            # Calculate similarities
            similarities = []
            for doc_id, emb in lang_embeddings.items():
                similarity = self.embedding_engine.cosine_similarity(query_embedding, emb)
                similarities.append((doc_id, similarity))

            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Get top-k results
            top_results = similarities[:top_k]

            # Format results
            results = []
            for doc_id, score in top_results:
                if doc_id in self.documents:
                    doc = self.documents[doc_id]
                    results.append({
                        "id": doc_id,
                        "content": doc["content"],
                        "metadata": doc["metadata"],
                        "score": float(score)
                    })

            logger.info(f"Search query '{query}' returned {len(results)} results for language {language}")
            return results

        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []

    def save(self):
        """
        Save vector store to disk
        """
        try:
            data = {
                'embeddings': self.embeddings,
                'documents': self.documents,
                'language_embeddings': self.language_embeddings
            }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

            with open(self.storage_path, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"Vector store saved to {self.storage_path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")

    def load(self):
        """
        Load vector store from disk
        """
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'rb') as f:
                    data = pickle.load(f)

                self.embeddings = data.get('embeddings', {})
                self.documents = data.get('documents', {})
                self.language_embeddings = data.get('language_embeddings', {"en": {}, "ur": {}})

                logger.info(f"Vector store loaded from {self.storage_path}")
            else:
                logger.info("No existing vector store found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            # Initialize empty stores
            self.embeddings = {}
            self.documents = {}
            self.language_embeddings = {"en": {}, "ur": {}}

    def get_embedding_count(self, language: str = None) -> int:
        """
        Get the number of embeddings in the store
        """
        if language:
            return len(self.language_embeddings.get(language, {}))
        else:
            return len(self.embeddings)

# Example usage
if __name__ == "__main__":
    # Initialize vector store
    vs = VectorStore()

    # Sample documents
    sample_docs = [
        {
            "id": "en_sample_1",
            "content": "Introduction to Physical AI and robotics systems",
            "title": "Introduction",
            "path": "docs/intro.md",
            "language": "en",
            "source": "docs/intro.md"
        },
        {
            "id": "ur_sample_1",
            "content": "فزکل AI اور روبوٹس سسٹمز کا تعارف",
            "title": "تعارف",
            "path": "docs-ur/intro.md",
            "language": "ur",
            "source": "docs-ur/intro.md"
        }
    ]

    # Add documents to store
    vs.add_documents_batch(sample_docs)

    # Search
    results = vs.search("Physical AI", language="en", top_k=2)
    print(f"Search results: {results}")

    # Save
    vs.save()