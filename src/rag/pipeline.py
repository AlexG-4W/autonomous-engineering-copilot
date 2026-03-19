import os
from typing import Any
from src.ingestion.pdf_extractor import extract_text_from_pdf
from src.ingestion.csv_extractor import extract_text_from_csv
from src.rag.chunker import chunk_text
from src.rag.embedder import Embedder
from src.rag.database import Database
from src.rag.generator import Generator


class RAGPipeline:
    """
    End-to-End RAG Pipeline for ingestion, vectorization, storage, and generation.
    """

    def __init__(self, db_uri: str = "./lancedb", model_path: str = "model.gguf"):
        """
        Initializes the full RAG pipeline.

        Args:
            db_uri (str): URI for LanceDB.
            model_path (str): Local path to the GGUF model for llama-cpp-python.
        """
        self.db = Database(uri=db_uri)
        self.embedder = Embedder()
        self.generator = Generator(model_path=model_path)
        self.table_name = "knowledge_base"
        self.db.create_table(self.table_name)

    def ingest_document(self, file_path: str) -> None:
        """
        Ingests a document by extracting text, chunking, vectorizing, and storing it.

        Args:
            file_path (str): The path to the document to ingest.
        """
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".csv"):
            text = extract_text_from_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format for {file_path}")

        metadata = {"source": os.path.basename(file_path)}
        chunks = chunk_text(text, metadata=metadata)

        if chunks:
            texts = [c["text"] for c in chunks]
            embeddings = self.embedder.generate_embeddings(texts)
            self.db.add_chunks(self.table_name, chunks, embeddings)

    def query(self, user_query: str, top_k: int = 3, **kwargs: Any) -> Any:
        """
        Processes a user query and returns a generated RAG response.

        Args:
            user_query (str): The question to ask.
            top_k (int): Number of context chunks to retrieve. Defaults to 3.
            **kwargs: Extra parameters passed to the generator (e.g. stream, max_tokens)

        Returns:
            str | Iterator[Any]: The final generated answer or generator.
        """
        query_embedding = self.embedder.generate_embeddings([user_query])[0]
        results = self.db.search(self.table_name, query_embedding, limit=top_k)

        contexts = [res.get("text", "") for res in results]
        return self.generator.generate_rag_response(user_query, contexts, **kwargs)
