from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDBService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
            # Uncomment if using cloud Qdrant
            # api_key=os.getenv("QDRANT_API_KEY")
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Collection name for textbook content
        self.collection_name = "physical_ai_textbook"

        # Initialize the collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection for textbook content"""
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

            # Add sample textbook content
            self._populate_sample_content()

    def _populate_sample_content(self):
        """Populate the vector database with sample textbook content"""
        print("Populating sample textbook content...")

        # Sample textbook content organized by chapters
        textbook_content = [
            {
                "id": "intro_physical_ai_1",
                "content": "Physical AI represents a paradigm shift in artificial intelligence, moving beyond traditional digital computation to embrace the challenges and opportunities of intelligent systems operating in the physical world. Unlike conventional AI that processes abstract symbols and data, Physical AI integrates perception, reasoning, and action within real-world environments.",
                "title": "Introduction to Physical AI",
                "chapter": "Introduction to Physical AI",
                "section": "Overview"
            },
            {
                "id": "intro_physical_ai_2",
                "content": "Physical AI encompasses the design and implementation of intelligent systems that interact with and operate within physical environments. These systems must handle uncertainty, dynamics, and the complex interplay between computational processes and physical laws.",
                "title": "What is Physical AI?",
                "chapter": "Introduction to Physical AI",
                "section": "Core Concepts"
            },
            {
                "id": "ros2_overview_1",
                "content": "The Robot Operating System 2 (ROS2) serves as the nervous system for modern robotic platforms, providing the foundational infrastructure for communication, coordination, and control. Unlike a simple communication protocol, ROS2 embodies a comprehensive ecosystem of tools, libraries, and conventions that enable complex robotic behaviors.",
                "title": "ROS2 Nervous System",
                "chapter": "ROS2 Nervous System",
                "section": "Overview"
            },
            {
                "id": "ros2_architecture_1",
                "content": "ROS2 adopts Data Distribution Service (DDS) as its underlying communication layer, providing Quality of Service (QoS) policies for different communication needs, real-time performance with deterministic message delivery, fault tolerance and redundancy capabilities, and language interoperability beyond C++ and Python.",
                "title": "ROS2 Architecture",
                "chapter": "ROS2 Nervous System",
                "section": "Core Concepts"
            },
            {
                "id": "gazebo_digital_twin_1",
                "content": "Gazebo serves as the premier simulation environment for robotics, functioning as a digital twin that mirrors the physical world with remarkable fidelity. This simulation platform enables rapid prototyping, testing, and validation of robotic systems before deployment in the real world, dramatically reducing development time and costs while improving safety.",
                "title": "Gazebo Digital Twin",
                "chapter": "Gazebo Digital Twin",
                "section": "Overview"
            },
            {
                "id": "nvidia_isaac_1",
                "content": "The NVIDIA Isaac platform represents the cutting-edge of AI-powered robotics, serving as the 'brain' for intelligent robotic systems. Built on NVIDIA's extensive GPU computing expertise, Isaac provides a comprehensive suite of tools, libraries, and frameworks specifically designed for developing, training, and deploying AI-driven robotic applications.",
                "title": "NVIDIA Isaac Brain",
                "chapter": "NVIDIA Isaac Brain",
                "section": "Overview"
            },
            {
                "id": "vla_framework_1",
                "content": "Vision-Language-Action (VLA) represents a paradigm shift in robotics, where robots can perceive visual information, understand natural language instructions, and execute complex physical actions in a unified framework. This integration enables robots to interact naturally with humans and adapt to novel situations through language-guided behavior.",
                "title": "Vision Language Action",
                "chapter": "Vision Language Action",
                "section": "Overview"
            },
            {
                "id": "humanoid_robots_1",
                "content": "Humanoid robotics represents the pinnacle of physical AI, creating anthropomorphic machines that mirror human form, movement, and behavior. These sophisticated systems integrate mechanical engineering, artificial intelligence, and biomechanics to achieve human-like mobility, dexterity, and interaction capabilities.",
                "title": "Humanoid Robotics",
                "chapter": "Humanoid Robotics",
                "section": "Overview"
            },
            {
                "id": "locomotion_zmp_1",
                "content": "The Zero Moment Point (ZMP) criterion ensures stable walking by maintaining the center of pressure under the center of mass. This is crucial for humanoid robot stability during bipedal locomotion.",
                "title": "ZMP Locomotion Control",
                "chapter": "Humanoid Robotics",
                "section": "Locomotion and Gait Control"
            },
            {
                "id": "capstone_project_1",
                "content": "The capstone project synthesizes all concepts covered throughout this textbook into a comprehensive Physical AI system. Students will design, implement, and deploy an integrated humanoid robot capable of perceiving its environment, understanding natural language instructions, and executing complex physical tasks.",
                "title": "Capstone Project",
                "chapter": "Capstone Project",
                "section": "Overview"
            }
        ]

        # Add content to vector database
        points = []
        for item in textbook_content:
            # Generate embedding for the content
            embedding = self.embedding_model.encode(item['content']).tolist()

            # Create a point for Qdrant
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": item['content'],
                    "title": item['title'],
                    "chapter": item['chapter'],
                    "section": item['section'],
                    "id": item['id']
                }
            )
            points.append(point)

        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"Added {len(textbook_content)} sample textbook entries to vector database")

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content in the vector database"""
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
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
                "section": hit.payload["section"]
            })

        return results

    def add_document(self, content: str, title: str, chapter: str, section: str) -> str:
        """Add a new document to the vector database"""
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
        """Delete a document from the vector database"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[document_id])
            )
            return True
        except:
            return False

    def get_all_chapters(self) -> List[str]:
        """Get a list of all chapters in the knowledge base"""
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