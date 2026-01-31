"""
Document loader for Physical AI textbook in English and Urdu
"""
import os
import re
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    def __init__(self, docs_path: str = "PhysicalAI_Book/frontend/docs",
                 docs_ur_path: str = "PhysicalAI_Book/frontend/docs-ur"):
        self.docs_path = docs_path
        self.docs_ur_path = docs_ur_path

    def load_documents(self, language: str = "en") -> List[Dict[str, str]]:
        """
        Load documents for the specified language
        """
        if language.lower() == "ur":
            docs_dir = self.docs_ur_path
            lang_label = "ur"
        else:
            docs_dir = self.docs_path
            lang_label = "en"

        documents = []

        # Walk through all markdown files in the docs directory
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Extract title from first H1 header
                        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                        title = title_match.group(1) if title_match else file.replace('.md', '')

                        # Create document metadata
                        rel_path = os.path.relpath(file_path, self.docs_path if lang_label == "en" else self.docs_ur_path)

                        document = {
                            'id': f"{lang_label}_{rel_path}",
                            'content': content,
                            'title': title,
                            'path': rel_path,
                            'language': lang_label,
                            'source': file_path
                        }

                        documents.append(document)
                        logger.info(f"Loaded document: {document['id']}")

                    except Exception as e:
                        logger.error(f"Error loading document {file_path}: {str(e)}")

        logger.info(f"Loaded {len(documents)} documents for language: {language}")
        return documents

    def chunk_document(self, document: Dict[str, str], chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, str]]:
        """
        Chunk a document into smaller pieces
        """
        content = document['content']
        chunks = []

        # Split content into sentences to avoid breaking mid-sentence
        sentences = re.split(r'[.!?]+\s+', content)

        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            # Add some context like title to each chunk
            sentence_with_context = f"{document['title']}: {sentence}"

            if current_length + len(sentence_with_context) > chunk_size and current_chunk:
                # Save current chunk
                chunk_doc = {
                    'id': f"{document['id']}_chunk_{len(chunks)}",
                    'content': current_chunk.strip(),
                    'title': document['title'],
                    'path': document['path'],
                    'language': document['language'],
                    'source': document['source'],
                    'original_id': document['id']
                }
                chunks.append(chunk_doc)

                # Start new chunk with overlap
                overlap_sentences = []
                temp_len = 0
                for s in reversed(current_chunk.split('. ')):
                    if temp_len + len(s) < overlap:
                        overlap_sentences.insert(0, s)
                        temp_len += len(s)
                    else:
                        break

                current_chunk = '. '.join(overlap_sentences) + '. ' + sentence_with_context
                current_length = len(current_chunk)
            else:
                current_chunk += " " + sentence_with_context
                current_length += len(sentence_with_context)

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk_doc = {
                'id': f"{document['id']}_chunk_{len(chunks)}",
                'content': current_chunk.strip(),
                'title': document['title'],
                'path': document['path'],
                'language': document['language'],
                'source': document['source'],
                'original_id': document['id']
            }
            chunks.append(chunk_doc)

        logger.info(f"Document {document['id']} chunked into {len(chunks)} pieces")
        return chunks

    def load_and_chunk_documents(self, language: str = "en", chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, str]]:
        """
        Load and chunk documents for the specified language
        """
        documents = self.load_documents(language)
        all_chunks = []

        for doc in documents:
            chunks = self.chunk_document(doc, chunk_size, overlap)
            all_chunks.extend(chunks)

        return all_chunks

# Example usage
if __name__ == "__main__":
    loader = DocumentLoader()

    # Load English documents
    print("Loading English documents...")
    en_chunks = loader.load_and_chunk_documents("en")
    print(f"Loaded {len(en_chunks)} English chunks")

    # Load Urdu documents
    print("Loading Urdu documents...")
    ur_chunks = loader.load_and_chunk_documents("ur")
    print(f"Loaded {len(ur_chunks)} Urdu chunks")