from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        # Initialize embedding model
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str] or str) -> List[List[float]] or List[float]:
        """
        Encode text(s) into embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(texts)

        # Convert to list of lists if single text, otherwise list of embeddings
        if len(texts) == 1:
            return embeddings[0].tolist()
        else:
            return embeddings.tolist()

    def get_sentence_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings
        """
        return self.model.get_sentence_embedding_dimension()

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        """
        emb1 = np.array(self.encode(text1)).reshape(1, -1)
        emb2 = np.array(self.encode(text2)).reshape(1, -1)

        from sklearn.metrics.pairwise import cosine_similarity
        similarity_score = cosine_similarity(emb1, emb2)[0][0]

        return float(similarity_score)