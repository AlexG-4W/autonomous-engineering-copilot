from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore


class Embedder:
    """
    A class to handle text vectorization using sentence-transformers.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """
        Initializes the embedder with the given model.

        Args:
            model_name (str): The name of the sentence-transformers model to load.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of text strings.

        Args:
            texts (List[str]): The list of text chunks to vectorize.

        Returns:
            List[List[float]]: The resulting embedding vectors.
        """
        if not texts:
            return []

        embeddings = self.model.encode(texts, convert_to_numpy=True)

        if isinstance(embeddings, np.ndarray):
            return list(embeddings.tolist())

        return [list(e) for e in embeddings]  # type: ignore
