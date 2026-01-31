from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class QdrantVectorStore:
    def __init__(self):
        # Initialize Qdrant client - prefer cloud if URL contains https
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

        if qdrant_url.startswith("https://"):
            # Cloud Qdrant setup
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=os.getenv("QDRANT_API_KEY"),
                prefer_grpc=True
            )
        else:
            # Local Qdrant setup
            self.client = QdrantClient(
                url=qdrant_url,
                port=int(os.getenv("QDRANT_PORT", 6333))
            )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))

        # Collection name for textbook content
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_textbook")

    async def initialize(self):
        """
        Initialize the Qdrant collection if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_model.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection '{self.collection_name}'")

            # Optionally populate with initial content
            await self._populate_initial_content()

    async def _populate_initial_content(self):
        """
        Populate the vector database with initial textbook content
        """
        print("Populating initial textbook content...")

        # Define possible paths for English and Urdu docs
        base_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "frontend"),  # Relative to services
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend"),  # Alternative path
            os.path.join(os.getcwd(), "PhysicalAI_Book", "frontend"),  # From project root
        ]

        en_docs_dir = None
        ur_docs_dir = None

        # Find English and Urdu docs directories
        for base_path in base_paths:
            abs_base_path = os.path.abspath(base_path)
            en_path = os.path.join(abs_base_path, "docs")
            ur_path = os.path.join(abs_base_path, "docs-ur")

            if os.path.exists(en_path):
                en_docs_dir = en_path
            if os.path.exists(ur_path):
                ur_docs_dir = ur_path

            if en_docs_dir or ur_docs_dir:
                print(f"Found docs base at: {abs_base_path}")
                break

        if en_docs_dir or ur_docs_dir:
            if en_docs_dir:
                print(f"Found English docs directory: {en_docs_dir}")
            if ur_docs_dir:
                print(f"Found Urdu docs directory: {ur_docs_dir}")

            await self._index_docs_directories(en_docs_dir or "", ur_docs_dir)
        else:
            print("Neither English nor Urdu docs directories found in any expected location, skipping initial content population")

    async def _index_docs_directory(self, docs_dir: str):
        """
        Index all markdown files in the docs directory
        """
        import os

        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Extract title and section info from filename/path
                        title = os.path.splitext(file)[0]
                        section = os.path.relpath(root, docs_dir)

                        # Determine language based on directory path
                        language = "ur" if "ur" in docs_dir.lower() else "en"

                        # Add to vector store
                        doc_id = self.add_document(
                            content=content,
                            title=title,
                            chapter=section,
                            section=title,
                            language=language
                        )

                        print(f"Indexed document: {file_path} with ID: {doc_id}")
                    except Exception as e:
                        print(f"Error indexing {file_path}: {e}")

    async def _index_docs_directories(self, en_docs_dir: str, ur_docs_dir: str = None):
        """
        Index both English and Urdu markdown files in the docs directories
        """
        print("Indexing English documents...")
        await self._index_docs_directory(en_docs_dir)

        if ur_docs_dir and os.path.exists(ur_docs_dir):
            print("Indexing Urdu documents...")
            await self._index_docs_directory(ur_docs_dir)
        else:
            print("Urdu docs directory not found, continuing with English docs only")

    async def search_similar(self, query: str, limit: int = 5, language: str = None) -> List[Dict[str, Any]]:
        """
        Search for similar content in the vector database
        """
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode(query).tolist()

        # Prepare search filter if language is specified
        search_filter = None
        if language:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="language",
                        match=MatchValue(value=language)
                    )
                ]
            )

        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True,
            query_filter=search_filter  # Apply language filter if specified
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "content": hit.payload["content"],
                "title": hit.payload["title"],
                "chapter": hit.payload["chapter"],
                "section": hit.payload["section"],
                "language": hit.payload.get("language", "en")  # Include language in result
            })

        return results

    def add_document(self, content: str, title: str, chapter: str, section: str, language: str = "en") -> str:
        """
        Add a new document to the vector database
        """
        # Generate embedding for the content
        embedding = self.embedding_model.encode(content).tolist()

        # Create a point for Qdrant
        point_id = str(uuid.uuid4())
        point = models.PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "content": content,
                "title": title,
                "chapter": chapter,
                "section": section,
                "language": language,
                "id": point_id
            }
        )

        # Upload point to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        return point_id

    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the vector database
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[document_id])
            )
            return True
        except:
            return False

    def get_all_chapters(self) -> List[str]:
        """
        Get a list of all chapters in the knowledge base
        """
        # Get all unique chapters
        scroll_result = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000,  # Adjust based on your needs
            with_payload=True
        )

        chapters = set()
        for point, _ in scroll_result:
            if 'chapter' in point.payload:
                chapters.add(point.payload['chapter'])

        return list(chapters)