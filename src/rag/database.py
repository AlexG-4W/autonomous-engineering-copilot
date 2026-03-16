import lancedb  # type: ignore
import pyarrow as pa  # type: ignore
import json
import uuid
from typing import List, Dict, Any


class Database:
    """
    Handles storage and retrieval of vector embeddings and text chunks using LanceDB.
    """

    def __init__(self, uri: str = "./lancedb") -> None:
        """
        Initializes the database connection.

        Args:
            uri (str): The URI for the LanceDB instance.
        """
        self.uri = uri
        self.db = lancedb.connect(self.uri)

    def create_table(self, name: str, dimension: int = 384) -> Any:
        """
        Creates or opens an existing LanceDB table.

        Args:
            name (str): Name of the table.
            dimension (int): The dimensionality of the vectors.

        Returns:
            The opened table.
        """
        schema = pa.schema(
            [
                pa.field("id", pa.string()),
                pa.field("vector", pa.list_(pa.float32(), dimension)),
                pa.field("text", pa.string()),
                pa.field("metadata", pa.string()),
            ]
        )
        # Handle deprecation warning for table_names
        tables = (
            self.db.table_names()
            if hasattr(self.db, "table_names")
            else self.db.list_tables()
        )
        if name in tables:
            return self.db.open_table(name)
        return self.db.create_table(name, schema=schema)

    def add_chunks(
        self,
        table_name: str,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> None:
        """
        Adds text chunks and their embeddings to the table.

        Args:
            table_name (str): The table to add data to.
            chunks (List[Dict[str, Any]]): List of chunk dictionaries
                containing 'text' and 'metadata'.
            embeddings (List[List[float]]): List of embedding vectors.
        """
        table = self.db.open_table(table_name)
        data = []
        for chunk, emb in zip(chunks, embeddings):
            data.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": emb,
                    "text": chunk.get("text", ""),
                    "metadata": json.dumps(chunk.get("metadata", {})),
                }
            )
        table.add(data)

    def search(
        self, table_name: str, query_vector: List[float], limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Searches the table for vectors closest to the query_vector.

        Args:
            table_name (str): The table to search in.
            query_vector (List[float]): The embedding query vector.
            limit (int): Number of results to return.

        Returns:
            List[Dict[str, Any]]: List of results, including text and parsed metadata.
        """
        table = self.db.open_table(table_name)
        results = table.search(query_vector).limit(limit).to_list()

        parsed_results = []
        for res in results:
            if "metadata" in res and isinstance(res["metadata"], str):
                res["metadata"] = json.loads(res["metadata"])
            parsed_results.append(res)
        return parsed_results
