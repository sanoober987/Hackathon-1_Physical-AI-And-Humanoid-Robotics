"""
Setup script for Physical AI Assistant Backend
"""
from setuptools import setup, find_packages

setup(
    name="physical-ai-assistant-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sentence-transformers==2.2.2",
        "torch==2.1.0",
        "numpy==1.24.3",
        "pydantic==2.5.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "transformers==4.35.0",
        "scikit-learn==1.3.0",
        "sqlite3"
    ],
    author="Physical AI Team",
    author_email="info@physicalai-book.com",
    description="Backend for Physical AI Assistant with RAG capabilities",
    python_requires=">=3.8",
)